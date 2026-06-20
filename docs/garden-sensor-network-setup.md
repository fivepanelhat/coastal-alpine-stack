# Garden Sensor Network

A local, decentralized IoT sensor network for monitoring garden environmental metrics. Built with an ESP32 edge node publishing data to a Raspberry Pi 5 via MQTT, processed by Node-RED, and stored in InfluxDB 2 for local data sovereignty.

---

## Hardware Stack

| Component | Model & Details |
| --- | --- |
| **Microcontroller** | Keyestudio ESP32 (XC3800) |
| **Local Server** | Raspberry Pi 5 (arm64) + AI HAT 2+ |
| **Temp/Humidity** | DHT11 (XC4520) |
| **Rain Sensor** | Duinotech Rain Sensor (XC4603) |

---

## Software & Infrastructure

* **OS:** Raspberry Pi OS / Debian Trixie
* **Firmware:** Arduino IDE (v1.8.19), ESP32 Core
* **Broker:** Mosquitto MQTT (v2.0.21-1)
* **Database:** InfluxDB 2 (v2.9.1-1)
* **Integration:** Node-RED (v5.0.0)

---

## Wiring Reference

| Sensor | Module Pin | ESP32 Pin | Notes |
| --- | --- | --- | --- |
| **DHT11** | S | GPIO4 | Ensure empty rows between pins to prevent shorts |
| **DHT11** | V | 5V | Direct to ESP32 currently |
| **DHT11** | G | GND | Direct to ESP32 currently |
| **Rain Sensor** | VCC | 5V Rail | Powered from shared breadboard rail |
| **Rain Sensor** | GND | GND Rail | Grounded to shared breadboard rail |
| **Rain Sensor** | AO | GPIO34 | ADC-capable input |
| **Rain Sensor** | DO | N/A | Unconnected |

> **⚠️ Warning:** Be incredibly careful with DHT11 pin placement. Placing S, V, and G in the same breadboard row will short the power to ground, causing a Pi 5 USB over-current event and knocking peripherals offline.

---

## Network & Service Configuration

### 1. MQTT Broker (Mosquitto)

Create a local configuration file to avoid port-binding crashes with the default listener.
**File:** `/etc/mosquitto/conf.d/local.conf`
**Config:** `allow_anonymous true`

See also: [`mosquitto/mosquitto.conf`](../mosquitto/mosquitto.conf) for the full broker listener configuration.

### 2. Firewall (UFW)

Ensure the Pi firewall is configured to accept inbound MQTT traffic from the ESP32 node.
```bash
sudo ufw allow 1883
```

### 3. InfluxDB Setup

Use the rotated compat key (exp 2029) for the official apt repo to avoid expired GPG errors during installation. Configure the database via `http://localhost:8086` and generate an All-Access API Token for Node-RED authorization.

### 4. Node-RED Flow

Install via the official Node-RED Linux bash script. Add the `node-red-contrib-influxdb` package via the Manage Palette menu. Route topics (e.g., `garden/sensor1/temperature`) directly from the `mqtt in` node to the `influxdb out` node using the generated API token.

---

## Known Issues & Troubleshooting

* **Wi-Fi Connection Loops:** ESP32 SSIDs are strictly case-sensitive. Ensure your capitalization is perfectly matched.
* **Failed ESP32 Uploads:** The Pi 5 and ESP32 USB-to-UART combination can repeatedly drop out at high speeds. Hardcode your Arduino IDE upload speed to **115200 baud** to maintain stability.
* **Busy Serial Port:** If an upload fails, the IDE's Java process will often hold `/dev/ttyUSB0` hostage. Closing the Serial Monitor usually releases the lock.
* **Compiler/Linker Errors:** Repeated USB upload interruptions can eventually corrupt the ESP32 board package files (throwing EOF or getApbFrequency errors). Resolve this by deleting `~/.arduino15/packages/esp32` and reinstalling via the Boards Manager.

---

## Project Roadmap

* Confirm fresh ESP32 board package reinstall completes and compiling succeeds.
* Re-upload the combined sketch (DHT11 + rain sensor + MQTT) with a healthy compiler.
* Debug intermittent DHT11 reads (test migrating power from direct-ESP32 to the shared 5V rail).
* Complete Node-RED wiring for `garden/sensor1/rain` directly to InfluxDB.
* Integrate physical light and moisture sensors into the enclosure.
* Deploy Grafana to visualize the InfluxDB metrics.
* Configure persistent headless boot for all Pi services (`systemctl enable`).

---

## Related Repos

| Repo | What Lives There |
| --- | --- |
| [`Sovereign-Edge-Firmware/`](../Sovereign-Edge-Firmware/README.md) | ESP32 firmware, wiring reference, and troubleshooting |
| [`mosquitto/`](../mosquitto/README.md) | MQTT broker configuration |
| [`rpi_secops/`](../rpi_secops/README.md) | Raspberry Pi security hardening and ACLs |

---

Wayne Roberts, Coastal Alpine Tech Limited
16:53:37 Saturday 20/06/2026
