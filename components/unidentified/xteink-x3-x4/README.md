# Unidentified parts — Xteink X3 / X4 board family

Parts fitted to the ESP32-C3 Xteink boards that are **evidenced but not
identified to a part number**. Scoped to this device family so that unrelated
unknowns never collapse into one record, per the research method.

| Record | What is known | What is missing |
|---|---|---|
| [`spi-nor-flash-128mbit-puya`](spi-nor-flash-128mbit-puya/README.md) | Maker (Puya), density (128 Mbit / 16 MB), two independent teardowns | Part number |
| [`rtc-ds-series`](rtc-ds-series/README.md) | Address 0x68, "DS-series" | **Which DS part — three sources disagree** |
| [`nfc-tag-iso14443a`](nfc-tag-iso14443a/README.md) | Passive, writable, ISO 14443A, **purpose now established** | Part number, tag type |
| [`battery-charger-tp4056-class`](battery-charger-tp4056-class/README.md) | "TP4056-like" | Actual part |

**None of these has been promoted from candidate to finding.** Each record states
exactly what evidence would resolve it. In every case that evidence is cheap — a
legible top-marking photograph, or one I²C register read.

The boards themselves: [X3](../../../devices/xteink/x3/README.md) ·
[X4](../../../devices/xteink/x4/README.md)

---

## Round 2 — 2026-09-11: the evidence that resolves these now exists and is in this repository

**No line above was altered.** None of the four parts is resolved by this pass.
What has changed is that the **kind of evidence that resolves them has become
available**, and it is retained here rather than hypothetical.

### FCC internal photographs, public and retained

| Device | Exhibit | Public since | Local path | Images | SHA-256 |
|---|---|---|---|---|---|
| **X3** | Internal Photos | **2026-06-24** | [`devices/xteink/x3/artifacts/certification/2BTR9-XTEINKX3-internal-photos.pdf`](../../../devices/xteink/x3/artifacts/certification/2BTR9-XTEINKX3-internal-photos.pdf) | **16** | `b3affd56115e9c3e49428f9727ba194c0eec6705ddd0b039fd9b4ce28b430a45` |
| **X4** | Internal Photos | **2026-07-04** | [`devices/xteink/x4/artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf`](../../../devices/xteink/x4/artifacts/certification/2BTR9-XTEINKX4-internal-photos.pdf) | **15** | `fd1623a7c9df42ba8140cea6d2618722726c1f442209c02f8229c1b50658f370` |

Both were fetched from `fccid.io` on 2026-09-11 with UA `WhatsApp/2.23.20.0`
(a desktop-Chrome UA is served 403) and validated `%PDF`. Images are extractable
with `nix-shell -p poppler-utils --run 'pdfimages -png in.pdf out/p'`.

**These are regulatory photographs of the board as shipped**, taken under an
obligation to show the assembly, and at higher resolution than the community
teardowns already archived for the X3.

### Status of each part, unchanged

| Part | Status | What these photographs could give it |
|---|---|---|
| `flash` | unresolved | The 8-pin SOIC package is **visible** in at least one X4 image. A readable top marking would name the manufacturer and density directly |
| `rtc` | unresolved — **and it is a live 3-way conflict**: `DS3231` (firmware) vs `DS1307` (teardown caption) vs "DS-series" (Chinese BOM) | A readable top marking would **settle a conflict that has stood since 2026-09-04**. This is the single highest-value read in the set |
| `nfc-tag` | unresolved (X3 only) | The tag is an inlay, likely under the rear shell — may not appear |
| `charger` | unresolved | A readable marking on the charge-path IC |

### One observation, offered as an observation and not as an identification

A **single** image from the X4 set (`p-007`) was opened. It shows a green PCB
with a meandering trace antenna, a shielded area containing an Espressif-logo
QFN part, a **40.000 MHz crystal**, an **8-pin SOIC** package, a USB-C
receptacle on an adjoining board section, and two FPC connectors of different
widths.

**No top marking was transcribed and no part was identified.** Doing that
properly needs the full 31 images across both devices opened at native
resolution, cross-referenced against the reference designators, and read
carefully — work this pass did not do and deliberately did not guess at.

**The next session's cheapest high-value task in the whole Xteink tree is to read
these 31 images.** Four unidentified parts and one three-way conflict are waiting
on it, and the files are already here and hashed.
