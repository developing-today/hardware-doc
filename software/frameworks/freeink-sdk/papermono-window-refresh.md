# PaperMono windowed (rectangular partial) refresh — who has it

> The M5Stack PaperMono panel driver gained RAM-window addressing on **2026-08-26**.
> Whether *your* build has it depends entirely on which `freeink-sdk` commit your
> firmware pins — and the four known consumers do not agree.
>
> Mined **2026-09-20** from the cloned SDK history and the four consumer gitlinks.
> Git archaeology is `executed-success`; panel behaviour is **`not-tested`** — no
> hardware was involved at any point.

Records: [FreeInk SDK](README.md) · [SDK architecture](architecture.md) ·
[porting a device](../../ecosystems/crosspoint-freeink/porting-a-device.md) ·
[M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) ·
[SSD1677](../../../components/solomon-systech/ssd1677/README.md)

## Why this page exists

Two documents promoted into this knowledge base on 2026-09-20 disagreed about
whether upstream FreeInk supports rectangular partial refresh on the PaperMono.
One asserted it did **not**; the other said some of it had landed but did not
check. Both were written 2026-09-02.

**Both were wrong in the same direction.** The feature had merged a week before
either was written. This page records what actually happened, because the
consequence — *a fork can silently lack a panel capability upstream has* — is the
generally useful finding, not the specific commit.

## What landed, and when

| Field | Value |
|---|---|
| Commit | `4327a6d887b1c60b758d13e89ede263fe0da5147` — "Add PaperMono window refresh support" |
| Author | **Henry Li** (`MagicCube`) |
| Authored | 2026-08-26T13:19:03+08:00 |
| Merge commit | `9a6f7d1a1fcdf93bcf4f299353dc99a65e8a6e1d` |
| Pull request | **#58**, branch `MagicCube/codex/papermono-window-refresh` |
| Merged by | Justin Mitchell, 2026-08-26T09:28:53-04:00 |
| Diff | `PaperMonoDriver.cpp` **+139/−4**, `PaperMonoDriver.h` **+7** — 2 files, +142/−4 |

The author of the patch and the author of the third-party demo repo that still
carries it as a local patch are **the same person**. This was not an
un-upstreamed fork improvement; it was a contribution that succeeded.

## What it adds

Four SSD1677 RAM-addressing commands, previously absent from the driver
(`libs/display/FreeInkDisplay/src/driver/PaperMonoDriver.cpp:15-18` at SDK HEAD
`24003795`):

| Constant | Opcode | Role |
|---|---|---|
| `CMD_SET_RAM_X_RANGE` | `0x44` | X window bounds |
| `CMD_SET_RAM_Y_RANGE` | `0x45` | Y window bounds |
| `CMD_SET_RAM_X_COUNTER` | `0x4E` | X address counter |
| `CMD_SET_RAM_Y_COUNTER` | `0x4F` | Y address counter |

Plus the public entry point and the state it needs
(`PaperMonoDriver.h:47, 107-111, 148`):

```cpp
void displayWindow(EpdBus& bus, const uint8_t* fb, const uint8_t* prev,
                   uint16_t x, uint16_t y, uint16_t w, uint16_t h);
void setRamWindow(EpdBus& bus, uint16_t x, uint16_t y, uint16_t w, uint16_t h);
void restoreFullRamWindow(EpdBus& bus);
void writePlaneWindow(EpdBus& bus, uint8_t command, const uint8_t* data, …);
bool _windowBaselineValid = false;
```

**`_windowBaselineValid` is the load-bearing part, and the trap.** A windowed
update only produces a correct image if both panel RAM planes already hold a
known baseline. The driver seeds both full planes once before the first windowed
update and then re-seeds only each window's own rectangle
(`PaperMonoDriver.cpp:833-865`). It invalidates the flag on `begin()`, on
`initController()`, and at three other points where the panel's RAM can no longer
be trusted (`:201, :210, :343, :1074, :1137`), with the comment that a *"window
update must not trust them until they are explicitly re-seeded"* (`:342`).

Anyone implementing windowed refresh on another SSD1677 board should copy that
invalidation discipline rather than just the four opcodes. Writing a window
against a stale baseline is the classic source of e-paper ghosting that
"only appears after a sleep cycle".

## Which consumers actually have it

`git merge-base --is-ancestor 4327a6d <pin>` against each gitlink
(`executed-success`, 2026-09-20):

| Consumer | Pinned `freeink-sdk` commit | Pin date | Windowed refresh? |
|---|---|---|---|
| `freeink-sdk` `main` HEAD | `24003795381a6c23630a26472ae3b06550333e71` | 2026-09-01 | **yes** |
| [`crosspoint-reader`](../../applications/crosspoint-reader/README.md) `develop` | `68425f8eec1246a0be0c0f311540f60ad733fa76` | 2026-08-31 | **yes** |
| `MagicCube/free-ink-on-paper-mono` | `df4a1b7b7be9f8ac75078b9fe6a2ea4e15639039` | 2026-08-24 | **no** — patched locally instead |
| `uxjulia/CrossInk` | `1ff020263cd2202ea79ce3eb811f5ac8489b8cde` | 2026-08-07 | **no** |
| `Free-Ink/freeink-reader` | `1dc8dfc6c689d3c57e49cc4ee0ae156362f0a34b` | 2026-07-08 | **no** |

**Upstream CrossPoint has it. CrossInk does not.** Neither repository contains a
single line of code expressing that difference — it is entirely a function of the
submodule pin. This is the concrete instance of the general hazard recorded in
the [fork network analysis](../../ecosystems/crosspoint-freeink/fork-network.md#finding-6--forks-of-the-sdk-not-just-the-firmware):
*a fork's behaviour can differ from upstream's without any fork-owned code
differing.*

It also means **a PaperMono bug report is not answerable without the reporter's
SDK pin**, not merely their firmware version.

## The local patch is now redundant

`free-ink-on-paper-mono` builds against
`symlink://.cache/freeink-sdk-patched/…` (`platformio.ini:49`), produced by
applying its own patch. Tested 2026-09-20 (`executed-success`):

| Target | `git apply --check` |
|---|---|
| SDK `main` HEAD `24003795` | **fails** — *"patch does not apply"*: the code is already present |
| SDK `df4a1b7b` (that repo's own pin) | **succeeds** |

So the patch is not a divergence from upstream; it is an artefact of a pin that
is **two days older than its own author's merge**. Bumping the submodule to any
SDK commit at or after `4327a6d` makes the patch and the `.cache` build step
unnecessary.

## Artifact

| File | Bytes | SHA-256 |
|---|---|---|
| [`artifacts/freeink-paper-mono-window-refresh.patch`](artifacts/freeink-paper-mono-window-refresh.patch) | 10 747 | `0bebaef2334e938e45ccd5a7ec196157ea97ee2d04ac5e2822c29e5b1341b7ec` |

Retained in the repository despite being redundant against upstream, because it
is the **only self-contained expression of this change as a patch** and its
source repository has **no `LICENSE` file** (GitHub API `license: null`) and a
single author — the at-risk profile that
[cost this project `crosspoint-reader-lua`](../../applications/crosspoint-reader/source-snapshots/ideo2004-afk_crosspoint-reader-lua.ARCHIVED.md).
Licence **unknown**, redistribution status **unknown**, disposition
**repository**. Read it for technique; do not assume a licence grant.

- Source: `MagicCube/free-ink-on-paper-mono`, `patches/freeink-paper-mono-window-refresh.patch`, at repo HEAD `34cc879427d5fc0b35f6af5084d4e7a003457665` (2026-08-27), retrieved 2026-09-01, re-verified reachable 2026-09-20.
- Equivalent upstream, MIT-licensed: `git show 4327a6d` in `Free-Ink/freeink-sdk` — **prefer this** for any reuse.

## Limits

- **No hardware.** Nothing here was rendered on a panel. That the code exists and
  merges is established; that it refreshes correctly is `not-tested`.
- Whether the merged version is byte-identical in behaviour to the local patch was
  **not** established — only that they touch the same two files with near-identical
  size (+142/−4 upstream vs 144 added lines locally) and that the patch will not
  re-apply. A hunk-level diff was not performed.
- Ghosting, refresh latency and LUT quality for windowed updates are unmeasured.
