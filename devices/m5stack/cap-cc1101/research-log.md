# Research log — Cap CC1101 & NFC (U219)

Single pass, **2026-09-04** — **seven days after the product went on sale.** No hardware.

## Why this record exists in the shape it does

The task brief identified the Cap LoRa-1262 as "the newest one, released ~August/September
2026". Checking that claim against `shop.m5stack.com`'s Shopify JSON showed the LoRa Cap
was published **2025-12-30**, and that the product actually published in that window was
**this** board — `published_at 2026-08-28T12:00:54+08:00`, created 72 minutes earlier the
same morning. So the "brand-new" half of the brief resolves to U219, and this record was
given full depth accordingly.

## Sources searched

| Class | Searched? | Notes |
|---|---|---|
| Manufacturer docs | ✅ | Product page + Arduino guide (62 821 B of extracted text) |
| Manufacturer store | ✅ | Product JSON + full 662-product catalogue |
| Manufacturer repositories | ✅ | `org:m5stack cc1101` → **0**; `M5Unit-NFC` walked (230 blobs) |
| Component datasheets | ✅ | CC1101 (TI, via M5Stack mirror), ST25R3916 (ST, via M5Stack — **duplicate detected**) |
| Framework/library | ✅ | RadioLib, M5Unit-NFC |
| Community | ✅ | Reddit; **very thin** — the board is 7 days old |
| Regulatory | ❌ | Declared exclusion |
| Distributors / marketplaces | ❌ | Declared exclusion |
| `community.m5stack.com` | ❌ | Declared exclusion |
| Video | ❌ | The product page's Video section was empty at retrieval |

## Query ledger

| Service | Query | Result |
|---|---|---|
| `docs.m5stack.com/en/cap/Cap_CC1101` | direct | 200, 138 934 B |
| `docs.m5stack.com/en/arduino/projects/cap/cap_cc1101` | direct | 200, 456 766 B |
| `shop.m5stack.com/products/cap-cc1101-nfc-for-cardputer.json` | direct | 200 — **the release date** |
| GitHub search | `org:m5stack cc1101` | **0 repositories** (negative result) |
| GitHub API | `repos/m5stack/M5Unit-NFC/git/trees/main?recursive=1` | 230 blobs; `CapCC1101NFC` located in `src/M5UnitUnifiedNFC.hpp` |
| GitHub API | `repos/m5stack/M5Unit-NFC/commits?per_page=10` | head 2026-06-10 — **library predates the product by 11 weeks** |
| `old.reddit.com/search.json` | `"Cap CC1101"` | 1 substantive thread (the announcement) |
| `old.reddit.com` | `/r/CardPuter/comments/1w0nwti/`, `/1nbe134/` | full comment trees |

## What changed the conclusions

1. **The release-date correction** (above) — this is the new board, not the LoRa Cap.
2. **The band-switch architecture.** Reading sheet 3 showed `CC1101_RF_SW1` never leaves the
   PCB; it comes from the CC1101's own `GDO2`. The vendor's Arduino guide and a vendor
   Reddit comment independently confirm it. That is the board's genuinely novel idea and it
   got its own feature guide.
3. **The NFC interface strap.** Same ST25R3916 as the PaperMono, but **SPI** here vs **I²C**
   there. The existing component record covers everything above the transport, so this
   record documents the delta rather than duplicating 555 lines.
4. **The duplicate datasheet.** The ST25R3916 PDF at `/1229/` is byte-identical to the copy
   already in the repository. Recorded as an extra URL; not stored twice.
5. **The library-before-product finding.** `CapCC1101NFC` existed on 2026-06-10 with the
   README stating *"included in this library for future use"*. Useful because it means the
   driver is not speculative.
6. **The 11-month slip.** A 2025-09-08 owner post quotes M5Stack predicting December 2025.

## Negative results kept

- No M5Stack CC1101 library.
- No certification identifier.
- **No firsthand use report of this board anywhere** — every community mention is
  announcement, ordering intent, or correct-but-theoretical explanation.
- No Bruce/M5Launcher support yet; band switching explicitly noted as still to be
  implemented.

## Stopping criterion

Stopped when the schematic's text layer was exhausted (six remaining gaps all require a
**render**, which this host cannot do without poppler), the vendor's two pages were fully
extracted, and Reddit returned no further threads. **Declared exclusions:** regulatory
databases, marketplaces, `community.m5stack.com`, UiFlow2 zh-cn page, schematic page
renders, remaining product photography.

**Re-search advice:** this record is dated within a week of release. Anyone reading it after
~2026-10 should expect real field evidence to exist and should treat
[`compatibility-and-status.md`](compatibility-and-status.md) as stale.
