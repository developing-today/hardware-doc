# How do I power the DinMeter — and why does it keep switching itself off?

**Applies to:** K134 and K134-V11 (identical power circuit — same schematic bytes).
**Evidence status:** power tree `executed-success` from the schematic; latch behaviour
`reported-working` (vendor documentation, restated identically on both product pages and
independently modelled by Espressif); current figures are **vendor claims with no stated
method**. **Last verified:** 2026-09-04.

---

## The short answer to "why does it switch off"

**GPIO46 is a power latch.** On battery power the board stays alive only while GPIO46 is
**high**. Raise it in `setup()`, first thing:

```cpp
DinMeter.begin(cfg, true);   // M5.begin() raises GPIO46 for you (M5Unified.cpp:282)
```
or, without M5Unified:
```c
gpio_set_direction(GPIO_NUM_46, GPIO_MODE_OUTPUT);
gpio_set_level(GPIO_NUM_46, 1);          // inferred; esp-board-manager: gpio_power_hold, default_level 1
```

On USB it works without this, because USB feeds the rail directly. That is why the bug always
shows up as "it only fails on battery".

---

## Three ways in

| Source | Connector | Range | Path |
|---|---|---|---|
| **DC** | `J1`, 2-pin 2.54 mm screw terminal (`DB2EK-2.54-2P-GN-S`, green) | **6 – 36 V** | `D13`/`D12` → `U1` **ME3116AM6G** buck → `+5VIN` |
| **USB** | USB-C **on the Stamp module** | 5 V | directly onto `+5VIN` |
| **Battery** | `J2`, 1.25 mm 2-pin | 1S Li-ion; 250 mA·h cell bundled | `U2` **TP4057** charger; `Q3`/`Q6` AP40P05 power path; `U3` **SY7088** boost → `+5VOUT` |

Rails produced:

| Rail | From | Feeds |
|---|---|---|
| `+5VIN` | `U1` buck, or USB | Stamp pad 13, `U2` charger, `U7` CN809J supervisor, buzzer `LS1` |
| `+5VOUT` | `U3` boost from `VBAT_OUT` | **both Grove ports**, pin 3 |
| `+3.3V` | `U4` **BL8075CB5TR33** LDO from `VBAT_IN` | RTC `U5`, I²C and encoder pull-ups, LCD `FPC1` |

Note `+3.3V` comes off the **battery** node, not `+5VIN` — which is why the RTC keeps time while
the board is latched off.

## Charging

| Property | Value | Source |
|---|---|---|
| Charger | TP4057 linear, SOT23-6 | schematic `U2` |
| Programme resistor | `R13` = 3.3 kΩ | schematic |
| Charge current | **100 mA** | vendor spec row |
| Float voltage | **4.24 V ±1 %** | TP4057 datasheet — note, *not* 4.20 V |
| Bundled cell | 250 mA·h polymer Li-ion → ~0.4 C | vendor bundle list |
| Status | `CHRG` / `STDBY` pins → indicator LEDs `D1`/`D2`/`D3` | schematic |
| Battery sense | `R7`/`R8` 1 MΩ divider → **GPIO10** (`BATADC`) | schematic |

`DinMeter.Power.getBatteryVoltage()` / `getBatteryLevel()` (M5Unified `Power_Class`, which has a
`board_M5DinMeter` case at `utility/Power_Class.cpp:572`). `reported-working`.

## The latch, precisely

Vendor text, DinMeter v1.1 page (the v1.0 page says the same in different words):

> **Power On:** When powered only by the battery, the device can be woken up by pressing the
> WAKE button or via an RTC scheduled interrupt (IRQ). After the wake-up signal is triggered,
> the initialization program **must set the HOLD (GPIO46) pin to high level (1)** to maintain
> power supply; otherwise, the device will return to sleep.
>
> **Power Off:** When there is no USB external power (battery power only) — (1) press the RST
> button; (2) the program actively sets the HOLD (GPIO46) pin to low level (0).

Circuit: `HOLD` (Stamp pad 27 = GPIO46) → `Q4` **LN2324DT2AG**, which gates the `Q3`/`Q6`
AP40P05 P-channel power path. Wake sources reach the same node through `D4` (from the encoder
button `BTN`) and from the RTC `INT`. **[SCH]**

**Two wake sources, and that is the design.** A panel meter that sleeps at 38.4 µA and wakes on
an RTC alarm to take a reading is exactly what this circuit is for.

## Sleeping

```cpp
DinMeter.Power.timerSleep(5);                              // seconds
// DinMeter.Power.timerSleep(const rtc_time_t&);
// DinMeter.Power.timerSleep(const rtc_date_t&, const rtc_time_t&);
// DinMeter.Power.powerOff();                              // hard shutdown via the latch
```
Verbatim from `M5DinMeter/examples/Basic/wakeup/wakeup.ino` (release 1.0.0). `reported-working`.
`timerSleep` programmes the BM8563 alarm and then releases the latch — so this is not an ESP32
deep sleep, it is a *power-off with an alarm*. That is why the standby figure is microamps
rather than the ~10 µA an ESP32-S3 deep sleep would give plus regulator quiescent.

## Numbers, with their caveats

| Figure | Value | Caveat |
|---|---|---|
| Standby, battery | **DC 4.2 V @ 38.4 µA** | Vendor. **Identical on v1.0 and v1.1** pages, which is consistent with it being dominated by the carrier's latch/LDO rather than by the module |
| DC input | 6 – 36 V | Vendor |
| Charge current | 100 mA | Vendor |
| Grove load | 5 V @ 220 mA per port | Vendor |
| Grove rail, computed | **≈ 5.38 V** from `U3`'s own divider and the formula printed on the sheet | See [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) §6. **Measure before connecting anything 5 V-max** |
| Module sleep (S3 → S3A) | 310.89 µA → **6.84 µA** on `VIN_5V` | Vendor, method unstated. Does not change the *board* standby figure, because the board cuts the battery entirely |

**None of these were measured here.** No instrument, no hardware.

## Safety and design constraints

- **`C24`, the buck input bulk capacitor, is rated 35 V** while the spec ceiling is 36 V. At
  36 V it sits at 103 % of rating. Treat 36 V as an absolute maximum, not an operating point;
  ≤ 30 V continuous is the prudent reading (`inferred` engineering judgement, **not** a vendor
  statement).
- Reverse-polarity Schottkys `D13`/`D12` are fitted but their ratings were not read. Do not rely
  on them.
- The DC terminal is a **screw terminal on a 32 mm-deep body**. Strain-relieve the cable.
- 0 – 40 °C operating range. A sealed panel in direct sun will exceed that.

## Pitfalls

| Symptom | Cause |
|---|---|
| Dies when you let go of the knob (battery) | GPIO46 not held |
| Works on USB, dies on battery | same |
| Won't boot at all after you added a pull-up to GPIO46 | GPIO46 is a strapping pin; high at reset stops the chip booting. Remove it |
| Battery reads 0 V | GPIO10 ADC not configured, or you are reading before `M5.begin()` |
| Grove peripheral browns out | 220 mA per port; the boost is not unlimited |
| Cell charges to 4.24 V, not 4.20 V | TP4057's documented float voltage. Expected |

## Related

[`components/microne/me3116am6g`](../../../../components/microne/me3116am6g/README.md) ·
[`components/generic/tp4057`](../../../../components/generic/tp4057/README.md) ·
[`components/silergy/sy7088`](../../../../components/silergy/sy7088/README.md) ·
[`components/belling/bl8075`](../../../../components/belling/bl8075/README.md) ·
[`rtc-and-timekeeping.md`](rtc-and-timekeeping.md) (the other wake source)
