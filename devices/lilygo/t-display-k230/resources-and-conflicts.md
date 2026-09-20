# T-Display K230 — resources, ownership and conflicts

Evidence status throughout: **`reported-working`** or **`inferred`**, never `executed-*`. No
hardware was available.

## 1. Hard conflicts — things that physically cannot coexist

| # | Conflict | Why | Consequence |
|---|---|---|---|
| **HC-1** | **AMOLED panel vs LT9611 HDMI output** | The K230 has **exactly one MIPI DSI output** (Canaan brief datasheet: "1 × MIPI DSI"). Both sinks are DSI. | Mutually exclusive, and resolved at **boot time by device tree**: `canaan/k230-canmv-rm69a10` vs `canaan/k230-canmv-rm69a10-hdmi`. There is no runtime switch. LilyGO: "HDMI support is kept as a diagnostic feature. AMOLED remains the default display path." |
| **HC-2** | **GT9895 touch vs LT9611 control lines** | Both use I²C3 (`GPIO37`/`GPIO36`), IRQ `GPIO23` and reset `GPIO24`. | A reset asserted for one resets the other. They must occupy different I²C addresses. Since HC-1 already makes them exclusive in practice, this is mostly a diagnostic-mode hazard. |
| **HC-3** | **BOOT0 button vs `IO0` boot strap** | `GPIO0` is both the BOOT0 strap and the button the launcher reads for screen toggle. | Holding the button through reset changes boot behaviour. Do not wire anything else to it. |
| **HC-4** | **Two base boards, one 40-pin header** | The nRF52840 base and the nRF9151 keyboard base both plug into the same 2 × 20 header and both claim `GPIO46`/`GPIO47`. | You get one base at a time. The launcher detects which. |

## 2. Shared buses

### I²C4 (`GPIO46` SCL / `GPIO47` SDA) — the crowded one

Carries, depending on base board: TCA8418 `0x34`, AHT20 `0x38`, BQ27220 `0x55`, BQ25896 `0x6B`,
XL9555 **`0x20`–`0x27` (probed)**. It is **also exposed on the 40-pin header**, so any user
peripheral joins the same bus as the keyboard scanner and the charger.

Three practical rules:

1. **Never hard-code the XL9555 address.** LilyGO's own software probes and caches it.
2. **Anything you add in `0x20`–`0x27` may shadow the expander.** Pick outside that block.
3. **Bus errors take down power management, not just your device.** A peripheral that holds SDA
   low blinds the charger and gauge, and the launcher's low-battery shutdown depends on gauge
   reads. Consider that before hanging a marginal sensor on this bus.

### SPI — LoRa only

`GPIO15/16/17` + CS `GPIO14`, exposed to userspace through **spidev**
(`0054-riscv-dts-rm69a10-enable-lora-spidev.patch`). The radio is driven by **RadioLib from
userspace**, not by a kernel LoRa driver. Two consequences: any process can open the spidev node
and corrupt radio state, and there is no kernel-side arbitration between, say, the Meshtastic app
and the LoRa test app. The launcher arbitrates in software; another program does not have to.

### SDIO / SD-MMC

Two controllers. **MMC1 (`GPIO54`–`GPIO59`) is the microSD and is the boot medium.** The Wi-Fi
module is on the other SDIO controller. They do not contend.

### I²S

`GPIO32/33/35` + shutdown `GPIO34` reach the MAX98357A on the nRF52840 base. The K230 also has
an **on-die codec** with its own DAC/ADC path, so there are two audio outputs and the BSP adds
`0059-asoc-canaan-add-external-i2s-output-switch.patch` to choose between them. **Choosing the
wrong route is the most likely "no sound" cause** on this board.

### USB

Both K230 USB 2.0 OTG controllers are in play: one is the **host** carrying Ethernet (RTL8152B),
the Bluetooth dongle and any USB modem; one is used for the **gadget** side — the rootfs overlay
ships `k230-usb-storage-gadget` and `/etc/default/k230_usb_storage`, and the kernel fragment
enables `USB_CONFIGFS` with mass storage, RNDIS and ACM functions. Enabling USB mass-storage
gadget on the same port you are using for host devices is the obvious conflict.

## 3. Ownership arbitration the launcher performs

These are software policies, not hardware interlocks. Anything running outside the launcher can
break them.

| Resource | Contenders | Arbitration |
|---|---|---|
| **nRF52840 UART (`/dev/ttyS1`)** | Meshtastic BLE app, nRF52840 UART DFU | Explicit ownership coordination, added in BSP **v0.2.2** |
| **Microphone** | Xiaozhi wake-word listener, recorder, mic spectrum | "Wake-word listening is active only while the Xiaozhi app is open and **owns the microphone**" |
| **LoRa spidev** | Meshtastic, LoRaWAN test, FLRC bench, RF test profiles | Launcher-internal only |
| **`GPIO42` IOMUX** | kernel pinctrl, launcher | The launcher **writes the K230 IOMUX register for `GPIO42` directly** to force GPIO-input mode. If a kernel driver later re-muxes it, the keyboard IRQ stops. |
| **Display framebuffer** | U-Boot boot logo, kernel DRM, LVGL | Three patches manage the handoff (`0038`, `0051`, `0043`) |

## 4. Interrupts

| Line | Owner | Note |
|---|---|---|
| `GPIO23` | GT9895 touch **and** LT9611 | see HC-2 |
| `GPIO20` | LoRa — **`DIO1` on SX1262, `DIO11` on LR2021** | same K230 pin, different radio pin |
| `GPIO42` | TCA8418 keyboard | launcher forces the IOMUX |
| `GPIO64` (PMU INT0) | power key | routed to **CPU IRQ 175** |
| `GPIO0` | BOOT0 button | also a boot strap |

## 5. Power rails and domains

| Rail | Notes |
|---|---|
| USB-C in | **5 V, 500 mA** per the product page — a modest charge budget for a 1.6 GHz SoC plus an AMOLED |
| 21700 cell | in the keyboard base compartment |
| **5 V boost** | enabled by the **nRF52840's `P0.04`**, supplying the host unit from the 21700 |
| 3V3 / 5V on header | pins 19/20 of the 40-pin header, plus `USB-IN-5V` |
| PMIC | **unidentified** — [`components/unidentified/t-display-k230`](../../../components/unidentified/t-display-k230/README.md) U1 |

**The boost-enable arrangement is worth stating plainly:** on a kit configuration the *companion
MCU on an expansion board* controls the 5 V rail that powers the main unit from the battery. If
the nRF52840 firmware is wedged or being reflashed, that is a power dependency, not just a
comms dependency.

Low-battery shutdown is a **userspace policy** in `ui_hardware.c` driven by BQ27220 readings and
gated on BQ25896 USB-present, with a confirm count before acting. It is not a hardware cut-off.

## 6. Memory and storage

| Resource | Size | Notes |
|---|---|---|
| LPDDR4 | **1 GB** (8 Gb, 32-bit) | Product specification. **Note:** the Canaan U-Boot reference DTS this BSP derives from declares `memory@0 … 0x20000000` = **512 MB**; that is the upstream CanMV-v3 baseline, not necessarily what the LilyGO build uses. Unverified — [`GC-7`](gaps-and-conflicts.md). |
| K230 SRAM | 2 MB shared + 2 MB KPU | see the component record |
| microSD | user-supplied | Holds the whole system image. BSP v0.2.4 added **storage expansion for cards larger than the flashed image** — before that, the extra space was simply unused. |
| Flash | LilyGO's wiki says **16 MB**; the BSP boots from SD | Role unclear; possibly the boot SPI NOR. Unverified. |

## 7. Realistic simultaneous-use scenarios

| Scenario | Assessment |
|---|---|
| Display + touch + keyboard + Wi-Fi | Expected to work; this is the shipped default |
| Display + camera + KPU inference | Supported by design (ISP → KPU); no throughput figure published |
| Camera RTSP + Wi-Fi | `camera_rtsp_demo` package is built in; bandwidth impact unmeasured |
| LoRa + Wi-Fi | Different buses; no conflict. 2.4 GHz Wi-Fi and sub-GHz LoRa do not share spectrum. |
| Bluetooth + Wi-Fi | **Bluetooth is a USB dongle**, so this is a USB-bandwidth question, not an RF-coexistence one — unusually, it avoids the classic combo-chip coexistence problem entirely |
| HDMI + AMOLED | **Impossible** (HC-1) |
| USB mass-storage gadget + USB Ethernet | Contends for USB roles; untested |
| Audio out (I²S amp) + microphone capture | K230 supports simultaneous I²S-out and PDM/ADC-in per its datasheet; on this board, untested |
| nRF52840 DFU + Meshtastic BLE | **Arbitrated in software only** (v0.2.2) |
