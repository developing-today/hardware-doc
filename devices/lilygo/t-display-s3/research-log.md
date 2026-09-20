# T-Display-S3 — research log

Snapshot pass, **2026-09-07**. Broad-coverage, reproducible; **not** a claim that no other
source exists.

## Date discrepancy — recorded, not silently resolved

The task brief stated "today is 2026-09-04". The host clock reported **2026-09-07 10:23 UTC**,
and LilyGO's Shopify feed independently returned `updated_at: 2026-09-07` on every product.
Two independent sources beat one assertion, so **every retrieval date in this tree is
2026-09-07**. If the brief's date is the correct one, subtract three days uniformly; nothing
here depends on the difference.

## Search ledger

| Service | Query / method | Depth | Date | Outcome |
|---|---|---|---|---|
| GitHub API | `orgs/Xinyuan-LilyGO/repos`, 3 pages ×100, sorted by update | all 254 repos | 09-07 | **the family enumeration.** 60+ display-related repos identified; 17 pinned to commits |
| GitHub API | `repos/…/git/trees/<sha>?recursive=1` on 12 repos | full trees, 84–5 008 entries each | 09-07 | located every schematic, datasheet, firmware and pin header without guessing paths |
| GitHub raw | 60+ individual files at pinned commits | — | 09-07 | all 200 OK; no HTML served under a binary name |
| GitHub API | issues, `state=all`, 6 pages, on 6 repos | 550 issues | 09-07 | T-Display-S3 **318**, AMOLED-Series 123, Long 45, AMOLED 38, Pro 25, AMOLED-1.64 1 |
| GitHub API | 22 individual issue threads with all comments | — | 09-07 | the gotcha corpus. Selection rule: ≥5 comments **or** ≥2 reactions, then filtered for technical content |
| GitHub code search | `repo:esphome/esphome t-display-s3` | 4 hits | 09-07 | **found**: `mipi_spi/models/lilygo.py`, `amoled.py`, `esp32/boards.py` |
| GitHub code search | `repo:arendst/Tasmota lilygo` | 19 hits | 09-07 | Tasmota has LilyGO material but no T-Display-S3 board file; support is via a runtime template |
| GitHub code search | `org:meshtastic tdisplay` | 247 hits | 09-07 | **negative result**: no T-Display-S3 variant. Expected — no LoRa |
| GitHub code search | `repo:wled/WLED lilygo` | 10 hits | 09-07 | **negative result**: only a `TTGO-T-Display` usermod for the ESP32 predecessor |
| GitHub code search | `repo:russhughes/st7789s3_mpy t-display` | 7 hits | 09-07 | MicroPython driver confirmed, with this board's `tft_config.py` |
| LilyGO store | `collections/all/products.json`, 6 pages | 214 products | 09-07 | dated prices, SKUs, stock, `published_at`, **the V1.0/V2.0 concurrency finding** |
| old.reddit.com | `search.json` × 4 query shapes, `t=all` | 25 results each | 09-07 | 27 family-relevant posts; 2 threads read in full |
| Reddit | `r/esp32`, `r/arduino`, `r/LilyGO`, `r/Esphome`, `r/esp32projects`, `r/cyberDeck` | via search | 09-07 | see [`community.md`](community.md) |
| Local | SHA-256 + size of every retained artifact | 30 files | 09-07 | **found G1** (byte-identical firmware pair) |
| Local | ESP app-descriptor + partition-table decode, 6 images | — | 09-07 | Arduino-core dating; the 8 MB/16 MB layout split |
| Local | PDF text extraction, 8 schematics | — | 09-07 | designator/part census for 7 boards; **T4-S3 needed a second extractor** (Type0/Identity-H) |

## What was deliberately not done

- **Net-level schematic tracing.** Blocked on poppler; see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) K1.
  This is the largest single quality gap in the record and the cheapest to close.
- **Marketplace price sampling** (AliExpress, Amazon, Banggood). Only LilyGO's own store was
  sampled. K8.
- **Regulatory databases** (FCC ID, CE DoC). Not searched.
- **Chinese-language sources** beyond the Chinese datasheets and READMEs already in the repos.
  Bilibili, Zhihu and CSDN were not searched; recorded as a deliberate exclusion.
- **YouTube.** LilyGO links two of their own videos from the README; no independent video was
  catalogued.
- **Hardware.** None available.

## Dead ends and corrections

| Attempt | What happened |
|---|---|
| `gh api repos/Xinyuan-LilyGO/T-Display-S2` | 404. The repo is `LilyGo-T-Display-S2` — LilyGO's naming is inconsistent between repo and product |
| First PDF extractor read `/Contents` only | Returned 403 pin markers and zero labels. Altium puts the sheet in a Form XObject |
| Second attempt read `Tj`/`TJ` per line | Shredded every label into single characters. Fixed by grouping on `BT…ET` |
| T4-S3 schematic returned nothing | Uses Type0/Identity-H subset fonts; needed a `/ToUnicode` CMap decoder |
| CO5300 datasheet text looked readable but wrong | **Uniform +0x1D code-point offset.** Two independent extraction routes both produced garbage that decodes to the same answer. Exactly the trap the skill warns about; recorded in the vendor guide |
| Assumed the charger was SY6970 (it is, on four other boards) | **Wrong for this board.** The schematic says TP4065. Corrected before it reached any record |
| Assumed `U6` = flash from a partial text join | **Wrong.** `U3` is the W25Q128JV; `U6` is the charger. Corrected by re-reading the joined strings |

That last pair is worth keeping: both were candidate readings promoted too early, caught by
re-reading the primary evidence. Neither reached a component record.

## Stopping criterion

Two consecutive broad passes over the issue trackers and Reddit produced only duplicates of
findings already recorded (GPIO15, `USB CDC On Boot`, `User_Setup_Select.h`, battery ADC).
Remaining unexplored sources require **hardware** (K4, K5), **a package manager** (K1–K3), or
**marketplace sampling** (K8). The record stops there and says so.
