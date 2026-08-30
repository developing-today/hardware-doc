# Tanmatsu — feature coverage map

> Every advertised or fitted capability, mapped to hardware, evidence, documentation and remaining gap.
> **2026-08-24.** Evidence classes: **P** = primary vendor design/firmware · **D** = vendor documentation · **B** = BSP source · **N** = none found.
> **No feature was tested on hardware.** "Documented" means documented *here*, not verified.

## Core compute and memory

| Feature | Hardware | Evidence | Documented in | Gap |
|---|---|---|---|---|
| ESP32-P4 application processor | `U7` | P, D, B | [README](README.md), [pinouts](pinouts-and-buses.md) | **Clock 360 vs 400 MHz disputed** |
| 32 MB PSRAM | in-package | D | [README](README.md), [display](display.md) | Must run at 200 MHz — see display §4.1 |
| 16 MB flash | `U9` W25Q128JVS | P, D | [bom](bom.md), [development](development.md) | — |
| AI instruction extensions | ESP32-P4 | D (badge.team only) | [konsool-and-family](konsool-and-family.md) | **Unexplored** — no example uses them |
| Flash partitioning | — | D | [development](development.md) | — |

## Human interface

| Feature | Hardware | Evidence | Documented in | Gap |
|---|---|---|---|---|
| 69-key QWERTY keyboard | KeebDeck keypad + 72 diodes | P, D, B | [keyboard](keyboard.md) | Vendor never names the part |
| Keyboard matrix scan | CH32V203 9×8 | **P (firmware)** | [keyboard §1.3–1.5](keyboard.md) | — |
| Full keymap | — | P | [keyboard §1.5](keyboard.md) | — |
| AltGr layer | — | D | [keyboard §1.7](keyboard.md) | Depends on app font coverage |
| 6 coloured function keys | — | P, D | [keyboard §1.6](keyboard.md) | — |
| Keyboard backlight | 8× LTW-010DCG | P, D | [keyboard §1.9](keyboard.md) | Dimming curve unknown |
| Volume up | matrix row 8 bit 7 | P | [keyboard §1.5](keyboard.md) | — |
| Volume down | **GPIO35 button** | B, D | [keyboard §1.5](keyboard.md) | **Resolved** — not a matrix key |
| Power / up / down buttons | `SW1`–`SW3` | P, D | [pinouts §7](pinouts-and-buses.md) | — |
| 3.97" 480×800 MIPI DSI display | `CN1`, ST7701S | P, D, B | [display](display.md) | **RGB888 support disputed** |
| Display backlight | AP3032 + coprocessor PWM | P, D | [display §2.1](display.md) | Curve/frequency unknown |
| Tearing-effect sync | GPIO11 | B, D | [display §2a](display.md) | **Undocumented by vendor**; unused by known software |
| 6 addressable LEDs | SK6805 ×6 | P, D, B | [component](../../../components/normand/sk6805-ec20/README.md) | — |
| Touchscreen | — | — | — | **Not present** |

## Connectivity

| Feature | Hardware | Evidence | Documented in | Gap |
|---|---|---|---|---|
| Wi-Fi 6 (2.4 GHz) | ESP32-C6 | D, B | [component](../../../components/espressif/esp32-c6-wroom-1/README.md) | **Throughput unmeasured** |
| BLE 5.3 | ESP32-C6 | D | idem | Untested |
| Thread / Zigbee 802.15.4 | ESP32-C6 | D | idem | **No known software uses it** |
| P4↔C6 transport | 4-bit SDIO 2.0 | **B** | [pinouts §8a](pinouts-and-buses.md) | **Not in vendor prose** |
| LoRa | E22-900M22S | D | [component](../../../components/ebyte/e22-900m22s/README.md) | **Range unmeasured**; 433 MHz variant unavailable |
| Meshtastic / MeshCore | — | D | [software-and-apps](software-and-apps.md) | Meshtastic fork is WIP |
| USB-C device | CH334R hub | P, D | [pinouts §6](pinouts-and-buses.md) | — |
| USB-A host, 1 A | `J5`, SY6280AAC | P, D | [pinouts §6](pinouts-and-buses.md) | ⚠ enable shared with C6 boot pin |
| Qwiic / Stemma-QT I2C+I3C | GPIO32/33 | D | [pinouts §1.3](pinouts-and-buses.md) | **I3C mode untested** |

## Expansion

| Feature | Hardware | Evidence | Documented in | Gap |
|---|---|---|---|---|
| Internal 36-pin add-on port | `J7` | D | [pinouts §2](pinouts-and-buses.md) | ⚠ **E-numbering conflict** in badge.team's own pages |
| CATT port (PMOD+SAO+JTAG) | `J4` | D, B | [pinouts §3](pinouts-and-buses.md) | — |
| JTAG debugging | via CATT or USB | D | [pinouts §3.1](pinouts-and-buses.md) | Untested |
| Add-on identification EEPROM | 0x50 | D | [pinouts §1.4](pinouts-and-buses.md) | **Format undefined by vendor** |
| Konsool expansion boards | — | **P** | [expansion-boards](expansion-boards.md) | **All cloned & inspected.** `konsool-zero` is WIP; `expansion-template` is an empty repo |
| Front panels | decorative PCB | **P** | [expansion-boards](expansion-boards.md) | 4 mounting holes, no components. 0.8 mm / ENIG / Remove Mark |

## Storage and media

| Feature | Hardware | Evidence | Documented in | Gap |
|---|---|---|---|---|
| microSD, 4-bit SDIO 3.0 | `J8` | **B**, D | [pinouts §8a](pinouts-and-buses.md) | Throughput unmeasured |
| 1.8 V / 3.3 V SD signalling | VSDCARD LDO | D, B | [pinouts §8b](pinouts-and-buses.md) | — |
| MIPI CSI camera | `J6`, 22-pin | D | [pinouts §5](pinouts-and-buses.md) | — |
| **Supported camera sensors** | — | D (badge.team) | [konsool-and-family](konsool-and-family.md) | **Resolved** — 7 sensors listed |
| **H.264 hardware encoding** | ESP32-P4 | D (badge.team only) | [display §2c](display.md) | **Unverified; no example app** |
| Audio out — headphone + speaker | ES8156 + FM8002A | P, D, B | [component](../../../components/everest-semiconductor/es8156/README.md) | Untested |
| Headphone detect | coprocessor `PB5` | P | [keyboard §1.10](keyboard.md) | — |
| Audio input | — | — | — | **No microphone fitted** |

## Power

| Feature | Hardware | Evidence | Documented in | Gap |
|---|---|---|---|---|
| Battery charging | BQ25895 | P, D | [component](../../../components/texas-instruments/bq25895/README.md) | Charge current not published |
| Battery telemetry (mV/mA) | via coprocessor | **P (registers)** | [keyboard §1.10](keyboard.md) | — |
| 3.3 V buck-boost | TPS63020 | P, D | [component](../../../components/texas-instruments/tps63020/README.md) | — |
| 5 V boost / OTG | BQ25895 | D | idem | — |
| Always-on RTC | CH32V203 + 32.768 kHz | P, D | [component](../../../components/wch/ch32v203c8t6/README.md) | ">10 year" claim is theoretical |
| RTC alarm power-on latch | `74LVC2G02` | P, D | idem | Untested |
| Deep sleep / wake on `E7` | GPIO7 | D | [pinouts §2](pinouts-and-buses.md) | **No current figures published at all** |
| Battery life | 2500 mAh | N | — | **Completely unknown** |

## Software

| Feature | Evidence | Documented in | Gap |
|---|---|---|---|
| Launcher firmware | **P**, D | [software-architecture](software-architecture.md) | **Read**: dependencies, partition table, app tiering, boot sequence |
| **Plugin system (ELF)** | **P** | [software-architecture §4](software-architecture.md) · [apps-vs-plugins](apps-vs-plugins.md) | **Undocumented upstream.** API v2.0.0, default-off. SDK + 2 community examples found |
| **App vs plugin build process** | **P** | [apps-vs-plugins](apps-vs-plugins.md) | Neither was compiled — no toolchain available |
| **App execution / custom `.bin`** | **P** | [apps-vs-plugins §8–9](apps-vs-plugins.md) | `appfsBootSelect` + reboot; interpreter apps confirmed working |
| **Plugin permission model** | **P** | [apps-vs-plugins §11](apps-vs-plugins.md) | **Declared but not parsed or enforced** |
| **Portability (chips/targets)** | **P** | [portability](portability.md) | ESP32/S3/P4/S31/linux. Plugins P4-only |
| **Case fasteners** | **P** | [mechanical-and-case](mechanical-and-case.md) | 7 × M2×12 + 7 × M2 nuts, from FCStd XML |
| **eFuse identity** | **P** | [software-architecture §5](software-architecture.md) | Revision/radio/colour/region in `EFUSE_BLK3` |
| AppFS | D, **P** | [badgelink-and-appfs](badgelink-and-appfs.md) | Metadata model + launcher settings recovered. **On-flash layout not examined** |
| BadgeLink (WebUSB/Python) | D, **P** | [badgelink-and-appfs](badgelink-and-appfs.md) | **Protocol fully documented from source.** Untested on hardware |
| App repository (57 apps) | **P** | [software-and-apps](software-and-apps.md) | No app built or run |
| ESP-IDF workflow | D | [development](development.md) | Not executed |
| Coprocessor reflash over RVSWD | D | [development §7](development.md) | Untested; risky |
| PAX graphics | D | [software-and-apps](software-and-apps.md) | Not explored |
| LVGL (Konsool template) | D | [konsool-and-family](konsool-and-family.md) | Not explored |
| CircuitPython | — | [software-and-apps](software-and-apps.md) | Repo not examined |

## Mechanical

| Feature | Evidence | Documented in | Gap |
|---|---|---|---|
| 3D-printed case | P, D | [mechanical-and-case](mechanical-and-case.md) | Print settings unpublished |
| Board revisions 1/2/3 | D | idem | **Rev 1→2 changes unknown** |
| Custom front panels | D | idem | Two vendor designs, not cloned |
| Dimensions 120×135×18 mm, 215 g | D | [README](README.md) | — |
| **PCB dimensions** | **measured** | [pricing-and-dimensions](pricing-and-dimensions.md) | Not vendor-published; derived from STEP |
| **Pricing & availability** | **P** | [pricing-and-dimensions](pricing-and-dimensions.md) | €99.17 ex VAT; supply constrained |

---

## Summary of unresolved gaps

**Contradictions** (see [`gaps-and-conflicts.md`](gaps-and-conflicts.md)): P4 clock speed; display RGB888; expansion-port E-numbering within badge.team's own documentation.

**Never measured, by anyone, publicly:** battery life, deep-sleep current, Wi-Fi throughput, LoRa range, SD throughput, display frame rate, thermals.

**Documented but unexercised:** H.264 encoding, Thread/Zigbee, I3C mode, TE-synced rendering, AI extensions, add-on ID EEPROM (format undefined).

**Excluded from this pass:** community channels, pricing, regulatory filings, FreeCAD dimension extraction, `netlist.ipc` parsing.
