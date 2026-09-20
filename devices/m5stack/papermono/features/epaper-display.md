# E-paper display — M5Stack PaperMono

> **How do I draw on the screen, and how do I do it without damaging the panel?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

The single most important sentence on this page: **M5Stack says its own M5GFX waveforms
for this panel are unstable and recommends bypassing them.** Everything else follows
from that.

## 1. Capability summary and the hardware path

A 3.97-inch monochrome electrophoretic panel, 480 × 800 at 235 DPI, marketed as
4-level greyscale, with an integrated [frontlight](frontlight.md) and a
[capacitive touch layer](touch.md) on separate FPCs.

```
ESP32-S3  ──SPI2 (write-only)──▶  SSD1677 controller  ──▶  DKE DEPG0397BBS770F3 panel
   │                                    ▲
   │                                    │ RST  ◀── M5IOE1 IO5
   │                                    │ 3V3  ◀── M5IOE1 IO3  (EPD_3V3_L3B rail)
   └── GPIO18 BUSY ◀────────────────────┘
```

| Element | Part | Record |
|---|---|---|
| Panel | DKE `DEPG0397BBS770F3` (vendor demo says `DEPG0397BBS770F3HP-XM`) | [`components/dke/depg0397bbs770f3`](../../../../components/dke/depg0397bbs770f3/README.md) |
| Controller | Solomon Systech SSD1677, 4-wire SPI | [`components/solomon-systech/ssd1677`](../../../../components/solomon-systech/ssd1677/README.md) |
| Rail enable + reset | M5IOE1 `IO3` / `IO5` | [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md) · [`io-expander.md`](io-expander.md) |
| Panel 3.3 V LDO | `U5` SSP7615-33DFR, 400 mA | [`../power-architecture.md`](../power-architecture.md#rails-and-what-produces-them) |
| Host | ESP32-S3R8 | [`components/espressif/esp32-s3r8`](../../../../components/espressif/esp32-s3r8/README.md) |

**There is no MISO.** The link is write-only; the only status you get back is the
`BUSY` line on GPIO18.

## 2. Prerequisites and exact versions

| Item | Value | Why it matters |
|---|---|---|
| ESP-IDF | **5.5.1** | Both vendor projects' `dependencies.lock` |
| arduino-esp32 | **3.3.10** (managed component) | idem |
| M5Unified | **0.2.21** | `board_M5PaperMono` ships in this release tag |
| M5GFX | **0.2.28** | idem |
| PSRAM | **8 MB octal, `CONFIG_SPIRAM_MODE_OCT=y`** | **Mandatory.** See §7 |
| Flash | 16 MB, single `factory` app at `0x10000`, size `0xF00000` | No OTA slot |

PlatformIO, as published by M5Stack:

```ini
[env:m5stack-papermono]
platform = espressif32@6.12.0
board = esp32-s3-devkitm-1
framework = arduino
board_build.partitions = default_16MB.csv
board_upload.flash_size = 16MB
board_build.arduino.memory_type = qio_opi     ; <- QIO flash + OPI PSRAM. Not optional.
build_flags = -DESP32S3 -DBOARD_HAS_PSRAM -mfix-esp32-psram-cache-issue
              -DARDUINO_USB_CDC_ON_BOOT=1 -DARDUINO_USB_MODE=1
lib_deps =
    M5Unified = https://github.com/m5stack/M5Unified#develop
    M5PM1 = https://github.com/m5stack/M5PM1
    M5IOE1 = https://github.com/m5stack/M5IOE1
```

> **The `#develop` pin is stale.** `board_M5PaperMono` is byte-identical on `master` and
> `develop` and ships in released tags M5Unified 0.2.21 / M5GFX 0.2.28. Verified
> 2026-09-01; see [`../gaps-and-conflicts.md` R5](../gaps-and-conflicts.md#r5--m5unifieddevelop-requirement--resolved-the-instruction-is-stale).
> You may still want `develop` for unrelated behavioural fixes, but not for board support.

## 3. Resources consumed

| Resource | Value |
|---|---|
| SPI bus | **SPI2_HOST**, MOSI GPIO14, SCLK GPIO15, DC GPIO17, CS GPIO16, 3-wire mode, SPI mode 0 |
| Clock | **40 MHz write** in M5GFX; **20 MHz** in the vendor OTP demo — see §8 |
| Status line | GPIO18 `BUSY`, input only |
| Expander pins | `IO3` rail enable, `IO5` reset (both behind I²C `0x4F`) |
| Rail | `EPD_3V3_L3B`, part of power state **L3A/L3B** |
| PSRAM | M5GFX framebuffers; OTP demo allocates `3 × 48 000 = 144 000 B` with `MALLOC_CAP_SPIRAM` |
| Series resistor | 22 Ω on SCLK (`R38`) |

Panel RAM packing (OTP demo): MSB-first, **100 bytes per row × 480 rows**; in monochrome
RAM **1 = white, 0 = black**. Four-grey encoding across two planes is
`white=00, light=10, dark=01, black=11`.

## 4. Orientation — the axis trap

**The controller is addressed 800 × 480; the panel is natively 480 × 800 portrait.**

| Layer | Geometry |
|---|---|
| Vendor product page, spec table | `480 × 800` |
| Store title and URL handle | `800x480` |
| M5GFX panel config | `panel_width = 800`, `panel_height = 480`, **`offset_rotation = 3`** |
| Vendor OTP demo raw driver | works natively in `800 × 480`, RAM X = visible vertical |

Through M5GFX you see 480 × 800 and the rotation is done for you. **Anyone writing a raw
SSD1677 driver from the docs' `480 × 800` figure will get the axes transposed.**

## 5. Minimal procedure — M5GFX (`inferred`)

Derived from `M5GFX/src/M5GFX.cpp:2030–2146` and the vendor's own published sketch
shape. **Not run on hardware.**

```cpp
#include <M5Unified.h>

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);                       // brings up I²C, M5PM1, M5IOE1,
                                       // the EPD rail (IO3) and the panel reset (IO5)

  M5.Display.setEpdMode(epd_mode_t::epd_text);   // quality | text | fast | fastest
  M5.Display.setRotation(0);                     // 480 x 800 portrait as presented
  M5.Display.setTextDatum(middle_center);
  M5.Display.setFont(&fonts::FreeSansBold18pt7b);
  M5.Display.drawString("hello", M5.Display.width() / 2, M5.Display.height() / 2);
  M5.Display.display();                          // push
}

void loop() { M5.update(); }
```

`M5.begin()` performs the expander bring-up itself, in raw register writes rather than
through the M5IOE1 library — `M5GFX.cpp:2088–2096` sets `IO5`/`IO6` and `IO13`/`IO14` to
output, drives `IO3` high, sets those pins push-pull, then pulses `IO5`/`IO6` low for
8 ms to reset the panel and the touch controller together.

> One of those comments is wrong. `M5GFX.cpp:2096` reads
> `// Set LOW io11, HIGH io13,14` on a `bitOn` of register `0x06` with mask `0b00110000`
> — register `0x06` is `GPIO_OUT_H` covering P14–P9, so the mask is P13 and P14 only, and
> `bitOn` cannot set anything low. The code is right, the comment is not. Do not
> reverse-engineer the expander map from M5GFX comments.

### Refresh modes

| Mode | `epd_mode_t` | Vendor lab figure |
|---|---|---|
| Quality | `epd_quality = 1` | 4.71 s |
| Text | `epd_text = 2` | 0.45 s |
| Fast | `epd_fast = 3` | 0.34 s |
| Fastest | `epd_fastest = 4` | 0.07 s |

> ⚠ **These four numbers are vendor laboratory figures for a LUT set that may no longer
> be the shipped one.** M5GFX `develop` has *replaced* `lut_quality` and `lut_text`
> outright, leaving 17 lines of the previous `lut_quality` commented out in-tree, and
> added a new `_refresh_mode1_text()` code path. The factory firmware pins a M5GFX commit
> (`02107b82…`) older than either current branch. So the published timings correspond to
> some specific unnamed build and **should not be treated as characteristic of any
> version you can check out today**. Vendor claim, `not-tested`, and known to be
> version-sensitive.
>
> The same four numbers appear on the PaperMono-Lite page, whose own caption still says
> *"laboratory test results for **PaperMono**"* — they were copied, not separately
> measured.

## 6. Minimal procedure — the OTP path (`reported-working` as a vendor recommendation, `inferred` as code)

**This is what M5Stack tells you to use.** `M5PaperMono-OTP-Demo` bypasses M5GFX's panel
driver entirely, talks to the SSD1677 directly over SPI2 at 20 MHz, and **uploads no LUT
at all** — it uses only the controller's factory-programmed OTP waveforms. Verified by
enumerating all 24 `write_command`/`write_register` call sites: none is the SSD1677
LUT-write command `0x32`.

Reset, through the expander rather than an ESP32 pin
(`M5PaperMono-OTP-Demo/components/EDP_OTP_LUT_demo/src/EDP_SPI.cpp`):

```c
auto& ioe = M5.getIOExpander(0);
ioe.setHighImpedance(2, false);  ioe.setDirection(2, true);  ioe.digitalWrite(2, true);   // IO3: EPD 3V3
ioe.setHighImpedance(4, false);  ioe.setDirection(4, true);
ioe.digitalWrite(4, false);  vTaskDelay(pdMS_TO_TICKS(10));                                // IO5: EPD RST
ioe.digitalWrite(4, true);   vTaskDelay(pdMS_TO_TICKS(10));
```

Note the raw `2` and `4`: the demo bypasses the library enum on purpose, with the comment
`// M5IOE1 uses zero-based pin indexes.` See [`io-expander.md`](io-expander.md).

Controller init (`EDP_OTP_LUT_demo.cpp:206–224`, comments are M5Stack's):

```c
write_command(0x12);                                  // SOFT RESET
write_register(0x18, {0x80});                         // Internal temperature sensor
write_register(0x0C, {0xAE,0xC7,0xC3,0xC0,0x80});     // Booster soft-start
write_register(0x01, {0xDF,0x01,0x02});               // 480 gate outputs
write_register(0x3C, {0x01});                         // Border waveform
write_register(0x21, {0x00});                         // Normal RAM display mode
```

Four-grey init differs: data-entry mode `0x02` instead of `0x03`, plus
`write_register(0x1A, {0x5A})` — a forced "grey-mode temperature value" that selects the
OTP grayscale waveform bank instead of letting the internal sensor pick one. That reading
is `inferred` from the vendor comment and SSD1677 convention; it was not checked against
the datasheet.

Refresh triggers — the `0x22` Display Update Control value selects waveform and scope:

| Mode | `0x22` | Then |
|---|---|---|
| Partial refresh | `0xF8` | `0x20` Master Activation; border floated first with `0x3C = 0x80` |
| Partial, follow-up | `0x14` | `0x20` |
| Mono full refresh | `0xFF` | `0x21 = 0x00`, then `0x20` |
| Four-grey full refresh | `0xD7` | after `0x24` and `0x26` RAM writes, then `0x20` |

The demo issues `0x10 {0x01}` (deep sleep) after every refresh.

## 7. Octal PSRAM is mandatory — and the failure looks like dead hardware

`M5GFX.cpp:2025` / `:2030`:

```
E ... M5PaperMono need OPI-PSRAM enabled
```

If `CONFIG_ESP32S3_SPIRAM_SUPPORT` or `CONFIG_SPIRAM_MODE_OCT` is missing, M5GFX **still
identifies the board**, then resets the panel and touch objects and jumps to
`init_clear`. You get a correctly-detected board, a completely blank screen, and one log
line that is easy to miss at `CORE_DEBUG_LEVEL=0` — which is exactly what the vendor's
own PlatformIO snippet sets.

**Framework limit**, fixable in the build config: `board_build.arduino.memory_type = qio_opi`
(PlatformIO) or `CONFIG_SPIRAM=y` + `CONFIG_SPIRAM_MODE_OCT=y` (ESP-IDF).

## 8. Panel safety — the rules that are not optional

All four are M5Stack's own words, reproduced from the product page. `reported-working`
as guidance; the failure modes were not reproduced here.

1. **Avoid direct sunlight and prolonged sun exposure.** "High temperatures or strong UV
   can damage the panel." This is a **physics/board** limit, not a software one.
2. **Roughly one full refresh per ten partial fast refreshes**, to clear accumulated
   ghosting.
3. **Never run uninterrupted continuous partial fast refreshes.** M5Stack: long-term DC
   imbalance causes **irreversible damage**. This is the single destructive failure mode
   on the board, and it is reachable from ordinary application code — an animation loop
   is enough.
4. **If you upload custom waveforms, DC balance is your responsibility.** "Otherwise,
   irreversible damage may be caused to the panel." The OTP path exists precisely so you
   do not have to take that on.

A recoverable relative of (2), also from the vendor: after prolonged repeated refreshing,
black deposited pixels may appear from ink-particle physics. Leave the panel idle a
while, then do one full refresh.

## 9. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Silicon (SSD1677)** | 20 MHz maximum write clock (§12.1); 680 gate outputs — the board configures 480 |
| **Silicon (panel)** | Electrophoretic; image persists unpowered; DC imbalance is cumulative and irreversible |
| **Board** | Write-only SPI, no MISO. Panel rail and reset only reachable through I²C. 22 Ω on SCLK |
| **Framework (M5GFX)** | Drives 40 MHz — **above both the SSD1677 and DKE ratings**. Four LUT modes. `offset_rotation = 3` |
| **Framework (M5GFX)** | Aborts silently without OPI PSRAM (§7) |
| **Observed / reported** | Vendor states its own waveforms are "currently unstable"; corroborated in-tree by the `master`→`develop` LUT replacement |
| **Unresolved** | 4 grey levels (M5Stack) vs `GN — 2Grey Level` in the DKE manual's own optical table |

### The clock conflict, stated plainly

M5GFX writes at **40 MHz** (`M5GFX.cpp:2114`). The SSD1677 datasheet §12.1 **and** the DKE
panel manual p. 16 **independently** state a **20 MHz** maximum, and the vendor's own OTP
demo uses 20 MHz. This is a 2× overclock of a rated bus limit in the vendor's own
graphics library, in the same library the vendor says has refresh problems.

It is not proven to be the cause of anything. It is the **first thing worth measuring**
if you have hardware and are chasing refresh artefacts. Tracked as
[`../gaps-and-conflicts.md` C3](../gaps-and-conflicts.md#c3--spi-clock-exceeds-the-panels-rated-maximum).

## 10. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| Display + [touch](touch.md) | ✅ intended | Different buses. M5GFX resets both together on `IO5`/`IO6` |
| Display + [microSD](microsd.md) | ✅ no pin conflict | SDMMC is GPIO8–13, panel is GPIO14–18. Both draw from the L3B domain; both power enables are expander pins, so both need a working I²C bus |
| Display + [Wi-Fi](wifi-and-bluetooth.md) | ⚠ untested together | No pin conflict. A full refresh is seconds of SPI DMA alongside a radio duty cycle; no measurement exists |
| Display + [LoRa](lora.md) | ✅ separate SPI hosts | Panel on `SPI2_HOST`, LoRa on `SPI3_HOST` |
| Display + [frontlight](frontlight.md) | ✅ | Different chips entirely — panel rail on M5IOE1 `IO3`, frontlight PWM on M5PM1 `G3` |
| Display + deep sleep | ✅ by design | The image persists with the rail off. Turn the rail off *after* `BUSY` clears |
| **Writing "PYG3" to the expander expecting brightness** | ❌ **silent panel death** | You just cut `EPD_3V3_L3B`. Nothing reports an error. See [`../pin-naming-and-the-pyg-ambiguity.md`](../pin-naming-and-the-pyg-ambiguity.md) |

## 11. Debugging

| Symptom | Likely cause |
|---|---|
| Blank screen, board otherwise fine | **OPI PSRAM not enabled** (§7). Check the log at `CORE_DEBUG_LEVEL≥3` |
| Blank screen, no log line | `EPD_3V3_L3B` never enabled — the enable has a 1 MΩ pulldown and defaults **off** |
| Panel stops updating mid-session | Something wrote M5IOE1 `IO3` low. Nine times in ten this is the `PYG3` mix-up |
| `BUSY` never clears | Panel not out of reset (`IO5`), or the rail is off, or SPI is going nowhere (no MISO to tell you) |
| Ghosting builds up | You are past ~10 partial refreshes. Do a full one |
| Refresh looks wrong on one build, fine on another | Different M5GFX commit → different LUTs. Pin the commit |
| Axes transposed in a hand-written driver | 480 × 800 is the *rotated* view; the controller is 800 × 480 |

## 12. Alternatives and when to choose each

| Approach | Choose when | Cost |
|---|---|---|
| **M5GFX / `M5.Display`** | You want fonts, sprites, LVGL-adjacent conveniences and touch integration for free | The unstable-LUT warning; 40 MHz clock; needs OPI PSRAM |
| **Vendor OTP demo path** | You care about panel lifetime and refresh stability — **the vendor's own recommendation** | You write your own drawing layer. No fonts, no sprites |
| Third-party drivers (`bb_epaper`, ESPHome `SSD1677`) | Existing ecosystem integration | PaperMono support is **claimed but unverified**; see [`../compatibility-and-status.md`](../compatibility-and-status.md) |

## 13. Unresolved questions

- **How many of the panel's 34 waveform slots are OTP-programmed, and over what
  temperature span?** Unpublished. Outside the programmed range the failure is a silent
  no-refresh.
- **Is it really four grey levels?** The vendor demo implements a working four-grey mode;
  the panel manual's optical table says two. Unresolved.
- **`DEPG0397BBS770F3` vs `DEPG0397BBS770F3HP-XM`** — the suffix is undocumented.
- **DKE's mechanical drawing note 3 (`800 gate × 480 source`) is provably backwards** —
  800 gate lines would exceed the SSD1677's 680 gate outputs, and the firmware configures
  480 gates.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2** (SKU C153 and C153-LITE; the panel is identical on both) |
| Framework range | ESP-IDF 5.5.1 · arduino-esp32 3.3.10 · M5Unified 0.2.21 · M5GFX 0.2.28 |
| Evidence | Pin map and register sequences: **read from vendor source at cited `file:line`**. Safety rules: **`reported-working`** (vendor). Code sketches: **`inferred`**. Timings: **vendor lab figures, version-sensitive, `not-tested`** |
| Confidence | High on wiring and register sequences; **low on timing and refresh quality** |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md`](../pinouts-and-buses.md#spi-buses) · [`../power-architecture.md`](../power-architecture.md) · [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md)
- [`frontlight.md`](frontlight.md) · [`touch.md`](touch.md) · [`io-expander.md`](io-expander.md) · [`power-and-sleep.md`](power-and-sleep.md)
- [`components/dke/depg0397bbs770f3`](../../../../components/dke/depg0397bbs770f3/README.md) · [`components/solomon-systech/ssd1677`](../../../../components/solomon-systech/ssd1677/README.md)
- [`vendors/dke`](../../../../vendors/dke/README.md) — how the panel manual was obtained, and why `pdftotext` returns nothing
