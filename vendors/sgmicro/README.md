# SGMicro — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation for **any** SGMicro analog part.

> **TL;DR** — SGMicro is the pleasant surprise among Chinese analog vendors: a clean, guessable
> product-page pattern (`https://www.sg-micro.com/product/<PART>`, verified 2026-08-24, S2) and real
> English datasheets with revision letters and dates (`SGM2036 datasheet, rev. B.2, November 2021`,
> S3). Treat it as the counter-example to the "Chinese vendor = no docs" assumption.

---

## 1. Who they are

SG Micro Corp (圣邦微电子, Beijing; SSE STAR Market 300661) is a fabless analog semiconductor company.
Their strategy is transparent and worth understanding because it tells you exactly how to use their
catalogue: **SGMicro builds pin-and-function-compatible alternatives to Western analog parts**,
principally [TI](../texas-instruments/README.md), Analog Devices, and Maxim, at lower cost.

They are a *component* vendor; they appear only in
[`components/`](../../components/README.md).

---

## 2. Product lines

| Line | What it is | Relevance |
|---|---|---|
| **`SGM20xx` / `SGM21xx` — LDO regulators** | Low-dropout linear regulators, many low-noise | [SGM2036-3.3](../../components/sgmicro/sgm2036-3.3/README.md) |
| **`SGM61xx` / `SGM63xx` — switching regulators** | Buck, boost, buck-boost | Competes with [TI's `TLV62xxx`](../../components/texas-instruments/tlv62569dbvt/README.md) |
| **`SGM8xxx` — op-amps and comparators** | General-purpose through precision | The core of the catalogue by part count |
| **`SGM4xxx` — interface / switches** | Analog switches, level shifters, muxes | Competes with [WCH `CH44x`](../../components/wch/ch445p/README.md) and TI `TS3A` |
| **`SGM3xxx` — display / LED drivers, charge pumps** | Backlight, charge pumps | |
| **`SGM7xxx` — audio** | Headphone amps, class-D | |

**How they fit together:** the numbering blocks map to function almost exactly as TI's do — because
they are largely tracking TI's catalogue. If you know the TI part you want, there is a reasonable
chance an SGMicro equivalent exists and that its datasheet is structured similarly.

---

## 3. Market position

**The deliberate second source.** SGMicro parts are chosen when the design needs a specific analog
function and the TI or ADI original is too expensive for the BOM. They are *not* counterfeits or
grey-market re-marks — they are legitimate competing designs, often with their own improvements.

The BOM-reading signal is the mirror image of the [TI](../texas-instruments/README.md) one: **an
SGMicro part is where the designer decided the function mattered but the brand did not.** Our knob
board illustrates the split precisely — TI silicon for the DAC, haptics and main buck rail, SGMicro
for the low-noise LDO feeding the DAC's analog rail. That is a considered division, not a random one.

---

## 4. Part numbering

```
SGM 2036 - 3.3 Y N5 G / TR
│   │      │    │  │  │   └─ Packaging: TR = tape & reel
│   │      │    │  │  └───── G = green / RoHS
│   │      │    │  └──────── Package code (N5 = SOT-23-5 and similar)
│   │      │    └─────────── Temperature/grade letter
│   │      └──────────────── **Fixed output voltage** — the key field for regulators
│   └─────────────────────── Base part number; leading digit ≈ function class
└─────────────────────────── SGMicro prefix
```

Rules:

- **For regulators, the `-x.x` suffix is the fixed output voltage**, and it is the most important part
  of the number. `SGM2036-3.3` is the 3.3 V fixed variant; an adjustable variant typically carries
  `-ADJ`.
- **The base number's leading digits track function** — see the §2 table.
- **The datasheet is per *base* part, not per voltage option.** Look up `SGM2036`; the document covers
  every voltage option in one table. This mirrors the
  [TI suffix-stripping rule](../texas-instruments/README.md#7-gotchas).
- **[inference]** for the package/grade letters specifically — the general shape is confirmed by the
  SGM2036 datasheet's ordering table, but we have not verified each letter across the catalogue.

---

## 5. Documentation: URL patterns

| Document class | Pattern | Verified |
|---|---|---|
| Corporate site | `https://www.sg-micro.com/` | ✅ 2026-08-24 (S1) |
| **Product page** | `https://www.sg-micro.com/product/<PART>` | ✅ 2026-08-24 (S2) — uppercase base part, **no voltage suffix** |
| Datasheet PDF | Linked from the product page; asset path is **not** guessable | Scrape it |
| Selection guides | Published as catalogue PDFs | |

### The reliable procedure

1. `https://www.sg-micro.com/product/SGM2036` — guessable, uses the **base** part.
2. Scrape the datasheet asset URL from that page.
3. **Record the revision letter and date from the PDF's cover** — SGMicro versions properly
   (`rev. B.2, November 2021`) which is more than several vendors here manage. The URL alone does not
   pin the revision.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| **LCSC** | ✅ Excellent — the primary channel; JLCPCB stocks the common parts |
| Taobao / AliExpress | ✅ |
| Mouser / Digi-Key | ⚠️ Limited but **non-zero and growing** — SGMicro has been pushing into Western distribution |
| SGMicro direct | Samples via contact form |

---

## 7. Gotchas

- **Product page wants the base part, not the voltage variant.** `product/SGM2036`, not
  `product/SGM2036-3.3`.
- **SGMicro soft-404s.** A nonexistent part path returns **HTTP 200** with a ~69 KB page, versus
  ~590 KB for a real one (S2/S3, 2026-08-24). **Never trust the status code** — compare body size or
  look for the part number in the body. This is a milder version of the
  [WCH SPA-shell problem](../wch/README.md#7-gotchas).
- **The datasheet asset URL is not guessable** even though the product-page URL is. Scrape, don't
  construct.
- **"Pin-compatible with X" is a claim to verify, not to assume.** SGMicro's alternatives are usually
  genuinely drop-in, but dropout voltage, quiescent current, PSRR and output-capacitor stability
  requirements can differ from the part they replace. For an LDO feeding an audio DAC — exactly our
  case — **PSRR and output noise are the whole point**, so check them specifically rather than
  trusting the pin-compatibility headline.
- **Output capacitor requirements matter.** Many low-noise LDOs are only stable across a specified
  ESR/capacitance window. Substituting an SGMicro part for a TI one without checking this is a
  classic field-failure cause.
- **Chinese and English datasheets both exist**; where they disagree, the Chinese one is usually
  newer.
- **Not a counterfeit vendor — do not confuse SGMicro with re-marked parts.** Genuine SGMicro silicon
  bought through LCSC is exactly what it says it is. The counterfeit risk in this repository attaches
  to [TI](../texas-instruments/README.md#6-distribution) and
  [Alps](../alps-alpine/README.md#7-gotchas) parts, not to this vendor.

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [SGM2036-3.3](../../components/sgmicro/sgm2036-3.3/README.md) | Low-noise 3.3 V LDO, `U20`, feeds the `3V3_DAC` rail | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |

Related power-tree records:
[TI TLV62569DBVT](../../components/texas-instruments/tlv62569dbvt/README.md) (the main `3V3` buck) ·
[charger / power-path](../../components/generic/charger-power-path/README.md) ·
[LiPo 102035](../../components/generic/lipo-102035/README.md) ·
[AOS AO3400A](../../components/alpha-and-omega-semiconductor/ao3400a/README.md).

No device in this repository is manufactured by SGMicro.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | SGMicro corporate site | primary | https://www.sg-micro.com/ | 2026-08-24 | HTTP 200 |
| S2 | SGM2036 product page | primary | https://www.sg-micro.com/product/SGM2036 | 2026-08-24 | HTTP 200, 590,614 bytes — the `product/<PART>` pattern resolves with the **base** part |
| S3 | **Negative control** — nonexistent part | probe | https://www.sg-micro.com/product/BOGUS999 | 2026-08-24 | **HTTP 200, 69,130 bytes.** SGMicro **soft-404s**: a nonexistent part still returns 200. Distinguish by body size / content, never by status code |
| S4 | SGM2036 datasheet, rev. B.2, November 2021 | primary | Asset linked from S2; see the [component record §8](../../components/sgmicro/sgm2036-3.3/README.md) | 2026-08-23 | The part's specifications and the revision-lettering convention |

> **Evidence boundary.** S1–S3 are **probes performed 2026-08-24**; S3 is a deliberate negative
> control establishing the soft-404 behaviour. S4 was retrieved 2026-08-23 during the component pass
> and its asset URL is recorded in the component record rather than duplicated here. §3 (market
> position and strategy) is **inference** from the catalogue's shape and the parts we hold — SGMicro
> does not describe itself this way in marketing material. §4's package/grade letters are marked
> **[inference]**.

---

## Related

- [Vendor guide index](../README.md)
- [SGM2036-3.3](../../components/sgmicro/sgm2036-3.3/README.md)
- [Texas Instruments](../texas-instruments/README.md) — the catalogue SGMicro tracks, and the other half of our power tree
- [Alpha & Omega Semiconductor](../alpha-and-omega-semiconductor/README.md)
