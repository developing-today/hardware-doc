# LiPo 102035 battery (optional, maker and capacity unknown)

- **Category:** 3.7 V nominal single-cell lithium-polymer pouch cell
- **Reference on this board:** the battery connector does not carry a legible reference designator in the five published sheets. The cell itself is a **product option**, sold with or without
- **Owning MCU:** **ESP32-S3**, indirectly — GPIO1 reads a divider on the **5 V** rail, not on the battery terminal (§4)
- **Research status:** the designation `102035` and the fact that it is optional are established from Waveshare's product material. **Capacity, chemistry-protection details, maker, and even the dimension decode are not established.** The charge path is a separate unresolved item
- **Retrieved:** 2026-08-21; dimension decode analysed and runtime estimation built 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source or community source · **[DOC]** manufacturer datasheet · **[WEB]** vendor page/wiki · **[INF]** inference, arithmetic shown

---

## 1. What is established

| Fact | Evidence |
|---|---|
| The product is offered **with or without** a battery — it is an option, not standard | [WEB] |
| Waveshare describes it as a **3.7 V `102035` LiPo** | [WEB] |
| It connects via a small polarised connector on the board | [WEB, imagery] |
| The board has a **`BATT_ADC` net** on ESP32-S3 GPIO1 through a 10 kΩ/10 kΩ divider | [SCH sheet 4] |
| **That divider is on the 5 V net, not on a battery terminal** | [SCH sheet 4] — §4 |

That is the whole list. In particular:

- **Capacity (mAh) is not stated anywhere in the retained material.** Not on the product page snapshot, not on the wiki, not in the schematic.
- **The cell maker, protection-circuit specification, and any datasheet are unknown.**
- **No charger IC is identifiable in the published schematic sheets.** See [generic/charger-power-path](../charger-power-path/README.md). This means **charge current, termination voltage, pre-charge behaviour, temperature qualification and over-discharge protection are all unknown at the board level.**

## 2. ⚠ Decoding `102035` — and why it is genuinely ambiguous

Lithium-polymer pouch cells are conventionally named with a six-digit code `TTWWLL`:

- `TT` — thickness
- `WW` — width in millimetres
- `LL` — length in millimetres

So `102035` decodes to **10 / 20 / 35**, giving a cell **20 mm × 35 mm** with a thickness of "10".

**The thickness unit is where the ambiguity lies**, and this is not pedantry — the two readings differ by a factor of ten in volume:

| Reading | Thickness | Volume | Plausible capacity at ~300 Wh/L |
|---|---:|---:|---:|
| `TT` in **tenths of a millimetre** (the strict convention) | **1.0 mm** | 0.70 cm³ | ~0.21 Wh ≈ **57 mAh** |
| `TT` in **whole millimetres** (common marketplace usage) | **10.0 mm** | 7.00 cm³ | ~2.1 Wh ≈ **570 mAh** |

The strict convention is well established for codes like `502030` (5.0 × 20 × 30 mm) — reading `50` as 50 mm would be absurd. But the same convention applied to widely-sold codes like `103450`, which are physically 10 mm thick and around 2000 mAh, gives 1.0 mm and a nonsense capacity. **The market applies the convention inconsistently for `TT` values of 10 and above**, and this cell sits exactly on that boundary.

**Which is it here?** **[INF]** The evidence points to **10 mm × 20 mm × 35 mm**:

1. **Form factor.** The device is a round metal knob puck, not a card or a wearable band. There is depth available. A 1.0 mm cell is a specialty item used in smart cards and ultra-thin wearables.
2. **Energy plausibility.** At 57 mAh, and with the board's measured idle draw (§5), the device would run for well under an hour. A vendor would not offer that as a product option.
3. **Consistency with the code's neighbours.** Waveshare's other battery-equipped boards in this size class use cells of a few hundred mAh.

**But this is inference, not evidence.** No Waveshare document in the retained archive states either the thickness or the capacity. **If you have a cell in hand, measure it and record the printed capacity here** — it is a two-minute observation that closes a real gap.

The rest of this page uses **500 mAh** as a working figure where a number is needed, always labelled as such, on the grounds that it is the most common capacity for a 10 × 20 × 35 mm cell. **Do not treat it as established.**

## 3. Connector — also unresolved, and this one is dangerous

The board documentation conflicts with itself **[WEB]**:

- Some Waveshare product wording describes a **PH1.25** connector
- The wiki imagery is described as **MX1.25**

These are different connector families with different housings, and — critically — **there is no industry-wide polarity convention for two-pin LiPo connectors.** Some vendors wire red to pin 1, some to pin 2.

**Before connecting any battery:**

1. **Measure the pitch.** PH is 2.0 mm; "PH1.25" and MX1.25 are both 1.25 mm, so the conflict is more about family than pitch — but measure anyway.
2. **Check the keying** physically against the housing.
3. **Verify polarity with a meter**, on the board, before the cell goes anywhere near it. Positive should be identifiable by tracing to the 5 V/charger side.
4. **Do not rely on wire colour alone.** Reversed-polarity cells are sold.

**Connecting a LiPo backwards can vent or ignite it.** This is the one place on this board where an unresolved documentation detail has a physical-safety consequence, which is why it is flagged this prominently. The conflict is also recorded in [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md).

## 4. ⚠ `BATT_ADC` does not measure the battery

This is the single most commonly misunderstood thing about power on this board.

The schematic **[SCH sheet 4 `4_OTHER.png`]** shows:

```
5V ──── R62 (10 kΩ) ──┬──── BATT_ADC ──── ESP32-S3 GPIO1 (ADC1 channel 0)
                      │
                     R63 (10 kΩ)
                      │
                     GND
```

**The divider taps the `5V` net.** It does not connect to a battery terminal, to a charger output, or to any dedicated `VBAT` node. The net is *named* `BATT_ADC`, but its name is aspirational.

> **Re-verified 2026-08-24.** Because this claim is load-bearing for every battery-monitoring and runtime figure on this page, it was deliberately re-tested in a later pass that treated *"the divider actually senses VBAT"* as the hypothesis to beat. **It does not.** The divider's top net label was read at 600× magnification and is unambiguously two glyphs — **`5V`**, not `VBAT` and not `VSYS`. The resistor legends read `R62`/`10K` and `R63`/`10K`, and the mid-node carries a junction dot with a wire running left to the net label `BATT_ADC`. **The reading above stands unchanged, and no runtime estimate on this page needed revision.**

The vendor demo reads it correctly and, to its credit, labels the result honestly **[SRC `adc_bsp.c`]**:

```c
adc_cali_curve_fitting_config_t cali_config = {
    .unit_id  = ADC_UNIT_1,
    .atten    = ADC_ATTEN_DB_12,     // ~0-3.1 V input range
    .bitwidth = ADC_BITWIDTH_12,     // 4096 counts
};
// ...
adc_oneshot_read(adc1_handle, ADC_CHANNEL_0, &adcdata);
adc_cali_raw_to_voltage(cali_handle, adcdata, &vol);
*value = 0.001 * vol * 2;            // mV -> V, and undo the /2 divider
```

and prints it as `"system voltage"`, not "battery voltage".

**What this means in practice:**

| Question | Answerable from GPIO1? |
|---|---|
| What is the 5 V rail sitting at? | **Yes**, accurately, with calibration |
| Is USB connected? | **Probably** — a USB-powered 5 V rail reads near 5.0 V |
| What is the battery voltage? | **Only indirectly, and only if you know the power-path topology — which is unknown.** See [charger-power-path](../charger-power-path/README.md) |
| What is the state of charge? | **No.** Not without a battery-terminal measurement |
| Is the battery charging? | **No.** No `CHG`/`STAT` signal reaches either MCU **[SCH]** |

**[INF]** If the power path is a simple ideal-diode OR (the common Waveshare arrangement), then on battery power the "5 V" net would actually sit at the *boosted* output, or at the cell voltage if there is no boost — either way, the reading would move with the battery and could be *calibrated* into a rough state-of-charge estimate. **But that requires knowing the topology, and the topology is not established.** Do not ship a fuel gauge based on this ADC without first characterising it against a bench supply and a real cell.

The divider also costs **165 µA continuously** from the 5 V rail (`5 V / 20 kΩ`) — it is unswitched **[SCH]**. Small, but it is a permanent parasitic that a JFET or a switched divider would have avoided.

## 5. Battery life estimation for this board

Here is where the picture gets interesting, because **the dominant term is not the one you would expect.**

### 5.1 The current draws that matter

| Load | Current | Evidence |
|---|---:|---|
| **ESP32-U4WDH running stock firmware, idle** | **~50 mA continuous** | **[SRC]** community measurement, `svwhisper/lyngdorf-secondary-sleep`, quoted in [development.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/development.md#the-secondary-mcu-costs-50-ma-if-you-leave-it-alone) |
| **ESP32-U4WDH after flashing a deep-sleep stub** | **~10 µA** | **[SRC]** same source |
| ESP32-S3, active, radio idle | ~40–50 mA | [DOC] |
| ESP32-S3, Wi-Fi connected, light traffic | ~80–120 mA avg | [DOC, INF] |
| Backlight at 100% | ~30–110 mA | **[INF]** — see [tlv62569dbvt §4](../../texas-instruments/tlv62569dbvt/README.md#4--the-backlight-is-the-load-to-worry-about) |
| Display + touch + panel logic | ~15–30 mA | [INF] |
| Everything else idle (flash, mic, haptic quiescent, pull-ups) | ~10 mA | [INF] |
| `BATT_ADC` divider | 0.165 mA | [SCH] arithmetic |

### 5.2 The headline finding

**If you are not using Classic Bluetooth, the secondary MCU is burning ~50 mA doing nothing, and you cannot switch it off in hardware.** `EN` on the ESP32-U4WDH is pulled up and driven only by the USB-UART bridge; no S3 GPIO reaches it **[SCH sheet 3]**.

On a nominal 500 mAh cell, 50 mA alone is **a 10-hour ceiling with the rest of the board completely off.** In an idle scenario where the S3 is also awake and the screen is on, the secondary MCU is something like a **quarter to a third of total draw, contributing nothing.**

The fix is firmware, not hardware: flash the U4WDH with an image whose `app_main` is `esp_deep_sleep_start()` with no wake source, taking it to ~10 µA. Two independent community projects ship exactly that. **Back up `ESP32-KNOB_ESP32_0.bin` first** — it is the only copy of the Classic Bluetooth application in existence, and it cannot be rebuilt. See [development.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/development.md#the-secondary-mcu-costs-50-ma-if-you-leave-it-alone) and [espressif/esp32-u4wdh](../../espressif/esp32-u4wdh/README.md).

### 5.3 Scenario estimates

Assuming **500 mAh [INF]**, and accounting for the buck's ~90% efficiency stepping the battery-derived rail down (plus whatever the unknown boost/power-path costs — call the combined efficiency 85%, which makes these **optimistic**):

| Scenario | 3V3 draw | Battery draw at 3.7 V, 85% end-to-end | **Runtime from 500 mAh** |
|---|---:|---:|---:|
| **Screen on, Wi-Fi active, U4WDH stock** | ~250 mA | ~265 mA | **~1.9 h** |
| Screen on, Wi-Fi active, **U4WDH slept** | ~200 mA | ~212 mA | **~2.4 h** |
| Screen on, radios idle, U4WDH stock | ~180 mA | ~191 mA | **~2.6 h** |
| Screen on, radios idle, **U4WDH slept** | ~130 mA | ~138 mA | **~3.6 h** |
| **Screen off**, S3 awake polling knobs, U4WDH stock | ~110 mA | ~117 mA | **~4.3 h** |
| Screen off, S3 awake, **U4WDH slept** | ~60 mA | ~64 mA | **~7.8 h** |
| S3 in **light sleep**, screen off, U4WDH stock | ~52 mA | ~55 mA | **~9.1 h** |
| S3 in light sleep, screen off, **U4WDH slept** | ~2 mA | ~2.1 mA | **~10 days** |
| S3 in **deep sleep**, U4WDH slept | ~0.3 mA | ~0.3 mA | **~2 months** |

**[INF]** — arithmetic ours, from the §5.1 current figures. Two of those figures (the 50 mA and 10 µA for the U4WDH) are measured by a third party; the rest are datasheet-derived or estimated. **Treat the table as showing ratios, not absolute hours.**

Read the last four rows against the first four. **The two biggest levers are the backlight and the secondary MCU, in that order — and both are entirely under your control.** MCU sleep modes only start to matter after you have dealt with both.

### 5.4 Practical recommendations

1. **Sleep the ESP32-U4WDH** unless you need Classic Bluetooth. Biggest single win, ten lines of code. §5.2.
2. **Aggressively blank the backlight.** An idle timeout of 15–30 seconds roughly doubles screen-off runtime. The knob and touch controller can wake it.
3. **Do not fight for the last milliamp elsewhere first.** The `BATT_ADC` divider's 165 µA and the DRV2605L's 0.65 mA are rounding errors next to the backlight.
4. **Deep sleep is only useful if the U4WDH is also asleep.** Otherwise you deep-sleep the S3 and still burn 50 mA.
5. **You cannot measure state of charge.** §4. Design the UX around that — a "low battery" warning derived from a rail voltage you cannot interpret is worse than no warning.

## 6. Charging — what is and is not known

**No charger IC is identifiable in the five published schematic sheets** **[SCH]**. Waveshare's product material claims charging **[WEB]**, and the board evidently has a battery connector, but the block that would do it is not drawn.

Consequently **all of the following are unknown**:

| Unknown | Why it matters |
|---|---|
| Charge current | Determines charge time, and whether the cell is being charged within its C-rate |
| Termination voltage | 4.2 V is standard; 4.35 V high-voltage cells exist. Wrong pairing shortens life or is unsafe |
| Pre-charge / trickle behaviour for deeply discharged cells | Whether a flat cell recovers |
| Temperature qualification (NTC) | Whether charging is inhibited when hot or cold. **Most low-cost single-cell chargers omit this** |
| Charge-status output | None reaches either MCU **[SCH]** — see §4 |
| Over-discharge cut-off | Usually in the cell's own protection PCM, not on the board |
| Power-path behaviour (charge-while-running) | Whether the load is fed from the charger or from the cell |

See [generic/charger-power-path](../charger-power-path/README.md) for the identification strategy.

**The safety consequence:** because the charge termination voltage and the temperature qualification are both unknown, **you should not substitute a cell with a different chemistry or a different termination voltage**, and you should not leave the device charging unattended in an enclosed or hot space until the charger has been identified and characterised.

## 7. Safety

Standard single-cell LiPo practice, with the board-specific points called out:

1. **Verify connector polarity with a meter before first connection.** §3. This is the highest-risk item on this page.
2. **Use a cell with an integrated protection circuit (PCM).** Most pouch cells sold with pigtail leads have one; bare cells do not. Since the board's over-discharge behaviour is unknown (§6), the cell's own protection is your only guarantee.
3. **Match the termination voltage.** Do not fit a 4.35 V cell to an unidentified 4.2 V charger or vice versa.
4. **Do not exceed the mechanical envelope.** A cell that has to be compressed to fit is a punctured cell waiting to happen. The internal cavity dimensions are **undocumented** — see §2.
5. **Watch for swelling.** A pouch cell that has visibly puffed is at end of life and should be removed and disposed of properly, not "used up".
6. **Charge at moderate temperature.** LiPo charging below 0 °C causes lithium plating. Whether this board's charger inhibits that is **unknown** (§6), so assume it does not.
7. **Do not leave a battery-equipped board charging unattended** until the charger is identified.
8. **Transport and storage:** partially charged (~50%) is kindest to the cell and safest.

## 8. Open questions

| Question | Status | How to close it |
|---|---|---|
| **Capacity in mAh** | **Unknown.** §2 uses 500 mAh as a working figure only | Read the label on a supplied cell |
| **Thickness: 1.0 mm or 10 mm** | **Unresolved.** §2. Inference favours 10 mm | Measure a supplied cell |
| Cell maker and datasheet | **Unknown** | Cell label |
| Connector family and **polarity** | **Conflicting** — PH1.25 vs MX1.25. §3 | Measure the pitch and the polarity on the board |
| Charger IC, charge current, termination voltage | **Unknown.** §6 | [charger-power-path](../charger-power-path/README.md) |
| Whether `BATT_ADC` can be calibrated into a state-of-charge estimate | **Unknown** — depends on the power-path topology. §4 | Characterise against a bench supply and a real cell |
| Measured runtimes | **Unknown.** §5.3 is arithmetic, not measurement | Run the board down with a coulomb counter inline |
| Presence of an NTC on the battery connector | **Unknown** — the connector is not drawn with a legible pin count | Continuity-check the connector |

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — optional product configuration

## Related pages

- [generic/charger-power-path](../charger-power-path/README.md) — the unidentified charging block
- [texas-instruments/tlv62569dbvt](../../texas-instruments/tlv62569dbvt/README.md) — the buck the battery ultimately feeds, and the load budget behind §5
- [espressif/esp32-u4wdh](../../espressif/esp32-u4wdh/README.md) — the secondary MCU that dominates idle current
- [generic/lcd-panel-module](../lcd-panel-module/README.md) — the backlight, the other dominant load
- [development.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/development.md) — the ~50 mA / ~10 µA community finding in context
- [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md) — where the connector conflict is tracked board-wide

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Waveshare product page — the "3.7 V 102035 LiPo" option and the connector wording | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki — battery imagery and the conflicting connector description | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
| Board schematic sheet 4 — the `BATT_ADC` divider `R62`/`R63` **on the 5 V net** | — | 2026-08-21 | `.../artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/4_OTHER.png` |
| Board schematic sheet 1 — the 5 V rail and `CN1` | — | 2026-08-21 | `.../artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Waveshare demo `01_ADC_Test` — `adc_bsp.c`, the "system voltage" reading | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/01_ADC_Test/` |
| Community measurement of the ESP32-U4WDH's ~50 mA idle / ~10 µA slept draw | `svwhisper/lyngdorf-secondary-sleep`, catalogued in [examples/catalog.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/catalog.md) | 2026-08-23 | retained under `.../examples/selected/` |
| ESP32-S3 datasheet (current figures in §5.1) | https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` |
| ESP32 datasheet (ESP32-U4WDH current figures) | https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf | 2026-08-21 | `../../espressif/esp32-u4wdh/artifacts/esp32-datasheet.pdf` |
| ESP-IDF v5.3.2 ADC oneshot + calibration drivers | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/adc_oneshot.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
