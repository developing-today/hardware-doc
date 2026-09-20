# Texas Instruments BQ25896 — I²C single-cell 3 A buck battery charger with narrow-VDC power path

- **Category:** Li-ion/Li-polymer switch-mode battery charger + system power path + **boost (OTG)** output, I²C-controlled
- **Manufacturer:** Texas Instruments
- **Research status:** part identified from vendor BSP; TI datasheet referenced, not retrieved in this pass.
- **Retrieved:** 2026-09-04

## 1. Core facts

| Property | Value |
|---|---|
| Topology | Synchronous buck, **up to 3 A** charge current |
| Input | 3.9 – 14 V (abs max higher); **D+/D− input-source detection** |
| Battery | single cell Li-ion / LiPo |
| Boost / OTG | yes — 4.55 – 5.51 V programmable |
| Control | **I²C**, 7-bit address **`0x6B`** |
| Notable | integrated ADC for VBUS/VBAT/VSYS/ICHG/TS readback; input-current-limit detection; NTC (TS) monitoring |
| Datasheet | `https://www.ti.com/lit/ds/symlink/bq25896.pdf` |

## 2. Relationship to BQ25895 (already in this repository)

[`components/texas-instruments/bq25895`](../bq25895/README.md) exists here. **BQ25895 and
BQ25896 are siblings, not the same part.** They share the register map layout and the `0x6B`
address, and differ mainly in input voltage/current handling and in the default settings burned
at the factory. Firmware written for one will *mostly* drive the other, which is exactly the
condition that produces subtle field failures — verify `REG14` (part revision / device ID)
rather than assuming. The BQ25890 also appears once in the LilyGO tree, presumably as a
fallback probe.

## 3. Used By

### [LilyGO T-Display-S3 AMOLED Plus](../../../devices/lilygo/t-display-s3-amoled-plus/README.md) — *added 2026-09-07*

Designator **`U6`** on `schematic/T-Display-S3-AMOLED-Plus.pdf` (`Xinyuan-LilyGO/LilyGo-AMOLED-Series` @ `6d1dc008b94578cc34ba4a0f3b223dd808ca963f`, retained at [`devices/lilygo/t-display-s3-amoled-plus/artifacts/schematic/`](../../../devices/lilygo/t-display-s3-amoled-plus/artifacts/schematic/T-Display-S3-AMOLED-Plus.pdf)). Read from the sheet's designator/part text; **net connectivity was not traced**.

This is the **only** board in the [LilyGO T-Display-S3 family](../../../devices/lilygo/t-display-s3-shared/README.md) using a BQ25896. Its siblings use a [Silergy SY6970](../../silergy/sy6970/README.md) (Long, Pro, T4-S3, the DS-series AMOLEDs), an [X-Powers AXP2101](../../x-powers/axp2101/README.md) (AMOLED Lite), or a dumb linear [TP4065-class charger](../../nanjing-top-power/tp4065/README.md) with a soldered current-programming resistor (base T-Display-S3, 1.91″ AMOLED). The board also fits a [PCF85063ATL](../../nxp/pcf85063a/README.md) RTC with a Seiko MS412FE backup cell and an on-board microSD slot, none of which the plain 1.91″ AMOLED has — the PMIC is part of a deliberate step up in power management, not an incidental substitution.

Driven with `lewisxhe/XPowersLib`; vendor example `examples/PPM_Example_for_191Plus` in `LilyGo-AMOLED-Series`. LilyGO's own current table gives this board **≈230–700 µA “dynamic”** deep-sleep current against a flat ≈230 µA for the plain AMOLED — the range being the PMIC and RTC remaining active.


### [LilyGO T-Display K230 Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

Charger on the **nRF9151 keyboard base board**. I²C4, shared bus: **`GPIO46` SCL / `GPIO47`
SDA**, 7-bit address **`0x6B`**. Used by the launcher for charger state and USB/power-source
status, alongside a [BQ27220](../bq27220/README.md) fuel gauge at `0x55` on the same bus.

The launcher treats the charger as **optional hardware**: "Optional hardware features are shown
only when the related module is detected. This includes nRF9151, nRF52840, TCA8418, BQ27220,
BQ25896, XL9555, and AHT20." A bare K230 main board has none of these.

Low-battery shutdown policy lives in the launcher (`battery_low_shutdown_*` in
`ui_hardware.c`), driven from BQ27220 voltage/SoC readings with the BQ25896's USB-present
status as a gate — i.e. **the shutdown decision is a software policy in userspace, not a
hardware cut-off.** Changelog v0.2.3 "set the default low-battery shutdown threshold" and
v0.2.2 "improved first-run charger, battery, and low-voltage shutdown defaults" show this was
tuned after release.

## 4. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | `0x6B`, I²C4 on GPIO46/47 |
| S2 | `k230_launcher/k230_phone_ui/src/ui_hardware.c` | LILYGO | primary | source | same repo | 2026-09-04 | Charger/gauge integration, low-battery shutdown policy |
| S3 | BQ25896 datasheet | Texas Instruments | primary | datasheet | `https://www.ti.com/lit/ds/symlink/bq25896.pdf` | not retrieved | Electrical specification |
