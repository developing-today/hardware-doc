# Xteink — certification and pricing

Compiled **2026-09-11**.

> **Promoted into the repository 2026-09-20** from
> `archive/guides/research/artifacts/certification-and-market-2026-09-11/xteink-certification-and-pricing.md`.
> **34 repository records cited it through an `archive/…` path** as the authority for a dated
> correction — and the archive is machine-local, so someone cloning this repository never had it.
> That is the same defect the [index-merge pass](../../research/passes/index-merge/README.md)
> fixed for its own documents. Content is unchanged; all 34 citations were repointed here. The
> archive copy is retained and marked superseded.
>
> The note below about `devices/xteink/` being off-limits was true **on 2026-09-11** and is left
> as written, because it is the record of why the file was created outside this tree. It no longer
> applies: the file now lives here. Its findings have **not** yet been merged into the five
> per-device `certification-and-compliance.md` records — see
> [§ Unfinished](#unfinished-as-of-2026-09-20) at the end.

> **Why this is not in `devices/xteink/`.** That tree is owned by a concurrent sibling agent for
> the duration of this session, and this pass was forbidden to write into it. Everything below is
> ready to move or cite; nothing in `devices/xteink/` was read-modified or written.

---

## 1. The headline: the 2026-09-04 sweep's certification finding is wrong

[`VERIFICATION-sweep-2026-09-04.md`](../../VERIFICATION-sweep-2026-09-04.md) §6 records:

> **Certification and regulatory records** were checked only for Xteink (where the finding was
> that no external CE/FCC marking exists on the devices at all). No positive control was run, so
> the absence is weaker evidence than it looks.

That self-doubt was justified. **Xteink is an FCC grantee with five granted equipment
authorisations.**

| Field | Value |
|---|---|
| Applicant | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.** |
| Grantee code | **`2BTR9`** |
| Registered | **2025-12-21** |
| Contact | Chen Chu |
| Address | Room 1209, Yichuang International Center, Building 2B, No. 8 Golf Avenue, Guangpei Community, Guanlan Street, Longhua District, Shenzhen, China |
| FCC IDs | **5** (the page header claims 6 — see the trap below) |

| FCC ID | Date | Product | Purpose |
|---|---|---|---|
| `2BTR9-X4L` | **2026-08-13** | XTEINK X4 Light | Original Equipment |
| `2BTR9-X4C` | **2026-07-20** | XTEINK X4 Classic | Original Equipment |
| `2BTR9-X4PRO` | **2026-06-16** | XTEINK X4 Pro | Original Equipment |
| `2BTR9-XTEINKX4` | **2026-01-05** | XTEINK X4 | Original Equipment |
| `2BTR9-XTEINKX3` | **2025-12-26** | XTEINK X3 | Original Equipment |

All five: 2402–2480 MHz (BLE) and 2412–2462 MHz (Wi-Fi, US ch 1–11). Long-term confidentiality
granted on all five for Schematics, Block Diagram and Operational Description.

### How the two claims differ, and which one survives

The sweep made a claim about **markings on photographs**. That claim may well still be true — it
was not re-tested here. What does **not** follow from it is the claim about **grants**, and the
sweep's own wording ("no external CE/FCC marking exists on the devices at all") reads naturally
as the latter.

- ✅ **Survives:** "no FCC ID is printed on the exterior of the units we photographed."
- ❌ **Refuted:** any reading that Xteink devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** displayed in software instead of a printed mark, which is
the ordinary arrangement for a device with a screen. **This is a likely explanation and it was
not verified.**

### Also notable

Xteink filed **Original Equipment** authorisations, not module-based ones. The FCC internal
photographs (below) show why: the X4 main PCB carries a **bare QFN SoC with a PCB meander
antenna etched into the board**, not a drop-in pre-certified Espressif module. A design like
that cannot inherit a module grant, so the vendor had to certify the whole device. That is
consistent with, and corroborates, the grant record.

---

## 2. Controls

Same run as everything else this pass — `logs/fcc-controls.txt`, **2026-09-11**:

| ID | HTTP | Role |
|---|---|---|
| `2BTR9-XTEINKX4` | **200** | positive |
| `2AC7Z-ESPS3WROOM1` | **200** | positive (ESP32-S3-WROOM-1) |
| `2AN3WM5CARDPUTER` | **200** | positive |
| `2AN3WM5CARDPUTERZERO` | **404** | negative, invented |
| `2ASYE-T-DISPLAY-K230` | **404** | negative, invented |
| `2ZZZZNOSUCHGRANTEE` | **404** | negative, invented |

4/4 positive → 200, 5/5 negative → 404. The grantee page was enumerated in full, so the absence
of an `S4` or `Nano` grant is an absence against a complete listing.

**Not granted:** no FCC ID under `2BTR9` corresponds to the **Xteink S4** or **Xteink Nano**
records in this repo. Those two devices are **not FCC-authorised as of 2026-09-11**.

### Trap worth recording

`https://fccid.io/2BTR9` prints **"6 FCC IDs"** in its header but the applications table lists
**five**, and exactly five `href="/2BTR9…"` links exist in the HTML. The headline counter and the
table disagree. **Trust the table.**

---

## 3. First public teardown of the Xteink X4

The `2BTR9-XTEINKX4` filing includes **Internal Photos** (4 pages, 15 embedded images, lab
*Shenzhen CTB Testing Technology Co., Ltd.*). The sweep recorded that no teardown of any Xteink
device existed. One does; it is a US Government public record.

Downloaded 2026-09-11 to `fcc/2BTR9-XTEINKX4/`, rendered with
`pdfimages -png`, images up to 944×708.

**Resolved from the photographs:**

| Finding | Confidence |
|---|---|
| Battery is **`SZA303759`, 3.7 V, 650 mAh, 2.405 Wh**, cell date-coded **2025/07/07** | ✅ **legible directly**, printed on the cell label, confirmed at 2 zoom levels |
| Single main PCB, roughly square, with a large **circular cut-out region** | ✅ clear |
| **Capacitive touch-wheel electrodes** — a ring of arc-shaped copper segments around that circle | ✅ clear; this is how the X4's rotary control is implemented |
| **Bare QFN SoC** (~5 × 5 mm, centre dimple) inside a silkscreened keep-out rectangle, beside an **etched meander/inverted-F PCB antenna** | ✅ clear that it is a bare SoC + PCB antenna; ❌ **the part marking is not legible** |
| **SOIC-8** package adjacent to the SoC, in the position a serial NOR flash normally occupies | ⚠ **inferred from package and placement only.** Marking not legible |
| **microSD / TF socket** (hinged metal tray) at the board edge | ✅ clear |
| USB receptacle at the opposite edge | ⚠ shape is **consistent with USB-C**; at this resolution micro-USB cannot be firmly excluded. **Not established** |
| Two further SOIC-8 parts, plausibly charger and EPD boost | ⚠ **inferred from count and placement.** Markings not legible |
| E-ink panel with FPC, separate from the main PCB | ✅ clear |

**What the photographs did not resolve:** every IC marking. The images are 944×708 for a
~70 mm board; a 2 mm package simply does not carry legible text at that scale. **No part number
was identified.** Reporting it otherwise would be invention.

### ⏰ Diary entry: the X4 Pro teardown becomes public on 2026-12-12

The sweep's §6 says *"The Xteink X4 Pro record traces substantially to one commit. No teardown,
no firmware dump and no price-independent corroboration were obtained for the family's
flagship."*

The teardown exists and has a **release date**. Three Xteink filings withhold photographs under
**short-term** confidentiality, which expires:

| Filing | Withheld exhibits | Becomes public |
|---|---|---|
| **`2BTR9-X4PRO`** | Internal Photos, Test Setup Photos, Users Manual | **2026-12-12** |
| `2BTR9-X4C` (X4 Classic) | Internal **and External** Photos, Test Setup Photos, Users Manual | **2027-01-16** |
| `2BTR9-X4L` (X4 Light) | Internal Photos, Test Setup Photos, Users Manual | **2027-02-09** |

On 2026-12-12, fetch:

```
https://fccid.io/2BTR9-X4PRO/Internal-Photos/<slug>.pdf     # curl UA, not a browser UA
```

The X3 and X4 internal photos were **not** withheld and are already held locally.

---

## 4. Dated pricing — `xteink.com`, 2026-09-11

Source: **`https://xteink.com/products.json?limit=250&page=1`**, retrieved **2026-09-11**.
Full catalogue: **25 products**, enumerated completely. Ships from: not stated by the endpoint.
Currency USD as served; no conversion applied. Condition: new, genuine (manufacturer store).

| Product | Published | Variant | SKU | Price | In stock |
|---|---|---|---|---|---|
| Xteink X3 Pocket eReader | 2025-12-11 | X3 Mist Gray | `xteink-x3-white` | **USD 69.00** | ✅ |
| Xteink X3 Pocket eReader | 2025-12-11 | X3 Space Black | `xteink-x3-black` | **USD 69.00** | ✅ |
| Xteink X3 Pocket eReader | 2025-12-11 | X3 + Mist Gray Base | `xteink-x3B+BW` | **USD 85.00** | ✅ |
| Xteink X3 Pocket eReader | 2025-12-11 | X3 + Space Black Base | `X3W+BB` | **USD 85.00** | ✅ |
| **XTEINK X4 Classic (X4 V2)** | **2026-09-06** | Mist Gray | `X4Classic-gray` | **USD 79.00** | ✅ |
| XTEINK X4 Classic (X4 V2) | 2026-09-06 | Space Black | `X4Classic-black` | **USD 79.00** | ✅ |
| XTEINK X4 Classic (X4 V2) | 2026-09-06 | + Base (4 combos) | `X4CW+BW` etc. | **USD 95.00** | ✅ |
| **Xteink X4 Pro Pocket eReader** | 2026-07-21 | Space Black | `X4Pro-Black` | **USD 99.00** | ✅ |
| Xteink X4 Pro Pocket eReader | 2026-07-21 | + Mist Sage Base | `X4PB+BW` | **USD 115.00** | ❌ |
| Xteink X4 Pro Pocket eReader | 2026-07-21 | + Space Black Base | — | **USD 115.00** | ❌ |

Citation form per `guides/markets/vendor-comparison.md` § *A note on prices*:

> *USD 99.00, 1 unit, retrieved 2026-09-11, `https://xteink.com/products/xteink-x4-pro-pocket-ereader`, ships from CN (origin not stated by vendor)*

### Two findings from the catalogue

1. ✅ **The X4 Pro is USD 99.00.** This **independently confirms** correction #4 claim 2 in
   `../index-merge/corrections-requiring-review.md`, which recorded USD 99.00 observed
   2026-09-04 from the same endpoint. Two observations, one week apart, identical. **The
   PaperMono record's "the XTEINK X4 Pro … was never priced" is wrong on both dates.**

2. ⚠ **The plain X4 is gone from the store.** Of the 25 products, none is a bare "Xteink X4".
   The X4 Classic's own store title is **"XTEINK X4 Classic (X4 V2)"** — the vendor is stating
   that the Classic *is* the second version of the X4. The `devices/xteink/x4/` record therefore
   documents a **withdrawn** product, and `x4-classic` its successor. **The FCC record agrees**:
   `2BTR9-XTEINKX4` (2026-01-05) then `2BTR9-X4C` (2026-07-20).

3. ⚠ **`2BTR9-X4L` "XTEINK X4 Light" has no storefront listing** as of 2026-09-11 — certified
   2026-08-13 but not on sale. An **unreleased or imminent product**, and not a device record in
   this repo. Its internal photos unlock 2027-02-09.

### Accessories, for completeness

Magnetic reading light USD 9.99 / 15.99 · magnetic case USD 8.99 · matte screen protector
USD 3.99–8.39 · adhesive metal ring USD 4.99–7.99 · pogo-pin charging cable USD 4.99 ·
magnetic charging adapter USD 5.99. Plus six **service** line-items (handling fees, shipping fee,
after-sale charges) which are **not products** and must be excluded from any price range — a
naive "cheapest item in the store" read would return USD 1.00.

### Not obtained

AliExpress, Amazon, eBay, Taobao, JD and used/refurbished: **all blocked or JS-shelled** from
this host on 2026-09-11 (see `README.md`). **No street, clone or used Xteink price is reported,
because none was observed.**

---

## 5. Other jurisdictions

| Regime | Result |
|---|---|
| **CE / RED** | ⚠ No published DoC located. No `xteink.com` certification page exists. CE is self-declared; **there is no database to search** |
| **CE mark on product** | ⚠ **Not determined.** The X4/X3 `ID Label` exhibits were downloaded but not visually inspected for secondary marks in this pass — **open work** |
| **UKCA** | ⚠ Not determined; no database exists |
| **SRRC / CCC (CN)** | ❌ **Not searched** — `wireless.miit.gov.cn` and `srrccn.org` both failed to connect. **Not an absence finding** |
| **MIC 技適 (JP)** | ⚠ **Not searched** — endpoint reachable, not queried |
| **ISED (CA)** | ⚠ **Not searched** — `sms-sgs.ic.gc.ca` returned 503 |

---

## 6. Ready-to-apply summary for whoever owns `devices/xteink/`

Per-device, one line each:

- **`x3/`** — FCC `2BTR9-XTEINKX3`, granted **2025-12-26**. Internal photos available.
- **`x4/`** — FCC `2BTR9-XTEINKX4`, granted **2026-01-05**. Internal photos available (teardown above). **Withdrawn from the store; superseded by X4 Classic, which the vendor titles "X4 V2".**
- **`x4-pro/`** — FCC `2BTR9-X4PRO`, granted **2026-06-16**. **USD 99.00** confirmed 2026-09-11. Internal photos withheld until **2026-12-12**.
- **`x4-classic/`** — FCC `2BTR9-X4C`, granted **2026-07-20**. **USD 79.00** (bare) / 95.00 (with base). Internal *and external* photos withheld until **2027-01-16**.
- **`s4/`** — ❌ **no FCC grant** under `2BTR9` (complete enumeration, controls passed).
- **`nano/`** — ❌ **no FCC grant** under `2BTR9` (same).
- **New, undocumented:** **X4 Light**, FCC `2BTR9-X4L`, granted 2026-08-13, **not yet on sale**.

And the sweep-level correction: **§6's certification bullet in
`VERIFICATION-sweep-2026-09-04.md` should be superseded, not merely annotated.**

---

## Unfinished as of 2026-09-20

Recorded by the archive audit that promoted this file, so the state is not mistaken for completeness:

- **Not merged into the per-device records.** The five
  `devices/xteink/*/certification-and-compliance.md` files cite this document, but the grant
  numbers, dates and photo-embargo dates above have not been written into them. Until that
  happens this page is the only place they exist.
- **The sweep-level correction is still outstanding.** `VERIFICATION-sweep-2026-09-04.md` §6 is
  annotated, not superseded, exactly as the line above asks.
- **Internal photographs are barely mined.** The X4 internal-photo exhibits are held
  (`devices/xteink/x4/artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf`) and a montage
  was rendered, but no part census was taken from them — the same gap the
  [index-merge round-two workdir](../../archive/research/passes/index-merge/round-two-workdir-2026-09-11/README.md)
  flags.
