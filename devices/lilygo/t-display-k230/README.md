# LILYGO T-Display K230 / T-Display K230 Kit

> **Product IDs:** bare board `K256` / `K256-A` / `K256-B` / `K256-C` · kit `K256-03` / `K277` / `K256-04` / `K256-04-A`
> **Status:** in production, actively developed (BSP `v0.2.4`, 2026-09-03) · **Research retrieved 2026-09-04**
> **Evidence basis:** LilyGO's own board-support repository at commit `bb831ab358b66f5bd9a87ecd7c580fee4537492e`, the Shopify product JSON, the LilyGO wiki, the Canaan K230 datasheets, and Reddit threads. **No hardware was in hand; nothing below was executed or measured.**

---

## 1. Identity, SKUs and variants

The board's **confirmed marketed name is "T-Display K230"**, and the keyboard bundle is
**"T-Display K230 Kit"**. It is *not* a T-Deck, not a "T-Deck K230", not a "T-K230" and not a
"Cardputer". Those were plausible names to search for and every one of them is wrong; LilyGO
files this product in its **T-Display** series, alongside T-Display-S3 and T-Display P4.

### The SKU trap

| String | What it actually is |
|---|---|
| **`K230`** | A **LilyGO stock code for the transparent-shell T-Embed CC1101** — an ESP32-S3 board containing no Kendryte silicon at all. It is the top hit when you search the LilyGO store for "K230". |
| `K230-A`, `K230DE`, `K230US`, `K230-ADE`, `K230-AUS` | Same T-Embed CC1101, black shell and regional-warehouse suffixes. |
| **`K256*` / `K277`** | The **actual Kendryte K230 boards.** |

**LilyGO stock codes collide with chip part numbers and carry no information about silicon.**
Never infer hardware from a LilyGO SKU. (Reusable version of this finding:
[`archive/devices/lilygo/t-display-k230/artifacts/research-scratch/vendor-guide-additions.md`](../../../archive/devices/lilygo/t-display-k230/artifacts/research-scratch/vendor-guide-additions.md).)

### Bare board — "T-Display K230", `/products/t-display-k230`

Shopify product id `8182759063733`, created **2025-03-21 13:52 +08:00**, published **2025-03-21 14:22 +08:00**.

| SKU | Variant | Price (2026-09-04) | Available |
|---|---|---:|---|
| `K256` | 868 MHz | $98.79 | yes |
| `K256-A` | 915 MHz | $98.79 | yes |
| `K256-B` | 923 MHz | $98.79 | yes |
| `K256-C` | 433 MHz | $98.79 | yes |

All four differ **only** in the LoRa band. Same PCB, same silicon otherwise.

### Kit — "T-Display K230 Kit", `/products/t-display-k230-kit`

Shopify product id `10544222011573`, created **2026-08-06 09:31 +08:00**, published **2026-08-20 15:10 +08:00**.

| SKU | Variant | Price (2026-09-04) | What you get |
|---|---|---:|---|
| `K256-03` | Main Unit / **SX1262** / 868 MHz | **$150.31** | K230 main unit in the kit configuration |
| `K277` | Main Unit / **LR2021** / 830–940 MHz | **$153.01** | Same, with the newer multi-protocol radio |
| `K256-04` | **Keyboard Only** / **with nRF9151** | **$113.25** | Keyboard base including the cellular/GNSS SiP |
| `K256-04-A` | **Keyboard Only** / **without nRF9151** | **$70.94** | Keyboard base, no cellular |

**Read that table carefully — it is the single most misread thing about this product.** "Main
Unit" and "Keyboard Only" are *separate purchases*. There is no single SKU that is "the whole
handheld". A buyer wanting the complete keyboard handheld with cellular pays
**$150.31 + $113.25 = $263.56** before shipping. A Reddit user on the launch thread asked
exactly this — "I'm confused on what is what… I want the kit with the keyboard. What do I buy?"
— and received no answer (R-KIT).

The **$42.31 delta** between `K256-04` and `K256-04-A` is the cleanest available price for the
nRF9151 cellular option.

### Third variant: "Cased Version"

LilyGO's wiki documents a **T-Display K230 Cased Version** at
`/products/t-display-series/t-display-k230/cased-version.html`: a 110 × 58 × 30 mm enclosed unit
with speaker, microphone, 3.5 mm jack, QWIIC and an nRF52840 GPIO expansion header. It has **no
shop listing** as of 2026-09-04. A buyer confirmed on 2026-08-13 that "the encased K230 model
that goes with keyboard is a newer one that isn't listed on the website yet" (R-CASE), and an
earlier buyer received "just the screen and motherboard on risers in the package" — no case, no
battery (R-BARE).

### Related but distinct

| Product | Relationship |
|---|---|
| **T-Display P4** | Espressif ESP32-P4 sibling in the same T-Display line, with **its own, incompatible keyboard** (`/products/t-display-p4-keyboard`). LilyGO confirmed on 2026-07-28: "the keyboard for the T-Display K230 does **not** fit the T-Display P4". |
| **T-Deck / T-Deck Plus / T-Deck Pro / T-Deck MAX** | LilyGO's *other* keyboard handheld family, all ESP32-S3. Different series, different keyboard, different everything. A sibling session documents **T-Display-S3 and variants** in this repository (expected at `devices/lilygo/t-display-s3*`; not yet present at the time of writing, so no link is given). |
| **CanMV-K230**, **BPI-CanMV-K230D-Zero** | Other K230 boards; see [the K230 component record](../../../components/canaan/k230/README.md#13-notable-k230-boards). |

---

## 2. What it is, and visual identification

A **4.1-inch AMOLED handheld running Linux on a 64-bit RISC-V SoC**, with LoRa, a 2 MP camera,
an RJ45 Ethernet port, a 40-pin expansion header, and — via the Kit — a physical QWERTY keyboard
base carrying an LTE-M/NB-IoT/GNSS modem, a charger, a fuel gauge and a keyboard scanner.

Identify it by, in descending order of reliability:

1. **The tall narrow AMOLED.** 568 × 1232 in a 104 × 51 mm board is an unusually tall aspect
   ratio; it looks like a phone screen, because it is one.
2. **An RJ45 socket on a handheld.** Almost nothing else in this class has one, and community
   reaction on first sight was "the ethernet port is an odd choice. It just seems too big for
   this type of device" (R-ETH).
3. **A 2 × 20 pin header** along the long edge.
4. **No ESP32 markings** and a large BGA under the shield/heat area.

Images with full provenance: [`media.md`](media.md) and [`media/manifest.json`](media/manifest.json).

---

## 3. Product history, family and culture

Full timeline with sources: [`product-history-and-family.md`](product-history-and-family.md).
Condensed:

| Date | Event | Evidence |
|---|---|---|
| 2023-07-06 | Canaan K230 datasheet V1.0 | C1 |
| 2023-10-24 | CanMV-K230 reference board covered by CNX-Software | N1 |
| **2025-03-21** | **T-Display K230 created and published on lilygo.cc**; announced on r/LilyGO the same day; **sold out within days** | D1, R-LAUNCH |
| 2025-03-26 | oreboot maintainer publicly notes oreboot supports K230 and boots Linux from mask ROM over USB in ~3 s | R-OREBOOT |
| 2025-07-07 | r/meshtastic post reaches **187 points / 40 comments** — the board's largest single moment of attention | R-MESH |
| 2026-07-28 | Keyboard announced on r/LilyGO | R-KB |
| **2026-08-06 / 2026-08-20** | **T-Display K230 Kit created / published**; announced on r/LilyGO (83 points) | D2, R-KIT |
| 2026-08-13 | BSP repository `Xinyuan-LilyGO/T-Display-K230` created | G1 |
| 2026-08-16 | nRF52840 AT firmware build `r4` | G3 |
| 2026-08-23 · 2026-08-14 | nRF52840 and nRF9151 firmware repositories last pushed | G3, G4 |
| **2026-09-03** | BSP **v0.2.4** — PicoClaw chat app, Meshtastic map-tile download, storage expansion, async I²C scan | G1 |

**Culture.** This is a LilyGO product in the strong sense: shipped early, documented late,
supported publicly on Reddit by `u/LilyGoXinyuan`, and improved rapidly afterwards. The BSP
repository is **three weeks old at the time of writing and already at v0.2.4**. The gap between
"board on sale" (2025-03-21) and "board-support repository exists" (2026-08-13) is **almost
seventeen months**, which is the single best explanation for the early-owner experience
described in [§8](#8-shortcomings-and-constraints).

---

## 4. Key specifications

Every functional part links to its component record.

| Function | Part | Interface / detail | Component record |
|---|---|---|---|
| **SoC** | **Canaan Kendryte K230** | 2 × XuanTie C908 RISC-V 64-bit: **CPU1 @ 1.6 GHz with RVV 1.0**, CPU0 @ 800 MHz; KPU/NPU, DPU, 2.5D GPU, H.264+H.265 VPU, ISP | [canaan/k230](../../../components/canaan/k230/README.md) |
| **DRAM** | LPDDR4, **8 Gb = 1 GB**, 32-bit | external (K230 13 × 13 mm package, not the K230D SiP) | [canaan/k230](../../../components/canaan/k230/README.md#6-audio-memory-and-peripherals) |
| **Display** | **RM69A10** 4.1″ AMOLED | MIPI DSI, **RGB 568 × 1232**, `GPIO22` reset, `GPIO25` enable, DSI-command backlight | [raydium/rm69a10](../../../components/raydium/rm69a10/README.md) |
| **Touch** | **Goodix GT9895** ("Berlin") | I²C3 `GPIO37`/`GPIO36`, addr **`0x5D`**, IRQ `GPIO23`, RST `GPIO24` | [goodix/gt9895](../../../components/goodix/gt9895/README.md) |
| **Camera** | **GalaxyCore GC2093** 2 MP | MIPI CSI + I²C0 `GPIO49`/`GPIO48`, addr **`0x37`** | [galaxycore/gc2093](../../../components/galaxycore/gc2093/README.md) |
| **Wi-Fi** | **Realtek RTL8189FS** | SDIO, 802.11 b/g/n 2.4 GHz, `wlan0` | [realtek/rtl8189fs](../../../components/realtek/rtl8189fs/README.md) |
| **Bluetooth** | **USB dongle** (CSR8510/8891 workaround) | *no on-board BT radio* | see [features/wifi-and-bluetooth.md](features/wifi-and-bluetooth.md) |
| **Ethernet** | **RTL8152B** claimed, 100 Mbps, `eth0` | USB-attached; **K230 has no Ethernet MAC** | [realtek/rtl8152b](../../../components/realtek/rtl8152b/README.md) |
| **LoRa** | **Semtech SX1262** *or* **LR2021** | SPI `GPIO15/16/17`, CS `GPIO14`, RST `GPIO5`, BUSY `GPIO19`, IRQ `GPIO20`, PWR `GPIO44`; **spidev + RadioLib** | [semtech/sx1262](../../../components/semtech/sx1262/README.md) · [semtech/lr2021](../../../components/semtech/lr2021/README.md) |
| **HDMI bridge** | **LT9611** — *presence unconfirmed* | shares touch I²C/IRQ/reset; boot-time alternative to AMOLED | [lontium/lt9611](../../../components/lontium/lt9611/README.md) |
| **Storage** | microSD | MMC1 `GPIO54–59`; **also the boot medium** | [generic/micro-sd-sdmmc](../../../components/generic/micro-sd-sdmmc/README.md) |
| **Keyboard scanner** | **TI TCA8418** | I²C4, addr **`0x34`**, RST `GPIO43`, IRQ `GPIO42`; **7 ROW × 10 COL** | [texas-instruments/tca8418](../../../components/texas-instruments/tca8418/README.md) |
| **GPIO expander** | **XL9555** | I²C4, addr **probed** in `0x20–0x27` | [xlsemi/xl9555](../../../components/xlsemi/xl9555/README.md) |
| **Charger** | **TI BQ25896** | I²C4, addr **`0x6B`** | [texas-instruments/bq25896](../../../components/texas-instruments/bq25896/README.md) |
| **Fuel gauge** | **TI BQ27220** | I²C4, addr **`0x55`** | [texas-instruments/bq27220](../../../components/texas-instruments/bq27220/README.md) |
| **Cellular + GNSS** | **Nordic nRF9151** | UART3 `GPIO28/29` @115200, enable `GPIO2`; NCS v3.4.0 Serial LTE Modem | [nordic-semiconductor/nrf9151](../../../components/nordic-semiconductor/nrf9151/README.md) |
| **BLE central** | **Nordic nRF52840** | UART1 `GPIO3/4` @115200; also drives the 21700 5 V boost on `P0.04` | [nordic-semiconductor/nrf52840](../../../components/nordic-semiconductor/nrf52840/README.md) |
| **Audio amp** | **MAX98357A** | I²S `GPIO32/33/35`, SD `GPIO34` | [analog-devices/max98357a](../../../components/analog-devices/max98357a/README.md) |
| **Temp/humidity** | **AHT20** | I²C4, addr **`0x38`** | [asair/aht20](../../../components/asair/aht20/README.md) |
| **PMIC, speaker amp, microphone, 21700 pack** | **unidentified** | — | [unidentified/t-display-k230](../../../components/unidentified/t-display-k230/README.md) |
| Dimensions | 104 × 51 × 15.5 mm (board) · ~110 × 58 × 30 mm (cased) | | |
| USB charging | 5 V, 500 mA | | |

**What the table means in practice.** Only the first eleven rows are on the main board. Rows
from TCA8418 down are on **base boards you buy separately** — and the launcher treats every one
of them as optional, detected at runtime. A bare `K256` is a screen, a camera, a radio and a
40-pin header; it is not a handheld until you add a base.

---

## 5. Architecture

```
                    ┌──────────────────────── K230 main board (K256*) ────────────────────────┐
   4.1" AMOLED ─DSI─┤ RM69A10                                                                 │
   GT9895 touch ─I²C3(G37/G36)+IRQ G23+RST G24─┐                                              │
   LT9611 HDMI  ─── same four lines ───────────┘   ┌─────────────────────┐                    │
   GC2093 cam  ─CSI + I²C0(G49/G48 @0x37)──────────┤   Kendryte K230     │                    │
   microSD     ─MMC1 (G54..G59) ── BOOT MEDIUM ────┤ CPU1 1.6GHz  RVV1.0 │── 1 GB LPDDR4      │
   RTL8189FS   ─SDIO ────────────────────────── ───┤ CPU0 0.8GHz  Linux  │                    │
   SX1262/LR2021─SPI(G15/16/17) CS G14 RST G5      │ KPU DPU GPU VPU ISP │                    │
                 BUSY G19 IRQ G20 PWREN G44 ───────┤                     │                    │
   RTL8152B ─USB─ RJ45                             │  PMU  ── INT0 = power key (G64)          │
   USB-BT dongle ─USB─                             └──────────┬──────────┘                    │
   BOOT0 button ── G0                                         │ 2x20 header                   │
   └───────────────────────────────────────────────────────── │ ──────────────────────────────┘
                                                              │
        ┌─────────────────────────────────────────────────────┴───────────────────────────┐
        │                                                                                 │
 ┌──────┴────── nRF52840 base ──────┐              ┌───────────── nRF9151 keyboard base ──┴────────┐
 │ nRF52840 ─UART1 G3/G4 @115200    │              │ nRF9151 ─UART3 G28/G29 @115200, EN G2        │
 │   P0.04 → 21700 5 V boost enable │              │ TCA8418  0x34  RST G43  IRQ G42   7x10 matrix│
 │ AHT20   0x38 ─┐                  │              │ XL9555   0x20-0x27 (probed) ─┐               │
 │ MAX98357A ─I²S G32/33/35, SD G34 │              │ BQ25896  0x6B ───────────────┼─ I²C4 G46/G47 │
 └───────────────┴─ I²C4 G46/G47 ───┘              │ BQ27220  0x55 ───────────────┘               │
                                                   │ keyboard backlight ← G52 / PWM4              │
                                                   └──────────────────────────────────────────────┘
```

Three structural points:

1. **One MIPI DSI output, two possible sinks.** The AMOLED and the LT9611 HDMI bridge cannot run
   at once; the BSP builds a *separate device tree* (`k230-canmv-rm69a10-hdmi`) for the HDMI
   case. HDMI is a boot-time alternative and LilyGO calls it "a diagnostic feature".
2. **Everything the K230 lacks is bolted on over a serial bus.** No radio on the die → SDIO
   Wi-Fi + USB Bluetooth + SPI LoRa + UART cellular + UART BLE. No Ethernet MAC → USB Ethernet.
   That is five external devices doing what an integrated SoC would do internally, and it is the
   defining architectural fact of the board.
3. **The two base boards share one I²C bus (I²C4, `GPIO46`/`GPIO47`) and are mutually
   exclusive in practice** — they are different physical bases. Nothing prevents address
   collisions in principle, but as fitted, `0x38` (AHT20), `0x34`, `0x55`, `0x6B` and `0x20–0x27`
   do not overlap.

---

## 6. Common uses and representative projects

| Use | Status | Notes |
|---|---|---|
| **Phone-style LVGL launcher** with camera, gallery, music, network radio, recorder, video player, terminal, MTP, settings | **Stable** per LilyGO | The shipped default experience |
| **Meshtastic handheld** | **Beta** | Chat, node display, map view, channel sharing. **Voice/photo transfer requires LR2021**; SX1262 units get text only |
| **LoRaWAN tooling** | Beta | `lorawan_test.cpp`, RF test profiles |
| **On-device AI** — face detection, QR scan, AI camera | Working | KPU-accelerated; `camera_face_detect.cpp`, `ui_ai_demo.c` |
| **Xiaozhi voice assistant** | Beta | Needs network + a compatible Xiaozhi service; wake-word only while the app owns the mic |
| **PicoClaw** LLM chat client | Beta (v0.2.4) | Needs an OpenAI-compatible API key |
| **NES emulator** | Present | `ui_nes.cpp`; **ROMs not bundled** |
| **Offline maps** | Present | Tile downloader added v0.2.4; **tiles not bundled** |
| **Cellular data / GNSS** | Beta | Requires the `K256-04` keyboard base |
| **nRF52840 UART DFU from the K230** | Beta | Field-update the companion MCU with no PC |

Community-originated work is catalogued in
[`projects-and-community.md`](projects-and-community.md). The most substantive third-party items
are **oreboot** (K230 support, mask-ROM USB boot), **k230-debian**, and an in-progress
independent Meshtastic UI announced 2026-06-02.

---

## 7. Distinctive strengths

- **It is a RISC-V Linux handheld you can buy for $98.79.** Not an MCU running a GUI library —
  a Linux userspace with 1 GB of RAM, a package set, SSH, and a terminal app.
- **1 GB LPDDR4 is 2× the CanMV-K230 reference board and 8× a K230D board.** Among K230 hardware
  this is the memory-rich option, and memory is the binding constraint on that SoC.
- **A genuine NPU plus H.265 encode *and* decode**, which nothing in the ESP32 class has.
- **Radio choice at purchase**, including a current-generation LR2021.
- **The BSP is unusually good for LilyGO**: a documented pin map, 30+ named kernel patches, a
  pinned upstream SDK commit, pinned kernel commit, pinned toolchain version, an `overlay_manifest.txt`,
  and separate repositories for each companion MCU with their own patch sets and prebuilt firmware.
- **Companion-MCU firmware is open and buildable**, including the nRF9151 Serial LTE Modem fork
  with its five patches and the pinned upstream commit they apply to.

## 8. Shortcomings and constraints

- **Bricking is real and recovery is not documented by LilyGO.** A verified owner: "I managed to
  get an mp3 player and notepad working… but once I attempted to turn on the 'fun' features it
  bricked it… my board is still unresponsive to boot pin and term. I think I flashed it into mmc
  mode vs sd card and it's stuck" (R-BRICK, 2026-08-21 / 2026-08-28). There is **no recovery
  section in any LilyGO document**. See [`factory-firmware.md`](factory-firmware.md).
- **The 17-month documentation gap.** Sold from 2025-03-21; BSP repository created 2026-08-13.
  Early buyers were on their own — "I've also been completely unable to figure out how to even
  get an OS installed" (R-BARE).
- **No Bluetooth without a USB dongle**, and the dongle support is two patches whose own
  filenames say *workaround* and *experimental*.
- **The kit is two purchases**, and the store does not say so clearly.
- **Ethernet is 100 Mbit over USB**, not a MAC.
- **Nothing in the ESP32 ecosystem applies.** No Arduino, no PlatformIO for the main SoC, no
  ESP-IDF. LilyGO's own FAQ says so: "No. T-Display K230 is based on the Kendryte K230 RISC-V SoC
  and requires the K230 SDK toolchain."
- **Build host requirements are heavy**: Ubuntu 20.04/22.04/24.04 or WSL2 or Docker, plus a
  vendor toolchain at a hard-coded `/opt/toolchain` path. On NixOS this needs deliberate work —
  [`guides/nixos/riscv-and-vendor-sdk-toolchains.md`](../../../guides/nixos/riscv-and-vendor-sdk-toolchains.md).
- **No schematic is published.** The wiki has a `#schematic` heading with nothing under it.
- **No IP rating.** "Wish there were more IPX water resistant options across all your product
  lines. I prototype field devices" (R-IPX).
- **Battery life is unmeasured** and community scepticism is explicit: "the battery life on this
  would be less than it would be with just a phone and a regular nRF node" (R-BATT) — an opinion,
  not a measurement, and nobody has published a measurement.

## 9. Performance summary

**No independent benchmark of this board exists.** Everything available is either a Canaan
silicon-level claim or a vendor statement. The BSP does build **CoreMark and CoreMark-PRO** into
the image (`BR2_PACKAGE_COREMARK=y`, `BR2_PACKAGE_COREMARK_PRO=y`), so the board ships with the
tools to produce a number that nobody has published. Full treatment, including exactly what to
run: [`performance.md`](performance.md).

## 10. Pricing and availability

Dated observations, currency conversion notes and stock evidence: [`market-and-pricing.md`](market-and-pricing.md).
Headline, **2026-09-04, lilygo.cc, USD**: bare board **$98.79**; kit main unit **$150.31**
(SX1262) or **$153.01** (LR2021); keyboard base **$113.25** (with nRF9151) or **$70.94**
(without). Complete keyboard handheld with cellular: **$263.56** before shipping.

## 11. Competitors, equivalents and clones

Full comparison: [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md).
Nearest things: LilyGO **T-Deck Plus** (ESP32-S3, cheaper, mature, no Linux),
**T-Display P4** (ESP32-P4, MCU-class, its own keyboard), **M5Stack Cardputer**
(much cheaper, much less capable), **CanMV-K230** (same SoC, no display, half the RAM),
**BPI-CanMV-K230D-Zero** ($29, K230D, 128 MB). **No clone of this board was found.**

## 12. Launch-era versus current market fit

**At launch (2025-03-21):** near-unique. A sub-$100 RISC-V Linux handheld with AMOLED and LoRa
had no direct equivalent, which is why the r/meshtastic thread drew 187 points. But there was no
board-support repository, no wiki entry with substance, and no keyboard — it was a development
board with a beautiful screen and no software story.

**Now (2026-09-04):** the software story exists and is moving weekly, and the keyboard makes it a
handheld. But the competitive picture changed: the **T-Display P4** exists in the same line with
a mature toolchain, and the K230's own advantage — Linux — is still gated behind a build process
that assumes Ubuntu and a vendor toolchain. It is a much better product than it was and a
slightly harder sell.

## 13. When to use / when not to use

**Use it when** you need on-device Linux with a real NPU and a MIPI camera in a handheld form
factor; when you specifically want RISC-V; when you want LoRa mesh with **voice/photo** transfer
(LR2021 only); or when you need a Linux userspace — Python, SSH, standard tooling — on a
battery-powered device with a screen.

**Do not use it when** you want an Arduino/ESP-IDF workflow; when you need Bluetooth without a
dongle; when you need a documented recovery path for a fleet; when you need gigabit Ethernet or
5 GHz Wi-Fi; when you need certified radios for a product; or when the project is a Meshtastic
node and nothing more — a $30 dedicated node does that better and lasts far longer on a charge.

**Alternatives by tier:** [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md).

---

## 14. Common tasks / How do I…?

| I want to… | Guide |
|---|---|
| Drive the 4.1″ AMOLED, set brightness, understand the boot-logo handoff | [features/display.md](features/display.md) |
| Read touch input | [features/touch.md](features/touch.md) |
| Use the QWERTY keyboard, read the key matrix, change F-key actions, set backlight | [features/keyboard.md](features/keyboard.md) |
| Capture from the camera, run face detect / QR / RTSP | [features/camera.md](features/camera.md) |
| Get on Wi-Fi; get Bluetooth working at all | [features/wifi-and-bluetooth.md](features/wifi-and-bluetooth.md) |
| Use the RJ45 Ethernet port | [features/ethernet.md](features/ethernet.md) |
| Send and receive LoRa; choose between SX1262 and LR2021; run Meshtastic | [features/lora.md](features/lora.md) |
| Play or record audio, use the I²S amplifier, use the microphone | [features/audio.md](features/audio.md) |
| Mount, resize or replace the microSD card | [features/microsd.md](features/microsd.md) |
| Use USB — host, gadget, MTP, mass storage | [features/usb.md](features/usb.md) |
| Read battery state, configure charging and low-battery shutdown | [features/battery-and-power.md](features/battery-and-power.md) |
| Use the 40-pin header, ADCs, I²C, PWM, spare GPIO | [features/gpio-and-expansion.md](features/gpio-and-expansion.md) |
| Run a neural network on the KPU/NPU | [features/kpu-npu.md](features/kpu-npu.md) |
| Understand and use the two CPU cores and RVV | [features/dual-core-riscv.md](features/dual-core-riscv.md) |
| Talk to the nRF52840 (BLE) or nRF9151 (cellular/GNSS) | [features/nrf52840-ble.md](features/nrf52840-ble.md) · [features/nrf9151-cellular-gnss.md](features/nrf9151-cellular-gnss.md) |
| Build the whole image from source | [development.md](development.md) |
| Flash an SD card, or recover a board that will not boot | [factory-firmware.md](factory-firmware.md) |

## 15. Documentation map

| File | Contents |
|---|---|
| [pinouts-and-buses.md](pinouts-and-buses.md) | Every pin, bus, address and its source |
| [resources-and-conflicts.md](resources-and-conflicts.md) | Shared lines, arbitration, what cannot coexist |
| [development.md](development.md) | Toolchain, build, deploy, all four toolchains |
| [factory-firmware.md](factory-firmware.md) | Images, flashing, **recovery and bricking** |
| [compatibility-and-status.md](compatibility-and-status.md) | Working / partial / failing / untested |
| [coverage.md](coverage.md) | Feature → evidence → guide map |
| [gaps-and-conflicts.md](gaps-and-conflicts.md) | `GC-1`…`GC-9`, unresolved |
| [performance.md](performance.md) | What is claimed, what is measured (little) |
| [market-and-pricing.md](market-and-pricing.md) | Dated price observations |
| [product-history-and-family.md](product-history-and-family.md) | Timeline, family, lineage |
| [projects-and-community.md](projects-and-community.md) | Every firmware/project, with licence and status |
| [community.md](community.md) | Threads, posts, anecdotes, evidence labels |
| [comparisons-and-recommendations.md](comparisons-and-recommendations.md) | Competitors and tiers |
| [sources.md](sources.md) | Full source table |
| [research-log.md](research-log.md) | Every query, every dead end |
| [commands.md](commands.md) | Command ledger with execution status |
| [media.md](media.md) · [media/manifest.json](media/manifest.json) | Images and provenance |
| [examples/](examples/) | Catalogue, search log, selection |
| [acquisition/](acquisition/) | Manifest and clean-clone instructions |

## 16. Artifact layout

```
devices/lilygo/t-display-k230/
├── artifacts/
│   ├── datasheets/          (empty — chip documents live under components/, by design)
│   ├── source-snapshots/    BSP pin map, defconfig, patch list, keyboard matrix extract
│   ├── firmware/            nRF52840 firmware/bootloader provenance (files upstream)
│   ├── schematic/           EMPTY — LilyGO publishes no schematic (see gaps GC-5)
│   └── originals/
├── media/                   product and wiki images + manifest.json
└── examples/
```

**Chip documents are filed under the component, not here.** The K230 datasheet lives at
[`components/canaan/k230/artifacts/`](../../../components/canaan/k230/artifacts/), reached from
here through the [key-specification table](#4-key-specifications).

## 17. Known conflicts and unresolved identities

Nine open items, tracked in [`gaps-and-conflicts.md`](gaps-and-conflicts.md). The three that
matter most:

- **`GC-2`** — LilyGO's wiki claims an **ESP32-S3-R8 co-processor** for Wi-Fi/BT. The BSP
  contains **zero** Espressif references; Wi-Fi is RTL8189FS over SDIO and BT is a USB dongle.
- **`GC-3`** — Ethernet is variously **RTL8152B** (wiki) and **"RC01812"** (shop). The K230 has
  no Ethernet MAC, and the BSP kernel fragment does not enable `USB_RTL8152`.
- **`GC-1`** — LilyGO's wiki inverts the K230's core roles relative to Canaan's datasheet.

---

*Compiled 2026-09-04. Reproducible broad-coverage snapshot, not a claim of completeness — see
[`research-log.md`](research-log.md) for searched sources, depth and exclusions.*
