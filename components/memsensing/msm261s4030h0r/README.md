# MEMSensing MSM261S4030H0R

- **Category:** MEMS microphone. The `S` in this family designation denotes the **analogue**
  output variant of the MSM261 family, as against the `D` (digital PDM/I²S) parts — **but that
  reading is inferred from the family naming, not from the datasheet**, which was retained but
  not read.
- **Manufacturer:** MEMSensing Microsystems (Suzhou) Co., Ltd.
- **Retrieved:** 2026-09-07
- **Siblings already here:** [`msm261d3526h1cpm`](../msm261d3526h1cpm/README.md) ·
  [`msm261d4030h1cpm`](../msm261d4030h1cpm/README.md) · [`msm381a3729h9bp`](../msm381a3729h9bp/README.md)

The microphone of the **LilyGO T-Display-S3 Pro MVSRBoard** backplate — the **M** in *MVSR*
(Microphone, Vibration, Speaker, RTC).

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **MSM261S4030H0R** |
| Local artifact | [`artifacts/msm261s4030h0r-datasheet-lilygo-mirror.pdf`](artifacts/msm261s4030h0r-datasheet-lilygo-mirror.pdf) — 1 694 952 B, SHA-256 `bd2a5507eea390942ea60707b418bcfddb3ff41e561ed2e69c63a80ca2390cd5` |
| Mirror source | `Xinyuan-LilyGO/T-Display-S3-Pro` → `datasheet/MEMSensing-MSM261S4030H0R.pdf` @ `08b8b2bbcb8b263131af119476403080cd30224f` |
| Licence | MEMSensing copyright. **The `T-Display-S3-Pro` repository declares no licence**, so redistribution status is doubly unknown |

## 2. Relationship to the parts already documented here

This repository already holds two close relatives, both fitted to Waveshare boards:

| Part | Output | Documented for |
|---|---|---|
| `MSM261D3526H1CPM` | digital (PDM) | Waveshare |
| `MSM261D4030H1CPM` | digital (PDM) | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |
| **`MSM261S4030H0R`** | **`S`** — see the caveat above | LilyGO T-Display-S3 Pro MVSRBoard |

`MSM261D**4030**H1CPM` and `MSM261S**4030**H0R` share the `4030` size/sensitivity field, which
suggests the same acoustic element in different output configurations. **That is a reading of
the part-number structure, not a documented fact**, and the `D`/`S` and `H1CPM`/`H0R` suffixes
were not decoded from any datasheet. If you need to know whether this part outputs PDM or an
analogue signal — and you do, because it determines whether it can connect to the ESP32-S3's
I²S peripheral directly — **read the retained datasheet.**

## 3. Board integration

Fitted to the **MVSRBoard** backplate, not to the T-Display-S3 Pro mainboard. Pin assignment,
clock and data routing were **not established** — no MVSRBoard pin header was located, and the
board's own schematic was retrieved but not traced.

Alongside it on the same backplate: a
[MAX98357A](../../analog-devices/max98357a/README.md) I²S class-D speaker amplifier, a
[PCF85063ATL](../../nxp/pcf85063a/README.md) RTC, and a vibration motor.

## 4. Gaps

- **Datasheet retained but not read.** Output type, sensitivity, SNR, supply and clock
  requirements are all unrecorded.
- Pin assignment on the MVSRBoard unknown.
- Not verified on hardware.

## 5. Used by

### LilyGO T-Display-S3 Pro MVSRBoard
→ [`devices/lilygo/t-display-s3-pro-mvsrboard`](../../../devices/lilygo/t-display-s3-pro-mvsrboard/README.md)
(a stub record) · mainboard: [`devices/lilygo/t-display-s3-pro`](../../../devices/lilygo/t-display-s3-pro/README.md)
