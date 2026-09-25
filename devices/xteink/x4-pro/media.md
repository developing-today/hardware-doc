# Xteink X4 Pro — images and media

**No image of this device — external, internal or PCB — is held in this
repository.** This page records what was sought and what exists, so the search is
not repeated blindly.

## What was searched

| Target | Where | Result |
|---|---|---|
| Teardown / PCB photography | Reddit `xteink teardown`, `xteink teardown chip` across 1,798 posts | **None for the X4 Pro.** Two X3 teardowns exist |
| Vendor product imagery | `xteink.com` Shopify product record | Images exist in `products.json` but were **not downloaded** — see below |
| FCC internal photos | not searched — **no FCC ID is known** | — |
| YouTube teardowns | only via Reddit-surfaced links | none found for the Pro |

## Why no vendor images were retained

The Shopify product record carries image URLs on the Shopify CDN. They were not
downloaded because:

1. They are **marketing renders and lifestyle shots**, not identification or
   mechanical references — they show a black slab.
2. Their **rights status is clearly the vendor's** and redistribution here would
   be unexamined.
3. They establish **nothing not already in the text record**.

If wanted later, they are in `vendors/xteink/artifacts/store-snapshots/2026-09-04/products-p1.json` under
`products[].images[].src`, retrieved 2026-09-04.

## What exists elsewhere in this tree

The [X3 record](../x3/media.md) holds **two independent teardowns**, both
archived with placeholders:

- a 13-image English-captioned Imgur album
- a 10-image Chinese set **including a hand-drawn schematic**

The X3 is a **different board** (ESP32-C3, different panel, different peripherals)
so those images are **not** a substitute for X4 Pro photography. They do
establish the vendor's general construction style: glued battery, glued pogo
magnets, glass back.

## The gap, stated plainly

Seven separate unknowns in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) —
battery capacity, mass, dimensions, charger IC, panel module part, antenna, debug
pads — **would all be closed by one X4 Pro teardown.** Producing or finding one is
the single highest-value next action for this device.

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 13:* | FCC internal photos | not searched — **no FCC ID is known** | — |
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
