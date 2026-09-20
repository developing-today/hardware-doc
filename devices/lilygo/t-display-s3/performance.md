# T-Display-S3 — performance

> **This record contains no measurement of this board.** None was produced (no hardware) and
> none was found (40+ sources searched). What follows is what is actually evidenced, and what
> would have to be measured.

## What is evidenced

| Quantity | Value | Class | Source |
|---|---|---|---|
| Display pixel clock, vendor's choice | **16 MHz**, with the vendor's own caveat *"Too low or too high pixel clock may cause screen mosaic"* | official configuration | `examples/factory/pin_config.h` @ `ec889e7` |
| Display pixel clock, ESPHome's choice | **10 MHz** | third-party configuration | `esphome/.../mipi_spi/models/lilygo.py`, `dev` |
| CPU | 240 MHz, dual Xtensa LX7 | official spec | board manifest `f_cpu 240000000L` |
| Flash | 16 MB, **QIO 80 MHz** per the board manifest; the shipped factory bootloaders say **DIO** | official / measured | manifest vs decoded images |
| PSRAM | 8 MB octal (OPI) | official | `memory_type qio_opi` |
| Usable RAM | 327 680 B per the board manifest | official | — |
| Upload speed | 921 600 baud | official | — |

## Derived, not measured

An 8-bit 8080 bus at 16 MHz carries one byte per `WR` strobe → 2 strobes per RGB565 pixel →
~8 M pixel/s. A 170 × 320 = 54 400-pixel full-screen redraw is therefore **~6.8 ms of bus
time**. Real figures will be worse: driver overhead, DMA setup, and any per-line command
framing. Treat this as a ceiling, not a benchmark. At ESPHome's 10 MHz it becomes ~10.9 ms.

For comparison, the same panel on a 40 MHz single-lane SPI link would need ~21.8 ms of bus
time. **That ~3× is the entire argument for the 13-wire bus**, and it is arithmetic, not a
measurement.

## Numbers from other boards, clearly labelled as such

LilyGO publishes a current table for its **AMOLED** boards and none for this one:

| Board | Active (240 MHz, Wi-Fi on) | Deep sleep | Wake source |
|---|---|---|---|
| T-Display AMOLED Lite | 90–230+ mA | ~1.1 mA | timer |
| **T-Display-S3 AMOLED** | 90–230+ mA | ~230 µA | GPIO0 |
| T4-S3 | 90–230+ mA | ~230 µA | GPIO0 |
| T-Display-S3 AMOLED Plus | 90–230+ mA | ~230–700 µA dynamic | GPIO0 |

— `LilyGo-AMOLED-Series/README.MD` @ `6d1dc00`, vendor table.

**These are different boards.** Different display technology, different regulators (LDO vs
buck), different charger, different sleep topology. The active figure is dominated by the SoC
and radio and is therefore roughly transferable; **the deep-sleep figure is not**, because it
is exactly the part that the board design determines. Anyone quoting "230 µA deep sleep for the
T-Display-S3" is quoting the AMOLED board.

## What to measure, and why each matters

| Measurement | Method | Why it matters |
|---|---|---|
| Full-screen fill rate at 10/16/20 MHz | `Arduino_GFX` `PDQgraphicstest` (already in the repo) at each clock, timed | settles the mosaic threshold, which varies by production run |
| Deep-sleep current, battery only, GPIO15 held low | µA-capable meter in series with the cell | LilyGO publishes nothing; the divider question ([K3](gaps-and-conflicts.md)) is worth ~21 µA |
| Deep-sleep current **with and without** `gpio_hold_en()` on 16/17 | as above | quantifies the fitted-pull-up cost |
| Wi-Fi TX peak | high-bandwidth current probe | explains brown-outs on marginal supplies ([issue #143](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/143)) |
| RSSI vs a reference ESP32-S3 devkit at fixed distance | both boards, same AP, same orientation | the "weak Wi-Fi" complaint has **never** been measured by anyone in the searched set |
| Actual charge current into a discharged cell | series meter | settles the 500-vs-580 mA conflict **and** identifies the fitted charger by behaviour |
| Backlight luminance vs PWM duty | photometer | tests the AW9364 non-linearity claim |

Each of these is a few minutes with a board and a meter, and each closes a question that
currently has no answer anywhere.

## LVGL

LilyGO ships `examples/lv_demos` with an LVGL **8.x** config. `examples/Lvgl_benchmark`
exists in the **1.64″ AMOLED** repo but **not** in the base-board repo, so there is no vendor
LVGL benchmark for this board. One community report notes the `PCBClock` example failing to
fit ([issue #256](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/256)) — an out-of-memory
symptom that resolves to the OPI PSRAM setting rather than to performance.
