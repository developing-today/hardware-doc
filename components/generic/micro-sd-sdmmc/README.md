# microSD socket and 4-bit SDMMC interface

- **Category:** removable storage interface
- **Reference designator on this board:** `CARD1`
- **Socket part in the schematic BOM field:** `TF-018` — a generic 10-pin push-push microSD socket designation, not a traceable manufacturer part number
- **Owning MCU:** **ESP32-S3 only**, SDMMC host slot 1, 4-bit mode
- **Research status:** wiring fully established pin-by-pin; ESP-IDF and Arduino paths documented; two significant limitations of the shipped configuration identified (§5)
- **Retrieved:** 2026-08-21; schematic re-read pin-by-pin and demo `sdkconfig` audited 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source, including `sdkconfig` · **[DOC]** manufacturer datasheet or official programming guide · **[INF]** inference, reasoning given

---

## 1. Exact wiring **[SCH sheet 4 `4_OTHER.png`]**

`CARD1` is a 10-pin socket symbol. Every pin is accounted for:

| Socket pin | Name | Net | → ESP32-S3 GPIO | Pull-up |
|---:|---|---|---:|---|
| 1 | `DAT2` | `SDMMC_D2` | **42** | `R10` 10 kΩ → 3V3 |
| 2 | `CD/DAT3` | `SDMMC_D3` | **2** | `R49` 10 kΩ → 3V3 |
| 3 | `CMD` | `SDMMC_CMD` | **3** | `R48` 10 kΩ → 3V3 |
| 4 | `VDD` | **3V3** | — | `C21` 100 nF decoupling |
| 5 | `CLK` | `SDMMC_SCK` | **4** | **none — correct** |
| 6 | `VSS` | GND | — | |
| 7 | `DAT0` | `SDMMC_D0` | **5** | `R47` 10 kΩ → 3V3 |
| 8 | `DAT1` | `SDMMC_D1` | **6** | `R46` 10 kΩ → 3V3 |
| 9 | **`SWITCH`** | — | — | **NOT CONNECTED** |
| 10 | `SHELL` | GND | — | Shield to ground |

Three observations, in order of importance:

**1. All five pull-ups are present, and none is on `CLK`.** This is exactly right. Espressif's *SD Pull-up Requirements* document specifies 10 kΩ pull-ups on `CMD` and `DAT0`–`DAT3`, and explicitly **not** on `CLK` **[DOC]**. Many hobby boards get this wrong in one direction or the other. This one does not.

**2. Pin 9, the card-detect switch, is not connected.** There is **no card-detect signal on this board**. Software cannot tell whether a card is inserted except by attempting a transaction. §5.2.

**3. The socket is powered directly from the 3V3 rail with no switch.** There is no load switch and no way to power-cycle the card. If a card wedges in a bad state, **the only recovery is a full board power cycle** — a software reset does not reset the card. §5.3.

### 1.1 GPIO summary

```
CLK  = GPIO4      CMD  = GPIO3
D0   = GPIO5      D1   = GPIO6
D2   = GPIO42     D3   = GPIO2
```

Cross-checked between the schematic alias table on sheet 2 **[SCH]** and the vendor's own `#define`s in `sd_card_bsp.cpp` **[SRC]**. They agree.

**None of these six is an ESP32-S3 strapping pin**, so there are no boot-time constraints. (GPIO0, GPIO45 and GPIO46 are the strapping pins in use on this board, and they carry the audio mux select and the microphone respectively.)

### 1.2 Why arbitrary GPIOs work

The ESP32-S3's SDMMC host can route through the **GPIO matrix** rather than being fixed to dedicated IO-MUX pins — `CONFIG_SOC_SDMMC_USE_GPIO_MATRIX=y` in the vendor's `sdkconfig` confirms the capability is compiled in **[SRC]**. That is why this board can put `D2` on GPIO42 and `D3` on GPIO2, which are nowhere near each other.

The trade-off **[INF]**: GPIO-matrix routing adds propagation delay compared with direct IO-MUX pins, which slightly reduces the maximum reliable clock. In practice the ESP32-S3 handles 40 MHz high-speed mode through the matrix without difficulty, and that is what the vendor demo uses — but if you ever see CRC errors at 40 MHz that vanish at 20 MHz, this is the reason, not a bad card.

The `sdkconfig` also reports `CONFIG_SOC_SDMMC_NUM_SLOTS=2` and `CONFIG_SOC_SDMMC_DELAY_PHASE_NUM=4` **[SRC]** — two host slots and four selectable clock delay phases, the latter being the tuning knob if you do hit timing trouble.

## 2. Bus width, speed modes and what is *not* available

### 2.1 4-bit mode

The board wires all four data lines, so **4-bit SDMMC is available and is what the vendor uses** (`slot_config.width = 4`) **[SRC]**. Compared with 1-bit mode this is roughly a 4× throughput improvement, and compared with SPI mode considerably more than that.

You can drop to 1-bit (`width = 1`) if you need `D1`/`D2`/`D3` for something else — those three GPIOs (6, 42, 2) become free. `D3` doubles as card detect in some designs, but not here (§1).

### 2.2 Speed modes

| Mode | Clock | Signalling | Available here? |
|---|---:|---|---|
| Default Speed (DS) | 20 MHz | 3.3 V | ✅ `SDMMC_FREQ_DEFAULT` |
| **High Speed (HS)** | **40 MHz** | 3.3 V | ✅ **`SDMMC_FREQ_HIGHSPEED`, what the demo uses** |
| SDR12 / SDR25 / **SDR50** / SDR104 | up to 208 MHz | **1.8 V** | ❌ |
| DDR50 | 50 MHz | **1.8 V** | ❌ |

**All UHS-I modes are unavailable on this board**, and this is a hardware fact, not a driver limitation. UHS-I requires the host to switch the bus to **1.8 V signalling**, and this board has:

- The card's `VDD` hard-wired to the 3.3 V rail **[SCH]**
- No level shifter on any bus line **[SCH]**
- No 1.8 V rail anywhere **[SCH, all five sheets]**

So the ceiling is **High Speed, 40 MHz, 4-bit**. Theoretical bus bandwidth is `40 MHz × 4 bits = 20 MB/s`; realistic sustained throughput after protocol and FATFS overhead is meaningfully lower, and is usually limited by the card's own controller rather than the bus.

**Practical consequence:** buying a fast UHS-I or V30 card for this board buys you nothing over a decent Class 10. Card *quality* still matters — random-write latency varies enormously between cards — but the headline speed rating does not.

## 3. What the vendor demo does **[SRC]**

`Arduino/examples/02_SD_Card/sd_card_bsp.cpp` and its ESP-IDF twin `ESP-IDF/02_SD_Card/components/sdcard_bsp/sdcard_bsp.c`:

```c
esp_vfs_fat_sdmmc_mount_config_t mount_config = {
    .format_if_mount_failed = false,   // will NOT format an unreadable card
    .max_files              = 5,
    .allocation_unit_size   = 512,
};

sdmmc_host_t host = SDMMC_HOST_DEFAULT();
host.max_freq_khz = SDMMC_FREQ_HIGHSPEED;   // 40 MHz

sdmmc_slot_config_t slot_config = SDMMC_SLOT_CONFIG_DEFAULT();
slot_config.width = 4;
slot_config.clk = GPIO_NUM_4;
slot_config.cmd = GPIO_NUM_3;
slot_config.d0  = GPIO_NUM_5;
slot_config.d1  = GPIO_NUM_6;
slot_config.d2  = GPIO_NUM_42;
slot_config.d3  = GPIO_NUM_2;

esp_vfs_fat_sdmmc_mount("/sdcard", &host, &slot_config, &mount_config, &card);
```

Then ordinary C stdio against `/sdcard/...`: `fopen`, `fprintf`, `fread`, `fclose`. `sdmmc_card_print_info(stdout, card)` dumps the card's CID/CSD, which is the single most useful diagnostic when a card misbehaves — call it.

The demo also computes capacity as `(float)(card->csd.capacity) / 2048 / 1024`, giving GiB **[SRC]**. That is correct only for 512-byte-sector cards, which in practice is all of them.

### 3.1 Two bugs worth not copying

**`ESP_ERROR_CHECK_WITHOUT_ABORT` on the mount.** The demo logs a mount failure and carries on with `card == NULL`, and every subsequent function tests for `NULL` and silently returns `ESP_ERR_NOT_FOUND` **[SRC]**. That is defensible for a demo, but in real firmware you want the mount result and you want to act on it.

**`fprintf(f, data)` with a runtime string as the format argument** in `s_example_write_file()` **[SRC]**. If the data ever contains a `%`, this is undefined behaviour and a format-string vulnerability. Use `fputs(data, f)` or `fprintf(f, "%s", data)`.

## 4. ⚠ Formatting requirements the demos expect

This section is the one most likely to save you an afternoon.

### 4.1 The card must be FAT — and `format_if_mount_failed` is `false`

The demo sets `.format_if_mount_failed = false` **[SRC]**. So:

- An **exFAT** card will not mount. ESP-IDF's FATFS is built without exFAT support by default, and exFAT is what Windows and macOS choose by default for cards **larger than 32 GB**.
- An **NTFS**, **ext4** or **APFS** card will not mount.
- An **unformatted** card will not mount.
- In every case you get a mount failure and, in the vendor demo, a silent `card == NULL`.

**Format the card as FAT32 (or FAT16 for small cards) before first use.** On Linux: `mkfs.vfat -F 32 /dev/sdX1`. On Windows, cards over 32 GB need a third-party tool or `format /FS:FAT32`, because the built-in dialog refuses FAT32 above 32 GB. On macOS, Disk Utility → "MS-DOS (FAT)".

The practical guidance: **use a card of 32 GB or less.** Larger cards work if you force FAT32, but the default formatting on a retail 64 GB+ card is exFAT and it will not mount.

### 4.2 ⚠ Long filenames are disabled

The vendor's `sdkconfig` contains **[SRC]**:

```
CONFIG_FATFS_LFN_NONE=y
CONFIG_FATFS_CODEPAGE_437=y
CONFIG_FATFS_CODEPAGE=437
```

`FATFS_LFN_NONE` means **8.3 short filenames only**. `myverylongfilename.txt` cannot be created and an existing one cannot be opened by that name. Codepage 437 means US-ASCII — **no accented characters, no CJK, no UTF-8 filenames.**

This is the kind of setting that produces baffling "file not found" behaviour on a card that clearly contains the file. If you need long filenames — and for anything storing user content you do — change it in `menuconfig`:

```
Component config → FAT Filesystem support → Long filename support
    → Long filename buffer in heap        (CONFIG_FATFS_LFN_HEAP)
Component config → FAT Filesystem support → OEM Code Page
    → API uses UTF-8                       (CONFIG_FATFS_API_ENCODING_UTF_8)
```

`LFN_HEAP` costs a little RAM per open file; `LFN_STACK` costs stack instead. Either is fine on this board given the PSRAM.

### 4.3 Sector size and allocation unit disagree

The `sdkconfig` sets `CONFIG_FATFS_SECTOR_4096=y` **[SRC]**, while the mount config passes `.allocation_unit_size = 512` **[SRC]**.

`allocation_unit_size` is only consulted when ESP-IDF *formats* a card, and `format_if_mount_failed` is `false`, so in the shipped demo this mismatch is inert. But **if you enable `format_if_mount_failed`, this combination is inconsistent** and you should set `allocation_unit_size` to `4096` (or to `16 * 1024`, which ESP-IDF's own examples use for better throughput) to match the compiled sector size.

Related: `CONFIG_FATFS_ALLOC_PREFER_EXTRAM=y` **[SRC]** puts FATFS buffers in PSRAM. Good on a board with 8 MB of it — but it means FATFS buffers are in a slower memory and are not DMA-capable, which the driver handles by bouncing. Fine; just be aware if you are profiling.

Other relevant settings in the shipped `sdkconfig` **[SRC]**:

| Setting | Value | Meaning |
|---|---|---|
| `CONFIG_FATFS_VOLUME_COUNT` | 2 | Two mount points possible (SD + a flash FAT partition) |
| `CONFIG_FATFS_FS_LOCK` | 0 | **No file-lock table.** Concurrent access to the same file from two tasks is unprotected |
| `CONFIG_FATFS_TIMEOUT_MS` | 10000 | 10 s FS mutex timeout |
| `CONFIG_FATFS_PER_FILE_CACHE` | y | A sector cache per open file — costs RAM, helps sequential I/O |
| `CONFIG_FATFS_LINK_LOCK` | y | |

Note `FATFS_FS_LOCK = 0` in particular: if two FreeRTOS tasks touch the same file, **you must provide your own mutex.**

## 5. Limitations of this hardware design

### 5.1 No write-protect

microSD has no write-protect notch (that is a full-size SD feature), so this is not a board limitation — just do not expect one.

### 5.2 No card detect

Socket pin 9 (`SWITCH`) is unconnected **[SCH]**. Consequences:

- **You cannot detect insertion or removal.** No interrupt, no polling target.
- **Hot-swap is unsupported.** Removing a card while mounted will corrupt whatever was in flight and leave the VFS with a stale handle.
- Detecting a card requires *attempting* `esp_vfs_fat_sdmmc_mount()`, which takes hundreds of milliseconds and prints errors on failure.

**Recommended pattern:** mount once at boot; if it fails, mark storage unavailable and expose a "retry" action in the UI rather than polling. If you must poll, `sdmmc_get_status(card)` is a cheap liveness check on an already-mounted card — the vendor demo uses it before each file operation **[SRC]**, which is a reasonable idiom.

### 5.3 No power control

`VDD` is hardwired to 3V3 **[SCH]**. There is no load switch. A card that has hung — which does happen, particularly cheap cards during a write — **cannot be reset in software.** `esp_vfs_fat_sdmmc_unmount()` and remount will often not recover it, because the card's own controller is stuck. The only reliable recovery is removing the card or power-cycling the board.

### 5.4 It shares the 3.3 V rail with everything else

SD write bursts draw **100–200 mA [INF]**, card-dependent, and they are bursty. That lands on the same rail as the radios, the display and the haptics. See [tlv62569dbvt §5](../../texas-instruments/tlv62569dbvt/README.md#5-power-budget-for-the-33-v-rail) — the rail copes, but stacking an SD write on a Wi-Fi TX burst and a haptic pulse is the worst case and is avoidable.

`C21` is only 100 nF **[SCH]**. There is no bulk capacitor at the socket. **[INF]** If you see write failures on a particular card, adding 10–22 µF close to socket pin 4 is the first thing to try — it is a classic fix for cards with aggressive inrush.

## 6. Software: ESP-IDF and Arduino

### 6.1 ESP-IDF

The vendor demos build against **ESP-IDF 5.3.2** **[SRC, `sdkconfig` header line]**. The relevant APIs are stable across 5.x:

| Header | Purpose |
|---|---|
| `driver/sdmmc_host.h` | `SDMMC_HOST_DEFAULT()`, `SDMMC_SLOT_CONFIG_DEFAULT()`, the slot/pin structure |
| `sdmmc_cmd.h` | `sdmmc_card_print_info()`, `sdmmc_get_status()`, raw block I/O |
| `esp_vfs_fat.h` | `esp_vfs_fat_sdmmc_mount()`, `esp_vfs_fat_sdmmc_unmount()` |

A more defensive version of the vendor's init:

```c
#include "driver/sdmmc_host.h"
#include "esp_vfs_fat.h"
#include "sdmmc_cmd.h"

static sdmmc_card_t *s_card;

esp_err_t sd_mount(void)
{
    esp_vfs_fat_sdmmc_mount_config_t mount_cfg = {
        .format_if_mount_failed = false,      // see 4.1 before changing this
        .max_files              = 5,
        .allocation_unit_size   = 16 * 1024,  // only used if formatting
    };

    sdmmc_host_t host = SDMMC_HOST_DEFAULT();
    host.max_freq_khz = SDMMC_FREQ_HIGHSPEED;   // 40 MHz; drop to
                                                // SDMMC_FREQ_DEFAULT (20 MHz)
                                                // if you see CRC errors
    sdmmc_slot_config_t slot = SDMMC_SLOT_CONFIG_DEFAULT();
    slot.width = 4;
    slot.clk = GPIO_NUM_4;  slot.cmd = GPIO_NUM_3;
    slot.d0  = GPIO_NUM_5;  slot.d1  = GPIO_NUM_6;
    slot.d2  = GPIO_NUM_42; slot.d3  = GPIO_NUM_2;
    // External 10k pull-ups are fitted on CMD and D0-D3 (R46-R49, R10).
    // Enabling the internal ones as well is harmless but redundant:
    // slot.flags |= SDMMC_SLOT_FLAG_INTERNAL_PULLUP;

    esp_err_t err = esp_vfs_fat_sdmmc_mount("/sdcard", &host, &slot,
                                            &mount_cfg, &s_card);
    if (err == ESP_FAIL) {
        ESP_LOGE(TAG, "Mount failed. Card is probably exFAT or unformatted "
                      "-- reformat as FAT32. See section 4.1.");
        return err;
    } else if (err != ESP_OK) {
        ESP_LOGE(TAG, "SD init failed: %s. Check the card is seated.",
                 esp_err_to_name(err));
        return err;
    }
    sdmmc_card_print_info(stdout, s_card);
    return ESP_OK;
}
```

Note the distinction ESP-IDF makes: **`ESP_FAIL` means the card was found but the filesystem could not be mounted** (almost always a formatting problem), while other errors mean the card itself did not initialise (seating, wiring, clock). Reporting them differently turns a mysterious failure into an actionable one.

### 6.2 Arduino

The vendor's "Arduino" example is really ESP-IDF code inside an `.ino` — it includes `driver/sdmmc_host.h` and calls `esp_vfs_fat_sdmmc_mount()` directly **[SRC]**. That works, and it is the most portable option.

If you prefer the idiomatic Arduino path, **arduino-esp32 3.x** (which is built on ESP-IDF 5.x) provides `SD_MMC` with configurable pins:

```cpp
#include "SD_MMC.h"

void setup() {
  Serial.begin(115200);
  // clk, cmd, d0, d1, d2, d3
  SD_MMC.setPins(4, 3, 5, 6, 42, 2);
  //             mountpoint, mode1bit, format_if_empty, freq
  if (!SD_MMC.begin("/sdcard", false, false, SDMMC_FREQ_HIGHSPEED)) {
    Serial.println("SD_MMC mount failed");
    return;
  }
  Serial.printf("Card size: %llu MB\n", SD_MMC.cardSize() / (1024ULL*1024ULL));
}
```

`SD_MMC.setPins()` requires **arduino-esp32 ≥ 2.0.7**; on earlier versions the pins were fixed and this board would not work at all. Note the second argument is `mode1bit` — pass `false` for 4-bit.

**Do not use the `SD` library** (`SD.h`) here. That is the SPI-mode driver; it would work electrically but would throw away the 4-bit bus for no reason.

### 6.3 Card compatibility

| Card type | Works? | Note |
|---|---|---|
| SDSC (≤ 2 GB), FAT16 | ✅ | |
| SDHC (4–32 GB), FAT32 | ✅ | **The sweet spot.** Retail formatting is FAT32 |
| SDXC (≥ 64 GB), **exFAT as shipped** | ❌ | **Must be reformatted to FAT32.** §4.1 |
| SDXC (≥ 64 GB), reformatted FAT32 | ✅ | Works, but you gain nothing over 32 GB |
| UHS-I / UHS-II speed classes | ✅ but **derated** | Falls back to 3.3 V High Speed. §2.2 |
| Cards with a partition table vs superfloppy | Both usually fine | ESP-IDF handles both. If one fails, try the other layout |
| microSD-to-SD adapters | n/a | Socket is microSD |

Cheap counterfeit cards are the single most common cause of unexplained SD trouble. `sdmmc_card_print_info()` prints the reported capacity; compare it against reality with a full-card write-read test before trusting a card.

## 7. Pitfalls, in order of likelihood

1. **exFAT card silently fails to mount.** §4.1. Reformat as FAT32.
2. **Long filenames do not work.** §4.2. `CONFIG_FATFS_LFN_NONE=y` in the shipped config.
3. **No card detect, so "is there a card?" is not answerable cheaply.** §5.2.
4. **A hung card cannot be reset without a power cycle.** §5.3.
5. **CRC errors at 40 MHz.** Drop to `SDMMC_FREQ_DEFAULT` (20 MHz). §1.2.
6. **Two tasks writing the same file corrupt it.** `CONFIG_FATFS_FS_LOCK=0`. §4.3.
7. **Removing a card while mounted corrupts it.** No hot-swap support.
8. **`format_if_mount_failed = true` will erase a user's card** on the first mount hiccup. Think carefully before enabling it in shipping firmware; it is a data-loss footgun dressed as convenience.
9. **`GPIO2` is `D3`.** If you are probing, note that GPIO2 sits between the microphone pins and the SD pins in the numbering but belongs to SD.

## 8. Open questions

| Question | Status |
|---|---|
| Socket manufacturer and exact part | **Unknown.** `TF-018` is a generic designation used by many Chinese connector vendors, not a traceable part number |
| Whether the socket is push-push or push-pull | **[INF]** almost certainly push-push, the near-universal choice for microSD, but not documented |
| Measured sustained read/write throughput | **Unknown.** Not published, not measured here |
| Measured peak current during write | **Unknown.** §5.4 uses a generic 100–200 mA estimate |
| Whether the factory S3 firmware uses the SD card at all | **Not established** from the retained material |

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `CARD1`, ESP32-S3 SDMMC 4-bit on GPIO2/3/4/5/6/42

## Related pages

- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)
- [texas-instruments/tlv62569dbvt](../../texas-instruments/tlv62569dbvt/README.md) — the shared 3.3 V rail and its transient budget
- [winbond/w25q128jvpiq](../../winbond/w25q128jv/README.md) — the other non-volatile storage on the S3
- [espressif/esp32-s3r8](../../espressif/esp32-s3r8/README.md) — the host

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Board schematic sheet 4 — `CARD1` `TF-018`, pull-ups `R10`/`R46`–`R49`, `C21`, unconnected `SWITCH` | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/4_OTHER.png` |
| Board schematic sheet 2 — `SDMMC_*` nets aliased to GPIO2/3/4/5/6/42 | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Waveshare demo `02_SD_Card` (Arduino) — `sd_card_bsp.cpp` | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/02_SD_Card/` |
| Waveshare demo `02_SD_Card` (ESP-IDF) — including the `sdkconfig` that sets `FATFS_LFN_NONE` and `FATFS_SECTOR_4096` | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/ESP-IDF/02_SD_Card/` |
| ESP-IDF v5.3.2 — SDMMC Host Driver | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/sdmmc_host.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
| ESP-IDF v5.3.2 — **SD Pull-up Requirements** (source of the "no pull-up on CLK" rule) | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/sd_pullup_requirements.html | 2026-08-23 | same archived PDF |
| ESP-IDF v5.3.2 — FAT Filesystem Support (`FATFS_LFN_*`, `FATFS_SECTOR_*`, `FATFS_FS_LOCK`) | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/storage/fatfs.html | 2026-08-23 | same archived PDF |
| arduino-esp32 — `SD_MMC` with `setPins()` (requires ≥ 2.0.7) | https://github.com/espressif/arduino-esp32/tree/master/libraries/SD_MMC | 2026-08-23 | — |
| ESP32-S3 Technical Reference Manual (SDMMC host chapter) | https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual.pdf` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
