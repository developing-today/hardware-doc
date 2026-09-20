# Display driver datasheets are filed under `components/`, not here

`ek79007ad-datasheet.pdf`, `ek73217bcga-datasheet.pdf` and `st7789vw-datasheet.pdf` used to sit in
this directory as copies. They are **part-level documents** — the same PDFs apply to any board
using those driver ICs — so they now live once under `components/`, and the Espressif boards that
share this directory cite them.

Moved **2026-08-30**. The bytes are unchanged and still in the repository.

| Driver IC | Canonical file | Bytes | SHA-256 |
|---|---|---:|---|
| **Fitipower EK79007AD** | [`components/fitipower/ek79007ad/artifacts/ek79007ad-datasheet.pdf`](../../../components/fitipower/ek79007ad/artifacts/ek79007ad-datasheet.pdf) | 3,723,767 | `2dbab767e040959f1c7ce1ae3af4e65c888e04d88b066bcb1f3bddee6c8287a4` |
| **Fitipower EK73217BCGA** | [`components/fitipower/ek73217bcga/artifacts/ek73217bcga-datasheet.pdf`](../../../components/fitipower/ek73217bcga/artifacts/ek73217bcga-datasheet.pdf) | 1,571,109 | `bd4ec28f5b11ab95536da6cf6162af18ff8d1ec34fa19379444eb5c0e8f7763a` |
| **Sitronix ST7789VW** | [`components/sitronix/st7789vw/artifacts/st7789vw-datasheet.pdf`](../../../components/sitronix/st7789vw/artifacts/st7789vw-datasheet.pdf) | 3,135,599 | `1f9e956057e3909c0714bdab9e682205e03cf52adefd5b4a01093fa3167d398b` |

Component records, which carry the register-level detail and cross-device usage:

- [`components/fitipower/ek79007ad`](../../../components/fitipower/ek79007ad/README.md)
- [`components/fitipower/ek73217bcga`](../../../components/fitipower/ek73217bcga/README.md)
- [`components/sitronix/st7789vw`](../../../components/sitronix/st7789vw/README.md)

## Why this directory still exists

`devices/espressif/shared-artifacts/` is legitimately shared — it holds material common to several
Espressif evaluation boards that is **board-level**, such as the camera and LCD adapter-board
reference designs, sub-board schematics, assembly drawings and layouts. Those stay here.

The distinction now applied consistently:

| Belongs here | Belongs in `components/` |
|---|---|
| Adapter-board reference designs, sub-board schematics, assembly drawings, connector specs | Datasheets for a *part* that any board might use |

A part datasheet filed here would have to be duplicated for every other board using the same
part — which is exactly what had happened.
