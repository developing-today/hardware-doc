# Pinouts and buses — Cap LoRa-1262 (U214)

Snapshot 2026-09-04. Schematic **V1.1 / 2025-10-29**. Nothing measured on hardware.

---

## 1. The Cap-Bus, and its two incompatible numbering conventions

The connector is a **2 × 7, 2.54 mm header** — `P1`, footprint `HDR-SMD_14P-P2.54` on
the Cap; **EXT 2.54-14P** on the Cardputer-Adv. **[SCH]**, **[DOC]**

**M5Stack numbers the same connector two different ways in two different documents.**
This is the single most confusing thing about the Cap-Bus and it has to be stated plainly:

| Document | Convention |
|---|---|
| Cap product pages (`Cap_LoRa-1262`, `Cap_CC1101`, `Cap_LoRa868`) | **LEFT column = 1…7 top-to-bottom, RIGHT column = 14…8 top-to-bottom** |
| Cardputer Mesh Kit page ("Cardputer-Adv EXT 2.54-14P") | **odd 1,3,5,…13 down the left, even 2,4,…14 down the right** — normal 2×N dual-row numbering |

They describe the same 14 contacts. The table below is keyed by the **Cap page numbering**,
because that is what is silkscreened in the Cap documentation, and gives the host GPIO
alongside — the host GPIO is the unambiguous identity.

| Cap pin | Cap net | Host GPIO (Cardputer-Adv) | Direction (Cap view) | Function |
|---:|---|---|---|---|
| 1 | `GPS_TX` | **G15** | O → host | GNSS module TX → **host RX** |
| 2 | `GPS_RX` | **G13** | I ← host | GNSS module RX ← **host TX** |
| 3 | `SCL` | **G9** | I/O | I²C clock (shared with host bus) |
| 4 | `SDA` | **G8** | I/O | I²C data (shared with host bus) |
| 5 | `5V_OUT` | — | P | 5 V from host |
| 6 | `GND` | — | P | Ground |
| 7 | `5V_IN` | — | P | 5 V into host |
| 8 | `LoRa_RST` | **G3** | I | SX1262 `NRST` |
| 9 | `LoRa_IRQ` | **G4** | O | SX1262 `DIO1` |
| 10 | `LoRa_BUSY` | **G6** | O | SX1262 `BUSY` |
| 11 | `LoRa_SCK` | **G40** | I | SPI clock |
| 12 | `LoRa_MOSI` | **G14** | I | SPI MOSI |
| 13 | `LoRa_MISO` | **G39** | O | SPI MISO |
| 14 | `LoRa_NSS` | **G5** | I | SPI chip select |

Every row is confirmed by **two independent primary sources**: the schematic's `P1` symbol
(which annotates each pin with both the Cap net name *and* the host GPIO) and M5Stack's
published pin-map graphic. **[SCH]** + **[DOC]**

### 1.1 ⚠ The GNSS UART direction is documented inconsistently — here is the resolution

The Cardputer Mesh Kit page labels EXT pin 12 (`G13`) **`UART_RX`** and pin 14 (`G15`)
**`UART_TX`**. Taken at face value that means the host receives on G13. **That reading is
wrong**, and three independent sources agree against it:

| Source | Says |
|---|---|
| Cap LoRa-1262 pin-map graphic **[DOC]** | `G13 → GPS-RX`, `G15 → GPS-TX` |
| Schematic `P1` **[SCH]** | pin 1 `GPS-TX` ← `G15`; pin 2 `GPS-RX` ← `G13` |
| M5Stack's own Arduino example **[SRC]** | `static const int RXPin = 15, TXPin = 13;` then `MultipleSatellite gps(Serial1, 115200, SERIAL_8N1, RXPin, TXPin)` |
| Meshtastic upstream `variant.h` **[SRC]** | `#define GPS_RX_PIN 15` / `#define GPS_TX_PIN 13` |

**Resolution: `G15` is the host's *receive* pin (it is fed by the GNSS module's TX);
`G13` is the host's *transmit* pin.** The `UART_RX` / `UART_TX` labels on the Mesh Kit
page are named from the *peripheral's* perspective, or are simply mislabelled.

This is not academic. A user on 2026-08-28 reported the GNSS finding zero satellites
across several firmwares and fixed it by *"setting manually the gpio rx and tx pins"* in
Meshtastic — [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1w0gv7y/). **[COM]**

### 1.2 An extraction artifact you will hit if you re-parse the schematic

In the text layer of `U214-Cap-LoRa1262_SCH_V1.1_20251029.pdf`, the GPIO labels for the
two I²C pins extract as **`GO`** and **`GI`**, never as `G8`/`G9` — there is no `G8` or `G9`
token anywhere in the file. The same substitution appears in the Cap CC1101 schematic.

The correct values are `G8` = SDA and `G9` = SCL, established independently by the vendor
pin-map graphic, the Mesh Kit EXT table, and M5Stack's Arduino example which opens
`m5::In_I2C.begin(I2C_NUM_0, 8, 9)`. **The `GO`/`GI` strings are an extraction artifact of
this PDF, not a hardware fact.** Recorded so the next agent does not "discover" a
nonexistent net. (Compare the PaperMono schematic's separate artifact where `_` renders
as `0` — different bug, same class of trap.)

---

## 2. On-board nets

```
                     ┌──────────── Cap LoRa-1262 (U214) ──────────────┐
 5V_IN/5V_OUT ──▶ U3 JW5712 buck ──▶ VDD_3V3 (0–0.6 A) ──┬──────────┐ │
 (P1.5 / P1.7)      ENB ◀── R1 10k pull-up (always on)   │          │ │
                                                          │          │ │
 G40 SCK  ─────────────────────────────────┐              │          │ │
 G14 MOSI ─────────────────────────────────┤              ▼          ▼ │
 G39 MISO ◀────────────────────────────────┤   M1 Stamp LoRa-1262 Mini │
 G5  NSS  ─────────────────────────────────┤   (SX1262 inside)         │
 G6  BUSY ◀────────────────────────────────┤    pin 10 SW ◀── U2.P0    │
 G4  IRQ (DIO1) ◀──────────────────────────┤    pin 12 ANT ──▶ E4 SMA  │
 G3  NRST ─────────────────────────────────┘                           │
                                                                        │
 G8 SDA ──┬──▶ U2 PI4IOE5V6408 @ 0x43 ── P0 ──▶ LoRa antenna switch     │
 G9 SCL ──┤                                                             │
          └──▶ J2 HY2.0-4P Grove (pass-through, R3 10k pull-up)         │
                                                                        │
 G15 ◀── GPS_TX ── M2 ATGM336H-6N ── ANT ◀── U1 MAX2659 LNA ◀── J1 patch │
 G13 ──▶ GPS_RX ──┘        VBAT ◀── BT1 backup cell                     │
                     └──────────────────────────────────────────────────┘
```

## 3. `M1` — `Stamp LoRa-1262 Mini`, all 13 pins

Read directly from the `M1` symbol. **[SCH]**

| Pin | Name | Direction | Net on this board |
|---:|---|---|---|
| 1 | `GND` | P | `GND` |
| 2 | `NRST` | I | `RST` → P1.8 → host **G3** |
| 3 | `BUSY` | O | `BUSY` → P1.10 → host **G6** |
| 4 | `IRQ` | O | `IRQ` → P1.9 → host **G4** (SX1262 `DIO1`) |
| 5 | `3V3` | P | `VDD_3V3` from `U3` |
| 6 | `CLK` | I | `SCK` → P1.11 → host **G40** |
| 7 | `MOSI` | I | `MOSI` → P1.12 → host **G14** |
| 8 | `MISO` | O | `MISO` → P1.13 → host **G39** |
| 9 | `NSS` | I | `NSS` → P1.14 → host **G5** |
| 10 | **`SW`** | I | **RF/antenna switch control** ← `PI4IOE5V6408` **P0** |
| 11 | **`GND`** | P | RF ground |
| 12 | **`ANT`** | RF | → `E4` antenna connector |
| 13 | **`GND`** | P | RF ground |

> ### This resolves an open question in the PaperMono documentation
> [`components/m5stack/stamp-lora-1262` §2.1](../../../components/m5stack/stamp-lora-1262/README.md)
> records module pins **11, 12 and 13 as "unlabelled, not proven no-connect"**, because the
> PaperMono schematic symbol prints no names there. The Cap LoRa-1262 symbol for the same
> 13-pin module **does** print them: **11 = GND, 12 = ANT, 13 = GND** — a
> ground-signal-ground coplanar RF launch, exactly what one would expect at a module's
> antenna edge. Pin 10, which PaperMono calls `SX_ANT_SW`, is simply `SW` here.
>
> Confidence: **high but not certain**. Both symbols have 13 pins in the same order with
> the same first-nine names, and both are called `Stamp LoRa-1262 Mini`/`Stamp-LoRa-1262-mini`.
> What has *not* been done is a photograph of either footprint. Treated as
> `inferred (strong)`, and recorded in the component record rather than asserted as fact.

## 4. `M2` — `ATGM336H-6N` GNSS module, all 18 pins

**[SCH]**

| Pin | Name | Net |
|---:|---|---|
| 1 | `GND` | `GND` |
| 2 | `TXD1` | `GPS-TX` → P1.1 → host **G15** |
| 3 | `RXD1` | `GPS-RX` → P1.2 → host **G13** |
| 4 | `1PPS` | **not routed to the Cap-Bus** — see gap **G5** |
| 5 | `ON/OFF` | tied off on-board; not host-controllable |
| 6 | `VBAT` | `BT1` backup cell |
| 7 | `NC` | — |
| 8 | `VCC` | `+3.3V` via `FB3` (120 Ω/MB) |
| 9 | `NRST` | tied off on-board; **not host-controllable** |
| 10 | `GND` | `GND` |
| 11 | `ANT` | ← `U1` MAX2659 `RFOUT` |
| 12 | `GND` | `GND` |
| 13 | `NC` | — |
| 14 | `VCC_RF` | `+3.3V` via `FB2` (120 Ω/MB) — feeds the LNA bias |
| 15 | `NC` | — |
| 16 | `SDA` | **not routed to the Cap-Bus** |
| 17 | `SCL` | **not routed to the Cap-Bus** |
| 18 | `NC` | — |

**Consequence:** the GNSS is a **UART-only device on this board.** Its I²C port, its
`1PPS` output and its hardware reset are all unavailable to the host. Anything you want
to do to it — cold/warm/hot start selection, constellation selection, update rate — must
go over the serial link as CASIC binary or NMEA proprietary sentences. See
[`features/gnss.md`](features/gnss.md).

## 5. `U1` — MAX2659 GNSS LNA

**[SCH]**

| Pin | Name | Net |
|---:|---|---|
| 1, 2 | `GND` | `GND` |
| 3 | `RFIN` | ← `J1` ceramic patch antenna, via `L1` 6.8 nH |
| 4 | `VCC` | `+3.3V` |
| 5 | `SHDN` | tied — **no host shutdown control** |
| 6 | `RFOUT` | → `M2` pin 11 `ANT`, via `C5` 470 pF |

`C6` 100 nF and `C7` 33 nF decouple the LNA supply.

## 6. `U2` — PI4IOE5V6408 I/O expander

I²C address **0x43** (7-bit), on the host's main I²C bus (`G8`/`G9`). **[SCH]** for the
part and pinout, **[DOC]** + **[SRC]** for the address.

| Pin | Name | Net |
|---:|---|---|
| 1 | `INT` | not routed to the host |
| 2 | `VDD` | `VDD_3V3` |
| 3–8 | `P7 … P2` | **unused** on this board |
| 9 | `ADDR` | strapped → **0x43** |
| 10 | `RESET` | tied off |
| 11 | `P1` | **unused** |
| **12** | **`P0`** | **`SX_ANT_SW`** → `M1` pin 10 |
| 13 | `SCL` | `SCL` → host **G9** |
| 14 | `SDA` | `SDA` → host **G8** |
| 15 | `VDD_Bus` | bus-voltage reference |
| 16 | `GND` | `GND` |

Depopulated: `R5/NC`, `R6/NC`, `R7/NC` (10 kΩ each), `C13/NC`, `C14/NC` (100 nF each).

**Seven of the eight expander outputs are unused.** If you are designing a derivative
board, `P1`–`P7` are free I²C-reachable GPIO already on the bus.

## 7. Power

| Rail | Source | Notes |
|---|---|---|
| `+5V` | Cap-Bus pins 5/7 from the host | `C1` 1 nF, `C2`–`C4` 22 µF bulk |
| `VDD_3V3` | `U3` JW5712 buck, `L2` = 2.2 µH `WPN201610U2R2MT` | sheet prints `IOUT: 0~0.6A`; `C15` 22 µF, `C16`/`C17` 100 nF, `C12` 470 µF |
| Enable | `R1` 10 kΩ pull-up on `ENB` | **no host enable line** — the Cap is live whenever the host provides 5 V. `inferred` from adjacency; the ENB net was not traced end-to-end |

Contrast with the [Cap CC1101](../cap-cc1101/pinouts-and-buses.md), where the *same*
Cap-Bus pin 8 is `POWER_EN` and gates the whole board's regulator. **The two Caps use pin 8
for entirely different purposes.** Anything that auto-detects a Cap must not assume pin 8
semantics.

## 8. Host-side resource cost

Fitting this Cap consumes, on the Cardputer-Adv:

| Resource | Pins | Shared? |
|---|---|---|
| SPI (SCK/MOSI/MISO) | G40, G14, G39 | **Yes — shared with the microSD slot** (`SDCARD_CS` = G12). Chip-select arbitration required |
| SPI chip select | G5 | LoRa only |
| LoRa control | G3 (RST), G4 (DIO1), G6 (BUSY) | LoRa only |
| UART1 | G15 (RX), G13 (TX) | GNSS only |
| I²C | G8, G9 | **Yes — shared with keyboard TCA8418, IMU BMI270, audio ES8311 and the Grove port** |

That is **nine host GPIO plus a share of two buses**. It is exactly why no Cap fits the
original Cardputer: u/IceSubstantial5572, 2025-09-04 — *"No, not enough gpio pins"*
([r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1n8d8j2/)). The Cardputer-Adv
freed them by moving the keyboard from a GPIO matrix onto an **I²C TCA8418** controller
(u/MrBoomer1951, 2025-09-09, [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1nch377/)). **[COM]**

---

Evidence key as in [`README.md`](README.md). Sources listed in [`sources.md`](sources.md).

---

# 2026-09-07 — Cap-Bus pinout confirmed from the schematic

Appended beneath the existing tables; **nothing above is altered.** Full trace with coordinates:
[`schematic-netlist.md`](schematic-netlist.md). Method:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).

## The connector is `HDR-SMD_14P-P2.54` — 14 pins, 2.54 mm, SMD

Each bus net carries **two** labels on the same wire: a host-GPIO alias and a functional alias.
A 300 dpi render was needed to establish that both are net labels rather than one label plus an
annotation.

| Pin | Symbol pin name | Host GPIO | Functional alias (U214) | Token |
|---|---|---|---|---|
| 1 | `GPS-TX` | `G15` | — | `PIP101` @ 705.00, 506.37 |
| 2 | `GPS-RX` | `G13` | — | `PIP102` @ 705.00, 498.91 |
| 3 | `SCL` | `GI` = **GPIO1** | `SCL` | `PIP103` @ 705.00, 491.37 |
| 4 | `SDA` | `GO` = **GPIO2** | `SDA` | `PIP104` @ 705.00, 484.37 |
| 5 | `5VOUT` | — | `+5VOUT` | `PIP105` @ 705.00, 477.37 |
| 6 | `GND` | — | `GND` | `PIP106` @ 705.00, 470.37 |
| 7 | `5VIN` | — | `+5VIN` | `PIP107` @ 705.00, 462.91 |
| 8 | `RESET` | `G3` | **`RST`** → SX1262 `NRST` | `PIP108` @ 633.00, 462.91 |
| 9 | `INT` | `G4` | `IRQ` | `PIP109` @ 633.00, 470.37 |
| 10 | `BUSY` | `G6` | `BUSY` | `PIP1010` @ 633.00, 477.37 |
| 11 | `SCK` | `G40` | `SCK` | `PIP1011` @ 633.00, 484.37 |
| 12 | `MOSI` | `G14` | `MOSI` | `PIP1012` @ 633.00, 491.37 |
| 13 | `MISO` | `G39` | `MISO` | `PIP1013` @ 633.00, 498.91 |
| 14 | `CS` | `G5` | `NSS` | `PIP1014` @ 633.00, 506.37 |

`GI` = GPIO1 and `GO` = GPIO2 is fixed by the Cardputer ADV sheet, where the same two net names
land on module pins printed `G1` and `G2`. **Here the sheet corroborates it directly**: pin 3's
symbol name is `SCL` and it carries `GI`; pin 4's is `SDA` and it carries `GO`. That matches
M5Unified's `EX SCL = GPIO_NUM_1`, `EX SDA = GPIO_NUM_2`.

## The reported "pin 8 conflict" with the Cap CC1101 — **explained, not a bus conflict**

The bus itself is **identical** on `U214` and `U219`: same connector part, same pin numbering,
same symbol pin names, same host-GPIO aliases. What differs is the *functional* alias, because
each daughterboard defines what it does with the host line:

| Pin | Host GPIO | U214 Cap LoRa-1262 | U219 Cap CC1101 |
|---|---|---|---|
| **8** | **`G3`** | **`RST`** — SX1262 `NRST` (`M1` pin 2) | **`POWER_EN`** — enables the board's own `JW5712` buck |
| 9 | `G4` | `IRQ` | `NFC_IRQ` |
| 10 | `G6` | `BUSY` | `NFC_CS` |
| 11 | `G40` | `SCK` | `SPI_SCLK` |
| 12 | `G14` | `MOSI` | `SPI_MOSI` |
| 13 | `G39` | `MISO` | `SPI_MISO` |
| 14 | `G5` | `NSS` | `CC1101_CS` |
| 1 | `G15` | (GNSS TX, `M2` `GP-02`) | `CC1101_G0` |
| 2 | `G13` | (GNSS RX, `M2` `GP-02`) | `CC1101_RF_SW0` |

**Firmware consequence:** driving `G3` low on a Cap CC1101 **removes power from the radio**;
on a Cap LoRa-1262 it merely asserts the radio's reset. Code must not be ported between the two
boards without changing the meaning of that pin.

## On-board power — `U3` is a `JW5712`, permanently enabled

Value string `JW5712` @ (140, 186.3); annotation `IOUT: 0~0.6A` @ (155–175, 92.9).

| Ball | Name | Net |
|---|---|---|
| `A1` | `SW` | `L2` `WPN201610U2R2MT` 2.2 µH → `VDD_3V3` |
| `A2` | `VIN` | `+5V` / `+5VOUT` |
| `B1` | `EN` | **`R1` 10 kΩ pull-up to `+5V` — no host control** |
| `B2` | `GND` | `GND` |
| `C1`/`D1`/`D2` | `VSEL1`/`VSEL2`/`VSEL3` | output-voltage straps |
| `C2` | `VOS` | `VDD_3V3` remote sense |

See [`components/joulwatt/jw5712`](../../../components/joulwatt/jw5712/README.md).

## Other parts on the sheet

`U1` `MAX2659` GNSS LNA (`L1` 6.8 nH ±5 %, `C5` 470 pF, `J1` `ANT181804`) ·
`U2` `PI4IOE5V6408ZTAEX` I²C GPIO expander (`P0`…`P7`, `ADDR` via `R7/NC` 10 kΩ) ·
`M1` `Stamp LoRa-1262 Mini` (13 pins; `NRST`, `BUSY`, `IRQ`, `3V3`, `CLK`, `MOSI`, `MISO`, `NSS`,
`ANT`) · `M2` `GP-02` GNSS module · `E4` `SMA-KE` LoRa antenna · `J2` `GROVE 4P` ·
`BT1` battery with `FB3` 120 Ω/MB.
