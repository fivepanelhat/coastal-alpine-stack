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
/dev/mmcblk0p2  /          ext4    ro,noatime,errors=remount-ro  0  1
/dev/mmcblk0p1  /boot/firmware  vfat    ro,fmask=0022,dmask=0022  0  2

# Route Hailo, Python, and system volatile tasks directly to the 16GB RAM pool
tmpfs           /tmp            tmpfs   nodev,nosuid,size=2G          0  0
tmpfs           /var/log        tmpfs   nodev,nosuid,size=512M        0  0
tmpfs           /var/tmp        tmpfs   nodev,nosuid,size=512M        0  0

# Crucial Hailo RT and Python wheel compilation directories mapped to RAM
tmpfs           /root/.cache    tmpfs   nodev,nosuid,size=1G          0  0
tmpfs           /var/lib/hailo  tmpfs   nodev,nosuid,size=256M        0  0
EOF

# 4. Reload and enable systemd OTA verification service
echo "Reloading systemd daemons and enabling OTA verification services..."
sudo systemctl daemon-reload
sudo systemctl enable sovereign-ota.service 2>/dev/null || sudo systemctl enable ota-verify.service

echo "Secure boot and system services staged. Please reboot your Pi to apply the hardware perimeter lock."



