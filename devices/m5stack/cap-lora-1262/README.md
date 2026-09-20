# M5Stack Cap LoRa-1262 (SKU U214)

> **What it is:** a 14-pin expansion board ("Cap") for the **Cardputer-Adv** and
> **CardputerZero**, carrying a **Semtech SX1262** LoRa radio in an M5Stack
> `Stamp LoRa-1262 Mini` module *and* an **ATGM336H-6N** GNSS receiver, plus a
> `PI4IOE5V6408` I/O expander, a `MAX2659` GNSS LNA, a `JW5712` buck and a
> pass-through Grove port.
>
> **Snapshot:** 2026-09-04 · **Schematic revision documented: V1.1, dated 2025-10-29**
> · nothing tested on hardware.

---

## ⚠ Read this first: the release date in circulation is wrong

**Cap LoRa-1262 is not a new product.** It was published to M5Stack's store on
**2025-12-30**, more than eight months before this snapshot. The board that shipped
in **August 2026** is its sibling, the [**Cap CC1101 & NFC**](../cap-cc1101/README.md)
(2026-08-28). §2 lays out the primary evidence and the full family timeline.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[SCH]** | Read out of `U214-Cap-LoRa1262_SCH_V1.1_20251029.pdf`, held in [`artifacts/schematic/`](artifacts/schematic/) | `executed-success` for the extraction; `not-tested` electrically |
| **[DOC]** | `docs.m5stack.com/en/cap/Cap_LoRa-1262`, retrieved 2026-09-04 | `not-tested` |
| **[SHOP]** | `shop.m5stack.com` product JSON, retrieved 2026-09-04 | machine-readable, `executed-success` |
| **[SRC]** | Source code read at a cited path/commit | `executed-success` for the read |
| **[COM]** | Community report — Reddit thread, cited by permalink and date | `reported-working` at best |
| **[INF]** | Inference | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Marketed name | **Cap LoRa-1262** (store title: *Cap LoRa 1262 for Cardputer Adv (SX1262, ATGM336H)*) | **[DOC]**, **[SHOP]** |
| SKU | **U214** | **[DOC]** header, **[SHOP]** variant SKU |
| Shopify product id / variant id | `8988582248705` / `47023567274241` | **[SHOP]** |
| Store publish date | **2025-12-30T09:27:06+08:00** (created 2025-12-25T18:14:13+08:00) | **[SHOP]** |
| List price | **USD 14.50** | **[SHOP]** |
| Documented schematic revision | **V1.1, 2025-10-29** (file uploaded 2025-11-07) | **[SCH]** filename + title block |
| Host compatibility | **Cardputer-Adv**, **CardputerZero**; announced as compatible with the unreleased **Cardputer P4 (Next)** | **[DOC]**; P4 claim is **[COM]** — M5Stack community manager, [r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/) |
| ❌ Not compatible with | **the original Cardputer (K132 / K132-V11)** — it has no expansion bus, only a Grove port | **[DOC]** Cardputer spec table; **[COM]** |
| Bus | **Cap-Bus**, a 14-pin 2.54 mm header (`HDR-SMD_14P-P2.54`, designator `P1`) that mates with the Cardputer-Adv **EXT 2.54-14P** | **[SCH]**, **[DOC]** |
| Extra connector | **HY2.0-4P Grove** (`J2`, `GROVE 4P`) carrying `5V / GND / SDA / SCL` — pass-through of the host I²C bus | **[SCH]**, **[DOC]** |
| Size / weight | 84.0 × 24.0 × 15.2 mm · 22.1 g excl. antenna | **[DOC]** |
| Predecessor | [**Cap LoRa868 / U201**](../cap-lora868/README.md), published 2025-09-05, now **[EOL]** | **[SHOP]**, **[DOC]** |
| Sold inside | [**Cardputer Mesh Kit / K152**](../cardputer-mesh-kit/README.md) (Cardputer-Adv + this Cap), published 2026-04-30 | **[DOC]**, **[SHOP]** |

### 1.1 One SKU, no regional variants — and that matters

There is **one** Cap LoRa-1262. The band is **868–923 MHz** as a single wideband range,
covering EU 868, US 915 and JP 920/923 allocations with no per-region part number, no
per-region antenna in the box, and **no published certification identifier of any kind**
(`docs.m5stack.com/en/certification` lists nothing for `U214`, `Cap LoRa`, or `Cardputer`).
See [`features/lora.md` §7](features/lora.md) for what that means legally and practically.

---

## 2. Where this board sits in the family — dated, from primary evidence

Every date below is a Shopify `published_at` from `shop.m5stack.com/products/<handle>.json`,
retrieved 2026-09-04. **[SHOP]**

| Date | SKU | Product | Price (USD) | Relevance |
|---|---|---|---|---|
| 2023-10-13 | K132 | M5Stack Cardputer Kit w/ M5StampS3 **[EOL]** | 23.90 | The original. **Grove port only** — no Cap can attach |
| 2023-10-20 | U170 | LoRa Unit with Antenna (E220) | 33.00 | Grove/UART LoRa modem — attaches to *any* Cardputer |
| 2024-07-12 | U170-433 | LoRa Unit 433 MHz (E220) | 12.95 | ditto, 433 MHz |
| 2024-12-20 | U184-\* | LoRaWAN Unit EU868/US915/AS923/CN470 (STM32WLE5) | 18.95–21.50 | Grove/UART LoRaWAN modem |
| 2025-03-07 | K132-V11 | Cardputer with M5StampS3 v1.1 **[EOL]** | 29.90 | still Grove-only |
| **2025-09-05** | **K132-ADV** | **M5Stack Cardputer Adv** | 29.90 | **introduces the EXT 2.54-14P bus** |
| **2025-09-05** | **U201** | **LoRa+GPS Cap for Cardputer Adv** ("Cap LoRa868") **[EOL]** | 14.50 | **the first Cardputer LoRa expansion** |
| 2025-10-10 | U202 | M5Stack C6L Unit for Meshtastic (SX1262 + ESP32-C6) | 22.90 | Grove-attached *self-contained* Meshtastic node |
| 2025-11-07 | M146 | M5Stack CC1101 Module (855–925 MHz) | 10.95 | Core-bus module, **not** Cardputer |
| **2025-12-30** | **U214** | **Cap LoRa-1262** ← *this record* | 14.50 | supersedes U201 |
| 2026-03-13 | S012 | [M5Stamp C6LoRa](../stamp-c6lora/README.md) | 12.95 | solder-down module, not an expansion |
| 2026-04-30 | K152 | [Cardputer Mesh Kit](../cardputer-mesh-kit/README.md) | 48.00 | ADV + U214 + antenna, Meshtastic-licensed |
| **2026-08-28** | **U219** | [**Cap CC1101 & NFC**](../cap-cc1101/README.md) | 18.95 | **the genuinely new board** |

**Corroboration for the U214 date, independent of Shopify:** M5Stack's own announcement
post *"New Arrival Alert! Cap LoRa 1262 Available Now!"* was posted to
[r/M5Stack](https://old.reddit.com/r/M5Stack/comments/1pzazbe/) and
[r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1pzazuu/) on **2025-12-30**. **[COM]**

**Third line of evidence:** the documentation CDN allocates a per-product numeric prefix in
release order — `1208` = U214, `1223` = S012, `1240` = K152, `1250` = U219. U214's assets sit
*below* all three of the 2026 products. **[DOC]**, `inferred` for the ordering rule.

### 2.1 What changed from Cap LoRa868 (U201) to Cap LoRa-1262 (U214)

M5Stack publishes a comparison table on the U214 page. **[DOC]**

| Feature | Cap LoRa868 (U201) | Cap LoRa-1262 (U214) |
|---|---|---|
| HY2.0-4P Grove expansion | **No** | **Yes** |
| LoRa module | `Stamp LoRa-1262` — "legacy version, standard size" | `Stamp LoRa-1262` **Mini**, smaller |
| RF shielding can | **No** | **Yes** |
| RF switch control | **None** | **via I/O expander** (`PI4IOE5V6408` P0) |
| TX power (vendor claim) | **+20 dBm** | **+22 dBm** |
| Performance | — | "Better" |

Owner reaction on release day was that this is an incremental refresh, not a fix:
u/griffog asked *"was there an issue with the original cap … or does this just have the
addition of the I2C port?"*, and M5Stack-adjacent poster u/truthfly replied
*"Just a little upgrade, yours is fine 👌"*
([r/CardPuter, 2025-12-30](https://old.reddit.com/r/CardPuter/comments/1pzazuu/)). **[COM]**

---

## 3. Chip inventory

Complete `CO`-marker designator census from the schematic: `BT1 C1–C17 D1 E4 FB2 FB3 J1 J2
L1 L2 M1 M2 P1 R1–R4 R5/NC R6/NC R7/NC U1 U2 U3`. **[SCH]**, `executed-success`.

| Ref | Part | Function | Record |
|---|---|---|---|
| **M1** | **`Stamp LoRa-1262 Mini`** (13-pin module) | LoRa radio module — contains the **Semtech SX1262** | [`components/m5stack/stamp-lora-1262`](../../../components/m5stack/stamp-lora-1262/README.md) → [`components/semtech/sx1262`](../../../components/semtech/sx1262/README.md) |
| **M2** | **`ATGM336H-6N`**, comment `GP-02` (18-pin module) | GNSS receiver — contains the **AT6668** chipset | [`components/zhongkewei/atgm336h-6n`](../../../components/zhongkewei/atgm336h-6n/README.md) → [`components/zhongkewei/at6668`](../../../components/zhongkewei/at6668/README.md) |
| **U1** | **`MAX2659`** | GNSS **low-noise amplifier** ahead of the ceramic antenna | [`components/analog-devices/max2659`](../../../components/analog-devices/max2659/README.md) |
| **U2** | **`PI4IOE5V6408`** (16-pin) | 8-bit I²C I/O expander at **0x43**; **P0 drives the LoRa RF switch** | [`components/diodes-incorporated/pi4ioe5v6408`](../../../components/diodes-incorporated/pi4ioe5v6408/README.md) |
| **U3** | **`JW5712`** | 5 V → 3.3 V synchronous buck, `IOUT: 0~0.6 A` printed on the sheet | [`components/joulwatt/jw5712`](../../../components/joulwatt/jw5712/README.md) |
| **J1** | `ANT1818-04` *(printed `ANT181804`)* | **GNSS ceramic patch antenna**, 18 × 18 × 4 mm ⚠ part number read from the schematic comment only | [`components/generic/gnss-ceramic-patch-antenna`](../../../components/generic/gnss-ceramic-patch-antenna/README.md) |
| **E4** | `SMA-KE` | **LoRa antenna connector** — see the RP-SMA/SMA conflict in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) | [`components/generic/rp-sma-and-sma-antenna-connectors`](../../../components/generic/rp-sma-and-sma-antenna-connectors/README.md) |
| **P1** | `HDR-SMD_14P-P2.54` | Cap-Bus header (2 × 7, 2.54 mm) | [`pinouts-and-buses.md`](pinouts-and-buses.md) |
| **J2** | `GROVE 4P` | HY2.0-4P pass-through: `5V / GND / SDA / SCL` | — |
| **BT1** | `Battery` | GNSS backup cell on `M2` pin 6 `VBAT` — keeps ephemeris for hot start | — |
| **L1** | 6.8 nH ±5 % | GNSS LNA input match | — |
| **L2** | `WPN201610U2R2MT` (2.2 µH) | JW5712 output inductor | — |
| **FB2, FB3** | 120 Ω/MB ferrite beads | GNSS supply isolation (`VCC_RF`, `VCC`) | — |
| **C5, C6, C7** | 470 pF, 100 nF, 33 nF | MAX2659 bias/decoupling | — |
| **R1** | 10 kΩ | **JW5712 enable pull-up** → the buck has **no host enable**; the Cap powers up with 5 V. `inferred` from adjacency, not traced | — |
| **R2, R4** | 0 Ω | Series links | — |
| **R3** | 10 kΩ | Grove I²C pull-up | — |
| R5/NC, R6/NC, R7/NC, C13/NC, C14/NC, D1 (`NC`) | not fitted | Depopulated options around `U2` and the antenna path | — |

> **Two chips named on the vendor page do not appear on the schematic as described.**
> The pin-map graphic labels an element `FM8625H` next to `PI4IOE5V6408 P0 → SX_ANT_SW`,
> but the V1.1 schematic's only regulator is `U3 = JW5712`. Recorded as a conflict, not
> resolved. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md) **G3**.

---

## 4. Common tasks / How do I…?

| Question | Guide |
|---|---|
| …send and receive a LoRa packet? | [`features/lora.md`](features/lora.md) |
| …**port LoRa to another board's firmware?** | [`features/lora.md` §11](features/lora.md) — the portability checklist |
| …get a GNSS fix / read NMEA? | [`features/gnss.md`](features/gnss.md) |
| …fix "GPS never locks"? | [`features/gnss.md` §6](features/gnss.md) — it is usually the RX/TX pin swap |
| …drive the antenna RF switch? | [`features/io-expander-and-rf-switch.md`](features/io-expander-and-rf-switch.md) |
| …tell a Cap LoRa-1262 from a Cap LoRa868 at runtime? | [`features/io-expander-and-rf-switch.md` §4](features/io-expander-and-rf-switch.md) — probe `0x43` |
| …use the Grove port while the Cap is fitted? | [`features/power-and-grove.md`](features/power-and-grove.md) |
| …run Meshtastic on it? | [`development.md` §4](development.md) |
| …know which pin is which? | [`pinouts-and-buses.md`](pinouts-and-buses.md) |
| …know what is *not* established? | [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |

---

## 5. Vendor specification (as published)

| Specification | Value | Note |
|---|---|---|
| LoRa module | SX1262 | inside `Stamp LoRa-1262 Mini` |
| LoRa frequency range | **868 – 923 MHz** | single wideband SKU |
| LoRa programmable bit rate | up to 300 kbps | (G)FSK figure, not LoRa |
| LoRa interface | SPI | |
| LoRa TX power | **+22 dBm** | vs +20 dBm on U201 |
| LoRa RX sensitivity | **−147 dBm** | "LoRa low data rate mode" |
| LoRa operating current | **DC 5 V @ 163.4 mA** | condition unstated |
| Modulation | FSK / GFSK / MSK / LoRa / OOK | the page's *Features* list also claims GMSK |
| Antenna (supplied) | 108 × 9.3 mm, 3 dBi, "RP-SMA (internal thread, internal hole)" | ⚠ see conflict **G1** |
| GPS module | **ATGM336H-6N @ AT6668** | |
| GPS interface | **UART, 115200 bps 8N1** | note: *not* the 9600 default of most ATGM336H boards |
| GNSS systems | GPS / QZSS / BD2 / BD3 / GAL / GLO | |
| GNSS bands | BDS B1I+B1C · GPS/QZSS/SBAS L1 · GALILEO E1 · GLONASS R1 | |
| Channels | 50 | |
| Accuracy | < 1.5 m CEP50 | |
| Update rate | up to 10 Hz | |
| Protocol | NMEA 0183 4.1 (+ CASIC binary) | |
| Sensitivity | tracking −162 dBm · acquisition −160 dBm · cold start −148 dBm | |
| TTFF | cold 23 s · hot 1 s | |
| Power-on consumption | **33.1 mA** | condition unstated |

Prose caveat: the two current figures (33.1 mA "power on" and 163.4 mA "LoRa operating")
are given without stating the radio state, duty cycle or supply path, and the board draws
them through a 5 V→3.3 V buck whose own efficiency is unstated. The **predecessor** U201's
page is considerably more useful here — it breaks current down into four named states
(GPS on/LoRa standby 29.24 mA; GPS sleep/LoRa standby 3.16 mA; GPS sleep/LoRa TX max
129.72 mA; GPS on/LoRa TX max 155.03 mA). Those numbers are for a *different board* and
must not be transplanted, but they are the only state-resolved figures M5Stack publishes
for this hardware class. **[DOC]** on both.

---

## 6. Photographs

Product photography from M5Stack's documentation CDN, retained in [`media/`](media/) — see
[`media.md`](media.md) for provenance, rights status, captions and alt text.

---

## 7. Related records

- [**Cap CC1101 & NFC (U219)**](../cap-cc1101/README.md) — the other Cap, same bus, sub-GHz + NFC
- [**Cap LoRa868 (U201)**](../cap-lora868/README.md) — direct predecessor
- [**Cardputer Mesh Kit (K152)**](../cardputer-mesh-kit/README.md) — this Cap bundled with a Cardputer-Adv
- **Cardputer-Adv** — `devices/m5stack/cardputer-adv/README.md` *(owned by a parallel research pass; this record does not write it)*
- [**M5Stack PaperMono**](../papermono/README.md) — the other M5Stack product using a `Stamp LoRa-1262`, wired completely differently
- [`guides/lora`](../../../guides/lora/README.md) · [`guides/nfc`](../../../guides/nfc/README.md)
- [`software/`](../../../software/README.md)

## 8. Files in this record

`README.md` · [`pinouts-and-buses.md`](pinouts-and-buses.md) · [`development.md`](development.md) ·
[`compatibility-and-status.md`](compatibility-and-status.md) · [`gaps-and-conflicts.md`](gaps-and-conflicts.md) ·
[`market-and-pricing.md`](market-and-pricing.md) · [`projects-and-community.md`](projects-and-community.md) ·
[`sources.md`](sources.md) · [`research-log.md`](research-log.md) · [`commands.md`](commands.md) ·
[`media.md`](media.md) · [`features/`](features/README.md) · [`artifacts/`](artifacts/)
