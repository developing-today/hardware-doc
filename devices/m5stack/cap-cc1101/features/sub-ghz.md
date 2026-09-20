# Sub-GHz radio — Cap CC1101 (U219)

> **How do I transmit and receive?** §5. **How do I change band?** [`band-switching.md`](band-switching.md).
> **How do I put a CC1101 on my own hardware?** §9.
> Snapshot 2026-09-04 · schematic **V0.3 / 2026-05-28** · nothing tested on hardware.

## 1. Hardware path

```
                                     ┌── L6/L7/L8 + L17 3.6nH + C50 8pF ──┐   315 MHz
CC1101 (U3)                          │                                     │
  RF_P(12) ── C46 100pF ──┐          ├── L9 + L10..L13 + C52..C55 ─────────┤   433 MHz
  RF_N(13) ── C42 100pF ──┤ B1 balun │                                     │
      C43 0.6pF across ───┘ B0310J50100AHF                                 │
      L4 3.3nH / L5 6.8nH / R5 0R    ├── L15 0R / L16 10nH + C58..C61 ─────┤   868/915 MHz
      C44 DNP / C45 / C47 100pF      │                                     │
                                U4 BGS13SN8 (SP3T)                   U5 BGS13SN8 (SP3T)
                                  V1/V2 ◀── RF_SW0, RF_SW1 ──▶ V1/V2
                                                                            └──▶ E1 SMA
```

| Element | Part | Record |
|---|---|---|
| Transceiver | **`CC1101RGPR`**, QFN-20 + EPAD | [`components/texas-instruments/cc1101`](../../../../components/texas-instruments/cc1101/README.md) |
| Balun | **`B0310J50100AHF`** — 6-pin, `Unbalanced`(1) / `GND`(2) / `Balanced`(3,4) / `DNC`(5) / `NC`(6) | [`components/generic/rf-balun-b0310j50100ahf`](../../../../components/generic/rf-balun-b0310j50100ahf/README.md) |
| Band switches | **2 × `BGS13SN8E6327XTSA1`** SP3T | [`components/infineon/bgs13sn8`](../../../../components/infineon/bgs13sn8/README.md) |
| Reference | **26 MHz** crystal `Y2` (`Y2016` package), `C48`/`C49` 12 pF | — |
| Bias | `R6` **56 kΩ** on `RBIAS` (pin 17) | — |
| Antenna | `E1` `SMA-TH_KH-SMA-KE-Z`; three whips supplied | [`components/generic/rp-sma-and-sma-antenna-connectors`](../../../../components/generic/rp-sma-and-sma-antenna-connectors/README.md) |

**Why the design looks like this.** A CC1101 has a differential RF port and needs a
band-specific match; one match cannot serve 315 and 915 MHz well. M5Stack solved it by
putting a **wideband balun** at the chip and then switching between **three narrowband LC
paths** with a pair of SP3T switches. That is why there are three inductor/capacitor
clusters on sheet 3 with the Chinese annotations `315MHz 频段`, `433MHz 频段` and
`868MHz 频段` ("frequency band"), and why the vendor can claim usable range on all of them
rather than only on one.

## 2. Chip pin map as fitted

**[SCH]** sheet 3, `U3`.

| Pin | Name | Net |
|---:|---|---|
| 1 | `SCLK` | `SPI_SCLK` → Cap-Bus 11 → host **G40** |
| 2 | `MISO` | `SPI_MISO` → Cap-Bus 13 → host **G39** |
| 20 | `MOSI` | `SPI_MOSI` → Cap-Bus 12 → host **G14** |
| 7 | `CSN` | `CC1101_CS` → Cap-Bus 14 → host **G5** |
| **6** | **`GDO0`** | via `R4` **330 Ω** → `CC1101_G0` → Cap-Bus 1 → host **G15** — the interrupt/data line |
| **3** | **`GDO2`** | **`CC1101_RF_SW1`** — stays on the board, drives the band switches |
| 5 | `DCOUPL` | decoupled locally |
| 17 | `RBIAS` | `R6` 56 kΩ |
| 12 | `RF_P` | → `C46` → balun |
| 13 | `RF_N` | → `C42` → balun |
| 8 | `XOSC_Q1` | `Y2` 26 MHz |
| 10 | `XOSC_Q2` | `Y2` 26 MHz |
| 4 | `DVDD` | `VDD_3V3` |
| 9, 11, 14, 15 | `AVDD` | `VDD_3V3`, `C37`–`C41` 100 nF |
| 18 | `DGUARD` | — |
| 16, 19 | `GND` | — |
| 21 | `EPAD` | `GND` |

> **`GDO0` carries a 330 Ω series resistor** on its way to the host. That is a
> current-limit/edge-softening measure, not a level shift. Worth knowing if you plan to run
> it fast or drive it as an output.

> **`GDO1` is not used.** On a CC1101, `GDO1` doubles as `MISO`; leaving it as MISO only is
> the normal choice.

## 3. Vendor RF claims

| Item | Value | Caveat |
|---|---|---|
| TX power | **+10 dBm** | RadioLib's allowed set for CC1101 is `-30, -20, -15, -10, 0, 5, 7, 10` dBm; +10 is the maximum |
| RX sensitivity | **up to −99.5 dBm** | data-rate dependent; the rate is not stated |
| Range | 315 MHz **435 m**; 433/868/915 MHz **441 m** | at "FSK modulation, 58 kbps air rate"; **no antenna, height, terrain or link-margin criterion given** |
| FIFOs | 64 B TX + 64 B RX | independent; the classic CC1101 packet-length constraint |
| Modulations | 2-FSK, 4-FSK, GFSK, MSK, ASK, OOK | |

Prose: the two range numbers differing by 6 m across a 3× frequency span is not physically
meaningful as a measurement — it reads like two runs of the same test. Treat "a few hundred
metres, line of sight, with the supplied whip" as the honest summary.

## 4. Software — RadioLib, and the exact vendor configuration

M5Stack's "Cap CC1101 Arduino CC1101 Driver Library" link points at **`jgromes/RadioLib`**.
There is **no M5Stack CC1101 library**. **[DOC]**, corroborated by a `org:m5stack cc1101`
GitHub search returning **0 repositories**.

```cpp
#include <M5Unified.h>
#include <RadioLib.h>

#define CC1101_FREQ         915.0f   // MHz, must match the receiver
#define CC1101_BIT_RATE     2.4f     // kbps
#define CC1101_FREQ_OFFSET  25.4f    // kHz, FSK deviation
#define CC1101_BW           58.0     // kHz RX filter, >= occupied BW
#define CC1101_TX_POWER     10       // dBm; allowed: -30,-20,-15,-10,0,5,7,10
#define CC1101_PREAMBLE_LEN 16       // bits; 16/24/32/48/64/96/128/192

constexpr int CC1101_CS   = 5;
constexpr int CC1101_GDO0 = 15;
constexpr int RF_SW0      = 13;      // G14 on CardputerZero

// CC1101 PIN order: CSN, GDO0, RST(unused), GDO2
CC1101 radio = new Module(CC1101_CS, CC1101_GDO0, RADIOLIB_NC, RADIOLIB_NC);

int state = radio.begin(CC1101_FREQ, CC1101_BIT_RATE, CC1101_FREQ_OFFSET,
                        CC1101_BW, CC1101_TX_POWER, CC1101_PREAMBLE_LEN);
```

Note both `RST` and `GDO2` are passed as `RADIOLIB_NC`: **the CC1101 has no reset pin**
(it is reset by an SPI strobe), and `GDO2` is not available to RadioLib as an interrupt
because the board uses it for band selection. The guide states the remaining SPI pins are
mapped automatically: *"The CC1101 SPI pins are G5 (CS), G14 (MOSI), G39 (MISO), G40 (SCK),
with G15 (GD0) as the interrupt pin."*

Receive side reports `RSSI`, `SNR` and **`LQI`** — the guide's sample output is
`[CC1101] RSSI: -23.00 dBm / SNR: -25.00 dB / LQI: 2`.

> ⚠ **SPI mode collision.** M5Stack's NFC example configures the shared bus for **mode 1**
> at 10 MHz. RadioLib drives the CC1101 in its own default mode. Anything using both chips
> must re-establish the SPI configuration per transaction. Neither vendor example does
> both at once, so **nobody has demonstrated the combination** — see
> [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).

## 5. Minimal transmit / receive

TX: set the band (see [`band-switching.md`](band-switching.md)), then
`radio.setPacketSentAction(cb); radio.startTransmit("...")`, and `radio.finishTransmit()`
in the callback. RX: `radio.setPacketReceivedAction(cb); radio.startReceive();` then
`radio.readData(...)`. Standard RadioLib. `not-tested`.

## 6. Resources consumed

| Resource | Value |
|---|---|
| Host GPIO | **3 dedicated** — G5 (`CS`), G15 (`GDO0`), G13/G14 (`RF_SW0`) — plus 3 shared SPI |
| Second switch control | **none** — `RF_SW1` is the CC1101's own `GDO2` |
| Power | `VDD_3V3` from `U1`, gated by `POWER_EN` ← host **G3** |

## 7. Legality by band — this one genuinely matters

| Band | Typical status |
|---|---|
| **315 MHz** | US/JP remote-control allocation. **Not an EU ISM band** |
| **433 MHz** | ISM in ITU Region 1 (EU) and widely tolerated elsewhere; **amateur allocation in some regions** |
| **868 MHz** | EU SRD, duty-cycle limited |
| **915 MHz** | US/AU ISM. **Not permitted in the EU** |

The board hands you a switch that spans all four and three antennas to match, with **no
region lock, no certification identifier published** by M5Stack, and firmware examples that
default to **915.0 MHz**. A European user running the shipped example transmits out of
band. This is a genuine, foreseeable compliance hazard and it is worth saying plainly:
**pick the band deliberately, in code, per deployment region.** Nothing in the vendor
material does this for you.

The board's headline use — *"Copy/read/transmit signals on the specified frequencies, and
jam"* (u/No_Confusion7932, [r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/))
— is, in the "jam" case, illegal essentially everywhere. Recorded because it is what the
community says the board is for. **[COM]**

## 8. Conflicts and simultaneous use

| Combination | Verdict |
|---|---|
| CC1101 + NFC | ⚠ shared SPI, **different modes** — [`nfc.md` §8](nfc.md) |
| CC1101 + microSD | ⚠ shared SPI with the host's card slot (CS = G12) |
| CC1101 + Wi-Fi/BLE | ✅ different bands |
| CC1101 + LoRa | ❌ **not on the same host** — only one Cap slot, and the CC1101 cannot do LoRa anyway |
| CC1101 + Grove sensor | ✅ different bus |

## 9. Porting checklist — adding a CC1101 to other firmware

**Hardware:**

| Resource | Count | Notes |
|---|---|---|
| SPI SCK/MOSI/MISO | 3 | shareable |
| `CSN` | 1 | dedicated |
| `GDO0` | 1 | packet interrupt / data line. A series resistor (330 Ω here) is cheap insurance |
| `GDO2` | 0–1 | **free general-purpose output if you do not need a second interrupt** — this board spends it on band select. That trick is the most reusable idea here |
| Reset | **0** | The CC1101 has no reset pin; `SRES` is an SPI strobe |
| 26 MHz crystal | 1 | 12 pF load caps here |
| `RBIAS` resistor | 1 | 56 kΩ here; it sets the internal bias current and is not optional |
| Balun + match | 1 set | Single band: one narrowband match. Multi-band: wideband balun + switched paths, as here |
| Antenna | 1 | |

**Software:** **RadioLib** (MIT) covers the CC1101 with the same API shape as the SX1262 —
so a firmware that already carries RadioLib for LoRa gets CC1101 support for the cost of
one more class. That is a genuinely useful fact for the wider project: **one library,
both radios.**

`new Module(csn, gdo0, RADIOLIB_NC /*rst*/, gdo2_or_NC)` then
`begin(freq, bitrate, freqDev, rxBw, power, preambleLen)`.

**What is board-specific:** pin numbers, the `POWER_EN` gate, the band-switch truth table,
and the LC values of the three band paths (tuned to this PCB).

## 10. Unresolved

- The on-sheet RF-switch truth table could not be transcribed from the PDF text layer; the
  table in §3 of the [README](../README.md) comes from the **product page and Arduino
  guide**, which agree with each other and with the community announcement.
- `B0310J50100AHF` is decoded as a **300–1000 MHz, 50 Ω↔100 Ω balun** from the part-number
  pattern. **`inferred` — no datasheet was located.** See the component record.
- No measurement of output power, sensitivity, harmonic content or inter-band isolation.
- No demonstrated firmware for this Cap yet — Bruce and others will need band-switch
  support added, as the community noted on release day.

## Applicability

| Field | Value |
|---|---|
| Hardware | Cap **U219**, schematic **V0.3 / 2026-05-28** |
| Software | RadioLib ≥ 7.x. **`RF_SW0` = G13 on Cardputer-Adv, G14 on CardputerZero** |
| Evidence | Pin map: schematic + vendor guide + vendor pin-map, three-way. RF values: schematic text layer. Performance: **vendor claim only** |
| Last verified | 2026-09-04 |
