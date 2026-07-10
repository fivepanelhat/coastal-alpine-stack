# Coastal Alpine Tech - Stack Security Matrix

Maps priority controls and implementation layers for zero-trust / data-sovereignty boundaries. Updated 2026-07-11 against GitHub security notifications.

| Repository | Component | Priority | Implementation layer |
| :--- | :--- | :--- | :--- |
| **Coastal-Alpine-Core** | Prompt / tenant / posture guards | Critical (P1) | `src/coastal_alpine_core/security.py` (`SecurityGuard`, `tenant_isolated_query`, `device_posture_check`) |
| **Coastal-Alpine-Core** | Telemetry & flywheel integrity | High (P2) | `src/coastal_alpine_core/telemetry.py` |
| **Sovereign-Edge-Firmware** | TPM quote / mTLS client | Critical (P1) | `src/attestation_agent.py`, MQTT mTLS client |
| **Weaver** | Multi-tenant routing + SecurityGuard | Critical (P1) | `weaver_graph`, agent ingress, Core guards |
| **Weaver** | LangChain supply chain | High (P2) | `langsmith>=0.8.18`, `pydantic-settings>=2.14.2` |
| **AquaGuard-Portal** | Actuator guard rails | High (P2) | Portal AI agent + hardware enforce paths |
| **SoilGuard-Portal** | Ingestion rate limits / soil AI | Medium (P3) | API controllers + Core guards |
| **Blue-Moon-Portal** | Multimodal crop AI prompts | High (P2) | `ai_agent` + Core `SecurityGuard` |
| **Sting-Operation-AI** | Vision inference + secret hygiene | High (P2) | Inference engine + `tools/download_dataset.py` (no key disk write) |
| **coastal-alpine-stack** | ChromaDB vector memory | Critical (P1 residual) | Localhost-only bind until GHSA-f4j7-r4q5-qw2c patched upstream |
| **All CI** | GITHUB_TOKEN least privilege | High (P2) | Workflow `permissions: contents: read` (release jobs: contents write) |
| **All product repos** | Dependency notifications | High (P2) | `.github/dependabot.yml` + SecOps / red-team workflows |

See `SECURITY.md` and `SECURITY_POSTURE_REPORT.md` for the live threat register and SLAs.
