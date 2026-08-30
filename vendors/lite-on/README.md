# Lite-On — Documentation Sourcing Guide

> **Status: no record yet; vendor unreachable; but we hold a datasheet anyway.** There is no Lite-On
> component record here, and **we could not reach Lite-On's web presence at all** in this pass — yet
> an `LTR-553ALS-01` datasheet is retained, obtained from a bundled third-party library (§8).

> **TL;DR** — Every Lite-On host probed on 2026-08-24 **failed to connect** — not a 403, not a 404,
> but no HTTP response at all: `https://www.liteon.com/`, `https://www.liteon.com/en-us`,
> `https://optoelectronics.liteon.com/`, `https://optoelectronics.liteon.com/en-global`, and a
> plausible `LTR-303ALS-01` datasheet path (S1–S3). `https://www.lite-on.com/` returned an **empty
> body** (S4). **Plan to source Lite-On documentation from third parties.**

---

## 1. Who they are

Lite-On Technology Corporation (光寶科技, Taipei; TWSE 2301) is a large Taiwanese electronics group.
Its relevance to boards of the kind this repository documents is the **optoelectronics** division:
LEDs, infrared emitters and detectors, optocouplers, and — the parts you are most likely to be
chasing — the **`LTR-` series ambient light and proximity sensors**.

Lite-On is a *component* vendor here. (The group also makes power supplies, optical drives and
mechanical assemblies, none of which are in scope.)

---

## 2. Product lines

| Prefix | What it is |
|---|---|
| **`LTR-3xx`** | Ambient light sensors — `LTR-303ALS-01`, `LTR-329ALS`, `LTR-390UV` |
| **`LTR-5xx` / `LTR-55x`** | Proximity + ALS combos |
| **`LTV-` / `LTV-8xx`** | Optocouplers / photocouplers |
| **`LTST-`** | Chip LEDs (SMD indicator LEDs) |
| **`LTE-` / `LTR-` IR** | IR emitters and photodetectors |

**How they fit together:** Lite-On is an *optoelectronics* house — everything is light in or light
out. The `LTR-390UV` (ALS + UV) and `LTR-329ALS` in particular are widely used on hobbyist
environmental boards, and the `LTST-` chip LEDs are the generic indicator LEDs on a great many
designs, usually specified by colour and package rather than by part number.

Direct competitors: [Capella](../capella-microsystems/README.md) (also in a degraded state),
Vishay `VEML`, Rohm `BH1750`, AMS `TSL`/`TMD` series.

---

## 3. Market position

High volume, low cost, Taiwanese, and largely invisible — Lite-On parts are specified by design
houses and rarely thought about again. Documentation has historically been adequate: real
English datasheets with proper part numbers and revision codes, distributed through
`optoelectronics.liteon.com`.

**[unverified]** That last statement is **recalled, not verified** — we could not reach the site to
check (§9).

---

## 4. Part numbering

```
LTR - 303 ALS - 01
│     │   │     └─ Package / bin / variant code
│     │   └─────── Function tag: ALS = ambient light sensor, UV, PS = proximity
│     └─────────── Series index
└───────────────── LTR = Lite-On receiver/sensor family (LTV = optocoupler, LTST = LED)
```

The useful rule is the **prefix**: `LTR` = sensor/receiver, `LTV` = optocoupler, `LTST` = SMD LED,
`LTE` = emitter. **[inference]** — no numbering key retrieved.

---

## 5. Documentation: where to actually look

Given §9, the vendor is **not** the recommended starting point.

| Rank | Source | Notes |
|---|---|---|
| 1 | **Linux kernel** | `drivers/iio/light/ltr501.c`, `ltrf216a.c` and device-tree bindings. In-tree and maintained |
| 2 | **Mouser / Digi-Key product pages** | These distributors host manufacturer datasheet PDFs on their own CDNs. Note both **block scripted access** (403) per the repository's [crawler table](../../ai-crawler-site-access-table.md#electronics-distributors--parts-catalogues) — Mouser's Search API is the intended path |
| 3 | **LCSC mirror** | `https://datasheet.lcsc.com/lcsc/...` — the [MEMSensing pattern](../memsensing/README.md#5-documentation-where-it-actually-comes-from). **Recommended first attempt**, since LCSC is scriptable |
| 4 | **`web.archive.org`** | Given the site is unreachable, an archived capture of `optoelectronics.liteon.com` is a realistic route. Worth a `https://web.archive.org/web/*/optoelectronics.liteon.com/*` query |
| 5 | Lite-On direct | ❌ Unreachable in this pass (S1–S4) |

### Historical URL shape

Lite-On datasheets were served from paths of roughly the form
`https://optoelectronics.liteon.com/upload/download/<DOC-ID>/<PART>_DS_V<n>.pdf`.
**[unverified]** — a probe of exactly this shape produced **no connection** (S3), so this is recorded
as a shape to try against an archive, not as a working pattern.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ✅ Well catalogued (but see §5 rank 2 on scripted access) |
| LCSC | ✅ Good, especially `LTST-` LEDs |
| AliExpress | ✅ As modules |

**[unverified]** — not probed.

---

## 7. Gotchas

- **The vendor site is unreachable from here.** Whether this is a geographic block, a transient
  outage, or a decommissioning is **not determined**. Do not record "Lite-On has no documentation" —
  record "we could not reach it on 2026-08-24".
- **`liteon.com` vs `lite-on.com`.** Both exist as names; the hyphenated one at least resolved, but
  returned an empty body (S4). Try both.
- **ALS parts are not interchangeable.** Same caution as
  [Capella §7](../capella-microsystems/README.md#7-gotchas): lux scaling and IR rejection differ.
- **`LTST-` LED part numbers encode colour and bin**, and a "same" LED with a different bin code has
  a visibly different brightness and dominant wavelength. This matters for a product with a visible
  indicator.
- **Optocoupler CTR degrades with age and current.** `LTV-8xx` design margins must account for it;
  a datasheet CTR is an initial value.

---

## 8. Parts and devices we document

**No README record yet — but we hold an LTR-553ALS-01 datasheet**, which is fortunate given that
every Lite-On host was unreachable (§9).

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **LTR-553ALS-01** (ambient light + proximity sensor) | [`components/lite-on/ltr-553als-01/artifacts/ltr-553als-01-datasheet.pdf`](../../components/lite-on/ltr-553als-01/artifacts/ltr-553als-01-datasheet.pdf) | 741,439 | ❌ **missing** |

**This is the practical answer to §7's warning.** We could not reach the vendor, and we have the
document anyway — because it was bundled downstream. Note the part is an **ALS + proximity combo**
(`LTR-55x`), not the `LTR-3xx` ALS-only part guessed at in §5's URL probe.

**Provenance:** it shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive.
**The LTR-553ALS-01 is not fitted on the knob board.** See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

Writing the `components/lite-on/ltr-553als-01/README.md` record is **outstanding work**.
---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | **Negative probe** — main site | probe | https://www.liteon.com/ and https://www.liteon.com/en-us | 2026-08-24 | **Connection failure**, no HTTP status returned |
| S2 | **Negative probe** — optoelectronics subdomain | probe | https://optoelectronics.liteon.com/ and `/en-global` | 2026-08-24 | **Connection failure**, no HTTP status |
| S3 | **Negative probe** — guessed datasheet path | probe | https://optoelectronics.liteon.com/upload/download/DS86-2015-0004/LTR-303ALS-01_DS_V1.pdf | 2026-08-24 | **Connection failure** |
| S4 | Hyphenated domain | probe | https://www.lite-on.com/ | 2026-08-24 | Resolved but returned an **empty body** and no usable title |

> **Evidence boundary.** S1–S4 are **negative probes performed 2026-08-24 with a Chrome
> User-Agent**; **UA rotation was not attempted** against these hosts, so the failures are not
> confirmed to be UA-independent. Per the repository's
> [retrieval policy](../../AGENTS.md), a future pass should rotate UAs before accepting this
> result. **No Lite-On document has been retrieved or read.** Everything in §1–§4, §6 and §7 is
> **recalled general knowledge, explicitly unverified.** This guide is a research lead, not a record.

---

## Related

- [Vendor guide index](../README.md) · [Capella Microsystems](../capella-microsystems/README.md)
- [Repository crawler / site-access table](../../ai-crawler-site-access-table.md)
- [Marketplace comparison](../../guides/markets/vendor-comparison.md)
