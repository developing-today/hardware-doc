# PaperMono — third-party firmware, software projects and community venues

> **Retrieval snapshot 2026-09-02 (UTC).** Every row was re-retrieved on this date unless a
> different date is given on the row. This pass supersedes and in several places **corrects**
> the 2026-09-01 community sweep recorded in the device
> [`README.md`](README.md#community-editorial-and-project-coverage); the corrections are
> collected in [§8](#8-what-this-pass-changes-in-the-existing-record).
>
> **No PaperMono hardware was available to this pass.** Nothing below was built, flashed or
> executed. Every project was assessed by **static inspection of published source, published
> binaries, repository metadata and author statements**. Where a project is described as
> "runs on hardware", that is *the author's* evidence, classified below — never this record's.
>
> Companion files: [`examples/catalog.json`](examples/catalog.json) (machine-readable, one
> entry per example including the rejected ones) · [`examples/search-log.md`](examples/search-log.md)
> (every query and disposition) · [`examples/best.md`](examples/best.md) (the selected portfolio).

---

## 1. Headline findings

1. **The CrossPoint reader is open source, and its PaperMono support is upstream.**
   The binary held at
   [`artifacts/firmware/crosspoint-paper-mono-cjk-1.5.0-RC.bin`](artifacts/firmware/)
   traces, by exact commit hash, to **[`MarsTechHAN/crosspoint-reader-mono`](https://github.com/MarsTechHAN/crosspoint-reader-mono)
   at `87a191fcea17a9658686083187765c600ad03866`** — a public MIT fork of
   **[`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader)**
   (MIT, 7,487 stars, homepage <https://crosspointreader.com>). Full derivation in
   [§3](#3-crosspoint-the-source-repository-question-answered).
2. **The ecosystem is roughly five times larger than the previous pass recorded.** That pass
   found "four third-party GitHub repositories and one YouTube video". This pass finds
   **9 projects with firsthand PaperMono hardware evidence**, **13 upstream frameworks/
   libraries that ship a PaperMono target**, and **2 official vendor demos**, among
   **129 distinct repositories surfaced** by GitHub search and **48 inspected in detail**.
3. **Support landed *before* the product did.** `crosspoint-reader` merged PaperMono support
   into `develop` on **2026-08-16**, five days before launch; M5Stack merged PaperMono
   changes into M5Unified from **2026-07-17** and into M5GFX from **2026-07-14**; the
   `m5stack_papermono` Arduino board id shipped in M5Stack Arduino core **3.3.9**. A
   pre-retail hardware-beta channel demonstrably existed
   ([§4.4](#44-the-hardware-beta-channel)).
4. **The independent written-coverage picture is unchanged and still bleak.** Zero written
   reviews, one hands-on video (Volos Projects, vendor affiliate link, self-described first
   look), all written articles traceable to one vendor blog post. Re-verified 2026-09-02.
5. **The first independent end-user photographs of third-party firmware on retail hardware
   appeared on 2026-09-01/02**, on r/xteinkereader, not on any venue the previous pass
   searched ([§6.3](#63-reddit)).
6. **M5GFX's board-autodetect source names an unannounced "PaperMono Pro".** No such SKU
   exists on the M5Stack store, docs site or M5Burner device list. See
   [§8](#8-what-this-pass-changes-in-the-existing-record).

---

## 2. How projects are classified here

The method requires that demonstrated work is not mixed with claims. Six classes are used,
and every project in [§4](#4-the-project-population) carries exactly one.

| Class | Meaning | Bar |
|---|---|---|
| **D — Demonstrated** | The author presents firsthand evidence of the code running on a PaperMono or PaperMono-Lite | A device photograph, a measured number that cannot come from a datasheet, a factory-flash dump, an explicit "verified on hardware" statement backed by matching commit history, or a published flashable binary plus a bug report containing device-specific observations |
| **S — Shipped target** | An upstream framework, library or firmware that carries a first-class PaperMono build target, merged and released, but where *this record* found no firsthand hardware evidence from the maintainers themselves | A merged board profile, build environment, board id, or driver on a default branch or in a release |
| **V — Vendor** | Published by M5Stack | — |
| **P — Proposal / untested** | PaperMono support written but explicitly not validated, or validated only by compilation | Author's own statement, or absence of any hardware claim in a compile-only artefact |
| **C — Copy** | A mirror, vendored tree or re-publication of someone else's PaperMono code, adding nothing | — |
| **R — Rejected** | Surfaced by search, not a PaperMono project | See [§5](#5-rejected-false-positives-and-adjacent-work) |

Evidence-type letters used inside rows follow the existing record's key:
`M` firsthand measurement · `O` firsthand ownership · `P` demonstrable project ·
`Op` opinion · `H` hearsay · `V` vendor-published.

> **A standing caveat on all of class D.** "Demonstrated" means *the author demonstrated it*.
> None of it was reproduced here. Where an author's claim is unusually specific (a measured
> refresh time, a register value) that raises confidence that hardware was present; it does
> not make the number correct.

---

## 3. CrossPoint: the source-repository question, answered

The previous pass recorded CrossPoint as *"roadmap, not shipped support"*. That is wrong, and
the correction is fully evidenced.

### 3.1 Provenance chain for the held binary

| Link | Evidence | Retrieved |
|---|---|---|
| The binary's build id is `paper-mono-v2-15-g87a191f`, app name `crosspoint-reader-mono` | strings extracted in the prior pass, `scratch/m5stack-papermono/docs/firmware/crosspoint-paper-mono-cjk-1.5.0-RC.strings.txt` | 2026-09-01 |
| The M5Burner listing for it declares `sourceUrl` = `https://github.com/MarsTechHAN/crosspoint-reader-mono` | `https://burner.m5stack.com/api/v1/firmwares/2091144466157694978` | 2026-09-02 |
| That repository's `develop` head is **`87a191fcea17a9658686083187765c600ad03866`** — the `g87a191f` in the build id | `git ls-remote https://github.com/MarsTechHAN/crosspoint-reader-mono.git` | 2026-09-02 |
| It carries an annotated tag **`paper-mono-v2`** (tag object `296eaff965382e4bd2f982fa83f1370c7a8d9ff3`, commit `efbfa3a08605af7bbf77b8e1d19e9ccab5bc43e7`), making `git describe` = `paper-mono-v2-15-g87a191f` exactly | same `ls-remote` | 2026-09-02 |
| Its `platformio.ini` defines `[env:paper_mono]` with `-DCROSSPOINT_VERSION="1.5.0-paper-mono"` — matching the binary strings `CrossPoint version: 1.5.0-paper-mono` and `CrossPoint-ESP32-1.5.0-paper-mono` | `https://raw.githubusercontent.com/MarsTechHAN/crosspoint-reader-mono/develop/platformio.ini` | 2026-09-02 |
| It is a **fork of `crosspoint-reader/crosspoint-reader`** (GitHub `parent` field), created 2026-07-29, last pushed 2026-08-12 | GitHub API `/repos/MarsTechHAN/crosspoint-reader-mono` | 2026-09-02 |
| Its submodule `freeink-sdk` is repointed to **`MarsTechHAN/freeink-sdk-mono`** at `f5518c7a39d3956dbc9d43be508bf9edae8f222d`; HEAD commit `87a191f`'s message is *"chore: bump freeink-sdk to the 5% Li-ion SoC curve — Picks up f5518c7…"* | GitHub contents API + commit API | 2026-09-02 |

**Answer.** CrossPoint is **open source, MIT-licensed**. Homepage <https://crosspointreader.com>.
Canonical repository <https://github.com/crosspoint-reader/crosspoint-reader>. The specific
M5Burner build held in this record was produced from the public fork
<https://github.com/MarsTechHAN/crosspoint-reader-mono> at commit `87a191f`, against the
public SDK fork <https://github.com/MarsTechHAN/freeink-sdk-mono> at `f5518c7`.

### 3.2 Upstream also ships PaperMono

Upstream `crosspoint-reader/crosspoint-reader` (`develop`, head
`e6139861a2a8c634aa18c333b7e214ee51a9965c`, 2026-09-01) carries:

- `[env:papermono]`, `[env:papermono-gh_release]`, `[env:papermono-gh_release_rc]` in
  `platformio.ini`, on `board = esp32-s3-devkitc1-n16r8`, `memory_type = dio_opi`, with
  `-DFREEINK_DEVICE_PAPERMONO=1`, `-DFREEINK_CAP_USB_MSC=1`, `-DBOARD_HAS_PSRAM`,
  `-DUSB_PRODUCT="CrossPoint_Paper_Mono"`;
- `src/network/FirmwareBoardTag.cpp`, which derives the OTA compatibility tag
  `CROSSPOINT-BOARD-V1:papermono;` from `FREEINK_DEVICE_PAPERMONO`;
- `ROADMAP.md:40`, whose "pluggable per-device SDK layers" item is now struck through and
  marked **Done**, listing PaperMono among the shipped ESP32-S3 targets.

The enabling change is **PR #2983 "feat: Add support for x4pro & papermono devices"** by
[@itsthisjustin](https://github.com/itsthisjustin), **merged into `develop` 2026-08-16
01:22 UTC** (merge commit `bbca4886c97a251480ea908aad00ea16dc3d8b75`), from branch
`feat-x4-papermono-support`. An earlier attempt, PR #2675 (2026-07-22), was closed unmerged.

> **A stale third-party claim.** `jpirnay/witchhunt-reader`'s
> [`docs/x4pro_support.md`](https://github.com/jpirnay/witchhunt-reader/blob/master/docs/x4pro_support.md)
> states that PR #2983 is *"still open — it is on neither `develop` nor `master`"*. That was
> true when written; it is **false as of 2026-09-02**. Do not propagate it.

### 3.3 The CrossPoint constellation

| Repository | Role | Licence | Head (2026-09-02) | PaperMono? |
|---|---|---|---|---|
| [`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader) | Upstream reader firmware | MIT | `e6139861a2a8c634aa18c333b7e214ee51a9965c` | **Yes** — 3 build envs |
| [`MarsTechHAN/crosspoint-reader-mono`](https://github.com/MarsTechHAN/crosspoint-reader-mono) | Fork that produced the held M5Burner binary | MIT | `87a191fcea17a9658686083187765c600ad03866` | **Yes** — `[env:paper_mono]`, `[env:paper_mono_lab]` |
| [`Free-Ink/freeink-sdk`](https://github.com/Free-Ink/freeink-sdk) | The HAL CrossPoint builds on | MIT | `fad70f28a982c978737410e535a4f7276ce28c19` | **Yes** — `PaperMonoBoard.h`, `PaperMonoDriver.cpp` |
| [`MarsTechHAN/freeink-sdk-mono`](https://github.com/MarsTechHAN/freeink-sdk-mono) | SDK fork pinned by the above | MIT | `f5518c7a39d3956dbc9d43be508bf9edae8f222d` | **Yes** |
| [`crosspoint-reader/crosspoint-simulator`](https://github.com/crosspoint-reader/crosspoint-simulator) | Desktop simulator of the firmware | MIT | `6aa3b5476f783953bff4ae8aa0b84d9a64dd07ef` | **Yes** — `simulator_papermono` / `-DSIMULATOR_DEVICE_PAPERMONO` |
| [`crosspoint-reader/crosspoint-tools`](https://github.com/crosspoint-reader/crosspoint-tools) | Web installer / tooling | MIT | `a3f0abf6a06fe0abe9309b3e0ff3c25aea11579a` | Mentions papermono in the worker |
| [`crosspoint-reader/escape-hatch`](https://github.com/crosspoint-reader/escape-hatch) | 400 KB SD-card recovery flasher | **none** | `90841adf6304354d1393936d1ca203294b76c09b` | Carries `FirmwareBoardTag.cpp`; targets X3/X4 |
| [`0x1abin/crossmux`](https://github.com/0x1abin/crossmux) | Fork with a **PaperMono Hardware Beta** channel | MIT | `85f7696b3ee51e0a067cdc012cfabc2783616f3a` | **Yes** — 4 papermono envs |
| [`Belphemur/crosspoint-x-reader`](https://github.com/Belphemur/crosspoint-x-reader) | Fork, X4-Pro-focused | MIT | `4547187dc29cca731352147a63877c24184fe1fc` | Inherits 3 papermono envs |
| [`sfoulad/midad-by-foulad`](https://github.com/sfoulad/midad-by-foulad) | Arabic-focused derivative | MIT | `ef3b455c3aa9ea06204cabbae717b05bc28c1803` | Inherits 3 papermono envs |

Forks that do **not** carry a PaperMono target — and so are *not* PaperMono projects despite
appearing in searches — are listed in [§5](#5-rejected-false-positives-and-adjacent-work):
`eszter007/matcha-reader`, `jpirnay/witchhunt-reader`, `aBER0724/crosspoint-reader-cjk`,
`juicecultus/crosspoint-reader-papers3`, `dito94/CrossDiTo`.

---

## 4. The project population

### 4.1 Class D — demonstrated on PaperMono hardware (9)

| Project | Author | Licence | Framework | Head commit | What the hardware evidence is | What it demonstrates about the device |
|---|---|---|---|---|---|---|
| [`MagicCube/free-ink-on-paper-mono`](https://github.com/MagicCube/free-ink-on-paper-mono) | Henry Li ([@henry19840301](https://x.com/henry19840301)) | **none published** | PlatformIO / Arduino / FreeInk SDK | `34cc879427d5fc0b35f6af5084d4e7a003457665` (2026-08-27) | `M+O+P`. Author posted dated purchase photographs 2026-08-21 04:09 UTC; his SDK patch was **merged upstream** as [freeink-sdk PR #58](https://github.com/Free-Ink/freeink-sdk/pull/58), 2026-08-26 | RX8130 time, M5PM1 battery/USB/charge telemetry, touch + buttons, light/dark whole-screen inversion, frontlight held at 127/255, async refresh with periodic full cleanup, **disabling M5PM1's default single-click reset**, rectangular (window) partial refresh |
| [`MingRZou/PaperMono-Launcher`](https://github.com/MingRZou/PaperMono-Launcher) | MingRZou | MIT | PlatformIO / Arduino / M5Unified 0.2.21 | `daf3edcee4f8669e2adf7a58bc174d62e4e40f42` (2026-08-30), release `v0.1.0` | `P+O+M`. Repo carries `docs/images/papermono-launcher-real-hardware.jpg`; **published on M5Burner** as firmware `2094259851119865857`, binary `PaperMono-Launcher-v0.1.0.bin`; author's [crossmux issue #218](https://github.com/0x1abin/crossmux/issues/218) reports firsthand device behaviour (enters S3 download mode, detected as 16 MB flash / 8 MB PSRAM); his [Launcher PR #416](https://github.com/bmorcelli/Launcher/pull/416) was **merged upstream** 2026-08-29 | Launcher UI, touch/buttons/SD/frontlight, SSD1677 refresh policy with periodic full cleanup, protected payload partition install + boot + return-to-launcher, F1-v1 FullFlash wrapper handling |
| [`hectorzin/M5PaperMono-HomeAssistant-ESPHome`](https://github.com/hectorzin/M5PaperMono-HomeAssistant-ESPHome) | hectorzin | **none published** | ESPHome ≥ 2026.6.x (ESP-IDF) | `c144086af7291f6340422361534e9374fa4d2bdd` (2026-09-01) | `M+P`. README states **measured** refresh times (PARTIAL ≈ 0.9 s, FULL ≈ 4.3 s) and a specific interrupt route; those are not published vendor figures | **The only measured refresh timings found anywhere.** Also: BMI270 INT1 → M5PM1 GPIO4 → ESP32 GPIO1 motion path; frontlight at 30 % on activity with timeout; ESP32 light sleep with Wi-Fi off; M5PM1 SHUTDOWN for quiet hours; M5IOE1 pin numbering as ESPHome sees it (EPD power 2, EPD reset 4, touch reset 5, touch power 12) at I²C `0x4F` |
| [`GOROman/learning-paper-mono`](https://github.com/GOROman/learning-paper-mono) | GOROman | **none published** | PlatformIO / Arduino / M5GFX + M5Unified + RadioLib | `21abc4ec84f17b3966bc7c936f78a1e4facc6372` (2026-09-02) | `M+O+P`. Steps 1–4 marked done with 「実機表示確認済み」 (*verified displaying on the actual device*); a **16 MB factory flash dump** is described as taken and kept out of git; a two-device LoRa link to a Cardputer ADV is parameterised | Step-by-step per-feature bring-up: display, touch, buzzer, **LoRa TX/RX**, frontlight 0–10 steps, window partial refresh. Records the LoRa pin map (SPI3 SCK 39 / MISO 40 / MOSI 38, NSS 41, DIO1 5, BUSY 21; power via M5PM1 GPIO2; RST/ANT-SW via M5IOE1 pins 10/2) and the demo radio settings (868 MHz, BW 62.5 k, SF12, CR8, sync 0x34, 22 dBm, TCXO 3.0 V) |
| [`tinyrange/renvo`](https://github.com/tinyrange/renvo) — [issue #444](https://github.com/tinyrange/renvo/issues/444) + [PR #445](https://github.com/tinyrange/renvo/pull/445) | Vbitz (Joshua Scarsbrook) | Apache-2.0 | Renvo (Rust/`.rtg`), `esp32s3/xtensa_lx7` backend | repo head `1215bdd5d69824b924d06572ad4476460dbff044`; **PR #445 open, unmerged**, 56 files, +7,190 lines | `M+P`. A structured bring-up plan whose checkboxes are ticked with hardware-specific outcomes ("hardware-confirm enable and shutdown-off behavior", "hardware-test a two-pixel touch-trails example"), plus explicit factory-flash backup and JEDEC RDID capacity detection | The most systematic independent bring-up: board registration, M5PM1 + M5IOE1 drivers with transaction tests, bounded 100 kHz software I²C, SSD1677 protocol driver over bounded 20 MHz SPI2 mode 0, OTP full/partial/4-gray refresh with a mandatory monochrome baseline and automatic full-refresh recovery after ten partials, FT6336G driver with active-area normalisation, serial and touch **hardware oracles** |
| [`MarsTechHAN/crosspoint-reader-mono`](https://github.com/MarsTechHAN/crosspoint-reader-mono) + [`freeink-sdk-mono`](https://github.com/MarsTechHAN/freeink-sdk-mono) | Han (MarsTechHAN) | MIT | PlatformIO / Arduino (pioarduino 55.03.37) | `87a191fcea17a9658686083187765c600ad03866` / `f5518c7a39d3956dbc9d43be508bf9edae8f222d` | `P`. A **shipped, downloadable binary** on M5Burner (24→27 downloads), plus a `[env:paper_mono_lab]` bare-metal SSD1677 characterisation harness, a serial waveform lab (`CMD:WAVE`), a sleep lab (`CMD:WRIST`) and touch-probe tracing — instrumentation that is pointless without a device | A complete EPUB reader on the device: CJK font pipeline (`.cpfont`, PSRAM glyph arena raised 128→512 slots for Han pages), WebDAV/OPDS/KOSync networking, USB MSC file transfer, native 1-bit SDMMC via SdFat block-device interface |
| [`EggUncle/PaperMonoCalendar`](https://github.com/EggUncle/PaperMonoCalendar) | EggUncle | **none published** | Arduino CLI 1.4.1 / M5GFX | `53385729b35249c4fe4f8a3f2d7ded6ad2de5696` (2026-08-31) | `P`, **partial**. README states v2 activity sync and `HUB / SYNCED` are 「已在 PaperMono 上确认」 (*confirmed on PaperMono*) and the date format was user-confirmed; v3 RTC calibration is explicitly **compiled and flashed but not yet accepted on device** | Landscape 800×480 calendar, BLE activity tiles, RTC sync, four-level black/white dither used as pseudo-grey, PSRAM canvas then push, minute-scoped partial updates with a "every 10th update use quality" counter. **Pins an exact toolchain**: M5Stack ESP32 core 3.3.9, M5Unified 0.2.21, M5GFX 0.2.28, M5PM1 1.0.7, M5IOE1 1.0.9 |
| [`LuoIsHere/SeeSeeBook`](https://github.com/LuoIsHere/SeeSeeBook) | LuoIsHere | MIT | ESP-IDF (devcontainer), M5GFX `M5Canvas` for rasterising only | `64bc8332628f00d025a6f68e72fe951d9db9f44f` (2026-09-01) | `P`, **implied not asserted**. No photograph and no explicit claim, but the commit log is daily iteration on device-shaped problems — *"harden PaperMono I2C recovery"*, *"serialize internal i2c and isolate ip2315 sessions"*, *"fix some display bugs"* — which is not how a paper design evolves. Classified D with that caveat stated | A cleanly layered device port: `m5_hal/paper_mono/` (display, touch, RTC, battery, storage, internal I²C) built on its **own SSD1677 OTP driver ported from `m5stack/M5PaperMono-OTP-Demo` at the pinned commit `c7c02554f89fd06f80d988b805b2a59050c78a46`**, deliberately bypassing M5GFX's `Panel_SSD1677_4Gray` waveforms. Scene-aware regional refresh policy; async SD browser |
| [`0x1abin/crossmux`](https://github.com/0x1abin/crossmux) | 0x1abin | MIT | PlatformIO / Arduino | `85f7696b3ee51e0a067cdc012cfabc2783616f3a` (2026-09-02) | `P`, **channel demonstrated, validation unanswered**. Published a `hardware-beta-papermono` / `papermono_cn` web-installer channel **before retail units were widely out**; the direct question "has this been tested on retail PaperMono hardware?" ([issue #218](https://github.com/0x1abin/crossmux/issues/218), 2026-08-24) is **still open and unanswered** on 2026-09-02 | That a pre-retail PaperMono firmware distribution channel existed. Also the source of the SSD1683→SSD1677 documentation correction ([PR #221](https://github.com/0x1abin/crossmux/pull/221), merged 2026-08-24) |

### 4.2 Class S — upstream targets that ship PaperMono support (13)

These are not "PaperMono projects"; they are the substrate the projects above stand on. Each
carries a merged, released PaperMono target.

| Project | Licence | Head (2026-09-02) | The PaperMono artefact | Note |
|---|---|---|---|---|
| [`Free-Ink/freeink-sdk`](https://github.com/Free-Ink/freeink-sdk) | MIT | `fad70f28a982c978737410e535a4f7276ce28c19` | `libs/hardware/BoardConfig/include/PaperMonoBoard.h`, `libs/display/FreeInkDisplay/src/driver/PaperMonoDriver.{h,cpp}`, `M5Pm1.h`, `M5Ioe1.h` | The single richest third-party description of the board's power topology. Sequences the PMIC and expander itself so consumer firmware never touches them; disables the PMIC single-click reset while **preserving the hardware long-hold download escape**. Describes the frontlight as PMIC 12-bit PWM driving an **AW9967** boost LED driver fed from the EPD rail — so the light only runs while EPD power is on |
| [`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader) | MIT | `e6139861a2a8c634aa18c333b7e214ee51a9965c` | 3 `papermono` envs; `FirmwareBoardTag.cpp` | See [§3.2](#32-upstream-also-ships-papermono) |
| [`crosspoint-reader/crosspoint-simulator`](https://github.com/crosspoint-reader/crosspoint-simulator) | MIT | `6aa3b5476f783953bff4ae8aa0b84d9a64dd07ef` | `simulator_papermono` target, `-DSIMULATOR_DEVICE_PAPERMONO` | Added by [PR #34](https://github.com/crosspoint-reader/crosspoint-simulator/pull/34) (@lpla), merged **2026-08-20 — the day before launch**. Exposes FT6336-compatible touch/swipe, RTC and single-channel frontlight state. **The only way to exercise PaperMono UI code without hardware** |
| [`m5stack/M5Unified`](https://github.com/m5stack/M5Unified) | MIT | `8530f5377d782e4a25a6c482de2e71c3f75ca8eb`, release **0.2.21** (2026-08-26) | `board_M5PaperMono`, `LED_PaperMono_Class`, `M5IOE1_Class`, PaperMono paths in `Power_Class` / `RTC_Class` | PaperMono PRs by @TinyuZhao merged **2026-07-17** (#279), **2026-07-23** (#286, touch wake-up), **2026-07-27** (#289, SD card power) |
| [`m5stack/M5GFX`](https://github.com/m5stack/M5GFX) | MIT | `d91077b9a607b59404e4e4a49f775c792bfae382`, release **0.2.28** (2026-08-25) | `board_M5PaperMono` in `lgfx/boards.hpp`; autodetect + `Light_M5PaperMono` in `M5GFX.cpp` | SSD1677 LUT tuning PRs by @zhenquan-yao merged **2026-07-14** (#223, fastest mode) and **2026-08-27** (#272, text/quality modes). Aborts with `"M5PaperMono need OPI-PSRAM enabled"` if octal PSRAM is off — see [`features/epaper-display.md`](features/epaper-display.md) |
| [`m5stack/uiflow-micropython`](https://github.com/m5stack/uiflow-micropython) | MIT | `587e134c61b31431335351e04ebfc05f69064bb7`, release **2.5.2** | `m5stack/boards/M5STACK_PaperMono/` (`board.json`, `mpconfigboard.cmake/.h`, `sdkconfig.board`, `manifest.py`, boot artwork), `tests/display/test_papermono_startup.py`, `docs/source/hardware/{lora,nfc}.rst` | **MicroPython/UIFlow2 is a fully supported PaperMono path and the previous pass missed it entirely.** Shipped on M5Burner as `UIFlow2.0 PaperMono` v2.5.1 (2026-08-18) and v2.5.2 (2026-08-28) |
| [`m5stack/M5PM1`](https://github.com/m5stack/M5PM1) | MIT | `be9a5456c007c333e7ac963f33bfde1ffa5d82ee`, release **1.0.7** | Standalone PMIC driver, in the Arduino library registry | Usable directly from PlatformIO (`library.json`) — GOROman's project does exactly that |
| [`m5stack/M5IOE1`](https://github.com/m5stack/M5IOE1) | MIT | `846eec7d05e25c09013be2acdb8804487f48a62e`, release **1.0.9** | Standalone expander driver, in the Arduino library registry | See [`features/io-expander.md`](features/io-expander.md) |
| [`m5stack/esphome-yaml`](https://github.com/m5stack/esphome-yaml) | MIT | `c515c83edc1aa16f11e0297d95a8528ae485931c` | `components/m5ioe1/` external component (switch, light, output, sensor) | The bridge that makes PaperMono possible in ESPHome at all; `hectorzin`'s project depends on it |
| [`m5stack/m5stack-board-id`](https://github.com/m5stack/m5stack-board-id) | **none** | `f7e2d4a4f34dfd1fb9be0630b4102cb67d3d4cca` | papermono board id added by [PR #2](https://github.com/m5stack/m5stack-board-id/pull/2), 2026-04-08 | The **earliest public trace of the product found by this pass — four and a half months before launch**, and earlier than the UserDemo repository's 2026-05-07 creation |
| [`bitbank2/bb_epaper`](https://github.com/bitbank2/bb_epaper) | GPL-3.0 | `bfb8dbca98f21e438d8cb23d306b057f516b6819`, release **2.1.11** | `EPD_M5_PAPER_MONO`, `EPD_M5_PAPER_MONO_4GRAY` product enums in `src/bb_epaper.h`; M5IOE1 GPIO sequencing in `src/bb_epaper.cpp` | **Resolves an explicit open question in the existing record.** The previous pass searched `PaperMono` and got zero hits; the code spells it `M5_PAPER_MONO`. Sequence recorded in source: IOE1 `0x4f` pin 3 → EPD 3V3 LDO on, pin 5 toggled for EPD reset, panel type `EP426_800x480` / `_4GRAY`; commented-out lines for touch enable (13), uSD enable (14), touch reset (6) |
| [`usetrmnl/trmnl-firmware`](https://github.com/usetrmnl/trmnl-firmware) | GPL-3.0 | `8f84e23002197fefb4a53eb3a1d8a10657e0b583`, release **v1.8.16** | `EPD_M5_PAPER_MONO` referenced in `src/display.cpp` | **Confirms the second half of Larry Bank's 2026-08-17 pre-launch claim** (bb_epaper *and* TRMNL BYOD). Whether a shipping TRMNL PaperMono device profile exists was not established |
| [`bmorcelli/Launcher`](https://github.com/bmorcelli/Launcher) | MIT | `69fdc7d127f516766f0406b609091b90887b83cf`, release **2.8.0** | `boards/m5stack-paper-mono/{platformio.ini,interface.cpp}` | README line 102 marks *"Port to M5-Paper Mono"* **done**. Env: `-DTFT_WIDTH=480 -DTFT_HEIGHT=800 -DROTATION=0 -DDIMMER_SETUP=30 -DHAS_2_BUTTONS=1 -DHAS_TOUCH=1`, `memory_type=qio_opi`, `M5Unified ^0.2.21`, and a **4-bit `SD_MMC`** map: CLK 13, CMD 12, D0 11, D1 10, D2 9, D3 8 |

### 4.3 Class V — official vendor examples and binaries (2 repositories, 4 M5Burner entries)

| Artefact | Where | Version / commit | Note |
|---|---|---|---|
| [`m5stack/M5PaperMono-UserDemo`](https://github.com/m5stack/M5PaperMono-UserDemo) | GitHub, MIT | `c1099107271d31a0678d661a896e2b04dbb331ea` (2026-08-10) | Factory firmware, ESP-IDF 5.5.1, fifteen demo apps. One fork exists — `Tr2e/M5PaperMono-UserDemo` — and it is **byte-identical** (GitHub compare: `status: identical, ahead 0, behind 0`) |
| [`m5stack/M5PaperMono-OTP-Demo`](https://github.com/m5stack/M5PaperMono-OTP-Demo) | GitHub, MIT | `c7c02554f89fd06f80d988b805b2a59050c78a46` (2026-08-20) | Minimal SSD1677 driver using only the panel's OTP waveforms; vendor-recommended over M5GFX. Reused verbatim by SeeSeeBook |
| `PaperMono UserDemo` v1.2 | M5Burner id `2089640807996628993` | `C153-PaperMono-ESP32S3R8-UserDemo-V1.2-yaozhenquan-8300e309-20260806_0x00.bin`, uploaded 2026-08-18, **18 downloads** | Binary held locally |
| `UIFlow2.0 PaperMono` v2.5.1 / v2.5.2 | M5Burner id `2089633464953118721` | `…uiflow-efa3815d-…-v2.5.1-20260818.bin` / `…uiflow-428a68d0-…-v2.5.2-20260828.bin`, **3 downloads total** | Build ids embed uiflow-micropython commit prefixes |

### 4.4 The hardware-beta channel

Three independent facts establish that PaperMono units reached third-party developers before
retail availability, which is why so much software existed on day one:

1. `crosspoint-reader` merged PaperMono support **2026-08-16**, five days before launch
   (PR #2983); the simulator profile landed **2026-08-20**, one day before.
2. `0x1abin/crossmux` published a firmware channel literally named
   **`hardware-beta-papermono`**, referenced in [issue #218](https://github.com/0x1abin/crossmux/issues/218)
   on 2026-08-24.
3. M5Stack's own libraries carry PaperMono changes from **2026-07-14** (M5GFX) and
   **2026-07-17** (M5Unified), and the board id from **2026-04-08**.

### 4.5 Class P — proposals and explicitly untested support (4)

| Project | Licence | Head | Why it is a proposal, not a demonstration |
|---|---|---|---|
| [`koosoli/ESPHomeDesigner`](https://github.com/koosoli/ESPHomeDesigner) | GPL-3.0 | `0d82d6763c36b23cfd153d44126d8cd2b7d09425`, release `v1.0.0-rc.42` (2026-08-26) | **The author flags it himself**, and does so well: *"The profile is flagged untested — the device launched only days ago and no community ESPHome config exists yet."* Also honestly states what is missing: battery level, frontlight dimming and deep sleep are not wired "because they run through the M5PM1 PMIC, which has no ESPHome component at this time" |
| [`shelbeeely/claude-desktop-buddy`](https://github.com/shelbeeely/claude-desktop-buddy) | NOASSERTION (fork of `anthropics/claude-desktop-buddy`) | `15d5e2c947686151453d9c849217442096b384d0` | [PR #4](https://github.com/shelbeeely/claude-desktop-buddy/pull/4) "Add M5Stack Paper Mono support (env:papermono)", merged **2026-08-21 — launch day**. The PR body's own verification is *reading* `PaperMonoBoard.h`: "Verified end-to-end (read `PaperMonoBoard.h` in full)… **zero new `setup()` code** was needed". Three files, no device |
| [`Belphemur/crosspoint-x-reader`](https://github.com/Belphemur/crosspoint-x-reader) + [`Belphemur/freeink-sdk`](https://github.com/Belphemur/freeink-sdk) | MIT | `4547187dc29cca731352147a63877c24184fe1fc` / `089bd85a71bed6e0e5ef635dbae3da56dd12a2fd` | Very active fork (release v1.9.1, 2026-09-01) but **every PaperMono-adjacent PR in it is X4-Pro work**; the papermono envs are inherited from upstream, unexercised |
| [`sfoulad/midad-by-foulad`](https://github.com/sfoulad/midad-by-foulad) | MIT | `ef3b455c3aa9ea06204cabbae717b05bc28c1803`, release `v1.8.57` | Same: 3 inherited papermono envs; the project's own hardware-test RC branches are explicitly X4 Pro |

### 4.6 Class C — copies and vendored trees (3 named + ~15 unnamed)

Recorded so they are not mistaken for independent evidence.

| Repository | What it is |
|---|---|
| [`goodyttoor/inkback-freeink-sdk`](https://github.com/goodyttoor/inkback-freeink-sdk) | A **detached copy** of `Free-Ink/freeink-sdk` (GitHub does not mark it a fork; `default_branch = inkback/inkmotion`), README and MIT licence preserved, `PaperMonoBoard.h`/`PaperMonoDriver` carried along unchanged. Head `d26ab55af1c67d451de99f08280a6de83608fd0b`, last pushed 2026-08-18 |
| [`dito94/CrossDiTo`](https://github.com/dito94/CrossDiTo) | A CrossPoint derivative that **vendors `freeink-sdk/` in-tree** rather than as a submodule. Its own `platformio.ini` has 7 envs and **no papermono env** — the PaperMono files are dead weight |
| [`vjFaLk/esphome-xteink`](https://github.com/vjFaLk/esphome-xteink) | Wraps the whole FreeInk SDK as an ESPHome external component under `components/xteink/sdk/`. Targets Xteink; PaperMono files carried, not exercised |
| ~15 further repositories | Vendored `M5GFX`/`M5Unified` under `.pio/libdeps/`, `managed_components/` or `components/` — e.g. `infinitechris/esPod`, `jedld/slam_burger`, `myendless1/stack-chan`, `MarkRanton1917/rForth-M5Cardputer`, `scsagentclub/WorldCupLive_ESP`, `Notorious-Squirrel/NS-DOS`, `popolony2k/maritaca-e88-controller`, `kirikak2/midori`, `mdodkins/soledex`. They match `board_M5PaperMono` because the library defines it, not because they use it. **These inflate every GitHub code-search count for this device** |

### 4.7 The useful negative example

[`hawkymisc/buddy-watch`](https://github.com/hawkymisc/buddy-watch) (NOASSERTION, head
`b28c7d06b5c0a39651dcf837c8b2192c6984b2d8`) is a **M5StopWatch** project, not a PaperMono
project — and that is exactly why it matters. Its
[`docs/LAUNCHER.md`](https://github.com/hawkymisc/buddy-watch/blob/main/docs/LAUNCHER.md)
documents an infinite recursion in
`Panel_SSD1677_4Gray::display → IPanel::endWrite → display`, diagnosed as **M5GFX
misidentifying a StopWatch as a PaperMono**: the two boards share the I²C detect block
(RX8130 `0x32`, BMI270 `0x68`), so when the StopWatch's CST820 touch controller fails to
answer, M5GFX falls through to `board_M5PaperMono` and instantiates an SSD1677 panel that
is not there. The recorded root cause is that **M5IOE1 P4 (TP_RST) stayed LOW across an ESP
reset** (observed `ioe1_out_l=0xB5`, bit 3 clear) — because the IOE1 and PM1 retain state
independently of the ESP32-S3.

This is a genuine, reproducible-in-principle pitfall for PaperMono work too: the same
autodetect path, the same latching expander. See
[`features/io-expander.md`](features/io-expander.md) and
[`features/epaper-display.md`](features/epaper-display.md).

---

## 5. Rejected: false positives and adjacent work

Recorded because a future pass will hit the same search results.

| Item | Why rejected |
|---|---|
| [`namelessmucguy/PaperMono`](https://github.com/namelessmucguy/PaperMono) (created 2026-09-01) | **Named for the device, contains none of it.** `app/main/app_main.c` is Espressif's stock `hello_world` example verbatim (CC0 header intact); `app/sdkconfig` even sets `CONFIG_ESPTOOLPY_FLASHSIZE_2MB` — wrong for a 16 MB board. A placeholder, not a project |
| `harshalpawar/PaperMono-Nerd-Font`, `paper-design/paper-mono`, `Homebrew/homebrew-cask` `font-paper-mono.rb`, `internet-development/www-sacred`, `cosscom/coss`, `rpamis/comet`, `pexllecn/pexllecn`, `tlap9/multiclonage`, `rutopio/mahjong-font` | **A typeface also called "Paper Mono".** Responsible for a large share of the 1,274 `papermono` code-search hits |
| `PaperMonoid/PaperMonoid` | Username collision, 2023 |
| [`esphome/esphome`](https://github.com/esphome/esphome) | **Identifier collision.** `epaper_spi`'s C++ class for monochrome panels is called `EPaperMono`; `models/ssd1677.py` exists because Seeed's reTerminal E1004 uses SSD1677. Upstream ESPHome has **no PaperMono board support** — `is:issue papermono repo:esphome/esphome` returns **0** |
| [`HenryBaby/TamaInk`](https://github.com/HenryBaby/TamaInk) | `verification/freeink-display-drivers/` includes a `papermono` row in a **compile-only** driver matrix. The README states plainly: *"X4 Pro and other devices are unsupported"* |
| [`canardleteer/sticky-rs`](https://github.com/canardleteer/sticky-rs) | Seeed reTerminal Sticky. Mentions PaperMono only inside a comparative catalogue of FreeInk/CrossPoint targets |
| [`Lakphy/eego-a4-template-firmware`](https://github.com/Lakphy/eego-a4-template-firmware), [`mohitagw15856/Inkkit`](https://github.com/mohitagw15856/Inkkit) | Carry `M5Pm1.h` inherited from the FreeInk lineage; neither defines `FREEINK_DEVICE_PAPERMONO` nor includes `PaperMonoBoard.h`. Different devices |
| `eszter007/matcha-reader`, `jpirnay/witchhunt-reader`, `aBER0724/crosspoint-reader-cjk`, `juicecultus/crosspoint-reader-papers3` | CrossPoint forks with **no papermono build env** at their current heads. `matcha-reader` PR #117 (2026-08-16, closed) proposed one; `crosspoint-reader-papers3` is the **PaperS3** port, a different board |
| `Tr2e/M5PaperMono-UserDemo` | Fork of the vendor demo, verified byte-identical to upstream |
| `78/xiaozhi-esp32`, `m5stack/m5stack-linux-dtoverlays`, `zephyrproject-rtos/zephyr`, `nanoframework/*`, `tuya/TuyaOpen`, `lshaf/unigeek`, `PFalko/m5stack-papercolor-esphome`, and the whole M5StopWatch cluster | Surfaced by `M5PM1`/`M5IOE1` searches. Those chips are shared with the StickS3, StopWatch, PaperColor and CoreP4. **A Zephyr `regulator_m5pm1.c` driver exists** — relevant to the chip, not to this board |
| `koosoli/ESPHomeDesigner` copies in `DrBlokmeister/HASS_NUC` | A user's Home Assistant config directory containing the add-on |

---

## 6. Community venues and what their evidence is worth

### 6.1 M5Burner — the community firmware listing

The full catalogue was enumerated on 2026-09-02 via `https://burner.m5stack.com/api/v1/firmwares`
with `pageNum`/`pageSize` paging: **2,373 firmwares total, of which exactly 4 are PaperMono**.
This is a complete census of that venue, not a sample.

| Firmware | id | Source type | Uploader | Uploaded | Downloads | Declared source |
|---|---|---|---|---|---|---|
| `PaperMono UserDemo` v1.2 | `2089640807996628993` | OFFICIAL | m5stack (userId 1) | 2026-08-18 | 18 | — |
| `UIFlow2.0 PaperMono` v2.5.2 | `2089633464953118721` | OFFICIAL | m5stack | 2026-08-18 (v2.5.2 2026-08-28) | 3 | — |
| `CrossPoint-PaperMono-CJK` 1.5.0-RC | `2091144466157694978` | **COMMUNITY** | **IAMLIUBO** (userId 3966, <https://github.com/imliubo>) | 2026-08-22 | 27 | `https://github.com/MarsTechHAN/crosspoint-reader-mono` |
| `PaperMono Launcher` v0.1.0 | `2094259851119865857` | **COMMUNITY** | **MingRZou** (userId 256310) | 2026-08-31 | 1 | `https://github.com/MingRZou/PaperMono-Launcher` |

M5Burner's device registry contains **both** a legacy `Paper` device (`1897100000000000013`)
and a distinct `PaperMono` device (`2093000000000000020`); only the Launcher uses the latter,
which is why a naive device-filtered query misses three of the four.

> **Do not read those download counts as popularity.** 27 downloads of the top community
> build eleven days after launch is consistent with a product that was purchasable for nine
> minutes. It is a measure of unit scarcity, not of interest.

### 6.2 M5Stack forum and Discord

`community.m5stack.com` remains **auth-walled and unusable**: `/api/search?term=papermono`
returns HTTP 401 *"A valid login session was not found"* (re-checked 2026-09-02).
`/api/recent` is open and returned 20 topics with **zero** PaperMono topics in the window.
**No determination is possible** about forum activity — this is an inaccessible source, not
a negative result.

The M5Stack Discord was not searchable by any unauthenticated method available to this pass.
Recorded as an unexamined venue.

### 6.3 Reddit

Reddit tokenises the two spellings differently, so both were searched in every subreddit.

| Query | Result (2026-09-02) |
|---|---|
| sitewide `papermono` | 3 threads: two automated HN mirrors (r/hackernews, r/hypeurls) + **one new**: [r/xteinkereader "M5Stack PaperMono"](https://old.reddit.com/r/xteinkereader/comments/1w472fk/m5stack_papermono/) |
| sitewide `"paper mono" m5stack` | 5 threads: the above plus the two r/M5Stack threads already recorded |
| r/M5Stack `papermono` / `paper mono` | Still only [`1vquxa5`](https://old.reddit.com/r/M5Stack/comments/1vquxa5/paper_mono_coming_august_21st/) and [`1vuaneb`](https://old.reddit.com/r/M5Stack/comments/1vuaneb/check_out_whats_new_this_week/) |
| r/eink, r/CrossPointReader | 0 relevant |

**The new thread matters.** [r/xteinkereader `1w472fk`](https://old.reddit.com/r/xteinkereader/comments/1w472fk/m5stack_papermono/)
(u/arghya1988, 2026-09-01 09:39 UTC, 8 points, 9 comments) drew a reply from
**u/WolfieLee90**, who wrote: *"I managed to pick one up when they opened orders and received
it yesterday. I got the Lite model that does not have LoRa and NFC. I will be flashing it with
Crosspoi[nt]"* — and then, on 2026-09-02, posted **two further photographs: CrossPoint running
with the frontlight on, and a side-by-side comparison against an Xteink X4.** Evidence type
`O` (firsthand ownership) with images.

This is **the first independent end-user evidence of third-party firmware on retail PaperMono
hardware** found anywhere. It is a forum photo, not a measurement: no timings, no current
draw, no battery figures.

Also on that thread, u/mba2016kid gives a correct availability summary ("sold out the initial
batch and won't have more for a couple months") and an opinion on build quality; and
u/arghya1988's premise contains **the same $55/NFC/LoRa conflation Liliputing published** —
$55 is the Lite, which has neither. See
[`README.md`](README.md#community-editorial-and-project-coverage).

### 6.4 Video

Re-checked on YouTube 2026-09-02 (`M5Stack PaperMono`, `PaperMono`, sorted by upload date).
**No new PaperMono project video exists.** The population is unchanged since the previous pass:

| Video | Channel | Published | Views 2026-09-02 (2026-09-01) | Evidence |
|---|---|---|---|---|
| [M5Stack PaperMono: The Ultimate ESP32 Pocket Gadget?](https://youtu.be/sRlGOgX9KOA) | **Volos Projects** | 2026-08-29 | **72,122** (61,590) | `O + Op`. The only hands-on. **Description carries a vendor referral link (`?ref=kmjp2x8a`)** — a disclosed commercial relationship. Self-described first look, not a measurement review. Repeats "backlight" for what is a *frontlight* |
| [New Arrivals: PaperMono & PaperMono-Lite](https://youtu.be/0-qQ0y-WEek) | M5Stack | 2026-08-21 | 18,101 (16,938) | `V` |
| [Super Cool products! Let's unboxing!](https://youtu.be/gX4cTpS2gUA) | IAMLIUBO | 2026-08-25 | 173 (145) | `O`. Note this is **the same person who uploaded the CrossPoint CJK build to M5Burner** — an M5Stack-affiliated account, not an independent reviewer |

### 6.5 Written coverage

Unchanged and re-verified 2026-09-02: `hackaday.com/wp-json/wp/v2/search?search=papermono`
returns `[]`. `hackaday.io/search?term=papermono` now **302-redirects to a sign-in page** —
newly auth-walled, so no determination. `hackster.io/search?q=papermono` returns a JavaScript
shell with no server-rendered results. GitLab.com `/api/v4/projects?search=papermono` returns
an empty array (`/api/v4/search` requires auth). PlatformIO registry, npm and the Arduino
library registry contain **no PaperMono library** — the Arduino registry's only textual match,
`PDLS_EXT3_Basic_Fast`, is a Pervasive Displays "paper monochrome" library.

Every written article about this device still traces to
[one vendor blog post](https://shop.m5stack.com/blogs/news/m5stack-launches-papermono-a-compact-e-ink-development-terminal-for-connected-projects).

---

## 7. Prevalence, stated honestly

- **129 distinct repositories** were surfaced across 17 GitHub code queries, 4 repository
  queries and 4 issue/PR queries (raw counts in [`examples/search-log.md`](examples/search-log.md)).
- **48 repositories were inspected in detail** — metadata, default-branch head commit,
  licence file, README, and where relevant `platformio.ini`, board headers and commit logs.
- Of those 48: **9 are class D**, **13 class S**, **2 class V** (plus 4 M5Burner binaries),
  **4 class P**, **3 class C** (plus ~15 unnamed vendored copies), **1 useful negative**, and
  the remainder rejected.
- **M5Burner: 4 PaperMono firmwares out of a complete enumeration of 2,373.**
- **Reddit: 3 threads sitewide for `papermono`, 5 for `"paper mono" m5stack`.**
- **YouTube: 1 independent hands-on video, with a disclosed affiliate link.**

**No star count, download count or view count in this document should be read as evidence of
adoption.** The device was purchasable for approximately nine minutes on 2026-08-21 and has
been out of stock since. The largest third-party PaperMono repository has **4 stars**; the
frameworks that carry PaperMono targets have thousands, but those stars belong to the
frameworks. Nothing here was measured against a user population, because there effectively
is not one yet.

---

## 8. What this pass changes in the existing record

| Existing statement | Where | Correction (2026-09-02) |
|---|---|---|
| CrossPoint PaperMono support is *"roadmap, not shipped support"* | prior market sweep §4.3 | **Wrong.** Merged into `crosspoint-reader` `develop` on 2026-08-16 (PR #2983); three `papermono` build envs on the default branch; a shipped M5Burner binary since 2026-08-22. [§3](#3-crosspoint-the-source-repository-question-answered) |
| *"A GitHub code search of `bitbank2/bb_epaper` for 'PaperMono' returned 0 matches… Unresolved; do not cite `bb_epaper` support as fact"* | prior market sweep §4.3 | **Resolved: support exists.** The identifiers are `EPD_M5_PAPER_MONO` and `EPD_M5_PAPER_MONO_4GRAY`, with M5IOE1 power/reset sequencing in `src/bb_epaper.cpp`. The TRMNL half of the same claim also holds (`usetrmnl/trmnl-firmware/src/display.cpp`) |
| *"the community evidence base for PaperMono is currently four GitHub repositories and one YouTube video"* | prior market sweep §4.5; echoed in [`README.md`](README.md#community-editorial-and-project-coverage) | **Understated by roughly 5×.** 9 hardware-evidenced projects, 13 upstream targets, 2 vendor demos, 4 M5Burner binaries. The video count is correct |
| `EggUncle/PaperMonoCalendar` — *"ownership claimed not shown"* | prior market sweep §4.3 | **Partly superseded.** Preview images remain software-generated (the README still says so, commendably), but the README now states v2 sync and `HUB / SYNCED` are confirmed on a PaperMono, and v3 is flashed but not yet accepted |
| `hectorzin/…-ESPHome` — *"early WIP… labelled 'hipótesis de prueba'"* | prior market sweep §4.3 | **Superseded.** Now carries measured refresh timings, a specific IMU-interrupt route, light-sleep and PMIC-shutdown power policy. The rotation section is still honestly hedged |
| Third-party repository commit hashes were not captured | brief; prior `coverage.md` | **Fixed.** Every repository in [`examples/catalog.json`](examples/catalog.json) is pinned to a full 40-character default-branch head SHA retrieved 2026-09-02 |
| MicroPython / UIFlow2 support not recorded | absent from prior passes | **New.** `m5stack/uiflow-micropython` carries a complete `M5STACK_PaperMono` board plus `tests/display/test_papermono_startup.py`, shipped on M5Burner as v2.5.1/v2.5.2 |
| Earliest public trace of the product is the UserDemo repo, 2026-05-07 | [`README.md`](README.md) product history | **Earlier trace found.** `m5stack/m5stack-board-id` [PR #2](https://github.com/m5stack/m5stack-board-id/pull/2), *"Add papercolor, papermono and stopwatch"*, **2026-04-08** |
| Only two variants exist (C153, C153-LITE) | [`README.md`](README.md#identity-and-variants) | **An unexplained third name appears in vendor source.** `m5stack/M5GFX` `src/M5GFX.cpp` at `d91077b9a607b59404e4e4a49f775c792bfae382` contains, at line 1893, `0x50u, // NFC (for PaperMono Pro)` and at line 1899 `// no CST820, with NFC == PaperMono,PaperMono Pro`. **No "PaperMono Pro" SKU exists** on `shop.m5stack.com` (search suggest returns only PaperMono and PaperMono Lite), on `docs.m5stack.com` (`/en/core/PaperMono-Pro` → 404) or in the M5Burner device registry. Evidence class: **vendor source comment only.** Do not treat as a product |
| Display controller naming | [`features/epaper-display.md`](features/epaper-display.md) | The FreeInk/CrossPoint tree called the controller **SSD1683** in build comments until [crossmux PR #221](https://github.com/0x1abin/crossmux/pull/221) corrected it to SSD1677 on 2026-08-24. **Upstream `crosspoint-reader/crosspoint-reader`'s `platformio.ini` still says `SSD1683 800x480`** in the `[env:papermono]` header comment at head `e6139861`. A comment-only defect, but it will mislead a reader |
| microSD bus width | [`features/microsd.md`](features/microsd.md) | **Two upstream projects disagree.** `bmorcelli/Launcher` configures `-DSD_MMC_4BIT=1` with D0–D3 on GPIO 11/10/9/8; `Free-Ink/freeink-sdk` and `MarsTechHAN/crosspoint-reader-mono` describe **native 1-bit SDMMC**. Both are software choices on the same 4-bit-capable wiring, but a reader copying one into the other's stack will get a mount failure |
| Touch controller naming | [`features/touch.md`](features/touch.md) | GOROman's notes call it **FT5x06**, the vendor and everyone else call it **FT6336G**. `Free-Ink/freeink-sdk`'s README reconciles this explicitly: it handles "the **FT5x06 family** (Paper Mono's FT6336)". Not a conflict, a family name |

---

## 8b. CrossPlay — added 2026-09-02

[`ma-r-s/crossplay`](https://github.com/ma-r-s/crossplay) is a personal fork of
CrossPoint Reader (MIT, ★15, branch `xteink`, HEAD checked 2026-09-02) that adds
roughly 26 games and small tools alongside the reader. It is relevant here for
one concrete reason: **`platformio.ini` carries `papermono`,
`papermono-gh_release` and `papermono-gh_release_rc` build environments.**

Classification: **Class P — proposed or explicitly untested PaperMono support.**

> **Update 2026-09-11 — this remains correct for *upstream* CrossPlay, but a
> dedicated port now exists.** `fperuzzo72/crossplay-papermono` was created and
> pushed **2026-09-11**, MIT, on a branch named `papermono-bringup`, with commits
> that tune the render task stack to 16384 to match the X4 Pro, wire up release
> environments, and repoint the updater. That is hands-on bring-up, not a
> build-flag claim.
>
> **Nobody has yet reported it working on hardware**, so the port is recorded as
> its own entry rather than reclassifying upstream CrossPlay. Re-check this — a
> port that appeared *during* a research pass is a moving target.
The environments exist in the build configuration, but the fork's own
`LOCAL_SCOPE.md` describes only the Xteink X4 Pro and Seeed reTerminal Sticky as
its targets, and **no report of anyone running CrossPlay on a PaperMono was
found**. It is not Class D; nothing demonstrates it on this hardware.

Full record: [`software/applications/crossplay`](../../../software/applications/crossplay/README.md),
including a divergence analysis (2,391 ahead / 65 behind upstream, but −862
deletions — an overwhelmingly *additive* fork) and a seam-by-seam assessment of
which of its changes could be upstreamed as patches.

## 8c. `osprey74/Nostos` — Meshtastic reception — added 2026-09-11

Absent from every prior sweep, and the most technically ambitious third-party use
of this board's radio found so far.

| | |
|---|---|
| Repository | `osprey74/Nostos` @ `56acd5e` |
| Language | Rust |
| What it does | **Receives and decodes Meshtastic traffic** on the onboard SX1262 |

`crates/nostos-meshtastic` performs on-air header parsing, **AES-CTR decryption**
and **Position protobuf decoding**. It is a *custom receiver*, **not** a
Meshtastic firmware port — upstream `meshtastic/firmware` has no PaperMono
variant (see [`features/lora.md`](features/lora.md) §12).

Its radio configuration differs from the vendor demo in every parameter —
923.000 MHz / BW 125 kHz / SF9 / CR 4-5 / sync `0x3A` versus the factory
868.0 MHz / BW 62.5 kHz / SF12 / CR 4/8 / sync `0x34` — which makes it a useful
independent cross-check that the documented bring-up sequence is not
vendor-specific folklore.

It also independently corroborates the RGB LED wiring, with a comment stating in
Japanese that the LED is three independent lines and **not** a WS2812 — see
[`features/buttons-and-rgb-led.md`](features/buttons-and-rgb-led.md).

**Not run, not verified on hardware.** Classified by source reading only.

## 9. Cross-references

- Device overview and identity: [`README.md`](README.md)
- Per-feature guides, which these projects are the working examples for:
  [`features/README.md`](features/README.md) —
  [display](features/epaper-display.md) ·
  [frontlight](features/frontlight.md) ·
  [touch](features/touch.md) ·
  [LoRa](features/lora.md) ·
  [microSD](features/microsd.md) ·
  [I/O expander](features/io-expander.md) ·
  [power and sleep](features/power-and-sleep.md) ·
  [RTC](features/rtc.md) ·
  [IMU](features/imu.md)
- Capability-to-evidence matrix: [`coverage.md`](coverage.md)
- Contradictions ledger: [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
- Source classes and retrieval dates: [`sources.md`](sources.md)
- Machine-readable example catalogue: [`examples/catalog.json`](examples/catalog.json)
- Search method and stopping criterion: [`examples/search-log.md`](examples/search-log.md)
- Selected portfolio: [`examples/best.md`](examples/best.md)
