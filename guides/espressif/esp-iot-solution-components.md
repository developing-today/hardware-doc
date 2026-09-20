# ESP-IoT-Solution components — knob, touch, LCD interfaces and USB

- **Purpose:** the component-level facts from the ESP-IoT-Solution User Guide that bear on the **[Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)** and the ESP32-S3/P4 display and USB work documented here, extracted before the 26.1 MB PDF was archived.
- **Extracted:** 2026-08-24

## Source

| Key | Document | Build | Pages | Regenerate from |
|---|---|---|---|---|
| **IOT** | *ESP-IoT-Solution User Guide*, Release `master` | dated **Jul 29, 2026**; PDF `CreationDate` 2026-07-29, server `Last-Modified` 2026-07-29 | 747 | `https://docs.espressif.com/projects/esp-iot-solution/en/latest/esp-iot-solution-en-master.pdf` |

Archive record, SHA-256 and URL verification: [`components/espressif/esp32-s3r8/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md`](../../components/espressif/esp32-s3r8/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md).

> **Moving-target caveat.** This is a `master`/`latest` build. The URL always serves the *current* master build; it will not reproduce this exact file indefinitely. At archiving time it served a byte-identical file (26 148 298 bytes). Page numbers are for **this** build.

Why this document is in the knowledge base at all: ESP-IoT-Solution is the official home of the ESP-IDF *component* drivers — QSPI LCD panels, touch controllers, knob/encoder input, LVGL porting — **none of which are documented in the core ESP-IDF Programming Guide**.

---

## 1. LCD driver-interface selection

The single most reusable table in the document. ESP-IoT-Solution § 4.1.1 *LCD Introduction* → *Driver Interface*, **p. 174**, compares IO count, data width / lane count, bandwidth and GRAM location:

| Type | Description | IO count | Data width / lane count | Bandwidth | GRAM location |
|---|---|---|---|---|---|
| **SPI** | Serial interface on the SPI bus protocol, typically 4-wire or 3-wire | **Minimum** | 1 | **Minimum** | LCD |
| **QSPI** (Quad-SPI) | Extension of SPI; parallel transmission over 4 data lines | Fewer | 4 | Smaller | LCD **or MCU** |
| **I80** (MCU, DBI) | Parallel interface on the I80 bus protocol | More | 8 / 16 | Larger | LCD |
| **RGB** (DPI) | Parallel interface, usually paired with a 3-wire SPI interface | **Maximum** | 8 / 16 / 18 / 24 | Larger | **MCU** |
| **MIPI-DSI** | Serial, differential; D-PHY high-speed low-power scalable serial interconnect | More | 1 / 2 / 3 / 4 lanes | **Maximum** | LCD or MCU |

Espressif's own summary (p. 175):

1. SPI bandwidth is small — suitable for **low-resolution** screens.
2. QSPI and I80 have larger bandwidth. **I80 requires the LCD to have built-in GRAM**, raising screen cost and making large screens hard.
3. RGB is like I80 but **does not require LCD GRAM**, so it suits higher-resolution screens.
4. **MIPI-DSI suits high-resolution, high-refresh-rate screens.**

### 1.1 Two gotchas worth knowing

> "For the **QSPI** interface, different models of driver ICs may adopt different driving methods. For example, the **SPD2010 has built-in GRAM**, and its driving method is similar to the SPI/I80 interface, while the **ST77903 does not have built-in GRAM**, and its driving method is similar to the RGB interface."
> — IOT § 4.1.1, p. 175

> "For the **MIPI-DSI** interface, the use of **Command mode requires the LCD to have built-in GRAM**, while **Video mode does not**."
> — same page

**This directly affects the ST77916 on the knob board** — a QSPI panel IC. Which of the two QSPI driving styles applies determines whether you need a framebuffer in MCU RAM. See [ST77916 component record](../../components/sitronix/st77916/README.md).

### 1.2 Driver IC model does not determine interface

> "The actual interface type of many LCD driver ICs is determined by the **logic levels of their `IM[3:0]` pins**. While most screens have these pin configurations fixed internally, some screens reserve these pins… **Therefore, knowing just the model of the driver IC is not sufficient to determine the interface type of the screen.** In such cases, you can consult the screen manufacturer, refer to the screen's datasheet, or use the schematic combined with experience."
> — IOT § 4.1.1, p. 175

Named examples of multi-interface ICs: **ST7789, GC9A01, ILI9341**. Also: "RGB LCDs usually also use the SPI interface" (for the command/init channel).

### 1.3 LCD module anatomy

§ 4.1.1 *Structure*, p. 172 — four parts: **Panel** (IPS/VA/TN; sets colour, viewing angle, resolution), **Backlight** ("its brightness can generally be controlled using PWM"), **Driver IC** (control circuit + driver circuit; "usually affixed at the connection point between the FPC and the panel"), **FPC**.

Other display sections worth knowing exist: *LCD Terms Table* (§ 4.1.2), *MIPI DSI LCD Detailed Guide* (§ 4.1.6, p. 209), *LCD Touch Support* (§ 4.1.7), **Detailed Explanation of LCD Screen Tearing** (§ 4.1.8, p. 224), *GUI Optimization Solutions* (§ 4.1.10, p. 235). LCD tooling components: **ESP LVGL ADAPTER** (§ 4.4.1, p. 250), **ESP LV DECODER** (p. 267), **ESP LV FS** (p. 269), **ESP MMAP ASSETS** (p. 271).

---

## 2. Touch panel support

### 2.1 Controllers with drivers *in ESP-IoT-Solution itself*

IOT § 9.4.1 *Supported Touch Controllers*, **p. 489**:

| Touch controller | Interface | Component name |
|---|---|---|
| ILI2118 | I2C | `esp_lcd_touch_ili2118` |
| **SPD2010** | I2C | `esp_lcd_touch_spd2010` |
| ST7123 | I2C | `esp_lcd_touch_st7123` |

### 2.2 Controllers supported elsewhere (ESP-IDF / ESP-BSP / Component Registry)

> "For additional touch controllers, please refer to the `esp_lcd_touch` drivers available on the **ESP Component Registry**. Common touch controllers supported by ESP-IDF and ESP-BSP include:
> - **GT911 / GT1151** — Capacitive touch controllers
> - **FT5x06 series (FT5216, FT5316, FT5436, FT6336)** — Capacitive
> - **CST816S** — Capacitive
> - **TT21100** — Capacitive"
> — IOT § 9.4.1, p. 489

> **Note for this knowledge base.** The knob board's touch controller is a **[CST816D](../../components/hynitron/cst816d/README.md)**. Espressif's list above names **CST816S** — a *different part number in the same Hynitron family*, so an `esp_lcd_touch_cst816s` driver is a plausible starting point but **not a documented match**; treat the substitution as unverified. Two further touch parts have artifacts retained here but no Espressif-maintained `esp_lcd_touch` driver on either list: **[CHSC5816](../../components/chipsemi/chsc5816/artifacts/)** (ChipSemi) and **[GT911](../../components/goodix/gt911/artifacts/)** (Goodix) — although GT911 *is* named in the ESP-IDF/ESP-BSP list above, so a driver exists for it in the Component Registry even though this tree holds only its datasheet.

### 2.3 The `esp_lcd_touch` abstraction

IOT § 9.4.2–9.4.3, p. 489:

- **Unified API** — same interface for all touch controllers
- **Easy integration** with LVGL and other GUI libraries
- **Hardware abstraction** — switch controllers without changing application code
- **I2C communication**

Capacitive panel features: multi-touch (controller-dependent), **"No calibration required (calibrated by controller)"**, gesture support (swipe/zoom/rotate, controller-dependent).

Configuration options: coordinate **mirroring** (X/Y), coordinate **swapping** (swap X and Y), interrupt pin, reset pin. (Also § 9.4.6 *Touch Rotation and Mirroring*, p. 492.)

Typical init pairs `esp_lcd_touch.h` + `esp_lcd_touch_<ic>.h` with `driver/i2c_master.h` and an `i2c_master_bus_config_t`.

---

## 3. Knob — software PCNT for rotary encoders

**This is the most directly applicable section to the knob board**, because the factory firmware uses exactly this component (`iot_knob_create`, `iot_knob_register_cb`) — see [ESP32-U4WDH § 5](../../components/espressif/esp32-u4wdh/README.md).

### 3.1 What it is, and its documented accuracy ceiling

> "Knob is the component that provides the **software PCNT**, it can be used on chips (esp32c2, esp32c3) that **do not have PCNT hardware capabilities**. By using knob you can quickly use a physical encoder, such as the EC11 encoder."
> — IOT § 9.3 *Knob*, p. 482

> "This is suitable for **low-speed** rotary knob counting scenarios where the pulse rate is **less than 30 pulses per second**, such as the EC11 encoder. It is suitable for scenarios where **100 % accuracy of pulse counting is not required**."
> — IOT § 9.3.1 *Applicable Scenarios*, p. 482

> ⚠ "For precise or fast pulse counting, please use the **hardware PCNT** function. The hardware PCNT is supported by **ESP32, ESP32-C6, ESP32-H2, ESP32-S2, ESP32-S3** chips."
> — IOT § 9.3.1 note, p. 482

**Consequence for the knob board.** Both MCUs on that board (**ESP32-S3** and **ESP32-U4WDH**) *do* have hardware PCNT, per Espressif's own list above. The factory firmware nevertheless uses the **software** `iot_knob` component, and therefore inherits its documented limits: a **~30 pulses/second** ceiling and **no guarantee of 100 % pulse accuracy**. If you rewrite that firmware and want fast-spin fidelity, moving to `driver/pulse_cnt.h` is the documented upgrade path — and it also gets you the hardware **glitch filter** and **watch points** described in [ESP-IDF peripheral capabilities § 6](esp-idf-peripheral-capabilities.md#pcnt-capability-summary-software-view).

This also bears on the board's *second* knob, the [Alps SSCM110100](../../components/alps-alpine/sscm110100/README.md) directional switch, which is decoded as if it were an A/B encoder.

### 3.2 Events

IOT § 9.3.3 *Knob Event*, p. 482 — five events per knob:

| Event | Trigger condition |
|---|---|
| `KNOB_LEFT` | Left |
| `KNOB_RIGHT` | Right |
| `KNOB_H_LIM` | Count reaches maximum limit |
| `KNOB_L_LIM` | Count reaches the minimum limit |
| `KNOB_ZERO` | Count back to 0 |

> "Each event of a knob can have a callback function registered for it… This approach is efficient and real-time, and **no events are lost**."
> ⚠ "**No blocking operations such as `TaskDelay` in the callback function.**"
> — IOT § 9.3.3, p. 482

### 3.3 Configuration

IOT § 9.3.4, p. 484:

| Item | Meaning |
|---|---|
| `KNOB_PERIOD_TIME_MS` | Scan cycle |
| `KNOB_DEBOUNCE_TICKS` | Number of de-shaking (debounce) ticks |
| `KNOB_HIGH_LIMIT` | Highest number the knob can count to |
| `KNOB_LOW_LIMIT` | Lowest number the knob can count to |

```c
knob_config_t cfg = {
    .default_direction = 0,
    .gpio_encoder_a    = GPIO_KNOB_A,
    .gpio_encoder_b    = GPIO_KNOB_B,
};
s_knob = iot_knob_create(&cfg);
```

API also includes `iot_knob_register_cb()`, `iot_knob_get_count_value()`, `iot_knob_clear_count_value()` (§ 9.3.8, p. 486), and explicit enable/disable (§ 9.3.7).

### 3.4 Low-power support — GPIO wake-up instead of `esp_timer`

> "In **light_sleep** mode, the `esp_timer` wakes up the CPU, resulting in **high power consumption**. The Knob component offers a low power solution through **GPIO level wake-up**. Required Configuration: Enable the **`enable_power_save`** option in `knob_config_t`."
> — IOT § 9.3.6 *Low Power Support*, p. 484

This is a real, non-obvious gotcha: a scanning software encoder defeats light sleep unless `enable_power_save` is set.

### 3.5 Related input components

- **Button** (§ 9.1, p. 463) — events documented at § 9.1.1, p. 464; configuration § 9.1.2, p. 465
- **Keyboard Scanning** (§ 9.2, p. 475) — matrix scanning with component events

---

## 4. USB peripherals

IOT § 5.1 *USB Host & Device*, pp. 279–316. Useful because it states the controller taxonomy plainly — complementing the counts in [ESP-IDF peripheral capabilities § 2](esp-idf-peripheral-capabilities.md#2-peripheral-instance-counts-stated-numerically-in-the-guide).

### 4.1 The three controller kinds

| Controller | Speeds | Protocol compatibility | Secondary development |
|---|---|---|---|
| **USB-OTG Full-Speed** | Full-speed **12 Mbps**, Low-speed **1.5 Mbps** | USB 1.1 and USB 2.0 | Yes — Host and Device stacks since **ESP-IDF 4.4** |
| **USB-OTG High-Speed** | High-speed **480 Mbps**, Full-speed 12 Mbps, Low-speed 1.5 Mbps | USB 2.0 | Yes |
| **USB-Serial-JTAG** | — | Firmware download, log printing, CDC transmission, JTAG debugging | ⚠ **No** — "Secondary development such as modifying USB functions or descriptors is **not supported**." |

All quotes IOT § 5.1.1–5.1.3, p. 280.

> "Starting from **ESP-IDF version 5.5**, the originally independent USB PHY implementation of **ESP32-P4** has been merged into the shared PHY module with **S2/S3**, unified driving structure, simplified maintenance."
> — IOT § 5.1.1, p. 280

That is a concrete migration note for P4 work: pre-5.5 P4 USB PHY code is on a separate code path.

### 4.2 Type-A electrical reference

IOT § 5.1.1, p. 280:

| Pin | Name | Cable colour | Description |
|---|---|---|---|
| 1 | VBUS | Red | +5 V |
| 2 | D− | White | Data− (0 or 3.3 V) |
| 3 | D+ | Green | Data+ (0 or 3.3 V) |
| 4 | GND | Black | Ground |

> "For **self-powered** devices, an additional IO is required to check the VBUS voltage, to detect whether the device is unplugged."
> "**Reversing the D− D+ connection will not damage the hardware**, but the host will be unable to recognize it."
> — IOT § 5.1.1, p. 280

### 4.3 Other USB material in the document

Guides: *USB VID and PID* (§ 5.1.5, p. 290), *Self-Powered USB Device Solutions* (§ 5.1.8, p. 296), *Prevent Windows from incrementing COM numbers based on USB device serial number* (§ 5.1.9, p. 298), *USB Signal Quality Test* (§ 5.1.10, p. 299), *TinyUSB Application Guide* (§ 5.1.11, p. 304), **USB Type-C Hardware Design Guide** (§ 5.1.13, p. 312).

Host drivers: USB Stream (§ 5.2.1), ESP MSC OTA (§ 5.2.2), USB Host CDC (§ 5.2.3), **USB RNDIS Host** (§ 5.2.4), USB PPP (§ 5.2.5), **USB ECM Host** (§ 5.2.6).
Device drivers: **UVC** (§ 5.3.1, p. 362), **UAC** (§ 5.3.2, p. 365), **ESP TinyUF2** (§ 5.3.3, p. 367).

---

## 5. Other sections relevant to hardware documented here

| Section | Page | Why it matters |
|---|---|---|
| **§ 11.1 ESP32-P4 Battery Backup Solution** | 499 | Battery connection and circuit protection, power switching, **Brown-out Detector & BOD filter**, charging circuit, and **"Peripheral Support in VBAT Power Supply Scenario"** (p. 504). Directly relevant to the battery-powered [ESP32-P4X-EYE](../../devices/espressif/esp32-p4x-eye/README.md) |
| § 2.1 Boards Component — `i2c_bus`, `spi_bus` | 7, 14 | Bus-abstraction helpers used by many of the sensor drivers in this tree |
| § 6.1 PWM Audio / § 6.2 DAC Audio / § 6.3 ADC Microphone | 373–382 | The "minimum" audio path when no codec is fitted; § 6.3 includes a **reference circuit** for an ADC microphone |
| § 12.1 Sensor Hub | 505 | Unified sensor-driver framework |
| § 4.3 LED Indicator | 241 | Blink types, **predefined blinking priorities**, gamma adjustment, drive-level setting |
| § 10.1 IR learn | 493 | RMT-based IR capture/replay |
| § 8.3 Xiaozhi AI Chatbot | 441 | Architecture of the widely-cloned ESP32 voice assistant |

---

## 6. Related records

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)
- [ESP32-S3R8 component record](../../components/espressif/esp32-s3r8/README.md)
- [ST77916 display controller](../../components/sitronix/st77916/README.md)
- [Alps SSCM110100 directional switch](../../components/alps-alpine/sscm110100/README.md)
- [ESP-IDF peripheral capabilities](esp-idf-peripheral-capabilities.md)
- [ESP-ADF audio pipelines](esp-adf-audio-pipelines.md)
- [Espressif vendor documentation-sourcing guide](../../vendors/espressif/README.md)
