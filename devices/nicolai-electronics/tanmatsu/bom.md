# Tanmatsu — bill of materials

> Full production BOM, annotated with each part's role.
> Source: [`artifacts/production/bom.csv`](artifacts/production/bom.csv), from `tanmatsu-hardware` @ `640805dd` (2026-02-25), **CERN-OHL-P**.
> Retrieved **2026-08-24**. 84 BOM lines; LCSC part numbers are the vendor's own and link to LCSC search.

## Why this BOM is unusually useful

Nicolai Electronics publishes the **production** BOM — designators, footprints, quantities and **LCSC part numbers for every line** — not a marketing parts list. Combined with `positions.csv` and `netlist.ipc` in the same directory, this is enough to actually have the board fabricated and assembled. That is rare for any commercial product and is the practical meaning of the CERN-OHL-P licence here.

A few things the BOM reveals that the prose documentation does not:

- **`U9` is a Winbond `W25Q128JVS`** — the 16 MB flash is a discrete SOIC-8 part, not in-package. It is replaceable/reflashable externally if you ever truly brick the P4.
- **72 × `1N4148WS` diodes (`D10`…)** — one per key, giving the keyboard matrix full **N-key rollover** without ghosting. A deliberate quality decision for a device meant to be typed on.
- **8 × `LTW-010DCG-SR-G`** white LEDs for the keyboard backlight, plus **6 × `SK6805`** addressable RGB LEDs.
- **`U19` `LR8341A-M25`** is the always-on standby LDO that keeps the coprocessor's RTC alive while the device is "off".
- **`U11` `74LVC2G02` (dual NOR)** is part of the power **latch circuit** that lets the coprocessor switch the device on from an RTC alarm.
- **Three crystals**: 40 MHz (P4), 12 MHz (CH32V203), 32.768 kHz (RTC watch crystal).
- **`Y3` + `U19` + `U11` together** are the entire always-on subsystem — worth studying if you are designing something with similar standby behaviour.

## Full BOM

| Ref | Value / MPN | Qty | Footprint | LCSC | Function |
|---|---|---:|---|---|---|
| C1, C17, C18, C2, C22, C28, C41, C57, C65… | `1u` | 15 | 0603 | [C5199872](https://www.lcsc.com/search?q=C5199872) |  |
| C3, C32, C42, C43, C45, C46, C48, C49, C5… | `10u` | 17 | 0805 | [C3039694](https://www.lcsc.com/search?q=C3039694) |  |
| C10, C11, C12, C14, C15, C19, C20, C21, C… | `100n` | 35 | 0402 | [C307331](https://www.lcsc.com/search?q=C307331) |  |
| C13, C16, C34, C35, C75, C76 | `22p` | 6 | 0402 | [C1555](https://www.lcsc.com/search?q=C1555) |  |
| C44 | `47n` | 1 | 0603 | [C469624](https://www.lcsc.com/search?q=C469624) |  |
| C47 | `4u7` | 1 | 0603 | [C69335](https://www.lcsc.com/search?q=C69335) |  |
| C58, C59, C61, C63, C67, C78, C79 | `22u` | 7 | 0805 | [C602037](https://www.lcsc.com/search?q=C602037) |  |
| C77 | `0.39u` | 1 | 0603 | [C1623](https://www.lcsc.com/search?q=C1623) |  |
| C83, C84, C85, C86 | `10n` | 4 | 0402 | [C15195](https://www.lcsc.com/search?q=C15195) |  |
| CN1 | `DF37NB-24DS-0.4V(51)` | 1 | CONN-SMD_DF37NB-24DS-0.4V | [C3036280](https://www.lcsc.com/search?q=C3036280) | **Display board-to-board connector** (MIPI DSI + 24 V backlight) |
| D1 | `ESD prot.` | 1 | D_SOD-323 | [C22363742](https://www.lcsc.com/search?q=C22363742) |  |
| D2 | `2.0v` | 1 | D_SOD-123 | [C438287](https://www.lcsc.com/search?q=C438287) |  |
| D3 | `2.7v` | 1 | D_SOD-323F | [C550976](https://www.lcsc.com/search?q=C550976) |  |
| D10, D11, D12, D13, D18, D19, D20, D21, D… | `1N4148WS` | 72 | D_SOD-323 | [C2843305](https://www.lcsc.com/search?q=C2843305) | **Keyboard matrix diodes** — 72 of them, one per key |
| D14, D15, D16, D17, D4, D5, D6, D7 | `LTW-010DCG-SR-G` | 8 | LTW-010DCG-SR-G | [C5175309](https://www.lcsc.com/search?q=C5175309) | Keyboard backlight LEDs ×8 (white) |
| D84 | `LED` | 1 | 0603 | [C7496820](https://www.lcsc.com/search?q=C7496820) |  |
| D85 | `SMD24PL-TP` | 1 | SOD-123_L2.8-W1.8-LS3.7-RD | [C151787](https://www.lcsc.com/search?q=C151787) |  |
| D86, D87 | `1N5819WS` | 2 | D_SOD-323 | [C369937](https://www.lcsc.com/search?q=C369937) |  |
| J1 | `USB device` | 1 | USB_C_Receptacle_HRO_TYPE-C-31-M-1 | [C165948](https://www.lcsc.com/search?q=C165948) | USB-C receptacle |
| J2 | `Expansion I3C` | 1 | 1X04_1MM_RA_GND | [C7433425](https://www.lcsc.com/search?q=C7433425) | QWIIC / Stemma-QT 4-pin JST-SH (I2C + I3C) |
| J4 | `External Add-On (SAO / PMOD)` | 1 | PinSocket_2x07_P2.54mm_Horizontal | [C2936004](https://www.lcsc.com/search?q=C2936004) | **CATT port** (2×7, 2.54 mm) — PMOD + SAO + JTAG |
| J5 | `USB host` | 1 | USB-A-TH_JTJ-USB-A-F-10.0-010 | [C42576](https://www.lcsc.com/search?q=C42576) | USB-A host receptacle |
| J6 | `CAMERA` | 1 | FPC-SMD_XUNPU_FPC-0.5FX-22PWBH20 | [C3446014](https://www.lcsc.com/search?q=C3446014) | **22-pin MIPI CSI FPC** — Raspberry Pi Zero/5 compatible pinout |
| J7 | `Internal Add-On` | 1 | PinSocket_2x18_P2.54mm_Vertical_SM | [C3975163](https://www.lcsc.com/search?q=C3975163) | **36-pin personality-module header** (2×18, 2.54 mm) |
| J8 | `Micro_SD_Card` | 1 | SD_Card-micro_socket_A | [C7529389](https://www.lcsc.com/search?q=C7529389) | microSD socket, SDIO 2.0/3.0, 3.3 V and 1.8 V |
| J9 | `Speaker` | 1 | Molex_PicoBlade_53261-0271_1x02-1M | [C3029359](https://www.lcsc.com/search?q=C3029359) | Molex PicoBlade 2-pin, 8 Ω speaker |
| J10 | `Headphone` | 1 | PJ-327ST-SMT | [C319103](https://www.lcsc.com/search?q=C319103) | 3.5 mm jack |
| J11 | `Battery` | 1 | CONN-SMD_PH-2AWB | [C20598817](https://www.lcsc.com/search?q=C20598817) | JST PH-2.0 battery connector (Adafruit compatible) |
| L1 | `2.2u` | 1 | Inductor_MSC20FC | [C48945436](https://www.lcsc.com/search?q=C48945436) |  |
| L2 | `YHNR4020-2R2M` | 1 | L_Wurth_WE-LQSH-4020 | [C2926400](https://www.lcsc.com/search?q=C2926400) |  |
| L3, L5 | `6.8uH` | 2 | IND-SMD_L4.0-W4.0 | [C520306](https://www.lcsc.com/search?q=C520306) |  |
| L4 | `CMLW6028S1R5MST` | 1 | IND-SMD_L6.0-W6.0 | [C431354](https://www.lcsc.com/search?q=C431354) |  |
| Q1 | `MMBT2222A` | 1 | SOT-23 | [C8512](https://www.lcsc.com/search?q=C8512) | NPN transistor |
| Q2 | `AO3401A` | 1 | SOT-23 | [C15127](https://www.lcsc.com/search?q=C15127) | P-channel MOSFET |
| Q3, Q4, Q5, Q6 | `AP2302B` | 4 | SOT-23 | [C406812](https://www.lcsc.com/search?q=C406812) | MOSFET ×4 |
| R1, R2 | `5k1` | 2 | 0402 | [C25905](https://www.lcsc.com/search?q=C25905) |  |
| R3, R45 | `1k` | 2 | 0402 | [C11702](https://www.lcsc.com/search?q=C11702) |  |
| R10, R11, R4 | `2k2` | 3 | 0402 | [C25879](https://www.lcsc.com/search?q=C25879) |  |
| R12, R13, R18, R19, R20, R21, R22, R23, R… | `51k` | 16 | 0402 | [C25794](https://www.lcsc.com/search?q=C25794) |  |
| R14, R15, R29, R30, R33, R37, R38, R39, R… | `10k` | 19 | 0402 | [C60490](https://www.lcsc.com/search?q=C60490) |  |
| R16, R24, R34, R35, R47, R52, R56, R58, R… | `100k` | 15 | 0402 | [C25741](https://www.lcsc.com/search?q=C25741) |  |
| R17, R54, R62, R63 | `1M` | 4 | 0402 | [C26083](https://www.lcsc.com/search?q=C26083) |  |
| R25, R26 | `4k02` | 2 | 0402 | [C43251](https://www.lcsc.com/search?q=C43251) |  |
| R27, R28 | `499k` | 2 | 0402 | [C137971](https://www.lcsc.com/search?q=C137971) |  |
| R31, R32, R36, R46, R5, R6, R7, R78, R8, R86 | `4k7` | 10 | 0402 | [C25900](https://www.lcsc.com/search?q=C25900) |  |
| R48 | `261` | 1 | 0402 | [C7467416](https://www.lcsc.com/search?q=C7467416) |  |
| R49 | `6.8k` | 1 | 0402 | [C25917](https://www.lcsc.com/search?q=C25917) |  |
| R53 | `10` | 1 | 0402 | [C25077](https://www.lcsc.com/search?q=C25077) |  |
| R55 | `180k` | 1 | 0402 | [C2909325](https://www.lcsc.com/search?q=C2909325) |  |
| R57 | `4R7` | 1 | 0402 | [C25121](https://www.lcsc.com/search?q=C25121) |  |
| R60 | `1.5k` | 1 | 0402 | [C25867](https://www.lcsc.com/search?q=C25867) |  |
| R64 | `52.3` | 1 | 0402 | [C114978](https://www.lcsc.com/search?q=C114978) |  |
| R72, R73 | `27` | 2 | 0402 | [C25100](https://www.lcsc.com/search?q=C25100) |  |
| R75, R76 | `33` | 2 | 0402 | [C25105](https://www.lcsc.com/search?q=C25105) |  |
| SW1 | `Boot` | 1 | KEY-TH_TC-1101V-C-A-W | [C318992](https://www.lcsc.com/search?q=C318992) | Boot push button |
| SW2 | `User` | 1 | KEY-TH_TC-1101V-C-A-W | [C318992](https://www.lcsc.com/search?q=C318992) | User push button |
| SW3 | `Power` | 1 | KEY-TH_TC-1101V-C-A-W | [C318992](https://www.lcsc.com/search?q=C318992) | Power push button |
| U1, U2 | `ESD` | 2 | Diodes_UDFN-10_1.0x2.5mm_P0.5mm | [C5180236](https://www.lcsc.com/search?q=C5180236) |  |
| U3, U6 | `USBLC6-2P6` | 2 | SOT-666 | [C2827693](https://www.lcsc.com/search?q=C2827693) | USB ESD protection |
| U4 | `TPD4E05U06DQAR` | 1 | USON-10_L2.5-W1.0-P0.50-BL | [C138714](https://www.lcsc.com/search?q=C138714) | 4-channel ESD protection |
| U5 | `CH334R` | 1 | QSOP-16_3.9x4.9mm_P0.635mm | [C4154405](https://www.lcsc.com/search?q=C4154405) | **USB 2.0 hub** — splits USB-C to P4, C6 and the internal add-on port |
| U7 | `ESP32-P4` | 1 | QFN-104_EP_10x10_Pitch0.35mm-ESP32 | [C22387510](https://www.lcsc.com/search?q=C22387510) | **Application processor** — dual-core RISC-V, 32 MB in-package PSRAM |
| U8 | `TXB0104RGY` | 1 | Texas_S-PVQFN-N14 | [C400708](https://www.lcsc.com/search?q=C400708) | **Level shifter** — VSDCARD domain to 3.3 V for expansion pins E3–E6 |
| U9 | `W25Q128JVS` | 1 | SOIC-8_5.23x5.23mm_P1.27mm | [C97521](https://www.lcsc.com/search?q=C97521) | **16 MB QSPI flash** for the ESP32-P4 |
| U10 | `TLV62569DBV` | 1 | SOT-23-5 | [C141836](https://www.lcsc.com/search?q=C141836) | Step-down converter |
| U11 | `74LVC2G02HD4-7` | 1 | X2-DFN2010-8_L2.0-W1.0-P0.50-BL | [C842640](https://www.lcsc.com/search?q=C842640) | Dual NOR gate — part of the power latch circuit |
| U12 | `CH32V203C8T6` | 1 | LQFP-48_7x7mm_P0.5mm | [C3001172](https://www.lcsc.com/search?q=C3001172) | **Management coprocessor** — keyboard, RTC, power, backlight, LEDs. I2C 0x5F |
| U14 | `SY6280AAC` | 1 | SOT-23-5 | [C55136](https://www.lcsc.com/search?q=C55136) | **USB-A host port power switch** — 1 A limit, short-circuit protection |
| U15 | `BQ25895RTW` | 1 | Texas_S-PWQFN-N24_EP2.7x2.7mm_Ther | [C80200](https://www.lcsc.com/search?q=C80200) | **PMIC** — battery charger, monitoring, 5 V boost. I2C 0x6A on the coprocessor bus |
| U16, U18 | `AP3032KTR` | 2 | SOT-23-6 | [C264086](https://www.lcsc.com/search?q=C264086) | Backlight LED driver ×2 — one display, one keyboard. PWM from coprocessor |
| U17 | `TPS63020DSJR` | 1 | VSON-14_L4.0-W3.0-P0.50-BL-EP_TI_D | [C15483](https://www.lcsc.com/search?q=C15483) | **3.3 V buck-boost** — holds 3.3 V as the cell sags below 3.3 V |
| U19 | `LR8341A-M25` | 1 | SOT-89-3 | [C5205210](https://www.lcsc.com/search?q=C5205210) | **Standby LDO** — 2.5 V to the coprocessor Vbatt rail while the device is off |
| U20 | `ESP32-C6-WROOM-1` | 1 | ESP32-C6-WROOM-1 | [C5366877](https://www.lcsc.com/search?q=C5366877) | **Radio module** — Wi-Fi 6, BLE 5.3, 802.15.4 (Thread/Zigbee), 8 MB flash |
| U21 | `IR968-8P(X1-X4)XBY` | 1 | LED-TH_L3.0-W2.9-P2.54-FD | [C17179483](https://www.lcsc.com/search?q=C17179483) |  |
| U22 | `74LVC1GU04` | 1 | SOT-353_SC-70-5 | [C485082](https://www.lcsc.com/search?q=C485082) | Unbuffered inverter |
| U23 | `E22-900M22S` | 1 | WIRELM-SMD_E22-900M22S | [C411293](https://www.lcsc.com/search?q=C411293) | **LoRa module** (868/915 MHz, 22 dBm). E22-400M22S fitted on 433 MHz units |
| U24 | `ES8156` | 1 | VQFN-20-1EP_3x3mm_P0.4mm_EP1.7x1.7 | [C2887138](https://www.lcsc.com/search?q=C2887138) | **Stereo audio DAC / codec**, hardware volume. I2C 0x08 |
| U25 | `FM8002A` | 1 | SSOP-8_3.9x5.05mm_P1.27mm | [C94625](https://www.lcsc.com/search?q=C94625) | **Mono speaker amplifier** — switchable by the coprocessor |
| U26 | `74LVC1G17GW,125` | 1 | SOT-353_SC-70-5 | [C426705](https://www.lcsc.com/search?q=C426705) | Schmitt-trigger buffer |
| U27, U28, U29, U30, U31, U32 | `SK6805` | 6 | SK6805-EC20 | [C2890036](https://www.lcsc.com/search?q=C2890036) | Addressable RGB LEDs ×6, driven by the coprocessor |
| U33 | `BMI270` | 1 | LGA-14_L3.0-W2.5-P0.50-BR | [C2836813](https://www.lcsc.com/search?q=C2836813) | **IMU** — accelerometer + gyroscope. I2C 0x68 |
| Y1 | `12MHz` | 1 | Crystal_SMD_2520-4Pin_2.5x2.0mm | [C284156](https://www.lcsc.com/search?q=C284156) | Crystal — CH32V203 coprocessor |
| Y2 | `40MHz` | 1 | Crystal_SMD_3225-4Pin_3.2x2.5mm | [C2901712](https://www.lcsc.com/search?q=C2901712) | Crystal — ESP32-P4 |
| Y3 | `32.768KHz` | 1 | Crystal_SMD_3215-2Pin_3.2x1.5mm | [C95361](https://www.lcsc.com/search?q=C95361) | **Watch crystal** — coprocessor RTC, runs while device is off |

## Related production files

| File | Contents |
|---|---|
| [`artifacts/production/bom.csv`](artifacts/production/bom.csv) | This table, raw |
| [`artifacts/production/designators.csv`](artifacts/production/designators.csv) | Designator ↔ part mapping |
| [`artifacts/production/positions.csv`](artifacts/production/positions.csv) | Pick-and-place centroids |
| [`artifacts/production/netlist.ipc`](artifacts/production/netlist.ipc) | IPC-D-356 netlist — machine-readable connectivity for bare-board electrical test |
| `production/tanmatsu.zip` *(archive only)* | **Complete Gerber + drill set** — see below |
| [`artifacts/schematics/kicad/`](artifacts/schematics/kicad/) | KiCad schematics (`tanmatsu`, `esp32p4`, `audio`, `sensors`, `keyboard_matrix`) and the PCB |
| [`artifacts/schematics/tanmatsu-schematic.pdf`](artifacts/schematics/tanmatsu-schematic.pdf) | Rendered schematic |

The `netlist.ipc` file is worth knowing about: it is a full connectivity list in IPC-D-356 format, so you can recover net membership without parsing KiCad at all. It is what [`tools/parse_ipc_netlist.py`](tools/parse_ipc_netlist.py) uses to verify pinouts against actual copper.

### The Gerber set (`production/tanmatsu.zip`)

Inspected 2026-08-24 — a **complete, valid manufacturing package**, not a placeholder:

| Layer | File | Size |
|---|---|---:|
| Front copper | `tanmatsu-F_Cu.gtl` | 1.36 MB |
| **Inner 1** | `tanmatsu-In1_Cu.g1` | 1.07 MB |
| **Inner 2** | `tanmatsu-In2_Cu.g2` | 587 KB |
| Back copper | `tanmatsu-B_Cu.gbl` | 2.14 MB |
| Solder mask | `F_Mask.gts`, `B_Mask.gbs` | 46 / 52 KB |
| Silkscreen | `F_Silkscreen.gto`, `B_Silkscreen.gbo` | 78 KB / 894 KB |
| Paste | `F_Paste.gtp`, `B_Paste.gbp` | 5 / 47 KB |
| Outline | `Edge_Cuts.gm1` | 30 KB |
| Drill | `PTH.drl`, `NPTH.drl` + map files | |

Two things worth noting:

- **The four copper layers independently confirm the 4-layer stackup** (`F_Cu`, `In1_Cu`, `In2_Cu`, `B_Cu`) stated in [`README.md`](README.md).
- **The Gerbers are dated `2026-02-07`**, eighteen days before the repository's last commit (`640805dd`, 2026-02-25). So the published manufacturing data slightly predates the final commit — check both if you intend to fabricate.

The ZIP is not vendored (it is regenerable from the KiCad source); it lives in the archive at
`archive/scratch/tanmatsu/sources/tanmatsu-hardware/production/tanmatsu.zip`.

## Component records

Chips documented separately under `components/`:
[ESP32-P4](../../../components/espressif/esp32-p4/README.md) · ESP32-C6-WROOM-1 · CH32V203C8T6 · W25Q128JVS · BQ25895 · TPS63020 · ES8156 · FM8002A · BMI270 · E22-900M22S · CH334R · SK6805 · ST7701S / LH397K-IC01

## Related

- [`README.md`](README.md) — overview and architecture
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — connector pinouts
- [`sources.md`](sources.md) — repository provenance
