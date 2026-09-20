# Chipsemi (基合半导体) — Documentation Sourcing Guide

> **Status: no record yet, but we hold the CHSC5816 datasheet (§8).** Chipsemi has no component
> record here. It appears as a comparison in the [CST816D record](../../components/hynitron/cst816d/README.md),
> which lists the Chipsemi `CHSC5816` touch controller as supported by `SensorLib` but using a
> **different register map** — i.e. not a drop-in substitute for our part.

> **TL;DR** — `https://www.chipsemicorp.com/` is live and **Chinese-first** (title
> 基合半导体（宁波）有限公司 – Chipsemicorp; HTTP 200; a WordPress site, verified 2026-08-24, S1).
> A guessed `/products/` path **404s** (S2). Note the domain is **`chipsemicorp.com`** —
> `http://www.chipsemi.com/` **does not resolve** (S3).

---

## 1. Who they are

Chipsemi (Ningbo) Co., Ltd. — 基合半导体（宁波）有限公司 — is a Chinese fabless designer of capacitive
touch controllers and related human-interface ICs. They are a smaller, later entrant than
[Hynitron](../hynitron/README.md) or [Goodix](../goodix/README.md), operating in the same
low-cost small-panel touch market.

Chipsemi is a *component* vendor.

---

## 2. Product lines

| Prefix | What it is |
|---|---|
| **`CHSC`** | Capacitive touch controllers — `CHSC5816`, `CHSC6413`, `CHSC5448` |
| Touch keys / sliders | Simpler capacitive sensing |

**[unverified]** — this table is assembled from part numbers seen in community driver code, **not
from a Chipsemi catalogue**. The site was not enumerated.

**How they fit:** `CHSC5816` turns up on small round and square touch panels of exactly the class
used by our knob board — which is precisely why it is a plausible substitution on a clone. See §7.

---

## 3. Market position

**A third-tier alternative in an already low-margin market.** Chipsemi competes for the same design
wins as Hynitron `CST816x`, Goodix `GT9xx`, FocalTech `FT6x36` and Sitronix `ST16xx`. Selection is
driven by unit price and by whichever vendor the panel module house has a relationship with — which
is why the touch IC is one of the **most volatile** parts of a cheap display module's BOM.

Documentation posture is the familiar one for this tier: **module-house-first, NDA-gated register
manuals, thin or absent public datasheets.** Community drivers are the practical source.

---

## 4. Part numbering

```
CHSC 5816
│    └─ Series index
└────── CHSC = Chipsemi Capacitive Sensing Controller (inferred expansion)
```

**[inference]** — no numbering key located, and the expansion of the prefix is a guess.

---

## 5. Documentation

| Rank | Source | Notes |
|---|---|---|
| 1 | **`lewisxhe/SensorLib`** — <https://github.com/lewisxhe/SensorLib> | Supports `CHSC5816` alongside `CST816` and `GT911`. **The most useful public description of the register interface we know of** |
| 2 | Other community drivers | ESP-IDF / LVGL / Arduino ports |
| 3 | Panel module house | Whoever bonded the die |
| 4 | Chipsemi direct — `https://www.chipsemicorp.com/` (S1) | ✅ responds; contents not enumerated; **no public datasheet located** |

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ❌ None |
| LCSC | ⚠️ Possibly, as COG/COF die — not a normal purchase |
| **Panel module houses** | ✅ The real channel, pre-bonded |

As with [Hynitron](../hynitron/README.md#6-distribution) and [Sitronix](../sitronix/README.md), you do
not buy this part — you inherit it with a panel.

---

## 7. Gotchas

- **The domain is `chipsemicorp.com`.** `chipsemi.com` does not resolve (S3).
- **Chinese-first site**, and no public register manual located.
- **`CHSC5816` is not register-compatible with `CST816x`.** Confirmed by the
  [CST816D comparison table](../../components/hynitron/cst816d/README.md), which marks it ❌
  "Different map". If a clone board substituted this controller, the stock driver will find nothing.
- **This is a *likely* clone substitution.** Touch controllers are the highest-churn item in a cheap
  panel BOM. When a clone board's touch does not work, **enumerate the I²C bus and read chip IDs
  before assuming the panel is faulty** — see
  [clones-and-variants.md](../../guides/markets/clones-and-variants.md).
- **Do not confuse Chipsemi with "ChipSemi"/"Chipsea" (芯海科技)**, a different Chinese company making
  ADCs and MCUs. The names collide in search results.

---

## 8. Parts and devices we document

**No README record yet — but we do hold the CHSC5816 datasheet.**

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **CHSC5816** (capacitive touch controller) | [`components/chipsemi/chsc5816/artifacts/chsc5816-datasheet-v1-20221114-zh.pdf`](../../components/chipsemi/chsc5816/artifacts/chsc5816-datasheet-v1-20221114-zh.pdf) | 950,989 | ❌ **missing** |

Note the `-zh` suffix: **the document is in Chinese**, consistent with §7. It is V1, dated
2022-11-14.

This substantially changes §5: **we have a vendor datasheet locally**, so `SensorLib` is no longer
the best available description of the register interface — the datasheet is.

**Provenance:** it shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive.
**The CHSC5816 is not fitted on the knob board.** See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

Writing the `components/chipsemi/chsc5816/README.md` record is **outstanding work**.
---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Chipsemi corporate site | primary | https://www.chipsemicorp.com/ | 2026-08-24 | HTTP 200; title `基合半导体（宁波）有限公司 – Chipsemicorp`; a WordPress-based site (from its `robots` meta and asset paths) |
| S2 | **Negative probe** | probe | https://www.chipsemicorp.com/products/ | 2026-08-24 | **HTTP 404** |
| S3 | **Negative probe** — alternate domain | probe | http://www.chipsemi.com/ | 2026-08-24 | **Does not resolve** (connection failure, no HTTP status) |
| S4 | CST816D record, controller comparison table | secondary (internal) | [`components/hynitron/cst816d/README.md`](../../components/hynitron/cst816d/README.md) | 2026-08-21 | `CHSC5816` is SensorLib-supported but has a different register map |
| S5 | `lewisxhe/SensorLib` | secondary | https://github.com/lewisxhe/SensorLib | 2026-08-21 | The driver that supports the part |

> **Evidence boundary.** S1–S3 are **HTTP probes performed 2026-08-24** establishing only that the
> site exists, its language, and two negative results. **The site was not enumerated and no Chipsemi
> document has been retrieved or read** — so §2's product table and §3's market characterisation are
> **unverified inference** from community driver code and from the shape of the market, not from the
> vendor. The only claim here resting on retrieved evidence is the register-map incompatibility
> (S4/S5).

---

## Related

- [Vendor guide index](../README.md)
- [Hynitron](../hynitron/README.md) — the incumbent on our board · [Goodix](../goodix/README.md) · [Sitronix](../sitronix/README.md)
- [CST816D component record](../../components/hynitron/cst816d/README.md)
- [Clones and variants](../../guides/markets/clones-and-variants.md)
