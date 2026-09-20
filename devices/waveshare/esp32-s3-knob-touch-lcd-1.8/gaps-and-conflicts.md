# Conflicts and unresolved gaps

Retrieved: 2026-08-21; dual-MCU items added and one S3 pin corrected 2026-08-22; inter-MCU baud, OTA and demo-coverage findings added 2026-08-22. These are evidence boundaries, not assumptions to fill.

## Dual-MCU and audio-path gaps

These arise specifically from the [two-MCU architecture](dual-mcu-architecture.md) and are the ones most likely to bite you in practice. Full context in [Dual-MCU architecture](dual-mcu-architecture.md) and on the [ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md).

| Topic | Evidence | Current conclusion |
|---|---|---|
| **ESP32-U4WDH core count and clock** | Espressif PCN-2021-021 (v1.3, 2021-09-02, effective 2021-12-02): the part was **single-core ECO V3 at 160 MHz** before that date and dual-core after. No Waveshare document, photo or firmware string identifies which is fitted | **Genuinely unresolved.** Do not assume dual-core or 240 MHz. Read `esp_chip_info().cores` at runtime, or `esptool chip_id` / `espefuse summary`. Design code that works either way |
| **Inter-MCU UART protocol** | Two wires, both sides on UART1. Framing shape reconstructed from log strings in both factory binaries: command field, transfer id, explicit length, multi-packet pull-based JPEG cover-art transfer, status frames. **No example in the entire demo archive uses the link**; Waveshare publishes no protocol description | **Byte format, field widths, delimiters and checksum are all unknown and are not guessed.** Sniff with a logic analyser, or reflash both MCUs and define your own protocol |
| **Inter-MCU UART baud rate** | Searched exhaustively 2026-08-22: every baud literal in the demo tree is a *console* baud (`CONFIG_ESP_CONSOLE_UART_BAUDRATE`, `CONFIG_MONITOR_BAUD`) in `sdkconfig` files, never in source. ESP-IDF does not log the configured baud, and the value reaches the hardware as a computed `UART_CLKDIV_REG` divider, so it is not recoverable from strings in either binary | **Unknown.** Do **not** assume 115200 — that is a different UART on a different peripheral instance. Obtain it by auto-bauding a logic analyser on S3 GPIO48/38, or by disassembling `../main/uart1.c` (ESP32) / `src/driver/uart1.cpp` (S3). See [Dual-MCU architecture §2.3.1](dual-mcu-architecture.md#231-the-configured-baud-rate-is-unknown) |
| **No ESP32-U4WDH source code, anywhere** | All 8 ESP-IDF demo projects set `CONFIG_IDF_TARGET="esp32s3"`; zero target `esp32`. No project, `main/`, `sdkconfig` or build file for the secondary MCU exists in the published archive | **Not a gap in our research — a gap in the product.** The Classic Bluetooth application exists publicly only as the prebuilt blob `ESP32-KNOB_ESP32_0.bin`. Back it up before overwriting; it cannot be rebuilt |
| **U4WDH `storage` SPIFFS contents** | The ESP32 partition table declares a 1408 KB `storage` (SPIFFS) partition at `0x1a0000`, but the published 1 130 672-byte image ends before it | **Unknown, and not recoverable from the published binary.** Only a full `esptool read_flash 0x0 0x400000` off a factory-state board captures it. Do this before your first write |
| **S3 OTA: capable but not implemented** | S3 partition table has `otadata` + `app0`(ota_0) + `app1`(ota_1), 3 MB each — genuinely OTA-capable. But the factory app has **no** `esp_https_ota`/`ArduinoOTA`/`Update.h` strings and its HTTP server exposes no `/update` or `/ota` URI | Not a conflict, but frequently misread. **The layout supports OTA; the shipped application does not perform it.** Your own S3 firmware can add it trivially. The U4WDH has `factory` only, no `otadata`, and no room for a second slot — **it is not OTA-capable at any layer**. See [Dual-MCU architecture §5](dual-mcu-architecture.md#5-ota-the-s3-can-the-u4wdh-cannot) |
| **CH445P truth table** | No CH445P datasheet obtained (see the [component record](../../../components/wch/ch445p/README.md)). Schematic shows `IN` = S3 GPIO0, `EN#` = GND, `S1` bank = ESP32-U4WDH, `S2` bank = ESP32-S3 | **Which `IN` logic level selects which bank is unknown.** S3 GPIO0 is also the BOOT strap with a 10 k pull-up, so the power-on default routing is likewise unknown. Measure it |
| **How S3-only audio gets past `XSMT`** | The PCM5100A soft-mute pin is driven by **ESP32-U4WDH GPIO32 only**, with no pull resistor and no S3 connection (sheets 3 and 5). Yet Waveshare's `07_Audio_Test` runs on the S3 alone and is documented to produce output | **Unresolved.** Either the PCM5100A's `XSMT` has an internal pull-up, or the factory ESP32 firmware un-mutes at boot, or the example only works with stock ESP32 firmware resident. Scope `XSMT`; test S3 audio with the U4WDH held in reset. **Practical mitigation: drive GPIO32 high in any replacement ESP32 firmware** |
| **DAC master clock** | CH445P channel D (`S1D`/`S2D`/`DD`) is unconnected on both banks | **No MCLK reaches the PCM5100A from either MCU.** The DAC must run in BCK-derived clocking mode. Not a conflict, but easy to get wrong |
| **`ESP32_IO2`, `IO4`, `IO21`, `IO33`** | Net-labelled on the U4WDH but with **no second endpoint anywhere in the five sheets** | Possibly test points or unrouted stubs. **These are the only candidate spare pins on the chip** and their availability is unresolved. Continuity-map before relying on them |
| **Second knob press contact** | `SW1` (`SSCM110100`) presents only `EC2_A` and `EC2_B` to the U4WDH | **There is no push/press contact wired from knob 2 to the secondary MCU.** Rotation only |
| **Bluetooth device name** | The string `BTAUDIOMATE` appears in the ESP32 factory image with no surrounding format specifier | Probably the advertised name; unconfirmed. Scan for the device from a phone |
| **ESP32-U4WDH ordering-suffix decoding** | The ESP32 datasheet PDF is archived and valid, but its text layer is glyph-subset encoded and the ordering-information table could not be extracted with available tooling | Only `4` = 4 MB embedded flash is established (corroborated by the bootloader flash-size nibble). `U`, `WD` and `H` are inferred, not documented |

## Board-wide gaps

| Topic | Evidence | Current conclusion |
|---|---|---|
| Display controller | Product says ST77916; official code/file/API names SH8601 and defines an unused `ID 0x86` | **Resolved 2026-08-26 — confidence raised from ~90 % to ~99 %.** Prior reasoning stands (`esp_lcd_sh8601` is a generic QSPI-DCS shim, `SH8601_ID` is dead code, the init table is textbook Sitronix, and the panel has a backlight so it cannot be an AMOLED). **New independent evidence:** ESPHome's device page for the pin-identical Guition JC3636K518C names the panel **"ST77916 driver 360×360"**, drives it with the generic `qspi_dbi` platform under `model: CUSTOM` — *not* an SH8601 driver — and its `init_sequence` opens `0xF0 0x28 / 0xF2 0x28 / 0x73 0xF0 / 0x7C 0xD1 / 0x83 0xE0 / 0x84 0x61`, **byte-for-byte the vendor demo's opening sequence**. `0xF0/0xF1/0xF2` command-page select with a `0xB0–0xC0` power/gamma block is the Sitronix idiom. GitHub code search finds `JC3636K518 + st77916` (1 hit) and `JC3636K518 + sh8601` (**0 hits**) — nobody in the wild associates this panel with SH8601. Controller is **ST77916**. See [ST77916 §2](../../../components/sitronix/st77916/README.md) and [esphome-and-clone-confirmation.md](./esphome-and-clone-confirmation.md) |
| Battery connector | Described as PH1.25 in some material and MX1.25 on wiki imagery | Measure pitch and verify polarity/keying physically |
| Haptic IC | Product/wiki shorthand DRV2605; schematic says DRV2605LDGSR | Document fitted part as DRV2605L |
| USB-UART bridge | Functional symbol `U10` only, no part number | **Resolved 2026-08-21: WCH CH340X**, MSOP-10, VID:PID `1A86:7523`. Decided by `R14` 5.1 kΩ between pin 6 and pin 5 = CH340 datasheet §5.3 option ②. CH9102F (QFN-24 only) and CH343P/K (wrong pin order) eliminated from their datasheets. **Do tell users to install the WCH CH34x driver.** See [USB-UART bridge record](../../../components/wch/ch340x/README.md) |
| Charger/power path | Product claims charging; identifiable complete charger block absent | Charge IC and safety behavior unknown |
| Audio wording | Called headphone jack; schematic has PCM5100A DAC but no headphone/speaker amp | Document as 3.5 mm stereo DAC line output; no onboard speaker |
| LCD module | No maker/module number/optical spec | Replacement not determined |
| LRA | No maker/model/electrical data | Tune/auto-calibrate fitted actuator; replacement unresolved |
| Antennas | `CA-C03` symbol only, on both `ANT1` (S3) and `ANT2` (U4WDH) | Exact antenna identity/gain unknown |
| Expansion headers | Advertised as two PH1.27 10P headers, but **only one 10-pin connector (`CN1`, `PM127-2-05-S-4.3`) appears in the five sheets**, and its pin numbering cannot be read unambiguously from the raster PNG. It carries 5 V, GND, **both** USB pairs, S3 GPIO0 (the audio mux select) and the DAC's `OUTL`/`OUTR` | Do not publish an inferred pinout. Given that this header carries USB and a mux-select line, verify by continuity before connecting anything |
| Schematics | Archive contains only five raster PNGs | No source schematic, BOM, Gerbers, PCB layout or mechanical CAD |
| USB-C | FAQ says plug orientation selects MCU. **No USB Type-C receptacle symbol appears anywhere in the five sheets**; both differential pairs terminate only at `CN1` | Behaviour is confirmed by the vendor and by the presence of two independent USB endpoints, but the switching topology is entirely unresolved |
| Product revisions | No PCB/BOM revision identifier | Findings apply to published files retrieved on this date |

## Schematic verification pass 2026-08-24

A dedicated pass re-read all five schematic sheets as tiled crops upscaled 6–14× (ImageMagick Lanczos, grayscale + normalise + sharpen), to settle four suspicions that a previous attempt had raised but could not confirm. **Three of the four came back negative.** Recording them here so the same ground is not re-covered.

| # | Suspicion under test | Verdict | Evidence actually read |
|---|---|---|---|
| 1 | The `BATT_ADC` divider senses **VBAT**, not the 5 V rail — which would have made this a correction affecting battery-monitoring code and every runtime estimate | **REFUTED. The existing docs were already right.** | Sheet `4_OTHER.png`, top-left, read at 600×. The divider's top net label is two glyphs, `5V`. Not `VBAT`, not `VSYS`. Topology verbatim: net `5V` → `R62` `10K` → junction dot with a wire left to net label `BATT_ADC` → `R63` `10K` → GND symbol. No edit was made to `pinouts-and-buses.md`, `lipo-102035`, `project-ideas.md` or `techniques.md`, because **none of them were wrong** |
| 2 | `U17` = ETA9740 power-path IC | **UNCONFIRMED — the designator does not exist in the published schematic** | See below |
| 3 | `U11` = SGM40561 charger IC | **UNCONFIRMED — likewise absent** | See below |
| 4 | `CN1` is now legible enough to publish a definitive pinout | **CONFIRMED** | Sheet `1_LCD&POWER.png` at 500× and again at 1000×, reading each pin-number annotation against its own wire stub. Matches the independently-derived pinout already published in [generic/ph1.27-expansion-connectors §2](../../../components/generic/ph1.27-expansion-connectors/README.md) pin-for-pin. `pinouts-and-buses.md` has been updated to carry it rather than continuing to decline |

### On `U11` and `U17`: they are not in the schematic at all

The reference designators actually present across the five sheets are **`U2`, `U3`, `U5`, `U10`, `U12`, `U13`, `U14`, `U18`, `U19`, `U20`** and no others. `U1`, `U4`, `U6`, `U7`, `U8`, `U9`, **`U11`**, `U15`, `U16` and **`U17`** appear nowhere.

The `ETA9740` and `SGM40561` names appear to have originated as *candidate leads* from [charger-power-path §3](../../../components/generic/charger-power-path/README.md), which is an explicitly-labelled checklist of parts to compare a top marking against — not a reading. (`SGM40561` is additionally very close to `SGM40567`, a charger that **is** documented in this tree but belongs to a different board entirely.) **No component records were created for either part.** Creating `components/etasolution/eta9740/` or `components/sgmicro/sgm40561/` on this evidence would have manufactured a false attribution.

This pass therefore **independently re-confirms** the central finding of the charger-power-path record: there is no charger, no power-path IC, no battery connector, no USB-C receptacle and **no source for the `5V` net** anywhere in the five published sheets. That record's conclusion — that Waveshare published an incomplete schematic and at least one power/charging sheet is missing — stands, and is now corroborated by a designator census rather than by block inspection alone.

### What the pass did add

All **[SCH]**, all newly published in [pinouts-and-buses](pinouts-and-buses.md):

- **`LCD_TE` carries an explicit `X` no-connect marker** on sheet 2, alongside its empty GPIO cell. The previous wording ("the alias table leaves its MCU GPIO blank, so its MCU connection is not established") understated this: it is a positive assertion of no-connect. **Tearing-effect synchronisation is unavailable on this board.**
- **`HAPTIC_EN` → 3V3 and `HAPTIC_TRIG` → GND.** The DRV2605L is permanently enabled and its trigger pin is hard-grounded, so it is I2C-controllable only. This was **already documented in [drv2605l §3/§3.1](../../../components/texas-instruments/drv2605l/README.md), and this pass independently re-derived it** — the gap was that the device-level GPIO page did not carry it, which is now fixed. Additionally corroborated by the absence of any `HAPTIC_EN`/`HAPTIC_TRIG` GPIO in Waveshare's demo sources.
- **The microSD card-detect switch (`CARD1` pin 9) is an explicit no-connect.**
- **`MIC1` pin 2 `L/R` is strapped to GND.**
- The CH445P's D channel (`MCK`) is unpopulated at **three** points, and `U12` pin 12 `SCK` carries no net — four independent confirmations of the existing "no MCLK" finding.
- SD pull-up designators `R10`/`R46`/`R47`/`R48`/`R49`, including one on `D3` that the GPIO table had omitted, and the fact that **the SD clock has no pull-up**.
- The power tree: `U19` TLV62569 feedback divider `R7` 100 k / `R8` 22.1 k; `U20` SGM2036 fed from `5V` through ferrite `L8` `BLM18AG102SN1D`; `A3V3` net-tied to `3V3_DAC` and `AGND` to `GND`.

**Both GPIO maps were re-checked entry-by-entry against the on-sheet alias tables. Not one assignment changed.**

### Still unreadable / still open after this pass

- The **`5V` net's source.** Not a legibility problem — it is genuinely not drawn. Unchanged from before; still resolvable only by a fuller schematic release or physical inspection.
- `L3` "24nH" at the ESP32-S3's `XTAL_P`/`XTAL_N` pins (sheet 2, package pins 54/53). The value and designator are legible; the **topology is not** — whether it is in series or across the crystal pins could not be established at the available raster resolution. Not published.
- Panel connector `U5`'s right-hand pins 10/16/18/20/22/24 appear tied together and probably to ground, but this was read at overview resolution only and is **not** published as fact.

## Corrections made to earlier revisions of these notes

| Item | Was | Is |
|---|---|---|
| ESP32-S3 GPIO0 | Described as a "CHIP_PU/USB selection-related net in connector block" | It is `I2S_SWITCH_IN`, the **CH445P audio mux select** (sheet 2 alias table → sheet 5 CH445P pin 15). It is additionally the S3 BOOT strap and is exposed on `CN1` |
| ESP32-U4WDH core count | Stated as "dual LX6 up to 240 MHz" in the device spec table | Unresolved — see the PCN caveat above |
| **Spectrum Analyzer app** *(corrected 2026-08-23)* | "Not confirmed to exist as a distinct app — no `spectrum`/`fft`/`vu` string found in the S3 image; may be a display mode" | **It exists.** Wiki §4.2.6 documents a "pickup spectrum analyzer" fed by the **PDM microphone**, so it is entirely ESP32-S3-local and does **not** use the inter-MCU UART. The negative string search was sound but misread: the shipped SD card carries a `fonts/` directory of **binary bitmap font blobs**, so this UI renders text from off-chip assets rather than firmware string tables — that search would have failed for *every* app name. See [factory-demo-apps.md §3.6](factory-demo-apps.md) |
| **Weather app** *(added 2026-08-23)* | Firmware strings `/saveweather`, `CityCode`, `apikey` recorded but no app confirmed | **A weather app exists and the wiki never documents it.** The shipped SD card carries a `weather/` directory of 19 condition graphics with day/night variants and a `nowifi` offline fallback. The wiki's §4 lists nine apps; this is a tenth. See [factory-demo-apps.md §3.10](factory-demo-apps.md) |

## Failed retrievals

- Immutable rendered wiki URL with `oldid=111069`: HTTP 404 on 2026-08-21. MediaWiki API metadata was retained and confirms revision date 2026-08-07.
- WCH CH445P manufacturer search/download attempts returned no usable PDF; a candidate endpoint returned JavaScript and was rejected. **This is what leaves the audio mux truth table unresolved.**
- Espressif PCN-2021-021 is published as HTML only; no PDF exists to archive. URL retained in the [ESP32-U4WDH sources table](../../../components/espressif/esp32-u4wdh/README.md#111-authoritative-sources).
- Espressif publishes no PDF build of the ESP-IDF programming guide for v5.3 or later, so the ESP32 factory firmware's exact IDF (v5.4-727) has no offline manual; v5.2.5 is stored as the closest available.
- Alps Alpine SSCM110100 manufacturer PDF catalog was downloaded and validated successfully.
- SGMicro direct SGM2036 PDF: HTTP 404. Manufacturer product/direct links retained.
- MSM261D4030H1CPM distributor PDF endpoint: returned HTML rather than PDF. Link retained; no substitute specifications invented.
- **(2026-08-23)** Guition clone vendor source `JC3636K518CN_knob_EN.zip` from `pan.jczn1688.com`: JS file-manager returns HTML; Cloudreve API paths 404. Needs a browser session. **This is what leaves the factory comprehensive-example source unavailable.**
- **(2026-08-23)** `nkinnan/manufacturer-firmware-and-sd-card-contents_Waveshare-ESP32-S3-Knob-Touch-LCD-1.8`: **empty repository** (`size: 0`, no branches). The Waveshare-specific SD dump was never pushed; only the Guition sibling has content.
- **(2026-08-23)** Waveshare wiki `api.php` and `action=raw`: broken server-side, PHP parse error — see the vendor-side regression note below.

## Open questions added 2026-08-23

| # | Question | Status |
|---|---|---|
| A | Which knob does the **HID Volume Control** app read — knob 1 (S3, would require UART relay) or knob 2 (U4WDH, self-contained)? | Unresolved. The wiki says only "the knob". A self-contained implementation on knob 2 is simpler and matches the layout, but that is inference only ([factory-demo-apps.md §3.9](factory-demo-apps.md)) |
| B | Which weather service does the undocumented weather app query, and where is `CityCode` set? | Unresolved. `apikey` implies a user-supplied keyed API; no string identifies the provider |
| C | Is the weather display a standalone launcher entry or a face of the Theme Clock? | Unresolved. The firmware groups `/clockbg` and `/saveweather` into one app, mildly favouring the latter |
| D | Is the Guition **JC3636K518** vendor source genuinely the same application as the Waveshare comprehensive example? | Unverified, and **we could not retrieve the archive**. If true it is the only public source for the factory UI. See [examples/catalog.md §1.1](examples/catalog.md) |
| E | Does the shipped SD card differ between the Waveshare unit and the Guition clone? | Unknown. Our directory listing is from a **clone** dump; directory names and roles are strong evidence, exact file lists only indicative |

## Vendor-side regression 2026-08-23

**The Waveshare wiki's MediaWiki API is broken.** Every `api.php` request returns
`Parse error: syntax error, unexpected '?' in /yundisk/web/waveshare/dotcom/w/includes/Setup.php on line 472`,
and `action=raw` returns the same. Rendered page views still work (HTTP 200).

This matters because on 2026-08-21 the API was the documented **workaround** for the WAF block on
`index.php?oldid=` — so **both routes to a pinned wiki revision are now unavailable**, and there is
currently no way to re-verify a revision ID or fetch clean wikitext from this vendor. The locally retained
`artifacts/source-snapshots/waveshare-wiki-wikitext-oldid-111069.txt` is the authoritative copy.
The live page was confirmed still at revision 111069 with byte-identical content on 2026-08-23.

## Needed to close gaps

A high-resolution board teardown with IC top markings (`U10`'s in particular, and the ESP32-U4WDH's **date code**, which settles the core-count question), continuity mapping of `CN1` and the battery connector, a logic-analyser capture of the inter-MCU UART, a CH445P datasheet, USB descriptor capture in both orientations, an LCD read-ID trace, and the complete Waveshare design package/BOM would resolve most open items.
