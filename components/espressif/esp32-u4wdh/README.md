# Espressif ESP32-U4WDH

- **Category:** Wi-Fi + Bluetooth Classic/BLE MCU with in-package (embedded) 4 MB flash
- **Research status:** verified against the board schematic, both factory firmware images and linked primary Espressif material
- **Retrieved:** 2026-08-21 (firmware/schematic re-analysis 2026-08-22)

This is the **secondary** MCU on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md). It is not a module — it is a bare 48-pin QFN silicon package soldered directly to the board as reference designator **U14**, with its own crystal, its own antenna, its own USB-UART bridge and its own firmware image. It exists on this board for one reason: **the ESP32-S3 has no Bluetooth Classic radio**, and this product is a Bluetooth audio/AVRCP knob. Everything below follows from that.

## Evidence labelling

Every non-obvious claim in this document carries one of these markers. Do not promote a claim from one class to another without new evidence.

| Marker | Meaning |
|---|---|
| **[SCH]** | Read directly off the official board schematic PNGs in `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/` |
| **[FW]** | Extracted from the official factory firmware binaries (image headers, partition table, embedded log/format strings) |
| **[DOC]** | Stated by Espressif in a document retrieved into `artifacts/` or in a cited PCN |
| **[INF]** | Inference or convention. Explicitly **not** established by the above. Treat as a hypothesis to verify on hardware |
| **[WEB]** | Retrieved from a non-Espressif web source — distributor catalogue, aggregator, vendor page. Always dated at point of retrieval. Commercial data goes stale fast; re-check before relying on it |
| **[COM]** | Community evidence — forum thread, GitHub issue, blog, video. Note **who** said it: an Espressif-staff forum post carries close to **[DOC]** weight; an anonymous post carries very little. Both appear below and are labelled |

> **Sections 13–20 were added 2026-08-21** as a dedicated study of the chip *itself* — its place in the ESP32 line-up, where else it is used, what it costs, what the community has learned about it, and what you would design with instead.
>
> They **close three gaps left open by sections 1, 2 and 11**. Those sections have been annotated in place rather than rewritten, so the original reasoning remains auditable:
> - §1.1's `[INF]` suffix decoding is now **superseded by [DOC]** — see **§13.1**.
> - §2's "unresolved" core-count question is now **resolved** — see **§14**.
> - §11's claims that PCN-2021-021 has "no PDF" and that no chip-revision user guide exists are both **wrong**; both documents are now in `artifacts/`. See **§19.3**.
>
> **Section 21 was added 2026-08-21**: the complete silicon-revision matrix (v0.0 → v3.1), what changed at each step, the per-revision errata table, five ways to read the revision off a real board, and what the board's **v3.1** silicon means in practice. **Every loose reference to "ECO V3" elsewhere in this document is superseded by §21.1's naming table** — "ECO3" is v3.0, and "ECO4" is v3.1.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marked part | `ESP32-U4WDH` | **[SCH]** sheet `3_ESP32-CHIP.png`, symbol name on U14 |
| Reference designator on this board | **U14** | **[SCH]** |
| Package | 48-pin QFN, 5 x 5 mm, with a large exposed centre ground pad (pin 49) | **[SCH]** pins 1-48 plus pad 49 tied to GND; **[DOC]** ESP32 series datasheet package drawings |
| Family | Original ESP32 series (Xtensa LX6), **not** ESP32-S3, **not** RISC-V | **[DOC]** |
| Embedded flash | **4 MB in package** | **[DOC]**; **[FW]** the ESP32 factory bootloader header flash-size nibble is `2` (= 4 MB) |
| Flash clock at reset | 40 MHz | **[FW]** bootloader header byte 3 = `0x20` (high nibble `2` = 4 MB, low nibble `0` = 40 MHz) |
| PSRAM | **None**, neither in package nor external | **[SCH]** no PSRAM device and no free SPI bus on U14 |
| SRAM | 520 KB on-chip | **[DOC]** |
| Crystal | Dedicated **40 MHz** crystal `X2`, load caps `C55`/`C56` 10 pF, series `R51` 0 R on XTAL_P | **[SCH]** |
| 32.768 kHz crystal | **Not fitted.** The `32K_XP`/`32K_XN` pins are repurposed as GPIO32/GPIO33 | **[SCH]** — see §5 |
| Antenna | Dedicated ceramic antenna `ANT2`, symbol `CA-C03`, fed by a π network `C46` 2.2 pF / `L5` 2 nH / `C45` 2.2 pF from `LNA_IN` | **[SCH]**; part identity unresolved, see [ceramic antenna record](../../generic/ceramic-antenna/README.md) |
| Supply | 3V3 board rail; `L6` 2 nH in the VDD3P3 feed; local decoupling `C47`-`C52`, `C57` on VDD_SDIO | **[SCH]** |

### 1.1 What the "U4WDH" suffix means

> **⚠ SUPERSEDED 2026-08-21.** The table below was written when the ordering table could not be read out of the PDF. It has since been read — in full, verbatim — out of Espressif's **HTML** build of the same datasheet. **Every row below is now known, and one row is flat wrong: `U` means *dual core*, and `H` does *not* buy you a wider temperature range — it comes with a *narrower* one.** Go to **§13.1**. The text below is retained only to show what the guess was.

**Read this section as [INF] except where marked.** Espressif's ordering-information table in the ESP32 series datasheet is the authority. The copy of that datasheet stored in `artifacts/esp32-datasheet.pdf` is a genuine, validated PDF, but its text layer is glyph-subset encoded and could not be reliably extracted with the tooling available here (verified 2026-08-22), so the ordering table has **not** been transcribed and is not quoted below. The following is the widely-used community decoding, offered only so you know what to go and check:

| Field | Common reading | Confidence |
|---|---|---|
| `U` | Package/variant letter distinguishing this part from `D0WD`, `D0WDQ6`, `D2WD`, `S0WD`, `PICO-D4` | **[INF]** — and note the trap: in `D0WD`/`S0WD` the leading letter encodes **D**ual-core / **S**ingle-core. `U` does **not** follow that pattern, which is precisely why the core count of this part is ambiguous. See §2 |
| `4` | **4 MB embedded flash** | Effectively **[DOC]** — corroborated **[FW]** by the bootloader flash-size nibble |
| `WD` | Same `WD` group letters as `D0WD`/`D2WD`; not decoded here | **[INF]** |
| `H` | Extended/high temperature grade | **[INF]** — do **not** design to a temperature range on the basis of this letter. Get the range from the datasheet's characteristics table |

Practical takeaway: the only suffix field you should rely on without opening the datasheet is the **4 = 4 MB embedded flash**, and that one is independently confirmed by the factory bootloader header.

---

## 2. ⚠ The core-count and clock-speed caveat (unresolved)

> **⚠ RESOLVED 2026-08-21 — see §14.** The part you are almost certainly holding is **dual-core, 240 MHz-capable**. The current ESP32 series datasheet (v5.3) lists ESP32-U4WDH as "Dual core" outright, the PCN's own marking specification gives you a way to **read the answer off the top of the chip**, and a 2022 forum capture shows `esptool` reporting `Dual Core, 240MHz` on a real part. §2 is retained because its *engineering advice* — write code that survives either answer — is still correct and still worth following, and because a single-core part remains physically possible if your board is old enough. Read §2 for the caution, §14 for the answer.

**This is the single most important uncertainty about this chip. Do not paper over it.**

Espressif **PCN-2021-021**, "Upgrade ESP32-U4WDH to a Dual-Core Processor Product" (document version 1.3, issued 2021-09-02, change effective **2021-12-02**), records that ESP32-U4WDH was originally a **single-core** ESP32 **ECO V3** part limited to **160 MHz**, and was subsequently upgraded to a dual-core product. **[DOC]**

Consequences:

- Parts manufactured **before 2021-12-02** are single-core / 160 MHz.
- Parts manufactured **after** that date are dual-core and, per the general ESP32 family specification, capable of 240 MHz.
- **Nothing in Waveshare's schematic, wiki, product page or demo archive states which one is fitted to your board.** The date code is on the chip's top marking, which is not visible in any published photograph at usable resolution.
- The board's own factory firmware does not settle it either: an ESP-IDF application built for `esp32` runs unchanged on both variants, and the ESP32 factory image contains no string that reveals the core count. **[FW]**

This PCN is published by Espressif as HTML only, with no PDF, so no artifact is stored locally; the URL is in the sources table in §11 and in the repository's failures file. — **Correction (2026-08-21): a PDF build of this PCN does exist**, on the legacy `pcn_downloads` path. It has been retrieved, validated and transcribed; see **§19.3** and `artifacts/pcn-2021-021-esp32-u4wdh-dual-core.pdf`.

### 2.1 How to determine it empirically

Do this before you write any code that assumes a second core or a 240 MHz clock. All three methods are non-destructive.

**A. esptool, no firmware needed.** Put the ESP32 into download mode (see §7) and run:

~~~sh
esptool --port PORT chip_id
esptool --port PORT read_mac
esptool --port PORT flash_id
~~~

`chip_id` prints the chip description and revision, e.g. `Chip is ESP32-U4WDH (revision v3.x)`. Recent esptool versions print the single/dual-core distinction as part of the chip description because it is derived from eFuse. If your esptool is old enough that it does not, dump the relevant eFuse block instead:

~~~sh
espefuse --port PORT summary
~~~

and look for the `DIS_APP_CPU` / `CHIP_VER_DIS_APP_CPU` field. **A burned (set) `DIS_APP_CPU` means the second core is disabled — i.e. a single-core part.** **[INF]** on the exact field name for your silicon revision; confirm against the eFuse chapter of `artifacts/esp32-technical-reference-manual.pdf` and the chip-revision identification chapter of `artifacts/esp32-errata.pdf`.

**B. From your own firmware, at runtime.** This is the most direct answer:

~~~c
#include "esp_system.h"
#include "esp_chip_info.h"

esp_chip_info_t info;
esp_chip_info(&info);
ESP_LOGI(TAG, "cores=%d rev=%d features: WiFi=%d BT=%d BLE=%d",
         info.cores, info.revision,
         !!(info.features & CHIP_FEATURE_WIFI_BGN),
         !!(info.features & CHIP_FEATURE_BT),
         !!(info.features & CHIP_FEATURE_BLE));
ESP_LOGI(TAG, "cpu freq = %d MHz", esp_clk_cpu_freq() / 1000000);
~~~

`info.cores` returns 1 or 2. Print it on every boot of anything you build for this chip.

**C. Let the build fail loudly.** In `idf.py menuconfig`, if you set `CONFIG_ESP32_DEFAULT_CPU_FREQ_240` and the fitted part is the 160 MHz single-core variant, the clock will not come up as requested. Do not rely on this as a *test*, but do use `esp_clk_cpu_freq()` from method B to verify that the frequency you configured is the frequency you got.

### 2.2 How to write code that survives either answer

- Do **not** pin tasks to `APP_CPU_NUM` (core 1) unconditionally. Use `tskNO_AFFINITY`, or branch on `esp_chip_info()`.
- Do **not** budget CPU time on the assumption of 240 MHz. The Bluetooth Classic A2DP + SBC decode workload on this chip is not trivial; if you are on a 160 MHz single-core part, the radio stack and your application share one core.
- Set `CONFIG_FREERTOS_UNICORE` deliberately if you want identical behaviour on both variants at the cost of throughput on dual-core parts.

---

## 3. Capabilities

**[DOC]** unless marked. Full detail in `artifacts/esp32-datasheet.pdf` and `artifacts/esp32-technical-reference-manual.pdf`.

| Area | Capability | Note for this board |
|---|---|---|
| Wi-Fi | 802.11 b/g/n, 2.4 GHz, station/AP/AP+STA | Available but **unused by the factory firmware** **[FW]** — no Wi-Fi provisioning strings, no HTTP server, in the ESP32 image. The S3 image is the one with the Wi-Fi config web page **[FW]** |
| **Bluetooth Classic (BR/EDR)** | Full BR/EDR controller and host | **The reason this chip is on the board.** See §4 |
| Bluetooth Low Energy | BLE **4.2** | Note: 4.2, not the BLE 5 of the ESP32-S3 |
| Coexistence | Wi-Fi / BT software coexistence | **[FW]** coexistence adapter strings present in the ESP32 image |
| CPU | Xtensa LX6, 1 or 2 cores — **see §2** | |
| Memory | 520 KB SRAM, 4 MB embedded flash, no PSRAM | ~1 MB of the flash is the factory app; see §8 |
| RTC / ULP | RTC domain with 8 KB RTC SRAM and a ULP coprocessor | RTC GPIOs on this board are consumed as normal GPIO — see §5 |
| Deep sleep | Full deep-sleep support with RTC GPIO and ULP wake sources | The board's second knob (GPIO19/22) is on RTC-capable pins, so knob-wake is physically possible **[INF]** |
| Peripherals | 2x I2C, 3x SPI, **2x I2S**, 3x UART, SDMMC host, 8x 16-bit + 8x 8-bit LEDC, PWM, pulse counter, RMT, TWAI/CAN, 12-bit SAR ADC x2, 2x 8-bit DAC, 10x touch sensor, temperature sensor, hall sensor | Only I2S0, UART0 and UART1 are actually wired on this board — §5 |
| Crypto | AES, SHA, RSA, RNG, flash encryption, Secure Boot | Not enabled in the factory image **[FW]** — `secure_version` = 0 in the app descriptor |
| Native USB | **None.** The original ESP32 has no USB OTG/serial-JTAG peripheral | This is why U14 needs the external bridge U10 — §7 |

### 3.1 Limits worth stating explicitly

- **No native USB device controller.** Unlike the ESP32-S3 there is no CDC-ACM, no USB-serial-JTAG, no HID-over-USB from this chip. Everything USB-facing goes through the external UART bridge.
- **No Bluetooth 5 LE features** — no coded PHY, no 2 M PHY, no extended advertising. BLE 4.2 only.
- **GPIO6-GPIO11 are gone.** They are bonded to the in-package flash die. On this board they appear on the schematic as `SD_DATA_0..3`, `SD_CMD`, `SD_CLK` with **no net attached at all** **[SCH]** — the schematic itself confirms they are unavailable. Never attempt to use them.
- **GPIO34-39 are input-only** on the ESP32 family. None are used on this board **[SCH]**.
- **Bluetooth Classic and BLE together consume a large fraction of the 4 MB flash and the 520 KB SRAM.** The factory app is already ~1 MB with A2DP + AVRCP + SPP + HID enabled **[FW]**. Budget accordingly; there is no PSRAM to fall back on.

---

## 4. Why this chip exists on this board: the Classic Bluetooth gap

The ESP32-S3 supports **Bluetooth LE 5 only**. It has **no Bluetooth Classic (BR/EDR) radio at all** — this is a silicon-level omission, not a software limitation, and no ESP-IDF version, Arduino core version or library can add it.

Bluetooth **audio** in the mainstream sense — A2DP music streaming, AVRCP transport control and metadata, HFP hands-free, SPP serial, Classic HID keyboards/media keys — is a **BR/EDR** profile stack. So a board that wants to be a Bluetooth media-control knob and a Bluetooth speaker/receiver *cannot* do it from an ESP32-S3.

Waveshare's answer was to solder an original ESP32 next to the S3 and give the two chips a private UART. The S3 keeps the graphics, touch, storage and microphone; the ESP32 owns the Bluetooth Classic radio and the audio path. **[SCH]** **[FW]**

The factory ESP32 firmware confirms which profiles are actually built in **[FW]** (strings extracted from `ESP32-KNOB_ESP32_0.bin`):

| Profile / role | Evidence strings |
|---|---|
| **A2DP sink** (board acts as a Bluetooth speaker) | `btc_a2dp_sink_thread_init`, `Advanced Audio Sink`, `bt_av_hdl_a2d_evt` |
| **A2DP source** (board streams audio out) | `btc_a2dp_source_aa_start_tx`, `btc_a2dp_source_encoder_update`, `btc_media_aa_prep_sbc_2_send` |
| **AVRCP controller (CT)** | `btc_avrc_ct_init`, `btc_avrc_ct_send_passthrough_cmd`, `btc_avrc_ct_send_metadata_cmd`, `btc_avrc_ct_send_set_absolute_volume_cmd` |
| **AVRCP target (TG)** | `btc_avrc_tg_init`, `btc_avrc_tg_send_rn_rsp` |
| **AVRCP Cover Art (BIP / OBEX)** | `btc_avrc_ct_cover_art_connect`, `btc_avrc_ct_cover_art_get_image`, `obex_main.c` |
| **SPP** (Serial Port Profile) | `SPP` |
| **Bluetooth Classic HID device** | `BT_HIDD`, `bt_hid_device_init`, `hidd_l2cif_connect_ind` |
| **BLE HID device** | `BLE_HIDD`, `ble_hid_task`, `esp_ble_hidd_dev_feature_set` |
| Bluetooth host | Bluedroid (`BT_BTC`, `BT_BTIF`, `BT_BTM`, `bta_sys_main.c`) |

The AVRCP **Cover Art** support is notable: it means the ESP32 fetches album artwork over Bluetooth (OBEX/BIP) and, per §6, ships it to the S3 over the internal UART to be drawn as a JPEG on the round LCD.

**[FW]** The string `BTAUDIOMATE` appears in the ESP32 image and is very likely the advertised Bluetooth device name — but it is a bare string with no surrounding format specifier, so this is **[INF]**; confirm by scanning for the device from a phone.

---

## 5. Complete pin table for this board

**[SCH]** from `3_ESP32-CHIP.png` unless noted. All 48 signal pins plus the ground pad are listed, including the ones that go nowhere, because "this pin is unconnected" is a load-bearing fact when you are looking for a spare GPIO.

### 5.1 By package pin

| Pin | Chip function | Net on this board | Role |
|---:|---|---|---|
| 1 | VDDA | 3V3 (RF analog) | Supply, decoupled by `C47`/`C48`/`C49`/`C50` |
| 2 | LNA_IN | to `C46`/`L5`/`C45` π network → `ANT2` | RF in/out to the dedicated ceramic antenna |
| 3 | VDD3P3 | 3V3 via `L6` 2 nH | RF supply |
| 4 | VDD3P3 | 3V3 via `L6` 2 nH | RF supply |
| 5 | SENSOR_VP (GPIO36) | *no net* | **Unused, unavailable at any connector** |
| 6 | SENSOR_CAPP | *no net* | Unused |
| 7 | SENSOR_CAPN | *no net* | Unused |
| 8 | SENSOR_VN (GPIO39) | *no net* | **Unused** |
| 9 | CHIP_PU (EN) | `ESP32_EN` | Reset. `R54` 10 k pull-up to 3V3, `C22` 1 µF to GND. Driven by bridge `U10` RTS# — §7 |
| 10 | VDET_1 (GPIO34) | *no net* | **Unused** |
| 11 | VDET_2 (GPIO35) | *no net* | **Unused** |
| 12 | 32K_XP (**GPIO32**) | `ESP32_IO32` → **`XSMT`** | **PCM5100A soft-mute control.** See §9 — this is the arbitration chokepoint |
| 13 | 32K_XN (**GPIO33**) | `ESP32_IO33` | Net labelled but **terminates nowhere else in the 5-sheet set**. Effectively a free pin, physically unreachable |
| 14 | GPIO25 | `ESP32_IO25` → `ESP32_I2S_DAC_BCK` | I2S bit clock → CH445P `S1A` |
| 15 | GPIO26 | `ESP32_IO26` → `ESP32_I2S_DAC_DIN` | I2S serial data → CH445P `S1B` |
| 16 | GPIO27 | `ESP32_IO27` → `ESP32_I2S_DAC_LRCK/WS` | I2S word select → CH445P `S1C` |
| 17 | MTMS (GPIO14) | *no net* | **Unused.** JTAG TMS |
| 18 | MTDI (GPIO12) | *no net* | **Unused.** JTAG TDI — also the flash-voltage strapping pin |
| 19 | VDD3P3_RTC | 3V3, `C51` 100 nF | RTC domain supply |
| 20 | MTCK (GPIO13) | *no net* | **Unused.** JTAG TCK |
| 21 | MTDO (GPIO15) | *no net* | **Unused.** JTAG TDO — also a boot-log strapping pin |
| 22 | GPIO2 | `ESP32_IO2` | Net labelled, **no other endpoint in the 5-sheet set**. Also a boot strapping pin |
| 23 | GPIO0 | `ESP32_IO0` | **Boot mode strap.** `R50` 10 k pull-up to 3V3, `C24` 100 nF. Driven by bridge `U10` TNOW/DTR# through `R14` 5.1 k — §7 |
| 24 | GPIO4 | `ESP32_IO4` | Net labelled, **no other endpoint in the 5-sheet set** |
| 25 | GPIO16 | *no net* | **Unused** |
| 26 | VDD_SDIO | `C57` 1 µF to GND | Internal flash-die supply rail. **Do not load** |
| 27 | GPIO17 | *no net* | **Unused** |
| 28 | SD_DATA_2 (GPIO9) | *no net* | **Bonded to embedded flash — unusable** |
| 29 | SD_DATA_3 (GPIO10) | *no net* | **Bonded to embedded flash — unusable** |
| 30 | SD_CMD (GPIO11) | *no net* | **Bonded to embedded flash — unusable** |
| 31 | SD_CLK (GPIO6) | *no net* | **Bonded to embedded flash — unusable** |
| 32 | SD_DATA_0 (GPIO7) | *no net* | **Bonded to embedded flash — unusable** |
| 33 | SD_DATA_1 (GPIO8) | *no net* | **Bonded to embedded flash — unusable** |
| 34 | GPIO5 | *no net* | **Unused.** Also a boot strapping pin |
| 35 | GPIO18 | `ESP32_IO18` → net `ESP32S3_TX` | **Inter-MCU UART receive.** S3 GPIO38 drives this line — §6 |
| 36 | GPIO23 | `ESP32_IO23` → net `ESP32S3_RX` | **Inter-MCU UART transmit.** Drives S3 GPIO48 — §6 |
| 37 | VDD3P3_CPU | 3V3, `C52` 100 nF | Digital supply |
| 38 | GPIO19 | `ESP32_IO19` → `EC2_A` | **Second knob, channel A.** `R55` 10 k pull-up **[SCH sheet 1]** |
| 39 | GPIO22 | `ESP32_IO22` → `EC2_B` | **Second knob, channel B.** `R56` 10 k pull-up **[SCH sheet 1]** |
| 40 | U0RXD (GPIO3) | `ESP32_UART0_RX` via `R65` 470 R | Console/download receive from bridge `U10` TXD |
| 41 | U0TXD (GPIO1) | `ESP32_UART0_TX` | Console/download transmit to bridge `U10` RXD |
| 42 | GPIO21 | `ESP32_IO21` | Net labelled, **no other endpoint in the 5-sheet set** |
| 43 | VDDA | 3V3 | Analog supply |
| 44 | XTAL_N | `ESP32_XTAL_N` → `X2` pin 3, `C56` 10 pF | 40 MHz crystal |
| 45 | XTAL_P | `ESP32_XTAL_P` via `R51` 0 R → `X2` pin 1, `C55` 10 pF | 40 MHz crystal |
| 46 | VDDA | 3V3 | Analog supply |
| 47 | CAP2 | `R52` 20 k + `C58` 3.3 nF | Internal-regulator RC network per the Espressif reference design |
| 48 | CAP1 | `C59` 10 nF to GND | Internal-regulator RC network per the Espressif reference design |
| 49 | GND pad | GND | Exposed thermal/ground pad |

### 5.2 By GPIO number — the eight pins that actually do something

This is the table to copy into your firmware's `pin_config.h`.

| GPIO | Net | Function | Direction | Notes |
|---:|---|---|---|---|
| 0 | `ESP32_IO0` | Boot strap / auto-download | in (strap) | 10 k pull-up; also brought out to connector `CN1` **[SCH sheet 1]** |
| 1 | `ESP32_UART0_TX` | UART0 console TX | out | to bridge `U10` RXD |
| 3 | `ESP32_UART0_RX` | UART0 console RX | in | from bridge `U10` TXD via 470 R |
| 18 | `ESP32S3_TX` | **UART1 RX** from ESP32-S3 | in | S3 GPIO38 → here **[FW]** UART1 |
| 19 | `EC2_A` | Second knob channel A | in | 10 k pull-up, active low |
| 22 | `EC2_B` | Second knob channel B | in | 10 k pull-up, active low |
| 23 | `ESP32S3_RX` | **UART1 TX** to ESP32-S3 | out | here → S3 GPIO48 **[FW]** UART1 |
| 25 | `ESP32_I2S_DAC_BCK` | I2S0 BCLK | out | via CH445P `S1A`→`DA` |
| 26 | `ESP32_I2S_DAC_DIN` | I2S0 SDOUT | out | via CH445P `S1B`→`DB` |
| 27 | `ESP32_I2S_DAC_LRCK/WS` | I2S0 WS/LRCK | out | via CH445P `S1C`→`DC` |
| 32 | `XSMT` | PCM5100A soft mute | out | **direct, not muxed** — §9 |

Everything not in this table is either bonded to internal flash, unconnected, or a supply pin. **There are no spare, board-accessible GPIOs on this chip.** `ESP32_IO2`, `ESP32_IO4`, `ESP32_IO21` and `ESP32_IO33` have net labels but no second endpoint anywhere in the five published schematic sheets, so they are probably test points or unrouted stubs **[INF]** — they are not usable without a board teardown to find where (if anywhere) they land.

### 5.3 What is *not* connected, and why that matters

The second knob is a **[SSCM110100 directional switch](../../alps-alpine/sscm110100/README.md)** (`SW1`), not a conventional quadrature encoder. It presents two active-low contacts, `EC2_A` and `EC2_B`, each with a 10 k pull-up **[SCH sheet 1]**. The factory ESP32 firmware decodes it with Espressif's `iot_knob` component (`../main/iot_knob.c`, `iot_knob_create`, `iot_knob_register_cb`, error string `encoder A can't be the same as encoder B`) **[FW]**, i.e. it is treated in software as an A/B encoder. There is **no switch/push contact on `SW1` wired to the ESP32** in the schematic **[SCH]** — if you need a "press" gesture on the second knob, it is not there.

The MSM261 microphone, the CST816 touch controller, the DRV2605L haptic driver, the microSD socket, the LCD and the W25Q128 flash are **all on the S3** **[SCH]**. The ESP32 cannot see any of them, at all, ever, except by asking the S3 over the UART.

---

## 6. The inter-MCU UART link

> **Device-level treatment:** [Dual-MCU architecture §2](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md#2-the-inter-mcu-link-a-two-wire-uart) builds on this section with the full-duplex/no-flow-control analysis, a baud-vs-throughput table, worked album-art transfer times, and an explicit register of what about the protocol is *not* known. **Re-verified 2026-08-22: the configured baud rate is not recoverable from either binary or from the demo tree** — every baud literal in the demo archive is a console baud in an `sdkconfig`.

### 6.1 Physical layer — fully established **[SCH]**

| | ESP32-U4WDH (U14) | ESP32-S3R8 (U2) |
|---|---|---|
| U4WDH transmits | GPIO23 (pin 36) | → GPIO48 (`ESP32S3_RX`) |
| U4WDH receives | GPIO18 (pin 35) | ← GPIO38 (`ESP32S3_TX`) |

Two wires, cross-connected, 3.3 V CMOS levels, no flow control, no reset line, no interrupt line, no shared clock. There is **no** other communication channel between the two MCUs.

### 6.2 Peripheral assignment — established **[FW]**

Both sides use **UART1** (not UART0, which is each chip's console):

- ESP32 side: `uart_get_buffered_data_len(UART_NUM_1, (size_t *)&rxBytes)` in `../main/uart1.c`, FreeRTOS task `task_uart1`, log tag `uart1`.
- S3 side: `src/driver/uart1.cpp`, log line `[I] UART1 task started.`, log tag `[UART]`.

### 6.3 Framing — partially established, byte format **UNKNOWN**

The wire format is **not documented by Waveshare anywhere**, and **no example in the official Arduino or ESP-IDF demo archive uses this link** (verified 2026-08-22 by searching the entire demo tree for `Serial1`/`Serial2`/`UART_NUM_1`/GPIO 38/48 references — zero hits). The only evidence is the log/assert strings compiled into both factory images.

What those strings **do** establish **[FW]**:

| Fact | Evidence string | Side |
|---|---|---|
| Frames carry a **command/opcode** field, and unknown values are rejected | `[E] [UART] Wrong cmd:%d` | S3 |
| Frames carry a **transfer id**, validated against expected | `[E] [UART] Wrong transfer id:%d` | S3 |
| Frames carry an explicit **length**, validated | `[E] [UART] Data len wrong:%d` | S3 |
| Cover-art transfers are **multi-packet with a known total** | `[I] [UART] Recv cover art begin , total packet:%d` | S3 |
| The receiver can **request a specific packet** (retransmission / pull-style flow) | `[I] [UART] Need packet:%d` | S3 |
| Transfers complete with a byte count | `[I] [UART] Recv cover art ok, size:%u` | S3 |
| Transfers can be **aborted with a reason code** | `[I] [UART] Recv cover stoped,reason:%u` | S3 |
| The S3 **pushes status** back to the ESP32 | `[I] [UART] Report status` | S3 |
| The ESP32 sends **AVRCP metadata** | `W (%lu) %s: Uart send meta data error` | ESP32 |
| The ESP32 sends **cover art**, with a minimum frame length of **7 bytes** | `Uart send cover art error, rcv data length < 7` | ESP32 |
| The ESP32 tracks a **send id** and a **packet id** separately | `Uart send cover art error, bad send id:%u,%u`, `... bad packet id` | ESP32 |
| Transfers are **stateful** — the ESP32 rejects packets outside an active transfer | `Uart send cover art error, not in sending` | ESP32 |
| Cover art is **JPEG** and is decoded on the S3 | `[I] [IO] Skip decode cover jpeg`, `[I] [IO] Decode jpeg from ram,size :%u` | S3 |
| The S3 can command the ESP32 to **forget the A2DP pairing** | `Clear BT A2DP pair` (S3 UI string); `PEERADDR` NVS key + `Clear peer addr err,code: %d` on the ESP32 | both |

So the shape of the protocol is: **a length-prefixed, command-coded frame with a transfer id, used bidirectionally, with a pull-based multi-packet bulk mode for JPEG album art flowing ESP32 → S3, and status/control frames flowing S3 → ESP32.** The minimum cover-art frame is 7 bytes, which is consistent with a header of roughly `{cmd, transfer id, packet id, length…}` — but **the byte order, the field widths, the framing delimiters or sync bytes, the checksum (if any) and the baud rate are all unknown and are deliberately not guessed here.**

### 6.4 If you need the protocol

Options, in increasing order of effort:

1. **Don't.** Reflash *both* MCUs with your own firmware and define your own protocol. This is by far the sanest path for a custom project, and it is what most community projects do. You control both ends; the link is just two GPIOs.
2. **Sniff it.** Tap ESP32 GPIO23 and GPIO18 (or the corresponding S3 pins 48/38) with a logic analyser while running the stock firmware, and auto-baud. This will give you the real baud rate and real frames within minutes.
3. **Disassemble.** Both factory images are present locally with known hashes; `uart1.c` / `uart1.cpp` are small, identifiable translation units.

Until one of those is done, **treat the protocol as undocumented.** Do not build against a guessed frame layout.

---

## 7. Programming and flashing this chip

### 7.1 The USB-C orientation quirk

This board has **one** USB-C receptacle but **two** independent USB endpoints:

- the **ESP32-S3's native USB peripheral** (`USB_DP`/`USB_DN`, S3 GPIO20/GPIO19), and
- the **USB-UART bridge `U10`** which serves the ESP32-U4WDH (`USB_ESP32_DP`/`USB_ESP32_DN`).

Per Waveshare's FAQ, **which of the two you get depends on which way round the Type-C plug is inserted.** Rotating the plug 180° switches you to the other MCU. This is genuinely how the product behaves and it is the single most common source of "my board doesn't show up" confusion.

**Evidence boundary:** the five published schematic sheets **do not contain a USB Type-C receptacle symbol at all** (verified 2026-08-22 across all five PNGs). Both differential pairs appear only on the 10-pin connector `CN1` (`PM127-2-05-S-4.3`) on sheet `1_LCD&POWER.png` **[SCH]**. The actual orientation-selection topology — whether it is a passive CC-based arrangement, a mux IC, or simply the two pairs wired to the A-side and B-side pins of the receptacle — is **not shown and is not inferred here**. See the [USB-C target-selection interface record](../../generic/usb-c-interface/README.md).

The practical rule is simply: **if `esptool ... chip_id` reports the wrong chip, or no port appears, unplug, flip the cable, plug back in.**

### 7.2 The USB-UART bridge U10

**[SCH]** sheet `3_ESP32-CHIP.png`. The bridge is drawn as a 10-pin functional symbol with **no part number**:

| U10 pin | Signal | Connects to |
|---:|---|---|
| 1 | UD+ | `USB_ESP32_DP` |
| 2 | UD- | `USB_ESP32_DN` |
| 3 | GND | GND |
| 4 | RTS# | **`ESP32_EN`** (U14 pin 9, CHIP_PU) |
| 5 | CTS# | — |
| 6 | TNOW/DTR# | **`ESP32_IO0`** (U14 pin 23) via `R14` 5.1 k, `C24` 100 nF |
| 7 | VCC | 3V3 |
| 8 | TXD | `ESP32_UART0_RX` → U14 pin 40 via `R65` 470 R |
| 9 | RXD | `ESP32_UART0_TX` ← U14 pin 41 |
| 10 | V3 | 3V3 |

Note that `RTS#` drives `EN` and `DTR#` drives `IO0` **directly**, rather than through the two-transistor cross-coupled network used on most ESP32 dev boards. This is a simpler auto-reset arrangement; the practical consequence is that **any serial terminal that asserts DTR or RTS on open can accidentally reset the ESP32 or drop it into the bootloader.** If your monitor session dies the instant you connect, disable DTR/RTS assertion in your terminal program. **[INF]** on the failure mode; **[SCH]** on the wiring.

**Part identity is unresolved.** The symbol's pin naming (`UD+`/`UD-`, and especially `TNOW/DTR#`) matches WCH's CH340-family symbol conventions, and Waveshare ships a CH34x macOS driver in the board's tools archive — but the schematic gives no part number and the silkscreen is not legible in any published photo, so this remains **[INF]** and is recorded as unresolved in the [USB-UART bridge record](../../wch/ch340x/README.md). **Do not tell users to install a CP210x driver, or a CH34x driver, as though it were established.**

### 7.3 esptool

Manual bootloader entry is not normally needed — the bridge's RTS#/DTR# lines give automatic download mode. If it fails, the ESP32 enters download mode when `GPIO0` is low at the rising edge of `EN`.

~~~sh
# 1. Confirm you are talking to the ESP32 and not the S3.
esptool --port PORT chip_id
#    Expect: "Chip is ESP32-U4WDH (revision ...)". If it says ESP32-S3, flip the USB-C plug.

# 2. Note the core count / revision it reports — see §2 for cores, §21.6 for revision.
#    On current silicon expect: "Chip is ESP32-U4WDH (revision v3.1)".

# 3. Read the whole 4 MB out before you overwrite anything.
esptool --chip esp32 --port PORT --baud 921600 read_flash 0x0 0x400000 esp32-u4wdh-backup.bin

# 4. Flash.
esptool --chip esp32 --port PORT --baud 921600 write_flash -z 0x0 ESP32-KNOB_ESP32_0.bin
~~~

Drop to `--baud 115200` if the link is unreliable. **Never** flash an `esp32s3` image to this chip or vice versa; `esptool` will normally refuse on the chip-id check, but only if you let it detect rather than forcing `--chip`.

### 7.4 ESP-IDF

Target is **`esp32`** (not `esp32s3`):

~~~sh
idf.py set-target esp32
idf.py menuconfig      # enable Bluedroid + Classic BT; see §10
idf.py build
idf.py -p PORT flash monitor
~~~

`idf.py` also prints the detected chip and revision on connect, which is another place to read the answer to §2.

Framework versions relevant to this board:

| Framework | Version | Where it comes from |
|---|---|---|
| ESP-IDF (factory ESP32 image) | **v5.4-727-g5cbd2a3877** | **[FW]** app descriptor in `ESP32-KNOB_ESP32_0.bin` |
| ESP-IDF (Waveshare's documented setup) | 5.1.4 | Waveshare wiki; matches the S3 examples |
| ESP-IDF (offline PDF manuals stored here) | 5.1.4 and 5.2.5 | `artifacts/` — see §11.1 for why not 5.4 |
| Arduino-ESP32 | 3.2.0+ recommended for the board generally | Waveshare wiki |

### 7.5 Arduino

Select **"ESP32 Dev Module"** — *not* "ESP32S3 Dev Module" — when targeting this chip. USB CDC settings are irrelevant here because there is no native USB; you are always going through the external bridge at whatever baud you set.

---

## 8. Factory firmware image for this chip

**[FW]** — parsed directly from `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/ESP32-KNOB_ESP32_0.bin`.

| Property | Value |
|---|---|
| File | `ESP32-KNOB_ESP32_0.bin` |
| Size | 1,130,672 bytes |
| SHA-256 | `0c1c21b9822d4c2d80d58534b33eb0083880de4ed7354a38b4c78ba51757349d` |
| Image type | **Merged** image, written at offset `0x0`. Bytes `0x0`–`0xFFF` are `0xFF` padding (the ESP32 bootloader lives at `0x1000`) |
| Bootloader | at `0x1000`, magic `0xE9`, chip id `0` (= ESP32) |
| Flash config byte | `0x20` → 4 MB @ 40 MHz |
| App | at `0x10000`, app descriptor magic `0xABCD5432` |
| **Project name** | **`TAIJI_KNOB_32`** |
| App version | `1` |
| Build timestamp | **09:24:52 Apr 18 2025** |
| ESP-IDF version | **v5.4-727-g5cbd2a3877** |
| Secure version | 0 (Secure Boot / anti-rollback not in use) |

Partition table at `0x8000`:

| Label | Type | Subtype | Offset | Size |
|---|---|---|---:|---:|
| `nvs` | data | `0x02` (nvs) | `0x9000` | `0x6000` (24 KB) |
| `phy_init` | data | `0x01` | `0xF000` | `0x1000` (4 KB) |
| `factory` | app | `0x00` | `0x10000` | `0x190000` (1.5625 MB) |
| `storage` | data | `0x82` (FAT) | `0x1A0000` | `0x160000` (1.375 MB) |

Notes:

- Single `factory` app slot, **no OTA partitions** — this firmware cannot self-update over the air, and there is no rollback slot.
- The `storage` FAT partition is **not present in the shipped image** (the file ends at `0x1101B0`), so it is formatted on first boot. Any content Waveshare intended to live there is not recoverable from this file.
- Total partitioned space is `0x300000` = 3 MB of the 4 MB; the top 1 MB is unallocated.
- The `nvs` partition holds the Bluetooth pairing state: namespace/key `PEERADDR` **[FW]**, with the ESP32 logging `Get saved bt addr:%02x:...`. Erasing NVS (`esptool erase_region 0x9000 0x6000`) is the clean way to force re-pairing without a full reflash.

---

## 9. Shared-resource arbitration: the PCM5100A DAC

Both MCUs want to drive one [PCM5100A stereo DAC](../../texas-instruments/pcm5100a/README.md). The board resolves this with a [CH445P](../../wch/ch445p/README.md) four-channel 2:1 analog switch (`U18`) — but the arrangement has a subtlety that is easy to miss and important to get right.

### 9.1 The I2S mux — S3-controlled **[SCH sheet 5]**

| CH445P channel | `S1` input (ESP32-U4WDH side) | `S2` input (ESP32-S3 side) | `D` common → PCM5100A |
|---|---|---|---|
| A | `ESP32_I2S_DAC_BCK` (GPIO25) | `S3_I2S_DAC_BCK` (S3 GPIO39) | `I2S_DAC_BCK` → PCM5100A pin 13 BCK |
| B | `ESP32_I2S_DAC_DIN` (GPIO26) | `S3_I2S_DAC_DIN` (S3 GPIO41) | `I2S_DAC_DIN` → PCM5100A pin 14 DIN |
| C | `ESP32_I2S_DAC_LRCK/WS` (GPIO27) | `S3_I2S_DAC_LRCK/WS` (S3 GPIO40) | `I2S_DAC_LRCK/WS` → PCM5100A pin 15 LRCK |
| D | *unconnected* | *unconnected* | *unconnected* (would have been MCK) |

- Select input: `IN` (pin 15) = net **`I2S_SWITCH_IN`**, which is **ESP32-S3 GPIO0** **[SCH sheet 2]**.
- `EN#` (pin 13) is tied to ground → the switch is permanently enabled **[SCH sheet 5]**.
- `VCC` (pin 14) is `3V3_DAC`, the clean rail from the [SGM2036-3.3 LDO](../../sgmicro/sgm2036-3.3/README.md) **[SCH sheet 5]**.
- Channel D is unused, so **no MCLK reaches the DAC from either MCU** — the PCM5100A must be run in its clock-recovery / MCLK-less mode.

**The critical consequence: the U4WDH cannot select itself onto the DAC.** The mux select line belongs to the S3. If the S3 is held in reset, unprogrammed, or its firmware never configures GPIO0, the ESP32's audio may never reach the DAC no matter what the ESP32 does.

Two further traps:

- **S3 GPIO0 is also the S3's BOOT strapping pin**, with an external 10 k pull-up (`R58`) **[SCH sheet 1]**. So the mux sits in whichever state a logic-high select produces from reset until S3 firmware drives it otherwise. **Which bank (`S1` = ESP32, or `S2` = S3) a logic high selects is [INF] and unverified** — no CH445P datasheet has been obtained (see the [CH445P record](../../wch/ch445p/README.md)), so the truth table is not established. Verify on hardware before relying on the power-on default.
- **S3 GPIO0 is also routed to connector `CN1`** **[SCH sheet 1]**, so anything attached to that header can fight the mux select.

### 9.2 The mute line — U4WDH-controlled **[SCH]**

The PCM5100A's `XSMT` soft-mute input (`U12` pin 17) is driven by net `XSMT`, which comes from **ESP32-U4WDH GPIO32 and nothing else** — it is *not* routed through the CH445P and no S3 pin touches it. It is checked on both sheet `3_ESP32-CHIP.png` (`ESP32_IO32 → XSMT`) and sheet `5_DAC.png` (`XSMT → U12 pin 17`), and no pull-up or pull-down resistor is fitted on the net.

**So the two MCUs each hold one half of the audio path:**

| Resource | Owner |
|---|---|
| I2S source selection (CH445P `IN`) | **ESP32-S3** (GPIO0) |
| DAC mute / un-mute (`XSMT`) | **ESP32-U4WDH** (GPIO32) |

Neither chip can produce sound on its own without the other's cooperation. That is a deliberate-looking but awkward split, and it has a concrete implication that is **currently unresolved**:

> **Open question:** Waveshare's official `07_Audio_Test` example runs on the ESP32-S3 alone and is documented as producing audio out of the 3.5 mm jack. But un-muting the DAC requires the U4WDH to drive `XSMT` high. Either (a) the PCM5100A's `XSMT` input has an internal pull-up that un-mutes when the pin floats, (b) the factory ESP32 firmware un-mutes at boot and stays that way, or (c) the example only works with the factory ESP32 firmware still resident. **This has not been verified.** If you reflash the U4WDH with your own firmware and then lose all audio from the S3, this is why: drive GPIO32 high on the ESP32 side. Recorded in the device's [gaps and conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md).

### 9.3 Practical arbitration recipe

If you are writing both firmwares:

1. On the S3, drive `GPIO0` to the level that selects the bank you want — **and measure which level that is**, once, on your board.
2. On the ESP32, drive `GPIO32` **high** to un-mute whenever *either* MCU intends to play, and low to mute during source switches (switching the I2S clocks under a live DAC will produce a click or a burst of noise).
3. Sequence a handover as: ESP32 mutes (`GPIO32` low) → S3 flips `GPIO0` → new source starts its I2S clocks → ESP32 un-mutes. Since `GPIO32` is on the ESP32 and `GPIO0` is on the S3, **this handshake has to travel over the inter-MCU UART** (§6), which is presumably part of what the undocumented protocol carries.
4. Remember there is no MCLK. Configure the PCM5100A for BCK-derived clocking, and keep BCK/LRCK ratios within what the DAC's PLL will lock to.

---

## 10. Software: libraries, APIs and frameworks

### 10.1 ESP-IDF — Bluetooth Classic (Bluedroid)

The factory firmware uses the **Bluedroid** host **[FW]**. NimBLE is *not* an option here for anything Classic — NimBLE is BLE-only. In `menuconfig`:

```
Component config → Bluetooth → [*] Bluetooth
  → Bluetooth controller → Bluetooth controller mode → BR/EDR Only  (or Bluetooth Dual Mode)
  → Bluetooth Host → Bluedroid - Dual-mode
  → Bluedroid Options → [*] Classic Bluetooth
      → [*] A2DP    → sink and/or source
      → [*] AVRCP
      → [*] SPP
      → [*] Classic BT HID Device      (if you want media keys / HID)
```

Relevant API surfaces, all documented in the ESP-IDF v5.2.5 (`esp32`) Programming Guide — **archived 2026-08-24**, see [ARCHIVED-FRAMEWORK-GUIDES.md](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md); peripheral-level extracts in [ESP-IDF peripheral capabilities](../../../guides/espressif/esp-idf-peripheral-capabilities.md):

| Header / API | Purpose |
|---|---|
| `esp_bt_main.h`, `esp_bt_device.h` | Bluedroid init/enable, device name and address |
| `esp_gap_bt_api.h` | Classic GAP: discovery, pairing, IO capability, class of device |
| `esp_a2dp_api.h` | **A2DP sink and source** — the music stream |
| `esp_avrc_api.h` | **AVRCP CT and TG** — play/pause/next, absolute volume, track metadata, and Cover Art |
| `esp_spp_api.h` | **SPP** — Bluetooth serial |
| `esp_hidd_api.h` / `esp_hid_common.h` | Classic **and** BLE HID device roles |
| `esp_hf_client_api.h` / `esp_hf_ag_api.h` | **HFP** hands-free (client and audio-gateway). *Not* present in the factory image **[FW]**, but supported by the chip and IDF |
| `driver/i2s_std.h` | I2S standard mode TX to the DAC — the factory firmware uses the new `i2s_new_channel` / `i2s_channel_init_std_mode` API **[FW]**, i.e. IDF ≥ 5.0 style, not the legacy `i2s_driver_install` |
| `esp_chip_info.h`, `esp_clk.h` | Core count and clock — see §2 |

Espressif's own reference examples that map almost one-to-one onto this hardware live in `esp-idf/examples/bluetooth/bluedroid/classic_bt/`: `a2dp_sink`, `a2dp_source`, `bt_spp_acceptor`, `bt_discovery`, and `esp-idf/examples/bluetooth/esp_hid_device`.

### 10.2 ESP-ADF

The ESP-ADF Programming Guide was stored under **this** component rather than under the ESP32-S3 deliberately: ADF's Bluetooth A2DP audio-pipeline elements target the original ESP32, because that is the chip with BR/EDR. If you want a proper element-graph audio pipeline (`bluetooth_service` → `a2dp_stream` → decoder → `i2s_stream_writer`) rather than hand-rolled ring buffers, ADF is the framework and this is the chip it runs on.

> **The PDF was archived 2026-08-24** ([record](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md)) after its content was distilled into **[ESP-ADF audio pipelines](../../../guides/espressif/esp-adf-audio-pipelines.md)** — which includes the Element/Pipeline architecture, the full `bluetooth_service` + AVRCP API surface, and the [audio memory budget](../../../guides/espressif/esp-adf-audio-pipelines.md#5-the-audio-memory-budget--the-most-useful-table-in-the-document) showing Classic Bluetooth costs **140 kB of the ~290 kB internal-RAM baseline when no PSRAM is fitted** — which is this chip's situation.

The factory firmware does **not** appear to use ADF **[FW]** — it drives I2S directly from the A2DP callback through its own ring buffer (`BtI2STask`, `ringbuffer is full, drop this packet!`, `../main/bt_app_av.c`), which is the plain ESP-IDF `a2dp_sink` example structure.

### 10.3 Arduino

| Library | Use |
|---|---|
| `BluetoothSerial` (bundled with Arduino-ESP32) | SPP. One include, works immediately. **Compiles only for `esp32`, not `esp32s3`** — that error message is how a lot of people discover the Classic BT gap |
| `BLEDevice` / `NimBLE-Arduino` | BLE 4.2 |
| `ESP32-A2DP` (pschatzmann) | A2DP sink/source with I2S output. The de-facto Arduino route to "Bluetooth speaker" on this chip |
| `arduino-audio-tools` (pschatzmann) | Fuller audio-pipeline layer; pairs with the above |
| `USBHIDKeyboard` etc. | **Not available.** No native USB on this chip — use `esp_hidd` / BLE HID instead |

When configuring I2S in Arduino for this board, the pins are BCK = 25, WS/LRCK = 27, DOUT = 26, and **MCK must be disabled** (§9.1).

---

## 11. Sources and artifacts

### 11.1 Authoritative sources

| Title | URL | Retrieved | Version | Local artifact |
|---|---|---:|---|---|
| ESP32 Series Datasheet | https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf | 2026-08-21 | – | `artifacts/esp32-datasheet.pdf` |
| ESP32 Technical Reference Manual | https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf | 2026-08-21 | – | `artifacts/esp32-technical-reference-manual.pdf` |
| ESP32 Series SoC Errata (ECO and workarounds) | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/esp-chip-errata-en-master-esp32.pdf | 2026-08-21 | esp-docs `master` build | `artifacts/esp32-errata.pdf` |
| ESP Hardware Design Guidelines (ESP32) | https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf | 2026-08-21 | esp-docs `master` build | `artifacts/esp32-hardware-design-guidelines.pdf` |
| **PCN-2021-021 Upgrade ESP32-U4WDH to a Dual-Core Processor Product** | https://documentation.espressif.com/en/PCN-2021-021%20ESP32-U4WDH%20%E5%8D%87%E7%BA%A7%E4%B8%BA%E5%8F%8C%E6%A0%B8%E5%A4%84%E7%90%86%E5%99%A8%E4%BA%A7%E5%93%81.html | 2026-08-21 | doc v1.3, issued 2021-09-02, effective 2021-12-02 | ~~none — HTML only, no PDF published~~ **superseded: a PDF exists, see §19.3 and 11.1a below** |
| ESP-IDF Programming Guide v5.1.4 (esp32 target) | https://docs.espressif.com/projects/esp-idf/en/v5.1.4/esp32/esp-idf-en-v5.1.4-esp32.pdf | 2026-08-21 | v5.1.4 | **archived 2026-08-24** — [record](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |
| ESP-IDF Programming Guide v5.2.5 (esp32 target) | https://docs.espressif.com/projects/esp-idf/en/v5.2.5/esp32/esp-idf-en-v5.2.5-esp32.pdf | 2026-08-21 | v5.2.5 | **archived 2026-08-24** — [record](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |
| ESP-ADF (Audio Development Framework) Programming Guide | https://docs.espressif.com/projects/esp-adf/en/latest/esp-adf-en-master.pdf | 2026-08-21 | esp-docs `master` build | **archived 2026-08-24** — [record](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md) |

**Version skew on the ESP-IDF guide.** The factory image reports **ESP-IDF v5.4-727-g5cbd2a3877**, but Espressif publishes **no PDF build of the ESP-IDF programming guide for v5.3 or later** — PDF generation was dropped after the v5.2 series (verified 2026-08-22: v5.2.5 resolves; v5.3.3, v5.4 and v5.5 all return 404). The v5.2.5 PDF stored here is therefore the closest available *offline* manual, **not** an exact match for the factory firmware, and API details may differ. The v5.1.4 PDF is retained because that is the version Waveshare's own board examples are built against. For an exact v5.4 reference use the HTML docs or build from the `esp-idf` repository at the matching tag.

**No standalone ESP32-U4WDH datasheet exists.** The part is covered by the ESP32 series datasheet. ~~There is likewise no standalone "ECO V3 / chip revision v3 user guide" PDF — chip-revision identification and ECO workarounds are chapters of the ESP32 Series SoC Errata.~~ — **Correction (2026-08-21):** the first sentence is still true; the second is **wrong**. A standalone *ESP32 Chip Revision v3.0 User Guide* PDF does exist and has been retrieved. See §19.3 and the table below.

### 11.1a Sources added 2026-08-21 (sections 13–20)

Primary documents:

| Title | URL | Retrieved | Version | Class | Local artifact |
|---|---|---:|---|---|---|
| **ESP32 Series Datasheet — HTML build** (text-extractable; the PDF's text layer is not) | https://documentation.espressif.com/esp32_datasheet_en.html | 2026-08-21 | **v5.3** | **[DOC]** | `artifacts/esp32-series-datasheet-v5.3.html` |
| **PCN-2021-021 — PDF build** | https://www.espressif.com/sites/default/files/pcn_downloads/PCN-2021-021%20ESP32-U4WDH%20%E5%8D%87%E7%BA%A7%E4%B8%BA%E5%8F%8C%E6%A0%B8%E5%A4%84%E7%90%86%E5%99%A8%E4%BA%A7%E5%93%81.pdf | 2026-08-21 | doc v1.3 (ESP-07-2-007-03); ECN-2021-027 | **[DOC]** | `artifacts/pcn-2021-021-esp32-u4wdh-dual-core.pdf` |
| **ESP32 Chip Revision v3.0 User Guide** | https://documentation.espressif.com/esp32_chip_revision_v3_0_user_guide_en.pdf | 2026-08-21 | v1.3, 2022.11 | **[DOC]** | `artifacts/esp32-chip-revision-v3-0-user-guide.pdf` |
| **ESP32-MINI-1 & ESP32-MINI-1U Datasheet** | https://documentation.espressif.com/esp32-mini-1_datasheet_en.pdf | 2026-08-21 | v1.8 | **[DOC]** | `artifacts/esp32-mini-1-mini-1u-datasheet.pdf` |
| ESP32-MINI-1 / 1U Datasheet — HTML build | https://documentation.espressif.com/esp32-mini-1_datasheet_en.html | 2026-08-21 | v1.8 | **[DOC]** | — |
| Espressif PCN listing filtered to ESP32-U4WDH | https://www.espressif.com/en/taxonomy/term/871 | 2026-08-21 | – | **[DOC]** | — |
| `espressif/esp-hosted` — official radio co-processor framework | https://github.com/espressif/esp-hosted | 2026-08-21 | – | **[DOC]** | — |

### 11.1b Sources added 2026-08-21 (section 21 — silicon revisions)

Fourteen further primary sources were retrieved for the silicon-revision matrix, including **PCN20220901**, the document that announces v3.1. **They are catalogued in full in §21.9** rather than duplicated here. Three new local artifacts result:

| Local artifact | Bytes | What it is |
|---|---:|---|
| `artifacts/pcn20220901-esp32-chip-revision-upgrade.pdf` | 738,047 | The v3.0 → v3.1 (and v1.0 → v1.1) PCN. **The primary v3.1 document** |
| `artifacts/ar2022-005-chip-revision-numbering-scheme.pdf` | 97,490 | The ECO → `vM.X` naming advisory |
| `artifacts/ar2022-003-esp32-v3-aes-fault-injection-advisory.pdf` | 108,350 | Ledger Donjon AES core / flash-encryption side-channel advisory for v3.0 |

Retrieval obstacles, working URL patterns and the errata PDF's text-layer problem are recorded in §21.10.

Community sources (§17 catalogue IDs in brackets):

| Ref | Title | URL | Medium | Date | Class |
|---|---|---|---|---:|---|
| C1 | U4WDH are all the Dn Pins used for internal flash? | https://esp32.com/viewtopic.php?t=17065 | Forum (Espressif staff) | 2020-08-24 | **[COM]** |
| C2 | Cannot program ESP32-U4WDH Flash, flash not detected | https://esp32.com/viewtopic.php?t=28486 | Forum (+ Espressif staff) | 2022-06-21 | **[COM]** |
| C3 | Connecting SD-CARD and JTAG to the ESP32-U4WDH using the HS1 pins | https://esp32.com/viewtopic.php?t=26037 | Forum (+ Espressif staff) | 2022-02-09 | **[COM]** |
| C4 | ESP32-U4WDH crystal mandatory? | https://esp32.com/viewtopic.php?t=25878 | Forum | 2022-01-31 | **[COM]** |
| C5 | ESP32-U4WD Preinstalled Bootloader | https://esp32.com/viewtopic.php?t=31940 | Forum (+ Espressif staff) | 2023-02-03 | **[COM]** |
| C6 | Barebones ESP32-U4WDH with separate programming board | https://esp32.com/viewtopic.php?t=28232 | Forum | 2022-06-07 | **[COM]** |
| C7 | ESP32-U4WDH PSRAM: wiring, which chips, how to use? | https://esp32.com/viewtopic.php?t=45793 | Forum | 2025-06-03 | **[COM]** |
| C8 | `CONFIG_BOOTLOADER_SPI_CUSTOM_WP_PIN=n` fails with ESP32-U4WDH | https://github.com/espressif/esp-idf/issues/6191 | GitHub issue (staff-confirmed) | 2020-12-01 | **[COM]** |
| C9 | ESP32-U4WDH rtc wakeup — **core-count misinformation, §17.2** | https://github.com/espressif/arduino-esp32/issues/9252 | GitHub issue | 2024-02-15 | **[COM]** |
| C10 | ESP32-MINI-1 (ESP32-U4WDH) identified as ESP32-PICO-D2 | https://github.com/espressif/arduino-esp32/issues/10683 | GitHub issue | 2024-12-04 | **[COM]** |
| C11 | fix(esp32): ESP32-U4WDH chip detection by `ESP.getChipModel()` | https://github.com/espressif/arduino-esp32/pull/10695 · https://github.com/espressif/arduino-esp32/pull/10696 | GitHub PRs | 2024-12-08 | **[COM]** |
| C12 | blink / hello_world example crashes on ESP32 U4wdh | https://github.com/espressif/esp-idf/issues/5503 · https://github.com/espressif/esp-idf/issues/6864 | GitHub issues | 2020-06-26, 2021-04-13 | **[COM]** |
| C13 | esptool flash-access and esptool-js stub issues | https://github.com/espressif/esptool/issues/1183 · https://github.com/espressif/esptool/issues/1058 | GitHub issues | 2026-08-21, 2025-01-23 | **[COM]** |
| C14 | ESP32-S3 dual-mode Bluetooth 5.0 (BR/EDR + BLE) — **§20 companion-MCU evidence** | https://esp32.com/viewtopic.php?t=23059 | Forum (+ Espressif staff) | 2021-09-02 | **[COM]** |
| C15 | ESP32-D0WD-V3 vs ESP32-U4WDH for ultra-compact bare-chip PCB | https://www.reddit.com/r/esp32/comments/1myw0wy/esp32d0wdv3_vs_esp32u4wdh_for_ultracompact/ | Reddit | 2025 | **[COM]** |

Commercial / catalogue sources — **all retrieved 2026-08-21, all [WEB], all perishable**:

| Source | URL | Notes |
|---|---|---|
| LCSC `C20622217` | https://www.lcsc.com/product-detail/RF-Transceiver-ICs_Espressif-Systems-ESP32-U4WDH-dual-core_C20622217.html | Price ladder + stock (§16.2). Accessible with a Chrome UA |
| LCSC pinout/footprint image | https://www.lcsc.com/product-image/C20622217.html | — |
| Digi-Key `12153913` | https://www.digikey.com/en/products/detail/espressif-systems/ESP32-U4WDH/12153913 | **403 to all UAs.** Regional alternates: `digikey.ca/.../12153913`, `digikey.com.br/.../12153915` (also 403) |
| Digi-Key catalogue mirror | https://www.digi-electronics.com/en/products/detail/espressif-systems/ESP32-U4WDH/9213418.html | Parametrics reliable; prose is AI-generated and wrong (§17.5) |
| Mouser | https://www.mouser.com/ProductDetail/Espressif-Systems/ESP32-U4WDH?qs=GBLSl2AkirunIR6VFFVeEA%3D%3D | **403 bot-wall to all UAs tried** |
| JLCPCB | https://jlcpcb.com/partdetail/EspressifSystems-ESP32U4WDH/C3013932 · https://jlcpcb.com/partdetail/ESPRESSIFINC-ESP32U4WDH/C529586 | **Two distinct part codes — check both** |
| Octopart | https://octopart.com/esp32-u4wdh-espressif+systems-107540643 | 403 |
| Findchips | https://findchips.com/detail/ESP32-U4WDH | 403 |
| TrustedParts | https://www.trustedparts.com/en/part/espressif-systems/ESP32-U4WDH | 403 |
| Amazon retail single unit | https://www.amazon.com/Espressif-ESP32-U4WDH-IC/dp/B09D33WL5B | — |
| SnapEDA symbol/footprint | https://www.snapeda.com/parts/ESP32-U4WDH/Espressif%20Systems/view-part/ | CAD models |
| Ultra Librarian CAD model | https://app.ultralibrarian.com/details/c41b3ff4-a400-11ed-b159-0a34d6323d74/Espressif-Systems/ESP32-U4WDH | CAD models |

Mirror and re-acquisition notes for every document above are consolidated in **§19.4**.

### 11.2 Local artifacts

| File | Bytes | SHA-256 |
|---|---:|---|
| `artifacts/esp32-datasheet.pdf` | 989,523 | `a7917e6b47528c9dcab06837a49d452e582751335797db879f1cf2d17cd29adf` |
| `artifacts/esp32-technical-reference-manual.pdf` | 10,173,126 | `4ba58e9fa0405ec2bf80b912a29b483f6edc8c4b2b1058201913a2fe37e582f0` |
| `artifacts/esp32-errata.pdf` | 710,473 | `10dadd5993b69c01ed80aa5a1403450bb0487a56b963ff5243137c812f3ebaf1` |
| `artifacts/esp32-hardware-design-guidelines.pdf` | 2,512,576 | `bc9915db9027f2f3975ee1aa5b5f5eabc86d2d626677aba02b971d8a23bce502` |
| ~~`artifacts/esp-idf-programming-guide-v5.1.4-esp32.pdf`~~ **archived 2026-08-24** | 37,852,819 | `05dbacd27a36cd1189f036cfd93d5e711fa3b9a0933dfda63f6ba326b44a384e` |
| ~~`artifacts/esp-idf-programming-guide-v5.2.5-esp32.pdf`~~ **archived 2026-08-24** | 30,789,611 | `02b301cff2b2816ea36bd2cc45003a327097c1005a88274c8f560d73ead6098b` |
| ~~`artifacts/esp-adf-programming-guide.pdf`~~ **archived 2026-08-24** | 25,732,191 | `ed250ded5ae0174ec9b5ba8e4944641f057dd24e1441b5dee37b1a76fe242e61` |
| **added 2026-08-21** | | |
| `artifacts/pcn-2021-021-esp32-u4wdh-dual-core.pdf` | 782,406 | `8ac9154a232cc4a851a2ce774bf53dfb380c9f46494ceb65eb3b1b4fed8a9455` |
| `artifacts/esp32-chip-revision-v3-0-user-guide.pdf` | 350,173 | `7fa403d962987837c516a3b7c2769c06ca33a2b74db76d4e8eedbae28745a9d1` |
| `artifacts/esp32-mini-1-mini-1u-datasheet.pdf` | 1,115,857 | `a1a8d1c571ff339884d910035a193d1a6ca5c066cfec6fee0565064e51570292` |
| `artifacts/esp32-series-datasheet-v5.3.html` | 144,126 | `f95334062f4bbd30d2b56c51805b7824c8ff0f474d56f76319446c4ac4a480fe` |
| **added 2026-08-24 (Waveshare mirror, older revisions)** | | |
| `artifacts/esp32-datasheet-v4.9-waveshare-mirror.pdf` | 991,747 | `608f5d36daa88db44da29cf3fe7e4651e0905301948fb22b0af889433bf1ce9b` |
| `artifacts/esp32-technical-reference-manual-v5.4-waveshare-mirror.pdf` | 10,220,576 | `e897ef6a5b1aaecdfeb4412e98dcedff6ab6175489529fafc58aeca32153aeca` |

All ten PDFs were validated as genuine (`%PDF` header and `%%EOF` trailer both present) on retrieval; the three added 2026-08-21 were validated the same way. The one HTML artifact was checked for a `<!doctype` opening and for the presence of the datasheet body text (the `documentation.espressif.com` soft-404 shell is a distinct 13,745-byte file — see §19.4). Total 111.2 MB.

### 11.2a Multiple document revisions held

Two revisions each of the datasheet and the TRM are held deliberately. The older pair arrived
2026-08-24 from the Waveshare wiki mirror, relocated out of
`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/datasheets/` so component documentation
lives in the component record. Revisions were read from pages 1–2 with `pdftotext`; hashes and
sizes re-verified after the move.

| Document | Revision | Standing | Source | Local path |
|---|---|---|---|---|
| ESP32 Series Datasheet | **v5.3** | current | Espressif direct | `artifacts/esp32-datasheet.pdf` |
| ESP32 Series Datasheet | v4.9 | older | Waveshare mirror, `files.waveshare.com/wiki/common/Esp32_datasheet_en.pdf` | `artifacts/esp32-datasheet-v4.9-waveshare-mirror.pdf` |
| ESP32 Technical Reference Manual | **v5.8** | current | Espressif direct | `artifacts/esp32-technical-reference-manual.pdf` |
| ESP32 Technical Reference Manual | v5.4 | older | Waveshare mirror, `files.waveshare.com/wiki/common/Esp32_technical_reference_manual_en.pdf` | `artifacts/esp32-technical-reference-manual-v5.4-waveshare-mirror.pdf` |

**Which revision applies to the fitted part?** The board fits an **ESP32-U4WDH, silicon revision
v3.1** (see §21). Use the **current** v5.3 / v5.8 documents: this matters more here than for most
parts, because the v4.9 datasheet **predates the dual-core correction** for this exact SKU. The
U4WDH core-count and revision material documented in §14 and §21 is *only* correct in the newer
revisions — reading v4.9 is how the long-running "U4WDH is single-core" misinformation in §17.2
propagated. Do not use v4.9 to answer a core-count or revision question.

The older pair is retained because it is what Waveshare's firmware and wiki were written against,
and it is direct evidence for the sourcing chain behind that misinformation.

> ⚠ **The vendor links older documents.** Waveshare serves ESP32 datasheet **v4.9** and TRM
> **v5.4** from its shared `/wiki/common/` pool. For this part that is not merely stale — v4.9
> carries the superseded core-count description. Prefer the Espressif copies above, and read §21
> alongside whichever revision you open.
>
> Waveshare updates that pool **in place**, so those URLs may begin returning a different revision
> under the same filename. The copies here are revision-pinned by filename and hash; the upstream
> URL is not.

### 11.3 Board-side evidence used in this document

| Evidence | Path (relative to ``) |
|---|---|
| ESP32 schematic sheet (U14, X2, ANT2, U10) | `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/3_ESP32-CHIP.png` |
| ESP32-S3 sheet (net aliases incl. `GPIO0 ↔ I2S_SWITCH_IN`) | `.../2_ESP32S3-R8.png` |
| DAC / CH445P / LDO sheet | `.../5_DAC.png` |
| Knob pull-ups, CN1, power | `.../1_LCD&POWER.png` |
| ESP32 factory firmware | `devices/.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/ESP32-KNOB_ESP32_0.bin` |
| ESP32-S3 factory firmware (for the S3 half of the UART protocol) | `devices/.../Firmware/WX-ESP32S3-KNOB_V1.2.bin` |

### 11.4 Documentation sourcing

Espressif's documentation hosts, URL templates, migrated document classes, PCN discovery method and validation procedure are documented once, reusably, in the **[Espressif vendor guide](../../../vendors/espressif/README.md)**. Read it before attempting to acquire any further Espressif document — it will save you the 404 hunt.

Note on source URLs: the `www.espressif.com/sites/default/files/documentation/*.pdf` paths now HTTP-redirect to Espressif's newer documentation platform. The datasheet and TRM still resolve to real PDFs through that redirect; the errata and hardware design guidelines have been migrated into the versioned `esp-docs` projects, whose PDF build URLs are given above.

---

## 12. Open questions

| # | Question | Why it matters | How to close it |
|---:|---|---|---|
| 1 | ~~**Single-core 160 MHz or dual-core 240 MHz?**~~ (§2) | Determines your entire CPU budget and whether core affinity is meaningful | **CLOSED 2026-08-21 → dual core, 240 MHz (§14).** Datasheet v5.3 Table 1-1 states it; nomenclature confirms it; a real esptool capture reports it. To verify *your* die offline, read line 5 of the top marking — a leading **`D`** means dual-core (§14.2). Residual risk: pre-2021-12-02 single-core parts exist under the same MPN, so §2.2's defensive coding still applies |
| 2 | **Inter-MCU UART frame format and baud rate** (§6) | You cannot interoperate with stock firmware on either side without it | Logic-analyser tap on GPIO23/GPIO18 with auto-baud, or disassemble `uart1.c`/`uart1.cpp` |
| 3 | **CH445P truth table: which `IN` level selects which bank?** (§9.1) | Determines the power-on default audio source and whether S3 GPIO0's boot-strap pull-up puts you on the right bank | Obtain a real CH445P datasheet, or measure continuity while toggling S3 GPIO0 |
| 4 | **How does S3-only audio get past `XSMT`?** (§9.2) | If you reflash the U4WDH you may silently kill all audio, including the S3's | Scope `XSMT` with stock firmware; test S3 audio with the U4WDH held in reset |
| 5 | **USB-C orientation-select topology** (§7.1) | The receptacle is absent from all five schematic sheets | Board teardown / continuity mapping; USB descriptor capture in both orientations |
| 6 | **USB-UART bridge part number** (§7.2) | Driver guidance for users is currently a guess | Legible photo of U10's top marking |
| 7 | **Where do `ESP32_IO2`, `IO4`, `IO21`, `IO33` actually go?** (§5.2) | These are the only candidate spare pins on the chip | Continuity mapping against `CN1` and any test points |
| 8 | **Is `BTAUDIOMATE` the advertised BT name?** (§4) | Cosmetic but useful for identification | Scan for the device from a phone |
| 9 | **Exact chip revision / applicable ECOs** | Errata workarounds are revision-specific | `esptool chip_id` revision output, cross-referenced with `artifacts/esp32-errata.pdf`. **Narrowed 2026-08-21:** datasheet v5.3 Table 1-1 restricts U4WDH to **v3.0 or v3.1 only**, so `artifacts/esp32-chip-revision-v3-0-user-guide.pdf` applies in full (§19.3) |
| 10 | ~~**Ordering-suffix field-by-field decoding**~~ (§1.1) | Currently `[INF]` for every field except the `4` | **CLOSED 2026-08-21 → §13.1.** Read verbatim from Figure 1-1 of the datasheet's **HTML** build. `U` = dual core, `4` = 4 MB in-package flash, `WD` = Wi-Fi + dual-mode BT, `H` = high temperature, no `Q6` = QFN 5×5 |
| 11 | **Which line-5 marking does U14 actually carry?** (§14.2) | The one remaining way to confirm this specific chip's core count without powering it | Macro photograph of U14's top marking under magnification. Also: locate the **ESP32 Chip Packaging Information** document, which defines the full marking layout — not found under any slug tried (§19.4) |
| 12 | **Is U4WDH's 85 °C ceiling reflected anywhere in this product's rating?** (§13.3) | Distributors misreport this by 20 °C; a knob in a warm enclosure is not obviously safe | Compare against Waveshare's stated product operating range; measure U14 case temperature under sustained A2DP load |
| 13 | **Why does Espressif use `U` rather than `D` for dual core here?** (§13.4) | Pure curiosity, but it is the root of the recurring core-count confusion (§17.2) | Not answered by any retrieved document. Espressif support enquiry |
| 14 | **Are GPIO9/GPIO10 genuinely free on U4WDH?** (§18.1) | They are *not* in the in-package flash map, unlike on external-flash ESP32 parts — potentially two extra pins | Bench test on a spare U4WDH; cross-check the IO_MUX appendix of `artifacts/esp32-series-datasheet-v5.3.html` |

---

## 13. The chip in its own right: identity, nomenclature and siblings

Everything above this line is about U14 *on this board*. Sections 13–20 are about the part number, so that you can reason about it in a design that has nothing to do with a Waveshare knob.

The authority for all of §13 is the **ESP32 Series Datasheet v5.3**. Espressif publishes it in two forms from the same content: a PDF whose text layer is glyph-subset encoded and effectively unreadable by tooling (this is the `artifacts/esp32-datasheet.pdf` problem recorded in §1.1), and an **HTML build whose text extracts cleanly**. The HTML build has been retrieved into `artifacts/esp32-series-datasheet-v5.3.html`. **Use the HTML copy whenever you need to quote or search the datasheet.** Everything quoted below came out of it verbatim.

### 13.1 The ordering nomenclature, decoded — this replaces §1.1

Datasheet v5.3, **Figure 1-1 "ESP32 Series Nomenclature"**, transcribed **[DOC]**:

~~~
ESP32 - D 0 W D R2 - V3
        │ │ └┬┘ │    └── Chip revision:  V3 = revision v3.0 or newer
        │ │  │  └─────── In-package PSRAM:  R2 = 2 MB PSRAM
        │ │  └────────── Connection:  WD = Wi-Fi b/g/n + Bluetooth/Bluetooth LE dual mode
        │ └───────────── In-package flash:  0 = none, 2 = 2 MB, 4 = 4 MB
        └─────────────── Core:  D or U = Dual core,  S = Single core

  further suffix letters:
        H  = High temperature
        Q6 = QFN 6*6 package     (absent = QFN 5*5)
~~~

Applying that to **ESP32-U4WDH**, field by field. Compare against the `[INF]` guesses in §1.1:

| Field | §1.1 guess (2026-08-22) | Datasheet v5.3 says | Verdict |
|---|---|---|---|
| `U` | "package/variant letter … does **not** follow the D/S core pattern, which is precisely why the core count is ambiguous" | **Core field. `D` *or* `U` = Dual core.** `U` sits in the same slot as `D` and carries the same meaning | **Wrong, and consequentially so.** The letter that was thought to make core count ambiguous is in fact the letter that *states* it. See §14 |
| `4` | 4 MB embedded flash | **4 = 4 MB in-package flash** | **Correct** |
| `WD` | "same `WD` group letters …; not decoded here" | **Connection field: Wi-Fi b/g/n + Bluetooth/Bluetooth LE dual mode.** Not a package code at all | Now decoded |
| `H` | "Extended/high temperature grade … do **not** design to a temperature range on the basis of this letter" | **High temperature.** But see the trap in §13.3 — the letter is real and the caution was *exactly right* | Caution vindicated |
| (no `Q6`) | — | Absence of `Q6` means **QFN 5×5**, matching the 48-pin 5×5 package in §1 | Confirms §1 |

**[DOC]** So the part number reads: *dual-core, 4 MB in-package flash, Wi-Fi + dual-mode Bluetooth, high-temperature grade, QFN 5×5.*

**Open question 10 in §12 is closed.**

### 13.2 The series comparison table — where U4WDH sits

Datasheet v5.3, **Table 1-1 "ESP32 Series Comparison"**, transcribed in full **[DOC]**:

| Part Number | Core | Chip Revision | In-Package Flash/PSRAM | Package | VDD_SDIO Voltage | Lifecycle |
|---|---|---|---|---|---|---|
| ESP32-D0WD-V3 | Dual core | v3.0/v3.1 | — | QFN 5×5 | 1.8 V / 3.3 V | **Active** |
| **ESP32-U4WDH** | **Dual core** ᶜ | v3.0/v3.1 | **4 MB flash** | **QFN 5×5** | **3.3 V only** | **Active** |
| ESP32-D0WDR2-V3 | Dual core | v3.0/v3.1 | 2 MB PSRAM | QFN 5×5 | 3.3 V | **EOL** → ESP32-D0WDRH2-V3 |
| ESP32-D0WDQ6-V3 | Dual core | v3.0/v3.1 | — | QFN 6×6 | 1.8 V / 3.3 V | NRND |
| ESP32-D0WD | Dual core | v1.0/v1.1 | — | QFN 5×5 | 1.8 V / 3.3 V | NRND |
| ESP32-D0WDQ6 | Dual core | v1.0/v1.1 | — | QFN 6×6 | 1.8 V / 3.3 V | NRND |
| ESP32-S0WD | **Single core** | v1.0/v1.1 | — | QFN 5×5 | 1.8 V / 3.3 V | NRND |

ᶜ Datasheet footnote 3, verbatim: *"ESP32-U4WDH will be produced as dual-core instead of single core. See PCN-2021-021 for details."*

Four things in that table matter more than they look:

1. **U4WDH and D0WD-V3 are the only two ESP32-series bare chips that are neither NRND nor EOL.** Everything else in the original ESP32 line is on the way out. If you are designing new with a classic ESP32 die, your choice is essentially *these two* — and the axis between them is "do I want the flash in the package or on the board".
2. **ESP32-D2WD is not in the table at all.** It appears in older datasheet revisions and in the flash pin-mapping notes, and forum threads still reference it (§17), but it has dropped off the current comparison. Do not design it in.
3. **VDD_SDIO on U4WDH is 3.3 V only** — it is the one column where U4WDH differs from D0WD-V3. This is not a detail. It is the single most common way people brick a U4WDH bring-up, and §18.3 explains why.
4. **ESP32-S0WD is the only single-core part in the whole table** — and it is NRND. This is worth holding on to, because it is the root of a widespread piece of community misinformation about U4WDH (§17.2).

Datasheet footnote 6 also specifies the in-package flash itself **[DOC]**: *"More than 100,000 program/erase cycles"* and *"More than 20 years data retention time."* If you are considering a wear-heavy NVS or logging workload on this part, those are the numbers to budget against.

### 13.3 The temperature trap — `H` means the opposite of what you would assume

This is the most surprising finding in this whole section, and it directly vindicates §1.1's warning.

Datasheet v5.3, **Table 5-2 note 3**, verbatim **[DOC]**:

> *"The operating temperature of ESP32-U4WDH and ESP32-D0WDRH2-V3 ranges from **–40 °C to 85 °C**, due to the in-package flash or PSRAM. For other chips that have no in-package flash or PSRAM, their operating temperature is **–40 °C ~ 125 °C**."*

So:

- The `H` ("High temperature") letter is a **grade marker on the die**, not a promise about the finished part.
- **The in-package flash is the limiting component.** Putting flash inside the package *costs* you 40 °C of operating range relative to a bare ESP32-D0WD-V3 with the same flash sitting outside it.
- **ESP32-U4WDH is therefore the *narrowest*-temperature part in the ESP32 series, not the widest.**

This is actively contradicted by the parts catalogues, which is exactly why it is worth stating loudly:

| Source | Claimed operating temperature | Retrieved | Assessment |
|---|---|---:|---|
| **ESP32 Series Datasheet v5.3, Table 5-2 note 3** | **–40 °C to +85 °C** | 2026-08-21 | **[DOC]** — authoritative. Use this |
| LCSC product page C20622217 | −40 °C ~ +105 °C | 2026-08-21 | **[WEB]** — wrong. Appears to be a generic ESP32-series figure, or the MINI-1-**H4** module figure, pasted onto the chip |
| digi-electronics.com (Digi-Key catalogue mirror) | "–40 °C to 105 °C, aligning with industrial-grade requirements" | 2026-08-21 | **[WEB]** — wrong, and it is machine-generated marketing prose built on top of the wrong number. See §17.5 |

**Do not quote 105 °C for this chip.** The 105 °C figure is real, but it belongs to the **module** part numbers `ESP32-MINI-1-H4` / `ESP32-MINI-1U-H4`, where it is specified as a *module ambient* rating (§15.1) — a different measurement of a different object. The bare die's own operating range is 85 °C.

**Absolute maximum storage** temperature is separately −40 °C to 150 °C (Table 5-1) **[DOC]**. Storage ≠ operating.

### 13.4 The other siblings you asked about

**ESP32-PICO series** does not appear in Table 1-1 because it is not a bare chip in the same sense — the PICO parts (PICO-D4, PICO-V3, PICO-V3-02) are **SiP** packages that integrate crystal, flash, and in the `-02` case PSRAM, into one LGA module-like package. They are documented in their own datasheets. Relative to U4WDH:

| | ESP32-U4WDH | ESP32-PICO-V3-02 |
|---|---|---|
| What it is | Bare QFN die + in-package flash | SiP: die + **crystal** + flash + PSRAM |
| External crystal needed? | **Yes** — mandatory 40 MHz (§18.2) | No, integrated |
| PSRAM | None in package (§18.5) | 2 MB integrated |
| Package | QFN 5×5, 48-pin, solderable by hand with effort | LGA — **notoriously painful to hand-solder** **[COM]**, §17.1 ref C4 |
| Board area | Larger (needs crystal + caps) | Smallest |

The PICO parts are the answer when board area is the binding constraint and you will pay for it; U4WDH is the answer when unit cost is the binding constraint. A 2025 Reddit thread comparing exactly these for an ultra-compact bare-chip design reaches the same conclusion **[COM]** (§17.1, ref C15).

**Naming footnote worth internalising:** in `ESP32-S0WD` the `S` genuinely does mean **S**ingle core, and in `ESP32-D0WD` the `D` genuinely does mean **D**ual core. The trap that §1.1 fell into was assuming `U` therefore encoded something *other* than core count. It does not — per Figure 1-1 it occupies the same field and means the same thing as `D`. Why Espressif used a second letter for "dual" is not explained in any document retrieved here, and remains an open curiosity (§12, new question 13).

---

## 14. Core count: resolved

**Short answer: dual core, 240 MHz capable.** Four independent lines of evidence agree, and there is a fifth that lets you check your specific chip without powering it on.

### 14.1 The evidence

**1. The current datasheet says so outright. [DOC]**
ESP32 Series Datasheet v5.3, Table 1-1, lists ESP32-U4WDH as **"Dual core"**, with footnote 3 pointing at PCN-2021-021. Datasheet §4.1.1 further specifies the 7-stage pipeline supports *"the clock frequency of up to 240 MHz (160 MHz for ESP32-S0WD (NRND))"* — U4WDH is not carved out of the 240 MHz statement; only S0WD is.

**2. The nomenclature says so. [DOC]**
Figure 1-1: `U` is the core field and means Dual core (§13.1).

**3. PCN-2021-021, now read in full. [DOC]**
The PCN PDF has been retrieved and its text transcribed (§19.3). Verbatim:

> *"ESP32-U4WDH is a single-core chip based on ESP32 ECO V3 and supports CPU clock frequency of up to 160 MHz. The chip embeds a 4 MB flash, which reduces design space and lowers cost for customer, and is thus favored by customers. … Espressif decides to upgrade this chip specification …"*
>
> *"Upgrade ESP32-U4WDH from a single-core processor to a dual-core processor; upgrade the supported maximum CPU clock frequency from 160 MHz to 240 MHz."*

with Appendix I:

| Item | Before Change | After Change |
|---|---|---|
| Processor | Single-core | **Dual-core** |
| Maximum CPU Clock Frequency | 160 MHz | **240 MHz** |
| ESP32 Datasheet | v3.7 | v3.8 |
| ESP32-MINI-1 & ESP32-MINI-1U Datasheet | v1.0 | v1.1 |

Document metadata **[DOC]**: Document No. `ESP-07-2-007-03`, version **1.3**, PCN No. **PCN-2021-021**, category **R**, issue date **2021-09-02**, proposed date of change **2021-12-02**, date of first shipment **2021-12-02**, related **ECN-2021-027**.

**4. A real chip reported it. [COM]**
ESP32 Forum thread 28486, post dated **2022-06-21**, user `Stef_Esp32` pasting unmodified `esptool.py v3.3-dev` output from a custom board:

~~~
Chip is ESP32-U4WDH (revision 3)
Features: WiFi, BT, Dual Core, 240MHz, Embedded Flash, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
~~~

That is a post-change part, self-reporting from eFuse, saying **Dual Core, 240MHz**. A second capture in `arduino-esp32` issue 10683 (2024-12-04) shows `esptool.py v4.5.1` reporting `Chip is ESP32-U4WDH (revision v3.1)` **[COM]**.

### 14.2 How to tell *your* chip apart — without powering it on

This is the genuinely new capability, and it comes from the PCN's Appendix I marking specification. PCN-2021-021 changed the **top marking** of the chip at the same time as the silicon, specifically so that the two builds are distinguishable. Verbatim **[DOC]**:

> **ESP32-U4WDH Marking Spec — Line 5, "Product Type & Flash Tracking Information" changes.**
> *Before change:* Total **8** characters on Line 5; 1st character: shows **`H`**.
> *After change:* Total **9** characters on Line 5; 1st character: shows **`D`**; 2nd character: shows **`H`**.

So, under magnification, on **line 5** of the chip's top marking:

| What you see on line 5 | Length | Meaning |
|---|---|---|
| Starts **`D`**, then `H`… | 9 chars | **Dual-core part** — post-2021-12-02 |
| Starts **`H`**… | 8 chars | **Single-core part**, 160 MHz max — pre-2021-12-02 |

**A leading `D` is the dual-core marker.** This is a direct, offline answer to §12 open question 1 for the chip on your board, needing only a microscope or a macro photograph. The same PCN applies the same rule to the modules: `ESP32-MINI-1` and `ESP32-MINI-1U` single-core units show `XXXXXX`, dual-core units show `DXXXXX`.

The three runtime/eFuse methods in §2.1 remain valid and are easier if the board is already powered; use the marking when it is not, or when you are inspecting stock before assembly.

### 14.3 What has *not* changed

**A single-core U4WDH is still a physically real object.** Espressif shipped them until 2021-12-02, and — this is the important part — **the part number did not change**. PCN-2021-021 §5.3, verbatim **[DOC]**:

> *"Customers can continue using the existing chip product name to place orders. There is no change to the MPN of the affected Espressif modules … Customers can continue using the existing MPN to place orders."*

So `ESP32-U4WDH` on a BOM, a reel label, or a schematic symbol tells you **nothing** about core count. Only the date code, the line-5 marking, or the running silicon does. Given this board's vintage a dual-core part is overwhelmingly likely, but "overwhelmingly likely" is not "verified", and §2's defensive-coding advice stands.

Espressif's own recommended mitigation, verbatim from the PCN **[DOC]**, is the same advice §2.2 arrived at independently:

> *"If the customer needs to use single- and dual-core processor products for the same client product, for compatibility with the previous client products before this change, the customer should keep using the same software configuration before this change, i.e., using a single-core processor and a maximum CPU frequency of 160 MHz."*

The PCN's software-verification note spells out the exact menuconfig settings that produce a binary running correctly on **both** builds **[DOC]**: `Component config → ESP32-specific → CPU frequency → 160 MHz`, and `Component config → FreeRTOS → Run FreeRTOS only on first core`.

One consequence worth flagging for this board: the RF side is unaffected. PCN §5.4, verbatim **[DOC]**: *"The change does not affect the RF performance of the modules and does not affect the validity of their existing RF certifications."*

---

## 15. Where else this chip is used

### 15.1 Espressif's own modules — the largest deployment by far

The single biggest consumer of ESP32-U4WDH is **Espressif itself**. PCN-2021-021 §1 lists the affected products as **[DOC]**:

> *Chip Product: ESP32-U4WDH. Module Products: ESP32-MINI-1, ESP32-MINI-1U.*
> *"The main chip used in the modules listed in para 1 is ESP32-U4WDH."*

Confirmed independently by the **ESP32-MINI-1 / ESP32-MINI-1U Datasheet v1.8** **[DOC]** (retrieved into `artifacts/esp32-mini-1-mini-1u-datasheet.pdf`):

> *"ESP32-U4WDH embedded, Xtensa dual-core 32-bit LX6 microprocessor, up to 240 MHz"*
> *"At the core of this module is ESP32-U4WDH, an Xtensa 32-bit LX6 CPU that operates at up to 240 MHz."*

The module family, from that datasheet **[DOC]**:

| Part Number | Flash | Ambient Temp. | Size (mm) | Antenna |
|---|---|---|---|---|
| ESP32-MINI-1-N4 | 4 MB | −40 ~ **85** °C | 13.2 × 19.0 × 2.4 | On-board PCB antenna |
| ESP32-MINI-1-H4 | 4 MB | −40 ~ **105** °C | 13.2 × 19.0 × 2.4 | On-board PCB antenna |
| ESP32-MINI-1U-N4 | 4 MB | −40 ~ **85** °C | 13.2 × 13.5 × 2.4 | External antenna connector |
| ESP32-MINI-1U-H4 | 4 MB | −40 ~ **105** °C | 13.2 × 13.5 × 2.4 | External antenna connector |

Note the module datasheet's own framing of the ambient figure **[DOC]**: *"Ambient temperature specifies the recommended temperature range of the environment immediately outside the Espressif module."* That is a system-level rating measured outside the can — it is **not** the die's operating range, and it does not override §13.3. If you need to reconcile the two numbers, treat 85 °C as the number you design the silicon to and 105 °C as a module-level qualification claim you would need Espressif to substantiate for your duty cycle.

The MINI-1 datasheet also gives the module's GPIO budget **[DOC]**, which is really the U4WDH budget with the module's own wiring subtracted: *"Up to 28 GPIOs — 5 strapping GPIOs, 6 GPIOs used for in-package flash, 6 input-only GPIOs."* That "6 GPIOs used for in-package flash" is the constraint §18.1 enumerates.

Because ESP32-MINI-1 is the module inside **ESP32-DevKitM-1**, Espressif's own low-cost development kit, every DevKitM-1 in the world contains an ESP32-U4WDH. This is corroborated from an unexpected direction: in ESP32 Forum thread 31940 a developer debugging a custom U4WDH board writes **[COM]** *"I bought ESP Mini 1 Dev kit and replaced the ESP32-U4WDH with mine. And it worked"* — a die-level swap between the DevKitM-1 module and a bare chip, which only works because they are the same part.

### 15.2 Third-party designs

Evidence here is thinner and almost entirely of the form "an engineer on a forum is designing with it", rather than "here is a named shipping product". That is itself informative: **U4WDH is a component that shows up inside other people's products rather than a product that gets written about.** Catalogued instances **[COM]**:

| Design | Where | Date | What it establishes |
|---|---|---:|---|
| Industrial data-logger with SD card + JTAG, by **Seneca** (Italian industrial automation vendor) | ESP32 Forum t=26037 | 2022-02-09 | A named commercial vendor selecting U4WDH for an industrial product; also the source of the HS1/HS2 finding in §18.1 |
| Board migrating **from ESP32-D2WD to ESP32-U4WDH** | ESP32 Forum t=28486 | 2022-06-21 | U4WDH as the successor for designs built on the older 2 MB in-package-flash part |
| Board migrating **from ESP32-PICO-D4 to ESP32-U4WDH** | ESP32 Forum t=25878 | 2022-01-31 | Cost/solderability-driven move off the LGA SiP |
| Board migrating **from ESP32-WROOM-32E module to ESP32-MINI-1** | GitHub `arduino-esp32` #10683 | 2024-12-04 | Motive stated verbatim: *"gives me 2 extra IO pins which come in handy"* |
| Board migrating **from ESP32-WROOM-32U module to bare ESP32-U4WDH** | GitHub `arduino-esp32` #9252 | 2024-02-15 | Module → bare-chip cost-down, and the deep-sleep surprise that followed |
| Barebones minimum-footprint U4WDH design with off-board programmer | ESP32 Forum t=28232 | 2022-06-07 | The "smallest possible ESP32" use case |
| Custom PCB, first bring-up | ESP32 Forum t=31940 | 2023-02-03 | Typical bring-up failure mode (§18.4) |
| Custom PCB attempting external PSRAM | ESP32 Forum t=45793 | 2025-06-03 | Still in active use in new designs in 2025 |

**This board — the Waveshare ESP32-S3-Knob-Touch-LCD-1.8 — is the only *shipping consumer product* identified in this research that uses a bare ESP32-U4WDH.** That is a statement about the limits of the search, not a proof of uniqueness; bare chips inside sealed consumer products are invisible without teardowns, and no U4WDH teardown was located.

### 15.3 The application profile

Synthesising the datasheet's framing, the MINI-1 positioning and the migration patterns above, U4WDH is chosen when **all three** of these are true:

1. **You need Bluetooth Classic (BR/EDR)** — or you would already be on a C3/C6/S3 (§19).
2. **Board area or BOM line count is tight** — the in-package flash removes a flash IC, its decoupling, and six routed nets. The MINI-1 datasheet's own words **[DOC]**: *"especially suitable for applications within a compact space, such as bulbs, switches and sockets."*
3. **Volume justifies bare-die integration** — you are absorbing the RF certification cost yourself (§18.6).

Datasheet-listed applications for the series include smart home, industrial automation, POS terminals, audio devices, and touch/proximity sensing **[WEB]** (LCSC's mirror of the datasheet feature list, 2026-08-21). The U4WDH-specific slice of that is the cost-sensitive, space-constrained, Classic-Bluetooth-requiring corner — smart lighting, switches, sockets, and Bluetooth audio endpoints. This board sits squarely in the last of those.

---

## 16. Availability, pricing and lifecycle

**All figures below are point-in-time observations retrieved 2026-08-21 and will be stale by the time you read them.** They are recorded with quantity break, currency and source so they can be re-checked, not so they can be trusted indefinitely.

### 16.1 Lifecycle status

| Statement | Source | Class |
|---|---|---|
| **Active.** ESP32-U4WDH is one of only two ESP32-series bare chips in the v5.3 datasheet carrying no NRND or EOL annotation (the other is ESP32-D0WD-V3) | ESP32 Series Datasheet v5.3, cover + Table 1-1 | **[DOC]** |
| Product Status: **Active** | Digi-Key catalogue (via `digi-electronics.com` mirror) | **[WEB]** |
| No EOL or NRND PCN for U4WDH found on Espressif's PCN portal | Espressif PCN listing for U4WDH (`taxonomy/term/871`) | **[WEB]** |

For contrast, sibling lifecycle events *are* published and were found: **ESP32-D0WDR2-V3 is EOL**, upgraded to ESP32-D0WDRH2-V3 per **PCN20251001**, and the v1.x/v3.x chips were re-based to revision v1.1/v3.1 per **PCN20220901** **[DOC]** (datasheet v5.3, Table 1-1 footnotes 4, 5, 7). The absence of a comparable U4WDH notice is meaningful: this part is being actively carried, not wound down.

### 16.2 Pricing and stock, 2026-08-21

**LCSC** — part `C20622217`, listed under the product-page slug `…ESP32-U4WDH-dual-core…` (the URL itself asserts dual-core) **[WEB]**:

| Quantity break | Unit price (USD) | Extended |
|---:|---:|---:|
| 1 | $2.9282 | $2.93 |
| 10 | $2.6020 | $26.02 |
| 30 | $2.4069 | $72.21 |
| 100 | $2.2462 | $224.62 |
| 500 | $2.1380 | $1,069.00 |
| 1,000 | $2.0888 | — |

- Stock: **383 pieces**, "In stock, ships now"
- Minimum order: **1 piece**; order multiple: 1
- Full reel (`minPacketNumber`): **5,000 pieces**
- Package: **QFN-48-EP(5×5)**

**Digi-Key** — part detail 12153913 **[WEB]**, retrieved via catalogue mirror because Digi-Key returned HTTP 403 to every user-agent tried (§19.4):

| Attribute | Value |
|---|---|
| Digi-Key part numbers | `1904-ESP32-U4WDHCT` (cut tape), `1904-ESP32-U4WDHDKR` (Digi-Reel), `1904-ESP32-U4WDHTR` (tape & reel) |
| Packaging | Tape & Reel (TR) |
| Standard Package | **5,000** |
| Product Status | Active |
| Moisture Sensitivity Level | **MSL 3 (168 hours)** |
| RoHS / REACH | ROHS3 Compliant / REACH Unaffected |
| ECCN / HTSUS | 5A992C / 8517.62.0090 |
| Memory Size | 4 MB Flash, 448 kB ROM, 520 kB SRAM |
| Power output | 19.5 dBm |

**MSL 3 is worth pulling out of that table.** It means floor life is limited and the reel needs baking if the moisture bag has been open too long — a real assembly constraint that a module (typically MSL 3 as well, but pre-qualified) does not spare you.

Other listings located but not priced here: JLCPCB carries the part under **two** distinct part codes, `C3013932` and `C529586` — if you are ordering JLCPCB assembly, check which code has basic/extended status and stock before committing. Mouser lists it as `ESP32-U4WDH`; Amazon carries a retail single-unit listing (`B09D33WL5B`). Aggregator pages exist on Octopart (`107540643`), Findchips, and TrustedParts. All URLs are in §19.

**Order-of-magnitude read:** at roughly **$2.10–2.90** in small quantity, U4WDH sits *above* the flash-less siblings — the same Digi-Key mirror lists ESP32-D0WD-V3, ESP32-S0WD, ESP32-D2WD and ESP32-D0WDQ6 at **$1.5852** **[WEB]**. You are paying roughly **$0.50–1.30 per unit for the in-package flash**, against a discrete 4 MB SPI NOR that costs well under $0.50. **The economic case for U4WDH is therefore not the flash die — it is the board area, the six freed routing channels, the removed BOM line, and the removed placement.** That is consistent with Espressif's own stated rationale in PCN-2021-021: *"reduces design space and lowers cost for customer."*

---

## 17. Community and ecosystem

Every entry is catalogued with who said it, when, and what it actually establishes. Espressif-staff posts are marked, because they carry near-**[DOC]** weight.

### 17.1 Catalogue

| # | Source | Medium | Date | Evidence type | What it establishes |
|---:|---|---|---:|---|---|
| C1 | ESP32 Forum **t=17065** — "U4WDH are all the Dn Pins used for internal flash?" | Forum, **Espressif staff (`igrr`)** | 2020-08-24 | **[COM]**, staff quoting datasheet | The complete embedded-flash pin map, plus the DIO/QIO nuance. **The single most useful thread about this chip.** See §18.1 |
| C2 | ESP32 Forum **t=28486** — "Cannot program ESP32-U4WDH Flash, flash not detected" | Forum, user + **Espressif staff (`Sprite`)** | 2022-06-21 → 06-24 | **[COM]** | The MTDI / VDD_SDIO 1.8 V bricking trap and its eFuse fix (§18.3); *also* the `Dual Core, 240MHz` esptool capture (§14.1); *also* staff confirmation on GPIO16/17 |
| C3 | ESP32 Forum **t=26037** — "Connecting SD-CARD and JTAG … using the HS1 pins" | Forum, user + **Espressif staff (`LJH`)** | 2022-02-09 → 02-10 | **[COM]** | HS1/SPI2 is unusable on U4WDH; SD card must go on HS2. Names datasheet **v3.8** as the source of the flash pin map |
| C4 | ESP32 Forum **t=25878** — "ESP32-U4WDH crystal mandatory?" | Forum, users | 2022-01-31 → 2026-01-18 | **[COM]** | External 40 MHz crystal is mandatory; a PICO-D4 migrant lost time to this (§18.2) |
| C5 | ESP32 Forum **t=31940** — "ESP32-U4WD Preinstalled Bootloader" | Forum, user + **Espressif staff (`Sprite`)** | 2023-02-03 → 02-22 | **[COM]** | ROM bootloader is always present; the CHIP_PU RC network and ≥600 mA LDO requirements (§18.4) |
| C6 | ESP32 Forum **t=28232** — "Barebones ESP32-U4WDH with separate programming board" | Forum, users | 2022-06-07 | **[COM]** | Minimum-footprint design pattern; off-board USB-UART. Unanswered — a gap in the community record |
| C7 | ESP32 Forum **t=45793** — "ESP32-U4WDH PSRAM: wiring, which chips, how to use?" | Forum, user | 2025-06-03 | **[COM]** | External PSRAM on U4WDH is hard and the user failed; quotes Espressif's FAQ (§18.5). **Zero replies** |
| C8 | GitHub `espressif/esp-idf` **#6191** — "CONFIG_BOOTLOADER_SPI_CUSTOM_WP_PIN=n fails with ESP32-U4WDH" | Issue, **Espressif staff (`projectgus`)** | 2020-12-01 → 2021-06-28 | **[COM]**, staff-confirmed bug | A real, acknowledged IDF bug specific to this chip's QIO mode, with a workaround (§18.7) |
| C9 | GitHub `espressif/arduino-esp32` **#9252** — "ESP32-U4WDH rtc wakeup" | Issue, **Espressif staff (`SuGlider`)** + community | 2024-02-15 | **[COM]** | The **core-count misinformation incident** — see §17.2. Also EXT0 deep-sleep wake debugging |
| C10 | GitHub `espressif/arduino-esp32` **#10683** — "ESP32-MINI-1 (ESP32-U4WDH) identified as ESP32-PICO-D2" | Issue | 2024-12-04 → 12-09 | **[COM]**, fixed | Arduino core misreported this chip for years (§17.3) |
| C11 | GitHub `espressif/arduino-esp32` **#10695 / #10696** | Pull requests | 2024-12-08 | **[COM]** | The fix for C10 |
| C12 | GitHub `espressif/esp-idf` **#5503**, **#6864** — "blink/hello_world example crashes on ESP32 U4wdh" | Issues | 2020-06-26, 2021-04-13 | **[COM]** | Early-adopter instability on this part in the 2020–21 window |
| C13 | GitHub `espressif/esptool` **#1183**, **#1058** | Issues | 2025-01-23, 2026-08-21 | **[COM]** | Ongoing flash-access and macOS/esptool-js stub issues on U4WDH and MINI-1 |
| C14 | ESP32 Forum **t=23059** — "ESP32-S3 dual-mode Bluetooth 5.0 (BR/EDR + BLE)" | Forum, **Espressif staff (`Sprite`)** + community | 2021-09-02 → 09-12 | **[COM]** | Staff confirmation that S3 has no BR/EDR, **and the only located discussion of the companion-MCU pattern** (§20) |
| C15 | Reddit `r/esp32` — "ESP32-D0WD-V3 vs ESP32-U4WDH for ultra-compact bare-chip PCB" | Reddit thread | 2025 | **[COM]** | Real designers weighing exactly this trade-off; PICO-V3-02 raised as the area-optimal alternative (§13.4) |
| C16 | LCSC `C20622217`, JLCPCB `C3013932`/`C529586`, Digi-Key `12153913`, Mouser, Octopart, SnapEDA, Ultra Librarian | Distributor / CAD-model pages | 2026-08-21 | **[WEB]** | Pricing, stock, packaging (§16); footprint and symbol availability |

### 17.2 The core-count misinformation incident — worth reading in full

This is the most instructive thread in the catalogue, because it shows the wrong answer being given by someone with authority and then corrected by the community.

In `arduino-esp32` issue **#9252** (2024-02-15), an Espressif staff member (`SuGlider`) responded to a U4WDH question with **[COM]**:

> *"The ESP32-U4WDH module is based on the ESP32-SOLO-1 chip variant, which is a single-core processor."*

That is **wrong on two counts**: U4WDH is a chip, not a module, and it is not SOLO-1-based. The staff member went on to recommend single-core workarounds — `CONFIG_FREERTOS_UNICORE`, pinning everything to core 0, third-party solo-core Arduino forks — which would have cost the reporter half their CPU for no reason.

Community member `Jason2866` corrected it the same day **[COM]**:

> *"Regarding to the datasheet the ESP32-U4WDH is a dual core. If it would be a single core it would get stuck in bootloader code already. It was a one core but the actual ones are dual core."*

— attaching the PCN-2021-021 **PDF** link. The staff member accepted the correction, and the reporter confirmed: *"Dualcore working fine…"*.

Three lessons, all of which this document has now acted on:

1. **The U4WDH/SOLO-1 confusion is a live, recurring error** — and it is easy to see how it starts, since S0WD is genuinely the single-core part (§13.2) and U4WDH genuinely *was* single-core before 2021-12-02.
2. **Espressif staff answers are high-weight but not infallible.** §2's instinct to demand primary evidence was right.
3. **That thread is where the PCN PDF URL came from.** The link Jason2866 pasted in 2024 is the link that let this document retrieve, validate and transcribe PCN-2021-021 in 2026 (§19.3) — after §11 had concluded no PDF existed. A community post recovered a primary source.

### 17.3 Tooling has historically misidentified this chip

`arduino-esp32` issue **#10683** (2024-12-04) **[COM]**: `ESP.getChipModel()` returned **`ESP32-PICO-D2`** for an ESP32-MINI-1 / U4WDH, while `esptool` on the same board correctly printed `Chip is ESP32-U4WDH (revision v3.1)`. The reporter traced it to a missing case in `cores/esp32/Esp.cpp`, even though `EFUSE_RD_CHIP_VER_PKG_ESP32U4WDH` had long been defined in ESP-IDF's `soc/esp32/include/soc/efuse_defs.h`. Fixed in PRs #10695/#10696 (2024-12-08).

**Practical consequence for anyone working on this board:** if your firmware branches on `ESP.getChipModel()` and you are on `arduino-esp32` **≤ 2.0.17**, it will lie to you about this chip. Prefer `esp_chip_info()` (§2.1 method B), which reads `cores` and `features` from eFuse directly and was never affected. `esptool` has always been correct.

### 17.4 What the community discusses — and what it doesn't

The catalogue is dominated by **hardware bring-up problems**, not software. Ranked by frequency: flash/VDD_SDIO voltage strapping, embedded-flash pin restrictions, crystal and reset-network mistakes, PSRAM attempts, then core count. There is almost no discussion of U4WDH-specific *software*, which makes sense — to ESP-IDF it is just `esp32`, and applications are portable across the whole series.

Two notable **absences**, both of which are themselves findings:

- **No thermal or RF-layout discussion specific to U4WDH was located.** No thread was found about the 85 °C ceiling (§13.3), which given how badly the distributors misreport it is a little alarming. RF layout guidance is generic ESP32 guidance (§18.6).
- **No teardowns.** No blog post, video, or teardown of a shipping product identified as containing a bare U4WDH was found.

### 17.5 A warning about AI-generated parts content

Several distributor-adjacent sites now publish long, confident, machine-generated technical prose about this part. `digi-electronics.com`'s U4WDH page is the clearest example encountered: it asserts *"–40°C to 105°C, aligning with industrial-grade requirements such as factory process automation, outdoor telemetrics, and automotive sensor nodes"* — contradicting the datasheet by 20 °C (§13.3) — and elsewhere claims the part supports *"both 5×5 mm and 6×6 mm footprints"*, which is false; U4WDH is QFN 5×5 only, and the 6×6 package belongs to the `Q6` parts (§13.1).

Its *parametric table* (mirrored from Digi-Key) is used in §16.2 and appears reliable. Its *prose* is not. Treat the two differently, and treat this as a general hazard when researching any part in 2026.

---

## 18. Designing with the bare chip

### 18.1 The six GPIOs consumed by the in-package flash

This is the defining constraint of the part, and the reason the pin table in §5 has so many "not connected" rows.

ESP32 Series Datasheet v5.3, **Table 2-5 "Pin-to-Pin Mapping Between Chip and In-Package Flash/PSRAM"**, transcribed verbatim **[DOC]**:

| ESP32-U4WDH pin | In-Package Flash (4 MB) signal |
|---|---|
| SD_DATA_1 | IO0 / DI |
| **GPIO17** | IO1 / DO |
| SD_DATA_0 | IO2 / WP# |
| SD_CMD | IO3 / HOLD# |
| SD_CLK | CLK |
| **GPIO16** | CS# |
| GND | VSS |
| VDD_SDIO | VDD |

Mapping the SD_* names to GPIO numbers, the six pins you lose are:

| Package signal | GPIO | Flash function |
|---|---:|---|
| SD_CLK | **GPIO6** | CLK |
| SD_DATA_0 | **GPIO7** | IO2 / WP# |
| SD_DATA_1 | **GPIO8** | IO0 / DI |
| SD_CMD | **GPIO11** | IO3 / HOLD# |
| GPIO16 | **GPIO16** | CS# |
| GPIO17 | **GPIO17** | IO1 / DO |

Datasheet §2.3.1 classifies these as *"GPIO — allocated for communication with in-package flash/PSRAM and NOT recommended for other uses"* **[DOC]**.

**Note what is *not* on that list: GPIO9 and GPIO10 (SD_DATA_2 / SD_DATA_3).** On a conventional ESP32 with *off-package* flash those two are consumed (datasheet Table 2-6 maps SD_DATA_3 → IO2/WP# and SD_DATA_2 → IO3/HOLD#), but U4WDH's in-package flash routes WP#/HOLD# to SD_DATA_0/SD_CMD instead. GPIO9 and GPIO10 are therefore *theoretically* free on this part in a way they are not on a WROOM module. Treat that as a lead to verify on silicon, not a licence — they remain in the SDIO power domain and are historically troublesome.

**The DIO/QIO subtlety.** Espressif staff member `igrr`, ESP32 Forum t=17065, 2020-08-24, verbatim **[COM]**:

> *"Since the default mode is 'DIO', you will not see any activity on D0 and CMD (which are WP and HOLD of Flash). If you switch flash mode to QIO in menuconfig, then these pins will also get used. Note that even if you configure the application to use DIO mode, D0 and CMD are still connected to the flash chip's WP and HOLD, which means that **you can't run arbitrary signals through those pins**."*

In other words: measuring the pins and seeing them idle does **not** mean they are free. They are physically bonded to the flash die. The original poster's hope — *"I was hoping it was more boilerplate than fact"* — is exactly the mistake to avoid.

**Knock-on effect: HS1/SPI2 is dead.** ESP32 staff member `LJH`, forum t=26037, 2022-02-10, verbatim **[COM]**:

> *"Yes, those pins could not be used to connect SD card, you could only use HS2: MTDI MTDO MTCK MTMS GPIO2 GPIO4."*

So on U4WDH: **no SD/MMC on the HS1 slot**, and no IO_MUX function-3 use of those pads. If you need an SD card, it goes on HS2 (MTDI/MTDO/MTCK/MTMS/GPIO2/GPIO4) — which collides with JTAG, so you cannot have both SD-on-HS2 and JTAG debugging simultaneously.

### 18.2 The external crystal is mandatory

Datasheet v5.3 Table 2-2 lists XTAL_P/XTAL_N (pins 44/45) as *"External clock input/output connected to chip's crystal or oscillator"* **[DOC]**, and the features list specifies *"only 40 MHz crystal supported when using Wi-Fi/Bluetooth"*.

There is no internal crystal and no way to run the radio without one. This catches migrants from the PICO SiP parts, which integrate it. ESP32 Forum t=25878 is a complete worked example of the failure **[COM]**: a designer moved from ESP32-PICO-D4 to U4WDH, omitted the crystal, and got a dead chip — *"nothing on serial on boot, and impossible to flash"*. The thread sat unanswered for **four years** before another user posted the answer in 2026: *"Yes the whole ESP32 series requires an external 40MHz crystal clock source, I learnt it the hard way as well."*

This board does it correctly: crystal `X2`, 10 pF load caps `C55`/`C56`, 0 Ω series `R51` (§1) **[SCH]**.

### 18.3 ⚠ The VDD_SDIO / MTDI trap — the top bring-up killer

**If you design one thing wrong on a U4WDH board, it will be this.**

The in-package flash is a **3.3 V** die. Datasheet v5.3, Table 2-5 note 1, verbatim **[DOC]**:

> *"As the in-package flash (ESP32-U4WDH) and the in-package PSRAM (ESP32-D0WDRH2-V3) operate at 3.3 V, VDD_SDIO must be powered by VDD3P3_RTC via a 6 Ω resistor."*

But **MTDI is a strapping pin that selects VDD_SDIO's voltage at reset**. Datasheet §3.2 **[DOC]**:

- **MTDI = 0 (default)** → VDD_SDIO powered from VDD3P3_RTC, typically 3.3 V. ✅ correct for U4WDH.
- **MTDI = 1** → VDD_SDIO powered from the internal **1.8 V** LDO. ❌ **the flash will not work.**

MTDI's default configuration is pull-**down** (Table 3-1) **[DOC]**, so a board that leaves it alone is fine. A board that pulls MTDI high — perfectly reasonable on a flash-less ESP32, and common in JTAG-adjacent designs — silently underpowers the embedded flash.

The symptom, from ESP32 Forum t=28486 **[COM]**, is *not* an obvious power fault. It is this:

~~~
Chip is ESP32-U4WDH (revision 3)          <- chip talks fine
Features: WiFi, BT, Dual Core, 240MHz, Embedded Flash
WARNING: Failed to communicate with the flash chip, read/write operations will fail.
Manufacturer: ff
Device: ffff
Detected flash size: Unknown
~~~

The chip enumerates perfectly and the flash reads as all-ones. The reporter diagnosed it himself and also surfaced the relevant datasheet distinction **[COM]**: minimum VDD_SDIO in 3.3 V mode is **3.0 V** for parts with 3.3 V embedded flash (U4WDH), versus **2.3 V** for D2WD's 1.8 V flash and for parts with no flash. Datasheet v5.3 Table 5-2 note 2 still carries this, phrased as the 2.3 V/3.0 V split **[DOC]**.

**Three fixes, in order of preference:**

1. **Pull MTDI low** (or just leave it — the internal pull-down is correct). Best; costs nothing.
2. **Burn the eFuses**, which overrides the strapping pin permanently. Suggested by Espressif staff `Sprite` in that thread — *"a third option is to burn an eFuse to fix the flash voltage, independent of the bootstrap pins"* — and confirmed working by the reporter with all three of `XPD_SDIO_FORCE`, `XPD_SDIO_REG`, `XPD_SDIO_TIEH` set to 1 **[COM]**. Note his finding that `XPD_SDIO_REG` must be set even though 3.3 V does not need the regulator. Datasheet §3.2 names these `EFUSE_SDIO_FORCE` / `EFUSE_SDIO_TIEH` **[DOC]**. **eFuses are one-way — you cannot undo this.**
3. **Wire VDD_SDIO to 3.3 V externally.** Works (the reporter tried it first), but wastes the internal path and a pin.

### 18.4 Reset network and power supply

From Espressif staff `Sprite`, forum t=31940, 2023-02-07, verbatim **[COM]**:

> *"You need a reset RC network for the ESP32 to function correctly. Add an 1uF capacitor between CHIP_PU and GND and together with R3 it should suffice as the RC network."*
>
> *"You're not trying to power the ESP32 off the CP2102, are you? If so, that chip can only provide a very small amount of current… You need some kind of LDO or other regulator capable of providing 3.3V at at least 600mA, as per the ESP32 datasheet."*

Corroborated by the datasheet: Table 5-2 specifies I_VDD, *"Current delivered by external power supply"*, minimum **0.5 A** **[DOC]**; and Table 2-1 warns *"Do not leave the CHIP_PU pin floating"* **[DOC]**. Do not size the rail off average current — the radio's TX bursts are what the 600 mA figure is protecting.

### 18.5 PSRAM: officially supported, practically painful

Contrary to what "the flash pins are all used up" suggests, Espressif's hardware FAQ does state that U4WDH supports external PSRAM — with restrictions, quoted by a user in forum t=45793 **[COM]**:

> *"The ESP32-U4WDH chip supports external PSRAM chips. However, only the ESP-PSRAMXXH chip released by Espressif is supported. Third-party PSRAM chips are not supported. For hardware design, all the PSRAM pins except for the CS pin can be multiplexed with Flash."*

In practice the 2025 attempt in that thread **failed**: the user could not source ESP-PSRAM parts, tried an LY68L6400, got a boot loop with CS shared and `id 0xffffffff` with CS on GPIO0, and received **no replies at all**. Treat external PSRAM on U4WDH as **high-risk and effectively unsupported in practice**, and if you need PSRAM choose a part that has it in the package (ESP32-D0WDRH2-V3, or an ESP32-WROVER-E module) instead.

On this board the question is moot — no PSRAM is fitted and there is no free SPI bus (§1) **[SCH]**.

### 18.6 Antenna, RF layout and the certification consequence

No U4WDH-specific RF guidance exists; the governing document is the **ESP Hardware Design Guidelines (ESP32)**, already in `artifacts/esp32-hardware-design-guidelines.pdf`, which covers RF trace impedance, the π-matching network, keep-out zones, and ground stitching generically for the series **[DOC]**. This board implements the standard pattern: π network `C46` 2.2 pF / `L5` 2 nH / `C45` 2.2 pF from `LNA_IN` into ceramic antenna `ANT2` (§1) **[SCH]**.

**The certification consequence is the thing most people underestimate, and it is the real reason to prefer a module.**

- An **ESP32-MINI-1 module** ships with FCC / CE / IC / SRRC modular approvals already granted. You inherit them. Your product's radio testing collapses to unintentional-radiator scope.
- A **bare ESP32-U4WDH** carries **no modular approval whatsoever**. The antenna, matching network and PCB stack-up are *yours*, so the radio is yours, and **your board needs its own full intentional-radiator certification** in every market you sell into.

That cost is typically thousands of dollars and weeks of lab time per market, and it is a **fixed** cost. This is precisely why bare-die integration only makes sense at volume: you are trading a large fixed certification cost against a small per-unit saving. Below some break-even volume the module is strictly cheaper. This is the trade-off Waveshare made on this board, and it is why U14 has its own antenna and its own π network rather than being a soldered-down module.

One useful data point on the other side: PCN-2021-021's single-to-dual-core change explicitly *did not* invalidate existing approvals — *"does not affect the RF performance of the modules and does not affect the validity of their existing RF certifications"* **[DOC]**. Silicon revisions of this part have not historically forced re-certification.

### 18.7 Strapping pins, and one IDF bug

Datasheet v5.3 Table 3-1, default configuration of the five strapping pins **[DOC]**:

| Strapping Pin | Default | Bit Value | Also controls |
|---|---|---:|---|
| **GPIO0** | Pull-up | 1 | Boot mode (with GPIO2) |
| **GPIO2** | Pull-down | 0 | Boot mode (with GPIO0) |
| **MTDI** | Pull-down | 0 | **VDD_SDIO voltage — see §18.3** |
| **MTDO** | Pull-up | 1 | U0TXD boot-log printing; SDIO slave timing |
| **GPIO5** | Pull-up | 1 | SDIO slave timing |

Boot mode (Table 3-3): **GPIO0 = 0 and GPIO2 = 0 → Joint Download Boot Mode** (i.e. flashing); GPIO0 = 1 → SPI Boot Mode **[DOC]**. Setup time t_SU ≥ 0 ms before CHIP_PU rises; hold time t_H ≥ 1 ms after **[DOC]**. All strapping pins are latched at reset and are free for general I/O afterwards.

Note MTDO's second job: pulling it **low** at boot **disables the U0TXD boot log** — a useful production trick, and an easy way to accidentally lose your only debug output.

**The QIO bug.** ESP-IDF issue **#6191** **[COM]**, confirmed by Espressif's `projectgus` (2021-04-12): with `CONFIG_BOOTLOADER_SPI_CUSTOM_WP_PIN=n` — the default, which is supposed to auto-select the correct WP pin for any Espressif chip with integrated flash — **automatic WP-pin selection fails on U4WDH**, and QIO flash mode does not work; the bootloader dies checking the partition table.

> *"You're totally right, the automatic WP pin selection fails in this case and quad flash modes don't work automatically. As you probably already know, a manual workaround is to enable `CONFIG_BOOTLOADER_SPI_CUSTOM_WP_PIN` and keep the default choice (7), and it works."*

If you want QIO on this chip (roughly 2× flash read throughput over DIO), **explicitly enable `CONFIG_BOOTLOADER_SPI_CUSTOM_WP_PIN` and leave the pin at 7**. Reported against IDF v4.2-rc and fixed later; if you are on a modern IDF this may no longer bite, but verify rather than assume. This board's factory firmware runs the flash at 40 MHz (§1) **[FW]**; flash *mode* was not determined.

---

## 19. Alternatives

### 19.1 ⚠ Classic Bluetooth is the axis that matters

Everything in this section is dominated by one fact: **Bluetooth Classic (BR/EDR) exists only on the original ESP32 die.** Espressif has not shipped it on any newer part. Confirmed by Espressif staff `Sprite`, ESP32 Forum t=23059, 2021-09-11, verbatim **[COM]**:

> *"BR/EDR is Bluetooth Classic, right? If so, no; the S3 only supports BLE."*

| Part | Classic BT (BR/EDR)? | BLE? | Notes |
|---|---|---|---|
| **ESP32** (all variants incl. U4WDH) | ✅ **Yes** — v4.2 BR/EDR | ✅ | **The only family with it** |
| ESP32-S2 | ❌ | ❌ | No Bluetooth at all |
| ESP32-S3 | ❌ | ✅ BLE 5.0 | The chip on this board that *needed* a companion |
| ESP32-C3 / C2 / C6 / C5 / C61 | ❌ | ✅ | RISC-V; C6 adds 802.15.4 |
| ESP32-H2 / H4 / H21 | ❌ | ✅ | Thread/Zigbee focus; H2 has no Wi-Fi |
| ESP32-P4 | ❌ | ❌ | **No radio at all** — needs a companion for any wireless |

**If your design needs A2DP, AVRCP, HFP, SPP or any other BR/EDR profile — as this board does — every "newer, better" Espressif part is disqualified.** That is not a limitation of U4WDH; it is the reason U4WDH is still in production in 2026 and is one of only two non-NRND bare ESP32 chips (§13.2).

### 19.2 Replacement options, ranked by what you are optimising for

**A. Same die, same capability, less integration risk — modules that retain Classic BT:**

| Module | Core chip | Flash | Why choose it |
|---|---|---|---|
| **ESP32-MINI-1 / MINI-1U** | **ESP32-U4WDH** | 4 MB in-package | **The drop-in module form of this exact chip** (§15.1). Identical silicon, identical software, but you inherit the RF certification and the crystal. `-1U` has an external antenna connector. **This is the default recommendation for anyone who does not need to shave the last few mm²** |
| ESP32-WROOM-32E / 32UE | ESP32-D0WD-V3 | 4/8/16 MB external | The workhorse. Bigger, more flash options, cheapest per unit at low volume, most widely certified. `UE` = external antenna |
| ESP32-WROVER-E / IE | ESP32-D0WD-V3 | 4–16 MB + **8 MB PSRAM** | When you need PSRAM and Classic BT together — the answer to §18.5 |
| ESP32-SOLO-1 | single-core ESP32 | 4 MB | Cheapest; single-core. Note this is the part genuinely confused with U4WDH (§17.2) |
| ESP32-PICO-MINI-02 | ESP32-PICO-V3-02 | 8 MB + 2 MB PSRAM | Smallest module with PSRAM |

**B. Same capability, still a bare chip:**

| Chip | Trade vs U4WDH |
|---|---|
| **ESP32-D0WD-V3** | The only other Active bare ESP32. **No in-package flash** — you add a SPI NOR and route six nets, but you regain GPIO6/7/8/11/16/17, get 1.8 V *or* 3.3 V VDD_SDIO flexibility, choose your own flash size, and **regain 40 °C of operating range** (−40 to 125 °C, §13.3). Cheaper per chip ($1.59 vs ~$2.09–2.93, §16.2) |
| ESP32-D0WDRH2-V3 | Successor to the EOL D0WDR2-V3. **2 MB in-package PSRAM**, no in-package flash. Same 85 °C ceiling as U4WDH |
| ESP32-PICO-V3-02 | SiP with crystal + flash + PSRAM. Smallest total area, no external crystal, but LGA and hard to hand-assemble (§13.4) |

**C. If — and only if — you can drop Classic Bluetooth:** ESP32-C3 is the cheap modern BLE+Wi-Fi replacement; ESP32-C6 adds Wi-Fi 6, Thread and Zigbee; ESP32-S3 adds performance, USB-OTG and AI acceleration. All are better parts than U4WDH in nearly every respect **except the one that matters here**. Re-read §19.1 before going down this road: on this board the U4WDH exists *precisely because* the S3 could not do BR/EDR.

### 19.3 Documents recovered that §11 records as non-existent

Two corrections to §11, both material:

**1. PCN-2021-021 has a PDF.** §11 and §2 state it is HTML-only. It is not: a PDF exists on the legacy `pcn_downloads` path, discovered via a community link in `arduino-esp32` issue #9252 (§17.2). Retrieved 2026-08-21, `%PDF-1.7` magic and `%%EOF` trailer both validated, **782,406 bytes**, stored as `artifacts/pcn-2021-021-esp32-u4wdh-dual-core.pdf`. Its full text is transcribed in §14.

*Extraction note for whoever comes next:* this PDF's text layer uses a **glyph-subset substitution in which every character is offset by −29 from its true code point**. Adding 29 to each extracted byte recovers plain ASCII, digits included. This is the same class of obstruction that defeated §1.1 on the datasheet — but note the datasheet PDF uses a *different, non-uniform* mapping that this trick does **not** solve. For the datasheet, use the HTML build instead (§13, `artifacts/esp32-series-datasheet-v5.3.html`).

**2. A standalone chip-revision user guide exists.** §11 states *"There is likewise no standalone 'ECO V3 / chip revision v3 user guide' PDF."* There is: **ESP32 Chip Revision v3.0 User Guide**, v1.3, dated 2022.11. Retrieved 2026-08-21, validated, **350,173 bytes**, stored as `artifacts/esp32-chip-revision-v3-0-user-guide.pdf`. Its text layer *is* plain and extracts without tricks. It covers the design changes in revision v3.0 (flash-startup watchdog fix, PSRAM cache bug fix, 32.768 kHz oscillator stability, fault-injection protection, RSA secure boot), and two migration "use cases" for customers moving to v3.0 silicon. Since U4WDH is v3.0/v3.1 only (§13.2), **this document applies to your chip in full**.

### 19.4 Retrieval notes — mirrors and blocks

Recorded so that re-acquisition is cheap. All checked 2026-08-21.

| Document | Primary URL | Working mirrors / alternates |
|---|---|---|
| PCN-2021-021 (**PDF**) | `https://www.espressif.com/sites/default/files/pcn_downloads/PCN-2021-021%20ESP32-U4WDH%20%E5%8D%87%E7%BA%A7%E4%B8%BA%E5%8F%8C%E6%A0%B8%E5%A4%84%E7%90%86%E5%99%A8%E4%BA%A7%E5%93%81.pdf` | HTML form: `https://documentation.espressif.com/en/PCN-2021-021%20…%E4%BA%A7%E5%93%81.html`; PCN index: `https://espressif.com/en/support/documents/pcns`; part-filtered: `https://www.espressif.com/en/taxonomy/term/871` |
| ESP32 Series Datasheet | `https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf` | **`https://documentation.espressif.com/esp32_datasheet_en.pdf`** (byte-identical, 989,523 B — this is the redirect target); **`https://documentation.espressif.com/esp32_datasheet_en.html` ← the extractable HTML build, strongly preferred**; third-party mirrors: `https://cdn.sparkfun.com/assets/e/b/6/b/0/esp32_datasheet_en-1223853.pdf`, `https://components101.com/sites/default/files/component_datasheet/ESP32-Datasheet.pdf` |
| ESP32-MINI-1 / 1U Datasheet | `https://documentation.espressif.com/esp32-mini-1_datasheet_en.pdf` | HTML: `https://documentation.espressif.com/esp32-mini-1_datasheet_en.html`; legacy: `https://espressif.com/sites/default/files/documentation/esp32-mini-1_datasheet_en.pdf`. **Note the slug is `esp32-mini-1_…`, *not* `esp32-mini-1_mini-1u_…`** — the latter soft-404s |
| ESP32 Chip Revision v3.0 User Guide | `https://documentation.espressif.com/esp32_chip_revision_v3_0_user_guide_en.pdf` | — |
| ESP Hardware Design Guidelines | esp-docs PDF (see §11) | `https://www.lcdwiki.com/res/PublicFile/esp32_hardware_design_guidelines_en.pdf` |

**Wayback captures made 2026-08-21**, so these survive if Espressif reorganises again:

- PCN-2021-021 PDF → `https://web.archive.org/web/20260823001902/https://documentation.espressif.com/PCN-2021-021%20ESP32-U4WDH%20%e5%8d%87%e7%ba%a7%e4%b8%ba%e5%8f%8c%e6%a0%b8%e5%a4%84%e7%90%86%e5%99%a8%e4%ba%a7%e5%93%81.pdf` *(note: the save request was made against the legacy `espressif.com/sites/default/files/pcn_downloads/…` URL and the Wayback machine followed the redirect, so the capture is filed under the `documentation.espressif.com` name)*
- ESP32 Chip Revision v3.0 User Guide → `https://web.archive.org/web/20260616101319/https://documentation.espressif.com/esp32_chip_revision_v3_0_user_guide_en.pdf` *(pre-existing capture, 2026-06-16)*

**Soft-404 fingerprint** for `documentation.espressif.com`, re-confirmed 2026-08-21: HTTP **200**, `text/html`, exactly **13,745 bytes**. Matches the value recorded in the [Espressif vendor guide](../../../vendors/espressif/README.md). Slugs that produced it: `esp32_chip_packaging_information_en`, `esp32_packaging_information_en`, `esp32-mini-1_esp32-mini-1u_datasheet_en`, `esp32-devkitm-1`. **Always test the magic bytes, never the status code.**

**Not retrievable:** the **ESP32 Chip Packaging Information** document (referenced by datasheet §6 as the authority for tape, reel and chip marking) could not be located under any slug tried. This is a real gap — it is the document that would show the *full* marking layout that PCN-2021-021's line-5 rule (§14.2) sits inside.

**Crawler blocks encountered** (relevant to `ai-crawler-site-access-table.md`):

| Site | Chrome UA | WhatsApp UA | ChatGPT-User / ClaudeBot UA | Workaround used |
|---|---|---|---|---|
| `lcsc.com` | ✅ 200 | — | — | Direct; price ladder is in embedded JSON (`productPriceList`) |
| `mouser.com` | ❌ 403 bot-wall | ❌ 403 | ❌ connection reset | None found |
| `digikey.com` / `.ca` | ❌ 403 | ❌ 403 | ❌ 403 | `digi-electronics.com` catalogue mirror (parametrics reliable, prose is AI slop — §17.5) |
| `octopart.com`, `findchips.com`, `trustedparts.com` | ❌ 403 | — | — | None found |
| `esp32.com`, `github.com`, `documentation.espressif.com` | ✅ 200 | — | — | Direct. GitHub issue bodies are far cleaner via `api.github.com` than via HTML |

---

## 20. The companion-MCU pattern: is a second Classic-BT ESP32 alongside an ESP32-S3 normal?

This section answers a question posed about *this board's architecture* rather than about the chip. It is kept deliberately hedged, because **the evidence is thin and the honest answer is a qualified one.**

### 20.1 The short answer

**The pattern is well-known and explicitly recommended in discussion, but no evidence was found that it is common in shipping products. On current evidence this board is an unusual — not unheard-of — instance.**

To be explicit about the epistemic status: this is a **negative result from web search**, which is weak evidence. Bare chips inside sealed consumer products are invisible without teardowns, and no relevant teardowns were located. Absence of found evidence is not evidence of absence. What *can* be said with confidence is stated below; what cannot, is flagged as such.

### 20.2 What the evidence does support

**The pattern is proposed, by name, as the standard workaround. [COM]**

ESP32 Forum thread **t=23059** is the only substantive discussion located. On 2021-09-11 a commercial developer (Rivers, of Dearlight Corporation, Thailand) confirmed with Espressif staff that the S3 has no BR/EDR and lamented that this forced him back to *"an old solution ESP32 + Audio DSP which are significantly higher cost."* Community member `chegewara` (2,500+ posts) replied, verbatim:

> *"You can always use S3 + old esp32, which is not that much expensive."*

and elaborated, suggesting the single-core ESP32-SOLO *"(and maybe embedded flash)"* — i.e. **exactly the class of part U14 is** — and noting *"espressif is providing AT command firmware to control bluetooth"* as the inter-chip control mechanism.

**But the commercial designer rejected it as unsuitable for a product. [COM]** His reply, verbatim:

> *"Thanks for your idea. Yes that's probably a workaround for hobbyist. But you will end up with 4 cores MCU @ 160MHz along with 2 SPI Flash memories draining lot of power, let alone managing 2 OS through OTA update. In commercial application only single core Cortex M7 @ 480MHz with DSP instructions combine with Murata WiFi + dual-mode BLE chip and 1 SPI Flash could do the same job…"*

That is a designer with a shipping product to build, considering the exact architecture this board uses, and turning it down. His three objections — **power, dual-firmware OTA complexity, and silicon redundancy** — are precisely the costs Waveshare accepted here.

**Espressif *does* bless the general shape of the idea. [DOC]/[WEB]**

`espressif/esp-hosted` is an official, actively maintained framework in which *"Espressif SoCs/modules (like ESP32) act as wireless communication co-processors for external host systems"*, connected over *"SPI, SDIO, or UART"*, exposing *"Bluetooth via standard HCI"* — and its capability matrix explicitly lists **"Classic Bluetooth support: All Variants"**. Espressif also ships **ESP-AT**, an AT-command firmware for exactly this role (the mechanism `chegewara` referenced).

So "an ESP32 acting as a radio co-processor for another MCU" is a first-class, supported architecture. Two important caveats before reading that as support for this board:

1. ESP-Hosted's usual framing is **Linux hosts or third-party MCUs** gaining Wi-Fi/BT — not one Espressif SoC hosting another to backfill a missing radio mode.
2. **This board does not use ESP-Hosted or ESP-AT.** The link between the S3 and U14 is a **bespoke UART protocol** whose framing this document has been unable to determine (§6.3, §12 question 2). It is an ad-hoc private link, not a standard one. Had Waveshare used ESP-Hosted or ESP-AT, §6 would have been a five-line section.

**A closely analogous pattern *is* genuinely mainstream — for a different chip. [DOC]** ESP32-P4 has no radio at all, and the standard, Espressif-endorsed answer is to pair it with an ESP32-C6 over SDIO running ESP-Hosted. Multiple P4 dev boards ship this way. This proves Espressif-SoC-hosts-Espressif-SoC is a real, normal, productised pattern — but it is driven by *"the host has no radio"*, not by *"the host's radio is missing one mode"*, and it does not by itself establish that the S3 + Classic-BT-ESP32 variant is common.

### 20.3 What was searched, and found nothing

For transparency about the negative result. No hits, across Mojeek, Bing and GitHub issue/code search, for:

- Other **named shipping boards** pairing an ESP32-S3 with a second ESP32 for Classic Bluetooth
- Teardowns or blog posts describing such a dual-MCU S3 board
- Any GitHub project implementing an S3 ↔ ESP32 Classic-BT bridge as a reusable component
- Any Waveshare or third-party documentation describing this as a product-line design pattern

The one artefact that comes closest — the only place the idea is discussed at all — is thread t=23059 above, where it is proposed and then rejected as hobbyist-grade.

### 20.4 Conclusion, with confidence levels

| Claim | Confidence |
|---|---|
| Pairing an S3 with a Classic-BT-capable ESP32 is a **known and recommended workaround** for the S3's missing BR/EDR | **High** — directly attested **[COM]** |
| An Espressif SoC acting as a **radio co-processor** for another MCU is a legitimate, officially supported architecture | **High** — ESP-Hosted, ESP-AT **[DOC]** |
| That architecture is **mainstream for ESP32-P4 + ESP32-C6** | **High** **[DOC]/[WEB]** |
| The specific **S3 + Classic-BT-ESP32** combination is **common in shipping products** | **Low — no supporting evidence found.** Do not assert this |
| At least one experienced commercial designer **evaluated and rejected** it for a product | **High** — directly attested **[COM]** |
| This board's use of a **bespoke UART link** rather than ESP-Hosted/ESP-AT is unusual | **Medium** — no counter-example found, but this was not exhaustively searched |

**Practical takeaway.** Treat this board's dual-MCU architecture as a **deliberate, defensible, but uncommon** solution to a specific product requirement — a Bluetooth-audio knob whose main MCU cannot do Bluetooth audio. Do not expect to find a community of other boards doing the same thing, reusable libraries for the S3↔ESP32 link, or Waveshare documentation treating it as a platform. Section 6's warning stands: **you are on your own with that UART protocol.**

---

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)
  - [Dual-MCU architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md#dual-mcu-architecture)
  - [Classic Bluetooth guide](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/classic-bluetooth.md)
  - [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)
  - [Development and examples](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/development.md)
  - [Factory firmware and restore](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/factory-firmware.md)
  - [Gaps and conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md)

## Related components

| Component | Relationship to this chip |
|---|---|
| [Espressif ESP32-S3R8](../esp32-s3r8/README.md) | The main MCU. Peer over UART1; owns the CH445P mux select. **Has no Bluetooth Classic** — the reason U14 exists |
| [Texas Instruments PCM5100A](../../texas-instruments/pcm5100a/README.md) | The DAC this chip feeds over I2S and mutes over GPIO32 |
| [WCH CH445P](../../wch/ch445p/README.md) | The 4x 2:1 analog switch that arbitrates I2S between the two MCUs |
| [SGMicro SGM2036-3.3](../../sgmicro/sgm2036-3.3/README.md) | Supplies `3V3_DAC`, which powers both the PCM5100A and the CH445P |
| [Alps Alpine SSCM110100](../../alps-alpine/sscm110100/README.md) | `SW1`, the second knob read by this chip on GPIO19/22 |
| [USB-UART bridge (unidentified)](../../wch/ch340x/README.md) | `U10`, this chip's only path to a host PC |
| [USB-C target-selection interface](../../generic/usb-c-interface/README.md) | The orientation quirk that decides whether you are talking to this chip or the S3 |
| [2.4 GHz ceramic antennas (unidentified)](../../generic/ceramic-antenna/README.md) | `ANT2`, this chip's dedicated antenna |

### Framework guides

Distilled from the ESP-IDF and ESP-ADF PDFs formerly held in `artifacts/` (see [ARCHIVED-FRAMEWORK-GUIDES.md](artifacts/ARCHIVED-FRAMEWORK-GUIDES.md)):

- [ESP-ADF audio pipelines](../../../guides/espressif/esp-adf-audio-pipelines.md) — the Element/Pipeline architecture, the HFP/A2DP/AVRCP `bluetooth_service` API, and the **audio memory budget** that constrains this chip's Classic-BT audio path.
- [ESP-IDF peripheral capabilities](../../../guides/espressif/esp-idf-peripheral-capabilities.md) — **ESP32** vs ESP32-S3 vs ESP32-P4, including the LEDC high-speed group unique to this chip, the SDMMC `HS1_*`/SPI-flash pin conflict, and the [ESP32 PSRAM 1.8 V/MTDI hazard](../../../guides/espressif/esp-idf-peripheral-capabilities.md#41-esp32--the-18-v-trap-can-destroy-hardware).
| [3.5 mm stereo line output](../../generic/3.5mm-audio-output/README.md) | Where the audio ends up |
| [PH1.27 expansion connectors](../../generic/ph1.27-expansion-connectors/README.md) | `CN1`, which carries this chip's USB pair and the S3's mux-select line |
| [Espressif vendor sourcing guide](../../../vendors/espressif/README.md) | How to obtain any further Espressif document |

---

## 21. Silicon revisions: the complete matrix, and what v3.1 means

**Your chip reports `v3.1`.** This section establishes what that is, what it is not, and what it lets you do. It supersedes every loose reference to "ECO V3" elsewhere in this document.

The short version, stated up front because it is the single most useful fact here:

> **v3.1 is a minor revision of v3.0. It is functionally identical to v3.0 as far as software is concerned. Every erratum that applies to v3.0 applies identically to v3.1; every fix present in v3.0 is present in v3.1. The change was a wafer-level tweak for high-temperature stability, plus a new eFuse minor-version code and a new marking letter. No software change is required, permitted or implied.** **[DOC]** — Espressif **PCN20220901** §5 states the change comparison explicitly and records "Quality & Performance: No impact" and "Changed products listed in Para 1 are compatible with the current version of ESP-IDF."

### 21.1 Two naming schemes, and why you see both

Espressif shipped ESP32 silicon under an **ECO** ("Engineering Change Order") scheme for the first six years, then replaced it in September 2022 with a **major.minor `vM.X`** scheme. Both names are still in circulation — the ECO names survive inside ESP-IDF's own Kconfig menu labels to this day.

The scheme itself is documented in **AR2022-005, "Compatibility Advisory for Chip Revision Numbering Scheme"**, issued 2022-09-29 **[DOC]**:

| Field | Meaning **[DOC]** |
|---|---|
| **M** — major | *Breaking.* "If this number changes, it means the software used for the previous version of the product is incompatible with the new product, and the software version shall be upgraded for the use of the new product." |
| **X** — minor | *Non-breaking.* "If this number changes, it means the software used for the previous version of the product is compatible with the new product, and there is no need to upgrade the software." |

> "The vM.X scheme replaces previously used chip revision schemes, including ECOx numbers, Vxxx, and other formats if any." — AR2022-005 **[DOC]**

AR2022-005's own mapping table is *incomplete* — it was published one month before v1.1 and v3.1 were announced, and lists only three ESP32 rows. The **authoritative complete mapping** for the old ECO names is ESP-IDF's `components/esp_hw_support/port/esp32/Kconfig.hw_support`, whose menu entries name both schemes side by side **[DOC]**:

| `vM.X` | Old ECO name | Old ESP-IDF log identification | `CONFIG_ESP32_REV_MIN_FULL` | Kconfig symbol |
|---|---|---:|---:|---|
| **v0.0** | ECO0 (also "V0") | `0` | `0` | `ESP32_REV_MIN_0` |
| **v1.0** | ECO1 (also "ECO", "V1") | `1` | `100` | `ESP32_REV_MIN_1` |
| **v1.1** | ECO1.1 | *(not representable)* | `101` | `ESP32_REV_MIN_1_1` |
| **v2.0** | ECO2 | `2` | `200` | `ESP32_REV_MIN_2` |
| **v3.0** | ECO3 (also "ECO V3", "V3") | `3` | `300` | `ESP32_REV_MIN_3` |
| **v3.1** | **ECO4** | *(not representable)* | **`301`** | **`ESP32_REV_MIN_3_1`** |

Two consequences of that table that catch people out:

1. **"ECO3" and "v3.0" are the same thing.** Espressif's own *ESP32 Chip Revision v3.0 User Guide* was originally titled with "ECO" and was renamed in version 1.2 (2022.10) — its revision history records *"Replaced 'ECO' with 'Chip Revision'"* and *"Renamed this document as 'ESP32 Chip Revision v3.0 User Guide'"* **[DOC]**. When a forum post from 2019 says "ECO V3", it means v3.0.
2. **"ECO4" and "v3.1" are the same thing** — and this is the *only* place Espressif publishes that equivalence, in a Kconfig prompt string. It is easy to read "ECO4" and assume a fourth major generation with new features. It is not. It is the minor bump described in §21.4. **[DOC]** on the equivalence; the "easy to misread" part is **[INF]**.

**⚠ The v2.0 / ECO2 anomaly.** v2.0 is in ESP-IDF's Kconfig and in esptool's eFuse decode table (`combine_value == 3` maps to major `2`), but it appears in **no** Espressif-published document consulted here: not in the ESP32 Series SoC Errata (which jumps v1.1 → v3.0), not in AR2022-005's mapping table, and not in the datasheet's series comparison table (which lists only `v1.0/v1.1` and `v3.0/v3.1` parts). The most likely explanation is that ECO2 was an internal or never-broadly-released stepping. **[INF] — treat v2.0 as a decodable-but-not-shipping revision. Do not design around it, and do not be alarmed that the errata document skips it.** If you actually hold a chip that decodes as v2.0, that is worth reporting upstream.

### 21.2 The complete revision matrix

Consolidated from the ESP32 Series SoC Errata v3.0 (2025-10-11), the ESP32 Chip Revision v3.0 User Guide v1.3, PCN20220901, and the ESP32 Series Datasheet v5.3. **[DOC]** throughout unless marked.

| Revision | ECO name | Chip marking (tracking line) | Module marking (spec-ID line) | What it changed | Shipping status |
|---|---|---|---|---|---|
| **v0.0** | ECO0 | `XXXXXXXX` (no letter) | `XXXXXX` ¹ | Original silicon. Brown-out reset broken, spurious watchdog resets, CPU crash on direct 240→80/160 MHz clock switch, audio PLL range limited, repeated-address peripheral writes lost | Long obsolete |
| **v1.0** | ECO1 | `X B XXXXXX` | `XXXXXX` | Fixed BOR, the spurious WDT reset, the clock-switch crash, the audio-PLL range and the lost peripheral writes. **Introduced** the external-SRAM (PSRAM) sequence bug `CPU-3.9` | NRND parts (`ESP32-D0WD`, `ESP32-S0WD`, `ESP32-D0WDQ6`) |
| **v1.1** | ECO1.1 | `X F XXXXXX` | `MF XXXX` | **Minor** bump of v1.0. Announced in the same PCN20220901 as v3.1; same "no software change" character. Errata set identical to v1.0 | Current, for the surviving v1.x parts |
| **v2.0** | ECO2 | *not published* | *not published* | *not published* — see the anomaly note in §21.1 | **[INF]** none |
| **v3.0** | ECO3 | `X E XXXXXX` | `ME XXXX` | **The big one.** Seven design changes — see §21.3. Fixed the PSRAM cache bug, the flash-start-up watchdog reset and the dual-CPU simultaneous-read error; hardened against fault injection; enabled Secure Boot V2 and `UART_DOWNLOAD_DIS`. **Introduced** `WDT-3.15`, the dual-core cache live-lock | Superseded by v3.1 from 2023-01 |
| **v3.1** | **ECO4** | **`X G XXXXXX`** | **`MG XXXX`** | **Minor** bump of v3.0. Wafer-level change for high-temperature stability; new minor eFuse code; new marking letter. **Errata set byte-for-byte identical to v3.0** | **Current. This is your chip** |

¹ The errata's module-marking table notes that v0.0 and v0.1 cannot be told apart from the marking and require the eFuse bits. (No v0.1 appears anywhere else; noted for completeness.)

**What ESP32-U4WDH specifically ships as.** Datasheet v5.3 Table 1-1 lists `ESP32-U4WDH — Dual core — v3.0/v3.1 — 4 MB flash — QFN 5*5 — 3.3 V`, with footnote 4: *"The chips will be produced with chip revision v3.1 inside. See PCN20220901 for details."* **[DOC]** So **U4WDH has never existed below v3.0**, and current production is v3.1. This is why §19.3's claim that the v3.0 user guide "applies to your chip in full" is correct, and it is also why the PSRAM cache workaround discussion in §18.5 is moot for this part.

### 21.3 v3.0 in detail — the seven design changes

Transcribed from **ESP32 Chip Revision v3.0 User Guide, v1.3 (2022.11), Chapter 1** **[DOC]**. This is the change set that makes a v3.x chip meaningfully better than a v1.x chip.

| # | Change | Corresponding erratum |
|---|---|---|
| 1 | Fixed *"Due to the flash start-up time, a spurious watchdog reset occurs when ESP32 is powered up or wakes up from Deep-sleep"* | `RES-3.8` |
| 2 | **PSRAM Cache Bug Fix** — fixed *"When the CPU accesses the external SRAM in a certain sequence, read & write errors can occur"* | `CPU-3.9` |
| 3 | Fixed *"When each CPU reads certain different address spaces simultaneously, a read error can occur"* | `CPU-3.10` |
| 4 | Optimised **32.768 kHz crystal oscillator stability**. The guide records the field report: on v1.0 hardware there was a low probability the 32.768 kHz crystal would not start properly | — |
| 5 | **Fixed fault-injection issues regarding secure boot and flash encryption.** References CVE-2019-17391 (fault injection and eFuse protections) and CVE-2019-15894 (fault injection and secure boot) | — |
| 6 | TWAI (CAN) minimum baud rate lowered from **25 kbit/s to 12.5 kbit/s** — corroborated by datasheet v5.3's TWAI feature list, which states 25 kbit/s–1 Mbit/s for v0.0/v1.0/v1.1 and 12.5 kbit/s–1 Mbit/s for v3.0/v3.1 | — |
| 7 | **`UART_DOWNLOAD_DIS` eFuse** — Download Boot mode can be permanently disabled. Written via bit 27 of `EFUSE_BLK0_WDATA0_REG`, read via bit 27 of `EFUSE_BLK0_RDATA0_REG`. Write-disable for this bit is shared with write-disable for `flash_crypt_cnt`. Datasheet v5.3 §3.1 confirms: *"It permanently disables Download Boot mode when `uart_download_dis` is set to 1 (valid only for ESP32 chip revisions v3.0 and higher)"* | — |

The guide's §2.1 also states the software consequence directly: a project moving to v3.0 *"can benefit from protection against fault injection attack and can also take advantage of newer secure boot mechanism and PSRAM cache bug fix with slightly enhanced PSRAM performance"*, and recommends **RSA-based secure boot (Secure Boot V2) from ESP-IDF v4.1 and later** **[DOC]**.

Its §2.2 is equally worth knowing if you ever mix stock: *"The same application binary will work on both chip revision v1.0 and chip revision v3.0."* **[DOC]** A v1.0-minimum build runs on v3.1 silicon. The reverse does not hold.

**⚠ One thing v3.0 did *not* fix, and one thing it introduced.**

- **Did not fix:** the fault-injection hardening of item 5 does **not** make v3.x immune to side-channel attack. **AR2022-003, "Security Advisory Concerning Breaking the Hardware AES Core and Firmware Encryption of ESP32 Chip Revision v3.0"** (V2.0, 2022-11-18) documents two vulnerabilities found by Ledger Donjon in **v3.0 specifically**: the hardware AES core and the Flash Encryption feature are both extractable by Side Channel Attack (CPA on power traces), and the AES core is additionally extractable by Body Biasing Injection. Espressif's stated position is that there is **no hardware fix**; countermeasures are per-device unique keys, physical tamper resistance, and enabling Flash Encryption and Secure Boot together. **[DOC]** Since the advisory targets v3.0 and v3.1 is functionally identical to v3.0, **assume it applies to your chip.** **[INF]** on that last inference — but it is a safe one, and Espressif has published nothing suggesting v3.1 changed the AES core.
  - One mitigation in that advisory is *directly relevant to this part*: Espressif notes that **SiP packages with flash pins terminated internally protect better**, because they prevent use of an external flash emulator or monitoring of the flash pins. **ESP32-U4WDH is exactly such a package** — its 4 MB flash is in-package and its six SPI pins are not board-accessible (§18.1). **[DOC]** on the mitigation principle; **[INF]** on applying it to U4WDH, since the advisory names ESP32-PICO-V3 as its example rather than U4WDH.
- **Introduced:** `WDT-3.15`, a dual-core cache live-lock affecting **only v3.0 and v3.1**. See §21.4.

### 21.4 v3.1 specifically — what actually changed

**This is the question the whole section exists to answer, so here is the evidence chain in full.**

The change is announced in **PCN20220901, "Upgrade Chip Revision of ESP32 Series Products"** (document ESP-07-2-007-03 v1.4, PCN issued 2022-10-25, change effective 2022-12-25, first shipment after change 2023-01-25, related ECNs ECN-2022-005 / -015 / -036). ESP32-U4WDH is named explicitly in Appendix I, Category 2. **[DOC]**

**Stated reason for change, verbatim:**

> "To broaden the product application realm and ensure stable operating under more complicated and high temperature circumstances, the chip revision of ESP32 series of chips will be upgraded. The series resistance of the crystal on the ESP32 high temperature version (–40 ℃ ~ 105 ℃) modules will also be changed."

**Stated description of change, verbatim:**

> "Upgrade the chip revision v1.0 on the ESP32 series products to v1.1, and chip revision v3.0 to v3.1. Change the crystal's series resistance on the ESP32 high temperature version (–40 ℃ ~ 105 ℃) modules from 0 Ω to 100 Ω."

**The Category 2 change-comparison table, transcribed in full** (Appendix I §2) **[DOC]**:

| # | Item | Before change | After change |
|---|---|---|---|
| 1 | Chip Revision | v3.0 | **v3.1** |
| 2 | eFuse `EFUSE_BLK0_RDATA5[25]` | 0 | 0 |
| 2 | eFuse **`EFUSE_BLK0_RDATA5[24]`** | **0** | **1** |
| 2 | eFuse `APB_CTRL_DATA[31]` | 1 | 1 |
| 2 | eFuse `EFUSE_BLK0_RDATA5[20]` | 1 | 1 |
| 2 | eFuse `EFUSE_BLK0_RDATA3[15]` | 1 | 1 |
| 3 | Chip marking (main die line) | `xExxxxxx` | **`xGxxxxxx`** |
| 4 | Module MPN | *No change* | *No change* |
| 5 | Module marking (specification line) | `XXXXXX` | **`MGXXXX`** |
| 6 | Crystal series resistance on –40 ℃ ~ 105 ℃ modules | 0 Ω | 100 Ω |

**Stated impact, verbatim** (PCN §5) **[DOC]**:

- "Quality & Performance: No impact"
- "Delivery: No impact"
- "Material Part Numbers (MPN): Customers can continue using the existing product name to place orders."
- "Certification: No impact"
- "Software / IDF: Changed products listed in Para 1 are compatible with the current version of ESP-IDF. Customers can still use the current version for the changed products."

**So, precisely:**

| Question | Answer | Confidence |
|---|---|---|
| Is v3.1 a functional change relative to v3.0? | **No.** Exactly one bit of the change table is a silicon-observable difference (`RDATA5[24]`, the minor-version code); everything else is marking or a module-level passive value. The *reason* is a wafer-level process improvement for high-temperature stability | **High — [DOC]**, PCN §3 and Appendix I §2 |
| Does any erratum apply to v3.0 but not v3.1, or vice versa? | **No.** The v3.0 and v3.1 columns of the ESP32 Series SoC Errata summary table are identical for all 30 listed errata | **High — [DOC]**, errata v3.0 (2025-10-11) |
| Does v3.1 add features? | **No.** Nothing in the datasheet, errata, PCN or IDF distinguishes v3.1's capability from v3.0's. `uart_download_dis`, Secure Boot V2 and the 12.5 kbit/s TWAI floor are all documented as "v3.0 and higher" / "v3.0/v3.1" | **High — [DOC]** |
| Does v3.1 require newer software? | **No** — see §21.6. It *may* be reported differently by older tooling | **High — [DOC]**, PCN §5(5) |
| Is the –40 ℃ ~ 105 ℃ crystal resistance change relevant to a bare U4WDH design? | The PCN scopes the 0 Ω → 100 Ω change to **modules**, not to the bare chip. But the *motivation* (high-temperature crystal stability) suggests the same care is worth taking in a bare-chip design. §18.2 already treats the crystal as mandatory | **[INF]** on the design advice; **[DOC]** that the PCN scopes item 6 to modules |
| Why is it called "ECO4" if it's minor? | Because the ECO scheme was sequential and had no way to express "minor" — that inexpressiveness is precisely the reason Espressif replaced it (AR2022-005). The `vM.X` name `v3.1` is the informative one; "ECO4" is a legacy label | **[INF]** on the reasoning; **[DOC]** that ECO4 ≡ v3.1 and that the scheme was replaced for this reason |

**On the thinness of the public record.** v3.1 has no dedicated user guide (unlike v3.0), no dedicated advisory, and gets no prose in the datasheet beyond a footnote. That is not an omission — it is the *point* of a minor revision, and it is consistent with what the numbering scheme promises. **The single most complete public document about v3.1 is PCN20220901, and it is four sentences long on the subject.** Anyone telling you v3.1 has new capabilities should be asked for a citation. **[INF]**

The public record does firmly date it: the errata document's own revision history records **v2.4, 2022-10-13: "Added chip revision v3.1 and v1.1"** **[DOC]** — twelve days before the PCN issue date.

### 21.5 Errata by revision — the ones you would actually hit

Full table is the ESP32 Series SoC Errata, Table 4. Reproduced here in full for the categories a developer touches, with **v3.0 and v3.1 collapsed into one column because they are identical**. `Y` = affected. **[DOC]**

| Erratum | v0.0 | v1.0 | v1.1 | **v3.0 / v3.1** | Fixed in | Practical bite |
|---|:--:|:--:|:--:|:--:|---|---|
| `CPU-3.5` CPU crashes on direct 240 → 80/160 MHz clock switch | Y | | | | v1.0 | Historic. IDF steps frequencies anyway |
| `CPU-3.9` External-SRAM access sequence causes read/write errors | | Y | Y | | **v3.0** | **The PSRAM cache bug.** Cost ~n% performance and a compiler workaround (`CONFIG_SPIRAM_CACHE_WORKAROUND`) on v1.x. **Gone on your chip** |
| `CPU-3.2` External SRAM through cache: read/write errors | Y | | | | v1.0 | Historic |
| `CPU-3.10` Simultaneous reads of different address spaces by both CPUs | Y | Y | Y | | **v3.0** | Underpins the DPORT workaround. **Gone on your chip** |
| `CPU-3.3` Repeated writes to a single peripheral address may be lost | Y | | | | v1.0 | Historic |
| `CPU-3.16` Speculative reads / delayed FIFO pointer in `0x3FF0_0000`–`0x3FF1_EFFF`, `0x3FF4_0000`–`0x3FF7_FFFF` | Y | Y | Y | **Y** | **No fix scheduled** | **Live on your chip.** Why register accesses must be `volatile`; why consecutive FIFO reads need 6 (@160 MHz) or 7 (@240 MHz) `nop`s. IDF handles this — do not hand-roll register access |
| `CPU-3.18` CPU limitations accessing peripherals (umbrella for 3.3/3.10/3.16) | Y | Y | Y | **Y** | — | Umbrella entry |
| `CPU-3.21` CPU interrupted during access to five specific FIFO registers halts subsequent accesses | Y | Y | Y | **Y** | No fix scheduled | Live. Added to the errata 2023-09-19 |
| `ULP-3.19` ULP + touch sensors unusable in deep sleep if `RTC_PERIPH` is powered up | Y | Y | Y | **Y** | No fix scheduled | **Live.** Bites anyone doing ULP or touch wake-up |
| `GPIO-3.6` GPIO pull-up/pull-down register fields nonfunctional on pads that are also `RTC_GPIO` | Y | Y | Y | **Y** | No fix scheduled | **Live, and a genuine trap.** On dual-function pads you must configure pulls through the **RTC_GPIO** registers. On this board that covers GPIO32 (`XSMT`) and the knob pins GPIO19/22 — see §5.2 |
| `GPIO-3.14` Edge interrupts cannot coexist with other interrupts within a GPIO group | Y | Y | Y | **Y** | No fix scheduled | **Live.** Relevant to knob-2 quadrature decoding if you use edge IRQs |
| `GPIO-3.11` GPIO36 / GPIO39 inputs pulled down ~80 ns when certain RTC peripherals power on | Y | Y | Y | **Y** | No fix scheduled | Live, but neither pin is used on this board (§5.3) |
| `RES-3.4` Brown-out reset does not work | Y | | | | v1.0 | Historic. IDF's `ESP_BROWNOUT_USE_INTR` exists for v0.0 |
| `RES-3.1` Spurious watchdog reset on power-up / deep-sleep wake | Y | | | | v1.0 | Historic |
| `RES-3.8` Flash start-up time causes spurious watchdog reset | Y | Y | Y | | **v3.0** | **Gone on your chip.** Was a real bring-up annoyance on v1.x |
| `CLK-3.7` Audio PLL frequency range limited | Y | | | | v1.0 | Historic — matters for I2S audio, which this board does |
| `CLK-3.22` Cannot use ESP32 as PHY clock source with Wi-Fi + Ethernet simultaneously | Y | Y | Y | **Y** | No fix scheduled | Live; no Ethernet on this board |
| `RTC-126` RTC register read error after light-sleep wake | Y | Y | Y | **Y** | No fix scheduled | Live |
| **`WDT-3.15` Dual-core cache live-lock → interrupt watchdog** | | | | **Y** | **No fix scheduled** | **⚠ Live on your chip and on no earlier revision.** See below |
| `UART-3.17` `fifo_cnt` misreports FIFO length when a DPORT read is interrupted | Y | Y | Y | **Y** | No fix scheduled | **Live.** Relevant to the inter-MCU UART link (§6) if you bypass the driver |
| `TWAI-3.13.x` (eleven separate CAN controller errata) | Y | Y | Y | **Y** | No fix scheduled | Live; no CAN on this board |
| `LEDC-3.12` Duty overflow in decremental fade mode | Y | Y | Y | **Y** | No fix scheduled | Live if you fade an LED down |

**⚠ `WDT-3.15` deserves its own paragraph, because it is the one erratum that is *worse* on your revision than on older silicon.** **[DOC]**

> "On ESP32 chip revision v3.0, when the following conditions are met at the same time, a live lock will occur, causing the CPUs to get stuck in the state of memory access and stop executing instructions. **(1)** Dual-core system. **(2)** Of the four Instruction/Data buses (IBUS/DBUS) that access external memory, three simultaneously initiate access requests to the same cache set, and all three requests result in cache misses."

Affected revisions: **v3.0 and v3.1 only.** Solution: **no fix scheduled.** The workaround is software: a level-4-or-5 high-priority interrupt on each core, wired to a common timer, which forces both cores into the handler and releases the IBUS contention in a three-stage dance. ESP-IDF implements this behind **`CONFIG_ESP32_ECO3_CACHE_LOCK_FIX`**, and the Kconfig entries for both `ESP32_REV_MIN_3` and `ESP32_REV_MIN_3_1` carry `select ESP_INT_WDT if ESP32_ECO3_CACHE_LOCK_FIX` **[DOC]**.

Note the two preconditions. **Dual-core** — which, per §14, this part now is. **External memory** — code or data in external flash/PSRAM via cache. Both hold for essentially every real IDF application on this chip. **Leave `CONFIG_ESP32_ECO3_CACHE_LOCK_FIX` alone (it defaults on when the minimum revision is v3.x) and do not disable the interrupt watchdog.** **[INF]** on that advice, **[DOC]** on the mechanism.

### 21.6 How to read the revision off a real board

Five independent methods, in order of how easy they are.

**1. esptool — the fastest check.** `chip_id` (or the modern spelling `chip-id`) prints the revision as part of the chip description.

```bash
# The board must be in download mode; see §7.1 for the USB-C orientation quirk
# — plug it the wrong way round and you will be talking to the S3, not this chip.
esptool.py --port /dev/ttyACM0 chip_id
```

Expected output — the line that matters is the third:

```
esptool.py v4.7.0
Serial port /dev/ttyACM0
Connecting....
Detecting chip type... ESP32
Chip is ESP32-U4WDH (revision v3.1)
Features: Wi-Fi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: ...
```

The exact format comes from esptool's own source, `esptool/targets/esp32.py` **[DOC]**:

```python
def get_minor_chip_version(self):
    return (self.read_efuse(5) >> 24) & 0x3

def get_major_chip_version(self):
    rev_bit0 = (self.read_efuse(3) >> 15) & 0x1
    rev_bit1 = (self.read_efuse(5) >> 20) & 0x1
    apb_ctl_date = self.read_reg(self.APB_CTL_DATE_ADDR)
    rev_bit2 = (apb_ctl_date >> self.APB_CTL_DATE_S) & self.APB_CTL_DATE_V
    combine_value = (rev_bit2 << 2) | (rev_bit1 << 1) | rev_bit0
    revision = {0: 0, 1: 1, 3: 2, 7: 3}.get(combine_value, 0)
    return revision

def get_chip_description(self):
    ...
    return f"{chip_name} (revision v{major_rev}.{minor_rev})"
```

Note that `flash_id` and every other esptool subcommand print the same `Chip is …` banner, so any esptool invocation will tell you. `chip_id` is simply the one with no side effects.

**⚠ esptool version matters for the *format*, not the answer.** `get_minor_chip_version()` and the `v{major}.{minor}` format string were introduced in **esptool v4.3**. Verified across tags: v4.2.1 and earlier print `revision %d` — i.e. a **v3.1 chip shows as `(revision 3)`** — while v4.3, v4.4, v4.5.x, v4.6 and v4.7.0 all print `(revision v3.1)`. **[DOC]** If you see `revision 3`, upgrade esptool before concluding anything; you are looking at a tool limitation, not at v3.0 silicon.

**2. The ESP-IDF boot banner.** The second-stage bootloader prints the revision on every boot:

```
I (29) boot: ESP-IDF v5.4-727-g5cbd2a3877 2nd stage bootloader
I (29) boot: compile time HH:MM:SS
I (29) boot: chip revision: v3.1
```

Watch it with `idf.py -p /dev/ttyACM0 monitor` (Ctrl-`]` to exit). This is the line you would quote in a bug report. **[DOC]** on the format — ESP-IDF's chip-revision documentation shows the same `vX.Y` rendering in its error messages.

**3. From code, at runtime.** Two APIs, and they answer subtly different questions:

```c
#include "esp_chip_info.h"
#include "hal/efuse_hal.h"

esp_chip_info_t info;
esp_chip_info(&info);
// info.revision is in major*100 + minor form on IDF >= v5.0  -> 301
// info.model    == CHIP_ESP32
// info.cores    == 2 on this part (see §14)

uint32_t full  = efuse_hal_chip_revision();        // 301
uint32_t major = efuse_hal_get_major_chip_version(); // 3
uint32_t minor = efuse_hal_get_minor_chip_version(); // 1

ESP_LOGI(TAG, "chip revision v%" PRIu32 ".%" PRIu32, major, minor);
```

`efuse_hal_chip_revision()` "returns revision in the `major * 100 + minor` format" **[DOC]**. So **`301` is the number to test for**, and the matching Kconfig constant is `CONFIG_ESP32_REV_MIN_FULL`. On **IDF < v5.0**, `esp_chip_info_t::revision` held a bare major number and would read `3` — see §21.7.

**4. eFuse bits — the ground truth.** Four fields encode the revision. Transcribed from the errata's Table 1 **[DOC]**:

| eFuse bit | v0.0 | v1.0 | v1.1 | v3.0 | **v3.1** |
|---|:--:|:--:|:--:|:--:|:--:|
| *Major* `APB_CTRL_DATE[31]` | 0 | 0 | 0 | 1 | **1** |
| *Major* `EFUSE_BLK0_RDATA5[20]` | 0 | 0 | 0 | 1 | **1** |
| *Major* `EFUSE_BLK0_RDATA3[15]` | 0 | 1 | 1 | 1 | **1** |
| *Minor* `EFUSE_BLK0_RDATA5[25]` | 0 | 0 | 0 | 0 | **0** |
| *Minor* `EFUSE_BLK0_RDATA5[24]` | 0 | 0 | **1** | 0 | **1** |

Read them with:

```bash
espefuse.py --port /dev/ttyACM0 summary
```

**The whole of v3.1 is `EFUSE_BLK0_RDATA5[24] == 1` on top of a v3.0 pattern.** That single bit is the difference, and PCN20220901's change table says so in as many words.

**5. The package marking.** The chip's *Espressif Tracking Information* line carries a letter in the second position **[DOC]**:

| Revision | Tracking-information line | Module specification-ID line |
|---|---|---|
| v0.0 | `XXXXXXXX` | `XXXXXX` |
| v1.0 | `X B XXXXXX` | `XXXXXX` |
| v1.1 | `X F XXXXXX` | `MF XXXX` |
| v3.0 | `X E XXXXXX` | `ME XXXX` |
| **v3.1** | **`X G XXXXXX`** | **`MG XXXX`** |

So on a bare U4WDH: **look for `G` in the second character of the tracking line.** `E` means v3.0. This is the only method that works with the board unpowered, and it pairs with the line-5 core-count rule already described in §14.2. Reading it in practice needs a macro lens and good raking light on a 5 × 5 mm QFN — it is a last resort, not a first one. **[INF]** on the practicality.

### 21.7 Tooling versions — what recognises v3.1, and what mis-reports it

**Nothing refuses to run.** There is no "chip revision too new" failure mode here, and it is worth being explicit about *why*, because the mechanism is genuinely reassuring.

ESP-IDF stores a maximum supported revision in the image header (`max_chip_rev_full`) and the bootloader refuses to boot beyond it. For ESP32 that value is **`CONFIG_ESP32_REV_MAX_FULL = 399`** — "maximum supported MAJOR version + 99" **[DOC]**. Since v3.1 is `301`, it sits far inside the window, and *every* ESP32 revision Espressif could ship without a major bump will too. The error you will therefore **never** see on this chip is:

```
Image requires chip rev <= v2.99, but chip is v3.0
```

The error you *can* see, if you build with `CONFIG_ESP32_REV_MIN` set to v3.x and then run it on old v1.x silicon, is the opposite one **[DOC]**:

```
Image requires chip rev >= v3.0, but chip is v1.0
```

That is not a v3.1 problem — it is a min-revision problem, and it only fires in the direction that cannot affect you.

| Tool | Version | Behaviour on a v3.1 chip | Class |
|---|---|---|---|
| **esptool** | ≤ v4.2.1 | Prints `Chip is ESP32-U4WDH (revision 3)` — major only, minor silently dropped | **[DOC]** |
| **esptool** | **≥ v4.3** | Prints `Chip is ESP32-U4WDH (revision v3.1)` | **[DOC]** |
| **ESP-IDF** | < v5.0 bootloaders | "The old bootloaders did not read the minor wafer version eFuse … the old bootloader can detect correctly only chip version in range v0.0 to v3.0, where the minor version is always set to 0." Boots and runs correctly; **reports `chip revision: 3`** | **[DOC]** |
| **ESP-IDF** | **v4.3.5 / v4.4.5 and later 4.x** | `ESP32_REV_MIN_3_1` / `Rev v3.1 (ECO4)` backported. Verified present at tags `v4.3.5`, `v4.4.5`, `v4.4.6`, `v4.4.7`; **absent** at `v4.4`, `v4.4.1`, `v4.4.2`, `v4.4.3`, `v4.4.4` | **[DOC]** |
| **ESP-IDF** | **≥ v5.0** | Full `vM.X` scheme. `major*100+minor` everywhere. Introduced by commit `1f9260d79` "all: Apply new version logic (major * 100 + minor)", 2022-11-03 | **[DOC]** |
| **ESP-IDF** | v5.1.4 / v5.2.5 / **v5.4** (this board's factory images, §11) | Full support. No action needed | **[DOC]** |
| **Arduino-ESP32** | 3.x (built on IDF v5.1+) | Full support | **[INF]** — inferred from the IDF version it embeds, not separately verified |
| **Arduino-ESP32** | 2.0.x (built on IDF v4.4) | Runs correctly. Whether the *label* reads `v3.1` or `3` depends on the exact IDF v4.4.x point release bundled | **[INF]** |

**The practical rule:** if your toolchain is ESP-IDF v5.x or Arduino-ESP32 3.x — which is everything this board's own firmware is built with — v3.1 is a non-event. If you are on something older and see `revision 3`, that is a *display* limitation and nothing is wrong.

**Note the asymmetry that makes all of this safe**, stated by Espressif directly: *"ESP-IDF is designed to execute seamlessly on future chip minor revisions with the same logic as the chip's nearest previous minor revision. Thus users can directly port their compiled binaries to newer MINOR chip revisions without upgrading their ESP-IDF version and re-compile the whole project."* **[DOC]** A v3.1 chip is treated as a v3.0 chip by any software that does not know about v3.1. Since it *is* a v3.0 chip functionally, that is correct behaviour rather than a fallback.

### 21.8 What v3.1 means for you, concretely

Everything below is a consequence of being **v3.x**, and applies to v3.0 and v3.1 alike. Nothing is unlocked by v3.1 that v3.0 did not already have.

| You can | Because | Class |
|---|---|---|
| **Use Secure Boot V2 (RSA-3072)** | v3.0 introduced the RSA-based scheme. The v3.0 user guide recommends it "from ESP-IDF v4.1 and later"; ESP32 Secure Boot V2 requires v3.x silicon | **[DOC]** |
| **Use Flash Encryption with fault-injection hardening** | v3.0 design change #5, addressing CVE-2019-17391 and CVE-2019-15894 | **[DOC]** |
| **Permanently disable UART Download Boot mode** | v3.0 design change #7, the `UART_DOWNLOAD_DIS` eFuse. Datasheet: "valid only for ESP32 chip revisions v3.0 and higher" | **[DOC]** |
| **Attach PSRAM without the cache workaround** | `CPU-3.9` fixed in v3.0. `CONFIG_SPIRAM_CACHE_WORKAROUND` is gated on `ESP32_REV_MIN_FULL < 300` in IDF's `esp_psram/esp32/Kconfig.spiram` and is therefore not even offered. Slightly better PSRAM performance results. **But read §18.5 first** — the U4WDH's real PSRAM obstacle is pin availability, not silicon | **[DOC]** |
| **Skip the DPORT simultaneous-read workaround** | `CPU-3.10` fixed in v3.0 | **[DOC]** |
| **Stop worrying about spurious watchdog resets at power-up** | `RES-3.8` fixed in v3.0. This was a common and confusing bring-up symptom on v1.x | **[DOC]** |
| **Run TWAI/CAN down to 12.5 kbit/s** | v3.0 design change #6. Irrelevant on this board — no CAN transceiver | **[DOC]** |
| **Set `CONFIG_ESP32_REV_MIN` to `Rev v3.0 (ECO3)` and shrink the binary** | Compiling out v0.x/v1.x workarounds reduces image size, per the Kconfig help text: "The compiled binary will only support chips above this revision, this will also help to reduce binary size." Safe here because U4WDH has never existed below v3.0 | **[DOC]** |

| You must still | Because | Class |
|---|---|---|
| **Leave `CONFIG_ESP32_ECO3_CACHE_LOCK_FIX` enabled and keep the interrupt watchdog on** | `WDT-3.15` is a **v3.x-only** erratum with no silicon fix. Both preconditions — dual core, external memory via cache — hold for this part | **[DOC]** on the erratum; **[INF]** on the advice |
| **Treat AES and flash-encryption keys as extractable by a well-equipped physical attacker** | AR2022-003. No hardware fix. Use per-device unique keys; enable Secure Boot and Flash Encryption together | **[DOC]** |
| **Configure pull-ups/pull-downs through RTC_GPIO registers on dual-function pads** | `GPIO-3.6`, unfixed on every revision. Affects GPIO32 (`XSMT`) and GPIO19/22 (knob 2) on this board | **[DOC]** |
| **Use `volatile` for all register access and respect the FIFO `nop` rules** | `CPU-3.16`, no fix scheduled. IDF's drivers already do; hand-written register code may not | **[DOC]** |
| **Avoid mixing edge interrupts with other interrupt types within one GPIO group** | `GPIO-3.14`, unfixed. Directly relevant if you decode knob 2 with edge IRQs | **[DOC]** |

**Should you set `CONFIG_ESP32_REV_MIN` to v3.1 rather than v3.0?** No reason to, and one small reason not to. Since the two are functionally identical, `301` buys you nothing over `300` in generated code, while `300` keeps the image runnable on any v3.0 stock you might later encounter — including, plausibly, an earlier board revision from the same vendor. **Set it to `Rev v3.0 (ECO3)`.** **[INF]**

### 21.9 Sources added 2026-08-21 for this section

| Title | URL | Retrieved | Version | Class | Local artifact |
|---|---|---:|---|---|---|
| **PCN20220901 — Upgrade Chip Revision of ESP32 Series Products** — *the primary v3.1 document* | https://www.espressif.com/sites/default/files/pcn_downloads/PCN20220901%20Upgrade%20Chip%20Revision%20of%20ESP32%20Series%20Products.pdf | 2026-08-21 | ESP-07-2-007-03 v1.4; issued 2022-10-25; ECN-2022-005/-015/-036 | **[DOC]** | `artifacts/pcn20220901-esp32-chip-revision-upgrade.pdf` |
| **AR2022-005 — Compatibility Advisory for Chip Revision Numbering Scheme** | https://www.espressif.com/sites/default/files/advisory_downloads/AR2022-005%20Compatibility%20Advisory%20for%20Chip%20Revision%20Numbering%20%20Scheme.pdf | 2026-08-21 | v1.0, 2022-09-29 | **[DOC]** | `artifacts/ar2022-005-chip-revision-numbering-scheme.pdf` |
| **AR2022-003 — Security Advisory Concerning Breaking the Hardware AES Core and Firmware Encryption of ESP32 Chip Revision v3.0** | https://www.espressif.com/sites/default/files/advisory_downloads/AR2022-003%20Security%20Advisory%20Concerning%20Breaking%20the%20Hardware%20AES%20Core%20and%20Firmware%20Encryption%20of%20ESP32%20Chip%20Revision%20v3.0%20-%20V2.0%20EN.pdf | 2026-08-21 | V2.0, 2022-11-18 | **[DOC]** | `artifacts/ar2022-003-esp32-v3-aes-fault-injection-advisory.pdf` |
| **ESP32 Series SoC Errata — HTML build** (text-extractable; the PDF's text layer is not — see §21.10) | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/index.html | 2026-08-21 | doc v3.0, 2025-10-11 | **[DOC]** | — (PDF form: `artifacts/esp32-errata.pdf`) |
| Errata — Chip Revision Identification chapter (eFuse + marking tables) | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/01-chip-identification/index.html | 2026-08-21 | doc v3.0 | **[DOC]** | — |
| Errata — Errata Summary chapter (Table 4, the per-revision matrix) | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/02-errata-summary/index.html | 2026-08-21 | doc v3.0 | **[DOC]** | — |
| Errata — All Errata Descriptions chapter | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/03-errata-description/index.html | 2026-08-21 | doc v3.0 | **[DOC]** | — |
| Errata — Revision History (dates v3.1's public appearance to 2022-10-13) | https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/revision-history/index.html | 2026-08-21 | doc v3.0 | **[DOC]** | — |
| **ESP-IDF Programming Guide — Chip Revision** (versioning scheme, compatibility checks, `efuse_hal_*` API, error strings) | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/chip_revision.html | 2026-08-21 | `latest` | **[DOC]** | — |
| **ESP-IDF `components/esp_hw_support/port/esp32/Kconfig.hw_support`** — *the only public source mapping ECO4 ≡ v3.1* | https://github.com/espressif/esp-idf/blob/master/components/esp_hw_support/port/esp32/Kconfig.hw_support | 2026-08-21 | `master` | **[DOC]** | — |
| ESP-IDF commit `1f9260d79` "all: Apply new version logic (major * 100 + minor)" — introduces `ESP32_REV_MIN_3_1` | https://github.com/espressif/esp-idf/commit/1f9260d79 | 2026-08-21 | 2022-11-03 | **[DOC]** | — |
| **esptool `esptool/targets/esp32.py`** — revision decode and output format | https://github.com/espressif/esptool/blob/master/esptool/targets/esp32.py | 2026-08-21 | `master` | **[DOC]** | — |
| Espressif PCN index (where PCN20220901 was located) | https://www.espressif.com/en/support/documents/pcns | 2026-08-21 | – | **[DOC]** | — |
| Espressif advisory index (where AR2022-003/-005 were located) | https://www.espressif.com/en/support/documents/advisories | 2026-08-21 | – | **[DOC]** | — |

**Wayback captures submitted 2026-08-21** (both accepted, HTTP 302 to the capture): PCN20220901 and AR2022-005. These are single-copy Espressif-hosted PDFs with no mirrors found, so they qualify under the repository's preserve-scarce-sources rule.

### 21.10 Retrieval notes for the next person

Three things cost time here and are worth recording.

**1. The errata PDF's text layer is obfuscated; use the readthedocs HTML build instead.** `artifacts/esp32-errata.pdf` and `artifacts/esp32-chip-revision-v3-0-user-guide.pdf` both carry a glyph-subset text layer with a **uniform +29 code-point offset** — but the offset is applied only to *some* character classes, so decoding is ambiguous where the shifted ranges collide (a raw `3` is either the digit `3` or an encoded `P`; a raw `p` is either lowercase `p` or an encoded `S`). Mechanical decoding produces text like `bpmPO peries po` brrataK` for *"ESP32 Series SoC Errata."* — legible to a human, useless to a parser.

The fix: **the errata is published as a proper Sphinx HTML site** at `https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/`, with clean tables. That is where every errata table in §21.5 and the eFuse/marking tables in §21.6 came from. The chapter slugs are `01-chip-identification/`, `02-errata-summary/`, `03-errata-description/`, `revision-history/`. **[INF]** on the workaround; it is simply what worked.

The v3.0 user guide has **no** HTML build — `https://documentation.espressif.com/esp32_chip_revision_v3_0_user_guide_en.html` returns the SPA shell, and the PDF is the only form. Its content is short enough (8 pages) to decode by eye, which is what was done for §21.3.

**2. `documentation.espressif.com` is now a JavaScript SPA and cannot be scraped.** Every `*.html` slug returns the same **13,745-byte** app shell (the soft-404 fingerprint already recorded in §19.4 — note it now matches *successful* pages too, not just missing ones, so the fingerprint is no longer a reliable 404 test on that host). Only `*.pdf` slugs return real content. **The `www.espressif.com/en/support/documents/pcns` and `…/advisories` index pages are still plain server-rendered HTML** and are the reliable way to enumerate PCNs and advisories — that is how PCN20220901 was found after direct URL guessing failed.

**3. Search engines were unhelpful and mostly blocked.** DuckDuckGo's `html`/`lite` endpoints returned an anti-bot challenge (HTTP 202 with a CAPTCHA page) under a Chrome UA. The document was found instead by **grepping the Espressif PCN index page for `href` values** — a reminder that for vendor documents, the vendor's own index beats a search engine. **[INF]**

| Document | Primary URL | Notes |
|---|---|---|
| PCN20220901 | `https://www.espressif.com/sites/default/files/pcn_downloads/PCN20220901%20Upgrade%20Chip%20Revision%20of%20ESP32%20Series%20Products.pdf` | 738,047 B, `%PDF-1.7` validated. Bilingual zh/en. **Guessing the filename fails** — enumerate from the PCN index |
| AR2022-005 | `https://www.espressif.com/sites/default/files/advisory_downloads/AR2022-005%20Compatibility%20Advisory%20for%20Chip%20Revision%20Numbering%20%20Scheme.pdf` | 97,490 B. **Note the double space** before `Scheme.pdf` in the real filename |
| AR2022-003 | `https://www.espressif.com/sites/default/files/advisory_downloads/AR2022-003%20Security%20Advisory%20Concerning%20Breaking%20the%20Hardware%20AES%20Core%20and%20Firmware%20Encryption%20of%20ESP32%20Chip%20Revision%20v3.0%20-%20V2.0%20EN.pdf` | 108,350 B |
| ESP32 Series SoC Errata | `https://docs.espressif.com/projects/esp-chip-errata/en/latest/esp32/` | **Use the HTML site.** PDF at `…/esp32/esp-chip-errata-en-master-esp32.pdf` |

### 21.11 Open questions left by this section

| # | Question | Status |
|---|---|---|
| 21a | Was **ECO2 / v2.0** ever shipped, and in what parts? | **Unresolved.** Present in ESP-IDF Kconfig and esptool's decode table; absent from the errata, from AR2022-005's mapping table and from datasheet Table 1-1. **[INF]** that it never reached broad production |
| 21b | Does the AES/flash-encryption side-channel advisory **AR2022-003** formally cover v3.1, or only v3.0? | **Unresolved.** The advisory names v3.0 in its title and predates the v3.1 PCN by three weeks. No v3.1-specific advisory has been published. **Assume it applies** — v3.1 is functionally v3.0 — but this is **[INF]**, not **[DOC]** |
| 21c | What exactly was the wafer-level process change behind v3.1? | **Not public.** PCN20220901 gives the goal ("stable operating under more complicated and high temperature circumstances") and none of the mechanism. Unlikely ever to be published |
| 21d | Does v3.1 shift the U4WDH's rated temperature range? | **No** — datasheet v5.3 lists one range for the part regardless of revision, and the PCN's item 6 (crystal resistance) is scoped to *modules*, not the bare chip. See §13.3 for the `H` grade trap. **[DOC]** on the PCN scoping |
| 21e | Which exact **Arduino-ESP32 2.0.x** point release first labels v3.1 correctly? | **Unresolved.** Bounded by the bundled IDF version (v4.4.5+ has the label); not verified release-by-release. Practically irrelevant — the chip works regardless |
