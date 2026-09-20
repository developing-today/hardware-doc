# Software

Records for **software** that runs on, or is used with, the hardware documented
in [`devices/`](../devices/README.md) — firmware, SDKs, graphics libraries, host
tooling and the ecosystems they form.

> **Status: partial.** This tree was started 2026-09-01/02. Only the records
> listed below exist; the directory skeleton anticipates more. Empty directories
> are placeholders, not omissions to be treated as findings.

## Taxonomy

Software is filed by **what it is**, not by what hardware it happens to target —
the same rule the device tree uses for artifacts.

| Category | Definition | Test |
|---|---|---|
| [`libraries/`](libraries/) | Reusable code you link against. Solves one problem, no opinion about your application structure | Could you use two of these together? |
| [`frameworks/`](frameworks/) | Provide the structure; your code fills in the gaps. Inversion of control | Does it call you, or do you call it? |
| [`applications/`](applications/) | Complete, runnable products — firmware images, host applications | Can a user run it without writing code? |
| [`tooling/`](tooling/) | Host-side development and content tooling — flashers, simulators, library managers, converters | Runs on your computer, not the device |
| [`ecosystems/`](ecosystems/) | Cross-cutting analysis of how a family of related projects interrelate: fork networks, dependency graphs, patch portability | Describes relationships, not a single project |
| [`guides/`](guides/) | Task-oriented, project-independent procedures | — |

A project that genuinely spans categories is filed by its **primary** identity
with cross-links, rather than duplicated.

## Records

### Applications

| Record | What | Licence | Status |
|---|---|---|---|
| [**CrossPoint Reader**](applications/crosspoint-reader/README.md) | The ecosystem's centre of gravity — ESP32 e-reader firmware, ★7,538, **1,621 forks**. Ships `papermono` build environments | MIT | written 2026-09-04 |
| [**CrossPlay**](applications/crossplay/README.md) | Personal fork of CrossPoint Reader adding ~26 games and tools alongside the reader. ESP32-S3; targets Xteink X4 Pro, Seeed reTerminal Sticky and **M5Stack PaperMono** | MIT | written 2026-09-02 |

### Frameworks

| Record | What | Licence | Status |
|---|---|---|---|
| [**FreeInk SDK**](frameworks/freeink-sdk/README.md) | Hardware-independent e-paper reader SDK — panel drivers (incl. **SSD1677**), board profiles, capability gates, and **FreeInkBook**, a full EPUB engine. CrossPoint's submodule | MIT | written 2026-09-04 |

### Tooling and plugins

| Record | What |
|---|---|
| [**PaperMono + plugin branch notes**](applications/crosspoint-reader/plugins/papermono-plugin-branch-notes.md) | What is verified vs unknown about running `feat-sd-plugins` on a PaperMono, and the failure modes to expect |
| [**Plugin source snapshots (archived)**](applications/crosspoint-reader/plugins/source-snapshots.ARCHIVED.md) | 18 snapshots, ~176 MB — **15 unlicensed**, one existing on a single Railway host with no git repo and no Wayback mirror |
| [**The Libby path**](applications/crosspoint-reader/plugins/libby-path.md) | **Complete, verified route to reading library loans** — which of three competing plugins works (one), the ByteBooks account nobody mentions, and the four fork catalogues pointing at a dead URL |
| [**SD-card plugins & protected content**](applications/crosspoint-reader/plugins/sd-plugins-and-protected-content.md) | The browser-plugin API, hard limits, store protocol, and the ADEPT client hosted off-GitHub |
| [**CrossPoint plugin systems**](applications/crosspoint-reader/plugins/README.md) | **There are two, and they are nothing alike.** Upstream's is browser JS with no MCU-side execution; a fork ships native C++ ELF modules with a versioned host ABI. Answers whether NFC/LoRa can be a plugin |
| [**Simulator build notes**](tooling/crosspoint-simulator-build-notes.md) | ✅ **`executed-success`** — CrossPoint firmware built and run natively on NixOS with no hardware. The working config, and seven portability problems the sample config does not mention |
| [**Host tooling**](tooling/README.md) | Flasher, simulator, KoSync server, the 400 KB SD recovery flasher, fonts and the pre-FreeInk `community-sdk` — nine tools, two with **no licence file** |
| [**Calibre**](tooling/calibre/README.md) | The content pipeline: device plugins, the Libby/OverDrive path (**3 years stale**), DRM tooling status, and format guidance for e-paper |

### Libraries

| Record | What |
|---|---|
| [**Graphics and display libraries**](libraries/README.md) | LVGL, GxEPD2, u8g2, Adafruit-GFX, epdiy, bb_epaper, JPEGDEC and more — by layer, with the finding that **e-paper panel drivers skew copyleft (GPL/LGPL) while general graphics libraries skew permissive**, which constrains firmware architecture |

### Ecosystems

| Record | What |
|---|---|
| [**Using `M5Unit-NFC` in practice**](ecosystems/crosspoint-freeink/m5unit-nfc-practical.md) | Traps, default timeouts, the `config()`-doesn't-configure gotcha, FeliCa system codes, and **measured** per-stage latencies — plus why "slow NFC" turned out to be antenna coupling |
| [**`M5Unit-NFC` stack overflow**](ecosystems/crosspoint-freeink/m5unit-nfc-overflow.md) | **RF-reachable unbounded write** in the NFC-A emulation listener: the bounds check is real but fed the FIFO length instead of the buffer capacity. Up to ~448 bytes past a 64-byte stack array. Unfixed upstream |
| [**`paper_name_plate` code review**](ecosystems/crosspoint-freeink/paper-name-plate-review.md) | The Rust firmware held to the same standard — **it contains the same logic error**, where Rust turns memory corruption into a panic |
| [**Asian-platform search**](ecosystems/crosspoint-freeink/asian-platform-search.md) | Closing the Japanese/Chinese gap: found a **fourth, MIT-licensed** badge project and a 24-article Qiita corpus on the very library with the overflow |
| [**Plugin architecture**](applications/crosspoint-reader/plugins/plugin-architecture.md) | **How the plugin system actually works** — the two systems, the job queue, the six APIs, and precisely what you can add without firmware vs what forces a fork |
| [**The ContentProtection library**](frameworks/freeink-sdk/contentprotection-library.md) | The DRM engine, read from source: **ADEPT-only (LCP is a keyword, not code)**, per-entry decrypt at read time, expiry enforced by a monotonic clock floor, **private key stored in the clear on the SD card** |
| [**`dtsbytebooks.com` review**](applications/crosspoint-reader/plugins/dtsbytebooks-review.md) | **It is Adobe's ebook DRM platform, now run by Wipro** — `adeactivate.adobe.com` CNAMEs into it. Not a grey-market intermediary |
| [**Plugin source survey**](applications/crosspoint-reader/plugins/plugin-source-survey.md) | `protected-content` and `libby` share **71% of their code**; both use ByteBooks; `sentry.libbyapp.com` is OverDrive's API, not telemetry |
| [**NFC implementation comparison**](ecosystems/crosspoint-freeink/nfc-implementation-comparison.md) | Three independent NFC stacks on one board — use / patch / replace the vendor library. Includes an **RF-reachable stack overflow in `M5Unit-NFC` 0.1.0** and six other defects found via a third party's build-time patch |
| [**New PaperMono projects (2026-09)**](ecosystems/crosspoint-freeink/new-papermono-projects-2026-09.md) | Two-week re-sweep: five new projects incl. **two in Rust**, one implementing **NFC tag emulation**. Independently confirms this KB's pin map on every contested point |
| [**Radios on the PaperMono**](ecosystems/crosspoint-freeink/radios-on-papermono.md) | Can LoRa/NFC be added? **Yes — and not via the SDK.** CrossInk already bypasses the abstraction for ESP-NOW. The four missing pin constants, the RadioLib path, and prototype-vs-upstream effort |
| [**CrossPoint / FreeInk fork network**](ecosystems/crosspoint-freeink/fork-network.md) | The dependency chain, measured divergence for the major forks, why **9 of 14 named forks are invisible to GitHub's `/forks`**, why "commits behind" is a brick-risk signal here, and a generalisable patch-portability classification |

### Not yet written

Still empty, and **not** to be read as "surveyed and found nothing":
`applications/crosspoint-reader/plugins/`, `tooling/calibre/` (and its
`plugins/`), `ecosystems/crosspoint-freeink/`, `libraries/`, and
`software/guides/`. The plugin system, the Calibre integration, the Libby/DRM
path, the fork-divergence analysis and the graphics-library survey are all
**unwritten**.

## Fork links

Where a project is a fork, the parent's directory carries a `forks/`
subdirectory of **relative symlinks** to the fork records, so the relationship is
navigable from either end:

```
applications/crosspoint-reader/forks/crossplay -> ../../crossplay
```

The symlink resolves to a real record today even though the parent's own record
does not yet exist — the fork was documented first because its URL was supplied
directly.

## Relationship to the hardware tree

Software records cross-link device records and vice versa. The live example:
[CrossPlay](applications/crossplay/README.md) carries `[env:papermono]` build
targets, so it appears in the
[M5Stack PaperMono](../devices/m5stack/papermono/projects-and-community.md)
project population.

## Method

Same evidence discipline as the rest of this knowledge base — see
[`.agents/skills/hardware-device-research/SKILL.md`](../.agents/skills/hardware-device-research/SKILL.md).
In particular, for software records:

- **Pin every repository to a full commit SHA.** Branches move.
- Record licence as metadata. `unknown` and "no LICENSE file, therefore all
  rights reserved" are both normal, recordable outcomes — not blockers.
- Label evidence `executed-success` / `reported-working` / `inferred` /
  `not-tested`. **A repository that was read but not built is `inferred`.**
- Fork analysis should measure divergence (`ahead`/`behind`, files touched,
  additions vs deletions) rather than describing it, and should distinguish
  *additive* divergence from *invasive* divergence — they have completely
  different maintenance costs.
