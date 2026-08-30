# Goodix — Documentation Sourcing Guide

> **Status: no record yet, but we hold the GT911 datasheet (§8).** Goodix has no component record
> here. It appears as a comparison in the [CST816D record](../../components/hynitron/cst816d/README.md),
> which tabulates the Goodix `GT911` as **not** register-compatible with our touch controller
> (different register map, I²C address `0x5D`/`0x14`, 5-point multi-touch).
>
> That is exactly why the guide is worth having: if a clone of our knob board substitutes the touch
> IC, `GT911` is the single most likely substitute, and nothing will work until you know that.

> **TL;DR** — Goodix runs a real document portal at `https://www.goodix.com/en/document/center`
> (verified 2026-08-24: HTTP 200, 115,480 bytes of real HTML, S2). Note the path is
> `/en/document/center` — **singular `document`**. `/en/product` (singular) **404s**; the working
> product path is `/en/product/<category>`, e.g. `/en/product/touch` (S3, S4).

---

## 1. Who they are

Shenzhen Goodix Technology Co., Ltd. (汇顶科技; SSE 603160) is a Chinese fabless designer of
human-interface and biometric ICs. They became globally significant by winning under-display optical
fingerprint sensing in Android flagships, and they are one of the few Chinese fabless companies
operating at genuine scale in the West.

Goodix is a *component* vendor.

---

## 2. Product lines

| Line | What it is | Relevance here |
|---|---|---|
| **`GT` — touch controllers** | Capacitive touch, single- through multi-point | **`GT911`, `GT9xx` — the direct competitor to [Hynitron `CST816x`](../hynitron/README.md)** |
| **Fingerprint** | Optical under-display, capacitive | Their flagship business |
| **Audio** | Smart PA, codecs | |
| **Bluetooth / NFC** | Connectivity SoCs | |
| **Health sensors** | PPG, heart rate | |
| **Automotive HMI** | Touch and sensing for cars | Growing |

**How they fit together:** Goodix's organising idea is *"the interface between a human and a
device"* — touch, fingerprint, voice, biometrics. That is a coherent portfolio, and it means a
Goodix part will usually be found at the point where a user's finger meets the product.

---

## 3. Market position

Large, credible, and better-documented than most Chinese fabless peers — but **still a
module-house-first vendor** for touch controllers, with the same consequence described in the
[Hynitron](../hynitron/README.md#3-market-position) and [Sitronix](../sitronix/README.md) guides:
full register manuals go to volume customers under NDA, while the public tier is thinner.

Goodix is nevertheless a notable step up: they operate an actual document centre (S2) and a developer
kit portal (`/en/kit`), which Hynitron does not.

The `GT911` in particular is **extremely well supported by community drivers** (Linux `goodix_ts`
in-tree, ESP-IDF components, LVGL ports), so the practical documentation situation for that specific
part is much better than the vendor's own publishing would suggest.

---

## 4. Part numbering

```
GT 911
│  └─ Series index; roughly, capability and generation
└──── GT = Goodix Touch
```

**[inference]** — no public Goodix numbering key located. Observed conventions:

- **`GT9xx`** is the mainstream capacitive touch family (`GT911`, `GT928`, `GT9147`).
- **Higher numbers are generally newer or larger-panel**, but the mapping is not monotonic.
- **Register maps differ across the family**, so `GT911` driver code is not automatically a `GT928`
  driver. Confirm against the specific part.

---

## 5. Documentation: URL patterns

| Document class | Pattern | Status |
|---|---|---|
| Document centre | `https://www.goodix.com/en/document/center` | ✅ verified 2026-08-24 (S2) |
| Product category | `https://www.goodix.com/en/product/<category>` — e.g. `touch` | ✅ verified (S4) |
| Product index (singular, no category) | `https://www.goodix.com/en/product` | ❌ **HTTP 404** (S3) |
| Developer kits | `https://www.goodix.com/en/kit` | **[unverified]** — observed as a link on the homepage, not probed |
| Chinese site | `https://www.goodix.com/zh/...` | **[unverified]** |

### Where `GT911` documentation actually comes from

In descending order of practical usefulness — and note that **for this part the community sources
outrank the vendor**:

1. **Linux kernel driver** — `drivers/input/touchscreen/goodix.c`. In-tree, maintained, documents the
   register layout by construction.
2. **ESP-IDF / LVGL community components** — e.g. `esp_lcd_touch_gt911`.
3. **Widely-circulated `GT911 Programming Guide` PDFs.** These exist in many copies with unclear
   provenance. **Treat as secondary**: they are almost certainly genuine Goodix documents that leaked
   out of an NDA channel, which means they are accurate but unpinnable and possibly outdated.
4. **Goodix document centre** (S2) — check first out of principle; expect briefs and selection
   guides rather than register manuals.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ❌ Essentially none |
| LCSC | ⚠️ Some `GT911`; more often you buy it bonded to a panel |
| **Panel module houses** | ✅ The real channel |
| AliExpress / Taobao | ✅ As touch panel modules and as loose `GT911` for repair |

---

## 7. Gotchas

- **`/en/product` 404s; `/en/product/<category>` works.** A trailing-category path is required (S3/S4).
- **`GT911` has two I²C addresses — `0x5D` and `0x14`** — selected by the state of the `INT` pin
  during reset. This is a real trap: the same physical part enumerates at different addresses
  depending on your reset timing, and a scan that finds "nothing" may simply have reset it into the
  other address. Documented in the
  [CST816D comparison table](../../components/hynitron/cst816d/README.md).
- **Not compatible with `CST816x`.** Different register map, different point count. A clone board
  that substituted the touch IC needs a different driver, not a tweak.
- **Register manuals circulate outside official channels.** Accurate but unpinnable — see §5.
- **Configuration is written to the controller, not just read.** `GT9xx` parts take a large
  configuration blob (panel geometry, sensitivity, channel mapping) that is panel-specific. **The
  config from another board will not work on yours.** This is the biggest practical difference from
  the simpler `CST816x` parts.

---

## 8. Parts and devices we document

**No README record yet — but we do hold the GT911 datasheet.**

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **GT911** (5-point capacitive touch controller) | [`components/goodix/gt911/artifacts/gt911-datasheet-rev-1.0.pdf`](../../components/goodix/gt911/artifacts/gt911-datasheet-rev-1.0.pdf) | 1,467,494 | ❌ **missing** |

This materially improves on §5: **we have Rev. 1.0 of the datasheet locally**, so the ranked
source list above is the procedure for obtaining *another* Goodix part, not for this one.

**Provenance:** the PDF shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive.
**The GT911 is not fitted on the knob board** — our touch controller is the
[Hynitron CST816D](../../components/hynitron/cst816d/README.md). See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

Writing the `components/goodix/gt911/README.md` record is **outstanding work** — and it would let
§7's dual-address and configuration-blob claims be upgraded from recollection to **[DOC]**.
---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Goodix corporate site | primary | https://www.goodix.com/ | 2026-08-24 | HTTP 200; English site at `/en/`; navigation structure |
| S2 | Goodix document centre | primary | https://www.goodix.com/en/document/center | 2026-08-24 | **HTTP 200, 115,480 bytes of real HTML** — a genuine portal, not a shell |
| S3 | **Negative probe** | probe | https://www.goodix.com/en/product | 2026-08-24 | **HTTP 404** — the bare product path does not exist |
| S4 | Touch product category | primary | https://www.goodix.com/en/product/touch | 2026-08-24 | HTTP 200 — the `<category>` segment is required |
| S5 | CST816D record, controller comparison table | secondary (internal) | [`components/hynitron/cst816d/README.md`](../../components/hynitron/cst816d/README.md) | 2026-08-21 | `GT911` address `0x5D`/`0x14`, 5-point, incompatible register map |

> **Evidence boundary.** S1–S4 are **HTTP probes performed 2026-08-24** establishing which paths
> resolve — the portal's *contents* were **not enumerated**, so the claim that register manuals are
> absent from it is **not verified**. §2, §3, §4 and §7 are **general knowledge and inference**, not
> read from a Goodix document; in particular the `GT911` dual-address and configuration-blob claims
> in §7 are **recalled from community driver behaviour, not confirmed against a vendor datasheet**.
> No Goodix document is stored in this repository.

---

## Related

- [Vendor guide index](../README.md)
- [Hynitron](../hynitron/README.md) — the incumbent on our board · [Sitronix](../sitronix/README.md)
- [CST816D component record](../../components/hynitron/cst816d/README.md)
- [Clones and variants](../../guides/markets/clones-and-variants.md) — substituted touch controllers
