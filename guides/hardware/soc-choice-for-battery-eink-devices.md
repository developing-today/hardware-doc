# SoC choice for a battery-powered e-ink device

> Why the devices in this repository pick what they pick — **ESP32-C3 vs ESP32-S3
> vs ESP32-P4 vs Kendryte K230 vs nRF52840/nRF9151** — and what each choice costs
> in memory, sleep current, radio complexity, toolchain effort and price.
>
> **Every number below is cited to a record already in this repository. Nothing was
> retrieved, measured or benchmarked for this page.** Where a figure does not exist
> here, it is marked **`no figure in this repository`** rather than filled in from
> memory. §2 is a list of those gaps and it is longer than anyone would like.

## 0. The short answer

| If your device is… | Pick | Because |
|---|---|---|
| A **1-bit e-ink reader** that must be cheap and small | **ESP32-C3** | 400 KB SRAM holds a 1 bpp 800×480 plane with room to spare, and the radio is integrated. **But it will be the thing that limits your firmware** |
| An e-ink reader with **greyscale, partial refresh, a big font set or a large library index** | **ESP32-S3 with PSRAM (`R8`)** | 8 MB in-package PSRAM is the difference between multi-buffer rendering and not. This is the default choice, and the one four of the six documented e-ink devices made |
| A **colour GUI handheld** with a camera or a DSI panel | **ESP32-P4** | 16–32 MB PSRAM, MIPI-DSI/CSI, a pixel-processing accelerator — **and no radio at all**, so budget a companion chip |
| A device that must run **Linux, Python, SSH** or a neural network | **Kendryte K230** | 1 GB LPDDR4, an NPU, H.265 encode *and* decode. And **no radio, no Ethernet MAC, and nothing from the ESP32 ecosystem applies** |
| A **BLE companion** or a **cellular/GNSS** link | **nRF52840 / nRF9151** | In this repository both appear only as companions to a bigger SoC, never as the application processor |

**The single most consequential decision is PSRAM, and it is made when you pick the
part number, not later.** `ESP32-S3FN8` and `ESP32-S3R8` are both "an ESP32-S3" and
they are opposite choices: `FN8` = 8 MB flash in package, **no PSRAM**; `R8` =
8 MB PSRAM in package, **no flash** (you add an external chip). Every Cardputer is
`FN8`, and that is *"the single most consequential fact about every Cardputer"*
([`esp32-s3fn8`](../../components/espressif/esp32-s3fn8/README.md)).

---

## 1. The candidates, side by side

Only cells with a citable source are filled. Everything else says so.

| | [**ESP32-C3**](../../components/espressif/esp32-c3/README.md) | [**ESP32-S3R8**](../../components/espressif/esp32-s3r8/README.md) | [**ESP32-S3FN8**](../../components/espressif/esp32-s3fn8/README.md) | [**ESP32-P4**](../../components/espressif/esp32-p4/README.md) | [**Kendryte K230**](../../components/canaan/k230/README.md) | [**nRF52840**](../../components/nordic-semiconductor/nrf52840/README.md) | [**nRF9151**](../../components/nordic-semiconductor/nrf9151/README.md) |
|---|---|---|---|---|---|---|---|
| **Core(s)** | 1 × RISC‑V RV32IMC, ≤160 MHz | 2 × Xtensa LX7, ≤240 MHz | same as S3R8 | **2 × RISC‑V HP ≤400 MHz + 1 × RISC‑V LP ≤40 MHz** | **2 × RV64 XuanTie C908 — CPU1 1.6 GHz with RVV 1.0, CPU0 800 MHz RV64GCB** | *not in this record* | *not in this record* |
| **On-chip SRAM** | **400 KB** | **512 KB** | 512 KB | **768 KB L2MEM** (SRAM *or* L2 cache for PSRAM) + 8 KB SPM + **32 KB LP SRAM, retained in deep sleep** | *not stated in the record* | — | — |
| **PSRAM / DRAM** | **none** on the documented boards | **8 MB octal, in package** | **none** | **16 MB (`NRW16`) or 32 MB (`NRW32`), in package** | **external LPDDR4, up to 2 GB** (1 GB fitted on the T‑Display K230) | — | — |
| **Flash** | external (16 MB on the Xteinks) | **none in package** — external required | **8 MB in package** | **none on any variant** — external required | **none on die** — boots from microSD on the documented board | — | — |
| **Radio** | Wi‑Fi 2.4 GHz b/g/n + **BLE 5**. **No Bluetooth Classic** | Wi‑Fi 4 + **BLE 5 + Mesh**. **No Bluetooth Classic** (silicon-level) | same | **None of any kind** | **None.** Also **no Ethernet MAC** | BLE | **LTE‑M / NB‑IoT + GNSS** |
| **USB** | USB Serial/JTAG — no bridge IC needed | USB 2.0 OTG + Serial/JTAG | same | USB 2.0 **High-Speed** OTG | — | **USB 2.0 full-speed device** (this is what makes UF2 drag-and-drop bootloaders possible) | — |
| **Display path** | SPI | SPI / QSPI / parallel-8080 (LCD_CAM) | same | **MIPI-DSI + MIPI-CSI + ISP + H.264 enc + JPEG + PPA + 2D-DMA** | **MIPI DSI/CSI + KPU/NPU + DPU + 2.5D GPU + H.264/H.265 VPU + ISP** | — | — |
| **Deep-sleep current** | **no figure in this repository** | **no figure in this repository** | **no figure in this repository** | **no µA figure**; the record establishes the *architecture* (LP domain retained, HP gated) | **≤ 20 µW standby** — vendor figure | **no figure** — the datasheet was **not downloaded** | **no figure** |
| **Vendor perf claim** | — | — | — | **6.92 CoreMark/MHz dual-core** → ≈2 768 CoreMark at 400 MHz. Espressif's own build; no independent reproduction found | ⚠ the TOPS number is *"a marketing figure, not a datasheet figure"* | — | — |
| **Documentation maturity** | ⚠ **the datasheet was never retrieved** into this repository (`not-attempted`) | datasheet + TRM v1.8 held locally | derived from M5Stack schematics + vendor BSP | ⚠ the datasheet is a **pre-release** document | datasheet + brief datasheet from Canaan's own `k230_docs` repo | ⚠ **product specification not downloaded** | ⚠ **AT command reference behind a restricted path, not retrieved** |
| **Documented in this repo as** | Xteink X3, X4 | PaperMono, Waveshare 3.97, all 11 LilyGO T‑Display‑S3 boards, Waveshare knob, XIAO Sense | every Cardputer, DinMeter | Tanmatsu, Waveshare P4 boards, Espressif P4 boards | LilyGO T‑Display K230 | **companion** on the K230 base board | **companion** on the K230 keyboard base |

---

## 2. ⚠ The numbers this repository does not have

State these first, because the rest of the page is shaped by them.

**There is no deep-sleep current figure for the ESP32-C3, ESP32-S3 or ESP32-P4
anywhere in this repository.** The C3 component record has no power table at all
and its datasheet is recorded as `not-attempted`. The S3R8 record covers the radio,
PSRAM, PIE/SIMD and package pins but no sleep figures. The P4 record describes the
*architecture* of the low-power domain — the LP core runs on a retained domain
doing sensor polling and wake decisions while the two HP cores stay powered down —
but gives no current.

**So this page cannot rank these parts on sleep current, and does not.** Anyone who
needs that must fetch the datasheets; note the repository's own precedent that
three agents once fetched three ESP32-S3 datasheets from three portals and got
**three different SHA-256 values and three different sizes**.

What *does* exist here is **board-level** sleep and idle claims, which are a
different quantity — they include regulators, load switches, an expander, a PMIC
and whatever the vendor left powered — and every one of them is a vendor claim
under **unstated conditions**:

| Board figure | Value | Source record |
|---|---|---|
| Cardputer v1.0 / v1.1 / ADV, **power switch OFF** | 0.26 / 0.15 / **0.23 µA** at 4.2 V | [Cardputer ADV](../../devices/m5stack/cardputer-adv/README.md) |
| M5Stack **Stamp-S3 → Stamp-S3A**, `VIN_5V` sleep | **310.89 µA → 6.84 µA** | [Cardputer v1.1](../../devices/m5stack/cardputer-v1.1/README.md) |
| Stamp-S3 → Stamp-S3A, standby | 33.5 mA → **25.5 mA** | idem |
| Cardputer ADV operating, 4.2 V | **120.2 mA** idle · 132.3 mA Wi-Fi · **154.6 mA BLE** | [Cardputer ADV](../../devices/m5stack/cardputer-adv/README.md) |
| Cap CC1101 & NFC, both radios asleep | **140.87 µA @ 5 V** | [Cap CC1101](../../devices/m5stack/cap-cc1101/README.md) |
| Unit C6L (ESP32-C6 + SX1262), sleep | **696.86 µA** (Grove) / 866.42 µA (USB-C) | [Unit C6L](../../devices/m5stack/unit-c6l/README.md) |
| LoRaWAN Unit (STM32WLE5), sleep | **28.61 µA @ 5 V** | [LoRaWAN Unit](../../devices/m5stack/unit-lorawan-stm32wle5/README.md) |
| T-Display K230, **idle** | **2.5 W** | [T-Display K230](../../devices/lilygo/t-display-k230/README.md) |

**Read the last row against the others.** 2.5 W at *idle* is roughly three orders
of magnitude above every MCU-class board here. That single figure is the whole
Linux-vs-MCU trade, and it is why the community reaction to the K230 as a
Meshtastic node was *"the battery life on this would be less than it would be with
just a phone and a regular nRF node"* — an opinion, and nobody has published a
measurement either way.

**And note the Stamp-S3 → Stamp-S3A row: a 45× improvement in board sleep current
that came from swapping a µPOL power module for a discrete buck and moving the
WS2812 onto a switched rail** — and which cost the RGB LED its always-on supply,
so PWM-dimming the backlight now browns out the LED. **On a battery device, sleep
current is usually a power-tree property, not a SoC property.**

Two further absences worth stating:

- **No device in this repository has a measured e-paper refresh energy, frontlight
  current or battery runtime, from anyone.** The one panel-level figure is
  Waveshare's *"< 40 mW"* refresh claim, with the panel manual saying **36 mW
  typical at 3.0 V and 120 mA peak**.
- **No independent benchmark of the K230 exists**, even though its own BSP builds
  **CoreMark and CoreMark-PRO into the shipped image**. The tools to produce the
  number ship on the device and nobody has published one.

---

## 3. PSRAM and framebuffer size — the decision that actually gets made

### 3.1 The arithmetic

Framebuffer sizes computed from resolutions sourced in the device records
(`inferred` — it is arithmetic, but the inputs are cited):

| Panel | Depth | One plane | Two planes (old + new) |
|---|---|---|---|
| Xteink X4 / X4 Pro / X4C · Waveshare 3.97 — **800 × 480** | 1 bpp | **46.9 KiB** | 93.8 KiB |
| Xteink X3 — **792 × 528** | 1 bpp | **51.0 KiB** | 102.1 KiB |
| PaperMono — **480 × 800, 4-grey** | 2 bpp | **93.8 KiB** | 187.5 KiB |
| Cardputer — 240 × 135 | RGB565 | 63.3 KiB | — |
| T-Display-S3 — 170 × 320 | RGB565 | 106.3 KiB | — |
| Waveshare P4 reference — 1024 × 600 | RGB565 | **1.2 MB** (stated in the [P4 record](../../components/espressif/esp32-p4/README.md)) | 2.4 MB |
| T-Display K230 — 568 × 1232 AMOLED | RGB565 | **1.33 MiB** | 2.67 MiB |

### 3.2 What that means per SoC

**On a C3 (400 KB SRAM) a 1-bit e-paper framebuffer fits — and is not the
problem.** One 800×480 plane is ~47 KB, two are ~94 KB. That leaves ~300 KB for
everything else, and *everything else* is where a reader firmware actually lives:
an EPUB parser, a CSS engine, UAX #14 line breaking with hyphenation, a glyph
cache, a page cache with position anchors, and a TLS stack for sync.

The evidence that this is the binding constraint, not a theoretical concern:

- **CrossPoint's current development focus, in priority order, is "DRAM/heap
  footprint (the C3 sets the ceiling), flash footprint, code cleanup, then reading
  experience."** The *tightest target sets the ceiling for every device*.
- **OTA out-of-memory was observed on the X3**, and CrossPoint stopped using
  GitHub releases because of it.
- The C3 component record states it plainly: *"The absence of PSRAM is the single
  most consequential fact for anyone writing firmware for the X3 or X4."*

**On an S3R8 (8 MB PSRAM) the constraint moves somewhere else entirely.** Multi-buffer
rendering, damage-window partial refresh and large book indices become possible.
The cost is not memory, it is **pins**: the octal PSRAM consumes **GPIO33–GPIO37
and `SPICS1` inside the package**, which the boards' own schematics mark `NC`.
Driving them raises no error — *"it corrupts PSRAM access, typically surfacing as a
cache-access panic far from the offending code."* That is *"the most important
practical consequence of choosing the R8 variant"*, and it is why the LilyGO
T-Display-S3 boards have so few free pins.

⚠ **Arduino must be told `PSRAM = OPI PSRAM`, or `ps_malloc()` silently fails.**

**On an S3FN8 (no PSRAM) you are back in C3 territory with a faster CPU.** The
Cardputer worked example is instructive: an author memory-mapped a **2.16 MB
Unicode font out of its own flash partition** *"so rendering Cyrillic, CJK or Greek
costs no heap at all"* — because there is nowhere else for it to live.

**On a P4 the question inverts: how much of the 768 KB L2MEM do you give to
cache?** The record is explicit that this is *"a tradeoff you configure, not a
fixed budget"* — more cache raises effective PSRAM bandwidth for framebuffer work,
more directly-addressed SRAM gives deterministic low-latency working memory. A
1024×600 RGB565 single buffer already lives in PSRAM and depends on cache
behaviour; double buffering is 2.4 MB. **This is why the 32 MB variant exists.**

**On a K230, 1 GB of LPDDR4 makes the framebuffer question disappear** and
replaces it with a different one: the two cores are **separate subsystems, not a
coherent cluster**, each with its own L2 and its own PLIC, and Canaan's own SDK
runs **two different operating systems simultaneously** — RT-Smart on CPU1, Linux
on CPU0 — with an explicit IPC API and a `sharefs`. *You do not schedule a Linux
thread onto CPU1.* (The LilyGO board's BSP builds a Linux-only image, which
sidesteps this.)

---

## 4. Radio duty cycle, and the cost of not having one

For an e-ink reader the radio duty cycle is usually near-zero — Wi-Fi comes up to
sync a library or pull an OTA, then goes away for hours. That makes **integration**
matter far more than radio performance.

| SoC | Radio situation | What it costs a battery e-ink design |
|---|---|---|
| **ESP32-C3** | Wi-Fi + BLE 5 on die | Nothing extra. **No Bluetooth Classic** — any project expecting A2DP or SPP is on the wrong SoC |
| **ESP32-S3** | Wi-Fi + BLE 5 + Mesh on die | Nothing extra. **No Bluetooth Classic, at silicon level** — the record spends a full section on this because it is the part's *"single most consequential architectural constraint"*, and treats **LE Audio as unavailable** too (an argument from documented absence, marked *uncertain*) |
| **ESP32-P4** | **None** | A companion SoC over SDIO — ESP32-C6-MINI-1 or ESP32-C5-MINI-1 on every documented P4 board. A second crystal, a second antenna, a second flash, a second firmware image |
| **Kendryte K230** | **None, and no Ethernet MAC either** | **Five external devices doing what an integrated SoC does internally**: RTL8189FS Wi-Fi over SDIO, Bluetooth **via a USB dongle only**, SPI LoRa, UART cellular, UART BLE, USB Ethernet. The record calls this *"the defining architectural fact of the board"* |
| **nRF52840** | BLE | On the K230 board it is a **companion** running LilyGO's AT-command BLE-central firmware, and it also drives the 21700 5 V boost on `P0.04` |
| **nRF9151** | LTE-M / NB-IoT + GNSS | A **10 × 16 mm SiP** and a second toolchain (§5) |

**The Bluetooth-Classic worked example is the one to internalise**, because it
shows what a late-discovered radio requirement actually costs. The
[Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)
needed A2DP, so Waveshare soldered an **original ESP32 (`ESP32-U4WDH`)** next to
the S3 purely to do Bluetooth Classic. The result: a second 40 MHz crystal, a
second antenna, an inter-MCU UART with a private protocol, the audio hardware
**split across both chips** so neither can produce sound alone, and a flashing
procedure where **the USB-C plug's orientation selects which MCU you are talking
to**. As the component record puts it: *"It is far cheaper to check this
constraint at part-selection time."*

**And for what it is worth, the radio is rarely the sleep problem.** An SX1262
sleeps at **600 nA with its configuration retained**
([SX1262 §5](../../components/semtech/sx1262/README.md)); the whole Cap CC1101
board sleeps at 140.87 µA. The two-order-of-magnitude difference is the board, not
the radio.

---

## 5. Toolchain maturity

| SoC | Toolchain | Maturity notes from the records |
|---|---|---|
| **ESP32-C3 / S3** | ESP-IDF, Arduino-ESP32, PlatformIO | The mature end. But two real traps are documented: LilyGO **pins its test matrix at Arduino core 2.0.14** and says higher versions may not work (corroborated — the newest factory binary is built on ESP-IDF v4.4.6, the base of 2.0.14); and the **`USB CDC On Boot` trap**, where a board that runs fine on USB **blocks before `setup()` finishes on battery** because the Arduino core waits for a host to open the port |
| **ESP32-P4** | ESP-IDF, target `esp32p4` | ⚠ **the datasheet is a pre-release document**. Also a board-level constraint that looks like a silicon one: Espressif states the onboard flash on both Function-EV boards *"operates at a maximum clock frequency of 80 MHz and does not support the auto suspend feature"*, with 120 MHz gated behind contacting Espressif |
| **Kendryte K230** | **Canaan K230 SDK only** | ⚠ *"Nothing in the ESP32 ecosystem applies. No Arduino, no PlatformIO for the main SoC, no ESP-IDF"* — LilyGO's own FAQ says so. Build host must be Ubuntu 20.04/22.04/24.04, WSL2 or Docker, with a vendor toolchain at a **hard-coded `/opt/toolchain`** path. **17 months** elapsed between the board going on sale (2025-03-21) and its BSP repository existing (2026-08-13). **A verified owner bricked one and there is no recovery section in any LilyGO document.** On NixOS this needs deliberate work — [`guides/nixos/riscv-and-vendor-sdk-toolchains.md`](../nixos/riscv-and-vendor-sdk-toolchains.md) |
| **nRF52840** | Zephyr / nRF Connect SDK, **or** the Adafruit nRF52 bootloader with **UF2** (family ID `0xADA52840`) — double-tap reset, drag a `.uf2` onto a mass-storage device | The UF2 route is the friendliest flashing story of any part on this page. LilyGO also exposes a **UART DFU** path so the K230 can field-update its companion with no PC |
| **nRF9151** | **NCS v3.4.0** | ⚠ **Every nRF91 application is really two images**: TF-M (secure) plus the non-secure application. That is a permanent build-system fact, not a one-off. ⚠ The **AT Commands Reference is behind a restricted path** and was not retrieved here |

**Two toolchain observations that are really about maintenance, not tooling:**

- **The K230's 17-month documentation gap is the honest measure of its
  maturity**, and it is the single best explanation for the early-owner
  experience: *"I've also been completely unable to figure out how to even get an
  OS installed."* The BSP is now three weeks old and already at v0.2.4 — moving
  fast, from a standing start.
- **On the ESP32 side the risk is not the toolchain, it is version pinning.**
  Vendor firmware pins libraries *and patches them*, while the vendor's own
  published PlatformIO snippets pin nothing. Building from the documentation does
  not reproduce the shipped firmware.

---

## 6. The price consequence

Every figure is item-only, vendor-direct, from the record's own dated observation.
Note that these are **device** prices, not chip prices — this repository holds no
component-level pricing for any of these SoCs.

| SoC | Cheapest documented board carrying it | Price | Date |
|---|---|---|---|
| **ESP32-S3R8** | [LilyGO T-Display-S3](../../devices/lilygo/t-display-s3/README.md) — 16 MB flash **+ 8 MB OPI PSRAM + a 1.9″ colour LCD** | **$9.04** | 2026-09-07 |
| **ESP32-S3R8** (module) | [Waveshare ESP32-S3-ePaper-3.97](../../devices/waveshare/esp32-s3-epaper-3.97/README.md) — the same memory, plus e-paper, AXP2101, RTC, IMU, audio | **$34.99** | 2026-09-01 |
| **ESP32-S3R8** | [M5Stack PaperMono](../../devices/m5stack/papermono/README.md) — e-paper + frontlight + NFC + LoRa | **$65.00** | 2026-09-01 |
| **ESP32-S3FN8** (no PSRAM) | [Cardputer ADV](../../devices/m5stack/cardputer-adv/README.md); the bare Stamp-S3A module is **$7.50** | **$29.90** / $7.50 | 2026-09-04 |
| **ESP32-C3** | [Xteink X3](../../devices/xteink/x3/README.md) — a complete sealed reader with battery, enclosure and 3.7″ 257 PPI panel | **$69.00** | 2026-09-04 |
| **ESP32-P4** | [Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) — 32 MB PSRAM, MIPI DSI, keyboard, LoRa, **full KiCad under CERN-OHL-P** | **€99.17 ex VAT / €119.99 inc** | 2026-08-24 |
| **Kendryte K230** | [LilyGO T-Display K230](../../devices/lilygo/t-display-k230/README.md) bare board | **$98.79** | 2026-09-04 |
| **K230 + keyboard + cellular** | T-Display K230 Kit, **two separate SKUs** | **$263.56** | 2026-09-04 |
| **nRF9151** | **the cleanest price signal available**: $113.25 with it, $70.94 without, same keyboard base | **$42.31 delta** | 2026-09-04 |
| **nRF52840** | no standalone price observed | **no figure in this repository** | — |

### Reading the price table

**The S3-with-PSRAM row is the anomaly, and it is the strongest argument in this
whole guide.** A T-Display-S3 at **$9.04** carries the same memory configuration —
16 MB flash, 8 MB OPI PSRAM — as a $65 PaperMono and a $99 Xteink X4 Pro. **PSRAM
is not what makes those devices expensive.** The enclosure, the battery, the
e-paper glass, the frontlight and the radios are.

**Therefore: on a new design, choosing an `R8` over an `FN8`, or an S3 over a C3,
is close to free at the silicon level, and the C3's memory ceiling is the most
expensive constraint in this repository measured in developer time.** It is the
reason CrossPoint's number-one development priority is heap footprint; it is why
OTA had to move off GitHub releases; it is why an author had to memory-map a font
out of flash. None of that would exist on an S3R8 at the same board price.

**The K230 costs ~11× a T-Display-S3 and ~1.5× a Tanmatsu for the bare board**, and
what it buys is Linux, 1 GB of DRAM, an NPU and H.265. It also buys ~2.5 W of idle
draw and no radio of any kind. That is a legitimate purchase for a specific job and
a bad default.

**The nRF9151's $42.31 delta is the only clean per-chip price signal in this
repository**, because LilyGO sells the identical keyboard base with and without it.
Cellular is expensive.

---

## 7. Recommendation, restated as a decision

For a **battery-powered e-ink handheld** specifically:

1. **Start from ESP32-S3 with PSRAM (`R8`).** It is what the PaperMono, the
   Waveshare 3.97, the Xteink X4 Pro and the X4 Classic all use, the ecosystem's S3
   targets all share one `esp32-s3-devkitc1-n16r8` board definition, and the memory
   headroom is nearly free. Accept that **GPIO33–37 are gone** and plan the pin
   budget around it.
2. **Choose C3 only if the device is genuinely 1-bit, genuinely small, and you
   accept that it will set your firmware's memory ceiling forever.** It works — the
   X3 and X4 are shipping products with a large firmware ecosystem — but every
   downstream project inherits the limit.
3. **Do not choose P4 for an e-ink reader.** No radio, a pre-release datasheet, and
   the features you would be paying for (MIPI-DSI, ISP, H.264, a pixel-processing
   accelerator) are irrelevant to a monochrome panel that updates in hundreds of
   milliseconds. Choose it for a **colour GUI or camera handheld**, as Tanmatsu
   and the Waveshare P4 boards do.
4. **Do not choose K230 for an e-ink reader either.** 2.5 W idle against a
   battery, five bolt-on radio devices, a vendor-only toolchain and no documented
   recovery path. Choose it when *"Linux with an NPU"* is the requirement.
5. **Treat nRF parts as companions, not application processors** — which is the
   only way this repository has ever seen them used. If you need BLE alongside a
   non-radio SoC, the nRF52840's UF2 story is the least painful; if you need
   cellular, budget the money *and* the TF-M dual-image build.
6. **Whatever you pick, measure the sleep current yourself.** This repository
   cannot tell you what it will be (§2), and the Stamp-S3 → Stamp-S3A jump from
   310.89 µA to 6.84 µA shows the answer is dominated by the power tree, not the
   part number.

---

## 8. Evidence boundary

- **Nothing on this page was retrieved, built, measured or benchmarked.**
- **Every deep-sleep figure quoted is a board-level vendor claim under unstated
  conditions**, except the K230's ≤20 µW, which is a vendor figure at the SoC
  level. **No independent power measurement of any device or SoC in this
  repository exists.**
- **Framebuffer sizes in §3.1 are arithmetic** on resolutions cited in the device
  records — `inferred`, not measured, and they exclude driver working buffers.
- **The ESP32-C3 datasheet has never been retrieved into this repository**, so the
  C3 column is the weakest one on this page and is family-level throughout. The
  exact C3 package variant on the Xteink boards has **never been read**.
- The ESP32-P4 datasheet is **pre-release**; the nRF52840 product specification and
  the nRF91 AT command reference were **not downloaded**.
- The P4's CoreMark figure is Espressif's own, under Espressif's own build and
  configuration, and **says nothing about the memory-bound graphics and camera
  workloads most P4 designs actually run**.
- Prices are single-storefront, single-date, single-currency observations. They
  exclude shipping, tax and duty, and for a $9 board international shipping can
  exceed the item price.

## Related

- [E-paper displays](e-paper-displays.md) — waveforms, bias rails, VCOM, update-mode trade-offs
- [Display interfaces](display-interfaces.md) — bandwidth arithmetic and framebuffer sizing
- [Parallel 8080 LCD buses](parallel-8080-lcd-buses.md)
- [Adding LoRa, NFC and an RGB sidelight to e-ink firmware](adding-lora-nfc-and-sidelight-to-eink-firmware.md)
- [Handheld and e-ink device landscape, 2026-09](../markets/handheld-and-eink-device-landscape-2026-09.md) · [Device comparison matrix](../markets/device-comparison-matrix.md)
- [Xteink firmware ecosystem](../../devices/xteink/firmware-ecosystem.md) — what a board must provide to be supported
- [Espressif ecosystem and product lines](../espressif/ecosystem-and-product-lines.md) · [SoC peripheral reference](../espressif/soc-peripheral-reference.md) · [Memory and boot](../espressif/memory-and-boot.md) · [Practical errata](../espressif/errata-practical.md)
- Components: [ESP32-C3](../../components/espressif/esp32-c3/README.md) · [ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md) · [ESP32-S3FN8](../../components/espressif/esp32-s3fn8/README.md) · [ESP32-P4](../../components/espressif/esp32-p4/README.md) · [K230](../../components/canaan/k230/README.md) · [nRF52840](../../components/nordic-semiconductor/nrf52840/README.md) · [nRF9151](../../components/nordic-semiconductor/nrf9151/README.md)
