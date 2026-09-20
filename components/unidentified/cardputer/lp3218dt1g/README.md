# `LP3218DT1G` — power-path MOSFET (manufacturer unidentified)

> **This is an unidentified part.** `LP3218DT1G` is the value string read from the M5Stack
> Cardputer schematics; **the manufacturer has not been established** and no datasheet was
> located. Scoped to the Cardputer family rather than filed under a guessed vendor, per the
> research skill's rule for unidentified parts.
> Record created **2026-09-04**.

## What is actually known

| Fact | Evidence | Confidence |
|---|---|---|
| The value string is exactly `LP3218DT1G` | appears three times on Cardputer ADV schematic sheet 1 and on the v1.0/v1.1 shared schematic | **high** — read from a rendered sheet crop, not only from the text layer |
| Three are fitted, designators **Q1, Q2, Q3** | designator census, all four ADV sheets | **high** |
| They sit in the **battery power path** | Q1 between `VBAT_IN` and the charger/supervisor block; Q2 and Q3 between `BAT+` and `VBAT_OUT` | **high** |
| The symbol is a **P-channel MOSFET with a body diode**, drawn source-up in a high-side load-switch configuration | rendered crop of sheet 1 | **medium** — read from the symbol, which is a vendor drawing |
| Gate network involves R7 100 kΩ and the CN809J's `RESET` output | rendered crop | **medium** |

## What is not known

* **Manufacturer.** The `DT1G` suffix is an **ON Semiconductor / onsemi packaging convention**
  (`D` = SOT-223-class or dual, `T1G` = tape-and-reel, green), which is suggestive but is used by
  several vendors and by second sources copying the convention. `LP3218` itself does not resolve
  to an onsemi part in any source located in this pass.
* Voltage and current ratings, `R_DS(on)`, gate threshold, package.
* Whether all three are the same channel type.

## Why it is recorded rather than guessed

The skill is explicit that a candidate must never be promoted to a finding, and that a part
number differing by one character from a real part on a different board is a common trap.
`LP3218` is close enough to several real part numbers (`LP3218`, `LP3210`, `AO3401`-class
alternatives) that guessing would be worse than saying nothing.

**What would settle it:** a photograph of the Cardputer mainboard showing Q1–Q3's top marking, or
a BOM. Neither is published.

## Used By

### M5Stack Cardputer ADV (K132-Adv) — [`devices/m5stack/cardputer-adv`](../../../../devices/m5stack/cardputer-adv/README.md)

**Q1, Q2, Q3** on schematic sheet 1.

* **Q1** sits between `VBAT_IN` and the downstream rail, gated from the network that includes the
  **CN809J** supervisor's `RESET` output and R7 (100 kΩ). This is the classic arrangement for
  "hold the load off until the supply is good".
* **Q2** and **Q3** sit between the battery connector `J8` (`BAT+`/`BAT-`) and `VBAT_OUT`,
  back-to-back — the usual way to make a bidirectional switch out of two MOSFETs whose body
  diodes would otherwise conduct.

Together with `D1`/`D2` (`SS34` Schottky) from `+5VIN`, this is the board's **power path**:
it selects between USB and battery, and prevents the battery back-feeding USB.

**Firmware relevance: none directly** — no GPIO reaches these gates. They matter because they
determine what happens when USB is inserted or removed under load, and they are part of the
circuit that makes M5Stack's *"switch the power to ON to charge"* instruction necessary.

### M5Stack Cardputer v1.0 (K132) and v1.1 (K132-V11)

[`devices/m5stack/cardputer-v1.0`](../../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../../devices/m5stack/cardputer-v1.1/README.md)

Same three designators, same value string, on the shared schematic (SHA-256 `6016c1fe…`). Part
of the power train that is **carried over unchanged** across all three Cardputer generations.

## If you are replacing one

Do **not** substitute from this record — it does not contain a rating. Read the part off the
board, or choose a P-channel MOSFET rated well above 5 V with low `R_DS(on)` at 2.5 V gate drive
and a package that fits, and verify the body-diode orientation matches the original.

## Resolution path

1. Board photograph of Q1–Q3 top marking (highest value, lowest effort).
2. `github.com/m5stack/M5_Hardware` — no BOM was found for `K132-Adv` in this pass, but only the
   `Structures` directory was ever linked; the repository was not walked.
3. Ask M5Stack support.
