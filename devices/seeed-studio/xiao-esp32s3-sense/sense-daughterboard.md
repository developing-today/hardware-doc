# Sense daughterboard — schematic analysis

> The camera / microphone / microSD board, reverse-engineered from Seeed's own EAGLE source.
> Snapshot **2026-08-24**. **This closes the single largest gap in this research tree.**

## 1. The file was hiding in plain sight

For most of this research pass the Sense daughterboard was treated as undocumented — [`gaps-and-conflicts.md` §6](gaps-and-conflicts.md#6-j3-board-to-board-pinout-is-undocumented--resolved-2026-08-24) recorded that Seeed publishes a schematic for the XIAO mainboard and for "the unrelated XIAO ESP32S3 Expansion Board accessory", but not for the sensor board.

**That was wrong.** The file published as **`XIAO_ESP32S3_ExpBoard_v1.0_SCH.pdf`** / `XIAO ESP32S3 Exp. Board v1.0.sch` **is the Sense daughterboard.** It contains a camera FPC connector, a microSD holder and a PDM microphone — not the OLED, RTC and buzzer of the separate "XIAO Expansion Board" accessory.

Two things concealed it:

1. **The name.** Seeed sells a genuinely different product called the *Seeeduino XIAO Expansion Board*. The names are close enough to look like duplicates.
2. **The PDF has no text layer.** It was exported from EAGLE 9.6.2 via Qt, which renders all text as vector paths — text extraction returns a single stray character. Anyone checking the PDF sees nothing.

The `.sch` inside the ZIP is **XML with an explicit `<nets>` section**, so it parses cleanly. Extracted with [`tools/eagle_netlist.py`](../../../tools/eagle_netlist.py).

> **Lesson:** when a vendor PDF yields no text, check whether the archive contains EDA source. EAGLE `.sch` is XML; unlike KiCad schematics it *states* the netlist rather than implying it geometrically.

## 2. What is on the board

**84 parts, 40 nets.** The functional inventory:

| Ref | Part | Function |
|---|---|---|
| **MIC1** | **`MSM261D3526H1CPM`** | **PDM microphone** — [component record](../../../components/memsensing/msm261d3526h1cpm/README.md) |
| **JA1** | `AFC01-S24FCC-00` | **24-pin FPC connector** — the camera module |
| **JA2** | `ST-TF-003D-3-2` (Seeed 320090495) | **microSD holder**, 8-pin short push-push |
| **JA3** | **`DF40HC(3.0)-30DS-0.4V(51)`** | **30-pin B2B socket** — mates the XIAO's `DF40C-30DP` plug |
| **U1** | `SGM2036S-2.8XXDH4G/TR` | **2.8 V LDO** — camera analog supply |
| **U2** | `SGM2036S-1.3XXDH4G/TR` | **1.3 V LDO** — camera core supply. ⚠ the schematic net is mislabelled `VCC_1V8`; see below |
| D1–D4 | `ESDPSA0402V05` | ESD protection on the SD lines |
| D5 | `ESD9B3.3ST5G` | ESD on the SD supply |
| D6 | `MSK4005` | Schottky, 2.8 V rail |
| FB1, FB2 | `120R-1.3A` | Ferrite beads — SD and camera supply isolation |
| JP1, JP2, JP3 | 2-pad jumpers | **Solder-selectable** mic CLK, mic DATA, SD supply |
| R11/R13/R15, R12/R14/R16 | DNP / 0 Ω pairs | **Configuration straps** |
| TP1–TP5 | test points | `VCC_IN`, `VCC_2V8`, `VCC_1V8`, `GND`, `AVCC_2V8` |
| J4, J5 | DNP header pads | On the PDM CLK / DATA nets |

## 2A. Physical layout (from the `.brd`)

Parsed from the EAGLE board file — **58 placed elements, 40 signals**.

| Property | Value |
|---|---|
| **Board outline** | **17.78 × 15.37 mm** |
| Layers | **4** — `Top`, `Route2`, `Route15`, `Bottom` |
| Placement | 20 components top, **38 bottom** |

The daughterboard is the **same width as the XIAO (17.78 mm) but shorter** (15.37 vs 21.14 mm), so it does not overhang.

Which side things are on matters for the modifications in §7:

| Component | Side | Note |
|---|---|---|
| **JA1** camera FPC | **TOP** | Faces away from the XIAO — the camera ribbon is accessible when assembled |
| **JA2** microSD holder | **TOP** | Card slot accessible when assembled |
| **MIC1** microphone | **TOP** | At the board edge (x ≈ 1.9 mm) |
| U1, U2 LDOs | TOP | |
| **JA3** B2B socket | **BOTTOM** | Mates down onto the XIAO |
| **JP1, JP2, JP3** solder jumpers | **BOTTOM** | ⚠ see below |
| **TP1–TP5** test points | **BOTTOM** | ⚠ see below |
| D1–D4 SD ESD arrays | BOTTOM | |

⚠ **The solder jumpers and test points are on the underside — the face that mates against the XIAO.** To cut JP1/JP2 (disconnecting the microphone) or probe TP1–TP5, **you must separate the two boards first**, and they are inaccessible while the device is assembled. That makes every modification in §7 a bench operation, not a field one.

## 3. Power — the camera needs three rails

The daughterboard generates its own supplies from the XIAO's 3.3 V:

```
VCC_IN (from B2B) ──┬── U1 SGM2036S-2.8  ──> VCC_2V8 ──FB2──> AVCC_2V8   (camera analog)
                    └── U2 SGM2036S-1.3  ──> "VCC_1V8" = actually 1.3 V   (camera core)

VCC_3V3 (B2B 12/13) ──┬── MIC1.VDD                                (microphone)
                      └── FB1 ──> VCC_SD_3V3 ──> JA2.VDD          (microSD)
```

This is a genuinely useful correction. [`pinouts-and-buses.md`](pinouts-and-buses.md) previously noted the stock board was *believed* to run the camera from 3V3. It does not: **the camera runs from locally regulated 2.8 V (analog) and 1.3 V (core)**, matching the OV-sensor requirement for 2.6–3.0 V analog and ~1.5 V core.

Consequences:

- **The camera is not directly powered from the XIAO's 3.3 V rail** — it sits behind two LDOs whose input is `VCC_IN`.
- **The microphone and the microSD *are*** on 3.3 V, the SD via ferrite bead FB1 and jumper JP3.
- Separate ferrite beads on the camera analog rail and the SD rail indicate deliberate supply isolation — the designer expected SD write bursts to inject noise.
- **This is where a camera power-switch modification would go**: `VCC_IN` feeding U1/U2 is a single controllable node, and both SGM2036S parts have `EN` pins currently tied to `VCC_IN`. Cutting that and driving `EN` from the spare GPIO3 would give the sensor power-down the board otherwise [architecturally lacks](pinouts-and-buses.md#31-there-is-no-camera-power-down-or-reset-line--and-that-has-consequences). **Untested inference**, but the design supports it.

### The `VCC_1V8` net name is wrong — vendor-confirmed

The schematic labels U2's output net **`VCC_1V8`**, but the fitted part is an **`SGM2036S-1.3`**, a **1.3 V** regulator. A forum user raised this and **Seeed confirmed the schematic is in error**:

> "We are using SGM2036S-1.3XXDH4G/TR at U2, which outputs **1.3V**. The network label (VCC_1V8) on the schematic is **incorrect and should be changed to 1V3**."
> — `Seeed_Seraphina`, [forum thread 273213](https://forum.seeedstudio.com/t/273213)

The camera's stated limits for that pin (min 1.24 V, typ 1.3 V, max 1.36 V) confirm 1.3 V is correct.

**Read every `VCC_1V8` in this document and in the schematic as 1.3 V.** See [`community.md` §4A.1](community.md#4a1-a-vendor-confirmed-schematic-error).

## 4. Camera FPC connector (JA1, 24-pin)

The pinout of the camera module's own ribbon — needed to substitute a non-Seeed sensor.

| Pin | Signal | | Pin | Signal |
|---:|---|---|---:|---|
| 2 | `GND` | | 14 | `DVP_Y8` (GPIO11) |
| 3 | `CAM_SDA` (GPIO40) | | 15 | `GND` |
| 4 | **`AVCC_2V8`** | | 16 | `DVP_Y7` (GPIO12) |
| 5 | `CAM_SCL` (GPIO39) | | 17 | `DVP_PCLK` (GPIO13) |
| 6 | *net N$7* (R9 10 kΩ pull-up to 3V3) | | 18 | `DVP_Y6` (GPIO14) |
| 7 | `DVP_VSYNC` (GPIO38) | | 19 | `DVP_Y2` (GPIO15) |
| 8 | *net N$10* (R10 10 kΩ pull-down) | | 20 | `DVP_Y5` (GPIO16) |
| 9 | `DVP_HREF` (GPIO47) | | 21 | `DVP_Y3` (GPIO17) |
| 10 | **`VCC_1V8`** ⚠ *actually 1.3 V* | | 22 | `DVP_Y4` (GPIO18) |
| 11 | **`VCC_2V8`** | | 23 | `GND` |
| 12 | `DVP_Y9` (GPIO48) | | 24 | *net N$8* (2.8 V via D6, C14/C15) |
| 13 | `XMCLK` (GPIO10) | | P1, P2 | `GND` (shell) |

**Pins 6 and 8 are the missing `PWDN` / `RESET` signals.** They are *not* routed to the ESP32-S3 — pin 6 is pulled **up** to 3.3 V through R9 (10 kΩ) and pin 8 pulled **down** through R10 (10 kΩ), permanently asserting the sensor's enabled, out-of-reset state.

This is the precise mechanism behind the "no camera reset" limitation. It is not that the sensor lacks the pins; it is that **the daughterboard hard-wires them to fixed levels**. A determined modification could lift R9/R10 and drive those pins from a spare GPIO.

## 5. microSD (JA2)

| SD pin | Net | Via | To |
|---|---|---|---|
| `CLK` | *N$4* | **R2 22 Ω** series, D3 ESD | `D8/SCK` → GPIO7 |
| `DO/D0` | *N$3* | **R1 22 Ω** series, D2 ESD, R4 4.7 kΩ pull-up | `D9/MISO` → GPIO8 |
| `DI/CMD` | *N$6* | **R3 22 Ω** series, D4 ESD, R5 4.7 kΩ pull-up | `D10/MOSI` → GPIO9 |
| `CS/D3` | `SD_CS` | R6 4.7 kΩ pull-up, D1 ESD | see below |
| `VDD` | `VCC_SD_3V3` | FB1 ferrite, D5 ESD, JP3 jumper | 3V3 |

Every SD line has **22 Ω series termination and an ESD diode** — a careful design.

### The GPIO3-vs-GPIO21 contradiction is now explained

[`features/microsd.md` §6](features/microsd.md#6-a-vendor-contradiction-is-cs-gpio21-or-gpio3) recorded that Seeed's wiki lists SD `CS` as GPIO3 in a table and GPIO21 in every code example. The daughterboard netlist resolves it:

```
SD_CS   ── R12 (0 Ω, fitted)  ── IO21/USER_LED   → B2B pad 15
        ── R11 (DNP)          ── D2/SD_CS        → B2B pad 29 (GPIO3)
```

**Both paths exist on the PCB.** `SD_CS` reaches GPIO21 through a fitted 0 Ω link (R12) and GPIO3 through an unpopulated position (R11).

So:
- **As shipped, `CS` is GPIO21** — GPIO21 is correct, and the code examples are right.
- **GPIO3 is a designed-in alternative.** Moving the 0 Ω from R12 to R11 relocates `CS` to GPIO3, **freeing GPIO21 and eliminating the [user-LED/SD collision](features/microsd.md#4-the-chip-select-collision) entirely.**
- The wiki's "GPIO3 → CS" table is not a typo. It documents the alternate configuration without saying so.

This is the most valuable single finding of the whole pass: **the board's worst design wart is fixable by moving one 0 Ω resistor.** Untested, but the intent is unambiguous in the netlist.

The same R13/R15 ↔ R16/R14 DNP/0 Ω pattern appears on the camera SCCB pull-ups and the `VIN` path, so strap-selectable configuration is a deliberate theme of this board.

## 6. Microphone (MIC1)

`VDD` on 3.3 V, `L/R` **tied to GND** (left channel — hence mono), and `CLK`/`DATA` reaching the B2B connector through **solder jumpers JP1 and JP2**.

**Cutting JP1 and JP2 isolates the microphone** and frees GPIO42/GPIO41 — which are `MTMS` and `MTDI`, half the JTAG port. Combined with the FCC finding that [the mainboard breaks all four JTAG pins out as labelled bottom-side pads](regulatory-and-certification.md#31-the-jtag-pins-are-broken-out-as-labelled-bottom-side-pads), the "no JTAG with the daughterboard" limitation is **less absolute than previously documented** — it is a fitted-strap consequence, not an architectural one.

## 7. Board-to-board socket (JA3) — cross-check

The daughterboard's `DF40HC(3.0)-30DS-0.4V(51)` socket mates the mainboard's `DF40C-30DP-0.4V(51)` plug. Its net assignment **independently confirms** the [J3 pinout reconstructed from the mainboard PCB](pinouts-and-buses.md#2-the-j3-board-to-board-connector-sense-daughterboard-interface) — two separate design files, in different EDA tools, from different years, agree.

One difference worth noting: the daughterboard numbers its socket pins in the **reverse** order to the mainboard plug (socket pad 4 = `PDM_CLK` where the plug's pad 27 carries it), which is normal for mated B2B pairs but will confuse anyone probing both sides.

`VIN` appears on JA3 pads 1 and 16; `VCC_3V3` on 12 and 13.

## 8. What this changes elsewhere

| Document | Correction |
|---|---|
| [`gaps-and-conflicts.md` §6](gaps-and-conflicts.md) | Daughterboard **is** documented — gap closed |
| [`gaps-and-conflicts.md` §7](gaps-and-conflicts.md) | Microphone **identified** — gap closed |
| [`features/microsd.md` §6](features/microsd.md) | GPIO3/GPIO21 contradiction **explained** — both are real |
| [`features/camera.md` §3.1](features/camera.md) | `PWDN`/`RESET` exist on the FPC but are **strapped**, not absent |
| [`pinouts-and-buses.md` §8](pinouts-and-buses.md) | Camera runs on **local 2.8 V / 1.3 V LDOs**, not 3V3 |
| [`features/microphone.md`](features/microphone.md) | Mono because **`L/R` is grounded**; JP1/JP2 make it removable |

## 9. Artifacts

- [`artifacts/extracted/xiao-esp32s3-expansion-board-v1.0-sch-pcb/XIAO ESP32S3 Exp. Board v1.0.sch`](artifacts/extracted/) — EAGLE 9.6.2 XML, the source for everything above
- `…/XIAO ESP32S3 Exp. Board v1.0.brd` — PCB layout, **not yet parsed**
- [`artifacts/schematics/xiao-esp32s3-expansion-board-v1.0-sch.pdf`](artifacts/schematics/xiao-esp32s3-expansion-board-v1.0-sch.pdf) — the text-layer-free PDF
- [`tools/eagle_netlist.py`](../../../tools/eagle_netlist.py) — the parser

## 10. Still unknown

- **Camera module internals** — the module beyond JA1 is a sealed assembly; the sensor die and its own passives are not in this schematic.
- **The `.brd` file is unparsed** — would give physical placement and the daughterboard outline.
- **Board revision** — this is "v1.0" dated 2023-03-24. Whether current Sense boards ship a revised daughterboard is **unestablished**, and matters because the OV2640→OV3660 sensor change happened later.
- **The separate OLED/RTC "XIAO Expansion Board" accessory** remains genuinely undocumented here.

## 11. Related
- [MSM261D3526H1CPM](../../../components/memsensing/msm261d3526h1cpm/README.md) · [DF40C-30DP-0.4V](../../../components/hirose/df40c-30dp-0.4v/README.md) · [OV3660](../../../components/omnivision/ov3660/README.md)
- [`pinouts-and-buses.md`](pinouts-and-buses.md) · [`regulatory-and-certification.md`](regulatory-and-certification.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
