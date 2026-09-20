# T-Display-S3 — power, battery and charging

> The single highest-value page for this board. Most "dead board" reports resolve here.

## 1. The GPIO15 gate — read this first

```cpp
pinMode(15, OUTPUT);
digitalWrite(15, HIGH);   // enables the V3V rail: panel, 3V header pin, peripherals
```

> "**Note:** GPIO15 is the peripheral power control pin. You must set it HIGH before using the
> board, otherwise the LCD and other peripherals will not work."
> — `README.md` @ `ec889e789b3cf093412689a143f7f37b42b56af7`

**Why it only bites on battery:** the LDO output is present whenever USB is attached, so a
board on a desk works with or without the line. Unplug it and the gate matters. This produces
the classic report *"works on USB, dead on battery"* — [issue #79](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/79)
exists solely because of it, and a commenter's summary is worth quoting:

> "it is so ridiculous there is nothing mentioned on their site about pulling pin 15 high to
> get it to power on when using the little jst battery input." — 2023-10-06

**Free diagnostic:** the **green LED** sits on the `V3V` rail. On battery, green off = GPIO15
low. On USB it is always on, which is why the LED does not help you at the desk.

**It applies in MicroPython too**, and there is no `setup()` to hide it in — see
[`../development.md`](../development.md#6-micropython-and-other-languages).

## 2. Power topology

```
USB-C (U5) ── 5V ──┬─→ charger U6 ──→ VBAT ─┬─→ LDO U7 (AP2112K-3.3) ──→ 3V3 (SoC, always on)
                   │                        │
JST 1.25mm ────────┴────────────────────────┘        └─→ Q2/Q3 (SI2301) gate ──→ V3V rail
                                                          ▲                        │
                                                     GPIO15                        ├→ LCD panel
                                                                                   ├→ 3V header pin
                                                                                   └→ green LED8
```

Designators from `schematic/T_Display_S3.pdf` @ `ec889e7`. **The gate's exact wiring was not
traced** — see [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) K1.

| Rail | Value | Notes |
|---|---|---|
| USB-C input | 5 V | the **only** charger input; `VBUS` is not on the header |
| Battery | 3.7–4.2 V, JST **1.25 mm** 2-pin | polarity is not standardised across vendors — **check before plugging in** |
| Header `VBUS` pin | 5 V **out**, sourced from USB-C | capacity = whatever your USB supply gives |
| Header `VBAT` pin | 4.2 V | |
| Header `3V` pin | 3.3 V, **≤ 100 mA** | vendor figure. Gated by GPIO15 |

## 3. Charging

| | |
|---|---|
| Charger | `U6`; schematic says **TP4065**, a shipping board carried a 5-lead TSOT-23 marked `65b311` — [G2](../gaps-and-conflicts.md#g2--charger-part-number-vs-shipping-hardware) |
| Current | README: **500 mA**. Schematic note: **`R13 IBAT (mA) = 580`** with a 2 kΩ program resistor. Unresolved |
| Indicator | **red LED1** — *flashes or glows dimly with no battery*, solid while charging, off when full |
| Protection | **none on board.** LilyGO maintainer, 2025-02-06: *"No built-in battery protection, needs to be used with a lithium-ion battery with battery protection"* |
| Path management | none evidenced. There is no PPM/power-path IC; this is a plain linear charger |

<a id="changing-the-charge-current"></a>
### Changing the charge current

The commonly cited procedure — replace the 2 kΩ `PROG` resistor with 10 kΩ for ≈130 mA — comes
from the **TP4056/TP4065 datasheet equation** (I = 1200 V / R<sub>PROG</sub>) applied to the
published schematic. **It may not describe the part actually fitted** (G2). LilyGO's README
points at [issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230) for this.

If you must: identify `U6` on your board *first*, read the marking, and find the datasheet for
that part. Do not desolder on the strength of a PDF that a careful owner has already shown to
disagree with hardware.

### Why this matters for the shell

LilyGO sells the board with a shell and a **700 mAh** battery (`K204-01`, `K206-01` — both
out of stock 2026-09-07). Cells that physically fit third-party shells are commonly
**350–400 mAh**, and 500–580 mA into a 350 mAh cell is **1.4–1.7 C** — above the 1 C most
datasheets allow. That is precisely the concern that opened issue #230.

Community-reported working combination (firsthand ownership, 2026-08-30, r/esp32): *MakerFocus
3.7 V 1000 mAh LiPo #952540*, in a printed
[battery backpack for the LilyGO shell](https://www.printables.com/model/1065538-lilygo-t-display-s3-shell-battery-backpack).
At 1000 mAh, 580 mA is a comfortable 0.6 C.

## 4. Powering from anything else

- **You cannot charge from the 5 V pin.** `VBUS` is not brought out.
  [Issue #42](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/42), 2022-11-07; LilyGO's
  answer was to solder a wire to `VBUS`. Still true in 2026.
- **Feeding 5 V into the 5 V pin back-powers the charger input.** Firsthand report, 2023-11-01:
  *"The charging voltage jumps up to 5V, because of backpowering. If you're using an
  unprotected battery it might blow up in this case!"* — one owner, not independently
  reproduced, but consistent with the topology.
- **3.3 V into the 3V pin** is discussed in [issue #205](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/205);
  the answers there are community, not vendor, and involve back-feeding an LDO output. Treat
  as unsupported.
- **The supported inputs are USB-C and the JST connector.** Anything else is a modification.

## 5. Consumption

**No measurement exists in this record.** LilyGO publishes current figures for its AMOLED
boards and **not** for this one. For scale, the same-SoC AMOLED boards are documented at
*"(240MHz) WiFi On 90~230+ mA"* active and *"About 230uA"* in deep sleep — that is a different
board with a different display and different regulators, and is offered as an order of
magnitude only. See [`deep-sleep.md`](deep-sleep.md) and
[`../performance.md`](../performance.md).

## Cross-references

[`battery-voltage-measurement.md`](battery-voltage-measurement.md) ·
[`usb.md`](usb.md) · [`deep-sleep.md`](deep-sleep.md) ·
[`../../t-display-s3-shared/board-revision-drift.md`](../../t-display-s3-shared/board-revision-drift.md)
