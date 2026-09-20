# RP-SMA vs SMA antenna connectors (and the `SMA-KE` designation)

- **Category:** generic **RF connector interface** — not a specific part number
- **Why this record exists:** M5Stack's LoRa and sub-GHz Caps carry a board-edge antenna
  connector that the vendor describes **inconsistently**, and owners repeatedly buy the
  wrong antenna or an unnecessary adapter as a result. This page states the physics, the
  evidence, and what is actually unresolved.
- **Retrieved:** 2026-09-04

## 1. The physics, in one table

The confusing part is that "male/female" and "pin/socket" are **decoupled** in reverse-polarity
variants. The *shell* determines male/female; the *centre contact* is what RP swaps.

| Connector | Shell | Centre contact | Typical role |
|---|---|---|---|
| **SMA male (plug)** | outer thread | **pin** | on a cable / antenna |
| **SMA female (jack)** | inner thread | **socket (hole)** | on a board |
| **RP-SMA male (plug)** | outer thread | **socket (hole)** | on a cable / antenna |
| **RP-SMA female (jack)** | inner thread | **pin** | on a board |

Rules of thumb that follow:

- **Inner thread + hole = standard SMA female.**
- **Inner thread + pin = RP-SMA female.**
- Wi-Fi gear is overwhelmingly RP-SMA (a historical regulatory artefact); LoRa and GNSS gear
  is more often standard SMA. Mixing the two ecosystems is where adapters get bought.

## 2. `SMA-KE` — the Chinese designation on M5Stack schematics

M5Stack's schematics label the board-side connector:

| Board | Designator | Schematic comment |
|---|---|---|
| [Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) | `E4` | **`SMA-KE`** |
| [Cap CC1101 (U219)](../../../devices/m5stack/cap-cc1101/README.md) | `E1` | **`SMA-TH_KH-SMA-KE-Z`** |

In Chinese connector nomenclature `K` (母 / *kǒng*-style suffixes) conventionally marks the
**jack** side and `E`/`Z` denote body style and mounting. **`SMA-KE` therefore reads as "SMA
jack", i.e. a *standard* SMA female — not RP-SMA.** That reading is `inferred` from
nomenclature convention, not from a connector datasheet, and it is exactly the sort of
inference that should be checked before being trusted.

## 3. The conflict, laid out

| Source | Says | Class |
|---|---|---|
| Cap LoRa-1262 docs, prose | *"equipped by default with an external **RP-SMA** antenna"* | primary |
| Cap LoRa-1262 docs, spec row | *"Interface Type **RP-SMA (internal thread, internal hole)**"* — **internally contradictory** (see §1: inner thread + hole = *standard* SMA) | primary |
| Cap LoRa-1262 **store** description | *"equipped by default with an external **SMA** antenna"* | primary |
| Cap LoRa-1262 / CC1101 schematics | `SMA-KE`, `SMA-TH_KH-SMA-KE-Z` | primary |
| Cap CC1101 docs, spec row | *"RP-SMA connector (internal thread, **female pin**)"* — **self-consistent as RP-SMA** | primary |
| Unit C6L store spec | *"SMA connector (**female thread, female pin**)"* — again describes RP-SMA female | primary |
| u/skinwill, 2025-12-30 | *"Looks like RP-SMA in the image."* | community, visual |
| u/jader242, 2025-12-30 | *"It's still rp."* | community, assertion |
| u/Big-Bunch2804, 2026-08-23 | *"Just so you know it's a rp-sma. They are a little specific."* | community, assertion |
| **u/malonestar, 2025-11-24, with photo** | *"I think it is regular SMA female, I don't see any indications anywhere to RP-SMA… **Worked for me with a SMA antenna**."* | community, **firsthand with evidence** — but about the **U201**, not U214 |

**Verdict: unresolved.** The strongest single piece of evidence is a photographed firsthand
mating with a standard SMA antenna, but it is on the predecessor board. The vendor
contradicts itself on the same page. Nobody has posted a close-up of the centre contact.

**Would settle it:** one photograph of the connector's centre contact, or an M5Stack part
number. Product photo `U214-Cap-LoRa-1262-main-pictures_02.webp` is held in the repository
and **has not been inspected** — that is the cheapest next step.

## 4. Practical guidance

- **Buy a four-way SMA/RP-SMA adapter pack before you need one.** That is what owners
  actually do; u/malonestar's link is to exactly such a pack.
- **The band matters more than the polarity.** Every LoRa Cap ships an **868 MHz** whip;
  North-American users on 915 MHz should plan on a second antenna
  ([r/CardPuter 2026-08-22](https://old.reddit.com/r/CardPuter/comments/1vvlcs9/): *"new
  antenna worked"*). The Cap CC1101, to M5Stack's credit, ships **three** whips.
- **Never power a transmitter with no antenna.** M5Stack's own warning on the Cap LoRa-1262
  page: *"Do not connect or power on the device without installing the antenna, otherwise
  the device hardware may be permanently damaged!"*

## 5. Used By

| Board | Designator | Bands | Antenna supplied |
|---|---|---|---|
| [Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) | `E4` `SMA-KE` | 868–923 MHz | 1 × 868 MHz, 3 dBi, 108 × 9.3 mm |
| [Cap LoRa868 (U201)](../../../devices/m5stack/cap-lora868/README.md) | not fetched | 868–923 MHz | 1 × 3 dBi, 108 × 9.3 mm |
| [Cap CC1101 (U219)](../../../devices/m5stack/cap-cc1101/README.md) | `E1` `SMA-TH_KH-SMA-KE-Z` | 315/433/868/915 MHz | **3** — 315, 433, 868 MHz |
| [Unit C6L (U202)](../../../devices/m5stack/unit-c6l/README.md) | — | 2.4 GHz + 868 MHz | 2 — Wi-Fi 84 mm, LoRa 108 mm |
| [Unit LoRa E220](../../../devices/m5stack/unit-lora-e220/README.md) | — | 433 or 920 MHz | 1 × 2.5 dBi, 110 mm, **SMA male** stated |
| [Unit LoRaWAN STM32WLE5](../../../devices/m5stack/unit-lorawan-stm32wle5/README.md) | — | per-SKU | 1 × 2.8 dBi, 195 mm, **SMA male** stated |
| [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) | — | 868–923 MHz | **none — built-in FPC antenna**, no connector |

Note the pattern: **Units state "SMA male" unambiguously; Caps do not.** The ambiguity is
specific to the Cap product line.

## 6. Sources

| ID | Title | Class | URL | Retrieved |
|---|---|---|---|---|
| R-1 | Cap LoRa-1262 documentation + store JSON | primary | `docs.m5stack.com/en/cap/Cap_LoRa-1262`, `shop.m5stack.com/products/cap-lora-1262-….json` | 2026-09-04 |
| R-2 | Cap CC1101 documentation | primary | `docs.m5stack.com/en/cap/Cap_CC1101` | 2026-09-04 |
| R-3 | Cap LoRa-1262 / Cap CC1101 schematics | primary | held under the device records | 2026-09-04 |
| R-4 | r/CardPuter "Cardputer adv up and running with Lora cap on US915" | community | `https://old.reddit.com/r/CardPuter/comments/1nkyy4c/` | 2026-09-04 |
| R-5 | r/M5Stack "New Arrival Alert! Cap LoRa 1262" | community | `https://old.reddit.com/r/M5Stack/comments/1pzazbe/` | 2026-09-04 |
| R-6 | r/CardPuter "cap lora issues" | community | `https://old.reddit.com/r/CardPuter/comments/1vvlcs9/` | 2026-09-04 |
