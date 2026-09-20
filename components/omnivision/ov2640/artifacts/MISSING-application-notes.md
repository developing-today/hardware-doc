# MISSING: OV2640 camera module software application notes

**This document is not held in this repository, despite a file having claimed otherwise.**

## What happened

`components/omnivision/ov2640/artifacts/` contained a file named
`ov2640-camera-module-software-application-notes.pdf`. It was **byte-identical** to
`ov2640-datasheet-v2.2.pdf` sitting beside it — same 676,989 bytes, same SHA-256
`4460f2f13b761eae4d1778a28f6d86db50a54e77b96cf8af9ddb2fa3168feab7`.

The application notes were therefore **never actually obtained**. The retrieval that was supposed
to fetch them returned the datasheet instead — most likely a vendor or mirror serving the wrong
file for the advertised link — and the result was saved under the intended name without the
content being checked.

Detected **2026-08-30** by a repository-wide byte-identical duplicate scan. The misnamed file has
been removed; nothing unique was lost, because its bytes are still present as the datasheet.

> The failure worth remembering is not the bad download — that happens. It is that a file was
> **named after what was requested rather than what arrived**, which made a missing document look
> like a held one. A hash check at retrieval time, comparing against files already in the same
> directory, would have caught it immediately.

## What this document actually is

OmniVision's *OV2640 Camera Module Software Application Notes* is a separate publication from the
datasheet. It covers what the datasheet largely omits and what people usually need:

- Recommended initialisation register sequences for common resolutions
- JPEG mode configuration and quality control
- Windowing, scaling and the DSP register bank
- Auto-exposure / auto-white-balance tuning guidance

The datasheet documents the register *map*; the application notes document the register
*sequences*. Anything in this repository describing OV2640 initialisation ordering is therefore
**not** sourced from an OmniVision application note held here.

## Reacquisition

Not available from OmniVision directly — they do not publish OV2640 documentation openly. It
circulates through module vendors and mirrors. Candidate routes, none verified at the time of
writing:

```bash
# Commonly mirrored alongside the datasheet by module vendors and on documentation aggregators.
# VERIFY THE HASH DIFFERS FROM THE DATASHEET before saving:
#   sha256sum <downloaded>.pdf
#   # must NOT be 4460f2f13b761eae4d1778a28f6d86db50a54e77b96cf8af9ddb2fa3168feab7
```

- Search for `OV2640 Camera Module Software Application Notes` plus `filetype:pdf`
- ArduCAM and M5Stack documentation repositories have historically mirrored OmniVision app notes
- The Espressif `esp32-camera` driver source encodes much of the same initialisation knowledge in
  `sensors/ov2640.c` and its register tables, and is a legitimate substitute for most purposes

## Practical impact

Low. The register sequences this document would provide are, in practice, already embodied in the
`esp32-camera` driver used by every board in this repository that carries an OV2640. The gap
matters only if you are writing a driver from scratch or debugging an initialisation sequence
against the vendor's own recommendations.

## Related

- [`ov2640-datasheet-v2.2.pdf`](ov2640-datasheet-v2.2.pdf) — the document that *is* held
- [`../README.md`](../README.md) — the OV2640 component record
- [`components/omnivision/ov5640/artifacts/ov5640-software-application-notes.pdf`](../../ov5640/artifacts/ov5640-software-application-notes.pdf) — the equivalent OV5640 document, which **is** genuinely held, and is a useful model for what the OV2640 one would contain
