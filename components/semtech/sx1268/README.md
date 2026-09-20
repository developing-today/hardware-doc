# Semtech SX1268 — the 410–810 MHz SX1262

> **Lineage:** [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md).
> **Domain:** [`guides/lora`](../../../guides/lora/README.md). **Full sibling record:**
> [`sx1262`](../sx1262/README.md) — the register model, `BUSY` handshake, DIO2/DIO3 behaviour, the
> DC-DC/LDO trade and the four mandatory errata workarounds. **All of it applies here unchanged.**

- **Category:** sub-GHz **LoRa / (G)FSK** transceiver, SPI command interface, **+22 dBm**
- **Frequency:** ⚠ **410–810 MHz** — *not* the SX1262's 150–960 MHz
- **Generation:** **2** — an SX1262 sibling. ⚠ Not named in `DS.LR20xx` §23.8; the assignment is **[INF]** from the shared datasheet family and Semtech's own grouping of "SX1261, SX1262 and SX1268" on one product page **[PP]**
- **Package:** QFN24, 4 × 4 mm · Order code **`SX1268IMLTRT`**, tape & reel, 3 000 pieces **[PP]**
- **Research depth:** ⚠ **light record.** The SX1261/2/8 datasheet family is Salesforce-gated; **no SX1268-specific document was obtained.** Content is Semtech's product page, RadioLib source, and the SX1262 record.
- **Retrieved:** 2026-09-04

---

## 1. What is different, and it is only one thing that matters

Semtech's product page covers the SX1261, SX1262 and SX1268 together, and the operative sentence is
**[PP]**:

> The **SX1268 is suitable for systems targeting compliance with Chinese regulatory requirements**,
> and runs in the **410 – 810 MHz** range.

| | **SX1262** | **SX1268** |
|---|---|---|
| **Frequency range** | **150 – 960 MHz** | ⚠ **410 – 810 MHz** |
| Max Tx | +22 dBm | **+22 dBm** |
| Max link budget **[PP]** | **170 dB** (quoted as "SX1262 / 68") | **170 dB** |
| Best sensitivity | −148 dBm | −148 dBm |
| RX current | 4.6 mA | 4.6 mA |
| LoRa bit rate | to 62.5 kbps | to 62.5 kbps |
| FSK bit rate | to 300 kbps | to 300 kbps |
| SF range | SF5–SF12, **no restriction** | SF5–SF12, **no restriction** |
| Blocking immunity @1 MHz offset | 88 dB | 88 dB |
| Co-channel rejection, LoRa | 19 dB | 19 dB |
| Errata §15 PA clamp fix | **required** | **required** |
| Package | QFN24 4 × 4 | QFN24 4 × 4 |

**So: an SX1268 is an SX1262 with a different synthesiser/front-end range.** Everything else —
command set, register map, `BUSY`, DIO conventions, PA topology, errata — is the same. That is the
opposite of the [LLCC68](../llcc68/README.md), which keeps the band and cuts the configuration
space.

### 1.1 RadioLib encodes exactly this **[RL]**

Read live 2026-09-04; the [`guides/lora` §4 table](../../../guides/lora/README.md) records the same
lines:

| | `SX1262.cpp` | `SX1268.cpp` |
|---|---|---|
| Enforced frequency range | **150 – 960 MHz** (`:179`) | ⚠ **410 – 810 MHz** (`:180`) |
| Enforced power range | −9 … +22 dBm (`:212`) | −9 … +22 dBm (`:213`) |
| `fixPaClamping()` called from | every `begin`/`beginFSK` variant (`:62,94,125,153`) | **every `begin`/`beginFSK` variant (`:62,94,125,153`)** |

⚠ **`fixPaClamping()` is called on the SX1268 and on no `SX1261` path** — which is independent
confirmation that the SX1268 shares the SX1262's `VBAT`-fed +22 dBm PA topology and therefore its
errata §15.2 5–6 dB clamp defect, even though the datasheet's note is worded "SX1262 only". Treat
the errata section as applying to the whole +22 dBm class. **[INF]**, strongly.

### 1.2 ⚠ Where the substitution trap actually is

**Not on the bench — in the band plan.**

- **868 MHz (EU) and 915 MHz (US) are outside the SX1268's range.** An SX1268 fitted where an
  SX1262 was expected simply cannot operate in the two most common ISM allocations. RadioLib rejects
  the frequency; a hand-rolled driver may not, and will produce an unlocked PLL or an out-of-spec
  emission.
- **433 MHz and the Chinese 470–510 MHz allocation are the SX1268's home**, and there it is the
  right part — the SX1262 covers those frequencies too, but the SX1268's front end is matched for
  them.
- ⚠ **Cheap 433 MHz modules are frequently SX1268 while their listings say "SX1262".** Because the
  parts are pin-compatible and the command set is identical, a driver written for an SX1262 will
  *appear* to work at 433 MHz on either. The divergence only shows up when someone tries to reuse
  the same board design at 868 MHz.
- **How to tell:** ask the driver for **915 MHz**. An SX1262 accepts it; an SX1268 must not.
  **[INF]**, `not-tested` here.

---

## 2. What is identical to the SX1262

Everything in [`components/semtech/sx1262/README.md`](../sx1262/README.md) except the frequency row.
Specifically: the SPI command interface and 8-bit opcodes; the mandatory `BUSY` handshake;
`SetDio2AsRfSwitchCtrl` and `SetDio3AsTcxoCtrl`; the **`VBAT`-fed PA** and the consequence that the
DC-DC cannot reduce transmit current; the 140 mA over-current setting after `SetPaConfig`; the four
§15 errata workarounds; and `XOSC_START_ERR` being expected at power-on with a TCXO.

**Do not duplicate that material here.**

---

## 3. Software support

| Stack | Status |
|---|---|
| **RadioLib** | ✅ `src/modules/SX126x/SX1268.{h,cpp}` — a sibling class of `SX1262` over the shared `SX126x` base. MIT **[RL]** |
| **Semtech `sx126x_driver`** | ✅ covers SX1261/SX1262/SX1268 in one driver, **BSD-3-Clause-Clear**, last push **2025-10-15** **[GH]** |
| **`SWSD003`** | LR11xx **and** SX126x SDK, explicitly *"SX126x chip (SX1261 / SX1262 / SX1268)"* **[GH]** |
| **`one_channel_hub`** | *"with support of sx1261, sx1262, sx1268 and llcc68"* **[GH]** |
| **Meshtastic** | ✅ `SX1268_RADIO` in `LoRaRadioType`, present in **v2.7.26 stable** **[MT]** |
| **USP** | "buildable" on SX126x shields **[GH]** |
| Linux kernel | ❌ none |

---

## 4. Caveats and gaps

| # | Issue |
|---|---|
| **S1** | ⚠ **No SX1268-specific document was obtained.** Salesforce-gated ([vendor guide §4](../../../vendors/semtech/README.md)). Every figure here is from the product page or RadioLib source |
| **S2** | ⚠ **410–810 MHz, not 150–960 MHz.** 868 MHz and 915 MHz are out of range (§1.2) |
| **S3** | ⚠ **Pin-compatible with the SX1262**, so substitution is invisible from the PCB and from the driver until you change band |
| **S4** | **Errata §15.2's "SX1262 only" wording under-states it.** RadioLib applies `fixPaClamping()` to the SX1268 as well (§1.1). Treat it as "+22 dBm class" |
| **S5** | **Generation assignment is `inferred`**, not stated by Semtech |
| **S6** | ⚠ **The "170 dB link budget" figure is printed as "(SX1262 / 68)"** on a page that also covers the SX1261. Do not copy it into an SX1261 row |
| **S7** | **Nothing measured**; no SX1268 hardware in this knowledge base |
| **S8** | **Introduction date not established.** `unresolved` |

---

## 5. Used By

**No board in this knowledge base uses an SX1268.** Every LoRa-bearing device here carries an
[SX1262](../sx1262/README.md). This record exists because the two are pin-compatible, because
433 MHz modules commonly carry the 68, and because
[`guides/lora` §4](../../../guides/lora/README.md) already compares the three parts and deserved a
component record to point at.

---

## 6. Local artifacts

**None.** No SX1268-specific document was obtained; the SX1261/2 datasheet held under
[`sx1262/artifacts/`](../sx1262/README.md) does **not** cover the SX1268. Recorded as a deliberate
gap; `artifacts/` does not exist for this component.

**How to fill it:** Digi-Key or Mouser mirror per
[`vendors/semtech/README.md` §6](../../../vendors/semtech/README.md). ⚠ The Wayback CDX index for
`semtech.com` has `DS_SX1261-2_V1.1.pdf` but **no SX1268 datasheet**.

---

## 7. Related components

- [**Semtech SX1262**](../sx1262/README.md) — **the record to read.** Everything except the frequency row applies
- [**Semtech LLCC68**](../llcc68/README.md) — the other SX1262 sibling; restricts SF/BW instead of band, and is the nastier trap
- [**Semtech LR2021**](../lr2021/README.md) — **Gen 4** · [**LR1121**](../lr1121/README.md) — **Gen 3** · [**SX1276**](../sx1276/README.md) — **Gen 1**
- [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md) · [`guides/lora` §4](../../../guides/lora/README.md) · [`vendors/semtech/README.md`](../../../vendors/semtech/README.md) · [Components index](../../README.md)

---

## 8. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S-1 | SX1268 product page (covers SX1261/SX1262/SX1268) | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-connect/sx1268` | 2026-09-04 | §1 — the 410–810 MHz range and the Chinese-regulatory framing |
| S-2 | RadioLib `src/modules/SX126x/SX1268.cpp` | jgromes | community | source | `github.com/jgromes/RadioLib` | 2026-09-04 | §1.1, §3 |
| S-3 | `LoRa-Net/sx126x_driver`, `SWSD003`, `one_channel_hub` | Semtech | primary | source | `github.com/LoRa-Net` | 2026-09-04 | §3 |
| S-4 | Meshtastic `src/detect/LoRaRadioType.h` @ `v2.7.26.54e0d8d` | Meshtastic | community | source | `github.com/meshtastic/firmware` | 2026-09-04 | §3 |
| S-5 | SX1262 component record; `guides/lora` §4 | this repository | derived | record | [`sx1262`](../sx1262/README.md), [`guides/lora`](../../../guides/lora/README.md) | 2026-09-04 | §1.1, §2 |
