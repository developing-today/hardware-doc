# M5Stack Cardputer Mesh Kit (K152)

> **SKU `K152`** · product id **`1240`** · Shopify `9135211610369`
> Released **2026-04-30** · **$48.00**, in stock 2026-09-04
> An **officially licensed Meshtastic device**. Research snapshot **2026-09-04**.

A bundle, not a new board: a **Cardputer ADV in a green back shell** plus a **Cap LoRa-1262**,
an antenna and hardware, pre-flashed with Meshtastic and — uniquely — **eligible for Meshtastic
device registration**.

| Component | Record |
|---|---|
| Cardputer ADV (host) | [`../cardputer-adv/`](../cardputer-adv/README.md) — **full depth** |
| Cap LoRa-1262 (module) | [`../cap-lora-1262/`](../cap-lora-1262/README.md) — *owned by a different session* |
| The host-side CAP interface | [`../cardputer-adv/features/cap-header.md`](../cardputer-adv/features/cap-header.md) |

## Contents

* 1 × Cardputer-Adv (**Green Back Shell Version** — the only place this colourway is sold)
* 1 × Cap LoRa-1262
* 1 × LoRa rubber-duck antenna, **RP-SMA**, 108 × 9.3 mm, 3 dBi
* 2 × M2 × 4 mm cap-head machine screws
* 1 × 1.5 mm hex key
* 1 × safety-warning sticker

**Bundle arithmetic:** ADV $29.90 + Cap LoRa-1262 $14.50 = $44.40 versus **$48.00**. The $3.60
premium buys the antenna, the fasteners, the green shell — and the registration entitlement.

## ⚠ Meshtastic registration is restricted to the kit

M5Stack states it plainly:

> "Only devices in the Cardputer Mesh Kit set can be registered. Other Cardputer/-Adv devices
> are **not eligible** for Meshtastic authorization registration."

Registration flow: flash Meshtastic (pre-flashed at the factory) → attach the Cap →
USB-C to a computer → `https://meshtastic-reg.m5stack.com/` → *Connect Device* → select port →
*Connect*. After success the Meshtastic app shows the device model and an authorisation mark.

**Practical consequence:** an ADV plus a separately bought Cap LoRa-1262 runs identical firmware
and joins the same mesh, but cannot claim the licensed-device badge. If that matters, buy the
kit; if it does not, buy the parts and save $3.60.

## Specifications beyond the ADV

Host specs are the ADV's. The kit adds:

| Item | Value |
|---|---|
| LoRa transceiver | **SX1262** |
| Frequency | 868 – 923 MHz |
| Programmable bit rate | up to 300 kbps |
| TX power | **+22 dBm** |
| RX sensitivity | **−147 dBm** (low data rate) |
| Modulations | FSK / GFSK / MSK / LoRa / OOK |
| LoRa operating current | DC 5 V @ 163.4 mA |
| Antenna | RP-SMA (female), 108 × 9.3 mm, 3 dBi |
| GNSS module | **ATGM336H-6N @ AT6668** |
| GNSS interface | UART, **115200 8N1** |
| Constellations | GPS / QZSS / BD2 / BD3 / GAL / GLO, 50 channels |
| GNSS accuracy | < 1.5 m CEP50, up to 10 Hz |
| TTFF | cold 23 s, hot 1 s |
| Cap size / kit weight | 84.0 × 24.0 × 15.2 mm; 77.2 g product, 127.2 g gross |

Component records: [`semtech/sx1262`](../../../components/semtech/sx1262/README.md) (existing);
the ATGM336H, PI4IOE5V6408 and FM8625H belong to the
[Cap LoRa-1262 record](../cap-lora-1262/README.md).

## Assembly

1. Turn the Cardputer-Adv over and locate the **EXT 2.54-14P** female header.
2. Align the Cap's male header and press until seated.
3. Screw the antenna into the RP-SMA connector.

⚠ **Never transmit without the antenna fitted.** The kit ships a safety sticker for this reason.

## Host-side pin usage

The Cap consumes **every** CAP signal pin:

| Cap function | Host GPIO | Host role |
|---|---|---|
| LoRa `NSS` | **G5** | SPI CS |
| LoRa `RST` | **G3** | out |
| LoRa `IRQ`/`DIO1` | **G4** | in |
| LoRa `BUSY` | **G6** | in |
| LoRa SPI | G40 / G14 / G39 | **shared with the microSD card** |
| GNSS → host | **G15** | host **RX** |
| host → GNSS | **G13** | host **TX** |
| I²C (PI4IOE5V6408, HY2.0-4P) | G8 / G9 | **the host's internal bus** — shares with TCA8418 `0x34`, ES8311 `0x18`, BMI270 `0x69` |

With a Cap fitted the ADV has **no free GPIO left** apart from the Grove port.

**The step people miss:** M5Stack states that initialising the radio requires *"Enable the RF
antenna switch: set **P0 of the PI4IOE I/O expander to HIGH**"*. That expander is on the host's
internal I²C bus. Omit it and the SX1262 transmits into a disconnected antenna.

## ⚠ A documentation defect on this product's page

The Mesh Kit page's **"Cardputer-Adv EXT 2.54-14P"** table gives pin 12 = `G13` = `UART_RX` and
pin 14 = `G15` = `UART_TX`. That is **wrong**, and the same page contradicts it two tables later
where the Cap-Bus table maps `G13 → GPS-RX`. Four sources agree that **G13 is the host's TX and
G15 its RX**: the ADV product page, the ADV schematic's symbol pin names, M5Stack's own factory
firmware `uart_set_pin(port, GPIO_NUM_13 /*tx*/, GPIO_NUM_15 /*rx*/)`, and Meshtastic's
`variant.h`. Full evidence:
[`../cardputer-adv/pinouts-and-buses.md` §4](../cardputer-adv/pinouts-and-buses.md).

## Firmware

| Route | Notes |
|---|---|
| **Meshtastic upstream** | env `m5stack-cardputer-adv`, `board = m5stack-stamps3`, `default_8MB.csv`. HEAD `be2f68b5` (2026-09-03). **This is what ships.** |
| M5Stack factory `CardputerADV` branch | includes `main/hal/cap_lora868/` — SX1262 via a vendored RadioLib HAL, `TinyGPSPlus`, and `app_lora_chat` |
| `d4rkmen/plai` | ADV-only Meshtastic client. A user reports it *"automatically detected the lora cap and switched configurations"* (r/CardPuter, 2026-08-05) |
| MeshCore ports ×3 | `Stachugit`, `sosprz`, `MultiMote` — a different mesh protocol on the same hardware |
| `ratspeak/rsCardputer` | Reticulum / LXMF |

Tutorial: `https://docs.m5stack.com/en/guide/lora/meshtastic/cardputer_mesh_kit`
(recorded, **not fetched** in this pass).

## Where it fits

Before the kit existed, an r/meshtastic thread of **2026-03-11** asked *"Any reason not to just
get a Cardputer with lora cap for 55 bucks total even after ship?"* (19 comments). The kit is
M5Stack's answer: the same idea, cheaper, in one box, with a licence.

Against a dedicated Meshtastic node it wins on **input** — a keyboard means composing messages
without a phone, which is the whole pitch of the ADV-native clients. It loses on battery life
and ruggedness. Against a LilyGO T-Deck it has a better keyboard and no PSRAM; see
[`../cardputer-adv/comparisons-and-recommendations.md`](../cardputer-adv/comparisons-and-recommendations.md).

## Sources

Product page `https://docs.m5stack.com/en/core/Cardputer_Mesh_Kit` (retrieved 2026-09-04,
snapshot at `artifacts/docs-en-core-Cardputer_Mesh_Kit.html`); `/en/history` for the
2026-04-30 release date; Shopify `<handle>.json`; Meshtastic `variant.h` @ `be2f68b5`.
Full table: [`../cardputer-adv/sources.md`](../cardputer-adv/sources.md).
