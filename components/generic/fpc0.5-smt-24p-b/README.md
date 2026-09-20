# FPC0.5-SMT-24P-B — e-paper panel FPC connector (manufacturer **unidentified**)

> **24-contact, 0.5 mm-pitch flat-flex (FPC) connector**, surface-mount. Fitted as **`J5` on sheet 4** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153). It is the board's interface to the e-paper display module.
> Research snapshot **2026-09-01**. **The manufacturer and the true ordering part number were not established** — see [§2](#2--the-part-number-is-a-library-designation-not-an-orderable-part).
> **No hardware was available.** The pinout below is nevertheless solid: it is confirmed twice, independently.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH-V]** | Read off sheet 4 of `PaperMono_SCH_V0.6.2_20260522.pdf` rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[SCH-M]** | Recovered from the schematic's `PI` pin-marker layer | `executed-success` for the extraction |
| **[MAN]** | DKE **EPD Module User Manual** p. 7, held at [`components/dke/depg0397bbs770f3/artifacts/`](../../dke/depg0397bbs770f3/artifacts/) | `not-tested` |
| **[SRC]** | M5Stack source at a cited `file:line` | `executed-success` for the read |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Designation on the schematic | **`FPC0.5-SMT-24P-B`** | **[SCH-V]** |
| Manufacturer | **unidentified** — §2 | — |
| Function | 24-way flat-flex connector, board-to-FPC | **[SCH-V]** |
| Contacts | **24** | **[SCH-M]** — 24 `PI` markers, `J5`.1 … `J5`.24 |
| Pitch | **0.5 mm**, from the name | **[INF]** |
| Mount | **SMT**, from the name | **[INF]** |
| Reference designator | **`J5`**, sheet 4 | **[SCH-V]** |
| Mates with | the [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) panel's 24-pin FPC tail | **[MAN]** |
| Datasheet | **none found** — §5 | — |

---

## 2. ⚠ The part number is a library designation, not an orderable part

`FPC0.5-SMT-24P-B` decomposes transparently: **FPC**, **0.5** mm pitch,
**SMT** mount, **24P** contacts, variant **B**. That is a *description*, and it
is how EDA library symbols are commonly named when the librarian does not want
to bind the schematic to one vendor.

**Searching for it as a part number returns nothing.** A query against LCSC /
JLCPCB's catalogue for the exact string produced **no result**. Near-neighbour
parts in the same class exist in quantity —

| Part found | Vendor | Note |
|---|---|---|
| `HC-FPC-0.5-24P-FH20` | Hong Cheng | 24P, 0.5 mm, 2.0 mm height, flip-top, bottom contact |
| `FPC-0.5-24P-H20` | SHOU HAN | 24P, 0.5 mm, right-angle SMT |
| `FPC-05F-6PH20`, `FPC-05F-8PH20` | XUNPU | same series, different contact counts |

— and **none of them is this part.** XUNPU supplies both of this board's other
connectors ([USB-C](../typec-302-brp16sc08/README.md) and
[board-to-board](../btb0.408-10plbdr-g41/README.md)), so a XUNPU FPC connector
is a *plausible* candidate. **That is a hypothesis and it is deliberately not
promoted to a finding.** No part number is asserted here.

### What would resolve it

1. **A photograph of the connector body on an assembled PaperMono.** FPC
   connector housings usually carry no marking, so this may not settle it either.
2. **M5Stack's manufacturing BOM**, which is not published.
3. **A replacement-part or repair listing** from M5Stack or a reseller.
4. The **`-B` suffix** is the one genuinely discriminating token; a vendor whose
   series uses a trailing `-B` for a variant (contact side, latch style, height)
   would be a strong lead.

Two properties the schematic does **not** state, and which matter for
substitution:

- **Contact side** — top-contact or bottom-contact. This determines which way up
  the panel's flex tail must be inserted, and getting it wrong reverses the
  entire pinout.
- **Latch style** — flip-lock, slide-lock or ZIF-less. Determines assembly and
  serviceability.

---

## 3. Used By

### `devices/m5stack/papermono` — `J5`, sheet 4

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md).
The **[PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) uses
the same panel and the same connector**: both product pages carry an identical
display specification and link the same 3.97-inch datasheet. The Lite's
schematic is published only as a 4-sheet `PRJ` PDF, so its `J5` wiring is
`inferred`, not independently read.

### 3.1 Pinout — established, and cross-checked against the panel manual

This is the pinout's strongest property: **two independent documents agree
position for position**. The left three columns are the panel's own pin
assignment from **[MAN]** p. 7; the right two are how the PaperMono wires them
**[SCH-V]** / **[SCH-M]**.

| Pin | Panel signal **[MAN]** | I/O | PaperMono net | Goes to |
|---:|---|---|---|---|
| 1 | `NC` | — | — | keep open |
| 2 | **`GDR`** | O | `GDR` | **gate of `Q4`** ([CJ2310](../../changjing/cj2310/README.md)) — the panel's external boost NMOS |
| 3 | **`RESE`** | I | `RESE` | current-sense node: `Q4` source through **`R59` = 1.2 Ω** |
| 4 | `VDHR` | C | — | `C74` = 4.7 µF/25 V |
| 5 | `VDHR`/`NC` region | C | — | `C75` = 4.7 µF/25 V |
| 6 | `NC` (temp-sensor SCL) | O | — | not used |
| 7 | `NC` (temp-sensor SDA) | I/O | — | not used |
| 8 | **`BS`** | I | — | bus-interface select; **`R60` = 0 Ω** sets 4-wire SPI |
| 9 | **`BUSY_N`** | O | `G18_EINK_BUSY` | **ESP32-S3 GPIO18** |
| 10 | **`RST_N`** | I | `PYB_EINK_RST` | **[M5IOE1](../../m5stack/m5ioe1/README.md) `IO5`** — *not* an ESP32 pin; `R61` = 0 Ω in series |
| 11 | **`DC`** | I | `G17_EINK_DC` | **ESP32-S3 GPIO17** |
| 12 | **`CSB`** | I | `G16_EINK_CS` | **ESP32-S3 GPIO16** |
| 13 | **`SCL`** | I | `G15_SPI2_CLK` | **ESP32-S3 GPIO15** |
| 14 | **`SDA`** | I/O | `G14_SPI2_MOSI` | **ESP32-S3 GPIO14** |
| 15 | **`VDDIO`** | P | `EPD_3V3_L3` | rail gated by M5IOE1 `IO3` |
| 16 | `VDD` | P | `EPD_3V3_L3` | `C77` = 10 µF/25 V |
| 17 | `GND` | P | `GND` | |
| 18 | `VDDD` | C | — | `C79` = 1 µF/25 V |
| 19 | `VPP` | P | — | test pin, keep open |
| 20 | `VSH` | C | — | `C81` = 4.7 µF/25 V |
| 21 | `VGH` | C | `PREVGH` | fed by the §3.2 boost; `C82` = 4.7 µF/25 V |
| 22 | `VSL` | C | — | `C83` = 4.7 µF/25 V |
| 23 | `VGL` | C | `PREVGL` | fed by the §3.2 charge pump |
| 24 | `VCOM` | C | — | `C84` = 1 µF/25 V |

Signal-to-GPIO assignments are corroborated a third time by M5Stack's own driver
**[SRC]**: `EDP_SPI.cpp:26–30, 37–38` and `M5GFX.cpp:2085, 2106–2125`.

> The [device record already notes](../../../devices/m5stack/papermono/pinouts-and-buses.md)
> that this FPC pinout "matches the DKE panel manual's Input/Output Pin
> Assignment table (p. 7) position for position — an independent cross-check that
> the schematic extraction is being read correctly." This record reproduces that
> table so the connector can be understood without opening the panel record.

### 3.2 The connector carries a switching converter, not just logic

Pins 2, 3, 21 and 23 are not signals in the usual sense. The SSD1677 inside the
panel runs its own DC/DC, but the **inductor, switch, rectifier and charge pump
are on the mainboard** and reach the die through this connector:

```
EPD_3V3_L3 ──[ L8 33 µH ]──┬──▶|── D4 ──┬── PREVGH ── J5.21
  SPH252010H330MT          │            │            (C72 10 µF/25 V)
                     Q4 drain           └─┤C67 10 µF/25 V├─┬─ D5 ─┘
  J5.2 GDR ──┬── Q4 gate (CJ2310)                          └─ D6 ─ GND
             │                                             │
         R58 10 kΩ                            PREVGL ── J5.23  (C73 10 µF/25 V)
             │
            GND     Q4 source ── R59 1.2 Ω ── GND
                              └── J5.3 RESE
```

**[SCH-V]**, and it matches DKE's own typical application circuit **[MAN]** §7.4.

Two practical consequences:

1. **This connector carries high-voltage rails.** `PREVGH` and `PREVGL` are the
   panel's gate-drive supplies; the decoupling around pins 17–24 is rated
   **25 V**, and `D4`/`D5`/`D6` are 40 V parts. Treat pins 20–24 as high-voltage
   when probing, and do not hot-plug the flex.
2. **`GDR` and `RESE` are a current-mode switching loop closed through a
   connector.** Contact resistance is in that loop. A dirty or partially inserted
   FPC does not fail cleanly — it changes the sense voltage across `R59` = 1.2 Ω
   and therefore the peak current, which shows up as display artefacts rather
   than as an obvious dead panel. **[INF]** This is worth knowing before chasing
   a refresh-quality bug in software.

---

## 4. Substitution guidance

**The functional pinout is fixed by the panel**, so any 24-way 0.5 mm FPC
connector is a *functional* candidate. What is not interchangeable:

| Property | Why it blocks a swap |
|---|---|
| **Contact side** (top vs bottom) | Reverses the flex orientation — pin 1 lands on pin 24 |
| **Footprint** | Pad pitch is fixed at 0.5 mm but pad length, latch-anchor pads and body width are not |
| **Height** | The PaperMono is a thin device; a 2.0 mm-tall flip-top may not fit under the panel |
| **Latch mechanism** | Affects assembly force and whether the flex can be reseated |

Since **M5Stack does not publish the PCB layout**, none of these can be matched
from this record. A substitution needs a physical board.

---

## 5. Datasheet search — negative result

**No datasheet was found, and none is expected to exist**, because the string is
a library designation rather than a manufacturer's ordering code (§2).

| Attempt | Result |
|---|---|
| JLCPCB SMT parts API, exact keyword `FPC0.5-SMT-24P-B` | **no results** |
| Same API, `FPC0.5-SMT-24P` | only JLCPCB-internal assembly SKUs, no vendor part |
| Same API, `FPC-0.5-24P` | Hong Cheng and SHOU HAN parts — **different part numbers**, not this one |
| Same API, `0.5mm 24P FPC connector XUNPU` | XUNPU `FPC-05F-*` series, 6P and 8P — right family, wrong contact count, and the naming pattern does not match |
| DuckDuckGo-lite, Mojeek, searx.be via `curl` | **all blocked or captcha'd** on 2026-09-01; no result obtained by general web search |

Date of search: **2026-09-01**. This is a recorded negative result: it should not
be repeated without new evidence of the kind listed in §2.

---

## 6. Open questions

- Manufacturer and ordering part number (§2).
- Contact side (top or bottom) and latch style — both needed for any repair.
- Current and voltage rating per contact. Unstated, and non-trivial here because
  pins 21/23 carry the panel's gate-drive rails.
- Insertion-cycle rating — relevant because the flex is a serviceable joint.
- Whether the PaperMono-Lite fits the same connector (`inferred`, §3).

---

## Manufacturer

**Unidentified.** No vendor sourcing guide applies. If the part is later
established as XUNPU — the vendor of this board's two other connectors — the
retrieval notes in the
[TYPEC-302-BRP16SC08 record](../typec-302-brp16sc08/README.md#manufacturer)
apply, in particular the `wmsc.lcsc.com` vs `www.lcsc.com/datasheet` trap.

## Related pages

- [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) — the panel on the other end, and the source of the §3.1 table
- [Solomon Systech SSD1677](../../solomon-systech/ssd1677/README.md) — the controller whose DC/DC §3.2 serves
- [Changjing CJ2310](../../changjing/cj2310/README.md) — `Q4`, the boost NMOS driven by `J5`.2
- [1N5819WS](../1n5819ws/README.md) — `D4`/`D5`/`D6` in the same converter
- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — owns the panel reset and rail enable
- [PaperMono bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | the designation `FPC0.5-SMT-24P-B`, 24 pin markers, the §3.1 net column, the §3.2 converter | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| M1 | EPD Module User Manual, p. 7 §5 *Input/output Pin Assignment* | DKE | primary | see the [panel record](../../dke/depg0397bbs770f3/README.md#12-authoritative-sources) | 2026-09-01 | 30 pp, drawing `REV. A0` 2024-09-29 | the §3.1 panel-signal column | `../../dke/depg0397bbs770f3/artifacts/depg0397bbs770f3-epd-module-user-manual.pdf` |
| S2 | `M5PaperMono-UserDemo` `EDP_SPI.cpp`, `M5GFX.cpp` | M5Stack | primary | <https://github.com/m5stack/M5GFX> | 2026-09-01 | MIT | third corroboration of the GPIO assignments | `../../../scratch/m5stack-papermono/repos/` |

**Local artifacts** — none. No datasheet exists for this designation (§5); the
panel manual that supplies the pin assignment is held under the
[panel's own record](../../dke/depg0397bbs770f3/README.md) and is cited from
there rather than duplicated.
