# Raydium RM69A10 — AMOLED display driver IC

- **Category:** MIPI-DSI AMOLED display driver / timing controller
- **Manufacturer:** **Raydium Semiconductor Corporation** (瑞鼎科技). *Attribution note:* the `RM69xxx` prefix is Raydium's AMOLED driver family (RM67162, RM69090, RM690B0 are the widely documented siblings). **No public RM69A10 datasheet was located on 2026-09-04**; the manufacturer attribution is by family-prefix inference and is labelled as such.
- **Research status:** driven entirely from **vendor BSP source**, not from a datasheet. Evidence class: primary source code, secondary product copy.
- **Retrieved:** 2026-09-04

## 1. What is actually known

| Property | Value | Evidence |
|---|---|---|
| Part marking / driver name | `RM69A10` | S1, S2 |
| Interface | **MIPI DSI**, video mode; the BSP explicitly forces **burst mode** | S3 (`0029-drm-canaan-fix-video-mode-to-burst.patch`) |
| DSI lanes | 2 (the BSP carries a "fix 2lan dsi phy with timeout" patch) | S3 (`0025-…`) |
| Panel resolution as fitted | **RGB 568 × 1232**, 4.1-inch AMOLED | S1, S2 |
| Colour formats driven | XRGB8888 added by patch; **RGB565 is the validated LVGL path** | S3, S4 |
| Backlight | **DSI-command backlight**, not PWM — added by `0049-drm-panel-canaan-universal-add-rm69a10-dsi-backlight.patch` | S3 |
| Linux driver | `panel-canaan-universal` (Canaan's generic DSI panel driver), *not* an upstream `panel-raydium-*` driver | S3 |

## 2. Behaviour worth knowing before you write code

**It is driven by a *generic* panel driver, not a Raydium-specific one.** Canaan's
`panel-canaan-universal` is a table-driven DSI panel driver; the RM69A10 support is a set of
init commands plus timing, added downstream. There is no upstream Linux support and no
`compatible` string outside Canaan's tree.

**Backlight is a DSI command.** There is no backlight PWM pin for the panel — brightness is a
DSI write. A board-level PWM (`GPIO52`/PWM4 on the LilyGO board) exists but drives the
*keyboard* backlight, not the panel. Conflating the two is the obvious mistake.

**Reset must happen in `prepare`, not later.** `0027-panel-canaan-universal-enable-reset-in-prepare.patch`
moves panel reset into the prepare stage; without it the panel does not come up reliably.

**The boot logo and the kernel fight over the framebuffer.** Three separate patches exist to
manage the handoff: `0038-reserve-rm69a10-uboot-logo-fb`, `0051-drm-canaan-preserve-rm69a10-boot-splash-handoff`
and `0043-drm-canaan-defer-vo-config-load-to-vblank`. Expect flicker or a black frame at
handoff if you rebuild without them.

**High refresh needs an automatic PHY setting.** `0042-drm-canaan-rm69a10-use-auto-phy-high-refresh.patch`
plus a diagnostic patch that logs the DSI clock PHY (`0041-…`) exist because getting the DSI
PHY clock right on this panel was evidently not straightforward.

## 3. Unknowns, stated as unknowns

- No datasheet, no register map, no init sequence documentation from Raydium.
- Panel module vendor and part number: unknown.
- Whether the driver IC is Raydium at all rather than a compatible clone: **unverified**.
- Touch is a separate IC ([GT9895](../../goodix/gt9895/README.md)); this record covers display only.

## 4. Used By

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

The only display. 4.1″ AMOLED, RGB 568 × 1232, MIPI DSI from the K230's single DSI output.
`GPIO22` = panel reset, `GPIO25` = panel enable — both used by the U-Boot logo path and by the
Linux bring-up. The board's entire BSP defconfig is named after this panel
(`k230_canmv_t_display_rm69a10_defconfig`) and so are its device trees
(`canaan/k230-canmv-rm69a10`, `canaan/k230-canmv-rm69a10-hdmi`), which is a useful signal that
the panel is the defining feature of the design.

## 5. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | T-Display K230 product page | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230` | 2026-09-04 | "Drive Chip: RM69A10", RGB 568×1232, 4.1″ |
| S2 | T-Display K230 Kit product page | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230-kit` | 2026-09-04 | Same, restated in the kit specification table |
| S3 | `k230_bsp/overlay/buildroot-overlay/linux/*.patch` | LILYGO | primary | source | `https://github.com/Xinyuan-LilyGO/T-Display-K230/tree/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/overlay/buildroot-overlay/linux` | 2026-09-04 | Burst mode, 2-lane PHY, DSI backlight, reset-in-prepare, splash handoff |
| S4 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | same repo | 2026-09-04 | GPIO22 reset / GPIO25 enable; "validated LVGL path uses RGB565" |
