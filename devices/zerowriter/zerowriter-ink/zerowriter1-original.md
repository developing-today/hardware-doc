# ZeroWriter 1 — the original Raspberry Pi typewriter

> The DIY project that started everything: a Pi Zero 2 W, a Waveshare 4.2" e-paper panel and a 40 % keyboard.
> **MIT licence** · 367★ · commit `e476d056` (2026-05-19) · snapshot **2026-08-24**
> Preserved at [`artifacts/source-snapshots/zerowriter1/`](artifacts/source-snapshots/zerowriter1/)

This is the predecessor to [ZeroWriter Ink](README.md) — a *build-it-yourself guide*, not a product. It is documented here because it explains the lineage, and because the display-driver work in it is directly ancestral to the Ink's headline feature.

## What it is

| | |
|---|---|
| Compute | **Raspberry Pi Zero 2 W** ("Don't use an original Zero. The extra power is very useful.") |
| Display | **Waveshare 4.2" e-Paper** |
| Keyboard | Any USB keyboard; the reference build uses a **Vortex Core 40 %** |
| OS | **Debian Bookworm Lite 32-bit** |
| Language | Python, on top of Waveshare's example code |
| Licence | **MIT** (project); Waveshare driver code remains Waveshare's |
| Inspiration | Credited to [penkesu.computer](https://penkesu.computer/) |

### Cost

| Build | Parts | Total |
|---|---|---|
| **Minimum** | Pi Zero 2 W + SD ($15), Waveshare 4.2" ($30), any USB keyboard | **~$45 USD** |
| **Full** | + Vortex Core 40 % ($90), M2/M2.5 hardware ($5), right-angle micro-USB ($10), 2×20 header ($8), micro-USB→USB ($5), printed STLs ($20), **Game Boy SP hinges** ($2), external battery | **~$200 USD** |

The Game Boy SP hinges are a nice detail — a clamshell built from salvageable console parts, and arguably the ancestor of the [Zerowriter Fold](../zerowriter-fold/README.md)'s folding enclosure.

## ⚠ Two compatibility traps

These are the project's own warnings, and both will silently break a build.

### 1. The Waveshare panel revision determines which branch you need

> Check the back of your 4.2" waveshare e-Paper. **If it says Rev2.2 or has a V2 sticker**, you'll want to use [the `waveshare_2.2` branch]. The main branches **won't function properly** on these displays.
>
> If it says **Rev2.1**, you'll want [`main_full`].

| Panel marking | Branch | Notes |
|---|---|---|
| **Rev2.2 / V2 sticker** | `waveshare_2.2` | "likely to be the default branch going forward" |
| **Rev2.1** | `main_full` | more features |
| — | `main` | **discontinued**, kept only as a minimal codebase |

Only the **preserved snapshot's default branch** is captured here. If you are building this, check the branch against your panel.

### 2. Raspberry Pi OS changed GPIO support

> important update: **raspberry pi OS has changed GPIO support**, so it is important you use **archived versions of the OS**

Pointing at [issue #26](https://github.com/zerowriter/zerowriter1/issues/26#issuecomment-2466903737). Modern Raspberry Pi OS moved from the legacy GPIO interface, breaking the Waveshare drivers. **A fresh install of current Pi OS will not work** — you need an archived image. This is the single most likely reason a new build of this project fails today.

## The fast-refresh lineage

The project's own description of how it drives the panel:

> `epd.init()` clears the screen using **slow look-up tables** — this prevents artifacting
>
> `epd.init_Partial()` runs a **faster update using modified LUT** ([Ben Krasnow](https://hackaday.com/2017/10/31/ben-krasnow-hacks-e-paper-for-fastest-refresh-rate/)) — important to note **this only works with the 4.2" v1 waveshare display**

This matters for understanding the Ink. The original ZeroWriter's responsiveness came from **hand-modified e-paper look-up tables**, a technique popularised by Ben Krasnow's 2017 Hackaday work. The same obsession — *"e-paper doesn't have to be slow"* — later produced the Ink's [200 ms → 100 ms optimisation](development-history.md#the-e-paper-latency-problem-and-how-it-was-solved) with bitbank2.

So the through-line across both generations is **e-paper latency engineering**, not the enclosure or the keyboard.

The project is candid about the risk:

> Use this modified code at your own risk. **The modified driver may cause damage to your display.** Don't blame me.

Driving e-paper with non-vendor waveforms genuinely can damage a panel — the warning is not boilerplate. The modifications to Waveshare's driver are documented separately in [`zerowriter1-epaper-driver-notes.md`](zerowriter1-epaper-driver-notes.md).

## Setup

`how-to-setup-your-pi` is a beginner-oriented, step-by-step guide — flash Bookworm Lite with the Pi Imager, preconfigure Wi-Fi and SSH, then configure headless over SSH. It is written with unusual self-awareness:

> I'm not a Linux guy, and it can be frustrating trying to get started in that world because — frankly — a lot of Linux users are the worst. I'll try to make this clear and approachable for anyone!

That tone is worth noting because it is the same philosophy the Ink is sold on: a tool for writers first, hackers second.

## Repository contents

```
zerowriter1/                          MIT, commit e476d056
├── README.md                         branch guidance, compatibility warnings, theory of operation
├── componentslist                    the BOM above
├── how-to-setup-your-pi              step-by-step headless Pi setup
├── sampleconfig                      example configuration
├── zerowriter_stl_apr13.zip          enclosure STLs (April revision)
├── zerowriter_stl_mar24.zip          enclosure STLs (March revision)
└── e-Paper/                          modified Waveshare drivers — ARCHIVED, see the placeholder
```

The application lives at `e-Paper/RaspberryPiJetsonNano/python/examples/main.py`, built on Waveshare's example code.

## Relationship to ZeroWriter Ink

| | **ZeroWriter 1** | **ZeroWriter Ink** |
|---|---|---|
| Compute | Raspberry Pi Zero 2 W (Linux) | ESP32-WROVER (bare metal, Arduino) ×2 |
| Display | Waveshare 4.2", SPI | Inkplate 5 Gen 2, 1280×720 parallel |
| Keyboard | Any USB keyboard | Custom ESP32 matrix board |
| Enclosure | Self-printed, Game Boy SP hinges | Injection-adjacent 3D print, professionally designed |
| Boot | Linux boot time | Instant-on |
| Licence | **MIT** | GPL-3.0 (hardware + keyboard fw); main app unpublished |
| Form | DIY guide | Finished product |
| Cost | $45–200 self-built | $285 |

They share a **name, a philosophy and an obsession with refresh latency** — but no code, no processor family and no display technology. Treat them as separate projects.

The font carried over: the Ink ported **Courier Prime** from the Pi project ([development history](development-history.md#the-font-system)).

## Status

Still maintained — last pushed **2026-05-19**, and the README carries a 2024-era GPIO warning, so the author is still fielding issues. But the main branch is explicitly **discontinued** in favour of `main_full` / `waveshare_2.2`, and the project now functions mostly as the free/DIY on-ramp to the commercial Ink.

## Related

- [`README.md`](README.md) — ZeroWriter Ink
- [`zerowriter1-epaper-driver-notes.md`](zerowriter1-epaper-driver-notes.md) — the Waveshare driver modifications
- [`development-history.md`](development-history.md) — how the latency work carried forward
- Upstream: <https://github.com/zerowriter/zerowriter1>
