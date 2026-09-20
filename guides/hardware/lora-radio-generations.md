# The four generations of Semtech LoRa transceiver silicon

**What "the 4th gen LoRa chip" is, where the generation numbering comes from, what changed at each
step, and — the part that costs you weeks — what breaks when you move between them.**

Written 2026-09-04. Every claim carries a source marker; §0.1 defines them.

> **Scope.** This guide covers **end-node transceivers**. Semtech's gateway/concentrator silicon
> (SX1301/SX1302/SX1303/SX1308 and the SX125x/SX1250 radio front ends) is a separate product line
> — `lora-core` rather than `lora-connect`/`lora-edge`/`lora-plus` — and is not generation-numbered
> alongside the transceivers. **[SM]**
>
> **Related.** [`guides/lora`](../lora/README.md) is the device-independent LoRa domain guide —
> modulation arithmetic, airtime, duty cycle, band plans, antenna and debugging. This guide is
> about the *silicon lineage*. Read that one to understand LoRa; read this one to choose or migrate
> a part.

---

## 0. The short answer

**The "4th generation LoRa chip" is the Semtech LR2021**, and the label is Semtech's own — printed
on page 1 of its datasheet as **"Generation 4 LoRa® IP"** and used in the product page's own HTML
title. It is the first member of a new family, **LoRa Plus™**, which also contains the **LR2022**
and **LR2012**. **[DS20]**, **[PP]**

The full lineage is not inferred. Semtech states it in **§23.8 of the LR20xx datasheet**, headed
*"Compatibility of Generation 1-4 LoRa Radios"*, verbatim:

> Semtech has developed four generations of LoRa radios:
> • **Generation 1 (Gen 1): SX1272, SX1276** - First LoRa chips (2013)
> • **Generation 2 (Gen 2): SX1261, SX1262, SX1280** - Enhanced performance and efficiency
> • **Generation 3 (Gen 3): LR1110, LR1120, LR1121** - LoRa Edge™ - Added geolocation
> • **Generation 4 (Gen 4): LR2021 LoRa Plus™** Multi-band, and multi-protocol

The identical paragraph appears in **[DS20-1.1]** §23.7, six months earlier — so it is corroborated
across two document revisions, not an editorial one-off. Two further primary confirmations:
the **LR1121** product page opens *"The LR1121 is Semtech's **third generation** ultra-low power
LoRa transceiver"* **[PP]**, and Waveshare's `Core2021` listing independently calls the LR2021
*"the **fourth-generation** LoRa multi-band transceiver"* **[3P]**.

### 0.1 One line per generation

| Gen | Parts Semtech names | Also in the family | Introduced | Defining change | Host interface |
|---|---|---|---|---|---|
| **1** | **SX1272, SX1276** | SX1273, SX1277, SX1278, SX1279 | **2013** **[DS20]** | LoRa exists | **Register-mapped SPI**, no `BUSY` |
| **2** | **SX1261, SX1262, SX1280** | SX1268, LLCC68; STM32WL (SX126x core on-die) | **2018** (SX1280 2017) **[WB]** | "Enhanced performance and efficiency" — 2× lower RX current, +22 dBm, SF5, LR-FHSS, 2.4 GHz | **Command-based SPI + mandatory `BUSY`** |
| **3** | **LR1110, LR1120, LR1121** | — | **2020** (LR1110) **[WB]** | "Added geolocation" — GNSS + Wi-Fi passive scanning, **AES-128 crypto engine and secure key store** | Command-based, **LR11xx** command set |
| **4** | **LR2021** | LR2022, LR2012 | announced **2025-03-12** **[COM]**; datasheet Rev 0.2 **June 2025** **[DS20]** | "Multi-band, and multi-protocol" — dual-band single-SKU, FLRC to 2.6 Mbps, multi-SF receive, BLE/802.15.4/Z-Wave/Sigfox PHYs, SATCOM | Command-based, **16-bit opcodes**, LR20xx command set |

### 0.2 Three things this rules out

| Common claim | Verdict |
|---|---|
| *"SX1280 / LoRa at 2.4 GHz is its own generation"* | ❌ **No.** Semtech puts SX1280 in the **Gen 2** bullet beside the SX1261 and SX1262. 2.4 GHz is a band, not a generation |
| *"LR-FHSS is a generation"* | ❌ **No.** It is a modulation, present on SX126x (Gen 2), LR11xx (Gen 3) and LR20xx (Gen 4). The LR-FHSS patent notice **[DS20]** p. 3 names `SX1261, SX1262, SX1268, LR1110, LR1120, LR1121, LR2012, LR2021, LR2022` as the parts whose purchase conveys rights — a neat cross-generation list |
| *"'4th generation' is community shorthand"* | ❌ **No.** It is on the datasheet cover, in the general description, in the product page title, and in §23.8's heading |

⚠ **§23.8 names one or two representatives per generation, not every part.** SX1268 and LLCC68 are
absent but are SX1262 siblings (Gen 2); SX1273/77/78/79 are absent but are SX1272/76 siblings
(Gen 1); LR2022 and LR2012 are absent because §23.8 was written when the LR2021 was alone.
Assigning those by family is **[INF]**, and marked as such wherever it matters.

---

## 0.3 Evidence markers

| Marker | Source |
|---|---|
| **[DS20]** | `DS.LR20xx` LR2021/LR2022/LR2012 datasheet **Rev 2.1**, 13/04/26, 243 pp — [held here](../../components/semtech/lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf) |
| **[DS20-1.1]** | The same document at **Rev 1.1**, 10/14/25 — [archived](../../components/semtech/lr2021/artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf.ARCHIVED.md) |
| **[DS12]** | `DS.SX1261-2` **Rev 2.2**, Dec 2024 — read by the [SX1262 record](../../components/semtech/sx1262/README.md), not re-read here; figures attributed to it are that record's transcription |
| **[DS76]** | `SX1276/77/78/79` datasheet **Rev. 5, August 2016** — [held here](../../components/semtech/sx1276/artifacts/sx1276-77-78-79-datasheet-v5-wayback.pdf) |
| **[PP]** | Semtech product pages, retrieved 2026-09-04 |
| **[SM]** | `www.semtech.com/sitemap-products.xml`, retrieved 2026-09-04 |
| **[DRV]** | Semtech `lr20xx_driver` v2.0.2 in `LoRa-Net/usp` @ `512a095e…` |
| **[RL]** | RadioLib source, read live at named tags |
| **[MT]** | Meshtastic firmware source, read live |
| **[3P]** | Third-party vendor page (Waveshare, Seeed) |
| **[WB]** | Secondary/date evidence — first appearance in an artifact or archive capture; see §7 |
| **[COM]** | Community — catalogued in [`lr2021/projects-and-community.md`](../../components/semtech/lr2021/projects-and-community.md) |
| **[INF]** | Inference |

⚠ **Nothing in this guide was measured.** Every electrical figure is a manufacturer specification,
reproduced. Where two generations' numbers are compared, they come from two different documents
written years apart under **different measurement conditions** — see §3.1's warning before drawing
a conclusion from a 1 dB difference.

---

## 1. The product families, and why the URL matters

Semtech's own catalogue splits the transceivers into families that map onto generations, and
knowing this is the fastest way to tell what you are looking at. **[SM]**

| URL family | Marketing name | Contains | Generation |
|---|---|---|---|
| `/products/wireless-rf/lora-connect/` | **LoRa Connect™** | SX1272, SX1276, SX1278, SX1261, SX1262, SX1268, LLCC68, SX1280, SX1281, **LR1121** | Gen 1 **and** Gen 2 **and** part of Gen 3 |
| `/products/wireless-rf/lora-edge/` | **LoRa Edge™** | **LR1110, LR1120** | Gen 3 |
| `/products/wireless-rf/lora-plus/` | **LoRa Plus™** | **LR2012, LR2021, LR2022** | **Gen 4** |
| `/products/wireless-rf/lora-core/` | LoRa Core™ | SX1250, SX125x, SX1301/2/3/8 | Gateway silicon — outside this guide |

⚠ **Two traps here, both cost real time.**

1. **`/lora-connect/lr2021` returns a hard HTTP 404.** The LR2021 lives under `lora-plus`. Guessing
   the family from the part number's prefix does not work — `LR1121` is under `lora-connect` while
   its own siblings `LR1110`/`LR1120` are under `lora-edge`. Verified 2026-09-04, `executed-success`.
2. **The `lora-connect` index page does not list the LR2021 at all**, and lists `LR1121` but neither
   `LR1110` nor `LR1120`. **The only complete enumeration is `sitemap-products.xml`.** **[SM]**

**The LR1121 sitting in `lora-connect` rather than `lora-edge` is a real signal, not a filing
error**: alone in Gen 3, the LR1121 has **no GNSS and no Wi-Fi scanner**. It is the LR1120 with the
geolocation front end removed — a communications part in a geolocation family, so Semtech shelved
it with the communications parts. §4.2.

---

## 2. Feature matrix

### 2.1 Modulation and PHY

✅ present · ❌ absent · ⚠ present with a caveat spelled out below.

| | **Gen 1** SX1276 | **Gen 2** SX1262 | **Gen 2** SX1280 | **Gen 3** LR1121 | **Gen 4** LR2021 |
|---|:--:|:--:|:--:|:--:|:--:|
| LoRa | ✅ SF6–SF12 | ✅ **SF5**–SF12 | ✅ SF5–SF12 | ✅ SF5–SF12 | ✅ SF5–SF12 |
| **LR-FHSS** | ❌ | ✅ | ❌ | ✅ | ✅ (incl. **SATCOM**) |
| (G)FSK | ✅ | ✅ | ✅ | ✅ | ✅ |
| MSK / GMSK | ✅ | ✅ | ✅ | ✅ | ✅ |
| OOK | ✅ | ❌ | ❌ | ❌ | ✅ (Rx to **2 Mbps**) |
| **FLRC** | ❌ | ❌ | ✅ | ❌ | ✅ **to 2.6 Mbps** |
| (D)BPSK — Sigfox uplink | ❌ | ⚠ via `AN1200.73` | ❌ | ⚠ via `AN1200.73` | ✅ native modem |
| **BLE PHY** | ❌ | ❌ | ✅ "PHY layer compatibility" | ❌ | ✅ 1M/2M/Coded 500k/125k |
| **O-QPSK 802.15.4** | ❌ | ❌ | ❌ | ❌ | ✅ Thread/Zigbee |
| **Z-Wave / Z-Wave LR** | ❌ | ❌ | ❌ | ❌ | ✅ + HomeID & beam filtering |
| **Wi-SUN FSK / WM-Bus** | ⚠ generic FSK | ⚠ generic FSK | ❌ | ⚠ generic FSK | ✅ **dedicated packet handlers** |
| **Multi-SF receive** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Multi-SF CAD, Fast CAD** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Convolutional CR8/CR9** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Long interleaver** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Intra-packet freq. hopping** | ✅ | ❌ | ❌ | ❌ | ✅ (with an SX1276-compat mode) |
| **Ranging / ToF** | ❌ | ❌ | ✅ ranging engine | ⚠ RTToF on LR1110/20 | ✅ **RTToF** §10 |
| **GNSS scanning** | ❌ | ❌ | ❌ | ❌ **(LR1110/LR1120 only)** | ❌ |
| **Wi-Fi passive scanning** | ❌ | ❌ | ❌ | ❌ **(LR1110/LR1120 only)** | ❌ |
| **AES-128 crypto + key store** | ❌ | ❌ | ❌ | ✅ | ❌ **regression** |

Rows sourced: LoRa/LR-FHSS/CAD/hopping/interleaver/CR from **[DS20]** §23.8 and §9; Gen-4 PHYs from
**[DS20]** §11–§20; Gen-1/2/3 features from **[PP]** and **[DS76]**; crypto from **[PP]** LR1121 and
a whole-document search of **[DS20]** returning no `AES` (§5.3).

### 2.2 Radio and electrical

| | **SX1276** (G1) | **SX1262** (G2) | **SX1280** (G2) | **LR1121** (G3) | **LR2021** (G4) |
|---|---|---|---|---|---|
| Frequency | **137–1020 MHz** | 150–960 MHz | 2.4 GHz ISM | 150–960 MHz **+ 2.4 GHz + 2 GHz S-band + 1.55 GHz L-band** | **150–960 MHz + 1.5–2.5 GHz** |
| Max Tx | +20 dBm (+14 high-eff PA) | **+22 dBm** | +12.5 dBm | +22 dBm sub-GHz / **+11.5 dBm** 2.4 GHz | **+22 dBm** sub-GHz / **+12 dBm** HF |
| Tx power step | — | 1 dB | 1 dB | 1 dB | **0.5 dB, 63 steps** |
| Best LoRa sensitivity | **−148 dBm** | −148 dBm | −132 dBm | ≈−148 dBm class | **−143 dBm @SF12/62 kHz**, **−141.5 @SF12/125 kHz** |
| Max link budget | 168 dB | 170 dB | — | — | not quoted as a single figure |
| Rx current | **9.9 mA** | **4.6 mA** (4.2 mA quoted elsewhere) | "low, on-chip DC-DC" | ≈SX126x class | **5.7 mA** (LoRa SF7/125 kHz) |
| Tx current @max | ~120 mA @+20 dBm | **118 mA @+22 dBm** | — | — | **105 mA @+22 dBm** |
| Sleep / retention | **200 nA** register retention | ~600 nA–1.2 µA | — | — | **470 nA**; ⚠ **+80 nA with PRAM loaded** |
| Supply | 1.8–3.7 V | 1.8–3.7 V | — | — | 1.8–3.7 V |
| Regulator | LDO only | LDO **or DC-DC (core only — PA runs from `VBAT`)** | on-chip DC-DC | LDO or DC-DC | **SIMO buck feeding core *and* PA**, or LDO |
| Package | **QFN 28** | **QFN 24, 4 × 4 mm** | QFN 4 × 4 | **QFN 32, 5 × 5 mm** | **QFN 32, 5 × 5 mm** |
| Order code | `SX1276IMLTRT` | `SX1262IMLTRT` | `SX1280IMLTRT` | `LR1121IMLTRT` | `LR2021IMLTRT` |
| Max LoRa bit rate | 300 kbps (FSK); ~37.5 kbps LoRa | 62.5 kbps LoRa | — | — | **125 kbps LoRa**, 2.6 Mbps FLRC |

⚠ **Do not read the sensitivity row as a ranking.** SX1276's "−148 dBm" and SX1262's "−148 dBm" are
headline figures at very narrow bandwidth; LR2021's "−141.5 dBm" is at **SF12/125 kHz with a 64-byte
payload**, and the same part reaches **−143 dBm at 62 kHz**. **The three numbers come from three
documents with different measurement conditions.** Compare like for like or not at all — the LR20xx
datasheet's Table 3-17 is the only per-SF/per-BW grid transcribed anywhere in this knowledge base
([LR2021 §5.3](../../components/semtech/lr2021/README.md)).

### 2.3 Host interface — the migration-relevant row set

| | **Gen 1** SX127x | **Gen 2** SX126x | **Gen 3** LR11xx | **Gen 4** LR20xx |
|---|---|---|---|---|
| Model | **Register-mapped** — read/write addresses | **Command/opcode** | Command/opcode | Command/opcode |
| SPI mode | 0 | 0 | 0 | 0 |
| Max SCK | 10 MHz | 16 MHz | 16 MHz | **16 MHz** |
| **`BUSY` line** | ❌ **none** | ✅ **mandatory handshake** | ✅ | ✅ |
| **Opcode width** | n/a (address byte) | **8-bit** | 8-bit + sub-opcode (16-bit group/op) | **16-bit** |
| Register addressing | 8-bit address, 8-bit data | 16-bit address, 8-bit data | 32-bit address | **24-bit address, 32-bit data**, with read-modify-write |
| Status on MISO | address echo | **1 status byte** | status word | **2 status bytes + 4 IrqStatus bytes, every command** |
| IRQ status width | 8-bit (`IrqFlags`) | **16-bit** | 32-bit | **32-bit**, *plus a second FIFO-IRQ domain* |
| Data buffer | **FIFO with paged access** | **one 256 B buffer**, `SetBufferBaseAddress` | one 256 B buffer | **two independent 256 B FIFOs** with thresholds, level readback, streaming > 256 B |
| DIO pins | DIO0–DIO5, `DioMapping1/2` registers | DIO1–DIO3; **DIO2 = RF switch, DIO3 = TCXO by convention** | DIO5–DIO11 | **DIO5–DIO11, all fully general** |
| RF-switch control | host GPIO | `SetDio2AsRfSwitchCtrl` — 1 pin, 2 states | `SetDioAsRfSwitch` | **`SetDioRfSwitchConfig`, any DIO, 5 states** (`tx_hf`,`rx_hf`,`tx_lf`,`rx_lf`,`standby`) |
| TCXO | host-supplied | **`SetDio3AsTcxoCtrl`** — steals a DIO | `SetTcxoMode` | **`SetTcxoMode` → dedicated `VTCXO` pin** |
| Reference | XTAL or TCXO | XTAL or TCXO | XTAL or TCXO | XTAL, TCXO, **or XTAL + on-chip NTC temperature compensation** |
| Antenna-switch states needed | 2 | 2 | 4 (dual band) | 4 (dual band), **driven by the chip** |
| Mandatory boot blob | ❌ | ❌ | ⚠ **firmware image, updatable** (`AN1200.57 LR11xx Program Memory Update`) | ✅ **PRAM patch, re-uploaded every cold start** |
| Errata handling | datasheet notes | **4 register pokes** (`DS.SX1261-2` §15) | driver-applied | **PRAM + named workaround functions**, some needing retention-memory parking |

---

## 3. What breaks, generation by generation

### 3.1 Gen 1 → Gen 2: total register-model change

The canonical break, and the one everyone has heard about.

- **Register-mapped becomes command-based.** On an SX1276 you write `RegOpMode`; on an SX1262 you
  issue `SetStandby(0x80)`. No address, no constant, no initialisation sequence survives.
- **`BUSY` appears and is mandatory.** An SX127x driver has no concept of it. Ignore it on an
  SX126x and you get silent command loss — the single most common Gen-2 bring-up failure, covered
  at length in [`guides/lora` §5.2](../lora/README.md).
- **`DIO2`/`DIO3` acquire hidden meanings.** `SetDio2AsRfSwitchCtrl` and `SetDio3AsTcxoCtrl` turn
  two "GPIOs" into a switch driver and a regulator. Nothing analogous exists on Gen 1.
- **`XOSC_START_ERR` is expected at power-on with a TCXO** and must not be treated as fatal.
- **SF6 is not interoperable**, and SF5 arrives (Gen 2 only). **[DS20]** §23.8
- **Intra-packet frequency hopping disappears.** A Gen-1 feature Gen 2 simply does not have.
- Four **mandatory register workarounds** appear (`DS.SX1261-2` §15) with no Gen-1 equivalent.

**Driver reality:** RadioLib keeps `SX127x` and `SX126x` as entirely separate modules; Semtech ships
separate `sx126x_driver`; nothing is shared. **[RL]**

### 3.2 Gen 2 → Gen 3: same shape, different command set

The gentlest step, and the only one Semtech advertises as compatible.

- The LR1110/1120/1121 product pages all claim ***"Fully compatible with SX1261/2/8 devices and the
  LoRaWAN standard"*** **[PP]** — read that as **air-interface and LoRaWAN-profile** compatibility.
  It is **not** a claim of pin or register compatibility, and the parts are not pin-compatible
  (QFN32 5 × 5 vs QFN24 4 × 4).
- **The command set is different.** RadioLib has a separate `LR11x0` module; Semtech ships `SWDR001`
  as a separate driver from `sx126x_driver`. **[RL]**
- **A firmware image enters the picture.** LR11xx carries updatable program memory —
  `AN1200.57 LR11xx Program Memory Update` and the `SWTL001` "reference implementation of the LR11xx
  firmware update procedure" exist for exactly this. A Gen-2 driver has no such concept.
- **Long interleaver arrives** (Gen 3 and 4 only) — a LoRa PHY option a Gen-2 peer cannot decode.
  **[DS20]** §23.8
- **Package and pinout change**: QFN32 5 × 5, and the GNSS/Wi-Fi parts need an extra antenna path.

**What you gain:** GNSS + Wi-Fi passive scanning (LR1110/LR1120), 2.4 GHz and satellite bands
(LR1120/LR1121), and an **AES-128 crypto engine with secure key storage and DevEUI/JoinEUI/NwkKey/AppKey
handling** — a genuine security-architecture change, not a checkbox.

### 3.3 Gen 3/2 → Gen 4: the second big break

**Verdict up front: SX126x → LR2021 is a break of the same magnitude as SX127x → SX126x, and
migrating from Gen 3 is only slightly easier than from Gen 2.** The command *model* survives; its
encoding, addressing, buffering and initialisation do not.

Here is what your driver has to change, concretely. Sourced from **[DS20]** §5–§7, §22 and **[DRV]**.

| # | Change | What you rewrite |
|---|---|---|
| 1 | **Opcodes go 8-bit → 16-bit** | Every opcode constant; the framing helper; the unit tests. `MOSI` is now `Op(15:8), Op(7:0), Arg0…` |
| 2 | **Every command returns 6 status bytes**, not 1: `Stat(15:8), Stat(7:0), IrqStat(31:24)…IrqStat(7:0)` | Read helpers, offsets, and the "did that work?" path. Upside: you get IRQ state free with every transaction |
| 3 | **Registers: 16-bit addr / 8-bit data → 24-bit addr / 32-bit data** (`WriteRegMem32 0x0104`, `ReadRegMem32 0x0106`, `WriteRegMemMask32 0x0105`) | The entire register layer, and every constant in it. Nothing ports |
| 4 | **One shared 256 B buffer → two independent 256 B FIFOs** with high/low thresholds, level readback, explicit clear and overflow/underflow flags | The whole payload path. ⚠ And it is a **capability change**: >256 B payloads are now supported by streaming, which Gen 2 could not do at all |
| 5 | **A second IRQ domain.** `ConfigFifoIrq`/`GetFifoIrqFlags`/`ClearFifoIrqFlags` are separate from `SetDioIrqConfig`/`ClearIrq`/`GetAndClearIrqStatus` | Your ISR. A "one IRQ register" model is now wrong |
| 6 | **`SetDio2AsRfSwitchCtrl` → `SetDioRfSwitchConfig(Dio, tx_hf, rx_hf, tx_lf, rx_lf, standby)`** | Antenna-switch handling. A dual-band front end needs four states; the chip drives them, but you must describe them |
| 7 | **`SetDio3AsTcxoCtrl` → `SetTcxoMode` on the dedicated `VTCXO` pin** | Clock bring-up, and one DIO handed back to you |
| 8 | **⚠ A firmware Patch RAM (PRAM) must be uploaded at every cold start** and after every sleep-without-retention. Per-part images (`lr20xx_pram_load_pram_lr2021` vs `…_lr20x2`). Costs +80 nA retention current | **A new mandatory boot stage with no Gen-2 equivalent.** Skip it and the part *appears* to work while BLE Coded PHY, RTToF and sub-GHz SIMO sensitivity are all degraded |
| 9 | **⚠ Retention-memory parking.** SX1276 compatibility mode, SX1276 hopping compatibility and the RTToF deviation fix are **lost across sleep-with-retention** unless explicitly stored in a retention slot | Your sleep/wake path. A brand-new bug class |
| 10 | **SIMO supply topology.** `VDCC1`→`VDCC2` and `VPAX1`→`VPAX2` are **external PCB connections**; the buck feeds the PA as well as the core | **The board, not just the driver.** Also a new trade: Semtech's own driver docs say SIMO **costs sub-GHz sensitivity** for LoRa, FSK, FLRC, OOK and Z-Wave **[DRV]** |
| 11 | **⚠ `SetPaConfig` can damage the part.** **[DS20]** §7.4.1 lists "PA damage" and "Regulatory non-compliance" among the consequences of wrong parameters; `pa_hf_duty_cycle` is restricted to 16–31 "to avoid risk of aging" | Take PA tables from `lr20xx_pa_pwr_cfg.h`, not from arithmetic. ⚠ The CN 490 MHz variant needs a **different** table from 868/915 **[DRV]** |
| 12 | **DIO Rx/Tx hardware triggers**, where **`BUSY` is not raised** | Any `BUSY`-polling state machine written for Gen 2 reads this state wrong |
| 13 | **No AES engine, no secure key store** (if coming from Gen 3) | Move LoRaWAN key handling to the MCU or an external secure element |
| 14 | **`LoRaMac-node` has no Gen-4 support** and has not been pushed since 2024-07-03 | If that is your LoRaWAN stack, you are changing stack as well as driver — to LoRa Basics Modem / USP |

**Corroboration from two independent implementations**, which is the strongest evidence that this
is a real break rather than a documentation style change:

- **Semtech** ships `lr20xx_driver` as a **new tree**, not a shim over `sx126x_driver` **[DRV]**.
- **RadioLib** created a **new base class** for the LR2021 — commit
  `d696fed842bc77c6699ac83d9611a7d6e1c838d6`, *"[LRxxxx] Create base class for common LR11xx and
  LR20xx commands"*, 2025-10-13 **[RL]**. Note what it shares with: **LR11xx**, not SX126x.
- **Meshtastic** likewise added `LR20x0Interface` *"based on the LR11x0 and LR1110"* — PR #10401
  body, 2026-05-06 **[MT]**.

**All three chose Gen 3 as the ancestor. None of them could reuse Gen 2.**

### 3.4 The reassuring half: the air interface is compatible

**[DS20]** §23.8:

> LoRa radios across the different generations can communicate with each other when properly
> configured with identical parameters (frequency, spreading factor, bandwidth, and coding rate).
> … Note that **all the LoRaWAN configurations are fully compatible between all four generations**.

The exceptions, in full:

| Feature | Gen 1 | Gen 2 | Gen 3 | Gen 4 | Practical effect |
|---|:--:|:--:|:--:|:--:|---|
| **SF5** | ❌ | ✅ | ✅ | ✅ | An SF5 network excludes Gen 1 |
| **SF6** | ⚠ | ⚠ | ⚠ | ⚠ | *"requires additional configuration for backwards compatibility"*. Gen 4 has `SetLoraSF6Compat` and driver `lr20xx_workarounds_lora_*_sx1276_compatibility_mode` |
| **Long interleaver** | ❌ | ❌ | ✅ | ✅ | Gen 3/4 only; invisible to Gen 1/2 peers |
| **Intra-packet hopping** | ✅ | ❌ | ❌ | ✅ | Skipped two generations and came back |
| **Multi-SF CAD / Fast CAD** | ❌ | ❌ | ❌ | ✅ | Receiver-side; does not break peers |
| **Convolutional CR8/CR9** | ❌ | ❌ | ❌ | ✅ | Gen-4-only coding rates — turning these on splits your mesh |

**So an LR2021 drops into an existing SX1262 Meshtastic or LoRaWAN network and works — provided you
do not enable anything that makes it worth having.** That is the central tension of this migration,
and it is worth saying out loud before anyone budgets for it.

---

## 4. Generation notes

### 4.1 Gen 1 — SX1272/SX1276 (2013)

Two sub-families, and **they are not the same silicon**: SX1272/73 cover **860–1020 MHz** with a
157 dB link budget and −137 dBm sensitivity; SX1276/77/78/79 cover **137–1020 MHz** with a 168 dB
budget and −148 dBm. **[PP]** Register-mapped, QFN28, no `BUSY`, `+20 dBm` PA, RX 9.9 mA (SX1276) /
10 mA (SX1272), packet engine to 256 bytes, 61 Hz synthesiser resolution, built-in temperature
sensor and low-battery indicator. Both are still orderable and both still ship in vast quantity as
`RFM95`-class modules. Record: [`components/semtech/sx1276`](../../components/semtech/sx1276/README.md).

### 4.2 Gen 2 — SX1261/62/68, LLCC68, SX1280 (2017–2018)

The generation every board in this knowledge base actually has. The step change is **receive
current**: 9.9 mA → **4.6 mA**, achieved with an integrated DC-DC. ⚠ **That DC-DC does not help
transmit on an SX1262** — its PA is fed from `VBAT`, which is exactly the constraint the LR2021's
SIMO removes ([SX1262 record](../../components/semtech/sx1262/README.md) and §5.2 below).

Within the generation, four parts that are easy to confuse and are documented separately here:
[SX1262](../../components/semtech/sx1262/README.md) (+22 dBm, 150–960 MHz),
[SX1268](../../components/semtech/sx1268/README.md) (+22 dBm, **410–810 MHz** for Chinese bands),
[LLCC68](../../components/semtech/llcc68/README.md) (**restricted SF/BW combinations** — a genuine
substitution trap), and SX1261 (+15 dBm, PA from `VREG`, DC-DC covers the whole IC).
**SX1280/SX1281** sit in the same generation at 2.4 GHz with FLRC and a ranging engine.

### 4.3 Gen 3 — LoRa Edge, LR1110/LR1120/LR1121 (2020–)

Semtech's own summary is *"Added geolocation"*, and the family is best understood as three points on
a scanner spectrum. **[PP]**

| | **LR1110** | **LR1120** | **LR1121** |
|---|---|---|---|
| Sub-GHz 150–960 MHz | ✅ | ✅ | ✅ |
| 2.4 GHz ISM | ❌ | ✅ | ✅ |
| Satellite bands | ❌ | 1.9–2.1 GHz S-band | **2 GHz S-band + 1.55 GHz L-band** |
| **GNSS (GPS/BeiDou) scanning** | ✅ | ✅ | ❌ |
| **Wi-Fi passive AP-MAC scanning** | ✅ | ✅ | ❌ |
| **AES-128 crypto + key store** | ✅ | ✅ | ✅ |
| Synthesiser range | **150–2700 MHz continuous** | — | — |
| Semtech catalogue family | LoRa Edge | LoRa Edge | **LoRa Connect** |
| Order code | `LR1110IMLTRT` | `LR1120IMLRT` ⚠ | `LR1121IMLTRT` |

⚠ **`LR1120IMLRT` on Semtech's own page is missing the `T`** that `LR1110IMLTRT` and `LR1121IMLTRT`
both carry. Almost certainly a typo on the product page, but **do not order from this table** —
confirm against the datasheet or the distributor. Recorded because it is exactly the kind of thing
that gets copied. **[PP]**, `unresolved`.

The crypto engine is the under-appreciated part: hardware AES-128, DevEUI/JoinEUI handling, and
storage of `NwkKey`/`AppKey` "against unauthorized access". **Gen 4 drops all of it.** If you chose
Gen 3 for that, Gen 4 is a step backwards and you should say so in your migration paperwork.
Records: [`lr1121`](../../components/semtech/lr1121/README.md),
[`lr11x0`](../../components/semtech/lr11x0/README.md).

### 4.4 Gen 4 — LoRa Plus, LR2021/LR2022/LR2012 (2025–)

Full dossier: [`components/semtech/lr2021`](../../components/semtech/lr2021/README.md). The
three-part split, since one datasheet covers all three and mixing them up is the standard error:

| | **LR2021** | **LR2022** | **LR2012** |
|---|---|---|---|
| Sub-GHz + HF (1.5–2.5 GHz) | ✅ + ✅ | ✅ + ✅ | ✅ + ❌ (`RFI_HF`/`RFO_HF` are NC) |
| FLRC · O-QPSK · Z-Wave | ✅ | ❌ | ❌ |
| Bluetooth LE PHY | ✅ | ✅ | ❌ |
| LoRa · LR-FHSS · (G)FSK · OOK · BPSK · WM-Bus · Wi-SUN | ✅ | ✅ | ✅ |

⚠ **No LR2022 or LR2012 silicon, module or firmware was found in the wild** as of 2026-09-04.
Every product located — Waveshare `Core2021`, Seeed `Wio-LR2021`, NiceRF `LoRa2021F33-2G4`, Seeed
MeshTracker X1, Meshnology W12 — uses the **LR2021**. Negative result.

---

## 5. Three cross-generation themes worth understanding

### 5.1 The reference clock, and how the TCXO requirement melted away

| Gen | Situation |
|---|---|
| 1 | XTAL is fine for most work; sensitivity is high but frequency tolerance is the designer's problem |
| 2 | ⚠ TCXO effectively required at high SF, and it is bolted on by **stealing `DIO3` as its power supply**. `XOSC_START_ERR` at power-on is normal and must be ignored |
| 3 | `SetTcxoMode`; the DIO-stealing hack is gone |
| 4 | **`VTCXO` is a dedicated pin.** More importantly: *"Increased frequency offset tolerance obviating TCXO and large thermal relief"* **[PP]**, plus an **on-chip NTC temperature-compensation path** that measures crystal temperature and corrects for it — explicitly aimed at PA self-heating on small boards **[DS20]** §1.9.2 |

**This is a real BOM and power win, not marketing.** A TCXO is a part, a footprint, and 1.5–4 mA
whenever the radio is awake. Gen 4 lets a well-designed board delete it — and a community poster
planning a TDMA schedule was already relying on it in mid-2026: *"You can rely on the crystal
oscillator of the LR2021, which should be less than ±30 ppm, which can also be improved with the API
`set_xosc_trim`"* **[COM]**.

⚠ Meshtastic's Gen-4 variants still carry `LR2021_DIO3_TCXO_VOLTAGE` **[MT]** — a constant name
inherited from RadioLib's SX126x API. It does **not** mean DIO3 supplies the TCXO on this part.

### 5.2 Transmit efficiency is a supply-topology story

| Gen | Regulator | PA supply | Tx @ max |
|---|---|---|---|
| 1 | LDO only | `VBAT` | ~120 mA @ +20 dBm |
| 2 (SX1262) | LDO **or** DC-DC | ⚠ **`VBAT` — the DC-DC covers the core only** | **118 mA @ +22 dBm** |
| 2 (SX1261) | LDO or DC-DC | `VREG` — DC-DC covers the whole IC | 25.5 mA @ +14 dBm |
| 4 (LR2021) | **SIMO buck** or LDO | **`VPAX` from the SIMO** | **105 mA @ +22 dBm** |

**~11 % less transmit current at the same output power, from supply topology alone.** For a
duty-cycled node whose energy budget is dominated by transmit bursts, that is the most directly
useful number in this whole guide.

⚠ **But SIMO is not free.** Semtech's own driver documentation says the SIMO converter *"may
negatively impact RF sensitivity for sub-GHz operations"* for FSK, FLRC, OOK, LoRa **and** Z-Wave
**[DRV]**, and **[DS20]** §23.1–23.2 adds a further degradation for SIMO under a metallic RF shield.
The datasheet's electrical tables are specified *"no shield, SIMO"*. **The current-versus-sensitivity
trade is a live design decision on Gen 4 in a way it was not on Gen 2.**

### 5.3 Security went backwards

| Gen | AES-128 engine | Secure key storage | DevEUI/JoinEUI handling |
|---|:--:|:--:|:--:|
| 1 | ❌ | ❌ | ❌ |
| 2 | ❌ | ❌ | ❌ |
| **3** | **✅** | **✅** | **✅** |
| **4** | **❌** | **❌** | **❌** |

Evidence for the Gen-4 row is a **negative result and worth stating as such**: the string `AES` does
not appear anywhere in the 243-page **[DS20]**; there is no crypto section in the table of contents;
and the only crypto-adjacent sentence is a *warning* that `GetRandomNumber` *"should not be used for
cryptographic purposes"* (§6.6.2). Independently, Waveshare's own `Core2021` vs `Core1121`
comparison table marks AES-128 and secure key storage as present on the LR1121 and absent on the
LR2021 **[3P]**.

**If your LoRaWAN root keys currently live in an LR11xx, Gen 4 has nowhere to put them.** Plan for
MCU-side storage or an external secure element, and price that in.

---

## 6. Software support across the lineage

| Stack | Gen 1 | Gen 2 | Gen 3 | Gen 4 | Note |
|---|:--:|:--:|:--:|:--:|---|
| **RadioLib** (MIT) | ✅ `SX127x` | ✅ `SX126x`, `LLCC68`, `SX128x`, `STM32WLx` | ✅ `LR11x0` | ✅ **`LR2021`, from release 7.6.0 (2026-02-19)** | Four separate modules; the LR2021 shares a base class with LR11x0 |
| **Semtech driver** | in `LoRaMac-node` | `sx126x_driver`, `llcc68_driver` (BSD-3-Clause-Clear) | `SWDR001` | ⚠ **no standalone repo** — `lr20xx_driver` lives inside `LoRa-Net/usp` | Every other generation has a standalone driver |
| **LoRa Basics Modem** (`SWL2001`) | ❌ | ✅ | ✅ | ✅ bundled as 4.9.0 inside USP | The current LoRaWAN path |
| **USP** (Unified Software Platform) | ❌ | ✅ "buildable" | ✅ "buildable" | ✅ **"validated"** | ⚠ *"not intended for production use"* at v1.1.2 |
| **LoRaMac-node** | ✅ | ✅ | ✅ | ❌ | ⚠ **last push 2024-07-03**; predates Gen 4 |
| **Meshtastic** | ✅ `RF95_RADIO` | ✅ `SX1262/1268/LLCC68/SX1280`, `STM32WLx` | ✅ `LR1110/1120/1121` | ✅ `LR2021_RADIO` — **2.8.x only, not in v2.7.26** | `LoRaRadioType` enum, read 2026-09-04 |
| **Zephyr** | — | ✅ | ✅ | ✅ via `usp_zephyr` | Not evaluated here |
| **Linux kernel** | ❌ | ❌ | ❌ | ❌ | **No in-tree driver for any Semtech LoRa transceiver.** Everything is userspace SPI (USP on Linux, Meshtastic Portduino). Negative result, 2026-09-04 |

**The single most useful software fact for a migration plan:** RadioLib 7.5.0 (2026-01-10) has
nothing; **7.6.0 (2026-02-19) is the floor**. And Meshtastic's stable 2.7 line has nothing —
LR2021 is a 2.8 feature.

---

## 7. Dating the generations — and where the dates are soft

| Gen | Date | Evidence strength |
|---|---|---|
| **1** | **2013** | **Strong.** **[DS20]** §23.8 states it; independently, the earliest Wayback capture of `semtech.com/images/datasheet/sx1272.pdf` is **2013-05-10** and of `sx1276.pdf` **2013-05-01** **[WB]** |
| **2** | SX1280 **2017**, SX1261/62 **2018** | ⚠ **Moderate.** Semtech gives no date in §23.8. Earliest Wayback captures: `sx1280-1.pdf` **2017-03-29**, `DS_SX1261-2_V1.1.pdf` **2019-01-08** **[WB]**. A first-capture date is a *latest-possible* introduction date, not the announcement. `inferred` |
| **3** | LR1110 **2020** | ⚠ **Weak in this pass.** No Semtech-dated source was retrieved; no LR11xx PDF exists in the Wayback index for `semtech.com`. **Not established here** — treat "2020" as the commonly-repeated figure, `unresolved` |
| **4** | Announced **2025-03-12**; datasheet Rev 0.2 **June 2025**; Rev 1.1 **Oct 2025**; Rev 2.1 **Apr 2026**; Rev 2.2 **2026-08-08** | **Strong.** The revision history is in **[DS20]**; the announcement date is fixed by the official Meshtastic account's post **[COM]** and by RadioLib issue #1457, opened **2025-03-13** — the next day |

⚠ **Gen 2 and Gen 3 introduction dates are the weakest claims in this guide.** They are marked
`inferred`/`unresolved` rather than dressed up. What would settle them: a Semtech press release, or
a datasheet Rev 1.0 with a printed date — neither of which was obtainable through the document gate
described in [`vendors/semtech/README.md`](../../vendors/semtech/README.md).

---

## 8. Which generation should you actually use?

| Situation | Choose | Why |
|---|---|---|
| **New plain sub-GHz LoRa or LoRaWAN node, cost matters** | **Gen 2 — SX1262** | Mature, cheap, ubiquitous, best-documented part in this library. Gen 4 buys you nothing if you only run stock LoRa |
| **433 MHz or Chinese 470 MHz** | Gen 2 — **SX1268** | 410–810 MHz |
| **High volume, restricted SF/BW acceptable** | Gen 2 — **LLCC68** | ⚠ Read the [substitution trap](../../components/semtech/llcc68/README.md) first |
| **2.4 GHz only, FLRC, bulk transfer** | Gen 2 — **SX1280** | Cheaper and far better supported than Gen 4 for this specific job — a recommendation made repeatedly by experienced posters **[COM]** |
| **Asset tracking, "where is it" beats "how far"** | Gen 3 — **LR1110/LR1120** | GNSS + Wi-Fi scanning. Nothing in Gen 4 replaces this |
| **LoRaWAN with keys that must not leave the radio** | Gen 3 — **LR1121** | The crypto engine and key store. **Gen 4 has neither** |
| **Dual-band single-SKU, one antenna path, no external RF switch** | **Gen 4 — LR2021** | The multi-region front end is the actual BOM argument |
| **You need >125 kbps over ISM** | **Gen 4 — LR2021** (or Gen 2 SX1280 at 2.4 GHz) | FLRC. ⚠ Expect ~50 % of nominal after framing and FEC **[COM]** |
| **Mesh efficiency: asymmetric links, better CAD** | **Gen 4 — LR2021** | Multi-SF receive is the standout, and is Gen-4-only |
| **Deleting the TCXO matters** | **Gen 4** | §5.1 |
| **A PHY the SX126x cannot make at all** — Z-Wave, BLE, 802.15.4, Sigfox BPSK | **Gen 4** | Dedicated packet handlers, ⚠ third-party stacks required |
| **Interoperating with an existing Gen-1 deployment** | Gen 1 — **SX127x** | Or Gen 4 with its SX1276 compatibility modes, which is now a genuine third option |

**And the honest caution.** Gen 4 is ~18 months old. Its reference driver says *"not intended for
production use"*; RadioLib support is ~7 months old and was still receiving datasheet-conformance
fixes in August 2026; Meshtastic support is not in a stable release; and **no independent,
method-stated sensitivity or range comparison against an SX1262 exists anywhere this pass could
find** ([community survey](../../components/semtech/lr2021/projects-and-community.md)). Every
performance advantage claimed above is a Semtech specification. That is not a reason to avoid the
part — it is a reason to prototype before committing a BOM.

---

## 9. Sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| G-1 | LR2021/LR2022/LR2012 Datasheet | Semtech, via Digi-Key | authorized mirror | datasheet | [`components/semtech/lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf`](../../components/semtech/lr2021/artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf) | 2026-09-04 | **`DS.LR20xx` Rev 2.1, 13/04/26** | **§0 — the generation list (§23.8)**; §2, §3.3, §5 |
| G-2 | LR2021 Datasheet Rev 1.1 | Semtech, via Mouser | authorized mirror | datasheet | [archived](../../components/semtech/lr2021/artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf.ARCHIVED.md) | 2026-09-04 | `DS.LR2021` Rev 1.1, 10/14/25 | §0 — independent corroboration of §23.8 |
| G-3 | SX1276/77/78/79 Datasheet | Semtech, via Wayback | credible mirror | datasheet | [`components/semtech/sx1276/artifacts/sx1276-77-78-79-datasheet-v5-wayback.pdf`](../../components/semtech/sx1276/artifacts/sx1276-77-78-79-datasheet-v5-wayback.pdf) | 2026-09-04 | **Rev. 5, August 2016** | §2, §4.1 |
| G-4 | Product pages: LR2021, LR1121, LR1110, LR1120, SX1276, SX1272, SX1262, SX1268, LLCC68, SX1280 | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/{lora-plus,lora-connect,lora-edge}/…` | 2026-09-04 | undated | §1, §2, §4 |
| G-5 | Product sitemap | Semtech | primary | sitemap | `www.semtech.com/sitemap-products.xml` | 2026-09-04 | — | §1 — the only complete family enumeration |
| G-6 | `lr20xx_driver` v2.0.2 in `LoRa-Net/usp` | Semtech | primary | source | @ `512a095e303872f900021361a619b7b1e6e29469`; [snapshot](../../components/semtech/lr2021/artifacts/usp-lr20xx_driver-v2.0.2-512a095.tar.gz) | 2026-09-04 | driver v2.0.2, 2026-04-07; BSD-3-Clause-Clear | §3.3, §5.2, §6 |
| G-7 | RadioLib | jgromes | community | source | `github.com/jgromes/RadioLib` | 2026-09-04 | LR2021 first in **7.6.0**, 2026-02-19 | §3.1, §3.3, §6 |
| G-8 | Meshtastic firmware | Meshtastic | community | source | `github.com/meshtastic/firmware` | 2026-09-04 | PR #10401 merged 2026-05-08 | §3.3, §5.1, §6 |
| G-9 | `Core2021-XF` product page and comparison table | Waveshare | primary | store listing | `www.waveshare.com/Core2021-XF.htm` | 2026-09-04 | — | §0, §5.3 |
| G-10 | Wayback CDX index for `semtech.com` PDFs (6 000 rows) | Internet Archive | archive | index | `web.archive.org/cdx/search/cdx?url=semtech.com/*&matchType=domain&filter=mimetype:application/pdf` | 2026-09-04 | captures 2011–2019 | §7 — **and a negative result: zero LR11xx or LR20xx PDFs are indexed under `semtech.com`** |
| G-11 | Community corpus | various | community | forum | catalogued in [`lr2021/projects-and-community.md`](../../components/semtech/lr2021/projects-and-community.md) | 2026-09-04 | 2025-03-12 … 2026-09-02 | §7 announcement date; §8 caution |
| G-12 | SX1262 component record | this repository | derived | record | [`components/semtech/sx1262/README.md`](../../components/semtech/sx1262/README.md) | 2026-09-04 | — | Gen-2 rows in §2 and §5.2 |
