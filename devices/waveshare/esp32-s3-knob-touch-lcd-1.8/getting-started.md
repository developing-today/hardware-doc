# Getting started: actually developing on this board

> Written 2026-08-24. This is the **practical build guide**. It assumes you have the board in
> your hand and want to compile and flash your own code today.
>
> It deliberately does **not** re-explain the hardware. Where something is subtle or dangerous,
> it links to the page that treats it properly. Read [§8 Pitfalls](#8-pitfalls-you-should-read-before-your-first-build)
> before you flash anything.

**Read [§7 Back up the factory firmware](#7-back-up-the-factory-firmware-before-you-overwrite-it) first if
you care about the Bluetooth functionality.** Waveshare publishes **no source** for the ESP32
Classic-Bluetooth firmware. Overwrite it without a backup and it is gone.

---

## Contents

1. [Which MCU am I talking to?](#1-which-mcu-am-i-talking-to)
2. [Step zero: restore the demo dependencies](#2-step-zero-restore-the-demo-dependencies)
3. [The Arduino path (ESP32-S3)](#3-the-arduino-path-esp32-s3)
4. [The ESP-IDF path (ESP32-S3)](#4-the-esp-idf-path-esp32-s3)
5. [The eight vendor ESP-IDF examples](#5-the-eight-vendor-esp-idf-examples)
6. [The other MCU: ESP32-U4WDH](#6-the-other-mcu-esp32-u4wdh)
7. [Back up the factory firmware before you overwrite it](#7-back-up-the-factory-firmware-before-you-overwrite-it)
8. [Pitfalls you should read before your first build](#8-pitfalls-you-should-read-before-your-first-build)
9. [Where to go next](#9-where-to-go-next)

---

## 1. Which MCU am I talking to?

This board has **two independent MCUs** sharing one USB-C connector:

| | Chip | Role | Toolchain |
|---|---|---|---|
| `U2` | **ESP32-S3R8** | Display, touch, knob 1, SD, mic, GUI. **This is the one you develop on.** | Arduino core ≥ 3.2.0, or ESP-IDF 5.1.4 |
| `U14` | **ESP32-U4WDH** | Classic Bluetooth / A2DP audio, DAC mute, knob 2 | **Nothing is published.** No source, no example, no header |

### The USB-C flip selects which one enumerates

There is no switch and no UI for this. **Which chip you can flash depends on which way round
the USB-C plug is inserted.** Rotate the plug 180°, re-enumerate, and you are talking to the
other chip.

Never assume. Always ask the board:

```sh
esptool --port /dev/ttyACM0 chip_id
# "Chip is ESP32-S3 (QFN56) ..."    -> the GUI MCU, native USB
# "Chip is ESP32-U4WDH (revision ...)" -> the Bluetooth MCU, via the USB-serial bridge
```

> `esptool` **4.3 or newer** is required to print `ESP32-U4WDH` correctly; 4.2.1 and older
> report the silicon revision as `3` rather than `v3.1`.

Because the two chips enumerate through different paths (S3 = native USB CDC, U4WDH = the
CH34x bridge), **the port name usually changes too.** On Linux the S3 typically appears as
`/dev/ttyACM*` and the U4WDH as `/dev/ttyUSB*`. That is a useful hint but not a guarantee —
run `chip_id` anyway.

Full treatment, including the evidence boundary (the schematic does **not** show this
mechanism — it is a vendor claim, corroborated by users):
[dual-mcu-architecture.md §1](dual-mcu-architecture.md#1-the-usb-c-orientation-flip).

---

## 2. Step zero: restore the demo dependencies

The vendor demo tree is committed here:

```
artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/
├── Arduino/
│   ├── examples/            # Arduino sketches
│   └── libraries/
│       └── lv_conf.h        # <-- KEPT. board-specific. see below
├── ESP-IDF/                 # eight independent IDF projects
└── Firmware/                # the two factory .bin images
```

Two bundled third-party libraries were **removed** from it, because they are exactly
reproducible from upstream and together weigh ~200 MiB:

| Library | Version | Path the build expects |
|---|---|---|
| LVGL | 8.4.0 | `Arduino/libraries/lvgl/` |
| SensorLib | 0.3.1 | `ESP-IDF/03_DRV2605_Test/components/SensorLib/` |

`tools/restore-demo-deps.sh` puts them back, byte-for-byte, from GitHub.

```sh
# Work on a COPY. The committed tree is deliberately kept without these deps,
# and the script refuses to write into it.
cp -a artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo ~/knob-demo

./tools/restore-demo-deps.sh --dest ~/knob-demo
```

It downloads the pinned upstream tags, verifies their SHA-256, applies Waveshare's two one-line
patches, and then verifies the resulting trees against recorded content digests. It is
idempotent — re-running it on an already-correct tree does nothing. It fails loudly rather than
producing a tree it cannot vouch for.

Full documentation, including the two patches and what they fix:
[`tools/README.md`](tools/README.md).

### ⚠ `lv_conf.h` is **not** part of LVGL and must stay where it is

```
Arduino/libraries/lv_conf.h        <-- committed, board-specific, NOT restored by the script
Arduino/libraries/lvgl/            <-- restored by the script
```

`lv_conf.h` is Waveshare's LVGL build configuration for *this panel*: colour depth, buffer
strategy, enabled widgets, font set. It is **not** an upstream LVGL file and is **not**
reproducible from the LVGL repository. It survived the dependency removal precisely because it
lives one directory **above** `lvgl/`, which is also where LVGL's own build system expects to
find it (`lv_conf.h` is included from the parent of the library directory).

**Do not move it inside `lvgl/`. Do not replace it with upstream's `lv_conf_template.h`.**
If you delete it, restore it from this repository — the script cannot regenerate it.

---

## 3. The Arduino path (ESP32-S3)

### 3.1 Versions

| Component | Version | Note |
|---|---|---|
| **Arduino IDE** | current **2.x** | Waveshare specifies no version. 1.8.x is not a sensible target for a core ≥ 3.2.0 |
| **`esp32` by Espressif Systems** board package | **≥ 3.2.0** | Vendor requirement. A **2.x core will not build these examples** — the 2.x→3.x boundary is a large peripheral-API break |
| **LVGL** | **8.4.0 exactly** | Install *offline*, from `Arduino/libraries/lvgl` after running the restore script |
| **SensorLib** | **0.3.1** | Library Manager (`SensorLib@0.3.1`) or offline |

> **⚠ LVGL 9 will not work.** The Library Manager offers 9.x and the wiki links
> `docs.lvgl.io/master` (which is 9.x) — both are traps. LVGL 9 is not API-compatible with 8.4.
> Use <https://docs.lvgl.io/8.4/>. This is a documented vendor error; see
> [development.md § Reconciliation notes](development.md#reconciliation-notes).

### 3.2 Installing the libraries offline

Point the Arduino IDE's sketchbook `libraries/` directory at, or copy from, the restored tree:

```sh
cp -a ~/knob-demo/Arduino/libraries/lvgl      ~/Arduino/libraries/
cp -a ~/knob-demo/Arduino/libraries/lv_conf.h ~/Arduino/libraries/   # sibling of lvgl/, not inside it
```

The `lv_conf.h` placement above is the single most common cause of "it compiles but the screen
is blank/garbled".

### 3.3 Board settings (Tools menu)

Waveshare publishes these only as a screenshot. These are the values that matter:

| Setting | Value | Why |
|---|---|---|
| **Board** | **ESP32S3 Dev Module** | *Not* "ESP32 Dev Module" — that is the **other** chip on this board |
| **Flash Size** | **16 MB (128 Mb)** | |
| **PSRAM** | **OPI PSRAM** | **Omitting this is the classic cause of LVGL allocation failures.** The S3R8 has octal PSRAM; the default setting is wrong |
| **Flash Mode** | QIO 80 MHz | |
| **Partition Scheme** | one with **≥ 4 MB app** | The stock default is too small for an LVGL sketch |
| **USB CDC On Boot** | **Enabled** | Required if you want the serial monitor over the S3's native USB |
| **Upload Speed** | 921600 | |

> **⚠ 120 MHz octal PSRAM is temperature-fragile on the S3.** If you are tempted to raise the
> PSRAM clock, read
> [esp-idf-peripheral-capabilities.md §4.3](../../../guides/espressif/esp-idf-peripheral-capabilities.md#43-esp32-s3--120-mhz-octal-psram-is-temperature-fragile)
> first. Leave it at 80 MHz.

### 3.4 First compile is very slow

Expect several minutes on a first build — the ESP32 core compiles a large amount of framework
code, and LVGL 8.4 with the demos duplicated under `src/demos/` is a lot of translation units.
Subsequent builds are cached. This is normal and is
[FAQ item 5](faq-and-troubleshooting.md#5-how-to-deal-with-the-first-compilation-of-the-program-being-extremely-slow).

---

## 4. The ESP-IDF path (ESP32-S3)

### 4.1 Version

**ESP-IDF v5.1.4**, target `esp32s3`.

An important caveat on that number: **5.1.4 is never stated in prose anywhere on the vendor
wiki.** It appears only inside a documentation URL in a note box. Treat it as *the version
Waveshare tested*, not a hard floor — the `sdkconfig` files shipped with each example are the
real authority for what builds. All eight examples set `CONFIG_IDF_TARGET="esp32s3"` and
`CONFIG_ESPTOOLPY_FLASHSIZE="16MB"`.

### 4.2 Build, flash, monitor

Each of the eight examples is an **independent IDF project** — there is no top-level project.
`cd` into the one you want:

```sh
. $IDF_PATH/export.sh

cd ~/knob-demo/ESP-IDF/08_LVGL_Test

idf.py set-target esp32s3          # only needed if you clear the build dir
idf.py build

# Confirm you are on the S3 before flashing (see §1)
esptool --port /dev/ttyACM0 chip_id

idf.py -p /dev/ttyACM0 flash monitor
# Ctrl-] to exit the monitor
```

Useful extras:

```sh
idf.py menuconfig            # change sdkconfig (e.g. enable long filenames — see §8)
idf.py fullclean             # when switching target or after odd link errors
idf.py -p PORT erase-flash   # nuclear option; also wipes nvs
```

> If the serial port shows `waiting for download...` after a successful flash, that is
> [FAQ item 6](faq-and-troubleshooting.md#6-how-to-handle-the-display-waiting-for-download-on-the-serial-port-after-successfully-esp-idf-flashing) —
> power-cycle with the physical switch.

### 4.3 A note on PlatformIO

The wiki documents only Arduino IDE and ESP-IDF, but a community PlatformIO board definition
exists and several projects use it successfully. See
[examples/catalog.md](examples/catalog.md).

---

## 5. The eight vendor ESP-IDF examples

All eight target the **ESP32-S3 only**. There is **no Bluetooth Classic example, no Bluetooth
audio example, and no inter-MCU UART example anywhere in the archive.**

| # | Example | What it demonstrates | Interfaces |
|---|---|---|---|
| 01 | `01_ADC_Test` | Reading the battery divider / system voltage | ADC1 ch0, GPIO1 |
| 02 | `02_SD_Card` | Mount, read and write a FAT card | 4-bit SDMMC, GPIO2–6, 42 |
| 03 | `03_DRV2605_Test` | Cycling haptic waveform effects | I²C GPIO11/12, addr `0x5A`, **SensorLib** |
| 04 | `04_Encoder_Test` | Counting knob direction and events | GPIO8/7 — **knob 1 only**; knob 2 belongs to the other MCU |
| 05 | `05_WIFI_AP` | Running a Wi-Fi access point | S3 radio |
| 06 | `06_WIFI_STA` | Joining a Wi-Fi network | S3 radio |
| 07 | `07_Audio_Test` | PDM microphone → I²S DAC | PDM GPIO45/46; I²S GPIO39/40/41. **Depends on the DAC being un-muted by the *other* MCU** — see §8 |
| 08 | `08_LVGL_Test` | Display + touch GUI, backlight | QSPI LCD, CST816 touch over I²C, LVGL 8.4.0 |

`08_LVGL_Test` is the one to start from for anything with a UI. `03_DRV2605_Test` is the one
that needs SensorLib restored.

> **Display driver caveat.** The example declares 360×360 RGB565 over SPI2 QSPI with a driver
> named `esp_lcd_sh8601`, while the product identity says **ST77916**. Community practice has
> converged on the *bus parameters* rather than the name: `esp_lcd_sh8601` at **40 MHz, 32-bit
> QSPI command frames, `quad_mode` enabled**. 8-bit commands at 20 MHz reportedly give a blank
> or garbled screen. Keep the vendor command table and timings together.
> [development.md § Display driver note](development.md#display-driver-note).

---

## 6. The other MCU: ESP32-U4WDH

**Waveshare ships no source code for it at all.** It exists in the published materials only as
the prebuilt blob `Firmware/ESP32-KNOB_ESP32_0.bin`.

You *can* develop for it — it is an ordinary ESP32 (target `esp32`, 4 MB flash) and IDF will
build for it happily. But doing so means **replacing** the Classic Bluetooth application, and
you cannot get it back except from that binary. See §7.

If your project needs the two MCUs to talk, the physical layer is two wires (S3 `GPIO38` →
ESP32 `GPIO18`, ESP32 `GPIO23` → S3 `GPIO48`, both on UART1), cross-connected, full duplex,
**no flow-control wires**. The **baud rate of the stock protocol is unknown** and the protocol
itself is undocumented. Do not guess it — reflash both ends and define your own.
[dual-mcu-architecture.md §2](dual-mcu-architecture.md#2-the-inter-mcu-link-a-two-wire-uart)
has the bandwidth arithmetic and a working `uart_param_config` skeleton for both ends.

Leaving the secondary MCU running idle costs roughly **50 mA**
([development.md](development.md#the-secondary-mcu-costs-50-ma-if-you-leave-it-alone)).

---

## 7. Back up the factory firmware before you overwrite it

> **`ESP32-KNOB_ESP32_0.bin` is the only copy of the Classic Bluetooth application that exists.
> There is no source. If you lose it, you cannot rebuild it.**

Waveshare still publishes it, so it is re-downloadable *today* — but vendor links rot. More
importantly, **a `read_flash` backup captures things the published image does not**: your `nvs`
partition (Bluetooth pairing records under the `PEERADDR` key, Wi-Fi credentials, settings) and
the 1408 KB `storage` SPIFFS partition, whose contents are undocumented and are **not** in the
published binary.

Do this **before your first flash**, for **both** chips.

### 7.1 Back up

```sh
# --- Chip A: insert USB-C in the orientation that gives you the ESP32-U4WDH ---
esptool --port PORT chip_id            # MUST print "ESP32-U4WDH"
esptool --chip esp32   --port PORT --baud 921600 \
        read_flash 0x0 0x400000  esp32-u4wdh-full-backup.bin      # 4 MB

# --- Chip B: unplug, FLIP THE PLUG 180°, replug ---
esptool --port PORT chip_id            # MUST print "ESP32-S3"
esptool --chip esp32s3 --port PORT --baud 921600 \
        read_flash 0x0 0x1000000 esp32s3-full-backup.bin          # 16 MB, slower

sha256sum esp32-u4wdh-full-backup.bin esp32s3-full-backup.bin
# record these somewhere durable, off this machine
```

| MCU | `--chip` | Offset | Size | Flash |
|---|---|---|---|---|
| ESP32-U4WDH (`U14`) | `esp32` | `0x0` | `0x400000` | 4 MB |
| ESP32-S3R8 (`U2`) | `esp32s3` | `0x0` | `0x1000000` | 16 MB |

### 7.2 Known-good hashes of the *published* images

For verifying a fresh download (these are the vendor images, **not** your `read_flash` dumps,
which will differ because they include your `nvs`):

| File | Size | SHA-256 |
|---|---:|---|
| `ESP32-KNOB_ESP32_0.bin` | 1,130,672 | `0c1c21b9822d4c2d80d58534b33eb0083880de4ed7354a38b4c78ba51757349d` |
| `WX-ESP32S3-KNOB_V1.2.bin` | 2,138,224 | `f7c1cc18b687559f3bd69e5c9ab526bc61c2b2d9c502f38367f7f2bfe4ff8e87` |

Both are committed in this repository at
[`artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/`](artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/).

### 7.3 Restore

Full factory state = **both** images, flashed in **both** orientations.

```sh
# 1. Verify your files against the hashes above.

# 2. Plug in. Identify what you are on. Do NOT force --chip for this step.
esptool --port PORT chip_id

# 3. Flash whichever chip that is, at offset 0x0.
esptool --chip esp32   --port PORT --baud 921600 write_flash -z 0x0 ESP32-KNOB_ESP32_0.bin
#   ...or...
esptool --chip esp32s3 --port PORT --baud 921600 write_flash -z 0x0 WX-ESP32S3-KNOB_V1.2.bin

# 4. Unplug. FLIP THE PLUG 180°. Plug back in.
# 5. Repeat steps 2-3 for the other chip.
# 6. Power-cycle with the physical switch.
```

If you took a full `read_flash` backup, **restore that instead** of the published image — it
brings back your `nvs` and `storage` contents too:

```sh
esptool --chip esp32 --port PORT --baud 921600 write_flash -z 0x0 esp32-u4wdh-full-backup.bin
```

Notes:

- **`write_flash 0x0` overwrites `nvs`** — Wi-Fi credentials and Bluetooth pairings are erased.
  You will re-pair afterwards.
- To reset pairing *without* a full reflash, the stock UI has `Clear BT A2DP pair`:
  [factory-firmware.md](factory-firmware.md#resetting-bluetooth-pairing-without-a-full-reflash).
- If a flash fails or the port vanishes: unplug, flip, re-plug, re-run `chip_id`. Per
  Waveshare's own FAQ that is the first thing to try for essentially every symptom.

Deeper treatment:
[dual-mcu-architecture.md §6.2](dual-mcu-architecture.md#62--back-up-the-factory-esp32-image-before-you-touch-it)
and [factory-firmware.md](factory-firmware.md).

---

## 8. Pitfalls you should read before your first build

These are documented properly elsewhere in this repository. They are listed here because each
one has cost somebody a debugging session, and none of them is obvious from the vendor
materials. **Links, not duplicates** — go read the source page.

| Pitfall | Why it bites | Read |
|---|---|---|
| **DRV2605L is configured for ERM, but the actuator is an LRA** | Both vendor demos select an ERM effect library for what is physically an LRA. Haptics feel weak or wrong, and the drive waveform is not what the actuator wants | [drv2605l §4.3](../../../components/texas-instruments/drv2605l/README.md#43--both-vendor-demos-select-an-erm-library-for-an-lra-actuator) · [lra-motor §2](../../../components/generic/lra-motor/README.md#2-lra-versus-erm--why-the-distinction-matters-here) |
| **The "encoders" are not quadrature encoders** | They are detector/detent switches. If you write standard quadrature decoding you will get nonsense. Direction must be derived differently | [sscm110100 §2.1](../../../components/alps-alpine/sscm110100/README.md#21-it-is-not-a-quadrature-rotary-encoder) |
| **GPIO0 has three jobs** | BOOT strap (10 kΩ pull-up), *and* the CH445P audio mux select, *and* an expansion-header pin. Drive it after boot, never during. Get it wrong and audio goes silent or the board won't boot | [esp32-s3-boot-button §3](../../../components/generic/esp32-s3-boot-button/README.md#3--gpio0-has-three-jobs-on-this-board) · [ph1.27 §3.3](../../../components/generic/ph1.27-expansion-connectors/README.md#33-gpio0--pin-8-and-why-it-is-the-dangerous-one) |
| **The DAC mute line (`XSMT`) belongs to the *other* MCU** | The S3 physically cannot un-mute the PCM5100A. If you reflash the U4WDH, nothing un-mutes the DAC and **all** audio dies — including SD-card playback from the S3. This is the single nastiest failure mode on the board | [pcm5100a §7.1](../../../components/texas-instruments/pcm5100a/README.md#71--the-xsmt-ownership-trap--read-this-before-you-erase-anything) |
| **FATFS is built with 8.3 short filenames only** | `CONFIG_FATFS_LFN_NONE=y` in the shipped `sdkconfig`, codepage 437. Long or non-ASCII filenames silently "do not exist" on a card that clearly contains them | [micro-sd-sdmmc §4.2](../../../components/generic/micro-sd-sdmmc/README.md#42--long-filenames-are-disabled) |
| **The microSD socket has no card-detect** | No CD pin is wired, and no write-protect either. You cannot know a card is present without trying to mount it, and hot-swap is undetectable | [micro-sd-sdmmc §5.2](../../../components/generic/micro-sd-sdmmc/README.md#52-no-card-detect) |

More, including things the vendor FAQ does not cover:
[gaps-and-conflicts.md](gaps-and-conflicts.md) ·
[faq-and-troubleshooting.md § Problems the vendor FAQ does not cover](faq-and-troubleshooting.md#problems-the-vendor-faq-does-not-cover).

---

## 9. Where to go next

| Page | What it gives you |
|---|---|
| [dual-mcu-architecture.md](dual-mcu-architecture.md) | The definitive who-owns-which-peripheral table, the USB-C flip, the inter-MCU UART, OTA capability |
| [factory-firmware.md](factory-firmware.md) | Image internals, partition tables, full restore procedure, provenance of both binaries |
| [development.md](development.md) | The vendor toolchain audit, every version Waveshare states, and where each claim comes from |
| [faq-and-troubleshooting.md](faq-and-troubleshooting.md) | The vendor FAQ in the vendor's own words, with commentary |
| [factory-demo-apps.md](factory-demo-apps.md) | What the preinstalled apps do, and the SD-card layout they need |
| [pinouts-and-buses.md](pinouts-and-buses.md) | Pin assignments traced to the schematic |
| [examples/catalog.md](examples/catalog.md) | 28 community projects, a PlatformIO board definition, a working SquareLine Studio project |
| [tools/README.md](tools/README.md) | The dependency restore script in detail |
| [gaps-and-conflicts.md](gaps-and-conflicts.md) | What is still unresolved — read before trusting any single number |
