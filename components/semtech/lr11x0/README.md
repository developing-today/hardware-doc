# Semtech LR1110 and LR1120 — LoRa Edge™, the third-generation geolocation transceivers

> **Lineage:** [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md).
> **Sibling record:** [`lr1121`](../lr1121/README.md) — the same generation with the geolocation
> front end removed, and the deeper of the two records.

- **Category:** **LoRa / LR-FHSS / (G)FSK** transceiver **+ multi-constellation GNSS scanner + passive Wi-Fi AP-MAC scanner + AES-128 crypto engine**
- **Package:** **QFN32, 5 × 5 mm** both parts **[PP]**
- **Order codes:** `LR1110IMLTRT` · `LR1120IMLRT` ⚠ (see G3)
- **Generation:** **3.** `DS.LR20xx` §23.8: *"Generation 3 (Gen 3): **LR1110, LR1120**, LR1121 - LoRa Edge™ - Added geolocation"* **[DS20]**
- **Research depth:** ⚠ **light record.** Neither datasheet was obtained — both are behind Semtech's Salesforce gate, and **the Wayback Machine has no LR11xx PDF at all**. Content here is Semtech's own feature lists, the Gen-4 datasheet's cross-generation statements, and driver source.
- **Retrieved:** 2026-09-04

**Why one record for two parts:** they share a package, an order-code shape, a command set, a driver
(`SWDR001`), a RadioLib module (`LR11x0`) and a feature list. The LR1120 is the LR1110 with bands
added. Splitting them would duplicate nine sections to change three rows.

---

## Evidence labelling

**[PP]** Semtech product pages (`…/lora-edge/lr1110`, `…/lora-edge/lr1120`), retrieved 2026-09-04 ·
**[DS20]** `DS.LR20xx` Rev 2.1, [held here](../lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf) ·
**[GH]** `github.com/LoRa-Net`, read live · **[RL]** RadioLib · **[MT]** Meshtastic firmware ·
**[INF]** inference.

---

## 1. The two parts

| | **LR1110** | **LR1120** |
|---|---|---|
| Sub-GHz | **150–960 MHz** | **150–960 MHz** |
| 2.4 GHz ISM | ❌ | ✅ |
| Satellite | ❌ | **1.9–2.1 GHz S-band** |
| Sub-GHz max Tx | **+22 dBm** high-power path, **+15 dBm** high-efficiency path | **+22 dBm** |
| 2.4 GHz max Tx | — | **+11.5 dBm** |
| **GNSS (GPS/BeiDou) low-power scanning** | ✅ | ✅ |
| **802.11 b/g/n Wi-Fi ultra-low-power passive scanning** | ✅ | ✅ |
| **AES-128 crypto engine + secure key store** | ✅ | ✅ |
| LR-FHSS modulator | ✅ | ✅ |
| **Synthesiser range** | ⚠ **150–2700 MHz continuous** | not separately stated |
| **RX ADC** | **up to 24 MHz DSB** | not separately stated |
| Package / order code | QFN32 5×5 · `LR1110IMLTRT` | QFN32 5×5 · `LR1120IMLRT` ⚠ |

All rows **[PP]**.

⚠ **The LR1110's "150–2700 MHz continuous frequency synthesizer range" is not a communications
band.** It is the front end's tuning range, and it exists to let the same silicon land on GPS L1
(1575.42 MHz) and Wi-Fi (2.4 GHz) for *scanning*. Reading it as "the LR1110 can transmit at 2.4 GHz"
is wrong — the LR1110 has no 2.4 GHz PA path; that is exactly what the LR1120 adds. **[INF]**, but
strongly: Semtech lists the synthesiser range under *"Multi-Purpose Radio Front-End Targeting
Geolocation Purposes"*, not under the transceiver features.

---

## 2. What the geolocation front end actually is

Semtech's own framing **[PP]**:

> Ultra-low power platform that integrates a LoRa® transceiver, long range FHSS modulator,
> **multi-constellation scanner**, and **passive Wi-Fi AP MAC address scanner** targeting asset
> management applications. The LR1110 solution utilizes Semtech's cloud-based geolocation services
> from Semtech's partners **to significantly reduce power consumption by determining asset location
> in a cloud solver**.

**This is the defining architectural idea of Gen 3, and it is easy to miss.** The chip does **not**
compute a position. It captures a short burst of GNSS pseudorange data or a list of nearby Wi-Fi AP
MAC addresses, and **ships the raw scan over LoRaWAN to a cloud solver** which returns coordinates.
A conventional GNSS receiver has to stay powered long enough to acquire, track and solve; this does
not.

⚠ **Two consequences that belong in any evaluation:**

1. **It creates a cloud dependency for a core function.** No solver, no position. Semtech's
   `SWNW001` (*"Example code to integrate LoRa Edge with cloud solvers"*, MIT) and
   `node-red-contrib-loracloud-utils` exist precisely to wire this up **[GH]**. If the solver
   service changes terms or disappears, the scanner is a data source with no consumer.
2. **Wi-Fi scanning is passive AP-MAC harvesting.** That is a privacy-relevant capability and, in
   some jurisdictions, a regulated one. Worth a deliberate decision, not an accident of part choice.

Also in Gen 3 and worth noting: **RTToF (round-trip time-of-flight) ranging** — `AN1200.78 LR1110
Round-Trip-Time-of-flight Application Note` and the `lr11xx_ranging_demo` repository
(*"a fully featured ranging demonstration featuring communication and distance measurement phases
and the statistical post processing needed to yield accurate results"*) **[GH]**. Gen 4 keeps and
extends this as `RTToF` §10 of `DS.LR20xx` **[DS20]**.

---

## 3. The crypto engine

Identical wording on both product pages **[PP]**:

> **Cryptographic Engine** — Hardware support for **AES-128** encryption/decryption based
> algorithms · Handling device parameters such as **DevEUI and JoinEUI** · **Protects confidential
> information such as encryption keys against unauthorized access** · **Stores NwkKey, AppKey**

Gen 1 and Gen 2 have nothing comparable, and **Gen 4 dropped it** — see
[`lr1121` §2.1](../lr1121/README.md) and
[`lora-radio-generations` §5.3](../../../guides/hardware/lora-radio-generations.md).

---

## 4. Compatibility with the rest of the lineage

Both pages carry the same claim: ***"Fully compatible with SX1261/2/8 devices and the LoRaWAN®
standard, defined by the LoRa Alliance®"*** **[PP]**. Read it as **air-interface and LoRaWAN-profile**
compatibility only — the parts are not pin-compatible with an SX1262 (QFN32 5 × 5 vs QFN24 4 × 4),
the command set differs, and the driver is a different repository. The full unpacking is in
[`lr1121` §3](../lr1121/README.md).

**Long interleaver** is available on Gen 3 and Gen 4 and on nothing older **[DS20]** §23.8 — enable
it and Gen-1/Gen-2 peers cannot decode.

---

## 5. Documents — enumerated, none retrieved

All behind `semtech.my.salesforce.com/sfc/p/…`, `blocked`
([vendor guide §4](../../../vendors/semtech/README.md)). Recorded so the next reader does not repeat
the enumeration.

**LR1110** **[PP]**: Datasheet · `AN1200.56` LR1110 evaluation kit · `AN1200.57` LR11xx Program
Memory Update · `AN1200.58` LR-FHSS Demo Code · `AN1200.59` Selecting the Optimal Reference Clock ·
`AN1200.62` FCC Pre-Compliance testing · `AN1200.64` LR-FHSS System Performance · `AN1200.66` PCB
Design Guidelines · **`AN1200.69` GNSS Antenna** · **`AN1200.70` LoRa Edge Advanced GNSS Scan
Performance Overview** · `AN1200.73` SX126x/LR11xx SigFox Modulation · **`AN1200.74` LoRa Edge Clock
Requirements** · `AN1200.76` LR11xx IPD Reference Design · **`AN1200.78` LR1110 RTToF** ·
`AN1200.80` LoRa Modem Doppler Immunity.

⚠ **`AN1200.69` (GNSS antenna) and `AN1200.74` (clock requirements) have no Gen-2 or Gen-4
equivalent.** A GNSS-scanning design has antenna and reference-clock constraints a plain LoRa design
does not, and those two documents are where they live. Do not start an LR1110/LR1120 board without
them.

**Evaluation kits and reference designs** **[PP]**: `LR1110DVK1TBKS/TCKS/TGKS/TPKS`,
`LR1110MB1LBKS`, `LR1110MB1LCKS`, `LR1110MB1IPDT1DKS`, and the **tracker reference designs**
`LR1110TRK1BKS` (+ `-IN`), `LR1110TRK1CKS` (+ `-AU`, `-JP`, `-KR`); `LR1120DVK1TBKS/TCKS/TGKS/TPKS`,
`LR1120MB1IPDT1DKS`; `LRDVK17INTERFACE`. ⚠ **Note the regional tracker SKUs** — `-AU`, `-JP`, `-KR`,
`-IN` — a level of per-region productisation Gen 4 explicitly set out to eliminate with its
single-SKU front end.

⚠ **No archive route exists.** The Wayback CDX index for `semtech.com` contains **zero LR11xx PDFs**;
these documents have only ever lived behind the Salesforce shell. Negative result, verified.

---

## 6. Software support

| Repo / stack | What | Licence | Last push |
|---|---|---|---|
| **`SWDR001`** | *"Driver for LR11xx chip (LR1110 / LR1120 / LR1121)"* — the reference driver | NOASSERTION | 2026-04-07 |
| **`SWTL001`** | LR11xx **firmware update** procedure | NOASSERTION | 2026-04-07 |
| **`radio_firmware_images`** | *"Firmware images for all flash-based Semtech products"* | — | 2026-04-07 |
| **`SWSD003`** | LR11xx **and** SX126x SDK | NOASSERTION | 2025-10-01 |
| **`SWSD006`** | LR11xx multi-stack SDK for nRF52840 | Apache-2.0 | 2025-02-12 |
| **`SWSD004`** / `lora_edge_tracker_ref_design` | Tracker reference-design applications | NOASSERTION | 2025-10-27 |
| **`SWDR006` / `SWDR007`** | LR11xx **Amazon Sidewalk** drivers (nRF52840 / SiLabs EFR32) | NOASSERTION | 2024-07-18 / 2024-08-22 |
| **`lr11xx_ranging_demo`** | RTToF demonstration | NOASSERTION | 2025-04-02 |
| **`SWNW001`** | *"Example code to integrate LoRa Edge with cloud solvers"* | **MIT** | 2025-07-15 |
| `node-red-contrib-loracloud-utils` | Node-RED LoRa Cloud integration | — | 2023-07-18 |
| `lr1110_driver` | **Superseded** by `SWDR001` | BSD-3-Clause-Clear | 2022-04-13 |
| `lr1110_evk_demo_app` | EVK demo | — | 2021-11-03 |
| **`LoRa_Basics_ModemE`**, `ModemE_command_interpreter`, `ModemE_application_examples`, `lr1121_modemE_driver` | The **Modem-E** firmware variant — LoRaWAN stack running *inside* the radio | — | 2024–2026 |
| **RadioLib** | `src/modules/LR11x0` with `LR1110`, `LR1120`, `LR1121` classes | MIT | current |
| **Meshtastic** | `LR1110Interface`, `LR1120Interface`, shared `LR11x0Interface`; `LR1110_RADIO` / `LR1120_RADIO` in `LoRaRadioType`, present in **v2.7.26 stable** | GPL-3.0 | current |

All **[GH]**, **[RL]**, **[MT]**, read 2026-09-04.

**Modem-E deserves a sentence**, because it has no Gen-4 counterpart: it is a Semtech firmware image
that runs the LoRaWAN stack *on the radio*, so the host MCU speaks a high-level command interface
instead of a PHY driver. Four repositories support it. If you have seen "LoRa Basics Modem-E" and
wondered where it fits, it is a Gen-3 delivery mode.

---

## 7. Caveats and gaps

| # | Issue |
|---|---|
| **G1** | ⚠ **Neither datasheet was obtained** (§5), and **no archive route exists**. Every claim here is from a marketing feature list. No electrical figure is reproduced |
| **G2** | ⚠ **Geolocation is cloud-dependent by design** (§2). The chip scans; a solver locates |
| **G3** | ⚠ **`LR1120IMLRT` on Semtech's own page is missing a `T`** relative to `LR1110IMLTRT`/`LR1121IMLTRT`. Probable typo — verify before ordering. `unresolved` |
| **G4** | **The LR1110 cannot transmit at 2.4 GHz** despite a 150–2700 MHz synthesiser. The range is for scanning (§1) |
| **G5** | **Passive Wi-Fi MAC scanning is a privacy-relevant capability**, and in some jurisdictions a regulated one. Decide deliberately |
| **G6** | **Introduction date not established.** "2020" is widely repeated; no Semtech-dated source retrieved. `unresolved` |
| **G7** | ⚠ **`lr1110_driver` is superseded by `SWDR001`** but is still present, still findable, and still the top search hit for "lr1110 driver". Last push 2022-04-13 |
| **G8** | **Nothing measured**; no hardware, teardown or community measurement gathered |
| **G9** | ⚠ **Regional tracker SKUs (`-AU`, `-JP`, `-KR`, `-IN`) mean the reference design is not one design.** Do not assume a `TRK1CKS` document applies to a `TRK1CKS-JP` |

---

## 8. Used By

**No board in this knowledge base uses an LR1110 or LR1120.** Boards that do, for navigability:
Semtech's own **LoRa Edge Tracker reference design** (`LR1110TRK1*`, with regional variants), and
Meshtastic's LR1110/LR1120 variants **[MT]**.

---

## 9. Local artifacts

**None** — see §5 and G1. `artifacts/` does not exist for this component because nothing was
obtained. Recorded as a deliberate gap.

**How to fill it:** Digi-Key or Mouser mirror, per
[`vendors/semtech/README.md` §6](../../../vendors/semtech/README.md). ⚠ Wayback will not work.

---

## 10. Related components

- [**Semtech LR1121**](../lr1121/README.md) — same generation, no scanners, filed under `lora-connect`
- [**Semtech LR2021**](../lr2021/README.md) — **Gen 4**; ⚠ **no GNSS, no Wi-Fi scanning, no crypto engine**
- [**Semtech SX1262**](../sx1262/README.md) — **Gen 2**
- [**Semtech SX1276**](../sx1276/README.md) — **Gen 1**
- [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md) · [`vendors/semtech/README.md`](../../../vendors/semtech/README.md) · [Components index](../../README.md)

---

## 11. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| E-1 | LoRa Edge™ LR1110 product page | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-edge/lr1110` | 2026-09-04 | §1, §2, §3, §5 |
| E-2 | LoRa Edge™ LR1120 product page | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-edge/lr1120` | 2026-09-04 | §1, §3, §5 |
| E-3 | `DS.LR20xx` Rev 2.1 §23.8 | Semtech via Digi-Key | authorized mirror | datasheet | [held here](../lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf) | 2026-09-04 | generation placement; §4 |
| E-4 | Semtech product sitemap | Semtech | primary | sitemap | `www.semtech.com/sitemap-products.xml` | 2026-09-04 | §5 EVK/reference-design SKU list |
| E-5 | `LoRa-Net` org listing | Semtech | primary | source | `api.github.com/orgs/LoRa-Net/repos` | 2026-09-04 | §6 |
| E-6 | RadioLib · Meshtastic firmware | jgromes · Meshtastic | community | source | GitHub | 2026-09-04 | §6 |
| E-7 | Wayback CDX index for `semtech.com` PDFs | Internet Archive | archive | index | `web.archive.org/cdx/search/cdx?url=semtech.com/*&matchType=domain&filter=mimetype:application/pdf` | 2026-09-04 | §5 — **negative result: zero LR11xx PDFs** |
