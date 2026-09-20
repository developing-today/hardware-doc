# Alps Alpine — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation for **any** Alps Alpine electromechanical component.
This is the one vendor in this repository whose documentation problem is *not* language or secrecy —
it is that the parts are **catalogue items**, not datasheet items.

> **TL;DR** — Alps Alpine's technical site uses a clean, guessable pattern:
> `https://tech.alpsalpine.com/e/products/detail/<PART-NUMBER>/` (S2). But the **downloadable document
> is usually a multi-part product *catalogue* PDF, not a per-part datasheet** — e.g.
> `https://tech.alpsalpine.com/cms.media/product_catalog_sw_01_sscm_en_90b44d6d7f.pdf` (S3), whose
> filename contains an unguessable content hash.

---

## 1. Who they are

Alps Alpine Co., Ltd. (アルプスアルパイン, Tokyo; TSE: 6770) is the 2019 merger of Alps Electric and
Alpine Electronics. Alps Electric was — and the merged company remains — the world's leading maker of
**electromechanical components**: switches, encoders, potentiometers, connectors, sensors and
haptic actuators. Alpine brought automotive infotainment.

If you have used a laptop trackpad, a car's rotary volume control, or a game-controller thumbstick,
you have very likely touched an Alps part. They are the quality benchmark in this category.

Alps Alpine is a *component* vendor; it appears only in
[`components/`](../../components/README.md).

---

## 2. Product lines

| Line | What it is | Relevance |
|---|---|---|
| **Switches** | Tactile, detector, slide, push, DIP, automotive | [SSCM110100](../../components/alps-alpine/sscm110100/README.md) is a slide/directional switch |
| **Encoders** | Incremental rotary encoders, with and without push | Directly relevant to smart-knob designs |
| **Potentiometers** | Rotary and slide, including motorised | |
| **Sensors** | Magnetic, current, pressure, humidity | |
| **Haptic actuators** | HAPTIC™ Reactor — a force-feedback actuator line | Compare our [LRA motor record](../../components/generic/lra-motor/README.md) |
| **Connectors** | Board-to-board, FPC, automotive | |
| **Communication modules** | Bluetooth/Wi-Fi modules | Minor |

**How they fit together for a knob-style device:** Alps supplies the *human-interface* half of the
BOM — the thing the user physically touches — while the silicon vendors supply everything behind it.
On our board that division is visible: an Alps switch and an encoder mechanism on the front end, a
[TI haptic driver](../../components/texas-instruments/drv2605l/README.md) and an
[Espressif SoC](../espressif/README.md) behind it.

---

## 3. Market position

**Premium.** Alps parts cost several times a generic Chinese equivalent and are specified when
tactile feel, actuation-force consistency and cycle life matter. A 300,000-cycle rating with a
specified force curve is what you are paying for.

The interesting signal for BOM reading: **an Alps part on a cost-optimised board means the designer
cared about feel.** On a smart-knob product that is exactly the right place to spend money, and it is
consistent with the design intent documented for our board.

Beware, though: **Alps is heavily counterfeited and heavily "equivalent-ed"** in the Chinese supply
chain. See §7.

---

## 4. Part numbering

Alps part numbers are systematic but **not human-decodable without the catalogue**. Example:

```
SSCM 110100
│    └─ Variant / configuration index within the series
└────── Series code (SSCM = a specific slide-switch series)
```

The rules that actually help:

- **The leading alphabetic block is the series**, and the series is what the catalogue is organised
  by. Find the series, get the catalogue, then find your variant in its table.
- **The numeric block is a position in that catalogue table** — actuator style, terminal style,
  detent count, packaging. It is not independently meaningful.
- **Do not try to infer specifications from the number.** Unlike [TI](../texas-instruments/README.md)
  or [Winbond](../winbond/README.md), there is no encoded voltage/package/temperature grammar to
  decode. **[inference]** — Alps publishes numbering keys *inside* each catalogue rather than as a
  general scheme.

---

## 5. Documentation: URL patterns

| Document class | Pattern | Verified |
|---|---|---|
| Technical site (EN) | `https://tech.alpsalpine.com/e/` | ✅ 2026-08-24 (S1) |
| Products index | `https://www.alpsalpine.com/e/products/` | ✅ 2026-08-24 (S4) |
| **Part detail page** | `https://tech.alpsalpine.com/e/products/detail/<PART>/` | ✅ (S2) — guessable, uppercase part number |
| Product catalogue PDF | `https://tech.alpsalpine.com/cms.media/<slug>_<hash>.pdf` | ✅ (S3) — **hash is unguessable; scrape it** |
| 2D/3D CAD | Linked from the detail page | Often requires no login, sometimes does |

### The reliable procedure

1. Construct the detail-page URL from the part number — this step *is* guessable.
2. Scrape the `cms.media` PDF link out of that page. The trailing hex block is a CMS content hash and
   **changes when the catalogue is re-published**, so a cached URL will eventually rot.
3. Note that the PDF is a **catalogue covering a whole series**. Record the page number of your part,
   not just the file, or the citation is useless to the next reader.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ✅ Excellent — Alps is a fully catalogued Western-distribution vendor |
| RS / Farnell | ✅ Good |
| LCSC | ⚠️ Some parts; more commonly you find *equivalents* sold under Alps-like numbers |
| AliExpress | ⚠️ **Counterfeit and "compatible" parts are the norm here**, not the exception |

---

## 7. Gotchas

- **Catalogues, not datasheets.** The single defining difference from a semiconductor vendor. Cite the
  catalogue *and the page*.
- **`cms.media` URLs contain a content hash** and rot on republication. Re-derive from the detail page.
- **Counterfeits and "equivalents".** Parts marked as Alps in the low-cost supply chain frequently are
  not, and the difference shows up as actuation force and cycle life — i.e. it *feels* wrong rather
  than failing outright. This is the hardest class of substitution to detect from a photograph, and
  is discussed in [clones-and-variants.md](../../guides/markets/clones-and-variants.md).
- **Board schematics often name the mechanism generically.** "Slide switch", "encoder" — resolving
  that to an actual Alps part number usually requires the physical part or a real BOM, neither of
  which vendors like Waveshare publish. Our
  [SSCM110100 record](../../components/alps-alpine/sscm110100/README.md) should be read with that
  identification caveat in mind.
- **Japanese and English sites differ.** `tech.alpsalpine.com/j/` is the Japanese tree and is
  sometimes more current.
- **Merged-company legacy.** Older documents are branded "Alps Electric" and may live on legacy
  hosts. A dead `alps.com` link usually has a `alpsalpine.com` successor.

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [SSCM110100](../../components/alps-alpine/sscm110100/README.md) | Directional / slide switch | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |

Adjacent human-interface records not attributed to Alps:
[power button](../../components/generic/power-button/README.md) ·
[ESP32-S3 BOOT button](../../components/generic/esp32-s3-boot-button/README.md) ·
[LRA vibration motor](../../components/generic/lra-motor/README.md).

No device in this repository is manufactured by Alps Alpine.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Alps Alpine English site | primary | https://www.alpsalpine.com/e/ | 2026-08-24 | HTTP 200 |
| S2 | SSCM110100 detail page | primary | https://tech.alpsalpine.com/e/products/detail/SSCM110100/ | 2026-08-21 | The `detail/<PART>/` pattern. Cited by the [SSCM110100 record](../../components/alps-alpine/sscm110100/README.md) |
| S3 | SSCM series product catalogue (EN) | primary | https://tech.alpsalpine.com/cms.media/product_catalog_sw_01_sscm_en_90b44d6d7f.pdf | 2026-08-21 | The `cms.media` hashed-filename pattern; the catalogue-not-datasheet model |
| S4 | Products index | primary | https://www.alpsalpine.com/e/products/ | 2026-08-24 | HTTP 200 |

> **Evidence boundary.** S1 and S4 are **reachability probes performed 2026-08-24**. S2 and S3 were
> retrieved 2026-08-21 during the component pass. §4 (numbering) is marked **[inference]** — we have
> not located a general Alps numbering key. §3's counterfeit claims are **general industry
> observation, not measured** in this repository, and are flagged accordingly rather than sourced.

---

## Related

- [Vendor guide index](../README.md)
- [SSCM110100](../../components/alps-alpine/sscm110100/README.md)
- [Texas Instruments](../texas-instruments/README.md) — the haptic driver behind the front panel
- [Clones and variants](../../guides/markets/clones-and-variants.md)
