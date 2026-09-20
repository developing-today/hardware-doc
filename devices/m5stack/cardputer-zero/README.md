# M5Stack CardputerZero (C154 / C155-Lite)

> **SKU `C154`** (with 32 GB microSD) and **`C155`** (`-Lite`, no card) · product id **`1243`**
> Schematic `C154-CardputerZERO_SCH_V0.6.1_20260702.pdf`
> ⚠ **M5Stack's own page carries a "Work in progress" banner**: *"This product's packaging and
> software development are not yet complete. Final features and documentation are subject to
> change."* Crowdfunded on Kickstarter in spring 2026; not generally on sale as of **2026-09-04**.
> Research snapshot **2026-09-04**.

**This is not a faster Cardputer. It is a different computer that happens to be the same shape.**
Where every other Cardputer is an ESP32-S3 microcontroller, the CardputerZero is a **Raspberry Pi
Compute Module 0** running Linux — quad-core Cortex-A53, 512 MB LPDDR2, a camera, Ethernet, USB
host, an RTC and a fuel gauge.

This record is deliberately light: the product is unfinished, its documentation says so, and
committing detail now would be committing to something that will change. What is recorded here
is the identity, the confirmed architecture, and — most usefully — **what it shares with the
Cardputer ADV**.

## Identity

| Field | Value |
|---|---|
| SKUs | `C154` (32 GB card included) · `C155` **`-Lite`** (no card) |
| Core | **Raspberry Pi Compute Module 0 (CM0)** |
| CPU | RP3A0 (BCM2837), quad-core Cortex-A53 @ 1 GHz, ARMv8-A aarch64 |
| RAM | **512 MB LPDDR2** |
| Storage | microSD only |
| Display | **1.9″ ST7789v3, 320 × 170** |
| Keyboard | **46 keys** (not 56), **TCA8418RTWR @ `0x34`** |
| Camera | **IMX219 CSI 4-lane, 8 MP (3280 × 2464)** |
| IMU | **BMI270 @ `0x68`** + **BMM150 magnetometer @ `0x10`** |
| **RTC** | **RX8130CE @ `0x32`** |
| **Fuel gauge** | **BQ27220YZFR** |
| I/O expander | **M5IOE1 @ `0x4F`** |
| Audio | **ES8389** codec, MEMS mic, **AW8737A** amp, 1 W 8 Ω, **3.5 mm TRRS** with CTIA/OMTP switching |
| Video | 1080p30 out; H.264/MPEG-4 1080p30 decode, H.264 1080p30 encode |
| Network | 2.4 GHz Wi-Fi b/g/n + **10/100 Ethernet** via **SR9900A** USB-Ethernet |
| USB | **GL852G-OHY60 hub**, 1 × USB-A, 2 × USB-C, physical **Host/Slave toggle**, OTG on the right port |
| IR | **transmitter *and* receiver** |
| Expansion | **EXT 2.54-14P** + HY2.0-4P with **switchable I²C/UART** (< 500 mA on 5 V) |
| Battery | 3.7 V **1750 mAh with integrated NTC** |
| Idle power | **2.5 W** |
| Supply | 5 V @ 2 A recommended |
| Size | 84.0 × 54.0 × **23.1 mm** |

## What it shares with the Cardputer ADV

Three things, and they are worth knowing because they are reusable knowledge:

1. **The TCA8418RTWR keypad scanner at `0x34`.** Same part, same address, 46 keys instead of 56.
   → [`../cardputer-adv/features/keyboard.md`](../cardputer-adv/features/keyboard.md),
   [`texas-instruments/tca8418`](../../../components/texas-instruments/tca8418/README.md).
2. **The BMI270 IMU** — but at **`0x68`**, not the ADV's `0x69` (`SDO` strapped the other way),
   and here it carries a **BMM150 magnetometer on its auxiliary I²C interface**, which the ADV's
   BMI270 has pinned out but unpopulated.
3. **The EXT 2.54-14P connector**, with the same physical shape and the same
   `5VIN / GND / 5VOUT / I2C_SDA / I2C_SCL / UART` positions on the right column.

## ⚠ The EXT header is *not* pin-compatible with the ADV's

Same connector, different left column, and the UART pair is **swapped relative to the ADV's
product page**:

| Position | Cardputer ADV | CardputerZero |
|---|---|---|
| L1 | `RESET` G3 | **`HAT_P0`** — `USB4_D_P` **or** `GPIO26`, switchable |
| L2 | `INT` G4 | **`HAT_P1`** — `USB4_D_N` **or** `GPIO23` |
| L3 | `BUSY` G6 | `G22` |
| L4 | `SCK` G40 | `SPI0_CLK` G11 |
| L5 | `MOSI` G14 | `SPI0_MOSI` G10 |
| L6 | `MISO` G39 | `SPI0_MISO` G9 |
| L7 | `CS` G5 | `SPI0_CS1` G7 |
| R1–R3 | `5VIN`, `GND`, `5VOUT` | **same** |
| R4/R5 | `I2C_SDA` G8 / `I2C_SCL` G9 | `I2C1_SDA` G2 / `I2C1_SCL` G3 |
| R6 | **`UART_TX`** G13 | **`UART_RXD`** G15 |
| R7 | **`UART_RX`** G15 | **`UART_TXD`** G14 |

**A CAP board that uses only power + I²C has a chance of working on both. One that uses
`RESET`/`INT`/`BUSY` — i.e. the Cap LoRa-1262 and the Cap CC1101 — does not.** And the UART pair
is reversed, so even a serial-only board needs its TX/RX swapping.

The `HAT_P0`/`HAT_P1` pins are genuinely novel: `PYG1_HAT_SW` on the M5IOE1 switches them between
**GPIO** (default) and **USB Hub port 4**, so a CardputerZero HAT can be a USB device.
`PYG13_HAT_EN` gates the port's power.

## Architecture highlights

* **M5IOE1** (`0x4F`) — M5Stack's own I/O expander, already documented at
  [`components/m5stack/m5ioe1`](../../../components/m5stack/m5ioe1/README.md) from the PaperMono
  pass. Here it owns LCD reset and backlight PWM, the shared **keyboard + USB-hub reset**
  (`PYG3_KB_HUB_RST`), the CTIA/OMTP microphone switch (`PYG6_MIC_SW`), Grove 5 V enable, HAT
  enable and switching, power detect/enable, and three **CAPS/SHIFT/FN/SYM indicator LEDs** —
  something no ESP32 Cardputer has.
* **USB Host/Slave is a physical switch.** In Slave mode the hub is disconnected and the USB-A
  port, the left USB-C, the HAT USB pins and Ethernet all go away.
* **Headphone detect reaches a CPU GPIO** (`G17`) and the amplifier is enabled from `G24` — where
  the ADV does the same job entirely in hardware and software cannot see it.
* **RX8130CE RTC** — the ADV has no RTC at all. → [`components/seiko-epson`](../../../components/seiko-epson/) (part record not created by this pass).

## Software

`https://docs.m5stack.com/en/guide/linux/cardputerzero/image` (flashing) and `…/adb`
(ADB debugging); application template at `github.com/CardputerZero/Template`; SDK and kernel
pages both say *"coming soon…"*. M5Stack also maintains `m5stack/CardputerZeroRepository`.
Community index: `UnAneOnyme/CardputerZeroCollection` (CC0-1.0).

## Community

r/CardPuterZero exists as a separate subreddit. The Kickstarter announcement threads are among
the largest in the family: *"CARDPUTER ZERO 😱"* (r/CardPuter 2026-03-06, ↑698/105),
*"CardputerZero KickStarter !!!"* (2026-04-16, ↑283/**140 comments**), and an AMA
(2026-04-17, ↑151/114). *"Cardputer Zero is the same thickness as the ADV!"* (2026-05-05, ↑370).

The recurring confusion is exactly the one this record exists to clear up. u/G33K_FISH,
r/CardPuter 2026-05-31: *"FYI, the ADV and the Zero are different. The Zero will be linux based.
You can do things on the Zero you can not do on the ADV and vise versa."*
And a skeptical counterpoint from r/CardPuterZero (2026-07-16): *"Everyone is waiting for the
Cardputer Zero, but you know that your phone can do the same…"* (41 comments).

## Not researched in this pass

The schematic (`…/1243/C154-CardputerZERO_SCH_V0.6.1_20260702.pdf`), the sticker design files
(`…/1243/CardputerZero_Labels.zip`), the Linux image, the ADB guide and the application template
were all **identified and not fetched**. A device whose vendor says its features are subject to
change does not warrant a full-depth record yet. When it ships, the two things worth doing first
are parsing that schematic and diffing the EXT header against this table.

## Sources

`https://docs.m5stack.com/en/CardputerZero` (retrieved 2026-09-04, snapshot at
`artifacts/docs-en-CardputerZero.html`); Reddit threads cited inline.
Full table: [`../cardputer-adv/sources.md`](../cardputer-adv/sources.md).
