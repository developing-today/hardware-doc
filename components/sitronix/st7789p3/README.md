# Sitronix ST7789P3

- **Category:** single-chip TFT-LCD controller/driver, ST7789 family.
- **Manufacturer:** Sitronix Technology Corporation (Taiwan) — **inferred from the part-number
  family**, not from a datasheet in hand.
- **Research status:** ⚠ **No datasheet was located, from Sitronix or from any mirror.**
  Everything below is what M5Stack states plus what is structurally implied by the board it
  sits on. Nothing here is read from a component document.
- **Retrieved:** 2026-09-04

The display controller specified for the **M5Stack DinMeter v1.1 (K134-V11)**, replacing the
[ST7789V2](../st7789v2/README.md) of the original DinMeter.

---

## 1. What is actually established

| Property | Value | Evidence |
|---|---|---|
| Part string | **`ST7789P3`** | M5Stack DinMeter v1.1 page, in **three** places: Features list ("ST7789P3 display"), Specifications row *Display Driver*, and the PinMap section heading. Retrieved 2026-09-04 |
| Panel it drives on DinMeter v1.1 | 1.14 in, **135 × 240** | same page, *Display Resolution* row |
| Interface | 4-wire SPI, write-only | DinMeter schematic (`FPC1`, 8-pin 0.5 mm FPC) — **unchanged** from v1.0 |
| Pin assignment | CS G7, SCK G6, RS G4, MOSI G5, RESET G8, BL G9 | v1.1 PinMap — **identical to v1.0** |
| Datasheet on `docs.m5stack.com` | **none.** The v1.1 page's *Datasheets* section lists BM8563, tp4057, the DC connector and the battery seat — and **no display part**. The v1.0 page did link `ST7789V2_SPEC_V1.0.pdf` | verified 2026-09-04 |
| Mentioned in M5Stack's own v1.0↔v1.1 comparison table | **no** — that table has one row, *Main Controller* | verified 2026-09-04 |

## 2. What is *not* established

- **No datasheet.** Not on `sitronix.com.tw`, not mirrored by M5Stack, not found in this pass.
- **No register map, no command set, no differences from ST7789V2/V/VW.**
- **Not confirmed by a chip marking.** No teardown photograph of a v1.1 unit was inspected.
  The part string rests entirely on M5Stack's product page.
- **Whether "P3" denotes a different die, a different package, a different panel-integration
  variant, or a second-source label is unknown.**

## 3. Working assumption, and its status

M5Stack changed exactly one thing in the display line — the part string — while leaving the
resolution, the pin assignment, the FPC connector and the entire published schematic untouched,
and did not list the display in its own comparison table. M5GFX/LovyanGFX and ESP-IDF's
`esp_lcd_panel_st7789` continue to drive DinMeter v1.1 through the unchanged
`board_M5DinMeter` path in M5Unified (master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb`,
2026-09-04, which has no v1.1 board enum and no ST7789P3 branch).

**Therefore:** treat it as command-compatible with ST7789V2 for application purposes, including
the +52 / +40 GRAM gap and the `INVON` inversion.

**Evidence status: `inferred`.** Supported by the absence of any contrary evidence and by the
framework's silence, which is weak positive evidence. It is *not* verified, and a driver author
targeting register-level behaviour should not rely on it. What would settle it: an ST7789P3
datasheet, or a teardown photograph of a v1.1 unit's FPC-side controller marking.

## 4. Artifacts

**None.** No document exists to retain. This absence is itself recorded in
[`devices/m5stack/dinmeter/gaps-and-conflicts.md`](../../../devices/m5stack/dinmeter/gaps-and-conflicts.md) §4
and in [`devices/m5stack/dinmeter-v1.1/gaps-and-conflicts.md`](../../../devices/m5stack/dinmeter-v1.1/gaps-and-conflicts.md).

Searches performed and their (empty) results are logged in
[`devices/m5stack/dinmeter/research-log.md`](../../../devices/m5stack/dinmeter/research-log.md).

---

## Used By

### M5Stack DinMeter v1.1 (SKU K134-V11)

1.14 in 135 × 240 IPS panel, 8-pin 0.5 mm FPC. `SPI2_HOST`, mode 0, write-only: SCLK GPIO6,
MOSI GPIO5, CS GPIO7, D/C GPIO4, RESET GPIO8. Backlight via GPIO9 →
[AW35122FDR](../../awinic/aw35122/README.md) load switch. The wiring is identical to v1.0's
ST7789V2 in every respect.

→ [`devices/m5stack/dinmeter-v1.1/README.md`](../../../devices/m5stack/dinmeter-v1.1/README.md)
→ [`devices/m5stack/dinmeter/features/display.md`](../../../devices/m5stack/dinmeter/features/display.md)
