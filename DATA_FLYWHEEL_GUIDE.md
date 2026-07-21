# Data Flywheel Guide - Coastal Alpine Stack

## Overview

The Data Flywheel is a core component of the Coastal Alpine sovereign edge AI platform. It enables continuous collection of high-value interaction trajectories, automated quality evaluation, human-in-the-loop feedback, and future self-improvement through fine-tuning or Bayesian optimisation.

Its purpose is to turn real-world operational data (sensor readings, AI plans, hardware outcomes) into a growing asset for model improvement while maintaining full data sovereignty.

## Core Components

### 1. `Trajectory` (Dataclass)
A structured record of a single meaningful event in the system.

Key fields:
- `trajectory_id`
- `action` (e.g. `generate_optimization_plan`, `hardware_irrigation`)
- `outcome` (`success`, `failure`, `human_corrected`)
- `input_summary` / `output_summary`
- `latency_seconds`, `estimated_energy_joules`
- `metadata` (plan_id, requires_human_review, etc.)
- `quality_score` (assigned by evaluation loop)
- `human_feedback`

### 2. `DataFlywheel` Class
Main interface for recording and managing trajectories.

**Key Methods**:
- `record_trajectory(trajectory)`
- `record_hardware_outcome(plan_id, action, success, ...)` - Convenience method used after `enforce_plan()`
- `update_with_human_feedback(original_id, feedback, new_outcome)`
- `evaluate_trajectory(trajectory, llm_judge_func=None)` - Rule-based + optional LLM judge
- `curate_golden_set(min_quality=0.7)` - Returns high-quality trajectories for training
- `get_recent_trajectories(limit=100)`

**Usage Pattern**:
```python
from coastal_alpine_core.flywheel import DataFlywheel, Trajectory

flywheel = DataFlywheel(storage_path="flywheel_my_portal.jsonl")

# Automatic recording after plan generation or hardware action
flywheel.record_hardware_outcome(
 plan_id=plan["plan_id"],
 action="irrigation",
 success=True,
 metadata=plan
)
```

### 3. `BayesianOptimisationHook`
Scaffolding for future multi-objective optimisation (latency, power, compliance cost, information gain).

Currently contains placeholder methods that can be connected to a real optimiser.

## Integration Across the Stack

| Component | Integration Level | What is Recorded |
|-------------------------|------------------------|-------------------------------------------|
| Blue-Moon-Portal | Full | Plan generation + Hardware outcomes |
| AquaGuard-Portal | Full | Plan generation + Hardware outcomes |
| SoilGuard-Portal | Full | Plan generation + Hardware outcomes |
| Sting-Operation-AI | Full (Inference) | YOLO detection results + confidence |
| Weaver | Partial | Orchestrator message processing |

All portals now automatically record trajectories when:
- An optimization plan is generated
- A hardware action is executed (success/failure)

## Human-in-the-Loop (HITL)

Operators can provide feedback on specific trajectories:

```python
flywheel.update_with_human_feedback(
 original_trajectory_id="traj-abc123",
 feedback="Irrigation should have been higher",
 new_outcome="human_corrected"
)
```

Feedback is stored as new correction trajectories and can be used for quality scoring.

## Evaluation Loop

`evaluate_trajectory()` assigns a `quality_score` (0.0-1.0) using:
- Rule-based heuristics (outcome, `requires_human_review` flag)
- Optional LLM-as-Judge (pass any callable that scores text)

High-scoring trajectories are returned by `curate_golden_set()` for fine-tuning or RAG augmentation.

## Current File Locations

Each portal uses its own flywheel file:
- `flywheel_blue_moon.jsonl`
- `flywheel_aquaguard.jsonl`
- `flywheel_soilguard.jsonl`
- `flywheel_sting_operation.jsonl`

These are stored locally on the edge node for full data sovereignty.

## Future Roadmap

1. **Prometheus Metrics Export** - Expose flywheel statistics as metrics.
2. **Active Learning Pipeline** - Use low-confidence or failed trajectories to trigger targeted data collection.
3. **LLM-as-Judge Refinement** - Improve automated quality scoring.
4. **LoRA Fine-Tuning Integration** - Periodically fine-tune local models using curated golden sets.
5. **Bayesian Optimisation** - Replace placeholder hook with real multi-objective optimiser.

## Related Documentation

- `SECURITY_POSTURE_REPORT.md`
- `PRODUCTION_HARDENING.md`
- `coastal_alpine_core/flywheel.py` (source code)

---

*Maintained by Coastal Alpine Tech - June 2026*
