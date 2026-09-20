# NFC — a device-independent guide

> **How does 13.56 MHz NFC actually work, and how do I bring a reader up on an MCU?**
> A cross-cutting guide compiled from the NFC knowledge in this library — principally the
> [ST ST25R3916 record](../../components/stmicroelectronics/st25r3916/README.md) (555 lines,
> built on `DS12484 Rev 8` held locally) and the
> [M5Stack PaperMono NFC feature guide](../../devices/m5stack/papermono/features/nfc.md).
> Compiled **2026-09-02**. **No hardware. No tag has been read by anyone whose report could be
> located.**

## 0. What this guide is, and what it is not

This is the **common** layer the research method asks for in step 13: reusable concepts, APIs,
alternatives, validation and generic pitfalls, **without unqualified device pin assignments**. Where
a concrete example is needed, the device is named and its record linked; no pin number here stands
alone.

It does **not** duplicate the deep records. The
[ST25R3916 record](../../components/stmicroelectronics/st25r3916/README.md) is the authority on that
chip's registers, mode byte, power states and the PaperMono's front end. **Where this guide and a
deep record disagree, the deep record wins.**

Three things this guide does that no single record can:

1. Explains the **standards landscape** once, so component records need not re-derive which ISO
   number corresponds to which real-world card.
2. Treats **antenna and matching** as a subject, because it is the part that most often turns a
   correct driver into a reader that finds nothing.
3. States, in one place, **what is and is not establishable** about NFC read range from documents
   alone — which is the honest answer to the open question in the PaperMono record.

### Evidence labels

| Label | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Datasheet claim, inherited from a component record that cites a section or table of a locally-held document | `not-tested` |
| **[SRC]** | Read out of source at a cited `file:line`, either from a repo record or from a live read on 2026-09-02 | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | Vendor documentation or repository metadata, retrieved 2026-09-02 | `not-tested` |
| **[SCH]** | Inherited label: read out of a schematic by the linked component record | `executed-success` for that record's extraction; `not-tested` electrically |
| **[STD]** | A claim about a formal standard (ISO/IEC, JIS, NFC Forum, ETSI, FCC). ⚠ **This repository holds none of these documents.** Cited by number so it can be checked; the text was not read in this pass | `not-tested`, **unverified against the primary document** |
| **[REC]** | Recalled general engineering knowledge with no document behind it in this repository | **`not-tested` and unsourced** — treat as a lead, not a fact |
| **[INF]** | Derived here, with the reasoning shown | `inferred` |

⚠ **[STD] and [REC] claims are the weak part of this guide and are marked on every occurrence.**
§11 lists what could not be sourced.

---

## 1. The standards landscape

### 1.1 The four physical layers

"NFC" is a marketing umbrella over four mutually unintelligible radio protocols that happen to share
a 13.56 MHz carrier. A reader supports each one separately, and a tag answers exactly one of them.

| NFC Forum name | Standard | Origin | PCD→PICC | PICC→PCD | Typical bit rate |
|---|---|---|---|---|---|
| **NFC-A** | **ISO/IEC 14443** Type A | Philips/NXP MIFARE lineage | 100 % ASK, modified Miller **[STD]** | load modulation, **fc/16 = 847.5 kHz** subcarrier, Manchester **[STD]** | 106 kbit/s, up to 848 **[STD]** |
| **NFC-B** | **ISO/IEC 14443** Type B | Innovatron/ASK lineage | ~10 % ASK, NRZ **[STD]** | BPSK on the same fc/16 subcarrier **[STD]** | 106 kbit/s, up to 848 **[STD]** |
| **NFC-F** | **JIS X 6319-4** (FeliCa), also reachable via **ISO/IEC 18092** | Sony | ~10 % ASK, Manchester **[STD]** | load modulation, **no subcarrier**, Manchester **[STD]** | **212 / 424 kbit/s** **[STD]** |
| **NFC-V** | **ISO/IEC 15693** ("vicinity") | Philips/TI lineage | 10 % or 100 % ASK, 1-of-4 or 1-of-256 pulse position **[STD]** | fc/32 = 423.75 kHz single or dual subcarrier **[STD]** | ~26.5 kbit/s high rate **[STD]** |

The carrier itself is the one thing they genuinely share: **13.56 MHz**, which is why an ST25R3916
runs from a **27.12 MHz** crystal — twice the carrier **[DS]**
([ST25R3916 §1](../../components/stmicroelectronics/st25r3916/README.md)).

**What this means in practice.** Support for one of these tells you nothing about the others. A
chip's marketing sheet listing "ISO14443A/B, FeliCa, ISO15693" is four separate framing engines,
four separate anticollision procedures and — in a library — usually four separate code paths. The
[`M5Unit-NFC` tree carries exactly that shape](../../components/stmicroelectronics/st25r3916/README.md):
`unit_ST25R3916_nfc{a,b,f,v}.cpp` and `src/nfc/layer/{a,b,f,v}/` **[SRC]**. ST's RFAL does the same
with `rfal_nfca.cpp` / `rfal_nfcb.cpp` / `rfal_nfcf.cpp` / `rfal_nfcv.cpp` **[SRC]**
(`stm32duino/NFC-RFAL` @ `main`, read 2026-09-02).

The ST25R3916 supports all four in silicon, plus **NFC tag types 1–5 read** — stated in the
datasheet's own feature table **[DS]**
([§1.1](../../components/stmicroelectronics/st25r3916/README.md#11-st25r3916-vs-st25r3917--the-fitted-part-is-the-full-one)).
Its cut-down sibling the ST25R3917 keeps all four *reader* technologies and loses card emulation,
peer-to-peer target mode, automatic antenna tuning and the capacitive sensor **[DS]**. **The identity
register cannot distinguish them** — both report `ic_type = 0x05` **[DS]**, a trap documented as
[C2](../../components/stmicroelectronics/st25r3916/README.md#9-caveats-and-gaps).

### 1.2 NFC Forum tag types 1–5 and what they are in the shop

The NFC Forum's tag types are an **application-layer** classification layered on the physical
protocols above. They exist so that an NDEF reader can work without knowing the silicon.

| Tag type | Runs on | Real products **[REC]** | Memory, roughly **[REC]** |
|---|---|---|---|
| **Type 1** | NFC-A (ISO 14443-3A, no part 4) | Broadcom/Innovision **Topaz** / Jewel | 96 B – 2 kB |
| **Type 2** | NFC-A (ISO 14443-3A, no part 4) | **NTAG213/215/216**, **MIFARE Ultralight**, MIFARE Ultralight C/EV1 | 48 B – 888 B |
| **Type 3** | NFC-F (FeliCa) | **Sony FeliCa Lite / Lite-S**, FeliCa Standard | 1 – 9 kB |
| **Type 4** | NFC-A **or** NFC-B with ISO 14443-4 (ISO-DEP) and APDUs | **MIFARE DESFire EV1/2/3**, JCOP and other JavaCards, phone HCE | 2 – 8 kB+ |
| **Type 5** | NFC-V (ISO 15693) | **NXP ICODE SLIX/SLIX2**, **ST ST25TV**, TI Tag-it | 112 B – 2 kB |

The **[REC]** label on the product column is deliberate: this repository holds no NXP, Sony or
Broadcom tag datasheet. The mapping is engineering-common-knowledge, it is very unlikely to be
wrong, and it is still not sourced here. Verify against the tag vendor's datasheet before you design
around a specific memory layout.

**Structural consequence.** Types 1, 2 and 5 are *memory* tags — you address blocks or pages
directly. Type 4 is a *smartcard* — you open a logical channel with ISO-DEP and exchange APDUs, and
the tag decides what to answer. That is why a library that reads NTAG fine may not touch DESFire at
all: the latter needs an entire extra protocol layer. RFAL splits them exactly on that line:
`rfal_t1t.cpp`, `rfal_t2t.cpp`, `rfal_t4t.cpp` for the tag operations, and a separate
`rfal_isoDep.cpp` for the ISO 14443-4 transport underneath Type 4 **[SRC]**.

### 1.3 ⚠ MIFARE Classic is not an NFC Forum tag type

This catches people constantly. **MIFARE Classic** is ISO 14443-3A for anticollision and selection,
and then a **proprietary NXP protocol secured by Crypto1** instead of ISO 14443-4. It is not any of
tag types 1–5, NDEF on it is a vendor mapping rather than a Forum specification, and a reader stack
that implements the Forum types will select a MIFARE Classic card and then be unable to read a byte
of it. **[REC]**

Practically, a stack either has Crypto1 or it does not. `M5Unit-NFC` does — its tree carries
`src/nfc/a/mifare` and `src/nfc/crypto/`, and the record notes "MIFARE Classic Crypto1, AES, DESFire
file-system helpers, ISO-DEP, NDEF and APDU are all in-tree" **[SRC]**
([ST25R3916 §7.1](../../components/stmicroelectronics/st25r3916/README.md#71-m5unit-nfc-is-a-from-scratch-driver-not-an-rfal-wrapper)).
ST's RFAL, as packaged for Arduino, does **not**: there is no `mifare` or `crypto` file anywhere in
the 85-file `stm32duino/NFC-RFAL` tree **[SRC]**, a **verified negative** from a full tree
enumeration on 2026-09-02.

That is a real capability difference between the two stacks and it is invisible from either
project's description.

### 1.4 Where NDEF sits

**NDEF** (NFC Data Exchange Format) is a container — a message of typed records — defined by the NFC
Forum above all five tag types **[STD]**. Each tag type has its own *Type n Tag Operation*
specification saying how an NDEF message is stored in that tag's memory model **[STD]**. So "does it
support NDEF" is really five questions.

RFAL's NDEF layer makes the structure legible without reading a single specification **[SRC]**:

```
ndef_message.cpp / ndef_record.cpp     the container format itself
ndef_poller.cpp / ndef_poller_rf.cpp   the read/write state machine over RFAL
ndef_t2t.cpp  ndef_t3t.cpp             per-tag-type memory mapping —
ndef_t4t.cpp  ndef_t5t.cpp             note there is no ndef_t1t.cpp
ndef_type_text.cpp  ndef_type_uri.cpp  the well-known record types
ndef_type_wifi.cpp  ndef_type_bluetooth.cpp   ← handover records
ndef_type_vcard.cpp ndef_type_aar.cpp  ← Android Application Record
```

Two readings worth taking from that listing. **Type 1 tag NDEF mapping is absent** from this package
even though `rfal_t1t.cpp` exists at the protocol layer — so RFAL can talk to a Topaz but this NDEF
layer will not parse one **[SRC]**, `inferred` from the file list, not from a stated limitation.
And **`ndef_type_wifi` and `ndef_type_bluetooth` are the connection-handover records** — the
mechanism behind "tap to pair", which is the single most common real use of NFC beyond identity.

---

## 2. Reader/writer, card emulation, peer-to-peer

| Mode | What the chip is | Realistic on an MCU? |
|---|---|---|
| **Reader/writer** (initiator, poller) | Generates the field; powers and talks to a passive tag | ✅ **Yes.** This is the case every library, every example and every vendor demo covers |
| **Card emulation** (passive target) | Sits in someone else's field and load-modulates a reply | ⚠ **Silicon says yes; evidence says nobody does it.** See below |
| **Peer-to-peer** (NFC-DEP / ISO 18092 active mode) | Two powered devices alternate field generation | ⚠ Technically supported; **strategically dead**. See below |

**Card emulation** is a full ST25R3916 feature — the datasheet's own comparison table lists it as one
of the four things the 3917 loses **[DS]**. But on the one device in this library that fits the part,
the [PaperMono feature guide records](../../devices/m5stack/papermono/features/nfc.md) that
`cfg.emulation` exists and is **set `false` everywhere in vendor code and never demonstrated**
**[SRC]**. The gap between "the silicon can" and "someone has" is the whole of §8 below.

Emulation also has a hardware dimension that is easy to miss: the chip provides an **`EXT_LM`**
external load-modulation gate driver pin and a **PT_memory** (passive target) region reached by its
own mode-byte operations — `0xA0` / `0xA8` / `0xAC` to load the A-config, F-config and TSN, `0xBF` to
read back **[DS]**
([ST25R3916 §3.3](../../components/stmicroelectronics/st25r3916/README.md#33-the-mode-byte-why-the-firmware-reads-register-0x7f)).
If a board leaves `EXT_LM` unpopulated, strong emulation may not be available even though the
register path is.

**Peer-to-peer** deserves a blunt note. The chip supports ISO 18092 active initiator *and* target
**[DS]**, and RFAL ships `rfal_nfcDep.cpp` **[SRC]**. But Android removed Android Beam in Android 10
and the SNEP/LLCP peer-to-peer stack with it **[REC]** — so an MCU implementing P2P has essentially
nothing to talk to. **Card emulation (HCE on the phone side, reader on yours) is the modern
phone-to-device path**, not P2P. Treat any tutorial that opens with peer-to-peer as dated.

---

## 3. Choosing a front end

⚠ **This repository holds a datasheet for exactly one of these parts.** Everything in the
ST25R3916 row is **[DS]**-grade. Every other row is **[REC]** — recalled, unverified, and included
because a decision table with one row is useless. Library-maintenance columns *are* sourced: they
were checked live against the GitHub API on 2026-09-02 **[DOC]**.

| Part | Technologies | Modes | Host | Library reality **[DOC]** | Reach for it when |
|---|---|---|---|---|---|
| **ST ST25R3916** | A, B, F, V; tag types 1–5 **[DS]** | reader + **card emulation** + P2P + AAT + cap sense **[DS]** | **SPI or I²C, strapped by `I2C_EN`** **[DS]** | ST **RFAL** — `stm32duino/NFC-RFAL` 2.0.2 + `stm32duino/ST25R3916` 2.1.0, pushed **2026-08-31**, actively maintained | You want every technology, EMVCo-grade analog, or emulation. The best-documented option in this library |
| ST ST25R3917 | A, B, F, V **[DS]** | reader only — **no** emulation, AAT or cap sense **[DS]** | same **[DS]** | same RFAL | Cost-down reader-only. ⚠ shares `ic_type` with the 3916 — you cannot probe which you have **[DS]** |
| ST ST25R3911B | A, B, F, V **[REC]** | reader + emulation **[REC]** | SPI **[REC]** | `stm32duino/ST25R3911B`, pushed 2025-04-02 | The previous generation. Choose the 3916 for new work — same stack, newer silicon |
| ST ST25R200 / R100 / R500 / R300 | reduced sets **[REC]** | reader **[REC]** | SPI **[REC]** | `stm32duino/ST25R200` (2025-04), `ST25R500` (2025-12) | ST's newer low-cost line. **Same RFAL**, so the porting cost from a 3916 design is small |
| **NXP PN532** | A, B, F; **no** ISO 15693 **[REC]** | reader + emulation + P2P **[REC]** | I²C, SPI, **HSU/UART** **[REC]** | `adafruit/Adafruit-PN532` (2025-02), `elechouse/PN532` (2026-07); **`libnfc` supports it** | Hobby ubiquity, three host interfaces, huge example base. ⚠ **no NFC-V** — it will not read ICODE |
| NXP PN5180 | A, B, F, **V** **[REC]** | reader + emulation **[REC]** | SPI **[REC]** | ⚠ `ATrappmann/PN5180-Library` is **archived** (last push 2022-06) | Full technology coverage in the NXP ecosystem — but the popular Arduino library is abandoned |
| NXP MFRC522 ("RC522") | **A only** **[REC]** | reader **[REC]** | SPI, I²C, UART **[REC]** | ⚠ `miguelbalboa/rfid` README: *"The development by owner miguelbalboa has ended"*, maintenance badge **`no/2019`**; successor `OSSLibraries/Arduino_MFRC522v2` (LGPL-2.1, 2026-04) | The €2 blue board. Fine for MIFARE Classic/NTAG toys. **Not** for FeliCa, ISO 15693 or anything you must certify |

**How to read this table.** The dominant selection axis is not price — it is **which technologies you
must support**, and the second is **whether a maintained stack exists for your MCU**. An RC522 that
cannot see an ISO 15693 tag is not cheap, it is wrong. Conversely the ST25R3916 costs you a
harder bring-up (§5) and an antenna you must actually design (§4) in exchange for the full technology
set and ST's own analog configuration tables.

**Uncertainty.** Every [REC] cell should be checked against the part's datasheet before it decides
anything. The technology-coverage claims are the ones most likely to be subtly wrong — vendors
sometimes list a technology that is supported only at one bit rate, or only in one mode.

---

## 4. Antenna and matching — the part people get wrong

A correct driver on a badly matched antenna reads nothing, reports nothing, and looks exactly like a
software bug. This section is why.

### 4.1 An NFC reader is a tuned transformer, not a transmitter

At 13.56 MHz a wavelength is ~22 m and every practical antenna is a small loop operating in the
**magnetic near field**. The reader coil and the tag coil form a loosely coupled air transformer.
Nothing radiates usefully; the tag is *powered* by the field and replies by **load modulation** —
changing its own impedance so the reader sees its own field perturbed **[REC]**.

Three consequences follow, and they explain most NFC field behaviour:

1. **The field falls off very fast.** On the axis of a circular loop the classic result is
   `H = N·I·a² / (2·(a² + r²)^{3/2})` — asymptotically **1/r³** **[REC]**. Doubling the distance
   costs 18 dB, not 6.
2. **Range is capped by antenna size, not by power.** That same expression is maximised, for a given
   distance, by making `a` comparable to `r`. The practical rule of thumb is that usable read
   distance is on the order of the **antenna radius** **[REC]**. You cannot brute-force a small coil
   with more current.
3. **Both sides must be tuned to the same frequency**, and a detuned tag pulls the reader too.

### 4.2 The matching chain

Between the driver pins and the coil sits a chain that every 13.56 MHz reader design has in some
form **[REC]**:

```
driver output ─► EMC low-pass filter ─► matching network ─► damping ─► antenna coil
   (RFO1/RFO2)      (series L, shunt C)    (series/shunt C)    (series R)   (loop)

receiver input ◄── attenuation / DC-bias network ◄── tap off the antenna
   (RFI1/RFI2)
```

- **The EMC filter** is a low-pass placed *above* the carrier. It exists to keep the driver's square
  wave from radiating its harmonics — the driver is a switching push-pull stage, not a linear
  amplifier.
- **The matching network** transforms the coil's impedance to the driver's target load, which is what
  actually determines how much current flows in the coil.
- **The damping resistor** deliberately lowers Q (§4.3).
- **The receiver path** is separate and is *not* a power path — it taps the antenna and attenuates it
  down to something the receiver front end can handle. On the ST25R3916 that front end is specified
  at **V<sub>RFI</sub> typ. 0.5 mV<sub>rms</sub>** with 12–16 kΩ input resistance **[DS]** — and the
  datasheet marks it "specified by design, not tested in production"
  ([§5.4](../../components/stmicroelectronics/st25r3916/README.md#54-driver-architecture-the-network-implies)).

The ST25R3916's transmitter is **two identical push-pull drivers** (`RFO1`, `RFO2`) normally driving
the tank **differentially**, with `IO configuration register 1` bit 7 (`single`) switching to
single-ended and bit 6 (`rfo2`) then selecting which driver and which receiver input are used
**[DS]**. Differential doubles the voltage swing across the coil for the same supply, and it is the
default for a reason.

### 4.3 Q versus bandwidth — the actual trade

The tank's quality factor `Q = ω₀L / R_total`, and its −3 dB bandwidth is `B = f₀ / Q`. High Q means
a strong field and a narrow bandwidth; that is the whole tension.

The bandwidth you need is set by the **subcarrier**, not by the data rate. NFC-A and NFC-B put the
tag's reply on a subcarrier at **fc/16 = 847.5 kHz** **[STD]**, so the reply occupies sidebands at
roughly ±0.85 MHz around 13.56 MHz. To pass both sidebands without severe attenuation you need
`B ≳ 1.7 MHz`, i.e. `Q ≲ 8` **[INF]** — arithmetic on `B = f₀/Q` with `f₀ = 13.56 MHz`. Real reader
designs do not go that low; they run higher Q, accept sideband attenuation, and rely on the
receiver's gain. Published reader-antenna Q targets are typically in the tens **[REC]** — the exact
number is vendor application-note territory and **this repository holds no NFC antenna application
note**.

Higher bit rates make it worse: 424 and 848 kbit/s widen the modulation, and FeliCa at 212/424 kbit/s
uses **no subcarrier at all** **[STD]**, changing the spectral shape entirely. A design tuned by ear
for 106 kbit/s type A can fail at 424 kbit/s FeliCa.

**This is what damping resistors are for.** In the
[PaperMono's front end the record identifies `R3`, `R5` = 2 Ω in the antenna branches](../../components/stmicroelectronics/st25r3916/README.md#53-the-parts-that-are-there)
**[SCH]**. Two ohms in series with a coil of a few hundred nH at 13.56 MHz is a substantial, and
deliberate, Q reduction.

### 4.4 A worked component census — and one number that does not add up

The [ST25R3916 record §5.3](../../components/stmicroelectronics/st25r3916/README.md#53-the-parts-that-are-there)
carries a **complete component census of a real, shipping NFC front end**, recovered from the
PaperMono schematic: two 270 nH inductors, 680 pF, 160 pF, 150 pF, 220 pF and 10 pF capacitor groups,
2 Ω damping resistors, and an `NC` position in the AAT/`CSI` branch. **Read it there rather than
here** — it is the best worked example in this library, and it is device-specific by nature.

Two things about it belong in a general guide.

**First, the record is explicit that the topology was not recovered.** Its §5.2 says the extraction
"recovers text adjacency, not electrical connectivity", and the "Almost certainly" column heading is
doing real work. That honesty matters for anyone tempted to copy the values.

**Second, a sanity check on the inferred pairing does not come out right — and that is a useful
lesson about reviewing someone else's matching network.** If `L1`/`L2` (270 nH) and `C6`/`C8`
(680 pF) form the EMC filter in the conventional per-branch arrangement, the corner sits at

```
f = 1 / (2π·√(L·C)) = 1 / (2π·√(270 nH × 680 pF)) ≈ 11.7 MHz     [INF]
```

**below the 13.56 MHz carrier**, which is the wrong side for a filter whose job is to suppress
harmonics while passing the carrier. Pair the same inductor with the 220 pF group instead and it
lands at **≈ 20.6 MHz** **[INF]** — a thoroughly conventional place for an NFC EMC filter corner.

That is not a claim that the record is wrong. The differential topology, the coil's own inductance
and any series capacitance all move the answer, and none of them is known. It *is* a demonstration
of the review technique: **compute the corner frequency implied by every plausible L–C pairing, and
treat any result below the carrier as a signal that you have mis-read the topology.** Recorded as an
open observation for whoever next reads that schematic sheet graphically.

### 4.5 Layout dominates, and the numbers are small

The same record captures the vendor's own antenna specification, printed on the schematic
**[SCH]**: **4 turns, 25 × 25 mm, 0.25 mm line width, 0.3 mm spacing, 17 µm (0.5 oz) copper**. Two
general points from it:

- **That is a small reader antenna.** By §4.1's rule of thumb, an equivalent radius of ~14 mm bounds
  usable range at **centimetres, not tens of centimetres** **[INF]**. This does **not** produce a
  read-range figure, and the ST25R3916 record is right to refuse one — "no range figure follows from
  geometry alone". What geometry establishes is the *order of magnitude*, and therefore what a
  reasonable test expectation looks like.
- **The specification is on the schematic, in the copper, at a stated thickness.** Turn count, track
  width, spacing and copper weight all set the coil's inductance and its series resistance, so they
  set both the tuning and the Q. **An NFC antenna is a component with a tolerance, drawn in the
  stackup.** Change the stackup and you have detuned the radio.

Everything nearby matters too: ground pours, metal enclosures, batteries and displays behind the coil
all load it and shift its resonance **[REC]**. This is why a design that works on a bench coupon can
fail in the case.

### 4.6 Automatic antenna tuning, and why it may not be populated

The ST25R3916 offers **AAT** — `AAT_A` and `AAT_B` pins driving variable capacitors, with the tuning
procedure run at start-up **[DS]**. RFAL ships the driver for it: `st25r3916_aat.cpp` /
`st25r3916_aat.h` **[SRC]**. AAT compensates for exactly the detuning §4.5 describes.

It needs **external parts**, and a board can provision the branch without populating it. The
PaperMono appears to be such a board — the record's
[C3](../../components/stmicroelectronics/st25r3916/README.md#9-caveats-and-gaps) reads the `NC`
capacitor in that branch as AAT and the capacitive sensor being laid out but unfitted, `inferred` and
explicitly unconfirmed. **Generalise the check, not the conclusion:** if you are selecting a part
for AAT, confirm the variable-capacitor network is actually on the BOM, because the silicon feature
and the board feature are different things.

### 4.7 Reviewing an NFC antenna design — a checklist

1. **Is there an EMC filter, and is its corner above 13.56 MHz?** (§4.4.)
2. **Is the drive differential or single-ended, and does the register configuration agree with the
   populated branches?** On the ST25R3916 this is `IO configuration register 1` bits 7 and 6 **[DS]**
   — a mismatch between a differential board and a single-ended register setting is silent.
3. **Is there a damping resistor?** No damping usually means Q was never considered.
4. **Is the receiver path separate from the driver path**, with its own attenuation and DC bias?
5. **Does the coil's copper specification appear anywhere in the design files** — turns, width,
   spacing, thickness? If not, it is not specified, it is whatever the fab did.
6. **What is behind the coil?** Ground pour, battery, display, metal case.
7. **Are the driver current and dissipation limits respected?** For the ST25R3916: **350 mA** max
   driver current from the internal regulator, **500 mA** peak with the regulator bypassed, against a
   **300 mW** total dissipation ceiling **[DS]**
   ([§6](../../components/stmicroelectronics/st25r3916/README.md#6-electrical)). Those two numbers
   are in tension by design and it is why ST mandates the overheat-protection frame (§5.7).
8. **Does the stack's analog configuration match this antenna?** See §6.1 — RFAL ships a table of
   per-technology analog register settings and it is antenna-dependent.

---

## 5. Host interface, interrupts, FIFO, and the shape of a transaction

Everything in this section is **[DS]** from the ST25R3916 record. The *patterns* generalise across
NFC front ends; the specific values do not.

### 5.1 SPI or I²C, and how the chip is told which

The ST25R3916 selects its interface with a **strap pin**, `I2C_EN`: pulled to `GND` it is SPI, pulled
to `VDD_D` it is I²C **[DS]**
([§3.1](../../components/stmicroelectronics/st25r3916/README.md#31-the-interface-is-chosen-by-a-strap-and-this-board-straps-it-to-i²c)).
I²C is available at 100 kHz, **400 kHz**, 1 MHz Fast-mode Plus and 3.4 MHz high-speed **[DS]**.

Choosing between them is a system decision, not a driver one:

| | SPI | I²C |
|---|---|---|
| Pins | 4 dedicated | 2, **shared** |
| Throughput | higher; no address or ACK overhead | capped by the bus, and by everything else on it |
| Bus contention | none | ⚠ **the real risk** |
| FIFO streaming | clean | works, but every byte costs an ACK slot |

⚠ **The trap is naming.** In I²C mode the ST25R3916's data line is the pin *called* `MISO` and its
clock is the pin *called* `SCLK` — the datasheet names them `MISO (SDA)` and `SCLK (SCL)` **[DS]**.
A schematic symbol showing SPI pin names will read as an SPI design at a glance when it is not
([C5](../../components/stmicroelectronics/st25r3916/README.md#9-caveats-and-gaps)).

⚠ **The second trap is contention, and it is not hypothetical.** NFC polling is chatty. The
PaperMono's vendor scan app issues **180 ms detect calls at 60 ms intervals for seconds at a time**
**[SRC]**, and the device record names NFC-polling-versus-charger-gate as **the one documented
bus-stability hazard on that board**
([features/nfc.md §9](../../devices/m5stack/papermono/features/nfc.md)). **General rule: if the NFC
front end shares an I²C bus with anything latency-sensitive, schedule around the scan windows rather
than hoping.**

### 5.2 The operation byte, and why a driver seems to read a register that does not exist

The ST25R3916 puts an **operation byte** in front of every transaction — top two bits select the
operation, bottom six carry an address or command **[DS]** (full table at
[§3.3](../../components/stmicroelectronics/st25r3916/README.md#33-the-mode-byte-why-the-firmware-reads-register-0x7f)).
Register read is `0x40 | addr`; the IC identity register is at `0x3F`; therefore firmware that reads
identity sends `0x7F`, and **there is no register `0x7F`** **[DS]** + **[SRC]**, two independent
sources agreeing exactly.

This pattern — a command/address byte rather than a flat register file — recurs across radio front
ends. The SX126x does the same thing more aggressively ([LoRa guide §5](../lora/README.md)). **When a
driver constant does not appear in the register map, check whether it is an operation byte before
concluding the documentation is wrong.**

Two further behaviours generalise as habits:

- **Auto-increment.** All read and write modes auto-increment, so a burst is one operation byte, one
  address and then a stream **[DS]**.
- ⚠ **A non-existent register reads back as all zeros, not a NACK** **[DS]**. **A successful zero
  read proves nothing about the bus.** Probe with a register whose reset value is documented and
  non-zero.

### 5.3 Register banks

The ST25R3916 has two 64-register spaces, **A** (everything ordinary) and **B** (sparse: EMD
suppression, correlator, squelch, TX driver timing, overshoot/undershoot protection), with space B
reached by prefixing the transaction with direct command **`0xFB`** **[DS]**. RFAL and `M5Unit-NFC`
both encode this — the latter as `PREFIX_SPACE_B = 0xFB << 8` **[SRC]**.

**Generic hazard:** a banked register map means an address is ambiguous without its bank, and a
half-finished bank switch corrupts every subsequent access. If you hand-roll, make the bank part of
the address type, not a mode flag.

### 5.4 Interrupts

The ST25R3916's `IRQ` is **active high** and **push-pull — not open-drain, and therefore not
shareable** **[DS]**. Four interrupt status registers (main, timer-and-NFC, error-and-wake-up,
passive-target) each have a mask register, and **reading a status register clears it** **[DS]**.

Three general points:

- **Read-to-clear status registers must be read once and cached.** Reading twice loses events.
- **A push-pull IRQ cannot be wire-ORed** with another device's interrupt. This constrains the board,
  not the firmware.
- ⚠ **Polling instead of using the IRQ is common and usually undocumented.** The PaperMono's vendor
  firmware sets `cfg.using_irq = false` and polls, leaving the interrupt path **unexercised by any
  vendor code** **[SRC]**
  ([features/nfc.md §7](../../devices/m5stack/papermono/features/nfc.md)). If you switch a working
  polled design to interrupts, you are the first person to test that path.

### 5.5 FIFO

512 bytes on the ST25R3916, reached through its own operation-byte codes — `0x80` to load, `0x9F` to
read **[DS]**. FIFO status lives in two registers at `1Eh`–`1Fh` **[DS]**.

The generic discipline: **a framing engine with a FIFO wants to be fed and drained on watermark
interrupts, not on completion.** For short NFC frames this rarely bites; for a long ISO-DEP exchange
or a 255-byte Type 4 APDU it does.

### 5.6 The shape of a poll cycle

Assembled from the ST25R3916 direct-command table **[DS]** and the vendor demo's call sequence
**[SRC]**. **Not run on hardware.**

```
power/enable the front end                (board-specific — see the device record)
send the mandatory post-POR frame          FCh / 04h / 10h              §5.7
Set default                     C0/C1     → then re-send the frame above
configure IO config 1 and 2               00h, 01h
Adjust regulators               D6h        (ST: "to improve the system PSRR")
[if AAT is fitted] run the tuning procedure

per technology:
  select technology + bit rate            mode definition 03h, bit rate 04h
  NFC initial field ON            C8      performs RF collision avoidance, then field on
                                          → raises an interrupt on completion
  poll                            C6/C7   Transmit REQA / WUPA  (ISO 14443A only)
  anticollision + select                  (framing engine + protocol layer)
  transceive                      C4/C5   Transmit with / without CRC
  halt                            CD/CE   Go to sense (Idle) / sleep (Halt)
  field off                               before switching technology
```

⚠ **Commands marked "interrupt after termination" must be waited on.** The datasheet warns that on
I²C **no bus access may be made while such a command runs** — completion is signalled by interrupt
precisely so the host knows the bus is free again **[DS]**. A driver that polls a status register
during a running direct command is violating the interface.

The "field off before switching technology" step is real and is what the vendor app does —
`disableField()` between modes, with a settling delay **[SRC]**
([features/nfc.md §5](../../devices/m5stack/papermono/features/nfc.md)).

### 5.7 Power states, and one mandatory magic write

The ST25R3916's operation control register drives everything, and the mode ladder is steep **[DS]**
([§4](../../components/stmicroelectronics/st25r3916/README.md#4-operating-modes-power-states-and-wake-up)):
**0.8 µA** power-down · **3.0 µA** wake-up · **4.5 mA** ready · **16 mA** fully active.

Three things generalise:

- **Wake-up mode is the feature to know about.** A low-power RC oscillator takes periodic amplitude,
  phase or capacitance measurements and interrupts only on a departure from a stored reference
  **[DS]**. **This is how a reader detects a card without keeping the field on** — the difference
  between a battery device that lasts days and one that lasts hours. On the PaperMono **no vendor
  code touches it** and the board cuts the chip's supply instead **[SRC]**.
- ⚠ **Power-down current is temperature-dependent by an order of magnitude.** The PaperMono
  schematic annotates "2.5 µA"; that is the datasheet **maximum at ≤25 °C**. At 85 °C the maximum is
  **20 µA**, at 125 °C **60 µA** **[DS]**
  ([C4](../../components/stmicroelectronics/st25r3916/README.md#9-caveats-and-gaps)). **A sleep
  budget built from a room-temperature maximum is wrong in a warm enclosure.**
- ⚠ **There is a mandatory undocumented-looking write.** ST requires the 3-byte frame
  **`FCh / 04h / 10h`** after power-on *and* after every `Set default`, "to prevent the internal
  overheat protection to trigger below the junction temperature" **[DS]**. `FCh` is the *Test access*
  direct command, so this is a write into test register space and it looks like a magic number
  because it is one. Whether `M5Unit-NFC` issues it **was not traced** and is a live open question
  ([C6](../../components/stmicroelectronics/st25r3916/README.md#9-caveats-and-gaps)). **If you are
  evaluating any ST25R3916 driver, grep for `0xFC` first.**

Note also that the ST25R3916 **has no reset pin in any package** **[DS]**. Anything on a board named
"NFC reset" is a supply gate — on the PaperMono, demonstrably so
([§10.2](../../components/stmicroelectronics/st25r3916/README.md#102-pyb_nfc_en-and-pyb_rfid_rst-are-the-same-wire-and-it-is-a-rail-enable)).
Cycling it is a cold start, and the `FCh/04h/10h` frame must be re-sent afterwards.

---

## 6. Software stacks

| Stack | Scope | Silicon | Licence **[DOC]** | Maintenance, checked 2026-09-02 **[DOC]** | Good for |
|---|---|---|---|---|---|
| **ST RFAL** | Full: RF abstraction → technology layers → ISO-DEP/NFC-DEP → tag types → NDEF | ST25R only | `NOASSERTION` on the stm32duino packaging | ✅ `stm32duino/ST25R3916` pushed **2026-08-31**; `NFC-RFAL` 2.0.2, "based on version 3.0.0 of the RFAL Middlewares from STM32Cube" | Anything serious on ST silicon. The reference implementation |
| **`M5Unit-NFC`** | Full, and reaches higher: Crypto1, AES, DESFire helpers, ISO-DEP, NDEF, APDU | ST25R3916 (SPI **and** I²C) | — | Pinned by PaperMono firmware at **0.1.0** and **vendor-patched** **[SRC]** | M5Stack hardware. It is what ships |
| **`libnfc`** | Host-side reader abstraction | ⚠ **PN53x family and readers, not ST25R** **[REC]** | LGPL-3.0 | Alive but slow: last push **2025-03-05** | Linux/PC with a PN532 or ACR122. **Irrelevant to an ST25R3916** |
| `adafruit/Adafruit-PN532` | Reader, NDEF basics | PN532 | `NOASSERTION` | last push 2025-02-18 | Arduino PN532 |
| `elechouse/PN532` | Reader, some P2P | PN532 | ⚠ none declared | last push 2026-07-28 | Arduino PN532 |
| `miguelbalboa/rfid` | Reader, MIFARE Classic | MFRC522 | Unlicense | ⚠ **frozen**: *"development by owner miguelbalboa has ended"*, maintenance badge `no/2019` | Legacy projects only |
| `OSSLibraries/Arduino_MFRC522v2` | Successor to the above | MFRC522 | LGPL-2.1 | last push 2026-04-01 | New MFRC522 work |
| `ATrappmann/PN5180-Library` | Reader | PN5180 | LGPL-2.1 | ⚠ **archived**, last push 2022-06 | Nothing new |
| `pguyot/st25r391x` | Linux kernel driver | ST25R3916/7 | GPL-2.0 | last push 2024-05 | Linux hosts |
| `vouch-opensource/zephyr-st25r` | Zephyr driver | ST25R | Apache-2.0 | last push 2023-05 | Zephyr, with caution |

**What the maintenance column actually tells you.** Two of the most-linked Arduino NFC libraries are
frozen or archived, and neither says so on its front page in a way a search result surfaces. That is
the practical reason to prefer the ST + RFAL path for new work on this class of part: it is the one
line in the table with a 2026 commit *and* a vendor behind it.

### 6.1 RFAL's structure, and the one thing to know before porting it

Read live from `stm32duino/NFC-RFAL` @ `main` and `stm32duino/ST25R3916` @ `main`, 2026-09-02
**[SRC]**. The split across two packages *is* the portability story:

```
NFC-RFAL  (silicon-independent)          ST25R3916  (silicon-specific)
  rfal_rf.h            the RF interface    rfal_rfst25r3916.cpp      implements rfal_rf.h
  rfal_nfc.cpp         discovery loop      rfal_rfst25r3916_analogConfig.cpp
  rfal_nfca/b/f/v.cpp  technologies        rfal_rfst25r3916_analogConfigTbl.h
  rfal_isoDep.cpp      ISO 14443-4         rfal_rfst25r3916_iso15693_2.cpp
  rfal_nfcDep.cpp      NFC-DEP / P2P       st25r3916_com.cpp         bus layer
  rfal_t1t/t2t/t4t.cpp tag operations      st25r3916_interrupt.cpp
  rfal_st25tb/st25xv   ST tag families     st25r3916_aat.cpp         AAT (§4.6)
  ndef_*.cpp           NDEF (§1.4)         st25r3916_timer.cpp
  st_errno.h                               st25r3916_{,default_}config.h
```

**Porting means implementing the bus and timer layer**, not the protocols: `st25r3916_com.cpp`,
`st25r3916_timer.cpp` and the interrupt plumbing are the files that touch a platform. Everything
above `rfal_rf.h` is portable by construction. **[INF]** from the file layout; ST does not state it
in this packaging.

⚠ **`rfal_rfst25r3916_analogConfigTbl.h` is the file people do not expect.** RFAL ships a table of
**analog register settings per technology, per bit rate, per direction** — receiver gain, modulation
depth, thresholds. Those values are matched to a reference antenna. **A design with a different
antenna may need a different table**, which is precisely the coupling §4 warns about: the "software"
and the "antenna" are not separable on this class of part. **[INF]** from the file's existence and
naming; the tuning procedure itself is ST application-note material this repository does not hold.

### 6.2 `M5Unit-NFC` is not an RFAL wrapper

Worth stating because the assumption is natural and wrong. The
[ST25R3916 record §7.1](../../components/stmicroelectronics/st25r3916/README.md#71-m5unit-nfc-is-a-from-scratch-driver-not-an-rfal-wrapper)
enumerated the pinned tree — 301 entries — and found **no RFAL directory, no ST source file and no ST
licence header** **[SRC]**. It is M5Stack's own implementation, it goes further up the stack than
RFAL's Arduino packaging does (Crypto1, DESFire helpers), and it has correspondingly less provenance
behind it.

⚠ **Every M5Stack dependency in that firmware is pinned *and patched*.** A library-manager install
gives you neither the pinned commit nor the vendor's patch **[SRC]**.

---

## 7. Regulatory and safety context

⚠ **Not legal advice. This repository holds none of the standards cited here.** [STD] and [REC]
throughout; check with someone qualified before shipping.

- **13.56 MHz inductive readers are regulated by field strength, not by transmit power.** The
  European standard is **ETSI EN 300 330** (9 kHz – 25 MHz, inductive loop systems) and the US rule
  is **47 CFR §15.225**, which carves out 13.553–13.567 MHz with a field-strength limit measured at a
  specified distance **[STD]**. The limit is on **H-field at a distance**, which is why a bigger coil
  is a legitimate way to get more range and more drive current often is not.
- **Read range is fundamentally capped, and not by your firmware.** §4.1's 1/r³ roll-off plus a
  field-strength ceiling is the reason NFC is a *proximity* technology by design. Vicinity
  (ISO 15693) reaches further because it tolerates a much weaker field, not because it is allowed
  more of one **[REC]**.
- **Thermal and electrical limits are real.** The ST25R3916 can push **350 mA** into an antenna
  against a **300 mW** dissipation ceiling **[DS]**, and ST's mandatory overheat-protection frame
  (§5.7) exists because of exactly that gap.
- **Collision handling is part of the protocol, not an optimisation.** Each technology defines its
  own anticollision, and the field-on commands `C8`/`C9` perform **RF collision avoidance** before
  switching the field on — i.e. the chip checks for an existing external field first **[DS]**. That
  matters when two readers are near each other; also see the external field detector bits in the
  operation control register **[DS]**.
- **Certification does not come for free with a chip.** The
  [PaperMono has no published certification of any kind, including for its 13.56 MHz emitter](../../components/stmicroelectronics/st25r3916/README.md#9-caveats-and-gaps)
  — a **verified negative** **[DOC]**. A front-end IC with EMVCo-compliant analog says nothing about
  *your* board with *your* antenna.

---

## 8. Debugging and diagnostics

### 8.1 Telling the four common failures apart

| Symptom | Likely class | How to discriminate |
|---|---|---|
| Chip not on the bus at all | **Power or enable** | Is the front end's rail actually up? On many designs the chip is behind a load switch controlled by an expander — no I²C, no NFC. Also: is this the SKU that has NFC? |
| Bus responds, identity read returns `0x00` | **Bus or address, not silicon** | ⚠ Zeros are the documented response to a non-existent register **[DS]**; they are also what a floating bus looks like. Read a register with a documented non-zero reset value |
| Identity correct, **no tag ever detected in any technology** | **Field, matching, or antenna** | Field never enabled; matching wrong; coil detuned by its surroundings. Check the field-on command actually completed (it interrupts on completion **[DS]**) before blaming the tag |
| Detects in one technology, never in another | **Protocol / configuration**, not RF | Wrong layer for the card; bit rate mismatch; analog configuration wrong for that technology (§6.1). Try NFC-A first — it is the best-tested path everywhere |
| Detects at 0 mm, nothing at 10 mm | **Matching or Q** | Classic under-coupled/detuned signature. Field exists but is weak, or the reply sidebands are being filtered out (§4.3) |
| Works on the bench coupon, fails in the enclosure | **Antenna environment** | Metal, battery or display behind the coil (§4.5) |
| Intermittent, correlated with other bus traffic | **Contention** | §5.1. Correlate against the other device's transaction windows |
| Initialises, then misbehaves after a while, warm | **Thermal / the missing `FCh/04h/10h` frame** | §5.7 |
| Interrupt never fires but polling works | **Untested IRQ path** | On at least one documented board no vendor code ever enables it **[SRC]** |

### 8.2 What actually distinguishes "no tag" from "wrong protocol" from "bad matching"

The single most useful discriminator on an ST25R3916 is that the chip can **measure its own front
end** without a tag present. Direct commands **`D3` Measure amplitude**, **`D9` Measure phase** and
**`DF` Measure power supply** put results into readable registers **[DS]**, and there is an RSSI
register at `2Dh` **[DS]**.

Consequently:

- **Amplitude/phase stable and plausible with no tag, changing when a tag approaches** → the antenna
  works and the field exists. A detection failure after that is a **protocol** problem.
- **Amplitude implausible or unchanging with a tag on the coil** → **matching or antenna**. No amount
  of protocol work will help.
- **Amplitude fine, tag changes it, but no technology completes anticollision** → **configuration**:
  bit rate, analog table, or the wrong technology for the card.

`not-tested` — this is the documented capability of the measurement commands applied as a procedure,
**[INF]**. It is, however, the reason to prefer a front end that exposes these measurements at all.

### 8.3 Test-tag discipline

**Keep one known tag of each technology and label them.** NFC-A (an NTAG21x), NFC-B (harder to source
— many bank cards are Type B), NFC-F (a Japanese transit card or FeliCa Lite), NFC-V (an ICODE SLIX
label). Debugging a reader with an unknown card confounds every diagnosis in §8.1. **[REC]**

And a caution that this library earned honestly: on the one documented device fitting this chip,
**nobody has reported reading any tag at all** — no vendor test report, no compatibility list, no
community account, after two independent broad passes
([features/nfc.md §8](../../devices/m5stack/papermono/features/nfc.md), a **verified negative**).
**Do not assume a technology works because a chip advertises it and a library exposes a class for
it.** The existence of a code path is not a read.

---

## 9. Validation checklist

Nothing below was executed. This is the sequence the evidence implies, in dependency order.

1. **Confirm the part is fitted at all.** On dual-SKU products this is a real question, and on at
   least one it is how the firmware itself distinguishes variants **[SRC]**.
2. **Bring the rail up before touching the bus**, in the board's documented order.
3. **Probe identity with a documented non-zero value** (§5.2, §8.1).
4. **Send the vendor-mandated post-POR frame** if the part has one (§5.7).
5. **Enable the field and confirm completion by interrupt or status**, not by delay.
6. **Measure amplitude/phase with no tag, then with a tag** (§8.2). Record both. This is your
   baseline for every future regression.
7. **Detect NFC-A first**, with a known NTAG.
8. **Then each other technology in turn**, with a known tag each, field disabled between changes.
9. **Then read NDEF**, then anything proprietary.
10. **Then measure read range** at each technology, and **record the antenna environment** — coupon
    or enclosure — because the number is meaningless without it.
11. **Then re-run everything at temperature**, if the product has a sleep budget (§5.7).

---

## 10. Device-specific pages

| Device | Front end | Applicability |
|---|---|---|
| [**M5Stack PaperMono**](../../devices/m5stack/papermono/features/nfc.md) | ST25R3916, I²C, on a sub-board | **Applies with deltas** — I²C strap rather than SPI, no chip reset (the "reset" is a rail gate), interrupt unused by vendor code, `M5Unit-NFC` rather than RFAL |
| [M5Stack PaperMono-Lite](../../devices/m5stack/papermono-lite/README.md) | **none fitted** | Not applicable — no NFC hardware |

---

## 11. Evidence boundary — and what could not be sourced

**This guide contains no new hardware research and no measurements.** Its inherited claims come from
the [ST25R3916 record](../../components/stmicroelectronics/st25r3916/README.md) and the
[PaperMono NFC feature guide](../../devices/m5stack/papermono/features/nfc.md) as they stood on
**2026-09-02**, and carry their labels transitively.

**New to this page, live-verified on 2026-09-02 [SRC]/[DOC]:** the RFAL and NFC-RFAL file layouts and
versions (2.1.0 / 2.0.2), the absence of MIFARE/Crypto1 from RFAL's Arduino packaging, the absence of
a Type 1 NDEF mapping, and every library maintenance status in §3 and §6 — including the
`miguelbalboa/rfid` freeze notice quoted verbatim and the `ATrappmann/PN5180-Library` archived flag.

**New and derived here [INF]:** the §4.4 EMC-corner arithmetic and the observation that the record's
inferred L–C pairing lands below the carrier; the §4.3 `Q ≲ 8` bound; the §4.5 order-of-magnitude
range bound from antenna geometry; the §6.1 porting-boundary reading; the §8.2 diagnostic procedure.

### Claims I could not source

| Claim | Why it is unsourced | Risk if wrong |
|---|---|---|
| **Every ISO/IEC and JIS modulation, coding and subcarrier detail in §1.1** | This repository holds **no** ISO/IEC 14443, 15693 or 18092 document, and none is freely obtainable | Low for the structure, moderate for specific numbers. `fc/16` and `fc/32` are the ones a design would actually depend on |
| **The tag-product mapping in §1.2** | No NXP, Sony, Broadcom or TI tag datasheet is held | Low. Verify memory sizes before designing to them |
| **MIFARE Classic's Crypto1 layering (§1.3)** | Proprietary; no document | Low — the practical consequence (a stack either has Crypto1 or does not) is confirmed by the two trees actually enumerated |
| **Reader-antenna Q targets (§4.3)** | This repository holds **no NFC antenna application note** from ST or NXP. The `B = f₀/Q` arithmetic is sound; the *target* is not stated | **Moderate.** This is a real gap for anyone doing a design review |
| **The 1/r³ near-field roll-off and the "range ≈ coil radius" rule (§4.1, §4.5)** | Standard magnetostatics, but no document behind it here | Low as an order-of-magnitude bound; **do not quote it as a specification** |
| **ETSI EN 300 330 and 47 CFR §15.225 (§7)** | Neither document is held; cited by number only | **High if relied upon.** Get the actual limits from the actual regulation |
| **Everything about PN532, PN5180, MFRC522 and ST25R3911B capability in §3** | No datasheet for any of them | **Moderate** — the table decides part selection. Library-maintenance cells in the same table *are* sourced |
| **Android's removal of Beam/P2P (§2)** | Recalled; no citation retrieved | Low; the conclusion (prefer card emulation) is robust either way |
| **Whether RFAL's analog configuration table must be retuned per antenna (§6.1)** | Inferred from the file's existence and name. ST's tuning procedure was not located | **Moderate.** It is the right question to ask a vendor, not yet an established fact |

### Where this guide sits relative to the deep records

**No contradiction was found** with the ST25R3916 record or the PaperMono feature guide. One point of
**tension**, recorded rather than resolved: §4.4's corner-frequency arithmetic sits uneasily with the
"Almost certainly" component attribution in
[ST25R3916 §5.3](../../components/stmicroelectronics/st25r3916/README.md#53-the-parts-that-are-there).
That column is already labelled as inference and its §5.2 already states the topology was not
traced, so this is a **new open observation, not a conflict** — and the deep record's own caution is
what makes it visible.

---

## Related

- [**ST STMicroelectronics ST25R3916**](../../components/stmicroelectronics/st25r3916/README.md) — the deep record: register spaces, operation byte, power states, the real front end, the mandatory `FCh/04h/10h` frame
- [M5Stack PaperMono — NFC feature guide](../../devices/m5stack/papermono/features/nfc.md) — the device-specific companion to this page
- [M5Stack PaperMono — device record](../../devices/m5stack/papermono/README.md) · [gaps and conflicts](../../devices/m5stack/papermono/gaps-and-conflicts.md)
- [**LoRa — a device-independent guide**](../lora/README.md) — the other radio on the same board, and the same `BUSY`/command-byte/errata patterns in a different key
- [Guides index](../README.md) · [Components index](../../components/README.md) · [Devices index](../../devices/README.md)
- [Vendor sourcing guides](../../vendors/README.md) — ⚠ **no STMicroelectronics guide exists yet**; the retrieval findings in [ST25R3916 §8](../../components/stmicroelectronics/st25r3916/README.md#8-sourcing-and-documentation) are what one would open with
