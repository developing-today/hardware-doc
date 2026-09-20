# Finding certification and regulatory records

**Created 2026-09-11.** Method guide for source class **3** in
[`.agents/skills/hardware-device-research/SKILL.md`](../../.agents/skills/hardware-device-research/SKILL.md)
§3 — *standards bodies and certification/regulatory databases*.

Everything below was **live-probed on 2026-09-11** from this host. Every URL template carries a
measured status code. Two controls — one positive, one negative — are run and recorded, because
**without them an "absent" result is not evidence.**

---

## 0. Why this guide exists

A seven-session sweep searched for Xteink certification records, found none, and wrote that
"no external CE/FCC marking exists on the devices at all". It then honestly added: *"No positive
control was run, so the absence is weaker evidence than it looks."*

It was right to worry. **Xteink holds FCC grantee code `2BTR9` with five granted FCC IDs.**
The search method, not the world, was at fault.

Two distinct failures produced that result, and both are common:

1. **No control.** If your search returns nothing for a device that *is* certified, you cannot
   tell "not certified" from "search broken". You must prove the method finds a known-good
   record *in the same run*.
2. **Conflating two claims.** "No mark visible in a product photo" and "no certification grant
   exists" are different propositions with different evidence. A device may legally carry an
   **e-label** in software instead of a printed mark (47 CFR §2.935). Never let one stand in for
   the other.

---

## 1. Run the controls first. Always.

Before believing any absence, run both in the same session and record the status codes.

```bash
UA='curl/8.5.0'
probe(){ printf '%-24s %s\n' "$1" "$(curl -sL -A "$UA" --max-time 30 \
        -o /dev/null -w '%{http_code}' "https://fccid.io/$1")"; }

# POSITIVE — must return 200. Pick something you are certain is certified.
probe 2AC7Z-ESPS3WROOM1      # ESP32-S3-WROOM-1, Espressif. The module inside half these boards.
probe 2AN3WM5CARDPUTER       # a device you already enumerated from its grantee page

# NEGATIVE — must return 404. Invent IDs that look completely plausible.
probe 2AN3WM5CARDPUTERZERO   # right grantee, plausible product code, does not exist
probe 2ASYE-T-DISPLAY-K230   # matches LilyGO's hyphenated house style exactly
probe 2ZZZZNOSUCHGRANTEE     # invented grantee
```

Measured 2026-09-11 (`logs/fcc-controls.txt` in the scratch dir; status: `executed-success`):

| ID probed | HTTP | Bytes | Verdict | Role |
|---|---|---|---|---|
| `2AC7Z-ESPS3WROOM1` | **200** | 75 066 | granted | **positive** — ESP32-S3-WROOM-1 |
| `2AC7Z-ESPS3WROOM1U` | **200** | 31 810 | granted | **positive** — U.FL variant |
| `2AN3WM5CARDPUTER` | **200** | 30 445 | granted | **positive** |
| `2BTR9-XTEINKX4` | **200** | 22 648 | granted | **positive** |
| `2AN3WM5CARDPUTERZERO` | **404** | 8 981 | absent | **negative** — invented |
| `2ASYE-T-DISPLAY-K230` | **404** | 9 005 | absent | **negative** — invented |
| `2AN3WM5CAPLORA868` | **404** | 8 930 | absent | **negative** — invented sibling of a real ID |
| `2AC7Z-ESPZZ9NOTREAL` | **404** | 8 965 | absent | **negative** — invented under a real grantee |
| `2ZZZZNOSUCHGRANTEE` | **404** | 8 599 | absent | **negative** — invented grantee |

4/4 positive → 200. 5/5 negative → 404. **The discriminator is the HTTP status code, cleanly
separated.** Now — and only now — a 404 means something.

> Do **not** use body text as the discriminator. A first attempt here grepped for the word
> `Exhibits` and scored all nine probes "found", because the string appears in site navigation
> on the 404 page too. Status code, not page text.

---

## 2. The grantee-code trick

This is the core technique and it inverts the obvious approach.

**Do not guess FCC IDs one at a time.** An FCC ID is `<grantee code><product code>`. The grantee
code is a stable 3–5 character identifier assigned once per company; the product code is chosen
freely by the applicant and is unguessable (`2AN3WSTAMPLORA1262` has no `M5` prefix while
`2AN3WM5CAPLORA1262` does — same company, same year, same product family).

So: **find the grantee code once, then enumerate everything under it.**

```bash
# Step 1 — company search finds the grantee code
curl -s -A 'curl/8.5.0' 'https://fccid.io/search?q=LilyGO'
#   → Shenzhen Xin Yuan Electronic Technology Co., Ltd. (2ASYE)

# Step 2 — the grantee page lists every ID, with dates and product names, on one page
curl -sL -A 'curl/8.5.0' 'https://fccid.io/2ASYE' -o grantee.html
```

Search the **legal entity name**, not the brand. LilyGO's filings are all under *Shenzhen Xin
Yuan Electronic Technology Co., Ltd.*; Xteink's are under *Shenzhen Xiaohu Xingtong Technology
Co., Ltd.* A brand-name search happened to work for both here, but only because fccid.io indexes
product names as well.

Grantee codes established 2026-09-11:

| Brand | Legal applicant | Grantee | Registered | IDs |
|---|---|---|---|---|
| **M5Stack** | M5Stack Technology Co.,Ltd | **`2AN3W`** | 2017-10-23 | 59 |
| **LilyGO** | Shenzhen Xin Yuan Electronic Technology Co., Ltd. | **`2ASYE`** | 2019-04-05 | 33 |
| **Espressif** | ESPRESSIF SYSTEMS (SHANGHAI) CO., LTD | **`2AC7Z`** | 2014-09-15 | 78–80 |
| **Xteink** | Shenzhen Xiaohu Xingtong Technology Co., Ltd. | **`2BTR9`** | 2025-12-21 | 5 |

Parse the grantee page with:

```python
pat = re.compile(
  r'<tr><td data-label="FCC ID / Date"><b><a href="/([^"]+)">[^<]+</a></b><br>([\d-]+)</td>'
  r'<td data-label="Product / Type">(.*?)<br>(.*?)</td></tr>', re.S)
```

**Trap:** the grantee page header for `2BTR9` says *"6 FCC IDs"* but the table lists **5**, and
only 5 `href`s exist. The headline count and the table disagree. Trust the table; report the
discrepancy.

**Trap:** `?page=N` on a grantee URL returns **302** and drops you. Fetch the bare
`https://fccid.io/<GRANTEE>` and read `Page N of M` from the panel heading instead. All four
grantees above fit on one page.

---

## 3. Which databases are reachable without login

Measured 2026-09-11, browser UA unless noted.

| Database | URL | HTTP | Login? | Verdict |
|---|---|---|---|---|
| **fccid.io** (FCC mirror) | `https://fccid.io/<ID>` | **200** *(with `curl` UA — see §4)* | no | ✅ **the workhorse** |
| FCC official EA search | `https://apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm` | **403** | n/a | ❌ blocked to all 5 UAs |
| FCC official EA landing | `https://www.fcc.gov/oet/ea/fccid` | **403** | n/a | ❌ blocked to all 5 UAs |
| FCC attachment endpoint | `https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=N` | **403** | n/a | ❌ blocked |
| FCC open data | `https://opendata.fcc.gov/resource/kfc9-pnvf.json` | **404** | no | ❌ EAS is not published there under that ID |
| fcc.report (mirror) | `https://fcc.report/FCC-ID/<ID>` | **403** | n/a | ❌ blocked to all 5 UAs |
| **Japan MIC 技適** | `https://www.tele.soumu.go.jp/giteki/SearchServlet?pageID=js01` | **200** | no | ✅ reachable; form-driven, not probed further |
| Japan MIC (English) | `https://www.tele.soumu.go.jp/e/index.htm` | **200** | no | ✅ reachable |
| China CCC (CNCA) | `https://www.cnca.gov.cn/` | **200** | no | ⚠ portal reachable; the searchable CCC register was not reached |
| China MIIT | `https://www.miit.gov.cn/` | **200** | no | ⚠ portal only |
| **China SRRC** | `https://wireless.miit.gov.cn/`, `https://www.srrccn.org/` | **000** | n/a | ❌ **connection failed** — no SRRC lookup achieved |
| ISED Canada REL | `https://sms-sgs.ic.gc.ca/equipmentSearch/searchRadioEquipments?lang=en` | **503** | no | ❌ service unavailable at probe time; retry |
| ISED CEB | `https://ised-isde.canada.ca/site/certification-engineering-bureau/en` | **200** | no | ✅ landing only |
| UKCA | `https://www.gov.uk/guidance/using-the-ukca-marking` | **200** | no | ℹ️ **guidance only. There is no UKCA database.** |

### On UKCA and CE: there is no database to search

This trips people up. **CE/UKCA are self-declaration regimes.** No public register of conformity
exists for either. The only primary artifact is the manufacturer's own **Declaration of
Conformity (DoC)**, published at the vendor's discretion. If the vendor does not publish one,
there is nothing to find and *that is the finding*.

Checked 2026-09-11, all **404**:

- `shop.m5stack.com/pages/certificate`
- `docs.m5stack.com/en/certificate`
- `www.lilygo.cc/pages/certification`

So for these vendors: **no published DoC was located.** State it that way — not "not CE marked".
The Cardputer ADV label photograph (§5) shows a **CE mark is printed on the product**, which
means a DoC legally exists; it simply is not published.

---

## 4. ⚠ The inverted user-agent block on fccid.io

`AGENTS.md` teaches: plain request first, then a browser UA, then bot UAs. **On fccid.io that
ladder is backwards.**

| UA | `fccid.io/` | `fccid.io/2AN3W` | `fccid.io/search?q=…` |
|---|---|---|---|
| `Chrome/131.0.0.0` (browser) | 200 | **403** | **403** |
| `WhatsApp/2.23.20.0` | 200 | **200** | **200** |
| `ChatGPT-User/1.0` | 200 | **200** | **200** |
| `ClaudeBot/1.0` | 200 | **200** | **200** |
| `curl/8.5.0` | 200 | **200** | **200** |

The 403 is a **Cloudflare managed challenge** (`Security check`, `cType: 'managed'`,
`cZone: 'fccid.io'`) requiring JS and cookies. Cookie jars and `Accept`/`Accept-Language` headers
do not help. The honest `curl/8.5.0` UA passes.

Note also that the **root** page returns 200 to everything, so a reachability probe against
`https://fccid.io/` alone reports "site is up" and tells you nothing. **Probe a deep path.**

Per `AGENTS.md` rule 6: a 200 obtained this way is a *retrieval* result only. It is not evidence
that the resource behaves this way for ordinary clients, and it must not be used to bypass
authentication or access control. These are public records with no access control; the block is
anti-scraping, not authorisation.

---

## 5. Mining the exhibits — often the only public teardown

FCC filings are **US Government public records**. For a board with no published schematic, the
filing is frequently the only internal photography that exists anywhere.

### Verified download template

```
https://fccid.io/<FCC-ID>/<Type-Slug>/<Document-Slug>-<exhibit-id>.pdf
```

The **`.pdf` suffix is what matters.** The same URL without it returns a 16 KB HTML viewer page.

```bash
# verified 2026-09-11: 200, application/pdf, 1 848 880 bytes
curl -sL -A 'curl/8.5.0' \
  'https://fccid.io/2AN3WM5CARDPUTERADV/Internal-Photos/Internal-Photos-8755029.pdf' \
  -o internal.pdf
```

Scrape the exhibit table from the filing page:

```python
EXH = re.compile(
  r'<tr><td data-label="Document"><a href="(?P<href>[^"]+)">(?P<doc>.*?)</a></td>'
  r'<td data-label="Type">(?P<type>.*?)</td>'
  r'<td data-label="Available">(?P<avail>.*?)</td>'
  r'<td data-label="File">(?P<file>.*?)</td></tr>', re.S)
# then: url = 'https://fccid.io' + href + '.pdf'
```

A reusable harvester is at `scratch/market-and-certification/fcc/harvest.py`.
Run 2026-09-11 over 26 filings: **~170 PDFs, 198 MB, 0 failures, 0 type mismatches.**

### Which exhibit types are worth the bytes

| Type | Value | Note |
|---|---|---|
| **Internal Photos** | ⭐⭐⭐ | The teardown. Board top/bottom, shields off, connectors, battery labels |
| **ID Label/Location Info** | ⭐⭐⭐ | **Shows other jurisdictions' marks** — CE, UKCA, WEEE, IC, 技適 |
| External Photos | ⭐⭐ | Enclosure, ports, dimensions against a ruler |
| Test Report | ⭐⭐ | Antenna gain, conducted power, exact frequency edges |
| RF Exposure Info | ⭐ | Separation distance, SAR/MPE |
| Users Manual | ⭐ | Sometimes a pre-release manual not on the vendor site |
| **Schematics** | — | **Essentially always withheld.** See below |
| **Block Diagram** | — | Essentially always withheld |
| **Operational Description** | — | Essentially always withheld |

### Confidentiality: what you will and will not get

**Long-term confidentiality was requested and granted on 26 of 26 filings examined.** In every
single case the withheld set was the same three: **Schematics, Block Diagram, Operational
Description.** Do not plan on getting a schematic out of the FCC. Plan on getting photographs.

**Short-term confidentiality is different and it expires.** Three Xteink filings withhold
photographs until a stated date:

| Filing | Withheld | Released on |
|---|---|---|
| `2BTR9-X4PRO` | Internal Photos, Test Setup Photos, Users Manual | **2026-12-12** |
| `2BTR9-X4C` | Internal + **External** Photos, Test Setup Photos, Users Manual | **2027-01-16** |
| `2BTR9-X4L` | Internal Photos, Test Setup Photos, Users Manual | **2027-02-09** |

**These dates are diary entries.** The Xteink X4 Pro currently has no public teardown anywhere;
on 2026-12-12 it will have one. Record the date in the device record rather than concluding "no
teardown exists".

### ⚠ The exhibit trap that will bite you: labels are photographs

A tempting one-liner: extract the text layer of every `ID Label` exhibit and grep for `CE`,
`IC:`, `CMIIT`, `UKCA`.

Run over 26 filings on 2026-09-11 it reported **"no secondary marks" on 26 of 26.** That result
is **entirely false**, and it is a perfect miniature of the mistake this guide exists to prevent.

`pdfimages -list` on the Cardputer ADV label:

```
page num type  width height color comp bpc enc  ... size ratio
   1   0 image   947   705 rgb      3   8 jpeg  ... 140K  7.2%
```

The whole label is **one JPEG photograph**. The PDF text layer contains exactly two things: the
word `Label` and the string `FCC ID: 2AN3WM5CARDPUTERADV`. There is nothing to grep.

Rendering and looking at that same image shows, on the StampS3A module label: the **FCC logo**,
a **CE mark**, a **crossed-out wheelie bin (WEEE)**, a recycling mark, Bluetooth and USB logos.

**You must render and look.**

```bash
nix-shell -p poppler-utils imagemagick --run '
  pdfimages -png ID-Label-*.pdf out
  magick "$(ls -S out*.png | head -1)" -crop 150x80+435+245 +repage -resize 700% -sharpen 0x1 zoom.png'
```

Same caveat for internal photos: they resolve **large** markings well (a 650 mAh battery label
was legible at 944×708) but a 2 × 2 mm DFN regulator marking was **not** legible even at
2835×2126 upscaled 300%. Say which parts the photos did and did not resolve.

---

## 6. Per-product checklist

1. **Controls.** One positive, one negative, same session, record both status codes.
2. **Grantee code** via company search on the *legal entity* name.
3. **Enumerate the whole grantee** — dump every ID, date and product name to a file.
4. **Match products to IDs by name and date**, not by guessing product codes.
   A missing product is now a real absence, because step 1 proved the method works.
5. **Fetch each filing page**; record frequencies, equipment class, test firm, TCB,
   confidentiality status, and the full exhibit table including withheld rows and release dates.
6. **Download exhibits** with the `.pdf` template. Validate magic bytes (`%PDF-`), not the
   extension.
7. **Render the label and the internal photos and actually look at them.** Record what you could
   and could not resolve.
8. **CE/UKCA:** look for a DoC PDF on the vendor site. If none, say "no published DoC located",
   never "not CE marked" — check the label photograph for the mark itself.
9. **Module vs. device.** If the board carries a pre-certified module, the module's grant may be
   what matters. If the board has a bare SoC and a PCB antenna, the vendor needed their own
   Original Equipment grant — which is why Xteink has one.
10. **Record absences with the controls attached.** An absence without a control is not a finding.

---

## 7. Reading an FCC ID

```
2AN3W  M5CARDPUTERADV
└─┬─┘  └──────┬──────┘
  │           └─ product code — applicant's free choice, unguessable
  └───────────── grantee code — stable per company, the thing to search for
```

Grantee codes beginning with `2` are post-2013 assignments. A hyphen may or may not appear
between the two halves and **is part of the ID**: `2AN3WM5DINMETER` has none,
`2BTR9-X4PRO` does, and the same grantee uses both styles
(`2AN3WM5STAMP-C3` vs `2AN3WM5STAMPS3A`). If a lookup 404s, try it both ways before concluding
absence.

---

## 8. Cross-references

- Scratch, raw data and the full failure log:
  [`scratch/market-and-certification/README.md`](../../scratch/market-and-certification/README.md)
- UA/site access matrix, repo-wide:
  [`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md)
- Vendor documentation-sourcing guides: [`vendors/`](../../vendors/)
- Sibling method guide:
  [`finding-projects-that-use-a-board.md`](finding-projects-that-use-a-board.md)
