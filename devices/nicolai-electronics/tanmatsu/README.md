# Nicolai Electronics Tanmatsu

> "The terminal for hackers" — an ESP32-P4 handheld with a QWERTY keyboard, LoRa, MIPI DSI display and a 36-pin expansion port.
> Manufacturer: **Nicolai Electronics** (Netherlands) · Designer: **Renze Nicolai** with **Paul Honig**
> Research snapshot **2026-08-24** · Hardware repo commit `640805dd` (2026-02-25)

Tanmatsu is a conference-badge-derived, commercially sold handheld computer. It sits in the lineage of the Dutch hacker-camp badges (MCH2022, WHY2025) built by [Badge.team](https://badge.team), but is a product in its own right rather than an event giveaway.

**It is unusually well documented for a custom board, and unusually open**: the full KiCad design is published under **CERN-OHL-P**, the firmware under **MIT**, and there is a Sphinx documentation site maintained in git. The limiting factor on information is not secrecy — it is that the device is new, low-volume, and much of the detail is spread across ~10 repositories rather than being absent.

---

## Common tasks / How do I…?

| Question | Answer |
|---|---|
| What chips are on it? | [§ Architecture](#architecture-three-processors) · [`bom.md`](bom.md) |
| **How does the keyboard work? / I have spare keyboards** | [`keyboard.md`](keyboard.md) — matrix, keymap, I2C, and the Solder Party family |
| **How does the display work?** | [`display.md`](display.md) |
| **How do I build an add-on / front panel?** | [`expansion-boards.md`](expansion-boards.md) |
| **What does it cost? How big is it?** | [`pricing-and-dimensions.md`](pricing-and-dimensions.md) |
| **How does BadgeLink / AppFS work internally?** | [`badgelink-and-appfs.md`](badgelink-and-appfs.md) |
| **How is the software architected? How do I add an app?** | [`software-architecture.md`](software-architecture.md) |
| **How do I *build* an app vs a plugin?** | [`apps-vs-plugins.md`](apps-vs-plugins.md) |
| **Custom `.bin` vs installing an app? How does an app get executed?** | [`apps-vs-plugins.md` §8–9](apps-vs-plugins.md) |
| **Does this need a P4? A dual-chip setup?** | [`portability.md`](portability.md) — **no** to both |
| What is on the expansion ports? | [`pinouts-and-buses.md`](pinouts-and-buses.md) |
| How do I flash / recover it? | [`development.md`](development.md) |
| How do I write an app? | [`development.md`](development.md) · [`software-and-apps.md`](software-and-apps.md) |
| What apps exist already? | [`software-and-apps.md`](software-and-apps.md) — 57 catalogued |
| **What is "Konsool"?** | [`konsool-and-family.md`](konsool-and-family.md) — **answered** |
| What is unresolved or contradictory? | [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |
| Where did all this come from? | [`sources.md`](sources.md) |

---

## Identity: Tanmatsu, Konsool and WHY2025

Three names appear throughout the software and they are **not** interchangeable in the way you might assume:

| Name | What it is |
|---|---|
| **Tanmatsu** | The commercial product sold by Nicolai Electronics. 端末 (*tanmatsu*) is Japanese for "terminal / handheld device". |
| **Konsool** | A sibling device. The app repository states plainly: *"Since Tanmatsu and Konsool are essentially the same device we recommend always adding both to apps developed for one of these boards."* Firmware treats them as separate build targets (`CONFIG_BSP_TARGET_TANMATSU` / `CONFIG_BSP_TARGET_KONSOOL`) that share almost all code. |
| **WHY2025** | The badge for the WHY2025 hacker camp. A third BSP target (`CONFIG_BSP_TARGET_WHY2025`) sharing the same code paths. |

In the badge BSP the three appear together in the same `#if defined(...)` guards, e.g. in [`esp32-component-tanmatsu-wifi/wifi_remote.c`](artifacts/source-snapshots/):

```c
#if defined(CONFIG_BSP_TARGET_TANMATSU) || defined(CONFIG_BSP_TARGET_KONSOOL) || defined(CONFIG_BSP_TARGET_WHY2025)
```

**Practical consequence:** software written for one generally runs on the others, and app authors are asked to declare multiple targets. Of the 57 apps in the official repository, **54 declare `tanmatsu`, 43 declare `konsool`, and only 4 declare `why2025`** — so the Tanmatsu/Konsool pair is the real ecosystem.

> The exact commercial and organisational relationship between the three names — and why a second name exists at all — is **not explained in any repository or document I retrieved**. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md). I am deliberately not repeating community speculation about naming disputes as fact.

---

## Key specifications

| | |
|---|---|
| **Application processor** | **Espressif ESP32-P4NRW32** — dual-core 32-bit RISC-V, **32 MB in-package PSRAM** |
| Clock | **360 MHz or 400 MHz — the vendor's own docs disagree**, see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |
| **Flash** | **Winbond W25Q128JVS**, 16 MB (128 Mbit), SOIC-8 |
| **Radio module** | **Espressif ESP32-C6-WROOM-1-N8** — RISC-V @160 MHz, 512 KB RAM, 8 MB flash. Wi-Fi 6 (2.4 GHz), BLE 5.3, IEEE 802.15.4 (Thread 1.3 / Zigbee 3.0) |
| **Coprocessor** | **WCH CH32V203C8T6** — RISC-V @144 MHz, 20 KB RAM, 64 KB flash, LQFP-48 |
| **LoRa** | **Ebyte E22-900M22S** (868/915 MHz) or **E22-400M22S** (433 MHz). 22 dBm |
| **Display** | **SWI LH397K-IC01**, 3.97", 480×800, RGB565, **ST7701S** controller, **MIPI DSI 2-lane**, 330 cd/m² |
| **Keyboard** | 69-key QWERTY + 6 coloured function keys, metal dome sheet, white LED backlight. Designed by **Solder Party** |
| **Battery** | 2500 mAh LiPo, 3.7 V nominal, "104050", JST PH-2.0 (Adafruit-compatible), Tewaycell |
| **Audio** | **ES8156** stereo DAC/codec + **FM8002A** mono amp → 8 Ω speaker; 3.5 mm jack |
| **PMIC** | **TI BQ25895RTW** — charger, monitoring, 5 V boost |
| **3.3 V rail** | **TI TPS63020DSJR** buck-boost |
| **IMU** | **Bosch BMI270** accel + gyro |
| **LEDs** | 6 × **SK6805-EC20** addressable |
| **USB** | **CH334R** 4-port hub; USB-C device + USB-A host (1 A, current limited) |
| **Storage** | microSD, SDIO 2.0/3.0, **3.3 V and 1.8 V** signalling |
| **Camera** | 22-pin MIPI CSI, Raspberry Pi Zero/5 pinout compatible |
| **Case** | 3D printed, **120 × 135 × 18 mm**, **215 g** with battery |
| **Mainboard PCB** | **~114.9 mm wide** — *measured from `tanmatsu.step`, not vendor-published*. See [`pricing-and-dimensions.md`](pricing-and-dimensions.md) |
| **Price** | **€99.17** ex VAT / **€119.99** inc 21% NL VAT (2026-08-24) |

Full reference-designator BOM with LCSC part numbers: [`bom.md`](bom.md) · raw [`artifacts/production/bom.csv`](artifacts/production/bom.csv)

---

## Architecture: three processors

Tanmatsu is not a single-MCU board. Three processors run concurrently, each owning a distinct domain.

```
                    ┌──────────────────────────────────────────┐
   USB-C ──► CH334R │  ESP32-P4 (U7)  dual RISC-V, 32MB PSRAM  │
      hub  ─┬──────►│  application processor · 16MB W25Q128    │
            │       │  MIPI DSI display · MIPI CSI camera      │
            │       │  SDIO · I2S · I3C · USB OTG ×2 PHY       │
            │       └───────┬──────────────────────────────────┘
            │          internal I2C (GPIO9 SDA / GPIO10 SCL)
            │               │
            │       ┌───────▼──────────────────────────────────┐
            │       │  CH32V203C8T6 (U12) @0x5F                │
            │       │  keyboard matrix scan · RTC (32.768kHz)  │
            │       │  backlight PWM ×2 · PMIC control         │
            │       │  power sequencing · SK6805 LEDs          │
            │       │  headphone detect · USB-A power switch   │
            │       └───────┬──────────────────────────────────┘
            │           PMIC I2C │  BQ25895 @0x6A
            │                    ▼
            └──────►┌──────────────────────────────────────────┐
                    │  ESP32-C6-WROOM-1 (U20)                  │
                    │  Wi-Fi 6 / BLE 5.3 / 802.15.4            │
                    │  runs esp-hosted — a *radio peripheral*, │
                    │  not a general applications processor    │
                    └──────────────────────────────────────────┘
                    ┌──────────────────────────────────────────┐
                    │  E22-900M22S (U23)  LoRa, SPI            │
                    └──────────────────────────────────────────┘
```

**The coprocessor is the interesting design decision.** The CH32V203 is always powered — a small **LR8341A-M25** LDO keeps its `Vbatt` rail at 2.5 V even when the device is "off". Nicolai Electronics claims this draws so little that *"theoretically the battery would last over 10 years on a single charge if the device is never turned on, ignoring LiPo self-discharge"*. This is what lets the RTC keep time while off, and a **latch circuit lets the coprocessor power the whole device on from an RTC alarm by emulating a press of the power button**.

The coprocessor firmware is reflashable **from the ESP32-P4** over RVSWD, using a dedicated Espressif component ([`nicolaielectronics/rvswd`](https://components.espressif.com/components/nicolaielectronics/rvswd)) that can reprogram CH32V20x/CH32V30x parts. That is a genuinely unusual capability: the main SoC can reflash its own power controller.

Component records:
[ESP32-P4](../../../components/espressif/esp32-p4/README.md) ·
[ESP32-C6-WROOM-1](../../../components/espressif/esp32-c6-wroom-1/README.md) ·
[CH32V203C8T6](../../../components/wch/ch32v203c8t6/README.md) ·
[W25Q128JVS](../../../components/winbond/w25q128jv/README.md) ·
[BQ25895](../../../components/texas-instruments/bq25895/README.md) ·
[TPS63020](../../../components/texas-instruments/tps63020/README.md) ·
[ES8156](../../../components/everest-semiconductor/es8156/README.md) *(maker: [Everest Semiconductor](../../../vendors/everest-semiconductor/README.md))* ·
[BMI270](../../../components/bosch-sensortec/bmi270/README.md) ·
[E22-900M22S](../../../components/ebyte/e22-900m22s/README.md) ·
[CH334R](../../../components/wch/ch334r/README.md) ·
[SK6805-EC20](../../../components/normand/sk6805-ec20/README.md) ·
[ST7701S / LH397K-IC01](../../../components/sitronix/st7701s/README.md)

---

## Distinctive strengths

**Genuinely open hardware.** CERN-OHL-P KiCad sources, not just a PDF. You can open `tanmatsu.kicad_pcb`, change it, and fabricate it. The BOM ships with LCSC part numbers for every line.

**The ESP32-P4 with 32 MB PSRAM** is a lot of memory for a microcontroller-class device, and it is what makes an 800×480 framebuffer, emulators and a video player practical.

**Two well-thought-out expansion ports.** The rear 36-pin "personality module" port exposes 14 GPIO, all four power rails, USB, I2C, I3C and I2S. The side "CATT" port is simultaneously **PMOD-compatible, SAO-compatible and a JTAG port** — a genuinely clever piece of connector design.

**Recovery is hard to lose.** Secure boot is *permanently disabled by design* to prevent bricking, the ROM bootloader is always reachable by holding the `-` button at power-on, and the USB-C port reaches the P4, the C6 *and* an expansion device through a hub.

**Radio-rich**: Wi-Fi 6, BLE 5.3, Thread, Zigbee *and* LoRa in one handheld is an unusual combination.

## Shortcomings and constraints

- **The ESP32-P4 datasheet was not public** at the time the vendor documentation was written ("The datasheet for this chip is not yet publicly available"). Much P4-specific detail must come from ESP-IDF sources.
- **No Wi-Fi/BLE in the main SoC.** The ESP32-P4 has no radio; all networking goes through the ESP32-C6 over `esp-hosted`, which adds latency and a second firmware to maintain.
- **Camera software support is narrow** — "limited to a subset of Raspberry Pi compatible camera module sensor chips such as OV5647", despite the connector being physically RPi-compatible.
- **Display colour depth is under-used**: the panel does RGB888 but "current software can not make use of this mode".
- **Shared-function pins** on the expansion header: using the I2S or I3C pins as GPIO disables on-board audio or the QWIIC port respectively.
- **Hard current limits**: ≤1 A total from all 3.3 V outputs, ≤1.5 A from the battery, and **do not charge the battery via the internal add-on port**.
- **Availability.** Pre-order only for much of its life, and only the 868/915 MHz external-antenna variant has been offered.
- **Documentation carries an explicit health warning**: *"information on this page is actively being worked on and might contain accidental errors and inaccuracies."* It does contain at least one — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

---

## Licensing

| Component | Licence |
|---|---|
| Hardware design (`tanmatsu-hardware`) | **CERN-OHL-P** (permissive) |
| Mechanical design (`tanmatsu-mechanical`) | **CERN-OHL-P** |
| Launcher firmware | **MIT** |
| Coprocessor firmware | **MIT** |
| Wi-Fi component | **MIT** |
| Radio (C6) firmware | **Apache-2.0** |
| Documentation, template, app-repository | **no licence file** |
| Branding / logos / artwork | **All rights reserved** — explicitly excluded from the hardware licence |

That last row matters if you fork the design: the electronics are permissively licensed, but *"all organization names, logos, trademarks and artwork including but not limited to the Nicolai Electronics and Tanmatsu branding are all rights reserved… and may not be reproduced on derivative works."*

---

## Documentation map

| Document | Contents |
|---|---|
| [`pinouts-and-buses.md`](pinouts-and-buses.md) | Expansion ports, I2C map, GPIO assignments |
| [`keyboard.md`](keyboard.md) | Keyboard matrix, keymap, backlight, and the Solder Party KeebDeck / BlackBerry keyboard families |
| [`display.md`](display.md) | Panel, MIPI DSI, driver stack, mandatory PSRAM config |
| [`konsool-and-family.md`](konsool-and-family.md) | **What Konsool is**, how WHY2025 differs, the badge family |
| [`mechanical-and-case.md`](mechanical-and-case.md) | Case, board revisions, front panels, FreeCAD workflow |
| [`expansion-boards.md`](expansion-boards.md) | Existing add-ons, front-panel fab specs, add-on design rules |
| [`pricing-and-dimensions.md`](pricing-and-dimensions.md) | Prices, spare parts, availability, measured dimensions |
| [`badgelink-and-appfs.md`](badgelink-and-appfs.md) | BadgeLink wire protocol and AppFS internals |
| [`software-architecture.md`](software-architecture.md) | Launcher architecture, app tiering, **plugin system**, eFuse identity, recent changes |
| [`apps-vs-plugins.md`](apps-vs-plugins.md) | **Build systems compared**, app execution, custom `.bin` vs install, plugin loader validation |
| [`portability.md`](portability.md) | Which chips run the launcher and AppFS; what is genuinely P4-only |
| [`coverage.md`](coverage.md) | Feature → evidence → gap map |
| [`research-log.md`](research-log.md) | Queries run, sources found and rejected |
| [`commands.md`](commands.md) | Command ledger with execution status |
| [`bom.md`](bom.md) | Full BOM with LCSC parts and function notes |
| [`development.md`](development.md) | Flash layout, esptool, AppFS, BadgeLink, toolchain |
| [`software-and-apps.md`](software-and-apps.md) | Launcher, app repository, 57 catalogued apps |
| [`gaps-and-conflicts.md`](gaps-and-conflicts.md) | Contradictions and unknowns |
| [`sources.md`](sources.md) | Repositories, commits, licences, retrieval dates |

## Artifact layout

```
artifacts/
├── schematics/         schematic.pdf + full KiCad sources (CERN-OHL-P)
├── production/         bom.csv, designators, positions, netlist.ipc
├── source-snapshots/   complete official documentation source
└── app-repository-catalog.json   57 apps, machine-readable
```

## Provenance note

Everything here derives from **primary sources**: the vendor's own KiCad design files, production BOM, and Sphinx documentation source, all cloned at pinned commits on 2026-08-24 (see [`sources.md`](sources.md)). **No hardware was available** — nothing here is a firsthand measurement, and no firmware was built or flashed.
