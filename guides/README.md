# Guides

Cross-cutting notes that do not belong to a single chip or board. Per-part records live under [`components/`](../components/README.md); per-board records live under [`devices/`](../devices/README.md); procedures for *obtaining* documents live under [`vendors/`](../vendors/README.md).

| Area | Contents |
|---|---|
| [Espressif](espressif/README.md) | **Ecosystem and product lines** (the family map: which chip, which radio, which ISA) · **SoC peripheral reference** (the numeric ESP32 / S3 / P4 tables, extracted from the TRMs) · **Practical errata** · **Memory and boot** · ESP-IDF cross-target peripheral capabilities · ESP-ADF audio pipelines and memory budget · ESP-IoT-Solution display/touch/knob/USB components |
| [**Hardware subsystems**](hardware/README.md) | **E-paper displays** (waveforms, bias rails, VCOM, ghosting, temperature, the NDA boundary) · **Display interfaces** (SPI / QSPI / parallel / MIPI-DSI / e-paper, bandwidth and framebuffer arithmetic, TE lines, LVGL, every documented controller) |
| [Reverse engineering](reverse-engineering/netlists-from-vendor-eda-files.md) | **Recovering netlists from vendor EDA files** — KiCad PCB/schematic and EAGLE XML, and what a recovered netlist reliably reveals |
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

### Research technique — [`research/`](research/finding-projects-that-use-a-board.md)

| Page | One line |
|---|---|
| [Finding projects that use a board or component](research/finding-projects-that-use-a-board.md) | Search by **dependency**, not product name; authenticated GitHub code search — the technique that took one board's known projects from two to a dozen |

### Host platform — [`nixos/`](nixos/README.md)

| Page | One line |
|---|---|
| [NixOS as an embedded development host](nixos/README.md) | ESP-IDF, Arduino, PlatformIO and proprietary UI editors on NixOS — including why installing the `esp-idf-full` *package* alone yields no `idf.py`, package availability in the locked nixpkgs with dated absences, and why LVGL and sensor libraries are project dependencies rather than system packages |

---

## Conventions

Guides use the repository's evidence labels: **[DOC]** vendor document · **[SCH]** schematic · **[SRC]** source code · **[FW]** firmware · **[WEB]** vendor web page · **[COM]** community report · **[INF]** inference.

Because guides **synthesise** rather than research, they carry a heavier burden of honesty about provenance. The guides added in the 2026-08-24 pass, and all three added on 2026-08-30, each end with an explicit **evidence boundary** section stating which claims are evidenced and which are recalled or inferred. **Where a guide disagrees with a linked deep record, the deep record wins.**

Guides should **link to** deep records rather than restate them. If a guide starts duplicating a component record, the content belongs in the component record.
