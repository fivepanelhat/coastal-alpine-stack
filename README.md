# Coastal Alpine Stack Sovereign Edge AI Platform

[![Privacy](https://img.shields.io/badge/Privacy-Local--first%20%2B%20Privacy%20Act%202020-00247D)](./COMPLIANCE.md)
[![No data sold](https://img.shields.io/badge/Data-Not%20sold%20to%20third%20parties-0f766e)](./COMPLIANCE.md)
[![NZ Privacy Act](https://img.shields.io/badge/NZ-Privacy%20Act%202020-00247D)](./COMPLIANCE.md)
[![Te Mana Raraunga](https://img.shields.io/badge/Te%20Mana%20Raraunga-In%20accordance-0f766e)](./COMPLIANCE.md)
[![NZ AI Safety](https://img.shields.io/badge/NZ%20AI%20Safety-Aligned-8B5CF6)](./COMPLIANCE.md)
[![SOC2](https://img.shields.io/badge/SOC%202-Alignment%20path-6366f1)](./COMPLIANCE_REGIONS.md)
[![Regions](https://img.shields.io/badge/AU%20%7C%20Asia%20%7C%20EU-Mapped-0ea5e9)](./COMPLIANCE_REGIONS.md)
[![Security](https://img.shields.io/badge/Security-No%20silent%20exfil%20%2B%20SecOps-dc2626)](./SECURITY.md)
[![Governance](https://img.shields.io/badge/Governance-HITL%20%2B%20Te%20Mana%20Raraunga-0f766e)](./COMPLIANCE.md)


<!-- BEGIN CAT_CONGRUENCE_SNIPPET -->
## Coastal Alpine Tech portfolio

[![Stage](https://img.shields.io/badge/Stage-Pre--seed-8B5CF6)](https://github.com/fivepanelhat/fivepanelhat)
[![Hybrid](https://img.shields.io/badge/Hybrid-Edge%20%2B%20Multi--model-0f766e)](https://github.com/fivepanelhat/fivepanelhat)
[![HITL](https://img.shields.io/badge/HITL-Draft%2FPrepare%20only-dc2626)](./.github/agent-fleet/AGENTS.md)
[![Te Mana Raraunga](https://img.shields.io/badge/Te%20Mana%20Raraunga-Aligned-0f766e)](https://github.com/fivepanelhat/fivepanelhat)

**Part of the [Kiwi Edge AI Stack](https://github.com/fivepanelhat/fivepanelhat)** | Founder OS: [NZ-Start-Up](https://github.com/fivepanelhat/NZ-Start-Up) | Agent policy: [`.github/agent-fleet/`](./.github/agent-fleet/)

> Sovereign hybrid edge AI for NZ farms and founders - local-first + multi-model, Te Mana Raraunga aligned - collaborating with Venture Taranaki, startups.com investors and Kotahitanga Investment Fund (HITL + cultural advisory for formal approaches).

**Agents inform, draft, prepare, monitor, and remind. Humans advise, sign, file, send, and pay.** 
Anti-hallucination policy: [`.github/agent-fleet/anti-hallucination.md`](./.github/agent-fleet/anti-hallucination.md) | Congruence: [`CAT_CONGRUENCE.md`](./CAT_CONGRUENCE.md)
<!-- END CAT_CONGRUENCE_SNIPPET -->

<!-- BEGIN PRIVACY_SECURITY_GOVERNANCE -->
## Privacy / Security / Governance

Coastal Alpine Tech products treat operational and personal data as **taonga**. Defaults favour **local-first** operation, **purpose-limited** collection, and **Human-in-the-Loop** for high-stakes actions.

### Hard commitments

| Commitment | Statement |
| :--- | :--- |
| **No data sales** | **We do not sell personal information or customer operational data to third parties** for advertising, brokerage, or unrelated commercial exploitation. |
| **NZ Privacy Act 2020** | Collection, use, storage, and disclosure of personal information is designed to operate in accordance with the **Privacy Act 2020** information privacy principles (including IPP awareness and IPP 3A indirect-collection notification where applicable). |
| **Te Mana Raraunga** | Where Māori data or community data interests arise, systems are designed to operate **in accordance with Te Mana Raraunga** principles (including Rangatiratanga, Whakapapa, Whanaungatanga, Kotahitanga, Manaakitanga, Kaitiakitanga) as a sovereignty and stewardship lens — not as a marketing slogan. |
| **NZ AI safety** | AI features follow a **NZ AI safety-aligned** posture: Algorithm Charter spirit (fairness, transparency, human oversight where relevant), digital.govt.nz / responsible AI guidance awareness, no silent model training on private journals without consent, and HITL for high-stakes outcomes. |
| **Security** | No silent exfiltration; owner-controlled credentials; least privilege; SecOps / dependency hygiene on the fleet cadence. |
| **Governance** | Agents **inform, draft, prepare**; humans **advise, sign, file, send, and pay**. |

| Pillar | Commitment |
| :--- | :--- |
| **Privacy** | Local-first / offline-capable where practical; Privacy Act 2020; Te Mana Raraunga spirit; third-party AI only when **opt-in and labelled** |
| **Security** | No silent exfil of tenant or personal data; owner-controlled keys |
| **Governance** | HITL for high-stakes; Te Mana Raraunga spirit; multi-region compliance maps in [`COMPLIANCE_REGIONS.md`](./COMPLIANCE_REGIONS.md) |

**Agents inform, draft, prepare, monitor, and remind. Humans advise, sign, file, send, and pay.**

Fleet policy: [fivepanelhat / Kiwi Edge AI Stack](https://github.com/fivepanelhat/fivepanelhat) · [`COMPLIANCE.md`](./COMPLIANCE.md) · [`COMPLIANCE_REGIONS.md`](./COMPLIANCE_REGIONS.md) · [`SECURITY.md`](./SECURITY.md)
<!-- END PRIVACY_SECURITY_GOVERNANCE -->


<!-- BEGIN PROBLEMS_SOLUTIONS_ECONOMY -->
## Problems we are solving

**coastal-alpine-stack** is the compose / K3s monorepo that shows how the full Kiwi Edge system deploys together.

1. **Integration fog** - Separate repos hide how Core, portals, and ops actually run as one system.
2. **Fragile hand-deploy** - Without compose/K3s maps, pilots stall at "works on my Pi".
3. **Inconsistent environments** - Windows/Linux dev vs RPi prod drift without a reference stack.
4. **Weak ops defaults** - Auth, webhooks, and remediation must be documented as fail-closed targets.

## Solution we have built

| Built capability | What it does |
| :--- | :--- |
| **Monorepo architecture** | Reference layout for multi-service edge deploy |
| **Compose / K3s path** | Reproducible bring-up targets for pilots |
| **Cross-links** | Quick paths into Core, portals, and ops docs |
| **Hardening notes** | Diamond-oriented webhook and auth patterns |

This repo is architecture proof for technical diligence and pilot engineering - not a separate consumer brand.

### Local (Taranaki) and national (Aotearoa) economic benefits

| Lever | Benefit |
| :--- | :--- |
| **Regional R&D HQ** | Product design and IP stay in New Plymouth / Taranaki - not only Auckland/offshore SaaS |
| **Primary-sector productivity** | On-farm and rural tools aim to cut waste, protect consents, and support export competitiveness |
| **Skilled employment pathways** | Edge install, field support, agritech ops, software, compliance, and cultural advisory roles as pilots scale |
| **Data sovereignty** | Te Mana Raraunga-aligned local custody keeps high-value operational data onshore |
| **HITL jobs quality** | Agents **inform / draft / prepare / monitor / remind**; humans **advise / sign / file / send / pay** - augment people, do not fake full autonomy |

**Stage honesty (pre-seed):** Impact today is founder R&D, near-term contractors, and EDA/partner leverage. Permanent multi-region payroll follows paid pilots and revenue - we do not invent headcount claims.
<!-- END PROBLEMS_SOLUTIONS_ECONOMY -->

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary--Commercial-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://www.python.org)
[![Version](https://img.shields.io/badge/version-0.5.x-blue.svg)](./CHANGELOG.md)

[![Linux](https://img.shields.io/badge/Linux-Ubuntu%2C%20Debian%2C%20Fedora-FCC624?logo=linux&logoColor=black)](https://github.com/fivepanelhat/coastal-alpine-stack)
[![Windows](https://img.shields.io/badge/Windows-10%2B-0078D4?logo=windows&logoColor=white)](https://github.com/fivepanelhat/coastal-alpine-stack)
[![macOS](https://img.shields.io/badge/macOS-12%2B-000000?logo=apple&logoColor=white)](https://github.com/fivepanelhat/coastal-alpine-stack)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-5%20%2816GB%29-C11A5B?logo=raspberry-pi&logoColor=white)](https://github.com/fivepanelhat/coastal-alpine-stack)

[![Claude AI](https://img.shields.io/badge/Claude-Anthropic-9C27B0)](https://anthropic.com)
[![Gemini](https://img.shields.io/badge/Gemini-Google-4285F4?logo=google&logoColor=white)](https://gemini.google.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-00A67E)](https://openai.com)
[![Grok](https://img.shields.io/badge/Grok-xAI-000000)](https://x.ai)

[![Hailo NPU](https://img.shields.io/badge/NPU-Hailo--10H-005A9C)](https://github.com/fivepanelhat/coastal-alpine-stack)
[![Data Sovereign](https://img.shields.io/badge/Data%20Sovereign-NZ%20Bound-00247D)](./ARCHITECTURE.md)
[![K3s Ready](https://img.shields.io/badge/K3s-Container%20Ready-FF9900?logo=kubernetes&logoColor=white)](./docker-compose.yml)
[![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-3C5280?logo=mqtt&logoColor=white)](./docker-compose.yml)

[![CI Status](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/ci-scan.yml/badge.svg?branch=main)](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/ci-scan.yml)
[![Security Status](https://img.shields.io/github/actions/workflow/status/fivepanelhat/coastal-alpine-stack/secops.yml?branch=main&label=Security&style=flat-square&color=success)](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/secops.yml)
[![Dependencies](https://img.shields.io/badge/Dependencies-Monitored-brightgreen?logo=dependabot)](https://github.com/fivepanelhat/coastal-alpine-stack/security/dependabot)

![Banner](assets/social_preview.png)

**Coastal Alpine Tech Limited** pre-seed startup, New Plymouth, Taranaki, Aotearoa New Zealand.
*Edge-Native | Data Sovereign | Self-Improving*

An early-stage (pre-seed) stack aiming at production-oriented, sovereign edge AI ecosystem for New Zealand's primary industries (agriculture, aquaculture, biosecurity). Designed for offline operation, strict data sovereignty, and continuous self-improvement.

---

## Recent Major Improvements (July 2026)

- **Hybridised stack** Core | Weaver | Aether | monorepo unified for **Windows + Linux** (edge remains RPi 5)
- **Enhanced system map** multi-plane Mermaid + liquid-glass overview (field -> fabric -> runtime -> companion -> trust)
- **Dual-platform installers** `install.sh` (Linux/macOS) + `install.ps1` (Windows) + `bootstrap.py`
- **Core SDK 0.5.x** edge optimisations, expanded `SecurityGuard`, flywheel rotation
- **Aether companion** ReAct skills, HITL gates, computer use for sovereign development
- **Security notifications** Dependabot estate-wide, least-privilege CI, GHSA floors
- **Full Data Flywheel** plan generation + hardware outcome recording across portals
- **Production deployment** K3s manifests + `PRODUCTION_HARDENING.md`

---

## Architecture Overview

> **Diagrams:** Architecture images and Mermaid maps describe the **target product architecture** for this pre-seed stack. They are engineering design maps not claims of large-scale commercial fleet deployment.

The stack repo composes the full **sovereign edge runtime**: field firmware -> mTLS MQTT -> Core SDK -> Weaver -> domain portals -> Ollama + Hailo-10H, hybridised with the **Aether** agentic companion. **Develop on Windows or Linux; deploy on RPi 5 16GB**.

<p align="center">
 <img src="assets/architecture_overview.png" alt="Coastal Alpine Stack architecture hybrid liquid glass system map" width="100%" />
</p>

### System map

Five planes: **field**, **fabric**, **runtime apps**, **companion**, and **trust** with dual-platform host paths.

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

 subgraph FIELD["1 | Field & firmware"]
 ESP["Sovereign-Edge-Firmware<br/>ESP32 | sensors | actuators"]
 CAM["Cameras / mics"]
 end

 subgraph FABRIC["2 | Message fabric"]
 MQTT["Mosquitto mTLS :8883"]
 ACL["Topic ACLs | nftables"]
 end

 subgraph NODE["3 | Edge runtime hybrid Core + Weaver + portals"]
 K3["K3s / compose"]
 CORE["Coastal-Alpine-Core<br/>SecurityGuard | Telemetry | Flywheel | portal_core"]
 W["Weaver<br/>LangGraph multi-tenant router"]
 AQ["AquaGuard"]
 SO["SoilGuard"]
 BM["Blue-Moon"]
 ST["Sting"]
 OLL["Ollama gemma4:e4b"]
 HAI["Hailo-10H NPU"]
 MEM["Chroma local | SQLCipher | flywheel JSONL"]
 end

 subgraph COMPANION["4 | Aether companion"]
 AETH["Aether<br/>ReAct | skills | computer use"]
 SK["kiwi-edge + security skills"]
 end

 subgraph TRUST["5 | Trust & control"]
 HITL["HITL gates"]
 SEC["SecOps | red-team | Dependabot"]
 PROM["Prometheus"]
 end

 subgraph HOSTS["Hosts Windows + Linux + edge"]
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
 AETH -.-> | dev / remediate / HITL | CORE & W
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
 | **Portals** | AquaGuard | SoilGuard | Blue-Moon | Sting | Domain agents |
 | **Companion** | Aether | Agentic dev, skills, computer use, HITL |
 | **AI** | Ollama + Hailo-10H | Offline LLM + NPU vision |
 | **Trust** | HITL, SecOps, Prometheus | Governance + observability |
 | **Hosts** | Windows | Linux | RPi 5 | Dual-platform install; edge production |

*Full maps (data plane + trust plane): [ARCHITECTURE.md](./ARCHITECTURE.md)*

## Documentation

 | Document | Description |
 | -------------------------------- | -------------------------------------------------- |
 | `ARCHITECTURE.md` | High-level system architecture |
 | `DATA_FLYWHEEL_GUIDE.md` | Complete guide to the self-improving data flywheel |
 | `SECURITY_POSTURE_REPORT.md` | Security & hardening status across the stack |
 | `PRODUCTION_HARDENING.md` | Enterprise / government deployment recommendations |

---

## Quick Links to Repositories

 | Repo | Role | Platforms |
 | :--- | :--- | :--- |
 | [Coastal-Alpine-Core](https://github.com/fivepanelhat/Coastal-Alpine-Core) | Shared Python SDK | Windows | Linux | RPi |
 | [Weaver](https://github.com/fivepanelhat/Weaver) | Multi-tenant orchestration | Windows | Linux | RPi |
 | [Aether](https://github.com/fivepanelhat/Aether) | Agentic companion + computer use | Windows | Linux | macOS |
 | [Blue-Moon-Portal](./Blue-Moon-Portal) | Crop optimisation | Edge Linux |
 | [AquaGuard-Portal](./AquaGuard-Portal) | Water quality & aquaculture | Edge Linux |
 | [SoilGuard-Portal](./SoilGuard-Portal) | Soil & pasture health | Edge Linux |
 | [Sting-Operation-AI](./Sting-Operation-AI) | Biosecurity vision | Edge Linux + Hailo |

---

## Getting Started (Windows + Linux)

**Requirements:** Python 3.10+ (stack workspace prefers 3.11+), Git, Docker optional for compose.

### One-line install

<details open>
<summary><strong> Linux / macOS</strong></summary>

```bash
curl -fsSL https://raw.githubusercontent.com/fivepanelhat/coastal-alpine-stack/main/install.sh | bash
```

</details>

<details>
<summary><strong> Windows (PowerShell)</strong></summary>

```powershell
irm https://raw.githubusercontent.com/fivepanelhat/coastal-alpine-stack/main/install.ps1 | iex
```

> **Note:** If script execution is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

</details>

### From a clone

<details open>
<summary><strong> Linux / macOS</strong></summary>

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
<summary><strong> Windows (PowerShell)</strong></summary>

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
 | Linux / macOS | `curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.sh \ | bash` |
 | Windows | `irm https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.ps1 \ | iex` |

---

## License

Proprietary Coastal Alpine Tech Limited

---

*Last major update: July 2026*
