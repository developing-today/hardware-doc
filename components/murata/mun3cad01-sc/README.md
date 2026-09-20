# MUN3CAD01-SC — 1 A µPOL step-down power module

- **Category:** fully-integrated point-of-load DC-DC **module** (converter + inductor + input/
  output capacitance in one package).
- **Manufacturer:** **Murata** — `µPOL` is Murata's trademark for this monolithic power-module
  family, and the part-number grammar matches. **The mirrored datasheet's first page carries no
  vendor name or logo**, so the attribution is `inferred` from the trademark, not read. Filed
  under `murata/` on that basis; if a contrary source appears, this record should move.
- **Retrieved:** 2026-09-04

The 5 V → 3.3 V converter inside the **M5Stack Stamp-S3** module (`M2`). **Not fitted on the
Stamp-S3A** despite what M5Stack's Stamp-S3A page says — see §3.

---

## 1. Specification (from the datasheet)

| Property | Value |
|---|---|
| Output current | **1 A** |
| Peak efficiency | 93 % at 3.3 V<sub>IN</sub> |
| Input range | **2.7 – 5.5 V** |
| Output range | **0.8 – 4.0 V** (set by external feedback divider) |
| Modes | automatic power-saving / PWM |
| Protection | UVLO, OCP (non-latching) |
| Soft start | internal |
| Package | **2.9 × 2.3 × 1.05 mm** |
| Compliance | Pb-free / RoHS, MSL 2, 260 °C reflow |
| Stated applications | single Li-ion powered equipment, LDO replacement, phones/PDAs/palmtops |

All from page 1 of the retained datasheet; the text layer was validated against the visible
title block before transcription.

## 2. As fitted on the Stamp-S3 (board rev v0.2)

| Property | Value | Evidence |
|---|---|---|
| Designator | `M2`, 6 pins: `EN`, `GND`, `VIN`, `GND`, `FB`, `VOUT` | `Sch_M5StampS3_v0.2.pdf` |
| Input | `VIN_5V` | schematic |
| Output | `VDD_3V3` | schematic |
| Feedback divider | `R6` **100 kΩ** / `R17` **22.1 kΩ** | schematic |
| Bulk capacitance | `C21`, `C22` 10 µF/10 V | schematic |

Divider check: with a 0.6 V reference, 0.6 × (100/22.1 + 1) ≈ 3.32 V. Consistent with a 3.3 V
rail. Arithmetic on read values; the reference voltage was **not** read from the datasheet page
retained here.

## 3. ⚠ It is *not* on the Stamp-S3A

The [Stamp-S3A](../../m5stack/stamp-s3a/README.md) product page lists `DC-DC: MUN3CAD01-SC` and
links this very datasheet — from the **`S007 StampS3`** directory, i.e. the Stamp-S3's own path.

But the string `MUN3CAD01` **does not appear anywhere in `Sch_StampS3_v0.3.3.pdf`**, the
designator `M2` is absent from that sheet, and the regulator there is `U4`: an 8-ball part with
`VIN`/`EN`/`SW`/`VOS`/`VSEL1`/`VSEL2`/`VSEL3`/`GND`, annotated `IOUT: 0~0.6A`, driving an
**external** 2.2 µH inductor (`L4`, `MWTC201608S2R2`). A µPOL module has an *integrated*
inductor and an `FB` pin, not `SW` and `VSEL` straps.

The specification row appears to have been carried over unedited when the Stamp-S3A page was
created. The schematic is the stronger evidence.
→ [`components/unidentified/m5stack-stamp-s3a/dcdc-u4/`](../../unidentified/m5stack-stamp-s3a/dcdc-u4/README.md)

## 4. Artifacts

| File | Size | SHA-256 | Licence | Redistribution | Disposition |
|---|---:|---|---|---|---|
| [`artifacts/mun3cad01-sc-datasheet-m5stack-mirror.pdf`](artifacts/mun3cad01-sc-datasheet-m5stack-mirror.pdf) | 2 045 960 | `90e2ecbd8cf35af2102ded0216a5f94d58d94a31adf0436308356376633433cb` | unknown | `unknown` | `repository` |

Retrieved 2026-09-04 from
`https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/Stamp/S007%20StampS3/MUN3CAD01-SC.pdf`
(HTTP 200, `%PDF` validated, text extracted and cross-checked against the visible title).
Renamed to record that this is an **M5Stack mirror**; no manufacturer-hosted copy was located.
No document version or revision date is printed on page 1 — recorded as unknown rather than
omitted.

---

## Used By

### M5Stack Stamp-S3 (SKU S007), board rev v0.2

`M2` — the module's only 5 V → 3.3 V converter, feeding `VDD_3V3` which supplies the
ESP32-S3FN8, the WS2812B-2020 RGB LED (always-on on this revision) and the
[SGM2578](../../sgmicro/sgm2578/README.md) backlight load switch.
→ [`components/m5stack/stamp-s3/README.md`](../../m5stack/stamp-s3/README.md)

### Reached from these devices

- [M5Stack DinMeter (K134)](../../../devices/m5stack/dinmeter/README.md) — fits a Stamp-S3, so
  this part is inside it
- [M5Stack DinMeter v1.1 (K134-V11)](../../../devices/m5stack/dinmeter-v1.1/README.md) —
  **does not** contain this part; it fits a Stamp-S3A
