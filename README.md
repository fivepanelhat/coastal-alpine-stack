# Coastal Alpine Stack — Sovereign Edge AI Platform

![Banner](assets/social_preview.png)


**Coastal Alpine Tech Limited**  
*Edge-Native | Data Sovereign | Self-Improving*


A production-grade, sovereign edge AI ecosystem for New Zealand’s primary industries (agriculture, aquaculture, biosecurity). Designed for offline operation, strict data sovereignty, and continuous self-improvement.

---

## Recent Major Improvements (July 2026)

- **Enhanced system map** — multi-plane Mermaid + liquid-glass overview (field → fabric → runtime → trust)
- **Core SDK 0.5.x** — edge optimisations, expanded `SecurityGuard`, flywheel rotation
- **Security notifications** — Dependabot estate-wide, least-privilege CI, GHSA floors
- **Full Data Flywheel** — plan generation + hardware outcome recording across portals
- **Production deployment** — K3s manifests + `PRODUCTION_HARDENING.md`

---

## Architecture Overview

The stack repo composes the full **sovereign edge runtime**: field firmware → mTLS MQTT → Core SDK → Weaver → domain portals → Ollama + Hailo-10H, with SecurityGuard, SecOps, and the data flywheel on **RPi 5 16GB**.

<p align="center">
  <img src="assets/architecture_overview.png" alt="Coastal Alpine Stack architecture — liquid glass system map" width="100%" />
</p>

### System map

Four planes on one edge node: **field**, **fabric**, **runtime apps**, and **trust**.

```mermaid
%%{init: {
  "theme": "dark",
  "themeVariables": {
    "fontSize": "22px",
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
    "nodeSpacing": 48,
    "rankSpacing": 56,
    "padding": 28,
    "htmlLabels": true,
    "curve": "basis",
    "useMaxWidth": true
  }
}}%%
flowchart TB

    classDef field fill:#052e16,stroke:#4ade80,stroke-width:2px,color:#f0fdf4
    classDef fabric fill:#0c4a6e,stroke:#38bdf8,stroke-width:2px,color:#f0f9ff
    classDef core fill:#134e4a,stroke:#2dd4bf,stroke-width:2px,color:#f0fdfa
    classDef orch fill:#312e81,stroke:#a5b4fc,stroke-width:2px,color:#eef2ff
    classDef portal fill:#1e1b4b,stroke:#c4b5fd,stroke-width:2px,color:#eef2ff
    classDef ai fill:#3b0764,stroke:#e879f9,stroke-width:2px,color:#fdf4ff
    classDef fly fill:#422006,stroke:#fbbf24,stroke-width:2px,color:#fffbeb
    classDef sec fill:#450a0a,stroke:#f87171,stroke-width:2px,color:#fef2f2
    classDef ops fill:#164e63,stroke:#22d3ee,stroke-width:2px,color:#ecfeff

    subgraph FIELD["1 · Field & firmware"]
        ESP["Sovereign-Edge-Firmware<br/>ESP32 · sensors · actuators"]
        CAM["Cameras / mics"]
    end

    subgraph FABRIC["2 · Message fabric"]
        MQTT["Mosquitto mTLS :8883"]
        ACL["Topic ACLs · nftables"]
    end

    subgraph NODE["3 · Edge node — RPi 5 16GB + Hailo-10H"]
        K3["K3s / compose"]
        CORE["Coastal-Alpine-Core<br/>SecurityGuard · Telemetry · Flywheel · portal_core"]
        W["Weaver<br/>LangGraph multi-tenant router"]
        AQ["AquaGuard"]
        SO["SoilGuard"]
        BM["Blue-Moon"]
        ST["Sting"]
        OLL["Ollama gemma4:e4b"]
        HAI["Hailo-10H NPU"]
        MEM["Chroma local · SQLCipher · flywheel JSONL"]
    end

    subgraph TRUST["4 · Trust & control"]
        HITL["HITL gates"]
        SEC["SecOps · red-team · Dependabot"]
        PROM["Prometheus"]
    end

    ESP --> MQTT
    CAM --> CORE
    MQTT --> ACL --> CORE
    CORE --> W
    W --> AQ & SO & BM & ST
    AQ & SO & BM & ST --> OLL
    ST & BM --> HAI
    AQ & SO & BM & ST --> MEM
    CORE --> MEM
    K3 --> CORE & MQTT & OLL
    CORE -.-> HITL
    CORE --> PROM
    SEC -.-> CORE

    class ESP,CAM field
    class MQTT,ACL fabric
    class CORE core
    class W orch
    class AQ,SO,BM,ST portal
    class OLL,HAI ai
    class MEM fly
    class HITL,SEC sec
    class K3,PROM ops
```

| Plane | Components | Role |
| :--- | :--- | :--- |
| **Field** | Sovereign-Edge-Firmware, cameras/mics | Sense + actuate on-site |
| **Fabric** | Mosquitto mTLS, ACLs, nftables | Encrypted, micro-segmented bus |
| **SDK** | Coastal-Alpine-Core | Guards, telemetry, flywheel, portal_core |
| **Orchestration** | Weaver | Multi-tenant routing + RAG |
| **Portals** | AquaGuard · SoilGuard · Blue-Moon · Sting | Domain agents |
| **AI** | Ollama + Hailo-10H | Offline LLM + NPU vision |
| **Trust** | HITL, SecOps, Prometheus | Governance + observability |

*Full maps (data plane + trust plane): [ARCHITECTURE.md](./ARCHITECTURE.md)*

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

*Last major update: July 2026*

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
