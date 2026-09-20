# DinMeter — resources and conflicts

Applies to K134 and K134-V11 (identical GPIO map). Evidence: schematic + `M5Unified` +
`espressif/esp-board-manager` + `bmorcelli/Launcher`, all cross-checked. `not-tested` on hardware.

---

## 1. Complete GPIO budget

The Stamp-S3 breaks out **23** IOs. Here is every one of them.

| GPIO | Owner | Free? | Notes |
|---:|---|---|---|
| 0 | Stamp `G0` button / boot strap | ⚠ shared | Usable as `M5.BtnB` at runtime; **must be high at reset** |
| 1 | **PORT.B** signal | ✔ user | ADC1, LEDC-capable |
| 2 | **PORT.B** signal | ✔ user | ADC1, LEDC-capable |
| 3 | Buzzer `LS1` | ✘ | via `Q5` SS8050 |
| 4 | Display D/C | ✘ | |
| 5 | Display MOSI | ✘ | |
| 6 | Display SCLK | ✘ | |
| 7 | Display CS | ✘ | |
| 8 | Display RESET | ✘ | |
| 9 | Display backlight enable | ✘ | drives `U6` AW35122FDR |
| 10 | Battery ADC (`R7`/`R8` 1 MΩ + 1 MΩ, **ratio 2.0**) | ✘ | ADC1 |
| 11 | **Internal** I²C SDA (RTC) | ✘ | |
| 12 | **Internal** I²C SCL (RTC) | ✘ | |
| 13 | **PORT.A** — SDA per M5Unified | ✔ user | 10 kΩ pull-up fitted |
| 14 | Power-latch OR network (`D7`, `R9`) | ⚠ **not free** | Vendor PinMap implies free; hardware is fitted. **Do not repurpose** |
| 15 | **PORT.A** — SCL per M5Unified | ✔ user | 10 kΩ pull-up fitted |
| 39 | Power-latch OR network (`R10`) | ⚠ **not free** | Same caution as GPIO14 |
| 40 | Encoder B | ✘ | `MTDO` |
| 41 | Encoder A | ✘ | `MTDI` |
| 42 | Encoder push-button / WAKE | ✘ | `MTMS`, also a wake source |
| 43 | **UART0 TX** | ✔ **free** | **No net label on the schematic** — a blank cell, not a drawn no-connect. Probably free; verify with a meter |
| 44 | **UART0 RX** | ✔ **free** | Same caveat |
| 46 | **Power hold** | ✘ | Strapping pin. Never fit an external pull-up |

**Free for the user: 6 pins** — GPIO1, 2, 13, 15 (the two Grove ports) and GPIO43, 44 (UART0,
unverified). Plus GPIO0 if you can share it with the boot strap.

### Internal to the Stamp module — invisible to the carrier

| GPIO | Function | Notes |
|---:|---|---|
| 19, 20 | USB D−/D+ | native USB-C |
| 21 | WS2812B-2020 RGB LED data | see [`features/rgb-led.md`](features/rgb-led.md) |
| 33–38 | Rear LCD FPC (`DISP_RST/RS/MOSI/SCK/CS/BL`) | GPIO38 is the LED power enable **on Stamp-S3A** |

These are the pins an ESP32-S3**R8** spends on octal PSRAM. The `FN8` has none, which is why
M5Stack could route them to the module's rear header — and why there is no PSRAM.

---

## 2. Peripheral budget

| Peripheral | Total on ESP32-S3 | Used by the board | Free |
|---|---:|---:|---|
| SPI host | 2 usable (`SPI2`, `SPI3`) | **1** (`SPI2_HOST`, display) | 1 |
| I²C | 2 | **1** (internal, RTC) + 1 if you use PORT.A | 0–1 |
| LEDC channel | 8 | **2** (backlight ch 0, buzzer ch 1) | 6 |
| LEDC timer | 4 | **2** (timer 0 backlight, timer 1 buzzer) | 2 |
| PCNT unit | 4 | **1** if you use the IDF encoder path | 3 |
| RMT channel | 8 | 1 if you drive the RGB LED via RMT | 7 |
| ADC1 channel | 10 | **1** (GPIO10 battery) + up to 2 on PORT.B | — |
| GPIO interrupt | many | 2 if you use the Arduino encoder path | — |
| DMA | — | display, optional | — |

---

## 3. Real conflicts

Only three exist. Everything else composes freely.

### 3.1 LEDC timer sharing — backlight vs buzzer

Both want LEDC. Espressif's board definition puts them on **different timers by design**
(backlight ch 0 / timer 0; buzzer ch 1 / timer 1) because **channels on the same timer share a
frequency**. If you write your own LEDC setup and put them together, changing the buzzer's pitch
changes the backlight's PWM frequency — usually visible as a brightness step or flicker.

**Mitigation:** keep them on separate timers. This is the only conflict that will actually
surprise you.

### 3.2 JTAG pins are all consumed

GPIO39 (`MTCK`), 40 (`MTDO`), 41 (`MTDI`), 42 (`MTMS`) are the ESP32-S3's pin-based JTAG. All
four have hardware on them (encoder ×2, button, latch network). **Pin-based JTAG debugging is
not possible while the knob works.**

**Mitigation:** use **USB-Serial-JTAG**, which is on GPIO19/20 inside the module and unaffected.

### 3.3 GPIO14 and GPIO39 are advertised free but are not

The vendor PinMap lists the Stamp's 23 IOs and does not mark GPIO14 or GPIO39 as used. The
schematic shows both carrying a 10 kΩ + 1N4148WT network tied into the power-latch region.
**Repurposing them risks defeating the wake/latch circuit.** The circuit was not fully traced —
see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §8.

---

## 4. Combinations, evaluated

Not one feature at a time — the combinations people actually build.

| Combination | Pin conflict? | Other constraint | Verdict |
|---|---|---|---|
| Display + encoder + button | none | — | **fine** |
| Display + encoder + buzzer | none | LEDC timers must differ (§3.1) | **fine, with care** |
| Display + RTC + Wi-Fi | none | RAM: framebuffer 64.8 KB + Wi-Fi stack, **no PSRAM** | **fine with band buffers**; a full-screen sprite + TLS is tight |
| Display + Wi-Fi + TLS + BLE | none | **RAM.** ~65 KB fb + ~40 KB NimBLE + 20–50 KB per TLS session on ~512 KB SRAM | **tight** — profile it |
| Both Grove ports as SD-card SPI | consumes all 4 free Grove pins | — | **demonstrated** by Bruce/Launcher (`SDCARD_CS=13, SCK=15, MISO=2, MOSI=1`) |
| Grove I²C + Grove GPIO simultaneously | none | 220 mA per port from a shared boost | **fine** |
| Everything at once + battery | none | 25.5–33.5 mA standby on a 250 mA·h cell ≈ 8–10 h | **works, but plan the duty cycle** |
| Pin-based JTAG + encoder | **yes, hard** | — | **impossible.** Use USB-Serial-JTAG |

---

## 5. Power budget

| Rail | Source | Limit | Consumers |
|---|---|---|---|
| `+5VIN` | `U1` ME3116AM6G buck (6–36 V) **or** USB | not published | Stamp pad 13, charger, supervisor, buzzer |
| `+5VOUT` | `U3` SY7088 boost from battery | **220 mA per Grove port** (vendor) | PORT.A + PORT.B pin 3 |
| `+3.3V` | `U4` BL8075CB5TR33 LDO from `VBAT_IN` | not published | RTC, pull-ups, LCD FPC |
| Module `VDD_3V3` | inside the Stamp: MUN3CAD01-SC (**1 A**) on S3, unidentified buck (**0.6 A**) on S3A | see left | ESP32-S3, RGB LED, module FPC |

⚠ **The Stamp-S3A's internal regulator is rated 0.6 A where the Stamp-S3's was 1 A.** Not
mentioned in either vendor spec table. Unlikely to matter on a DinMeter (the carrier makes its
own 3.3 V), but it is a reduction. See
[`../dinmeter-v1.1/stamp-s3-to-s3a-delta.md`](../dinmeter-v1.1/stamp-s3-to-s3a-delta.md) §5.

⚠ **`C24`, the buck input capacitor, is rated 35 V against a 36 V input spec** — 103 % of
rating at the ceiling. Treat 36 V as an absolute maximum.

---

## 6. Flash and partitions

8 MB, no PSRAM. **M5Stack publishes no partition table.** Two known-working third-party layouts:

| Project | Layout |
|---|---|
| `M5DinMeter-UserDemo` | PlatformIO `esp32-s3-devkitc-1` default (unstated in the project file) |
| `bmorcelli/Launcher` | `support_files/custom_8Mb.csv`, `board_upload.maximum_size = 8388608`, SPIFFS threshold `0x2F0000` |

---

## Related

[`pinouts-and-buses.md`](pinouts-and-buses.md) · [`coverage.md`](coverage.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md) · [`features/`](features/README.md)
