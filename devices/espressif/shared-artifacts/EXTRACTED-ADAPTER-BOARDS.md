# Extracted adapter-board reference designs — inventory and disposition

> Extracted and inventoried **2026-08-24**. Both ZIPs remain in this directory; see
> [*Why both the ZIP and the extraction are kept*](#6-why-both-the-zip-and-the-extraction-are-kept).

The two `*-adapter-board-reference-design.zip` files described in [`README.md`](./README.md)
had never been opened. They are now extracted in place as:

- `camera-adapter-board-reference-design/`
- `lcd-adapter-board-reference-design/`

These are the **most complete design packages Espressif publishes anywhere in the P4 family** —
editable OrCAD schematic source, editable Allegro board source, full Gerbers, drill files, BOM
and fabrication notes. Nothing else in this repository, for any board, comes with EDA source.

---

## 1. Inventory

### `camera-adapter-board-reference-design.zip`

| Field | Value |
|---|---|
| ZIP size | 1,349,188 bytes (1.29 MiB) |
| ZIP SHA-256 | `2ab4b8ad20b60817ddd1e8d72de0680f841c9bc0d452b82d9d93aa82c9b8e529` |
| Members reported by `unzip -l` | **74** |
| Real files after excluding macOS noise | **25** |
| Extracted size, as extracted | **2,835,704 bytes** (2.70 MiB) |
| Tree content digest, **as extracted** (pristine) | `56024d57070734e42a870d55c7d45ee1713f4e0f2d0e0d1a1fa55c5618babea4` |
| Tree content digest, **as it now stands in this repo** | `4722d65676b6e78a9e584435f610b3729071d6560ac9c10df6d6f7a0206f3115` (2,818,825 B / 25 files, after the §3 promotion and its placeholder) |
| Design version | Schematic **V1.1** / PCB **V1.1**, both dated **2024-05-29**; fabrication notes **2024-06-05** |
| BOM version | `BOM(V0.3)` |
| Author / vendor | Espressif Systems. BOM `docProps`: created by **`lizijin`** 2024-05-30, last modified by **`Wang Dong`** 2026-05-26 |
| License | **None stated.** Redistribution status `unknown` (unchanged from [`README.md`](./README.md)) |
| Upstream repo / commit | **Not applicable** — published as a ZIP on `dl.espressif.com`, not in any git repository |

### `lcd-adapter-board-reference-design.zip`

| Field | Value |
|---|---|
| ZIP size | 1,276,237 bytes (1.22 MiB) |
| ZIP SHA-256 | `231e1ff2f9373de5b9924eaaab00801ad777fb483945629f160423c3752693ed` |
| Members reported by `unzip -l` | **74** |
| Real files after excluding macOS noise | **26** |
| Extracted size, as extracted | **3,296,614 bytes** (3.14 MiB) |
| Tree content digest, **as extracted** (pristine) | `a7d40ec056f13ee274d5fc9244f74430e055217a0c9b18c8ae572fd065ba5fd9` |
| Tree content digest, **as it now stands in this repo** | `097170c68a55432f391b6dfdd670440d3b306a2ff25c3335d9fdbfdd2157e130` (3,215,489 B / 26 files, after the §3 promotion and its placeholder) |
| Design version | Schematic **V1.3 (2024-07-09)** / PCB **V1.2 (2024-05-27)** — *see the version-skew caveat below* |
| BOM version | `BOM(V0.4)` |
| Author / vendor | Espressif Systems. BOM `docProps`: created by **`lizijin`** 2024-05-24, last modified by **`Wang Dong`** 2026-05-26 |
| License | **None stated.** Redistribution status `unknown` |
| Upstream repo / commit | **Not applicable** |

### Tree content digest definition

```bash
d=camera-adapter-board-reference-design      # or lcd-adapter-board-reference-design
find "$d" -type f -exec sha256sum {} + \
  | sed "s|  $d/|  |" | LC_ALL=C sort -k2 | sha256sum
```

Two digests are recorded per package because they answer different questions:

- **as extracted (pristine)** — reproduce it by extracting the ZIP with the decoding rules in §2
  (skip `__MACOSX/` and `.DS_Store`, decode names as UTF-8) and hashing immediately. Use this to
  confirm your extraction of a freshly downloaded ZIP matches ours.
- **as it now stands** — the same computation run against this repository today. It differs
  because §3 promoted one PDF out of each tree and left a `PROMOTED-assembly-drawing.md`
  placeholder behind. Use this to confirm the checked-in trees have not drifted.

---

## 2. What was dropped on extraction, and why

`unzip -l` reports 74 members per archive but there are only 25/26 real files. The gap is macOS
packaging noise, which was **not** extracted:

| Excluded | Count (camera / LCD) | What it is |
|---|---|---|
| `__MACOSX/…/._*` | 37 / 36 | AppleDouble resource forks — a macOS artifact of zipping from Finder. Each is 120–268 bytes of metadata about a file that is also in the archive. No content |
| `.DS_Store` | 3 / 3 | Finder folder-view state. No content |
| directory entries | 8 / 8 | Zero-length entries recreated implicitly by extraction |

They are still inside the retained ZIPs, so nothing is lost; the byte-exact archive is
recoverable and its hash unaffected.

### Filename encoding — a real trap

Both archives contain one directory whose name is **Chinese**: `04_PCB 加工说明`
("PCB fabrication notes"). The ZIP does **not** set the UTF-8 general-purpose bit (bit 11) on
these entries, so:

- Stock `unzip` produces `04_PCB ????`.
- Applying the usual CP437→GBK repair produces the mojibake `04_PCB 鍔犲伐璇存槑`.

The bytes are in fact **already UTF-8**, merely unflagged. Correct handling is to decode the raw
name as UTF-8 and ignore the flag. Reproduce the extraction with:

```python
import zipfile, pathlib
zf = zipfile.ZipFile("camera-adapter-board-reference-design.zip")
for i in zf.infolist():
    name = i.filename if (i.flag_bits & 0x800) else \
           i.orig_filename.encode('cp437').decode('gbk').encode('gbk').decode('utf-8')
    if name.startswith('__MACOSX/') or name.endswith('.DS_Store'):
        continue
    ...
```

> This is worth remembering: [`README.md`](./README.md) previously stated that member paths were
> "preserved as supplied rather than renamed, since renaming inside an archive would break its
> integrity hash". That is still true of the ZIP — but the *extraction* here uses the correctly
> decoded name `04_PCB 加工说明`, which is what the archive actually encodes. This is a decoding
> fix, not a rename.

---

## 3. Documents found, and where they went

Every PDF, spreadsheet and document in both archives was identified. **No component datasheets
were found** — these packages are entirely board-level design data. Consequently **no new
`components/<manufacturer>/<part>/` records were created from them**; see §5 for what that
leaves open.

| Document (in archive) | Bytes | SHA-256 (prefix) | Disposition |
|---|---:|---|---|
| `Camera Adapter Board/01_Schematic/SCH_…MIPI_Camera_Sub_V1.1_20240529.pdf` | 331,500 | `b26da766` | **Kept in the extracted tree.** Near-duplicate of `camera-subboard-schematics.pdf` — see §4 |
| `Camera Adapter Board/02_PCB/PCB_…MIPI_Camera_Sub_V1.1_20240529.pdf` | 130,803 | `a8b9443e` | **Kept in the extracted tree.** Near-duplicate of `camera-subboard-pcb-layout.pdf` — see §4 |
| `Camera Adapter Board/06_Placement/Assemble_…MIPI_Sub_V1_20240529.pdf` | 20,334 | `c527fae1` | ➡️ **PROMOTED** to `camera-subboard-assembly-drawing.pdf` |
| `LCD Adapter Board/01_Schematic/SCH_ESP32-P4_HMI_SubBoard_V1.3_20240709.pdf` | 328,112 | `cbb6a53d` | **Kept in the extracted tree.** *Byte-identical* to the existing `lcd-subboard-schematics.pdf` — see §4 |
| `LCD Adapter Board/02_PCB/PCB_ESP32-P4_HMI_SubBoard_V1.2_20240527.pdf` | 308,099 | `f07ef2f2` | **Kept in the extracted tree.** Near-duplicate of `lcd-subboard-pcb-layout.pdf` — see §4 |
| `LCD Adapter Board/06_Placement/Assemble_ESP32-P4_HMI_SubBoard_V1.2_20240527.pdf` | 85,267 | `721e1b04` | ➡️ **PROMOTED** to `lcd-subboard-assembly-drawing.pdf` |
| `…/05_BOM/BOM(V0.3)ESP32-P4_Function_EV_board_MIPI_Sub_XX_TTNNVV.xlsx` | 11,835 | — | Kept in place (spreadsheet, not a document) |
| `…/05_BOM/BOM(V0.4)_ESP32-P4-HMI-SubBOARD_XX_TTNNVV.xlsx` | 13,140 | — | Kept in place |
| `…/04_PCB 加工说明/PCB 加工说明_….xls` (×2) | 541,184 / 82,432 | — | Kept in place. Chinese-language fabrication/stackup notes for the board house |
| `…/06_Placement/place_txt.txt` (×2) | 2,332 / 7,953 | — | Kept in place. Machine-readable placement (refdes, X/Y, rotation, side) |

**Two files were promoted**, both because they are documents that exist **nowhere else in this
repository** — Espressif does not publish the assembly drawings as standalone downloads, only
inside these ZIPs. Leaving them buried five directories deep inside an extracted archive would
have made them undiscoverable. Placeholders were written at both original locations before the
move; see `…/06_Placement/PROMOTED-assembly-drawing.md` in each tree.

The four schematic/layout PDFs were **not** moved, because equivalents are already published at
the top level of this directory and are recorded in [`README.md`](./README.md). Moving them would
have created confusion rather than resolving it.

---

## 4. Finding: the standalone sub-board PDFs are *re-prints*, not different revisions

This was not previously documented and is easy to get wrong. Comparing the standalone PDFs in
this directory against their counterparts inside the ZIPs:

| Standalone file | SHA-256 (prefix) | ZIP counterpart | SHA-256 (prefix) | Identical? |
|---|---|---|---|:--:|
| `lcd-subboard-schematics.pdf` | `cbb6a53d` | `SCH_…HMI_SubBoard_V1.3_20240709.pdf` | `cbb6a53d` | ✅ **yes, byte-for-byte** |
| `camera-subboard-schematics.pdf` | `dcb30637` | `SCH_…Camera_Sub_V1.1_20240529.pdf` | `b26da766` | ❌ no |
| `camera-subboard-pcb-layout.pdf` | `791c0922` | `PCB_…Camera_Sub_V1.1_20240529.pdf` | `a8b9443e` | ❌ no |
| `lcd-subboard-pcb-layout.pdf` | `6f1c9a35` | `PCB_…HMI_SubBoard_V1.2_20240527.pdf` | `f07ef2f2` | ❌ no |

The three that differ are **not different design revisions**. PDF metadata shows they are
separate print runs of the same design:

- `camera-subboard-schematics.pdf` — `Producer: Microsoft: Print To PDF`,
  `CreationDate: D:20240702164928+08'00'`
- ZIP's camera schematic — same producer, `CreationDate: D:20240530155352+08'00'`
- `lcd-subboard-pcb-layout.pdf` — `Creator: Allegro Design Publisher`,
  `CreationDate: D:20240702171437+08'00'`, and its embedded text contains **`V1.2`** — the same
  board revision as the ZIP copy

So Espressif re-exported the standalone PDFs on **2024-07-02** from the same source designs, with
a slightly different film selection in the layout prints (the standalone layouts include a
`Composite` sheet; the ZIP copies include the individual `DRII`/`OUTLINE`/`PASTE`/`SOLDER` films).
The `Print To PDF` producer string also means the byte differences are partly just
non-deterministic printer-driver output.

**Practical consequence:** do not treat the differing hashes as evidence of a design change. For
the camera board, schematic and PCB are both **V1.1 / 2024-05-29** in every copy we hold.

### The version-skew caveat is confirmed, and it is real

For the **LCD** adapter board the schematic and the PCB genuinely *are* different revisions:

- `SCH_ESP32-P4_HMI_SubBoard_**V1.3**_20240709` — schematic
- `PCB_ESP32-P4_HMI_SubBoard_**V1.2**_20240527` — board, Gerbers, placement, assembly drawing
- `PCB 加工说明_ESP32-P4_HMI_SubBoard_**V1.2**_20240524` — fabrication notes

Every manufacturing output in the package is **V1.2**; only the schematic is V1.3. Anyone
fabricating from these Gerbers is building V1.2 hardware while reading a V1.3 schematic.
[`README.md`](./README.md) flagged this; the extraction confirms the skew extends to the Gerbers,
drill files, placement and assembly drawing, not just the two files whose names were previously
visible.

The camera adapter board has no such skew — everything is V1.1 / 2024-05-29.

---

## 5. Findings from the BOMs — components not yet recorded

The two BOMs name real manufacturer part numbers that have **no `components/` record** in this
repository. No datasheets were present in the archives, so nothing was auto-created; these are
listed as leads.

| Part | Manufacturer | Function | On which board |
|---|---|---|---|
| `DMN63D8LDW-7` | Diodes Incorporated | Dual N-MOSFET, SOT-363, 30 V / 220 mA. **BOM note: "注意阈值电压最大值小于1.8V" — Vgs(th) max must be < 1.8 V.** Level-shifter, hence the constraint | Camera |
| `LBSS138DW1T1G` | LRC (Leshan Radio) | Second-source for the above | Camera |
| `ME6211C18M5G-N` / `ME6211C28M5G-N` | Microne (微盟) | 1.8 V / 2.8 V LDO, SOT23-5 | Camera, LCD |
| `AFA07-S15FCA-00`, `AFA07-S06ECA-00`, `AFC01-S30FCA-00` | 钜硕/矩硕电子 (Jushuo) | FFC/FPC connectors, 15P/6P/30P | Camera, LCD |
| `FPC-05F-24PH20` | 讯普 (Xunpu) | FFC connector, 0.5 mm, 24P | Camera |
| `ETA1611S2G` | ETA Solutions | Backlight boost, 2 A, 22 V OVP, true-PWM dimming | LCD |
| `AP3012KTR-G1` | Diodes Incorporated | DC-DC boost | LCD |
| `TYPE-C-31-M-12` | HRO (韩荣) | USB Type-C receptacle, 16-pin | LCD |
| `SWPA3012S100MT` | Sunlord (顺络) | 10 µH power inductor, 830 mA, 3×3×1.2 mm | LCD |
| `2.1.3.2400037` | MDH | 24 MHz oscillator, 1.8–3.3 V, ±10 ppm | Camera |

`1.0K-GT-15PB` (华德共创) is on the LCD BOM as `J3` and **is** already covered — see
`1.0K-GT-15PB-fpc-connector-specification.pdf` in this directory.

Several rows carry LCSC/JLCPCB cross-references in the `备注` (remarks) column
(e.g. `参考：嘉立创C262721`), which is the fastest route to a datasheet for any of the above.

---

## 6. Why both the ZIP and the extraction are kept

| | ZIP | Extraction |
|---|---|---|
| Bytes | 2,625,425 (both) | 6,132,318 (both) |
| Hash-verifiable against `dl.espressif.com`? | ✅ yes | ✗ no |
| Greppable / diffable / browsable in a code host? | ✗ no | ✅ yes |
| Preserves `__MACOSX` and `.DS_Store`? | ✅ yes | ✗ deliberately not |
| Preserves the unflagged-UTF-8 filename quirk? | ✅ yes | ✗ decoded correctly instead |

Total cost of keeping both: **8.8 MiB**. That is small enough that the duplication is not worth
resolving, and the two forms answer different questions. The ZIP stays because it is the only
artifact whose hash can be checked against the vendor; the extraction stays because a ZIP nobody
opens is a ZIP nobody reads — which is exactly the state this directory was in until today.

**Noted duplication:** roughly 6.1 MiB of this directory is now the same content stored twice.
This is intentional and is recorded here so that any duplicate-hash verification tooling can be
told to expect it.

### One further nested duplication

`camera-adapter-board-reference-design/Camera Adapter Board/03_Gerber/` contains **both**
`Gerber_…_V1.1_20240529.zip` (42,478 bytes) *and* an already-extracted directory of the same
name. Verified 2026-08-24 with `diff -rq`: the two are **identical, all 16 files**. Espressif
shipped the Gerbers twice inside the same archive. The inner ZIP is kept as-supplied rather than
removed, since at 42 KB it is not worth a placeholder and removing it would make the extraction
diverge from the archive for no benefit. The LCD package has no equivalent inner ZIP.

---

## 7. Reacquire

```bash
# Source 1 — Espressif, primary (note the /schematics/ path, NOT /dl/schematics/)
curl -L -O https://dl.espressif.com/schematics/CameraAdapterBoardReferenceDesign.zip
curl -L -O https://dl.espressif.com/schematics/LCDAdapterBoardReferenceDesign.zip

# Source 2 — Espressif China mirror host (same path scheme)
curl -L -O https://dl.espressif.cn/schematics/CameraAdapterBoardReferenceDesign.zip
curl -L -O https://dl.espressif.cn/schematics/LCDAdapterBoardReferenceDesign.zip

# Source 3 — linked from the ESP32-P4-Function-EV-Board user guide
#   https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html
#   (also reproduced offline in esp-dev-kits-en-master-esp32p4.pdf in this directory)
```

## 8. Verify

```bash
sha256sum CameraAdapterBoardReferenceDesign.zip
# expect 2ab4b8ad20b60817ddd1e8d72de0680f841c9bc0d452b82d9d93aa82c9b8e529
sha256sum LCDAdapterBoardReferenceDesign.zip
# expect 231e1ff2f9373de5b9924eaaab00801ad777fb483945629f160423c3752693ed

# integrity of every member without extracting:
unzip -t CameraAdapterBoardReferenceDesign.zip
unzip -t LCDAdapterBoardReferenceDesign.zip
```

## 9. URL probe results (2026-08-24)

| URL | HTTP | Content-Length | Last-Modified | Notes |
|---|---|---:|---|---|
| `https://dl.espressif.com/schematics/CameraAdapterBoardReferenceDesign.zip` | `HTTP/2 200` | 1349188 — **matches** | `Fri, 21 Aug 2026 09:58:12 GMT` | Hash still matches despite the recent `Last-Modified`; the file was re-uploaded, not changed |
| `https://dl.espressif.com/schematics/LCDAdapterBoardReferenceDesign.zip` | `HTTP/2 200` | 1276237 — **matches** | `Fri, 21 Aug 2026 09:56:56 GMT` | Same |
| `https://web.archive.org/cdx/…/CameraAdapterBoardReferenceDesign.zip` | — | — | — | ⚠️ **No captures. Not in the Internet Archive** |
| `https://web.archive.org/cdx/…/LCDAdapterBoardReferenceDesign.zip` | — | — | — | ⚠️ **No captures. Not in the Internet Archive** |

> **Single-source risk — flagged, not resolved.** Unlike the Waveshare originals, these two ZIPs
> have **exactly one** live origin (`dl.espressif.com`, with `dl.espressif.cn` being the same
> operator) and **no Internet Archive capture at all**. Under this repository's own policy that
> is a reason to *keep* them, which is what was done. They are strong candidates for
> `https://web.archive.org/save/` — see the recommendation at the end of this file.

---

## 10. Recommended, not done

1. **Submit both ZIP URLs to `https://web.archive.org/save/`.** They are single-source, they are
   the most complete design data Espressif publishes for the P4 family, and the archive has never
   seen them. This is the single highest-value follow-up.
2. **Create `components/` records** for the ten parts in §5, starting with `ETA1611`
   (the backlight boost — the part most likely to matter when debugging an LCD adapter) and
   `DMN63D8LDW-7` (whose threshold-voltage constraint is a genuine design gotcha).
3. **Add `04_PCB 加工说明` translations.** The two `.xls` files contain the stackup, impedance
   control and surface-finish requirements. They are Chinese-only and currently unreadable to
   most of this repository's audience. The camera one is 541 KB, which suggests embedded images.
4. **Cross-check the LCD V1.2/V1.3 skew against the published `lcd-subboard-schematics.pdf`.**
   That PDF is byte-identical to the ZIP's V1.3 schematic, so Espressif's *only* published LCD
   sub-board schematic documents a revision its own Gerbers do not build.
