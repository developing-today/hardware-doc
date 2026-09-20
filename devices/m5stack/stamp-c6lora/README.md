# M5Stack Stamp C6LoRa (SKU S012)

> **Light record.** Included because the task brief listed it as a candidate for "the older
> Cardputer LoRa extension" — and the answer is **no: it is a solder-down SMD module, not an
> expansion board, and it does not attach to any Cardputer.** It matters here for a
> different reason: it is the third M5Stack product to use a **PI4IOE5V6408** to control an
> **SX1262** antenna switch, which makes that pattern a house style rather than a one-off.
>
> Published **2026-03-13**, USD **12.95**. Snapshot 2026-09-04.

## 1. Identity

| Property | Value |
|---|---|
| SKU | **S012** |
| Store title | *M5Stamp C6LoRa Module (ESP32-C6, SX1262)* |
| **Published** | **2026-03-13** |
| Price | USD **12.95** |
| Docs | `https://docs.m5stack.com/en/core/Stamp_C6LoRa` |
| Form factor | **SMD surface-mount module**, 18.0 × 15.0 × 2.3 mm, **1.7 g** |
| SoC | ESP32-C6 — RISC-V 160 MHz HP + 20 MHz LP, **16 MB flash**, **Wi-Fi 6** |
| LoRa | **SX1262**, **850 – 960 MHz**, **+22 dBm**, **−148 dBm** |
| **LNA** | **SGM13005L4** — a receive low-noise amplifier |
| **I/O expander** | **PI4IOE5V6408** — *"to control the LoRa module's transceiver circuit and signal amplifier enable function"*, exposing **EXT_P0 … P4** |
| Antenna | **two IPEX-4** connectors (Wi-Fi + LoRa) |
| GPIO brought out | **16** — G9/G11/G8/G10/G2/G7/G4/G5/G6/G15/G16/G17/G18/G20/G21/G22 — plus 5 expander pins |
| Power | DC 3.7–5 V on `BAT`, or DC 3.3 V on `VDD_3V3` |
| Schematic | `S012-SCH_Sch_M5_C6_Lora_v0.2.3_2025_12_02…pdf` — **v0.2.3, 2025-12-02**, 3 sheets, held in [`artifacts/`](artifacts/) |
| Toolchain | `pioarduino/platform-espressif32` pinned **`#55.03.37`** in the vendor docs |
| KiCad footprint | `M5_Hardware/KiCad/Footprints/M5Stack.pretty/Stamp_C6LoRa_SMD.kicad_mod` |

## 2. ❌ Not a Cardputer expansion

It is an SMD module intended to be reflowed onto a carrier PCB. It has no Cap-Bus
connector, no Grove connector and no enclosure. Where it *does* appear in Cardputer-adjacent
territory is inside the **[Unit C6L (U202)](../unit-c6l/README.md)**, which is Grove-cabled
and therefore usable alongside any Cardputer.

## 3. Why it is worth a record anyway — the PI4IOE5V6408 pattern

Three M5Stack products now put an **I²C I/O expander in charge of an SX1262's RF switch**:

| Product | Expander | What it controls |
|---|---|---|
| [Cap LoRa-1262 (U214)](../cap-lora-1262/README.md) | `PI4IOE5V6408` @ 0x43 | **P0** → module pin 10 `SW` |
| **Stamp C6LoRa (S012)** | `PI4IOE5V6408` | transceiver switch **and LNA enable**, EXT_P0–P4 exposed |
| [M5Stack PaperMono](../papermono/README.md) | `M5IOE1` (different part) | `SX_ANT_SW` on IO2, `SX_NRST` on IO10 |

The recurring design idea: **do not spend host GPIO on RF-path control; put it behind I²C.**
The recurring consequence: **no I²C, no radio** — an I²C fault takes the RF path down even
though SPI is fine. Anyone porting M5Stack LoRa hardware should expect this and look for the
expander before concluding a radio is dead.

Stamp C6LoRa goes further than the Cap by putting the **LNA enable** on the expander too,
which is a real power-management win (an always-on LNA is exactly what the Cap LoRa-1262
pays for on its GNSS front end — see
[`../cap-lora-1262/features/gnss.md` §4](../cap-lora-1262/features/gnss.md)).

## 4. Meshtastic

**No `stamp_c6lora` variant exists upstream.** The relevant variant is
`variants/esp32c6/m5stack_unitc6l/` — i.e. Meshtastic supports the *product built around*
this module, not the module itself. `executed-success` on the negative, from the full
recursive tree listing, 2026-09-04.

## 5. Local artifacts

| File | Bytes | SHA-256 | Source |
|---|---:|---|---|
| [`artifacts/S012-Stamp_C6LoRa_SCH_v0.2.3.pdf`](artifacts/S012-Stamp_C6LoRa_SCH_v0.2.3.pdf) | 489 288 | `2dafe92c5090a01aa948c1ce88b17d1237421d09701c1e0a15a122bd9d844d35` | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1223/S012-SCH_Sch_M5_C6_Lora_v0.2.3_2025_12_02_19_14_35.pdf`, retrieved 2026-09-04 |

**The schematic was downloaded and bbox-extracted (3 sheets, 508/963/178 words) but not
decoded** — that was out of scope for this pass. It is here so the next agent does not have
to re-fetch it. Extraction command in
[`../cap-lora-1262/commands.md`](../cap-lora-1262/commands.md).

## 6. Related

[`../unit-c6l/README.md`](../unit-c6l/README.md) ·
[`components/semtech/sx1262`](../../../components/semtech/sx1262/README.md) ·
[`components/diodes-incorporated/pi4ioe5v6408`](../../../components/diodes-incorporated/pi4ioe5v6408/README.md)

## 7. Sources

| ID | Title | Class | URL | Retrieved |
|---|---|---|---|---|
| S-1 | Stamp C6LoRa documentation | primary | `https://docs.m5stack.com/en/core/Stamp_C6LoRa` | 2026-09-04 |
| S-2 | S012 store listing JSON | primary | `https://shop.m5stack.com/products/m5stamp-c6lora-module-esp32-c6-sx1262.json` | 2026-09-04 |
| S-3 | Schematic v0.2.3 | primary | see §5 | 2026-09-04 |
| S-4 | Meshtastic variant tree | primary | `api.github.com/repos/meshtastic/firmware/git/trees/master?recursive=1` | 2026-09-04 (negative result) |
