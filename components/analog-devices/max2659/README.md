# Maxim / Analog Devices MAX2659

- **Category:** **GNSS low-noise amplifier** (single-stage, high-gain LNA for 1.575 GHz L1)
- **Package as fitted:** 6-pin (`GND` 1, `GND` 2, `RFIN` 3, `VCC` 4, `SHDN` 5, `RFOUT` 6)
- **Research status:** **no datasheet retrieved.** Identity and integration come from an
  M5Stack schematic symbol. Performance figures below are the *board's* claims, not the
  part's.
- **Retrieved:** 2026-09-04

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | Maxim Integrated, now **Analog Devices** | part-number lineage, `inferred` |
| Part | **`MAX2659`** | schematic comment, Cap LoRa-1262 `U1` |
| Function | GNSS/GPS **low-noise amplifier** | function follows from the pinout and its position between a patch antenna and a GNSS receiver |
| Pinout as fitted | 1 `GND`, 2 `GND`, 3 `RFIN`, 4 `VCC`, 5 `SHDN`, 6 `RFOUT` | schematic |

⚠ **Gain, noise figure, current and supply range are not stated here** because no datasheet
was retrieved. The MAX2659 family is widely cited as a ~+20 dB, sub-1 dB-NF GNSS LNA, but
**this record does not assert that** — it is exactly the kind of remembered number that
should be checked against the datasheet before use.

## 2. Why a board fits one

A passive ceramic patch antenna feeding a GNSS receiver directly loses sensitivity to trace
loss and to the receiver's own noise figure. Putting a high-gain, low-noise amplifier
**immediately at the antenna** sets the system noise figure to (approximately) the LNA's
own, which is what buys the last several dB of tracking sensitivity.

That is visible in the Cap LoRa-1262's claimed figures: **tracking −162 dBm**, acquisition
−160 dBm, cold start −148 dBm — numbers a bare ATGM336H module typically does not reach.

## 3. Used By

### [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) — designator `U1`

| Pin | Net |
|---:|---|
| 1, 2 `GND` | `GND` |
| **3 `RFIN`** | ← `J1` ceramic patch antenna (`ANT1818-04`, 18 × 18 × 4 mm) via **`L1` 6.8 nH ±5 %** |
| 4 `VCC` | `+3.3V` |
| **5 `SHDN`** | **tied — the host cannot shut the LNA down** |
| **6 `RFOUT`** | → `M2` `ATGM336H-6N` pin 11 `ANT`, via **`C5` 470 pF** |

Decoupling: `C6` 100 nF, `C7` 33 nF.
Supply routing: the GNSS module's `VCC_RF` (pin 14) reaches `+3.3V` through **`FB2`
120 Ω/MB**, and its digital `VCC` (pin 8) through **`FB3`** — M5Stack isolates the RF supply
from the digital one and both from the LoRa module's rail.

**Consequence worth stating:** because `SHDN` is tied, the LNA's quiescent current is paid
whenever the Cap is powered, even with the GNSS receiver asleep. The predecessor board's
published *"GPS sleep, LoRa standby: DC 5 V @ 3.16 mA"* is therefore a floor that includes
an always-on LNA. Contrast **[Stamp C6LoRa](../../../devices/m5stack/stamp-c6lora/README.md)**,
where an I/O expander *does* gate the LNA enable — the better design for battery life.

## 4. Related components

- [`components/zhongkewei/atgm336h-6n`](../../zhongkewei/atgm336h-6n/README.md) — what it feeds
- [`components/generic/gnss-ceramic-patch-antenna`](../../generic/gnss-ceramic-patch-antenna/README.md) — what feeds it

## 5. Local artifacts

**None.** Analog Devices publishes the MAX2659 datasheet; it was not fetched by this pass.
Doing so would let §1 be filled in properly.

## 6. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| M-1 | Cap LoRa-1262 schematic V1.1 | M5Stack | primary | schematic | [`devices/m5stack/cap-lora-1262/artifacts/schematic/`](../../../devices/m5stack/cap-lora-1262/artifacts/schematic/) | 2026-09-04 | Part identity, six-pin net list, `SHDN` tied |
| M-2 | Cap LoRa-1262 documentation | M5Stack | primary | official page | `https://docs.m5stack.com/en/cap/Cap_LoRa-1262` | 2026-09-04 | The −162 dBm tracking claim the LNA enables |
