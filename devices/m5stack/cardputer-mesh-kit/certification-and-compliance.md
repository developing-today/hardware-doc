# Certification and compliance — cardputer-mesh-kit

Compiled **2026-09-11** by the certification/market pass. Method and URL templates: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

> **Evidence status.** Everything here is `executed-success` **retrieval** of public regulatory records. **Nothing was verified against a physical device**, no board was inspected, and no label was read off real hardware. Where a mark is reported as present it was read from a photograph inside an FCC exhibit.

---

## 1. Summary

**FCC: no grant found.** See §2 for the controls that make this a real absence, and §4 for what it does and does not imply.

A retail bundle, not a distinct radio product. The two radio-bearing parts are separately granted; a bundle does not require its own authorisation.

| Regime | Status |
|---|---|
| **FCC (US)** | ❌ **no grant found** (controlled — §2) |
| **CE / RED (EU)** | ⚠ no published DoC located; CE mark observed on M5Stack labels (§3) |
| **UKCA** | ⚠ not determined (§3) |
| **SRRC / CCC (CN)** | ⚠ **not searched** — database unreachable (§3) |
| **MIC 技適 (JP)** | ⚠ **not searched** — reachable, not queried (§3) |
| **ISED (CA)** | ⚠ **not searched** — 503 (§3) |

**Supporting / related grants:** `2AN3WM5CARDPUTERADV`, `2AN3WM5CAPLORA1262`.

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

### `2AN3WM5CARDPUTERADV`

| Field | Value |
|---|---|
| Applicant | M5Stack Technology Co.,Ltd |
| Grantee code | `2AN3W` — registered 2017-10-23, 59 FCC IDs total |
| Final action date | **2412-2462 MHz Original Equipment 2025-11-19** |
| Application purpose | Final Action Date 2412-2462 MHz Original Equipment 2025-11-19 |
| Frequency ranges | **2402-2480 MHz** (BLE), **2412-2462 MHz** (Wi-Fi 2.4 GHz, US channels 1–11) |
| Test firm | Dongguan Yaxu (AiT) Technology Limited |
| Long-term confidentiality | Yes |
| Exhibit rows | 16 available, 4 metadata-only |
| Filing page | `https://fccid.io/2AN3WM5CARDPUTERADV` — HTTP 200, retrieved 2026-09-11 |

**Withheld (confidentiality granted):**

- Block Diagram [Block Diagram]
- Schematic [Schematics]
- Operation Description [Operational Description]
- USA-DueDigilenceLetter_V0.1 [Operational Description]

**Exhibits obtained** — US Government public records, redistribution `allowed`. Downloaded 2026-09-11, magic bytes validated (`%PDF-`):

| Exhibit | Bytes | SHA-256 (first 16) |
|---|---|---|
| `External-Photos-External-Photos.pdf` | 1,041,781 | `b6e8389cbab5335b…` |
| `ID-Label-Location-Info-FCC-ID-Label.pdf` | 184,122 | `38b3c9554c31c2df…` |
| `Internal-Photos-Internal-Photos.pdf` | 1,848,880 | `b7b25570be4a4fb5…` |
| `RF-Exposure-Info-AiTDG-251013004W3_FCC-RF-EXPOSURE-0cm.pdf` | 258,022 | `f63d066218178f0e…` |
| `Test-Report-AiTDG-251013004W1-FCC-BLE-test-report.pdf` | 987,894 | `5023c54591ee8a5f…` |
| `Users-Manual-User-Manual.pdf` | 390,005 | `2e7ea0b53e452386…` |

Filed under this record's `artifacts/certification/` — ID-label and internal-photo exhibits retained in the repository, the rest archived with `.ARCHIVED.md` placeholders. The scratch copies at `scratch/market-and-certification/fcc/2AN3WM5CARDPUTERADV/` were **consolidated 2026-09-20** after every exhibit was re-hashed and matched byte-for-byte against its filed copy; only `_filing.html` remains there. Reacquire from upstream with `https://fccid.io/2AN3WM5CARDPUTERADV/<Type-Slug>/<Doc-Slug>.pdf` and a `curl` UA — see [the method guide](../../../guides/research/finding-certification-records.md).

### `2AN3WM5CAPLORA1262`

| Field | Value |
|---|---|
| Applicant | M5Stack Technology Co.,Ltd |
| Grantee code | `2AN3W` — registered 2017-10-23, 59 FCC IDs total |
| Final action date | **903-914.9 MHz Original Equipment 2026-02-12** |
| Application purpose | Final Action Date 903-914.9 MHz Original Equipment 2026-02-12 |
| Frequency ranges | **903-914.9 MHz** |
| Test firm | Shenzhen Accurate Technology Co., Ltd. |
| Long-term confidentiality | Yes |
| Exhibit rows | 14 available, 3 metadata-only |
| Filing page | `https://fccid.io/2AN3WM5CAPLORA1262` — HTTP 200, retrieved 2026-09-11 |

**Withheld (confidentiality granted):**

- Block Diagram [Block Diagram]
- Schematics [Schematics]
- Operation Description [Operational Description]

**Exhibits obtained** — US Government public records, redistribution `allowed`. Downloaded 2026-09-11, magic bytes validated (`%PDF-`):

| Exhibit | Bytes | SHA-256 (first 16) |
|---|---|---|
| `External-Photos-External-Photos.pdf` | 767,323 | `dca8f216a5c65942…` |
| `ID-Label-Location-Info-Label-and-Label-Location.pdf` | 134,335 | `e3963b8a5baed487…` |
| `Internal-Photos-Internal-Photos.pdf` | 809,213 | `61f89fc08fde8a09…` |
| `RF-Exposure-Info-RF-Exposure-Information.pdf` | 324,207 | `ac8a66ce38b09480…` |
| `Test-Report-Antenna-Specification.pdf` | 592,270 | `da669cafd28d9fd1…` |
| `Users-Manual-User-Manual.pdf` | 765,439 | `fb81cff4fb9a5d09…` |

Filed under this record's `artifacts/certification/` — ID-label and internal-photo exhibits retained in the repository, the rest archived with `.ARCHIVED.md` placeholders. The scratch copies at `scratch/market-and-certification/fcc/2AN3WM5CAPLORA1262/` were **consolidated 2026-09-20** after every exhibit was re-hashed and matched byte-for-byte against its filed copy; only `_filing.html` remains there. Reacquire from upstream with `https://fccid.io/2AN3WM5CAPLORA1262/<Type-Slug>/<Doc-Slug>.pdf` and a `curl` UA — see [the method guide](../../../guides/research/finding-certification-records.md).

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
- **Absence of a mark is not absence of a grant.** The reverse error was made about Xteink by the 2026-09-04 sweep and is corrected in [`archive/guides/research/artifacts/certification-and-market-2026-09-11/xteink-certification-and-pricing.md`](../../../archive/guides/research/artifacts/certification-and-market-2026-09-11/xteink-certification-and-pricing.md).
- **The SRRC, CCC, MIC and ISED rows in §3 are not negative results.** Those searches did not run. Treat them as open work.
- **Schematics are withheld** on 26 of 26 filings examined, along with block diagrams and operational descriptions. The FCC is not a route to a schematic for these vendors.

## 5. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| C-1 | FCC Equipment Authorization filings | FCC (via fccid.io mirror) | primary (US Govt record), accessed through a mirror | regulatory record | `https://fccid.io/` | 2026-09-11 | Grant existence, dates, frequencies, exhibits |
| C-2 | Grantee listing, `2AN3W` etc. | FCC / fccid.io | primary via mirror | regulatory record | `https://fccid.io/<grantee>` | 2026-09-11 | Complete enumeration per company |
| C-3 | Control run | this pass | — | executed probe | `scratch/market-and-certification/logs/fcc-controls.txt` | 2026-09-11 | That the method separates present from absent |

⚠ `fccid.io` is a **mirror**, not the FCC. The official endpoints (`apps.fcc.gov`, `www.fcc.gov/oet/ea/fccid`) returned **403 to all five user agents tried** on 2026-09-11, so no independent confirmation against the primary host was possible. Exhibit PDFs are served with FCC document IDs and lab letterheads, which is corroborating but not dispositive.

