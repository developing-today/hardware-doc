# Waveshare ESP32-P4-WIFI6-Touch-LCD-3.4C

> 3.4-inch 800 × 800 round capacitive-touch ESP32-P4 development board with Wi-Fi 6 via a
> companion ESP32-C6. Current, purchasable product. Research retrieved **2026-08-24**.

- **Manufacturer:** Waveshare
- **SoC:** [ESP32-P4NRW32](../../../components/espressif/esp32-p4/README.md) — dual-core RISC-V HP @ 360 MHz + single-core LP @ 40 MHz, 32 MB in-package PSRAM
- **Radio:** ESP32-C6-MINI-1-N4 over SDIO (the P4 has **no** built-in radio)
- **Status:** current; listed at **US $64.99 – $74.99** (waveshare.com, 2026-08-24)
- **Sibling:** [ESP32-P4-WIFI6-Touch-LCD-4C](../esp32-p4-wifi6-touch-lcd-4c/README.md) — same PCB, 4 in / 720 × 720, **not currently purchasable**

## Identity and variants

| Field | Value |
|---|---|
| Marketed name | ESP32-P4-WIFI6-Touch-LCD-3.4C |
| **SKU** | **31523** (the 4C is **31522**, same listing) |
| Wiki (legacy MediaWiki) | <https://www.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-3.4C> |
| **Docs platform (current)** | <https://docs.waveshare.com/ESP32-P4-WIFI6-Touch-LCD-XC> |
| Store | <https://www.waveshare.com/esp32-p4-wifi6-touch-lcd-3.4c.htm> (`HTTP 200`, 2026-08-24) |
| Platform family | `ESP32-P4-WIFI6-Touch-LCD-XC` — Waveshare's own wildcard covering 3.4C and 4C |
| Price range | $64.99 – $74.99 — the span across the **two display variants** sold under this listing |
| PCB revision | **rev1.1** — stated only in Waveshare's repo `docs/HARDWARE.md`, not on the wiki or store page |

The listing sells **both variants** through a *Version Options* selector — 3.4C is SKU **31523**,
4C is SKU **31522**, and both are marked saleable. The `$64.99 – $74.99` span is therefore the
difference between the two panels, not an accessory bundle. **Which price maps to which SKU was not
extractable** (rendered client-side); check at purchase. See
[C6](./gaps-and-conflicts.md#c6--purchase-options-for-the-34c--resolved-2026-08-24).

## What it is

A round-display HMI board. The headline capability is that the ESP32-P4 drives a genuine
**MIPI-DSI** panel — not a parallel RGB or SPI display — with hardware JPEG decode, a 2D DMA
engine and a pixel-processing accelerator behind it. Paired with a MIPI-CSI camera input on the
same board, it is aimed at smart-home control panels, video doorbell/intercom style products, and
machine-vision experiments.

The 40-pin header is described by Waveshare as "compatible with some Raspberry Pi HAT expansion
boards". Read *some* literally: the header is electrically a GPIO breakout, not a Pi-compatible
power/ID-EEPROM implementation, and HAT compatibility is per-HAT rather than general.

## Key specifications

| Item | Value | Component record |
|---|---|---|
| SoC | ESP32-P4NRW32, RISC-V dual-core 360 MHz + LP core 40 MHz | [espressif/esp32-p4](../../../components/espressif/esp32-p4/README.md) |
| RAM | 32 MB PSRAM in package; 768 KB L2MEM; 32 KB LP SRAM; 8 KB TCM | — |
| Flash | 32 MB NOR over QSPI — **GD25Q256** | — |
| Display | **3.4 in round IPS, 800 × 800**, JD9365, MIPI-DSI 2-lane @ 1500 Mbps, **170° viewing angle**, **optically bonded tempered glass** | [components/jadard/jd9365](../../../components/jadard/jd9365/README.md) |
| Touch | **GT9271** capacitive, I²C (GT911-compatible driver) | [goodix/gt9271](../../../components/goodix/gt9271/README.md) |
| Radio | ESP32-C6-MINI-1-N4 — Wi-Fi 6, BT 5 LE, 802.15.4 — over SDIO | *(record pending)* |
| Audio out | ES8311 codec + power amplifier, PH2.0 speaker header (8 Ω 2 W) | *(record pending)* |
| Audio in | **Dual** on-board MEMS microphones + ES7210 echo-cancellation ADC | *(record pending)* |
| Camera | MIPI-CSI 2-lane, 15-pin 1.0 mm FPC; 1080p30 H.264/JPEG encode | — |
| Storage | microSD, SDIO 3.0 | [generic/micro-sd-sdmmc](../../../components/generic/micro-sd-sdmmc/README.md) |
| USB | USB 2.0 HS OTG Type-A; USB 2.0 FS Type-C (power/flash/debug) | — |
| Serial | CH343P USB-UART, Type-C | [wch/ch340x](../../../components/wch/ch340x/README.md) |
| Power | MP1658, MP1605 regulators | *(record pending)* |
| RTC | Backup cell on `ESP_VBAT` — **rechargeable cells ONLY**, see safety note | — |
| Expansion | 40-pin (2 × 20) header exposing **28 GPIOs**; SH1.0 headers for C6 UART and I²C | — |

The RTC holder constraint is a real hazard: fitting a non-rechargeable CR2032 to a holder wired
for a rechargeable cell means the board will attempt to charge a primary cell. Waveshare state
this explicitly on the wiki.

## Architecture: the two-chip radio split

The ESP32-P4 is Espressif's first application-class RISC-V part with **no integrated Wi-Fi or
Bluetooth**. All networking on this board is provided by the ESP32-C6-MINI-1 over SDIO, using
Espressif's `esp_hosted` / `esp_wifi_remote` split stack. Practical consequences:

- Wi-Fi/BT code runs against `esp_wifi_remote`, and the C6 needs its **own** firmware, flashed
  through a **separate** SH1.0 4-pin header.
- Two MCUs means two flashing paths and two failure modes. A board that will not join Wi-Fi may
  have perfectly good P4 firmware and stale C6 firmware.
- Throughput and latency are bounded by the SDIO link, not by the radio alone.

See [`features/wifi-and-bluetooth.md`](./features/wifi-and-bluetooth.md).

## Pin map

Full table, with per-row provenance and the inherited-example warning, is in the shared platform
record: [**pin map**](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md#verified-pin-map).

Complete verified map: [**`pinouts-and-buses.md`**](./pinouts-and-buses.md), established by
reading the schematic visually and cross-checking Waveshare's demo source.

| Signal | GPIO | Evidence |
|---|---:|---|
| I²C SDA / SCL (touch + both audio chips) | **7** / **8** | Schematic + code |
| Panel reset | **27** | Schematic + code |
| Backlight PWM / **enable** | **26** / **33** | Schematic |
| Touch reset | **23** | Schematic |
| Touch interrupt | **not wired — poll** | Schematic |
| microSD CLK / CMD / D0–D3 | **43** / **44** / **39–42** | Schematic |
| microSD **power switch** | **45** | Schematic |
| I²S MCLK / BCLK / WS / DOUT / DIN | **13** / **12** / **10** / **9** / **11** | Code only |
| Speaker amplifier enable | **53** | Code only |

The **40-pin header `J8`** is 28/40 mapped, and is **not** Raspberry Pi compatible — pin 4 is a
GPIO where a Pi has 5 V. Twelve power/GND pins remain unidentified; check with a meter before
connecting anything. The **camera's SCCB shares the same I²C bus** as touch and audio, so four
device families are on GPIO7/8.

Three signals are wired but **untouched by every shipped demo** — `BL_EN` (33), the microSD power
switch (45), and touch reset (23). A from-scratch project that ignores 33 or 45 can get a dark
panel or a dead card slot with no obvious cause.

## Display: what makes this variant specific

| Parameter | Value |
|---|---|
| Controller | JD9365 |
| Active area | 800 × 800 |
| Colour depth | 24 bpp in the reference demo |
| DSI lanes / rate | 2 @ 1500 Mbps |
| hsync pw / bp / fp | 20 / 20 / 40 |
| vsync pw / bp / fp | 4 / 12 / 24 |
| JD9365 init reg `0x40` | **`0x00`** ← the one byte that differs from the 4C |

Against the 4C, **only** the resolution constants and register `0x40` differ. The porch timings
and lane rate are identical across both panels, meaning they were not derived per panel. Re-derive
them if you change pixel clock or colour depth. Detail:
[shared record](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md#what-is-genuinely-shared-vs-per-variant).

Reference code: `artifacts/demo/ESP-IDF/06_displaypanel_3.4inch/` in the shared record — use
**06**, not 07.

## Start here for development

Waveshare maintain an **official, Apache-2.0, CI-tested repository** and a **published BSP
component** for these boards. Neither is mentioned in the demo ZIP, and both are better starting
points than it:

```bash
git clone https://github.com/waveshareteam/ESP32-P4-WIFI6-Touch-LCD-XC.git
```

```yaml
dependencies:
  waveshare/esp32_p4_wifi6_touch_lcd_xc: "3.0.1"    # then select BSP_LCD_TYPE_800_800_3_4_INCH
```

Target **ESP-IDF v5.5.5 or v6.0.2** — the two versions Waveshare's CI actually validates. Factory
firmware images are published for both variants. Full detail:
[`official-repo-and-community.md`](./official-repo-and-community.md).

## Common tasks / How do I...?

| Task | Guide |
|---|---|
| Drive the round display | [`features/display.md`](./features/display.md) |
| Read touch input | [`features/touch.md`](./features/touch.md) |
| Get Wi-Fi 6 or Bluetooth working | [`features/wifi-and-bluetooth.md`](./features/wifi-and-bluetooth.md) |
| Play or record audio | [`features/audio.md`](./features/audio.md) |
| Use the MIPI-CSI camera | [`features/camera.md`](./features/camera.md) |
| Mount the microSD card | [`features/storage.md`](./features/storage.md) |
| Use USB (OTG host/device, serial) | [`features/usb.md`](./features/usb.md) |
| Use the 40-pin expansion header | [`features/expansion-header.md`](./features/expansion-header.md) |
| Build, flash and recover | [`development.md`](./development.md) |

## Documentation map

| Document | Contents |
|---|---|
| [`bsp-source-findings.md`](./bsp-source-findings.md) | **Facts extracted from the vendor BSP source** — pin confirmation, backlight polarity, SD slot, I²C default |
| [`official-repo-and-community.md`](./official-repo-and-community.md) | **Official GitHub repo, published BSP, factory firmware, community projects** — start here for development |
| [shared platform record](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md) | Schematic, demo archive, pin map, architecture, artifact provenance |
| [`pinouts-and-buses.md`](./pinouts-and-buses.md) | **Complete verified GPIO map** |
| [`examples/best.md`](./examples/best.md) | **Selected examples and bring-up order** |
| [`examples/catalog.json`](./examples/catalog.json) | Every discovered example with disposition |
| [`examples/search-log.md`](./examples/search-log.md) | Discovery queries and stopping criterion |
| [`development.md`](./development.md) | Toolchain, build, dual-MCU flashing |
| [`gaps-and-conflicts.md`](./gaps-and-conflicts.md) | Unresolved identities and source conflicts |
| [`coverage.md`](./coverage.md) | Feature → evidence → status map |
| [`sources.md`](./sources.md) | Full source table |
| [`research-log.md`](./research-log.md) | Queries, depth, dispositions |
| [`commands.md`](./commands.md) | Verbatim command ledger |
| [`acquisition/manifest.json`](./acquisition/manifest.json) | Machine-readable artifact acquisition record |

## Shortcomings and constraints

- **Dual-MCU complexity.** Two firmwares, two flash headers, two ways to be out of date. Waveshare
  do not appear to publish the ESP32-C6 image or its revision.
- **Silicon-revision sensitivity.** Published firmware is **rev3.x only**; pre-v3 boards need a
  different DSI PHY clock source and cannot run it as-is.
- **Small community.** Two GitHub projects target the 3.4C; none target the 4C.
- **Schematic and wiki carry no stated licence**, even though the source code is Apache-2.0.
- **Bundled LVGL 9.3.0 not verified against upstream** — patch status unknown.
- **Untested here.** No claim in this record has been validated on hardware.

## Evidence status

Everything above derives from Waveshare's published wiki, store page, schematic PDF, demo source
and **official GitHub repository**, retrieved 2026-08-24. **Nothing has been built or run on
hardware.**

Pin values were read from the schematic visually and **independently confirmed** by Waveshare's own
`docs/HARDWARE.md` — two sources agreeing. Note Waveshare themselves state their hardware contract
is compile-verified but **not** hardware-in-the-loop verified.

## Related

- [ESP32-P4-WIFI6-Touch-LCD-4C](../esp32-p4-wifi6-touch-lcd-4c/README.md) — the 4-inch sibling
- [Shared XC platform](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
- [Espressif's own P4 boards](../../espressif/) — official comparison points
- [Waveshare vendor guide](../../../vendors/waveshare/README.md)
