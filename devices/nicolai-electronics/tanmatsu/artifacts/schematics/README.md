# Tanmatsu KiCad design source

Source: **`Nicolai-Electronics/tanmatsu-hardware`** @ `640805dd` (2026-02-25). Licence
**CERN-OHL-P** (`LICENSE-CERN-OHL-P`); branding, logos and artwork are **explicitly excluded** and
remain all-rights-reserved. Cloned 2026-08-24.

| Path | Added | Contents |
|---|---|---|
| `tanmatsu-schematic.pdf` | 2026-08-24 | Exported schematic, 1 153 359 B |
| `kicad/` | 2026-08-24 | 11 schematic sheets, `tanmatsu.kicad_pcb`, `tanmatsu.kicad_pro` |
| `kicad/library/` | **2026-09-20** | **75 custom symbols and footprints** — see below |
| `kicad/fp-lib-table`, `kicad/sym-lib-table` | **2026-09-20** | Library tables the project needs to resolve `library/` |
| `design/` | **2026-09-20** | Board outline and the coprocessor latch-circuit figure |
| `hardware-repo-README.md`, `LICENSE-CERN-OHL-P` | 2026-08-24 | Upstream README and licence |

## Why `library/` was added

Until 2026-09-20 this directory held the sheets and the PCB but **not the symbol and footprint
libraries they reference**, nor the `fp-lib-table` / `sym-lib-table` that bind them. The published
"full KiCad source" therefore could not be opened without re-cloning upstream — every custom part
(`esp32-p4`, `ch32v203`, `ch32v003`, `ES8156`, `BMI270`, `BHI360`, `keyboard`, `flashchip`,
`custom-power`, the Hirose and JST connectors, the keyboard footprint) would resolve as a broken
symbol.

The 75 files copied are the `.kicad_sym`, `.kicad_mod` and bundled `LICENSE` files only — **936 KB**.

### What was deliberately **not** copied

`library/` upstream is **74 MB**; the remaining ~73 MB is `.step` and `.wrl` **3D package meshes**
— generic LCSC package shapes (`SOT-23-3P…`, `QFN-24…`, `USB-C_SMD-TYPE-C-31-M-12`,
`ESP32-C6-WROOM-1.STEP`, …). They are:

- **not board-specific** — generic package geometry shared across countless designs,
- **not needed** to open, edit, netlist or fabricate the board — KiCad renders placeholders,
- **carriers of no electrical information** at all.

They remain in `scratch/tanmatsu/sources/tanmatsu-hardware/library/`, reacquirable from
`Nicolai-Electronics/tanmatsu-hardware` @ `640805dd`. This is the "regenerable / off-topic" case
from the skill's archiving rules; they were not even worth a placeholder each.

Also left in scratch: `production/tanmatsu.zip` (1 670 984 B, Gerbers — regenerable from the
retained `.kicad_pcb`, and [`SIZE-AUDIT.md`](../../../../../SIZE-AUDIT.md) §6 already rules Gerbers
prunable), `fabrication.kicad_jobset`, `fabrication-toolkit-options.json` and `.gitignore`.

## `design/`

| File | Bytes | What it is |
|---|---:|---|
| `board.kicad_mod` | 559 105 | **Mainboard outline as a KiCad footprint** — what an add-on or front-panel designer imports to get the board shape and connector placement right |
| `board.svg` | 83 622 | Same outline, vector |
| `board_case.svg` | 92 166 | Outline with case |
| `coprocessor-latch-circuit.png` | 204 175 | Upstream `latch.png` — the circuit letting the always-on CH32V203 power the whole device up by emulating a power-button press. Renamed from `latch.png`, which said nothing about its subject |

The latch figure is the visual source for the architecture claim in
[`../../README.md`](../../README.md) that the coprocessor can wake the device from an RTC alarm.

---

## ⚠ Provenance note — `production/bom.csv` and `positions.csv` were line-ending-normalised

Not a file in this directory, but discovered while auditing it on 2026-09-20 and recorded here
because it affects how those artifacts verify.

[`../production/bom.csv`](../production/bom.csv) and
[`../production/positions.csv`](../production/positions.csv) are **not byte-identical to upstream**:

| File | Upstream SHA-256 | Repository SHA-256 | Δ bytes |
|---|---|---|---:|
| `bom.csv` | `1e2329e4b4aa9467…` | `db385cd1ca78c0ea…` | −85 |
| `positions.csv` | `a71154b38a4d7c8d…` | `9540faff84265154…` | −333 |

The upstream files use **CRLF**; the repository copies use **LF**. The deltas are exactly one byte
per line (85 lines, 333 lines). Stripping `\r` from the upstream copies reproduces the repository
hashes exactly — `executed-success`, 2026-09-20.

**Content is identical**; the UTF-8 BOM is preserved in both. But a verifier comparing the
repository copy against a fresh `git clone` will see a hash mismatch, so the upstream hashes are
recorded above. `designators.csv` and `netlist.ipc` **were not** normalised and match upstream
byte for byte.

The other four `production/` files are byte-identical to upstream and were confirmed so in the
same sweep.
