# Tanmatsu — research log

> Reproducible record of what was searched, what was found, and what was rejected.
> Pass conducted **2026-08-24**. Search cutoff: 2026-08-24.

## Method

Primary-source-first. The device is fully open hardware, so effort went into **retrieving and parsing
the vendor's own design and firmware files** rather than aggregating secondary commentary. Community
mining was deliberately limited (see *Exclusions*).

## Source-class coverage

| Class | Searched | Result |
|---|---|---|
| Manufacturer product page | ✅ `tanmatsu.cloud` / `tanmatsu.com` | **Rejected as a source** — JavaScript SPA, returns no server-rendered content |
| Manufacturer documentation | ✅ `tanmatsu-documentation` repo | **Primary** — Sphinx/MyST source cloned and snapshotted |
| Manufacturer design files | ✅ `tanmatsu-hardware`, `tanmatsu-mechanical` | **Primary** — KiCad + production BOM + FreeCAD, CERN-OHL-P |
| Manufacturer firmware | ✅ 6 repos | **Primary** — coprocessor, radio, launcher, components |
| **Community/ecosystem docs** | ✅ `badge.team/docs/badges/konsool/` | **Primary, high value** — 42 pages, IC-level pinouts. *Found late via a README link* |
| Board support package | ✅ `badgeteam/esp32-component-badge-bsp` | **Primary** — authoritative pin definitions |
| Third-party component vendor | ✅ `solder.party` docs + 31 repos | **Primary** — keyboard identification |
| Component registry | ✅ `components.espressif.com` | Display and RVSWD components |
| Package/app registry | ✅ `app-repository` (57 apps) | Ecosystem statistics |
| Repository search | ✅ GitHub `tanmatsu` (117 repos), `konsool` (38) | Catalogued |
| Component datasheets | ⚠ Manufacturer product pages only | **No local datasheet copies retained** — gap |
| Regulatory databases | ❌ Not searched | Gap |
| Forums / chat | ❌ Not searched — **excluded by request** | Discord, Telegram |
| Blogs / video / social | ❌ Not searched | Gap |
| Pricing / retail | ❌ Not searched | Gap |

## Query ledger

| # | Service | Query / URL | Result |
|---:|---|---|---|
| 1 | curl | `tanmatsu.cloud`, `tanmatsu.com`, `www.tanmatsu.cloud` | 200, all → `tanmatsu.cloud`. **SPA, no content.** `.com` 301s to `.cloud` |
| 2 | GitHub API | `search/repositories?q=tanmatsu` | 117 results; 10 official under `Nicolai-Electronics` |
| 3 | git clone | 10 × `Nicolai-Electronics/*` | All succeeded, pinned commits in [`sources.md`](sources.md) |
| 4 | GitHub API | `repos/badgeteam/esp32-component-badge-bsp/contents/targets` | 11 targets; **no `konsool` target** |
| 5 | grep | `konsool` across all cloned repos | Hits in `app-repository`, `esp32-component-tanmatsu-wifi`, docs |
| 6 | GitHub API | `search/repositories?q=konsool` | 38 results; **badgeteam owns 4 Konsool repos** |
| 7 | raw.githubusercontent | `badgeteam/konsool-template-lvgl/main/README.md` | **Breakthrough** — links `badge.team/docs/badges/konsool/` |
| 8 | curl | `badge.team/docs/badges/konsool/` | **Definitive Konsool/Tanmatsu explanation** |
| 9 | curl | `badge.team/sitemap.xml` | 42 Konsool URLs enumerated |
| 10 | curl | all 42 Konsool pages | All 200. IC pinouts, camera compatibility, FAQ |
| 11 | curl | `solder.party`, `/docs/`, `docs.solder.party` | 200; `docs.` → `www./docs/`. Server-rendered |
| 12 | GitHub API | `search/repositories?q=user:solderparty` | 31 repos |
| 13 | curl | 7 Solder Party product doc pages | All 200 |
| 14 | git clone | `solderparty/i2c_puppet` | MIT; full I2C protocol README |
| 15 | curl | `components.espressif.com/.../mipi_dsi_abstraction` | Panel/controller mapping |
| 16 | direct read | `production/bom.csv` | 84 lines, LCSC numbers |
| 17 | direct read | `tanmatsu-coprocessor-firmware/src/application/*` | Matrix, register map, pin defines |
| 18 | direct read | `badge-bsp/targets/{tanmatsu,why2025}/*` | Authoritative pins; proved WHY2025 ≠ Tanmatsu |

## Dead ends and rejected results

| Attempt | Outcome |
|---|---|
| `tanmatsu.cloud` HTML scrape | **Rejected** — SPA shell, only "Application is starting…" |
| `badge.team/docs/badges/konsool/quick-start/` | **404** — correct path is `/quickstart/` (no hyphen). Found via sitemap |
| `badge.team/docs/badges/konsool/expansion-boards/` | **404** — correct path is `/expansion_boards/` (underscore) |
| `raw.githubusercontent.com/badgeteam/konsool-*/main/README.md` | **404** for 3 of 4 repos — default branch is not `main`. Not retried |
| Sidebar link extraction from badge.team HTML | **Failed** — navigation is not in the served HTML. Sitemap used instead |
| `snowdrop4/tanmatsu`, `d3npa/GB-tanmatsu` | **Rejected** — unrelated projects sharing the word |
| Konsool hardware repository | **Does not exist.** Konsool uses the Tanmatsu hardware repo |

## Notable retrieval findings

- **`badge.team` is the more valuable hardware source**, and nothing in any Nicolai Electronics repository links to it. It was reached only via a badgeteam *app template* README. A researcher following the vendor's own documentation would never find the IC pinouts.
- **badge.team URL paths are inconsistent** — `quickstart` (no separator) vs `expansion_boards` (underscore) vs `pinout/ics` (slash). **Always enumerate via `sitemap.xml`**; do not guess.
- Both `badge.team` and `solder.party` are **server-rendered Hugo** sites: plain `curl` with a browser User-Agent works, no bot-blocking encountered.
- **No source required authentication, and nothing was paywalled or rate-limited.**

## Stopping criteria

Stopped when:

- All 10 official repositories were cloned and their design/firmware/documentation content extracted.
- All 42 badge.team Konsool pages and all applicable Solder Party product pages were retrieved.
- The BSP, the coprocessor firmware and the production BOM had all been read for pin-level facts, with three-way cross-checking.
- Two further GitHub searches (`tanmatsu`, `konsool`) returned only duplicates and unrelated name collisions.
- Remaining unknowns require **hardware**, **FreeCAD**, or **excluded community channels**.

## Declared exclusions

- **Discord and Telegram** — excluded at the user's request.
- **Pricing, availability, retail** — not researched.
- **Regulatory filings** — not searched.
- **Blogs, video, social media** — not searched.
- **Component datasheets were not downloaded**, only manufacturer product pages cited.
- **FreeCAD files not opened** — tool unavailable; case dimensions not extracted.
- **KiCad netlist not parsed** — pin data taken from BSP/docs instead. `production/netlist.ipc` is retained and would allow independent derivation.

This is a **broad-coverage snapshot dated 2026-08-24**, not proof that no other resource exists.
