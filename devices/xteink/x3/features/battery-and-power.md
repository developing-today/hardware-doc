# X3 — battery and power

> **650 mAh**, a real TI fuel gauge, and pogo-pin charging. 2026-09-04.

| Item | Value | Evidence |
|---|---|---|
| Battery | **650 mAh**, glued to the back cover, **connectorised** | **[TD]** photos 3 and 4 |
| Fuel gauge | **TI BQ27220** @ I²C **0x55** | **[SDK]**, **[CN]** BOM |
| Charger IC | **TP4056-class** | **[CN]** BOM — *"类似TP4056的电池管理芯片"* |
| Charge connector | **Magnetic pogo pins**; magnets glued to the back cover | **[TD]** photo 3, **[VENDOR]** |
| SD power rail | **GPIO13, active-HIGH** | **[SDK]**, confirmed by factory-firmware RE |
| Device mass | **55 g** | **[VENDOR]** |

## The BQ27220 — a real gauge, unlike its siblings

The X3 has the best battery instrumentation in the family:

| Device | Battery sensing |
|---|---|
| **X3** | **BQ27220** — TI impedance-track gas gauge, no profile upload needed |
| X4 | **Bare ADC** on GPIO0 with a ÷2 divider |
| X4 Pro / X4C | CW2017 — needs an 80-byte BATINFO profile uploaded or it reports 0 % |

`GaugeType::Bq27220`: *"TI command registers, **no profile upload**"*. That makes
it the least fragile of the three. `XteinkDetect` reads SoC from register `0x2C`
and voltage from `0x08`.

**No charger IC on the I²C bus** (`chargerAddr = 0`), so charge state is not
readable over I²C. Unlike the X4 Pro there is also **no charge-STAT GPIO**
declared. How the stock firmware displays charging state is **not established**.

## The SD power rail — and why it exists

```
setup():      digitalWrite(13, HIGH)   // power the card
deep sleep:   digitalWrite(13, LOW)    // cut it
```

Confirmed by X3 factory-firmware reverse engineering. The SDK spells out the
consequence of omitting it:

> "Without declaring it, `powerDownRailsForSleep()` has no X3 SD enable to cut, so
> **the card stays powered through sleep → battery drain.**"

**Polarity trap:** GPIO13 is **active-HIGH** here. The X4 Pro's SD enable (GPIO5)
and the X4 Classic's (GPIO6) are **active-LOW**. And on the [X4](../../x4/features/battery-and-power.md),
GPIO13 is the **battery MOSFET latch** — driving it LOW powers the device off.
**The same pin number means three different things across the family.**

## Pogo charging

The magnets and the pogo pads are **glued to the back cover**, not part of the
PCB — the PCB has silkscreened keep-out areas where the magnets sit
(**[TD]** photo 12). That is a deliberate mechanical design, not an afterthought.

Required accessories, sold separately (2026-09-04):
Magnetic Pogo Pin Charging Cable **$4.99**; Magnetic Charging Adapter **$5.99**.

## The unmeasured measurement

The teardown author's stated purpose was to attach a **Nordic Power Profiler
Kit II** *"to see if I can make any power optimizations to crosspoint firmware"*.

**No results were ever posted.** This is the closest anyone has come to measuring
power on any Xteink device, and it produced nothing. Runtime, sleep current and
active draw are all **unknown**.

## Mechanical fragility

An owner reports the **rear glass cracking**:

> "My glass cracked a bit on the rear side. So it might not have happened if I had
> black x3."
> — [r/xteinkereader `1w56phf`](https://old.reddit.com/r/xteinkereader/comments/1w56phf/), 2026-09-02

The same post asks which models have **metal backing** rather than glass and
**received no authoritative answer**. The teardown confirms the back is glass and
comes off with a heat gun and suction cup — so replacement is feasible, but no
part source is known.

## Status

`hardware-confirmed` for capacity, gauge and SD rail. `unknown` for charger part,
charge-state signalling, runtime and all current draw.
