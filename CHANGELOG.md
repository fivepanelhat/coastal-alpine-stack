# Changelog


## Hybrid platform update (July 2026)

- Dual-platform installers: `install.sh` (Linux/macOS) and `install.ps1` (Windows)
- Mermaid system maps updated for hybridisation (Core | Weaver | Aether | stack) and Windows + Linux hosts
- Architecture overview images refreshed for hybrid stack + dual OS targets
- Developer setup / installation docs cover Windows and Linux prerequisites and packages

All notable changes to the Coastal Alpine Stack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased] - 2026-06-16 - Enterprise Hardening & Data Flywheel Release

### Added
- **Full Data Flywheel system** with automatic trajectory recording across all portals
- Hardware outcome recording after every `enforce_plan()` call
- Human-in-the-Loop (HITL) feedback mechanism
- Evaluation loop with rule-based + optional LLM-as-judge scoring
- Golden set curation for future model improvement
- `DataFlywheel` and `Trajectory` classes in `coastal_alpine_core`
- `BayesianOptimisationHook` scaffolding
- New high-level documentation:
 - `ARCHITECTURE.md` (system overview)
 - `DATA_FLYWHEEL_GUIDE.md` (detailed usage guide)
 - Updated root and individual repository READMEs

### Changed
- Replaced legacy input guards with modern `SecurityGuard` + structured `SecurityResult`
- Major upgrade to `TelemetryTracker` (context manager, psutil metrics, structured JSON logging)
- CI/CD standardisation and hardening:
 - All workflows now use Python 3.10 + pip caching
 - Replaced unreliable manual Gitleaks installation with official GitHub Action
 - Made Enterprise CI stricter (reduced error masking)
- Packaging improvements:
 - Added modern `pyproject.toml` to Weaver
 - Improved `pyproject.toml` and dependency management in Coastal-Alpine-Core
- Docker base image aligned to Python 3.10 for consistency

### Improved
- Complete end-to-end Data Flywheel coverage in Blue-Moon-Portal, AquaGuard-Portal, and SoilGuard-Portal
- Sting-Operation-AI now records inference trajectories in `predict.py`
- Weaver integrated with SecurityGuard, Telemetry, and flywheel
- Production K3s manifests created for all major components
- Documentation aligned and improved across the entire stack

### Fixed
- Multiple CI reliability issues (Gitleaks installation, Python version inconsistency, missing caching)

---

## [1.2.0] - 2026-06-08

### Added
- Created `rpi_secops` provisioning scripts for high-security Raspberry Pi 5 configurations.
- Implemented secure hardware NPU inference initialization.
- Established secure MQTT communication guidelines.

## [1.1.0] - 2026-06-07

### Added
- Implemented `AquaGuard-Portal` water quality and aquaculture edge monitor.
- Integrated `coastal-alpine-core` shared controls.
- Created Pydantic compliance schemas and `ComplianceExporter`.

## [1.0.0] - 2026-06-07

### Added
- Created unified Coastal Alpine Stack monorepo.
- Implemented `coastal_alpine_core` shared package.
- Restructured Weaver, Blue-Moon-Portal, and Sting-Operation-AI.

---

*See git history for full details of earlier development.*
