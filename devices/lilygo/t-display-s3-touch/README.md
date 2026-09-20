# LilyGO T-Display-S3 Touch

> **Not a separate PCB.** LilyGO publishes **one schematic** (`T_Display_S3.pdf`) for both the
> T-Display-S3 and the Touch version, and one repository covers both. This record exists
> because the Touch version is a distinct SKU with distinct software requirements — and because
> **which touch controller it carries changed silently**.
>
> SKUs `H587` (non-soldered) **USD 12.61**, `H589` (soldered) **USD 13.02**,
> `H717`/`H705`/`H681` shell and regional variants up to **USD 38.48**. In stock 2026-09-07.
> Research retrieved 2026-09-07. Depth: **medium — deliberately, because the base-board record
> covers everything electrical.**

## Read the base-board record first

Everything about the SoC, flash, PSRAM, display bus, power, GPIO15, USB, battery and Wi-Fi is
identical and is documented once at **[`../t-display-s3/README.md`](../t-display-s3/README.md)**.
Shared artifacts: [`../t-display-s3-shared/`](../t-display-s3-shared/README.md).

## What is different

| | Base | **Touch** |
|---|---|---|
| Panel | 1.9″ IPS, no digitiser | 1.9″ IPS **with a bonded capacitive digitiser** |
| Touch controller | none | **Hynitron CST816S** (early) **or CST328** (later) |
| I²C address | — | **`0x15`** (CST816S) / **`0x1A`** (CST328) |
| GPIO16 (`TOUCH_INT`) | fitted pull-up, otherwise unused | touch interrupt |
| GPIO21 (`TOUCH_RES`) | free | touch reset |
| Price | USD 9.04 | **USD 12.61** (+3.57) |
| Build flag | irrelevant | **`-DTOUCH_MODULES_CST_MUTUAL`** (CST328) or `-DTOUCH_MODULES_CST_SELF` (CST816S) |

That is the entire delta. The touch controller is **on the panel flex**, not on the mainboard —
which is why one schematic covers both, and why no touch-controller designator appears in the
schematic's part census.

## The one thing that will cost you an evening

**Two generations of touch controller ship under the same product name**, and the driver flag
that selects between them lives in `platformio.ini`, not in your sketch. LilyGO's current
default is `-DTOUCH_MODULES_CST_MUTUAL` (**CST328**). If your board is an early **CST816S**,
that default finds nothing and reports "no Touch IC found" —
[issue #125](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/125), 15 comments.

**Identify before you build:** run `examples/I2CScan` on GPIO17/18.

The evidence that both exist is that the board repository ships **both register documents** —
`CST816S寄存器说明-20190508.pdf` (76 816 B) and `CST328数据手册V2.2.pdf` (1 297 291 B). A board
with one controller does not need two manuals. Full treatment:
[revision R1](../t-display-s3-shared/board-revision-drift.md#r1--t-display-s3-touch-cst816s--cst328)
and [`../t-display-s3/features/touch.md`](../t-display-s3/features/touch.md).

## Second thing: I²C lives on the gated rail

The touch controller is powered from the GPIO15-gated `V3V` rail. **An I²C scan with GPIO15
low finds nothing**, which is indistinguishable from a dead controller. Drive GPIO15 high
before scanning.

## Software

Identical to the base board except the flag above. `TouchLib` (`mmMicky/TouchLib`) is the
Arduino driver; ESP-IDF users need `LilyGo-Display-IDF`
([issue #156](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/156)). ESPHome's
`T-DISPLAY-S3` model covers the display; touch is configured separately.

Examples: `touch_test`, `CapacitiveTouch`, `usb_hid_pad`, `factory` — all in the base-board
repo at `ec889e7`, catalogued in
[`../t-display-s3/examples/catalog.json`](../t-display-s3/examples/catalog.json).

## Artifacts

**None held separately.** The schematic, firmware and dimension files are the base board's and
live once in [`../t-display-s3-shared/artifacts/`](../t-display-s3-shared/artifacts/). The
touch-controller datasheets are filed under
[`components/hynitron/cst816d/`](../../../components/hynitron/cst816d/artifacts/) and
[`components/hynitron/cst328/`](../../../components/hynitron/cst328/artifacts/).

The repo does hold Touch-specific mechanical files —
`dimensions/CapacitiveTouchScreen.stp` (169 278 B) and
`dimensions/Lilygo_T-DisplayS3_Touch_from Stuttgart.zip` (2 393 118 B, a community-contributed
3D model) — **neither retrieved by this pass**; recorded here so they are findable.

## Sources

| ID | Source | Class | Retrieved | Establishes |
|---|---|---|---|---|
| T1 | `Xinyuan-LilyGO/T-Display-S3` README § *Supported Products* @ `ec889e7` | primary | 2026-09-07 | Touch is a variant of the same board, same schematic, same dimensions |
| T2 | `platformio.ini` @ `ec889e7` | primary | 2026-09-07 | `-DTOUCH_MODULES_CST_MUTUAL` is the current default |
| T3 | `datasheet/CST816S…pdf` + `datasheet/CST328…pdf` @ `ec889e7` | credible mirror | 2026-09-07 | two controller generations |
| T4 | Store feed | primary | 2026-09-07 | SKUs and prices |
| T5 | [Issue #125](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/125), [#168](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/168), [#156](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/156) | community | 2026-09-07 | the driver-flag failure, I²C NAK behaviour, ESP-IDF gap |

## Gaps

- **The changeover date from CST816S to CST328 is unknown.** No vendor announcement exists.
- **No external way to tell the two apart** was found; identification is by I²C scan only.
- Not verified on hardware.
