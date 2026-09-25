# FreeInk SDK — architecture

**Repo:** `Free-Ink/freeink-sdk` · **HEAD** `24003795381a6c23630a26472ae3b06550333e71`
· **branch** `main` · **license** MIT (`LICENSE`, "Copyright (c) 2026 FreeInk"; `NOTICE`
carries upstream MIT attribution) · **research date** 2026-09-02.

Evidence labels: `executed-success`, `inferred`, `not-tested`. **Nothing is
hardware-verified.**

---

## 1. What it is

A **library**, not a framework or application scaffold — with one caveat.

Evidence for "library": it has no `main()`, no application entry point, no
`src/`; it is a set of 27 independently-linkable PlatformIO libraries under `libs/`, each
with its own `library.json`, consumed via `symlink://` `lib_deps`
(`README.md:781-789`). Consumers keep their own `platformio.ini`, their own runtime, and
their own `setup()`/`loop()`. `README.md:53-54` asserts it has "no build-time or runtime
dependency on the upstream repository". CrossPoint consumes 14 of the libraries; the
PaperMono demo consumes 10; `freeink-reader` consumes a handful.

The caveat: **`libs/ui/FreeInkUI` is a framework** — it provides `FreeInkApp`, `Screen`,
retained-ish composition and a widget set benchmarked against LVGL
(`README.md:451-505`). It is optional and CrossPoint does not use it for rendering (see
[CrossPoint architecture](../../applications/crosspoint-reader/architecture.md) §7). So the SDK is a library collection that *contains* an
optional UI framework.

**Origin:** a June-2026 re-architecture derived from `open-x4-epaper/community-sdk` — see
[dependency and lineage](../../ecosystems/crosspoint-freeink/dependency-and-lineage.md) for the full lineage and the
`NOTICE`/`README` attribution text.

---

## 2. HAL / device-abstraction design

Two orthogonal compile-time axes, plus one runtime axis. This is the central design idea.

### Axis 1 — devices (`-DFREEINK_DEVICE_<NAME>`)

15 devices declared at `BoardConfig.h:33-77`: `X4, X3, X4PRO, X4CLASSIC, M5, MURPHY,
DELINK, LILYGO, M5PAPER, STICKY, PAPERMONO, PAPERS3, MURPHY_M4, EEGO_A4, ONEPAGE`.

Selecting none is a **compile error** (`BoardConfig.h:80-85`):

```cpp
#if !(FREEINK_DEVICE_X4 || FREEINK_DEVICE_X3 || … || FREEINK_DEVICE_ONEPAGE)
#error "FreeInk: no device selected. Pass at least one -DFREEINK_DEVICE_<NAME> …"
```

MCU family is *derived* from the device set and mixing families is also a compile error
(`BoardConfig.h:91-99`):

```cpp
#define FREEINK_MCU_C3  (FREEINK_DEVICE_X3 || FREEINK_DEVICE_X4)
#define FREEINK_MCU_C61 (FREEINK_DEVICE_ONEPAGE)
#define FREEINK_MCU_S3  (FREEINK_DEVICE_M5 || … || FREEINK_DEVICE_EEGO_A4)
#define FREEINK_MCU_ESP32 (FREEINK_DEVICE_M5PAPER)
#if (FREEINK_MCU_C3 + FREEINK_MCU_C61 + FREEINK_MCU_S3 + FREEINK_MCU_ESP32) != 1
```

### Axis 2 — capabilities (`FREEINK_CAP_*`), derived not declared

Each capability is a **boolean expression over the selected devices**
(`BoardConfig.h:193-299`), so a consumer normally never sets them:

```cpp
#define FREEINK_CAP_TOUCH  (FREEINK_DEVICE_MURPHY || FREEINK_DEVICE_LILYGO || … )
#define FREEINK_CAP_MIC    (FREEINK_DEVICE_STICKY || FREEINK_DEVICE_PAPERMONO)
#define FREEINK_CAP_RTC    (FREEINK_DEVICE_X3 || … || FREEINK_DEVICE_PAPERMONO || …)
#define FREEINK_CAP_LED    (FREEINK_DEVICE_M5 || FREEINK_DEVICE_PAPERMONO)
#define FREEINK_FB_PSRAM   (FREEINK_DEVICE_M5PAPER || FREEINK_DEVICE_PAPERMONO)
```

Full capability list at `README.md:339-353`: `TOUCH, FRONTLIGHT, WARMLIGHT, COLOR, AUDIO,
MIC, RTC, TEMP_HUMIDITY, IMU, BUZZER, LED, USB_MSC, BLE_HID_HOST, NET_TLS13`. Each can be
forced with `=0`/`=1`. This is what keeps binaries tight: unused peripheral code never
compiles.

### Axis 3 — runtime profile selection

`BoardConfig::ACTIVE` points at a `BoardProfile`; a consumer may call
`BoardConfig::selectDevice(...)` after its own detection. The SDK deliberately **does not
ship the detector** — `README.md:329-332`: *"the SDK doesn't ship a detector; X3/X4
detection stays in the consumer"*. (In practice `libs/hardware/XteinkDetect` does supply
`freeink::selectXteinkDevice()` for the Xteink case, `README.md:133-142` — a documented
convenience that slightly contradicts the "no detector" line. **Conflict recorded.**)

Boards enum at `BoardConfig.h:366-377+`.

### The `BoardProfile` struct — the single porting surface

`BoardConfig.h:686-731+`. Everything device-specific is *data* in this struct:

```cpp
struct BoardProfile {
  Board board;  const char* name;
  InputStyle inputStyle;
  DisplayController displayController;
  uint16_t displayWidth, displayHeight;     // resolution is ALWAYS profile data
  DisplayPins display;  uint32_t displaySpiHz;
  SdPins sd;  InputPins input;
  int8_t batteryAdc, batteryChargeStatus;  float batteryDividerMultiplier;
  int8_t usbDetect;
  TouchConfig touch;  FrontlightConfig frontlight;
  AudioConfig audio;  LedConfig leds;
  DisplayOrientation orientation;           // MIRROR_X/MIRROR_Y/ROTATE_180 in hardware
  SdmmcPins sdmmc;  BatteryGaugeConfig batteryGauge;
  MicConfig mic = …;  SensorsConfig sensors = …;
  float uiScale = 1.0f;                     // touch boards bump this for finger targets
  PowerConfig power = {};
  uint8_t displayControllerVariant = 0;     // filled by boot probe
  ViewableInsets viewableInsets = {};        // bezel-covered edges
};
```

Note the **defaulted** members (`mic`, `sensors`, `uiScale`, `power`,
`viewableInsets`, …) — each carries a comment saying "Defaulted so existing profiles need
no change". That is an explicit backwards-compatibility discipline for profile evolution.

### The stated invariant

`README.md:104-118` — *"Nothing device-specific is hardcoded in generic code"*:

> files — facade, drivers, input, SD — key only off those derived flags and injected
> config/hooks, **never a device name**. Board quirks that aren't plain config (e.g. an
> SD rail behind an I²C PMIC) come in through hooks like `SDCardManager::setPowerHook()`,
> so the SD manager itself stays device-agnostic.

---

## 3. How this differs from CrossPoint's approach

| | FreeInk SDK | CrossPoint `lib/hal/` |
|---|---|---|
| Purpose | portable multi-device hardware layer | thin adapters over the SDK for app convenience |
| Device knowledge | `BoardProfile` data + capability macros | none — it consumes `BoardConfig::ACTIVE` |
| Size | 130,278 code lines / 385 files | 16 files |
| Selection | compile-time flags + runtime profile swap | inherits whatever the SDK resolved |
| Panel drivers | 13 `PanelDriver` implementations | none |

CrossPoint's HAL is **not** a competing abstraction; it is a shim. The migration PR
`crosspoint-reader@ebebc6f2` states the long-term intent is to delete even that:

> Eventually we will want to remove a lot of the manual isx3 type stuff from our firmware
> and go through the boardsupport api the sdk provides.

The real contrast is with the **pre-FreeInk `community-sdk`**, which FreeInk explicitly
restructured — `README.md:50-53`:

> where the upstream interleaves every device in one monolithic driver, FreeInk splits each
> controller into a standalone, compile-time-selectable driver behind a stable facade, with
> per-device behavior supplied as injectable config.

`community-sdk` is 2,102 code lines total (`tokei`); FreeInk is 130,278. A ~60× expansion.

---

## 4. Display stack

`README.md:66-73`:

```
firmware  ─calls─▶  EInkDisplay  (alias of freeink::FreeInkDisplay, the facade)
                          │ owns framebuffer + geometry, selects a driver at begin()
                          ▼
                    PanelDriver  (interface)
```

13 drivers in `libs/display/FreeInkDisplay/src/driver/` (`executed-success`, `ls`):
`Ssd1677Driver`, `Uc8253X3Driver`, `Uc8253MurphyDriver`, `Uc8179Driver`, `Uc8279Driver`,
`Uc8279X4Driver`, `Uc8279cA4Driver`, `Ed2208M5Driver`, `It8951Driver`, `LgfxEpdDriver`,
`M5OfficialDriver`, `PaperMonoDriver`, plus the `PanelDriver.h` interface.

Key separations:
- **Resolution is `BoardProfile` data**, never a driver constant (`README.md:801-806`).
- **Waveforms/LUTs are an injected config struct**, e.g.
  `-DFREEINK_UC8253_X3_CONFIG=yourConfig` / `-DFREEINK_SSD1677_CONFIG=...`
  (`README.md:795-800`). A new panel of an existing controller needs **no driver edit**.
- **External libraries are wrapped, per device.** `LgfxEpdDriver` wraps LovyanGFX's
  `Panel_EPD` for raw-parallel EPDs with no on-glass controller (LilyGo T5 S3, PaperS3);
  `M5OfficialDriver` wraps M5GFX (`README.md:815-843`). `usesExternalBus()` marks these.
  The external `#include` sits inside the `#if FREEINK_DRIVER_<NAME>` guard so PlatformIO's
  LDF only links it for builds that need it.
- **Per-batch controller auto-detection**: several Xteink panels ship different silicon per
  production batch on the same board. `applyXteinkDisplayController()` resolves it from an
  OEM NVS value (`hw_calib`/`screenType`) first, falling back to a bit-banged half-duplex
  read of the UC81xx `VER (0x70)`/`FLG (0x71)` registers (`README.md:207-253`).
- Orientation is profile data (`MIRROR_X/MIRROR_Y/ROTATE_180`), applied in hardware.
  **90°/270° is not supported** — "need a software transpose, which the driver does not do"
  (`README.md:371-372`).

---

## 5. Library inventory (`libs/`, 27 directories)

```
assets/Icons/              freeink::Icon 1-bpp format + vendored Lucide SVGs + generator
assets/ImageToneMapper/
book/FreeInkBook/          EPUB/book handling  (third_party: expat, libunibreak, miniz,
                                                pngle, stb, tjpgd, unicode, hyphen-patterns)
book/ContentProtection/    DRM: content.key, rights files, streamed decrypt
display/FreeInkDisplay/    facade + EInkDisplay shim + 13 drivers + LUTs
hardware/BoardConfig/      board profiles & capability descriptors (2,010-line header)
hardware/BoardPaperS3/  hardware/BoardT5S3/
hardware/InputManager/     buttons + capacitive touch (CHSC6x, GT911, FT5x06)
hardware/BatteryMonitor/   ADC battery + optional I²C gauge (BQ27220/BQ25896/CW2017)
hardware/SDCardManager/    SdFat-over-SPI or native SDMMC
hardware/PowerManager/     per-SoC deep-sleep wake-on-power-button
hardware/MemoryManager/    on-demand cache-sink reclaim + heap reporting
hardware/FrontlightManager/ PWM frontlight (LEDC or PMIC-PWM)
hardware/LedManager/  hardware/AudioManager/  hardware/Microphone/  hardware/Buzzer/
hardware/Rtc/  hardware/Imu/  hardware/EnvironmentSensor/
hardware/UsbMassStorage/  hardware/RecoveryBoot/  hardware/XteinkDetect/
network/SecureNet/         wolfSSL TLS 1.3 client + HTTP shim (opt-in)
network/BleKeyboardHost/   BLE HID central (page-turner remotes)
network/NearbyTransfer/
ui/FreeInkUI/              immediate-mode e-paper widget toolkit
```

(layout per `README.md:846-860`, verified against the tree)

---

## 6. API surface a firmware author uses

Minimum viable consumer (`README.md:781-789`):

```ini
lib_deps =
  BoardConfig=symlink://path/to/freeink-sdk/libs/hardware/BoardConfig
  EInkDisplay=symlink://path/to/freeink-sdk/libs/display/FreeInkDisplay
  InputManager=symlink://path/to/freeink-sdk/libs/hardware/InputManager
  BatteryMonitor=symlink://path/to/freeink-sdk/libs/hardware/BatteryMonitor
  SDCardManager=symlink://path/to/freeink-sdk/libs/hardware/SDCardManager
```

`#include <EInkDisplay.h>` and the `EInkDisplay` type "keep working via the compat shim"
(`README.md:791-793`) — an explicit source-compatibility layer for the old
`community-sdk` API, which is why CrossPoint's migration needed zero code changes.

Representative documented calls (all `not-tested` — I did not compile a consumer against
them beyond CrossPoint's own build):
- `freeink::selectXteinkDevice()`, `BoardConfig::selectDevice(...)`,
  `BoardConfig::ACTIVE`, `BoardConfig::holdPowerRails()`, `releaseSdRail()`
- `applyXteinkDisplayController()`, `display.begin()`, `display.setDisplayX3()`,
  `getDisplayWidth()/Height()`, `displayCommitted()`, `runMaintenance()`, `controllerIdle()`
- `InputManager`: `hasTouch/isTouchPressed/wasTouchPressed/wasTouchReleased/getTouchPoint`
  (`README.md:290-296`); GT911 additionally exposes allocation-free multi-contact
  snapshots, 2–4-finger translation gestures and two-finger rotation with signed angle
- `SDCardManager::begin()`, `SDCardManager::setPowerHook()`
- `FrontlightManager`, `LedManager`, `Rtc`, `Imu`, `PowerManager` per capability

---

## 7. Language, build, runtime

| Property | Value | Source |
|---|---|---|
| Language | **C++**, `-std=gnu++2a` (C++20) | `platformio.sample.ini:21` |
| Exceptions | disabled (`-fno-exceptions`) | mirrors CrossPoint `platformio.ini:62` |
| FreeInkUI subset | "freestanding C++17" | `README.md:481` |
| Build system | PlatformIO, `framework = arduino` | `platformio.sample.ini:15-16` |
| Platform | pioarduino `platform-espressif32` **55.03.37** (Arduino-ESP32 3.3.x / ESP-IDF 5.5.x) | `platformio.sample.ini:14-15` |
| RTOS | FreeRTOS via Arduino-ESP32; the SDK creates no tasks of its own | `inferred` |
| MCUs | ESP32-C3, ESP32-C61, ESP32-S3, classic ESP32 | `BoardConfig.h:91-97` |
| CMake / ESP-IDF component | **none** — no `CMakeLists.txt`, no `idf_component.yml` | `executed-success`, `find` |

**Size** (`tokei`, excluding `.git`, `executed-success`):

| Language | Files | Code |
|---|---|---|
| C | 27 | 36,603 |
| C++ | 70 | 27,628 |
| C Header | 174 | 26,711 |
| SVG | 42 | 35,614 (vendored Lucide icons) |
| Python | 10 | 1,525 |
| **Total** | **385** | **130,278** |

Repo size 3,447 KB (GitHub API). `BoardConfig.h` alone is **2,010 lines**.

**Binary size:** the SDK ships no binary and has no releases. Its contribution is only
measurable inside a consumer. The one number I measured (`executed-success`) is the
CrossPoint `papermono` image: 5,364,128 B total, `.text` 1,906,640 B, and IRAM fully
exhausted — see [CrossPoint architecture](../../applications/crosspoint-reader/architecture.md) §9. I did **not** isolate the SDK's share.

**Dependencies:** vendored, not fetched. `libs/book/FreeInkBook/third_party/` contains
`expat, hyphen-patterns, libunibreak, miniz, pngle, stb, tjpgd, unicode`;
`libs/book/ContentProtection/{third_party,src/vendor}` likewise. The only git submodule is
`libs/assets/Icons/lucide` → `lucide-icons/lucide` (`.gitmodules`). External libraries that
are *fetched* (LovyanGFX/M5GFX, SdFat) are declared per-consumer-env, not by the SDK
(`README.md:826-830`).

---

## 8. Maintainership and funding

**Effectively a single-maintainer project**, in sharp contrast to CrossPoint.

Last 200 commits on `main` (`executed-success`):

| Author | Commits |
|---|---|
| **Justin Mitchell** | **148 (74 %)** |
| winst0niuss | 9 |
| Julia Nguyen | 9 |
| Antoine Aflalo | 8 |
| MarsTechHAN | 6 |
| jpirnay | 3 |
| Erica Jensen | 3 |
| others (11) | ≤2 each |
| **distinct authors** | **18** |

Span 2026-07-27 → 2026-09-01 (200 commits in ~5 weeks — high velocity).

**On the "open-source collective" framing:** the `Free-Ink` org and `freeink.org` present
FreeInk as a collective. The `LICENSE` says "Copyright (c) 2026 FreeInk" and `NOTICE` says
"Copyright (c) 2026 FreeInk" — an entity name, not a person. But the commit record shows
one person doing three-quarters of the work, who is also the org's sole other repo owner
(`freeink-reader/LICENSE`: "Copyright (c) 2026 Justin Mitchell"). **Treat "collective" as
branding; the bus factor is 1.** `inferred` from commit distribution.

**Funding:** the only file in `.github/` is `FUNDING.yml` — there is **no CI at all**
(no `.github/workflows/`). `README.md:914` has a "Commercial use & sponsorship" section.
Compare CrossPoint's five workflows including a 4-env build matrix.

**Releases:** none. The GitHub releases API returns an empty list. Consumers pin by
submodule SHA only.

**Throughput** (GitHub search API, 2026-09-02): 31 PRs merged since 2026-08-01, 11 PRs
open, 6 issues open, 1 issue closed since 2026-08-01. Low issue volume — consistent with a
library consumed by a handful of projects rather than by end users.

---

## 9. Devices supported today

15 device flags; `README.md:121-133` documents 13 in its table (MURPHY_M4 and EEGO_A4 have
flags and docs — `docs/eego-a4-support.md` — but no table row; **conflict recorded**,
the table lags the macro list).

| Device | MCU | Controller | Panel |
|---|---|---|---|
| Xteink X4 | ESP32-C3 | SSD1677 | 800×480 |
| Xteink X3 | ESP32-C3 | UC8253 / UC8279d | 792×528 |
| OnePage | ESP32-C61 | SSD1677 | 800×480 |
| de-link | ESP32-S3 | SSD1677 | 800×480 |
| M5Stack PaperColor | ESP32-S3 | ED2208 | 400×600 Spectra-6 colour |
| Murphy M3 | ESP32-S3 | UC8253 | 240×416 |
| LilyGo T5 S3 | ESP32-S3 | ED047TC1 raw parallel | 960×540 16-gray |
| M5Paper v1.1 | ESP32 classic | IT8951E | 540×960 16-gray |
| Sticky | ESP32-S3 | SSD1677 | 3.97" 800×480 |
| Xteink X4 Pro | ESP32-S3 | SSD1677/UC8179/UC8279 auto | 800×480 |
| Xteink X4 Classic | ESP32-S3 | SSD1677/UC8179/UC8279 auto | 800×480 |
| **M5Stack Paper Mono** | ESP32-S3 | SSD1677 | 800×480 |
| M5Stack PaperS3 | ESP32-S3 | ED047TC1 raw parallel | 960×540 16-gray |
| (+ Murphy M4, eEGO A4) | ESP32-S3 | — | flags + docs only |

### M5Stack Paper Mono — the best-documented port

`README.md:254-296` and `libs/hardware/BoardConfig/include/PaperMonoBoard.h` (99 lines),
`M5Pm1.h` (213), `M5Ioe1.h` (160), `libs/display/FreeInkDisplay/src/driver/PaperMonoDriver.{h,cpp}`.

Power and reset run through two PY32 helper chips on the system I²C bus rather than ESP
GPIOs — the **M5PM1 PMIC** (battery telemetry, charging, power button, frontlight PWM, red
LED) and the **M5IOE1 expander** (EPD power+reset, touch power+reset, TF-card rail, PDM-mic
rail, green/blue LEDs). `PaperMonoBoard.h` is "the single owner of the bring-up"
(`README.md:262`), so consumers normally never touch the PMIC or expander. The one
exception is the PDM microphone rail, which a consumer must raise itself
(`m5ioe1::PIN_MIC_POWER`, `README.md:266-268`).

Profile constants live at `BoardConfig.h:979-1004` (`PAPER_MONO_AUDIO`,
`PAPER_MONO_FRONTLIGHT`, `PAPER_MONO_LEDS`, `PAPER_MONO_MIC`). Derived flags:
`FREEINK_DRIVER_PAPER_MONO` (`:179-180`), touch (`:195`), frontlight (`:203`), mic (`:275`),
RTC (`:282`), buzzer (`:296`), LED (`:299`), **`FREEINK_FB_PSRAM` on** (`:316`), SDMMC
(`:326`).

Notable behaviours (`README.md:270-288`, `not-tested`): non-flashing internal waveform for
binary UI paints; host-authored LUTs with a 3-level grayscale target batched in host RAM;
`DigitalTwoButton` input style where holds synthesize back/confirm and the power button
arrives as `BTN_POWER` from the PMIC (its dangerous single-click hardware reset is disabled
at boot); frontlight PWM inside the PMIC driving an AW9967 boost driver fed from the EPD
rail, so the light only runs while EPD power is on.

---

## 10. Related repos

### `MagicCube/free-ink-on-paper-mono` — FreeInk on PaperMono

HEAD `34cc8794`, `main`, 10 commits, **single author (Henry Li)**, created 2026-08-25.
**No LICENSE file** (GitHub API `license: null`) — default all-rights-reserved. Flag this
before reusing any of it.

What it is: **not** a reader. It is a UI/tooling demo. `README.md:1-20`: *"Its purpose is
to prove that Loop Engineering for embedded UI is ready to use"* — an agent-driven workflow
where a native preview CLI and the firmware "execute the same FreeInkUI screen code against
the same 1-bit framebuffer model, orientation, fonts, and layout rules", making the result
WYSIWYG.

What it demonstrates (`README.md:22-34`, `not-tested`):
- status bar with RX8130 time and M5PM1 battery / USB-power / charging telemetry
- touch and physical-button interaction, light/dark theming
- frontlight held off at boot, controlled only from an on-screen switch at 127/255
- asynchronous e-ink refresh with periodic full cleanup
- "a bounded PaperMono rectangular-refresh laboratory with a PR-ready SDK patch"
- verified disabling of M5PM1's default single-click reset

**Completeness:** 12,173 lines across 38 files, of which 10,405 are generated font headers
(`src/fonts/inter-*.hpp`, `ndot57-*.hpp`) — so roughly **1,700 lines of real application
code**. Screens are `today-screen`, `piano-screen`, `demo-app`, plus `refresh-scheduler`
and `book-text-layout`. It consumes 10 SDK libraries (`platformio.ini:47-57`), including
`FreeInkBook` and `FreeInkUI` — notably it *does* use FreeInkUI, unlike CrossPoint.

**It patches the SDK.** `platformio.ini:49` points `EInkDisplay` at
`symlink://.cache/freeink-sdk-patched/libs/display/FreeInkDisplay`, built by applying
`patches/freeink-paper-mono-window-refresh.patch` (10,747 B). The patch adds RAM
window-addressing commands to `PaperMonoDriver.cpp` — `CMD_SET_RAM_X_RANGE (0x44)`,
`CMD_SET_RAM_Y_RANGE (0x45)`, `CMD_SET_RAM_X_COUNTER (0x4E)`, `CMD_SET_RAM_Y_COUNTER (0x4F)`
— plus a `_windowBaselineValid` state flag. It also pins its own SDK submodule commit
(`df4a1b7b`), different from CrossPoint's.

> **Correction, verified 2026-09-20 (`executed-success`).** The original 2026-09-02 text
> here read "rectangular partial refresh that **upstream FreeInk does not yet have**". That
> was **wrong on the research date and is wrong now.** The change had already merged
> upstream six days earlier:
>
> | Fact | Value |
> |---|---|
> | Upstream commit | `4327a6d887b1c60b758d13e89ede263fe0da5147` "Add PaperMono window refresh support" |
> | Author | **Henry Li** — the same person who wrote `free-ink-on-paper-mono` |
> | Authored / merged | 2026-08-26 |
> | Merge commit | `9a6f7d1a1fcdf93bcf4f299353dc99a65e8a6e1d`, PR **#58** from `MagicCube/codex/papermono-window-refresh`, merged by Justin Mitchell |
> | Upstream diff | same two files, **+142 / −4** |
>
> The local patch is **redundant against SDK `main`** — `git apply --check` against HEAD
> `24003795` fails with *"patch does not apply"* because the code is already there, and
> succeeds against `df4a1b7b`. The patch exists only because the repo pins an SDK commit
> **two days older than its own author's upstream merge**.
>
> See [PaperMono windowed refresh](papermono-window-refresh.md) for which consumer pins
> carry the capability — the answer differs per fork.

**Read this as:** an independent developer's proof that FreeInk+PaperMono works end to end,
whose principal SDK improvement **was upstreamed by its own author**. Useful as a worked
reference; the "unmerged patch" framing does not survive checking. Not a maintained product.

### `Free-Ink/freeink-reader`

HEAD `ca1c53d0`, `main`, 4★, 52 KB, MIT (Justin Mitchell). 2,949 code lines, essentially
**one 2,766-line C++ file**. A minimal reference consumer by the SDK's own author, last
pushed 2026-07-08. Demo, not product.

### `mohitagw15856/Inkkit`

HEAD `5e2f7418`, `main`, 1★, MIT ("Copyright (c) 2026 InkCards contributors"). 9,233 code
lines, 9 commits, 3 authors — Mohit (5), mohitagw15856 (2), **Claude (2)**.

Self-described as "**The** shared device-layer HAL for freeink-sdk" (`README.md:8`) —
a **self-declared** status with **zero adoption**. Grep for `inkkit` across
`crosspoint-reader/{src,lib,platformio.ini}` and `freeink-sdk/{libs,README.md}` returns
nothing (`executed-success`). Neither FreeInk nor CrossPoint references it.

What it actually is (`README.md:36-40`): a C++17 PlatformIO library wrapping the freeink-sdk
`Storage`, `gpio`, `display` and `powerManager` singletons plus `HalFile` streaming,
"extracted from two shipping firmwares — InkCards … and HabitInk", both by the same author.
Scope is **ESP32-C3 / Xteink X4+X3 only** — a subset of FreeInk's 15 devices, so it cannot
be a general device layer. The README carries an SEO comment on line 1.

**Assessment:** a personal convenience wrapper, marketed as ecosystem infrastructure. It
sits *above* freeink-sdk, not beside or below it, and adds no device support. Record it as
peripheral.
