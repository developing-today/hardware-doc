# ZeroWriter Ink — gaps, conflicts and unresolved questions

> Snapshot **2026-08-24**. No hardware was available; nothing here is a firsthand measurement.

## 1. zerowriter.com is a decoy — RESOLVED

**Corrected 2026-08-24.** My first pass recorded the project's website as dead. That was wrong.

`zerowriter.com` *is* a domain-for-sale parking page — but it is **not the project's domain**. The live site is **<https://zerowriter.ink>**, and it is fully operational, with firmware downloads, a web flasher, a news blog and a second product (**Zerowriter Fold**, Kickstarter-funded).

The confusion is real and not mine alone: the **Crowd Supply campaign and essentially all press coverage link to `.com`**. The correct domain was found only inside `firmware_releases/updates-readme.txt` in the GitHub repository.

**Lesson recorded** in [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md): when a vendor site looks dead, grep the repository for the domain.

⚠ Secondary trap: `zerowriter.ink` **403s a normal Chrome user agent** on `/pages/*` and `/products/*` while serving the root fine. See the [vendor guide](../../../vendors/zerowriter/README.md).

## 2. The dual-ESP32 architecture — RESOLVED

**Resolved 2026-08-24** by reading `src/keyboard/zwi_kb_feb2026/zwi_kb_feb2026.ino` (277 lines, GPL-3.0). Full write-up: [`keyboard.md`](keyboard.md).

Answers to what was open:

| Question | Answer |
|---|---|
| Protocol between the two ESP32s | **One raw byte per key event, 921600 baud, `SERIAL_8N1`, TX on GPIO 1, RX disabled (`-1`) — unidirectional** |
| Byte encoding | Key indices 0–60; modifiers 240–247 as separate down/up events; 255 = matrix sentinel |
| Where the keymap lives | **Main board**, via user-editable `keymap.json`. The keyboard has no notion of key meaning |
| Is the keyboard reflashable? | Yes — 6-pin `NOVA_programmer_header` + boot/reset buttons, external USB-UART adapter required |
| Why an ESP32 for a keyboard? | **The developer agrees it is over-specified**: *"we should move away from esp32 to a STM chip, or a cheaper/lower power alternative"* |
| Matrix | 5 rows × 14 columns, 61 keys. Rows GPIO 13/12/27/26/14, columns 19/21/23/22/2/15/4/16/17/5/18/25/33/32 |
| Radio | **Torn down at boot** — `esp_wifi_deinit()`, BT controller disabled and **memory released**. CPU at 80 MHz, light sleep after 200 ms idle |

**Still open:** whether an antenna is fitted to the `U` (external-antenna) module variant; which pins of the 6-pin connector carry TX/power/ground; whether shipped keyboard firmware matches this file.

## 3. What ships versus what is in the repository — PARTLY RESOLVED

The README states the current public firmware is **1.30** and that factory units may be older and buggy. `firmware_releases/` contains **SD-1.3** (current), plus archived **1.24**, **1.25**, **1.27**, and a merged full-flash `zw_latest.merged.bin`. Changelogs for 1.28 and 1.3 are in `SD-1.3/readme.txt`. Analysis: [`firmware-and-updates.md`](firmware-and-updates.md).

**Resolved:** the main board is a plain **ESP32** (chip ID 0), **4 MB flash, DIO, 80 MHz**; images are Arduino-core builds against **ESP-IDF v5.4.1**.

**Still open:**
- The **factory-shipped version** is still not stated anywhere. ("1.30" in the README vs "1.3" as a directory name are probably the same release — unconfirmed.)
- Changelogs for 1.24–1.27 were not shipped.
- ⚠ **A trap for anyone dating these images:** the `esp_app_desc_t` build timestamp is **identical (`Mar 28 2025 06:14:09`) across 1.24 and 1.3** despite different content and different ELF hashes. That timestamp belongs to the Arduino core, not the application. **Do not use it to identify a release.**

## 3a. The main application firmware is not open source

The project is marketed as open source, and the hardware design, enclosure and **keyboard** firmware genuinely are (GPL-3.0). But the **writing application — the actual product — is published only as compiled `.bin` files.** No source for it is in the repository.

The campaign states "Our source code will all be published on GitHub." As of this snapshot that is true of the keyboard and untrue of the main application.

**Status: open.** It may be published elsewhere, or intended for later release.

## 3b. Arrow-key indices — RESOLVED

The keyboard firmware's matrix constants and `keymap.json` disagree on which index is `RIGHT` vs `DOWN`. **The developer confirmed on Reddit that the keymap is authoritative** — the firmware constants serve only the vestigial panic chord and are simply misnamed.

Practical notes: remapping needs firmware **≥ 1.30**; the **web keymap editor greys out the arrow keys**, so edit `keymap.json` by hand; and at least one vendor-supplied alternate keymap was reported to have only the middle pair swapped, so verify rather than trust the filename.

Detail: [`community-and-ecosystem.md`](community-and-ecosystem.md#the-arrow-key-conflict--resolved-by-the-developer).

## 3c. "Zerowriter Core" — clarified

The [Fold](../zerowriter-fold/README.md) page describes Core as "releasing as open source in the coming months" (future tense). The blog post **"Zerowriter Core 1.1 Update" (2025-12-23)** confirms **Core is the Ink's software too**, not Fold-only — so the open-source promise covers both, and neither is open yet.

⚠ **Two version schemes coexist and do not reconcile:** "Core 1.1" (blog) vs SD firmware "1.24 … 1.3" (repo). Which maps to which is **not stated**. Detail: [`software-and-shortcuts.md`](software-and-shortcuts.md).

## 3d. Which Inkplate generation — **Gen 2** (a prototype used gen 1)

The shipping ZeroWriter Ink uses the **Inkplate 5 Gen 2** panel (`ED052TC4`, 1280 × 720), confirmed by the BOM part number, the designator, ZeroWriter's own KiCad project name, the Crowd Supply spec ("second-edition… 1280 × 720") and a campaign update.

**The development prototype used the gen-1 panel** (`ED052TC2`, 960 × 540). The switch happened after funding, in Nov 2024, and directly caused the [latency work](development-history.md#the-e-paper-latency-problem-and-how-it-was-solved) — Gen 2 was slower at ~200 ms.

Pre-funding material describing a 960 × 540 ZeroWriter Ink is therefore accurate *for the prototype* and wrong for the shipped product. Detail: [`README.md`](README.md#which-inkplate-generation--gen-2-confirmed-five-ways).

## 4. Whether the shipped main board matches the published design

The published KiCad project is `Zerowriter Inkplate 5 Gen2 **v1.2.0**`. Crowd Supply updates through 2026 mention "New Improvements" (Feb 2026) and "the Latest Developments" (May 2026). It is **not established** that v1.2.0 is what shipped, or whether later revisions exist that were not published.

**Status: open.** Compare silkscreen revision against the repo if you have a unit.

## 5. The breakout board schematic — RESOLVED (my earlier claim was wrong)

I recorded that `design/src/Zerowriter breakout board/` contained "gerbers only — no KiCad schematic or BOM". **That was wrong.** I had looked only at `OUTPUTS/SingleBoardOutputs/`, which holds gerbers. The full sources are in `v1.2.0/CAD/`:

- `Zerowriter breakout board.kicad_sch`
- `Zerowriter breakout board.kicad_pcb`
- `OUTPUTS/Zerowriter breakout board.csv` (BOM), `ibom.html`, `Schematics.pdf`, `3D.step`

The board is fully documented and has now been netlist-parsed. It carries the **USB-C receptacle, microSD socket, power slide switch, a 350 mA PTC fuse, and the charge/power LEDs** — see [`inter-board-wiring.md`](inter-board-wiring.md).

**Both inter-board connector pinouts are now recovered**, closing the related "which pins carry TX/power/ground" question:

- Keyboard ↔ main: 6-pin, `2× +3V3 / USART2_RX / USART2_TX / 2× Earth`
- Main ↔ breakout: 16-pin, carrying **USB D±**, SD SPI, the switched SD rail, power switch and LED lines

## 6. Peripheral-mode coordinate width — RESOLVED (and moot here)

Resolved on the Inkplate side: the current Arduino library ships a **completely different peripheral protocol** from the one Soldered documents, using `;`-separated variable-width arguments parsed with `atol()`. The 3-digit limit belongs to an obsolete protocol. See [Inkplate 5 gaps §2](../../soldered-electronics/inkplate-5/gaps-and-conflicts.md) and [`peripheral-mode.md`](../../soldered-electronics/inkplate-5/features/peripheral-mode.md).

Moot for ZeroWriter regardless — the Ink runs its own firmware and does not use peripheral mode.

## 7. Claims not verified

| Claim | Source | Status |
|---|---|---|
| ~100 h battery life | campaign | **Unverified.** Plausible given the `BQ25306` switch-mode charger and e-paper, but no measurement, no cell capacity published |
| 3,000 lines / ~24,000 words per document | campaign | Unverified — presumably a firmware buffer limit |
| "Weeks of daily use on a single charge" | campaign | Unverified; not obviously consistent with "100 hours" unless daily use is ~1 h |
| Variable refresh rate produces "almost no perceptible lag" | campaign | Unverified. E-paper partial refresh on a 1280×720 panel is the hardest part of this product and the claim most worth testing |
| Battery is "user-replaceable" | campaign | Plausible — enclosure STLs are published — but the cell type and connector are not documented |

## 9. The repository firmware is two major versions stale

`firmware_releases/` ends at SD-1.3 and the README says "current public firmware is 1.30", but **v2.0/2.1 shipped in July 2026** and lives only on the website. The repo is authoritative for hardware; the website is authoritative for firmware. Whether 2.x changes the flash layout is **not established** — the 2.1 release notes mention a "stronger SD card engine" and internal storage exposed as "HD", which implies partition changes, but no image was parsed.

## 10. The RTC coin cell ships unpopulated — DOCUMENTED

v2.1's writing-stats feature "requires a coin cell installed for all timekeeping features". The board carries **`K11` = `CR2032-BS-6-1`**, an **SMD coin-cell holder footprint** (two 3 × 4.2 mm pads, 29 mm apart, on `F.Cu`) feeding the [PCF85063A](../../../components/nxp/pcf85063a/README.md) through a diode-OR with the main 3V3 rail — but it is **not fitted at the factory**.

**No add-on board is needed** — solder a `BS-6-1`-style holder to the existing pads, or wire a tabbed cell directly. ZeroWriter's respin also adds test points **`TP72`** (`RTC-BATT`) and **`TP71`** (`3V3_RTC`) as alternative attachment/verification points.

Full detail, including polarity, the diode-OR circuit and fitting cautions: [**`rtc-backup-battery.md`**](../../soldered-electronics/inkplate-5/features/rtc-backup-battery.md).

**Still unexplained:** why it ships empty. No vendor states a reason, and only ZeroWriter's v2.1 release notes acknowledge the requirement at all — the Inkplate product pages, Inkplate documentation and the ZeroWriter campaign/repo are all silent.

## 8. What this research pass did not cover

Still genuinely open:

- **No hardware.** Nothing here is a firsthand measurement.
- **Firmware 2.x was not parsed** — only the 1.x images in the repository.
- **The main application source remains unpublished**, pending final order fulfilment.
- **Battery capacity and cell type unknown.** Connector is a **JST 2-pin SMD (`K4`)**; no cell spec appears in any design file.
- **The Discord was not accessed** — it is the primary support venue and where community keymaps and custom firmware are shared.
- **Ize Compose** (third-party firmware) was identified but its repository was not located or analysed.
- **The Fold's Kickstarter page is blocked** (403 to every UA tried). A Wayback snapshot exists — `web.archive.org/web/20260824205508/…` — but the Internet Archive was returning 503 during this pass. Retrievable later.
- **The "double wake from sleep" report** is unexplained.

## Related

- [`README.md`](README.md) — device record
- [Inkplate 5 / Gen 2](../../soldered-electronics/inkplate-5/README.md)
- [Soldered vendor guide](../../../vendors/soldered-electronics/README.md)
