# Espressif ESP32-P4-EYE — **END OF LIFE**

> The original ESP32-P4 hand-held vision board. **Superseded** by the [ESP32-P4X-EYE](../esp32-p4x-eye/README.md). Retained here because it is the **only** version of this design for which Espressif publishes a schematic and PCB layout. Research retrieved **2026-08-21**.

- **Manufacturer:** Espressif Systems
- **Chip:** [ESP32-P4](../../../components/espressif/esp32-p4/README.md), silicon revisions **before v3.1**
- **Companion radio:** ESP32-C6-MINI-1U
- **Board revisions:** *"No previous versions available."* (S1) — i.e. this record covers the first and only release of the pre-P4X design
- **Status:** **EOL** — no updates, bug fixes or official support (S3)

---

## 1. Why this record exists

The successor's user guide offers only a *"ESP32-P4X-EYE Reference Design (ZIP)"* link, and **that link does not resolve** (every variant returns the documentation platform's 13 745-byte soft-404 shell; probes recorded in [component-download-failures.txt](../../../component-download-failures.txt)). This EOL board, by contrast, publishes a real schematic PDF and a real PCB layout PDF on `dl.espressif.com`.

Espressif states the only difference between the two boards is the fitted silicon revision (S2), so these files are the closest available primary evidence for the current board's circuitry. **That is a substitution, not an equivalence** — record it as such wherever you rely on it.

---

## 2. A versioning wrinkle worth noticing

The two published files are from **different board versions**:

| File | Version | Date in filename |
|---|---|---|
| `SCH_ESP32-P4-EYE-MB_V2.3_20250416.pdf` | **V2.3** | 2025-04-16 |
| `PCB_ESP32-P4-EYE-MB_V2.2_20250314.pdf` | **V2.2** | 2025-03-14 |

The schematic is one revision newer than the layout. Espressif publishes no changelog between V2.2 and V2.3 and the user guide says only "No previous versions available" (S1) — which refers to *user guides*, not to board revisions. **Do not assume the layout implements the schematic you are reading.** If a net matters, check both.

`MB` in the filenames is "main board" — consistent with the board's split top/bottom PCB description.

---

## 3. Hardware

Functionally the same board as the [ESP32-P4X-EYE](../esp32-p4x-eye/README.md), whose record carries the full top- and bottom-PCB component tables, the design-intent discussion and the notable design points. The differences are:

- The fitted **ESP32-P4 silicon is a revision earlier than v3.1**, so the earlier errata apply — the MSPI cluster (MSPI-749/750/751), Analog-765, DMA-767, ROM-764, APM-560 — and **ROM-770 and ROM-816 do not**. See the [ESP32-P4 errata table](../../../components/espressif/esp32-p4/README.md#10-errata-summary).
- Its Related Documents list is shorter: schematic, PCB layout, camera datasheet, display datasheet, ST7789VW datasheet, OV2710 overview (S1). The successor's list drops the schematic and PCB in favour of the (broken) reference-design ZIP — a **regression in published detail**, not an improvement.

Everything else — ESP32-C6-MINI-1U companion reached only via test points, 16 MB SPI flash, 1.54-inch 240 × 240 SPI LCD on an ST7789VW, 2 MP manual-focus MIPI-CSI camera, digital microphone, fill light, rotary encoder, 2 × 10P header, MicroSD in 4-line SDIO or SPI mode, lithium battery connector with red/green charge indicator, USB 2.0 HS **device**-only port plus a USB Debug port, and the absence of any audio output path — is as documented in the P4X-EYE record.

---

## 4. Local artifacts

Board-specific:

| File | Bytes | SHA-256 |
|---|---:|---|
| artifacts/esp32-p4-eye-mb-schematics-v2.3.pdf | 748 835 | `8d3769796bb38dda8682d87e94764f2163eb6cd4f1be886b3da91a512a55bffa` |
| artifacts/esp32-p4-eye-mb-pcb-layout-v2.2.pdf | 1 371 064 | `9ad4f2ec83442c843487ad2f7e5100cf91ca5ea4a9facfa1d4bba5d9ef9d4f7c` |

Both validated by `%PDF` magic. Both were renamed from Espressif's upstream filenames (`SCH_ESP32-P4-EYE-MB_V2.3_20250416.pdf`, `PCB_ESP32-P4-EYE-MB_V2.2_20250314.pdf`) to the repository's lowercase-hyphen convention; the original names and URLs are in §5.

**Not published:** BOM, Gerbers, dimensions, assembly drawing or EDA source. Unlike the Function-EV family there are no adapter-board reference designs either, because there are no adapter boards.

Shared component documentation in [`../shared-artifacts/`](../shared-artifacts/): ~~`esp-dev-kits-en-master-esp32p4.pdf`~~ (**archived 2026-08-24** — [record](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md)), `ov2710-camera-module-datasheet.pdf`, `hdf2710-47-mipi-camera-module-spec.pdf`, `st7789vw-datasheet.pdf`, `zjy154kc-if17-lcd-module-spec.pdf`. Sizes and hashes are tabulated in the [P4X-EYE record §6](../esp32-p4x-eye/README.md#6-local-artifacts).

---

## 5. Sources

**Full manifest — class, medium, retrieval dates, what each source establishes and its limitations:
[`sources.md`](sources.md).** The summary below is retained for quick reference; `S1`–`S4` map onto
`P4E-1`–`P4E-4` there.

> ⚠ **S1's URL is now dead.** This board's user guide moved from `…/esp32p4/eol/esp32-p4-eye/…` to
> `…/esp32p4/esp32-p4-eye/…` between 2026-08-21 and 2026-08-28. The old path returns HTTP 404 and
> **has no Wayback capture**. Full finding: [`sources.md` §4](sources.md#4-retrieval-findings).

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes |
|---|---|---|---|---|---|---|---|---|
| S1 | ESP32-P4-EYE User Guide (EOL section) | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/esp32-p4-eye/user_guide.html | 2026-08-21 | esp-dev-kits `latest`, source commit `f6f80ab` | Component tables; Related Documents list; "No previous versions available" |
| S2 | ESP32-P4X-EYE User Guide | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-eye/user_guide.html | 2026-08-21 | esp-dev-kits `latest` | That the successor differs only by fitted chip revision |
| S3 | esp-dev-kits — EOL (End of Life) Boards, ESP32-P4 | Espressif Systems | primary | official page | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/eol-boards.html | 2026-08-21 | `latest` | EOL status and support statement |
| S4 | Schematic and PCB layout | Espressif Systems | primary | schematic | https://dl.espressif.com/AE/esp-dev-kits/SCH_ESP32-P4-EYE-MB_V2.3_20250416.pdf and https://dl.espressif.com/AE/esp-dev-kits/PCB_ESP32-P4-EYE-MB_V2.2_20250314.pdf | 2026-08-21 | V2.3 / V2.2 | Local artifacts; the version mismatch in §2 |

---

## 6. Related records

- [Source manifest](sources.md) — every source behind this record
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [ESP32-P4X-EYE](../esp32-p4x-eye/README.md) — the current successor
- [ESP32-P4-Function-EV-Board (EOL)](../esp32-p4-function-ev-board/README.md)
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
- [Component index](../../../components/README.md) · [Device index](../../README.md)


> **Shared artifact note.** The offline esp-dev-kits PDF for the ESP32-P4 boards (`esp-dev-kits-en-master-esp32p4.pdf`) was **archived 2026-08-24** — its content was already mined into this and the sibling board records. Provenance, SHA-256 and verified download URLs: [`shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md).
