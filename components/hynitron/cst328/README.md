# Hynitron CST328

- **Category:** **mutual-capacitance** multi-touch controller, I²C slave.
- **Manufacturer:** Hynitron Microelectronics (上海海栎创).
- **Retrieved:** 2026-09-07
- **Sibling record here:** [`cst816d`](../cst816d/README.md) — the *self*-capacitance CST816
  family this part replaced on LilyGO's boards.

The touch controller on **later** production of the **LilyGO T-Display-S3 Touch**.

## 1. Why this record exists separately from CST816

Because they are not interchangeable, and LilyGO swapped one for the other **without renaming
the product**.

| | CST816S | **CST328** |
|---|---|---|
| Sensing | **self**-capacitance | **mutual**-capacitance |
| I²C address | `0x15` | **`0x1A`** |
| `TouchLib` build flag | `-DTOUCH_MODULES_CST_SELF` | **`-DTOUCH_MODULES_CST_MUTUAL`** |
| Multi-touch | limited | more simultaneous points |

Mutual capacitance is the better technology — it resolves multiple touches properly and is less
affected by a hand hovering — which is presumably why the swap happened. The cost is that
firmware built for one reports **"no Touch IC found"** on the other, and the flag that selects
between them lives in `platformio.ini`, not in the sketch. That is
[LilyGO issue #125](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/125) (15 comments).

**LilyGO's current default is `-DTOUCH_MODULES_CST_MUTUAL`**, i.e. CST328 — see
`platformio.ini` @ `ec889e789b3cf093412689a143f7f37b42b56af7`.

## 2. Identity and artifact

| Property | Value |
|---|---|
| Part | **CST328** |
| Datasheet | `CST328数据手册V2.2.pdf` — Chinese, **V2.2** per the filename |
| Local artifact | [`artifacts/cst328-datasheet-cn-v2.2-lilygo-mirror.pdf`](artifacts/cst328-datasheet-cn-v2.2-lilygo-mirror.pdf) — 1 297 291 B, SHA-256 `fd7770d17fb29bf6bc3f0b6116f940d8249a3ab9129c9df1491e24078b6fcbd6` |
| Mirror source | `Xinyuan-LilyGO/T-Display-S3` → `datasheet/CST328数据手册V2.2.pdf` @ `ec889e7` |
| Language | **Chinese only.** No English version was located, from Hynitron or any mirror. Per the multi-language policy this is therefore the **primary source**, not a translation, and it is retained on its own merits |
| Licence | Hynitron copyright; the surrounding repository is MIT, which does not cover it. **Redistribution status: unknown** |

The presence of *both* this datasheet and the CST816S register guide in one board repository is
the evidence that both controllers ship — a board with one controller does not need two
manuals.

## 3. Software

| Route | Note |
|---|---|
| **`mmMicky/TouchLib`** | the Arduino driver LilyGO uses. Select the mutual branch with `-DTOUCH_MODULES_CST_MUTUAL` |
| ESP-IDF | no first-party driver; use `LilyGo-Display-IDF` or write one. [Issue #156](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/156) is someone discovering this |
| ESPHome | the `T-DISPLAY-S3` model covers the display only; touch is configured separately |

**Reset before probing.** Hold `RST` low ≥ 10 ms, release, wait ≥ 50 ms. Many "intermittent
touch" reports are a missing reset.

**Expect NAKs.** The CST parts NAK while idle; a driver that treats a NAK as a bus fault will
log errors continuously. That is
[issue #168](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/168) (21 comments), where the
reporter had nothing else on the bus.

## 4. What was not verified

The datasheet was **not read** — it is in Chinese, its text layer was not validated against a
rendered heading, and **no register value is transcribed into this record**. The addresses and
flag names above come from board-level and library-level sources. Reading the register map is
the obvious next step and would let this record document the protocol properly.

## 5. Used by

### LilyGO T-Display-S3 Touch (later production)
→ [`devices/lilygo/t-display-s3-touch`](../../../devices/lilygo/t-display-s3-touch/README.md)

I²C address **`0x1A`** on **GPIO17 (SCL) / GPIO18 (SDA)**, with on-board 10 kΩ pull-ups.
Interrupt **GPIO16**, reset **GPIO21**. The controller sits on the panel flex, not on the
mainboard, which is why it does not appear in the board schematic's part census — and it is
powered from the **GPIO15-gated rail**, so an I²C scan with GPIO15 low finds nothing.
Revision detail: [R1](../../../devices/lilygo/t-display-s3-shared/board-revision-drift.md#r1--t-display-s3-touch-cst816s--cst328).
