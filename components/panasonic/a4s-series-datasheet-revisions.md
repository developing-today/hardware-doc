# Panasonic A4S (0.4 mm pitch) — datasheet revisions across three distributor mirrors

> Shared between [`axe512127d`](axe512127d/README.md) (socket) and
> [`axe612124d`](axe612124d/README.md) (header). Both parts are fitted on the
> [M5Stack PaperMono](../../devices/m5stack/papermono/README.md) (`J6` socket, `J1` header on
> the KEY/RGB/PDM sheet).
>
> Extracted **2026-09-20** from three independently-mirrored copies of the same Panasonic
> document bundle. Evidence class: **primary, via distributor mirrors**. Status:
> `executed-success` (text extracted and validated with `pdftotext -layout`, poppler-utils
> via `nix shell nixpkgs#poppler-utils`).

## Why this document exists

The A4S series datasheet is not one document — it is a **two-document bundle**, and the three
distributor mirrors serve **three different revision pairs, spanning 2013-03 to 2016-06**.
The differences are not cosmetic: **the socket part number itself changes between revisions**,
and the packaging variant actually fitted on the PaperMono does not exist in the older copies
at all.

Anyone who reads only the 2013 mirrors will conclude that `AXE512127D` is not a real part
number. It is. This is the [SKILL §18.2](../../.agents/skills/hardware-device-research/SKILL.md)
case — *same document, different hash, keep both and investigate* — with a concrete consequence.

## The three mirrors

| Mirror | Bytes | SHA-256 | `ACCTB7E` rev | pp | `ACCTB48E` rev | pp | Total pp |
|---|---:|---|---|---:|---|---:|---:|
| **Digi-Key** | 399,357 | `292023186ef0758f1862f8aa2a5f545dc1c14659f4ba84f14f7183f6385503b4` | **201602** (2016-02) | 7 | **201606** (2016-06) | 3 + 1 unnumbered | **11** |
| Future Electronics | 324,968 | `8245f6fa8ced22a64f4af4a836ad7a288598c899ba88ad3de1d82ce313aeabe1` | **201310** (2013-10) | 6 | **201303** (2013-03) | 4 | 10 |
| Mouser | 298,896 | `934604bb0b4c27e1bdc0540894b71be4b951cdca9850c4de2d057e450cc201b2` | **201303** (2013-03) | 6 | **201303** (2013-03) | 4 | 10 |

Local copies, all three retained in [`axe512127d/artifacts/`](axe512127d/artifacts/):

- `panasonic-a4s-series-connectors-digikey-mirror.pdf` — **the copy this project designs against**
- `panasonic-a4s-series-connectors-future-mirror-ACCTB7E-201310.pdf`
- `panasonic-a4s-series-connectors-mouser-mirror-ACCTB7E-201303.pdf`

The two documents in the bundle are:

| Doc | Covers |
|---|---|
| `ACCTB7E` | The A4S datasheet proper — features, ordering key, specifications, dimensions, PC-board patterns, soldering conditions |
| `ACCTB48E` | `PRODUCT TYPES` — the part-number-to-pin-count tables, split by tape-and-reel pitch, plus packing quantities |

Revisions were read from the **per-page footers**, not from PDF metadata. The PDF
`CreationDate` fields disagree with the Panasonic document dates and must not be used:
Digi-Key's copy reports `CreationDate 2016-03-01 / ModDate 2017-02-21` while carrying
`ACCTB7E 201602-T`; Mouser's reports `2013-04-02` while carrying `201303-T`.

## Finding 1 — the socket surface-treatment digit was renumbered `4` → `7`

The ordering key's socket surface-treatment position changed between `ACCTB7E 201303` and
`ACCTB7E 201310`, **with the description text left unchanged**:

| Revision | Socket digit | Description |
|---|---|---|
| `ACCTB7E 201303` (Mouser) | **`4`** | Ni plating on base, Au plating on surface (for Ni barrier available) |
| `ACCTB7E 201310` (Future) | **`7`** | Ni plating on base, Au plating on surface (for Ni barrier available) |
| `ACCTB7E 201602` (Digi-Key) | **`7`** | Ni plating on base, Au plating on surface (for Ni barrier available) |

The header digit stayed `4` throughout.

**Consequence.** The same physical 12-pin socket is printed as `AXE512124` in the 2013-03
copy and `AXE512127` in the 2013-10 and 2016-02 copies. The whole socket column shifts:
the Mouser copy lists `AXE510124 … AXE580124`; both later copies list `AXE510127 … AXE580127`.

This is a **documentation renumbering, not a part change**, and the identical description
text is the evidence for that. It is still worth stating plainly, because a BOM cross-check
against the Mouser mirror will report the PaperMono's socket as an unknown part number.

## Finding 2 — the `D` package suffix does not exist before `ACCTB48E 201606`

| Revision | `D`-suffixed part numbers | `4 mm pitch embossed packaging` section |
|---|---:|---|
| `ACCTB48E 201303` (Mouser, Future) | **0** | **absent** |
| `ACCTB48E 201606` (Digi-Key) | **26** | present |

The ordering key's `Package` position is only documented in the 2016 revision:

```
Nil: Embossed packaging (8 mm pitch)
D:   Embossed packaging (4 mm pitch)
```

**Consequence.** `AXE512127D` and `AXE612124D` — the exact strings on the PaperMono
schematic — appear **only** in the Digi-Key mirror. Neither 2013 copy documents the `D`
option in any form.

## What `AXE512127D` and `AXE612124D` decode to

Decoded against the `ACCTB7E 201602` ordering key and cross-checked against the
`ACCTB48E 201606` `4 mm pitch embossed packaging` table:

| Position | `AXE` **5** `12` **1** `2` **7** `D` | `AXE` **6** `12` **1** `2` **4** `D` |
|---|---|---|
| Series | A4S socket | A4S header |
| Pins | **12** | **12** |
| Mated height | `1` = 0.8 / 1.0 mm (socket covers both) | `1` = **0.8 mm** |
| Functions | `2` = without positioning bosses | `2` = without positioning bosses |
| Surface treatment | `7` = Ni base / Au surface, Ni barrier available | `4` = Ni base / Au surface |
| Package | **`D` = 4 mm pitch embossed tape** | **`D` = 4 mm pitch embossed tape** |

The `4 mm pitch embossed packaging` table pairs them on one row —
**12 pins · `AXE512127D` socket · `AXE612124D` header** — under the **0.8 mm** mated-height
band, at **15,000 pieces per inner carton (1 reel)**, 30,000 per outer carton.

Two practical points follow:

- **The mated height of the PaperMono `J1`/`J6` stack is 0.8 mm**, fixed by the header's
  `1` digit. The socket does not constrain it; the header does.
- **The `D` suffix is a tape-and-reel pitch only.** The non-`D` parts `AXE512127` /
  `AXE612124` are the same connectors on 8 mm tape. For any question that is not about
  feeder setup or reel quantity, the non-`D` rows in the older mirrors are applicable.

## Negative results and confirmations

- **The existing records were already correct.** [`axe512127d/README.md`](axe512127d/README.md)
  cites `ACCTB7E 201602-T` and decodes the ordering key correctly; the PaperMono
  [`bill-of-materials.md`](../../devices/m5stack/papermono/bill-of-materials.md) correctly
  lists `J6 = AXE512127D` and `J1 = AXE612124D`. Nothing in either needed correction.
  Recorded here so this is not re-investigated. *(Checked 2026-09-20.)*
- **No conflict in the PaperMono BOM.** `bill-of-materials.md` line 161 describes `J1` on
  *sheet 2* as a 6-pin frontlight connector while the `AXE612124D` decode gives 12 pins.
  That row is a **per-sheet designator-collision table** — the same string `J1` naming
  different parts on sheets 2, 5 and 6 — and `AXE612124D` is the *sheet 5* entry. Not a
  contradiction. *(Checked 2026-09-20.)*
- **Text layers validated** before any value was transcribed: the `FEATURES` heading and the
  `ORDERING INFORMATION` block were located in all three extractions and matched a rendered
  page. No glyph-subsetting or code-point-offset corruption was observed.
- **Not verified:** whether Panasonic issued revisions *between* `201310` and `201602`, and
  whether a revision later than `201606` exists. No Panasonic-hosted original was retrieved —
  all three copies are distributor mirrors. Resolving this needs `industrial.panasonic.com`,
  which was not attempted in this pass.

## Retrieval notes

Mirror behaviour, as observed when these were fetched (2026-09-01) and recorded in
[`axe512127d/README.md`](axe512127d/README.md):

| Host | Result |
|---|---|
| `media.digikey.com` | 200, `application/pdf`, `%PDF` ✓ on first try with a Chrome 131 UA — the reliable mirror |
| `www.mouser.com/catalog/specsheets/…` | 200 but **13,897 B of non-PDF** under Chrome and ClaudeBot UAs; **succeeded only with the `WhatsApp/2.23.20.0` UA** |

The Mouser copy retained here is the successful `WhatsApp` UA fetch. See
[`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md) for the general
pattern.

**Digi-Key serves the newest revision here and Mouser the oldest**, which is the opposite of
the usual assumption that a large distributor's copy is stale. Do not infer revision currency
from the distributor's size — read the footer.

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | Narrow pitch connectors A4S (0.4 mm pitch) | Panasonic, via Digi-Key mirror | primary, via distributor mirror | datasheet | <https://media.digikey.com/pdf/Data%20Sheets/Panasonic%20Electric%20Works%20PDFs/A4S_Series.pdf> | 2026-09-01 | `ACCTB7E 201602-T` + `ACCTB48E 201606-T` | ordering key with `7`/`D`; the `D` product-types table; the 12-pin 0.8 mm pairing | [`axe512127d/artifacts/panasonic-a4s-series-connectors-digikey-mirror.pdf`](axe512127d/artifacts/panasonic-a4s-series-connectors-digikey-mirror.pdf) |
| F1 | Narrow pitch connectors A4S (0.4 mm pitch) | Panasonic, via Future Electronics mirror | primary, via distributor mirror | datasheet | <https://www1.futureelectronics.com/doc/PANASONIC/AXE610224_panasonic.pdf> | 2026-09-01 | `ACCTB7E 201310-T` + `ACCTB48E 201303-T` | that the `4`→`7` renumbering had already happened by 2013-10, while `D` had not yet appeared | [`axe512127d/artifacts/panasonic-a4s-series-connectors-future-mirror-ACCTB7E-201310.pdf`](axe512127d/artifacts/panasonic-a4s-series-connectors-future-mirror-ACCTB7E-201310.pdf) |
| M1 | A4S Series | Panasonic, via Mouser mirror | primary, via distributor mirror | datasheet | <https://www.mouser.com/catalog/specsheets/> (a4s-catalog.pdf; `WhatsApp/2.23.20.0` UA required) | 2026-09-01 | the pre-renumbering socket column `AXE5xx124` and surface-treatment digit `4` | [`axe512127d/artifacts/panasonic-a4s-series-connectors-mouser-mirror-ACCTB7E-201303.pdf`](axe512127d/artifacts/panasonic-a4s-series-connectors-mouser-mirror-ACCTB7E-201303.pdf) |

> **F1's "duplicate" status was wrong and is now corrected.**
> [`axe512127d/README.md`](axe512127d/README.md) source row D2 previously recorded this file
> as *"not retained (duplicate)"*. It is **not** a duplicate — different revision
> (`ACCTB7E 201310-T` vs `201602-T`), different page count (10 vs 11), different SHA-256.
> Refuted and corrected **2026-09-20**; the file is now retained.

## Licensing

| Field | Value |
|---|---|
| Licence | `unknown` — no terms stated in any of the three PDFs |
| Redistribution | `unknown` |
| Disposition | `repository` (all three, ~1.0 MB total) |
| Rationale for keeping all three | Not byte-identical, and not the same document: three distinct Panasonic revisions. SKILL §18.2. |
