# Espressif ESP32-C6-WROOM-1-N8

> Wi-Fi 6 / BLE 5.3 / IEEE 802.15.4 module
> Research snapshot **2026-08-24**. Documented as fitted to the Nicolai Electronics Tanmatsu; no hardware was available.

## Key specifications

| Property | Value |
|---|---|
| Core | 32-bit RISC-V single core, up to **160 MHz** |
| RAM | 512 KB |
| Flash | **8 MB** (N8 suffix) |
| Wi-Fi | **Wi-Fi 6** (802.11ax) 2.4 GHz |
| Bluetooth | **BLE 5.3** |
| 802.15.4 | IEEE 802.15.4-2015 — **Thread 1.3**, **Zigbee 3.0** |
| Antenna | PCB trace (WROOM-1); WROOM-1U is the U.FL variant |
| LCSC | [`C5366877`](https://www.lcsc.com/search?q=C5366877) |

Datasheet / product page: <https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf>

## Notes

A self-contained radio module. On boards that pair it with a non-radio application processor it is
usually run as a **radio peripheral** rather than as a general-purpose MCU, using Espressif's
`esp-hosted` firmware — the host drives it over SDIO or SPI and the C6 presents a network interface.

Its value in that role is breadth: a single module covers Wi-Fi 6, BLE and 802.15.4, so Thread and
Zigbee mesh come for free alongside conventional networking.

⚠ **The C6 enable signal is shared with the USB-A port power enable, and its boot-mode pin with the same.** Enabling the radio briefly force-powers the USB-A port on; entering radio bootloader mode briefly powers it off. The camera connector's enable line is also shared with the radio enable.

## Used by

### Nicolai Electronics Tanmatsu

| | |
|---|---|
| Reference designator | `U20` |
| Role | Radio peripheral running `esp-hosted`, driven by the ESP32-P4 |
| Host transport | **4-bit SDIO 2.0** — P4 GPIO: CLK 17, CMD 16, D0–D3 18–21 |
| Interrupt | P4 GPIO8 |
| Power/boot control | By the **CH32V203 coprocessor** — enable on `PB8`, boot mode on `PD1` |
| I2C | Wired to the internal I2C bus but **not currently used** by any firmware |
| Firmware | [`tanmatsu-radio`](https://github.com/Nicolai-Electronics/tanmatsu-radio) (Apache-2.0) |
| Host driver | [`esp32-component-tanmatsu-wifi`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-wifi) (MIT) |

Device record: [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) · BOM: [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md) · pinouts: [`pinouts-and-buses.md`](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md)

## Caveats

- Nothing in this record was verified on hardware.
- Board-level integration details come from the Tanmatsu production BOM (CERN-OHL-P), the Badge.Team BSP (MIT) and badge.team documentation, all retrieved 2026-08-24.
- Part-level specifications are from manufacturer product pages; **no local datasheet copies were retained**.
