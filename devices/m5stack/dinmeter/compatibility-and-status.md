# DinMeter — compatibility and status

Keyed by hardware revision and software version. **No entry in this document is a firsthand
hardware test by this research pass** — none was possible. Every row states whose evidence it is.

Status vocabulary: **works** · **partial** · **fails** · **untested** · **conflicting**.

---

## 1. Framework and library versions

| Software | Version | K134 (Stamp-S3) | K134-V11 (Stamp-S3A) | Evidence |
|---|---|---|---|---|
| `M5DinMeter` | **1.0.0** (2024-03-07, the only release) | works | works | vendor-published; **no v1.1-specific changes** in the library, HEAD `8ccbad72…` still `version=1.0.0` |
| `M5Unified` | ≥ 0.1.13 declared; 0.2.21 current | works | works **except the RGB LED** | source read at master `8530f537…` |
| `M5GFX` | 0.2.28 current | works | works | via M5Unified |
| `LovyanGFX` | **1.1.12** (pinned by M5Stack's own factory project) | works | works | `M5DinMeter-UserDemo/platformio.ini` |
| `SmoothUIToolKit` | **1.0.1** (pinned by the same) | works | works | same |
| `mathertel/RotaryEncoder` | **1.5.3** | works | works | `bmorcelli/Launcher` board file |
| PlatformIO `espressif32` | **6.3.1** (pinned by M5Stack) | works | works | same |
| Arduino M5Stack board package | **2.1.1** (named in every vendor example header) | works | works | vendor examples, all dated 2024-03-07 |
| ESP-IDF + `esp-board-manager` | HEAD `2beb9b22…` (2026-09-03) | works | untested | Espressif board definition exists and is complete |
| UiFlow2 / `uiflow-micropython` | current | works | works | DinMeter in both CI configs |
| MicroPython (vanilla) | any | **not supported** | not supported | no board port upstream |
| `mattytrentini/chipboard` MicroPython | — | untested | untested | board YAML exists, not evaluated |

## 2. The one known incompatibility

| Item | Revision | Status | Detail |
|---|---|---|---|
| **RGB LED via stock M5Unified** | **K134-V11 only** | **fails (predicted)** | Stamp-S3A moves the WS2812B's supply onto the switched `BL_3V3` rail, gated by GPIO38. M5Unified at master `8530f537…` has no GPIO38 enable step for any board, no `board_M5StampS3A` and no v1.1 board enum, so a v1.1 unit takes the v1.0 code path and the LED stays dark. **`inferred` — not reproduced on hardware.** Workaround: `pinMode(38,OUTPUT); digitalWrite(38,HIGH);` before driving GPIO21 |

Everything else in the API surface is unchanged between revisions — see
[`../dinmeter-v1.1/stamp-s3-to-s3a-delta.md`](../dinmeter-v1.1/stamp-s3-to-s3a-delta.md) §8 for
the pin-by-pin verdict table.

## 3. Third-party firmware

| Project | Version/commit | Status | Evidence type |
|---|---|---|---|
| `bmorcelli/Launcher` | `main`, board `m5stack-dinmeter`, last push 2026-09-04 | **works** — in the release CI matrix and distributed as `Launcher-m5stack-dinmeter.bin` (MD5 `bccbefef5284357a2a7c3c7cc196fd98`) via M5Burner | demonstrable project. ⚠ **The project's own README contradicts itself**, listing the port once as `[x]` and once as `[ ] (Beta)`. The CI matrix and the MD5 map both say it ships |
| `viniciusbo/m5-palnagotchi` | last push 2026-01-28 | untested here; `palnagotchi/ui.h` references M5DinMeter | demonstrable project |
| `pr3y/Bruce` (upstream) | — | **no DinMeter support** — `repo:pr3y/Bruce dinmeter` → 0 results. Easy to confuse with Launcher | negative result |
| ESPHome / Tasmota / Meshtastic | any | **no support** — 0 code-search hits in each | negative result |

## 4. Peripherals reported working

| Peripheral | On | Status | Evidence |
|---|---|---|---|
| Grove I²C units on PORT.A | both | works | vendor design intent + `Ex_I2C` in the library |
| **SD card bit-banged across both Grove ports** | both | **works** | `bmorcelli/Launcher` ships it: `SDCARD_CS=13, SCK=15, MISO=2, MOSI=1`. Consumes all four free Grove pins |
| 250 mA·h bundled Li-ion cell | both | works | shipped in the box |
| Larger 1S Li-ion cells | both | untested | charger is 100 mA fixed; larger cells simply charge slower |

## 5. Known-bad and cautionary combinations

| Combination | Status | Why |
|---|---|---|
| Backlight and buzzer on the **same LEDC timer** | **fails** (visibly) | Channels on one timer share a frequency; retuning the buzzer changes backlight PWM. Espressif's board definition separates them (timer 0 / timer 1) |
| Pin-based JTAG + encoder | **fails** | GPIO39–42 are all occupied. Use USB-Serial-JTAG |
| Repurposing GPIO14 or GPIO39 | **risky** | The vendor PinMap implies they are free; the schematic shows 10 kΩ + 1N4148WT networks tied into the power latch. Circuit not fully traced |
| External pull-up on GPIO46 | **fails to boot** | Strapping pin, pulled down by design on the Stamp module |
| Enabling PSRAM in a build | **fails** | There is none, on either revision |
| Battery operation without setting GPIO46 high | **fails** | The board switches itself off. The single most common first-time failure |
| `esp-board-manager` PCNT with `en_step_notify_*` set | **build fails** | Those fields need `SOC_PCNT_SUPPORT_STEP_NOTIFY`, which the ESP32-S3 lacks. Espressif's own board file documents this |
| 36 V continuous on the DC terminal | **cautionary** | `C24` is rated 35 V — 103 % at the ceiling |
| 5 V-max peripheral on a Grove port | **cautionary** | The boost's divider computes to ≈ 5.38 V against a "5 V" spec |

## 6. Conflicting reports

| Item | Source A | Source B | Resolution |
|---|---|---|---|
| Backlight PWM frequency | M5Stack's own factory firmware: **200 Hz**, LEDC channel 7 | Espressif `esp-board-manager`: **5 kHz**, channel 0 / timer 0 | Both work. 200 Hz can be visible as flicker in person and on video. **Unresolved**; prefer 5 kHz |
| Grove wire colours | vendor PinMap: yellow = G13 | schematic + M5Unified: yellow = G15 (SCL) | **Unresolved.** No practical impact via M5Unified/UiFlow2. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §1 |
| Launcher DinMeter port maturity | README `[x] Port to M5-DinMeter` | README `[ ] (Beta) M5-DinMeter port` | The CI matrix builds it and the binary ships. Treat as **working, self-described as beta** |
| Stamp-S3A DC-DC | product page: `MUN3CAD01-SC` | schematic v0.3.3: an unidentified 8-ball buck + external inductor, `IOUT: 0~0.6A` | **Schematic wins.** The spec row was carried over unedited |
| Stamp-S3A length | spec table: 26.0 mm | STL byte-identical to Stamp-S3's, no new footprint | **Unresolved.** Probably a doc error; measure a real part |

## 7. What is untested, and it is nearly everything

| Category | Status |
|---|---|
| Any firmware built here | **none** |
| Any firmware flashed here | **none** |
| Any electrical measurement | **none** |
| Any RF measurement | **none** |
| Any thermal measurement | **none** |
| Any timing/throughput measurement | **none** |
| Any teardown / visual chip-marking confirmation | **none** |

**This record is a documentary and source-code analysis.** It is thorough about what can be
established from published documents, schematics and code, and it is worth exactly nothing as
evidence about how a physical unit behaves. Every claim is labelled accordingly.

If you have hardware, the five highest-value tests are listed in
[`coverage.md`](coverage.md) §4.
