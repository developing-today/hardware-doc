# Xteink X4 Pro — example search log

Snapshot **2026-09-04**. **No example was built, flashed or run** — no hardware.
Every entry is cataloged from repository metadata and, where fetched, source text.

## Where "examples" live for this device

There is **no vendor SDK and no vendor example set.** Xteink publishes nothing:
no datasheet, no board-support package, no sample code, no documentation.

So the example corpus is entirely **community firmware**, and it has an unusual
shape: instead of many small per-feature demos, it is a handful of **large,
complete e-reader applications** plus a very long tail of forks that change UI
details. Per-feature minimal examples barely exist.

That shapes selection: [`best.md`](best.md) picks by **which project best
demonstrates a given hardware path**, not by "smallest runnable demo".

## Searches performed

| Service | Query | Depth | Useful | Rejected |
|---|---|---|---|---|
| GitHub repo search | `xteink` | 2 pages / 378 total | many | forks, wallpaper tools |
| GitHub repo search | `xteink x4` | 2 pages / 198 total | many | duplicates |
| GitHub repo search | `crosspoint reader` | 2 pages / 105 total | many | non-Xteink `CrossPoint` (an OS/2 mail reader) |
| GitHub repo search | `freeink` | 2 pages / 17 total | 4 | unrelated "FreeInk" web projects |
| GitHub repo search | `crossink` | 2 pages | ~15 | simulators, wallpapers |
| GitHub code search | `FREEINK_DEVICE_X4PRO`, `XTEINK_X4_PRO`, `xteink_x4_classic` | 100 each | board-profile consumers | — |
| GitHub GraphQL | `crosspoint-reader` discussion #2259 | 1 | **1 — decisive on NFC** | — |
| Reddit | 22 term queries + 6 subreddit sweeps + 8 full threads | 2,136 posts | project announcements | — |

## Filtering

~200 repositories mention the family. Of those:

| Category | Count (approx) | Disposition |
|---|---|---|
| Complete firmware (mainline or substantial fork) | ~40 | **candidates** |
| Personal/cosmetic forks | ~60 | rejected — no new hardware coverage |
| Wallpaper / sleep-screen generators | ~25 | rejected — host-side, no device code |
| Format converters (`.XTC`, EPUB, PDF) | ~20 | rejected — host-side |
| Font tooling | ~10 | rejected — host-side |
| Sync servers / OPDS / companion apps | ~20 | rejected — host-side |
| Flashers and recovery tools | ~6 | **cataloged** — they exercise the flash path |
| **X4 Pro-specific** | **6** | **all cataloged** |

## Rejected candidates worth naming

| Repo | Why rejected |
|---|---|
| `OS2World/APP-INTERNET-OpenXP` | A 2013 OS/2 mail reader also called "CrossPoint". **Name collision**, not this ecosystem |
| `daviddivinefavour/freeInks`, `ranya-alhosan/FreeInk-React`, `hp-freeink/*` | Unrelated projects sharing the word "FreeInk" |
| `Dirinkbottle/freeink` (2025-01) | Predates this ecosystem; unrelated |
| Dozens of `crosspoint-reader` forks with no description and no divergence | No additional hardware coverage |

## Inaccessible / not inspected

| Item | Reason |
|---|---|
| `crossplay.ma-r-s.com`, `crosspointreader.com`, `crossink.uxj.io`, `brickclub.pages.dev`, `readme.club` | Community sites; **not fetched** this session |
| `spokenlikeageek.com` Tong Card write-up | Not fetched |
| Any binary release asset | Not downloaded — no hardware to flash |

## Declared limits

- **Nothing was built.** No toolchain was installed, no `pio run` was attempted.
- Selection is by **source reading and repository metadata**, so every status
  below is `inferred` unless the project itself claims otherwise.
- Fork lineage is recorded where the API reports a parent; several personal forks
  are standalone re-uploads and their lineage is stated as `unknown`.
