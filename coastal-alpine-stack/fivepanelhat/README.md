# Coastal Alpine Tech Limited: Kiwi Edge AI Stack

![CI](https://github.com/fivepanelhat/fivepanelhat/actions/workflows/secops.yml/badge.svg?branch=main)


![Coastal Alpine Tech Banner](assets/social_preview.png)

[![License](https://img.shields.io/badge/License-Proprietary--Commercial-blue?style=flat-square)](LICENSE)  
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)  
[![Hardware Target](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%2016GB-C11A5B?style=flat-square&logo=raspberry-pi&logoColor=white)]()  
[![Hardware: Edge AI](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%20%2B%20Hailo--10L%2F10H%20NPU-orange.svg)]()  
[![Sovereignty](https://img.shields.io/badge/Sovereignty-NZ%20Data%20Bound-00247D?style=flat-square)]()  
[![SecOps Scan](https://img.shields.io/github/actions/workflow/status/fivepanelhat/fivepanelhat/secops.yml?branch=main&label=SecOps%20Scan&style=flat-square&color=success)](https://github.com/fivepanelhat/fivepanelhat/actions/workflows/secops.yml)  
[![Sustainability](https://img.shields.io/badge/EECA%20NZ-Carbon%20Tracked-green?style=flat-square)]()

Welcome to the official repository landing page for **Coastal Alpine Tech Limited**, headquartered in New Plymouth, Taranaki, New Zealand. We design and deploy offline-native, data-sovereign edge intelligence systems for remote, high-stakes industrial, agricultural, and biosecurity settings across New Zealand.

Our stack operates entirely on-premise (e.g. on Raspberry Pi 5 hardware with NPU acceleration) to maintain customary data rights (Te Mana Raraunga / Māori Data Sovereignty) and guarantee 100% operational uptime in rural catchments facing cloud blackouts.

---

## 🚀 The Kiwi Edge AI Stack Portfolio

| Repository | Role | Core NZ Regulations | Primary Hardware Target |
| :--- | :--- | :--- | :--- |
| [weaver](https://github.com/fivepanelhat/weaver) | Multi-tenant helpdesk & local RAG mesh | Privacy Act 2020, Public Records Act 2005 | RPi 5 (8GB/16GB) |
| [Blue-Moon-Portal](https://github.com/fivepanelhat/Blue-Moon-Portal) | Multi-modal edge AI for microgreen cultivation (Byte Size Kai) | Biosecurity Act 1993, HSNO Act 1996, Food Act 2014 | RPi 5 + AI HAT+ (Hailo-8 NPU) |
| [Sting-Operation-AI](https://github.com/fivepanelhat/Sting-Operation-AI) | YOLO wasp & bee classifier beehive sentinel | Biosecurity Act 1993, Animal Welfare Act 1999 | RPi 5 + Hailo-10L NPU |
| [AquaGuard-Portal](https://github.com/fivepanelhat/AquaGuard-Portal) | Water runoff, sediment, & turbidity telemetry | RMA 1991, Horizons One Plan, regional consents | RPi 5 + Camera + Mic |
| [SoilGuard-Portal](https://github.com/fivepanelhat/SoilGuard-Portal) | Soil N-P-K, pH, & moisture crop control | NES-F 2020 (Synthetic N cap), FWFPs | RPi 5 + AI HAT+ |
| [coastal-alpine-core](https://github.com/fivepanelhat/coastal-alpine-core) | Shared SDK (Offline LLM wrapper, safety, telemetry) | - | Python 3.10+ Edge-wide |

---

## 🛠️ Stack Architecture Overview

The following diagram illustrates how the shared core SDK powers data-sovereign telemetry parsing, security screening, and offline reasoning across the different application portals:

```mermaid
flowchart TD
    subgraph "Sovereign Local Hardware"
        Core["coastal-alpine-core SDK<br/>(Safety Guards / Telemetry)"]
        
        subgraph "Application Layer"
            Weaver["weaver<br/>(LangGraph AI Helpdesk)"]
            BlueMoon["Blue-Moon-Portal<br/>(Microgreen Crop AI)"]
            Sting["Sting-Operation-AI<br/>(Bee Sentinel Box)"]
            Aqua["AquaGuard-Portal<br/>(Runoff Telemetry)"]
            Soil["SoilGuard-Portal<br/>(NPK Soil Monitor)"]
        end
    end
    
    Weaver & BlueMoon & Sting & Aqua & Soil -->|Imports & Telemetry| Core
    Core -->|Local Port Inference| Ollama["Local Ollama<br/>(Gemma 4 Instruct)"]
```

---

## 💼 Core Operating Philosophies

1. **Sovereign by Design**: Data generated on NZ *whenua* is processed and stored locally, fully conforming to Te Mana Raraunga principles. We avoid commercial third-party cloud data leakage.
2. **Rural Resilience**: Our systems are engineered to withstand rural connectivity blackouts, executing local multi-modal vision and audio inference without any internet connection.
3. **Regulatory Safety**: Systems actively control actuators (like locking out fertigation lines or disabling class 3B lasers) to automatically prevent regulatory breaches of Regional Council rules.

Developed with pride in **Taranaki, New Zealand** 🇳🇿
