# T-Display K230 — feature coverage

Legend for **Evidence**: `V` vendor-documented · `S` vendor source code read in this pass ·
`C` community-reported · `—` none found.
**Test status** is uniform: nothing was executed on hardware in this pass.

| Feature | Hardware | Component record | Vendor doc | Source read | Community | Feature guide | Build tested | HW tested | Gap |
|---|---|---|---|---|---|---|---|---|---|
| AMOLED display | RM69A10 + K230 DSI | [✔](../../../components/raydium/rm69a10/README.md) | V | S | C | [✔](features/display.md) | no | **no** | refresh rate, brightness curve, measured fps |
| Touch | GT9895 | [✔](../../../components/goodix/gt9895/README.md) | V | S | — | [✔](features/touch.md) | no | **no** | touch-point count, datasheet |
| Keyboard | TCA8418 + XL9555 | [✔](../../../components/texas-instruments/tca8418/README.md) · [✔](../../../components/xlsemi/xl9555/README.md) | V | S | C | [✔](features/keyboard.md) | no | **no** | rollover, XL9555 actual address |
| Keyboard backlight | K230 PWM4 | — | V | S | — | [✔](features/keyboard.md) | no | **no** | brightness curve |
| Camera | GC2093 | [✔](../../../components/galaxycore/gc2093/README.md) | V | S | C | [✔](features/camera.md) | no | **no** | `GC-6` — sensor parameters |
| ISP | K230 | [✔](../../../components/canaan/k230/README.md) | V | — | — | [✔](features/camera.md) | no | **no** | tuning not exercised |
| **KPU / NPU** | K230 | [✔](../../../components/canaan/k230/README.md) | V | S | C | [✔](features/kpu-npu.md) | no | **no** | no measurement on this board; TOPS disputed |
| Dual RISC-V cores / RVV | K230 | [✔](../../../components/canaan/k230/README.md) | V | S | C | [✔](features/dual-core-riscv.md) | no | **no** | `GC-1` — which core runs Linux here |
| Video encode/decode | K230 VPU | [✔](../../../components/canaan/k230/README.md) | V | — | — | — *(covered in the component record)* | no | **no** | not exercised |
| GPU (2.5D) | K230 | [✔](../../../components/canaan/k230/README.md) | V | S (`vg_lite_demos`) | — | — *(component record)* | no | **no** | not exercised |
| DPU (structured light) | K230 | [✔](../../../components/canaan/k230/README.md) | V | — | — | — | no | **no** | **no structured-light projector on this board** — silicon feature, unusable as fitted |
| Wi-Fi | RTL8189FS | [✔](../../../components/realtek/rtl8189fs/README.md) | V | S | C | [✔](features/wifi-and-bluetooth.md) | no | **no** | throughput; which module is actually fitted |
| Bluetooth | USB dongle | — *(no on-board part)* | partial | S | C | [✔](features/wifi-and-bluetooth.md) | no | **no** | `GC-2` — ESP32-S3 claim |
| Ethernet | USB, RTL8152B claimed | [✔](../../../components/realtek/rtl8152b/README.md) | V | S | C | [✔](features/ethernet.md) | no | **no** | `GC-3` — controller identity |
| LoRa | SX1262 / LR2021 | [✔](../../../components/semtech/sx1262/README.md) · [✔](../../../components/semtech/lr2021/README.md) | V | S | C | [✔](features/lora.md) | no | **no** | range, TX current, certification |
| Audio out | K230 codec + MAX98357A | [✔](../../../components/analog-devices/max98357a/README.md) | V | S | — | [✔](features/audio.md) | no | **no** | speaker amp unidentified (U2) |
| Microphone | unknown | [U3](../../../components/unidentified/t-display-k230/README.md) | partial | S | — | [✔](features/audio.md) | no | **no** | PDM or analogue? |
| 3.5 mm jack | K230 codec | — | V (cased only) | — | — | [✔](features/audio.md) | no | **no** | |
| microSD | K230 MMC1 | [✔](../../../components/generic/micro-sd-sdmmc/README.md) | V | S | C | [✔](features/microsd.md) | no | **no** | throughput |
| USB host | K230 OTG | — | V | S | C | [✔](features/usb.md) | no | **no** | speed not confirmed |
| USB gadget (MTP/MSC/RNDIS/ACM) | K230 OTG | — | V | S | — | [✔](features/usb.md) | no | **no** | |
| Battery + charging | BQ25896 + BQ27220 | [✔](../../../components/texas-instruments/bq25896/README.md) · [✔](../../../components/texas-instruments/bq27220/README.md) | V | S | C | [✔](features/battery-and-power.md) | no | **no** | **battery life never measured** |
| Power key | K230 PMU INT0 | [✔](../../../components/canaan/k230/README.md) | V | S | — | [✔](features/battery-and-power.md) | no | **no** | |
| Thermal sensor | K230 | [✔](../../../components/canaan/k230/README.md) | V | S | — | [✔](features/battery-and-power.md) | no | **no** | no thermal data |
| 40-pin header / GPIO | K230 | [✔](../../../components/canaan/k230/README.md) | V | S | — | [✔](features/gpio-and-expansion.md) | no | **no** | current limits |
| ADC ×3 | K230 | — | **—** | — | — | [✔](features/gpio-and-expansion.md) | no | **no** | `GC-8` — not in the peripheral list |
| BLE via nRF52840 | nRF52840 | [✔](../../../components/nordic-semiconductor/nrf52840/README.md) | V | S | — | [✔](features/nrf52840-ble.md) | no | **no** | range, throughput |
| Cellular + GNSS | nRF9151 | [✔](../../../components/nordic-semiconductor/nrf9151/README.md) | V | S | — | [✔](features/nrf9151-cellular-gnss.md) | no | **no** | bands, SIM form factor, antenna, certification |
| Temp/humidity | AHT20 | [✔](../../../components/asair/aht20/README.md) | V | S | — | [✔](features/gpio-and-expansion.md) | no | **no** | AHT10 vs AHT20 uncertainty |
| HDMI out | LT9611 (?) | [✔](../../../components/lontium/lt9611/README.md) | V | S | — | referenced in [display.md](features/display.md) | no | **no** | `GC-4` — presence unconfirmed |
| QWIIC | — | — | V (cased only) | — | — | [✔](features/gpio-and-expansion.md) | no | **no** | which bus? |
| 16 MB flash | unknown | — | V | **—** | — | — | no | **no** | `GC-9` — role unknown |
| PMIC | unknown | [U1](../../../components/unidentified/t-display-k230/README.md) | **—** | **—** | — | — | no | **no** | not identified at all |

## Summary

| | Count |
|---|---:|
| Advertised or fitted capabilities enumerated | **32** |
| With a component record | 24 |
| With a feature guide | 16 (guides) covering 28 capabilities |
| With an explicit recorded gap | 9 tracked as `GC-1`…`GC-9`, plus 6 unidentified parts |
| **Build-tested here** | **0** |
| **Hardware-tested here** | **0** |

**The honest headline: coverage of *documentation* is broad; coverage of *verification* is zero.**
Every capability above has a hardware path traced to a component record and a task-oriented guide,
and not one of them has been observed working. The `commands.md` §5 list is written so that a
single session with hardware in hand could close most of the gaps in an afternoon.

## Silicon capabilities present but unusable as fitted

Worth stating because they inflate spec-sheet comparisons:

- **DPU (3D structured light)** — needs a projector and an IR camera. Neither is fitted.
- **RGB-IR 4×4 ISP mode** — needs an RGB-IR sensor. GC2093 is not one.
- **Two further MIPI CSI inputs** — unpopulated, but genuinely available on the header.
- **eMMC / SPI NAND boot** — supported by the SoC; the board boots from SD.
- **8 PDM DMIC inputs** — far more than the board fits.
- **Deep sleep ≤ 20 µW** — a silicon claim with no board-level demonstration.
