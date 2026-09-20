# Espressif ESP32-P4X-C5-Function-EV-Board

> The dual-band-Wi-Fi member of the ESP32-P4 evaluation-board family. Same multimedia design as the [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md), but with an **ESP32-C5-MINI-1** companion module giving **2.4 GHz *and* 5 GHz Wi-Fi 6**. Research retrieved **2026-08-21**.

- **Manufacturer:** Espressif Systems
- **Chip:** [ESP32-P4](../../../components/espressif/esp32-p4/README.md)
- **Companion radio:** ESP32-C5-MINI-1 (dual-band 2.4/5 GHz Wi-Fi 6, Bluetooth 5 LE, 802.15.4)
- **Board version documented:** **2.0** (design files are named `…-2.0-…`)
- **Documentation project:** `esp-dev-kits`, target `esp32p4`, slug `esp32-p4x-c5-function-ev-board`
- **Status:** current, **no previous revisions** (S1)

---

## 1. Why this board exists

There is exactly one reason to choose this board over its C6 sibling: **5 GHz Wi-Fi**.

Because the ESP32-P4 has no radio, the wireless capability of every P4 board is a property of its *companion module*, not of the P4 (see [ESP32-P4 §5](../../../components/espressif/esp32-p4/README.md#5-no-wireless--the-defining-constraint)). Espressif has exploited that cleanly here: swap ESP32-C6-MINI-1 for ESP32-C5-MINI-1 and the same P4 design gains a 5 GHz band. Nothing about the P4 side changes.

| | ESP32-P4X-Function-EV-Board | **ESP32-P4X-C5-Function-EV-Board** |
|---|---|---|
| Companion module | ESP32-C6-MINI-1 | **ESP32-C5-MINI-1** |
| Wi-Fi | 2.4 GHz Wi-Fi 6 | **2.4 GHz + 5 GHz Wi-Fi 6** |
| Bluetooth | 5 (LE) | 5 (LE) |
| 802.15.4 | Yes | Yes |
| P4 programming connector on board | No (USB Serial/JTAG only) | **Yes** — dedicated ESP-Prog/UART connector for P4 rev v3.x+ |
| Main-board schematic/PCB/dimensions published | **No** | **Yes** — full set of PDFs + DXF |
| Board revisions | Supersedes an EOL predecessor | No previous revisions |

That third and fourth rows matter more than they look. This is currently the **only** ESP32-P4 board in the family for which Espressif publishes the main board's schematic, PCB layout and dimensions as direct downloads. If you are doing your own P4 hardware, this is the reference design you can actually read.

Why 5 GHz matters for this specific board: it is a *camera and display* platform. Streaming 1080p H.264 out over Wi-Fi, or pulling video in, is exactly the workload that suffers on a congested 2.4 GHz band. If your product streams video, start here.

---

## 2. Feature list

Espressif's own summary (S1):

- **Main SoC:** ESP32-P4, dual-core RISC-V, with **16 MB SPI flash and 32 MB PSRAM** on board
- **On-board module:** ESP32-C5-MINI-1 — 2.4 GHz & 5 GHz dual-band Wi-Fi 6, Bluetooth 5 (LE), IEEE 802.15.4
- **Display:** MIPI-DSI, 7-inch capacitive touch screen 1024 × 600 (optional accessory)
- **Camera:** MIPI-CSI, 2 MP (optional accessory)
- **Audio:** ES8311 codec, NS4150B power amplifier, onboard microphone, speaker output port
- **Storage:** MicroSD card slot, 4-bit mode
- **USB:** USB 2.0 OTG Type-C, USB 2.0 Type-A, USB Full-Speed port, USB Serial/JTAG port
- **Network:** RJ45 Ethernet, 10/100 Mbps adaptive (IP101GR PHY on the P4 EMAC RMII)
- **Expansion:** J1 header
- **Buttons:** BOOT, Reset

Note that unlike the C6 board's user guide, this one commits to **32 MB PSRAM** in its feature list. That implies an `ESP32-P4NRW32X` part; the C6 board's guide only says "supports up to 32 MB". Treat the C6 board's PSRAM size as unconfirmed and this one as stated.

### Component records

**Manufacturer:** [Espressif Systems — vendor sourcing guide](../../../vendors/espressif/README.md).

| Part / interface | Role | Record |
|---|---|---|
| ESP32-P4 | Main SoC | [`espressif/esp32-p4`](../../../components/espressif/esp32-p4/README.md) · [memory subsystem](../../../components/espressif/esp32-p4/README.md#3-memory-subsystem) |
| MicroSD slot | 4-bit mode | [`generic/micro-sd-sdmmc`](../../../components/generic/micro-sd-sdmmc/README.md) |
| USB 2.0 OTG Type-C / Type-A / Full-Speed / Serial-JTAG | Four USB paths, two on one HS OTG controller | [`generic/usb-c-interface`](../../../components/generic/usb-c-interface/README.md) |
| **ESP32-C5-MINI-1** | Dual-band Wi-Fi 6 + BLE 5 + 802.15.4 companion — **the entire reason this board exists** | **no record.** ⚠ Not covered by [ESP32-C6-WROOM-1](../../../components/espressif/esp32-c6-wroom-1/README.md), which is a different chip in a different module |
| **ES8311** audio codec · **NS4150B** Class-D amplifier | Audio in/out | **no record** |
| **IP101GR** | Ethernet PHY on the P4 EMAC RMII → RJ45 10/100 | **no record** |
| **TPS2051C** | USB host power switch, 500 mA limit | **no record** |
| `1.0K-GT-15PB` FPC connector · 7″ 1024 × 600 MIPI-DSI panel · **EK79007AD** + **EK73217BCGA** drivers (a **pair** on one panel, not alternatives) · 2 MP MIPI-CSI camera | Optional display and camera accessories | [ek79007ad](../../../components/fitipower/ek79007ad/README.md) · [ek73217bcga](../../../components/fitipower/ek73217bcga/README.md); connector and camera **no record** |
| 16 MB SPI flash, 40 MHz and 32.768 kHz crystals, 3.3 V and `VDD_HP` bucks, 5 V→3.3 V LDO | — | **no record**; part numbers not published |

Rows marked **no record** name a real fitted part with no entry under
[`components/`](../../../components/README.md). Where a datasheet was retained it lives once in
[`../shared-artifacts/`](../shared-artifacts/) with provenance in
[its manifest](../shared-artifacts/sources.md).

---

## 3. Board layout, clockwise from J1

Espressif's numbering (S1). Differences from the C6 board are **bolded**.

1. J1 GPIO header · 2. **ESP32-C5-MINI-1 module** · 3. **ESP32-C5 module programming connector** · 4. Microphone · 5. Reset button · 6. ES8311 codec · 7. Speaker output port (4 Ω / 3 W, 2.00 mm pitch) · 8. NS4150B PA · 9. 5 V→3.3 V LDO · 10. BOOT button · 11. IP101GR Ethernet PHY · 12. 3.3 V buck · 13. 5 V power-on LED · 14. RJ45 · 15. USB Full-speed port · 16. USB Serial/JTAG port · 17. USB 2.0 Type-C · 18. USB 2.0 Type-A · 19. Power switch · 20. TPS2051C USB power switch · 21. MIPI CSI connector (`1.0K-GT-15PB`, 1.0 mm pitch, 15-pin) · 22. `VDD_HP` buck · 23. ESP32-P4 · 24. 40 MHz XTAL · 25. 32.768 kHz XTAL · 26. MIPI DSI connector · 27. 16 MB SPI flash · **28. ESP32-P4 programming connector — ESP-Prog/UART, for chip revision v3.x and later** · 29. MicroSD slot

The two ordering differences from the C6 board are that the C5's programming connector sits at position 3 rather than 2, and that a **new item 28** appears: a UART programming connector for the P4 itself. On the C6 board there is no such connector and the P4 can only be flashed over USB Serial/JTAG.

---

## 4. Shared characteristics with the C6 board

The following are identical to the [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md) and are documented in full there rather than repeated:

- **USB Type-C (HS device) and USB Type-A (HS host) cannot be used simultaneously** — one OTG controller, two connectors. The Type-A path is current-limited to 500 mA by the TPS2051C.
- **Flash runs at 80 MHz max with no auto-suspend** by default; 120 MHz or auto-suspend requires contacting Espressif (S1).
- **LDO_VO3 / LDO_VO4 must be configured in software**, and even when disabled the board's power architecture may exceed the chip datasheet's low-power figures. Espressif explicitly recommends optimising the power tree in your own design (S1). **Do not benchmark P4 sleep current on this board.**
- **LCD and camera are optional accessories**, connected through adapter boards over 15-pin 1.0 mm FPC cables, with **forward-direction cable for the camera and reverse-direction for the LCD**.
- **The companion module has no USB path** — flash it over its dedicated programming connector with an ESP-Prog or UART tool.
- **Two firmware images**, host and ESP-Hosted slave, must be version-matched.

---

## 5. Design files — the good case

Unlike every other board in the P4 family, Espressif publishes this board's main-board design files directly, from `dl.espressif.com/schematics/` (S1). All four were retrieved and validated:

| Document | Local file |
|---|---|
| Schematics | [artifacts/esp32-p4x-c5-function-ev-board-2.0-schematics.pdf](artifacts/esp32-p4x-c5-function-ev-board-2.0-schematics.pdf) |
| PCB layout | [artifacts/esp32-p4x-c5-function-ev-board-2.0-pcb-layout.pdf](artifacts/esp32-p4x-c5-function-ev-board-2.0-pcb-layout.pdf) |
| Dimensions (drawing) | [artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.pdf](artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.pdf) |
| Dimensions (CAD source, DXF) | [artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.dxf](artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.dxf) |

**Not published:** BOM, Gerbers, assembly drawing, or EDA source for the main board. Espressif directs those requests to `sales@espressif.com`. The *adapter* boards do have complete reference designs including BOM and Gerbers (see §7).

The `-2.0-` in every filename is the board version. If Espressif issues a 2.1, these URLs will not silently update — re-check them.

---

## 6. Getting started

Standard ESP-IDF flow, target `esp32p4`, **minimum ESP-IDF v5.3**, newer preferred — see [ESP32-P4 §9](../../../components/espressif/esp32-p4/README.md#9-software-support-and-minimum-esp-idf-version). Note that the **ESP32-C5** companion has its own, later ESP-IDF floor than the C6 (`COMPATIBILITY.md` records C5 as supported since v5.5.2 — S3); if you intend to build ESP-Hosted slave firmware for the C5 yourself, that, not v5.3, is your practical minimum for the toolchain overall.

Flash and monitor the P4 over the **USB Serial/JTAG** port; hold **BOOT** and pulse **Reset** to enter download mode. Alternatively use the new P4 programming connector with an ESP-Prog.

Espressif's user guide points at the same `esp_brookesia_phone` example as the C6 board, in `espressif/esp-dev-kits` at `examples/esp32-p4-function-ev-board/examples/esp_brookesia_phone` (commit `f6f80ab`), and at the same ESP Launchpad configuration — both still published under the older board name. **Expect example code to need the companion-radio configuration changed from C6 to C5.**

---

## 7. Local artifacts

Board-specific:

| File | Bytes | SHA-256 |
|---|---:|---|
| artifacts/esp32-p4x-c5-function-ev-board-2.0-schematics.pdf | 789 023 | `ceff97cf20e86b30480f8410d285f411108b4402beb2f63c1a0559f5119b9bd9` |
| artifacts/esp32-p4x-c5-function-ev-board-2.0-pcb-layout.pdf | 1 858 663 | `99f52f5e42d09f31807ab3b434a62d494cc689303bdd6de4cd9d5f3ff5c06e16` |
| artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.pdf | 973 576 | `e17701e88dcd413dbc9c8dbc6756dd1e80548f0bbd28cb1bd026a5abc73c6473` |
| artifacts/esp32-p4x-c5-function-ev-board-2.0-dimensions.dxf | 3 790 900 | `66098f18545d861f3655a80ecdf8e789a112c60da59ea77e5dd0eb2eca028a29` |

Shared with the rest of the family in [`../shared-artifacts/`](../shared-artifacts/): ~~`esp-dev-kits-en-master-esp32p4.pdf`~~ (**archived 2026-08-24** — [record](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md)), `1.0K-GT-15PB-fpc-connector-specification.pdf`, `camera-module-datasheet.pdf`, `display-datasheet.pdf`, `ek73217bcga-datasheet.pdf`, `ek79007ad-datasheet.pdf`, `lcd-subboard-schematics.pdf`, `lcd-subboard-pcb-layout.pdf`, `camera-subboard-schematics.pdf`, `camera-subboard-pcb-layout.pdf`, `lcd-adapter-board-reference-design.zip`, `camera-adapter-board-reference-design.zip`. Sizes and hashes are tabulated in the [P4X-Function-EV-Board record §12](../esp32-p4x-function-ev-board/README.md#12-local-artifacts).

The two adapter-board ZIPs are the most complete design packages Espressif publishes anywhere in this family: each contains `01_Schematic` (OrCAD `.DSN` + PDF), `02_PCB` (Allegro `.brd` + PDF), `03_Gerber` (full `.art` set + drill files), `05_BOM` (`.xlsx`) and `06_Placement` (assembly PDF + placement text). 74 members each, integrity-verified.

The DXF files are AutoCAD drawing exchange format; Espressif suggests the free Autodesk Viewer.

---

## 8. Sources

**Full manifest — class, medium, retrieval dates, what each source establishes and its limitations:
[`sources.md`](sources.md).** The summary below is retained for quick reference; `S1`–`S4` map onto
`C5-1`–`C5-4` there.

> ✅ **This is the only board in the P4 family with no dead or migrated source** — every URL cited
> here still resolves as of 2026-08-28. Its EOL siblings were not so lucky; see
> [`sources.md` §5](sources.md#5-retrieval-findings).

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes |
|---|---|---|---|---|---|---|---|---|
| S1 | ESP32-P4X-C5-Function-EV-Board User Guide | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-c5-function-ev-board/user_guide.html | 2026-08-21 | esp-dev-kits `latest`, source commit `f6f80ab` | Feature list, component descriptions, 32 MB PSRAM, no previous revisions, design-file URLs, flash and LDO restrictions |
| S2 | Espressif DevKits product catalogue | Espressif Systems | primary | store listing | https://www.espressif.com/en/products/devkits | 2026-08-21 | as served | Board lineup and marketing description |
| S3 | ESP-IDF `COMPATIBILITY.md` and chip-support matrix | Espressif Systems | primary | repository | https://github.com/espressif/esp-idf/blob/master/COMPATIBILITY.md | 2026-08-21 | `master` as served | ESP32-C5 supported since ESP-IDF v5.5.2 |
| S4 | Design files (schematics, PCB layout, dimensions PDF and DXF) | Espressif Systems | primary | schematic | https://dl.espressif.com/schematics/ESP32_P4X_C5_Function_EV_board-2.0-{schematics,pcb-layout,dimensions}.{pdf,dxf} | 2026-08-21 | board v2.0 | Circuit and mechanical detail; local artifacts |

---

## 9. Related records

- [Source manifest](sources.md) — every source behind this record
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md) — the 2.4 GHz sibling
- [ESP32-P4X-EYE](../esp32-p4x-eye/README.md)
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
- [Component index](../../../components/README.md) · [Device index](../../README.md)


> **Shared artifact note.** The offline esp-dev-kits PDF for the ESP32-P4 boards (`esp-dev-kits-en-master-esp32p4.pdf`) was **archived 2026-08-24** — its content was already mined into this and the sibling board records. Provenance, SHA-256 and verified download URLs: [`shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md).
