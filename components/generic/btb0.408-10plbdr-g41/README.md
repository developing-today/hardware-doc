# XUNPU BTB0.408-10PLBDR-G41

> **0.4 mm-pitch board-to-board connector**, 10 contacts in 2 rows, 0.8 mm mated height, 300 mA / 30 V, copper alloy, vertical surface mount.
> Research snapshot **2026-09-01**. Used **twice** on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153): **`J3` on sheet 4** (mainboard) and **`J1` on sheet 6** (NFC sub-board) — the two halves of one joint.
> **No datasheet exists** for this part anywhere reachable ([§5](#5-datasheet-search--negative-result)). **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[CAT]** | LCSC / JLCPCB catalogue entry `C42420580`, retrieved 2026-09-01 | `not-tested` |
| **[SCH-V]** | Read off sheets 4 and 6 rendered to PNG at 200 dpi | `executed-success` for the reading |
| **[SCH-M]** | Recovered from the schematic's `CO`/`PI` marker layer | `executed-success` for the extraction |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **`BTB0.408-10PLBDR-G41`** | **[SCH-V]**, **[CAT]** |
| Manufacturer | **XUNPU** (深圳市讯普电子有限公司) | **[CAT]** |
| LCSC part | **`C42420580`** | **[CAT]** |
| Function | Board-to-board / backplane connector | **[CAT]** |
| **Pitch** | **0.4 mm** | **[CAT]** |
| **Mated height** | **0.8 mm** | **[CAT]** |
| **Contacts** | **10**, in **2 rows** | **[CAT]** |
| Current rating | **300 mA** | **[CAT]** |
| Voltage rating | **30 V** | **[CAT]** |
| Contact material | copper alloy | **[CAT]** |
| Mount | surface mount, **vertical** | **[CAT]** |
| Operating temperature | **−35 °C to +85 °C** | **[CAT]** |
| RoHS | yes | **[CAT]** |
| Datasheet | **none — see §5** | — |

### 1.1 Reading the part number

`BTB` **0.4** **08** — **10P** — **LBDR** — **G41**, i.e. **B**oard-**T**o-**B**oard,
**0.4 mm pitch**, **0.8 mm** mated height, **10 positions**. The trailing fields
are XUNPU's own variant coding and **were not decoded**; guessing what `LBDR` or
`G41` select would be exactly the kind of promotion-of-a-candidate the research
method forbids. The decoded fields are all independently confirmed by the LCSC
parametric entry (§1), which is why they are asserted and the rest is not.

> ⚠ **The schematic labels *both* halves of the pair `BTB0.408-10PLBDR-G41`.**
> A board-to-board joint needs a plug and a receptacle, which are ordinarily two
> different orderable parts. One of the two symbols almost certainly carries the
> wrong part string. Which one could not be determined, and it feeds directly
> into the conflict in §3.3. **[SCH-V]**

---

## 2. The symbol has 14 pins; the connector has 10 contacts

Both symbols carry 14 pin markers **[SCH-M]**. Numbers 1–10 take the signals;
**11, 12, 13 and 14 are all tied to `GND`** — 11+12 as a pair at one end, 13+14
as a pair at the other. **[SCH-V]**

Given a part number that says **10P** and an LCSC entry that says **10 contacts,
2 rows**, positions 11–14 are the four **mounting posts / soldering tabs**, given
pin numbers by the library symbol so they can be netted to ground. This is the
same convention the board's Panasonic
[A4S connectors](../../panasonic/axe512127d/README.md#32-pins-1316-are-soldering-tabs-and-the-datasheet-explains-the-tie)
use, where the manufacturer's drawing states it explicitly. Here **no drawing
exists to confirm it**, so it is `inferred` — strongly, but inferred.

This reconciles the [device record's](../../../devices/m5stack/papermono/pinouts-and-buses.md)
"10" with the raw marker count of 14. Not a contradiction: **10 contacts plus 4
tabs**.

---

## 3. Used By

### `devices/m5stack/papermono` — `J3` sheet 4 **and** `J1` sheet 6

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md). This
is the joint between the mainboard and the **NFC sub-board**
(`02 Paper Mono NFC.SchDoc`, title block `Paper Mono NFC`, `2/2`, `V0.2`, dated
**2026-07-28**), which carries the
[ST25R3916](../../stmicroelectronics/st25r3916/README.md), its
[27.12 MHz crystal](../xl7el89cmi-111ylc-27.12mhz-crystal/README.md), the
matching bank and a 4-turn 25 × 25 mm PCB loop antenna.

**On the [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md):
NO.** The Lite drops NFC entirely — that and LoRa are the whole difference
between the two SKUs. There is no NFC sub-board and therefore **no reason for
this connector to be fitted at all**. Whether the mainboard still carries the
unpopulated `J3` footprint is not established. `inferred`.

### 3.1 `J3` — mainboard half, sheet 4 **[SCH-V]**

| Pin | Net | Notes |
|---:|---|---|
| 1 | `GND` | |
| **2** | **`3V3_L2`** | decoupled by `C59` = 10 µF/10 V |
| 3 | — | stub, no net label |
| **4** | **`G48_SYS_SCL`** | system I²C clock |
| 5 | — | stub |
| **6** | **`G47_SYS_SDA`** | system I²C data |
| 7 | — | stub |
| **8** | **`G6_RFID_INT`** | ST25R3916 `IRQ` → ESP32-S3 GPIO6 |
| 9 | — | stub |
| **10** | **`PYB_NFC_EN`** | carries a red ✗ marker; the sheet annotates *"`PYB_NFC_EN` is a spare GPIO pin"* |
| 11, 12 | `GND` | tab pair |
| 13, 14 | `GND` | tab pair |

### 3.2 `J1` — NFC sub-board half, sheet 6 **[SCH-V]**

| Pin | Net | Notes |
|---:|---|---|
| **1** | **`3V3_L2` → `VCC_3V3`** | through `R1` = 0 Ω and the `U1` [AW35122FDR](../../awinic/aw35122/README.md) load switch; `C1` = 10 µF |
| 2 | `GND` | |
| **3** | **`G48_SYS_SCL`** | |
| 4 | — | stub |
| **5** | **`G47_SYS_SDA`** | |
| 6 | — | stub |
| **7** | **`G6_RFID_INT`** | |
| 8 | — | stub |
| **9** | **`PYB_RFID_RST`** | same wire as `PYB_NFC_EN`; drives the load-switch enable |
| 10 | — | stub |
| 11, 12 | `GND` | tab pair |
| 13, 14 | `GND` | tab pair |

### 3.3 ⚠ **Unresolved conflict — the two halves do not agree on pin numbering**

Put the two tables side by side and the same signal appears on a different pin
number on each board:

| Signal | `J3` (mainboard, sheet 4) | `J1` (NFC board, sheet 6) |
|---|---:|---:|
| `GND` | **1** | **2** |
| 3V3 | **2** | **1** |
| `G48_SYS_SCL` | **4** | **3** |
| `G47_SYS_SDA` | **6** | **5** |
| `G6_RFID_INT` | **8** | **7** |
| enable / "reset" | **10** | **9** |

`J3` puts every signal on an **even** pin; `J1` puts every signal on an **odd**
pin. Both symbols mark pin 1 with a polarity dot, and both were read from 200 dpi
renders, twice, so this is not an extraction artefact.

**If pin *N* mated pin *N*, this connector would short `3V3_L2` to `GND`.** It
plainly does not do that in a shipping product, so one of two things is true:

| Reading | Implication |
|---|---|
| **A — deliberate.** The two halves are numbered from each board's own pin 1, and flipping a two-row connector over swaps the rows, so *odd mates even* by construction | The design is correct as drawn, and anyone reproducing it must replicate the same numbering convention |
| **B — a drawing error.** One symbol's pin numbering (or its part string, §1.1) is wrong, and the PCB layout silently does the right thing | The schematic is misleading; only the layout is authoritative |

**This record does not choose between them.** Most board-to-board pairs from
mainstream vendors are designed to mate 1↔1 — but those pairs also have *two
different part numbers*, and this one does not. Both anomalies point the same
way and neither can be settled from the published evidence.

**What is certain, and is enough for most purposes:**

- The **signal set** across the joint: `3V3_L2`, `GND`, `G48_SYS_SCL`,
  `G47_SYS_SDA`, `G6_RFID_INT`, and the enable line. Six nets, four grounds, four
  unused positions.
- **Each board's own net-to-pin mapping**, which is what firmware and net-level
  debugging need.

**What must not be assumed:** that `J3` pin *N* is electrically `J1` pin *N*.
**Anyone designing a replacement NFC sub-board must verify the physical mapping
against a real board or the connector's true datasheet, which does not exist
(§5).** Getting this wrong applies 3.3 V to a ground pin.

### 3.4 `PYB_NFC_EN` / `PYB_RFID_RST` — a power cut, not a reset

Already established in
[`gaps-and-conflicts.md`](../../../devices/m5stack/papermono/gaps-and-conflicts.md)
R9: the two names are the same wire across this connector, it drives an
[AW35122FDR](../../awinic/aw35122/README.md) load-switch enable, and the
ST25R3916 **has no reset pin in any package** — so asserting it removes power
rather than resetting the device. The `_RST` half of the name is misleading.

This record adds one wrinkle, from the sheet-6 side: **`R2`, the resistor drawn
between `PYB_RFID_RST` and `U1`'s `EN`, carries the value `NC` — not fitted** —
and the mainboard side marks pin 10 with a red ✗ and the note *"spare GPIO pin"*.
**[SCH-V]** So as drawn, it is not clear that the enable line reaches the load
switch at all. What actually enables the NFC rail was **not resolved**; the
answer may be on **NFC sheet 1 of 2, which M5Stack does not publish**.

---

## 4. Substitution

There is no datasheet, no footprint drawing and no published PCB layout, so a
substitution cannot be specified from this record. What is known:

| Property to match | Value |
|---|---|
| Pitch | 0.4 mm |
| Mated height | 0.8 mm |
| Contacts | 10, two rows |
| Current | ≥ 300 mA per contact |

Parts in the same class include Panasonic **A4S** (which this very board uses
elsewhere — see [AXE512127D](../../panasonic/axe512127d/README.md), documented
with a real datasheet), Hirose **DF40C**
([documented here](../../hirose/df40c-30dp-0.4v/README.md)), JAE **WP7B** and
Molex **SlimStack**. **None of these is claimed to be a drop-in**; the footprint
is unknown.

> Note the mild irony worth recording: the same board uses a **fully documented
> Panasonic 0.4 mm connector** for the KEY/RGB joint and an **undocumented XUNPU
> 0.4 mm connector** for the NFC joint. If a redesign wanted one connector family
> across both joints, the A4S side is the one with a datasheet.

---

## 5. Datasheet search — negative result

**No datasheet was found. This is a recorded negative result.**

| Attempt | Result |
|---|---|
| JLCPCB SMT parts API, exact keyword `BTB0.408-10PLBDR-G41` | **found the part** (`C42420580`, XUNPU) — but the record's `dataManualUrl` field is **`None`** and `lcscGoodsUrl` is **`None`** |
| LCSC product page | none exists for this part code; the catalogue entry carries parametric data only |
| `wmsc.lcsc.com` CDN, the path pattern that works for this board's other XUNPU part | no candidate stamp/filename to construct a URL from |
| DuckDuckGo-lite, Mojeek, searx.be via `curl` | **all blocked or captcha'd** on 2026-09-01 |

So the **entire specification in §1 comes from LCSC's parametric fields** — a
distributor's transcription, not the manufacturer's document. It should be
treated accordingly: good enough to identify the part, not good enough to
qualify a design against.

Date of search: **2026-09-01**.

**What would resolve it:** XUNPU's own catalogue (the company distributes almost
exclusively through LCSC and has little independent web presence); a Chinese-
language connector distributor listing the `BTB0.4xx` series; or M5Stack's
manufacturing BOM.

---

## 6. Integration pitfalls

1. **The mating pin correspondence is unresolved and a wrong assumption shorts a
   rail** (§3.3). This is the single most important item on this page.
2. **300 mA per contact**, and `3V3_L2` crosses on **one** contact to power the
   entire NFC sub-board. The ST25R3916's transmitter is the load that matters and
   its peak draw was not measured. **[INF]**
3. **No datasheet** (§5) — no retention force, no mating-cycle rating, no
   footprint, no reflow profile.
4. **Both halves carry the same part string** (§1.1), so ordering "the part on the
   schematic" gets you two of one half.
5. **The enable path is drawn through an unfitted resistor** (§3.4).
6. **−35 °C lower limit**, narrower than the Panasonic connector's −55 °C on the
   same product. Irrelevant indoors; relevant to any outdoor claim.

---

## 7. Open questions

- Which half is the plug and which the receptacle, and what the true part number
  of the other half is (§1.1).
- Whether pin *N* mates pin *N* (§3.3) — **the blocking question**.
- Whether positions 11–14 are really mounting tabs (§2) — `inferred`, unconfirmed.
- What drives the NFC load switch's enable (§3.4) — likely answered by the
  unpublished NFC sheet 1 of 2.
- Whether the PaperMono-Lite mainboard retains an unpopulated `J3` footprint.
- Mating-cycle rating, retention force, footprint — all absent (§5).

---

## Manufacturer

**XUNPU** (深圳市讯普电子有限公司), a Shenzhen connector maker distributed almost
entirely through LCSC. No vendor sourcing guide exists in this repository yet.

XUNPU also supplies this board's
[USB-C receptacle](../typec-302-brp16sc08/README.md), for which a (text-layer-free,
one-page) drawing **does** exist on the `wmsc.lcsc.com` CDN. **The contrast is the
useful finding: XUNPU part coverage on LCSC is inconsistent — some parts carry a
`dataManualUrl`, others carry `None`, and there is no fallback host.** Check the
API's `dataManualUrl` field before spending time constructing CDN URLs by hand.

Part discovery used JLCPCB's SMT parts API, which unlike DuckDuckGo-lite, Mojeek
and searx.be was not bot-filtered on 2026-09-01:

```bash
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"keyword":"BTB0.408-10PLBDR-G41","currentPage":1,"pageSize":2}' \
  https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList
```

`executed-success`, 2026-09-01. Helper:
[`archive/devices/m5stack/papermono/artifacts/research-scratch/tools/lcsc_lookup.sh`](../../../archive/devices/m5stack/papermono/artifacts/research-scratch/tools/lcsc_lookup.sh).
This belongs in [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Related pages

- [STMicroelectronics ST25R3916](../../stmicroelectronics/st25r3916/README.md) — what sits on the far side
- [XL7EL89CMI-111YLC 27.12 MHz crystal](../xl7el89cmi-111ylc-27.12mhz-crystal/README.md) — on the same sub-board
- [Awinic AW35122FDR](../../awinic/aw35122/README.md) — `U1` sheet 6, the rail this connector's enable line is meant to gate
- [Panasonic AXE512127D](../../panasonic/axe512127d/README.md) — the board's *other* 0.4 mm board-to-board, fully documented
- [XUNPU TYPEC-302-BRP16SC08](../typec-302-brp16sc08/README.md) — same vendor, USB-C
- [PaperMono NFC feature guide](../../../devices/m5stack/papermono/features/nfc.md) · [bill of materials](../../../devices/m5stack/papermono/bill-of-materials.md)

## Authoritative sources

| ID | Title | Publisher | Class | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|
| C1 | JLCPCB/LCSC catalogue entry `C42420580` | LCSC / JLCPCB | distributor | JLCPCB SMT parts API, keyword `BTB0.408-10PLBDR-G41` | 2026-09-01 | — | manufacturer XUNPU, 0.4 mm pitch, 0.8 mm height, 10P/2 rows, 300 mA, 30 V, −35…+85 °C, copper alloy, vertical SMD. **`dataManualUrl` = `None`** | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | both instances, both pinouts, the §3.3 discrepancy, `R2` = `NC` | `../../../devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |

**Local artifacts** — **none.** No manufacturer document exists (§5). This is a
negative result, recorded so it is not re-investigated.
