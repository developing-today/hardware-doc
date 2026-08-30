# PH1.27 expansion connector `CN1` (10-pin)

- **Category:** board expansion interface
- **Reference designator on this board:** `CN1`
- **Part in the schematic BOM field:** `PM127-2-05-S-4.3` — a 1.27 mm-pitch, 2-row, 5-per-row (10-pin) header
- **Owning MCU:** **both, and the 5 V rail.** This one connector carries signals belonging to the ESP32-S3, to the USB-UART bridge that serves the ESP32-U4WDH, and to the analogue audio output
- **Research status:** ⚠ **The pinout is now fully resolved** (§2) — this supersedes an earlier decision not to publish it. **The count is not:** the vendor advertises *two* headers; only **one** appears in the schematic
- **Retrieved:** 2026-08-21; the `CN1` symbol re-read at 300% magnification and the pinout resolved 2026-08-23; **pinout independently re-derived from the raster and confirmed 2026-08-24** — see §2.1

## Evidence labelling

**[SCH]** schematic PNG · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. ⚠ Read this before connecting anything

`CN1` is **not** a general-purpose GPIO breakout. It carries:

- **Two USB differential pairs** — one belonging to the ESP32-S3's native USB, one belonging to the ESP32-U4WDH's USB-UART bridge
- **ESP32-S3 GPIO0**, which is simultaneously the S3's **BOOT strapping pin** and the **audio multiplexer select line**
- **The DAC's analogue line outputs**
- **5 V and GND**

Pulling any of the middle pins to a random level can drop the S3 into its bootloader, switch which processor owns the audio DAC, or damage a USB pair. **Verify by continuity before connecting anything**, and treat §2 as a strong hypothesis rather than a guarantee.

## 2. Pinout — resolved **[SCH sheet 1 `1_LCD&POWER.png`]**

The `CN1` symbol is drawn with pin numbers on both the symbol body and on each stub. At 300% magnification every stub is unambiguous:

| Pin | Net | What it is | Belongs to |
|---:|---|---|---|
| **1** | `5V` | 5 V rail | board power |
| **2** | `GND` | Ground | — |
| **3** | `USB_DN` | Native USB D− | **ESP32-S3** (GPIO19) |
| **4** | `USB_DP` | Native USB D+ | **ESP32-S3** (GPIO20) |
| **5** | `USB_ESP32_DP` | Bridge-side USB D+ | **USB-UART bridge `U10`** → ESP32-U4WDH |
| **6** | `USB_ESP32_DN` | Bridge-side USB D− | **USB-UART bridge `U10`** → ESP32-U4WDH |
| **7** | `GND` | Ground | — |
| **8** | `GPIO0` | **S3 BOOT strap *and* CH445P audio-mux select** | **ESP32-S3** |
| **9** | `OUTR` | DAC analogue right channel | **PCM5100A `U12` pin 7** |
| **10** | `OUTL` | DAC analogue left channel | **PCM5100A `U12` pin 6** |

**Layout convention:** odd pins on the top row, even on the bottom, with pin 1 marked by the usual dot on the symbol. Two grounds (2 and 7), sensibly placed to flank the USB pairs.

**This supersedes the earlier position** recorded in [pinouts-and-buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md), which declined to transcribe the numbering on the grounds that the raster was ambiguous. It is not ambiguous at sufficient magnification; the earlier caution was reasonable given the risk, and the caution in §1 still stands, but the reading itself is now clear.

**Remaining caveat:** a schematic symbol's pin numbering establishes the *net-to-pin-number* mapping. It does **not** establish which physical pin on the fitted header is pin 1, nor the row orientation as seen from above the assembled board. **Continuity-check before use.**

### 2.1 Independent confirmation, 2026-08-24

The table in §2 was **re-derived from scratch** in a later pass that deliberately did not consult this page first, as a check on a reading that had been flagged as risky. Method: the `CN1` region of `1_LCD&POWER.png` was cropped and upscaled 500×, then a second crop of just the symbol and its stubs was taken at 1000× (Lanczos, grayscale, normalised, sharpened).

The 1000× crop established the drawing convention that makes the reading safe: **each pin-number annotation sits immediately to the *left* of its own wire stub.** Once that offset is fixed, every stub can be assigned unambiguously:

| Read at 1000× | Terminates in |
|---|---|
| pin 1 stub | up, then left, to net label `5V` |
| pin 2 stub | down, then left, to a GND symbol |
| pin 3 stub | the **first** long vertical running up, vertical label `USB DN` |
| pin 5 stub | the **second** long vertical running up, vertical label `USB ESP32 DP` |
| pin 7 stub | up to the **higher** corner, then right to a GND symbol |
| pin 9 stub | up to the **lower** corner, then right to net label `OUTR` |
| pin 4 stub | the **first** long vertical running down, vertical label `USB DP` |
| pin 6 stub | the **second** long vertical running down, vertical label `USB ESP32 DN` |
| pin 8 stub | the **third** long vertical running down, vertical label `GPIO0` |
| pin 10 stub | down, then right, to net label `OUTL` |

**The result matches §2 pin-for-pin.** Two sanity checks also pass: each USB differential pair lands on a single odd/even column pair, and power and ground occupy column 1 — both are what a competent layout would do and neither was assumed during the read.

The device page [pinouts-and-buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md) has been updated to carry this pinout rather than continuing to decline to transcribe it. **The §1 warning still stands in full** — corroboration of the *schematic* reading does nothing to establish physical pin-1 orientation on the fitted part.

## 3. What each group is for

### 3.1 Power — pins 1, 2, 7

`5V` and two grounds. **Note what is absent: there is no 3.3 V pin.** You cannot power a 3.3 V accessory from this header without your own regulator — which is arguably the right decision given how tight the 3.3 V budget is ([tlv62569dbvt §5](../../texas-instruments/tlv62569dbvt/README.md#5-power-budget-for-the-33-v-rail)).

`5V` is the board's input rail. **How much current you can draw is unknown**, because the upstream source is unresolved — see [generic/charger-power-path](../charger-power-path/README.md). On USB power it is bounded by the port; on battery power it is bounded by an undocumented boost stage. **[INF]** Treat a few hundred milliamperes as the sensible ceiling and measure if it matters.

### 3.2 The two USB pairs — pins 3, 4, 5, 6

This is the most interesting thing on the connector. **Both** of the board's USB endpoints appear here:

| Pair | Endpoint |
|---|---|
| `USB_DP`/`USB_DN` (pins 4, 3) | ESP32-S3 **native USB** (GPIO20/GPIO19) — CDC, JTAG, DFU |
| `USB_ESP32_DP`/`USB_ESP32_DN` (pins 5, 6) | The **USB-UART bridge `U10`**, which fronts the ESP32-U4WDH's UART0 |

And critically: **no USB Type-C receptacle symbol appears anywhere in the five schematic sheets** **[SCH]**. Both pairs terminate *only* at `CN1`. See [generic/usb-c-interface](../usb-c-interface/README.md) for what that does and does not tell us.

**[INF]** The most likely explanation is that the USB-C receptacle and its orientation-selection circuitry live on a second, unpublished sheet or a separate flex/daughterboard, and that `CN1` is the interconnect between the main PCB and that assembly — i.e. **`CN1` may be an internal board-to-board connector rather than a user-facing expansion header.** The composition of the pinout supports this reading strongly: 5 V, ground, both USB pairs and the two audio outputs is exactly the signal set you would route to a connector/jack daughterboard. A general-purpose expansion header would carry I2C, SPI or spare GPIOs, and this carries none of them.

If that reading is right, **connecting to `CN1` while the USB-C assembly is also attached would put two drivers on the same USB pairs.** Another reason for the §1 warning.

### 3.3 GPIO0 — pin 8, and why it is the dangerous one

`GPIO0` on the ESP32-S3 is doing three jobs at once **[SCH]**:

1. **The BOOT strapping pin.** Held low at reset, the S3 enters download mode. `R58` 10 kΩ pulls it up to 3V3.
2. **`I2S_SWITCH_IN`** — the select input of the CH445P audio multiplexer (`U18` pin 15), which chooses whether the ESP32-S3 or the ESP32-U4WDH drives the PCM5100A **[SCH sheet 5]**.
3. **Exposed on `CN1` pin 8.**

So pulling `CN1` pin 8 low:

- **during reset** → the S3 enters the ROM bootloader
- **at any other time** → **switches which processor owns the audio DAC**

The vendor's own audio example drives GPIO0 **high** at startup with the comment *"give control of the PCM5100A to the ESP32-S3"* **[SRC `audio_bsp.c`]** — though note that which logic level selects which bank is itself unverified, because no CH445P datasheet has been obtained. See [wch/ch445p](../../wch/ch445p/README.md).

**Do not use `CN1` pin 8 as a general-purpose GPIO.** It has two other jobs.

### 3.4 The analogue audio outputs — pins 9, 10

`OUTL` and `OUTR` come directly from the PCM5100A's `OUTL` (pin 6) and `OUTR` (pin 7) **[SCH sheet 5]**.

These are **line-level, ground-centred** outputs. The PCM5100A family generates a negative rail internally (the `CPVDD`/`CAPP`/`CAPM`/`VNEG` charge pump, all populated here **[SCH]**), which is precisely why **no DC-blocking capacitors appear on `OUTL`/`OUTR`** — none are needed. Do not add them; you would only add a high-pass corner.

**There is no headphone amplifier anywhere on the board** **[SCH]**. See [generic/3.5mm-audio-output](../3.5mm-audio-output/README.md) for the loading consequences.

## 4. ⚠ The "two headers" discrepancy

Waveshare's product material advertises **two PH1.27 10-pin expansion headers** **[WEB]**.

**Only one 10-pin connector appears in the five published schematic sheets: `CN1`** **[SCH]**. All five sheets were searched.

Possible explanations, none confirmed **[INF]**:

1. The second header is on an unpublished sheet — consistent with the charger and the USB-C receptacle also being absent.
2. The second connector is the same physical part described twice in marketing (e.g. a header and its mating cable).
3. The product description is simply inaccurate.
4. The second header exists on a daughterboard.

This is tracked board-wide in [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md).

**Consequence:** if your board has two headers, **do not assume the second has the same pinout as `CN1`.** Continuity-map it.

## 5. Connector mechanics

| Property | Value | Evidence |
|---|---|---|
| BOM string | `PM127-2-05-S-4.3` | [SCH] |
| Pitch | **1.27 mm** (the `127`) | [INF] from the part string |
| Rows | **2** (the `-2-`) | [INF] |
| Positions per row | **5** (the `-05-`), so **10 pins total** | [INF], corroborated by the 10 numbered pins on the symbol |
| `S` | Straight (vertical) — **[INF]**, the usual meaning in this naming style | |
| `4.3` | Likely a height or pin-length variant in millimetres — **[INF]**, unconfirmed | |
| Manufacturer | **Unknown.** `PM127` is a generic series designation used by multiple Chinese connector vendors | |
| Gender (header vs socket) | **Unknown** from the schematic | |
| Current rating per contact | **Unknown.** 1.27 mm headers are typically rated 1 A per contact **[INF]**, but this is not established for this part | |

Note the naming mismatch: Waveshare calls it **PH1.27**, the schematic calls it **PM127**. "PH" is properly JST's 2.0 mm-pitch family name, so "PH1.27" is a vendor-marketing conflation rather than a real part family. **When sourcing a mating connector, go by the 1.27 mm pitch and 2×5 arrangement, not by the name.**

## 6. Pitfalls

1. **This is not a GPIO breakout.** §1. It exposes no I2C, SPI, UART or spare GPIO.
2. **It may be an internal board-to-board connector, not a user header.** §3.2. If a USB-C assembly is already mated to it, do not connect anything else.
3. **Pin 8 switches the audio mux and is a boot strap.** §3.3.
4. **No 3.3 V pin.** §3.1.
5. **The pinout in §2 is read from a raster.** Continuity-check first.
6. **"Two headers" is unverified.** §4.
7. **Two independent USB pairs on one connector** is unusual and easy to mis-wire. Getting `USB_DP` and `USB_ESP32_DP` crossed would put the S3's native USB against the bridge's.
8. **1.27 mm pitch is small.** Standard 2.54 mm jumper wires do not fit; you need a 1.27 mm IDC cable or a purpose-made harness.

## 7. Open questions

| Question | Status |
|---|---|
| **Is there a second 10-pin header?** | **Unresolved.** §4 |
| Is `CN1` user-facing or internal board-to-board? | **Unresolved.** §3.2 argues internal **[INF]** |
| Physical pin-1 location and row orientation on the assembled board | **Unknown.** §2 caveat |
| Connector manufacturer, gender, current rating | **Unknown.** §5 |
| Available current on the `5V` pin | **Unknown** — depends on the unresolved power path |
| Whether the second header (if it exists) shares this pinout | **Unknown** |

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `CN1`, the only 10-pin connector in the published schematic

## Related pages

- [generic/usb-c-interface](../usb-c-interface/README.md) — both USB pairs terminate here, and the receptacle is missing from the schematic
- [generic/3.5mm-audio-output](../3.5mm-audio-output/README.md) — `OUTL`/`OUTR` terminate here too
- [wch/ch445p](../../wch/ch445p/README.md) — what pin 8 controls
- [texas-instruments/pcm5100a](../../texas-instruments/pcm5100a/README.md) — the source of pins 9 and 10
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)
- [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Board schematic sheet 1 — the `CN1` `PM127-2-05-S-4.3` symbol, source of the §2 pinout | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Board schematic sheet 2 — `GPIO0` = `I2S_SWITCH_IN`, `USB_DP`/`USB_DN` = GPIO20/GPIO19, pull-up `R58` | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Board schematic sheet 3 — `USB_ESP32_DP`/`DN` at bridge `U10` | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/3_ESP32-CHIP.png` |
| Board schematic sheet 5 — `OUTL`/`OUTR` at PCM5100A `U12`, and `I2S_SWITCH_IN` at CH445P `U18` pin 15 | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/5_DAC.png` |
| Waveshare product page — the "two PH1.27 headers" claim | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
