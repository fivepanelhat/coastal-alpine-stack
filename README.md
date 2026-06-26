# Coastal Alpine Stack — Sovereign Edge AI Platform

**Coastal Alpine Tech Limited**  
*Edge-Native | Data Sovereign | Self-Improving*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)  
![Hardware](https://img.shields.io/badge/Target-RPi5%20%2B%20Hailo%20NPU-orange)  
![Status](https://img.shields.io/badge/Status-Enterprise%20Hardening%20Phase-green)

A production-grade, sovereign edge AI ecosystem for New Zealand’s primary industries (agriculture, aquaculture, biosecurity). Designed for offline operation, strict data sovereignty, and continuous self-improvement.

---

## Recent Major Improvements (June 2026)

- **Full Data Flywheel Integration** across all portals (plan generation + hardware outcome recording)
- **Modern Security Layer** — `SecurityGuard` with structured `SecurityResult`
- **Enhanced Telemetry** — System metrics, structured JSON logging, context managers
- **Hardened CI/CD** — Standardised Python 3.10, pip caching, reliable Gitleaks scanning
- **Improved Packaging** — `pyproject.toml` in Core + Weaver
- **Production Deployment Assets** — K3s manifests + hardening guide
- **Comprehensive Documentation** — New Architecture and Data Flywheel guides

---

## Architecture Overview

See the high-level architecture document:

→ **[ARCHITECTURE.md](./ARCHITECTURE.md)**

Key layers:
- **Coastal-Alpine-Core** — Shared SDK (Security, Telemetry, Data Flywheel)
- **Weaver** — Multi-tenant LangGraph orchestrator
- **Domain Portals** — Blue-Moon, AquaGuard, SoilGuard, Sting-Operation-AI
- **Edge Runtime** — RPi5 + Hailo NPU + K3s + Ollama

---

## Documentation

| Document                        | Description                                      |
|--------------------------------|--------------------------------------------------|
| `ARCHITECTURE.md`              | High-level system architecture                   |
| `DATA_FLYWHEEL_GUIDE.md`       | Complete guide to the self-improving data flywheel |
| `SECURITY_POSTURE_REPORT.md`   | Security & hardening status across the stack     |
| `PRODUCTION_HARDENING.md`      | Enterprise / government deployment recommendations |

---

## Quick Links to Repositories

- [Coastal-Alpine-Core](./coastal_alpine_core) — Shared Python SDK
- [Weaver](./weaver) — Multi-tenant orchestration
- [Blue-Moon-Portal](./Blue-Moon-Portal) — Crop optimisation
- [AquaGuard-Portal](./AquaGuard-Portal) — Water quality & aquaculture
- [SoilGuard-Portal](./SoilGuard-Portal) — Soil & pasture health
- [Sting-Operation-AI](./Sting-Operation-AI) — Biosecurity vision

---

## Getting Started

See individual repository READMEs for setup instructions.

**Core requirement**: Python 3.10+

```bash
# Example: Install shared core
pip install -e ./coastal_alpine_core[dev]
```

---

## License

Proprietary — Coastal Alpine Tech Limited

---

*Last major update: June 2026*