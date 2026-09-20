# M5Stack LoRaWAN Unit (STM32WLE5) — U184-EU868 / US915 / AS923 / CN470

> **Light record.** The **LoRaWAN** answer for a Grove-equipped M5Stack host, including the
> original Cardputer. Region is baked into the SKU, which is the correct way to sell a
> LoRaWAN node. Snapshot 2026-09-04; vendor documentation only, no hardware.

## 1. Identity

| Property | Value |
|---|---|
| SKUs | **U184-EU868**, **U184-US915**, **U184-AS923**, **U184-CN470** |
| **Published** | **2024-12-20** (all four) |
| Price | USD **21.50** (EU868/US915/AS923), **18.95** (CN470) |
| Docs | `https://docs.m5stack.com/en/unit/Unit%20LoRaWAN-EU868` |
| LoRa solution | **STM32WLE5** — 256 KB Flash, 64 KB RAM |
| Module | **RAK3172** — the docs' Certifications section links *"RAK3172 Module Certification Information"* |
| Protocol | **LoRaWAN 1.0.3**, **Class A / B / C**; plus LoRa P2P |
| Activation | **OTAA, ABP** |
| Interface | **UART, 115200 default, AT commands**, HY2.0-4P **PORT.C** |
| Grove pinout | Black `GND` · Red `5V` · Yellow **`UART_RX`** · White **`UART_TX`** |
| RX sensitivity | **−137 dBm** |
| TX power | max **22 dBm** |
| P2P range (claimed) | 2 300 m @ 125 kbps · 1 300 m @ 500 kbps |
| Antenna | 2.8 dBi, 195 mm, **SMA male**, 50 Ω |
| Size / weight | 71.4 × 24.0 × 8.0 mm · 11.9 g |

### Power, by state (unusually well specified)

| State | Current |
|---|---|
| Idle | DC 5 V / **7.23 mA** |
| **Sleep** | DC 5 V / **28.61 µA** |
| RX @ 500 kbps | 9.20 mA |
| TX @ 500 kbps | 11.36 mA |
| RX @ 125 kbps | 8.43 mA |
| **TX @ 125 kbps** | **117.16 mA** |

## 2. Predecessor

M5Stack's own comparison table on the same page:

| | **Unit LoRaWAN-EU868 (U184)** | Unit LoRaWAN 868 MHz (U117, **[EOL]**) |
|---|---|---|
| Chip | **STM32WLE5** | **ASR6501** |
| Sensitivity | −137 dBm | −137 dBm |
| Interface | UART 115200 | UART 115200 |
| LoRaWAN | **1.0.3, Class A/B/C** | 1.0.1, Class A/C |
| TX power | max **22 dBm** | max 21 dBm |

The ASR6501 generation (U115 915 MHz / U116 470 MHz / U117 868 MHz, all published
**2021-05-14**, all now `[EOL]`) predates the Cardputer entirely.

## 3. Cardputer attachability

**Yes, electrically** — it is a UART device on a Grove cable, and both the original
Cardputer (`PORT.CUSTOM`, G2/G1) and the Cardputer-Adv (`PORT.CUSTOM`, G2/G1, plus the
Cap's pass-through) can drive it.

**No, for Meshtastic** — an AT-command LoRaWAN modem is a different protocol universe.
LoRaWAN is star-of-stars to a gateway; Meshtastic is a flooding mesh. They share modulation
and nothing else.

## 4. Why the region-per-SKU model matters

Contrast with the Caps: **U214 and U219 are single wideband SKUs with no published
certification**, while U184 splits the product line by regional band plan and points at
**RAK3172 module certification**. If the wider project needs a *deployable* LoRa link rather
than a benchtop one, this is the architecture that has the regulatory paperwork behind it —
at the cost of giving up direct radio control.

## 5. Related

- Siblings: **Atomic DTU LoRaWAN Base** A152-EU868/US915/CN470 (STM32WLE5CC), USD 22.90,
  published 2025-04-18 — the same silicon in an ATOM-form DTU.
- **M5Stack LoRaWAN EU868 Module (M148)**, USD 24.90, published 2026-04-24 — Core-bus
  module, **not Cardputer-attachable**.
- Libraries: `github.com/m5stack/M5-LoRaWAN`, `M5-LoRaWAN-RAK`, `ATOM_DTU_LoRaWAN` (all last
  pushed 2025-05-12).
- Component: [`components/stmicroelectronics/stm32wle5`](../../../components/stmicroelectronics/stm32wle5/README.md)

## 6. Gaps

- Only the **EU868** documentation page was read; US915/AS923/CN470 pages not fetched.
- Schematic, structure files, AT-command manual and datasheet **located but not fetched**.
- The RAK3172 certification page (the only regulatory pointer in this family besides the
  E220-JP's Telec number) **not fetched**.
- No community report of this unit on any Cardputer.

## 7. Sources

| ID | Title | Class | URL | Retrieved |
|---|---|---|---|---|
| W-1 | Unit LoRaWAN-EU868 documentation | primary | `https://docs.m5stack.com/en/unit/Unit%20LoRaWAN-EU868` | 2026-09-04 |
| W-2 | M5Stack catalogue JSON | primary | `https://shop.m5stack.com/collections/all/products.json` | 2026-09-04 |
