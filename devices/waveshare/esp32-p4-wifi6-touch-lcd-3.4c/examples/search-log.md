# Example discovery log

> ESP32-P4-WIFI6-Touch-LCD-3.4C / 4C. Searches run **2026-08-24** and **2026-08-26**.
> Dispositions in [`catalog.json`](./catalog.json); selections in [`best.md`](./best.md).

## Queries run

| # | Service | Query | Depth | Result |
|---|---|---|---|---|
| 1 | GitHub repo search | `ESP32-P4-WIFI6-Touch-LCD` | 37 hits, top 10 | **Found Waveshare's official org** — the highest-value result of the whole pass |
| 2 | GitHub repo search | `ESP32-P4-WIFI6-Touch-LCD-3.4C` | 3 hits, all | 2 community projects on the exact board |
| 3 | GitHub repo search | `esp32_p4_wifi6_touch_lcd` | 37 hits, top 10 | Duplicates of #1 |
| 4 | GitHub org search | `org:waveshareteam ESP32-P4-WIFI6` | all | **7-board family**: 3.5, 4.3, 4B, 5, 7B, X, XC |
| 5 | GitHub contents API | `…/XC/contents/examples/esp-idf` | all | **12 official examples** enumerated |
| 6 | GitHub contents API | `…/XC/contents/{docs,firmware,hardware,scripts}` | all | 16 bilingual docs, factory firmware, schematic |
| 7 | Espressif registry API | `waveshare/esp32_p4_wifi6_touch_lcd_xc` | all versions | BSP `0.0.1`→`3.0.1`, Apache-2.0 |
| 8 | Espressif registry API | `espressif/esp_lcd_jd9365` | all versions | Driver source; **third `0x40` value** (C15) |
| 9 | Demo ZIP inspection | 5052 files | full extract | Older example numbering, per-variant panel demos |
| 10 | Vendor wikis (EN + CN) | product pages | full | Feature lists; **28-GPIO count** from CN only |

## Dispositions

| Status | Count | Notes |
|---|---:|---|
| **selected** | 11 | 10 official ESP-IDF + 1 community |
| **catalogued** | 4 | Real but not in the recommended path |
| **rejected** | 4 | 1 no-hardware skeleton + **3 wrong-board** |
| **superseded** | 1 | Demo ZIP, replaced by the repository |

## The rejection that matters

The three most-starred projects in the ESP32-P4 display family — NINA Display (46★, **4B**), LVGL
Boilerplate (10★, **7B**), HA Dashboard (4★, **7B**) — all target **different boards**.

They are the obvious things to cite when a search for "ESP32-P4 Waveshare display" returns them
near the top, and citing them as evidence for the 3.4C/4C would be wrong: different panels,
resolutions and BSP variants. Their *techniques* transfer; their pin values and configuration do
not. Recorded as `rejected` rather than dropped, so a future pass does not rediscover and misuse
them.

## Pass 12 — authenticated code search (2026-08-26)

Obtained a token with `gh auth token`, which unblocked the code search that had returned `401`.

| Query | Type | Result |
|---|---|---|
| `BSP_LCD_TYPE_800_800_3_4_INCH` | code | **187 matches**, 8+ distinct projects |
| `BSP_LCD_TYPE_720_720_4_INCH` | code | **171 matches** |
| `esp32_p4_wifi6_touch_lcd_xc` | code | **178 matches**, incl. **`waveshareteam/Waveshare-ESP32-components`** — the BSP source |

**This changed the picture completely.** Community projects went from 2 to a dozen-plus, including
a **256-star** project on the 3.4C and an **89-star** one on the 4C. Variants were confirmed
individually from each project's `sdkconfig`.

It also found the **BSP source repository**, which an earlier pass had written off as *"resolved by
the Component Manager, not vendored"*. Its header independently confirmed all sixteen GPIO
assignments derived from the schematic.

Technique written up as a reusable guide:
[`guides/research/finding-projects-that-use-a-board.md`](../../../../guides/research/finding-projects-that-use-a-board.md).

## Pass 13 — probing for GPIO45 / GPIO33 use (2026-08-26)

Targeted code searches to attack the two highest-impact open items:

| Query | Result |
|---|---|
| `GPIO_NUM_45` + board | **0 hits** — nobody drives the SD power switch |
| `GPIO_NUM_33` + board | 62 hits, **all XiaoZhi board configs for *other* variants** |
| `BL_EN` + esp32p4 | 11 hits, none for this board (NuttX Tab5, ESP-IDF EMAC) |

Both searches were **negative**, which is itself the finding: across the BSP, the demos, a Linux
port, XiaoZhi and three application projects, **nothing drives GPIO45 or GPIO33**. Both rails are
almost certainly default-on.

The `GPIO_NUM_33` search also surfaced **XiaoZhi**, which turned out to be the most useful community
source found — see [`best.md`](./best.md).

## Honest limits

**Nothing was built or run.** No hardware, no toolchain invocation. Every catalogue entry carries
`build_status: not-built-here`. Selections rest on source inspection, feature coverage and
provenance — not observed behaviour. Waveshare say the same of their own BSP contract: it is
compile-verified, not hardware-verified.

**GitHub-only community search.** Not searched: forums, Reddit, YouTube, blogs, Hackaday,
Instructables, or Chinese community sites (立创开源, 电子发烧友, CSDN, Bilibili). One
Chinese-language GitHub project (`ShizhanQiao/FishAgent`) was found incidentally, so more likely
exist off-GitHub.

**No non-English query was run against GitHub**, despite Waveshare shipping 中文 documentation.

## Stopping criterion

Stopped when GitHub queries returned only duplicates and the official repository had been
enumerated exhaustively. This is a complete survey of **GitHub and vendor sources**, and is
labelled as such — not a claim that no other example exists.

## Highest-value next searches

1. Chinese community sites — most likely to hold real projects.
2. YouTube — round-display builds are visual and often demoed rather than written up.
3. ~~GitHub code search~~ — **done, pass 12; it was the single highest-yield query of the whole
   research.**
