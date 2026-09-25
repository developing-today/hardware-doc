# Compatibility and status — M5Stack PaperMono

> What is known to work, what is known to fail, and by which hardware and software
> version.
> Snapshot **2026-09-01**.

> ## ⚠ Almost everything here is `untested`
>
> **No PaperMono was in hand.** Nothing below was verified on a device by this research.
> Statuses come from vendor documentation, source read at cited `file:line`, parsed
> firmware binaries, and a small number of third-party reports — each labelled. The table
> is deliberately dominated by `untested`; that is the accurate picture, not an
> incomplete one.

Evidence labels: **official** (vendor states it) · **source** (read in vendor code) ·
**binary** (recovered from a shipped image) · **schematic** · **reported** (third party,
firsthand) · **inferred** · **absent** (searched for, not found).

## 1. Hardware revisions

| Rev | Date | Evidence | Compatibility impact |
|---|---|---|---|
| **V0.6.2** | file dated **2026-05-22**, PDF exported 2026-06-08, last modified 2026-07-28 | schematic filename and title blocks | **The only revision in evidence** |
| KEY/RGB sub-board | 2026-04-14 | title block | — |
| NFC sub-board **V0.2** | 2026-07-28 | title block, marked **sheet 2/2** | Sheet 1 unpublished |

**There is exactly one hardware revision**, and the FCC filing confirms it
(`Multiple Model(s) No.: N/A`). No regional variants were found.

> **Corrected 2026-09-20.** This section previously concluded that **no
> FCC/CE/TELEC identifier exists**, on the strength of `/en/certification`
> returning zero matches for `PaperMono` and `C153`. The zero matches are real;
> the conclusion was wrong. The board holds **FCC ID `2AN3WM5PAPERMONO`**
> (granted 2026-08-12) and carries a Japanese MIC number `Ⓡ 211-260514` on its
> label artwork. See [`certification.md`](certification.md).
>
> Two things that belong in a compatibility record specifically:
>
> - **Wi-Fi and BLE cannot transmit simultaneously** — declared in the SAR report
>   (p. 29) as a not-simultaneous transmitter combination. `official-claim`.
> - **`certification.md` §10 opens a new conflict, C26**: the FCC label exhibit
>   says the microSD power rail is enabled by `IOE_G13`; the schematic says
>   `PYG14`. Treat both pins as unsafe to repurpose until someone probes it.
>   `untested`.

**As-built hardware identifiers** recovered from the FCC internal photographs
(2026-09-20), which are the first physical-hardware evidence in this record:

| Item | Value | Status |
|---|---|---|
| Main PCB silkscreen | **`V0.6`**, date code `251222` (2025-12-22) | read from photograph |
| Hardware / software version, as filed with the FCC | `V1.0` / `V1.0` | **conflicts with the V0.6 silkscreen** |
| NFC FPC | rev **`V0.2`** | matches the schematic's NFC sheet |
| LoRa antenna FPC | **`Paper Mono V3.0`** | matches the `RSY-E8131` antenna spec's own V3.0 |
| EUT serial tested | `3MFY-1` | SAR report p. 5 |

## 2. SKU variants

| SKU | Price (2026-09-01) | NFC | LoRa | Case | Weight |
|---|---|:-:|:-:|---|---|
| **C153** PaperMono | USD 65.00 | ✅ ST25R3916 | ✅ Stamp LoRa-1262 | Grey | 74.7 g |
| **C153-LITE** PaperMono-Lite | USD 55.00 | ❌ | ❌ | White | 72.4 g |

Everything else is identical, **including the 1150 mAh battery** — the Lite does not get a
smaller cell. The USD 10 delta is entirely NFC + LoRa.

| Compatibility fact | Status |
|---|---|
| One firmware image serves both | **official** — the M5Burner API description is literally `"PaperMono / PaperMono-Lite UserDemo"` |
| M5GFX **cannot** distinguish them | **source** — both map to `board_M5PaperMono`; NFC is masked out of the detection test (`M5GFX.cpp:1945`) |
| The application layer **can** | **source** — `hal_board.cpp:160–172` writes M5IOE1 `IO4` and reads NFC register `0x7F` expecting `0x05` |
| SKU case differs between vendor systems | `C153-Lite` in the docs, `C153-LITE` on Shopify |
| ⚠ Store handles say `800x480`; every docs page says `480x800` | **official**, both — marketing landscape vs driver portrait |

## 3. Software stack support

| Stack | Version | Board | Display | Touch | Power | LoRa | NFC | Status |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| **ESP-IDF** | **5.5.1** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **source** — both vendor projects' `dependencies.lock` |
| **arduino-esp32** | **3.3.10** (managed component) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **source** — same lock file |
| **M5Unified** | **0.2.21** | ✅ | ✅ | ✅ | ✅ | — | — | **source** — `board_M5PaperMono` present in the release tag |
| **M5GFX** | **0.2.28** | ✅ | ✅ | ✅ | — | — | — | **source** — idem |
| M5PM1 | **1.0.7** | — | — | — | ✅ | — | — | **official** registry `m5stack/m5pm1` |
| M5IOE1 | **1.0.9** | — | — | — | ✅ | ✅ | ✅ | **official** registry `m5stack/m5ioe1` |
| RadioLib | **7.2.1** pinned (`b91c6af1…`), **patched** | — | — | — | — | ✅ | — | **source** — `repos.json` |
| M5Unit-NFC | **0.1.0** (`93745b54…`), patched | — | — | — | — | — | ✅ | **source** |
| M5UnitUnified | **0.5.5** (`bf711f37…`), patched | — | — | — | — | — | ✅ | **source** |
| PlatformIO | `espressif32@6.12.0`, `board = esp32-s3-devkitm-1` | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | **official** — but **no dedicated PlatformIO board definition exists** |
| Arduino IDE | M5Stack board package, board **`M5PaperMono`** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **official** + **binary** (`[Autodetect] board_M5PaperMono`) |
| arduino-esp32 core variant | `3.3.9/variants/m5stack_papermono/pins_arduino.h` | ✅ | — | — | — | — | — | **reported** via `tanakamasayuki/M5Stack-Arduino-Check` |
| **UiFlow2** | **unspecified** | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | ⚠ | **official but empty** — no firmware version, no block list, no limitations published |
| ESPHome | — | ⚠ | ⚠ | ⚠ | ⚠ | — | — | **reported**, early WIP; the author labels the display/touch rotation section a *test hypothesis* |
| MicroPython / CircuitPython / Zephyr / NuttX / Rust | — | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **absent** — nothing located |

### 3.1 ⚠ Version-specific report: the `#develop` requirement is stale

The vendor's PlatformIO snippet pins
`M5Unified = https://github.com/m5stack/M5Unified#develop`.

**Verified `executed-success` on 2026-09-01:**

- `board_M5PaperMono = 29` is **byte-identical** on `master` and `develop`
  (`M5GFX/src/lgfx/boards.hpp:40`).
- `LED_PaperMono_Class.cpp` / `.hpp` are **byte-identical** between branches.
- `board_M5PaperMono` **is present in release tags M5Unified 0.2.21 and M5GFX 0.2.28**,
  both on `master`.
- The `master`↔`develop` deltas touching PaperMono are unrelated fixes, not board support.

**Caveat, preserved deliberately:** this is true *as of the branch SHAs recorded on
2026-09-01*. The docs may have been accurate when written — the M5GFX board-id commit
`3c2552d9` is dated 2026-04-10 and the M5Unified one `09a1c135` 2026-07-16.

### 3.2 ⚠ Version-specific report: the factory firmware is not built from released libraries

`repos.json` pins M5GFX and M5Unified to `develop` **at commits older than either current
branch head**:

| Component | Pinned commit | Current `develop` head (2026-09-01) |
|---|---|---|
| M5GFX | `02107b828acb3eb782fccd747863638d64c876d7` | `8d6e8b3e0e9629e0bf0702d263e9263b588b6075` |
| M5Unified | `2fe93c0c64f12f916e73a0605c86bf1241c06a6b` | `98c81b182f10760fe5313c31982cf975dfd73bda` |

So **the shipped factory firmware was built against a different e-paper waveform table
than either current branch.** Anyone comparing display behaviour against a factory device
is not comparing like with like. `inferred` from the pinned SHAs vs current heads.

Compounding it: the shipped image's `esp_app_desc_t` reports **`c78f6c5-dirty`** — built
from an uncommitted tree, therefore **not reproducible from any published commit**.

### 3.3 ⚠ Version-specific report: M5GFX has replaced the waveform LUTs

`diff` of `src/lgfx/v1/panel/Panel_SSD1677.cpp` between `master` and `develop`,
114 changed lines, `executed-success`:

- **`lut_quality` wholly replaced** on `develop`, with the previous 17-line table **left
  commented out in-tree**. The frame-rate row changed from `0x22 × 5` to `0xFF × 5` and
  all four grayscale rows differ.
- **`lut_text` replaced**, its comment rewritten from *"Text: 64-frame absolute four-gray
  waveform for Mode 1"* to *"GC1 binary full-refresh waveform used by epd_text"*, and a
  new `Panel_SSD1677_4Gray::_refresh_mode1_text()` path added, with `epd_text` dispatch
  switched to it.
- That new path **ignores its first parameter** (`(void)planeL;`), forcing the "old plane"
  to zero rather than using the previous frame, with a comment explaining it is deliberate
  ("Match the source binary text test") — which reads like a test scaffold promoted into
  production. `inferred`.

**Consequence:** the vendor's published refresh timings (4.71 / 0.45 / 0.34 / 0.07 s)
correspond to some specific unnamed build and **must not be treated as characteristic of
any version you can check out**. `inferred`.

## 4. Known-failing, hazardous and problematic

### 4.1 Vendor states its own e-paper waveforms are unstable — **official**

> "The e-paper driver waveforms for PaperMono in the M5GFX library are **currently
> unstable**. It is recommended to prioritize the e-paper manufacturer's OTP example below
> for refresh configuration to achieve better panel life and refresh stability."

Corroborated in-tree by §3.3. **Status: unresolved, live issue.** Mitigation: use
[`M5PaperMono-OTP-Demo`](https://github.com/m5stack/M5PaperMono-OTP-Demo).

### 4.2 Continuous partial refresh causes irreversible panel damage — **official**

M5Stack: *"Avoid uninterrupted continuous partial fast refreshes, to prevent long-term DC
imbalance from causing irreversible damage to the panel."* Do roughly one full refresh per
ten partials. **This is the only destructive failure mode on the board reachable from
ordinary application code.**

Related, and **recoverable**: after prolonged repeated refreshing, black deposited pixels
may appear from ink-particle physics. Leave the panel idle, then do one full refresh.

### 4.3 M5GFX drives the panel above its rated clock — **schematic + official datasheets**

40 MHz in M5GFX vs a **20 MHz** maximum in both the SSD1677 datasheet §12.1 and the DKE
panel manual p. 16, and 20 MHz in the vendor's own OTP demo. **Unresolved, untested, and
the first thing to measure** if you are chasing refresh artefacts.

### 4.4 Blank screen without octal PSRAM — **source**

`M5GFX.cpp:2025`/`:2030` log `"M5PaperMono need OPI-PSRAM enabled"`, reset the panel and
touch objects, and continue. The board is **correctly identified** with a completely dark
screen — and `CORE_DEBUG_LEVEL=0` in the vendor's own published build flags compiles the
log line out. **A build misconfiguration that presents as dead hardware.**

### 4.5 IP2315 bus interference at low battery — **official**

*"if the VBAT voltage is too low, the IP2315 may not initialize into I2C mode properly,
which can interfere with other devices on the same I2C bus."* Documented recovery: a short
press of the power button. Mitigation is structural in M5Unified — gate on, 64-attempt
scan, transact, gate off.

### 4.6 The `PYG3` collision can silently cut panel power — **schematic**

`PYG3` is an M5PM1 **net** (frontlight PWM) and an M5IOE1 **pin** (e-paper rail enable).
Both are live; a mistake is silent, not inert. Compounded by `M5IOE1_PIN_3 = 2`.
See [`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md).

### 4.7 Default single-click reset is disruptive — **reported ×2**

Two independent third-party projects — `MagicCube/free-ink-on-paper-mono` (which describes
itself as having a *complete verified hardware path* on a **C153-LITE**) and
`Free-Ink/freeink-sdk` — report explicitly **disabling the M5PM1's default single-click
reset** while preserving the long-hold download escape. `pm1.setSingleResetDisable(true)`.

**This is the strongest independent behavioural corroboration in the entire record**: two
projects, two authors, the same finding, one of them with photographic ownership evidence
cross-linked to a dated purchase post.

### 4.8 Vendor documentation contradictions — **official vs official**

| # | Contradiction | Resolution |
|---|---|---|
| C-1 | Docs use `PYG<n>` for **M5PM1** pins in ≥4 places, though `PYG` is also the M5IOE1's pin-name prefix | Both usages are accurate at different layers of the schematic. **The defect is ambiguity, not error** |
| C-2 | PaperMono page: frontlight via `PYG3_BL_PWM`; Lite page: via `G3_WAKEin` | **Both correct** — different layers of the same drawing, faithfully translated into all three languages |
| C-4 | Prose says the IMU interrupt is **active-high**; code, comments and the shipped binary say **active-low** | **Prose is wrong** |
| C-5 | Product + UiFlow2 pages say **power button** for download mode; Arduino page says **"reset button on the side"** | **No reset button exists.** Arduino page is wrong |
| C-7 | Arduino page requires `M5UnitUnified`; PlatformIO `lib_deps` omits it. Product pages pin `#develop`; Arduino page never mentions it | Install both; ignore the `#develop` pin (§3.1) |
| C-8 | PlatformIO sets `qio_opi`; both shipped binaries report **DIO** | **Not a defect** — hardware supports QIO; DIO is an IDF default because `sdkconfig.defaults` pins no flash mode |
| C-10 | "PaperMono Factory Reset Firmware" resolves to a record named "PaperMono UserDemo" | Same image, different label |
| C-11 | The IP2315 bus hazard and `M5IOE1_PIN_11` appear **only** on the product page, not on the dedicated power page | Coverage gap in the page most likely to be read |
| C-12 | PaperMono is absent from `/en/product_i2c_addr` **and** `/en/certification`, both HTTP 200 | Real omissions, verified negatives |

### 4.9 Documentation omissions found by reading the code — **source**

- **M5IOE1 `IO4` = NFC power enable** is used by the firmware and **never mentioned** in
  the docs' expander pin list.
- **M5IOE1 `IO7` = `ADD_SET`** likewise omitted.
- **USB (GPIO19/20) and UART0 (GPIO43/44)** are absent from every vendor pin table.
- Docs mention `G0_BOOT_OUT` and the M5IOE1 `G7` interrupt; **the UserDemo references
  neither**. Not contradicted — **unexercised**. A negative result.
- `M5GFX.cpp:2096`'s comment `// Set LOW io11, HIGH io13,14` is **wrong** — the mask covers
  P13/P14 only, and `bitOn` cannot set anything low.
- `Power_Class.cpp` says **"IP2316"** twice while the constant is `ip2315_i2c_addr`. Typo.

### 4.10 Third-party library support claimed but not found — **unresolved**

On 2026-08-17, four days *before* launch, `bitbank2` publicly claimed
*"I already support the Paper Mono and Paper Color in my `bb_epaper` library"*. A GitHub
code search of `bitbank2/bb_epaper` for `PaperMono` returned **0 matches** on 2026-09-01.
Support may be under a different identifier, in an unpushed branch, or may not have
landed. **Do not cite `bb_epaper` support as fact.**

## 5. Accessory and platform compatibility

| Item | Status | Note |
|---|---|---|
| **Any expansion accessory** | ❌ **impossible** | **No Grove port, no M-Bus, no header of any kind** |
| M5Stack HATs / Units | ❌ | Nothing to plug them into |
| PaperS3 firmware | ❌ **not drop-in** | `MingRZou/PaperMono-Launcher` is an explicit *port* of a PaperS3 project — concrete evidence the platforms differ. Larry Bank's public summary of the difference (PaperS3: parallel, 4.7", 960×540; PaperMono: SPI, 3.97", 800×480) was verified accurate |
| CrossPoint e-reader | ⚠ community image exists | `crosspoint-paper-mono-cjk-1.5.0-RC.bin`, third-party, repartitions the flash entirely. `crosspoint-reader` upstream lists PaperMono on its **roadmap only** |
| microSD cards | ⚠ **no documented limit** | No capacity or filesystem limit published by M5Stack |
| USB-C PD chargers | ❌ | **No PD.** 5 V only, OVP at 5.95 V |
| Meshtastic / MeshCore | ❌ unknown | Raised as an open question in the largest community thread and **not answered** |

## 6. Untested / unknown — the honest list

| Item | Why it matters |
|---|---|
| **Everything** | No device was available. This is the header row, not a footnote |
| Actual refresh times on any current library version | The four published figures are lab results for an unnamed build (§3.3) |
| **Current draw in any of the five power states** | The entire product pitch is low power, and **no figure exists from anyone** |
| Battery runtime under any workload | idem |
| Whether the 40 MHz panel clock causes the refresh instability | §4.3 — the single most valuable experiment |
| 4 grey levels vs 2 | M5Stack markets four; the DKE manual's optical table says `GN — 2Grey Level` |
| Which NFC card types actually read, and at what range | Four technologies advertised, **zero reports** |
| LoRa range, throughput, RF output, regional legality | No module datasheet, no certification, no report |
| Wi-Fi throughput, range, antenna | No antenna is documented anywhere |
| microSD throughput and capacity limits | No figure from anyone |
| Display + SD + Wi-Fi concurrently | No pin conflict; DMA/PSRAM/rail contention unmeasured |
| Whether GPIO3/45/46 strap exposure causes real boot failures | `inferred` hazard, unconfirmed |
| Whether the M5IOE1 GPIO7 interrupt works at all | **No vendor code exercises it** |
| Whether NFC/LoRa genuinely act as L2 wake sources | Sheet 1 says yes; no firmware demonstrates it |
| Whether the frontlight audibly whines at 5 kHz | Below the AW9967's rated 10–100 kHz range |
| M5IOE1 address `0x4F` vs its manual's `0x6F`–`0x76` | Unresolved |
| Restock date | Vendor said "two or three months" (2026-08-22); CNX-Software reported "next year". Both recorded, neither preferred |

## 7. Claims examined and rejected

| Claim | Source | Why rejected |
|---|---|---|
| Restock delayed by an e-ink driver IC shortage | widely repeated | The cited post and its **full reply chain** were retrieved; the reason **does not appear in them**. Hearsay |
| "$55 with NFC and LoRa" | Liliputing | $55 is the Lite, which has neither |
| PaperMono is the successor to / an upgrade over PaperS3 | several launch articles | Contradicted by the vendor's own specs: ~35 % fewer pixels, 4 vs 16 grey levels, 1150 vs 1800 mAh, no expansion port. A **repositioning**, not an upgrade |
| "Bluetooth 5.0 LE + Mesh" | CNX-Software | The publication's inference from the SoC; **not in M5Stack's specification table** |
| "Half the price of the XTEINK X4 Pro" | launch coverage | No X4 Pro price captured; a sealed reader vs a development board is not like-for-like |

## Related

- [`coverage.md`](coverage.md) · [`resources-and-conflicts.md`](resources-and-conflicts.md) · [`features/README.md`](features/README.md)
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — the full conflict register with resolutions
- [`README.md`](README.md) · [`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md)
