# ESP-IDF peripheral capabilities and constraints — ESP32 vs ESP32-S3 vs ESP32-P4

- **Purpose:** cross-target comparison of the three Espressif SoCs documented in this knowledge base, extracted from the target-specific ESP-IDF Programming Guide PDF builds before those PDFs were archived.
- **Extracted:** 2026-08-24
- **Scope note:** this page records what the *ESP-IDF Programming Guide* states. It is a **software** document. Where it defers to the chip TRM, this page says so rather than inventing a number.

## Sources

Every fact below cites one of these. All three were target-specific PDF builds (Espressif renders a separate PDF per chip target, so prose such as "ESP32-P4 contains 3 TWAI controller(s)" is generated from that target's SOC capability header).

| Key | Document | Version / build | Pages | Regenerate from |
|---|---|---|---|---|
| **IDF-32** | ESP-IDF Programming Guide, target `esp32` | v5.1.4, built 2024-05-09 | 3006 | `https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32/esp-idf-en-v5.1.4-esp32.pdf` |
| **IDF-32b** | ESP-IDF Programming Guide, target `esp32` | v5.2.5, built 2025-02-26 | 3292 | `https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32/esp-idf-en-v5.2.5-esp32.pdf` |
| **IDF-S3** | ESP-IDF Programming Guide, target `esp32s3` | v5.2.5, built 2025-02-26 | 3244 | `https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/esp-idf-en-v5.2.5-esp32s3.pdf` |
| **IDF-S3a** | ESP-IDF Programming Guide, target `esp32s3` | v5.1.4, built 2024-05-09 | 2870 | `https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32s3/esp-idf-en-v5.1.4-esp32s3.pdf` |
| **IDF-P4** | ESP-IDF Programming Guide, target `esp32p4` | v5.3.2, built 2024-12-05 | 2262 | `https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32p4/esp-idf-en-v5.3.2-esp32p4.pdf` |

Archive record and checksums: [ARCHIVED-FRAMEWORK-GUIDES.md in esp32-u4wdh](../../components/espressif/esp32-u4wdh/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md), [in esp32-s3r8](../../components/espressif/esp32-s3r8/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md), [in esp32-p4](../../components/espressif/esp32-p4/artifacts/ARCHIVED-FRAMEWORK-GUIDES.md).

---

## 1. ⚠ Read this before using this page for peripheral counts

**The ESP-IDF Programming Guide is not a reliable source for peripheral instance counts.** It renders capability macros *symbolically*, not numerically. Representative example, identical in all three targets' builds:

> "`mcpwm_timer_config_t::group_id` specifies the MCPWM group ID. The ID should belong to **[0, SOC_MCPWM_GROUPS - 1]** range."
> — IDF-32 § *MCPWM*, p. 1218; same wording in IDF-S3 and IDF-P4

The same applies to `SOC_PCNT_UNITS_PER_GROUP`, `SOC_PCNT_CHANNELS_PER_UNIT`, `SOC_LEDC_TIMER_BIT_WIDTH`, `SOC_TIMER_GROUP_TOTAL_TIMERS`, `SOC_SPI_MAXIMUM_BUFFER_SIZE` and `SOC_RSA_MAX_BIT_LEN`. The guide additionally states the counts explicitly *do not* live in it:

> "Different ESP chip series might have different number of PCNT units and channels. **Please refer to the [TRM] for details.** The driver does not forbid you from applying for more PCNT units and channels, but it returns error when all available hardware resources are used up."
> — IDF-S3 § *Pulse Counter (PCNT)*, footnote 1, p. 1224

> "Different ESP chips might have different numbers of independent timer groups, and within each group, there might be several independent timers."
> — IDF-P4 § *GPTimer* → *Resource Allocation*

**Therefore:** for RMT channel counts, PCNT unit/channel counts, MCPWM group counts and timer-group counts, the authoritative local documents are the **Technical Reference Manuals and datasheets, which this knowledge base retains**:

- [`components/espressif/esp32-u4wdh/artifacts/esp32-technical-reference-manual.pdf`](../../components/espressif/esp32-u4wdh/artifacts/esp32-technical-reference-manual.pdf)
- [`components/espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual.pdf`](../../components/espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual.pdf)
- [`components/espressif/esp32-p4/artifacts/esp32-p4-technical-reference-manual.pdf`](../../components/espressif/esp32-p4/artifacts/esp32-p4-technical-reference-manual.pdf)

This is itself a useful finding: it is *why* the TRMs are the scarce, high-value documents here and the framework guides were not.

The rest of this page records the counts and limits the guide **does** state numerically in prose, plus the target differences and gotchas — which is where the guide genuinely adds value over the TRM.

---

## 2. Peripheral instance counts stated numerically in the guide

Counts below are quoted verbatim from each target's own build. A blank cell means that target's build does not state the number in prose (consult the TRM).

| Peripheral | ESP32 | ESP32-S3 | ESP32-P4 | Citations |
|---|---|---|---|---|
| **I2C controllers ("ports")** | **2** | **2** | **2** | IDF-32 p. 1127 · IDF-S3 p. 1046 · IDF-P4 p. 382 |
| **I2S peripherals** | **2** | **2** | **1** | IDF-32 p. 1145 · IDF-S3 p. 1071 · IDF-P4 p. 407 |
| **SPI peripherals** | **3** ("ESP32 integrates 3 SPI peripherals") | — (enumerates `SPI2_HOST`, `SPI3_HOST`) | — (enumerates `SPI2_HOST`, `SPI3_HOST`) | IDF-32 p. 1370 · IDF-S3 p. 1328 · IDF-P4 p. 731 |
| **TWAI (CAN) controllers** | **1** | **1** | **3** | IDF-32 p. 1421 · IDF-S3 p. 1390 · IDF-P4 p. 794 |
| **UART controllers** | **3** | **3** | **5** regular **+ 1 LP UART** | IDF-32 p. 1439 · IDF-S3 p. 1413 · IDF-P4 p. 817 |
| **ADC units** | **2** | **2** | **2** | IDF-32 p. 1046 · IDF-S3 p. 959 · IDF-P4 p. 259 |
| **DAC channels** | **2** | *none* | *none* | IDF-32 p. 1080 (DAC chapter absent from S3/P4 builds) |
| **Analog comparator units** | — | — | **2** | IDF-P4 p. 281 |
| **SDMMC host slots** | **2** (slot 0 = 8-bit, slot 1 = 4-bit) | **2** (both 1/4/8-line) | **2** (both 1/4/8-line) | IDF-32 p. 1314 · IDF-S3 p. 1268 · IDF-P4 p. 672 |
| **USB-OTG controllers** | *none* | **1** (Full-Speed) | **2** — one **HS**, one **FS** | IDF-S3 p. 2626 · IDF-P4 p. 850 |
| **USB Serial/JTAG controller** | *none* | **1** | **1** | IDF-S3 p. 2808 · IDF-P4 p. 2008 |
| **LEDC timers per speed mode** | **4** | **4** | **4** | IDF-32 p. 1205 · IDF-S3 p. 1158 · IDF-P4 p. 525 |

> **ESP32 has no USB peripheral of any kind.** The DAC and USB rows above are the clearest illustration of why the U4WDH board fits a separate USB-UART bridge, and why the ESP32-S3 cannot drive an analogue output without an external codec.

---

## 3. Target differences and gotchas

### 3.1 LEDC — the ESP32 high-speed mode is unique

> "LEDC channels are divided into two groups of 8 channels each. One group of LEDC channels operates in high speed mode…"
> — IDF-32 § *LED Control (LEDC)*, p. 1198

On **ESP32** there are therefore **16 LEDC channels in two speed-mode groups** (high-speed and low-speed), each group with its own 4 timers. High-speed channels change duty automatically in hardware.

On **ESP32-S3** and **ESP32-P4** the guide states flatly:

> "Speed mode (value must be `LEDC_LOW_SPEED_MODE`)"
> — IDF-S3 p. 1150; IDF-P4 p. 517

**Consequence:** LEDC code written for the ESP32 that requests `LEDC_HIGH_SPEED_MODE` — including much backlight-dimming and RGB-LED example code — will not port to the S3 or P4 unchanged. The guide's generic parameter docs carry the warning "not all targets support high speed mode" (IDF-S3 p. 1155 et al.).

### 3.2 SDMMC — the slots differ substantially in kind

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Slot 0 | **8-bit**, uses `HS1_*` pins in the **PIN MUX** (fixed pins) | 1/4/8-line, via **GPIO matrix** | **Dedicated to UHS-I**, *"not yet supported in the driver"* |
| Slot 1 | **4-bit**, uses `HS2_*` pins in the PIN MUX (fixed pins) | 1/4/8-line, via GPIO matrix | 1/4/8-line via GPIO matrix, **non-UHS-I usage** |
| Pin routing | **Fixed** — no GPIO matrix | **Any GPIO** | **Any GPIO** (slot 1) |

ESP32 carries an explicit hardware warning:

> "Pins used by Slot 0 (`HS1_*`) are also used to connect the SPI flash chip in ESP32-WROOM and ESP32-WROVER modules. These pins cannot be shared… To use Slot 0, connect SPI flash to different pins and set eFuses accordingly."
> — IDF-32 § *SDMMC Host Driver*, p. 1315

**Consequence:** on ESP32, slot 0 is effectively unusable on any standard module — you get one 4-bit slot on fixed pins. On S3/P4 the GPIO matrix removes the pin constraint entirely. On **P4**, note additionally:

> "On ESP32-P4, SDMMC host requires an **external power supply for the IO voltage**."
> — IDF-P4 § *SDMMC Host Driver*, p. 672

Supported speed modes are identical in wording on S3 and P4: Default Speed (20 MHz), High Speed (40 MHz), and High Speed DDR (40 MHz, 4-line, 3.3 V eMMC only) — IDF-S3 p. 1268.

### 3.3 I2S — PDM TX restriction is the same on all three

> "PDM TX is only supported on **I2S0** and it only supports **16-bit** width sample data."
> — IDF-32 p. 1148; IDF-S3 p. 1074; IDF-P4 p. 410 (identical wording)

Since **ESP32-P4 has only one I2S peripheral**, this is not a constraint there; on ESP32 and ESP32-S3 it means PDM microphone output cannot be moved to I2S1. Headers are split per mode: `i2s_std.h`, `i2s_pdm.h`, `i2s_tdm.h` (all three targets).

### 3.4 ESP32-P4 has no radio — `esp_wifi_remote`

> "ESP32-P4 does not support Wi-Fi functionality natively, but it is possible to use the same Wi-Fi API and features using Wi-Fi expansion. The principle of Wi-Fi Expansion operation is to add another ESP32 series, Wi-Fi capable, target connected to the ESP32-P4 in a pre-defined way."
> — IDF-P4 § 4.27 *Wi-Fi Expansion*, p. 2010

Entry point is a managed component, not a built-in:

```
idf.py add-dependency esp_wifi_remote
```

The guide points at `examples/protocols/mqtt/tcp/` and says to choose "Wi-Fi connection" in the project configuration menu. This is the software counterpart to the ESP32-C5-MINI-1 / ESP32-C6-MINI-1U companion modules fitted on the P4 boards documented here.

### 3.5 Cache coherency — neither S3 nor P4 has it

> "1. Hardware based cache Coherent Interconnect, **ESP32-S3 does not have such ability**."
> — IDF-S3 p. 2257
> "1. Hardware based cache Coherent Interconnect, **ESP32-P4 does not have such ability**."
> — IDF-P4 p. 1615

This appears in the DMA/`async_memcpy` discussion and is the reason DMA buffers must be explicitly aligned and written back.

### 3.6 No SWD on any of them

> "…take note that the ESP32 does not support SWD."
> — IDF-32 p. 2476; identical statements for ESP32-S3 (p. 2673) and ESP32-P4 (p. 1875)

JTAG only. Relevant when selecting a debug probe.

### 3.7 UART wakeup

> "ESP32 does not support wakeup from UART2."
> — IDF-32 p. 2246; the same note is reproduced in the S3 and P4 builds

---

## 4. PSRAM configuration — the biggest per-target divergence

This is where the three chips differ most, and it is genuinely well documented in the guide (the TRM does not cover the software configuration).

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Line mode (`CONFIG_SPIRAM_MODE`) | Quad (QPI only) | **Quad** or **Octal** (`_QUAD` / `_OCT`) | **16-line / HEX only** (`CONFIG_SPIRAM_MODE_HEX`) |
| Clock speeds offered | 40 / 80 MHz | **40 / 80 / 120 MHz** | **20 / 200 MHz** |
| Power | Shares flash rail; **1.8 V vs 3.3 V must match flash** | Shares flash rail | **Internal LDO channel 2**, 1.9 V domain |
| ECC | — | `CONFIG_SPIRAM_ECC_ENABLE` — costs **1/16 of total PSRAM** | — |
| XiP from PSRAM | — | — | `CONFIG_SPIRAM_XIP_FROM_PSRAM` |

### 4.1 ESP32 — the 1.8 V trap (can destroy hardware)

> "Some PSRAM chips are 1.8 V devices and some are 3.3 V. **The working voltage of the PSRAM chip must match the working voltage of the flash component.** … For a 1.8 V PSRAM chip, make sure to either set the **MTDI pin to a high signal level on bootup**, or program ESP32 eFuses to always use the VDD_SIO level of 1.8 V. **Not doing this can damage the PSRAM and/or flash chip.**"
> — IDF-32 § *Support for External RAM*, p. 2443

### 4.2 ESP32 — the 64 Mbit PSRAM silicon bug and 2T mode

> "Enable this option to fix single bit errors inside 64Mbit PSRAM. Some 64Mbit PSRAM chips have a hardware issue in the RAM which causes **bit errors at multiple fixed bit positions**. Note: If this option is enabled, the **64Mbit PSRAM chip will appear to be 32Mbit in size**. Applications will not be affected unless they use the `esp_himem` APIs, which are not supported in 2T mode."
> — IDF-32 `CONFIG_SPIRAM_2T_MODE`, p. 1635

So the ESP-PSRAM64 workaround **halves usable PSRAM**. Also: ESP-IDF "only supports Espressif branded PSRAM chips (e.g. ESP-PSRAM32, ESP-PSRAM64)" — p. 2443.

### 4.3 ESP32-S3 — 120 MHz Octal PSRAM is temperature-fragile

> "**Quad PSRAM 120 MHz is stable.** **Octal PSRAM 120 MHz is an experimental feature**, it works when the temperature is stable. *Risks: If your chip powers on at a certain temperature, then after the temperature increases or decreases by approximately **20 Celsius degrees** (depending on the chip), the accesses to / from PSRAM will **crash randomly**.*"
> — IDF-S3 `CONFIG_SPIRAM_SPEED`, p. 1686

This directly concerns the **ESP32-S3R8**, whose 8 MB in-package PSRAM is octal. Running it at 120 MHz is not a safe default for a product that sees ambient swings. `CONFIG_SPIRAM_ECC_ENABLE` is the mitigation, at the cost of 1/16 of the array (S3 p. 1686).

### 4.4 ESP32-P4 — PSRAM is powered by an internal LDO

> "The **LDO channel 2** can be used to power the PSRAM chip. If the PSRAM chip is not powered by ESP internal LDO, you can disable this option. Then you will free up one LDO channel for other general purpose."
> — IDF-P4 `CONFIG_ESP_LDO_RESERVE_PSRAM`, p. 1071

`CONFIG_ESP_LDO_CHAN_PSRAM_DOMAIN` has **range "from 2 to 2"** — i.e. it is fixed to channel 2 — and `CONFIG_ESP_LDO_VOLTAGE_PSRAM_DOMAIN` offers **1.9 V**. The SPI NOR flash LDO domain is separately configured at **3.3 V** (`CONFIG_ESP_LDO_VOLTAGE_SPI_NOR_FLASH_3300_MV`, p. 1071).

**Consequence:** on ESP32-P4 one of the four internal LDO channels is consumed by PSRAM by default. This is the software side of the LDO_VO3/VO4 warning already recorded in the [ESP32-P4 component record](../../components/espressif/esp32-p4/README.md).

P4 XiP is also distinctive:

> "If enabled, firmware in flash including instructions and data will be **moved into PSRAM on startup**, firmware code will execute directly from PSRAM. With this option enabled, code that requires execution during an MSPI1 Flash operation does not have to be placed in IRAM."
> — IDF-P4 `CONFIG_SPIRAM_XIP_FROM_PSRAM`, p. 1078

Benchmarks in the P4 build were run "at a CPU frequency of **360 MHz** and a SPIRAM clock frequency of…" (p. 472) — useful as an indication of Espressif's own reference operating point.

---

## 5. Flash operation constraints (all targets)

> "In a **single-core** setup, the SDK needs to disable interrupts or scheduler before performing the flash operation. In a **dual-core** setup, the SDK needs to make sure that **both CPUs are not running any code from flash**."
> — IDF-S3 § *SPI Flash API* → *Concurrency Constraints*, p. 1297

This is the root cause of the familiar "cache disabled" class of crashes: any ISR that must run during a flash write has to be in IRAM (`ESP_INTR_FLAG_IRAM` + `IRAM_ATTR`), or on P4, moved to PSRAM via XiP (§ 4.4).

---

## 6. API entry points worth knowing, by peripheral

Component/header names as given in the guides. These are stable across v5.1–v5.3 unless noted.

| Peripheral | Header(s) | Notes |
|---|---|---|
| I2S standard | `driver/i2s_std.h` | New (v5.x) driver; `i2s_common.h` for channel alloc |
| I2S PDM | `driver/i2s_pdm.h` | TX restricted to I2S0, 16-bit (§ 3.3) |
| I2S TDM | `driver/i2s_tdm.h` | |
| GPTimer | `driver/gptimer.h` | Replaces the legacy timer-group driver |
| PCNT | `driver/pulse_cnt.h` | Units + channels; per-unit **glitch filter**; watch points |
| MCPWM | `driver/mcpwm_prelude.h` | Timer / operator / comparator / generator objects, all group-scoped |
| RMT | `driver/rmt_tx.h`, `driver/rmt_rx.h` | Channels independently configurable TX **or** RX |
| LEDC | `driver/ledc.h` | See § 3.1 for the speed-mode divergence |
| SDMMC | `driver/sdmmc_host.h`, `sdmmc_cmd.h` | `SDMMC_HOST_SLOT_0` / `_1` |
| SPI master | `driver/spi_master.h` | `SPI2_HOST`, `SPI3_HOST` |
| TWAI | `driver/twai.h` | Standard (11-bit) + Extended (29-bit) frame formats, all targets |
| ADC oneshot | `esp_adf`-independent: `esp_adc/adc_oneshot.h` | `ADC_BITWIDTH_9` … `ADC_BITWIDTH_13` enumerated |
| ADC continuous | `esp_adc/adc_continuous.h` | |
| DAC (ESP32 only) | `driver/dac_oneshot.h`, `dac_continuous.h`, `dac_cosine.h` | "The DAC on ESP32 has two channels… separate soft-…" IDF-32 p. 1079 |
| Async memcpy (DMA) | `esp_private/esp_async_memcpy.h` → public `esp_async_memcpy.h` | See § 3.5 on coherency |
| Wi-Fi on P4 | `esp_wifi_remote` (managed component) | § 3.4 |

### PCNT capability summary (software view)

The guide describes the PCNT programming model even though it withholds the counts:

> "Each unit is in effect an independent counter with multiple channels… **By combining the usage of both edge and level signals, a PCNT unit can act as a quadrature decoder.** Besides that, PCNT unit is equipped with a **separate glitch filter**, which is helpful to remove noise from the signal."
> — IDF-S3 § *Pulse Counter (PCNT)*, p. 1224

Documented sub-features: Resource Allocation, **Watch Points** (trigger an event when the count reaches a set value), glitch filter, and explicit Enable/Disable of the unit. This matters for the knob board — see [ESP-IoT-Solution components § Knob](esp-iot-solution-components.md#3-knob--software-pcnt-for-rotary-encoders) for when to use hardware PCNT versus the software `iot_knob` component.

---

## 7. Related records

- [ESP32-U4WDH component record](../../components/espressif/esp32-u4wdh/README.md)
- [ESP32-S3R8 component record](../../components/espressif/esp32-s3r8/README.md)
- [ESP32-P4 component record](../../components/espressif/esp32-p4/README.md)
- [ESP-ADF audio pipelines](esp-adf-audio-pipelines.md)
- [ESP-IoT-Solution components](esp-iot-solution-components.md)
- [Espressif vendor documentation-sourcing guide](../../vendors/espressif/README.md)
