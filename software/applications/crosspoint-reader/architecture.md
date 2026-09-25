# CrossPoint Reader — architecture

**Repo:** `crosspoint-reader/crosspoint-reader` · **HEAD** `e6139861a2a8c634aa18c333b7e214ee51a9965c`
· **branch** `develop` · **license** MIT (`LICENSE`, "Copyright (c) 2025 Dave Allie")
· **research date** 2026-09-02.

Evidence labels: `executed-success` (I ran it), `inferred` (read from source), `not-tested`
(documented only). **No claim is hardware-verified.**

---

## 1. Top-level module map

```
crosspoint-reader/
├── platformio.ini          build definition: 15 envs, 14 SDK lib_deps, device flags
├── partitions.csv          16MB flash, dual-OTA
├── freeink-sdk/            git submodule → Free-Ink/freeink-sdk @ 68425f8e
├── src/
│   ├── main.cpp            (763 lines) setup() + loop(): the runtime
│   ├── CrossPointSettings  SETTINGS singleton — user preferences
│   ├── CrossPointState     APP_STATE singleton — session state
│   ├── activities/         screen-level controllers (the app)
│   │   ├── Activity.{h,cpp}, ActivityManager.{h,cpp}
│   │   ├── home/ reader/ settings/ network/ boot_sleep/ browser/ util/
│   │   └── plugins/        ← only on feature branches, not develop
│   ├── network/            web server (2912 lines), OTA, WebDAV, flasher
│   ├── components/         theming + shared UI widgets
│   └── platform/           USB Serial/JTAG handoff, efuse check skip
└── lib/                    25 in-tree libraries
    ├── hal/                (16 files) wrappers over freeink-sdk
    ├── Epub/               (69 files, 33,627 code) parser + layout + hyphenation
    ├── GfxRenderer/        (4,195 lines) 1-bit drawing + font cache
    ├── EpdFont/            font format + ~40 generated builtin font tables
    ├── expat miniz uzlib MiniBidi   vendored third-party
    └── I18n Txt Xtc ZipFile Utf8 KOReaderSync OpdsParser JsonParser …
```

Source of the layering: `docs/contributing/architecture.md:10-23` —
`Hardware → freeink-sdk → lib/hal wrappers → src/main.cpp runtime loop → Activities`.

**Size** (`tokei`, excluding `.git` and the submodule, `executed-success`):

| Language | Files | Code |
|---|---|---|
| C Header | 294 | 169,708 (mostly generated font/hyphenation tables) |
| C++ | 177 | 46,774 |
| C | 10 | 17,858 |
| Python | 26 | 7,934 (build scripts) |
| YAML | 34 | 14,277 (30+ i18n translation files) |
| **Total** | **620** | **264,683** |

Hand-written application C++ is ~47 k lines; the rest is generated data and vendored code.

---

## 2. Runtime: main loop and task structure

**Not** a heavy RTOS design. Arduino `setup()`/`loop()` on FreeRTOS, with **exactly one**
application-created task.

`src/main.cpp:343` `setup()` sequence — `BoardConfig::holdPowerRails()` (`:344`) →
optional serial (`:346-356`) → `HalSystem::begin()` (`:358`) → panic/silent-reboot
classification from `RTC_NOINIT` memory (`:361-368`) → SD storage → settings/state →
display + fonts → route to Home or resume Reader
(flow documented at `docs/contributing/architecture.md:27-46`).

`src/main.cpp:569` `loop()` per-iteration work:
1. `mappedInputManager.update()` (`:575`)
2. exclusive-storage short circuit while USB-MSC has handed the SD card to a host
   (`:577-591`) — no sleep/screenshot/navigation while the filesystem is detached
3. tilt-sensor page turn (`:593`)
4. run active activity, auto-sleep policy, adaptive CPU frequency
   (`:625`, `:751-756` `powerManager.setPowerSaving()`)

**The one application task** — `src/activities/ActivityManager.cpp:38`:

```cpp
xTaskCreatePinnedToCore(&renderTaskTrampoline, "ActivityManagerRender",
                        8192,               // Stack size
                        this, 1, &renderTaskHandle,
                        renderTaskCore);    // core 1 when configNUM_CORES > 1, else 0
```

Comment (`:44`): *"Keep long renders/cover decodes off CPU 0's idle watchdog when
available."* On the single-core ESP32-C3 it is pinned to core 0; on dual-core S3 it moves to
core 1. Rendering is serialised by `renderingMutex` (`ActivityManager.h:71`,
`ActivityManager.cpp:403-421`).

Other FreeRTOS use is incidental: a binary semaphore for USB reset
(`src/platform/UsbSerialJtagHandoff.cpp:67`), a power-mode mutex
(`lib/hal/HalPowerManager.cpp:30`), and `vTaskDelay(1)` yields in long parsing loops
(`lib/Xtc/Xtc.cpp:20`, `lib/JpegToBmpConverter/JpegToBmpConverter.cpp:176`,
`src/activities/reader/TxtReaderActivity.cpp:113`).

### Activity model

`src/activities/Activity.h` — `onEnter()` / `loop()` / `onExit()`, plus `skipLoopDelay()`
and `preventAutoSleep()` for long-running flows such as the web server
(`docs/contributing/architecture.md:48-63`). Groups: `home/`, `reader/`, `settings/`,
`network/`, `boot_sleep/`, `browser/`.

---

## 3. Display abstraction

Three layers, bottom-up:

1. **`freeink-sdk` `FreeInkDisplay`** — the facade; owns framebuffer + geometry, selects a
   `PanelDriver` at `begin()` (`freeink-sdk/README.md:67-73`). Drivers: `Ssd1677Driver`,
   `Uc8253X3Driver`, `Ed2208M5Driver`, `Uc8253MurphyDriver`, `PaperMonoDriver`,
   `LgfxEpdDriver`.
2. **`lib/hal/HalDisplay.{h,cpp}`** (268 lines) — CrossPoint's thin wrapper.
3. **`lib/GfxRenderer/`** (4,195 lines) — the actual drawing surface:
   `GfxRenderer.cpp` (2,360), `Bitmap.cpp` (295), `BitmapHelpers.cpp` (149),
   `FontCacheManager.cpp` (220). 1-bit framebuffer composition, text layout, bitmaps.

Framebuffer placement is an SDK build decision, not a CrossPoint one —
`freeink-sdk/README.md:373-387`: static DRAM `.bss` by default (largest panel 960×540 ≈
63 KB); `FREEINK_FB_PSRAM` auto-on for M5Paper and Paper Mono, which
`heap_caps_malloc(MALLOC_CAP_SPIRAM)` once in `begin()` with a DRAM fallback.

---

## 4. Storage and settings persistence

SD-card-first, via `lib/hal/HalStorage` over the SDK's `SDCardManager` (SdFat-over-SPI or
native SDMMC — `-DUSE_BLOCK_DEVICE_INTERFACE=1` on the S3 boards, `platformio.ini:264,
290, 368`).

On-card layout (`docs/contributing/architecture.md:143-158`):

```
/.crosspoint/
  epub_<hash>/
    book.bin           parsed metadata cache
    css_rules.cache
    progress.bin
    cover.bmp
    sections/*.bin     rendered pages + anchor/paragraph/list/offset lookup tables
    img_* cache files
  settings.json
  state.json
```

Two singletons: `SETTINGS` (`src/CrossPointSettings.h`) and `APP_STATE`
(`src/CrossPointState.h`). Binary cache formats are specified in `docs/file-formats.md`.

`sections/*.bin` carries a visible-text-offset table so reading positions are
**content-based**, not layout-based: "KOReader XPaths resolve to an exact chapter offset,
and the current layout derives the corresponding page" (`architecture.md:152-155`). This is
what lets typography changes not destroy sync position.

**Why SD-first:** `architecture.md:85-88` — RAM is the binding constraint; expensive parse
and layout results are persisted rather than recomputed.

---

## 5. EPUB / format pipeline

`lib/Epub/` — 69 files, 33,627 code lines, the largest subsystem.

Path (`architecture.md:65-88`, `:89-134`):

```
ReaderActivity → format dispatch (EPUB | XTC | TXT)
  EPUB → Epub::load
       → locate container + OPF
       → build or load BookMetadataCache (book.bin)
       → TOC + spine
       → CSS cache or parse manifest/base-dir CSS (css_rules.cache)
  EpubReaderActivity
       → section cache hit?  yes → read sections/<n>.bin
                             no  → parse chapter HTML, lay out text,
                                   apply typography + hyphenation, write cache
       → GfxRenderer draws current page
```

Supporting pieces: `lib/expat` (XML, vendored), `lib/ZipFile` + `lib/miniz`/`lib/uzlib`
(container), `lib/MiniBidi` (RTL), `lib/Utf8`, `lib/XmlParserUtils`,
`lib/Epub/Epub/hyphenation/` with generated tries (e.g. `generated/hyph-de.trie.h`,
12,908 lines). Other formats: `lib/Txt`, `lib/Xtc`.

Build flags relevant to parsing (`platformio.ini:32-40`): `-DXML_GE=0`,
`-DXML_CONTEXT_BYTES=1024` (expat hardening), `-DPNG_MAX_BUFFERED_PIXELS=16416`.

---

## 6. Fonts

- `lib/EpdFont/` — the glyph format plus ~40 **generated** builtin tables under
  `builtinFonts/` (Noto Sans/Serif and Ubuntu at 12/14/16/18 px × regular/bold/italic/
  bolditalic). Individually 3.7k–4.8k lines; collectively the bulk of the "C Header" LOC.
- `lib/GfxRenderer/FontCacheManager.cpp` (220 lines) — runtime glyph caching.
- `src/SdCardFontSystem.{h,cpp}` + `src/FontInstaller.{h,cpp}` — SD-loaded fonts with an
  on-device downloader and manager, incl. CJK. Documented in `docs/sd-card-fonts.md`;
  `ROADMAP.md:61-62` marks this "**Landed early**".
- `src/ReaderFontSizes.{h,cpp}`, `src/fontIds.h`.
- A separate release channel exists for font packs:
  `.github/workflows/release-fonts.yml`.

---

## 7. UI framework

CrossPoint predates FreeInkUI and does **not** use it for its own screens: it draws through
`GfxRenderer` with list/tab activity base classes —
`src/activities/UiListActivity.{h,cpp}`, `UiTabListActivity.{h,cpp}`,
`src/components/` (theming, `OptionPopup.h`, etc.).

`FreeInkUI` *is* in `lib_deps` (`platformio.ini:96`) but the SDK migration PR `ebebc6f2`
states plainly:

> right now the freeinkui and icons libraries are in the platform.io file but as they are
> not used anywhere, they won't be included in the final build.

**Conflict recorded:** the SDK ships a full UI toolkit (`freeink-sdk/README.md:404-616`,
with an LVGL parity table); CrossPoint links it but renders with its own stack. Whether
this has changed since June 2026 I did not exhaustively verify — `inferred`.

Localisation: `lib/I18n/` with 30+ YAML translations compiled by `scripts/gen_i18n.py`
into `I18nKeys.h` / `I18nStrings.{h,cpp}` (`architecture.md:187-191`).

---

## 8. Power management

- `lib/hal/HalPowerManager.{h,cpp}` over the SDK's `PowerManager` (per-SoC deep-sleep
  wake-on-power-button, `freeink-sdk/README.md:853`).
- Adaptive CPU frequency: `setPowerSaving(true/false)` toggled on user activity and
  inactivity (`src/main.cpp:582, 587, 625, 751, 756`).
- Deep sleep via `esp_deep_sleep_start` inside `enterDeepSleep` (`src/main.cpp:681, 699`).
- `BoardConfig::holdPowerRails()` first thing in `setup()` (`:344`); GPIO hold across sleep
  handled in `HalPowerManager.cpp:84`.
- Panic/watchdog capture persisted in `RTC_NOINIT` and dumped to SD on next boot
  (`src/main.cpp:359-368`), with `-Wl,--wrap=panic_print_backtrace,--wrap=panic_abort`
  (`platformio.ini:61`).
- Sleep-entry hooks feed the (unmerged) plugin event system's `sleep.enter`.

---

## 9. Build system — verified

**Toolchain** (`executed-success`):

| Component | Version |
|---|---|
| PlatformIO Core | 6.1.19 |
| Platform | pioarduino `platform-espressif32` **55.03.37** (`platformio.ini:10`) |
| Framework | Arduino (Arduino-ESP32 3.3.x / ESP-IDF 5.5.x per `freeink-sdk/platformio.sample.ini:14`) |
| Compiler | `xtensa-esp-elf-gcc (crosstool-NG esp-14.2.0_20251107) 14.2.0` |
| esptool | v5.3.1 |
| C++ standard | `-std=gnu++2a` (C++20), `-fno-exceptions` (`platformio.ini:35,62,64-66`) |

**Build executed** (`executed-success`):

```
$ export PLATFORMIO_CORE_DIR=/tmp/pio-core
$ pio run -e papermono
======================== [SUCCESS] Took 287.76 seconds ========================
papermono      SUCCESS   00:04:47.763
```

Result (`.pio/build/papermono/firmware.bin` = **5,364,128 bytes**):

| Metric | Value |
|---|---|
| Flash | 5,363,622 / 6,553,600 B — **81.8 %** |
| RAM (`.bss`+`.data`) | 106,028 / 327,680 B — 32.4 % |
| DIRAM total | 172,914 / 341,760 B — 50.6 % |
| **IRAM** | 16,384 / 16,384 B — **100.0 %** (`.text` 15,356 + `.vectors` 1,028) |
| RTC SLOW | 5,524 / 7,680 B — 71.9 % (`.rtc_noinit`) |
| Flash Code `.text` | 1,906,640 B |
| Flash Data `.rodata` | 3,327,668 B |

Two things stand out and are worth flagging as risk: **flash is 81.8 % full** and **IRAM is
completely exhausted**. `.rodata` at 3.3 MB — larger than the code — is the generated font
and hyphenation data, which is exactly what `ROADMAP.md:70-74` targets for eviction to SD.

**Attempted and NOT completed** (`not-tested` — do not read this as a failure of the code):

```
$ pio run -e default          # ESP32-C3, X3+X4
```

I started this for a C3-vs-S3 memory comparison and terminated it before completion. The
`default` env extends `[firmware_tuned]`, whose `custom_sdkconfig` forces a full rebuild of
the Arduino core on first build (`platformio.ini:113-120` — "slower once, cached after"), and
it had not finished. No `firmware.bin` was produced. **I therefore have no C3 size figures,
and no evidence either way about whether that env builds cleanly here.** The C3 numbers would
be the more interesting ones, since the C3 is the project's tightest target
(`SCOPE.md:25`) — treat this as an open gap.

**Host unit tests executed** (`executed-success`):

```
$ cmake -S test -B /tmp/cp-test-build -DCMAKE_BUILD_TYPE=Release && cmake --build … -j8
$ ctest --output-on-failure -j8
100% tests passed, 0 tests failed out of 173      (0.25 s)
```

GoogleTest v1.17.0 via `FetchContent` (`test/CMakeLists.txt:14-18`), C++20
(`test/CMakeLists.txt:4`). 19 test suites: `css_parser`, `hyphenation_eval`,
`minibidi_arabic`, `streaming_json_parser`, `utf8_compose`, `credential_integrity`,
`font_cache_manager`, `page_link`, `ligature_guard`, `combining_marks`, etc.

**Flash / partition layout** (`partitions.csv`) — 16 MB:

| Name | Type | Offset | Size |
|---|---|---|---|
| nvs | data/nvs | 0x9000 | 0x5000 |
| otadata | data/ota | 0xe000 | 0x2000 |
| **app0** | app/ota_0 | 0x10000 | 0x640000 (6.5 MB) |
| **app1** | app/ota_1 | 0x650000 | 0x640000 (6.5 MB) |
| spiffs | data/spiffs | 0xc90000 | 0x360000 |
| coredump | data/coredump | 0xFF0000 | 0x10000 |

Dual-OTA slots ⇒ a failed update can roll back.

**Build scripts** run pre/post (`platformio.ini:73-80`): `patch_pioarduino_cache.py`,
`patch_wolfssl.py`, `build_html.py`, `gen_i18n.py`, `git_branch.py`, `patch_jpegdec.py`,
`register_unit_tests_target.py`.

**Nix support** exists: `nix/{default,shell,flake}.nix`, `nix develop -f nix` or
`nix-shell nix` (`README.md:169-175`). I did **not** use it (`not-tested`) — I built with
the host's PlatformIO 6.1.19.

---

## 10. Dependencies

**Vendored in-tree** (no version pin, copied source): `lib/expat` (24 files),
`lib/miniz` (7), `lib/uzlib` (7), `lib/MiniBidi` (6), plus `lib/InflateReader`,
`lib/JsonParser`, `lib/Serialization`, `lib/Utf8`.

**Fetched by PlatformIO, pinned** (`platformio.ini:98-103`):

| Library | Pin |
|---|---|
| `bblanchon/ArduinoJson` | `7.4.2` |
| `ricmoo/QRCode` | `0.0.1` |
| `bitbank2/PNGdec` | `1.1.6` |
| `bitbank2/JPEGDEC` | git `#86282979224c8a32fd51e091ed5a35b0c699a52b` |
| `links2004/WebSockets` | `2.7.3` |
| `wolfssl/Arduino-wolfSSL` | `5.7.2` |

Plus the 14 `symlink://freeink-sdk/...` libraries (see [dependency and lineage](../../ecosystems/crosspoint-freeink/dependency-and-lineage.md) §2).
`lib_ignore = BLE` (`:105-106`).

wolfSSL is heavily tuned for heap: `-DWOLFSSL_HAVE_SP_ECC`, `-DWOLFSSL_SP_SMALL`
(`platformio.ini:52-53`), with a long comment (`:46-51`) explaining that without
single-precision ECC, P-256 operations OOM at the ~50 KB free heap a reading session
leaves.

---

## 11. Device support

Device selection is entirely via SDK compile-time flags. Envs in `platformio.ini`:

| Env(s) | Device | MCU | Flag |
|---|---|---|---|
| `default`, `gh_release`, `gh_release_rc`, `slim` | Xteink X4 **and** X3 (one binary, runtime-detected) | ESP32-C3 | `FREEINK_DEVICE_X4=1 FREEINK_DEVICE_X3=1` |
| `sticky`, `sticky-gh_release`, `sticky-gh_release_rc` | Seeed Sticky, 3.97" 800×480 SSD1677 + GT911 | ESP32-S3 | `FREEINK_DEVICE_STICKY=1` |
| `x4pro`, `x4pro-gh_release`, `x4pro-gh_release_rc` | Xteink X4 Pro | ESP32-S3 | `FREEINK_DEVICE_X4PRO=1` |
| `x4c`, `x4c-gh_release` | Xteink X4 Classic | ESP32-S3 | `FREEINK_DEVICE_X4CLASSIC=1` |
| `papermono`, `papermono-gh_release`, `papermono-gh_release_rc` | **M5Stack Paper Mono** | ESP32-S3 | `FREEINK_DEVICE_PAPERMONO=1` |

**M5Stack PaperMono is already a first-class, CI-built, released target** — see
[porting a device](../../ecosystems/crosspoint-freeink/porting-a-device.md). It is in the CI matrix
(`.github/workflows/ci.yml:84-90`) and shipped in release `1.6.0rc` as
`papermono-1.6.0_beta_RC03.bin` (5,293,984 bytes).

**Conflict recorded:** `docs/contributing/architecture.md:3` still says *"CrossPoint is
firmware for the Xteink X4 … targeting the ESP32-C3 microcontroller."* That is stale — the
SDK supports 15 devices across C3/C61/S3/ESP32 and CrossPoint ships five device families.
`SCOPE.md:3,9` and `ROADMAP.md:28-43` reflect the current multi-device reality.

---

## 12. Governance, cadence, CI

- **Maintainership: genuinely community-distributed.** Last 200 commits on `develop`:
  **56 distinct authors**, top contributor 39 commits (19.5 %) — Uri Tauber 39,
  Justin Mitchell 37, Leopoldo Pla Sempere 14, Thiago Kenji Okada 10, Phạm Bình An 8,
  Julia 7 (`executed-success`, `git log -200 --format=%an | sort | uniq -c`). Span:
  2026-07-15 → 2026-09-01, i.e. ~200 commits in 7 weeks.
- **Governance is documented**: `GOVERNANCE.md` — "community-driven", "do-ocracy with
  guidance", public-by-default decisions, moderation contact `@daveallie`. Scope is
  actively enforced: `SCOPE.md:30-37` lists *Temporarily Closed Areas* and
  `ROADMAP.md:23-24` says "'But it was on the old roadmap' is not a valid argument for
  accepting a PR."
- **Branch strategy**: `develop` is default and the integration branch; `master` exists;
  25 remote branches, feature branches long-lived (the plugin branches are 26 and 64
  commits behind).
- **Release cadence** — roughly monthly, accelerating:
  `0.15.0` 2026-01-21 · `1.0.0` 2026-02-09 · `1.2.0` 2026-04-03 · `1.3.0` 2026-05-15 ·
  `1.4.0` 2026-06-24 · `v1.5.0` 2026-08-07 · `1.6.0rc` 2026-08-17 (prerelease, 4 assets).
  Version is declared at `platformio.ini:7` (`version = 1.5.0`).
- **CI**: `.github/workflows/` — `ci.yml` (matrix build of `default`, `sticky`, `x4pro`,
  `papermono` with size reporting, `:75-147`), `pr-formatting-check.yml`, `release.yml`,
  `release_candidate.yml`, `release-fonts.yml`. Static analysis via `pio check` with
  cppcheck (`platformio.ini:15-20`).
- **Throughput** (GitHub search API, `executed-success`, as of 2026-09-02):
  156 PRs merged since 2026-08-01; 175 PRs open; 316 issues open; 106 issues closed since
  2026-08-01. High-volume, healthy, with a real backlog.
- **OTA**: supported. `src/network/OtaUpdater.{h,cpp}` (231+38 lines) with error codes incl.
  `WRONG_DEVICE_ERROR` (`OtaUpdater.h:30`), `OtaBootSwitch`, `FirmwareFlasher`, and
  `FirmwareBoardTag.{h,cpp}` to stop cross-flashing the wrong device binary. Plus
  `SdFirmwareUpdateActivity` for SD-based updates.

---

## 13. Runtime requirements, performance, risks

**Established by the source/build:**

- **Flash 81.8 % used** on the S3 papermono build; C3 targets are tighter still. Flash
  headroom is the stated Phase 1 priority (`SCOPE.md:26`, `ROADMAP.md:35-36`).
- **IRAM 100 % used** — no headroom at all on this env.
- Heap is the real constraint: `platformio.ini:46-51` documents that a reading session
  leaves **~50 KB free heap**, which is why wolfSSL SP-ECC is mandatory. `firmware_tuned`
  reclaims ~32-37 KB by rebuilding the Arduino core with a trimmed sdkconfig
  (`:112-143`), including moving Wi-Fi hot paths out of IRAM (`CONFIG_ESP_WIFI_IRAM_OPT=n`,
  ~25-30 KB back on the C3, at the cost of Wi-Fi throughput).
- **PSRAM required** for `papermono`, `x4pro`, `x4c` (`-DBOARD_HAS_PSRAM`); the C3 targets
  have none.
- Task stacks were right-sized from measured high-water marks in July 2026
  (`platformio.ini:122-127`).
- E-ink refresh behaviour (ghosting, partial update) is delegated to the SDK's per-panel
  drivers and LUTs; CrossPoint tracks it as an open Phase 1 item (`ROADMAP.md:44`).
  I have **no** measured refresh or battery figures — `not-tested`, and none are stated
  numerically in the docs.

**Bricking risk:** mitigated but non-zero. Dual-OTA + `FirmwareBoardTag` + `WRONG_DEVICE_ERROR`
guard against flashing the wrong image. The repo nonetheless ships
`docs/fix-bricked-xteink.md` and `docs/images/spiflash/` recovery photos, so the failure
mode is real enough to document. The SDK provides `libs/hardware/RecoveryBoot`.

**Security:** the web server has **no authentication** — see
[firmware plugin internals](plugins/firmware-plugin-internals.md) §5. This is a property of
`develop` too, not just the plugin branches.
