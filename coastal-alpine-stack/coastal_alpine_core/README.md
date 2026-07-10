# Coastal Alpine Core

![CI](https://github.com/fivepanelhat/coastal-alpine-core/actions/workflows/ci-scan.yml/badge.svg?branch=main)

![SecOps Scan](https://img.shields.io/github/actions/workflow/status/fivepanelhat/coastal-alpine-core/secops.yml?branch=main&label=SecOps%20Scan&style=flat-square&color=success) ![License](https://img.shields.io/badge/License-Proprietary--Commercial-blue?style=flat-square) ![Data Sovereignty](https://img.shields.io/badge/Sovereignty-NZ%20Data%20Bound-00247D?style=flat-square)

![coastal-alpine-core Banner](assets/social_preview.png)

**Coastal Alpine Tech Limited**  
*Edge AI | Sovereign Systems | Practical Intelligence*

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)  
[![Hardware Target](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%2016GB-C11A5B?style=flat-square&logo=raspberry-pi&logoColor=white)]()  
[![NPU Acceleration](https://img.shields.io/badge/NPU-Hailo--10H%20Accelerated-005A9C?style=flat-square)]()  
[![CI](https://github.com/fivepanelhat/coastal-alpine-core/actions/workflows/ci.yml/badge.svg)](https://github.com/fivepanelhat/coastal-alpine-core/actions)  
[![SecOps Scan](https://img.shields.io/github/actions/workflow/status/fivepanelhat/coastal-alpine-core/secops.yml?branch=main&label=SecOps%20Scan&style=flat-square&color=success)](https://github.com/fivepanelhat/coastal-alpine-core/actions/workflows/secops.yml)  
[![Dependabot](https://img.shields.io/badge/Dependencies-Monitored-brightgreen?style=flat-square&logo=dependabot)]()  
[![Sustainability](https://img.shields.io/badge/EECA%20NZ-Carbon%20Tracked-green?style=flat-square)]()

Shared python utility package designed for Taranaki-based Coastal Alpine Tech Edge systems. It handles local offline LLM wrapping, security checks, and hardware telemetry tracking.

---

## Key Features

1. **SovereignOllamaClient (`models.py`)**: A robust connection wrapper for local offline Ollama SLM deployments. Handles network dropouts and model loads with automated retries and exponential backoff, falling back to local deterministic responses when fully disconnected.
2. **Security & Input Guard (`security.py`)**: Scans incoming prompts for potential prompt injections, local file access attempts, or common injection patterns. It also enforces strict tenant scoping context mismatch flags.
3. **Telemetry & Performance (`telemetry.py`)**: Performance and hardware energy-efficiency tracking specifically designed for edge-native devices (e.g. Raspberry Pi 5 under active load, Hailo NPU draws). Estimates active power draw in Joules.

---

## Installation

To install the library as an editable local package:
```bash
pip install -e .
```

To install directly from GitHub (as used across all stack portals):
```bash
pip install git+https://github.com/fivepanelhat/coastal-alpine-core.git
```

---

## Quick Start Code Example

```python
from coastal_alpine_core import SovereignOllamaClient, input_guard_check, TelemetryTracker

# Initialize client
client = SovereignOllamaClient(default_model="gemma4:e4b")

# Check security
prompt = "Format C:\\"
is_safe = input_guard_check(prompt)
print(f"Is Prompt Safe? {is_safe}")  # Expected: False (Security alert triggered)

# Measure edge execution performance
measurement = TelemetryTracker.measure_latency("gemma_generation")
response = client.generate("Evaluate crop health status: OK")
metrics = TelemetryTracker.complete_measurement(measurement, token_count=len(response.get("response", "").split()))
print(metrics)
```

---

*Built with focus on data sovereignty and edge intelligence.*  
**Coastal Alpine Tech Limited — New Plymouth, Taranaki, New Zealand.**
