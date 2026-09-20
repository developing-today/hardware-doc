# DinMeter v1.1 — gaps and conflicts

v1.1-specific items. Everything that applies to both revisions — the Grove wire-colour conflict,
the three unmarked designators, the Grove 5 V rail arithmetic, the untraced GPIO14/39 network,
and the full negative-result table — is in
**[`../dinmeter/gaps-and-conflicts.md`](../dinmeter/gaps-and-conflicts.md)**.

---

## V1 · ⚠ The RGB LED almost certainly does not work with stock M5Unified — **predicted, unverified**

**The most consequential open question in this record.**

| Evidence | Says |
|---|---|
| M5Stack, DinMeter v1.1 page | *"Stamp-S3A adds an independent electronic switch for the RGB LED power supply… Before controlling the RGB LED in software, set **GPIO38**, which controls this switch, to a high level."* |
| M5Stack, Stamp-S3A page comparison table | S3A: *"RGB LED power is multiplexed with the reserved screen FPC bus backlight"*; S3: *"Powered as soon as power is applied"* |
| `Sch_StampS3_v0.3.3.pdf` | `U3` (WS2812B-2020) `VDD` ← **`BL_3V3`**, the output of `U2` (AW35122FDR), whose `EN` is `DISP_BL` = GPIO38 |
| `Sch_M5StampS3_v0.2.pdf` | `U3` `VDD` ← `VDD_3V3` — always on |
| AW35122 datasheet | `EN` has an internal ~7.1 MΩ **pull-down** ⇒ the rail defaults **off** |
| M5Unified master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb` (2026-09-04) | `_pin_table_other0` → `{ board_M5DinMeter, GPIO_NUM_21 }` (`src/M5Unified.cpp:246`); **no `board_M5StampS3A`, no v1.1 board enum, and no GPIO38 enable step for any board** |

**Conclusion:** a v1.1 unit enumerates as `board_M5DinMeter`, takes the v1.0 LED path, and the
rail is never enabled — so the LED stays dark.

**Status: `inferred`. NOT reproduced on hardware.** No v1.1 unit was available.

**Why it matters more than it looks:** the failure is *silent*. Code compiles, links, boots and
runs; the LED simply does nothing. The natural diagnosis is "faulty LED" or "broken library",
neither of which is true.

**What would settle it:** two lines on a real v1.1 unit —
```cpp
pinMode(38, OUTPUT); digitalWrite(38, HIGH); delay(1);   // then drive GPIO21
```
Result belongs in [`compatibility-and-status.md`](compatibility-and-status.md).

---

## V2 · ⚠ No v1.1 schematic, STL or footprint exists — **established**

| Asset | v1.1 URL / path | Same bytes as v1.0? |
|---|---|---|
| Schematic | `…/1211/K134-V11_DIN_Meter_**v1.0**_2025_11_25_17_15_58.pdf` | **yes** — SHA-256 `03ec3353…6e4c070` |
| Structure STL | `Products/K134-V11_DinMeter_v1.1/Structures/DinMeter_v1.1.stl` | **yes** — SHA-256 `90f04d6a…` |
| Dimension drawing | *the same URL as v1.0* | yes |

Even the v1.1 schematic's own filename says `v1.0`.

**What this licenses:** M5Stack has published no v1.1-specific board documentation. **It does not
prove the PCB is unchanged.** The two boards could differ in ways no published document shows —
different passives, a different encoder supplier, a different panel vendor.

**Corroborating (but not proving) that it really is unchanged:** the PinMap is identical
signal-for-signal; M5Unified has one board enum; the factory firmware has not been touched since
2024-03-04, 22 months before the v1.1 shipped; and the same pattern holds one level down, where
`Stamp-S3A.stl` is byte-identical to `Stamp-S3.stl` and **no Stamp-S3A footprint exists at all**.

**What would settle it:** a v1.1 schematic from M5Stack, or a teardown photograph of a v1.1 PCB
next to a v1.0 one.

---

## V3 · ⚠ ST7789P3 — named three times, documented nowhere

The v1.1 page names `ST7789P3` in the Features list, the *Display Driver* specification row and
the PinMap section heading. It then **removes** the display datasheet link that the v1.0 page
carried (`ST7789V2_SPEC_V1.0.pdf`) and replaces it with **nothing** — the v1.1 *Datasheets*
section lists BM8563, tp4057, the DC connector and the battery seat, and no display part.

And M5Stack's own v1.0↔v1.1 "Product Comparison" table has **one row** — *Main Controller* — and
does not mention the display at all.

No ST7789P3 datasheet was located from Sitronix or any mirror.

**Working assumption:** command-compatible with ST7789V2. Supported by identical pins, identical
resolution, an unchanged driver path, M5Unified having no ST7789P3 branch, and M5Stack's own
factory firmware using the *generic* `lgfx::Panel_ST7789` class rather than a V2-specific one.
**That is absence of contrary evidence, not verification.** `inferred`.

→ [`components/sitronix/st7789p3`](../../../components/sitronix/st7789p3/README.md)

---

## V4 · ⚠ The Stamp-S3A page's DC-DC row is stale

It lists `DC-DC: MUN3CAD01-SC` and links that datasheet from the **`S007 StampS3`** directory —
the Stamp-S3's own path.

The string `MUN3CAD01` **does not occur anywhere** in `Sch_StampS3_v0.3.3.pdf`. Designator `M2`
is absent. The regulator there is `U4`: an 8-ball part with `VIN`/`EN`/`SW`/`VOS`/`VSEL1`/
`VSEL2`/`VSEL3`/`GND`, annotated **`IOUT: 0~0.6A`**, driving an external 2.2 µH inductor (`L4`,
`MWTC201608S2R2`). A µPOL module has an integrated inductor and an `FB` pin, not `SW` and `VSEL`
straps, and is rated 1 A.

**Resolution: the schematic wins; the spec row was carried over unedited.** `U4`'s part number is
left **unidentified** rather than guessed —
[`components/unidentified/m5stack-stamp-s3a/dcdc-u4`](../../../components/unidentified/m5stack-stamp-s3a/dcdc-u4/README.md).

**Undisclosed consequence:** the new regulator is **0.6 A** where the old one was **1 A**. M5Stack
mentions this nowhere. It is unlikely to matter on a DinMeter (the carrier makes its own 3.3 V)
but it matters for anyone designing with a bare Stamp-S3A.

---

## V5 · ⚠ Stamp-S3A: 24 mm or 26 mm

Vendor tables: Stamp-S3 = 24.0 × 18.0 × 4.7 mm; Stamp-S3A = **26.0** × 18.0 × 4.7 mm. But the two
published STLs are byte-identical, `m5stack/M5_Hardware` publishes **no Stamp-S3A footprint**, and
M5Stack ships the S3A on a DinMeter carrier whose published assets are unchanged.

A 2 mm growth would break every host PCB. `inferred`: the 26.0 is probably a documentation error.
**Not established.** Measure a real part before laying out a board.

---

## V6 · ⚠ The rear FPC connectors are numbered in opposite directions

`J1` (12 P) and `J3` (8 P) on the Stamp carry the same nets in the same physical order on both
revisions, but their pin **numbers** run opposite ways — `J1` pin 1 = `VIN_5V` on v0.2, pin **12**
on v0.3.3.

**Unresolved:** either the connector was physically re-oriented (an existing display flex would
mate backwards) or the symbol was renumbered with the footprint mirrored (nothing changed).
Evidence leans to the latter — same connector part number, no new footprint, identical STLs — but
that is inference.

**Does not affect the DinMeter**, which does not use the Stamp's rear header. Does affect anyone
attaching a flex to a bare Stamp-S3A: check
[`S007-V033_PinMap_01.jpg`](../../../components/m5stack/stamp-s3a/artifacts/S007-V033_PinMap_01.jpg)
first. **That image was not OCR'd in this pass** — reading it would settle this.

---

## V7 · The antenna claim is unquantified

M5Stack: *"Optimized antenna design with better signal reception"* vs *"Conventional antenna
design"*. **No dBi, no RSSI comparison, no method, no test conditions.**

The schematics do show a real change — the match went from 3 elements
(`L1` 2.2 nH, `C1` 2.2 pF, `C2` 2.0 pF) to 6 positions plus a filter on `CHIP_PU`, and
`PROANT440` no longer appears as the `ANT1` value. So *something* was done. Whether it helps, and
by how much, is **unmeasured**.

This matters more than usual here, because the DinMeter is designed to be installed **behind a
panel**, often in a metal cabinet — the worst RF case. **What would settle it:** RSSI at a fixed
distance, v1.0 vs v1.1, same firmware, same AP.

---

## V8 · Nothing about v1.1 has been tested on hardware

No v1.1 unit was available. Every v1.1-specific claim in this record is derived from vendor
documentation, published schematics and source code. See
[`compatibility-and-status.md`](compatibility-and-status.md) §5.

## Related

[`../dinmeter/gaps-and-conflicts.md`](../dinmeter/gaps-and-conflicts.md) (items shared by both
revisions) · [`stamp-s3-to-s3a-delta.md`](stamp-s3-to-s3a-delta.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md)
