# Dependency truth: CrossPoint Reader ↔ FreeInk SDK

**Research date:** 2026-09-02. All claims below are from cloned source trees at the
SHAs recorded in [`repo-identity.json`](repo-identity.json). Evidence labels:
`executed-success` = I ran it; `inferred` = read from source/history; `not-tested` =
asserted by docs, not verified. **No claim here is hardware-verified** — I have no
e-reader.

---

## The answer

**Yes — `crosspoint-reader` genuinely depends on `freeink-sdk` today. The dependency is
real, load-bearing, and pinned. But the prior assumption's *implied history* is wrong in
two ways:**

1. **FreeInk SDK is not an independent upstream that CrossPoint adopted.** It is a
   June-2026 re-architecture of the SDK CrossPoint was *already* using
   (`open-x4-epaper/community-sdk`), created by a CrossPoint co-maintainer, and adopted
   by CrossPoint three weeks later. CrossPoint is the SDK's anchor consumer, not a
   downstream discoverer.
2. **The "CrossPoint is C, FreeInk is C++" hint is a GitHub Linguist artifact, not a real
   language boundary.** Both are C++. There is no C/C++ interop story to explain.

The fork claim in the assumption is correct: **CrossInk is a direct fork of
crosspoint-reader** (`uxjulia/CrossInk`, GitHub API `fork: true`,
`parent: crosspoint-reader/crosspoint-reader`).

**Direction:** `crosspoint-reader` → *depends on* → `freeink-sdk`. Not the reverse.
`freeink-sdk` has **no** build-time or runtime dependency on crosspoint-reader
(`freeink-sdk/README.md:53-54`: "It is **not a fork** and has no build-time or runtime
dependency on the upstream repository").

---

## Evidence 1 — the submodule is declared and pinned

`crosspoint-reader/.gitmodules` (at HEAD `e6139861`, branch `develop`):

```
[submodule "freeink-sdk"]
	path = freeink-sdk
	url = https://github.com/Free-Ink/freeink-sdk.git
	branch = main
```

Gitlink at HEAD (`git ls-tree HEAD freeink-sdk`):

```
160000 commit 68425f8eec1246a0be0c0f311540f60ad733fa76	freeink-sdk
```

That SDK commit is `2026-08-31T12:44:26-04:00`, **7 commits behind `freeink-sdk/main`** at
the time of research — i.e. actively tracked, not abandoned. (`inferred`, from
`git rev-list --count 68425f8e..HEAD` in the SDK clone.)

## Evidence 2 — the build actually consumes it (this is the load-bearing part)

A `.gitmodules` entry alone proves nothing. The PlatformIO manifest wires **14 SDK
libraries** directly into the link, via `symlink://` paths into the submodule —
`crosspoint-reader/platformio.ini:83-97`:

```ini
lib_deps =
  BatteryMonitor=symlink://freeink-sdk/libs/hardware/BatteryMonitor
  InputManager=symlink://freeink-sdk/libs/hardware/InputManager
  EInkDisplay=symlink://freeink-sdk/libs/display/FreeInkDisplay
  SDCardManager=symlink://freeink-sdk/libs/hardware/SDCardManager
  UsbMassStorage=symlink://freeink-sdk/libs/hardware/UsbMassStorage
  BoardConfig=symlink://freeink-sdk/libs/hardware/BoardConfig
  XteinkDetect=symlink://freeink-sdk/libs/hardware/XteinkDetect
  PowerManager=symlink://freeink-sdk/libs/hardware/PowerManager
  FrontlightManager=symlink://freeink-sdk/libs/hardware/FrontlightManager
  Rtc=symlink://freeink-sdk/libs/hardware/Rtc
  Imu=symlink://freeink-sdk/libs/hardware/Imu
  SecureNet=symlink://freeink-sdk/libs/network/SecureNet
  FreeInkUI=symlink://freeink-sdk/libs/ui/FreeInkUI
  Icons=symlink://freeink-sdk/libs/assets/Icons
```

This is display, input, storage, battery, power, frontlight, RTC, IMU, USB-MSC, TLS
networking, UI and icons — **the entire hardware layer**. CrossPoint cannot build without
it.

Further, the device-selection macros in every build env are *SDK* macros, not CrossPoint
macros — `platformio.ini:163-164, 254, 280, 357`:

```
-DFREEINK_DEVICE_X4=1  -DFREEINK_DEVICE_X3=1
-DFREEINK_DEVICE_X4PRO=1
-DFREEINK_DEVICE_X4CLASSIC=1
-DFREEINK_DEVICE_PAPERMONO=1
```

Those are consumed by `freeink-sdk/libs/hardware/BoardConfig/include/BoardConfig.h:33-97`.
CrossPoint's own HAL is a thin wrapper over the SDK: `crosspoint-reader/lib/hal/`
(`HalDisplay`, `HalGPIO`, `HalStorage`, `HalPowerManager`, `HalFrontlight`, `HalClock`,
`HalSystem`, `HalTiltSensor` — 16 files), described in
`docs/contributing/architecture.md:199` as "hardware abstraction wrappers around
freeink-sdk".

**Independently corroborated:** I configured and ran CrossPoint's host-side unit suite
(173/173 pass, `executed-success`) — see [CrossPoint architecture](../../applications/crosspoint-reader/architecture.md) —
and the firmware build outcome is recorded there too.

## Evidence 3 — the real chronology (refutes the "FreeInk came first" reading)

| Date | Event | Source |
|---|---|---|
| 2025-12-02 | `open-x4-epaper/community-sdk` created by **Dave Allie** | first commit `fd8b341` "Initial community-sdk structure" |
| 2025-12-03 | `crosspoint-reader` public release by **Dave Allie**, submodule = `open-x4-sdk` | `.gitmodules` @ `2ccdbeec` "Public release" |
| 2026-05-06 | CrossPoint repoints submodule to its **own fork** `crosspoint-reader/community-sdk` | `4ea938b7` "chore: Update SDK to fork in CrossPoint org (#1836)", Zach Nelson |
| **2026-06-02/03** | **`Free-Ink/freeink-sdk` created by Justin Mitchell** | `8dff913` "Initial commit"; `2bb2043` "Rebuild as FreeInk SDK" |
| 2026-06-27 | CrossPoint migrates submodule to `freeink-sdk` | `ebebc6f2` "chore: migrate from open-x4-sdk to freeink-sdk (#2449)" |

`crosspoint-reader` predates `freeink-sdk` by **six months**. The GitHub API confirms
creation dates: `crosspoint-reader` `2025-12-03T11:01:12Z`, `freeink-sdk`
`2026-06-03T01:24:39Z`.

**They are not independent parallel projects, and FreeInk is not a pre-existing upstream.**
They are sequential links in one lineage:

```
open-x4-epaper/community-sdk  (Dave Allie, 2025-12-02, MIT)
        │  forked 2026-05
        ▼
crosspoint-reader/community-sdk  (fork; GitHub API fork:true, parent:open-x4-epaper/community-sdk)
        │  code derived, history NOT inherited
        ▼
Free-Ink/freeink-sdk  (Justin Mitchell, 2026-06-02, MIT)
        ▲
        │ submodule, 14 lib_deps
crosspoint-reader ──────────────┘
        │ fork
        ▼
uxjulia/CrossInk, ma-r-s/crossplay
```

## Evidence 4 — "derived from", but a fresh history

`freeink-sdk` is a **code-level derivative with a clean git history**, not a git fork.
I verified there are **zero shared commit SHAs** between `freeink-sdk` and
`community-sdk` (`comm -12` over both `rev-list --all` sets returned empty) — and GitHub
reports `freeink-sdk` `fork: false`.

The derivation is disclosed explicitly. `freeink-sdk/NOTICE:10-15`:

> This project is based in part on, and contains code derived from, the OpenX4
> E-Paper Community SDK (https://github.com/open-x4-epaper/community-sdk) and its
> community device ports (M5Stack PaperColor, Murphy M3, and the
> community-sdk-de-link ESP32-S3 port). In particular, the SSD1677 and UC8253
> panel initialization sequences and waveform LUTs are derived from that work.
> Original e-paper driver authorship is credited to CidVonHighwind.

And `freeink-sdk/README.md:36-43, 50-56`:

> FreeInk is an MIT-licensed **re-architecture derived from** the **OpenX4 E-Paper
> Community SDK** … What FreeInk changes is the **structure**, not the panel work …
> It is **not a fork** and has no build-time or runtime dependency on the upstream
> repository.

An early SDK commit does the transplant literally: `3a6e6bb` "Replace UC8253 X3 waveform
LUTs with community-sdk banks" (2026-06-02).

## Evidence 5 — the same person is on both sides

**Justin Mitchell** authored `freeink-sdk`'s "Initial commit" (`8dff913`), is its dominant
committer (**148 of the last 200 commits, 74%**), authored CrossPoint's migration commit
`ebebc6f2`, is CrossPoint's **#2 committer** over its last 200 commits (37), and authored
CrossPoint's PaperMono/X4Pro device-support PR `bbca4886`. He also owns
`Free-Ink/freeink-reader` (`LICENSE`: "Copyright (c) 2026 Justin Mitchell").

The migration PR body (`ebebc6f2`) is candid that the swap was a no-op at the code level:

> Out of the box there are NO changes needed in the firmware to support this swap, it all
> magically works as is.

That is only possible because FreeInk deliberately preserved the API of the SDK CrossPoint
was already on — further evidence of continuity rather than adoption of a foreign library.

## Evidence 6 — the C-vs-C++ hint is an artifact

GitHub labels `crosspoint-reader` as **C**. The source says otherwise (`tokei`,
`executed-success`, excluding `.git` and the submodule):

| Language | Files | Code lines |
|---|---|---|
| C Header | 294 | 169,708 |
| **C++** | **177** | **46,774** |
| C | 10 | 17,858 |
| Python | 26 | 7,934 |

The `C Header` mass is **generated data tables**, not C code — e.g.
`lib/Epub/Epub/hyphenation/generated/hyph-de.trie.h` (12,908 lines) and ~40 font tables
under `lib/EpdFont/builtinFonts/` (`notoserif_18_bolditalic.h`, 4,817 lines, etc.).
Linguist counts these as C and they dominate by volume.

The build is unambiguously C++20: `platformio.ini:35` `-std=gnu++2a`, `:62`
`-fno-exceptions`, `:65` `build_unflags = -std=gnu++11`. The SDK uses the identical flags
(`freeink-sdk/platformio.sample.ini:21`).

**Conflict recorded:** the language metadata on GitHub contradicts the source tree. Trust
the source.

---

## Secondary relationships (verified)

| Repo | Relationship | Evidence |
|---|---|---|
| **`uxjulia/CrossInk`** | Hard fork of `crosspoint-reader`. Carries the same `freeink-sdk` submodule, but pinned to a **different, older** SDK commit `1ff02026` (vs CrossPoint's `68425f8e`) → the fork has diverged on SDK version. | GitHub API `fork:true, parent:crosspoint-reader/crosspoint-reader`; `CrossInk/.gitmodules`; `git ls-tree HEAD freeink-sdk` |
| **`crosspoint-reader/community-sdk`** | The *old* SDK, now vestigial. A fork of `open-x4-epaper/community-sdk`, last pushed 2026-06-24, 5★. Superseded by the FreeInk migration three days later. | GitHub API `fork:true, parent:open-x4-epaper/community-sdk`; HEAD `198ad267` |
| **`Free-Ink/freeink-reader`** | Reference/demo consumer of the SDK by its own author. 4★, 52 KB, one C++ file of 2,766 lines. Not a product. | `freeink-reader/.gitmodules`; `tokei` |
| **`MagicCube/free-ink-on-paper-mono`** | Independent third-party FreeInk consumer on M5Stack PaperMono. **Not** affiliated with CrossPoint. Uses 10 SDK libs; **patches the SDK** (`patches/freeink-paper-mono-window-refresh.patch`). | `free-ink-on-paper-mono/platformio.ini:47-57` |
| **`mohitagw15856/Inkkit`** | Self-declared "shared device-layer HAL for freeink-sdk". **Adoption is zero** — grep for `inkkit` across `crosspoint-reader/{src,lib,platformio.ini}` and `freeink-sdk/{libs,README.md}` returns nothing. 1★, 9 commits, 3 authors (one of which is "Claude"). It is a personal wrapper for the author's own two apps, not an ecosystem component. | `git log --format=%an`; grep (`executed-success`) |
| **`ideo2004-afk/crosspoint-reader-lua`** | A CrossPoint fork **still on the pre-FreeInk `open-x4-sdk`** (`.gitmodules` → `open-x4-epaper/community-sdk`). Its submodule pin `a75faa88` is **dangling** — `git submodule update` fails with `upload-pack: not our ref`. Last pushed 2026-04-03; branch `crosspoint-flow`. Stale. | `crosspoint-reader-lua/.gitmodules`; submodule init failure (`executed-success`) |

### Note on `crosspoint-reader-lua` and the "scripting" hint

The repo name suggests Lua scripting, but **no Lua interpreter is vendored** in
`crosspoint-reader` at HEAD or on any of its 25 remote branches — a tree-wide grep for
`lua.h`, `wasm3`, `quickjs`, `duk_config`, `berry` and `mruby` across `*.h/*.cpp/*.c/*.ini`
matched only `freeink-sdk/libs/book/FreeInkBook/third_party/expat/internal.h` (a false
positive on "…evalua…"). The fork predates the FreeInk migration and is stale. It is not
evidence of a scripting engine in upstream CrossPoint. See
[firmware plugin internals](../../applications/crosspoint-reader/plugins/firmware-plugin-internals.md).

Separately, a sibling fork `ma-r-s/crossplay` carries the GitHub topic `webassembly` — if a
WASM runtime exists anywhere in this family it is **there, in a fork**, not upstream. I did
not clone or verify it (outside the assigned repo set). `inferred`, from GitHub API metadata
only.

---

## What to correct in the knowledge base

- ❌ "freeink is used by crosspoint-reader, which is forked by crossplay/crossink" —
  half right. The fork half is correct. The dependency half is correct *as a present-tense
  fact* but wrong if it implies FreeInk is a pre-existing external upstream.
- ✅ Replace with: *CrossPoint Reader (Dec 2025) and its SDK were created together by the
  same author. The SDK was re-architected and rebranded as FreeInk SDK in June 2026 by a
  CrossPoint co-maintainer; CrossPoint adopted it three weeks later and remains its anchor
  consumer. CrossInk and crossplay are forks of CrossPoint and inherit the SDK submodule.*
- ❌ "CrossPoint is C, FreeInk SDK is C++" — both are C++20. The C label is Linguist
  miscounting generated font/hyphenation tables.
