# Semtech LR2021 — LoRa Plus™, the fourth-generation LoRa transceiver

> **Cross-cutting guide:** [`guides/hardware/lora-radio-generations.md`](../../../guides/hardware/lora-radio-generations.md)
> — the four generations side by side, and what breaks when you move between them.
> **Domain guide:** [`guides/lora`](../../../guides/lora/README.md) — LoRa vs LoRaWAN vs Meshtastic,
> airtime/duty-cycle arithmetic, band plans as a legal constraint. This record covers the part.

- **Category:** multi-band, multi-PHY **LoRa / LR-FHSS / FLRC / (G)FSK / OOK / BPSK / O-QPSK / BLE-PHY / Z-Wave** transceiver, SPI-controlled
- **Bands:** **150–960 MHz** *and* **1.5–2.5 GHz** (2.4 GHz ISM plus licensed L/S-band) **[DS]**
- **Package:** **QFN 32, 5 × 5 mm**, Pb-free/halogen-free, RoHS/WEEE **[DS]**
- **Order code:** `LR2021IMLTRT` · tape & reel · MOQ 3 000 **[DS]**
- **Family:** first silicon in Semtech's **LoRa Plus™** line, alongside `LR2022` and `LR2012` (§1.2)
- **Research status:** **Rev 2.1 of the datasheet is retained and was read** (`DS.LR20xx`, 243 pp). **Rev 1.1 is also retained**, archived, because the two differ in substance (§14). The chip has never been seen or measured here — every electrical figure below is a manufacturer specification.
- **Retrieved:** 2026-09-04

**This is the part the phrase "the new 4th gen LoRa chip" refers to, and the label is Semtech's
own, not community shorthand.** Two independent primary sources say so in as many words — see §1.1.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | `artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf` — `DS.LR20xx`, Final Datasheet **Rev. 2.1**, `13/04/26`, 243 pp, with section/table reference | `not-tested` — manufacturer specification reproduced, nothing measured |
| **[DS1.1]** | The superseded `DS.LR2021` **Rev. 1.1**, `10/14/25`, 236 pp — [archived](artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf.ARCHIVED.md) | `not-tested`; cited only where the two revisions disagree |
| **[DRV]** | Semtech's own `lr20xx_driver` **v2.0.2** inside `LoRa-Net/usp` @ `512a095e303872f900021361a619b7b1e6e29469`, retained as `artifacts/usp-lr20xx_driver-v2.0.2-512a095.tar.gz` | `executed-success` for the read; `not-tested` on hardware |
| **[RL]** | RadioLib source read live through the GitHub API at a named tag/commit | `executed-success` for the read; `inferred` for behaviour |
| **[MT]** | Meshtastic firmware source/PR read live through the GitHub API | `executed-success` for the read |
| **[DOC]** | `www.semtech.com` / vendor product page, retrieved 2026-09-04 | `not-tested` |
| **[COM]** | Community report — always labelled firsthand-measurement / firsthand-ownership / informed-interpretation / hearsay in [`projects-and-community.md`](projects-and-community.md) | non-authoritative |
| **[INF]** | Inference | `inferred` |

**Nothing in this record was verified on hardware by this pass.** No opcode, register, pin or
current figure below was guessed; each is transcribed from a cited document or source file.

**Text-layer validation.** `pypdf` extraction of Rev 2.1 was checked against the document's own
running footer (`LR2021/LR2022/LR2012 · Final Datasheet Rev. 2.1 · DS.LR20xx 13/04/26 · N of 243`)
on every quoted page, and against the page count reported by the PDF page tree (243). ⚠ **The
micro sign is dropped by the extractor** — sleep currents render as bare `A` where the document
says `µA`, and PA ramp times as `s` where the document says `µs`. Both are corrected below from
context and from the front-page summary (`470nA` sleep). ⚠ **Figures are vector art with no text
layer at all**, so the pin-out diagram, the SIMO/LDO connection drawings and the package marking
drawing extract as bare pin-name word lists or as nothing. Values taken from figures are marked.

---

## 1. Identity and capability

### 1.1 "Fourth generation" is Semtech's word — the evidence

The user-facing question this record exists to answer is *what is the 4th generation LoRa chip*.
Three primary sources, two of them inside the datasheet itself:

| # | Source | Exact wording |
|---|---|---|
| 1 | Datasheet **front page**, feature block **[DS]** p. 1 | **"Generation 4 LoRa® IP"** |
| 2 | Datasheet **General Description** **[DS]** p. 2 | "The LR2021 is Semtech's **first chip in the LoRa Plus family**. Incorporating a **fourth-generation LoRa IP** …" |
| 3 | Semtech product page `<title>` **[DOC]** | "LoRa Plus™ LR2021 \| **Fourth-generation LoRa® IP** for Fast Long Range Communication (FLRC) \| Semtech" |

And the numbering is not left implicit. **[DS]** **§23.8 "Compatibility of Generation 1-4 LoRa
Radios"** enumerates the whole lineage verbatim:

> Semtech has developed four generations of LoRa radios:
> • Generation 1 (Gen 1): SX1272, SX1276 - First LoRa chips (2013)
> • Generation 2 (Gen 2): SX1261, SX1262, SX1280 - Enhanced performance and efficiency
> • Generation 3 (Gen 3): LR1110, LR1120, LR1121 - LoRa Edge™ - Added geolocation
> • Generation 4 (Gen 4): LR2021 LoRa Plus™ Multi-band, and multi-protocol

The same list, word for word, appears in **[DS1.1]** §23.7 — so it is **corroborated across two
independent document revisions six months apart**, not a one-off editorial line.

Four consequences worth stating plainly, because each rules something out:

- **SX1280/SX1281 (2.4 GHz LoRa) is Gen 2, not a generation of its own.** Semtech puts it in the
  same bullet as the SX1261/SX1262. The 2.4 GHz band is a band, not a generation.
- **LR-FHSS is not a generation either.** It is a modulation, available on SX126x (Gen 2), LR11xx
  (Gen 3) and LR20xx (Gen 4) alike — the patent notice in **[DS]** p. 3 lists
  `SX1261, SX1262, SX1268, LR1110, LR1120, LR1121, LR2012, LR2021, LR2022` as the parts whose
  purchase conveys LR-FHSS patent rights, which is the clearest available statement of which
  silicon carries it.
- **SX1268 and LLCC68 are not named** in §23.8. They are SX1262 siblings and inherit Gen 2 by
  family, not by enumeration — see [`components/semtech/sx1268`](../sx1268/README.md) and
  [`components/semtech/llcc68`](../llcc68/README.md). **[INF]**
- **SX1277/78/79 and SX1273 are not named either**, for the same reason: §23.8 names one
  representative per generation, not a full part list.

⚠ **The LR2022 and LR2012 are also Gen 4 silicon** and §23.8 does not mention them, because §23.8
was written for Rev 1.1 when the LR2021 was the only member. Read it as a generation list, not a
part list. **[INF]**

### 1.2 Three parts, one datasheet, and the differences are exclusions

`DS.LR20xx` Rev 2.1 documents **LR2021, LR2022 and LR2012 together**, and warns explicitly that
"product features unavailable in the LR2022 and LR2012 are described in this document but are not
available in the corresponding IC" **[DS]** p. 2. That is the same trap as the SX1261/SX1262
datasheet — *a claim copied from the wrong part is the most common error made with this document.*

| | **LR2021** | **LR2022** | **LR2012** |
|---|---|---|---|
| Order code **[DS]** | `LR2021IMLTRT` | `LR2022IMLTRT` | `LR2012IMLTRT` |
| Sub-GHz 150–960 MHz | ✅ | ✅ | ✅ |
| 1.5–2.5 GHz (HF path) | ✅ | ✅ | ❌ — `RFI_HF`/`RFO_HF` are **NC** |
| LoRa, LR-FHSS, (G)FSK, OOK, BPSK, WM-Bus, Wi-SUN | ✅ | ✅ | ✅ |
| **FLRC** | ✅ | ❌ | ❌ |
| **O-QPSK (802.15.4 / Thread / Zigbee)** | ✅ | ❌ | ❌ |
| **Z-Wave / Z-Wave LR** | ✅ | ❌ | ❌ |
| **Bluetooth LE PHY** | ✅ | ✅ | ❌ |
| Semtech's one-line summary **[DS]** | Full feature set, dual band | "Same as LR2021, excluding support for FLRC, O-QPSK (802.15.4), and Z-Wave" | "Sub-GHz only, excluding support for FLRC, O-QPSK (802.15.4), Bluetooth LE, and Z-Wave" |

**Everything below describes the LR2021** unless a row says otherwise. `LR20xx` marks a statement
that holds for all three; the datasheet uses that convention in its own section headings and this
record follows it.

### 1.3 What it actually is

A single-SKU, switch-less-front-end, dual-band software-defined radio that happens to speak LoRa.
**[DS]** p. 1–2 and **[DOC]**:

- **Modulations:** LoRa (SF5–SF12), LR-FHSS, (G)FSK, GMSK/MSK, OOK, (D)BPSK, O-QPSK DSSS, FLRC,
  Bluetooth LE PHY (1M/2M/Coded 500k/125k)
- **Protocol PHY compatibility** claimed with third-party stacks: LoRaWAN, **Amazon Sidewalk**,
  **Sigfox** BPSK, **Wi-SUN** FSK, **Wireless M-Bus** (device *and* collector), **Z-Wave / Z-Wave LR**,
  **802.15.4 Thread/Zigbee**, Bluetooth LE 5.0 PHY
- **Terrestrial and NTN/SATCOM**, the latter in the licensed L/S-band — this is what the
  "1.5–2.5 GHz" figure is for, and it is the headline reason the part exists
- **RTToF (round-trip time-of-flight) ranging engine** — §10, inherited in spirit from the SX1280
- **Dedicated packet handlers per PHY** in hardware, not a generic FIFO with host-side framing

Semtech's positioning line, **[DOC]**: *"multi-region, single-SKU design, reducing external BOM
costs, PCB footprint, and power consumption, while offering superior performance compared to
previous LoRa transceivers."* Take "single-SKU" literally — the multi-region front end and the
absence of an external RF switch are the actual BOM argument, not marketing filler (§5.3).

⚠ **The chip's band coverage is not a board's band coverage.** 150–960 MHz continuous is a
synthesiser capability; every real module narrows it with a matching network and antenna. The
Waveshare `Core2021` ships as **three separate SKUs** (`-LF`, `-HF`, `-XF`) for exactly this
reason **[DOC]**.

---

## 2. Pin table

QFN32 + exposed pad. Transcribed from **[DS]** Table 2-1 (a real table, not the figure).

| Pin | LR2021 / LR2022 | LR2012 | Description |
|---:|---|---|---|
| 0 | `GND` | `GND` | Exposed ground pad |
| 1 | `VR_PA` | `VR_PA` | Regulated supply for all power amplifiers |
| 2 | `VPAX2` | `VPAX2` | Regulated supply for the PA regulator |
| 3 | `NTC` | `NTC` | NTC thermistor connection (XTAL temperature compensation, §6.2) |
| 4 | `XTA` | `XTA` | 32 MHz crystal — **also the external-reference / TCXO input** |
| 5 | `XTB` | `XTB` | 32 MHz crystal; **leave unconnected when a TCXO is used** |
| 6 | `VTCXO`/`VNTC` | `VTCXO`/`VNTC` | Regulated TCXO supply **or** NTC supply — one pin, two jobs |
| 7–11 | `DIO11`…`DIO7` | idem | Multi-purpose digital I/O |
| 12 | `VDCC1` | `VDCC1` | SIMO converter output — **must be wired externally to `VDCC2`** |
| 13 | `VPAX1` | `VPAX1` | SIMO converter output for PA supply — **wire externally to `VPAX2`** |
| 14 | `LXB` | `LXB` | SIMO coil |
| 15 | `GND_DCC` | `GND_DCC` | SIMO ground |
| 16 | `LXA` | `LXA` | SIMO coil |
| 17 | `VBAT` | `VBAT` | Main battery supply |
| 18–19 | `DIO6`, `DIO5` | idem | Multi-purpose digital I/O |
| 20 | `NRESET` | `NRESET` | Reset, active low |
| 21–24 | `MISO`, `MOSI`, `SCK`, `NSS` | idem | SPI |
| 25 | `BUSY` | `BUSY` | Busy indicator |
| 26 | `VDCC2` | `VDCC2` | Regulated supply input |
| 27–28 | `RFO_LF2`, `RFO_LF1` | idem | LF PA outputs — **two of them** |
| 29 | `RFI_LF` | `RFI_LF` | LF receiver input |
| 30 | `GND` | `GND` | Ground |
| 31 | `RFI_HF` | **NC** | HF receiver input |
| 32 | `RFO_HF` | **NC** | HF PA output |

Three things a driver author should notice immediately:

1. **There are seven DIOs (`DIO5`–`DIO11`) and none of them is special.** Unlike the SX126x —
   where `DIO2` means RF-switch and `DIO3` means TCXO-supply by hard convention — every function
   here is assigned at run time by `SetDioFunction` / `SetDioRfSwitchConfig` / `SetDioIrqConfig`
   (§4.3). Do not carry an SX126x pin habit across.
2. **`VDCC1`→`VDCC2` and `VPAX1`→`VPAX2` are external connections you must make on the PCB.**
   The SIMO converter's outputs leave the package and come back in. Miss one and the part does not
   run. **[DS]** §1.8.4.
3. **The TCXO goes to `XTA`, not to a DIO**, and its supply comes from the dedicated `VTCXO` pin
   (§6.2). The SX126x trick of stealing `DIO3` for TCXO power is gone, and so is the class of bug
   that came with it.

---

## 3. The command interface — and why your SX126x driver will not survive

This is the section that answers "what breaks". The LR2021 is **not** an evolution of the SX126x
host interface. It is a different interface that happens to keep the same four wires plus `BUSY`.

### 3.1 What carried over

- **SPI mode 0** (CPOL = CPHA = 0), subordinate only, transaction framed by `NSS` falling/rising,
  MISO high-Z while `NSS` is high. **[DS]** §3.7.2
- **`BUSY` is still a mandatory handshake**, still asserted on the falling edge of `NSS`, still
  released when the command has been processed and the chip has reached a stable mode. **[DS]** §5.2
- Max **SCK 16 MHz**, `tCP` ≥ 61.50 ns, `tSLCH` ≥ 31.25 ns at 10 pF load. **[DS]** Table 3-27
- A `Sleep` / `Standby RC` / `Standby XOSC` / `FS` / `Rx` / `Tx` mode ladder. **[DS]** §4.4

### 3.2 What changed, item by item

| | **SX126x (Gen 2)** | **LR2021 (Gen 4)** | Consequence for a driver |
|---|---|---|---|
| **Opcode width** | **8 bits** | **16 bits** — `Op(15:8)`, `Op(7:0)` **[DS]** §5.4.1.1 | Every opcode constant, every command-framing helper, every unit test. Total rewrite of the transport layer |
| **Status returned on MISO** | 1 status byte | **16 status bits followed by the full 32-bit `IrqStatus`**, on *every* command **[DS]** §5.4.1.1 | You get IRQ state free with each transaction. Also: your read helpers must skip 6 bytes, not 1 |
| **IRQ width** | 16-bit `IrqStatus` | **32-bit** **[DS]** §5.6.3 (`ClearIrq irqs_to_clear(31:0)`) | Bitmask type changes; masks do not port |
| **Register address width** | 16-bit, byte-wide access | **24-bit address, 32-bit data** — `WriteRegMem32 0x0104 Addr(23:0) Data[1:64]`, `ReadRegMem32 0x0106`, plus a read-modify-write `WriteRegMemMask32 0x0105` **[DS]** Table 5-2 | The whole register map is a different address space with different granularity. No SX126x register constant is meaningful |
| **Data buffer** | **one** 256-byte buffer, shared, positioned with `SetBufferBaseAddress` | **two independent 256-byte FIFOs**, `ReadRadioRxFifo 0x0001` / `WriteRadioTxFifo 0x0002`, with programmable high/low thresholds, level readback (`GetRxFifoLevel`/`GetTxFifoLevel`), explicit clear, and `FifoEmpty/Full/Overflow/Underflow` flags **[DS]** §5.3 | ⚠ **This is a capability change, not just an API change.** Payloads > 256 B are supported by *streaming* — refill Tx / drain Rx mid-packet against the threshold IRQs. The SX126x could not do that at all |
| **RF switch control** | `SetDio2AsRfSwitchCtrl` — one pin, on or off | `SetDioRfSwitchConfig 0x0113` with **five independent state masks**: `tx_hf, rx_hf, tx_lf, rx_lf, standby`, on **any** DIO **[DS]** §6.8.2 | Genuinely more capable: a dual-band front end needs four states, and the chip drives them itself |
| **TCXO** | `SetDio3AsTcxoCtrl` — repurposes a DIO | `SetTcxoMode 0x0120 tune(7:0) start_time(31:0)` driving the **dedicated `VTCXO` pin** **[DS]** §6.11.3 | Cleaner, and one fewer DIO consumed |
| **Errata handling** | Four register pokes you apply yourself | **A firmware Patch RAM (PRAM) image you upload at every cold start** (§7.1) | ⚠ **New mandatory boot step with no Gen-2 equivalent** |
| **Direct FIFO access** | — | `ReadRadioRxFifo`/`WriteRadioTxFifo` complete **within a single SPI frame** rather than needing a second frame **[DS]** §5.4.1.3–5.4.1.4 | Faster, but a different transaction shape your HAL must expose (`lr20xx_hal_direct_read`, `lr20xx_hal_direct_read_fifo` **[DRV]**) |
| **DIO as Rx/Tx trigger** | — | A DIO can *start* an Rx or Tx sequence in hardware; ⚠ **`BUSY` is not raised** for the trigger **[DS]** §5.5 | New capability, and a `BUSY`-polling loop written for Gen 2 will read this state wrong |

**Verdict.** SX127x → SX126x was a total register-model change: register-mapped to command-based.
**SX126x → LR2021 is a second break of the same magnitude**, in the opposite direction from
"gentle": the command model survives conceptually but nothing about its encoding, addressing,
buffering or initialisation is portable. Semtech's own driver reflects this — `lr20xx_driver` is a
new tree, not a `#define` layer over `sx126x_driver` **[DRV]**. So does RadioLib: `LR2021` is a new
module under a **new `LRxxxx` base class** created to share what the LR11xx and LR20xx have in
common — `d696fed842bc77c6699ac83d9611a7d6e1c838d6`, *"[LRxxxx] Create base class for common LR11xx
and LR20xx commands"*, 2025-10-13 **[RL]**. Note what that says: the common ancestor is **LR11xx**,
not SX126x.

**What does survive is the air interface**, and that is the point — see §8.

---

## 4. Modems and packet engine

### 4.1 LoRa

| Parameter | Value | Source |
|---|---|---|
| Spreading factor | **SF5 – SF12** | **[DS]** Table 3-9 |
| Bandwidth | **7.825 – 1000 kHz** (434 MHz–2.5 GHz); **7.825 – 500 kHz** (150–433 MHz) | **[DS]** Table 3-9 |
| Bit rate | 45.8 bps (SF12/31.25 kHz/CR4:8) … **125 kbps** (SF5/1000 kHz/CR4:5) | **[DS]** Table 3-9 |
| Coding rate | 4/5…4/8 **plus new convolutional CR8/CR9** | **[DS]** §9.1.3, §23.8 |
| Sync word, address filter, hopping | `SetLoraSyncword`, `SetLoraAddress`, `SetLoraHopping` | **[DS]** §9.9 |

Four LoRa features are **new in Gen 4** and have no Gen-2/Gen-3 counterpart **[DS]** §9.3–9.7, §23.8:

- **Multi-SF detection** — receive several spreading factors *simultaneously*. For a mesh this is
  the single most consequential item on the list: it lets the two legs of an asymmetric link run
  at different SFs.
- **Multi-SF CAD** and **Fast CAD**. §9.4 notes that CAD on previous generations "uses a fixed
  peak-to-noise ratio threshold across all symbols"; Gen 4 does not.
- **Extended LoRa Rx bandwidth** (§9.7).
- **Convolutional CR8/CR9**.

And two are **compatibility shims** pointing straight back at Gen 1:

- **§9.8 Intra-packet frequency hopping compatibility with SX127x.** Hopping existed in Gen 1,
  vanished in Gens 2–3, and returns in Gen 4 — §23.8: *"Intra-packet hopping is available in
  generations 1 and 4."*
- **§9.9.2 SF6 compatibility with SX127x.** SF6 has been an interoperability trap across the whole
  lineage; here it is an explicit mode.

### 4.2 The other modems

| Modem | Headline | Parts |
|---|---|---|
| **FLRC** | up to **2.6 Mbps**; the flagship new PHY, and the reason the marketing title says "Fast Long Range Communication" | LR2021 only |
| **LR-FHSS** | 488 bps raw; **for SATCOM and sub-GHz** | LR20xx |
| **(G)FSK / GMSK** | 3.4 kHz – 2666 kHz channel BW; modulation index 0.3–8.3 | LR20xx |
| **OOK** | 1.2–32.768 kbps Tx, up to **2 Mbps** Rx | LR20xx |
| **(D)BPSK** | 0.1–0.6 kbps, **Tx only** — this is the Sigfox uplink | LR20xx |
| **O-QPSK DSSS** | 250 kbps @2.4 GHz, 100 kbps sub-GHz — 802.15.4 | LR2021 only |
| **Bluetooth LE PHY** | 1M / 2M / Coded 500k / Coded 125k | LR2021, LR2022 |
| **Z-Wave / Z-Wave LR** | dedicated packet handler with HomeID and beam filtering, and a `SetZwaveScan` engine | LR2021 only |
| **WM-Bus** | S/T/C/R/N modes, **device *and* collector** | LR20xx |
| **Wi-SUN FSK** | modes 1a…4b | LR20xx |

⚠ **A PHY is not a stack.** Semtech is careful, and so should you be: BLE, Zigbee/Thread, Z-Wave,
Wi-SUN and Sidewalk work *"when integrated with third-party stack offerings"* **[DOC]**. The chip
gives you the radio and the packet handler. It does not give you a qualified Bluetooth product —
**[DS]** p. 3 says so explicitly: *"Semtech's products are designed to be used in connection with
qualified Bluetooth products and applications but are **not** certified or qualified Bluetooth
products."*

### 4.3 Interrupts and DIO assignment

Three orthogonal commands, all taking an explicit `Dio(7:0)` argument **[DS]** §6.8:

```
SetDioFunction        0x0112   Dio(7:0), Func(3:0), pull_drive(3:0)
SetDioRfSwitchConfig  0x0113   Dio(7:0), tx_hf, rx_hf, tx_lf, rx_lf, standby
SetDioIrqConfig       0x0115   Dio(7:0), Irq(31:0)
```

Plus a **second, separate IRQ domain for the FIFOs** — `ConfigFifoIrq 0x011A` with independent
enable masks and four thresholds (`rx_high`, `rx_low`, `tx_high`, `tx_low`), read back through
`GetFifoIrqFlags 0x011B` and cleared through `ClearFifoIrqFlags 0x0114`. A driver that models
"the IRQ register" as one 32-bit word will miss half the machine.

---

## 5. RF front end, power and performance

### 5.1 Two PAs, and a front end designed to avoid an external switch

**[DS]** §1.5, §7.4, Table 3-22:

| | **LF PA** (150–960 MHz) | **HF PA** (1.5–2.5 GHz, LR2021/22) |
|---|---|---|
| Max Tx power | **+22 dBm** typ (min 19) | **+12 dBm** typ |
| Power range | 63 steps of **0.5 dB** (≈32 dB dynamic) | 63 steps of 0.5 dB |
| Step accuracy | ±2 dB | ±2 dB |
| OCP trip | **164 mA** | **55 mA** |
| Ramp time | 2 µs … 340 µs, programmable | idem |
| Outputs | **`RFO_LF1` *and* `RFO_LF2`** — two branches run in phase in the default "Full single-ended mode" | `RFO_HF` |

⚠ **`SetPaConfig` is dangerous to guess at.** **[DS]** §7.4.1 states that non-optimised PA
parameters may cause *"Incorrect output power / Excessive current consumption / **PA damage** /
Regulatory non-compliance"*, and that `pa_hf_duty_cycle` accepts **only 16–31** "to avoid risk of
aging the power amplifier". The datasheet's advice for any board that is not the reference design
is to contact Semtech applications support. Take the PA tables from `lr20xx_pa_pwr_cfg.h` **[DRV]**
rather than inventing them. ⚠ Semtech's own USP README adds that the **China 490 MHz `Wio-LR20xx`
variant needs a different PA table** from the 868/915 boards **[DRV]**.

### 5.2 Current

**[DS]** Tables 3-4 to 3-7. `VBAT = 3.3 V`, 25 °C, **no shield, SIMO** — Rev 2.1 explicitly
clarified those conditions, and §23.2 warns that a metallic RF shield over a SIMO design costs
sensitivity.

| Mode | Typ | Note |
|---|---:|---|
| Sleep, no retention, no RTC | **470 nA** | front-page figure; Table 3-4 `IDDSL0`/`IDDSL1` group spans 0.47–1.4 µA depending on retention and RTC. ⚠ **The `µ` is lost by text extraction and the five-row/five-column alignment in Table 3-4 did not survive it — read the PDF before quoting a specific retention variant** |
| Sleep + PRAM loaded | **+80 nA** on top | **[DS]** §22.3 — the patch image costs retention current |
| `STDBY_RC` | 1.21 mA | HFRC 32 MHz on |
| `STDBY_XOSC` | 1.79 mA | |
| Synthesiser (FS) | 3.0 mA | @915 MHz |
| **Rx, LoRa SF7/125 kHz sub-GHz** | **5.7 mA** | `IDDRXLFL4` |
| Rx, LoRa SF7/125 kHz @2.4 GHz | 6.4 mA | `IDDRXHFL4` |
| Rx boosted, LF path | **+1.2 mA** | `IDDDELTA1` |
| Rx, FLRC 260 kbps / 2.6 Mbps | 6.6 / 10.4 mA | |
| **Tx +22 dBm, 868/915 MHz** | **105 mA** | `IDDTXLF1` |
| Tx +20 / +17 / +14 / +10 dBm | 72 / 43 / **27** / 17 mA | |
| Tx +10 dBm via HF PA with dedicated matching | **12 mA** | `IDDTXLF8` — a genuinely unusual option |
| Tx +22 dBm, 434/490 MHz | 100 mA | |
| Tx +12 dBm @2.4 GHz | 23 mA | `IDDTXHF` |

**The receive figure is the headline.** 5.7 mA against the SX1262's 4.6 mA (DC-DC) / 9.7 mA (LDO)
is not a dramatic win on its own — but the SX1262 only reaches 4.6 mA with its DC-DC enabled, and
its DC-DC **cannot help the PA at all** because the SX1262's PA is fed from `VBAT`. The LR2021's
**SIMO converter supplies both the core rail (`VDCC`, ~1.55 V, ≤20 mA) and the PA rail (`VPAX`)**
**[DS]** §1.8.4. That is why +22 dBm costs **105 mA here versus 118 mA on an SX1262** — a ~11 %
transmit-energy reduction that comes from supply topology, not from the PA.

⚠ **SIMO is not free.** Semtech's own driver documentation states that *"Usage of DCDC regulator
(a.k.a. SIMO converter) may negatively impact RF sensitivity for sub-GHz operations"* for FSK,
FLRC, OOK, LoRa **and** Z-Wave **[DRV]**. LDO mode exists for "noise sensitive, low-cost or small
size applications" **[DS]** §1.8.4, selected with `SetRegMode 0x0109`. **The current-versus-sensitivity
trade is a real design decision on this part, and the datasheet's electrical numbers are the SIMO
column.**

### 5.3 Sensitivity — LoRa sub-GHz, 64 B payload, CR 4/5

**[DS]** Table 3-17. Typical values, dBm.

| BW ↓ / SF → | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **62 kHz** | — | −126.5 | −129 | −132 | −135 | −137.5 | −140.5 | **−143** |
| **125 kHz** | — | −125 | −127.5 | −130.5 | −133 | −136 | −138.5 | **−141.5** |
| **250 kHz** | −119 | −122 | −124.5 | −127.5 | −130 | −133 | −135.5 | −138.5 |
| **400 kHz** | −117 | −120 | −122.5 | −125.5 | −128.5 | −130.5 | −134 | −136.5 |
| **500 kHz** | −116 | −119 | −122 | −124.5 | −127.5 | −130 | −133 | −135.5 |
| **800 kHz** | −113 | −115.5 | −118 | −121 | −124 | −126.5 | −130 | −132 |
| **1000 kHz** | −112.5 | −115.5 | −118 | −120 | −123 | −126 | −129 | −131 |

(SF5 at 62/125 kHz is present in the document; the value did not survive the text extraction on
those two rows and is left blank rather than guessed. **[DS]** Table 3-17 sheets 3–4.)

**−141.5 dBm at SF12/125 kHz is the marketed number** and is genuinely ~1 dB better than the
SX1262's −140.6 dBm at the same setting. The larger practical gain is elsewhere: **multi-SF
reception**, **improved CAD**, and **increased frequency-offset tolerance** — the last of which
Semtech markets as *"obviating TCXO and large thermal relief"* **[DOC]**, i.e. the ability to run
SF12 on a **plain crystal**. On Gen 2 that generally needed a TCXO, and a TCXO is both a BOM line
and a standing sleep-current cost.

Other PHYs, front-page typicals **[DS]**: FLRC sub-GHz −111 dBm @260 kbps, −104.5 @0.975 Mbps,
**−100.5 @1.95 Mbps** (⚠ **[DS1.1]** said **−101.5** — see §14); BLE −100 dBm @1 Mbps, −97 @2 Mbps;
O-QPSK −103 dBm @250 kbps 2.4 GHz, −111 dBm @100 kbps sub-GHz.

---

## 6. Clocks, reset and start-up

### 6.1 Reset and boot

**[DS]** §4.2–4.3: `BUSY` stays **high** through reset and through the boot calibration sequence,
falling only when the device reaches `STDBY_RC` and can accept commands. Same contract as Gen 2;
the timing is different and the PRAM upload (§7.1) is bolted on after it.

### 6.2 Crystal, TCXO, or neither

Three reference options, and this is one of the areas where Gen 4 is materially cheaper to build:

- **32 MHz XTAL** on `XTA`/`XTB`. The default, and — thanks to the wider frequency-offset
  tolerance — the *intended* choice for most designs.
- **32 MHz TCXO** on `XTA` with `XTB` unconnected, powered from the dedicated **`VTCXO`** pin whose
  regulated voltage is programmed by `SetTcxoMode`. `ILTCXO` 1.5–4 mA; `ATCXO` 0.4/0.6/1.2 V p-p
  clipped sine, AC-coupled through 10 pF in series with 220 Ω. **[DS]** §1.9.3, Table 3-25
- **XTAL + NTC temperature compensation.** A resistor and NTC hung off `VTCXO` and `NTC` let the
  chip measure crystal temperature and compensate the induced frequency shift on-chip
  (`SetNtcParams`, `SetTempCompCfg`). **[DS]** §1.9.2, §6.12. Semtech calls this out as
  *"particularly useful when high power PA is desired on a small PCB footprint"* — i.e. it exists
  to fix the self-heating pull that a +22 dBm PA inflicts on a nearby crystal. **There is no Gen-2
  equivalent.**
- **External 32 kHz LF reference** can be injected on `DIO11` via `ConfigLfClock`, for synchronous
  protocols that need accurate wake timing. **[DS]** §1.9.4

Clock output: any of `DIO5`–`DIO11` can emit the HF clock, divided by any power of two from 32 MHz
down to 976.562 kHz (`ConfigClkOutputs`); `DIO7`–`DIO11` can emit the 32 kHz LF clock, available
even in sleep. **[DS]** §1.9.5

---

## 7. Known limitations, workarounds and the PRAM

### 7.1 ⚠ The Patch RAM is the biggest single migration surprise

**[DS]** §22.3 and **[DRV]**:

- The LR20xx ships with a **firmware patch image (PRAM)** that the host **uploads over SPI**.
- *"While not strictly required, using the chip without the PRAM can create performance issues and
  unexpected bugs. The use of the PRAM is therefore **highly recommended**."*
- **It is lost on reset and on cold start.** It survives sleep-with-retention.
- It costs **+80 nA** of retention sleep current while loaded.
- Two images exist: `lr20xx_pram_load_pram_lr2021` and `lr20xx_pram_load_pram_lr20x2`. **They are
  per-part.** **[DRV]** `inc/lr20xx_pram_lr2021.h`, `inc/lr20xx_pram_lr20x2.h`
- Version-checkable at run time: `lr20xx_patch_get_version`, `lr20xx_patch_enable_pram`. **[DRV]**

There is no SX126x analogue. On Gen 2 you applied four register pokes; on Gen 4 you ship a binary
blob and load it every cold boot. A driver that does not do this will *appear* to work.

### 7.2 What the PRAM fixes — Semtech's own list **[DRV]**

Bluetooth LE Coded PHY access-address failures · BLE Coded PHY frequency drift degrading
sensitivity · wrong default preamble length for BLE 2M · degraded BLE Coded PHY blocking
performance · RTToF PLL frequency-step bias when the RF frequency is not a multiple of **122 Hz**
· incorrect RTToF RSSI · RTToF extended mode hanging for seconds · **SIMO impact on sub-GHz
sensitivity for FSK, FLRC, OOK, LoRa and Z-Wave**.

### 7.3 Workarounds that are *not* in the PRAM — you call these yourself **[DRV]**, **[DS]** §22

| Workaround function | What it is for |
|---|---|
| `lr20xx_workarounds_lora_enable_sx1276_compatibility_mode` | **Gen-1 LoRa interop.** ⚠ Not retained across sleep unless you also call `…_store_retention_mem` |
| `lr20xx_workarounds_lora_freq_hop_enable_sx1276_compatibility_mode` | SX1276-compatible **intra-packet hopping**; must be called *after* `lr20xx_radio_lora_set_freq_hop` |
| `lr20xx_workarounds_ook_set_detection_threshold_level` | **[DS]** §22.1 — the automatic OOK RSSI threshold is too conservative; measure the noise floor with `GetRssiInst` and override |
| `lr20xx_workarounds_rttof_results_deviation` | **[DS]** §22.2 — RTToF standard deviation on the SX1280-compatible "fractional" bandwidths 101/203/406/812 kHz. Reverted by the next `set_modulation_params`; needs `…_store_retention_mem` to survive sleep |

⚠ **The retention-memory pattern is a new class of bug.** Several workarounds touch registers that
are *not* preserved by sleep-with-retention unless explicitly parked in a retention slot. A node
that sleeps between packets will silently lose its SX1276 compatibility mode, or its RTToF fix,
unless the driver stores it. This has no Gen-2 equivalent and is easy to miss.

---

## 8. Interoperability with older generations — what actually still talks

**[DS]** §23.8, and this is the reassuring half of the migration story:

> LoRa radios across the different generations can communicate with each other when properly
> configured with identical parameters (frequency, spreading factor, bandwidth, and coding rate).
> … Note that **all the LoRaWAN configurations are fully compatible between all four generations**.

The exceptions, all from §23.8:

| Feature | Gen 1 | Gen 2 | Gen 3 | Gen 4 |
|---|:--:|:--:|:--:|:--:|
| **SF5** | ❌ | ✅ | ✅ | ✅ |
| **SF6** | ⚠ needs a compatibility mode across the boundary | ⚠ | ⚠ | ⚠ `SetLoraSF6Compat` / §9.9.2 |
| **Long interleaver** | ❌ | ❌ | ✅ | ✅ |
| **Intra-packet hopping** | ✅ | ❌ | ❌ | ✅ |
| **Multi-SF CAD, Fast CAD** | ❌ | ❌ | ❌ | ✅ |
| **Convolutional CR8/CR9** | ❌ | ❌ | ❌ | ✅ |

So: an LR2021 node drops into an existing SX1262 Meshtastic or LoRaWAN mesh and works, provided you
do not turn on the new toys. The new toys are exactly what makes the part worth having, and every
one of them is a mesh-splitting decision.

---

## 9. Drivers, SDKs and software support

| Option | Where | Verdict |
|---|---|---|
| **Semtech `lr20xx_driver`** (inside **USP**) | `github.com/LoRa-Net/usp`, driver **v2.0.2**, repo @ `512a095e303872f900021361a619b7b1e6e29469`, release `v1.1.2-feature-202604` (2026-04-16) · **BSD-3-Clause-Clear** | **The reference implementation.** ⚠ There is **no standalone `lr2021_driver` repository** — unlike `sx126x_driver`, `llcc68_driver`, `lr1110_driver` and `SWDR001`, the Gen-4 driver ships only inside USP |
| **RadioLib** | `github.com/jgromes/RadioLib`, `src/modules/LR2021` — **first shipped in release 7.6.0, 2026-02-19** | **Use this for Arduino/PlatformIO work.** 15 files, ~250 KB of source. Details in [`projects-and-community.md`](projects-and-community.md) |
| **Meshtastic** | `LR2021Interface` + `LR20x0Interface`, merged 2026-05-08 (PR #10401) | Supported on the **2.8.x** line; **not** in v2.7.26. Details in [`projects-and-community.md`](projects-and-community.md) |
| **Zephyr** | `github.com/LoRa-Net/usp_zephyr` — "Zephyr RTOS integration of Semtech's USP … Compatible with LR20xx, SX126x and LR11xx" | Exists; not evaluated here |
| **LoRaMac-node** | `github.com/LoRa-Net/LoRaMac-node` — last push **2024-07-03** | ⚠ **Predates the part.** The Gen-4 LoRaWAN path is USP/LoRa Basics Modem, not LoRaMac-node |
| **Linux** | USP builds for "Linux (x86/x86_64 native + ARM cross-compilation for Raspberry Pi, embedded Linux)"; ⚠ **"Linux porting was only tested with LR2021"** **[DRV]**. Meshtastic's Portduino also has an LR2021 path (PR #11252, merged 2026-07-30) **[MT]** | Userspace SPI. **No in-tree Linux kernel driver was found** for any Semtech LoRa transceiver, Gen 4 included — `not-tested`, negative result |
| Raw SPI | — | Feasible — §3 is the whole interface — but §7's PRAM upload and retention-memory workarounds are exactly what a hand-rolled driver omits |

### 9.1 ⚠ USP is explicitly pre-production

Its own README, at the pinned commit **[DRV]**:

> **USP RELEASE v1.1.2 - Experimental Feature Release**
> ⚠ **Warning**: This preview release is not intended for production use. A stable release will be
> available soon

It bundles **LoRa Basics Modem 4.9.0**. Validation status is unusually candid and worth reproducing:

| Target | Status |
|---|---|
| LoRa Plus EVK (LoRa Plus Expansion Board + Wio-LR2021/LR2022/LR2012) on **STM32L476RG** | **Validated** — "passed the Semtech nominal validation process" |
| LR11xx shield radios · SX126x shield radios | **Buildable** — compiles, no full validation |
| Linux (x86/x86_64/ARM) | Buildable; **tested only with LR2021** |
| Renesas FPB-RA0E2, STM32L073RZ | **Experimental** — one sample application, US915 Class A |

The architectural claim in the repo description is the one that matters strategically: USP is
*"MCU FW SW driving LR20xx multi-PHY radios with multiprotocol operations and radio resource
arbitration … **Backward-compatible with SX126x and LR11xx radio devices**."* Semtech's answer to
the three-driver problem is one abstraction over all three generations — but that abstraction is
new, pre-production, and does not retrofit onto anything already shipped.

---

## 10. Caveats, gaps and errata

| # | Issue | Evidence |
|---|---|---|
| **G1** | ⚠ **Semtech's current datasheet revision could not be obtained.** The product page lists **"LR2021/22/12 Datasheet v2.2, 2026-08-08"**; the newest copy retained here is **Rev 2.1 (13/04/26)**. The canonical link is a Salesforce JS shell that yields no bytes to any non-browser client. **So this record may be one revision behind, and that is `unresolved`, not "no lag"** | `executed-failed` 2026-09-04; [`vendors/semtech/README.md` §4](../../../vendors/semtech/README.md) |
| **G2** | **Two retained revisions disagree on a published number.** FLRC sub-GHz @1.95 Mbps: **−101.5 dBm** in Rev 1.1, **−100.5 dBm** in Rev 2.1. Both are kept; Rev 2.1 is authoritative | **[DS]** vs **[DS1.1]** front pages |
| **G3** | ⚠ **No AES engine, no secure key store, no DevEUI/JoinEUI management.** The word `AES` does not appear in the 243-page datasheet; the only crypto-adjacent line is a warning that `GetRandomNumber` *"should not be used for cryptographic purposes"* (§6.6.2). **This is a regression against Gen 3** — the LR11xx has a crypto engine and secure key storage. Independently asserted by Waveshare's own `Core2021` vs `Core1121` comparison table | **[DS]** §6.6.2 (negative result, whole-document search); **[DOC]** Waveshare |
| **G4** | **The package marking is a figure with no text layer.** **[DS]** §24.2 Figure 24-2 exists but extracts as nothing, so **this record cannot tell you what is printed on the lid**. Neither can it give the package outline or land pattern dimensions (§24.1, §24.3) | **[DS]** — explicit gap; open the PDF |
| **G5** | **Nothing here was measured.** No range, throughput, sensitivity, current or battery figure in this record was reproduced by anyone whose method could be inspected. The only firsthand numbers located anywhere are community bench reports, catalogued and labelled in [`projects-and-community.md`](projects-and-community.md) | negative result |
| **G6** | ⚠ **PA configuration can damage the part.** **[DS]** §7.4.1 lists "PA damage" among the consequences of non-optimised `SetPaConfig` parameters, and restricts `pa_hf_duty_cycle` to 16–31 "to avoid risk of aging". Any board that is not the reference design needs Semtech applications support or a vetted PA table | **[DS]** §7.4.1 |
| **G7** | **SIMO costs sensitivity.** Semtech's driver docs list LoRa, FSK, FLRC, OOK and Z-Wave sub-GHz sensitivity as degraded by the SIMO converter, and §23.1/§23.2 add a further degradation for SIMO under a metallic RF shield. The datasheet's electrical tables are specified "no shield, SIMO" | **[DRV]**; **[DS]** §23.1–23.2 |
| **G8** | ⚠ **Retention-memory workarounds silently revert.** SX1276 compatibility mode, SX1276 hopping compatibility and the RTToF deviation fix are all lost across sleep-with-retention unless explicitly stored in a retention slot | **[DRV]** driver README |
| **G9** | **The PRAM is mandatory in practice and optional in wording.** "Not strictly required … therefore highly recommended" is the datasheet's phrasing for a patch that fixes BLE Coded PHY, RTToF and SIMO sensitivity. Treat it as mandatory | **[DS]** §22.3 |
| **G10** | ⚠ **`LR2021` ≠ `LR20xx`.** FLRC, O-QPSK and Z-Wave are LR2021-only; BLE is LR2021/22-only; the whole HF path is absent on LR2012. The single-datasheet-many-parts trap that bites SX1261-vs-SX1262 readers bites harder here, because there are three parts | **[DS]** p. 2 |
| **G11** | **No standalone driver repository.** `lr20xx_driver` exists only inside the 47 MB `usp` monorepo, whose own README says it is not for production. Compare `sx126x_driver`, `llcc68_driver`, `lr1110_driver`, `SWDR001` — all standalone | **[DRV]**, GitHub org listing |
| **G12** | **`LoRaMac-node` has not been touched since 2024-07-03** and has no LR20xx support. Anyone whose LoRaWAN stack is LoRaMac-node has no Gen-4 path without switching to LoRa Basics Modem / USP | GitHub API, 2026-09-04 |
| **G13** | **LR-FHSS remains patent-encumbered.** **[DS]** p. 3 grants no patent rights with the software; rights come *"by purchasing Semtech SX1261, SX1262, SX1268, LR1110, LR1120, LR1121, LR2012, LR2021 or LR2022 semiconductor devices, or their authorized counterparts"* | **[DS]** p. 3 |
| **G14** | **Every page is stamped "Semtech Proprietary & Confidential"** — on a document freely mirrored by two distributors. Redistribution status is recorded `unknown` and the artifacts are unstaged pending review (§14) | **[DS]** running footer |
| **G15** | **No LR2022 or LR2012 hardware was found in the wild.** Every module, board and firmware located — Waveshare `Core2021`, Seeed `Wio-LR2021`, NiceRF `LoRa2021F33-2G4`, SenseCAP MeshTracker X1, Meshnology W12 — uses the **LR2021**. ⚠ **The LR2012 is nonetheless a real, documented product**: Semtech's document catalogue lists `LR2012EVK1XBS1`/`XCS1`/`XGS1` production folders and LR2012 reference designs for EU868, US915 and CN490, all dated **2026-08-18**, and there is an `LR2012` product page with its own EVK SKUs. **The LR2022 has neither an EVK nor a reference design in the catalogue** — it appears only as a column in the datasheet and in the `LR2021EVK2*` kit names. Semtech's own driver ships a separate `lr20xx_pram_load_pram_lr20x2` patch image, so the `x2` parts are real silicon to the driver | negative result for hardware; **[DOC]** catalogue + **[DRV]**, 2026-09-04 |

---

## 11. Lifecycle, sourcing, pricing and availability

**Timeline** (dates are evidenced; see [`projects-and-community.md`](projects-and-community.md) for the community half):

| Date | Event | Evidence |
|---|---|---|
| **2025-03-12** | Announced. Meshtastic's own account posts *"Semtech announced their 4th gen #LoRa chip!"* linking the LR2021 product page, and notes Semtech named Meshtastic specifically | **[COM]** r/meshtastic `1j9xjw6`, 82 pts |
| **2025-06** | Datasheet **Rev 0.2**, "Preliminary release" | **[DS]** revision history |
| **2025-06-09** | RadioLib `[LR2021] Initial WIP commit` `2472fbdf727e7263167bdc511f2bd0744194dd33` | **[RL]** |
| **2025-10** | Datasheet **Rev 1.1**, "Final datasheet" (`DS.LR2021`, 10/14/25) | **[DS1.1]** |
| **2025-10-14** | `LoRa-Net/usp` repository created | GitHub API |
| **2025-12-16** | USP **v1.0.0** | GitHub API |
| **2026-02-19** | **RadioLib 7.6.0** — first release shipping LR2021 support | **[RL]** |
| **2026-04** | Datasheet **Rev 2.1** — expanded to cover LR2022 and LR2012 (`DS.LR20xx`) | **[DS]** |
| **2026-05-08** | **Meshtastic** merges LR2021 support (PR #10401) | **[MT]** |
| **2026-07-23** | Seeed SenseCAP **MeshTracker X1** pre-orders open — first mass-market Meshtastic product with the part | **[COM]** r/meshtastic `1v49g4p`, 170 pts |
| **2026-08-08** | Datasheet **v2.2** per Semtech's listing — ⚠ not obtained (G1) | **[DOC]** |
| **2026-08-25** | LR2021 **ETSI** and **FCC prescan** radio test reports published (ZIP) | **[DOC]** |

**Lifecycle status: active, in volume, ~18 months after announcement.** Not sampling; there are
shipping consumer products.

### 11.1 What you can buy, and what it costs

| Item | Vendor | Price / date | Note |
|---|---|---|---|
| **`LR2021EVK2XBS1`** (EU 868 + 2.4 GHz) · **`LR2021EVK2XCS1`** (NA 915 + 2.4 GHz) · **`LR2021EVK2XGS1`** (CN/Asia 490 + 2.4 GHz) | Semtech | list price not published on the product page — ⚠ the "Unit Price (USD)" widget renders as `$0` without JavaScript **[DOC]** | Each kit contains **2 × RF boards** (`LR2021RF2XDS1`, or `…XGS1` for the 490 MHz kit) |
| `LR2021EVK1XGS1` | Semtech | — | Earlier EVK1 generation; still listed |
| **LR2021 LoRa Plus Evaluation Kit, 915 MHz US, V2.0** | **Seeed Studio** | **US$99.00**, 2026-09-04 | ⚠ **Two complete nodes**, so ≈$50/node: nRF54L15 + Wio-LR2021 + OLED + 2 SMA antennas + cable **[COM]** |
| **`Core2021-LF` / `-HF` / `-XF`** module | **Waveshare** | **US$11.99 / US$12.99**, 2026-09-04 | Bare LR2021 module, three band SKUs. Waveshare's own page calls it *"the fourth-generation LoRa multi-band transceiver LR2021"* |
| **`LoRa2021F33-2G4`** 1 W module | **NiceRF** | not retrieved — `www.nicerf.com` returned **HTTP 403** to both the Chrome and WhatsApp agents, 2026-09-04 | LR2021 + external PA, ~+30 dBm. Community bench-tested (see `projects-and-community.md`) |
| **SenseCAP MeshTracker X1** | Seeed | pre-order opened 2026-07-23; price not captured this pass | Meshtastic variant `seeed_mesh_tracker_X1` upstream **[MT]** |
| LilyGo **T-Display P4 LR2021** | LilyGo | listed then unavailable on AliExpress, "Release on May 20" 2026 | **[COM]** hearsay, r/meshtastic `1tcb7ni` |

⚠ **Distributor stock could not be checked.** The Semtech page's Digi-Key-powered inventory widget
is JavaScript-only and renders empty to `curl`; `www.mouser.com/c/?q=` returns a 13 895-byte
"Access Denied" page to every agent tried. **`unresolved`**, 2026-09-04.

### 11.2 Reference designs and certification — available, unusually

Semtech publishes, all gated behind the Salesforce shell (§14, G1):

- **`LR202x` reference design files** for **CN490**, **EU868** and **US915**, each covering
  sub-GHz *and* 2.4 GHz, 2026-08-18, ZIP
- **LR2021 ETSI Radio Test Report** and **LR2021 FCC Prescan Radio Test Report**, both 2026-08-25, ZIP
- `AN1200.112 - SubGHz FLRC Regulatory Measurement Reports v2.0`, 2026-07-27
- `AN1200.66: PCB Design Guidelines`, 2026-05-20 · `AN1200.59 - Selecting the Optimal Reference Clock`, 2026-07-16

This is a **better** certification story than the SX1262 has in this knowledge base, where no
module-level certification could be found at all. Published ETSI and FCC prescan reports for a
reference design are a real head start — they are not a grant, and they do not transfer to your
board with your antenna, but they tell you the design has been through a chamber.

---

## 12. Choosing it, and choosing against it

**Reasons to choose the LR2021**

- You need **two bands from one SKU and one antenna path** — sub-GHz for range, 2.4 GHz for
  short-hop bulk — without an external RF switch.
- You need **more than LoRa's data rate**: FLRC at up to 2.6 Mbps is the only Semtech PHY that
  makes image or audio transfer over an ISM link plausible.
- You want **multi-SF reception** — for a mesh this is the standout, and nothing else in the
  lineage has it.
- You want to **drop the TCXO**. Wider frequency-offset tolerance plus on-chip NTC compensation is
  a BOM line and a sleep-current line removed.
- **Transmit energy**: 105 mA at +22 dBm versus 118 mA on an SX1262, because SIMO feeds the PA.
- You need a **PHY the SX126x cannot produce at all** — Z-Wave, BLE, 802.15.4, Sigfox BPSK.

**Reasons not to**

- ⚠ **Your driver is a rewrite, not a port** (§3). Budget for it honestly.
- ⚠ **No AES engine or secure key storage** (G3). If you picked LR11xx for its crypto, Gen 4 is a
  step backwards.
- ⚠ **No GNSS, no Wi-Fi scanning.** Gen 4 is not a superset of Gen 3 — geolocation stayed in the
  LoRa Edge line. If you want "where is it", you still want an [LR1121](../lr1121/README.md).
- ⚠ **Software is young.** USP says "not intended for production use"; RadioLib support is ~7
  months old; `LoRaMac-node` has no path at all.
- **Price and volume.** A `Core2021` at $12 against SX1262 modules at a few dollars, and an
  ecosystem two orders of magnitude smaller.
- **You gain nothing if you only ever run stock LoRaWAN or stock Meshtastic** — §8 says the air
  interface is compatible, which cuts both ways.

**Competing and substitute parts**

| Part | Relationship | When it wins |
|---|---|---|
| [**SX1262**](../sx1262/README.md) | Gen 2 baseline; **not a drop-in in either direction** | Cost, maturity, ecosystem. Still the right default for plain sub-GHz LoRa |
| [**LR1121**](../lr1121/README.md) | Gen 3; multi-band + GNSS + Wi-Fi scanning + **crypto** | Asset tracking; anything needing a secure element |
| [**LLCC68**](../llcc68/README.md) / [**SX1268**](../sx1268/README.md) | Gen-2 SX1262 siblings | Cost-down and 433/470 MHz respectively |
| [**SX1276/SX127x**](../sx1276/README.md) | Gen 1 | Only for compatibility with an existing Gen-1 deployment |
| **SX1280/SX1281** | **Gen 2**, 2.4 GHz only, has FLRC and ranging | Cheaper and far better supported if you only need 2.4 GHz FLRC — a community recommendation made repeatedly (`projects-and-community.md`) |
| **STM32WL** | SX126x core on-die with a Cortex-M | One chip instead of two, on the Gen-2 driver |
| **LR2022 / LR2012** | Same die family, features fused off | Cost, when you do not need FLRC/O-QPSK/Z-Wave/BLE. ⚠ No evidence of availability (G15) |

**Drop-in compatibility: none, in any direction.** Different package (QFN32 5 × 5 vs QFN24 4 × 4),
different pinout, different supply topology, different command encoding. What *is* compatible is
the air interface (§8).

---

## 13. Used By

**No board in this knowledge base uses the LR2021.** Every LoRa-bearing device documented here is
Gen 2 — the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md), the
[Cap LoRa-1262](../../../devices/m5stack/cap-lora-1262/README.md), the
[Cap LoRa868](../../../devices/m5stack/cap-lora868/README.md), the
[Cardputer Mesh Kit](../../../devices/m5stack/cardputer-mesh-kit/README.md), the
[Stamp C6LoRa](../../../devices/m5stack/stamp-c6lora/README.md) and
[Unit C6L](../../../devices/m5stack/unit-c6l/README.md) all carry an
[SX1262](../sx1262/README.md), and the [Ebyte E22-900M22S](../../ebyte/e22-900m22s/README.md)
is an SX1262 with an external PA. This record is here for the lineage and for the next board, not
because anything on the shelf needs it.

**Boards that do use it**, so the record is not a dead end:

| Board / module | Vendor | Evidence |
|---|---|---|
| **SenseCAP MeshTracker X1** | Seeed Studio | Meshtastic variant `variants/nrf52840/seeed_mesh_tracker_X1/` — `#define USE_LR2021`, `LR2021_DIO3_TCXO_VOLTAGE 1.6`, `LORA_DIO2` used as `BUSY` **[MT]** |
| **Meshnology W12** | Meshnology | Meshtastic variant `variants/esp32s3/meshnology-w12/` **[MT]** |
| **Wio-LR2021** RF board (in `LR2021EVK2*`) | Semtech / Seeed | Semtech's own EVK radio board; the only target USP calls *Validated* **[DRV]** |
| **Waveshare `Core2021-LF/-HF/-XF`** | Waveshare | Product page **[DOC]**; used in community builds |
| **NiceRF `LoRa2021F33-2G4`** (1 W) | NiceRF | **[COM]** — page 403s to automated clients |
| `nrf52_promicro_diy_tcxo` | DIY | The Meshtastic variant PR #10401 landed against **[MT]** |
| LilyGo T-Display P4 LR2021 | LilyGo | **[COM]**, hearsay; availability unconfirmed |

---

## 14. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf` | 5 809 234 | `0d9051db78b243bf89db7ff00bc549ff1fe3ffedc6e08649c9081e8393ef00b7` | **`DS.LR20xx`, LR2021/LR2022/LR2012 Final Datasheet Rev. 2.1, `13/04/26`, 243 pp.** The current retained revision |
| ~~`artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf`~~ **archived 2026-09-04** | 5 158 757 | `926b88cbfb6434e3954569b3f0d96e47c3ca2952245ebc1d01f65ab52d382ff7` | **`DS.LR2021`, LR2021 Final Datasheet Rev. 1.1, `10/14/25`, 236 pp.** Superseded; kept because it differs in substance — [placeholder](artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf.ARCHIVED.md) |
| `artifacts/usp-lr20xx_driver-v2.0.2-512a095.tar.gz` | 106 656 | `f1f172ce871a183d8d6431c157e0d44b457057ccd0c9e4d0e1c98bf76a3493ee` | **Semtech `lr20xx_driver` v2.0.2** plus the USP top-level `README.md`, `CHANGELOG.md`, `LICENSE.txt`, `LICENSES.txt`. 70 files, 688 630 B uncompressed |

### 14.1 Datasheet Rev 2.1 — provenance

| Field | Value |
|---|---|
| Document number / revision | **`DS.LR20xx`**, **Final Datasheet Rev. 2.1** |
| Publication date | **`13/04/26`** (running footer); PDF `/CreationDate` `D:20260413161603Z` |
| Pages | **243** |
| Retrieval date | **2026-09-04** |
| Byte size | **5 809 234** |
| SHA-256 | `0d9051db78b243bf89db7ff00bc549ff1fe3ffedc6e08649c9081e8393ef00b7` |
| **Canonical URL** | `https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ00000EZ5fu/L1sOvqDN_QMyCWYAAychIL5ygPsQw1AEq7xzcvpGNZg`, linked from `https://www.semtech.com/products/wireless-rf/lora-plus/lr2021`. ⚠ **`blocked`** — JS/POST content-distribution shell, see [`vendors/semtech/README.md` §4](../../../vendors/semtech/README.md) |
| **Digi-Key mirror (working)** | `https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8924/600_62785538.LR20xxDatasheet_V2_1.pdf` — HTTP 200, `application/pdf`, no UA games needed |
| Second independent source | Wayback capture of the Digi-Key URL, submitted 2026-09-04 |
| **Mirror lag** | ⚠ **`unresolved`.** Semtech lists **v2.2 dated 2026-08-08**; Digi-Key serves v2.1. A v2.2 exists but could not be retrieved (G1) |
| PDF metadata | `/Title` `LR20xxDatasheet_V2_1.pdf`, `/Author` `oprevost`, `/Creator` `FrameMaker 17.0.3`, `/Producer` `Adobe PDF Library 17.0`, `/ModDate` `D:20260413193222+02'00'` |
| Licence | **`unknown`** — © Semtech Corporation; every page footed **"Semtech Proprietary & Confidential"**, plus the LR-FHSS patent notice (G13) |
| Redistribution status | **`unknown`** — ⚠ a "Proprietary & Confidential" marking on a document that two authorised distributors mirror openly is a genuine conflict, not an oversight. Recorded, not resolved |
| Disposition | **`repository`, unstaged** pending review |
| Type validated | Yes — magic bytes `%PDF-1.6`; 243 pages parsed by `pypdf`; running footer cross-checked on every quoted page |

### 14.2 Datasheet Rev 1.1 vs Rev 2.1 — which is which

Same part, two revisions, **two different SHA-256 values and two different page counts**, and the
differences are substantive. Rev 2.1's own revision history:

| Version | Date | Change |
|---|---|---|
| 0.2 | June 2025 | Preliminary release |
| **1.1** | **October 2025** | Final datasheet; clarifications throughout |
| **2.1** | **April 2026** | Expanded to cover LR2022 and LR2012; **+0.5 dB added to all sensitivity numbers in Tables 3-13 and 3-18**; FLRC bandwidth values corrected in three places; **new command `SetLoraTxSync`**; **new §11.1.3 (G)FSK Limitations**; **new §22.3 Firmware Patch RAM**; `IDDSL1` sleep current changed; 434/490 MHz transmit table changed; Z-Wave typical sensitivities changed; electrical conditions clarified to *"no shield, SIMO"*; reference-design figure updated |
| 2.2 | 2026-08-08 | ⚠ **not obtained** (G1) |

**Rev 2.1 is authoritative. Rev 1.1 is the record of what Semtech said first**, and the only way to
tell whether a 2025-vintage board or driver was designed against numbers that no longer hold.

### 14.3 `lr20xx_driver` snapshot — provenance

| Field | Value |
|---|---|
| Upstream | `github.com/LoRa-Net/usp` (`Lora-net/usp` is the same org, case-insensitive) |
| **Commit** | **`512a095e303872f900021361a619b7b1e6e29469`** |
| Release tag | **`v1.1.2-feature-202604`**, published **2026-04-16T15:17:08Z** |
| Driver version string | **`v2.0.2`** — `smtc_rac_lib/radio_drivers/lr20xx_driver/inc/lr20xx_driver_version.h` |
| Driver changelog date | **2026-04-07** |
| Licence | **BSD-3-Clause-Clear** (`The Clear BSD License`, © Semtech Corporation 2022/2025). ⚠ GitHub's repo-level label is `NOASSERTION` because the monorepo is mixed-licence; the driver subtree carries its own `LICENSE.txt` |
| Redistribution status | **`allowed`**, conditional on preserving the copyright notice and the disclaimer — both are inside the tarball verbatim |
| Disposition | **`repository`** |
| Contents | The complete `smtc_rac_lib/radio_drivers/lr20xx_driver/` subtree (66 files) plus USP's top-level `README.md`, `CHANGELOG.md`, `LICENSE.txt`, `LICENSES.txt` |
| Why a subtree, not the repo | The full `usp` tree is **47 768 093 B** across 1 419 files, overwhelmingly `examples/` (977 files). The driver and its licence are what this record cites |
| Reacquisition | `gh api repos/LoRa-Net/usp/git/trees/512a095e303872f900021361a619b7b1e6e29469?recursive=1`, then `raw.githubusercontent.com/LoRa-Net/usp/512a095e.../<path>`. Also `https://github.com/LoRa-Net/usp/releases/tag/v1.1.2-feature-202604` |

---

## 15. Related components

- [**Semtech SX1262**](../sx1262/README.md) — **Gen 2**, the part every board in this repository actually has. Read it for what the migration is *from*
- [**Semtech LR1121**](../lr1121/README.md) — **Gen 3**, multi-band with GNSS and Wi-Fi scanning and the crypto engine Gen 4 dropped
- [**Semtech LR1110 / LR1120**](../lr11x0/README.md) — the rest of the Gen-3 LoRa Edge line
- [**Semtech SX1276 / SX127x**](../sx1276/README.md) — **Gen 1**, and the generation the LR2021 has explicit compatibility shims for
- [**Semtech SX1268**](../sx1268/README.md) · [**Semtech LLCC68**](../llcc68/README.md) — Gen-2 SX1262 siblings, and a real substitution trap
- [**`guides/hardware/lora-radio-generations.md`**](../../../guides/hardware/lora-radio-generations.md) — **start here** for the four generations side by side
- [**`vendors/semtech/README.md`**](../../../vendors/semtech/README.md) — how to get Semtech documents, what is gated, and what lies to you
- [**`projects-and-community.md`**](projects-and-community.md) — RadioLib and Meshtastic support with exact commits, evaluation kits, and what people report in the field
- [Components index](../../README.md)

---

## 16. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | LR2021/LR2022/LR2012 Datasheet | **Semtech**, mirrored by **Digi-Key** | authorized mirror | datasheet | `artifacts/lr20xx-datasheet-v2.1-digikey-mirror.pdf`; `mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8924/600_62785538.LR20xxDatasheet_V2_1.pdf` | 2026-09-04 | **`DS.LR20xx` Rev 2.1, 13/04/26**, 243 pp | §1–§8, §10 — including **§23.8, the generation list** |
| S-2 | LR2021 Datasheet | **Semtech**, mirrored by **Mouser** | authorized mirror | datasheet | [archived](artifacts/lr2021-datasheet-v1.1-mouser-mirror.pdf.ARCHIVED.md); `mouser.com/pdfDocs/61979758LR2021_V1_1_datasheet.pdf` (⚠ WhatsApp UA) | 2026-09-04 | **`DS.LR2021` Rev 1.1, 10/14/25**, 236 pp | §14.2 — corroborates §23.8 independently; G2 |
| S-3 | LoRa Plus™ LR2021 product page | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-plus/lr2021` | 2026-09-04 | datasheet entry **v2.2, 2026-08-08** | §1.1 (page title), §11.2 document list, G1 |
| S-4 | Semtech product sitemap | Semtech | primary | sitemap | `www.semtech.com/sitemap-products.xml` | 2026-09-04 | — | §1.2 — the **`lora-plus`** family exists and holds LR2012/LR2021/LR2022; LR2021 is **not** under `lora-connect` |
| S-4b | Semtech document catalogue — 1 984 entries embedded as JSON in the Development Support Documents page | Semtech | primary | machine-readable index | `www.semtech.com/design-support/development-support-documents/` (`var doc_portal`) | 2026-09-04 | dates 2018-11-14 … 2026-08-25 | G1 (the product page's *Datasheet* link is catalogued as **v2.2, 2026-08-08**), §11.2, G15. Extraction method in [`vendors/semtech/README.md` §3.2](../../../vendors/semtech/README.md) |
| S-5 | Semtech Salesforce content-distribution endpoint | Semtech | primary | download shell | `semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ00000EZ5fu/…` | 2026-09-04 | — | G1 — **negative result**, `executed-failed`; analysed in the vendor guide |
| S-6 | `LoRa-Net/usp` — Unified Software Platform, incl. `lr20xx_driver` | Semtech | primary | source | `artifacts/usp-lr20xx_driver-v2.0.2-512a095.tar.gz`; `github.com/LoRa-Net/usp` @ `512a095e303872f900021361a619b7b1e6e29469` | 2026-09-04 | driver **v2.0.2**; release `v1.1.2-feature-202604`, 2026-04-16; **BSD-3-Clause-Clear** | §7, §9, §9.1, G7, G8, G11 |
| S-7 | RadioLib | jgromes | community | source | `github.com/jgromes/RadioLib`, `src/modules/LR2021` | 2026-09-04 | first release **7.6.0**, 2026-02-19; first commit `2472fbdf…`, 2025-06-09 | §3.2, §9, §11 |
| S-8 | Meshtastic firmware | Meshtastic | community | source | `github.com/meshtastic/firmware`, PR #10401 → `5e2ca8aed4239f6682dede26485c63fcb2fdd521` | 2026-09-04 | merged **2026-05-08**; absent from v2.7.26, present in v2.8.0.* | §9, §13 |
| S-9 | `Core2021-XF/-HF/-LF` product page | Waveshare | primary | store listing | `www.waveshare.com/Core2021-XF.htm` | 2026-09-04 | US$11.99 / US$12.99 | §11.1; **G3** — independent assertion of no AES / no secure key storage |
| S-10 | LR2021 LoRa Plus Evaluation kit 915 MHz US V2.0 | Seeed Studio | primary | store listing | `www.seeedstudio.com/LR2021-LoRa-Plus-Evaluation-kit-915Mhz-US-V2-0-p-6698.html` | 2026-09-04 | **US$99.00** | §11.1 |
| S-11 | Reddit / community corpus | various | community | forum | catalogued in [`projects-and-community.md`](projects-and-community.md) | 2026-09-04 | 2025-03-12 … 2026-09-02 | §11 timeline; firsthand bench reports |
| S-12 | `www.nicerf.com/lora-module/lora2021f33-2g4.html` | NiceRF | primary | store listing | — | 2026-09-04 | — | **negative result**: HTTP **403** to both the Chrome and WhatsApp agents |
