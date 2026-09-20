# Techniques — writing software for the ESP32-S3-Knob-Touch-LCD-1.8

Practical, reusable patterns organised by subsystem. Each entry gives **the minimal working pattern**, the **library/component and version**, the **gotcha** that will cost you an afternoon, and a **citation**.

This page is deliberately *not* a hardware reference. Pin tables live in [pinouts-and-buses.md](pinouts-and-buses.md); per-chip analysis lives in the component pages linked from each section. Nothing here is duplicated from those — follow the links.

## Evidence labels

| Tag | Meaning |
|---|---|
| **[SRC]** | Read from real code in [`artifacts/demo/`](artifacts/demo/) or a catalogued repository. Paths and line numbers are given. |
| **[COM]** | Community claim — a forum post, issue or video. Not independently reproduced by us. |
| **[INF]** | Inference from datasheets, schematic or arithmetic. Reasoning is shown so you can check it. |

All `[SRC]` citations below were re-verified against the demo tree on **2026-08-24**.

---

## 1. Display

### 1.1 Bring-up: get the bus parameters right, ignore the controller-name argument

The single most useful fact about this panel is that **the bus parameters matter and the driver name does not.** The vendor code calls the driver `esp_lcd_sh8601`, the product page says **ST77916**, and this conflict is *unresolved* — see [gaps-and-conflicts.md](gaps-and-conflicts.md#L29) and [Sitronix ST77916 §2](../../../components/sitronix/st77916/README.md). Community projects succeed with **both** driver names, which is itself the evidence that the naming is not what makes the panel work. **[COM]** ([examples/catalog.md](examples/catalog.md) — `juggernautwins608` patches `Arduino_GFX` for "ST77916 V2"; `UnkMihai` and `BlueKnob` use `esp_lcd_sh8601`; all three work.)

What actually has to be right is **QSPI, 32-bit command frames, 40 MHz**:

```c
// The whole story is in this one macro — do not hand-roll it.
#define SH8601_PANEL_IO_QSPI_CONFIG(cs, cb, cb_ctx) {  \
    .cs_gpio_num   = cs,                               \
    .dc_gpio_num   = -1,        /* QSPI: no D/C pin, command is in-band */ \
    .spi_mode      = 0,                                \
    .pclk_hz       = 40 * 1000 * 1000,                 \
    .trans_queue_depth = 10,                           \
    .lcd_cmd_bits  = 32,        /* <-- 32, not 8. This is the usual failure */ \
    .lcd_param_bits = 8,                               \
    .flags = { .quad_mode = true },                    \
}
```

**[SRC]** `artifacts/demo/.../Arduino/examples/08_LVGL_Test/esp_lcd_sh8601.h:97-111`

Call site, with the vendor's own 1-line-per-register init table passed as `vendor_config`:

```c
const spi_bus_config_t buscfg = SH8601_PANEL_BUS_QSPI_CONFIG(
    13, 15, 16, 17, 18,                    // PCLK, D0..D3
    360 * 360 * 16 / 8);                   // max transfer = one full frame
sh8601_vendor_config_t vendor_config = {
    .init_cmds      = lcd_init_cmds,       // ~60 entries, keep verbatim
    .init_cmds_size = sizeof(lcd_init_cmds)/sizeof(lcd_init_cmds[0]),
    .flags = { .use_qspi_interface = 1 },
};
const esp_lcd_panel_dev_config_t panel_config = {
    .reset_gpio_num = 21,
    .rgb_ele_order  = LCD_RGB_ELEMENT_ORDER_RGB,
    .bits_per_pixel = 16,
    .vendor_config  = &vendor_config,
};
```

**[SRC]** `.../08_LVGL_Test/lcd_bsp.c:212-245`; pins from `lcd_config.h:8-15` (CS 14, PCLK 13, D0-D3 15/16/17/18, RST 21, BL 47).

> **Gotcha — the `lcd_cmd_bits = 32` trap.** Point a stock 8-bit-command SPI driver at this panel and you get a blank or snowy screen with no error: the transfer succeeds, the panel just never recognises a command. If your display is dead and the bus is otherwise wired correctly, check this field first. Cross-referenced in [faq-and-troubleshooting.md](faq-and-troubleshooting.md#L261).

> **Gotcha — keep the init table with the panel.** The ~60-entry `lcd_init_cmds` array is panel-specific gamma/power tuning, not controller-generic. Copy it verbatim rather than substituting a generic table from another board. **[SRC]** `lcd_bsp.c:120-205`.

### 1.2 The 2-pixel rounding constraint — the non-obvious one

The panel's RAM addressing will not accept odd start or end coordinates. LVGL must be told to snap every dirty area to even boundaries, or you get **tearing, smearing, or a one-pixel diagonal drift** on partial redraws — which looks like an LVGL bug and is not.

```c
void example_lvgl_rounder_cb(struct _lv_disp_drv_t *drv, lv_area_t *area)
{
    // round START down to the nearest even number
    area->x1 = (area->x1 >> 1) << 1;
    area->y1 = (area->y1 >> 1) << 1;
    // round END up to the nearest odd number (i.e. even width/height)
    area->x2 = ((area->x2 >> 1) << 1) + 1;
    area->y2 = ((area->y2 >> 1) << 1) + 1;
}
disp_drv.rounder_cb = example_lvgl_rounder_cb;   // <-- easy to forget
```

**[SRC]** `.../08_LVGL_Test/lcd_bsp.c:351-366` (registration at `:260`).

> **Gotcha.** This is the thing most often lost when people port a working display setup from another board or move to LVGL 9. There is no runtime warning. If you write your own flush path, port `rounder_cb` with it.

### 1.3 Draw buffers and LVGL version

| | |
|---|---|
| **Library** | `lvgl/lvgl` **8.4.0**, `esp_lcd_sh8601` version `*` (unpinned by the vendor) |
| **Source** | **[SRC]** `artifacts/demo/.../ESP-IDF/08_LVGL_Test/main/idf_component.yml` |

```c
#define EXAMPLE_LVGL_BUF_HEIGHT (360 / 10)   // 36 lines = 1/10 screen

lv_color_t *buf1 = heap_caps_malloc(360 * 36 * sizeof(lv_color_t), MALLOC_CAP_DMA);
lv_color_t *buf2 = heap_caps_malloc(360 * 36 * sizeof(lv_color_t), MALLOC_CAP_DMA);
lv_disp_draw_buf_init(&disp_buf, buf1, buf2, 360 * 36);   // double-buffered, DMA-capable
```

**[SRC]** `lcd_bsp.c:251-255`. Two buffers of 360x36 px x 2 B = **25.9 KB each**, both `MALLOC_CAP_DMA`.

> **Gotcha — `MALLOC_CAP_DMA` is mandatory and it means internal RAM.** These two buffers take ~52 KB of internal DMA-capable RAM before your application allocates anything. You cannot move them to PSPIRAM without also handling the fact that the QSPI DMA engine needs DMA-capable memory. If you enlarge the buffers for smoother animation, watch internal-RAM headroom, not total heap.

The vendor's LVGL task runs at priority 2 with a 4 KB stack and a 2 ms tick (`lcd_config.h:18-23`) **[SRC]**. The 4 KB stack is tight — if you call file I/O or decode images from an LVGL callback, raise it.

### 1.4 Backlight

PWM via LEDC on **GPIO 47**, in `lcd_bl_pwm_bsp.c`. **[SRC]** `lcd_config.h:15`.

> **Gotcha — [INF]:** a backlight pin is itself an argument in the controller dispute. An SH8601 is an AMOLED driver and AMOLEDs have no backlight; this panel has one. See [gaps-and-conflicts.md](gaps-and-conflicts.md#L29). Practically: use the PWM path for dimming, and do not expect per-pixel-brightness AMOLED behaviour.

---

## 2. Touch

### 2.1 The reset sequence is the whole problem

CST816-family controller at **I2C `0x15`**, SDA **11**, SCL **12**, RST **10**, INT **9**. **[SRC]** `lcd_config.h:25-27` for address/SDA/SCL.

The reset timing that reliably brings the part up is **10 ms low / 10 ms high / 50 ms settle**:

```c
gpio_set_level(TP_RST, 0);  vTaskDelay(pdMS_TO_TICKS(10));
gpio_set_level(TP_RST, 1);  vTaskDelay(pdMS_TO_TICKS(10));
vTaskDelay(pdMS_TO_TICKS(50));          // <-- chip is NOT addressable before this
// only now will 0x15 ACK
```

**[COM]** — established in the Tasmota port discussion, [arendst/Tasmota #23737](https://github.com/arendst/Tasmota/discussions/23737) (2025-08-01). Short-changing the final 50 ms produces an intermittent "touch controller not found" that varies with build timing and supply ramp — i.e. it works on the bench and fails in the field.

### 2.2 The vendor driver polls and ignores INT

Waveshare's `cst816.cpp` never configures GPIO 9. It reads 7 bytes from register `0x00` on every LVGL input-device tick:

```c
uint8_t data[7];
I2C_read_buff(0x15, 0x00, data, 7);     // called from lv_indev read_cb — pure polling
```

**[SRC]** `.../08_LVGL_Test/cst816.cpp:55` — the file contains no `gpio_isr`, no INT pin reference, and no reset sequence at all.

> **Gotcha, two of them.**
> 1. **You get no power benefit and added latency.** The INT line *is* wired (GPIO 9). Attaching an ISR and reading only on assertion is straightforward and strictly better if you are running from battery.
> 2. **The vendor driver's init is buggy beyond the missing reset.** Do not treat `cst816.cpp` as a reference implementation. The specific defects are catalogued in **[../../../components/hynitron/cst816d/README.md](../../../components/hynitron/cst816d/README.md)** — read that before writing touch code.

### 2.3 Rotation is applied in software

If you `#define EXAMPLE_Rotate_90`, the touch coordinates are swapped in the LVGL callback (`data->point.x = tp_y; data->point.y = 360 - tp_x;`) *and* the panel gets MADCTL `0x36 = 0x60`. **[SRC]** `lcd_bsp.c:368-382` and `:200-204`. Change one without the other and touch is mirrored relative to the display — a classic self-inflicted bug on this board.

---

## 3. Encoders — the most misunderstood subsystem on this board

### 3.1 It is not a quadrature encoder

This is the single highest-value technique on the page, because **every assumption you carry over from a normal rotary encoder is wrong.**

The knob presents as **two independent detector switches** (Alps SSCM110100 — see [../../../components/alps-alpine/](../../../components/alps-alpine/)) on **GPIO 8 (`ECA`) and GPIO 7 (`ECB`)** **[SRC]** `ESP-IDF/04_Encoder_Test/main/user_config.h:11-12`.

Waveshare ships `bidi_switch_knob.c`, a fork of Espressif's `iot_knob` **with the quadrature state machine removed**. Each channel is debounced independently and each directly emits a direction event:

```c
static void knob_handler(knob_dev_t *knob)
{
    uint8_t pha = knob->hal_knob_level(knob->encoder_a);
    uint8_t phb = knob->hal_knob_level(knob->encoder_b);

    // Channel A -> RIGHT (+1).  Channel B -> LEFT (-1).  Independently.
    process_knob_channel(pha, &knob->encoder_a_level, &knob->debounce_a_cnt,
                         &knob->count_value, KNOB_RIGHT, true,  knob);
    process_knob_channel(phb, &knob->encoder_b_level, &knob->debounce_b_cnt,
                         &knob->count_value, KNOB_LEFT,  false, knob);
}
```

**[SRC]** `ESP-IDF/04_Encoder_Test/components/user_encoder_bsp/src/bidi_switch_knob.c:88-100`. There is no A-vs-B phase comparison anywhere in the file — direction comes solely from *which pin fired*.

Polling is a periodic `esp_timer` at **3 ms**, with a **2-tick debounce** (so ~6 ms to confirm an edge):

```c
#define TICKS_INTERVAL 3        // ms
#define DEBOUNCE_TICKS 2
esp_timer_start_periodic(s_knob_timer_handle, TICKS_INTERVAL * 1000U);
```

**[SRC]** same file, `:20-21` and `:152`.

> **Gotcha #1 — do not reach for a PCNT quadrature decoder.** It will not work. There is no phase relationship to decode.

> **Gotcha #2 — the ~30 pulses/sec ceiling.** `iot_knob` is *software* PCNT: a 3 ms timer with a 2-tick debounce cannot resolve events faster than roughly **30 per second**. Spin the knob briskly and you will drop counts. **[INF]** from the constants above.

> **Gotcha #3 — hardware PCNT is sitting unused.** Both MCUs have a hardware pulse counter peripheral. Because the channels are independent switch closures rather than quadrature, you can attach each channel to its own hardware PCNT unit (or a GPIO ISR) and remove the rate ceiling entirely. This is the highest-leverage change available to a project that cares about fast knob spins. **[INF]**

> **Gotcha #4 — the S3 sees only one encoder.** `EC2_A`/`EC2_B` are not connected to the S3 at all. **[SRC]** [pinouts-and-buses.md](pinouts-and-buses.md#L45).

---

## 4. Haptics — DRV2605L

### 4.1 Two separate defects in the vendor path

TI DRV2605L on the same I2C bus as touch (SDA 11, SCL 12) **[SRC]** `Arduino/examples/03_DRV2605_Test/03_DRV2605_Test.ino:7-11`. Deep-dive: [../../../components/texas-instruments/](../../../components/texas-instruments/).

**Defect 1 — the chip ID is `0x05`, and stock SensorLib rejects it.** The DRV2605L on this board reports status-register device ID `0x05` where the library expects `0x03`, so `drv.begin()` fails outright. **[COM]** — [lewisxhe/SensorLib #32](https://github.com/lewisxhe/SensorLib/issues/32), "DRV2605 ChipID 0x05", opened by `gilphilbert` 2026-01-19, closed 2026-01-22. You need the patched library or a locally widened ID check.

**Defect 2 — an ERM waveform library is selected for an LRA actuator, and nothing is ever calibrated.** The two vendor demos do not even agree with each other:

```c
drv.selectLibrary(1);   // Arduino demo  — ERM library A
drv.selectLibrary(5);   // ESP-IDF demo  — ERM library
```

**[SRC]** `Arduino/examples/03_DRV2605_Test/03_DRV2605_Test.ino:31` and `ESP-IDF/03_DRV2605_Test/components/i2c_equipment/i2c_equipment.cpp:50`.

Libraries 1-5 are **ERM** libraries; library **6** is the LRA library. An LRA is fitted. Neither demo calls auto-calibration — a repo-wide search for `Calibrat` in `ESP-IDF/03_DRV2605_Test/` returns only ADC-related `sdkconfig` lines **[SRC]**.

Minimal corrected pattern:

```c
drv.begin(Wire, DRV2605_SLAVE_ADDRESS, 11, 12);
drv.useLRA();               // tell the chip what is actually fitted
drv.selectLibrary(6);       // LRA library, not 1 or 5
// then run auto-calibration ONCE and persist the resulting
// A_CAL_COMP / A_CAL_BEMF / FEEDBACK registers to NVS
drv.setMode(DRV2605_MODE_INTTRIG);
drv.setWaveform(0, effect);
drv.setWaveform(1, 0);      // terminator
drv.go();
```

> **Gotcha.** Driving an LRA from an ERM library gives weak, buzzy, off-resonance haptics — it *works*, which is why the bug survived, but the actuator is being driven far from its resonant frequency. Auto-calibration is a once-per-device operation; run it, store the coefficients, and reload them at boot rather than calibrating on every start.

---

## 5. Audio — the subsystem neither MCU owns

### 5.1 The arbitration you cannot avoid

This is the board's sharpest architectural constraint and it is not a software problem you can code around:

- The **ESP32-S3 owns the mux select** (GPIO 0 → CH445P pin 15).
- The **ESP32-U4WDH owns `XSMT`**, the PCM5100A soft-mute, on its GPIO 32 — wired **directly to the DAC, bypassing the mux, with no pull resistor fitted**.

**Therefore neither MCU can produce sound by itself.** **[SRC]/[SCH]** [pinouts-and-buses.md §Audio arbitration](pinouts-and-buses.md#L125-L155).

Select polarity, resolved: **`IN`=0 → `S1` bank (U4WDH); `IN`=1 → `S2` bank (S3)**.

```c
// Hand the PCM5100A to the ESP32-S3.
gpio_set_level(GPIO_NUM_0, 1);
// ...but you are still muted until the U4WDH raises XSMT.
// A source handover MUST be coordinated over the inter-MCU UART (§7).
```

> **Gotcha — GPIO 0 is also the S3 BOOT strapping pin**, with a 10 k pull-up (`R58`) and a run to connector `CN1`. Driving it low early in boot, or wiring anything to `CN1` that loads it, affects entry to download mode. **[SCH]** [pinouts-and-buses.md](pinouts-and-buses.md#L13).

### 5.2 I2S TX and PDM RX

```c
// I2S standard TX -> PCM5100A (via the mux)
#define BCLK 39
#define WS   40
#define DOUT 41
// PDM RX <- microphone
#define PDM_CLK  45
#define PDM_DATA 46
```

**[SRC]** `ESP-IDF/07_Audio_Test/main/user_config.h:15-21`. Vendor runs 44.1 kHz / 16-bit **[SRC]** `components/audio_bsp/audio_bsp.c:22-23`.

> **Gotcha — no MCLK is routed to the PCM5100A.** It must run in BCK-derived PLL clocking mode, which **constrains the usable sample rates**. Do not assume an arbitrary rate will lock. See [PCM5100A §5](../../../components/texas-instruments/pcm5100a/README.md).

> **Gotcha — the demo's channel format is edited in place.** `audio_bsp.c:25` and `:27` both `#define I2S_CHANNEL_FORMAT`, mono then stereo; the later wins. Check which you are actually compiling. **[SRC]**

---

## 6. Storage — SDMMC

### 6.1 4-bit SDMMC, fixed pins

```c
sdmmc_slot_config_t slot = SDMMC_SLOT_CONFIG_DEFAULT();
slot.width = 4;
slot.clk = 4;  slot.cmd = 3;
slot.d0 = 5;   slot.d1 = 6;   slot.d2 = 42;  slot.d3 = 2;

esp_vfs_fat_sdmmc_mount_config_t mount = {
    .format_if_mount_failed = false,   // vendor default — see gotcha
    .max_files = 5,
};
esp_vfs_fat_sdmmc_mount(SDlist, &host, &slot, &mount, &card_host);
```

**[SRC]** `ESP-IDF/02_SD_Card/components/sdcard_bsp/sdcard_bsp.c:15-58`.

### 6.2 The three constraints that shape SD code on this board

**(a) 8.3 filenames only.** The vendor build sets `CONFIG_FATFS_LFN_NONE=y` with codepage 437. **[SRC]** `ESP-IDF/02_SD_Card/sdkconfig:1282-1288`.

> Long filenames silently truncate or fail to open. If your project reads user-supplied media, either enable `CONFIG_FATFS_LFN_HEAP` yourself or design around `MUSIC001.MP3`-style names. Note that enabling LFN costs RAM and, depending on codepage, can raise licensing questions on some FAT stacks.

**(b) No card-detect line.** Nothing tells you a card was inserted or removed. **[SRC]** — no CD pin appears in `sdcard_bsp.c` or the pin tables.

> You must poll by attempting a mount, and handle hot-removal by detecting I/O errors rather than an event. `format_if_mount_failed = false` is the right default: with it set to `true`, a transient read failure on a *good* card can reformat the user's media.

**(c) Factory apps expect fixed lowercase directories.** `music/`, `mjpeg/`, `pic/`, `txt/`, `fonts/`, `weather/`. **[SRC]** — layout recovered from the as-shipped SD archive, analysed in [factory-demo-apps.md](factory-demo-apps.md).

> Interoperating with the stock firmware means matching these exactly. Combined with (a), that means lowercase 8.3 names inside lowercase 8.3 directories.

**(d) SDMMC init can crash some stacks.** A reproducible MMC-mode init crash, plus a genuine listing of a factory card, is documented at [lvgl_micropython #547](https://github.com/lvgl-micropython/lvgl_micropython/issues/547). **[COM]**

---

## 7. Wireless and the inter-MCU link

### 7.1 Know which radio lives where

- **ESP32-S3: Wi-Fi + BLE only.** It has no Classic Bluetooth. This is a silicon fact, not a configuration.
- **Classic BT (A2DP etc.) lives on the ESP32-U4WDH**, the secondary MCU.

Full treatment: [classic-bluetooth.md](classic-bluetooth.md) and [dual-mcu-architecture.md](dual-mcu-architecture.md).

### 7.2 The link itself

Two wires, full duplex, **no flow control**: S3 **GPIO 38 TX** → U4WDH GPIO 18; U4WDH GPIO 23 → S3 **GPIO 48 RX**. **[SCH]** [pinouts-and-buses.md](pinouts-and-buses.md#L35-L43).

Framing is **pull-based**: the receiver requests a numbered packet with a `"Need packet:%d"` string and the sender replies. **[FW]** [dual-mcu-architecture.md §2.4](dual-mcu-architecture.md#24-the-protocol--what-is-known-and-what-is-not).

> **Gotcha — the baud rate is UNKNOWN and you must not guess.** No `.c/.h/.cpp/.ino` file in the entire demo tree contains `uart_driver_install`, `uart_param_config`, `uart_set_pin`, `UART_NUM_1`, `Serial1` or `Serial2`; every baud literal in the tree is a *console* baud (115200) in `sdkconfig` only. **Do not assume 115200 for the inter-MCU link** — that is a different UART on a different peripheral instance. Recover it with a logic analyser on GPIO 38/48 (minutes of work) before writing any protocol code. **[SRC]** [dual-mcu-architecture.md §2.3.1](dual-mcu-architecture.md#231-the-configured-baud-rate-is-unknown).

> **Gotcha — no RTS/CTS.** With no hardware flow control, a busy receiver drops bytes silently. The pull-based `"Need packet:%d"` framing exists precisely to provide application-level flow control; if you design your own protocol, you must supply an equivalent. **[INF]**

### 7.3 Power: the secondary MCU is a permanent ~50 mA load

The U4WDH is permanently powered from `3V3` with **no GPIO-controllable enable from the S3**, and draws **~50 mA continuously** running stock firmware. Flashing it a deep-sleep image drops it to **~10 µA** — a 5,000x reduction. **[COM]** `svwhisper/lyngdorf-secondary-sleep`, corroborated independently by `joshuacant/BlueKnob`; see [examples/catalog.md §1.2](examples/catalog.md).

> **Technique.** If your project does not use Classic Bluetooth, the single most effective battery optimisation available is to flash the secondary MCU with a deep-sleep image. It dominates every other idle-power decision you can make on the S3 side. Back up the factory image first — [dual-mcu-architecture.md §6.2](dual-mcu-architecture.md#62--back-up-the-factory-esp32-image-before-you-touch-it).

### 7.4 Flashing: USB-C orientation selects the target

Which MCU enumerates depends on **USB-C plug orientation**. The U4WDH is reached through a CH340X bridge; the S3 through native USB. Procedure and risks: [dual-mcu-architecture.md §1](dual-mcu-architecture.md#1-the-usb-c-orientation-flip).

> **Gotcha — the U4WDH has no OTA partition layout.** It can only be updated over USB-C serial. There is no field-update path for the secondary MCU unless you build one. **[FW]** [dual-mcu-architecture.md §5](dual-mcu-architecture.md#5-ota-the-s3-can-the-u4wdh-cannot).

---

## Related

- [pinouts-and-buses.md](pinouts-and-buses.md) — authoritative pin tables for both MCUs
- [dual-mcu-architecture.md](dual-mcu-architecture.md) — the two-chip design in full
- [project-ideas.md](project-ideas.md) — what these techniques let you build, and what they rule out
- [faq-and-troubleshooting.md](faq-and-troubleshooting.md) — symptom-first index
- [gaps-and-conflicts.md](gaps-and-conflicts.md) — what is still unresolved
- [examples/catalog.md](examples/catalog.md) — 28 catalogued community projects
