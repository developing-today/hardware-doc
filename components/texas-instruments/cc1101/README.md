# Texas Instruments CC1101

- **Category:** low-power **sub-1 GHz RF transceiver** (300–348 / 387–464 / 779–928 MHz), SPI
- **Package as fitted:** **`CC1101RGPR`** — QFN-20 4 × 4 mm, pin 21 = exposed pad
- **Research status:** vendor-mirrored datasheet held; **register map decoded 2026-09-20** — see
  §11. Board integration documented for the two boards in this repository that fit it.
- **Retrieved:** 2026-09-04; extended **2026-09-20**

## 1. Identity and capability

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | Texas Instruments | datasheet |
| Ordering part | **`CC1101RGPR`** (RGP = QFN-20, R = tape and reel) | schematic comment on the Cap CC1101 |
| Bands | 300–348, 387–464, 779–928 MHz | datasheet / vendor claims |
| Modulations | **2-FSK, 4-FSK, GFSK, MSK, ASK, OOK** | vendor |
| Data rate | 0.6 – 600 kbps (silicon); the Cap's example uses **2.4 kbps** | datasheet / vendor example |
| FIFOs | **64 B TX + 64 B RX**, independent | vendor |
| Host interface | **4-wire SPI** + `GDO0` / `GDO2` general-purpose digital outputs (`GDO1` doubles as MISO) | datasheet |
| **Reset** | **no reset pin** — reset is the `SRES` SPI command strobe | datasheet |
| Reference | external crystal **26 or 27 MHz**, *or* an external **reference signal** 26–27 MHz into `XOSC_Q1` — see §12 | datasheet §4.4, §7.4 |
| Bias | external `RBIAS` resistor — **56 kΩ** as fitted | as fitted |
| RF port | **differential** (`RF_P`, `RF_N`) — needs a balun for a 50 Ω single-ended antenna | as fitted |
| Output power | **up to +12 dBm** across all bands (silicon); RadioLib exposes the quantised set **−30, −20, −15, −10, 0, 5, 7, 10 dBm** | datasheet Key Features / RadioLib |
| Sensitivity | **−116 dBm** @ 0.6 kBaud 433 MHz · **−112 dBm** @ 1.2 kBaud 868 MHz (1 % PER) | datasheet Key Features |
| Sleep | **200 nA**; **240 µs** sleep → RX or TX | datasheet Key Features |
| ❌ **Cannot do** | **LoRa.** Chirp spread spectrum is Semtech-proprietary and not implemented in any TI sub-GHz part | see §5 |

## 2. `GDO0` and `GDO2` — the pins worth understanding

The CC1101's two general-purpose digital outputs are **software-selected from a large menu**
of internal signals via `IOCFG0` / `IOCFG2`. Two menu entries matter disproportionately:

| Use | How |
|---|---|
| Packet interrupt / sync-word detect | the conventional `GDO0` configuration |
| **Static logic level** | select **`GDOx_HW_TO_0`** ("hardwired to 0") and then set or clear the **polarity-inversion** bit to emit a constant **0** or **1** |

The second use turns a radio pin into a **free general-purpose output that costs the host no
GPIO**. The Cap CC1101 spends `GDO2` exactly that way, to drive half of its band-select
logic. RadioLib exposes the constants as `RADIOLIB_CC1101_GDOX_HW_TO_0`,
`RADIOLIB_CC1101_GDO2_NORM` and `RADIOLIB_CC1101_GDO2_INV`.

**Cost of the trick:** the pin is only controllable once SPI is up, so anything it drives
cannot be configured before the radio is initialised.

## 3. What a host must provide

| Resource | Count | Notes |
|---|---|---|
| SPI SCK/MOSI/MISO | 3 | shareable with other SPI devices |
| `CSN` | 1 | dedicated |
| `GDO0` | 1 | packet interrupt |
| `GDO2` | 0–1 | optional second interrupt **or** a free static output |
| Reset GPIO | **0** | there is no reset pin |
| Crystal | 1 | 26 MHz, 12 pF loads as fitted |
| `RBIAS` resistor | 1 | not optional — sets internal bias current |
| Balun + matching | 1 set | differential-to-50 Ω |

## 4. Drivers and libraries

| Library | Notes |
|---|---|
| **RadioLib** (jgromes), **MIT** | The driver M5Stack's documentation links to for the Cap CC1101. Same API family as its SX1262 driver, so **one library serves both radios** — a meaningful fact for firmware that already carries RadioLib for LoRa. `new Module(csn, gdo0, RADIOLIB_NC /*rst*/, gdo2)` then `begin(freq, bitrate, freqDev, rxBw, power, preambleLen)` |
| SmartRF Studio (TI) | Register-set generator; not used by any project in this repository |
| **M5Stack** | **No M5Stack CC1101 library exists** — `org:m5stack cc1101` returns 0 repositories (2026-09-04, `executed-success`) |

## 5. CC1101 versus LoRa — a recurring confusion

The bands overlap almost exactly (433/868/915 MHz), so buyers repeatedly ask whether a
CC1101 board can join a LoRa or Meshtastic network. It cannot: LoRa's chirp-spread-spectrum
PHY is Semtech intellectual property, licensed to a handful of vendors (ST, Microchip, ASR),
and TI is not among them. A CC1101 and an SX1262 cannot hear each other at all.

## 6. Caveats

- **64-byte FIFOs.** Longer packets require infinite-packet-length mode with mid-transfer
  FIFO servicing — a classic source of CC1101 bugs.
- **Band-specific matching.** One CC1101 covers three bands, but one *matching network* does
  not. Multi-band designs need switched paths (see the Cap CC1101) or accept large losses.
- **`GDO1` is `MISO`.** Do not configure `IOCFG1` casually.
- **Legality is per-band and per-region** — 315 MHz is not an EU allocation, 915 MHz is not
  either. See [`devices/m5stack/cap-cc1101/features/sub-ghz.md` §7](../../../devices/m5stack/cap-cc1101/features/sub-ghz.md).

## 7. Used By

### [M5Stack Cap CC1101 & NFC (U219)](../../../devices/m5stack/cap-cc1101/README.md) — designator `U3`, sheet 3

The only board in this repository fitted with a CC1101.

| Signal | Chip pin | Board net | Host GPIO (Cardputer-Adv) |
|---|---:|---|---|
| `SCLK` | 1 | `SPI_SCLK` | **G40** |
| `MISO` | 2 | `SPI_MISO` | **G39** |
| `MOSI` | 20 | `SPI_MOSI` | **G14** |
| `CSN` | 7 | `CC1101_CS` | **G5** |
| `GDO0` | 6 | `CC1101_G0`, via `R4` **330 Ω** | **G15** |
| **`GDO2`** | 3 | **`CC1101_RF_SW1`** — stays on the board | — |
| `RF_P` / `RF_N` | 12 / 13 | via `C46`/`C42` 100 pF → `B1` balun | — |
| `XOSC_Q1` / `Q2` | 8 / 10 | `Y2` **26 MHz**, `C48`/`C49` 12 pF | — |
| `RBIAS` | 17 | `R6` **56 kΩ** | — |
| `DCOUPL` | 5 | local decoupling | — |
| `AVDD` | 9, 11, 14, 15 | `VDD_3V3`, `C37`–`C41` 100 nF | — |
| `DVDD` | 4 | `VDD_3V3` | — |
| `DGUARD` | 18 | — | — |
| `GND` | 16, 19, EPAD 21 | `GND` | — |

Board-level notes:

- **Shared SPI** with an ST25R3916 NFC front end (`CS` = G6) and the host's microSD
  (`CS` = G12). The NFC part is driven in **SPI mode 1**; anything using both must
  re-establish the mode per transaction.
- **`GDO2` drives band selection**, not an interrupt — see §2 and
  [the band-switching guide](../../../devices/m5stack/cap-cc1101/features/band-switching.md).
- The whole board's 3.3 V rail is gated by host **G3** (`POWER_EN`).
- Vendor claims for the fitted part: **+10 dBm** TX, **−99.5 dBm** RX, ~435–441 m at
  58 kbps FSK.

### Not fitted elsewhere

M5Stack also sells a **CC1101 Module (M146)**, 855–925 MHz single-band, USD 10.95, published
2025-11-07 — a **Core-bus** module, not a Cardputer accessory. No record in this repository.

### [`badgeteam/konsool-zero`](https://github.com/badgeteam/konsool-zero) — designator `U1`, sheet `sub-ghz-radio` · *added 2026-09-20*

The **second** board in this repository fitted with a CC1101, and the first outside M5Stack. A
work-in-progress Flipper-Zero-class radio expansion for the
[Tanmatsu / Konsool](../../../devices/nicolai-electronics/tanmatsu/README.md) rear 36-pin port.
**Fitment established** from the project's own KiCad schematic at commit `0f0b964`:

| Field | Value |
|---|---|
| Reference | **`U1`** |
| Value | **`CC1101RGPR`** — the same orderable as the Cap CC1101 |
| Footprint | `lcsc:QFN-20_L4.0-W4.0-P0.5-TL-EP` — QFN-20 4 × 4 mm, exposed pad |
| Reference clock | **`U2`** — a **27 MHz 4-pin SMD oscillator** (`lcsc:OSC-SMD_4P-L3.2-W2.5-BL`, `G3226000161060`), ⚠ **not a passive crystal**. See below |

Hierarchical nets on the `sub-ghz-radio` sheet: `CC1101_CS`, `CC1101_G0`, `SPI_R_SCK`,
`SPI_R_MOSI`, `SPI_R_MISO`, `RF_SW`, `RF_SW_0`, `RF_SW_1`. `J2` is an **SMA edge-mount coaxial
connector** (`Connector_Coaxial:SMA_Samtec_SMA-J-P-H-ST-EM1_EdgeMount`) whose schematic value is
the string `LoRa`.

Three observations, all read from the schematic only:

- **⚠ This board drives the CC1101 from an oscillator, not a crystal.** The Cap CC1101 fits a
  two-pin 26 MHz crystal with 12 pF loads (§7); konsool-zero fits a powered four-pin XO. That is a
  **supported but different configuration** — datasheet §7.4 *Reference Signal*: the part "can
  alternatively be operated with a reference signal from 26 to 27 MHz instead of a crystal",
  driven into **`XOSC_Q1`**, with **`XOSC_Q2` left unconnected** and the load capacitors `C81`/`C101`
  omitted. A full-swing digital signal may be DC-coupled; a sine ≤ 1 Vpp needs a series capacitor.
  Anyone reworking this board must not "fix" it by fitting a crystal without also restoring
  `XOSC_Q2` and the loads. Whether the layout actually leaves `XOSC_Q2` open was **not traced** —
  `not-tested`.
- **27 MHz is a deliberate band choice**, not an error: TI recommends 27 MHz for operation
  **above 869 MHz** (§12).
- **The same SP3T band-switch part as the Cap.** `RF_SW_0`/`RF_SW_1` drive two Infineon
  **`BGS13S4N9E6327XTSA1`** switches (`U3`, `U4`, `antenna-balance` sheet) — the same part the Cap
  CC1101 uses (§8). But here both labels *also* appear on the `zero-mcu` sheet beside the
  [CH32V003](../../wch/ch32v003/README.md), so band select appears to be driven by the **local
  MCU** rather than by a repurposed `GDO` pin as on the Cap. `inferred` from label co-occurrence;
  nets were not traced individually.

⚠ **`J2`'s `LoRa` label is unexplained.** It is an SMA antenna jack on the sub-GHz sheet, and a
CC1101 cannot do LoRa (§5). Plausible readings — a copied symbol value, a shared antenna port
intended for an alternative radio, or simply loose naming — but **none is established**; the sheet
was not traced to determine what `J2` connects to. Recorded as an open question, not a finding.

⚠ **Status: design study, not a buildable board.** One commit, no README, no stated licence, no
firmware. **Nothing was built, fitted or powered.** `not-tested`. No host-GPIO column is given
because the expansion-connector mapping was not traced in this pass.

## 8. Related components

- [`components/generic/rf-balun-b0310j50100ahf`](../../generic/rf-balun-b0310j50100ahf/README.md) — the balun on its RF port
- [`components/infineon/bgs13sn8`](../../infineon/bgs13sn8/README.md) — the SP3T switches it feeds
- [`components/semtech/sx1262`](../../semtech/sx1262/README.md) — the LoRa part it is *not*

## 9. Local artifacts

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/cc1101-datasheet-m5stack-mirror.pdf`](artifacts/cc1101-datasheet-m5stack-mirror.pdf) | 2 718 663 | `0c5cdadd06a9f8de6776dda8c8fb29c5029baa2838413335270e223e55a4e169` | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1188/CC1101_Datasheet.pdf`, retrieved 2026-09-04, HTTP 200, `%PDF-1.4` |

⚠ **This is a vendor mirror.** Note the CDN path prefix `/1188/` belongs to the **CC1101 Module
(M146)** product, not to the Cap CC1101 — M5Stack reuses one upload across products.

✅ **Revision resolved 2026-09-20.** This copy is **`SWRS061I`**, and its body has been verified
**byte-identical** to an independently-acquired second copy of the same revision. The earlier
concern that its revision was "unverified against TI's own copy" is settled — see **§13**, which
also explains why two copies of this datasheet will nearly always have different hashes without
differing technically. A second copy is now held alongside it.

Licence/redistribution: **unknown** (TI datasheets carry TI's standard notices). Disposition:
**repository, unstaged** pending review.

## 10. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| T-1 | CC1101 datasheet | Texas Instruments, mirrored by M5Stack | authorized mirror | datasheet | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1188/CC1101_Datasheet.pdf` | 2026-09-04 | The part |
| T-2 | Cap CC1101 schematic V0.3 | M5Stack | primary | schematic | held at [`devices/m5stack/cap-cc1101/artifacts/schematic/`](../../../devices/m5stack/cap-cc1101/artifacts/schematic/) | 2026-09-04 | §7 pin table |
| T-3 | Cap CC1101 Arduino guide | M5Stack | primary | tutorial | `https://docs.m5stack.com/en/arduino/projects/cap/cap_cc1101` | 2026-09-04 | §2 `GDOX_HW_TO_0` trick, §4 RadioLib usage |
| T-4 | RadioLib | jgromes | primary | repository | `https://github.com/jgromes/RadioLib` | 2026-09-04 | Driver, MIT, rel. 7.7.1 |
| T-5 | r/CardPuter release thread | community | forum | `https://old.reddit.com/r/CardPuter/comments/1w0nwti/` | 2026-09-04 | §5 — the CC1101-vs-LoRa explanations |

---

## 11. SPI, the status byte, and the traps · *added 2026-09-20*

Mined from `SWRS061I` §10 and §19 — the material the 2026-09-04 pass left undecoded.

### 11.1 The status byte

Every SPI transaction returns a status byte on `SO`. On **writes** it is emitted for each header
*and* data byte; on **reads**, only for the header byte.

| Bits | Field | Meaning |
|---|---|---|
| 7 | `CHIP_RDYn` | Stays **high** until power and crystal have stabilised. **Should always be low** when using SPI — a high bit means you are talking to a chip that is not ready |
| 6:4 | `STATE[2:0]` | `000` IDLE · `001` RX · `010` TX · `011` FSTXON · `100` CALIBRATE · `101` SETTLING · `110` **RXFIFO_OVERFLOW** · `111` **TXFIFO_UNDERFLOW** |
| 3:0 | `FIFO_BYTES_AVAILABLE` | Bytes available in RX FIFO, or **free** bytes in TX FIFO, depending on the `R/W̄` bit of the strobe. Saturates: `15` means "15 or more" |

⚠ `IDLE` is **also reported for some transitional states** instead of `SETTLING` or `CALIBRATE`.
Do not treat `STATE == IDLE` as proof the radio is idle.

### 11.2 Four traps that produce real bugs

**① Burst access does not work on status registers.** Configuration registers live at `0x00`–`0x2E`
and support burst reads/writes with an auto-incrementing address counter. But for addresses
**`0x30`–`0x3D`** the burst bit is **repurposed**: burst = 1 selects a *status register*, burst = 0
selects a *command strobe*. Consequently:

> "burst access is not available for status registers and they must be accessed one at a time."

Code that burst-reads `0x30`+ to grab `PARTNUM`, `VERSION`, `RSSI`, `MARCSTATE` and `TXBYTES` in
one transaction will instead **fire command strobes**. This is the classic CC1101 defect.

**② Dynamically-updated registers can read back corrupt.** For registers the radio hardware
updates underneath you — `MARCSTATE`, `TXBYTES`, `RXBYTES`, `RSSI` — there is a small but finite
probability a single read is corrupt: TI quantifies it as **≈ 80 ppm per read from `TXBYTES` at
maximum data rate**. The documented mitigation is to read repeatedly until two consecutive reads
agree. TI's *CC1101 Errata Notes* (`SWRZ020`) has the detail; **that errata document is not held
in this repository** — a gap.

**③ `SIDLE` silently swallows subsequent strobes.**

> "An `SIDLE` strobe will clear all pending command strobes until IDLE state is reached."

So a strobe issued between `SIDLE` and the actual arrival at IDLE is **ignored without error**.
Poll the status byte for `STATE == IDLE` before the next strobe.

**④ Three strobes are deferred to `CSn` rising.** Strobes execute immediately **except**
`SPWD`, `SWOR` and `SXOFF`, which execute when **`CSn` goes high**. Holding `CSn` low after an
`SPWD` leaves the part awake. Related: a strobe may be followed by another SPI access without
raising `CSn` — **but after `SRES` you must wait for `SO` to go low** before the next header byte.

### 11.3 Reset — the manual power-up sequence

There is no reset pin (§1). The automatic POR is used when the supply ramp meets the Table 18
requirements; otherwise use the manual sequence (§19.1, Figure 27), in order:

1. Set `SCLK = 1` and `SI = 0` — avoids tripping the chip into **pin control mode** (§11.3 of the datasheet).
2. Strobe `CSn` low, then high.
3. Hold `CSn` low, then high, for **at least 40 µs** relative to pulling `CSn` low.
4. Pull `CSn` low and **wait for `SO` to go low** (`CHIP_RDYn`).
5. Issue the `SRES` strobe on `SI`.
6. When `SO` goes low again, reset is complete and the part is in **IDLE**.

⚠ **`GDO0` outputs a clock by default.** After any reset the default `IOCFG0` setting emits
`CLK_XOSC/192` on `GDO0`. The datasheet explicitly recommends changing it to optimise TX/RX
performance. If `GDO0` drives a host interrupt line, that default is an unexpected ~135 kHz
interrupt storm at power-up until firmware reconfigures it — configure `IOCFG0` early.

### 11.4 FIFO fault states must be cleared explicitly

`RXFIFO_OVERFLOW` (`110`) and `TXFIFO_UNDERFLOW` (`111`) are **latched states**, not flags. Read
out any useful data, then clear with **`SFRX`** / **`SFTX`** respectively. The radio will not
leave the state on its own, and `MARCSTATE` values 17 (`RX_OVERFLOW`) and 22 (`TX_UNDERFLOW`)
correspond. Combined with the 64-byte FIFOs (§6), this is the mechanism behind most
"CC1101 stops receiving after a while" reports.

## 12. The crystal: 26 MHz vs 27 MHz · *added 2026-09-20*

Datasheet §4.4, Table 13: crystal frequency **min 26, typ 26, max 27 MHz**; tolerance **±40 ppm
total** (initial + loading + aging + temperature); load capacitance 10/13/20 pF; ESR ≤ 100 Ω;
start-up ≈ 150 µs.

TI's guidance is **band-dependent**, and it is a compliance point rather than a preference:

> "For compliance with modulation bandwidth requirements under **EN 300 220** in the 863 to
> 870 MHz frequency range it is recommended to use a **26 MHz** crystal for frequencies **below
> 869 MHz** and a **27 MHz** crystal for frequencies **above 869 MHz**."

There is a second consequence: with a 27 MHz reference the **lower limit of the middle band rises
from 387 MHz**, and the frequency-programming resolution changes (`FXOSC/2¹⁶` ≈ 397 Hz at 26 MHz,
412 Hz at 27 MHz). Data-rate and channel-bandwidth register arithmetic is referenced to `FXOSC`
throughout, so **register sets generated for 26 MHz are wrong on a 27 MHz board** — SmartRF Studio
asks for the crystal frequency for exactly this reason.

This explains the divergence between the two boards in this repository: the M5Stack Cap fits
**26 MHz** (§7) and targets 433/868 MHz; konsool-zero fits **27 MHz** (§7) and is evidently aimed
at the **≥ 869 MHz** part of the band. Neither is an error.

**A crystal is not the only option.** Datasheet §7.4 *Reference Signal*: the part can run from an
external 26–27 MHz reference instead — a full-swing digital clock (0 V to VDD, DC-coupled) or a
sine of **max 1 Vpp** through a series capacitor, into **`XOSC_Q1`**. In that configuration
**`XOSC_Q2` must be left unconnected** and the load capacitors `C81`/`C101` omitted. konsool-zero
appears to take this route, fitting a powered 4-pin oscillator rather than a 2-pin crystal (§7).
The trap is symmetrical: a crystal-designed layout will not work with an XO, and an XO-designed
layout will not work with a crystal, because `XOSC_Q2` and the loads differ.

## 13. Two copies of `SWRS061I`, and what differs · *added 2026-09-20*

A second copy of this datasheet arrived via `badgeteam/konsool-zero`'s `docs/` folder. §9
previously flagged this as an open question:

> *"⚠ This is a vendor mirror, and its revision is unverified against TI's own copy… If precision
> about a register detail matters, fetch TI's copy and compare hashes; a differing hash under the
> same document name is itself a finding."*

**That question is now answered.** The hashes differ — and the finding is benign.

| | konsool-zero copy *(new)* | M5Stack mirror *(held since 2026-09-04)* |
|---|---|---|
| Document revision | **`SWRS061I` (Rev I)** | **`SWRS061I` (Rev I)** |
| Pages | **107** | **112** |
| Bytes | 2 572 666 | 2 718 663 |
| SHA-256 | `61efc50f…` | `0c5cdadd…` |
| PDF `CreationDate` | 2023-09-17 | 2025-07-20 |
| Copyright line | © **2023** | © **2025** |
| *Package option addendum* | 10-Dec-2020 | *(regenerated)* |
| *Package materials information* | **17-Apr-2023** | **18-Jul-2025** |
| Land-pattern drawing | `4226714/A` **04/2021** | `4219027/A` **03/2025** |

### The datasheet body is byte-identical

Both files were extracted with `pdftotext -layout` and truncated at the body's own last page
marker (`SWRS061I … Page 98 of 98`). The two extractions are **5 927 lines each and `diff`
reports zero differences** — `executed-success`, 2026-09-20.

**So the 5-page delta is entirely TI's auto-generated appendix.** TI appends a *Package Option
Addendum* and *Package Materials Information* section that is **regenerated at download time**;
the technical content of Rev I is unchanged since 2023. Two copies of the "same" TI datasheet will
essentially always differ in hash. **This is not mirror lag and not a revision difference.**

### The delta is not entirely worthless, though

Two things did change between the 2023 and 2025 appendices, and both matter to whoever fabricates
a board:

- **Recommended stencil aperture changed.** Solder-paste coverage under the QFN-20 exposed pad
  (pin 21) went from **69 %** (drawing `4226714/A`, 04/2021) to **78 %** (drawing `4219027/A`,
  03/2025), on a 0.125 mm stencil. **Use the newer copy for land-pattern and stencil work.**
- **Orderable part numbers expanded.** The 2023 addendum lists `CC1101RGP` / `RGPR` / `RGPT`. The
  2025 one adds die-revision and green-variant suffixes — `CC1101RGP.B`, `CC1101RGPR.A`,
  `CC1101RGPR.B`, `CC1101RGPRG4`, `CC1101RGPRG4.A`, `CC1101RGPRG4.B` — all **Active / Production**,
  QFN (RGP) 20-pin, −40 to 85 °C, marking `CC1101`. **`CC1101RGPR`**, the part both boards here
  fit, is Active in both.

**Both copies retained.** Same revision, different bytes → keep both per the repository's
deduplication rule; the older one is a dated snapshot of TI's 2020/2021 ordering and land-pattern
data, which TI does not otherwise publish historically. For any *technical* question, either copy
serves — the body is identical. For **land patterns, stencils or ordering**, use the **2025**
copy.

### Updated artifact table

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/cc1101-datasheet-m5stack-mirror.pdf`](artifacts/cc1101-datasheet-m5stack-mirror.pdf) | 2 718 663 | `0c5cdadd06a9f8de6776dda8c8fb29c5029baa2838413335270e223e55a4e169` | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1188/CC1101_Datasheet.pdf`, retrieved 2026-09-04, HTTP 200, `%PDF-1.4`. **`SWRS061I`, appendix regenerated 2025-07-20, 112 pp.** ⭐ **preferred copy** |
| [`artifacts/cc1101-datasheet-swrs061i-2023-addendum-konsool-zero-mirror.pdf`](artifacts/cc1101-datasheet-swrs061i-2023-addendum-konsool-zero-mirror.pdf) | 2 572 666 | `61efc50fdf7a18f258a6f326dac8acca168bd006cccca426103aa99d7e491a3d` | **`SWRS061I`, appendix generated 2023-09-17, 107 pp.** PDF metadata `Author "Texas Instruments, Incorporated [SWRS061,I"`, `Creator "Microsoft® Word 2010"` — an unmodified TI export. Vendored in `badgeteam/konsool-zero` `docs/cc1101_datasheet.pdf` @ `0f0b964`; moved here 2026-09-20. Upstream URL not recorded by the vendoring project; TI serves only the current build at `https://www.ti.com/lit/ds/symlink/cc1101.pdf`, so this 2023 appendix is **`blocked`** for reacquisition from TI |

Both validated as `%PDF-1.4` from content. Text layers cross-checked against the rendered cover
heading ("CC1101 / Low-Power Sub-1 GHz RF Transceiver") and the `SWRS061I` page footers before any
value was transcribed — `executed-success`, 2026-09-20. Licence **unknown** for both (TI's
standard "IMPORTANT NOTICE AND DISCLAIMER"; note it states *"Other reproduction and display of
these resources is prohibited"* — recorded as metadata, not adjudicated). Disposition:
**repository, unstaged.**

## 14. Additional sources · *added 2026-09-20*

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| T-6 | CC1101 datasheet, konsool-zero copy | Texas Instruments | primary | datasheet | [`artifacts/…-2023-addendum-konsool-zero-mirror.pdf`](artifacts/cc1101-datasheet-swrs061i-2023-addendum-konsool-zero-mirror.pdf) | 2026-09-20 | `SWRS061I`, appendix 2023-09-17, 107 pp | §11 SPI traps, §12 crystal, §13 comparison |
| T-7 | `badgeteam/konsool-zero` KiCad design @ `0f0b964` | Badge.Team | primary | repository (schematic) | `scratch/tanmatsu/sources/konsool-zero/sub-ghz-radio.kicad_sch` | 2026-09-20 | single commit, 2025-03-22, no stated licence | §7 fitment `U1 = CC1101RGPR`, `U2` 27 MHz |
| T-8 | Flipper Zero **Sub-1 GHz CC1101** schematic | **Flipper Devices Inc.** | primary (third-party) | schematic PDF | `scratch/tanmatsu/sources/konsool-zero/docs/Sub-1 GHz CC1101 schematic.pdf` | 2026-09-20 | undated | §7 — prior art; independently names `CC1101RGPR` |
| T-9 | CC1101 Errata Notes `SWRZ020` | Texas Instruments | primary | errata | `https://www.ti.com/lit/er/swrz020b/swrz020b.pdf` | — | — | ⚠ **not retrieved.** Referenced by §11.2; a known gap |
