# QST (QST Corporation / 矽睿科技) — Documentation Sourcing Guide

> **Status: no records yet, but we hold two QST datasheets (§8).** QST is also included because its
> `QMC5883L` magnetometer and `QMI8658` IMU are among the most commonly encountered sensors on
> low-cost ESP32 boards, and because it is a textbook case of the **"cloned part number"** problem
> described in [clones-and-variants.md](../../guides/markets/clones-and-variants.md).

> **TL;DR** — `https://www.qstcorp.com/` is live and **Chinese-first** (title 上海矽睿科技股份有限公司,
> HTTP 200, verified 2026-08-24, S1); an English tree exists at `/en/` (S2). A guessed product path
> `/en_product_info/QMC5883L` **404s** (S3) — the URL scheme was not determined in this pass.

---

## 1. Who they are

QST Corporation — 上海矽睿科技股份有限公司, Shanghai — is a Chinese sensor company founded 2012,
describing itself as focused on high-quality sensor products (S1). They make magnetometers,
accelerometers, gyroscopes, IMUs and pressure sensors.

QST is a *component* vendor.

---

## 2. Product lines

| Prefix | What it is | Notable parts |
|---|---|---|
| **`QMC`** | Magnetometers / compasses | `QMC5883L`, `QMC6310` |
| **`QMA`** | Accelerometers | `QMA6100`, `QMA7981` |
| **`QMI`** | IMUs (accel + gyro) | `QMI8658`, `QMI8610` |
| **`QMP`** | Pressure sensors | |

The prefix convention mirrors [Bosch's](../bosch-sensortec/README.md#4-part-numbering) third-letter
scheme closely enough that it is clearly deliberate: `QM` + a type letter. That similarity is not an
accident and leads directly to §3.

---

## 3. Market position — and the `HMC5883L` story

QST's position is **the low-cost alternative to Bosch, ST and Honeywell**, and the `QMC5883L` is the
clearest illustration of how that plays out in practice.

Honeywell's `HMC5883L` was a widely-used 3-axis magnetometer that went end-of-life. QST's `QMC5883L`
appeared with **a nearly identical part number, the same package and the same pinout — but a
different I²C address and a different register map.**

The consequence, which has burned a very large number of people: **breakout boards sold as "HMC5883L"
on AliExpress are overwhelmingly fitted with `QMC5883L`.** Code written against Honeywell's datasheet
silently fails. The fix is to probe both addresses and branch.

This is worth internalising as a general pattern, not just a fact about one part: **a Chinese
part number that differs from a discontinued Western one by a single letter is a compatibility
claim about the *pinout*, not about the *registers*.**

---

## 4. Part numbering

```
QM C 5883 L
│  │ │    └─ Variant / package suffix
│  │ └────── Series index — here, deliberately echoing the Honeywell part it replaces
│  └──────── Type: C=compass/magnetometer, A=accelerometer, I=IMU, P=pressure
└─────────── QM = QST MEMS
```

**[inference]** — no QST numbering key located.

---

## 5. Documentation

| Source | Pattern | Status |
|---|---|---|
| Corporate site (CN) | `https://www.qstcorp.com/` | ✅ HTTP 200, Chinese-first (S1) |
| English tree | `https://www.qstcorp.com/en/` | ✅ HTTP 200 (S2) |
| Product page | *unknown* | ❌ A guessed `/en_product_info/<PART>` **404s** (S3) |
| **LCSC datasheet mirror** | `https://datasheet.lcsc.com/lcsc/..._QST-<PART>_C<NNNNN>.pdf` | **[unverified]** but this is the pattern that worked for [MEMSensing](../memsensing/README.md#5-documentation-where-it-actually-comes-from) and is the **recommended first attempt** |
| Community drivers | Linux `qmc5883l` in-tree; many Arduino/ESP-IDF libraries | Often the most usable description of the registers |

**Recommended procedure:** treat this exactly like [MEMSensing](../memsensing/README.md) — **go to
LCSC first**, search by part number, take the mirrored datasheet and record the `C`-code. The
manufacturer site is a fallback, not a starting point.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| **LCSC** | ✅ The primary channel |
| Taobao / AliExpress | ✅ Very common, usually as breakout modules |
| Mouser / Digi-Key | ❌ Essentially absent |

---

## 7. Gotchas

- **`QMC5883L` is not `HMC5883L`.** See §3. Different I²C address, different registers, same pinout.
- **Modules are mislabelled as a matter of routine.** The silkscreen, the listing title and the fitted
  die frequently disagree. **Probe the bus and read the chip ID.**
- **Chinese-first documentation.** English datasheets exist for the popular parts but lag.
- **URL scheme undetermined.** See §5 — this is an open gap in this guide, not a claim that no
  product pages exist.
- **Magnetometers need calibration in situ.** Hard- and soft-iron distortion from the board's own
  copper, battery and speaker magnet dominate the error budget. A datasheet accuracy figure is not
  achievable without on-board calibration, regardless of vendor.

---

## 8. Parts and devices we document

**No README records yet — but we hold two QST datasheets, both revision-stamped.**

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **QMC6310** (3-axis magnetometer), Rev. C | [`components/qst/qmc6310/artifacts/qmc6310-datasheet-rev-c.pdf`](../../components/qst/qmc6310/artifacts/qmc6310-datasheet-rev-c.pdf) | 884,797 | ❌ **missing** |
| **QMI8658A** (6-axis IMU), Rev. A | [`components/qst/qmi8658a/artifacts/qmi8658a-datasheet-rev-a.pdf`](../../components/qst/qmi8658a/artifacts/qmi8658a-datasheet-rev-a.pdf) | 3,085,534 | ❌ **missing** |

These **confirm §2's prefix convention** (`QMC` = magnetometer, `QMI` = IMU) with real documents, and
they mean the LCSC-first advice in §5 was not needed here — the documents arrived bundled downstream.

⚠️ **Note what we do *not* have: the `QMC5883L`.** The entire `HMC5883L` narrative in §3 — the most
load-bearing claim in this guide — **remains unverified**, and these two datasheets do not bear on it.

**Provenance:** both shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive.
**Neither part is fitted on the knob board.** See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

Writing these records is **outstanding work**.
---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | QST corporate site | primary | https://www.qstcorp.com/ | 2026-08-24 | HTTP 200; title 上海矽睿科技股份有限公司; founded 2012; sensor positioning (from the page's `meta description`) |
| S2 | QST English tree | primary | https://www.qstcorp.com/en/ | 2026-08-24 | HTTP 200 |
| S3 | **Negative probe** — guessed product path | probe | https://www.qstcorp.com/en_product_info/QMC5883L | 2026-08-24 | **HTTP 404** — the guessed scheme is wrong |

> **Evidence boundary.** S1–S3 are **HTTP probes performed 2026-08-24**; only the site's existence,
> language and one negative path result are established. **No QST document has been retrieved or
> read.** §2, §3, §4 and §7 — including the entire `HMC5883L`/`QMC5883L` narrative, which is the most
> load-bearing claim in this guide — are **recalled general knowledge, not verified in this pass.**
> The `HMC5883L` substitution story is widely reported in community sources but is **not sourced to a
> primary document here.** Confirm the address and register differences against a datasheet before
> acting on them.

---

## Related

- [Vendor guide index](../README.md) · [MEMSensing](../memsensing/README.md) · [Bosch Sensortec](../bosch-sensortec/README.md)
- [Clones and variants](../../guides/markets/clones-and-variants.md) — the "near-identical part number" pattern
