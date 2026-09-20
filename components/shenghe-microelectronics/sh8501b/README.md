# Shenghe Microelectronics SH8501B (SH8501B0)

- **Category:** AMOLED display driver IC — **240 RGB × n**, 16.7 M colours.
- **Manufacturer:** **SHENGHE MICRO ELECTRONICS**, established from the datasheet cover.
- **Retrieved:** 2026-09-07
- **Sibling:** [`sh8601z`](../sh8601z/README.md)

The display driver of the **LilyGO T-Display AMOLED Lite (1.47″)**, 194 × 368 — and the reason
that board needs a level shifter.

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **SH8501B** (LilyGO's filename says `SH8501B0`) |
| Cover page text | "CONFIDENTIAL · SHENGHE MICRO ELECTRONICS · 240 RGB x … / 16.7M color · AMOLED Display Driver IC · Datasheet · SH8501B" |
| Local artifact | [`artifacts/sh8501b0-datasheet-lilygo-mirror.pdf`](artifacts/sh8501b0-datasheet-lilygo-mirror.pdf) — 4 412 013 B, SHA-256 `663d767850d7db71252c62f9de709cbaf278a88d25048aa168f6cb5586425b41` |
| Mirror source | `Xinyuan-LilyGO/LilyGo-AMOLED-Series` → `datasheet/SH8501B0 DataSheet.pdf` @ `6d1dc008b94578cc34ba4a0f3b223dd808ca963f` |
| Marked | **CONFIDENTIAL** |
| Licence | Shenghe copyright, marked confidential; repository MIT does not cover it. **Redistribution status: `prohibited` on the face of the document** — should remain **unstaged** |

## 2. The 1.8 V problem

On the T-Display AMOLED Lite, every signal between the ESP32-S3 and this controller crosses an
**RS0108YTQC20 8-bit level translator** (`U2`). The schematic's net names make it explicit:
`AM_SPI_CSX`/`AM_SPI_CSX-1V8`, `AM_SPI_SCL`/`AM_SPI_SCL_1V8`, `AM_SPI_SD0..3`/`…_1V8`,
`TE`/`TE_1V8`, `TP_INT`/`TP_INT_1V8`.

**The panel side runs at 1.8 V.** That is not true of any other display in the family, and it
has consequences:

- Extra propagation delay and reduced maximum QSPI clock versus a direct 3.3 V link.
- The board needs an **AXP2101 PMU** partly to generate the 1.8 V rail — which is why the Lite
  is the only board in the family with a full PMU.
- Panel power sequencing is more involved, and is plausibly why LilyGO's own figures give the
  Lite a **1.1 mA** deep-sleep current against 230 µA for the 1.91″/2.41″ boards, and
  **timer-only** wake instead of external GPIO wake.

## 3. What was not verified

Cover and table of contents only. **No register, timing or electrical value is transcribed.**
Extraction method and its pitfalls: [`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md).

## 4. Used by

### LilyGO T-Display AMOLED Lite (1.47″)
→ [`devices/lilygo/t-display-amoled-lite`](../../../devices/lilygo/t-display-amoled-lite/README.md)

194 × 368, 450 nits. QSPI via the level shifter: `DISP_CS` GPIO4, `SCK` GPIO5,
`DATA0..3` GPIO 7/10/11/12, `RESET` GPIO40, `TE` GPIO6. Touch is a separate
[Chipsemi CHSC5816](../../chipsemi/chsc5816/README.md); PMU is an
[X-Powers AXP2101](../../x-powers/axp2101/README.md).
**Vendor states this board does not support hardware screen rotation.**
