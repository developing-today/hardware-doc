# ZhongKeWei ATGM336H-6N

- **Category:** **GNSS receiver module** — a carrier for an **AT6668** multi-mode
  satellite-navigation chipset, presented as an 18-pad UART/I²C module
- **Scope:** module level. The chipset's protocol, constellations and configuration commands
  belong to [`components/zhongkewei/at6668`](../at6668/README.md)
- **Retrieved:** 2026-09-04

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **ZhongKeWei / 中科微电子** (Zhongke Microelectronics), Chengdu | datasheet title, `inferred` for the English rendering |
| Part | **`ATGM336H-6N`** — the `-6N` suffix denotes the variant/firmware grade | M5Stack specification tables |
| Chipset inside | **`AT6668`** — M5Stack writes the pairing as **`ATGM336H-6N@AT6668`** | M5Stack specification tables, three product pages |
| Pads | **18** | schematic symbol |
| Interfaces | **UART** (primary), **I²C**, `1PPS`, `ON/OFF`, `NRST`, `VBAT` backup | schematic symbol |
| Protocol | **NMEA 0183 4.1** on the wire; **CASIC binary** for configuration | M5Stack |

### Pinout as drawn on M5Stack's symbol

| Pin | Name | Pin | Name |
|---:|---|---:|---|
| 1 | `GND` | 10 | `GND` |
| 2 | `TXD1` | 11 | `ANT` |
| 3 | `RXD1` | 12 | `GND` |
| 4 | `1PPS` | 13 | `NC` |
| 5 | `ON/OFF` | 14 | `VCC_RF` |
| 6 | `VBAT` | 15 | `NC` |
| 7 | `NC` | 16 | `SDA` |
| 8 | `VCC` | 17 | `SCL` |
| 9 | `NRST` | 18 | `NC` |

Note the **separate `VCC` and `VCC_RF` supplies** (pins 8 and 14) — boards commonly feed
them through separate ferrites, and `VCC_RF` is what biases an external active antenna or
LNA.

## 2. Capability, as M5Stack publishes it

| Item | Value |
|---|---|
| Constellations | **GPS · QZSS · BDS (BD2 + BD3) · GALILEO · GLONASS** |
| Bands | BDS **B1I + B1C** · GPS/QZSS/SBAS **L1** · GALILEO **E1** · GLONASS **R1** |
| Channels | 50 |
| Accuracy | **< 1.5 m CEP50** |
| Update rate | up to **10 Hz** |
| Sensitivity | tracking **−162 dBm** · acquisition −160 dBm · cold start −148 dBm |
| TTFF | cold **23 s** · hot **1 s** |
| Default UART on M5Stack boards | **115200 bps 8N1** |

⚠ **"Multi-frequency" here means multiple *constellations'* L1-neighbourhood signals
(1.56–1.61 GHz), not L1+L5 dual-frequency.** One 18 mm patch and one LNA cover all of them.
Do not read RTK-grade capability into the specification table.

⚠ The **−162 dBm tracking** figure quoted by M5Stack is for a board carrying an external
**MAX2659 LNA**, not for the bare module. Attributing it to the module alone would be wrong.

## 3. Software

| Library | Notes |
|---|---|
| **`m5stack/TinyGPSPlus`** — class **`MultipleSatellite`** | M5Stack's fork, head `254a10041ac38d17d98dab24c0ae4d2a8d19a677` (2025-01-02). ⚠ The vendor documentation says explicitly: *"needs to be downloaded from the GitHub version adapted for M5Stack devices… **Do not download it from the Arduino Library Manager**"*. **No LICENSE file is present in the fork**; upstream TinyGPSPlus is LGPL-2.1 — flagged, unresolved |
| Meshtastic | built-in GPS subsystem; `GPS_BAUDRATE 115200` |
| Any NMEA parser | sufficient for position/time; **not** sufficient for configuration |

`MultipleSatellite` adds M5Stack-specific calls — `setSystemBootMode(BOOT_FACTORY_START)`,
`setSatelliteMode(...)`, `getGNSSVersion()` — which are **CASIC binary commands**, not NMEA.
See the [AT6668 record](../at6668/README.md).

## 4. Used By

### [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) — designator `M2`, symbol comment `GP-02`

| Function | Module pin | Board / host |
|---|---:|---|
| UART TX (module → host RX) | 2 | Cap-Bus 1 → host **G15** |
| UART RX (module ← host TX) | 3 | Cap-Bus 2 → host **G13** |
| `VCC` | 8 | `+3.3V` via `FB3` 120 Ω/MB |
| `VCC_RF` | 14 | `+3.3V` via `FB2` 120 Ω/MB |
| `ANT` | 11 | ← `U1` **MAX2659** LNA `RFOUT` via `C5` 470 pF ← `J1` `ANT1818-04` patch |
| `VBAT` | 6 | `BT1` backup cell |
| `1PPS` (4), `ON/OFF` (5), `NRST` (9), `SDA` (16), `SCL` (17) | — | **not routed to the Cap-Bus** |

**So on this board it is a UART-only device with no host reset, no hardware standby and no
pulse-per-second.** Everything configurable must go over the serial link. Full detail:
[`devices/m5stack/cap-lora-1262/features/gnss.md`](../../../devices/m5stack/cap-lora-1262/features/gnss.md).

⚠ **The symbol comment reads `GP-02`, not `ATGM336H-6N`.** The specification table says
`ATGM336H-6N@AT6668`. Whether `GP-02` is an M5Stack internal library name, a second-source
designation, or something else is **unresolved**.

### [M5Stack Cap LoRa868 (U201)](../../../devices/m5stack/cap-lora868/README.md) — same part

Specification table gives the identical `ATGM336H-6N@AT6668` pairing and identical GNSS
figures. Pin map shows the same two Cap-Bus lines (`GPS_TX` → G15, `GPS_RX` → G13). The
U201 page additionally publishes **state-resolved current** — GPS on / LoRa standby
**29.24 mA** vs **GPS sleep / LoRa standby 3.16 mA** — i.e. **the GNSS dominates idle draw**
on that board.

### [M5Stack Cardputer Mesh Kit (K152)](../../../devices/m5stack/cardputer-mesh-kit/README.md)

Via the bundled Cap LoRa-1262.

### Elsewhere in M5Stack's catalogue

The datasheet mirror this repository holds is served from M5Stack's **`Unit-GPS v1.1`**
documentation path, so the same module is fitted to at least one Unit-series product. **Not
researched** by this pass.

## 5. Caveats

| # | Issue |
|---|---|
| 1 | **115200 bps is not the ATGM336H's usual factory default** (9600 is common elsewhere). Whether M5Stack's boards store the setting in the module or apply it from firmware is **unknown**. Autobaud should include 9600 |
| 2 | Sensitivity/accuracy figures quoted by M5Stack are **board-level with an external LNA** |
| 3 | `GP-02` unexplained (§4) |
| 4 | On both Caps the module's I²C, `1PPS`, `NRST` and `ON/OFF` are **not available to the host** |
| 5 | No independent measurement of TTFF, accuracy or sensitivity |

## 6. Related components

- [`components/zhongkewei/at6668`](../at6668/README.md) — the chipset inside, and the CASIC protocol
- [`components/analog-devices/max2659`](../../analog-devices/max2659/README.md) — the LNA in front of it on both Caps
- [`components/generic/gnss-ceramic-patch-antenna`](../../generic/gnss-ceramic-patch-antenna/README.md)

## 7. Local artifacts

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/atgm336h-6n-datasheet-m5stack-mirror.pdf`](artifacts/atgm336h-6n-datasheet-m5stack-mirror.pdf) | 752 259 | `7b1c10193709d7600e0234445a1c15603bf3443e14780ecde4818091ec2eda32` | `https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/Unit-GPS%20v1.1/ATGM336H-6N.pdf`, retrieved 2026-09-04, HTTP 200, `%PDF-1.7` |

⚠ **Vendor mirror, served from a *different product's* documentation path** (`Unit-GPS
v1.1`), linked from the Cap LoRa-1262 and Cardputer Mesh Kit pages. Revision unverified
against ZhongKeWei's own publication; the file carries no version in its name.
**The PDF was downloaded and type-verified but its contents were not read** by this pass —
every ATGM336H figure in this record comes from M5Stack's specification tables, not from the
datasheet. That is a gap a future pass should close.

Licence/redistribution: **unknown**. Disposition: **repository, unstaged** pending review.

## 8. Sources

| ID | Title | Publisher | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|
| A-1 | ATGM336H-6N datasheet | ZhongKeWei, mirrored by M5Stack | authorized mirror | see §7 | 2026-09-04 | The module (**held, not yet read**) |
| A-2 | Cap LoRa-1262 documentation | M5Stack | primary | `https://docs.m5stack.com/en/cap/Cap_LoRa-1262` | 2026-09-04 | `ATGM336H-6N@AT6668`, all §2 figures, the pin map |
| A-3 | Cap LoRa868 documentation | M5Stack | primary | `https://docs.m5stack.com/en/cap/Cap_LoRa868` | 2026-09-04 | Same module on the predecessor; **state-resolved current** |
| A-4 | Cardputer Mesh Kit documentation | M5Stack | primary | `https://docs.m5stack.com/en/core/Cardputer_Mesh_Kit` | 2026-09-04 | Third citation of the same pairing |
| A-5 | Cap LoRa-1262 schematic V1.1 | M5Stack | primary | [`devices/m5stack/cap-lora-1262/artifacts/schematic/`](../../../devices/m5stack/cap-lora-1262/artifacts/schematic/) | 2026-09-04 | The 18-pad pinout and what is/is not routed |
| A-6 | `m5stack/TinyGPSPlus` | M5Stack | primary | `https://github.com/m5stack/TinyGPSPlus` | 2026-09-04 | `MultipleSatellite`; head `254a1004…`; **no LICENSE file** |
