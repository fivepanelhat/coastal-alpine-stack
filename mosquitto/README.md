# Mosquitto MQTT Broker

![CI](https://github.com/fivepanelhat/coastal-alpine-stack/actions/workflows/secops.yml/badge.svg?branch=main)

**Coastal Alpine Tech Limited**

Local Mosquitto MQTT broker configuration for the Coastal Alpine Stack edge deployment. Handles message routing between ESP32 sensor nodes and the Raspberry Pi 5 processing pipeline.

---

## Broker Configuration

The broker is configured to accept anonymous connections on the standard MQTT port for local-network sensor traffic.

**File:** `mosquitto.conf`

```
listener 1883 0.0.0.0
allow_anonymous true
```

> **Note:** For production deployments using mTLS-secured MQTT (port 8883), see the ACL and TLS configuration in [`rpi_secops/mosquitto.acl`](../rpi_secops/mosquitto.acl).

---

## Firewall (UFW)

Ensure the Raspberry Pi firewall is configured to accept inbound MQTT traffic from ESP32 nodes on the local network:

```bash
sudo ufw allow 1883
```

---

## Garden Sensor Network Integration

This broker sits between the ESP32 edge nodes and the Node-RED → InfluxDB pipeline:

```
ESP32 (DHT11 + Rain Sensor)
    ↓ MQTT publish
Mosquitto Broker (port 1883)
    ↓ subscribe
Node-RED
    ↓ route by topic
InfluxDB 2
```

Topics follow the pattern `garden/sensor1/<metric>` (e.g., `garden/sensor1/temperature`, `garden/sensor1/rain`).

For the full deployment guide, see [garden-sensor-network-setup.md](../docs/garden-sensor-network-setup.md).

---

## Avoiding Port-Binding Crashes

If using the default Mosquitto installation alongside a custom config, create a local override file to prevent the default listener from conflicting:

**File:** `/etc/mosquitto/conf.d/local.conf`

```
allow_anonymous true
```

This prevents the default config from binding port 1883 before your custom listener.
