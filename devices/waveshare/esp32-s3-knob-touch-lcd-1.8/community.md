# Community resources

> **Superseded 2026-08-23 by [examples/catalog.md](examples/catalog.md)**, which covers **28** board-specific repositories (against the 8 below), adds pinned commits, frameworks and per-project assessment, and retains five permissively-licensed projects locally under [`examples/selected/`](examples/). This page is kept for its original 2026-08-21 snapshot metadata.

Retrieved: 2026-08-21. These are secondary examples, not hardware authority. No repository source was copied because several repositories report no license or an indeterminate license. Snapshot metadata is retained at `artifacts/source-snapshots/community-repositories-2026-08-21.json`.

The eight rows below are exactly the projects the Waveshare wiki lists in §8.8 "Project Resources".

| Repository | Default branch | Last push at retrieval | API license |
|---|---|---|---|
| https://github.com/VolosR/Knob18Meters | main | 2025-07-29 | none reported |
| https://github.com/ihayri/ESP32-S3-1.8inch-Knob-Display-Development-Board | main | 2026-01-08 | none reported |
| https://github.com/muness/roon-knob | master | 2026-08-21 | NOASSERTION |
| https://github.com/0015/lvgl_kawaii_face | main | 2026-02-27 | MIT |
| https://github.com/knobby-mtg/knobby-mtg-life-counter | main | 2026-07-30 | GPL-3.0 |
| https://github.com/juggernautwins608/Waveshare-1.8-Magic-the-Gathering-Life-Counter | main | 2026-07-04 | MIT |
| https://github.com/EmbeddedWizardGUI/ESP32-S3-Knob-Touch-LCD-1.8-EN | main | 2026-07-20 | none reported |
| https://github.com/chris023/orion-waveshare-rotary-dial | main | 2026-08-05 | NOASSERTION |

The Waveshare wiki additionally links project videos/forums; follow the live wiki for those mutable references. Dates above are metadata snapshots, not endorsements or tested compatibility claims.

## Update 2026-08-23

The wiki's list has not changed (page still at revision 111069), but a GitHub search found **20 further
board-specific repositories** the vendor does not list — including the only ESP32-U4WDH source we have
found anywhere, an ESPHome configuration covering this board and its Guition clone, and an as-shipped
firmware/SD-card archive. All 28 are catalogued with pinned commits in
**[examples/catalog.md](examples/catalog.md)** and machine-readably in
[`examples/catalog.json`](examples/catalog.json).

## Update 2026-08-24

Compiling [techniques.md](techniques.md) surfaced **five further sources that are not repositories** —
three issue/discussion threads, one repo and one video. They are recorded in full, with medium, author,
date, evidence type and what each establishes, in
**[examples/catalog.md §6](examples/catalog.md)** and under the new `non_repository_sources` key in
[`examples/catalog.json`](examples/catalog.json).

They matter disproportionately because, unlike the demonstration projects above, **each one fixes a
specific defect in the vendor code**:

| Source | Author, date | Establishes |
|---|---|---|
| [Tasmota discussion #23737](https://github.com/arendst/Tasmota/discussions/23737) | Tasmota community, 2025-08-01 | CST816 reset timing **10 ms / 10 ms / 50 ms**; QSPI bring-up in a working third-party port. Thread title says **ST77916** |
| [lewisxhe/SensorLib #32](https://github.com/lewisxhe/SensorLib/issues/32) | `gilphilbert`, 2026-01-19 | DRV2605 reports chip ID **`0x05`, not `0x03`** — stock SensorLib `begin()` fails |
| [lvgl_micropython #547](https://github.com/lvgl-micropython/lvgl_micropython/issues/547) | `d51r3verse`, 2026-03-27 | SDMMC MMC-mode init crash, **plus a real factory SD-card listing** |
| [nishad2m8/WS-1.8-Knob](https://github.com/nishad2m8/WS-1.8-Knob) + [video](https://youtu.be/ACAmAXBgFy0) | nishad2m8, 2025-08-17 → 2025-10-30 | **USB HID** smart knob (DaVinci Resolve); PlatformIO/Arduino + LVGL + SquareLine. No licence declared |

The **Volos** ([`8pHF0OAG2TI`](https://www.youtube.com/watch?v=8pHF0OAG2TI), [`5G4W3irHkks`](https://www.youtube.com/watch?v=5G4W3irHkks)) and **iHayri** ([`d2aSVfH3RDM`](https://www.youtube.com/watch?v=d2aSVfH3RDM)) videos were **already catalogued** and have now been given explicit evidence typing — **demonstration only**, no defect analysis or measurements.

Practical consequences of all of the above are worked through in
[techniques.md](techniques.md) and [project-ideas.md](project-ideas.md).
