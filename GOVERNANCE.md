# Governance — CAT Architectural Standards

This repository is governed by the **Coastal Alpine Tech (CAT) Architectural
Standards** maturity model (Gold / Diamond / Platinum). The canonical decision
skill lives in the [Aether](https://github.com/fivepanelhat/Aether) repo at
`skills/cat-architectural-standards/SKILL.md`.

## Tier classification

The stack repo **composes the full sovereign edge runtime**, so it spans all
three tiers by design (field → fabric → runtime apps → trust):

| Tier | Role | Applies to the stack as |
| :--- | :--- | :--- |
| **Diamond** *(primary)* | Enterprise-grade foundation | Field firmware, mTLS MQTT fabric, K3s manifests, SecOps, `PRODUCTION_HARDENING.md`, least-privilege CI, secret scanning — the production edge platform. |
| **Platinum** *(co-primary)* | Intelligent self-improving system | The estate-wide data flywheel (capture → curate → improve) and portal AI agents on Ollama + Hailo-10H. |
| **Gold** *(secondary)* | Workflow-native design | Each domain portal (Aqua/Soil/Blue/Sting) mirrors a real primary-industry workflow end to end. |

## Operating rules

- **Classify before building.** Declare the primary (and any secondary) tier in
  each PR/ADR. Cross-cutting infra changes are **Diamond**; flywheel/agent
  changes are **Platinum**.
- **HITL gates are non-negotiable:** changes to production manifests, security
  posture, mTLS/secrets, data sovereignty, classification, or any tier-compliance
  release claim require human approval.
- **Sovereignty overlay applies to all tiers.** Te Tiriti o Waitangi and Te Mana
  Raraunga principles are architectural requirements — local processing, whenua
  custody of data, no silent cloud exfiltration.

## References

- Aether: `skills/cat-architectural-standards/SKILL.md` — decision protocol
- `SECURITY.md`, `SECURITY_MATRIX.md`, `THREAT_MODEL.md`,
  `PRODUCTION_HARDENING.md`, `ARCHITECTURE.md` — Diamond/sovereignty detail
