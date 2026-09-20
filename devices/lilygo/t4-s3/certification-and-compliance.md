# Certification and compliance — t4-s3

Compiled **2026-09-11** by the certification/market pass. Method and URL templates: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

> **Evidence status.** Everything here is `executed-success` **retrieval** of public regulatory records. **Nothing was verified against a physical device**, no board was inspected, and no label was read off real hardware. Where a mark is reported as present it was read from a photograph inside an FCC exhibit.

---

## 1. Summary

**FCC: granted.** 1 filing(s) apply directly.

| Regime | Status |
|---|---|
| **FCC (US)** | ✅ `2ASYE-T4-S3-241` |
| **CE / RED (EU)** | ⚠ no published DoC located; CE mark observed on M5Stack labels (§3) |
| **UKCA** | ⚠ not determined (§3) |
| **SRRC / CCC (CN)** | ⚠ **not searched** — database unreachable (§3) |
| **MIC 技適 (JP)** | ⚠ **not searched** — reachable, not queried (§3) |
| **ISED (CA)** | ⚠ **not searched** — 503 (§3) |

**Supporting / related grants:** `2AC7Z-ESPS3WROOM1`.

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

### `2ASYE-T4-S3-241`

| Field | Value |
|---|---|
| Applicant | Shenzhen Xin Yuan Electronic Technology Co., Ltd. (LilyGO) |
| Grantee code | `2ASYE` — registered 2019-04-05, 33 FCC IDs total |
| Final action date | **2402-2480 MHz Original Equipment 2024-02-27** |
| Application purpose | Final Action Date 2402-2480 MHz Original Equipment 2024-02-27 |
| Frequency ranges | **2402-2480 MHz** (BLE), **2412-2462 MHz** (Wi-Fi 2.4 GHz, US channels 1–11) |
| Test firm | CHINA CERTIFICATION ICT CO., LTD (DONGGUAN) |
| Long-term confidentiality | Yes |
| Exhibit rows | 17 available, 3 metadata-only |
| Filing page | `https://fccid.io/2ASYE-T4-S3-241` — HTTP 200, retrieved 2026-09-11 |

**Withheld (confidentiality granted):**

- Block Diagram [Block Diagram]
- Schematics [Schematics]
- Circuit Description [Operational Description]

**Exhibits obtained** — US Government public records, redistribution `allowed`. Downloaded 2026-09-11, magic bytes validated (`%PDF-`):

| Exhibit | Bytes | SHA-256 (first 16) |
|---|---|---|
| `External-Photos-External-Photos.pdf` | 765,158 | `18969bc229faadde…` |
| `ID-Label-Location-Info-Label-Label-Location.pdf` | 370,771 | `7fcd4d856c5a0859…` |
| `Internal-Photos-Internal-Photos.pdf` | 983,085 | `3dbcb6171dd1904e…` |
| `RF-Exposure-Info-RF-Exposure---BLE.pdf` | 146,101 | `dc70b64ee5e41734…` |
| `RF-Exposure-Info-RF-Exposure---WiFi.pdf` | 146,127 | `96c6adb398c1ccce…` |
| `Test-Report-Antenna-Specification.pdf` | 1,174,923 | `a1300af9d0563dac…` |
| `Users-Manual-User-Manual.pdf` | 1,308,927 | `392e0deb78d4e31d…` |

Held at `scratch/market-and-certification/fcc/2ASYE-T4-S3-241/` (**unstaged**, 198 MB total for the pass). Reacquire with `https://fccid.io/2ASYE-T4-S3-241/<Type-Slug>/<Doc-Slug>.pdf` and a `curl` UA — see [the method guide](../../../guides/research/finding-certification-records.md).

### `2AC7Z-ESPS3WROOM1`

| Field | Value |
|---|---|
| Applicant | ESPRESSIF SYSTEMS (SHANGHAI) CO., LTD |
| Grantee code | `2AC7Z` — registered 2014-09-15, 78 FCC IDs total |
| Final action date | **2026-02-27** |
| Application purpose | Class II permissive change or modification of presently authorized equipment |
| Frequency ranges | **2402-2480 MHz** (BLE), **2412-2462 MHz** (Wi-Fi 2.4 GHz, US channels 1–11) |
| Test firm | SGS-CSTC Standards Technical Services Co., Ltd. |
| Long-term confidentiality | Yes |
| Exhibit rows | 57 available, 11 metadata-only |
| Filing page | `https://fccid.io/2AC7Z-ESPS3WROOM1` — HTTP 200, retrieved 2026-09-11 |

**Withheld (confidentiality granted):**

- Block Diagram [Block Diagram]
- Block diagram [Block Diagram]
- Schematic [Schematics]
- Schematics [Schematics]
- Operation description [Operational Description]
- Operational Description [Operational Description]
- Parts list [Parts List/Tune Up Info]
- Tune up [Parts List/Tune Up Info]
- Tune up [Parts List/Tune Up Info]
- Tune up [Parts List/Tune Up Info]
- Tune up procedure [Parts List/Tune Up Info]

**Exhibits obtained** — US Government public records, redistribution `allowed`. Downloaded 2026-09-11, magic bytes validated (`%PDF-`):

| Exhibit | Bytes | SHA-256 (first 16) |
|---|---|---|
| `External-Photos-External-Photo.pdf` | 1,367,037 | `a0104b88a862efd5…` |
| `External-Photos-External-Photos.pdf` | 1,275,356 | `8fe953474e9707bc…` |
| `External-Photos-External-photos.pdf` | 332,733 | `b04d392ae5298711…` |
| `ID-Label-Location-Info-Label-location.pdf` | 30,758 | `68e843105466c162…` |
| `ID-Label-Location-Info-Label.pdf` | 44,224 | `081ac1c0f3292f1b…` |
| `ID-Label-Location-Info-Lable-and-location.pdf` | 1,437,286 | `0a57b90982013049…` |
| `Internal-Photos-Internal-Photo.pdf` | 3,636,909 | `318d8c6c95232515…` |
| `Internal-Photos-Internal-photos.pdf` | 338,977 | `1f60246b57db6172…` |
| `RF-Exposure-Info-RF-Exposure.pdf` | 499,298 | `b1ae557e1e78bbfa…` |
| `RF-Exposure-Info-SAR-Report-A.pdf` | 845,988 | `54f4972a02877d9b…` |
| `RF-Exposure-Info-SAR-Report-B.pdf` | 850,218 | `62b4f82db50809aa…` |
| `RF-Exposure-Info-SAR-Report-C1.pdf` | 5,908,102 | `8fbf6c55dc6a0248…` |
| `RF-Exposure-Info-SAR-Report-C2.pdf` | 3,930,042 | `4c6ed64c435d4f04…` |
| `RF-Exposure-Info-SAR-Report-D.pdf` | 3,974,985 | `04798068d0a5ee3b…` |
| `RF-Exposure-Info-SAR-Report.pdf` | 1,936,491 | `60f7208dd54ccff8…` |
| `Test-Report-Antenna-specification.pdf` | 1,996,381 | `da8da91adaa5b481…` |
| `Users-Manual-User-Manual.pdf` | 2,603,588 | `3e493b8b9ea24f00…` |
| `Users-Manual-User-manual.pdf` | 886,672 | `f8d1d246c0c849a6…` |

Held at `scratch/market-and-certification/fcc/2AC7Z-ESPS3WROOM1/` (**unstaged**, 198 MB total for the pass). Reacquire with `https://fccid.io/2AC7Z-ESPS3WROOM1/<Type-Slug>/<Doc-Slug>.pdf` and a `curl` UA — see [the method guide](../../../guides/research/finding-certification-records.md).

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

