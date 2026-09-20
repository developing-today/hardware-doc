# DinMeter — development

Applies to **K134 and K134-V11** unless a row says otherwise. Every command carries a status:
`executed-success` · `executed-failed` · `reported-working` · `inferred` · `not-tested`.

> **No DinMeter hardware was available for this pass.** Nothing below is `executed-success` on
> the device. Build and flash commands are `inferred` from vendor documentation, vendor project
> files and framework documentation, and are labelled as such. The command ledger in
> [`commands.md`](commands.md) records exactly what *was* run (all of it acquisition and
> analysis) and what was not.

---

## 0. The one thing to do first

```cpp
void setup() {
    auto cfg = M5.config();
    DinMeter.begin(cfg, true);   // <- this calls M5.begin(), which raises GPIO46 (HOLD)
    ...
}
```

On battery power the board is only alive while **GPIO46 is high**. `M5.begin()` does it for you
via M5Unified's power-hold table (`_pin_table_other1`, `board_M5DinMeter → GPIO_NUM_46`,
`M5Unified/src/M5Unified.cpp:282`). If you write bare ESP-IDF or bare Arduino without
M5Unified, **you must do it yourself, before anything slow**:

```c
gpio_set_direction(GPIO_NUM_46, GPIO_MODE_OUTPUT);
gpio_set_level(GPIO_NUM_46, 1);
```
`inferred` from the vendor Learn section and `esp-board-manager`'s `gpio_power_hold`
(`default_level: 1`).

Symptom if you forget: the board runs for as long as you hold the knob in, then dies. On USB it
works fine, which makes the bug look like a "battery problem".

---

## 1. Arduino — M5Unified + M5DinMeter (the vendor path)

### Versions

| Component | Version | Evidence |
|---|---|---|
| Board package | **M5Stack Arduino Board Manager v2.1.1** — the version every vendor example header names | `M5DinMeter/examples/Basic/*/*.ino` header comments, all dated 2024-03-07 |
| Board target | `M5Stack-Din-Meter` (M5Stack board package) — **not verified**; the vendor examples do not name a board FQBN | `inferred` |
| `M5DinMeter` | **1.0.0** — the only release, tagged 2024-03-07. Repo HEAD `8ccbad7297beb82a140f812e5606e060d8a5e0dc` (pushed 2026-08-03) is still `version=1.0.0` | `library.properties:2`; GitHub API |
| `M5Unified` | `>= 0.1.13` declared; latest release **0.2.21** (2026-08-26) | `M5DinMeter/library.json:16` |
| `M5GFX` | pulled in by M5Unified; latest **0.2.28** (2026-08-25) | GitHub API |

`M5DinMeter` declares exactly one dependency (`depends=M5Unified`) and its licence file lists
M5GFX (MIT), M5Unified (MIT) and the bundled `Encoder` (PJRC, MIT). The library itself carries
**no `LICENSE` file** and GitHub reports no licence for the repository.

### What the library actually is

45 lines of header and 23 of implementation. It is a façade over M5Unified plus one vendored
third-party encoder driver:

```cpp
// M5DinMeter/src/M5DinMeter.h
#define DIAL_ENCODER_PIN_A 41
#define DIAL_ENCODER_PIN_B 40
class M5DinMeter {
  M5GFX &Display = M5.Display;   Power_Class &Power = M5.Power;
  RTC8563_Class &Rtc = M5.Rtc;   Speaker_Class &Speaker = M5.Speaker;
  Button_Class &BtnA = M5.BtnA;
  I2C_Class &In_I2C = m5::In_I2C;   // internal bus  (GPIO12/11) - RTC
  I2C_Class &Ex_I2C = m5::Ex_I2C;   // external bus  (GPIO15/13) - PORT.A
  ENCODER Encoder = ENCODER(DIAL_ENCODER_PIN_A, DIAL_ENCODER_PIN_B);
  void begin(m5::M5Unified::config_t cfg, bool enableEncoder = false);
  void update(void);
};
extern m5::M5DinMeter DinMeter;
```

**Note `enableEncoder` defaults to `false`.** `DinMeter.begin(cfg)` will not start the encoder;
you need `DinMeter.begin(cfg, true)`. Every vendor example that reads the knob passes `true`.

### Install

```bash
# Arduino IDE: Library Manager -> "M5DinMeter"          (reported-working; vendor instruction)
# or, pinned to the exact snapshot analysed here:
git clone https://github.com/m5stack/M5DinMeter.git ~/Arduino/libraries/M5DinMeter
git -C ~/Arduino/libraries/M5DinMeter checkout 8ccbad7297beb82a140f812e5606e060d8a5e0dc
```
`inferred` — the clone form was not run; the tarball of that exact commit **was** fetched and is
retained at
[`artifacts/source-snapshots/M5DinMeter-8ccbad7297beb82a140f812e5606e060d8a5e0dc.tar.gz`](artifacts/source-snapshots/M5DinMeter-8ccbad7297beb82a140f812e5606e060d8a5e0dc.tar.gz)
(SHA-256 `de47c4109635870506bb7a02040db496f82e5bbb22a5b1befe600a3985eb0f02`, `executed-success`).

### Build, flash, monitor

```bash
arduino-cli core install m5stack:esp32                                   # not-tested
arduino-cli lib install M5DinMeter                                       # not-tested
arduino-cli compile -b m5stack:esp32:m5stack_dinmeter sketch/            # not-tested; FQBN unverified
arduino-cli upload  -b m5stack:esp32:m5stack_dinmeter -p /dev/ttyACM0 sketch/   # not-tested
arduino-cli monitor -p /dev/ttyACM0 -c baudrate=115200                   # not-tested
```

**The FQBN `m5stack:esp32:m5stack_dinmeter` is a guess and is flagged as such.** M5Stack's own
documentation gives IDE instructions only; no vendor source in this pass names the FQBN. Verify
with `arduino-cli board listall | grep -i din`.

### PlatformIO

The vendor's own factory-firmware project uses a **generic** board, not a DinMeter board:

```ini
; m5stack/M5DinMeter-UserDemo/platformio.ini  (executed-success: read from the retained snapshot)
[env:esp32-s3-devkitc-1]
platform = espressif32@6.3.1
board = esp32-s3-devkitc-1
framework = arduino
board_build.f_cpu = 240000000L
monitor_speed = 115200
monitor_filters = esp32_exception_decoder
lib_deps =
    lovyan03/LovyanGFX @ 1.1.12
    forairaaaaa/SmoothUIToolKit @ 1.0.1
```

That is a useful, working, *pinned* starting point — and it tells you something: **you do not
need a DinMeter board definition.** `esp32-s3-devkitc-1` with `f_cpu` pinned is enough, because
everything board-specific is pin numbers.

---

## 2. ESP-IDF

There is **no M5Stack ESP-IDF component** for the DinMeter. There are two credible routes.

### 2a. Espressif's `esp-board-manager` (recommended — it is a real, maintained board definition)

`espressif/esp-board-manager` ships `m5stack_boards/m5stack_dinmeter/` with three YAML files
that between them define the whole board. Fetched at repository HEAD
`2beb9b22b0892b343bd555a1ebc9929a7edce8fc` (2026-09-03) and retained at
[`artifacts/source-snapshots/`](artifacts/source-snapshots/) (`executed-success`).

What it gives you, ready to use:

| Definition | Value |
|---|---|
| `board_info.yaml` | `board: m5stack_dinmeter`, `chip: esp32s3`, `version: 1.0.0` |
| `spi_display` | `SPI2_HOST`, SCLK 6, MOSI 5, MISO −1, `max_transfer_sz: 6480` |
| `display_lcd` | `chip: st7789`, 135 × 240, CS 7, DC 4, RST 8, mode 0, **40 MHz**, `invert_color: true`, 16 bpp, RGB order |
| `ledc_backlight` | GPIO9, ch 0, timer 0, **5 kHz**, 10-bit |
| `ledc_buzzer` | GPIO3, ch 1, timer 1, **4 kHz**, 10-bit |
| `pcnt_encoder` | edge 41 / level 40 and edge 40 / level 41, `max_glitch_ns: 1000`, ±1000, `accum_count: true`, watch points −1000/0/1000 |
| `i2c_master` | port 0, SDA 11, SCL 12 (the RTC bus) |
| `gpio_power_hold` | GPIO46, output, `default_level: 1` |
| `gpio_button_wake` | GPIO42, input, pull-up, active-low, long-press 2000 ms |

Its own comments are unusually candid and worth reading — they document the GRAM gap
(**column +52, row +40**, applied by the application via the panel gap API because the board
model has no offset field), the reason both PCNT channels are used, and an ESP32-S3-specific
build trap:

> "No `en_step_notify_up` / `en_step_notify_down` here on purpose: those `pcnt_unit_config_t`
> fields exist only under `SOC_PCNT_SUPPORT_STEP_NOTIFY`, which the ESP32-S3 does not have, and
> bmgr's `periph_pcnt` generator emits the field whenever the key is PRESENT — even when false.
> Keeping them (both were false) breaks the build with `'struct <anonymous>' has no member named
> 'en_step_notify_up'`."

It also records what it deliberately does **not** model: the BM8563 RTC (no device type — the
I²C bus is provided, the driver is yours), both Grove ports, the DC input, the charger, the RST
button, and USB.

```bash
idf.py set-target esp32s3                                    # not-tested
idf.py -DBOARD=m5stack_dinmeter build flash monitor          # not-tested; consult esp-board-manager's own README for the exact invocation
```

### 2b. Plain ESP-IDF

Nothing about the board needs a BSP. Target `esp32s3`, **no PSRAM**, 8 MB flash, and the pin map
from [`pinouts-and-buses.md`](pinouts-and-buses.md). Use `esp_lcd_panel_st7789` (built in), the
`pcnt` driver for the encoder, `ledc` for backlight and buzzer, `i2c_master` for the RTC.

```bash
idf.py set-target esp32s3 && idf.py menuconfig
#   Serial flasher config -> Flash size -> 8 MB
#   Component config -> ESP PSRAM -> [ ] Support for external SPI RAM   (there is none)
idf.py build && idf.py -p /dev/ttyACM0 flash monitor          # not-tested
```

---

## 3. UiFlow2 (and how it relates to the Arduino path)

M5Stack documents a UiFlow2 tutorial for the DinMeter at
`https://docs.m5stack.com/en/uiflow2/m5dinmeter/program` (HTTP 200, 2026-09-04) and lists
UiFlow2 first among the supported development platforms on both product pages.

**How the two relate — this trips people up.** UiFlow2 is *not* a layer over the Arduino
library. It is a **MicroPython firmware** (`m5stack/uiflow-micropython`, which has a
`build-firmware.yml` CI workflow and a `.gitlab-ci.yml` that both reference DinMeter) which you
flash **in place of** your Arduino sketch, using **M5Burner**. The relationship is:

| | Arduino / M5DinMeter | UiFlow2 |
|---|---|---|
| What is on the flash | your compiled sketch | a MicroPython interpreter + the UiFlow2 runtime |
| How you program | compile & upload | drag blocks in a browser, push over Wi-Fi/USB |
| Underlying HAL | M5Unified (C++) | M5Stack's MicroPython bindings, which wrap the *same* M5GFX/M5Unified C++ code |
| Switching between them | reflash — they are mutually exclusive images | reflash |
| Pin map | identical | identical |

So the pin assignments and the GPIO46 hold requirement in this document apply verbatim to
UiFlow2; only the API surface differs.

**Getting UiFlow2 firmware:** M5Burner (desktop app, from `docs.m5stack.com` → Software →
M5Burner) is the vendor's distribution channel; it downloads images at run time from an M5Stack
endpoint rather than from a documented static URL. **No stable direct download URL for a
DinMeter UiFlow2 binary was located in this pass** — recorded as a gap in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) §7.

---

## 4. MicroPython

Two routes:

1. **UiFlow2** (§3) — M5Stack's own MicroPython fork with board bindings. The supported path.
2. **`mattytrentini/chipboard`** ships `boards/m5stack_din_meter.yaml`, a community board
   definition for generic MicroPython. **[COM]** — not evaluated, not built. Recorded in
   [`examples/catalog.json`](examples/catalog.json) as a discovered candidate.

Vanilla `micropython/micropython` has **no** DinMeter board port (searched 2026-09-04).

---

## 5. Serial, USB and download mode

| Aspect | Value | Evidence |
|---|---|---|
| USB connector | USB-C, **on the Stamp module**, not on the carrier | Stamp-S3 schematic `J2` |
| USB peripheral | ESP32-S3 native **USB OTG / USB-Serial-JTAG** — there is **no UART bridge chip** | vendor spec row; no bridge designator in the 84-part census |
| Port on Linux | typically `/dev/ttyACM*` (CDC-ACM), not `/dev/ttyUSB*` | `inferred` from the native-USB architecture |
| Monitor baud | 115200 (vendor project setting) | `M5DinMeter-UserDemo/platformio.ini` |
| **Download mode** | **hold the `G0` button on the Stamp module while applying power, release after power is applied** | vendor Learn section, both product pages, identical wording for Stamp-S3 and Stamp-S3A |
| Reset | `S4` RST button on the carrier drives the Stamp's `EN` | DinMeter schematic |
| JTAG | USB-Serial-JTAG is available; the classic JTAG pins (GPIO39–42, `MTCK/MTDO/MTDI/MTMS`) are **all in use** — 40/41 encoder, 42 button — so pin-based JTAG is not practical | schematic + `pinouts-and-buses.md` |

Because USB is the SoC's own peripheral, **a crashed or sleeping application takes the serial
port with it.** If the port disappears, use download mode.

---

## 6. Bricking and power risks

| Risk | Why | Mitigation |
|---|---|---|
| **Board switches off mid-flash on battery** | GPIO46 low = battery disconnected | Flash over USB, which bypasses the latch |
| **Forgetting the GPIO46 hold** | see §0 | `M5.begin()`, or set it manually first thing |
| **Pulling GPIO46 high externally** | It is an ESP32-S3 strapping pin, pulled *down* by design on the Stamp module; high at reset prevents boot | Never fit an external pull-up; drive it only after boot |
| **36 V on the DC terminal** | `C24`, the input bulk cap, is rated **35 V** — 103 % of the spec ceiling | Treat 36 V as absolute maximum, not a working point. Stay ≤ 30 V for continuous use (`inferred`, engineering judgement, not a vendor statement) |
| **Reverse polarity on the DC terminal** | `D13`/`D12` Schottkys are fitted, but their rating was not read | Do not rely on it; get the polarity right |
| **5 V-max peripheral on a Grove port** | the boost's own divider computes to ≈ 5.38 V, while the spec says 5 V | Measure before connecting. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §6 |
| **Losing the factory firmware** | there is no vendor-published pre-built binary with a documented URL | Read the flash out *before* you overwrite it: `esptool.py read_flash 0 0x800000 backup.bin` (`not-tested`). See [`factory-firmware.md`](factory-firmware.md) |

---

## 7. Firmware image metadata

| Field | Value |
|---|---|
| Target MCU | ESP32-S3 (`esp32s3`), Xtensa LX7 dual-core |
| Flash | 8 MB, in-package (`ESP32-S3FN8`) |
| PSRAM | **none** — do not enable it |
| CPU frequency | 240 MHz (`board_build.f_cpu = 240000000L`) |
| Flash mode / freq | not stated by the vendor; ESP32-S3 default QIO 80 MHz applies unless changed |
| Partition table | **not published.** Not stated on either product page, not in the UserDemo `platformio.ini`, which means PlatformIO's `esp32-s3-devkitc-1` default applies to that project |
| Bootloader | stock ESP-IDF second-stage bootloader (framework-supplied) |

---

## Related

- [`features/`](features/README.md) — per-capability procedures
- [`commands.md`](commands.md) — everything actually executed, with output
- [`coverage.md`](coverage.md) — which features have a build/test status
- [`examples/best.md`](examples/best.md) — which example to start from
