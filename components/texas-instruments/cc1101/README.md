# Texas Instruments CC1101

- **Category:** low-power **sub-1 GHz RF transceiver** (300–348 / 387–464 / 779–928 MHz), SPI
- **Package as fitted:** **`CC1101RGPR`** — QFN-20 4 × 4 mm, pin 21 = exposed pad
- **Research status:** vendor-mirrored datasheet held; **register map not decoded** by this
  pass. What is documented here is the part's role and its integration on the one board in
  this repository that fits it.
- **Retrieved:** 2026-09-04

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
| Reference | external crystal, **26 MHz** typical | as fitted |
| Bias | external `RBIAS` resistor — **56 kΩ** as fitted | as fitted |
| RF port | **differential** (`RF_P`, `RF_N`) — needs a balun for a 50 Ω single-ended antenna | as fitted |
| Output power | quantised set; RadioLib exposes **−30, −20, −15, −10, 0, 5, 7, 10 dBm** | RadioLib / vendor example |
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

## 8. Related components

- [`components/generic/rf-balun-b0310j50100ahf`](../../generic/rf-balun-b0310j50100ahf/README.md) — the balun on its RF port
- [`components/infineon/bgs13sn8`](../../infineon/bgs13sn8/README.md) — the SP3T switches it feeds
- [`components/semtech/sx1262`](../../semtech/sx1262/README.md) — the LoRa part it is *not*

## 9. Local artifacts

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/cc1101-datasheet-m5stack-mirror.pdf`](artifacts/cc1101-datasheet-m5stack-mirror.pdf) | 2 718 663 | `0c5cdadd06a9f8de6776dda8c8fb29c5029baa2838413335270e223e55a4e169` | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1188/CC1101_Datasheet.pdf`, retrieved 2026-09-04, HTTP 200, `%PDF-1.4` |

⚠ **This is a vendor mirror, and its revision is unverified against TI's own copy.** Note
the CDN path prefix `/1188/` belongs to the **CC1101 Module (M146)** product, not to the Cap
CC1101 — M5Stack reuses one upload across products. If precision about a register detail
matters, fetch TI's `www.ti.com/lit/ds/symlink/cc1101.pdf` and compare hashes; a differing
hash under the same document name is itself a finding.

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
