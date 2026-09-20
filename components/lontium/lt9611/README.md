# Lontium LT9611 — MIPI DSI to HDMI 1.4 bridge

- **Category:** display bridge — MIPI DSI input, HDMI/DVI transmitter output
- **Manufacturer:** **Lontium Semiconductor** (龙迅半导体)
- **Research status:** **presence on the LilyGO board is not confirmed.** This record documents the part and the evidence for and against it being fitted. Do not read it as an assertion that the board has one.
- **Retrieved:** 2026-09-04

## 1. Core facts

| Property | Value |
|---|---|
| Input | MIPI DSI, up to 4 lanes, up to 2 Gbps/lane |
| Output | HDMI 1.4, up to **1080p60** (LT9611**UXC** variant goes to 4K30) |
| Audio | I²S / SPDIF audio embedding into HDMI |
| Control | I²C |
| Typical control pins | `RESET`, `INT` |

## 2. Evidence on the LilyGO T-Display K230

**For:**
- LilyGO's pin map devotes four rows to an "LT9611 HDMI bridge", giving it I²C on `GPIO37`/`GPIO36`,
  IRQ on `GPIO23` and reset on `GPIO24` — all four **shared with the GT9895 touch controller** (S1).
- The BSP ships `0055-riscv-dts-add-rm69a10-hdmi-output-dtb.patch` and
  `0062-riscv-dts-rm69a10-hdmi-use-sdk-v3-baseline.patch`, and the Buildroot config builds a
  third device tree, `canaan/k230-canmv-rm69a10-hdmi` (S2).
- The launcher has a dedicated `ui_hdmi_test.c` page.
- LilyGO's wiki lists **"HDMI 1080P @ 30 FPS"** as a headline feature of both the bare board and
  the Cased Version (S3).
- `lt9611` appears 29 times across the LilyGO tree.

**Against / qualifying:**
- LilyGO's pin map calls it the "**optional** HDMI bridge path" in every row (S1).
- The main `README.MD` says "**HDMI support is kept as a diagnostic feature.** AMOLED remains the
  default display path" (S2).
- **The part is never named in the shop listing** for either the board or the kit.
- The K230 has exactly **one** MIPI DSI output, which is already driving the RM69A10 AMOLED.
  An HDMI bridge on the same DSI cannot run simultaneously with the panel; the separate
  `-hdmi` device tree exists precisely because it is a **boot-time choice**, not a second head.

**Conclusion:** the software supports it, it is a build-time-selected alternative to the AMOLED,
and whether the bridge IC is populated on a given SKU is **unverified**. Tracked as `GC-4` in
[gaps-and-conflicts.md](../../../devices/lilygo/t-display-k230/gaps-and-conflicts.md). Settle it
by `i2cdetect` on the touch bus, or by a photograph of the PCB.

## 3. Used By

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04, presence unconfirmed*

If fitted: I²C on `GPIO37` SDA / `GPIO36` SCL, IRQ `GPIO23`, reset `GPIO24` — **the same four
lines as the GT9895 touch controller**. That sharing is the important integration fact: a reset
of one resets the other, and both must live at distinct I²C addresses on one bus.

## 4. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | Shared I²C/IRQ/reset with touch; "optional" |
| S2 | `README.MD`, `0055-…`, `0062-…`, defconfig `BR2_LINUX_KERNEL_INTREE_DTS_NAME` | LILYGO | primary | source | same repo | 2026-09-04 | HDMI as diagnostic feature; separate DTB |
| S3 | T-Display K230 wiki + Cased Version pages | LILYGO | primary | official wiki | `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/` | 2026-09-04 | "HDMI 1080P @ 30 FPS" |
