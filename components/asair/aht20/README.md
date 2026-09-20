# ASAIR (Aosong) AHT20 — I²C temperature and relative-humidity sensor

- **Category:** digital temperature + relative-humidity sensor
- **Manufacturer:** **Guangzhou Aosong Electronics / ASAIR** (广州奥松电子)
- **Retrieved:** 2026-09-04

## 1. Core facts

| Property | Value |
|---|---|
| Interface | I²C, **fixed 7-bit address `0x38`** (not configurable) |
| Humidity | 0 – 100 % RH, typical accuracy ±2 % RH |
| Temperature | −40 … +85 °C, typical accuracy ±0.3 °C |
| Supply | 2.2 – 5.5 V |
| Protocol | trigger-measurement command `0xAC 0x33 0x00`, wait ≥ 80 ms, read 6 bytes + CRC8 |
| Predecessor | **AHT10** — same address, *different* init sequence. Not interchangeable without a driver check. |

**Fixed address is the operational constraint.** Two AHT20s cannot share a bus. On any board
where `0x38` already appears, an AHT20 cannot be added without a mux.

## 2. Used By

### [LilyGO T-Display K230 Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

Fitted on the **nRF52840 base board**. I²C4 — the shared expansion bus — on **`GPIO46` SCL /
`GPIO47` SDA**, address **`0x38`**. Treated by the launcher as optional, detected at runtime,
surfaced in the sensor settings page.

The LilyGO tree references `AHT10` twice alongside `AHT20`, which suggests a probe that accepts
either; do not assume the fitted part from source alone.

## 3. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | `0x38`, GPIO46/47, base-board placement |
| S2 | AHT20 product datasheet | ASAIR | primary | datasheet | `http://www.aosong.com/en/products-32.html` | not retrieved | Electrical and protocol specification |
