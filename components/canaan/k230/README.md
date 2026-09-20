# Canaan Kendryte K230

- **Category:** dual-core 64-bit **RISC-V** AIoT application SoC with a KPU/NPU, 3D DPU, 2.5D GPU, H.264/H.265 VPU, ISP and MIPI DSI/CSI — **no radio, no Ethernet MAC, no on-die flash**
- **Manufacturer:** Canaan Creative Co., Ltd (嘉楠科技, NASDAQ: **CAN**), Kendryte® product line
- **Research status:** written from Canaan's own datasheet and brief datasheet (Markdown sources in the official `kendryte/k230_docs` repository, pinned commit) plus vendor BSP source. **No K230 hardware was executed or measured in this pass.**
- **Retrieved:** 2026-09-04
- **First RISC-V part in this repository.** Nothing in the repo's ESP-IDF/Xtensa toolchain guidance applies to it — see [§14](#14-software-toolchain-and-os-support).

---

## 1. Identity, family and variants

| Field | Value | Evidence |
|---|---|---|
| Marketed name | **Kendryte K230** | C1, C2 |
| Vendor | Canaan Creative (Kendryte brand) | C1 |
| Announced / datasheet V1.0 | **2023-07-06** (document revision date) | C1 |
| CPU cores | **two** XuanTie **C908** RISC-V 64-bit cores | C1, C2 |
| Package — K230 | **BGA, 0.65 mm pitch, 13 × 13 mm**, single die, external DRAM | C2 |
| Package — K230D | **BGA, 0.65 mm pitch, 11 × 11 mm**, SiP with **128 MB (1 Gb) 16-bit LPDDR4 @ 3200 Mbps** in package | C1, C2 |
| Max external DRAM | **2 GB** | C1, C2 |
| On-die SRAM | **2 MB shared + 2 MB KPU-default** | C1 |
| Embedded flash | **none** — boots from SD/eMMC or SPI NOR/NAND | C1 |
| Radio | **none** | C1 (no RF block in the feature list or block diagram) |
| Ethernet MAC | **none** | C1, C2 (negative result — see [§7](#7-what-the-k230-does-not-have)) |
| Operating temperature | **−40 … +85 °C** | C1, C2 |
| Deep-sleep standby | **≤ 20 µW** (vendor figure) | C2 |

### Naming and lineage

`K230` sits in Canaan's Kendryte AIoT line: **K210** (2018, dual RV64GC @ 400 MHz, 0.23 TOPS-class KPU, 8 MB on-die SRAM, no DDR) → **K510** (2021, *tri*-core RISC-V, up to 3 TOPS, C4) → **K230** (2023, dual C908, RVV 1.0). K230 is the successor to K210 in positioning and to K510 in capability; it is **not** a K510 derivative and shares no software with K210 beyond the "CanMV" MicroPython branding.

**Variant trap.** `K230` and `K230D` are different *packages of the same die*, distinguished only by whether an LPDDR4 die is co-packaged. A `K230D` board is memory-capped at **128 MB**; a `K230` board can carry up to 2 GB externally. Do not read a "K230" board specification as implying the D part or vice versa — the GPIO count also differs (**64 GPIO + 8 PMU GPIO** on K230 versus **50 GPIO + 6 PMU GPIO** in SiP form, C2).

`K256` appears in LilyGO's SKU strings for K230 boards (`K256`, `K256-A`, `K256-03`). **`K256` is a LilyGO stock code, not a Canaan part number** — see the [device record](../../../devices/lilygo/t-display-k230/README.md#1-identity-skus-and-variants).

---

## 2. The two C908 cores — which one has the vector unit

This is the single most misquoted fact about the part, so it is stated exactly as Canaan states it.

| | **CPU 1** ("big core") | **CPU 0** ("little/small core") |
|---|---|---|
| Max frequency | **1.6 GHz** | **800 MHz** |
| ISA | RV64 with **RISC-V Vector Extension **v1.0** | **RV64GCB** (G + Compressed + **B**itmanip) |
| Vector unit | **Yes — 128-bit VPU** | **No** |
| FPU | Yes | Yes |
| L1 | 32 KB I + 32 KB D | 32 KB I + 32 KB D |
| L2 | **256 KB** | **128 KB** |
| MMU | Yes | Yes |
| PLIC | own, 208 external sources | own, 208 external sources |
| JTAG | Yes | Yes |
| Canaan's intended OS | **RTOS** (RT-Thread / RT-Smart) | **Linux** | 

Evidence: C1 §"CPU subsystem", C2 §"CPU".

> **Only CPU1 has RVV 1.0.** Vector-optimised libraries (OpenBLAS RVV kernels, nncase runtime paths, the `-mcpu=c908v` build target) are meaningful only on CPU1. Code compiled with vector instructions will trap on CPU0.

### This is *not* a big.LITTLE cluster, and there is no third core

Two structural points that catch people coming from Arm SoCs or from the ESP32-P4:

1. **The two cores are separate subsystems, not a coherent cluster.** Each has its own L2 and its own PLIC with its own 208 interrupt sources. Canaan's own SDK runs *two different operating systems* simultaneously — RT-Smart on CPU1, Linux on CPU0 — with an explicit inter-processor communication API (`K230_Inter_Processer_Communication_API_Reference`) and a `sharefs` mechanism to share a filesystem between them. You do not schedule a Linux thread onto CPU1.
2. **There is no third CPU.** The datasheet's feature list contains exactly two CPU subsystems (C1). The **PMU** is a hardware block — 32 kHz RTC, 6 inputs / 2 outputs, long/short-press detection, edge/level detection with debounce, 512 bits of shutdown log — **not a programmable core** (C1 §PMU, C2 §PMU). Where the K230 is described as having "two cores plus a small core", the "small core" being referred to is **CPU0 itself**, which Canaan and its SDK call the *small core* (小核) in contrast to CPU1, the *big core* (大核). This is a naming collision, not a third processor.

   Contrast with **[ESP32-P4](../../espressif/esp32-p4/README.md)**, which genuinely does have a third, separate low-power RISC-V core (single-core, 40 MHz, retained LP power domain, LP peripherals and an LP mailbox). K230 has no equivalent: there is no retained programmable core, and the only always-on logic is the PMU's fixed-function RTC and key-detect state machine.

### Which core runs Linux — a live source conflict

| Source | Claim |
|---|---|
| Canaan brief datasheet (C2) | "CPU 1 … **runs RTOS** system"; "CPU 0 … **runs LINUX** system" |
| LilyGO wiki, T-Display K230 Quick Start FAQ, retrieved 2026-09-04 (D5) | "**big core runs Linux, little core runs RT-Thread** or bare-metal" |

Canaan's document is primary and its statement matches the SDK's own configuration names. **Treat the LilyGO wiki FAQ as wrong.** Recorded as conflict `GC-1` in the device record's [gaps-and-conflicts.md](../../../devices/lilygo/t-display-k230/gaps-and-conflicts.md). A third arrangement exists too: `kendryte/k230_linux_sdk` builds a **Linux-only** image, which is what the LilyGO T-Display K230 BSP is built from.

---

## 3. KPU / NPU — capability and supported operators

| Item | Value | Evidence |
|---|---|---|
| Precision | **INT8 and INT16** | C1, C2 |
| Weight sparsity | supported ("weight sparse compression") | C1, C2 |
| ResNet-50 | **≥ 85 fps @ INT8** | C1, C2 |
| MobileNet v2 | **≥ 670 fps @ INT8** | C1, C2 |
| YOLOv5s | **≥ 38 fps @ INT8** | C1, C2 |
| Frameworks | TensorFlow, PyTorch, TFLite, PaddlePaddle, ONNX (C1); C2 lists TVM instead of TFLite/Paddle | C1, C2 |
| Quantisation loss | **< 1 %** (vendor claim) | C1, C2 |
| Dedicated SRAM | 2 MB (the second 2 MB block defaults to KPU) | C1 |

### The TOPS number is a marketing figure, not a datasheet figure

**Neither the K230 full datasheet nor the brief datasheet states a TOPS rating.** They state the three network throughputs above and nothing else. The commonly repeated numbers come from downstream sources and they disagree:

- LilyGO's own wiki: "**up to 1.6 TOPS NPU**" (D5).
- A Reddit commenter, 2025-07-08: "the k230 has abt **17 tops**" — unsupported assertion, contradicted by every vendor figure; recorded here only because it circulates.

Use the fps figures. They are the ones Canaan is prepared to write down, and they are workload-defined.

### Supported ONNX operators (verbatim from C1)

Abs, Acos, Acosh, And, ArgMax, ArgMin, Asin, Asinh, Add, AveragePool, BatchNormalization, Cast, Ceil, Celu, Clip, Concat, Constant, ConstantOfShape, Conv, ConvTranspose, Cos, Cosh, CumSum, DepthToSpace, DequantizeLinear, Div, Dropout, Elu, Equal, Exp, Erf, Expand, Flatten, Floor, Gather, GatherElements, GatherND, Gemm, GlobalAveragePool, GlobalMaxPool, Greater, GreaterOrEqual, Hardmax, HardSigmoid, HardSwish, Identity, InstanceNormalization, LpNormalization, LeakyRelu, Less, LessOrEqual, Log, LogSoftmax, LRN, LSTM, MatMul, MaxPool, Max, Min, Mod, Mul, Neg, Not, OneHot, Pad, Pow, PRelu, QuantizeLinear, QLinearConv, QLinearMatmul, RandomNormal, RandomNormalLike, RandomUniform, RandomUniformLike, Range, ReduceL1, ReduceL2, ReduceLogSum, ReduceLogSumExp, ReduceMax, ReduceMean, ReduceMin, ReduceProd, ReduceSum, ReduceSumSquare, Relu, Reshape, Resize, ReverseSequence, Round, ScatterND, Selu, Shape, Sin, Sinh, Sigmoid, Sign, Size, Slice, Softmax, Softplus, Softsign, SpaceToDepth, Split, Sqrt, Squeeze, Sub, Sum, Tanh, Tile, TopK, Transpose, Upsample, Unsqueeze, Where.

Operators outside this list fall back to CPU through nncase, which is where most real-world "the model runs but it is slow" reports originate. The compiler is **nncase**; see `K230_nncase_Development_Guide.md` in the [artifacts](#16-local-artifacts).

---

## 4. Other accelerators

| Block | What it is | Headline numbers (C1) |
|---|---|---|
| **2D GDMA engine** | mirror / rotate 90-180-270, linked-list DMA, 64-bit AXI | 2 × 1080×1280 YUV400 @15 fps **+** 1 × 1080×1920 YUV420 @30 fps; max image 64K×64K; 8/16/24/32-bit pixels |
| **Non-AI 2D** | OSD, colour-space conversion, border draw, crop | — |
| **AI 2D engine** (independent) | affine / crop / resize / pad / shift / CSC, OpenCV-compatible rounding | source images up to 4K; can access the 2 MB system SRAM; DDR addresses want 16-byte alignment |
| **DPU** | 3D **structured-light** depth engine (Img_check / LCN / SAD / Post_proc / Align / Disptodepth) | 1280×800@30, 1280×1080@15, 1920×1080@9 fps; max 1920×1080 landscape, 1080×1440 portrait |
| **2.5D GPU** (VeriSilicon-style, VGLite driver) | tessellation, 16× MSAA at no throughput cost, 4 texels/cycle bilinear, alpha blend, frame-buffer compression, path/gradient draw | RGBA8888/BGRA8888/ABGR8888, RGBA5551, RGB565, A8/L8/RGB332, A4/L4, A2/L2, A1/L1, 1/2/4/8-bit indexed |
| **Decompression** | hardware **GZIP/DEFLATE** | **≥ 400 MB/s**, 32 KB dictionary, dynamic-Huffman only, CRC32, 32 KB max per DMA request |
| **FFT/IFFT** | up to **4096-point**, INT16 | 4096-point round trip **≤ 1 ms** including data movement and interrupt |

The GZIP block and the FFT block are unusual for this class and are easy to miss. The decompression engine is what makes Canaan's "fastboot: 3A first picture ≤ 400 ms" claim (C1, C2) achievable — boot images are shipped compressed and expanded in hardware.

---

## 5. Video, camera and display subsystems

| Subsystem | Capability | Evidence |
|---|---|---|
| **MIPI CSI-2 in** | **3 × CSI**, arranged as (1 × 4-lane + 1 × 2-lane) **or** 3 × 2-lane | C2 |
| **ISP** | total throughput **8 MP @ 30 fps**; 3A, 2DNR, 3DNR, WDR, HDR, local tone mapping, sharpen, BLS, LSC, de-warping, **RGB-IR 4×4** | C2 |
| **MIPI DSI out** | **1 × DSI**, 4-lane or 2-lane; **2 MP @ 60 fps** | C2 |
| **Video encode** | H.264 BP/MP/HP, H.265 MP, JPEG/MJPEG; **8 MP @ 20 fps**; CBR/VBR/CQP/ROI | C2 |
| **Video decode** | H.264 BP/MP/HP, H.265 MP, JPEG/MJPEG; **8 MP @ 40 fps** | C2 |

The RGB-IR 4×4 pattern support and the structured-light DPU together are the give-away that this part was designed for **face-unlock door locks and payment terminals** — Canaan's own application list leads with exactly that (C1).

---

## 6. Audio, memory and peripherals

**Audio (on-die codec — no external codec required for basic use):**
- **2 DAC channels**, stereo playback, **8–192 kHz**
- **2 ADC channels**, stereo mic capture, 8–192 kHz, with **ALC** (automatic level control)
- up to **8 PDM DMIC** inputs (1–4 IO pins, 32×/64×/128× oversampling, clocks 0.256–24.576 MHz)
- **I2S** with 2×2 expansion, master mode, full duplex; PDM-in, I2S-in and I2S-out can run simultaneously
- PCM over PDMA; APB2.0 register interface, PCLK default 100 MHz

**Memory controller:**
- **LPDDR4** 16-bit per channel × **2 channels** (so 32-bit total), max **3200 Mbps** per C1; C2 quotes **LPDDR4 @ 2667 Mbps** and the SiP at **3200 Mbps** — a vendor-internal inconsistency, recorded rather than resolved
- **LPDDR3** 32-bit @ 2133 Mbps; **DDR3L** @ 1600 Mbps (C2)
- max **2 GB**, up to 2 ranks, 1:2 clock ratio as configured by Canaan
- 5 AXI host ports, out-of-order execution, write combining, automatic power-down/clock-stop, periodic retraining, firmware 2D eye-mapping diagnostic

**Flash:** SPI NOR **and** SPI NAND, internal-DMA read/write, dual/quad/octal, DDR with read data strobe, **XIP from SPI NOR**.

**Low-speed peripherals (C2):** 5 × UART (16550-compatible, 32-deep FIFOs, fractional baud), 5 × I²C (standard/fast/fast+/**high-speed 3.4 Mb/s**, 7- and 10-bit), 6 × PWM, 64 GPIO + 8 PMU GPIO (50 + 6 on the SiP), WDT, RTC, timers.

**High-speed peripherals (C2):** 2 × **USB 2.0 OTG**, 2 × **SDxC** (SD 3.01 / eMMC 5.0, 4/8-bit, HS200/HS400, boot operation), 3 × SPI (1 × OSPI + 2 × QSPI, 256-deep FIFOs, 4–32-bit frames).

**Security (C1):** PUF, **32 kbit OTP** with protection, TRNG (160 Mbps @ 20 MHz, ≤ 50 µs stabilisation), AES-128/192/256, CMAC, SM4-128, RSA-1024…4096, ECC/ECDSA/ECDH across the usual curve set, SM2, HMAC, SHA-224…512 and the SHA-512/t truncations, SM3, and **secure boot with signature verification**.

**PMU (C1, C2):** 32 kHz RTC; default 6 inputs / 2 outputs, IO-configurable and reusable as GPIO up to 25 MHz; one long/short-press detector usable as shutdown or wake; one edge counter with periodic clear; two edge+level detectors with debounce; four edge/level detect groups; **two output IOs specifically for controlling an external PMIC and system reset**; 512 bits of retained shutdown log.

That last item matters at board level: **K230 expects an external PMIC**, and the PMU's job is to sequence it.

---

## 7. What the K230 does *not* have

Stated as positive negative results, each checked against the full feature list in C1 and the summary list in C2 on 2026-09-04:

| Absent | Consequence |
|---|---|
| **Any radio** — no Wi-Fi, no Bluetooth, no 802.15.4, no cellular | Every K230 board needs an external radio. On the LilyGO board that is an SDIO Wi-Fi module + a **USB** Bluetooth dongle. |
| **Ethernet MAC** | An RJ45 on a K230 board is a **USB**-attached Ethernet controller, not a MAC+PHY pair. This is exactly what LilyGO did (RTL8152B, [§Used By](#17-used-by)). |
| **On-die or in-package flash** | Boot media is external: SD, eMMC, SPI NOR or SPI NAND. |
| **A third / low-power programmable core** | No always-on core to hand sensor polling to. Compare ESP32-P4's LP core. |
| **CAN / TWAI** | Not in the peripheral list. |
| **A published TOPS figure** | See [§3](#the-tops-number-is-a-marketing-figure-not-a-datasheet-figure). |
| **A public errata document** | None located in `kendryte/k230_docs` or on the developer portal as of 2026-09-04. Absence of published errata is not absence of errata. |

---

## 8. Electrical and thermal

The full datasheet (C1) carries Absolute Maximum Ratings, Recommended Operating Conditions, general-IO DC characteristics, PLL characteristics, and separate electrical sections for **DDR, MIPI DSI, MIPI CSI, USB and SD/eMMC**. Working environment temperature is **−40 … +85 °C** (C1, C2). Deep-sleep standby is quoted at **≤ 20 µW** (C2).

**IO bank voltages are software-selected and can destroy the chip.** The board device tree sets a per-bank `MSC` field, and Canaan's own reference DTS carries the comment *"Please pay attention to the bank voltage! will damage the chip."* Banks are grouped `IO0–IO1` (fixed 1.8 V on the reference design), `IO2–IO13`, `IO14–IO25`, `IO26–IO37`, `IO38–IO49`, `IO50–IO61`, `IO62–IO63`. Getting a bank's `K230_MSC_1V8` / `K230_MSC_3V3` selection wrong against the external circuit is a documented hardware-damage path, not a soft failure. See the device record's [pinouts-and-buses.md](../../../devices/lilygo/t-display-k230/pinouts-and-buses.md).

Detailed numeric tables are in the retained datasheet artifact rather than copied here, because they are long and because the text layer of the Markdown source is trustworthy only for what has been cross-checked against the published HTML build.

---

## 9. Boot media and boot-ROM behaviour

| Mechanism | Detail | Evidence |
|---|---|---|
| Boot sources | SD (SDIO/SDMMC), eMMC (with boot and alternative-boot operation), SPI NOR, SPI NAND | C1 |
| Boot strapping | **`IO0` = BOOT0, `IO1` = BOOT1** on Canaan's reference DTS (both configured 1.8 V, output, pull-up in the reference pinmux) | C3 |
| USB recovery | Boot ROM can be driven over USB; Canaan ships **`k230_burntool`** (`K230_SDK_Burntool_User_Guide.md`) | C1 docs set |
| Third-party recovery | **oreboot** supports K230 and boots Linux **from mask ROM over USB in ~3 s**; author also publishes `kendryte_boot` | R1 |
| Secure boot | signature-verified, backed by OTP and PUF | C1 |

**The practical failure mode.** Selecting the wrong boot medium is recoverable *only* through the boot ROM's USB path. A T-Display K230 owner reported on 2026-08-21/28 that after flashing "into mmc mode vs sd card" the board was "**still unresponsive to boot pin and term**" (R2, firsthand ownership). If you are going to change boot configuration on a K230 board, know the USB boot-ROM path **before** you do it.

---

## 10. Documentation set and where it lives

Canaan publishes K230 documentation as **Markdown in a Git repository**, not as PDFs on a portal. This is unusual and it is the single most useful sourcing fact about the vendor.

| What | Where |
|---|---|
| Canonical repository | `github.com/kendryte/k230_docs`, branch `main` |
| Rendered HTML | `https://www.kendryte.com/k230/en/main/00_hardware/K230_datasheet.html` |
| Developer portal | `https://developer.canaan-creative.com/` (SDK images under *K230 → Images*, resources under `/resource`) |
| Language split | Everything exists twice: `en/…` and `zh/…`. **The `zh/` tree carries binary hardware artifacts the `en/` tree does not** — schematics (`.DSN`, PDF), Gerbers, PCB, DXF, SMT and BOM `.xlsx` for the K230 LP3 demo board, the LP4 USIP EVB and the K230D SIP EVB, plus `CanMV-K230-V1.0_2023-09-15.pdf`. If you only read `en/`, you will conclude no schematics are published. They are — under `zh/00_hardware/`. |
| Pinout | `《K230_PINOUT_V1.0_20230524》` is **referenced by the datasheet but not present in the repository** (C1 §"Pin information description"). Negative result, verified 2026-09-04 against the full recursive tree listing. |
| Licence | Repository is **BSD-2-Clause**; the datasheet body carries a **restrictive Canaan copyright notice** forbidding redistribution without written permission. The two disagree — see [§18](#18-licensing). |

Sourcing procedure and traps are written up once, reusably, in [`vendors/canaan/README.md`](../../../vendors/canaan/README.md).

---

## 11. Competing and substitute parts

Compared for the workload this part actually appears in: a battery-powered handheld or fixed appliance with a MIPI panel, a MIPI camera, on-device inference and a Linux userspace.

| Part | Cores | Vector/DSP | NPU | RAM | Display | Camera | Video codec | Radio | Ethernet MAC | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| **Canaan K230** | 2 × RV64 C908 @ 1.6 GHz + 0.8 GHz | **RVV 1.0, 128-bit, CPU1 only** | KPU INT8/INT16; ResNet-50 ≥ 85 fps | ext. LPDDR4 ≤ 2 GB (K230) / 128 MB SiP (K230D) | 1 × MIPI DSI, 2 MP@60 | **3 × MIPI CSI** | H.264 **and H.265** enc+dec, 8 MP@20/40 | **none** | **none** | 3D structured-light DPU, GZIP engine, FFT unit |
| **[Espressif ESP32-P4](../../espressif/esp32-p4/README.md)** | 2 × RV32 HP @ 400 MHz **+ 1 × RV32 LP @ 40 MHz** | Espressif PIE (AI/DSP ext.) | **none** | 16/32 MB **in-package PSRAM** | 1 × MIPI DSI | 1 × MIPI CSI | **H.264 encode only** | **none** | **yes** (RMII, ext. PHY) | Genuine third LP core; MCU-class RAM; ESP-IDF ecosystem |
| Allwinner V853 | 1 × Cortex-A7 @ 1 GHz + RISC-V E907 | NEON | 1 TOPS NPU | 64/128 MB DDR3 in-package | RGB/LVDS/MIPI DSI | 2 × MIPI CSI | H.264/H.265 enc | none | yes | Arm; mature Tina/Linux BSP; weaker vector story |
| Rockchip RV1106 | 1 × Cortex-A7 + RISC-V | NEON | 0.5 TOPS | 64/128/256 MB DDR3L in-package | MIPI DSI | 1 × MIPI CSI | H.264/H.265 enc | none | **yes** (10/100) | The IP-camera default; huge community; single A7 |
| Sophgo/CVITEK **CV1800B** | 1 × C906 @ 1 GHz + 1 × C906 @ 700 MHz | **no RVV** (C906 here is RV64GC) | 0.5 TOPS TPU | 64 MB DDR2 in-package | MIPI DSI | MIPI CSI | H.264/H.265 enc | none | yes | Milk-V Duo; cheapest RISC-V Linux; far less memory and no vector |
| Sophgo **SG2002** | C906 @ 1 GHz + C906 @ 700 MHz + 8051 | no RVV | 1 TOPS | 256 MB in-package | MIPI DSI | MIPI CSI | H.264/H.265 | none | yes | CV1800B successor, Arm-or-RISC-V selectable big core |

### K230 versus ESP32-P4, stated precisely

They are not the same class of part and the comparison is worth doing only because they are both "RISC-V, MIPI DSI + CSI, no radio" and land in similar handheld designs.

- **K230 is an application processor; ESP32-P4 is a high-end MCU.** K230 runs a full Linux distribution against gigabytes of external LPDDR4 with an MMU per core and 64-bit addressing. ESP32-P4 runs FreeRTOS against 768 KB of L2MEM plus 16–32 MB of in-package PSRAM and has no external DRAM interface at all. The step from 32 MB PSRAM to 1 GB LPDDR4 is roughly 30×, and it is what makes a browser, a Python stack or a general-purpose launcher possible on one and not the other.
- **K230 has a real NPU and a real H.265 codec; ESP32-P4 has neither.** The P4 has an H.264 *encoder* only, no decoder and no neural accelerator; K230 encodes and decodes H.264 and H.265 at 8 MP and adds an INT8/INT16 KPU quoted at ResNet-50 ≥ 85 fps.
- **ESP32-P4 wins on the things K230 omitted**: a genuine always-on low-power core with its own peripheral set, an Ethernet MAC, USB 2.0 High-Speed device *and* the ESP-IDF ecosystem with first-party Wi-Fi companion-chip support. K230's answer to all three is "add another chip on USB or SDIO".
- **Toolchain maturity is not close.** ESP-IDF is a single, versioned, well-documented SDK with a `nixpkgs-esp-dev` flake ([`guides/nixos/README.md`](../../../guides/nixos/README.md)). K230 requires a vendor XuanTie GCC tarball unpacked at a hard-coded `/opt/toolchain` path, Buildroot, a submodule SDK and — per Canaan's own instructions — Docker or Ubuntu 20.04/22.04. See [§14](#14-software-toolchain-and-os-support).

**Two-sentence summary.** The K230 is an application-class RISC-V SoC — gigabyte-scale external LPDDR4, MMU-backed Linux, a real INT8/INT16 NPU, H.264 *and* H.265 encode and decode, three MIPI CSI inputs and a structured-light depth engine — where the ESP32-P4 is a high-end microcontroller with 16–32 MB of in-package PSRAM, no NPU and H.264 encode only. In exchange the P4 gives you a genuine always-on low-power third core, an Ethernet MAC and the mature ESP-IDF toolchain, none of which the K230 has; K230's software story is a vendor Buildroot tree pinned to a hard-coded toolchain path.

---

## 12. Availability and pricing

**Bare-chip pricing was not established in this pass.** Canaan does not publish K230 unit pricing, no authorised-distributor line-card entry was located on Digi-Key, Mouser or LCSC on 2026-09-04, and the sales channel published on the datasheet is an email address (`salesAI@canaan-creative.com`). Treat any TR/tray price you find as unverified.

Board-level prices give the only usable floor, dated 2026-09-04 (see the device record's [market-and-pricing.md](../../../devices/lilygo/t-display-k230/market-and-pricing.md) for full observations):

| Board | Part | Observed | Date | Source |
|---|---|---|---|---|
| Banana Pi **BPI-CanMV-K230D-Zero** | K230**D** (SiP, 128 MB) | **$29** at announcement | 2024-11-18 | N2 |
| **CanMV-K230** | K230 + 512 MB | listed at launch, repeatedly out of stock | 2023-10 onward | N1, R3 |
| LilyGO **T-Display K230** | K230 + 1 GB | **$98.79** | 2026-09-04 | D1 |
| LilyGO **T-Display K230 Kit** | + keyboard base | **$150.31 / $153.01** | 2026-09-04 | D2 |

Community reports of purchasing difficulty are persistent and old: r/RISCV, 2024-05-08, "**Where do people buy CANMV K230 from?**" (R3); LilyGO's first T-Display K230 announcement thread, 2025-03-26, "**Already sold out**" (R4).

---

## 13. Notable K230 boards

| Board | Vendor | K230 variant | RAM | Distinguishing |
|---|---|---|---|---|
| **CanMV-K230** | Canaan | K230 | 512 MB | Reference board; 3 × camera; the board the SDK targets by default |
| K230 DEMO BOARD (LP3) / K230 USIP EVB (LP4) | Canaan | K230 | — | Full EDA source published under `zh/00_hardware/` |
| K230-SIP-EVB | Canaan | K230D | 128 MB | SiP evaluation board, EDA source published |
| **BPI-CanMV-K230D-Zero** | Banana Pi | K230D | 128 MB | $29 Zero-form-factor |
| **T-Display K230 / K230 Kit** | LilyGO | K230 | **1 GB** | 4.1″ AMOLED handheld, LoRa, keyboard base — [device record](../../../devices/lilygo/t-display-k230/README.md) |
| MaixCAM-derived K230 boards | Sipeed | K230 | varies | MaixPy runtime |

---

## 14. Software, toolchain and OS support

| Stack | Repository | Status |
|---|---|---|
| **k230_sdk** (dual-OS: RT-Smart on CPU1 + Linux on CPU0) | `kendryte/k230_sdk`, BSD-2-Clause, 273★, last push **2025-09-12** | The original, full-feature SDK. Docker image `ghcr.io/kendryte/k230_sdk` is the supported build environment. |
| **k230_linux_sdk** (Linux-only) | `kendryte/k230_linux_sdk`, branch `dev`, BSD-2-Clause, 62★, last push **2026-09-03** | Actively maintained; **this is what the LilyGO BSP builds on**, pinned at `22d02c6b6783a57a3aca7eb3160e313e772cb710`. |
| **CanMV / canmv_k230** (MicroPython) | `kendryte/canmv_k230`, 119★, last push 2026-09-03 | MicroPython on K230, the K210 "CanMV" lineage continued. |
| **MaixPy** | `sipeed/MaixPy`, 843★, last push 2026-08-28 | Sipeed's Python runtime; K230 is a supported target. |
| **nncase** | Canaan | Model compiler; version must match the SDK — Canaan publishes an explicit `K230_SDK_nncase_version_correspondence` table. Mismatched nncase/runtime pairs are a common failure. |
| **oreboot** | `oreboot/oreboot`, GPL-2.0, 1795★ | Third-party open firmware **with K230 support**; boots Linux from mask ROM over USB in ~3 s (R1). |
| **k230-debian** | `intx82/k230-debian`, BSD-2-Clause, kernel 6.6 branch, last push 2024-12-03, 1★ | Debian userspace experiment. Low activity — treat as a starting point, not a distribution. |
| **RT-Thread / RT-Smart** | upstream RT-Thread | The CPU1 OS in `k230_sdk`. |
| **Zephyr** | — | **No K230 board or SoC support found upstream** as of 2026-09-04. Negative result. |

### Toolchain reality

The compiler is **T-Head/XuanTie GCC**, not upstream RISC-V GCC. LilyGO's Buildroot defconfig pins it exactly:

```
BR2_TOOLCHAIN_EXTERNAL_PATH="/opt/toolchain/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V3.0.2/"
BR2_TOOLCHAIN_EXTERNAL_CUSTOM_PREFIX="riscv64-unknown-linux-gnu"
BR2_TARGET_OPTIMIZATION="-mcpu=c908v -mtune=c908 -mrvv-v0p10-compatible -mrvv-auto-vectorize"
```

Three things follow. First, `-mcpu=c908v` is a **XuanTie-specific** `-mcpu` value; mainline GCC does not know it. Second, `-mrvv-v0p10-compatible` means the shipped userspace is built for the **draft RVV 0.10** encoding even though the core implements ratified **RVV 1.0** — vendor toolchains carry this compatibility mode and binaries built with a mainline RVV-1.0 GCC are not interchangeable with it. Third, the path is **hard-coded to `/opt/toolchain/…`**, which is the specific detail that breaks NixOS and any non-FHS host.

The kernel is **not** mainline either: `BR2_LINUX_KERNEL_CUSTOM_REPO_URL="https://github.com/ruyisdk/linux-xuantie-kernel.git"` at commit `7d4e1f444f461dbe3833bd99a4640e7b6c2cd529`, defconfig `k230`.

NixOS-specific analysis, including why `pkgsCross.riscv64-embedded` does not substitute: [`guides/nixos/riscv-and-vendor-sdk-toolchains.md`](../../../guides/nixos/riscv-and-vendor-sdk-toolchains.md).

---

## 15. Known caveats and unsafe assumptions

1. **Do not assume RVV on CPU0.** Only CPU1 has the vector unit.
2. **Do not assume a coherent SMP pair.** Two OSes, two PLICs, IPC in between.
3. **Do not assume "K230" means "K230D"** or that a K230D board can be given more RAM. The DRAM is in the package.
4. **Do not assume a TOPS figure.** Canaan does not publish one.
5. **Do not assume Ethernet or any radio.** Neither exists on the die.
6. **Do not set IO bank voltages casually.** Canaan's own DTS warns this damages the chip.
7. **Do not mix nncase versions.** Canaan publishes a correspondence table because mismatches fail at runtime, not at build time.
8. **Do not treat `-mrvv-v0p10-compatible` binaries as RVV-1.0 binaries.**
9. **`K230_PINOUT_V1.0_20230524` is cited by the datasheet but not published.** Ball assignments must come from a board schematic.
10. **No errata document is published.** Plan verification accordingly.

---

## 16. Local artifacts

All retrieved 2026-09-04 from `github.com/kendryte/k230_docs` at commit **`f8e30213963e0ed5cf995c3cd4701218a45e4793`** (2025-09-12), raw path `https://raw.githubusercontent.com/kendryte/k230_docs/main/<path>`. Permalink form: `https://github.com/kendryte/k230_docs/blob/f8e30213963e0ed5cf995c3cd4701218a45e4793/<path>`.

| File | Upstream path | Bytes | SHA-256 | Establishes |
|---|---|---|---|---|
| `artifacts/K230_datasheet-v1.0-2023-07-06.md` | `en/00_hardware/K230_datasheet.md` | 83 002 | see [`artifacts/SHA256SUMS`](artifacts/SHA256SUMS) | Full feature list, packages, electrical sections |
| `artifacts/K230_brief_datasheet.md` | `en/K230_brief_datasheet.md` | 7 781 | ″ | Core roles, package sizes, peripheral counts, SiP memory |
| `artifacts/K230_Hardware_Design_Guide.md` | `en/00_hardware/K230_Hardware_Design_Guide.md` | 49 061 | ″ | Board-design rules |
| `artifacts/K230_PMU_User_Guide.md` | `en/01_software/board/osdrv/K230_PMU_User_Guide.md` | 10 039 | ″ | PMU register flow, power key, shutdown |
| `artifacts/K230_nncase_Development_Guide.md` | `en/01_software/board/ai/K230_nncase_Development_Guide.md` | 81 128 | ″ | KPU model compilation |
| `artifacts/K230_RVV_In_Action.md` | `en/02_applications/tutorials/K230_RVV_In_Action.md` | 12 528 | ″ | Practical RVV use on CPU1 |
| `artifacts/K230_RVV_optimization_performance_description.md` | `en/02_applications/tutorials/K230_RVV_optimization_performance_description.md` | 12 004 | ″ | Vector speed-up figures |

**Not retrieved, and why.** The binary hardware set under `zh/00_hardware/` — `CanMV-K230-V1.0_2023-09-15.pdf` (3.1 MB), `K230-SIP-EVB-V1.0-A.1-20230317.pdf` (967 KB), `K230-DEMO-BOARD-SCH.pdf` (969 KB), the `.DSN` OrCAD sources (1.7–1.85 MB each), and the Gerber/PCB/DXF/SMT/BOM archives — is **Canaan reference-board** material, not K230 die documentation, and none of it describes the LilyGO board. It is enumerated in [`artifacts/CANAAN-EDA-SET.md`](artifacts/CANAAN-EDA-SET.md) with exact paths, sizes and two reacquisition URLs each, so it can be fetched on demand without re-deriving the listing. Reacquisition status: **automatic**.

---

## 17. Used By

### [LilyGO T-Display K230 / T-Display K230 Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

The main SoC. **K230 (13 × 13 mm, non-SiP) with 1 GB of external LPDDR4** — LilyGO's own kit specification reads "32 LPDDR4, Capacity: 8 Gb", i.e. a 32-bit-wide bus (both 16-bit channels populated) and an 8 Gb = 1 GB device. This is four times the CanMV-K230 reference board and eight times a K230D.

How the board resolves each of the SoC's absences:

| K230 lacks | LilyGO's answer on this board |
|---|---|
| Wi-Fi | **RTL8189FS** over SDIO ([component](../../realtek/rtl8189fs/README.md)); the BSP also builds RTL8723DS and RTL8733BS drivers |
| Bluetooth | **USB dongle** — the BSP force-enables a CSR8510/8891 workaround and builds BlueZ; there is *no* on-board BT radio. LilyGO's wiki additionally claims an ESP32-S3-R8 co-processor, which the BSP does not corroborate — conflict `GC-2` |
| Ethernet MAC | **RTL8152B USB 10/100** ([component](../../realtek/rtl8152b/README.md)) behind the RJ45 |
| Cellular / GNSS | **nRF9151** on the keyboard base, over UART3 |
| BLE central | **nRF52840** on the expansion base, over UART1 |
| PMIC | present but unidentified — [`components/unidentified/t-display-k230`](../../unidentified/t-display-k230/README.md) |

K230 signals used, from LilyGO's own BSP pin map (D3): MIPI DSI → RM69A10 AMOLED with `GPIO22` reset and `GPIO25` enable; MIPI CSI + I²C0 (`GPIO48/49`) → GC2093; I²C3 (`GPIO36/37`) → GT9895 touch at `0x5D`, `GPIO23` IRQ, `GPIO24` reset; MMC1 (`GPIO54–59`) → microSD, which is also the boot medium; SDIO → Wi-Fi; SPI (`GPIO14–17`, `19`, `20`, `44`) → SX1262/LR2021 LoRa; UART1 (`GPIO3/4`) → nRF52840; UART3 (`GPIO28/29`) → nRF9151; I²C4 (`GPIO46/47`) → the whole keyboard-base I²C bus; I2S (`GPIO32–35`) → MAX98357A; PWM4 (`GPIO52`) → keyboard backlight; `GPIO0` = BOOT0 button; `GPIO64` = PMU INT0 power key. Full table: [pinouts-and-buses.md](../../../devices/lilygo/t-display-k230/pinouts-and-buses.md).

LilyGO ships a Linux-only image built from `k230_linux_sdk`, so on this board **Linux runs on CPU0 and CPU1 is not running RT-Smart** in the default configuration.

---

## 18. Licensing

| Artifact class | Terms | Evidence | Disposition |
|---|---|---|---|
| `kendryte/k230_docs` repository as a whole | **BSD-2-Clause** (GitHub-detected licence on the repository) | C4 | `repository`, unstaged |
| The datasheet *text* | "**without the written permission of the company, any unit or individual shall not disseminate part or all of the content of this document in any form**" | C1 §Trademark Notice | **conditional / conflicting** |

These two are in direct conflict: the repository is published under a permissive licence that grants redistribution, while the document inside it carries a notice forbidding it. **Recorded, not resolved.** The retained copies are held unstaged pending a user decision. The safe reading is that Canaan applied a boilerplate corporate notice to a document it then published under BSD-2-Clause and did not reconcile the two.

Redistribution status: **unknown/conflicting**. Disposition: **repository (unstaged)**.

---

## 19. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published/updated | Establishes |
|---|---|---|---|---|---|---|---|---|
| C1 | K230 Product Full Datasheet, **V1.0** | Canaan Creative | primary | datasheet (Markdown) | `https://github.com/kendryte/k230_docs/blob/f8e30213963e0ed5cf995c3cd4701218a45e4793/en/00_hardware/K230_datasheet.md` | 2026-09-04 | doc **2023-07-06**; repo commit 2025-09-12 | Complete feature list, KPU operators, packages, electrical sections, security, PMU |
| C2 | K230 Brief Datasheet | Canaan Creative | primary | datasheet (Markdown) | `https://github.com/kendryte/k230_docs/blob/f8e30213963e0ed5cf995c3cd4701218a45e4793/en/K230_brief_datasheet.md` | 2026-09-04 | repo commit 2025-09-12 | Core roles and frequencies, package dimensions, SiP memory, peripheral counts |
| C3 | `k230_canmv_v3.dts` (U-Boot, Canaan copyright 2023) | Canaan / LilyGO overlay | primary | source | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/overlay/buildroot-overlay/boot/uboot/u-boot-2022.10-overlay/arch/riscv/dts/k230_canmv_v3.dts` | 2026-09-04 | commit 2026-09-03 | IO bank voltage warning, BOOT0/BOOT1 on IO0/IO1, per-pin mux |
| C4 | `kendryte/k230_docs` repository metadata | Canaan Creative | primary | repository | `https://github.com/kendryte/k230_docs` | 2026-09-04 | HEAD `f8e3021…`, 2025-09-12 | Licence field BSD-2-Clause; full file inventory incl. `zh/00_hardware` EDA set |
| C5 | `kendryte/k230_linux_sdk` repository metadata | Canaan Creative | primary | repository | `https://github.com/kendryte/k230_linux_sdk` | 2026-09-04 | pushed 2026-09-03 | Active Linux-only SDK, BSD-2-Clause |
| D1 | T-Display K230 product page + `/products/t-display-k230.js` | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230` | 2026-09-04 | published 2025-03-21 | SKUs K256/-A/-B/-C, $98.79, SoC/display specification |
| D2 | T-Display K230 Kit product page + `.js` | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230-kit` | 2026-09-04 | published 2026-08-20 | Kit SKUs, prices, full component list incl. RTL8189, GC2093, 8 Gb LPDDR4 |
| D3 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | commit 2026-09-03 | Complete K230 pin/bus/peripheral map |
| D4 | `k230_canmv_t_display_rm69a10_defconfig` | LILYGO | primary | source | same repo, `k230_bsp/overlay/buildroot-overlay/configs/` | 2026-09-04 | commit 2026-09-03 | XuanTie toolchain path and flags, kernel repo/commit, Wi-Fi packages |
| D5 | T-Display K230 wiki page | LILYGO | primary | official wiki | `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/` | 2026-09-04 | undated | 1.6 TOPS claim, ESP32-S3-R8 claim, RTL8152B Ethernet, big/little-core FAQ error |
| N1 | "CanMV-K230 AI development board features Kendryte K230 dual-core 64-bit RISC-V processor" | CNX-Software | community | blog | `https://www.cnx-software.com/2023/10/24/canmv-k230-ai-development-board-features-kendryte-k230-dual-core-64-bit-risc-v-processor/` | 2026-09-04 | 2023-10-24 | Launch-era independent coverage |
| N2 | "$29 Banana Pi BPI-CanMV-K230D-Zero features Kendryte K230D RISC-V SoC" | CNX-Software | community | blog | `https://www.cnx-software.com/2024/11/18/29-banana-pi-bpi-canmv-k230d-zero-features-kendryte-k230d-risc-v-soc-for-aiot-applications/` | 2026-09-04 | 2024-11-18 | K230D board pricing datum |
| N3 | "Kendryte K510 tri-core RISC-V AI processor deliver up to 3 TOPS" | CNX-Software | community | blog | `https://www.cnx-software.com/2021/07/09/kendryte-k510-tri-core-risc-v-ai-processor-3-tops/` | 2026-09-04 | 2021-07-09 | K510 lineage datum |
| R1 | r/LilyGO comment by u/CyReVolt | Reddit | community | forum (**demonstrable project** — oreboot maintainer) | `https://old.reddit.com/r/LilyGO/comments/1jgb4kn/tdisplay_k230_is_available/` | 2026-09-04 | 2025-03-26 | oreboot K230 support; Linux from mask ROM over USB in ~3 s; `kendryte_boot` tool |
| R2 | r/LilyGO comments by u/phirzcolru | Reddit | community | forum (**firsthand ownership**) | `https://old.reddit.com/r/LilyGO/comments/1vtcjuj/the_tdisplay_k230_kit_is_finally_here/` | 2026-09-04 | 2026-08-21 / 2026-08-28 | Bricked by boot-medium change; unresponsive to boot pin |
| R3 | "Where do people buy CANMV K230 from?" | Reddit r/RISCV | community | forum | `https://old.reddit.com/r/RISCV/comments/1cmyur9/where_do_people_buy_canmv_k230_from/` | 2026-09-04 | 2024-05-08 | Availability difficulty |
| R4 | "T-Display K230 is available!" thread | Reddit r/LilyGO | community | forum | `https://old.reddit.com/r/LilyGO/comments/1jgb4kn/` | 2026-09-04 | 2025-03-21 | Launch date, immediate sell-out |
| R5 | "Kendryte K230 (RVV1.0 supported) available for remote access" | Reddit r/RISCV | community | forum | `https://old.reddit.com/r/RISCV/comments/1cnsdlh/kendryte_k230_rvv10_supported_available_for/` | 2026-09-04 | 2024-05-09 | RVV 1.0 interest; remote-access offer |

---

## 20. Related records

- Device using this part: [LilyGO T-Display K230](../../../devices/lilygo/t-display-k230/README.md)
- Nearest comparable in this repository: [Espressif ESP32-P4](../../espressif/esp32-p4/README.md)
- Vendor sourcing guide: [`vendors/canaan/README.md`](../../../vendors/canaan/README.md)
- Host toolchain notes: [`guides/nixos/riscv-and-vendor-sdk-toolchains.md`](../../../guides/nixos/riscv-and-vendor-sdk-toolchains.md)
