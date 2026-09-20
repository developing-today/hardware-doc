# M5Stack Cap CC1101 & NFC (SKU U219)

> **What it is:** a 14-pin expansion board ("Cap") for the **Cardputer-Adv** and
> **CardputerZero** combining a **TI CC1101** multi-band sub-GHz transceiver
> (315 / 433 / 868 / 915 MHz, switched by **two Infineon BGS13SN8 SP3T switches**) with an
> **ST ST25R3916** NFC front end (reader/writer *and* card emulation), on a **shared SPI
> bus**, behind a **host-gated** power rail, plus a Grove pass-through.
>
> **This is the newest board in the family: store publish date 2026-08-28**, seven days
> before this snapshot. **Schematic revision documented: V0.3, dated 2026-05-28.**
> Nothing tested on hardware.

> **Why this record matters beyond the Cardputer:** it is the cleanest published example of
> "NFC + sub-GHz on one SPI bus with a shared antenna", which is exactly the shape of the
> wider project's goal of adding NFC and LoRa capability to e-ink reader firmware. The
> portability material is in [`features/nfc.md` §10](features/nfc.md) and
> [`features/sub-ghz.md` §9](features/sub-ghz.md).

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[SCH]** | `U219-Cap_CC1101_SCH_V0.3_20260528.pdf`, 3 sheets, in [`artifacts/schematic/`](artifacts/schematic/) — text-layer extraction, `executed-success`; not rendered |
| **[DOC]** | `docs.m5stack.com/en/cap/Cap_CC1101` and the Arduino guide, retrieved 2026-09-04 |
| **[SHOP]** | `shop.m5stack.com/products/cap-cc1101-nfc-for-cardputer.json`, 2026-09-04 |
| **[SRC]** | Source read at a cited path/commit |
| **[COM]** | Community report, cited by permalink and date |
| **[INF]** | Inference |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marketed name | **Cap CC1101** (store title: *Cap CC1101 & NFC for Cardputer Adv*) | **[DOC]**, **[SHOP]** |
| SKU | **U219** | **[DOC]**, **[SHOP]** |
| Shopify product / variant id | `9328460431617` / `50248139571457` | **[SHOP]** |
| **Store publish date** | **2026-08-28T12:00:54+08:00** (created 2026-08-28T10:48:38+08:00 — 72 minutes earlier) | **[SHOP]** |
| List price | **USD 18.95** | **[SHOP]** |
| Schematic revision | **V0.3, 2026-05-28** | **[SCH]** filename + title block |
| Hosts | **Cardputer-Adv**, **CardputerZero**; announced for **Cardputer P4 (Next)** | **[DOC]**; P4 is **[COM]** |
| ❌ Not | the original Cardputer (no expansion bus) | **[DOC]** |
| Bus | Cap-Bus 14-pin (`HDR_14P-P2.54`, `P1`) | **[SCH]** |
| Extra connector | HY2.0-4P Grove (`J1`) — `5V / GND / SDA / SCL` pass-through | **[SCH]**, **[DOC]** |
| Antenna connector | **`E1` = `SMA-TH_KH-SMA-KE-Z`**, one port for all bands | **[SCH]** |
| In the box | the Cap + **three** RP-SMA rubber antennas: **315 MHz, 433 MHz, 868 MHz** (the 868 one covers 915) | **[DOC]** |
| Size / weight | 84.0 × 24.0 × **19.7** mm · 14.9 g | **[DOC]** |

> **Note the height.** 19.7 mm vs the LoRa Cap's 15.2 mm. If you are printing a case, the
> two Caps are **not** dimensionally interchangeable. Existing Cardputer+LoRa-Cap cases on
> Printables ([r/CardPuter 2026-07-18](https://old.reddit.com/r/CardPuter/comments/1v05l8h/))
> will not fit this one.

### 1.1 Eleven months from tease to shelf

An owner emailed M5Stack in September 2025 and posted the reply:
*"Cardputer ADV Hacker cap (CC1101 SubGHz & ST25R3916 RFID) expected release … So release
will be in around 3-4 months, either in December or January."*
([r/CardPuter 2025-09-08](https://old.reddit.com/r/CardPuter/comments/1nbe134/)). **[COM]**
It shipped **2026-08-28**. In between, u/Relevant-Lynx-6688 asked for an update on
2026-01-31 and got none. Both chips were named correctly in that 2025 email, so the design
was fixed nearly a year before release.

---

## 2. Chip inventory

Designator census across all three sheets. **[SCH]**

| Ref | Sheet | Part | Function | Record |
|---|---|---|---|---|
| **U3** | 3 | **`CC1101RGPR`** (QFN-20 + EPAD21) | Sub-1 GHz FSK/OOK transceiver | [`components/texas-instruments/cc1101`](../../../components/texas-instruments/cc1101/README.md) |
| **U2** | 2 | **`ST25R3916-AQWT`** (QFN-32 + EPAD33) | NFC front end, reader/writer + card emulation | [`components/stmicroelectronics/st25r3916`](../../../components/stmicroelectronics/st25r3916/README.md) |
| **U4, U5** | 3 | **`BGS13SN8E6327XTSA1`** ×2 | **SP3T RF switches** — the multi-band trick | [`components/infineon/bgs13sn8`](../../../components/infineon/bgs13sn8/README.md) |
| **B1** | 3 | **`B0310J50100AHF`** | Wideband **balun**, CC1101 differential RF ↔ 50 Ω single-ended | [`components/generic/rf-balun-b0310j50100ahf`](../../../components/generic/rf-balun-b0310j50100ahf/README.md) |
| **U1** | 1 | **`JW5712`** | 5 V → 3.3 V buck, `IOUT: 0~0.6 A`, **enabled by host G3** | [`components/joulwatt/jw5712`](../../../components/joulwatt/jw5712/README.md) |
| **Y2** | 3 | **26 MHz** crystal, `Y2016` package, C48/C49 = 12 pF | CC1101 reference | — |
| **Y1** | 2 | **27.12 MHz** crystal, C19/C20 = 6.0 pF | ST25R3916 reference — **the NFC carrier is 13.56 MHz = 27.12/2** | [`components/generic/xl7el89cmi-111ylc-27.12mhz-crystal`](../../../components/generic/xl7el89cmi-111ylc-27.12mhz-crystal/README.md) |
| **ANT1** | 2 | NFC antenna, differential `ANT1_P` / `ANT1_N` | 13.56 MHz loop | — |
| **E1** | 3 | `SMA-TH_KH-SMA-KE-Z` | Sub-GHz antenna connector | [`components/generic/rp-sma-and-sma-antenna-connectors`](../../../components/generic/rp-sma-and-sma-antenna-connectors/README.md) |
| **P1** | 1 | `HDR_14P-P2.54` | Cap-Bus | [`pinouts-and-buses.md`](pinouts-and-buses.md) |
| **J1** | 1 | `GROVE 4P` | HY2.0-4P pass-through | — |
| **L1** | 1 | `MWTC201608S2R2` (2.2 µH) | Buck inductor | — |
| **R1** | 1 | **100 kΩ** | Buck enable network with `POWER_EN` | — |
| L4 3.3 nH · L5 6.8 nH · C42 100 pF · C43 0.6 pF · C46 100 pF · C47 100 pF · R5 0 Ω · R6 56 kΩ (`RBIAS`) | 3 | CC1101 balun / bias network | — |
| L6 10 nH · L7 0 R · L8 10 nH · L17 3.6 nH · C50 8 pF · C51 DNP | 3 | **315 MHz** band path (`315MHz 频段`) | — |
| L9 · L10–L13 · C52–C55 (0 R, 0 R, 15 nH, 0 R, 10 pF, NC, 6.2 pF) | 3 | **433 MHz** band path | — |
| L15 0 R · L16 10 nH · C58/C59 · C60/C61 · R7 · D1 0 R | 3 | **868/915 MHz** band path | — |
| C7 220 pF · C8 10 pF · C9 DNP · R2/R3 1.5 Ω · L2/L3 270 nH ±5 % · C10 220 pF · C11/C13 680 pF · C12/C14 150 pF · C15 180 pF · C16 · C17 10 pF · C18 220 pF | 2 | **ST25R3916 differential antenna matching + EMC filter** | — |
| C21–C36 (8 × 10 nF + 8 × 10 µF) | 2 | ST25R3916 supply decoupling — one pair per supply pin | — |
| C37–C41 (100 nF ×5) | 3 | CC1101 AVDD/DVDD decoupling | — |
| R4 330 Ω | 3 | Series on `GDO0` → `CC1101_G0` | — |

**No I/O expander on this board.** Unlike the Cap LoRa-1262, everything is directly
host-driven — plus one trick using the CC1101's own GDO2 pin (§3).

---

## 3. The band-switching architecture — the interesting part

One antenna port serves four bands. Two `BGS13SN8` SP3T switches (one on each side of the
band-specific matching networks) select which of three LC paths the CC1101's balun output
travels through. They are driven by **two control lines**, and only one of them is a host
GPIO:

| Control | Comes from |
|---|---|
| **`CC1101_RF_SW0`** | **host GPIO** — `G13` on Cardputer-Adv, **`G14` on CardputerZero** |
| **`CC1101_RF_SW1`** | **the CC1101's own `GDO2` pin (pin 3)** — set over SPI, not by a host pin |

Truth table (M5Stack publishes it identically on the product page and in the Arduino guide;
the schematic carries an on-sheet table which this pass could **not** transcribe reliably
from the text layer — noted honestly rather than guessed):

| `RF_SW0` | `RF_SW1` | Band |
|:---:|:---:|---|
| 0 | 0 | **315 MHz** |
| 0 | 1 | **433 MHz** |
| 1 | 1 | **868 / 915 MHz** |

`1,0` is unlisted — treat as undefined.

**This is the single most portable idea on the board.** It costs one host GPIO instead of
two, because the transceiver's own general-purpose output does half the work. The cost is
that you cannot set the band before the CC1101 is talking. Full walkthrough with code in
[`features/band-switching.md`](features/band-switching.md).

Independent corroboration from M5Stack's community manager, the day of release:
*"multiple frequency bands: 315 / 433 / 868 / 915 MHz, which can be switched via firmware
using a combination of G13 (Cardputer ADV) or G14 (CardputerZero) as SW0 and GDO2 from the
CC1101 as SW1."* ([r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/)). **[COM]**

---

## 4. Common tasks / How do I…?

| Question | Guide |
|---|---|
| …transmit/receive sub-GHz? | [`features/sub-ghz.md`](features/sub-ghz.md) |
| …switch bands? | [`features/band-switching.md`](features/band-switching.md) |
| …read an NFC tag / emulate a card? | [`features/nfc.md`](features/nfc.md) |
| …**port NFC to other firmware?** | [`features/nfc.md` §10](features/nfc.md) |
| …**port sub-GHz to other firmware?** | [`features/sub-ghz.md` §9](features/sub-ghz.md) |
| …power the Cap on and off? | [`features/power-and-grove.md`](features/power-and-grove.md) |
| …find the pin numbers? | [`pinouts-and-buses.md`](pinouts-and-buses.md) |
| …know why it can't do LoRa? | §6 below |

---

## 5. Vendor specification

| Specification | Value |
|---|---|
| RF chip | **CC1101** |
| Bands | **315 / 433 / 868 / 915 MHz** |
| Range (FSK, 58 kbps air rate) | 315 MHz: **435 m** · 433/868/915 MHz: **441 m** |
| TX power | **+10 dBm** |
| RX sensitivity | **up to −99.5 dBm** |
| Modulation | 2-FSK, 4-FSK, GFSK, MSK, ASK, OOK |
| FIFOs | 64 B TX + 64 B RX, independent |
| NFC chip | **ST25R3916** |
| NFC reader/writer | NFC-A/B (ISO14443A/B), NFC-F (FeliCa™), NFC-V (ISO15693) |
| NFC card emulation | **NFC-A / NFC-F** |
| NFC FIFO | **512 B** |
| Host interface | **SPI** (both chips) |
| Sleep current | **DC 5 V @ 140.87 µA** — CC1101 and NFC both asleep |
| Operating current | **DC 5 V @ 96 mA** — CC1101 continuous TX at max power *and* NFC continuously reading |
| Size / weight | 84.0 × 24.0 × 19.7 mm · 14.9 g |

Prose on those numbers: the two current figures are unusually *well* specified for M5Stack —
both name the exact operating state, and the 140.87 µA sleep figure is the more useful of
the two because it tells you the Cap can be left fitted without meaningfully loading the
host's battery. The "435 m / 441 m" range figures name a modulation and an air rate but not
antennas, height, terrain or a link-margin criterion, so they are marketing numbers with a
method-shaped hole in them; treat as order-of-magnitude only.

---

## 6. ⚠ CC1101 cannot do LoRa. It is not a LoRa board.

The frequencies overlap, so people ask. u/crypticsmellofit, release day:
*"Will the cc1101 also work for LoRA? Those are the right frequencies…"*
Two independent, correct answers followed within the hour:

- u/dargerlick: *"LoRa uses chirp spread spectrum modulation which is not supported on
  CC1101 chips."*
- u/No_Confusion7932: *"No LoRa. … LoRa uses a proprietary spread spectrum modulation that
  is similar to and a derivative of chirp spread spectrum (CSS) modulation. Texas
  Instruments does not manufacture its own LoRa chips. LoRa technology and its associated
  patents belong to Semtech."*

([r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/)) **[COM]**

**If you want LoRa on a Cardputer-Adv, that is the [Cap LoRa-1262](../cap-lora-1262/README.md).**
The two Caps are complementary, and there is only one Cap slot — a limitation owners
complain about explicitly.

What the CC1101 *is* good for: the same territory as a Flipper Zero's sub-GHz radio —
capture, replay and analysis of OOK/FSK remotes, Wireless M-Bus at 868 MHz, and
point-to-point FSK links. u/No_Confusion7932 again: *"It's like the Sub-GHz CC1101 on the
Flipper Zero, except this Cap for the Cardputer has a longer range"* — attributed to the
external antenna and the per-band matching, which is a plausible interpretation but **not a
measurement**.

---

## 7. Photographs

Four product photographs in [`media/`](media/); provenance, rights and captions in
[`media.md`](media.md).

## 8. Related records

- [**Cap LoRa-1262 (U214)**](../cap-lora-1262/README.md) — the LoRa Cap, same bus
- [**Cap LoRa868 (U201)**](../cap-lora868/README.md) — the first Cap
- **Cardputer-Adv** — `devices/m5stack/cardputer-adv/README.md` *(parallel research pass)*
- [**M5Stack PaperMono**](../papermono/README.md) — uses the *same* ST25R3916 over **I²C**
  instead of SPI; the interface strap is the whole difference
- [`guides/nfc`](../../../guides/nfc/README.md) · [`guides/lora`](../../../guides/lora/README.md)

## 9. Files in this record

`README.md` · [`pinouts-and-buses.md`](pinouts-and-buses.md) · [`development.md`](development.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md) ·
[`market-and-pricing.md`](market-and-pricing.md) · [`projects-and-community.md`](projects-and-community.md) ·
[`sources.md`](sources.md) · [`research-log.md`](research-log.md) · [`commands.md`](commands.md) ·
[`media.md`](media.md) · [`features/`](features/README.md) · [`artifacts/`](artifacts/)
