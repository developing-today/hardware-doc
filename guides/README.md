# Guides

Cross-cutting notes that do not belong to a single chip or board. Per-part records live under [`components/`](../components/README.md); per-board records live under [`devices/`](../devices/README.md); procedures for *obtaining* documents live under [`vendors/`](../vendors/README.md).

| Area | Contents |
|---|---|
| [Espressif](espressif/README.md) | **Ecosystem and product lines** (the family map: which chip, which radio, which ISA) · **SoC peripheral reference** (the numeric ESP32 / S3 / P4 tables, extracted from the TRMs) · **Practical errata** · **Memory and boot** · ESP-IDF cross-target peripheral capabilities · ESP-ADF audio pipelines and memory budget · ESP-IoT-Solution display/touch/knob/USB components |
| [**Hardware subsystems**](hardware/README.md) | **E-paper displays** (waveforms, bias rails, VCOM, ghosting, temperature, the NDA boundary) · **Display interfaces** (SPI / QSPI / parallel / MIPI-DSI / e-paper, bandwidth and framebuffer arithmetic, TE lines, LVGL, every documented controller) |
| [**Serial device access**](serial-access/README.md) | Getting a board to appear as a usable serial port: bridge chips vs native USB-CDC, `dialout` vs **`uucp` on Arch**, udev rules, and the two processes that silently steal the port — **`brltty`** (CH340) and **ModemManager** (intermittent flash failures). Plus macOS `cu.*` vs `tty.*` and Windows COM |
| [**NFC**](nfc/README.md) | Device-independent NFC: the 14443-A/B / FeliCa / 15693 standards landscape and which tags are which, **antenna matching and the Q trade-off** (where the real difficulty is), reader silicon comparison, RFAL and the library options, and symptom-to-cause debugging |
| [**LoRa**](lora/README.md) | Device-independent LoRa: **LoRa vs LoRaWAN vs Meshtastic**, the SF/airtime/duty-cycle trade, **regional band plans as a legal constraint**, SX1261 vs SX1262, `BUSY`/TCXO/DIO and the LDO-vs-DC-DC current cost, RadioLib, and honest range estimation |
| [Reverse engineering](reverse-engineering/netlists-from-vendor-eda-files.md) | **Recovering netlists from vendor EDA files** — KiCad PCB/schematic and EAGLE XML, and what a recovered netlist reliably reveals |
| [**Research technique**](research/finding-projects-that-use-a-board.md) | **Finding projects that use a board** (search by dependency, not product name) · **Finding certification records** (FCC grantee-code enumeration, which regulatory databases are actually reachable, and the positive/negative controls that make an absence finding mean anything) |
| [Markets and sourcing](markets/README.md) | **Device comparison matrix** (every documented device, side by side) · **Vendor and marketplace comparison** (where to buy, and whether the documentation will still exist later) · **Clones, siblings and variants** (identifying and working with copies) |
| [NixOS as a development host](nixos/README.md) | Running embedded toolchains — ESP-IDF, Arduino, PlatformIO, mesh/LoRa/SDR tooling, proprietary UI editors — on NixOS, where "download the installer and run it" does not apply |

---

## Every guide, one line each

### Espressif — [`espressif/`](espressif/README.md)

| Page | One line |
|---|---|
| [Ecosystem and product lines](espressif/ecosystem-and-product-lines.md) | The family map: ESP8266 → ESP32 → S2/S3 → C-series → H-series → P4, which have Classic Bluetooth vs BLE-only vs 802.15.4 vs **no radio**, Xtensa vs RISC-V, the ordering-nomenclature decode, and the **companion-radio pattern** |
| [SoC peripheral reference](espressif/soc-peripheral-reference.md) | The authoritative **numeric** cross-target table — PCNT, RMT, LEDC, I2S, timers, SPI, I²C, UART, ADC, GPIO, DMA, USB, SD/MMC, memory and crypto — extracted from the locally-held TRMs and datasheets with printed page citations |
| [Practical errata](espressif/errata-practical.md) | Which silicon errata actually bite in practice, per chip revision |
| [Memory and boot](espressif/memory-and-boot.md) | Memory maps, boot behaviour and PSRAM voltage constraints |
| [ESP-IDF peripheral capabilities](espressif/esp-idf-peripheral-capabilities.md) | Cross-target peripheral divergences and API entry points — plus the negative result that the IDF guide renders `SOC_*` counts symbolically, which is why the TRMs stay authoritative |
| [ESP-ADF audio pipelines](espressif/esp-adf-audio-pipelines.md) | The Element→Pipeline architecture, the Bluetooth Classic (HFP/A2DP/AVRCP) service API, codec integration, and the **audio memory budget** |
| [ESP-IoT-Solution components](espressif/esp-iot-solution-components.md) | The **LCD driver-interface selection table**, touch-controller support, the software-PCNT **Knob** component and its accuracy limits, and the USB controller taxonomy |

### Hardware subsystems — [`hardware/`](hardware/README.md)

| Page | One line |
|---|---|
| [E-paper displays](hardware/e-paper-displays.md) | How e-paper works and how to drive it: waveforms and LUTs, why a multi-rail PMIC and a hardware sequencer are unavoidable, **VCOM and why it is per-panel**, update-mode trade-offs with real timings, temperature dependence, burn-in, and **exactly what the E Ink NDA does and does not put out of reach** |
| [Display interfaces](hardware/display-interfaces.md) | Every display transport in the library compared — **who owns the frame**, bandwidth arithmetic, the ESP32 family's LCD peripherals per chip, **framebuffer/PSRAM sizing**, TE lines and tearing, LVGL buffer patterns, init tables, and a table of **every documented display controller** |
| [Parallel Intel-8080 LCD buses on ESP32](hardware/parallel-8080-lcd-buses.md) | Why the display-library choice matters more than the board — 8080 vs RGB vs QSPI, the `TFT_eSPI`/`Arduino_GFX`/`LovyanGFX` decision, the `User_Setup_Select.h` trap, GRAM offsets, and a black-screen debugging checklist |
| [LoRa radio generations](hardware/lora-radio-generations.md) | The four generations of Semtech LoRa transceiver silicon, where the numbering comes from, a like-for-like matrix across SX127x / SX126x / SX128x / LR11xx / LR20xx, and **what breaks when you migrate** |

### NFC — [`nfc/`](nfc/README.md)

| Page | One line |
|---|---|
| [**NFC — a device-independent guide**](nfc/README.md) | The four physical layers (14443-A/B, FeliCa, 15693) and which real tags are which · NFC Forum types 1–5 and why **MIFARE Classic is none of them** · reader / card-emulation / P2P and which are realistic · **antenna matching, the Q-versus-bandwidth trade and why range is capped by coil size** · the operation-byte pattern, banked registers, IRQ and FIFO · **RFAL's structure and what porting it actually means** · a maintenance-checked library table · symptom-to-cause debugging |

### LoRa — [`lora/`](lora/README.md)

| Page | One line |
|---|---|
| [**LoRa — a device-independent guide**](lora/README.md) | **SF/BW/CR against airtime, battery and legality**, with the arithmetic shown — one SF step buys 2.5 dB and costs 2× airtime · **LoRa vs LoRaWAN vs Meshtastic** · a sourced **regional band table**, and why EU duty cycle and US dwell time forbid opposite things · **SX1261 vs SX1262 vs SX1268** precisely · `BUSY`, TCXO on `DIO3`, RF switch on `DIO2`, **LDO vs DC-DC and why receive current dominates** · RadioLib, and the finding that it implements **all four** of Semtech's mandatory errata workarounds · **honest range estimation**, and why 2 450 km is the wrong answer |

### Markets and sourcing — [`markets/`](markets/README.md)

| Page | One line |
|---|---|
| [**Device comparison matrix**](markets/device-comparison-matrix.md) | All fourteen documented devices side by side — SoC, memory, display, input, connectivity, power, audio, camera, expansion, enclosure, dated prices, open-source posture and lifecycle — followed by which device suits which use case, **the conflicts found between records**, and the gaps the comparison exposes |
| [Vendor and marketplace comparison](markets/vendor-comparison.md) | Where to buy, what each vendor actually sells, documentation quality, schematic and EDA-source availability, licensing posture, and **long-term file-hosting reliability** |
| [Clones, siblings and variants](markets/clones-and-variants.md) | Spotting a clone from a listing photo, what actually differs, a five-minute triage procedure, and the **Guition JC3636K518** worked example |

### Reverse engineering — [`reverse-engineering/`](reverse-engineering/netlists-from-vendor-eda-files.md)

| Page | One line |
|---|---|
| [Recovering netlists from vendor EDA files](reverse-engineering/netlists-from-vendor-eda-files.md) | Parse the `.kicad_pcb`, not the `.kicad_sch` — how to extract authoritative connectivity from KiCad and EAGLE sources, and what it reliably reveals |
| [Tracing nets from schematic PDFs](reverse-engineering/tracing-nets-from-schematic-pdfs.md) | **When the vendor published a PDF and nothing else.** Altium exports embed invisible `CO` / `PI` / `NL` marker tokens at item coordinates, which is what makes a net list recoverable from the text layer with poppler alone; the geometric fallback for non-Altium exports; and ⚠ **the outlined-text trap** — KiCad and EAGLE routinely convert schematic text to vector paths, yielding zero extractable words and a permanently untraceable file. Companion to [`netlists-from-vendor-eda-files.md`](reverse-engineering/netlists-from-vendor-eda-files.md), which is preferred whenever EDA sources exist. *Added 2026-09-11* |

### Research technique — [`research/`](research/finding-projects-that-use-a-board.md)

| Page | One line |
|---|---|
| [Finding projects that use a board or component](research/finding-projects-that-use-a-board.md) | Search by **dependency**, not product name; authenticated GitHub code search — the technique that took one board's known projects from two to a dozen |
| [**Finding certification records**](research/finding-certification-records.md) | FCC OET equipment-authorisation lookup and **the grantee-code enumeration trick** — enumerate the vendor's grantee code, not the product name, and you get every device it has certified, **including ones it never announced**. Which regulatory databases are reachable without a login (measured, with the failures named); the **inverted Cloudflare block on `fccid.io`**, which serves 403 to a Chrome UA and 200 to `curl`; exhibit download templates; a worked **positive/negative control pair**; and why CE and UKCA have no database to search at all. *Added 2026-09-11* |

### Host platform — [`nixos/`](nixos/README.md)

| Page | One line |
|---|---|
| [NixOS as an embedded development host](nixos/README.md) | ESP-IDF, Arduino, PlatformIO and proprietary UI editors on NixOS — including why installing the `esp-idf-full` *package* alone yields no `idf.py`, package availability in the locked nixpkgs with dated absences, and why LVGL and sensor libraries are project dependencies rather than system packages |
| [RISC-V and vendor-SDK toolchains](nixos/riscv-and-vendor-sdk-toolchains.md) | Why `pkgsCross.riscv64-*` does not substitute for XuanTie GCC (`-mcpu=c908v` is XuanTie-specific and unknown to mainline GCC; the shipped userspace targets **draft RVV 0.10** on silicon that implements ratified RVV 1.0), three ways around a hard-coded `/opt/toolchain`, and the nRF Connect SDK case. Companion to [`nixos/README.md`](nixos/README.md), which is unmodified. *Added 2026-09-04* |

---

## Conventions

Guides use the repository's evidence labels: **[DOC]** vendor document · **[SCH]** schematic · **[SRC]** source code · **[FW]** firmware · **[WEB]** vendor web page · **[COM]** community report · **[INF]** inference.

Because guides **synthesise** rather than research, they carry a heavier burden of honesty about provenance. The guides added in the 2026-08-24 pass, and all three added on 2026-08-30, each end with an explicit **evidence boundary** section stating which claims are evidenced and which are recalled or inferred. **Where a guide disagrees with a linked deep record, the deep record wins.**

Guides should **link to** deep records rather than restate them. If a guide starts duplicating a component record, the content belongs in the component record.
