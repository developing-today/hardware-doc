# Hynitron CST3530

- **Category:** capacitive touch controller, I²C slave.
- **Manufacturer:** Hynitron Microelectronics.
- **Retrieved:** 2026-09-07
- **Siblings here:** [`cst816d`](../cst816d/README.md) · [`cst328`](../cst328/README.md) ·
  [`cst226se`](../cst226se/README.md)

The touch controller on **later production** of the **LilyGO T-Display-S3 Long**, where it
replaces or supplements the AXS15231B's integrated touch.

## 1. Identity and artifact

| Property | Value |
|---|---|
| Part | **CST3530** |
| Datasheet | `CST3530数据手册V1.0(1).pdf` — Chinese, **V1.0** |
| Local artifact | [`artifacts/cst3530-datasheet-cn-v1.0-lilygo-mirror.pdf`](artifacts/cst3530-datasheet-cn-v1.0-lilygo-mirror.pdf) — 781 716 B, SHA-256 `3a103cef456f696f8861593871e2cf94d71982ff5f0791384ef190fb6b9baca7` |
| Mirror source | `Xinyuan-LilyGO/T-Display-S3-Long` → `datasheet/CST3530数据手册V1.0(1).pdf` @ `37a7e83af79a98bb395012200f811777e52b9cfc` |
| Language | Chinese only; no English version located. **Primary source in its own right** |
| Related document in the same repo | `CST66xx_Application Note_en_V1.01.pdf` — an **English** application note for a *different* Hynitron family, shipped alongside. Whether it applies to the CST3530 is **unknown** |
| Licence | Hynitron copyright. **The T-Display-S3-Long repository declares no licence at all**, so redistribution status is doubly unknown |

## 2. How you know a board has it

The `T-Display-S3-Long` repository's **default branch is `T-Display-S3-Long-cst3530`** and it
ships **two factory images**:

| Image | Bytes |
|---|---|
| `firmware/factory.bin` | 1 815 872 |
| `firmware/factory-cst3530.bin` | 2 158 624 |

plus `examples/cst3530_touch/` beside the original AXS15231B touch path. **Flash `factory.bin`;
if touch does not respond, flash `factory-cst3530.bin`.** That is the only identification
procedure that exists — LilyGO published no statement about the change.

## 3. What was not verified

The datasheet was **not read**; no I²C address, register or timing value is transcribed here.
The I²C address is therefore **unknown** — do not assume it matches the AXS15231B's `0x3B`.
An I²C scan on the Long's bus (SDA GPIO15 / SCL GPIO10) will find it.

## 4. Gaps

- Register map, address and protocol: unknown.
- Whether the CST3530 **replaces** the AXS15231B's integrated touch or **supplements** it is
  unknown. Both readings are consistent with a separate example and a separate firmware image.
- Whether the English `CST66xx` application note applies.
- Not verified on hardware.

## 5. Used by

### LilyGO T-Display-S3 Long (later production)
→ [`devices/lilygo/t-display-s3-long`](../../../devices/lilygo/t-display-s3-long/README.md)

I²C on **GPIO15 (SDA) / GPIO10 (SCL)**; the board also defines `TP_RST` GPIO2 and `TP_IRQ`
GPIO11. Note the vendor's `pins_config.h` has `PIN_BAT_VOLT 2` colliding with `TP_RST 2` —
see the device record's conflict L1.
Revision detail: [R5](../../../devices/lilygo/t-display-s3-shared/board-revision-drift.md#r5--t-display-s3-long-cst3530-touch-appears-mid-life-in-a-branch).
