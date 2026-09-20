# X4 — battery and power

> ADC voltage sense, a MOSFET power latch, **and two board revisions that behave
> differently**. 2026-09-04.

| Item | Value |
|---|---|
| Battery sense | **ADC on GPIO0**, `batteryDividerMultiplier = 2.0` |
| Fuel gauge | **NONE** (`NO_GAUGE`) — unlike the X3 (BQ27220) and X4 Pro (CW2017) |
| Charge status pin | **none** (`batteryChargeStatus = PIN_UNASSIGNED`) |
| Power latch | **GPIO13** — battery MOSFET gate |
| Charging | **USB-C** |
| Capacity | **unknown** — the X3 is 650 mAh by teardown; the X4 is unmeasured |
| Charger IC | unidentified; the X3 uses a *"TP4056-class"* part per its Chinese teardown |

**Battery percentage on the X4 is a voltage estimate through a divider**, with no
coulomb counting and no charge-state signal. It will be less accurate than the X3's
or the Pro's, particularly near the ends of the curve, and it cannot tell you
whether the device is charging.

## The two board revisions — read this before writing power code

Quoted in full because the consequence is severe:

> "GPIO13 gates the battery MOSFET. **Known units self-latch through a pull once
> the power button bridges the rail, so firmware never had to assert it — but at
> least one hardware revision in the field does not self-latch and stays powered
> only while the button is held.** Asserting the latch is a no-op on self-latching
> units. Driving it LOW is the battery power-off."
> — **[SDK]** `BoardConfig.h:868–874`

| | Self-latching revision | Non-self-latching revision |
|---|---|---|
| Firmware never asserts GPIO13 | works | **device powers off when you release the button** |
| Firmware asserts GPIO13 HIGH early | works (no-op) | works |

The revisions are **not externally distinguishable** and no revision marking is
known. **Always assert GPIO13 HIGH in early boot.** It costs nothing on the
majority of units and is the difference between working and unusable on the rest.

To power off: drive GPIO13 **LOW**.

## Sleep

Carried as `power.latch0 = {13}`, driven by the consumer's sleep path. Note the
**same GPIO13 is the SD power enable on the X3** — the X4 explicitly leaves it
alone in SD code. Do not port sleep logic between the two without checking.

The X4 has no SD power enable, so **the card stays powered through sleep**. No
sleep-current measurement exists for this device.

## Related

[`storage.md`](storage.md) · [`../pinouts-and-buses.md`](../pinouts-and-buses.md)
