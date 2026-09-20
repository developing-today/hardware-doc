# OmniVision OV2640

> 2-megapixel CMOS image sensor with an on-chip JPEG compression engine, DVP output, and a **two-bank 8-bit register map** that is the source of most driver bugs written against it.
> Research snapshot **2026-08-30** (part-level detail added; specification tables retrieved 2026-08-24). Fitted to early Seeed XIAO ESP32S3 Sense units. **No hardware was available.**

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DS]** | OV2640 datasheet, **Version 1.6, 28 February 2006** (*Advanced Information / Preliminary*) — `artifacts/ov2640-datasheet-v2.2.pdf` (symlink into `shared-assets/`) |
| **[DRV]** | `espressif/esp32-camera` **v2.0.15** — `sensors/ov2640.c`, `sensors/private_include/ov2640_regs.h`, `driver/include/sensor.h` |
| **[DEV]** | Seeed XIAO ESP32S3 Sense device record |
| **[INF]** | Author inference |

> ⚠ **Filename caveat.** The local file is named `…-v2.2.pdf` but its first page reads **"Version 1.6, February 28, 2006"**. The name came from the mirror URL, not the document. The document's own revision — **v1.6** — is authoritative. This is a recurring OmniVision trap; see [`vendors/omnivision/README.md`](../../../vendors/omnivision/README.md) §3.

---

## 1. Identity, package and lifecycle

| Property | Value | Source |
|---|---|---|
| Part | **OV2640**, ordering code `OV02640-VL9A` | [DS] |
| Resolution | **1600 × 1200** (UXGA), 2 MP | [DS] |
| Total / active array | 1632 × 1232 (2 010 624 px) / 1 991 040 active | [DS] |
| Optical format | **1/4"** | [DS] |
| Pixel | **2.2 × 2.2 µm**, OmniPixel2, **front-side illuminated** | [DS] |
| Package | 38-pin CSP2, 5725 × 6285 µm; image area 3590 × 2684 µm | [DS] |
| Output | **8/10-bit DVP** only — **no MIPI** | [DS] |
| Control | **SCCB**, **8-bit register addresses**, two banks | [DS], [DRV] |
| SCCB 7-bit address | **`0x30`** (write `0x60`, read `0x61`) | [DRV] `sensor.h`: `OV2640_SCCB_ADDR = 0x30, // 0x60 >> 1` |
| Product ID | **`0x26`** (`OV2640_PID`) | [DRV] `sensor.h` |
| Version register | `REG_VER` = `0x0B` in the sensor bank | [DRV] `ov2640_regs.h:110` |
| Datasheet status | **Advanced Information / Preliminary**, 2006 | [DS] |
| Lifecycle | **Legacy.** Twenty-year-old part; still manufactured for the module market, but discontinued on the XIAO Sense | [DEV] |

### 1.1 It is the only one of the three at a *different* SCCB address

| Sensor | SCCB 7-bit | Register width | Chip-ID register |
|---|---|---|---|
| **OV2640** | **`0x30`** | **8-bit**, banked | `0x0A`/`0x0B` in sensor bank |
| OV3660 | `0x3C` | 16-bit | `0x300A`/`0x300B` |
| OV5640 | `0x3C` | 16-bit | `0x300A`/`0x300B` |

This is convenient: an OV2640 and an OV3660/OV5640 can be told apart by *address alone*, unlike the latter two, which need a chip-ID read. `esp32-camera` probes both addresses during autodetect.

---

## 2. Capabilities **[DS]**

| Parameter | Value |
|---|---|
| Supply | core **1.2 V ±5 %** · analog 2.5–3.0 V · I/O 1.7–3.3 V |
| Power, active | **125 mW** (15 fps UXGA YUV) · 140 mW compressed |
| Standby | **600 µA** |
| S/N ratio | **40 dB** — the best of the three sensors used on this board |
| Dynamic range | **50 dB** — the worst of the three |
| Sensitivity | 0.6 V/lux-s · well capacity 12 Ke⁻ |
| Scan mode | **progressive** |
| Chief ray angle | 25° · max exposure 1247 × t_ROW |
| Dark current | 15 mV/s @ 60 °C · FPN < 1 % of V_pp |
| Input clock | 6–27 MHz |
| Operating temp | −30 °C to 70 °C |

**Frame rates:** UXGA/SXGA @ **15 fps** · SVGA @ **30 fps** · CIF @ **60 fps**.

**Output formats:** YUV(422/420) / YCbCr422, RGB565/555, **8-bit compressed (JPEG)**, 8-/10-bit RAW RGB.

**On-chip automatics:** AEC, AGC, AWB, ABF (auto black-level filter), ABLC, 50/60 Hz luminance detection. Windowing from 2×4 up to 1632×1220. **VarioPixel®** sub-sampling. An embedded microcontroller and a **compression engine**.

---

## 3. The two-bank register map — the thing to understand first

The OV2640 has **8-bit register addresses** and therefore only 256 slots — far too few. OmniVision solved this with **bank switching**, and it is the single most common source of OV2640 driver bugs.

**Register `0xFF` is `BANK_SEL`** **[DRV]** `ov2640_regs.h:45`:

```c
#define BANK_SEL   0xFF
enum { BANK_DSP = 0, BANK_SENSOR = 1, BANK_MAX };
```

| Bank | `0xFF` value | Contents |
|---|:-:|---|
| **`BANK_DSP`** | `0` | The DSP/ISP side: windowing (`HSIZE`, `VSIZE`, `XOFFL`, `YOFFL`, `ZMOW`, `ZMOH`), output format, **JPEG quality (`QS`)**, DVP setup (`R_DVP_SP`), bypass (`R_BYPASS`), brightness/contrast/saturation/special-effects/AWB-mode tables |
| **`BANK_SENSOR`** | `1` | The sensor core: `COM7` (including the **software reset** bit `COM7_SRST`), `CLKRC` (clock divider), `PIDH`/`PIDL`, `REG_VER`, AEC level tables, gain, exposure |

**The trap:** the *same* 8-bit address means different registers in the two banks. Writing what you believe is a DSP register while the chip is in the sensor bank silently corrupts sensor-core state. Because there is no error, the symptom is a sensor that produces *almost* correct images — wrong colours, wrong size, or intermittent corruption — rather than an obvious failure.

**How `esp32-camera` handles it correctly** **[DRV]** `ov2640.c:28–50`: it caches the current bank and only emits a `BANK_SEL` write when the bank actually changes, and its register tables carry `{BANK_SEL, BANK_x}` entries inline so a table can switch banks mid-sequence:

```c
res = SCCB_Write(sensor->slv_addr, BANK_SEL, bank);      // ov2640.c:33
...
if (regs[i][0] == BANK_SEL) { /* track the bank */ }      // ov2640.c:42
```

Every register write in the driver is routed through `WRITE_REG_OR_RETURN(BANK_x, reg, val)`, so the bank is explicit at every call site — e.g. the software reset at `ov2640.c:104`:

```c
WRITE_REG_OR_RETURN(BANK_SENSOR, COM7, COM7_SRST);
```

and the windowing block at `ov2640.c:148–156`, which explicitly re-selects `BANK_DSP` first.

> **If you are reading or writing an OV2640 driver, this is the invariant to check.** A driver that writes `0xFF` once at init and then assumes the bank never changes will work until the first `set_quality()` or `set_framesize()` call.

### 3.1 Notable registers **[DRV]** `ov2640_regs.h`

| Bank | Reg | Name | Purpose |
|---|---|---|---|
| — | `0xFF` | `BANK_SEL` | 0 = DSP, 1 = sensor |
| SENSOR | `0x0A`/`0x0B` | `PIDH`/`PIDL`, `REG_VER` | Product ID `0x26` and version |
| SENSOR | `0x12` | `COM7` | Bit 7 = `COM7_SRST` software reset; resolution select |
| SENSOR | `0x11` | `CLKRC` | Internal clock divider |
| DSP | `0x05` | `R_BYPASS` | `R_BYPASS_DSP_BYPAS` / `R_BYPASS_DSP_EN` — **must bypass the DSP while changing clocks** |
| DSP | `0xD3` | `R_DVP_SP` | DVP output speed / PCLK divider |
| DSP | `0x51`/`0x52` | `HSIZE`/`VSIZE` | Input window size |
| DSP | `0x53`/`0x54` | `XOFFL`/`YOFFL` | Window offsets |
| DSP | `0x5A`/`0x5B` | `ZMOW`/`ZMOH` | **Zoom/scaler output** width and height |
| DSP | `0x44` | `QS` | **JPEG quantisation scale** — the JPEG quality knob |
| DSP | `0xC7` | — | Bit 6 gates manual vs. auto white balance |

### 3.2 The clock-change sequence is order-sensitive **[DRV]** `ov2640.c:197–202`

```c
WRITE_REG_OR_RETURN(BANK_DSP,    R_BYPASS, R_BYPASS_DSP_BYPAS);  // 1. bypass the DSP
WRITE_REG_OR_RETURN(BANK_SENSOR, CLKRC,    c.clk);               // 2. change sensor clock
WRITE_REG_OR_RETURN(BANK_DSP,    R_DVP_SP, c.pclk);              // 3. change DVP speed
WRITE_REG_OR_RETURN(BANK_DSP,    R_BYPASS, R_BYPASS_DSP_EN);     // 4. re-enable the DSP
```

Changing `CLKRC` with the DSP enabled leaves the pipeline running on a clock that has moved under it. The bypass/restore bracket is not optional, and a driver that omits it produces corrupted first frames after any resolution change. [INF] — inferred from the driver's deliberate ordering; the datasheet does not state the requirement explicitly in the text this record examined.

---

## 4. Where it differs from its successors

- **Larger pixels (2.2 µm vs 1.4 µm)** and **the best S/N ratio of the three (40 dB)** — but the **worst dynamic range (50 dB vs ~70 dB)** and the oldest process (FSI, not BSI). In practice: cleaner in good light, worse in high-contrast scenes.
- **Progressive scan**, where the OV3660 and OV5640 use rolling shutters. Less motion skew.
- **Much higher standby current (600 µA vs 20 µA)** — relevant to battery designs, though on the XIAO board the sensor cannot be powered down anyway (§6).
- **Lowest resolution, no autofocus, no MIPI.**
- **8-bit banked registers**, where the others use a flat 16-bit space. Driver code is not portable in either direction.

---

## 5. Use on ESP32 — `esp32-camera`

`esp32-camera` auto-detects PID `0x26` at SCCB `0x30` and loads the correct register set **[DRV]**. The OV2640 is **the most widely supported sensor in the ESP32 ecosystem** — the entire ESP32-CAM / AI-Thinker corpus targets it, so example code, tutorials and StackOverflow answers are abundant and mostly correct.

Enable via `menuconfig` → *Camera configuration → Support OV2640* (`CONFIG_OV2640_SUPPORT`). Each sensor's init tables cost flash, so disable the ones you do not fit.

### 5.1 Frame-buffer budget

Uncompressed frames at 2 bytes/pixel:

| Frame size | Bytes |
|---|---:|
| QQVGA 160×120 | 37 KB |
| QVGA 320×240 | 150 KB |
| VGA 640×480 | 600 KB |
| SVGA 800×600 | 937 KB |
| **UXGA 1600×1200** | **3.75 MB** |

The ESP32-S3 has 512 KB of internal SRAM. Therefore:

- **QQVGA and QVGA fit in internal DRAM** (`fb_location = CAMERA_FB_IN_DRAM`) — the OV2640 is the only one of the three sensors for which a **PSRAM-less** design is genuinely practical, and that is a real reason to choose it.
- **VGA and above need PSRAM**, or `PIXFORMAT_JPEG`.
- **`PIXFORMAT_JPEG` uses the on-chip compression engine**, so the ESP32 receives an already-small stream. A UXGA JPEG at quality 12 is typically 50–150 KB.
- ⚠ **`jpeg_quality` is inverted**: 0 = best, 63 = worst.

### 5.2 Configuration

Identical in shape to the OV5640's — see [`ov5640/README.md` §6.2](../ov5640/README.md#62-exact-configuration). The only OV2640-specific differences are the achievable `frame_size` ceiling (`FRAMESIZE_UXGA`) and that low resolutions can live in DRAM.

---

## 6. Exact role on the XIAO ESP32S3 Sense **[DEV]**

Original sensor on the detachable Sense daughterboard, connected to the ESP32-S3R8 over an 8-bit DVP bus plus SCCB, all routed across the 30-pin `DF40C-30DP-0.4V(51)` board-to-board connector.

| Signal | GPIO | | Signal | GPIO |
|---|---:|---|---|---:|
| `XCLK` | **10** (LEDC-generated, ~20 MHz) | | `D0` (Y2) | 15 |
| `PCLK` | 13 | | `D1` (Y3) | 17 |
| `VSYNC` | 38 | | `D2` (Y4) | 18 |
| `HREF` | 47 | | `D3` (Y5) | 16 |
| `SIOD` (SCCB SDA) | **40** | | `D4` (Y6) | 14 |
| `SIOC` (SCCB SCL) | **39** | | `D5` (Y7) | 12 |
| **`PWDN`** | **−1, not routed** | | `D6` (Y8) | 11 |
| **`RESET`** | **−1, not routed** | | `D7` (Y9) | 48 |

- ⚠ **SCCB is on GPIO40/39, not the board's `Wire` I²C bus.** Do not attempt to share it with other I²C peripherals.
- ⚠ **`PWDN` and `RESET` are unrouted**, so the sensor cannot be reset or powered down independently. This is the direct cause of the "works cold, fails after soft reset" behaviour and of the board's elevated deep-sleep current — the OV2640's 600 µA standby is *always* being drawn.
- **`XCLK` consumes an LEDC channel and timer** (`LEDC_CHANNEL_0`/`LEDC_TIMER_0` by convention). Avoid channel 0 and timer 0 for anything else.

Full wiring: [`pinouts-and-buses.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#3-camera-bus-dvp-8-bit-parallel) · usage: [`features/camera.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/features/camera.md)

### 6.1 ⚠ Which sensor is actually fitted is not knowable from the SKU

Seeed's product page and feature bullets **still advertise the OV2640 and its 1600×1200 resolution**, while the wiki states it is discontinued and current units ship the [OV3660](../ov3660/README.md). Read it at runtime:

```c
sensor_t *s = esp_camera_sensor_get();
// s->id.PID:  0x26 = OV2640, 0x3660 = OV3660, 0x5640 = OV5640
```

See [`gaps-and-conflicts.md` §5](../../../devices/seeed-studio/xiao-esp32s3-sense/gaps-and-conflicts.md#5-the-camera-sensor-fitted-has-changed-and-the-product-page-is-stale).

---

## 7. Pitfalls, in priority order

1. **Bank switching.** `0xFF` selects DSP (0) or sensor (1). The same address means different things in each. §3.
2. **Bracket clock changes with `R_BYPASS`.** §3.2.
3. **8-bit register addresses.** OV3660/OV5640 code will not work, and vice versa. §1.1.
4. **`jpeg_quality` is inverted** — lower is better.
5. **Discard the first few frames** after init or a `set_framesize()` change while AEC/AGC converges.
6. **Set the 50/60 Hz banding filter** or accept banded images under artificial light.
7. **Lower `xclk_freq_hz` to 10 MHz** as the first response to torn or discoloured frames.
8. **600 µA standby is not nothing** if the sensor cannot be powered down. §6.
9. **Do not write init tables from the datasheet** — the 2006 preliminary specification does not document the analog core. Start from `esp32-camera`'s `ov2640_settings.h`.

---

## 8. Alternatives

| Part | vs. OV2640 | When |
|---|---|---|
| **[OV3660](../ov3660/README.md)** | 3 MP, BSI, better dynamic range, 20 µA standby, 1/5" (narrower FoV) | Its direct replacement on this board |
| **[OV5640](../ov5640/README.md)** | 5 MP + autofocus + MIPI, but ~140 mA and much more RAM | When you need stills or AF |
| **GC2145** | 2 MP, cheaper, `esp32-camera` supported | Cost-driven second source |
| **GC0308** | VGA, very cheap, tiny RAM footprint | Low-resolution vision on a PSRAM-less board |
| **SC031GS** | VGA **global shutter** | Fast motion, machine vision |

**The OV2640 remains the right default for ESP32 camera work** unless you specifically need resolution. It is the cheapest, the best-supported, the least RAM-hungry, and the only one that works comfortably without PSRAM.

---

## 9. Open questions

- The `R_BYPASS` bracketing requirement in §3.2 is inferred from driver behaviour; the v1.6 preliminary datasheet does not state it in the text examined.
- Whether any current XIAO ESP32S3 Sense units still ship the OV2640 is unresolved — the vendor's own pages disagree.
- No hardware measurement of standby current or frame rate.

---

## Manufacturer

**OmniVision Technologies, Inc.** — see [`vendors/omnivision/README.md`](../../../vendors/omnivision/README.md) for sourcing patterns. OmniVision publishes nothing publicly; this datasheet came from a camera-module vendor's mirror.

## Used By

| Device | Role |
|---|---|
| [Seeed XIAO ESP32S3 Sense](../../../devices/seeed-studio/xiao-esp32s3-sense/README.md) | Original camera on the Sense daughterboard (now superseded by the OV3660). DVP + SCCB across the [DF40C-30DP-0.4V](../../hirose/df40c-30dp-0.4v/README.md); `PWDN`/`RESET` unrouted. §6 |

## Related pages

- [`components/omnivision/ov3660/README.md`](../ov3660/README.md) · [`components/omnivision/ov5640/README.md`](../ov5640/README.md)
- [`components/espressif/esp32-s3r8/README.md`](../../espressif/esp32-s3r8/README.md) — the LCD_CAM host and PSRAM
- [`components/hirose/df40c-30dp-0.4v/README.md`](../../hirose/df40c-30dp-0.4v/README.md)

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | OV2640 datasheet | OmniVision | primary (via mirror) | datasheet | <https://www.uctronics.com/download/cam_module/OV2640DS.pdf> | 2026-08-30 | **v1.6, 2006-02-28**, "Advanced Information", 43 pp, 676 989 B, SHA-256 `4460f2f1…` | All §2 specifications, formats, frame rates | `artifacts/ov2640-datasheet-v2.2.pdf` → `shared-assets/` |
| D2 | `espressif/esp32-camera` | Espressif | primary | repository | <https://github.com/espressif/esp32-camera> | 2026-08-30 | tag **v2.0.15** | SCCB address `0x30`, PID `0x26`, **the bank-switching mechanism**, register names, clock-change sequence | not vendored |
| S1 | XIAO ESP32S3 Sense records | this repository | — | internal | — | 2026-08-30 | — | §6 wiring, the sensor-identity conflict | `devices/seeed-studio/xiao-esp32s3-sense/` |

**Acquisition note.** D1 was fetched independently and proved **byte-identical (SHA-256 `4460f2f1…`)** to the copy already in this repository — one artifact, two source URLs, per skill §18. A second URL (`OV2640_DS.pdf`, advertised as "software application notes") returned **the same bytes**; that duplicate has been archived to `components/omnivision/ov2640/artifacts/ov2640-datasheet-v2.2.pdf` rather than retained. No separate OV2640 application-notes document was located.

> **Redistribution: `unknown`.** D1 is marked *"Proprietary to OmniVision Technologies"*; no explicit redistribution clause was located in v1.6 — unlike the OV3660 and OV5640 datasheets, which carry one. The specification tables above are extracted factual data, not a reproduction of the document.
