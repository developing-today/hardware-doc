# Xteink (Shenzhen Xiaohu Xingtong Technology Co., Ltd. · 深圳市小虎星瞳科技有限公司)

*Written 2026-09-11 by the round-two index merge, from the sourcing findings of the Xteink
round-two and certification/market passes. Everything below was **observed**, not recalled;
every claim carries the date it was observed on.*

Shenzhen maker of low-cost pocket e-ink readers — the [Xteink family](../../devices/README.md#xteink-阅星瞳--星瞳-star-pupil),
and the hardware target of the CrossPoint Reader / FreeInk firmware ecosystem.

> **Why this guide exists.** Xteink publishes **no datasheet, no schematic, no wiki and no
> support portal**. There is a Shopify storefront and nothing else. That sounds like a dead end
> and is not: the storefront's JSON endpoints and the company's **FCC grantee record** between
> them yield launch dates, SKUs, stock, prices, the legal entity, and the complete list of
> products — *including ones the vendor has never announced*. This guide is about those two
> routes.

---

## 1. Identity

| Field | Value | Evidence |
|---|---|---|
| Legal name | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.** | FCC grantee record, 2026-09-11 |
| Brand names | Xteink · 阅星瞳 · 星瞳 ("Star Pupil") | vendor site, community |
| **FCC grantee code** | **`2BTR9`**, registered **2025-12-21** | <https://fccid.io/2BTR9> |
| FCC contact | Chen Chu, `chuchen@xteink.cn` | FCC grantee record |
| Address | Room 1209, Yichuang International Center, Building 2B, No. 8 Golf Avenue, Guangpei Community, Guanlan Street, Longhua District, Shenzhen | FCC grantee record |
| Storefront | `xteink.com` — **stock Shopify** | measured 2026-09-11 |
| Chinese domain | `xteink.cn` — **confirmed theirs by the FCC filing**, but the apex was unreachable from the research host. `bofi.xteink.cn` is referenced inside X4 firmware | 2026-09-11 |

---

## 2. The storefront is Shopify, and its JSON is far better evidence than its prose

`xteink.com` is an unmodified Shopify install. Every standard endpoint works **unauthenticated**:

```bash
curl -s 'https://xteink.com/products.json?limit=250&page=1'      # whole catalogue
curl -s 'https://xteink.com/collections.json'                    # collection handles
curl -s 'https://xteink.com/collections/<handle>/products.json'  # one product line
curl -s 'https://xteink.com/products/<handle>.js'                # one product, richer
```

These carry **`published_at`, per-variant SKU, price, `compare_at_price`, stock state and
grams** — which is how launch dates and withdrawals in this repository are dated at all.

**Paginate to exhaustion.** `?limit=250&page=1` returned the entire catalogue on 2026-09-11
(25 products), but confirm pages 2+ are empty rather than assuming.

### Traps, all measured

- ⚠ **`body_html` can be empty.** The X4 Classic's entire specification table exists **only in
  the rendered product-page HTML**, not in the JSON. **Fetch both**, always.
- ⚠ **The product prose is SEO-generated and demonstrably wrong.** Where the prose and the JSON
  disagree, the JSON is evidence and the prose is marketing. Where the prose and the *hardware*
  disagree, both lose.
- ⚠ **`compare_at_price` is not a former selling price.** It is a Shopify "was" anchor. The X4
  Classic was published at 79.00 and has never been listed at the 89.00 it is compared against.
- ⚠ **`grams` is shipping weight, not device mass.** The X4 Classic reports `250`; the vendor's
  own spec block says the device is **68 g**.
- ⚠ **Six catalogue line-items are services, not products** — handling fees, shipping fee,
  after-sale charges. Exclude them from any price range, or "cheapest item in the store" returns
  **USD 1.00**.
- **An empty collection is a pre-launch signal.** A `x4-classic` collection handle existed with
  zero devices in it days before the device was listed. A collection whose *device* is gone but
  whose accessories remain is the opposite — an end-of-life signature.
- Reviews are **Judge.me**, embedded as JSON inside the product page rather than fetched
  separately.

---

## 3. ⭐ The FCC grantee code is the real product catalogue

**This is the most valuable finding about this vendor, and it generalises to every vendor in
this repository.**

```
https://fccid.io/2BTR9          # every device Xteink has ever certified for the US
https://fccid.io/<FCC-ID>       # one filing: dates, frequencies, exhibit list, embargoes
https://fccid.io/<FCC-ID>/<Type-Slug>/<Doc-Slug>.pdf    # an exhibit
```

Searching for *"Xteink"* by **product name** finds little. Enumerating the **grantee code**
returned five devices on 2026-09-11 — **one of which the vendor has never announced, listed or
priced**: the [X4 Light](../../devices/xteink/x4-light/README.md), `2BTR9-X4L`, granted
2026-08-13.

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light — **never announced** |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

**Grant dates lead store listings by weeks to months** — `2BTR9-X4C` was granted 2026-07-20 and
the X4 Classic appeared in the store on 2026-09-06. The grantee index is therefore a **forward
indicator**, not just a record.

### What the exhibits give you that the vendor does not

- **Internal photographs** — the X3's and the X4's were never withheld, and the X4's are the
  **first public teardown of that device**.
- Antenna part numbers, gains and VSWR. The
  [KH3216-A35](../../components/generic/kh3216-a35-chip-antenna/README.md) record exists only
  because of an antenna report.
- Battery part number, capacity and cell date code, read off a label in a photograph.
- The legal entity, address and contact.

### What they never will

⚠ **Schematics, block diagrams and operational descriptions are under *long-term*
confidentiality on all five filings.** That is permanent. **The FCC is not a route to an Xteink
schematic.** Photographs, users manuals and test setup photos are withheld under *short-term*
confidentiality and **do** unlock — X4 Pro **2026-12-12**, X4 Classic **2027-01-16**, X4 Light
**2027-02-09**.

### Access traps

- ⚠ **`fccid.io` serves an inverted block.** Deep paths return **403** to a Chrome User-Agent
  (Cloudflare managed challenge) and **200** to `curl/8.5.0`, `WhatsApp/2.23.20.0`,
  `ChatGPT-User/1.0` and `ClaudeBot/1.0`. **The honest UA works; the disguised one does not.**
- ⚠ **The root `https://fccid.io/` returns 200 to everything**, so a reachability probe against
  the root reports a false success. **Probe a deep path.**
- ⚠ **The `.pdf` suffix is mandatory** on exhibit URLs. Without it you get a 16 KB HTML viewer.
- ⚠ **`https://fccid.io/2BTR9` prints "6 FCC IDs" and lists five.** Exactly five
  `href="/2BTR9…"` links exist in the HTML. **Trust the table, not the counter.**
- The **official** FCC endpoints (`apps.fcc.gov`, `www.fcc.gov/oet/ea/fccid`) returned **403 to
  all five user agents tried** on 2026-09-11. `fccid.io` is a **mirror** — label it as one.

Full method, with the measured user-agent matrix and the control procedure:
[`guides/research/finding-certification-records.md`](../../guides/research/finding-certification-records.md).

---

## 4. What Xteink does not publish

| Class | Status |
|---|---|
| Datasheet, schematic, BOM, EDA sources | ❌ **none, for any product** |
| Wiki, support portal, docs site | ❌ none |
| Firmware downloads, OTA URLs | ❌ none official. Community dumps exist for the X3 and X4 |
| Certification page | ❌ none — despite holding five FCC grants |
| Declaration of Conformity (CE) | ❌ none located. CE is self-declared and **has no database to search** |

**Consequence:** essentially every technical claim about an Xteink device in this repository
traces to third-party reverse engineering (`Free-Ink/freeink-sdk`, CrossPoint Reader), community
teardowns, or the FCC record. Treat vendor prose as the weakest source available.

---

## 5. Per-product checklist

1. `products.json` **and** the rendered product page — the spec table may exist only in the HTML.
2. `collections.json` — an empty collection handle predicts a launch; a device-less collection
   with live accessories signals withdrawal.
3. `https://fccid.io/2BTR9` — re-enumerate; new grants appear before products do.
4. For each FCC ID: grant date, frequencies, test firm, **exhibit list and embargo dates**.
5. Download the exhibits with a `curl` UA and the `.pdf` suffix. Validate magic bytes.
6. Diary the short-term confidentiality expiry dates. They are the cheapest future evidence.
7. Reddit `r/XTEINK` and `r/xteinkereader` for prices, channels and firsthand ownership.

---

## 6. Evidence boundary

Written **2026-09-11** from two research passes. **No Xteink hardware was handled**, no store
purchase was made, and no claim here was tested against a physical device. Every endpoint,
status code and user-agent result above was executed from one host on 2026-09-11 and may differ
from yours — the Cloudflare behaviour in particular is likely to change.

`xteink.cn` was **not reachable** from the research host, so the Chinese-market channel is
documented only through community reports. Chinese marketplaces (Taobao, JD, Xianyu) were
**bot-walled or JS-shelled** and were not sampled.
