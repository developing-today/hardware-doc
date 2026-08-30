# Espressif ESP32-P4

- **Category:** dual-core RISC-V high-performance application MCU/SoC with in-package PSRAM — **no radio**
- **Research status:** verified against Espressif primary documents retrieved and validated locally; datasheet is a **pre-release** document (see [Documentation maturity](#11-documentation-maturity-and-what-that-costs-you))
- **Retrieved:** 2026-08-21
- **Documentation sourcing procedure:** [Espressif vendor guide](../../../vendors/espressif/README.md)

---

## 1. Identity and variants

ESP32-P4 is Espressif's first *application-processor-class* part: a dual-core 32-bit RISC-V HP (high-performance) CPU at up to 400 MHz, paired with a single-core 32-bit RISC-V LP (low-power) CPU at up to 40 MHz, with MIPI-DSI and MIPI-CSI, an ISP, an H.264 encoder, a JPEG codec, 2D-DMA and a Pixel-Processing Accelerator, USB 2.0 High-Speed OTG, Ethernet MAC and 16 or 32 MB of in-package PSRAM. **It contains no wireless radio of any kind** — see §5.

| Field | Value | Evidence |
|---|---|---|
| Marketed family name | ESP32-P4 Series | S1 |
| Orderable part numbers on the datasheet cover | **ESP32-P4NRW16X**, **ESP32-P4NRW32X** | S1 |
| Package | **QFN104, 10 × 10 mm** | S1 |
| In-package memory | 16 MB (`RW16`) or 32 MB (`RW32`) PSRAM | S1 |
| Programmable GPIOs | 55, of which five are strapping pins | S1, S2 |
| Embedded flash | **None** — external SPI flash required | S1 (no flash suffix in nomenclature) |
| Radio | **None** | S1, S2 |
| Silicon revisions published | v0.0, v1.0, v1.3, v3.0, v3.1, v3.2 | S3 |
| Modules (WROOM/MINI style) | **None published** as of 2026-08-21 | S8 (negative result, §11) |

The `NRW16`/`NRW32` element of the part number encodes *no embedded flash, in-package PSRAM of 16 or 32 MB*, following the same scheme as ESP32-S3R8 (`R8` = 8 MB in-package PSRAM). Do not read `RW32` as flash; there is no on-die or in-package flash on any ESP32-P4 variant, and every board documented here fits a separate 16 MB external SPI NOR flash.

### The "P4X" naming trap

You will see the string **ESP32-P4X** in Espressif's development-board names (`ESP32-P4X-Function-EV-Board`, `ESP32-P4X-EYE`, `ESP32-P4X-C5-Function-EV-Board`). **`ESP32-P4X` is not a chip.** No datasheet, errata document, ESP-IDF target or ordering code uses it. It is a *board*-name suffix that Espressif adopted to distinguish boards populated with **chip revision v3.1 or later** from the earlier, now end-of-life boards of the same design. Espressif states this explicitly:

> "The difference between the ESP32-P4X-Function-EV-Board and the ESP32-P4-Function-EV-Board is that the main chip on the former has been upgraded to the ESP32-P4 chip revision v3.1 or later version." — S4

The ESP-IDF target string remains `esp32p4` for all of them.

---

## 2. Architecture: the two-CPU split

ESP32-P4 is organised as two largely independent subsystems that share the pin ring and eFuse block. This is a bigger structural difference from the ESP32/ESP32-S3 line than the CPU ISA change is, and it drives most of the low-power design work on the part.

| | HP system | LP system |
|---|---|---|
| CPU | 32-bit RISC-V, **dual-core**, up to **400 MHz** | 32-bit RISC-V, **single-core**, up to **40 MHz** |
| FPU | Single-precision FPU present | No |
| ISA extensions | Espressif "Processor Instruction Extensions" (AI/DSP extensions), datasheet §4.1.1.3 | — |
| ROM | 128 KB HP ROM | 16 KB LP ROM |
| SRAM | **768 KB L2MEM** + 8 KB system SPM (scratchpad) | 32 KB LP SRAM |
| Cache | **Two-level cache** (L1 per core + shared L2) | — |
| Peripherals | Full set (§4) | LP GPIO, LP UART, LP SPI, LP I2C, LP I2S, LP ADC, touch sensor, temperature sensor, LP timers, super-WDT, LP mailbox |
| Power | HPSPM domain, gated in sleep | LPSPM domain, retained |

Evidence: S1 (block diagram, Features list), S2.

The intended pattern is that the LP core runs continuously on the retained LP domain doing sensor polling, wake decisions and touch scanning, and the two HP cores — which are what makes the part expensive in power terms — stay powered down until there is real work. `LP Mailbox` is the documented inter-system communication path. This is the same idea as the ESP32/ESP32-S3 ULP coprocessor, but with a full RISC-V core and a real peripheral set rather than a restricted FSM/RISC-V ULP.

### Reported performance

The datasheet quotes **6.92 CoreMark/MHz (dual-core)** (S1). At 400 MHz that implies roughly 2 768 CoreMark. Treat this as a vendor figure produced under Espressif's own build and configuration; it is not an independently reproduced measurement, and CoreMark says nothing about the memory-bound graphics and camera workloads that most P4 designs actually run. No independent benchmark was located during this pass.

---

## 3. Memory subsystem

| Resource | Size | Notes |
|---|---:|---|
| HP L2MEM (SRAM) | 768 KB | Usable as ordinary SRAM, or reconfigured as **L2 cache backing external PSRAM** |
| System SPM (scratchpad) | 8 KB | Zero-wait-state, called "TCM RAM" in Espressif marketing copy (S2) |
| LP SRAM | 32 KB | Retained in Deep-sleep |
| HP ROM | 128 KB | Boot ROM |
| LP ROM | 16 KB | |
| In-package PSRAM | 16 MB or 32 MB | Part-number-dependent (`NRW16` / `NRW32`) |
| External flash | not integrated | Board must supply SPI NOR flash |

Two points matter more than the raw numbers.

**The 768 KB is not simply "768 KB of RAM".** The datasheet describes L2MEM as accessible as cache when external PSRAM is available (S1, S2). The practical consequence is a *tradeoff you configure*, not a fixed budget: dedicating more L2MEM to cache raises effective PSRAM bandwidth for framebuffer work, and dedicating more to directly addressed SRAM gives you deterministic, low-latency working memory. A 1024×600 RGB565 framebuffer is 1.2 MB, so single-buffered 7-inch operation already lives in PSRAM and depends on cache behaviour; double buffering is 2.4 MB. This is the single most important sizing question on the part and it is why the 32 MB variant exists.

**The flash clock ceiling is a board-level restriction, not just a silicon one.** Espressif states on both Function-EV boards that the onboard flash "operates at a maximum clock frequency of 80 MHz and does not support the auto suspend feature", with 120 MHz and auto-suspend gated behind contacting Espressif (S4, S6). Do not assume 120 MHz flash on a P4 design without checking the specific flash part and its qualification.

---

## 4. Peripheral set

From the datasheet Features list and block diagram (S1):

**Image and video**
- MIPI-DSI (display) and MIPI-CSI (camera), both up to 1080p per Espressif's product page (S2)
- Image Signal Processor (ISP)
- **H.264 encoder**, quoted at up to 1080p @ 30 fps (S2)
- JPEG codec
- **Pixel-Processing Accelerator (PPA)** and **2D-DMA** — the GUI/blit acceleration path
- Parallel LCD and camera controller (`LCD_CAM`) for non-MIPI panels and sensors

**Audio / analog**
- Three I2S (with PDM) plus an LP I2S
- Voice Activity Detection (VAD) hardware
- ADC controller, LP ADC controller, analog voltage comparator, temperature sensor, capacitive touch sensor

**Connectivity**
- **USB 2.0 High-Speed OTG** (host or device), **USB 2.0 Full-Speed OTG**, and a separate **USB Serial/JTAG** controller
- **Ethernet MAC (EMAC)** — RMII; requires an external PHY
- **SD/MMC host controller**
- Five UARTs + LP UART; four SPIs + LP SPI; two I2Cs + LP I2C + analog I2C; **I3C master and slave**
- TWAI (CAN-compatible), MCPWM, LEDC, RMT, PCNT, PARLIO, BitScrambler
- GDMA, VDMA, 2D-DMA; SOC ETM (event-task matrix)

Three of these deserve emphasis because they are *new to the Espressif line* and are frequently the reason a design chooses P4 over S3: **MIPI-DSI/CSI**, **USB 2.0 High-Speed** (the S3 is Full-Speed only), and **Ethernet MAC**. The 2D-DMA + PPA pair is the reason LVGL performance on P4 is not comparable to a software-blit S3 port.

---

## 5. No wireless — the defining constraint

**ESP32-P4 has no Wi-Fi, no Bluetooth of any kind, and no 802.15.4.** There is no radio block anywhere in the SoC block diagram (S1), and Espressif's own product page frames connectivity entirely as something you add externally (S2):

> "If the application requires wireless connectivity, any product from the ESP32-C/S series can serve as a wireless companion chip for ESP32-P4, connecting via SPI/SDIO/UART interfaces using ESP-Hosted or ESP-AT solutions."

This is a *silicon* absence, exactly like the ESP32-S3's absence of Bluetooth Classic. No ESP-IDF version can add it.

### How this compares to the ESP32-S3 radio discussion

The [ESP32-S3R8 record](../esp32-s3r8/README.md) documents at length how a *partial* radio gap — Bluetooth LE present, Bluetooth Classic absent — forced the Waveshare knob board to fit an entire second MCU (an [ESP32-U4WDH](../esp32-u4wdh/README.md)) purely to supply BR/EDR profiles, at the cost of a second crystal, second antenna, second flash, a private inter-MCU UART protocol and a doubled flashing procedure. See [Radio capabilities and the Classic Bluetooth limitation](../esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation).

ESP32-P4 takes that pattern and makes it **the normal, intended, first-class architecture** rather than a workaround:

| | ESP32-S3 + companion (Waveshare knob board) | ESP32-P4 + companion (Espressif's own boards) |
|---|---|---|
| Why a second chip | Retrofit to recover a *missing profile* (BR/EDR) | Designed in — the main SoC has **no radio at all** |
| Transport | Private UART protocol written by the board vendor, undocumented | **ESP-Hosted** or **ESP-AT**, official Espressif frameworks over SDIO/SPI/UART |
| Host-side API | Vendor-specific | Standard ESP-IDF Wi-Fi/BLE APIs, transparently remoted |
| Second firmware image | Vendor-built, opaque | Espressif-built slave firmware, versioned with ESP-Hosted |
| Cost | Second crystal, antenna, flash, board area, permanent coupling | Same physical costs, but with supported tooling |

The physical costs are identical; what differs is that on P4 the software stack is Espressif's problem rather than yours. Both official P4 Function-EV boards carry the companion radio as a **module**, not a bare die: `ESP32-C6-MINI-1` on the [ESP32-P4X-Function-EV-Board](../../../devices/espressif/esp32-p4x-function-ev-board/README.md) and `ESP32-C6-MINI-1U` on the [ESP32-P4X-EYE](../../../devices/espressif/esp32-p4x-eye/README.md), or `ESP32-C5-MINI-1` on the [ESP32-P4X-C5-Function-EV-Board](../../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md), which is what buys that board 5 GHz Wi-Fi 6.

### Practical consequences to plan for

1. **Latency and throughput are now a bus problem.** Wi-Fi traffic crosses SDIO or SPI. SDIO 4-bit is the higher-bandwidth option and is why the boards use it; UART-based ESP-AT is far slower and is appropriate only for control-plane traffic.
2. **You maintain two firmware images.** The companion module runs ESP-Hosted slave firmware that must be flashed and version-matched to the host's ESP-Hosted component. Both P4 Function-EV boards therefore expose a dedicated *module programming connector* for the companion, separate from the P4's own USB Serial/JTAG port.
3. **Provisioning, OTA and certification all move.** RF certification attaches to the companion module. Choosing a pre-certified `-MINI-1` module rather than a bare companion die is the reason Espressif's own boards do it that way.
4. **Radio choice is a product decision made at the companion, not at the P4.** C6 gives 2.4 GHz Wi-Fi 6 + BLE 5 + 802.15.4 (Thread/Zigbee). C5 gives dual-band 2.4/5 GHz Wi-Fi 6 + BLE 5 + 802.15.4. The P4 is unchanged either way — which is precisely the advantage of the split.

The one-line rule from the S3 record still holds and now extends: **if the part number has a letter suffix after "ESP32", it does not have Classic Bluetooth — and if that suffix is "P", it has no radio at all.**

---

## 6. Security features

From the datasheet block diagram and Features (S1):

- **Secure Boot**, **Flash encryption** via XTS_AES external-memory encryption/decryption
- Accelerators: **AES**, **SHA**, **HMAC**, **RSA**, **ECC**
- **RSA Digital Signature (RSA_DS)** and **ECDSA Digital Signature (ECDSA_DS)** peripherals
- **TRNG**
- **HUK (hardware unique key) and Key Manager** — private keys are generated inside the SoC and are never visible in plaintext to software (S2)
- **TEE** block, **APM** (access permission management), **PMP and PMA** memory protection, **PMS** permission control
- **4096-bit OTP** eFuse

Two caveats you must read before relying on any of this:

- **ECDSA_DS-836 and ECDSA_DS-837 are open errata affecting signature validation** — signatures with invalid `r`/`s` values are incorrectly accepted. ECDSA_DS-836 affects **v3.0, v3.1 and v3.2**, i.e. every currently shipping revision (S3). If you are using the ECDSA_DS peripheral for verification, read the errata before designing around it.
- **ROM-770 disables Secure Download Mode on revision v3.1.** Espressif's own board documentation carries this as a boxed warning: "The ESP32-P4X-Function-EV-Board with the ESP32-P4 chip revision v3.1 does not support Secure Download. Please do not enable Secure Download Mode." (S4). Enabling it on affected silicon is not recoverable in the field.

---

## 7. Clocks, package and pin summary

| Item | Value | Evidence |
|---|---|---|
| Package | QFN104, 10 × 10 mm | S1 |
| Main crystal | 40 MHz (external) | S4 board designs; datasheet §4.1.4.3 |
| Low-power crystal | 32.768 kHz (external, optional) | S4 board designs |
| HP CPU max | 400 MHz | S1 |
| LP CPU max | 40 MHz | S1 |
| Programmable GPIOs | 55 | S1 |
| Strapping pins | 5 | S1 |

The datasheet's structural pin documentation is in §2 (`Pin Layout`, `Pin Overview`, `IO MUX Functions`, `LP IO MUX Functions`, `Analog Functions`, `Restrictions for GPIOs and LP GPIOs`, `Peripheral Pin Assignment`, `Dedicated Interface Pins`, `Power Supply`, `Pin Mapping Between Chip and Flash`) plus `Appendix A – ESP32-P4 Consolidated Pin Overview`. Boot configuration (boot mode control, `VDDO_FLASH` voltage control, ROM message printing, JTAG signal source) is §3. **The full per-pin tables are not transcribed here** — see [artifacts/esp32-p4-datasheet.pdf](artifacts/esp32-p4-datasheet.pdf) §2, §3 and Appendix A. Transcribing 55 pins × multiple IO-MUX functions from a pre-release document into a second location would create a stale copy with no upside.

For board-level pin usage, see the header-block tables in the individual board records, e.g. [ESP32-P4X-Function-EV-Board J1 header](../../../devices/espressif/esp32-p4x-function-ev-board/README.md#6-j1-header-block).

### Power-domain gotcha carried by Espressif's own boards

Both Function-EV boards ship the same warning about the P4's internal LDOs (S4, S6):

> "LDO_VO3 and LDO_VO4 are used to power certain on-board VDD domains. Users must configure the correct output voltage and enable state in software. In Light-sleep or Deep-sleep mode, if LDO_VO3 / LDO_VO4 remain enabled, the system power consumption will be relatively high. Even when turned off, the total power consumption may still exceed the typical low-power specifications listed in the chip datasheet due to the board-level power architecture."

Read that as: **the datasheet's Deep-sleep current figures are chip-level and are not achievable on the evaluation boards.** If low power matters, you must design your own power tree; the reference boards are explicitly not the model to copy for that.

---

## 8. Chip revisions

Espressif publishes six ESP32-P4 revisions under the `vM.X` scheme (S3):

| Revision | eFuse `MAC_SPI_SYS_2` [23],[5:0] | Chip marking manufacturing code | Notes |
|---|---|---|---|
| v0.0 | major 000, minor 0000 | `X A XX` | Earliest samples |
| v1.0 | major 001, minor 0000 | `X C XX` | |
| v1.3 | major 001, minor 0011 | `X E XX` | |
| v3.0 | major 011, minor 0000 | `X F XX` | |
| **v3.1** | major 011, minor 0001 | `X G XX` | Fitted to the current "P4X" boards |
| **v3.2** | major 011, minor 0010 | `X H XX` | Newest published |

Identification procedure, eFuse field names and the chip-marking diagram are in the errata document, [artifacts/esp32-p4-errata.pdf](artifacts/esp32-p4-errata.pdf), chapter *Chip Revision Identification*. **Read it before assuming which revision you have** — the marking code is a single letter in the manufacturing-code line, which is easy to overlook.

> **Unresolved conflict.** Espressif's `COMPATIBILITY.md` in the ESP-IDF repository lists ESP32-P4 revisions as only "**v1.0, v1.3** — Supported since ESP-IDF v5.3" (S7), while the errata document and the dev-kit user guides document **v3.0, v3.1 and v3.2** as real, shipping revisions (S3, S4). The two documents were retrieved on the same day. The most likely reading is that `COMPATIBILITY.md` has not been updated for the v3.x family and that v3.x inherits the "supported since v5.3" baseline, but this is an inference, not a stated fact. If you need a hard minimum-IDF answer for v3.1/v3.2 silicon, ask Espressif rather than relying on either document. Recorded rather than silently resolved.

---

## 9. Software support and minimum ESP-IDF version

| Question | Answer | Evidence |
|---|---|---|
| ESP-IDF target string | `esp32p4` | S5 |
| **Minimum ESP-IDF version** | **v5.3** | S7 (chip-support matrix: "Supported since … ESP32-P4 v5.3") |
| Practical recommendation | v5.4 or newer | see below |
| Arduino-ESP32 | Available in the 3.x series, which is built on ESP-IDF 5.x; verify per release | — |

The chip-support matrix Espressif publishes with ESP-IDF states plainly that ESP32-P4 is "supported since v5.3", while ESP32, ESP32-S2/S3, ESP32-C2/C3/C6 and ESP32-H2 are supported in every currently supported release (S7). **v5.3 is a hard floor: earlier ESP-IDF has no `esp32p4` target at all.**

In practice v5.3 is the *earliest* usable version, not the one you want. The multimedia stack that justifies choosing a P4 — `esp_lcd` MIPI-DSI panel support, `esp_cam_sensor` / MIPI-CSI, ISP, PPA, the H.264 encoder driver, and ESP-Hosted for the companion radio — matured across v5.4 and v5.5. Pick the newest release your project can accept, and pin it.

**Documentation-version caveat.** The offline programming guide retained here is **v5.3.2**, which is the newest ESP-IDF release for which Espressif publishes a PDF build for the `esp32p4` target *at all*. v5.3.3 and everything after it (v5.4.x, v5.5.x) return HTTP 404 for the PDF; only HTML docs exist. This is a *later* cutoff than the vendor guide previously recorded (it said v5.2.x) — see the [vendor guide §4](../../../vendors/espressif/README.md#4-important-finding--documents-that-migrated-off-the-legacy-path) for the corrected table. If you are building on v5.4 or v5.5, **the local PDF does not match your version**; use the HTML docs or build `docs/` from the tagged source.

---

## 10. Errata summary

Retrieved 2026-08-21 from the `esp-chip-errata` project; local copy at [artifacts/esp32-p4-errata.pdf](artifacts/esp32-p4-errata.pdf).

| Errata | Category | Affects | Summary |
|---|---|---|---|
| RMT-176 | RMT | v0.0, v1.0, v1.3 | Idle-state signal level may be wrong in RMT continuous TX mode |
| I2C-308 | I2C | v0.0, v1.0, v1.3 | I2C slave fails on multiple-read in non-FIFO mode |
| APM-560 | APM | v0.0, v1.0, v1.3, v3.0 | Unauthorised AHB access may block subsequent PSRAM or flash transactions |
| MSPI-749 | MSPI | v3.0 | Load access fault during chip power-on or Deep-sleep wake-up |
| MSPI-750 | MSPI | v3.0 | PSRAM unaligned DMA reads may return stale data on overlapping addresses |
| MSPI-751 | MSPI | v3.0 | Data errors from asynchronous timing in MSPI address-overlap detection at specific frequencies |
| ROM-764 | ROM | v3.0 | Secure Boot verification failure from incorrect buffer address in ROM |
| Analog-765 | Analog | v3.0 | Output regulators cannot generate a reliable supply when the peripheral power domain is off |
| DMA-767 | DMA | v3.0 | DMA channel 0 transaction-ID overlap causes a permission-management issue |
| **ROM-770** | ROM | **v3.1** | **Secure Download Mode flash power-on failure — do not enable Secure Download on v3.1** |
| **ROM-816** | ROM | **v3.2** | Device hang when the flash power-on sequence runs twice with the `rom_download_xpd_on` eFuse |
| **ECDSA_DS-836** | ECDSA_DS | **v3.0, v3.1, v3.2** | Signatures with invalid `r` and `s` values are incorrectly accepted |
| ECDSA_DS-837 | ECDSA_DS | v0.0, v1.0, v1.3 | Signatures with invalid `s` values are incorrectly accepted |

Per-revision affiliation was taken from the errata project's per-revision tag indexes (`_tags/v3-0.html`, `_tags/v3-1.html`, `_tags/v3-2.html`), not from a visual reading of the merged summary table, because the summary table uses row spans that make flat text extraction unreliable. The v0.0/v1.0/v1.3 rows were read from the summary table and are lower-confidence than the v3.x rows.

The two rows to internalise: **ROM-770 on v3.1** (no Secure Download Mode — Espressif repeats this warning at the top of the board user guide) and **ECDSA_DS-836 on all shipping revisions** (signature verification accepts invalid signatures). The v3.0 MSPI cluster is largely why v3.1 exists.

---

## 11. Documentation maturity, and what that costs you

The ESP32-P4 datasheet retained here is **"Pre-release v0.7"** and is watermarked **PRELIMINARY** on every page (S1). That is unusual for a part that has been shipping on retail development boards for well over a year, and it has concrete consequences:

- Electrical characteristics (§5), current consumption (§5.6) and packaging (§6) are provisional and may change between revisions of the datasheet.
- The ordering/nomenclature section may not list every variant Espressif actually sells.
- Any figure you take from it should be re-checked against the current published datasheet before a production commit. Pin the version you read — this record read **v0.7**.

By contrast the Technical Reference Manual is large and substantive (23.5 MB, the biggest Espressif TRM in this knowledge base — for comparison the ESP32-S3 TRM is 15.2 MB and the original ESP32 TRM 10.2 MB), and the errata and hardware design guidelines are actively maintained `master` builds. So the *reference* documentation is mature; the *specification* documentation is not.

**No ESP32-P4 module exists.** Probing the legacy documentation path for `esp32-p4-mini-1`, `esp32-p4-wroom-1`, `esp32-p4-module` and `esp32-p4-mini-1_mini-1u` datasheets returned the 13 745-byte soft-404 shell in every case, and Espressif's modules product page lists no P4 module (S8). Every design must therefore integrate the bare QFN104 die, which makes the [hardware design guidelines](artifacts/esp32-p4-hardware-design-guidelines.pdf) mandatory reading rather than optional — there is no pre-certified module to hide behind. This is a real barrier to entry compared with the S3, and it is one reason boards fit a *radio module* for the companion while running the P4 bare.

---

## 12. When to choose ESP32-P4, and when not to

**Choose it when** you need MIPI-DSI or MIPI-CSI, a display above roughly 800×480, hardware H.264, USB 2.0 High-Speed, Ethernet, more than ~8 MB of working memory, or a genuinely low-power always-on sensing core alongside a fast application core.

**Do not choose it when** wireless is central and the product is otherwise modest. A P4 plus a C6 module is more silicon, more board area, more power, two firmware images and a bus in the middle, versus a single ESP32-S3 that does Wi-Fi and BLE natively. If an S3 with a QSPI or RGB panel meets the requirement, it is the simpler system.

**Also weigh** the absence of a module (no pre-certified path, full RF/PI design responsibility on you), the pre-release datasheet, the v5.3 ESP-IDF floor, and the open ECDSA_DS errata.

---

## 13. Used By

| Device | Status | Role of the ESP32-P4 |
|---|---|---|
| [ESP32-P4X-Function-EV-Board](../../../devices/espressif/esp32-p4x-function-ev-board/README.md) | Current | Main SoC; 7-inch MIPI-DSI panel, MIPI-CSI camera, Ethernet, audio, USB HS; radio delegated to an ESP32-C6-MINI-1 |
| [ESP32-P4X-C5-Function-EV-Board](../../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) | Current | Same board concept with an ESP32-C5-MINI-1 for dual-band Wi-Fi 6 |
| [ESP32-P4X-EYE](../../../devices/espressif/esp32-p4x-eye/README.md) | Current | Main SoC of a hand-held camera board; MIPI-CSI 2 MP camera, SPI LCD, USB HS device |
| [ESP32-P4-Function-EV-Board](../../../devices/espressif/esp32-p4-function-ev-board/README.md) | **EOL** | Predecessor of the P4X board, chip revisions before v3.1 |
| [ESP32-P4-EYE](../../../devices/espressif/esp32-p4-eye/README.md) | **EOL** | Predecessor of the P4X-EYE |

---

## 14. Related components

- [ESP32-S3R8](../esp32-s3r8/README.md) — the natural comparison point: has the radio the P4 lacks, lacks the multimedia the P4 has. Its [Classic Bluetooth discussion](../esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation) is the precedent for §5 above.
- [ESP32-U4WDH](../esp32-u4wdh/README.md) — worked example of a companion-MCU radio retrofit, for contrast with P4's designed-in companion architecture.
- [ESP-IDF peripheral capabilities](../../../guides/espressif/esp-idf-peripheral-capabilities.md) — cross-target comparison distilled from the archived `esp32p4` Programming Guide: the 5+1 UARTs, 3 TWAI controllers, dual USB-OTG, single I2S, the UHS-I/SDMMC driver gap, `esp_wifi_remote`, and the HEX-mode / internal-LDO PSRAM configuration.
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md) — hosts, URL templates and validation procedure for every document cited here.

---

## 15. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version/date | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| S1 | ESP32-P4 Series Datasheet | Espressif Systems | primary | datasheet | https://www.espressif.com/sites/default/files/documentation/esp32-p4_datasheet_en.pdf | 2026-08-21 | **Pre-release v0.7, PRELIMINARY** | Part numbers, package, memory sizes, CPU clocks, CoreMark, peripheral list, block diagram, security blocks, absence of radio | artifacts/esp32-p4-datasheet.pdf |
| S1b | ESP32-P4 Series Datasheet, HTML rendition (used to read the text layer, which is glyph-subset obfuscated in the PDF) | Espressif Systems | primary | official page | https://documentation.espressif.com/esp32-p4_datasheet_en.html | 2026-08-21 | v0.7 as served | Same content as S1; front matter and Features list transcribed from this | — (SPA, link-only) |
| S2 | ESP32-P4 product page | Espressif Systems | primary | official page | https://www.espressif.com/en/products/socs/esp32-p4 | 2026-08-21 | as served | 768 KB SRAM/8 KB TCM framing, 1080p DSI/CSI, H.264 1080p30, PPA + 2D-DMA, 55 GPIO, security summary, **ESP-Hosted/ESP-AT companion-radio statement** | — (HTML, link-only) |
| S3 | ESP32-P4 Series SoC Errata | Espressif Systems | primary | errata | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32p4/esp-chip-errata-en-master-esp32p4.pdf | 2026-08-21 | esp-docs `master` build | Chip revision list v0.0–v3.2, eFuse and marking identification, all errata and affected revisions | artifacts/esp32-p4-errata.pdf |
| S3b | ESP Chip Errata — ESP32-P4 chip identification and per-revision tag indexes | Espressif Systems | primary | official page | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32p4/01-chip-identification/index.html and `…/_tags/v3-0.html`, `v3-1.html`, `v3-2.html` | 2026-08-21 | `master` build | Per-revision errata affiliation used in §10 | — (HTML, link-only) |
| S4 | ESP32-P4X-Function-EV-Board User Guide | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-function-ev-board/user_guide.html | 2026-08-21 | esp-dev-kits `latest`, repo commit `f6f80ab` | "P4X" = chip rev v3.1+; ROM-770 Secure Download warning; LDO_VO3/VO4 warning; 80 MHz flash restriction | — (HTML; PDF equivalent in shared artifacts) |
| S5 | ESP Hardware Design Guidelines (ESP32-P4) | Espressif Systems | primary | design guide | https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32p4/esp-hardware-design-guidelines-en-master-esp32p4.pdf | 2026-08-21 | esp-docs `master` build | Schematic/PCB design rules for the bare QFN104 part | artifacts/esp32-p4-hardware-design-guidelines.pdf |
| S6 | ESP32-P4X-C5-Function-EV-Board User Guide | Espressif Systems | primary | manual | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-c5-function-ev-board/user_guide.html | 2026-08-21 | esp-dev-kits `latest`, repo commit `f6f80ab` | Same flash and LDO restrictions; ESP32-C5-MINI-1 companion | — (HTML) |
| S7 | ESP-IDF `README.md` chip-support matrix and `COMPATIBILITY.md` | Espressif Systems | primary | repository | https://github.com/espressif/esp-idf/blob/master/README.md , https://github.com/espressif/esp-idf/blob/master/COMPATIBILITY.md , https://dl.espressif.com/dl/esp-idf/chip-support.svg | 2026-08-21 | `master` as served | **ESP32-P4 supported since ESP-IDF v5.3**; revision-compatibility table (and its v3.x gap, §8) | — (link-only) |
| S8 | Negative result: no ESP32-P4 module | Espressif Systems | primary | — | https://www.espressif.com/en/products/modules plus four probed legacy datasheet slugs | 2026-08-21 | — | No WROOM/MINI-class ESP32-P4 module is published; see [component-download-failures.txt](../../../component-download-failures.txt) | — |
| S9 | ESP32-P4 Technical Reference Manual | Espressif Systems | primary | reference manual | https://www.espressif.com/sites/default/files/documentation/esp32-p4_technical_reference_manual_en.pdf | 2026-08-21 | as served (no cover version transcribed — see caveat below) | Register-level detail for every block summarised above | artifacts/esp32-p4-technical-reference-manual.pdf |
| S10 | ESP-IDF Programming Guide, `esp32p4` target | Espressif Systems | primary | programming guide | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32p4/esp-idf-en-v5.3.2-esp32p4.pdf | 2026-08-21 | **v5.3.2** | API reference for the target; newest version with a published PDF | **archived 2026-08-24** — [record](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md); extracts in [guides](../../../guides/espressif/esp-idf-peripheral-capabilities.md) |

**Caveat on S9.** The TRM's cover version number was **not** transcribed. Espressif ships several of its PDFs with glyph-subset-obfuscated text layers that no simple offset recovers (documented in [component-download-failures.txt](../../../component-download-failures.txt)), and no PDF text-extraction tooling was available in this environment. The artifact is pinned by SHA-256 and retrieval date instead. Do not cite a TRM version number from this record; open the local file and read the cover.

---

## 16. Local artifacts

| File | Bytes | SHA-256 |
|---|---:|---|
| artifacts/esp32-p4-datasheet.pdf | 1 576 185 | `fb4f3e91cc2ac519ec08cdec3dac9cb62b546cf5402ead1c5b83595a21bb6bc6` |
| artifacts/esp32-p4-technical-reference-manual.pdf | 23 537 234 | `622fe9625d19cf00bd7aa49e65f0b5dd6ef2197f83cb7a88b4405078d6a957d4` |
| artifacts/esp32-p4-errata.pdf | 144 853 | `5fd0fec5b306873a68b0a22d2f937abfc5d3e3c90a572e0a71018a455d6b38b7` |
| artifacts/esp32-p4-hardware-design-guidelines.pdf | 1 781 833 | `54b11b53fc0431f848f10643514b4cf03225f1fd84072cb0987c89cc53db0de4` |
| ~~artifacts/esp-idf-programming-guide-v5.3.2-esp32p4.pdf~~ **archived 2026-08-24** | 13 656 675 | `adf06f5531a5c84505dcb069e28a864a653b39e0d299701c0fb905e02f2e6f65` |

All five were validated as genuine PDFs (`%PDF` magic) at download time; the staging-file download pattern from the [vendor guide §6.2(c)](../../../vendors/espressif/README.md#62-resolving-an-unknown-filename-slug) guarantees that a non-PDF response never reached the final filename.

Redistribution status for all five: **unknown** — Espressif publishes them freely without an explicit redistribution licence. Disposition: `repository`. Retained for internal engineering reference.

## 17. Documentation sourcing

Every URL above follows a pattern documented in the [Espressif vendor guide](../../../vendors/espressif/README.md). Two findings from this research pass were fed back into that guide and are worth knowing before you fetch anything else:

1. **`dl.espressif.com` *is* a documentation host** for board schematics, PCB layouts, dimension drawings and mirrored component datasheets, under `/dl/schematics/`, `/schematics/` and `/AE/esp-dev-kits/`. The vendor guide previously said it was binaries-only. Corrected — see [vendor guide §1 and §2.4](../../../vendors/espressif/README.md).
2. **The ESP-IDF PDF cutoff is v5.3.2, not v5.2.x.** Corrected in the vendor guide with the probe evidence.
