# Semtech SX1276/77/78/79 (SX127x) — the first-generation LoRa transceiver

> **Lineage:** [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md)
> — the four generations side by side. **Domain:** [`guides/lora`](../../../guides/lora/README.md).

- **Category:** sub-GHz **LoRa / FSK / GFSK / MSK / GMSK / OOK** transceiver, **register-mapped SPI**
- **Bands:** **137–1020 MHz** (SX1276/77/78/79); the SX1272/73 sibling covers **860–1020 MHz**
- **Package:** **QFN 28** · Order code `SX1276IMLTRT`, Pb-free/halogen-free/RoHS **[PP]**
- **Generation:** **1.** `DS.LR20xx` §23.8: *"Generation 1 (Gen 1): **SX1272, SX1276** - First LoRa chips (**2013**)"* **[DS20]**
- **Silicon revision:** **V1b**, `RegVersion` (`0x42`) = `0x12`. ⚠ V1a exists and is engineering-sample only **[ER76]**
- **Research depth:** **light record with real artifacts.** The **Rev 5 datasheet (August 2016, 132 pp) and both errata notes are retained.** The current revision is **Rev 7** and was **not** obtained (G1).
- **Retrieved:** 2026-09-04

**Why this record exists.** No board in this knowledge base uses an SX127x. It is here so the
generation lineage is navigable, and because **the SX127x → SX126x break is the canonical
"everything changed" migration** that the LR2021 record's §3 is measured against.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DS76]** | `artifacts/sx1276-77-78-79-datasheet-v5-wayback.pdf` — **Rev. 5, August 2016**, 132 pp |
| **[ER76]** | `artifacts/sx1276-77-78-errata-wayback.pdf` — SX1276/77/78 Errata Note, **Revision 1, Sept 2013** |
| **[ER72]** | `artifacts/sx1272-73-errata-wayback.pdf` — SX1272/73 Errata Note |
| **[PP]** | Semtech product pages (`…/lora-connect/sx1276`, `…/sx1272`), retrieved 2026-09-04 |
| **[DS20]** | `DS.LR20xx` Rev 2.1 — cited for cross-generation statements only. [Held here](../lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf) |
| **[RL]** | RadioLib source, read live |
| **[INF]** | Inference |

---

## 1. Two sub-families, and they are not the same silicon

The most common SX127x error is treating "SX127x" as one part. **[PP]**:

| | **SX1272 / SX1273** | **SX1276 / 77 / 78 / 79** |
|---|---|---|
| Frequency | **860–1020 MHz** | **137–1020 MHz** |
| Max link budget | **157 dB** | **168 dB** |
| Best sensitivity | **−137 dBm** | **−148 dBm** |
| IIP3 | −12.5 dBm | −11 dBm |
| Blocking immunity | 89 dB | "excellent" (not quoted numerically) |
| RX current | **10 mA** | **9.9 mA** |
| Register retention | **100 nA** | **200 nA** |
| Order codes | `SX1272IMLTRT`, `SX1273IMLTRT` | `SX1276IMLTRT` (+77/78/79) |
| Errata | **[ER72]** | **[ER76]** |
| Package | QFN 28 | QFN 28 |

Shared by both: +20 dBm PA (100 mW, constant vs supply) and a +14 dBm high-efficiency PA;
programmable bit rate to 300 kbps; **FSK, GFSK, MSK, GMSK, LoRa and OOK**; built-in bit synchroniser;
preamble detection; 127 dB dynamic-range RSSI; automatic RF sense and CAD with ultra-fast AFC;
**packet engine up to 256 bytes with CRC**; 61 Hz synthesiser resolution; built-in temperature sensor
and low-battery detector. **[PP]**

⚠ **Within the SX1276/77/78/79 group the differences are bandwidth and band, not architecture** —
`RFM95`/`RFM96`/`RFM98` modules are built on them and the module suffix does not always match the
die. **This record does not resolve which module carries which die**; that is a per-module question.

---

## 2. ⭐ The register model — what SX126x threw away

This is the section worth reading even if you never touch a Gen-1 part, because it is the *before*
picture for [`lora-radio-generations` §3.1](../../../guides/hardware/lora-radio-generations.md).

**[DS76]** §4.3, verbatim in substance:

- SPI, **CPOL = 0, CPHA = 0**, slave only, max 10 MHz.
- **The first byte is an address byte**: **1 `wnr` bit (1 = write, 0 = read) + 7 address bits, MSB
  first.** So the whole device is **128 registers**, and that is the entire interface.
- Three access modes:
  - **SINGLE** — address byte, then one data byte.
  - **BURST** — address byte then many data bytes; **the address auto-increments internally**.
  - **FIFO** — if the address byte is the FIFO's address, the address is **memorised and does not
    increment**, so succeeding bytes stream into/out of the FIFO.
- ⚠ **On a write, MISO returns the register's value *before* the write.** A free read-back that
  almost nobody uses, and a genuine trap if you assume MISO is idle during writes.
- **There is no `BUSY` pin.** Timing is the driver's problem.
- **Mode is a register**, not a command: `RegOpMode` (`0x01`) holds the operating mode **and the
  LoRa/FSK selection bit**, and *"it is possible to access any mode from any other mode by changing
  the value in the `RegOpMode` register."*
- ⚠ **There are two register maps, and they overlap.** **[DS76]** §6.2 is the FSK/OOK map and §6.4
  is the LoRa map; the same address means different things depending on the `RegOpMode` modem bit.
  Address `0x28` is `RegSyncValue1` in FSK and `RegFeiMsb` in LoRa. **This is the single nastiest
  property of the Gen-1 interface** and it is why a half-initialised driver produces plausible
  nonsense rather than an error.
- **Interrupts** are mapped to **DIO0–DIO5** through `RegDioMapping1`/`RegDioMapping2` — host-side
  configuration of which event lands on which pin.

**Every one of those properties is gone in Gen 2.** No address byte, no `wnr` bit, no auto-increment
semantics, no dual register map, no `RegOpMode`; instead an 8-bit opcode, a mandatory `BUSY`
handshake, and `SetStandby`/`SetRx`/`SetTx` commands. That is why nothing ports, and why RadioLib
keeps `SX127x` and `SX126x` as unrelated modules **[RL]**.

---

## 3. Analog and power

**[DS76]** §5:

- Internal voltage regulation across the full industrial range. **+17 dBm is maintained from 1.8 V
  to 3.7 V; +20 dBm requires 2.4 V to 3.7 V.** ⚠ A real constraint on a single-cell Li-ion design as
  it discharges.
- Supplies split three ways — `VBAT_ANA`, `VBAT_RF`, `VBAT_DIG` — with decoupling on `VR_PA`,
  `VR_DIG`, `VR_ANA`. **No DC-DC anywhere.** Gen 2 adds one for the core; Gen 4 adds a SIMO that
  feeds the PA too ([lineage §5.2](../../../guides/hardware/lora-radio-generations.md)).
- Crystal on `XTA`/`XTB`, Pierce oscillator, automatic PLL trigger when stable. **A TCXO is
  supported via the `TcxoInputOn` bit** — note this is a *bit*, not a pin function, and the TCXO is
  powered by the host. Compare Gen 2's `SetDio3AsTcxoCtrl` (steals a DIO) and Gen 4's dedicated
  `VTCXO` pin.
- Over-current protection, low-battery detector (`RegLowBat`, mappable to any DIO), temperature
  measurement.

---

## 4. Errata — and a live interoperability trap

### 4.1 SX1276/77/78 Errata Note, Revision 1, Sept 2013 **[ER76]**

⚠ **Applies to silicon V1b only** — `RegVersion` at `0x42` returns `0x12`. Semtech states plainly:
*"The devices of previous silicon revision V1a are engineering samples which do not offer full
functionality. They should not be used in a production device."* **Read `0x42` before trusting
anything.**

| § | Issue |
|---|---|
| 2.1 | **Sensitivity optimisation with a 500 kHz bandwidth** |
| 2.2 | **Frequency offset tolerance with 500 kHz bandwidth** |
| 2.3 | **Receiver spurious reception of a LoRa signal** |
| 2.4 | **Valid packet counter offset** |
| 3.1 | `PayloadReady` set for 31.25 ns if the FIFO is empty (FSK) |
| 3.2 | **Erroneous IBM data whitening/de-whitening** (FSK) |

⚠ **§3.2 is the one that bites cross-vendor**: a whitening implementation that follows the IBM
convention will not interoperate with an SX1276 that has this defect. If you are debugging an FSK
link between an SX127x and anything else and the payload arrives as plausible garbage, start here.

### 4.2 The SF6 trap, still live in 2026

`DS.LR20xx` §23.8 lists *"SF6 requires additional configuration for backwards compatibility"* across
**all four generations**, and Semtech's Gen-4 driver ships
`lr20xx_workarounds_lora_enable_sx1276_compatibility_mode` and
`lr20xx_workarounds_lora_freq_hop_enable_sx1276_compatibility_mode` **[DS20]**. **Thirteen years
later, "SX1276 compatibility mode" is still a named function in current silicon's driver.** That is
the measure of how much Gen-1 hardware is still deployed.

**Intra-packet frequency hopping** is the other Gen-1 survival: present in Gen 1, absent in Gens 2
and 3, **back in Gen 4** with an explicit SX1276-compatibility mode **[DS20]** §9.8, §23.8.

### 4.3 SF5 does not exist on Gen 1

**[DS20]** §23.8: *"SF5 is available starting from generation 2."* An SF5 network silently excludes
every SX127x node.

---

## 5. Software support

| Stack | Status |
|---|---|
| **RadioLib** | ✅ `src/modules/SX127x` — a **separate module** from `SX126x`, with no shared base class **[RL]** |
| **Semtech** | No standalone `sx127x_driver` repository exists on `LoRa-Net`; Gen-1 support lives inside `LoRaMac-node` (⚠ last push **2024-07-03**) |
| **Meshtastic** | ✅ as **`RF95_RADIO`** in `LoRaRadioType` — named for the RFM95 module rather than the die |
| **Arduino `LoRa`** (sandeepmistry) | The classic hobby library; SX127x-only. Not evaluated this pass |
| Linux kernel | ❌ none |

⚠ **Meshtastic calls it `RF95_RADIO`, not `SX1276_RADIO`.** If you are grepping a codebase for
Gen-1 support, search both.

---

## 6. Caveats and gaps

| # | Issue |
|---|---|
| **G1** | ⚠ **The retained datasheet is Rev 5 (August 2016); the current revision is Rev 7.** The Rev 7 filename `DS_SX1276-7-8-9_W_APP_V7.pdf` appears in countless citations but `www.semtech.com/uploads/documents/` now **soft-404s** — HTTP 200 with 21 149 B of HTML for every path ([vendor guide §2.3](../../../vendors/semtech/README.md)). Rev 7 was **not obtained**. Differences between Rev 5 and Rev 7 are **`unresolved`** |
| **G2** | ⚠ **The retained errata is Revision 1 (Sept 2013).** A later revision very likely exists. `unresolved` |
| **G3** | ⚠ **Two register maps share one address space**, selected by a bit in `RegOpMode` (§2). Half-initialised drivers produce plausible nonsense |
| **G4** | ⚠ **Errata applies to silicon V1b only.** Read `RegVersion` (`0x42`) = `0x12` before trusting it. V1a parts are engineering samples |
| **G5** | ⚠ **+20 dBm needs ≥ 2.4 V**; only +17 dBm is guaranteed down to 1.8 V. Bites late in a single-cell discharge curve |
| **G6** | **SX1272/73 ≠ SX1276/77/78/79** (§1). Different bands, 11 dB different sensitivity, different errata |
| **G7** | **Module-to-die mapping unresolved.** `RFM95`/`RFM96`/`RFM98` are third-party modules; which die each carries is not established here |
| **G8** | **Nothing measured**; no hardware in this knowledge base |
| **G9** | **Lifecycle:** still listed, still orderable, still sold in enormous module volume. **No EOL notice was found** — but PCN/EOL enumeration was not performed |

---

## 7. Used By

**No board in this knowledge base uses an SX127x.** Every LoRa-bearing device documented here
carries a Gen-2 [SX1262](../sx1262/README.md). This record exists for the lineage.

Where you *will* meet it: `RFM95W`-class modules, the enormous installed base of first-generation
LoRaWAN nodes and Meshtastic `RF95` boards, and any TTN deployment older than about 2019.

---

## 8. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/sx1276-77-78-79-datasheet-v5-wayback.pdf` | 2 152 983 | `ec4e2fb67736b5d706e60ffb84fc0a22ca25a4eed33c58aa62e52580a59f7b2b` | **SX1276/77/78/79 Datasheet, Rev. 5, August 2016**, 132 pp |
| `artifacts/sx1276-77-78-errata-wayback.pdf` | 173 175 | `d31cd91430b1ba04cc237e38895fd210a3a33aaa15a30077eb10d7cf79e0c010` | **SX1276/77/78 Errata Note, Revision 1, Sept 2013** |
| `artifacts/sx1272-73-errata-wayback.pdf` | 140 550 | `a15152c7fdeb31fbebdfeb027157ed54b9badaf26a5adbc0532e67e0f2866242` | **SX1272/73 Errata Note** — kept because §1 shows the two sub-families are different silicon |

**Provenance, all three.** All were recovered from the **Internet Archive**, because both of
Semtech's own historical document stores are now unusable
([vendor guide §5.2](../../../vendors/semtech/README.md)).

| Field | Datasheet | Errata (76) | Errata (72) |
|---|---|---|---|
| Original URL | `www.semtech.com/uploads/documents/DS_SX1276-7-8-9_W_APP_V5.pdf` | `www.semtech.com/images/datasheet/sx1276_77_78-errata.pdf` | `www.semtech.com/images/datasheet/sx1272_73_errata.pdf` |
| Wayback timestamp | **20180903190247** | **20150902061654** | **20150412001918** |
| Recovery URL | `https://web.archive.org/web/20180903190247if_/https://www.semtech.com/uploads/documents/DS_SX1276-7-8-9_W_APP_V5.pdf` | `https://web.archive.org/web/20150902061654if_/http://www.semtech.com/images/datasheet/sx1276_77_78-errata.pdf` | `https://web.archive.org/web/20150412001918if_/http://www.semtech.com/images/datasheet/sx1272_73_errata.pdf` |
| Second source | Semtech LR2021-era catalogue lists `SX1276-7-8 Errata Note` and `SX1272 Errata Note` — but behind the `blocked` Salesforce shell, so **it is a locator, not a download** | idem | idem |
| ⚠ Note | The Wayback CDX also indexes `DS_SX1276-7-8-9_W_APP_V7.pdf`-era captures under a **different** path; **Rev 7 was not obtained** (G1) | — | — |
| Retrieval date | 2026-09-04 | 2026-09-04 | 2026-09-04 |
| Type validated | `%PDF`, 132 pages parsed by `pypdf` | `%PDF`; `/Title` `SX1276_77_8_ErrataNote_1.1_STD`, `/Author` `slebreton`, created 2013-09-23, `/Producer` GPL Ghostscript 9.05 | `%PDF` |
| Licence | **`unknown`** — © Semtech Corporation | idem | idem |
| Redistribution | **`unknown`** | idem | idem |
| Disposition | **`repository`, unstaged** pending review | idem | idem |

⚠ **The errata PDF's internal `/Title` says `1.1` while its cover page says "Revision 1 - Sept 2013".**
Recorded as observed; not resolved.

---

## 9. Related components

- [**Semtech SX1262**](../sx1262/README.md) — **Gen 2**, and the migration that broke everything (§2)
- [**Semtech SX1268**](../sx1268/README.md) · [**Semtech LLCC68**](../llcc68/README.md) — Gen-2 siblings
- [**Semtech LR1121**](../lr1121/README.md) · [**LR1110 / LR1120**](../lr11x0/README.md) — **Gen 3**
- [**Semtech LR2021**](../lr2021/README.md) — **Gen 4**, which ships an explicit *SX1276 compatibility mode* (§4.2)
- [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md) · [`vendors/semtech/README.md`](../../../vendors/semtech/README.md) · [Components index](../../README.md)

---

## 10. Sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| X-1 | SX1276/77/78/79 Datasheet | Semtech, via Internet Archive | credible mirror | datasheet | `artifacts/sx1276-77-78-79-datasheet-v5-wayback.pdf` | 2026-09-04 | **Rev. 5, August 2016**, 132 pp | §2, §3 |
| X-2 | SX1276/77/78 Errata Note | Semtech, via Internet Archive | credible mirror | errata | `artifacts/sx1276-77-78-errata-wayback.pdf` | 2026-09-04 | **Revision 1, Sept 2013** | §4.1, G4 |
| X-3 | SX1272/73 Errata Note | Semtech, via Internet Archive | credible mirror | errata | `artifacts/sx1272-73-errata-wayback.pdf` | 2026-09-04 | — | §1 |
| X-4 | SX1276 product page | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-connect/sx1276` | 2026-09-04 | undated | §1 |
| X-5 | SX1272 product page | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-connect/sx1272` | 2026-09-04 | undated | §1 |
| X-6 | `DS.LR20xx` Rev 2.1 §9.8, §23.8 | Semtech via Digi-Key | authorized mirror | datasheet | [held here](../lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf) | 2026-09-04 | Rev 2.1, 13/04/26 | Gen-1 placement and the **2013** date; §4.2, §4.3 |
| X-7 | Wayback CDX index for `semtech.com` PDFs | Internet Archive | archive | index | `web.archive.org/cdx/search/cdx?url=semtech.com/*&matchType=domain&filter=mimetype:application/pdf&limit=6000` | 2026-09-04 | captures 2011–2019 | §8 provenance; the 2013 first-capture dates supporting Gen 1 = 2013 |
| X-8 | RadioLib `src/modules/SX127x`; Meshtastic `LoRaRadioType.h` | jgromes; Meshtastic | community | source | GitHub | 2026-09-04 | §5 |
