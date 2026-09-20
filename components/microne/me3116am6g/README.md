# Microne ME3116AM6G — wide-input step-down converter

- **Category:** asynchronous buck (step-down) DC-DC converter IC with integrated high-side
  switch and bootstrap, SOT23-6.
- **Manufacturer:** **Nanjing Micro One Electronics** (南京微盟, "Microne") — inferred from the
  `ME3xxx` part-number family, which is Micro One's buck/boost series. **No datasheet was
  located** and no vendor page was retrieved in this pass, so the manufacturer attribution is
  `inferred`, not read.
- **Research status:** ⚠ **Schematic-only.** Every fact below comes from the M5Stack DinMeter
  schematic. No component document was obtained.
- **Retrieved:** 2026-09-04

The **6–36 V wide-range input converter** of the M5Stack DinMeter — the part that makes the
board a panel instrument rather than a 5 V dev board.

---

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Part string | **`ME3116AM6G`** | DinMeter schematic, visible value text at (387, 99.8), associated with `U1` |
| Pin count / names | **6**: `VIN`, `BST`, `EN`, `LX`, `GND`, `FB` | DinMeter schematic `U1` symbol, `PIU101`–`PIU106` |
| Topology | asynchronous buck — external Schottky and external inductor, bootstrap capacitor on `BST` | implied by the pin set + the fitted `L1` and Schottky diodes |
| Input on this board | **6 – 36 V** | M5Stack specification row |
| Output on this board | `+5VIN` rail | schematic net |
| Feedback divider | `R5` 56 kΩ (upper) / `R6` 10 kΩ (lower) | schematic |
| Inductor | `L1` **10 µH**, 3015 package | schematic |
| Input bulk | `C24` **10 µF / 35 V** | schematic |
| Decoupling | `C7`, `C8` 100 nF; `C6` (near `D9`) | schematic |
| Freewheel / clamp | `D9`, `D11`, `D12` (`SD36`), `D13` — B5819W / SD36 Schottky | schematic |

Feedback arithmetic: 5 V out through a 56 k / 10 k divider implies a reference near
5 × 10/(56+10) ≈ **0.758 V**, which is a common buck reference value. This is arithmetic on
read values, **not** a datasheet figure — it is offered as a consistency check, not a
specification.

## 2. What is not established

- **No datasheet.** Not from Micro One, not from a distributor, not from an aggregator, in this
  pass. Searches logged in
  [`devices/m5stack/dinmeter/research-log.md`](../../../devices/m5stack/dinmeter/research-log.md).
- Absolute-maximum input, switching frequency, current limit, efficiency, thermal behaviour,
  `EN` threshold, soft-start, protection behaviour — all **unknown**.
- **The `AM6G` suffix is unparsed.** Whether it encodes package, grade, or a voltage option is
  unknown.
- **No chip-marking confirmation.** No teardown photograph of the DinMeter was inspected. The
  part number rests on the schematic value text alone.

**What would resolve it:** a Micro One datasheet, or a photograph of `U1`'s top marking on a
real board.

## 3. Practical consequences for firmware and integration

- The **36 V ceiling is the board's DC-input rating**, and it is set by this part plus its
  input capacitor (`C24` is rated 35 V — *below* the 36 V spec). Running sustained at 36 V puts
  `C24` at 103 % of its rating. That is a design observation from read values, not a fault
  report; derating a 35 V X7R at 36 V is common but not free.
- `EN` is available; whether M5Stack ties it to anything switchable was not traced.
- Nothing about this part is firmware-visible. There is no register interface.

## 4. Artifacts

**None.** No document was obtained. The schematic that establishes the part is a *device*
artifact and lives at
[`devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf`](../../../devices/m5stack/dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf).

---

## Used By

### M5Stack DinMeter (K134) and DinMeter v1.1 (K134-V11)

`U1`. Takes 6–36 V from the 2-pin screw terminal `J1` (via reverse/clamp Schottkys) and produces
the `+5VIN` rail that feeds the Stamp module's pad 13, the [TP4057](../../generic/tp4057/README.md)
charger and the `U7` CN809J supervisor. It is the *only* path from the DC terminal into the
board.

→ [`devices/m5stack/dinmeter/features/power-and-battery.md`](../../../devices/m5stack/dinmeter/features/power-and-battery.md)
