# OmniVision OV3660

> 3-megapixel backside-illuminated CMOS image sensor with an on-chip ISP and DVP output. Register-compatible in *shape* with the OV5640 — same SCCB address, same 16-bit register space, same `0x3xxx` layout — but not in content.
> Research snapshot **2026-08-30** (part-level detail added; specification tables retrieved 2026-08-24). The **current default sensor** on the Seeed XIAO ESP32S3 Sense. **No hardware was available.**

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DS]** | OV3660 datasheet **v1.3, May 2011**, marked **PRELIMINARY SPECIFICATION** — held at `artifacts/ov3660-datasheet.pdf` (see §9) |
| **[MOD]** | Seeed OV3660 camera module specification — same directory |
| **[DRV]** | `espressif/esp32-camera` **v2.0.15** — `sensors/ov3660.c`, `sensors/private_include/ov3660_settings.h`, `driver/include/sensor.h` |
| **[DEV]** | Seeed XIAO ESP32S3 Sense device record |
| **[INF]** | Author inference |

> ⚠ **The datasheet is PRELIMINARY and several figures are "TBD"** (dark current among them). Its numbers carry less weight than the OV5640's released PRODUCT SPECIFICATION. Where a decision turns on a marginal figure, measure rather than trust.

---

## 1. Identity, package and lifecycle

| Property | Value | Source |
|---|---|---|
| Part | **OV3660**, ordering code `OV03660-A51A` (colour, lead-free) | [DS] |
| Resolution | **2048 × 1536** (QXGA, 3 MP) | [DS] |
| Optical format | **1/5"** | [DS] |
| Pixel | **1.4 × 1.4 µm, OmniBSI** backside-illuminated | [DS] |
| Image area | 2912 × 2167.2 µm; package 5010 × 4960 µm | [DS] |
| Package | 51-pin CSP3 | [DS] |
| Output | **8/10-bit DVP** only — **no MIPI** | [DS] |
| Control | **SCCB**, **16-bit register addresses** | [DS], [DRV] |
| SCCB 7-bit address | **`0x3C`** (write `0x78`) — **shared with the OV5640** | [DRV] `sensor.h`: `OV3660_SCCB_ADDR = 0x3C, // 0x78 >> 1` |
| Chip ID | **`0x3660`**, 16-bit, from `0x300A` (high) / `0x300B` (low) | [DRV] `ov3660.c:1002–1006` |
| Datasheet status | **PRELIMINARY**, v1.3, May 2011 | [DS] |
| Lifecycle | Current default on the XIAO Sense as of this snapshot | [DEV] |

### 1.1 ⚠ The address clash with the OV5640, and how detection actually works

`OV3660_SCCB_ADDR == OV5640_SCCB_ADDR == 0x3C` **[DRV]**. Probing the bus cannot distinguish them. `esp32-camera` resolves it by reading the 16-bit chip ID and comparing **[DRV]** `ov3660.c:999–1013`:

```c
int ov3660_detect(int slv_addr, sensor_id_t *id) {
    if (OV3660_SCCB_ADDR == slv_addr) {
        uint8_t h = SCCB_Read16(slv_addr, 0x300A);
        uint8_t l = SCCB_Read16(slv_addr, 0x300B);
        uint16_t PID = (h << 8) | l;
        if (OV3660_PID == PID) { id->PID = PID; return PID; }
        else { ESP_LOGI(TAG, "Mismatch PID=0x%x", PID); }
    }
    return 0;
}
```

The `ov5640_detect()` function at `ov5640.c:1079` is byte-for-byte the same shape with a different constant. **Any code that identifies the sensor by SCCB address alone is wrong**, and the "Mismatch PID" log line is what you will see if you fit the other sensor.

Note also that the register *layout* is superficially identical to the OV5640 — same `0x300A` chip ID, same `0x3xxx`/`0x5xxx` block structure — which makes it tempting to reuse OV5640 code. **The register *contents* differ substantially**; `esp32-camera` ships entirely separate init tables (`ov3660_settings.h` vs `ov5640_settings.h`). Shape compatibility is not content compatibility.

---

## 2. Capabilities **[DS]**

| Parameter | Value |
|---|---|
| Supply | core **1.5 V** (embedded regulator) · analog 2.6–3.0 V (2.8 V typ) · I/O 1.8 V or 2.8 V (**1.8 V recommended**) |
| Active current | **98 mA** |
| Standby | **20 µA** |
| Input clock | **6–27 MHz** |
| S/N ratio | 34 dB |
| Dynamic range | **70 dB @ 8× gain** |
| Sensitivity | **670 mV/lux-s** |
| Shutter | **rolling** |
| Chief ray angle | 27.6° |
| Max exposure | 1560 × t_ROW |
| Operating temp | −20 °C to 70 °C junction |
| Stable image | 0 °C to 50 °C junction |
| Dark current | **TBD** in the preliminary datasheet |

**Frame rates:** 2048×1536 @ **15 fps** · 1080p @ 20 fps · 720p @ 45 fps · XGA @ 45 fps · VGA @ 60 fps · QVGA @ 120 fps.

**Output formats:** RAW RGB, RGB565/555/444, CCIR656, YCbCr422, and compressed. 8-/10-bit.

**On-chip automatics:** AEC, AWB, automatic flicker detection, ABLC. Supports **2×2 binning with an anti-artefact binning filter**, windowing, cropping, panning, mirror/flip, and **16-zone AEC/AGC weighting**.

### 2.1 The 1/5" optical format is the most consequential spec

The OV2640 and OV5640 are **1/4"**; the OV3660 is **1/5"** — a smaller sensor die. With the same lens and the same mount:

- **Field of view narrows.** A design framed around an OV2640 will crop when an OV3660 is substituted. This is not a firmware setting; it is optics.
- **Less light-gathering area**, partly offset by BSI and the higher 670 mV/lux-s sensitivity.
- Combined with 1.4 µm pixels (vs the OV2640's 2.2 µm), per-pixel light collection is substantially lower — hence the **34 dB S/N ratio**, worse than the OV2640's 40 dB, despite the newer process.

The compensating win is **dynamic range: 70 dB vs the OV2640's 50 dB**. In high-contrast scenes the OV3660 is clearly better; in dim uniform light the OV2640 is cleaner. That is the honest trade, and it is not the "newer is better" story the resolution bump suggests.

---

## 3. Register architecture

16-bit addresses in a flat space, no banking — structurally the same as the [OV5640](../ov5640/README.md#4-register-set-and-why-everyone-uses-vendor-init-tables), and unlike the [OV2640](../ov2640/README.md#3-the-two-bank-register-map--the-thing-to-understand-first)'s banked 8-bit map.

Blocks follow the OV5640 convention:

| Range | Block |
|---|---|
| `0x3000`–`0x30xx` | System / I/O pad control, clock enables, **chip ID at `0x300A`/`0x300B`**, software reset |
| `0x3100`–`0x31xx` | SCCB control (`0x3103` appears first in the init table **[DRV]** `ov3660_settings.h:29`) |
| `0x3500`–`0x350x` | AEC/AGC — exposure and gain |
| `0x3600`–`0x37xx` | Analog / sensor core — **undocumented magic numbers** |
| `0x3800`–`0x382x` | Timing: output window, cropping, **binning**, mirror/flip |
| `0x3A00`–`0x3Axx` | AEC control, banding filter. `esp32-camera` reads AEC2 state from **`0x3a00` mask `0x04`** **[DRV]** `ov3660.c:995` |
| `0x3C00`–`0x3Cxx` | 50/60 Hz light-frequency detection |
| `0x4000`–`0x40xx` | BLC |
| `0x4300`–`0x43xx` | Format control |
| `0x4700`–`0x47xx` | DVP control |
| `0x5000`–`0x50xx` | ISP top control |
| `0x5180`–`0x51xx` | AWB |
| `0x5300`–`0x58xx` | CIP / CMX / gamma / SDE / LENC |

**As with the OV5640, the `0x3600`–`0x37FF` analog block is effectively undocumented** and carries process-dependent trims supplied by OmniVision as opaque sequences. Every working driver begins with a vendor init table. **Do not attempt a from-scratch bring-up**; start from `esp32-camera`'s `ov3660_settings.h`.

---

## 4. Use on ESP32 — `esp32-camera`

Auto-detected as PID `0x3660` at SCCB `0x3C` with the correct register set loaded, so **substituting sensors on the XIAO Sense requires no code changes** **[DRV]**. Enable via `menuconfig` → *Camera configuration → Support OV3660* (`CONFIG_OV3660_SUPPORT`).

Arduino: define `CAMERA_MODEL_XIAO_ESP32S3`, then `esp_camera_init()`.

Identify at runtime:

```c
sensor_t *s = esp_camera_sensor_get();
// s->id.PID:  0x26 = OV2640, 0x3660 = OV3660, 0x5640 = OV5640
```

### 4.1 Frame-buffer budget

Uncompressed at 2 bytes/pixel:

| Frame size | Bytes |
|---|---:|
| QVGA 320×240 | 150 KB |
| VGA 640×480 | 600 KB |
| XGA 1024×768 | 1.5 MB |
| FHD 1920×1080 | 4.0 MB |
| **QXGA 2048×1536** | **6.0 MB** |

Against 512 KB of ESP32-S3 internal SRAM: **anything above QVGA needs PSRAM or JPEG**, and full 3 MP uncompressed with `fb_count = 2` exceeds even 8 MB of PSRAM once the rest of the application is accounted for. Use `PIXFORMAT_JPEG` above VGA. ⚠ `jpeg_quality` is inverted — **0 is best, 63 is worst**.

Configuration is otherwise identical in shape to the OV5640's; see [`ov5640/README.md` §6.2](../ov5640/README.md#62-exact-configuration).

---

## 5. Limits and caveats

- **Preliminary datasheet**, several figures TBD. §Evidence labelling.
- **1/5" format changes framing** versus the OV2640/OV5640. §2.1.
- **No autofocus.** Fixed focus only.
- **Rolling shutter** — motion skew on fast pans; the OV2640's progressive scan is better here.
- **Worse S/N than the OV2640** (34 dB vs 40 dB) despite being newer. §2.1.
- **Register map differs substantially from the OV2640 and, in content, from the OV5640.** Direct register writes are not portable. §1.1, §3.
- **Banding under artificial light** unless the 50/60 Hz filter (`0x3C00`–`0x3Cxx`) is configured or set to auto-detect. The single most common image-quality complaint.
- **Discard the first 3–5 frames** after init or a `set_framesize()` change while AEC/AGC converges; the driver does not do this for you.
- **First response to torn or discoloured frames: lower `xclk_freq_hz`** to 10 MHz, and reseat the FPC.

---

## 6. Exact role on the XIAO ESP32S3 Sense **[DEV]**

Fitted on the detachable Sense daughterboard, connected to the ESP32-S3R8 over an 8-bit DVP bus plus SCCB, all routed across the 30-pin `DF40C-30DP-0.4V(51)` board-to-board connector.

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

- ⚠ **SCCB is on GPIO40/39, *not* the board's `Wire` I²C bus.**
- ⚠ **`PWDN` and `RESET` are unrouted**, so the sensor cannot be reset or powered down independently. This causes the "works cold, fails after soft reset" behaviour and contributes to elevated deep-sleep current — though at **20 µA standby** the OV3660 is far better here than the OV2640's 600 µA.
- **`XCLK` consumes `LEDC_CHANNEL_0`/`LEDC_TIMER_0`** by convention; avoid them elsewhere.

Full wiring: [`pinouts-and-buses.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md#3-camera-bus-dvp-8-bit-parallel) · usage: [`features/camera.md`](../../../devices/seeed-studio/xiao-esp32s3-sense/features/camera.md)

### 6.1 The sensor-identity conflict

Seeed originally shipped the [OV2640](../ov2640/README.md) and now ships the OV3660, while **the product page still advertises the OV2640 and its 1600×1200 resolution**. The [OV5640](../ov5640/README.md) is sold as an upgrade. The SKU does not tell you what is fitted; read `esp_camera_sensor_get()->id.PID`. See [`gaps-and-conflicts.md` §5](../../../devices/seeed-studio/xiao-esp32s3-sense/gaps-and-conflicts.md#5-the-camera-sensor-fitted-has-changed-and-the-product-page-is-stale).

---

## 7. Alternatives

| Part | vs. OV3660 | When |
|---|---|---|
| **[OV2640](../ov2640/README.md)** | 2 MP, 1/4", better S/N, progressive scan, no PSRAM needed at low res; 600 µA standby | The lighter, better-supported default |
| **[OV5640](../ov5640/README.md)** | 5 MP, 1/4", **autofocus**, MIPI option; ~140 mA | Stills and AF |
| **GC2145** | 2 MP, cheaper, `esp32-camera` supported | Cost-driven |
| **SC031GS** | VGA **global shutter** | Fast motion, machine vision |

The OV3660 occupies an awkward middle: more pixels than the OV2640 but worse noise and a narrower field of view, and no autofocus to justify the OV5640's cost. It is on this board because Seeed's supply changed, not because it is the best of the three for most uses. If you are choosing freely, **the OV2640 or the OV5640 is usually the better answer**. [INF]

---

## 8. Open questions

- Dark current and several other figures are **TBD** in the only publicly obtainable datasheet.
- Whether a released (non-preliminary) OV3660 datasheet exists is unknown; nothing found.
- No hardware measurement of frame rate, current or image quality.
- Whether the narrower 1/5" field of view is compensated by a different lens in Seeed's module was not established from [MOD].

---

## 9. Artifacts and a filing note

The OV3660 datasheet and Seeed module specification currently live in the **device** tree:

- [`ov3660-datasheet.pdf`](artifacts/ov3660-datasheet.pdf) — v1.3, May 2011, 1 917 798 B, SHA-256 `5afc0efd…`
- [`ov3660-camera-module-spec.pdf`](artifacts/ov3660-camera-module-spec.pdf) — 387 241 B, SHA-256 `c38741e9…`

> **Filing note — resolved 2026-08-30.** Per the research skill's placement rule, a *chip* datasheet is a
> **component** artifact even when a device task fetched it. Both files have now been **moved** here from
> `devices/seeed-studio/xiao-esp32s3-sense/artifacts/datasheets/`; hashes re-verified unchanged after the
> move, and a [pointer](../../../devices/seeed-studio/xiao-esp32s3-sense/artifacts/datasheets/RELOCATED-ov3660.md)
> remains at the old location. This was a **move, not a copy** (duplication is what the shared-asset pass is
> removing, and redistribution is `prohibited`) and **not an archive** — with all five re-fetch URLs 404 as of
> 2026-08-30, these are scarce and stay in the repository.

> **Redistribution: `prohibited`.** The datasheet states: *"Individuals and/or organizations are not allowed to re-distribute said information."* Rehosting by Seeed does not relicense it. The specification tables in this record are extracted factual data, not a reproduction of the document.

### 9.1 Independent re-acquisition failed

Five URLs were tried on 2026-08-30 to obtain an independent copy for hash comparison. **All five failed**, and the failures are recorded in `component-download-failures.txt`:

| URL | Result |
|---|---|
| `https://www.arducam.com/downloads/modules/OV3660/OV3660_datasheet.pdf` | HTTP 404 — **260 KB of HTML** that would pass a size check |
| `https://www.arducam.com/wp-content/uploads/2018/01/OV3660_datasheet.pdf` | HTTP 404 |
| `https://www.arducam.com/wp-content/uploads/2019/10/OV3660_datasheet.pdf` | HTTP 404 |
| `https://files.waveshare.com/upload/9/9a/OV3660_datasheet.pdf` | HTTP 404 |
| `https://dl.espressif.com/dl/schematics/OV3660_datasheet.pdf` | HTTP 404 |

Consequence: unlike the OV2640 and OV5640 — both of which were independently re-fetched and proved byte-identical to the repository's copies — **the OV3660 datasheet has a single unverified source**. It is the scarcer document of the three.

---

## Manufacturer

**OmniVision Technologies, Inc.** — see [`vendors/omnivision/README.md`](../../../vendors/omnivision/README.md). OmniVision publishes nothing publicly; the OV3660 in particular has proved the hardest of the three to source, with every mirror tried returning 404.

## Used By

| Device | Role |
|---|---|
| [Seeed XIAO ESP32S3 Sense](../../../devices/seeed-studio/xiao-esp32s3-sense/README.md) | **Current default** camera on the Sense daughterboard. DVP + SCCB across the [DF40C-30DP-0.4V](../../hirose/df40c-30dp-0.4v/README.md); `PWDN`/`RESET` unrouted. §6 |

## Related pages

- [`components/omnivision/ov2640/README.md`](../ov2640/README.md) · [`components/omnivision/ov5640/README.md`](../ov5640/README.md)
- [`components/espressif/esp32-s3r8/README.md`](../../espressif/esp32-s3r8/README.md) — the LCD_CAM host and PSRAM
- [`components/hirose/df40c-30dp-0.4v/README.md`](../../hirose/df40c-30dp-0.4v/README.md)

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | OV3660 datasheet | OmniVision | primary (via Seeed mirror) | datasheet | via Seeed wiki; **five independent re-fetch URLs 404 on 2026-08-30** (§9.1) | 2026-08-24 | **v1.3, May 2011, PRELIMINARY**, 1 917 798 B, SHA-256 `5afc0efd…` | All §2 specifications | [`artifacts/ov3660-datasheet.pdf`](artifacts/ov3660-datasheet.pdf) |
| D2 | OV3660 camera module specification | Seeed Studio | primary | datasheet | via Seeed wiki | 2026-08-24 | 387 241 B, SHA-256 `c38741e9…` | Module-level lens and flex detail | same directory |
| D3 | `espressif/esp32-camera` | Espressif | primary | repository | <https://github.com/espressif/esp32-camera> | 2026-08-30 | tag **v2.0.15** | SCCB address, PID, **detection code**, register-block usage | not vendored |
| S1 | XIAO ESP32S3 Sense records | this repository | — | internal | — | 2026-08-30 | — | §6 wiring, §6.1 identity conflict | `devices/seeed-studio/xiao-esp32s3-sense/` |
