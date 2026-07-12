# Compliance — NZ AI + SOC 2 Type II

This repository is governed by the **NZ AI Compliance + SOC 2 Type II** framework.  
**Classification:** Diamond (primary) | Platinum (secondary) | Gold (tertiary)

## Purpose

Coastal Alpine Stack is the **orchestration + deployment** layer. Handles:
- Webhook relay for GitHub GitOps automation
- Autonomous swarm loop triggering
- Compliance code remediation
- Deployment orchestration

**Compliance Impact:** HIGH
- Autonomous decision-making (requires HITL for high-risk remediation)
- Signature verification (fail-closed on missing secrets)
- Webhook security (prevent unauthorized GitOps triggers)

## Key Requirements

- **Webhook Security:** Fail-closed on missing secrets, signature verification
- **HITL Gates:** High-risk remediation requires human approval
- **Audit Trail:** All autonomous decisions logged
- **Code Security:** No secrets in CI logs

## Compliance Contacts

- Compliance Officer: [ASSIGN]
- Privacy Officer: [ASSIGN]
- CISO / Security Lead: [ASSIGN]

## Compliance Milestones

- [ ] Phase 1: Governance (Week 1)
- [ ] Phase 2: Technical controls (Week 4)
- [ ] Phase 3: Privacy Act (Week 4)
- [ ] Phase 4: Te Mana Raraunga (Week 6)
- [ ] Phase 5: Incident response (Week 8)
- [ ] Phase 6: SOC 2 audit (Week 12)

## Monthly Checklist

- [ ] Webhook verification working (fail-closed)
- [ ] HITL approvals logged (all decisions auditable)
- [ ] No secrets in deployment logs
- [ ] Incident response tested
- [ ] Audit logs immutable + 18-month retention

**Sign-Off:** _________________ Date: _________

**Related:** [NZ AI Compliance Skill](./.github/compliance/nz-ai-compliance-soc2/)  
**Last Updated:** 2026-07-12
