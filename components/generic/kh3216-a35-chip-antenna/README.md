# KH3216-A35 — 2.4 GHz chip antenna

- **Manufacturer:** **Shenzhen Jinhangbiao Electronics Co., Ltd.** (深圳市金航标电子)
  — the specification document's own cover and footer; their site is given in the
  document footer as `http://www.BDS666.com`.
- **Part:** `KH3216-A35`
- **Document version:** **V1.2** (the specification's own version block)
- **Function:** surface-mount ceramic/chip antenna for 2.4 GHz ISM.
- **Research status:** identified from a **primary regulatory exhibit** —
  the antenna report filed with FCC ID `2BTR9-X4C`. Retrieved **2026-09-11**.

## Why this record exists

This is the **first named RF component in the Xteink family**. Nothing in any
firmware profile, teardown or vendor page names an antenna part; FCC antenna
reports do, because §15.203 requires the antenna to be identified.

## Specifications

Read from the manufacturer's specification document as filed. **Manufacturer's
own figures — not an independent measurement of the fitted part.**

| Parameter | Value |
|---|---|
| Package / designation | `3216` — nominally 3.2 × 1.6 mm SMD |
| Passband width | **100 MHz typ.** |
| **Peak gain** | **2.30 dBi** |
| Peak gain across band | 1.98 / **2.30** / 1.55 dBi (low / mid / high channel) |
| Average gain across band | −0.23 / −0.36 / −0.51 dBi |
| **Efficiency** | **70 % / 71.2 % / 69 %** |
| V.S.W.R. | **≤ 2.0** |
| Impedance | **50 Ω** |
| Polarization | Linear |
| Azimuth pattern | Omni-directional |
| Post-reliability tolerance | ±5 MHz bandwidth, ±0.1 dBi gain, ±0.1 VSWR |

The document also contains external dimensions and test-board pad dimensions, a
matching-circuit evaluation board, radiation patterns, reliability test
conditions, and reflow profile — **sections that were not transcribed** and are
available in the retained exhibit.

## Where the document is

**Not held as a standalone file.** It is embedded as the whole of the FCC antenna
exhibit, retained in the device record that caused the fetch:

| | |
|---|---|
| Path | [`devices/xteink/x4-classic/artifacts/certification/2BTR9-X4C-antenna-report.pdf`](../../../devices/xteink/x4-classic/artifacts/certification/2BTR9-X4C-antenna-report.pdf) |
| **SHA-256** | `720ce021f0d403a69e7095bb5ef29f393cb49a8ad4676f8e2652245ffbd355cb` |
| **Bytes** | **1,548,468** |
| Source URL | <https://fccid.io/2BTR9-X4C/Test-Report/Antenna-Report-9480914.pdf> |
| Retrieved | **2026-09-11** (UA `WhatsApp/2.23.20.0`; desktop-Chrome UA is served 403) |
| Validation | magic bytes `%PDF`; text layer cross-checked against the rendered heading |
| Redistribution status | `unknown` — third-party submission published by a US federal agency |
| Disposition | `repository`, unstaged |

**This is a deliberate exception to the usual filing rule.** A component
datasheet normally belongs in the component's own `artifacts/`. Here the document
is not a standalone datasheet — it is an FCC exhibit whose identity, integrity
and provenance are the *device's* certification record. Splitting it would create
a second copy of the same bytes under a different name. **The component record
points at the device's copy, with the hash, so the chain resolves from either
end.**

## No manufacturer portal was found

`BDS666.com` was not reached this pass. No independent copy of the `KH3216-A35`
specification was located outside the FCC filing. If the standalone document is
ever needed, the FCC exhibit is a complete copy of it.

## Used by

### Xteink X4 Classic (`2BTR9-X4C`)

→ [`devices/xteink/x4-classic/`](../../../devices/xteink/x4-classic/README.md)

The only internal antenna in the X4 Classic, feeding the ESP32-S3's 2.4 GHz
radio. The FCC grant covers **2412–2462 MHz** only — Wi-Fi 802.11b/g/n and BLE;
**no 5 GHz**, consistent with the SoC.

### Not the X4 Light

The sibling [`X4 Light`](../../../devices/xteink/x4-light/README.md)
(`2BTR9-X4L`, granted 2026-08-13) declares an internal antenna with a **maximum
gain of 5.19 dBi** — more than twice this part's 2.30 dBi. **That is a different
antenna**, and its part number is in an exhibit that was not fetched. Do not
assume the two devices share this component.

### Not established for the X3, X4 or X4 Pro

Each has its own FCC antenna report; **none was fetched**. Their antennas are
unidentified. The X4's FCC internal photographs show a **meandering PCB trace
antenna** rather than a chip part, so at least one device in this family does not
use a discrete antenna component at all.
