# Coastal Alpine Core: Architecture Overview

The `coastal_alpine_core` repository provides shared libraries and utility frameworks used across all edge portals and orchestrator agents in the Coastal Alpine Stack.

It contains both a Python package and a Node.js package, exposing telemetry, security, database, and environmental sustainability helpers.

## Package Structure

```
coastal_alpine_core/
├── coastal_alpine_core/       # Python Package
│   ├── analytics/             # Device posture and statistical z-score outlier detection
│   ├── logging/               # PMIC power consumption and sequentially chained audit logging
│   ├── models.py              # LLM client wrapper for Ollama Gemma 4 with retries
│   ├── security.py            # Prompt injection scanning and multi-tenant constraints
│   └── telemetry.py           # Core latency and resource tracking helpers
├── src/                       # Node.js Package (CommonJS)
│   ├── database/              # SQLCipher encrypted-at-rest local cache interface
│   ├── security/              # Actuator command timing and velocity checking
│   ├── sustainability/        # Battery adaptive sleep interval calculators
│   ├── attestation_validator.js # TPM 2.0 quote and PCR baseline verifier
│   └── validation.js          # Graceful payload boundary parsing and clamps
├── pyproject.toml             # Python build configuration
└── package.json               # Node.js package description
```

## Core Systems & Mechanisms

### 1. Zero-Trust Hardware Attestation
The Node.js validator (`attestation_validator.js`) checks edge-provided hardware quotes (cryptographic PCR measurements signed by the TPM 2.0 module's AIK key) against a registered public key and the expected "Golden Boot" baseline hash (PCR 0-7) to verify edge node integrity before releasing configuration keys.

### 2. Encryption at Rest (SQLCipher)
Local caches are secured via `secure_store.js` which configures 256-bit AES database encryption at rest using SQLCipher. It requires a high-entropy key of at least 32 characters, optimizes pages to 4KB, and locks key derivation iterations (KDF) to 64,000 passes to prevent brute-force attacks.

### 3. Sustainability and Power Governance
* **Power Profiling:** Calculates optimal reporting intervals (deep sleep duty cycles) based on battery voltage trends (e.g. step-down to 30 or 60 min when critical, or increase to 5 min when solar charging).
* **Carbon Mitigations:** Estimates local power mitigation metrics based on regional grid emission coefficients (e.g., Taranaki 0.122 kg CO2e/kWh, Horowhenua 0.098 kg CO2e/kWh).
* **Sequentially Chained Audits:** Chained logging hashes each log entry with the SHA-256 hash of the previous line, ensuring telemetry integrity and compliance logs cannot be retrospectively altered.

### 4. Input Guards and Posture Controls
* **Prompt Protection:** Validates LLM input against common SQL/Prompt injection profiles.
* **Device Posture Check:** Validates incoming telemetry packets to check if the firmware matches expected SHA-256 signatures and validates that critical services (like security daemons) are actively running.
* **Telemetry Outliers:** Computes rolling Z-Scores over a 50-sample sliding window, flagging outliers with Z-scores > 3.5.
