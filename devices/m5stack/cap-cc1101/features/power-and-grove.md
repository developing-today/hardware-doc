# Power gate and Grove pass-through — Cap CC1101 (U219)

Snapshot 2026-09-04, schematic **V0.3 / 2026-05-28**.

## 1. The Cap is host-switchable — unlike the LoRa Cap

| Item | Value | Evidence |
|---|---|---|
| Regulator | **`U1` JW5712** buck, `IOUT: 0~0.6 A` | **[SCH]** sheet 1 |
| Inductor | `L1` `MWTC201608S2R2` (2.2 µH) | **[SCH]** |
| Input caps | `C1` 1 nF, `C2`/`C3`/`C4` 22 µF | **[SCH]** |
| Output caps | `C5` 22 µF, `C6` 100 nF | **[SCH]** |
| **Enable** | **`POWER_EN`** ← Cap-Bus **pin 8** ← host **G3** → `U1` `ENB` | **[SCH]** sheet 1; **[DOC]** pin map |
| Enable network | `R1` **100 kΩ** | **[SCH]**; **polarity `inferred`, not traced** |

**Cap-Bus pin 8 means something completely different on the two Caps.** On the
[Cap LoRa-1262](../../cap-lora-1262/features/power-and-grove.md) it is `LoRa_RST`; here it
is `POWER_EN` for the whole board. Any auto-detect logic that assumes pin-8 semantics
across Caps is wrong.

Practical consequence, and it is a good one: the host can **fully power down** the CC1101,
the ST25R3916 and everything else on this Cap with one GPIO. That is how the vendor's
**140.87 µA @ 5 V** sleep figure is achievable — it is a board that can be switched off, not
merely a pair of chips in their own low-power modes.

> ⚠ The `R1` polarity was not traced end-to-end from the PDF text layer, so whether the Cap
> defaults **on** (pull-up, host pulls low to disable) or **off** (pull-down, host must
> drive high) is **not established**. Both vendor documentation and the pin-map name the
> signal `POWER_EN`, which conventionally implies **active-high enable**. Bring-up code
> should therefore drive **G3 HIGH and wait** before touching SPI. `inferred`.

## 2. Bring-up order

1. Host **G3 → OUTPUT, HIGH** (`POWER_EN`).
2. Allow the buck to settle (no time given by the vendor; `not-tested`).
3. Configure SPI.
4. `radio.begin()` for the CC1101, and/or `addSPI(...)` for the NFC front end.
5. `setRfBand()` — [`band-switching.md`](band-switching.md).

Powering down is the reverse; note the CC1101 will lose all configuration.

## 3. Grove pass-through (`J1`, HY2.0-4P)

| Wire | Colour | Net | Host |
|---|---|---|---|
| 1 | Black | `GND` | — |
| 2 | Red | `5V` (`+5VOUT`) | host 5 V |
| 3 | Yellow | `SDA` | **G8** |
| 4 | White | `SCL` | **G9** |

Same arrangement as the LoRa Cap: a tap onto the host's **shared** I²C bus, not a private
one. **Unlike the LoRa Cap, there is no I²C device on this board at all**, so there is no
address to collide with — a Grove sensor here is simply an extra device on the host bus.

The vendor markets this as *"HY2.0-4P Grove expansion interface — supports sensor module
expansion"*, which is fair: with only one Cap slot on the host, the pass-through is the
only way to add anything else.

## 4. Consumers of `VDD_3V3`

| Load | Notes |
|---|---|
| `U3` CC1101 — `DVDD`(4), `AVDD`(9,11,14,15) | `C37`–`C41` 100 nF |
| `U2` ST25R3916 — eight supply pins | `C21`–`C36`, a **10 nF + 10 µF pair per pin** |
| `U4`, `U5` BGS13SN8 switches | `VDD1`/`VDD` with `C56`/`C57` 100 nF |

The ST25R3916's decoupling is the dominant passive cost on the board and it is not
optional; under-decoupling an NFC front end costs read range rather than producing a clean
failure. See [`nfc.md` §10](nfc.md).

## Applicability

| Field | Value |
|---|---|
| Hardware | U219 schematic V0.3 |
| Evidence | Parts/values **[SCH]** `executed-success`; **enable polarity `inferred`** |
| Last verified | 2026-09-04 |
