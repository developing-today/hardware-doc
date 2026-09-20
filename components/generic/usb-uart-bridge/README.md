# USB-UART bridge (`U10`) — resolved and re-filed as WCH CH340X

> **This record moved on 2026-08-30** to
> **[`components/wch/ch340x/`](../../wch/ch340x/README.md)**.

This directory existed because the part was **unidentified**: the Waveshare
ESP32-S3-Knob-Touch-LCD-1.8 schematic draws `U10` as a bare 10-pin functional symbol with no BOM
string, so it was filed under `generic/` by function rather than by part.

It was **resolved to a WCH CH340X on 2026-08-21** — from the pin names, pin order, the 10-pin
package and, decisively, the `R14` resistor topology. Filing by function was correct *only while*
the identity was unknown; once resolved, the record belonged under its manufacturer like every
other component. It simply never moved. That is the error this pointer records.

| | |
|---|---|
| Full record | [`components/wch/ch340x/README.md`](../../wch/ch340x/README.md) |
| Part | **WCH CH340X**, MSOP-10 |
| Board | `U10` on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |
| Family datasheet | [`vendors/wch/artifacts/ch340-datasheet-v3.4.pdf`](../../../vendors/wch/artifacts/ch340-datasheet-v3.4.pdf) |

## Not the same part as CH340C

[`components/wch/ch340c`](../../wch/ch340c/README.md) documents a **different variant** — SOP-16,
integrated clock generator, fitted on the Inkplate 5, Inkplate 5 Gen 2 and ZeroWriter Ink.

The two records held byte-identical copies of WCH's datasheet, which briefly made them look like
one part filed twice. They are not. The datasheet is a **family document** covering
CH340B/C/E/G/K/N/T/X together, and it now lives once at the vendor level, symlinked into both
component records. Both records remain, because both parts are real and distinct.

## Related generic records that stay generic

[`components/generic/usb-c-interface`](../usb-c-interface/README.md) remains under `generic/`
legitimately — it documents a connector/orientation topology rather than a specific silicon part.
