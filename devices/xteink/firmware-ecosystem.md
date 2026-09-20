# Xteink firmware ecosystem — the hardware-side map

> **Which firmware runs on which Xteink board, and what a new board has to provide
> to be supported.** The [software tree](../../software/README.md) documents these
> projects as software; this page is the view from the hardware.
>
> Snapshot **2026-09-07**, from records dated 2026-09-01/04. **Nothing here was
> built, flashed or run.** Repository facts are `executed-success` on the read;
> everything about behaviour is `inferred` unless it cites a third party.

## Why this page exists

Four of the five Xteink products are ESP32 devices with **no vendor SDK, no vendor
board-support package and no vendor documentation of any kind**. Every development
path in this family is community-built, and the community converged on a single
stack. If you own one of these devices, the practical question is not "how do I
program it" — it is "which of these projects already knows about my board, and at
what commit".

The five products, and where each stands:

| Product | Platform | In the ecosystem? |
|---|---|---|
| [**X3**](x3/README.md) | ESP32-C3 | ✅ two board profiles (UC8253 and UC8279d) |
| [**X4**](x4/README.md) | ESP32-C3 | ✅ — **the device that created the ecosystem** |
| [**X4 Pro**](x4-pro/README.md) | ESP32-S3 | ✅ — **the design floor**, and the only target of the native-plugin fork |
| [**X4 Classic**](x4-classic/README.md) | ESP32-S3 | ✅ profile exists; the *product* is not sold internationally |
| [**S4**](s4/README.md) | **Android 11** | ❌ **and never will be.** Different architecture. No SoC is even identified |
| [**Nano / Tong Card**](nano/README.md) | **passive, NFC-powered** | ❌ Not a computer. No MCU at all |

⚠ One recurring community error worth killing here: an r/EDC carry post describes
an *"Xteink S4 e reader (running crosspoint)"*. **CrossPoint is ESP32 firmware and
cannot run on an Android device.** The [S4 record](s4/README.md) records three
possible explanations and endorses the mundane one — the owner mislabelled an X3 or
X4 — because the same corpus contains a post titled "Got my white (?) X5" whose
author later corrected it to "X4".

---

## 1. The stack

```
open-x4-epaper/community-sdk          MIT · CidVonHighwind et al.
        │ code derived, re-architected — SSD1677 and UC8253 init sequences and LUTs
        ▼
Free-Ink/freeink-sdk                  MIT · ★248 · 95 forks · created 2026-06-03
        │  ← panel drivers, board profiles, capability gates, device managers, FreeInkBook
        │  git submodule (branch-pinned in .gitmodules; the SHA is in the gitlink)
        ▼
crosspoint-reader/crosspoint-reader   MIT · ★7,538 · 1,621 forks · created 2025-12-03
        ├── uxjulia/CrossInk                    ★~1,451   X3 · X4 · Sticky
        ├── ma-r-s/crossplay                    ★~17      C3 · Sticky · X4 Pro · PaperMono
        ├── mekhontsev/crosspoint-reader        —         X4 Pro only — native plugin host
        ├── MarsTechHAN/crosspoint-reader-mono  ★1        PaperMono port
        └── ~9 further named derivatives, most of them detached re-uploads
```

**Note the inversion at the top: CrossPoint predates its own SDK by six months.**
FreeInk is a later re-architecture of the SDK CrossPoint was already using, not an
upstream that CrossPoint adopted from outside. Anyone reading the star counts
(7,538 vs 248) as "big project depends on small project it found" has the history
backwards. Full analysis:
[FreeInk SDK record](../../software/frameworks/freeink-sdk/README.md#lineage--and-why-the-freeink-came-first-reading-is-wrong).

**The FreeInk SDK board profile header is the single most authoritative hardware
document for four of these five devices.** Every board-level pin, address and chip
in this tree traces to it, to a parsed OEM flash image, to a teardown photograph,
to a vendor statement, or to a labelled community report. **Vendor marketing prose
is not used as evidence anywhere**, because the X3 listing advertises a frontlight
the device does not have.

---

## 2. Support matrix, by firmware

### 2.1 CrossPoint Reader — `crosspoint-reader/crosspoint-reader`, branch `develop`

MIT. Fifteen build environments across five device families, listed on `develop`
and retrieved **2026-09-04**.

| Env family | PlatformIO board | Device | SoC assumption |
|---|---|---|---|
| `default`, `gh_release`, `gh_release_rc`, **`slim`** | `esp32-c3-devkitm-1` | **Xteink X3 / X4 (C3-class)** | RISC-V, **no PSRAM** — *this env sets the project's memory ceiling* |
| `sticky`, `sticky-gh_release`, `sticky-gh_release_rc` | `esp32-s3-devkitc1-n16r8` | Seeed reTerminal Sticky | S3, 16 MB flash, 8 MB PSRAM |
| `x4pro`, `x4pro-gh_release`, `x4pro-gh_release_rc` | `esp32-s3-devkitc1-n16r8` | **Xteink X4 Pro** | idem |
| `x4c`, `x4c-gh_release` | `esp32-s3-devkitc1-n16r8` | **Xteink X4 Classic** | idem |
| `papermono`, `papermono-gh_release`, `papermono-gh_release_rc` | `esp32-s3-devkitc1-n16r8` | [**M5Stack PaperMono**](../m5stack/papermono/README.md) | idem, and the PaperMono has a **hard OPI-PSRAM requirement** |

Two things fall out of that table:

- **Every S3 target shares one board definition** — `esp32-s3-devkitc1-n16r8`,
  16 MB flash + 8 MB octal PSRAM. Four physically different products, one memory
  configuration.
- **PaperMono support is upstream, not a fork-only capability.** The
  7,500-star repository builds for a board M5Stack shipped in August 2026.

⚠ **No commit SHA is pinned in the software record.** Identity is by branch. Pin
`develop`'s HEAD before citing specific code. Likewise `.gitmodules` pins the
FreeInk SDK **by branch** (`main`); the actual revision lives in the gitlink, so
**a fork can behave differently from upstream without a single line of fork-owned
code differing**.

### 2.2 FreeInk SDK — `Free-Ink/freeink-sdk`, branch `main`

MIT. The Xteink records in this tree cite commit
**`24003795381a6c23630a26472ae3b06550333e71`**. Board profiles and their build
flags:

| Profile | Build flag | Device | Panel drivers auto-enabled |
|---|---|---|---|
| `XTEINK_X3` | `-DFREEINK_DEVICE_X3=1` | X3, UC8253 batches | links **both** X3 drivers |
| `XTEINK_X3_UC8279` | (same flag) | X3, UC8279d batches from ~2026-07 | idem |
| `XTEINK_X4` | `-DFREEINK_DEVICE_X4=1` | X4 | SSD1677 · UC8179 · UC8279 |
| `XTEINK_X4_PRO` | `-DFREEINK_DEVICE_X4PRO=1` | X4 Pro | SSD1677 · UC8179 · **+ `FREEINK_CAP_TOUCH`, `FREEINK_CAP_FRONTLIGHT`** |
| `XTEINK_X4_CLASSIC` | `-DFREEINK_DEVICE_X4CLASSIC=1` | X4 Classic | SSD1677 · UC8179 · UC8279_X4 · `FREEINK_CAP_RTC` · `FREEINK_BATTERY_I2C_GAUGE` · `FREEINK_SD_SDMMC`; **touch and frontlight left off** |
| `PAPER_MONO` | — | M5Stack PaperMono | SSD1677 |

Panel drivers shipped in the SDK: **SSD1677, UC8179, UC8253, UC8279, ED2208,
IT8951**, plus external-library-backed panels.

The SDK's architectural thesis, in its own words: *"Adding a new device means
adding **data** (a board profile + a driver config), not editing the generic
code."* That is what makes §4 short.

⚠ **The panel init sequences and waveform LUTs are third-party derived work**,
credited in `NOTICE` to the OpenX4 E-Paper Community SDK and to CidVonHighwind.
Worth knowing before treating them as authoritative for a given panel.

### 2.3 CrossPlay — `ma-r-s/crossplay`, branch `xteink`

MIT. Adds ~26 games and tools alongside the reader. Envs:

| Env | Device |
|---|---|
| `default`, `gh_release`, `gh_release_rc`, `slim` | C3, inherited from upstream |
| `sticky`, `gh_release_sticky` | Seeed reTerminal Sticky |
| **`x4pro`, `gh_release_x4pro`** | **Xteink X4 Pro — the design floor** |
| `papermono`, `papermono-gh_release`, `papermono-gh_release_rc` | M5Stack PaperMono |

**It consumes a *fork* of the SDK** — `ma-r-s/freeink-sdk`, branch
`x4pro-measured-insets` — so a port here has two moving upstreams, not one.

⚠ **The `papermono` envs are present in `platformio.ini` and absent from
`LOCAL_SCOPE.md`, and nobody has reported running CrossPlay on a PaperMono.**
Recorded as an open question, not as "supported".

**One CrossPlay change is a hardware fact, not a software preference.** Its
`src/network/OtaUpdater.cpp` repoints the release URL because **upstream's would
flash a C3 build onto an S3**. That is the sharpest available illustration of why
"X4 Pro" being an S3 and "X4" being a C3 matters.

### 2.4 The rest, by device

| Project | Devices | Note |
|---|---|---|
| `uxjulia/CrossInk` | **X3, X4, Sticky only** | The major second-tier fork. **No PaperMono support.** Notable for having shipped **ESP-NOW straight from an Activity** with no SDK capability gate — the working precedent for bypassing the abstraction |
| `mekhontsev/crosspoint-reader` + `crosspoint-plugins` + `pagewire` | **X4 Pro only** | MIT. Native C++ ELF plugin host loaded from SD against an ABI. Self-described experimental |
| `MarsTechHAN/crosspoint-reader-mono` | PaperMono | True fork, ★1 |
| `juicecultus/crosspoint-reader-papers3` | M5PaperS3 | Detached re-upload, ★67 |
| `vjFaLk/esphome-xteink` | X4 Pro | Exposes the device to Home Assistant as an ESPHome component |
| `thepropm/proink-os` | X4 Pro | From-scratch firmware on the FreeInk SDK |
| `parsimo2010/xteink-ft8` | X4 Pro | FT8 amateur-radio display |
| `MrStu82/crosspoint-llama-pro` | X4 Pro | Explicitly *"ESP32-S3, GT911 touch, dual warm/cold frontlight"* |

⚠ **Do not measure this ecosystem from GitHub's `/forks` listing.** Of fourteen
named, actively-discussed derivatives, **only five are GitHub forks**; the other
nine were re-uploaded as fresh repositories and are detached (`fork: false`,
`parent: null`), including the top-ten-by-stars CrumBLE and the CJK port. The
`1,621` figure simultaneously overcounts, because most forks of any popular
repository carry zero commits. **Enumerate by name.**

### 2.5 A hardware-relevant consequence of fork age

**Being behind upstream is a brick-risk signal in this ecosystem, not a tidiness
metric.** Xteink revises hardware silently — the X3's controller changed from
UC8253 to UC8279d around July 2026, and the X4 Pro ships three different
controllers on identical wiring — and upstream carries the fixes. CrossPoint's own
1.5 release notes say it directly: *"Other forks will need to pull the latest SDK
to avoid **soft bricking locked units**."*

---

## 3. The panel-controller runtime-detection trick

**This is the mechanism that lets one binary serve several boards, and it is the
most reusable idea in this whole ecosystem.** It is worth understanding even if you
never touch an Xteink.

### 3.1 The problem

The X4, X4 Pro and X4 Classic each ship with **at least three different display
controllers depending on production batch, on identical wiring**: a Solomon Systech
**SSD1677**, or an UltraChip **UC8179**, or an UltraChip **UC8279**. The X3 ships
either a **UC8253** or, from around July 2026, a **UC8279d**.

The command sets differ. A firmware that assumes the wrong one produces a panel
that resets, runs waveforms, and **never develops an image** — a failure mode the
X4 Pro bring-up spent months on. And **there is no external revision marking that
tells you which you have before powering the unit on.**

### 3.2 The trick

**UC81xx parts answer the vendor commands `VER (0x70)` and `FLG (0x71)`. The
SSD16xx family does not answer them at all.**

The SDK exploits that with a bit-banged half-duplex read on the display pins —
which are normally write-only — after a reset pulse:

1. Bit-bang a half-duplex 4-wire SPI **read** on the display bus after reset.
2. Issue **`VER (0x70)`** — 5 bytes — and **`FLG (0x71)`** — 1 byte.
3. Because the SSD family never drives the line, a released SDA floats to a
   **uniform `0x00` or `0xFF`** through the pull-up.
4. **Match = UltraChip** when `FLG` is neither `0x00` nor `0xFF`, has `BUSY_N`
   (bit 0) set, **and** `VER` is non-uniform.
5. Then **`VER` byte 2 (`LUT_VER`)** discriminates the family member:
   `0x02` / `0x68` / `0x69` → **UC8279**; anything else → **UC8179**.

```c
// freeink-sdk XteinkDetect.cpp:113-119, commit 2400379
bool matchUc81xx(const uint8_t ver[5], uint8_t flg) {
  if (flg == 0x00 || flg == 0xFF) return false;
  if ((flg & 0x01) != 0x01) return false;
  return !verIsFloating(ver);
}
```

The probe logs `[XTDET] bus probe VER=… FLG=… -> UltraChip|default|inconclusive`
over serial, plus the MTP header (`RMTP 0xA2`) when the status line was driven —
`0xA5` at byte 0 means a UC part with a programmed MTP.

### 3.3 ⚠ A negative result worth keeping

An earlier matcher additionally required `ver[1] != 0`. **A shipping X4 Pro UC8179
was then observed returning `VER = 00 00 01 FF FF` — a `CHIP_VER` byte of
`0x00` — and was wrongly rejected.** The matcher now deliberately **does not pin
any specific `CHIP_VER` value**. Do not reintroduce that check.

Two related questions remain open on the X3 side: what the **UC8253** actually
answers to `0x70`, and whether production MTP programs `CHIP_VER` to something
other than `0x03`.

### 3.4 The X4 Classic exception, and why it is dangerous

**The X4 Classic's display bus has no MISO line at all**, so the probe cannot work
— the released line always floats to `0xFF`. It is the one device in the family
where **NVS is authoritative**:

```
NVS namespace hw_calib, key screenType (u8):
  1 or 0x0B → UC8179
  2 or 0x0C → UC8279
  3 / default / unset → SSD1677
```

The factory writes this once. On every *other* device the SDK reads
`hw_calib/screenType` **for diagnostics only** and never decides on it, because a
full-flash image taken from another unit overwrites it and can therefore name the
wrong panel. On the X4C there is no live check to override it.

> **Consequence: restoring an X4 Classic from someone else's full-flash image can
> leave it with the wrong panel driver and no way to detect that.**

### 3.5 The same idea, applied to the board itself

The SDK uses a second runtime fingerprint to tell an **X3 from an X4** — they share
a SoC, a flash size and a firmware binary:

- Probe the C3's secondary I²C bus (**SDA GPIO20 / SCL GPIO0**) for **`0x55`**
  (BQ27220 fuel gauge), **`0x68`** (DS-series RTC) and **`0x6B`** (QMI8658 IMU).
- **Find them → X3. Find nothing → X4.** The X4 has no I²C peripherals at all, and
  that absence *is* the discriminator.

⚠ **That probe must be compiled out on an S3.** On the C3, GPIO20 and GPIO0 are
ordinary pins; on the **ESP32-S3** they are **USB D+ and a boot strap**. Running
the C3 fingerprint on an S3 would poke USB D+ and a strapping pin at boot.
`XteinkDetect` compiles the path to a no-op unless a C3 profile is in the build.

### 3.6 Prior art elsewhere in this repository

The pattern — *probe at boot, branch on capability rather than on a compile-time
device identity* — recurs:

| Device | Probe | Discriminates |
|---|---|---|
| Xteink X4 Pro / X4 / X3 | `VER`/`FLG` on the panel bus | SSD16xx vs UC8179 vs UC8279 |
| Xteink X3 vs X4 | I²C addresses `0x55`/`0x68`/`0x6B` | which board |
| [M5Stack PaperMono vs Lite](../m5stack/papermono/features/nfc.md) | write M5IOE1 `IO4`, then read ST25R3916 register `0x7F` expecting `0x05` | Pro vs Lite. ⚠ **M5GFX cannot make this distinction** — it masks NFC out of board detection, so both SKUs land on one enum |
| [Cardputer ADV vs v1.x](../m5stack/cardputer-adv/README.md#board-autodetect) | drive G8/G9 as input-pulldown and read them | TCA8418 vs 74HC138 keyboard. ⚠ The test is only *"are there pull-ups"* — anything pulling those pins high on a v1.x makes M5GFX declare it an ADV and the keyboard stops working |
| [Cap LoRa-1262 vs Cap LoRa868](../m5stack/cap-lora-1262/features/io-expander-and-rf-switch.md) | probe I²C `0x43` | which Cap is fitted |

The recurring lesson is in the two ⚠ rows: **a fingerprint that tests a proxy
rather than the thing itself will eventually misfire.** The `VER`/`FLG` probe is
the good version because it asks the controller to identify itself.

---

## 4. What a new board has to provide to be supported

`inferred` from the SDK's design and from three measured ports. This is the
checklist to work through before proposing a board.

### 4.1 The measured cost of a port

From the FreeInk SDK record (`reported-working`, measured on real ports):

| Port | Files touched | Lines |
|---|---|---|
| Xteink X4 Classic | 7 | +295 |
| M5Stack PaperS3 | 10 | +397 |
| OnePage (a new MCU) | 8 | +245 |

**A typical port is 7–10 files and 250–400 lines.** Order matters: the SDK port
comes first, then the consuming firmware's build environment — CrossPoint's
`ROADMAP.md` says so explicitly.

⚠ **There is no CI validation for device ports in the SDK**, against CrossPoint's
multi-environment build matrix. A port can break without the SDK's own tests
noticing.

### 4.2 The hardware checklist

| # | Requirement | Why | Consequence if absent |
|---|---|---|---|
| 1 | **An ESP32-C3 or ESP32-S3** | Those are what the SDK targets in practice | Anything else is a new MCU port (the `OnePage` port is the precedent that it is possible) |
| 2 | **A supported panel controller** — SSD1677, UC8179, UC8253, UC8279, ED2208 or IT8951 | Drivers ship | A new driver, plus **waveform LUTs, which are the hard part** and are third-party derived work. See [`guides/hardware/e-paper-displays.md`](../../guides/hardware/e-paper-displays.md) |
| 3 | **PSRAM, if you want the good rendering path** | Multi-buffer rendering, damage-window partial refresh and large book indices need it | On a C3 they are simply unavailable. **The C3 env sets CrossPoint's memory ceiling**, and OTA out-of-memory was *observed* on the X3 — CrossPoint stopped using GitHub releases because of it |
| 4 | **A MISO line on the display bus**, if you want runtime controller detection | §3 | You inherit the X4 Classic's problem: a stored value is your only source of truth, and it can be wrong |
| 5 | **An input path the SDK models** — an ADC ladder, discrete GPIOs, or touch | Input manager | CrossPlay's stated design floor is **"two side keys plus touch"**; firmware that works there is expected to degrade gracefully elsewhere |
| 6 | **Storage** — SPI microSD, or 1-bit SDMMC | `FREEINK_SD_SDMMC` | ⚠ **1-bit SDMMC additionally needs `-DUSE_BLOCK_DEVICE_INTERFACE=1` in the *consumer* build.** A hand-rolled env that forgets it compiles and then fails to mount the card |
| 7 | **A documented master peripheral rail**, asserted first at boot | e.g. the X4 Pro's **GPIO1**, driven HIGH before any other bring-up | Symptom: *"EPD BUSY never asserts, SD returns 0xFF"* |
| 8 | **Known enable polarities** | The X4 Pro's touch (GPIO2) and SD (GPIO5) enables are **active-LOW**, the opposite of the usual convention | Driving them HIGH — the naive "enable" — leaves the touch controller silent and breaks every SD block read with error `0x107` |
| 9 | **A battery power story** | latch, gauge or bare ADC | The X4's **GPIO13 gates the battery MOSFET**, and *"at least one hardware revision in the field does not self-latch"*. Always assert the latch |
| 10 | **Bezel viewable insets** | Screens draw under the glass without them | The X4 Pro's are `{9,7,3,7}` |
| 11 | **A flashing route that survives a USB lock** | §5 | Otherwise you cannot get your first image on |

### 4.3 ⚠ The trap: GPIO numbers do not port within this family

Three worked examples from one family, all real:

- **`GPIO13` means three different things.** SD power rail on the X3
  (**active-HIGH**), battery power-off latch on the X4, unused on the S3 boards.
  **Never port power code between them.**
- **The X4 Classic's display pins are a permutation of the X4 Pro's** on the same
  SoC and the same panel: DC 18 → **14**, RST 14 → **10**, BUSY 6 → **18**. SCLK,
  MOSI and CS are shared. Porting display code without changing those three
  produces a panel that resets and never develops an image.
- **`GPIO0` on an X4 Pro is the Left button *and* the boot strap.** Powering on
  with Left held enters download mode.

### 4.4 What a board profile actually declares

Read the [X4 Classic record](x4-classic/README.md#development) for a complete
worked example — it is the shortest and the most explicit, because the whole board
was decoded from a firmware dump and the SDK records its confidence per pin:

```ini
[env:x4c]
extends = base
board = esp32-s3-devkitc1-n16r8
board_build.mcu = esp32s3
build_flags =
  ${base.build_flags}
  -DBOARD_HAS_PSRAM
  -DUSE_BLOCK_DEVICE_INTERFACE=1   ; SD is 1-bit SDMMC
  -DFREEINK_DEVICE_X4CLASSIC=1
```

That, plus the profile struct, is the port.

**What the profile has no field for: a radio.** Grepping the SDK for the
PaperMono's LoRa SPI pins returns nothing, and there is no radio struct. See
[adding LoRa, NFC and an RGB sidelight](../../guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md)
for what that means and what the four missing pin constants are. Note that the SDK
**does** already carry `T5S3_LORA_CS/IRQ/RST/BUSY` for the LilyGO T5S3 — so a
second LoRa board already exists to justify a real `FREEINK_CAP_LORA` abstraction.

---

## 5. Getting your first image onto the hardware

Firmware support is worthless if the device will not accept a flash. **Many
Xteink units — X3, X4 and X4 Pro alike — ship from the factory with USB flashing
disabled.** `esptool` cannot see them. The community calls these "USB-locked".

| Path | What it does | Status |
|---|---|---|
| **CrossPointReader.com web flasher** | *"OTA Unlock usb locked stock devices by flashing CrossPoint and CrossInk"* | `reported-working` — 346 pts |
| **SD-card update** | Drop `update.bin` on the SD root, hold **Power + Up** at boot; the **stock bootloader** picks it up. No cable, no unlock | `reported-working` — ⚠ its own author says *"that path relies on stock-bootloader behavior I don't control, so confirm the button combo for your unit first"* |
| **Developer-unlocked units** | Xteink sells an explicitly unlocked variant | `reported-working` |
| `OvermindDL1/xteink-unlocker` | Tauri/Rust desktop app implementing the unlock | not inspected in depth |

⚠ **Lock state is not predictable from the sales channel.** One owner who bought
three units reported an Amazon X3 unlocked, an official-store X3 **locked**, and an
AliExpress X4 locked.

⚠ **Make a full-flash backup before you do anything.** Only **one** Xteink factory
image exists publicly anywhere — the X4's 16 MB dump, archived in this repository.
**No X4 Pro or X4 Classic stock image was located.**

Per-device detail: [X4 Pro development](x4-pro/development.md) ·
[factory firmware](x4-pro/factory-firmware.md).

---

## 6. Where the hardware and software trees meet

| From here | To there |
|---|---|
| [X3](x3/README.md) · [X4](x4/README.md) · [X4 Pro](x4-pro/README.md) · [X4 Classic](x4-classic/README.md) | [CrossPoint Reader](../../software/applications/crosspoint-reader/README.md) — build envs and device support |
| Board profiles, panel drivers, capability gates | [FreeInk SDK](../../software/frameworks/freeink-sdk/README.md) |
| X4 Pro as the design floor; the OTA C3/S3 hazard | [CrossPlay](../../software/applications/crossplay/README.md) |
| Which derivative is a real fork, and what "behind" costs | [Fork network](../../software/ecosystems/crosspoint-freeink/fork-network.md) |
| Can a plugin reach a bus? (**No** — 81-symbol allow-list, link fails) | [CrossPoint plugin systems](../../software/applications/crosspoint-reader/plugins/README.md) |
| Adding radios to this class of firmware | [Radios on the PaperMono](../../software/ecosystems/crosspoint-freeink/radios-on-papermono.md) · [the capability guide](../../guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md) |
| Running the firmware with no hardware at all | [Simulator build notes](../../software/tooling/crosspoint-simulator-build-notes.md) — ✅ `executed-success` on NixOS |
| Content pipeline | [Calibre](../../software/tooling/calibre/README.md) |
| Why the SoC choice constrains all of this | [SoC choice for battery e-ink devices](../../guides/hardware/soc-choice-for-battery-eink-devices.md) |
| Where these boards sit in the market | [Handheld and e-ink device landscape, 2026-09](../../guides/markets/handheld-and-eink-device-landscape-2026-09.md) |

---

## 7. Open questions and evidence boundary

- **Nothing on this page was built, flashed or run.**
- **No commit SHA is pinned for CrossPoint `develop` or FreeInk `main`** in the
  software records; the FreeInk commit `2400379…` cited here is the one the Xteink
  device records read. Pin HEAD before citing code.
- **Whether the `papermono` envs — upstream's or CrossPlay's — have ever been run
  on real hardware by anyone is unknown.**
- **The FreeInk SDK declares `ImuType::None` for the PaperMono** despite a BMI270
  being fitted and wired. Deliberate or unported: **not established**.
- **What the UC8253 answers to `0x70`** is not established, and the UC8279d X3
  variant *"has never been on a bench"* — the SDK's own words.
- **The X3's RTC is unresolved**: the SDK drives a DS3231, the English teardown
  captions "DS1307", the Chinese BOM says only "DS-series". All at `0x68`.
- **The X4 Classic's `GPIO4` role is unknown** — an input, but not
  interrupt-attached, so not a button.
- The **74 % single-author concentration** in SDK commits is carried over from an
  earlier analysis and was **not re-measured**.
- **No binary size, flash usage, heap figure or build time exists for any
  environment of any of these projects.**

## See also

[Family index](README.md) · [X3](x3/README.md) · [X4](x4/README.md) ·
[X4 Pro](x4-pro/README.md) · [X4 Classic](x4-classic/README.md) ·
[S4](s4/README.md) · [Nano](nano/README.md) ·
[M5Stack PaperMono](../m5stack/papermono/README.md) ·
[`software/`](../../software/README.md)
