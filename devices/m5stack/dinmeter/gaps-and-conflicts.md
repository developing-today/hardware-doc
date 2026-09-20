# DinMeter — gaps, conflicts and unresolved identities

**Snapshot 2026-09-04.** Applies to K134 and K134-V11 unless stated. Conflicts are recorded, not
resolved by preference; each says what evidence would settle it.

---

## 1. ⚠ PORT.A / PORT.B wire colours — **unresolved**

**The claim in dispute:** which physical Grove wire carries which signal.

| Source | Class | Says |
|---|---|---|
| M5Stack DinMeter PinMap (both v1.0 and v1.1 pages) | primary | PORT.A `Yellow=G13, White=G15`; PORT.B `Yellow=G2, White=G1` |
| M5Stack **M5Dial** PinMap | primary | **the same table**, `Yellow=G13, White=G15` |
| DinMeter schematic, `PIJ30x`/`PIJ40x` markers | primary | `J3` pin1 = `IIC_SCL` → GPIO15, pin2 = `IIC_SDA` → GPIO13; `J4` pin1 = `GI` → GPIO1, pin2 = `GO` → GPIO2 |
| `M5Unified.cpp:96` | primary (framework) | `board_M5DinMeter`: **EX SCL = GPIO_NUM_15, EX SDA = GPIO_NUM_13** |
| `M5Unified.cpp:157-160` | primary (framework) | port-B table, comment `p1 close to 5V`, values `GPIO_NUM_1, GPIO_NUM_2` |
| `espressif/esp-board-manager` `board_peripherals.yaml` | community | "PORT.A (GPIO13 yellow / GPIO15 white) and PORT.B (GPIO2 yellow / GPIO1 white)" — **but its own header says `Source: M5Stack Din Meter official documentation (pin map)`**, so it is a *reproduction* of the disputed table, not corroboration |

**The analysis.** Under the Grove standard (connector pin 1 = yellow, pin 2 = white), the
schematic makes yellow = GPIO15 = SCL and white = GPIO13 = SDA — the opposite of the vendor
table. Every M5Stack PORT.A elsewhere is documented as *yellow = SCL, white = SDA*; if the
DinMeter really put SDA on yellow, a standard Grove I²C unit would receive SDA on its SCL pin
and nothing would work. Since Grove units demonstrably do work on M5Dial and DinMeter, the most
likely reading is that **the vendor table's Yellow/White columns are transposed**.

**Status: `inferred`, not established.** Two possibilities remain: (a) the table is wrong, or
(b) M5Stack's HY2.0 symbol numbers pin 1 at the black end, in which case the table is right and
the Grove-pin-1 assumption is wrong.

**Consequence:** *none* for anyone using M5Unified, UiFlow2 or a Grove cable — the software
drives the right pins and the cable is symmetric in the right way. It matters **only** for
hand-wiring to bare leads.

**What would settle it:** a photograph of the DinMeter's bundled pin sticker or rear silkscreen;
or M5Stack's PCB/Gerber files, which are not published.

---

## 2. ⚠ Three designators with no marker layer — **partly an extraction limit**

`S1`, `R20` and `Y1` appear as visible text on the schematic with **no `CO` and no `PI`
marker** anywhere in the document. Searched exhaustively in both single and double-struck glyph
forms; zero hits for `COS1`, `COR20`, `COY1`.

| Text | Position | Adjacent | Assessment |
|---|---|---|---|
| `S1` | (246.7, 242.9) | `SW-PB` 16.8 units below — the identical designator/part spacing that `S4` uses | A drawn WAKE push-button. **Not asserted as DNP** |
| `R20` | (249.3, 276.9) | `10 kΩ` below, on the RTC `INT` net | Almost certainly a real pull-up on `INT` |
| `Y1` | (163.8, 495.0) | immediately right of `SS8050` on the same baseline, under `COQ5`/`Q5` | **Probably not a designator at all** — `Y1` is the SOT-23 marking code for an SS8050 NPN |

**Context that matters:** ~20 `PI` markers are missing overall (238 recovered vs ~260 expected
for 84 parts), because Altium glues some markers to adjacent text in a way the parser's
negative-lookbehind rule — which is required to stop `GPIO0` parsing as a `PI` marker — must
discard. So an **extraction loss is the more likely explanation** for `S1` and `R20`.

**Not established.** Settled by a higher-fidelity PDF parse, or by a photograph of the board.

---

## 3. ⚠ M5Stack publishes v1.0 assets under v1.1 filenames — **established, and it is a finding**

| Asset | v1.0 URL | v1.1 URL | SHA-256 |
|---|---|---|---|
| Schematic | `…/500/DIN_Meter_v1.0.pdf` | `…/1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf` | **identical** `03ec3353…6e4c070` |
| Structure STL | `Products/K134_DinMeter/…/DinMeter.stl` | `Products/K134-V11_DinMeter_v1.1/…/DinMeter_v1.1.stl` | **identical** `90f04d6a…4aef00fbf7` |
| Dimension drawing | `…/1211/K134-din_meter_asm_v1.pdf` | **the same URL** | — |

The v1.1 schematic's own filename contains `_v1.0_`.

**What this licenses us to conclude:** M5Stack has published **no v1.1-specific board
documentation**. It does **not** prove the PCB is unchanged — it proves the *documentation* is.
The two boards could differ in ways no published document shows.

**What would settle it:** a v1.1 schematic, or a teardown photograph of a v1.1 PCB.

This is why this repository holds **one full record plus a scoped revision record**, rather than
two full records asserting differences the evidence cannot support.

Same pattern at module level: `Stamp-S3.stl` and `Stamp-S3A.stl` are byte-identical
(`f72c1af2…`), and `m5stack/M5_Hardware` publishes **no Stamp-S3A footprint** at all.

---

## 4. ⚠ ST7789P3 has no datasheet — **gap**

The DinMeter v1.1 page names `ST7789P3` in three places (Features, spec row, PinMap heading) and
**removes the display datasheet link** the v1.0 page had, replacing it with nothing. No ST7789P3
document was located from Sitronix or any mirror. The vendor's own v1.0↔v1.1 comparison table
does not mention the display at all.

Command-compatibility with ST7789V2 is **assumed** — same pins, same resolution, same driver
path, and M5Unified has no ST7789P3 branch. That is weak positive evidence, not verification.
See [`components/sitronix/st7789p3`](../../../components/sitronix/st7789p3/README.md).

**What would settle it:** an ST7789P3 datasheet, or a teardown photograph of a v1.1 unit's
controller marking.

---

## 5. ⚠ Stamp-S3A: 24 mm or 26 mm — **unresolved**

Vendor spec tables: Stamp-S3 = 24.0 × 18.0 × 4.7 mm, Stamp-S3A = **26.0** × 18.0 × 4.7 mm.
But the two published STLs are byte-identical and no new footprint was published — and M5Stack
ships the S3A on a DinMeter carrier whose published assets are unchanged. A 2 mm growth would be
a breaking change for any host PCB.

`inferred`: the `26.0` is probably a documentation error. **Not established.** Measure a real
part before laying out a board.

---

## 6. ⚠ Grove 5 V rail: 5.00 V or 5.38 V — **arithmetic conflict inside one M5Stack document**

The DinMeter spec row says the Grove rail is **DC 5 V** @ 220 mA. The schematic prints, beside
`U3` (SY7088 boost), the formula **`Vout = 1.2 V × (R1/R2 + 1)`**, and fits `R16` = 52.3 kΩ,
`R18` = 15 kΩ. That evaluates to **1.2 × (52.3/15 + 1) ≈ 5.38 V** — about 7.6 % high.

Both are primary M5Stack statements. Possible explanations: the divider is not the pair assumed
(nearest-neighbour value association could be wrong), the reference is not 1.2 V in practice, or
the rail really is ~5.38 V and the spec is rounded.

**Consequence:** real, if you are attaching a peripheral with a hard 5 V maximum to a Grove port.
**Measure the rail before connecting it.**

**What would settle it:** a multimeter on `J3` pin 3.

---

## 7. ⚠ No stable URL for the UiFlow2 firmware binary — **gap**

M5Stack distributes UiFlow2 and the DinMeter EasyLoader image through **M5Burner**, a desktop
application that resolves images at run time from an undocumented endpoint. No stable static
download URL for a DinMeter UiFlow2 or factory binary was located.

**Consequence:** the factory firmware cannot be archived here, and cannot be reacquired without
running M5Burner. See [`factory-firmware.md`](factory-firmware.md).

---

## 8. Untraced circuit: the `G14` / `G39` diode-OR network

Stamp pads 16 (`G14`) and 19 (`G39`) each sit on a 10 kΩ + 1N4148WT network (`R9`/`D7`,
`R10`/`D6`?) tied into the power-latch region. The most plausible reading is a diode-OR of wake
sources into the latch, but **the nets were not fully traced** in this pass and no vendor
document mentions either pin.

**Consequence:** GPIO14 and GPIO39 are documented in the vendor PinMap as free, but they are
**not** free — they have hardware on them. Do not repurpose them without tracing the circuit.

---

## 9. Sources searched with no result (negative findings, recorded so they are not re-chased)

| Question | Searched | Result |
|---|---|---|
| ESPHome support | `repo:esphome/esphome dinmeter` | **0** |
| Tasmota support | `repo:arendst/Tasmota dinmeter` | **0** |
| Meshtastic support | `repo:meshtastic/firmware dinmeter`, `din_meter` | **0** each |
| Bruce upstream support | `repo:pr3y/Bruce dinmeter` | **0** — the port lives in `bmorcelli/Launcher` |
| ME3116AM6G datasheet | web + aggregators | **not found** |
| SY7088 datasheet | web + aggregators | **not found** |
| BL8075 datasheet | web + aggregators | **not found** |
| SGM2578 datasheet | web + aggregators | **not found** |
| Stamp-S3A `U4` part number | schematic + vendor pages | **not printed anywhere** |
| Rotary encoder part number | schematic + both product pages | **not published** |
| Buzzer `LS1` part number | schematic + both product pages | **not published** |
| DinMeter teardown / bare-PCB photograph | image and web search | **none found** |
| AliExpress clones | marketplace search | **none found** |
| M5Stack forum threads | `community.m5stack.com` API + HTML | **HTTP 401 / JS shell — blocked, not empty** |

---

## 10. Confirmed-correct: things that were checked and found already right

Recorded so nobody re-investigates them.

| Claim | Verified against | Verdict |
|---|---|---|
| Encoder A = GPIO41, B = GPIO40 | schematic + `M5DinMeter.h:8-9` + `esp-board-manager` + Bruce | **correct**, four independent sources |
| Buzzer = GPIO3, **not** GPIO42 | schematic + `M5Unified.cpp:2921-2928` | **correct**; the vendor table's adjacent rows make this easy to misread, and Espressif's board file flags it explicitly |
| Power hold = GPIO46, active high | schematic + `M5Unified.cpp:282` + vendor Learn + `esp-board-manager` | **correct** |
| Display GRAM offset (52, 40), `INVON`, 40 MHz | M5Stack's own factory firmware + `esp-board-manager` + Bruce/Launcher | **correct**, three independent sources |
| Battery ADC on GPIO10, divider ratio 2.0 | schematic `R7`/`R8` 1 MΩ + 1 MΩ + Bruce/Launcher comment | **correct** |
| Internal I²C (RTC) ≠ external I²C (PORT.A) | schematic + `M5Unified.cpp:96` | **correct** |
| No PSRAM | vendor spec (`FN8`) + Bruce `build_unflags = -DBOARD_HAS_PSRAM` | **correct** |
| ESP32-S3 datasheet already in this repo | SHA-256 `b6db403d…` matches `components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet-v2.0-m5stack-mirror.pdf` | **duplicate — not re-added**, extra URL recorded instead |

---

## Related

[`../dinmeter-v1.1/gaps-and-conflicts.md`](../dinmeter-v1.1/gaps-and-conflicts.md) ·
[`research-log.md`](research-log.md) · [`sources.md`](sources.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md)
