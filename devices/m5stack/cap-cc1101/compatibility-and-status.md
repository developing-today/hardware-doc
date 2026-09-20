# Compatibility and status — Cap CC1101 & NFC (U219)

**Released 2026-08-28; this snapshot is 2026-09-04.** There is almost no field evidence yet,
and the honest state of this page is *"documented, unproven"*. Nothing was tested here.

## 1. Hosts

| Host | Fits? | Evidence |
|---|---|---|
| **Cardputer-Adv** | ✅ | vendor **[DOC]**; schematic annotates every Cap-Bus pin with its ADV GPIO |
| **CardputerZero** | ✅, **with a pin change** — `RF_SW0` moves from **G13** to **G14** | vendor **[DOC]**; **[COM]** M5Stack community post, [2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/) |
| **Cardputer P4 ("Next")** | claimed; **product unreleased** | **[COM]** same post |
| **Original Cardputer (K132)** | ❌ | no expansion bus |

**The CardputerZero pin difference is important and under-documented.** A firmware that
hard-codes `RF_SW0 = 13` will silently select the wrong band on a Zero. No vendor code
handles this; the only statement of it is a Reddit comment by M5Stack's community manager.

## 2. Firmware

| Firmware | CC1101 | NFC | Status |
|---|---|---|---|
| **M5Stack Arduino examples** | ✅ | ✅ | Published with the product. `not-tested` here |
| **M5Stack UiFlow2 / MicroPython** | ✅ | ✅ | Vendor page exists (zh-cn path) |
| **`m5stack/M5Unit-NFC` 0.1.0** | — | ✅ | `CapCC1101NFC` present since 2026-06-10, **before** release |
| **RadioLib** | ✅ | — | CC1101 fully supported upstream; band switching is application code |
| **Bruce** | ❌ **not yet** | ❌ | Community expectation is that Bruce will add it; band switching needs implementing |
| **Meshtastic** | ❌ n/a | ❌ n/a | Wrong radio class entirely |

## 3. Field evidence

| Date | Report | Class |
|---|---|---|
| 2026-08-28 | Release announcement thread, 41 upvotes / 16 comments. Several *"Ordered!"*; **no owner has posted a working result yet** | community, ordering intent only |
| 2026-08-28 | *"I have mine ordered with the Zero"* — u/Zatoichi80 | firsthand purchase, no result |
| 2026-08-28 | Correct technical answers on why CC1101 ≠ LoRa | informed interpretation |
| 2025-09-08 | Pre-announcement: M5Stack told an owner "December or January". Slipped ~8 months | firsthand quote of vendor email |

**Nothing in the sample is a firsthand use report of this board.** Anyone reading this
record after ~2026-10 should re-search; the evidence base will have changed.

## 4. Untested / unknown

Everything measurable: output power, sensitivity, per-band insertion loss, inter-band
isolation, NFC read range, tag compatibility, card-emulation behaviour, the two chips
sharing one SPI bus in different modes, the `POWER_EN` polarity, and the 140.87 µA sleep
figure.
