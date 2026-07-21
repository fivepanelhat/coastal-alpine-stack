# Security Policy - coastal-alpine-stack

Monorepo / superproject for the Kiwi Edge AI stack (submodules: Core, Weaver, portals, Sting, firmware).

## Supported Versions

| Track | Supported |
| ----- | --------- |
| `main` | Yes - security updates |
| Tags `v*` | Best-effort if still deployed |

## Vulnerability Disclosure

Do **not** file public issues for exploitable stack defects.

- Prefer a **private GitHub Security Advisory** on this repository, or contact the Chief Architect.
- Include: which submodule/path, edge vs cloud exposure, and whether multi-tenant isolation is affected.

## Security Notifications

| Channel | Owner | Action |
| ------- | ----- | ------ |
| Dependabot (pip / Actions / Docker) | This repo | Weekly; group `security-critical` for chromadb, langsmith, pydantic-settings |
| Code scanning | Enterprise CI + SecOps | Least-privilege workflow tokens; Bandit + Trivy |
| Submodule alerts | Member repos | Fix in upstream repo, bump submodule pointer |
| NVD / GHSA | Architecture | Update `SECURITY_POSTURE_REPORT.md` + pin floors |

## Active threat register (2026-07)

| ID | Threat | Severity | Stack mitigation |
| -- | ------ | -------- | ---------------- |
| GHSA-f4j7-r4q5-qw2c | ChromaDB pre-auth code injection (1.5.9, **no patch yet**) | Critical | Bind Chroma to `127.0.0.1` only; never expose `/api` externally; disable remote model trust; NetworkPolicy on K3s; watch for fixed release |
| GHSA-f4xh-w4cj-qxq8 | LangSmith TracingMiddleware file read | High | `langsmith>=0.8.18` in root requirements |
| GHSA-4xgf-cpjx-pc3j | pydantic-settings secrets_dir symlink | Medium | `pydantic-settings>=2.14.2` |
| CodeQL missing workflow permissions | Over-broad `GITHUB_TOKEN` | Warning | `permissions: contents: read` on Enterprise CI |
| Prompt injection across portals | LLM abuse | High | Shared `SecurityGuard` from Core 0.5.4 |

## Quality & SecOps

- `enterprise-ci.yml` - lint, Bandit, Trivy, SDK import smoke (submodules recursive).
- `secops.yml` / `redteam.yml` / `ci-scan.yml` - scheduled and PR security paths.
- See also: `SECURITY_MATRIX.md`, `SECURITY_POSTURE_REPORT.md`, `THREAT_MODEL.md`, `PRODUCTION_HARDENING.md`.

## SLA

Critical edge/actuator paths: mitigation within **48 hours**. Multi-tenant isolation defects: treat as Critical.

## Fleet security principles

- **No silent exfiltration** of personal or tenant operational data
- Prefer **local-first** processing; third-party AI only with explicit operator configuration and UI/docs disclosure
- Report vulnerabilities via GitHub Security Advisories or the maintainer contact on the org profile
- High-stakes production changes require human approval (HITL)

