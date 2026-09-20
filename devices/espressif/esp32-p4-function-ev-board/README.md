# Espressif ESP32-P4-Function-EV-Board — **END OF LIFE**

> The original ESP32-P4 multimedia evaluation board. **Superseded** by the [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md). Retained here because it is the **only** version of this design for which Espressif publishes complete main-board schematic, PCB layout, dimension and assembly files. Research retrieved **2026-08-21**.

- **Manufacturer:** Espressif Systems
- **Chip:** [ESP32-P4](../../../components/espressif/esp32-p4/README.md), silicon revisions **before v3.1**
- **Companion radio:** ESP32-C6-MINI-1
- **Board versions:** v1.4, **v1.52**
- **Status:** **EOL** — Espressif: *"these boards … no longer receive updates, bug fixes, or official support. It is recommended to switch to newer development boards"* (S3)

---

## 1. Why this record exists

Two reasons, and the second is the important one.

1. It is the direct ancestor of the current P4X board and appears in a great deal of existing example code, blog posts and the `esp-dev-kits` repository (its example directory is still named `examples/esp32-p4-function-ev-board/`, and the ESP Launchpad configuration for the *current* board is still hosted under this board's name).
2. **Espressif publishes this board's design files and does not publish the successor's.** The P4X board's *"Reference Design (ZIP)"* link is dead (see [P4X record §8](../esp32-p4x-function-ev-board/README.md#8-design-files-what-exists-and-an-important-substitution)), whereas this board's schematic, PCB layout, dimensions, DXF and assembly drawing all resolve as real PDFs from `dl.espressif.com`. Since Espressif describes the difference between the two boards as **only the fitted silicon revision** (S2), these files are the best available primary evidence for the current board's circuitry.

**Do not overstate that.** "Espressif describes the difference as a chip-revision change" is not the same claim as "the schematics are byte-identical". Silkscreen, passives and errata-driven changes are unverified.

---

## 2. Board revision history

| Version | Changes | Source |
|---|---|---|
| **v1.4** | Original release. Debug port was a **USB-to-UART bridge** on a Type-C connector. **IO24 and IO25 present** on the pin headers | S1 |
| **v1.52** | Debug port replaced by the ESP32-P4's **built-in USB Serial/JTAG**; a **Full-speed USB OTG** breakout added on a Type-C port; **IO24 and IO25 removed** from the pin headers | S1 |

Espressif's own summary (S1):

> "The main improvements in development board version v1.52 compared to v1.4 include: replacing the USB-to-UART Type-C port used for debugging with the ESP32-P4 chip's built-in USB Serial/JTAG port, adding a Full-speed USB OTG breakout to a Type-C port, and removing IO24 and IO25 from the pin headers."

**This is the single most likely source of silent breakage when reusing old P4 code or pin maps.** If a tutorial, example or forum post references IO24 or IO25 on a header, it predates v1.52 and will not work on any current board. Likewise, if it describes installing a CP210x/CH34x USB-UART driver to talk to the board, it is a v1.4 document.

The retained schematic and assembly drawing are **v1.52**. The PCB layout, dimensions PDF and DXF carry no version in their filenames and are assumed to match v1.52; that assumption is **not verified**.

---

## 3. Hardware

Functionally the same board as the [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md), whose record carries the full component list, J1 header pinout, LCD adapter wiring, ribbon-cable direction rules and known limitations. Rather than duplicate them, the differences are:

- The fitted **ESP32-P4 silicon is a revision earlier than v3.1** — so the v3.0-and-earlier errata cluster applies, notably the three MSPI errata (MSPI-749/750/751), Analog-765, DMA-767, ROM-764 and APM-560. See the [ESP32-P4 errata table](../../../components/espressif/esp32-p4/README.md#10-errata-summary). Conversely **ROM-770 (v3.1) and ROM-816 (v3.2) do *not* apply** to this board.
- On **v1.4** only: a USB-UART bridge chip is present and IO24/IO25 are on the headers.
- The 40-pin J1 header on v1.52 matches the P4X board's.

Everything else — ESP32-C6-MINI-1 companion, 16 MB SPI flash at 80 MHz, ES8311 + NS4150B audio, IP101GR Ethernet PHY, TPS2051C USB power switch, MicroSD, MIPI-DSI/CSI 15-pin FPC connectors, 40 MHz and 32.768 kHz crystals, and the LDO_VO3/VO4 sleep-power caveat — is as documented in the P4X record.

---

## 4. Design files

All published by Espressif from `dl.espressif.com/dl/schematics/` and retrieved and validated 2026-08-21 (S1):

| Document | Local file |
|---|---|
| Schematics, board v1.52 | [artifacts/esp32-p4-function-ev-board-schematics-v1.52.pdf](artifacts/esp32-p4-function-ev-board-schematics-v1.52.pdf) |
| PCB layout | [artifacts/esp32-p4-function-ev-board-pcb-layout.pdf](artifacts/esp32-p4-function-ev-board-pcb-layout.pdf) |
| Assembly drawing, v1.52 | [artifacts/esp32-p4-function-ev-board-assembly-v1.52.pdf](artifacts/esp32-p4-function-ev-board-assembly-v1.52.pdf) |
| Dimensions (drawing) | [artifacts/esp32-p4-function-ev-board-dimensions.pdf](artifacts/esp32-p4-function-ev-board-dimensions.pdf) |
| Dimensions (CAD source, DXF) | [artifacts/esp32-p4-function-ev-board-dimensions.dxf](artifacts/esp32-p4-function-ev-board-dimensions.dxf) |

**Not published:** BOM, Gerbers or EDA source for the main board. Espressif directs those to `sales@espressif.com`. The **adapter boards do** have complete reference designs including BOM and Gerbers — see [`../shared-artifacts/`](../shared-artifacts/).

Note this board has an assembly drawing where the C5 board (the only other one with published main-board files) does not; and the C5 board is *not* an ancestor of this design, so its schematic is not a substitute for this one.

---

## 5. Local artifacts

| File | Bytes | SHA-256 |
|---|---:|---|
| artifacts/esp32-p4-function-ev-board-schematics-v1.52.pdf | 817 278 | `7a1d12a37e21db20fe7db8092f4428b87465873feab65b3cd90bc6fe7dd6673b` |
| artifacts/esp32-p4-function-ev-board-pcb-layout.pdf | 1 808 476 | `382426995df9dd4c5c26d4ef4fcbe575ef45425516ff6675039ede5b8c565a00` |
| artifacts/esp32-p4-function-ev-board-assembly-v1.52.pdf | 131 618 | `0d035b10b35f717a344f11d59059f228b42ba3a64fa4c751dc16f967d86bc816` |
| artifacts/esp32-p4-function-ev-board-dimensions.pdf | 885 140 | `f34799b848dc8b1638f1db473c69415512cad423c4e77be5fb03f534a334f57a` |
| artifacts/esp32-p4-function-ev-board-dimensions.dxf | 3 879 854 | `980ad74d4f7af35d403367acc735ac5f2a9bca726bd565bd4a21cda61250fe23` |

The four PDFs were validated by `%PDF` magic. The DXF is an ASCII AutoCAD drawing-exchange file (verified to begin with the standard `  0` / `SECTION` header, not HTML); Espressif suggests the free Autodesk Viewer.

Shared artifacts (FPC connector spec, panel/camera/display-driver datasheets, LCD and camera sub-board schematics and PCB layouts, and the two adapter-board reference-design ZIPs with Gerbers and BOM) are in [`../shared-artifacts/`](../shared-artifacts/); sizes and hashes are tabulated in the [P4X record §12](../esp32-p4x-function-ev-board/README.md#12-local-artifacts).

---

## 6. Sources

**Full manifest — class, medium, retrieval dates, what each source establishes and its limitations:
[`sources.md`](sources.md).** The summary below is retained for quick reference; `S1`–`S4` map onto
`P4F-1`–`P4F-4` there.

> ⚠ **S1's URL is now dead.** This board's user guide moved from
> `…/esp32p4/eol/esp32-p4-function-ev-board/…` to `…/esp32p4/esp32-p4-function-ev-board/…` between
> 2026-08-21 and 2026-08-28. The old path returns HTTP 404 and **has no Wayback capture**. Full
> finding: [`sources.md` §4](sources.md#4-retrieval-findings).

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes |
|---|---|---|---|---|---|---|---|---|
| S1 | ESP32-P4-Function-EV-Board User Guide (EOL section) | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/esp32-p4-function-ev-board/user_guide.html | 2026-08-21 | esp-dev-kits `latest`, source commit `f6f80ab` | v1.4 → v1.52 revision history; all design-file URLs; component list |
| S2 | ESP32-P4X-Function-EV-Board User Guide | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-function-ev-board/user_guide.html | 2026-08-21 | esp-dev-kits `latest` | That the successor differs only by fitted chip revision |
| S3 | esp-dev-kits — EOL (End of Life) Boards, ESP32-P4 | Espressif Systems | primary | official page | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/eol-boards.html | 2026-08-21 | `latest` | EOL status and support statement |
| S4 | Design files | Espressif Systems | primary | schematic | https://dl.espressif.com/dl/schematics/esp32-p4-function-ev-board-{schematics_v1.52,pcb-layout,assembly_v1.52,dimensions}.{pdf,dxf} | 2026-08-21 | v1.52 where versioned | Local artifacts |

---

## 7. Related records

- [Source manifest](sources.md) — every source behind this record
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md) — the current successor
- [ESP32-P4X-C5-Function-EV-Board](../esp32-p4x-c5-function-ev-board/README.md)
- [ESP32-P4-EYE (EOL)](../esp32-p4-eye/README.md)
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
- [Component index](../../../components/README.md) · [Device index](../../README.md)


> **Shared artifact note.** The offline esp-dev-kits PDF for the ESP32-P4 boards (`esp-dev-kits-en-master-esp32p4.pdf`) was **archived 2026-08-24** — its content was already mined into this and the sibling board records. Provenance, SHA-256 and verified download URLs: [`shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md).
