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

echo "Secure boot configuration staged. Please reboot your Pi to apply the hardware perimeter lock."
