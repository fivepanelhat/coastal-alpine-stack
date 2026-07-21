# Unified Security Posture & Hardening Report

**Coastal Alpine Tech Kiwi Edge AI Stack** 
**Date**: 11 July 2026 
**Scope**: Coastal-Alpine-Core, Weaver, Blue-Moon-Portal, AquaGuard-Portal, SoilGuard-Portal, Sting-Operation-AI, coastal-alpine-stack, Aether, Front_Line_Whanau, whanau-preterm-support-hub

## Executive Summary

The stack was re-audited against **GitHub security notifications** (Dependabot, Code Scanning, GHSA/NVD) and local `pip-audit` / `npm audit` runs.

**Overall posture**: Strong - shared `SecurityGuard`, SecOps/red-team CI, least-privilege workflow tokens, and dependency floors for known CVEs. One **critical** upstream gap remains: ChromaDB pre-auth RCE has **no fixed release** yet (network isolation required).

## Notification sources used

| Source | Result (2026-07-11) |
| ------ | ------------------- |
| Dependabot open alerts (all org repos scanned) | None open (many repos previously lacked Dependabot config - now enabled) |
| Code scanning open | coastal-alpine-stack: missing workflow permissions (fixed); Sting: clear-text API key write (fixed) |
| `pip-audit` | Aether env transitive: langsmith, pydantic-settings (floored in Weaver/stack); chromadb GHSA critical (mitigated, not patched upstream) |
| `npm audit` (Front_Line, whanau, portals) | 0 vulnerabilities |

## Component status

### Coastal-Alpine-Core (v0.5.4)
- Expanded `SecurityGuard` patterns (jailbreak, SSRF metadata, exfil, pipe-to-shell, private keys).
- Precompiled hot-path guards, flywheel rotation, edge Ollama client (from 0.5.3).
- SECURITY.md threat register + SLA.

### Weaver
- `langsmith>=0.8.18`, `pydantic-settings>=2.14.2`, Core pin bump path to 0.5.3+.
- CI least-privilege permissions; Dependabot pip weekly.

### Portals (Aqua / Blue-Moon / SoilGuard)
- SECURITY.md notifications sections; CI `permissions: contents: read`.
- Continue using Core `SecurityGuard` on LLM paths.

### Sting-Operation-AI
- **Fixed** CodeQL clear-text storage: dataset tool no longer writes Roboflow keys to `.env`.
- CI permissions + SECURITY.md.

### coastal-alpine-stack
- Enterprise CI permissions fixed (clears CodeQL `actions/missing-workflow-permissions`).
- Dependabot for pip/Actions/Docker; chromadb threat documented; floors for langsmith / pydantic-settings.
- SECURITY.md rewritten (was placeholder template).

### Aether / Front_Line_Whanau / whanau-preterm-support-hub
- Dependabot added; SECURITY.md + notifications; CI permissions on FLW/Aether.

## Cross-cutting controls

| Control | Status | Details |
| ------- | ------ | ------- |
| Secret scanning (Gitleaks) | Active | SecOps CI + `.gitleaks.toml` where present |
| SAST (Bandit / CodeQL) | Active | SecOps + Enterprise CI |
| Red team | Active | Scheduled adversarial suites |
| Least-privilege Actions | Active | Default `contents: read` on CI workflows |
| Dependabot | Active | All scanned product repos |
| npm supply chain | Clean | 0 high/critical on audited lockfiles |
| ChromaDB exposure | Mitigated | Localhost-only until upstream patch |
| Prompt injection | Strong | Core `SecurityGuard` 0.5.4 patterns |

## Remaining gaps

1. **ChromaDB GHSA-f4j7-r4q5-qw2c** - wait for fixed release; keep network isolation.
2. **Secret scanning** disabled on some repos (e.g. Weaver) - enable at org/repo settings when plan allows.
3. **Code scanning** not configured on all repos (Aether, FLW, etc.) - enable CodeQL where feasible.
4. Full multi-portal e2e security regression in a single CI job still optional (member repos own CI).

## Conclusion

Security notifications have been **actioned**: code fixes, dependency floors, workflow hardening, Dependabot coverage, and markdown threat registers updated across the estate. Ready for continued government/enterprise review with the ChromaDB network control as the primary residual risk.
