# DinMeter v1.1 — product history and family

Full family treatment, the M5Dial/Capsule/AirQ relationship, culture and the naming traps are in
**[`../dinmeter/product-history-and-family.md`](../dinmeter/product-history-and-family.md)**.

---

## The v1.1 timeline

| Date | Event | Evidence |
|---|---|---|
| 2023-02-10 | Stamp-S3 (`S007`) listed | shop `.js` |
| 2024-03-08 | **DinMeter (`K134`) listed**, USD 24.50 | shop `.js` |
| **2025-09-11** | **Stamp-S3A (`S007-…-V033`) listed**, USD 7.50 | shop `.js` |
| **2026-01-30** | **DinMeter v1.1 (`K134-V11`) announced.** Shop `created_at 10:02:16+08:00`, `published_at 12:30:47+08:00`; official r/M5Stack weekly post the same day | shop `.js` + Reddit — **two independent sources** |
| 2026-09-04 | Observed: `K134` and `S007` **both `[EOL]` and out of stock**; `K134-V11` and `S007-V033` in stock | shop `.js` |

## What the ordering tells you

**The module came first, by 4½ months.** Stamp-S3A shipped 2025-09-11; the DinMeter v1.1
followed on 2026-01-30; and the Stamp-S3 and DinMeter K134 went end-of-life **together**.

That is a **module-lifecycle event**, not a product refresh. Every other artefact agrees:

| Signal | Reading |
|---|---|
| No v1.1 schematic — the file served is byte-identical to v1.0's | the carrier was not redesigned |
| No v1.1 STL — byte-identical to v1.0's | the enclosure was not redesigned |
| No new KiCad footprint for the Stamp-S3A | the module drops into the same pads |
| `M5DinMeter` library still `1.0.0` (2024-03-07) | no software work was needed |
| M5Unified has one board enum for both | no software work was needed |
| Factory-firmware source untouched since **2024-03-04** — 22 months before the v1.1 shipped | the evaluation firmware needed no attention |
| Vendor's own comparison table has **one row**: *Main Controller* | M5Stack says so itself |
| Price identical at USD 24.50 | no repositioning |

## M5Stack did this to more than one product

The shop also lists **"Air Quality Kit v1.1 with M5StampS3A (SEN55, SCD40)"** at USD 89.90 —
the same `vN.N with M5StampS3A` naming pattern applied to a different carrier.

So the DinMeter v1.1 is one instance of a **fleet-wide module transition**, not a decision about
the DinMeter specifically. That framing is useful: it predicts, correctly, that the changes would
be whatever the module forced and nothing more.

## The "A" in Stamp-S3A

Three independent signals say the "A" is a marketing label for **board revision v0.3.3 of the
same `S007` product**, not a new part:

1. SKU: `S007` → **`S007-V033`**
2. Schematic filename: `Sch_M5StampS3_v0.2.pdf` → **`Sch_StampS3_v0.3.3.pdf`** (no "A" in it)
3. Repository path: `Products/S007-V033_Stamp-S3A/`

And the schematics bear it out — 48 of 59 designators are common, the SoC, crystal, USB
receptacle, CC resistors, both FPC headers, the RGB LED, the button and the antenna designator
are all unchanged. See [`stamp-s3-to-s3a-delta.md`](stamp-s3-to-s3a-delta.md) §1–2.

## Naming traps specific to v1.1

| Trap | Detail |
|---|---|
| Doc URL | v1.0 is `/en/core/**M5DinMeter**`; v1.1 is `/en/core/**DinMeter_v1.1**`. `/en/core/DinMeter` is a **404** |
| Shop slug | v1.0 is `m5stack-din-meter-**w**-m5stamps3`; v1.1 is `m5stack-din-meter-v1-1-**with**-m5stamps3a` |
| Stamp-S3A schematic filename | `Sch_StampS3_v0.3.3.pdf` — searching for "S3A" will not find it |
| v1.1 schematic filename | `K134-V11_DIN_Meter_**v1.0**_2025_11_25_17_15_58.pdf` — it says v1.0 because it *is* v1.0 |
| Stamp docs path | `/en/core/Stamp-S3A`, **not** `/en/stamp/…` (that path 404s) |

## Community

**No community project, board file or fork anywhere distinguishes v1.1 from v1.0.** Searched
2026-09-04; see [`research-log.md`](research-log.md) §4. That is unsurprising given that the
firmware is compatible — and it is also why the RGB-LED change has gone unremarked.

→ [`../dinmeter/product-history-and-family.md`](../dinmeter/product-history-and-family.md)
