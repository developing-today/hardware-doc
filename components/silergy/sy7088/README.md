# Silergy SY7088 — synchronous step-up (boost) converter

- **Category:** synchronous boost DC-DC converter with integrated switches.
- **Manufacturer:** **Silergy Corp** — inferred from the `SY7xxx` part-number family, which is
  Silergy's DC-DC series. **No datasheet was located** in this pass; attribution is `inferred`.
- **Research status:** ⚠ **Schematic-only.**
- **Retrieved:** 2026-09-04

The **battery-to-5 V boost** of the M5Stack DinMeter — what powers the Grove ports and the
Stamp module when the board is running from the Li-ion cell.

---

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Part string | **`SY7088`** | DinMeter schematic, visible value text at (586, 214.8), associated with `U3` |
| Pin count / names | **9**: `LX`, `LX`, `OUT`, `OUT`, `IN`, `EN`, `FB`, `GND`, `PGND` | DinMeter schematic `U3`, `PIU301`–`PIU309` |
| Topology | synchronous boost (`LX` + `OUT` both present, no external Schottky in the loop) | pin set + fitted parts |
| Input on this board | `VBAT_OUT` (Li-ion, ~3.0–4.24 V) | schematic net |
| Output on this board | `+5VOUT` — Grove `J3`/`J4` pin 3 | schematic net |
| Inductor | `L4` **1.5 µH**, 3015 package (`R12` 0 Ω in series) | schematic |
| Feedback divider | `R16` **52.3 kΩ** / `R18` **15 kΩ** | schematic |
| Vendor formula printed on the sheet | **`Vout = 1.2 V × (R1/R2 + 1)`** | schematic annotation at (575.4, 233.2) |
| Output capacitance | `C18` 22 µF, `C19` 22 µF, `C16`/`C17` 10 µF | schematic |

**Computed output:** 1.2 × (52.3 / 15 + 1) = **≈ 5.38 V**.

M5Stack's specification calls the Grove rail "DC 5 V @ 220 mA". The schematic's own divider and
its own printed formula give 5.38 V. Both are primary M5Stack statements and they disagree by
~7.6 %. This is recorded as a conflict in
[`devices/m5stack/dinmeter/gaps-and-conflicts.md`](../../../devices/m5stack/dinmeter/gaps-and-conflicts.md) §6.
**If you are attaching a 5 V-max peripheral to a Grove port on battery power, measure the rail
first.**

## 2. What is not established

No datasheet: switching frequency, current limit, efficiency, `EN` threshold, true-disconnect
behaviour, maximum output current, thermal limits — all **unknown**. No chip-marking
confirmation (no teardown photograph inspected).

## 3. Artifacts

**None.** Establishing evidence is the device schematic:
[`devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf`](../../../devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf).

---

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

`U3`. Boosts the battery path (`VBAT_OUT`, after the `Q3`/`Q6` AP40P05 power-path FETs) to
`+5VOUT`, which supplies **both Grove ports** (`J3` PORT.A and `J4` PORT.B, pin 3 on each) and
`C5` decoupling. On USB or DC power the same rail is present; the boost is what keeps the Grove
5 V alive on battery.

→ [`devices/m5stack/dinmeter/features/power-and-battery.md`](../../../devices/m5stack/dinmeter/features/power-and-battery.md)
→ [`devices/m5stack/dinmeter/features/porta-portb-expansion.md`](../../../devices/m5stack/dinmeter/features/porta-portb-expansion.md)

### M5Stack Cardputer v1.0, v1.1 and ADV

Designator **U2** on all three. Boost from `VBAT_OUT` (through R2 0 Ω) to **`+5VOUT`**, with
L1 **3015 1.5 µH**, input C4 22 µF / C5 1 µF, feedback divider **R4 75 kΩ / R6 22 kΩ**.

The sheet prints its own formula beside the part — `Vout = 1.2 V × (R1/R2 + 1)` — giving
**≈ 5.29 V**. **Inferred, not measured.**

`+5VOUT` feeds the Grove connector's red wire, the CAP header's `5VOUT` pin (ADV only) and the
[SY8089](../sy8089/README.md) buck that makes 3.3 V. So the entire 3.3 V domain is paid for at
the product of two converter efficiencies — worth remembering when reading M5Stack's current
figures.

**No current limit is published for the Grove or CAP 5 V output on the ADV.** The CardputerZero's
equivalent port is specified at **< 500 mA**; do not assume more.

Records: [v1.0](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[v1.1](../../../devices/m5stack/cardputer-v1.1/README.md) ·
[ADV](../../../devices/m5stack/cardputer-adv/README.md)

*Added 2026-09-07 from `scratch/m5stack-cardputer/index-fragments.md` §3.8.*
