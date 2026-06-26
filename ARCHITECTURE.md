```markdown
# Coastal Alpine Tech — High-Level Architecture

**Version**: June 2026  
**Status**: Active Development — Enterprise Hardening Phase

---

## 1. Vision

Coastal Alpine Tech builds **sovereign, edge-native AI systems** for New Zealand’s primary industries (agriculture, aquaculture, biosecurity). The platform enables local decision-making, data sovereignty (Te Mana Raraunga aligned), and continuous self-improvement while minimising cloud dependency and protecting founder equity.

Core principles:
- **Edge-first & offline-capable**
- **Data sovereignty** (local processing + owner-controlled keys)
- **HITL governance** on high-stakes decisions
- **Self-improving data flywheels**
- **Production-grade security & observability**

---

## 2. Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Portals (Vertical Solutions)            │
│  Blue-Moon │ AquaGuard │ SoilGuard │ Sting-Operation-AI     │
├─────────────────────────────────────────────────────────────┤
│                  Weaver (Multi-Tenant Orchestrator)         │
├─────────────────────────────────────────────────────────────┤
│              Coastal-Alpine-Core (Shared SDK)               │
│   SecurityGuard │ TelemetryTracker │ DataFlywheel │ Models  │
├─────────────────────────────────────────────────────────────┤
│                  Hardware & Edge Runtime Layer              │
│   Raspberry Pi 5 + Hailo NPU │ K3s │ Ollama (local LLM)    │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Coastal-Alpine-Core (Shared Foundation)
- `SecurityGuard` — Modern prompt/input security with structured `SecurityResult`
- `TelemetryTracker` — Latency, power estimation, optional system metrics (`psutil`)
- `DataFlywheel` — Trajectory collection, evaluation, HITL feedback, golden set curation
- `SovereignOllamaClient` — Resilient local LLM client with fallbacks
- `BayesianOptimisationHook` — Future multi-objective optimisation

### 2.2 Weaver (Orchestration Layer)
- Multi-tenant agent orchestrator built on LangGraph
- Protocol-based dependency injection
- Integrated Security + Telemetry + Flywheel
- Tenant-aware routing and handoff between specialist agents

### 2.3 Domain Portals
Each portal specialises in a vertical while sharing the core SDK:

| Portal                | Primary Domain          | Key Capabilities                     |
|-----------------------|-------------------------|--------------------------------------|
| Blue-Moon-Portal      | Microgreens / Protected Cropping | Multi-modal (sensor + vision + audio) |
| AquaGuard-Portal      | Aquaculture / Water     | Water quality + compliance           |
| SoilGuard-Portal      | Pasture / Soil Health   | Soil metrics + nutrient management   |
| Sting-Operation-AI    | Biosecurity (Wasps)     | YOLO vision inference                |

All portals now include full Data Flywheel integration (plan generation + hardware outcome recording).

### 2.4 Hardware & Deployment Layer
- **Edge Nodes**: Raspberry Pi 5 + Hailo AI HAT
- **Orchestration**: K3s (lightweight Kubernetes)
- **LLM Runtime**: Ollama (local models)
- **Observability**: Structured JSON logs + TelemetryTracker
- **Security**: Non-root containers, read-only filesystems, Gitleaks + Bandit in CI

---

## 3. Data Flow (Typical Portal)

1. Sensors / MQTT → `analyze_sensor_state()`
2. Vision + Audio capture → `process_visual_feedback()` / `process_audio_feedback()`
3. Multi-modal reasoning → `generate_optimization_plan()` → **Trajectory recorded**
4. Hardware enforcement → `enforce_plan()` → **Hardware outcome recorded**
5. Compliance / Audit logging
6. Data lands in local `flywheel_*.jsonl` for future improvement

---

## 4. Key Cross-Cutting Concerns

| Concern              | Implementation                              | Status      |
|----------------------|---------------------------------------------|-------------|
| Security             | `SecurityGuard` + Gitleaks + Bandit         | Strong      |
| Observability        | `TelemetryTracker` + structured JSON        | Strong      |
| Self-Improvement     | `DataFlywheel` + Evaluation Loop            | Strong      |
| Deployment           | K3s manifests + `PRODUCTION_HARDENING.md`   | Good        |
| CI/CD                | Hardened workflows (Python 3.10, caching)   | Good        |
| Packaging            | Modern `pyproject.toml` (Core + Weaver)     | Good        |

---

## 5. Current Maturity (June 2026)

- **Core SDK**: Production-ready foundations
- **Portals**: Full flywheel integration complete
- **CI/CD**: Hardened and standardised
- **Deployment**: K3s manifests + hardening guide available
- **Self-Improvement**: Data collection + evaluation in place; fine-tuning & Bayesian optimisation in roadmap

---

## 6. Related Documentation

- `DATA_FLYWHEEL_GUIDE.md` — Detailed guide to the self-improvement system
- `SECURITY_POSTURE_REPORT.md` — Security & hardening status
- `PRODUCTION_HARDENING.md` — Enterprise deployment recommendations
- Individual repo `README.md` files

---

*Maintained by Coastal Alpine Tech Limited — Taranaki, Aotearoa New Zealand*
```