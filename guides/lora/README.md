# LoRa — a device-independent guide

> **How does LoRa actually work, what does LoRaWAN add, and how do I bring an SX126x up?**
> A cross-cutting guide compiled from the LoRa knowledge in this library — principally the
> [Semtech SX1262 record](../../components/semtech/sx1262/README.md) (662 lines, built on
> `DS.SX1261-2.W.APP` Rev 2.2 held locally), the
> [M5Stack Stamp-LoRa-1262 module record](../../components/m5stack/stamp-lora-1262/README.md),
> the [Ebyte E22-900M22S record](../../components/ebyte/e22-900m22s/README.md) and the
> [PaperMono LoRa feature guide](../../devices/m5stack/papermono/features/lora.md).
> Compiled **2026-09-02**. **No radio has been keyed by anyone whose report could be located.**

## 0. What this guide is, and what it is not

This is the **common** layer the research method asks for in step 13: reusable concepts, APIs,
alternatives, validation and generic pitfalls, **without unqualified device pin assignments**. Where
a concrete example is needed the device is named and its record linked.

It does **not** duplicate the deep records. The
[SX1262 record](../../components/semtech/sx1262/README.md) owns the opcode table, the electrical
tables, the DIO2/DIO3 mechanics and Semtech's four mandatory errata workarounds. **Where this guide
and a deep record disagree, the deep record wins.**

What this page adds: the **arithmetic** that connects SF/BW/CR to airtime, battery and legality —
which is the part that is always described qualitatively and always bites quantitatively — plus the
LoRa/LoRaWAN/Meshtastic distinction, a sourced regional band table, and a set of failure signatures.

### Evidence labels

| Label | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Datasheet claim, inherited from a component record citing a section or table of a locally-held document (`DS.SX1261-2.W.APP` Rev 2.2) | `not-tested` |
| **[SRC]** | Read out of source at a cited `file:line` — either from a repo record, or from a live read of upstream on **2026-09-02** | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | Vendor documentation or repository metadata, retrieved 2026-09-02 | `not-tested` |
| **[PCB]** · **[BOM]** · **[GAP]** | Inherited labels from the [Ebyte E22-900M22S record](../../components/ebyte/e22-900m22s/README.md): a parsed KiCad netlist, a production BOM, and that record's marker for a claim that would normally be datasheet-backed and is not | `executed-success` for [PCB]/[BOM] extraction; **[GAP] is an explicit absence of evidence** |
| **[STD]** | A claim about a standard or regulation (ETSI, FCC, ARIB, LoRa Alliance). ⚠ **This repository holds none of these documents** | `not-tested`, **unverified against the primary document** |
| **[REC]** | Recalled general knowledge with no document behind it here | **`not-tested` and unsourced** |
| **[INF]** | Derived here, with the arithmetic shown | `inferred` |

⚠ **No figure in this guide was measured.** §12 lists what could not be sourced.

---

## 1. LoRa modulation, and the arithmetic that follows from it

### 1.1 Chirp spread spectrum

LoRa modulates by sweeping the carrier linearly across the channel bandwidth. A symbol is a chirp
whose *starting point* in the cycle encodes the data; the receiver de-chirps by multiplying with a
conjugate sweep and takes an FFT, so the symbol becomes a peak in a bin **[REC]**.

Two properties fall out, and they are the whole of LoRa's value:

- **Processing gain.** Each symbol spans `2^SF` chips **[DS]** ([SX1262 §3.1, Table 6-1](../../components/semtech/sx1262/README.md#31-lora)),
  so the receiver integrates over many chips per bit and can demodulate **below the noise floor**.
- **Orthogonality between spreading factors.** Signals at different SF are largely invisible to each
  other, which is why a gateway can hear several rates at once — **and why both ends of a
  point-to-point link must be configured identically in advance** **[REC]**.

The datasheet gives the demodulator's SNR floor per spreading factor **[DS]**:

| SF | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|
| chips/symbol | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 |
| typical SNR (dB) | −2.5 | −5 | −7.5 | −10 | −12.5 | −15 | −17.5 | **−20** |

**Read the pattern, not the row.** From SF5 to SF12 the SNR floor improves by 17.5 dB across seven
steps: **exactly 2.5 dB per spreading factor step** **[INF]**, arithmetic on the table above. And
because a symbol spans `2^SF` chips, **each step also doubles the time on air.** That single sentence
is the entire SF trade-off:

> **One spreading-factor step buys 2.5 dB of link budget and costs exactly 2× airtime.**

### 1.2 Bandwidth

`BW_L` runs **7.81 – 500 kHz** **[DS]**. Halving the bandwidth halves the noise power in the
receiver, so it should buy ~3 dB. The datasheet's own sensitivity table mostly agrees **[DS]**
([SX1262 §6.3](../../components/semtech/sx1262/README.md#63-sensitivity)):

| LoRa, RX-boosted, split RF paths | SF7 | SF12 |
|---|---:|---:|
| BW 10.4 kHz | −134 dBm | **−148 dBm** |
| BW 125 kHz | −124 dBm | −137 dBm |
| BW 250 kHz | −121 dBm | −134 dBm |
| BW 500 kHz | −117 dBm | −129 dBm |

500 → 250 kHz buys 5 dB and 250 → 125 kHz buys 3 dB **[INF]** — the 500 kHz step is *worse* than
theory, and 500 kHz is also the exact case Semtech's **known limitation §15.1** exists to patch
**[DS]** ([SX1262 §8](../../components/semtech/sx1262/README.md#8-register-level-workarounds-you-must-implement)).
Those two facts are probably the same fact.

⚠ **Two gaps in Semtech's own document.** Table 6-1 states "not all SF are available for any
bandwidth" **without enumerating which** **[DS]**
([G9](../../components/semtech/sx1262/README.md#10-caveats-gaps-and-errata)) — an unresolved
documentation gap. And **62.5 kHz does not appear in the sensitivity table at all**, despite being a
perfectly legal setting and the one a shipping product in this library actually uses (§4.4). Its
sensitivity has to be interpolated at roughly **−140 dBm at SF12** **[INF]**, which is an estimate,
not a specification.

### 1.3 Coding rate

`CR` runs **4/5 to 4/8** **[DS]** — forward error correction overhead. Going from 4/5 to 4/8 multiplies
the payload symbol count by **8/5 = 1.6×** **[INF]**. It buys robustness against burst interference,
not against thermal noise; SF and BW own the noise floor.

### 1.4 Symbol time and airtime — the consequence that bites

The datasheet gives the symbol rate as `Rs = BW / 2^SF` **[DS]**, so the **symbol time** is:

```
Ts = 2^SF / BW                                      [DS] for Rs; [INF] for the inversion
```

| Ts (ms) | SF7 | SF8 | SF9 | SF10 | SF11 | SF12 |
|---|---:|---:|---:|---:|---:|---:|
| BW 500 kHz | 0.256 | 0.512 | 1.024 | 2.048 | 4.096 | 8.192 |
| BW 250 kHz | 0.512 | 1.024 | 2.048 | 4.096 | 8.192 | 16.384 |
| **BW 125 kHz** | **1.024** | 2.048 | 4.096 | 8.192 | 16.384 | **32.768** |
| BW 62.5 kHz | 2.048 | 4.096 | 8.192 | 16.384 | 32.768 | **65.536** |

All **[INF]** — arithmetic on the datasheet's own definition.

A LoRa symbol carries `SF` raw bits **[REC]**, so the nominal bit rate is
`Rb = SF · (BW / 2^SF) · 4/(4 + n)` for `CR = 4/(4+n)`:

| Nominal Rb, BW 125 kHz, CR 4/5 | SF7 | SF8 | SF9 | SF10 | SF11 | SF12 |
|---|---:|---:|---:|---:|---:|---:|
| **[INF]** bit/s | 5469 | 3125 | 1758 | 977 | 537 | 293 |

**Sanity check, and it passes.** LoRaWAN's EU868 data rates DR5…DR0 are commonly quoted as
5470 / 3125 / 1760 / 980 / 440 / 250 bit/s **[REC]**. The first four match the derivation exactly.
SF11 and SF12 come out high until you apply **LDRO** — low-data-rate optimisation, which reserves two
bits per symbol: `537 × 9/11 = 439` and `293 × 10/12 = 244` **[INF]**. That agreement is itself
evidence the derivation is right, and it is why LDRO is not optional at long symbol times.

**Now the part that bites.** Take the configuration the
[PaperMono factory firmware actually programs](../../devices/m5stack/papermono/features/lora.md) —
**SF12, BW 62.5 kHz, CR 4/8** **[SRC]**:

```
Ts  = 4096 / 62 500          =  65.536 ms per symbol            [INF]
Rb  = 12 / 0.065536 × 4/8    =  91.6 bit/s   (76 bit/s with LDRO) [INF]
preamble alone, 10 symbols   =  0.66 s                          [INF]
a 16-byte payload            =  128 bits ≈ 1.4 s of payload      [INF]
⇒ a single small frame is on the order of 2–3 seconds on air.
```

The SX1262 record independently characterises this configuration as "on the order of tens of bits per
second… a maximum-range demonstration, not a sensible throughput default"
([§12](../../components/semtech/sx1262/README.md#12-used-by)) — **the derivation agrees with the
record**, which is the point of showing it.

⚠ **Do not hand-roll the exact figure.** The closed-form airtime expression (with its header,
sync-word, CRC and ceiling terms) lives in Semtech application notes **this repository does not
hold**. Use the library: RadioLib exposes **`SX126x::getTimeOnAir(size_t len)`** — declared
`src/modules/SX126x/SX126x.h:634`, implemented `SX126x.cpp:812`, and it reads SF, BW, CR, preamble
length, CRC, implicit-header mode and LDRO out of the current configuration
(`SX126x.cpp:817-832`) **[SRC]**, read live 2026-09-02. RadioLib itself uses it internally to
compute transmit timeouts (`SX126x.cpp:236`, `:286`).

### 1.5 The battery consequence, which is not the one people expect

Semtech's figures at 3.3 V, 25 °C, TCXO and RF-switch consumption excluded **[DS]**
([SX1262 §5.4, §6.1](../../components/semtech/sx1262/README.md#54-regulator-choice-and-what-the-papermono-firmware-gives-up)):

| Mode | DC-DC | **LDO** |
|---|---:|---:|
| RX, LoRa 125 kHz | 4.6 mA | **8.8 mA** |
| RX boosted, LoRa 125 kHz | 5.3 mA | **10.1 mA** |
| `STDBY_RC` | 0.6 mA | 0.6 mA |
| Sleep, config retained | 600 nA | 600 nA |
| Sleep, cold (no retention) | 160 nA | 160 nA |
| **TX +22 dBm (SX1262)** | **118 mA** | **118 mA** — the PA runs from `VBAT` either way |

Now put airtime against it **[INF]**:

```
one 3 s frame at +22 dBm   = 118 mA × 3 s     = 0.098 mA·h
ten frames per hour                            ≈ 1 mA average
continuous receive, LDO                        = 8.8 mA
continuous receive, DC-DC                      = 4.6 mA
```

**Transmitting at full legal power ten times an hour costs about a ninth of what listening costs.**
For any node that is not asleep, **receive current dominates**, and therefore the **LDO-versus-DC-DC
decision matters more than the transmit power decision**. On the SX1262 the DC-DC covers the IC core
only — the PA is fed from `VBAT` either way — so DC-DC does **nothing** for transmit current and
roughly **halves** receive current **[DS]**.

This is why the SX1262 record calls the LDO choice
"[the single most consequential unverified fact about the radio on this board](../../components/semtech/sx1262/README.md#54-regulator-choice-and-what-the-papermono-firmware-gives-up)"
(G5). The arithmetic above is why that judgement is right. DC-DC needs two external inductors — 47 nH
before pin 1 and 15 µH between the regulator pins — which is exactly the BOM a small module omits
**[DS]**.

Two more numbers for a duty-cycled design **[DS]**: sleep→standby is **3500 µs cold-start** versus
**340 µs warm-start with retention**. **Ten to one** — which is the entire reason `SetSleep` has a
retention flag, and it must be paid *plus* the TCXO delay (§5.4) on every wake.

---

## 2. LoRa is not LoRaWAN, and Meshtastic is neither

The single most common confusion in this subject.

| Layer | What it is | What you get | What you must build |
|---|---|---|---|
| **LoRa** | A **physical layer**. Semtech's proprietary chirp modulation, in silicon | A radio that sends and receives framed bytes at a chosen SF/BW/CR with a CRC and a sync word | **Everything**: addressing, retries, encryption, key management, channel policy, duty-cycle accounting |
| **LoRaWAN** | A **MAC layer and network architecture** specified by the LoRa Alliance, on top of LoRa | Device classes A/B/C, join procedure (OTAA/ABP), two AES-128 key hierarchies, adaptive data rate, regional channel plans, and a star-of-stars topology through gateways to a network server | An account with a network server, gateway coverage, and acceptance that **downlink is scarce** |
| **Meshtastic** | An **application and mesh protocol** using raw LoRa — **not** LoRaWAN | A flooding mesh of peer nodes, phone apps, position and text messaging, per-region presets | Nothing, if you use its firmware. But you are on **its** channel plan and **its** airtime budget |

**Raw LoRa point-to-point** is entirely reasonable and is what the SX126x drivers give you by
default. It is the right answer for a private link between devices you own. It is the wrong answer
the moment you want many nodes, roaming, or someone else's infrastructure.

**LoRaWAN's real cost is asymmetry.** A Class A device can only receive in two short windows after it
transmits **[REC]**; that is what makes the battery numbers work and it is also why LoRaWAN is a poor
fit for anything needing prompt downlink. Class C listens continuously — and §1.5 says what that
costs.

**Meshtastic is a flood mesh**, so every node's airtime is consumed by every other node's traffic.
That interacts badly with §3's duty-cycle limits at scale, and it is why Meshtastic ships
conservative presets rather than the fastest settings the radio supports **[REC]**.

The library layering mirrors this exactly. RadioLib keeps the PHY in `src/modules/` and puts LoRaWAN
in `src/protocols/LoRaWAN/` alongside APRS, AX.25, RTTY and a dozen other protocols **[SRC]** — the
radio and the network stack are separate concerns in the code as well as on paper.

---

## 3. Regional band plans and duty cycle

⚠ **This is a legal constraint, not a firmware preference.** A wideband module is *capable* of
transmitting outside your allocation. You are not permitted to.

The clearest machine-readable statement of the band plans in this library is RadioLib's own table,
read live from `src/protocols/LoRaWAN/LoRaWANBands.cpp` @ `master`, 2026-09-02 **[SRC]**. Frequencies
are stored in units of 100 Hz; `dutyCycle` is **milliseconds of transmit permitted per hour**;
`dwellTime` is a per-transmission cap in ms (`RADIOLIB_LORAWAN_DWELL_TIME` = **400**,
`LoRaWAN.h:148`).

| Band | Type | Range (MHz) | Max power | Steps | **Duty cycle** | Dwell-time cap |
|---|---|---|---:|---:|---|---|
| **EU868** | dynamic | 863.0 – 870.0 | 16 dBm | 7 | **36 000 ms/h = 1 %** | — |
| **US915** | fixed | 902.0 – 928.0 | 30 dBm | 14 | **none** | **400 ms** |
| EU433 | dynamic | 433.0 – 434.0 | 12 dBm | 5 | **36 000 ms/h = 1 %** | — |
| **AU915** | fixed | 915.0 – 928.0 | 30 dBm | 10 | none | **400 ms** |
| CN470 | fixed | 470.0 – 510.0 | 19 dBm | 7 | none | — |
| **AS923** (+ `_2`, `_3`) | dynamic | 915.0 – 928.0 | 16 dBm | 7 | **36 000 ms/h = 1 %** | **400 ms** |
| AS923_4 | dynamic | 917.0 – 920.0 | 16 dBm | 7 | 36 000 ms/h | 400 ms |
| KR920 | dynamic | 920.9 – 923.3 | 14 dBm | 7 | none | — |
| **IN865** | dynamic | 865.0 – 867.0 | 30 dBm | 10 | none | — |

Eleven bands total (`LoRaWANBands.cpp:6-18`). EU868's three default join channels are **868.1,
868.3, 868.5 MHz** **[SRC]** (`LoRaWANBands.cpp:32-34`).

**What this table means in practice.**

- **`dutyCycle = 36000` is the 1 % rule made concrete: 36 seconds of transmission per hour.** Put
  §1.4's arithmetic beside it — a single SF12/62.5 kHz frame is **2–3 seconds** — and you get
  **roughly a dozen frames per hour, for the whole device** **[INF]**. That is not a tuning
  parameter; it is the design envelope. People discover it after building the product.
- **The two regimes are structurally different, not just numerically.** EU and AS923 are
  *duty-cycle* regimes: transmit rarely, at any length. US915 and AU915 are *dwell-time* regimes: no
  hourly budget, but **no single transmission may exceed 400 ms** — which **forbids SF12 at 125 kHz
  outright**, since §1.4 shows a bare 12-symbol preamble already costs 393 ms **[INF]**. A
  configuration that is legal in Europe can be illegal in the United States for the opposite reason.
- **AS923 has four sub-variants** in the same nominal band, and the frequency offsets differ. "AS923"
  alone is not a configuration.
- **Max power in the table is EIRP at the network layer**, not the chip's `SetTxParams` value.
  EU868's 16 dBm against the SX1262's +22 dBm capability means **the radio can trivially exceed the
  band's limit**, and antenna gain counts against you.

The Ebyte record makes the underlying point bluntly for raw LoRa, outside LoRaWAN entirely
([E22-900M22S §5](../../components/ebyte/e22-900m22s/README.md#5-regulatory-notes)) **[INF]** in that
record: **22 dBm is 158 mW, above the 25 mW (14 dBm) e.r.p. ceiling of the most common EU
sub-bands**, some of which additionally require Listen-Before-Talk / Adaptive Frequency Agility; and
US 915 MHz operation under **FCC Part 15.247** expects frequency hopping or wideband operation, with
fixed-channel use potentially falling under **15.249**'s much lower limits instead **[STD]**.

Semtech states compliance *intent* for **ETSI EN 300 220**, **FCC CFR 47 Part 15**, Chinese
regulations and Japanese **ARIB T-108** **[DS]** — intent for the chip, which is not approval for
your board.

⚠ **A wideband SKU is a regulatory liability, not a feature.** The
[Stamp-LoRa-1262 is a single 868–923 MHz part with no per-region variant and no published
certification of any kind](../../components/m5stack/stamp-lora-1262/README.md#5-caveats-and-gaps)
(G5, a verified negative) — one module spanning EU 868, US 915 and JP 920 allocations. The
[Tanmatsu takes the opposite approach](../../components/ebyte/e22-900m22s/README.md#11-the-family-and-the-one-substitution-that-matters-here):
**a different module is fitted on 433 MHz units** (E22-400M22S instead of E22-900M22S), same
footprint, same digital interface, **different antenna, matching and legal regime** **[BOM]** — and
that record's warning generalises perfectly:

> **Read the band from a configuration source, not from a constant.** Firmware that hardcodes
> 868 MHz will transmit out of band on a 433 MHz unit.

---

## 4. SX1261 vs SX1262 vs SX1268 — precisely

One datasheet covers the SX1261 and SX1262 together, and **a claim copied from the wrong column is
the most common error made with this document** **[DS]**
([SX1262, opening section](../../components/semtech/sx1262/README.md)).

| | **SX1261** | **SX1262** | **SX1268** |
|---|---|---|---|
| Max RF output | **+14 dBm** nominal, +15 dBm with special settings **[DS]** | **+22 dBm** **[DS]** | **+22 dBm class** **[SRC]** |
| `SetTxParams` range | **−17 … +14 dBm** (`0xEF`…`0x0E`) **[DS]** | **−9 … +22 dBm** (`0xF7`…`0x16`) **[DS]** | −9 … +22 dBm **[SRC]** |
| RadioLib's enforced range | −17 … **+15** (`SX1261.cpp:42`) **[SRC]** | −9 … +22 (`SX1262.cpp:212`) **[SRC]** | −9 … +22 (`SX1268.cpp:213`) **[SRC]** |
| RadioLib's enforced frequency range | — | **150 – 960 MHz** (`SX1262.cpp:179`) **[SRC]** | **410 – 810 MHz** (`SX1268.cpp:180`) **[SRC]** |
| **PA supply** | `VDD_IN` tied to **`VREG`** **[DS]** | `VDD_IN` tied to **`VBAT`** **[DS]** | as SX1262 **[REC]** |
| `SetPaConfig` `deviceSel` | **`0x01`** **[DS]** | **`0x00`** **[DS]** | own constant **[SRC]** |
| `hpMax` | **no effect** **[DS]** | selects PA size; **`0x07`** for +22 dBm **[DS]** | as SX1262 **[REC]** |
| OCP after `SetPaConfig` | **60 mA** (`0x18`) **[DS]** | **140 mA** (`0x38`) **[DS]** | — |
| TX current at 868/915 MHz, full power | **25.5 mA @ +14 dBm** **[DS]** | **118 mA @ +22 dBm** **[DS]** | — |
| **DC-DC scope** | **whole IC** **[DS]** | **IC core only — PA runs from `VBAT`** **[DS]** | as SX1262 **[REC]** |
| Errata §15.2 PA clamp fix | **not applicable** | **required** | required |

**The PA difference is a supply-topology difference, not a setting.** The SX1261's PA is fed from the
internal regulator; the SX1262's is fed straight from the battery rail. That is why the SX1262's
DC-DC cannot help transmit current (§1.5), why its over-current limit is more than twice as high, and
why the two parts are **not** interchangeable on a board even though they share a pinout, a command
set and a register map.

**RadioLib encodes the distinction structurally, and that is itself confirmation** **[SRC]**, read
live 2026-09-02: separate `SX1261`, `SX1262` and `SX1268` classes over a shared `SX126x` base, each
with its own `checkOutputPower()` range — and **`fixPaClamping()` is called from every `SX1262` and
`SX1268` `begin`/`beginFSK` variant (`SX1262.cpp:62,94,125,153`; `SX1268.cpp:62,94,125,153`) and from
no `SX1261` path at all**, exactly matching the datasheet's "SX1262 only" note on errata §15.2
**[DS]**.

**How to tell which you have when the schematic will not say.** The
[SX1262 record's method](../../components/semtech/sx1262/README.md) is worth generalising: the
firmware asked for **22 dBm**, and +22 dBm is unreachable on an SX1261 — its `SetTxParams` range stops
at +14 and RadioLib would reject it. **A power request above +15 dBm that a driver accepts is
evidence of a 62.** Circumstantial, but strong, and much easier than a teardown.

⚠ **The chip's frequency range is not the module's.** The SX1262 synthesiser covers **150 – 960 MHz
continuously** **[DS]**; the Stamp module is sold as **868 – 923 MHz** **[DOC]**. The narrowing is
imposed by a matching network and antenna nobody outside the vendor has seen
([G6](../../components/semtech/sx1262/README.md#10-caveats-gaps-and-errata)). Read the datasheet's
floor as silicon capability, never as a usable setting.

---

## 5. The host interface, and the five things that go wrong

### 5.1 Commands, not registers

The SX126x is driven by an **opcode-based command set** over SPI mode 0 (CPOL 0, CPHA 0), MSB first,
**up to 16 MHz** **[DS]**. There is no flat register file in the usual sense: registers are reached
through `WriteRegister` (`0x0D`) / `ReadRegister` (`0x1D`) with a 16-bit address, and the packet
buffer through `WriteBuffer` (`0x0E`) / `ReadBuffer` (`0x1E`) **[DS]**. The full opcode table is in
the [SX1262 record §4.2](../../components/semtech/sx1262/README.md#42-command-structure).

Two ordering rules that are not incidental **[DS]**:

- **`SetPacketType` must precede `SetModulationParams` and `SetPacketParams`**, because the parameter
  encodings differ per modem.
- **`SetRegulatorMode` is valid only in `STDBY_RC`.**

Semtech devotes an entire section (§14.5) to "Issuing Commands in the Right Order" **[DS]**. Treat the
command set as a state machine, not as a bag of setters.

### 5.2 `BUSY` is a mandatory handshake

**The single most important behavioural fact about this family** **[DS]**
([SX1262 §4.3](../../components/semtech/sx1262/README.md#43-busy--a-mandatory-handshake-not-a-status-led)):

- **Every "write" command raises `BUSY`** within `T_SW ≤ 600 ns` of the NSS rising edge. The host must
  wait for it to fall.
- **"Read" commands do not raise it** — but Semtech still says "it is essential to wait for the BUSY
  line to go low before sending an SPI command (either a 'read' or a 'write' command)", **because
  `BUSY` also rises to service the chip's own internal interrupts.**
- **In sleep, `BUSY` is held high through a 20 kΩ resistor** and falls when the chip leaves sleep —
  which is the correct, timing-independent way to satisfy `t10`, the **100 µs** minimum from NSS
  falling to the first SCK when leaving sleep **[DS]**.
- **`BUSY` falls at different moments per mode:** in FS when the PLL locks, in RX when the receiver is
  up, in TX **when the PA has ramped and preamble transmission starts**.

The [Ebyte record puts the practical consequence best](../../components/ebyte/e22-900m22s/README.md#2-the-sx1262-inside):
**drivers ported from the SX127x — which has no `BUSY` — omit `WaitOnBusy()` and produce intermittent,
timing-dependent failures that look like SPI corruption.** It is the number-one SX126x integration
bug.

**Verification test for any SX126x driver:** does it wait on `BUSY` before *every* transaction, and
does it call `SetDio2AsRfSwitchCtrl`? A driver failing either was probably ported from the SX127x
([E22 §6](../../components/ebyte/e22-900m22s/README.md#6-drivers-and-libraries)).

### 5.3 `DIO1`, and why modules bring out only that one

Ten interrupt sources, each maskable and each mappable to any of `DIO1`/`DIO2`/`DIO3` via
`SetDioIrqParams` (`0x08`) **[DS]**: `TxDone`, `RxDone`, `PreambleDetected`, `SyncWordValid` (FSK),
`HeaderValid`/`HeaderErr` (LoRa), `CrcErr`, `CadDone`, `CadDetected`, `Timeout`.

`DIO1` is documented as "the generic IRQ line, any interrupt can be mapped to DIO1" **[DS]** — which
is exactly why a module that exposes one DIO exposes that one
([Stamp-LoRa-1262 §3.3](../../components/m5stack/stamp-lora-1262/README.md#33-lora_irq-is-the-sx1262s-dio1)).

⚠ **In Reset, Start-up and Sleep all three DIOs are pulled down (50 kΩ) and `BUSY` is pulled up**
**[DS]**. Only from `STDBY_RC` upward are they driven. **A DIO used for an external function is not
driven while the chip sleeps** — which matters for both of the next two sections.

### 5.4 `DIO3` as a TCXO supply — and the error you are supposed to ignore

`SetDIO3AsTcxoCtrl(tcxoVoltage, delay[23:0])` (opcode `0x97`) hands `DIO3` to the state machine, which
drives it to a programmed voltage whenever the reference is needed and power-cycles the TCXO
otherwise **[DS]**. Settings run 1.6 / 1.7 / 1.8 / 2.2 / 2.4 / 2.7 / **3.0** / 3.3 V (`0x00`…`0x07`),
±50 mV **[DS]**.

Four things catch people, all **[DS]**
([SX1262 §5.2](../../components/semtech/sx1262/README.md#52-dio3-as-a-tcxo-supply)):

1. ⚠ **`VDDop > VTCXO + 200 mV`.** The regulator targets 200 mV below its supply. A 3.3 V rail with a
   3.0 V setting leaves exactly 100 mV of margin over the rule — on a rail that also feeds the PA.
2. **`delay` is in units of 15.625 µs** and gates the 32 MHz clock until the TCXO settles. **It is
   added to every `STDBY_RC` → TX/RX transition.** Go to `STDBY_XOSC` once and wait there, rather
   than paying it per packet.
3. ⚠ **`XOSC_START_ERR` is *expected* at POR and at every cold-start sleep wake when a TCXO is used**,
   because the chip does not yet know it is TCXO-clocked. Semtech: *"It is an expected behaviour…
   The user should simply clear this flag with the ClearDeviceErrors command."* **An error handler
   that treats it as fatal will refuse to start a perfectly good radio**
   ([G8](../../components/semtech/sx1262/README.md#10-caveats-gaps-and-errata)).
4. **Issuing the command forces the `XTA` trimming cap register to `0x2F` (33.4 pF)**, unconditionally.

**Why a TCXO at all?** Because frequency drift across a packet must stay inside `Freq_drift_max`, and
at long symbol times that gets hard **[DS]**. Semtech is explicit about the mechanism: an SX1262
transmitting +22 dBm from a 4 × 4 mm package heats up, "careful PCB design using thermal isolation
techniques must be applied between the circuit and the crystal resonator", and where that isolation
is impossible **the recommendation is a TCXO** **[DS]**. LoRaWAN system guidance expects **±30 ppm**
overall across initial error, temperature and ageing **[DS]**.

⚠ **On a module you usually cannot see whether a TCXO is fitted.** The
[Stamp-LoRa-1262 record's G3](../../components/m5stack/stamp-lora-1262/README.md#5-caveats-and-gaps)
is the general warning: getting this wrong yields a radio that **appears to initialise and then fails
to transmit or receive** — the hardest class of fault to diagnose. **The evidence you can get is what
the working vendor firmware configures.** Treat that as the known-good starting point and change it
only with a spectrum analyser to hand.

### 5.5 `DIO2` as RF switch control

`SetDIO2AsRfSwitchCtrl(enable)` (opcode `0x9D`) makes `DIO2` **high during TX and low in every other
mode** **[DS]** — a one-line antenna-path selector with exactly the right timing, which is the point:
getting TX/RX switching right in host software is error-prone.

**This is the expected topology, not an exotic one.** Semtech devotes two application-schematic
sections to it, and omitting the switch costs measurable sensitivity: with a direct Rx/Tx tie instead
of a switch, LoRa at BW 125 kHz / SF12 falls from **−137 to −133 dBm**, and 2-FSK at 4.8 kb/s from
−118 to −115 dBm **[DS]**. **A 4 dB link-budget penalty** for saving a part. Note also that the
headline sensitivity figures **exclude RF switch insertion loss**, so the real number sits below them
either way.

The [Ebyte E22 record documents the canonical implementation](../../components/ebyte/e22-900m22s/README.md#42--the-rf-switch-is-driven-by-dio2-inverted--an-elegant-detail-worth-documenting)
**[PCB]** — `DIO2` drives `TXEN` directly and a `74LVC1GU04` unbuffered inverter generates the
complementary `RXEN`, with a **100 kΩ pull-down** holding the front end in **receive** whenever the
radio is unpowered, in reset, or has `DIO2` high-impedance (§5.3). Read it as the reference pattern:

- the two enables can never be asserted together;
- the safe default is receive, never transmit;
- and **if the driver forgets `SetDio2AsRfSwitchCtrl`, the module receives but never transmits, with
  no error anywhere.**

⚠ **A module-level "antenna switch" pin is not the same signal.** A board can have **two** switch
controls — one automatic and internal on `DIO2`, one manual and external — and conflating them is an
easy and expensive mistake
([SX1262 §5.3.1](../../components/semtech/sx1262/README.md#531-the-papermono-evidence-and-the-two-switches-that-are-not-the-same-thing),
[Stamp G4](../../components/m5stack/stamp-lora-1262/README.md#5-caveats-and-gaps)).

### 5.6 Semtech's four mandatory workarounds — and a resolved open question

Semtech publishes four **Known Limitations** in datasheet §15. **All four are register writes the
datasheet says to make; none is optional; a driver that omits them is subtly wrong rather than
obviously broken** **[DS]**
([SX1262 §8](../../components/semtech/sx1262/README.md#8-register-level-workarounds-you-must-implement)).

The SX1262 record leaves as an explicit gap
([G4](../../components/semtech/sx1262/README.md#10-caveats-gaps-and-errata)) whether RadioLib applies
them. **Read live from `jgromes/RadioLib` @ `master` on 2026-09-02, it applies all four** **[SRC]**:

| Datasheet | Symptom | RadioLib | Called from |
|---|---|---|---|
| **15.1** | Sensitivity loss on any LoRa receiver hearing a 500 kHz signal from an SX126x | `SX126x::fixSensitivity()` — `SX126x.cpp:1277`, register `0x0889` | `SX126x.cpp:1095` |
| **15.2** | PA over-voltage clamp over-protective; **5–6 dB** loss on a reasonable mismatch. **SX1262 only** | `SX126x::fixPaClamping(bool)` — `SX126x.cpp:1295`, register `0x08D8` | `SX1262.cpp:62,94,125,153`; `SX1268.cpp:62,94,125,153`; **never from `SX1261`** |
| **15.3** | Implicit-header RX timeout timer not stopped on `RxDone`; fires spuriously later | `SX126x::fixImplicitTimeout()` — `SX126x.cpp:1313`, registers `0x0902` / `0x0944` | `SX126x.cpp:468` |
| **15.4** | Packet loss on longer packets with inverted IQ | `SX126x::fixInvertedIQ(uint8_t)` — `SX126x.cpp:1338`, register `0x0736` | IQ-polarity path |

Each function carries a source comment naming the datasheet section it implements **[SRC]**.

⚠ **Scope of this resolution.** It was verified on **`master`, `library.properties` version 7.7.1**.
The [PaperMono firmware pins **7.2.1**](../../devices/m5stack/papermono/features/lora.md) and the
vendor **patches** it; **7.2.1 was not read**. So G4 is resolved for current RadioLib and **remains
open for the pinned version**. This finding should be folded back into the
[SX1262 record](../../components/semtech/sx1262/README.md) by whoever next edits it.

Note also that **`SetPaConfig` silently reprograms over-current protection** — `0x18` (60 mA) after
POR, `0x38` (**140 mA**) once `deviceSel` selects the SX1262 **[DS]**. Any manual OCP change must come
*after* `SetPaConfig` or it is overwritten. Firmware calling `setCurrentLimit(140.0f)` is re-applying
the default, not tuning anything **[SRC]**.

---

## 6. Antenna and RF

Unlike NFC (see the [NFC guide §4](../nfc/README.md)), sub-GHz LoRa is a genuine **far-field, 50 Ω**
problem. **[REC]** throughout this section except where marked.

- **Everything is 50 Ω**: the PA output match, the transmission line to the connector, the connector,
  the antenna. A mismatch anywhere reflects power back into the PA.
- ⚠ **Never transmit without an antenna or a 50 Ω load.** "A 22 dBm PA into an open circuit can
  damage itself" ([E22 §5](../../components/ebyte/e22-900m22s/README.md#5-regulatory-notes)) **[INF]**
  in that record. The SX1262 does have a **PA over-voltage clamp** — which is precisely the
  over-protective mechanism errata §15.2 relaxes **[DS]**. Note what that means: **applying the §15.2
  workaround makes the chip less eager to protect itself into a mismatch.** Semtech says the
  workaround "improves chip functionality, but is not required to ensure long-term reliability", so
  it is safe — but do not read it as "mismatch no longer matters".
- **The PA settings and the matching network are coupled.** `paDutyCycle` "will affect the
  distribution of the power in the harmonics and should thus be selected to work in conjunction of a
  given matching network" **[DS]**. **Changing `paDutyCycle` on a module you did not design is not a
  software-only decision** ([SX1262 §1.1](../../components/semtech/sx1262/README.md#11-150960-mhz-silicon-versus-an-868923-mhz-module)).
- **Re-matching for lower power is a real efficiency win, and it is a hardware change.** With the PA
  re-optimised for a lower target — a different `paDutyCycle`/`hpMax` **and** a different matching
  network — +14 dBm costs **45 mA** instead of the 90 mA it costs on a +22 dBm match **[DS]**. Half
  the current, but only with the network to match.
- **Ground plane and layout.** A monopole or chip antenna works against the board's ground plane,
  which is part of the antenna; shortening it detunes the radio. Keep the RF trace short, on a
  controlled-impedance layer, over unbroken ground, with the antenna's keep-out honoured. **[REC]**
- **A battery-supply fact worth designing around** **[DS]**: at +22 dBm the SX1262's output falls
  **2 dB at 2.7 V, 3 dB at 2.4 V and 6 dB at 1.8 V**. **A radio asked for +22 dBm delivers +16 dBm on
  a nearly-flat cell.** Regulating the radio rail avoids it; running straight from a cell does not.
- **`CalibrateImage` matters.** The SX126x uses a low-IF architecture, so the RX frequency is the TX
  frequency minus the IF; `CalibrateImage` exists for this and **should be run for the band in use**
  **[DS]**.

---

## 7. Software

| Option | Scope | Licence **[DOC]** | Maintenance, checked 2026-09-02 **[DOC]** | Reach for it when |
|---|---|---|---|---|
| **RadioLib** (`jgromes/RadioLib`) | PHY for **12 radio families** plus LoRaWAN, APRS, AX.25, RTTY, SSTV, ADS-B, pagers | **MIT** | ✅ **7.7.1**, released 2026-05-31, pushed **2026-08-22** | ⭐ **The default.** Arduino and ESP-IDF; first-class `SX1262`; explicit `BUSY` handling; all four errata workarounds (§5.6) |
| Semtech **`LoRaMac-node`** (`Lora-net/LoRaMac-node`) | Reference LoRaWAN node + SX126x HAL | `NOASSERTION` | ⚠ last push **2024-07-03** | Authoritative reference, and certification lineage. Heavy |
| Semtech **LoRa Basics Modem** (`Lora-net/SWL2001`) | Current LoRaWAN stack | BSD-3-Clause-Clear | last push **2025-10-15** | Semtech's live stack — the successor path to LoRaMac-node |
| **`mcci-catena/arduino-lmic`** | Arduino LoRaWAN (LMIC lineage) | MIT | last push **2026-08-05** | Existing LMIC codebases. ⚠ LMIC is memory-hungry and its timing assumptions are strict |
| **Meshtastic** (`meshtastic/firmware`) | A whole application: mesh, phone apps, region presets | **GPL-3.0** | ✅ pushed **2026-09-02**; 8 200+ stars | Off-grid messaging out of the box — and a good reference for per-region tables |
| Zephyr `drivers/lora/sx126x.c` | In-tree Zephyr driver | Apache-2.0 | mainline **[REC]** | Zephyr targets |
| Raw SPI | — | — | — | Feasible — §5 is the whole interface — but §5.6's four workarounds are exactly what a hand-rolled driver silently omits |

### 7.1 RadioLib's structure

Read live from the repository tree, 2026-09-02 **[SRC]** — 409 files:

```
src/Module.h  src/Hal.h            the porting boundary: implement a Hal, pass a Module
src/modules/                       CC1101 · LLCC68 · LR11x0 · LR2021 · RF69 · RFM2x ·
                                   SX123x · SX126x · SX127x · SX128x · Si443x · nRF24
src/modules/SX126x/
   SX126x.{cpp,h}                  shared base: BUSY, commands, the four errata fixes
   SX126x_commands.{cpp,h}         opcode layer
   SX126x_registers.h              the 16-bit register addresses
   SX1261.{cpp,h}  SX1262.{cpp,h}  SX1268.{cpp,h}   per-part PA and range limits
   STM32WLx.{cpp,h}               the SX126x core inside an STM32WL
   SX126x_LR_FHSS.cpp
src/protocols/LoRaWAN/             LoRaWAN.cpp · LoRaWANBands.cpp (§3) · package managers
src/protocols/                     APRS · AX25 · RTTY · SSTV · Morse · Pager · ADSB · …
```

**The porting story is `Hal.h` and `Module.h`.** A platform integration implements a hardware
abstraction and hands the library a `Module` — which is precisely what the
[PaperMono vendor firmware does](../../devices/m5stack/papermono/features/lora.md): a thin
`RadioLibHal` over the SoC's SPI and GPIO, six pin numbers handed over, and then it gets out of the
way **[SRC]**. That is the shape to copy.

**`STM32WLx` in the same directory is worth noticing**: the STM32WL is an SX126x core on the same die
as a Cortex-M, so the same driver serves it. If you are choosing between a discrete radio and an
integrated SoC, the software cost of that decision is nearly zero with this library. **[INF]**

### 7.2 ⚠ Pinning is not optional, and nobody does it the same way

- **The PaperMono firmware pins RadioLib at `7.2.1`, commit `b91c6af1…`, and *patches* it** to remove
  `idf_component.yml` so it builds as a plain ESP-IDF component **[SRC]**.
- **M5Stack's own published PlatformIO snippet pins nothing** — `RadioLib = https://github.com/jgromes/RadioLib`
  pulls `master` **[DOC]**. Building from the documentation does **not** reproduce the shipped
  firmware ([Stamp §4](../../components/m5stack/stamp-lora-1262/README.md#4-software)).
- **Meshtastic pins a raw commit archive**: `[radiolib_base]` in `platformio.ini:121-124` points at
  `https://github.com/jgromes/RadioLib/archive/510e00cf….zip` **[SRC]**, read live 2026-09-02. That
  is what "pinned in practice" looks like for a project that must ship.
- ⚠ **Licence mismatch, flagged not confirmed.** The
  [Stamp record notes RadioLib as LGPL-3.0 upstream while the M5Stack demo carrying it is MIT](../../components/m5stack/stamp-lora-1262/README.md#4-software),
  "not verified in this pass". **`library.properties` on `master` today declares `MIT`** and the
  GitHub API reports `MIT` **[DOC]**, 2026-09-02 — so either the licence changed or the earlier note
  was mistaken. **Recorded as an unresolved discrepancy, not silently corrected**; the licensing of
  the *pinned 7.2.1 tree* was not checked and is what would actually matter.

---

## 8. Link budget and range, honestly

**Marketing range figures for LoRa are meaningless**, and it is easy to show why with the datasheet's
own numbers.

```
TX power (SX1262, max)                       +22 dBm      [DS]
RX sensitivity, SF12 / BW 125 kHz, boosted   −137 dBm     [DS]
                                             ─────────
link budget                                   159 dB      [INF]

Free-space path loss at 868 MHz, 1 km:
  FSPL = 32.44 + 20·log10(868) + 20·log10(1) = 91.2 dB    [INF]
Distance for 159 dB, 0 dBi antennas both ends:
  20·log10(d_km) = 159 − 91.2 = 67.8  ⇒  d ≈ 2 450 km     [INF]
```

**Nobody gets 2 450 km on the ground.** That gap — between a genuine 159 dB budget and a real result
of a few kilometres in a town — *is* what "range" means in practice. Everything in it is the
environment: terrain, buildings, foliage, antenna height, polarisation, body loss, and the fact that
free-space propagation does not exist near the ground.

**What actually determines range, in descending order of leverage [REC]:**

1. **Antenna height and line of sight.** Dominates everything else. This is why the spectacular LoRa
   records are balloons and satellites — where the free-space calculation nearly *does* apply.
2. **Antenna quality and matching**, at both ends. A 4 dB error here is a 60 % distance change in
   free space and often more in clutter.
3. **Spreading factor.** 2.5 dB per step (§1.1) — and 2× airtime, and therefore duty-cycle cost.
4. **Bandwidth.** ~3 dB per halving (§1.2), same airtime cost.
5. **Transmit power.** The *least* leverage per unit of cost: +8 dB from +14 to +22 dBm costs ~2.6×
   the transmit current (§4) and is capped by regulation (§3) long before it is capped by silicon.

**Honest estimation procedure [INF]:**

- Compute the budget: `TX dBm − RX sensitivity dBm`, using the sensitivity row for **your** SF *and*
  BW (interpolating if your BW is not in the table — see §1.2's 62.5 kHz gap).
- **Subtract 4 dB if the front end has no TX/RX switch** (§5.5) **[DS]**, plus the real switch's
  insertion loss if it has one, plus connector and cable loss.
- **Subtract antenna inefficiency at both ends.** A small internal FPC antenna is not 0 dBi.
- Then **do not convert the remainder to a distance**. Use it comparatively: as a budget to spend on
  SF, on a better antenna, or on height — and **measure the actual link**, because the propagation
  term is the only one you cannot compute.

⚠ **The honest state of the evidence in this library:** for the two LoRa devices documented here,
**no range, throughput, sensitivity, TX current or battery-impact figure exists from the vendor or
from anyone in the community**
([G15](../../components/semtech/sx1262/README.md#10-caveats-gaps-and-errata),
[E22 §9](../../components/ebyte/e22-900m22s/README.md#9-open-questions)) — verified negatives, not
oversights.

---

## 9. Debugging

### 9.1 Failure signatures

| Symptom | Cause class | Discriminator |
|---|---|---|
| `begin()` fails immediately | **Power or reset** | Is the radio's rail actually enabled? Is reset released? On modules with an expander-driven reset, **no I²C means no reset** |
| Intermittent, timing-dependent SPI corruption | ⚠ **`BUSY` ignored** | §5.2. Driver ported from SX127x. **Check first** |
| `BUSY` stuck **high** forever | **Never left sleep, or no reference clock** | In sleep `BUSY` is held high through 20 kΩ **[DS]**. If it never falls: the chip is not waking (check `t10`, 100 µs after NSS falls), or the 32 MHz reference never started — see the next row |
| Initialises cleanly, then **never transmits or receives** | ⚠ **TCXO misconfiguration** | The classic. TCXO configured on a crystal-only design, or a crystal design given no TCXO configuration. §5.4. The [device record calls this out by name](../../devices/m5stack/papermono/features/lora.md) |
| Init aborts on a device error at every cold start | **`XOSC_START_ERR` treated as fatal** | It is **expected** with a TCXO. Clear it with `ClearDeviceErrors` **[DS]**. §5.4 |
| Receives fine, **never transmits**, no error anywhere | ⚠ **`SetDio2AsRfSwitchCtrl` not called** | §5.5. On an inverter-based front end the switch sits in RX forever. **Predictable and silent** |
| Transmits, receives nothing from a known-good peer | **Configuration mismatch** | Sync word, SF, BW, CR, preamble length, header mode, IQ polarity, CRC — **all must match**. SF is orthogonal, so a mismatch is total, not degraded |
| Works against a new radio, fails against an old one at SF6 | ⚠ **SF6 is not interoperable with SF6 on an SX1276** **[DS]** | SF5/SF6 were redefined in the SX1261/2. Also use **12 preamble symbols** at SF5/SF6 ([G10](../../components/semtech/sx1262/README.md#10-caveats-gaps-and-errata)) |
| Sensitivity worse than the datasheet, only at 500 kHz | **Errata §15.1 not applied** | §5.6 |
| Output power 5–6 dB low | **Errata §15.2 not applied**, or antenna mismatch | §5.6, §6 |
| Spurious timeouts after an implicit-header receive | **Errata §15.3** | §5.6 |
| Range collapses as the battery drains | **PA supply droop** | −2 dB at 2.7 V, −6 dB at 1.8 V **[DS]**. §6 |
| Battery life far worse than expected | **Receive current, not transmit** | §1.5. Check the LDO/DC-DC selection before optimising the transmit path |
| Radio disappears after a sleep cycle | **Rail was cut** | If the module's supply is gated externally, re-run the entire bring-up; the chip's own sleep modes are a different mechanism |
| Everything works, throughput is glacial | **SF12 was the default** | §1.4. Change it deliberately |

### 9.2 Two diagnostics worth wiring in early

- **`GetDeviceErrors` (`0x17`) / `ClearDeviceErrors` (`0x18`)** **[DS]**. Read and log them at every
  init. This is where `XOSC_START_ERR` and PLL/PA problems surface, and most integrations never look.
- **`GetPacketStatus` (`0x15`) and `GetRssiInst` (`0x14`)** **[DS]**. RSSI *and* SNR on every received
  packet turn "the link is bad" into a number. SNR against the §1.1 table tells you directly how many
  spreading-factor steps of margin you have — which is the most actionable diagnostic in LoRa.

---

## 10. Choosing a radio

⚠ Rows for parts without a record in this repository are **[REC]**; RadioLib support is **[SRC]**.

| Option | vs SX1262 | Choose when |
|---|---|---|
| **Semtech SX1262** | The baseline here: 150–960 MHz, +22 dBm, LoRa + LR-FHSS + (G)FSK, `BUSY` handshake, command interface **[DS]** | Default for new sub-GHz work. Best-documented option in this library |
| Semtech SX1261 | +14/+15 dBm, PA from `VREG`, DC-DC covers the whole IC **[DS]** | Duty-cycle-limited regions where +22 dBm is illegal anyway, and receive-heavy nodes — its DC-DC helps everywhere |
| Semtech SX1268 | +22 dBm class, **410–810 MHz** **[SRC]** | 433 MHz and Chinese 470 MHz allocations |
| **SX1276 / SX1278 (SX127x)** | ⚠ **Not a drop-in.** No `BUSY`, register-based rather than command-based, **entirely different driver** **[REC]**; RadioLib has a separate `SX127x` module **[SRC]** | Only for compatibility with an existing SX127x deployment. ⚠ **SF6 is not interoperable across the generations** **[DS]** |
| LLCC68 | Cost-reduced SX1262 sibling; **restricted SF/BW combinations** **[REC]**; own RadioLib module **[SRC]** | High volume where the restrictions are acceptable |
| **Semtech LR1110 / LR11xx** | Adds multi-constellation **GNSS** and **Wi-Fi passive scanning** for geolocation **[REC]**; RadioLib `LR11x0` module **[SRC]** | Asset tracking, where "where is it" beats "how far does it reach" |
| **STM32WL** | SX126x core **on the same die** as a Cortex-M **[REC]**; RadioLib `STM32WLx` in the SX126x directory **[SRC]** | One chip instead of two, and the same driver |
| **Ebyte E22-900M22S** (module) | SX1262 **plus external PA/LNA and RF switch**; needs explicit `RXEN`/`TXEN` handling a bare SX1262 does not — [documented here](../../components/ebyte/e22-900m22s/README.md) | More output than a bare chip, with a stamp footprint. ⚠ **worse regulatory headroom**; ⚠ **`E22-...T` variants are a completely different UART product** |
| **M5Stack Stamp-LoRa-1262** (module) | SX1262 in a 13-pin stamp with an FPC antenna — [documented here](../../components/m5stack/stamp-lora-1262/README.md) | M5Stack ecosystem. ⚠ **no module datasheet exists**; RF output, antenna gain, matching, TCXO and internal DIO use are all undocumented (G1) |
| **RAK3172 / RAK4630** (module) | SX1262 **plus an MCU** running the stack inside the module **[REC]** | When you want the LoRaWAN stack to be someone else's problem |

**The selection question that actually matters** is not which radio — the SX126x family answers that
for most sub-GHz work — but **where the stack runs and who owns certification**. A bare chip gives
maximum control and maximum obligation. A module with an MCU inside gives you a stack and possibly a
modular approval. A module without one, like both documented here, gives you neither, plus an
undocumented matching network.

⚠ **Module-level certification does not transfer automatically** into your product with your antenna
([E22 §5](../../components/ebyte/e22-900m22s/README.md#5-regulatory-notes)) **[GAP]** in that record —
and for both modules documented here, **no certification of any kind is published at all** **[DOC]**.

---

## 11. Device-specific pages

| Device | Radio | Applicability |
|---|---|---|
| [**M5Stack PaperMono**](../../devices/m5stack/papermono/features/lora.md) | SX1262 inside a `Stamp-LoRa-1262` module | **Applies with deltas** — RadioLib is not given the reset pin (it is behind an expander), the module's rail is gated externally, `DIO2`/`DIO3` are consumed inside the module, and the vendor default is a maximum-range SF12 configuration |
| [Nicolai Electronics Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) | SX1262 inside an [Ebyte E22-900M22S](../../components/ebyte/e22-900m22s/README.md) | **Applies with deltas** — external PA/LNA with inverter-generated `RXEN`, the radio belongs to a companion SoC rather than the application processor, and a **different module is fitted on 433 MHz units** |
| [M5Stack PaperMono-Lite](../../devices/m5stack/papermono-lite/README.md) | **none fitted** | Not applicable |

---

## 12. Evidence boundary — and what could not be sourced

**No measurement anywhere in this guide.** Inherited claims come from the
[SX1262](../../components/semtech/sx1262/README.md),
[Stamp-LoRa-1262](../../components/m5stack/stamp-lora-1262/README.md) and
[Ebyte E22-900M22S](../../components/ebyte/e22-900m22s/README.md) records and the
[PaperMono LoRa feature guide](../../devices/m5stack/papermono/features/lora.md) as they stood on
**2026-09-02**, carrying their labels transitively.

**New to this page, live-verified 2026-09-02 [SRC]/[DOC]:** the RadioLib module and protocol layout;
the per-part power and frequency ranges at `SX1261.cpp:42`, `SX1262.cpp:179,212`,
`SX1268.cpp:180,213`; **all four errata workarounds and their call sites** (§5.6, resolving
[G4](../../components/semtech/sx1262/README.md#10-caveats-gaps-and-errata) for current RadioLib);
`getTimeOnAir` at `SX126x.h:634` / `SX126x.cpp:812`; the **entire §3 band table** from
`LoRaWANBands.cpp`; Meshtastic's pinned RadioLib commit at `platformio.ini:121-124`; and every
maintenance and licence status in §7.

**New and derived here [INF]:** the §1.1 "2.5 dB per SF step" reading; the §1.4 symbol-time and
bit-rate tables and their cross-check against the recalled LoRaWAN DR table; the §1.4 airtime
estimate for the vendor configuration; the §1.5 receive-dominates-transmit arithmetic; the §3
"a dozen frames per hour" and "US915's 400 ms dwell cap forbids SF12/125 kHz" conclusions; the §8
link-budget and free-space calculation.

### Claims I could not source

| Claim | Why it is unsourced | Risk if wrong |
|---|---|---|
| **"A LoRa symbol carries `SF` raw bits" (§1.4)** | The datasheet gives `2^SF` **chips** per symbol and `Rs = BW/2^SF`; the bits-per-symbol step is standard CSS theory with no document here | **Low** — the derived rates reproduce the recalled LoRaWAN DR table to within rounding, which is a strong check |
| **The LoRaWAN DR0–DR5 rates used as a cross-check (§1.4)** | LoRa Alliance **RP002 Regional Parameters** is not held | Low; it is a check, not a load-bearing claim |
| **The exact closed-form airtime formula** | Semtech application notes (`AN1200.13` and relatives) are **not held** — and [Semtech's document portal is `blocked`](../../components/semtech/sx1262/README.md#11-sourcing) | **Low, because it is avoided**: §1.4 gives an order-of-magnitude estimate and points at `getTimeOnAir()` for the real number |
| **All regional/legal detail beyond RadioLib's table (§3)** | ETSI EN 300 220, FCC Part 15.247/15.249, ARIB T-108 and RP002 are **all** unheld. RadioLib's table is a *library's* encoding of them, which is evidence about the library first and the law second | **High if relied upon.** Read the regulation. The 1 % / 36 s and 400 ms figures are sourced *as RadioLib constants* |
| **LoRaWAN device-class behaviour (§2)** | Recalled; the specification is not held | Low for the architectural point |
| **Meshtastic's mesh and preset behaviour (§2)** | Only the RadioLib pin was read from its repository; the protocol was not | Low |
| **SX1268 PA topology, LLCC68 restrictions, SX127x architecture, LR11xx and STM32WL capability (§4, §10)** | No datasheet held for any of them. RadioLib's enforced ranges *are* sourced and are the strongest evidence in those rows | **Moderate** — the table decides part selection |
| **50 Ω / ground-plane / layout guidance (§6)** | General RF practice; no document behind it here. `AN1200.37` "Recommendations for Best Performance" is cited by the datasheet itself and **was not located at all** | Moderate for a real design review |
| **Zephyr's `sx126x.c` status (§7)** | Not checked live this pass, unlike every other row | Low |
| **Whether the *pinned* RadioLib 7.2.1 applies the four workarounds (§5.6)** | Only `master` was read | **Moderate** — it is the version actually shipping on a documented device |

### Where this guide sits relative to the deep records

**No contradiction was found.** Three things to feed back:

1. **§5.6 resolves [SX1262 G4](../../components/semtech/sx1262/README.md#10-caveats-gaps-and-errata)
   for current RadioLib** — all four §15 workarounds are implemented, and `fixPaClamping` is
   correctly SX1262/SX1268-only. The gap remains open for the pinned 7.2.1.
2. **§7.2 records a discrepancy on RadioLib's licence.** The
   [Stamp record flags LGPL-3.0 upstream, "not verified"](../../components/m5stack/stamp-lora-1262/README.md#4-software);
   `master` today declares **MIT**. Recorded as unresolved rather than corrected — the pinned tree
   was not checked, and that is the one that matters.
3. **§1.4's derived rate for the vendor configuration (≈92 bit/s, ≈76 with LDRO) agrees with the
   SX1262 record's "tens of bits per second"** characterisation. Agreement, not conflict — noted so
   the arithmetic is available if anyone needs the number rather than the adjective.

---

## Related

- [**Semtech SX1262**](../../components/semtech/sx1262/README.md) — the deep record: opcodes, `BUSY` timing, DIO2/DIO3, LDO vs DC-DC, sensitivity and current tables, the four errata
- [**M5Stack Stamp-LoRa-1262**](../../components/m5stack/stamp-lora-1262/README.md) — a module with **no datasheet**, and what that costs
- [**Ebyte E22-900M22S**](../../components/ebyte/e22-900m22s/README.md) — SX1262 with an external PA/LNA; the canonical `DIO2`-plus-inverter RF-switch pattern, and the band-variant trap
- [M5Stack PaperMono — LoRa feature guide](../../devices/m5stack/papermono/features/lora.md) — the device-specific companion to this page
- [Nicolai Electronics Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) — the other documented LoRa device
- [**NFC — a device-independent guide**](../nfc/README.md) — the other radio on the PaperMono; the same command-byte, mandatory-errata and undocumented-module patterns recur there
- [Guides index](../README.md) · [Components index](../../components/README.md) · [Devices index](../../devices/README.md)
- [Vendor sourcing guides](../../vendors/README.md) — ⚠ **no Semtech and no Ebyte guide exists yet**; [SX1262 §11](../../components/semtech/sx1262/README.md#11-sourcing) and [E22 §8](../../components/ebyte/e22-900m22s/README.md#8--documentation-gaps--both-primary-documents-are-missing) are what one would open with
