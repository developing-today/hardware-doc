# Hardware subject guides

Cross-cutting guides about **hardware subsystems** rather than about a vendor, a chip family or a
market. They compile knowledge that is spread across several [component](../../components/README.md)
and [device](../../devices/README.md) records into a single treatment of the subject.

| Guide | What it covers |
|---|---|
| [**E-paper displays**](e-paper-displays.md) | How electrophoretic displays work — waveforms, LUTs, greyscale, ghosting and why periodic full refreshes are forced. Why a bare panel needs a multi-rail PMIC and a hardware power sequencer. **VCOM and why it is per-panel-lot.** Partial vs full vs greyscale trade-offs with real timings. Temperature dependence, and the gap between the sensor that exists and the sensor that is used. Burn-in and lifetime. **The NDA problem: exactly what is and is not publicly establishable about an E Ink panel.** Practical guidance for driving one |
| [**Display interfaces**](display-interfaces.md) | SPI vs QSPI vs i80/RGB parallel vs MIPI-DSI vs e-paper parallel — when each is used, who owns the frame, and bandwidth arithmetic from real figures. The ESP32 family's LCD peripheral support per chip. **Framebuffer and PSRAM sizing with worked cases.** Tearing, TE lines and what happens when TE is not routed. LVGL integration and buffer sizing. **A table of every display controller in the library**, with and without a component record |

---

## Conventions

These guides follow the [repository evidence labels](../README.md#conventions) — **[DOC]** vendor
document · **[SCH]** schematic · **[SRC]** source code · **[WEB]** vendor web page · **[COM]**
community report · **[INF]** inference — applied transitively from the records they cite.

Because they **synthesise rather than research**, each ends with an explicit **evidence boundary**
section stating what is inherited and what is new. **Where a guide disagrees with a linked deep
record, the deep record wins.**

Both guides were compiled **2026-08-30** with **no new retrieval and no hardware access**, which is
consistent with every record they draw on: nothing in this library has been tested on a physical
board.

## Related

- [Guides index](../README.md) · [Espressif guides](../espressif/README.md) · [Markets and sourcing](../markets/README.md)
- [Device comparison matrix](../markets/device-comparison-matrix.md) — the display, power and input columns across every documented device
- [Component index](../../components/README.md) · [Device index](../../devices/README.md)
