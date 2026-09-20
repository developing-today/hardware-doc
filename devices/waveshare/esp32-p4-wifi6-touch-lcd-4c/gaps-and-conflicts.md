# Gaps and conflicts — ESP32-P4-WIFI6-Touch-LCD-4C

The 4C shares its PCB, artifacts and every unresolved issue with the 3.4C. The conflict register
is maintained once, in the
[**3.4C gaps-and-conflicts.md**](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md).

## Most relevant entries for this variant

| ID | Issue | Why it matters here |
|---|---|---|
| [C2](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c2--4c-availability--resolved-2026-08-24) | 4C availability — **resolved: it is on sale**, SKU 31522 | Was the defining open question; now closed |
| [C1](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c1--microsd-pin-assignment--resolved-2026-08-24) | microSD pins — **resolved** | Same PCB, same pins |
| [C11](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c11--touch-interrupt-is-not-wired-to-the-soc) | Touch INT not wired — **poll** | Identical |
| [C12](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c12--backlight-has-two-controls-and-the-demos-use-only-one) | Two backlight controls | Identical |
| [C13](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c13--microsd-sits-on-a-switched-rail-no-demo-enables) | microSD rail switched by GPIO45 | Identical |
| [C4](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c4--dsi-porch-timings-are-not-derived-per-panel) | DSI porches reused from the 800 × 800 panel | This board is the one running with the extra slack |
| [C9](../esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c9--community-evidence--resolved-2026-08-26) | No community evidence | Especially acute — no photograph of a real 4C was found |

## 4C-specific

### The Arduino library defaults to the 3.4C

`Arduino/libraries/displays/displays_config.h` sets `CURRENT_SCREEN` to `SCREEN_3INCH_4_DSI` when
undefined. A stock Arduino build therefore configures **800 × 800 on a 720 × 720 panel**.

This is a **trap, not a bug** — the default is correct for the board Waveshare actually sells.
Expect a shifted, wrapped or torn image rather than a blank screen, since the DSI link still
trains. Override before including the header:

```c
#define CURRENT_SCREEN SCREEN_4INCH_DSI
```

### JD9365 register `0x40` = `0x04`

The one byte differing from the 3.4C. **What it controls is unnamed** — the official per-register
datasheet is unobtained, but the controller's architecture and comparable panel tables are now
documented publicly ([JD9365 aggregation](../esp32-p4-wifi6-touch-lcd-3.4c/features/display-controller-jd9365.md)):
the byte sits in a page-0x01 tuning block that varies per panel even within one vendor's lineup. Do not port the 3.4C init table to this panel assuming the difference is cosmetic.

### Pixel density

~255 ppi here versus ~333 ppi on the 3.4C — **derived arithmetic**, not vendor figures. Assets
designed pixel-exact for one variant will not transfer cleanly to the other.
