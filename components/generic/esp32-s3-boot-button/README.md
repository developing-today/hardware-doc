# ESP32-S3 BOOT button

- **Category:** ESP32-S3 download-mode control
- **Reference designator on this board:** **none.** ⚠ **No button symbol appears in the five published schematic sheets.** What *is* in the schematic is the net it must pull down, and its pull-up resistor
- **Owning MCU:** **ESP32-S3** — GPIO0
- **Research status:** the button's *function* is stated by Waveshare; the *net* it acts on is now established by elimination from the schematic (§2). The button part, its debounce and its physical placement remain undocumented
- **Retrieved:** 2026-08-21; the `GPIO0` net traced across three sheets and its triple role identified 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. What Waveshare says

Waveshare identifies a control as the **ESP32-S3R8 BOOT button** and instructs users to **hold it while powering the device on to enter download mode** **[WEB]**.

That is the entire vendor statement. No pin, no net, no part number.

## 2. The net it must act on — established by elimination

On any ESP32-S3, download mode is entered by holding the **BOOT strapping pin, GPIO0**, low while `CHIP_PU` (reset) is released **[DOC, ESP32-S3 datasheet]**. There is no alternative mechanism.

The schematic shows the supporting circuitry for exactly that **[SCH]**:

| Element | Value | Sheet |
|---|---|---|
| `R58` — pull-up on `GPIO0` | **10 kΩ to 3V3** | 1 |
| `R57` — pull-up on `CHIP_PU` | **10 kΩ to 3V3** | 1 |
| `C8` — reset capacitor on `CHIP_PU` | **1 µF** | 2 |
| `GPIO0` alias | `I2S_SWITCH_IN` | 2 |

**Both pull-ups exist, both are in the standard 10 kΩ position, and neither has a switch drawn against it.** The pull-ups are exactly what a momentary-to-ground button needs on the other side.

So **[INF]**, with high confidence: **the BOOT button is a momentary switch from `GPIO0` to ground**, and the RESET/power control is a momentary switch from `CHIP_PU` to ground (see [generic/power-button](../power-button/README.md)). Neither switch is drawn, for the same reason the USB-C receptacle and the charger are not drawn — the published archive is incomplete.

`GPIO0` is additionally brought out to **`CN1` pin 8** **[SCH sheet 1]**, so the same function is available on the header. See [generic/ph1.27-expansion-connectors §3.3](../ph1.27-expansion-connectors/README.md#33-gpio0--pin-8-and-why-it-is-the-dangerous-one).

## 3. ⚠ GPIO0 has three jobs on this board

This is the interesting part, and it is specific to this design.

| Job | Detail | Evidence |
|---|---|---|
| **1. BOOT strapping pin** | Sampled at reset. Low → ROM download mode. Pulled up by `R58` 10 kΩ | [SCH], [DOC] |
| **2. `I2S_SWITCH_IN`** — the **CH445P audio multiplexer select** | Chooses whether the ESP32-S3 or the ESP32-U4WDH drives the PCM5100A DAC. `U18` pin 15 | [SCH sheets 2 and 5] |
| **3. Exposed on `CN1` pin 8** | Available on the expansion/interconnect header | [SCH sheet 1] |

**Consequences:**

- **Pressing BOOT at runtime switches the audio source.** It is not an inert button once the board has started; it is the mux select. If audio cuts out when someone presses BOOT, that is why.
- **The vendor's audio example drives GPIO0 high at startup** — `gpio_set_level(GPIO_NUM_0, 1)` with the comment *"give control of the PCM5100A to the ESP32-S3"* **[SRC `audio_bsp.c`]**. It also sets `GPIO_PULLUP_ENABLE` on the pin, redundantly with `R58`.
- **The power-on default audio routing is unverified.** `R58` holds GPIO0 high before firmware runs, but **which logic level selects which mux bank is unknown**, because no CH445P datasheet has been obtained. See [wch/ch445p](../../wch/ch445p/README.md) and [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md).
- **You cannot use GPIO0 as a free application input.** Any firmware that reads it as a "button" is also, unavoidably, driving the audio mux.

## 4. How to use it

### 4.1 Entering download mode

The reliable sequence on any ESP32-S3:

1. Hold **BOOT** (pull GPIO0 low)
2. Pulse **RESET** (`CHIP_PU`), or apply power
3. Release BOOT

Waveshare's instruction — hold BOOT while powering on **[WEB]** — is the same thing with power-on standing in for the reset pulse.

**On this board you usually do not need to.** The S3's native USB includes a ROM bootloader that `esptool` can reach without any button, and both the S3's ROM DFU and the USB-serial-JTAG path enumerate on their own. The button matters when:

- Your firmware crashes early, before USB enumerates
- Your firmware disables or reconfigures the native USB pins
- You have flashed something that hangs in `app_main`
- You need to recover from a bad OTA

That last set is exactly when you *most* need a recovery path, which is why the button is worth knowing about even though it is rarely used.

**Note there is no serial fallback for the S3.** Its UART0 is not routed to the USB bridge **[SCH]**; native USB is the only path. See [generic/usb-c-interface §4](../usb-c-interface/README.md#4-the-esp32-s3-side-native-usb).

### 4.2 Remember the USB-C orientation

**If `esptool` reports "ESP32" rather than "ESP32-S3", you are talking to the wrong processor** and no amount of BOOT-button pressing will help — the plug is the wrong way round. Rotate it 180°. See [generic/usb-c-interface §1](../usb-c-interface/README.md#1-the-behaviour--this-is-the-thing-to-know).

The BOOT button acts on the **ESP32-S3's** GPIO0 only. The **ESP32-U4WDH** has its own strapping pin (`ESP32_IO0`, package pin 23) which is driven automatically by the bridge's `DTR#` through `R14` 5.1 kΩ **[SCH sheet 3]** — no button needed, and no button available.

### 4.3 As an application button

You can read GPIO0 as a user button, subject to §3:

```c
gpio_config_t cfg = {
    .pin_bit_mask = 1ULL << GPIO_NUM_0,
    .mode         = GPIO_MODE_INPUT,
    .pull_up_en   = GPIO_PULLUP_DISABLE,   // R58 already does this
    .pull_down_en = GPIO_PULLDOWN_DISABLE,
    .intr_type    = GPIO_INTR_NEGEDGE,
};
gpio_config(&cfg);
// Active LOW. Debounce in software -- no hardware debounce is fitted.
```

**But do not**, unless you have accepted that reading it means you are no longer driving the audio mux, and that the mux will float to whatever `R58` gives it. On a board with a DAC shared between two processors, that is a poor trade. Use the touchscreen or a knob instead.

## 5. What remains unknown

| Unknown | Note |
|---|---|
| **Button part number** | No symbol in the schematic, therefore no BOM string |
| Physical type (tactile SMT? side-actuated? through a hole in the metal body?) | **Unknown** |
| Debounce components | **None are drawn.** `C8` 1 µF is on `CHIP_PU`, not on `GPIO0` **[SCH]**. **[INF]** GPIO0 has no hardware debounce — debounce in software if you read it |
| Physical placement and accessibility | **Unknown.** On a sealed metal knob this matters: the button may be recessed, or may require disassembly |
| Whether it is user-accessible at all | **Unknown** |
| Contact rating and cycle life | **Unknown** |

Every one of these is closed by a single board photograph.

## 6. Pitfalls

1. **GPIO0 is the audio mux select.** §3. This is the one that surprises people.
2. **No hardware debounce.** §5.
3. **Wrong-orientation USB makes the button appear not to work.** §4.2.
4. **The S3 has no UART fallback.** §4.1. If native USB will not enumerate and BOOT will not help, you are into JTAG or a reflash via the ROM DFU class.
5. **`CN1` pin 8 is the same net.** Anything you connect there is electrically in parallel with the button.
6. **Do not confuse this with the ESP32-U4WDH's boot strap.** Different pin, different chip, driven by the bridge rather than by a button. §4.2.
7. **Do not confuse it with the power button**, which acts on `CHIP_PU`. See [generic/power-button](../power-button/README.md).

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — acts on ESP32-S3 GPIO0

## Related pages

- [generic/power-button](../power-button/README.md) — the other button, acting on `CHIP_PU`
- [generic/usb-c-interface](../usb-c-interface/README.md) — the orientation quirk, and the S3's native-USB bootloader
- [wch/ch445p](../../wch/ch445p/README.md) — what GPIO0 also controls
- [generic/ph1.27-expansion-connectors](../ph1.27-expansion-connectors/README.md) — GPIO0 on `CN1` pin 8
- [development.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/development.md) — flashing workflow
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Waveshare product page — the "BOOT button, hold while powering on" instruction | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
| Board schematic sheet 1 — the pull-up bank containing `R57` (`CHIP_PU`) and `R58` (`GPIO0`), both 10 kΩ | — | 2026-08-21 | `.../artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Board schematic sheet 2 — `GPIO0` aliased to `I2S_SWITCH_IN`; `CHIP_PU` with `C8` 1 µF | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Board schematic sheet 5 — `I2S_SWITCH_IN` arriving at CH445P `U18` pin 15 | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/5_DAC.png` |
| Waveshare demo `07_Audio_Test` — `audio_bsp.c` drives GPIO0 high to claim the DAC | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/07_Audio_Test/` |
| ESP32-S3 datasheet — GPIO0 strapping behaviour and download mode | https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` |
