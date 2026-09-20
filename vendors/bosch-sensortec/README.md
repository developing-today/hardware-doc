# Bosch Sensortec — Documentation Sourcing Guide

> **Status: no record yet, but we hold a datasheet.** This repository has **no Bosch Sensortec
> component record**, though it does retain a **BMA423 datasheet** obtained from a bundled
> third-party library — see §8.
> The guide is written because Bosch is the reference vendor for MEMS environmental and inertial
> sensors, and because its documentation model is the **best-in-class example** worth measuring the
> Chinese sensor vendors ([MEMSensing](../memsensing/README.md), [QST](../qst/README.md)) against.

> **TL;DR** — Datasheets are at a **guessable, verified path**:
> `https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-<part>-ds<NNN>.pdf`.
> Verified 2026-08-24: `bst-bme280-ds002.pdf` → HTTP 200, 1,663,806 bytes, `%PDF` magic (S2). The
> `ds<NNN>` suffix is a **document revision counter you cannot guess** — scrape it from the product
> page.

---

## 1. Who they are

Bosch Sensortec GmbH (Reutlingen, Germany) is the consumer-MEMS subsidiary of Robert Bosch GmbH.
Bosch is the largest MEMS manufacturer in the world by volume — the accelerometer in a very large
fraction of all smartphones ever shipped is a Bosch part.

Bosch Sensortec is a *component* vendor.

---

## 2. Product lines

| Prefix | What it is | Notable parts |
|---|---|---|
| **`BMA`** | Accelerometers | `BMA400` (ultra-low-power), `BMA456` |
| **`BMG`** | Gyroscopes | `BMG250` |
| **`BMI`** | Inertial Measurement Units (accel + gyro) | `BMI160`, `BMI270` — extremely common |
| **`BMM`** | Magnetometers | `BMM150` |
| **`BMP`** | Barometric **pressure** sensors | `BMP280`, `BMP388`, `BMP390` |
| **`BME`** | **Environmental** combos — pressure + temperature + humidity (+ gas) | `BME280`, `BME680`, `BME688` |
| **`BHI`** | Smart sensor hubs with a programmable core | `BHI260AP` |
| **`BMV`** / **`BMF`** | Voice activity, force | Niche |

**How they fit together — and the one trap.** `BMP280` and `BME280` are **pin-compatible, nearly
register-compatible, and different parts**: the `BME` adds humidity. They are routinely confused,
routinely mislabelled on cheap breakout boards, and are distinguishable by reading the chip-ID
register (`0x58` vs `0x60`). This is the sensor-world equivalent of the
[`DRV2605` / `DRV2605L` confusion](../texas-instruments/README.md#7-gotchas), and it is the single
most common "clone board" complaint in this vendor's ecosystem — see
[clones-and-variants.md](../../guides/markets/clones-and-variants.md).

---

## 3. Market position

**Premium and the de-facto reference.** Bosch parts cost more than QST, MEMSensing or Silan
equivalents and are specified when accuracy, drift and calibration quality matter. The Bosch driver
ecosystem (open-source `BME280`/`BMI270` sensor APIs on GitHub) is a substantial part of the value.

Documentation is **complete, English, public, and includes full register maps** — no NDA, no account.
In this repository only [TI](../texas-instruments/README.md) matches it.

---

## 4. Part numbering

```
BM E 280
│  │ └─ Series index (loosely: higher = newer/better)
│  └─── Sensor type: A=accel, G=gyro, I=IMU, M=magneto, P=pressure, E=environmental
└────── BM = Bosch MEMS   (BH = Bosch sensor Hub)
```

This is one of the cleanest schemes among the vendors documented here: **the third letter tells you
what the sensor measures.** Suffixes (`BMI270`, `BHI260AP`) denote packaging or feature bundles.

---

## 5. Documentation: URL patterns

| Document class | Pattern | Status |
|---|---|---|
| Product category | `https://www.bosch-sensortec.com/products/<category>/` | ✅ verified 2026-08-24 (S3) |
| **Datasheet** | `https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-<part>-ds<NNN>.pdf` | ✅ verified (S2) |
| Application notes | `.../downloads/application_notes/...` | **[unverified]** — inferred by symmetry |
| Handling/soldering guides | `.../downloads/handling/...` | **[unverified]** — inferred |
| Sensor driver APIs | `https://github.com/boschsensortec/` | ✅ Open source; often better than the datasheet for integration |

**The `ds<NNN>` counter is the catch.** `bst-bme280-ds002.pdf` is document revision 002. There is no
`latest` alias. Increment-probing works but is crude; scraping the product page is correct. The
happy side effect, as with [Winbond](../winbond/README.md#5-documentation-what-exists-and-where), is
that **the URL is itself a pinned revision** — cite it in full.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ✅ Excellent |
| LCSC | ✅ Good for `BME280`/`BMP280`/`BMI160` |
| AliExpress | ⚠️ Breakout modules are cheap and **frequently fitted with `BMP280` sold as `BME280`**, or with clone dies. Verify by chip ID |

---

## 7. Gotchas

- **`BME280` vs `BMP280`.** See §2. Verify by chip-ID register, always.
- **Counterfeit and re-marked sensors are endemic on cheap breakout modules.** A "BME280" that
  reports no humidity is a `BMP280`.
- **`ds<NNN>` revision counter is unguessable.** See §5.
- **Register maps are public but calibration is subtle.** The compensation formulae are integer
  routines given in the datasheet and are easy to implement wrongly. **Use Bosch's own driver API**
  rather than reimplementing — this is the rare case where the vendor's C code is the shortest path
  to correctness.
- **Self-heating.** `BME280` humidity and temperature readings are biased by the sensor's own power
  dissipation and by nearby hot components. A reading that is consistently 1–2 °C high is usually a
  layout problem, not a broken part.

---

## 8. Parts and devices we document

**No README record yet — but we do hold a datasheet.**

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **BMA423** (3-axis accelerometer) | [`components/bosch-sensortec/bma423/artifacts/bma423-datasheet.pdf`](../../components/bosch-sensortec/bma423/artifacts/bma423-datasheet.pdf) | 2,803,247 | ❌ **missing** |

**Provenance, and the scoping caveat that matters:** this PDF was **not** downloaded from Bosch. It
shipped inside `SensorLib/datasheet/` in the vendored copy of [`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib)
bundled in the Waveshare demo archive, and was relocated to a reusable component directory. **The
BMA423 is not fitted on the knob board** — it is one of many parts SensorLib supports. Do not infer
otherwise. See [vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

Writing the `components/bosch-sensortec/bma423/README.md` record is **outstanding work**.

Adjacent record: [MEMSensing MSM261D4030H1CPM](../../components/memsensing/msm261d4030h1cpm/README.md).
---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Bosch Sensortec site | primary | https://www.bosch-sensortec.com/ | 2026-08-24 | HTTP 200 |
| S2 | BME280 datasheet rev. 002 | primary | https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf | 2026-08-24 | **HTTP 200, 1,663,806 bytes, `%PDF` magic** — the datasheet URL pattern, byte-validated |
| S3 | Environmental sensors category | primary | https://www.bosch-sensortec.com/products/environmental-sensors/ | 2026-08-24 | HTTP 200 |

> **Evidence boundary.** S1–S3 are **probes performed 2026-08-24**. S2 is the only one byte-validated.
> The datasheet was **not read** in this pass — §2, §3, §4 and §7 are **general industry knowledge,
> not verified against the retrieved document**, and the chip-ID values (`0x58`/`0x60`) in §2 are
> **recalled, not checked**; confirm them against S2 before relying on them. The application-note and
> handling-guide URL patterns are **[unverified]**. No Bosch document is stored in this repository.

---

## Related

- [Vendor guide index](../README.md) · [MEMSensing](../memsensing/README.md) · [QST](../qst/README.md)
- [Clones and variants](../../guides/markets/clones-and-variants.md)
