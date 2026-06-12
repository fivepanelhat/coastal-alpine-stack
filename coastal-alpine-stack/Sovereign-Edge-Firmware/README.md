# Sovereign Edge Firmware

![CI](https://github.com/UNKNOWN_OWNER/Sovereign-Edge-Firmware/actions/workflows/secops.yml/badge.svg?branch=main)

![Hardware Target](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%2016GB-C11A5B?style=flat-square&logo=raspberry-pi&logoColor=white) ![NPU Acceleration](https://img.shields.io/badge/NPU-Hailo--10H%20Accelerated-005A9C?style=flat-square) ![Protocols](https://img.shields.io/badge/Interop-MQTT%20%7C%20OPC--UA-orange?style=flat-square)

**Coastal Alpine Tech Limited**
Firmware repository for ESP32 edge nodes operating within the Sovereign AI Stack. 

## Architecture
This firmware is designed to operate completely off-grid, utilizing local ES256 JWT authentication via the Blue-Moon-Portal, communicating over mTLS-secured MQTT.

## SecOps Notice
Never commit `secrets.h` to this repository. All physical node configurations must remain local to the deployment site.
