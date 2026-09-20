# LoRa — SX1262 or LR2021, and Meshtastic

**Question:** *How do I send LoRa, and which radio should I buy?*

| | |
|---|---|
| Radio (option A) | [Semtech SX1262](../../../../components/semtech/sx1262/README.md) |
| Radio (option B) | [Semtech LR2021](../../../../components/semtech/lr2021/README.md), 830–940 MHz |
| Bus | SPI — MOSI `GPIO16`, MISO `GPIO17`, SCK `GPIO15`, CS `GPIO14` |
| Control | RESET `GPIO5`, BUSY `GPIO19`, **IRQ `GPIO20`**, power enable `GPIO44` |
| Kernel | **spidev** (`0054-riscv-dts-rm69a10-enable-lora-spidev.patch`) |
| Userspace | **RadioLib** |
| Evidence | `reported-working` |

## Choose the radio before you buy

| SKU | Radio | Band | Price 2026-09-04 | Meshtastic capability |
|---|---|---|---:|---|
| `K256` / `-A` / `-B` / `-C` | SX1262 | 868 / 915 / 923 / 433 MHz | $98.79 | text mesh only |
| `K256-03` (kit) | SX1262 | 868 MHz | $150.31 | text mesh only |
| **`K277`** (kit) | **LR2021** | 830–940 MHz | $153.01 | **voice and photo transfer** |

LilyGO states it plainly: *"Voice/photo transfer is only available between K230 boards fitted
with LR2021 modules; SX1262 boards support basic text mesh messages only."* For **$2.70** more at
kit level, the LR2021 unlocks a capability class. If mesh voice or images matter at all, buy
`K277`.

## The DIO trap

Both radios connect their interrupt to K230 `GPIO20`, but from **different radio pins**:

- **SX1262 → `DIO1`**
- **LR2021 → `DIO11`**

A driver that hard-codes `DIO1` sees no interrupts on an LR2021 board and looks like dead
hardware. Configure per fitted part.

## Software model

The radio is **not** a kernel LoRa driver. The device tree exposes plain **spidev** and
everything happens in userspace through **RadioLib**, including reset, which LilyGO notes is
"controlled by the RadioLib HAL".

Consequences:

- Any process that can open the spidev node can corrupt radio state. There is **no kernel-side
  arbitration** between the Meshtastic app, the LoRa test app and the FLRC bench — the launcher
  arbitrates internally, and only internally.
- Porting RadioLib code from an Arduino board is mostly a matter of writing a Linux spidev +
  gpiod HAL, which LilyGO has already done.

## What ships

| App | Status | Notes |
|---|---|---|
| **Meshtastic** | **Beta** | chat, node list, map view, channel sharing; on-device **map tile download** added v0.2.4 |
| **LoRaWAN** | Beta | `lorawan_test.cpp` |
| **LoRa tools** | v0.2.4 added radio-model persistence and cleaner RF-test profile controls | `ui_lora.cpp` |
| **FLRC bench** | present | `lora_flrc_bench.cpp` |
| **FLRC camera stream** | present | `k230_flrc_camera_stream.sh` — images over a LoRa-family modulation |
| Meshtastic probe | present | `k230_meshtastic_probe.cpp` |

An **independent** Meshtastic UI is in progress: r/meshtastic, 2026-06-02 — *"I am working on a
full Meshtastic UI app for this and will publish a repo once complete. Lots of challenges
adapting everything to the K230's preferred formats but making progress."* (announced project,
no repository at the time of writing).

## Antenna

Product photography shows a LoRa antenna. **No external-antenna connector option is offered**,
and a user asked for one on 2025-03-24 without a recorded response.

## Limits

| Limit | Value | Class |
|---|---|---|
| Radios fitted | one, chosen at purchase | board |
| Band | fixed per SKU | board |
| Meshtastic voice/photo | **LR2021 only** | board |
| Kernel arbitration | none — spidev | framework |
| Link budget, range, TX current | **not published for this board** | unmeasured |
| Regulatory certification | **not established** | unknown |

## Pitfalls

1. Buying `K256-03` and then wanting mesh voice.
2. Hard-coding `DIO1`.
3. Forgetting `GPIO44` — the radio is unpowered until you assert it.
4. Two programs opening spidev at once.
