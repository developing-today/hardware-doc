# T-Display-S3 Long — gaps and conflicts

| # | Item | Evidence | Status |
|---|---|---|---|
| L1 | **`pins_config.h` contradicts itself twice.** `TFT_QSPI_D2 21` vs `PIN_BUTTON_2 21`; `TP_RST 2` vs `PIN_BAT_VOLT 2` | `examples/factory/pins_config.h` @ `37a7e83`, single file | **Confirmed defect.** Copy-paste residue from the AMOLED header. Neither `PIN_BUTTON_2` nor `PIN_BAT_VOLT` is valid on this board |
| L2 | **Which touch controller does a given board have?** Default branch is `…-cst3530`; two factory images ship; the AXS15231B has integrated touch | branch name, `firmware/factory.bin` vs `factory-cst3530.bin`, `examples/cst3530_touch/` | **Unresolved by documentation.** Resolve empirically: flash each factory image |
| L3 | **With or without SD slot?** Two schematics exist; the store lists no SD option | `T-Display-S3-Long-3.4-V1.0.pdf` vs `…-with-SD-slot.pdf` | **Unresolved.** The SPI SD pins in `pins_config.h` (38/39/40/41) presuppose the slot |
| L4 | **Repo has no LICENSE.** `gh api repos/…` reports `license: none` | GitHub API 2026-09-07 | Redistribution status of the schematics and firmware here is **unknown**, unlike the MIT base-board repo |
| L5 | **Battery voltage** has no ADC path; must be read from the SY6970 over I²C | absence of a valid `PIN_BAT_VOLT`; SY6970 present | **Inferred**, consistent, but no vendor example named `SY6970` exists in *this* repo (the 1.64″ repo has one) |
| L6 | **No ESPHome support.** `mipi_spi` has models for T-DISPLAY-S3, -PRO, -AMOLED, -AMOLED-PLUS and T4-S3, but none for the Long | `esphome/components/mipi_spi/models/*.py`, `dev` @ 2026-09-07 | **Negative result** |
| L7 | **25 open issues**, the most of any board in the family | GitHub API | Not a defect per se; a maturity signal worth stating |

## Gaps

- No hardware; nothing verified.
- Schematic net connectivity not traced.
- The AXS15231B touch protocol is described only by a 2-page vendor note; the full command set
  is not documented anywhere located.
- Which SKU (`H685` / `H721`) corresponds to which schematic is unknown.
