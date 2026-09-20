# Semtech LLCC68 — "LoRa Smart Home", the cost-reduced SX1262 that cannot do SF12

> **Lineage:** [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md).
> **Domain:** [`guides/lora`](../../../guides/lora/README.md). **Full sibling record:**
> [`sx1262`](../sx1262/README.md) — read that for the register model, `BUSY` handshake, DIO2/DIO3
> behaviour and the four mandatory errata workarounds. **All of it applies here unchanged.**

- **Category:** sub-GHz **LoRa / (G)FSK** transceiver, SPI command interface, **+22 dBm**
- **Generation:** **2** — an SX1262 sibling. ⚠ Not named in `DS.LR20xx` §23.8, which lists one or two representatives per generation; assigning it to Gen 2 is **[INF]**, from *"Pin-to-pin compatible to SX1262"* **[PP]**
- **Package:** *"QFN (same as SX1262)"* — i.e. QFN24, 4 × 4 mm **[PP]**
- **Research depth:** ⚠ **light record.** The LLCC68 datasheet is behind Semtech's Salesforce gate and **was not obtained**. Content here is Semtech's product page, RadioLib source, and the SX1262 record.
- **Retrieved:** 2026-09-04

---

## 1. ⚠ The substitution trap, stated plainly

**Cheap modules and cheap boards use the LLCC68 and the SX1262 interchangeably, and they are not
interchangeable.** They share a pinout, a package, a command set, a register map and a driver base
class. What differs is the LoRa configuration space, and it differs in the direction that matters
most for range.

| | **SX1262** | **LLCC68** |
|---|---|---|
| Max link budget **[PP]** | **170 dB** | **151 dB** |
| Best sensitivity **[PP]** | **−148 dBm** | **−129 dBm** |
| **Max SF at BW 125 kHz** | **SF12** | ⚠ **SF9** |
| **Max SF at BW 250 kHz** | SF12 | ⚠ **SF10** |
| **Max SF at BW 500 kHz** | SF12 | ⚠ **SF11** |
| **Bandwidths below 100 kHz** | ✅ down to 7.81 kHz | ❌ **none** |
| LoRa bit-rate range **[PP]** | up to 62.5 kbps | **1.76 – 62.5 kbps** |
| Max Tx | +22 dBm | +22 dBm |
| RX current | 4.6 mA | 4.6 mA |
| FSK | to 300 kbps | to 300 kbps |
| Pinout | — | **pin-to-pin compatible** |

**19 dB of link budget.** That is roughly the difference between a 2 km link and a 200 m one, and it
is invisible from the schematic, the footprint and the module photo.

### 1.1 The restriction, in Semtech's own words

**[PP]**, verbatim from the LLCC68 product page feature list:

> Data rates for LoRaWAN include **SF7 to SF9 at 125 kHz, SF7 to SF10 at 250 kHz, and SF7 to SF11 at
> 500 kHz**

### 1.2 The restriction, as code

**RadioLib encodes it structurally, which is independent confirmation** — `src/modules/LLCC68/LLCC68.cpp`,
read live 2026-09-04 **[RL]**:

```cpp
class LLCC68: public SX1262 { ... };            // derives from SX1262

int16_t LLCC68::setBandwidth(float bw) {
  RADIOLIB_CHECK_RANGE(bw, 100.0f, 510.0f, RADIOLIB_ERR_INVALID_BANDWIDTH);   // ⚠ floor of 100 kHz
  return(SX1262::setBandwidth(bw));
}

int16_t LLCC68::setSpreadingFactor(uint8_t sf) {
  switch(SX126x::bandwidth) {
    case RADIOLIB_SX126X_LORA_BW_125_0: RADIOLIB_CHECK_RANGE(sf, 5,  9, ...); break;   // ⚠
    case RADIOLIB_SX126X_LORA_BW_250_0: RADIOLIB_CHECK_RANGE(sf, 5, 10, ...); break;
    case RADIOLIB_SX126X_LORA_BW_500_0: RADIOLIB_CHECK_RANGE(sf, 5, 11, ...); break;
    default: return(RADIOLIB_ERR_INVALID_SPREADING_FACTOR);
  }
  return(SX1262::setSpreadingFactor(sf));
}
```

Two things to take from that beyond the numbers:

1. ⚠ **`setBandwidth` has a 100 kHz floor.** The SX1262's narrow bandwidths — 7.81, 10.4, 15.6,
   20.8, 31.25, 41.7, 62.5 kHz — are **all unavailable**. Semtech's marketing line only mentions the
   SF ceiling; the bandwidth floor is at least as consequential, and is the reason a "just use a
   lower bandwidth instead" workaround does not exist.
2. ⚠ **The SF check reads the *current* bandwidth.** Set SF before BW and you can get a spurious
   rejection, or pass a check against the wrong limit. **Always set bandwidth first.**

### 1.3 What it means in practice

- **Meshtastic's `LONG_SLOW` and `VERY_LONG_SLOW` presets use SF12.** An LLCC68 node **cannot join
  such a mesh at all** — not "with reduced range", at all. `RADIOLIB_ERR_INVALID_SPREADING_FACTOR`.
- **LoRaWAN DR0 (SF12/125 kHz) is unreachable.** In EU868 that is the mandatory join/fallback data
  rate, so an LLCC68 end device has a materially different regional-parameter story.
- **A board advertised as "SX1262-compatible" tells you nothing about which die is fitted.** They
  are pin-to-pin compatible, so a manufacturer can substitute silently between production runs.

### 1.4 How to tell which one you have

Ranked by reliability:

1. **Read the chip marking.** Definitive, needs a teardown and a microscope.
2. **Ask the driver.** RadioLib's `SX126x` base exposes the device's status; more practically,
   **request SF12 at BW 125 kHz.** An SX1262 accepts it; an LLCC68 returns
   `RADIOLIB_ERR_INVALID_SPREADING_FACTOR` **[RL]**. Cheap, non-destructive, conclusive for the
   thing you actually care about. **[INF]** — logically sound, `not-tested` on hardware here.
3. **Read the firmware.** Which RadioLib class does the vendor instantiate? This is the method the
   [SX1262 record](../sx1262/README.md) used to establish `62` rather than `61`, and it generalises.
4. ⚠ **Do not trust the product name.** "LoRa Smart Home" is Semtech's marketing name for the
   LLCC68; module vendors rarely use it.

---

## 2. What is identical to the SX1262

Everything in [`components/semtech/sx1262/README.md`](../sx1262/README.md) except §1's table.
Specifically: the SPI command interface and 8-bit opcodes; the mandatory `BUSY` handshake;
`SetDio2AsRfSwitchCtrl` and `SetDio3AsTcxoCtrl`; the DC-DC/LDO choice and the fact that **the DC-DC
does not help transmit current** because the PA runs from `VBAT`; the four §15 errata workarounds
including the **SX1262-only PA-clamp fix**, which applies to the LLCC68 too since it shares the
+22 dBm PA topology; `XOSC_START_ERR` being expected at power-on with a TCXO; and the 150–960 MHz
synthesiser range.

**Do not duplicate that material here.** If you are debugging an LLCC68, you are debugging an
SX1262 with a smaller configuration space.

---

## 3. Software support

| Stack | Status |
|---|---|
| **RadioLib** | ✅ `src/modules/LLCC68`, **deriving from `SX1262`** and overriding exactly two methods (§1.2). MIT **[RL]** |
| **Semtech `llcc68_driver`** | ✅ standalone repository, **BSD-3-Clause-Clear**, last push **2025-10-15** — same day as `sx126x_driver`, so the two are maintained in lockstep **[GH]** |
| **`one_channel_hub`** | Semtech's ESP-IDF one-channel hub explicitly *"with support of sx1261, sx1262, sx1268 and llcc68 Semtech radio chips"* **[GH]** |
| **Meshtastic** | ✅ `LLCC68_RADIO` in `LoRaRadioType`, present in **v2.7.26 stable** **[MT]** |
| **USP** | "buildable" on SX126x shields; the LLCC68 is not separately called out **[GH]** |
| Linux kernel | ❌ none |

⚠ **The LLCC68 has a standalone Semtech driver while the Gen-4 LR20xx does not**
([LR2021 G11](../lr2021/README.md)). Worth knowing when you are weighing ecosystem maturity.

---

## 4. Caveats and gaps

| # | Issue |
|---|---|
| **L1** | ⚠ **The datasheet was not obtained.** Salesforce-gated ([vendor guide §4](../../../vendors/semtech/README.md)). Every figure here is from the product page or RadioLib source. **No datasheet section is cited in this record** |
| **L2** | ⚠ **The SF/BW restriction is the whole point of the part** (§1) and is invisible from the footprint |
| **L3** | ⚠ **Bandwidths below 100 kHz are unavailable** — a restriction Semtech's marketing line does not mention (§1.2) |
| **L4** | ⚠ **Set bandwidth before spreading factor** — the SF check reads the current BW (§1.2) |
| **L5** | **Pin-to-pin compatibility makes silent substitution easy.** A vendor can change die between runs without changing the PCB |
| **L6** | **Generation assignment is `inferred`**, not stated by Semtech (§0) |
| **L7** | **Nothing measured**; no LLCC68 hardware in this knowledge base |
| **L8** | **Introduction date not established.** `unresolved` |

---

## 5. Used By

**No board in this knowledge base uses an LLCC68.** Every LoRa-bearing device here carries an
[SX1262](../sx1262/README.md) — which is precisely why this record exists: the two are pin-compatible
and a future board could carry either.

---

## 6. Local artifacts

**None.** The datasheet is `blocked` and no mirror was located this pass. Recorded as a deliberate
gap; `artifacts/` does not exist for this component.

**How to fill it:** Digi-Key `mm.digikey.com/Volume0/opasdata/…` or Mouser `pdfDocs` with the
**WhatsApp** User-Agent — [`vendors/semtech/README.md` §6](../../../vendors/semtech/README.md).
⚠ Wayback has no LLCC68 PDF under `semtech.com`.

---

## 7. Related components

- [**Semtech SX1262**](../sx1262/README.md) — **the record to read.** Everything except §1 applies
- [**Semtech SX1268**](../sx1268/README.md) — the other SX1262 sibling; a *band* restriction rather than an SF/BW one
- [**Semtech LR2021**](../lr2021/README.md) — **Gen 4** · [**LR1121**](../lr1121/README.md) — **Gen 3** · [**SX1276**](../sx1276/README.md) — **Gen 1**
- [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md) · [`guides/lora` §4](../../../guides/lora/README.md) — the existing SX1261/62/68 comparison · [`vendors/semtech/README.md`](../../../vendors/semtech/README.md) · [Components index](../../README.md)

---

## 8. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| C-1 | LoRa Connect for Smart Home (LLCC68) product page | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-connect/llcc68` | 2026-09-04 | §1, §1.1 — including *"Pin-to-pin compatible to SX1262"* and the SF/BW sentence |
| C-2 | RadioLib `src/modules/LLCC68/LLCC68.cpp`, `LLCC68.h` | jgromes | community | source | `github.com/jgromes/RadioLib` | 2026-09-04 | §1.2 — the restriction as executable code; §1.4 |
| C-3 | `LoRa-Net/llcc68_driver`, `one_channel_hub` | Semtech | primary | source | `github.com/LoRa-Net` | 2026-09-04 | §3; BSD-3-Clause-Clear, last push 2025-10-15 |
| C-4 | Meshtastic `src/detect/LoRaRadioType.h` @ `v2.7.26.54e0d8d` | Meshtastic | community | source | `github.com/meshtastic/firmware` | 2026-09-04 | §3 |
| C-5 | SX1262 component record | this repository | derived | record | [`components/semtech/sx1262/README.md`](../sx1262/README.md) | 2026-09-04 | §2 |
