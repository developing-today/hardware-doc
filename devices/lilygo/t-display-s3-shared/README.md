# LilyGO T-Display-S3 family — shared platform record

> **Not a product you can buy.** This is the hub for the T-Display-S3 *name*, which LilyGO
> applies to at least ten electrically distinct boards. It holds the material that is genuinely
> shared across them, the enumeration evidence, and the family-level findings.
>
> Research snapshot **2026-09-07** (host clock, corroborated by `updated_at` timestamps in
> LilyGO's own Shopify product feed). The task brief stated 2026-09-04; the three-day
> discrepancy is recorded in [`research-log.md`](research-log.md) and every retrieval date in
> this tree is the machine-verified one.

## Why this directory exists

Three separate things are shared and would otherwise be duplicated eleven times:

1. **`LilyGo-Display-IDF/main/product_pins.h`** — one header that carries the pin map for
   *nine* boards behind `CONFIG_LILYGO_*` switches. It is the single best cross-variant
   primary source in the whole family, and it belongs to no one board.
   → [`artifacts/originals/LilyGo-Display-IDF-product_pins.h`](artifacts/originals/LilyGo-Display-IDF-product_pins.h)
2. **The base-board schematic and factory firmware**, which cover the T-Display-S3 *and*
   T-Display-S3-Touch — LilyGO ships one schematic PDF for both.
   → [`artifacts/schematic/T_Display_S3.pdf`](artifacts/schematic/T_Display_S3.pdf)
3. **The family-wide traps** — the `USB CDC On Boot` trap, the Arduino-core version
   dependency, the parallel-8080/QSPI bus split. These recur on every board and are written
   once, here and in [`guides/hardware/parallel-8080-lcd-buses.md`](../../../guides/hardware/parallel-8080-lcd-buses.md).

Precedent: [`devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/`](../../waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md).

---

## 1. The confirmed family, enumerated from primary evidence

Enumerated by listing **every repository in the `Xinyuan-LilyGO` GitHub organisation**
(254 repos, captured 2026-09-07 →
[`artifacts/originals/xinyuan-lilygo-org-repos-2026-09-07.tsv`](artifacts/originals/xinyuan-lilygo-org-repos-2026-09-07.tsv))
and cross-checking against LilyGO's Shopify product feed
(`https://lilygo.cc/collections/all/products.json`, 214 products, same date).

**A board is listed as confirmed only when it has both a repository and a store listing, or a
repository containing a schematic naming it.**

| # | Board | One-line identity | Repo (commit) | Record | Depth |
|---|---|---|---|---|---|
| 1 | **T-Display-S3** | ESP32-S3R8 + 1.9″ 170×320 **ST7789V** on an **8-bit Intel-8080 parallel** bus; the reference board | `T-Display-S3` @ `ec889e7` | [`t-display-s3`](../t-display-s3/README.md) | **full** |
| 2 | **T-Display-S3 Touch** | Same PCB and schematic as #1, panel swapped for one with a bonded **CST816S** (later **CST328**) I²C touch controller | `T-Display-S3` @ `ec889e7` | [`t-display-s3-touch`](../t-display-s3-touch/README.md) | medium |
| 3 | **T-Display-S3 AMOLED** (1.91″) | ESP32-S3 + 240×536 **RM67162** AMOLED on **QSPI**; V1.0 and V2.0 PCBs sold side by side; touch/non-touch options | `T-Display-S3-AMOLED` @ `edd1333`, `LilyGo-AMOLED-Series` @ `6d1dc00` | [`t-display-s3-amoled`](../t-display-s3-amoled/README.md) | **full** |
| 4 | **T-Display-S3 AMOLED Plus** | Same 1.91″ RM67162 panel, **completely different power section**: TI **BQ25896** PMIC, **PCF85063ATL** RTC + Seiko **MS412FE** backup cell, microSD slot | `LilyGo-AMOLED-Series` @ `6d1dc00` | [`t-display-s3-amoled-plus`](../t-display-s3-amoled-plus/README.md) | medium |
| 5 | **T-Display-S3 AMOLED (DS) 1.64″** | 280×456 **CO5300 / ICNA3311** AMOLED, **FT3168** touch, **SY6970** PMIC | `T-Display-S3-AMOLED-1.64` @ `e236a4d` | [`t-display-s3-amoled-1-64`](../t-display-s3-amoled-1-64/README.md) | medium |
| 6 | **T-Display-S3 AMOLED (DS) 1.43″ / 1.75″** | Round 466×466 panels; 1.43″ = **SH8601 / CO5300** + FT3168, 1.75″ = **CO5300** + **CST9217**; adds **PCF8563** RTC | `T-Display-S3-AMOLED-1.43-1.75` @ `87aabe8` | [`t-display-s3-amoled-1-43-1-75`](../t-display-s3-amoled-1-43-1-75/README.md) | medium |
| 7 | **T4-S3** (the "AMOLED 2.41″") | 450×600 **RM690B0** AMOLED, **CST226SE** touch, **SY6970** PMIC, SPI microSD. Marketed as *T4-S3*, **not** as a T-Display-S3 | `LilyGo-AMOLED-Series` @ `6d1dc00` | [`t4-s3`](../t4-s3/README.md) | medium |
| 8 | **T-Display AMOLED Lite** (1.47″) | 194×368 **SH8501B** AMOLED behind an **RS0108** 1.8 V level shifter; **AXP2101** PMU; **CHSC5816** touch. Same library, different silicon generation | `LilyGo-AMOLED-Series` @ `6d1dc00` | [`t-display-amoled-lite`](../t-display-amoled-lite/README.md) | medium |
| 9 | **T-Display-S3 Long** | 3.4″ 180×640 bar display, **AXS15231B** (display **and** touch in one die) on QSPI; **SY6970** PMIC; hardware slide switch | `T-Display-S3-Long` @ `37a7e83` | [`t-display-s3-long`](../t-display-s3-long/README.md) | **full** |
| 10 | **T-Display-S3 Pro** | 2.33″ 222×480 **ST7796S** on **4-wire SPI** (not parallel), **CST226SE** touch, **SY6970** PMIC, microSD, camera FPC, 3 buttons | `T-Display-S3-Pro` @ `08b8b2b` | [`t-display-s3-pro`](../t-display-s3-pro/README.md) | **full** |
| 11 | **T-Display-S3 Pro MVSRBoard** | Backplate for #10: MAX98357A speaker amp, MSM261S4030H0R mic, PCF85063 RTC, vibration motor | `T-Display-S3-Pro-MVSRBoard` @ `c9c1a76` | [`t-display-s3-pro-mvsrboard`](../t-display-s3-pro-mvsrboard/README.md) | stub |

### Refuted or out of family

Recorded so nobody re-investigates them:

| Candidate from the brief | Verdict | Evidence |
|---|---|---|
| "T-Display-S3 AMOLED Touch" as a *separate product* | **Refuted as a distinct board.** It is a purchase option of #3. LilyGO's own resource table lists `T-Display-S3-AMOLED-Touch.pdf` as *the* schematic for both the touch and non-touch 1.91″ SKUs, and the library README states "This code supports T-Display-S3 AMOLED both touch and non-touch versions" | `LilyGo-AMOLED-Series` README.MD @ `6d1dc00`, §1 and §8 |
| "T-Display-S3 Cardputer-style" | **Refuted.** No such product or repo exists. LilyGO's keyboard handhelds are **T-Deck**, **T-Deck-Pro**, **T-Deck-MAX** and **T-Display-keyboard**, none of which carry the T-Display-S3 name or PCB | org repo listing; store feed |
| **T-Deck** family | **Out of family.** Separate PCB, separate repo, ESP32-S3 + LoRa + BlackBerry keyboard. Related only by vendor | `T-Deck` repo, 602★ |
| **T-Display** (ESP32), **T-QT**, **T-Dongle-S3**, **T-Display-S2**, **T-Display-RP2040**, **T-Display-GD32** | **Predecessors / cousins, not variants.** Kept as lineage stubs — see [`product-history-and-family.md`](product-history-and-family.md) | separate repos |
| **T-Display-C5 / P4 / K230 / SF32 / CM0** | **Successor line, different SoC.** The `T-Display-` prefix is being reused for ESP32-C5, ESP32-P4, Kendryte K230 and SiFli SF32. The K230 keyboard kit is documented separately at [`t-display-k230`](../t-display-k230/) by another agent | org repo listing |
| "AMOLED 2.41″" as a *T-Display-S3* | **Partially refuted.** The 2.41″ AMOLED board exists and is in the same library, but LilyGO sells and names it **T4-S3**. Calling it "T-Display-S3 AMOLED 2.41″" will not match any repo, SKU or board file | store handle `t4-s3`; `LilyGo-AMOLED-Series` README §1 |

---

## 2. What is actually shared, and what is not

The family name implies far more commonality than exists. This table is derived from the
schematics and board headers, not from marketing.

| Aspect | Shared across all? | Detail |
|---|---|---|
| SoC | **Yes, effectively** | **ESP32-S3R8** bare die (not a module) on every board in the table, 16 MB external NOR + 8 MB in-package OPI PSRAM. Only the 2023-era 1.91″ AMOLED schematic shows a **W25Q32** (4 MB) — see [§4 conflicts](#4-family-level-conflicts) |
| Flash part | Yes | Winbond **W25Q128JV**, 16 MB, QIO → [`components/winbond/w25q128jv`](../../../components/winbond/w25q128jv/README.md) |
| Display bus | **No — this is the big one** | 8-bit **Intel-8080 parallel** (base, Touch) · **QSPI** (all AMOLED, Long) · **4-wire SPI** (Pro) |
| Display controller | No | ST7789V · RM67162 · RM690B0 · SH8501B · SH8601 · CO5300 · AXS15231B · ST7796S — **eight** controllers |
| Touch controller | No | CST816S · CST328 · CST226SE · CST3530 · CST9217 · FT3168 · CHSC5816 · AXS15231B (integrated) |
| Charger / PMIC | **No** | **TP4065** (base, 1.91″ AMOLED) · **SY6970** (Long, Pro, T4-S3, 1.64/1.43/1.75) · **BQ25896** (AMOLED Plus) · **AXP2101** (AMOLED Lite) |
| Battery-sense pin | Mostly GPIO4 | GPIO4 on base, 1.91″ AMOLED, 1.43/1.64/1.75. **Not** on Long/Pro/T4-S3, which read the PMIC over I²C instead |
| `BOOT` button | Yes | GPIO0 on every board |
| Second button | GPIO14 (base) / GPIO21 (AMOLED) / GPIO0+12+16 (Pro) | Not portable |
| Arduino board target | **Yes** | `ESP32S3 Dev Module`, 16 MB flash, OPI PSRAM, `USB CDC On Boot = Enable`, partition `16M Flash (3M APP/9.9MB FATFS)` |
| The `USB CDC On Boot` trap | **Yes** | [§3.1](#31-the-usb-cdc-on-boot-trap) |
| Peripheral power-enable GPIO | **No** | GPIO15 on base/Touch **only**. Nothing equivalent on the AMOLED boards |

**Practical consequence.** Code written for the base T-Display-S3 will not run on any AMOLED
board without changing the display driver, the bus type, the button pins and the power
sequence. The only thing that ports unchanged is the Arduino board configuration. Treat
"T-Display-S3" as a *marketing prefix*, not a platform.

---

## 3. The three traps that catch almost everyone

Full write-ups live in the base-board record; the summaries are here because they apply to
every board in the table.

### 3.1 The `USB CDC On Boot` trap

**Symptom:** a board that appears completely dead — no serial output, or the sketch never
starts — until you connect it to a PC.

Every board here uses the ESP32-S3's **native USB** for both flashing and `Serial`. There is
no CH340/CP210x. When `USB CDC On Boot = Enable` (which LilyGO's own instructions require,
and PlatformIO sets via `-DARDUINO_USB_CDC_ON_BOOT=1`), `Serial` is the USB CDC device — and
the Arduino core **blocks at startup waiting for a host to open the port**. Run the same
firmware from a battery or a bench supply and it hangs before `setup()` finishes.

The fix is version-dependent and counter-intuitive, and it is documented in LilyGO's own FAQ:

```ini
build_flags =
    ; -DARDUINO_USB_CDC_ON_BOOT=1   ; prints to USB-C, BLOCKS on startup until a terminal attaches
    -UARDUINO_USB_CDC_ON_BOOT       ; no blocking on battery; Serial moves to GPIO43/44
```

> — `T-Display-S3/README.md` FAQ 5 @ `ec889e7`; `LilyGo-AMOLED-Series/README.MD` FAQ 4 @ `6d1dc00`

Disabling it moves `Serial` to **UART0 on GPIO43 (TX) / GPIO44 (RX)**, which on most of these
boards are broken out to the header — so you lose USB console but gain a working battery
device. Full treatment, including `USB Mode`, `Upload Mode` and the recovery ritual:
[`t-display-s3/features/usb.md`](../t-display-s3/features/usb.md).

### 3.2 The Arduino-core version dependency

LilyGO pins its test matrix and does not track the current core. From
`T-Display-S3/README.md` @ `ec889e7`:

> "The test phase uses version **2.0.14**. Versions above 2.0.14 may not work correctly —
> please downgrade if you encounter issues. As of 2024/08/02, **TFT_eSPI does not work on
> versions higher than 2.0.14**."

That is corroborated independently: the factory binaries in the repo carry
`arduino-lib-builder` app descriptors naming their ESP-IDF base, and the newest
(`t-display-s3-lvgl-demo-20250109`) is built on **ESP-IDF v4.4.6**, the base of
arduino-esp32 **2.0.14** — LilyGO has not rebuilt against a 3.x core.
Exact version table: [`t-display-s3/development.md`](../t-display-s3/development.md).

### 3.3 The display-bus split

`TFT_eSPI`, `Arduino_GFX` and `LovyanGFX` are **not** interchangeable here, and which one
works depends on the bus, not the board name.

| Bus | Boards | Recommended library | Why |
|---|---|---|---|
| 8-bit Intel-8080 parallel | T-Display-S3, Touch | **`TFT_eSPI` with `Setup206_LilyGo_T_Display_S3.h`** *or* `Arduino_GFX` `Arduino_ESP32LCD8` | TFT_eSPI needs a hand-edited `User_Setup_Select.h`; `Arduino_GFX` needs none |
| QSPI | all AMOLED, Long | **`Arduino_GFX`** or LilyGO's own `LilyGo-AMOLED-Series` | `TFT_eSPI` has no QSPI transport; it can only be used through a **Sprite** pushed by a vendor QSPI routine |
| 4-wire SPI | Pro | `Arduino_GFX` (LilyGO's choice) or `TFT_eSPI` | ordinary SPI, nothing special |

Detail and the failure modes: [`guides/hardware/parallel-8080-lcd-buses.md`](../../../guides/hardware/parallel-8080-lcd-buses.md)
(new, written by this pass) and the existing
[`guides/hardware/display-interfaces.md`](../../../guides/hardware/display-interfaces.md).

---

## 4. Family-level conflicts

Recorded, not resolved by preference. Per-board detail lives in each record's
`gaps-and-conflicts.md`.

| # | Conflict | Sources | Status |
|---|---|---|---|
| F1 | **The two "different" factory firmwares for the base board are byte-identical.** `firmware/t-display-s3-touch-20230417_0x0.bin` and `firmware/t-display-s3-no-touch-20231013_0x0.bin` both hash to `f288081645eecf7bf6a17fd7b5bc2e724121d00cdc2099b5a5ea7db5107eb9fa`, 1 601 328 B | measured locally 2026-09-07; user-reported in [issue #212](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/212) (2024-01-02) | **Confirmed by measurement.** The filenames and their two different dates are misleading |
| F2 | **Charger part mismatch on the base board.** Schematic sheet dated 2024-04-29 shows `U6 = TP4065` in an SOP-8-style symbol; an owner tracing a physical PCB found a **5-lead TSOT-23 marked `65b311`** | schematic `T_Display_S3.pdf`; [issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230) (2024-03-02, firsthand PCB inspection) | **Unresolved.** LilyGO never published a corrected sheet. The `65611`/`65b311` marking also appears as `AXPM65611` on three AMOLED schematics — see [§4.1](#41-the-65611-thread) |
| F3 | **1.91″ AMOLED flash size.** The 2023 `T-DISPLAY-S3-AMOLED.pdf` shows `U3 = W25Q32` (4 MB); every README and store listing says 16 MB; the newer `T-Display-S3-AMOLED-Touch.pdf` shows `U3 = W25Q128JV` | both schematics, this repo's `artifacts/` | **Probably a stale early sheet.** Treat 16 MB as correct for shipping boards but verify with `esptool.py flash_id` before assuming |
| F4 | **1.43/1.75″ resolution.** README says **466×466**; the board header says `LCD_WIDTH 473 / LCD_HEIGHT 467` | `T-Display-S3-AMOLED-1.43-1.75` README.md vs `components/private_library/pin_config.h`, both @ `87aabe8` | **Unresolved.** 473×467 is almost certainly the *driver window* (CO5300 addressable area) and 466×466 the visible circle |
| F5 | **Long board pin collisions in LilyGO's own header.** `examples/factory/pins_config.h` @ `37a7e83` defines `PIN_BAT_VOLT 2` while `TP_RST 2`, and `PIN_BUTTON_2 21` while `TFT_QSPI_D2 21` | single file, self-contradictory | **Confirmed defect.** Copy-paste residue from the AMOLED header. Do not use those two defines — see [`t-display-s3-long/gaps-and-conflicts.md`](../t-display-s3-long/gaps-and-conflicts.md) |
| F6 | **GPIO16/17 are not free on the non-touch base board.** LilyGO fits pull-ups on the back of the panel even where no touch controller exists | [issue #313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313) (2025-07-28), answered with PCB photos by LilyGO's own maintainer `lewisxhe` | **Confirmed by vendor** |

### 4.1 The `65611` thread

Worth flagging because it ties F2 together with the AMOLED boards. Three independent AMOLED
schematics — `T-Display-S3-AMOLED-Touch.pdf` (U5), `T-Display-S3-AMOLED-Plus.pdf` (U4) — carry
a part LilyGO writes as **`AXPM65611`** on a `VIN`-pin-12 symbol, and the base-board owner in
issue #230 read **`65b311`** off a 5-lead TSOT-23. No datasheet for either string was located
during this pass and no manufacturer could be identified from primary evidence.

**It is recorded as unidentified rather than guessed** —
[`components/unidentified/lilygo-t-display-s3-family/axpm65611/`](../../../components/unidentified/lilygo-t-display-s3-family/axpm65611/README.md)
states exactly what evidence would resolve it.

---

## 5. Shared artifacts held here

| File | Bytes | SHA-256 (first 16) | What it is |
|---|---|---|---|
| [`artifacts/schematic/T_Display_S3.pdf`](artifacts/schematic/T_Display_S3.pdf) | 395 064 | `607b6330063652 1f` | **The** base-board schematic, one sheet, title block dated **2024-04-29**. Covers T-Display-S3 and T-Display-S3-Touch |
| [`artifacts/schematic/SCH_T-Display-S3-MIDI_V1.1.pdf`](artifacts/schematic/SCH_T-Display-S3-MIDI_V1.1.pdf) | 693 393 | `c3d5651d79b933d0` | MIDI shield add-on schematic V1.1 |
| [`artifacts/originals/LilyGo-Display-IDF-product_pins.h`](artifacts/originals/LilyGo-Display-IDF-product_pins.h) | 13 544 | `c400cc8dcc1ccf28` | Nine boards' pin maps in one header, ESP-IDF side |
| [`artifacts/originals/xinyuan-lilygo-org-repos-2026-09-07.tsv`](artifacts/originals/xinyuan-lilygo-org-repos-2026-09-07.tsv) | — | — | The enumeration evidence: all 254 org repos with push dates |
| [`artifacts/originals/platformio.ini`](artifacts/originals/platformio.ini) · [`boards-lilygo-t-display-s3.json`](artifacts/originals/boards-lilygo-t-display-s3.json) | 7 981 / 855 | `d0ce207e8bdea5f3` / `529abb0314591c5f` | PlatformIO build definition and board manifest |
| [`artifacts/tft-espi/Setup206_LilyGo_T_Display_S3.h`](artifacts/tft-espi/Setup206_LilyGo_T_Display_S3.h) | 906 | `809949416716286a` | The `TFT_eSPI` user setup that must be selected by hand |
| `artifacts/firmware/*.bin` (6 files) | 489 616 – 1 601 328 | see [`../t-display-s3/factory-firmware.md`](../t-display-s3/factory-firmware.md) | Merged `0x0` factory images, ESP32-S3, decoded partition tables |

All retrieved 2026-09-07 from `raw.githubusercontent.com` at the pinned commits above.
Repository licence is **MIT** for `T-Display-S3`, `T-Display-S3-AMOLED` and
`LilyGo-AMOLED-Series`; **none declared** for `T-Display-S3-Long` and `T-Display-S3-Pro`;
**GPL-3.0** for the 1.64 and 1.43-1.75 repos. Vendor-mirrored *chip* datasheets are filed under
their component records, not here — see [`sources.md`](sources.md).

---

## 6. Documentation map

- [`product-history-and-family.md`](product-history-and-family.md) — the lineage from TTGO
  T-Display (2019) to T-Display-P4/K230 (2026), with dates
- [`sources.md`](sources.md) — full source table for the family-level claims
- [`research-log.md`](research-log.md) — queries, depth, dead ends, date discrepancy
- Per-board records — see [§1](#1-the-confirmed-family-enumerated-from-primary-evidence)
- [`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md) — how to find LilyGO
  documentation, and the traps in doing so
- [`guides/hardware/parallel-8080-lcd-buses.md`](../../../guides/hardware/parallel-8080-lcd-buses.md)
- [`guides/markets/clones-and-variants.md`](../../../guides/markets/clones-and-variants.md) —
  read for method; the T-Display-S3 worked example is in
  [`t-display-s3/comparisons-and-recommendations.md`](../t-display-s3/comparisons-and-recommendations.md)
