# Tanmatsu — pinouts and buses

> Consolidated wiring reference. Snapshot **2026-08-24**.
> Primary sources: the vendor's Sphinx documentation source (`tanmatsu-documentation` @ `bd3ded51`) and the KiCad design (`tanmatsu-hardware` @ `640805dd`, CERN-OHL-P).
> **No hardware was available**; nothing here has been verified with a meter.

All GPIO numbers below are **ESP32-P4** GPIOs unless stated otherwise.

---

## 1. I2C / I3C bus map

Tanmatsu has **four** distinct two-wire buses. Confusing them is the most likely early mistake.

### 1.1 Internal I2C — GPIO9 (SDA) / GPIO10 (SCL)

The board's own peripherals live here. The ESP32-P4 is the controller.

| Address | Device | Role |
|---|---|---|
| **0x5F** | **CH32V203 coprocessor** | keyboard, power management, RTC, backlight, LEDs |
| **0x08** | **ES8156** audio codec | stereo DAC, hardware volume |
| **0x68** | **BMI270** IMU | accelerometer + gyroscope |
| **0x50** | Add-on identification EEPROM | *optional*, lives on an attached add-on board |
| **0x62** | **SCD4x** CO₂/temp/humidity | *optional*, user-soldered sensor header |

The ESP32-C6's I2C connection to this bus exists in hardware but is **not currently used** by any firmware.

### 1.2 Power-management I2C — CH32V203 ↔ BQ25895

A **separate** bus, not reachable from the ESP32-P4. The coprocessor is the controller.

| Address | Device |
|---|---|
| **0x6A** | BQ25895 PMIC |

To change charging behaviour you must go **through the coprocessor's register interface**, not talk to the PMIC directly.

### 1.3 QWIIC / Stemma-QT — GPIO33 (SDA) / GPIO32 (SCL)

Brought out to a 4-pin JST-SH connector. Wired to the ESP32-P4's **I3C** peripheral, so it can operate as I2C controller, I2C peripheral, **or I3C controller**. Nothing else is attached to these pins, so they are free for any use.

### 1.4 CATT port I2C — GPIO12 (SDA) / GPIO13 (SCL)

Two of the eight CATT GPIOs default to I2C at startup. The launcher probes address **0x50** here to identify an attached add-on. Expect brief bus activity during boot.

---

## 2. Internal add-on port ("personality module") — 36-pin 2.54 mm

Rear-facing, 2×18 pin socket (`J7`, LCSC `C3975163`). Requires a modified back cover to access. This is the main expansion interface.

| Pin | Name | GPIO | Function | Notes |
|---:|---|---:|---|---|
| 1 | `VOTG` | — | Power out | 5 V when PMIC booster enabled, else ≈VSYS |
| 2 | `HUB_USB1_P` | — | USB D+ | Hub port shared with USB-C — lets an add-on present a USB device to the host PC |
| 3 | `VBATT` | — | Power out | Battery 3.0–4.2 V, **always on, even when device is off** |
| 4 | `HUB_USB1_N` | — | USB D− | |
| 5 | `VSYS` | — | Power out | System rail 3.0–5.0 V, off when device off |
| 6, 7 | `GND` | — | Ground | |
| 8 | `+3.3V` | — | Power out | Main logic rail |
| 9 | `INT_SCL` | **10** | I2C | Internal bus — shared with coprocessor/codec/IMU |
| 10 | `INT_SDA` | **9** | I2C | Internal bus |
| 11 | `E0` | **36** | GPIO | **free** |
| 12 | `E1` | **0** | GPIO | **free** |
| 13 | `E2` | **6** | GPIO | ⚠ shared with camera GPIO 1 |
| 14 | `E3` | **46** | GPIO | ⚠ needs VSDCARD LDO enabled; level-shifted to 3.3 V |
| 15 | `E4` | **47** | GPIO | ⚠ as E3 |
| 16 | `E5` | **48** | GPIO | ⚠ as E3 |
| 17 | `E6` | **45** | GPIO | ⚠ as E3 |
| 18 | `E7` | **7** | GPIO | **free**; in P4 low-power domain, 51 kΩ pull-up — **usable as deep-sleep wake pin** |
| 19 | `E8` | **54** | GPIO | **free** |
| 20 | `E9` | **49** | GPIO | **free** |
| 21 | `E10` | **53** | GPIO | **free** |
| 22 | `EXT_USB_P` | **26** | GPIO / USB FS D+ | P4 USB PHY 2 |
| 23 | `E11` | **52** | GPIO | **free** |
| 24 | `EXT_USB_N` | **27** | GPIO / USB FS D− | P4 USB PHY 2 |
| 25 | `E12` | **51** | GPIO | **free** |
| 26 | `P4_TX` | **37** | GPIO / UART TX | ⚠ **must be LOW during boot** |
| 27 | `E13` | **50** | GPIO | **free** |
| 28 | `P4_RX` | **38** | GPIO / UART RX | ⚠ **must be HIGH during boot** |
| 29 | `I2S_MCLK` | **30** | I2S | ⚠ shared with audio codec |
| 30 | `I2S_LRCK` | **31** | I2S | ⚠ shared with audio codec |
| 31 | `I2S_DATA` | **28** | I2S | ⚠ shared with audio codec |
| 32 | `I2S_SCLK` | **29** | I2S | ⚠ shared with audio codec |
| 33 | `+3.3V` | — | Power out | |
| 34 | `I3C_SDA` | **33** | I3C/I2C | ⚠ shared with QWIIC connector |
| 35 | `GND` | — | Ground | |
| 36 | `I3C_SCL` | **32** | I3C/I2C | ⚠ shared with QWIIC connector |

### 2.1 Which pins are actually safe

The vendor's own tiering, worth following exactly:

- **Unrestricted:** `E0, E1, E7, E8, E9, E10, E11, E12, E13`
- **Available only if ESP32-P4 internal LDO 4 is enabled** (this rail also powers the SD card slot): `E3, E4, E5, E6`. A level shifter on the mainboard keeps them at 3.3 V externally whether the SD card is running at 3.3 V or 1.8 V.
- **Usable but noisy at startup / while the launcher runs:** `EXT_USB_P, EXT_USB_N, P4_TX, P4_RX`
- **Shared — using these breaks something else:** `E2` (camera), `I2S_*` (on-board audio), `I3C_*` (QWIIC port)

### 2.2 Hard electrical limits

- **≤ 1 A total** across all 3.3 V outputs — "generally advised to stay well below this figure"
- **≤ 1.5 A** drawn from the battery when connected to the internal battery connector
- **Do not charge the battery via the internal add-on port**

`P4_TX` and `P4_RX` are the ESP32-P4 boot console. Their required boot levels (TX low, RX high) are a real trap: an add-on that pulls `P4_RX` low, or drives `P4_TX` high, at power-on can prevent the device booting.

---

## 2c. ⚠ VERIFIED FROM COPPER: `E8` and `E10` are NOT free GPIO

**This contradicts both vendors' documentation and matters if you are designing an add-on board.**

Nicolai Electronics and badge.team both state that these expansion pins can be used
"**without limitations**":

> `E0, E1, E7, E8, E9, E10, E11, E12 and E13`

Parsing the **IPC-D-356 fabrication netlist** ([`artifacts/production/netlist.ipc`](artifacts/production/netlist.ipc) —
exported from the actual PCB for bare-board electrical test) with
[`tools/parse_ipc_netlist.py`](tools/parse_ipc_netlist.py) shows that is **not true for two of them**:

| Net | J7 pin | ESP32-P4 | Third connection | Consequence |
|---|---:|---|---|---|
| **`E8`** | 19 | U7.98 = **GPIO54** | **`R4` (2.2 kΩ) → `/RADIO/TX` → U20.25** | Carries the **ESP32-C6 UART TX** |
| **`E10`** | 21 | U7.97 = **GPIO53** | **U20.24 directly** | Carries the **ESP32-C6 UART RX** |
| `E0` | 11 | U7.68 = **GPIO36** | **`R5` (4.7 kΩ) pull-up to +3.3 V** | Undocumented pull-up |
| `E7` | 18 | U7.7 = GPIO7 | `R12` (51 kΩ) pull-up | ✅ documented |
| `E2` | 13 | U7.6 = GPIO6 | `J6.5` (camera) | ✅ documented |
| `E3`–`E6` | 14–17 | *via `U8` TXB0104* | level shifter, VSDCARD domain | ✅ documented |
| `E1`, `E9`, `E11`, `E12`, `E13` | — | GPIO0, 49, 52, 51, 50 | none | ✅ genuinely free |

Corroboration: badge.team's own [ESP32-C6 pinout page](https://badge.team/docs/badges/konsool/hardware/pinout/ics/esp32c6/)
independently lists C6 module **pin 24 = `RXD0`, "UART to P4 Receive"** and **pin 25 = `TXD0`,
"UART to P4 Transmit"** — the same pins the netlist puts on `E10` and (through `R4`) `E8`. So both
facts are true; the "no limitations" list simply never reconciled them.

**Practical guidance:**

- **Do not drive `E8` or `E10`** from an add-on board unless you are certain no ESP32-C6 console
  traffic is expected. Driving `E10` fights the C6's TX driver; `E8` is protected by the 2.2 kΩ
  series resistor, but you will still corrupt the radio's serial console.
- Treat `E8`/`E10` as **reserved**. The genuinely unrestricted pins are **`E1`, `E9`, `E11`, `E12`, `E13`**
  (GPIO0, 49, 52, 51, 50), plus `E0` (GPIO36) if you can tolerate its 4.7 kΩ pull-up.
- `E0`'s pull-up means it **idles high** — do not use it for an active-high enable that must default off.

Reproduce this yourself:

```bash
python3 tools/parse_ipc_netlist.py artifacts/production/netlist.ipc --net E10
#   J7.21
#   U20.24
#   U7.97
```

## 2d. The E-numbering conflict, settled

[`gaps-and-conflicts.md` §14](gaps-and-conflicts.md) recorded that badge.team's ESP32-P4 IC page and
its own back-expansion page disagree about which GPIO carries which `E` pin. That is now resolved
from fabrication data by [`tools/verify_expansion_pinout.py`](tools/verify_expansion_pinout.py),
which cross-references the netlist against the ESP32-P4 datasheet pin table
([`tools/p4_pinmap.py`](tools/p4_pinmap.py), transcribed from Table 2-1):

```
net    U7 pin  actual   connector  IC page   verdict
E0         68  GPIO36   36         None      A=ok
E1        104  GPIO0    0          6         A=ok B=MISMATCH
E2          6  GPIO6    6          0         A=ok B=MISMATCH
E7          7  GPIO7    7          49        A=ok B=MISMATCH
E8         98  GPIO54   54         50        A=ok B=MISMATCH
E9         92  GPIO49   49         51        A=ok B=MISMATCH
E10        97  GPIO53   53         52        A=ok B=MISMATCH
E11        95  GPIO52   52         53        A=ok B=MISMATCH
E12        94  GPIO51   51         54        A=ok B=MISMATCH
E13        93  GPIO50   50         None      A=ok
--------------------------------------------------------
connector page : 10 correct, 0 wrong
IC page        :  0 correct, 8 wrong
```

**Use the connector pinout. The badge.team ESP32-P4 IC page's `E`-labels are wrong** (its other
content — SWD pins, SDIO, LDO allocation, TE pin — is correct and unavailable elsewhere).

## 2e. Undocumented test points and headers

Also visible in the fabrication netlist and absent from all vendor documentation:

| Ref | Net | Use |
|---|---|---|
| `TP18` | `I2S_MCLK` | I2S master clock probe |
| `TP19` | `I2S_SCLK` | I2S sample clock probe |
| `TP20` | `I2S_LRCK` | I2S word clock probe |
| `TP21` | `I2S_DATA` | I2S data probe |
| `TP8` | `VBATT` | battery rail probe |
| `TP1` | `/UNUSED_USB_N` | unused USB pair |
| `J13`, `J14`, `J15`, `J16` | `+3.3V`, `INT_SDA`, `INT_SCL`, GND | **the unpopulated sensor header** (SCD4x CO₂ etc.) |
| `J3` | `SAO_*` | a **6-pin SAO header footprint** present on the PCB but **absent from the BOM** — a DNP position |

The four I2S test points make audio bring-up on this board far easier than the documentation
suggests. `J3` being in the netlist but not the BOM is worth flagging to anyone diffing the two.

---

## 3. External add-on port — "CATT" (Connect All The Things)

Side-facing 2×7 pin socket (`J4`, LCSC `C2936004`). Simultaneously **PMOD**, **SAO** and **JTAG** compatible — one connector, three standards.

| Pin | CATT | PMOD | SAO | JTAG | **P4 GPIO** |
|---:|---|---|---|---|---:|
| 1 | +3.3 V out | — | +3.3 V | +3.3 V | — |
| 2 | GND | — | GND | GND | — |
| 3 | I2C SDA | "7": D4 | I2C SDA | — | **12** |
| 4 | I2C SCL | "1": D0 | I2C SCL | — | **13** |
| 5 | IO 1 | "8": D5 | IO 1 | — (LED on adapter) | **15** |
| 6 | IO 2 | "2": D1 | IO 2 | **DETECT** | **34** |
| 7 | IO 3 | "9": D6 | — | **MTMS** | **4** |
| 8 | IO 4 | "3": D5 | — | **MTDO** | **5** |
| 9 | IO 5 | "10": D7 | — | **MTCK** | **2** |
| 10 | IO 6 | "4": D3 | — | **MTDI** | **3** |
| 11 | GND | GND | — | GND | — |
| 12 | GND | GND | — | GND | — |
| 13 | P4 reset | "+3.3 V" | — | P4 reset | — |
| 14 | +3.3 V out | +3.3 V out | — | +3.3 V | — |

### 3.1 JTAG switching behaviour

- Pulling **pin 6 (`DETECT`, GPIO34) low** switches the JTAG interface from the internal USB-serial/JTAG peripheral over to the CATT pins. The pin has a pull-up, so an unconnected port leaves JTAG on USB.
- **Software can override this** by configuring the JTAG pins as GPIO — the debugger will then disconnect.
- **If an add-on holds GPIO34 low, USB-C JTAG stops working** until you set the JTAG source manually in software. This is an easy-to-miss interaction between an unrelated add-on and your debugger.
- **`JP1`** can be shorted to tie pin 13 to +3.3 V, **disabling the reset signal** on the CATT port. Pin 13 can otherwise be safely ignored or tied to 3.3 V.
- Nicolai Electronics sells a JTAG adapter that adds an LED and a QWIIC port beside a standard 10-pin JTAG header.

Pinout sheet as supplied by the vendor: [`artifacts/source-snapshots/tanmatsu-documentation/hardware/connectors/external-add-on-port/catt.pdf`](artifacts/source-snapshots/tanmatsu-documentation/hardware/connectors/external-add-on-port/catt.pdf)

---

## 4. Display connector

Board-to-board connector `CN1` — **Hirose DF37NB-24DS-0.4V(51)**, 24-pin, hidden under the front panel. The display is factory-fitted.

| Signal group | Detail |
|---|---|
| MIPI DSI | **three differential pairs** — two data lanes + one clock |
| Logic power | 3.3 V |
| Backlight | ~**24 V @ 20 mA** rail, driven by an AP3032 |

Backlight brightness is **not** a P4 PWM output — the current is set by the **coprocessor's** PWM, so you change it by writing the display-backlight-brightness register at coprocessor I2C address 0x5F.

Panel: **SWI LH397K-IC01**, 3.97", 480×800, ST7701S controller. Espressif component for the DSI setup: [`nicolaielectronics/mipi_dsi_abstraction`](https://components.espressif.com/components/nicolaielectronics/mipi_dsi_abstraction) — notable because it also supports the official ESP32-P4 dev-kit display, so code ports between them.

---

## 5. Camera connector

`J6` — 22-pin 0.5 mm FPC (XUNPU `FPC-0.5FX-22PWBH20`), **pinout-compatible with the Raspberry Pi Zero and Pi 5** camera connector.

| Signal group | Detail |
|---|---|
| MIPI CSI | three differential pairs — two data + one clock |
| Power | 3.3 V |
| Enable | ⚠ **shared with the ESP32-C6 radio module enable** |
| LED control | ⚠ shared with internal expansion pin `E2` (GPIO6) |

Two sharing hazards in one connector. The enable line being common with the radio module means camera power and radio power are not independent.

**Software support is narrower than the connector suggests** — the vendor states it is "limited to a subset of Raspberry Pi compatible camera module sensor chips such as OV5647". Physical fit does not imply a working driver.

---

## 6. USB topology

A **CH334R** 4-port hub (`U5`) sits behind the USB-C connector and splits it three ways:

```
USB-C (J1) ──► CH334R hub ─┬─► ESP32-P4 USB PHY 1  (default: USB-serial/JTAG)
                           ├─► ESP32-C6 USB-serial/JTAG
                           └─► internal add-on port pins 2/4
```

**Downstream port numbering** [SCH, from the `tanmatsu.kicad_pcb` netlist + CH334R datasheet pin names; corrected 2026-08-30]. The set of three consumers above is right, but the port *numbers* previously recorded here were not:

| Physical port | Hub pins | Connected to |
|---|---|---|
| **Port 1** (`DM1`/`DP1`) | 7, 8 | **Internal add-on port** |
| **Port 2** (`DM2`/`DP2`) | 5, 6 | **Unused** — test points (`TP1`) only |
| **Port 3** (`DM3`/`DP3`) | 3, 4 | **ESP32-P4** |
| **Port 4** (`DM4`/`DP4`) | 1, 2 | **ESP32-C6** |

The USB-C connector is the hub's **upstream** port, not a downstream one. This matters for per-port power control, per-port status reads, and for interpreting hub topology in `lsusb -t`. Full derivation: [CH334R §4.1](../../../components/wch/ch334r/README.md#41--the-port-numbering-in-the-device-record-is-wrong).

- The **ESP32-P4's PHY 1 defaults to USB-serial/JTAG** but firmware can swap it for a custom USB device — this is how **BadgeLink** (WebUSB app/file management) works.
- Because the ROM exposes USB-serial/JTAG unconditionally, **you can always flash the P4 even with no valid firmware installed**.
- **Bootloader entry:** hold the third button on the right side (`-`, "down") while powering on. Practical recipe: hold the power button until the device turns off, then hold `-` while plugging in USB. The screen stays black — that is expected.

**USB-A host port** (`J5`): 480 Mbit USB 2.0, 5 V limited to **1 A** with short-circuit protection, switched by `SY6280AAC` (`U14`).

> ⚠ **The USB-A enable signal is shared with the ESP32-C6 boot-mode pin.** Enabling the radio briefly force-powers the USB-A port on; putting the radio into bootloader mode briefly force-powers it off. If you have a device plugged into USB-A, reflashing the radio will glitch its power.

---

## 7. Buttons

| Ref | Function |
|---|---|
| `SW3` | **Power** |
| `SW1` | Boot |
| `SW2` | User |

Externally the case exposes **Power, up (`+`) and down (`-`)**. Holding `-` at power-on forces ESP32-P4 USB download mode.

---

## 8. Storage

microSD socket `J8`, SDIO. Supports **SDIO 2.0 and 3.0** cards at both **3.3 V and 1.8 V** signalling — 1.8 V is what enables the higher-speed modes. The SD card power domain (`VSDCARD`, ESP32-P4 internal LDO 4) also gates expansion pins `E3`–`E6`.

---

## 8a. Storage and radio are BOTH 4-bit SDIO

The prose documentation describes the SD card slot loosely. The BSP is precise, and the answer is
better than the prose implies — **both** the microSD card and the ESP32-C6 radio are on **4-bit SDIO**
buses, not SPI:

| Bus | Width | ESP32-P4 GPIOs |
|---|---|---|
| **microSD card** (`BSP_SDCARD_*`, `WIDTH 4`) | **4-bit SDIO 3.0** | CLK **43**, CMD **44**, D0–D3 **39, 40, 41, 42** |
| **ESP32-C6 radio** (`BSP_SDIO_*`, `WIDTH 4`) | **4-bit SDIO 2.0** | CLK **17**, CMD **16**, D0–D3 **18, 19, 20, 21** |

This is the transport `esp-hosted` uses to carry Wi-Fi and BLE traffic between the P4 and the C6 —
a 4-bit SDIO link, not UART or SPI, which is why throughput is respectable. The C6 also raises an
interrupt on **GPIO8**.

Source: `targets/tanmatsu/tanmatsu_hardware.h` (BSP `9037f0e`, MIT) and
[badge.team ESP32-P4 pinout](https://badge.team/docs/badges/konsool/hardware/pinout/ics/esp32p4/).

## 8b. ESP32-P4 internal LDO allocation

The ESP32-P4 has four internal LDOs. On this board:

| LDO | Net | Powers |
|---|---|---|
| `VO1` | `VFLASH` | SPI flash |
| `VO2` | `VPSRAM` | PSRAM |
| **`VO3`** | `VMIPI` | **MIPI DSI PHY** — 2.5 V, `BSP_DSI_LDO_CHAN 3` |
| **`VO4`** | `VSDCARD` | **SD card domain + expansion pins `E3`–`E6`** |

This is why the internal add-on port documentation says `E3`–`E6` require "the VSDCARD LDO enabled":
those pins live in the `VO4` power domain and are dead until software brings that LDO up.

## 8c. Other fixed GPIO assignments

From the BSP and badge.team's P4 pinout, not otherwise documented:

| GPIO | Function |
|---:|---|
| **1** | Interrupt input from the CH32V203 coprocessor (**high** on interrupt) |
| **8** | Interrupt input from the ESP32-C6 radio (ESP-HOSTED) |
| **11** | LCD TE (tearing effect) |
| **14** | LCD reset |
| **22** | **CH32V203 SWDIO** — coprocessor programming |
| **23** | **CH32V203 SWCLK** — coprocessor programming |
| **24 / 25** | USB DN / DP → **CH334R downstream port 3** (`DM3`/`DP3`, hub pins 3/4). ⚠ Corrected 2026-08-30 — previously recorded as "hub port 1 (the USB-C port)"; the USB-C connector is the hub's *upstream* port, and the P4 sits on downstream port 3. See [CH334R §4.1](../../../components/wch/ch334r/README.md#41--the-port-numbering-in-the-device-record-is-wrong) |
| **35** | **Volume-down button**; also a boot strap (`1` at reset release = SPI boot, `0` = DEBUG) |
| **36** | Expansion `E0`; *"depending on fuses can influence boot"* |

GPIO22/23 are the **RVSWD path** that lets the ESP32-P4 reflash the coprocessor — see
[`development.md` §7](development.md#7-reflashing-the-coprocessor-from-the-esp32-p4).

⚠ **GPIO35 and GPIO36 both interact with boot.** GPIO35 is additionally wired to the volume-down
button, which is why holding volume-down at power-on is meaningful to the ROM.

---

## 9. Crystals

| Ref | Frequency | Serves |
|---|---|---|
| `Y2` | 40 MHz | ESP32-P4 |
| `Y1` | 12 MHz | CH32V203 coprocessor |
| `Y3` | **32.768 kHz** | Coprocessor RTC — keeps time while the device is off |

---

## Related

- [`README.md`](README.md) — device overview and architecture
- [`bom.md`](bom.md) — every reference designator
- [`development.md`](development.md) — flashing, flash layout, toolchain
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — unresolved items
- Primary KiCad sources: [`artifacts/schematics/kicad/`](artifacts/schematics/kicad/) · rendered [`schematic.pdf`](artifacts/schematics/tanmatsu-schematic.pdf)
