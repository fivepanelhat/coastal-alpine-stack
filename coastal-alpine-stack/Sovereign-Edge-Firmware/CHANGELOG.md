# Changelog

All notable changes to the ESP32 `Sovereign-Edge-Firmware` will be documented in this file.

## [1.2.0] - 2026-06-08

### Added
- Added secure mTLS MQTT client connection hooks targeting port `8883`.
- Added dynamic telemetry publishers (`publishSensorData`).
- Added exponential backoff circuit breakers for reconnect attempts (capping at 60s max delay).
- Added PubSubClient dependency config in `platformio.ini`.

## [1.1.0] - 2026-06-07

### Added
- Added local JWT handshake client (`edge_auth.cpp`).
- Configured JSON parsing libraries for edge payload structures.

## [1.0.0] - 2026-06-07

### Added
- Initialized PlatformIO configuration.
- Configured board definitions for `esp32dev` targets.
- Created baseline WiFi connection wrapper.
