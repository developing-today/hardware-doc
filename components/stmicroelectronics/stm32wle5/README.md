# STMicroelectronics STM32WLE5

- **Category:** **system-on-chip combining an Arm Cortex-M4 with a Semtech sub-GHz radio
  IP core** — i.e. an MCU and a LoRa transceiver on one die
- **Research status:** light. No ST datasheet retrieved; identity and integration are from
  M5Stack product documentation.
- **Retrieved:** 2026-09-04

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | STMicroelectronics | — |
| Family | **STM32WL** — the first general-purpose MCU with an integrated LoRa-capable radio | — |
| Part as cited by M5Stack | **`STM32WLE5`** — *"@256 KB Flash, 64 KB RAM"* | Unit LoRaWAN-EU868 specification table |
| Variant on the DTU products | `STM32WLE5CC` | Atomic DTU LoRaWAN Base store listings |
| Radio | Semtech sub-GHz IP, LoRa + (G)FSK; the SX126x family lineage | — |
| Why it exists | ST is one of the small number of licensees of Semtech's LoRa PHY | see [`components/texas-instruments/cc1101` §5](../../texas-instruments/cc1101/README.md) for the contrast |

## 2. How M5Stack uses it — as a *modem*, not as an MCU

Every M5Stack STM32WLE5 product presents the chip as a **UART AT-command LoRaWAN modem**, not
as a programmable Cortex-M4. The host talks AT; the STM32WLE5 runs a stack the host never
sees. On the Unit LoRaWAN-EU868 the module is identified in the documentation's
Certifications section as a **RAK3172** — RAKwireless's STM32WLE5 module with RUI3 firmware,
which is exactly that architecture.

| Item | Value |
|---|---|
| Protocol | **LoRaWAN 1.0.3**, **Class A / B / C**; plus LoRa **P2P** |
| Activation | **OTAA, ABP** |
| Interface | **UART, 115200 default, AT commands**, Grove **PORT.C** (yellow `UART_RX`, white `UART_TX`) |
| RX sensitivity | **−137 dBm** |
| TX power | max **22 dBm** |
| Sleep current | **28.61 µA @ 5 V** (board level) |
| TX current @ 125 kbps | **117.16 mA @ 5 V** (board level) |

**Consequence:** you get a certified regional LoRaWAN stack and give up radio control. That
is the opposite trade from the Caps, which give you a raw SX1262 and no certification.

## 3. Region is the SKU — and that is the right way round

| SKU | Band |
|---|---|
| U184-EU868 | EU868 (863–870 MHz) |
| U184-US915 | US915 |
| U184-AS923 | AS923 |
| U184-CN470 | CN470 |
| A152-EU868 / US915 / CN470 | Atomic DTU LoRaWAN Base, `STM32WLE5CC` |

Compare with the Cardputer Caps: **one wideband 868–923 MHz SKU, no regional variant, no
published certification.** If a project needs a LoRa link it can lawfully deploy rather than
bench-test, this is the product family that has the paperwork.

## 4. Predecessor silicon in the same M5Stack role

M5Stack's own comparison table on the Unit LoRaWAN-EU868 page:

| | STM32WLE5 (U184, 2024-12-20) | **ASR6501** (U115/U116/U117, 2021-05-14, all `[EOL]`) |
|---|---|---|
| LoRaWAN | 1.0.3, Class A/B/C | 1.0.1, Class A/C |
| TX power | 22 dBm | 21 dBm |
| Sensitivity | −137 dBm | −137 dBm |
| Interface | UART 115200 | UART 115200 |

The ASR6501 generation is the **oldest** LoRa hardware in M5Stack's catalogue that this pass
enumerated, predating the Cardputer by two and a half years.

## 5. Used By

### [M5Stack LoRaWAN Unit (U184-\*)](../../../devices/m5stack/unit-lorawan-stm32wle5/README.md)

Grove/UART, region-per-SKU, RAK3172 module. **Attachable to any M5Stack host with a Grove
port, including the original Cardputer** — but it is a LoRaWAN modem, so it is not a
Meshtastic path and not a raw-LoRa path.

### Atomic DTU LoRaWAN Base (A152-\*) — **no record in this repository**

`STM32WLE5CC`, USD 22.90, published 2025-04-18. ATOM-form DTU, not Cardputer-attachable.

### M5Stack LoRaWAN EU868 Module (M148) — **no record**

USD 24.90, published 2026-04-24. Core-bus module.

## 6. Gaps

- **No ST datasheet or reference manual retrieved.** Nothing here is register-level.
- The **RAK3172 certification page** — the only regulatory pointer in M5Stack's LoRa line
  besides the E220-JP's Telec number — was **not fetched**.
- Only the EU868 documentation page was read.
- Whether the STM32WLE5 in these products can be reflashed with custom firmware (it is, after
  all, a Cortex-M4) was **not investigated**. If it can, these units become far more
  interesting than an AT modem.

## 7. Related

- [`components/semtech/sx1262`](../../semtech/sx1262/README.md) — the discrete equivalent radio
- [`components/ebyte/e220-400t22s`](../../ebyte/e220-400t22s/README.md) — the other "UART LoRa modem" architecture in this repository
- [`components/stmicroelectronics/st25r3916`](../st25r3916/README.md) — unrelated, same manufacturer

## 8. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| ST-1 | Unit LoRaWAN-EU868 documentation | primary | `https://docs.m5stack.com/en/unit/Unit%20LoRaWAN-EU868` | 2026-09-04 | `STM32WLE5 @256 KB Flash, 64 KB RAM`, LoRaWAN 1.0.3 Class A/B/C, AT/UART, RAK3172 certification link, the ASR6501 comparison, state-resolved current |
| ST-2 | M5Stack catalogue JSON | primary | `https://shop.m5stack.com/collections/all/products.json` | 2026-09-04 | The four U184 SKUs, three A152 SKUs, M148, and the `[EOL]` ASR6501 generation with dates |
