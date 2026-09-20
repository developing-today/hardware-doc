# Camera — GC2093 2 MP over MIPI CSI

**Question:** *How do I capture, stream and run vision on the camera?*

| | |
|---|---|
| Sensor | [GalaxyCore GC2093](../../../../components/galaxycore/gc2093/README.md), 2 MP 1080p |
| Data | K230 **MIPI CSI-2** |
| Control | I²C0 — `GPIO49` SDA / `GPIO48` SCL, **`0x37`** |
| ISP | K230 on-chip ISP, **8 MP @ 30 fps** total throughput, 3A / 2DNR / 3DNR / WDR / HDR / LTM / de-warp / RGB-IR |
| Stack | Canaan **`vvcam`** (VeriSilicon ISP) → V4L2 |
| Evidence | `reported-working` |

## Software

`BR2_PACKAGE_VVCAM=y` with `BR2_PACKAGE_VVCAM_DEF_SENSOR="gc2093"`. The sensor driver is
`vvcam/src/gc2093.c` (26 213 bytes); board integration is `0036-add-gc2093-camera.patch`. A V4L2
↔ DRM shim lives at `vvcam/v4l2-drm/src/lib.c` (21 372 bytes), and the MIPI driver is
`vvcam/mipi/vvcam_mipi_driver.c` (16 697 bytes).

Because it goes through `vvcam` rather than a plain V4L2 subdev, **the tuning surface is the ISP,
not the sensor driver.** Canaan's relevant documents are `K230_ISP_Image_Tuning_Guide`,
`K230_ISP_Initial_Setting_Guide`, `K230_VICAP_API_Reference` and
`K230_VICAP_SENSOR_Parameter_Partition_Reference`.

## What is already built and working

| Capability | Where |
|---|---|
| Preview + still capture | `camera_capture.c` (28 230 bytes) |
| **Face detection** | `camera_face_detect.cpp`, `BR2_PACKAGE_FACE_DETECT=y` — KPU-accelerated |
| **QR scanning** | `qr_scan.c` |
| **RTSP push** | `BR2_PACKAGE_CAMERA_RTSP_DEMO=y`, `BR2_PACKAGE_LIB_RTSPSERVER=y` |
| Motion probe | `drm_motion_probe.c` |
| Camera over LoRa FLRC | `k230_flrc_camera_stream.sh` |
| Camera over HaLow | `k230_halow_camera_stream.sh`, `halow_udp_stream.c` |
| UVC / OpenCV | Canaan `K230_Opencv_UVC_Usage_Guide`, `BR2_PACKAGE_*` OpenCV guides |

The **FLRC camera stream** is worth calling out: streaming images over a LoRa-family modulation
is unusual, and it is the concrete reason LilyGO gates Meshtastic photo transfer on LR2021
hardware.

## Adding a second or third camera

The K230 has **three MIPI CSI inputs** — (1 × 4-lane + 1 × 2-lane) or 3 × 2-lane. Only one is
populated. Canaan's reference DTS references `OV5647` and the tree mentions `IMX219`, so those
two are the least-effort additions. Procedure:
`K230_Image_Capture_Practice_How_to_support_a_new_sensor` and
`K230_Camera_Sensor_Adaptation_Guide`.

A community comment on the launch thread got this right: *"It might support two more cams. Might
be able to wrap their tethers around a tree and have a 360 degree view."*

## Limits

| Limit | Value | Class |
|---|---|---|
| CSI inputs | 3 | silicon |
| ISP throughput | 8 MP @ 30 fps | silicon |
| Encode | H.264/H.265/JPEG, 8 MP @ 20 fps | silicon |
| Decode | 8 MP @ 40 fps | silicon |
| Fitted sensor | 2 MP 1080p | board |
| Sensor lane count, link rate, HDR modes | **unknown** | [`GC-6`](../gaps-and-conflicts.md) |
| Measured capture latency / fps on this board | **none published** | unmeasured |

## Pitfalls

1. `0x37` is unusual for an image sensor — do not assume `0x3C`.
2. The camera has its **own** I²C bus, so it is not affected by keyboard-base bus problems.
3. ISP tuning is a real project. Canaan ships a PC-side tuning tool for a reason.
4. **nncase version must match the SDK** for KPU-accelerated vision, or you get a runtime failure.
