# Capella Microsystems — Documentation Sourcing Guide

> **Status: no record yet, but we hold two CM32181 documents (§8) — and a warning.**
> Capella is included because its `CM32181` / `CM3218` ambient-light sensors are common on
> low-cost display boards, and because the vendor's web presence is in a **degraded state** that is
> itself the most useful thing to record.

> **TL;DR** — `https://www.capellamicro.com/` responds (HTTP 200) but serves a **legacy static site**
> — the page title is literally `New Products` and it references an `old.css` stylesheet (verified
> 2026-08-24, S1). The Taiwanese domain `www.capellamicro.com.tw` **does not resolve** (S2), and a
> plausible datasheet path **404s** (S3). **Assume Capella documentation must be sourced from third
> parties, not from Capella.**

---

## 1. Who they are

Capella Microsystems, Inc. (新竹, Hsinchu, Taiwan) designed optical sensors — ambient light sensors,
proximity sensors and UV sensors. **Capella was acquired by Vishay Intertechnology in 2014.**

That acquisition is the key fact. Capella's product line was folded into Vishay's optoelectronics
catalogue, and the surviving `capellamicro.com` site appears to be an unmaintained remnant. For
anything current, **the vendor you actually want is Vishay.**

**[unverified]** The acquisition date and the Vishay relationship are **recalled, not confirmed in
this pass** — the Capella site was not read in enough depth to establish it, and no Vishay source was
probed. Treat §1 as a strong hypothesis to check first.

---

## 2. Product lines

| Prefix | What it is |
|---|---|
| **`CM32xx` / `CM36xx`** | Ambient light sensors (ALS), I²C |
| **`CM36xxx`** | Combined ALS + proximity sensors |
| **`CM3512` / UV parts** | UV index sensors |

These are small, single-function I²C parts: read a lux value, optionally an IR or proximity channel.
They compete directly with [Lite-On's `LTR-3xx`](../lite-on/README.md), Vishay's own `VEML` series,
Rohm's `BH1750` and AMS/TAOS `TSL2561`.

**Relevance to this repository:** none of our documented devices carries an ambient-light sensor.
Should one appear — an auto-brightness display board is the obvious case — this is one of four or
five vendors it will come from.

---

## 3. Market position

Historically low-cost Taiwanese optical sensing; **now effectively a Vishay sub-brand.** The parts
remain in circulation and in Linux kernel drivers (`cm32181`, `cm3232`, `cm3605` are in-tree IIO
drivers), so they are far from dead in software terms even where the vendor presence has faded.

---

## 4. Part numbering

```
CM 32 181
│  │  └─ Variant index
│  └──── Family / generation
└─────── CM = Capella Micro
```

**[inference]** — no numbering key located, and given the site's state, unlikely to be recoverable
from the vendor.

---

## 5. Documentation: where to actually look

Because the vendor site is degraded, the ordering here is unusually important.

| Rank | Source | Notes |
|---|---|---|
| 1 | **Vishay** | The acquirer. Search Vishay's optoelectronics catalogue for the part or its successor. Vishay documents well |
| 2 | **Linux kernel** | `drivers/iio/light/cm32181.c` and siblings, plus `Documentation/devicetree/bindings/iio/light/`. In-tree, maintained, and describes the register set by construction |
| 3 | **LCSC / distributor mirrors** | The [MEMSensing pattern](../memsensing/README.md#5-documentation-where-it-actually-comes-from) |
| 4 | **Datasheet aggregators** | Unreliable provenance; verify the title block |
| 5 | `https://www.capellamicro.com/` | ✅ responds, but is a legacy static site (S1). A guessed `/PDF/CM32181_ver8_pub.pdf` **404s** (S3) |

**Do not spend long on rank 5.** The evidence says it will not repay the effort.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ⚠️ Under **Vishay** part numbers, if at all |
| LCSC | ⚠️ Some `CM32xx` stock |
| AliExpress | ⚠️ As breakout modules, often mislabelled |

**[unverified]** — availability was not probed.

---

## 7. Gotchas

- **The vendor is effectively gone.** Go to Vishay or to the kernel. See §1 and §5.
- **`capellamicro.com.tw` does not resolve** (S2). A dead Taiwanese domain is not evidence the part
  is undocumented — it is evidence the company moved.
- **Ambient light sensors are not interchangeable even when the interface matches.** Lux scaling,
  integration time and IR rejection differ substantially between `CM32181`, `BH1750` and `LTR-303`.
  Swapping one for another changes your readings, not just your driver.
- **Cover-glass transmittance dominates accuracy.** A calibrated ALS behind an uncharacterised tinted
  window is uncalibrated. This is a mechanical problem more than an electrical one.
- **Watch for `CM3218` vs `CM32181`.** Similar numbers, different parts — the same trap as
  [`BME280`/`BMP280`](../bosch-sensortec/README.md#2-product-lines).

---

## 8. Parts and devices we document

**No README record yet — but we hold two CM32181 documents**, which is more than the vendor's own
site would have given us (§5).

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **CM32181** (ambient light sensor) | [`.../cm32181a3op-datasheet.pdf`](../../components/capella-microsystems/cm32181/artifacts/cm32181a3op-datasheet.pdf) | 977,240 | ❌ **missing** |
| CM32181 application note ("for Archtech") | [`.../cm32181-application-note-archtech.pdf`](../../components/capella-microsystems/cm32181/artifacts/cm32181-application-note-archtech.pdf) | 716,648 | ❌ **missing** |

Note the datasheet is for the **`CM32181A3OP`** ordering variant — a reminder that §4's numbering
decode has a package/variant suffix we did not account for.

**This is the vindication of §5's ranking:** the vendor site 404'd our guessed datasheet path, and
the documents turned up bundled in a third-party library instead.

**Provenance:** both shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive.
**The CM32181 is not fitted on the knob board.** See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

There is also a related generic record directory,
[`components/generic/ambient-light-and-proximity-sensor-selection/`](../../components/generic/ambient-light-and-proximity-sensor-selection/artifacts/ambient-light-and-proximity-sensor-selection-zh.pdf)
— a Chinese-language ALS/proximity **selection guide** (1,075,546 bytes) from the same bundle.

Writing these records is **outstanding work**.
---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Capella Microsystems site | primary | https://www.capellamicro.com/ | 2026-08-24 | HTTP 200; `<TITLE>New Products</TITLE>`; references `old.css` — a legacy, apparently unmaintained static site |
| S2 | **Negative probe** — Taiwanese domain | probe | https://www.capellamicro.com.tw/ | 2026-08-24 | **Does not resolve** (connection failure, no HTTP status). A probe of `http://www.capellamicro.com.tw/en/` returned **404** |
| S3 | **Negative probe** — guessed datasheet path | probe | https://www.capellamicro.com/PDF/CM32181_ver8_pub.pdf | 2026-08-24 | **HTTP 404** |

> **Evidence boundary.** S1–S3 are **HTTP probes performed 2026-08-24** and are the *only* verified
> content in this guide. **No Capella document has been retrieved or read.** The Vishay acquisition
> (§1), the product-line table (§2), the market position (§3), the numbering decode (§4) and every
> gotcha in §7 are **recalled general knowledge, explicitly unverified.** This guide is a
> starting point for a future research pass, not a finished record — it should be revised the first
> time anyone actually needs a Capella part.

---

## Related

- [Vendor guide index](../README.md) · [Lite-On](../lite-on/README.md) — the closest competitor, in a similar state
- [Marketplace comparison](../../guides/markets/vendor-comparison.md)
