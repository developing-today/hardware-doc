# Touch — Goodix GT9895

**Question:** *How do I read touch input, and why does resetting HDMI break it?*

| | |
|---|---|
| Controller | [Goodix GT9895](../../../../components/goodix/gt9895/README.md) ("Berlin" family) |
| Bus | I²C3 — `GPIO37` SDA, `GPIO36` SCL |
| Address | **`0x5D`** |
| IRQ / RESET | `GPIO23` / `GPIO24` — **both shared with LT9611** |
| Driver | `CONFIG_TOUCHSCREEN_GOODIX_BRL` (`goodix_berlin`), **built-in** |
| Evidence | `reported-working` |

## Software

Touch is a standard Linux **input** device. LVGL consumes it through the evdev backend; nothing
board-specific is needed in application code.

**Use the right driver.** The BSP sets `CONFIG_TOUCHSCREEN_GOODIX_BRL=y` and explicitly
**disables** `CONFIG_TOUCHSCREEN_GOODIX`. The legacy driver serves GT911/GT9271 and will not
drive a GT9895, even though both answer at `0x5D`. This repository holds
[GT911](../../../../components/goodix/gt911/README.md) and
[GT9271](../../../../components/goodix/gt9271/README.md) records — they are **not**
interchangeable with this part.

LilyGO carries a **307 439-byte** downstream patch, `0034-gt9895-touch.patch`. That size means a
substantially vendored driver, not a device-tree addition. It is the authoritative description
of this controller's behaviour on this board.

## Minimal procedure

```sh
evtest                       # built into the image; pick the Goodix device
cat /proc/bus/input/devices  # confirm it enumerated
i2cdetect -y <bus>           # 0x5D should answer   (launcher: I2C Scan)
```

## Conflicts

**`GPIO23` and `GPIO24` are shared with the LT9611 HDMI bridge.** Anything that resets HDMI
resets touch. In practice the two are already mutually exclusive because they contend for the
single DSI output ([HC-1](../resources-and-conflicts.md)), so this bites only in HDMI diagnostic
mode.

## Limits and unknowns

- **Touch-point count: unknown.** The launcher has a multitouch test page (`ui_multitouch.c`) but
  no source asserts a number.
- Report rate, gesture support, palm rejection, firmware update procedure: **unknown**.
- No Goodix datasheet is public for this part.

## Debugging

No touch at all → check the driver actually bound (`dmesg | grep -i goodix`), then that `0x5D`
answers, then that `GPIO23` is not held by something else. Touch working but coordinates wrong →
axis swap/invert in the device tree, not a driver bug.
