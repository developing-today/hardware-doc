# Diodes Incorporated AP2112K-3.3

- **Category:** 600 mA low-dropout linear regulator, fixed 3.3 V output, with an enable pin and
  short-circuit/thermal protection. SOT-25 / SOT-23-5.
- **Manufacturer:** Diodes Incorporated.
- **Retrieved:** 2026-09-07
- **Sibling record here:** [`pi4ioe5v6408`](../pi4ioe5v6408/README.md)

The 3.3 V regulator of the **LilyGO T-Display-S3**, designator `U7`.

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Schematic part string | **`AP2112K-3.3V(RT9013)`** | designator/part text `OUT 5 U7 AP2112K-3.3V(RT9013)` recovered from `T_Display_S3.pdf` @ `ec889e7` |
| Pins shown | `IN 1`, `GND 2`, `EN 3`, `NC 4`, `OUT 5` | same |
| Alternate part | **RT9013** (Richtek), named in parentheses on the sheet | same |
| Datasheet | **not retrieved by this pass.** Diodes Inc. publishes AP2112 openly at `diodes.com`; acquisition is straightforward and simply was not done | — |
| Local artifact | **none** | — |

**The parenthesised `(RT9013)` is the interesting part.** It is LilyGO explicitly declaring a
**second source**: AP2112K-3.3 and RT9013-33 are pin-compatible SOT-23-5 3.3 V LDOs from
different manufacturers. So the part fitted to any given board **may be either**, and that is
by design rather than by drift — a rare case where LilyGO documented an alternate up front.

Practical difference between the two: AP2112K is rated **600 mA**, RT9013 **500 mA**. Both
comfortably exceed the ESP32-S3's needs, but if you are budgeting the header's 3V rail against
the vendor's stated **100 mA** limit, note that the limit is a *board* figure, not the LDO's.

## 2. Board integration

```
USB-C 5V or VBAT ──→ U7 (AP2112K-3.3 / RT9013) ──→ 3V3 ──┬─→ ESP32-S3, flash   (always on)
                                                          └─→ Q2/Q3 SI2301 gate ──→ V3V rail
                                                                    ▲
                                                               GPIO15
```

The LDO output feeds the SoC directly and, through a P-channel gate controlled by **GPIO15**,
the switched `V3V` rail carrying the panel, the touch controller and the header's 3V pin.
The `EN` pin's control net was **not traced** — the schematic's connectivity was not recovered,
only its designators.

## 3. Gaps

- Datasheet not retrieved for either part.
- **Which of the two is actually fitted is unknown**, and there is no reason to expect
  consistency across production runs.
- `EN` net not traced; whether the LDO itself can be shut down (as opposed to the downstream
  gate) is therefore unknown — and that matters for deep-sleep current.

## 4. Used by

### LilyGO T-Display-S3 / T-Display-S3 Touch — designator `U7`
→ [`devices/lilygo/t-display-s3`](../../../devices/lilygo/t-display-s3/README.md)

Sole 3.3 V regulator. Its output is unswitched to the SoC and switched via GPIO15 to
everything else — which is why the board runs, but shows nothing, when GPIO15 is left low.
See [`features/power-and-battery.md`](../../../devices/lilygo/t-display-s3/features/power-and-battery.md).
