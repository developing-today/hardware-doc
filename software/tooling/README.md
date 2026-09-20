# CrossPoint / Xteink host tooling

> The companion tools around the firmware: flashers, a simulator, a sync server,
> a web toolbox and asset repositories. All host-side or browser-side.
>
> Snapshot **2026-09-04**. Repository facts `executed-success` (GitHub API).
> **Nothing was installed, built or run** — no hardware, no browser session.
> Capability descriptions are `inferred` from repository metadata and READMEs.

**Classification:** tooling — runs on your computer or in a browser, not on the
device. For the firmware itself see
[CrossPoint Reader](../applications/crosspoint-reader/README.md).

## The set

| Tool | ★ | Language | Licence | HEAD | Last push | What it does |
|---|---|---|---|---|---|---|
| [`xteink-flasher`](https://github.com/crosspoint-reader/xteink-flasher) | 136 | TypeScript | MIT | `2b09cb43` | 2026-05-20 | **Browser-based flasher** (Web Serial) |
| [`xtlibre`](https://github.com/shakogegia/xtlibre) | 81 | TypeScript | MIT | `9d2c47a3` | 2026-04-07 | Self-hosted companion app — *third-party* |
| [`crosspoint-simulator`](https://github.com/crosspoint-reader/crosspoint-simulator) | 55 | C++ | MIT | `c55f168b` | 2026-09-02 | **Run the firmware without a device** |
| [`crosspoint-sync`](https://github.com/crosspoint-reader/crosspoint-sync) | 42 | TypeScript | MIT | `a986b3ce` | 2026-08-19 | Lightweight **KoSync** server for progress/stats |
| [`crosspoint-tools`](https://github.com/crosspoint-reader/crosspoint-tools) | 35 | JavaScript | MIT | `a3f0abf6` | 2026-09-01 | Website and browser tools |
| [`crosspoint-fonts`](https://github.com/crosspoint-reader/crosspoint-fonts) | 21 | — | **none** | `e435b40d` | 2026-08-20 | Prebuilt device fonts |
| [`Murphy`](https://github.com/crosspoint-reader/Murphy) | 15 | HTML | MIT | `78ef80e6` | 2026-08-13 | Firmware dumps + support docs for Hamgeek M3/M4 |
| [`escape-hatch`](https://github.com/crosspoint-reader/escape-hatch) | 10 | C++ | **none** | `90841adf` | 2026-08-22 | **400 kB SD-card recovery flasher** |
| [`community-sdk`](https://github.com/crosspoint-reader/community-sdk) | 5 | C++ | MIT | `198ad267` | 2026-06-24 | The pre-FreeInk SDK — historical |

All but two are MIT. `crosspoint-fonts` and **`escape-hatch` carry no licence
file**, which for a recovery tool people are told to use when their device is
bricked is an unfortunate gap — it is all-rights-reserved by default.

## The two flashers, and why both exist

**`xteink-flasher`** is the normal path: a browser page using **Web Serial** to
talk to the device over USB. No toolchain, no `esptool` install, no driver
wrangling beyond the OS recognising the port. Web Serial means **Chrome or Edge
only** — Firefox and Safari have declined to implement it — and it needs HTTPS or
localhost.

**`escape-hatch`** exists for when that cannot work. It is a *firmware* — a
minimal SD-card flasher, deliberately **400 kB** — that you flash onto the device
so it can then flash something else from an SD card. Its reason to exist is the
ecosystem's own recovery problem: an ecosystem finding recorded elsewhere in this
knowledge base is that **"locked" devices block USB flashing but still accept
SD-card `update.bin`**. `escape-hatch` is the lever for that case.

Its size is the design: at 400 kB it fits where a full firmware will not.

Upstream also ships `docs/fix-bricked-xteink.md`. **A project with a dedicated
unbricking document, a recovery firmware and a locked-device workaround is
telling you something about its risk profile** — see
[`guides/serial-access`](../../guides/serial-access/README.md) for the host side
of avoiding that situation.

## The simulator — the most underrated tool here

`crosspoint-simulator` (★55, C++, MIT, actively pushed 2026-09-02) runs the
firmware on a desktop. `uxjulia/crossink-simulator` is the equivalent for that
fork, using SDL.

Why it matters more than its star count suggests:

- **No hardware needed** to develop UI, layout, typography or EPUB rendering —
  which is most of what this firmware does.
- **No flash cycles**, so no wear and no bricking risk during iteration.
- CrossPlay's fork ships `platformio.sim.ini` as a tracked file precisely so
  every checkout can run the simulator, and it also produces a **WASM browser
  build** of the real firmware.

For anyone evaluating this ecosystem without buying a device — which describes
this knowledge base's own position — the simulator is the only route to
first-hand observation.

> ✅ **It has now been built and run.** CrossPoint firmware compiles and executes
> natively on NixOS/x86-64 — `[SUCCESS]`, a 6.6 MB binary, running headless under
> `SDL_VIDEODRIVER=dummy`. Seven portability problems had to be solved, three of
> which are general toolchain bugs rather than NixOS quirks (a **C23 `bool`**
> breakage in QRCode, an **`#include_next` ordering** assumption, and missing
> defines/`-lcrypto` in the sample config).
>
> Full working configuration, commands and findings:
> **[Building the simulator on NixOS](crosspoint-simulator-build-notes.md)**.

## Sync — and a good standards decision

`crosspoint-sync` is a *"Lightweight KoSync Server for Syncing
Crosspoint/CrossInk stats & progress"*.

**KoSync is KOReader's sync protocol.** Rather than inventing a format, the
ecosystem implemented an existing one — so a CrossPoint device can share reading
position with KOReader clients and with any existing KoSync server. That is a
better decision than it looks: it means progress sync is not locked to one
firmware's lifetime.

Note it explicitly serves **CrossPoint *and* CrossInk**, which fits the
[fork network's](../ecosystems/crosspoint-freeink/fork-network.md) division of
labour — upstream defers stats to forks, and shared infrastructure serves both.

`xtlibre` (★81, third-party, MIT) is a self-hosted companion app for Xteink and
CrossPoint readers. **Last pushed 2026-04-07** — the least current tool in this
set, five months stale at snapshot.

## Assets and hardware support

- **`crosspoint-fonts`** — prebuilt fonts for the device. Fonts live on the SD
  card, not in the book; see upstream's `docs/sd-card-fonts.md`. `uxjulia` maintains
  parallel `crossink-fonts` and `crossink-dictionaries` repositories.
- **`Murphy`** — firmware dumps and initial support documentation for the
  **Hamgeek M3/M4**. Evidence that this ecosystem's device reach extends past
  Xteink hardware, consistent with upstream's stated "not Xteink-only" scope.
- **`community-sdk`** — the **pre-FreeInk SDK**, created by Dave Allie the day
  before CrossPoint's public release. Now historical: FreeInk's `NOTICE` credits
  it as the work FreeInk was derived from. Kept for lineage; not a current
  dependency. See [FreeInk SDK](../frameworks/freeink-sdk/README.md).

## Practical notes

**Flashing, in order of preference:** `xteink-flasher` in Chrome/Edge → `esptool`
if you have a toolchain → `escape-hatch` + SD card if USB is blocked or the
device is locked.

**Before flashing anything, save a full flash dump.** An ecosystem finding
recorded in this knowledge base is that most "bricks" are a short restore *if a
dump exists* — and locked devices cannot produce one, which is exactly when you
most want it.

**Serial permissions** are a separate problem from any of these tools and are
covered in [`guides/serial-access`](../../guides/serial-access/README.md).
`xteink-flasher` sidesteps Linux group membership entirely by using Web Serial,
which is a genuine advantage of the browser approach.

## Sources

All retrieved **2026-09-04** from the GitHub REST API, authenticated. Repository
metadata and HEAD commit for each of the nine repositories tabulated above; SHAs
are given in the table and are the identity to cite, since branches move.

## Open questions

- **Nothing was installed, built or run.** No flasher was used, no simulator
  started, no sync server deployed.
- `xteink-flasher`'s device coverage (which boards, which chip families) was not
  read from its source.
- Whether `crosspoint-simulator` supports the **PaperMono** board profile is
  unknown, and would determine whether this knowledge base could observe that
  device's firmware behaviour without hardware.
- `escape-hatch`'s licence absence should be raised upstream; it is a recovery
  tool users are directed to.
- No tool here was checked for PaperMono-specific support.

## See also

- [CrossPoint Reader](../applications/crosspoint-reader/README.md) · [plugin systems](../applications/crosspoint-reader/plugins/README.md)
- [Calibre and the content pipeline](calibre/README.md)
- [Serial device access](../../guides/serial-access/README.md)
- **Devices these tools flash:** [Xteink X3](../../devices/xteink/x3/README.md) · [X4](../../devices/xteink/x4/README.md) · [X4 Pro](../../devices/xteink/x4-pro/README.md)
- [Fork network](../ecosystems/crosspoint-freeink/fork-network.md)
