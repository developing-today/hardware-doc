# LilyGO board-revision drift — what changes under one name, and how to tell

> Family-level. Snapshot **2026-09-07**. This is the document to read before trusting *any*
> pin map, schematic or photograph for a LilyGO board you have not physically identified.

## The problem, stated plainly

LilyGO revises boards without renaming them, without incrementing a visible revision, and
without withdrawing the old schematic. There is no changelog, no ECN, no revision field on most
silkscreens. The result is that "T-Display-S3" and "T-Display-S3 AMOLED" each name **a set of
boards**, and code that works on one member can fail on another.

This is not a criticism that requires inference — LilyGO **sells two revisions of the same
product side by side in the same dropdown** (see R2 below), which is the clearest possible
admission that the name does not identify the hardware.

## Evidenced revisions

Ordered by how likely you are to be bitten.

### R1 — T-Display-S3 Touch: **CST816S → CST328**

| | |
|---|---|
| **Boards** | T-Display-S3 Touch (`H587`, `H589`) |
| **What changed** | The bonded touch controller. **CST816S** is *self*-capacitance, I²C `0x15`. **CST328** is *mutual*-capacitance, I²C `0x1A`, and supports more simultaneous points |
| **Evidence** | The board repo `Xinyuan-LilyGO/T-Display-S3` @ `ec889e7` ships **both** datasheets in `datasheet/`: `CST816S寄存器说明-20190508.pdf` (76 816 B) and `CST328数据手册V2.2.pdf` (1 297 291 B). A board with one controller does not need two register manuals |
| **Second evidence** | `platformio.ini` @ `ec889e7` carries `-DTOUCH_MODULES_CST_MUTUAL` in the shared `[env]` — i.e. the vendor's *current default build* selects the **mutual**-capacitance (CST328) driver branch |
| **How to tell them apart without opening anything** | Scan I²C on GPIO17/18. `0x15` → CST816S. `0x1A` → CST328 |
| **What breaks** | A sketch built with `-DTOUCH_MODULES_CST_SELF` (or an older LilyGO example) finds no touch controller on a new board, and vice versa. This is the mechanism behind [issue #125 "no Touch IC found"](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/125) (15 comments) |
| **Date bounds** | CST816S register guide is dated 2019; the CST328 datasheet is V2.2. LilyGO never announced the switch, so the changeover date is **unknown** |

### R2 — T-Display-S3 AMOLED 1.91″: **V1.0 and V2.0 sold concurrently**

| | |
|---|---|
| **Evidence** | LilyGO's own store feed, retrieved 2026-09-07, offers under the single handle `t-display-s3-amoled`: `H619` "V1.0 Non-Soldered Pin", `H634` "V1.0 Soldered Pin", `H713` "V2.0 Non-Soldered Pin", `H712` "V2.0 Soldered Pin" — **all four in stock at the same time**, plus separate `H681`/`H705`/`H717` "Touch" SKUs |
| **What changed** | Not stated by LilyGO anywhere. Comparing the two schematics LilyGO publishes for this board strongly suggests a power-section redesign: `T-DISPLAY-S3-AMOLED.pdf` (in the older `T-Display-S3-AMOLED` repo) shows `U4 = RT9080` LDO, `U6 = BV6802`, `U3 = W25Q32`; `T-Display-S3-AMOLED-Touch.pdf` (in `LilyGo-AMOLED-Series`) shows `U4 = SY8089A1AAC` **buck**, `U5 = AXPM65611`, `U3 = W25Q128JV` |
| **How to tell** | Read the silkscreen; these boards do carry `V1.0`/`V2.0`. Failing that, `esptool.py flash_id` distinguishes 4 MB from 16 MB |
| **What breaks** | Anything assuming 16 MB flash on a V1.0 built to the older sheet; any current-consumption assumption (LDO vs buck) |
| **Status** | **Unresolved.** LilyGO publishes no V1→V2 delta. Recorded as conflict F3 in the [family README](README.md#4-family-level-conflicts) |

### R3 — T-Display-S3 base: **the charger does not match the schematic**

| | |
|---|---|
| **Evidence — schematic** | `schematic/T_Display_S3.pdf`, title block **2024-04-29**, shows `U6 = TP4065` with a `PROG` pin and a 2 kΩ program resistor `R9`; a sheet note reads `R13  IBAT (mA) = 580` |
| **Evidence — hardware** | [Issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230), 2024-03-02, an owner tracing a physical PCB: *"when I try to find the TP4056 on the PCB it cannot be found? … Tracing out the PCB I find that the charging IC appears to be a device that is a **5-Lead TSOT-23 package with the marking of `65b311`** printed on top. This does not agree with the posted schematic."* Evidence class: **firsthand physical inspection** |
| **Third data point** | Three AMOLED schematics carry a part LilyGO spells **`AXPM65611`**. The shared `65611`/`65b311` fragment is suggestive but **not proof** |
| **Practical consequence** | The published charge-current programming procedure (swap `R9` for 10 kΩ to get ~130 mA) is derived from a TP4056/TP4065 datasheet that may not describe the fitted part. **Do not modify the charge resistor on the strength of the schematic alone** |
| **Status** | **Unresolved.** The part was never identified — [`components/unidentified/lilygo-t-display-s3-family/axpm65611/`](../../../components/unidentified/lilygo-t-display-s3-family/axpm65611/README.md) records what would settle it |

### R4 — T-Display-S3 base: **GPIO16/17 pull-ups fitted on non-touch boards**

| | |
|---|---|
| **Evidence** | [Issue #313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313), 2025-07-28. LilyGO maintainer `lewisxhe` posted **two photographs of the PCB back showing the resistors** and wrote: *"Pull-up resistors are already added to the 16 and 17 boards, so when you set it to floating, it's pulled high by default… If you must use these two GPIOs, you can remove these two resistors."* The reporter confirmed a **non-touch** board |
| **How to tell** | Measure GPIO16/GPIO17 to 3V3 with the board unpowered, or look at the back of the panel |
| **What breaks** | Any use of GPIO16/17 as a clean input or a low-side driver; and the pins go high again the moment you enter deep sleep |
| **Status** | **Confirmed by vendor.** Whether *all* production runs fit them is not established |

### R5 — T-Display-S3 Long: **CST3530 touch appears mid-life, in a branch**

| | |
|---|---|
| **Evidence** | The `T-Display-S3-Long` repo's **default branch is `T-Display-S3-Long-cst3530`**, not `main` or `master`. It ships `firmware/factory.bin` **and** `firmware/factory-cst3530.bin` as separate images, and `examples/cst3530_touch/` alongside the original touch example |
| **Reading** | The original Long used the AXS15231B's **integrated** touch. A later run adds/substitutes a discrete **Hynitron CST3530**. LilyGO handled it by making the CST3530 branch the default rather than merging |
| **How to tell** | Flash `factory.bin`; if touch does not respond, flash `factory-cst3530.bin` |
| **Status** | Evidenced by repository structure. No vendor statement located |

### R6 — T-Display-S3 Pro: **V1.0 vs V1.1 backlight driver**

| | |
|---|---|
| **Evidence** | `examples/factory/utilities.h` @ `08b8b2b`, verbatim: `//! Using T-Display-Pro V1.0 , uncomment use V1.1 , //! The difference between V1.0 and V1.1 is the backlight driver.` followed by `#ifdef USING_DISPLAY_PRO_V1 / #define BRIGHTNESS_MAX_LEVEL 255 / #else / #define BRIGHTNESS_MAX_LEVEL 16 / #endif` |
| **What changed** | The backlight brightness scale — **255 levels on V1.0, 16 on V1.1**. Firmware built for the wrong one is 16× off |
| **Second evidence** | The repo ships `firmware/v1.0/` and `firmware/v1.1/` as separate directories |
| **How to tell** | Try the V1.1 firmware; and see the schematics — the Pro repo carries `T-BHI260.pdf` *and* `T-BHI260_V1.1.pdf` |
| **Status** | **Vendor-documented, in a source comment only.** This is the clearest example of the pattern: a real, breaking revision documented nowhere but a `//!` comment |

### R7 — T-Display-S3 Pro: **two different IMU daughter-boards**

The Pro repo ships schematics for both `T-BHI260.pdf` (Bosch BHI260AP) and `T-ICM29048.pdf`
(TDK ICM-20948-class), plus `kicad_sensor.pretty/T-BHI260.kicad_mod` and
`T-CIM29048.kicad_mod`. Firmware named `UnitTest_V1.1_DisChg_BHI260_241111.bin` exists.
**The sensor fitted to your Pro is not determined by the product name.** Scan I²C.

### R8 — The 1.43/1.75″ AMOLED: **three panels, one product page**

Store handle `t-display-s3-amoled-1-64` sells four things: `H708` 1.64″, `H741` 1.43″,
`H741-01` 1.75″, `H741-02` 1.75″ half-circle convex mirror. Two repos cover them. The display
controllers differ (**CO5300/ICNA3311** vs **SH8601**) *and* the touch controllers differ
(**FT3168** vs **CST9217**). Selection is by `CONFIG_SCREEN_TYPE_*` Kconfig symbol —
`DO0143FMST10` (1.43″, CO5300+FT3168), `DO0143FAT01` (1.43″, SH8601+FT3168),
`H0175Y003AM` (1.75″, CO5300+CST9217) — and the header `#error`s if you pick none.
Source: `components/private_library/pin_config.h` @ `87aabe8`.

## How to identify a board you are holding

In increasing order of effort:

1. **Silkscreen.** AMOLED 1.91″ and Pro do carry `V1.0`/`V1.1`/`V2.0`. The base T-Display-S3
   does not.
2. **`esptool.py flash_id`** — distinguishes 4 MB from 16 MB, and reports the USB VID/PID
   (`303A:1001` for native USB-Serial-JTAG).
3. **I²C scan on the board's I²C pins.** This is the single most informative test: it names the
   touch controller (`0x15` CST816S · `0x1A` CST328 · `0x5A` CST226SE/CST3530 family ·
   `0x38` FT3168) and, on PMIC boards, the charger (`0x6B` SY6970/BQ25896 · `0x34` AXP2101).
4. **Flash the vendor factory image and see what it does.** LilyGO ships a
   `t-display-s3-screen-detect` image for exactly this purpose.
5. **Read the chip markings.** The definitive answer, and the only one that would have caught
   R3.

## What this means for anything written about these boards

Every pin map, current figure and library recipe — including everything in this repository —
is **valid for the revision it was derived from and no other**. Each record here states its
commit and retrieval date for that reason. When a source does not state which board it saw,
treat it as describing an unknown member of a set.

## Cross-references

- [Family README §4](README.md#4-family-level-conflicts) — the conflict register
- [`guides/markets/clones-and-variants.md`](../../../guides/markets/clones-and-variants.md) —
  the general method (read; not edited by this pass)
- Per-board `gaps-and-conflicts.md` files
