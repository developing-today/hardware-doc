# MEMSensing MSM261D3526H1CPM

- **Category:** MEMS **PDM digital microphone**, bottom-port, omnidirectional
- **Manufacturer:** MEMSensing Microsystems (Suzhou) Co., Ltd. — 敏芯微电子
- **Retrieved:** 2026-08-24
- **Evidence:** **primary** — reference designator `MIC1`, value `MSM261D3526H1CPM`, in the EAGLE BOM of the *XIAO ESP32S3 Sense expansion board v1.0* schematic. Library part `MIC-MSM261D3526H1CPM`.

> **This part number was widely repeated online but unconfirmed until this research pass.** It is now established from Seeed's own schematic.

## Part number decode

`MSM` MEMSensing microphone · `261` series · **`D` = digital (PDM)** · `3526` = 3.5 × 2.65 mm package · `H1` bottom-port · `CPM` packaging.

Sibling already documented here: [MSM261D4030H1CPM](../msm261d4030h1cpm/README.md) — same family, 4.0 × 3.0 mm package.

## Pinout as wired

| Pin | Signal | Connection on the Sense daughterboard |
|---|---|---|
| `VDD` | supply | **`VCC_3V3`** — the XIAO's 3.3 V rail directly (no local LDO) |
| `CLK` | PDM clock in | via solder jumper **JP1** → `IO42/PDM_CLK` → B2B pad 27 |
| `DATA` | PDM data out | via solder jumper **JP2** → `IO41/PDM_DATA` → B2B pad 26 |
| **`L/R`** | channel select | **tied to GND** |
| `GND` ×2 | ground | GND |

**`L/R` tied to GND selects the LEFT channel.** This is the hardware reason the device is mono, and why PDM configurations requesting the right channel return silence — the microphone only drives its data line during one half of the clock period.

## Capabilities

Typical for the MSM261D-series PDM part. ⚠ **No MEMSensing datasheet was obtained in this pass** — the table below is indicative, not established.

| Parameter | Typical |
|---|---|
| Interface | PDM, 1-bit, single data line |
| Supply | 1.6–3.6 V (here: 3.3 V) |
| Clock | ~1–3.25 MHz |
| Directionality | Omnidirectional |
| Port | Bottom |

**Sensitivity, SNR, AOP and frequency response are NOT established here.** Obtain the MEMSensing datasheet before making any acoustic-performance claim.

## Solder jumpers — the microphone is disconnectable

`CLK` and `DATA` each pass through a **2-pad solder jumper** (`JP1`, `JP2`) before reaching the board-to-board connector. Cutting them isolates the microphone and frees **GPIO41 and GPIO42** — which are also `MTDI` and `MTMS`, two of the four JTAG pins.

Test pads `J4` and `J5` (both **DNP**) sit on the `IO42` / `IO41` nets, so both signals are also probeable.

This is undocumented by Seeed, and is the only route to recovering half the JTAG port while keeping the camera fitted.

## Used by

### Seeed Studio XIAO ESP32S3 Sense

Sole microphone, on the detachable Sense daughterboard. Reached from the ESP32-S3R8 across the [DF40 board-to-board connector](../../hirose/df40c-30dp-0.4v/README.md) on **GPIO42 (CLK)** and **GPIO41 (DATA)**.

Driven by the ESP32-S3's I²S peripheral in **PDM RX mode**, available on **`I2S_NUM_0` only**. Mono, **16-bit only**; 16 kHz is the vendor-tested stable rate.

Usage guide: [`features/microphone.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/features/microphone.md) · Board detail: [`sense-daughterboard.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/sense-daughterboard.md)

## Related
- [MSM261D4030H1CPM](../msm261d4030h1cpm/README.md) — larger-package sibling
- [ESP32-S3R8](../../espressif/esp32-s3r8/README.md) · [DF40C-30DP-0.4V](../../hirose/df40c-30dp-0.4v/README.md)
