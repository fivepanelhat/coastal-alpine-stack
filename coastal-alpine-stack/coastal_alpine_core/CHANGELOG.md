# Changelog

All notable changes to the shared `coastal_alpine_core` package will be documented in this file.

## [1.2.0] - 2026-06-08

### Added
- Added Node.js `secure_store.js` using SQLCipher 256-bit AES database encryption at rest.
- Added Node.js `behavioral_analytics.js` for actuator timing and frequency control.
- Added Node.js `power_governor.js` for battery-aware duty cycle offsets.
- Added Python `analytics/input_guard.py` for device posture verification and Z-Score telemetry anomaly checks.
- Added Python `logging/compliance_guard.py` estimating carbon emission mitigation metrics and hash-chained audits.
- Created `dist/index.js` CommonJS entry point.

## [1.1.0] - 2026-06-07

### Added
- Added Node.js `attestation_validator.js` validating TPM 2.0 signatures against "Golden Boot" baseline registers.
- Added Node.js `validation.js` with telemetry clamps.

## [1.0.0] - 2026-06-07

### Added
- Initialized core structure and Python module.
- Added prompt sanitization and tenant scoping checks to `security.py`.
- Added Ollama connection wrapper to `models.py`.
- Added PMIC execution time metrics to `telemetry.py`.
