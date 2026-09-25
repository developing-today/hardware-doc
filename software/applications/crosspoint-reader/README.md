# CrossPoint Reader

> Open-source e-reader firmware for ESP32-based devices.
> **`crosspoint-reader/crosspoint-reader`** · branch **`develop`** · MIT · C++ ·
> ★7,538 · **1,621 forks** · created 2025-12-03 · last push 2026-09-04 ·
> ~100 MB · 497 open issues · https://crosspointreader.com
>
> Snapshot **2026-09-02/04**. Nothing was built, flashed or run — no hardware.
> Claims are read from the repository at the cited path and are `inferred` unless
> noted.

**Classification:** **application** — a complete, flashable firmware. It consumes
the [FreeInk SDK](../../frameworks/freeink-sdk/README.md) as a framework.

## Why it is in this knowledge base

**Upstream CrossPoint ships M5Stack PaperMono support.** `platformio.ini` on
`develop` carries `[env:papermono]`, `[env:papermono-gh_release]` and
`[env:papermono-gh_release_rc]`. This is not a fork-only capability — the
7,500-star upstream builds for the board documented at
[`devices/m5stack/papermono`](../../../devices/m5stack/papermono/README.md).

## Device support

Build environments on `develop`, retrieved 2026-09-04:

| Env family | Board | Device |
|---|---|---|
| `default`, `gh_release`, `gh_release_rc`, `slim` | `esp32-c3-devkitm-1` | Xteink X3 / C3-class — **the tightest target, and it sets the memory ceiling** |
| `sticky`, `sticky-gh_release`, `sticky-gh_release_rc` | `esp32-s3-devkitc1-n16r8` | Seeed reTerminal Sticky |
| `x4pro`, `x4pro-gh_release`, `x4pro-gh_release_rc` | `esp32-s3-devkitc1-n16r8` | Xteink X4 Pro |
| `x4c`, `x4c-gh_release` | `esp32-s3-devkitc1-n16r8` | Xteink X4C |
| **`papermono`, `papermono-gh_release`, `papermono-gh_release_rc`** | `esp32-s3-devkitc1-n16r8` | **M5Stack PaperMono** |

Fifteen environments across five device families, both ESP32-C3 and ESP32-S3.
Note every S3 target shares one `esp32-s3-devkitc1-n16r8` board definition —
16 MB flash, 8 MB octal PSRAM — which matches the PaperMono's configuration and
its hard OPI-PSRAM requirement.

## Architecture

Device-specific behaviour lives **behind the SDK boundary**, which `SCOPE.md`
states as policy:

> Device-specific code should live behind the HAL / SDK boundary so the reader
> core stays portable.

```
crosspoint-reader  (application: activities, UI, web server, sync, OTA)
        │  git submodule
        ▼
Free-Ink/freeink-sdk  (framework: panel drivers, board profiles,
                       capability gates, device managers, FreeInkBook)
```

`.gitmodules` on `develop`:

```ini
[submodule "freeink-sdk"]
	path = freeink-sdk
	url = https://github.com/Free-Ink/freeink-sdk.git
	branch = main
```

**The submodule pins a branch, not a commit, in `.gitmodules`** — the actual
pinned SHA lives in the gitlink. Forks that pin a different SDK revision can
therefore behave differently without any fork-owned code differing. See the
[FreeInk record](../../frameworks/freeink-sdk/README.md#who-consumes-it).

Published documentation under `docs/`: `activity-manager.md`, `comparison.md`,
`dictionary.md`, `file-formats.md`, **`fix-bricked-xteink.md`**,
`focus-reading.md`, `hyphenation-trie-format.md`, `i18n.md`, `sd-card-fonts.md`,
`translators.md`, `troubleshooting.md`, `webserver.md`,
`webserver-endpoints.md`, plus `contributing/`.

That `docs/` list is itself informative: a documented **web server with an
endpoint reference**, a **hyphenation trie format**, **i18n with a translators
guide**, and an **unbricking procedure** describe a project considerably past
hobby scope.

## Scope and governance — unusually explicit

`SCOPE.md` is worth reading in full; it is one of the clearer statements of
project boundaries in this ecosystem.

**Mission:** *"a dedicated e-reader should do one thing exceptionally well:
facilitate focused reading."* Explicitly **not** a kitchen-sink firmware, and
explicitly **not Xteink-only** — it is broadening across ESP32 e-reader hardware.

**The acceptance test for new work** is three questions:

1. Does the stock firmware already do this well? (If so, meet or beat that bar.)
2. **Is another popular CrossPoint fork already solving this well?** If yes,
   *defer to that fork* unless it is core reading experience — statistics is the
   named example.
3. Does it improve reading or long-term maintainability? If not, out of scope.

Question 2 is the interesting one. **Upstream explicitly delegates
non-core features to its own fork network** rather than absorbing them. That is a
deliberate ecosystem design, and it explains why 1,621 forks exist and why forks
like [CrossPlay](../../applications/crossplay/README.md) (games) and CrossInk
(stats and reading extras) are *complementary* to upstream rather than
competitive with it. CrossPlay's `LOCAL_SCOPE.md` — "reading stays upstream's to
own… anything that makes reading better belongs upstream, so send it there" — is
the downstream half of the same bargain.

**Current focus** is consolidation, in priority order: DRAM/heap footprint (the
C3 sets the ceiling), flash footprint, code cleanup, then reading experience.
**Some areas are temporarily closed to PRs**, new themes among them, because they
make the multi-device work harder.

## Maintenance signals

| Signal | Value | Reading |
|---|---|---|
| Stars / forks | 7,538 / **1,621** | A ~21 % fork ratio — extremely high. Consistent with a project designed to be forked |
| Open issues | **497** | High in absolute terms; expected at this fork ratio and age |
| Default branch | `develop`, not `main` | Contribute against `develop` |
| Age | created 2025-12-03 | Nine months old at snapshot |
| Activity | pushed 2026-09-04 | Actively developed |
| Repo size | ~100 MB | Large — mostly generated font and hyphenation assets |

**On the "C" language label:** GitHub reports C. A prior analysis in this project
found this is Linguist counting ~294 generated font/hyphenation headers
(~170,000 lines; `hyph-de.trie.h` alone is 12,908) against ~177 hand-written
C++ files (~47,000 lines). **The project is C++20** (`-std=gnu++2a`). Recorded
because the label misleads anyone sizing up the codebase. `reported-working`
from that analysis, not re-derived here.

## Ecosystem

CrossPoint anchors a large fork network. From the earlier survey — **`reported-working`,
not re-verified in this pass**:

| Fork | ★ | Note |
|---|---|---|
| `uxjulia/CrossInk` | ~1,431 | The major second-tier fork; itself heavily forked |
| `yattsu/biscuit` | ~461 | 2nd most starred, but ~596 commits behind and long untouched |
| `franssjz/cpr-vcodex` | ~408 | |
| `trilwu/crosspet` | ~216 | |
| [`ma-r-s/crossplay`](../../applications/crossplay/README.md) | ~15 | Games and tools; **has `papermono` envs** |

Two ecosystem findings worth carrying forward, both from that earlier survey:

- **Being behind upstream is a brick-risk signal here, not a tidiness metric** —
  vendors revise hardware silently, and upstream carries the fixes.
- **Many named forks are "detached"** (`fork: false`, no parent), so GitHub's
  `/forks` listing understates the network substantially.

Companion first-party projects: `crosspoint-simulator` (run firmware without
flashing), `xteink-flasher` (web-serial flasher), `crosspoint-sync` (KoSync
server), `crosspoint-tools`, `escape-hatch` (400-byte SD-card recovery flasher),
`calibre-plugins`.

## Sources

| ID | What | URL | Retrieved |
|---|---|---|---|
| CR01 | Repository metadata | `api.github.com/repos/crosspoint-reader/crosspoint-reader` | 2026-09-04 |
| CR02 | `platformio.ini` — the 15 environments | `raw.githubusercontent.com/crosspoint-reader/crosspoint-reader/develop/platformio.ini` | 2026-09-04 |
| CR03 | `.gitmodules` — the FreeInk submodule | same host | 2026-09-04 |
| CR04 | `SCOPE.md` — mission, acceptance test, closed areas | same host | 2026-09-04 |
| CR05 | `docs/` listing | `api.github.com/.../contents/docs?ref=develop` | 2026-09-04 |
| CR06 | `ROADMAP.md`, `GOVERNANCE.md`, `partitions.csv` | same host | 2026-09-04 |

## Open questions

Three of the four questions raised in the 2026-09-04 pass were **closed on
2026-09-20** by promoting the source-level analysis that this record had been
citing second-hand. It is now in the tree:

- ~~**No commit SHA pinned.**~~ **Closed.** `develop` HEAD is
  **`e6139861a2a8c634aa18c333b7e214ee51a9965c`** (2026-09-01). All code citations in
  [`architecture.md`](architecture.md) resolve against it.
- ~~**The plugin system is not covered by this record.**~~ **Closed, and confirmed.**
  [`plugins/firmware-plugin-internals.md`](plugins/firmware-plugin-internals.md) is
  that prior analysis, now present with file-and-line citations. It holds: `develop`
  contains **zero** plugin files; the implementation lives on two unmerged branches;
  plugins are browser JavaScript plus declarative JSON; **no plugin code executes on
  the MCU**; a grep for `digitalWrite|pinMode|Wire\.|SPI\.|ledcWrite|analogRead`
  across every plugin-path file returns **zero matches**. So **NFC or LoRa cannot be
  a plugin** — it needs a fork or an upstream feature.
- ~~**Binary size, flash/RAM usage and build time: unmeasured.**~~ **Closed —
  measured** (`executed-success`). `pio run -e papermono` succeeded in 287.76 s:
  `firmware.bin` **5 364 128 B**, flash **81.8 %** full, RAM 32.4 %, and **IRAM
  100.0 % exhausted**. See [`architecture.md` §9](architecture.md#9-build-system--verified).
  The `default` (ESP32-C3) env was started and **abandoned before completion**, so
  there are still **no C3 figures** — and the C3 is the tightest target.
- **Whether the `papermono` envs have been run on real hardware by anyone: still
  unknown.** Everything above is compile-and-CI evidence.
  See [`papermono/projects-and-community.md`](../../../devices/m5stack/papermono/projects-and-community.md).

Newly opened by that promotion:

- **Flash and IRAM headroom is a live constraint, not a note.** 81.8 % flash and
  100 % IRAM on the S3 target means a new device or feature may simply not fit.
- **The web server has no authentication at all**, on `develop` as well as the
  plugin branches — see
  [`plugins/firmware-plugin-internals.md` §5](plugins/firmware-plugin-internals.md#5-sandboxing-and-permissions--the-honest-assessment).

## See also

- **Target hardware:** [Xteink X3](../../../devices/xteink/x3/README.md) · [X4](../../../devices/xteink/x4/README.md) · [X4 Pro](../../../devices/xteink/x4-pro/README.md) · [X4 Classic](../../../devices/xteink/x4-classic/README.md) · [S4](../../../devices/xteink/s4/README.md) · [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md)

- [**Architecture**](architecture.md) — the module map, runtime and task model, EPUB
  pipeline, partition table, dependency pins, and the **measured** `papermono` build
  (flash 81.8 %, IRAM 100 %, 173/173 host tests passing)
- [**Firmware plugin internals**](plugins/firmware-plugin-internals.md) — the device
  side of the plugin system: the ten endpoints, their caps, and the unconfined write path
- [**Porting a device**](../../ecosystems/crosspoint-freeink/porting-a-device.md) — what a new board costs in each repository
- [**Source snapshots**](source-snapshots/README.md) — including a fork that **no longer exists upstream**
- [FreeInk SDK](../../frameworks/freeink-sdk/README.md) — the framework beneath it
- [CrossPlay](../crossplay/README.md) · [`forks/`](forks/) — fork records
- [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — a supported target
