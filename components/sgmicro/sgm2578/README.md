# SG Micro SGM2578 — load switch

- **Category:** integrated load switch (high-side power switch with enable).
- **Manufacturer:** **SG Micro Corp** — inferred from the `SGM` prefix, consistent with the
  other SG Micro parts already documented in this repository
  ([`sgm2036-3.3`](../sgm2036-3.3/README.md), [`sgm40567`](../sgm40567/README.md),
  [`sgm6029`](../sgm6029/README.md)). **No datasheet located** in this pass.
- **Research status:** ⚠ **Schematic-only.**
- **Retrieved:** 2026-09-04

The rear-LCD backlight power switch inside the **M5Stack Stamp-S3** module (`U2`, board rev
v0.2). Replaced by an [Awinic AW35122FDR](../../awinic/aw35122/README.md) on the
[Stamp-S3A](../../m5stack/stamp-s3a/README.md).

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| Part string | **`SGM2578`** | `Sch_M5StampS3_v0.2.pdf`, value text at (520.5, 121.4), associated with `U2` |
| Second value string | **`WS4622C-4/TR`** | same symbol, at (528.4, 121.4)+ — an alternate/second-source part in the same Altium parameter block |
| Balls/pins seen | `A1` (VOUT), `A2` (VIN), `B1`, `B2` (EN) | `PIU20A1`, `PIU20A2`, `PIU20B1`, `PIU20B2` |
| Input | `VDD_3V3` | schematic |
| Enable | `DISP_BL` = ESP32-S3 **GPIO38** (`U1` pad 43) | schematic |
| Output | rear LCD-FPC backlight rail | schematic |
| Decoupling | `C3` 100 nF/25 V | schematic |

Current rating, on-resistance, slew control, reverse-current blocking and quiescent current are
**unknown**. No chip-marking confirmation.

**Second-source note.** Altium symbols commonly carry a `Comment` and a manufacturer-part
parameter; here two distinct part strings render side by side. `WS4622C-4/TR` reads as a Will
Semiconductor (WS) alternate. Which one is actually fitted on a given production unit is
**not established** — only a teardown would settle it. This is recorded rather than resolved.

## 2. Why it matters

On the Stamp-S3 this switch gates **only** the rear FPC backlight rail. The WS2812B-2020 RGB
LED (`U3`) sits on the unswitched `VDD_3V3`.

On the Stamp-S3A the equivalent switch is an AW35122FDR whose output net is `BL_3V3`, and the
RGB LED was **moved onto it**. That single net change is the whole firmware-visible difference
between the two modules. See
[`components/m5stack/stamp-s3a/README.md` §3](../../m5stack/stamp-s3a/README.md#3-change-1--the-rgb-led-is-no-longer-always-powered-firmware-visible).

## 3. Artifacts

**None.** Establishing evidence:
[`components/m5stack/stamp-s3/artifacts/Sch_M5StampS3_v0.2.pdf`](../../m5stack/stamp-s3/artifacts/Sch_M5StampS3_v0.2.pdf).

---

## Used By

### M5Stack Stamp-S3 (SKU S007), board rev v0.2

`U2`. → [`components/m5stack/stamp-s3/README.md`](../../m5stack/stamp-s3/README.md)

### Reached from these devices

- [M5Stack DinMeter (K134)](../../../devices/m5stack/dinmeter/README.md) — inside its Stamp-S3.
  Note that the DinMeter carrier does **not** use the Stamp's rear FPC or GPIO38 at all: it
  drives its own panel backlight from GPIO9 through its own AW35122FDR (`U6`). So on the
  DinMeter this part is present but idle.
