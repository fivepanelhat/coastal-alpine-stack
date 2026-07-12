# Kotahitanga Investment Strategy — coastal-alpine-stack Deployment Layer

**Repository:** coastal-alpine-stack  
**Primary Tier:** DIAMOND (enterprise-grade deployment + webhooks)  
**Secondary Tier:** PLATINUM (autonomous remediation + self-healing)  
**Role:** Infrastructure-as-Code + deployment automation + webhook relay  
**Compliance Baseline:** 89% (target: ≥95% for Diamond tier)  
**Last Updated:** 2026-07-12

---

## Stack's Role in Kotahitanga

coastal-alpine-stack is the **infrastructure-as-code and deployment automation layer**. It manages:

1. **Infrastructure Provisioning** — Terraform for Aotearoa-based AWS infrastructure (VPC, security groups, databases)
2. **Secure Webhook Relay** — Receive GitHub events, validate signatures, relay to Weaver (fail-closed on auth failure)
3. **Deployment Automation** — Blue-green deployments, zero-downtime updates, automated rollbacks
4. **HITL Approval Gates** — Human review required before production deployment
5. **Compliance as Code** — Embedding compliance checks in every deployment (automatic rollback if violations detected)

**Diamond Tier Classification Rationale:**
- Infrastructure code directly controls security posture (encryption, firewalls, access controls)
- Webhook relay is security boundary (must fail-closed on signature validation failure)
- Deployments affect all downstream systems (Weaver, Core, Aether)
- Requires immutable audit trail (who deployed what, when, why)
- External audit required (SOC 2 Type II)

**Platinum Secondary Rationale:**
- Autonomous remediation: if compliance drift detected, auto-revert deployment
- Self-healing: if deployment causes SLA breach, auto-rollback
- Continuous compliance: every deployment re-checks 225-point compliance baseline

---

## Data Classification in Stack

| Level | Examples | Protection |
|-------|----------|-----------|
| **Level 1 (Public)** | Infrastructure configuration, deployment logs (sanitized) | Standard TLS, public documentation |
| **Level 2 (Restricted)** | GitHub secrets, encryption keys (in transit) | Vault encryption, MFA on vault access, audit logging |
| **Level 3 (Sensitive)** | Production encryption keys, iwi data encryption keys | Dual-key HSM, air-gapped key management, CAB veto on key rotation |

**Key Constraint:** No unencrypted credentials in code (static analysis prevents commits).

---

## Compliance Status (Current)

**Overall Score: 89% (200/225 items) — YELLOW (remediation in progress)** ⚠️

| Category | Items | Passing | Score | Status |
|----------|-------|---------|-------|--------|
| CC1 (Governance) | 15 | 15 | 100% | ✓ |
| CC6 (Access) | 49 | 45 | 92% | ✓ |
| CC7 (Change/Secrets) | 38 | 34 | 89% | ⚠️ |
| CC9 (Security) | 42 | 39 | 93% | ✓ |
| A (Availability) | 22 | 20 | 91% | ✓ |
| P (Privacy) | 34 | 31 | 91% | ✓ |
| Te Mana Raraunga | 11 | 11 | 100% | ✓ |
| Architecture | 9 | 9 | 100% | ✓ |
| **TOTAL** | **225** | **200** | **89%** | **🟡 YELLOW** |

**Status:** Remediation in progress. **50% escrow hold** on new capital allocations until Green status achieved.

**Remediation Plan (Target Green by Sept 30, 2026):**
- CC7 gaps (5 items): Automated secret rotation every 90 days (not manual), encryption key backup procedures, webhook fail-closed testing
- A gaps (2 items): Disaster recovery testing schedule, RTO/RPO documentation
- P gaps (3 items): Data retention auto-deletion for non-Māori data, privacy audit checklist

**Timeline:**
- Week 1–2: Secret rotation automation (high priority)
- Week 3–4: Webhook fail-closed testing + documentation
- Week 5–6: Disaster recovery procedures + automation

---

## OCAP® Verification Framework for Stack

### Infrastructure Possession Model

**Ownership:**
- Organization owns infrastructure code (Git repository)
- Aotearoa community owns computing infrastructure (data centers, physical equipment)
- Iwi owns encryption keys for Level 3 data

**Control:**
- Infrastructure changes require code review + HITL approval
- Deployment pipeline: staging (auto) → approval gate → production (manual trigger)
- Emergency override: CTO/CISO can force production deployment (with post-action audit)
- Quarterly infrastructure review (security posture assessment)

**Access:**
- Terraform state: encrypted at rest (S3 + AES-256)
- Deployment credentials: stored in Vault (rotated 90-day cycle)
- API keys: max 1-hour expiry (short-lived service credentials)
- All access logged to immutable audit system (18-month retention)

**Possession:**
- Infrastructure: AWS Aotearoa region only (no international cloud)
- Data centers: physical access controls (badge/CCTV/visitor log)
- Backup infrastructure: separate Aotearoa-based data center
- Disaster recovery: tested monthly (RTO ≤4 hours, RPO ≤1 hour)

---

## Webhook Relay Security (Stack's Key Control)

**Rule:** Webhook signatures must be validated before processing. If validation fails: FAIL CLOSED (reject webhook, log incident, alert).

**Implementation (Python example):**

```python
import hmac
import hashlib

def validate_webhook_signature(payload_body: bytes, signature_header: str | None, secret: bytes) -> bool:
    """
    Validate GitHub webhook signature.
    FAIL CLOSED: reject if signature missing or invalid.
    """
    # Fail closed: signature header MUST be present
    if signature_header is None:
        logger.error("Webhook rejected: missing signature header")
        return False
    
    # Compute expected signature (constant-time comparison)
    expected_sig = "sha256=" + hmac.new(secret, payload_body, hashlib.sha256).hexdigest()
    
    # Constant-time comparison (prevents timing attacks)
    if not hmac.compare_digest(expected_sig, signature_header):
        logger.error("Webhook rejected: signature mismatch")
        return False
    
    return True

# Usage in Flask
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature-256')
    
    if not validate_webhook_signature(payload, signature, webhook_secret):
        return {"error": "Unauthorized"}, 401
    
    # Process webhook (only if signature valid)
    return process_deployment(payload), 202
```

**Compliance Goal:** CC6 (Access Control) + CC9 (Logical Security)

---

## Deployment Pipeline with HITL Gates

**Rule:** Every production deployment requires human approval.

**Workflow:**

```
Developer Push → Commit to feature branch
  ↓
GitHub Actions:
  [ ] Static analysis (lint, security scanning)
  [ ] Unit tests pass
  [ ] Docker image build + container scan (Trivy)
  [ ] Compliance check (225-point baseline didn't drop)
  ↓ (all pass)
PR Review Required:
  [ ] Code review (peer approval + CISO sign-off for security-related changes)
  [ ] Compliance review (if data model changes: additional review)
  ↓ (merged to main)
Staging Deployment (Automatic):
  [ ] Docker image pushed to registry
  [ ] Deployed to staging environment
  [ ] Integration tests run (E2E workflows)
  [ ] Load tests run (verify performance)
  [ ] Backup restoration test (if infrastructure change)
  ↓ (all pass)
Production Deployment (Manual Approval):
  [ ] Incident Commander reviews staging results
  [ ] CTO approves deployment plan + rollback procedure
  [ ] Scheduled deployment window + stakeholder notification
  ↓ (approval given)
Blue-Green Deployment:
  [ ] New version deployed to green environment (parallel to blue)
  [ ] Health checks pass (green environment healthy)
  [ ] Switch traffic to green (users routed to new version)
  [ ] Monitor for 1 hour (no error spikes, SLA maintained)
  ↓ (stable)
Rollback Authority:
  [ ] If issues detected: Incident Commander can trigger rollback (revert to blue)
  [ ] Post-incident: Investigation + remediation required before re-deploy
```

---

## Infrastructure as Code (Diamond Tier Requirement)

**Rule:** All infrastructure must be managed via Terraform (no manual AWS console changes).

**Compliance Impact:**
- ✓ Immutable audit trail (Terraform state + Git history shows all changes)
- ✓ Code review gate (changes reviewed before applied)
- ✓ Disaster recovery (infrastructure rebuilds from Terraform in minutes)
- ✓ Environment parity (dev/staging/prod configurations identical, parameterized)
- ✓ Security baseline (security groups, encryption, RBAC enforced by code)

**Structure:**
```
terraform/
├── main.tf            (VPC, subnets, security groups)
├── database.tf        (RDS PostgreSQL, encrypted)
├── storage.tf         (S3 buckets, encryption, versioning)
├── iam.tf             (IAM roles, policies, MFA enforcement)
├── monitoring.tf      (CloudWatch, alarms, dashboard)
└── variables.tf       (environment-specific parameters)

environments/
├── dev.tfvars         (non-production configuration)
├── staging.tfvars     (pre-production configuration)
└── prod.tfvars        (production configuration, encrypted)
```

---

## Active Kotahitanga Projects Using Stack

| Project ID | Name | Infrastructure | Allocation | Status | Compliance |
|------------|------|-----------------|-----------|--------|-----------|
| KAS-2026-001 | Sovereign Regional Health Cloud | AWS NZ + bare-metal | $500K (infrastructure) | ACTIVE | 89% ⚠️ |

**For detailed tracking, see:**
- `.github/investment/CAPITAL_ALLOCATION_TRACKER.md` (updated weekly)

---

## How to Request Infrastructure Changes

**For Non-Critical Changes (Gold Tier workflow):**

1. File GitHub issue (feature request + business case)
2. Compliance review (3 days): any security impact?
3. Terraform code review (5 days): security review + cost estimate
4. Staging deployment (auto) + testing (5 days)
5. Production deployment approval + merge to main
6. Blue-green deployment + monitoring (1 hour)

**For Critical Changes (Diamond Tier workflow, requires HITL approval):**

1. Detailed proposal to CTO + CISO (security assessment)
2. **HITL Gate 1:** Compliance review (10 days)
3. **HITL Gate 2:** Incident Commander review (5 days)
4. **HITL Gate 3:** Board approval (if cost >$100K or security-critical)
5. Terraform code review (5 days)
6. Staging deployment + comprehensive testing (10 days)
7. Production deployment + monitoring (24/7 for first week)

**Timeline:** 7–30 days depending on change criticality

---

## Compliance Obligations During Project

**Monthly:**
- ☐ 225-point compliance checklist (webhook, secrets, deployment logs)
- ☐ Terraform state audit (no manual changes made outside code)
- ☐ Secret rotation verification (all service credentials rotated within 90 days)
- ☐ Deployment log review (audit trail intact, all deployments authorized)

**Quarterly:**
- ☐ Full 225-point compliance re-audit
- ☐ Disaster recovery drill (infrastructure rebuilt from Terraform)
- ☐ Infrastructure penetration test (external auditor)
- ☐ Board infrastructure review (cost, security posture, SLA metrics)

**If Compliance Drops Below 70%:**
- 🔴 RED: Immediate halt to all deployments (no new code can be deployed)
  - Infrastructure lockout: production systems returned to last-known-good state
  - Incident response triggered
  - Emergency patching only (life-or-death security issues)
  - Remediation required before deployments resume

---

## Key Governance Controls for Stack

### Fail-Closed Webhook Validation

**Rule:** If webhook signature validation fails, reject the webhook (don't process it).

**Why:**
- GitHub webhooks contain sensitive deployment commands
- Unsigned webhooks = potential unauthorized deployments
- Fail-closed = default deny (safe mode)

### Immutable Audit Trail

**Rule:** All infrastructure changes logged + audit trail retained 18 months minimum.

**Implementation:**
```
Terraform Execution:
  1. State file locked (only one apply() at a time)
  2. Plan reviewed (terraform plan output saved to audit log)
  3. Changes applied (terraform apply logged with timestamp + user)
  4. State file updated (Git commit + signed)

Audit Trail:
  - Git repository: all code changes with commit messages
  - S3 state file: versioning enabled (track all state changes)
  - CloudTrail: all AWS API calls (immutable, non-repudiable)
  - Deployment logs: who, what, when, approval status
```

### Blue-Green Deployments (Zero-Downtime)

**Rule:** Production updates must be zero-downtime (traffic switched, not restarted).

**Benefits:**
- ✓ No service interruption (users unaffected)
- ✓ Quick rollback (switch back to blue if issues detected)
- ✓ Testing in production (health checks verify new version before switching traffic)

---

## References

1. **Kotahitanga Investment Strategy:** `.github/investment/KOTAHITANGA_INVESTMENT_STRATEGY.md`
2. **Compliance Audit Checklist:** `.github/compliance/references/COMPLIANCE_AUDIT_CHECKLIST.md`
3. **Incident Response Playbook:** `.github/compliance/references/INCIDENT_RESPONSE_PLAYBOOK.md`
4. **SOC 2 Controls (CC7/A):** `.github/compliance/references/SOC2_CONTROL_MATRIX.md`

---

## Contacts

| Role | Name | Email |
|------|------|-------|
| CTO / Infrastructure Lead | [Name] | [Email] |
| CISO / Security Lead | [Name] | [Email] |
| Compliance Officer | [Name] | [Email] |
| Incident Commander | [Name] | [Email] |
| Repository Owner | [Name] | [Email] |

---

**Version:** 1.0.0  
**Status:** YELLOW (remediation in progress, 50% escrow hold)  
**Remediation Target:** Green by 2026-09-30
