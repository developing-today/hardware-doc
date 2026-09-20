# M5Stack LoRa Unit (E220) — U170 (920 MHz / JP) and U170-433 (433 MHz)

> **Light record.** Included because it is one of the *actual* answers to "what LoRa could
> you attach to a Cardputer before the Cap existed" — a **Grove/UART LoRa modem** that works
> on **any** M5Stack host with a HY2.0-4P port, including the **original Cardputer**.
> Snapshot 2026-09-04. Vendor documentation only; no schematic fetched, no hardware.

## 1. Identity

| | U170 | U170-433 |
|---|---|---|
| Doc name | **Unit LoRaE220-920** ("JP version") | **Unit LoRaE220-433** |
| Store title | LoRa Unit with Antenna (E220) | LoRa Unit 433MHz with Antenna (E220) |
| **Published** | **2023-10-20** | **2024-07-12** |
| Price | USD 33.00 | USD 12.95 |
| Module | **E220-900T22S (JP)** — *Telec cert `001-P01730`* | **E220-400T22S** |
| **Radio chip** | **Semtech LLCC68** | **Semtech LLCC68** |
| Band | **920.6 – 928.0 MHz** | default **433 MHz**, range **410.125 – 493.125 MHz** |
| Max TX | **13 dBm** (~20 mW) | **22 dBm**, software-selectable |
| RX sensitivity | not stated | **−129 dBm** |
| Interface | **UART**, HY2.0-4P Grove | **UART 115200**, HY2.0-4P Grove |
| Antenna | 2.5 dBi, 110 mm, **SMA male** | same |
| Size / weight | 71.4 × 24.0 × 8.0 mm · 19.2 g | 71.4 × 24.0 × 8.0 mm · 19.5 g |

**U170 is the older of the two by nine months and it predates the Cardputer itself by three
days** (Cardputer K132 published 2023-10-13).

## 2. Why it matters to the Cardputer question

The original Cardputer (K132/K132-V11) has **only** a HY2.0-4P Grove port
(`PORT.CUSTOM`, G2/G1) and no expansion bus. A **UART** LoRa modem on that port is
electrically straightforward — G1/G2 are ordinary ESP32-S3 GPIO and can be driven as a
software or hardware UART.

So the honest statement is: **before the Cardputer-Adv, "LoRa on a Cardputer" meant a
Grove-attached E220 or LoRaWAN modem, not a LoRa *radio* the host could drive directly.**

⚠ **But it is not a Meshtastic path, and never was.** Meshtastic requires **direct SPI
access to an SX126x/SX127x/LR11xx**. The E220 hides an LLCC68 behind an **AT-command UART
modem** with a fixed packet format and DIP-switch modes; the host cannot reach the radio's
registers. There is no Meshtastic variant for it and there cannot be one without new
transport code. `executed-success` on the negative: upstream Meshtastic's variant tree has
no E220/LLCC68 entry of any kind.

## 3. What it is good at

Point-to-point and broadcast serial links. Features named by the vendor: **Wake-on-Radio**
(wireless wake-up), carrier sensing, communication keys, and four modes selectable with an
**onboard DIP switch** — transmit, WOR transmit, WOR receive, sleep. That DIP switch is the
distinguishing usability feature: you can get a working link without writing configuration
code at all.

Claimed range for U170: *"up to 5 kilometres"* — no method, antenna height or data rate
given. Treat as marketing.

## 4. Regional variants — the band *is* the SKU

| SKU | Band | Region intent |
|---|---|---|
| U170 | 920.6–928.0 MHz | **Japan** — carries a **Telec certification number, `001-P01730`**, printed in the specification table |
| U170-433 | 410–493 MHz, default 433 | ITU Region 1 ISM / general |

**U170 is the only LoRa product in this whole family with a published regulatory
identifier.** Every Cap — U201, U214, U219 — has none. Worth noting when comparing them.

## 5. Software

`github.com/m5stack/M5-LoRa-E220` and `github.com/m5stack/M5-LoRa-E220-JP` (both last pushed
**2025-01-16**). AT-style configuration over UART. RadioLib is **not** applicable — there is
no SPI to the radio.

## 6. Related components

- **Semtech LLCC68** — a lower-cost SX1262 sibling limited to SF5–SF11. **No component
  record created** by this pass; see [`components/semtech/sx1262`](../../../components/semtech/sx1262/README.md)
  for the family context.
- **Ebyte E220 series** — [`components/ebyte/e220-400t22s`](../../../components/ebyte/e220-400t22s/README.md).
  The repository already holds a record for the related **[E22-900M22S](../../../components/ebyte/e22-900m22s/README.md)** (E22 = SX1262-based, SPI/UART; E220 = LLCC68-based, UART only) — read both before assuming they are interchangeable.

## 7. Gaps

- Schematics, pinouts and DIP-switch tables **not fetched** (`docs.m5stack.com` slugs for
  these units were not resolved — `/en/unit/lorae220-433` and `/en/unit/Unit-LoRaE220-JP`
  both **404**).
- No firsthand community report of an E220 unit on a Cardputer was found in the 217-post
  Reddit sample — only generic *"the rf and the ir and the Lora"* accessory mentions
  ([r/CardPuter 2026-08-30](https://old.reddit.com/r/CardPuter/comments/1w2n1rd/)).
- Whether M5Stack's Cardputer firmware (M5Launcher/Bruce) exposes these units at all:
  unknown.

## 8. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| E-1 | U170 store listing JSON | primary | `https://shop.m5stack.com/products/lora-unit-jp-version-with-antenna-e220.json` | 2026-09-04 | Published 2023-10-20, USD 33.00, `E220-900T22S (JP) @ Telec (001-P01730)`, LLCC68, 13 dBm |
| E-2 | U170-433 store listing JSON | primary | `https://shop.m5stack.com/products/lora-unit-433mhz-with-antenna-e220.json` | 2026-09-04 | Published 2024-07-12, USD 12.95, `E220-400T22S@LLCC68`, 22 dBm, −129 dBm, UART 115200 |
| E-3 | Cardputer documentation | primary | `https://docs.m5stack.com/en/core/Cardputer` | 2026-09-04 | The original Cardputer's only expansion is HY2.0-4P `PORT.CUSTOM` = G2/G1 |
| E-4 | Meshtastic variant tree | primary | `api.github.com/repos/meshtastic/firmware/git/trees/master?recursive=1` | 2026-09-04 | **Negative:** no LLCC68/E220 variant |
