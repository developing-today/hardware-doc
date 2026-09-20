# M5Stack Cap LoRa868 / "LoRa+GPS Cap for Cardputer Adv" (SKU U201) — **[EOL]**

> **This is the answer to "what was the older LoRa extension for the Cardputer?"**
> — with the important correction that it is for the **Cardputer-Adv**, not the original
> Cardputer. It was published **2025-09-05, the same day as the Cardputer-Adv itself**, and
> is now discontinued, superseded by the [Cap LoRa-1262 (U214)](../cap-lora-1262/README.md)
> on 2025-12-30.
>
> Snapshot 2026-09-04. Medium-depth record: the vendor documentation was fully read, the
> **schematic was located but not fetched**.

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Documentation name | **Cap LoRa868** | `docs.m5stack.com/en/cap/Cap_LoRa868` |
| Store name | **[EOL] LoRa+GPS Cap for Cardputer Adv (SX1262, ATGM336H)** | Shopify JSON |
| SKU | **U201** | both |
| **Publish date** | **2025-09-05** — same day as **K132-ADV** (Cardputer Adv) | Shopify catalogue JSON |
| Price | **USD 14.50** (identical to its successor) | Shopify |
| Status | **[EOL]** | store title prefix |
| Hosts | Cardputer-Adv / CardputerZero | docs |
| CDN prefix | `1177` (vs `1208` for U214) | docs link set |

## 2. What it is

Architecturally the same idea as the U214: a 14-pin Cap carrying a `Stamp LoRa-1262`
(SX1262) plus an `ATGM336H-6N @ AT6668` GNSS with a ceramic antenna, on the Cap-Bus.

Vendor specification, where it differs from or adds to the successor:

| Item | Cap LoRa868 (U201) | Cap LoRa-1262 (U214) |
|---|---|---|
| LoRa module | **`Stamp LoRa-1262`** — "legacy version, **standard size**" | `Stamp LoRa-1262` **Mini** |
| **TX power** | **+20 dBm** | **+22 dBm** |
| RX sensitivity | −147 dBm | −147 dBm |
| Frequency | 868 – 923 MHz | 868 – 923 MHz |
| Shielding can | **No** | **Yes** |
| RF switch control | **None** | I/O expander `PI4IOE5V6408` P0 @ 0x43 |
| HY2.0-4P Grove | **No** | **Yes** |
| Weight | 30.0 g | 22.1 g |
| Size | 84.0 × 24.0 × 15.2 mm | identical |
| GNSS | `ATGM336H-6N @ AT6668`, UART 115200 8N1, 50 ch, <1.5 m CEP50, 10 Hz, NMEA 0183 4.1 | identical |
| Antenna | rubber duck 3 dBi, 108 × 9.3 mm | identical |

The comparison table is M5Stack's own, published on the U214 page.

## 3. ⭐ The state-resolved current figures — U201's documentation is *better* than U214's

This is the only place in the whole Cap family where M5Stack publishes current by named
operating state, and it is the most useful power data available for this hardware class:

| State | Current @ DC 5 V |
|---|---|
| GPS on, LoRa standby | **29.24 mA** |
| **GPS sleep, LoRa standby** | **3.16 mA** |
| GPS sleep, LoRa TX max power | **129.72 mA** |
| GPS on, LoRa TX max power | **155.03 mA** |

Read across: **the GNSS costs ~26 mA and dominates idle draw**; putting it to sleep is worth
almost an order of magnitude. Transmitting costs ~126 mA on top of whatever the GNSS is
doing. The successor page replaces all four numbers with a single unconditioned
*"Power Consumption (Power On): 33.1 mA"* and *"LoRa Operating Current: DC 5 V @ 163.4 mA"*.

⚠ These are **U201** figures at **+20 dBm**. Do not transplant them into a U214 table — the
successor transmits 2 dB harder and carries a shield can. The *shape* of the tradeoff
carries; the numbers do not.

## 4. Pin map — identical to the successor, minus the expander

| Cap pin | Net | Cardputer-Adv |
|---:|---|---|
| 1 | `GPS_TX` | **G15** |
| 2 | `GPS_RX` | **G13** |
| 3 | `SCL` | G9 |
| 4 | `SDA` | G8 |
| 5 | `5V_OUT` | — |
| 6 | `GND` | — |
| 7 | `5V_IN` | — |
| 8 | `LoRa_RST` | **G3** |
| 9 | `LoRa_IRQ` | **G4** |
| 10 | `LoRa_BUSY` | **G6** |
| 11 | `LoRa_SCK` | **G40** |
| 12 | `LoRa_MOSI` | **G14** |
| 13 | `LoRa_MISO` | **G39** |
| 14 | `LoRa_NSS` | **G5** |

**Pin-compatible with the U214.** The vendor pin map for U201 shows *only* the LoRa and GPS
blocks — no `PI4IOE5V6408` row and no `HY2.0-4P` row. That is the documented basis for
runtime Cap detection by probing I²C `0x43`
([`../cap-lora-1262/features/io-expander-and-rf-switch.md` §4](../cap-lora-1262/features/io-expander-and-rf-switch.md)).

## 5. ⚠ Conflict: does U201 have an expander after all?

Meshtastic's `variant.cpp` comment reads *"PI4IOE5V6408 on the optional Cap LoRa-1262
**(and Cap LoRa868)**"*, contradicting M5Stack's comparison table ("RF Switch Control:
None") and the U201 pin map. The code probes and tolerates absence, so nothing breaks
either way, but the claim is unresolved. **The U201 schematic is published and would settle
it; it was not fetched by this pass.**

## 6. Software

Same as the successor: **RadioLib** for the SX1262, **`m5stack/TinyGPSPlus`
(`MultipleSatellite`)** for the GNSS. M5Stack's Arduino guide is served at
`docs.m5stack.com/en/arduino/projects/cap/cap_lora868` and **covers both Caps**, detecting
which is present by probing `0x43`. That is why `/cap/cap_lora1262` is a 404: the older
board's slug is the canonical one.

Meshtastic runs on it — the variant's `initLoraCap()` degrades gracefully when the expander
is absent — but this configuration is not separately named or tested upstream.

## 7. Community: the first Cardputer LoRa wave

| Date | Event |
|---|---|
| **2025-09-04** | *"Cardputer adv and lora module info sheet"* (66 pts) — the day before launch, from `x.com/M5Stack/status/1963562345785098345`. In the comments: **"Can other versions of Cardputers make use of the Caplora?" → "No, not enough gpio pins."** |
| 2025-09-06 | *"CardPuter free text to New CardPuter ADV by Meshtastic?"* (91 pts, 16 comments) |
| **2025-09-15** | *"Got my Cardputer ADV and Lora Cap"* — **156 upvotes**, the arrival wave |
| **2025-09-19** | *"Cardputer adv up and running with Lora cap on US915"* — first documented US915 use. *"Had to wait a few extra days for some sma gender converters / adapters. I cannot for the life of me find an SMA female antenna for the US."* Includes a photo of a standard SMA antenna mating, and the owner's view that *"I think it is regular SMA female, I don't see any indications anywhere to RP-SMA"* |
| 2025-11-11 → 12-16 | MeshClient firmware for CardPuter & CardPuter ADV |
| **2025-12-30** | U214 launches. u/griffog: *"was there an issue with the original cap (the one I have) or does this just have the addition of the I2C port?"* → u/truthfly: *"Just a little upgrade, your is fine 👌"* |

Sources: [r/CardPuter 1n8d8j2](https://old.reddit.com/r/CardPuter/comments/1n8d8j2/),
[1nhr7na](https://old.reddit.com/r/CardPuter/comments/1nhr7na/),
[1nkyy4c](https://old.reddit.com/r/CardPuter/comments/1nkyy4c/),
[1pzazuu](https://old.reddit.com/r/CardPuter/comments/1pzazuu/). **[COM]**

## 8. Gaps

| # | Gap |
|---|---|
| L1 | **Schematic located but not fetched** (linked from the docs page as "Cap LoRa868 Schematics PDF"). Would settle §5, and would give the designator census |
| L2 | Model-size PDF not fetched |
| L3 | Whether "standard size" `Stamp LoRa-1262` is the *same* 13-pin module as the "Mini" or a physically different part is **not established**. The PaperMono uses a `Stamp-LoRa-1262-mini` — so "Mini" is not unique to the U214 |
| L4 | No certification identifier, same as the successor |
| L5 | No RF or power measurement by anyone (the vendor's four-state table is a claim, not a measurement) |

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| U-1 | Cap LoRa868 documentation | primary | `https://docs.m5stack.com/en/cap/Cap_LoRa868` | 2026-09-04 | Identity, +20 dBm, **four-state current table**, pin map, no Grove/no expander |
| U-2 | M5Stack catalogue JSON | primary | `https://shop.m5stack.com/collections/all/products.json` | 2026-09-04 | **U201 published 2025-09-05, USD 14.50, `[EOL]`** — and K132-ADV on the same date |
| U-3 | Cap LoRa-1262 documentation (comparison table) | primary | `https://docs.m5stack.com/en/cap/Cap_LoRa-1262` | 2026-09-04 | The five documented differences between U201 and U214 |
| U-4 | Arduino guide (serves both Caps) | primary | `https://docs.m5stack.com/en/arduino/projects/cap/cap_lora868` | 2026-09-04 | The `0x43` detection that distinguishes them |
| U-5 | Meshtastic `variant.cpp` | primary | `github.com/meshtastic/firmware` `src/platform/extra_variants/m5stack_cardputer_adv/variant.cpp` | 2026-09-04 | The contested "(and Cap LoRa868)" comment |
| U-6 | r/CardPuter threads (4) | community | see §7 | 2026-09-04 | Launch chronology, SMA/RP-SMA firsthand reports, the U201→U214 upgrade framing |

## 10. Related

[`../cap-lora-1262/README.md`](../cap-lora-1262/README.md) ·
[`../cardputer-mesh-kit/README.md`](../cardputer-mesh-kit/README.md) ·
[`components/m5stack/stamp-lora-1262`](../../../components/m5stack/stamp-lora-1262/README.md) ·
[`components/semtech/sx1262`](../../../components/semtech/sx1262/README.md)
