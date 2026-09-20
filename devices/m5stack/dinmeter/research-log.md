# DinMeter — research log

**Snapshot date: 2026-09-04.** Single research pass, no hardware in hand. Covers K134 and
K134-V11 together. Every query is recorded, including the ones that returned nothing — those are
the ones that stop the next agent repeating the work.

---

## 1. Source classes searched

| Class | Searched? | Depth |
|---|---|---|
| Manufacturer product pages / docs | ✔ | Both product pages, both Stamp pages, 9 Arduino tutorial pages, 1 UiFlow2 page, the full 5 703-URL sitemap |
| Manufacturer schematics / CAD / downloads | ✔ | 3 schematics, 2 dimension drawings, 4 STL/STEP/footprint files, 7 datasheet mirrors |
| Manufacturer repositories | ✔ | `M5DinMeter`, `M5DinMeter-UserDemo`, `M5Unified`, `M5GFX`, `M5_Hardware`, `uiflow-micropython` |
| Component-manufacturer pages / datasheets | ✔ partial | 4 obtained; **4 not found** (ME3116AM6G, SY7088, BL8075, SGM2578) |
| Standards / certification databases | ✘ | **Declared exclusion.** No FCC/CE search was run |
| Framework / SDK / registry docs | ✔ | M5Unified, M5GFX, `esp-board-manager`, PlatformIO registry (via project files), MicroPython |
| Authorized distributors / mirrors | ✔ partial | M5Stack's own store only; no Mouser/DigiKey/Aliexpress price sweep |
| Community repositories | ✔ | GitHub repo + code search, several query forms |
| Forums | ⚠ **blocked** | `community.m5stack.com` returns HTTP 401 on its API and a JS shell on HTML |
| Reddit | ✔ | 4 query forms, ~200 results inspected |
| Blogs / reviews / videos | ✘ | **Declared exclusion** — not systematically searched |
| Chinese-language platforms | ✘ | **Declared exclusion** — Bilibili, CSDN, Taobao not searched |
| Web archives | ✔ minimal | No captures needed; nothing was dead |

---

## 2. Vendor documentation — URL discovery

The `/en/products` index is a JavaScript shell and contains **no product links** in its served
HTML (565 615 B fetched, 8 path matches, all generic). **The sitemap is the only way to
enumerate.**

| Query | Result |
|---|---|
| `GET https://docs.m5stack.com/en/core/DinMeter` | **HTTP 404** ← negative control; the obvious guess is wrong |
| `GET https://docs.m5stack.com/en/core/M5DinMeter` | HTTP 200, 139 501 B ← the v1.0 page |
| `GET https://docs.m5stack.com/en/core/DinMeter_v1.1` | HTTP 200, 142 090 B |
| `GET https://docs.m5stack.com/en/stamp/StampS3` | **HTTP 404** ← negative control; Stamp pages live under `/en/core/`, not `/en/stamp/` |
| `GET https://docs.m5stack.com/en/stamp/{Stamp-S3A,M5StampS3,stamps3,StampS3A}` | **HTTP 404** ×4 |
| `GET https://docs.m5stack.com/en/core/StampS3` | HTTP 200 |
| `GET https://docs.m5stack.com/sitemap.xml` | HTTP 200, 499 000 B, **5 703 URLs** |
| `GET https://docs.m5stack.com/en/sitemap.xml` | **HTTP 404** |
| `GET https://docs.m5stack.com/sitemap_index.xml` | **HTTP 404** |

Sitemap filtered for `Stamp` → 73 URLs, for `Din` → **6** (only `M5DinMeter` and `DinMeter_v1.1`
under `/en/core/`, plus 9 `/en/arduino/m5dinmeter/*` and 1 `/en/uiflow2/m5dinmeter/program`).

All 20 subsequently fetched doc pages returned HTTP 200. No fallback User-Agent was needed for
any `m5stack.com` host — the Chrome-131 UA was used throughout as the standing convention.

## 3. Artifact acquisition

19 files fetched, **all HTTP 200**, all validated by magic bytes. No failed downloads, no HTML
served under a `.pdf` extension. Full hash/size table:
[`acquisition/manifest.json`](acquisition/manifest.json).

**Two byte-identity discoveries made during acquisition** (both found by hashing, not by
reading):

1. `.../500/DIN_Meter_v1.0.pdf` and `.../1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf`
   → same SHA-256 `03ec3353…`. Different hosts paths, different filenames, same bytes.
2. `Stamp-S3.stl` and `Stamp-S3A.stl`, and `DinMeter.stl` and `DinMeter_v1.1.stl` → identical
   within each pair.

And one **deduplication against the existing repository**: the ESP32-S3 datasheet fetched from
`m5stack-doc…/472/esp32-s3_datasheet_en.pdf` has SHA-256 `b6db403d…`, matching
`components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet-v2.0-m5stack-mirror.pdf` already
held. Not re-added; the extra URL was recorded instead.

## 4. Schematic analysis

No `pdftotext`/poppler, no `pypdf`, no `pymupdf` on this host. `pymupdf` installed but failed to
import (`libstdc++.so.6` missing). **`pdfminer.six 20260107` in a `uv` venv worked.**

A poppler-`-bbox`-compatible XML emitter was written (`/tmp/opencode/pdf_bbox.py`) and a
DinMeter-specific parser retained at
[`artifacts/schematic/parse_dinmeter_sch.py`](artifacts/schematic/parse_dinmeter_sch.py).

**One real trap, recorded because it produces plausible-looking wrong output:** Altium draws its
marker layer **twice** at identical coordinates. Without glyph deduplication the two copies
interleave, so `PIJ10101` extracts as `PPIIJJ110011` — human-legible-ish, and completely wrong.
The first parse pass produced exactly this and was discarded. Dedupe key: rounded
`(x0, y0, x1, y1, char)`.

**Text-layer validation before transcription:** the page-frame zone letters `A`–`D` and numbers
`1`–`4` land at the expected coordinates, and `TP4057`, `SY7088`, `BL8075CB5TR33`,
`ME3116AM6G`, `STAMP-S3-SMD`, `RTC8563`, `32.768KHz ±20ppm 12.5pF` all render as legible strings
in the right places. 84 of 85 marker-derived designators match visible designator text.

**Completeness accounting:** 85 `CO`, 238 `PI`, 25 `NL`, 553 visible text runs. ~260 `PI` markers
expected for 84 parts ⇒ ~20 not recovered, caused by the negative-lookbehind rule that prevents
`GPIO0` parsing as a `PI` marker. All `M1` (31), `J3`, `J4`, `J5`, `FPC1`, `U5`, `U6` pads were
recovered, so no published table rests on a missing marker.

**Absence proven, not assumed:** searched for `COS1`, `COR20`, `COY1`, `COQ2`, `COL2`, `COL3`,
`COR21`, `COR22`, `COS2`, `COS3`, `COU8`, `COD14`, `COJ6` in both single and double-struck glyph
forms — **zero hits for all**. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §2.

## 5. GitHub

Authenticated via `gh auth token` throughout (`api.github.com` limits per identity; no
User-Agent helps).

| Query | Endpoint | Result |
|---|---|---|
| `DinMeter` | repo search | 5 |
| `M5DinMeter` | repo search | 6 |
| `din meter m5stack` | repo search | 2 |
| `DinMeter in:name,description,readme` | repo search, 50/page | **19** ← the productive form |
| `DinMeter in:file language:yaml` | code search | 94 (mostly false positives on unrelated YAML) |
| `din_meter` | code search | 109 (dominated by `whatnick/din_meter_atm90e26`, an unrelated ATM90E26 energy meter) |
| `M5DinMeter extension:h` | code search | 9 files / 6 repos |
| `repo:esphome/esphome dinmeter` | code search | **0** |
| `repo:arendst/Tasmota dinmeter` | code search | **0** |
| `repo:meshtastic/firmware dinmeter` | code search | **0** |
| `repo:meshtastic/firmware din_meter` | code search | **0** |
| `repo:pr3y/Bruce dinmeter` | code search | **0** ← support is in `bmorcelli/Launcher`, not Bruce upstream |
| `repo:bmorcelli/Launcher dinmeter` | code search | **6** ← the productive one |

**Naming traps found:** `din_meter` collides with `whatnick/din_meter_atm90e26` (an unrelated
KiCad energy-meter project) and with EV-charging DIN 70121 code (`din_msgDefDatatypes.c` in
EVerest/SmartEVSE). `DinMeter` also matches ski-binding "DIN meter" discussions on Reddit.

## 6. Reddit

`old.reddit.com/search.json` with UA `WhatsApp/2.23.20.0` — HTTP 200 on every request, where
`www.reddit.com` is documented in this repository as returning 403.

| Query | Results returned | Relevant |
|---|---:|---:|
| `DinMeter` | 50 | 1 |
| `Din Meter M5Stack` | 50 | 1 (same post) |
| `M5Stack knob DIN` | ~25 | 0 |
| `subreddit:M5Stack dinmeter` | 7 | 1 (same post) |
| `subreddit:esp32 dinmeter` | **0** | 0 |
| `din meter stamps3` | 50 | 0 |

**One relevant post in the entire index** — the official 2026-01-30 weekly-products
announcement. Recorded in [`projects-and-community.md`](projects-and-community.md) §4.

## 7. M5Stack community forum — blocked

| Attempt | Result |
|---|---|
| `https://community.m5stack.com/api/search?term=dinmeter&in=titlesposts` | **HTTP 401** — `{"status":{"code":"not-authorised",…}}` |
| `https://community.m5stack.com/search?term=dinmeter&in=titlesposts` (Chrome-131 UA) | HTTP 200, 16 986 B — NodeBB **JS shell**, no results in served HTML |

**No forum thread could be cited.** Largest single gap in this record. Would need an
authenticated session or a search-engine index.

## 8. Component datasheets — four failures

| Part | Where searched | Result |
|---|---|---|
| ME3116AM6G | vendor pages, aggregators, general web | **not found** |
| SY7088 | as above | **not found** |
| BL8075(CB5TR33) | as above | **not found** |
| SGM2578 | as above | **not found** |
| Stamp-S3A `U4` | schematic (no part text), vendor pages | **no part number exists to search for** |
| ST7789P3 | Sitronix, M5Stack mirrors, general web | **not found** — M5Stack removed the display datasheet link on the v1.1 page rather than replacing it |

All five are recorded as `unidentified` or schematic-only component records rather than guessed.

## 9. Explicit exclusions

Declared so the coverage claim is honest:

- **No hardware.** Nothing was flashed, measured, probed or photographed.
- **No teardown.** No PCB photograph, no chip marking confirmed visually. Every part number
  rests on schematic value text.
- **No RF measurement.** The Stamp-S3A antenna claim is neither confirmed nor refuted.
- **No FCC/CE/regulatory database search.**
- **No video, blog or review search.**
- **No Chinese-language platform search.**
- **No marketplace price sweep** beyond `shop.m5stack.com`.
- **Forum inaccessible** (§7).
- **Pin-map JPEGs not OCR'd** — which is what would settle the Grove wire-colour conflict.

## 10. Stopping criterion

Two consecutive broad passes over GitHub and Reddit returned only duplicates and the same
homonym noise (`din_meter_atm90e26`, DIN 70121, ski bindings). The remaining unresolved items
all require either **hardware in hand** (teardown, meter, RF), **an authenticated forum
session**, or **documents the manufacturers have not published**. Continuing the same search
classes would not have produced new qualifying sources.

This is a **reproducible broad-coverage snapshot dated 2026-09-04**, not a claim that no other
resource exists.
