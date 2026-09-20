# CrossPlay

> A personal fork of [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader)
> that adds games and small tools alongside the reader.
> **`ma-r-s/crossplay`** · branch **`xteink`** (default) · MIT · ★15 ·
> created 2026-08-07 · last push 2026-09-02 · https://crossplay.ma-r-s.com
>
> Research snapshot **2026-09-01/02**. Nothing was built, flashed or run — no
> hardware. Every claim is read from the repository at the cited path and is
> `inferred` unless marked otherwise.

**Classification:** application (complete firmware), not a library or framework.
Downstream fork. Single-author personal project, MIT-licensed, publicly developed.

## Why this record matters here

CrossPlay is the clearest worked example in this ecosystem of **how to fork a
fast-moving upstream and stay mergeable**. Its `LOCAL_SCOPE.md` is an explicit,
maintained accounting of every upstream file the fork touches and why — the
question "could these changes be a patch series instead of a fork?" is answered
in the repository itself rather than having to be reverse-engineered.

It is also, relevantly to this knowledge base, **a firmware that builds for the
[M5Stack PaperMono](../../../devices/m5stack/papermono/README.md)**.

## Identity

| Field | Value |
|---|---|
| Repository | `ma-r-s/crossplay` |
| Upstream parent | `crosspoint-reader/crosspoint-reader` (API `parent` and `source` both) |
| Default branch | **`xteink`** — not `main`, not `develop` |
| Licence | MIT |
| Language | C / C++ |
| Author | Mario Alejandro Ruiz |
| Homepage | `https://crossplay.ma-r-s.com` |
| Submodule | `freeink-sdk` → **`ma-r-s/freeink-sdk`**, branch `x4pro-measured-insets` |

The submodule is worth noting on its own: **CrossPoint consumes the FreeInk SDK
as a git submodule**, and CrossPlay forks that too. So the fork is a *pair* of
forks, and a port has two moving upstreams, not one.

## Divergence from upstream

Measured 2026-09-02 via `GET /repos/crosspoint-reader/crosspoint-reader/compare/develop...ma-r-s:crossplay:xteink`
(`executed-success` — the API call was made; the numbers are GitHub's).

| Metric | Value |
|---|---|
| Status | diverged |
| Ahead | **2,391 commits** |
| Behind | **65 commits** |
| Files changed | 300 (**API caps the file list at 300 — the true count is higher**) |
| Lines | +18,096 / −862 within that capped set |

Where the churn is concentrated, by top-level path:

| Path | Lines changed | Nature |
|---|---|---|
| `docs/` | 12,445 | new files |
| `host-tests/` | 2,956 | new files |
| `assets_local/` | 1,063 | new files |
| `.github/` | 933 | fork identity |
| `README.md`, `AGENTS.md`, `LOCAL_SCOPE.md`, `USER_GUIDE.md`, `ROADMAP.md` | ~1,250 | fork identity |

**Read that table carefully: essentially all of it is new files.** The
−862 deletions across 300 files is the real signal — this is an overwhelmingly
*additive* fork. "2,391 commits ahead" sounds like massive divergence and is not.

## The quarantine pattern

Everything the fork adds lives in paths that do not exist upstream:

```
src/apps_local/     the apps themselves (36 entries: shelf machinery + ~26 apps)
assets_local/       icons and art
scripts_local/      fork tooling
tools_local/
host-tests/         tests
docs/               fork documentation
```

New files cannot conflict. That is the whole trick, and it is applied
consistently.

### The upstream files it *does* touch

`LOCAL_SCOPE.md` enumerates **28 upstream files**, of which roughly half are
identity (README, LICENSE, GOVERNANCE, ROADMAP, `.github/` templates, funding,
workflows) and merge trivially or not at all. The genuine **code seams** are
these — quoted from the repository's own table:

| File | Why | Size |
|---|---|---|
| `src/activities/home/HomeActivity.{cpp,h}` | Games and Apps rows on Home, plus `upstreamMenuRows()` | 4 hooks + 1 method |
| `src/components/themes/BaseTheme.h` | Two values **appended** to the `UIIcon` palette | 1 appended block |
| `src/components/themes/lyra/LyraTheme.cpp` | Two cases mapping them to bitmaps | 4 lines |
| `src/activities/ActivityManager.cpp` | `Frontlight.present()` guard on the light-panel gesture | 1 guard |
| `src/MappedInputManager.{h,cpp}` | `swallowCurrentTouch()` wrapper over the SDK suppression latch | 1 method |
| `src/network/OtaUpdater.cpp` | Release URL repointed — upstream's would flash a **C3 build onto an S3** | 1 URL |
| `lib/hal/HalStorage.{h,cpp}` | `openFileForAppend()` — upstream's write carries `O_TRUNC` | 1 method |
| `lib/GfxRenderer/GfxRenderer.cpp` | Thick lines thicken across their direction; vertical paths drew 1 px | 1 fix |
| `lib/PngToBmpConverter/PngToBmpConverter.*` | `…FitWithin()` — contain, not cover | 1 method |
| `lib/KOReaderSync/KOReaderCredentialStore.cpp` | comment only | — |
| `src/components/UITheme.cpp` | `getScreenSafeArea()` starts from bezel viewable insets | 1 block |
| `.gitignore` | ignore `qa-artifacts/` and simulator SD cards | 3 lines, append-only |
| `platformio.ini` | one `extra_configs` line | 1 line |
| `.skills/SKILL.md` / `CLAUDE.md` | agent-facing banner | ~20 lines |
| `SCOPE.md` | one-line pointer | 2 lines |

## Patch portability — which of these would survive upstream churn

This is the analytically interesting part, and the fork's own design makes it
answerable.

**Trivially portable (append-only, structurally stable).** The `UIIcon` palette
addition, the `LyraTheme` switch cases, the `.gitignore` lines, the
`platformio.ini` include. Appending a value to the end of an enum preserves every
number below it; adding a case to a switch is a pure addition. The author states
explicitly that **none of these grow when an app is added** — the theme edits are
per *folder* and there are exactly two folders.

**Portable, and arguably belong upstream.** Four of the seams are not
game-specific at all — they are **bug fixes and missing primitives**:

- `GfxRenderer` thick-line direction fix
- `HalStorage::openFileForAppend()` (upstream cannot append to a file at all)
- `PngToBmpConverter::…FitWithin()` (contain vs cover)
- `UITheme::getScreenSafeArea()` bezel insets — without which *upstream's own
  screens draw under the glass*

Any of these could be a small upstream PR. That they live in a fork is a
maintenance liability for both sides, and the fourth in particular is a
correctness issue affecting stock CrossPoint on bezelled devices.

**Conflict-prone.** `HomeActivity.{cpp,h}` is the one real seam: four hooks plus
a method in a file upstream actively develops. The author mitigates this by
appending after upstream's rows so indices never shift, but any upstream
restructuring of the home screen lands here.

**Cannot be upstreamed by design.** The `OtaUpdater` URL — pointing at upstream
would flash a C3 image onto an S3 — and the identity files. These are inherent to
being a fork.

**Verdict:** this fork is **~90 % new files plus about a dozen small, mostly
append-only seams**. It is much closer to "a patch series plus a large additive
tree" than to a divergent codebase. The `SCOPE.md` disagreement — upstream says
interactive apps are out of scope, the fork says they are the point — is a
*policy* fork, not a technical one.

## Device support

Build environments in `platformio.ini`:

| Env | Board | Notes |
|---|---|---|
| `default`, `gh_release`, `gh_release_rc`, `slim` | `esp32-c3-devkitm-1` | inherited from upstream |
| `sticky`, `gh_release_sticky` | `esp32-s3-devkitc1-n16r8` | Seeed reTerminal Sticky, added 2026-08-25 |
| `x4pro`, `gh_release_x4pro` | ESP32-S3 | **Xteink X4 Pro — the design floor** |
| **`papermono`, `papermono-gh_release`, `papermono-gh_release_rc`** | `esp32-s3-devkitc1-n16r8` | **M5Stack PaperMono** |

`LOCAL_SCOPE.md` names the X4 Pro (ESP32-S3, 480×800 touch, frontlight) and the
reTerminal Sticky (same S3, same 800×480 panel, GT911 touch, three buttons, no
frontlight) as the targets; the design floor is "two side keys plus touch".

**The PaperMono envs are present in `platformio.ini` but are not described in
`LOCAL_SCOPE.md`.** Whether they are maintained, tested, or inherited from
upstream's PaperMono support is **not established here** — and nobody has
reported running CrossPlay on a PaperMono. Recorded as an open question, not as
"supported".

## What it adds

Roughly 26 app directories under `src/apps_local/`, described upstream-facing as
"twenty-one apps: seventeen games, a spaced-repetition trainer, a Hacker News
reader, an xkcd viewer and a catalog browser". Observed directory names include
`battleship`, `bridge`, `checkers`, `chess`, `connectfour`, `connections`,
`dungeon`, `forehead`, `insider`, `jaipur`, `knucklebones`, `minesweeper`,
`murdle`, `seasalt`, `solitaire`, `sudoku`, plus `hackernews`, `instapaper`,
`link`, `player`, `study`.

The shelf machinery (`Shelf`, `ShelfFolderActivity`, `ShelfScreen`,
`ShelfState`) enforces a two-level hierarchy — a folder holds items, never
folders — capped "by the type system rather than by discipline", and no app names
its own return destination (`shelf::leave()`).

## Deliberate deviations from upstream conventions

Scoped entirely to `src/apps_local/`, and documented rather than accidental:

| Upstream rule | CrossPlay in local apps | Stated reason |
|---|---|---|
| All user-facing text uses `tr()` | Raw `const char*` | `tr()` means editing `lib/I18n/translations/*.yaml` per app — per-app churn in an upstream file |
| Icons are `UIIcon` enum variants per app | Shelf items carry a generated `freeink::Icon` (Lucide) | An enum growing per app vs 1,735 icons resolved as assets |

This is a genuinely good pattern to note: **the fork deviates from upstream style
specifically where following it would increase the upstream-file conflict
surface.**

## Governance, maintenance and risk

- **Single author.** Bus factor 1.
- **Actively maintained** — pushed 2026-09-02, 65 commits behind upstream, with a
  documented `sync.sh` that computes the conflict set from git rather than a
  hand-kept list (the author notes the hand-kept list "sat at seven entries while
  the truth grew past twenty" — a nice illustration of why the automated version
  exists).
- **Risk:** 65 commits behind at snapshot. In this ecosystem, being behind
  upstream is a **brick-risk signal** rather than a tidiness one, because vendors
  revise hardware silently and upstream carries the fixes.
- OTA points at the fork's own releases; flashing upstream's release onto an S3
  device would be wrong.

## Artifacts held

Retrieved 2026-09-01/02 into `scratch/eink-software/crossplay/`, not vendored
into the repository: `README.md`, `LOCAL_SCOPE.md`, `SCOPE.md`, `.gitmodules`,
`platformio.ini`, `partitions.csv`, `USER_GUIDE.md` (43,621 B),
`THIRD-PARTY-NOTICES.md`. All fetched from
`raw.githubusercontent.com/ma-r-s/crossplay/xteink/`.

## Sources

| ID | What | URL | Retrieved | Establishes |
|---|---|---|---|---|
| CP01 | Repository metadata | `api.github.com/repos/ma-r-s/crossplay` | 2026-09-02 | Identity, parent, licence, branch, dates |
| CP02 | Compare vs upstream | `.../compare/develop...ma-r-s:crossplay:xteink` | 2026-09-02 | 2,391 ahead / 65 behind, +18,096/−862 |
| CP03 | `LOCAL_SCOPE.md` | `raw.githubusercontent.com/ma-r-s/crossplay/xteink/LOCAL_SCOPE.md` | 2026-09-02 | The seam table, quarantine pattern, deviations |
| CP04 | `platformio.ini` | same host | 2026-09-02 | Build environments incl. PaperMono |
| CP05 | `src/apps_local/` listing | `api.github.com/.../contents/src/apps_local?ref=xteink` | 2026-09-02 | 36 entries |
| CP06 | `.gitmodules` | same host | 2026-09-02 | FreeInk SDK submodule and its fork |

## Open questions

- **Are the `papermono` envs real?** Present in `platformio.ini`, absent from
  `LOCAL_SCOPE.md`, and no report of anyone running it on that board exists.
- **True file-change count** is unknown — the compare API caps at 300 files.
- `docs/shelf.md` reportedly references a "previous base" with Sokoban, hinting
  at an earlier rebase off a different fork. **Not corroborated** — recorded, not
  asserted.
- No build was attempted; no binary size, flash usage or runtime figure exists here.

## See also

- **Target hardware:** [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md) · [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md)

- [M5Stack PaperMono device record](../../../devices/m5stack/papermono/README.md) — the board one env targets
- [PaperMono third-party projects](../../../devices/m5stack/papermono/projects-and-community.md) — the wider population, including upstream CrossPoint
