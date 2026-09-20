# Cardputer ADV — development and recovery

> Snapshot **2026-09-04**. **Nothing here was executed on hardware.** Commands are labelled
> `official` (published verbatim by M5Stack), `source` (read from a build config at a pinned
> commit) or `inferred`. See [`commands.md`](commands.md) for the full ledger.

## Frameworks at a glance

| Framework | Minimum for ADV | Board target | Notes |
|---|---|---|---|
| **Arduino** | `M5Cardputer` **1.1.1** + `M5Unified` + `M5GFX` + `IRremote` | `esp32-s3-devkitc-1` (vendor) or `m5stack-cardputer` | autodetect does the rest |
| **PlatformIO** | `platform = espressif32@6.7.0` | as above | vendor profile below |
| **ESP-IDF** | **5.4.2** (from the factory firmware's `sdkconfig.defaults` header) | `esp32s3` | factory firmware is IDF, not Arduino |
| **UiFlow2** | live service | `cardputer-adv` | `/en/uiflow2/cardputer-adv/program` — a **different** path from the v1.x's `/uiflow2/cardputer/` |
| **MicroPython** | via UiFlow2 firmware, or MicroHydra | — | see below |
| **Rust** | `Kezii/Rust-M5Stack-Cardputer` (GPL-3.0) | — | community HAL |

## 1. Arduino / PlatformIO

M5Stack publishes this profile on the ADV, v1.0 **and** v1.1 pages — identical text on all three
(`official`):

```ini
[env:m5stack-cardputer]
platform = espressif32@6.7.0
board = esp32-s3-devkitc-1
framework = arduino
upload_speed = 1500000
build_flags =
  -DESP32S3
  -DCORE_DEBUG_LEVEL=5
  -DARDUINO_USB_CDC_ON_BOOT=1
  -DARDUINO_USB_MODE=1
lib_deps =
  M5Cardputer=https://github.com/m5stack/M5Cardputer
```

Notes, from reading the library at `f1392858`:

* `library.json` declares `"version": "1.1.1"` and dependencies `M5Unified`, `M5GFX`,
  `arduino-irremote/IRremote`. `library.properties` additionally lists `LibSSH-ESP32` —
  **the two dependency lists disagree**; the Arduino IDE will try to pull LibSSH, PlatformIO
  will not. Harmless but confusing.
* `5604284` (2026-07-20) exists solely to "specify IRremote owner to resolve PlatformIO
  ambiguous package warning" — if you pin an older library you will see that warning.
* `board = esp32-s3-devkitc-1` is a **generic** target. It works because M5GFX detects the board
  at runtime. Bruce and Launcher instead use `board = m5stack-cardputer` with their own
  `pins_arduino.h`; Meshtastic uses `board = m5stack-stamps3`.

Minimal sketch:

```cpp
#include <M5Cardputer.h>
void setup() {
  auto cfg = M5.config();
  M5Cardputer.begin(cfg, true);           // second arg enables the keyboard
}
void loop() { M5Cardputer.update(); }
```

`M5Cardputer.begin()` → `M5.begin(cfg)` → M5GFX autodetect → `Keyboard.begin()` picks
`TCA8418KeyboardReader` or `IOMatrixKeyboardReader` from `M5.getBoard()`.

Build and upload (`inferred`, standard PlatformIO):

```bash
pio run -e m5stack-cardputer
pio run -e m5stack-cardputer -t upload
pio device monitor -b 115200
```

## 2. ESP-IDF — the factory firmware path

`github.com/m5stack/M5Cardputer-UserDemo`, branch **`CardputerADV`**, commit `b549eac0`
(2026-06-08). ESP-IDF **5.4.2**.

M5Stack **does not vendor its dependencies.** `repos.json` + `fetch_repos.py` clone five
repositories at pinned refs:

| Repo | Pinned ref |
|---|---|
| `m5stack/M5GFX` | branch **`0.2.15`** |
| `m5stack/M5Unified` | branch **`0.2.10`** |
| `Forairaaaaa/mooncake` | `v2.2.0` |
| `Forairaaaaa/mooncake_log` | `v1.3.0` |
| `Forairaaaaa/smooth_ui_toolkit` | `v2.4.0` |

⚠ **Those pins are older than the current library heads** (`M5GFX` is at `d91077b9`,
`M5Unified` at `8530f537` as of 2026-08-27). The shipped factory firmware is therefore **not
built from anything you can check out at `HEAD`** — the same pattern the PaperMono pass
recorded for M5Stack's demos. If you are chasing a behavioural difference between the factory
image and your own build, this is the first thing to check.

`dependencies.lock` additionally pins IDF components including `espressif/esp-now@2.5.2`,
`espressif/esp_tinyusb`, `espressif/cmake_utilities@0.5.3`.

```bash
git clone -b CardputerADV https://github.com/m5stack/M5Cardputer-UserDemo.git
cd M5Cardputer-UserDemo
python fetch_repos.py          # clones the five pinned repos into components/
idf.py set-target esp32s3
idf.py build
idf.py -p /dev/ttyACM0 flash monitor
```

`inferred` from the repository layout — not executed here.

`sdkconfig.defaults` highlights: `CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y`,
`CONFIG_PARTITION_TABLE_CUSTOM=y`, `CONFIG_EXAMPLE_KBD_ENABLE=y`,
`CONFIG_BT_NIMBLE_ENABLED=y`, `CONFIG_BT_NIMBLE_SVC_GAP_DEVICE_NAME="CardputerADV Keyboard"`,
`CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ_240=y`.

The application tree is worth reading even if you never build it — `main/hal/hal_config.h` is
the single most compact authoritative pin list for the ADV, and `main/hal/cap_lora868/` is
M5Stack's own SX1262 + GNSS integration (with a vendored `RadioLib` `EspHal.h` and
`TinyGPSPlus`).

> ⚠ **Licence caveat.** The demo is MIT, but it pins/vendors **RadioLib**, which is
> **LGPL-3.0 upstream**. The same flag was raised in the PaperMono pass. Flagged, not resolved.

## 3. UiFlow2

`https://docs.m5stack.com/en/uiflow2/cardputer-adv/program` — a distinct path from the v1.x's
`/en/uiflow2/cardputer/program`, which means M5Stack ships a **different UiFlow2 firmware** for
the ADV. Neither page was mined for substance in this pass (the PaperMono pass found M5Stack's
UiFlow2 pages "empty of substance"; expect the same). Recorded as a gap.

## 4. MicroPython

No official standalone MicroPython port page for the Cardputer was found. Two routes:

* **UiFlow2 firmware** is MicroPython underneath; `uiflow2.m5stack.com` and M5Burner deliver it.
* **MicroHydra** (`echo-lalia/MicroHydra`, GPL-3.0, ★314) is a MicroPython "OS-like" app
  switcher, with `echo-lalia/Cardputer-Micropython-Examples` (MIT, ★49) as a starting point.
  ADV support **not confirmed**.

## 5. Flashing, download mode and recovery

**Download mode** (`official`, identical wording on all three product pages):

> Set the side power switch to **OFF**. Then, **before powering on, hold the G0 button**, apply
> power, and release it afterwards. The device will then enter download mode.

There is **no reset button on the ADV**, so the usual "hold BOOT, tap RESET" does not apply.

**EasyLoader** (Windows one-click): `…/1178/Easy_Loader_for_Cardputer-Adv.exe`.
URL recorded; **not downloaded** in this pass.

**esptool** (`inferred` — flash offsets not verified against a real image):

```bash
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 1500000 \
  write_flash 0x0 bootloader.bin 0x8000 partition-table.bin 0x10000 app.bin
```

The factory `partitions.csv` puts the application at **`0x10000`** with a 4 MB `factory`
partition. **Do not treat the command above as authoritative**; it is the standard IDF layout
applied to the published partition table, not a procedure anyone has run here.

**Erase and start over** (`inferred`): `esptool.py --chip esp32s3 erase_flash`.

## 6. Bricking and hazard notes

* **No UART bridge.** If your firmware never brings up USB CDC, you lose the serial port. USB
  Serial/JTAG remains, and download mode always works — so the device is very hard to brick, but
  easy to make *look* bricked.
* **Charging needs the switch ON.** A flat battery plus a switch left OFF looks like a dead
  device.
* **G3 is both the CAP `RESET` line and an ESP32-S3 JTAG-source strap.** Holding it at a defined
  level through reset changes strapping.
* **Keep a recovery path.** The factory partition table has a **single `factory` app and no OTA
  slots**, so a bad flash means re-flashing over USB. `CCP101/cardputer-recoverable-multiboot`
  is the community answer: M5Launcher in `factory`, applications in OTA slots.
* **NVS layouts differ between firmwares.** Switching firmware commonly loses settings; reported
  for Plai on 2026-08-29.

## 7. Debugging

| Tool | Availability |
|---|---|
| USB Serial/JTAG console | native, always available |
| **JTAG** | the ESP32-S3's built-in USB-JTAG works over the same port; the MTDI/MTDO/MTCK/MTMS pins (G41/G40/G39/G42) are all consumed by audio and SD, so external JTAG is impractical |
| `CORE_DEBUG_LEVEL=5` | in the vendor profile; very verbose — reduce it for real work |
| M5GFX autodetect log | `[Autodetect] board_M5CardputerADV` — **your first diagnostic** |
| I²C scan | expect exactly `0x18`, `0x34`, `0x69` on G8/G9 |
