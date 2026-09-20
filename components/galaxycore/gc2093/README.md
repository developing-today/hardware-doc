# GalaxyCore GC2093 — 1/2.9″ 2 MP MIPI CSI-2 CMOS image sensor

- **Category:** CMOS image sensor, MIPI CSI-2, rolling shutter
- **Manufacturer:** **GalaxyCore Inc.** (格科微电子). The `GC` prefix is GalaxyCore's; no public GC2093 datasheet was located on 2026-09-04, so the attribution rests on the family prefix and on the sensor's ubiquity in Chinese IPC/AIoT designs.
- **Research status:** primary evidence is a **26 213-byte vendor V4L2 sensor driver** (`vvcam/src/gc2093.c`) shipped in the LilyGO BSP, plus vendor product copy.
- **Retrieved:** 2026-09-04

## 1. Known properties

| Property | Value | Evidence |
|---|---|---|
| Part | **GC2093** | S1, S2 |
| Resolution | **2 MP, 1080p** | S1 |
| Interface | **MIPI CSI-2** | S2 |
| Control bus | I²C, 7-bit address **`0x37`** | S2 |
| Linux/ISP integration | Canaan **`vvcam`** (VeriSilicon ISP V4L2 stack); `BR2_PACKAGE_VVCAM_DEF_SENSOR="gc2093"` | S3 |
| Driver source | `k230_bsp/overlay/buildroot-overlay/package/vvcam/src/gc2093.c`, 26 213 bytes | S3 |
| DT integration | `0036-add-gc2093-camera.patch` | S3 |

`0x37` is a notable address: it is *not* the more common `0x3C`/`0x36` used by many sensors,
and it collides with nothing else on this board because the camera sits on its own I²C bus
(`GPIO48/49`, I²C0) rather than the shared expansion bus.

## 2. Integration notes

The sensor is wired through Canaan's `vvcam` ISP driver rather than a plain V4L2 subdev, so
the useful configuration surface is the **ISP tuning** path, not the sensor driver: Canaan
publishes `K230_ISP_Image_Tuning_Guide` and `K230_ISP_Initial_Setting_Guide`, and
`K230_Image_Capture_Practice_How_to_support_a_new_sensor` is the document to read before
swapping the sensor. `K230_VICAP_SENSOR_Parameter_Partition_Reference` documents where sensor
parameters live in flash/partition terms.

The K230 supports **three** MIPI CSI inputs; only one is populated on the LilyGO board, so two
CSI interfaces are available on the expansion header for additional sensors. Canaan's own
reference DTS also mentions `OV5647` and the BSP tree mentions `IMX219`, which are the two
sensors most likely to work with modest effort.

## 3. Unknowns

- Pixel size, optical format, frame-rate/exposure limits, HDR/WDR mode support, lane count and
  link rate: **all unknown from primary sources.** The driver contains the register writes but
  those were not decoded against a datasheet in this pass, because no datasheet was available
  to decode them against. This is a deliberate gap, not an oversight — see
  [gaps-and-conflicts.md](../../../devices/lilygo/t-display-k230/gaps-and-conflicts.md) `GC-6`.
- Lens/module vendor: unknown.

## 4. Used By

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

The single fitted camera. I²C0 on **`GPIO49` SDA / `GPIO48` SCL** at **`0x37`**, image data over
MIPI CSI. Exercised by the launcher's camera preview, still capture, RTSP push, QR scan
(`qr_scan.c`), face detection (`camera_face_detect.cpp`) and motion probe apps.

## 5. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | T-Display K230 Kit product page | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230-kit` | 2026-09-04 | "Camera: 2MP 1080P, Module: GC2093" |
| S2 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | I²C address `0x37`, GPIO48/49, MIPI CSI |
| S3 | `vvcam/src/gc2093.c`, `0036-add-gc2093-camera.patch`, `k230_canmv_t_display_rm69a10_defconfig` | LILYGO | primary | source | same repo | 2026-09-04 | Driver existence and size, default sensor selection |
