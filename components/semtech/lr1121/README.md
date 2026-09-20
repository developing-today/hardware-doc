# Semtech LR1121 — LoRa Connect™, the third-generation multi-band transceiver

> **Lineage:** [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md)
> — the four generations side by side. **Domain:** [`guides/lora`](../../../guides/lora/README.md).

- **Category:** multi-band **LoRa / LR-FHSS / (G)FSK** half-duplex transceiver with an **AES-128 cryptographic engine and secure key store**
- **Bands:** **150–960 MHz** (sub-GHz) **+ 2.4 GHz ISM + 2 GHz S-band + 1.55 GHz L-band** **[PP]**
- **Package:** **QFN32, 5 × 5 mm** · **Order code `LR1121IMLTRT`**, Pb-free/RoHS **[PP]**
- **Generation:** **3**, stated twice over — Semtech's product page opens *"The LR1121 is Semtech's **third generation** ultra-low power LoRa® transceiver"*, and `DS.LR20xx` §23.8 lists *"Generation 3 (Gen 3): LR1110, LR1120, **LR1121** - LoRa Edge™ - Added geolocation"* **[PP]**, **[DS20]**
- **Research depth:** ⚠ **light record.** The LR1121 datasheet is behind Semtech's Salesforce gate and **was not obtained** (§5). Everything here comes from Semtech's product page, the Gen-4 datasheet's cross-generation statements, and driver source. **No LR1121 datasheet figure is reproduced here.**
- **Retrieved:** 2026-09-04

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[PP]** | Semtech LR1121 product page, `www.semtech.com/products/wireless-rf/lora-connect/lr1121`, retrieved 2026-09-04 |
| **[DS20]** | `DS.LR20xx` Rev 2.1 — the **LR2021** datasheet, cited only where it makes cross-generation statements. [Held here](../lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf) |
| **[RL]** | RadioLib source, read live 2026-09-04 |
| **[MT]** | Meshtastic firmware source, read live 2026-09-04 |
| **[GH]** | `github.com/LoRa-Net`, read live 2026-09-04 |
| **[3P]** | Third-party vendor page |
| **[INF]** | Inference |

---

## 1. Identity and what makes it odd

**The LR1121 is the LR1120 with the geolocation front end removed.** That single sentence explains
everything unusual about it, including why Semtech files it in a different product family from its
own siblings.

| | **LR1110** | **LR1120** | **LR1121** |
|---|---|---|---|
| Sub-GHz 150–960 MHz | ✅ | ✅ | ✅ |
| 2.4 GHz ISM | ❌ | ✅ | ✅ |
| Satellite | ❌ | 1.9–2.1 GHz S-band | **2 GHz S-band + 1.55 GHz L-band** |
| **GNSS scanning** | ✅ | ✅ | ❌ |
| **Wi-Fi passive scanning** | ✅ | ✅ | ❌ |
| **AES-128 crypto + key store** | ✅ | ✅ | ✅ |
| Semtech catalogue family | `lora-edge` | `lora-edge` | ⚠ **`lora-connect`** |

**[PP]** for all rows. So the LR1121 is a *communications* part shelved with the communications
parts, while carrying a Gen-3 part number. ⚠ **Consequence for enumeration: you will not find it by
browsing `lora-edge`, and you will not find `lr1110`/`lr1120` by browsing `lora-connect`.** Use
`sitemap-products.xml` — [`vendors/semtech/README.md` §2.2](../../../vendors/semtech/README.md).

---

## 2. Capability, as Semtech states it

Reproduced from the product page's own feature list **[PP]**:

- Low-power high-sensitivity **LoRa/(G)FSK half-duplex** RF transceiver
- Worldwide ISM support **150–960 MHz (sub-GHz) and 2.4 GHz, as well as 2 GHz S-Band and 1.55 GHz L-Band**
- Low-noise-figure RX front end
- **High-power PA path +22 dBm** in the sub-GHz band; **PA path up to +11.5 dBm** in the 2.4 GHz band
- **LR-FHSS modulator**
- *"Integrated PA regulator supply selector to simplify dual power +15/+22 dBm with one board implementation (sub-GHz)"*
- *"Able to support world-wide multi-region BOM, the circuit adapts to matching network to satisfy regulatory limits"*
- **"Fully compatible with SX1261/2/8 devices and the LoRaWAN standard, defined by the LoRa Alliance"**

### 2.1 ⭐ The cryptographic engine — the reason to choose Gen 3

**[PP]**, verbatim:

> **Cryptographic Engine**
> • Supports **AES-128** encryption/decryption based algorithms
> • Handles device parameters such as **DevEUI and JoinEUI**, as defined by the LoRa Alliance
> • **Protects confidential information such as encryption keys against unauthorized access**
> • **Stores NwkKey, AppKey**, as defined in the LoRaWAN standard

**No other generation has this.** Gen 1 and Gen 2 have no crypto engine at all, and **Gen 4 dropped
it** — the string `AES` does not appear anywhere in the 243-page `DS.LR20xx` **[DS20]**, and
Waveshare's own `Core1121` vs `Core2021` comparison marks AES-128 and secure key storage as present
on the LR1121 and absent on the LR2021 **[3P]**.

⚠ **This is the single most important fact on this page for anyone planning a migration.** If your
LoRaWAN root keys currently live inside an LR1121, **the LR2021 has nowhere to put them** and you
need MCU-side storage or an external secure element. Say so explicitly in your migration plan.

---

## 3. ⚠ What "fully compatible with SX1261/2/8" does and does not mean

Semtech's phrasing is on all three Gen-3 product pages and is easy to over-read.

**It means:** the LoRa air interface and the LoRaWAN physical-layer profile interoperate. `DS.LR20xx`
§23.8 backs this — *"all the LoRaWAN configurations are fully compatible between all four
generations of LoRa radios"* **[DS20]**.

**It does not mean:**

| | SX1262 (Gen 2) | LR1121 (Gen 3) |
|---|---|---|
| Package | QFN **24**, 4 × 4 mm | QFN **32**, 5 × 5 mm |
| Pin compatible | — | ❌ **No** |
| Command set | SX126x | **LR11xx — different** |
| Driver | `sx126x_driver` | **`SWDR001`, a separate repository** **[GH]** |
| RadioLib module | `SX126x` | **`LR11x0`, a separate module** **[RL]** |
| Firmware image in the part | none | ✅ **updatable program memory** — see §4 |

**Long interleaver is a Gen-3/Gen-4-only LoRa option** **[DS20]** §23.8: turn it on and a Gen-1 or
Gen-2 peer cannot decode the packet. That is the one air-interface asymmetry to watch.

---

## 4. The firmware image — a Gen-3 concept Gen 2 does not have

LR11xx parts carry updatable **program memory**, and Semtech ships tooling specifically for it:

- `AN1200.57 LR11xx Program Memory Update` **[PP]** document list
- **`LoRa-Net/SWTL001`** — *"Reference implementation of the LR11xx firmware update procedure"*, last push 2026-04-07 **[GH]**
- **`LoRa-Net/radio_firmware_images`** — *"Firmware images for all flash-based Semtech products"*, last push 2026-04-07 **[GH]**

This is the ancestor of the Gen-4 **PRAM** mechanism, but it is not the same thing: LR11xx program
memory is *updated* and persists; Gen-4 PRAM is *re-uploaded at every cold start*
([LR2021 §7.1](../lr2021/README.md)). ⚠ **A driver written for one will not do the other.**

---

## 5. Documents — and why this record is light

Enumerated from the product page 2026-09-04 **[PP]**. **None was retrieved**: every one is behind
`semtech.my.salesforce.com/sfc/p/…`, which is `blocked` for automated clients
([vendor guide §4](../../../vendors/semtech/README.md)). Recorded so the next reader does not
re-enumerate.

| Document | Notes |
|---|---|
| **LR1121 Datasheet** | The primary gap in this record |
| **LR1121 User Manual** | ⚠ Note the LR11xx line splits datasheet from **user manual** — the SX126x line does not. Two documents to find, not one |
| `AN1200.57` LR11xx Program Memory Update | §4 |
| `AN1200.58` Long-Range FHSS Demo · `AN1200.64` LR-FHSS System Performance · `AN1200.81` LR-FHSS Doppler Immunity | LR-FHSS trio |
| `AN1200.59` Selecting the Optimal Reference Clock · `AN1200.66` PCB Design Guidelines | shared with the LR2021 page, different tokens |
| `AN1200.62` FCC Pre-Compliance testing of LoRaWAN Modules | |
| `AN1200.73` SX126x/LR11xx **SigFox** Modulation | how Gen 2/3 do BPSK without a BPSK modem — the LR2021 has one natively |
| `AN1200.76` LR11xx **IPD Reference Design** · `AN1200.80` LoRa Modem Doppler Immunity | |
| `AN1200.92` Modem-E Evaluation Guide · **LoRa Basics Modem-E V2.0 Reference Manual** | the Modem-E firmware variant |
| `AN1200.94` / `AN1200.96` One-Channel LoRa Hub | |
| Design files: `LR1121DVK1TGKS` @490 MHz · `LR1121DVK1TxKS` @868/915 MHz | |
| Module design files: `LR1121MB2THDAS`, `LR1121MB2XHDAS` (+22 dBm, 0201, XTAL), `LR1121MB2XLDAS` (+14 dBm) | ⚠ two are titled *"not purchasable"* |
| `LRDVK17INTERFACE` LoRa Shield → EFR32 interface board UG + production files | |

**Evaluation kits** **[PP]**: `LR1121DVK1TBKS` (EU 868), `LR1121DVK1TCKS` (NA 915),
`LR1121DVK1TGKS` (CN 490), `LR1121ED1THDAS`.

⚠ **The Wayback Machine cannot help.** The CDX index for `semtech.com` contains **zero LR11xx PDFs**
— these documents have only ever lived behind the Salesforce shell
([vendor guide §5.2](../../../vendors/semtech/README.md)). **There is no archive route to an LR11xx
datasheet.** Negative result, `executed-success` for the search.

---

## 6. Software support

| Stack | Status |
|---|---|
| **RadioLib** | ✅ `src/modules/LR11x0`, with `LR1110`, `LR1120` and `LR1121` classes. MIT **[RL]** |
| **Semtech `SWDR001`** | ✅ *"Driver for LR11xx chip (LR1110 / LR1120 / LR1121)"*, last push 2026-04-07 **[GH]** |
| **`SWSD003`** | LR11xx **and** SX126x SDK — the two generations share an SDK, which the LR20xx does not join **[GH]** |
| **`SWSD006`** | LR11xx multi-stack SDK for nRF52840, Apache-2.0 **[GH]** |
| **`SWDR006` / `SWDR007`** | LR11xx **Amazon Sidewalk** drivers for nRF52840 and Silicon Labs EFR32 **[GH]** |
| **`lr11xx_ranging_demo`** | RTToF ranging demo **[GH]** |
| **`lr1121_modemE_driver`** (`SWDR009`) | Modem-E firmware variant driver **[GH]** |
| **USP** | "buildable" on LR11xx shields — not Semtech-validated **[GH]** |
| **Meshtastic** | ✅ `LR1121Interface` alongside `LR1110Interface`, `LR1120Interface` and a shared `LR11x0Interface`; `LR1121_RADIO` in `LoRaRadioType`. Present in **v2.7.26 stable** — unlike the LR2021 **[MT]** |
| **Zephyr** | via `usp_zephyr` / `LBM_Zephyr` (Apache-2.0) **[GH]** |
| Linux kernel | ❌ none — userspace SPI only. Negative result |

**The LR11xx has markedly better tooling than the LR20xx**: a standalone driver, two SDKs, two
Sidewalk ports, a ranging demo, and stable-release Meshtastic support. That is what four extra
years buys.

---

## 7. Caveats and gaps

| # | Issue |
|---|---|
| **L1** | ⚠ **The datasheet was not obtained** (§5). Every electrical claim here is from a marketing feature list, and no sensitivity, current or timing figure is reproduced. This record is deliberately thin rather than confidently wrong |
| **L2** | ⚠ **The LR1121 has no GNSS and no Wi-Fi scanner** despite being "LoRa Edge generation". Assuming otherwise from the part number is the standard error |
| **L3** | ⚠ **Semtech's own page prints the LR1120 order code as `LR1120IMLRT`**, missing the `T` that `LR1110IMLTRT` and `LR1121IMLTRT` both carry. Almost certainly a typo — **confirm before ordering**. `unresolved` **[PP]** |
| **L4** | **"Fully compatible with SX1261/2/8" is an air-interface claim only** (§3) |
| **L5** | **Long interleaver excludes Gen-1/Gen-2 peers** **[DS20]** §23.8 |
| **L6** | **Introduction date not established.** "2020" for the LR1110 is widely repeated but no Semtech-dated source was retrieved and no LR11xx PDF exists in the Wayback index. `unresolved` |
| **L7** | **Nothing measured.** No hardware, no teardown, no community measurement gathered for this part |

---

## 8. Used By

**No board in this knowledge base uses an LR1121.** Every LoRa-bearing device documented here
carries a Gen-2 [SX1262](../sx1262/README.md).

Boards that do, so the record is navigable: **LilyGo T3-S3 LR1121** (`lilygo.cc/products/t3-s3-lr1121`,
cited by community discussion), **Waveshare `Core1121-XF`** **[3P]**, and Meshtastic's LR1121
variants **[MT]**.

---

## 9. Local artifacts

**None.** The datasheet and user manual are `blocked` (§5) and no mirror was located this pass.
⚠ Recorded as a deliberate gap, not an oversight: `artifacts/` does not exist for this component
because nothing was obtained.

**How to fill it**, in order of likelihood: Digi-Key `mm.digikey.com/Volume0/opasdata/…` (needs the
exact opaque path from a Digi-Key product page); Mouser `www.mouser.com/pdfDocs/<id>LR1121…pdf` with
the **WhatsApp** User-Agent; a board-vendor mirror (Waveshare and LilyGo both ship LR1121 modules).
Method: [`vendors/semtech/README.md` §6](../../../vendors/semtech/README.md).

---

## 10. Related components

- [**Semtech LR1110 / LR1120**](../lr11x0/README.md) — the geolocation siblings this part is derived from
- [**Semtech LR2021**](../lr2021/README.md) — **Gen 4**, and what you lose by moving to it
- [**Semtech SX1262**](../sx1262/README.md) — **Gen 2**, the "fully compatible" claim's referent
- [**Semtech SX1276**](../sx1276/README.md) — **Gen 1**
- [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md)
- [`vendors/semtech/README.md`](../../../vendors/semtech/README.md)
- [Components index](../../README.md)

---

## 11. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| L-1 | LoRa Connect LR1121 product page | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-connect/lr1121` | 2026-09-04 | §1, §2, §5 — including the **"third generation"** wording |
| L-2 | `DS.LR20xx` Rev 2.1 §23.8 | Semtech via Digi-Key | authorized mirror | datasheet | [held here](../lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf) | 2026-09-04 | §1 generation placement; §3 interoperability |
| L-3 | LR1110 / LR1120 product pages | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-edge/lr111{0,2}0` | 2026-09-04 | §1 comparison table; L3 |
| L-4 | `LoRa-Net` org listing | Semtech | primary | source | `api.github.com/orgs/LoRa-Net/repos` | 2026-09-04 | §4, §6 |
| L-5 | RadioLib `src/modules/LR11x0` | jgromes | community | source | `github.com/jgromes/RadioLib` | 2026-09-04 | §3, §6 |
| L-6 | Meshtastic `src/mesh/LR11*`, `LoRaRadioType.h` @ `v2.7.26.54e0d8d` | Meshtastic | community | source | `github.com/meshtastic/firmware` | 2026-09-04 | §6 |
| L-7 | `Core2021-XF` comparison table (`Core1121-XF` column) | Waveshare | primary | store listing | `www.waveshare.com/Core2021-XF.htm` | 2026-09-04 | §2.1 — independent confirmation of the crypto asymmetry |
| L-8 | Wayback CDX index for `semtech.com` PDFs | Internet Archive | archive | index | `web.archive.org/cdx/search/cdx?url=semtech.com/*&matchType=domain&filter=mimetype:application/pdf` | 2026-09-04 | §5 — **negative result: zero LR11xx PDFs** |
