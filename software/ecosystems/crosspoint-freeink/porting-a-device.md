# Porting notes — adding a device to CrossPoint vs. FreeInk SDK

**Research date:** 2026-09-02. Evidence labels: `executed-success`, `inferred`,
`not-tested`. Nothing hardware-verified.

---

## 0. Read this first if you care about M5Stack PaperMono

**M5Stack Paper Mono is already fully supported at both layers. There is nothing to port.**

- **FreeInk SDK**: `FREEINK_DEVICE_PAPERMONO` is a first-class device
  (`BoardConfig.h:63-64`), with a dedicated panel driver
  (`libs/display/FreeInkDisplay/src/driver/PaperMonoDriver.{h,cpp}`), a board bring-up owner
  (`libs/hardware/BoardConfig/include/PaperMonoBoard.h`, 99 lines) and PMIC/expander drivers
  (`M5Pm1.h` 213 lines, `M5Ioe1.h` 160 lines).
- **CrossPoint**: three build envs — `papermono`, `papermono-gh_release`,
  `papermono-gh_release_rc` (`platformio.ini:343-402`).
- **CI**: `papermono` is in the build matrix (`.github/workflows/ci.yml:84-90`).
- **Released**: `papermono-1.6.0_beta_RC03.bin` (5,293,984 B) shipped in release `1.6.0rc`,
  2026-08-17.
- **I built it myself** (`executed-success`):

  ```
  $ pio run -e papermono
  papermono      SUCCESS   00:04:47.763
  Flash: 81.8% (5,363,622 / 6,553,600)   RAM: 32.4% (106,028 / 327,680)
  ```

Support landed in `crosspoint-reader@bbca4886` — "feat: Add support for x4pro & papermono
devices (#2983)", 2026-08-15, Justin Mitchell.

**The real open questions for PaperMono are therefore not "can it be ported" but:**
1. ~~**Partial/windowed refresh is incomplete upstream.**~~ **Resolved 2026-09-20 —
   it is complete upstream.** `MagicCube/free-ink-on-paper-mono` carries
   `patches/freeink-paper-mono-window-refresh.patch`, adding RAM window addressing
   (`0x44/0x45/0x4E/0x4F`) to `PaperMonoDriver.cpp`. The 2026-09-02 pass could not say
   how much of it had landed. It all had: commit `4327a6d` "Add PaperMono window refresh
   support" (Henry Li, the patch's own author), merged 2026-08-26 as PR #58
   (`9a6f7d1`), +142/−4 across the same two files. The patch **does not apply** to SDK
   `main` and **does** apply to that repo's own older pin `df4a1b7b`. `executed-success`.
   **CrossPoint's pinned SDK `68425f8e` contains it; CrossInk's and `freeink-reader`'s
   pins do not** — see [PaperMono windowed refresh](../../frameworks/freeink-sdk/papermono-window-refresh.md).
2. **Flash headroom.** 81.8 % used. Adding features is constrained.
3. **Hardware validation.** Everything above is compile-and-CI evidence. I have no device.

---

## 1. The division of labour

`crosspoint-reader/ROADMAP.md:41-43` states the intended order explicitly:

> Adding support for a new device is done in the [FreeInk SDK](https://freeink.org) first
> (display, input, storage, battery drivers), followed by a commit to this repo adding
> board support (build environment and device configuration).

So a port is **two PRs against two repos, in order**. The SDK owns pins, panels, and
peripherals; CrossPoint owns build envs, UI affordances, and anything that must change
because the device has a capability the reader has never seen before.

---

## 2. FreeInk SDK — file-by-file

The documented procedure is `freeink-sdk/README.md:789-814`, summarised:

1. Add a `BoardProfile` to `BoardConfig.h` (pins, geometry, controller, input style,
   optional touch/frontlight/audio) plus a `FREEINK_DEVICE_*` flag and a `selectDevice`
   case pointing `ACTIVE` at it.
2. **Existing controller** → reuse the driver, inject a tuned **config struct** with your
   LUTs/waveforms via `-DFREEINK_UC8253_X3_CONFIG=yourConfig` or
   `-DFREEINK_SSD1677_CONFIG=...`. **Do not edit the driver.** Resolution is always a
   `BoardProfile` field (`displayWidth/Height`); the config struct is purely waveforms.
   **New controller** → add a `PanelDriver` in its own file plus a `FREEINK_DRIVER_*` flag.
3. Each device gets its own profile, flag, and build env. Two devices share a binary only
   when runtime-distinguishable on the same MCU and pinout (the X3/X4 case).

### What that costs in practice — three measured examples (`executed-success`)

**(a) Xteink X4 Classic** — new device, *existing* board, *existing* drivers.
`freeink-sdk@8eb982d`, **7 files, +295 / −30**:

| File | Why |
|---|---|
| `libs/hardware/BoardConfig/include/BoardConfig.h` | +141 — the profile, flag, capability rows |
| `docs/xteink-x4c-support.md` | +103 — new device doc (expected, not optional in practice) |
| `platformio.sample.ini` | +21 — sample env |
| `libs/hardware/XteinkDetect/src/XteinkDetect.cpp` | +29 — detection |
| `libs/display/.../driver/Uc8279X4Driver.cpp` | +17 — controller variant handling |
| `libs/hardware/SDCardManager/src/SdmmcBlockDevice.cpp` | +8 — SDMMC quirk |
| `README.md` | +6 — device table row |

**(b) M5Stack PaperS3** — new device reusing the LovyanGFX driver, but needing its own
board-support library. `freeink-sdk@d0c81dcd`, **10 files, +397 / −18**: the four above plus
a whole new `libs/hardware/BoardPaperS3/` (`library.json`, `include/BoardPaperS3.h`,
`include/BoardPaperS3Pins.h`, `src/BoardPaperS3.cpp`, `src/M5PaperS3LgfxConfig.cpp`) and
`+22` in `LgfxEpdDriver.cpp`.

**(c) OnePage** — new device **and a new MCU family** (ESP32-C61).
`freeink-sdk@3e5aff1`, **8 files, +245 / −20**, and note it touched four *managers*:
`BoardConfig.h` (+74), `InputManager.cpp` (+40, a new `InputStyle::OnePageAdcLadder`),
`BatteryMonitor.cpp` (+13, charge-pause sampling), `SDCardManager.cpp` (+10, rail settle +
retry), `PowerManager.cpp` (+3, C61 deep-sleep guard), plus docs, README and sample ini.
Contributed by an **outside contributor** (MoveCall) — evidence the porting path is usable
by non-maintainers.

### The canonical SDK porting file set

| Always | Usually | Only if… |
|---|---|---|
| `libs/hardware/BoardConfig/include/BoardConfig.h` — device flag, MCU-family row, capability rows, `BoardProfile`, `selectDevice` case | `docs/<device>-support.md` | new controller → `libs/display/FreeInkDisplay/src/driver/<New>Driver.{h,cpp}` + `FREEINK_DRIVER_*` |
| `platformio.sample.ini` — sample env | `README.md` — device table + a support section | complex power/reset → `libs/hardware/BoardConfig/include/<Device>Board.h` (+ PMIC/expander headers) |
| | | new board-support lib → `libs/hardware/Board<Name>/{library.json,include/,src/}` |
| | | new input topology → `libs/hardware/InputManager/src/InputManager.cpp` |
| | | non-standard battery → `libs/hardware/BatteryMonitor/src/BatteryMonitor.cpp` |
| | | SD quirks → `libs/hardware/SDCardManager/src/{SDCardManager,SdmmcBlockDevice}.cpp` |
| | | new MCU family → `libs/hardware/PowerManager/src/PowerManager.cpp` + `FREEINK_MCU_*` |
| | | external display lib → per-env `lib_deps` + `#include` inside the driver's `#if` guard |

**Realistic effort:** ~250–400 lines across 7–10 files for a device whose controller is
already supported. A genuinely new panel controller adds a driver (the existing ones run
several hundred to ~1,000 lines each). **No CI will check your work — the SDK has no
workflows.**

---

## 3. CrossPoint Reader — file-by-file

CrossPoint has **no device abstraction of its own**; it consumes the SDK's. So the minimum
is small, and the real cost is proportional to *new capabilities*, not new devices.

### Minimum for a device the SDK already supports

1. **`platformio.ini`** — add `[env:<device>]`, `[env:<device>-gh_release]`,
   `[env:<device>-gh_release_rc]` with `board`, `board_build.mcu`, memory type, and
   `-DFREEINK_DEVICE_<NAME>=1` plus any `-DFREEINK_CAP_*`, `-DBOARD_HAS_PSRAM`,
   `-DUSE_BLOCK_DEVICE_INTERFACE=1`, `USB_PRODUCT`/`USB_MANUFACTURER`. Model on
   `platformio.ini:343-402` (papermono).
2. **`.github/workflows/ci.yml`** — add the env to the matrix (`:79-90`).
3. **`.github/workflows/release.yml` / `release_candidate.yml`** — add the release artifact.
4. **`src/network/FirmwareBoardTag.cpp`** — register the board tag so OTA refuses to flash
   the wrong image (`OtaUpdater.h:30` `WRONG_DEVICE_ERROR`).

Whether the submodule pin also needs bumping depends on whether the SDK change is already
in the pinned commit (`.gitmodules` + gitlink).

### What it actually cost for PaperMono + X4 Pro

`crosspoint-reader@bbca4886` — **54 files, +1,419 / −176**, *plus* a `freeink-sdk` submodule
bump. But this landed **two devices at once and three new capabilities** (frontlight
control, swipe gestures, the X4 Pro home key). Grouped:

| Group | Files | Note |
|---|---|---|
| Build & CI | `platformio.ini` (+97), `ci.yml` (+107/−…), `release.yml` (+83), `release_candidate.yml` (+45), `release-fonts.yml` | the unavoidable core |
| Submodule | `freeink-sdk` gitlink | |
| HAL wrappers | `lib/hal/HalDisplay.{h,cpp}`, `HalFrontlight.{h,cpp}` (+67, **new**), `HalGPIO.{h,cpp}`, `HalPowerManager.cpp` | new capability plumbing |
| OTA safety | `src/network/FirmwareBoardTag.{h,cpp}` (+125, **new**), `FirmwareFlasher.{h,cpp}`, `OtaUpdater.{h,cpp}`, `lib/JsonParser/ReleaseJsonParser.{h,cpp}` | per-device artifacts need per-device identification |
| New UI | `src/activities/util/FrontlightPanelActivity.{h,cpp}` (+326, **new**) | because the device *has* a frontlight |
| Input | `src/MappedInputManager.{h,cpp}`, `src/activities/ActivityManager.cpp`, `src/activities/reader/ReaderUtils.h` (+71) | touch/swipe |
| Settings & i18n | `src/CrossPointSettings.h`, `src/SettingsList.h`, `lib/I18n/translations/english.yaml` (+9) | new user-visible options |
| Runtime | `src/main.cpp` (+160) | boot/power sequencing per device |
| Touched-in-passing | ~20 activity files, +4-13 lines each | UI scale / capability guards |

**Rule of thumb:** if the new device is capability-identical to an existing target, expect
**4–6 files**. If it introduces a capability CrossPoint has never rendered (frontlight,
touch, colour, audio), expect **dozens**, because a new activity, new settings entries, and
30+ translation files come with it.

---

## 4. Side-by-side

| | **FreeInk SDK** | **CrossPoint Reader** |
|---|---|---|
| Owns | pins, panel drivers, peripherals, power rails | build envs, UI, OTA identity, user settings |
| Device definition | `BoardProfile` struct + `FREEINK_DEVICE_*` flag in `BoardConfig.h` | a `[env:...]` block passing the SDK's flag |
| Capability model | derived macros over the device set (`BoardConfig.h:193-299`) | consumes them; adds UI where a capability is user-visible |
| Single file that matters most | `libs/hardware/BoardConfig/include/BoardConfig.h` (2,010 lines) | `platformio.ini` (402 lines) |
| Typical port size | 7–10 files, ~250–400 lines | 4–6 files if capability-identical; 50+ if not |
| Panel work needed? | yes if new controller; else inject a config struct | never |
| Docs expected | `docs/<device>-support.md` + README row | none formally |
| CI validation | **none** (no workflows) | yes — 4-env matrix with size reporting |
| Review load | 1 dominant maintainer (74 % of commits) | 56 authors / 200 commits; 156 PRs merged in Aug 2026 |
| Order | **first** | second |

---

## 5. Porting to a *genuinely* new device — recommended sequence

1. **Confirm the MCU family is supported.** C3, C61, S3, classic ESP32
   (`BoardConfig.h:91-97`). A fifth family means touching `PowerManager` and the family
   macros (the OnePage C61 commit is the template).
2. **Identify the panel controller.** If it is one of SSD1677 / UC8253 / UC8179 / UC8279 /
   ED2208 / IT8951 / ED047TC1-via-LovyanGFX, you write **no driver** — only a profile and
   possibly a waveform config struct.
3. **Write the `BoardProfile`.** Pins, geometry, orientation, input style, and the
   defaulted blocks you need (`mic`, `sensors`, `power`, `uiScale`, `viewableInsets`).
   Set `uiScale > 1.0` for touch devices — panels are ~220-235 PPI and a 30 px row is ~3 mm
   (`BoardConfig.h:714-719`).
4. **Handle exotic power/reset behind a board header + hooks**, not in the managers. The
   PaperMono PMIC/expander case is the worked example:
   `PaperMonoBoard.h` owns bring-up; `SDCardManager::setPowerHook()` keeps the SD manager
   device-agnostic (`freeink-sdk/README.md:114-118`).
5. **Add the sample env**, get the SDK PR merged.
6. **Then** open the CrossPoint PR: envs, CI matrix, release workflows, board tag.
7. **Expect hardware iteration.** The SDK README flags several devices as having
   "orientation/SD-sharing pending hardware validation" (Sticky) and "rotation/touch-flip
   pending hardware validation" (PaperS3). Compile-clean ≠ working.

---

## 6. Risks and caveats

- **The SDK has no CI and no releases.** Nothing mechanically verifies a port; consumers
  pin raw submodule SHAs. `executed-success` (empty `.github/workflows/`, empty releases API).
- **Bus factor 1 on the SDK** — 148 of the last 200 commits by one person.
- **Forks drift on the SDK pin.** CrossPoint pins `68425f8e`; CrossInk pins `1ff02026`;
  `free-ink-on-paper-mono` pins `df4a1b7b`; `freeink-reader` pins `1dc8dfc6`. A port
  verified against one pin is not automatically valid against another.
- **90°/270° rotation is unsupported** in the SSD1677 driver — only mirror/180
  (`freeink-sdk/README.md:371-372`). A portrait-mounted landscape panel needs a software
  transpose that does not exist.
- **Flash and IRAM are nearly full** on the S3 targets I built (81.8 % flash, **100 % IRAM**).
  A new device that needs extra code may not fit without the Phase-1 footprint work landing.
- **`free-ink-on-paper-mono` has no LICENSE** — do not copy code from it.
- All effort estimates here are `inferred` from git history. None is a measured port.
