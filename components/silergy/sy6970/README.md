# Silergy SY6970

- **Category:** I²C-controlled **switch-mode single-cell Li-ion charger** with power-path
  management, OTG boost, integrated ADC and programmable input-current limit.
- **Manufacturer:** Silergy Corp.
- **Retrieved:** 2026-09-07
- **Sibling Silergy records here:** [`sy7088`](../sy7088/README.md) ·
  [`sy8089`](../sy8089/README.md)

**LilyGO's standard PMIC for every board in the T-Display-S3 family above the entry tier** —
the Long, the Pro, the T4-S3 and all three DS-series AMOLED boards. It is the single most
important reason those boards handle batteries better than the base T-Display-S3, which uses a
dumb linear charger with a soldered current-programming resistor.

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **SY6970** |
| I²C address | **`0x6A`** on the T-Display-S3 Pro | LilyGO's own README I²C table |
| Local artifact | [`artifacts/sy6970-datasheet-lilygo-mirror.pdf`](artifacts/sy6970-datasheet-lilygo-mirror.pdf) — 1 940 565 B, SHA-256 `95e9bf27d96376ead60e454e448fa1593621bbbe316b4cf1c21c9e585f6ac74d` |
| Mirror sources — **three, all identical size** | `LilyGo-AMOLED-Series` → `datasheet/SY6970 Datasheet.pdf` @ `6d1dc00` · `T-Display-S3-Long` → `datasheet/SY6970 .pdf` [sic, trailing space] @ `37a7e83` · `T-Display-S3-Pro` → `datasheet/SY6970 .pdf` @ `08b8b2b` |
| Additional documents not retrieved | `AN_SY6970.pdf` (application note, 1 940 565 B — **the same size as the datasheet**, so possibly the same file renamed) and `EVB_SY6970.pdf` (363 619 B), both in the 1.64 and 1.43-1.75 repos |
| Licence | Silergy copyright; the mirroring repositories are variously MIT, GPL-3.0 and **no licence at all**. **Redistribution status: unknown** |

**One copy retained.** All three mirror paths report 1 940 565 B, so they are almost certainly
the same bytes; the other two URLs are recorded here rather than stored twice.

**The `AN_SY6970.pdf` size coincidence is worth someone's attention** — if it is the datasheet
under a different name, that is a LilyGO filing error worth recording; if it is a genuine
application note that happens to be the same size, that is a remarkable coincidence. Not
resolved here.

## 2. Why it changes the board

Against the base board's [TP4065-class linear charger](../../nanjing-top-power/tp4065/README.md):

| | Linear charger (base T-Display-S3) | **SY6970** |
|---|---|---|
| Charge current | fixed by a soldered resistor | **programmable over I²C** |
| Input current limit | none | programmable — matters on a weak USB port |
| Battery voltage readout | a separate ADC pin and divider (GPIO4) | **read from the chip over I²C**; no GPIO consumed |
| Charge status | one LED | full status/fault registers |
| OTG / 5 V boost | no | **yes** — the board can *source* 5 V |
| Efficiency | linear: dissipates (V<sub>in</sub>−V<sub>bat</sub>)×I as heat | switch-mode |

That last row matters on the Long, whose vendor-stated active current reaches **90–350+ mA**.

**Consequence for firmware:** on SY6970 boards there is **no `PIN_BAT_VOLT`** to read. Anyone
porting battery code from the base T-Display-S3 will look for one and, on the Long, will find a
`PIN_BAT_VOLT 2` define that is *wrong* — it collides with `TP_RST` and is copy-paste residue.
Read the PMIC instead.

## 3. Software

| Route | Note |
|---|---|
| **`lewisxhe/XPowersLib`** | the driver LilyGO uses; `LilyGo-AMOLED-Series` declares **v0.2.7**. Same author as `SensorLib` |
| Vendor examples | `examples/PMU_Example` (Pro) · `examples/PPM_Example_for_T4S3` · `examples/PPM_Example_for_191Plus` (that one is BQ25896, not SY6970) · `examples/SY6970` and `examples/SY6970_OTG` (1.64″ and 1.43/1.75″ repos) |
| ESPHome | no first-party SY6970 component located as of 2026-09-07 |

The `SY6970_OTG` example is the interesting one — it demonstrates using the board as a 5 V
*source*, which is not possible on any TP4065 board in the family.

## 4. What was not verified

The datasheet was **not read**; no register address, current range or timing is transcribed
here. The I²C address `0x6A` comes from LilyGO's README table. Note that TI's
[BQ25896](../../texas-instruments/bq25896/README.md) — a functionally similar part used on the
AMOLED Plus — is commonly at `0x6B`, so **do not assume the two are interchangeable at the same
address**.

## 5. Used by

| Board | Designator | Role |
|---|---|---|
| [T-Display-S3 Long](../../../devices/lilygo/t-display-s3-long/README.md) | `U6` | sole charger/PMIC; battery voltage is read from it, not from an ADC |
| [T-Display-S3 Pro](../../../devices/lilygo/t-display-s3-pro/README.md) | `U5` | I²C `0x6A`, sharing the bus (SDA GPIO5 / SCL GPIO6) with the CST226SE touch (`0x5A`), LTR-553ALS (`0x23`) and the camera |
| [T4-S3](../../../devices/lilygo/t4-s3/README.md) | `U5` | with `examples/PPM_Example_for_T4S3` |
| [T-Display-S3 AMOLED 1.64″](../../../devices/lilygo/t-display-s3-amoled-1-64/README.md) | — | vendor README names it; `examples/SY6970`, `SY6970_OTG` |
| [T-Display-S3 AMOLED 1.43/1.75″](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md) | — | same examples, plus a PCF8563 RTC |
