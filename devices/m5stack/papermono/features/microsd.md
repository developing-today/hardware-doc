# microSD — M5Stack PaperMono

> **How do I mount the card, and why does nothing happen when I try?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

## 1. Capability summary and the hardware path

A microSD slot wired for **4-bit SDMMC** — not SPI — with its power rail and its
card-detect switch both behind the [I/O expander](io-expander.md).

```
ESP32-S3  ──4-bit SDMMC, GPIO8-13──▶  microSD slot
                                          ▲
              TF_3V3_L3B (AW35122 U8) ────┤ power,  enabled by M5IOE1 IO14
              card-detect switch ─────────┘ sensed by M5IOE1 IO1 (LOW = inserted)
```

| Signal | GPIO | Note |
|---|---|---|
| `DAT3` | **GPIO8** | |
| `DAT2` | **GPIO9** | |
| `DAT1` | **GPIO10** | |
| `DAT0` | **GPIO11** | |
| `CMD` | **GPIO12** | |
| `CLK` | **GPIO13** | 22 Ω series (`R35`) |
| Power enable | M5IOE1 **`IO14`** | `TF_EN` |
| Card detect | M5IOE1 **`IO1`** | `TF_DET`, **low = inserted** |

Confirmed by two independent sources: `M5PaperMono-UserDemo/main/hal/hal_tf_card.cpp:17–22`
and `M5Unified/src/M5Unified.cpp:216` (the `board_M5PaperMono` SD pin set, identical on
`master` and `develop`).

Power switch: [`components/awinic/aw35122`](../../../../components/awinic/aw35122/README.md).
Expander: [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md).

## 2. Card detect

M5Stack, on the product page:

> "`TF_DET` is pulled up by the microSD power domain. When the card slot switch is closed,
> the detection pin is pulled low to identify microSD card insertion."

Two consequences that follow from *"pulled up by the microSD power domain"*:

- **Card detect only works while `TF_3V3_L3B` is on.** If you drop the card's power to
  save current, you also lose the ability to see whether a card is present.
- The factory firmware sets `IO1` as an input with a **pull-up enabled on the expander**
  (`hal_tf_card.cpp:34–37`) rather than relying solely on the card rail.

The vendor's own bring-up leaves the card **powered off** by default:

```cpp
ioe1.pinMode(TF_EN_PIN, OUTPUT);                        // M5IOE1_PIN_14
ioe1.pinMode(TF_DET_PIN, INPUT);                        // M5IOE1_PIN_1
ioe1.setDriveMode(TF_EN_PIN, M5IOE1_DRIVE_PUSHPULL);
ioe1.setPullMode(TF_DET_PIN, M5IOE1_PULL_UP);
ioe1.digitalWriteWithRes(TF_EN_PIN, LOW, &err);         // power OFF at init
```

M5GFX, by contrast, drives `IO14` **high** during board bring-up
(`M5GFX.cpp:2096`, mask bit 13). So depending on which library initialised the board, the
card rail may or may not already be on. Check, do not assume.

> A relevant version delta: M5Unified `develop` **removes an SD-card power-on block** from
> `Power_Class.cpp` around line 364 relative to `master`. If SD power behaviour changes
> between two of your builds, that is where to look.

## 3. Prerequisites

| Item | Value |
|---|---|
| ESP-IDF | 5.5.1 — `driver/sdmmc_host.h`, `esp_vfs_fat.h`, `sdmmc_cmd.h` |
| M5Unified | 0.2.21 |
| M5IOE1 | 1.0.9 |
| FATFS config | The vendor's `sdkconfig.defaults` sets `CONFIG_FATFS_LFN_HEAP=y`, `CONFIG_FATFS_MAX_LFN=255`, `CONFIG_FATFS_API_ENCODING_UTF_8=y`, `CONFIG_FATFS_CODEPAGE_DYNAMIC=y` |
| Power state | **L3B** |

The UTF-8 / long-filename settings are worth copying: they are why the factory firmware
handles CJK filenames, and their absence is a common cause of "the file is there but I
cannot open it".

## 4. Resources consumed

| Resource | Value |
|---|---|
| ESP32-S3 GPIO | **six**: GPIO8–GPIO13 |
| Peripheral | **SDMMC host**, slot config `width = 4` |
| Expander pins | `IO14` power, `IO1` detect |
| Rail | `TF_3V3_L3B` (state L3B) |
| Mount point | `/sdcard` in the factory firmware |
| Heap | `max_files = 8`, `allocation_unit_size = 16 * 1024` |

**Six GPIOs is the largest single GPIO allocation on the board.** Dropping to 1-bit mode
would free GPIO8–GPIO10, but there is no header to expose them on, so there is nothing to
gain.

## 5. Minimal procedure (`inferred`)

Transcribed in shape from `hal_tf_card.cpp:142–157`. **Not run on hardware.**

```c
#include <driver/sdmmc_host.h>
#include <esp_vfs_fat.h>
#include <sdmmc_cmd.h>

// 1. power the card and check detect, both through the expander
ioe1.setDriveMode(M5IOE1_PIN_14, M5IOE1_DRIVE_PUSHPULL);
ioe1.digitalWrite(M5IOE1_PIN_14, HIGH);         // TF_EN on
vTaskDelay(pdMS_TO_TICKS(10));
bool inserted = (ioe1.digitalRead(M5IOE1_PIN_1) == LOW);   // LOW = card present

// 2. mount
esp_vfs_fat_sdmmc_mount_config_t mount_config = {};
mount_config.format_if_mount_failed = false;    // vendor default - do not reformat a user's card
mount_config.max_files              = 8;
mount_config.allocation_unit_size   = 16 * 1024;

sdmmc_host_t host               = SDMMC_HOST_DEFAULT();
sdmmc_slot_config_t slot_config = SDMMC_SLOT_CONFIG_DEFAULT();
slot_config.width = 4;
slot_config.clk = GPIO_NUM_13;  slot_config.cmd = GPIO_NUM_12;
slot_config.d0  = GPIO_NUM_11;  slot_config.d1  = GPIO_NUM_10;
slot_config.d2  = GPIO_NUM_9;   slot_config.d3  = GPIO_NUM_8;

sdmmc_card_t* card = NULL;
esp_err_t ret = esp_vfs_fat_sdmmc_mount("/sdcard", &host, &slot_config, &mount_config, &card);
```

Remember the [expander off-by-one](io-expander.md#2--trap-1-m5ioe1_pin_3--2): use
`M5IOE1_PIN_14` and `M5IOE1_PIN_1`, never the literals `14` and `1`.

## 6. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Silicon (ESP32-S3)** | One SDMMC host; 4-bit mode uses six pins |
| **Board** | Power and detect both behind I²C. **No I²C, no card** |
| **Board** | 22 Ω series on `CLK` only |
| **Framework** | `SDMMC_HOST_DEFAULT()` — the vendor does **not** override `max_freq_khz`, so the card runs at the IDF default |
| **Framework** | `format_if_mount_failed = false` in vendor code |
| **Observed** | **Nothing.** No throughput figure, no capacity limit, no filesystem compatibility report exists from anyone |

**No card capacity or filesystem limit is documented by M5Stack anywhere.** The usual
ESP-IDF FATFS constraints apply — exFAT is not supported by the stock driver, so cards
larger than 32 GB generally need reformatting to FAT32 — but that is a general ESP-IDF
statement, `inferred`, not a PaperMono finding.

## 7. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| microSD + [display](epaper-display.md) | ✅ no pin conflict | SDMMC GPIO8–13, panel GPIO14–18. Both in L3B; both power enables are expander pins |
| **microSD + display + [Wi-Fi](wifi-and-bluetooth.md)** | ⚠ **untested, and the interesting case** | No pin conflict at all. The pressure is on GDMA, PSRAM bandwidth and the L3B rail simultaneously: a full e-paper refresh is seconds of SPI DMA, SDMMC is a second DMA client, and Wi-Fi is a third plus an RF current draw. **Nobody has run this.** See [`../resources-and-conflicts.md`](../resources-and-conflicts.md) |
| microSD + [LoRa](lora.md) | ✅ | Different SPI host; LoRa is on `SPI3_HOST`, SD is not on SPI at all |
| microSD + [sleep](power-and-sleep.md) | ⚠ **unmount first** | The rail is L3B. Dropping it under an open file is a corruption path |
| microSD + card removal | ⚠ | Detect is polled, not interrupt-driven, in vendor code. Hot-removal during a write is not protected |
| microSD + [charger](battery-and-charging.md) access | ⚠ | Unrelated buses, but both need the expander; do not gate the charger inside a mount sequence |

## 8. Debugging

| Symptom | Cause |
|---|---|
| Card never detected | `TF_EN` (`IO14`) is low — the vendor's own init leaves it off |
| Detect reads "inserted" with no card | Card rail off, so the pull-up domain is dead; or you inverted the sense (**low = inserted**) |
| Mount fails | Card not FAT32; `format_if_mount_failed = false` so it will not silently reformat |
| Filenames with non-ASCII characters fail | Missing `CONFIG_FATFS_API_ENCODING_UTF_8` / `CONFIG_FATFS_MAX_LFN=255` |
| Card works under one library, not another | M5GFX drives `IO14` high at bring-up; the factory HAL drives it low. Check who initialised |
| Corruption after sleep | Rail dropped with files open |
| SD power behaves differently between builds | M5Unified `develop` removed an SD power-on block relative to `master` |

## 9. Alternatives for storage

| Option | Size | Use when |
|---|---|---|
| **microSD** | unspecified by the vendor | Bulk data, book files, logs |
| **NVS** | 24 KB partition at `0x9000` | Settings, credentials |
| Flash free space | ~960 KB unallocated above the app | Nothing uses it as shipped |
| PSRAM | 8 MB octal | Volatile buffers only — and the display needs it |

> **There is no SPIFFS, no FATFS-in-flash and no OTA slot** in either vendor project. The
> partition table is three entries: `nvs` 24 KB, `phy_init` 4 KB, and a single
> `factory` app of `0xF00000` (15 MiB) at `0x10000`. By contrast the third-party
> CrossPoint e-reader image repartitions entirely — 6400 KB app, a 4096 KB `cjkfont`
> partition, SPIFFS and a coredump region — which is a good demonstration that the layout
> is a firmware choice, not a hardware constraint.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; microSD is fitted on both C153 and C153-LITE |
| Framework range | ESP-IDF 5.5.1 · M5Unified 0.2.21 · M5IOE1 1.0.9 |
| Evidence | Pin map: **two independent sources** (`hal_tf_card.cpp`, `M5Unified.cpp:216`), `executed-success` read. Detect semantics: **vendor-documented**. Mount sketch: **`inferred`** |
| Confidence | High on wiring; **no performance evidence at all** |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md)
- [`io-expander.md`](io-expander.md) · [`power-and-sleep.md`](power-and-sleep.md) · [`epaper-display.md`](epaper-display.md)
- [`components/awinic/aw35122`](../../../../components/awinic/aw35122/README.md) · [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md)
