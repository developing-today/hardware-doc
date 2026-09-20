# UltraChip (UC) — e-paper display controllers

UltraChip Inc. designs the **UC8xxx** family of electrophoretic display driver
ICs, ubiquitous in small mono and colour e-paper modules. Parts are usually
delivered **chip-on-glass or chip-on-film inside a display module**, so they have
no board reference designator and are identified from the module datasheet, the
driver source, or a runtime register read.

| Part | Role in this knowledge base |
|---|---|
| [`uc8253`](uc8253/README.md) | Xteink X3 (792×528) — original production |
| [`uc8179`](uc8179/README.md) | Xteink X4 / X4 Pro / X4 Classic (800×480) — newer batches |
| [`uc8279`](uc8279/README.md) | Xteink X3 (as UC8279d) and X4-family (800×480) — newer batches; also EEGO A4 as UC8279C |

## The family trait that matters most

**UC81xx parts answer `VER (0x70)` and `FLG (0x71)` register reads; the Solomon
Systech SSD16xx family does not.** That single asymmetry is what makes runtime
controller detection possible on boards that ship more than one panel variant —
see [`../solomon-systech/ssd1677/README.md`](../solomon-systech/ssd1677/README.md)
and the Xteink display guides.

## Sourcing note

UltraChip does not publish a public datasheet portal that this session could
reach. Every UC8xxx datasheet referenced here is served by a **module vendor
mirror** (Good Display, Elecrow, Waveshare). Record the mirror, and treat the
revision as unverified against the chip maker.
