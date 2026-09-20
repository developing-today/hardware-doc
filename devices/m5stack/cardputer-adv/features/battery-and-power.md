# Cardputer ADV — battery and power

> **Question:** *"How do I read the battery, charge it safely, and make it last?"*
> ADV specifics; the v1.x power train uses the **same parts** but a different battery topology.
> Verified **2026-09-04**. Nothing in this file was measured.

## The power train

```
USB-C (Stamp-S3A) ─ F1 6V/1A PPTC ─► +5VIN ─┬─► D1 SS34 ─► VBAT_OUT
                                            └─► U1 TP4057 charger ─► BAT ─► J8 (1750 mAh cell)
                                                   R1 0.8 Ω sense, R5 3.3 kΩ PROG
 VBAT_IN ─► U3 CN809J supervisor ─► RESET (R7 100 kΩ)
 VBAT_OUT ─► R2 0 Ω ─► U2 SY7088 boost (L1 3015 1.5 µH, FB R4 75 k / R6 22 k) ─► +5VOUT
 VBAT_OUT ─► Q1/Q2/Q3 LP3218DT1G power path
 +5VOUT   ─► U4 SY8089 buck  (L2 4.7 µH, FB R11 100 k? / R12 68 k / R13 15 k) ─► +3.3V
 SW1 SW-SPDT = the side power switch;  SW2 SW-SPDT;  BTN1/BTN2 SW-PB
```

| Part | Designator | Role | Record |
|---|---|---|---|
| TP4057 | U1 | Li-ion linear charger, `PROG` = R5 3.3 kΩ | [`generic/tp4057`](../../../../components/generic/tp4057/README.md) |
| CN809J | U3 | voltage supervisor / reset generator | [`consonance/cn809`](../../../../components/consonance/cn809/README.md) |
| SY7088 | U2 | boost → `+5VOUT` | [`silergy/sy7088`](../../../../components/silergy/sy7088/README.md) |
| SY8089 | U4 | buck → `+3.3V` | [`silergy/sy8089`](../../../../components/silergy/sy8089/README.md) |
| LP3218DT1G | Q1–Q3 | power-path MOSFETs | [`unidentified/cardputer/lp3218dt1g`](../../../../components/unidentified/cardputer/lp3218dt1g/README.md) |
| SS34 | D1, D2 | Schottky | — |
| JW5712 | Stamp U4 | 3.3 V buck on the module, 0–0.6 A | [`joulwatt/jw5712`](../../../../components/joulwatt/jw5712/README.md) |
| AW35122FDR | Stamp U2 | `BL_3V3` load switch | [`awinic/aw35122`](../../../../components/awinic/aw35122/README.md) |

**R3 (1 kΩ) and D3 (an LED) on sheet 1 are drawn greyed out — depopulated.** A charge-status
indicator that the production board does not fit. That is a positive DNP marking, not an
omission.

## Inferred rail voltages

The sheet prints its own formula next to the SY7088: `Vout = 1.2 V × (R1/R2 + 1)`.

| Rail | Divider | Computed | Status |
|---|---|---|---|
| `+5VOUT` | R4 75 kΩ / R6 22 kΩ | 1.2 × (75/22 + 1) = **5.29 V** | **inferred**, not measured |
| `+3.3V` | R12 68 kΩ / R13 15 kΩ (SY8089) | 1.2 × (68/15 + 1)… ≈ 6.6 V — **does not compute to 3.3 V**, so the SY8089's reference or divider topology differs from the SY7088's. **Do not trust this line.** | **unresolved** |
| Charge current | TP4057 with `R_PROG` = 3.3 kΩ | order of **300 mA** | **inferred** from the usual TP4057 `I = 1000 × V_PROG / R_PROG` relation; the datasheet was not retrieved |

The `+3.3V` arithmetic not working out is recorded honestly rather than fudged: either the
resistor identification from the extracted text is wrong, or the SY8089 uses a different
feedback reference. See [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).

## Reading the battery

Single ADC channel, **GPIO 10**, through a divider.

```cpp
#include <M5Cardputer.h>
void setup() { auto cfg = M5.config(); M5Cardputer.begin(cfg, true); }
void loop() {
  int32_t mv  = M5Cardputer.Power.getBatteryVoltage();   // millivolts
  int32_t pct = M5Cardputer.Power.getBatteryLevel();     // 0..100, curve-fitted
  M5Cardputer.Display.setCursor(0,0);
  M5Cardputer.Display.printf("%ld mV  %ld%%", mv, pct);
  delay(1000);
}
```

`Power_Class.cpp:573-574` groups `board_M5Cardputer` and `board_M5CardputerADV` together, so
the same conversion is used for both — despite the ADV having a *single* 1750 mAh cell where
the v1.x has 120 mAh + 1400 mAh. The divider ratio is the same; the capacity is not, so any
percentage curve tuned on a v1.x is only approximately right here. Bruce hard-codes
`-DANALOG_BAT_PIN=10` and does its own conversion.

There is **no fuel gauge**. The CardputerZero has a BQ27220YZFR; the ADV has a resistor divider.
Coulomb counting, cycle count, health and time-to-empty are not available.

## ⚠ Charging requires the power switch ON

M5Stack states this on the ADV, v1.0 and v1.1 pages alike: *"When charging the Cardputer-Adv,
please switch the power to ON."* The side switch (SW1) gates the path the charger needs; with
it OFF the device draws the quoted **0.23 µA** but does not charge.

This surprises people. It is the most consistently repeated warning across all three product
pages and the one most likely to produce a "my Cardputer won't charge" report.

## Vendor power figures

At DC 4.2 V, from the ADV product page:

| Condition | Current |
|---|---|
| Standby, power switch **OFF** | **0.23 µA** |
| Operating | 120.2 mA |
| Wi-Fi active | 132.3 mA |
| BLE active | 154.6 mA |

Against 1750 mAh that is roughly 13 h Wi-Fi / 11 h BLE **if** those figures include the display
backlight, which M5Stack does not say. Compare the v1.1's published numbers — *"IR transmission
mode 148.07 mA, key mode 138.93 mA"* — which are measured under different conditions again, so
the two generations' figures are **not directly comparable**. Do not build a runtime comparison
out of them.

Note also that BLE reads *higher* than Wi-Fi here, which is the opposite of the usual ordering
and suggests the three measurements were taken with different display/CPU states. Recorded as a
vendor-data oddity.

## Making it last

* **Backlight dominates.** But see [`display.md`](display.md): dimming below 100 % browns out
  the RGB LED, because they share the AW35122-switched rail.
* **Deep sleep** works; the ESP32-S3's RTC domain survives it. But there is **no RTC and no
  IMU interrupt**, so your only wake sources are timer, GPIO (G0, or a CAP `INT`) and touch.
* **`Speaker.end()` does nothing** — the ES8311 stays powered. Explicitly run the microphone's
  power-down sequence, or drive the codec yourself, before sleeping. See
  [`audio.md`](audio.md) §6.2.
* The `+5VOUT` boost runs whenever the device is on; a Grove or CAP peripheral drawing from it
  is paid for at boost efficiency.

## Safety and repair

* 0 – 40 °C operating range (vendor).
* The cell is internal and not user-serviceable without opening the case; there is **no
  published cell part number**.
* r/M5Stack, 2026-08-05: *"I'm looking for screws and buttons of the right height for the
  Cardputer ADV, but I can't find them on AE."* — M5Stack sells a mixed M3 screw pack; button
  caps are commonly 3D-printed. Spares for the ADV specifically are not stocked.
* r/M5Stack, 2026-08-22: *"Cardputer adv black screen only when turning it on"* — a boot-time
  display failure with two low-information replies. Unresolved; recorded because it is the only
  hardware-fault report found for the ADV in this pass.

## Evidence status

| Claim | Status |
|---|---|
| Part identities and topology | **official** — rendered schematic sheet 1 |
| DNP marking on R3/D3 | **official** — drawn greyed |
| `+5VOUT` ≈ 5.29 V, ~300 mA charge | **inferred**, formula shown, not measured |
| `+3.3V` divider arithmetic | **unresolved** — stated, not hidden |
| Current figures | **vendor claim**, conditions unstated, **not independently measured** |
| Runtime estimates | **derived** from vendor claims; treat as upper bounds |
