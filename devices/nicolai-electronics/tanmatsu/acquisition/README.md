# Acquiring the Tanmatsu artifacts from a clean clone

> **2026-08-24.** Every artifact in this tree came from a pinned git commit or a server-rendered
> documentation page. **Nothing required authentication, payment or manual steps.**

## Verify what is already here

```bash
python3 tools/verify_manifest.py
# 188 files: 188 ok, 0 mismatched, 0 missing
```

Exits non-zero on any mismatch, so it is usable as a CI or post-clone check.

## Re-acquire everything — one command

```bash
tools/fetch_sources.sh archive/scratch/tanmatsu/sources
```

Clones all twelve repositories at their **pinned commits**, enumerates the badge.team Konsool
documentation from `sitemap.xml`, and fetches the solder.party product pages. Idempotent — existing
clones are checked out to the pinned commit rather than re-cloned. ~930 MB.

> **Lesson learned:** the original clones were made under `/tmp` and were destroyed by a system
> cleanup. Fetch into `archive/scratch/<device>/sources` instead, and keep the
> acquisition script **in the repository** so it cannot be lost with the data.

## Re-acquire step by step

### 1. Official repositories (pinned commits)

```bash
for r in tanmatsu-hardware tanmatsu-documentation tanmatsu-mechanical \
         tanmatsu-coprocessor-firmware esp32-component-tanmatsu-coprocessor \
         tanmatsu-launcher tanmatsu-radio esp32-component-tanmatsu-wifi \
         tanmatsu-template app-repository; do
  git clone "https://github.com/Nicolai-Electronics/$r.git"
done
```

Then check out the exact commits recorded in [`../sources.md`](../sources.md) — for example:

```bash
git -C tanmatsu-hardware checkout 640805dd4304f4bfaac24965f8eecf81bec97bf1
```

Full commit list is in `manifest.json` under `sources`.

### 2. Ecosystem repositories

```bash
git clone --depth 1 https://github.com/badgeteam/esp32-component-badge-bsp   # 9037f0e
git clone --depth 1 https://github.com/solderparty/i2c_puppet                # f085518
```

### 3. badge.team documentation (42 pages)

**Enumerate from the sitemap — do not guess paths.** badge.team's URL separator style is
inconsistent (`quickstart`, `expansion_boards`, `pinout/ics`).

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
curl -sSL -A "$UA" https://badge.team/sitemap.xml -o sm.xml
grep -o '<loc>[^<]*</loc>' sm.xml | sed 's/<[^>]*>//g' | grep -i konsool | sort > urls.txt
while read u; do
  n=$(echo "$u" | sed 's|/docs/badges/konsool/||; s|/$||; s|/|_|g'); [ -z "$n" ] && n=index
  curl -sSL -A "$UA" -o "$n.html" "https://badge.team$u"
done < urls.txt
```

### 4. solder.party documentation (7 pages)

The `/docs/` index lists every product, so no sitemap is needed.

```bash
for p in bbq20kbd keyboard-pmod keyboard-featherwing/rev1 keyboard-featherwing/rev2 \
         keebdeck/keyboard keebdeck/basic rp2350-stamp-xl; do
  curl -sSL -A "$UA" -o "$(echo $p|tr / _).html" "https://www.solder.party/docs/$p/"
done
```

## Important: web pages are stored as text, not HTML

The `artifacts/badge-team-docs/` and `artifacts/solder-party-docs/` files are **extracted plain
text**, not the original HTML. This was deliberate — text is diffable and survives site redesigns —
but it means:

- The stored SHA-256 values are of the **extracted text**, not of the served HTML.
- Re-running the fetch will **not** reproduce those hashes unless you use the same extractor.
- Images, tables' visual structure and link targets are partially lost.

If you need faithful copies, re-fetch the HTML directly from the URLs above.

## Reacquisition status

| Source | Status | Notes |
|---|---|---|
| 10 × Nicolai-Electronics repos | `automatic` | Public, pinned commits |
| `badgeteam/esp32-component-badge-bsp` | `automatic` | Public |
| `solderparty/i2c_puppet` | `automatic` | Public, MIT |
| badge.team docs | `automatic` | Public, server-rendered; enumerate via sitemap |
| solder.party docs | `automatic` | Public, server-rendered |

**No source is `blocked` or `lost`.** No rate limiting, bot-blocking or User-Agent substitution was
needed — the browser UA above was applied for consistency, not necessity.

## Licensing — items flagged for review

Recorded in `manifest.json` under `redistribution_review`:

| Licence | Status |
|---|---|
| **CERN-OHL-P** (hardware, mechanical) | Redistribution allowed, attribution required |
| **MIT** (firmware, BSP, i2c_puppet) | Allowed |
| **Apache-2.0** (radio firmware) | Allowed |
| **No licence file** — `tanmatsu-documentation`, `tanmatsu-template`, `app-repository`, `esp32-component-tanmatsu-coprocessor` | ⚠ **FLAGGED.** Quoted and snapshotted for research; wholesale redistribution legally unclear |
| **Web docs** — badge.team, solder.party | ⚠ **FLAGGED.** No stated licence |
| **Branding** | ⚠ Nicolai Electronics / Tanmatsu names, logos and artwork are **all rights reserved** and explicitly excluded from CERN-OHL-P |

The most consequential of these is `tanmatsu-template` — the app template every developer is told to
start from carries **no licence at all**. Worth raising upstream.

## Not retained

| Item | Why | How to get it |
|---|---|---|
| Full repository clones (~490 MB) | Only the useful subset was copied in | Commands above |
| FreeCAD `.FCStd` files (36 MB) | Large; FreeCAD unavailable to inspect them | `tanmatsu-mechanical` repo |
| `tanmatsu.step` / `frontpanel.step` (45 MB) | Large binary CAD | idem |
| `production/tanmatsu.zip` | Not opened — presumed Gerbers | `tanmatsu-hardware` repo |
| Component datasheets | Only product pages cited | Links in each component record |
| Original HTML of web docs | Text extracted instead | Re-fetch per above |
