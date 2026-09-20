# GNSS ceramic patch antenna (18 × 18 × 4 mm class) — `ANT1818-04`

- **Category:** generic **passive ceramic patch antenna** for L1-band GNSS (~1.56–1.61 GHz)
- **⚠ Not to be confused with** [`components/generic/ceramic-antenna`](../ceramic-antenna/README.md),
  which documents the **2.4 GHz chip antennas** on an unrelated board. Different band,
  different physics, different part class.
- **Research status:** part number read from a schematic comment only. **No datasheet, no
  manufacturer identified.**
- **Retrieved:** 2026-09-04

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Schematic comment | **`ANT181804`** as extracted — almost certainly rendered **`ANT1818-04`** | Cap LoRa-1262 schematic V1.1, `J1` |
| Reading of the name | `18 × 18` mm footprint, `04` = **4 mm** ceramic height — the standard naming convention for this part class | `inferred` |
| Type | passive ceramic patch, single feed | topology on the sheet |
| Band | GNSS **L1 neighbourhood** — GPS/QZSS/SBAS L1, GALILEO E1, GLONASS R1, BDS B1I/B1C | follows from the receiver it feeds |
| Manufacturer | **unidentified** | — |

⚠ The literal extracted string is `ANT181804` with no hyphen. The repository's PaperMono
work already documents that M5Stack Altium PDFs mangle punctuation in some text layers, so
a missing hyphen is the likely explanation — but **the reading `ANT1818-04` is `inferred`**,
not read.

## 2. Why the size matters

An 18 mm patch on a 4 mm-thick ceramic is a compromise between gain and volume, and it
constrains what the rest of the receive chain must do:

- A patch this small has modest gain and a narrow effective bandwidth, so it is normally
  paired with an **external LNA placed immediately at the feed** to set the system noise
  figure. That is exactly what the Cap LoRa-1262 does with a
  [MAX2659](../../analog-devices/max2659/README.md).
- Ceramic patches are **strongly detuned by nearby metal and by the ground plane they sit
  on**. A patch inside a plastic Cap, 40 mm from a +22 dBm sub-GHz transmitter and above a
  host PCB, is not operating under datasheet conditions.
- They are **directional (hemispherical, sky-facing)**. Orientation matters; owners
  reporting "no satellites indoors" are usually seeing exactly this plus building
  attenuation.

## 3. Used By

### [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) — designator `J1`

| Item | Value |
|---|---|
| Feed | → `L1` **6.8 nH ±5 %** series match → `U1` **MAX2659** LNA `RFIN` (pin 3) |
| Onward | LNA `RFOUT` (6) → `C5` 470 pF → `M2` **ATGM336H-6N** pin 11 `ANT` |
| Bias path | LNA supply from `+3.3V`; GNSS `VCC_RF` (pin 14) through `FB2` 120 Ω/MB |
| Vendor description | *"built-in ceramic antenna"* |

Board-level claims this chain supports: tracking **−162 dBm**, acquisition −160 dBm, cold
start −148 dBm, cold TTFF 23 s / hot 1 s, accuracy < 1.5 m CEP50.

### [M5Stack Cap LoRa868 (U201)](../../../devices/m5stack/cap-lora868/README.md)

Vendor description is identical (*"built-in ceramic antenna"*) and the GNSS specification
table matches exactly, so the same antenna class is almost certainly fitted. **Not
confirmed** — the U201 schematic was not fetched.

## 4. Gaps

| # | Gap |
|---|---|
| 1 | **Manufacturer and datasheet unknown.** Gain, efficiency, axial ratio, required ground-plane size: all unknown |
| 2 | The hyphenless `ANT181804` reading is `inferred` |
| 3 | Ground-plane dimensions and keepout on the Cap PCB are unknown (no layout files) |
| 4 | No measurement of GNSS performance on either Cap by anyone |
| 5 | Whether LoRa TX at +22 dBm desensitises this front end has never been tested |

## 5. Related components

- [`components/analog-devices/max2659`](../../analog-devices/max2659/README.md) — the LNA at its feed
- [`components/zhongkewei/atgm336h-6n`](../../zhongkewei/atgm336h-6n/README.md) — the receiver it serves
- [`components/generic/ceramic-antenna`](../ceramic-antenna/README.md) — **a different part class** (2.4 GHz chip antennas), linked to prevent confusion

## 6. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| GA-1 | Cap LoRa-1262 schematic V1.1 | primary | [`devices/m5stack/cap-lora-1262/artifacts/schematic/`](../../../devices/m5stack/cap-lora-1262/artifacts/schematic/) | 2026-09-04 | `J1` comment, `L1` 6.8 nH, the LNA chain |
| GA-2 | Cap LoRa-1262 documentation | primary | `https://docs.m5stack.com/en/cap/Cap_LoRa-1262` | 2026-09-04 | *"built-in ceramic antenna"*; the sensitivity claims the chain supports |
