# Espressif — Ecosystem and Product Lines

A **map**, not a datasheet. This page exists to answer *"which Espressif chip should this be, and
why?"* and to make the family tree legible. Where a chip already has a deep record in this
repository, **this page links to it rather than restating it** — the detail lives there.

- **Compiled:** 2026-08-24. Chip-roster enumeration retrieved 2026-08-24 **[WEB]**.
- **Deep records this page defers to:** [ESP32-P4](../../components/espressif/esp32-p4/README.md) ·
  [ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md) ·
  [ESP32-U4WDH](../../components/espressif/esp32-u4wdh/README.md)
- **Document sourcing:** [Espressif vendor guide](../../vendors/espressif/README.md)

> **Evidence labels** follow the repository convention: **[DOC]** vendor document · **[WEB]** vendor
> web page · **[SCH]** schematic · **[SRC]** source code · **[COM]** community · **[INF]** inference.
> **Most of the per-chip capability claims on this page are [INF] or recalled general knowledge**,
> not read from datasheets in this pass. See §9. The claims that *are* firmly evidenced are the ones
> about **P4, S3 and the classic ESP32**, because those have their own researched records.

---

## 1. The roster, as Espressif publishes it

Enumerated from `https://www.espressif.com/en/products/socs`, retrieved 2026-08-24 **[WEB]**. The
page lists these SoC families:

> ESP8266 · ESP32 (incl. `ESP32-D0WD`, `ESP32-S0WD`, `ESP32-PICO`) · **ESP32-S** series ·
> **ESP32-C** series: C2, C3, C5, C6, **C61** · **ESP32-H** series: H2, **H21**, **H4** ·
> **ESP32-P** series: P4

**C61, H21 and H4 are real, currently-listed parts that this repository knows essentially nothing
about.** They are recorded here so the map is not silently out of date; do not infer capabilities for
them from their siblings' letters.

---

## 2. The family tree

```
ESP8266  ──────────────────────────────────► the origin. Wi-Fi only, Xtensa L106, single core
   │
   ▼
ESP32 (classic) ───────────────────────────► Xtensa LX6. THE ONLY LINE WITH CLASSIC BLUETOOTH
   │                                          e.g. ESP32-D0WD-V3, ESP32-U4WDH
   ├──────────────► ESP32-S2 ───────────────► Xtensa LX7, single core. Wi-Fi, USB OTG, NO Bluetooth
   │                    │
   │                    ▼
   │                ESP32-S3 ───────────────► Xtensa LX7, dual core. Wi-Fi + BLE 5. USB OTG. AI vector ops
   │
   ├──────────────► ESP32-C3 ───────────────► FIRST RISC-V part. Wi-Fi + BLE 5. The ESP8266 successor
   │                    ├── ESP32-C2 ───────► cost-reduced C3 (a.k.a. ESP8684)
   │                    ├── ESP32-C6 ───────► Wi-Fi 6 (2.4 GHz) + BLE + 802.15.4 (Thread/Zigbee)
   │                    ├── ESP32-C5 ───────► DUAL-BAND Wi-Fi 6 (2.4 + 5 GHz) + BLE + 802.15.4
   │                    └── ESP32-C61 ──────► (listed; not characterised here)
   │
   ├──────────────► ESP32-H2 ───────────────► NO Wi-Fi. BLE + 802.15.4 only
   │                    └── H21 / H4 ───────► (listed; not characterised here)
   │
   └──────────────► ESP32-P4 ───────────────► NO RADIO AT ALL. Dual RISC-V, MIPI-DSI/CSI, H.264
```

**The three axes that actually matter** — and note they are independent:

1. **Radio**: Classic BT / BLE-only / BLE + 802.15.4 / no Wi-Fi / **no radio at all**
2. **ISA**: Xtensa (8266, ESP32, S2, S3) vs **RISC-V** (everything from C3 onwards, plus P4)
3. **Role**: connectivity-first (C/H series) vs application-first (S3, P4)

---

## 3. Radio capability — the decision that cannot be undone in software

This is the first thing to check and the most expensive thing to get wrong.

| Chip | Wi-Fi | Classic BT (BR/EDR) | BLE | 802.15.4 |
|---|---|---|---|---|
| ESP8266 | b/g/n 2.4 GHz | ❌ | ❌ | ❌ |
| **ESP32 (classic)** | b/g/n 2.4 GHz | ✅ **the only line** | ✅ | ❌ |
| ESP32-S2 | b/g/n 2.4 GHz | ❌ | ❌ | ❌ |
| **ESP32-S3** | b/g/n 2.4 GHz | ❌ **[DOC]** | ✅ BLE 5 | ❌ |
| ESP32-C3 / C2 | b/g/n 2.4 GHz | ❌ | ✅ | ❌ |
| ESP32-C6 | **Wi-Fi 6**, 2.4 GHz | ❌ | ✅ | ✅ |
| ESP32-C5 | **Wi-Fi 6, 2.4 + 5 GHz** | ❌ | ✅ | ✅ |
| ESP32-H2 | ❌ | ❌ | ✅ | ✅ |
| **ESP32-P4** | ❌ **[DOC]** | ❌ | ❌ | ❌ |

**[INF]** for every row except ESP32-S3 and ESP32-P4, which are **[DOC]** via their component records.

### The Classic Bluetooth cliff

**Only the original ESP32 line has Bluetooth Classic.** Not the S2, not the S3, not any RISC-V part.
This is a **hardware** absence — no SDK version can add it.

This repository contains the definitive worked example of what that costs, and it is worth reading
before selecting any S3:

- [ESP32-S3R8 § Radio capabilities and the Classic Bluetooth limitation](../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation)
  — why it is absent, how people discover it, and the three ways out.
- The [Waveshare knob board](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) fits **an
  entire second MCU** — an [ESP32-U4WDH](../../components/espressif/esp32-u4wdh/README.md) — whose
  only job is Classic Bluetooth. Second crystal, second antenna, second flash, an inter-MCU UART, a
  private protocol, and a **split audio path neither chip can drive alone**. See
  [dual-mcu-architecture.md](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md)
  and [classic-bluetooth.md](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/classic-bluetooth.md).

**Rule of thumb, from that record:** "Bluetooth" in a requirement almost never means "Bluetooth LE".
Ask which *profiles* — A2DP, AVRCP, SPP, HFP, Classic HID — before choosing a part.

---

## 4. Xtensa vs RISC-V

| | Xtensa | RISC-V |
|---|---|---|
| Chips | ESP8266 (L106), ESP32 (LX6), S2/S3 (LX7) | C2, C3, C5, C6, C61, H2, H21, H4, **P4** |
| Toolchain | Espressif-maintained GCC fork | Increasingly **upstream** RISC-V GCC/LLVM |
| Direction of travel | **No new Xtensa parts have been announced** | Every new family since C3 |
| Practical impact | Almost none — ESP-IDF abstracts it | Better third-party tooling, Rust support, debuggers |

**Does it matter to you?** Usually not: ESP-IDF hides the ISA, and the same application code builds
for both. It matters when you are doing hand-written assembly, using an external debugger, working in
Rust (RISC-V support is more mature), or making a **long-term platform bet** — and on that last point
the direction is unambiguous. **[INF]**

The interesting exception is the **S3's vector instructions**, an Xtensa LX7 extension used by
`esp-dsp` and `esp-sr` for AI/DSP workloads. No RISC-V Espressif part currently matches it, which is
why the S3 remains the choice for on-device audio wake-word and light ML. **[INF]**

---

## 5. Choosing a part

| If you need… | Choose | Because |
|---|---|---|
| Cheapest possible Wi-Fi | **ESP32-C2** or ESP8266 | Cost-optimised; C2 is the modern option |
| Wi-Fi + BLE, small and cheap | **ESP32-C3** | The default modern general-purpose part |
| **Bluetooth Classic (A2DP/SPP/HFP)** | **ESP32 classic** — and *only* this | §3. There is no alternative |
| Rich UI, big display, camera, audio, AI | **ESP32-S3** | Dual core, PSRAM, USB OTG, vector ops |
| USB device, no Bluetooth needed | ESP32-S2 | Cheaper S3 without the radio you're not using |
| Thread / Zigbee / Matter | **ESP32-C6** or **ESP32-H2** | 802.15.4. H2 if you want *no* Wi-Fi |
| Wi-Fi 6 on **5 GHz** | **ESP32-C5** | The only dual-band part |
| **MIPI display / camera, H.264, real GPU-ish throughput** | **ESP32-P4** | And plan a companion radio — §6 |
| Battery-powered sensor, BLE only | ESP32-H2 or C3 | |

### Where PSRAM enters

Large framebuffers force PSRAM. A 360×360 16-bit display is ~259 KB per buffer — already awkward in
the S3's 512 KB SRAM once LVGL, Wi-Fi and the BT stack want their share. That is why our knob board
uses an **S3R8**: `R8` = **8 MB in-package PSRAM**. See
[ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md).

---

## 6. The companion-radio pattern (P4 + C6/C5)

The ESP32-P4 has **no radio of any kind** **[DOC]** — a deliberate choice, not an omission. It buys
die area for MIPI-DSI/CSI, H.264, and dual RISC-V cores.

So Espressif pairs it with a second Espressif chip acting purely as a radio, connected over SDIO or
SPI and driven by the `esp_hosted` / `esp_wifi_remote` components, so that **application code calls
the normal Wi-Fi APIs** and the transport is transparent. **[INF]** on the mechanism; **[DOC]** on the
pairings, which are visible across all five documented P4 boards:

| Board | Companion | Radio |
|---|---|---|
| [ESP32-P4X-Function-EV-Board](../../devices/espressif/esp32-p4x-function-ev-board/README.md) | ESP32-C6-MINI-1 | Wi-Fi 6, 2.4 GHz |
| [ESP32-P4X-C5-Function-EV-Board](../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md) | **ESP32-C5-MINI-1** | Wi-Fi 6, **2.4 + 5 GHz** |
| [ESP32-P4X-EYE](../../devices/espressif/esp32-p4x-eye/README.md) | ESP32-C6-MINI-1U | external antenna |
| [ESP32-P4-Function-EV-Board](../../devices/espressif/esp32-p4-function-ev-board/README.md) (EOL) | ESP32-C6-MINI-1 | |
| [ESP32-P4-EYE](../../devices/espressif/esp32-p4-eye/README.md) (EOL) | ESP32-C6-MINI-1U | |

### Two companion patterns, and they are not the same thing

It is worth being precise, because this repository documents both:

| | **P4 + C6** (designed-in) | **S3 + U4WDH** (retrofit) |
|---|---|---|
| Why | The P4 has no radio *by design* | The S3 lacks *one specific profile set* |
| Interface | SDIO/SPI, vendor-supported | UART, **private undocumented protocol** |
| Software | Transparent — normal Wi-Fi APIs | Custom on both sides |
| Cost | Planned | A second firmware image, a doubled flashing procedure, permanent cross-chip coupling |
| Verdict | Clean architecture | A workaround for a part-selection mistake |

The lesson is in the contrast: a companion radio is **fine when designed in and expensive when
bolted on.** See [ESP32-P4 §14](../../components/espressif/esp32-p4/README.md#14-related-components).

---

## 7. Naming and suffix conventions

### 7.1 Classic ESP32 — the authoritative decode

Transcribed from ESP32 series datasheet v5.3, Figure 1-1 **[DOC]** (full working, including a
corrected earlier guess, in
[ESP32-U4WDH §13.1](../../components/espressif/esp32-u4wdh/README.md#131-the-ordering-nomenclature-decoded--this-replaces-11)):

```
ESP32 - D 0 W D R2 - V3
        │ │ └┬┘ │    └── Chip revision:  V3 = v3.0 or newer
        │ │  │  └─────── In-package PSRAM:  R2 = 2 MB
        │ │  └────────── Connection:  WD = Wi-Fi b/g/n + Bluetooth/BLE dual mode
        │ └───────────── In-package FLASH:  0 = none, 2 = 2 MB, 4 = 4 MB
        └─────────────── Core:  D or U = Dual core,  S = Single core
  suffixes:  H = High temperature      Q6 = QFN 6x6  (absent = QFN 5x5)
```

So **`ESP32-U4WDH`** = dual-core, 4 MB in-package flash, Wi-Fi + dual-mode Bluetooth, high-temp
grade, QFN 5×5.

**Two traps this decode exposed**, both worth carrying to any Espressif part number:

- **`U` means dual core.** An earlier `[INF]` reading assumed `U` was a package letter and concluded
  the core count was ambiguous. It was wrong, and consequentially so.
- **`H` ("High temperature") comes with a *narrower* range, not a wider one** — the opposite of the
  natural assumption. See
  [§13.3](../../components/espressif/esp32-u4wdh/README.md#133-the-temperature-trap--h-means-the-opposite-of-what-you-would-assume).
  **Never design to a temperature range from a suffix letter. Read the characteristics table.**

### 7.2 S3 and later — `R` and `N`

- **`R<n>` = in-package PSRAM in MB.** `ESP32-S3R8` = **8 MB PSRAM**. It is **not** flash — our knob
  board supplies its 16 MB flash externally as a
  [Winbond W25Q128JVPIQ](../../components/winbond/w25q128jv/README.md). See
  [ESP32-S3R8 § Limits](../../components/espressif/esp32-s3r8/README.md).
- **`N<n>` = in-package flash in MB**, e.g. `ESP32-S3-WROOM-1-N16R8` = 16 MB flash + 8 MB PSRAM.
  **[INF]**

### 7.3 The `P4X` trap

**`P4X` is not a different chip.** It denotes a *board* fitted with ESP32-P4 silicon revision **v3.1
or later**. Same die family, different stepping — and different applicable errata. See
[devices/README.md](../../devices/README.md) and
[ESP32-P4 § The "P4X" naming trap](../../components/espressif/esp32-p4/README.md#the-p4x-naming-trap). **[DOC]**

### 7.4 Related myth

**There is no ESP32-P4 Korvo board.** Korvo is an audio/HMI family on the S3. See
[devices/README.md](../../devices/README.md). **[DOC]**

---

## 8. Bare chip vs module vs devkit

| Form | What it is | Choose when |
|---|---|---|
| **Bare chip** (`ESP32-S3R8`, `ESP32-U4WDH`) | The QFN die package | You are laying out your own RF, crystal, antenna and matching — and can certify it |
| **Module** (`ESP32-S3-WROOM-1`, `ESP32-C6-MINI-1`) | Chip + flash + PSRAM + crystal + antenna + shield, **pre-certified** | **The default.** Inherits FCC/CE/IC certification |
| **Devkit** (`ESP32-S3-DevKitC-1`) | Module + USB-UART + regulator + headers | Development and prototyping |

**The `U` suffix on a module** (`ESP32-C6-MINI-1U`) means **external antenna connector instead of the
PCB antenna** — used by the [P4-EYE boards](../../devices/espressif/esp32-p4x-eye/README.md) where the
enclosure blocks a PCB antenna. **[DOC]** via those board records.

**Certification is the real reason modules dominate.** A bare chip means your product needs its own
radio certification, which costs far more than the module premium at anything below very high volume.
**[INF]**

Note that our knob board uses **bare chips with discrete
[ceramic antennas](../../components/generic/ceramic-antenna/README.md)** — two of them, one per MCU —
which is the harder path and consistent with a vendor doing high volume.

---

## 9. Evidence boundary

**Read this before quoting anything above.**

- **[WEB] verified 2026-08-24:** the §1 chip roster, enumerated from
  `https://www.espressif.com/en/products/socs`. This establishes *which families Espressif currently
  lists*, and nothing more.
- **[DOC] via this repository's own researched records:** the ESP32-S3's lack of Classic Bluetooth;
  the ESP32-P4's lack of any radio; the classic-ESP32 nomenclature table (§7.1); the P4 board
  companion-radio pairings (§6); the `P4X` and Korvo clarifications (§7.3, §7.4). Each is linked to
  the record that carries the primary citation.
- **[INF] / recalled — NOT verified in this pass:** every other row of the §3 radio matrix; the §2
  tree's ISA and core-count details for S2, C2, C3, C5, C6, H2; §4's toolchain claims; §5's entire
  selection table; §6's description of the `esp_hosted` mechanism; §7.2's `N` suffix; §8's
  certification economics.
- **Not characterised at all:** **ESP32-C61, ESP32-H21, ESP32-H4**. They are listed in §1 because
  they exist; nothing else here applies to them.
- **No datasheet was retrieved or read in this pass.** This is a synthesis-and-navigation document
  built on top of records made 2026-08-21 to 2026-08-23. Where it disagrees with a linked deep
  record, **the deep record wins.**

---

## 10. Related

- **Components:** [ESP32-P4](../../components/espressif/esp32-p4/README.md) · [ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md) · [ESP32-U4WDH](../../components/espressif/esp32-u4wdh/README.md)
- **Devices:** [all five P4 boards](../../devices/README.md#espressif--official-esp32-p4-development-boards) · [Waveshare knob board](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md)
- **Sourcing:** [Espressif vendor guide](../../vendors/espressif/README.md) — how to obtain any Espressif document
- **Markets:** [vendor comparison](../markets/vendor-comparison.md) · [clones and variants](../markets/clones-and-variants.md)
