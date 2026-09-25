# Flipper Devices Flipper Zero — *artifact-preservation record*

> ⚠ **This is not a researched device record.** It exists to give six primary schematics and a set
> of teardown photographs a correctly-classified home, because they describe the **Flipper Zero**
> and were previously stranded inside a clone of an unrelated project.
>
> No product research, sourcing, pricing, firmware or component recursion has been done. The
> sections a full device record requires are **absent, not empty** — do not read their absence as
> a finding. If you are researching the Flipper Zero properly, start from these artifacts and
> replace this file.
>
> Created **2026-09-20**.

## Why this record exists

The six schematic PDFs below were vendored into
[`badgeteam/konsool-zero`](https://github.com/badgeteam/konsool-zero) — a Tanmatsu radio add-on —
as a **prior-art study**. A 2026-09-20 pass over that clone filed its seven *chip* datasheets as
component artifacts and explicitly deferred these six, noting:

> *"These describe a different product (Flipper Zero), which has no record in this repository.
> Filing them would mean creating `devices/flipper-devices/flipper-zero/` — out of scope for this
> pass… **Recommended follow-up**."* — [`…/tanmatsu/sources.md`](../../nicolai-electronics/tanmatsu/sources.md)

That follow-up is done here. The alternative was leaving six unique primary documents in `scratch/`,
which the research skill forbids: *scratch is not storage*.

**A hash sweep on 2026-09-20 confirmed all six were absent** from both `hardware-doc` and
`repo-archive/hardware-doc` — they existed in exactly one place.

## Artifacts

### `artifacts/schematics/` — six sheets, in the repository

Publisher **Flipper Devices Inc.** (from each sheet's title block). All are **Altium 365
WebViewer** PDF exports (`Title: Altium.WebViewer.Files.WebViewerJob_PDF_SCHPrint`,
`Producer: llPDFLib 3.x`), one page each, 1223 × 792 pt, in **two export batches**.

| File | Bytes | SHA-256 (first 16) | PDF `CreationDate` |
|---|---:|---|---|
| `iButton schematic.pdf` | 166 109 | `0eb0e83b9f5d4c7a…` | 2022-08-02 |
| `NFC schematic.pdf` | 270 099 | `57fdc9228d48e961…` | 2022-08-02 |
| `Power and vibro schematic.pdf` | 208 904 | `746579026c934360…` | 2022-08-02 |
| `RFID schematic.pdf` | 355 725 | `755ddf5c49256c5f…` | 2022-08-02 |
| `Power schematic.pdf` | 382 383 | `ea166c85c57a990a…` | **2023-02-07** |
| `Sub-1 GHz CC1101 schematic.pdf` | 294 321 | `4ade1517cbddb3ac…` | **2023-02-07** |
| `link-to-explanation.txt` | 50 | — | a URL konsool-zero shipped beside them |

Full SHA-256 values are in the source table at the bottom of this file.

**Text-layer validated** per the skill's PDF rule: extracted strings were cross-checked against
the known title-block heading *"Flipper Devices Inc."* and against part numbers that are
independently known to be on the Flipper Zero. The layer is sound; values below may be trusted.
`executed-success`, `pdftotext -layout`, poppler via `nix shell nixpkgs#poppler-utils`, 2026-09-20.

### `artifacts/teardown-photos/` — **archived**, placeholder in place

Seven PNGs (4 114 939 B total), several hand-annotated, showing the Flipper Zero's MCU board, its
NFC/RFID antenna and its sub-GHz section. Moved to the archive on 2026-09-20; see
[`artifacts/teardown-photos.ARCHIVED.md`](artifacts/teardown-photos.ARCHIVED.md) for hashes, byte
sizes and recovery URLs.

⚠ **Provenance is not established.** These came bundled in konsool-zero with no licence and no
photographer credit. Redistribution status `unknown`. konsool-zero's own BSD-3-Clause covers its
design files, not necessarily third-party photographs it vendored.

## What was mined from these sheets

Extraction is deliberately narrow — enough to make the artifacts useful without pretending to a
Flipper Zero research pass.

### Parts named on the sheets

| Sheet | Parts read from the text layer |
|---|---|
| Sub-1 GHz | **`CC1101RGPR`**, **`BGS13S4N9E6327XTSA1`** (SP3T RF switch), **`B0310J50100AHF`** (balun), **26 MHz** crystal, sheet labelled **433 MHz** |
| NFC | **`ST25R3916`** |
| RFID (125 kHz) | **`LMV331IDCKR`** (comparator), **`LMV358AIDGKR`** (op-amp) |
| Power | **`BQ25896RTWR`** (charger), **`BQ27220YZFR`** (fuel gauge), **`LM3281YFQR`** |
| iButton | **`VSMY14940`** |

### The finding that matters: konsool-zero is a near-copy of this RF chain

Set the Flipper's sub-1 GHz sheet beside
[`konsool-zero`'s](../../nicolai-electronics/tanmatsu/konsool-zero-wiring.md):

| Function | Flipper Zero | konsool-zero | |
|---|---|---|---|
| Sub-GHz transceiver | `CC1101RGPR` | `CC1101RGPR` (`U1`) | **same** |
| RF switches | `BGS13S4N9E6327XTSA1` | `BGS13S4N9E6327XTSA1` (`U3`, `U4`) | **same** |
| Balun | `B0310J50100AHF` | `B0310J50100AHF` (`T1`) | **same** |
| CC1101 reference | **26 MHz crystal** | **27 MHz oscillator** (`U2`, `G3226000161060`) | **changed** |
| NFC front end | `ST25R3916` | `ST25R3916-AQWT` (`U5`) | **same** |
| 125 kHz analog | `LMV331`, `LMV358` | `LMV331IDCKR` (`U12`), `LMV358` (`U10`, `U14`) | **same** |
| MCU | `STM32WB55` | **`CH32V003F4U6`** | **changed** |
| Charger / gauge | `BQ25896`, `BQ27220` | *(none — host-powered)* | n/a |

This settles two things the Tanmatsu records could previously only assert:

1. **The 26 → 27 MHz change is deliberate, not a transcription.**
   [`expansion-boards.md` §2](../../nicolai-electronics/tanmatsu/expansion-boards.md) flags
   konsool-zero's `U2` as *"an XO, not a crystal — **27** not 26 MHz = TI's recommendation for
   **≥ 869 MHz**"*. The prior art it was copied from uses 26 MHz on a sheet labelled 433 MHz. The
   designer changed both the frequency and the part type when moving to the higher band.
2. **It explains the stray `stm32wb55cc.pdf`.** The Flipper's MCU is an STM32WB55; konsool-zero
   replaced it with a ~10-cent CH32V003. An earlier pass read the datasheet's presence as evidence
   of a fitted part and invented an STM32WB55CC on konsool-zero. That fabrication is recorded and
   refuted at
   [`components/stmicroelectronics/stm32wb55xx`](../../../components/stmicroelectronics/stm32wb55xx/README.md)
   and in [`expansion-boards.md` §2](../../nicolai-electronics/tanmatsu/expansion-boards.md).

`executed-success` — read directly from the sheets' text layers, 2026-09-20.

## Deliberately **not** done

- No Flipper Zero product, pricing, community, firmware or market research.
- No component records created **for the Flipper Zero's own sake**. The overlapping parts already
  have records because the *Tanmatsu family* uses them:
  [CC1101](../../../components/texas-instruments/cc1101/README.md) ·
  [ST25R3916](../../../components/stmicroelectronics/st25r3916/README.md) ·
  [STM32WB55xx](../../../components/stmicroelectronics/stm32wb55xx/README.md)
- **No attempt to establish whether Flipper Devices publishes these sheets officially.** They are
  Altium 365 WebViewer exports, which is how Flipper Devices distributes schematics, but the
  konsool-zero copies were not traced back to a live URL in this pass. **Unverified.**
- Antenna matching, filter values and component values on the sheets were **not** transcribed.

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| FZ-1 | Six Flipper Zero schematic sheets | **Flipper Devices Inc.** (title blocks) | primary | schematic PDF | vendored copy: <https://github.com/badgeteam/konsool-zero/tree/0f0b964107c15dd398ee3e44a064fb853b17aaa8/docs> | 2026-08-26 | 2022-08-02 / 2023-02-07 (PDF `CreationDate`) | Flipper Zero part selection for sub-GHz, NFC, 125 kHz RFID, power, iButton | `artifacts/schematics/` |
| FZ-2 | Flipper Zero teardown photographs (7) | **unknown** | community | photographs | same commit, `docs/flipper-zero-photos/` | 2026-08-26 | unknown | Physical layout of the MCU board, NFC/RFID antenna and sub-GHz section | **archived** — `artifacts/teardown-photos.ARCHIVED.md` |
| FZ-3 | `link-to-explanation.txt` | cnblogs (shangdawei) | community | blog | <https://www.cnblogs.com/shangdawei/p/3729375.html> | not fetched | unknown | The reference konsool-zero's author kept beside the photos. **Not retrieved or read in this pass** | `artifacts/schematics/link-to-explanation.txt` |

Full SHA-256, for verification without the archive:

```
0eb0e83b9f5d4c7aad29ef321d956c297b1a32eee64a8a7e195515966d25503c  iButton schematic.pdf
57fdc9228d48e961a656cea225448c6a145f5c995e4aaf0761458f5d49e5fe58  NFC schematic.pdf
746579026c9343606814ae026449bb894ea5a2c6c14780e0a7652e1cd4fd856d  Power and vibro schematic.pdf
ea166c85c57a990a4d94d2407b83b190845b0c9090955bee4be2a91f456abf55  Power schematic.pdf
755ddf5c49256c5f06d54f54cf879d9bf95616d92f7ffc9d0ef1e9c5d72c88a8  RFID schematic.pdf
4ade1517cbddb3ac0aa58faf02e098b8a3788b27a2c99b95f133a2f8a574a21f  Sub-1 GHz CC1101 schematic.pdf
```

Licence: **unknown** for every artifact here. Redistribution status `unknown`. Disposition:
`repository` for the schematics, `archive` for the photographs.

## Related records

- [Tanmatsu → `konsool-zero-wiring.md`](../../nicolai-electronics/tanmatsu/konsool-zero-wiring.md)
  — the add-on these sheets were studied for
- [Tanmatsu → `expansion-boards.md` §2](../../nicolai-electronics/tanmatsu/expansion-boards.md)
- [Tanmatsu → `artifacts/konsool-zero/`](../../nicolai-electronics/tanmatsu/artifacts/konsool-zero/README.md)
