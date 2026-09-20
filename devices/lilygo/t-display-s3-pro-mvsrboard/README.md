# LilyGO T-Display-S3 Pro MVSRBoard

> **Stub record.** An accessory backplate for the
> [T-Display-S3 Pro](../t-display-s3-pro/README.md), not a standalone board.
> Store SKU `H751` "Only MVSR Board" **USD 10.20**; bundled with a mainboard as `K255`/`K255-01`
> at **USD 42.33**. In stock 2026-09-07.
> Repo `T-Display-S3-Pro-MVSRBoard` @ **`c9c1a76b263ee1696c9aefcd283086751bb9bf73`**,
> licence **GPL-3.0**. Research retrieved 2026-09-07. No hardware.

## What it is

LilyGO's own description, verbatim from the repository metadata:

> "The T-Display-S3-Pro-MVSRBoard is the backplate design for the T-Display-S3-Pro motherboard,
> featuring onboard speaker and microphone expansion with extremely low static current.
> Additionally, it includes vibration and RTC (Real-Time Clock) functions."

**MVSR** = **M**icrophone · **V**ibration · **S**peaker · **R**TC.

## Fitted parts

Read from the datasheets and schematics the Pro repository ships for it. **This is inference
from co-located documents, not from a traced schematic of the MVSRBoard itself.**

| Function | Part | Component record |
|---|---|---|
| Speaker amplifier | **MAX98357A** (I²S class-D) | [`analog-devices/max98357a`](../../../components/analog-devices/max98357a/README.md) |
| Microphone | **MEMSensing MSM261S4030H0R** (PDM) | [`memsensing/msm261s4030h0r`](../../../components/memsensing/msm261s4030h0r/README.md) |
| RTC | **NXP PCF85063ATL** | [`nxp/pcf85063a`](../../../components/nxp/pcf85063a/README.md) |
| Vibration | motor, part unidentified | [`generic/lra-motor`](../../../components/generic/lra-motor/README.md) *(family record)* |

## Sibling

**`T-Display-S3-Pro-MVSRLora`** — the same backplate **plus LoRa**, repo
`T-Display-S3-Pro-MVSRLora` @ `3457ffc0f9569858891d3692ce52f800947bd0c4`, GPL-3.0.
Not researched by this pass beyond its existence and description. Note that this, and the
separately sold **T-Display S3 Pro LR1121** (USD 65.29), are the only routes to LoRa anywhere
in the T-Display-S3 family — relevant to anyone who arrived here looking for Meshtastic.

## Artifacts

`artifacts/schematic/T-Display-S3-Pro-MVSRBoard_V1.0_20241109.pdf` — 1 184 978 B,
SHA-256 `5dda2c17f5e4c3ffe305b32b284380ca58d23670b45ced1b3b234107d9b31f09`, retrieved 2026-09-07
from the **Pro** repository at `08b8b2b`.

**An earlier sheet exists**, `T-Display-S3-Pro-MVSRBoard_V1.0_20240913.pdf` (1 173 823 B) — same
declared version `V1.0`, different date and different size. **Two documents, one version
number.** Not retrieved; recorded because the pair is itself evidence of the revision culture
described in [`../t-display-s3-shared/board-revision-drift.md`](../t-display-s3-shared/board-revision-drift.md).

## Gaps

**This is a stub.** Missing: a traced parts census from the MVSRBoard's own schematic, the pin
assignments (I²S clock/data, PDM, motor, RTC interrupt), the example catalogue, and any
verification that the parts above are the ones actually fitted rather than merely documented
alongside. The 2024-09-13 sheet was not retrieved and the two `V1.0` sheets were not diffed.
No hardware.
