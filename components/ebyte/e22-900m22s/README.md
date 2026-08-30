# Ebyte E22-900M22S

> LoRa transceiver module: a **Semtech SX1262** plus a power amplifier, LNA, RF switch and matching, in a stamp-hole SMD module. 868/915 MHz, 22 dBm.
> Research snapshot **2026-08-30**. Fitted as `U23` on the Nicolai Electronics Tanmatsu. **No hardware was available.**
>
> ⚠ **Neither the Ebyte module manual nor the Semtech SX1262 datasheet could be obtained this session** — see §8. Part-level claims below are therefore weaker than in this repository's better-sourced records, and are labelled accordingly. **The schematic-derived integration detail in §4 is the solid part of this record.**

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[PCB]** | `tanmatsu.kicad_pcb` pad→net assignments (CERN-OHL-P) — **primary, verified** |
| **[BOM]** | Tanmatsu production BOM (CERN-OHL-P) |
| **[VEN]** | Ebyte product-page / vendor prose. **Not** a retained document — the weakest class |
| **[INF]** | Author inference |
| **[GAP]** | Claim that would normally be datasheet-backed and is not |

---

## 1. Identity and variants

| Property | Value | Source |
|---|---|---|
| Module | **E22-900M22S** | [BOM] |
| Manufacturer | **Chengdu Ebyte Electronic Technology Co., Ltd.** (成都亿佰特) | [VEN] |
| Radio die | **Semtech SX1262** | [VEN], corroborated by pin function (§4) |
| Band | **868 / 915 MHz** (nominally 850–930 MHz) | [VEN] [GAP] |
| Output power | **22 dBm** (≈158 mW) — the `22` in the part number | [VEN] |
| Package | Stamp-hole SMD module, 22 pads | [PCB], [BOM] |
| Host interface | **SPI** + `BUSY`, `DIO1`, `NRST`, and RF-switch controls | [PCB] |
| LCSC | [`C411293`](https://www.lcsc.com/search?q=C411293) | [BOM] |

### 1.1 The family, and the one substitution that matters here

Ebyte's `E22-<freq>M<power>S` naming decomposes as band / power / form factor:

| Part | Band | Power | Note |
|---|---|---|---|
| **E22-900M22S** | 868/915 MHz | 22 dBm | **The part fitted** |
| **E22-400M22S** | 433 MHz | 22 dBm | ⚠ **Fitted instead on 433 MHz Tanmatsu units** [BOM] |
| E22-900M30S | 868/915 MHz | 30 dBm | Higher power, much higher TX current |
| E22-900MM22S | 868/915 MHz | 22 dBm | Smaller "MM" form factor |

> ⚠ **The Tanmatsu ships in two RF variants.** The production BOM records that **E22-400M22S is fitted on 433 MHz units** [BOM]. The footprint and the digital interface are the same; the **antenna, the matching and the legal regime are not**. Firmware that hardcodes 868 MHz will transmit out of band on a 433 MHz unit. Read the band from a configuration source, not from a constant.

The `S` variants expose the SX1262's SPI directly — they are **not** UART modules. See §3.

---

## 2. The SX1262 inside

The E22-900M22S is not a self-contained radio: it is an SX1262 with an external PA/LNA front end. What that means practically:

- **Modulations:** LoRa (SF5–SF12) and (G)FSK. LoRa gives the long range; FSK is there for higher data rates and for interoperating with non-LoRa systems. [VEN] [GAP]
- **Frequency range of the die:** the SX1262 covers roughly 150 MHz to 960 MHz; the *module* is matched to a narrow band and only that band is usable.
- **The SX1262 is the high-power sibling of the SX1261** (which tops out around 15 dBm). Semtech publishes them in a single datasheet, `DS_SX1261-2`.
- **The SX1262 has its own +22 dBm PA on-die.** Ebyte adds a further external PA/LNA, which is why the module needs explicit **RF switch control** (§4.2) that a bare SX1262 design does not.
- **Command interface, not a register map.** Unlike most radios, the SX126x family is driven by an **opcode-based command set** over SPI (`SetStandby`, `SetPacketType`, `SetRfFrequency`, `SetTx`, `SetRx`, `GetIrqStatus`, …), with a small number of directly addressed registers reached via `WriteRegister`/`ReadRegister`. [GAP] — exact opcodes are not reproduced here because the datasheet was not obtained; see §8.

> ⚠ **`BUSY` is not optional and is the number-one SX126x integration bug.** The chip asserts `BUSY` while it processes a command, and **the host must wait for `BUSY` to go low before issuing the next SPI transaction**. Every mature SX126x driver has an explicit `WaitOnBusy()`. Drivers ported from SX127x (which has no `BUSY`) omit it and produce intermittent, timing-dependent failures that look like SPI corruption. The Tanmatsu routes `BUSY` (§4), so this is implementable.

---

## 3. ⚠ This is the SPI variant — there is no UART on it

Ebyte sells two very different things under similar names:

| Family | Interface | Behaviour |
|---|---|---|
| **`E22-...S` (this part)** | **Raw SPI to the SX1262** | The host runs the full LoRa stack. Maximum control, maximum work |
| `E22-...T` / `-T22D` etc. | **UART + `M0`/`M1` mode pins + `AUX`** | An MCU inside runs a transparent-transmission firmware. Send bytes, they appear at the other end |

The Tanmatsu's netlist shows `LORA_SCK`, `LORA_MISO`, `LORA_MOSI`, `LORA_CS`, `LORA_BUSY`, `LORA_DIO1`, `LORA_RESET` **[PCB]** — unambiguously the **SPI** variant.

**Consequence:** there is no `M0`/`M1` mode configuration, no `AUX` pin, no AT-style parameter set, and none of Ebyte's transparent-transmission documentation applies. You need a LoRa stack — RadioLib, LoRaMac-node, Meshtastic's firmware, or similar (§6).

---

## 4. Exact wiring on the Tanmatsu **[PCB]**

| Pad | Net | Function |
|---:|---|---|
| 1–5, 10–12, 20, 22 | `GND` | Ground |
| **6** | `Net-(U23-RXEN)` | **RX enable** — RF switch control. See §4.2 |
| **7, 8** | `Net-(U23-DIO2)` | **DIO2 / TX enable** — both pads on one net. See §4.2 |
| 9 | `+3.3V` | Supply |
| **13** | `LORA_DIO1` | **DIO1** — the interrupt line, to the **ESP32-C6** (pad 4) |
| **14** | `LORA_BUSY` | **BUSY** — to the ESP32-C6 (pad 5) |
| **15** | `LORA_RESET` | **NRST** — to the ESP32-C6 (pad 11) |
| **16** | `LORA_MISO` | SPI MISO — ESP32-C6 (pad 26) |
| **17** | `LORA_MOSI` | SPI MOSI — ESP32-C6 (pad 27) |
| **18** | `LORA_SCK` | SPI SCK — ESP32-C6 (pad 8) |
| **19** | `LORA_CS` | SPI NSS — ESP32-C6 (pad 9) |
| **21** | **`ANT`** | ⚠ **`unconnected-(U23-ANT-Pad21)`** in the netlist. See §4.3 |

### 4.1 ⚠ The LoRa radio belongs to the ESP32-C6, not the ESP32-P4

Every digital pin of the module lands on the **ESP32-C6-WROOM-1** (`U20`) **[PCB]**, not on the ESP32-P4 application processor.

That is a significant architectural fact and it is easy to miss:

- **The ESP32-P4 cannot reach the LoRa radio directly at all.** Any application-level LoRa feature must be brokered by the C6 over the **4-bit SDIO** link the two share (`esp-hosted`), or by a custom protocol on top of it.
- The C6 is simultaneously the Wi-Fi 6 / BLE / 802.15.4 radio. Adding LoRa duty makes it the single point of contention for **four** radio stacks.
- The C6's own Wi-Fi/BLE traffic and the LoRa SPI transactions share one small MCU. Timing-sensitive LoRa work (precise RX windows, LBT) competes with Wi-Fi. [INF]

### 4.2 ✅ The RF switch is driven by DIO2, inverted — an elegant detail worth documenting

Pads 7 and 8 are both on `Net-(U23-DIO2)`, and that net connects to **`U22` pad 1, a `74LVC1GU04`** — a single **unbuffered inverter**. `U22` pad 4 drives `Net-(U23-RXEN)`, which is pad 6 (RX enable). There is also **`R69` = 100 kΩ** from `Net-(U23-DIO2)` to `GND` **[PCB]**.

So:

```
SX1262 DIO2 ──┬────────────────────────► TXEN  (module pads 7, 8)
              ├── R69 100k ── GND          (pull-down)
              └── U22 74LVC1GU04 ──────► RXEN  (module pad 6)
                     (inverter)
```

This is the standard SX126x idiom, implemented correctly:

- **The SX1262 can be configured to drive `DIO2` automatically as the RF switch control** (`SetDio2AsRfSwitchCtrl(1)` in the SX126x command set). `DIO2` then goes high for the duration of transmit and low otherwise — **with no host intervention and with exactly the right timing**, which is the point: getting TX/RX switching right in software is error-prone.
- **The inverter generates the complementary `RXEN`** from the same signal, so the front end is always in exactly one of TX or RX, and the two can never be asserted together.
- ⚠ **`R69` (100 kΩ pull-down) is the safety element.** It holds `DIO2` low — hence `TXEN` low and, through the inverter, **`RXEN` high** — whenever the SX1262 is unpowered, in reset, or has `DIO2` high-impedance. The front end therefore defaults to **receive**, never to transmit. Defaulting to TX with no valid signal would be both wasteful and potentially non-compliant.

**Firmware consequence:** the driver **must** call the equivalent of `SetDio2AsRfSwitchCtrl(true)` during init. If it does not, `DIO2` stays low, `TXEN` never asserts, `RXEN` stays permanently high, and **the module receives but never transmits** — with no error anywhere. This is a specific, predictable failure mode for this board, and it is the first thing to check if TX appears dead.

### 4.3 ⚠ Unresolved: the `ANT` pad is unconnected in the netlist

Pad 21 (`ANT`) appears as `unconnected-(U23-ANT-Pad21)` **[PCB]**.

A radio module with no antenna connection cannot work, so one of the following holds, and this record cannot distinguish them:

1. The RF path is a **copper trace or coplanar waveguide** whose connection is not represented as a pad-to-net relationship in the way the parser read it.
2. The antenna is a **connector or trace routed on a layer** the netlist extraction did not capture.
3. The published KiCad snapshot has an error here, as it appears to for the [TPS63020's `VINA`/`EN` net](../../texas-instruments/tps63020/README.md#44--unresolved-vina-en-and-pssync-form-an-isolated-net-in-the-published-design).

Recorded as a conflict rather than resolved by preference. The Tanmatsu's [`gaps-and-conflicts.md`](../../../devices/nicolai-electronics/tanmatsu/gaps-and-conflicts.md) discusses the LoRa antenna separately; that is the place to look next, along with reading the schematic sheet graphically.

---

## 5. Regulatory notes

⚠ **This section is [INF] and general. It is not legal advice and is not vendor-sourced.**

- **868 MHz (EU, ETSI EN 300 220) and 915 MHz (US, FCC Part 15.247) are different regimes with different rules.** The same module and the same firmware are not compliant in both.
- **EU 868 MHz imposes a duty-cycle limit** — commonly 1 % or 0.1 % depending on sub-band — and some sub-bands require **Listen Before Talk / Adaptive Frequency Agility**. **22 dBm is 158 mW, above the 25 mW (14 dBm) e.r.p. limit of the most common EU sub-bands.** Running this module at full power on 868 MHz in the EU is very likely non-compliant without a specific sub-band and antenna-gain analysis.
- **US 915 MHz** permits higher power but requires **frequency hopping or wideband** operation under Part 15.247; a fixed-channel LoRa link may fall under 15.249's much lower limits instead.
- **Output power is software-controlled** (`SetTxParams`). The "22 dBm" in the part number is a *capability*, not a fixed setting. Reduce it in firmware for your region.
- ⚠ **Never transmit without an antenna or a 50 Ω load.** A 22 dBm PA into an open circuit can damage itself.
- **Module-level certification does not transfer automatically.** Whether Ebyte holds FCC/CE modular approval, and whether it survives integration into this board with this antenna, was not established. [GAP]
- **The 433 MHz variant (§1.1) is a different regime again** and is not permitted for general use in some regions.

---

## 6. Drivers and libraries

| Option | Notes |
|---|---|
| **RadioLib** (`jgromes/RadioLib`) | ⭐ The best general choice. First-class `SX1262` class, explicit `BUSY` handling, and a `setDio2AsRfSwitch(true)` call that matches §4.2 exactly. Arduino and ESP-IDF |
| **Semtech `LoRaMac-node`** | Reference implementation, including the SX126x HAL. Heavy but authoritative |
| **Meshtastic firmware** | Ships production-quality SX1262 support and per-region frequency/duty-cycle tables — a good reference for §5 |
| **ESP-IDF `esp_lora` / community components** | Varies in quality; check for `BUSY` handling before trusting one |
| **Zephyr** `drivers/lora/sx126x.c` | Mainline, well structured |

**Two things to verify in any SX126x driver before using it:**

1. **Does it wait on `BUSY`** before every SPI transaction? (§2)
2. **Does it call `SetDio2AsRfSwitchCtrl`?** Without it, this board cannot transmit. (§4.2)

A driver failing either test was probably ported from the SX127x.

**On the Tanmatsu specifically**, all of this runs on the **ESP32-C6**, and the application on the ESP32-P4 must reach it over `esp-hosted` SDIO (§4.1). No LoRa support appears in the Badge.Team BSP snapshot examined.

---

## 7. Alternatives

| Part | vs. E22-900M22S | When |
|---|---|---|
| **E22-900M30S** | 30 dBm | More range; much higher TX current and worse regulatory headroom |
| **E22-400M22S** | 433 MHz | The variant Ebyte/Nicolai fit on 433 MHz units |
| **E22-900T22S** | Same radio, **UART transparent transmission** | When you want bytes in and bytes out and no LoRa stack |
| **RAK3172 / RAK4630** | SX1262 + STM32WL or nRF52 in one module | When you want the stack to run *inside* the module |
| **Heltec / LilyGO SX1262 boards** | SX1262 + ESP32 | Prototyping |
| **Bare SX1262** | No external PA | Simpler RF switching (DIO2 alone); lower power |
| **SX1276 (SX127x)** | Older generation | ⚠ **Not** a drop-in — no `BUSY`, register-based rather than command-based, different driver entirely |

---

## 8. ⚠ Documentation gaps — both primary documents are missing

Neither authoritative document could be retrieved. Both attempts are fully logged in `component-download-failures.txt`.

**The Ebyte module manual.** Ebyte serves documents from `https://www.cdebyte.com/pdf-down.aspx?id=<N>` where `<N>` is an **opaque, non-guessable integer unrelated to the product**. Seven IDs were tried; every one returned a *valid PDF of the wrong product*:

| id | Actually contains |
|---|---|
| 1211 | "Ethernet to TTL E810-TTL-01 User Manual", 34 pp — ⚠ **nearly filed as the E22 manual** |
| 1210 | "XC-NK-SJ-300 Antenna Extensible Cable", 3 pp |
| 1212 | "E810-DTU(4RS1E) User Manual", 23 pp |
| 1213 | "E810-DTU", 46 pp |
| 1105 | "AM11-12W05V AC-DC Step-down Power Supply Module", 9 pp |
| 286, 1209 | ZIP archives (Altium footprint libraries) |

`https://www.cdebyte.com/products/E22-900M22S` returns 200 and 120 KB of HTML, but **the download links are injected by JavaScript** — no `pdf-down` or `.pdf` URL appears in the raw markup. A bounded ID sweep filtering on the part number was run without a confirmed hit.

**Next method to try:** drive the product page with a headless browser, or capture the XHR endpoint it calls to populate its download list.

**The Semtech SX1262 datasheet (`DS_SX1261-2`).** Semtech gates datasheets behind a Salesforce-backed portal. Six URLs tried, all returning HTML or JavaScript rather than PDF. **Next methods to try:** module-vendor mirrors (RAKwireless, Heltec, Waveshare all ship SX1262 modules and must publish it), LoRa Alliance, or Wayback.

**What this costs:** every numeric part-level figure — exact frequency range, TX/RX current, sensitivity by spreading factor, link budget, the SX126x opcode table, pin-by-pin absolute maxima — is **absent or vendor-prose only**. This record is deliberately thin on numbers rather than filling the gap with plausible values.

---

## 9. Open questions

- §4.3: the `ANT` pad's connection is unresolved in the published design files.
- §8: both primary documents are missing.
- Whether any Tanmatsu firmware drives the LoRa radio at all — none was found in the BSP snapshot.
- Whether the ESP32-C6 firmware calls `SetDio2AsRfSwitchCtrl`; if not, the board cannot transmit (§4.2). Not verifiable without the C6 firmware source.
- Module-level FCC/CE certification status and whether it survives integration.
- Nothing was verified on hardware.

---

## Manufacturer

**Chengdu Ebyte Electronic Technology Co., Ltd. (成都亿佰特电子科技有限公司)** — `www.cdebyte.com`. No vendor sourcing guide exists in this repository yet; §8 records what was learned and should seed one. The key finding for a future guide: **document IDs are opaque and the product page is JavaScript-driven**, so document discovery requires browser automation or the underlying XHR endpoint.

The radio die is from **Semtech Corporation**, whose datasheets are behind a Salesforce-backed portal (§8).

## Used By

| Device | Ref | Role |
|---|---|---|
| [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) | `U23` | LoRa radio, **owned entirely by the ESP32-C6** (§4.1) over SPI + `BUSY`/`DIO1`/`NRST`. RF switch driven by `DIO2` with a `74LVC1GU04` inverter generating `RXEN` and a 100 kΩ pull-down defaulting the front end to receive (§4.2). **E22-400M22S is fitted instead on 433 MHz units** (§1.1). See [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md), [`gaps-and-conflicts.md`](../../../devices/nicolai-electronics/tanmatsu/gaps-and-conflicts.md) |

## Related pages

- [`components/espressif/esp32-c6-wroom-1/README.md`](../../espressif/esp32-c6-wroom-1/README.md) — the host that owns this radio
- [`components/generic/ceramic-antenna/README.md`](../../generic/ceramic-antenna/README.md)
- [`components/espressif/esp32-p4/README.md`](../../espressif/esp32-p4/README.md) — reaches this radio only via `esp-hosted`

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| S1 | `tanmatsu.kicad_pcb`, `radio.kicad_sch` | Nicolai Electronics | **primary** | repository | in-tree snapshot | 2026-08-24 | `tanmatsu-hardware` @ `640805dd`, CERN-OHL-P | **All of §4** — every pad, the `74LVC1GU04` inverter, `R69`, the C6 ownership, the unconnected `ANT` | `devices/nicolai-electronics/tanmatsu/artifacts/schematics/kicad/` |
| S2 | Tanmatsu production BOM | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | CERN-OHL-P | `U23 = E22-900M22S`, LCSC C411293, **the 433 MHz variant note** | `devices/nicolai-electronics/tanmatsu/artifacts/production/bom.csv` |
| — | E22-900M22S user manual | Ebyte | primary | manual | `https://www.cdebyte.com/pdf-down.aspx?id=<opaque>` | **NOT OBTAINED 2026-08-30** | — | *Would establish* frequency range, currents, sensitivity, pinout | — |
| — | `DS_SX1261-2` SX1261/SX1262 datasheet | Semtech | primary | datasheet | Salesforce-gated | **NOT OBTAINED 2026-08-30** | — | *Would establish* the opcode set, electricals, sensitivity tables | — |
| V1 | Ebyte E22-900M22S product page | Ebyte | **community/vendor prose** | official page | <https://www.cdebyte.com/products/E22-900M22S> | 2026-08-30 | — | Band, 22 dBm, SX1262 — **unverified against a document** | — |
