# Hardened NZ AI Safety Guidelines
**Coastal Alpine Tech / Aether / Kiwi Edge Stack**  
**Version 1.0.0 — 16 July 2026**

These guidelines harden official New Zealand AI materials into enforceable, fail-closed, production-ready controls for sovereign edge, hybrid agentic, and offline-first systems.

They are designed for Coastal Alpine Tech and the Aether fleet while remaining suitable for reference by other NZ organisations building high-stakes AI.

---

## 1. Purpose & Scope

Apply to every AI system, agent, model, data flywheel, RAG pipeline, computer-use path, and edge deployment under Coastal Alpine Tech (Coastal-Alpine-Core, Weaver, Aether, domain portals, Sovereign-Edge-Firmware, Front_Line_Whanau, and related projects).

Cover the full lifecycle: design, development, inference, monitoring, evaluation, and decommissioning.

Prioritise fail-closed behaviour, human authority, data sovereignty, and cultural safety over convenience or autonomy.

---

## 2. Official NZ Alignment

These guidelines implement and exceed:

- Public Service AI Framework (GCDO) and Responsible AI Guidance for the Public Service: GenAI
- MBIE Responsible AI Guidance for Businesses and New Zealand’s AI Strategy (Investing with Confidence)
- Algorithm Charter for Aotearoa New Zealand (transparency, partnership, human oversight, impact assessment)
- Privacy Act 2020 and relevant sector legislation
- Te Mana Raraunga principles
- NCSC / Five Eyes guidance on AI-related cyber risk

They convert voluntary guidance into mandatory controls for CAT systems.

---

## 3. Core Hardened Principles

1. **Human Authority is Non-Negotiable**  
   Agents may only inform, draft, prepare, monitor, and remind.  
   Humans alone advise, decide, sign, file, send, pay, or actuate high-impact controls.  
   No system may present agent output as final authority.

2. **Sovereignty First (Te Mana Raraunga + Data Locality)**  
   Prefer local / on-device / NZ-resident processing and storage.  
   Owner-controlled or jointly-controlled keys.  
   No silent exfiltration.  
   Explicit, recorded consent graphs for any data movement.  
   Māori data and knowledge treated as taonga under rangatiratanga.

3. **Fail-Closed & Least Privilege**  
   Default deny.  
   SecurityGuard-style input/output screening, injection defence, tenant isolation, and capability gating are mandatory.  
   Systems must degrade gracefully to safe deterministic behaviour when models or connectivity fail.

4. **Transparency & Explainability with Purpose**  
   Maintain structured, auditable trails of prompts, decisions, tool calls, and human overrides.  
   Explanations must be meaningful to the affected party and to cultural advisors where relevant.  
   Align with Algorithm Charter transparency commitments.

5. **Cultural Safety & Te Tiriti Partnership**  
   Actively mitigate cultural bias, especially regarding mātauranga Māori, te reo Māori, and Pacific knowledge.  
   Embed Te Ao Māori perspectives in design, evaluation, and high-impact use cases.  
   Partnership is operational, not performative.

6. **Risk-Proportionate Human Oversight**  
   Risk tier determines required HITL gates, review frequency, and approval authority.  
   High-impact or novel uses require multi-person or external cultural/technical review.

7. **Continuous Assurance & Anti-Hallucination**  
   Grounding, verification, red-teaming, and outcome recording (data flywheel) are required.  
   Hallucinated or ungrounded high-stakes content is treated as a safety failure.

8. **Accountability & Auditability**  
   Clear ownership, versioned policies, reproducible runs where feasible, and retained records sufficient for regulatory, cultural, or legal scrutiny.

---

## 4. Risk Tiering & HITL Escalation

Use the standard Aether HITL gate levels (L0–L4). Map risk as follows:

| Tier              | Examples                                                                 | Minimum Gate | Additional Requirements                                      |
|-------------------|--------------------------------------------------------------------------|--------------|--------------------------------------------------------------|
| Low               | Internal drafting, non-personal research summaries                       | L0 / L1     | Logging + basic SecurityGuard                                |
| Medium            | Tenant-facing advice, operational recommendations                        | L2          | Explicit human approval before action                        |
| High              | Actuation, safety-critical decisions, personal or Māori data, regulatory compliance, computer-use on production systems | L2 or L3 | Multi-person or elevated review + cultural safety check where relevant + full audit trail |
| Critical / Novel  | New model classes, cross-border data movement, high-stakes autonomous loops, public-facing high-impact systems | L3 or L4 | Formal impact assessment + external or cultural advisory input + founder-level gate |

**Default** for any new external, production, health, cultural, or deployment action is **L2 (Approve)**.

---

## 5. Mandatory Technical & Governance Controls

- **Input/Output Guards**: Every agent and portal path must run SecurityGuard (or equivalent) before model invocation and before any external action.
- **HITL Gates**: Hard stops for write actions, computer-use actuation, high-impact recommendations, data export, model updates, and any action affecting safety, consent, or legal/regulatory compliance.
- **Local-First Preference**: Ollama / edge models preferred. Cloud models only with explicit justification, data minimisation, and contractual / documented sovereignty protections.
- **Tenant & Data Isolation**: Strict partitioning of vector stores, SQL, and memory. No cross-tenant leakage.
- **Logging & Provenance**: Structured, preferably immutable logs with human-readable audit views.
- **Evaluation & Red-Teaming**: Adversarial testing (prompt injection, cultural bias, capability escalation) before promotion to production or pilot. Ongoing monitoring of drift and failure modes.
- **Consent & Purpose Limitation**: Explicit, recorded purpose for data use. No secondary use without fresh consent or clear legal basis.
- **Decommissioning**: Secure deletion paths and key destruction when systems or data leave scope.

---

## 6. Te Mana Raraunga Operational Mapping

| Principle          | Operational Requirement                                                                 |
|--------------------|------------------------------------------------------------------------------------------|
| Rangatiratanga    | Decision rights and key control remain with data owners / mana whenua where applicable. |
| Whakapapa         | Maintain lineage of data, models, and decisions.                                         |
| Kaitiakitanga     | Active guardianship — minimise collection, maximise protection, plan for intergenerational benefit. |
| Manaakitanga      | Systems must not harm relationships or collective wellbeing.                             |
| Kotahitanga       | Prioritise collective benefit in primary-industry and community deployments under clear consent. |

---

## 7. Implementation Checklist

For every new or significantly changed system:

1. Assign risk tier and required HITL level.
2. Confirm SecurityGuard (or equivalent) is active on every model path.
3. Verify local-first preference or documented justification for external models.
4. Confirm consent graph / purpose limitation for any personal or Māori data.
5. Ensure audit trail captures prompts, decisions, tool calls, and human overrides.
6. Confirm cultural safety review path exists for High / Critical items.
7. Document residual risks and named owner.
8. Update the system register.
9. Schedule red-team + cultural safety review (minimum quarterly at current stage).

---

## 8. Anti-Patterns (Do Not Do)

- Treating voluntary NZ business guidance as sufficient without hardening.
- Claiming Te Mana Raraunga or Algorithm Charter alignment without concrete technical and governance controls.
- Allowing agent outputs to be treated as authoritative without a human gate.
- Defaulting to cloud-hosted models for convenience on sensitive workloads.
- Skipping formal impact assessment for High / Critical or novel uses.
- Logging full prompts that contain personal or culturally sensitive data without minimisation and protection.
- Building features that make later sovereignty or safety compliance harder.

---

## 9. Governance & Review

- These guidelines are owned by Coastal Alpine Tech.
- Any material change requires explicit founder approval.
- Claims of compliance in external materials (grants, investor decks, public statements, pilot agreements) require explicit approval.
- Related Aether skills: `aether-hitl-protocol`, `aether-data-sovereignty`, `aether-core`, `cat-architectural-standards`.

---

**Document status**: Active  
**Last updated**: 16 July 2026  
**Next formal review**: Upon first paid pilot or incorporation, whichever comes first.
