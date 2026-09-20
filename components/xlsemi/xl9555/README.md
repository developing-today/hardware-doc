# XL9555 — 16-bit I²C GPIO expander

- **Category:** I²C to 16-bit parallel I/O expander, interrupt-capable
- **Manufacturer:** filed here under **XLSEMI** to match this repository's existing
  `components/xlsemi/xl9555/artifacts/` directory, which already held
  `xl9555-datasheet-rev-2.3.pdf` before this pass. *Attribution caution:* the XL9555 is
  variously attributed to XLSEMI and to Shenzhen XINLUDA; it is functionally a **TCA9555 /
  PCA9555 clone**. Verify against the retained datasheet rather than against the folder name.
- **Research status:** this README is new (2026-09-04); the datasheet artifact beside it predates
  this pass and was **not** modified.
- **Retrieved:** 2026-09-04

## 1. Core facts

| Property | Value |
|---|---|
| I/O | **16** bidirectional pins, two 8-bit ports (`P0.x`, `P1.x`) |
| Interface | I²C, **7-bit address `0x20` – `0x27`** selected by `A0`/`A1`/`A2` |
| Interrupt | open-drain `INT`, asserted on input change |
| Registers | `0x00/0x01` input, `0x02/0x03` output, `0x04/0x05` polarity inversion, `0x06/0x07` configuration (1 = input) |
| Compatible with | TCA9555, PCA9555, and the Linux `pca953x` driver family |
| Local artifact | [`artifacts/xl9555-datasheet-rev-2.3.pdf`](artifacts/xl9555-datasheet-rev-2.3.pdf) |

**Address ambiguity is the operational hazard.** Eight possible addresses in a contiguous block
means an I²C scan cannot distinguish an XL9555 from anything else in `0x20–0x27`, and the strap
resistors are frequently changed between board revisions without a note.

## 2. Used By

### [LilyGO T-Display K230 Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

On the **nRF9151 keyboard base board**, I²C4 (`GPIO46` SCL / `GPIO47` SDA), used for LED and
keyboard-base support alongside the [TCA8418](../../texas-instruments/tca8418/README.md)
keyboard scanner, [BQ25896](../../texas-instruments/bq25896/README.md) charger and
[BQ27220](../../texas-instruments/bq27220/README.md) gauge.

LilyGO does not pin the address. Their pin map says: "7-bit I²C address can be **`0x20`-`0x27`**;
**software probes and caches the detected address**", and the main README lists the address as
depending on "hardware strap/version". That is an unusually honest vendor statement and it
means **any firmware for this board must probe rather than hard-code.** Treat a hard-coded
`0x20` as a bug.

## 3. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | Bus, address range, probe-and-cache behaviour |
| S2 | `xl9555-datasheet-rev-2.3.pdf` | XLSEMI | primary | datasheet | retained locally, pre-existing artifact | before 2026-09-04 | Register map, addressing |
