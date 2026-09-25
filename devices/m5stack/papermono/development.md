# Development and recovery — M5Stack PaperMono

> Board **C153**, schematic revision **V0.6.2** · research snapshot **2026-09-01**.
>
> ## ⚠ Nothing on this page was executed against hardware
>
> **There is no PaperMono in this session and there never was.** Every command below is
> `reported-working` (transcribed from a vendor document or a vendor README) or `inferred`
> (derived from the build files, the shipped binary, or standard framework behaviour).
> **No command on this page carries `executed-success`**, because the only things executed
> in this pass were static analyses of files on disk — those are ledgered in
> [`commands.md`](commands.md), which is the authoritative record of what actually ran.

This is the §9 development-and-recovery record: what to build with, what versions, what to
flash, through which port, how to put the factory image back, and what can leave you with a
board you cannot talk to. It **consolidates and cross-links** rather than repeats:

| For | Go to |
|---|---|
| Port wiring, USB-PD absence, console behaviour, debugging symptoms | [`features/usb-and-serial.md`](features/usb-and-serial.md) |
| The verbatim command ledger with tool versions and execution status | [`commands.md`](commands.md) |
| What is inside the shipped images, and the restore evidence | [`factory-firmware.md`](factory-firmware.md) |
| GPIO map, strapping pins, bus ownership | [`pinouts-and-buses.md`](pinouts-and-buses.md) · [`resources-and-conflicts.md`](resources-and-conflicts.md) |
| Per-capability API guides | [`features/`](features/README.md) |

## Contents

- [1. Supported frameworks and exact versions](#1-supported-frameworks-and-exact-versions)
- [2. Board target and profile](#2-board-target-and-profile)
- [3. The vendor PlatformIO block, verbatim](#3-the-vendor-platformio-block-verbatim)
- [4. Required libraries and versions](#4-required-libraries-and-versions)
- [5. Build, flash and monitor](#5-build-flash-and-monitor)
- [6. USB, UART and debug-port selection](#6-usb-uart-and-debug-port-selection)
- [7. Factory restore and flash offsets](#7-factory-restore-and-flash-offsets)
- [8. Known bricking and bootstrapping risks](#8-known-bricking-and-bootstrapping-risks)
- [9. What is not established](#9-what-is-not-established)

---

## 1. Supported frameworks and exact versions

| Framework | Minimum / recommended | Evidence | Status |
|---|---|---|---|
| **ESP-IDF** | **5.5.1** | `M5PaperMono-UserDemo/dependencies.lock` (`idf: version: 5.5.1`); `M5PaperMono-OTP-Demo/README.md` states "ESP-IDF v5.5.1"; the shipped binary's `esp_app_desc_t` reports `idf_version v5.5.1` — **three independent confirmations** (S41, S42, S38) | `reported-working` |
| **arduino-esp32** | **3.3.10** as an ESP-IDF managed component | `M5PaperMono-UserDemo/dependencies.lock` (S41) | `reported-working` |
| **arduino-esp32** | **3.3.9** is the earliest core in evidence that carries the board variant | `tanakamasayuki/M5Stack-Arduino-Check` contains `3.3.9/variants/m5stack_papermono/pins_arduino.h` (S96) | `inferred` |
| **PlatformIO** | `platform = espressif32@6.12.0`, `framework = arduino` | vendor product page (S01), reproduced verbatim in §3 | `reported-working` |
| **Arduino IDE** | **no version stated anywhere** | S07 names no IDE version and no board-package version | gap |
| **UiFlow2** | **advertised, undocumented** | S09 states no required firmware version, no block list, no limitations — established by full-text search of the retrieved page, so this is a documentation gap, not a retrieval failure ([G4](gaps-and-conflicts.md#g4--uiflow2-support-is-advertised-but-undocumented)) | gap |

**Both arduino-esp32 rows are true, and they are not in conflict.** 3.3.10 is what the vendor's
own ESP-IDF project pins as a managed component and is therefore what built the shipped image;
3.3.9 is the earliest *Arduino core* release in which a third-party inventory shows the
`m5stack_papermono` variant directory existing. They are statements about two different
artifacts, recorded separately so a later pass does not "resolve" one of them as an error —
see [C17](gaps-and-conflicts.md#c17--arduino-esp32-version-differs-between-sources).

**Newer ESP-IDF demonstrably works, from community evidence.** The third-party CrossPoint
image ([`factory-firmware.md` §3](factory-firmware.md#3-the-community-image--crosspoint-paper-mono-cjk-150-rc)) reports `idf_version 5.5.2.260206` and boots on the same board.
That is one data point from a shipped binary, not a support statement: **5.5.1 remains the
only version M5Stack pins.**

## 2. Board target and profile

| Layer | Identifier | Where it comes from |
|---|---|---|
| Arduino IDE board menu | **`M5PaperMono`** | S07; independently corroborated by the string `[Autodetect] board_M5PaperMono` in the shipped binary (S38) |
| arduino-esp32 variant directory | **`m5stack_papermono`** | S96 (`3.3.9/variants/…/pins_arduino.h`) |
| M5Unified / M5GFX board enum | **`board_M5PaperMono`** (`= 29` in M5Unified) | S46, S47 |
| PlatformIO board | **`esp32-s3-devkitm-1`** — a generic devkit, reconfigured by flags | S01 |
| ESP-IDF target | `esp32s3` | both `sdkconfig.defaults` and `dependencies.lock` (S41, S42) |

**There is no PlatformIO board definition for the PaperMono.** The vendor uses a generic
ESP32-S3 devkit profile and fixes it up with `board_build.*` and `build_flags`. Practical
consequence: PlatformIO will not warn you about anything board-specific — not the flash size,
not the PSRAM mode, not the partition scheme. Every one of those is your responsibility, and
getting the PSRAM one wrong produces a board that looks dead (§8).

**M5GFX cannot tell a C153 from a C153-LITE.** Both map to the single enum
`board_M5PaperMono`, with NFC masked out of the detection test (`M5GFX.cpp:1945`). Variant
detection is an *application-layer* job: the factory firmware powers the NFC rail through
M5IOE1 `PYG4` and reads the ST25R3916 identity register, declaring `Lite` if either step
fails (`hal_board.cpp:160–172`, S41). If your code needs to know which SKU it is running on,
you must do the same thing yourself. `inferred` from source; `not-tested`.

## 3. The vendor PlatformIO block, verbatim

Reproduced exactly as published on the PaperMono product page (S01). It is the only build
configuration M5Stack publishes anywhere. **`reported-working`; not built here.**

```ini
[env:m5stack-papermono]
platform = espressif32@6.12.0
board = esp32-s3-devkitm-1
framework = arduino
board_build.partitions = default_16MB.csv
board_upload.flash_size = 16MB
board_upload.maximum_size = 16777216
board_build.arduino.memory_type = qio_opi
build_flags =
    -DESP32S3
    -DBOARD_HAS_PSRAM
    -mfix-esp32-psram-cache-issue
    -DCORE_DEBUG_LEVEL=0
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
lib_deps =
    M5Unified = https://github.com/m5stack/M5Unified#develop
    M5PM1 = https://github.com/m5stack/M5PM1
    M5IOE1 = https://github.com/m5stack/M5IOE1
    M5Unit-NFC=https://github.com/m5stack/M5Unit-NFC
    RadioLib = https://github.com/jgromes/RadioLib
```

The **PaperMono-Lite** page (S04) publishes the same block with exactly two differences: the
environment is `[env:m5stack-papermono-lite]`, and `M5Unit-NFC` and `RadioLib` are absent from
`lib_deps`.

### Five things to change or know about this block

| # | Line | What is wrong or worth knowing |
|---|---|---|
| 1 | `board_build.arduino.memory_type = qio_opi` | **Do not remove this.** The `opi` half is load-bearing (§8.1). The `qio` half is cosmetic on this board: the shipped binaries report **DIO** in their image headers, `sdkconfig.defaults` pins no flash mode, and the hardware supports QIO either way — [R2](gaps-and-conflicts.md#r2--qio-versus-dio-flash--resolved) |
| 2 | `M5Unified#develop` | **Stale.** `board_M5PaperMono` is byte-identical on `master` and `develop` and ships in released tags M5Unified 0.2.21 / M5GFX 0.2.28 — [R5](gaps-and-conflicts.md#r5--m5unifieddevelop-requirement--resolved-the-instruction-is-stale). Use the release |
| 3 | `M5UnitUnified` absent | The Arduino quick-start page (S07) lists it among seven required libraries; this block omits it. If you follow the Arduino page and the PlatformIO block at once you get two different dependency sets |
| 4 | `-DCORE_DEBUG_LEVEL=0` | Compiles out the diagnostics you need — including M5GFX's `"M5PaperMono need OPI-PSRAM enabled"`. **Raise it to 3 or 4 while bringing a board up** |
| 5 | `board_build.partitions = default_16MB.csv` | This is the *Arduino* default 16 MB scheme, which has **two OTA app slots**. It is **not** the layout the factory image uses (a single 15 MiB `factory` app, no OTA). The two vendor projects and the vendor build block disagree about the flash map — see [`factory-firmware.md` §4](factory-firmware.md#4-partition-maps--three-different-layouts-are-in-evidence) |

Point 5 is the one that is easy to miss and hard to debug later. Nothing breaks at build time;
you simply end up with a different flash geometry from the shipped product, which matters the
moment you try to compare behaviour against the factory image or restore it.

## 4. Required libraries and versions

The vendor names libraries without versions in every place it names them. The versions below
come from the release tags and, where the shipped firmware is concerned, from the exact commits
pinned in `M5PaperMono-UserDemo/repos.json` (S41).

| Library | Release tag (2026-09-01) | Commit pinned by the factory firmware | Role |
|---|---|---|---|
| **M5Unified** | **0.2.21** (2026-08-26) | `develop` @ `2fe93c0c64f12f916e73a0605c86bf1241c06a6b` | Board abstraction, I²C bring-up, button/RTC/IMU wrappers |
| **M5GFX** | **0.2.28** (2026-08-25) | `develop` @ `02107b828acb3eb782fccd747863638d64c876d7` | Panel driver, expander bring-up, frontlight PWM |
| **M5PM1** | **1.0.7** (repo HEAD `be9a5456c007c333e7ac963f33bfde1ffa5d82ee`) | registry `m5stack/m5pm1` 1.0.7 | Power manager — rails, wake, shutdown, PWM |
| **M5IOE1** | **1.0.9** (repo HEAD `846eec7d05e25c09013be2acdb8804487f48a62e`) | registry `m5stack/m5ioe1` 1.0.9 | I/O expander — panel/touch/SD/mic power, resets, LEDs |
| **M5Unit-NFC** | no release tag located | `0.1.0` @ `93745b547364f310cd64b5155a870103a7800a5d` | ST25R3916 driver (C153 only) |
| **RadioLib** | **7.2.1** | `7.2.1` @ `b91c6af112e423dcb14529ade5827802a14e1015` | SX1262 LoRa stack (C153 only) |
| M5UnitUnified | — | `0.5.5` @ `bf711f370047cf16355b00005450ef615fab36e2` | Required by S07, absent from the PlatformIO block |
| M5Utility | — | `0.1.0` @ `5b5ed9626bc4c1cf81ec6039a34e33c901b5b68f` | transitive |
| M5HAL | — | `0.1.2` @ `0f06f9d3134706ce030fd5515601cce65a267233` | transitive |
| mooncake | — | `v2.3.3` @ `572a7e488641f1c3f22e85d65c27f095ecf27d12` | App framework used by the factory demo |
| LGFX_Fonts | — | `1.1.2` @ `253cf549fe0b1aa932be68fe06a13c3077918d61` | Fonts |
| Arduino_BMI270_BMM150 | — | `1.2.3` @ `a599119044554015e06735f9d7187fc56295b9b6` | A *third* BMI270 driver in the same tree |

**Two things about this table matter more than the numbers.**

*The factory firmware does not build from released libraries.* It pins `develop` branch commits
of M5Unified and M5GFX, fetches ten repositories with `fetch_repos.py` rather than vendoring
them, and applies eight local patches. Those patches were read in full: they are **build
plumbing only** — `arduino-esp32` → `espressif__arduino-esp32` in CMake, plus dropping a
duplicate `m5gfx` dependency — and **no pin, register or waveform is patched**. That is a
genuinely useful negative result: all PaperMono board knowledge lives upstream in
M5GFX/M5Unified, none of it is private to the firmware, so a release-tag build has the same
board support the factory image does. Recorded also in
[`compatibility-and-status.md` §3.2](compatibility-and-status.md#32--version-specific-report-the-factory-firmware-is-not-built-from-released-libraries).

*RadioLib's licence is not MIT.* The demo repositories are MIT, but RadioLib is LGPL-3.0
upstream and is fetched into `components/` rather than vendored. Nobody in this pass verified
what obligations that creates for a derived binary; it is flagged, `not-tested`, and it is the
one licence question on this board that could actually matter to a product.

## 5. Build, flash and monitor

### 5.1 ESP-IDF — the path the vendor actually used

`reported-working`, transcribed from `M5PaperMono-OTP-Demo/README.md` (S42):

```bash
idf.py set-target esp32s3
idf.py build
idf.py -p PORT flash
```

For the **UserDemo** (S41) the dependencies are not vendored, so they must be fetched first:

```bash
python3 fetch_repos.py     # clones 10 repos at pinned commits into components/, applies patches/
idf.py set-target esp32s3
idf.py build
idf.py -p PORT flash
```

`inferred` — `fetch_repos.py` was read but **not run**, and the UserDemo README was not read in
full for build steps.

Monitoring is not in either README. Standard IDF usage would be:

```bash
idf.py -p PORT monitor          # inferred; console baud not stated by the vendor anywhere
idf.py -p PORT flash monitor    # inferred
```

`inferred`, `not-tested`. The vendor's M5Burner page (S09) exposes a `BaudRate` field but does
not say what value the device uses; the ESP-IDF default is 115200 and nothing in
`sdkconfig.defaults` overrides it, so 115200 is the reasonable first guess — **an inference,
not a reading**.

### 5.2 PlatformIO

`inferred` (standard PlatformIO usage against the vendor's own env block; not run):

```bash
pio run -e m5stack-papermono                 # build
pio run -e m5stack-papermono -t upload       # build + flash
pio device monitor -b 115200                 # console
```

### 5.3 Arduino IDE

`reported-working`, from S07:

1. Install the M5Stack board package.
2. Install seven libraries: `M5Unified`, `M5GFX`, `M5PM1`, `M5IOE1`, `M5UnitUnified`,
   `M5Unit-NFC`, `RadioLib` — "then install all prompted dependencies". **No versions given
   for any of them**; use §4.
3. Select the **`M5PaperMono`** board.
4. Enter download mode (§6.3).
5. The page tells you to open the **`BarGraph`** example and click Upload. A bar-graph demo
   corresponds to none of the 14 advertised API sub-pages and reads as boilerplate carried
   over from another product. Reproduced because it is what the vendor says; **flagged
   because it is probably not what you want.**

### 5.4 M5Burner / EasyLoader — the GUI route

M5Burner is also how UiFlow2 firmware is installed. Two PaperMono images are listed
(§7 and [`factory-firmware.md`](factory-firmware.md)). A Windows EasyLoader executable
`C153-PaperMono-UserDemo_0x00.exe` is linked from **both** the PaperMono and the
PaperMono-Lite pages, and it lives under PaperMono's asset folder `1267/`, not the Lite's
`1268/` — corroborating that **one image serves both SKUs** (S40, S33). The executable was
**not retrieved**; a Windows binary was out of scope for this pass.

> ⚠ **M5Burner's device filter will not protect you.** Both listings carry
> `deviceName: "Paper"` — the same family key used across M5Stack's Paper line. The catalogue
> therefore does not distinguish a PaperMono image from an M5Paper or PaperS3 image.
> `inferred` from the M5Burner API records (S33, S35); `not-tested`.

## 6. USB, UART and debug-port selection

Full wiring, the USB-PD analysis and the debugging symptom table are in
[`features/usb-and-serial.md`](features/usb-and-serial.md). The selection decision in short:

| Port | Pins | Use it when |
|---|---|---|
| **Native USB** (CDC) | **GPIO19 D− / GPIO20 D+**, via the `FT1` common-mode filter | Normal flashing and console. This is what `-DARDUINO_USB_CDC_ON_BOOT=1` makes `Serial` |
| **UART0** | **GPIO43 TX (499 Ω series `R30`) / GPIO44 RX** | Boot-time and crash debugging. **Not brought out to any connector** — using it means probing the board |
| External JTAG (MTDI/MTCK/MTMS/MTDO) | GPIO39–42 | **Unavailable.** Those pins carry LoRa SPI CLK/MISO/NSS and the buzzer |
| USB-Serial/JTAG (built into the ESP32-S3, on the native USB pins) | GPIO19/20 | Probably available, and the only debug path that does not require desoldering. **`inferred`, unverified** |

**Neither USB nor UART0 appears on the vendor's product-page pin tables.** Both are established
from the schematic alone (S14). That omission is recorded in
[R6](gaps-and-conflicts.md#r6--the-vendor-product-pages-pin-tables-are-accurate--confirmed-correct).

**On the JTAG row, be precise about what is and is not established.** The *external* JTAG pin
group is definitively consumed — GPIO39/40/41 are LoRa SPI and GPIO42 is the buzzer, read from
the schematic. The *internal* USB-Serial/JTAG controller is a documented ESP32-S3 peripheral on
the same GPIO19/20 pads, and the vendor's `-DARDUINO_USB_MODE=1` flag is what selects the
hardware CDC/JTAG path rather than TinyUSB in arduino-esp32 — but **that mapping was not
verified against arduino-esp32's own board definitions in this pass**, and no debug session has
been reported by anyone on this board. Treat "you can debug over USB" as a plausible
expectation to test first, not as a documented capability.

**Practical consequence of native USB.** The serial port disappears on every reset, crash,
sleep and USB reconfiguration, and comes back as a new device. Early boot output before CDC
enumerates is lost. UART0 does not have this problem, which is exactly why it is worth the
probe wires when something fails before `app_main`.

## 7. Factory restore and flash offsets

### 7.1 The offsets

From parsing the shipped image (`executed-success` as a static analysis — [`commands.md` §5](commands.md#5-firmware-image-inspection)) and from `partitions.csv` in both vendor projects
(S41, S42):

| Region | Offset | Size | Contents |
|---|---|---|---|
| Second-stage bootloader | `0x0000` | — | ESP32-S3 image, magic `0xE9`, 3 segments, entry `0x403c8924` |
| Partition table | `0x8000` | — | 3 entries |
| `nvs` (data/nvs) | `0x9000` | `0x6000` (24 K) | Wi-Fi credentials, NTP and timezone settings |
| `phy_init` (data/phy) | `0xF000` | `0x1000` (4 K) | RF calibration |
| `factory` (app/factory) | `0x10000` | `0xF00000` (15 360 K) | The application |
| *(unallocated)* | `0xF10000` | ~960 K | Free to the end of the 16 MB device |

`esp_app_desc_t` sits at `0x10020`, i.e. 0x20 into the app image, which is where the version,
project name, build date and IDF version were read from.

### 7.2 Restoring the official image

**The retained `.bin` is a merged whole-flash image, not an app-only image.** Three independent
indications: the parse finds a bootloader header at `0x0`, a partition table at `0x8000` and an
app header at `0x10000` inside the one file; the vendor's own object name ends `_0x00.bin`
(S34); and the file is 2 868 208 bytes — far larger than the app alone would be at that offset.

**Authoritative route** (`reported-working` — this is what the vendor supports):

> Use **M5Burner** or the **EasyLoader** executable, select the *PaperMono UserDemo* firmware,
> put the board in download mode (§6.3 / [`features/usb-and-serial.md` §3](features/usb-and-serial.md#3--download-mode-is-the-power-button--there-is-no-reset-button)),
> and flash. This is the only restore path M5Stack documents.

**Inferred equivalent** (`inferred`, **never executed, on any board**):

```bash
# INFERRED. Not run here. Verify the port and the chip before trusting this.
esptool.py --chip esp32s3 --port PORT --baud 921600 \
  write_flash --flash_mode dio --flash_freq 80m --flash_size 16MB \
  0x0 C153-PaperMono-UserDemo-v1.2.bin
```

The `--flash_mode dio --flash_freq 80m --flash_size 16MB` values are the ones the image's own
header reports, so they are the self-consistent choice; `0x0` follows from §7.2's three
indications. **Nothing about this command has been observed to work.** It is written down
because the method requires reacquisition and recovery instructions to exist rather than be
silently omitted — not because it has been validated.

### 7.3 What "factory reset" does and does not mean here

| Claim | Reality |
|---|---|
| The vendor link is labelled "PaperMono **Factory Reset** Firmware" | It resolves to a M5Burner record named **"PaperMono UserDemo"** — the same image, differently labelled ([C11](gaps-and-conflicts.md#c11--mislabelled-firmware-link)) |
| Flashing it "resets" the device | It replaces the application. Whether `nvs` (Wi-Fi credentials, timezone) survives depends on the tool and offsets used; a whole-flash write at `0x0` includes the image's own `nvs` region and would overwrite it. `inferred` |
| It restores the M5PM1 | **No.** The power manager runs its own firmware in its own part and is not touched by anything you flash into the ESP32-S3 (§8.3) |

## 8. Known bricking and bootstrapping risks

Five of these are recoverable, one is not, and one is a hardware kill. Ordered by how likely
you are to hit them.

### 8.1 Octal PSRAM is mandatory — and the failure looks like dead hardware

`M5GFX/src/M5GFX.cpp:2072–2081` aborts display initialisation and logs
`"M5PaperMono need OPI-PSRAM enabled"` when either `CONFIG_ESP32S3_SPIRAM_SUPPORT` or
`CONFIG_SPIRAM_MODE_OCT` is missing. The board is still identified, the firmware still runs,
**the screen simply stays blank**.

Compounding it: the vendor's own `build_flags` set `-DCORE_DEBUG_LEVEL=0`, which compiles that
message out. **The default configuration hides the message that explains the symptom.**

- PlatformIO: keep `board_build.arduino.memory_type = qio_opi`.
- ESP-IDF: `CONFIG_SPIRAM=y` and `CONFIG_SPIRAM_MODE_OCT=y` (both are in the vendor's
  `sdkconfig.defaults`).
- Recovery: rebuild. Nothing is damaged. `inferred` from source; `not-tested`.

### 8.2 GPIO3, GPIO45 and GPIO46 are strapping pins carrying user-facing signals

| GPIO | Strap function | Also carries | Who drives it |
|---|---|---|---|
| **GPIO0** | boot mode select | M5PM1 `BOOT_OUT_OD` | the power manager — by design |
| **GPIO3** | JTAG source select strap | **User button B** (`G3_KEY2`) | the user's finger |
| **GPIO45** | `VDD_SPI` voltage select strap | **PDM microphone clock** | the ESP32-S3 itself |
| **GPIO46** | boot-message routing strap | **PDM microphone data** | the microphone, whenever `PDM_VDD` is up |

**Holding user button B across a reset perturbs a strapping pin**, and a microphone that is
still powered and clocking across a reset perturbs two more. The vendor firmware does explicitly
release the mic pins before reconfiguring them ([`features/microphone.md` §2](features/microphone.md#2--both-microphone-pins-are-esp32-s3-strapping-pins)), but nothing in
any vendor code guards the button-B case.

This is a **bootstrapping** hazard rather than a bricking one on paper: straps are sampled at
reset and the board should come back on the next clean reset. It is listed here because the
symptom — "it sometimes does not come up, and it seems to depend on how I was holding it" — is
extremely easy to misdiagnose as flaky hardware. `inferred` from the pin map; `not-tested`.
Also in [`resources-and-conflicts.md` §9](resources-and-conflicts.md#9-boot-straps).

### 8.3 The M5PM1 owns reset and the boot strap — this is the real bricking vector

`CHIP_PU` carries `SOC_RESET` from the M5PM1, and GPIO0 is driven by its open-drain
`BOOT_OUT_OD`. **The power manager, not a button, puts the ESP32-S3 into download mode.** There
is no separate reset button on the board — the schematic shows exactly three switches on the
KEY/RGB sub-board (`S1` `PWR_BTN`, `S2` `G2_KEY1`, `S3` `G3_KEY2`) and nothing else.

Three consequences, in increasing order of seriousness:

1. **If the M5PM1 will not assert the boot strap, you cannot flash the board at all.** Your
   escape hatch is a peripheral, and it is behind an I²C bus that your own firmware also drives.
2. **The M5PM1 has its own firmware-update mode**, entered by `SYS_CMD` `0x0C` `CMD=11` or by a
   long press — and it is **lockable** through `BTN_CFG_1[7] DL_LOCK`. Writing that lock bit
   from application code is a plausible way to remove your own recovery path. Nothing in this
   pass tested it and nobody has reported doing it; it is called out because the register exists
   and is writable over the same bus everything else uses.
3. **Third-party projects disable the M5PM1's default single-click reset**, which two
   independent sources describe as disruptive
   (`MagicCube/free-ink-on-paper-mono` calls it "M5PM1's dangerous default single-click reset";
   `Free-Ink/freeink-sdk`'s `PaperMonoBoard.h` does the same). Note what the freeink SDK is
   careful to do: it disables single-click reset **while preserving the hardware long-hold
   download escape**. If you copy the first half of that and not the second, you have removed
   the only documented way back into download mode. **Copy both halves.**

### 8.4 There is no OTA partition

Both vendor projects ship a single `factory` app and no OTA slot, no `otadata`, and no
filesystem. **The product as shipped has no field-update path.** If you intend to ship
something, decide your partition layout at the start, because changing it later means a
full reflash of every unit in the field — which for this board means a cable and a hand.

The community CrossPoint image does something different again (`app0` + a dedicated 4 MB
`cjkfont` partition + SPIFFS + coredump), which is direct evidence that repartitioning works —
see [`factory-firmware.md` §4](factory-firmware.md#4-partition-maps--three-different-layouts-are-in-evidence).

### 8.5 The `PYG3` collision can silently cut panel power

`PYG3` denotes **M5IOE1 pin 3** (`PYB_EPD_EN`, the e-paper 3.3 V rail enable) *and* **M5PM1 G3**
(`PYG3_BL_PWM`, the frontlight PWM). The vendor documentation uses the same token for both, on
the same page. Writing a "frontlight" value to the wrong chip switches off the display's power
rail. Compounding it, the M5IOE1 library's pin labels are 1-based while its enum values are
0-based (`M5IOE1_PIN_3 = 2`), so passing a documentation `PYG<n>` straight into the API reaches
pin *n+1*.

**Read [`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md) before
writing any expander or PMIC code.** This is recoverable in software, but the symptom is a
blank screen, which is also the symptom of §8.1 and of forgetting to enable the rail at all.

### 8.6 Continuous partial refresh can destroy the panel — permanently

This is the one item on this page that is not recoverable by reflashing. M5Stack's own
precautions (S01) state that **uninterrupted continuous partial fast refreshes cause long-term
DC imbalance and irreversible panel damage**, and that custom external waveforms must maintain
DC balance for the same reason. Their software recommendation is roughly **one full refresh per
ten partial refreshes**.

Two things make this more than boilerplate:

- **M5Stack says its own M5GFX waveforms are "currently unstable"** and recommends the panel
  maker's OTP example instead. That is corroborated in-tree: M5GFX `develop` has *replaced* the
  LUTs, leaving 17 lines of the previous `lut_quality` commented out.
- **M5GFX drives the panel at 40 MHz** while both the SSD1677 datasheet (§12.1) and the DKE
  panel manual (p. 16) independently state a **20 MHz** maximum write clock, and the vendor's
  own OTP demo uses 20 MHz ([C3](gaps-and-conflicts.md#c3--spi-clock-exceeds-the-panels-rated-maximum)).

If you are writing a refresh loop, start from
[`features/epaper-display.md`](features/epaper-display.md) and the OTP demo, not from M5GFX
defaults.

### 8.7 A low battery can wedge the I²C bus

The IP2315 charger's I²C mode depends on its bus pins being pulled to `VBAT`. The vendor
documents that at low battery it may fail to enter I²C mode and disturb the other six devices
on the shared bus. It is therefore **gated off the bus by default** through M5IOE1 `IO11`
(`PYB_CHG_IIC`); attach it, transact, detach. The vendor's documented recovery from a wedged
bus is a short press of the power button.

**An I²C scan that does not find `0x75` is behaving correctly.** Details in
[`power-architecture.md`](power-architecture.md#the-charger-is-normally-off-the-i²c-bus).

## 8b. Two bring-up traps reported by a Rust porter — added 2026-09-11

From `ciniml/paper_name_plate`'s `DESIGN.ja.md`. **Both sit in that document's
§2.4 「未確定事項 / リスク」 — "Undetermined items / risks" — and carry neither the
author's `実機確認済み` ("verified on real hardware") stamp nor a date**, unlike a
dozen other findings in the same file that do. The author is demonstrably
disciplined about applying that stamp, so its absence is meaningful.

**Grade these as an experienced porter's practical caution, not as verified
behaviour.** They are recorded because the failure modes are expensive and
non-obvious, not because they are proven.

### Trap 1 — `espflash monitor` / `espflash reset` can strand the board in download mode

> 「`espflash monitor` / `espflash reset` の USB-JTAG リセットは PM1 管理のダウンロード
> モード（`boot:0x21`）に落ち、本体ボタンを押すまで復帰しない。」

*"The USB-JTAG reset of `espflash monitor` / `espflash reset` drops into the
PM1-managed download mode (`boot:0x21`) and does not recover until you press the
device's physical button."*

**Practical consequence:** after flashing, reboot with the **physical button**,
and read logs with a serial reader that **does not touch DTR/RTS**. This is
specific to the PaperMono because download mode is arbitrated by the M5PM1, not
by the usual auto-reset transistor pair — see
[`commands.md`](commands.md) §"Enter download mode" and the vendor-page conflict
recorded as C-5 in [`compatibility-and-status.md`](compatibility-and-status.md).

### Trap 2 — the I²C speed setting survives an ESP32 reset

> 「PM1/IOE1 の SPD ビット(400 kHz)は常時給電のため ESP32 リセット後も残り、100 kHz
> アクセスが部分的に失敗する。`main.rs` の `recover_i2c_speed` が 400 kHz で SPD を戻す。
> `I2C_CFG` 書き込み直後は 5 ms 待つ（次トランザクションが NACK になる）。」

*"Because PM1/IOE1 are permanently powered, the SPD bit (400 kHz) persists even
after an ESP32 reset, and 100 kHz access partially fails. `recover_i2c_speed` in
`main.rs` restores SPD at 400 kHz. Wait 5 ms immediately after writing `I2C_CFG`
(the next transaction will NACK)."*

This is the more insidious of the two. The bus starts at 100 kHz and is raised to
400 kHz after bring-up (needed to meet the NFC tag-emulation response deadline).
Because **the expander and PMIC are on always-on rails**, they keep the fast-mode
bit across a host reset — so a fresh boot's 100 kHz probing **partially** fails.
Partially, which is the worst kind.

**⚠ The source never says where the SPD bit is.** Its register maps list
M5IOE1 `I2C_CFG (0x23)` and M5PM1 `I2C_CFG (0x09)` documenting only *"low 4 bits
= sleep"* / *"sleep timeout"*. No address or bit index for SPD appears anywhere
in the document, and `pm1.rs` / `ioe1.rs` were not captured. **A porter cannot
act on this without reading that source.** Recorded as a lead, not a recipe.

Cross-check against this knowledge base's own
[M5IOE1 register map](../../../components/m5stack/m5ioe1/README.md) before
relying on either address.

## 9. What is not established

- **Nothing here was run.** No build, no flash, no monitor, no recovery, on any board.
- **No console baud rate is documented** by the vendor for any framework.
- **JTAG/debugging has not been demonstrated by anyone**, in any source located. The external
  pin group is definitively consumed; the USB-Serial/JTAG path is inferred and untested.
- **The `-DARDUINO_USB_MODE=1` semantic was not verified** against arduino-esp32's own board
  definitions in this pass.
- **UiFlow2 has no documented version floor, block list or limitation** — the vendor page is
  empty of all three ([G4](gaps-and-conflicts.md#g4--uiflow2-support-is-advertised-but-undocumented)).
- **RadioLib's LGPL-3.0 obligations were not analysed**, only noticed.
- **No one has reported a flashing session on real PaperMono hardware** in any source found in
  two broad passes — see [`community.md`](community.md).

## Related

- [`commands.md`](commands.md) — the command ledger, with tool versions and true execution status
- [`factory-firmware.md`](factory-firmware.md) — what is in the shipped images, and restore evidence
- [`features/usb-and-serial.md`](features/usb-and-serial.md) — ports, console, flashing routes, debugging
- [`compatibility-and-status.md`](compatibility-and-status.md) — version-keyed working/failing reports
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — every conflict cited above
- [`sources.md`](sources.md) — S01, S04, S07, S09, S14, S38, S40–S47, S96
