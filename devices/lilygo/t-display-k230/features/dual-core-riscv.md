# The two RISC-V cores, RVV, and what "small core" means

**Question:** *There are two cores with different capabilities — which is which, which one runs
my code, and how do I use the vector unit?*

| | CPU 1 — "big core" | CPU 0 — "little/small core" |
|---|---|---|
| Clock | **1.6 GHz** | **800 MHz** |
| ISA | RV64 + **RVV 1.0**, 128-bit VPU | **RV64GCB** — no vector |
| L2 | 256 KB | 128 KB |
| L1 | 32 KB I + 32 KB D | 32 KB I + 32 KB D |
| MMU / FPU / PLIC (208 sources) / JTAG | yes | yes |
| Canaan's intended OS | **RTOS** (RT-Smart) | **Linux** |

Both are **XuanTie C908** cores. Evidence: Canaan K230 datasheet and brief datasheet.

## Three things people get wrong

**1. Only CPU1 has the vector unit.** Vector code traps on CPU0. Every RVV-accelerated library —
OpenBLAS RVV kernels, vectorised OpenCV, nncase vector paths — is a CPU1 story.

**2. There is no third core.** The K230 has exactly two CPU subsystems. Where you see "two cores
plus a small core", the "small core" **is CPU0** — that is Canaan's own name for it (小核), in
contrast to CPU1, the big core (大核). The **PMU is fixed-function hardware**: a 32 kHz RTC, six
inputs, two outputs, long/short-press detection and a 512-bit shutdown log. It is not
programmable. Contrast the [ESP32-P4](../../../../components/espressif/esp32-p4/README.md), which
genuinely does have a third 40 MHz RISC-V core on a retained power domain with its own
peripherals — the K230 has no equivalent.

**3. It is not an SMP pair.** Two independent L2 caches, two independent PLICs, and in Canaan's
dual-OS SDK **two different operating systems** with an explicit IPC API
(`K230_Inter_Processer_Communication_API_Reference`) and a `sharefs` mechanism. You do not
schedule a Linux thread onto CPU1.

## On *this board*, specifically

LilyGO builds from **`kendryte/k230_linux_sdk`**, which is the **Linux-only** SDK. So the dual-OS
arrangement above is not what this board ships. What exactly runs on CPU1 in the Linux-only
configuration was **not established** in this pass — see [`GC-1`](../gaps-and-conflicts.md) —
and `cat /proc/cpuinfo` on a running unit settles it in one command.

⚠ LilyGO's wiki FAQ states the opposite of Canaan's datasheet ("big core runs Linux, little core
runs RT-Thread"). **Canaan is primary; the wiki is wrong.**

## Using RVV

The Buildroot target flags are:

```
BR2_TARGET_OPTIMIZATION="-mcpu=c908v -mtune=c908 -mrvv-v0p10-compatible -mrvv-auto-vectorize"
BR2_RISCV_ISA_RVV=y
BR2_RISCV_ISA_RVC=y
```

Three consequences:

1. **`-mcpu=c908v` is XuanTie-specific.** Mainline GCC does not accept it.
2. **`-mrvv-v0p10-compatible` targets draft RVV 0.10**, not ratified 1.0, even though the core
   implements 1.0. Binaries are **not** interchangeable with mainline RVV-1.0 output.
3. `-mrvv-auto-vectorize` is on, so ordinary C gets auto-vectorised for CPU1.

Canaan's own tutorials, retained locally:
[`K230_RVV_In_Action.md`](../../../../components/canaan/k230/artifacts/K230_RVV_In_Action.md) and
[`K230_RVV_optimization_performance_description.md`](../../../../components/canaan/k230/artifacts/K230_RVV_optimization_performance_description.md).

## DVFS

CPU1 and the KPU both support DVFS. When they share a clock source their frequencies change
together; on separate sources they change independently. Frequency must match the current
voltage — this is the PMIC's job, and the PMIC on this board is
[unidentified](../../../../components/unidentified/t-display-k230/README.md).

## Limits

| Limit | Value | Class |
|---|---|---|
| Vector length | 128-bit | silicon |
| RVV version implemented | 1.0 | silicon |
| RVV version the shipped toolchain targets | **0.10-compatible** | toolchain |
| Cores | 2, no third | silicon |
| CoreMark on this board | **built into the image, never published** | unmeasured |

## Pitfalls

1. Compiling with vector instructions and running on CPU0.
2. Mixing mainline-RVV-1.0 and XuanTie-0p10-compatible binaries.
3. Expecting an always-on core for sensor polling. There isn't one.
4. Expecting `taskset` to move work to the fast core in a dual-OS configuration.
