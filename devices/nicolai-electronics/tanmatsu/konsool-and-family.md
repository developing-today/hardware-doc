# Konsool, Tanmatsu and WHY2025 — what the three names mean

> The question "what is a Konsool?" answered from primary sources, plus how the three BSP targets actually relate.
> Snapshot **2026-08-24**. Primary source: [badge.team Konsool documentation](https://badge.team/docs/badges/konsool/) (retrieved 2026-08-24), corroborated by the Badge.Team BSP and the app repository.

---

## The short answer

**Konsool and Tanmatsu are the same device.** The difference is not technical — it is who builds it.

Badge.Team state it directly:

> *"The open-source badge design is released under the CERN-OHL-P license. This applies to both Konsool and Tanmatsu, **which are essentially the same device**.*
>
> ***Konsool is an open design**, freely available for anyone to modify, extend, and use as they see fit.*
>
> ***Tanmatsu is the pre-assembled version sold by Nicolai Electronics**, eliminating the hassle of sourcing components and manufacturing the PCB.*
>
> *Selling electronic devices involves additional requirements, such as safety and environmental certifications. Badge.Team appreciates that Nicolai Electronics takes on these responsibilities, offering the badge practically at cost."*

So:

| | **Konsool** | **Tanmatsu** |
|---|---|---|
| What | The **open hardware design** | The **product you can buy** |
| Custodian | **Badge.Team** (community) | **Nicolai Electronics** (company) |
| Licence | CERN-OHL-P | CERN-OHL-P (same files) |
| You get | Design files — source your own parts, fab your own PCB | An assembled, certified device |
| Certification | Your problem | Nicolai Electronics handles safety/environmental compliance |
| Price | Cost of building it | *"practically at cost"* |

This is a deliberate and rather elegant split: the community keeps an unencumbered open design, and a company shoulders the regulatory and logistics burden of actually selling hardware. It is **not** a fork, a dispute, or a rebrand.

> This resolves what was previously logged as an open question in [`gaps-and-conflicts.md` §3](gaps-and-conflicts.md). Earlier in this research pass the relationship was undocumented in every Nicolai Electronics repository — the explanation lives only on badge.team, which the Tanmatsu documentation does not link to.

### Naming

**端末 (tanmatsu)** is Japanese for "terminal" / "handheld device". **Konsool** is Dutch-flavoured for "console" — Badge.Team is a Dutch organisation.

---

## Are they binary compatible?

**Yes — demonstrably.** This is the strongest available evidence that the hardware is identical, and it comes from the app repository rather than from marketing copy.

Of the **57 apps** in [`Nicolai-Electronics/app-repository`](https://github.com/Nicolai-Electronics/app-repository) at commit `f83e1559`:

- **56 apps ship a single binary** covering every target they declare
- **43 apps declare both `tanmatsu` and `konsool`** — and hand both targets *the same executable*
- **Exactly 1 app ships per-target binaries**: `nl.cj.wifianalyzer`, which splits `wifianalyzer.bin` (tanmatsu) from `wifianalyzer-why2025.bin` (why2025)

So the only device in the ecosystem that ever needs its own build is **WHY2025** — never Konsool. The app repository's own advice reflects this: *"we recommend always adding both to apps that have been developed for one of these boards."*

---

## WHY2025 is different hardware

Despite appearing alongside the other two in target lists, **the WHY2025 badge is not the same device.** Comparing the two BSP targets in [`badgeteam/esp32-component-badge-bsp`](https://github.com/badgeteam/esp32-component-badge-bsp) @ `9037f0e`:

| | Tanmatsu / Konsool | WHY2025 |
|---|---|---|
| Internal I2C | SDA **9**, SCL **10** | SDA **18**, SCL **20** |
| Keyboard | **9×8 matrix scanned by a CH32V203 coprocessor** @ I2C 0x5F | **I2C keyboard controller**, INT on GPIO2, separate RST line |
| Coprocessor | Yes — `BSP_COPROCESSOR_I2C_ADDRESS 0x5f` | **None** |
| LCD reset | GPIO **14**, plus TE on GPIO 11 | GPIO **17** (*"low for normal operation, high for reset"* — inverted) |
| SD card | 4-bit SDIO, pins 39–44 | **not defined** |
| CATT port | 8 pins defined | **none** |
| BMI270 IMU | 0x68 | **none** |
| ES8156 audio | 0x08 + I2S pins | **none** |
| Addressable LEDs | 6 | **none defined** |
| Hardware header size | 1,964 bytes | 534 bytes |

`badge_bsp_input.c`, `badge_bsp_display.c` and `badge_bsp_i2c.c` all **differ** between the two targets — they are not shared files with a `#define` switch.

The WHY2025 device identifies itself as manufacturer *"WHY2025 team:badge"*, and its BSP source carries `SPDX-FileCopyrightText: 2025 Nicolai Electronics` — so Nicolai Electronics designed it, but it is a **smaller, simpler board**: no coprocessor, no CATT, no SD card, no IMU, no audio codec.

**There is no `konsool` target in the BSP at all** — only `tanmatsu` and `why2025`. Konsool builds use `CONFIG_BSP_TARGET_TANMATSU`. The `CONFIG_BSP_TARGET_KONSOOL` symbol appears in [`esp32-component-tanmatsu-wifi`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-wifi)'s `#if defined(...)` guards, but the BSP never defines it — a vestigial symbol, not a real second build.

---

## The wider Badge.Team badge family

The BSP supports eleven targets, which is useful context for how much of the Tanmatsu software stack is shared:

| Target | Device |
|---|---|
| `BSP_TARGET_TANMATSU` | **Nicolai Electronics Tanmatsu** (also used for Konsool) — *the BSP default* |
| `BSP_TARGET_WHY2025` | WHY2025 badge |
| `BSP_TARGET_KAMI` | Nicolai Electronics Kami |
| `BSP_TARGET_MCH2022` | Badge.Team MCH2022 badge |
| `BSP_TARGET_HACKERHOTEL_2024` | Badge.Team Hackerhotel 2024 badge |
| `BSP_TARGET_BORNHACK_2024_POV` | Bornhack 2024 POV |
| `BSP_TARGET_BORNHACK_2025_CIRCLE` | Bornhack 2025 circle |
| `BSP_TARGET_HACKADAY2025` | Hackaday 2025 Communicator badge |
| `BSP_TARGET_HELTECV3` | Heltec v3 |
| `BSP_TARGET_ESP32_P4_FUNCTION_EV_BOARD` | Espressif ESP32-P4 dev kit |
| `BSP_TARGET_ESP32_S31_KORVO_1` | Espressif ESP32-S31 Korvo 1 |
| `BSP_TARGET_STUB` | Generic stub |

Two things worth noting: **Tanmatsu is the BSP's default target**, which tells you where the maintenance effort sits; and the **ESP32-P4 Function EV Board** target exists specifically so Tanmatsu/Konsool software can be developed on Espressif's own dev kit.

## Konsool expansion boards

Badge.Team maintain expansion hardware under the Konsool name, all for the back-facing internal port:

| Repo | What |
|---|---|
| [`badgeteam/konsool-zero`](https://github.com/badgeteam/konsool-zero) | RFID / NFC / sub-1 GHz radio expansion board |
| [`badgeteam/konsool-18650-expansion`](https://github.com/badgeteam/konsool-18650-expansion) | 18650 cell expansion — described as *"for the Tanmatsu/Konsool badge"* |
| [`badgeteam/konsool-expansion-template`](https://github.com/badgeteam/konsool-expansion-template) | Outline, connector and mounting-hole placement for designing your own |
| [`badgeteam/konsool-template-lvgl`](https://github.com/badgeteam/konsool-template-lvgl) | App template using **LVGL** (CC0-1.0) — an alternative to the PAX-based Tanmatsu template |

The expansion template is the one to start from if you are designing a personality module — it gives you the mechanical outline, not just the electrical pinout in [`pinouts-and-buses.md`](pinouts-and-buses.md).

## Additional specifications from badge.team

The Konsool documentation states several things the Tanmatsu documentation does not:

- **ESP32-P4 clock: 400 MHz** — badge.team says 400 MHz consistently, which supports 400 MHz being correct and Tanmatsu's "360 MHz" being the stale figure. See [`gaps-and-conflicts.md` §1](gaps-and-conflicts.md).
- **The ESP32-P4 has AI instruction extensions.**
- **Hardware-accelerated H.264 encoding** via the MIPI DSI/CSI interfaces — *"can record video from devices such as a Raspberry Pi camera, encode it, and stream it wirelessly over WiFi."* This is not mentioned anywhere in the Tanmatsu documentation and is a significant capability.
- **60 Hz screen**, described as "high resolution 60Hz".
- **LoRa at 433, 868 *or* 915 MHz** depending on module fitted.
- The back expansion port exposes **SPI** as well as I2C, USB 2.0 and GPIO.
- **Custom front panels are supported**, with published information; the front panel is a separate PCB.

## The team

Badge.Team credit the following volunteers for Konsool:

| Handle | Name | Role |
|---|---|---|
| r3nz3 | Renze Nicolai | Hardware and software development |
| Ranzbak | Paul Honig | Hardware, testing, documentation |
| Jhaand | Jelle Haandrikman | Testing and review |
| RobotMan2412 | Julian Scheffers | Software and testing |
| Ankhaneko | Nikolett | Artwork and more |
| Orange Murker | Luna | Software and testing |
| NightOwlNL | Emiel Bart | Documentation |
| Noor | | Testing |
| Jay | Jay Visschedijk | Ergonomic board outline |
| Wietsman | Wietse Boonstra | Component footprints |
| Kliment | Kliment Yanev | Hardware review |
| Anus | Anne Jan Brouwer | Software |

## Documentation split — and which to trust

The two documentation sites cover the same hardware with different emphases, and **neither links to the other**:

| | [Tanmatsu docs](https://github.com/Nicolai-Electronics/tanmatsu-documentation) | [badge.team Konsool docs](https://badge.team/docs/badges/konsool/) |
|---|---|---|
| Strength | Connector pinouts, flash layout, BadgeLink, ESP-IDF setup | **Per-IC pinouts**, camera compatibility, expansion boards, FAQ |
| Weakness | No IC-level pinout, no camera list, doesn't explain Konsool | Thinner on software workflow |
| Unique content | AppFS, BadgeLink, esptool commands | **CH32V203 and ESP32-P4 full pin tables**, supported camera sensors, H.264, team credits |

**If you are doing hardware work, badge.team's `hardware/pinout/ics/` pages are the more valuable source** and are easy to miss because nothing in the Tanmatsu repositories points at them. They are enumerable from `https://badge.team/sitemap.xml`.

⚠ **They do sometimes disagree** — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) for the expansion-port GPIO numbering conflict *within* badge.team's own pages.

## Related

- [`README.md`](README.md) — device overview
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — full pin tables including the badge.team IC data
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — remaining contradictions
- [`sources.md`](sources.md) — provenance
