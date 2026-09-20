# T-Display-S3 — touch (Touch SKU only)

| | |
|---|---|
| Fitted on | `H587` / `H589` "Touch" SKUs and the `H717`-style shell bundles. **Not** on `H569`/`H577` |
| Controller | **Hynitron CST816S** (early boards) or **CST328** (later) — see [revision R1](../../t-display-s3-shared/board-revision-drift.md#r1--t-display-s3-touch-cst816s--cst328) |
| Bus | I²C on **GPIO17 (SCL) / GPIO18 (SDA)**, 10 kΩ pull-ups fitted on board |
| Address | **`0x15`** (CST816S) · **`0x1A`** (CST328) |
| IRQ / RST | **GPIO16** (`TOUCH_INT`) / **GPIO21** (`TOUCH_RES`) |
| Component records | [`hynitron/cst816d`](../../../../components/hynitron/cst816d/README.md) (CST816 family) · [`hynitron/cst328`](../../../../components/hynitron/cst328/README.md) |

## The generation split, and the single flag that decides it

LilyGO's `platformio.ini` @ `ec889e7` carries, in the **shared** `[env]` section:

```ini
build_flags =
    …
    -DTOUCH_MODULES_CST_MUTUAL
```

`TouchLib` uses this to select the **mutual-capacitance** driver — the CST328 branch. The
alternative is `-DTOUCH_MODULES_CST_SELF` for the self-capacitance **CST816S**. Get it wrong
and the driver probes the wrong address with the wrong register semantics, and reports **no
touch controller found** — which is exactly [issue #125](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/125)
(15 comments, "no Touch IC found").

**The evidence that both generations exist** is that the board repository ships **both**
register documents:

| File in `datasheet/` @ `ec889e7` | Bytes | Now filed at |
|---|---|---|
| `CST816S寄存器说明-20190508.pdf` | 76 816 | [`components/hynitron/cst816d/artifacts/`](../../../../components/hynitron/cst816d/artifacts/cst816s-register-guide-cn-20190508-lilygo-mirror.pdf) |
| `CST328数据手册V2.2.pdf` | 1 297 291 | [`components/hynitron/cst328/artifacts/`](../../../../components/hynitron/cst328/artifacts/cst328-datasheet-cn-v2.2-lilygo-mirror.pdf) |

A board with one controller does not need two register manuals.

## Identify your board in 30 seconds

Run `examples/I2CScan/I2CScan.ino` from the repo, or any I²C scanner on GPIO17/18:

```
0x15 → CST816S  → build with -DTOUCH_MODULES_CST_SELF
0x1A → CST328   → build with -DTOUCH_MODULES_CST_MUTUAL   (LilyGO's current default)
nothing → you have a non-touch board, or GPIO15 is low
```

That last line matters: **the touch controller is on the gated `V3V` rail**, so an I²C scan
with GPIO15 low finds nothing and looks like a hardware fault.

## Minimal use

LilyGO's `examples/touch_test/touch_test.ino` and `examples/CapacitiveTouch/` @ `ec889e7` are
the reference. Both include a `pin_config.h` with `PIN_TOUCH_INT 16` / `PIN_TOUCH_RES 21` and
drive reset before probing.

Reset sequence matters: hold `TOUCH_RES` low ≥ 10 ms, release, wait ≥ 50 ms, then probe. Many
"intermittent touch" reports are a missing reset.

## Known problems

- **Constant I²C errors with nothing else on the bus** —
  [issue #168](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/168) (21 comments,
  2023-06-29). The CST parts NAK aggressively while asleep; the driver must tolerate it rather
  than treating a NAK as a fault.
- **Touch works under Arduino but not ESP-IDF** —
  [issue #156](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/156). `TouchLib` is an
  Arduino library; ESP-IDF users need `LilyGo-Display-IDF` or their own driver.
- **GPIO16 is pulled up even on non-touch boards** — see
  [`../pinouts-and-buses.md`](../pinouts-and-buses.md#5-gpio16--gpio17-are-not-free). Do not
  infer "touch fitted" from a high GPIO16.

## Resource cost

GPIO16, GPIO17, GPIO18, GPIO21 — four pins, of which two (17/18) are the board's only I²C bus
and are shared with the SH1.0 external connector. Adding an external I²C sensor means sharing
with the touch controller; that works (different addresses) but the CST parts' NAK behaviour
can confuse naive bus scanners. See [issue #181](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/181).
