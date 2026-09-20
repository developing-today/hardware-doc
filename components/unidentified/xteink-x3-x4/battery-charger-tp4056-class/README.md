# "TP4056-class" Li-ion charger — Xteink X3 (part unresolved)

- **Category:** single-cell Li-ion linear charge-management IC.
- **Manufacturer / part:** **unknown.**
- **Research status:** ⚠ **One source, and that source hedges.**
- **Retrieved:** 2026-09-04

## What is established

Exactly one line of evidence:

> 类似TP4056的电池管理芯片
> *"a battery-management chip similar to the TP4056"*
> — [`sunwoods/Xteink-X3`](https://github.com/sunwoods/Xteink-X3) BOM, firsthand teardown

**The author explicitly wrote "similar to", not "is".** This record preserves that
hedge rather than laundering it into a part number.

The TP4056 is an extremely widely second-sourced Chinese linear charger
(constant-current/constant-voltage, ~1 A programmable, SOP-8 with thermal pad,
`CHRG`/`STDBY` open-drain status outputs). "TP4056-class" therefore describes a
**category of interchangeable parts**, not a specific one — which is probably why
the teardown author phrased it that way.

## What is missing

- **The part number**, and therefore the programmed charge current, float voltage,
  thermal-regulation behaviour and whether it has a battery-temperature input.
- **Whether it exposes a status line to the SoC.** The X3's board profile declares
  **no `batteryChargeStatus` GPIO** — unlike the
  [X4 Pro and X4 Classic](../../../cellwise/cw2017/README.md), which read a charge
  `STAT` line on GPIO21. So either the X3's charger status is unconnected, or it
  is connected to a pin the SDK has not identified.
- **Whether the X4 uses the same part.** No X4 teardown exists.

## Why the missing status line is interesting

The X3 has the family's best battery *gauge*
([BQ27220](../../../texas-instruments/bq27220/README.md)) and, apparently, **no
charge-state signal at all**. The BQ27220 *can* report charge/discharge direction
through its flags register — which no Xteink firmware reads — so the stock
firmware may derive charging state from the gauge rather than a GPIO. **Not
established.**

Note also the physical evidence that a charge indicator exists: an owner
describes *"the XTEINK where the **led glows red while charging**"* on the back of
the device ([r/XTEINK `1vkuhbi`](https://old.reddit.com/r/XTEINK/comments/1vkuhbi/),
2026-08-10, firsthand). A TP4056-class part drives exactly such an LED from its
`CHRG` pin **without host involvement** — which would explain both the LED and the
absent GPIO.

That is a coherent hypothesis, and it is **not** confirmed.

## What would resolve it

A legible top-marking photograph. The archived teardown includes chip close-ups
explicitly captioned *"at an angle to better read the chip labels"* —
**not examined at full resolution.**
See [`devices/xteink/x3/media.md`](../../../../devices/xteink/x3/media.md).

---

## Used By

### [Xteink X3](../../../../devices/xteink/x3/README.md)

Charges a **650 mAh** connectorised cell over the **magnetic pogo-pin
connector**. Drives a red charge LED visible through the back cover on at least
some units. No charge-status GPIO is declared in the board profile.

→ [`devices/xteink/x3/features/battery-and-power.md`](../../../../devices/xteink/x3/features/battery-and-power.md)

### [Xteink X4](../../../../devices/xteink/x4/README.md) — **assumed, not evidenced**

The X4 charges over **USB-C** and no teardown of it exists. Whether it carries the
same charger is **unknown**. Recorded here only so the assumption is visible
rather than silent.

## Contrast

A fully identified charger of the same class is documented elsewhere in this
repository at [`components/generic/tp4057`](../../../generic/tp4057/README.md)
(M5Stack DinMeter) — useful as a reference for what this record would contain if
the part were known.
