# T-Display K230 — performance

**There is no independent performance measurement of this board. None. In any source searched.**

That statement is the most important content on this page, so it comes first. What follows
separates what Canaan claims about the silicon from what is known about the board, and says
exactly how to close the gap.

## 1. Silicon claims — vendor figures, not measurements

From Canaan's K230 datasheet and brief datasheet. These are **official claims** produced under
Canaan's own build and configuration, on Canaan's own boards.

| Workload | Claim |
|---|---|
| ResNet-50 INT8 (KPU) | **≥ 85 fps** |
| MobileNet v2 INT8 (KPU) | **≥ 670 fps** |
| YOLOv5s INT8 (KPU) | **≥ 38 fps** |
| Video encode | H.264/H.265, **8 MP @ 20 fps** |
| Video decode | H.264/H.265, **8 MP @ 40 fps** |
| ISP throughput | **8 MP @ 30 fps** |
| DPU depth | 1280×800 @ 30 fps · 1280×1080 @ 15 fps · 1920×1080 @ 9 fps |
| 2D GDMA rotation | 2 × 1080×1280 YUV400 @ 15 fps **+** 1 × 1080×1920 YUV420 @ 30 fps |
| GZIP decompression | **≥ 400 MB/s** |
| 4096-point FFT/IFFT | **≤ 1 ms** including data movement and interrupt |
| Boot to first 3A image | **≤ 400 ms** |
| Deep-sleep standby | **≤ 20 µW** |
| Operating temperature | −40 … +85 °C |

**No CoreMark or DMIPS figure is published for the K230 by Canaan.** Compare
[ESP32-P4](../../../components/espressif/esp32-p4/README.md), where Espressif quotes
6.92 CoreMark/MHz.

**No TOPS figure is published either.** LilyGO's wiki says "up to 1.6 TOPS"; a Reddit commenter
said "abt 17 tops". Neither number appears in any Canaan document. Use the fps figures.

## 2. What is known about *this board*

| Metric | Value | Class |
|---|---|---|
| CPU1 clock | 1.6 GHz | vendor spec |
| CPU0 clock | 800 MHz | vendor spec |
| RAM | 1 GB LPDDR4, 32-bit | vendor spec — but see [`GC-7`](gaps-and-conflicts.md) |
| Ethernet | 100 Mbit/s ceiling | vendor spec |
| Wi-Fi | 802.11n, 2.4 GHz only | vendor spec |
| USB charge input | 5 V, 500 mA | vendor spec |
| **Everything else** | **unmeasured** | — |

Unmeasured and unpublished: boot time, LVGL frame rate, display refresh rate, camera capture
latency, Wi-Fi throughput, Ethernet throughput, SD throughput, LoRa range and TX current, KPU
inference latency on this board, thermal behaviour under load, **and battery life under any
workload whatsoever.**

## 3. The board ships with benchmarks nobody has run

This is the striking part. The Buildroot configuration contains:

```
BR2_PACKAGE_COREMARK=y
BR2_PACKAGE_COREMARK_PRO=y
```

**CoreMark and CoreMark-PRO are built into every image LilyGO produces**, and no CoreMark result
for this board exists anywhere. A single command on a running unit would produce the first
published number.

Also built in and unused for measurement: `evtest`, `linux-tools-gpio`, `alsa-utils`, plus
LilyGO's own `drm_motion_probe.c`, `lvgl_scroll_probe.c` and `lora_flrc_bench.cpp` — three
purpose-built probes whose outputs have never been published.

## 4. Reasoning that is *not* measurement

One community comparison is worth recording because it is the only quantitative reasoning found,
and it is **informed interpretation, not a measurement** (r/meshtastic, 2025-07-09):

> "This board has 1G ram and a 1.6GHz RVV1 'big' core. It's basically more powerful than the
> 1GHz non RVV core in my MQ-Pro, and has 8x the memory."

Comparing to the Allwinner D1 in a MangoPi MQ-Pro: the clock ratio (1.6× ) and the memory ratio
(8×) are both correct arithmetic on published specifications, and RVV 1.0 versus the D1's draft
RVV 0.7.1 is a real architectural difference. **But it is inference from specifications, and
specification-derived performance claims are exactly what this repository does not accept as
measurement.** Recorded, labelled, not promoted.

## 5. What would close the gap — a concrete protocol

Every command below runs on the shipped image with no additional software. Anyone with hardware
could produce all of it in an afternoon, and it would be the first performance data that exists
for this product.

| Measurement | Command | Record alongside |
|---|---|---|
| CPU | `coremark` (and `coremark-pro`) | which core it ran on (`taskset`), governor, clock, ambient |
| Memory | `sysbench`/`mbw` if added, else a simple `dd` to `/dev/null` from tmpfs | frequency, single vs dual channel |
| Boot time | `systemd-analyze` if present, else timestamped `dmesg` | to first LVGL frame, not just to shell |
| Display | `lvgl_scroll_probe`, `drm_motion_probe` | resolution, colour format, buffering |
| SD | `dd` and `fio` if added | card make/model/class — **this dominates the result** |
| Wi-Fi | `iperf3` | AP model, distance, band, channel width, RSSI |
| Ethernet | `iperf3` | link speed, switch |
| KPU | run the shipped face-detect at a fixed resolution and time it | nncase version, model, input size |
| Camera | timestamp V4L2 buffer dequeues | resolution, format, ISP settings |
| **Battery** | log BQ27220 voltage/current/SoC over a defined workload | **cell capacity, screen brightness, radios on/off** — without these the number means nothing |
| Thermal | read the Canaan thermal sensor under sustained load | ambient, warm-up time, duration, throttling observed |
| Power | external meter at the USB-C input | measurement point and instrument |

**Do not merge results across different SD cards, different image versions or different
governors into one ranking.** The single largest confounder on this board is the SD card, because
the card is the root filesystem.
