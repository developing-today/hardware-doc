# PaperMono — FCC certification, certified radio parameters and what the exhibits show

> FCC ID **`2AN3WM5PAPERMONO`** · granted **2026-08-12** · mined **2026-09-20**
> from the eleven exhibits filed at
> [`artifacts/certification/`](artifacts/certification/README.md).
> Every claim below cites the exhibit and page it came from. Nothing here is
> vendor prose; where the vendor and the filing disagree, both are given.

## Why this document exists, and what it overturns

Before this pass every PaperMono document in the repository said the same thing:

> "No FCC/CE/TELEC identifier appears anywhere on M5Stack's site —
> `/en/certification` returns zero matches for both `PaperMono` and `C153`. That
> is a verified negative, not a failed search."
> — [`README.md`](README.md) §Identity and variants

**The verified negative was correct and the conclusion drawn from it was wrong.**
M5Stack does not publish a certification identifier for this board. The board is
nevertheless certified, under two grants issued on the same day, and the exhibits
are public. `/en/certification` was the wrong place to look; the FCC grantee
database was never searched.

This is recorded as a **refuted hypothesis**, not quietly corrected:
[`gaps-and-conflicts.md` G2](gaps-and-conflicts.md#g2--no-certification-identifiers-exist-on-the-vendor-site)
is closed by this document, and the same correction applies to
[`features/lora.md` §7](features/lora.md), [`features/wifi-and-bluetooth.md`](features/wifi-and-bluetooth.md),
[`features/nfc.md`](features/nfc.md), [`coverage.md`](coverage.md),
[`compatibility-and-status.md`](compatibility-and-status.md),
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) and
[`product-history-and-family.md`](product-history-and-family.md).

The general lesson is already written up in
[`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md):
*the absence of a printed mark, or of a vendor page, is not the absence of a grant.*

## Contents

| § | What is in it |
|---|---|
| [1. Grant identity](#1--grant-identity) | FCC ID, grantee, equipment classes, dates, lab, TCB |
| [2. The certified radio envelope](#2--the-certified-radio-envelope) | Bands, channels, conducted power per mode, duty cycle, what is *not* stated |
| [3. Antenna specification](#3--antenna-specification) | RSY-E8131, gain and efficiency tables, physical placement, the replaceability question |
| [4. RF exposure and SAR](#4--rf-exposure-and-sar) | Measured SAR, 0 mm separation, exclusions, simultaneous transmission |
| [5. The label exhibit is an architecture diagram](#5--the-label-exhibit-is-an-architecture-diagram) | Full transcription — rails, regulators, I²C addresses, GPIO map, MIC number |
| [6. What the internal photographs show](#6--what-the-internal-photographs-show) | Part-by-part, legible vs illegible, with confirmations and one contradiction |
| [7. What the user manual adds](#7--what-the-user-manual-adds) | The FCC-filed spec table and the behaviours it reveals |
| [8. Identifiers, SKUs and model strings](#8--identifiers-skus-and-model-strings) | Every identifier the filing carries |
| [9. Constraints this imposes](#9--constraints-this-imposes-on-anyone-building-on-the-board) | What the grant actually permits |
| [10. Conflicts advanced or opened](#10--conflicts-advanced-or-opened-by-this-filing) | C1, C2, C18, and one new one |
| [11. Unverified and not fetched](#11--unverified-not-read-and-not-fetched) | The honest limits of this pass |

---

## 1 — Grant identity

Two grants were issued on the same day under one FCC ID, because the board has a
digital-modulation transmitter and a separate 13.56 MHz emitter.

| Field | Value | Evidence |
|---|---|---|
| FCC ID | **`2AN3WM5PAPERMONO`** | grant, both applications; SAR report p. 1; label exhibit |
| Grantee code | `2AN3W` | filing index |
| Product code | `M5PAPERMONO` | filing index |
| Grantee / applicant | M5Stack Technology Co.,Ltd, Block A10, Expo Bay South Coast, Fuhai Street, Bao'an District, Shenzhen, Guangdong, China | grant; SAR report p. 1 |
| Applicant FRN | `0026912345` | filing index |
| Equipment class, grant 1 | **Digital Transmission System** (`DTS`) | grant, application `TRHAipRYjij4wjjVV4V9JA==` |
| Equipment class, grant 2 | **Part 15 Low Power Communication Device Transmitter** (`DXX`) | grant, application `cV4RemadFogfsatkKapmuQ==` |
| FCC rule part | **15C** on every frequency row of both grants | both grants |
| Date of grant | **2026-08-12** | both grants |
| Application dated | **2026-08-12** | both grants |
| Application purpose | Original Equipment | both applications |
| Device description / notes | `M5PaperMono` | both grants |
| Test firm | **Shenzhen Accurate Technology Co., Ltd.**, Floor 1 KuMaKe Building, Guangming District, Shenzhen — **A2LA accreditation 4297.01** | SAR report pp. 1, 7 |
| TCB | **Bay Area Compliance Laboratories Corp.**, 1274 Anvilwood Avenue, Sunnyvale CA 94089 | both grants |
| Responsible party | Jimmy Lai, `JimmyLai@M5Stack.com` | filing index |
| US agent | Benjamin Kaur, Iconsigh (`iconsigh.com`) | filing index |
| Composite device | **Yes** | filing index |
| Modular equipment | Does not apply | filing index |
| Short-term confidentiality | No | filing index |
| Long-term confidentiality | **Yes** — Schematics, Block Diagram, Operation Description permanently withheld | filing index |

### The certification timeline, against the product timeline

The filing dates slot cleanly into the timeline already in
[`product-history-and-family.md`](product-history-and-family.md) and extend it
backwards and forwards:

| Date | Event | Evidence |
|---|---|---|
| 2025-09-13 (or 2025-12-13) | NFC sub-board FPC printed `Paper_Mono_NFC V0.2` | internal photos p. 4 — **middle digits not legible**, see §6 |
| 2025-12-22 | Main board silkscreen date code `…251222`, revision **`V0.6`** | internal photos p. 2 |
| 2026-02-01 | Antenna vendor specification `RSY-E8131` released at V3.0 | antenna spec p. 1 |
| 2026-05-22 | Main schematic V0.6.2 *(already in the record)* | schematic filename |
| 2026-07-14 | Sample received by the SAR laboratory | SAR report p. 1 |
| **2026-07-15** | **SAR testing performed** — by Devon Liang, Jack Yang, Ryse Chai | SAR report pp. 5, 25 |
| 2026-07-25 | SAR report `2604T59815E-SA` issued, revision 0 | SAR report pp. 1, 4 |
| **2026-08-12** | **Both grants issued** | grants |
| 2026-08-20 / 21 | Documentation published; store published *(already in the record)* | vendor |

**The device was certified nine days before it went on sale**, and the sample
was in the laboratory a month before that. The board silkscreen is dated
2025-12-22 — roughly eight months before launch — which is the earliest hardware
date now in evidence anywhere in this record.

---

## 2 — The certified radio envelope

### Frequency rows as granted

Directly from the two grant certificates. The note on grant 1 states **"Output
power listed is peak conducted."**

| Rule part | Frequency range (MHz) | Output (W) | Output (dBm) | Mode this corresponds to |
|---|---|---:|---:|---|
| 15C | 2402.0 – 2480.0 | 0.0036 | **5.56** | Bluetooth LE |
| 15C | 2412.0 – 2462.0 | 0.2523 | **24.02** | Wi-Fi 802.11b/g/n20 |
| 15C | 2422.0 – 2452.0 | 0.2547 | **24.06** | Wi-Fi 802.11n40 |
| 15C | 903.0 – 914.9 | 0.0133 | **11.24** | LoRa |
| 15C | 13.56 – 13.56 | *(blank)* | — | NFC |

dBm columns are computed from the granted watts and are therefore `inferred`,
not transcribed.

### Conducted power actually measured

SAR report p. 21 gives the applicant's declared tune-up targets; p. 22 gives what
the laboratory measured. Both are reproduced verbatim.

**Declared maximum target output power** *(SAR report p. 21)*

| Mode / band | Low ch. | Middle ch. | High ch. |
|---|---:|---:|---:|
| Wi-Fi 2.4G (802.11b) | 17.5 dBm | 17.5 dBm | 17.5 dBm |
| Wi-Fi 2.4G (802.11g/n) | 16.5 dBm | 16.5 dBm | 16.5 dBm |
| BLE | 6.0 dBm | 6.0 dBm | 6.0 dBm |
| **LoRa** | **11.5 dBm** | **11.5 dBm** | **11.5 dBm** |

**Measured conducted output** *(SAR report p. 22)*

| Mode | Channel (MHz) | Data rate | Duty cycle | Average output |
|---|---:|---|---:|---:|
| 802.11b | 2412 | 1 M | 99.80 % | 16.98 dBm |
| 802.11b | 2437 | 1 M | 99.80 % | 17.05 dBm |
| 802.11b | **2462** | 1 M | 99.80 % | **17.17 dBm** ← band max |
| 802.11g | 2412 / 2437 / 2462 | 6 M | not stated | 16.11 / 15.96 / 16.22 dBm |
| 802.11n20 | 2412 / 2437 / 2462 | MCS0 | not stated | 15.11 / 15.15 / 15.43 dBm |
| 802.11n40 | 2422 / 2437 / 2452 | MCS0 | not stated | 15.02 / 14.96 / **15.51** dBm |
| BLE 1M | low / mid / high | — | — | 4.12 / **5.56** / 5.30 dBm |
| BLE 2M | low / mid / high | — | — | 4.03 / 5.50 / 5.30 dBm |
| **LoRa** | low / mid / high | — | — | **11.24** / 11.20 / 11.18 dBm *(peak, not average)* |

Three things are worth saying plainly about this table.

**The Wi-Fi channel plan is narrower than the ESP32-S3's capability.** Only
channels 1–11 are certified (2412–2462 MHz), and 40 MHz operation is certified
only on 2422–2452 MHz. This is the ordinary US channel plan, but it is now a
*documented* constraint on this board rather than an assumption.

**The LoRa band as certified is 903.0–914.9 MHz — not 868–923 MHz.** Every other
document in this record, including [`features/lora.md`](features/lora.md) and the
[`stamp-lora-1262`](../../../components/m5stack/stamp-lora-1262/README.md)
component record, quotes M5Stack's "868–923 MHz" hardware capability. The grant
authorises **11.9 MHz of that range** for US operation. The user manual filed
with the FCC contradicts itself on exactly this point: its prose (p. 2) says
"supporting the 868–923 MHz band" while its own specification table (p. 3) says
"LoRa 903.0–914.9MHz". This closes the "no regional band plan" half of
[`features/lora.md` §7](features/lora.md) **for the United States only** — no CE,
IC, RCM or SRRC record was located in this pass.

**The grant's Wi-Fi watts and the SAR report's dBm do not agree, and that is
expected.** The grant lists 24.02 dBm peak conducted where the SAR report
measures 17.17 dBm average. For BLE (5.56 dBm) and LoRa (11.24 dBm) the two
match to the hundredth of a dB. The ~7 dB Wi-Fi gap is consistent with the
peak-to-average ratio of an OFDM/DSSS waveform, but **the reconciling figures are
in the Wi-Fi test report, which was not fetched** (§11). Do not treat 24 dBm as a
transmit power you can configure.

### Duty cycle

| Mode | Duty cycle | Evidence |
|---|---|---|
| 802.11b | **99.80 %** | SAR report p. 22; scaling factor 1.002 on p. 26 |
| 802.11g / n20 / n40 | **not stated** — the cell reads `/` | SAR report p. 22 |
| BLE | not stated | — |
| **LoRa** | **not stated anywhere in the fetched exhibits** | — |
| NFC | not stated | — |

The 802.11b duty cycle is the only one given, and the report defers even that to
a document it does not include: *"The Duty cycle of 802.11b, please refer to the
report of `2604T59815E-RF-00B`"* (p. 22). **There is no certified LoRa duty-cycle
limit in evidence**, which matters because sub-GHz duty cycle is the usual
regulatory constraint on a LoRa deployment. Unresolved.

### Simultaneous transmission

*(SAR report p. 29)*

| Transmitter combination | Simultaneous? | Hotspot? |
|---|:-:|:-:|
| WLAN + LoRa + NFC | **✓** | ✗ |
| BLE + LoRa + NFC | **✓** | ✗ |
| WLAN + BLE | **✗** | ✗ |

**Wi-Fi and BLE are declared mutually exclusive on this board** — they cannot
transmit simultaneously. That is a coexistence property of the ESP32-S3's single
2.4 GHz radio rather than a board decision, but it is now a *certified* statement
and belongs in [`resources-and-conflicts.md`](resources-and-conflicts.md)
alongside the other simultaneous-use limits. LoRa and NFC may run concurrently
with either.

---

## 3 — Antenna specification

The "Antenna Specification" exhibit is not a laboratory document at all — it is
the antenna vendor's own product datasheet, filed as a test report.

| Field | Value | Evidence |
|---|---|---|
| Antenna supplier | **Shenzhen Rongshengyuan Technology Co., Ltd**, 703 No. 55 Ainan Road, Longdong Community, Baolong Street, Longgang District, Shenzhen | antenna spec p. 1 |
| Customer | "M5" | antenna spec p. 1 |
| Part number | **`RSY-E8131`** | antenna spec p. 1 |
| Document version / date | **V3.0, 2026-02-01**, author Yang Ye | antenna spec p. 1 |
| Working bands | 868 / 915 / 2.4 GHz | antenna spec p. 1 |
| Bandwidth | 50 MHz | antenna spec p. 2 |
| Input impedance | 50 Ω | antenna spec p. 2 |
| VSWR | **< 4** | antenna spec p. 2 |
| Headline gain | **−4.57 dBi** | antenna spec p. 2 |
| Polarisation | Vertical | antenna spec p. 2 |
| Connection | **IPEX4** | antenna spec p. 2 |
| Element size, sub-GHz | **52 × 7.7 mm** | antenna spec pp. 2, 11 |
| Element size, 2.4 GHz | **14.42 × 5.04 mm** | antenna spec pp. 2, 11 |
| Operating / storage temperature | −30 … +70 °C | antenna spec p. 2 |
| Colour | black | antenna spec p. 2 |
| Matching network | series `0 Ω` to the antenna, `5.6 nH` shunt to ground, one `NC` position | antenna spec p. 4 (schematic fragment) |

The single headline **−4.57 dBi** on p. 2 is the *best* figure in the sub-GHz
sweep, not a band-wide number. The measured table is considerably worse at the
edges:

**Sub-GHz gain and efficiency** *(antenna spec p. 4, §2.5)*

| Freq (MHz) | Gain (dBi) | Efficiency (dB) | Efficiency (%) |
|---:|---:|---:|---:|
| 860 | −6.72 | −9.36 | 11.59 |
| 870 | −5.92 | −8.58 | 13.87 |
| 880 | −4.92 | −7.90 | 16.23 |
| **890** | **−4.57** | −7.62 | **17.31** ← the datasheet headline |
| 900 | −5.51 | −8.07 | 15.58 |
| **910** | **−5.00** | −7.98 | 15.92 |
| 920 | −6.13 | −9.34 | 11.65 |

**2.4 GHz gain and efficiency** *(antenna spec p. 7, §4.4)*

| Freq (MHz) | Gain (dBi) | Efficiency (dB) | Efficiency (%) |
|---:|---:|---:|---:|
| 2400 | −0.899 | −7.011 | 19.90 |
| 2410 | −0.423 | −6.646 | 21.65 |
| 2420 | −0.487 | −6.821 | 20.79 |
| 2430 | −0.940 | −7.082 | 19.58 |
| 2440 | −0.355 | −6.681 | 21.47 |
| 2450 | −0.125 | −6.260 | 23.66 |
| 2460 | **+0.157** | −6.184 | 24.08 |
| 2470 | +0.519 | −5.895 | 25.73 |
| 2480 | +0.737 | −5.666 | 27.12 |
| 2490 | +0.838 | −5.415 | 28.74 |
| 2500 | +0.666 | −5.320 | 29.38 |

### What this means in practice

**The sub-GHz antenna is poor, and the LoRa link budget in this record should be
revised downward.** Total radiated efficiency is **11.6 – 17.3 %** across
860–920 MHz — that is 7.6 to 9.4 dB of loss. At the certified band centre
(~909 MHz) gain is about **−5 dBi**. Combined with the 11.2 dBm conducted peak,
radiated power is around **+6 dBm EIRP** — `inferred`, because **no EIRP figure
for LoRa appears in any fetched exhibit**.

That is a small radio. Any range expectation in
[`features/lora.md`](features/lora.md) or
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) that
assumes a nominal 0 dBi antenna is optimistic by roughly 5 dB, which is a factor
of ~1.8 in free-space distance. The record has never carried a range measurement
([`coverage.md`](coverage.md) marks LoRa range `not-tested`), so nothing is
contradicted — but the ceiling is now known to be lower than a naive estimate.

**The 2.4 GHz antenna is unremarkable and slightly better at the top of the
band.** Efficiency 19.9 – 27.1 % across 2400–2480 MHz; gain crosses 0 dBi around
2455 MHz. Note the sweep is *best* at 2490–2500 MHz, outside the band — the
element is tuned marginally high.

### Antenna placement, and the replaceability question

*(SAR report p. 23, "Antennas Location", EUT front view — drawn **portrait**,
101 mm tall × 62 mm wide; corroborated by internal photos pp. 5–7)*

| Antenna | Location in the portrait front view |
|---|---|
| **LoRa** | a full-width strip across the **top edge** |
| **NFC** | a large rounded region occupying the **lower ~40 % of the front face** |
| **WLAN / BLE** | a narrow vertical strip in the **bottom-right corner**, inboard of the NFC region |

Mind the orientation. The SAR diagram is portrait; the external-photo and
label-location exhibits show the device **landscape**, with the NFC panel on the
right-hand ~35 % of the face. Rotating the landscape view 90° counter-clockwise
maps the NFC region to the bottom, which reconciles the two — the same NFC
daughterboard, drawn against two different conventions for "up".

The internal photographs place these physically (§6), photographed with the rear
housing open and the device lying **landscape**:

- **LoRa** — a **52 × 7.7 mm FPC strip** bonded along one long edge of the rear
  housing, silkscreened `Paper Mono V3.0`, reaching the Stamp LoRa module through
  a coaxial pigtail and an **IPEX/U.FL connector** (pp. 6, 7).
- **NFC** — a **printed loop on a separate FPC daughterboard** carrying its own
  reader IC and matching network, bonded into the opposite portion of the
  housing, behind the black `NFC` panel visible from outside (pp. 4, 6).
- **Wi-Fi / BLE** — at the **edge of the main PCB itself**, annotated
  "BLE 2.4G WiFi Ant" on p. 5. Not a separate FPC assembly.

The main board occupies only about half the enclosure; a **copper-foil shield**
covers it, with the battery above (p. 4).

**On "no user-replaceable antenna": the filing does not say that in those
words.** What it does say:

- *"Antenna Type(s): **Internal Antenna**"* — SAR report p. 5.
- *"The antenna(s) used for this transmitter **must not be co-located with any
  other transmitters**, except in accordance with FCC multi-transmitter product
  procedures."* — grant note, grant 1.
- The user manual's FCC Caution (p. 10): *"Any Changes or modifications not
  expressly approved by the party responsible for compliance could void the
  user's authority to operate the equipment."*

The customary §15.203 "unique antenna connector / non-standard connector"
language **does not appear in any of the eleven exhibits fetched**; it may be in
one of the four unfetched test reports. So the correct statement is: *the device
is certified with fixed internal antennas, and changing them voids the
authorisation* — which follows from the Caution — **not** that a specific
anti-replacement construction was certified.

**And there is a real IPEX connector inside.** The LoRa antenna is detachable at
a U.FL connector (internal photos pp. 3, 6, 7), and `RSY-E8131` is specified with
an **IPEX4** interface (antenna spec p. 2). It is not user-accessible without
opening the case, but it is a standard connector, and anyone substituting an
antenna there is outside the grant.

---

## 4 — RF exposure and SAR

SAR report `2604T59815E-SA`, 34 pp, revision 0, issued 2026-07-25.

### Headline results

*(SAR report p. 2; carried onto both grant certificates)*

| Mode | Metric | Max reported SAR | Limit |
|---|---|---:|---:|
| Wi-Fi 2.4G | 1 g body SAR | **0.19 W/kg** | 1.6 W/kg |
| Simultaneous | 1 g body SAR | **0.55 W/kg** | 1.6 W/kg |

The grant note repeats these verbatim: *"The highest reported SAR for body-worn
accessory and simultaneous transmission use conditions is 0.19 W/kg, and
0.55 W/kg, respectively."* Both are comfortably below limit — the worst case uses
**34 %** of the allowance.

### The test separation distance, and what it implies about intended use

> *"In this case the EUT (Equipment Under Test) is set **0 mm** away from the
> phantom, the test distance is **0 mm** for body."*
> — SAR report p. 18

This is the most informative single line in the filing. The standard body-worn
allowance is 15 mm, and up to 25 mm is permitted (p. 18). M5Stack certified at
**zero** — the device pressed directly against the phantom — and did so on **all
six faces**: front, back, left, right, top and bottom (p. 26; setup photographs
in the EUT test-position exhibit, 4 pp).

Three consequences follow:

1. **The certified posture is "held in the hand or against the body, in direct
   contact."** That is an e-reader / access-badge posture, and it matches the
   product: a 62 × 101 × 8 mm slab with a front-lit e-paper panel, a 1150 mAh
   cell and an NFC loop on the face you present to a reader. Compare the
   [Cardputer](../cardputer-v1.0/README.md) and
   [DinMeter](../dinmeter/README.md) filings, which use MPE at 20 cm — a
   fixed-installation posture. The PaperMono is certified as a **portable**
   device (SAR report p. 5, "Device Type: Portable").
2. **There is no separation-distance caveat to honour.** A 0 mm result is the
   most permissive possible; no enclosure, spacer or "keep 15 mm from the body"
   instruction is load-bearing.
3. **Exposure category is Population/Uncontrolled** (p. 5) — the consumer limit,
   1.6 W/kg over 1 g, not the 8.0 W/kg occupational limit (p. 6).

The report also records `Body-Worn Accessories: None` and `Proximity Sensor:
None` (p. 5). The grant's standard restriction therefore applies: body-worn use
is *"restricted to belt clips, holsters or similar accessories that have **no
metallic component** in the assembly."*

### Measured Wi-Fi SAR by face

*(SAR report p. 26 — 802.11b @ 2437 MHz, 17.05 dBm measured, scaled to the
17.5 dBm tune-up target by factor 1.109 and by duty-cycle factor 1.002)*

| EUT position (0 mm) | Measured 1 g SAR | Scaled 1 g SAR |
|---|---:|---:|
| Body front | 0.129 W/kg | 0.14 W/kg |
| **Body back** | **0.167 W/kg** | **0.19 W/kg** ← worst case |
| Body left | 0.019 W/kg | 0.02 W/kg |
| Body right | 0.066 W/kg | 0.07 W/kg |
| Body top | 0.00821 W/kg | 0.01 W/kg |
| Body bottom | 0.063 W/kg | 0.07 W/kg |

Only the middle channel was measured; per the report's own note 1, testing other
channels is optional once SAR is below half the limit.

**The back is the hot face, and by a wide margin** — 20× the top face. The
Wi-Fi/BLE antenna is on the bottom edge of the main PCB, and the main PCB sits
against the rear housing behind a copper shield (internal photos p. 4). The
practical reading: this device radiates most strongly through its back, which is
the face you would hold against a pocket or a desk.

The single scan plot filed *(SAR scan plots exhibit, plot `1#`)* corresponds to
this worst case: Body Back, 802.11b mid channel, 2437 MHz, duty cycle 1:1.002,
area scan 13×14, peak SAR extrapolated 0.321 W/kg, SAR(1 g) 0.167 W/kg,
SAR(10 g) 0.106 W/kg, power drift 0.01 dB. DUT serial `3MFY-1`.

### SAR exclusions — BLE, LoRa and NFC were never measured

Only Wi-Fi was measured. The other three qualified for test exclusion under
KDB 447498 D01 v06 §4.3, and the report shows the arithmetic.

**Standalone exclusion** *(SAR report p. 24)*

| Mode | Freq (MHz) | Power | Distance | Calculated | Threshold (1 g) | Excluded? |
|---|---:|---:|---:|---:|---:|:-:|
| BLE | 2480 | 6 dBm / 3.98 mW | 0 mm | 1.3 | 3 | **yes** |
| LoRa | 914.9 | 11.5 dBm / 14.13 mW | 0 mm | 2.7 | 3 | **yes** |

LoRa clears the exclusion threshold at **2.7 against a limit of 3.0** — a 10 %
margin. Any tune-up above 11.5 dBm would push LoRa over the line and require
actual SAR measurement. That is a hard ceiling on this design, not a
configuration choice.

**Estimated standalone SAR, used for the simultaneous case** *(p. 24)*

| Mode | Freq (MHz) | Pavg | Distance | Estimated 1 g SAR |
|---|---:|---:|---:|---:|
| BLE body | 2480 | 3.98 mW | 0 mm | 0.17 W/kg |
| LoRa body | 914.9 | 14.13 mW | 0 mm | **0.36 W/kg** |

**Simultaneous transmission** *(p. 29)*

| Combination | Position | SAR1 | SAR2 | ΣSAR | < 1.6 W/kg |
|---|---|---:|---:|---:|:-:|
| WLAN + LoRa + NFC | Body | 0.19 | 0.36 | **0.55** | ✓ |
| BLE + LoRa + NFC | Body | 0.17 | 0.36 | **0.53** | ✓ |

**NFC** *(RF Exposure Information exhibit, 1 p., report `2604T59815E-RF-22C`,
p. 11 of 51; repeated at SAR report p. 24)*

The NFC emitter was excluded by a very wide margin:

- Measured field **66.65 dBµV/m at 3 m** → EIRP **−28.55 dBm = 0.0014 mW**
  (using `E[dBµV/m] = EIRP[dBm] + 95.2` for `d = 3 m`).
- Exclusion threshold at 13.56 MHz for < 50 mm separation:
  `[474 × (1 + log(100/13.56))] / 2` = **443 mW**.
- 443 mW ≫ 0.0014 mW → **excluded**, and the report notes NFC therefore "almost
  have no influence on the results of simultaneous transmission."

**This is the only EIRP figure anywhere in the fetched exhibits**, and it is for
the one emitter nobody cares about. It also says something useful: the NFC field
is *tiny* at 3 m, consistent with a near-field reader loop rather than anything
that will interfere at distance. The underlying measurement is in
`2604T59815E-RF-00C`, which was not fetched.

### Laboratory conditions and instrument chain

Recorded because a future reader comparing this against another filing will want
them. *(SAR report pp. 8–17, 25, 31)*

| Field | Value |
|---|---|
| System | SPEAG **DASY5**, DASY52 v52.10(4), SEMCAD X 14.6.14 (7501) |
| Probe | **EX3DV4 SN 7441**, calibrated 2025-09-11, ConvF (6.49, 6.46, 6.38) @ 2450 MHz |
| Electronics | DAE4 SN 1493, calibrated 2025-12-01 |
| Phantom | Twin SAM V5.0, type `QD000P40CD`, serial 1470 |
| Sensor–surface distance | 1.4 mm, mechanical surface detection |
| System validation | D2450V2 dipole SN 751 — SAR(1 g) 5.13 W/kg, SAR(10 g) 2.25 W/kg, power drift 0.14 dB |
| Environment | 20.1–21.6 °C, 46–52 % RH, 100.4 kPa |
| Expanded uncertainty (95 %) | **±24.3 % (1 g)**, ±23.9 % (10 g) |
| Tissue liquid | `HBBL600-10000V6`; σ = 1.792 S/m, εr = 39.369 @ 2437 MHz |

Neither SAR measurement variability nor device-holder perturbation testing was
required — both tables on pp. 27 and 28 are empty, because the highest measured
SAR (0.167 W/kg) is far below the 0.80 W/kg and 1.2 W/kg thresholds that trigger
them.

---

## 5 — The label exhibit is an architecture diagram

**This is the find of the filing.** An FCC "ID Label / Location Info" exhibit is
normally a photograph of a compliance sticker. M5Stack filed its **complete
system architecture and pinout diagram** as the label artwork — a 775 × 832
raster, filed at 176 ppi, naming every power rail, every regulator part number,
every I²C address and essentially the whole GPIO map.

It is **an independent primary source for the pin map**, produced by M5Stack for
a regulator rather than for its documentation site, and it agrees with the
schematic-derived table in [`pinouts-and-buses.md`](pinouts-and-buses.md) on
every point but one.

### Header block

| Item | Value |
|---|---|
| Title | **M5PaperMono** — "= LoRa + NFC" |
| Marks | **CE**, **FCC**, Japanese MIC 技適 mark, WEEE crossed-bin, M5STACK logo |
| **Japanese MIC number** | **Ⓡ 211-260514** |
| Model Name | **PaperMono** |
| FCC ID | **2AN3WM5PAPERMONO** |

**`211-260514` is a second regulatory identifier and it was not previously known
to this record.** It is a Japanese MIC *Construction Design Certification* (工事
設計認証) number; the `Ⓡ` prefix denotes radio equipment (特定無線設備) under the
Radio Law. `211` is the registered certification body's prefix. **This was not
verified against the MIC database in this pass** — see §11.

The presence of **CE** on the label is also new information: no CE marking or DoC
was located anywhere during the original pass.

### Display block

| Item | Value | Note |
|---|---|---|
| Size | **3.97″** | agrees with the record |
| Resolution | **800 × 480 P** | **the record and the vendor product page say 480 × 800** — see §10 |
| Greyscale | **4-Level Gray** | M5Stack's third statement of 4-level; see §10 |
| Frontlight | "FRONT LIGHT", switched from **`PM_G3`** | agrees — M5PM1 G3 PWM |

### Power tree, as drawn

| Rail / block | Part | Enable | Feeds |
|---|---|---|---|
| `L0` VBUS | — | — | source node |
| `3V3_L0` | **LDO SSP7615**, marked **"AlwaysOn"** | — | M5PM1, always-on logic, Btn PWR |
| `3V3_L1` | **LDO SSP7615** | `PM_L1_EN` | BMI270 |
| `3V3_L2` | **DC/DC JW5712** | `PM_L2_EN` | ESP32-S3 and most peripherals |
| `3V3_L2_LoRa` | *(drawn as a rail)* | — | LoRa |
| `EPD_3V3_L3` | **LDO SSP7615** | **`IOE_G3`** | e-paper panel |
| `TF_3V3_L3B` | **LDO SSP7615** | **`IOE_G13`** ⚠ | microSD |
| Charging | **CHG-IC IP2315** | — | `VBAT` |
| USB input | **AW32901** | — | `5V IN` |
| Battery | **1150 mAh** | `PM_BAT_ADC_EN`, `PM_BAT_ADC`, series `0 Ω` + MOS | — |
| **Charge current** | **= 500 mA** | — | stated on the diagram |
| USB | **USB-C**, `OTG/DATA` | — | D+ `G20`, D− `G19` |

Every part number matches [`power-architecture.md`](power-architecture.md) and
[`bill-of-materials.md`](bill-of-materials.md): `SSP7615-33DFR`, `JW5712`,
`IP2315`, `AW32901FCR`. The `IOE_G13` cell is the one disagreement — §10.

**`CHG CURRENT = 500 mA` is a new figure.** See
[C18](gaps-and-conflicts.md#c18--ip2315-charge-current-cannot-be-read-from-the-datasheet-table),
which currently records that the charge current *cannot be derived* and that the
only statement of intent is schematic sheet 1's `充电电流 0.5C` (~575 mA). The
label says 500 mA. Two M5Stack sources, two different numbers — C18 is now a
conflict between vendor statements rather than an absence of evidence, and it is
**still unresolved**, because neither is a measurement.

### Silicon blocks and bus addresses

| Block | Label text | Matches record? |
|---|---|:-:|
| **ESP32 S3R8** + `40M` crystal + `16M FLASH` | — | ✓ |
| **IOE1 (PY32)** | `0×4F` | ✓ |
| **PM1 (PY32)** | `0×6E`, `IRQ: G1`, `Btn_PWR`, `PM_5VIN_ADC` | ✓ |
| **BMI270** | `SDA:G47 SCL:G48 IMU_INT:PM_G4` | ✓ |
| **RX 8130** | `SDA:G47 SCL:G48 INT:PM_G0` | ✓ |
| **ST25R3916** | `SDA:G47 SCL:G48 NFC_INT:G6` | ✓ |
| **LoRa1262** | *(see below)* | ✓ |
| **SSD1677** *(implied by the EINK block)* | — | ✓ |

The label writes the expander and power-manager addresses as `0×4F` and `0×6E`
with a multiplication sign — cosmetic, but worth knowing if you grep for `0x4F`.
Note that the label does **not** show the I²C addresses of the touch controller,
IMU, RTC, NFC or charger; the record's `0x38 / 0x68 / 0x32 / 0x50 / 0x75` come
from elsewhere and are not corroborated here.

### GPIO assignments, as labelled

Transcribed verbatim. The right-hand column is the corresponding row in
[`pinouts-and-buses.md`](pinouts-and-buses.md).

**E-paper**

| Label | Pin | Schematic net | ✓ |
|---|---|---|:-:|
| `EINK_RST` | **IOE_G5** | `PYB_EINK_RST` = `PYG5_ADC3` | ✓ |
| `EINK_BUSY` | G18 | `G18_EINK_BUSY` | ✓ |
| `EINK_DC` | G17 | `G17_EINK_DC` | ✓ |
| `EINK_CS` | G16 | `G16_EINK_CS` | ✓ |
| `SPI_CLK` | G15 | `G15_SPI2_CLK` | ✓ |
| `SPI_MOSI` | G14 | `G14_SPI2_MOSI` | ✓ |

**Touch**

| Label | Pin | Schematic net | ✓ |
|---|---|---|:-:|
| `TP_RST` | **IOE_G6** | `PYB_TP_RST` = `PYG6` | ✓ |
| `SDA` / `SCL` | G47 / G48 | system I²C | ✓ |
| `TP_INT` | G4 | `G4_TP_INT` | ✓ |

**LoRa1262**

| Label | Pin | Schematic net | ✓ |
|---|---|---|:-:|
| `SPI_CLK` | G39 | `G39_SPI1_CLK` | ✓ |
| `SPI_MOSI` | G38 | `G38_SPI1_MOSI` | ✓ |
| `SPI_MISO` | G40 | `G40_SPI1_MISO` | ✓ |
| `LoRa_CS` | G41 | `G41_LoRa_NSS` | ✓ |
| `LoRa_BUSY` | G21 | `G21_LoRa_BUSY` | ✓ |
| `LoRa_INT` | G5 | `G5_LoRa_INT` (DIO1) | ✓ |
| `LoRa_RST` | **IOE_G10** | `PYB_LoRa_RST` = `PYG10_PWM4` | ✓ |
| **`LoRa_ANT_SW`** | **IOE_G2** | `PYB_LoRa_ANT_SW` = `PYG2_ADC1` | ✓ |

**microSD**

| Label | Pin | Schematic net | ✓ |
|---|---|---|:-:|
| `TF_Data3` | G8 | `G8_TF_DATA3` | ✓ |
| `TF_Data2` | G9 | `G9_TF_DATA2` | ✓ |
| `TF_Data1` | G10 | `G10_TF_DATA1` | ✓ |
| `TF_Data0` | G11 | `G11_TF_DATA0` | ✓ |
| `TF_CMD` | G12 | `G12_TF_CMD` | ✓ |
| `TF_CLK` | G13 | `G13_TF_CLK` | ✓ |
| `TF_DET` | **IOE_G1** | `PYB_TF_DET` = `PYG1` | ✓ |
| *(TF LDO enable)* | **IOE_G13** | `PYB_TF_EN` = **`PYG14`** | ⚠ **conflict** |

**Buttons, indicators, audio, USB**

| Label | Pin | Schematic net | ✓ |
|---|---|---|:-:|
| Btn UP | G2 | `G2_KEY1` | ✓ |
| Btn DOWN | G3 | `G3_KEY2` | ✓ |
| `PDM_CLK` | G45 | `G45_PDM_CLK` | ✓ |
| `PDM_DAT` | G46 | `G46_PDM_DAT` | ✓ |
| Buzzer `PWM` | G42 | `G42_BB_PWM` | ✓ |
| RGB `R` | **PM_LED** | M5PM1 `LED_EN_PP` | ✓ |
| RGB `G` | **IOE_G8** | `PYB_LED_G` = `PYG8_PWM2` | ✓ |
| RGB `B` | **IOE_G9** | `PYB_LED_B` = `PYG9_PWM1` | ✓ |
| USB `D+` / `D−` | G20 / G19 | `G20_USB_P` / `G19_USB_N` | ✓ |

**30 of 31 GPIO assignments on the label match the schematic-derived table
exactly.** That is a strong independent corroboration of
[`pinouts-and-buses.md`](pinouts-and-buses.md) from a source M5Stack prepared for
a different audience.

### Power-button behaviour

The label states the power-button semantics compactly — and this is the clearest
published statement of them anywhere:

| Action | Result |
|---|---|
| **Press** | **ON / RST** |
| **Double** | **OFF** |
| **HOLD** | **BOOT** |

Compare [`features/power-and-sleep.md`](features/power-and-sleep.md) and
[`development.md`](development.md), which describe the same behaviour from the
M5PM1 firmware. The `Btn PWR` node is drawn on `3V3_L0` — the always-on rail —
which is why it works with the ESP32-S3 unpowered.

---

## 6 — What the internal photographs show

Seven pages, thirteen JPEGs, **944 × 708 at 200 ppi**. That resolution is enough
to read large QFN and SOP markings and silkscreen, and **not** enough to read
small LGA laser marks. Everything below is either legible or explicitly marked
illegible. Nothing is inferred from a part's shape or position.

> **Method.** Images extracted with `pdfimages -j`, cropped and upscaled 4–16×
> with ImageMagick `-unsharp 0x2`. "Legible" means the characters were read from
> the pixels, not matched against an expectation.

### Page-by-page

| Page | Contents |
|---|---|
| 1 | Main PCB, e-paper panel (rear, markings visible), KEY/RGB sub-board flex |
| 2 | Main PCB top and bottom, against a mm rule |
| 3 | Main PCB top, two close-ups — **the readable page** |
| 4 | Main PCB top close-up; rear housing with NFC FPC, copper shield, LoRa FPC; battery |
| 5 | Main PCB with **"BLE 2.4G WiFi Ant"** annotated on the right edge |
| 6 | Rear housing with **"NFC Ant"** and **"LORA Ant"** annotated; NFC FPC daughterboard close-up |
| 7 | **"LORA ANT"** — the FPC strip and its coaxial pigtail, alone |

### Parts read from the photographs

| Marking as read | Identification | Confirms | Page |
|---|---|---|---|
| `ESP32-S3` / `392025` / `R8MRK714000` / `FC00MCJ114` with Espressif logo, 56-pin QFN | **ESP32-S3**, `R8` present in the lot string | [esp32-s3r8](../../../components/espressif/esp32-s3r8/README.md) — record says bare `ESP32-S3R8` die in 56-pin QFN, **confirmed** | 3 |
| `SX1262` / `LoRa®` / `2237` / `25486` with Semtech logo, 24-pin QFN | **Semtech SX1262**, date code 2237 (2022 wk 37), lot 25486 | [sx1262](../../../components/semtech/sx1262/README.md) — **confirmed** | 3 |
| `XMC` logo / `25UH128DHIG` / `P4J71900` / `2529K`, SOP-8 | **XMC XM25UH128DHI…**, 128 Mbit = 16 MB | [xm25uh128dhiqt](../../../components/xmc/xm25uh128dhiqt/README.md) — **`UH` confirmed**, final character(s) not resolvable, so `…Q` vs `…G` is *not* settled | 3 |
| `R8130` / `○3581K`, 12-pad ceramic | **Epson RX8130**(CE) RTC | [rx8130ce](../../../components/seiko-epson/rx8130ce/README.md) — **confirmed** | 3 |
| `IP2315` / `0Y21.1CA` with Injoinic logo, QFN | **Injoinic IP2315** charger | [ip2315](../../../components/injoinic/ip2315/README.md) — **confirmed** | 4 |
| `M10` + lot, 4-pad ceramic oscillator beside the SX1262 | **unidentified** — see below | [G5](gaps-and-conflicts.md#g5--no-stamp-lora-1262-module-datasheet-exists-anywhere-located) | 3 |
| ST logo, 32-pin QFN on the NFC FPC daughterboard | **STMicroelectronics part — number ILLEGIBLE** | consistent with [st25r3916](../../../components/stmicroelectronics/st25r3916/README.md), **not confirmed** | 6 |
| Small LGA beside silkscreen `IMU` + X/Y/Z axis glyph | **ILLEGIBLE** | position consistent with [bmi270](../../../components/bosch-sensortec/bmi270/README.md), **not confirmed** | 3 |
| `HN`, large shielded module beside the SX1262 | **ILLEGIBLE / unidentified** | — | 3 |
| `0397BBS770F3HP-` + 2 illegible chars / `N2510P10340-01-50519-1` / `15AL11102200347`, laser-etched on the panel glass | **the e-paper panel** — see §10, C2 | [depg0397bbs770f3](../../../components/dke/depg0397bbs770f3/README.md) | 1 |
| `YS 414250 1150mAh` / `3.7V 4.255Wh 2603`, pouch cell | **1150 mAh Li-poly, 4.1 × 42 × 50 mm, 4.255 Wh** | [cell](../../../components/generic/papermono-1150mah-liion-cell/README.md) — **1150 mAh confirmed**; Wh and dimensions are **new** | 4, 5 |

**On the `M10` oscillator.** A 4-pad ceramic-packaged oscillator or crystal sits
immediately beside the SX1262 on the LoRa module. `M10` is a house code, not a
part number, and the manufacturer logo is not legible. **This does not settle
[G5](gaps-and-conflicts.md#g5--no-stamp-lora-1262-module-datasheet-exists-anywhere-located)'s
TCXO-versus-XTAL question**: both a 32 MHz TCXO and a bare crystal for the
SX1262 use 4-pad ceramic packages of this size. What it does establish is that a
**discrete frequency reference is fitted on the module**, which was previously
only assumed. Resolving it needs a higher-resolution photograph or a
`DIO3_TCXO_CTRL` probe.

**On the ST part.** The ST corporate logo is unmistakable at the die corner; the
part number below it is a smear at 200 ppi. The NFC daughterboard carries a
32-pin QFN, an antenna-matching network and a printed loop antenna — an entirely
ordinary ST25R3916 reader front end. **But the marking was not read**, so this
is corroboration of the vendor's claim, not independent confirmation of it.

### Board-level structure

**The three-PCB-plus-flex structure described in
[`pinouts-and-buses.md`](pinouts-and-buses.md#board-set--this-is-not-one-pcb) is
visually confirmed.** The photographs show the main board, a KEY/RGB flex
assembly (p. 1), a separate NFC FPC daughterboard with its own reader IC (p. 6),
the e-paper panel with its own FPC tail, and the LoRa antenna FPC (p. 7).

**The Stamp LoRa-1262 is a genuine module, not a bare chip on the mainboard.**
This was worth checking, because the `LoRa1262` block on the label exhibit could
be read either way. Page 3 shows the SX1262 sitting inside a **castellated
sub-PCB** with a stitched-via perimeter, its own matching network, its own
oscillator and its own U.FL connector, soldered onto the mainboard. That
**confirms** the record's "plug-in `Stamp-LoRa-1262-mini` module" description and
the [stamp-lora-1262](../../../components/m5stack/stamp-lora-1262/README.md)
component record.

### Silkscreen and assembly markings

| Marking | Where | Reading |
|---|---|---|
| `M5Stack` / `PAPER mono` / `…251222  V0.6` | main PCB, bottom side | **PCB revision V0.6**, date code `251222` = 2025-12-22. The first digits are hidden by an adhesive blob; `20251222` is the obvious completion but is **not legible**. |
| `Paper_Mono_NFC` / `V0.2  2025?2?3` / `M5STACK` | NFC FPC | **rev V0.2** — matches the schematic's NFC sheet rev V0.2. The date string's middle digits are not legible; it is 2025. |
| `Paper Mono V3.0` | LoRa antenna FPC | antenna assembly revision **V3.0** — matches the `RSY-E8131` spec's own V3.0 |
| `NFC`, `IMU` + axis glyph, `KEY RGB PDM` | main PCB, top side | function labels beside the respective parts |

### The test-pad census on the bottom side

Sixteen labelled pads, read from page 2. **None of these appears anywhere else in
this record**, and several are directly useful for bring-up and debugging.

| Pad | Evident purpose |
|---|---|
| `GND` | ground reference |
| `SWD1` / `SWC1` | SWD data/clock — **one PY32** |
| `SWD2` / `SWC2` | SWD data/clock — **the other PY32** |
| `RESET1` / `RESET2` | the two PY32 resets |
| `SOC_BOOT` | ESP32-S3 boot strap |
| `SOC_RST` | ESP32-S3 reset |
| `Tx` / `Rx` | UART0 |
| `3V3_L0` / `3V3_L1` / `3V3_L2` / `3V3_L2_LoRa` | the four switched rails |
| `VBUS_L0` | USB rail |

**Both custom PY32 microcontrollers have SWD broken out to test pads.** The
M5PM1 and M5IOE1 are the two parts this record repeatedly identifies as opaque —
[`m5pm1`](../../../components/m5stack/m5pm1/README.md) and
[`m5ioe1`](../../../components/m5stack/m5ioe1/README.md) run M5Stack firmware on
`PY32L020F15U6` silicon with no published source. `SWD1/SWC1/RESET1` and
`SWD2/SWC2/RESET2` are the physical route to reading or replacing that firmware.
Which pair belongs to which chip **is not marked** and was not determined.

> ⚠ **Untested and risky.** Nothing here has been probed. Both PY32 parts are
> very likely read-protected, and attaching a debugger to a live power manager
> that owns the ESP32-S3's reset and boot straps can brick the board. See
> [`development.md`](development.md) for the bricking risks already catalogued.
> Status: `not-tested`, `inferred` from silkscreen only.

---

## 7 — What the user manual adds

The FCC-filed user manual (10 pp) is a different document from anything on
`docs.m5stack.com`. Its specification table is the most complete single-page
component list M5Stack has published for this board, and it names parts the
product page does not.

**Specification table** *(user manual p. 3)* — this is M5Stack's own list, filed
under penalty with a federal agency:

| Specification | Parameter | vs. this record |
|---|---|---|
| SoC | ESP32-S3R8 @ dual-core Xtensa LX7, to 240 MHz | ✓ |
| PSRAM / Flash | 8 MB / 16 MB | ✓ |
| Wi-Fi | 2.4 GHz, **2412–2462 MHz** | ✓ and now certified |
| BLE | 2.4 GHz, **2402–2480 MHz** | ✓ and now certified |
| Display | 3.97″ E-Paper (Mono) **SSD1677 @ 480 × 800**, touch **FT6336G** | ✓ — and note **480 × 800**, contradicting the label exhibit |
| Front light | integrated E-paper front light | ✓ |
| Power input | USB Type-C DC 5 V | ✓ |
| Battery | 1150 mAh | ✓ |
| Microphone | PDM **LMD4737T261-AC02** | ✓ |
| Buzzer | built-in | ✓ |
| IMU | **BMI270** | ✓ |
| IO expander | **M5IOE1** | ✓ |
| External storage | microSD | ✓ |
| RTC | **RX8130CE** | ✓ |
| RGB LED | built-in | ✓ |
| NFC | **ST25R3916** — ISO14443A/B, FeliCa™, ISO15693, 13.56 MHz | ✓ |
| LoRa | **903.0–914.9 MHz** | ⚠ conflicts with the same manual's p. 2 |
| User keys | 2 × user + 1 × power (ON/OFF/RESET/BOOT) | ✓ |
| **Hardware version** | **V1.0** | ⚠ the PCB silkscreen says **V0.6** and the schematic V0.6.2 |
| **Software version** | **V1.0** | new — no other source gives a shipped software version |

### Things the manual reveals that the vendor docs omit

**The board is described as running a 40 MHz crystal** (p. 2) — corroborating the
schematic's `CN4040M000157A530001`.

**The LoRa radio is described as "SX1262 chip (Stamp LoRa-1262) with a built-in
FPC antenna"** (p. 2) — this is the clearest vendor statement that the LoRa
subsystem is the Stamp module *and* that its antenna is an FPC, both of which the
internal photographs then confirm independently.

**The M5PM1 is called a "multi-level power management system"** (p. 2) — matching
the five power states in [`power-architecture.md`](power-architecture.md).

**The Arduino setup is spelled out** (pp. 4–6), and it is the same configuration
[`development.md`](development.md) already records, from a second source:

- Board manager URL `https://espressif.github.io/arduino-esp32/package_esp32_dev_index.json`
- Board: **"ESP32S3 Dev Module"**
- **USB CDC On Boot: Enabled**
- **PSRAM: "OPI PSRAM"** — mandatory, as the record already states
- **USB Mode: "Hardware CDC and JTAG"**

**The intended applications are named** (p. 2): *"e-readers, electronic signage,
access control systems, identity authentication, intelligent transportation, and
other IoT and embedded applications."* Access control and identity
authentication are listed first among the non-obvious ones, which fits the
ST25R3916 + 0 mm SAR posture and supports the positioning analysis in
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) (W3).

**The FCC Caution and Class B statement** (p. 10) are the standard §15.19 /
§15.105(b) boilerplate plus: *"This equipment complies with FCC radiation
exposure limits set forth for an uncontrolled environment."* No separation
distance is stated, consistent with the 0 mm SAR result.

---

## 8 — Identifiers, SKUs and model strings

Every identifier the filing carries, in one place.

| Identifier | Value | Source |
|---|---|---|
| FCC ID | `2AN3WM5PAPERMONO` | grant |
| FCC grantee code | `2AN3W` | filing index |
| FCC product code | `M5PAPERMONO` | filing index |
| FCC applicant FRN | `0026912345` | filing index |
| FCC application IDs | `TRHAipRYjij4wjjVV4V9JA==` (DTS), `cV4RemadFogfsatkKapmuQ==` (DXX) | grants |
| **Japan MIC certification** | **`Ⓡ 211-260514`** | label exhibit |
| Product name, as filed | `M5PaperMono` | SAR report p. 1 |
| Model number, as filed | `PaperMono` | SAR report p. 1 |
| Model, in the application | `M5PAPERMONO` | filing index |
| Multiple models | `N/A` — **one model only** | SAR report p. 1 |
| Vendor SKU | `C153` — **does not appear in the filing at all** | vendor store |
| Hardware version (manual) | `V1.0` | user manual p. 3 |
| Software version (manual) | `V1.0` | user manual p. 3 |
| PCB revision (silkscreen) | `V0.6`, date code `251222` | internal photos p. 2 |
| NFC FPC revision | `V0.2` | internal photos p. 4 |
| LoRa antenna FPC revision | `V3.0` | internal photos p. 6 |
| EUT serial number | `3MFY-1` | SAR report p. 5; scan plot |
| Antenna part number | `RSY-E8131` | antenna spec p. 1 |
| Battery marking | `YS 414250 1150mAh  3.7V 4.255Wh  2603` | internal photos pp. 4, 5 |
| E-paper glass marking | `0397BBS770F3HP-??`, `N2510P10340-01-50519-1`, `15AL11102200347` | internal photos p. 1 |
| SAR report number | `2604T59815E-SA` | SAR report p. 1 |
| RF exposure report number | `2604T59815E-RF-22C` | RF exposure info exhibit |
| Cited but not filed | `2604T59815E-RF-00B` (802.11b duty cycle), `2604T59815E-RF-00C` (NFC) | SAR report pp. 22, 24 |

**There is no barcode, UPC/EAN, HS/tariff code or country-of-origin statement in
any of the eleven exhibits.** The skill's compliance-extraction checklist asks
for tariff codes and barcodes; for this filing they simply do not exist. FCC
equipment-authorisation exhibits are not customs documents, and M5Stack filed no
packaging artwork. Recorded as a negative result so nobody looks again.

**`C153` is absent from the filing.** M5Stack's own store SKU appears nowhere in
the FCC paperwork — which is precisely why a `/en/certification` search for
`C153` was always going to fail. The bridge between the vendor SKU and the
regulatory identity is the string **`PaperMono`**, and nothing else.

---

## 9 — Constraints this imposes on anyone building on the board

Practical consequences, for the reader who came here from
[`features/lora.md`](features/lora.md) or
[`development.md`](development.md).

| Constraint | Detail | Consequence |
|---|---|---|
| **LoRa is certified 903.0–914.9 MHz in the US only** | grant; user manual p. 3 | Configuring the SX1262 to 868 MHz or 923 MHz is outside the US grant. The hardware supports it; the authorisation does not. No CE/IC/RCM/SRRC record was located. |
| **LoRa conducted power ceiling is 11.5 dBm** | SAR report pp. 21, 24 | This is not a tuning preference. At 11.5 dBm the SAR exclusion calculation gives 2.7 against a limit of 3.0. Raising transmit power breaks the exclusion and invalidates the SAR basis of the grant. |
| **Wi-Fi is certified on channels 1–11 only; 40 MHz only on 2422–2452** | grant | The ordinary US plan, now documented. |
| **Wi-Fi and BLE cannot transmit simultaneously** | SAR report p. 29 | Design around it. Add to [`resources-and-conflicts.md`](resources-and-conflicts.md). |
| **Antennas are internal and fixed** | SAR report p. 5; user manual p. 10 | A U.FL connector exists on the LoRa module, but substituting an antenna voids the authorisation under the §15.21 Caution. |
| **Body-worn accessories must contain no metal** | grant note | Applies to any case or holster you design. |
| **Certified posture is 0 mm body contact, all six faces** | SAR report pp. 18, 26 | No separation-distance warning is needed, and none is published. |
| **The back is the RF-hot face** | SAR report p. 26 | 0.19 W/kg vs 0.01 W/kg on top. Relevant to enclosure and mounting design. |
| **No LoRa duty-cycle limit is in evidence** | — | If your region imposes one, this filing will not tell you what M5Stack assumed. |
| **The grant covers one model** | SAR report p. 1 | `Multiple Model(s) No.: N/A`. **[PaperMono-Lite](../papermono-lite/README.md) is not covered by this FCC ID** and no separate grant for it was located — it has no LoRa and no NFC, so its radio profile differs. |

---

## 10 — Conflicts advanced or opened by this filing

### C1 — 4 grey levels versus 2: *unchanged*

The label exhibit says **"4-Level Gray"**. That is now M5Stack's *third*
independent statement of four-level greyscale (product page, OTP demo, FCC label)
against the DKE panel manual's `GN — 2Grey Level`. But all three are the same
party. [C1](gaps-and-conflicts.md#c1--4-grey-levels-versus-2) turns on whether
DKE's optical table or M5Stack's implementation is authoritative, and a third
M5Stack document does not move that. **Still unresolved.**

### C2 — panel part number: *materially advanced*

[C2](gaps-and-conflicts.md#c2--panel-part-number) records that the DKE manual
says `DEPG0397BBS770F3` while `M5PaperMono-OTP-Demo` calls the fitted panel
`DEPG0397BBS770F3HP-XM`, with the suffix "undocumented".

**The panel glass itself is laser-etched `0397BBS770F3HP-` followed by two
characters that are not legible at 200 ppi** (internal photos p. 1). So:

- **The `HP` is real and is on the hardware.** It is not an OTP-demo typo, and it
  is not a DKE ordering-code artefact. The fitted part genuinely carries a suffix
  the manual does not document.
- **`-XM` is neither confirmed nor refuted.** My best reading of the final two
  characters is `H2`/`HE`/`N2`, and I do not trust it. `XM` cannot be excluded.
- The glass also carries `N2510P10340-01-50519-1` and `15AL11102200347`, neither
  of which appears in any DKE document held here. `N2510` is consistent with a
  2025 week-10 production code but that is a guess and is labelled as one.

C2 moves from "an undocumented suffix appears in one source file" to "the fitted
panel is a `…HP` variant, and DKE's published manual does not describe it."
**Partially resolved.** What would settle it: a photograph of the glass at
≥ 600 ppi, or DKE's `…HP` ordering documentation, which
[`vendors/dke`](../../../vendors/dke/README.md) records as unobtainable.

### C10 / display orientation — *new evidence, no resolution*

[C10](gaps-and-conflicts.md#c10--dke-drawing-note-reversed) records that DKE's
drawing note 3 reads `800 gate × 480 source`, which the record calls "provably
backwards". The **label exhibit says `800x480P`** while the user manual filed
alongside it says **`480 × 800`** — the two exhibits in the *same filing*
disagree. This does not resolve anything; it shows the transposition is endemic
across M5Stack's documentation rather than a single DKE error. **Unresolved.**

### C18 — IP2315 charge current: *a number now exists, and it is a third one*

[C18](gaps-and-conflicts.md#c18--ip2315-charge-current-cannot-be-read-from-the-datasheet-table)
records that `ICHGSET` = 15 kΩ is untabulated, so the programmed current is not
derivable, and that schematic sheet 1's `充电电流 0.5C` (~575 mA for a 1150 mAh
cell) is the only statement of intent.

**The label exhibit states `CHG CURRENT = 500 mA` outright.** That is a concrete
figure, and it is *not* 575 mA. Two M5Stack documents now give two different
charge currents, and neither is a measurement. The practical answer for a
developer is "around 500 mA", and the conflict is **unresolved** — a bench
measurement of charge current at 15 kΩ would close it in minutes.

### New conflict — the microSD LDO enable: IOE_G13 versus PYG14

⚠ **NEW 2026-09-20.**

**The label exhibit and the schematic disagree about which expander pin enables
the microSD power rail.**

| Source | microSD LDO (`TF_3V3_L3B`) enable |
|---|---|
| Label exhibit | **`IOE_G13`** |
| Schematic, via [`pinouts-and-buses.md`](pinouts-and-buses.md#m5ioe1-expander-pins) | **`PYG14`** = `PYB_TF_EN` |

`PYG13` on the schematic is `PYB_TP_EN` — **touch** power enable, a different
rail entirely.

This looks at first like the off-by-one hazard documented in
[`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md) and
in the M5IOE1 note ("`M5IOE1_PIN_3 = 2` — the label is 1-based, the enum value
0-based"). **It is not, and that is what makes it interesting.** All *seven*
other `IOE_G*` assignments on the label match the schematic's `PYG*` numbering
exactly — `G1`↔`TF_DET`, `G2`↔`LoRa_ANT_SW`, `G3`↔`EPD_EN`, `G5`↔`EINK_RST`,
`G6`↔`TP_RST`, `G8`↔`LED_G`, `G9`↔`LED_B`, `G10`↔`LoRa_RST`. A systematic
off-by-one would have shifted all of them.

So one of two things is true, and the evidence does not choose:

1. **The label has a single typo**, `G13` for `G14`; the schematic is right.
2. **The label is right and the schematic net names are misleading**, in which
   case `PYB_TF_EN` and `PYB_TP_EN` are the pins that are swapped.

**Reading (1) is more economical** — a one-character error on a marketing diagram
versus a two-net error on a schematic — but that is a preference, not evidence,
and this repository's Conflict Protocol forbids settling it that way.

> **Least-risky implementation path:** treat **both `PYG13` and `PYG14` as
> unsafe to repurpose**, and when enabling microSD power, drive the pin the
> schematic names `PYB_TF_EN` (`PYG14`) — the schematic is the higher-authority
> source for a net. If the card does not enumerate, try `PYG13` before assuming
> a hardware fault. Toggling the wrong one will cut power to the touch panel,
> which is recoverable and diagnostic.

**What would settle it:** reading the enable net at the microSD LDO on schematic
sheet 2, or an I²C experiment on hardware — toggle `PYG13` and `PYG14` in turn
and observe which kills the card and which kills touch. Logged to
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) and
[`compatibility-and-status.md`](compatibility-and-status.md).

### Confirmed correct — recorded so it is not re-investigated

Per the skill's rule that confirmed-correct documentation is recorded with the
same rigour as a correction:

- **The three-PCB-plus-flex board set** — confirmed visually (internal photos
  pp. 1, 4, 6).
- **The Stamp LoRa-1262 is a real castellated module**, not a bare SX1262 on the
  mainboard — confirmed (p. 3).
- **ESP32-S3 in a bare 56-pin QFN, not a module** — confirmed (p. 3).
- **XMC flash, `25UH…` family** — the `UH` is confirmed on the package (p. 3),
  which rules out the `XM25QH` family that a casual reading might assume.
- **`RX8130` RTC and `IP2315` charger** — confirmed (pp. 3, 4).
- **1150 mAh battery** — confirmed on the cell label (pp. 4, 5).
- **30 of 31 GPIO assignments** — confirmed against a second primary source (§5).

---

## 11 — Unverified, not read, and not fetched

Stated plainly, because the value of this document depends on its limits being
known.

**Not fetched.** Four detailed radio test reports (main, Wi-Fi 5 MB, BLE 2.8 MB,
LoRa 1.8 MB), two Test Setup Photos exhibits, four attestation letters and two
cover letters. URLs, sizes and FCC document IDs are in
[`artifacts/certification/README.md`](artifacts/certification/README.md).
**These are the only route to per-channel EIRP, band-edge compliance, spurious
emissions, and the LoRa duty cycle.** They are also where the two cited-but-absent
reports `2604T59815E-RF-00B` and `-00C` most likely live. This is the highest-value
follow-up available on this filing.

**Never published.** Schematics, Block Diagram and Operation Description are
metadata-only under a long-term confidentiality request. Nothing to reacquire.
(No loss for the schematic — M5Stack publishes it, and it is at
[`artifacts/schematic/`](artifacts/schematic/).)

**Not verified.**

- **The Japanese MIC number `211-260514` was not checked** against
  `https://www.tele.soumu.go.jp/giteki/` or any MIC registry. It is transcribed
  from the label artwork and nothing more. The `Ⓡ`-prefix and `211`-body-code
  interpretation is `inferred` from the general form of Japanese certification
  numbers.
- **The CE mark on the label is not backed by a located DoC.** A mark on artwork
  is not a Declaration of Conformity.
- **No IC (Canada), RCM (Australia/NZ), UKCA or SRRC (China) record was searched
  for** in this pass.
- **No certification was located for [PaperMono-Lite](../papermono-lite/README.md)**
  (SKU C153-LITE). Its FCC status is **unknown**, not negative — the grantee index
  was not re-walked for it.

**Illegible, not absent.** The BMI270 marking, the ST25R3916 part number, the
`M10` oscillator's identity, the `HN` shielded module, the final two characters
of the e-paper part number, and the leading digits of two date codes were all
**unreadable at 200 ppi**. They are recorded as illegible. None of them was
guessed, and none should be promoted to a finding by a later reader without a
better photograph.

**Computed, not transcribed.** The dBm column in §2, and the ~+6 dBm LoRa EIRP
estimate in §3, are arithmetic on figures from the exhibits. They are `inferred`.

---

## Sources

| ID | Exhibit | Pages | Disposition |
|---|---|---:|---|
| F1 | Grant certificates + filing index, `fccid.io/2AN3WM5PAPERMONO` | — | `scratch/market-and-certification/fcc/2AN3WM5PAPERMONO/_filing.html`, retrieved 2026-09-11 |
| F2 | SAR Test Report `2604T59815E-SA` | 34 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-sar-test-report.pdf.ARCHIVED.md) |
| F3 | Antenna Specification (`RSY-E8131` V3.0) | 11 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-antenna-specification.pdf.ARCHIVED.md) |
| F4 | User Manual | 10 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-user-manual.pdf.ARCHIVED.md) |
| F5 | **Internal Photos** | 7 | **[in repository](artifacts/certification/2AN3WM5PAPERMONO-internal-photos.pdf)** |
| F6 | **ID Label / Location Info** (the architecture diagram) | 1 | **[in repository](artifacts/certification/2AN3WM5PAPERMONO-label-and-label-location.pdf)** |
| F7 | RF Exposure Information `2604T59815E-RF-22C` | 1 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-rf-exposure-information.pdf.ARCHIVED.md) |
| F8 | SAR Scan Plots | 1 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-sar-scan-plots.pdf.ARCHIVED.md) |
| F9 | SAR EUT Test Position Photos | 4 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-sar-eut-test-position-photos.pdf.ARCHIVED.md) |
| F10 | SAR Calibration Certificates | 15 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-sar-calibration-certificates.pdf.ARCHIVED.md) |
| F11 | SAR Return Loss & Impedance Measurement | 2 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-sar-return-loss-impedance-measurement.pdf.ARCHIVED.md) |
| F12 | External Photos | 3 | [archived, placeholder](artifacts/certification/2AN3WM5PAPERMONO-external-photos.pdf.ARCHIVED.md) |

All twelve are **US Government public records** under 47 CFR §2.1033;
redistribution **`allowed`**. Class: `primary` / `regulatory record`. Retrieved
**2026-09-11** from `fccid.io` with `curl/8.5.0`; every file magic-byte validated
and SHA-256 verified before and after filing. Hashes and byte sizes are in
[`artifacts/certification/README.md`](artifacts/certification/README.md) and in
each placeholder.

**Text-layer validation.** Per the skill's rule against trusting an unvalidated
PDF text layer: the SAR report's extracted text was cross-checked against
rendered images of pages 5 and 22 at 130 dpi before any value on this page was
transcribed. The rendered pages match the extracted text exactly, and the PDF
page index equals the printed page number throughout. Figures read from the
internal-photo and label *images* were read from pixels; those exhibits have no
useful text layer at all.
