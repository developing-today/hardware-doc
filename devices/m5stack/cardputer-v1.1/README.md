# M5Stack Cardputer v1.1 (K132-V11)

> **SKU `K132-V11`** · product id **`1127`** · Shopify `8741357388033`
> Launched **2025-03-07** · **marked `[EOL]` on M5Stack's own store as of 2026-09-04**, yet still
> listed at **$29.90** — the same price as the ADV that replaces it.
> Core module: **Stamp-S3A** (`Sch_StampS3_v0.3.3`). Research snapshot **2026-09-04**.

The middle Cardputer. It is a **module refresh of the v1.0, not a new board**: M5Stack publishes
the *same mainboard schematic file* for both, and its own comparison table lists only
module-level differences.

This record is deliberately lighter than the ADV's. Everything the two share — display, microSD,
IR, Grove, USB, power train — is documented once, in depth, at
[`../cardputer-adv/`](../cardputer-adv/README.md), and linked from here rather than repeated.

---

## Identity

| Field | Value | Evidence |
|---|---|---|
| Name | Cardputer v1.1 | product page |
| SKU | `K132-V11` | product page |
| Store title | **`[EOL]` M5Stack Cardputer with M5StampS3 v1.1** | Shopify, 2026-09-04 |
| Core module | **Stamp-S3A** | product page + comparison table |
| SoC | ESP32-S3FN8, 8 MB flash, **no PSRAM** | spec table |
| Mainboard schematic | `…/1127/Sch_M5Cardputer.pdf` — **byte-identical to the v1.0's** | SHA-256 `6016c1fe…`, 717 743 B |
| Base schematic | `…/1127/M5Cardputer_Base.pdf` — likewise identical | `29542fe1…`, 24 076 B |
| Size / weight | 84.0 × 54.0 × 19.7 mm, 90.0 g | spec table |
| Battery | **120 mAh internal + 1400 mAh in the base** | spec table |
| Includes | 1 × Cardputer v1.1, 1 × **1.5 mm** hex key (the v1.0 shipped a **2.0 mm** one) | product page |

## What actually changed from v1.0

M5Stack's own comparison table, verbatim in substance:

| | Cardputer v1.0 | **Cardputer v1.1** |
|---|---|---|
| Core module | StampS3 | **Stamp-S3A** |
| RGB LED control | "Powered immediately upon power-on" | "**shares power with screen backlight**, optimized control logic" |
| Antenna | standard | "optimized … better signal reception" |
| Boot key | 2.6 × 1.6 × 0.55 mm | **4.0 × 3.0 × 2.0 mm** |
| Power consumption | standard | "optimized for lower" |

Corroborated by the two Stamp schematics:

| | StampS3 `v0.2` | **Stamp-S3A `v0.3.3`** |
|---|---|---|
| 3.3 V rail | `M2` = **Murata `MUN3CAD01-SC` µPOL** 1 A power module | **JoulWatt `JW5712`** buck, 0–0.6 A, `VSEL` strapped |
| Load switch | **SGM2578** (U2) | **AW35122FDR** (U2), enabled by `DISP_BL` |
| **WS2812 supply** | **`VDD_3V3`** (always on) | **`BL_3V3`** (switched backlight rail) |
| Solder jumper JP4 at the WS2812 | present | removed |
| Crystal load caps | 12 pF / 10 pF | 12 pF / 12 pF |

Sleep current improves from **0.26 µA to 0.15 µA**; both figures are vendor claims under
unstated conditions.

## ⚠ The RGB LED / backlight interaction

Only the v1.1 page states it, and it applies verbatim to the ADV as well:

> "Since RGB and LCD backlight share the same power source, when the LCD backlight brightness is
> below 100%, RGB will not be powered properly. Please use the RGB function when the backlight is
> at full brightness."

Mechanism: G38 (`DISP_BL`) → **AW35122FDR** enable → `BL_3V3` → LCD backlight **and** WS2812.
PWM-dimming the backlight chops the LED's supply. On the **v1.0** the WS2812 sits on the
always-on `VDD_3V3` and this does not happen — so this is a *regression* introduced by the
Stamp-S3A, traded for the lower sleep current.

## The keyboard — 74HC138 GPIO matrix

The whole reason the ADV exists. See [`../cardputer-adv/features/keyboard.md`](../cardputer-adv/features/keyboard.md)
for the full comparison and the proof that the two matrices are electrically identical.

```
ESP32-S3 G8/G9/G11 ──► 74HC138 (U7) A0/A1/A2
                        /E1, /E2 → GND ;  E3 → +3.3V
                        Y0..Y7 ──► R34..R27 (22 Ω 1 %) ──► the 8-line Y bus
56 × SW-PB (S1..S56) matrix
7 sense lines ──► G13, G15, G3, G4, G5, G6, G7   (INPUT_PULLUP)
```

Read from the rendered sheet: U7 pin 1 = `A0` ← **G8**, pin 2 = `A1` ← **G9**,
pin 3 = `A2` ← **G11**, pins 4/5 = `/E1`,`/E2` → GND, pin 6 = `E3` → +3.3 V,
pin 7 = `Y7` → R27, pins 9–15 = `Y6..Y0` → R28…R34, pin 16 = `VCC`, pin 8 = `GND`.

Vendor driver, [`IOMatrix.cpp`](https://github.com/m5stack/M5Cardputer/blob/f1392858b9994c3547120e602a57d3553d16ab01/src/utility/Keyboard/KeyboardReader/IOMatrix.cpp):

```cpp
const std::vector<int> output_list = {8, 9, 11};                  // 74HC138 A0,A1,A2
const std::vector<int> input_list  = {13, 15, 3, 4, 5, 6, 7};     // 7 sense lines
const Chart_t X_map_chart[7] = {{1,0,1},{2,2,3},{4,4,5},{8,6,7},{16,8,9},{32,10,11},{64,12,13}};
…
for (int i = 0; i < 8; i++) { set_output(output_list, i); input_value = get_input(input_list); … }
coor.x = (i > 3) ? X_map_chart[j].x_1 : X_map_chart[j].x_2;
coor.y = (i > 3) ? (i - 4) : i;  coor.y = -coor.y + 3;
```

Scanning is **fully synchronous polling**: eight address settings per `update()`, seven
`digitalRead()`s each, no interrupt, no debounce hardware. Sense lines are `INPUT_PULLUP` and the
switch pulls low, so `pin_value = (digitalRead(pin) == 1) ? 0 : 1`.

**Cost: ten GPIOs**, which is why the v1.x has no expansion beyond the Grove port.

## Audio — NS4168 + SPM1423, no codec

| | v1.x | ADV |
|---|---|---|
| Speaker | **NS4168** I²S class-D → 8 Ω 1 W cavity | ES8311 codec + NS4150B |
| Mic | **SPM1423** PDM MEMS | analog MEMS via the codec ADC |
| 3.5 mm jack | **none** | present |
| I²S pins | G41 `BCLK`, G43 `LRCK`, G42 `SDATA`, G46 mic `DAT`, G43 mic `CLK` | same four pins |

M5Unified sets only `pin_data_in = G46` and `pin_ws = G43` for the mic on the v1.x — **no
`pin_bck`**, because a PDM microphone needs a clock and a data line, not a full I²S frame.
The ADV row adds `pin_bck = GPIO_NUM_41`.

Because the pins are the same, **v1.x audio code appears to "almost work" on an ADV**: the I²S
peripheral configures fine and nothing comes out, because the codec was never enabled.

Datasheets M5Stack links for this board: `SPM1423HM4H-B_datasheet_en.pdf`,
`NS4168_CN_datasheet.pdf` (Chinese only), `ST7789V2_SPEC_V1.0.pdf`. They file under the
components: [`knowles/spm1423hm4h-b`](../../../components/knowles/spm1423hm4h-b/README.md),
[`nsiway/ns4168`](../../../components/nsiway/ns4168/README.md),
[`sitronix/st7789v2`](../../../components/sitronix/st7789v2/README.md).

**The first two were filed and mined on 2026-09-20.** They are held at
[`components/knowles/spm1423hm4h-b/artifacts/spm1423hm4h-b-datasheet-rev-a-m5stack-mirror.pdf`](../../../components/knowles/spm1423hm4h-b/artifacts/spm1423hm4h-b-datasheet-rev-a-m5stack-mirror.pdf)
(1 272 831 B, `85ecd7d7…`) and
[`components/nsiway/ns4168/artifacts/ns4168-user-manual-v0.9-cn-m5stack-mirror.pdf`](../../../components/nsiway/ns4168/artifacts/ns4168-user-manual-v0.9-cn-m5stack-mirror.pdf)
(829 468 B, `479e75a1…`). Four things they establish that this record did not previously know
— all read from the datasheets plus a 400 dpi render of `Sch_M5Cardputer.pdf`:

| Finding | Consequence for this board |
|---|---|
| The microphone's designator is **`U5`**, not `M1` (`M1` is the **Stamp module footprint**) | corrects the component record |
| The mic's **`SELECT` pin is tied to `GND`** — the `Data_L` default | the PDM data is valid **after the falling `CLK` edge**; the host must sample that half-cycle. Not changeable in firmware |
| The amplifier's **`CTRL` pin is strapped to its own `VDD`** (+3.3 V behind ferrite `FB1`) | the speaker plays the **right** I²S channel; **shutdown is physically unreachable**, so the NS4168's quiescent draw cannot be removed in firmware; and its high-pass corner cannot be programmed |
| Series **33 Ω** resistors sit on all five audio lines (`R16`,`R17`,`R23`,`R24`,`R25`) | edge-rate damping; previously unrecorded |

⚠ **The mic's clock band is 1.0 – 3.25 MHz, and below 1 kHz it sleeps** — with the
1 kHz … 1 MHz band undefined by Knowles. Because `CLK` **is** the speaker's `LRCLK` (G43), an
active speaker parks the microphone squarely in that undefined band. That is the hardware reason
behind "one direction at a time", not merely a driver limitation. *(inferred; not measured.)*

⚠ **M5Stack's "1 W into 8 Ω" speaker figure is not supported by the NS4168 datasheet**, which
publishes 2.5 W at 5 V / 4 Ω and 1.2 W at 3.6 V / 4 Ω and **no 8 Ω figure at all** — and this
board runs the part at **3.3 V**. Recorded as an unresolved conflict in
[the component record §4.3](../../../components/nsiway/ns4168/README.md).

## Pin map

| Function | Pins |
|---|---|
| Keyboard drive (74HC138 A0/A1/A2) | G8, G9, G11 |
| Keyboard sense | G13, G15, G3, G4, G5, G6, G7 |
| Battery ADC | G10 |
| microSD | CS G12, MOSI G14, SCK G40, MISO G39 |
| Display | BL G38, RST G33, DC G34, MOSI G35, SCK G36, CS G37 |
| RGB LED | G21 |
| Speaker (NS4168) | BCLK G41, LRCLK G43, SDATA G42 |
| Mic (SPM1423) | CLK G43, DAT G46 |
| IR TX | G44 |
| Grove | G1, G2 |
| Boot | G0 |
| **Internal I²C** | **none** (`_pin_table_i2c_ex_in` = `255, 255`) |

Everything except the keyboard rows is identical to the ADV.

## Components

| Part | Designator | Record |
|---|---|---|
| 74HC138 | U7 | [`generic/74hc138`](../../../components/generic/74hc138/README.md) |
| NS4168 | **U6** | [`nsiway/ns4168`](../../../components/nsiway/ns4168/README.md) — ⚠ `CTRL` strapped to `VDD`: right channel, no shutdown. ⚠ manufacturer attribution unresolved |
| SPM1423HM4H-B | **U5** *(not `M1` — `M1` is the Stamp footprint)* | [`knowles/spm1423hm4h-b`](../../../components/knowles/spm1423hm4h-b/README.md) — `SELECT` tied low → falling-edge data |
| ST7789V2 | on the FPC | [`sitronix/st7789v2`](../../../components/sitronix/st7789v2/README.md) |
| ESP32-S3FN8 | in the module | [`espressif/esp32-s3fn8`](../../../components/espressif/esp32-s3fn8/README.md) |
| Stamp-S3A | module | [`m5stack/stamp-s3a`](../../../components/m5stack/stamp-s3a/README.md) |
| AW35122FDR / JW5712 / SGM2578 | on the module | [`awinic/aw35122`](../../../components/awinic/aw35122/README.md) · [`joulwatt/jw5712`](../../../components/joulwatt/jw5712/README.md) · [`sgmicro/sgm2578`](../../../components/sgmicro/sgm2578/README.md) |
| WS2812 | U3 on the module | [`worldsemi/ws2812`](../../../components/worldsemi/ws2812/README.md) |
| TP4057 / SY7088 / SY8089 / CN809J | U1 / U2 / U4 / U3 | [`generic/tp4057`](../../../components/generic/tp4057/README.md) · [`silergy/sy7088`](../../../components/silergy/sy7088/README.md) · [`silergy/sy8089`](../../../components/silergy/sy8089/README.md) · [`consonance/cn809`](../../../components/consonance/cn809/README.md) |
| LP3218DT1G | Q1–Q3 | [`unidentified/cardputer/lp3218dt1g`](../../../components/unidentified/cardputer/lp3218dt1g/README.md) |

## Development

Identical to the ADV — same PlatformIO profile, same download-mode procedure, same
`M5Cardputer` library, which autodetects and installs `IOMatrixKeyboardReader` instead.
See [`../cardputer-adv/development.md`](../cardputer-adv/development.md).

Factory firmware: `github.com/m5stack/M5Cardputer-UserDemo` **`main`** branch
(`a34d7ebcd508fb903a2b1123be8c8b54abd55d07`, 2026-07-17) — *not* the `CardputerADV` branch.
EasyLoader: `m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/core/Cardputer/Cardputer.exe`
(**shared with the v1.0** — a further instance of the vendor guide's "variant assets live under
the parent product" pattern).

## Community firmware

Broadest support of any Cardputer: Bruce, Launcher, Marauder, **Evil-M5Project**, NEMO,
MicroHydra and every emulator all target it. It loses upstream **Meshtastic** (ADV-only variant)
and every 2026 ADV-only project. Full matrix:
[`../cardputer-adv/compatibility-and-status.md`](../cardputer-adv/compatibility-and-status.md).

## Should you buy one?

**No, not at $29.90 with the ADV at the same price** — see
[`../cardputer-adv/comparisons-and-recommendations.md`](../cardputer-adv/comparisons-and-recommendations.md) §1.
The only defensible reasons are a firmware that has not been ported (Evil-M5Project's ADV
support is unconfirmed; NEMO has no ADV config) or a deliberate wish for the simpler,
fully-GPIO keyboard.

## Sources

Product page `https://docs.m5stack.com/en/core/Cardputer%20V1.1` (retrieved 2026-09-04,
snapshot at `artifacts/docs-en-core-Cardputer-V1.1.html`);
schematics `artifacts/schematic/` (`6016c1fe…`, `29542fe1…`);
`M5Cardputer` @ `f1392858`; `M5Unified` @ `8530f537`; Shopify `<handle>.json` 2026-09-04.
Full table: [`../cardputer-adv/sources.md`](../cardputer-adv/sources.md).
