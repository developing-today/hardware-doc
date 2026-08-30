# OmniVision OV5640

> 5-megapixel CMOS image sensor with an on-chip ISP, DVP and MIPI CSI-2 outputs, an embedded microcontroller for autofocus, and a register set so large that essentially nobody programs it from the datasheet.
> Research snapshot **2026-08-30**. Fitted to the Seeed XIAO ESP32S3 Sense in its OV5640 variant. **No hardware was available.**

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DS]** | OV5640 datasheet **version 2.03** — `artifacts/ov5640-datasheet-v2.03.pdf` (symlink into `shared-assets/`) |
| **[AN]** | *OV5640 Auto Focus Camera Module Application Notes (with DVP Interface)*, document **revision 2.13**, last modified 4 Nov 2011 — `artifacts/ov5640-software-application-notes.pdf` |
| **[DRV]** | `espressif/esp32-camera` **v2.0.15**, `sensors/ov5640.c`, `driver/include/sensor.h`, `driver/sccb.c` |
| **[DEV]** | Seeed XIAO ESP32S3 Sense device record and its schematics |
| **[INF]** | Author inference |

---

## 1. Identity and variants

| Property | Value | Source |
|---|---|---|
| Part | **OV5640** | [DS] |
| Resolution | 2592 × 1944 (**5 MP**) | [DS] |
| Optical format | **1/4"** | [DS] |
| Outputs | **8/10-bit DVP** (parallel) **and 2-lane MIPI CSI-2** | [DS] |
| Control interface | **SCCB** (I²C-like) | [DS] |
| SCCB 7-bit address | **`0x3C`** (write `0x78`, read `0x79`) | [DRV] `sensor.h`: `OV5640_SCCB_ADDR = 0x3C, // 0x78 >> 1` |
| Chip ID | **`0x5640`**, read as 16-bit from register **`0x300A`** (high) / `0x300B` (low) | [DRV] `ov5640.c:1079` |
| On-chip ISP | Yes — AWB, AEC/AGC, defect correction, lens shading, gamma, denoise, scaler | [DS] |
| Autofocus | **Yes**, via an embedded microcontroller + VCM driver | [AN] §4.10.1 |
| Datasheet status | **Released PRODUCT SPECIFICATION** (contrast the OV3660's "PRELIMINARY") | [DS] |
| Lifecycle | Mature/legacy. Circa 2011 silicon, still in volume production through module houses | [INF] |

> ⚠ **`0x3C` is shared with the OV3660.** Both answer at the same SCCB address, so probing the bus tells you nothing. You **must** read the 16-bit chip ID at `0x300A`. This is exactly what `esp32-camera` does, and it is why its autodetect works.

> ⚠ **Do not confuse OV5640 with OV5647.** The OV5647 is the Raspberry Pi Camera v1 sensor — a different part, MIPI-only, no embedded AF microcontroller. The confusion is widespread; even OmniVision's own AF application note contains the typo, referring to *"the built-in micro-controller of OV5647"* in a document titled for the OV5640 **[AN] §4.10.1**. The Seeed-distributed AF library likewise unpacks to a directory named `OV5647_AF-main` while its contents are entirely OV5640 — see [DEV] `features/camera.md`.

---

## 2. Resolution and frame-rate matrix

Sensor-level capability **[DS]**:

| Mode | Resolution | Max frame rate |
|---|---|---:|
| QSXGA / full | 2592 × 1944 | **15 fps** |
| 1080p | 1920 × 1080 | 30 fps |
| 720p | 1280 × 720 | 60 fps |
| XGA | 1024 × 768 | 30 fps |
| VGA | 640 × 480 | 90 fps |
| QVGA | 320 × 240 | 120 fps |

These are the *sensor's* numbers over a suitably fast interface. On an ESP32-S3 over 8-bit DVP the ceiling is the parallel bus and the JPEG encoder, not the sensor — see §6.3.

`esp32-camera` exposes the sizes through `framesize_t` **[DRV]** `sensor.h`; the OV5640 supports the whole ladder up to `FRAMESIZE_5MP` (2592×1944), plus `FRAMESIZE_QSXGA` (2560×1920), `FRAMESIZE_WQXGA` (2560×1600), `FRAMESIZE_QHD` (2560×1440) and the portrait variants `FRAMESIZE_P_FHD` (1080×1920) and `FRAMESIZE_P_HD` (720×1280).

---

## 3. Interfaces

### 3.1 DVP vs MIPI — the choice is made by the module, not by you

The OV5640 die supports both. Which one you get is decided by the camera module's flex and the sensor's `0x300E` / `0x4800` configuration:

| | **DVP (parallel)** | **MIPI CSI-2** |
|---|---|---|
| Pins | ~12 (D0–D9, PCLK, HREF, VSYNC) + XCLK + 2 SCCB | 2 data lanes + clock lane, differential |
| Host support | ESP32/ESP32-S3 LCD_CAM, most MCUs with a camera peripheral | Needs a real CSI-2 receiver — ESP32-P4, i.MX, Rockchip, RPi |
| Practical ceiling | Limited by PCLK × bus width | Much higher |
| Cable | Wide, EMI-prone, short | Two differential pairs |
| On the XIAO Sense | **DVP** | not used |

For ESP32-S3 work, DVP is the only option; `esp32-camera` is a DVP driver.

### 3.2 SCCB — it is I²C, with two traps

SCCB is OmniVision's I²C variant. In practice a standard I²C master drives it, which is what `esp32-camera` does **[DRV]** `driver/sccb.c:118–160`, shifting the 7-bit address left and OR-ing the R/W bit like any I²C transaction.

The two things that differ from ordinary I²C:

1. **The OV5640 uses 16-bit register addresses.** The register space runs to `0x6100`-ish, so a write is `[addr_hi][addr_lo][data]` and a read is a two-byte address write, a repeated start, then a one-byte read. `esp32-camera` provides `SCCB_Read16` / `SCCB_Write16` separately from the 8-bit versions used for the OV2640 **[DRV]**. A driver that assumes 8-bit register addresses (as an OV2640 driver would) fails immediately.
2. **Classic SCCB does not require the peripheral to ACK**, and some OmniVision parts do not drive ACK on the final byte. The OV5640 behaves well enough with a normal I²C master that this is rarely a problem in practice, but it is why bit-banged SCCB implementations exist.

### 3.3 Clocking

The sensor needs an external **XCLK**; it has no internal oscillator. The internal PLL multiplies it up for the pixel clock.

- Nominal input range is **6–27 MHz** **[DS]**; **24 MHz** is the reference value most module datasheets and init tables assume.
- `esp32-camera` generates XCLK with an **LEDC channel and timer** — by convention `LEDC_CHANNEL_0` / `LEDC_TIMER_0` **[DEV]** `features/camera.md`. That is a real resource cost: if your application also uses `ledcWrite` for servos or backlight, avoid channel 0 and timer 0.
- The XIAO Sense reference configuration uses `xclk_freq_hz = 20000000` **[DEV]**.
- ⚠ **XCLK frequency is the first thing to lower when frames come back green, pink or torn.** Dropping to 10 MHz costs frame rate and frequently fixes marginal FPC connections and long ribbon cables **[DEV]** `features/camera.md`.

---

## 4. Register set, and why everyone uses vendor init tables

The OV5640 register map spans roughly `0x3000`–`0x6100` — on the order of **twelve thousand** addressable registers, of which several hundred matter. `esp32-camera`'s own commented-out debug helper hints at the scale **[DRV]** `ov5640.c:75`:

```c
//// dump_range(sensor, "All Regs", 0x3000, 0x6100);
//// dump_range(sensor, "system and IO pad control", 0x3000, 0x3052);
```

Functional blocks, by address range **[DS]**:

| Range | Block |
|---|---|
| `0x3000`–`0x3052` | System and I/O pad control, clock enables, chip ID, software reset |
| `0x3100`–`0x31FF` | SCCB control |
| `0x3200`–`0x32FF` | SRB (auto-focus VCM control) |
| `0x3400`–`0x3406` | AWB gain manual control |
| `0x3500`–`0x350D` | AEC/AGC — exposure and gain |
| `0x3600`–`0x36FF` | Analog / sensor core control (largely undocumented magic numbers) |
| `0x3700`–`0x37FF` | Timing control |
| `0x3800`–`0x3821` | **Timing: output window, cropping, binning, mirror/flip** |
| `0x3A00`–`0x3A25` | AEC/AGC control — banding filter, target luminance |
| `0x3C00`–`0x3C1E` | 50/60 Hz light-frequency auto-detection |
| `0x4000`–`0x4033` | BLC (black level calibration) |
| `0x4300`–`0x430D` | Format control — the output format select |
| `0x4400`–`0x4407` | JPEG control |
| `0x4740`–`0x4745` | DVP polarity control |
| `0x4800`–`0x4837` | MIPI control |
| `0x5000`–`0x5063` | **ISP top control** — enable/disable each ISP block |
| `0x5180`–`0x51D0` | AWB |
| `0x5300`–`0x530F` | CIP (sharpening/denoise) |
| `0x5380`–`0x538B` | CMX (colour matrix) |
| `0x5480`–`0x5490` | Gamma |
| `0x5580`–`0x558C` | SDE (special digital effects — brightness, contrast, saturation, hue) |
| `0x5800`–`0x583D` | LENC (lens shading correction) |
| `0x5A00`–`0x5A04` | AVG (average window) |
| `0x5B00`–`0x5B06` | LEC |

**Why vendor init tables are universal.** The `0x3600`–`0x37FF` analog block is essentially undocumented — the datasheet lists the addresses but not the meaning of most bits. Those registers carry process-dependent bias and timing trims that OmniVision supplies as opaque sequences to module makers. There is no way to derive them. Every working OV5640 driver in existence therefore begins with a several-hundred-entry `{reg, value}` table inherited from an OmniVision reference, and only the registers *after* that table (window, format, ISP enables, AEC targets) are set from documented meanings.

Practical consequence: **do not attempt a from-scratch OV5640 bring-up.** Start from `esp32-camera`'s `ov5640_settings.h` (or the Linux `ov5640.c` tables), get a picture, then change documented registers one at a time.

---

## 5. Autofocus — the firmware upload **[AN] §4.10]**

This is the OV5640's distinguishing feature and its biggest operational gotcha.

**The mechanism.** Autofocus is executed by a **microcontroller embedded in the OV5640**, which reads focus statistics from the sensor, computes a lens position and drives the VCM through the on-chip driver. The host does not run the AF algorithm. But:

> **"The firmware of micro-controller is downloaded from host."** — [AN] §4.10.1

The AF firmware is **not in ROM**. It must be uploaded over SCCB **at every power-up**, exactly like an init table. Without it, the sensor works perfectly as a fixed-focus camera and every AF command silently does nothing.

**The command interface [AN] §4.10.2]** — three registers, real values:

| Register | Address | Meaning |
|---|---|---|
| **`CMD_MAIN`** | **`0x3022`** | `0x03` trigger single autofocus · `0x06` pause AF (hold current position) · `0x08` release focus (lens to infinity) · `0x12` re-launch focus zones · `0x00` command finished |
| **`CMD_ACK`** | **`0x3023`** | `0x00` command finished · `0x01` command running |
| **`FW_STATUS`** | **`0x3029`** | `0x7F` **S_FIRMWARE** — firmware downloaded but not running (cause 1: MCU off; cause 2: firmware incorrect) · `0x7E` **S_STARTUP** — initialising · `0x70` **S_IDLE** — focus released, lens at furthest position · `0x00` **S_FOCUSING** · `0x10` **S_FOCUSED** — complete |

The MCU auto-clears `CMD_MAIN` on receipt and `CMD_ACK` on completion **[AN]**.

**The sequence [AN] §4.10.3–4.10.6]:**

```
1. Initialise the sensor normally (main init table).

2. Download the AF firmware — "same as download the initial setting".
   I²C multi-byte (burst) writes are strongly recommended for speed. [AN §4.10.4]

3. Verify the MCU actually came up:
      MCU on:  0x3000 bit6 = 0, bit5 = 0
               0x3004 bit6 = 1, bit5 = 1
      AFC on:  0x3001 bit6 = 0
               0x3005 bit6 = 1
   Then poll FW_STATUS (0x3029) until it leaves 0x7F.

4. To focus (before capture):
      write 0x3022 = 0x03          # single autofocus
      poll  0x3029 until == 0x10   # S_FOCUSED
      write 0x3022 = 0x06          # pause — lens holds position

5. After capture, returning to preview:
      write 0x3022 = 0x08          # release — lens back to infinity
```

**Gotchas:**

- ⚠ **`FW_STATUS == 0x7F` is the symptom you will actually see** when AF "doesn't work". It means the blob transferred but the MCU is not running — either the enable bits in step 3 were not set, or the firmware image is wrong for your module. Reading `0x3029` first saves hours.
- ⚠ **AF must complete before the capture sequence starts** **[AN] §4.10.5**. Firing a capture mid-focus gives a blurred frame.
- ⚠ **The AF firmware is module-specific**, because it is tuned to the VCM's stroke and current. A blob from a different module may focus over the wrong range.
- ⚠ **`esp32-camera` does not do any of this.** Its `ov5640.c` contains no AF code. Autofocus on ESP32 requires a separate library layered on top — Seeed distributes `ESP32_OV5640_AF` (Eric Nam, v1.0.0), retained in the device tree at [DEV] `artifacts/originals/ov5640-autofocus-firmware.zip`. Note the misleading `OV5647_AF-main` directory name inside; see §1.
- The AF firmware upload is ~5 KB of SCCB traffic and, over 100 kHz I²C, takes a noticeable fraction of a second. Burst writes matter.

---

## 6. Use on ESP32 — `esp32-camera`

### 6.1 Driver support

`espressif/esp32-camera` v2.0.15 supports the OV5640 as a first-class sensor **[DRV]**: `sensors/ov5640.c`, `CAMERA_OV5640` in `camera_model_t`, `OV5640_PID = 0x5640`. Enable it in `menuconfig` under *Camera configuration → Support OV5640* (each sensor's init tables cost flash, so they are individually selectable).

Detection is by 16-bit chip ID at `0x300A` **[DRV]** `ov5640.c:1079–1082` — necessary because of the address clash with the OV3660 (§1).

### 6.2 Exact configuration

The working configuration, as used on the XIAO ESP32S3 Sense **[DEV]** `features/camera.md`:

```c
camera_config_t c = {};
c.ledc_channel   = LEDC_CHANNEL_0;      // XCLK is generated by LEDC
c.ledc_timer     = LEDC_TIMER_0;
c.pin_d0 = Y2_GPIO_NUM;  /* ... d1..d7 ... */
c.pin_xclk       = XCLK_GPIO_NUM;
c.pin_pclk       = PCLK_GPIO_NUM;
c.pin_vsync      = VSYNC_GPIO_NUM;
c.pin_href       = HREF_GPIO_NUM;
c.pin_sccb_sda   = SIOD_GPIO_NUM;
c.pin_sccb_scl   = SIOC_GPIO_NUM;
c.pin_pwdn       = -1;                  // not routed on the XIAO Sense
c.pin_reset      = -1;                  // not routed on the XIAO Sense
c.xclk_freq_hz   = 20000000;
c.pixel_format   = PIXFORMAT_JPEG;
c.frame_size     = FRAMESIZE_UXGA;
c.jpeg_quality   = 12;                  // 0..63, LOWER is better quality
c.fb_count       = 2;                   // requires PSRAM
c.fb_location    = CAMERA_FB_IN_PSRAM;
c.grab_mode      = CAMERA_GRAB_WHEN_EMPTY;
```

⚠ **`pin_pwdn` and `pin_reset` are `-1` on the XIAO Sense** — neither is routed **[DEV]**. The sensor cannot be power-cycled or hardware-reset in software; recovery from a wedged sensor requires a board reset. Budget for that in any long-running application.

### 6.3 PSRAM is not optional

A single uncompressed frame:

| Frame size | Pixels | RGB565 / YUV422 (2 B/px) |
|---|---:|---:|
| QVGA 320×240 | 76 800 | 150 KB |
| VGA 640×480 | 307 200 | 600 KB |
| UXGA 1600×1200 | 1 920 000 | **3.75 MB** |
| QSXGA 2592×1944 | 5 038 848 | **9.6 MB** |

The ESP32-S3 has **512 KB of internal SRAM**, not all of it contiguous or available. Therefore:

- **Anything above QVGA in an uncompressed format requires PSRAM**, and full resolution uncompressed exceeds even the 8 MB PSRAM on a XIAO Sense once you account for double buffering.
- **`PIXFORMAT_JPEG` is the practical format** above VGA. The OV5640 compresses on-chip (registers `0x4400`–`0x4407`), so the ESP32 receives an already-small stream. A UXGA JPEG at quality 12 is typically 100–300 KB.
- **`fb_count = 2` doubles the requirement** but is what makes streaming smooth. With `fb_count = 1` the driver must finish transferring before the next frame starts.
- **`fb_location = CAMERA_FB_IN_PSRAM`** is mandatory for anything non-trivial. Set `CAMERA_FB_IN_DRAM` only for QQVGA-class work on a PSRAM-less board.
- ⚠ **`jpeg_quality` is inverted** — 0 is best, 63 is worst. Setting it "high" for high quality produces mush. Values below ~10 at UXGA can overrun the frame buffer and produce truncated JPEGs.

### 6.4 Realistic throughput

The 15 fps full-resolution figure in §2 is a sensor number. On an ESP32-S3 over 8-bit DVP the limit is the parallel bus and DMA. Expect roughly: UXGA JPEG in the low single-digit fps, VGA JPEG at 20–25 fps, QVGA higher. [INF] — this record's author measured nothing; see the device's `performance.md` for any measured figures.

---

## 7. Known image-quality caveats

- **Fixed-pattern banding under artificial light.** The AEC banding filter (`0x3C00`–`0x3C1E`, `0x3A05`–`0x3A0E`) must be told whether the mains is 50 Hz or 60 Hz, or set to auto-detect. Left wrong, you get rolling horizontal bands. This is the single most common "my OV5640 pictures look bad" cause, and it is a two-register fix.
- **Auto white balance is mediocre** under mixed lighting. The AWB block (`0x5180`–`0x51D0`) has manual gain overrides at `0x3400`–`0x3406` if you can characterise your scene.
- **Lens shading correction is off by default in some init tables.** Corner darkening on a 1/4" sensor with a cheap lens is pronounced; LENC (`0x5800`–`0x583D`) exists but needs per-module calibration data to be worth enabling.
- **Rolling shutter.** Fast motion and horizontal panning skew. There is no global shutter option.
- **Thermal.** The OV5640 draws around **140 mA active** **[DEV]** — comparable to the rest of a XIAO board under load, and enough that Seeed ships it with a heat sink. Sustained full-resolution streaming warms the sensor and increases dark current and noise. `FRAMESIZE`-reduction between captures is a real mitigation.
- **First frames after init are bad.** AEC/AGC needs several frames to converge. Discard the first 3–5 frames after `esp_camera_init()` or after any large `set_framesize()` change; the driver does not do this for you.

---

## 8. Alternatives

| Part | vs. OV5640 | When |
|---|---|---|
| **[OV2640](../ov2640/README.md)** | 2 MP, DVP only, no AF, ~half the power | The default. Good enough for most ESP32 work, much lighter on RAM |
| **[OV3660](../ov3660/README.md)** | 3 MP, 1/5" (narrower FoV), no AF, same SCCB address | Middle ground; note the preliminary datasheet |
| **OV5647** | 5 MP, **MIPI only**, no embedded AF MCU | Raspberry Pi ecosystem. **Not** a drop-in |
| **GC2145** | 2 MP, cheap, supported by `esp32-camera` | Cost-driven |
| **SC031GS** | VGA **global shutter**, supported by `esp32-camera` | Machine vision, fast motion — where rolling shutter is disqualifying |
| **IMX219 / IMX477** | Far better sensors, MIPI only | ESP32-P4, Raspberry Pi, real imaging |

**Choose the OV5640 when you specifically need 5 MP stills or autofocus.** For streaming and vision work at VGA/QVGA the OV2640 gives the same result for less power, less RAM and no AF firmware complexity.

---

## 9. Pitfalls, in priority order

1. **Read the chip ID at `0x300A`; do not trust the SCCB address.** OV3660 is also at `0x3C`. §1.
2. **16-bit register addressing.** OV2640 code will not work. §3.2.
3. **Autofocus needs a firmware upload every power-up**, and `esp32-camera` does not do it. Check `FW_STATUS` (`0x3029`) — `0x7F` means "not running". §5.
4. **Use `PIXFORMAT_JPEG` above VGA, and PSRAM for everything.** §6.3.
5. **`jpeg_quality` is inverted** — lower is better. §6.3.
6. **Set the 50/60 Hz banding filter** or accept banded images. §7.
7. **Discard the first few frames** while AEC converges. §7.
8. **If frames are torn or discoloured, lower `xclk_freq_hz`** before suspecting anything else. §3.3.
9. **On boards where `PWDN`/`RESET` are unrouted**, a wedged sensor needs a full board reset. §6.2.
10. **Do not try to write init tables from the datasheet.** §4.

---

## 10. Open questions

- The exact provenance and module-specificity of the AF blob in the Seeed-distributed library is unverified; whether it is OmniVision's reference image or a module-house variant is unknown.
- No measured frame rates on ESP32-S3 for this record.
- The `0x3600`–`0x37FF` analog register meanings remain undocumented by OmniVision; nothing in this record resolves them.
- [AN] is marked *"Company Confidential / OmniVision Confidential for BYD Only"* on every page. It circulates widely via module vendors, but its redistribution status is **`restricted`/`unknown`** and it is retained here for research use only. Flagged for review.

---

## Manufacturer

**OmniVision Technologies, Inc.** (Santa Clara, CA; part of Will Semiconductor since 2019). See [`vendors/omnivision/README.md`](../../../vendors/omnivision/README.md).

Sourcing note relevant here: **OmniVision publishes essentially nothing publicly.** There is no customer-accessible datasheet portal; datasheets reach the world through camera-module vendors (Arducam, UCTRONICS, SparkFun, Waveshare) and distributor mirrors. Every OmniVision document in this repository came from a third-party mirror, and every one carries a redistribution restriction. Expect to hunt, and expect version ambiguity — mirrors rarely state which revision they hold.

## Used By

| Device | Role |
|---|---|
| [Seeed XIAO ESP32S3 Sense](../../../devices/seeed-studio/xiao-esp32s3-sense/README.md) | Optional 5 MP camera variant on the Sense daughterboard, DVP to the ESP32-S3 LCD_CAM peripheral via the [Hirose DF40C-30DP-0.4V](../../hirose/df40c-30dp-0.4v/README.md) board-to-board connector. `PWDN` and `RESET` unrouted. See [`features/camera.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/features/camera.md), [`sense-daughterboard.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/sense-daughterboard.md), [`pinouts-and-buses.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md) |

## Related pages

- [`components/omnivision/ov2640/README.md`](../ov2640/README.md) · [`components/omnivision/ov3660/README.md`](../ov3660/README.md)
- [`components/espressif/esp32-s3r8/README.md`](../../espressif/esp32-s3r8/README.md) — the LCD_CAM host and PSRAM
- [`components/hirose/df40c-30dp-0.4v/README.md`](../../hirose/df40c-30dp-0.4v/README.md) — the connector the DVP bus crosses

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | OV5640 datasheet | OmniVision | primary (via mirror) | datasheet | <https://cdn.sparkfun.com/datasheets/Sensors/LightImaging/OV5640_datasheet.pdf> | 2026-08-30 | **v2.03**, 179 pp, 1 749 719 B, SHA-256 `0e0b34b9…` | Register block map, resolutions/frame rates, DVP+MIPI, electricals | `artifacts/ov5640-datasheet-v2.03.pdf` → `shared-assets/` |
| D2 | OV5640 Auto Focus Camera Module Application Notes (with DVP Interface) | OmniVision | primary (via mirror) | application note | <https://www.arducam.com/downloads/modules/OV5640/OV5640_Software_app_note_parallel.pdf> | 2026-08-30 | **rev 2.13**, 4 Nov 2011, 63 pp, 1 909 564 B | **The entire §5 AF protocol** — `CMD_MAIN`/`CMD_ACK`/`FW_STATUS` values, MCU enable bits, sequence | `artifacts/ov5640-software-application-notes.pdf` |
| D3 | `espressif/esp32-camera` | Espressif | primary | repository | <https://github.com/espressif/esp32-camera> | 2026-08-30 | tag **v2.0.15** | SCCB address, PID, detection method, `framesize_t`, config struct | `/tmp` working copy, not vendored |
| S1 | XIAO ESP32S3 Sense camera feature guide | this repository | — | internal | — | 2026-08-30 | — | Board wiring, working config, XCLK/LEDC cost, AF library provenance | `devices/seeed-studio/xiao-esp32s3-sense/features/camera.md` |

**Acquisition note.** D1 was fetched independently from SparkFun's mirror and proved **byte-identical (SHA-256 `0e0b34b9…`)** to the copy already held in this repository from a different source — an independent confirmation of provenance, and per skill §18 the two are one artifact with two source URLs. It has since been consolidated into `shared-assets/` by the repository's deduplication pass, and the path here is a symlink.

D2 is **new to this repository**. Two other URLs for it returned HTTP 404 (both SparkFun paths); the Arducam mirror worked with a Chrome 131 User-Agent. Recorded in `component-download-failures.txt`.
