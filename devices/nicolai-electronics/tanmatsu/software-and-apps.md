# Tanmatsu — software and the app ecosystem

> The launcher, the official app repository, and what has actually been built.
> Snapshot **2026-08-24**, from `app-repository` @ `f83e1559` (2026-08-22).
> Machine-readable: [`artifacts/app-repository-catalog.json`](artifacts/app-repository-catalog.json)

## How the ecosystem works

The **launcher firmware** ([`tanmatsu-launcher`](https://github.com/Nicolai-Electronics/tanmatsu-launcher), MIT) boots from firmware slot A and presents a menu. Apps are separate ESP32-P4 firmware binaries stored in the **8 MB AppFS partition** and started directly by a modified bootloader — see [`development.md` §6](development.md#6-appfs).

Publishing is deliberately low-friction and entirely git-based: **fork [`Nicolai-Electronics/app-repository`](https://github.com/Nicolai-Electronics/app-repository), add a folder, open a pull request.** There is no store, no review fee, no signing.

App folders are named with a **reverse-DNS slug** (`com.example.test`) and must contain a `metadata.json`:

```json
{
  "name": "Commodore 64 emulator",
  "description": "C64 emulator based on T-HMI-C64",
  "categories": ["games"],
  "version": "0.0.6",
  "icon": { "16x16": "icon16.png", "32x32": "icon32.png", "64x64": "icon64.png" },
  "author": "Ranzbak",
  "license_type": "GPLv3 or later",
  "application": [{
      "targets": ["tanmatsu", "konsool"],
      "type": "appfs",
      "revision": 6,
      "executable": "c64.bin",
      "assets": []
  }]
}
```

Notable fields:

- **`targets`** — currently only `tanmatsu`, `konsool` and `why2025` are valid. The repo advises always declaring both `tanmatsu` and `konsool` "since [they] are essentially the same device".
- **`license_type`** — an SPDX identifier, or `proprietary` with a `license_file`. **Licensing is mandatory metadata**, which is a better norm than most hobbyist app ecosystems manage.
- **`assets`** — files copied to `<mountpoint>/apps/<slug>/` on the internal FAT partition *or* the SD card. The repo explicitly warns that apps must check **both** locations.
- **`type`** — only `appfs` is supported today.

## Ecosystem statistics

**57 apps** from **21 distinct authors**.

| Licence | Apps |
|---|---:|
| MIT | 34 |
| CC0-1.0 | 14 |
| GPL family (2.0 / 3.0 / -or-later) | 6 |
| proprietary | 2 |

| Target declared | Apps |
|---|---:|
| `tanmatsu` | 54 |
| `konsool` | 43 |
| `why2025` | 4 |

**48 of 57 apps are MIT or CC0** — an unusually permissive ecosystem, and a marked contrast to the XIAO/ESP32 maker world where most community projects carry no licence at all. Requiring `license_type` in metadata evidently works.

Only **4 apps target `why2025`**, confirming that despite three BSP targets existing, the practical ecosystem is the Tanmatsu/Konsool pair.

## The catalogue

### Communication

| App | Author | Version | Licence | Targets |
|---|---|---|---|---|
| **MatrixMatsu** <br/><sub>`nl.daandobber.matrixmatsu`</sub> | Daan Dobber | 0.3.0 | MIT | konsool, tanmatsu |
| **MultiMesh** <br/><sub>`fi.ps.multimesh`</sub> | Petri Simolin | 0.10.0 | MIT | konsool, tanmatsu |
| **SSHmatsu** <br/><sub>`nl.nickbouwhuis.sshmatsu`</sub> | Nick Bouwhuis | 1.0.0 | MIT | konsool, tanmatsu |

### Games

| App | Author | Version | Licence | Targets |
|---|---|---|---|---|
| **Catch the apple** <br/><sub>`nl.mansoft.catchtheapple`</sub> | Henri Manson | 0.0.1 | MIT | konsool, tanmatsu |
| **Commodore 64 emulator** <br/><sub>`nl.ranzbak.c64`</sub> | Ranzbak | 0.0.6 | GPLv3 or later | konsool, tanmatsu |
| **Floppy Bird GL** <br/><sub>`at.cavac.floppybird`</sub> | Rene cavac Schickbauer | 2.1.0 | CC0-1.0 | konsool, tanmatsu |
| **HowBoyAdvance** <br/><sub>`com.irak4t0n.howboyadvance`</sub> | Irak4t0n | 1 | GPL-2.0 | konsool, tanmatsu |
| **HowBoyMatsu** <br/><sub>`com.irak4t0n.howboymatsu`</sub> | Irak4t0n | 2 | GPL-2.0 | tanmatsu |
| **MatsuMonsterMesh** <br/><sub>`com.irak4t0n.matsumonstermesh`</sub> | Irak4t0n | 1 | GPL-3.0-or-later | tanmatsu |
| **MQTT demo** <br/><sub>`nl.mansoft.mqtt`</sub> | Henri Manson | 0.0.1 | MIT | konsool, tanmatsu |
| **Nofrendo NES emulator** <br/><sub>`team.badge.nofrendo`</sub> | Badge.Team | 0.0.2 | GPLv2 | konsool, tanmatsu |
| **OpenJazz** <br/><sub>`nl.daandobber.openjazz`</sub> | Daan Dobber | 0.1.0 | GPL-2.0-or-later | tanmatsu |
| **Place Invaders GL** <br/><sub>`at.cavac.placeinvaders`</sub> | Rene cavac Schickbauer | 2.2.0 | CC0-1.0 | konsool, tanmatsu |
| **POGN GL** <br/><sub>`at.cavac.pogn`</sub> | Rene cavac Schickbauer | 2.1.0 | CC0-1.0 | konsool, tanmatsu |
| **Race the Synth GL** <br/><sub>`at.cavac.racethesynth`</sub> | Rene cavac Schickbauer | 0.3.0 | MIT | konsool, tanmatsu |
| **Spirograph** <br/><sub>`nl.mansoft.spiro`</sub> | Henri Manson | 0.0.1 | MIT | konsool, tanmatsu |
| **TaDOOM** <br/><sub>`at.cavac.tadoom`</sub> | Rene cavac Schickbauer | 0.6.0 | CC0-1.0 | konsool, tanmatsu |
| **TIC-80** <br/><sub>`com.annejan.tic80`</sub> | Vadim Grigoruk (nesbox) - Tanmatsu port by Anne Jan Brouwer | 1.3.1 | MIT | konsool, tanmatsu |
| **Universal Paperclips GL** <br/><sub>`at.cavac.paperclips`</sub> | Rene cavac Schickbauer | 0.2.0 | MIT | konsool, tanmatsu |
| **VT01A** <br/><sub>`nl.mansoft.vt01a`</sub> | Henri Manson | 0.0.1 | MIT | konsool, tanmatsu |

### Tools

| App | Author | Version | Licence | Targets |
|---|---|---|---|---|
| **Graceloader** <br/><sub>`at.cavac.graceloader`</sub> | Rene cavac Schickbauer | 2.1.0 | MIT | konsool, tanmatsu |
| **Key LED Indicator** <br/><sub>`at.cavac.key-led-indicator`</sub> | Rene Schickbauer | 2.0.0 | MIT | konsool, tanmatsu |
| **LED Matrix** <br/><sub>`nl.cj.whyledmatrix`</sub> | CJ van Soest | 1.0.0 | MIT | why2025 |
| **Matter comms** <br/><sub>`hu.zh4ck.matter`</sub> | zh4ck | 1.0.5 | MIT | konsool, tanmatsu |
| **MeshCore** <br/><sub>`nl.cj.meshcore`</sub> | CJ van Soest | 3.6.0 | MIT | konsool, tanmatsu |
| **Micropython** <br/><sub>`nl.mansoft.micropython`</sub> | Henri Manson | 0.2 | MIT | konsool, tanmatsu |
| **Nuke-it** <br/><sub>`at.cavac.nukeitformatter`</sub> | Rene cavac Schickbauer | 1.5.0 | CC0-1.0 | konsool, tanmatsu |
| **Power Info** <br/><sub>`at.cavac.powerinfo`</sub> | Rene Schickbauer | 2.0.0 | MIT | konsool, tanmatsu |
| **Screenshot** <br/><sub>`at.cavac.screenshot`</sub> | Rene Schickbauer | 2.0.0 | MIT | konsool, tanmatsu |
| **Sensors (LVGL)** <br/><sub>`nl.cj.whysensorslvgl`</sub> | CJ van Soest | 1.0.0 | MIT | why2025 |
| **Storage Monitor** <br/><sub>`nl.cj.whystorage`</sub> | CJ van Soest | 1.0.0 | MIT | why2025 |
| **T-IRC** <br/><sub>`hu.zh4ck.tirc`</sub> | zh4ck | 1.0.0 | MIT | konsool, tanmatsu |
| **TanTerminal** <br/><sub>`lgbt.sky.tanterminal`</sub> | Sky.LGBT | 1.1.0 | MIT | konsool, tanmatsu |
| **Typewriter** <br/><sub>`com.lunardr4gn.typewriter`</sub> | Leviathan & Daandobber | 3.0.1 | MIT | tanmatsu |
| **WadaMesh** <br/><sub>`com.wadamesh.wadamesh`</sub> | Kaj Schittecat - ALLFATHER BV | 1.0.63 | GPL-3.0 | konsool, tanmatsu |
| **WiFi Analyzer** <br/><sub>`nl.cj.wifianalyzer`</sub> | CJ van Soest | 1.0.1 | MIT | tanmatsu, why2025 |
| **WifiScanner** <br/><sub>`de.saarbastler.wifiscanner`</sub> | Saarbastler | 0.2.0 | MIT | tanmatsu |

### Hardware

| App | Author | Version | Licence | Targets |
|---|---|---|---|---|
| **BLE cat printer** <br/><sub>`nl.nicolaielectronics.catprinter`</sub> | Nicolai Electronics | 0.0.1 | CC0-1.0 | tanmatsu |
| **IR Camera** <br/><sub>`de.asaril.tanmatsu.ircam`</sub> | Asaril | 0.2.1 | MIT | konsool, tanmatsu |
| **USB disk drive** <br/><sub>`nl.nicolaielectronics.usbmsc`</sub> | Nicolai Electronics | 0.0.1 | CC0-1.0 | tanmatsu |
| **USB HID keyboard** <br/><sub>`nl.nicolaielectronics.keyboard`</sub> | Nicolai Electronics | 0.0.2 | CC0-1.0 | tanmatsu |

### Media

| App | Author | Version | Licence | Targets |
|---|---|---|---|---|
| **Disc-O-Matsu** <br/><sub>`nl.daandobber.discomatsu`</sub> | Daan Dobber | 0.2.0 | MIT | konsool, tanmatsu |
| **ImageWag** <br/><sub>`lgbt.sky.imagewag`</sub> | Sky.LGBT | 2.0.0 | MIT | konsool, tanmatsu |
| **Kodi Remote** <br/><sub>`nl.daandobber.kodiremote`</sub> | Daan Dobber | 0.2.0 | CC0-1.0 | konsool, tanmatsu |
| **Music Player** <br/><sub>`at.cavac.musicplayer`</sub> | Rene Schickbauer | 2.0.0 | MIT | konsool, tanmatsu |
| **MusicMaker** <br/><sub>`nl.daandobber.musicmaker`</sub> | Daan Dobber | 0.1.0 | MIT | tanmatsu |
| **MusicPlayer** <br/><sub>`nl.daandobber.musicplayer`</sub> | Daan Dobber | 0.1.0 | proprietary | konsool, tanmatsu |
| **Neiro** <br/><sub>`net.scheffers.neiro`</sub> | Pascal Scheffers | 1.0.0 | MIT | konsool, tanmatsu |
| **Startup Sound** <br/><sub>`at.cavac.startup`</sub> | Rene Schickbauer | 2.0.0 | MIT | konsool, tanmatsu |
| **Tanmatype camera** <br/><sub>`at.cavac.tanmatype`</sub> | Rene cavac Schickbauer | 1.5.0 | CC0-1.0 | konsool, tanmatsu |
| **TanRadio** <br/><sub>`com.github.siviqt.tanradio`</sub> | siviqt | 0.1.0 | proprietary | tanmatsu |
| **Trackmatsu** <br/><sub>`gb.heathenuk.trackmatsu`</sub> | HeathenUK | 0.0.2 | MIT | konsool, tanmatsu |
| **Zotoropu** <br/><sub>`at.cavac.zoetrope`</sub> | Rene cavac Schickbauer | 1.4.0 | CC0-1.0 | konsool, tanmatsu |

### Demos

| App | Author | Version | Licence | Targets |
|---|---|---|---|---|
| **Ballz GL** <br/><sub>`at.cavac.ballz`</sub> | Rene cavac Schickbauer | 2.1.0 | CC0-1.0 | konsool, tanmatsu |
| **Musical Keyboard GL** <br/><sub>`at.cavac.musicalkeyboard`</sub> | Rene cavac Schickbauer | 2.1.0 | CC0-1.0 | konsool, tanmatsu |
| **TheCube GL** <br/><sub>`at.cavac.thecube`</sub> | Rene cavac Schickbauer | 2.1.0 | CC0-1.0 | konsool, tanmatsu |
| **Turret** <br/><sub>`at.cavac.turret`</sub> | Rene Schickbauer | 2.0.0 | MIT | konsool, tanmatsu |

## What the catalogue tells you

**This is a working, not aspirational, ecosystem.** 57 apps from 21 authors on a low-volume device is healthy, and the spread — emulators, mesh messaging, SSH, a Matrix client, IRC, tools, demos — matches the "terminal for hackers" positioning rather than being all blinkenlights demos.

**Communications apps are the distinctive cluster.** SSHmatsu (SSH client), MatrixMatsu (Matrix), MultiMesh (MeshCore + Meshtastic) and an IRC client exploit the specific combination of *keyboard + screen + Wi-Fi + LoRa* that almost no other microcontroller device has. This is the category to watch: it is what the hardware is actually for.

**Emulation is a recurring theme** — C64, NES, TIC-80 and an x86 emulator ([`tanmatsu-xtulator`](https://github.com/Nicolai-Electronics/tanmatsu-xtulator)) all exist. The ESP32-P4's 32 MB of PSRAM is what makes this practical.

## Notable software outside the app repository

| Project | What it is |
|---|---|
| [`tanmatsu-launcher`](https://github.com/Nicolai-Electronics/tanmatsu-launcher) | The launcher firmware itself (MIT) — the most-starred Tanmatsu repo |
| [`tanmatsu-template`](https://github.com/Nicolai-Electronics/tanmatsu-template) | Starting point for new apps, uses **PAX graphics** |
| [`tanmatsu-xtulator`](https://github.com/Nicolai-Electronics/tanmatsu-xtulator) | x86 emulator |
| [`tanmatsu-meshcore`](https://github.com/Nicolai-Electronics/tanmatsu-meshcore) | MeshCore client (preview) |
| [`tanmatsu-meshtastic-radio`](https://github.com/Nicolai-Electronics/tanmatsu-meshtastic-radio) | WIP Meshtastic fork; requires manual recovery steps |
| [`tanmatsu-circuitpython`](https://github.com/Nicolai-Electronics/tanmatsu-circuitpython) | CircuitPython port |
| [`ranzbak/konsoolnes`](https://github.com/ranzbak/konsoolnes) | NES emulator |
| [`petrisi/tanmatsu-multimesh`](https://github.com/petrisi/tanmatsu-multimesh) | MeshCore + Meshtastic |
| [`badgeteam/esp32-component-badge-bsp`](https://github.com/badgeteam/esp32-component-badge-bsp) | The BSP — 11 targets including Tanmatsu |
| [`badgeteam/esp32-component-badgelink`](https://github.com/badgeteam/esp32-component-badgelink) | BadgeLink protocol + host tools |
| [`badgeteam/appfs`](https://components.espressif.com/components/badgeteam/appfs) | The app filesystem component |

There is also an [issue tracker](https://github.com/Nicolai-Electronics/tanmatsu-issue-tracker/issues) and a public [project board](https://github.com/orgs/Nicolai-Electronics/projects/2/views/2) for following development.

## Community

- **Discord**: <https://discord.gg/KkY6JqNCqT>
- **Telegram**: <https://t.me/+SueEz5IWYR05NzU8>
- **Email**: contact@nicolaielectronics.nl
- **Badge.team**: <https://badge.team> — the wider ecosystem this device belongs to

## Evidence status

The app counts, licences, authors and targets above are **computed directly from `metadata.json` files** in the official repository at a pinned commit — firsthand, reproducible, and not editorial claims. What is **not** established: whether any given app works, how many people own the device, or how active the community is day to day. No app was built or run.

## Related

- [`development.md`](development.md) — how to build and install an app
- [`README.md`](README.md) — hardware overview
- [`sources.md`](sources.md) — repository provenance
