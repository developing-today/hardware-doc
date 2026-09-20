# T-Display-S3 — gaps, conflicts and unresolved identities

> Snapshot **2026-09-07**. Conflicts are recorded, not resolved by preference. Each entry says
> what evidence would settle it.

## Conflicts

### G1 — The "touch" and "no-touch" factory images are byte-identical

| | |
|---|---|
| Claim A | LilyGO ships `firmware/t-display-s3-touch-20230417_0x0.bin` and `firmware/t-display-s3-no-touch-20231013_0x0.bin` as distinct builds for distinct boards, dated six months apart |
| Claim B | They are one file. SHA-256 `f288081645eecf7bf6a17fd7b5bc2e724121d00cdc2099b5a5ea7db5107eb9fa`, 1 601 328 B, identical app descriptors including build timestamp |
| Evidence for B | **Measured locally 2026-09-07** (firsthand). Independently noticed by a user in [issue #212](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/212), 2024-01-02, where it was never addressed |
| Status | **Resolved in favour of B.** The filenames are wrong |
| Consequence | Flashing "no-touch" to a non-touch board yields a UI expecting touch |

### G2 — Charger part number vs shipping hardware

| | |
|---|---|
| Claim A | `schematic/T_Display_S3.pdf` (title block 2024-04-29) shows `U6 = TP4065`, `PROG` resistor `R9 = 2K`, sheet note `R13  IBAT (mA) = 580` |
| Claim B | A physical board carries a **5-lead TSOT-23 marked `65b311`**, and no SOP-8 is present — [issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230), 2024-03-02, firsthand PCB inspection with the package and marking quoted |
| Claim C | LilyGO's README says "The default charging current is **500mA**", citing that same issue |
| Notes | The issue author writes "TP4056" in prose while the schematic reads TP4065 — the two are different parts with similar programming equations. A 2 kΩ `PROG` resistor gives ≈ 580 mA on a TP4056 (I = 1200 V / R<sub>PROG</sub>), which matches the sheet note and **not** the 500 mA in the README |
| Status | **Unresolved, three ways.** The fitted part, the actual charge current, and whether the documented resistor swap applies are all open |
| What would settle it | A photograph of `U6` on a 2025-or-later board at readable magnification; or a measured charge current into a discharged cell; or a LilyGO statement |
| Do not | swap the charge-programming resistor on the strength of the schematic |

### G3 — Colour order: RGB or BGR?

| | |
|---|---|
| Claim A | `Setup206_LilyGo_T_Display_S3.h` @ `ec889e7`: `#define TFT_RGB_ORDER TFT_RGB` (with the BGR line commented out) |
| Claim B | ESPHome `mipi_spi` model `T-DISPLAY-S3`: `color_order=MODE_BGR` |
| Both agree on | colour **inversion** on (`TFT_INVERSION_ON` / `invert_colors=True`) |
| Status | **Unresolved.** Both libraries are in wide use and neither has a flood of "colours are wrong" reports, which suggests the two settings compensate for a difference elsewhere in each library's pipeline rather than describing the panel differently |
| What would settle it | Display a pure-red bitmap on one board with each library and photograph the result |
| Practical advice | If red and blue are swapped, flip this one setting; do not go looking for a hardware fault |

### G4 — Pixel clock: 16 MHz or 10 MHz?

`examples/factory/pin_config.h` @ `ec889e7` uses **16 MHz** with the comment *"Too low or too
high pixel clock may cause screen mosaic"*. ESPHome uses **10 MHz**. Neither is authoritative
for your board; the limit is set by the panel flex. **Not a defect** — recorded because people
copy the 16 MHz figure and then see tearing.

### G5 — Battery charge current: 500 mA or 580 mA?

README says 500 mA; the schematic note says 580 mA. See G2. Unresolved.

### G6 — Is GPIO16/17 pull-up fitment universal?

LilyGO confirmed the resistors exist on a non-touch board ([issue #313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313),
with photographs). **Whether every production run fits them is not established.** Measure your
board rather than assuming either way.

## Gaps — things this pass did not establish

| # | Gap | Why it is open | How to close it |
|---|---|---|---|
| K1 | **Schematic net connectivity was not traced.** Only designators, part strings and printed values were recovered from `T_Display_S3.pdf` | The PDF is an Altium export; the repo's [`tools/altium_pdf_netlist.py`](../../../tools/altium_pdf_netlist.py) needs `pdftotext -bbox` XML and **poppler was not installed on this host** | Install poppler-utils, run `pdftotext -bbox-layout` per page, then the existing tool. Everything else is already in place |
| K2 | **The battery divider ratio is inferred**, from two `100K %1` resistors plus the vendor multiplying by 2 | see K1 | as K1, or measure |
| K3 | **`Q4` (SI2307) gate control not traced** — so it is unknown whether the divider is disconnected in deep sleep, which matters for the sleep-current budget | see K1 | as K1 |
| K4 | **No independent performance measurement** of this board was located, and none was produced | No hardware available; no published benchmark found in 40+ searched sources | Measure full-screen fill rate at 10/16/20 MHz and deep-sleep current with and without a battery |
| K5 | **No product photography retained** | LilyGO's image rights were not established and no clearly licensed teardown was found | Ask LilyGO, or photograph a board |
| K6 | **CircuitPython support unknown** — no board definition found, but absence was not proven across all forks | search depth limited to the Adafruit repository and the CircuitPython board list | Search `adafruit/circuitpython/ports/espressif/boards` exhaustively |
| K7 | **The `AXPM65611` / `65b311` part is unidentified** | No datasheet found under either string; no manufacturer identifiable from primary evidence | See [`components/unidentified/lilygo-t-display-s3-family/axpm65611/`](../../../components/unidentified/lilygo-t-display-s3-family/axpm65611/README.md) |
| K8 | **No dated marketplace/clone price observations** beyond LilyGO's own store | AliExpress and Amazon listings were not sampled systematically in this pass | Sample ≥10 listings with dates, sellers and shipping, per [`guides/markets/clones-and-variants.md`](../../../guides/markets/clones-and-variants.md) |

## Negative results worth keeping

- **There is no USB-UART bridge on this board.** Searched the schematic designator census for
  CH340/CP210x/FTDI/CH343 — absent. The USB path is native ESP32-S3 only. Recorded because
  "which driver do I install" is a recurring question with the answer *none*.
- **There is no onboard microSD slot.** The `PIN_SD_*` defines in every `pin_config.h` describe
  the separately sold TF Shield. LilyGO's README says so explicitly. Recorded because the
  defines make it look otherwise.
- **There is no onboard IMU, no audio codec, no RTC and no battery-protection IC.** A full
  designator census of the single schematic sheet found `U1` (crystal), `U2` (ESP32-S3R8),
  `U3` (W25Q128JV), `U4` (AW9364DNR), `U5` (USB-C), `U6` (charger), `U7` (LDO) — and no `U8`.
  The gap in the sequence is itself the evidence that nothing else is fitted.
- **Meshtastic does not support this board**, and cannot: no LoRa radio. Searched
  `meshtastic/firmware` variants; no T-Display-S3 target exists.
- **WLED does not support this board.** `wled/WLED` carries a `TTGO-T-Display` usermod for the
  *ESP32* predecessor only; no S3 variant.
