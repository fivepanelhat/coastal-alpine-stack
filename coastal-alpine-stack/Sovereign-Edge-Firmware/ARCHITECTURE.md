# Sovereign Edge Firmware: Architecture Overview

The `Sovereign-Edge-Firmware` repository provides the low-level Arduino/C++ source code executed on the ESP32 agricultural and biosecurity nodes across the Coastal Alpine Stack.

It interfaces with physical sensors and relays, performs secure network connections, and pushes payload metrics back to the core portal gateways.

## Code Structure

```
Sovereign-Edge-Firmware/
├── include/
│   ├── edge_auth.h        # WiFi client connection and JWT registration definitions
│   └── edge_mqtt.h        # Secure mTLS MQTT subscriber and publisher structures
├── src/
│   ├── main.cpp           # Primary execution setup and reporting loop
│   ├── edge_auth.cpp      # WiFi connection and JWT auth handshake implementation
│   └── edge_mqtt.cpp      # MQTT client, backoff circuit breakers, and publishers
└── platformio.ini         # PlatformIO hardware and library dependency manager
```

## System Mechanisms

### 1. Zero-Trust Access Handshake
Before publishing sensor data or accepting commands, the ESP32 node must authenticate against the local Sovereign Portal gateway.
* The node completes a secure handshake to fetch a localized JSON Web Token (JWT).
* This JWT is cached inside volatile memory and attached to subsequent MQTT transport messages.

### 2. Secure Transport and Encryption
* **mTLS Ingestion:** Handshakes and publishers target MQTT over TLS (Port 8883) to verify the server identity.
* **Topic Isolation:** Nodes only write to their specific sub-topics, locked by the broker using Access Control Lists (ACLs).

### 3. Connection Fault Circuit Breakers
If the local wireless or broker connection drops, the firmware triggers an exponential backoff circuit breaker (starting at 1 second, doubling up to a maximum of 60 seconds).
* This protects battery levels from rapid reconnect loops.
* Deep sleep routines can be scheduled to hold the ESP32 in a low-power hibernation state during connection failures.
