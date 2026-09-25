# Joulwatt JW5712

> **Ultra-low-quiescent-current synchronous step-down (buck) converter** — 600 mA continuous, 800 mA peak, from a 2.3–5.5 V input, with a typical quiescent current of **360 nA** and eight resistor-free output voltages selected by three `VSEL` strap pins.
> Research snapshot **2026-09-01**. Fitted as **`U10`** on sheet 2 of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), where it produces **`3V3_L2`** — the main system rail that carries the ESP32-S3. **No hardware was available.**

> ⚠ **The publicly served datasheet is a 4-page, image-only scan with no text layer.** Most of the parametric data below therefore comes from Joulwatt's own **product database API**, which is a primary vendor source but not a datasheet. See [§8](#8-datasheet-status--read-this-before-relying-on-a-number-here).

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Joulwatt `JW5712_JW5712A_Datasheet.pdf` — local copy `artifacts/jw5712-jw5712a-datasheet-scanned.pdf`. **Image-only, 4 pages** | `not-tested`; content not machine-readable |
| **[VDB]** | Joulwatt product database, `https://www.joulwatt.com/jwt/web/product/list`, record `id 9661` / `plmProductId 212` | `executed-success` for the retrieval; vendor claim otherwise `not-tested` |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **`JW5712`** (sibling: `JW5712A`) | **[SCH]** sheet 2, `U10`; **[VDB]** |
| Manufacturer | **Joulwatt Technology** (杭州杰华特微电子 / Joulwatt Microelectronics) | **[VDB]** |
| Marketing description | *"Ultra-Low Quiescent Current Synchronous Step-Down Converter"* | **[VDB]** `titleEn` |
| Vendor category | Power management → *"low iq"* (`categoryCode` `PF23101001`) | **[VDB]** |
| Package | **WLCSP-8**, **1.6 mm × 0.9 mm** (parametric table: `WLCSP 1.575 × 0.875 - 8`) | **[VDB]** |
| Product status | **Active** (`productStatus: "Active"`, `validFlag: "Y"`) | **[VDB]** |
| Evaluation board | JW5712 EVM — 2.3–5.5 V in, 1.2 V out @ 0.6 A | **[VDB]** `demoSubtitleEn` |

---

## 2. Key parameters **[VDB]**

Taken from the vendor's own parametric record (`cols` field) and feature list. **These are vendor claims, `not-tested`.**

| Parameter | Value |
|---|---|
| Channels | 1 |
| Input voltage | **2.3 V – 5.5 V** |
| Output current | **600 mA continuous, 800 mA peak** |
| Output voltage range (JW5712) | **1.2 V – 3.3 V**, **8 selectable values** |
| Number of `VSEL` pins | **3** (2³ = 8 codes) |
| Quiescent current | **360 nA typical** |
| Switching frequency | 1200 kHz (parametric field `Data_07`) |
| Control architecture | **COT** (constant on-time) with **PFM** light-load mode |
| Compensation | Internal |
| Efficiency | **up to 90 % with load current > 15 µA** |
| 100 % duty-cycle mode | **Automatic** when V<sub>IN</sub> approaches V<sub>OUT</sub> — the high-side FET is held on and switching stops |
| Output discharge | Yes |
| Protections | output short-circuit, thermal |
| Intended sources | one rechargeable Li-ion cell, Li-primary chemistries (Li-MnO₂), or two to three alkaline cells |

**The 360 nA quiescent current is why this part is on this board.** A rail that stays up through `L2 DeepSleep` costs whatever its regulator burns doing nothing; at 360 nA that is roughly 0.003 mAh per day, i.e. nothing against a 1150 mAh pack. **[INF]**

The "up to 90 % efficiency with load current > 15 µA" claim is the same point from the other side — the PFM/COT architecture keeps efficiency up across four or five decades of load, which a fixed-frequency PWM buck does not.

---

## 3. Pinout as fitted **[SCH sheet 2, `U10`]**

The datasheet's own pin table could not be read (§8), so this table is recovered from the schematic symbol's pin names, which Altium renders as text.

| Ball | Name | Net on PaperMono |
|---|---|---|
| **A1** | `SW` | → **`L2` = `FTC201610S2R2MBCA`, 2.2 µH** → `3V3_L2` |
| **A2** | `VIN` | **`VBUS_L0`** |
| **B1** | `EN` | **`3V3_L2_EN`** — from [M5PM1](../../m5stack/m5pm1/README.md) `U7` pin 14, `DCDC3V3_EN_PP`; `R28` = **1 MΩ/1 %** pull-down |
| **B2** | `GND` | `GND` |
| **C1** | `VSEL1` | GND |
| **C2** | `VOS` | output sense, on `3V3_L2` |
| **D1** | `VSEL2` | GND |
| **D2** | `VSEL3` | GND |

> ⚠ **The `VSEL` strapping is reported as "all three to GND", and the code-to-voltage mapping is unknown.** The three `VSEL` pins each sit adjacent to a `GND` label in the extracted text layer, and the produced rail is unambiguously **3.3 V** (net `3V3_L2`, and the downstream ESP32-S3 requires it). But the datasheet's `VSEL` truth table is in the unreadable scan (§8), so **whether `000` selects 3.3 V or 1.2 V cannot be confirmed from any source retrieved here.** This is recorded as unresolved rather than guessed; if you are copying this design, read the strapping off the rendered sheet and the truth table off a legible datasheet.

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), designator **`U10`**, schematic sheet 2, in the block labelled `L2_SW`.

**`3V3_L2` is the busiest rail on the board.** Sheet 1's power-state table defines it as present in **L2 DeepSleep, L3A CORE ACTIVE and L3B All ACTIVE** — i.e. everything except `L0 Shipping` and `L1 Standby` — and it is enabled by the M5PM1's `DCDC3V3_EN_PP`, exposed to firmware as `pm1.setDcdcEnable(bool)`.

M5Stack's own description of the level: *"L2 / L3A: ESP32-S3, LoRa, NFC/RFID, M5IOE1, user-button pull-up, touch INT, buzzer, RGB red"*, with the distinction that *"When the ESP32-S3 is sleeping, the power system is at level L2. When the ESP32-S3 is operating, it is at level L3A."* L2 and L3A are **states, not separate rails.**

Loads traced to `3V3_L2` from the schematic **[SCH]**:

| Load | Where |
|---|---|
| **ESP32-S3R8** `VDD3P3`, `VDD3P3_CPU`, `VDD3P3_RTC`, `VDDA` | sheet 3, `U12` |
| **M5IOE1** `VCC` | sheet 4, `U17` pin 6 |
| **BMI270** `VDDIO` region / I²C pull-ups `R36`, `R37` (2.2 kΩ) | sheets 3–4 |
| **[AW9967DNR](../../awinic/aw9967/README.md)** frontlight boost `VIN` | sheet 2, `U11` |
| **[AW35122FDR](../../awinic/aw35122/README.md) `U8`** → `TF_3V3_L3B` (microSD) | sheet 2 |
| **[AW35122FDR](../../awinic/aw35122/README.md) `U18`** → `TP_VDD` (touch) | sheet 4 |
| **[AW35122FDR](../../awinic/aw35122/README.md) `U21`** → `PDM_VDD` (microphone) | sheet 4 |
| **Load switch `U1` (sheet 6)** → `VCC_3V3` (NFC sub-board) | sheet 6 |
| **[AW39112DNR](../../awinic/aw39112/README.md) `U19`** `VCCB` (touch bus translator) | sheet 4 |
| KEY1 / KEY2 pull-ups `R2`, `R5` (10 kΩ) | sheet 5 |
| Buzzer drive network | sheet 4 |

Rails that are **not** on `3V3_L2`, which is worth stating because it changes the budget: `3V3_L0`, `3V3_L1`, `3V3_L2_LoRa` and `EPD_3V3_L3B` are each produced by their own [SSP7615-33DFR](../../generic/ssp7615-33dfr/README.md) LDO **directly from `VBUS_L0`**, not from this DC-DC. Sheet 1's block diagram is explicit that the L1/L2/L3 switches all take their input from L0 rather than cascading.

#### 4.1 ⚠ 600 mA is not a generous budget for this rail

**[INF]** — an arithmetic observation, not a measurement:

| Load | Rough worst case at 3.3 V |
|---|---|
| ESP32-S3 Wi-Fi TX peak | ~350 mA |
| microSD write burst | ~100 mA |
| Frontlight boost at full brightness (~11 mA × ~15 V ÷ 3.3 V ÷ 0.85) | ~55 mA |
| NFC sub-board active | tens of mA |
| Touch, microphone, expander, pull-ups | ~10 mA |

Simultaneous worst case plausibly approaches the **600 mA continuous / 800 mA peak** rating. The design is not obviously under-specified — Wi-Fi TX peaks are short and the 800 mA peak rating exists for exactly this — but **a firmware that writes to the SD card during a Wi-Fi transmission with the frontlight at maximum is operating near the converter's limit**, and the symptom of exceeding it would be a `3V3_L2` sag that browns out the ESP32-S3 rather than any error message. Anyone chasing unexplained resets on this board should measure `3V3_L2` under that combination before looking anywhere else.

No hardware measurement was possible; the figures above are typical-part estimates, not this board's measured draw.

#### 4.2 The 100 % duty-cycle mode matters for a Li-ion board

`VBUS_L0` is joined to `VBAT_L0` through a 0 Ω link (`R20`) **[SCH]**, so the buck's input *is* the battery. A single Li-ion cell falls to ~3.3 V well before it is empty, at which point a 3.3 V buck has no headroom. The JW5712's automatic transition to 100 % duty — high-side FET held on, switching stopped — is what keeps `3V3_L2` alive (as `V_BAT` minus the FET drop) down to the pack's cut-off instead of dropping out at 3.4 V. **[VDB]**, **[INF]** for the board-level consequence.

The practical implication: **below roughly 3.4 V pack voltage, `3V3_L2` is no longer regulated 3.3 V** — it tracks the battery. Anything on that rail that cares about supply accuracy (the ADC references in the ESP32-S3, for instance) sees a moving target near end of charge.

---

### `devices/m5stack/cap-lora-1262` · *added 2026-09-04*

→ [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md), designator **`U3`**, single-sheet schematic V1.1 (2025-10-29).

5 V (from the Cardputer-Adv's EXT connector) → **3.3 V**, with the annotation **`IOUT: 0~0.6A`** printed beside the symbol. Inductor `L2` = `WPN201610U2R2MT` (2.2 µH). Input `C1` 1 nF + `C2`/`C3`/`C4` 22 µF; output `C15` 22 µF, `C12` 470 µF, `C16`/`C17` 100 nF.

Package pin names as drawn — **a chip-scale/BGA-style map, not the PaperMono's**: `SW` A1, `VIN` A2, `ENB` B1, `GND` B2, `VSEL1` C1, `VOS` C2, `VSEL2` D1, `VSEL3` D2. Three `VSEL` straps are brought out, which is how the output voltage is selected.

**`ENB` has no host connection.** `R1` = **10 kΩ** sits between the `+5V`/`+5VOUT` labels and the enable pin, so the rail comes up with the host's 5 V and stays up. ⚠ The net was **not traced end-to-end** from the PDF text layer — "always on" is `inferred` from that adjacency plus the absence of any enable signal on the 14-pin Cap-Bus.

Loads: the `Stamp LoRa-1262 Mini` module, the `ATGM336H-6N` GNSS (digital `VCC` and `VCC_RF` through separate 120 Ω/MB ferrites), the always-on `MAX2659` GNSS LNA, and the `PI4IOE5V6408` expander.

### `devices/m5stack/cap-cc1101` · *added 2026-09-04*

→ [M5Stack Cap CC1101 & NFC (U219)](../../../devices/m5stack/cap-cc1101/README.md), designator **`U1`**, sheet 1 of schematic V0.3 (2026-05-28).

Same part, same `IOUT: 0~0.6A` annotation, inductor `L1` = `MWTC201608S2R2` (2.2 µH), input `C1` 1 nF + `C2`/`C3`/`C4` 22 µF, output `C5` 22 µF + `C6` 100 nF.

**The difference that matters: here `ENB` *is* host-controlled.** Board net **`POWER_EN`** arrives on **Cap-Bus pin 8** from host **G3** and drives the enable, with `R1` = **100 kΩ** in the network. That is how the board reaches its published **140.87 µA @ 5 V** sleep figure — the host can switch the entire Cap off, rather than relying on the CC1101 and ST25R3916 low-power modes.

⚠ `R1`'s polarity was **not traced**, so whether the Cap defaults on (pull-up) or off (pull-down) is unestablished. The signal is *named* `POWER_EN`, which conventionally implies active-high; bring-up code should drive G3 **high and wait** rather than assume.

> **Design note worth carrying:** the *same* regulator, on two boards from the same vendor, in the same product family, on the same connector — with **Cap-Bus pin 8 meaning `LoRa_RST` on one and `POWER_EN` on the other**. Any firmware that auto-detects which Cap is fitted must not assume pin-8 semantics.

### M5Stack Stamp-S3A (`S007-V033`) — and every board carrying it

Designator **U4** on `Sch_StampS3_v0.3.3.pdf`, producing **`VDD_3V3`** from `VIN_5V`.
Sheet annotation: **`IOUT: 0~0.6A`**. Output selected by the **`VSEL1`/`VSEL2`/`VSEL3`** straps
(all three tied to `VIN_5V` through the C1/D1/D2 net) — **no feedback divider**, and `VOS` is a
remote-sense pin, not a divider tap. External inductor **`L4` = `MWTC201608S2R2`** (2.2 µH,
2016-metric) on `SW`; `EN` from an R16 100 kΩ network; support caps C15 1 nF, C16 10 µF,
C18 100 nF, C21/C22/C25 10 µF.

Replaces the **Murata [`MUN3CAD01-SC`](../../murata/mun3cad01-sc/README.md)** µPOL module used on
the StampS3 v0.2, which set its output with an R16 100 k / R17 22.1 k divider that the JW5712
design deletes.

Boards: [Cardputer v1.1](../../../devices/m5stack/cardputer-v1.1/README.md),
[Cardputer ADV](../../../devices/m5stack/cardputer-adv/README.md),
[Cardputer Mesh Kit](../../../devices/m5stack/cardputer-mesh-kit/README.md).

> **Provenance note.** `components/unidentified/m5stack-stamp-s3a/dcdc-u4/` was created on
> 2026-09-04 recording this same `U4` as "part number not established". The label **is** present
> on the sheet — see §0 of `archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md` for the verifying crop
> and hashes. That directory should be retired in favour of this record.
>
> ⚠ **Retiring it would edit another session's record, so it has not been done.** The conflict is
> parked for review in
> [`research/passes/index-merge/corrections-requiring-review.md`](../../../research/passes/index-merge/corrections-requiring-review.md).

*Added 2026-09-07 from `archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md` §3.5.*

## 5. Drivers and libraries

**Not applicable at the component level** — no bus interface. On the PaperMono the only control is the enable line, owned by the M5PM1:

```cpp
pm1.setDcdcEnable(true);    // 3V3_L2_EN -> JW5712 EN  (this rail)
pm1.setLdoEnable(true);     // 3V3_L1_EN -> the SSP7615 LDO feeding the IMU
```

> ⚠ **Calling `pm1.setDcdcEnable(false)` powers off the ESP32-S3 that is making the call.** It is a one-way trip; recovery is a power-button press or an M5PM1 wake source. **[INF]**

---

## 6. Integration pitfalls

1. **`VSEL` strapping is silent.** Three pins, eight voltages, no readback, no error. Mis-strapping produces a wrong but perfectly stable rail. Verify against a legible truth table (§3, §8).
2. **`EN` needs its pull-down.** `R28` = 1 MΩ on this board. Without it the rail state at power-up is whatever the enable driver's high-Z leakage decides.
3. **Below ~3.4 V input the output stops regulating** (§4.2). This is a feature, but it changes the rail's specification at end of discharge.
4. **Peak versus continuous** — 800 mA peak is not a duty-cycle-free rating (§4.1).
5. **Output discharge is active.** Disabling the rail actively pulls it down; do not rely on a slow decay for orderly shutdown of downstream logic.

---

## 7. Alternatives

| Part | vs. JW5712 | When |
|---|---|---|
| **JW5712A** | Same family, same package and description; the vendor lists them as one datasheet | Second option within the family; the difference was not established (§9) |
| TI **TPS62840** | 750 mA buck, **60 nA** I<sub>Q</sub>, very well documented | When quiescent current is the whole design and you want a legible datasheet |
| TI **TPS62203** / **TLV62569** | Higher current, ordinary I<sub>Q</sub> | When the rail never sleeps |
| **[SGM6029](../../sgmicro/sgm6029/README.md)** | Buck-boost, 3.3 V / 600 mA | When you need to hold 3.3 V *below* 3.3 V input rather than dropping into 100 % duty. Documented in this repository |
| **[SSP7615-33DFR](../../generic/ssp7615-33dfr/README.md)** LDO | 400 mA, 0.5 µA I<sub>Q</sub>, no inductor | Lower-current rails — which is exactly how the PaperMono uses it for `3V3_L0`, `3V3_L1`, `3V3_L2_LoRa` and `EPD_3V3_L3B` |

The interesting comparison is the last one: this board fits **one** buck and **four** LDOs. The buck goes where the current is (the ESP32-S3), and the LDOs go where the current is small and the noise matters or the cost of an inductor is not worth it. **[INF]**

---

## 8. Datasheet status — read this before relying on a number here

**A datasheet was obtained, and it is largely unusable.**

| Property | Value |
|---|---|
| URL | `https://www.joulwatt.com/jwt/profile/ProductFile/规格书/JW5712_JW5712A_Datasheet.pdf` |
| HTTP | 200, `application/pdf`, `%PDF` verified |
| Size | 2 547 415 B |
| SHA-256 | `077d56d71d5b5c921499f26b4254ec4cc5a3c4b5809ca8ef2ca2dc5b81d9dba2` |
| **Pages** | **4** |
| **Text layer** | **None.** `pdftotext` returns zero characters |
| Content | 4 × full-page RGB images, 2479 × 3507 px at 300 dpi — a scan or a rasterised export |

A separate `..._FirstPage.pdf` (1 page, 2 546 640 B) is also served and is the same material.

**Consequences, stated plainly:**

- The `VSEL` truth table, the full pin description, the absolute maximum ratings and the electrical characteristics table are **not available in machine-readable form** and were **not** transcribed here, because doing so from an unreadable scan would be guessing.
- Everything in §2 comes from **[VDB]**, Joulwatt's product-database API. That is a primary vendor source and it is internally detailed (it carries the parametric `cols` record, the bilingual feature list and the EVM description), but **it is not a datasheet** and carries no absolute maximum ratings.
- A four-page datasheet is in any case an abridgement. Joulwatt may publish a full version to registered customers; that was not pursued.

**How the file was found**, recorded because the path is not discoverable from the site UI:

1. `https://www.joulwatt.com/assets/js/request.js` reveals the API base `https://www.joulwatt.com/jwt/web/`.
2. `POST`/`GET` `https://www.joulwatt.com/jwt/web/product/list?pageSize=3000` returns all 1 564 products as JSON, including `datesheetFileSite` per part.
3. That relative path resolves under `https://www.joulwatt.com/jwt/profile/`.

`http://www.joulwatt.com/` timed out on first contact; `https://` worked. Plain `curl` with a Chrome 131 User-Agent throughout; no fallback User-Agent required, no login.

---

## 9. Open questions

- **The `VSEL` truth table.** Which of the eight codes produces 3.3 V, and therefore whether the PaperMono's strapping is what it appears to be (§3).
- **Absolute maximum ratings** — not available from any source retrieved (§8).
- **What distinguishes JW5712 from JW5712A.** The vendor gives both the same description, package and feature list; the parametric records differ only in the part name field. **[VDB]**
- Whether a full-length JW5712 datasheet exists publicly.
- No hardware measurement of `3V3_L2` under load, and no verification of the §4.1 budget concern.

---

## Manufacturer

**Joulwatt Technology** (杰华特微电子). No vendor sourcing guide exists in this repository yet. The retrieval recipe in §8 is the reusable part; the two facts worth carrying forward to any future Joulwatt part are:

- **The product database is public and complete** — `GET https://www.joulwatt.com/jwt/web/product/list?pageSize=3000` returns every product with descriptions, features, parametric data and datasheet paths, in one 4.4 MB JSON response.
- **Datasheet files live under `/jwt/profile/` + the `datesheetFileSite` value**, and the path contains Chinese characters (`规格书`) that must be percent-encoded.

## Related pages

- [M5Stack M5PM1](../../m5stack/m5pm1/README.md) — owns `3V3_L2_EN`
- [SSP7615-33DFR](../../generic/ssp7615-33dfr/README.md) — the LDOs producing the other four rails
- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the dominant load on this rail
- [Awinic AW9967DNR](../../awinic/aw9967/README.md) — frontlight boost, powered from this rail
- [Awinic AW35122](../../awinic/aw35122/README.md) — the three load switches downstream of this rail

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | JW5712 / JW5712A datasheet | Joulwatt | primary | datasheet | <https://www.joulwatt.com/jwt/profile/ProductFile/%E8%A7%84%E6%A0%BC%E4%B9%A6/JW5712_JW5712A_Datasheet.pdf> | 2026-09-01 | undated; 4 pp, **image-only**, 2 547 415 B | Existence and identity only — no machine-readable content (§8) | `artifacts/jw5712-jw5712a-datasheet-scanned.pdf` |
| D2 | Joulwatt product database, record `id 9661` | Joulwatt | primary | API | <https://www.joulwatt.com/jwt/web/product/list> | 2026-09-01 | live | Every parameter in §2: input range, 600/800 mA, 360 nA I<sub>Q</sub>, 8 output voltages via 3 `VSEL` pins, WLCSP-8 1.6 × 0.9 mm, COT/PFM, 100 % duty behaviour, Active status | not vendored (4.4 MB full listing) |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `U10` ball/net table, `L2` = 2.2 µH, `R28` = 1 MΩ, `3V3_L2_EN` ← M5PM1 pin 14, every load in §4 | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | PaperMono M5PM1/M5IOE1 power-management page | M5Stack | primary | official page | <https://docs.m5stack.com/en/arduino/papermono/m5pm1_m5ioe1> | 2026-09-01 | — | The L0–L3B level definitions and `setDcdcEnable()` | `archive/devices/m5stack/papermono/artifacts/research-scratch/docs/pages/en-arduino-papermono-m5pm1_m5ioe1.html` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages | Text layer |
|---|---:|---|---:|---|
| `artifacts/jw5712-jw5712a-datasheet-scanned.pdf` | 2 547 415 | `077d56d71d5b5c921499f26b4254ec4cc5a3c4b5809ca8ef2ca2dc5b81d9dba2` | 4 | **none** |

**Method note.** D1 was validated as `%PDF` and confirmed image-only with `pdfimages -list` (4 × 2479 × 3507 RGB, 300 dpi). It is retained despite being unreadable because it is the vendor's own file and a future reader with OCR can extract what this pass could not — and because recording *that it is a scan* is itself the finding that stops the next agent repeating the search.
