# DinMeter — feature coverage matrix

Applies to K134 and K134-V11. **Zero claims in this record are hardware-tested** — no device was
available. The "Hardware test" column is therefore uniformly `none`, stated plainly rather than
left blank.

Legend — Evidence: **O** official docs · **S** schematic · **F** framework/board-support source ·
**C** community project. Build/Test: `none` = not attempted here.

---

## 1. Advertised and fitted capabilities

| Capability | Hardware | Official docs | Official example | Community example | Feature guide | Build test | Hardware test | Gap |
|---|---|---|---|---|---|---|---|---|
| **Rotary encoder** | encoder on `J5` → GPIO41/40 | O ✔ (PinMap) | ✔ `examples/Basic/encoder` | ✔ Launcher, KilnController, BLE knob | [rotary-encoder-and-buttons](features/rotary-encoder-and-buttons.md) | none | **none** | Encoder part number unpublished; detents/rev unknown |
| **Encoder push-button / WAKE** | GPIO42 | O ✔ | ✔ `examples/Basic/button` | ✔ | [rotary-encoder-and-buttons](features/rotary-encoder-and-buttons.md) | none | **none** | — |
| **Stamp `G0` button** | GPIO0 | O ✔ (download mode) | — | ✔ Launcher | [rotary-encoder-and-buttons](features/rotary-encoder-and-buttons.md) | none | **none** | — |
| **Display** | ST7789V2/P3, GPIO4–8 | O ✔ | ✔ `examples/Basic/display` | ✔ Launcher, UserDemo | [display](features/display.md) | none | **none** | **ST7789P3 has no datasheet**; no measured frame rate |
| **Backlight / dimming** | GPIO9 → `U6` AW35122FDR | O ✘ (not documented) | — | ✔ UserDemo (`Light_PWM`), esp-board-manager | [display](features/display.md) | none | **none** | ⚠ PWM freq conflict: 200 Hz (UserDemo) vs 5 kHz (Espressif) |
| **RTC / timekeeping** | BM8563, GPIO11/12, 0x51 | O ✔ | ✔ `examples/Basic/rtc` (with NTP) | — | [rtc-and-timekeeping](features/rtc-and-timekeeping.md) | none | **none** | Datasheet is a derived document (stray `MAX1937`) |
| **RTC alarm wake-from-off** | `INT` → power latch | O ✔ | ✔ `examples/Basic/wakeup` | — | [rtc-and-timekeeping](features/rtc-and-timekeeping.md) | none | **none** | — |
| **Buzzer** | `LS1` via `Q5`, GPIO3 | O ✔ | ✔ `examples/Basic/buzzer` | — | [buzzer](features/buzzer.md) | none | **none** | Part number, resonant frequency, SPL all unpublished |
| **6–36 V DC input** | `U1` ME3116AM6G | O ✔ | — | — | [power-and-battery](features/power-and-battery.md) | none | **none** | No datasheet; `C24` rated 35 V vs 36 V spec |
| **Li-ion charging** | `U2` TP4057, 100 mA | O ✔ | — | — | [power-and-battery](features/power-and-battery.md) | none | **none** | 4.24 V float, not 4.20 V |
| **Battery voltage sense** | GPIO10, ÷2 | O ✘ | — | ✔ Launcher (`ANALOG_BAT_PIN=10`, ratio 2.0) | [power-and-battery](features/power-and-battery.md) | none | **none** | Not in the vendor PinMap at all |
| **Power latch (GPIO46)** | `Q4` LN2324DT2AG | O ✔ (Learn) | ✔ `examples/Basic/wakeup` | ✔ esp-board-manager | [power-and-battery](features/power-and-battery.md) | none | **none** | — |
| **PORT.A (I²C)** | `J3`, GPIO15/13 | O ⚠ (colours disputed) | — | ✔ Launcher (as SD SPI) | [porta-portb-expansion](features/porta-portb-expansion.md) | none | **none** | ⚠ Yellow/white conflict unresolved |
| **PORT.B (GPIO)** | `J4`, GPIO1/2 | O ⚠ | — | ✔ Launcher | [porta-portb-expansion](features/porta-portb-expansion.md) | none | **none** | Same conflict |
| **Wi-Fi** | ESP32-S3 + module antenna | O ✔ (tutorial page) | ✔ within `examples/Basic/rtc` | ✔ many | [wifi-and-ble](features/wifi-and-ble.md) | none | **none** | No RF measurement; S3A antenna claim unverified |
| **BLE** | ESP32-S3 (BLE 5, **no Classic**) | O ✔ | — | ✔ `tarmn3/m5dinmeter-ble-volume-knob` | [wifi-and-ble](features/wifi-and-ble.md) | none | **none** | — |
| **RGB LED** | WS2812B-2020 in the Stamp, GPIO21 | O ✔ (v1.1 page only) | — | — | [rgb-led](features/rgb-led.md) | none | **none** | ⚠ **v1.1 needs GPIO38 high — predicted, unverified** |
| **USB (native CDC/JTAG)** | ESP32-S3 OTG, USB-C on the Stamp | O ✔ | — | ✔ Launcher (`ARDUINO_USB_MODE=1`) | [development](development.md) §5 | none | **none** | — |
| **DIN panel mounting** | 1/32 DIN, 45 × 22.5 mm | O ✔ | — | — | [din-mounting-and-mechanical](features/din-mounting-and-mechanical.md) | none | **none** | Bezel dims, panel-thickness range, IP rating unpublished |
| **Deep-sleep / power-off** | latch, 38.4 µA | O ✔ | ✔ `examples/Basic/wakeup` | — | [power-and-battery](features/power-and-battery.md) | none | **none** | Vendor figure, no method |

## 2. Capabilities the device does **not** have

Stated positively so the absence is a finding rather than an omission. All from the 84-part
designator census plus the vendor specification tables.

| Not present | Evidence |
|---|---|
| PSRAM | `ESP32-S3FN8`; no PSRAM row on either page; Launcher `build_unflags = -DBOARD_HAS_PSRAM` |
| microSD / storage | no connector designator (Launcher bit-bangs one across the Grove ports) |
| Touch | no controller designator; not in any spec table |
| Microphone / speaker / codec | only `LS1`, a magnetic buzzer |
| IMU / accelerometer | no designator |
| Environmental sensors | no designator |
| USB-UART bridge | USB is the SoC's own peripheral |
| Bluetooth Classic (BR/EDR) | ESP32-S3 silicon limitation |
| External antenna connector | no designator on either Stamp schematic |
| RGB LED on the *carrier* | the WS2812B is inside the Stamp module |
| DIN-**rail** mounting | it is a panel-cutout device; see the mounting guide |

## 3. Coverage summary

| Metric | Count |
|---|---:|
| Advertised/fitted capabilities enumerated | **20** |
| With a task-oriented feature guide | **20 / 20** |
| With a natural-language entry in the README "How do I…?" index | **20 / 20** |
| With official vendor documentation | 16 / 20 |
| With an official vendor example | 7 / 20 |
| With a community example | 10 / 20 |
| **Build-tested here** | **0 / 20** |
| **Hardware-tested here** | **0 / 20** |
| With an open gap recorded | 12 / 20 |

## 4. The gaps that would move the needle most

Ranked by value to the next person:

1. **Verify the RGB-LED/GPIO38 prediction on a real v1.1 unit.** One line of code, five minutes,
   and it converts the single most consequential `inferred` claim in this record into a
   measurement. → [`compatibility-and-status.md`](compatibility-and-status.md)
2. **Photograph the rear silkscreen / pin sticker.** Settles the PORT.A/B wire-colour conflict
   that has stood since the M5Dial.
3. **Measure the Grove 5 V rail.** 5.00 V or 5.38 V — a meter on `J3` pin 3.
4. **Teardown photographs.** Would confirm the encoder, the buzzer, `U4` on the Stamp-S3A, and
   whether the v1.1 PCB really is the v1.0 PCB.
5. **Build one vendor example.** Would give this record its first `executed-success` on the
   software path and confirm or refute the guessed Arduino FQBN.
