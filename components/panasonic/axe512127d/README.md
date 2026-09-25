# Panasonic AXE512127D

> **A4S-series narrow-pitch board-to-board connector — the SOCKET half.** 0.4 mm pitch, **12 contacts**, 0.8 mm mated height, 2.5 mm body width, gold-plated, RoHS.
> Research snapshot **2026-09-01**. Fitted as **`J6` on sheet 4** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), where it carries the whole KEY/RGB/PDM sub-board interface.
> Its mating half is [**`AXE612124D`**](../axe612124d/README.md), `J1` on sheet 5. **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Panasonic **A4S (0.4 mm pitch)** series datasheet, document `ACCTB7E 201602-T`, issued **2016-02-29**; local copy `artifacts/panasonic-a4s-series-connectors-digikey-mirror.pdf` | `not-tested` |
| **[SCH-V]** | Read off the schematic rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[SCH-M]** | Recovered from the schematic's `CO`/`PI` marker layer | `executed-success` for the extraction |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **`AXE512127D`** | **[SCH-V]**; **[DS]** p. 2 product-type table |
| Manufacturer | **Panasonic Industry** (Panasonic Electric Works) | **[DS]** |
| Series | **A4S**, "Narrow pitch connectors, 0.4 mm pitch" | **[DS]** cover |
| Half | **Socket** (`AXE5…`) | **[DS]** ordering key |
| Mating half | **`AXE612124D`** — Header | **[DS]** p. 2, 4 mm-pitch packaging table, 12-pin row |
| Contacts | **12** | **[DS]**; **[SCH-M]** |
| Pitch | **0.4 mm** | **[DS]** |
| Mated height | **0.8 mm** | **[DS]** |
| Body | **4.90 × 2.50 mm**, height **0.77 mm** | **[DS]** socket dimension table, 12-pin row |
| Suffix `D` | **4 mm-pitch embossed packaging**, 15 000 pcs/reel | **[DS]** p. 2 |
| Datasheet | `ACCTB7E 201602-T`, **11 pages**, issued 2016-02-29 | **[DS]** metadata |

### 1.1 Reading the part number **[DS]** ordering key

```
AXE  5  12  1  27  D
     │  │   │  │   └── packaging: nil = 8 mm emboss, D = 4 mm emboss
     │  │   │  └────── surface treatment / variant
     │  │   └───────── mated height  (socket: 1 = for 0.8 / 1.0 mm)
     │  └───────────── number of pins (2 digits)  = 12
     └──────────────── 5 = A4S socket,  6 = A4S header
```

So `AXE512127D` and `AXE612124D` are the socket/header pair for **12 pins at
0.8 mm mated height in 4 mm embossed tape** — the exact row Panasonic's table
prints together. This is *decoded from the manufacturer's own key*, not guessed.

> ⚠ **This is the A4S series at 0.4 mm pitch, not a 0.5 mm part.** The `AXE`
> prefix is used across several Panasonic narrow-pitch families and it is easy to
> assume 0.5 mm from the pitch of neighbouring connectors on the same board. The
> datasheet's title, cover and dimension tables all say **0.4 mm**. **[DS]**

---

## 2. Specifications **[DS]** p. 3

| | Item | Value |
|---|---|---|
| **Electrical** | Rated current | **0.3 A per contact** (max **5 A** across all contacts) |
| | Rated voltage | **60 V AC/DC** |
| | Dielectric strength | 150 V AC for 1 min |
| | Insulation resistance | min. **1000 MΩ** initial, 250 V DC megger |
| | **Contact resistance** | **max. 90 mΩ** (JIS C 5402) |
| **Mechanical** | Composite insertion force | max. 1.200 N × contacts |
| | Composite removal force | min. 0.165 N × contacts |
| | Contact holding force (socket) | min. 0.20 N per contact |
| | **Insertion/removal life** | **30 cycles** |
| **Environmental** | Ambient temperature | **−55 °C to +85 °C**, no icing or condensation |
| | Soldering heat | reflow peak **≤ 260 °C**; iron 300 °C/5 s, 350 °C/3 s |
| | Storage | −55…+85 °C (product), **−40…+50 °C (emboss packing)** |
| | Thermal shock | 5 cycles −55/+85 °C, IR ≥ 100 MΩ, CR ≤ 90 mΩ |
| | Humidity | 120 h at 40 °C / 90–95 % RH |
| | Saltwater spray | 24 h, 5 % ± 1 %, IEC 60068-2-11 |
| | **H₂S resistance** | 48 h, 3 ppm ± 1 ppm at 40 °C — CR ≤ 90 mΩ |
| **Materials** | Moulding | LCP resin, UL94V-0 |
| | Contact/post | copper alloy, Ni base + **Au** surface; socket terminals carry **Ni barriers** against solder rise |
| Unit weight | 20-pin socket **0.02 g** / header 0.01 g | |

> ⚠ **30 insertion/removal cycles.** This is the number to notice. The sub-board
> joint is *not* a serviceable connector in any repeated sense — it is an assembly
> interconnect. Repeatedly separating the KEY/RGB/PDM board for debugging will
> exhaust the rating quickly, and the failure mode is intermittent contact rather
> than an obvious open. **[DS]** + **[INF]**

Panasonic's own headline features for the series: 2.5 mm body width (30 % narrower
footprint than the older F4S), "Tough Contact" construction — Ni-barrier against
solder rise, bellows contacts against drop shock, V-notch and double contacts
against particles and flux, and porosity treatment against corrosive gases.
**[DS]** cover.

---

## 3. Used By

### `devices/m5stack/papermono` — `J6`, sheet 4

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md). This
connector joins the mainboard to the **KEY / RGB / PDM sub-board**
(`PaperMono KEY RGB.SchDoc`, sheet 5), which carries the three buttons, the side
RGB indicator and the PDM microphone.

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes**. The Lite drops only NFC and LoRa; it keeps the buttons, the
RGB LED and the microphone, all of which live on this sub-board. The Lite's
schematic is published only as a 4-sheet `PRJ` PDF and its `J6` was not read
directly.

### 3.1 Pinout **[SCH-V]** — identical on both halves

Read off **both** sheet 4 (`J6`, this socket) and sheet 5 (`J1`, the
[AXE612124D](../axe612124d/README.md) header) rendered at 200 dpi. The two
symbols are drawn identically, which is the check that the pair mates 1↔1.

| Pin | Net | Purpose |
|---:|---|---|
| **1** | `3V3_L0` | **always-on rail** — reaches the sub-board even in the deepest power state |
| **2** | `GND` | tied to end tabs 13/14 (§3.2) |
| **3** | `3V3_L2` | main system rail; decoupled by `C76` = 10 µF/10 V (mainboard) and `C5` = 10 µF/10 V (sub-board) |
| **4** | `PDM_VDD` | microphone rail, switched by `U21` [AW35122FDR](../../awinic/aw35122/README.md) |
| **5** | `PY_LED_R` | RGB LED red — driven by the [M5PM1](../../m5stack/m5pm1/README.md), on/off only |
| **6** | `PWR_BTN` | power button, pulled up on the sub-board to **`3V3_L0`** by `R1` = 10 kΩ |
| **7** | `PYB_LED_G` | RGB LED green — [M5IOE1](../../m5stack/m5ioe1/README.md) PWM |
| **8** | `G2_KEY1` | user button A → ESP32-S3 GPIO2 |
| **9** | `PYB_LED_B` | RGB LED blue — M5IOE1 PWM |
| **10** | `G3_KEY2` | user button B → ESP32-S3 GPIO3 **(a strapping pin)** |
| **11** | `G46_PDM_DAT` | PDM data → ESP32-S3 GPIO46 **(a strapping pin)**, `R3` = 22 Ω series |
| **12** | `G45_PDM_CLK` | PDM clock → ESP32-S3 GPIO45 **(a strapping pin)**, `R4` = 22 Ω series |
| 13, 14 | `GND` | **soldering tabs**, not signal contacts (§3.2) |
| 15, 16 | `GND` | soldering tabs, tied together |

> ⚠ **Three of the twelve signals are ESP32-S3 strapping pins** — GPIO3, GPIO45
> and GPIO46. Holding user button B, or a microphone that drives its lines during
> reset, perturbs the straps. This is a board-level hazard already recorded in
> [`pinouts-and-buses.md`](../../../devices/m5stack/papermono/pinouts-and-buses.md);
> it is repeated here because the *connector* is where those signals cross a
> separable joint, and a mis-seated sub-board is one plausible cause of a boot
> that behaves differently after reassembly. **[INF]**

### 3.2 "Pins 13–16" are soldering tabs, and the datasheet explains the tie

The schematic symbol has **16 pins**: 12 signal contacts numbered 1–12, plus four
marked **`MP`** and numbered 13–16. **The A4S ordering table has no 16-pin
variant at 0.8 mm in `D` packaging; it has a 12-pin one, and that is what
`AXE512127D` is.** **[DS]** So the four `MP` positions are the connector's
**metal soldering terminals** (the mechanical anchors at each end), given pin
numbers by the library symbol so they can be netted.

The datasheet's dimension drawing carries the note:

> *"Since the soldering terminals has a single-piece construction, sections Y and
> Z are electrically connected."* **[DS]**

That is exactly what the schematic reflects: `J6`.13 and `J6`.14 are the pair at
one end and are drawn tied, with pin 2 joined to them and the whole net taken to
`GND`; 15 and 16 are the pair at the other end, tied, also to `GND`. **[SCH-V]**

So: **pin 2 is a ground contact**, and the end tabs are used as extra ground
anchors — sensible, and the correct reading of an otherwise odd-looking loop in
the drawing.

> This refines the [device record's connector table](../../../devices/m5stack/papermono/pinouts-and-buses.md),
> which lists `J6` as "16" pins. Sixteen is the *symbol's* pin count; the
> **connector has 12 contacts plus 4 soldering tabs**. Not a contradiction — a
> clarification. Date 2026-09-01.

---

## 4. Substitution and migration

`AXE512127D` is one row of a large table. Migrating within the series is
mechanically clean, because Panasonic designed it that way:

| Change | How |
|---|---|
| More or fewer signals | Any even count 10–80 exists at 0.8 mm; body length `A` = 4.50 + 0.4 × (pins − 10) mm **[DS]** |
| Taller stack | **1.0 mm mated height uses the *same socket*** — only the header changes (`AXE6xx224`). **[DS]** feature 3: *"Mated heights of 0.8 and 1.0 mm are available for the same foot pattern"* |
| 8 mm tape instead of 4 mm | Drop the `D`: `AXE512127`, 5000 pcs/reel |

Outside the series, the near equivalents are Hirose **DF40C** (0.4 mm, and
[already documented here](../../hirose/df40c-30dp-0.4v/README.md) for the XIAO
Sense), JAE **WP7B**, Molex **SlimStack 55560/54722**. None is a drop-in
footprint.

> **Do not substitute across pitches.** The board also carries a
> [`BTB0.408-10PLBDR-G41`](../../generic/btb0.408-10plbdr-g41/README.md), which is *also*
> 0.4 mm pitch and *also* 0.8 mm mated height but is a different, unrelated part
> from a different vendor. The two are not interchangeable and appear on adjacent
> sheets.

---

## 5. Integration pitfalls

1. **30 mating cycles** (§2). Plan disassembly accordingly.
2. **0.3 A per contact.** `3V3_L0`, `3V3_L2` and `PDM_VDD` each ride a *single*
   contact. That is a hard ceiling on what the sub-board may draw per rail, and
   the LED string plus the microphone must fit inside it. Not measured. **[INF]**
3. **Pins 13–16 are tabs, not contacts** (§3.2) — do not count on them for
   current beyond mechanical grounding.
4. **The series is specified as "board-to-FPC"** in the datasheet's keywords and
   applications, yet here it is used board-to-board. Electrically identical;
   worth knowing when reading Panasonic's application notes, which assume a flex
   on one side. **[DS]** + **[INF]**
5. **Emboss-packing storage is −40…+50 °C**, narrower than the product's own
   −55…+85 °C. Relevant only to stock handling.
6. **Three strapping pins cross this joint** (§3.1).

---

## 6. Open questions

- The `27` field in `AXE512127D` (surface treatment / Ni-barrier option) is
  decoded only as far as the datasheet's ordering key goes; the exact plating
  variant it selects was not established.
- Current derating with all 12 contacts loaded — the datasheet gives 0.3 A/pin
  and a 5 A total but no derating curve.
- Whether M5Stack fits `D` (4 mm tape) or plain (8 mm tape) in production; the
  schematic says `D`, which is a *packaging* choice and does not change the part.
- No hardware measurement of contact resistance or retention.

---

## Manufacturer

**Panasonic Industry.** No vendor sourcing guide exists in this repository yet.

**⚠ Retrieval finding.** Panasonic's own CDN was **not** the working route:

| Host | Result |
|---|---|
| `industrial.panasonic.com/content/data/CT/PDF/AXE_CT.pdf` | connection hang, then **404** |
| **`media.digikey.com/pdf/Data Sheets/Panasonic Electric Works PDFs/A4S_Series.pdf`** | **200, `application/pdf`, `%PDF` ✓** — first try, Chrome 131 UA |
| `www.mouser.com/catalog/specsheets/…a4s-catalog.pdf` | 200 but **13 897 B of non-PDF** under Chrome and ClaudeBot UAs; **succeeded only with the `WhatsApp/2.23.20.0` UA** |
| `www1.futureelectronics.com/doc/PANASONIC/AXE610224_panasonic.pdf` | **200, `%PDF` ✓** (the same series document under a different part's name) |

Two things worth carrying forward: **Digi-Key's `media.digikey.com` is a reliable
mirror for Panasonic connector series documents**, and **Mouser's specsheet host
served a short non-PDF body to browser and crawler agents but the real PDF to the
WhatsApp link-preview agent** — the same inversion already recorded for
`focuslcds.com` in the
[FT6336G record](../../focaltech/ft6336g/README.md). Both belong in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

Note also that the acquired PDF is **encrypted** (`print:yes copy:yes
change:no`), which does not impede reading but does mean tooling that rejects
encrypted PDFs will choke on it.

## Related pages

- [Panasonic AXE612124D](../axe612124d/README.md) — **the mating header**, `J1` sheet 5
- [Hirose DF40C-30DP-0.4V(51)](../../hirose/df40c-30dp-0.4v/README.md) — comparable 0.4 mm board-to-board documented here
- [BTB0.408-10PLBDR-G41](../../generic/btb0.408-10plbdr-g41/README.md) — the board's *other* 0.4 mm connector, unrelated
- [LMD4737T261-AC02](../../generic/lmd4737t261-ac02-pdm-microphone/README.md) · [RS-C1415MBAR](../../generic/rs-c1415mbar-rgb-led/README.md) — what lives on the far side
- [PaperMono bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | Narrow pitch connectors **A4S (0.4 mm pitch)** | Panasonic (via Digi-Key mirror) | primary, via distributor mirror | <https://media.digikey.com/pdf/Data%20Sheets/Panasonic%20Electric%20Works%20PDFs/A4S_Series.pdf> | 2026-09-01 | **`ACCTB7E 201602-T`**, issued **2016-02-29**, 11 pp, 399 357 B, AES-encrypted | the ordering key, the socket/header pairing, all of §2, the 12-pin dimensions, the soldering-terminal note | `artifacts/panasonic-a4s-series-connectors-digikey-mirror.pdf` |
| D2 | Same bundle, **older revision**, Future Electronics mirror | Panasonic (via Future) | primary, via distributor mirror | <https://www1.futureelectronics.com/doc/PANASONIC/AXE610224_panasonic.pdf> | 2026-09-01 | **`ACCTB7E 201310-T`** + `ACCTB48E 201303-T`, 10 pp, 324 968 B | that the socket digit was already `7` by 2013-10, but the **`D` package option did not yet exist** | `artifacts/panasonic-a4s-series-connectors-future-mirror-ACCTB7E-201310.pdf` |
| D3 | `A4S Series`, **oldest revision**, Mouser mirror | Panasonic (via Mouser) | primary, via distributor mirror | <https://www.mouser.com/catalog/specsheets/> `a4s-catalog.pdf` — **`WhatsApp/2.23.20.0` UA required** | 2026-09-01 | **`ACCTB7E 201303-T`** + `ACCTB48E 201303-T`, 10 pp, 298 896 B | that the socket surface-treatment digit was **`4`**, so this revision prints the part as `AXE512124` | `artifacts/panasonic-a4s-series-connectors-mouser-mirror-ACCTB7E-201303.pdf` |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `J6` = `AXE512127D`, the §3.1 pinout, the tab tie | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/panasonic-a4s-series-connectors-digikey-mirror.pdf` | 399 357 | `292023186ef0758f1862f8aa2a5f545dc1c14659f4ba84f14f7183f6385503b4` | 11 |
| `artifacts/panasonic-a4s-series-connectors-future-mirror-ACCTB7E-201310.pdf` | 324 968 | `8245f6fa8ced22a64f4af4a836ad7a288598c899ba88ad3de1d82ce313aeabe1` | 10 |
| `artifacts/panasonic-a4s-series-connectors-mouser-mirror-ACCTB7E-201303.pdf` | 298 896 | `934604bb0b4c27e1bdc0540894b71be4b951cdca9850c4de2d057e450cc201b2` | 10 |

> ⚠ **Three mirrors, three different Panasonic revisions — this matters for the part number.**
> The `201303` revision prints this socket as **`AXE512124`** (surface-treatment digit `4`),
> and **neither** 2013 revision documents the `D` package suffix at all, so `AXE512127D`
> appears only in the Digi-Key copy. Full comparison, ordering-key decode and consequences:
> [**`../a4s-series-datasheet-revisions.md`**](../a4s-series-datasheet-revisions.md)
> *(added 2026-09-20).* D2's earlier "not retained (duplicate)" status was **refuted** — the
> three copies are not the same document.

**Method note.** D1 validated as `%PDF` (`executed-success`) and full-text
searched: `AXE512127` occurs three times and `AXE512127D` once, in the 4 mm
embossed-packaging table beside `AXE612124D` on the 12-pin row — which is how the
socket/header pairing and the pin count were established rather than inferred.
The same file is held under the [header's record](../axe612124d/README.md)
because both records are read standalone; it is one document, byte-identical, and
its hash is the same in both places.
