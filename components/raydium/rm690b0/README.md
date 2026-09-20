# Raydium RM690B0

- **Category:** AMOLED display driver IC with on-chip GRAM; QSPI/SPI/MIPI host interfaces.
- **Manufacturer:** Raydium Semiconductor Corporation (Taiwan).
- **Retrieved:** 2026-09-07

The display driver of the **LilyGO T4-S3** — a 2.41″ 450 × 600 AMOLED, the largest and
brightest panel in the T-Display-S3 family.

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **RM690B0** |
| Datasheet version | **V0.2** per LilyGO's filename |
| Native resolution | **480 × 600** per ESPHome's base `DriverChip("RM690B0", width=480, height=600)`; the T4-S3 panel is **450** wide and sits at **`offset_width=16`** |
| Local artifact | [`artifacts/rm690b0-datasheet-v0.2-lilygo-mirror.pdf`](artifacts/rm690b0-datasheet-v0.2-lilygo-mirror.pdf) — 4 199 504 B, SHA-256 `2f21e71e83d818e6ac8285b6c883ff586951dcbce9037b3bdb2f4ee5a6350e7e` |
| Mirror source | `Xinyuan-LilyGO/LilyGo-AMOLED-Series` → `datasheet/RM690B0 DataSheet_V0.2.pdf` @ `6d1dc008b94578cc34ba4a0f3b223dd808ca963f` |
| Licence | Raydium copyright; repository MIT does not cover it. **Redistribution status: unknown** |

## 2. Initialisation, from an independent source

ESPHome's `RM690B0` driver definition (`esphome/components/mipi_spi/models/amoled.py`, `dev`,
fetched 2026-09-07) gives a base init sequence that is useful precisely because it is **not**
LilyGO's:

```
PAGESEL 0x20 · MIPI 0x0A · WRAM 0x80 · SWIRE1 0x51 · SWIRE2 0x2E ·
PAGESEL 0x00 · 0xC2 0x00 · delay(10) · TEON 0x00 · NORON
brightness 0xD0 · color_order RGB
```

`SWIRE1`/`SWIRE2` are the AMOLED brightness-control registers; `MIPI 0x0A` selects the host
interface. Anyone writing an RM690B0 driver from scratch can start here.

## 3. Software

| Route | Note |
|---|---|
| **`LilyGo-AMOLED-Series`** | auto-detects T4-S3 |
| ESPHome | `mipi_spi` model `T4-S3` extending `RM690B0`, `bus_mode=QUAD`, `requires psram` |
| `TFT_eSPI` | **cannot drive it** (QSPI) |

## 4. What was not verified

Datasheet cover and register map not read; no value here is transcribed from it. The register
names above are ESPHome's symbolic constants, which are themselves an interpretation.

## 5. Used by

### LilyGO T4-S3
→ [`devices/lilygo/t4-s3`](../../../devices/lilygo/t4-s3/README.md).
QSPI on GPIO 11 (CS), 15 (SCK), 14/10/16/12 (D0–D3), 13 (RST). Panel 450 × 600 at 550 nits,
window offset 16. Touch is a separate Hynitron **CST226SE** on I²C (SDA 6 / SCL 7, IRQ 8,
RST 17). **Vendor warns GPIO18 is assigned to the display TE pin** — though the vendor's own
`product_pins.h` says TE is not wired; see the device record's conflict T4-C1.
