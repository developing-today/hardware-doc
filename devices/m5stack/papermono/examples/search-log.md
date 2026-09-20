# PaperMono — example and project search log

> Search cutoff **2026-09-01**. The device shipped 2026-08-21, so the entire
> population is at most eleven days old.
>
> Most rows below are **consolidated from the earlier discovery passes** recorded
> in [`../research-log.md`](../research-log.md) and
> [`../projects-and-community.md`](../projects-and-community.md), rather than
> re-run. Rows marked **[new]** were executed during this cataloguing pass on
> 2026-09-01. The distinction matters: consolidated rows inherit their original
> retrieval dates and any staleness that came with them.

## Newly executed in this pass

| # | Service | Query / endpoint | Depth | Disposition |
|---|---|---|---|---|
| N1 | GitHub REST API **[new]** | `GET /repos/{owner}/{repo}` for all 43 repositories named in `projects-and-community.md` | 43/43 | **useful** — identity, licence, stars, dates |
| N2 | GitHub REST API **[new]** | `GET /repos/{owner}/{repo}/commits?per_page=1` for the same 43 | 43/43 | **useful** — HEAD SHA for every entry |

**Result: 43 of 43 repositories resolved. None gone, none private, none
archived.** This closes a recorded defect of the previous pass, which cited
third-party repositories without pinning any commit.

Authentication was required: `api.github.com` limits to 60 requests/hour
unauthenticated, and 86 calls were needed. `gh auth token` raises this to 5,000.
A first serial attempt was abandoned as too slow and replaced with a 16-way
parallel pass.

## Consolidated from earlier passes

| # | Service | Query | Depth | Disposition |
|---|---|---|---|---|
| C1 | GitHub repo search | `papermono`, `paper mono`, `PaperMono`, `C153`, `M5PaperMono` | multiple pages | useful — core population |
| C2 | GitHub code search | `board_M5PaperMono`, `m5stack_papermono`, `DEPG0397BBS770F3` | full | useful — found upstreams shipping support |
| C3 | GitHub org listing | `m5stack`, `crosspoint-reader`, `Free-Ink` | full | useful |
| C4 | M5Burner API | `burner.m5stack.com/api/v1/firmwares/...` | 4 PaperMono entries | useful — two binaries retrieved and validated |
| C5 | Reddit | `old.reddit.com/search.json` (UA `WhatsApp/2.23.20.0`) — `papermono` **and** `paper mono` | site-wide + r/esp32, r/eink | thin — two results, both bot mirrors of one HN post |
| C6 | Hacker News | `hn.algolia.com/api/v1/search?query=papermono` | full | one post |
| C7 | Mojeek | `M5Stack PaperMono` and variants | 5 pages | useful — surfaced LinuxGizmos, Liliputing, MuyLinux |
| C8 | YouTube | `M5Stack PaperMono` | first pages | one hands-on video (Volos Projects, 2026-08-29) |
| C9 | Hackaday `wp-json` | `papermono` | full | **dead** — `[]`, Hackaday published nothing |
| C10 | `community.m5stack.com` | search | — | **inaccessible** — 401, auth-walled |
| C11 | hackster.io | various | — | **inaccessible** — no working retrieval path found |
| C12 | DuckDuckGo / Marginalia | `papermono` | — | **rejected** — 202 anomaly / bot-wait |

## Known exclusions

- **GitLab, Codeberg, SourceHut and Gitea instances were not searched.** Recorded
  as a gap, not as absence of evidence.
- **Discord** (M5Stack and e-ink community servers) was not searched — not
  publicly indexable without joining.
- **Chinese-language platforms** (Gitee, Bilibili, CSDN) were not searched. Given
  M5Stack is a Shenzhen company with a large domestic community, this is the most
  likely place for uncatalogued work, and is the single biggest known hole.
- Release tags were **not** collected per repository; only HEAD commits. Recorded
  as `null` with a note in every catalogue entry.

## Stopping criterion

Discovery stopped when two consecutive broad passes returned only duplicates of
the already-catalogued population and vendor marketing copy. The binding
constraint is the world, not the search: eleven days after launch there were zero
written independent reviews and one video.

This is a **reproducible broad-coverage snapshot dated 2026-09-01**, not a claim
that no other project exists. The exclusions above — particularly the
Chinese-language platforms — are the places to look first in a later pass.

## Cross-references

- [`catalog.json`](catalog.json) — all 43 entries with pinned commits
- [`best.md`](best.md) — the selected portfolio and why
- [`../projects-and-community.md`](../projects-and-community.md) — the prose analysis and classification
- [`../coverage.md`](../coverage.md) — feature-to-evidence map
