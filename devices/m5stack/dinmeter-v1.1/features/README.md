# DinMeter v1.1 — feature guides

**All nine feature guides live in the v1.0 record and apply verbatim to v1.1**, because the
carrier board, its GPIO map and its peripherals are unchanged. They are not duplicated here.

→ **[`../../dinmeter/features/`](../../dinmeter/features/README.md)**

| Guide | v1.1 delta |
|---|---|
| [Rotary encoder and buttons](../../dinmeter/features/rotary-encoder-and-buttons.md) | none |
| [Display](../../dinmeter/features/display.md) | controller named **ST7789P3** instead of ST7789V2; same pins, same 135 × 240, same GRAM gap (+52, +40), same `INVON`, same driver path. **No ST7789P3 datasheet exists** |
| [RTC and timekeeping](../../dinmeter/features/rtc-and-timekeeping.md) | none |
| [Buzzer](../../dinmeter/features/buzzer.md) | none |
| [Power and battery](../../dinmeter/features/power-and-battery.md) | none at board level. The **module's** sleep current improves ~45× on `VIN_5V`, but the board's own 38.4 µA standby figure is **unchanged on both product pages** — because the board cuts the battery with a latch rather than sleeping the SoC |
| [PORT.A / PORT.B expansion](../../dinmeter/features/porta-portb-expansion.md) | none |
| [Wi-Fi and BLE](../../dinmeter/features/wifi-and-ble.md) | same radio and API. The module's antenna matching network was rebuilt and M5Stack claims *"better signal reception"* — **with no figure and no method**. Neither corroborated nor refuted |
| [**RGB LED**](../../dinmeter/features/rgb-led.md) | ⚠ **THE ONE REAL CHANGE.** Requires `GPIO38 = HIGH` before the LED will light. Silent failure otherwise |
| [DIN mounting and mechanical](../../dinmeter/features/din-mounting-and-mechanical.md) | none — the published STL is byte-identical. Packaging differs (136 × 95 × 24 mm, 44.9 g gross vs 136 × 93 × 23 mm, 47.0 g) and the bundle names changed |

## If you read one thing

[`../stamp-s3-to-s3a-delta.md`](../stamp-s3-to-s3a-delta.md) — the complete, schematic-derived
Stamp-S3 → Stamp-S3A change list, which *is* the v1.1 product.
