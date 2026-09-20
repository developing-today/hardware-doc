# M5Stack Stamp-S3A

- **Category:** ESP32-S3 **core module**. The successor to [Stamp-S3](../stamp-s3/README.md),
  and the reason the [DinMeter v1.1](../../../devices/m5stack/dinmeter-v1.1/README.md) exists.
- **SKU:** **`S007-V033`** (SMD). Header variants `S007-PIN127-V033`, `S007-PIN254-V033`.
- **Scope:** module level. ESP32-S3 silicon → [`components/espressif/esp32-s3r8/`](../../espressif/esp32-s3r8/README.md)
  (same family; this module fits the **FN8**: 8 MB in-package flash, **no PSRAM**).
- **Retrieved:** 2026-09-04

> **The one-line answer.** Same SoC, same flash, same *no* PSRAM, same 23 GPIOs, same 2.54/1.27
> pitch, same USB-C, same WS2812B-2020, same button. What changed: **the switching regulator was
> replaced**, **the antenna match was rebuilt**, and **the RGB LED lost its always-on supply** —
> it now hangs off the switched backlight rail and needs **GPIO38 driven high** before it will
> light. That last one is the only change that can break existing firmware.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH-A]** | `Sch_StampS3_v0.3.3-StampS3A.pdf`, Altium marker layer parsed, cited by designator | `executed-success` extraction |
| **[SCH-3]** | `Sch_M5StampS3_v0.2.pdf` (the Stamp-S3), same method | `executed-success` |
| **[DOC]** | <https://docs.m5stack.com/en/core/Stamp-S3A> and the DinMeter v1.1 page, 2026-09-04 | `not-tested` |
| **[SRC]** | Source at a cited `file:line` | `executed-success` read |
| **[INF]** | Inference | `inferred` |

**No Stamp-S3A hardware was in hand.** Nothing here is measured.

---

## 1. Identity, and the name

| Property | Value | Evidence |
|---|---|---|
| Marketed name | **Stamp-S3A** | **[DOC]** |
| SKU | **`S007-V033`** | **[DOC]** page header |
| Documentation | <https://docs.m5stack.com/en/core/Stamp-S3A> (HTTP 200) | **[DOC]** |
| Published schematic filename | **`Sch_StampS3_v0.3.3.pdf`** | **[SCH-A]** URL |
| M5_Hardware product directory | `Products/S007-V033_Stamp-S3A/` | **[SRC]** |

Three independent naming signals — SKU suffix `-V033`, schematic filename `v0.3.3`, and the
directory name — all say the same thing: **the "A" is a marketing label for board revision
v0.3.3 of the same S007 product**, not a new product line. The Stamp-S3's schematic is
`Sch_M5StampS3_v0.2.pdf` (rev v0.2). **[SCH-A]** **[SCH-3]** **[INF]**

That framing matters. It predicts — correctly, as §2 shows — that the changes would be
incremental board-level fixes rather than a redesign.

---

## 2. The complete Stamp-S3 → Stamp-S3A delta

### 2.1 What the vendor says

The Stamp-S3A page carries a two-row "Product Comparison" table and nothing else: **[DOC]**

| Item | Stamp-S3A | Stamp-S3 |
|---|---|---|
| RGB LED control logic | "RGB LED power is multiplexed with the reserved screen FPC bus backlight" | "Powered as soon as power is applied" |
| Antenna design | "Optimized antenna design with better signal reception" | "Conventional antenna design" |

The DinMeter v1.1 page restates the first one in actionable form: **[DOC]**

> "Stamp-S3A adds an independent electronic switch for the RGB LED power supply compared with the
> previous Stamp-S3. Before controlling the RGB LED in software, set **GPIO38**, which controls
> this switch, to a high level."

### 2.2 What the schematics say

Designator diff, from a full `CO`-marker census of both sheets plus visible designator text
(retained at [`artifacts/stamp-s3-vs-s3a-designator-diff.txt`](artifacts/stamp-s3-vs-s3a-designator-diff.txt)):

| | Designators |
|---|---|
| **Removed** in v0.3.3 | `D6`, `JP1`, `JP4`, **`M2`**, `R3`, `R6`, `R17` |
| **Added** in v0.3.3 | `C15`, `C16`, `C18`, `C19`, `C20`, `C24`, `C25`, **`L4`**, `L6`, `L7`, **`U4`** |
| Common (48) | `ANT1`, `C1`–`C14`, `C17`, `C21`–`C23`, `C26`, `D1`–`D4`, `D14`, `F1`, `J1`–`J3`, `JP2`, `JP3`, `L1`–`L3`, `L5`, `M1`, `PHD1`, `R1`, `R2`, `R4`, `R5`, `R7`, `R16`, `S1`, `U1`–`U3`, `X1` |

Four changes fall out of that, in descending order of consequence.

---

## 3. Change 1 — the RGB LED is no longer always powered *(firmware-visible)*

`U2` is the load switch that gates the rear LCD-FPC backlight rail. Its enable is `DISP_BL` =
**ESP32-S3 GPIO38** (`U1` pad 43) on **both** revisions. **[SCH-3]** **[SCH-A]**

| | Stamp-S3 v0.2 | Stamp-S3A v0.3.3 |
|---|---|---|
| `U2` part | **`SGM2578`** (alt value text `WS4622C-4/TR`) | **`AW35122FDR`** |
| `U2` `EN` | `DISP_BL` (GPIO38) | `DISP_BL` (GPIO38) |
| `U2` `VOUT` net | FPC backlight only | **`BL_3V3`** |
| `U3` (WS2812B-2020) `VDD` | **`VDD_3V3`** — always on | **`BL_3V3`** — switched |
| `U3` `DI` | `SK_DIN` ← GPIO21 | `SK_DIN` ← GPIO21 |

**[SCH-3]** `U2`@(509.5,69.7) value `SGM2578`@(520.5,121.4) + `WS4622C-4/TR`@(528.4,128.6);
`U3` `VDD` net `VDD_3V3`@(607.1,125.0).
**[SCH-A]** `U2`@(506.0,69.7) value `AW35122FDR`@(523.1,121.4); `U3` `VDD` net `BL_3V3`@(606.4,207.7).

So the schematic reading and the vendor prose agree exactly. **This is the one change that
breaks source compatibility**, and only for code that lights the RGB LED:

```cpp
// Works on Stamp-S3. Does nothing visible on Stamp-S3A.
M5.Lcd /* ... */;  pixels.setPixelColor(0, red); pixels.show();

// Portable across both:
pinMode(38, OUTPUT);
digitalWrite(38, HIGH);          // enable BL_3V3 -> WS2812 VDD (no-op on Stamp-S3)
delay(1);                        // allow the rail to settle before the first WS2812 frame
pixels.setPixelColor(0, red); pixels.show();
```

`inferred` — not built, not run on hardware. The GPIO number and the polarity are from the
schematic and the vendor text; the settle delay is prudence, not a documented requirement.

> **This affects the [DinMeter v1.1](../../../devices/m5stack/dinmeter-v1.1/README.md).** The
> DinMeter carrier does not use GPIO38 for anything — it drives its own panel backlight from
> GPIO9 through its own AW35122FDR. GPIO38 is entirely inside the module. So on DinMeter v1.1,
> GPIO38 has exactly one job: turning the Stamp's status LED on.
>
> **[SRC]** M5Unified's RGB-LED table gives `board_M5DinMeter → GPIO_NUM_21`
> (`M5Unified/src/M5Unified.cpp:246`) and contains **no GPIO38 enable step for any board**
> (checked at master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb`, 2026-09-04). If M5Unified's
> `board_M5DinMeter` path is used unchanged on a v1.1 unit, the RGB LED will not light. This is
> a **predicted** defect from reading the source against the vendor note — it has **not** been
> reproduced on hardware. Recorded as such in
> [`devices/m5stack/dinmeter-v1.1/gaps-and-conflicts.md`](../../../devices/m5stack/dinmeter-v1.1/gaps-and-conflicts.md).

---

## 4. Change 2 — the antenna front end was rebuilt

| | Stamp-S3 v0.2 | Stamp-S3A v0.3.3 |
|---|---|---|
| `ANT1` part text | **`PROANT440`** | **none printed** |
| Match elements between `ANT1` and `ESP_LNA` | `L1` 2.2 nH, `C1` 2.2 pF, `C2` 2.0 pF | `L6` (0 R), `C19`, `C20` (**NC**), `L1` 2.7 nH, `C2` 2.2 pF, `C1` 1.8 pF, values `4.3 nH` / `0R` present |
| Extra network on `ESP_EN` / `U1` pad 4 | none | `L7` 0 R + `C24` (3 pF) |
| `C9` (crystal network) | 10 pF | 12 pF |
| `C8` | 100 nF/25 V | 3 pF/25 V |
| `L2` adjacent values | `12 pF`, `2 nH` | `2 nH` |

**[SCH-3]** / **[SCH-A]**, from the value text nearest each `CO` marker.

Two honest caveats:

1. **Value-to-designator association is nearest-neighbour**, and the antenna corner is dense.
   `C19 ≈ 4.3 nH` is physically odd for a capacitor and probably belongs to `L6`; treat the
   individual antenna values as indicative, and the *topology* change (3 elements → 6, plus a
   filter on `ESP_EN`) as solid.
2. **`PROANT440` does not appear anywhere on the v0.3.3 sheet** (searched in both single and
   double-struck glyph forms; zero hits). Either the antenna part changed, or the value text was
   dropped. **Not established which.**

The vendor's claim is qualitative — "better signal reception" — with **no measured figure**
(no dBi, no RSSI comparison, no test method). Nothing here corroborates or refutes it.

---

## 5. Change 3 — the DC-DC was replaced *(and the datasheet page is stale)*

| | Stamp-S3 v0.2 | Stamp-S3A v0.3.3 |
|---|---|---|
| Designator | `M2` | `U4` |
| Part | **`MUN3CAD01-SC`** (µPOL module, 1 A, integrated inductor, 2.9 × 2.3 × 1.05 mm) | **not printed on the sheet** |
| Pins | 6: `EN`, `GND`, `VIN`, `GND`, `FB`, `VOUT` | 8 balls: `A1 SW`, `A2 VIN`, `B1 EN`, `B2 GND`, `C1 VSEL1`, `C2 VOS`, `D1 VSEL2`, `D2 VSEL3` |
| Annotation | — | **`IOUT: 0~0.6A`** |
| External inductor | none | **`L4` = `MWTC201608S2R2`** (2.2 µH, 2016 metric / 0806) |
| Output set by | `R6` 100 kΩ / `R17` 22.1 kΩ feedback divider | **pin-strapped** `VSEL1/2/3` (no divider — `R6`/`R17` deleted) |
| Support passives | `C21`, `C22` 10 µF | `C15` 1 nF, `C16` 10 µF, `C18` 100 nF, `C21`/`C22`/`C25` 10 µF |

**[SCH-3]** `M2`@(207,476.7), `MUN3CAD01-SC`@(228.7,513.7).
**[SCH-A]** `U4`@(185,465.7), ball labels at (174.1,474.2)…(218.8,535.3), `IOUT: 0~0.6A`@(209.4,452.6),
`L4`@(300,470.7) value `MWTC201608S2R2`@(307.2,463.4).

> ### ⚠ Conflict: the Stamp-S3A page still lists MUN3CAD01-SC
>
> The Stamp-S3A specification table gives **`DC-DC: MUN3CAD01-SC`** and links its datasheet at
> `https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/Stamp/S007%20StampS3/MUN3CAD01-SC.pdf`
> — the *same* path the Stamp-S3 page uses (note the `S007 StampS3` directory). **[DOC]**
>
> The string `MUN3CAD01` **does not occur anywhere** in `Sch_StampS3_v0.3.3.pdf`. The part it
> names is a µPOL module with an *integrated* inductor and an `FB` pin; the v0.3.3 design fits a
> part with an external 2.2 µH inductor and three `VSEL` strapping balls. These are not the same
> device.
>
> **Reading:** the specification row was carried over unedited from the Stamp-S3 page. The
> schematic is the stronger evidence. `U4`'s actual part number is **unidentified** — recorded
> at [`components/unidentified/m5stack-stamp-s3a/dcdc-u4/`](../../unidentified/m5stack-stamp-s3a/dcdc-u4/README.md)
> rather than guessed. **No candidate part number is asserted anywhere in this repository.**

---

## 6. Change 4 — `ESP_EN` and GPIO2 support parts

| | v0.2 | v0.3.3 |
|---|---|---|
| `D6` 1N4148WT on `ESP_EN` | present | **removed** |
| `R7` 10 kΩ, `R16` 100 kΩ, `C23` 1 µF on `ESP_EN` | present | present |
| `L7` 0 R + `C24` on `ESP_EN` | — | **added** |
| `R3` 10 kΩ/1 % on GPIO2 | present | **removed** |
| `JP1`, `JP4` | present | **removed** |

**[SCH-3]** **[SCH-A]** Effect not analysed; recorded for completeness.

---

## 6b. The FPC numbering question

`J1` (12-pin) and `J3` (8-pin) rear LCD headers carry the **same nets in the same physical
order** on both revisions, but the **pin numbers run in opposite directions**:

| | v0.2 | v0.3.3 |
|---|---|---|
| `J1` pin carrying `VIN_5V` | **1** | **12** |
| `J1` pin carrying `DISP_CS` | **12** | **1** |
| `J3` pin carrying `DISP_CS` | **8** | **1** |
| `J3` pin carrying GPIO2 node | **1** | **8** |

**[SCH-3]** / **[SCH-A]** from `PIJ10x` / `PIJ30x` markers.

**This is not resolved.** It is either (a) a physical re-orientation of the FPC connector, which
would mean an existing display flex mates backwards, or (b) a symbol renumbering that was
mirrored in the footprint, which would mean nothing changed physically. The schematic alone
cannot distinguish them.

Weight of evidence leans to **(b)**: the connector part number is unchanged
(`HDGC/0.5K-HX-8PWB/NC`), `m5stack/M5_Hardware` publishes **no Stamp-S3A footprint**, and
`Stamp-S3A.stl` is byte-identical to `Stamp-S3.stl`. But that is inference. Anyone attaching a
display flex to the back of a Stamp-S3A should verify against the official pin-map image
([`artifacts/S007-V033_PinMap_01.jpg`](artifacts/S007-V033_PinMap_01.jpg)) before powering up.
**[INF]**

**It does not affect the DinMeter.** The DinMeter drives its panel from carrier GPIOs through
its own `FPC1`, not through the Stamp's rear header.

---

## 7. Mechanical

| Property | Stamp-S3 | Stamp-S3A | Evidence |
|---|---|---|---|
| Product size | 24.0 × 18.0 × 4.7 mm | **26.0 × 18.0 × 4.7 mm** | **[DOC]** both pages |
| Weight | 3.0 g | 2.9 g | **[DOC]** |
| Package size | 138.0 × 93.0 × 10.5 mm | 138.0 × 93.0 × 10.5 mm | **[DOC]** |
| Published STL | `Stamp-S3.stl` | `Stamp-S3A.stl` | **[SRC]** |
| STL SHA-256 | `f72c1af2d42930fc57a3db1bd3282568a3952095f77539016a12437d59d7df5d` | **identical** | **[SRC]** |
| Published KiCad footprint | `Stamp-S3-SMD` / `-DIP` / `_PIN1.27_Socket` / `_PIN2.54_DIP` | **none** | **[SRC]** |

> ### ⚠ Conflict: 24 mm vs 26 mm
>
> The two specification tables differ by 2 mm in length, but the two mechanical models are the
> same bytes and no new footprint was published. One of the two is wrong, and the vendor has not
> said which. A 2 mm growth would be a breaking change for any host PCB — and yet **M5Stack ships
> the Stamp-S3A on the DinMeter v1.1 carrier whose published PCB assets are unchanged from
> v1.0**, which argues the footprint did not grow. **[INF]**
>
> **Practical advice:** if you are laying out a board for a Stamp-S3A, measure a real part or ask
> M5Stack. Do not trust either number. This is recorded in
> [`devices/m5stack/dinmeter/gaps-and-conflicts.md`](../../../devices/m5stack/dinmeter/gaps-and-conflicts.md) §5.

Dimension drawing: [`artifacts/STAMP-S3A-dimensions.pdf`](artifacts/STAMP-S3A-dimensions.pdf).

---

## 8. Power — the headline improvement

| Mode | Supply | Stamp-S3 | Stamp-S3A | Change |
|---|---|---|---|---|
| Sleep | USB Type-C | 400.67 µA | **88.82 µA** | **−78 %** |
| Sleep | `VIN_5V` | 310.89 µA | **6.84 µA** | **−98 %** (≈ 45×) |
| Standby | USB Type-C | 33.04 mA | **25.54 mA** | −23 % |
| Standby | `VIN_5V` | 33.56 mA | **25.53 mA** | −24 % |

**[DOC]** both product pages. **Vendor figures, no stated method** — no clock configuration, no
radio state, no peripheral state, no instrument, no sample count. They are quoted to two decimal
places, which implies more precision than an unspecified method can support. Do not size a
battery from them without measuring.

Mechanistically the improvement is consistent with the two power changes: a modern buck IC with
selectable light-load modes replacing a fixed µPOL module, plus removing the WS2812B's quiescent
draw from the always-on 3.3 V rail (a WS2812B-2020 idles around 0.6–1 mA). **[INF]** — plausible
but not decomposed or measured.

The `VIN_5V` sleep figure (6.84 µA) is startling and is the single strongest reason to prefer
the S3A for a battery product.

---

## 9. What did *not* change

Stated positively so the absence is a finding, not an omission:

| Property | Both revisions | Evidence |
|---|---|---|
| SoC | ESP32-S3FN8, Xtensa LX7 dual-core @ 240 MHz | **[DOC]** both; **[SCH]** `U1` symbol on both |
| Flash | 8 MB in-package | **[DOC]** |
| **PSRAM** | **none, on either** | **[DOC]** — no PSRAM row on either page; `FN8` has none |
| Broken-out GPIOs | 23 — G0, G1–G15, G39–G44, G46 — **identical list** | **[DOC]** both pages |
| Internal GPIO21 | WS2812B-2020 data | **[SCH]** both, `U1` pad 27 |
| Internal GPIO33–38 | rear FPC `DISP_RST/RS/MOSI/SCK/CS/BL` | **[SCH]** both, `U1` pads 38–43 |
| USB | native USB-C, `J2`, `R1`/`R2` 5.1 kΩ CC | **[SCH]** both |
| RGB LED part | WS2812B-2020 ×1 | **[DOC]** both |
| User button | ×1 on GPIO0 | **[DOC]** both |
| Crystal | `X1` + `L3` 10 nH | **[SCH]** both |
| IO pitch | 2.54 mm and 1.27 mm | **[DOC]** both |
| LCD FPC pitch | 0.5 mm, 12 P or 8 P | **[DOC]** both |
| Operating temp | 0 – 40 °C | **[DOC]** both |
| Download mode | hold `G0` while applying power | **[DOC]** both |
| Price | USD 7.50 (S3A, 2026-09-04) | **[DOC]** shop |

---

## 10. Is firmware source-compatible?

**Yes, with exactly one exception.**

| Aspect | Verdict | Basis |
|---|---|---|
| Toolchain / target | Identical (`esp32s3`, no PSRAM) | **[DOC]** |
| Pin assignments for user IO | Identical | **[DOC]** |
| M5Unified board enum | **Unchanged** — there is **no `board_M5StampS3A`** in M5Unified master `8530f537…` (2026-09-04). An S3A enumerates as `board_M5StampS3` | **[SRC]** grep of `src/` |
| DinMeter board enum | `board_M5DinMeter` for both v1.0 and v1.1 — M5Unified has no v1.1 variant | **[SRC]** |
| Display, encoder, RTC, buzzer, I²C, power-hold | Identical | **[SRC]** **[SCH]** |
| **RGB LED** | **Breaks.** Needs `GPIO38 = HIGH` first on S3A | **[DOC]** **[SCH-A]** |
| Boot / download procedure | Identical | **[DOC]** |
| Antenna / RF behaviour | Different silicon-external network; no API impact | **[SCH]** |

So: recompile nothing, change nothing — unless you use the RGB LED.

---

## 11. Artifacts

| File | Size | SHA-256 (16) | What it is | Licence | Redistribution | Disposition |
|---|---:|---|---|---|---|---|
| [`artifacts/Sch_StampS3_v0.3.3-StampS3A.pdf`](artifacts/Sch_StampS3_v0.3.3-StampS3A.pdf) | 369 766 | `2f9610aecc5a5d2e` | **Primary evidence.** Board rev v0.3.3 schematic. Renamed from upstream `Sch_StampS3_v0.3.3.pdf` to record that it is the S3A's | unknown | unknown | repository |
| [`artifacts/Sch_StampS3_v0.3.3-StampS3A.plaintext-layout.txt`](artifacts/Sch_StampS3_v0.3.3-StampS3A.plaintext-layout.txt) | 7 830 | `0dddf2cc41d9f6e2` | derived: sheet text as rows | derived | — | repository |
| [`artifacts/stamp-s3-vs-s3a-designator-diff.txt`](artifacts/stamp-s3-vs-s3a-designator-diff.txt) | 716 | `8278f9ab8975d7c5` | derived: the census diff behind §2.2 | derived | — | repository |
| [`artifacts/STAMP-S3A-dimensions.pdf`](artifacts/STAMP-S3A-dimensions.pdf) | 95 380 | `27ba520610b03e41` | mechanical drawing | unknown | unknown | repository |
| [`artifacts/Stamp-S3A.stl`](artifacts/Stamp-S3A.stl) | 158 484 | `f72c1af2d42930fc` | mechanical model — **byte-identical to `Stamp-S3.stl`** | unknown | unknown | repository |
| [`artifacts/S007-V033_PinMap_01.jpg`](artifacts/S007-V033_PinMap_01.jpg) | 693 286 | `979f3572d60fd9ef` | official pin-map diagram | unknown | unknown | repository |

Upstream URLs and retrieval dates: [`devices/m5stack/dinmeter/sources.md`](../../../devices/m5stack/dinmeter/sources.md)
(rows S-14 … S-20). `Stamp-S3A.stl` was fetched from `m5stack/M5_Hardware` at commit
`a240115c94b19ecf647f229c47fa9a8ce46ccdc4`.

**Deliberate duplication:** `Stamp-S3.stl` and `Stamp-S3A.stl` have the same SHA-256 and are both
retained, one under each component. That is intentional — the *fact* that M5Stack publishes the
same bytes under two product names is the finding, and deduplicating would erase it. Roughly
158 KB of redundancy, accepted.

## Related components

- [`components/awinic/aw35122`](../../awinic/aw35122/README.md) — `U2` on this module
- [`components/sgmicro/sgm2578`](../../sgmicro/sgm2578/README.md) — `U2` on the Stamp-S3
- [`components/murata/mun3cad01-sc`](../../murata/mun3cad01-sc/README.md) — `M2` on the Stamp-S3, *not* fitted here
- [`components/unidentified/m5stack-stamp-s3a/dcdc-u4`](../../unidentified/m5stack-stamp-s3a/dcdc-u4/README.md) — `U4`, this module's actual regulator
- [`components/espressif/esp32-s3r8`](../../espressif/esp32-s3r8/README.md) — the SoC family

---

## Used By

### M5Stack DinMeter v1.1 (SKU K134-V11)

Fitted as **`M1`** on a carrier whose published schematic and STL are byte-identical to the
v1.0 board's. The GPIO map is unchanged from v1.0 in every respect — display, encoder, RTC,
buzzer, button, power hold, Grove ports. **[DOC]** The substitution of this module for the
Stamp-S3 *is* the v1.1 revision.

The one behavioural consequence on this carrier: the Stamp's RGB LED (GPIO21) now requires
**GPIO38 high** first. GPIO38 is not otherwise used on the DinMeter, so there is no conflict —
just a required extra line.

→ [`devices/m5stack/dinmeter-v1.1/README.md`](../../../devices/m5stack/dinmeter-v1.1/README.md)

### Other M5Stack products carrying Stamp-S3A

Observed on `shop.m5stack.com` 2026-09-04 (search evidence, not exhaustive): **Air Quality Kit
v1.1 with M5StampS3A (SEN55, SCD40)**, USD 89.90. Also sold standalone as `M5StampS3A ESP32S3
Module` (USD 7.50), `M5StampS3A with 1.27 Header Pin` (7.50) and `M5StampS3A with 2.54 Header
Pin` (7.50). **[DOC]**

### Devices carrying this module

| Device | Record | Notes |
|---|---|---|
| **Cardputer ADV** (`K132-Adv`) | [`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md) | mainboard redesigned around the module's freed pins: TCA8418 keyboard on I²C, CAP expansion header |
| **Cardputer v1.1** (`K132-V11`) | [`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md) | **module-only refresh** of the v1.0 — the two mainboard schematics are byte-identical, SHA-256 `6016c1fe…` |
| **Cardputer Mesh Kit** (`K152`) | [`devices/m5stack/cardputer-mesh-kit`](../../../devices/m5stack/cardputer-mesh-kit/README.md) | ADV + Cap LoRa-1262 bundle |
| Cardputer Accessory Kit v1.1 | — | sold as a spare: Stamp-S3A + display, $9.95 at 2026-09-04 |

**How software tells this module's boards apart from Stamp-S3 boards:** it does not — M5GFX
discriminates on the *mainboard*, by driving G9/G8/G6/G5 as input-pulldown and testing whether
G8 and G9 still read high (the ADV's internal-I²C pull-ups). See
[`devices/m5stack/cardputer-adv/README.md` § Board autodetect](../../../devices/m5stack/cardputer-adv/README.md).

*Added 2026-09-07 from `scratch/m5stack-cardputer/index-fragments.md` §3.9.*
