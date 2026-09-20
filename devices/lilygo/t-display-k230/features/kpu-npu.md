# KPU / NPU — running neural networks

**Question:** *How do I run a model on the K230's AI accelerator, and what will it actually do?*

| | |
|---|---|
| Accelerator | [K230](../../../../components/canaan/k230/README.md) **KPU**, INT8 + INT16, weight-sparse |
| Compiler | **nncase** |
| Dedicated SRAM | 2 MB (the second of two 2 MB blocks) |
| On-board packages | `BR2_PACKAGE_LIBNNCASE=y`, `BR2_PACKAGE_FACE_DETECT=y`, `BR2_PACKAGE_AI2D_KPU=y` |
| Evidence | `reported-working` for the shipped face-detect demo; everything else `not-tested` |

## Published throughput — use these, not TOPS

Canaan's datasheet gives three numbers and **no TOPS figure at all**:

| Network | Throughput |
|---|---|
| ResNet-50 | **≥ 85 fps @ INT8** |
| MobileNet v2 | **≥ 670 fps @ INT8** |
| YOLOv5s | **≥ 38 fps @ INT8** |

LilyGO's wiki says "**up to 1.6 TOPS**". A Reddit commenter said "**abt 17 tops**". Neither
number appears in any Canaan document. **Quote the fps figures.**

## Workflow

1. Train wherever you like — supported import formats are **TensorFlow, PyTorch, TFLite,
   PaddlePaddle, ONNX** (the brief datasheet lists TVM instead of TFLite/Paddle).
2. Compile with **nncase**, quantising to INT8 or INT16. Canaan claims **< 1 %** accuracy loss.
3. **Check the nncase ↔ SDK version table** — Canaan publishes
   `K230_SDK_nncase_version_correspondence.md` precisely because mismatches fail *at runtime*,
   not at build time. This is the number one KPU support issue.
4. Deploy and run against `libnncase` on the board.
5. Preprocess with the **AI 2D engine** (`BR2_PACKAGE_AI2D_KPU`) — affine, crop, resize, pad,
   shift and colour-space conversion in hardware, with OpenCV-compatible rounding. Doing resize
   and CSC on the CPU instead is the most common avoidable slowdown.

Reference: [`K230_nncase_Development_Guide.md`](../../../../components/canaan/k230/artifacts/K230_nncase_Development_Guide.md)
(81 128 bytes, retained locally).

## Supported operators

The full ONNX operator list Canaan commits to is reproduced verbatim in the
[K230 component record §3](../../../../components/canaan/k230/README.md#3-kpunpu--capability-and-supported-operators).
**Anything outside it falls back to CPU**, which on CPU0 at 800 MHz without vector instructions
is slow. If a model is unexpectedly slow, check the operator list before blaming the hardware.

## What ships working on this board

- **Face detection** from the live camera (`camera_face_detect.cpp`, `BR2_PACKAGE_FACE_DETECT`)
- An AI demo page (`ui_ai_demo.c`) and a `models/` directory in the launcher
- QR scanning (classical CV, not the KPU)

## Alternatives

| Route | When |
|---|---|
| **nncase + KPU** | Anything real-time. The only path that uses the accelerator. |
| **OpenCV on CPU1** | Classical CV. Canaan ships an OpenCV guide; CPU1 has RVV 1.0, so vectorised OpenCV is meaningful. |
| **OpenBLAS with RVV kernels** | Dense linear algebra. Canaan ships `K230_OpenBLAS_Development_Guide`. |
| **HHB (T-Head)** | Alternative deployment tool, documented in `K230_AI_in_Action_HHB_…`. |
| CPU0 | Do not. No vector unit. |

## Resources and conflicts

The KPU has 2 MB of SRAM by default and can reach the **shared** 2 MB block as well, where it has
priority over the AXI slaves. Sharing that block with the decompression engine and AI 2D work is
a real bandwidth question at 1080p. No measurement exists.

## Limits

| Limit | Value | Class |
|---|---|---|
| Precision | INT8 / INT16 only — **no FP inference** | silicon |
| Operators | fixed list; unsupported ops → CPU | silicon/toolchain |
| Model size | bounded by 1 GB LPDDR4 in practice | board |
| Measured performance on *this board* | **none** | unmeasured |
| LLM-class workloads | not credible — INT8 CNN accelerator, 1 GB RAM | inferred |

The launcher's **PicoClaw** chat app makes this explicit: it "requires network access and an
OpenAI-compatible model API key". The board does not run the model.

## Pitfalls

1. nncase/SDK version mismatch — the single most common failure.
2. Unsupported operators silently falling back to CPU.
3. Doing preprocessing on the CPU instead of the AI 2D engine.
4. Believing a TOPS number.
