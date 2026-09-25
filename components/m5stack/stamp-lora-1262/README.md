# M5Stack Stamp-LoRa-1262

> **Common guide:** [`guides/lora`](../../../guides/lora/README.md) — the device-independent LoRa material (the module-independent LoRa material: modulation trade-offs, band plans, SX126x interface pitfalls and RadioLib). This record covers the part; that guide covers the domain.

- **Category:** LoRa transceiver **module** — a carrier for a [Semtech SX1262](../../semtech/sx1262/README.md) sub-GHz radio, presented to the host as a 13-pin SPI + control interface
- **Scope of this record:** **module level only.** Radio architecture, register map, modem configuration, RF characteristics and errata belong to the SX1262 and are documented in [`components/semtech/sx1262/`](../../semtech/sx1262/README.md). This record covers the module's pinout, supply, control lines and how the PaperMono drives it.
- **Research status:** ⚠ **No module datasheet was located.** M5Stack publishes the *chip* datasheet (`DS_SX1261_2_V2-2`) and nothing module-specific. Everything below comes from the PaperMono schematic symbol, the vendor pin map and the firmware — not from a module specification.
- **Retrieved:** 2026-09-01

The LoRa radio of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153). **The PaperMono-Lite does not fit it** — that is one of the two hardware differences between the SKUs.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[SCH]** | Read out of `PaperMono_SCH_V0.6.2_20260522.pdf`, cited as sheet + designator + pin | `executed-success` for the extraction (PDF text-position parsed, all 13 pin pads enumerated); `not-tested` electrically |
| **[SRC]** | Read out of M5Stack source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | `docs.m5stack.com` / `shop.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference | `inferred` |

**No pin below was guessed.** Pins 11–13 carry no printed name and no net label on the schematic symbol; that is stated as such rather than filled in (§2.1).

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Schematic symbol name | **`Stamp-LoRa-1262-mini`** | **[SCH]** sheet 4, symbol body at the `U14` footprint |
| Name in vendor documentation | **`Stamp LoRa-1262`** | **[DOC]** PaperMono PinMap and specification table |
| Reference designator | **`U14`**, sheet 4 | **[SCH]** |
| Pin count | **13** — pads `PIU1401` … `PIU14013` | **[SCH]**, full pad census |
| Radio inside | **Semtech SX1262** | **[DOC]** specification row: `SX1262 (Stamp LoRa-1262), 868–923 MHz, FPC ant.`; corroborated by the module's own pin names `SX_NRST`, `SX_NSS`, `SX_BUSY`, `SX_ANT_SW` **[SCH]** |
| Frequency range advertised | **868 MHz – 923 MHz**, single SKU | **[DOC]** |
| Antenna | **FPC antenna**, per the specification row. The antenna net was **not traced** in this pass | **[DOC]**; **[INF]** for the gap |
| Supply | **3.3 V** on `VIN_3V3` (pin 5), fed from the switched rail `3V3_L2_LoRa` | **[SCH]** `U14`.5 |
| Host interface | **SPI** (`SPI_MOSI`, `SPI_MISO`, `SPI_CLK`, `SX_NSS`) + `SX_BUSY`, `LORA_IRQ`, `SX_NRST`, `SX_ANT_SW` | **[SCH]** |
| ⚠ Marking verified? | **No.** No teardown photograph of `U14` was inspected. The module identity rests on the schematic symbol name and the vendor specification row, both primary M5Stack documents but neither a photograph | **[INF]** |
| ⚠ Naming variance | The schematic says `Stamp-LoRa-1262-**mini**`; the documentation says `Stamp LoRa-1262` with no suffix. Whether `-mini` denotes a distinct variant or is merely the symbol's library name is **not established** — no M5Stack catalogue entry for either exact string was confirmed in this pass | **[SCH]** vs **[DOC]** |

---

## 2. Pin table

All 13 pin pads on the `U14` symbol were enumerated from the schematic's text-position layer and matched to their printed names and adjacent net labels by coordinate. **[SCH]** sheet 4.

| Pin | Module pin name | Direction (module view) | PaperMono net | Connects to |
|---:|---|---|---|---|
| **1** | `GND` | — | `GND` | Ground |
| **2** | `SX_NRST` | I | `PYB_LoRa_RST` | **[M5IOE1](../m5ioe1/README.md) `IO10`** — *not* an ESP32 pin |
| **3** | `SX_BUSY` | O | `G21_LoRa_BUSY` | ESP32-S3 **GPIO21** |
| **4** | `LORA_IRQ` | O | `G5_LoRa_INT` | ESP32-S3 **GPIO5** |
| **5** | `VIN_3V3` | P | `3V3_L2_LoRa` | Switched 3.3 V rail, gated by **[M5PM1](../m5pm1/README.md) `IO2`** |
| **6** | `SPI_CLK` | I | `G39_SPI1_CLK` | ESP32-S3 **GPIO39** |
| **7** | `SPI_MOSI` | I | `G38_SPI1_MOSI` | ESP32-S3 **GPIO38** |
| **8** | `SPI_MISO` | O | `G40_SPI1_MISO` | ESP32-S3 **GPIO40** |
| **9** | `SX_NSS` | I | `G41_LoRa_NSS` | ESP32-S3 **GPIO41** |
| **10** | `SX_ANT_SW` | I | `PYB_LoRa_ANT_SW` | **[M5IOE1](../m5ioe1/README.md) `IO2`** |
| **11** | *(no printed name)* | — | *(no net label)* | see §2.1 |
| **12** | *(no printed name)* | — | *(no net label)* | see §2.1 |
| **13** | *(no printed name)* | — | *(no net label)* | see §2.1 |

Local decoupling: `C65`, **10 µF / 10 V**, adjacent to pin 5 **[SCH]**.

### 2.1 Pins 11–13: unlabelled, not proven no-connect

The pads `PIU14011`, `PIU14012` and `PIU14013` **exist on the symbol** and carry their pin numbers (13, 12, 11 top-to-bottom on the right-hand side of the symbol). They have:

- **no printed pin name** inside the symbol body, and
- **no net label** adjacent to them.

The SKILL's rule applies: *a drawn no-connect marker is a positive assertion; a blank cell is merely unknown*. **No `NC` glyph was found at those coordinates**, so these three pins are **unlabelled and apparently unrouted** — which is *not* the same as documented no-connects. They may be spare module GPIOs, factory-test pads, or genuinely absent from this module variant. **Unresolved**; a module datasheet or a photograph of the footprint would settle it.

---

## 3. Interface summary

### 3.1 SPI

Four-wire SPI on a bus the module does not share with anything else on this board: MOSI/MISO/CLK/NSS on ESP32-S3 GPIO 38 / 40 / 39 / 41 **[SCH]**, **[SRC]** `M5PaperMono-UserDemo/main/hal/hal_lora.cpp:23-26`. The e-paper uses a separate SPI host (SPI2 on GPIO 14/15/16/17), so there is **no chip-select arbitration** between display and radio.

SPI mode, clock rate and frame format are **not** fixed by the module — they are properties of the SX1262 and of RadioLib's configuration. See the [SX1262 record](../../semtech/sx1262/README.md).

### 3.2 `BUSY`

Pin 3, to GPIO21. On the SX1262 this is a mandatory handshake line, not an optional status output: the host must wait for it to fall before issuing most commands. Any driver that ignores it will intermittently lose commands. `not-tested` here; the constraint is the chip's, documented in the SX1262 record.

### 3.3 `LORA_IRQ` is the SX1262's `DIO1`

The module labels pin 4 `LORA_IRQ`; the docs call the net `LORA_IRQ`; **the firmware names the same line `LORA_DIO1_PIN`** **[SRC]** `hal_lora.cpp:27`. So the module brings out **DIO1** specifically — not a wired-OR of all DIO pins, and not DIO2 or DIO3. That matters, because on the SX1262 DIO2 can be repurposed as an RF switch control and DIO3 as a TCXO supply; whichever of those the module uses internally is **not visible from outside** and is not documented anywhere located in this pass.

The same GPIO5 line is registered as an ESP32-S3 **wake source** **[SRC]** `app_sleep_wake.cpp:44`, so a LoRa packet can wake the board.

### 3.4 `SX_NRST` and `SX_ANT_SW` are behind the I²C expander

Neither reset nor the antenna switch is an ESP32 pin. Both go to the [M5IOE1](../m5ioe1/README.md):

| Line | Module pin | M5IOE1 pin | Enum (⚠ value ≠ label) | Source |
|---|---:|---|---|---|
| `SX_NRST` | **2** | `IO10` | `M5IOE1_PIN_10` = **`9`** | **[SRC]** `hal_lora.cpp:30` |
| `SX_ANT_SW` | **10** | `IO2` | `M5IOE1_PIN_2` = **`1`** | **[SRC]** `hal_lora.cpp:31` |

> ⚠ Mind the **two** numbering traps colliding here: the *module* pin numbers and the *expander* pin numbers are unrelated (module pin 2 → expander `IO10`; module pin 10 → expander `IO2` — very nearly a transposition), and the expander's enum value is one less than its label. See [M5IOE1 §6](../m5ioe1/README.md#6--the-m5ioe1_pin_n--n--1-off-by-one).

**Consequence:** you cannot reset the radio, and cannot switch the antenna path, without a working I²C bus and a working M5IOE1. On a board where the same expander also gates the display's reset and power, an I²C fault takes down radio and screen together.

### 3.5 Power gating

`VIN_3V3` (pin 5) sits on `3V3_L2_LoRa`, a rail enabled by **M5PM1 `IO2`** — `PYG2_LoRa_EN` on the schematic **[SCH]** sheet 1 power map, `U7`.20; **[SRC]** `hal_lora.cpp:29`, `app_sleep_wake.cpp:70`.

So the module has a **hard power cut** available, independent of the SX1262's own sleep modes. Bring-up order matters: enable the M5PM1 rail, then release `SX_NRST` through the M5IOE1, then talk SPI. Nothing in the vendor documentation states this ordering explicitly — it follows from the wiring. **[INF]**

---

## 4. Software

| Item | Value | Evidence |
|---|---|---|
| **Driver** | **RadioLib** (jgromes) | **[SRC]**, **[DOC]** |
| **Version pinned by the factory firmware** | **`7.2.1`**, commit `b91c6af112e423dcb14529ade5827802a14e1015` | **[SRC]** `M5PaperMono-UserDemo/repos.json` |
| Local modification | **Patched**, and the patch **removes `idf_component.yml`** so it builds as a plain component rather than a managed one | **[SRC]** `repos.json` `patched: yes, + removes idf_component.yml` |
| Version in the published PlatformIO config | **Unpinned** — `RadioLib = https://github.com/jgromes/RadioLib` | **[DOC]** |
| Upstream licence | RadioLib is **LGPL-3.0** upstream, while the M5Stack demo carrying it is MIT. **Not verified in this pass** — flagged, not confirmed | **[INF]**, `not-tested` |

> ⚠ **The docs' unpinned dependency and the firmware's pinned commit are not the same thing.** Building from the published PlatformIO snippet pulls RadioLib `master`, not `7.2.1`. If you are trying to reproduce factory behaviour, use the pinned commit. **[SRC]** vs **[DOC]**.

There is **no M5Stack-specific LoRa library** for this module. `hal_lora.cpp` in the UserDemo is a thin wrapper that hands the six pin numbers to RadioLib and gets out of the way **[SRC]**.

Framework context: ESP-IDF **5.5.1**, target `esp32s3`, arduino-esp32 **3.3.10** as a managed component **[SRC]** `dependencies.lock`.

---

## 5. Caveats and gaps

| # | Issue | Evidence |
|---|---|---|
| **G1** | **⚠ No module datasheet exists in this repository, and none was located.** M5Stack's *Datasheets* list for the PaperMono links the **Semtech chip** datasheet (`DS_SX1261_2_V2-2`), not a module document. Nothing states the module's supply current, its RF output power at the connector, its antenna interface, its internal matching network, whether it fits a TCXO or a crystal, which DIO pins are consumed internally, or what pins 11–13 are | **[DOC]**; the absence is `executed-success` — the full datasheet list was enumerated |
| **G2** | **Pins 11–13 are unlabelled with no drawn no-connect.** §2.1. Unresolved | **[SCH]** |
| **G3** | **TCXO vs XTAL is unknown, and it changes the driver setup.** The SX1262 needs `DIO3` configured as a TCXO supply *if* a TCXO is fitted, and getting this wrong produces a radio that appears to initialise and then fails to transmit or receive. The module does not expose `DIO3`, so the decision was made inside the module — but no document says which. **Do not guess:** check what RadioLib's PaperMono configuration does before changing it | **[INF]**; the SX1262 record covers the mechanism |
| **G4** | **`SX_ANT_SW` semantics are undocumented.** Whether it selects TX/RX paths, enables an external PA/LNA, or switches between antenna connectors is not stated anywhere located. `hal_lora.cpp:31` only assigns the pin | **[SRC]** |
| ~~**G5**~~ | ⚠ **CORRECTED 2026-09-20 — the board is certified.** The narrow finding survives: `docs.m5stack.com/en/certification` really does return **0 matches** for `PaperMono` and **0** for `C153`, and no identifier appears on any documentation page or store listing. **But the PaperMono holds FCC ID `2AN3WM5PAPERMONO`, granted 2026-08-12**, and the US grant authorises this module on **903.0–914.9 MHz only, at 11.5 dBm conducted** — *not* the 868–923 MHz the SKU claims. The vendor firmware's hard-coded 868.0 MHz is outside that grant. The deployment warning therefore **stands and sharpens**; what changes is that US paperwork now exists. No CE, IC, RCM, UKCA or SRRC record has been located. See [`certification.md`](../../../devices/m5stack/papermono/certification.md) | **[DOC]** negative result superseded by **[REG]** FCC exhibits, retrieved 2026-09-11 |
| **G6** | **The `-mini` suffix is unexplained.** §1 | **[SCH]** vs **[DOC]** |
| **G7** | **PDF extraction artifact worth knowing.** In the schematic's net-annotation layer, underscores render as the digit `0` — `G41_LoRa_NSS` appears as `NLG410LoRa0NSS`, `PYB_LoRa_ANT_SW` as `oRa0ANT0SW`. The **visible** net labels are correct; only the hidden annotation strings are affected. Any future automated netlist extraction from this PDF must account for it or it will produce plausible-looking wrong net names | `executed-success` — observed directly in the text-position dump of sheet 4 |

---

## 6. Used By

### [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — designator `U14`, sheet 4

> **FCC internal photographs — 2026-09-20.** The PaperMono's FCC filing
> (`2AN3WM5PAPERMONO`) includes an internal-photograph exhibit, now retained at
> [`devices/m5stack/papermono/artifacts/certification/`](../../../devices/m5stack/papermono/artifacts/certification/README.md).
> It is the first physical-hardware evidence for this part on this board.
>
> **The module is confirmed to be a real module.** This record notes that no
> module datasheet exists and that everything comes from the schematic symbol.
> Exhibit p. 3 now shows it physically: a **castellated sub-PCB** carrying the
> SX1262 QFN, a matching network, a **U.FL/IPEX connector** and a **4-pad
> ceramic oscillator marked `M10`**, soldered onto the main board. Pages 6–7
> show the antenna it feeds — a **52 × 7.7 mm FPC strip** silkscreened
> `Paper Mono V3.0`, bonded into the bottom of the rear housing, reached by a
> coaxial pigtail.
>
> **The antenna is now identified**: supplier **Shenzhen Rongshengyuan**, part
> **`RSY-E8131`**, spec V3.0 dated 2026-02-01, **IPEX4**, VSWR < 4, and measured
> **−5.00 dBi / 15.9 % efficiency at 910 MHz** (−6.72 to −4.57 dBi across
> 860–920 MHz). That is a poor antenna, and any link-budget estimate assuming
> 0 dBi is optimistic by ~5 dB.
>
> **Certified US band is 903.0–914.9 MHz at 11.5 dBm conducted** — not the
> 868–923 MHz the SKU claims. **`SX_ANT_SW` is independently confirmed to be
> driven from M5IOE1 `IOE_G2`** by M5Stack's FCC label exhibit, though its
> semantics remain unknown.
>
> [G5](../../../devices/m5stack/papermono/gaps-and-conflicts.md#g5--no-stamp-lora-1262-module-datasheet-exists-anywhere-located)
> is partly advanced by this; extraction in
> [`certification.md` §3, §6](../../../devices/m5stack/papermono/certification.md#3--antenna-specification).

The only LoRa radio on the board, and one of the two features that distinguish the PaperMono from the PaperMono-Lite (the other is NFC). Priced at a **USD 10.00** delta for both together **[DOC]**.

Complete host-side wiring, all confirmed by two independent sources (schematic + firmware) except where noted:

| Function | Module pin | Host | Evidence |
|---|---:|---|---|
| SPI MOSI | 7 | ESP32-S3 **GPIO38** | **[SCH]** `U14`.7; **[SRC]** `hal_lora.cpp:25` |
| SPI MISO | 8 | ESP32-S3 **GPIO40** | **[SCH]** `U14`.8; **[SRC]** `hal_lora.cpp:24` |
| SPI CLK | 6 | ESP32-S3 **GPIO39** | **[SCH]** `U14`.6; **[SRC]** `hal_lora.cpp:23` |
| SPI NSS | 9 | ESP32-S3 **GPIO41** | **[SCH]** `U14`.9; **[SRC]** `hal_lora.cpp:26` |
| BUSY | 3 | ESP32-S3 **GPIO21** | **[SCH]** `U14`.3; **[SRC]** `hal_lora.cpp:28` |
| IRQ (**DIO1**) | 4 | ESP32-S3 **GPIO5**, also an **ESP32 wake source** | **[SCH]** `U14`.4; **[SRC]** `hal_lora.cpp:27`, `app_sleep_wake.cpp:44` |
| `NRST` | 2 | **M5IOE1 `IO10`** (`M5IOE1_PIN_10` = value `9`) | **[SCH]** `U14`.2; **[SRC]** `hal_lora.cpp:30` |
| `ANT_SW` | 10 | **M5IOE1 `IO2`** (`M5IOE1_PIN_2` = value `1`) | **[SCH]** `U14`.10; **[SRC]** `hal_lora.cpp:31` |
| Power enable | 5 (`VIN_3V3`) | Rail `3V3_L2_LoRa`, gated by **M5PM1 `IO2`** | **[SCH]** `U14`.5, `U7`.20; **[SRC]** `hal_lora.cpp:29` |

Board-level notes:

- **The LoRa rail is on the `L2` power level**, alongside the ESP32-S3, NFC, the M5IOE1 and the buzzer **[DOC]** power-tree table. It is not part of `L3B`, so it does not depend on the M5IOE1 for *power* — only for reset and antenna switching.
- **Bring-up ordering is implied by the wiring, not documented:** M5PM1 `IO2` high → M5IOE1 `IO10` released → SPI. `inferred`.
- **A LoRa interrupt is a documented ESP32 wake source** on this board (`c.LoRa_INT` in the schematic's wake-source note, sheet 1) **[SCH]**, and the sheet-1 block diagram tags the LoRa block "SX1262; Wake-up support".
- **No SPI contention with the display.** The e-paper is on SPI2 (GPIO 14–18); the radio is on the separate SPI1 pin group (GPIO 38–41) **[SCH]**, **[SRC]**.
- The UserDemo ships a **LoRa demo application** among its fifteen apps **[SRC]**, and the Arduino documentation advertises a dedicated `lora` API sub-page (enumerated but **not fetched** in this pass) **[DOC]**.

### [M5Stack PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) — **not fitted**

The Lite has **no LoRa row in its specification table at all**, no LoRa block in its PinMap, and its PlatformIO `lib_deps` omits `RadioLib` **[DOC]**. Its bill of materials is 2.3 g lighter than the PaperMono's (72.4 g vs 74.7 g product weight), which is consistent with two omitted radios **[DOC]**.

Note that the shared `M5PaperMono-UserDemo` firmware image serves **both** SKUs and detects the variant at runtime by probing the NFC rail, not the radio **[SRC]** `hal_board.cpp:160-172`.

### [M5Stack Cap LoRa-1262 (U214)](../../../devices/m5stack/cap-lora-1262/README.md) — designator `M1` · *added 2026-09-04*

A Cardputer-Adv / CardputerZero expansion board, store publish date **2025-12-30**, USD 14.50. Its schematic (V1.1, 2025-10-29, held at [`devices/m5stack/cap-lora-1262/artifacts/schematic/`](../../../devices/m5stack/cap-lora-1262/artifacts/schematic/)) draws the **same 13-pin module** under the same name — and **prints the three pin names that the PaperMono symbol leaves blank**. See §2.2.

| Module pin | Name on the Cap symbol | Net on that board | Host GPIO |
|---:|---|---|---|
| 1 | `GND` | `GND` | — |
| 2 | `NRST` | `RST` | **G3** — an *ordinary host pin*, not an expander |
| 3 | `BUSY` | `BUSY` | **G6** |
| 4 | `IRQ` | `IRQ` | **G4** |
| 5 | `3V3` | `VDD_3V3` from an on-board `JW5712` buck, **no host enable** | — |
| 6 | `CLK` | `SCK` | **G40** |
| 7 | `MOSI` | `MOSI` | **G14** |
| 8 | `MISO` | `MISO` | **G39** |
| 9 | `NSS` | `NSS` | **G5** |
| 10 | **`SW`** | `SX_ANT_SW` | **`PI4IOE5V6408` P0 @ I²C 0x43** |
| 11 | **`GND`** | RF ground | — |
| 12 | **`ANT`** | → `E4` SMA/RP-SMA connector | — |
| 13 | **`GND`** | RF ground | — |

Board-level notes:

- **SPI is shared with the host's microSD** (`SDCARD_CS` = G12), unlike the PaperMono where the radio has its own host.
- **No power gate.** The Cap's buck is enabled by a 10 kΩ pull-up; the module is live whenever the host supplies 5 V.
- **`SW` is still set once and forgotten** — M5Stack's example and Meshtastic both drive `P0` high at boot and never touch it again, exactly as the PaperMono firmware does with `M5IOE1 IO2`. §5-G4 remains open.
- **TCXO conflict:** M5Stack's Cap example passes `tcxoVoltage = 3.0` (matching the PaperMono firmware), while **Meshtastic upstream sets `SX126X_DIO3_TCXO_VOLTAGE 1.8`** with `TCXO_OPTIONAL`. Both ship; both are reported working. §5-G3 is therefore *narrowed* (a TCXO is fitted) but **not resolved** (its voltage is disputed).
- The Cap's predecessor, [**Cap LoRa868 (U201)**](../../../devices/m5stack/cap-lora868/README.md), fits the **"legacy version, standard size"** `Stamp LoRa-1262` and claims **+20 dBm** rather than +22 — so "Mini" is a real variant distinction, not just a library name. That partially answers §5-G6.

### [M5Stack Cap LoRa868 (U201)](../../../devices/m5stack/cap-lora868/README.md) — standard-size variant · *added 2026-09-04*

Same 14-pin host mapping as the U214 (G3/G4/G6/G40/G14/G39/G5), **without** the `PI4IOE5V6408` antenna-switch control and without a Grove pass-through. M5Stack's own comparison table describes the fitted module as *"Stamp LoRa-1262 legacy version, standard size"*. Published 2025-09-05, now **[EOL]**.

### [M5Stack Cardputer Mesh Kit (K152)](../../../devices/m5stack/cardputer-mesh-kit/README.md) · *added 2026-09-04*

Via the bundled Cap LoRa-1262. The kit page links this module's schematic directly.

---

## 6A. ⭐ Pins 11–13 are now named — §2.1 partially resolved (2026-09-04)

§2.1 records module pins **11, 12 and 13** as *"unlabelled and apparently unrouted — which is not the same as documented no-connects"*, because the PaperMono schematic symbol prints no names there.

**The Cap LoRa-1262 schematic prints them:**

| Pin | Name on the Cap symbol |
|---:|---|
| 11 | **`GND`** |
| 12 | **`ANT`** |
| 13 | **`GND`** |

A **ground-signal-ground coplanar RF launch** at the module's antenna edge — which is exactly what a shielded RF module's edge pads should look like, and it explains why the PaperMono (whose antenna is an FPC bonded elsewhere) leaves them unlabelled and unrouted.

**Confidence: `inferred (strong)`, not proven.** The evidence is that both symbols have **13 pins in the same order** with **the same first nine names** (allowing for the PaperMono's `SX_`/`SPI_`/`VIN_` prefixes), both are called `Stamp LoRa-1262 Mini` / `Stamp-LoRa-1262-mini`, and pin 10 is the antenna-switch control on both. What has **not** been done is compare a photograph of either footprint, or read a module datasheet — because none exists (§5-G1).

Also note: pin 10 is `SX_ANT_SW` on the PaperMono symbol and plain **`SW`** on the Cap symbol. Same pin, two names, one undocumented function.

---

## 7. Related components

- [**Semtech SX1262**](../../semtech/sx1262/README.md) — **the radio inside this module.** Modem, register map, RF performance, sleep modes, DIO configuration, TCXO handling and errata all live there. Read it for anything below the module's pin boundary
- [**M5Stack M5IOE1**](../m5ioe1/README.md) — supplies this module's `NRST` (`IO10`) and `ANT_SW` (`IO2`)
- [**M5Stack M5PM1**](../m5pm1/README.md) — gates this module's 3.3 V supply via `IO2`
- [Vendor sourcing guides index](../../../vendors/README.md) — no M5Stack module-documentation guide exists yet; **G1** above is exactly the kind of finding one should record

---

## 8. Local artifacts

> **Update 2026-09-04: a module-level schematic *was* located.** §5-G1 said no module
> document existed; that is now **partly wrong**. M5Stack publishes a `Stamp LoRa-1262 Mini`
> schematic from the **Cap LoRa-1262** and **Cardputer Mesh Kit** documentation pages — not
> from the PaperMono page, which is why the earlier pass did not find it. It is a
> *schematic*, not a datasheet: it still does not state RF output at the connector, supply
> current, the internal matching network, or which SX1262 DIO pins are consumed internally.
> **G1 is narrowed, not closed.**

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/Stamp-LoRa-1262-Mini_SCH_A1_20250827.pdf`](artifacts/Stamp-LoRa-1262-Mini_SCH_A1_20250827.pdf) | 184 442 | `6ec29a9240fc8dc41fbe699e74a9f645b9753d7932efc1de28b049fe58e8f03b` | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1208/NEW-1262-SCH_A1-Lora_2025_08_27_10_58_52.pdf`, retrieved **2026-09-04**, HTTP 200, `%PDF-1.4`. Filename encodes rev **A1**, dated **2025-08-27**. Linked from `docs.m5stack.com/en/cap/Cap_LoRa-1262` and `/en/core/Cardputer_Mesh_Kit` as *"Stamp LoRa-1262 Mini Schematics PDF"* |

⚠ **Downloaded and type-verified, but not yet decoded.** A bbox text dump exists
(`archive/devices/m5stack/shared-artifacts/lora-expansions/research-scratch/pdf/Stamp-LoRa-1262-Mini_SCH_A1_20250827/bbox-p1.xml`,
815 words) but was **not analysed** by the 2026-09-04 pass, whose subject was the Cap boards
rather than the module. Decoding it should settle §5-G3 (TCXO vs XTAL, and which voltage),
§5-G4 (`SW` semantics) and much of §5-G1. Licence/redistribution: **unknown**. Disposition:
**repository, unstaged** pending review.

The relevant primary documents for the parts around it live with their owners:

| Document | Where |
|---|---|
| SX1261/2 datasheet V2.2 | [`../../semtech/sx1262/artifacts/sx1261-2-datasheet-v2.2-m5stack-mirror.pdf`](../../semtech/sx1262/README.md) |
| PaperMono schematic V0.6.2 (sheet 4 carries `U14`) | Device tree — `PaperMono_SCH_V0.6.2_20260522.pdf` |
| Cap LoRa-1262 schematic V1.1 (carries `M1` and names pins 11–13) | [`devices/m5stack/cap-lora-1262/artifacts/schematic/`](../../../devices/m5stack/cap-lora-1262/artifacts/schematic/) |

If a `Stamp-LoRa-1262` module **datasheet** is ever located, it belongs here too.

---

## 9. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | PaperMono schematic | M5Stack | primary | schematic PDF | `PaperMono_SCH_V0.6.2_20260522.pdf` (held in the device tree) | 2026-09-01 | **V0.6.2, 2026-05-22**, 6 sheets | §1 symbol name, §2 full pin table, §3, §6 |
| S-2 | PaperMono product page (specification table + PinMap) | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono` | 2026-09-01 | undated | §1 identity and frequency range, §4, §6 |
| S-3 | PaperMono-Lite product page | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono-Lite` | 2026-09-01 | undated | §6 — **negative result**: no LoRa row, no `RadioLib` |
| S-4 | `M5PaperMono-UserDemo` — `main/hal/hal_lora.cpp`, `repos.json` | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-UserDemo` @ `c1099107271d31a0678d661a896e2b04dbb331ea` | 2026-09-01 | 2026-08-10, MIT | §2, §3, §4, §6 |
| S-5 | RadioLib | jgromes | third-party | source | `github.com/jgromes/RadioLib` @ `b91c6af112e423dcb14529ade5827802a14e1015` | 2026-09-01 | tag **7.2.1**; upstream licence LGPL-3.0 (**unverified**) | §4 |
| S-6 | SX1261/2 datasheet | Semtech, mirrored by M5Stack | authorized mirror | datasheet | [`../../semtech/sx1262/README.md`](../../semtech/sx1262/README.md) | 2026-09-01 | V2.2 | §1, §3, §5-G3 |
| S-7 | Certification index | M5Stack | primary | vendor docs | `docs.m5stack.com/en/certification` | 2026-09-01 | undated | §5-G5 — **negative result**, 0 matches for `PaperMono` / `C153` |
| S-8 | PaperMono store listing | M5Stack | primary | retail listing | `shop.m5stack.com/products/m5papermono-with-lora-nfc-800x480-3-97-eink-display` | 2026-09-01 | SKU `C153`, USD 65.00, published 2026-08-21 | §6 price delta vs the Lite (USD 55.00) |

## RadioLib licence — resolved 2026-09-02

This record previously flagged "RadioLib is LGPL-3.0 upstream vs MIT on the demo
— flagged, unverified", and a later pass observed MIT on today's `master` without
checking the pinned tree.

**Checked at tag `7.2.1`, the version the vendor demo pins.** RadioLib is **MIT**,
and has been since 2018:

| Evidence @ 7.2.1 | Value |
|---|---|
| `license.txt` (root) | "MIT License … Copyright (c) 2018 Jan Gromeš", 1,068 bytes |
| `library.json` `license` field | `MIT` |
| Any GPL/LGPL text in the licence file | none |
| GitHub API repo licence today | MIT |

**The LGPL-3.0 claim was wrong and is withdrawn.** Worth recording *why* it
survived two passes: an initial probe for a file named `LICENSE` returned 404,
because the file is `license.txt` — lowercase, `.txt`. A 404 on a guessed
filename is not evidence of an absent licence, and it was briefly read that way
here. There is no licence conflict between RadioLib and the MIT-licensed demo.
