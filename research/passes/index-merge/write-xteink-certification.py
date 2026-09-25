#!/usr/bin/env python3
"""Round-2 integration, TASK 2 — land the Xteink certification work.

Writes devices/xteink/<rec>/certification-and-compliance.md for x3, x4, x4-pro,
x4-classic and x4-light, in the house style established by the 27 records the
certification pass wrote on 2026-09-11.

Creates only.  If a file already exists it is left alone and reported, so the
caller can append a dated section instead of overwriting.
"""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..'))
os.chdir(REPO)
DRY = '--apply' not in sys.argv
TODAY = '2026-09-11'

META = json.load(open('scratch/market-and-certification/fcc/filing-metadata.json'))
plan = json.load(open(os.path.join(HERE, 'plan.json')))
byfid = collections.defaultdict(list)
for x in plan: byfid[x['fccid']].append(x)

REC = {
 'x3':         ('2BTR9-XTEINKX3', 'XTEINK X3', '2025-12-26',
   "Internal photographs are **public** and held in this record — see `artifacts/certification/`."),
 'x4':         ('2BTR9-XTEINKX4', 'XTEINK X4', '2026-01-05',
   "Internal photographs are **public** and held in this record. They are the "
   "**first public teardown of the Xteink X4** — no community teardown of this device exists."),
 'x4-pro':     ('2BTR9-X4PRO', 'XTEINK X4 Pro', '2026-06-16',
   "Internal photographs are **withheld under short-term confidentiality until 2026-12-12**."),
 'x4-classic': ('2BTR9-X4C', 'XTEINK X4 Classic', '2026-07-20',
   "Internal **and external** photographs are **withheld until 2027-01-16**."),
 'x4-light':   ('2BTR9-X4L', 'XTEINK X4 Light', '2026-08-13',
   "Internal photographs are **withheld until 2027-02-09**. External photographs are public."),
}

CONTROLS = """## 2. Controls — why the results below mean anything

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
"""

FAMILY = """## 3. The whole grantee — `2BTR9`

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
"""

CORRECTION = """## 5. ⚠ Correction — this supersedes the 2026-09-04 finding

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
[`scratch/index-merge/corrections-requiring-review.md`](../../../scratch/index-merge/corrections-requiring-review.md).
"""

NOTEST = """## 6. What this does **not** establish

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
"""

OTHER = """## 4. Other jurisdictions

| Regime | Result |
|---|---|
| **FCC (US)** | ✅ **granted** — see §1 |
| **CE / RED (EU)** | ⚠ No published DoC located; no `xteink.com` certification page exists. CE is self-declared; **there is no database to search** |
| **CE mark on product** | ⚠ **Not determined** — the `ID Label` exhibits were downloaded but not visually inspected for secondary marks. **Open work** |
| **UKCA** | ⚠ Not determined; no database exists |
| **SRRC / CCC (CN)** | ❌ **Not searched** — `wireless.miit.gov.cn` and `srrccn.org` both failed to connect. **Not an absence finding** |
| **MIC 技適 (JP)** | ⚠ **Not searched** — endpoint reachable, not queried |
| **ISED (CA)** | ⚠ **Not searched** — `sms-sgs.ic.gc.ca` returned 503 |
"""

def build(rec):
    fid, name, granted, photonote = REC[rec]
    m = META[fid]
    rows = byfid[fid]
    keep = [r for r in rows if r['dest'] and os.path.exists(r['dest'])]
    arch = [r for r in rows if r['disposition'] == 'archive']
    L = [f"# Certification and compliance — {rec}", "",
         f"Compiled **{TODAY}** by the round-2 index merge, from the certification pass's "
         "findings in "
         "[`scratch/market-and-certification/xteink-certification-and-pricing.md`]"
         "(../../../scratch/market-and-certification/xteink-certification-and-pricing.md). "
         "Method and URL templates: "
         "[`guides/research/finding-certification-records.md`]"
         "(../../../guides/research/finding-certification-records.md).", "",
         "> **Evidence status.** Everything here is `executed-success` **retrieval** of public "
         "regulatory records. **Nothing was verified against a physical device**, no board was "
         "inspected, and no label was read off real hardware.", "",
         "> **Why this arrived late.** These findings were produced on 2026-09-11 but written "
         "into `scratch/` because a sibling agent held `devices/xteink/` at the time. That "
         "conflict is over; this file is the properly-filed result.", "",
         "---", "", "## 1. Summary", "",
         f"**FCC: granted.** `{fid}`, {granted}.", "",
         "| Regime | Status |", "|---|---|",
         f"| **FCC (US)** | ✅ `{fid}` — granted **{granted}** |",
         "| **CE / RED (EU)** | ⚠ no published DoC located; no database exists to search (§4) |",
         "| **UKCA** | ⚠ not determined (§4) |",
         "| **SRRC / CCC (CN)** | ⚠ **not searched** — database unreachable (§4) |",
         "| **MIC 技適 (JP)** | ⚠ **not searched** — reachable, not queried (§4) |",
         "| **ISED (CA)** | ⚠ **not searched** — 503 (§4) |", "",
         "⚠ **This reverses the 2026-09-04 finding of "
         "*no FCC/CE filings*.** See §5.", "", "---", "", CONTROLS, "---", "", FAMILY, "",
         f"### The `{fid}` filing", "", "| Field | Value |", "|---|---|",
         f"| FCC ID | **`{fid}`** |",
         f"| Device description | {m.get('desc') or name} |",
         f"| Applicant | {m.get('applicant', 'unknown')} |",
         f"| Granted | **{granted}** |",
         f"| Frequency ranges | {', '.join(m.get('freq') or []) or 'unknown'} |",
         f"| Test firm | {m.get('test_firm', 'unknown')} |",
         f"| Long-term confidentiality | {m.get('lt_conf', '?')} |",
         f"| Short-term confidentiality | {m.get('st_conf', '?')} |",
         f"| Exhibit rows | {m.get('n_exhibits', '?')} |",
         f"| Filing page | <https://fccid.io/{fid}> — HTTP 200, retrieved {TODAY} |", "",
         "**Withheld:**", ""]
    for w in m.get('withheld_rows', []): L.append(f"- {w}")
    L += ["", photonote, "",
          "**Exhibits obtained** — US Government public records, redistribution **`allowed`**. "
          f"Downloaded {TODAY}, magic bytes validated (`%PDF`).", ""]
    if keep:
        L += ["Retained in this record, at "
              "[`artifacts/certification/`](artifacts/certification/README.md):", "",
              "| File | Bytes | SHA-256 | Exhibit type |", "|---|---:|---|---|"]
        for r in sorted(keep, key=lambda r: r['dest']):
            L.append(f"| [`{os.path.basename(r['dest'])}`](artifacts/certification/"
                     f"{os.path.basename(r['dest'])}) | {r['bytes']:,} | `{r['sha256'][:32]}…` "
                     f"| {r['exhibit_type']} |")
        L.append("")
    if arch:
        L += ["Archived out of the repository, each with a self-sufficient placeholder beside "
              "it carrying hash, size, FCC document id and five reacquisition URLs:", "",
              "| Placeholder | Bytes | Exhibit type |", "|---|---:|---|"]
        for r in sorted(arch, key=lambda r: r['dest']):
            b = os.path.basename(r['dest'])
            L.append(f"| [`{b}.ARCHIVED.md`](artifacts/certification/{b}.ARCHIVED.md) "
                     f"| {r['bytes']:,} | {r['exhibit_type']} |")
        L.append("")
    L += ["---", "", OTHER, "---", "", CORRECTION, "---", "", NOTEST, "",
          "## 7. Sources", "",
          "| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |",
          "|---|---|---|---|---|---|---|---|",
          f"| XC-1 | FCC ID `{fid}` record | US FCC via fccid.io | **primary (regulatory)**, "
          f"via mirror | regulatory record | <https://fccid.io/{fid}> | {TODAY} | Grant "
          "existence, date, frequencies, exhibit list, embargo dates |",
          f"| XC-2 | FCC grantee index `2BTR9` | US FCC via fccid.io | primary via mirror | "
          f"regulatory record | <https://fccid.io/2BTR9> | {TODAY} | The complete five-device "
          "Xteink certification history |",
          "| XC-3 | Control run | this pass | — | executed probe | "
          f"`scratch/market-and-certification/logs/fcc-controls.txt` | {TODAY} | That the "
          "method separates present from absent |", "",
          "⚠ `fccid.io` is a **mirror**, not the FCC. The official endpoints (`apps.fcc.gov`, "
          "`www.fcc.gov/oet/ea/fccid`) returned **403 to all five user agents tried** on "
          f"{TODAY}, so no independent confirmation against the primary host was possible. "
          "Exhibit PDFs are served with FCC document IDs and lab letterheads, which is "
          "corroborating but not dispositive.", "",
          "⚠ Deep `fccid.io` paths serve **403 to a Chrome User-Agent** and **200 to "
          "`curl/8.5.0`** — an *inverted* block. The honest UA works; the disguised one does "
          "not. The **root** `https://fccid.io/` returns 200 to everything, so a reachability "
          "probe against the root reports a false success. **Probe a deep path.**", ""]
    return "\n".join(L)

for rec in REC:
    p = f"devices/xteink/{rec}/certification-and-compliance.md"
    if os.path.exists(p):
        print(f"  EXISTS (append instead): {p}"); continue
    if not DRY:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(build(rec))
    print(f"  {'would write' if DRY else 'WROTE'}: {p}")
