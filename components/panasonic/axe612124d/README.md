# Panasonic AXE612124D

> **A4S-series narrow-pitch board-to-board connector — the HEADER half.** 0.4 mm pitch, **12 contacts**, 0.8 mm mated height, 2.0 mm body width, gold-plated, RoHS.
> Research snapshot **2026-09-01**. Fitted as **`J1` on sheet 5** of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — i.e. on the **KEY / RGB / PDM sub-board**, mating the [`AXE512127D`](../axe512127d/README.md) socket at `J6` on the mainboard.
> **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Panasonic **A4S (0.4 mm pitch)** series datasheet, `ACCTB7E 201602-T`, issued **2016-02-29**; local copy `artifacts/panasonic-a4s-series-connectors-digikey-mirror.pdf` | `not-tested` |
| **[SCH-V]** | Read off sheet 5 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **`AXE612124D`** | **[SCH-V]**; **[DS]** p. 2 |
| Manufacturer | **Panasonic Industry** | **[DS]** |
| Series | **A4S**, 0.4 mm pitch narrow-pitch connectors | **[DS]** |
| Half | **Header** (`AXE6…`) | **[DS]** ordering key |
| Mating half | **[`AXE512127D`](../axe512127d/README.md)** — Socket | **[DS]** p. 2, 12-pin row |
| Contacts | **12** | **[DS]**; **[SCH-V]** |
| Pitch | **0.4 mm** | **[DS]** |
| Mated height | **0.8 mm** | **[DS]** — the `1` in position 4 of the code |
| Body | **4.20 × 2.00 mm**, height **0.65 mm** | **[DS]** header dimension table, 12-pin row |
| Suffix `D` | 4 mm-pitch embossed packaging, 15 000 pcs/reel | **[DS]** |
| Unit weight | 0.01 g (20-pin reference) | **[DS]** |

### 1.1 Header vs socket — what actually differs

| | Socket `AXE512127D` | **Header `AXE612124D`** |
|---|---|---|
| Body length `A` (12 pin) | 4.90 mm | **4.20 mm** |
| Body width | 2.50 mm | **2.00 mm** |
| Height | 0.77 mm | **0.65 mm** |
| Terminal coplanarity | 0.08 mm | 0.08 mm |
| Plating, soldering terminals | Ni base + **Pd + Au flash** | Ni base + **Au** |
| Contact construction | **bellows contacts**, Ni barriers, contact holding force min. 0.20 N/contact | **posts** |
| 1.0 mm-height variant | **same socket** serves 0.8 and 1.0 mm | **different header** (`AXE612224D`) |

**[DS]** pp. 3–4. The last row is the useful one: Panasonic keeps one socket
across both stack heights and changes only the header, *"for the same foot
pattern"*. Raising or lowering the sub-board on this design therefore means
changing **this** part and not `J6`.

The full electrical, mechanical and environmental specification is shared by both
halves and is **tabulated once**, in the
[socket record §2](../axe512127d/README.md#2-specifications-ds-p-3) — rated
current **0.3 A per contact** (5 A total), rated voltage **60 V**, contact
resistance **max 90 mΩ**, **30 insertion/removal cycles**, −55 °C to +85 °C, LCP
UL94V-0 body.

> ⚠ **30 insertion/removal cycles**, as for the socket. The sub-board joint is an
> assembly interconnect, not a serviceable connector. **[DS]**

---

## 2. Used By

### `devices/m5stack/papermono` — `J1`, sheet 5

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), on
the **KEY / RGB / PDM sub-board** documented by
`PaperMono KEY RGB.SchDoc` (sheet 5, title block dated **2026-04-14**). That
board carries three tactile switches `S1`–`S3`, the
[RS-C1415MBAR](../../generic/rs-c1415mbar-rgb-led/README.md) RGB indicator, the
[LMD4737T261-AC02](../../generic/lmd4737t261-ac02-pdm-microphone/README.md) PDM
microphone and three [ESD5311](../../generic/esd5311/README.md) clamps.

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):**
`inferred` **yes** — the Lite keeps the buttons, RGB LED and microphone, and
differs only in dropping NFC and LoRa. Not read from the Lite's own schematic,
which is published only as a 4-sheet `PRJ` PDF.

> ⚠ **Sheet 5 is a different Altium document**, so its `J1` is unrelated to `J1`
> on sheet 2 (the frontlight connector) and to `J1` on sheet 6 (the NFC
> board-to-board). Cite it as **`J1` sheet 5**. See the
> [BOM's designator-collision table](../../../devices/m5stack/papermono/bill-of-materials.md#3--designators-repeat-across-sheets--a-designator-alone-is-meaningless).

### 2.1 Pinout **[SCH-V]**

Identical to the socket's, which is the evidence that the pair mates 1↔1: both
symbols were rendered at 200 dpi and read independently, and every net matches.

| Pin | Net | On the sub-board |
|---:|---|---|
| **1** | `3V3_L0` | always-on rail — feeds `R1` = 10 kΩ, the **power-button pull-up** |
| **2** | `GND` | tied to end tabs 13/14 |
| **3** | `3V3_L2` | main system rail; **`C5` = 10 µF/10 V** bulk, and the pull-ups `R2`/`R5` = 10 kΩ for the two user keys |
| **4** | `PDM_VDD` | microphone rail; `L1` = 2 nH and `C2` = 100 nF/10 V feed `U1` sheet 5 |
| **5** | `PY_LED_R` | RGB red, ballast **`R8` = 1 kΩ** |
| **6** | `PWR_BTN` | switch `S1`, clamp `DR1`, debounce `C1` = 100 nF/10 V |
| **7** | `PYB_LED_G` | RGB green, ballast **`R7` = 820 Ω** |
| **8** | `G2_KEY1` | switch `S2`, clamp `DR2`, debounce `C3` = 100 nF/10 V |
| **9** | `PYB_LED_B` | RGB blue, ballast **`R6` = 560 Ω** |
| **10** | `G3_KEY2` | switch `S3`, clamp `DR3`, debounce `C4` = 100 nF/10 V |
| **11** | `G46_PDM_DAT` | PDM data, **`R3` = 22 Ω** series |
| **12** | `G45_PDM_CLK` | PDM clock, **`R4` = 22 Ω** series |
| 13, 14 | `GND` | **soldering tabs**, tied, one end |
| 15, 16 | `GND` | soldering tabs, tied, other end |

**Two rails cross this connector, and the split is deliberate.** Pin 1 carries
`3V3_L0` (always on) and pin 3 carries `3V3_L2` (switched off in the deep power
states). The **power button pulls up to `3V3_L0`** while the two **user keys pull
up to `3V3_L2`** — so at the lowest power level only the power button can be
sensed at all. That matches sheet 1's power-state table, which lists the power
button as the `L0`/`L1` wake path and the keys only from `L2`. **[SCH-V]** +
**[INF]**

### 2.2 The `MP` positions

Pins 13–16 are the connector's four **metal soldering terminals**, numbered by
the library symbol. Panasonic's dimension drawing notes that *"since the
soldering terminals has a single-piece construction, sections Y and Z are
electrically connected"*, which is why the schematic ties 13↔14 (with pin 2) and
15↔16 and takes both to ground. **[DS]** + **[SCH-V]** — full discussion in the
[socket record §3.2](../axe512127d/README.md#32-pins-1316-are-soldering-tabs-and-the-datasheet-explains-the-tie).

---

## 3. Substitution

| Change | Part |
|---|---|
| **1.0 mm stack** instead of 0.8 mm | **`AXE612224D`** — socket unchanged **[DS]** |
| 8 mm tape instead of 4 mm | `AXE612124` (drop the `D`), 5000/reel |
| Different contact count | `AXE6xx124D` for xx ∈ {10, 12, 14, 16, 20, 24, 30, 34, 40, 44, 50, 60, 64} in `D` packaging **[DS]** p. 2 |

Outside the series: Hirose **DF40C** (documented
[here](../../hirose/df40c-30dp-0.4v/README.md)), JAE **WP7B**, Molex
**SlimStack**. None is a footprint drop-in, and **the header and socket must be
changed as a pair** — an A4S header will not mate a DF40 socket.

---

## 4. Integration pitfalls

1. **30 mating cycles** — the joint is not built for repeated service.
2. **0.3 A per contact**, and `3V3_L0`, `3V3_L2` and `PDM_VDD` each cross on a
   single contact. The RGB LED, the microphone and the pull-ups all draw through
   those three. Not measured. **[INF]**
3. **Header and socket are separate orderable parts** — replacing one without the
   other, or mixing 0.8 mm and 1.0 mm halves, gives a connector that appears to
   mate but does not seat.
4. **`3V3_L0` and `3V3_L2` are adjacent-ish contacts (1 and 3) on a 0.4 mm
   pitch.** A solder bridge there ties an always-on rail to a switched one, which
   would defeat the board's whole power-domain scheme and present as "the device
   will not power down". **[INF]**
5. **Three ESP32-S3 strapping pins cross this joint** (GPIO3, GPIO45, GPIO46) —
   see the [socket record §3.1](../axe512127d/README.md#31-pinout-sch-v--identical-on-both-halves).

---

## 5. Open questions

- The `24` field of `AXE612124D` (plating / variant) is decoded only as far as
  Panasonic's published ordering key allows.
- Whether M5Stack fits `D` or plain packaging in production — a packaging choice,
  not a part change.
- Per-contact derating with all 12 loaded; the datasheet gives no curve.
- No hardware measurement of retention force, contact resistance or seating.

---

## Manufacturer

**Panasonic Industry.** No vendor sourcing guide exists in this repository yet.
The retrieval findings for this document — Panasonic's own CDN 404s, Digi-Key's
`media.digikey.com` works first try, and Mouser's specsheet host served the real
PDF **only** to the `WhatsApp/2.23.20.0` user-agent — are recorded once, in the
[socket record's Manufacturer section](../axe512127d/README.md#manufacturer),
and belong in
[`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Related pages

- [Panasonic AXE512127D](../axe512127d/README.md) — **the mating socket**, `J6` sheet 4, and the shared specification table
- [RS-C1415MBAR](../../generic/rs-c1415mbar-rgb-led/README.md) · [LMD4737T261-AC02](../../generic/lmd4737t261-ac02-pdm-microphone/README.md) — the sub-board's active parts
- [ESD5311](../../generic/esd5311/README.md) — `DR1`–`DR3` on the same sub-board
- [Hirose DF40C-30DP-0.4V(51)](../../hirose/df40c-30dp-0.4v/README.md) — comparable 0.4 mm board-to-board
- [PaperMono bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| D1 | Narrow pitch connectors **A4S (0.4 mm pitch)** | Panasonic (via Digi-Key mirror) | primary, via distributor mirror | <https://media.digikey.com/pdf/Data%20Sheets/Panasonic%20Electric%20Works%20PDFs/A4S_Series.pdf> | 2026-09-01 | **`ACCTB7E 201602-T`**, issued **2016-02-29**, 11 pp, 399 357 B, AES-encrypted | the socket/header pairing on the 12-pin row, header dimensions, the shared specification, the soldering-terminal note | `artifacts/panasonic-a4s-series-connectors-digikey-mirror.pdf` |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `J1` sheet 5 = `AXE612124D`, the §2.1 pinout, the two-rail split | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/panasonic-a4s-series-connectors-digikey-mirror.pdf` | 399 357 | `292023186ef0758f1862f8aa2a5f545dc1c14659f4ba84f14f7183f6385503b4` | 11 |

**Method note.** One document covers both halves of the pair. It is held under
**both** records deliberately, byte-identical and with the same SHA-256, because
each record is read standalone and a reader arriving at the header should not
have to know the socket's part number to find the datasheet. `AXE612124D` occurs
once in the file, in the 4 mm embossed-packaging table beside `AXE512127D` — that
line is the whole basis for asserting the pairing.
