# Nsiway NS4150B

- **Category:** mono **class-D audio power amplifier**, ~3 W into 4 Ω class, single-supply, with a shutdown/enable input
- **Manufacturer:** Nsiway (NSIWAY / 纳芯威)
- **Document status:** **no datasheet obtained.** `reference-only`
- **Research status:** **stub — identity only.** The part number is read directly from a schematic; nothing beyond that is established here
- **Retrieved:** 2026-09-01. **Nothing verified on hardware.**

## Evidence for the part number

Read as the literal text `NS4150B` from the
[ESP32-S3-ePaper-3.97 schematic](../../../devices/waveshare/esp32-s3-epaper-3.97/artifacts/schematic/ESP32-S3_e-Paper-3.97-schematic.pdf)
text layer, and independently named as "NS4150B — Audio power amplifier chip" in
Waveshare's storefront and documentation "Onboard Resources" list.

Two sources, one of them design data. **The designator was confirmed to appear in the
evidence before this record was created**, per the method's rule against creating a
component record from a candidate or a near-miss part number.

## What is *not* established

Everything else. The category line above describes the NS4150/NS4150B family as
generally understood, and is **`inferred`, not sourced** — no datasheet was obtained
in this pass. Specifically unknown:

- Supply range, output power, load impedance, efficiency, THD+N
- Gain setting and whether it is fixed or resistor-programmable
- Shutdown polarity and timing
- Package and pinout
- Whether `NS4150B` differs from `NS4150` in any way that matters

**Do not design against the summary line at the top of this file.** Obtain the
datasheet first.

## Acquisition status

| Field | Value |
|---|---|
| Disposition | **`reference-only`** |
| Reacquisition | **`manual`** |
| Attempts this pass | **none** — the part was identified late, and Waveshare's `files.waveshare.com/wiki/common/` pool was not probed for it |
| Suggested next attempts | `files.waveshare.com/wiki/common/NS4150B.pdf` and variants; Nsiway's own site; the usual distributor datasheet aggregators |
| Licence | `unknown` |

Recorded honestly as an open acquisition rather than omitted — per the method,
a failed or unattempted acquisition belongs in the record.

## Used by

### [Waveshare ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md)

The board's speaker amplifier, sitting between the
[ES8311 codec](../../everest-semiconductor/es8311/README.md) DAC output and the
**MX1.25 / PH1.25-2P speaker header `H2`**. The board ships with an **8 Ω 1 W
speaker** in every SKU, per the storefront's package contents.

Schematic nets around it include `PA_INL+`, `PA_INL-`, `PA_OUTL+`, `PA_OUTL-`, with
`AudioCTR_PIN` on **GPIO39** as the enable/gate — a pin the schematic's allocation
table **also** assigns to the IMU's `AXIS_INT1`, which is
[unresolved](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws9--gpio39-carries-two-functions).

Series inductors `L7`/`L8` on the outputs are consistent with class-D output
filtering. `inferred` from net adjacency.

### M5Stack Cardputer ADV (K132-Adv) — [`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md)

Designator **U5** on schematic sheet 3. Analog input from the
[ES8311](../../everest-semiconductor/es8311/README.md) DAC (`INP` pin 3, `INN` pin 4), output
`VOP`/`VON` (pins 8/5) through ferrites FB1/FB2/FB3 to the 8 Ω 1 W cavity speaker. Input network
R16/R17 100 k 1 %, R23 10 k 1 %; `BYPASS` (pin 2) to C16 1 µF.

**`CTRL` (pin 1) = the `AMP_EN` net, and no GPIO reaches it.** `AMP_EN` is generated in hardware
from the 3.5 mm jack's `HP_DET` contact through D3 (`1N4148WT`) and Q4 (`2N7002T`) with
R40/R42 1 k. Inserting a plug mutes the amplifier; **software can neither read the jack state nor
override the mute.** This is the mechanism behind M5Stack's note *"When a 3.5 mm headphone jack
is inserted, the speaker amplifier will be disabled."*

Replaces the [NS4168](../ns4168/README.md) used on the Cardputer v1.0/v1.1, which took I²S
directly and had no analog input, no enable control and no line-out path.

*Added 2026-09-07 from `archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md` §3.2.*

## See also

- [ES8311](../../everest-semiconductor/es8311/README.md) — the codec that feeds it
- [All components](../../README.md)
