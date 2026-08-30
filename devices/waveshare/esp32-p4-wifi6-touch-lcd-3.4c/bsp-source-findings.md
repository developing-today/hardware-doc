# Findings extracted from the official BSP source

> Compiled **2026-08-26** from `waveshareteam/Waveshare-ESP32-components`,
> `bsp/esp32_p4_wifi6_touch_lcd_xc/` (Apache-2.0, repo 74★, last push 2026-08-25).
>
> Local copy: `archive/scratch/esp32-p4-wifi6-touch-lcd-xc/bsp-source/`
>
> This BSP was found on 2026-08-26 by **code search**, after earlier passes had recorded it as
> *"resolved by the Component Manager, not vendored"* and stopped. It is the single most
> authoritative software artifact for this board — Waveshare's own board-support implementation —
> and it settled several open questions.

## Why this document exists

The research method says facts should be extracted from artifacts into authored documents, so that
future work does not depend on reopening the artifact. These are the facts worth having in prose.

Nothing here was run. Everything is read from source.

---

## 1. Sixteen GPIO assignments, independently confirmed

`include/bsp/esp32_p4_wifi6_touch_lcd_xc.h`:

| BSP define | GPIO | Matches |
|---|---:|---|
| `BSP_I2C_SDA` / `BSP_I2C_SCL` | 7 / 8 | ✅ schematic |
| `BSP_I2S_MCLK` / `SCLK` / `LCLK` / `DOUT` / `DSIN` | 13 / 12 / 10 / 9 / 11 | ✅ schematic + demo |
| `BSP_POWER_AMP_IO` | 53 | ✅ |
| `BSP_LCD_BACKLIGHT` | 26 | ✅ |
| `BSP_LCD_RST` | 27 | ✅ |
| `BSP_SD_D0`–`D3` | 39, 40, 41, 42 | ✅ |
| `BSP_SD_CMD` / `BSP_SD_CLK` | 44 / 43 | ✅ |

Every value matches the pinout derived by reading the schematic PDF visually. That is now **three
independent derivations** in agreement — this record's schematic read, Waveshare's `docs/HARDWARE.md`,
and the BSP implementation.

Note `BSP_I2S_LCLK` is the WS/LRCK signal; the naming differs from the demos' `I2S_WS_IO`.

## 2. The backlight polarity contradiction — resolved

An apparent conflict had been sitting unnoticed:

- ESP-IDF demos set `TEST_LCD_BK_LIGHT_ON_LEVEL (0)` → **active low**
- The Linux port says *"P4 GPIO26, active-low"* → **active low**
- But `bsp_display_brightness_set()` computes `duty = (1023 * percent) / 100` → **higher duty = brighter**, which reads as active-high

The resolution is in `bsp_display_brightness_init()`:

```c
const ledc_channel_config_t LCD_backlight_channel = {
    .gpio_num = BSP_LCD_BACKLIGHT,
    .duty     = 0,
    .flags    = { .output_invert = 1 },     // <-- inverted in hardware
};
```

**The LEDC peripheral inverts the output.** So the pin really is active-low, while the API is
intuitive — `bsp_display_brightness_set(100)` gives full brightness.

**Practical consequence:** if you drive GPIO26 yourself with `gpio_set_level()` or your own LEDC
channel, you must invert. If you use the BSP, do not. Mixing the two — BSP init plus manual GPIO
writes — produces a backlight that behaves backwards.

Backlight PWM parameters: **LEDC low-speed mode, timer 1, 10-bit resolution (0–1023), 5 kHz**.

## 3. microSD is on **slot 0**, and power comes from an on-chip LDO

```c
host.slot         = SDMMC_HOST_SLOT_0;
host.max_freq_khz = SDMMC_FREQ_HIGHSPEED;          // 40 MHz

sd_pwr_ctrl_ldo_config_t ldo_config = { .ldo_chan_id = 4 };
sd_pwr_ctrl_new_on_chip_ldo(&ldo_config, &pwr_ctrl_handle);
host.pwr_ctrl_handle = pwr_ctrl_handle;

const sdmmc_slot_config_t slot_config = {
    /* SD card is connected to Slot 0 pins. Slot 0 uses IO MUX, so not specifying the pins here */
    .cd = SDMMC_SLOT_NO_CD,
    .wp = SDMMC_SLOT_NO_WP,
    .width = 4,
};
```

Four findings here:

**Slot 0.** This independently corroborates the Linux port's claim that the P4 exposes one DW-MMC
host with the card on **slot 0** and the ESP32-C6 link on **slot 1**. Two unrelated sources, same
mechanism. It strengthens the case that microSD and Wi-Fi genuinely contend.

**Slot 0 uses IO MUX**, which is why the pins are fixed and the BSP does not specify them — the
comment says so explicitly. It also explains why the demo's generic Kconfig pin defaults happened
to be right.

**Power is an on-chip LDO, channel 4** — not a GPIO. This refines the earlier
[C13](./gaps-and-conflicts.md#c13--microsd-sits-on-a-switched-rail-no-demo-enables) finding. The
schematic shows an AO3401 P-MOSFET on `SD1_VDD` gated by GPIO45; the BSP powers the card through
the SoC's internal LDO instead and never touches GPIO45.

> **Unresolved tension.** Two power paths appear to exist: an internal LDO (used by the BSP) and an
> external switch on GPIO45 (present on the schematic, driven by nothing). Either the external
> switch defaults on, or it controls a different rail than assumed. **The BSP works without
> touching GPIO45**, which suggests the former — but this is inference, and worth confirming on
> hardware before relying on either.

**Card detect is not used** — `SDMMC_SLOT_NO_CD` — consistent with the schematic's card-detect net
never having been traced to a GPIO.

## 4. Touch: address probing, exactly as documented

```c
if (ESP_OK == bsp_i2c_device_probe(ESP_LCD_TOUCH_IO_I2C_GT911_ADDRESS))        // 0x5D
    ...
else if (ESP_OK == bsp_i2c_device_probe(ESP_LCD_TOUCH_IO_I2C_GT911_ADDRESS_BACKUP))  // 0x14
    ESP_LOGI(TAG, "Touch 0x14 found");
```

Probing uses `i2c_master_probe(i2c_handle, addr, 100)` — a 100 ms timeout.

The header confirms the deliberate omissions:

```c
#define BSP_LCD_TOUCH_RST     (GPIO_NUM_NC)
#define BSP_LCD_TOUCH_INT     (GPIO_NUM_NC)
```

Both `GPIO_NUM_NC`, in the vendor's own **library** — not merely in its demos. That upgrades
[C11](./gaps-and-conflicts.md#c11--touch-interrupt-is-not-wired-to-the-soc) from "the demos poll" to
"the entire vendor software stack polls, by design".

Touch coordinate limits are set from the panel: `.x_max = BSP_LCD_H_RES`, `.y_max = BSP_LCD_V_RES`
— so selecting the wrong variant macro mis-scales touch as well as display.

## 5. What the vendor says is *not* fitted

```c
#define BSP_CAPS_DISPLAY        1
#define BSP_CAPS_TOUCH          1
#define BSP_CAPS_AUDIO          1
#define BSP_CAPS_AUDIO_SPEAKER  1
#define BSP_CAPS_AUDIO_MIC      1
#define BSP_CAPS_SDCARD         1
#define BSP_CAPS_BUTTONS        0     // <-- no user buttons
#define BSP_CAPS_IMU            0     // <-- no IMU
```

**`BSP_CAPS_BUTTONS 0`** is worth noting: the board has BOOT and RESET buttons, but the BSP exposes
no user-pressable button API. Do not expect a button abstraction.

**`BSP_CAPS_IMU 0`** settles a question the capability list might otherwise raise — there is no
inertial sensor on this board, unlike some sibling Waveshare boards.

## 6. Display configuration

```c
.dpi_clock_freq_mhz = 80,
.num_fbs            = CONFIG_BSP_LCD_DPI_BUFFER_NUMS,   // default 3, range 1-3
.video_timing = {
    .h_size = BSP_LCD_H_RES,  .v_size = BSP_LCD_V_RES,
    .hsync_back_porch = 20, .hsync_pulse_width = 20, .hsync_front_porch = 40,
    .vsync_back_porch = 12, .vsync_pulse_width =  4, .vsync_front_porch = 24,
}
```

Timings match the demos exactly, and are **identical across both variants** — confirming
[C4](./gaps-and-conflicts.md#c4--dsi-porch-timings-are-not-derived-per-panel) from a third source.

**Frame buffers default to 3**, not 1 as in the standalone demos. The Kconfig help says:

> *"Let DPI LCD driver create a specified number of frame-size buffers. Only when it is set to
> multiple can the avoiding tearing be turned on."*

At 800 × 800 × 24 bpp that is roughly **5.8 MB of PSRAM** for three buffers. Affordable in 32 MB,
but it is bandwidth as well as capacity — relevant when running the camera concurrently.

**Colour format is selectable**: `BSP_LCD_COLOR_FORMAT_RGB565` (default) or `RGB888`. The demos use
24 bpp; the BSP defaults to **16 bpp**, which halves framebuffer bandwidth. That default difference
is easy to miss when comparing demo behaviour to BSP behaviour.

LVGL adapter defaults: `ESP_LV_ADAPTER_TEAR_AVOID_MODE_TRIPLE_PARTIAL`, rotation 0,
`enable_ppa_accel = false` — **the pixel-processing accelerator is off by default**, which is a
performance lever nobody has measured.

## 7. Audio

- I²S standard mode, **Philips slot format, 16-bit, mono**, master role
- Separate TX and RX channel handles — `i2s_tx_chan`, `i2s_rx_chan` — so **full duplex is wired up**
- ES8311 at `ES8311_CODEC_DEFAULT_ADDR`, ES7210 at `ES7210_CODEC_DEFAULT_ADDR`

The RX path exists in the BSP even though **no official example exercises capture**. So the ES7210
is supported in the library; it is only the demonstration that is missing. That materially softens
the "audio capture is the least-evidenced feature" concern — the code is there to read.

## 8. I²C clock — the 100/400 kHz question answered

`Kconfig`:

```
config BSP_I2C_FAST_MODE
    bool "Enable I2C fast mode"
    default y
config BSP_I2C_CLK_SPEED_HZ
    default 400000 if BSP_I2C_FAST_MODE
    default 100000
```

**400 kHz is the vendor default**, with 100 kHz available by disabling fast mode. That resolves
[C8](./gaps-and-conflicts.md#c8--i²c-clock-rate--resolved-2026-08-26): the two
values seen in Waveshare's Arduino code were not a contradiction but the same choice, expressed as
a build option. 400 kHz is intended; 100 kHz is the documented fallback.

Worth remembering that four device families share this bus, so if you add peripherals on `J6` or
`J8`, dropping to 100 kHz is a supported first diagnostic.

## Summary of what this artifact settled

| Question | Before | After |
|---|---|---|
| Pin map correctness | Two sources | **Three sources agree** |
| Backlight polarity | Apparent contradiction | **LEDC `output_invert = 1`** |
| microSD slot | Unknown | **Slot 0**, IO MUX, corroborates one-DW-MMC-host |
| SD power | GPIO45 external switch | **On-chip LDO ch 4**; GPIO45 untouched — tension noted |
| Touch INT/RST | Demos leave NC | **The library itself defines them `GPIO_NUM_NC`** |
| I²C 100 vs 400 kHz | Conflict | **Build option; 400 kHz default** |
| Frame buffers | Demo used 1 | **BSP defaults to 3**, for tear avoidance |
| Colour depth | Demo 24 bpp | **BSP defaults RGB565** |
| ES7210 capture | No example | **RX channel implemented in the BSP** |
| IMU / buttons | Unstated | **Explicitly `0` — not fitted** |

## 9. Empirical cross-check against real projects

Four independent working projects were inspected on 2026-08-26 — three that build against this BSP,
plus **XiaoZhi**, a widely-forked Chinese AI voice-assistant firmware that carries a
`main/boards/waveshare/esp32-p4-wifi6-touch-lcd/` board definition (62 code hits across forks).

| Setting | traviscea (3.4C) | garagetinkering (3.4C) | fabkury (4C) | BSP default |
|---|---|---|---|---|
| I²C fast mode | `y`, **400000** | `y`, **400000** | `y`, **400000** | `y`, 400000 |
| Colour format | RGB565 | RGB565 | **RGB888** | RGB565 |
| Frame buffers | **1** | 3 | 3 | 3 |
| Brightness LEDC ch | 1 | 1 | 1 | 1 |

**Every project runs I²C at 400 kHz.** Nobody falls back to 100 kHz — strong practical support for
the [C8](./gaps-and-conflicts.md#c8--i²c-clock-rate--resolved-2026-08-26) resolution, on a bus
carrying four device families.

**Both colour formats and 1–3 frame buffers are in real use**, so neither is a hidden constraint.

### XiaoZhi independently confirms the pin map — and the inversion

Board-common section:

```c
#define AUDIO_I2S_GPIO_MCLK   GPIO_NUM_13     #define AUDIO_I2S_GPIO_BCLK  GPIO_NUM_12
#define AUDIO_I2S_GPIO_WS     GPIO_NUM_10     #define AUDIO_I2S_GPIO_DOUT  GPIO_NUM_9
#define AUDIO_I2S_GPIO_DIN    GPIO_NUM_11     #define AUDIO_CODEC_PA_PIN   GPIO_NUM_53
#define AUDIO_CODEC_I2C_SDA_PIN GPIO_NUM_7    #define AUDIO_CODEC_I2C_SCL_PIN GPIO_NUM_8
#define BOOT_BUTTON_GPIO      GPIO_NUM_35
```

Per-variant blocks, extracted from the `#elif CONFIG_BOARD_TYPE_…` chain:

```c
/* ..._LCD_3_4C */                        /* ..._LCD_4C */
#define DISPLAY_WIDTH  (800)              #define DISPLAY_WIDTH  (720)
#define DISPLAY_HEIGHT (800)              #define DISPLAY_HEIGHT (720)
#define PIN_NUM_LCD_RST GPIO_NUM_27       #define PIN_NUM_LCD_RST GPIO_NUM_27
#define DISPLAY_BACKLIGHT_PIN GPIO_NUM_26 #define DISPLAY_BACKLIGHT_PIN GPIO_NUM_26
#define DISPLAY_BACKLIGHT_OUTPUT_INVERT true   /* same */
#define LCD_MIPI_DSI_LANE_BITRATE_MBPS (1500)  /* same */
```

> **Care needed reading this file.** It is one `#elif` chain covering **nine** Waveshare P4 boards
> (4B, 4.3, 5, 7B, 3.4C, 4C, 7, 8, 10.1). Other variants use `GPIO_NUM_33`/`GPIO_NUM_32` for reset
> and backlight — grepping the file without isolating the right block attributes another board's
> pins to this one. I nearly made exactly that error.

A **fourth** independent source for the audio, I²C and display pins — and it sets
`DISPLAY_BACKLIGHT_OUTPUT_INVERT true`, corroborating §2 from a project that does not use the BSP
at all.

It also contributes something new: **`BOOT_BUTTON_GPIO GPIO_NUM_35`**. The BSP declares
`BSP_CAPS_BUTTONS 0`, so this is the only source found that maps the BOOT button — usable as a
general-purpose input once the bootloader has run.

And it runs audio at **24 kHz in and out with `AUDIO_INPUT_REFERENCE true`**, i.e. ES7210 capture
with an AEC reference channel actually configured — the closest thing to a working capture example
found anywhere.

### Nobody drives GPIO45 or GPIO33

A code search for `GPIO_NUM_45` alongside this board returned **zero** results, and no inspected
project references `BL_EN`.

So across the vendor BSP, the vendor demos, a Linux port, XiaoZhi and three application projects,
**not one touches the SD power switch or the backlight enable.** That is meaningful negative
evidence: both rails are almost certainly default-on, and
[C12](./gaps-and-conflicts.md#c12--backlight-has-two-controls-and-the-demos-use-only-one) /
[C13](./gaps-and-conflicts.md#c13--microsd-sits-on-a-switched-rail-no-demo-enables) are unlikely to
bite in practice.

It remains *negative* evidence — nobody driving a pin is not proof it never needs driving — but the
sample is now broad enough to lower the risk considerably.

## 9. Empirical cross-check against real projects

Inspected on 2026-08-26: three application projects that build against this BSP, plus **XiaoZhi**
(`78/xiaozhi-esp32`), a widely-forked Chinese AI voice-assistant firmware that carries a dedicated
`main/boards/waveshare/esp32-p4-wifi6-touch-lcd/` board definition — **62 code hits across forks**.

### What real projects actually configure

| Setting | traviscea (3.4C) | garagetinkering (3.4C) | fabkury (4C) | BSP default |
|---|---|---|---|---|
| I²C fast mode / speed | `y` / **400000** | `y` / **400000** | `y` / **400000** | `y` / 400000 |
| Colour format | RGB565 | RGB565 | **RGB888** | RGB565 |
| Frame buffers | **1** | 3 | 3 | 3 |
| Brightness LEDC channel | 1 | 1 | 1 | 1 |

**All three run I²C at 400 kHz.** Nobody falls back to 100 kHz, on a bus carrying four device
families — practical support for the [C8](./gaps-and-conflicts.md#c8--i²c-clock-rate--resolved-2026-08-26)
resolution. Both colour formats and 1–3 frame buffers are in real use, so neither is a hidden
constraint.

### XiaoZhi: a fourth independent pin source

It does **not** use the Waveshare BSP, yet arrives at identical values:

```c
#define AUDIO_I2S_GPIO_MCLK  GPIO_NUM_13   #define AUDIO_I2S_GPIO_BCLK GPIO_NUM_12
#define AUDIO_I2S_GPIO_WS    GPIO_NUM_10   #define AUDIO_I2S_GPIO_DOUT GPIO_NUM_9
#define AUDIO_I2S_GPIO_DIN   GPIO_NUM_11   #define AUDIO_CODEC_PA_PIN  GPIO_NUM_53
#define AUDIO_CODEC_I2C_SDA_PIN GPIO_NUM_7 #define AUDIO_CODEC_I2C_SCL_PIN GPIO_NUM_8
```

and per variant:

| | 3.4C | 4C |
|---|---|---|
| Resolution | 800 × 800 | 720 × 720 |
| `PIN_NUM_LCD_RST` | **27** | **27** |
| `DISPLAY_BACKLIGHT_PIN` | **26** | **26** |
| `DISPLAY_BACKLIGHT_OUTPUT_INVERT` | **`true`** | **`true`** |
| `LCD_MIPI_DSI_LANE_BITRATE_MBPS` | **1500** | **1500** |

That independently corroborates the pin map, the **1500 Mbps lane rate**, and — from a project that
never touches the BSP — the **active-low backlight** of §2.

### Two things only XiaoZhi provides

**`BOOT_BUTTON_GPIO GPIO_NUM_35`.** The BSP declares `BSP_CAPS_BUTTONS 0` and maps no buttons, so
this is the **only source found that identifies the BOOT button's GPIO** — usable as a
general-purpose input after boot.

**A working audio-capture configuration**: 24 kHz in *and* out with `AUDIO_INPUT_REFERENCE true`,
i.e. ES7210 capture with an AEC reference channel. Given no official example exercises capture,
this is the closest thing to a reference implementation found anywhere.

### Nobody drives GPIO45 or GPIO33

A code search for `GPIO_NUM_45` alongside this board returns **zero** results, and no inspected
project references `BL_EN`.

Across the vendor BSP, the vendor demos, a Linux port, XiaoZhi and three application projects,
**not one touches the SD power switch or the backlight enable.** Both rails are therefore almost
certainly default-on, and [C12](./gaps-and-conflicts.md#c12--backlight-has-two-controls-and-the-demos-use-only-one)
/ [C13](./gaps-and-conflicts.md#c13--microsd-sits-on-a-switched-rail-no-demo-enables) are unlikely
to bite in practice.

This is *negative* evidence — nobody driving a pin is not proof none is needed — but the sample is
now broad enough to lower the risk substantially.

## Reacquire

```bash
git clone https://github.com/waveshareteam/Waveshare-ESP32-components.git
# bsp/esp32_p4_wifi6_touch_lcd_xc/
```

Or take the published component, which is what your build will actually resolve:

```yaml
dependencies:
  waveshare/esp32_p4_wifi6_touch_lcd_xc: "3.0.1"
```

> The repository is `master` branch and moves. The local copy under
> `scratch/esp32-p4-wifi6-touch-lcd-xc/bsp-source/` is the 2026-08-26 state. Published component
> versions (`3.0.1` etc.) are the stable reference; the repository is the readable one.

## Related

- [Pinouts and buses](./pinouts-and-buses.md) · [Gaps and conflicts](./gaps-and-conflicts.md)
- [Official repo and community](./official-repo-and-community.md)
- [How this was found](../../../guides/research/finding-projects-that-use-a-board.md)
