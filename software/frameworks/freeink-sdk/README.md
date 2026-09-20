# FreeInk SDK

> A hardware-independent SDK for building e-paper reader firmware.
> **`Free-Ink/freeink-sdk`** · branch `main` · MIT · ★248 · 95 forks ·
> created 2026-06-03 · last push 2026-09-03 · ~3.5 MB · https://freeink.org
>
> Snapshot **2026-09-02/04**. Nothing was built or run — no hardware. Claims are
> read from the repository at the cited path and are `inferred` unless noted.

**Classification:** **framework** — it inverts control. Firmware calls a generic
API; the SDK injects device behaviour. It is not a library you pick features
from, and not an application.

## What it is

FreeInk abstracts every device-specific detail — display controller,
waveforms/LUTs, GPIOs, bus speeds, input style, touch, frontlight, audio — behind
small injectable interfaces. The project's own framing of the design goal:

> Adding a new device means adding **data** (a board profile + a driver config),
> not editing the generic code.

That sentence is the whole architectural thesis, and it is what makes porting
cheap relative to CrossPoint's older approach.

### What ships in it

| Layer | Contents |
|---|---|
| **Panel drivers** | SSD1677, UC8179, UC8253, UC8279, ED2208, IT8951, plus external-library-backed panels |
| **Board profiles + capability gates** | display, input, touch, SD, frontlight, audio, microphone, RTC, sensors, buzzer, LEDs, TLS networking |
| **Device managers** | input, battery, SD, frontlight, LEDs, audio, microphone, RTC, sensors, IMU |
| **FreeInkUI** | optional immediate-mode UI layer — screens, dialogs, settings, keyboards, library views |
| **FreeInkBook** | a complete EPUB engine: streaming parse, CSS, UAX #14 layout with hyphenation/justification/ligatures, page caching with exact position anchors, TTF with per-codepoint fallback, image dithering, links/footnotes. Freestanding, arena-allocated, host-tested |

**FreeInkBook is the surprising part.** A full EPUB layout engine with UAX #14
line breaking and hyphenation, written freestanding and arena-allocated so it can
be host-tested off-device, is a substantial piece of engineering in its own right
— arguably more valuable than the HAL it ships beside.

**Capability gates** matter for porting: a board profile declares what exists, and
firmware branches on capability rather than on device identity. That is why the
same binary logic runs on a board with a frontlight and one without.

### SSD1677 relevance

FreeInk ships an **SSD1677** driver — the controller on both the
[M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) and the
[Waveshare ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md).
See [`components/solomon-systech/ssd1677`](../../../components/solomon-systech/ssd1677/README.md).

## Lineage — and why the "FreeInk came first" reading is wrong

`NOTICE` is unusually candid, and it settles a question that was open in this
knowledge base:

> This project is based in part on, and contains code derived from, the **OpenX4
> E-Paper Community SDK** (`open-x4-epaper/community-sdk`) and its community
> device ports (M5Stack PaperColor, Murphy M3, and the community-sdk-de-link
> ESP32-S3 port). In particular, the **SSD1677 and UC8253 panel initialization
> sequences and waveform LUTs are derived from that work**. Original e-paper
> driver authorship is credited to **CidVonHighwind**.

So the dependency chain is:

```
open-x4-epaper/community-sdk  (MIT, CidVonHighwind et al.)
        │  re-architected, code derived
        ▼
Free-Ink/freeink-sdk  (MIT, created 2026-06-03)
        │  consumed as a git submodule
        ▼
crosspoint-reader/crosspoint-reader  (MIT, created 2025-12-03)
```

**CrossPoint predates FreeInk by six months.** FreeInk is not an upstream
CrossPoint adopted from outside — it is a re-architecture of the SDK CrossPoint
was already using, which CrossPoint then migrated onto. Anyone reading the star
counts (7,538 vs 248) as "big project depends on small project it found" has the
history backwards.

The attribution also means the **panel init sequences and LUTs in FreeInk are
third-party derived work**, which is worth knowing before treating them as
authoritative for a given panel.

## Who consumes it

| Consumer | Relationship |
|---|---|
| [`crosspoint-reader`](../../applications/crosspoint-reader/README.md) | **git submodule** — `.gitmodules` pins `https://github.com/Free-Ink/freeink-sdk.git`, branch `main` |
| [`CrossPlay`](../../applications/crossplay/README.md) | consumes a **fork**, `ma-r-s/freeink-sdk`, branch `x4pro-measured-insets` |
| `Free-Ink/freeink-reader` | the SDK authors' own minimal reference reader |
| 95 forks | see the fork discussion in the CrossPlay record |

**Drop-in compatibility** is claimed with firmware written against the original
`EInkDisplay` / `InputManager` / `BatteryMonitor` / `SDCardManager` / `BoardConfig`
API — "switching to FreeInk is a matter of repointing the library path". That
claim is from the README and is **`reported-working`, not verified here**.

Because forks pin different SDK commits, **a fork's behaviour can differ from
upstream CrossPoint's without a single line of fork-owned code differing** — the
SDK underneath is a different revision. That is a real and easily-missed source
of divergence.

## Funding and governance

Carries an **Open Collective** sponsorship badge (`opencollective.com/freeink`)
and presents as "an open-source collective". That places it between a
single-person project and a company-backed one.

**Bus factor is the open risk.** An earlier analysis in this project found ~74 %
of SDK commits from one author, who is also a CrossPoint co-maintainer and wrote
the migration. That figure is **carried over and not re-verified in this pass** —
treat it as `reported-working` from the prior analysis, not as measured today.

## Porting a new device

The SDK's design intent is that a port is *data*, not code. From the prior
analysis in this project (`reported-working`, measured on real ports):

| Port | Files touched | Lines |
|---|---|---|
| Xteink X4C | 7 | +295 |
| M5Stack PaperS3 | 10 | +397 |
| OnePage (a new MCU) | 8 | +245 |

So a typical port is **7–10 files, 250–400 lines**. Order matters: the SDK port
comes first, then the consuming firmware's build environment — CrossPoint's
`ROADMAP.md` states this explicitly.

**No CI validation** was found for device ports in the SDK, against CrossPoint's
multi-environment build matrix. A port can therefore break without the SDK's own
tests noticing.

## Build and runtime

- C++ (GitHub reports C++; CrossPoint builds it as C++20 / `-std=gnu++2a`).
- No root `platformio.ini` or `library.json` — it ships
  `platformio.sample.ini` and `platformio.crosspoint.sample.ini` instead, i.e.
  it is consumed as a path/submodule dependency rather than a registry package.
- Targets ESP32-C3 and ESP32-S3 in practice.
- Repo ~3.5 MB, 18 open issues.

## Sources

| ID | What | URL | Retrieved |
|---|---|---|---|
| FI01 | Repository metadata | `api.github.com/repos/Free-Ink/freeink-sdk` | 2026-09-04 |
| FI02 | `README.md` | `raw.githubusercontent.com/Free-Ink/freeink-sdk/main/README.md` | 2026-09-02 |
| FI03 | `NOTICE` — lineage and attribution | same host | 2026-09-02 |
| FI04 | `LICENSE` — MIT | same host | 2026-09-02 |
| FI05 | Root tree listing | `api.github.com/.../git/trees/main` | 2026-09-04 |
| FI06 | CrossPoint `.gitmodules` proving the submodule | `raw.githubusercontent.com/crosspoint-reader/crosspoint-reader/develop/.gitmodules` | 2026-09-04 |

## Open questions

- **No commit SHA pinned in this record.** Identity is by branch, which moves.
  A later pass should pin `main`'s HEAD.
- The drop-in-compatibility claim is untested.
- The 74 % single-author concentration is carried over, not re-measured.
- Which board profiles ship today was not enumerated file-by-file.

## See also

- **Devices with records here:** [Xteink X3](../../../devices/xteink/x3/README.md) · [X4](../../../devices/xteink/x4/README.md) · [X4 Pro](../../../devices/xteink/x4-pro/README.md) · [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md)

- [CrossPoint Reader](../../applications/crosspoint-reader/README.md) — the primary consumer
- [CrossPlay](../../applications/crossplay/README.md) — consumes a fork of this SDK
- [`guides/hardware`](../../../guides/hardware/README.md) — e-paper waveforms and bias rails
