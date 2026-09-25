# Xteink X4 — images and media

**No X4 teardown, PCB photo or board image is held.**

## What was searched

| Target | Where | Result |
|---|---|---|
| X4 teardown | Reddit, 1,798 posts, terms `xteink teardown`, `xteink teardown chip` | **None.** The two teardowns found are both **X3** |
| X4 PCB photos | GitHub repo census (~200 repos) | None |
| Vendor imagery | Shopify product record | **Product delisted** — the device's own images are gone with it |
| FCC internal photos | not searched | No FCC ID known |

## The nearest available evidence

The [X3 teardowns](../x3/media.md) — one 13-image English-captioned album, one
10-image Chinese set **with a hand-drawn schematic** — are of the **same board
family**: ESP32-C3, Puya 128 Mbit flash, the same shared-SPI architecture, the
same construction style.

They are **not a substitute**. The X3 has a different panel (792×528, UC8253), an
RTC, a fuel gauge, an IMU and an NFC tag, none of which the X4 has. Use them for
construction style and for the C3/flash identification only.

## What is lost

Because the X4 was delisted before any image of it was captured here, this record
has **no photograph of the device at all** — not even a marketing render. Vendor
imagery was not archived while the listing was live.

**Lesson for this knowledge base:** capture vendor product imagery at the time of
first observation, because delisting removes it. The X4 Pro and X3 listings are
live *now* and their images are enumerable from
`vendors/xteink/artifacts/store-snapshots/2026-09-04/products-p1.json` (`products[].images[].src`).

## Recovery options

| Route | Status |
|---|---|
| Wayback Machine snapshot of the X4 product page | **Attempted and failed** — CDX timed out. Worth retrying with a longer timeout or `matchType=prefix` |
| Community photos in Reddit posts | Many exist as Reddit-hosted images; **not enumerated** this session |
| A new teardown | Nobody has posted one |

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 12:* | FCC internal photos | not searched | No FCC ID known |
>

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment authorisations**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

The original finding confused **"no mark visible in a product photograph"** with **"no grant exists"**. Those are different claims, and only the first was tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is ordinary for a device with a screen. **That is a likely explanation and it was not verified.**

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

Full record, with controls: [`certification-and-compliance.md`](certification-and-compliance.md).

Listed in [`research/passes/index-merge/corrections-requiring-review.md`](../../../research/passes/index-merge/corrections-requiring-review.md).
