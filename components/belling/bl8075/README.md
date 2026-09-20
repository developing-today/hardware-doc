# Belling BL8075 (BL8075CB5TR33) — 3.3 V LDO regulator

- **Category:** low-dropout linear regulator, fixed output, with enable.
- **Manufacturer:** **Shanghai Belling Co., Ltd** (上海贝岭) — inferred from the `BL8xxx`
  part-number family. **No datasheet located**; attribution is `inferred`.
- **Research status:** ⚠ **Schematic-only.**
- **Retrieved:** 2026-09-04

The 3.3 V rail of the M5Stack DinMeter carrier board.

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Part string | **`BL8075CB5TR33`** | DinMeter schematic, value text at (606, 308.6), associated with `U4` |
| Suffix reading | `…33` → **3.3 V fixed output**; `B5` → 5-pin package; `TR` → tape-and-reel | conventional Chinese-vendor suffix grammar — `inferred`, not read from a datasheet |
| Pins | **5**: `VIN`, `VOUT`, `GND`, `EN`, `NC` | DinMeter schematic `U4`, `PIU401`–`PIU405` |
| Input on this board | `VBAT_IN` | schematic |
| Output on this board | `+3.3V` | schematic |
| Capacitors | `C30` 22 µF, `C31` 100 nF, `C32` 100 nF, `C33` 22 µF | schematic |

Current rating, dropout, quiescent current, PSRR, `EN` threshold and thermal behaviour are all
**unknown**. No chip-marking confirmation.

## 2. Artifacts

**None.** Establishing evidence:
[`devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf`](../../../devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf).

---

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

`U4`. Produces the carrier's `+3.3V`, which supplies the [BM8563 RTC](../../generic/bm8563/README.md)
(`U5`), the PORT.A I²C pull-ups `R2`/`R3`, the encoder pull-ups `R1`, and the LCD FPC `FPC1`.
Note it is fed from `VBAT_IN`, i.e. the battery/charger node, not from `+5VIN` — which is why
the RTC keeps time while the board is latched off.

→ [`devices/m5stack/dinmeter/pinouts-and-buses.md` §4](../../../devices/m5stack/dinmeter/pinouts-and-buses.md#4-power-tree-and-the-latch)

---

## Datasheet — **not obtained**, 2026-09-11

The record above states *"No datasheet located; attribution is `inferred`."*
**Still true.** What was tried this pass:

| Source tried | Result |
|---|---|
| `http://www.szbelling.com/` | **connection failure (HTTP 000)** — no response |
| GitHub code search, `BL8075` | no datasheet artefacts |
| LCSC JSON API | **403 on every UA** |
| DuckDuckGo HTML | **202 bot-check** |

**The attribution to Belling (上海贝岭 / Shanghai Belling) remains `inferred` from
the part-number family and the conventional suffix grammar.** Nothing in this
pass raised or lowered that confidence.

### What would settle it

1. **Read the top marking off a board photograph.** This is now newly possible:
   the **FCC internal photographs of the X3 and X4 are public and retained** in
   this repository —
   [`devices/xteink/x3/artifacts/certification/2BTR9-XTEINKX3-internal-photos.pdf`](../../../devices/xteink/x3/artifacts/certification/2BTR9-XTEINKX3-internal-photos.pdf)
   (16 images) and
   [`devices/xteink/x4/artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf`](../../../devices/xteink/x4/artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf)
   (15 images). **They have not been read at marking level by this pass.** That
   is the cheapest next step for this record and for every part in
   [`components/unidentified/xteink-x3-x4/`](../../unidentified/xteink-x3-x4/README.md).
2. Chinese search: `BL8075 规格书`, `上海贝岭 BL8075`.
3. LCSC HTML storefront with UA `WhatsApp/2.23.20.0`.

**Do not promote the Belling attribution to a finding until a marking is read.**
A part number differing by one character from a real part on a different board is
a documented trap in this repository's own conventions.
