# WCH CH32V203C8T6

> 32-bit RISC-V microcontroller, LQFP-48. Used as a always-on management coprocessor.
> Manufacturer: **WCH (Nanjing Qinheng Microelectronics)** · Research snapshot **2026-08-24**

## Function and capabilities

| Property | Value |
|---|---|
| Core | 32-bit **RISC-V** (WCH "V4B"), single core |
| Max clock | **144 MHz** |
| SRAM | **20 KB** |
| Flash | **64 KB** |
| Package | **LQFP-48**, 7 × 7 mm, 0.5 mm pitch |
| Family | CH32V203 (CH32V20x series) |
| LCSC | [`C3001172`](https://www.lcsc.com/search?q=C3001172) |

Datasheet: <https://www.wch-ic.com/downloads/CH32V203DS0_PDF.html>

The CH32V20x line is WCH's low-cost general-purpose RISC-V family — broadly an STM32F103-class part in capability and pinout philosophy, at a considerably lower price. It has the usual peripheral set: multiple I2C, SPI and USART, timers with PWM, ADC, and USB.

Two characteristics make it attractive specifically as a **management coprocessor**:

- **Very low standby power**, so it can be left permanently powered on a battery-backed rail.
- **RVSWD** programming — a two-wire debug/programming interface that can be driven by another microcontroller, so the part can be reflashed in-system without a dedicated programmer.

## Programming and toolchain

| Route | Notes |
|---|---|
| **`ch32v003fun`** | Minimal open-source bare-metal framework. Despite the name it supports CH32V20x/V30x, not just the V003. This is what the Tanmatsu coprocessor firmware builds against |
| WCH MounRiver Studio | Vendor IDE (Eclipse-based) |
| **RVSWD from a host MCU** | See below — the interesting option |
| WCH-LinkE | Vendor USB programmer/debugger |

### Reflashing from another microcontroller

Nicolai Electronics developed an ESP-IDF component that reprograms **CH32V20x and CH32V30x** parts over RVSWD directly from an ESP32:

**[`nicolaielectronics/rvswd`](https://components.espressif.com/components/nicolaielectronics/rvswd)**

This is worth knowing about independently of any particular product: it means a CH32V203 used as a coprocessor does not need a programming header, and its firmware can be shipped as part of the host processor's update mechanism.

⚠ **The obvious hazard:** if the coprocessor controls power sequencing, bad coprocessor firmware is far more serious than bad application firmware — there is no ROM-bootloader safety net for the power controller. Nicolai Electronics' own guidance for Tanmatsu is that modifying it "is of course possible but is not recommended."

## Typical coprocessor duties

Drawn from the Tanmatsu implementation, as a worked example of what this part is good for:

- Keyboard matrix scanning (9 × 8 in that design)
- PWM backlight control (display and keyboard)
- Real-time clock, backed by a 32.768 kHz watch crystal
- Alarm wakeup, including latching the whole system's power on
- PMIC control over a private I2C bus
- Power switching for peripherals (USB host port, audio amplifier)
- Boot-mode and power control for a companion radio module
- Addressable LED driving
- Presenting all of the above as a single **I2C peripheral** to the application processor

## Design notes

**Always-on rail.** In the Tanmatsu design the part's `Vbatt` rail is held at 2.5 V by a small LDO (`LR8341A-M25`) whenever a battery is connected, independent of the main system rail. The vendor's claim is that the resulting draw is low enough that "theoretically the battery would last over 10 years on a single charge if the device is never turned on, ignoring LiPo battery self-discharge". That claim is **theoretical and vendor-stated, not measured here.**

**Power latch.** Combined with a small logic gate (a `74LVC2G02` dual NOR in the Tanmatsu case), the coprocessor can **emulate a press of the power button** from its RTC alarm output, powering the entire device on at a scheduled time. This is a compact and reusable pattern for battery-powered devices that need scheduled wake.

**Clock.** A 12 MHz crystal in the Tanmatsu design, plus the separate 32.768 kHz watch crystal for the RTC.

## Used by

### Nicolai Electronics Tanmatsu

Reference designator **`U12`**. Acts as the **management coprocessor**, presenting itself on the internal I2C bus at address **`0x5F`**.

| Role | Detail |
|---|---|
| Keyboard | Scans a **9 × 8 matrix**. Rows `PA8, PA9, PA10, PA4, PA3, PA1, PA6, PA5, PA2`; columns `PB14, PB12, PB1, PA7, PB15, PB13, PB2, PB0` |
| Host interface | I2C peripheral — SDA `PB7`, SCL `PB6`, interrupt `PA0` |
| PMIC bus | Private I2C master to a BQ25895 — SDA `PB11`, SCL `PB10` |
| Backlights | Display PWM `PB4`, keyboard PWM `PB3` (into AP3032 drivers) |
| Radio control | ESP32-C6 enable `PB8`, boot mode `PD1` |
| Audio | Headphone detect `PB5`, amplifier enable `PD0` |
| Storage | SD card detect `PA15` |
| Power | Button input `PA12`, latch output `PC13` |
| LEDs | SK6805 data `PA11` |

Firmware: [`Nicolai-Electronics/tanmatsu-coprocessor-firmware`](https://github.com/Nicolai-Electronics/tanmatsu-coprocessor-firmware) (**MIT**), built on `ch32v003fun`.
Host driver: [`esp32-component-tanmatsu-coprocessor`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-coprocessor).

Full register map, matrix scanning algorithm and keymap: [Tanmatsu keyboard documentation](../../../devices/nicolai-electronics/tanmatsu/keyboard.md).
Device record: [Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md).

## Caveats and unknowns

- **No local datasheet copy.** WCH serves the datasheet behind a download page (`CH32V203DS0_PDF.html`); it was not retrieved in this pass.
- **Variant matters.** `CH32V203C8T6` specifically is the LQFP-48 / 64 KB flash / 20 KB RAM part. Other CH32V203 suffixes differ in package, flash and RAM — do not assume a pinout across the family.
- **Erratum status unknown.** WCH errata were not researched.
- **The 144 MHz figure is the family maximum**; the frequency any given design actually runs at is a firmware choice.
- Nothing in this record was verified on hardware.
