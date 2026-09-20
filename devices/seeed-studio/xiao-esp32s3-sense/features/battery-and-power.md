# Battery and power — XIAO ESP32S3 Sense

> Running untethered, and the two things this board cannot do.
> Snapshot **2026-08-24**. All figures are vendor-published or computed from design files — **nothing was measured**.

## 1. Power architecture

```
USB-C VBUS ──┬── header pin 14 ("5V")
             ├── D2 Schottky ────────────┐
             └── U4 SGM40567 charger ──┐ │
                                       │ │
              BAT+/BAT− pads ── VBAT ──┴─┼── Q1 P-MOS ──┐
                                         │              │
                                         └──────────────┴── VIN
                                                             │
                                              U3 SGM6029 buck-boost
                                                             │
                                                    VCC_3V3 (600 mA max)
```

Source selection between USB and battery is **automatic** — `VBUS` reaches `VIN` through Schottky D2, `VBAT` through P-MOS Q1. You can safely have both connected.

The 3.3 V rail is a **buck-boost**, not an LDO. That matters: a Li-ion cell falls from ~4.2 V to ~3.0 V, crossing 3.3 V. A buck-only regulator would drop out partway through the discharge; this one holds 3.3 V across the full range. Schematic annotates the intended input span as **3.7–5 V**.

## 2. Connecting a battery

**Polarity is not protected. Reversing the cell destroys the board.**

> "The negative terminal of the power supply should be the side **closest to the USB port**, and the positive terminal is the side **away from** the USB port."
> — `XIAO_ESP32S3_Getting_Started.md`

Use a **qualified rechargeable 3.7 V lithium cell**. The pads are on the bottom side (`BAT0` is the `VBAT` test pad in the netlist).

⚠ **When running on battery, there is 0 V on the `5V` header pin.** There is no boost path back to `VBUS`. Anything you power from `5V` dies the moment USB is unplugged.

## 3. Charging

| Property | Value |
|---|---|
| Charger | SG Micro **SGM40567-4.2XG/TR**, linear |
| Float voltage | 4.2 V |
| **Charge current** | **~110 mA** (schematic) / **100 mA** (wiki) — [conflict](../gaps-and-conflicts.md#3-battery-charge-current-110-ma-schematic-vs-100-ma-wiki) |
| Trickle | 0.9 mA (wiki) |
| Set by | **R10 = 220 kΩ**, `I ≈ 24000 / R10(Ω)` |

### Charge LED behaviour — not what you expect

| State | Red LED |
|---|---|
| USB connected, **no battery** | On, then **off after ~30 s** |
| Battery connected, charging | **Flashing** |
| Charge complete | **Off** |

**"Flashing" means charging** here, where most boards use steady-on. And "off" is ambiguous — it means either fully charged or no battery. This is a frequent source of "is it even charging?" confusion.

### Changing the charge current

R10 programs it, so ~110 mA is not fixed:

| R10 | Implied current |
|---|---|
| 330 kΩ | ~73 mA |
| **220 kΩ (stock)** | **~110 mA** |
| 150 kΩ | ~160 mA |
| 110 kΩ | ~218 mA |

At ~110 mA a 1000 mAh cell takes roughly 10 hours, which is why people attempt this. **Cautions:** it is a *linear* charger, so the extra power becomes heat in a 0.92 × 1.16 mm WLCSP on a 21 mm board; and this is **`inferred` from a schematic annotation, untested**.

## 4. You cannot read the battery voltage

Vendor-confirmed:

> "Since all GPIO pins of the XIAO ESP32-S3 are assigned their own functions, we do not have a GPIO configured for the battery pin. This means that we **cannot get the battery voltage at the software level** by reading the analog value of one of the GPIOs."

The netlist corroborates: the `VBAT` net has exactly four members — the battery pad, C26, Q1 and the charger. **No divider, no ADC path.**

Any tutorial claiming `analogRead()` gives you battery voltage on a XIAO ESP32S3 is describing a **different XIAO** — the nRF52840 variant does have one.

### Adding it yourself

The standard approach is a resistor divider from `BAT+` into a free ADC1 pin (`D0`–`D3` = GPIO1–4 are unused):

```
BAT+ ──[ R1 ]──┬──[ R2 ]── GND
               │
             D0 (GPIO1, ADC1_CH0)
```

With R1 = R2 = 100 kΩ you halve 4.2 V to 2.1 V, comfortably inside ADC1's range.

**Watch the quiescent drain.** A 2 × 100 kΩ divider across 4.0 V draws **20 µA continuously** — comparable to the *vendor-claimed* deep-sleep budget (~34 µA), though [the real figure with a camera is far higher](deep-sleep.md). For a sleeping design, either use much larger resistors (1 MΩ each ≈ 2 µA, at the cost of ADC accuracy) or switch the divider with a MOSFET from a GPIO so it only draws current while sampling.

Also calibrate: ESP32-S3 ADC readings are not precise without correction, and `esp_adc_cal` / `analogReadMilliVolts()` exist for this reason.

> Status: **`inferred`** — a standard technique, consistent with the pin map and the vendor's own suggestion to "connect the positive and negative terminals of the battery to two of the pins". Not built or verified here.

## 5. Consumption figures

Vendor-published. **Not measured here.**

| Mode | XIAO ESP32S3 | **Sense** |
|---|---|---|
| Modem-sleep | 27 mA | 31.6 mA @ 3.8 V |
| Light-sleep | 2 mA | 2.45 mA @ 3.8 V |
| **Deep-sleep** | **14 µA** | **33.51 µA @ 3.8 V** |
| Webcam, average | — | ~155 mA @ 3.8 V |
| Webcam, peak (capture) | — | ~366 mA @ 3.8 V |
| Mic record + SD write, avg | — | 64.5 mA @ 3.8 V |
| Mic record + SD write, peak | — | 109.3 mA @ 3.8 V |

### The deep-sleep number is contested

Seeed publishes **three mutually inconsistent** low-power figures for the Sense:

| Figure | Source |
|---|---|
| **33.51 µA** | wiki spec table |
| **3 mA** | wiki spec table, different row |
| **26.5 mA** | XIAO Reference Design catalogue, p.12 |

Plan around **~34 µA**, but **verify on your own hardware** before making a battery-life claim. See [`../gaps-and-conflicts.md` §4](../gaps-and-conflicts.md#4-seeeds-own-spec-table-gives-two-different-deep-sleep-figures-for-the-sense).

### Why the Sense sleeps worse than the bare board

**Vendor figures: ~34 µA vs 14 µA — about 2.4×.** ⚠ *In practice it is far worse — see [`deep-sleep.md`](deep-sleep.md).* The cause is architectural: the camera has **no `PWDN` line** ([`camera.md` §3.1](../pinouts-and-buses.md#31-there-is-no-camera-power-down-or-reset-line--and-that-has-consequences)). It draws its idle current whenever the 3.3 V rail is up, and there is no way to switch it off in software.

If your design is "wake hourly, take a picture, sleep", that residual draw is the dominant term.

## 6. Runtime estimates

Computed from the vendor figures above. **Arithmetic only** — no measurement, no real-world derating for cell ageing, temperature, or self-discharge.

| Cell | Deep sleep @ 34 µA *(vendor claim — see [`deep-sleep.md`](deep-sleep.md))* | Mic+SD @ 64.5 mA | Webcam @ 155 mA |
|---|---|---|---|
| 250 mAh | ~10 months | ~3.9 h | ~1.6 h |
| 500 mAh | ~1.7 years | ~7.8 h | ~3.2 h |
| 1000 mAh | ~3.4 years | ~15.5 h | ~6.5 h |
| 2000 mAh | ~6.7 years | ~31 h | ~12.9 h |

The multi-year sleep figures are theoretical — lithium self-discharge and the charger's own leakage will bound real life well before then. Treat them as "sleep current is not your problem", not as a shelf-life prediction.

Duty-cycled designs land between the columns. A wake-capture-sleep cycle is dominated by how long the camera is powered, which includes sensor start-up and auto-exposure settling on **every** wake, since the sensor loses no state but the board still boots.

## 7. Rail limits

| Rail | Limit | Notes |
|---|---|---|
| `VCC_3V3` | **600 mA** (SGM6029) | Shared by SoC, flash, camera (98–140 mA), mic, microSD |
| `3V3` header pin | output | **Do not back-feed** |
| `5V` header pin | USB host | 0 V on battery |
| Charge | ~110 mA | R10-programmed |

Worst case — Wi-Fi TX burst + OV5640 (140 mA) + SD write — leaves limited margin. Budget accordingly before hanging peripherals off `3V3`.

## 8. Sleep in practice

> **See [`deep-sleep.md`](deep-sleep.md) for the full treatment** — including owner-measured currents, the sensor-standby workaround that cuts deep sleep ~26x, and the `while(!Serial);` trap. The summary below is the short version.

```cpp
#include "esp_sleep.h"

esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);   // 60 s
esp_deep_sleep_start();                              // never returns
```

Notes specific to this board:

- **Deep sleep resets the SoC on wake.** Execution restarts at `setup()`; only RTC memory survives. Seeed's own SD example notes that this means the serial monitor must be reopened after each wake — the USB CDC device disappears and re-enumerates.
- **USB CDC and deep sleep interact badly during development.** The port vanishing is expected, not a fault. See [`../development.md` §5](../development.md#5-usb-serial-and-recovery).
- **You cannot power down the camera** before sleeping. The vendor's ~34 µA is optimistic by orders of magnitude once the camera has been initialised — [`deep-sleep.md`](deep-sleep.md) has measured figures and the mitigation.
- GPIO wake sources must be RTC-capable pins; with the daughterboard fitted your free-pin choice is narrow.

## 9. Related

- [SGM40567 charger](../../../../components/sgmicro/sgm40567/README.md) · [SGM6029 buck-boost](../../../../components/sgmicro/sgm6029/README.md)
- [`../pinouts-and-buses.md` §8](../pinouts-and-buses.md#8-power-tree) · [`../resources-and-conflicts.md` §5](../resources-and-conflicts.md#5-power-budget)
- [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) — the contested figures
