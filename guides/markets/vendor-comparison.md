# Hardware sourcing — vendor and marketplace comparison

Where to buy embedded hardware, and — far more importantly for this repository — **what
documentation you can expect to still exist in three years.**

- **Compiled:** 2026-08-24. Reachability probes performed 2026-08-24 **[WEB]**.
- **Evidence labels:** **[WEB]** vendor web page · **[DOC]** vendor document · **[COM]** community ·
  **[INF]** inference · **[SRC]** source code.

## A note on prices

**This document contains no prices.** Not because prices don't matter, but because **we did not
verify any**, and a plausible-looking invented figure is worse than no figure. Every price
observation in a document like this must carry a currency, a date, a quantity, a shipping origin and
a URL, or it is noise.

Where a price would naturally appear, this document says **"not verified"**. If you add one, cite it
as: *"USD 24.99, 1 unit, retrieved YYYY-MM-DD, `<url>`, ships from X"*.

The **relative positioning** claims below (e.g. "Adafruit is more expensive than AliExpress") are
**[INF]** — widely understood, not measured here.

---

## 1. The comparison

Reachability column verified 2026-08-24 **[WEB]**; everything else is **[INF]** unless marked.

| Vendor | What they sell | Docs quality | Schematics | Ships from | Reachable |
|---|---|---|---|---|---|
| **[Waveshare](../../vendors/waveshare/README.md)** | Own designs, huge range | **Good** — per-product MediaWiki | Usually, as **PNG in a ZIP** | Shenzhen, CN | ✅ 200 (S1) |
| **Seeed Studio** | Own designs (XIAO, Grove), fab services | **Good** — wiki + Fusion PCB | Often, incl. **KiCad/EAGLE source** | Shenzhen, CN | ✅ 200 (S2) |
| **M5Stack** | Own ecosystem, stackable modules | **Good** — structured docs site | Usually PDF | Shenzhen, CN | ✅ 200 (S3) |
| **Adafruit** | Own designs + resale | **Excellent** — best-in-class tutorials | ✅ **Always**, usually **open-source EDA** | New York, US | ✅ 200 (S4) |
| **SparkFun** | Own designs + resale | **Excellent** — hookup guides | ✅ **Always**, open hardware | Colorado, US | ✅ 200 (S5) |
| **DFRobot** | Own designs, robotics-leaning | **Moderate** — wiki, uneven | Sometimes | Shanghai, CN | ✅ 200 (S6) |
| **LilyGO** | Own designs (T-Display etc.) | **Poor→moderate** — **GitHub is the documentation** | Often, in the GitHub repo | Shenzhen, CN | ✅ 200 (S7) |
| **[Espressif](../../vendors/espressif/README.md) official** | Reference devkits | **Excellent** — real datasheets, errata, PCNs | ✅ For many boards; **not all** | CN (via distributors) | ✅ 200 (S8) |
| **Guition** | Display modules / HMI boards | **Poor** — pan-hosted ZIPs | Rarely | Shenzhen, CN | ✅ 200 (S9) |
| **[HAOYU](../../vendors/haoyu/README.md)** | Small retailer + own `HY-` modules | **Poor** — product pages only | Rarely | Shenzhen, CN | ✅ 200 (S10) |
| **AliExpress / Taobao** | Marketplace — everything | **None** — the listing *is* the doc | ❌ | CN | ✅ 200 (S11) |
| **Amazon / eBay** | Marketplace — mostly resold CN stock | **None** | ❌ | Varies | not probed |
| **LCSC** | Component distributor | **Excellent for datasheets** — see §4 | n/a | Shenzhen, CN | ✅ 200 (S12) |
| **Mouser** | Component distributor | Excellent | n/a | US/global | ⚠️ **403 to scripted access** (S13) |
| **Digi-Key** | Component distributor | Excellent | n/a | US/global | ⚠️ **403 to scripted access** (S13) |

---

## 2. The tiers, and what actually distinguishes them

### Tier 1 — Open-hardware Western (Adafruit, SparkFun)

Design their own boards, publish **schematics, board files, and drivers under open licences**, and
write genuinely excellent tutorials. You are paying for documentation and support as much as for
silicon. **[INF]**

The durability argument is the strongest one: their documentation lives on their own maintained
sites *and* in public Git repositories, so **it survives the product's discontinuation.** For a
design you will still be maintaining in five years, this matters more than the unit price.

### Tier 2 — Documented Chinese (Waveshare, Seeed, M5Stack)

The sweet spot for most work: own designs, substantially cheaper than Tier 1, with **real
documentation infrastructure**. Waveshare's per-product wiki is the archetype and is thoroughly
characterised in [our vendor guide](../../vendors/waveshare/README.md).

The reservations are documented, not hypothetical:

- **Specs disagree between sources.** Storefront, wiki, schematic and demo code routinely name
  different ICs. Waveshare's guide establishes a trust order — **schematic > demo source > wiki >
  storefront** — and our knob board is the worked example, where the display controller is named
  inconsistently across the set (resolved in the
  [ST77916 record](../../components/sitronix/st77916/README.md)).
- **Wiki pages are edited in place with no version bump.** Pin an `oldid`. **[DOC]**
- **Schematics are PNG sheets in a ZIP, not PDF; Gerbers and BOM are rare.** **[DOC]**
- **Licensing is unstated.** Demo archives bundle LVGL (MIT), Espressif components (Apache-2.0) and
  unattributed vendor BSP code with no header at all. **Do not assume the archive is
  redistributable.** **[DOC]**

### Tier 3 — GitHub-as-documentation (LilyGO)

Interesting hardware, minimal official documentation, and a **GitHub repo that is the real manual.**
Workable if you read code; frustrating otherwise. The risk is that a repo can be
force-pushed, renamed or deleted, and there is no vendor-side archive. **[INF]**

### Tier 4 — Marketplace and near-anonymous (AliExpress, Taobao, Amazon, eBay, Guition, small retailers)

Cheapest, widest selection, **no documentation guarantee whatsoever.** The listing photo is
frequently the only technical information, and it is frequently of a different board than the one
shipped. This tier is where [clones-and-variants.md](clones-and-variants.md) applies in full.

**Guition deserves a specific note**, because we have concrete evidence about it. Guition's
`JC3636K518` is a sibling/clone of the Waveshare knob board, and Guition **publishes application
source that Waveshare does not** — but it is hosted on `pan.jczn1688.com`, a JavaScript file manager.
We **could not retrieve it**: the direct link returns HTML and the Cloudreve API paths 404 **[COM]**.
The corporate site `guition.com` is live (S9) and `pan.jczn1688.com` responds (S14), but
`http://www.jczn1688.com/` returned **HTTP 530** (S15) — an unhealthy origin.

That is the tier-4 pattern in miniature: **the valuable artefact exists, and you still cannot get
it.**

---

## 3. Documentation durability — the axis nobody advertises

For this repository, the question is not "can I buy it" but **"will the schematic still be there when
I need it".**

| Risk | Evidence |
|---|---|
| **No directory listing** | `files.waveshare.com` returns **200 with an empty body** for a directory request — it is not a listing. Filenames must be discovered from wikitext or guessed **[DOC]** |
| **Link rot** | Some Waveshare wiki links no longer resolve; probes are logged in [component-download-failures.txt](../../component-download-failures.txt) |
| **Soft 404s** | `documentation.espressif.com` serves a **13,745-byte app shell with HTTP 200** for slugs that do not exist. A `.pdf` URL can return an HTML error page with HTTP 200 **[DOC]** |
| **Broken official links** | Espressif's own ESP32-P4X-EYE user guide links a *"Reference Design (ZIP)"* that **does not resolve** — every variant returns the soft-404 shell. See [ESP32-P4-EYE §1](../../devices/espressif/esp32-p4-eye/README.md) **[DOC]** |
| **Regression in published detail** | The P4X-EYE **dropped** the schematic and PCB its EOL predecessor published, in favour of that broken ZIP **[DOC]** |
| **In-place edits** | Waveshare wiki pages change with no version bump or changelog **[DOC]** |
| **JS-only file hosts** | Guition's `pan.jczn1688.com` needs a browser session **[COM]** |

### The operative conclusion

**Mirror everything you depend on, at acquisition time, with a checksum.** That is why this
repository stores artefacts with URL, retrieval date, byte size and SHA-256, and validates magic
bytes before committing — see [vendors/README.md](../../vendors/README.md) and the
[artifact manifest](../../artifact-manifest.md).

For scarce sources, also submit to `https://web.archive.org/save/<url>` per the repository's
[retrieval policy](../../AGENTS.md).

**Even a first-party vendor link is not durable.** Espressif — the best-documented vendor here —
supplies the counter-example above.

---

## 4. Distributors as a documentation channel

A finding worth stating plainly, because it inverts the obvious habit: **for Chinese components, the
distributor is often a better documentation source than the manufacturer.**

- **LCSC** mirrors datasheets at
  `https://datasheet.lcsc.com/lcsc/<id>_<Manufacturer>-<Part>_C<NNNNN>.pdf` — with the manufacturer,
  part number and stable LCSC `C`-code in the filename. This is how we obtained the
  [MEMSensing microphone datasheet](../../components/memsensing/msm261d4030h1cpm/README.md) **[DOC]**.
  LCSC's **price ladder and stock are in embedded JSON**, not the rendered HTML — grep for
  `"productPriceList"`, `"stockNumber"` **[DOC]**.
- **Mouser and Digi-Key host excellent datasheets but block scripted access** — 403 to every UA tried,
  including UA rotation (S13). Mouser publishes a **Search API**; that is the intended path **[DOC]**.
- **General pattern:** *Chinese/Asian distributors are open; US/EU distributors and aggregators are
  uniformly closed.* Rotating User-Agents did not help on any of them **[DOC]**.
- ⚠️ **Beware AI-generated parts content on distributor-adjacent sites.** One mirror's prose
  misstated a chip's operating temperature by 20 °C against the manufacturer datasheet. **Use the
  tables, discard the paragraphs** **[DOC]**.

All of the above is recorded in the repository's
[crawler / site-access table](../../ai-crawler-site-access-table.md#electronics-distributors--parts-catalogues).

---

## 5. Choosing a source

| If you want… | Go to |
|---|---|
| To learn, with support | **Adafruit / SparkFun** |
| Open EDA source you can modify | **Adafruit / SparkFun / Seeed** |
| Best capability per unit cost with usable docs | **Waveshare / Seeed / M5Stack** |
| The authoritative reference implementation | **Espressif official devkits** |
| A specific exotic display or sensor module | **Waveshare / AliExpress** — and budget reverse-engineering time |
| Components in small quantity, with datasheets | **LCSC** |
| Components with Western support and stock guarantees | **Mouser / Digi-Key** (via API for scripted access) |
| The absolute cheapest unit | **AliExpress / Taobao** — assume no documentation and see [clones-and-variants.md](clones-and-variants.md) |

**A default worth stating:** buy the **module**, not the bare chip, unless you are prepared to
certify your own radio — see
[ecosystem-and-product-lines.md §8](../espressif/ecosystem-and-product-lines.md#8-bare-chip-vs-module-vs-devkit).

---

## 6. Sources

| ID | Target | Class | URL | Retrieved | Result |
|---|---|---|---|---|---|
| S1 | Waveshare | probe | https://www.waveshare.com/ | 2026-08-24 | 200 |
| S2 | Seeed Studio | probe | https://www.seeedstudio.com/ | 2026-08-24 | 200 |
| S3 | M5Stack | probe | https://m5stack.com/ · https://docs.m5stack.com/en/products | 2026-08-24 | 200 both |
| S4 | Adafruit | probe | https://www.adafruit.com/ | 2026-08-24 | 200 |
| S5 | SparkFun | probe | https://www.sparkfun.com/ | 2026-08-24 | 200 |
| S6 | DFRobot | probe | https://www.dfrobot.com/ | 2026-08-24 | 200 |
| S7 | LilyGO (Xinyuan-LilyGO on GitHub) | probe | https://github.com/Xinyuan-LilyGO | 2026-08-24 | 200 |
| S8 | Espressif devkits | probe | https://www.espressif.com/en/products/devkits | 2026-08-24 | 200 |
| S9 | Guition | probe | https://www.guition.com/ | 2026-08-24 | 200 — title *"Display Module Manufacturers Suppliers Factory - GUITION"* |
| S10 | HAOYU | probe | https://www.hotmcu.com/ | 2026-08-24 | 200 |
| S11 | AliExpress | probe | https://www.aliexpress.com/ | 2026-08-24 | 200 |
| S12 | LCSC | probe | https://www.lcsc.com/ | 2026-08-24 | 200 |
| S13 | Mouser, Digi-Key | secondary (internal) | [crawler table](../../ai-crawler-site-access-table.md#electronics-distributors--parts-catalogues) | 2026-08-21 | **403 to all UAs tried**; our own 2026-08-24 probe of digikey.com also returned 403 |
| S14 | Guition file host | probe | https://pan.jczn1688.com/ | 2026-08-24 | 200 (JS file manager) |
| S15 | Guition corporate alt | probe | http://www.jczn1688.com/ | 2026-08-24 | **HTTP 530** |
| S16 | Waveshare sourcing guide | secondary (internal) | [vendors/waveshare](../../vendors/waveshare/README.md) | 2026-08-21 | Trust order, artefact set, gotchas |
| S17 | Community catalogue — Guition/nkinnan | secondary (internal) | [examples/catalog.md](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/catalog.md) | 2026-08-23 | Guition source hosting and retrieval failure |

> **Evidence boundary.** S1–S12, S14, S15 are **HTTP reachability probes performed 2026-08-24** —
> they establish only that a host responds, **not** the quality of its catalogue or documentation.
> **Every qualitative judgement in §1 and §2 (documentation quality, schematic availability,
> licensing posture, shipping origin, support channels) is [INF]** — it was *not* verified by reading
> each vendor's catalogue in this pass, and is drawn from general familiarity plus, for Waveshare and
> Espressif, this repository's own researched records. **No prices, shipping costs or delivery times
> were verified; none are stated.** The durability findings in §3 and the distributor findings in §4
> are the best-evidenced material here, being **[DOC]** from prior passes.

---

## 7. Related

- [Clones and variants](clones-and-variants.md) — the companion document
- [Espressif ecosystem map](../espressif/ecosystem-and-product-lines.md)
- [Vendor sourcing guides](../../vendors/README.md) — per-manufacturer document retrieval
- [Crawler / site-access table](../../ai-crawler-site-access-table.md)
- [Component download failures](../../component-download-failures.txt) — the log of what did not resolve
