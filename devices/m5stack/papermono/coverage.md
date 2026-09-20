# Feature coverage — M5Stack PaperMono

> Every advertised and fitted capability, mapped to hardware, documentation, examples,
> its feature guide and test status.
> Hardware revision **V0.6.2** · snapshot **2026-09-01**.

> ## ⚠ Every row's test status is `not-tested`
>
> **There is no PaperMono in hand and there never was in this research pass.** Nothing in
> this table has been built, flashed, run or measured on a device. No row reaches
> `built`, `hw-tested` or `limit-tested`, and the columns for those are therefore
> uniformly `not-tested` rather than left ambiguous.
>
> What *is* evidenced is: the schematic (parsed), the vendor libraries and firmware source
> (read at cited `file:line`), the vendor documentation pages (retrieved and hashed), and
> two shipped firmware binaries (retrieved and parsed). Where a claim rests only on
> M5Stack saying so, it is marked **V**; where it rests on reading their code, **S**.

Evidence key — **P** primary design data (schematic) · **S** vendor source read at
`file:line` · **V** vendor documentation · **F** shipped firmware binary ·
**C** community report · **I** inferred.

## 1. Fitted and advertised capabilities

| Capability | Hardware | Official docs | Official example | Community example | Feature guide | Build test | HW test | Limit test | Gaps |
|---|---|---|---|---|---|---|---|---|---|
| **E-paper display** | [DKE DEPG0397BBS770F3](../../../components/dke/depg0397bbs770f3/README.md) + [SSD1677](../../../components/solomon-systech/ssd1677/README.md) | ✅ product page + "E-Paper Driver Notes" | ✅ **[`M5PaperMono-OTP-Demo`](https://github.com/m5stack/M5PaperMono-OTP-Demo)** (vendor-recommended) + M5GFX | ✅ 4 third-party projects, 2 claiming hardware validation | [`epaper-display.md`](features/epaper-display.md) | `not-tested` | `not-tested` | `not-tested` | **Vendor calls its own M5GFX waveforms unstable**; 40 vs 20 MHz clock; 4-vs-2 grey levels; OTP waveform coverage unpublished |
| **Frontlight** | [AW9967](../../../components/awinic/aw9967/README.md) + M5PM1 `G3` | ✅ one line on the product page | ⚠ only inside M5GFX | ✅ one project holds it at 127/255 | [`frontlight.md`](features/frontlight.md) | `not-tested` | `not-tested` | `not-tested` | 5 kHz PWM below the AW9967's 10–100 kHz range; squared gamma; stale `Iset` annotation; **no current figure** |
| **Touch** | [FT6336G](../../../components/focaltech/ft6336g/README.md) | ✅ incl. the coordinate limit | ⚠ only via M5GFX | ✅ claimed by one project | [`touch.md`](features/touch.md) | `not-tested` | `not-tested` | `not-tested` | Usable area **X 5–475 / Y 5–795**; no accuracy or latency data |
| **User buttons ×2** | GPIO2 / GPIO3 | ✅ PinMap | ✅ `app_keyboard` in the UserDemo | ✅ | [`buttons-and-rgb-led.md`](features/buttons-and-rgb-led.md) | `not-tested` | `not-tested` | `not-tested` | GPIO3 is a strapping pin; wake-source role unconfirmed |
| **Power button** | M5PM1 `BTN_PU` | ✅, but **three vendor pages disagree** on the name | ✅ `app_shutdown` | ✅ two projects disable single-click reset | [`buttons-and-rgb-led.md`](features/buttons-and-rgb-led.md) | `not-tested` | `not-tested` | `not-tested` | Arduino page invents a "reset button on the side" |
| **RGB LED** | M5PM1 `LED_EN_PP` (red) + M5IOE1 `IO8`/`IO9` | ✅ incl. the no-PWM caveat | ✅ `app_rgb` | ❌ | [`buttons-and-rgb-led.md`](features/buttons-and-rgb-led.md) | `not-tested` | `not-tested` | `not-tested` | **Red has no PWM**; M5Unified also writes blue binary; LED part `RS-C1415MBAR` has **no datasheet** |
| **Power management / 5 states** | [M5PM1](../../../components/m5stack/m5pm1/README.md) | ✅ dedicated page + 4 sketches | ✅ `app_sleep_wake`, `app_shutdown`, 4 M5PM1 library examples | ✅ `Free-Ink/freeink-sdk` board bring-up | [`power-and-sleep.md`](features/power-and-sleep.md) | `not-tested` | `not-tested` | `not-tested` | **No current figure for any state**; L3A/L3B distinction unclear; `3V3_L0` enable unread |
| **Battery + charging** | [IP2315](../../../components/injoinic/ip2315/README.md) + [AW32901](../../../components/awinic/aw32901/README.md) | ✅ incl. the bus hazard (product page only) | ✅ `app_battery` | ✅ one project reports battery/charge telemetry | [`battery-and-charging.md`](features/battery-and-charging.md) | `not-tested` | `not-tested` | `not-tested` | `ICHGSET` resistor unresolved; **no runtime figure**; no fuel gauge |
| **USB / serial / flashing** | GPIO19/20 + UART0 GPIO43/44 | ⚠ **absent from the PinMap** — schematic only | ✅ build instructions in the OTP demo README | ✅ | [`usb-and-serial.md`](features/usb-and-serial.md) | `not-tested` | `not-tested` | `not-tested` | **No USB-PD**; QIO documented vs DIO shipped; no OTA slot |
| **Wi-Fi 2.4 GHz** | ESP32-S3R8 | ✅ one spec line | ✅ `app_wifi_scan` | ✅ | [`wifi-and-bluetooth.md`](features/wifi-and-bluetooth.md) | `not-tested` | `not-tested` | `not-tested` | **No throughput, range or antenna data at all**; no certification |
| **Bluetooth LE** | ESP32-S3R8 | ❌ **not in any vendor spec table** | ❌ none | ⚠ one project claims BLE tiles, shows no hardware | [`wifi-and-bluetooth.md`](features/wifi-and-bluetooth.md) | `not-tested` | `not-tested` | `not-tested` | **Undocumented by the vendor.** "Bluetooth 5.0 LE + Mesh" is a publication's inference |
| **LoRa (C153 only)** | [Stamp LoRa-1262](../../../components/m5stack/stamp-lora-1262/README.md) / SX1262 | ✅ PinMap + spec | ✅ `app_lora` (RadioLib 7.2.1) | ❌ | [`lora.md`](features/lora.md) | `not-tested` | `not-tested` | `not-tested` | **No module datasheet exists**; `SX_ANT_SW` semantics unknown; **no regional band plan, no certification**; TCXO only `inferred` |
| **NFC (C153 only)** | [ST25R3916](../../../components/stmicroelectronics/st25r3916/) | ✅ PinMap + spec | ✅ `app_nfc_scan` (M5Unit-NFC) | ❌ | [`nfc.md`](features/nfc.md) | `not-tested` | `not-tested` | `not-tested` | **Which card types actually work is unknown**; NFC schematic sheet 1/2 unpublished (but sheet 2/2 does carry the full front end) |
| **IMU** | [BMI270](../../../components/bosch-sensortec/bmi270/README.md) | ✅, but **polarity stated wrongly** | ✅ `app_imu` + the vendor wake sketch | ❌ | [`imu.md`](features/imu.md) | `not-tested` | `not-tested` | `not-tested` | Vendor prose says active-high; code and binary say active-low. Mirrored datasheet 5 years stale |
| **RTC** | [RX8130CE](../../../components/seiko-epson/rx8130ce/) | ✅ PinMap | ✅ `app_clock` | ✅ one project reports RTC time working | [`rtc.md`](features/rtc.md) | `not-tested` | `not-tested` | `not-tested` | **No vendor code demonstrates RTC wake end to end**; the M5Stack mirror is in fact Epson's English manual ETM50E-09, served under a `_cn` filename |
| **microSD** | 4-bit SDMMC, GPIO8–13 | ✅ PinMap + detect semantics | ✅ `app_tf_card` | ✅ CrossPoint uses `/​.crosspoint/` on the card | [`microsd.md`](features/microsd.md) | `not-tested` | `not-tested` | `not-tested` | **No throughput figure**; no documented capacity or filesystem limit |
| **PDM microphone** | `LMD4737T261-AC02` | ✅ PinMap | ✅ `app_mic_wave` | ❌ | [`microphone.md`](features/microphone.md) | `not-tested` | `not-tested` | `not-tested` | **No datasheet exists**; GPIO45/46 are strapping pins; only 16 kHz exercised |
| **Buzzer** | GPIO42 | ✅ PinMap | ✅ `app_buzzer` | ❌ | [`buzzer.md`](features/buzzer.md) | `not-tested` | `not-tested` | `not-tested` | Buzzer part unidentified; resonant frequency unknown |
| **I/O expander** | [M5IOE1](../../../components/m5stack/m5ioe1/README.md) | ✅ dedicated page + datasheet | ✅ 3 library examples + all HAL code | ✅ `Free-Ink/freeink-sdk` | [`io-expander.md`](features/io-expander.md) | `not-tested` | `not-tested` | `not-tested` | `M5IOE1_PIN_3 = 2`; address `0x4F` vs the manual's `0x6F`–`0x76`; `IO7` omitted from the PinMap; **GPIO7 interrupt path unexercised** |
| **PSRAM (8 MB octal)** | ESP32-S3R8, in package | ✅ spec line | ✅ implied by every build | ✅ | [`epaper-display.md` §7](features/epaper-display.md#7-octal-psram-is-mandatory--and-the-failure-looks-like-dead-hardware) | `not-tested` | `not-tested` | `not-tested` | **Mandatory** — M5GFX aborts without it. Bandwidth unmeasured |
| **Flash (16 MB)** | [XM25UH128DHIQT](../../../components/xmc/xm25uh128dhiqt/README.md) | ✅ spec line | ✅ `partitions.csv` in both projects | ✅ CrossPoint repartitions entirely | [`microsd.md` §9](features/microsd.md#9-alternatives-for-storage) | `not-tested` | `not-tested` | `not-tested` | **No OTA slot, no filesystem** as shipped |

## 2. Capabilities with no example and no documentation — flagged as gaps

| Capability | Status | Detail |
|---|---|---|
| **UiFlow2** | ⚠ **advertised, undocumented — the clearest gap** | M5Stack lists UiFlow2 support and publishes a page for it. That page states **no required firmware version, no minimum UiFlow2 version, no PaperMono-specific block list, and no limitations** other than browser-pairing caveats. Confirmed by full-text search of the retrieved 265 KB page — a genuine documentation gap, not a retrieval failure. **No feature guide was written**, because there is nothing to write from. [`gaps-and-conflicts.md` G4](gaps-and-conflicts.md#g4--uiflow2-support-is-advertised-but-undocumented) |
| **OTA update** | ❌ absent by construction | Single `factory` partition. Neither vendor project has an OTA slot |
| **Bluetooth LE** | ⚠ silicon-only | Not in any vendor spec table, no example anywhere (§1) |
| **NFC card emulation** | ⚠ API exists, never used | `cfg.emulation` is set `false` in all vendor code |
| **M5IOE1 ADC ×4, PWM3/4, NeoPixel, temperature sensor, retention RAM** | ⚠ fitted silicon, unused | All fourteen expander pins are digital assignments on this board |
| **M5PM1 retention RAM (32 B), NeoPixel, watchdog** | ⚠ fitted, unused | No vendor code exercises them |
| **JTAG / hardware debug** | ❌ not evaluated | Not investigated in this pass. GPIO39–42 (the ESP32-S3 JTAG group) carry LoRa SPI and the buzzer, so it is likely unavailable — **`inferred`, unconfirmed** |
| **Certification** | ❌ **verified negative** | `/en/certification` returns HTTP 200 with **zero** matches for `PaperMono` and `C153` |
| **Product I²C address table** | ❌ **verified negative** | `/en/product_i2c_addr` returns 200 with zero matches, despite seven fitted I²C devices |
| **Product/teardown imagery** | ❌ none retained | Vendor imagery is not licensed for redistribution; no independent teardown existed at the snapshot date |
| **Performance characterisation** | ❌ `performance.md` not written | Nothing to put in it — see §4 |

## 3. Example inventory

| Source | What exists |
|---|---|
| **`m5stack/M5PaperMono-UserDemo`** | The factory firmware. HEAD `c1099107…` (2026-08-10), MIT, ESP-IDF 5.5.1. **Fifteen demo apps**: battery, brightness, buzzer, clock, IMU, keyboard, LoRa, mic wave, NFC scan, RGB, shutdown, sleep/wake, TF card, WiFi scan. The single richest source of pin evidence, because the HAL declares pins as named constants |
| **`m5stack/M5PaperMono-OTP-Demo`** | HEAD `c7c02554…` (2026-08-20), MIT. Minimal SSD1677 driver using only OTP waveforms. **Vendor-recommended over M5GFX** |
| `m5stack/M5PM1` | 1.0.7. Examples: `basic_power_adc`, `gpio_pwm`, `neopixel`, `usb_interrupt_sleep` |
| `m5stack/M5IOE1` | 1.0.9. Examples: `interrupt_hardware`, `interrupt_polling`, `pin_test` |
| Vendor docs page sketches | Four verbatim sketches on the M5PM1/M5IOE1 power page |
| **Community** | `MagicCube/free-ink-on-paper-mono` (hardware-validated, Lite) · `MingRZou/PaperMono-Launcher` (hardware-validated) · `EggUncle/PaperMonoCalendar` (no hardware shown) · `hectorzin/M5PaperMono-HomeAssistant-ESPHome` (early WIP, self-labelled hypothesis) · `Free-Ink/freeink-sdk` (board bring-up) · `crosspoint-reader` (roadmap only) |

> **No example is vendored into this record.** `examples/` under this device record is
> empty; everything above is referenced by upstream URL and commit. That is a deliberate
> gap, recorded rather than papered over.

> ⚠ **The factory firmware is not reproducible.** Its `esp_app_desc_t` reports
> `c78f6c5-dirty` — built from an uncommitted tree. And it pins M5GFX/M5Unified to
> `develop` commits **older than either current branch head**, so it was built against a
> different waveform table than anything you can check out today.

## 4. Summary — and the honest bottom line

- **21 fitted or advertised capabilities tracked**, covered by **16 feature guides**.
  Every fitted capability has a guide or an explicit documented-absence.
- **Zero rows are hardware-tested.** Zero rows are even *build*-tested. This is the single
  largest limitation of the entire research pass and it is not recoverable without a
  device.
- **Four capabilities have official examples but no community example**: LoRa, NFC,
  microphone, buzzer. Eleven days after launch that is unsurprising, but it means the only
  evidence they work is that M5Stack wrote code for them.
- **One advertised capability has neither documentation nor an example: UiFlow2.**
- **No `performance.md` exists**, because there is nothing measured to put in one. No
  refresh time we can stand behind, no current in any power state, no Wi-Fi throughput, no
  SD throughput, no LoRa range, no battery runtime. The vendor's four refresh numbers are
  lab figures for an unnamed build.

The pattern in the missing rows is not random. The board is eleven days old, sold out
within minutes, and has **one hands-on video and zero written reviews**. Everything
written about it traces to a single vendor blog post. The real early signal is code —
four third-party GitHub projects, two with credible hardware validation, independently
corroborating the M5PM1 single-click-reset behaviour. That is a statement about
2026-09-01, not a permanent property of the product.

## Related

- [`features/README.md`](features/README.md) · [`resources-and-conflicts.md`](resources-and-conflicts.md) · [`compatibility-and-status.md`](compatibility-and-status.md)
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) · [`README.md`](README.md)
- [`vendors/m5stack`](../../../vendors/m5stack/README.md) · [`vendors/dke`](../../../vendors/dke/README.md)
