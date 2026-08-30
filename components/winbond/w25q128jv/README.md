# Winbond W25Q128JV family

- **Category:** 128 Mbit (16 MB) serial NOR flash, 2.7–3.6 V, Standard/Dual/Quad SPI with XIP
- **Research status:** verified against the board schematic, the vendor `sdkconfig`, and the Winbond datasheet retrieved into `artifacts/`. **The full 12-digit ordering code is now decoded field by field from Winbond's own §11.1 table** — previously the suffix was recorded as "the package/order variant shown in the schematic".
- **Retrieved:** 2026-08-21

## Variants covered by this record

This is a **family record**. Two ordering variants of the same die appear across the devices
documented here, and **Winbond publishes one datasheet covering both** —
`artifacts/w25q128jv-datasheet-rev-f.pdf`. They were previously filed as two separate component
records holding byte-identical copies of that datasheet; merged on **2026-08-30**.

| Variant | Package | Grade | QE bit | Fitted on | Was filed at |
|---|---|---|---|---|---|
| **`W25Q128JVPIQ`** | **WSON-8**, 6 × 5 mm (code `P`) | Industrial `I` | **Hard-wired to 1** (code `Q`) | `U3`, [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) | `components/winbond/w25q128jvpiq/` |
| **`W25Q128JVS`** | **SOIC-8**, 208 mil (code `S`) | — | not hard-wired | `U9`, [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) | `components/winbond/w25q128jvs/` |

Both decode through the same §11.1 ordering table (§1 below). **The package difference is not
cosmetic:** the SOIC-8 part on the Tanmatsu can be clipped and read or reflashed in-circuit with a
standard SOIC-8 test clip, whereas the WSON-8 part on the Knob board is a leadless package that
generally has to be hot-air removed to reach it externally.

Unless a section says otherwise, everything below was established on the **`JVPIQ`** part on the
Waveshare board — that is where the schematic, `sdkconfig` and partition evidence came from. The
Tanmatsu integration facts are in [§ Used By](#used-by).

---

`U3` on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md). This is the **ESP32-S3's application flash** — the thing that holds the bootloader, partition table, app, NVS and SPIFFS/LittleFS. It is Waveshare's headline "16MB Flash".

Two facts do most of the work in this document:

- The trailing **`Q`** means **the Quad Enable bit is hard-wired to 1 in silicon**. Quad I/O works with no configuration, and `/HOLD` does not exist. §1.1.
- Despite that, and despite all four data lines being wired, **the vendor's own `sdkconfig` runs the flash in DIO mode**, using half the available bandwidth. §6.2.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[SCH]** | Read directly off the board schematic PNGs in `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/` |
| **[DOC]** | Stated by Winbond in `artifacts/w25q128jv-datasheet-rev-f.pdf`, or by Espressif in the ESP32-S3 documents under `../../espressif/esp32-s3r8/artifacts/` |
| **[SRC]** | Read out of Waveshare's own example tree in the device's `artifacts/demo/` |
| **[INF]** | Inference. Not established by the above |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marked part | `W25Q128JVPIQ` | **[SCH]** symbol name on `U3` |
| Reference designator | **U3** | **[SCH]** |
| Density | **128 Mbit = 16 MiB = 16 777 216 bytes** | **[DOC]** |
| Package | **WSON-8, 6 × 5 mm** | **[DOC]** §11.1, package code `P` |
| Top-side marking | **`25Q128JVPQ`** (Winbond abbreviates the 12-digit part number to 10 digits on the package) | **[DOC]** §11.1 |
| Temperature grade | **Industrial, −40 °C to +85 °C** | **[DOC]** §11.1, grade code `I` |
| Supply | 2.7–3.6 V | **[DOC]** generation code `V` |
| JEDEC ID (`9Fh`) | **`EF 40 18`** | **[DOC]** §8.1.1, the `-IQ/JQ` row |
| Device ID (`ABh`, `90h`, `92h`, `94h`) | **`17h`** | **[DOC]** §8.1.1 |
| Datasheet | W25Q128JV, **Revision F**, 2018-03-27 | **[DOC]** |
| Lifecycle | Active, and the single most widely second-sourced 16 MB SPI NOR part in existence | **[WEB]** 2026-08-21 |

### 1.1 The full ordering code, decoded

**[DOC]** §11.1 ordering table and the part-number breakdown diagram. This supersedes the earlier record's "`PIQ` denotes the package/order variant".

| `W25Q` | `128J` | `V` | `P` | `I` | `Q` |
|---|---|---|---|---|---|
| SpiFlash family | 128 Mbit, **JV** generation | **2.7–3.6 V** | **WSON-8, 6 × 5 mm** | **Industrial, −40…+85 °C** | **QE = 1 fixed** |

The other values you may meet:

| Field | Codes | Meaning |
|---|---|---|
| Package | `S` = SOIC-8 208-mil · `F` = SOIC-16 300-mil · **`P` = WSON-8 6×5 mm** · `E` = WSON-8 8×6 mm · `B`/`C` = TFBGA-24 8×6 mm · `Y` = 24-ball WLCSP | |
| Grade | **`I` = Industrial (−40…+85 °C)** · `J` = Industrial Plus (−40…+105 °C) | |
| Feature | **`Q`** = Green package **with `QE` = 1 (fixed) in Status Register-2**; `/HOLD` disabled so Standard/Dual/Quad all work with no user setting. **Backward compatible with the FV family** · `M` = Green package with **`QE` = 0 (programmable)**, and a **different JEDEC ID** so the JV family can be identified | |

### 1.2 ⚠ `Q` versus `M` — the difference that actually bites

This is the most practically important thing in the ordering code, and it changes the JEDEC ID:

| Variant | `QE` bit | `/HOLD` pin | JEDEC ID (`9Fh`) |
|---|---|---|---|
| **`…IQ` / `…JQ` (this board)** | **Hard-wired 1** | **Disabled** — the pin is `IO3` and nothing else | **`EF 40 18`** |
| `…IM` / `…JM` | Programmable, **defaults 0** | Available in Standard/Dual SPI | **`EF 70 18`** |

Consequences for this board:

- **Quad I/O works from the very first instruction.** No bootloader has to program a status register to enable it, and there is no window where a reset mid-write could leave `QE` cleared. **[DOC]**
- **There is no `/HOLD` function.** Pin 7 is `IO3`, permanently. Do not look for a hold line.
- **If you ever substitute an `-IM` part, the ESP32-S3 flash driver has to set `QE` itself** before QIO/QOUT modes work, and the JEDEC ID changes from `EF4018` to `EF7018`. ESP-IDF handles both, but any tooling or test that hard-codes `EF4018` will break. **[INF]**

### 1.3 ⚠ This is *not* the S3's PSRAM

The [ESP32-S3R8](../../espressif/esp32-s3r8/README.md) has **8 MB of PSRAM in-package**, on a *separate* octal SPI interface (`CONFIG_SPIRAM_MODE_OCT`, `CLK_IO=30`, `CS_IO=26` **[SRC]**). The 16 MB here is **flash**, non-volatile, and slow to write. The two are frequently conflated in marketing copy for this board. Neither substitutes for the other.

---

## 2. Key specifications that matter in practice

**[DOC]** from `artifacts/w25q128jv-datasheet-rev-f.pdf`.

| Parameter | Value | Note |
|---|---|---|
| Organisation | 65 536 pages × 256 bytes | The **256-byte page** is the program granularity |
| Erase granularity | **4 KB sector**, 32 KB block, 64 KB block, chip | 4 KB is what ESP-IDF's `esp_partition_erase_range` and SPIFFS/LittleFS use |
| Max SPI clock | **133 MHz** for Standard/Dual/Quad | ⇒ 266 Mbit/s Dual, 532 Mbit/s Quad. The ESP32-S3 will not go this fast — §6.2 |
| Program/erase endurance | **100 000 cycles** per sector, minimum | See §7.3 |
| Data retention | **20 years** | |
| Security registers | 3 × 256 bytes, OTP-lockable | Useful for per-unit serial numbers |
| Unique ID | **64-bit**, factory-programmed, read with `4Bh` | The cleanest per-device identifier on this board |
| SFDP | JEDEC-standard Serial Flash Discoverable Parameters, read with `5Ah` | How ESP-IDF auto-detects geometry |
| Continuous Read / XIP | 8/16/32/64-byte wrap; true execute-in-place | This is how the S3 runs code directly from flash |
| Hardware `/RESET` pin | **Only on SOIC-16 and TFBGA packages** | **This board's WSON-8 has none.** §7.2 |

---

## 3. Instruction set — the parts you will actually touch

**[DOC]** §8. Full listing in the datasheet; this is the working subset.

| Opcode | Instruction | Note |
|---|---|---|
| `9Fh` | Read JEDEC ID | Returns `EF 40 18` here. Your first bring-up command |
| `4Bh` | Read Unique ID (64-bit) | |
| `5Ah` | Read SFDP register | |
| `05h` / `35h` / `15h` | Read Status Register-1 / -2 / -3 | SR-1 bit 0 is `BUSY`; SR-2 bit 1 is `QE` (fixed 1 here) |
| `01h` / `31h` / `11h` | Write Status Register-1 / -2 / -3 | |
| `06h` | Write Enable | Required before every program/erase |
| `50h` | Write Enable for Volatile Status Register | |
| `03h` | Read Data | Low speed, no dummy cycles |
| `0Bh` | Fast Read | 8 dummy cycles |
| `3Bh` / `6Bh` | Fast Read Dual / Quad **Output** | Address on IO0 only |
| `BBh` / `EBh` | Fast Read Dual / Quad **I/O** | Address on all lines. **`EBh` is what QIO mode uses** |
| `02h` | Page Program (≤ 256 bytes) | |
| `32h` | Quad Input Page Program | |
| `20h` / `52h` / `D8h` / `C7h` | Sector Erase 4 KB / Block 32 KB / Block 64 KB / Chip Erase | |
| `77h` | Set Burst with Wrap | Underpins Continuous Read/XIP |
| `ABh` | Release Power-down / read Device ID (`17h`) | |
| `66h` + `99h` | Enable Reset + Reset Device | **The only reset available on this board** — §7.2 |

**You will almost never issue these by hand.** §6.

---

## 4. Exact wiring on this board

**[SCH]**. `U3` sits on the ESP32-S3's *dedicated* SPI0/1 flash interface, not on a general-purpose SPI host.

| Flash pin (WSON-8) | Name | Net | ESP32-S3 signal |
|---:|---|---|---|
| 1 | `/CS` | `SPICS0` | Dedicated flash chip select |
| 2 | `DO (IO1)` | `SPIQ` | |
| 3 | `/WP (IO2)` | `SPIWP` | |
| 4 | `GND` | GND | |
| 5 | `DI (IO0)` | `SPID` | |
| 6 | `CLK` | `SPICLK` | |
| 7 | `/HOLD or /RESET (IO3)` | `SPIHD` | **`/HOLD` is disabled on the `Q` variant** — §1.2 |
| 8 | `VCC` | **`VDD_SPI`** | The S3's internal flash-voltage rail |

> **⚠ Do not bit-bang these pins, and do not allocate them to an SPI host.** They belong to the ESP32-S3's ROM/cache hardware. On the ESP32-S3 they are not exposed as ordinary GPIOs and any attempt to reconfigure them crashes execution from flash immediately. This is why they do not appear in the [S3 GPIO map](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md).

`VCC` from `VDD_SPI` means the flash rail is generated inside the S3 and is 3.3 V here (the S3R8's PSRAM is 1.8 V octal, but that is a separate rail). **[INF]** — the schematic shows the net name but not the voltage; confirm from the ESP32-S3 datasheet's `VDD_SPI` section if it matters to you.

There is **no** flash reset line, no write-protect strap and no external pull-ups drawn on this device **[SCH]**.

---

## 5. Partition layout as shipped

**[SRC]** from `artifacts/demo/…/ESP-IDF/08_LVGL_Test/sdkconfig`:

| Setting | Value |
|---|---|
| `CONFIG_ESPTOOLPY_FLASHSIZE` | **`16MB`** ✅ matches the part |
| `CONFIG_ESPTOOLPY_FLASHMODE` | **`dio`** ⚠ §6.2 |
| `CONFIG_ESPTOOLPY_FLASHFREQ` | `80m` |
| `CONFIG_ESPTOOLPY_FLASH_MODE_AUTO_DETECT` | `y` |

Individual examples ship their own `partitions.csv` / `user.csv`. Because the part is 16 MB, you have room that most ESP32 projects do not: a dual-OTA layout with a multi-megabyte SPIFFS/LittleFS partition for LVGL assets, fonts and audio fits comfortably.

---

## 6. Firmware and APIs

### 6.1 You do not write a driver for this

Nothing in an ordinary application talks to `U3` directly. The stack is:

| Layer | What it does |
|---|---|
| **ROM bootloader** | Reads the first-stage image using the mode/freq/size nibbles in the image header at `0x0000` |
| **Second-stage bootloader** | Re-configures the SPI flash controller, verifies the app, jumps to it |
| **`esp_flash` / `spi_flash`** (`esp_flash.h`, `spi_flash_mmap.h`) | Chip detection via `9Fh`/SFDP, read/write/erase, memory mapping for XIP |
| **`esp_partition`** (`esp_partition.h`) | The API you should actually use — `esp_partition_find`, `_read`, `_write`, `_erase_range` |
| **NVS, SPIFFS, LittleFS, FATFS, OTA** | Built on `esp_partition` |
| **Arduino** | `Preferences` (NVS), `SPIFFS`/`LittleFS`, `Update` (OTA), `EEPROM` (emulated in NVS) |

ESP-IDF **already knows this chip**: `spi_flash_chip_winbond.c` is in-tree and is selected automatically from the JEDEC ID. There is nothing to install, no component to add, no library to pick. If a tutorial tells you to add a "W25Q128 library" to an ESP32-S3 project, it is describing an *external* flash chip on a general-purpose SPI bus — a different situation entirely.

Useful runtime checks:

~~~c
#include "esp_flash.h"
#include "esp_partition.h"
#include "spi_flash_mmap.h"

uint32_t id = 0, size = 0;
ESP_ERROR_CHECK(esp_flash_read_id(NULL, &id));      // expect 0x00EF4018
ESP_ERROR_CHECK(esp_flash_get_size(NULL, &size));   // expect 16 * 1024 * 1024
ESP_LOGI(TAG, "flash jedec=0x%06" PRIx32 " size=%" PRIu32 " bytes", id, size);
~~~

and from the host:

~~~sh
esptool --chip esp32s3 --port /dev/ttyACM0 flash_id
#   Manufacturer: ef
#   Device: 4018
#   Detected flash size: 16MB
~~~

> Note the port: the ESP32-S3 enumerates over **native USB** (`/dev/ttyACM*`), not through the [CH340X bridge](../../wch/ch340x/README.md), which serves the *other* MCU.

### 6.2 ⚠ The vendor ships DIO, not QIO — and all four data lines are wired

`CONFIG_ESPTOOLPY_FLASHMODE_DIO=y` **[SRC]**, yet the schematic connects `SPIWP` (IO2) and `SPIHD` (IO3) **[SCH]**, and the fitted part has `QE` hard-wired to 1 **[DOC]**. So the hardware is fully capable of QIO and the software is asking for half of it.

Why? Not stated anywhere in the vendor material. Two plausible reasons, both **[INF]**:

- **Caution around octal PSRAM.** This board uses `CONFIG_SPIRAM_MODE_OCT=y` with `SPIRAM_FETCH_INSTRUCTIONS` and `SPIRAM_RODATA` enabled **[SRC]**. Flash and PSRAM share the S3's SPI0/1 hardware, and the combination of QIO flash with OPI PSRAM has historically been the fussier configuration.
- **Copy-paste from a generic Waveshare template.** DIO is the safest default that works on every part regardless of `QE` state.

**What to do:** QIO is worth testing — it roughly doubles instruction-fetch bandwidth from flash, which is directly visible in LVGL redraw rates on a 360 × 360 panel. Change `CONFIG_ESPTOOLPY_FLASHMODE_QIO=y`, rebuild, and confirm the board still boots and that `esp_flash_get_size()` still reports 16 MB. **If it does not boot, revert** — this is exactly the kind of change that produces a brick-until-reflash, and there is no hardware flash reset to fall back on (§7.2). Record the result here if you try it.

`CONFIG_ESPTOOLPY_FLASHFREQ_80M` is the right choice: the part is good to 133 MHz **[DOC]** so 80 MHz has margin, and 120 MHz on the S3 is an experimental feature with its own temperature caveats.

---

## 7. Gotchas and pitfalls

### 7.1 Program/erase is slow and blocking

A 4 KB sector erase is on the order of milliseconds and a chip erase is on the order of tens of seconds **[DOC]**. During any flash write, **XIP from flash is suspended** — code that is not in IRAM cannot execute. On this board that matters because:

- **LVGL redraws will stutter** during NVS commits or OTA writes unless the rendering path is in IRAM or PSRAM.
- **ISRs that are not `IRAM_ATTR` will not run.** If you write to flash from one task while another handles the rotary encoder, you will drop encoder edges. Mark encoder and touch ISRs `IRAM_ATTR`.
- The knob's `bidi_switch_knob` driver and the CST816 touch path are the two most likely victims. **[INF]**

### 7.2 ⚠ There is no hardware reset for the flash

The `/RESET` pin exists **only on the SOIC-16 and TFBGA packages** **[DOC]** §4.6. This board's **WSON-8 does not have one**. The only resets available are:

- the software reset pair `66h` + `99h`, issued by the ESP32-S3's flash driver, and
- **power cycling the board.**

Practical consequence: if the flash is left in an odd state — mid-Continuous-Read, or in QPI mode when the bootloader expects SPI — an ESP32 `CHIP_PU` reset alone may not recover it, because `CHIP_PU` does not reach the flash. **Fully power-cycle before concluding a board is bricked.** **[INF]**

### 7.3 Endurance is finite and NVS is not free

100 000 erase cycles per sector **[DOC]**. NVS wear-levels within its partition, but a naïve `nvs_set_*` + `nvs_commit()` on every encoder detent will chew through a sector. Buffer in RAM and commit on a timer or on shutdown.

### 7.4 Other pitfalls

1. **Confusing the 16 MB flash with the 8 MB PSRAM.** §1.3.
2. **`CONFIG_ESPTOOLPY_FLASHSIZE` set to less than 16 MB.** Partitions beyond the configured size are silently inaccessible. Waveshare gets this right **[SRC]**; downstream projects often do not.
3. **Assuming `/WP` write protection exists in hardware.** `SPIWP` is `IO2`. There is no write-protect strap on this board **[SCH]**. Protection is Status-Register-based only.
4. **Expecting `/HOLD`.** Disabled on the `Q` variant. §1.2.
5. **Hard-coding JEDEC ID `EF4018`.** True for this part, false for an `-IM` substitute (`EF7018`). §1.2.
6. **Trying to use `SPICS0`/`SPICLK`/`SPID`/`SPIQ`/`SPIWP`/`SPIHD` as GPIOs.** §4.
7. **Flash encryption / Secure Boot without a plan.** Both are one-way eFuse operations on the S3 and will make the board unrecoverable if you get them wrong. Not enabled in the factory image.
8. **Assuming 133 MHz.** That is the *flash's* limit, not the S3's practical operating point. 80 MHz is what ships.

---

## 8. Alternatives and drop-in compatibility

The WSON-8 6×5 mm SPI NOR footprint is one of the most standardised in the industry. Almost anything in the list below drops in, provided it is 2.7–3.6 V and has `QE` set (or your bootloader sets it).

| Part | Relationship | Drop-in? |
|---|---|---|
| **W25Q128JVPIM** | Same die family, `QE` **programmable**, JEDEC `EF7018` | ✅ Mechanically. ⚠ Bootloader must set `QE`; ID changes |
| **W25Q128JVPJQ** | Same, **Industrial Plus** −40…+105 °C | ✅ Straight upgrade if you need the temperature range |
| **W25Q128JVSIQ** | Same die, **SOIC-8 208-mil** | ❌ Different footprint |
| **W25Q128JVFIQ** | Same die, **SOIC-16** — **has a real `/RESET` pin** | ❌ Different footprint, but the right answer if §7.2 bothers you |
| **W25Q64JV / W25Q256JV** | 8 MB / 32 MB in the same footprint | ✅ Electrically. ⚠ **W25Q256 is >16 MB and needs 4-byte addressing**; ESP-IDF supports it but the configuration differs |
| **W25Q128FV** | Previous generation. The `Q` variant is explicitly documented as **"backward compatible to FV family"** **[DOC]** | ✅ |
| **GigaDevice GD25Q128** | Very common second source | ✅ ESP-IDF has `spi_flash_chip_gd.c` |
| **Macronix MX25L12835F** | Second source | ✅ ESP-IDF has `spi_flash_chip_mxic.c` |
| **ISSI IS25LP128** | Second source | ✅ ESP-IDF has `spi_flash_chip_issi.c` |
| **XMC / Zbit / BoyaMicro 128 Mbit** | Budget second sources, common on Chinese boards | ⚠ Usually work via the generic driver, but SFDP quality varies. **[WEB]** community reports of marginal parts at 80 MHz |
| **W25Q128JW** | **1.8 V** variant | ❌ **Wrong voltage.** Will not work on a 3.3 V `VDD_SPI` |

---

## 9. Open questions

| Question | Status |
|---|---|
| Does QIO mode work reliably alongside the S3R8's octal PSRAM on this board? | **Open, and worth testing.** §6.2 |
| What voltage does `VDD_SPI` actually run at here? | **[INF]** 3.3 V from the `JV` part being a 2.7–3.6 V device. Not stated on the schematic |
| Fitted date code / die revision | **Open.** Not readable from any published image. The `9Fh`/`4Bh` reads in §6.1 give you what actually matters |
| Is the on-board part genuine Winbond or a re-marked second source? | **Open.** `esptool flash_id` returning `ef 4018` is strong but not conclusive evidence — clones copy the ID. `4Bh` Unique ID uniqueness across units would be a better check **[INF]** |

---

## Manufacturer

**Winbond** — see the [Winbond documentation-sourcing guide](../../../vendors/winbond/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

### `W25Q128JVPIQ` — Waveshare ESP32-S3-Knob-Touch-LCD-1.8

[Device record](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — reference designator **`U3`**, the ESP32-S3's application flash, on the dedicated SPI0/1 flash interface powered from `VDD_SPI`. Marketed as "16MB Flash". See [Pinouts and buses § Bus inventory](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md).

### `W25Q128JVS` — Nicolai Electronics Tanmatsu

> Merged in from the former `components/winbond/w25q128jvs/` record on 2026-08-30.
> **Nothing in this subsection was verified on hardware**, and no separate datasheet copy was ever
> retained for it — the family datasheet in `artifacts/` covers this variant.

| | |
|---|---|
| Reference designator | `U9` |
| Role | Sole flash for the **ESP32-P4** — bootloader, firmware A/B, AppFS and FAT |
| Package | **SOIC-8** (208 mil) — externally clippable, see the variants table above |
| LCSC | [`C97521`](https://www.lcsc.com/search?q=C97521) |
| Layout | 2 MB firmware A, 2 MB firmware B, **8 MB AppFS**, 3.9 MB FAT — see [`development.md`](../../../devices/nicolai-electronics/tanmatsu/development.md) |
| Note | Secure boot is **permanently disabled** on this design, so the first 8 KB is unused |

Device record: [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) · BOM: [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md) · pinouts: [`pinouts-and-buses.md`](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md)

Board-level integration details come from the Tanmatsu production BOM (CERN-OHL-P), the Badge.Team
BSP (MIT) and badge.team documentation, all retrieved 2026-08-24.

> Being a **discrete SOIC-8 part rather than in-package flash** has a practical benefit on a
> hackable device: it can be read, reprogrammed or replaced with an external programmer and a clip,
> independently of whatever state the main SoC is in. This is the sharpest contrast with the
> Knob board's WSON-8 part.

## Related components

- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the host, and the source of the separate 8 MB **PSRAM** this part is often confused with
- [Espressif ESP32-U4WDH](../../espressif/esp32-u4wdh/README.md) — the other MCU, whose 4 MB flash is **in-package** and not board-accessible
- [microSD / SDMMC interface](../../generic/micro-sd-sdmmc/README.md) — the board's other, removable, storage

---

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| **Winbond W25Q128JV Datasheet, Revision F** (2018-03-27) — §4.6 reset, §7.1 status registers, §8.1.1 IDs, §8.2 instructions, §11.1 ordering | https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf | 2026-08-21 | `artifacts/w25q128jv-datasheet-rev-f.pdf` |
| Winbond W25Q128JV product page | https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/?__locale=en&partNo=W25Q128JV | 2026-08-21 | – |
| ESP-IDF SPI Flash API reference | https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/api-reference/peripherals/spi_flash/index.html | 2026-08-21 | – |
| ESP-IDF partition-table documentation | https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32s3/api-guides/partition-tables.html | 2026-08-21 | – |
| ESP-IDF Winbond flash chip driver (`spi_flash_chip_winbond.c`) | https://github.com/espressif/esp-idf/blob/master/components/spi_flash/spi_flash_chip_winbond.c | 2026-08-21 | – |
| Board schematic archive | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
| Official demo archive — `ESP-IDF/08_LVGL_Test/sdkconfig` (flash mode/size/freq as shipped) | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` |
| JEDEC JESD216 (SFDP) overview | https://www.jedec.org/standards-documents/docs/jesd216b | 2026-08-21 | – |
