# Cardputer ADV — the CAP expansion header (host side)

> **Question answered:** *"What is the 14-pin header on the underside, what can I plug into it,
> and how do I design my own board for it?"*
> **This is the host-side document.** The two M5Stack CAP boards have their own records, owned
> by a different session: [`../../cap-lora-1262/`](../../cap-lora-1262/README.md) and
> [`../../cap-cc1101/`](../../cap-cc1101/README.md). Nothing here duplicates them.
> Applies to **Cardputer ADV only** — v1.0, v1.1 and the accessory kits have no such connector.
> Last verified **2026-09-04**.

## What it is

M5Stack calls it two things and the community a third:

| Name | Used by |
|---|---|
| **EXT 2.54-14P expansion bus** | the ADV and Mesh Kit product pages, spec tables |
| **Cap-Bus** | the Mesh Kit page's pin table for the *module* side |
| **CAP** | the product family name — `Cap LoRa-1262` (U214), `Cap CC1101` (U219), and the docs URL space `docs.m5stack.com/en/cap/…` |

It is a **2 × 7 through-hole/SMD header on 2.54 mm pitch**, schematic designator **P3**,
footprint **`HDR-SMD_14P-P2.54`**, on the underside of the device. A CAP board presents the
mating male header and is retained by two M2 × 4 mm screws.

It exists because the TCA8418 freed seven GPIOs. Every signal pin on this connector except the
two I²C lines is a pin that a v1.x Cardputer spends on its keyboard matrix.

## Pinout — by physical position

Use this table. It does not depend on whose numbering you adopt.

| Row L (top→bottom) | Signal | GPIO | Direction (host) | | Row R (top→bottom) | Signal | GPIO | Direction (host) |
|---|---|---|---|---|---|---|---|---|
| L1 | `RESET` | **G3** | out | | R1 | `5VIN` | — | power **in** |
| L2 | `INT` / `IRQ` | **G4** | in | | R2 | `GND` | — | — |
| L3 | `BUSY` | **G6** | in | | R3 | `5VOUT` | — | power **out** |
| L4 | `SCK` | **G40** | out | | R4 | `I2C_SDA` | **G8** | I/O |
| L5 | `MOSI` | **G14** | out | | R5 | `I2C_SCL` | **G9** | I/O |
| L6 | `MISO` | **G39** | in | | R6 | `UART_TX` | **G13** | **out** |
| L7 | `CS` | **G5** | out | | R7 | `UART_RX` | **G15** | **in** |

Source: sheet 4 of `Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf`, read from the rendered
sheet. The schematic symbol's own pin names are
`RESET, INT, BUSY, SCK, MOSI, MISO, CS` on the left and
`5VIN, GND, 5VOUT, SDA, SCL, GPS-RX, GPS-TX` on the right, against nets
`G3, G4, G6, G40, G14, G39, G5` and `+5VIN, GND, +5VOUT, G8, G9, G13, G15`.

## ⚠ Three numbering schemes describe this one connector

This is the single most likely way to get a CAP board wrong, so it gets its own table. All
three orderings agree on the *physical* signal order; only the numbers differ.

| Physical position | Product-page number (interleaved) | Host schematic number (P3) | Cap-board number (Cap-Bus) |
|---|---|---|---|
| L1 `RESET` G3 | **1** | **1** | **8** (`LoRa_RST`) |
| L2 `INT` G4 | 3 | 2 | 9 (`LoRa_IRQ`) |
| L3 `BUSY` G6 | 5 | 3 | 10 (`LoRa_BUSY`) |
| L4 `SCK` G40 | 7 | 4 | 11 (`LoRa_SCK`) |
| L5 `MOSI` G14 | 9 | 5 | 12 (`LoRa_MOSI`) |
| L6 `MISO` G39 | 11 | 6 | 13 (`LoRa_MISO`) |
| L7 `CS` G5 | 13 | 7 | 14 (`LoRa_NSS`) |
| R1 `5VIN` | 2 | 14 | 7 (`5V_IN`) |
| R2 `GND` | 4 | 13 | 6 |
| R3 `5VOUT` | 6 | 12 | 5 (`5V_OUT`) |
| R4 `SDA` G8 | 8 | 11 | 4 |
| R5 `SCL` G9 | 10 | 10 | 3 |
| R6 `UART_TX` G13 | 12 | 9 | 2 (`GPS_RX`) |
| R7 `UART_RX` G15 | 14 | 8 | 1 (`GPS_TX`) |

* The **product page** numbers 1,3,5,…,13 down the left and 2,4,6,…,14 down the right — the
  usual IDC convention.
* The **host schematic** numbers 1–7 down the left and 8–14 **up** the right.
* The **Cap board** uses the mirror image, because that is what a mating header does:
  Cap pin *n* ↔ host schematic pin ((n + 6) mod 14) + 1.

**Design rule:** work from the physical-position table and the signal names. Never transfer a
bare pin number between a host document and a module document.

## The UART direction, settled

`G13` is the **host's TX**, `G15` is the **host's RX**. M5Stack's Mesh Kit page says the
opposite in its EXT table and then contradicts itself in its Cap-Bus table. Four sources agree
against it, including M5Stack's own factory firmware:

```c
/* M5Cardputer-UserDemo @ b549eac0, main/hal/hal_config.h */
#define HAL_PIN_GPS_TX  GPIO_NUM_13
#define HAL_PIN_GPS_RX  GPIO_NUM_15
/* main/hal/cap_lora868/uart/uart_helper.c:71 */
uart_set_pin(ECHO_UART_PORT_NUM, HAL_PIN_GPS_TX /*tx*/, HAL_PIN_GPS_RX /*rx*/, …);
```

and Meshtastic's `variants/esp32s3/m5stack_cardputer_adv/variant.h`:
`#define GPS_RX_PIN 15` / `#define GPS_TX_PIN 13`.
Full evidence table in [`../pinouts-and-buses.md` §4](../pinouts-and-buses.md).

## Electrical specification

| Property | Value | Evidence |
|---|---|---|
| Logic level | **3.3 V** — all signal pins are ESP32-S3 GPIOs, no level shifting anywhere on the host | schematic; no translator in the ADV designator census |
| `5VIN` | accepts the host's `+5VIN` domain (USB VBUS, behind the Stamp's 6 V/1 A PPTC) | Stamp-S3A sheet, F1 |
| `5VOUT` | the **SY7088** boost output, nominal **≈ 5.29 V [inferred]** from FB 75 k/22 k and the sheet's own `Vout = 1.2 V × (R1/R2 + 1)` | schematic sheet 1 |
| `5VOUT` current budget | **not published.** The SY7088 is a 2 A-class boost, but the shared Grove `+5V` and the whole 3.3 V rail come from it too. The CardputerZero's equivalent port is documented at **< 500 mA**; the ADV publishes no figure. Do not assume more than a few hundred mA. | gap |
| I²C pull-ups | **already fitted on the host** — R36/R37, 3.3 kΩ each. **Do not add more on a CAP board** unless you intend the parallel value. | schematic sheet 2 |
| I²C addresses in use | `0x18` ES8311, `0x34` TCA8418, `0x69` BMI270 — **avoid these** | see [`../pinouts-and-buses.md`](../pinouts-and-buses.md) |
| SPI | shared with the microSD card (CS G12). Your CS is **G5**. | see below |
| `RESET` (G3) | **also an ESP32-S3 JTAG-source strap pin.** Leave it high-Z or high at reset. | ESP32-S3 strapping |
| ESD | the host fits `PESDNC2FD3V3B` / `PESDNC2FD5VB` arrays elsewhere; **no ESD protection was identified on P3 itself** | designator census, sheet 4 |

## ⚠ The SPI bus is shared with the microSD card

`SCK` G40, `MOSI` G14, `MISO` G39 are the same three pins the microSD uses. Only the chip
selects differ (SD = G12, CAP = G5).

Consequences you must design for:

1. **Deassert one CS before asserting the other.** Neither is done for you.
2. **Clock rate is set by the slowest participant.** SD cards tolerate 20–40 MHz; an SX1262 is
   specified to 16 MHz. If you share a bus handle, run at the transceiver's limit.
3. **Long SD transactions add jitter to radio timing.** A LoRa receive window that opens while
   a 512-byte SD block is in flight will be late. Meshtastic and the M5 factory firmware both
   live with this; it is the main reason "SD logging + LoRa" projects report intermittent
   missed packets.
4. If you use two separate `SPIClass` instances on the same pins, you must serialise them
   yourself — the ESP32-S3 SPI peripheral will not.

Realistic combinations are tabulated in
[`../resources-and-conflicts.md`](../resources-and-conflicts.md).

## What plugs in today

| Board | SKU | Released | What it adds | Record |
|---|---|---|---|---|
| **Cap LoRa-1262** | U214 | **2026-01-04** | SX1262 868–923 MHz, RP-SMA, ATGM336H/AT6668 GNSS, PI4IOE5V6408 expander, FM8625H RF switch, HY2.0-4P | [`../../cap-lora-1262/`](../../cap-lora-1262/README.md) |
| **Cap CC1101 & NFC** | U219 | **2026-08-28** | CC1101 sub-GHz + NFC | [`../../cap-cc1101/`](../../cap-cc1101/README.md) |

Community CAP boards found on 2026-09-04 (not verified by this session):
`Prokuon/CardputerADV_Cap_TFT-2.8` and `CardputerADV_Cap_TFT_V2` (secondary displays — the
Reddit announcement reached ↑989), `JosephCGS/Cardputer-ADV-CC1101-NRF24L01-LoRa`,
`guicmg/cardputer_adv_external_screen`, and the `AndyAiCardputer` ZX Spectrum ports that drive
ILI9341/ILI9488 panels off the header.

### How the host talks to the Cap LoRa-1262

Host-side pin assignment as used by all three implementations:

| Function | GPIO | M5 UserDemo | Meshtastic |
|---|---|---|---|
| `NSS`/CS | G5 | `HAL_PIN_LORA_NSS_GPIO 5` | `LORA_CS 5` |
| `RESET` | G3 | `HAL_PIN_LORA_RST_GPIO 3` | `LORA_RESET 3` |
| `DIO1`/IRQ | G4 | `HAL_PIN_LORA_DIO1_GPIO 4` | `LORA_DIO1 4` |
| `BUSY` | G6 | `HAL_PIN_LORA_BUSY_GPIO 6` | `SX126X_BUSY` ← `LORA_DIO2 6` |
| SPI | G40/G14/G39 | `HAL_PIN_SPI_*` | `LORA_SCK/MISO/MOSI` |
| GNSS UART | G13 TX / G15 RX @115200 8N1 | `HAL_PIN_GPS_*` | `GPS_RX_PIN 15`, `GPS_TX_PIN 13` |

Meshtastic additionally declares `SX126X_DIO2_AS_RF_SWITCH` and
`SX126X_DIO3_TCXO_VOLTAGE 1.8` with `TCXO_OPTIONAL`.

**One extra step the header does not tell you:** the Cap LoRa-1262's RF antenna switch is not
free-running. M5Stack's Mesh Kit page states plainly:

> "The following steps are required to initialize the LoRa module: Enable the RF antenna
> switch: set **P0 of the PI4IOE I/O expander to HIGH**."

That expander lives on the **CAP I²C pins (G8/G9)** — i.e. on the host's *internal* bus,
alongside the keyboard scanner. Omit it and the radio transmits into a disconnected antenna.
Detail belongs to the Cap board's record.

## Designing your own CAP board — checklist

1. **Mechanical:** 84.0 × 24.0 × 15.2 mm is the Cap LoRa-1262's envelope; two M2 × 4 mm screws.
2. **Numbering:** use the physical-position table above; label your silkscreen with *signal
   names*, not numbers.
3. **Power:** take `5VIN` if you want to be fed from USB, `5VOUT` if from the boost. Budget
   conservatively; no host figure is published.
4. **I²C:** no pull-ups. Avoid `0x18`, `0x34`, `0x69`. Expect the keyboard scanner to be
   sharing your bus and to want low latency.
5. **SPI:** your CS is G5 only. Arbitrate against the microSD yourself.
6. **`RESET` on G3 is a strap pin** — do not drive it low during host reset.
7. **ESD:** add your own on any user-touchable pin; the host does not appear to protect P3.
8. **UART:** host TX is G13, host RX is G15. Cross them on your board.
9. **Detection:** there is **no ID pin, no EEPROM, no presence detect.** Firmware discovers a
   CAP board by probing — Meshtastic probes the SX1262 over SPI, the Plai client is reported by
   a user to "automatically detect the lora cap and switch configurations" (u/Big-Bunch2804,
   r/CardPuter, 2026-08-05). If you want your board discoverable, put something on I²C.

## Is it ADV-only?

**Yes, on the Cardputer line.** The v1.0/v1.1 mainboard has no such connector and, more
fundamentally, no free pins to build one from — G3–G7, G13 and G15 are the keyboard.

But the *connector* is not ADV-exclusive within M5Stack: the **CardputerZero (C154)** carries
an `EXT 2.54-14P` with the same physical shape and the same 5VIN/GND/5VOUT/I2C/UART positions,
while the left column becomes `HAT_P0/HAT_P1` (switchable USB or GPIO), `G22`, and SPI0. A CAP
board that only uses power + I²C + UART has a chance of working on both; one that uses
`RESET`/`INT`/`BUSY` does not, and the Zero's UART sits on the *opposite* member of the R6/R7
pair. See [`../../cardputer-zero/README.md`](../../cardputer-zero/README.md).

## Evidence status

| Claim | Status |
|---|---|
| Physical pinout, net names, GPIO assignment | **official** — rendered vendor schematic sheet 4 |
| UART direction | **official** ×4, one vendor page dissenting; resolved |
| SPI sharing with microSD | **official** — same nets in `_pin_table_sd` and on sheet 4 |
| I²C pull-up values | **official** — schematic sheet 2 |
| `5VOUT` ≈ 5.29 V | **inferred** from FB resistors + the formula printed on the sheet. Not measured. |
| `5VOUT` current limit | **unknown** — no vendor figure |
| No ESD on P3 | **inferred** from a designator census of sheet 4; absence of evidence, stated as such |
| Community CAP boards | **community**, catalogued not verified |
