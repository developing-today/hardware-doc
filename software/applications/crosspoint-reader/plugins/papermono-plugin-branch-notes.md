# Running the plugin branch on a PaperMono — working notes

> Separate from the Libby/store documentation: this is what is known, and what is
> unknown, about getting **`feat-sd-plugins` firmware onto an M5Stack PaperMono**.
>
> Compiled **2026-09-11**. Branch and source facts are `executed-success`
> (`git grep`/`git show` against the fetched branch). **Nothing was built for
> PaperMono and nothing was flashed** — there is no hardware. Everything
> operational below is `inferred` or `reported-working`.

## The good news

**`feat-sd-plugins` already carries `[env:papermono]`.** Confirmed by
`git show origin/feat-sd-plugins:platformio.ini` — the env list is:

```
default · gh_release · gh_release_rc · slim
sticky · sticky-gh_release · sticky-gh_release_rc
x4pro · x4c · x4c-gh_release · x4pro-gh_release · x4pro-gh_release_rc
papermono        ← present
```

and the file carries the comment `pio run -e papermono -t upload`.

**The branch is not stale.** Against `develop`: **66 ahead, 0 behind**, tip
**2026-09-10**. It contains everything in `develop` plus the plugin work, so it
merges cleanly and is being actively developed.

So in principle this is `pio run -e papermono` on that branch and nothing more.

## What has actually been verified here

| Claim | Status |
|---|---|
| `[env:papermono]` exists on `feat-sd-plugins` | **verified** — read from the branch |
| Branch is 66 ahead / 0 behind `develop` | **verified** — `git rev-list --left-right --count` |
| Plugin API endpoints exist on the branch | **verified** — `/api/plugins`, `/api/relay`, `/api/crypto`, `/api/fetch`, `/api/plugin-fs` in `CrossPointWebServer.cpp` |
| `ContentProtection.cpp` exists (DRM read path) | **verified** — present in `lib/Epub/` |
| **A PaperMono build of this branch compiles** | **NOT verified** |
| **It runs on PaperMono hardware** | **NOT verified — no device** |
| **Anyone has done this** | **no report found** |

The gap between rows 4 and 5 is the whole risk.

## What is known about building CrossPoint generally

A **simulator** build of `develop` was completed successfully on this host —
see [simulator build notes](../../../tooling/crosspoint-simulator-build-notes.md)
— which establishes the toolchain works and documents seven portability fixes.
That was `platform = native`, **not** an ESP32 target, so it does not validate a
PaperMono firmware build.

For a real device build the project ships a **Nix flake** at `nix/flake.nix`
providing an FHS environment with PlatformIO (`pioarduino` fork, v6.1.19) and the
runtime libraries its downloaded ESP32 toolchain needs. On NixOS that is the
supported path:

```bash
cd crosspoint-reader
git checkout feat-sd-plugins
git submodule update --init --recursive        # freeink-sdk
nix develop ./nix                               # or: nix-shell nix/shell.nix
pio run -e papermono
pio run -e papermono -t upload                  # per the file's own comment
```

`PLATFORMIO_CORE_DIR` is set to `$PROJECT_ROOT/.cache/platformio` by the flake,
which keeps the toolchain download inside the checkout.

**None of the above was executed.** It is read from `nix/flake.nix` and the
`platformio.ini` comment.

## Things that will probably bite, and why

Drawn from the PaperMono device record and the SDK, so these are hardware facts
rather than speculation — but their interaction with *this branch* is untested.

**Octal PSRAM is mandatory.** M5GFX aborts display init with
`"M5PaperMono need OPI-PSRAM enabled"`. A misconfigured build presents as a blank
screen on working hardware with one easily-missed log line. Check
`board_build.arduino.memory_type` in the papermono env before blaming hardware.

**The render task stack.** The independent porter of CrossPlay to PaperMono
(`fperuzzo72/crossplay-papermono`, 2026-09-11) needed a commit
*"give the render task the same 16384 stack the x4pro render task uses"*. That is
a different codebase, but it is the same panel size and the same SoC — if the
display crashes or renders partially, stack size is the first thing to check.

**Download mode is not a button.** The M5PM1 power-management MCU owns reset and
the boot straps. Hold the power button ~2 s until the red LED blinks. Standard
esptool auto-reset assumptions may not apply.

**No OTA slot in the stock partition layout.** The vendor's factory image uses a
single ~15 MiB `factory` app with no OTA partition. If the branch's updater
expects OTA, the partition table needs attention — note that
`fperuzzo72` also needed *"publish the release asset its updater asks for"* and
*"point the update check at this fork's releases"*.

**The shared I²C bus is busy.** RTC `0x32`, touch `0x38`, expander `0x4F`, IMU
`0x68`, PMIC `0x6E`, and a charger at `0x75` that is normally gated **off** the
bus. `ciniml/paper_name_plate` needed a commit *"Recover from a flaky I2C bus at
boot: retry IOE1 EPD power-on"* — independent evidence that bus bring-up on this
board needs to be defensive.

## Plugin-specific considerations on this board

**The web server is the plugin runtime.** Plugins are browser JavaScript served
by the device; they need the reader on a network. Use
**File Transfer → Join Network** (not Hotspot) or nothing with an outbound
dependency will work.

**Wi-Fi and the e-paper refresh contend for time and power.** Not measured, and
no power figure exists for this board from any source — but a plugin doing
`fetchToSd` of a multi-megabyte EPUB while the panel refreshes is the obvious
first place to look for instability.

**PSRAM matters here too.** The relay has a 32 KB response cap and `fetch`
segments at 4 MB; on a 8 MB-PSRAM part that is comfortable, but it is worth
knowing the caps exist before diagnosing a stall as a device fault. See
[sd-plugins](sd-plugins-and-protected-content.md).

## Prior art worth reading first

| Project | Why |
|---|---|
| [`fperuzzo72/crossplay-papermono`](https://github.com/fperuzzo72/crossplay-papermono) | **The only known in-progress PaperMono bring-up of a CrossPoint-family firmware.** Branch `papermono-bringup`, started 2026-09-11. Its commits are effectively a checklist |
| [`ciniml/paper_name_plate`](https://github.com/ciniml/paper_name_plate) | Independent Rust firmware; its `DESIGN.md` is the best third-party PaperMono hardware writeup and confirms the pin map |
| `m5stack/M5PaperMono-UserDemo` | Vendor reference — the only artifact exercising NFC, LoRa, IMU, RTC, PDM and the power path together |

## Honest summary

Building `feat-sd-plugins` for PaperMono **looks like a one-line operation and
probably is not**. The env exists, the branch is healthy, and the hardware is
well understood — but nobody has reported doing it, nothing here was compiled for
the target, and the one person publicly porting an adjacent CrossPoint fork to
this board needed several non-obvious fixes (stack size, release assets, updater
URL) within his first day.

Expect a short list of small problems rather than one large one, and check the
display path first.

## Open questions

- **Does `pio run -e papermono` succeed on `feat-sd-plugins` today?** Unknown.
  This is the single cheapest thing anyone with the repo could resolve.
- Does the papermono env on that branch differ from the one on `develop`?
  Not diffed.
- Does the plugin web server behave on this board's Wi-Fi + e-paper combination?
  Untested.
- Is there an OTA partition in the branch's papermono partition table? Not checked.
- Has anyone run *any* CrossPoint build on a PaperMono? **No report found.**

## See also

- [The Libby path](libby-path.md) · [SD-card plugins](sd-plugins-and-protected-content.md)
- [PaperMono device record](../../../../devices/m5stack/papermono/README.md) · [development](../../../../devices/m5stack/papermono/development.md)
- [Simulator build notes](../../../tooling/crosspoint-simulator-build-notes.md) — the one build that *was* completed
- [New PaperMono projects](../../../ecosystems/crosspoint-freeink/new-papermono-projects-2026-09.md)
