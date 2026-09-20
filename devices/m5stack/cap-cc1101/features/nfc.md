# NFC — Cap CC1101 (U219), ST25R3916 over SPI

> **Common guide:** [`guides/nfc`](../../../../guides/nfc/README.md).
>
> **Applicability:** the standard approach **applies with one large delta** — this board
> straps the ST25R3916 to **SPI**, where the other ST25R3916 board in this repository
> (M5Stack PaperMono) straps it to **I²C**. Everything above the transport is identical;
> everything about bus arbitration, speed and mode is not.

> **How do I read an NFC tag?** §5. **How do I put this on my own hardware?** §10.
> Snapshot 2026-09-04 · schematic **V0.3 / 2026-05-28** · nothing tested on hardware.

---

## 1. Hardware path

```
        13.56 MHz loop antenna (ANT1, ANT1_P / ANT1_N)
              ▲                              ▲
     ┌────────┴────────┐            ┌────────┴────────┐
     │ L2 270nH ±5%    │            │ L3 270nH ±5%    │   EMC + matching
     │ R2 1.5 Ω        │            │ R3 1.5 Ω        │
     │ C7 220p C8 10p  │            │ C15 180p C17 10p│
     │ C10 220p        │            │ C18 220p        │
     │ C11 680p C12150p│            │ C13 680p C14150p│
     └────────┬────────┘            └────────┬────────┘
       RFO1(13)                        RFO2(15)
       RFI1(22)/RFI_P                  RFI2(23)/RFI_N
       AAT_A(18)                       AAT_B(19)      ← automatic antenna tuning
                     U2  ST25R3916-AQWT
   XTI(5)/XTO(4) ── Y1 27.12 MHz (C19/C20 6.0 pF)     ← 13.56 = 27.12 / 2
   I2C_EN(20) ── strapped for SPI
   SS(29)  ◀── NFC_CS   ◀── Cap-Bus 10 ◀── host G6
   IRQ(27) ──▶ NFC_IRQ  ──▶ Cap-Bus  9 ──▶ host G4
   SCLK(30)/MOSI(31)/MISO(32) ◀──▶ shared SPI ◀──▶ G40 / G14 / G39
   VDD_IO(1) VDD_D(3) VDD_A(7) VDD(8) VDD_RF(9) VDD_TX(10) VDD_AM(11) VDD_DR(14)
        each with a 10 nF + 10 µF pair (C21…C36)
```

## 2. The interface strap is the whole story

The ST25R3916 chooses its host interface from a **pin strap**, not a command: `I2C_EN`
(pin 20). This board ties it for **SPI**; the PaperMono ties it for **I²C**. Consequences:

| | Cap CC1101 (SPI) | PaperMono (I²C) |
|---|---|---|
| Transport | 4-wire SPI, **mode 1** (CPOL=0, CPHA=1), **10 MHz** in M5Stack's example | I²C, address per `ST25R3916` record |
| Chip select | `SS` pin 29 ← host **G6** | none |
| Bus sharing | **with the CC1101** on the same board (different CS) and with the host's microSD | with keyboard, IMU, codec, expander |
| Latency | high-rate; adequate for ISO-DEP framing | ⚠ the M5Unit-NFC README warns that a **SoftwareI2C** Grove path has *"I2C register polling latency too high for ST25R3916 RF timing requirements"* |
| Library selection macro | `#define USING_CAP_CC1101` | `#define USING_UNIT_NFC` |

> **The latency note is the important transferable lesson.** ST25R3916 RF timing is
> enforced by register polling; if your transport is slow, protocols fail in ways that look
> like antenna problems. M5Stack say so explicitly for one bus type in their own library
> README. If you are porting to a host where I²C is bit-banged or heavily shared, **use
> SPI**.

Register-space, mode-byte and direct-command detail is **not repeated here** — it lives in
[`components/stmicroelectronics/st25r3916`](../../../../components/stmicroelectronics/st25r3916/README.md),
which already documents the mode byte, the space-B prefix, auto-increment behaviour and the
mandatory power-on write sequence.

## 3. Antenna and matching

The board carries a **fully differential** matching network — two symmetric arms of
270 nH ±5 % series inductance with 1.5 Ω damping, plus a 4-element EMC/matching capacitor
group per arm — feeding `ANT1_P`/`ANT1_N`. `AAT_A` (18) and `AAT_B` (19) are connected,
which means the chip's **Automatic Antenna Tuning** is available: the ST25R3916 can trim a
pair of on-chip varactor banks to compensate for detuning by a nearby metal object or a
card. Anything that wants reliable reads through a case should use it.

`EXT_LM` (17) is connected via `C19`-adjacent components — external load modulation is
therefore wired for card-emulation use.

Component values are transcribed from the schematic text layer, `executed-success` on the
read. They were **not** verified against a rendered sheet, so treat the *pairing* of value
to designator as `inferred` where two designators sit on the same row.

## 4. Software

| Stack | Class | Where |
|---|---|---|
| **M5Unit-NFC / `M5UnitUnifiedNFC`** — the vendor's own | **`m5::unit::CapCC1101NFC`**, an alias: `using CapCC1101NFC = m5::unit::CapST25R3916;` | `github.com/m5stack/M5Unit-NFC`, head `93745b547364f310cd64b5155a870103a7800a5d` (2026-06-10), release **0.1.0** (2026-06-10), **MIT** |
| ST's RFAL | — | **Not used.** The existing `ST25R3916` record establishes that M5Unit-NFC is *"a from-scratch driver, not an RFAL wrapper"* |
| Anything else | — | No community ST25R3916 driver for this Cap was located |

> **The library shipped before the product.** `CapCC1101NFC` and `USING_CAP_CC1101` are
> present at the 2026-06-10 head — **11 weeks before** the Cap went on sale (2026-08-28) —
> and the README says so in as many words: *"CapCC1101 / SKU:U219 (SPI connection via
> ST25R3916) is included in this library for future use."* That is useful provenance: the
> driver was written against the real hardware well ahead of release, so it is not
> speculative support.

Selection is by preprocessor macro in the examples:

```cpp
// #define USING_UNIT_NFC
#define USING_CAP_CC1101       // SKU U219
```

Example families in the repo (`examples/UnitUnified/`): **NFCA** — Detect, Dump, NDEF,
ReadWrite, ValueBlock, PolicyOverride, **Emulation**; **NFCB** — Detect, JapanIDCard;
**NFCF** — Detect, Dump, NDEF, Emulation, Subtract, ReadWriteMAC,
JapanTransportationICCard; **NFCV** — Detect, Dump, NDEF. Both Arduino (`.ino`) and
ESP-IDF (`main/*.cpp`) forms are provided. `Kconfig.variant.basic` notes that NFC-A
Emulation and *all* NFC-F and NFC-V examples are **only supported on ST25R3916-based
units** — i.e. this Cap and the Unit NFC, not the RFID2/WS1850S alternatives.

Support caveats from the library README, worth knowing before you promise a customer
anything: *"MIFARE DESFire Light — NDEF is not supported yet"*; and for the I²C variant
*"MIFARE Plus SL3 operation has issues, SL2 can not R/W"* (an I²C-variant limitation, so
**this SPI board should be the better one** for MIFARE Plus — `inferred`, untested).

## 5. Minimal read

From M5Stack's Arduino guide. `executed-success` on the read; `not-tested`. **[DOC]**

```cpp
#include <M5Cardputer.h>
#include <M5Unified.h>
#include <M5UnitUnified.h>
#include <M5UnitUnifiedNFC.h>
#include <wiring/m5_unit_unified_wiring.hpp>
using namespace m5::nfc::a;
using namespace m5::nfc::a::mifare::classic;

m5::unit::UnitUnified Units;
m5::unit::CapCC1101NFC unit{};          // Cap CC1101 NFC (ST25R3916, SPI)
m5::nfc::NFCLayerA    nfc_a{unit};
constexpr Key keyA = DEFAULT_KEY;        // 0xFFFFFFFFFFFF

void setup() {
    auto cfg = M5.config();
    M5Cardputer.begin(cfg, true);
    // SPI mode 1, 10 MHz. The library maps the Cardputer-Adv pins itself:
    //   SCK=G40, MOSI=G14, MISO=G39, NFC CS=G6, NFC IRQ=G4
    bool ready = m5::unit::wiring::addSPI(Units, unit, 10000000, 1) && Units.begin();
}
```

The guide's `Dump` example triggers on the Cardputer's **Tab** key, detects/identifies/
activates an NFC-A tag, authenticates MIFARE Classic with the default key, and dumps via
`picc.uidAsString()` / `picc.typeAsString()`.

Two things the guide states that are easy to miss:

1. **You do not specify the SPI pins.** `addSPI()` maps them from the host identity. That
   is convenient on a Cardputer-Adv and a trap on anything else — see §10.
2. **SPI mode 1**, not mode 0. The CC1101 on the same bus uses a different mode; see
   [`sub-ghz.md` §4](sub-ghz.md).

## 6. Resources consumed

| Resource | Value | Contention |
|---|---|---|
| Host GPIO | **2 dedicated** (G6 `NFC_CS`, G4 `NFC_IRQ`) + 3 shared SPI (G40/G14/G39) | SPI shared with **CC1101** (CS = G5) and the host **microSD** (CS = G12) |
| SPI mode/clock | mode **1**, 10 MHz | ⚠ differs from the CC1101's mode on the same wires |
| Power | via `VDD_3V3` from `U1`, gated by `POWER_EN` ← host **G3** | the whole Cap powers down together |
| Interrupt | G4 | ST25R3916 `IRQ` is level-ish and must be serviced or the chip stalls |

## 7. Card emulation

Supported for **NFC-A and NFC-F only** (vendor spec and library README agree). NFC-B and
NFC-V are reader/writer only. `EXT_LM` is wired, so external load modulation is available
for the emulation path.

This is the capability that makes the board interesting beyond tag reading: an NFC-A/NFC-F
card emulator with a keyboard and a screen attached is, functionally, a programmable
transit/access card sandbox. **No community project doing this on the Cap was found** — the
board is seven days old.

## 8. Simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| NFC + CC1101 sub-GHz | ⚠ **shared SPI, different modes** | Both on G40/G14/G39. You must switch SPI mode between transactions, or run two `SPIClass` configurations against one bus and re-`beginTransaction` each time |
| NFC + microSD | ⚠ shared SPI | Host `SDCARD_CS` = G12 |
| NFC + Wi-Fi/BLE | ✅ | 13.56 MHz vs 2.4 GHz |
| NFC + sub-GHz RF-wise | ✅ | 13.56 MHz vs 315–915 MHz, separate antennas |
| NFC + Grove I²C sensor | ✅ | different bus entirely |
| NFC while the Cap is powered down | ❌ | `POWER_EN` (G3) low kills the rail |

## 9. Debugging

| Symptom | Cause |
|---|---|
| Nothing on the bus at all | Cap not powered — drive host **G3 high** first ([`power-and-grove.md`](power-and-grove.md)) |
| Chip responds, no tags detected | Antenna detuning; try Automatic Antenna Tuning (`AAT_A`/`AAT_B` are wired) |
| Works standalone, fails when the sub-GHz radio is active | **SPI mode collision** — §8 |
| Protocol-level timeouts, ISO-DEP failures | Transport latency. Do not put this chip behind a slow/bit-banged bus — §2 |
| MIFARE Plus SL3 misbehaves | Known library limitation, documented for the I²C variant; status on SPI untested |
| DESFire Light NDEF unsupported | Known library gap, stated in the README |

## 10. Porting checklist — adding ST25R3916 NFC to other firmware

Written for the wider project's goal of adding NFC to e-ink reader firmware. The
PaperMono's I²C treatment is the sibling case:
[`devices/m5stack/papermono/features/nfc.md`](../../papermono/features/nfc.md).

**Hardware you must provide:**

| Resource | Count | Notes |
|---|---|---|
| SPI SCK/MOSI/MISO | 3 | shareable; **budget for mode switching** if other devices differ |
| Chip select | 1 | dedicated |
| `IRQ` | 1 | **strongly recommended.** Polling works but ISO-DEP timing suffers |
| 27.12 MHz crystal | 1 | **not optional** — the 13.56 MHz carrier is derived from it. C ≈ 6.0 pF load caps |
| 8 supply pins, each decoupled | — | this board uses a **10 nF + 10 µF pair per pin**. Under-decoupling an ST25R3916 shows up as read-range loss, not as a digital fault |
| Differential antenna + matching | 1 | the hard part. Two 270 nH ±5 % arms, 1.5 Ω damping, ~4 caps per arm on this board |
| `AAT_A`/`AAT_B` | 2 | wire them; automatic tuning is worth the two pins |
| `EXT_LM` | 1 | only if you want card emulation |
| `I2C_EN` strap | 1 | **decide early.** SPI for latency, I²C for pin count |

**Software:**

1. `m5stack/M5Unit-NFC` (**MIT**) is a complete, from-scratch ST25R3916 driver with
   Arduino *and* ESP-IDF builds, NFC-A/B/F/V, and card emulation. It is the shortest path
   and its licence permits reuse.
2. It is written against **M5UnitUnified**, so a port means either bringing that
   abstraction along or reimplementing `addSPI()`/`Units.begin()` against your own bus API.
   The `wiring::addSPI(Units, unit, 10'000'000, 1)` signature is the whole surface.
3. **`addSPI()` infers pins from the host board identity.** On non-M5Stack hardware that
   inference does not exist and you must supply pins explicitly — expect this to be the
   first thing you have to patch.
4. ST's **RFAL** is the alternative if you need ST's certification-grade protocol stack;
   it is much larger and this board does not use it.
5. Budget flash: the NFC-A/B/F/V protocol layers plus MIFARE are not small.

**What is board-specific and must not be copied:** the pin numbers, the `POWER_EN` gate,
the SPI mode collision with a co-resident CC1101, and the antenna matching values (they are
tuned to *this* PCB's loop).

## 11. Unresolved

- `I2C_EN` strap value read as "strapped for SPI" from the net name plus the vendor's
  interface claim; the **strap resistor was not identified** on the sheet. `inferred`.
- `ANT1` is a designator with no published geometry — PCB loop turns, area and inductance
  are unknown, so the matching network cannot be re-derived for another board.
- Whether the AAT is actually exercised by `M5Unit-NFC` on this Cap: not checked.
- No read-range, tag-compatibility or emulation test by anyone. The board is seven days old.

## Applicability

| Field | Value |
|---|---|
| Hardware | Cap **U219**, schematic **V0.3 / 2026-05-28** |
| Software | `m5stack/M5Unit-NFC` @ `93745b54…` (rel. 0.1.0, MIT) · M5Unified · M5UnitUnified |
| Evidence | Chip identity and pin map: **schematic + vendor pin-map + vendor Arduino guide**, three-way. Matching values: **schematic text layer**, `executed-success` on the read, pairing `inferred`. Behaviour: **none tested** |
| Confidence | High on architecture; **zero on RF performance and tag compatibility** |
| Last verified | 2026-09-04 |
