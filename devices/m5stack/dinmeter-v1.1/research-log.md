# DinMeter v1.1 — research log

The full log — every query, every source class, every negative result, the schematic-parsing
method and its failure modes, and the declared exclusions — is
**[`../dinmeter/research-log.md`](../dinmeter/research-log.md)**. Both revisions were researched
in a single pass on **2026-09-04**.

This page records only what was v1.1-specific.

---

## 1. v1.1-specific discovery

| Query / action | Result |
|---|---|
| `GET https://docs.m5stack.com/en/core/DinMeter_v1.1` | HTTP 200, 142 090 B |
| `GET https://docs.m5stack.com/en/core/DinMeter` | **HTTP 404** — negative control |
| Sitemap filtered for `Din` | **6 URLs only**: `/en/core/M5DinMeter`, `/en/core/DinMeter_v1.1`, 9 Arduino tutorial pages and 1 UiFlow2 page. **There is no separate v1.1 tutorial set** — the v1.1 page links the same `/en/arduino/m5dinmeter/*` pages |
| `GET .../products/m5stack-din-meter-v1-1-with-m5stamps3a.js` | HTTP 200 — SKU, price, launch date |
| `GET .../products/m5stack-din-meter-with-m5stamps3.js` | **HTTP 404** — wrong slug guess |
| `GET .../products/m5stack-din-meter-w-m5stamps3.js` | HTTP 200 — `[EOL]`, out of stock. Slug recovered from a link in `bmorcelli/Launcher`'s README, **not** from M5Stack |
| GitHub repo search for a v1.1-specific project | **none exist.** No repository, board file or fork distinguishes v1.1 from v1.0 |
| `grep -r "StampS3A\|board_M5DinMeter" M5Unified/src` | **no v1.1 or S3A enum.** A negative finding, and the load-bearing evidence for the predicted RGB-LED failure |

## 2. The three findings that came from hashing rather than reading

Each was discovered by `sha256sum` during acquisition, not by comparing documents:

1. **v1.1 schematic ≡ v1.0 schematic.** Two URLs, two filenames, one file (`03ec3353…`).
2. **`DinMeter_v1.1.stl` ≡ `DinMeter.stl`** (`90f04d6a…`).
3. **`Stamp-S3A.stl` ≡ `Stamp-S3.stl`** (`f72c1af2…`), and `m5stack/M5_Hardware` publishes **no
   Stamp-S3A footprint at all**.

Without hashing, all three would have been recorded as "v1.1 documentation obtained". This is
the single strongest argument in the whole pass for hashing every artifact at acquisition time.

## 3. The delta method

Both Stamp schematics were fetched, their Altium `CO`/`PI`/`NL` marker layers parsed with the
same glyph-deduplicating extractor used for the carrier board, and the two designator censuses
diffed:

```
Stamp-S3 v0.2      : 55 designators (54 CO + C26 from visible text only)
Stamp-S3A v0.3.3   : 59 designators
removed (7) : D6, JP1, JP4, M2, R3, R6, R17
added  (11) : C15, C16, C18, C19, C20, C24, C25, L4, L6, L7, U4
common (48)
```

Then each changed IC was read net-by-net (`U2`, `U3`, `U4`/`M2`, `ANT1`, `J1`, `J3`) and the
readings cross-checked against the vendor's two-row comparison table and the DinMeter v1.1 page's
GPIO38 note. Result: [`stamp-s3-to-s3a-delta.md`](stamp-s3-to-s3a-delta.md). Retained diff:
[`components/m5stack/stamp-s3a/artifacts/stamp-s3-vs-s3a-designator-diff.txt`](../../../components/m5stack/stamp-s3a/artifacts/stamp-s3-vs-s3a-designator-diff.txt).

## 4. Searched and found nothing (v1.1-specific)

| Question | Result |
|---|---|
| ST7789P3 datasheet | **not found** anywhere — Sitronix, M5Stack mirrors, general web |
| Stamp-S3A `U4` part number | **not printed on the schematic**; not stated on any page |
| A v1.1-specific schematic, STL, footprint or BOM | **none published** |
| A v1.1-specific library release or board enum | **none** |
| A v1.1 teardown or PCB photograph | **none found** |
| A v1.1-specific community project | **none** |
| An M5Unified issue/PR about the GPIO38 RGB-LED change | **none found** |
| M5Stack forum threads about v1.1 | **inaccessible** — API HTTP 401, HTML is a NodeBB JS shell |

## 5. Exclusions

Same as the shared log: no hardware, no teardown, no RF or electrical measurement, no
regulatory-database search, no video/blog/Chinese-platform search, no distributor price sweep,
and the vendor forum was inaccessible. Additionally: **the Stamp-S3A pin-map JPEG was not
OCR'd**, which is what would settle the rear-FPC numbering question.

→ [`../dinmeter/research-log.md` §9](../dinmeter/research-log.md)
