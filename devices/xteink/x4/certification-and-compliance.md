# Certification and compliance — x4

Compiled **2026-09-11** by the round-2 index merge, from the certification pass's findings in [`archive/guides/research/artifacts/certification-and-market-2026-09-11/xteink-certification-and-pricing.md`](../../../archive/guides/research/artifacts/certification-and-market-2026-09-11/xteink-certification-and-pricing.md). Method and URL templates: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

> **Evidence status.** Everything here is `executed-success` **retrieval** of public regulatory records. **Nothing was verified against a physical device**, no board was inspected, and no label was read off real hardware.

> **Why this arrived late.** These findings were produced on 2026-09-11 but written into `scratch/` because a sibling agent held `devices/xteink/` at the time. That conflict is over; this file is the properly-filed result.

---

## 1. Summary

**FCC: granted.** `2BTR9-XTEINKX4`, 2026-01-05.

| Regime | Status |
|---|---|
| **FCC (US)** | ✅ `2BTR9-XTEINKX4` — granted **2026-01-05** |
| **CE / RED (EU)** | ⚠ no published DoC located; no database exists to search (§4) |
| **UKCA** | ⚠ not determined (§4) |
| **SRRC / CCC (CN)** | ⚠ **not searched** — database unreachable (§4) |
| **MIC 技適 (JP)** | ⚠ **not searched** — reachable, not queried (§4) |
| **ISED (CA)** | ⚠ **not searched** — 503 (§4) |

⚠ **This reverses the 2026-09-04 finding of *no FCC/CE filings*.** See §5.

---

## 2. Controls — why the results below mean anything

An absence is only evidence if the method demonstrably finds things that are present. Every
probe below ran on **2026-09-11**, in one session, against one host, with one tool.

| ID probed | HTTP | Verdict | Role |
|---|---|---|---|
| `2BTR9-XTEINKX4` | **200** | granted | **positive** — a real Xteink grant |
| `2AC7Z-ESPS3WROOM1` | **200** | granted | **positive** — ESP32-S3-WROOM-1 (Espressif), a module known to be certified |
| `2AN3WM5CARDPUTER` | **200** | granted | **positive** — M5Stack Cardputer |
| `2AN3WM5CARDPUTERZERO` | **404** | absent | **negative** — invented, plausible form |
| `2ASYE-T-DISPLAY-K230` | **404** | absent | **negative** — invented, exact LilyGO house style |
| `2ZZZZNOSUCHGRANTEE` | **404** | absent | **negative** — invented grantee |

**Positives → 200. Negatives → 404.** Raw run:
`scratch/market-and-certification/logs/fcc-controls.txt`.

These controls are the whole basis on which the absence findings below may be read as evidence.
They are reproduced in each of the five Xteink records rather than referenced once, because a
reader arriving at one device record must be able to judge that record's evidence without
chasing a link.

Beyond the ID probes, **the grantee was enumerated in full rather than guessed**: `2BTR9`
yields **five** FCC IDs and no more. A product absent from a complete grantee listing is
*absent*, not merely *un-found* — which is exactly the distinction the 2026-09-04 sweep could
not make, because it had no grantee code to enumerate.

⚠ **A counter-trap worth recording.** `https://fccid.io/2BTR9` prints **"6 FCC IDs"** in its
page header, but the applications table lists **five**, and exactly five `href="/2BTR9…"` links
exist in the HTML. The headline counter and the table disagree. **Trust the table.**

---

## 3. The whole grantee — `2BTR9`

| Field | Value |
|---|---|
| Applicant | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.** |
| Grantee code | **`2BTR9`** |
| Registered | **2025-12-21** |
| Contact | Chen Chu |
| Address | Room 1209, Yichuang International Center, Building 2B, No. 8 Golf Avenue, Guangpei Community, Guanlan Street, Longhua District, Shenzhen, China |
| FCC IDs | **5** |

| FCC ID | Granted | Device | Purpose | Record |
|---|---|---|---|---|
| `2BTR9-X4L` | **2026-08-13** | XTEINK X4 Light | Original Equipment | [`x4-light`](../x4-light/README.md) |
| `2BTR9-X4C` | **2026-07-20** | XTEINK X4 Classic | Original Equipment | [`x4-classic`](../x4-classic/README.md) |
| `2BTR9-X4PRO` | **2026-06-16** | XTEINK X4 Pro | Original Equipment | [`x4-pro`](../x4-pro/README.md) |
| `2BTR9-XTEINKX4` | **2026-01-05** | XTEINK X4 | Original Equipment | [`x4`](../x4/README.md) |
| `2BTR9-XTEINKX3` | **2025-12-26** | XTEINK X3 | Original Equipment | [`x3`](../x3/README.md) |

All five: 2402–2480 MHz (BLE) and 2412–2462 MHz (Wi-Fi, US channels 1–11). Long-term
confidentiality granted on all five for Schematics, Block Diagram and Operational Description.

**Not granted:** no FCC ID under `2BTR9` corresponds to the [**Xteink S4**](../s4/README.md) or
the [**Xteink Nano**](../nano/README.md). Against a complete enumeration with passing controls,
those two devices are **not FCC-authorised as of 2026-09-11**.

Xteink filed **Original Equipment** authorisations, not module-based ones. The internal
photographs show why: the X4 main PCB carries a **bare QFN SoC with a PCB meander antenna etched
into the board**, not a drop-in pre-certified Espressif module. A design like that cannot
inherit a module grant, so the vendor had to certify the whole device. That is consistent with,
and corroborates, the grant record.


### The `2BTR9-XTEINKX4` filing

| Field | Value |
|---|---|
| FCC ID | **`2BTR9-XTEINKX4`** |
| Device description | XTEINK X4 |
| Applicant | Shenzhen Xiaohu Xingtong Technology Co., Ltd. 🇨🇳 |
| Granted | **2026-01-05** |
| Frequency ranges | 2402-2480 MHz, 2412-2462 MHz |
| Test firm | Shenzhen CTB Testing Technology Co., Ltd. |
| Long-term confidentiality | Yes |
| Short-term confidentiality | Yes |
| Exhibit rows | 13 |
| Filing page | <https://fccid.io/2BTR9-XTEINKX4> — HTTP 200, retrieved 2026-09-11 |

**Withheld:**

- Block Diagram [Block Diagram]
- Schematics [Schematics]
- Operational Description [Operational Description]

Internal photographs are **public** and held in this record. They are the **first public teardown of the Xteink X4** — no community teardown of this device exists.

**Exhibits obtained** — US Government public records, redistribution **`allowed`**. Downloaded 2026-09-11, magic bytes validated (`%PDF`).

Retained in this record, at [`artifacts/certification/`](artifacts/certification/README.md):

| File | Bytes | SHA-256 | Exhibit type |
|---|---:|---|---|
| [`2BTR9-XTEINKX4-id-label-location-info.pdf`](artifacts/certification/2BTR9-XTEINKX4-id-label-location-info.pdf) | 253,042 | `c56a7f80a9c4c99e1762c9b0fa6dc833…` | ID Label/Location Info |
| [`2BTR9-XTEINKX4-internal-photos.pdf`](artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf) | 770,254 | `fd1623a7c9df42ba8140cea6d2618722…` | Internal Photos |

Archived out of the repository, each with a self-sufficient placeholder beside it carrying hash, size, FCC document id and five reacquisition URLs:

| Placeholder | Bytes | Exhibit type |
|---|---:|---|
| [`2BTR9-XTEINKX4-ant-test-report.pdf.ARCHIVED.md`](artifacts/certification/2BTR9-XTEINKX4-ant-test-report.pdf.ARCHIVED.md) | 2,034,400 | Test Report |
| [`2BTR9-XTEINKX4-external-photos.pdf.ARCHIVED.md`](artifacts/certification/2BTR9-XTEINKX4-external-photos.pdf.ARCHIVED.md) | 381,099 | External Photos |
| [`2BTR9-XTEINKX4-rf-exposure-info.pdf.ARCHIVED.md`](artifacts/certification/2BTR9-XTEINKX4-rf-exposure-info.pdf.ARCHIVED.md) | 76,885 | RF Exposure Info |
| [`2BTR9-XTEINKX4-users-manual.pdf.ARCHIVED.md`](artifacts/certification/2BTR9-XTEINKX4-users-manual.pdf.ARCHIVED.md) | 1,417,715 | Users Manual |

---

## 4. Other jurisdictions

| Regime | Result |
|---|---|
| **FCC (US)** | ✅ **granted** — see §1 |
| **CE / RED (EU)** | ⚠ No published DoC located; no `xteink.com` certification page exists. CE is self-declared; **there is no database to search** |
| **CE mark on product** | ⚠ **Not determined** — the `ID Label` exhibits were downloaded but not visually inspected for secondary marks. **Open work** |
| **UKCA** | ⚠ Not determined; no database exists |
| **SRRC / CCC (CN)** | ❌ **Not searched** — `wireless.miit.gov.cn` and `srrccn.org` both failed to connect. **Not an absence finding** |
| **MIC 技適 (JP)** | ⚠ **Not searched** — endpoint reachable, not queried |
| **ISED (CA)** | ⚠ **Not searched** — `sms-sgs.ic.gc.ca` returned 503 |

---

## 5. ⚠ Correction — this supersedes the 2026-09-04 finding

[`VERIFICATION-sweep-2026-09-04.md`](../../../VERIFICATION-sweep-2026-09-04.md) §6 recorded:

> **Certification and regulatory records** were checked only for Xteink (where the finding was
> that no external CE/FCC marking exists on the devices at all). No positive control was run, so
> the absence is weaker evidence than it looks.

That self-doubt was justified. The original finding confused **"no mark visible in a product
photograph"** with **"no grant exists"**. They are different claims and only the first was ever
tested.

- ✅ **Survives:** "no FCC ID is printed on the exterior of the units we photographed." Not
  re-tested here, and may well still be true.
- ❌ **Refuted:** any reading that Xteink devices are uncertified or unauthorised for the US.
  **Xteink holds five granted Original Equipment authorisations.**

47 CFR §2.935 permits an **e-label** displayed in software instead of a printed mark, which is
the ordinary arrangement for a device with a screen. **That is a likely explanation and it was
not verified.**

The original sentences in the sweep report and in the Xteink records have **not been edited**.
Dated corrections sit beneath them, and every one is listed in
[`research/passes/index-merge/corrections-requiring-review.md`](../../../research/passes/index-merge/corrections-requiring-review.md).

---

## 6. What this does **not** establish

- **No hardware was inspected.** No Xteink unit was obtained, opened or powered.
- **A grant is not a mark.** A granted FCC ID does not prove the ID is printed on the unit.
- **CE is not established.** No published Declaration of Conformity was located and **there is
  no CE database to search** — CE is a self-declaration regime. Absence of a published DoC is
  not absence of conformity.
- **The `ID Label` exhibits were downloaded but not visually inspected for secondary marks.**
  Whether a CE mark appears on Xteink label artwork is **open work**, and cheap to close.
- **SRRC / CCC (CN) did not run.** `wireless.miit.gov.cn` and `srrccn.org` both failed to
  connect (`000`) on 2026-09-11. That is a method failure, **not** an absence finding.
- **MIC 技適 (JP) did not run.** The endpoint is reachable (200) but form-driven; not queried.
- **ISED (CA) did not run.** `sms-sgs.ic.gc.ca` returned 503.
- **Schematics are permanently withheld** on all five filings, along with block diagrams and
  operational descriptions. **The FCC is not a route to an Xteink schematic.**


## 7. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| XC-1 | FCC ID `2BTR9-XTEINKX4` record | US FCC via fccid.io | **primary (regulatory)**, via mirror | regulatory record | <https://fccid.io/2BTR9-XTEINKX4> | 2026-09-11 | Grant existence, date, frequencies, exhibit list, embargo dates |
| XC-2 | FCC grantee index `2BTR9` | US FCC via fccid.io | primary via mirror | regulatory record | <https://fccid.io/2BTR9> | 2026-09-11 | The complete five-device Xteink certification history |
| XC-3 | Control run | this pass | — | executed probe | `scratch/market-and-certification/logs/fcc-controls.txt` | 2026-09-11 | That the method separates present from absent |

⚠ `fccid.io` is a **mirror**, not the FCC. The official endpoints (`apps.fcc.gov`, `www.fcc.gov/oet/ea/fccid`) returned **403 to all five user agents tried** on 2026-09-11, so no independent confirmation against the primary host was possible. Exhibit PDFs are served with FCC document IDs and lab letterheads, which is corroborating but not dispositive.

⚠ Deep `fccid.io` paths serve **403 to a Chrome User-Agent** and **200 to `curl/8.5.0`** — an *inverted* block. The honest UA works; the disguised one does not. The **root** `https://fccid.io/` returns 200 to everything, so a reachability probe against the root reports a false success. **Probe a deep path.**
---

## 8. The first public teardown of the Xteink X4

The `2BTR9-XTEINKX4` filing includes **Internal Photos** (4 pages, 15 embedded images, lab
*Shenzhen CTB Testing Technology Co., Ltd.*), and they were **not** withheld. The 2026-09-04
sweep recorded that no teardown of any Xteink device existed. One does, it has existed since
2026-01-05, and it is a US Government public record.

Retrieved 2026-09-11; rendered with `pdfimages -png`; images up to 944×708.
Held at [`artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf`](artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf).

| Finding | Confidence |
|---|---|
| Battery is **`SZA303759`, 3.7 V, 650 mAh, 2.405 Wh**, cell date-coded **2025/07/07** | ✅ **legible directly**, printed on the cell label, confirmed at two zoom levels |
| Single main PCB, roughly square, with a large **circular cut-out region** | ✅ clear |
| **Capacitive touch-wheel electrodes** — a ring of arc-shaped copper segments around that circle | ✅ clear; this is how the X4's rotary control is implemented |
| **Bare QFN SoC** (~5 × 5 mm, centre dimple) inside a silkscreened keep-out rectangle, beside an **etched meander / inverted-F PCB antenna** | ✅ clear that it is a bare SoC + PCB antenna; ❌ **the part marking is not legible** |
| **SOIC-8** package adjacent to the SoC, in the position a serial NOR flash normally occupies | ⚠ **inferred from package and placement only.** Marking not legible |
| **microSD / TF socket** (hinged metal tray) at the board edge | ✅ clear |
| USB receptacle at the opposite edge | ⚠ shape is **consistent with USB-C**; at this resolution micro-USB cannot be firmly excluded. **Not established** |
| Two further SOIC-8 parts, plausibly charger and EPD boost | ⚠ **inferred from count and placement.** Markings not legible |
| E-ink panel with FPC, separate from the main PCB | ✅ clear |

**What the photographs did not resolve: every IC marking.** The images are 944×708 for a
~70 mm board; a 2 mm package does not carry legible text at that scale. **No part number was
identified.** Reporting otherwise would be invention.

The bare-QFN-plus-etched-antenna construction is also *why* Xteink had to file Original
Equipment authorisations rather than inherit a module grant — see §3.

### ⏰ Diary — the X4 Pro teardown becomes public on 2026-12-12

Three Xteink filings withhold photographs under **short-term** confidentiality, which expires:

| Filing | Withheld exhibits | Becomes public |
|---|---|---|
| **`2BTR9-X4PRO`** | Internal Photos, Test Setup Photos, Users Manual | **2026-12-12** |
| `2BTR9-X4C` (X4 Classic) | Internal **and External** Photos, Test Setup Photos, Users Manual | **2027-01-16** |
| `2BTR9-X4L` (X4 Light) | Internal Photos, Test Setup Photos, Users Manual | **2027-02-09** |

On 2026-12-12, fetch — with a `curl` UA, **not** a browser UA:

```
https://fccid.io/2BTR9-X4PRO/Internal-Photos/<slug>.pdf
```

That is the cheapest available route to closing the X4 Pro's single-source panel pinout gap
(`R2-P2`), and the earliest of the three to unlock.
