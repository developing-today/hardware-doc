# Goodix GT9895 — capacitive touch controller ("Berlin" series)

- **Category:** projected-capacitive touchscreen controller, I²C
- **Manufacturer:** Goodix (汇顶科技)
- **Research status:** no public GT9895 datasheet located on 2026-09-04. Everything below is from **Linux driver evidence** and vendor BSP configuration.
- **Retrieved:** 2026-09-04

## 1. Identity and driver

| Property | Value | Evidence |
|---|---|---|
| Part | **GT9895** | S1, S2 |
| Family | Goodix **"Berlin"** — the modern large-panel generation, not the GT911/GT9271 generation | S3 |
| Linux driver | `CONFIG_TOUCHSCREEN_GOODIX_BRL` (`goodix_berlin`) | S3 |
| **Not** the legacy driver | `CONFIG_TOUCHSCREEN_GOODIX` is explicitly **disabled** in the same fragment | S3 |
| Bus | I²C | S1 |
| 7-bit address as used | **`0x5D`** | S1 |
| Signals | SDA, SCL, IRQ, RESET | S1 |

## 2. Why the family distinction matters

This repository already holds [GT911](../gt911/README.md) and [GT9271](../gt9271/README.md).
**Do not treat GT9895 as a drop-in for either.** They are different generations with different
Linux drivers, different register maps and different firmware-download behaviour:

| | GT911 / GT9271 | **GT9895** |
|---|---|---|
| Linux driver | `goodix` (`drivers/input/touchscreen/goodix.c`) | **`goodix_berlin`** (`goodix_berlin_core.c` + `_i2c.c`/`_spi.c`) |
| Kconfig | `TOUCHSCREEN_GOODIX` | `TOUCHSCREEN_GOODIX_BRL` |
| Typical addresses | `0x5D` / `0x14` | `0x5D` |
| Config/firmware | config table written over I²C | Berlin-style firmware + config binary |

The addresses overlap at `0x5D`, which is precisely why the mistake is easy to make: an I²C
scan cannot tell them apart. The driver choice can.

## 3. Board-level behaviour on the K230

The LilyGO BSP builds the Berlin driver **in-tree** (not as a module) and carries a very large
downstream patch — `0034-gt9895-touch.patch`, **307 439 bytes** — which is far larger than a
bring-up patch and indicates a substantially vendored driver rather than a device-tree
addition. That patch is the authoritative description of this part's behaviour on this board.

**The IRQ and reset lines are shared with the optional LT9611 HDMI bridge** (`GPIO23` IRQ,
`GPIO24` reset). Anything that resets HDMI resets touch. See
[resources-and-conflicts.md](../../../devices/lilygo/t-display-k230/resources-and-conflicts.md).

## 4. Unknowns

- No datasheet, no register map, no maximum I²C rate, no supply limits from Goodix.
- Reported touch-point count and panel size support: unknown from primary sources; the
  launcher has a `ui_multitouch.c` test page but the point count is not asserted anywhere
  authoritative.
- Alternative I²C addresses: unknown.

## 5. Used By

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

Touch controller for the 4.1″ RM69A10 AMOLED. I²C3 on **`GPIO37` SDA / `GPIO36` SCL** at
**`0x5D`**, IRQ on **`GPIO23`**, reset on **`GPIO24`**. Both interrupt and reset are physically
shared with the LT9611 HDMI path on this board.

## 6. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | Address `0x5D`, GPIO36/37/23/24, shared IRQ/reset with LT9611 |
| S2 | T-Display K230 wiki page | LILYGO | primary | official wiki | `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/` | 2026-09-04 | "GT9895 capacitive touch" |
| S3 | `k230_bsp/overlay/buildroot-overlay/linux/linux.fragment` and `0034-gt9895-touch.patch` | LILYGO | primary | source | same repo | 2026-09-04 | `TOUCHSCREEN_GOODIX_BRL=y`, legacy `TOUCHSCREEN_GOODIX` disabled, 307 KB vendored driver patch |
