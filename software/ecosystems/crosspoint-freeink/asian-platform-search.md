# Asian-platform search for ESP32 / M5Stack e-paper software

> Closing the gap flagged in every previous sweep: all prior searching was
> English-language and GitHub-centric. This pass covers Japanese and Chinese
> developer platforms.
>
> Searched **2026-09-11**. Retrievals are `executed-success`; the absence claims
> are qualified below — some platforms could not be searched at all, which is
> **"no determination"**, not "nothing there".

## Headline

**Japanese-language sources are productive and were a real gap.** They surfaced a
project absent from every prior sweep, and a substantial technical corpus around
the exact NFC library this knowledge base has been analysing.

**Chinese-language sources are thin for this specific device, and that is now
partly measured rather than assumed.** CSDN — searchable on a second attempt via
its JSON API — carries **4,301 articles on `M5Paper` and zero on `M5PaperMono`**.
Gitee and Zhihu remain inaccessible, so the picture is still incomplete.

## Platform results

| Platform | Query path | Result |
|---|---|---|
| **Qiita** (JP) | public API `/api/v2/items` | ✅ **Productive** — see below |
| Zenn (JP) | `/api/search` | 0 articles for `PaperMono` |
| **Bilibili** (CN) | web search | 1 real hit — **the vendor's own product announcement only** |
| Gitee (CN) | API `/api/v5/search/repositories` | **0 for `m5stack`, `esp32` *and* `arduino`** — control test proves the endpoint is gated, not empty. **No determination** |
| Gitee search UI | `search.gitee.com` | 849 B — JS shell. **No determination** |
| **CSDN** (CN) | **`so.csdn.net/api/v3/search`** | ✅ **Searchable after all** — see the correction below |
| Zhihu (CN) | `/search` | **HTTP 403** — blocked |

The Gitee API returning zero results for `m5stack` — a vendor with a large Chinese
following — is strong evidence the endpoint is gated rather than empty. **Do not
read these as verified absences.**


## Correction: CSDN is searchable, and it changes two conclusions

The first pass hit `so.csdn.net`'s HTML search page, got a 5,850-byte JavaScript
shell, and recorded "no determination". **That was a tooling failure, not an
absence.** CSDN exposes a working JSON API:

```
https://so.csdn.net/api/v3/search?q=<query>&t=blog&p=1
```

With that, two earlier statements must be revised:

**1. `M5PaperMono` genuinely has no Chinese-language coverage.** CSDN returns
**4,301 articles for `M5Paper`** but **zero for `M5PaperMono`**. That is now a
*measured* absence on China's largest developer-blog platform, not an untested
guess. The general M5Paper line is well covered in Chinese; the Mono is not.

**2. There is a real SSD1677 corpus — 69 articles.** Two look directly relevant to
open questions in this knowledge base:

| Date | Title | Why it matters |
|---|---|---|
| 2023-08-08 | 高分辨率大屏墨水屏调测问题 — *"Debugging issues with high-resolution large e-paper displays"* | Predates this device; the SSD1677 drives exactly that class of panel |
| 2026-02-13 | SSD1683墨水屏驱动电压参数优化实战 — *"Practical driver voltage parameter optimisation for SSD1683 e-paper"* | **Voltage-parameter tuning on a sibling Solomon Systech controller** — the same family as the [C25 booster question](../../../devices/m5stack/papermono/gaps-and-conflicts.md) |

**Neither article was read.** They are recorded as leads, identified from titles
and dates only. The SSD1677 result set is also noisy — it contains QNAP NAS and
laptop-SSD articles matching on the alphanumeric fragment — so 69 is an upper
bound on genuinely relevant material.

`墨水屏 ESP32` ("e-paper ESP32") returns **1,567 articles**, including firmware
optimisation and SPI driver write-ups. So the Chinese ESP32 e-paper community is
substantial; it simply has not engaged with this specific board.

### What this says about method

The difference between "no determination" and a measured zero was **one API
endpoint**. The first pass treated a JavaScript shell as evidence; it was only
evidence that the wrong URL had been fetched. The Gitee control test — querying
`arduino` and `esp32` and getting zero for both — is the pattern that should have
been applied to CSDN immediately.

Gitee and Zhihu remain genuinely unsearched.

## The find: `mitsuharu/CardCase-For-M5Paper`

Discovered only via a Qiita article, and **not present in any prior sweep**.

| | |
|---|---|
| Repository | `mitsuharu/CardCase-For-M5Paper` |
| Licence | **MIT** — unlike the other two badge projects |
| Language | C++ · ★1 · 2.9 MB |
| Created | **2025-03-28** — predates the PaperMono |
| Pushed | 2026-09-07 |
| Description | *"Display images saved on an SD card on M5Stack e-paper devices. Also displays images received via WiFi or NFC."* |

Announced in [Qiita 6a764283f6f9e7ccf1b6](https://qiita.com/mitsuharu_e/items/6a764283f6f9e7ccf1b6)
(2026-09-05, author `mitsuharu_e`): *"A name-badge solution with smartphone
integration for M5Stack Paper v1.1 / S3 / Color / Mono."*

Two things make it notable:

1. **It supports four M5Paper generations** — v1.1, S3, Color and Mono — from one
   codebase. That is the broadest device coverage of any third-party project found
   for this board, and it arrived by extending an existing 2025 project rather
   than starting fresh.
2. **It is MIT.** `ciniml/paper_name_plate` and the sd-plugins ecosystem are
   unlicensed; this is a usable reference implementation.

## Four independent name-badge projects

With this addition the convergence is striking:

| Project | Language | Licence | Approach |
|---|---|---|---|
| `ciniml/paper_name_plate` | Rust | none | NFC **tag emulation**, BLE config |
| `Corvelis/m5-touch-card` | C++ | MIT | NFC exchange + **smartphone app** |
| `mitsuharu/CardCase-For-M5Paper` | C++ | **MIT** | Image display, **NFC/WiFi image receive**, 4 devices |
| *(vendor demo)* | C++ | MIT | NFC identity read only |

**Three independent Japanese developers built a digital name badge within weeks of
launch.** That is not coincidence: Japanese technical-conference culture places
heavy weight on 名札 (name badges) and 名刺交換 (business-card exchange), and a
device that is a screen plus a tag emulator maps onto it exactly.

This is the clearest "what is this hardware actually for" signal found in any
sweep, and **it was invisible to English-language search.**

## The Qiita corpus

Article counts by query (API, `per_page=100`, so 100 means "at least 100"):

| Query | Items |
|---|---|
| `M5Paper` | **100+** |
| `電子ペーパー` (e-paper) | **100+** |
| `ESP32 NFC` | 43 |
| **`M5Unit-NFC`** | **24** |
| **`ST25R3916`** | **11** |

**24 articles on `M5Unit-NFC`** — the library with the
[stack overflow documented here](m5unit-nfc-overflow.md). If community knowledge
of that library's behaviour exists anywhere, it is here, in Japanese, and this
project has not read it.

Relevant articles spotted:

- `fknaopen`, 2026-08-17 — *"Reading NFC-F (FeliCa) with Unit NFC (for the legacy
  M5Stack library)"*. FeliCa is the Japanese transit/payment standard; the
  ST25R3916 supports it and Western coverage of that path is thin.
- `misoca12`, 2024-11-29 (LGTM 5) — *"Reading multiple RFID tags simultaneously
  with M5Stack"* — anticollision, which is exactly the code path containing the
  overflow.
- `ksasao`, 2025-12-19 — *"Writing 'when and where' onto a paper business card on
  the spot"* — the same problem space, pre-dating the PaperMono.

## What this changes

- **The project catalogue was incomplete**, and the missing entry is the only
  MIT-licensed badge implementation.
- **Japanese sources should be part of the standard sweep**, not an afterthought.
  Qiita has a public, unauthenticated API and is trivial to query.
- **The "NFC is the killer app" finding is stronger than previously stated** —
  four implementations, three independent authors, one cultural driver.
- **Chinese-language coverage remains genuinely unknown.** Bilibili carries the
  vendor announcement and nothing else found; Gitee, CSDN and Zhihu could not be
  searched.

## Method and limits

Qiita and Zenn were queried through public APIs. Bilibili was fetched with a
browser user-agent and parsed from embedded JSON. Gitee's API returned an empty
array for every query including control terms; its search UI is a JS shell. CSDN
returned a near-empty JS shell. Zhihu returned 403.

**Corrected mid-survey:** CSDN was initially recorded as unsearchable; its JSON
API works and was used for the figures above.

**Not attempted:** Weibo, Baidu Tieba, Douyin, Xiaohongshu, Taobao listings,
Japanese `note.com`, `elchika`, Switch Science's blog, or any forum requiring
login. Machine translation was not used — Japanese titles were read directly and
Chinese hits were too few to need it.

**No article was read in full**; titles, dates, tags and the one relevant body
excerpt were used. Nothing was built or run.

## See also

- [New PaperMono projects](new-papermono-projects-2026-09.md) — the English-language sweeps
- [NFC implementation comparison](nfc-implementation-comparison.md)
- [`M5Unit-NFC` overflow](m5unit-nfc-overflow.md) — the library those 24 Qiita articles discuss
