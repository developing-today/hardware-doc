# T-Display K230 — selected examples

Six selections from thirteen catalogued candidates ([`catalog.json`](catalog.json)). **None was
built or run**: no Ubuntu host and no XuanTie toolchain were available. Every "status" below is
`not-attempted`, and that is stated rather than hidden.

## Why this set looks unusual

This board has **no library, no `examples/` directory and no sketches**. Its software is one
Buildroot system image containing one large LVGL application. So the selections are a BSP, a set
of application modules, two companion-MCU firmware projects, an upstream SDK, and a recovery
tool — not a portfolio of demos.

## The selections

### 1. `K230-BSP-FULL` — the integrated application

`Xinyuan-LilyGO/T-Display-K230` @ `bb831ab358b66f5bd9a87ecd7c580fee4537492e`

The complete board support package plus launcher. Covers **every** feature simultaneously. Chosen
because there is no alternative: it is the board's software. Notable for pinning its SDK, kernel,
toolchain and LVGL, for 30+ named kernel patches, and for retaining a `.rejected` patch instead of
deleting it. **Has no licence file.**

### 2. `K230-LAUNCHER-MODULES` — the per-feature minimal examples

`k230_launcher/k230_phone_ui/src/`, same commit

~50 modules that between them are the minimal-example set. The one to read first is
**`ui_hardware.c`** — the single most information-dense file in the corpus, containing the
complete TCA8418 key map, the register set, the PMU power-key constants, the battery shutdown
policy and the XL9555 address-probe logic. The purpose-built diagnostics
(`drm_motion_probe.c`, `lvgl_scroll_probe.c`, `ui_i2c_scan.c`, `ui_display_test.c`,
`ui_i2s_test.c`, `ui_multitouch.c`, `ui_mic_spectrum.c`) are the **limit-testing** examples.

### 3. `K230-NRF52840-AT` — the best small buildable example

`Xinyuan-LilyGO/T-Display-K230-nRF52840` @ `4646a728580739d487126f47a521e9b8032b3c2c`

A single-purpose firmware with a documented AT surface, two DFU routes, and prebuilt binaries to
compare a local build against. It is the only example on this platform that a newcomer can build
in minutes with a standard toolchain (`pip install platformio && pio run`). Also the clearest
demonstration of the board's architecture: **the companion MCU exists because the SoC has no
Bluetooth**, and it also owns the 5 V boost enable.

### 4. `K230-NRF9151-SLM` — the best-engineered vendor fork

`Xinyuan-LilyGO/T-Display-K230-nRF9151` @ `ed4ecbe34162dec9b81213a400198125bbd6e36f`

Selected specifically as an example of *how to vendor upstream code properly*: the upstream Serial
LTE Modem is a **pinned submodule** at `13c80da97fe4d55ecb5a9745834d97be22821307`, the five
patches are named for what they do, and the README pre-empts the classic nRF91 confusion by
stating that `tfm_merged.hex` does **not** update the modem firmware. This is better hygiene than
most vendor forks in this repository.

### 5. `K230-LINUX-SDK` — the upstream

`kendryte/k230_linux_sdk`, branch **`dev`**, pinned by LilyGO at
`22d02c6b6783a57a3aca7eb3160e313e772cb710`. **BSD-2-Clause** — the only clearly-licensed item in
the set. Required to understand what LilyGO's overlay changes. Note the default branch is `dev`.

### 6. `OREBOOT` — the negative / recovery example

`oreboot/oreboot`, GPL-2.0, 1795★

Selected as the **useful negative example**. The failure mode this board actually exhibits is
"wrong boot medium, now unresponsive", and neither LilyGO nor this record has a tested procedure
for it. oreboot's K230 support, and the maintainer's public statement that it boots Linux from
mask ROM over USB in ~3 seconds, is the only credible documented route back in. Studying it is the
highest-value thing a reader with hardware can do.

## Deliberately not selected, with reasons

| Candidate | Reason |
|---|---|
| **`T-Display-K230_canmv_rt`** | **NOT EXAMINED.** 745 MB, 25★ — more than the main BSP's 1 — created 2025-03-05, last push 2026-08-03. **The largest known gap in this survey.** Start here next. |
| `kendryte/k230_sdk` (dual-OS) | Targets Canaan EVB/CanMV. Its images boot but drive none of this board's peripherals. |
| `canmv_k230`, `MaixPy` | K230-capable, **no board profile**. Display, touch and keyboard need porting. |
| `intx82/k230-debian` | Stale: last push 2024-12-03, 1★, not board-specific. |
| Independent Meshtastic UI | Announced 2026-06-02, **no repository located**. |
| Bruce firmware | **Wrong architecture** — ESP32-only. A refuted association, recorded so it is not chased again. |

## Feature coverage of the selected set

| Feature | Covered by |
|---|---|
| Display, touch, keyboard, camera, audio, microSD, USB, battery, GPIO, Wi-Fi, Ethernet, LoRa, KPU | `K230-BSP-FULL` + `K230-LAUNCHER-MODULES` |
| BLE | `K230-NRF52840-AT` |
| Cellular, GNSS | `K230-NRF9151-SLM` |
| Build system, toolchain | `K230-LINUX-SDK` |
| Recovery / boot ROM | `OREBOOT` |
| **Not covered by any example** | **HDMI beyond a test page; the DPU (no projector fitted); RGB-IR (no sensor); the two spare CSI inputs; deep sleep** |

## Validation status

**Zero built. Zero run. Zero hardware-tested.** The blocking requirements are an Ubuntu 22.04/24.04
host (or Docker) and the XuanTie toolchain at `/opt/toolchain`. The nRF52840 example is the
cheapest to validate — PlatformIO alone — and would be the sensible first thing to attempt.
