# Espressif memory maps, boot process, strapping and eFuse — ESP32 / ESP32-S3 / ESP32-P4

- **Purpose:** the hardware-level facts you need to bring a board up, choose a flash/PSRAM configuration, lay out a partition table, and read a chip revision — extracted from the **Technical Reference Manuals and datasheets held locally**.
- **Extracted:** 2026-08-24
- **Companion:** [soc-peripheral-reference.md](soc-peripheral-reference.md) covers peripheral instance counts. This page covers memory, boot, power and eFuse.

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Quoted or read directly from the cited Espressif PDF, at the cited printed page |
| **[COM]** | Community evidence, attributed and dated |
| **[INF]** | Inference or synthesis by this knowledge base |

## Sources

Same document set as [soc-peripheral-reference.md § Sources](soc-peripheral-reference.md#sources) — **TRM-32** v5.8, **DS-32** v5.3, **TRM-S3** v1.8, **DS-S3** v2.2, **TRM-P4** v0.7 `PRELIMINARY`, **DS-P4** v0.7. Page numbers are **printed** page numbers.

Additional documents cited here:

| Key | Document | Local artifact |
|---|---|---|
| **ERR-32** | ESP32 Series SoC Errata **v3.0** | [`esp32-errata.pdf`](../../components/espressif/esp32-u4wdh/artifacts/esp32-errata.pdf) |
| **ERR-S3** | ESP32-S3 Series SoC Errata **v1.3** | [`esp32-s3-errata.pdf`](../../components/espressif/esp32-s3r8/artifacts/esp32-s3-errata.pdf) |
| **HDG-32 / HDG-S3 / HDG-P4** | Hardware Design Guidelines | in each component's `artifacts/` |

---

## 1. Memory maps

### 1.1 ESP32 — flat map with split ROM and three SRAM banks

**[DOC]** DS-32 v5.3 **Table 4-1 "Memory and Peripheral Mapping", pp. 28–29**. Embedded and external memory portion:

| Category | Target | Start | End | Size |
|---|---|---|---|---|
| Embedded | Internal ROM 0 | `0x4000_0000` | `0x4005_FFFF` | 384 KB |
| | Internal ROM 1 | `0x3FF9_0000` | `0x3FF9_FFFF` | 64 KB |
| | Internal SRAM 0 | `0x4007_0000` | `0x4009_FFFF` | 192 KB |
| | Internal SRAM 1 | `0x3FFE_0000` / `0x400A_0000` | `0x3FFF_FFFF` / `0x400B_FFFF` | 128 KB |
| | Internal SRAM 2 | `0x3FFA_E000` | `0x3FFD_FFFF` | 200 KB |
| | RTC FAST Memory | `0x3FF8_0000` / `0x400C_0000` | `0x3FF8_1FFF` / `0x400C_1FFF` | 8 KB |
| | RTC SLOW Memory | `0x5000_0000` | `0x5000_1FFF` | 8 KB |
| External | External Flash | `0x3F40_0000` | `0x3F7F_FFFF` | 4 MB (data) |
| | External Flash | `0x400C_2000` | `0x40BF_FFFF` | 11 MB + 248 KB (instruction) |
| | External RAM | `0x3F80_0000` | `0x3FBF_FFFF` | 4 MB |

Peripherals occupy `0x3FF0_0000`–`0x3FF7_5FFF` (DPort view). Selected bases, useful when reading a crash dump **[DOC]** (same table):

| Peripheral | Base | | Peripheral | Base |
|---|---|---|---|---|
| DPort Register | `0x3FF0_0000` | | RMT | `0x3FF5_6000` |
| AES | `0x3FF0_1000` | | PCNT | `0x3FF5_7000` |
| RSA | `0x3FF0_2000` | | LED PWM | `0x3FF5_9000` |
| SHA | `0x3FF0_3000` | | eFuse Controller | `0x3FF5_A000` |
| Secure Boot | `0x3FF0_4000` | | Flash Encryption | `0x3FF5_B000` |
| Cache MMU Table | `0x3FF1_0000` | | TIMG0 / TIMG1 | `0x3FF5_F000` / `0x3FF6_0000` |
| UART0 | `0x3FF4_0000` | | SPI2 / SPI3 | `0x3FF6_4000` / `0x3FF6_5000` |
| SPI1 / SPI0 | `0x3FF4_2000` / `0x3FF4_3000` | | I2C1 | `0x3FF6_7000` |
| GPIO | `0x3FF4_4000` | | SDMMC | `0x3FF6_8000` |
| RTC | `0x3FF4_8000` | | EMAC | `0x3FF6_9000` (8 KB) |
| IO MUX | `0x3FF4_9000` | | TWAI | `0x3FF6_B000` |
| I2S0 | `0x3FF4_F000` | | I2S1 | `0x3FF6_D000` |
| UART1 | `0x3FF5_0000` | | UART2 | `0x3FF6_E000` |
| I2C0 | `0x3FF5_3000` | | RNG | `0x3FF7_5000` |

**⚠ Peripherals appear at two addresses.** The same registers are reachable via the **DPORT** window (`0x3FF4_0000`–`0x3FF7_FFFF`) and the **AHB** window (`0x6000_0000`–`0x6003_FFFF`), with a fixed `0x2000_0000` offset. **This duality is the root of four separate ESP32 errata** — see [errata-practical.md](errata-practical.md), which covers `CPU-3.21`, `UART-3.17` and the related DPORT read hazards.

**Cache:** *"ESP32 uses a two-way set-associative cache. Each of the two CPUs has 32 KB of cache featuring a block size of 32 bytes."* **[DOC]** DS-32 v5.3 § 4.1.5, p. 29.

### 1.2 ESP32-S3 — separate instruction and data windows

**[DOC]** DS-S3 v2.2 **Figure 4-1 "Address Mapping Structure", p. 37**:

| Range | Size | Bus | Contents |
|---|---|---|---|
| `0x0000_0000`–`0x3BFF_FFFF` | — | — | Reserved |
| `0x3C00_0000`–`0x3DFF_FFFF` | **32 MB** | Data | **External memory** (flash/PSRAM, data window) |
| `0x3FC8_8000`–`0x3FCF_FFFF` | **480 KB** | Data | Internal SRAM |
| `0x3FF0_0000`–`0x3FF1_FFFF` | **128 KB** | Data | Internal ROM |
| `0x4000_0000`–`0x4005_FFFF` | **384 KB** | Instruction | Internal ROM |
| `0x4037_0000`–`0x403D_FFFF` | **448 KB** | Instruction | Internal SRAM |
| `0x4200_0000`–`0x43FF_FFFF` | **32 MB** | Instruction | **External memory** (flash/PSRAM, instruction window) |
| `0x5000_0000`–`0x5000_1FFF` | **8 KB** | Data + Instruction | **RTC SLOW memory** (★ ULP-accessible) |
| `0x6000_0000`–`0x600D_0FFF` | 836 KB | Data + Instruction | Peripherals (RTC ★ + others) |
| `0x600F_E000`–`0x600F_FFFF` | **8 KB** | — | **RTC FAST memory** |

**Cache** — configurable, unlike ESP32 **[DOC]** DS-S3 v2.2 § 4.1.2.3, p. 39:

- Instruction cache: **16 KB (one bank) or 32 KB (two banks)**, four-way or eight-way set associative
- Data cache: **32 KB (one bank) or 64 KB (two banks)**, four-way set associative
- Block size **16 or 32 bytes** for both
- **Both caches are shared by the two CPU cores.**

> **[INF]** Cache size is a build-time trade against usable SRAM: the cache banks come *out of* the 512 KB. `CONFIG_ESP32S3_INSTRUCTION_CACHE_SIZE` / `..._DATA_CACHE_SIZE` in ESP-IDF pick this. On a PSRAM-heavy graphics workload (as on the Knob board) a larger D-cache is usually the right call; on a code-heavy, SRAM-starved workload it is not.

**External memory:** *"ESP32-S3 supports up to 1 GB of external flash and RAM"*, but through the caches only **32 MB of instruction space and 32 MB of data space at a time**, in **64 KB blocks**. Data-space access supports 8/16/32/**128**-bit reads and writes for RAM, reads only for flash. **[DOC]** DS-S3 v2.2 § 4.1.2.2, pp. 38–39.

### 1.3 ESP32-P4 — HP and LP domains

**[DOC]** DS-P4 v0.7 § 4.1.3.1, pp. 45–46:

| Block | Size | Clock | Purpose |
|---|---|---|---|
| HP ROM | **128 KB** | 200 MHz | HP CPU boot and core functions |
| HP L2MEM | **768 KB** | 200 MHz | HP CPU data and instructions |
| LP ROM | **16 KB** | 40 MHz | LP CPU boot and core functions |
| LP SRAM | **32 KB** | 40 MHz | LP CPU data and instructions |
| SPM (scratchpad) | **8 KB** | **400 MHz** | HP CPU fast access |
| eFuse | 4096 bit | — | 1792 bits reserved for user data |

**In-package PSRAM** **[DOC]** (same section):

- **16-bit data bus**, max **250 MHz**, **DDR** (both clock edges)
- Up to **64 MB**
- Hardware **XTS-AES** encryption/decryption
- Cache maps **64 KB blocks into a 64 MB** instruction or data space; 8/16/32/128-bit read *and write*
- Espressif's own bandwidth formula and worked example:
  > *"Max theoretical bandwidth (PSRAM) = line_num × edge_mode × PSRAM_max_freq … 16 × 2 × 250 MHz = 8 Gbit/s."*

**External memory:** SPI / Dual SPI / Quad SPI / QPI, **max 120 MHz**, up to **64 MB of external flash**, mapped as 64 KB blocks into a 64 MB instruction space and a 64 MB read-only data space. **[DOC]** DS-P4 v0.7 § 4.1.3.1, p. 46.

> **[INF]** The P4's memory story is the inverse of the S3's: **PSRAM is in-package and fast, external RAM is not a thing.** You do not choose a PSRAM part or an octal/quad mode — you choose a P4 variant. Conversely there is no in-package *flash* on current P4 parts, so external flash and its 120 MHz ceiling is always in play.

---

## 2. Boot process and the ROM bootloader

### 2.1 The shape of it, on all three parts **[INF]**

1. Power rails come up; `CHIP_PU` released.
2. Hardware **latches the strapping pins** ([§ 4](#4-strapping-pins-per-chip)) and holds those values until power-down.
3. The **ROM bootloader** runs from internal ROM. It reads the latched strapping bits, combined with eFuse bits, to pick a boot mode.
4. **SPI Boot:** the ROM bootloader reads the second-stage bootloader from flash into SRAM and jumps to it. The second-stage bootloader reads the partition table, selects an app (OTA slot), and starts it.
5. **Download Boot:** the ROM bootloader waits for a host over UART / USB / SPI-slave and accepts flash writes, or loads a stub into SRAM and runs it.

### 2.2 Boot mode selection

**ESP32 [DOC]** — DS-32 v5.3 **Table 3-3, p. 23**:

| Boot mode | GPIO0 | GPIO2 |
|---|---|---|
| **SPI Boot Mode** (default) | **1** | Any value |
| Joint Download Boot Mode | 0 | 0 |

Joint Download Boot supports **SDIO Download Boot** and **UART Download Boot**. **[DOC]**

> `uart_download_dis` *"permanently disables Download Boot mode when … set to 1 (valid only for ESP32 chip revisions v3.0 and higher)."* **[DOC]** DS-32 v5.3 p. 23.

**ESP32-S3 [DOC]** — DS-S3 v2.2 **Table 3-3, p. 33** gives two rows (GPIO0/GPIO46). But **TRM-S3 v1.8 Table 8.2-1, p. 535 gives three rows and two more pins**:

| Boot mode | GPIO0 | GPIO46 | GPIO1 | GPIO2 |
|---|---|---|---|---|
| **SPI Boot mode** (default) | **1** | Ignored | Ignored | Ignored |
| Joint Download Boot mode | 0 | 0 | Ignored | Ignored |
| **SPI Download Boot mode** | 0 | 1 | **1** | **0** |

> **⚠ Datasheet / TRM discrepancy.** DS-S3 v2.2 § 3.1 lists **only GPIO0 and GPIO46** as boot-mode controls and names the strapping pins as GPIO0/3/45/46. TRM-S3 v1.8 § 8.2 adds **GPIO1 and GPIO2** as boot-mode inputs for SPI Download Boot, while explicitly saying they are *not* strapping pins:
> > *"GPIO1 and GPIO2 are not strapping pins. But you need to reserve them when using SPI Download Boot mode. GPIO1 and GPIO2 are floating by default and are in a high-impedance state at reset."* **[DOC]** TRM-S3 v1.8 p. 535
>
> **The TRM is the more complete statement and does not contradict the datasheet** — the datasheet simply omits the SPI Download Boot row. **[INF] Practical rule: if you are not using SPI Download Boot, GPIO1 and GPIO2 are ordinary pins. If you might be, leave them accessible and do not hard-tie them.**

S3 SPI Boot subdivides **[DOC]** TRM-S3 v1.8 p. 535:

- **Normal Flash Boot** — supports Secure Boot. ROM loads the program from flash into SRAM and executes it (in practice, the 2nd-stage bootloader).
- **Direct Boot** — **does not support Secure Boot**; the program runs in place from flash. Enabled by making *"the first two words of the bin file downloaded to flash (address: 0x42000000) … `0xaedb041d`"*.

**ESP32-P4 [DOC]** — DS-P4 v0.7 **Table 3-3, p. 37**:

| Boot mode | GPIO35 | GPIO36 | GPIO37 | GPIO38 |
|---|---|---|---|---|
| **SPI boot mode** (default) | **1** | Any | Any | Any |
| Joint download boot mode | 0 | 1 | Any | Any |

Joint Download Boot on P4 supports **USB-Serial-JTAG**, **USB 2.0 OTG** (High-Speed controller only, operating at Full Speed), **UART0**, and **SPI Slave Download Boot**. Binaries can be downloaded into flash **or into L2MEM and executed from L2MEM**. **[DOC]** DS-P4 v0.7 p. 37.

> **⚠ [DOC]** DS-P4 v0.7 Table 3-3 note 2: *"only the USB 2.0 High-Speed OTG can be used for flashing at Full-Speed mode; the USB 2.0 Full-Speed OTG does not support device firmware upgrade."* Wire your programming connector to the HS OTG pins.

### 2.3 ROM message printing

All three route ROM-stage log output under eFuse and strapping control **[DOC]**:

| | Control | Destinations |
|---|---|---|
| ESP32 | Strapping **MTDO** | U0TXD printing on/off — DS-32 v5.3 § 3.3, p. 25 |
| ESP32-S3 | Strapping **GPIO46** + `EFUSE_UART_PRINT_CONTROL`, `EFUSE_DIS_USB_SERIAL_JTAG_ROM_PRINT` | (default) UART0 **and** USB Serial/JTAG; or USB Serial/JTAG only; or UART0 only — DS-S3 v2.2 § 3.3, p. 34 |
| ESP32-P4 | Strapping **GPIO36** + `EFUSE_UART_PRINT_CONTROL` | (default) UART0 **and** USB Serial/JTAG; or USB Serial/JTAG only; or UART0 only — DS-P4 v0.7 § 3.3, p. 38 |

### 2.4 JTAG signal source

| | Control **[DOC]** |
|---|---|
| ESP32 | eFuse `EFUSE_DISABLE_JTAG` only — DS-32 v5.3 § 3.5, p. 25 |
| ESP32-S3 | Strapping **GPIO3** + `EFUSE_DIS_PAD_JTAG`, `EFUSE_DIS_USB_JTAG`, `EFUSE_STRAP_JTAG_SEL` — DS-S3 v2.2 § 3, p. 32 |
| ESP32-P4 | Strapping **GPIO34** + `EFUSE_DIS_PAD_JTAG`, `EFUSE_DIS_USB_JTAG`, `EFUSE_JTAG_SEL_ENABLE` — DS-P4 v0.7 § 3, p. 36 |

> **[INF]** On S3 and P4 the JTAG strap picks between the **built-in USB Serial/JTAG** and **external JTAG pads**. GPIO3 (S3) / GPIO34 (P4) default to *floating* — meaning the default is whatever the eFuses say. If you fit an external JTAG probe and it does not enumerate, this strap is the first thing to check.

---

## 3. Partition table and OTA implications **[INF]**

The TRMs and datasheets do not define the partition table — that is an ESP-IDF software convention. What the *hardware* constrains:

| Hardware fact | Partitioning consequence |
|---|---|
| ESP32 maps at most **11 MB + 248 KB** of flash into instruction space and **4 MB** into data space at once (DS-32 v5.3 Table 4-1) | Practical single-app image ceiling on ESP32 is well under 11 MB; and *"if more than 3 MB + 248 KB are mapped, cache performance will be reduced due to speculative reads by the CPU"* **[DOC]** DS-32 v5.3 § 4.1.3, p. 27. **Keep the app under ~3 MB on ESP32 if you care about cache hit rate.** |
| S3 maps **32 MB instruction + 32 MB data**, in 64 KB blocks (DS-S3 v2.2 § 4.1.2.2) | The 64 KB block granularity is why partition offsets and sizes must be 64 KB-aligned for mapped partitions. |
| P4 maps **64 MB**, 64 KB blocks (DS-P4 v0.7 § 4.1.3.1) | Same alignment rule, larger ceiling. |
| Flash encryption is **XTS-AES** on S3/P4, plain AES on ESP32 | Encrypted partitions have different alignment/padding rules per scheme; check the IDF flash-encryption docs for the target. |
| eFuse is **one-time programmable** on all three | Secure Boot and Flash Encryption keys, once burned, are permanent. There is no un-burning. |

> **⚠ OTA and the app-size ceiling [INF]:** a dual-OTA layout needs `2 × app + factory (optional) + NVS + phy_init` inside the flash part. On a **4 MB** part (the ESP32-U4WDH's in-package flash — see [esp32-u4wdh README § 8](../../components/espressif/esp32-u4wdh/README.md)) with a factory app already around 1 MB, dual OTA is tight. Espressif's own default `partitions_two_ota.csv` gives each slot ~1.25 MB on a 4 MB part.

---

## 4. Strapping pins per chip

### 4.1 Summary table

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| **Count** | **5** | **4** | **5** |
| Boot mode | **GPIO0**, GPIO2 | **GPIO0**, GPIO46 (+GPIO1/GPIO2 for SPI Download Boot) | **GPIO35**, GPIO36 (+GPIO37/GPIO38) |
| Flash/PSRAM voltage | **MTDI (GPIO12)** | **GPIO45** | *(eFuse only — no strap)* |
| ROM print | MTDO (GPIO15) | GPIO46 | GPIO36 |
| JTAG source | *(eFuse only)* | GPIO3 | GPIO34 |
| SDIO slave timing | MTDO, GPIO5 | — | — |

### 4.2 Default levels at reset **[DOC]**

| ESP32 (DS-32 v5.3 Table 3-1, p. 22) | | ESP32-S3 (DS-S3 v2.2 Table 3-1, p. 32) | | ESP32-P4 (DS-P4 v0.7 Table 3-1, p. 36) | |
|---|---|---|---|---|---|
| GPIO0 | Pull-up → **1** | GPIO0 | Weak pull-up → **1** | GPIO34 | **Floating** |
| GPIO2 | Pull-down → 0 | GPIO3 | **Floating** | GPIO35 | Weak pull-up → **1** |
| MTDI | Pull-down → 0 | GPIO45 | Weak pull-down → 0 | GPIO36 | **Floating** |
| MTDO | Pull-up → **1** | GPIO46 | Weak pull-down → 0 | GPIO37 | **Floating** |
| GPIO5 | Pull-up → **1** | | | GPIO38 | **Floating** |

> **⚠ Floating straps have no defined default.** GPIO3 on S3 and GPIO34/36/37/38 on P4 are floating — an unloaded input on a real board will pick up whatever the surrounding copper does. **[INF]** If you rely on the default behaviour for any of these, fit an explicit resistor. Do not assume a floating strap reads 0.

### 4.3 Latch timing **[DOC]**

All three parts describe the same mechanism:

> *"All strapping pins have latches. At system reset, the latches sample the bit values of their respective strapping pins and store them until the chip is powered down or shut down. The states of latches cannot be changed in any other way. It makes the strapping pin values available during the entire chip operation, and the pins are freed up to be used as regular IO pins after reset."*
> — DS-32 v5.3 p. 22; near-identical wording in DS-S3 v2.2 p. 32 and DS-P4 v0.7 p. 36

| Parameter | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| **t<sub>SU</sub>** — power rails stable before `CHIP_PU` goes high | **0 ms** min | **0 ms** min | **0 ms** min |
| **t<sub>H</sub>** — hold after `CHIP_PU` high before pins become normal IO | **1 ms** min | **3 ms** min | **3 ms** min |

**[DOC]** DS-32 v5.3 Table 3-2, p. 23 · DS-S3 v2.2 Table 3-2, p. 33 · DS-P4 v0.7 Table 3-2, p. 37.

> **⚠ The t<sub>H</sub> value tripled from ESP32 to S3/P4** (1 ms → 3 ms). **[INF]** If a host MCU drives a strap and then immediately repurposes the line, an ESP32-era 1 ms delay is **not enough on an S3 or P4**. This bites when a host MCU shares a bus with a boot strap — exactly the U4WDH↔S3 topology on the Knob board. Software can also read the latched values back from `GPIO_STRAPPING` **[DOC]** (TRM-S3 v1.8 § 8.1, p. 534; TRM-P4 v0.7 § 12.1, p. 1219), which is the reliable way to confirm what the chip actually sampled.

---

## 5. Flash and PSRAM voltage — the part that destroys hardware

### 5.1 ESP32: `VDD_SDIO`, MTDI, and the 1.8 V trap

**[DOC]** DS-32 v5.3 § 3.2, p. 24:

> *"MTDI is used to select the VDD_SDIO power supply voltage at reset:*
> - *MTDI = 0 (by default), VDD_SDIO pin is powered directly from VDD3P3_RTC. Typically this voltage is 3.3 V.*
> - *MTDI = 1, VDD_SDIO pin is powered from internal 1.8 V LDO.*
>
> *This functionality can be overridden by setting `EFUSE_SDIO_FORCE` to 1, in which case `EFUSE_SDIO_TIEH` determines the VDD_SDIO voltage: `EFUSE_SDIO_TIEH` = 0 → 1.8 V LDO; = 1 → VDD3P3_RTC."*

> ### ⚠ This is the single most destructive configuration mistake on ESP32.
>
> Parts with **3.3 V in-package flash or PSRAM** — **ESP32-U4WDH** and **ESP32-D0WDRH2-V3** — require `VDD_SDIO` at 3.3 V. Strapping MTDI high (or an external pull-up, or a probe on the pin at reset) puts the internal 1.8 V LDO on a 3.3 V memory die. The chip enumerates and the flash reads as all-ones.
>
> **This knowledge base already documents the full failure mode, the forum thread where Espressif staff diagnosed it, and the eFuse recovery** — see **[esp32-u4wdh README §§ 18.3–18.4](../../components/espressif/esp32-u4wdh/README.md)**. It is not duplicated here.
>
> **[INF] Design rule: on any ESP32 with in-package 3.3 V memory, leave MTDI/GPIO12 with its internal pull-down and put nothing on it. If you must use GPIO12, burn `EFUSE_SDIO_FORCE=1` + `EFUSE_SDIO_TIEH=1` first, before wiring anything to the pin.**

Related: the minimum `VDD_SDIO` in 3.3 V mode is **3.0 V** for parts with 3.3 V embedded flash, versus **2.3 V** otherwise — DS-32 v5.3 Table 5-2 note 2 **[DOC]**, as recorded in [esp32-u4wdh § 18.4](../../components/espressif/esp32-u4wdh/README.md).

### 5.2 ESP32-S3: `VDD_SPI`, GPIO45

**[DOC]** DS-S3 v2.2 **Table 3-4, p. 34**:

| VDD_SPI power source | Voltage | `EFUSE_VDD_SPI_FORCE` | GPIO45 | `EFUSE_VDD_SPI_TIEH` |
|---|---|---|---|---|
| **VDD3P3_RTC via R<sub>SPI</sub>** | **3.3 V** (default) | 0 | **0** | ignored |
| VDD3P3_RTC via R<sub>SPI</sub> | 3.3 V | 1 | ignored | 1 |
| Flash Voltage Regulator | **1.8 V** | 0 | **1** | ignored |
| Flash Voltage Regulator | 1.8 V | 1 | ignored | 0 |

GPIO45 defaults to **weak pull-down**, i.e. **3.3 V**. **[INF]** The same class of mistake as § 5.1 is possible — pulling GPIO45 high at reset switches an S3's flash/PSRAM rail to 1.8 V. The S3 is somewhat more forgiving because most S3 modules pair 3.3 V flash with 1.8 V-capable octal PSRAM and Espressif sets the eFuse at module level, but **on a bare S3R8 you own this choice**. Check `EFUSE_VDD_SPI_*` with `espefuse.py summary` before trusting the strap.

### 5.3 ESP32-P4: `VDDO_FLASH`, eFuse only

**[DOC]** DS-P4 v0.7 § 3.2 and **Table 3-4, p. 38**:

> *"ESP32-P4 supplies power to flash via VDDO_FLASH, which outputs 3.3 V by default. After burning `EFUSE_0PXA_TIEH_SEL_0`, the output changes to 1.8 V."*

| VDDO_FLASH source | `EFUSE_0PXA_TIEH_SEL_0` | Voltage |
|---|---|---|
| Flash LDO | **0** | **3.3 V** (default) |
| Flash LDO | 2 | 1.8 V |

> **[INF] P4 removes the strapping-pin hazard entirely** — there is no GPIO that can change the flash rail. This is a deliberate improvement over ESP32/S3. The trade-off is that switching to a 1.8 V flash part is **irreversible** (eFuse). Note the table's odd `0` / `2` values rather than `0` / `1`; that is what the pre-release datasheet prints.

### 5.4 Hardware design guidelines

Each part's Hardware Design Guidelines PDF is held locally and carries the decoupling, R<sub>SPI</sub>, crystal and reset-network requirements that go with the above:

- [`esp32-hardware-design-guidelines.pdf`](../../components/espressif/esp32-u4wdh/artifacts/esp32-hardware-design-guidelines.pdf) (38 pp.)
- [`esp32-s3-hardware-design-guidelines.pdf`](../../components/espressif/esp32-s3r8/artifacts/esp32-s3-hardware-design-guidelines.pdf) (42 pp.)
- [`esp32-p4-hardware-design-guidelines.pdf`](../../components/espressif/esp32-p4/artifacts/esp32-p4-hardware-design-guidelines.pdf) (32 pp.)

---

## 6. Sleep modes and RTC memory retention

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Power modes | **5**: Active, Modem-sleep, Light-sleep, Deep-sleep, **Hibernation** | **4**: Active, Modem-sleep, Light-sleep, Deep-sleep | Active / Light-sleep / Deep-sleep with per-module power options |
| Deep-sleep current | **10 µA** | **7 µA** | — |
| RTC memory in Deep-sleep | **retained** | **retained** | LP SRAM retained |
| ULP coprocessor | ULP-FSM | **ULP-FSM + ULP-RISC-V** | LP RISC-V core @ 40 MHz |

**[DOC]** DS-32 v5.3 "Features" p. 4 (*"Five power modes… Power consumption in Deep-sleep mode is 10 µA… RTC memory remains powered on in Deep-sleep mode"*); DS-S3 v2.2 "Features" p. 4 (*"Four power modes… 7 µA… RTC memory remains powered on in Deep-sleep mode"*).

### RTC memory: two blocks, different rules **[DOC]** DS-32 v5.3 § 4.1.2, p. 26

- **RTC FAST Memory — 8 KB.** *"can be used for data storage; it is accessed by the main CPU during RTC Boot from the Deep-sleep mode."*
- **RTC SLOW Memory — 8 KB.** *"can be accessed by the ULP coprocessor during the Deep-sleep mode."*

DS-S3 v2.2 § 4.1.2.1, pp. 38–39 gives the S3 equivalents, both 8 KB, both *"can retain data in Deep-sleep mode"*, with RTC SLOW additionally accessible by coprocessors.

> **[INF] Mapping to ESP-IDF:** `RTC_DATA_ATTR` / `RTC_NOINIT_ATTR` place variables in RTC SLOW; `RTC_FAST_ATTR` and deep-sleep wake stubs (`RTC_IRAM_ATTR`) live in RTC FAST. You have **8 KB each**, not 16 KB of one thing. Wake stubs and retained state compete for different budgets.

> **⚠ ESP32 Deep-sleep trap [DOC]** ERR-32 v3.0 § 3.9 **[ULP-3.19]**, p. 13 — the ULP coprocessor and touch sensors **cannot be used in Deep-sleep if the `RTC_PERIPH` power domain is powered up**, and EXT0 wake-up **requires** `RTC_PERIPH` powered up. **You must choose: EXT0 wake, or ULP/touch. Not both.** Affects every ESP32 revision including v3.1. Detail in [errata-practical.md](errata-practical.md#ulp-319--ulptouch-and-ext0-wake-are-mutually-exclusive-in-deep-sleep).

> **⚠ ESP32-S3 Light-sleep trap [DOC]** ERR-S3 v1.3 § 3.3 **[ANALOG-160]**, p. 7 — an analog power configuration reachable when using ULP and/or touch in sleep **permanently damages the chip**. Bypassed in ESP-IDF ≥ v4.4.2. See [errata-practical.md](errata-practical.md#analog-160--the-one-that-destroys-the-chip).

---

## 7. eFuse and chip revision detection

### 7.1 Why you care **[INF]**

Almost every entry in [errata-practical.md](errata-practical.md) is revision-scoped. Before you decide whether a workaround applies, you need to know which revision is in front of you. All three parts encode revision in eFuse and mirror it in the chip and module markings.

### 7.2 ESP32 — five revisions, four eFuse fields

The revision is *"encoded using four eFuse fields"* **[DOC]** ERR-32 v3.0 § 1.2, p. 1:

| | eFuse bit | v0.0 | v1.0 | v1.1 | v3.0 | v3.1 |
|---|---|---|---|---|---|---|
| **Major** | `APB_CTRL_DATE[31]` | 0 | 0 | 0 | 1 | 1 |
| | `EFUSE_BLK0_RDATA5[20]` | 0 | 0 | 0 | 1 | 1 |
| | `EFUSE_BLK0_RDATA3[15]` | 0 | 1 | 1 | 1 | 1 |
| **Minor** | `EFUSE_BLK0_RDATA5[25]` | 0 | 0 | 0 | 0 | 0 |
| | `EFUSE_BLK0_RDATA5[24]` | 0 | 0 | 1 | 0 | 1 |

**[DOC]** ERR-32 v3.0 Table 1.1, p. 1.

Without powering the part, read the markings **[DOC]** ERR-32 v3.0 Tables 1.2 and 1.3, pp. 2–3:

| Revision | Chip marking (Espressif Tracking Information) | Module marking (Specification Identifier) |
|---|---|---|
| v0.0 | `XXXXXXXX` | `XXXXXX` ¹ |
| v1.0 | `X B XXXXXX` | `XXXXXX` |
| v1.1 | `X F XXXXXX` | `MF XXXX` |
| **v3.0** | `X E XXXXXX` | `ME XXXX` |
| **v3.1** | `X G XXXXXX` | `MG XXXX` |

> ¹ *"To distinguish between v0.0 and v0.1, please check the eFuse bits."* **[DOC]**

**Note the numbering-scheme change.** ERR-32 v3.0 § 1.1, p. 1 **[DOC]**: *"The vM.X scheme replaces previously used chip revision schemes, including ECOx numbers, Vxxx, and other formats."* Major number changing means *"the software used for the previous version of the product is incompatible"*; minor number changing means it is compatible.

Local artifacts covering this transition: [`ar2022-005-chip-revision-numbering-scheme.pdf`](../../components/espressif/esp32-u4wdh/artifacts/ar2022-005-chip-revision-numbering-scheme.pdf), [`pcn20220901-esp32-chip-revision-upgrade.pdf`](../../components/espressif/esp32-u4wdh/artifacts/pcn20220901-esp32-chip-revision-upgrade.pdf), [`esp32-chip-revision-v3-0-user-guide.pdf`](../../components/espressif/esp32-u4wdh/artifacts/esp32-chip-revision-v3-0-user-guide.pdf).

**The full ESP32 v3.0/v3.1 story as it applies to the U4WDH — including the dual-core PCN and the AES fault-injection advisory — is already written up in [esp32-u4wdh README § 21](../../components/espressif/esp32-u4wdh/README.md).** This page does not duplicate it.

### 7.3 ESP32-S3 — three revisions, two eFuse fields

*"The chip revision is encoded using two eFuse fields"* **[DOC]** ERR-S3 v1.3 § 1.2, p. 1:

| | eFuse bit | v0.0 | v0.1 | v0.2 |
|---|---|---|---|---|
| **Major** | `EFUSE_RD_MAC_SPI_SYS_5_REG[25]` | 0 | 0 | 0 |
| | `EFUSE_RD_MAC_SPI_SYS_5_REG[24]` | 0 | 0 | 0 |
| **Minor** | `EFUSE_RD_MAC_SPI_SYS_5_REG[23]` | 0 | 0 | 0 |
| | `EFUSE_RD_MAC_SPI_SYS_3_REG[20]` | 0 | 0 | 0 |
| | `EFUSE_RD_MAC_SPI_SYS_3_REG[19]` | 0 | 0 | **1** |
| | `EFUSE_RD_MAC_SPI_SYS_3_REG[18]` | 0 | **1** | 0 |

Markings **[DOC]** ERR-S3 v1.3 Tables 1.2, 1.3, pp. 2–3:

| Revision | Chip marking | Module marking |
|---|---|---|
| v0.0 | `X A XXXXXX` | `—` ¹ |
| v0.1 | `X B XXXXXX` | `M0 XXXX` |
| **v0.2** | `X C XXXXXX` | `MC XXXX` |

> ¹ *"Missing specification identifier '—' means modules with this chip revision are not mass produced."* **[DOC]**

> **[INF]** All shipping ESP32-S3 silicon is **major revision 0**. Every errata in ERR-S3 v1.3 affects all three minors except `USBOTG-4289`, which is fixed *in some batches* of v0.2. There is no "good" S3 revision to wait for — you work around, in software, on all of them.

### 7.4 Additional identification: Date Code and PW Number

Some issues are fixed at manufacturing, not at silicon-revision level, and are identified differently **[DOC]** ERR-S3 v1.3 § 1.3, p. 3:

- **Date Code** in the chip marking — used for `USBOTG-4289` (chips before Date Code **2219**).
- **PW Number** on the module product label — used for the same issue (modules before **PW-2022-06-XXXX**). *"PW Number is only provided for reels packaged in aluminum moisture barrier bags (MBB)."*

### 7.5 eFuse sizes

| | Total | Available to user | Citation **[DOC]** |
|---|---|---|---|
| ESP32 | **1024 bit** | **768 bit** | DS-32 v5.3 § 4.1.2, p. 26 |
| ESP32-S3 | **4096 bit** | **1792 bit** | DS-S3 v2.2 § 4.1.2.1, p. 39 |
| ESP32-P4 | **4096 bit** | **1792 bit** | DS-P4 v0.7 § 4.1.3.2, p. 47 |

All three: *"Once an eFuse bit is programmed to 1, it can never be reverted to 0."* **[DOC]** P4 additionally offers *"Configurable write protection / Configurable read protection / Various hardware encoding schemes against data corruption"* (DS-P4 v0.7 § 4.1.3.2, p. 47).

### 7.6 ESP32-P4 revisions

DS-P4 v0.7 has a **§ 1.3 "Chip Revision"** section (p. 11). Given the pre-release status of the whole document, revision identification for P4 should be re-checked against a released datasheet and the P4 errata — see [esp32-p4 README § 8](../../components/espressif/esp32-p4/README.md#8-chip-revisions) which already tracks this.

---

## 8. Extraction notes

Text-layer quality and page-numbering caveats are identical to those recorded in [soc-peripheral-reference.md § 15](soc-peripheral-reference.md#15-extraction-notes-and-text-layer-quality): all documents extract cleanly with `pdftotext -layout`; **figures do not extract** (they are vector/raster with no recoverable text).

Specifically **not** recoverable from the text layer, and therefore *not* reproduced here:

- **DS-32 v5.3 Figure 4-1** and **DS-P4 v0.7 Figure 4-1** "Address Mapping Structure" — the graphical bus diagrams. The *tables* accompanying them (DS-32 Table 4-1) did extract; DS-S3 v2.2's Figure 4-1 extracted as readable column text and is transcribed in § 1.2.
- **DS-32 v5.3 Figure 3-2 "Chip Boot Flow"** — the Joint Download Boot flowchart. Prose around it extracted; the flowchart itself did not.
- **Figure 3-1** in all three datasheets (strapping-pin timing waveform). The associated timing *table* (Table 3-2) extracted and is in § 4.3.

Nothing needed for the decisions on this page was lost.

---

## Related

- [SoC peripheral reference](soc-peripheral-reference.md) — peripheral instance counts, per chip, with citations
- [Errata, practical](errata-practical.md) — which silicon bugs bite, per revision
- [ESP-IDF peripheral capabilities](esp-idf-peripheral-capabilities.md)
- [esp32-u4wdh README](../../components/espressif/esp32-u4wdh/README.md) — §§ 18.3–18.5 (VDD_SDIO / 1.8 V trap, PSRAM), § 21 (v3.0/v3.1 silicon revisions)
- [esp32-s3r8 README](../../components/espressif/esp32-s3r8/README.md)
- [esp32-p4 README](../../components/espressif/esp32-p4/README.md) — § 3 (memory subsystem), § 8 (chip revisions)
