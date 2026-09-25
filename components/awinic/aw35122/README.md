# Awinic AW35122 (AW35122FDR)

> Ultra-small **P-channel load switch** with controlled output slew rate, quick output discharge and an internal 7.1 MΩ enable pull-down, in a 1 mm × 1 mm × 0.55 mm four-ball package.
> Research snapshot **2026-09-01**. Fitted **at least four times** on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) as the switch element of the `L3B` power domain. **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Awinic `AW3512, AW35122` datasheet **V1.0**, July 2019 — local copy `artifacts/aw3512-aw35122-datasheet-en-v1.0.pdf` | `not-tested` |
| **[VP]** | Awinic product page for `AW35122FDR`, retrieved 2026-09-01 | `not-tested` |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | M5Stack source at a cited `file:line` | `executed-success` for the read |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Ordering part | **`AW35122FDR`** | **[SCH]**, **[VP]** |
| Manufacturer | **Shanghai Awinic Technology Co., Ltd.** | **[DS]** |
| Category | *"Single-Channel load switches"* — *"1.5 A Ultra-small Load Switch with Slew Rate Control"* | **[VP]** |
| Package | **FCDFN-4L, 1.00 × 1.00 × 0.55 mm** (balls A1, A2, B1, B2) | **[DS]**, **[VP]** |
| Datasheet | **`DS_AW35122_EN_V1.0`**, July 2019, 18 pp | **[DS]** cover |
| Lifecycle | Active | **[VP]** |

### 1.1 ⚠ `AW3512` vs `AW35122` — the difference is one resistor, and it matters

The datasheet covers both under one document **[DS Device Comparison Table]**:

| Part | Top mark | `EN` pull-down |
|---|---|---|
| **AW3512** | `SV` | **None.** The datasheet says explicitly: *"do not leave floating"* |
| **AW35122** | `UJ` | **Internal 7.1 MΩ pull-down** |

A board designed around the AW35122's internal pull-down that is later populated with an AW3512 has **four floating enable inputs**. The rails would come up indeterminate. The parts are otherwise identical and share a footprint, so this substitution is easy to make and hard to see.

On the PaperMono this is directly relevant: `U8`'s external enable pull-down `R25` is marked **`NC/1%`** — not fitted — because the AW35122's internal 7.1 MΩ is doing the job. **[SCH]** **[INF]**

---

## 2. Key limits **[DS Absolute Maximum Ratings, VP Parameters]**

| Parameter | Value |
|---|---|
| Input voltage `VIN` | **1.2 V – 5.5 V** (abs. max −0.3 to 6 V) |
| `EN`, `OUT` abs. max | −0.3 to 6 V |
| Max continuous switch current (V<sub>IN</sub> ≥ 2 V) | **1.5 A** |
| Max peak switch current (V<sub>IN</sub> ≥ 2.5 V) | 2 A |
| Enable logic | **Active high** |
| Output discharge | Yes (quick discharge on disable) |
| Slew-rate control | Yes — limits inrush at turn-on |
| Turn-on time t<sub>R</sub> | ≈165 µs **[VP]** |
| Reverse-current blocking | **No** |
| θ<sub>JA</sub> | 166 °C/W |
| Operating temperature | −40 to +85 °C |
| Max T<sub>J</sub> | 150 °C |
| Logic level | 1.8 V compatible **[VP]** |

**R<sub>DS(on)</sub> is strongly supply-dependent [DS]:**

| V<sub>IN</sub> | R<sub>DS(on)</sub> typ. |
|---|---:|
| 5.5 V | 52 mΩ |
| 4.2 V | 58 mΩ |
| **3.3 V** | **66 mΩ** |
| 2.5 V | 80 mΩ |
| 1.8 V | 110 mΩ |
| 1.2 V | 222 mΩ |

At the PaperMono's 3.3 V the switch drop is ≈66 mV per amp — negligible for the microphone and touch rails, but worth a thought on the microSD rail during a write burst. **[INF]**

---

## 3. Pinout **[DS Pin Definition]**

| Ball | Name | Function |
|---|---|---|
| **A1** | `OUT` | Switch output |
| **A2** | `IN` | Switch input and device supply |
| **B1** | `GND` | Ground |
| **B2** | `EN` | Control input, **active high**. On AW35122, internal 7.1 MΩ pull-down |

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).

The PaperMono's power architecture (sheet 1) defines five states — **L0 Shipping, L1 Standby, L2 DeepSleep, L3A CORE ACTIVE, L3B All ACTIVE** — and the `L3B` rails are the ones that exist only while the whole device is awake. **The AW35122 is the switch element of `L3B`**, and every instance is enabled from an [M5IOE1](../../m5stack/m5ioe1/README.md) GPIO rather than from the ESP32-S3. Sheet 1's legend annotates the `L3B Power Control` block with `AW35122` for both the PDM and TF branches. **[SCH]**

#### 4.1 Every instance found

Three instances carry the string `AW35122FDR` beside the designator in the schematic text layer; a fourth is a footprint- and pin-name-identical part on the NFC sub-board whose value string was not recovered.

| # | Ref | Sheet | Input | **Controlled rail** | **Enable net** | Enable source | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | **`U8`** | 2 | `3V3_L2` | **`TF_3V3_L3B`** — microSD card slot (`U20`, `AXE512127D`) | `PYB_TF_EN` | M5IOE1 **`PYG14`** (`U17` pin 3/18) → `M5IOE1_PIN_14`, enum value 13 | **[SCH]**; **[SRC]** `hal_tf_card.cpp:15` |
| 2 | **`U18`** | 4 | `3V3_L2` | **`TP_VDD`** — FT6336G touch controller on FPC `J4`, and the `AW39112DNR` (`U19`) bus translator's A-side supply and `OE` | `PYB_TP_EN` | M5IOE1 **`PYG13`** (`U17` pin 6/15) → `M5IOE1_PIN_13`, enum value 12 | **[SCH]**; **[SRC]** `app_sleep_wake.cpp:81` |
| 3 | **`U21`** | 4 | `3V3_L2` | **`PDM_VDD`** — LMD4737T261-AC02 PDM microphone (`U1`, sheet 5, via `J6`/`J1`) | `PYB_PDM_EN` | M5IOE1 **`PYG12`** (`U17` pin 5/16) → `M5IOE1_PIN_12`, enum value 11 | **[SCH]**; **[SRC]** `hal_mic.cpp:13`, `hal_board.cpp:30` |
| 4 | **`U1` (sheet 6)** | 6 | `3V3_L2` | **`VCC_3V3`** — the NFC sub-board rail feeding the ST25R3916 (`U2`, sheet 6) | **`PYB_RFID_RST`** (arriving on BTB `J1` pin 9) | not resolved on the main-board sheets | **[SCH]**; part number **[INF]** — see §4.2 |

Passive complement, from the schematic text layer **[SCH]**:

| Ref | Input cap | Output cap | EN pull-down |
|---|---|---|---|
| `U8` | — | `C21` 10 µF/10 V | `R25` **`NC/1%`** (relies on the internal 7.1 MΩ) |
| `U18` | `C66` 10 µF/10 V | `C68` 10 µF/10 V | — |
| `U21` | — | `C85` 10 µF/10 V | — |
| `U1` (sheet 6) | — | `C1` 10 µF | `R1` 0 Ω, `R2` `NC` |

#### 4.2 ⚠ Instance 4 is inferred, not confirmed

Sheet 6 (the NFC sub-board, a separate Altium document, `02 Paper Mono NFC.SchDoc`, rev V0.2, 2026-07-28) draws `U1` with pin names `IN` / `OUT` / `EN` / `GND` on balls A2 / A1 / B2 / B1 — **identical to the AW35122FDR pinout in §3** — but the value string is not present in the extracted text near that symbol. Every other four-ball load switch on this board is an AW35122FDR. That is suggestive, not conclusive. **`inferred`.** Reading sheet 6 graphically would settle it.

Note also that this instance's enable is `PYB_RFID_RST`, **not** `PYB_NFC_EN`. Sheet 4 carries the annotation *"PYB_NFC_EN is a spare GPIO pin"*, while M5Stack's firmware and documentation both describe M5IOE1 `PYG4` / `M5IOE1_PIN_4` as "NFC power enable" (`hal_board.cpp:29`). **This is a genuine conflict between the schematic and the vendor's software, and it is recorded here rather than resolved.** It belongs primarily in the device record; it is noted here because it determines which signal actually switches this instance.

#### 4.3 What this architecture buys, and what it costs

- **Rails that cost nothing in sleep.** Touch, microSD and the microphone all disappear in `L2 DeepSleep` without any leakage path, because a load switch has no quiescent draw worth naming when off.
- **Every one of them is behind an I²C transaction.** Turning the microphone on means talking to the M5IOE1 at `0x4F` first. There is no GPIO shortcut, and the 165 µs turn-on time is dwarfed by the bus transaction. **[INF]**
- **⚠ M5Unified already owns three of these four rails.** M5Stack's own warning: *"The pins associated with the e-paper display, touch controller, microSD, and PDM microphone are already used by M5Unified. Before modifying them, ensure that the corresponding peripheral has stopped, or the peripheral may stop working or require reinitialization."* Cutting `TP_VDD` under a running touch driver leaves the driver holding a handle to a dead device.
- **Not every `L3B` rail is a load switch.** `EPD_3V3_L3B` is produced by an [SSP7615-33DFR](../../generic/ssp7615-33dfr/README.md) LDO (`U5`, sheet 2) from `VBUS_L0`, not by an AW35122 from `3V3_L2`, and `BL_15V_L3B` comes from the [AW9967DNR](../aw9967/README.md) boost. Do not assume the whole domain is switched the same way.

### `devices/m5stack/dinmeter` and `devices/m5stack/dinmeter-v1.1`

→ [M5Stack DinMeter (K134)](../../../devices/m5stack/dinmeter/README.md) ·
→ [M5Stack DinMeter v1.1 (K134-V11)](../../../devices/m5stack/dinmeter-v1.1/README.md)

*Added 2026-09-04 by the DinMeter research pass. Evidence: `K134_DIN_Meter_v1.0-schematic.pdf`
(byte-identical for v1.0 and v1.1, SHA-256 `03ec3353…`) and `Sch_StampS3_v0.3.3.pdf`, both
Altium marker layers parsed.*

Two entirely separate roles, one on the carrier and one inside the core module:

| Where | Designator | Input | `EN` from | Output | Load |
|---|---|---|---|---|---|
| **DinMeter carrier** (both revisions) | `U6` | `+3.3V` | `LCD_BL` = **GPIO9** | `FPC_LCD_BL` | 1.14 in ST7789 panel backlight LEDs via `FPC1` pin 8 |
| **Stamp-S3A module only** (rev v0.3.3) | `U2` | `VDD_3V3` | `DISP_BL` = **GPIO38** (internal to the module) | `BL_3V3` | rear LCD-FPC backlight rail **and** the module's WS2812B-2020 RGB LED |

**Carrier `U6`.** The schematic value string is `AW35122FDR`, at (597, 521.3) beside the `U6`
outline; ball labels `A1`, `A2`, `B1`, `B2` and the pin names `VIN`, `VOUT`, `EN`, `GND` are all
recovered from the marker layer. It is driven as a **PWM-dimmed** backlight switch —
`espressif/esp-board-manager` models GPIO9 as an LEDC channel (`ledc_backlight`, channel 0,
timer 0, 5 kHz, 10-bit), so the part is being switched at 5 kHz rather than used as a static
enable. Its 165 µs typical rise time is far shorter than a 200 µs LEDC period, so dimming works,
but the *linearity* of the resulting brightness curve is a function of that rise time and has
not been characterised here.

**Stamp-S3A `U2` — the interesting one.** On the previous Stamp-S3 (board rev v0.2) this switch
was an [SGM2578](../../sgmicro/sgm2578/README.md) (second value string `WS4622C-4/TR`) gating only
the rear FPC backlight rail, while the WS2812B RGB LED sat on the always-on `VDD_3V3`. On rev
v0.3.3 the part became an AW35122FDR **and the RGB LED was moved onto its output**. That is the
single firmware-visible difference between Stamp-S3 and Stamp-S3A, and therefore between
DinMeter v1.0 and v1.1: on v1.1, **GPIO38 must be driven high before the RGB LED will light**.
M5Stack states this explicitly on the DinMeter v1.1 page; the schematic confirms the net change.
Full treatment: [`components/m5stack/stamp-s3a/README.md` §3](../../m5stack/stamp-s3a/README.md).

**Integration note specific to these boards.** The AW35122's `EN` has an internal ~7.1 MΩ
pull-down (§1.1), so both rails default **off** at reset — the panel backlight is dark and the
RGB LED is unlit until firmware acts. On the DinMeter that is desirable (no flash of a
white backlight during boot); on a Stamp-S3A it is the reason a straight port of Stamp-S3 LED
code appears to do nothing.

---

### M5Stack Stamp-S3A, and every board that uses it

Designator **U2** on `Sch_StampS3_v0.3.3.pdf`. `VIN` ← `VDD_3V3`, `VOUT` → **`BL_3V3`**,
**`EN` ← `DISP_BL` = GPIO 38**.

`BL_3V3` supplies the **LCD backlight *and* the [WS2812](../../worldsemi/ws2812/README.md) RGB
LED**. On the older **StampS3 v0.2** the WS2812 was fed from the always-on `VDD_3V3` and this
part was an [SGM2578](../../sgmicro/sgm2578/README.md) doing a different job — verified by
diffing U3's `VDD` net across the two schematics.

**Consequence, and it is documented behaviour:** PWM-dimming the backlight chops the LED's
supply. M5Stack states on the Cardputer v1.1 page — *"when the LCD backlight brightness is below
100%, RGB will not be powered properly"* — and **omits the same warning from the Cardputer ADV
page**, which inherits the identical arrangement.

Boards affected: [Cardputer v1.1](../../../devices/m5stack/cardputer-v1.1/README.md),
[Cardputer ADV](../../../devices/m5stack/cardputer-adv/README.md),
[Cardputer Mesh Kit](../../../devices/m5stack/cardputer-mesh-kit/README.md). **Not** the
[Cardputer v1.0](../../../devices/m5stack/cardputer-v1.0/README.md), which is therefore the only
Cardputer whose RGB LED is independent of the backlight.

*Added 2026-09-07 from `archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md` §3.4.*

## 5. Drivers and libraries

**Not applicable at the component level** — the part has no bus interface. On the PaperMono the control path is:

```cpp
// Arduino / ESP-IDF, via the M5IOE1 library
ioe1.pinMode(M5IOE1_PIN_12, OUTPUT);       // PDM_VDD  (PYG12)
ioe1.digitalWrite(M5IOE1_PIN_12, HIGH);    // enable the microphone rail
```

> ⚠ **Pin-numbering trap.** M5IOE1 labels are 1-based but the enum *values* are 0-based — `M5IOE1_PIN_3 == 2` (`M5IOE1/src/M5IOE1.h:34`). Passing a documentation "PYG*n*" number straight into a raw register write targets pin *n* + 1. Use the enum. **[SRC]**

---

## 6. Integration pitfalls

1. **Confirm you have AW35122, not AW3512** (§1.1). If the board omits an external `EN` pull-down, the substitution is a live hazard.
2. **No reverse-current blocking.** If the downstream rail can be back-driven (a card inserted with its own supply, an FPC shorted to another rail), current flows back through the body diode.
3. **R<sub>DS(on)</sub> triples between 3.3 V and 1.2 V** (§2). Budget the drop at your actual supply, not at 5.5 V.
4. **The output discharges on disable.** Convenient for clean power cycling, but it means you cannot use the switch to "park" a rail at its last value.
5. **1.5 A continuous is a thermal figure too** — θ<sub>JA</sub> is 166 °C/W in a 1 mm² package.

---

## 7. Alternatives

| Part | vs. AW35122 | When |
|---|---|---|
| **AW3512** | Same part, **no internal `EN` pull-down** | Only when the board provides its own pull-down |
| TI **TPS22918** / **TPS22916** | Comparable class, with reverse-current blocking on some variants, US-vendor documentation | When back-drive is possible, or Awinic sourcing is a problem |
| **[SGM40567](../../sgmicro/sgm40567/README.md)**-class discrete PMOS + gate resistor | Cheaper BOM | Loses slew-rate control and output discharge; inrush becomes your problem |
| An **enable-pin LDO** (e.g. [SSP7615-33DFR](../../generic/ssp7615-33dfr/README.md)) | Regulates as well as switches | When the downstream rail needs its own regulation — which is why the PaperMono uses one for `EPD_3V3_L3B` |

---

## 8. Open questions

- Whether sheet 6's `U1` is genuinely an AW35122FDR (§4.2).
- Whether the `PYB_NFC_EN` "spare GPIO" annotation on sheet 4 contradicts M5Stack's firmware, or whether the net is repurposed somewhere not visible in the extracted text (§4.2).
- No hardware measurement of turn-on slew, inrush or rail settling on any of the four instances.

---

## Manufacturer

**Shanghai Awinic Technology Co., Ltd.** No vendor sourcing guide exists in this repository yet; the working retrieval recipe is recorded in the [AW32901 record](../aw32901/README.md#manufacturer) and applies unchanged here — use the **full ordering part number** in `https://www.awinic.com/en/productDetail/<PART>`, read `data-file-url`, then fetch through `https://www.awinic.com/en/download?file=…&fileName=…`.

## Related pages

- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — drives all four enable lines
- [Awinic AW39112DNR](../aw39112/README.md) — the touch-bus translator powered from `TP_VDD`, instance 2's rail
- [Awinic AW9967DNR](../aw9967/README.md) — the other `L3B` rail, produced by a boost rather than a switch
- [SSP7615-33DFR](../../generic/ssp7615-33dfr/README.md) — the LDO used for `EPD_3V3_L3B`
- [FocalTech FT6336G](../../focaltech/ft6336g/README.md) — powered by instance 2
- [LMD4737T261-AC02 PDM microphone](../../generic/lmd4737t261-ac02-pdm-microphone/README.md) — powered by instance 3
- [microSD / SDMMC interface](../../generic/micro-sd-sdmmc/README.md) — powered by instance 1

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | AW3512 / AW35122 datasheet | Awinic | primary | datasheet | `https://www.awinic.com/en/download?file=doc/20230609wm/b56e7f1e-10ba-4096-aa95-2339ccbad7cc.pdf&fileName=DS_AW35122_EN_V1.0` | 2026-09-01 | **V1.0**, July 2019, 18 pp, 1 329 728 B | Pin definition, R<sub>DS(on)</sub> table, absolute maxima, the AW3512/AW35122 `EN` pull-down difference | `artifacts/aw3512-aw35122-datasheet-en-v1.0.pdf` |
| D2 | AW35122FDR product page | Awinic | primary | official page | <https://www.awinic.com/en/productDetail/AW35122FDR> | 2026-09-01 | — | Category, `FCDFN 1X1-4L` package, t<sub>R</sub> 165 µs, active-high enable, output discharge, no reverse-current block | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | Every instance, rail and enable net in §4 | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | `M5PaperMono-UserDemo` HAL — `hal_tf_card.cpp`, `hal_mic.cpp`, `hal_board.cpp`, `app_sleep_wake.cpp` | M5Stack | primary | repository | <https://github.com/m5stack/M5PaperMono-UserDemo> | 2026-09-01 | `main` @ `c1099107271d31a0678d661a896e2b04dbb331ea`, MIT | The M5IOE1 pin assignments in §4.1 | `archive/devices/m5stack/papermono/artifacts/source-snapshots/M5PaperMono-UserDemo/` |
| S3 | `M5IOE1/src/M5IOE1.h` | M5Stack | primary | repository | <https://github.com/m5stack/M5IOE1> | 2026-09-01 | `main` @ `846eec7d05e25c09013be2acdb8804487f48a62e`, MIT | The 1-based label / 0-based enum trap in §5 | `archive/devices/m5stack/papermono/artifacts/source-snapshots/M5IOE1/` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/aw3512-aw35122-datasheet-en-v1.0.pdf` | 1 329 728 | `35871c05ae81890b29f1223deca01ce8da5203539e72dbd826d473b3b1e925ee` | 18 |

**Method note.** D1 validated as `%PDF`, 18 pages, text layer intact. Retrieved with plain `curl` and a Chrome 131 User-Agent; no fallback needed and no login required.
