# Certification and compliance — cap-cc1101

Compiled **2026-09-11** by the certification/market pass. Method and URL templates: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

> **Evidence status.** Everything here is `executed-success` **retrieval** of public regulatory records. **Nothing was verified against a physical device**, no board was inspected, and no label was read off real hardware. Where a mark is reported as present it was read from a photograph inside an FCC exhibit.

---

## 1. Summary

**FCC: granted.** 1 filing(s) apply directly.

| Regime | Status |
|---|---|
| **FCC (US)** | ✅ `2AN3WM5CAPCC1101` |
| **CE / RED (EU)** | ⚠ no published DoC located; CE mark observed on M5Stack labels (§3) |
| **UKCA** | ⚠ not determined (§3) |
| **SRRC / CCC (CN)** | ⚠ **not searched** — database unreachable (§3) |
| **MIC 技適 (JP)** | ⚠ **not searched** — reachable, not queried (§3) |
| **ISED (CA)** | ⚠ **not searched** — 503 (§3) |

---

## 2. Controls — why the results below mean anything

An absence is only evidence if the method demonstrably finds things that are present. Both
controls were run on **2026-09-11** in the same session, against the same host, with the same tool.

| ID probed | HTTP | Verdict | Role |
|---|---|---|---|
| `2AC7Z-ESPS3WROOM1` | **200** | granted | **positive** — ESP32-S3-WROOM-1 (Espressif), a module known to be certified |
| `2AC7Z-ESPS3WROOM1U` | **200** | granted | **positive** |
| `2AN3WM5CARDPUTER` | **200** | granted | **positive** |
| `2BTR9-XTEINKX4` | **200** | granted | **positive** |
| `2AN3WM5CARDPUTERZERO` | **404** | absent | **negative** — invented, plausible form |
| `2ASYE-T-DISPLAY-K230` | **404** | absent | **negative** — invented, exact LilyGO house style |
| `2AN3WM5CAPLORA868` | **404** | absent | **negative** — invented sibling of a real ID |
| `2AC7Z-ESPZZ9NOTREAL` | **404** | absent | **negative** — invented under a real grantee |
| `2ZZZZNOSUCHGRANTEE` | **404** | absent | **negative** — invented grantee |

**4/4 positive → 200. 5/5 negative → 404.** Raw run: `scratch/market-and-certification/logs/fcc-controls.txt`.

Beyond the ID probes, the whole grantee was enumerated rather than guessed: `2AN3W` yielded
**59** FCC IDs, `2ASYE` **33**, `2AC7Z` **78**, `2BTR9` **5**. A product absent from a complete
grantee listing is absent, not merely un-found.

---

## 2b. The filings

### `2AN3WM5CAPCC1101`

| Field | Value |
|---|---|
| Applicant | M5Stack Technology Co.,Ltd |
| Grantee code | `2AN3W` — registered 2017-10-23, 59 FCC IDs total |
| Final action date | **902.3-923.4 MHz Original Equipment 2026-09-02 433.92 MHz Original Equipment 2026-09-02** |
| Application purpose | Original Equipment |
| Frequency ranges | **902.3-923.4 MHz** |
| Test firm | Dongguan Yaxu (AiT) Technology Limited |
| Long-term confidentiality | Yes |
| Exhibit rows | 17 available, 4 metadata-only |
| Filing page | `https://fccid.io/2AN3WM5CAPCC1101` — HTTP 200, retrieved 2026-09-11 |

**Withheld (confidentiality granted):**

- Block diagram [Block Diagram]
- Schematic [Schematics]
- Operation Description [Operational Description]
- USA-DueDigilenceLetter_V0.1 [Operational Description]

**Exhibits obtained** — US Government public records, redistribution `allowed`. Downloaded 2026-09-11, magic bytes validated (`%PDF-`):

| Exhibit | Bytes | SHA-256 (first 16) |
|---|---|---|
| `External-Photos-External-Photos.pdf` | 4,676,988 | `475348bb11a54fd3…` |
| `ID-Label-Location-Info-FCC-ID-Label.pdf` | 393,120 | `481c0f71a93501f2…` |
| `Internal-Photos-Internal-Photos.pdf` | 1,871,803 | `5ecb27e04b6abed2…` |
| `RF-Exposure-Info-AiTDG-260609002W5_FCC-RF-EXPOSURE-20cm.pdf` | 196,253 | `253c5be1e0ff6fa0…` |
| `Test-Report-AiTDG-260609002W1_Test-Report-315.pdf` | 886,164 | `da6829ba562a367a…` |
| `Users-Manual-User-Manual.pdf` | 547,721 | `86892fcec9338f1c…` |

Held at `scratch/market-and-certification/fcc/2AN3WM5CAPCC1101/` (**unstaged**, 198 MB total for the pass). Reacquire with `https://fccid.io/2AN3WM5CAPCC1101/<Type-Slug>/<Doc-Slug>.pdf` and a `curl` UA — see [the method guide](../../../guides/research/finding-certification-records.md).

---

## 3. Other jurisdictions

| Regime | Result | Evidence |
|---|---|---|
| **EU CE / RED** | ⚠ **No published Declaration of Conformity located.** `shop.m5stack.com/pages/certificate`, `docs.m5stack.com/en/certificate` and `www.lilygo.cc/pages/certification` all **404** (2026-09-11) | CE is a *self-declaration* regime — **there is no database to search**. Absence of a published DoC is not absence of conformity |
| **CE mark on product** | ✅ **Present.** The FCC `ID Label` exhibit photograph for the Cardputer ADV shows a **CE mark**, an **FCC logo**, a **WEEE crossed-bin** and a recycling mark printed on the M5StampS3A module label | Read visually from the rendered exhibit image, not from a text layer — see the trap in §5 of the method guide |
| **UKCA** | ⚠ **Not determined.** No UKCA database exists; no UKCA mark was legible on the labels inspected | — |
| **China SRRC (型号核准)** | ❌ **Not achieved.** `wireless.miit.gov.cn` and `srrccn.org` both **failed to connect** (`000`) on 2026-09-11 | Method failure, **not** an absence finding. Do not read this row as "not SRRC approved" |
| **China CCC** | ⚠ **Not achieved.** `cnca.gov.cn` reachable (200) but the searchable register was not reached | As above |
| **Japan MIC 技適** | ⚠ **Not searched.** `tele.soumu.go.jp/giteki/SearchServlet` reachable (**200**, 2026-09-11) but is form-driven and was not queried | The Cardputer has a JP variant, so this is a **real gap**, not an absence |
| **ISED Canada** | ⚠ **Not achieved.** `sms-sgs.ic.gc.ca` returned **503** on 2026-09-11. No IC number was legible on any label inspected | Retry later |

**Read this table carefully.** Only two rows are findings (`CE mark present`, `no published
DoC`). Every other row records that *the search did not run*, which is a different thing from
a negative result.


---

## 4. What this does **not** establish

- **No hardware was inspected.** The device in front of you may be a different revision than the one the test lab submitted.
- **A grant is not a mark.** A granted FCC ID does not prove the ID is printed on the unit; 47 CFR §2.935 permits an **e-label** in software instead.
- **Absence of a mark is not absence of a grant.** The reverse error was made about Xteink by the 2026-09-04 sweep and is corrected in [`scratch/market-and-certification/xteink-certification-and-pricing.md`](../../../scratch/market-and-certification/xteink-certification-and-pricing.md).
- **The SRRC, CCC, MIC and ISED rows in §3 are not negative results.** Those searches did not run. Treat them as open work.
- **Schematics are withheld** on 26 of 26 filings examined, along with block diagrams and operational descriptions. The FCC is not a route to a schematic for these vendors.

## 5. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| C-1 | FCC Equipment Authorization filings | FCC (via fccid.io mirror) | primary (US Govt record), accessed through a mirror | regulatory record | `https://fccid.io/` | 2026-09-11 | Grant existence, dates, frequencies, exhibits |
| C-2 | Grantee listing, `2AN3W` etc. | FCC / fccid.io | primary via mirror | regulatory record | `https://fccid.io/<grantee>` | 2026-09-11 | Complete enumeration per company |
| C-3 | Control run | this pass | — | executed probe | `scratch/market-and-certification/logs/fcc-controls.txt` | 2026-09-11 | That the method separates present from absent |

⚠ `fccid.io` is a **mirror**, not the FCC. The official endpoints (`apps.fcc.gov`, `www.fcc.gov/oet/ea/fccid`) returned **403 to all five user agents tried** on 2026-09-11, so no independent confirmation against the primary host was possible. Exhibit PDFs are served with FCC document IDs and lab letterheads, which is corroborating but not dispositive.

