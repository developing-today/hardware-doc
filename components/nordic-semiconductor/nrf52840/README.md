# Nordic Semiconductor nRF52840

- **Category:** Arm Cortex-M4F multiprotocol SoC — Bluetooth 5.4 LE, Bluetooth mesh, 802.15.4/Thread/Zigbee, ANT, 2.4 GHz proprietary, **USB 2.0 full-speed device**
- **Manufacturer:** Nordic Semiconductor ASA
- **Research status:** widely documented part; this record covers what is needed to work with it **as fitted on the LilyGO T-Display K230 expansion base**, and points at Nordic's own documentation for the rest.
- **Retrieved:** 2026-09-04

## 1. Core facts

| Property | Value |
|---|---|
| CPU | Arm **Cortex-M4** with FPU, 64 MHz |
| Flash / RAM | 1 MB / 256 KB |
| Radio | 2.4 GHz multiprotocol: Bluetooth LE (LE Coded PHY, LE 2M), Bluetooth mesh, IEEE 802.15.4, ANT, proprietary |
| USB | **USB 2.0 full-speed device** — this is what makes UF2 drag-and-drop bootloaders possible |
| Crypto | Arm CryptoCell-310 |
| Typical package | aQFN73 / QFN48 |
| Nordic documentation | `https://docs.nordicsemi.com/` (nRF52840 Product Specification) |

The part is thoroughly documented by Nordic; this record deliberately does not restate the
product specification. What is *not* documented anywhere else is how LilyGO uses it, below.

## 2. Firmware ecosystem relevant to this repository

| Route | Notes |
|---|---|
| **Adafruit nRF52 bootloader + UF2** | Double-tap reset enumerates a mass-storage device; drop a `.uf2` on it. Family ID **`0xADA52840`**. |
| PlatformIO `platform = nordicnrf52` | Board id used by LilyGO: **`nrf52840_dk_adafruit`**, framework `arduino` |
| nRF Connect SDK (Zephyr) | Nordic's own route; heavier |
| Serial DFU | Nordic's `nrfutil` / Adafruit `adafruit-nrfutil` |

## 3. Used By

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

Fitted on the **nRF52840 BLE / audio / sensor base board**, an optional expansion base for the
K230 main board. It exists because **the K230 has no Bluetooth radio of any kind**; the
nRF52840 is the board's BLE Central.

**Wiring (from LilyGO's own pin map, S1):**

| nRF52840 pin | Arduino pin | Goes to | Notes |
|---|---|---|---|
| `P0.11` | 11 | K230 **`GPIO3`** / UART1 **TX** | nRF52840 RX; K230 sends AT commands |
| `P0.12` | 12 | K230 **`GPIO4`** / UART1 **RX** | nRF52840 TX; AT responses and BLE events |
| `P1.00` | 32 | blue activity LED on the nRF52840 board | driven by firmware |
| `P0.04` | 4 | **external 5 V boost enable** | boosts the **21700** battery compartment to a stable 5 V for the host unit |
| USB CDC | — | host PC | 115 200 baud debug log |

Link parameters: **115 200 8N1, no flow control**, `/dev/ttyS1` on the K230 side, enabled by
`0060-riscv-dts-rm69a10-enable-uart1-nrf52840.patch`.

`P0.04` is the one to notice: it is not a peripheral pin, it is a **power** control. The
nRF52840 base owns the 5 V boost that powers the main unit from the 21700 cell.

**Firmware.** LilyGO ships a custom **AT-command BLE Central** firmware
(`Xinyuan-LilyGO/T-Display-K230-nRF52840`, commit `4646a728580739d487126f47a521e9b8032b3c2c`,
2026-08-23). Prebuilt artifacts are in the repository:

| File | Bytes | Role |
|---|---|---|
| `bootloader/k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex` | 525 680 | Bootloader with **UART DFU** at 115 200 and **SoftDevice S140 6.1.1** |
| `firmware/k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2` | 296 960 | Application, build date **2026-08-16**, revision **r4** |

**Two DFU paths exist and they are different.** The USB/UF2 path (double-tap reset, drag UF2 to
the enumerated drive) is the normal developer route. The **UART DFU** path is what lets the
*K230* reflash the nRF52840 in the field with no USB cable, and it is the reason for the custom
bootloader hex above and for `tools/k230_nrf52840_dfu.cpp` (33 370 bytes) and the launcher's
`ui_nrf52840_dfu.c`. The launcher explicitly arbitrates ownership of the nRF52840 between
Meshtastic BLE and UART DFU (changelog v0.2.2).

**AT surface:** `AT`, `AT+VER?`, `AT+MESHSTATUS?`, `AT+SCAN=<s>`, `AT+LIST?`, `AT+CONN=<i>`,
`AT+GATTS?`, `AT+DISC`, plus read/write/subscribe on characteristics; async URCs
`+SCAN:`, `+CONNECTED:`, `+DISCONNECTED:`, `+BOOT:K230_NRF52840_AT`, `+MESH:ADV,1`.
Full guide: `docs/AT_COMMANDS.md` in that repository.

⚠ **Serial-monitor gotcha, stated by LilyGO:** "for some serial monitors, you need to select
**DTR** to see the serial port output messages."

## 4. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | UART1 mapping, LED, AHT20 and MAX98357A on the same base |
| S2 | `T-Display-K230-nRF52840` README, firmware and bootloader | LILYGO | primary | repository | `https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840/tree/4646a728580739d487126f47a521e9b8032b3c2c` | 2026-09-04 | Pin map incl. `P0.04` boost enable, PlatformIO board, UF2 family ID, DFU procedure, AT set |
| S3 | nRF52840 Product Specification | Nordic Semiconductor | primary | datasheet | `https://docs.nordicsemi.com/` | 2026-09-04 (not downloaded) | Core specification |
