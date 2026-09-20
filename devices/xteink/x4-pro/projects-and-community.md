# Xteink X4 Pro — projects and community

> Census **2026-09-04** via the GitHub repository search API (5 queries × 2 pages,
> authenticated) plus 1,798 Reddit posts. **~200 relevant repositories.** This
> page covers the whole family where the ecosystem is shared, and marks what is
> X4 Pro-specific.

## The ecosystem in one paragraph

Two independent firmware lineages dominate — **CrossPoint Reader** and
**CrossInk** — both sitting on the **FreeInk SDK**, which is the shared hardware
abstraction layer and the source of every board fact in this record. Around them
is an unusually large tail of personal forks, converters, wallpaper generators,
sync servers and Calibre plugins. The tail exists because the devices are cheap,
the SDK is good, and the stock firmware is poor.

## The load-bearing projects

| Project | What | Licence | Relevance to X4 Pro |
|---|---|---|---|
| [`Free-Ink/freeink-sdk`](https://github.com/Free-Ink/freeink-sdk) | **The HAL.** Board profiles, drivers, display/touch/battery/SD managers | — | **The authoritative hardware source.** `BoardConfig::XTEINK_X4_PRO` |
| [`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader) | Upstream reader firmware | MIT | The reference implementation |
| [`uxjulia/CrossInk`](https://github.com/uxjulia/CrossInk) | The other major lineage | MIT | `x4pro` device type added to bug reports 2026-08-18 |
| [`ma-r-s/crossplay`](https://github.com/ma-r-s/crossplay) | CrossPoint fork adding ~26 games/apps | MIT | **The X4 Pro is its stated design floor.** [Full record](../../../software/applications/crossplay/README.md) |
| [`crosspoint-reader/community-sdk`](https://github.com/crosspoint-reader/community-sdk) | Community HAL | — | X3 grayscale preconditioning |

## X4 Pro-specific projects

| Repo | What |
|---|---|
| [`MrStu82/crosspoint-llama-pro`](https://github.com/MrStu82/crosspoint-llama-pro) | *"CrossPoint Reader llama edition for the Xteink X4 Pro (ESP32-S3, GT911 touch, dual warm/cold frontlight)"* — third-party corroboration of the hardware profile |
| [`thepropm/proink-os`](https://github.com/thepropm/proink-os) | *"a from-scratch e-reader firmware for the Xteink X4 Pro, built on the FreeInk SDK"* — pushed 2026-09-04 |
| [`dito94/CrossDiTo`](https://github.com/dito94/CrossDiTo) | Personal X4 Pro fork of CrossInk 1.5 |
| [`HomeAssistantPi/xteink-backup-utility`](https://github.com/HomeAssistantPi/xteink-backup-utility) | *"Flash and Storage Utility for XTEINK / ESP32-S3. Built for my XTEINK 4 PRO."* The **only** X4 Pro backup tool |
| [`goodyttoor/inkback-freeink-sdk`](https://github.com/goodyttoor/inkback-freeink-sdk) | FreeInk SDK fork — *"InkMotion (PSRAM multi-buffer, damage windows, ghost budget) and **X4 Pro display work**"* |
| [`hiroshi/freeink-x4pro-app`](https://github.com/hiroshi/freeink-x4pro-app) | Links the vendor product page directly |
| [`parsimo2010/xteink-ft8`](https://github.com/parsimo2010/xteink-ft8) | *"Field FT8 from a Raspberry Pi + Xteink X4 Pro e-ink"* |
| [`mylatestwork/crossink-wallpapers`](https://github.com/mylatestwork/crossink-wallpapers) | Sleep screens for X4 **and X4 Pro** |
| [`Paatricious/Andrra`](https://github.com/Paatricious/Andrra) | Wikimedia-sourced sleep screens for X4 Pro |
| [`vjFaLk/esphome-xteink`](https://github.com/vjFaLk/esphome-xteink) | ESPHome components for **X4 / X3 / X4 Pro**, wrapping the FreeInk SDK |

## Community service sites

Named together in [r/XTEINK `1uz8yiz`](https://old.reddit.com/r/XTEINK/comments/1uz8yiz/) (2026-07-17, 723 pts):

| Site | Purpose |
|---|---|
| `crosspointreader.com` | **Device unlock**, web flasher, flash-back-to-stock, nightly builds, font builder |
| `crossink.uxj.io` | CrossInk documentation |
| `brickclub.pages.dev` | *"to choose an appropriate firmware"* — a firmware chooser. The name is a joke about bricking |

## Non-firmware tooling (family-wide)

| Category | Examples |
|---|---|
| Flashers | `bigbag/papyrix-flasher` (Go), `zocs/eink-quick-flasher` (**1:1 full-flash backup/restore, ~2 min**), `OvermindDL1/xteink-unlocker` (Tauri/Rust) |
| Calibre plugins | `thirteen37/calibre-xtc`, `yemM/crosspoint-reader-sd-calibre-plugins`, `ElendilDrac01/xteink-x3-calibre-stock` |
| XTC format converters | `jonasdiemer/epub2xtc`, `alf-arv/epub-to-xtc-util`, `domschl/PDF2XTEink`, `smalltomatowater-boop/xtmaker` — **the stock firmware uses a proprietary `.XTC` book format**, which is why so many of these exist |
| Font tooling | `SamLinBIT/XTEink-ttf2bin`, `iwalton3/cpfont-editor`, `enfance-prog/Xteink-Fontbuilder-mac`, `Driftrabbinate714/crossglyph` |
| Sync / servers | `rcarmo/bun-opds-server`, `LowFlowIO/x4m`, `sroberts/shelf`, `datojulien/crosspoint-cwa-bridge` |
| Companion apps | `lukataylo/crosspoint-mac` (Swift), `duplexer/crosspoint-companion-pro` (Kotlin), `AirBook-for-CrossPoint` (iOS) |
| Home Assistant | `clintonmarshall/xteink-flexdisplay-ha`, `CraigBell/xteink-x3-home-assistant-dashboard`, `wiltodelta/xteink-sugartv` (CGM display) |
| Novelty | `davidpavlicek36/doom-xt4` (**Doom**), `CidVonHighwind/xteink-bad-apple`, `cassidoo/xteink-4-in-a-row`, `HenryBaby/TamaInk` (Tamagotchi P1) |

## Localisation forks — an indicator of reach

The device has been localised by independent developers into at least:
Chinese (`anki630/crossmosa` 繁體中文, `ZYFDroid`, `TrissElan/xteink-minimized-reader-cjk`),
Japanese (`lranslot/crosspoint-reader-jp`, `iori7295/crosspoint-jp`, `feeeeeeen/XTeinkToolkit_jp`),
Korean (`crosspoint-reader-ko`, `YMO1215/crosspoint-reader-ko-ai`),
Arabic (`sfoulad/midad-by-foulad`),
Russian/Ukrainian (`alpzoloto-sudo/inkmod`, `klanva/BookPoint`),
Myanmar (`bhonemyinthtoo999-pixel/CrossPoint-Myanmar-Edition`),
Persian, Gujarati (`monk-blade/xteink-gujarati-font-crosspoint`),
Vietnamese (`leductho911/crossVy`), Portuguese (`carlo-z-duardo/xteink-br`).

**Roughly a dozen languages ported by unrelated individuals** is a strong signal
of install base for a device with no distributor network.

## Cross-device: what the SDK also targets

The same SDK carries profiles for M5Stack PaperS3 / PaperMono / PaperColor,
LilyGo T5-S3, Seeed reTerminal Sticky, EEGO A4, OnePage C61 (ESP32-C61) and
Murphy M3/M4. So **firmware written for the X4 Pro is portable**, and the X4 Pro
is one node in a wider e-paper firmware ecosystem rather than an island. See
[`../../m5stack/papermono/projects-and-community.md`](../../m5stack/papermono/projects-and-community.md).

## Evidence caveat

This is a **repository census**, not an audit. Repository existence proves someone
started something; it does not prove the code builds, runs, or was ever flashed to
an X4 Pro. Only the FreeInk SDK's own claims are marked hardware-confirmed, and
only those are used as evidence elsewhere in this record.
