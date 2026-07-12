# Coastal Alpine Stack — Sovereign Edge AI Platform

![Banner](assets/social_preview.png)


**Coastal Alpine Tech Limited**  
*Edge-Native | Data Sovereign | Self-Improving*


A production-grade, sovereign edge AI ecosystem for New Zealand’s primary industries (agriculture, aquaculture, biosecurity). Designed for offline operation, strict data sovereignty, and continuous self-improvement.

---

## Recent Major Improvements (July 2026)

- **Hybridised stack** — Core · Weaver · Aether · monorepo unified for **Windows + Linux** (edge remains RPi 5)
- **Enhanced system map** — multi-plane Mermaid + liquid-glass overview (field → fabric → runtime → companion → trust)
- **Dual-platform installers** — `install.sh` (Linux/macOS) + `install.ps1` (Windows) + `bootstrap.py`
- **Core SDK 0.5.x** — edge optimisations, expanded `SecurityGuard`, flywheel rotation
- **Aether companion** — ReAct skills, HITL gates, computer use for sovereign development
- **Security notifications** — Dependabot estate-wide, least-privilege CI, GHSA floors
- **Full Data Flywheel** — plan generation + hardware outcome recording across portals
- **Production deployment** — K3s manifests + `PRODUCTION_HARDENING.md`

---

## Architecture Overview

The stack repo composes the full **sovereign edge runtime**: field firmware → mTLS MQTT → Core SDK → Weaver → domain portals → Ollama + Hailo-10H, hybridised with the **Aether** agentic companion. **Develop on Windows or Linux; deploy on RPi 5 16GB**.

<p align="center">
  <img src="assets/architecture_overview.png" alt="Coastal Alpine Stack architecture — hybrid liquid glass system map" width="100%" />
</p>

### System map

Five planes: **field**, **fabric**, **runtime apps**, **companion**, and **trust** — with dual-platform host paths.

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
    classDef companion fill:#4c1d95,stroke:#c4b5fd,stroke-width:2px,color:#f5f3ff
    classDef host fill:#052e16,stroke:#86efac,stroke-width:2px,color:#f0fdf4

    subgraph FIELD["1 · Field & firmware"]
        ESP["Sovereign-Edge-Firmware<br/>ESP32 · sensors · actuators"]
        CAM["Cameras / mics"]
    end

    subgraph FABRIC["2 · Message fabric"]
        MQTT["Mosquitto mTLS :8883"]
        ACL["Topic ACLs · nftables"]
    end

    subgraph NODE["3 · Edge runtime — hybrid Core + Weaver + portals"]
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

    subgraph COMPANION["4 · Aether companion"]
        AETH["Aether<br/>ReAct · skills · computer use"]
        SK["kiwi-edge + security skills"]
    end

    subgraph TRUST["5 · Trust & control"]
        HITL["HITL gates"]
        SEC["SecOps · red-team · Dependabot"]
        PROM["Prometheus"]
    end

    subgraph HOSTS["Hosts — Windows + Linux + edge"]
        WIN["Windows 10/11<br/>install.ps1"]
        LIN["Linux workstation<br/>install.sh"]
        RPI["RPi 5 16GB + Hailo-10H"]
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
    AETH --> SK
    AETH -.->|dev / remediate / HITL| CORE & W
    HITL -.-> AETH
    NODE -.-> HOSTS
    COMPANION -.-> WIN & LIN

    class ESP,CAM field
    class MQTT,ACL fabric
    class CORE core
    class W orch
    class AQ,SO,BM,ST portal
    class OLL,HAI ai
    class MEM fly
    class HITL,SEC sec
    class K3,PROM ops
    class AETH,SK companion
    class WIN,LIN,RPI host
```

| Plane | Components | Role |
| :--- | :--- | :--- |
| **Field** | Sovereign-Edge-Firmware, cameras/mics | Sense + actuate on-site |
| **Fabric** | Mosquitto mTLS, ACLs, nftables | Encrypted, micro-segmented bus |
| **SDK** | Coastal-Alpine-Core | Guards, telemetry, flywheel, portal_core |
| **Orchestration** | Weaver | Multi-tenant routing + RAG |
| **Portals** | AquaGuard · SoilGuard · Blue-Moon · Sting | Domain agents |
| **Companion** | Aether | Agentic dev, skills, computer use, HITL |
| **AI** | Ollama + Hailo-10H | Offline LLM + NPU vision |
| **Trust** | HITL, SecOps, Prometheus | Governance + observability |
| **Hosts** | Windows · Linux · RPi 5 | Dual-platform install; edge production |

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

| Repo | Role | Platforms |
| :--- | :--- | :--- |
| [Coastal-Alpine-Core](https://github.com/fivepanelhat/Coastal-Alpine-Core) | Shared Python SDK | Windows · Linux · RPi |
| [Weaver](https://github.com/fivepanelhat/Weaver) | Multi-tenant orchestration | Windows · Linux · RPi |
| [Aether](https://github.com/fivepanelhat/Aether) | Agentic companion + computer use | Windows · Linux · macOS |
| [Blue-Moon-Portal](./Blue-Moon-Portal) | Crop optimisation | Edge Linux |
| [AquaGuard-Portal](./AquaGuard-Portal) | Water quality & aquaculture | Edge Linux |
| [SoilGuard-Portal](./SoilGuard-Portal) | Soil & pasture health | Edge Linux |
| [Sting-Operation-AI](./Sting-Operation-AI) | Biosecurity vision | Edge Linux + Hailo |

---

## Getting Started (Windows + Linux)

**Requirements:** Python 3.10+ (stack workspace prefers 3.11+), Git, Docker optional for compose.

### One-line install

<details open>
<summary><strong>🐧 Linux / macOS</strong></summary>

```bash
curl -fsSL https://raw.githubusercontent.com/fivepanelhat/coastal-alpine-stack/main/install.sh | bash
```

</details>

<details>
<summary><strong>🪟 Windows (PowerShell)</strong></summary>

```powershell
irm https://raw.githubusercontent.com/fivepanelhat/coastal-alpine-stack/main/install.ps1 | iex
```

> **Note:** If script execution is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

</details>

### From a clone

<details open>
<summary><strong>🐧 Linux / macOS</strong></summary>

```bash
git clone --recurse-submodules https://github.com/fivepanelhat/coastal-alpine-stack.git
cd coastal-alpine-stack

python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e "./coastal_alpine_core[dev]"
pip install -r requirements-dev.txt

# Optional: Docker edge stack
# docker compose up -d
```

**System packages (Debian/Ubuntu/RPi OS):**

```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-venv python3-pip git build-essential
# Optional edge: docker.io docker-compose-v2
```

</details>

<details>
<summary><strong>🪟 Windows (PowerShell)</strong></summary>

```powershell
git clone --recurse-submodules https://github.com/fivepanelhat/coastal-alpine-stack.git
cd coastal-alpine-stack

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e "./coastal_alpine_core[dev]"
pip install -r requirements-dev.txt

# Optional: Docker Desktop + compose for local edge services
# docker compose up -d
```

**Prerequisites:** [Python 3.10+](https://www.python.org/downloads/) (PATH enabled), [Git for Windows](https://git-scm.com/), optional [Docker Desktop](https://www.docker.com/products/docker-desktop/).

</details>

### Companion (Aether)

Install Aether alongside the stack for skills, remediation, and computer use:

| OS | Command |
| :--- | :--- |
| Linux / macOS | `curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.sh \| bash` |
| Windows | `irm https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.ps1 \| iex` |

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
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20RPi-0078D6?style=flat-square)]()  
[![Hybrid](https://img.shields.io/badge/Hybrid-Core%20%7C%20Weaver%20%7C%20Aether-8B5CF6?style=flat-square)]()  
[![Install](https://img.shields.io/badge/Install-install.sh%20%7C%20install.ps1-0ea5e9?style=flat-square)]()  
[![Hardware Target](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%2016GB-C11A5B?style=flat-square&logo=raspberry-pi&logoColor=white)]()  
[![NPU Acceleration](https://img.shields.io/badge/NPU-Hailo--10H%20Accelerated-005A9C?style=flat-square)]()  
[![Sovereignty](https://img.shields.io/badge/Sovereignty-NZ%20Data%20Bound-00247D?style=flat-square)]()  
[![CI](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/ci-scan.yml/badge.svg?branch=main)](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/ci-scan.yml)  
[![SecOps](https://img.shields.io/github/actions/workflow/status/fivepanelhat/coastal-alpine-stack/secops.yml?branch=main&label=SecOps&style=flat-square&color=success)](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/secops.yml)  
[![RedTeam](https://img.shields.io/github/actions/workflow/status/fivepanelhat/coastal-alpine-stack/redteam.yml?branch=main&label=RedTeam&style=flat-square&color=critical)](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/redteam.yml)  
[![Dependabot](https://img.shields.io/badge/Dependencies-Monitored-brightgreen?style=flat-square&logo=dependabot)]()  
[![Interop](https://img.shields.io/badge/Interop-MQTT%20%7C%20OPC--UA-orange?style=flat-square)]()  
[![Sustainability](https://img.shields.io/badge/EECA%20NZ-Carbon%20Tracked-green?style=flat-square)]()
