# Stamp-S3 → Stamp-S3A: the complete delta

**Why this document exists.** The DinMeter v1.1 is the DinMeter with a different core module
soldered on it. Nothing else about the product changed that any published document shows. So
"what is a Stamp-S3A?" *is* "what is a DinMeter v1.1?", and it deserves to be answered from
primary evidence rather than from the two-row marketing table M5Stack provides.

**Method.** Both modules' Altium-published schematics were fetched and their invisible
`CO`/`PI`/`NL` marker layers parsed, giving a complete reference-designator census of each sheet
and a net-level reading of every IC. The two censuses were diffed. Board-support source
(M5Unified, Espressif's `esp-board-manager`, Bruce/Launcher) was read at pinned commits. Vendor
prose was used only where it says something the schematics cannot.

**Not measured.** No Stamp-S3A or DinMeter v1.1 hardware was available. Every current figure
below is the vendor's.

| Evidence marker | Meaning |
|---|---|
| **[SCH-3]** | `Sch_M5StampS3_v0.2.pdf` (Stamp-S3), SHA-256 `6d92e1aef6577838…`, parsed |
| **[SCH-A]** | `Sch_StampS3_v0.3.3.pdf` (Stamp-S3A), SHA-256 `2f9610aecc5a5d2e…`, parsed |
| **[DOC]** | `docs.m5stack.com` / `shop.m5stack.com`, retrieved 2026-09-04 |
| **[SRC]** | Source at a cited `file:line` / pinned commit |
| **[INF]** | Inference, reasoning stated |

---

## 1. The answer in one table

| Property | Stamp-S3 (`S007`) | Stamp-S3A (`S007-V033`) | Changed? | Evidence |
|---|---|---|---|---|
| **Board revision** | v0.2 | **v0.3.3** | ✔ | schematic filenames |
| **SoC** | ESP32-S3FN8, LX7 ×2 @ 240 MHz | ESP32-S3FN8, LX7 ×2 @ 240 MHz | ✘ | **[DOC]**, **[SCH-3]**/**[SCH-A]** `U1` symbol on both |
| **Flash** | 8 MB in-package | 8 MB in-package | ✘ | **[DOC]** |
| **PSRAM** | **none** | **none** | ✘ | **[DOC]** (no PSRAM row on either page); `FN8` has none in package; Bruce/Launcher `build_unflags = -DBOARD_HAS_PSRAM` **[SRC]** |
| **USB** | native USB-C on the module, `J2`, `R1`/`R2` 5.1 kΩ CC, `F1` fuse, `D14`, `JP3` | **identical designators, identical nets** | ✘ | **[SCH-3]**/**[SCH-A]** |
| **Broken-out GPIOs** | 23: G0, G1–G15, G39–G44, G46 | **same 23, same list** | ✘ | **[DOC]** both pages, character-for-character |
| **Pin pitch / mounting** | 2.54 mm + 1.27 mm; SMT/DIP/fly-wire | same | ✘ | **[DOC]** |
| **Rear LCD FPC** | 0.5 mm, 12 P (`J1`) or 8 P (`J3`), `HDGC/0.5K-HX-8PWB/NC` | same connector, **pin numbering runs the other way** | ⚠ | **[SCH-3]**/**[SCH-A]**, §6 |
| **RGB LED part** | WS2812B-2020 ×1, data GPIO21 | WS2812B-2020 ×1, data GPIO21 | ✘ | **[DOC]**, **[SCH]** `U3` on both |
| **RGB LED supply** | `VDD_3V3` — **always on** | **`BL_3V3` — switched, needs GPIO38 high** | **✔ ← the only firmware-visible change** | §3 |
| **Backlight/LED load switch** | `U2` = SGM2578 (alt `WS4622C-4/TR`) | `U2` = **AW35122FDR** | ✔ | §3 |
| **DC-DC** | `M2` = MUN3CAD01-SC µPOL module, 1 A, integrated inductor, FB divider `R6`/`R17` | `U4` = **unidentified 8-ball buck**, `IOUT: 0~0.6A`, external `L4` 2.2 µH, `VSEL1/2/3` straps | ✔ | §5 |
| **Antenna** | `ANT1` = **PROANT440**, 3-element match | `ANT1` **no part text**, 6-element match + `ESP_EN` filter | ✔ | §4 |
| **User button** | ×1, GPIO0 | ×1, GPIO0 | ✘ | **[DOC]**, `S1` on both |
| **Sleep, `VIN_5V`** | 310.89 µA | **6.84 µA** | ✔ **−98 %** | **[DOC]** |
| **Sleep, USB-C** | 400.67 µA | **88.82 µA** | ✔ **−78 %** | **[DOC]** |
| **Standby, `VIN_5V`** | 33.56 mA | **25.53 mA** | ✔ −24 % | **[DOC]** |
| **Size** | 24.0 × 18.0 × 4.7 mm | 26.0 × 18.0 × 4.7 mm | ⚠ **contradicted by identical STLs** | §7 |
| **Weight** | 3.0 g | 2.9 g | ✔ | **[DOC]** |
| **Price** | USD 7.50 | **USD 7.50** | ✘ | shop `.js`, 2026-09-04 |
| **Availability** | **`[EOL]`, out of stock** | in stock | ✔ | shop `.js`, 2026-09-04 |
| **Shop first published** | 2023-02-10 | 2025-09-11 | — | shop `.js` |
| **M5Unified board enum** | `board_M5StampS3` | **no `board_M5StampS3A` exists** — an S3A enumerates as `board_M5StampS3` | ✘ | **[SRC]** master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb` |

---

## 2. The designator diff

A complete `CO`-marker census of each sheet, plus visible designator text to catch markers the
parser's negative-lookbehind rule discards. Retained at
[`../../../components/m5stack/stamp-s3a/artifacts/stamp-s3-vs-s3a-designator-diff.txt`](../../../components/m5stack/stamp-s3a/artifacts/stamp-s3-vs-s3a-designator-diff.txt).

| | Count | Designators |
|---|---:|---|
| Stamp-S3 v0.2 total | 55 | — |
| Stamp-S3A v0.3.3 total | 59 | — |
| **Removed** | 7 | `D6`, `JP1`, `JP4`, **`M2`**, `R3`, `R6`, `R17` |
| **Added** | 11 | `C15`, `C16`, `C18`, `C19`, `C20`, `C24`, `C25`, **`L4`**, `L6`, `L7`, **`U4`** |
| **Common** | 48 | `ANT1`, `C1`–`C14`, `C17`, `C21`–`C23`, `C26`, `D1`–`D4`, `D14`, `F1`, `J1`–`J3`, `JP2`, `JP3`, `L1`–`L3`, `L5`, `M1`, `PHD1`, `R1`, `R2`, `R4`, `R5`, `R7`, `R16`, `S1`, `U1`, `U2`, `U3`, `X1` |

Note what is **common**: the SoC (`U1`), the crystal (`X1`), the USB receptacle (`J2`), the CC
resistors (`R1`/`R2`), both FPC headers (`J1`/`J3`), the RGB LED (`U3`), the button (`S1`), the
antenna designator (`ANT1`) and the load switch designator (`U2`). This is a **revision, not a
redesign** — which is exactly what the `S007` / `S007-V033` SKU relationship and the
`v0.2` → `v0.3.3` schematic numbering already implied.

Every added part clusters in two places: around `U4` (the new regulator and its passives) and
around `ANT1` (the new match). Every removed part is a support component for the parts they
replaced.

---

## 3. Change 1 — the RGB LED needs GPIO38 *(the only source-compatibility break)*

`U2` is the load switch feeding the rear LCD-FPC backlight rail. On **both** revisions its
enable is `DISP_BL` = **ESP32-S3 GPIO38** (`U1` pad 43). What changed is the *part* and, far
more importantly, **what its output feeds**.

| | Stamp-S3 v0.2 | Stamp-S3A v0.3.3 |
|---|---|---|
| `U2` value text | `SGM2578` @ (520.5, 121.4) + `WS4622C-4/TR` @ (528.4, 128.6) | `AW35122FDR` @ (523.1, 121.4) |
| `U2` `EN` (ball B2) | `DISP_BL` ← GPIO38 | `DISP_BL` ← GPIO38 |
| `U2` `VOUT` (ball A1) | FPC backlight rail only | **`BL_3V3`** |
| `U3` WS2812B-2020 `VDD` | **`VDD_3V3`** (always on) | **`BL_3V3`** (switched) |
| `U3` `DI` | `SK_DIN` ← GPIO21 | `SK_DIN` ← GPIO21 |
| Local decoupling | `C3` 100 nF/25 V | `C3` 100 nF/25 V |

**[SCH-3]** `U3` `VDD` net `VDD_3V3`@(607.1,125.0) · **[SCH-A]** `U3` `VDD` net `BL_3V3`@(606.4,207.7).

The vendor says the same thing in prose, on the DinMeter v1.1 page: **[DOC]**

> "The device uses Stamp-S3A as its main controller. To optimize overall power consumption,
> Stamp-S3A adds an independent electronic switch for the RGB LED power supply compared with the
> previous Stamp-S3. Before controlling the RGB LED in software, set **GPIO38**, which controls
> this switch, to a high level."

and on the Stamp-S3A page's comparison table: *"RGB LED power is multiplexed with the reserved
screen FPC bus backlight"* vs *"Powered as soon as power is applied"*.

Schematic and prose agree exactly. This is the strongest-evidenced claim in this document.

### Why it bites

The AW35122's `EN` has an internal **~7.1 MΩ pull-down** (see
[`components/awinic/aw35122`](../../../components/awinic/aw35122/README.md) §1.1), so `BL_3V3`
comes up **off** at reset. Existing DinMeter firmware that lights the LED will run, compile and
appear healthy — and the LED will simply stay dark.

Worse, **M5Unified will not save you.** At master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb`
(2026-09-04):

- `_pin_table_other0` (RGB LED) has `{ board_M5DinMeter, GPIO_NUM_21 }` at
  `src/M5Unified.cpp:246`. **[SRC]**
- There is **no `board_M5DinMeter_v11`** and **no `board_M5StampS3A`** enum anywhere in `src/`.
  **[SRC]** (grep, `executed-success`)
- There is **no GPIO38 enable step for any board** in the RGB-LED path. **[SRC]**

So a v1.1 unit enumerates as `board_M5DinMeter`, gets GPIO21 for the LED, and never gets the
rail turned on.

**Status: `inferred`.** Predicted from vendor documentation + schematic + source read. **Not
reproduced on hardware** — no v1.1 unit was available. If you have one, this is the first thing
to test, and the result belongs in
[`compatibility-and-status.md`](compatibility-and-status.md).

### Portable workaround

```cpp
// Safe on both revisions. On Stamp-S3, GPIO38 is unconnected to anything the carrier
// uses and driving it high is harmless; on Stamp-S3A it enables BL_3V3.
pinMode(38, OUTPUT);
digitalWrite(38, HIGH);
delay(1);                 // let the rail settle before the first WS2812 frame
// ... now drive GPIO21 as usual
```
`not-tested`. The 1 ms settle is prudence, not a documented requirement; the AW35122's typical
rise time is 165 µs.

> **On the DinMeter specifically, GPIO38 has exactly one job.** The DinMeter carrier does not use
> the Stamp's rear FPC header at all — it drives its own 1.14 in panel backlight from **GPIO9**
> through its **own** AW35122FDR (`U6`). GPIO38 is entirely internal to the module. So there is
> no conflict and no cost: raise it once at boot and forget it.

---

## 4. Change 2 — the antenna front end was rebuilt

| | Stamp-S3 v0.2 | Stamp-S3A v0.3.3 |
|---|---|---|
| `ANT1` part text | **`PROANT440`** @ (75.1, 55.7) | **none printed** |
| Match elements, `ANT1` → `ESP_LNA` | `L1` 2.2 nH, `C1` 2.2 pF, `C2` 2.0 pF — 3 elements | `L6` (0 R), `C19`, `C20` (**`NC`**), `L1` 2.7 nH, `C2` 2.2 pF, `C1` 1.8 pF — 6 positions, one unpopulated |
| Extra network at `U1` pad 4 (`CHIP_PU`/`ESP_EN`) | none | `L7` 0 R + `C24` (3 pF) |
| `C9` (crystal network) | 10 pF | 12 pF |
| `C8` | 100 nF/25 V | 3 pF/25 V |
| `L2` adjacent values | `12 pF`, `2 nH` | `2 nH` |

**[SCH-3]** / **[SCH-A]**, value text nearest each `CO` marker.

Two honest caveats:

1. **Value-to-designator association is nearest-neighbour** and the antenna corner is dense.
   `C19 ≈ 4.3 nH` is physically wrong for a capacitor and almost certainly belongs to `L6`.
   Treat individual values as indicative; treat the **topology** change (3 → 6 positions plus a
   `CHIP_PU` filter) as solid.
2. **`PROANT440` does not appear anywhere on the v0.3.3 sheet** — searched in both single and
   double-struck glyph forms, zero hits. Either the antenna part changed or its value text was
   dropped from the drawing. **Not established which.**

The vendor's claim is *"Optimized antenna design with better signal reception"* vs
*"Conventional antenna design"* — **qualitative, with no dBi figure, no RSSI comparison and no
test method**. Nothing found corroborates or refutes it. If you need the number, measure it.

---

## 5. Change 3 — the regulator was replaced *(and the spec page is stale)*

| | Stamp-S3 v0.2 | Stamp-S3A v0.3.3 |
|---|---|---|
| Designator | `M2` | `U4` |
| Part | **`MUN3CAD01-SC`** — µPOL module: 1 A, 2.7–5.5 V in, 0.8–4.0 V out, 93 % peak η, **integrated inductor**, 2.9 × 2.3 × 1.05 mm | **not printed on the sheet** |
| Pins | 6: `EN`, `GND`, `VIN`, `GND`, `FB`, `VOUT` | 8 balls: `A1 SW`, `A2 VIN`, `B1 EN`, `B2 GND`, `C1 VSEL1`, `C2 VOS`, `D1 VSEL2`, `D2 VSEL3` |
| Sheet annotation | — | **`IOUT: 0~0.6A`** @ (209.4, 452.6) |
| External inductor | none | **`L4` = `MWTC201608S2R2`** (2.2 µH, 2016-metric) |
| Output set by | `R6` 100 kΩ / `R17` 22.1 kΩ feedback divider | **pin straps** `VSEL1/2/3`; `R6`, `R17` **deleted** |
| Support passives | `C21`, `C22` 10 µF | `C15` 1 nF, `C16` 10 µF, `C18` 100 nF, `C21`/`C22`/`C25` 10 µF |

### ⚠ The Stamp-S3A page still lists `MUN3CAD01-SC`

Its specification table gives `DC-DC: MUN3CAD01-SC` and links
`…/resource/docs/datasheet/Stamp/**S007 StampS3**/MUN3CAD01-SC.pdf` — the Stamp-S3's own
directory. **[DOC]**

But the string `MUN3CAD01` **does not occur anywhere** in `Sch_StampS3_v0.3.3.pdf`, `M2` is
absent from the sheet, and the fitted part has `SW` + an external inductor + `VSEL` straps,
which a µPOL module does not have. The two are not the same device.

**Reading:** the row was carried over unedited. The schematic wins. `U4`'s part number is left
**unidentified** rather than guessed —
[`components/unidentified/m5stack-stamp-s3a/dcdc-u4/`](../../../components/unidentified/m5stack-stamp-s3a/dcdc-u4/README.md).
No candidate part number is asserted anywhere in this repository.

### The consequence nobody mentions

**The new regulator is rated 0.6 A; the old one was 1 A.** That is a *reduction* in 3.3 V
headroom, and the vendor does not mention it in either specification table or in the comparison
row. It is unlikely to matter on a DinMeter (the carrier makes its own 3.3 V from `U4`
BL8075CB5TR33 and only draws the module's `3V3` pin lightly), but it matters for anyone using a
bare Stamp-S3A to power external 3.3 V loads. **`inferred` from the sheet annotation.**

---

## 6. Change 4 — support parts, and the FPC numbering question

| | v0.2 | v0.3.3 |
|---|---|---|
| `D6` 1N4148WT on `ESP_EN` | present | **removed** |
| `L7` 0 R + `C24` on `ESP_EN` | — | **added** |
| `R3` 10 kΩ/1 % on GPIO2 | present | **removed** |
| `JP1`, `JP4` | present | **removed** |
| `R7` 10 kΩ, `R16` 100 kΩ, `C23` 1 µF on `ESP_EN` | present | present |

### The FPC headers are numbered in opposite directions

`J1` (12 P) and `J3` (8 P) carry the **same nets in the same physical order** on both
revisions, but their pin numbers run opposite ways:

| Net | v0.2 pin | v0.3.3 pin |
|---|---:|---:|
| `J1` `VIN_5V` | 1 | **12** |
| `J1` `DISP_CS` | 12 | **1** |
| `J3` `DISP_CS` | 8 | **1** |
| `J3` GPIO2 node | 1 | **8** |

**[SCH-3]** / **[SCH-A]** from `PIJ10x` / `PIJ30x` markers.

**Unresolved.** Either (a) the connector was physically re-oriented, in which case an existing
display flex mates backwards, or (b) the symbol was renumbered and the footprint mirrored with
it, in which case nothing changed. The schematic alone cannot distinguish them.

Evidence leans to **(b)**: same connector part number, `m5stack/M5_Hardware` publishes **no
Stamp-S3A footprint** at commit `a240115c94b19ecf647f229c47fa9a8ce46ccdc4`, and `Stamp-S3A.stl`
is byte-identical to `Stamp-S3.stl`. **[INF]**

**Irrelevant to the DinMeter** — the carrier does not use the Stamp's rear header. Relevant to
anyone attaching a display flex to a bare Stamp-S3A: verify against
[`S007-V033_PinMap_01.jpg`](../../../components/m5stack/stamp-s3a/artifacts/S007-V033_PinMap_01.jpg)
before powering up.

---

## 7. Mechanical — 24 mm or 26 mm?

| | Stamp-S3 | Stamp-S3A |
|---|---|---|
| Vendor size | 24.0 × 18.0 × 4.7 mm | **26.0** × 18.0 × 4.7 mm |
| Published STL | `Stamp-S3.stl` | `Stamp-S3A.stl` |
| STL SHA-256 | `f72c1af2d42930fc57a3db1bd3282568a3952095f77539016a12437d59d7df5d` | **identical** |
| Published KiCad footprint | `Stamp-S3-SMD` / `-DIP` / `_PIN1.27_Socket` / `_PIN2.54_DIP` | **none** |

**One of these is wrong and M5Stack has not said which.** A 2 mm growth would break every host
PCB — and yet M5Stack ships the Stamp-S3A on a DinMeter carrier whose published PCB assets are
unchanged from v1.0. That argues the footprint did not grow and the `26.0` is a documentation
error. **`inferred`, not established.**

If you are laying out for a Stamp-S3A: measure a real part, or ask M5Stack. Do not trust either
number.

---

## 8. Does existing DinMeter firmware run unmodified?

**Yes — with one exception, and it is a silent one.**

| Aspect | Verdict | Basis |
|---|---|---|
| Toolchain / target | Identical: `esp32s3`, 8 MB flash, **no PSRAM** | **[DOC]**; Bruce/Launcher `build_unflags = -DBOARD_HAS_PSRAM` **[SRC]** |
| Board enum | Unchanged — v1.1 enumerates as `board_M5DinMeter`; M5Unified has no v1.1 or S3A variant | **[SRC]** master `8530f537…` |
| Display (ST7789, GPIO4-9, gap 52/40, `INVON`, 40 MHz) | Unchanged | **[DOC]**, carrier schematic |
| Rotary encoder (GPIO41/40) | Unchanged | **[DOC]**, **[SRC]** |
| Button / wake (GPIO42) | Unchanged | **[SRC]** `M5Unified.cpp:3502-3505` |
| Buzzer (GPIO3) | Unchanged | **[SRC]** `M5Unified.cpp:2921-2928` |
| RTC (BM8563, GPIO11/12, 0x51) | Unchanged | **[SRC]** `M5Unified.cpp:96` |
| PORT.A / PORT.B | Unchanged | **[SRC]** `M5Unified.cpp:96, 159` |
| Power hold (GPIO46) | Unchanged | **[SRC]** `M5Unified.cpp:282` |
| Battery ADC (GPIO10, ÷2) | Unchanged | **[SRC]** Bruce/Launcher `ANALOG_BAT_PIN=10`, *"ratio 2.0, matching M5Unified's board table"* |
| Boot / download (`G0` held at power-on) | Unchanged | **[DOC]** identical wording on both Stamp pages |
| Flash layout / partitions | Unchanged | no vendor change published |
| **RGB LED (GPIO21)** | **Silently dark without `GPIO38 = HIGH`** | §3 |
| Wi-Fi / BLE API | Unchanged; RF *performance* may differ | §4 |

**So: do not recompile anything.** A binary built for DinMeter v1.0 will boot and run on v1.1.
The only user-visible difference is that the Stamp's status LED stays off — which will read as
"the LED is broken", not as "the firmware is wrong", and that is precisely why it is worth
documenting loudly.

Conversely, firmware written for v1.1 with the GPIO38 line in it runs unchanged on v1.0, because
GPIO38 is unconnected on the older module's carrier path and driving it is harmless.

---

## 9. What this means for a buyer

- If you already own a DinMeter v1.0: **there is no reason to upgrade** unless you run on a
  battery and care about a 300 µA → 7 µA sleep improvement, which on a device that already
  latches its battery *off* at 38.4 µA is largely theoretical.
- If you are buying now: **v1.1 is the only option.** Both `K134` and `S007` are marked `[EOL]`
  and out of stock on `shop.m5stack.com` (2026-09-04).
- Price is unchanged at USD 24.50.
- If you are designing a *new* board around a Stamp module: use the S3A (the S3 is EOL), budget
  for **0.6 A** on the 3.3 V rail rather than 1 A, and add the GPIO38 line if you want the LED.

---

## Sources for this document

Full rows with class, retrieval date and what each establishes: [`sources.md`](sources.md) and
[`../dinmeter/sources.md`](../dinmeter/sources.md).

Component records: [`components/m5stack/stamp-s3`](../../../components/m5stack/stamp-s3/README.md) ·
[`components/m5stack/stamp-s3a`](../../../components/m5stack/stamp-s3a/README.md) ·
[`components/awinic/aw35122`](../../../components/awinic/aw35122/README.md) ·
[`components/sgmicro/sgm2578`](../../../components/sgmicro/sgm2578/README.md) ·
[`components/murata/mun3cad01-sc`](../../../components/murata/mun3cad01-sc/README.md) ·
[`components/unidentified/m5stack-stamp-s3a/dcdc-u4`](../../../components/unidentified/m5stack-stamp-s3a/dcdc-u4/README.md)
