# Coastal Alpine Tech - Stack Security Matrix

This security registry maps the priority and implementation file layers responsible for enforcing zero-trust and data sovereignty boundaries across all monorepo components.

| Repository | Component | Security Priority | Target File / Implementation Layer |
| :--- | :--- | :--- | :--- |
| **Coastal-Alpine-Core** | TPM Attestation Validator <br> Compliance Logging Engine | Critical (P1) | [attestation_validator.js](file:///c:/Users/Admin/.gemini/antigravity-ide/scratch/coastal-alpine-stack/coastal_alpine_core/src/attestation_validator.js) <br> [compliance_guard.py](file:///c:/Users/Admin/.gemini/antigravity-ide/scratch/coastal-alpine-stack/coastal_alpine_core/coastal_alpine_core/logging/compliance_guard.py) |
| **Sovereign-Edge-Firmware** | TPM Quote Generator <br> mTLS Client Setup | Critical (P1) | `src/attestation_agent.py` <br> `src/mqtt_client.cpp` |
| **Weaver** | mTLS Broker & ACLs <br> Prometheus Metrics Scraper | High (P2) | [mosquitto.acl](file:///c:/Users/Admin/.gemini/antigravity-ide/scratch/coastal-alpine-stack/rpi_secops/mosquitto.acl) <br> [prometheus.yml](file:///c:/Users/Admin/.gemini/antigravity-ide/scratch/coastal-alpine-stack/telemetry/prometheus.yml) |
| **AquaGuard-Portal** | Actuator Guard Rails <br> Behavioral Analytics | High (P2) | [actuators.js](file:///c:/Users/Admin/.gemini/antigravity-ide/scratch/coastal-alpine-stack/AquaGuard-Portal/src/routes/actuators.js) <br> [behavioral_analytics.js](file:///c:/Users/Admin/.gemini/antigravity-ide/scratch/coastal-alpine-stack/coastal_alpine_core/src/security/behavioral_analytics.js) |
| **SoilGuard-Portal** | Ingestion Rate Limiting <br> Prometheus Exporting | Medium (P3) | API Controller routing infrastructure |
| **Blue-Moon-Portal** | Local JWT Authority <br> Asymmetric Signing | Medium (P3) | Express middleware authorization core |
