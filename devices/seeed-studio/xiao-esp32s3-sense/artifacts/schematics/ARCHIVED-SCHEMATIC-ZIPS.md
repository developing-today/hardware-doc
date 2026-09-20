# Archived schematic and KiCad ZIPs — reacquisition record

> Moved out of the repository **2026-08-30**, not deleted. **The extracted contents remain in
> [`../extracted/`](../extracted/)**, so every schematic, PCB and library file is still
> directly readable in this repository — only the redundant ZIP wrappers were archived.

Each ZIP below was stored alongside a full extraction of itself. Nothing here is needed to
read the designs; re-fetch only if you want the vendor's original container.

## What was archived

| File | Bytes (ZIP) | SHA-256 (of the ZIP) | Extraction retained at |
|---|---:|---|---|
| `schematics/xiao-esp32s3-v1.1-sch-pcb.zip` | 1 203 582 | `0110d0baa6e27b9d895d79a1e966312c35343f56b4a22f186e95c33c195bf694` | [`../extracted/xiao-esp32s3-v1.1-sch-pcb/`](../extracted/xiao-esp32s3-v1.1-sch-pcb/) |
| `schematics/xiao-esp32s3-sense-v1.5-sch-pcb.zip` | 836 170 | `a82247725c8a8bcd8cac81a7acbd126396217e5b680f6dfe28958851e02d5cdb` | [`../extracted/xiao-esp32s3-sense-v1.5-sch-pcb/`](../extracted/xiao-esp32s3-sense-v1.5-sch-pcb/) |
| `schematics/xiao-esp32s3-expansion-board-v1.0-sch-pcb.zip` | 717 005 | `5ee313210515bbc45428779e80944ceb7065c0ba508073dee22e698104ba1a47` | [`../extracted/xiao-esp32s3-expansion-board-v1.0-sch-pcb/`](../extracted/xiao-esp32s3-expansion-board-v1.0-sch-pcb/) |
| `kicad/xiao-esp32s3-plus-v1.1-kicad.zip` | 678 481 | `8a90aa5990a835e97bc1e74afdd36f6a84dc32ad2eee2c423a6818157e1e65cd` | [`../extracted/xiao-esp32s3-plus-v1.1-kicad/`](../extracted/xiao-esp32s3-plus-v1.1-kicad/) |

A fifth ZIP, `xiao-esp32s3-v1.4-sch-pcb.zip`, was **byte-identical** to the Sense v1.5 ZIP and is
recorded separately in
[`xiao-esp32s3-v1.4-sch-pcb.zip.DUPLICATE.md`](xiao-esp32s3-v1.4-sch-pcb.zip.DUPLICATE.md).
Its identical extraction was removed at the same time.

Archive path: `archive/devices/seeed-studio/xiao-esp32s3-sense/artifacts/{schematics,kicad}/`

## Reacquisition

```bash
B=https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res
curl -fsSL "$B/202003749_XIAO%20ESP32S3_v1.1_SCH%26PCB_260226.zip"        -o xiao-esp32s3-v1.1-sch-pcb.zip
curl -fsSL "$B/202003753_XIAO%20ESP32S3%20Sense_v1.5_SCH%26PCB_260226.zip" -o xiao-esp32s3-sense-v1.5-sch-pcb.zip
curl -fsSL "$B/XIAO_ESP32S3_ExpBoard_v1.0_SCH%26PCB.zip"                   -o xiao-esp32s3-expansion-board-v1.0-sch-pcb.zip
```

Retrieved **2026-08-24** from the wiki's *Resources → Schematic / PCB* section.

## Independent sources

`files.seeedstudio.com` is a single point of failure: every `curl` above resolves to that one
host, so the commands are one hostname's lifetime from useless. Two independent ways to
rediscover the links:

- **Seeed wiki page** (separate host, human-readable *Resources* section):  
  <https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/>
- **Wiki source on GitHub** — different infrastructure entirely, and the markdown carries the
  download URLs verbatim, so the links survive even if the rendered wiki changes:  
  <https://raw.githubusercontent.com/Seeed-Studio/wiki-documents/docusaurus-version/sites/en/docs/Sensor/SeeedStudio_XIAO/SeeedStudio_XIAO_ESP32S3/XIAO_ESP32S3_Getting_Started.md>  
  (branch `docusaurus-version`; `main` 404s and `master` is a near-empty tree)

> **Filenames carry a date suffix that changes.** This record cites
> `..._SCH%26PCB_260226.zip`, while the wiki snapshot in
> [`../wiki-snapshot/`](../wiki-snapshot/) references `..._SCH&PCB_230327.zip` and
> `XIAO_ESP32S3_ExpBoard_v1.0_SCH&PCB_230324.zip` for the same designs. If a URL 404s, list the
> *Resources* section rather than assuming the artifact is gone — the suffix has most likely
> moved on. Match by SHA-256, not by filename.


> ⚠ The expansion-board ZIP is the **Sense daughterboard** design, published under the
> misleading name `XIAO_ESP32S3_ExpBoard_v1.0_SCH&PCB`. It is not an "expansion board" in the
> shield sense — see [`sense-daughterboard.md`](../../sense-daughterboard.md). This naming is
> why the Sense schematic is widely believed to be unpublished.

The Plus KiCad set is served from the **same** `…/SeeedStudio-XIAO-ESP32S3/res/` bucket, under
`XIAO_ESP32S3_Plus_V1.1_KiCad_260115.zip` — see
[`../kicad/ARCHIVED-PLUS-KICAD-ZIP.md`](../kicad/ARCHIVED-PLUS-KICAD-ZIP.md).

## What was extracted before archiving

These design files are the primary evidence behind most of this device's documentation. Everything
load-bearing is already in committed Markdown:

| Extracted to | What |
|---|---|
| [`pinouts-and-buses.md`](../../pinouts-and-buses.md) | Net-level pin mapping, resolved from the `.kicad_pcb` net names |
| [`sense-daughterboard.md`](../../sense-daughterboard.md) | The B2B connector pinout, camera rail LDOs, `PWDN`/`RESET` strapping |
| [`bom-and-board-construction.md`](../../bom-and-board-construction.md) | Component designators, values, board outline **17.78 × 21.14 mm** from `Edge.Cuts` |
| [`gaps-and-conflicts.md`](../../gaps-and-conflicts.md) | The `VCC_1V8`-is-actually-1.3 V discrepancy, and the v1.4/v1.5 packaging bug |

Two findings that came only from these files, and would be lost without them:

- **R11/R12 on the SD card `CS` line.** R12 (0 Ω, fitted) routes `CS` to GPIO21; **R11 is
  depopulated and routes to GPIO3**. Moving one resistor resolves the LED/SD-card collision, and
  explains the wiki's own GPIO3-versus-GPIO21 contradiction.
- **The camera rails are local.** 2.8 V and 1.3 V LDOs sit on the daughterboard; the camera is not
  fed from the mainboard's 3.3 V.

Netlist extraction method — including why `.kicad_pcb` is parsed rather than `.kicad_sch` — is
documented in
[`guides/reverse-engineering/netlists-from-vendor-eda-files.md`](../../../../../guides/reverse-engineering/netlists-from-vendor-eda-files.md).
