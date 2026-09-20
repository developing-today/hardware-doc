# 2.4 GHz chip/ceramic antennas ×2 (unidentified)

- **Category:** onboard 2.4 GHz antennas — **two of them, one per MCU**
- **Reference designators:** `ANT1` (ESP32-S3) and `ANT2` (ESP32-U4WDH)
- **Schematic symbol name:** `CA-C03` on both
- **Owning MCUs:** one each. **`ANT1` belongs to the ESP32-S3, `ANT2` belongs to the ESP32-U4WDH. Neither MCU can use the other's antenna**
- **Research status:** matching-network topology and component values fully established. **Antenna part, manufacturer, gain, efficiency, bandwidth and physical placement are all unknown**
- **Retrieved:** 2026-08-21; both matching networks re-read pin-by-pin and coexistence analysis added 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo or community source · **[DOC]** manufacturer datasheet or official design guide · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. Two antennas, because there are two radios

This is the fact that makes this page unusual. The board carries **two complete, independent 2.4 GHz radios**:

| | `ANT1` | `ANT2` |
|---|---|---|
| Feeding MCU | **ESP32-S3R8** (`U2`) | **ESP32-U4WDH** (`U14`) |
| Schematic sheet | `2_ESP32S3-R8.png` | `3_ESP32-CHIP.png` |
| RF pin | `LNA_IN`, package pin 1 | `LNA_IN`, package pin 2 |
| Net from the pin | `WL_LNA` | `LNA_IN` |
| Radio capability | **Wi-Fi 2.4 GHz + Bluetooth LE 5** | **Wi-Fi 2.4 GHz + Bluetooth LE + Bluetooth Classic/BR-EDR** |
| Crystal | `X1` 40 MHz | `X2` 40 MHz |

Both are in the same 2.4 GHz ISM band, on the same small PCB, and **both can be transmitting at the same time.** That is the coexistence problem in §4, and it is the practically important part of this page.

Why two radios exist at all is the board's central architectural fact: the ESP32-S3 has no Bluetooth Classic, so a second, older ESP32 was added purely to provide A2DP audio. See [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md) and [classic-bluetooth](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/classic-bluetooth.md).

## 2. The matching networks — identical, and textbook

Both antennas are fed through a **π (pi) network**, and the two are component-for-component identical **[SCH sheets 2 and 3]**:

### 2.1 `ANT1` — ESP32-S3

```
U2 pin 1 (LNA_IN) ──── WL_LNA ────┬──── L1 (2 nH) ────┬──── ANT1 (CA-C03)
                                  │                   │
                                 C1 (2.2 pF)         C2 (2.2 pF)
                                  │                   │
                                 GND                 GND
```

### 2.2 `ANT2` — ESP32-U4WDH

```
U14 pin 2 (LNA_IN) ──── LNA_IN ───┬──── L5 (2 nH) ────┬──── ANT2 (CA-C03)
                                  │                   │
                                 C46 (2.2 pF)        C45 (2.2 pF)
                                  │                   │
                                 GND                 GND
```

| Element | `ANT1` | `ANT2` | Role |
|---|---|---|---|
| Shunt C, chip side | `C1` 2.2 pF | `C46` 2.2 pF | |
| Series L | `L1` 2 nH | `L5` 2 nH | |
| Shunt C, antenna side | `C2` 2.2 pF | `C45` 2.2 pF | |
| Antenna | `ANT1` `CA-C03` | `ANT2` `CA-C03` | |

**Both networks are fully populated** — all three positions have components fitted, none is a 0 Ω link or a DNP. That is the normal outcome after a real tuning exercise; a board that had never been tuned would typically ship with a 0 Ω series link and unpopulated shunts.

Note also the separate supply chokes, which are *not* part of the matching network but are easily confused with it: `L2` 2 nH on the S3's `VDD3P3` (pins 3/4) and `L6` 2 nH on the U4WDH's `VDD3P3` **[SCH]**. Those are RF decoupling on the supply, and Espressif's hardware design guidelines call for them.

### 2.3 Why a π network

**[INF]** A π network gives two degrees of freedom, which is what you need to move an arbitrary antenna impedance to 50 Ω — it can transform both the real and the imaginary parts. At 2.4 GHz, 2 nH is about `j30 Ω` and 2.2 pF is about `−j30 Ω`, so these are modest, sensible corrections rather than a heroic transformation. That in turn suggests the raw antenna impedance is not far from 50 Ω, which is what you would expect from a commercial chip antenna on a reference layout.

**The specific values are tuned to this PCB stack-up, this ground plane and this enclosure.** They are not transferable, and they are not adjustable without a VNA (§6).

## 3. What is unknown

| Unknown | Note |
|---|---|
| **Antenna manufacturer and part number** | `CA-C03` is the schematic *symbol* name. It resembles the naming style of several Chinese chip-antenna vendors but **has not been matched to a catalogue part** |
| Antenna type | Ceramic chip? Stamped metal? PCB trace with a chip-antenna footprint? **Unknown** — the schematic symbol is drawn as a generic antenna |
| **Peak gain and efficiency** | Unknown. This is the number that determines range |
| Radiation pattern | Unknown. Matters a great deal here — see §4.3 |
| Bandwidth / return loss | Unknown |
| **Physical placement on the PCB** | **Unknown.** No PCB layout, Gerbers or assembly drawing are published **[SCH — the archive is five raster PNGs]** |
| **Separation distance between `ANT1` and `ANT2`** | **Unknown, and this is the key coexistence parameter.** §4 |
| Keepout compliance | Unknown, because placement is unknown. §5 |
| Effect of the CNC **metal** knob body | **Unknown, and potentially significant.** §4.3 |
| Whether the board has been certified (FCC/CE) with a measured pattern | Unknown |

**None of this is recoverable from the published archive.** Closing it needs a board photograph (for the antenna part and placement), a mechanical drawing (for the enclosure interaction), or measurement.

## 4. ⚠ Coexistence: two radios, one small board

This is the section worth reading even if you skip the rest.

### 4.1 The problem

Both radios operate in **2400–2483.5 MHz**. Both can transmit. They are on the same PCB, share a ground plane, and are separated by an unknown but necessarily small distance — the board is a ~40 mm puck.

Unlike a single ESP32, where Wi-Fi and Bluetooth share one radio and Espressif's **internal coexistence arbiter** time-slices them, **these two chips have no coexistence mechanism whatsoever.** They cannot see each other. There is no shared PTA (packet traffic arbitration) signal, no coexistence GPIO pair, and no arbitration in software — the only link between them is a two-wire UART with an undocumented protocol **[SCH, and see [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md)]**.

### 4.2 What actually goes wrong

**[INF]**, reasoning from RF fundamentals rather than from measurement — **no coexistence measurements for this board exist in any retained source**:

| Effect | Mechanism | Symptom |
|---|---|---|
| **Receiver desensitisation** | One radio transmits at up to +20 dBm a few millimetres from the other's LNA input. Even 20–30 dB of antenna isolation leaves −10 dBm at the victim's input — enormously above its −90 dBm sensitivity floor | The idle radio's throughput and range collapse whenever the other transmits |
| **Blocking / front-end compression** | The victim's LNA is driven into compression by the aggressor's carrier | Packet loss, retries, not just reduced sensitivity |
| **Channel overlap** | Wi-Fi channels are 20 MHz wide; BLE and BR-EDR hop across the whole band | Unavoidable overlap in time and frequency at some point |
| **Harmonic and spurious coupling** | Shared ground plane and supply rails | Second-order, but real on a dense board |

The most likely user-visible manifestation is **audio dropouts on the Bluetooth Classic link when the S3's Wi-Fi is active**, or **Wi-Fi throughput falling off when audio is streaming**. Since the factory product's headline use case is exactly "Bluetooth audio player plus Wi-Fi-connected display", this is not a hypothetical.

### 4.3 The metal knob body

The device's outer body is CNC-machined **metal** **[WEB]**. A metal enclosure around a 2.4 GHz antenna:

- **Detunes it**, shifting the resonance and degrading return loss
- **Distorts the radiation pattern**, often severely, creating deep nulls in particular directions
- Can, depending on geometry, either *increase* isolation between the two antennas (a shield between them) or *decrease* it (a shared conductive path coupling them)

**[INF]** The matching-network values (§2) were presumably tuned with the enclosure in place, since that is the only way to get a meaningful result — but this is not documented, and the possibility that they were tuned on a bare board cannot be excluded.

**Practical consequence:** if you observe direction-dependent range on this device, that is expected behaviour for a metal-bodied radio product, not a fault.

### 4.4 Mitigations available to you

Ordered by effectiveness:

1. **Turn one radio off.** The most effective mitigation by a wide margin. If you do not need Bluetooth Classic, flash the ESP32-U4WDH with a deep-sleep stub — which also saves **~50 mA** of idle current **[SRC, community measurement]**. See [development.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/development.md#the-secondary-mcu-costs-50-ma-if-you-leave-it-alone) and [lipo-102035 §5.2](../lipo-102035/README.md#52-the-headline-finding). **This is the single best thing you can do for both RF performance and battery life.**
2. **Pin the S3's Wi-Fi to a channel far from where the BT link is active.** Only partially helps — BR-EDR hops across the whole band and uses adaptive frequency hopping to avoid *persistent* interferers, which a fixed Wi-Fi channel at least gives it a chance to learn.
3. **Coordinate transmission over the inter-MCU UART.** In principle you could build your own PTA: have the S3 tell the U4WDH before a Wi-Fi burst, and vice versa. **In practice this is impractical** — the UART protocol is undocumented, the U4WDH has no published source, and the latency of a UART round trip is orders of magnitude worse than the microsecond-scale arbitration a real PTA needs. Mentioned for completeness; do not attempt it.
4. **Reduce Wi-Fi TX power** with `esp_wifi_set_max_tx_power()`. Trades your own range for the other radio's sensitivity. Sometimes the right call in a fixed-location device.
5. **Duty-cycle the radios in your application.** Do the Wi-Fi work in bursts between audio buffers rather than continuously.

### 4.5 What is *not* available

- **No hardware coexistence interface exists.** Neither chip's PTA/coexistence pins are routed **[SCH]**.
- **No antenna diversity.** Each MCU has exactly one antenna, hard-wired.
- **No external antenna connector.** No U.FL/IPEX footprint appears in either matching network **[SCH]**. You cannot substitute an external antenna without rework.

## 5. Keepout and layout — what the rules are, and why compliance is unverifiable

Espressif's *ESP32-S3 Hardware Design Guidelines* and the ESP32 equivalent (both retained locally) specify **[DOC]**:

| Requirement | Rule |
|---|---|
| Antenna keepout | **No copper on any layer** beneath or immediately around the antenna — ground plane, traces and pours all excluded |
| Board-edge placement | Antenna at a board edge or, better, a corner |
| Clearance to other components | Keep metal, batteries, LCDs and shields away from the antenna region |
| RF trace | 50 Ω controlled impedance, as short as possible, with a solid reference plane under it |
| Matching network placement | Immediately adjacent to the chip's RF pin |
| Ground stitching | Vias along the RF trace's flanking ground |

**Whether this board complies is unverifiable**, because **no PCB layout, Gerbers or stack-up are published** **[SCH — five raster schematic PNGs only]**.

What can be said **[INF]**:

- The device is a small round puck containing a **metal body**, a **360 × 360 LCD**, a **battery**, a **microSD socket** and **two** antennas. That is an extremely crowded RF environment.
- Fitting two antennas with proper keepouts and useful mutual isolation into that volume is genuinely hard.
- Both matching networks being fully populated (§2) suggests a real tuning effort was made.
- **Do not assume good isolation.** Assume it is poor until measured.

If you are designing a derivative board, the two antennas should be placed as far apart as the outline allows and, ideally, with orthogonal polarisation — that is usually worth 10–15 dB of isolation for free.

## 6. If you need to re-tune

Only relevant if you are reworking or respinning. **Do not change these components speculatively.**

1. **You need a VNA.** Antenna matching cannot be done by ear, by trial substitution, or by measuring range. A cheap 2.4 GHz-capable VNA is sufficient.
2. **Measure in the final enclosure.** The metal body dominates. A bare-board measurement is close to worthless here.
3. **Measure both antennas, and measure `S21` between them.** The transmission between the two ports *is* the isolation number, and it is the one that predicts the §4 problems. Anything worse than about −20 dB is a warning sign.
4. **Keep the π topology.** The three positions give you the freedom you need; converting to an L network throws that away.
5. **After re-tuning, re-verify regulatory compliance.** Changing the matching network changes radiated power and spurious emissions. Any prior certification does not carry over.

## 7. Pitfalls

1. **Do not assume the two radios are independent in practice.** They are electrically independent and RF-coupled. §4.
2. **Do not attempt to build a software coexistence scheme over the inter-MCU UART.** §4.4 item 3.
3. **Do not change `C1`/`L1`/`C2` or `C45`/`L5`/`C46` without a VNA.** §6.
4. **Do not confuse the supply chokes `L2`/`L6` with the matching networks.** §2.2.
5. **Do not expect an external antenna option.** No U.FL footprint. §4.5.
6. **Expect direction-dependent range.** Metal body. §4.3.
7. **If range is poor, check whether the other MCU is transmitting** before suspecting the antenna. §4.2.

## 8. Open questions

Everything in §3, prioritised:

| Question | Priority | Method |
|---|---|---|
| **Isolation (`S21`) between `ANT1` and `ANT2`** | **Highest** — it predicts every coexistence symptom | VNA, two-port measurement on a real board |
| Physical placement and separation | High | Board photograph |
| Antenna part number and gain | Medium | Board photograph, then a vendor catalogue search on the marking |
| Whether the matching was tuned with the metal body fitted | Medium | Compare bare-board and assembled return loss |
| Measured Wi-Fi/BT throughput degradation when both radios are active | High, and directly useful | Iperf on the S3 while streaming A2DP to the U4WDH |
| Regulatory certification documents | Low | Vendor request |

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `ANT1` on the ESP32-S3, `ANT2` on the ESP32-U4WDH

## Related pages

- [Dual-MCU architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md) — why there are two radios at all
- [Classic Bluetooth guide](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/classic-bluetooth.md) — the use case that puts both radios on air simultaneously
- [espressif/esp32-s3r8](../../espressif/esp32-s3r8/README.md) — `ANT1`'s radio
- [espressif/esp32-u4wdh](../../espressif/esp32-u4wdh/README.md) — `ANT2`'s radio, and the deep-sleep stub that turns it off
- [generic/lipo-102035](../lipo-102035/README.md) — why turning the second radio off is also the biggest battery win
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Board schematic sheet 2 — `ANT1`, `C1`/`L1`/`C2`, `WL_LNA`, and the `L2` supply choke | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Board schematic sheet 3 — `ANT2`, `C46`/`L5`/`C45`, `LNA_IN`, and the `L6` supply choke | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/3_ESP32-CHIP.png` |
| ESP32-S3 Hardware Design Guidelines — antenna keepout and RF layout rules (§5) | https://www.espressif.com/sites/default/files/documentation/esp32-s3_hardware_design_guidelines_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-hardware-design-guidelines.pdf` |
| ESP32 Hardware Design Guidelines — same rules for the secondary MCU | https://www.espressif.com/sites/default/files/documentation/esp32_hardware_design_guidelines_en.pdf | 2026-08-21 | `../../espressif/esp32-u4wdh/artifacts/esp32-hardware-design-guidelines.pdf` |
| ESP32-S3 datasheet — RF characteristics and TX power | https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` |
| ESP32 datasheet — RF characteristics for the secondary MCU | https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf | 2026-08-21 | `../../espressif/esp32-u4wdh/artifacts/esp32-datasheet.pdf` |
| Community measurement of the ESP32-U4WDH's idle draw (relevant to §4.4 mitigation 1) | `svwhisper/lyngdorf-secondary-sleep`, catalogued in [examples/catalog.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/catalog.md) | 2026-08-23 | retained under `.../examples/selected/` |
| Waveshare product page — the metal body and the wireless claims | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
