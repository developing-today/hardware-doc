# Firmware projects supporting the Xteink X4 Classic

Census **2026-09-11**. Every entry is pinned to a commit. Support is graded by
**whether anyone has run it on X4 Classic hardware**, which is the only grade
that matters for a board whose pinout has never been verified against a physical
unit.

| Grade | Meaning |
|---|---|
| **A** | Built **and** run on a physical X4 Classic by a named party |
| **B** | Board profile present, built, **never run on X4C hardware** |
| **C** | Board profile present, copied from another project |
| **D** | Community reports of it working, no primary artefact |

## The projects

### FreeInk SDK — grade **B**, and the origin of everything

| | |
|---|---|
| Repo | [`Free-Ink/freeink-sdk`](https://github.com/Free-Ink/freeink-sdk) |
| HEAD at census | **`9f4d3f9ca675e64cc9d616081f39a33cdefce57e`**, 2026-09-10 |
| Stars | 253 |
| Profile | `BoardConfig::XTEINK_X4_CLASSIC`, `Board::XteinkX4Classic` |
| Build | `-DFREEINK_DEVICE_X4CLASSIC=1`, env `[env:x4c]` |
| Doc | [`docs/xteink-x4c-support.md`](https://github.com/Free-Ink/freeink-sdk/blob/9f4d3f9ca675e64cc9d616081f39a33cdefce57e/docs/xteink-x4c-support.md) |
| Derived from | A **privately held** X4C OEM flash dump, reverse-engineered in Ghidra |

**Change since the 2026-09-04 snapshot: exactly one line.** Commit
[`39606d5a`](https://github.com/Free-Ink/freeink-sdk/commit/39606d5a) (2026-09-09,
*"Fix e-ink display buffer tracking and optimize SPI writes"*) replaced the
X4C's literal `20000000` `displaySpiHz` with a shared
`XTEINK_DISPLAY_SPI_HZ = 10000000u` applied to **every** Xteink profile. The
support doc changed the matching sentence. Nothing else in the profile moved.

**No new Xteink board entered `enum class Board` between `2400379` (2026-09-01)
and HEAD.** The enum gained `M5PaperS3`, `EegoA4`, `OnePage` and `WsEpaper397` —
all other vendors. This is the strongest available evidence that **no new Xteink
SKU exists between the X4 and the X4 Pro** beyond the X4 Classic itself.

### `clackups/draftling` — grade **B** for X4C, grade **A** for X4 Pro

| | |
|---|---|
| Repo | [`clackups/draftling`](https://github.com/clackups/draftling) |
| HEAD at census | `92ba7e514f66bbe42a7fea6d38eff45eed82617b`, pushed **2026-09-11** |
| Licence | **MIT** · 71 stars · created 2026-06-05 |
| What it is | A **writerdeck** firmware for ESP32-S3 and ESP32-P4 — an editor, not a reader |
| X4C files | `firmware/main/boards/xteink_x4_classic.h`, `sdkconfig.defaults.xteink_x4_classic`, `partitions_xteink_x4_classic.csv`, a chapter in `HARDWARE.md` |

**The most useful third-party document about this board.** It is an independent
*reading* of the FreeInk profile by someone building a different product, which
surfaces things the profile alone does not:

- It states the naming equivalence in a source comment: *"Xteink X4 Classic
  (also marketed "X4 v2")"*.
- It maps the eight inputs to an editor: Power = F1 / 2 s = forget BLE keyboards;
  side keys = Up/Down; bottom keys = Left/Right/Enter/Esc; **GPIO4 ignored**,
  matching FreeInk.
- It names the panel-pin difference from the Pro explicitly: **DC 14, RST 10,
  BUSY 18** here versus **18 / 14 / 6** on the Pro, with SCLK/MOSI/CS the same.
- It notes the X4C's UC8279 init **omits the PLL (`0x30`) command** the Pro
  programs.
- It keeps a **dual-OTA partition table on purpose**, because the stock and
  CrossPoint updaters both refuse a table with no `otadata` — *"Partition table
  has no otadata partition"*. A single-`factory` table leaves the device unable
  to accept either without a USB reflash, and **the X4 Classic has no USB
  socket**, which makes that a much worse trap here than on a dev board.

**It is honest about its limits**, verbatim: *"**This board has been added
without on-hardware testing.**"*

Its **X4 Pro** support, by contrast, is grade **A** and produced two real
findings — see [`../x4-pro/README.md`](../x4-pro/README.md).

### CrossPoint Reader — grade **D**

[`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader)
carries `XteinkX4Classic` in `lib/hal/HalGPIO.cpp` and an `x4c` env in
`platformio.ini`. The simulator mirrors it.

Community evidence of it actually running:

- [r/CrossPointReader `1wbmagp`](https://old.reddit.com/r/CrossPointReader/comments/1wbmagp/),
  2026-09-09, "Xteink X4 Classic support".
- u/Diirge, 2026-09-10: *"CrossPoint sleep screen rendering got much better as of
  today on the x4c fyi"* — **firsthand, dated, on-device**, the single best
  evidence that CrossPoint runs on an X4C.
- [r/XTEINK `1wctkd6`](https://old.reddit.com/r/XTEINK/comments/1wctkd6/),
  2026-09-10, "Crosspoint or Crossink? Differences on x4 classic".

No build log, no flash log and no screenshot from an X4C was retrieved. **Grade D
is deliberate**: it is very probably working, and this repository has no artefact
proving it.

### `vjFaLk/esphome-xteink` — grade **C**

ESPHome components (MIT, created 2026-08-30). **Vendors the FreeInk SDK verbatim**
at `components/xteink/sdk/…/BoardConfig.h`. Not an independent reading; it is the
same file in a different tree. Useful only as a distribution channel.

### `mohitagw15856/Inkkit` — grade **C**

Shared HAL library (MIT, created 2026-07-29). `src/BoardConfig.h` is a copy. Its
own description scopes it to *"Xteink X4/X3, ESP32-C3"* — the X4C entry is
inherited, not targeted.

### `kycube/x4pro-emu` — X4 Pro only, but read it anyway

Not an X4C project. It matters here because the X4 Pro flash dump it publishes
contains **`ESP32S3_X4_CLA` and `ESP32S3_X4R2_CLA`**, proving the stock firmware
is one binary family across both boards. See [`README.md`](README.md) §`R2`.

### `x4pro-emu`-adjacent: no X4C emulator exists

A QEMU model of the X4 Pro now exists and boots both stock and CrossPoint. **No
equivalent exists for the X4 Classic**, and building one would be cheap: same
SoC, same flash map, same panel stack, fewer peripherals. It is the lowest-cost
way to test X4C firmware without the hardware, and nobody has done it.

## Independent-custodian count for this record

| Custodian | Independent of FreeInk? | Hardware? |
|---|---|---|
| FreeInk SDK | — | private X4C dump, not published |
| `clackups/draftling` | **reading only** — cites FreeInk as its source | **no** |
| CrossPoint Reader | no | community reports only |
| `esphome-xteink`, `Inkkit` | no — verbatim copies | no |
| **FCC `2BTR9-X4C`** | **yes** | **yes — but photos embargoed to 2027-01-16** |
| **Vendor store + spec block** | **yes** | product-level only |

**Two genuinely independent custodians now exist** (the FCC grant and the vendor
listing), where on 2026-09-04 there were none. Neither is a board-level custodian.
**The hardware claims in this record still rest on a single private firmware
dump**, and that will remain true until 2027-01-16 or until somebody opens one.
