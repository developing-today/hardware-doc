# Research log — Cap LoRa-1262 (U214)

Single pass, **2026-09-04**. Agent had no hardware. Search cutoff = the retrieval date.

## Source classes searched

| Class | Searched? | Depth |
|---|---|---|
| Manufacturer product pages / docs | ✅ | 10 pages fetched; link sets fully enumerated |
| Manufacturer store | ✅ | per-product JSON + full catalogue (662 products, 3 pages to exhaustion) |
| Manufacturer repositories | ✅ | `org:m5stack` searched for `lora`, `cc1101`, `cap`, `1262`; org repo listing walked |
| Component-manufacturer datasheets | ✅ (via M5Stack mirrors) | Semtech, TI, ST, ZhongKeWei/CASIC |
| Standards / regulatory databases | ⚠ partial | M5Stack's own certification index only (negative). **No FCC/CE database query was run** — declared exclusion |
| Framework / SDK docs | ✅ | Meshtastic repo, RadioLib, M5Unit-NFC, TinyGPSPlus |
| Distributors / mirrors | ❌ | Not searched. AliExpress/Amazon pricing not gathered — declared exclusion |
| Community forums | ✅ | Reddit (6 query families, 217 unique posts, 12 full comment trees) |
| M5Stack community forum (`community.m5stack.com`) | ❌ | **Not searched** — declared exclusion |
| Video | ⚠ | Product video URL captured, **not watched** |
| Archives (Wayback) | ❌ | Not needed; every live URL returned 200 |

## Query ledger

| Service | Query | Filters | Results | Outcome |
|---|---|---|---|---|
| `docs.m5stack.com` | direct slugs `en/cap/Cap_LoRa-1262`, `Cap_CC1101`, `Cap_LoRa868`, `en/core/Cardputer_Mesh_Kit`, `Stamp_C6LoRa`, `Cardputer`, `en/module/lora868` | — | 7 × HTTP 200 | all useful |
| `docs.m5stack.com` | `en/core/CardputerAdv`, `en/core/CardputerZero`, `en/unit/lora868`, `en/unit/Unit-LoRaWAN868`, `en/arduino/projects/cap/cap_lora1262` | — | **5 × HTTP 404** (4 162 B soft pages) | slugs wrong; recorded so they are not retried |
| `shop.m5stack.com` | `/products/<handle>.json` × 11 | — | 200 | **release dates** |
| `shop.m5stack.com` | `/collections/all/products.json?limit=250&page=1..4` | — | 662 products; page 4 empty | full catalogue timeline |
| GitHub search | `org:m5stack lora`, `org:m5stack cc1101`, `org:m5stack cap`, `org:m5stack 1262` | repositories | 5 / **0** / 1 / **0** | **negative:** no Cap driver repos |
| GitHub search | `cardputer meshtastic` | repositories | 13 | community firmware catalogue |
| GitHub search | `cardputer repo:meshtastic/firmware` | code | 9 files | located the variant |
| GitHub API | `repos/meshtastic/firmware/git/trees/master?recursive=1` | — | not truncated | **negative:** no variant for the original Cardputer; M5Stack variants are `m5stack_core`, `m5stack_coreink`, `m5stack-stamp-c3`, `m5stack_unitc6l`, `m5stack_cardputer_adv`, `m5stack_cores3` |
| GitHub API | `commits?path=variants/esp32s3/m5stack_cardputer_adv&per_page=20` (+ page 2 empty) | — | 20 commits, exhausted | full change history |
| GitHub API | `compare/<sha>...<tag>` × 2 | — | ahead 17 / behind 177 | **first containing release** |
| `old.reddit.com/search.json` | `"Cap LoRa-1262"`, `cardputer lora`, `cardputer meshtastic`, `"Cap CC1101"`, `"Cardputer Mesh Kit"`, `"LoRa868" cardputer` | `sort=new&limit=100&t=all` | 217 unique posts, 2025-09-04 → 2026-09-04 | community dossier |
| `old.reddit.com` | 12 permalinks `.json?limit=100` | — | 200 each | quoted threads |

## Chronology of what changed the conclusions

1. **First surprise (docs).** The Cap LoRa-1262 page names **`AT6668`** as the GPS chip and
   `ATGM336H-6N` as the module — the brief said "ATGM336H". Both are right; they are
   module and chipset. Two component records created accordingly.
2. **Second surprise (CDN filenames).** The schematic is `…SCH_V1.1_20251029…` — a
   **2025** design. Prompted the release-date check.
3. **The correction.** Shopify `published_at` = **2025-12-30**, not 2026-08/09. Confirmed
   three ways (Shopify, M5Stack's own Reddit announcement of the same date, CDN
   product-number ordering).
4. **The real 2026 board.** `Cap CC1101 & NFC` (U219), `published_at` **2026-08-28**, seven
   days before this snapshot.
5. **The "older extension" answer.** The full-catalogue dump surfaced
   **`U201 [EOL] LoRa+GPS Cap for Cardputer Adv`, published 2025-09-05** — the same day as
   the Cardputer-Adv itself. That is the older Cardputer LoRa extension, and it is for the
   **Adv**, not the original Cardputer.
6. **The original Cardputer's real story.** Its docs show only a Grove port; upstream
   Meshtastic has **no** variant for it; the community answer in 2025-09 was *"not enough
   GPIO"*. So for the original Cardputer the honest answer is Grove-attached **Units**, not
   a LoRa "cap".
7. **A resolved cross-device gap.** The U214 schematic prints names for `Stamp LoRa-1262
   Mini` pins **11/12/13** (GND/ANT/GND) that the PaperMono schematic leaves blank —
   answering an open question in the existing component record.
8. **A resolved cross-device conflict.** Meshtastic's `variant.h` uses **1.8 V** TCXO where
   M5Stack uses **3.0 V** on the same module family. Recorded rather than picked.

## Dead ends and negative results (kept deliberately)

- No `Cap LoRa-1262` driver library exists from M5Stack.
- No certification identifier for U214 anywhere in M5Stack's own certification index.
- No LoRaWAN example, project or configuration for any Cardputer Cap.
- No RF/current measurement of this board by anyone, vendor or community.
- `pins:` mode of the local schematic reader misattributes text under a pypdf-derived bbox;
  documented in [`commands.md`](commands.md) so it is not silently trusted.

## Stopping criterion

Stopped when: every published M5Stack artifact for U214 was either retrieved or explicitly
listed as *not fetched* in [`sources.md`](sources.md); the upstream Meshtastic history for
the board was walked to exhaustion; and Reddit queries had stopped returning new
threads for the product. **Declared exclusions:** `community.m5stack.com`, distributor and
marketplace pricing, FCC/CE regulatory databases, product video, and the UiFlow2
MicroPython API page.
