# T-Display-S3 AMOLED — gaps and conflicts

| # | Conflict | Evidence | Status |
|---|---|---|---|
| A1 | **Flash size: 4 MB or 16 MB?** `T-DISPLAY-S3-AMOLED.pdf` shows `U3 = W25Q32` (4 MB); `T-Display-S3-AMOLED-Touch.pdf` shows `U3 = W25Q128JV` (16 MB); every README and store listing says 16 MB | both LilyGO schematics, retained here | **Unresolved.** Probably a stale early sheet. Settle with `esptool.py flash_id` |
| A2 | **What differs between V1.0 and V2.0?** LilyGO sells both, states nothing | store feed 2026-09-07; schematic diff | **Unresolved.** The schematic diff (regulator, display supply, flash) is *this record's inference from two sheets that are not labelled by revision* |
| A3 | **I²C pins.** `product_pins.h` gives SDA 3 / SCL 2; the older `pins_config.h` defines no I²C at all | `LilyGo-Display-IDF` @ `b1a1cc5` vs `T-Display-S3-AMOLED` @ `edd1333` | **Resolved in favour of `product_pins.h`** — it is newer and covers the touch variant |
| A4 | **GPIO21 does double duty**: `PIN_BUTTON_2` in `pins_config.h` **and** `BOARD_TOUCH_IRQ` in `product_pins.h` for the Touch variant | both vendor files | **Confirmed collision.** On a Touch board, GPIO21 is the touch interrupt; treating it as a button will misfire |
| A5 | **`AXPM65611` (`U5`) is unidentified.** No datasheet or manufacturer found | schematic text | **Open** — [`components/unidentified/lilygo-t-display-s3-family/axpm65611/`](../../../components/unidentified/lilygo-t-display-s3-family/axpm65611/README.md) |
| A6 | **`BV6802` (`U6`, V1.0) is unidentified.** Same family as the `BV6804` on the AMOLED Lite | schematic text | **Open** |
| A7 | **Arduino core version.** The base board pins 2.0.14; this board's library says **"V2.0.16 or later or latest"** | two vendor READMEs | **Both correct for their own board.** Do not carry the base board's pin over |

## Gaps

- Net connectivity not traced (same poppler blocker as the base board).
- **The V1.0/V2.0 schematics are not labelled by revision** — the mapping of sheet to revision
  in the README is inferred from which repository each lives in, and from the flash part.
- No hardware; nothing verified.
- The Camera Shield was not researched beyond its schematic and example directory.

## Negative results

- **`TFT_eSPI` cannot drive this panel.** It has no QSPI transport. The vendor's "TFT_eSPI
  examples" are Sprite-based. Recorded because the example names strongly imply otherwise.
- **There is no GPIO15 power gate**, unlike the base board. Searched `pins_config.h`,
  `product_pins.h` and the schematic text; no `PWR_EN`-equivalent net.
- **No microSD on this board.** The AMOLED **Plus** has one; this one does not.
