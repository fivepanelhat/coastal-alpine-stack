# Production Hardening Guide - Coastal Alpine Stack

## Overview
This guide provides enterprise and government-grade hardening recommendations for deploying the Coastal Alpine Stack in production environments (edge, K3s, air-gapped, or sovereign data centers).

## 1. Security
- Use the `SecurityGuard` class from `coastal_alpine_core` for all LLM inputs.
- Enable Gitleaks in CI (already configured).
- Run with non-root user in containers.
- Use read-only root filesystems where possible.
- Implement network policies in K3s to restrict east-west traffic.
- Rotate Ollama API keys and MQTT credentials regularly.

## 2. Observability & Telemetry
- Integrate `TelemetryTracker` with `include_system_metrics=True` on critical paths.
- Export structured JSON logs to a local aggregator (e.g., Loki or filebeat).
- Monitor power, latency, and system metrics for the global optimisation objective.

## 3. Deployment
- Prefer K3s or microk8s on edge nodes.
- Use the provided example manifests in `k8s/`.
- Enable Pod Security Standards (restricted).
- Use immutable tags or digests for container images.

## 4. Resilience
- Implement circuit breakers around LLM calls.
- Use the offline fallback in `SovereignOllamaClient`.
- Run media pruner and health checks as background tasks.
- Test graceful degradation during connectivity blackouts.

## 5. Compliance
- Maintain chained audit logs (already in core).
- Document all actuator actions for regulatory review.
- Align with Te Mana Raraunga principles for data sovereignty.

## 6. Secrets Management
- Never commit secrets. Use external secret stores or Kubernetes secrets with encryption at rest.
- Rotate credentials on a schedule.

## Recommended Stack
- Edge Nodes: Raspberry Pi 5 + Hailo NPU
- Orchestration: K3s
- LLM Runtime: Ollama (local)
- Monitoring: Prometheus + Grafana (local)
- Logging: Structured JSON + local aggregator

For government deployments, engage with the security matrix and threat model documents in this repository.
