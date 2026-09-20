# Xteink X4 — projects

> Census **2026-09-04**: GitHub repository search API, 5 queries × 2 pages,
> authenticated. **~200 relevant repositories**, of which the clear majority name
> the X4 specifically. Owner-report material is in [`community.md`](community.md).

## Why the X4 has the biggest ecosystem

It was **first**, it was **cheap**, and it was **the target every firmware started
on**. CrossPoint Reader, CrossInk, Microreader, marigold-os, TrustyReader,
pluspoint-reader and AALU were all written for the X4 and grew to cover the X3 and
the S3 devices afterwards. Even now, records that describe the family usually say
*"for the Xteink X3 and X4"* — in that order only because X3 sorts first.

## Firmware targeting the X4

### The two mainlines

| Project | Licence | Note |
|---|---|---|
| [`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader) | MIT | Upstream. The X4 is its original target |
| [`uxjulia/CrossInk`](https://github.com/uxjulia/CrossInk) | MIT | The other lineage. Ships an [SDL simulator](https://github.com/uxjulia/crossink-simulator) |
| [`Free-Ink/freeink-sdk`](https://github.com/Free-Ink/freeink-sdk) | — | **The HAL under both**, and the source of every board fact in this record |

### Independent firmware — not CrossPoint forks

Unusually for a cheap device, several people wrote firmware **from scratch or in
other languages**:

| Project | Language | Note |
|---|---|---|
| [`CidVonHighwind/microreader`](https://github.com/CidVonHighwind/microreader) | C++ | GPLv2. *"If you have an unlocked X4 (**!!!UNLOCKED!!!**)"* — 514 pts on announcement |
| [`ngxson/pluspoint-reader`](https://github.com/ngxson/pluspoint-reader) | C | *"Yet another alternative firmware for Xteink X4"* |
| [`Jon-Vii/marigold-os`](https://github.com/Jon-Vii/marigold-os) | **Rust** | MIT. X4 and X3 |
| [`HookedBehemoth/TrustyReader`](https://github.com/HookedBehemoth/TrustyReader) | **Rust** | GPL-2.0 |
| [`aimindseye/rustmix-x4-firmware`](https://github.com/aimindseye/rustmix-x4-firmware), [`h0rv/rust-xteink-x4`](https://github.com/h0rv/rust-xteink-x4), [`yanganto/xteink-x4`](https://github.com/yanganto/xteink-x4) | **Rust** | Three more |
| [`h0rv/slint-xteink-backend`](https://github.com/h0rv/slint-xteink-backend) | Rust | A **Slint UI backend** for Xteink devices |
| [`evanstoddard/xteink_x3_zephyr`](https://github.com/evanstoddard/xteink_x3_zephyr) | — | **Zephyr RTOS** (X3, same board family) |
| [`adafruit/Adafruit_CircuitPython_Xteink_X4`](https://github.com/adafruit/Adafruit_CircuitPython_Xteink_X4) | Python | **Adafruit** published a CircuitPython helper — a notable third-party endorsement |

**Six independent Rust efforts** on one $69 consumer device is remarkable, and is
a direct consequence of the ESP32-C3's RISC-V core having good Rust support.

### Notable forks and applications

`AALU` (installs on locked devices via SD), `Flowe` (focus firmware + iOS BLE app,
303 pts), `Duet` ([`lauren-alexandra/duet-xteink`](https://github.com/lauren-alexandra/duet-xteink)),
`inkMOD` (Russian/Ukrainian, FB2), `BookPoint` (Russian), `crossmosa` (繁體中文),
`CrossPlant`, `SkyPoint`, `casper`, `crossfade`, `InkWyrm`, `CipherCodex OS`,
`Lector`, `PocketBook`, `CrossMux` (a Chinese fork adding **WeChat Read** support).

### Novelty and games

[`davidpavlicek36/doom-xt4`](https://github.com/davidpavlicek36/doom-xt4) — **Doom
on the X4** · [`CidVonHighwind/xteink-bad-apple`](https://github.com/CidVonHighwind/xteink-bad-apple)
· [`cassidoo/xteink-4-in-a-row`](https://github.com/cassidoo/xteink-4-in-a-row)
· [`HenryBaby/TamaInk`](https://github.com/HenryBaby/TamaInk) (Tamagotchi P1)
· [`lodyb/crosspoint-reader`](https://github.com/lodyb/crosspoint-reader) (MTG life tracker)
· [`padge01/xteink-pokemon-game`](https://github.com/padge01/xteink-pokemon-game).

### Non-reader uses of the hardware

| Project | What |
|---|---|
| [`maddiedreese/xteink-terminal`](https://github.com/maddiedreese/xteink-terminal) | ★32 — *"tmux bridge for using an XTeInk X4 as a small Wi-Fi e-ink terminal display"* |
| [`keithwithAI/xteink-agenda`](https://github.com/keithwithAI/xteink-agenda) | Google Calendar via a FastAPI server |
| [`fsocietyipa/WienerLinien-XteinkX4`](https://github.com/fsocietyipa/WienerLinien-XteinkX4) | Vienna transit departure board |
| [`pocmaker42/xteink-todo`](https://github.com/pocmaker42/xteink-todo) | Web UI + PHP API + firmware |
| [`t0nyz0/crosspoint-reader-lockscreens`](https://github.com/t0nyz0/crosspoint-reader-lockscreens) | GitHub / Weather / Tempest dashboards |
| [`vjFaLk/esphome-xteink`](https://github.com/vjFaLk/esphome-xteink) | **ESPHome** components wrapping the FreeInk SDK |

## Flashing, backup and recovery tooling

| Tool | Language | Note |
|---|---|---|
| [`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher) | Python | **1:1 full-flash backup & restore in ~2 min**, auto COM detect, ships stock images |
| [`bigbag/papyrix-flasher`](https://github.com/bigbag/papyrix-flasher) | Go | ★25. Auto-detection, embedded bootloader, MD5 verification |
| [`OvermindDL1/xteink-unlocker`](https://github.com/OvermindDL1/xteink-unlocker) | Rust/Tauri | Desktop unlocker with a privileged macOS helper |
| [`togotago/xteink-x4-escape`](https://github.com/togotago/xteink-x4-escape) | Python | **A named brick and its cure** — CrossPoint 1.2.0 OTA failing at `esp_ota_end()` |
| [`lvturner/x4-dual-boot`](https://github.com/lvturner/x4-dual-boot) | Shell | MicroSlate + CrossInk **dual-boot on a USB-locked X4** via SD |
| [`abhishek-nerella/XTEINK-OEM-BIN-`](https://github.com/abhishek-nerella/XTEINK-OEM-BIN-) | — | The **16 MB factory dump** archived in this record |

## The `.XTC` format problem

Stock firmware uses a proprietary **`.XTC`** book format, which spawned an entire
converter cottage industry: [`thirteen37/calibre-xtc`](https://github.com/thirteen37/calibre-xtc)
(★19), [`jonasdiemer/epub2xtc`](https://github.com/jonasdiemer/epub2xtc),
[`alf-arv/epub-to-xtc-util`](https://github.com/alf-arv/epub-to-xtc-util),
[`domschl/PDF2XTEink`](https://github.com/domschl/PDF2XTEink),
[`smalltomatowater-boop/xtmaker`](https://github.com/smalltomatowater-boop/xtmaker).

**Its existence is one of the strongest arguments for reflashing**: community
firmware reads EPUB directly.

## Fonts, wallpapers, sync

Font tooling ([`SamLinBIT/XTEink-ttf2bin`](https://github.com/SamLinBIT/XTEink-ttf2bin),
[`iwalton3/cpfont-editor`](https://github.com/iwalton3/cpfont-editor),
[`enfance-prog/Xteink-Fontbuilder-mac`](https://github.com/enfance-prog/Xteink-Fontbuilder-mac),
`crossglyph`); wallpaper generators (XKCD, Pokédex, Truchet, Wikimedia,
countries); OPDS and sync servers ([`rcarmo/bun-opds-server`](https://github.com/rcarmo/bun-opds-server),
[`sroberts/shelf`](https://github.com/sroberts/shelf),
[`LowFlowIO/x4m`](https://github.com/LowFlowIO/x4m)); companion apps for
[macOS](https://github.com/lukataylo/crosspoint-mac),
[Android](https://github.com/duplexer/crosspoint-companion-pro) and
[iOS](https://github.com/AirBook-for-CrossPoint).

## Localisation

Independent ports into **~12 languages**: Chinese (simplified + 繁體), Japanese,
Korean, Arabic, Russian, Ukrainian, Myanmar, Persian, Gujarati, Vietnamese,
Portuguese, Spanish. For a device with no distributor network, that is a strong
install-base signal.

## Community services

| Site | Purpose |
|---|---|
| `crosspointreader.com` | **Device unlock**, web flasher, flash-back-to-stock, nightly builds |
| `crossink.uxj.io` | CrossInk documentation |
| `brickclub.pages.dev` | Firmware chooser — the name is a joke about bricking |
| `readme.club` | Community hub with a model-selection quiz and spec comparisons; **linked by an r/XTEINK automoderator rule** |

## Evidence caveat

This is a **census, not an audit.** A repository proves someone started something.
It does not prove the code builds, runs, or was flashed to an X4. Only the FreeInk
SDK's claims are treated as hardware-confirmed elsewhere in this record.
