# XLSEMI (Shanghai Xinlong Semiconductor) — Documentation Sourcing Guide

> **Status: no record yet, but we hold an XL9555 datasheet (§8) — which corrects §2 of this guide.**
> XLSEMI is also included because
> its `XL` power-converter parts — especially the `XL6009` boost and the `SY8xxx`-class buck
> converters it competes with — are ubiquitous on cheap Chinese power modules, and because it is a
> representative example of the **Chinese-language-only vendor** documentation problem.

> **TL;DR** — `https://www.xlsemi.com/` is live and **Chinese-only** (title
> 上海芯龙半导体技术股份有限公司, HTTP 200, verified 2026-08-24, S1). No English tree was found. A
> guessed `/products/` path **404s** and so does `/product.html` (S2, S3) — the URL scheme was **not
> determined** in this pass.

---

## 1. Who they are

Shanghai Xinlong Semiconductor Technology Co., Ltd. — 上海芯龙半导体技术股份有限公司, trading as
**XLSEMI** — is a Chinese fabless analog company specialising in **power management**: DC-DC
converters, LED drivers and battery charging ICs. Listed on the Shanghai STAR Market.

XLSEMI is a *component* vendor.

---

## 2. Product lines

| Prefix | What it is | Notable parts |
|---|---|---|
| **`XL` — DC-DC converters** | Step-down (buck) and step-up (boost), typically 1–5 A | `XL4015` (5 A buck), `XL6009` (boost), `XL1509`, `XL4005` |
| **`XL` — LED drivers** | Constant-current, for lighting and backlight | `XL6003`, `XL7015` |
| **Battery charging** | Li-ion charger ICs | |

**How they fit together:** XLSEMI's catalogue is narrow and coherent — high-current switching
regulators in through-hole and simple SMD packages, aimed at the cost-driven power-module market.
These are the chips on the small blue "LM2596-style" adjustable buck boards sold by the thousand.

**Relevance to this repository:** none of our documented boards uses an XLSEMI part. Our power tree
is [TI](../texas-instruments/README.md) + [SGMicro](../sgmicro/README.md) + [AOS](../alpha-and-omega-semiconductor/README.md),
which is a **noticeably higher-specification choice** than the XLSEMI tier. That contrast is itself a
useful data point when reading a BOM: an XLSEMI part signals a cost-first power design.

---

## 3. Market position

**Bottom of the market by price, and openly so.** XLSEMI parts compete on cost against Silergy
(`SY8` series), Monolithic Power (`MP` series) and the enormous installed base of second-source
`LM2596` clones.

Documentation quality is the weak point and the reason this guide exists: datasheets are typically
**Chinese-only**, short, and light on the application detail (loop compensation, layout guidance,
thermal derating curves) that a Western vendor would consider mandatory. The parts generally work as
advertised; designing *robustly* with them requires more measurement and less reading.

**[unverified]** — the datasheet-quality characterisation is **recalled, not verified in this pass.**
No XLSEMI datasheet was retrieved.

---

## 4. Part numbering

```
XL 4015
│  └─ Series index — loosely encodes topology and current class
└──── XL = XLSEMI
```

There is no decodable grammar beyond the prefix. **`XL4015` (buck) and `XL6009` (boost) differ in
topology with no hint in the number** — you must look each part up. **[inference]**.

---

## 5. Documentation

| Source | Status |
|---|---|
| Corporate site | `https://www.xlsemi.com/` (and `http://`) — ✅ HTTP 200, **Chinese-only** (S1) |
| Product index | `https://www.xlsemi.com/products/` — ❌ **404** (S2); `https://www.xlsemi.com/product.html` — ❌ **404** (S3) |
| English tree | **Not found** |
| **LCSC mirror** | **[unverified]** but the **recommended first attempt** — the [MEMSensing pattern](../memsensing/README.md#5-documentation-where-it-actually-comes-from) |
| Datasheet aggregators | Widely mirrored for the popular parts (`XL4015`, `XL6009`); provenance poor |

**Recommended procedure:** LCSC first, aggregators second, vendor site last — and expect to read
Chinese when you get there. Machine translation of a datasheet's *parameter tables* is generally
safe; machine translation of its *application notes* is not, because the technical idiom translates
badly. Where a translated claim matters, verify by measurement.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| **LCSC / Taobao** | ✅ The primary channels |
| AliExpress | ✅ Overwhelmingly as **finished buck/boost modules** rather than loose ICs |
| Mouser / Digi-Key | ❌ Absent |

---

## 7. Gotchas

- **Chinese-only documentation.** The defining characteristic. See §5.
- **URL scheme undetermined.** Recorded as an open gap, not as absence.
- **Module ratings are optimistic.** The single most important practical warning about this tier of
  part: a module sold as "5 A" using an `XL4015` will require substantial heatsinking and airflow to
  approach that, and the bundled inductor is frequently undersized. **Derate aggressively** — 50 % of
  the advertised current is a reasonable starting assumption.
- **Counterfeit and re-marked `XL` parts exist**, including parts marked `XL4015` that are a
  different die entirely.
- **No thermal derating curves.** You will have to characterise it yourself.
- **Input capacitor quality is frequently the failure point** on these modules, not the IC.

---

## 8. Parts and devices we document

**No README record yet — but we hold an XL9555 datasheet**, which is fortunate given that the
vendor's URL scheme was never determined (§5).

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **XL9555** (16-bit I²C I/O expander), Rev. 2.3 | [`components/xlsemi/xl9555/artifacts/xl9555-datasheet-rev-2.3.pdf`](../../components/xlsemi/xl9555/artifacts/xl9555-datasheet-rev-2.3.pdf) | 589,855 | ❌ **missing** |

⚠️ **This corrects §2 of this guide.** The XL9555 is an **I/O expander**, not a power-management
part — a `PCA9555`/`TCA9555` work-alike. XLSEMI's catalogue is therefore **broader than the
"DC-DC converters and LED drivers" characterisation in §2**, which was inference and is now known to
be incomplete. The `XL` prefix spans more functions than assumed, reinforcing §4's point that the
numeric block carries no decodable topology hint.

**Provenance:** it shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive.
**The XL9555 is not fitted on the knob board.** See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

Writing the `components/xlsemi/xl9555/README.md` record is **outstanding work**.
---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | XLSEMI corporate site | primary | https://www.xlsemi.com/ (and `http://www.xlsemi.com/`) | 2026-08-24 | HTTP 200 on both; title 上海芯龙半导体技术股份有限公司; Chinese-only |
| S2 | **Negative probe** | probe | https://www.xlsemi.com/products/ | 2026-08-24 | **HTTP 404** |
| S3 | **Negative probe** | probe | https://www.xlsemi.com/product.html | 2026-08-24 | **HTTP 404** |

> **Evidence boundary.** S1–S3 are **HTTP probes performed 2026-08-24**. Only the site's existence,
> its language, and two negative path results are established. **No XLSEMI document has been
> retrieved or read**, and no XLSEMI part has been handled or measured. §2, §3, §4, §6 and §7 are
> **recalled general knowledge, explicitly unverified** — the derating advice in §7 in particular is
> **engineering judgement about this class of module, not a measurement of any specific part.**

---

## Related

- [Vendor guide index](../README.md)
- [SGMicro](../sgmicro/README.md) — the tier above, and the counter-example of a well-documented Chinese analog vendor
- [Texas Instruments](../texas-instruments/README.md) · [Clones and variants](../../guides/markets/clones-and-variants.md)
