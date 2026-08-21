# Coastal Alpine Tech - High-Level Architecture

**Version**: August 2026  
**Status**: Active Development - Enterprise Hardening Phase  
**Canonical hardware**: Raspberry Pi 5 16GB + Hailo-10H NPU (40 TOPS)  
**Core pin**: [v0.5.9](https://github.com/fivepanelhat/Coastal-Alpine-Core/releases/tag/v0.5.9)

---

## 1. Vision

Coastal Alpine Tech builds **sovereign, edge-native AI systems** for New Zealand's primary industries (agriculture, aquaculture, biosecurity). The platform enables local decision-making, data sovereignty (Te Mana Raraunga aligned), and continuous self-improvement while minimising cloud dependency.

Core principles:

- **Edge-first & offline-capable**
- **Data sovereignty** (local processing + owner-controlled keys)
- **HITL governance** on high-stakes decisions
- **Self-improving data flywheels**
- **Production-grade security & observability**

---

## 2. System map (full stack)

The monorepo composes field devices, a message fabric, the Core SDK, multi-tenant orchestration, domain portals, local AI acceleration, and the data flywheel - all on a single edge node (or small K3s fleet).

```mermaid
%%{init: {
 "theme": "dark",
 "themeVariables": {
 "fontSize": "20px",
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
 "nodeSpacing": 44,
 "rankSpacing": 52,
 "padding": 24,
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

 subgraph FIELD["1 | Field & firmware"]
 ESP["Sovereign-Edge-Firmware<br/>ESP32 | sensors | actuators"]
 CAM["Cameras / mics<br/>Sting | Blue-Moon AV"]
 end

 subgraph FABRIC["2 | Message fabric"]
 MQTT["Mosquitto MQTT<br/>mTLS :8883 | ACLs"]
 NFT["nftables + micro-seg"]
 end

 subgraph NODE["3 | Edge node - RPi 5 16GB + Hailo-10H"]
 direction TB
 K3["K3s / docker-compose runtime"]

 subgraph SDK["Coastal-Alpine-Core SDK"]
 SG["SecurityGuard"]
 TEL["TelemetryTracker"]
 SE["SessionEventStore"]
 FW["DataFlywheel"]
 OCL["SovereignOllamaClient"]
 PR["LLMProvider + profiles"]
 PC["portal_core<br/>AIAgent | MQTT | AV | Hardware"]
 end

 subgraph ORCH["Weaver"]
 LG["LangGraph multi-tenant router"]
 RAG["RAG / tenant stores"]
 end

 subgraph PORTALS["Domain portals"]
 AQ["AquaGuard<br/>water | compliance"]
 SO["SoilGuard<br/>soil | pasture"]
 BM["Blue-Moon<br/>crop | multi-modal"]
 ST["Sting-Operation<br/>biosecurity vision"]
 end

 subgraph AI["Local AI"]
 OLL["Ollama<br/>gemma4:e4b"]
 HAI["Hailo-10H NPU<br/>40 TOPS | YOLO/vision"]
 end

 subgraph MEM["Local memory"]
 CH["ChromaDB<br/>localhost only"]
 SQL["SQLite / SQLCipher"]
 JL["flywheel_*.jsonl"]
 SEJL["session_events.jsonl"]
 end
 end

 subgraph CTRL["4 | Control & trust"]
 HITL["HITL gates<br/>high-stakes actions"]
 SEC["SecOps | Bandit | Gitleaks<br/>red-team | Dependabot"]
 PROM["Prometheus scrapes"]
 end

 ESP -->|telemetry / state| MQTT
 CAM -->|frames / audio| PC
 MQTT --> NFT
 NFT --> PC
 PC --> SG
 SG --> LG
 LG --> AQ & SO & BM & ST
 AQ & SO & BM & ST --> OCL
 OCL --> OLL
 ST --> HAI
 BM --> HAI
 AQ & SO & BM & ST --> FW
 LG --> SE
 SE --> SEJL
 FW --> JL
 LG --> RAG
 RAG --> CH
 PC --> SQL
 K3 --> MQTT & OLL & LG
 SG -.->|block / allow| HITL
 TEL --> PROM
 SEC -.->|policy| SG

 class ESP,CAM field
 class MQTT,NFT fabric
 class SG,TEL,SE,FW,OCL,PR,PC core
 class LG,RAG orch
 class AQ,SO,BM,ST portal
 class OLL,HAI ai
 class CH,SQL,JL,SEJL fly
 class HITL,SEC sec
 class K3,PROM ops
```

### Layer table

| # | Layer | Components | Role |
|:-:|:------|:-----------|:-----|
| 1 | **Field** | Sovereign-Edge-Firmware, cameras/mics | Sense physical world; mTLS client identity |
| 2 | **Fabric** | Mosquitto, ACLs, nftables | Encrypted, topic-scoped message bus |
| 3a | **SDK** | Coastal-Alpine-Core | Guards, telemetry, SessionEvent, flywheel, providers, portal_core |
| 3b | **Orchestration** | Weaver (LangGraph) | Multi-tenant routing + RAG + audit emits |
| 3c | **Portals** | AquaGuard, SoilGuard, Blue-Moon, Sting | Domain agents + actuators |
| 3d | **AI** | Ollama + Hailo-10H | Offline LLM + NPU vision |
| 3e | **Memory** | Chroma (local), SQLCipher, JSONL flywheels / session_events | Sovereign stores |
| 4 | **Trust** | HITL, SecOps CI, Prometheus | Governance + observability |

### Sprint A–C Core seams (Aug 2026)

| Seam | Core | Stack adoption |
|------|------|----------------|
| SessionEvent | [v0.5.7](https://github.com/fivepanelhat/Coastal-Alpine-Core/releases/tag/v0.5.7) | Weaver + Aether HITL evidence |
| LLMProvider + profiles | [v0.5.8](https://github.com/fivepanelhat/Coastal-Alpine-Core/releases/tag/v0.5.8) | Soft bridges; local Ollama default |
| Session → Trajectory | [v0.5.9](https://github.com/fivepanelhat/Coastal-Alpine-Core/releases/tag/v0.5.9) | Outcome samples for flywheel / golden-set |

---

## 3. Data-plane map (portal control loop)

```mermaid
%%{init: {
 "theme": "dark",
 "themeVariables": {
 "fontSize": "20px",
 "fontFamily": "Inter, ui-sans-serif, system-ui, sans-serif",
 "lineColor": "#67e8f9",
 "clusterBkg": "#0b1220cc",
 "clusterBorder": "#38bdf880"
 },
 "flowchart": { "curve": "basis", "nodeSpacing": 48, "rankSpacing": 56, "padding": 24, "useMaxWidth": true }
}}%%
flowchart LR

 classDef in fill:#052e16,stroke:#4ade80,stroke-width:2px,color:#f0fdf4
 classDef mid fill:#0c4a6e,stroke:#38bdf8,stroke-width:2px,color:#f0f9ff
 classDef ai fill:#3b0764,stroke:#e879f9,stroke-width:2px,color:#fdf4ff
 classDef out fill:#422006,stroke:#fbbf24,stroke-width:2px,color:#fffbeb
 classDef rec fill:#1e1b4b,stroke:#a5b4fc,stroke-width:2px,color:#eef2ff

 S[Sensors / MQTT] --> A[analyze_sensor_state]
 V[Vision + audio] --> P[process_visual / audio]
 A --> G[SecurityGuard]
 P --> G
 G -->|safe| R[generate_optimization_plan]
 G -->|unsafe| X[reject + audit]
 R --> T1[DataFlywheel trajectory]
 R --> E[enforce_plan / hardware]
 E --> T2[hardware outcome]
 T1 --> F[flywheel_*.jsonl]
 T2 --> F
 F --> C[evaluate + golden set]
 E --> L[compliance / audit log]

 class S,V in
 class A,P,G mid
 class R ai
 class E,X out
 class T1,T2,F,C,L rec
```

Typical path:

1. Sensors / MQTT -> `analyze_sensor_state()`
2. Vision + audio -> `process_visual_feedback()` / `process_audio_feedback()`
3. `SecurityGuard` on all LLM-bound text
4. Multi-modal reasoning -> `generate_optimization_plan()` -> **trajectory recorded**
5. Hardware enforcement -> `enforce_plan()` -> **outcome recorded**
6. Compliance / audit logging
7. Local `flywheel_*.jsonl` for evaluation and golden-set curation

---

## 4. Trust & security plane

| Concern | Implementation | Status |
|---------|----------------|--------|
| Prompt / injection | Core `SecurityGuard` (v0.5.9 patterns) | Strong |
| Tenant isolation | Weaver routing + `tenant_isolated_query` | Strong |
| Session audit | `SessionEventStore` + Trajectory (no secrets) | Strong |
| Transit | mTLS MQTT :8883, ACLs, nftables | Strong |
| Supply chain | Dependabot, Gitleaks, Bandit, red-team | Strong |
| Vector DB | Chroma **localhost-only** until upstream RCE patch | Mitigated |
| Secrets | No tool-written API keys; env / operator `.env` | Strong |
| Observability | `TelemetryTracker` + Prometheus | Good |
| Deployment | K3s manifests + `PRODUCTION_HARDENING.md` | Good |

Detail: [`SECURITY.md`](./SECURITY.md) | [`SECURITY_MATRIX.md`](./SECURITY_MATRIX.md) | [`THREAT_MODEL.md`](./THREAT_MODEL.md)

---

## 5. Component catalogue

### 5.1 Coastal-Alpine-Core (shared foundation)

- `SecurityGuard` / `SecurityResult` - prompt, SSRF-lure, SQL, credential patterns
- `TelemetryTracker` - latency, optional system metrics
- `SessionEventStore` / `make_event` - append-only HITL evidence stream
- `DataFlywheel` / `record_session_trajectory` - trajectories, HITL feedback, golden sets
- `LLMProvider` Protocol + edge profiles (`get_provider`)
- `SovereignOllamaClient` - keep-alive session, edge defaults, LRU cache
- `portal_core` - AIAgent, MQTTClient, AVCapture, HardwareController, MediaPruner

### 5.2 Weaver (orchestration)

- Multi-tenant LangGraph orchestrator
- Security + telemetry + SessionEvent + Trajectory on process paths
- Tenant-aware routing between specialist agents
- Dual-platform install (`install.sh` / `install.ps1` / `bootstrap.py`)
- Core pin: `@v0.5.9`

### 5.3 Aether (hybrid companion)

- ReAct agentic development orchestrator
- Markdown skills (`kiwi-edge-architecture`, security, sovereignty)
- Soft SessionEvent + Trajectory bridges (optional `aether[core]`)
- **Computer use** hybrid: desktop actuation on Windows + Linux
- HITL gates aligned with stack trust plane
- Install: `install.sh` (Linux) | `install.ps1` (Windows)

### 5.4 Dual-platform hosts

| Role | Platform | Installer |
| :--- | :--- | :--- |
| Dev workstation | Windows 10/11 | `install.ps1` |
| Dev workstation | Linux / macOS | `install.sh` |
| Production edge | RPi 5 16GB + Hailo-10H (Linux) | `install.sh` + compose/K3s |

```mermaid
%%{init: { "theme": "dark", "flowchart": { "curve": "basis", "useMaxWidth": true } }}%%
flowchart LR
 subgraph DEV[Develop]
 Win[Windows]
 Lin[Linux]
 end
 subgraph HYBRID[Hybrid packages]
 Core[Coastal-Alpine-Core]
 Weaver
 Aether
 end
 subgraph EDGE[Deploy]
 RPi[RPi 5 + Hailo]
 K3[K3s / compose]
 end
 Win --> HYBRID
 Lin --> HYBRID
 HYBRID --> EDGE
```

### 5.5 Domain portals

| Portal | Domain | Key capabilities |
|--------|--------|------------------|
| Blue-Moon-Portal | Microgreens / protected cropping | Multi-modal sensor + vision + audio |
| AquaGuard-Portal | Aquaculture / water | Water quality + compliance |
| SoilGuard-Portal | Pasture / soil | Nutrients + soil health |
| Sting-Operation-AI | Biosecurity (wasps) | YOLO / Hailo vision inference |

### 5.6 Hardware & deployment

- **Edge nodes**: Raspberry Pi 5 16GB + Hailo-10H
- **Runtime**: K3s or docker-compose (`k8s/`, `docker-compose.yml`)
- **LLM**: Ollama (`gemma4:e4b` default)
- **Firmware**: Sovereign-Edge-Firmware (ESP32, mTLS MQTT)

---

## 6. Maturity (August 2026)

| Area | Status |
|------|--------|
| Core SDK | Production foundations + Sprint A–C seams (0.5.9) |
| Portals | Flywheel + SecurityGuard integrated |
| CI / SecOps | Enterprise CI, secops, red-team, Dependabot |
| Deployment | K3s manifests + hardening guide |
| Self-improvement | Collection + evaluation; Bayesian hooks on roadmap |

---

## 7. Related documentation

| Document | Description |
|----------|-------------|
| [README.md](./README.md) | Front-page overview + system map |
| [DATA_FLYWHEEL_GUIDE.md](./DATA_FLYWHEEL_GUIDE.md) | Self-improvement loop |
| [SECURITY_POSTURE_REPORT.md](./SECURITY_POSTURE_REPORT.md) | Live threat register |
| [PRODUCTION_HARDENING.md](./PRODUCTION_HARDENING.md) | Enterprise deployment |
| [THREAT_MODEL.md](./THREAT_MODEL.md) | Threat / defence matrix |

---

*Maintained by Coastal Alpine Tech Limited - Taranaki, Aotearoa New Zealand*
