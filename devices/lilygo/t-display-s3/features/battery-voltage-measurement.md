# T-Display-S3 — battery voltage measurement, the divider, and the pin conflict it creates

> Evidence: schematic designators + LilyGO's own example + three independent user reports.
> **Not hardware-verified by this pass.** The divider *ratio* is inferred, not traced — §5.

## 1. The circuit, as far as it is established

| Fact | Value | Evidence class |
|---|---|---|
| Sense pin | **GPIO4** (`PIN_BAT_VOLT`, ADC1 channel 3) | primary — `examples/*/pin_config.h` @ `ec889e7`, all copies agree |
| Divider resistors | `R2` and `R4`, both printed **`100K %1`** | primary — designator/value strings recovered from `schematic/T_Display_S3.pdf` |
| Implied ratio | **1 : 2** (V<sub>ADC</sub> = V<sub>BAT</sub> / 2) | **inferred**, corroborated by the vendor multiplying by 2 |
| Gate | a P-channel MOSFET (`Q4` = `SI2307`) sits in the sense path | primary designator; **the gate's control net was not traced** |
| Reading with USB attached | ≈ **2.5 V**, i.e. 5 V/2 — *not* the battery voltage | firsthand user report, corroborated by vendor doc |

LilyGO states the behavioural consequence directly:

> "The battery ADC pin can only read the battery voltage when the USB-C port is **not** plugged
> in; it cannot read the battery voltage after the USB-C port is plugged in."
> — `T-Display-S3/README.md` @ `ec889e789b3cf093412689a143f7f37b42b56af7`

## 2. The correct way to read it

This is the vendor-adjacent recipe from
[issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230) (2024, by the same
owner who traced the PCB), and it is right for a reason worth spelling out:

```cpp
void setup() {
    analogReadResolution(12);            // 0..4095
    analogSetAttenuation(ADC_11db);      // widest input range
}

void loop() {
    // analogReadMilliVolts() applies the per-chip eFuse ADC calibration.
    // analogRead() does NOT, and the ESP32-S3 ADC is markedly non-linear without it.
    uint32_t mv = analogReadMilliVolts(4) * 2;   // ×2 for the 100k/100k divider
}
```

**Use `analogReadMilliVolts()`, not `analogRead()` × a constant.** That is the whole difference
between the two most-reported bug reports on this topic:

- [issue #190](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/190) (2023-09-22) — an
  ESP-IDF user computing `raw * 3.3 / 4096` read **2.14–2.15 V** with a battery measuring
  **3.9 V** on a multimeter. Expected would be ~1.95 V; the raw-count arithmetic plus ADC
  non-linearity produced a number that is wrong in a plausible-looking way. Evidence class:
  **firsthand measurement with an independent instrument.**
- [issue #65](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/65) (2022-12-12) —
  "LCD_BAT_VOLT does not work on battery", 18 comments.

In ESP-IDF, the equivalent is `adc_cali_*` with the curve-fitting scheme, not
`raw * Vref / 4096`.

## 3. The pin conflict

**GPIO4 is the only battery sense, and it is a general-purpose pin on the header.** There is
no PMIC to ask instead — unlike the Long, Pro and T4-S3, which read the SY6970 over I²C and
leave GPIO4 free.

| If you want GPIO4 for… | Then |
|---|---|
| another ADC input | you lose battery monitoring entirely. There is no alternative path |
| a digital output | **do not.** You are driving into the top of a divider connected to `VBAT`; at minimum you fight the divider, and you can push current into the sense node |
| a digital input | works, but the fitted divider holds it near V<sub>BAT</sub>/2 with no battery and near 2.5 V on USB — it is not a clean input |

There is a subtler conflict too: **ADC2 is unusable while Wi-Fi is active** on ESP32-S3.
GPIO4 is on **ADC1**, so battery sensing is safe — but it means one of your scarce ADC1
channels is permanently spoken for, and if you also need an analogue sensor you must keep it
on ADC1 (GPIO1–GPIO10) rather than reaching for ADC2 pins.

## 4. What the reading means, and what it does not

- **There is no state-of-charge gauge.** No BQ27220, no coulomb counter. You are inferring
  charge from terminal voltage under unknown load, which on a LiPo is worth roughly ±20 % in
  the flat part of the curve.
- **There is no on-board battery protection.** LilyGO's maintainer, 2025-02-06:
  *"No built-in battery protection, needs to be used with a lithium-ion battery with battery
  protection."* Your firmware's low-voltage cutoff is not a substitute for a protected cell —
  it stops working the moment your firmware crashes.
- **While charging, the terminal voltage is the charger's output**, not the cell's state.
- **With USB attached you read ~2.5 V regardless**, so any "is the battery low" logic must
  first detect USB presence — and the only way to do that on this board is to notice the
  reading is pinned near 2.5 V, because `VBUS` is not sensed by any GPIO.

## 5. What was not established, and how to settle it

| Open question | How to settle it |
|---|---|
| Is the divider really 100 k/100 k to ground, or 100 k/100 k with a series gate that changes the ratio? | Trace `R2`/`R4`/`Q4` on the schematic sheet with a netlist extractor, or measure a board with no battery and a known voltage on the JST connector |
| What drives `Q4`'s gate? Is the divider disconnected in deep sleep? | Same. This matters for sleep current — a permanently connected 200 kΩ divider across a 4.2 V cell draws ~21 µA, which is comparable to the whole deep-sleep budget |
| Exact ADC attenuation LilyGO's own example uses | Read `examples/GetBatteryVoltage/GetBatteryVoltage.ino` @ `ec889e7` (retained in scratch); it is the vendor's reference |

The netlist route is available in this repository —
[`tools/altium_pdf_netlist.py`](../../../../tools/altium_pdf_netlist.py) — but it needs
`pdftotext -bbox` XML and poppler was not installed on the host used for this pass. Recorded
in [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).

## Cross-references

- [`power-and-battery.md`](power-and-battery.md) — charging, charge current, the GPIO15 gate
- [`deep-sleep.md`](deep-sleep.md) — why the divider matters for sleep current
- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) — the full GPIO map
