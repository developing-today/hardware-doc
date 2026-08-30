# Battery charger and power path (unidentified)

- **Category:** battery charging and power-path management function
- **Reference designator on this board:** **none.** No charger block appears in the five published schematic sheets
- **Owning MCU:** **none.** No charge-status, charge-enable or power-path signal reaches either processor
- **Research status:** ⚠ **This is a documented absence, not a partially-researched part.** The function is claimed by the vendor and is evidently present in hardware, but the published schematic does not contain it. This page records exactly what can and cannot be inferred, and how to identify it
- **Retrieved:** 2026-08-21; schematic re-searched sheet-by-sheet and inference boundaries tightened 2026-08-23; **designator census added and the ETA/SGM leads in §3 explicitly tested and found absent 2026-08-24** (§1.4)

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning always given

---

## 1. The shape of the gap

### 1.1 What the vendor claims

Waveshare's product material states that the board charges a battery, and sells the board with an optional 3.7 V `102035` LiPo **[WEB]**. Product imagery shows a battery connector on the PCB.

### 1.2 What the schematic contains

**Nothing.** All five sheets were searched **[SCH]**:

| Sheet | Contents | Charger present? |
|---|---|---|
| `1_LCD&POWER.png` | `CN1` header, the **TLV62569 3V3 buck**, both knob switches, the LCD connector `U5`, the backlight circuit | **No** |
| `2_ESP32S3-R8.png` | ESP32-S3, its crystal, `ANT1`, the SPI flash, the full net-alias table | No |
| `3_ESP32-CHIP.png` | ESP32-U4WDH, its crystal, `ANT2`, the USB-UART bridge `U10` | No |
| `4_OTHER.png` | `BATT_ADC` divider, the PDM microphone, the microSD socket | **No** |
| `5_DAC.png` | PCM5100A, DRV2605L, the SGM2036 LDO, the CH445P mux | No |

Despite the sheet named "LCD&POWER", the only power circuitry drawn is the 3.3 V buck. **The `5V` net simply appears, as a labelled net, with no source.**

### 1.3 What is therefore unknown

Everything about charging and power-path, specifically:

| Unknown | Consequence of not knowing |
|---|---|
| **Charger IC part number** | No datasheet, no register map, no known behaviour |
| **Charge current** | Charge time unknown; whether the cell is charged within its C-rate unknown |
| **Termination voltage** (4.2 V? 4.35 V?) | **You cannot safely substitute a cell of a different chemistry.** See [generic/lipo-102035 §6](../lipo-102035/README.md#6-charging--what-is-and-is-not-known) |
| **Whether the charge current is programmable** | If it is set by an `ISET` resistor, it is fixed at manufacture |
| **NTC / temperature qualification** | Whether charging is inhibited when hot or cold. Most low-cost single-cell chargers omit it |
| **Pre-charge / trickle behaviour** | Whether a deeply discharged cell recovers |
| **Safety timer** | Whether a fault condition eventually terminates |
| **Power-path topology** | Whether the load runs from the charger or from the cell while charging, and whether the cell can be charged and the board used simultaneously |
| **Whether there is a boost converter** | A 3.7 V cell cannot directly produce the board's 5 V net. **Something must boost it, and that something is also not drawn.** §2.1 |
| **Charge-status output** | **Confirmed absent from both MCUs** — see §3. This one *is* established |
| **Over-voltage / over-current input protection** | Behaviour with a non-compliant USB supply is unknown |
| **Reverse-current protection** | Whether the cell can back-feed a disconnected USB port |

### 1.4 Designator census, and the ETA/SGM leads tested directly — 2026-08-24

A later pass re-read all five sheets as tiled crops upscaled 6–14×, specifically to test two named suspicions: that **`U17` is an ETA9740** power-path IC and that **`U11` is an SGM40561** charger. **Both fail at the first step: neither designator exists in the published schematic.**

Reference designators actually present across the five sheets **[SCH]**:

| Designator | Part | Sheet |
|---|---|---|
| `U2` | ESP32-S3(R8) | 2 |
| `U3` | W25Q128JVPIQ | 2 |
| `U5` | LCD/touch FPC connector | 1 |
| `U10` | unmarked USB-UART bridge (identified CH340X) | 3 |
| `U12` | PCM5100APWR | 5 |
| `U13` | DRV2605LDGSR | 5 |
| `U14` | ESP32-U4WDH | 3 |
| `U18` | CH445P | 5 |
| `U19` | TLV62569DBVT | 1 |
| `U20` | SGM2036-3.3YN5G/TR | 5 |

**Absent entirely: `U1`, `U4`, `U6`, `U7`, `U8`, `U9`, `U11`, `U15`, `U16`, `U17`.** Ten gaps in a twenty-designator sequence — itself corroborating §2.4's reading that a sheet is missing rather than that the parts do not exist.

**Where the two names came from.** Almost certainly from **§3 of this very page**, which is an explicitly-labelled checklist of families to compare a physical top marking against, not a reading of anything. `ETA9740` appears there by name. `SGM40561` is one character from `SGM40567`, a charger that *is* documented in this tree — [`components/sgmicro/sgm40567`](../../sgmicro/sgm40567/README.md) — but which belongs to **a different board** (a Seeed XIAO ESP32S3 Sense), where it was read from an actual KiCad netlist.

This is exactly the failure mode §3 warns about, and it happened anyway. **The warning at the end of §3 is therefore restated here: no component record has been created for `ETA9740` or `SGM40561`, and none should be, until someone reads a top marking off a physical board.**

What the pass *did* confirm, by census rather than by block inspection: no charger, no power-path IC, no battery connector, no USB Type-C receptacle, and **no source for the `5V` net**. The `5V` net is consumed by `U19` (sheet 1), by `L8`/`U20` (sheet 5), by the `R62`/`R63` divider (sheet 4) and by `CN1` pin 1 (sheet 1), and produced by nothing. §2.1's experiment remains the highest-value next step.

## 2. What *can* be inferred from the board

Rigorously, these are the only inferences the published material supports.

### 2.1 There must be a boost converter, and it is not drawn

The board's main rail is **`5V`** **[SCH]**. It feeds:

- The `TLV62569DBVT` buck's `VIN` and `EN` **[SCH sheet 1]**
- The `SGM2036-3.3` LDO's input, via ferrite `L8` **[SCH sheet 5]**
- The `BATT_ADC` divider `R62`/`R63` **[SCH sheet 4]**
- `CN1` pin 1 **[SCH sheet 1]**

A single LiPo cell runs from about 3.0 V (empty) to 4.2 V (full). **It cannot produce 5 V.** And the TLV62569's UVLO is 2.3–2.45 V **[DOC]**, so the buck would keep running from a raw cell — but the LDO needs ≥3.55 V at load and the whole design is specified around a 5 V input.

**Therefore [INF]: either a boost converter exists between the cell and the `5V` net, or the `5V` net is not actually 5 V when running on battery.** Both are possible; neither is documented. This is a genuinely significant hole, because it determines what `BATT_ADC` reads on battery power (see [lipo-102035 §4](../lipo-102035/README.md#4--batt_adc-does-not-measure-the-battery)).

The two most likely arrangements **[INF]**:

| Arrangement | Implication for `BATT_ADC` | Implication for runtime |
|---|---|---|
| **Charger + boost to a regulated 5 V** | Reads ~5.0 V always; **useless as a fuel gauge** | Boost efficiency (~85–90%) multiplies into every runtime figure |
| **Charger + ideal-diode OR, `5V` net is really `VSYS`** and sags to cell voltage on battery | **Tracks the cell** and could be calibrated into a state-of-charge estimate | Better efficiency; but the LDO would drop out below ~3.55 V |

**Distinguishing these takes one measurement:** run the board on battery only and measure the `5V` net (available on `CN1` pin 1). If it reads ~5.0 V, it is boosted. If it tracks the cell, it is a `VSYS` node. **This is the single highest-value experiment on this page.**

### 2.2 There is no software control or observation of charging

Established, not inferred. Every GPIO on both MCUs is accounted for in [pinouts-and-buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md), and **none carries a `CHG`, `STAT`, `PG`, `CE`, `ISET` or `PROCHOT` signal** **[SCH]**.

The ESP32-U4WDH in particular has **no spare board-accessible GPIOs at all** — its eleven signals are fully enumerated. The ESP32-S3's unlisted pins are not claimed as free.

So: **charging is entirely autonomous. Firmware cannot start it, stop it, observe it or report on it.** Any charging indication in a UI would have to be inferred from a rail voltage whose meaning is itself unresolved (§2.1).

### 2.3 The charge indication is probably an LED

**[INF]** Almost every small charger IC drives a status LED, and Waveshare boards conventionally have one. Nothing in the schematic shows one, but the schematic also does not show the charger. If a charge LED exists on the physical board, it is being driven by the missing block. **Look for it during identification (§4).**

### 2.4 What the absence probably means

**[INF]** The most economical explanation is that **Waveshare published an incomplete schematic** — five sheets covering the digital design and omitting a power/charging sheet — rather than that the function is implemented by some exotic means. Supporting points:

- The sheets are numbered 1–5 and are internally consistent; nothing suggests a missing sheet was renumbered
- But sheet 1 is titled "LCD&POWER" and contains only *one* power block, which is a thin interpretation of "POWER"
- The `5V` net having no source is exactly the signature of a cross-sheet reference to a sheet that was not published

This is worth stating plainly because it changes the research strategy: **the answer is very unlikely to be found by re-reading the published files. It requires either a fuller schematic release from Waveshare, or physical inspection.**

## 3. What Waveshare typically fits — as a *lead*, not a conclusion

Explicitly **[INF]**, and explicitly not to be treated as established. The purpose of this section is to give someone with the board in hand a short list to check the top marking against, not to name a part.

Waveshare's small ESP32 boards commonly use single-cell linear chargers in SOT-23-5/6 or DFN packages, most often from these families:

| Family | Typical marking | Notes |
|---|---|---|
| **TP4054 / TP4056** | `4054`, `4056`, or a two-letter code | Extremely common in Chinese designs. TP4056 is SOP-8; TP4054 is SOT-23-5 |
| **MCP73831** | `DFAB`-style two/three-character code | Microchip, SOT-23-5, `ISET`-programmed |
| **LTH7 / LTC4054 clones** | `LTH7`, `LN4054` | |
| **ETA family** (ETA6003, ETA9740, ETA6096) | `ETAxxxx` or a house code | ETA parts often integrate **charger + boost in one package**, which would neatly explain both missing functions at once — see §2.1 |
| **IP5306 / IP5305** | `IP5306` | Integrated charger + boost + power path + button + LED gauge. Very common in power-bank-style designs |
| **SGM41511 / SGMicro chargers** | SGMicro house code | The board already uses SGMicro for the audio LDO, so a second SGMicro part is plausible |

**The ETA and IP5xxx rows are the interesting ones** **[INF]**, because a single IC providing charger + boost + power path would explain why *two* functions are absent from the schematic rather than one. A board with a `5V` net and a LiPo connector and no visible boost is the classic signature of an integrated charge-and-boost part.

**Do not write any of these into documentation as the fitted part.** They are a checklist for someone reading a top marking.

## 4. How to identify it

In increasing order of effort.

### 4.1 Photograph the board and read the top markings

The cheapest and most decisive step. Look specifically for:

- An IC near the battery connector
- An IC near the USB-C receptacle
- **An inductor.** A boost converter needs one. The board has three known inductors — `L4` (2.2 µH, the buck), plus the tiny 2 nH RF chokes `L1`/`L2`/`L5`/`L6` and the ferrite `L8`. **Any inductor in the 1–10 µH range that is not `L4` is almost certainly a boost inductor**, and the IC next to it is your target
- A status LED near the USB or battery area

Small-package chargers use two- or three-character house codes rather than the full part number. Cross-reference against an SMD-code database, and against §3.

### 4.2 Measure the `5V` net on battery power

Described in §2.1. One meter, one measurement, and it resolves the boost-versus-`VSYS` question, which is the most consequential unknown here.

### 4.3 Measure the charge current

Put a current meter in series with the battery (or a shunt and a scope) and observe:

- **Constant-current phase magnitude** → the programmed charge current
- **The voltage at which it tapers** → the termination voltage (4.2 V vs 4.35 V). **This is the safety-critical number**
- **The termination current** → typically 10% of the CC value
- **Whether there is a pre-charge phase** for a deeply discharged cell
- **Whether charging continues indefinitely** or a safety timer terminates it

### 4.4 Test temperature qualification

If §4.1 finds an NTC pin or an NTC on the battery connector, the charger qualifies by temperature. If not, **it does not**, and you must not charge outside the cell's rated range. Confirm by continuity-checking the battery connector for a third pin.

### 4.5 Ask Waveshare

The published archive is five raster PNGs with no BOM, no Gerbers and no mechanical CAD **[SCH]**. A complete design package would close this and several other gaps at once. This is worth a support request; it is the kind of thing vendors sometimes provide.

## 5. Practical guidance until it is identified

1. **Do not substitute a cell with a different termination voltage.** §1.3. Use a standard 4.2 V cell.
2. **Use a cell with an integrated protection circuit (PCM).** The board's over-discharge behaviour is unknown, so the cell's own protection is the only guarantee.
3. **Do not charge unattended in an enclosed or hot space.** Temperature qualification is unknown (§4.4).
4. **Do not build a fuel gauge on `BATT_ADC`** until §4.2 is answered. See [lipo-102035 §4](../lipo-102035/README.md#4--batt_adc-does-not-measure-the-battery).
5. **Do not promise "charging status" in a UI.** No signal reaches either MCU (§2.2). If there is a charge LED, it is the only indication and it is not software-readable.
6. **Assume the charge current is modest.** Linear chargers in SOT-23 packages typically run at 100–500 mA and are thermally limited. **[INF]** For a cell of a few hundred mAh, expect charge times measured in hours, not minutes.
7. **Verify the battery connector's polarity before first use.** The connector family is itself disputed — see [lipo-102035 §3](../lipo-102035/README.md#3-connector--also-unresolved-and-this-one-is-dangerous). This is the highest physical risk on the board.

## 6. Open questions

Every item in §1.3, plus:

| Question | Priority | Method |
|---|---|---|
| **Is there a boost converter, or is `5V` really `VSYS`?** | **Highest** — determines fuel-gauging and runtime | §4.2, one meter reading |
| Charger IC identity | High | §4.1, a photograph |
| Termination voltage | **Highest for safety** | §4.3 |
| Charge current and time | Medium | §4.3 |
| NTC present? | High for safety | §4.4 |
| Is there a charge-status LED? | Low | §4.1 |
| Does a fuller schematic exist? | Would close everything | §4.5 |

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — function claimed by the vendor; **not present in the published schematic**

## Related pages

- [generic/lipo-102035](../lipo-102035/README.md) — the battery, its unresolved connector, and runtime estimation
- [texas-instruments/tlv62569dbvt](../../texas-instruments/tlv62569dbvt/README.md) — the buck that consumes the `5V` net, and the `BATT_ADC` divider
- [sgmicro/sgm2036-3.3](../../sgmicro/sgm2036-3.3/README.md) — the other `5V` consumer, and its 3.55 V dropout floor
- [generic/usb-c-interface](../usb-c-interface/README.md) — the other place the `5V` net is unresolved
- [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md) — board-wide tracking of this gap

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Board schematic archive — **all five sheets, searched; no charger block present** | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
| Schematic sheet 1 "LCD&POWER" — contains only the 3V3 buck; the `5V` net has **no source** | — | 2026-08-21 | `.../artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Schematic sheet 4 — the `BATT_ADC` divider, the only battery-adjacent circuitry published | — | 2026-08-21 | `.../artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/4_OTHER.png` |
| Waveshare product page — the charging claim and the battery option | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
| TLV62569 datasheet — the UVLO and `VIN` range used in §2.1 | https://www.ti.com/lit/gpn/TLV62569 | 2026-08-21 | `../../texas-instruments/tlv62569dbvt/artifacts/tlv62569-datasheet.pdf` |
| SGM2036 datasheet — the 3.55 V dropout floor used in §2.1 | https://www.sg-micro.com/product/SGM2036 | 2026-08-23 | `../../sgmicro/sgm2036-3.3/artifacts/sgm2036-datasheet.pdf` |
