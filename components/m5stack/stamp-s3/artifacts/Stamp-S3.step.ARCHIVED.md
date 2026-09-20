# ARCHIVED — `Stamp-S3.step`

STEP (AP214) solid model of the M5Stack **Stamp-S3** module, published by M5Stack in the
`m5stack/M5_Hardware` KiCad library so the module can be placed in a host-board 3D view.

| Field | Value |
|---|---|
| Original repository path | `components/m5stack/stamp-s3/artifacts/Stamp-S3.step` |
| Archived to | `archive/components/m5stack/stamp-s3/artifacts/Stamp-S3.step` |
| SHA-256 | `7f29337cdac90c80400897f52795ed0709548d4e74dc4436efb3e4f3873d2ebf` |
| Byte size | 2 904 597 |
| Media type | ISO 10303-21 STEP text file |
| Retrieved | 2026-09-04 |
| Upstream repository | <https://github.com/m5stack/M5_Hardware> |
| Path in repository | `KiCad/3D/M5Stack.3dshapes/Stamp-S3.step` |
| Repository HEAD when fetched | `a240115c94b19ecf647f229c47fa9a8ce46ccdc4` (authored 2026-08-17T07:36:01Z) |
| Release/tag | none — the repository publishes no releases |
| Licence | **unknown** — `m5stack/M5_Hardware` carries no `LICENSE` file (checked 2026-09-04) |
| Redistribution status | `unknown` |
| Disposition | `repository` → archived for size |
| Why moved | Size, and it is **derived**: a mechanical export of a board M5Stack also ships as `Stamp-S3.stl` (158 484 bytes, retained in-repo beside this placeholder) and as a dimension drawing. The STL is sufficient for enclosure clearance work; the STEP matters only for parametric CAD. |
| Reproducible? | Yes — re-fetchable byte-for-byte from a pinned commit (below) |
| Reacquisition | `automatic` |

## Reacquisition

Two independent hosts:

1. **GitHub raw, pinned to the commit above** (preferred — immutable):
   ```bash
   curl -fSL -o Stamp-S3.step \
     'https://raw.githubusercontent.com/m5stack/M5_Hardware/a240115c94b19ecf647f229c47fa9a8ce46ccdc4/KiCad/3D/M5Stack.3dshapes/Stamp-S3.step'
   ```
2. **GitHub API tarball of the whole library** (survives a raw-CDN outage):
   ```bash
   curl -fSL -H "Authorization: Bearer $(gh auth token)" \
     -o M5_Hardware.tar.gz \
     'https://api.github.com/repos/m5stack/M5_Hardware/tarball/a240115c94b19ecf647f229c47fa9a8ce46ccdc4'
   ```
3. Branch link (moves — use only if the commit is gone):
   <https://github.com/m5stack/M5_Hardware/blob/master/KiCad/3D/M5Stack.3dshapes/Stamp-S3.step>

## Important: there is no `Stamp-S3A.step`

`m5stack/M5_Hardware` at the commit above publishes **exactly one** Stamp-S3-family STEP
model and **no Stamp-S3A footprint**. It does publish two STL files —
`Products/S007_Stamp-S3/Structures/Stamp-S3.stl` and
`Products/S007-V033_Stamp-S3A/Structures/Stamp-S3A.stl` — and those two files are
**byte-identical** (both SHA-256 `f72c1af2d42930fc57a3db1bd3282568a3952095f77539016a12437d59d7df5d`).

That is evidence, not proof, that the S3A is mechanically and footprint-compatible with
the S3. It sits against the vendor's own specification tables, which give the S3 as
24.0 × 18.0 × 4.7 mm and the S3A as 26.0 × 18.0 × 4.7 mm. The conflict is recorded in
[`../../stamp-s3a/README.md`](../../stamp-s3a/README.md) §"Mechanical" and in
[`devices/m5stack/dinmeter/gaps-and-conflicts.md`](../../../../devices/m5stack/dinmeter/gaps-and-conflicts.md).

## Consumers

- Component record: [`components/m5stack/stamp-s3/README.md`](../README.md)
- Device that caused the fetch: [`devices/m5stack/dinmeter/README.md`](../../../../devices/m5stack/dinmeter/README.md) (fits `Stamp-S3-SMD` as `M1`)
- Related: [`devices/m5stack/dinmeter-v1.1/README.md`](../../../../devices/m5stack/dinmeter-v1.1/README.md)
