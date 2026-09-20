# RF balun `B0310J50100AHF`

- **Category:** **balun / impedance transformer** — differential (balanced) to
  single-ended (unbalanced), sub-1 GHz
- **Research status:** ⚠ **manufacturer and datasheet not identified.** The part number is
  read from a schematic comment. Everything in §2 is an **inference from the part-number
  pattern** and should be treated as a hypothesis, not a fact.
- **Retrieved:** 2026-09-04

## 1. What is actually established

| Property | Value | Evidence |
|---|---|---|
| Schematic comment | **`B0310J50100AHF`** | Cap CC1101 schematic V0.3, `B1`, sheet 3 |
| Pin names as drawn | `Unbalanced` (1), `GND` (2), **`Balanced`** (3), **`Balanced`** (4), `DNC` (5), `NC` (6) | schematic |
| Function on the board | Converts the **CC1101's differential `RF_P`/`RF_N` port** to the single-ended path feeding the band-select switches and the SMA connector | schematic topology |
| Associated network | `C42` 100 pF (RF_N series), `C46` 100 pF (RF_P series), `C43` 0.6 pF (differential), `L4` 3.3 nH, `L5` 6.8 nH ±5 %, `R5` 0 Ω, `C44` **DNP**, `C45`, `C47` 100 pF | schematic |

## 2. ⚠ Inference about the part number — **not verified**

The pattern `B<four digits><letter>J50100AHF` matches the naming convention used by
**Anaren / TTM Technologies** for their balun product line, in which:

- the four digits encode the **frequency range**, and
- `50100` encodes the **impedance transformation, 50 Ω unbalanced ↔ 100 Ω balanced**.

Under that reading, `0310` would mean **0.3 – 1.0 GHz** — which would exactly suit a board
that must cover **315, 433, 868 and 915 MHz** through one balun and then switch the *matching*
per band. The design's shape corroborates the reading: you would not fit three narrowband
matching paths behind a *narrowband* balun.

**This is `inferred` and unconfirmed.** No datasheet was located; the manufacturer was not
identified; the six-pin footprint was not cross-checked against any published package. If a
future pass finds the real part, this section should be replaced rather than edited.

## 3. Why a balun is needed at all

A CC1101 (like most sub-GHz transceivers) presents a **differential** RF port with an
impedance that is neither 50 Ω nor single-ended. An antenna connector is 50 Ω
single-ended. Something has to do three jobs at once:

1. **Balanced → unbalanced** conversion, so common-mode currents do not radiate from the
   feed;
2. **impedance transformation**, here 100 Ω differential → 50 Ω single-ended;
3. **harmonic filtering**, to the extent the network provides it.

A discrete LC balun can do this cheaply for one band. A packaged wideband balun does it
across a decade, at the cost of a component and some insertion loss — which is the trade
this board makes in order to be multi-band.

## 4. Used By

### [M5Stack Cap CC1101 & NFC (U219)](../../../devices/m5stack/cap-cc1101/README.md) — designator `B1`, sheet 3

Sits directly at the CC1101's `RF_P` (pin 12) / `RF_N` (pin 13) port and feeds the pair of
[BGS13SN8](../../infineon/bgs13sn8/README.md) SP3T switches that select among the 315 MHz,
433 MHz and 868/915 MHz matching paths, terminating at `E1`.

Not used on any other board in this repository — the [Cap LoRa-1262](../../../devices/m5stack/cap-lora-1262/README.md)
hides its RF front end inside the shielded `Stamp LoRa-1262 Mini` module, so whatever balun
or matching it uses is invisible from outside.

## 5. Gaps

| # | Gap |
|---|---|
| 1 | **Manufacturer unidentified.** The Anaren/TTM reading in §2 is a pattern match, nothing more |
| 2 | **No datasheet.** Insertion loss, amplitude/phase balance, power handling and the real frequency range are all unknown |
| 3 | The `DNC` (5) and `NC` (6) pins' treatment on this board was not traced |
| 4 | Whether `C44` being **DNP** implies a tuning option or a depopulated alternative topology is unknown |

## 6. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| BA-1 | Cap CC1101 schematic V0.3 | primary | [`devices/m5stack/cap-cc1101/artifacts/schematic/`](../../../devices/m5stack/cap-cc1101/artifacts/schematic/) | 2026-09-04 | The part number, pin names, and the surrounding network |
| BA-2 | Cap CC1101 documentation | primary | `https://docs.m5stack.com/en/cap/Cap_CC1101` | 2026-09-04 | "multi-band RF matching circuits multiplex the 315/433/868/915 MHz bands to one RP-SMA antenna interface" — the design intent the balun serves |
