# Ebyte E220 series — `E220-400T22S` and `E220-900T22S`

- **Category:** **UART LoRa modem module** — an LLCC68 radio behind a microcontroller that
  speaks a serial/AT-style protocol. The host **cannot reach the radio's registers.**
- **Scope:** this page covers both M5Stack-fitted E220 variants;
  [`../e220-900t22s/`](../e220-900t22s/README.md) is a pointer to it.
- **Retrieved:** 2026-09-04
- **⚠ Not the same as the E22.** This repository also holds
  [`components/ebyte/e22-900m22s`](../e22-900m22s/README.md), which is **SX1262-based**.
  Read both before assuming interchangeability — §3.

## 1. Identity

| | `E220-400T22S` | `E220-900T22S (JP)` |
|---|---|---|
| Manufacturer | Chengdu Ebyte | Chengdu Ebyte |
| **Radio chip** | **Semtech LLCC68** | **Semtech LLCC68** |
| Band | **410.125 – 493.125 MHz** (default 433) | **920.6 – 928.0 MHz** |
| Max TX | **22 dBm**, software-selectable | **13 dBm** (~20 mW) |
| RX sensitivity | **−129 dBm** | not published by M5Stack |
| Host interface | **UART, 115200 default** | UART |
| Certification | none cited | **Telec `001-P01730`** |
| Fitted on | [M5Stack Unit LoRaE220-433 (U170-433)](../../../devices/m5stack/unit-lora-e220/README.md) | [M5Stack Unit LoRaE220-920 (U170)](../../../devices/m5stack/unit-lora-e220/README.md) |

Modes, selectable by an **onboard DIP switch** on the M5Stack units: transmission,
**WOR (Wake-on-Radio) transmit**, WOR receive, sleep. Additional features named by the
vendor: carrier sensing, communication keys, point-to-point and broadcast addressing.

## 2. What "UART modem" means for firmware — and why it rules out Meshtastic

The E220 is not a transceiver you drive; it is a **link** you configure. The module's own
MCU owns the LLCC68 and exposes a serial pipe, a configuration register set reachable with
`AT`-style / `0xC0`-framed commands, mode pins (`M0`/`M1`, wired to the DIP switch on the
M5Stack units) and an `AUX` busy/ready line.

| You want | Possible with E220? |
|---|---|
| Simple point-to-point or broadcast serial link | ✅ — easier than raw LoRa; the DIP switch alone can get a link up |
| Wake-on-Radio low-power receive | ✅ — a genuine strength |
| Choosing SF/BW/CR freely | ⚠ only from the module's supported table |
| Raw packet access, custom PHY, arbitrary sync words | ❌ |
| **Meshtastic** | ❌ **No.** Meshtastic drives an SX126x/SX127x/LR11xx **over SPI**. There is no upstream variant for any UART LoRa modem, and there cannot be one without a new radio-transport abstraction. `executed-success` on the negative: the full recursive Meshtastic variant tree (2026-09-04) contains no LLCC68 or E220 entry |
| **LoRaWAN** | ❌ — different product (see [STM32WLE5](../../stmicroelectronics/stm32wle5/README.md)) |

**This is the single most important fact in this record**, because M5Stack sells the E220
units as "LoRa" alongside genuinely SPI-attached SX1262 products, and buyers reasonably
assume they are equivalent. They are not.

## 3. E220 vs E22 — do not confuse them

| | **E220** | **E22** |
|---|---|---|
| Radio silicon | **LLCC68** | **SX1262** |
| Host access to the radio | **UART modem only** | E22 variants exist with **SPI** access to the SX1262 |
| Spreading factors | LLCC68 supports **SF5–SF11** (no SF12) | SX1262 supports SF5–SF12 |
| Meshtastic-capable | **No** | Depends on the variant — an SPI E22 exposes a real SX1262 |
| Record here | this page | [`components/ebyte/e22-900m22s`](../e22-900m22s/README.md) |

The **absence of SF12** on LLCC68 is the practical difference that bites: the longest-range,
lowest-rate LoRa configurations are simply unavailable, and a link configured for SF12 at
the other end will not be heard.

## 4. Used By

### [M5Stack LoRa Unit (E220)](../../../devices/m5stack/unit-lora-e220/README.md) — U170 and U170-433

Grove **HY2.0-4P** (UART), 5 V supply, SMA-male antenna, onboard DIP switch.
Attachable to **any** M5Stack host with a Grove port — **including the original
Cardputer (K132)**, whose only expansion is `PORT.CUSTOM` (G2/G1). That makes the E220 unit
one of the genuine pre-Cap answers to "LoRa on a Cardputer", with the large caveat in §2.

Libraries: `github.com/m5stack/M5-LoRa-E220` and `M5-LoRa-E220-JP` (both last pushed
2025-01-16).

## 5. Gaps

- **No Ebyte datasheet retrieved** for either part. Register map, command framing, `AUX`
  timing and the `M0`/`M1` mode table are unestablished here.
- M5Stack's documentation slugs for these units were **not resolved**
  (`/en/unit/lorae220-433`, `/en/unit/Unit-LoRaE220-JP` both 404), so no pin map or DIP
  table was obtained.
- The **LLCC68 has no component record** in this repository.
- No firsthand community report of an E220 unit driven from a Cardputer was found in the
  217-post Reddit sample.

## 6. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| EB-1 | U170-433 store listing JSON | primary | `https://shop.m5stack.com/products/lora-unit-433mhz-with-antenna-e220.json` | 2026-09-04 | `E220-400T22S@LLCC68`, 410–493 MHz, 22 dBm, −129 dBm, UART 115200, four DIP modes |
| EB-2 | U170 store listing JSON | primary | `https://shop.m5stack.com/products/lora-unit-jp-version-with-antenna-e220.json` | 2026-09-04 | `E220-900T22S (JP) @ Telec (001-P01730)`, LLCC68, 920.6–928.0 MHz, 13 dBm |
| EB-3 | Meshtastic variant tree | primary | `api.github.com/repos/meshtastic/firmware/git/trees/master?recursive=1` | 2026-09-04 | **Negative result** — no LLCC68/E220 variant exists |
| EB-4 | `m5stack/M5-LoRa-E220`, `M5-LoRa-E220-JP` | primary | `https://github.com/m5stack/M5-LoRa-E220` | 2026-09-04 | The vendor libraries, last pushed 2025-01-16 |
