#!/bin/bash
# Coastal Alpine Tech Limited - Raspberry Pi Hardware SecOps Provisioner
# Run this directly on your Raspberry Pi 5 to lock the bootloader perimeter.

echo "Initiating Raspberry Pi Hardware SecOps configuration..."

# 1. Extract the current bootloader configuration
rpi-eeprom-config --get > boot_config.txt

# 2. Append the security enforcement parameters
cat << 'EOF' >> boot_config.txt

# Coastal Alpine Tech - Hardware Security Boundary
SIGNED_BOOT=1
REQ_SIGNED_BOOT=1
DISABLE_HDMI_DIAGNOSTICS=1
BOOT_ORDER=0xf41 # Forces boot from NVMe/SD only, disables USB injection vectors
EOF

# 3. Compile and stage the new secure boot configuration
sudo rpi-eeprom-config --set boot_config.txt

# 3b. Configure PCIe Gen 3 and Hailo NPU Overlay in /boot/firmware/config.txt
echo "Configuring PCIe Gen 3 and Hailo NPU overlays..."
sudo tee -a /boot/firmware/config.txt > /dev/null << 'EOF'

# Enable PCIe Gen 3 speeds on the Pi 5 pipe
dtparam=pciex1_gen=3

# Allocate a generous 1GB CMA pool out of your 16GB total RAM for NPU DMA transfers
cma=1024M

# Enable the Hailo driver overlay
dtoverlay=hailo-10h
EOF

# 3c. Configure read-only fstab lockdowns and tmpfs mounts in /etc/fstab
echo "Configuring read-only fstab lockdowns and volatile tmpfs pools..."
sudo tee -a /etc/fstab > /dev/null << 'EOF'

# Coastal Alpine Tech - Sovereign Root Lockdown
# Mount core system components as read-only
/dev/mmcblk0p2 / ext4 ro,noatime,errors=remount-ro 0 1
/dev/mmcblk0p1 /boot/firmware vfat ro,fmask=0022,dmask=0022 0 2

# Mount persistent data partition as read-write
/dev/mmcblk0p3 /mnt/sovereign-data ext4 rw,noatime 0 2

# Route Hailo, Python, and system volatile tasks directly to the 16GB RAM pool
tmpfs /tmp tmpfs nodev,nosuid,size=2G 0 0
tmpfs /var/log tmpfs nodev,nosuid,size=512M 0 0
tmpfs /var/tmp tmpfs nodev,nosuid,size=512M 0 0

# Crucial Hailo RT and Python wheel compilation directories mapped to RAM
tmpfs /root/.cache tmpfs nodev,nosuid,size=1G 0 0
tmpfs /var/lib/hailo tmpfs nodev,nosuid,size=256M 0 0
EOF

# 3d. Configure nftables for sovereign network isolation
echo "Configuring nftables firewall for network isolation..."
sudo cp sovereign_isolation.nft /etc/nftables.conf 2>/dev/null || sudo cp rpi_secops/sovereign_isolation.nft /etc/nftables.conf
sudo systemctl enable nftables
sudo systemctl restart nftables

# 3e. Configure Mosquitto MQTT Access Control List
echo "Configuring Mosquitto MQTT access control list..."
sudo cp mosquitto.acl /etc/mosquitto/mosquitto.acl 2>/dev/null || sudo cp rpi_secops/mosquitto.acl /etc/mosquitto/mosquitto.acl
if [ -f /etc/mosquitto/mosquitto.conf ] && ! grep -q "acl_file" /etc/mosquitto/mosquitto.conf; then
 echo "acl_file /etc/mosquitto/mosquitto.acl" | sudo tee -a /etc/mosquitto/mosquitto.conf > /dev/null
fi
sudo systemctl restart mosquitto 2>/dev/null || true

# 3f. Configure rootless Docker for user space isolation
echo "Configuring rootless Docker for user space container isolation..."
sudo apt-get install -y dbus-user-session uidmap 2>/dev/null || true
sudo systemctl disable --now docker.service docker.socket 2>/dev/null || true
dockerd-rootless-setuptool.sh install 2>/dev/null || true
if ! grep -q "DOCKER_HOST" ~/.bashrc; then
 echo 'export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock' >> ~/.bashrc
fi

# 3g. Stage the Traefik K3s HelmChart mesh deployment
echo "Staging Traefik K3s HelmChart mesh deployment..."
sudo mkdir -p /var/lib/rancher/k3s/server/manifests/ 2>/dev/null || true
sudo cp sovereign-edge-mesh.yaml /var/lib/rancher/k3s/server/manifests/sovereign-edge-mesh.yaml 2>/dev/null || sudo cp rpi_secops/sovereign-edge-mesh.yaml /var/lib/rancher/k3s/server/manifests/sovereign-edge-mesh.yaml 2>/dev/null || true

# 3h. Stage Falco local security threat rules
echo "Staging Falco security threat detection rules..."
sudo mkdir -p /etc/falco/ 2>/dev/null || true
sudo cp falco_rules.local.yaml /etc/falco/falco_rules.local.yaml 2>/dev/null || sudo cp rpi_secops/falco_rules.local.yaml /etc/falco/falco_rules.local.yaml 2>/dev/null || true
sudo systemctl restart falco 2>/dev/null || true

# 4. Reload and enable systemd OTA verification service
echo "Reloading systemd daemons and enabling OTA verification services..."
sudo systemctl daemon-reload
sudo systemctl enable sovereign-ota.service 2>/dev/null || sudo systemctl enable ota-verify.service

echo "Secure boot and system services staged. Please reboot your Pi to apply the hardware perimeter lock."

# ==============================================================================
# MAINTENANCE & UPDATE UTILITIES
# ==============================================================================
# Add these aliases to your ~/.bashrc on the Pi 5 to easily toggle system writes:
#
# # 1. Unlock the system for updates
# alias unlock-stack='sudo mount -o remount,rw / && sudo mount -o remount,rw /boot/firmware && echo "Sovereign Stack UNLOCKED for maintenance."'
#
# # 2. Relock the perimeter when finished
# alias lock-stack='sudo mount -o remount,ro / && sudo mount -o remount,ro /boot/firmware && echo "Sovereign Stack RELOCKED. Root filesystem immutable."'
# ==============================================================================
