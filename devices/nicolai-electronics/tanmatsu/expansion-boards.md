# Expansion boards, front panels and add-on design — Tanmatsu / Konsool

> What already exists to plug into the two expansion ports, and what you need to build your own.
> Snapshot **2026-08-24**. All repositories cloned and inspected directly; sources archived under
> `scratch/tanmatsu/sources/`.
> **No hardware was available** — nothing here was built, fitted or powered.

Expansion hardware is developed under the **Konsool** name by Badge.Team, while front panels come
from Nicolai Electronics. Both attach to the same device — see
[`konsool-and-family.md`](konsool-and-family.md) for why there are two names.

---

## 1. Existing expansion boards

| Project | Port | Status | Licence |
|---|---|---|---|
| [`badgeteam/konsool-zero`](https://github.com/badgeteam/konsool-zero) | rear 36-pin | **Work in progress** | **BSD-3-Clause** *(corrected 2026-09-20)* |
| [`badgeteam/konsool-18650-expansion`](https://github.com/badgeteam/konsool-18650-expansion) | rear 36-pin | Buildable | **CERN-OHL-P v2** |
| [`badgeteam/konsool-expansion-template`](https://github.com/badgeteam/konsool-expansion-template) | rear 36-pin | ⚠ **empty repository** | — |
| [`Nicolai-Electronics/tanmatsu-frontpanel-cyberdeck`](https://github.com/Nicolai-Electronics/tanmatsu-frontpanel-cyberdeck) | front panel | Buildable | CERN-OHL-P |
| [`Nicolai-Electronics/tanmatsu-frontpanel-honeycomb`](https://github.com/Nicolai-Electronics/tanmatsu-frontpanel-honeycomb) | front panel | Buildable | CERN-OHL-P |

> ⚠ **`konsool-expansion-template` contains no commits.** Its GitHub description promises *"Outline,
> connector and mounting hole placement for creating a Konsool expansion board"* — exactly what an
> add-on designer wants — but `git clone` produces a repository with a broken `HEAD` and no files.
> **Do not plan on it.** Use `konsool-18650-expansion` as your outline reference instead: it contains
> a working `expansion-template.kicad_sch` / `.kicad_pcb` pair with the correct board outline and
> connector placement.

---

## 2. `konsool-zero` — RFID / NFC / sub-GHz

The most ambitious add-on: a **Flipper Zero-class radio board** for the rear expansion port.

**Silicon identified from the KiCad schematics** *(corrected and completed 2026-09-20 from a full
reference-designator census of all nine sheets — see the ⚠ note below)*:

| Ref | Part | Function | Record |
|---|---|---|---|
| `U1` | **`CC1101RGPR`** | TI **sub-1 GHz** transceiver, QFN-20 | [CC1101](../../../components/texas-instruments/cc1101/README.md) |
| `U2` | 27 MHz **oscillator** (`G3226000161060`, 4-pin SMD) | CC1101 reference clock. ⚠ an **XO, not a crystal** — datasheet §7.4 external-reference mode. **27** not 26 MHz = TI's recommendation for **≥ 869 MHz** | ibid. §7, §12 |
| `U3`, `U4` | `BGS13S4N9E6327XTSA1` | Infineon SP3T RF switches — band select | — |
| `U5` | **`ST25R3916-AQWT`** | NFC / HF RFID reader (13.56 MHz), VFQFPN32 | [ST25R3916](../../../components/stmicroelectronics/st25r3916/README.md) |
| `X1` | `XRCGB27M120F3M00R0` (LCSC `C1575`) | **27.12 MHz** crystal, 4-pad 2.0 × 1.6 mm — exactly 2 × the 13.56 MHz NFC carrier | ibid. |
| `U6` | `TSOP75338TR` | 38 kHz IR receiver | — |
| `U7`–`U9` | `VSMY14940` | IR emitter LEDs | — |
| `U10`, `U14` | `LMV358` | 125 kHz RFID analog front end | — |
| `U12` | `LMV331IDCKR` | comparator, RFID front end | — |
| `U11`, `U13`, `U15`, `U16` | `1N4148X-TP` | RFID envelope detectors | — |
| `U17` | `S3225SMD25MOSC` (LCSC `C7431183`) | **25 MHz** oscillator — the MCU's HSE. ⚠ 25 MHz is the top of the V003's HSE range, and ×2 PLL would exceed its 48 MHz max | [CH32V003](../../../components/wch/ch32v003/README.md) §3 |
| **`U19`** | **`CH32V003F4U6`** | **The board's only MCU** — WCH RISC-V, QFN-20, 16 KB flash / 2 KB SRAM | [CH32V003](../../../components/wch/ch32v003/README.md) |

*(`U18` is unused — a genuine gap in the designator sequence, not a missing reading.)*

> ### ⚠ Correction — there is **no STM32WB55CC** on this board
>
> **This section previously listed `STM32WB55CC` as "a wireless MCU … an on-board processor, not
> just a peripheral". That was wrong.** Verified 2026-09-20, `executed-success`:
>
> - Case-insensitive search for `stm32` or `wb55` across every `.kicad_sch`, `.kicad_pcb`,
>   `.kicad_pro` and `jlcpcb/project.db`: **zero matches.** Zero across the full git history too
>   (the repository has one commit).
> - The designator census above is complete and contains **no ST microcontroller of any kind**.
>
> The board's processor is the **CH32V003F4U6** at `U19` — a ~10-cent RV32EC part with 2 KB of
> SRAM, which is a very different proposition from a dual-core Cortex-M4F + M0+ BLE SoC.
>
> **Why the datasheet was there:** the **Flipper Zero's own MCU is an STM32WB55**, and `docs/` is a
> Flipper Zero prior-art study. The earlier pass read the presence of a datasheet as evidence of a
> fitted part. Full negative-result record:
> [`components/stmicroelectronics/stm32wb55xx`](../../../components/stmicroelectronics/stm32wb55xx/README.md).

**What the MCU actually does.** ✅ **Traced from the PCB, 2026-09-20.** The earlier reading below
was correct; it is now `executed-success` rather than `inferred`, with the complete pin map and the
host GPIO assignments in
[**`konsool-zero-wiring.md`**](konsool-zero-wiring.md) — read that file for the wiring.

Hierarchical labels on `zero-mcu.kicad_sch` show the CH32V003
handling the **125 kHz RFID carrier** (`RFID_CARRIER`, `RFID_IN`, `RFID_PULL`, `RFID_RF_OUT`,
`RFID_WR`), **band switching** (`RF_SW_0`, `RF_SW_1`), the **NFC interrupt** (`NFC_IRQ`) and an
**I2C** link (`SCL_MCU`, `SDA_MCU`), with `SWIO` — its one-wire debug pin — brought out to `J4`.
The CC1101 and ST25R3916 **SPI** buses do not appear on that sheet, which is consistent with those
radios being driven by the **Tanmatsu host across the expansion connector**, the CH32V003 acting
as a helper rather than an application processor.

> **Confirmed, and extended.** Parsing `tanmantsu-zero.kicad_pcb` — which, unlike a `.kicad_sch`,
> stores *resolved* net names on every pad — shows the CC1101 (`U1`) and ST25R3916 (`U5`) SPI pins
> land on connector pins 16–18 and 21 and never touch `U19`. The host drives both radios directly.
> Three things the sheet-level reading could not reach:
>
> - **`SWIO` also goes to the host**, on expansion pin 15 = **GPIO47** — not only to `J4`. Combined
>   with the `rvswd` component the Tanmatsu already ships, **the ESP32-P4 can reflash this add-on's
>   CH32V003 with no programmer.** `inferred`, `not-tested`.
> - **`NFC_IRQ` does not reach the host at all** — it stops at `U19.18`. A host-side NFC driver must
>   poll, or ask the CH32V003 over I²C, and **no firmware for that MCU is published**.
> - **The whole radio SPI bus sits in the `VSDCARD` power domain** (GPIO45/46/47/48), so the P4's
>   internal LDO 4 must be enabled before either radio answers.
>
> Also: konsool-zero's expansion-pin **`E8`/`E9`/`E10` labels follow badge.team's ESP32-P4 IC page —
> the numbering [`gaps-and-conflicts.md` §14](gaps-and-conflicts.md) proved wrong.** This is the
> first evidence that the bad table reached a real layout. See
> [`konsool-zero-wiring.md` §4](konsool-zero-wiring.md).

**Schematic sheets present:** `tanmantsu-zero` *(sic)*, `zero-mcu`, `nfc-block`, `rfid-schematic`,
`sub-ghz-radio`, `antenna-balance`, `rf-balance`, `ibutton`, `ir-comms`, `expansion-template`.

So the intended feature set is **NFC + 125 kHz RFID + sub-GHz + iButton + infrared** — i.e. a Flipper
Zero equivalent as a Tanmatsu personality module. The `ir-comms` sheet is interesting given the
mainboard *already* has an [undocumented IR LED](gaps-and-conflicts.md) on the ESP32-C6.

**Reference material vendored in `docs/`:** seven chip documents — `cc1101_datasheet.pdf`,
`ST25R3916.PDF`, `stm32wb55cc.pdf`, and a `ch32/` folder holding `CH32V003RM.PDF`,
`CH32V003DS0.PDF`, `CH32FV2x_V3xRM.PDF` and `CH32V203DS0.PDF` — plus **annotated Flipper Zero
teardown photos** (`NFC-RFID_antenna_annotations.png`, `MCU-board.png`, `sub1gHz-radio.png`) and
six extracted **Flipper Devices Inc.** schematics (RFID, NFC, Power, Power and vibro, iButton,
Sub-1 GHz). The design is openly derived from studying Flipper Zero.

**All seven chip documents were mined and filed as component records on 2026-09-20** — including
`CH32V203DS0.PDF`, which turned out to be the Tanmatsu *mainboard* coprocessor's own datasheet,
closing a gap in that record. See
[`sources.md`](sources.md#datasheets-recovered-from-konsool-zeros-docs-folder--added-2026-09-20).

**The six Flipper Devices schematics and the teardown photos were filed on 2026-09-20** under
[`devices/flipper-devices/flipper-zero/`](../../flipper-devices/flipper-zero/README.md) — they
describe a different product, so they belong to it. Reading them settles the design lineage: the
Flipper's sub-GHz chain uses the **same `CC1101RGPR`, the same `BGS13S4N9E6327XTSA1` switches and
the same `B0310J50100AHF` balun**, and its 125 kHz front end the same `LMV331`/`LMV358` pair.
konsool-zero changed exactly two things — the CC1101 reference (**26 MHz crystal → 27 MHz
oscillator**) and the MCU (**STM32WB55 → CH32V003F4U6**).

**Status: work in progress.** A single commit (`0f0b964`, 2025-03-22, *"board elements that were
missing."*) and **no README**. The vendored Flipper Zero documents have their own upstream terms.
Treat as a design study, not a buildable board.

> ### ✅ Correction — the licence *is* stated: **BSD 3-Clause**
>
> This section, and §1's table, previously said konsool-zero had **"no stated licence"**. That was
> wrong. A `LICENSE` file **is tracked at `0f0b964`** (1 506 B) and carries the **BSD 3-Clause
> License, Copyright (c) 2024, Nicolai Electronics**. Verified 2026-09-20 by reading the file and
> `git ls-files`; `executed-success`. Retained at
> [`artifacts/konsool-zero/LICENSE-BSD-3-Clause`](artifacts/konsool-zero/LICENSE-BSD-3-Clause).
>
> The **"no README"** and **"one commit"** claims were re-checked in the same pass and are
> **correct** — `git ls-files` lists no `README*`, and `git log` shows exactly one commit.
>
> Note the copyright holder is **Nicolai Electronics**, not Badge.team, even though the repository
> lives under `badgeteam/` and the sole commit is authored by Paul Honig.

### The design files are now in the repository

The nine schematic sheets, both PCBs and the shared expansion template are at
[`artifacts/konsool-zero/`](artifacts/konsool-zero/README.md). **Until 2026-09-20 they existed
only in `scratch/`** — which meant the corrections on this page cited evidence the repository did
not hold. A cross-repository SHA-256 sweep confirmed their absence before they were placed.

---

## 3. `konsool-18650-expansion` — external battery

A rear add-on carrying **18650 cells** to extend runtime. Author: **Ranzbak** (Paul Honig).

From the README:

> *"The Konsool/Tanmatsu battery lasts for a couple of hours and is internal to the device. This
> project extends the battery life… with several hours."*

| Feature | Detail |
|---|---|
| Protection | **One protection IC per 18650 cell** |
| Switch | `SS-12D06-G050` slide switch (on/off) |
| Holder | `BH-18650-A5BJ001-2D` |
| Charging | *"Charges off the USB-C power from the Konsool/Tanmatsu"* |
| Mounting | **M2** holes to fasten the holder securely |
| Licence | **CERN-OHL-P v2** |

### ⚠ Safety caveat, in the author's own words

> *"Given that all[e] batteries are current limited by protection IC's slightly different charges in
> the internal battery and 18650 cells should not be okay. **Please do monitor device during
> charging.**"*

The sentence is garbled, but the intent is clear: the internal LiPo and the external 18650s charge in
parallel through protection ICs with slightly different characteristics, and the author is **not
confident this is safe unattended**.

This also sits directly against the mainboard documentation, which states plainly:

> *"Do **not** charge the battery via the internal add-on port."*
> — [`pinouts-and-buses.md` §2.2](pinouts-and-buses.md)

**Do not treat this board as a validated design.** It is a community project whose own author asks
you to supervise charging. Lithium cells in parallel with mismatched protection is a real hazard.

*(The README also notes the board silkscreen uses the Dutch police logo as a lithium-fire hazard
marking, "because it was too perfect for that".)*

---

## 4. Front panels

Both official front panels are **purely decorative PCBs**. Their production BOMs contain exactly one
line each:

```
Designator,Footprint,Quantity,Value,LCSC Part #
"H1, H2, H3, H4",MountingHole_2.1mm_pad,4,Mounting hole,
```

**Four mounting holes, no components.** The front panel is artwork on fibreglass — which is why
custom panels are easy and why Badge.Team encourage them.

### How they are made

> *"This Kicad project makes use of [svg2shenzhen](https://github.com/badgeek/svg2shenzhen) to convert
> a vector graphics design file (SVG) into a Kicad footprint."*

So the workflow is **draw in a vector editor → `svg2shenzhen` → KiCad footprint → fab**. You do not
need to be a PCB designer to make a front panel; you need to be able to draw.

### Fabrication settings — use these exactly

> *"When manufacturing these boards select **0.8 mm** board thickness, **ENIG** surface finish and
> **Remove Mark**."*

| Setting | Value | Why |
|---|---|---|
| Thickness | **0.8 mm** | Thicker will not fit the case stack-up |
| Surface finish | **ENIG** | Gold-on-exposed-copper is what makes the artwork look right; HASL will not |
| Order mark | **Remove Mark** | Otherwise the fab prints its order number on your artwork |

Artwork for the cyberdeck panel is by **[Ankhaneko](https://ankhaneko.art)**.

### ⚠ Licence boundary

The panels are CERN-OHL-P, **but the artwork is not**:

> *"All organization names, logos, trademarks and artwork including but not limited to the Nicolai
> Electronics and Tanmatsu branding are all rights reserved… and may not be reproduced on derivative
> works."*

You may reuse the panel *outline and mounting geometry*; you may **not** reuse the artwork. Draw your
own. Note also that CERN-OHL-P **requires attribution** — the README asks that the copyright
statement be carried into derivative works.

Badge.Team additionally document front-panel artwork at
[`konsool/hardware/frontpanel/artwork/`](https://badge.team/docs/badges/konsool/hardware/frontpanel/artwork/).

Mechanical integration — including the FreeCAD Z-offsets for positioning the front panel PCB
(**+2.40 mm**) against the mainboard (**−1.55 mm**) — is in
[`mechanical-and-case.md`](mechanical-and-case.md). Remember the front panel is also what **retains
the keyboard keypad**, so its thickness and any cut-outs interact with the
[KeebDeck stack-up](keyboard.md).

---

## 5. Designing your own rear expansion board

### Electrical

Start from [`pinouts-and-buses.md` §2](pinouts-and-buses.md#2-internal-add-on-port-personality-module--36-pin-254-mm). The critical points:

- **Genuinely free GPIO: `E1`, `E9`, `E11`, `E12`, `E13`** (P4 GPIO 0, 49, 52, 51, 50).
- **`E8` and `E10` are NOT free** despite the vendor list — they carry the **ESP32-C6 UART**
  ([§2c](pinouts-and-buses.md#2c--verified-from-copper-e8-and-e10-are-not-free-gpio)). Verified from
  the fabrication netlist.
- **`E0`** has an undocumented **4.7 kΩ pull-up** — it idles high.
- **`E3`–`E6`** need the ESP32-P4's internal **LDO 4 (`VSDCARD`)** enabled.
- **`E2`** is shared with the camera connector.
- **`P4_TX` must be low and `P4_RX` high during boot** — an add-on that violates this stops the
  device booting.
- **`E7`** is in the P4 low-power domain with a 51 kΩ pull-up: the correct choice for a **wake-from-
  deep-sleep** interrupt.

### Power limits — hard numbers

| Limit | Value |
|---|---|
| All 3.3 V outputs combined | **≤ 1 A** (advice: stay well below) |
| Battery draw via internal connector | **≤ 1.5 A** |
| Charging via the add-on port | **Prohibited** |

Available rails: `VOTG` (5 V when the PMIC booster is on), `VBATT` (3.0–4.2 V, **live even when the
device is off**), `VSYS` (3.0–5.0 V, switched), `+3.3V`.

### Identification EEPROM

Fit an EEPROM at **I2C 0x50** on the internal bus. ⚠ **The content format is undefined** — the vendor
says it *"has yet to be determined"* and the launcher has no add-on identification support yet. Fit
the part, leave the contents for later.

### Mechanical

- The rear port is **not exposed by default**; a **modified back cover** is required. This is why it
  is also called the "internal" expansion port.
- `konsool-expansion-template` is empty, so use **`konsool-18650-expansion`**'s
  `expansion-template.kicad_pcb` for the outline and connector placement.
- Case and mounting geometry: [`mechanical-and-case.md`](mechanical-and-case.md).

### Side (CATT) port instead?

If you only need a few GPIO, I2C or JTAG, the **CATT** port is easier — it is exposed without case
modification and is simultaneously **PMOD-, SAO- and JTAG-compatible**. See
[`pinouts-and-buses.md` §3](pinouts-and-buses.md#3-external-add-on-port--catt-connect-all-the-things).
⚠ Pulling **pin 6 (GPIO34, `DETECT`) low moves JTAG off USB-C onto the CATT pins** — an add-on that
does this will break USB debugging until software overrides it.

---

## 6. App templates

Two, and they are not equivalent:

| Template | Graphics | Licence | Targets |
|---|---|---|---|
| [`tanmatsu-template`](https://github.com/Nicolai-Electronics/tanmatsu-template) | **PAX graphics** | ⚠ **none stated** | Tanmatsu |
| [`konsool-template-lvgl`](https://github.com/badgeteam/konsool-template-lvgl) | **LVGL** | **CC0-1.0** | `tanmatsu`, `mch2022`, `general` |

The LVGL template ships per-target `sdkconfigs/` directories (`tanmatsu`, `mch2022`, `general`),
which is a cleaner multi-board starting point, and it is **explicitly licensed** — unlike the PAX
template, whose missing licence is flagged in [`gaps-and-conflicts.md` §9](gaps-and-conflicts.md).

Badge.Team's recommendation:

> *"The contents of this repository may be considered in the public domain or CC0-1.0 licensed at
> your disposal… we recommend licensing your work based on this template under terms of the MIT
> license."*

**If licence clarity matters to you, start from the LVGL template.**

---

## 7. Gaps

| Question | Status |
|---|---|
| `konsool-expansion-template` contents | ⚠ **Repository is empty.** Not reported upstream |
| Is `konsool-zero` buildable? | **No** — WIP, one commit, no README, no licence |
| Are the vendored Flipper Zero documents redistributable? | **Unknown** — third-party material with its own terms |
| Is the 18650 board electrically safe? | **Unresolved.** Author advises supervision; conflicts with the mainboard's "do not charge via the add-on port" |
| Add-on identification EEPROM format | **Undefined by the vendor** |
| Are the front-panel `production/*.zip` Gerbers valid? | **RESOLVED** — opened 2026-08-24. Complete valid Gerber + drill sets. The front panel has `F_Silkscreen` at 353 KB against a 3.6 KB back silkscreen, consistent with artwork on the front face only |
| Do any commercial add-ons exist? | **Not researched** — vendor webshop not scraped |

## Related

- [`pinouts-and-buses.md`](pinouts-and-buses.md) — expansion port pinouts and verified conflicts
- [`mechanical-and-case.md`](mechanical-and-case.md) — case, front panel geometry, board revisions
- [`keyboard.md`](keyboard.md) — the front panel retains the keypad
- [`konsool-and-family.md`](konsool-and-family.md) — why expansion boards carry the Konsool name
- [`sources.md`](sources.md) — provenance
