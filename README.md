# Coastal Alpine Stack — Sovereign Edge AI Platform

![Banner](assets/social_preview.png)


**Coastal Alpine Tech Limited**  
*Edge-Native | Data Sovereign | Self-Improving*


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

The stack repo composes the full **sovereign edge runtime**: Core SDK, Weaver, domain portals, MQTT, and K3s/compose on **RPi 5 16GB + Hailo-10H**.

![Coastal Alpine Stack architecture — liquid glass overview](assets/architecture_overview.png)

### System map

```mermaid
%%{init: {
  "theme": "dark",
  "themeVariables": {
    "fontSize": "16px",
    "fontFamily": "Inter, ui-sans-serif, system-ui, sans-serif",
    "primaryColor": "#0ea5e9",
    "primaryTextColor": "#f8fafc",
    "primaryBorderColor": "#38bdf8",
    "lineColor": "#67e8f9",
    "secondaryColor": "#1e293b",
    "tertiaryColor": "#0f172a",
    "clusterBkg": "#0b1220cc",
    "clusterBorder": "#38bdf880",
    "titleColor": "#e2e8f0"
  },
  "flowchart": {
    "nodeSpacing": 40,
    "rankSpacing": 48,
    "padding": 20,
    "htmlLabels": true,
    "curve": "basis"
  }
}}%%
flowchart TB

    classDef sense fill:#052e16,stroke:#4ade80,stroke-width:2px,color:#f0fdf4
    classDef edge fill:#0c4a6e,stroke:#38bdf8,stroke-width:2px,color:#f0f9ff
    classDef core fill:#134e4a,stroke:#2dd4bf,stroke-width:2px,color:#f0fdfa
    classDef act fill:#422006,stroke:#fbbf24,stroke-width:2px,color:#fffbeb
    classDef store fill:#1e1b4b,stroke:#a5b4fc,stroke-width:2px,color:#eef2ff
    classDef ai fill:#3b0764,stroke:#e879f9,stroke-width:2px,color:#fdf4ff
    classDef app fill:#1e1b4b,stroke:#c4b5fd,stroke-width:2px,color:#eef2ff

    FW["Sovereign-Edge-Firmware<br/>ESP32 · mTLS MQTT"] --> BUS["Mosquitto / message bus"]
    BUS --> CORE["Coastal-Alpine-Core"]
    CORE --> W["Weaver"]
    CORE --> A["AquaGuard"]
    CORE --> S["SoilGuard"]
    CORE --> B["Blue-Moon"]
    CORE --> ST["Sting-Operation"]
    CORE --> OLL["Ollama + Hailo-10H"]
    K3["K3s / compose runtime"] --> CORE
    K3 --> BUS
    K3 --> OLL

    subgraph NODE["Edge node — RPi 5 16GB"]
        K3
        CORE
        OLL
        W
        A
        S
        B
        ST
    end

    class FW sense
    class BUS,K3 edge
    class CORE core
    class W,A,S,B,ST store
    class OLL ai
```

| Layer | Components | Role |
| :--- | :--- | :--- |
| **Runtime** | K3s / compose | On-device services |
| **SDK** | Coastal-Alpine-Core | Shared guards + LLM |
| **Apps** | Weaver + portals | Domain agents |
| **Hardware** | RPi 5 16GB + Hailo-10H | Canonical target |

*Full detail: [ARCHITECTURE.md](./ARCHITECTURE.md)*

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

---

## Project badges

Status badges for this repository (CI, security, license, and stack metadata):

[![License](https://img.shields.io/badge/License-Proprietary--Commercial-blue?style=flat-square)](LICENSE)  
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)  
[![Hardware Target](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%2016GB-C11A5B?style=flat-square&logo=raspberry-pi&logoColor=white)]()  
[![NPU Acceleration](https://img.shields.io/badge/NPU-Hailo--10H%20Accelerated-005A9C?style=flat-square)]()  
[![Sovereignty](https://img.shields.io/badge/Sovereignty-NZ%20Data%20Bound-00247D?style=flat-square)]()  
[![CI](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/ci-scan.yml/badge.svg?branch=main)](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/ci-scan.yml)  
[![SecOps](https://img.shields.io/github/actions/workflow/status/fivepanelhat/coastal-alpine-stack/secops.yml?branch=main&label=SecOps&style=flat-square&color=success)](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/secops.yml)  
[![RedTeam](https://img.shields.io/github/actions/workflow/status/fivepanelhat/coastal-alpine-stack/redteam.yml?branch=main&label=RedTeam&style=flat-square&color=critical)](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/redteam.yml)  
[![Dependabot](https://img.shields.io/badge/Dependencies-Monitored-brightgreen?style=flat-square&logo=dependabot)]()  
[![Interop](https://img.shields.io/badge/Interop-MQTT%20%7C%20OPC--UA-orange?style=flat-square)]()  
[![Sustainability](https://img.shields.io/badge/EECA%20NZ-Carbon%20Tracked-green?style=flat-square)]()
