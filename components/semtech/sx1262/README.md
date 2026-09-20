# Semtech SX1262

> **Common guide:** [`guides/lora`](../../../guides/lora/README.md) — the device-independent LoRa material (LoRa vs LoRaWAN vs Meshtastic, the SF/airtime/duty-cycle trade, regional band plans as a legal constraint, BUSY/TCXO/DIO handling and the LDO-vs-DC-DC current cost). This record covers the part; that guide covers the domain.

- **Category:** sub-GHz **LoRa® / LR-FHSS / (G)FSK radio transceiver**, SPI-controlled, 150–960 MHz, **+22 dBm** high-power PA
- **Package:** QFN 4 × 4 mm, 24 leads plus exposed pad (`SX1262IMLTRT`)
- **Scope of this record: the chip only.** On the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) the SX1262 is **not on the main board** — it is inside the [`Stamp LoRa-1262`](../../m5stack/stamp-lora-1262/README.md) plug-in module, and everything at or above the module's 13-pin boundary (host wiring, reset, antenna switch, power gating, bring-up order) belongs to that record. Read it for the board; read this for the silicon.
- **Research status:** the **full Semtech datasheet is retained** (`DS.SX1261-2.W.APP`, Rev 2.2, 118 pp) and was read. **No module datasheet exists anywhere** — see [§10-G1](#10-caveats-gaps-and-errata). The chip has never been seen directly: no teardown photograph, no probe, no measurement.
- **Retrieved:** 2026-09-01

**The [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) does not have it.** LoRa and NFC together are the entire difference between the two SKUs.

---

## ⚠ This datasheet covers two parts, and the differences are the whole story

`DS.SX1261-2` documents the **SX1261 and SX1262 together**. They share a die family, a pinout, a command set and a register map; they differ almost entirely in the power amplifier — and a claim copied from the wrong column is the most common error made with this document.

| | **SX1261** | **SX1262** ← *the one in the Stamp module* |
|---|---|---|
| Maximum RF output power | **+14 dBm** nominal, **+15 dBm** with special settings | **+22 dBm** |
| `SetTxParams` power range | **−17 to +14 dBm** (`0xEF`…`0x0E`) | **−9 to +22 dBm** (`0xF7`…`0x16`) |
| PA supply | `VDD_IN` (pin 1) connected to **`VREG`** (pin 7) | `VDD_IN` (pin 1) connected to **`VBAT`** (pin 10) |
| `SetPaConfig` `deviceSel` | **`0x01`** | **`0x00`** |
| `hpMax` | no effect | selects PA size; **`0x07`** for +22 dBm |
| Over-current protection after `SetPaConfig` | **60 mA** (`0x18`) | **140 mA** (`0x38`) |
| TX current at 868/915 MHz, full power | 25.5 mA @ +14 dBm | **118 mA @ +22 dBm** |
| DC-DC scope | whole IC | **IC core only — the PA is supplied from `VBAT`** |
| Order code | `SX1261IMLTRT` | **`SX1262IMLTRT`** |
| Ordering | QFN, tape and reel, MOQ 3 000 | idem |

**[DS]** §3.5.4 Table 3-9, §13.1.14 Tables 13-20/13-21, §13.4.4, §5.1 Table 5-2, §3.5.1 Table 3-6, Ordering Information.

**Everything below describes the SX1262** unless a row explicitly contrasts the two.

Two independent lines of evidence say the fitted part really is the **62**, not the 61:

1. The module is named `Stamp-LoRa-**1262**-mini` on the schematic and `Stamp LoRa-**1262**` in M5Stack's specification table, and its own pin names are `SX_NRST`, `SX_NSS`, `SX_BUSY`, `SX_ANT_SW` **[SCH]**, **[DOC]**.
2. The factory firmware asks RadioLib for **22 dBm** and instantiates the `SX1262` class **[SRC]** `hal_lora.cpp:37`, `:328`. **+22 dBm is unreachable on an SX1261** — its `SetTxParams` range stops at +14, and RadioLib would reject or clamp it.

Neither is a photograph of the die. `inferred`, but strongly.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Stated in `artifacts/sx1261-2-datasheet-v2.2-m5stack-mirror.pdf` (Rev 2.2), with section/table reference | `not-tested` — manufacturer specification reproduced; nothing measured |
| **[SCH]** | Read out of `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet 4, designator `U14` | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | Read out of M5Stack source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | `docs.m5stack.com` / `semtech.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference | `inferred` |

**Nothing in this record was verified on hardware, by anyone whose report could be located.** No register value, opcode or pin below was guessed.

**Text-layer validation.** `pdftotext -layout` output was checked against the document's own running footers (`SX1261/2 · Data Sheet · Rev 2.2 · DS.SX1261-2.W.APP · Dec 2024`) and page numbering before transcription. ⚠ **One real defect was found and is worth knowing about**: the *figure* fonts carry a **uniform +31 code-point offset**, so block-diagram labels extract as human-legible but wrong text — `-P3B¥` for `LoRa®`, `.PEFN` for `Modem`, `41*` for `SPI`. This is exactly the failure mode that looks fine and is not. **Body text, tables and headings are unaffected**, and every value in this record comes from body text or a table. Recorded so the next reader does not transcribe a figure label.

---

## 1. Identity and capability

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Semtech Corporation** | **[DS]** cover |
| Part | **SX1262** — "Long Range, Low Power, sub-GHz RF Transceiver" | **[DS]** cover |
| Document | **`DS.SX1261-2.W.APP`, Rev 2.2, December 2024**, 118 pp | **[DS]** cover, revision history |
| Order code | **`SX1262IMLTRT`**, QFN, tape and reel, 3 000 pcs MOQ, Pb-free / halogen-free / RoHS | **[DS]** Ordering Information |
| Package | **QFN 4 × 4 mm, 0.5 mm pitch, 24 leads + exposed ground pad** | **[DS]** §2.1, §16.1 |
| **Synthesizer frequency range** | **150 – 960 MHz, continuous** | **[DS]** Table 3-7 |
| Modulations | **LoRa®**, **LR-FHSS** (TX only), **(G)FSK** 0.6 – 300 kb/s (2-FSK to 500 kb/s in RX specs) | **[DS]** §6 |
| Host interface | **SPI**, mode 0 (CPOL = 0, CPHA = 0), **up to 16 MHz**, slave only | **[DS]** §8.2 |
| Supply `VBAT` / `VBAT_IO` | **1.8 – 3.7 V** | **[DS]** Table 3-3 |
| Reference | 32 MHz crystal **or** an external TCXO powered from `DIO3` | **[DS]** §4.1 |
| Data buffer | 256 bytes, shared TX/RX with programmable base addresses | **[DS]** §7 |
| ⚠ Marking verified? | **No.** The chip is inside a module; no teardown photograph exists (§10-G1) | **[INF]** |

Semtech positions it for smart meters, logistics, building automation, agriculture, asset tracking, street lighting and environmental sensing, and states compliance intent for **ETSI EN 300 220, FCC CFR 47 Part 15, Chinese regulations and Japanese ARIB T-108** **[DS]** General Description.

> ⚠ **LR-FHSS is patent-encumbered.** Semtech's own disclaimer on page 2: using Semtech's LR-FHSS software "does not grant any rights to their patents for LR-FHSS technology"; rights are available "by purchasing Semtech SX1261, SX1262, SX1268, or LR11xx semiconductor devices, or their authorized counterparts". Worth knowing before designing a product around it. **[DS]** p. 2.

### 1.1 150–960 MHz silicon versus an 868–923 MHz module

The **chip** covers 150–960 MHz continuously. The **module** M5Stack fits is advertised at **868 – 923 MHz**, one wideband SKU with no regional variant **[DOC]**.

That narrowing is not a chip limitation — it is the module's matching network and antenna, neither of which is documented anywhere ([§10-G1](#10-caveats-gaps-and-errata)). Do not read the datasheet's 150 MHz floor as something you can use on this board.

Note also that the datasheet's own performance figures are quoted at **434 / 490 / 868 / 915 MHz** with "all RF impedances matched" **[DS]** §3.5, so even the 868–923 range is only as good as a matching network nobody has seen. And the PA settings interact with matching directly: `paDutyCycle` "will affect the distribution of the power in the harmonics and should thus be selected to work in conjunction of a given matching network" **[DS]** §13.1.14. Changing `paDutyCycle` on this module is therefore not a software-only decision.

---

## 2. Pin table

**[DS]** §2.1, Table 2-1. The "brought out by the module?" column is from the [Stamp-LoRa-1262 record](../../m5stack/stamp-lora-1262/README.md) §2 and is `inferred` by name matching — the module has no datasheet.

| Pin | Name | Type | Function | Reaches the PaperMono? |
|---:|---|---|---|---|
| 0 | `GND` | — | Exposed ground pad | — |
| 1 | `VDD_IN` | I | PA regulator input, `VR_PA`. **SX1261: tie to pin 7. SX1262: tie to pin 10** | internal |
| 2 | `GND` | — | Ground | — |
| 3 | `XTA` | — | Crystal connection; can take an external reference clock | internal |
| 4 | `XTB` | — | Crystal connection | internal |
| 5 | `GND` | — | Ground | — |
| 6 | **`DIO3`** | I/O | Multi-purpose digital I/O — **or external TCXO supply** | **internal — not brought out** (§5.2) |
| 7 | `VREG` | O | Regulated output of the internal LDO / DC-DC | internal |
| 8 | `GND` | — | Ground | — |
| 9 | `DCC_SW` | O | DC-DC switcher output | internal |
| 10 | `VBAT` | I | Supply for the RFIC | module pin 5 `VIN_3V3` (3.3 V) |
| 11 | `VBAT_IO` | I | Supply for the digital I/O pins **except `DIO3`** | internal |
| 12 | **`DIO2`** | I/O | Multi-purpose digital I/O — **or RF switch control** | **internal — not brought out** (§5.3) |
| 13 | **`DIO1`** | I/O | Multi-purpose digital I/O — the generic IRQ line | **module pin 4 `LORA_IRQ`** → ESP32-S3 GPIO5 |
| 14 | **`BUSY`** | O | Busy indicator | **module pin 3 `SX_BUSY`** → ESP32-S3 GPIO21 |
| 15 | `NRESET` | I | Reset, active low | module pin 2 `SX_NRST` → **M5IOE1 `IO10`** |
| 16 | `MISO` | O | SPI slave output | module pin 8 → ESP32-S3 GPIO40 |
| 17 | `MOSI` | I | SPI slave input | module pin 7 → ESP32-S3 GPIO38 |
| 18 | `SCK` | I | SPI clock | module pin 6 → ESP32-S3 GPIO39 |
| 19 | `NSS` | I | SPI slave select | module pin 9 `SX_NSS` → ESP32-S3 GPIO41 |
| 20 | `GND` | — | Ground | — |
| 21 | `RFI_P` | I | RF receiver input | internal |
| 22 | `RFI_N` | I | RF receiver input | internal |
| 23 | `RFO` | O | **RF transmitter output** — SX1261 low-power PA or **SX1262 high-power PA** | internal → FPC antenna |
| 24 | `VR_PA` | — | Regulated power-amplifier supply | internal |

Three consequences of that last column, all of which shape how you drive this board:

- **Only `DIO1` leaves the module.** The module's `LORA_IRQ` is `DIO1` specifically — not a wired-OR of the DIOs — confirmed by the firmware naming the same line `LORA_DIO1_PIN` **[SRC]** `hal_lora.cpp:27`. `DIO2` and `DIO3` are consumed inside the module (§5).
- **`NRESET` is behind an I²C expander**, so RadioLib is handed `RADIOLIB_NC` for reset and never resets the radio itself **[SRC]** `hal_lora.cpp:327`.
- **`DIO3` is referenced to `VBAT`, not `VBAT_IO`** — the datasheet flags it explicitly in a footnote to the digital I/O table **[DS]** Table 3-10 note 1. That is because `DIO3` doubles as a *regulated supply output* (§5.2), not merely a logic pin.

---

## 3. Modems

### 3.1 LoRa

Spread-spectrum with forward error correction, configured through `SetModulationParams` after `SetPacketType`. Four parameters **[DS]** §6.1.1:

| Parameter | Range | Effect |
|---|---|---|
| **Spreading factor** `SF` | **5 – 12** | 2^SF chips/symbol. Symbol rate `Rs = BW / 2^SF` |
| **Bandwidth** `BW_L` | 7.81 – 500 kHz | Higher = faster, less sensitive |
| **Coding rate** `CR` | 4/5 – 4/8 | FEC overhead |
| **Low data-rate optimize** `LDRO` | 0 / 1 | Relaxes the allowed frequency drift by **16×** |

Demodulator SNR by spreading factor **[DS]** Table 6-1:

| SF | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|
| chips/symbol | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 |
| typical SNR (dB) | −2.5 | −5 | −7.5 | −10 | −12.5 | −15 | −17.5 | **−20** |

> ⚠ **SF5 and SF6 are not backward compatible.** Both were modified in the SX1261/2 and now work in implicit *and* explicit mode, but **SF6 here is not interoperable with SF6 on an SX1276**. For SF5/SF6, use **12 preamble symbols** rather than the usual 8 **[DS]** §6.1.1.1. Spreading factors are orthogonal, so both ends must agree in advance.
>
> Semtech also recommends 12 preamble symbols generally for optimal performance — added in datasheet Rev 1.1.

⚠ **Not every SF is available at every bandwidth** — Table 6-1 carries the footnote "Not all SF are available for any bandwidth with the SX1261/2" without enumerating which. An unresolved documentation gap in Semtech's own datasheet.

**Frequency drift matters at low data rates.** With `LDRO = 0`, total drift across a packet must stay under `Freq_drift_max`; `LDRO = 1` relaxes that 16-fold. This is the mechanism that makes a **TCXO** worthwhile in a miniaturised design where heat cannot be kept away from the crystal — and Semtech says so in as many words **[DS]** §4.1.2. See §5.2.

### 3.2 (G)FSK

2-FSK, 0.6 – 300 kb/s (RX specifications go to 500 kb/s), with selectable Gaussian pulse shaping and a sigma-delta fractional-N modulator giving fine deviation control **[DS]** §6.2. The demodulator bandwidth must satisfy:

```
2 × Fdev + BR  <  BW
```

Packet handling includes preamble detection, sync word up to 8 bytes, node/broadcast address filtering, fixed- or variable-length packets, CRC with programmable initial value and polynomial, and data whitening.

### 3.3 LR-FHSS

Long Range Frequency Hopping Spread Spectrum — **transmit only** on this part, aimed at very high node density **[DS]** §6.3. Patent-encumbered (§1).

### 3.4 Data buffer

A single **256-byte** buffer shared between TX and RX, with independent base addresses set by `SetBufferBaseAddress` **[DS]** §7. That is the origin of the 255-byte maximum packet the vendor firmware enforces **[SRC]** `hal_lora.cpp:42`.

---

## 4. The SPI command interface

### 4.1 Electrical and timing

**[DS]** §8.2: mode 0 (CPOL = 0, CPHA = 0), MSB first, slave only. MOSI is generated by the master on the SCK **falling** edge and sampled by the slave on the **rising** edge; MISO is generated on the falling edge. NSS low frames the transaction; MISO is high-Z while NSS is high. **Up to 16 MHz.**

Key timings, all at ≤10 pF load **[DS]** Table 8-1:

| Symbol | Meaning | Min |
|---|---|---|
| `t1` | NSS falling → SCK setup | 32 ns |
| `t2` | SCK period | 62.5 ns (⇒ 16 MHz) |
| `t8` | SCK → NSS rising hold | 31.25 ns |
| `t9` | **NSS high time** | **125 ns** |
| **`t10`** | **NSS falling → SCK when leaving SLEEP** | **100 µs** |
| `t11` | NSS falling → MISO when leaving SLEEP | ≤ 150 µs |

⚠ `t10` is the trap: **the first SPI clock after waking from sleep must wait 100 µs after NSS falls**, because the chip is bringing up its regulators. A driver that treats a sleep wake like an ordinary transaction will lose the first command. The correct approach is to watch `BUSY` (§4.3).

The PaperMono runs this bus at **8 MHz**, half the maximum **[SRC]** `hal_lora.cpp:31`.

### 4.2 Command structure

Every transaction is an **opcode byte** followed by parameters and/or returned status **[DS]** §10, §11. There is no register-address protocol in the usual sense — registers are reached through `WriteRegister` (`0x0D`) and `ReadRegister` (`0x1D`) with a 16-bit address, and the packet buffer through `WriteBuffer` (`0x0E`) / `ReadBuffer` (`0x1E`).

The commands that matter most **[DS]** Tables 11-1 to 11-5:

| Opcode | Command | Note |
|---|---|---|
| `0x84` | `SetSleep` | Cold start (no retention) vs warm start (configuration retained) |
| `0x80` | `SetStandby` | `STDBY_RC` (13 MHz RC) or `STDBY_XOSC` |
| `0xC1` / `0x83` / `0x82` | `SetFs` / `SetTx` / `SetRx` | `SetTx`/`SetRx` take a 24-bit timeout |
| `0x94` | `SetRxDutyCycle` | The low-power listen mode |
| `0xC5` | `SetCad` | Channel activity detection |
| `0x96` | `SetRegulatorMode` | LDO or DC-DC. **`STDBY_RC` only** |
| `0x89` / `0x98` | `Calibrate` / `CalibrateImage` | |
| **`0x95`** | **`SetPaConfig`** | **The command that differentiates SX1261 from SX1262** |
| `0x93` | `SetRxTxFallbackMode` | Where the chip lands after TX/RX done |
| `0x08` | `SetDioIrqParams` | Four 16-bit masks: global + one per DIO |
| `0x12` / `0x02` | `GetIrqStatus` / `ClearIrqStatus` | |
| **`0x9D`** | **`SetDIO2AsRfSwitchCtrl`** | §5.3 |
| **`0x97`** | **`SetDIO3AsTcxoCtrl`** | §5.2 |
| `0x86` / `0x8A` / `0x8E` | `SetRfFrequency` / `SetPacketType` / `SetTxParams` | |
| `0x8B` / `0x8C` | `SetModulationParams` / `SetPacketParams` | |
| `0xC0` / `0x13` / `0x14` / `0x15` | `GetStatus` / `GetRxBufferStatus` / `GetPacketStatus` / `GetRssiInst` | |
| `0x17` / `0x18` | `GetDeviceErrors` / `ClearDeviceErrors` | |

`SetPacketType` must be called **before** `SetModulationParams` and `SetPacketParams`, because the parameter encodings differ per modem. **[DS]** §13.4.5. `SetRegulatorMode` is only valid in `STDBY_RC`. Semtech devotes a whole section, §14.5, to "Issuing Commands in the Right Order" — the ordering is not incidental.

### 4.3 `BUSY` — a mandatory handshake, not a status LED

**[DS]** §8.3.1, and this is the single most important behavioural fact about the part:

> When the BUSY line is held low, it indicates that the internal state machine is in idle mode and that the radio is ready to accept a command from the host controller.

- **Every "write" command raises `BUSY`** after `T_SW`, which is **≤ 600 ns** from the NSS rising edge in all cases. The host must wait for `BUSY` to fall before the next command.
- **"Read" commands do not raise `BUSY`** — they are handled without the state machine.
- **`BUSY` also rises to service the chip's own internal interrupts.** Semtech: "it is essential to wait for the BUSY line to go low before sending an SPI command (either a 'read' or a 'write' command)." So the read exemption is not a licence to ignore the line.
- **In sleep, `BUSY` is held high through a 20 kΩ resistor** and falls as soon as the chip leaves sleep — which is the correct, timing-independent way to satisfy `t10` (§4.1).
- `BUSY` falls at meaningfully different moments per mode: in **FS** when the PLL locks; in **RX** when the receiver is up; in **TX** when the PA has ramped and preamble transmission starts.

Mode-transition times, NSS rising to `BUSY` falling **[DS]** Table 8-2:

| Transition | µs |
|---|---:|
| **SLEEP → STDBY_RC, cold start (no retention)** | **3500** |
| **SLEEP → STDBY_RC, warm start (retention)** | **340** |
| STDBY_RC → STDBY_XOSC | 31 |
| STDBY_RC → FS / RX / TX | 50 / 83 / **126** |
| STDBY_XOSC → FS / RX / TX | 40 / 62 / 105 |
| FS → RX / TX | 41 / 76 |
| RX → FS / TX | 15 / 92 |

**A cold-start wake costs 3.5 ms — ten times a warm start.** On a duty-cycled battery node that is the difference between viable and not, and it is the reason `SetSleep`'s retention flag exists.

⚠ **Add the TCXO delay to every one of these** if `DIO3` supplies a TCXO (§5.2).

### 4.4 Interrupts

Ten sources, each maskable and each mappable to any of `DIO1`, `DIO2` or `DIO3` **[DS]** §8.5, Table 8-4:

| Bit | IRQ | Modulation |
|---:|---|---|
| 0 | `TxDone` | all |
| 1 | `RxDone` | all |
| 2 | `PreambleDetected` | all |
| 3 | `SyncWordValid` | FSK |
| 4 | `HeaderValid` | LoRa |
| 5 | `HeaderErr` | LoRa |
| 6 | `CrcErr` | all |
| 7 | `CadDone` | LoRa |
| 8 | `CadDetected` | LoRa |
| 9 | `Timeout` | all |

`DIO1` is described as "the generic IRQ line, any interrupt can be mapped to DIO1" — which is exactly why a module that brings out only one DIO brings out `DIO1`.

Pin states per mode are worth knowing when the chip is asleep **[DS]** Table 8-3: in **Reset, Start-up and Sleep** all three DIOs are **pulled down** (50 kΩ) and `BUSY` is **pulled up**; only from `STDBY_RC` upward do they become real outputs. A DIO used for an external function is therefore *not* driven while the chip sleeps — relevant to both TCXO and RF-switch control.

---

## 5. `DIO2` and `DIO3` — the two pins that are not really I/O

### 5.1 Why this matters on a module

Both pins have a second personality, both are configured by a single command, and **both are consumed inside the Stamp module where they cannot be observed**. Getting either wrong produces a radio that initialises cleanly and then does not work — the hardest class of fault to diagnose.

### 5.2 `DIO3` as a TCXO supply

**[DS]** §8.3.2, §13.3.6. `SetDIO3AsTcxoCtrl(tcxoVoltage, delay[23:0])` (opcode `0x97`) hands `DIO3` to the internal state machine, which then **drives it to a programmed voltage whenever the reference is needed** — in `STDBY_XOSC`, `FS`, `TX` and `RX` — and power-cycles the TCXO the rest of the time.

| `tcxoVoltage` | `DIO3` output |
|---|---|
| `0x00` – `0x02` | 1.6 / 1.7 / 1.8 V |
| `0x03` – `0x05` | 2.2 / 2.4 / 2.7 V |
| **`0x06`** | **3.0 V** |
| `0x07` | 3.3 V |

Precision is roughly ±50 mV (quoted for the 1.8 V setting). ⚠ **The regulator targets 200 mV below the supply**, so the datasheet states the constraint as **`VDDop > VTCXO + 200 mV`**. With a 3.3 V module supply and a 3.0 V setting the margin is exactly 300 mV — inside the rule, but with only 100 mV to spare over a rail that also feeds the PA. Worth knowing before assuming headroom.

`delay(23:0)` is in units of **15.625 µs** and gates the 32 MHz clock until the TCXO has settled. If 32 MHz is not detected by the end of the delay, **`XOSC_START_ERR`** is raised. Two behaviours around that flag catch people:

- **`XOSC_START_ERR` is raised at POR and at every cold-start sleep wake when a TCXO is used**, because the chip does not yet know it is TCXO-clocked. Semtech: *"It is an expected behaviour... The user should simply clear this flag with the ClearDeviceErrors command."* An error handler that treats it as fatal will refuse to start a perfectly good radio.
- **The delay is added to every STDBY_RC → TX/RX transition.** To avoid paying it on each packet, go to `STDBY_XOSC` first, wait once, then move to TX or RX.

There is also a **side effect on the crystal trimming caps**: issuing `SetDIO3AsTcxoCtrl` automatically forces the `XTA` internal cap register to `0x2F` (33.4 pF) "to filter any spurious transitions which could occur and be propagated to the PLL" **[DS]** §4.1.3.

`DIO3` can alternatively be driven as a **plain switched output** through raw register writes to `0x0580`, `0x0583`, `0x0584`, `0x0585` and `0x0920` **[DS]** §8.6 — and that configuration **is overwritten by the state machine at POR and on every wake from sleep**, so it must be re-applied each time.

#### 5.2.1 The PaperMono evidence: `LORA_TCXO_VOLTAGE = 3.0f` — `inferred`

**This is not a datasheet fact about this board, and it is not a measurement. It is an inference from vendor firmware, and it is labelled `inferred` deliberately.**

```cpp
static constexpr float LORA_TCXO_VOLTAGE = 3.0f;          // hal_lora.cpp:40
...
radio->begin(868.0f, 62.5f, 12, 8, 0x34, 22, 10,
             LORA_TCXO_VOLTAGE, LORA_USE_REGULATOR_LDO);   // hal_lora.cpp:333-334
```

RadioLib's `SX126x::begin(..., tcxoVoltage, useRegulatorLDO)` maps a non-zero `tcxoVoltage` onto `SetDIO3AsTcxoCtrl`, and **3.0 V is `tcxoVoltage = 0x06`** in Semtech's table above.

What that supports, and what it does not:

- ✅ **The vendor firmware configures `DIO3` as a 3.0 V TCXO supply.** `executed-success` for the source read.
- ✅ **Therefore M5Stack believes a TCXO is fitted inside the module**, since configuring a TCXO supply on a crystal-only design is at best pointless and at worst harmful.
- ❌ **It does not prove a TCXO is physically present.** No module datasheet, no photograph, no measurement. The module could carry a plain 32 MHz crystal and the firmware could be wrong-but-working, or wrong-and-marginal.
- ❌ **It does not establish which TCXO, its stability, or its start-up time.** The `delay` RadioLib passes was not traced.

This is the same conclusion the [Stamp-LoRa-1262 record reaches at §5-G3](../../m5stack/stamp-lora-1262/README.md), which warns that getting TCXO configuration wrong yields a radio that "appears to initialise and then fails to transmit or receive". **Its advice stands: do not change this value blindly.** `3.0f` is the value the shipped firmware uses; treat it as the known-good starting point and change it only with a spectrum analyser to hand.

### 5.3 `DIO2` as RF switch control

**[DS]** §8.3.2, §13.3.3. `SetDIO2AsRfSwitchCtrl(enable)` (opcode `0x9D`) makes `DIO2` **high during TX and low in every other mode** — a one-line antenna-path selector for a design with separate TX and RX paths, or a single SPDT switch.

The datasheet devotes §14.6.1 and §14.6.2 to application schematics of exactly this ("Application Design of the SX1261/SX1262 **with RF Switch**"), so it is the expected topology rather than an exotic one. When the paths are *not* split — a "direct tie connection between Rx and Tx" — sensitivity is measurably worse: **−133 dBm instead of −137 dBm** for LoRa at BW 125 kHz / SF12, and −115 vs −118 dBm for 2-FSK at 4.8 kb/s **[DS]** Table 3-8. **A 4 dB link-budget penalty** is the price of omitting the switch.

Note also that the datasheet's headline receive figures assume "split RF paths for Rx and Tx, **RF switch insertion loss excluded**" — so real-world numbers sit below them by the switch's loss.

#### 5.3.1 The PaperMono evidence, and the two switches that are not the same thing

```cpp
s_lora.radio->setDio2AsRfSwitch(true);     // hal_lora.cpp:343
```

**[SRC]**, `executed-success` for the read. So the vendor firmware tells the SX1262 to drive an RF switch from `DIO2`, and `DIO2` never leaves the module — meaning **the switch it drives is inside the module**. `inferred`.

⚠ **That is emphatically not the same signal as the module's `SX_ANT_SW` pin.** The module brings out a separate `SX_ANT_SW` on pin 10, wired to **M5IOE1 `IO2`**, which the firmware sets HIGH once during bring-up and never touches again **[SRC]** `hal_lora.cpp:314`, `:319`. Its semantics are undocumented — whether it selects TX/RX paths, enables a PA/LNA, or picks between antenna connectors is stated nowhere, and remains [open question G4 in the module record](../../m5stack/stamp-lora-1262/README.md).

So this board has **two** antenna-switch controls: one automatic and internal (`DIO2`), one manual and external (`SX_ANT_SW`). Conflating them is an easy and expensive mistake.

### 5.4 Regulator choice, and what the PaperMono firmware gives up

**[DS]** §5.1. Two regulation modes, selected by `SetRegulatorMode` **in `STDBY_RC` only**:

| Mode | Sleep | STDBY_RC | STDBY_XOSC / FS / RX / TX |
|---|---|---|---|
| Regulator type **0** (LDO) | — | LDO | **LDO** |
| Regulator type **1** (DC-DC) | — | LDO | **DC-DC + LDO** |

DC-DC needs two external inductors — 47 nH before pin 1 and 15 µH between pins 7 and 9 — so LDO-only operation exists precisely to save that BOM and board area. On the **SX1262** the DC-DC covers the IC core only; **the PA is supplied from `VBAT` either way**, so DC-DC does not reduce transmit current at all.

Where it does matter is **receive**, and the difference is large **[DS]** Table 3-5:

| Mode | DC-DC | **LDO** |
|---|---:|---:|
| RX, FSK 4.8 kb/s | 4.2 mA | **8.0 mA** |
| RX, LoRa 125 kHz | 4.6 mA | **8.8 mA** |
| RX boosted, LoRa 125 kHz | 5.3 mA | **10.1 mA** |
| Synthesizer (FS) | 2.1 mA | 3.55 mA |

**The PaperMono firmware selects LDO** — `LORA_USE_REGULATOR_LDO = true` **[SRC]** `hal_lora.cpp:41`, passed as `begin()`'s last argument. **Receive current is therefore roughly double what the datasheet's headline "4.2 mA active receive" figure suggests**, and that headline is the first sentence of Semtech's own General Description.

Whether that is a considered choice or a default is unknown. The likeliest reading is that **the module simply does not fit the DC-DC inductors** — they are the exact components §5.1 says LDO-only operation exists to omit, and a "Stamp"-format module is space-constrained. `inferred`, and it would be settled by a photograph of the module. For a battery product that spends its life in receive, this is the single most consequential unverified fact about the radio on this board.

---

## 6. Power and RF performance

### 6.1 Current

**[DS]** Tables 3-5 and 3-6, at 25 °C, `VBAT = VBAT_IO = 3.3 V`, TCXO and RF-switch consumption **excluded**.

| Mode | Typical |
|---|---:|
| **OFF (sleep, cold start)** | **160 nA** |
| Sleep, configuration retained | 600 nA |
| Sleep, retained + RC64k running | 1.2 µA |
| `STDBY_RC` | 0.6 mA |
| `STDBY_XOSC` | 0.8 mA |
| RX — see §5.4 for the LDO/DC-DC split | 4.2 – 10.1 mA |

Transmit, **SX1262 at 868/915 MHz** with the +22 dBm PA match:

| Output | Typical |
|---|---:|
| **+22 dBm** | **118 mA** |
| +20 dBm | 102 mA |
| +17 dBm | 95 mA |
| +14 dBm | 90 mA |

With the PA re-optimised for a lower target (a different `paDutyCycle`/`hpMax` *and* a different matching network), the same output costs far less: +20 dBm → 84 mA, +17 dBm → 58 mA, +14 dBm → **45 mA**. Half the current at +14 dBm — but only with the matching network to match, which is not a software change (§1.1).

**The PaperMono firmware asks for +22 dBm**, i.e. ~118 mA in transmit, on a rail supplied by an LDO rated 400 mA that also feeds nothing else **[SRC]**, [module record](../../m5stack/stamp-lora-1262/README.md). Nobody has measured it.

### 6.2 Over-current protection

`SetPaConfig` **automatically reprograms OCP** (register `0x08E7`): `0x18` = 60 mA after POR, and **`0x38` = 140 mA once `deviceSel` selects the SX1262** **[DS]** Table 5-2. Range is 6 bits in 2.5 mA steps, max 157.5 mA. Any manual OCP change must come **after** `SetPaConfig`, or it is overwritten.

The PaperMono firmware calls `setCurrentLimit(140.0f)` **[SRC]** `hal_lora.cpp:344` — which is **exactly the SX1262 post-`SetPaConfig` default**. So the call re-applies the default rather than changing anything. Harmless, and possibly deliberate belt-and-braces; worth knowing it is not a tuning decision.

### 6.3 Sensitivity

**[DS]** Table 3-8, RX-boosted gain, split RF paths, switch insertion loss excluded:

| LoRa | SF7 | SF12 |
|---|---:|---:|
| BW 10.4 kHz | −134 dBm | **−148 dBm** |
| BW 125 kHz | −124 dBm | −137 dBm |
| BW 250 kHz | −121 dBm | −134 dBm |
| BW 500 kHz | −117 dBm | −129 dBm |

2-FSK ranges from −125 dBm at 0.6 kb/s to −94 dBm at 500 kb/s. LoRa adjacent-channel rejection reaches 72 dB at SF12/125 kHz, and blocking immunity 88–99 dB at 1–10 MHz offset.

With a "direct tie" front end instead of a switch, subtract ~4 dB (§5.3).

### 6.4 Transmit

**[DS]** Table 3-9:

| Parameter | Value |
|---|---|
| Max output, **SX1262** | **+22 dBm** |
| Power range | programmable in **31 steps**, `TXOP−31` to `TXOP` |
| Step accuracy | ±2 dB |
| Ramp time | programmable **10 µs to 3400 µs** (eight settings) |
| TX wake-up time | 36 µs + PA ramping |
| **Output power drop vs `VBAT`, SX1262 at +22 dBm** | **2 dB at 2.7 V · 3 dB at 2.4 V · 6 dB at 1.8 V** |

That last row is a battery-product fact: **an SX1262 asked for +22 dBm delivers +16 dBm on a nearly-flat cell.** On the PaperMono the module runs from a regulated 3.3 V LDO rather than the battery directly, which should avoid it — `inferred`, unmeasured.

### 6.5 Crystal and reference accuracy

**[DS]** §3.4, §4.1.3. 32 MHz, C<sub>LOAD</sub> 10 pF, R<sub>S</sub> ≤ 60 Ω, drive level ≤ 100 µW. **No external load capacitors are needed** — internal trimming caps on `XTA` and `XTB` are adjustable in 0.47 pF steps from 11.3 pF (`0x00`) to 33.4 pF (`0x2F`) via registers `0x0911` / `0x0912`.

⚠ **The trimming caps are overwritten by the state machine.** At POR or cold-start wake they initialise to `0x05` (13.6 pF); on entering `STDBY_XOSC` the state machine forces both to `0x12` (19.7 pF). **You must already be in `STDBY_XOSC` before changing them**, or your value is discarded.

Semtech's system-level guidance: **±30 ppm** overall reference accuracy is expected of a LoRaWAN end device across initial error, temperature drift and lifetime ageing.

⚠ **Thermal coupling is a real design constraint on this part.** §4.1.2: the SX1262 transmits up to +22 dBm from a 4 × 4 mm package, "the circuit may heat up", and "careful PCB design using thermal isolation techniques must be applied between the circuit and the crystal resonator to avoid transferring the heat to the external crystal resonator". In a miniaturised design where that isolation is impossible, Semtech's recommendation is **a TCXO** — which is a coherent reason for the Stamp module to fit one (§5.2).

---

## 7. Operating modes

**[DS]** §9:

| Mode | What is running | Leaves via |
|---|---|---|
| **SLEEP** | Most blocks off; optionally RC64k + timer. **`BUSY` held high** | **NSS going low** (any case), or an RTC end-of-count (Listen mode) |
| **STDBY_RC** | 13 MHz RC oscillator. The configuration mode | command |
| **STDBY_XOSC** | XOSC on. Use when timing is critical, or to pre-pay the TCXO delay | command |
| **FS** | PLL and regulators on. `BUSY` falls when the PLL locks or times out | command |
| **RX** | Front end, RX ADC, selected modem. Continuous / single / single-with-timeout | command, packet, or timeout |
| **TX** | PA ramped; `BUSY` falls when preamble transmission starts | command or timeout |

⚠ **RX and TX frequencies differ.** The SX1261/2 uses a low-IF architecture, so the RX frequency is the TX frequency minus the IF; in FS and TX modes the RF frequency is programmed directly **[DS]** §9.5. `CalibrateImage` exists for this reason and should be run for the band in use.

`SetRxDutyCycle` implements a low-power listen mode by alternating RX and sleep windows under RTC control, and `SetRxTxFallbackMode` chooses where the chip lands after a completed packet — both worth reaching for before hand-rolling a duty cycle in host firmware.

---

## 8. Register-level workarounds you must implement

Semtech publishes four **Known Limitations** in §15. All four are register writes the datasheet says to make, none is optional, and a driver that omits them is subtly wrong rather than obviously broken.

| # | Symptom | Workaround | When to apply |
|---|---|---|---|
| **15.1** | Sensitivity degradation on **any** LoRa receiver when receiving a 500 kHz-bandwidth signal transmitted by an SX1261/2 | **Bit 2 of `0x0889`**: set **0** when LoRa BW = 500 kHz, **1** for any other LoRa BW and for all (G)FSK | **Before every packet transmission** |
| **15.2** | The PA over-voltage clamp is over-protective, backing power off by **5–6 dB** on a "reasonable" antenna mismatch | **`TxClampConfig` bits 4–1 → `1111`** (default `0100`) | **After POR and after every cold-start wake.** SX1262 only |
| **15.3** | In LoRa **implicit-header** RX with timeout, the RTC-based timeout timer is **not stopped on `RxDone`** and can fire spuriously in a later mode | Write `0x0902` to stop the counter and `0x0944` to clear the event | **After any RX-with-timeout sequence** |
| **15.4** | Packet loss on longer packets when using **inverted IQ** | **Bit 2 of `0x0736`**: **0** for inverted IQ, **1** for standard IQ | Whenever IQ polarity is set |

Two are worth dwelling on for this board:

- **15.2 is an SX1262-specific fix with a 5–6 dB effect** — larger than most antenna decisions. Semtech is careful to say the workaround "improves chip functionality, but is not required to ensure long-term reliability", i.e. it is safe to apply. RadioLib is generally good about these; **whether the pinned 7.2.1 applies all four was not verified in this pass** and is recorded as an open item ([§10-G4](#10-caveats-gaps-and-errata)).
- **15.3 bites exactly the pattern the PaperMono firmware uses** — `startReceive()` in a loop with interrupt-driven handling. Whether RadioLib clears the RTC after each receive was not traced.

---

## 9. Drivers and libraries

| Option | Where | Verdict |
|---|---|---|
| **RadioLib** (jgromes) | `github.com/jgromes/RadioLib`, **pinned by the PaperMono factory firmware at `7.2.1`**, commit `b91c6af112e423dcb14529ade5827802a14e1015` | ✅ **Use this.** It is what the shipped firmware runs, and it is the de-facto SX126x driver outside Semtech's own stack |
| Semtech `SX126x` driver / `LoRaMac-node` | Semtech's GitHub organisation | The reference implementation and the LoRaWAN path. Not used by any M5Stack code found here |
| Raw SPI | — | Entirely feasible — §4 is the whole interface — but §8's four workarounds are the kind of thing a hand-rolled driver silently omits |

**Version and patch context** for the PaperMono, **[SRC]** `repos.json`:

- RadioLib is **patched by the vendor build to remove `idf_component.yml`**, so it builds as a plain ESP-IDF component rather than a managed one.
- ⚠ **M5Stack's published PlatformIO snippet pins nothing** — `RadioLib = https://github.com/jgromes/RadioLib` pulls `master`. Reproducing factory behaviour requires the pinned commit **and** the patch **[DOC]** vs **[SRC]**.
- ⚠ **Licence mismatch, flagged not confirmed:** RadioLib is **LGPL-3.0** upstream while the M5Stack demo carrying it is MIT. Not verified in this pass.
- ✅ **Correction, 2026-09-07 — the line immediately above is wrong and is left in place only for provenance.** RadioLib is **MIT**, not LGPL-3.0. Verified `executed-success` on 2026-09-04 by the LoRa-generations pass: the licence file is **`license.txt`, lower case** (which is why a `LICENSE` fetch 404s, and is the likely origin of the LGPL-3.0 belief), and it reads `MIT License / Copyright (c) 2018 Jan Gromeš` **byte-identically at tags `7.2.1` and `7.7.1`**. `gh api repos/jgromes/RadioLib --jq .license.spdx_id` → `MIT`. **There is no mismatch with the MIT-licensed M5Stack demo.** The original line was not edited because this pass was append-only; the correction is parked for a maintainer in [`scratch/index-merge/corrections-requiring-review.md`](../../../scratch/index-merge/corrections-requiring-review.md). Source: `scratch/lora-generations/index-fragments.md` §6.1.

Framework: ESP-IDF **5.5.1**, target `esp32s3`, arduino-esp32 **3.3.10** as a managed component **[SRC]** `dependencies.lock`.

The vendor's integration is deliberately thin: `hal_lora.cpp` implements a `RadioLibHal` over ESP-IDF SPI and GPIO, hands RadioLib six pin numbers, and gets out of the way. `NRESET` is passed as `RADIOLIB_NC` because reset is an I²C expander pin (§2).

---

## 10. Caveats, gaps and errata

| # | Issue | Evidence |
|---|---|---|
| **G1** | ⚠ **No `Stamp-LoRa-1262` module datasheet exists.** M5Stack's *Datasheets* list for the PaperMono links **this chip datasheet** and nothing module-specific. So the module's supply current, RF output power at the connector, antenna type and gain, matching network, TCXO-vs-crystal choice, internal DIO usage, and the identity of module pins 11–13 are **all undocumented**. This chip record cannot fill those gaps and does not try | **[DOC]** — the absence is `executed-success`, the full list was enumerated; [module record §5-G1](../../m5stack/stamp-lora-1262/README.md) |
| **G2** | **The chip has never been seen.** No teardown photograph of the module, no top marking read. `SX1262` rests on the module name, the vendor specification row, the module's `SX_*` pin names and the firmware's +22 dBm request — strong, but circumstantial | **[SCH]**, **[DOC]**, **[SRC]**; **[INF]** |
| **G3** | **TCXO presence is inferred from a firmware constant** (§5.2.1). `LORA_TCXO_VOLTAGE = 3.0f` shows what M5Stack *configures*, not what is *fitted*. `inferred`, `not-tested` | **[SRC]** `hal_lora.cpp:40` |
| **G4** | **Whether RadioLib 7.2.1 applies all four of Semtech's §15 workarounds was not verified.** Two of them (15.2's 5–6 dB clamp fix, 15.3's stuck RTC timeout) directly affect this board's usage pattern (§8) | not traced — explicit gap |
| **G5** | **The firmware selects LDO regulation, roughly doubling receive current** versus the datasheet's headline figure (§5.4). Whether the module even has the DC-DC inductors is unknown | **[SRC]** `hal_lora.cpp:41`; **[DS]** Table 3-5 |
| **G6** | **The chip's 150–960 MHz range is not the module's range.** The module is an 868–923 MHz single SKU, and the narrowing is imposed by an undocumented matching network and antenna (§1.1) | **[DS]** Table 3-7 vs **[DOC]** |
| **G7** | **`SetDIO2AsRfSwitchCtrl(true)` and the module's `SX_ANT_SW` pin are two different switches** (§5.3.1). `SX_ANT_SW`'s semantics are documented nowhere; the firmware sets it HIGH once and forgets it | **[SRC]**; [module record G4](../../m5stack/stamp-lora-1262/README.md) |
| **G8** | **`XOSC_START_ERR` is *expected* at POR and at every cold-start wake when a TCXO is used.** Treating it as a fatal error will refuse to start a working radio (§5.2) | **[DS]** §13.3.6 |
| **G9** | **Semtech's datasheet does not enumerate which spreading factors are unavailable at which bandwidths** — Table 6-1 carries the caveat without the table (§3.1). An unresolved gap in the primary document | **[DS]** Table 6-1 footnote 1 |
| **G10** | **SF6 is not interoperable with SF6 on an SX1276**, and SF5/SF6 need 12 preamble symbols (§3.1). A silent interoperability failure against older LoRa nodes | **[DS]** §6.1.1.1 |
| **G11** | **Crystal trimming caps are overwritten by the state machine** unless you are already in `STDBY_XOSC` (§6.5). And `SetDIO3AsTcxoCtrl` unconditionally forces `XTA` to 33.4 pF | **[DS]** §4.1.3 |
| **G12** | ⚠ **Semtech's canonical datasheet could not be downloaded, and Semtech's own listing is dated 2025-04-07 — later than the Rev 2.2 (Dec 2024) copy held here.** So this document **may be one revision behind**, and that is *unresolved*, not "no lag". See §11 | `executed-failed`, 2026-09-01 |
| **G13** | **LR-FHSS is patent-encumbered**, and Semtech's disclaimer explicitly declines to grant patent rights with the software (§1) | **[DS]** p. 2 |
| **G14** | **No certification of any kind is published for the PaperMono**, including for its sub-GHz emitter. A single wideband 868–923 MHz SKU with no per-region variant covers EU 868, US 915 and JP 920 allocations with no regulatory paperwork to point at | **[DOC]** — negative result; [`features/lora.md` §7](../../../devices/m5stack/papermono/features/lora.md) |
| **G15** | **Nothing has been measured.** No range, throughput, sensitivity, TX current or battery-impact figure exists from M5Stack or from anyone in the community | **[DOC]**, community — negative result |

---

## 11. Sourcing

No vendor sourcing guide exists in this repository for Semtech — see the [vendor guides index](../../../vendors/README.md). This pass's findings, for whoever writes one:

> ✅ **Correction, 2026-09-07 — the sentence immediately above is now out of date and is left in place only for provenance.** **A Semtech vendor guide now exists:** [`vendors/semtech/README.md`](../../../vendors/semtech/README.md), written 2026-09-04 from this section plus a fresh probe pass. It adds: the **embedded 1 984-entry JSON document catalogue** that enumerates everything Semtech publishes; the **`/uploads/documents/` soft-404**; the **`semtech.force.com` → `semtech.my.site.com`** portal migration; the exact scope of the registration wall (**no LoRa document is behind it**); working **Digi-Key and Mouser** templates with negative controls; and the finding that an **invalid Salesforce token also returns HTTP 200**, so that endpoint cannot be probed at all.
>
> On **G12** (whether a revision newer than Rev 2.2 exists): that catalogue confirms Semtech's current listing is `SX1261/SX1262 Datasheet` — the same document held here at Rev 2.2 — so the "2025-04-07 listing date vs Dec 2024 revision" question is **still `unresolved`**, but it is now known to be a *listing-date* field in a catalogue rather than a document date.
>
> The original text was not edited because this pass was append-only. Parked for a maintainer in [`scratch/index-merge/corrections-requiring-review.md`](../../../scratch/index-merge/corrections-requiring-review.md). Source: `scratch/lora-generations/index-fragments.md` §6.2.

**`www.semtech.com` serves its product pages to a normal browser user-agent** (HTTP 200, 237 407 bytes for the SX1262 page) but **403s a `WhatsApp/2.23.20.0` agent** — the reverse of `www.st.com`, which serves the WhatsApp agent and resets the connection for Chrome. There is no single agent that works everywhere; rotate.

**Semtech's documents are behind a Salesforce content-distribution front end and could not be retrieved.** The SX1261/SX1262 datasheet is linked as:

```
https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ000008nKCH/hp2iKwMDKWl34g1D3LBf_zC7TGBRIo2ff5LMnS8r19s
```

A `GET` returns a **1 359-byte HTML shell** that immediately JavaScript-submits a POST back to itself. Reproducing that POST returns a **53 747-byte JavaScript application** with no `<a href>`, no iframe and no servlet URL in the markup. Two guessed direct patterns (`/sfc/dist/version/download/`, `/sfc/servlet.shepherd/document/download/`) returned 550- and 787-byte HTML errors. **Reacquisition from Semtech: `blocked`.** `executed-failed`, 2026-09-01.

⚠ **The consequence is a real unresolved question.** Semtech's page labels the entry **"SX1261/SX1262 Datasheet · 2025-04-07 · PDF"**, four months *after* the Rev 2.2 (December 2024) copy held here. That is consistent with a **Rev 2.3 existing**, or with a re-upload of the same revision. **Mirror lag on this document is `unresolved`, not "none".** Previously it was recorded as "not checked"; it has now been checked and could not be settled.

The **working** source is M5Stack's mirror, which is open, fast and correctly typed:

```
https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1177/DS_SX1261_2_V2-2.pdf
```

Other Semtech documents enumerated from the product page and **not retrieved** (all behind the same Salesforce shell): `AN1200.115` Murata IPD design guide (2025-11-13), `AN1200.91` SX1261/62 IPD design guide (2024-07-11), `AN1200.40` reference-design explanation, `AN1200.36` `RxDutyCycle`, `AN1200.35` software Manchester encoding, `AN1200.53` packets longer than 255 bytes, the SX1261/SX1262 Development Kit user guide, and the SX1261 LoRa Calculator. **`AN1200.37` "Recommendations for Best Performance"** is cited by the datasheet itself (§4.1.2) for heat-dissipation guidance and was not located on the product page at all.

---

## 12. Used By

### [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — inside module `U14`, sheet 4

**The SX1262 is not a component of the main board.** It is inside the plug-in [`Stamp-LoRa-1262-mini`](../../m5stack/stamp-lora-1262/README.md) module (`U14`, sheet 4), which presents a 13-pin SPI-plus-control interface. **That record owns the board integration**; this section states only what the *chip* does on this board and points at it.

Chip-level facts established for this board:

| Chip-level property | Value on the PaperMono | Evidence |
|---|---|---|
| Part class | **SX1262** (high-power, +22 dBm), not SX1261 | firmware requests 22 dBm and instantiates `SX1262`; module name — **[SRC]** `hal_lora.cpp:37,328` |
| Host SPI | mode 0, **8 MHz** (chip maximum 16 MHz) | **[SRC]** `hal_lora.cpp:31` |
| `BUSY` handshake | wired out to **ESP32-S3 GPIO21**; RadioLib honours it | **[SCH]**, **[SRC]** `hal_lora.cpp:28` |
| `DIO1` | wired out to **ESP32-S3 GPIO5** as the sole IRQ line, registered `GPIO_INTR_POSEDGE`, and also an **ESP32 wake source** | **[SCH]**, **[SRC]** `hal_lora.cpp:27`, `app_sleep_wake.cpp:44` |
| `DIO2` | **configured as an internal RF switch control** — `setDio2AsRfSwitch(true)` | **[SRC]** `hal_lora.cpp:343` |
| `DIO3` | **configured as a 3.0 V TCXO supply** (`tcxoVoltage = 0x06`) — `inferred` (§5.2.1) | **[SRC]** `hal_lora.cpp:40,334` |
| `NRESET` | not driven by RadioLib (`RADIOLIB_NC`); reset is **M5IOE1 `IO10`** | **[SRC]** `hal_lora.cpp:327,330` |
| Regulator mode | **LDO**, not DC-DC — ~2× receive current (§5.4) | **[SRC]** `hal_lora.cpp:41` |
| OCP | `setCurrentLimit(140.0f)` — the SX1262 post-`SetPaConfig` default (§6.2) | **[SRC]** `hal_lora.cpp:344` |
| Supply | **3.3 V** on the module's `VIN_3V3`, from an SSP7615-33DFR LDO gated by **M5PM1 `IO2`** | **[SCH]**; [module record §3.5](../../m5stack/stamp-lora-1262/README.md) |

The full radio configuration the factory firmware programs **[SRC]** `hal_lora.cpp:32-43`, `:333-344`:

| Parameter | Value | Note |
|---|---|---|
| Frequency | **868.0 MHz** | hard-coded; the EU band, at the bottom of the module's 868–923 range |
| Bandwidth | 62.5 kHz | |
| Spreading factor | **12** | −20 dB demodulator SNR (§3.1) |
| Coding rate | 8 (4/8) | maximum FEC |
| Sync word | `0x34` | |
| TX power | **22 dBm** | ⇒ ~118 mA (§6.1) |
| Preamble | 10 symbols | ⚠ Semtech recommends **12** (§3.1) |
| TCXO voltage | 3.0 V | §5.2.1 |
| Regulator | LDO | §5.4 |
| Current limit | 140 mA | §6.2 |
| Max packet | 255 bytes | the 256-byte buffer (§3.4) |

This is **SF12 at 62.5 kHz with CR 4/8** — on the order of tens of bits per second. It is a maximum-range demonstration, not a sensible throughput default, and anyone building on it should change it deliberately.

⚠ **Two things in that table are worth a second look.** The preamble is **10 symbols** where Semtech recommends 12 for optimal performance across the receiver's dynamic range (and *requires* 12 at SF5/SF6, though SF12 is in use here) **[DS]** §6.1.1.1, Rev 1.1 changelog. And the whole configuration assumes a matching network nobody outside M5Stack has seen (§1.1, G1).

For host wiring, bring-up ordering, the `SX_ANT_SW` question, the SPI-host naming mismatch and the unlabelled module pins 11–13, go to the **[Stamp-LoRa-1262 record](../../m5stack/stamp-lora-1262/README.md)** and to [`features/lora.md`](../../../devices/m5stack/papermono/features/lora.md).

### [M5Stack PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) — **not fitted**

**The Lite has no SX1262, and no LoRa module to put one in.** It has no LoRa row in its specification table, no LoRa block in its PinMap, and its PlatformIO `lib_deps` omits `RadioLib` entirely **[DOC]**. Its product weight is 2.3 g lower than the PaperMono's (72.4 g vs 74.7 g), consistent with two omitted radios.

Together with the [ST25R3916 NFC front end](../../stmicroelectronics/st25r3916/README.md), LoRa is the whole of the **USD 10.00** difference between C153 (USD 65.00) and C153-LITE (USD 55.00) **[DOC]**. One widely repeated launch article inverted this and claimed the USD 55 model has NFC and LoRa; it does not.

Note that the shared `M5PaperMono-UserDemo` firmware image serves **both** SKUs and detects the variant at runtime by probing the **NFC** rail, **not** the radio **[SRC]** `hal_board.cpp:160-172`. So a Lite runs the same binary and simply never brings the radio up.

### [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) — inside module `M1` · *added 2026-09-04*

A **Cardputer-Adv / CardputerZero** expansion board, store publish date **2025-12-30**, carrying the same `Stamp LoRa-1262 Mini` module as the PaperMono but wired **entirely differently**. Read this row before copying any PaperMono configuration.

| Function | Host GPIO (Cardputer-Adv) | Contrast with PaperMono |
|---|---|---|
| SPI SCK / MOSI / MISO | **G40 / G14 / G39** | ⚠ **shared with the host's microSD** (`SDCARD_CS` = G12); PaperMono gives the radio its own bus |
| `NSS` | **G5** | — |
| `BUSY` | **G6** | direct GPIO, not behind an expander |
| `DIO1` (`LoRa_IRQ`) | **G4** | direct GPIO |
| `NRST` | **G3** — **an ordinary host pin** | PaperMono routes reset through the **M5IOE1 I²C expander** |
| External antenna switch | **`PI4IOE5V6408` P0 @ I²C 0x43** | PaperMono uses **M5IOE1 `IO2`** |
| Rail enable | **none** — the on-board `JW5712` buck is pulled on and stays on | PaperMono gates `3V3_L2_LoRa` with **M5PM1 `IO2`** |
| Antenna | **external SMA/RP-SMA** + rubber duck | PaperMono uses a built-in FPC antenna |
| `setDio2AsRfSwitch` | **not called** by M5Stack's Cap example | PaperMono firmware calls it `true` |

**⚠ The two boards disagree about the TCXO voltage, and both are shipping.**

| Source | `DIO3` TCXO voltage |
|---|---|
| M5Stack Cap Arduino example (`radio.begin(…, 3.0, true)`) | **3.0 V** |
| M5Stack PaperMono firmware | **3.0 V** |
| **Meshtastic upstream `variants/esp32s3/m5stack_cardputer_adv/variant.h`** | **`SX126X_DIO3_TCXO_VOLTAGE 1.8`** + `TCXO_OPTIONAL` |

Since §5.2 of this record explains that a wrong `DIO3` setting yields a radio that initialises and then fails silently, the disagreement matters. Both are reported working in the field. Unresolved; start from **3.0 V** on M5Stack's own hardware. See [`devices/m5stack/cap-lora-1262/features/lora.md` §8](../../../devices/m5stack/cap-lora-1262/features/lora.md).

Vendor claims for this board: **+22 dBm**, **−147 dBm**, 868–923 MHz single wideband SKU, **no published certification of any kind**. Default RadioLib configuration in M5Stack's example: 868.0 MHz, BW 125 kHz, SF12, CR 4/5, sync `0x34`, preamble 20, `useRegulatorLDO = true`, `setCurrentLimit(140)`.

**Meshtastic supports this board upstream** — board `m5stack-cardputer-adv`, hardware model `meshtastic_HardwareModel_M5STACK_CARDPUTER_ADV = 112`, introduced by PR #9540 (merged 2026-03-06, commit `969aefa551d645e6110be11f330774e15ad9c87d`), first shipped in **v2.7.20.6658ec2** (2026-03-11); the antenna-switch init was fixed in **v2.7.24** (2026-05-23).

### [M5Stack Cap LoRa868 (U201)](../../../devices/m5stack/cap-lora868/README.md) — inside a `Stamp LoRa-1262` (standard size) · *added 2026-09-04*

The predecessor Cap, published **2025-09-05**, now **[EOL]**. Same SX1262, same host pin map, but **+20 dBm** rather than +22, **no shield can**, **no RF-switch control** and **no Grove port**. Firmware distinguishes the two Caps by probing I²C `0x43` — present means U214. Its documentation publishes the only state-resolved current figures in the family: GPS on / LoRa standby **29.24 mA**, GPS sleep / LoRa standby **3.16 mA**, GPS sleep / LoRa TX max **129.72 mA**, GPS on / LoRa TX max **155.03 mA** at DC 5 V.

### [M5Stack Cardputer Mesh Kit (K152)](../../../devices/m5stack/cardputer-mesh-kit/README.md) — via the bundled Cap LoRa-1262 · *added 2026-09-04*

Cardputer-Adv + Cap LoRa-1262, published 2026-04-30, USD 48.00, pre-flashed with Meshtastic and the **only** configuration eligible for Meshtastic authorised-device registration.

### [M5Stack Stamp C6LoRa (S012)](../../../devices/m5stack/stamp-c6lora/README.md) and [Unit C6L (U202)](../../../devices/m5stack/unit-c6l/README.md) — *added 2026-09-04*

An **SX1262 paired with an ESP32-C6** on one SMD module, 850–960 MHz, +22 dBm, −148 dBm, with an **SGM13005L4 LNA** and a **`PI4IOE5V6408`** expander controlling both the RF switch *and* the LNA enable. Unit C6L is the Grove-cabled product built around it and has its own Meshtastic variant, `variants/esp32c6/m5stack_unitc6l/`, hardware model `M5STACK_C6L = 111`. Light records; the module schematic is held but not decoded.

### [M5Stack Cardputer Mesh Kit (K152)](../../../devices/m5stack/cardputer-mesh-kit/README.md) — host-side integration · *added 2026-09-07*

The SX1262 itself sits on the [Cap LoRa-1262](../../../devices/m5stack/cap-lora-1262/README.md),
which plugs into the **Cardputer ADV's** EXT 2.54-14P header. Host-side pin assignment, agreed by
three independent implementations (M5Stack's factory firmware, Meshtastic's variant, and the
docs PinMap):

| Function | Host GPIO |
|---|---|
| `NSS` | G5 |
| `RESET` | G3 |
| `DIO1` / IRQ | G4 |
| `BUSY` | G6 |
| SPI `SCK`/`MOSI`/`MISO` | G40 / G14 / G39 — **shared with the microSD card**, CS G12 |

Meshtastic additionally declares `SX126X_DIO2_AS_RF_SWITCH` and
`SX126X_DIO3_TCXO_VOLTAGE 1.8` with `TCXO_OPTIONAL`.

⚠ **Initialisation requires one non-obvious step**: M5Stack states that the RF antenna switch
must be enabled by setting **`P0` of the Cap's PI4IOE I/O expander HIGH**, over the host's
*internal* I²C bus (G8/G9). Omit it and the radio transmits into a disconnected antenna.

Host-side interface documentation:
[`devices/m5stack/cardputer-adv/features/cap-header.md`](../../../devices/m5stack/cardputer-adv/features/cap-header.md).

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — main board, default radio · *added 2026-09-07*

One of two selectable radios; the other is [LR2021](../lr2021/README.md). Fitted on the K230 main
board and exposed to userspace through **spidev**, driven by **RadioLib** — there is no in-kernel
LoRa driver on this board.

`MOSI` ← `GPIO16` · `MISO` → `GPIO17` · `SCK` ← `GPIO15` · `CS` ← `GPIO14` · `RESET` ← `GPIO5` ·
`BUSY` → `GPIO19` · **`DIO1` → `GPIO20`** · power-enable ← `GPIO44`.

⚠ **The interrupt DIO differs by fitted radio.** On SX1262 units it is `DIO1`; on LR2021 units it
is `DIO11`. Both land on K230 `GPIO20`, so firmware that hard-codes `DIO1` silently sees no
interrupts on an LR2021 board.

Band is fixed per SKU: `K256` 868 MHz · `K256-A` 915 MHz · `K256-B` 923 MHz · `K256-C` 433 MHz.
LilyGO states that **Meshtastic voice and photo transfer are unavailable on SX1262 units** — those
boards get text mesh only; the LR2021 variant is required for media.

---

## 13. Related components

- [**M5Stack Stamp-LoRa-1262**](../../m5stack/stamp-lora-1262/README.md) — **the module this chip lives inside.** Pinout, host wiring, reset, antenna switch, power gating and bring-up order are all there. Read it before this one if you are working on the board rather than the radio
- [**M5Stack M5IOE1**](../../m5stack/m5ioe1/README.md) — supplies the module's `NRST` (`IO10`) and `ANT_SW` (`IO2`). ⚠ its enum values are one *less* than its pin labels
- [**M5Stack M5PM1**](../../m5stack/m5pm1/README.md) — gates the module's 3.3 V rail via `IO2`
- [**Espressif ESP32-S3R8**](../../espressif/esp32-s3r8/README.md) — the host; `SPI3_HOST` on GPIO38/39/40/41, plus GPIO21 `BUSY` and GPIO5 `DIO1`
- [**SSP7615-33DFR**](../../generic/ssp7615-33dfr/README.md) — the 400 mA LDO producing `3V3_L2_LoRa`
- [**STMicroelectronics ST25R3916**](../../stmicroelectronics/st25r3916/README.md) — the other radio the Lite does without
- [Vendor sourcing guides index](../../../vendors/README.md) — **no Semtech guide exists yet**; §11 is what one would open with
- [Components index](../../README.md)

---

## 14. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/sx1261-2-datasheet-v2.2-m5stack-mirror.pdf` | 4 459 535 | `6d783125dbef567954ce53095ad068d0950b2a8de52f95bb2cfde4146c4306c2` | **SX1261/2 datasheet, `DS.SX1261-2.W.APP` Rev 2.2, December 2024, 118 pp.** PDF metadata: Title `DS_SX1261_2 V2-2.pdf`, Author `julie`, Creator `FrameMaker 16.0.6`, Producer `Adobe PDF Library 17.0`, created 2024-12-04, modified 2024-12-05. **This describes the chip, not the module** (§10-G1) |

| Field | Value |
|---|---|
| Version / revision | **Rev 2.2** (revision history runs Rev 1.0, October 2017 → Rev 2.2) |
| Publication date | **December 2024** |
| Retrieval date | **2026-09-01** |
| Byte size | **4 459 535** |
| SHA-256 | `6d783125dbef567954ce53095ad068d0950b2a8de52f95bb2cfde4146c4306c2` |
| **Canonical URL** | `https://semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ000008nKCH/hp2iKwMDKWl34g1D3LBf_zC7TGBRIo2ff5LMnS8r19s` — linked from `https://www.semtech.com/products/wireless-rf/lora-connect/sx1262`. ⚠ **`blocked`**: JavaScript/POST content-distribution shell, see §11 |
| **M5Stack mirror URL** | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1177/DS_SX1261_2_V2-2.pdf` — open, HTTP 200, `application/pdf` |
| Mirror lag | ⚠ **`unresolved`.** Semtech's listing is dated **2025-04-07**, four months after Rev 2.2. Canonical download blocked, so a Rev 2.3 can be neither confirmed nor ruled out (§10-G12) |
| Licence | **`unknown`** — © Semtech Corporation. The document carries Semtech's standard disclaimer plus an explicit **LR-FHSS patent notice** (§1) that grants no patent rights |
| Redistribution status | **`unknown`** |
| Disposition | **`repository`** |
| Type validated | Yes — `%PDF-1.6`, 118 pages, `pdfinfo` metadata as above |
| ⚠ Text-layer note | **Figure-label fonts carry a uniform +31 code-point offset** and extract as legible-but-wrong text. Body text and tables are clean. See the Evidence labelling section |

**Reacquisition:** use the M5Stack mirror. Semtech's own path is `blocked` for automated clients and requires a browser (§11). Recorded honestly rather than omitted.

The module-level document that *should* exist does not: see [`components/m5stack/stamp-lora-1262/README.md` §8](../../m5stack/stamp-lora-1262/README.md), whose `artifacts/` directory is empty for exactly that reason.

---

## 15. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | SX1261/2 Datasheet — Long Range, Low Power sub-GHz RF Transceiver | **Semtech Corporation**, mirrored by M5Stack | credible mirror | datasheet | `artifacts/sx1261-2-datasheet-v2.2-m5stack-mirror.pdf`; mirror `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1177/DS_SX1261_2_V2-2.pdf` | 2026-09-01 | **Rev 2.2, December 2024**, `DS.SX1261-2.W.APP`, 118 pp | §1–§8, §10 |
| S-2 | SX1262 product page — document list and dates | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-connect/sx1262` | 2026-09-01 | datasheet entry dated **2025-04-07** | §11, §10-G12; enumerates the application notes |
| S-3 | Semtech Salesforce content-distribution endpoint | Semtech | primary | download shell | `semtech.my.salesforce.com/sfc/p/E0000000JelG/a/RQ000008nKCH/…` | 2026-09-01 | — | §11 — **negative result**, `executed-failed`; reacquisition `blocked` |
| S-4 | PaperMono schematic, sheet 4 (`U14`) | M5Stack | primary | schematic PDF | `PaperMono_SCH_V0.6.2_20260522.pdf` (held in the device tree) | 2026-09-01 | **V0.6.2, 2026-05-22** | §2 module-boundary mapping, §12 |
| S-5 | `M5PaperMono-UserDemo` — `main/hal/hal_lora.cpp`, `main/app_sleep_wake.cpp`, `repos.json`, `dependencies.lock` | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-UserDemo` @ `c1099107271d31a0678d661a896e2b04dbb331ea` | 2026-09-01 | 2026-08-10, MIT | §5.2.1, §5.3.1, §5.4, §6.2, §9, §12 |
| S-6 | RadioLib | jgromes | third-party | source | `github.com/jgromes/RadioLib` @ `b91c6af112e423dcb14529ade5827802a14e1015` | 2026-09-01 | tag **7.2.1**; upstream licence LGPL-3.0 (**unverified**) | §9 |
| S-7 | PaperMono product page — specification table, PinMap, *Datasheets* list | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono` | 2026-09-01 | undated | §1.1 band, §10-G1, §12 |
| S-8 | PaperMono-Lite product page | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono-Lite` | 2026-09-01 | undated | §12 — **negative result**: no LoRa row, no `RadioLib` |
| S-9 | Certification index | M5Stack | primary | vendor docs | `docs.m5stack.com/en/certification` | 2026-09-01 | undated | §10-G14 — **negative result**, 0 matches for `PaperMono` / `C153` |
| S-10 | `C153-PaperMono-UserDemo-v1.2` firmware image | M5Stack via M5Burner | primary | binary | SHA-256 `72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa` | 2026-09-01 | v1.2, built 2026-08-06, IDF v5.5.1 | corroborates the LoRa pin map and wake source |

## G4 — RadioLib §15 errata workarounds — **RESOLVED 2026-09-02**

Previously open as: "whether RadioLib applies all four SX126x datasheet §15
workarounds — not verified", and later verified only on `master` 7.7.1, which is
**not** the version the M5Stack PaperMono pins.

**Verified at tag `7.2.1`** — the pinned version — by reading the source through
the GitHub contents API (`executed-success` for the retrieval; `inferred` for
behaviour, nothing was run on hardware):

| Datasheet §15 item | Symbol in `src/modules/SX126x/SX126x.cpp` @ 7.2.1 | Present |
|---|---|---|
| 15.1 RX gain / sensitivity | `rxGain` / sensitivity path | ✅ ×4 |
| 15.2 PA clamping (Tx resistance to antenna mismatch) | `fixPaClamping` | ✅ ×1 |
| 15.3 Implicit-header-mode timeout | `fixImplicitTimeout` | ✅ ×3 |
| 15.4 Inverted-IQ operation | `fixInvertedIQ` | ✅ ×2 |

`fixPaClamping` additionally appears ×3 in `SX1262.cpp` and **×0 in
`SX1261.cpp`**, exactly matching the datasheet's "SX1262 only" note — a good sign
the workaround is applied deliberately rather than blanket.

**Conclusion: 7.2.1 behaves as master does on this point.** The gap is closed for
the shipping version, not just the current one.
