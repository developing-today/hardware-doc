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
| Family | CH32V203 (CH32V20x series) — density class **`CH32V20x_D6`** |
| LCSC | [`C3001172`](https://www.lcsc.com/search?q=C3001172) |

Datasheet: <https://www.wch-ic.com/downloads/CH32V203DS0_PDF.html> — ✅ **now held locally**, see
[§Local artifacts](#local-artifacts).
Reference manual: [`components/wch/ch32f2x-ch32v2x-ch32v3x`](../ch32f2x-ch32v2x-ch32v3x/README.md)
— WCH documents CH32F2x, CH32V2x and CH32V3x in **one** manual, and that manual is this part's
register-level authority. It names `CH32V203C8` explicitly as a `CH32V20x_D6` device.

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

## Local artifacts

*Added 2026-09-20. This section resolves the first bullet of §Caveats, which previously read
"No local datasheet copy".*

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| [`artifacts/ch32v203-datasheet-v2.7.pdf`](artifacts/ch32v203-datasheet-v2.7.pdf) | 859 819 | `fe0914cbbcfe35ad98795e8620575d8b521efb75ac04609473c396d3e20a2d8f` | WCH **CH32V203 Datasheet V2.7**, 60 pp. PDF metadata `Title CH32V203DS0-EN`, `Author WCH`, `CreationDate 2023-05-18`, producer `pdfFactory Pro 8.31`. Validated `%PDF-1.7`; text layer cross-checked against the rendered cover heading ("CH32V203 Datasheet / V2.7") before transcription — `executed-success` |

**Provenance.** Not fetched from WCH. It was vendored in the `docs/ch32/` folder of
[`badgeteam/konsool-zero`](https://github.com/badgeteam/konsool-zero) @ `0f0b964` — an expansion
board for *this same device* — and moved into this record on **2026-09-20**. Canonical upstream
remains the HTML download shell `https://www.wch-ic.com/downloads/CH32V203DS0_PDF.html`;
reacquisition `manual`. Licence **unknown**, redistribution **unknown**, disposition
**repository, unstaged**.

**What it confirms.** The datasheet's package table gives `CH32V203C8T6` = **LQFP48, 7 × 7 mm,
0.5 mm pitch** — matching the package recorded above from other evidence. It also confirms the
144 MHz zero-wait main frequency, the V4B core, dual USB (Host + Device), 1 × CAN 2.0B, dual OPA,
4 × USART, dual I2C, 12-bit ADC and 10-channel TouchKey.

⚠ **Variant caution, now sourced.** The datasheet lists eleven CH32V203 orderables across QFN20,
QFN28, QSOP28, LQFP32, LQFP48, QFN48 and LQFP64M. `CH32V203C8U6` is the **QFN48** part with the
same die — same flash and RAM, different footprint. Confirm the suffix, not just `CH32V203`.

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

- ~~**No local datasheet copy.**~~ ✅ **Resolved 2026-09-20** — the WCH **CH32V203 Datasheet
  V2.7** is now held at [`artifacts/ch32v203-datasheet-v2.7.pdf`](artifacts/ch32v203-datasheet-v2.7.pdf),
  and the family **reference manual** (`CH32FV2x_V3x` V2.1) at
  [`components/wch/ch32f2x-ch32v2x-ch32v3x`](../ch32f2x-ch32v2x-ch32v3x/README.md). Both arrived
  via `badgeteam/konsool-zero`, not from WCH directly.
- **Variant matters.** `CH32V203C8T6` specifically is the LQFP-48 / 64 KB flash / 20 KB RAM part. Other CH32V203 suffixes differ in package, flash and RAM — do not assume a pinout across the family. *(Now sourced — see Local artifacts.)*
- ⚠ **Do not confuse this part with the [CH32V003](../ch32v003/README.md)**, added to this
  repository on 2026-09-20. The V003 is a *different* device: QingKe **V2A / `RV32EC`** (no
  hardware multiply or divide, 16 registers), 48 MHz, 16 KB flash, 2 KB SRAM, QFN-20, and a
  **one-wire SDI** debug interface rather than two-wire RVSWD. Toolchain flags, code and the
  `rvswd` reflashing component **do not transfer between them**.
- **Power modes, now sourced.** The family RM documents **three** low-power modes (Sleep / Stop /
  Standby) with **RTC, LSE/LSI and IWDG still running** in Stop and Standby, and Standby wake on
  `WKUP` pin, **RTC alarm**, `NRST` or IWDG reset. SRAM retention in Standby is **opt-in**
  (`R2KSTY`/`R30KSTY`, or `R2KVBAT`/`R32KVBAT` when on VBAT) — see
  [the family record §4](../ch32f2x-ch32v2x-ch32v3x/README.md#4-power-modes-and-wake-sources).
  This is the silicon basis for the always-on coprocessor pattern described under Design notes.
- **Erratum status unknown.** WCH errata were not researched.
- **The 144 MHz figure is the family maximum**; the frequency any given design actually runs at is a firmware choice.
- Nothing in this record was verified on hardware.
