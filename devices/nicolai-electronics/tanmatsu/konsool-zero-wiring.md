# `konsool-zero` — connector wiring, host GPIO map and the numbering trap

> How the `badgeteam/konsool-zero` radio add-on is actually wired to the Tanmatsu, recovered by
> parsing its KiCad PCB rather than reading sheets by eye.
>
> Evidence: **`executed-success`** — [`tools/kicad_pcb_nets.py`](../../../tools/kicad_pcb_nets.py)
> and [`tools/kicad_netlist.py`](../../../tools/kicad_netlist.py) run 2026-09-20 against
> [`artifacts/konsool-zero/kicad/tanmantsu-zero.kicad_pcb`](artifacts/konsool-zero/kicad/tanmantsu-zero.kicad_pcb)
> (upstream `badgeteam/konsool-zero` @ `0f0b964107c15dd398ee3e44a064fb853b17aaa8`), cross-checked
> against the Tanmatsu's own IPC-D-356 fabrication netlist
> [`artifacts/production/netlist.ipc`](artifacts/production/netlist.ipc).
>
> **No hardware was available.** Nothing here was built, fitted or powered.

Background on the board itself — what is fitted, why there is no STM32WB55, licence and status —
is in [`expansion-boards.md` §2](expansion-boards.md). This file is the wiring.

---

## 1. Why this matters: a `.kicad_pcb` is ground truth, a `.kicad_sch` is not

KiCad stores no netlist in a schematic file; connectivity there is implied by wire geometry. The
**PCB** file stores *resolved* net names on every pad. So `tanmantsu-zero.kicad_pcb` is the
authoritative statement of what is connected to what, and it is what everything below is read
from. The earlier pass could only say the SPI buses "do not appear on `zero-mcu.kicad_sch`" and
labelled the conclusion `inferred`; the PCB settles it.

`J1` is the add-on's mating connector: footprint `PinHeader_2x18_P2.54mm_Vertical`, value
`Internal Add-On`, LCSC `C168945`. The Tanmatsu mainboard side is `J7` (socket, LCSC `C3975163`).

---

## 2. The full 36-pin comparison — Tanmatsu `J7` versus konsool-zero `J1`

Tanmatsu column is from the **fabrication netlist** (copper, authoritative). GPIO column is the
vendor back-expansion page, which [`gaps-and-conflicts.md` §14](gaps-and-conflicts.md) already
verified against that same fab data. konsool-zero column is from its own PCB.

Power and ground fan-out is summarised rather than listed pad-by-pad.

| Pin | Tanmatsu `J7` | P4 GPIO | konsool-zero `J1` | What konsool-zero hangs on it |
|---:|---|---:|---|---|
| 1 | `VOTG` | — | `VOTG` | *not connected* |
| 2 | `HUB_USB1_P` | — | `HUB_USB1_P` | *not connected* |
| 3 | `VBATT` | — | `VBATT` | *not connected* |
| 4 | `HUB_USB1_N` | — | `HUB_USB1_N` | *not connected* |
| 5 | `VSYS` | — | `VSYS` | *not connected* |
| 6 | `GND` | — | `GND` | ground plane (108 pads) |
| **7** | **`GND`** | — | **`VSDCARD`** ⚠ | *not connected* — **see §3** |
| 8 | `+3.3V` | — | `+3.3V` | supply (38 pads) — the whole board runs from the host 3.3 V rail |
| 9 | `INT_SCL` | 10 | `INT_SCL` | `U19.9` (CH32V003 `PC2`) |
| 10 | `INT_SDA` | 9 | `INT_SDA` | `U19.8` (CH32V003 `PC1`) |
| 11 | `E0` | **36** | `E0` | `U1.3` — CC1101 **`GDO2`** |
| 12 | `E1` | **0** | `E1` | `R1` 330 Ω → `U1.6` — CC1101 **`GDO0`** |
| 13 | `E2` | 6 | `E2` | *not connected* |
| 14 | `E3` *(VSDCARD)* | **46** | `E3` | `U5.29` — ST25R3916 **`BSS`** (SPI select, active low) |
| 15 | `E4` *(VSDCARD)* | **47** | `E4` | `U19.15` (`PD1` = **`SWIO`**), `J4.2`, `R47` 10 kΩ pull-up |
| 16 | `E5` *(VSDCARD)* | **48** | `SPI_CMD` ⚠ | `U1.20` (CC1101 `SI`), `U5.31` (ST25R3916 `MOSI`) |
| 17 | `E6` *(VSDCARD)* | **45** | `SPI_SCK` ⚠ | `U1.1` (CC1101 `SCLK`), `U5.30` (ST25R3916 `SCLK`) |
| 18 | `E7` | **7** | `SPI_D0` ⚠ | `U1.2` (CC1101 `SO`), `U5.32` (ST25R3916 `MISO`) |
| 19 | `E8` | 54 | `SPI_D1` ⚠ | *not connected* |
| 20 | `E9` | 49 | `SPI_D2` ⚠ | *not connected* |
| 21 | `E10` | **53** | `SPI_D3` ⚠ | `U1.7` — CC1101 **`CSN`** |
| 22 | `EXT_USB_P` | 26 | `EXT_USB_P` | *not connected* |
| 23 | `E11` | **52** | `E10` ⚠ | `R7` 200 Ω → IR transmit gate, `IR_TX1` test point |
| 24 | `EXT_USB_N` | 27 | `EXT_USB_N` | *not connected* |
| 25 | `E12` | **51** | `E9` ⚠ | `U6.3` — TSOP75338 IR receiver output, `IR_RX1` test point |
| 26 | `P4_TX` | 37 | `P4_TX` | *not connected* |
| 27 | `E13` | 50 | `E8` ⚠ | *not connected* |
| 28 | `P4_RX` | 38 | `P4_RX` | *not connected* |
| 29–32 | `I2S_MCLK/LRCK/DATA/SCLK` | 30/31/28/29 | same | *not connected* |
| 33 | `+3.3V` | — | `+3.3V` | supply |
| 34 | `I3C_SDA` | 33 | `I3C_SDA` | *not connected* |
| 35 | `GND` | — | `GND` | ground |
| 36 | `I3C_SCL` | 32 | `I3C_SCL` | *not connected* |

**26 of 36 pins carry identical net names. Ten do not**, and the ten split into three separate
problems, below.

---

## 3. Trap 1 — pin 7 is `GND` on the Tanmatsu and `VSDCARD` on konsool-zero

The Tanmatsu fabrication netlist gives `J7-6` **and** `J7-7` as `GND`. konsool-zero names `J1-7`
`VSDCARD` — a *supply* name.

**On konsool-zero this is inert**: the `VSDCARD` net has exactly one pad (`J1.7`) and drives
nothing, so no short exists on the board as drawn. **It is a live trap for anyone who copies the
sheet**, which is plausible because konsool-zero is the most complete worked example of a rear
add-on that exists. Connecting anything to a net called `VSDCARD` at pin 7 shorts it to ground.

Where the mislabel came from is visible in the vendor documentation: the badge.team
back-expansion page lists **35 rows for a 36-pin connector** — one signal short — and its
`Function` column is shifted by one row relative to its `Name` column (`HUB_USB1_N` is labelled
"Power output", `VBATT` is labelled "USB"). A reader reconciling 35 rows onto 36 pins has to guess
which pin is duplicated. This repository's [`pinouts-and-buses.md` §2](pinouts-and-buses.md)
guessed `GND` at both 6 and 7 and was **right**; konsool-zero guessed a `VSDCARD` rail and was
wrong.

> **Confirmed-correct, recorded per skill:** `pinouts-and-buses.md` §2's "6, 7 | GND" row is
> correct against the fabrication netlist. `executed-success`, 2026-09-20.

## 4. Trap 2 — konsool-zero's `E8`/`E9`/`E10` are the *wrong* E-numbers

At pins 23, 25 and 27 konsool-zero writes `E10`, `E9`, `E8`. The Tanmatsu calls those pins `E11`,
`E12`, `E13`.

These are not arbitrary. Map them through the GPIOs:

| Pin | P4 GPIO | Tanmatsu name (correct) | badge.team **IC page** name (wrong) | konsool-zero uses |
|---:|---:|---|---|---|
| 23 | 52 | `E11` | `E10` | **`E10`** |
| 25 | 51 | `E12` | `E9` | **`E9`** |
| 27 | 50 | `E13` | `E8` | **`E8`** |

**konsool-zero was laid out against badge.team's ESP32-P4 IC page** — the numbering
[`gaps-and-conflicts.md` §14](gaps-and-conflicts.md) proved wrong from the Tanmatsu's own
fabrication netlist (`connector page: 10 correct, 0 wrong` / `IC page: 0 correct, 8 wrong`).

This upgrades §14 from a documentation inconsistency to a defect that **propagated into silicon
layout**. It is the first concrete evidence that anyone built hardware against the bad table.

**Practical consequence.** The wiring is still correct — konsool-zero's `E10` really is pin 23 —
but the *name* is not portable. Firmware written from konsool-zero's schematic that resolves
"`E10`" using Tanmatsu documentation lands on **GPIO53** when the IR transmitter is actually on
**GPIO52**. Use pin numbers or GPIO numbers across this boundary, never E-names.

## 5. Trap 3 — the SPI bus is renamed *and* sits in the VSDCARD power domain

konsool-zero renames Tanmatsu pins 16–21 (`E5`–`E10`) to an SD-card-style bus: `SPI_CMD`,
`SPI_SCK`, `SPI_D0`, `SPI_D1`, `SPI_D2`, `SPI_D3`. Only four of the six are used — `SPI_D1` and
`SPI_D2` (pins 19, 20) are unconnected.

Resolved against the Tanmatsu pinout, the add-on's SPI bus is:

| Function | konsool-zero net | Pin | Tanmatsu `E` | **ESP32-P4 GPIO** | Power domain |
|---|---|---:|---|---:|---|
| SCLK | `SPI_SCK` | 17 | `E6` | **45** | ⚠ **VSDCARD** |
| MOSI | `SPI_CMD` | 16 | `E5` | **48** | ⚠ **VSDCARD** |
| MISO | `SPI_D0` | 18 | `E7` | **7** | low-power domain, 51 kΩ pull-up |
| CC1101 `CSN` | `SPI_D3` | 21 | `E10` | **53** | free |
| ST25R3916 `BSS` | `E3` | 14 | `E3` | **46** | ⚠ **VSDCARD** |
| CC1101 `GDO0` | `E1` | 12 | `E1` | **0** | free |
| CC1101 `GDO2` | `E0` | 11 | `E0` | **36** | free |
| ST25R3916 `IRQ` | — | — | — | — | **does not reach the host** — goes to `U19.18` only |
| CH32V003 `SWIO` | `E4` | 15 | `E4` | **47** | ⚠ **VSDCARD** |
| CH32V003 I²C | `INT_SCL`/`INT_SDA` | 9/10 | — | **10 / 9** | internal I²C bus |

> ### ⚠ The whole radio interface depends on the ESP32-P4's VSDCARD LDO
>
> `SCLK` (GPIO45), `MOSI` (GPIO48), the NFC chip select (GPIO46) and the coprocessor debug line
> (GPIO47) are **all** on pins the vendor marks *"VSDCARD LDO must be enabled to use this pin"*.
> That rail also powers the microSD slot.
>
> **Neither radio can be reached at all unless the P4's internal LDO 4 is enabled.** MISO is the
> only bus line outside the domain, so a driver that forgets this reads a bus that is held by the
> 51 kΩ pull-up on GPIO7 and sees all-ones rather than an obvious failure.
>
> Status: `inferred` from the vendor's own pin-domain annotation combined with the traced
> netlist; `not-tested` — no hardware.

**Shared bus, two chip selects.** `SCLK`/`MOSI`/`MISO` are common to the CC1101 (`U1`) and the
ST25R3916 (`U5`); `U1` selects on GPIO53 and `U5` on GPIO46. A driver must arbitrate them.

---

## 6. The two radios, pin by pin

### 6.1 `U1` — CC1101RGPR, sub-1 GHz

| Pin | Name | Net | Goes to |
|---:|---|---|---|
| 1 | `SCLK` | `SPI_SCK` | host GPIO45 |
| 2 | `SO` (`GDO1`) | `SPI_D0` | host GPIO7 |
| 3 | `GDO2` | `E0` | **host GPIO36** |
| 5 | `DCOUPL` | — | `C2` 100 nF |
| 6 | `GDO0` | via `R1` **330 Ω** | **host GPIO0** |
| 7 | `CSN` | `SPI_D3` | host GPIO53 |
| 8, 10 | `XOSC_Q1`, `XOSC_Q2` | — | `U2`, a **27 MHz oscillator** + `C4`/`C5` 9 pF |
| 12, 13 | `RF_P`, `RF_N` | — | `T1` balun → `U3`/`U4` SP3T switches → `J2` SMA |
| 17 | `RBIAS` | — | `R2` **56 kΩ** |
| 4, 9, 11, 14, 15, 18 | supplies | `+3.3V` | host 3.3 V rail |
| 16, 19, 21 | grounds | `GND` | |

Two things line up with the existing [CC1101 component record](../../../components/texas-instruments/cc1101/README.md):

- **`GDO0` through a 330 Ω series resistor** is the same treatment M5Stack uses on the Cap CC1101
  (`R4`, 330 Ω). The component record's warning applies here unchanged: **`GDO0` emits a clock by
  default after reset** until `IOCFG0` is written.
- **`GDO2` reaches the host here**, unlike the Cap CC1101 where it is consumed on-board for band
  select. konsool-zero does band select from the CH32V003 instead (§7), which leaves `GDO2` free
  as a second host interrupt on GPIO36.

### 6.2 `U5` — ST25R3916-AQWT, NFC / 13.56 MHz

| Pin | Name | Net | Note |
|---:|---|---|---|
| 20 | **`I2C_EN`** | **`GND`** | **strapped low ⇒ the part runs in SPI mode** |
| 29 | `BSS` | `E3` | SPI select, active low → host GPIO46 |
| 30 | `SCLK/SCL` | `SPI_SCK` | host GPIO45 |
| 31 | `MOSI` | `SPI_CMD` | host GPIO48 |
| 32 | `MISO/SDA` | `SPI_D0` | host GPIO7 |
| 27 | `IRQ` | `NFC_IRQ` | → `U19.18` and `TP5` — **not** to the host connector |
| 4, 5 | `XTO`, `XTI` | — | `X1` **27.12 MHz** crystal, `C24`/`C25` 6 pF |
| 13, 15 | `RFO1`, `RFO2` | — | `L12`/`L13` 270 nH → antenna matching |
| 22, 23 | `RFI1`, `RFI2` | `RFI_P`, `RFI_N` | receiver inputs |
| 17, 18, 19, 28, 33 | `EXT_LM`, `AAT_A`, `AAT_B`, `MCU_CLK`, `EP` | — | **explicit no-connects** |

The `I2C_EN`→`GND` strap is worth stating plainly because the
[ST25R3916 component record](../../../components/stmicroelectronics/st25r3916/README.md) documents
the opposite case on the M5Stack PaperMono, where `I2C_EN` is tied high through a 0 Ω link and the
part runs **I²C**. Same silicon, opposite interface, on two boards in this repository.

`AAT_A`/`AAT_B` unconnected means **adaptive antenna tuning is not implemented** — the matching
network is fixed. This is a drawn no-connect, not an omission.

## 7. `U19` — CH32V003F4U6, the helper MCU

Full pin map, from `kicad_netlist.py` on `zero-mcu.kicad_sch` cross-checked against the PCB:

| Pin | Port | Net | Role |
|---:|---|---|---|
| 1 | `PD7` | `RFID_WR` | 125 kHz RFID write drive |
| 2 | `PA1` | ← `U17` via `C71` | **25 MHz oscillator input** (`S3225SMD25MOSC`) |
| 3 | `PA2` | — | no-connect ⇒ `U17` is a single-ended **XO driving OSCI**, not a crystal |
| 4, 21 | `VSS` | `GND` | |
| 5 | `PD0` | — | no-connect |
| 6 | `VDD` | `+3.3V` | |
| 7 | `PC0` | `RF_SW_1` | → `U3.8`, `U4.8` band select |
| 8 | `PC1` | `INT_SDA` | **host internal I²C SDA** (GPIO9) |
| 9 | `PC2` | `INT_SCL` | **host internal I²C SCL** (GPIO10) |
| 10 | `PC3` | `RF_SW_0` | → `U3.1`, `U4.1` band select |
| 11, 12 | `PC4`, `PC5` | — | no-connect |
| 13 | `PC6` | `RFID_CARRIER` | → `U12.4` comparator |
| 14 | `PC7` | `RFID_IN` | ← `R14` 100 Ω |
| 15 | `PD1` | **`SWIO`** → `E4` | **single-wire debug, brought out to host GPIO47 and to `J4`**, `R47` 10 kΩ pull-up |
| 16, 17 | `PD2`, `PD3` | — | no-connect |
| 18 | `PD4` | `NFC_IRQ` | ← ST25R3916 `IRQ` |
| 19 | `PD5` | `RFID_RF_OUT` | 125 kHz drive |
| 20 | `PD6` | `RFID_PULL` | → `R19` 220 Ω |

**Six pins are explicit no-connects** (`PA2`, `PD0`, `PC4`, `PC5`, `PD2`, `PD3`) — drawn
assertions, not blanks.

### 7.1 The host can reflash the add-on's MCU

`PD1`/`SWIO` is the CH32V003's single-wire debug pin, and it lands on **expansion pin 15 =
GPIO47**. The Tanmatsu already ships an Espressif component
([`nicolaielectronics/rvswd`](https://components.espressif.com/components/nicolaielectronics/rvswd))
that reprograms CH32V0xx/CH32V20x/CH32V30x parts from the ESP32-P4 — that is how the mainboard
coprocessor is reflashed (see [`README.md` § Architecture](README.md)).

So the same mechanism reaches this add-on: **the ESP32-P4 can reflash konsool-zero's CH32V003
over the expansion connector, with no programmer and no `J4` header.** `inferred` from the
netlist plus the existing rvswd capability; `not-tested`.

### 7.2 What the MCU is for

It owns the **125 kHz RFID analog chain** (`RFID_*` → `U10`/`U14` LMV358 op-amps, `U12` LMV331
comparator, `U11`/`U13`/`U15`/`U16` 1N4148 envelope detectors, `L14` 400 mH coil) and **sub-GHz
band selection** (`RF_SW_0/1` → the two Infineon `BGS13S4N9` SP3T switches), and it relays the
**NFC interrupt**. It is an I²C slave on the host's internal bus.

It is **not** in the CC1101 or ST25R3916 SPI path at all — the PCB confirms what the earlier pass
could only infer. Those radios are host-driven; the CH32V003 is a helper.

**Consequence for a driver author:** the NFC interrupt does not reach the ESP32-P4 on any wire.
Either poll the ST25R3916, or read the interrupt state from the CH32V003 over I²C — which requires
knowing its I²C address and register map. **No firmware exists in the repository for this MCU**,
so that interface is undefined. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

---

## 8. Other connectors

| Ref | Footprint | Nets | Purpose |
|---|---|---|---|
| `J2` | SMA edge mount, value `LoRa` | `ANT_OUT` ← `U4.4` | sub-GHz antenna |
| `J3` | 1×02 2.54 mm | `GND`, `IBTN` (via `D1` TVS) | **iButton** 1-Wire contact |
| `J4` | 1×02 2.54 mm | `GND`, `E4`/`SWIO` | CH32V003 debug header |
| `NT1`, `NT2` | net ties | `NFC_ANT` | NFC antenna feed |
| `H1`, `H2` | mounting | `GND` | |

---

## 9. Bonus finding — the "expansion template" is a copied file, not a repository

[`expansion-boards.md` §1](expansion-boards.md) records that
`badgeteam/konsool-expansion-template` is an empty repository. Confirmed again this pass: the
clone at `scratch/tanmatsu/sources/konsool-expansion-template/` has a `.git` directory with
**no `objects/` and no `refs/`**, `HEAD` reading `ref: refs/heads/.invalid`, and zero working
files. `git` does not even recognise it as a repository.

The template nevertheless exists — it is **copied between add-on projects by hand**:

```
fa79df7fc3988227bebae85eccb74a694b47a6fd14ca758553906ad9f4636dd1  konsool-zero/expansion-template.kicad_sch
fa79df7fc3988227bebae85eccb74a694b47a6fd14ca758553906ad9f4636dd1  konsool-18650-expansion/expansion-template.kicad_sch
```

**Byte-identical.** The `.kicad_pcb` files differ, as expected — each project laid out its own
board from the shared schematic. `executed-success`, 2026-09-20.

A new add-on designer should therefore take `expansion-template.kicad_sch` from either project;
this repository keeps a copy at
[`artifacts/konsool-zero/kicad/expansion-template.kicad_sch`](artifacts/konsool-zero/kicad/expansion-template.kicad_sch).
But note it inherits the **pin-7 `VSDCARD` mislabel** and the **wrong `E8`/`E9`/`E10` names**
described above — check it against [`pinouts-and-buses.md` §2](pinouts-and-buses.md) before use.

---

## 10. Reproducing this

```bash
# authoritative resolved netlist from the PCB
python3 tools/kicad_pcb_nets.py \
  devices/nicolai-electronics/tanmatsu/artifacts/konsool-zero/kicad/tanmantsu-zero.kicad_pcb --all

# one reference designator
python3 tools/kicad_pcb_nets.py \
  devices/nicolai-electronics/tanmatsu/artifacts/konsool-zero/kicad/tanmantsu-zero.kicad_pcb J1

# pin *names* (the PCB carries pad numbers only)
python3 tools/kicad_netlist.py \
  devices/nicolai-electronics/tanmatsu/artifacts/konsool-zero/kicad/zero-mcu.kicad_sch --ref U19
python3 tools/kicad_netlist.py \
  devices/nicolai-electronics/tanmatsu/artifacts/konsool-zero/kicad/nfc-block.kicad_sch --ref U5
```

All four `executed-success` on 2026-09-20, Python 3, no third-party dependencies.
`kicad_netlist.py` on `nfc-block.kicad_sch` takes a few minutes — it does geometric union-find
over every wire segment.

---

## 11. Status and confidence

| Claim | Evidence | Status |
|---|---|---|
| `J1` pin → net mapping | parsed from `tanmantsu-zero.kicad_pcb` | `executed-success` |
| `J7` pin → net mapping | parsed from `netlist.ipc` (fab data) | `executed-success` |
| E-name → GPIO | vendor back-expansion page, previously verified against fab data | `executed-success` (prior pass) |
| Pin 7 `VSDCARD` mislabel is inert on konsool-zero | net has one pad | `executed-success` |
| konsool-zero follows the bad IC-page E-numbering | three-way GPIO match | `executed-success` |
| Radio bus needs the VSDCARD LDO enabled | vendor pin annotation + traced netlist | `inferred`, `not-tested` |
| P4 can reflash the CH32V003 over `SWIO` | netlist + existing `rvswd` component | `inferred`, `not-tested` |
| CH32V003 I²C address / register map | — | **unknown, no firmware published** |

The board has **one commit, no README and no firmware**. Treat all of this as a design study.
