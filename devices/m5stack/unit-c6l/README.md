# M5Stack Unit C6L for Meshtastic (SKU U202)

> **Light record, but read §2** — this is the **only** M5Stack LoRa product that gives an
> *original* Cardputer a working Meshtastic node, and it does it by not being a peripheral
> at all. Published **2025-10-10**, USD **22.90**. Snapshot 2026-09-04; vendor
> documentation + upstream Meshtastic; no hardware.

## 1. Identity

| Property | Value |
|---|---|
| SKU | **U202** |
| Store title | *M5Stack C6L Unit for Meshtastic (SX1262, ESP32-C6)* |
| **Published** | **2025-10-10** |
| Price | USD **22.90** |
| Core | **[Stamp C6LoRa](../stamp-c6lora/README.md)** module — ESP32-C6 + SX1262 + RF switch |
| SoC | ESP32-C6, RISC-V 160 MHz HP core + 20 MHz LP core, **16 MB flash**, **Wi-Fi 6 (2.4 GHz)** |
| LoRa | **SX1262**, 868 – 923 MHz, **+22 dBm**, **−147 dBm** |
| Display | **SSD1306** 0.66" OLED, 64 × 48 |
| Indicators | **WS2812C** RGB LED, buzzer, user button |
| Protection | **AW32901FCR** over-voltage protection |
| Antennas | **two SMA** — 2.4 GHz Wi-Fi (84 mm, 3 dBi) and LoRa (108 mm, 3 dBi). Connectors described as *"female thread, female pin"* |
| Expansion | HY2.0-4P Grove; LEGO-compatible holes |
| Power | DC 5 V via USB-C **or** via the Grove port |
| Size / weight | 62.0 × 24.0 × 8.0 mm · 13.6 g (excl. antennas) |

### Power, by state

| State | Current |
|---|---|
| Sleep (HY2.0-4P powered) | **696.86 µA** |
| Sleep (USB-C powered) | 866.42 µA |
| LoRa RX standby (USB-C) | **85.18 mA** |
| LoRa max-power continuous TX (USB-C) | **80.02 mA** |

> ⚠ **RX standby draws *more* than continuous TX** in M5Stack's own table (85.18 vs
> 80.02 mA). That is counter-intuitive but not impossible — the SX1262 in LDO regulation
> mode has a high receive current, and the transmit figure may be measured with a duty
> cycle. **The vendor states no measurement conditions.** Recorded as published, flagged as
> suspicious; do not build a power budget on it without measuring.

## 2. ⭐ Why this is the answer for an *original* Cardputer

Unit C6L **is its own Meshtastic node.** It has its own MCU, its own flash, its own screen,
its own radio, its own antenna and its own power input. The Grove cable is a *link to a
companion*, not a peripheral bus.

- **Upstream Meshtastic variant exists:**
  [`variants/esp32c6/m5stack_unitc6l/`](https://github.com/meshtastic/firmware/tree/master/variants/esp32c6/m5stack_unitc6l)
  — `variant.h`, `variant.cpp`, `platformio.ini`, `pins_arduino.h`. `executed-success` on
  the tree listing, 2026-09-04.
- **Protobuf hardware model:** `meshtastic_HardwareModel_M5STACK_C6L = 111` — the entry
  immediately before `M5STACK_CARDPUTER_ADV = 112`.

So an original Cardputer running a **client** firmware (MeshClient, `cardtastic`,
`sigil-03/cardputer-meshtastic-client`, or the `Cardkb_emulator` trick) plus a Unit C6L
gives you a keyboard-driven Meshtastic experience on hardware that **cannot take a Cap**.
That is the practical, community-visible route, and it is why the "older LoRa extension for
the Cardputer" question has a different answer depending on which Cardputer you mean.

⚠ The exact Cardputer↔C6L transport (BLE companion, serial-over-Grove, or both) was **not
verified** by this pass. Recorded as `inferred` from the architecture; someone should check
before promising it works.

## 3. Related

- [`../stamp-c6lora/README.md`](../stamp-c6lora/README.md) — the module inside it
- [`components/semtech/sx1262`](../../../components/semtech/sx1262/README.md)
- [`components/diodes-incorporated/pi4ioe5v6408`](../../../components/diodes-incorporated/pi4ioe5v6408/README.md) — inside the Stamp module
- [`../cap-lora-1262/README.md`](../cap-lora-1262/README.md) — the Cardputer-**Adv** alternative

## 4. Gaps

- `docs.m5stack.com` slug not resolved (`/en/unit/UnitC6L` and `/en/unit/Unit-C6L` both
  **404**). All specification data here comes from the **store listing**, not the
  documentation page.
- Schematic, pin map and the Meshtastic variant's contents **not fetched**.
- The RX-vs-TX current anomaly (§1) unexplained.
- Cardputer↔C6L pairing mechanics unverified.

## 5. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| C-1 | U202 store listing JSON | primary | `https://shop.m5stack.com/products/m5stack-c6l-unit-for-meshtastic-sx1262-esp32-c6.json` | 2026-09-04 | Published 2025-10-10, USD 22.90, full specification |
| C-2 | Meshtastic repository tree | primary | `api.github.com/repos/meshtastic/firmware/git/trees/master?recursive=1` | 2026-09-04 | `variants/esp32c6/m5stack_unitc6l/` exists (4 files) |
| C-3 | Meshtastic `mesh.pb.h` | primary | `github.com/meshtastic/firmware/blob/master/src/mesh/generated/meshtastic/mesh.pb.h` | 2026-09-04 | `M5STACK_C6L = 111` |
