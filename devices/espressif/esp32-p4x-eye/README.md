# Espressif ESP32-P4X-EYE

> A hand-held, enclosed ESP32-P4 **vision** development board — camera, small LCD, microphone, rotary encoder, MicroSD and a battery connector in a case. Current board; supersedes the end-of-life [ESP32-P4-EYE](../esp32-p4-eye/README.md). Research retrieved **2026-08-21**.

- **Manufacturer:** Espressif Systems
- **Chip:** [ESP32-P4](../../../components/espressif/esp32-p4/README.md), silicon revision **v3.1 or later**
- **Companion radio:** ESP32-C6-MINI-1**U** module (external-antenna variant)
- **Documentation project:** `esp-dev-kits`, target `esp32p4`, slug `esp32-p4x-eye`
- **Status:** current

---

## 1. Identity and how it differs from the Function-EV boards

| | ESP32-P4X-EYE | ESP32-P4X-Function-EV-Board |
|---|---|---|
| Form factor | **Small, enclosed, battery-capable hand-held camera** | Large bare evaluation board |
| Display | 1.54-inch **SPI** LCD, 240 × 240 | 7-inch **MIPI-DSI** capacitive touch, 1024 × 600 |
| Camera | 2 MP MIPI-CSI, **manually adjustable focus**, fitted | 2 MP MIPI-CSI, optional accessory |
| USB | USB 2.0 HS **device** port + USB debug port | HS device + HS host + FS + Serial/JTAG |
| Ethernet | **No** | Yes (IP101GR / RJ45) |
| Audio out | **No codec, no amplifier, no speaker** | ES8311 + NS4150B + speaker header |
| Audio in | Digital microphone | Microphone into the codec |
| Battery | **Lithium battery connector + charging circuit with red/green indicator** | None |
| Input | **Rotary encoder**, user buttons | Touch screen |
| Extras | **Fill light** (illumination LED) | — |
| Expansion | 2 × 10P female header | 40-pin J1 header |
| Radio module | ESP32-C6-MINI-**1U** (external antenna) | ESP32-C6-MINI-**1** (PCB antenna) |

Source: S1, S2.

The design intent is different in kind, not degree. The Function-EV board is a *bench* platform for evaluating the P4's full peripheral set. The P4X-EYE is a **finished-feeling product** you can pick up and point at something: Espressif targets "smart surveillance cameras, vision model detection, and edge computing in IoT that require real-time image processing and wireless communication" (S1). The enclosure is even silkscreened with the port markings (`USB 2.0`, `Debug`, `↻` for reset, `⚙` for boot).

The `1U` suffix on the companion module is not cosmetic: it means an **external antenna connector** instead of a PCB antenna, which is the right choice for a device inside a plastic case that a hand wraps around.

> The "P4X" prefix means the same thing here as elsewhere: chip revision v3.1 or later. Espressif: *"The difference between the ESP32-P4X-EYE and the ESP32-P4-EYE is that the main chip on the former has been upgraded to the ESP32-P4 chip revision v3.1 or later version."* (S1) `ESP32-P4X` is **not** a chip — see [ESP32-P4 §1](../../../components/espressif/esp32-p4/README.md#the-p4x-naming-trap).

---

## 2. Components

### Top PCB (S1)

| Component | Notes |
|---|---|
| MicroSD card slot | 4-line SD bus with SDIO protocol, or SPI protocol |
| Test points | Programming/test access for the **ESP32-C6-MINI-1U** — DuPont wires |
| USB 2.0 Device Port | P4's USB 2.0 HS OTG, device role only. Also powers the board. Marked `USB 2.0` |
| USB Debug Port | Power, firmware flashing, USB Serial/JTAG. Marked `Debug` |
| Power switch | `I` = on (5 V), `O` = off |
| User-defined buttons | Application-defined |
| LCD FPC connector | To the 1.54-inch panel |
| LCD | **1.54-inch, 240 × 240, SPI**, ST7789VW controller |
| Charging indicator | Red while charging, green when complete |

### Bottom PCB (S1)

| Component | Notes |
|---|---|
| Rotary encoder | Application-defined; Espressif suggests UI navigation or camera zoom |
| ESP32-C6-MINI-1U | Wi-Fi + Bluetooth companion |
| Fill light | Illumination for capture and recording |
| Digital microphone | Voice recognition / audio recording |
| MIPI CSI connector | To the camera module |
| Female header | 2 × 10P, application-defined |
| SPI flash | **16 MB** |
| ESP32-P4 | Main SoC |
| Battery connector | Lithium battery |
| Reset button | Marked `↻` |
| Boot button | Marked `⚙`; hold while pressing Reset to enter download mode via the USB Debug Port. Doubles as a confirm button in applications |
| Camera | **2 MP, manually adjustable focal length** |

Camera and display parts, from the retained component documentation: the camera module is an **OV2710**-based unit (`HDF2710-47-MIPI`), and the display is a `ZJY154KC-IF17` 1.54-inch module driven by an **ST7789VW**.

### Component records

**Manufacturer:** [Espressif Systems — vendor sourcing guide](../../../vendors/espressif/README.md).

| Part / interface | Role | Record |
|---|---|---|
| ESP32-P4 | Main SoC, silicon revision v3.1+ | [`espressif/esp32-p4`](../../../components/espressif/esp32-p4/README.md) |
| MicroSD slot | 4-line SDIO or SPI | [`generic/micro-sd-sdmmc`](../../../components/generic/micro-sd-sdmmc/README.md) |
| USB 2.0 Device / Debug ports | HS device role; flashing and USB Serial/JTAG | [`generic/usb-c-interface`](../../../components/generic/usb-c-interface/README.md) |
| **ESP32-C6-MINI-1U** | Wi-Fi/BLE companion, external antenna | **no record.** ⚠ *Not* the [ESP32-C6-WROOM-1](../../../components/espressif/esp32-c6-wroom-1/README.md) — a different module in a different package with a different antenna arrangement |
| **ST7789VW** | LCD controller | [components/sitronix/st7789vw](../../../components/sitronix/st7789vw/README.md) |
| **ZJY154KC-IF17** | 1.54-inch 240 × 240 display module | **no record** — [spec retained](../shared-artifacts/sources.md#4-eye-family--camera-and-display-component-documentation) |
| **OV2710** / `HDF2710-47-MIPI` | 2 MP MIPI-CSI camera sensor and module | **no record** — [datasheets retained](../shared-artifacts/sources.md#4-eye-family--camera-and-display-component-documentation) |
| 16 MB SPI flash, digital microphone, fill light, rotary encoder, battery connector and charger | — | **no record**; part numbers are not published by Espressif for this board |

Rows marked **no record** name a real fitted part with no entry under
[`components/`](../../../components/README.md). Where a datasheet was retained it lives once in
[`../shared-artifacts/`](../shared-artifacts/) with provenance in
[its manifest](../shared-artifacts/sources.md).

---

## 3. Notable design points
**Device-only USB.** The USB 2.0 HS port here is documented as device role only — "ESP32-P4 acts as a USB device connecting to a USB host" (S1). There is no Type-A host connector and no TPS2051C power switch. The board's headline USB trick is *presenting its SD card to a PC*, which is exactly what the factory demo does.

**No audio output path.** There is a microphone but no codec, amplifier or speaker. This board records; it does not play.

**Battery power is a first-class feature.** A battery connector plus a charging circuit with a two-colour indicator makes this the only P4 board in the family that is meaningfully portable. Note, however, that the P4's low-power story is still constrained by the same board-level realities discussed for the Function-EV boards, and Espressif publishes no battery-life figure for this board. **No runtime claim is made here** because no source supports one.

**Two SD protocols are available.** The slot supports 4-line SDIO *or* SPI. 4-line SDIO is the one you want for video capture; SPI exists as a fallback and for pin-conflict relief.

**Flashing the companion is awkward.** The C6 module is reached through bare **test points** with DuPont wires — not even a connector, unlike the Function-EV boards. Plan for that if you intend to rebuild the ESP-Hosted slave firmware.

---

## 4. Firmware and examples

Standard ESP-IDF flow, target `esp32p4`, **minimum ESP-IDF v5.3** — see [ESP32-P4 §9](../../../components/espressif/esp32-p4/README.md#9-software-support-and-minimum-esp-idf-version). Flash over the **USB Debug Port**; hold **Boot** (`⚙`), press and release **Reset** (`↻`).

The single official example is the **Factory Demo** (`espressif/esp-dev-kits`, `examples/esp32-p4-eye/examples/factory_demo`, commit `f6f80ab`), and it is unusually complete for a vendor demo (S1):

- Photo capture and **timed capture**
- Video recording
- Album preview
- **USB SD-card mounting** (present the card to a host PC)
- Image parameter configuration
- **AI: face detection, pedestrian detection, and YOLOv11-nano object detection**

That last line is the most interesting thing about this board. Running YOLOv11-nano on-device is the concrete demonstration of what the P4's dual 400 MHz RISC-V cores plus AI instruction extensions plus 32 MB PSRAM are for, and it is a workload no ESP32-S3 can approach. **No performance figures (fps, latency, accuracy) are published by Espressif for this demo**, and none are invented here.

---

## 5. Design files — partial, and a substitution

**Espressif publishes no direct schematic or PCB PDF for the ESP32-P4X-EYE.** Its user guide offers only *"ESP32-P4X-EYE Reference Design (ZIP)"*, and that link **does not resolve** — every filename variant returns the documentation platform's 13 745-byte soft-404 shell. Probes recorded in [component-download-failures.txt](../../../component-download-failures.txt).

The **EOL ESP32-P4-EYE** does publish direct schematic and PCB PDFs, retained under [its record](../esp32-p4-eye/README.md):

- `SCH_ESP32-P4-EYE-MB_V2.3_20250416.pdf`
- `PCB_ESP32-P4-EYE-MB_V2.2_20250314.pdf`

Since Espressif states the only difference between the two boards is the chip revision (S1), those are the closest available primary evidence for this board's circuitry. **Label the substitution when you use it** — "identical schematic" is not established, only "difference described as a chip-revision change". Note also that the schematic (V2.3, 2025-04-16) and the PCB layout (V2.2, 2025-03-14) are themselves from *different board versions*; they do not describe the same artefact.

Component-level documentation (camera, display, ST7789VW, OV2710) is shared with the EOL board and retained once under [`../shared-artifacts/`](../shared-artifacts/).

---

## 6. Local artifacts

Board-specific: **none** — see §5.

Shared, in [`../shared-artifacts/`](../shared-artifacts/):

| File | Bytes | SHA-256 | What it documents |
|---|---:|---|---|
| ~~esp-dev-kits-en-master-esp32p4.pdf~~ **archived 2026-08-24** | 30 482 003 | `04d75d2acda82c8f5136bfed4d1732e7e4bd095437e2ecacce271374d8f8538c` | Offline user guides for every P4 board — [archive record](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |
| ov2710-camera-module-datasheet.pdf | 159 720 | `d34890622db7f06324242329e6b5193597c0088ffe9a2765194166ae3b201912` | Camera sensor overview |
| hdf2710-47-mipi-camera-module-spec.pdf | 246 656 | `050c43a50e45e77436dc99486098614f4ee04511c3586d702cab28b506868ecc` | The MIPI camera module as fitted |
| st7789vw-datasheet.pdf | 3 135 599 | `1f9e956057e3909c0714bdab9e682205e03cf52adefd5b4a01093fa3167d398b` | LCD controller |
| zjy154kc-if17-lcd-module-spec.pdf | 1 290 995 | `c323a0f082bea4a99431be5d54f2f3305d7489432e18c97d25aa23627bf3bfc5` | 1.54-inch display module |

Closest available board design files: [EOL ESP32-P4-EYE artifacts](../esp32-p4-eye/README.md#4-local-artifacts) — read §5 first.

Two of these were published under **percent-encoded Chinese filenames** on `dl.espressif.com` (`ST7789VW芯片手册.pdf`, `胶铁一体ZJY154KC-IF17.pdf`). They were renamed to ASCII on retrieval; the rename and the original URLs are recorded in §7 and in the vendor guide.

---

## 7. Sources

**Full manifest — class, medium, retrieval dates, what each source establishes and its limitations:
[`sources.md`](sources.md).** The summary below is retained for quick reference; `S1`–`S4` map onto
`PXE-1`–`PXE-4` there.

> ⚠ **S2's URL is now dead.** The EOL user guides moved out of the `eol/` path segment between
> 2026-08-21 and 2026-08-28; the cited path returns HTTP 404 with no Wayback capture. Current URL
> and full finding: [`sources.md` §5](sources.md#5-retrieval-findings).

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes |
|---|---|---|---|---|---|---|---|---|
| S1 | ESP32-P4X-EYE User Guide | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-eye/user_guide.html | 2026-08-21 | esp-dev-kits `latest`, source commit `f6f80ab` | Component tables, C6-MINI-1U, revision statement, factory-demo feature list, design-file links |
| S2 | ESP32-P4-EYE User Guide (EOL section) | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/eol/esp32-p4-eye/user_guide.html | 2026-08-21 | esp-dev-kits `latest` | Predecessor design-file URLs; "no previous versions" |
| S3 | Espressif DevKits product catalogue | Espressif Systems | primary | store listing | https://www.espressif.com/en/products/devkits | 2026-08-21 | as served | "ESP32-P4-based vision development board supporting MIPI-CSI camera and USB 2.0 High-Speed, integrating microphone and MicroSD slot" |
| S4 | Component documentation mirrored by Espressif | third-party via authorized mirror | datasheet | `https://dl.espressif.com/AE/esp-dev-kits/{ov2710pbv1.1web,HDF2710-47-MIPI-V2.0,ST7789VW芯片手册,胶铁一体ZJY154KC-IF17}.pdf` | 2026-08-21 | as served | Camera and display part identities |

Rights note for S4: these are third-party manufacturers' datasheets mirrored by Espressif with no stated licence. Copyright rests with the original IC/module vendors. Redistribution status **unknown**; retained for internal engineering reference only.

---

## 8. Related records

- [Source manifest](sources.md) — every source behind this record
- [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md)
- [ESP32-P4-EYE (EOL)](../esp32-p4-eye/README.md) — predecessor, and the source of the retained schematic/PCB
- [ESP32-P4X-Function-EV-Board](../esp32-p4x-function-ev-board/README.md)
- [ESP32-P4X-C5-Function-EV-Board](../esp32-p4x-c5-function-ev-board/README.md)
- [Shared artifacts](../shared-artifacts/README.md) · [their sources](../shared-artifacts/sources.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
- [Component index](../../../components/README.md) · [Device index](../../README.md)


> **Shared artifact note.** The offline esp-dev-kits PDF for the ESP32-P4 boards (`esp-dev-kits-en-master-esp32p4.pdf`) was **archived 2026-08-24** — its content was already mined into this and the sibling board records. Provenance, SHA-256 and verified download URLs: [`shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md`](../shared-artifacts/ARCHIVED-FRAMEWORK-GUIDES.md).
