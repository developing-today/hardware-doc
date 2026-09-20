# Display — 4.1″ AMOLED, 568 × 1232

**Question:** *How do I draw on the screen, control brightness, and stop the boot logo from
fighting the kernel?*

| | |
|---|---|
| Panel driver IC | [Raydium RM69A10](../../../../components/raydium/rm69a10/README.md) |
| SoC path | [K230](../../../../components/canaan/k230/README.md) **MIPI DSI**, 2-lane, video mode, **burst** |
| Resolution | RGB **568 × 1232**, 4.1 inch |
| Control pins | `GPIO22` reset · `GPIO25` enable |
| Backlight | **DSI command**, not PWM |
| Applicable revision | all SKUs `K256*`, `K277` |
| Evidence | `reported-working` — LilyGO BSP; **not** hardware-verified here |

## Hardware path

K230 MIPI DSI (the SoC's **only** DSI output) → RM69A10 → AMOLED. Because there is exactly one
DSI, the [LT9611 HDMI bridge](../../../../components/lontium/lt9611/README.md) is a **boot-time
alternative**, never a second head — see [`resources-and-conflicts.md`](../resources-and-conflicts.md) HC-1.

## Software stack

Standard Linux DRM/KMS. Panel driver is Canaan's **`panel-canaan-universal`** — there is no
upstream `panel-raydium-*` for this part, and no upstream `compatible` string. Userspace is
**LVGL** through the DRM backend.

LVGL is pinned in Buildroot at upstream commit `59dc7e436ae97a25e32656739ea6a943f9f11b6a` with
four LilyGO patches, two of which are display-related:

- `0002-lvgl-linux-drm-add-k230-plane-rotation.patch`
- `0004-lvgl-drm-add-k230-staging-scanout-buffer.patch`

## Minimal procedure

The panel is already up when Linux hands off to userspace. To draw:

1. Open the DRM device and pick the connector the RM69A10 is on.
2. **Use RGB565.** LilyGO: *"The validated LVGL path uses RGB565 for stable refresh."* XRGB8888
   works (added by `0026-drm-canaan-vo-add-xrgb8888-format.patch`) but is not the validated path.
3. For rotation, use the **GDMA** engine rather than CPU rotation —
   `0035-gdma-xrgb8888-rotation.patch` and the LVGL plane-rotation patch exist for exactly this.

Diagnostics already on the board: launcher → **Display Test** (`ui_display_test.c`),
`drm_motion_probe.c`, `lvgl_scroll_probe.c`.

## Resources consumed

MIPI DSI (all of it), `GPIO22`, `GPIO25`, one DRM plane, and a framebuffer. A 568 × 1232 RGB565
framebuffer is **1.40 MB**; double-buffered, 2.80 MB. Against 1 GB of LPDDR4 that is
inconsequential — unlike on an MCU-class part.

## Alternatives and decision table

| Approach | When |
|---|---|
| **LVGL over DRM** (LilyGO's) | Default. Widgets, fonts, input integration all done. |
| Raw DRM/KMS + your own drawing | You want full control or a different UI toolkit. |
| Framebuffer (`/dev/fb0`) | `DRM_FBDEV_EMULATION`, `FB` and `FRAMEBUFFER_CONSOLE` are all enabled, so a legacy fbdev app works. Simplest, slowest. |
| Console on the panel | `getty-tty1-rm69a10` in the rootfs overlay puts a login shell on the AMOLED with the `TER16x32` font. Genuinely useful for bring-up. |
| **HDMI via LT9611** | Diagnostics only; requires the `-hdmi` device tree and gives up the AMOLED. |

## Initialisation, teardown, handoff

**The boot-logo handoff is the fiddly part** and three patches exist for it:

- `0038-reserve-rm69a10-uboot-logo-fb` — reserve the U-Boot framebuffer so Linux does not stomp it
- `0051-drm-canaan-preserve-rm69a10-boot-splash-handoff` — keep the splash across the handoff
- `0043-drm-canaan-defer-vo-config-load-to-vblank` — load video-output config on vblank

U-Boot draws the logo itself: `display_logo.c` (32 KB), `k230_logo.c`, plus `logo.xrgb` (2.8 MB)
and `logo.yuv` (1.0 MB) in the rootfs overlay. If you rebuild U-Boot without the overlay you get
a blank screen until the kernel comes up.

`0027-panel-canaan-universal-enable-reset-in-prepare` moves panel reset into `prepare` — without
it the panel does not come up reliably.

## Limits

| Limit | Value | Class |
|---|---|---|
| DSI output count | **1** | silicon |
| Max DSI resolution | 2 MP @ 60 fps | silicon |
| Panel | 568 × 1232 fixed | board |
| Validated colour format | RGB565 | framework/board (LilyGO's word) |
| Refresh rate | not published | **unknown** |
| Brightness range/steps | not published | **unknown** |
| Measured frame rate | none published | **unmeasured** |

## Pitfalls

1. **Do not look for a backlight PWM for the panel.** `GPIO52`/PWM4 is the **keyboard** backlight.
2. Rebuilding without the display patch set gives flicker, a black handoff, or a dead panel.
3. Video mode must be **burst** (`0029-drm-canaan-fix-video-mode-to-burst`).
4. Colour swap bugs were real and are fixed by patch — `0030` (XRGB8888 opaque + RB swap) and
   `0033` (RGB2YUV colour swap). If you port to a different kernel, expect them back.

## Unresolved

Refresh rate, brightness curve, panel module vendor, actual measured LVGL frame rate. See
[`GC-5`](../gaps-and-conflicts.md).
