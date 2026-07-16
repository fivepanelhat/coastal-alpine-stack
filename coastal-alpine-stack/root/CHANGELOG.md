# Changelog

All notable changes to the Coastal Alpine Stack will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-06-08

### Added
- Created `rpi_secops` provisioning systemd & bootloader configuration scripts to enforce high-security read-only root system layouts on Raspberry Pi 5.
- Implemented secure hardware NPU inference initialization script (`Sting-Operation-AI/src/inference.py`) leveraging virtual Hailo NPU mappings.
- Established secure MQTT communication guidelines with JWT extraction, certificate verification, and exponential backoff circuit breakers.
- Integrated lock-stack/unlock-stack shell aliases for runtime firmware write toggles.

## [1.1.0] - 2026-06-07

### Added
- Implemented `AquaGuard-Portal` water quality and aquaculture edge monitor.
- Integrated `coastal-alpine-core` shared controls for prompt input scanning, automatic connection retries, and hardware latency/power logging.
- Created Pydantic compliance schemas for sensors, reasoning plans, and council audits.
- Implemented `ComplianceExporter` generating New Zealand regional council compliant CSV logs and detailed JSON audits (targeting NES-F and NES-MA).
- Configured thresholds mapping parameters for pH, dissolved oxygen, temperature, turbidity, and nitrate.

## [1.0.0] - 2026-06-07

### Added
- Created unified Coastal Alpine Stack monorepo workspace.
- Implemented `coastal-alpine-core` shared Python package containing:
 - `telemetry`: Latency tracking and energy-efficiency metrics.
 - `models`: Robust Ollama client wrapper with auto-retries and health checks.
 - `security`: Sanitization safeguards for input queries and multi-tenant scoping.
- Restructured `weaver`, `Blue-Moon-Portal`, and `Sting-Operation-AI` directories with uniform presentation and metadata.
- Created root `LICENSE`, `.gitignore`, `CONTRIBUTING.md`, `CHANGELOG.md`, and `requirements-dev.txt`.
- Set up Docker environment template for local MQTT and Ollama edge integration.
- Documented NZ agritech, apiculture, and compliance real-world application examples across all modules.
