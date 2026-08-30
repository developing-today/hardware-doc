# Archived firmware binaries and image payloads — reacquisition record

**9 files, 7,115,995 bytes (6.79 MiB)** moved out of the repository on **2026-08-30**. Not deleted.

> **These files are absent from the repository.** They are not symlinks and not placeholders-in-place —
> the paths simply do not exist here any more. This record is the only thing standing in for them,
> which is why it carries a SHA-256, a byte count and a pinned reacquisition URL for every file.
>
> The archive copy is a **convenience for whoever holds it, not part of the contract**: it lives
> outside the repository at a machine-local path, so nothing here may depend on it.

This took the vendored library from **8.5 MiB to 4.2 MiB while removing no Python at all.**

## What was archived, and why

Two categories, both non-source:

**1. Prebuilt firmware for other Inkplate models — 3,457,040 bytes.**
`inkplate-firmware.bin` and `inkplate13spectra-firmware.bin` are compiled MicroPython images.
**Neither is for the Inkplate 5.** There is no `inkplate5` firmware in this tree at all — they
target the generic Inkplate build and the Inkplate 13 Spectra. They were 41 % of the tree and are
of no use to this device record.

**2. Demo photographs — 3,658,955 bytes.** `displayimagesd/image.jpg` under six *other* boards'
example directories, plus `docs/inkplate_image.jpg`. Note that several are byte-identical to each
other across boards — upstream ships the same demo photo repeatedly.

**Every `.py` file was kept**, including all 230 board and example scripts. The three files that
authored documentation actually cites — `boards/inkplate5/inkplate5.py`,
`shared/drivers/pcal6416a.py`, `shared/drivers/tps65186.py` — are untouched, as is every path
around them.

**Checked before archiving:** each file was tested by full relative path, as a fixed string,
against all authored Markdown outside this tree. **Zero were cited.**

## Reacquisition

| | |
|---|---|
| Repository | `SolderedElectronics/Inkplate-micropython` |
| URL | <https://github.com/SolderedElectronics/Inkplate-micropython> |
| Commit | **`4a2b2926`** (2026-08-10) |
| Licence | **MIT** |
| Source ID | **IP5-20** in [`sources.md`](../../../sources.md) |

```bash
git clone https://github.com/SolderedElectronics/Inkplate-micropython
git -C Inkplate-micropython checkout 4a2b2926
```

Single file at the pinned commit:

```bash
curl -fsSL "https://raw.githubusercontent.com/SolderedElectronics/Inkplate-micropython/4a2b2926/<path-from-table>"
```

A public MIT-licensed GitHub repository at a pinned commit — low reacquisition risk.

Archive root:
`archive/hardware-doc/devices/soldered-electronics/inkplate-5/artifacts/source-snapshots/Inkplate-micropython/`

## Restoring a file

Re-fetch it from the pinned upstream in the Reacquisition section above and verify against the
SHA-256 in the table. If you happen to hold the local archive, copying from the archive root shown
above is faster and gives the identical bytes.

## Note on modifying a vendored snapshot

Removing files is a **local modification**: a fresh upstream clone at the pinned commit has these
files present. Reconcile against the table above before concluding that a diff means something.

## Contents

| File | Bytes | SHA-256 |
|---|---:|---|
| `firmware/inkplate13spectra-firmware.bin` | 1,810,960 | `bdcf28def25887e4b15ef30214d2cfd0717a4c63f24a02e6e034db4fbe837f91` |
| `firmware/inkplate-firmware.bin` | 1,646,080 | `0f541c9a712a796017ca823c3281f9010352510599bbf62ff034c2c091582577` |
| `examples/inkplate13spectra/displayimagesd/image.jpg` | 1,029,704 | `e9a06f811a20a1a6756e4889370c341897f2700faa3b9553586ac658debf1611` |
| `examples/inkplate7spectra/displayimagesd/image.jpg` | 1,029,704 | `e9a06f811a20a1a6756e4889370c341897f2700faa3b9553586ac658debf1611` |
| `examples/inkplate6flick/displayimagesd/image.jpg` | 413,693 | `e643133dd5ab3aa8185dd9928ce5e97c8aaddd652ac67249c11f890e1a259d93` |
| `docs/inkplate_image.jpg` | 392,860 | `82dcc2109bbccfab32adb447e7031ed8a376ed9063df5afd560525105f9f5037` |
| `examples/inkplate10/displayimagesd/image.jpg` | 272,552 | `4eb432d2765501159ce08be5deca7e5f2d7e8733884802614c71f22f8703257c` |
| `examples/inkplate6/displayimagesd/image.jpg` | 260,221 | `76587eda5cffcafd2edc0d7e17a445b0879e29493ea7148e7dc4c7418320752a` |
| `examples/inkplate6color/displayimagesd/image.jpg` | 260,221 | `76587eda5cffcafd2edc0d7e17a445b0879e29493ea7148e7dc4c7418320752a` |
