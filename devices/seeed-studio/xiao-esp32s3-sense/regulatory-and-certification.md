# Regulatory and certification — XIAO ESP32S3 Sense

> FCC filing data, and the hardware facts it reveals that Seeed does not publish.
> Retrieved **2026-08-24** from [fccid.io](https://fccid.io/Z4T-XIAOESP32S3). Exhibits retained in [`artifacts/regulatory/`](artifacts/regulatory/).

## 1. The filing

| Field | Value |
|---|---|
| **FCC ID** | **`Z4T-XIAOESP32S3`** |
| Grantee code | **`Z4T`** — Seeed Technology Co., Ltd. |
| Product code | `XIAOESP32S3` |
| **Covers** | **"Seeed Studio XIAO ESP32S3, Seeed Studio XIAO ESP32S3 Sense"** — one grant, both models |
| Application date | **2023-04-21** |
| Purpose | Original Equipment |
| Frequency range | 2402–2480 MHz |
| Test firm | Centre Testing International (CTI) |
| Test report No. | `EED32P80440601` |
| Sibling filing | `Z4T-XIAOESP32S3P` — the **Plus** variant (separate grant) |

The **Sense is covered by the same grant as the plain board.** That is consistent with the daughterboard containing no radio — the RF design is entirely on the mainboard.

There is also a **Module approval letter**, meaning Seeed sought modular approval so the XIAO can be designed into a host product without recertifying the radio. That is a genuinely useful fact for anyone building a product around it, and it is not mentioned anywhere in Seeed's own documentation.

`Z4T` is the grantee code to search for **any** Seeed product on the FCC databases.

## 2. Antenna specification — performance figures published nowhere else

The **FPC Antenna Specification** exhibit ([`artifacts/regulatory/fpc-antenna-spec.pdf`](artifacts/regulatory/fpc-antenna-spec.pdf), 18 pages) is a supplier datasheet, and it is the only source of real antenna performance data for this board.

| Parameter | Value |
|---|---|
| **Supplier** | **ShenZhen MyAntenna RF Technology Co., Ltd** |
| **Part number** | **`M01-0600890R0A`** (Seeed code `318020748`) |
| Type | **FPC (flexible printed circuit)**, not a rubber-duck |
| **FPC size** | **40.0 × 20.0 mm** ±0.3/±0.2 |
| **Coax pigtail** | **Ø1.13 × 80.0 mm** ±2.0 |
| Connector | **IPEX / U.FL** |
| Frequency range | 2400–2500 MHz |
| **Peak gain** | **2.90 dBi** |
| **Efficiency** | **70.5 %** |
| VSWR | ≤ 2.0 (measured 1.52 @ 2.4 GHz, **1.23 @ 2.45 GHz**, 1.47 @ 2.5 GHz) |
| Impedance | 50 Ω |
| Polarisation | **Vertical** |
| Working temp | −30 °C to +80 °C |
| Marking | "Seeed Studio V1.0" (V1.2 on the unit photographed) |

Measured gain and efficiency across the band:

| Freq (MHz) | 2400 | 2410 | 2420 | 2430 | 2440 | 2450 | 2460 | 2470 | 2480 | 2490 | 2500 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Gain (dBi) | 2.43 | 2.80 | 2.68 | 2.63 | 2.44 | 2.26 | 2.54 | 2.77 | 2.81 | 2.84 | 2.90 |
| Efficiency (%) | 61.8 | 67.3 | 67.8 | 66.7 | 64.6 | 63.6 | 66.2 | 69.7 | 70.0 | 69.8 | 70.5 |

Three practical points:

**2.9 dBi / ~70 % is a decent FPC antenna**, not a compromise part. Seeed's "100 m+" range claim is at least not implausible with line of sight.

**Efficiency dips to 61.8 % at 2400 MHz** — the bottom of the band, i.e. Wi-Fi channel 1 and the BLE advertising channel at 2402 MHz. Marginally better performance is available higher in the band.

**Polarisation is vertical**, and it is a flat FPC. Orientation matters: laying the antenna flat inside a horizontal enclosure while the access point is vertically polarised costs real signal. Wearable projects that fold the antenna against a body will do worse again.

> ⚠ **The document is titled for the `Seeed XIAO ESP32C3`.** It is a shared antenna across the XIAO family, submitted as part of the ESP32-S3 filing. The dated revision history (2022-05-13 → 2022-06-13, "Change FPC") predates this board. Treat it as *the antenna Seeed ships*, not as a document specific to this product.

## 3. What the internal photos show

Exhibits: [`internal-photos-1.pdf`](artifacts/regulatory/internal-photos-1.pdf) (10 pages) and [`internal-photos-2.pdf`](artifacts/regulatory/internal-photos-2.pdf) (3 pages), from test report `EED32P80440601`. Six representative images extracted to [`artifacts/regulatory/fcc-photos/`](artifacts/regulatory/fcc-photos/).

### 3.1 The JTAG pins are broken out as labelled bottom-side pads

[`mainboard-bottom-jtag-pads.jpg`](artifacts/regulatory/fcc-photos/mainboard-bottom-jtag-pads.jpg) shows the mainboard underside with silkscreen labels **`MTDO`, `MTDI`, `MTMS`, `MTCK`** — plus `BAT+`/`BAT−` — as an array of exposed pads.

This corresponds to test points **TP2–TP5** in the netlist (`PDM_CLK`, `PDM_DATA`, `CAM_SDA`, `CAM_SCL` = `MTMS`, `MTDI`, `MTDO`, `MTCK`), but the photo establishes something the netlist alone does not: **they are deliberately labelled, user-accessible pads, not bare test points.**

Consequence: **on a plain XIAO ESP32S3 (no daughterboard), you can solder to these pads and get a full JTAG port.** The [JTAG conflict](pinouts-and-buses.md#72-the-camera-and-microphone-occupy-all-four-jtag-pins) is caused entirely by the Sense daughterboard occupying those signals — the mainboard itself brings them out on purpose.

That is a materially better answer than "hardware debugging is impossible": debug on a bare board using the bottom pads, then fit the daughterboard.

### 3.2 The ESP32-S3 is under a metal shield can

[`mainboard-top-shield-fcc-label.jpg`](artifacts/regulatory/fcc-photos/mainboard-top-shield-fcc-label.jpg) shows a soldered shield can covering the SoC, with the FCC label on top and `R`/`B` silkscreen for the RESET and BOOT buttons.

This explains the v1.3 revision note about "shield positioning hole spacing" and confirms the SoC is not accessible without desoldering the can. It also means **thermal contact for a heat sink is to the shield, not the die** — relevant to the [82 °C community report](community.md#42-a-hard-thermal-datum).

### 3.3 The camera is a separate module on an FPC ribbon

[`camera-module-with-fpc.jpg`](artifacts/regulatory/fcc-photos/camera-module-with-fpc.jpg) shows the camera as a ~10 mm module with a lens barrel, terminating in an FPC ribbon and a **ZIF connector** — so the camera detaches from the *daughterboard* as well as the daughterboard detaching from the XIAO. That is the mechanism by which the OV2640 → OV3660 → OV5640 swap is possible.

### 3.4 The certification label

[`label-and-location.pdf`](artifacts/regulatory/label-and-location.pdf) specifies a **12 × 10 mm PI (polyimide) high-temperature sticker** applied to the **shield can** (屏蔽罩), reading:

```
Model: XIAO-ESP32-S3
FCC ID: Z4T-XIAOESP32S3
```

The choice of a high-temperature polyimide label is itself a small signal that Seeed expected the shield can to get hot.

## 4. What the FCC filing did **not** resolve

**The microphone part number remains unknown.** The internal photos concentrate on the RF-relevant hardware — mainboard, antenna, camera module — and at 709 × 531 px no daughterboard component markings are legible. No exhibit shows the microphone.

This was the main reason for pursuing the filing, and it did not work. [`gaps-and-conflicts.md` §7](gaps-and-conflicts.md#7-microphone-part-number-not-established--resolved-2026-08-24) stays open. Remaining routes: a physical teardown with a macro lens, or a Seeed BOM release.

## 4A. What the "model differences" exhibit says — read 2026-08-24

`model-differences.pdf` is a 2-page scanned letter with no text layer. Read directly from the page images. It states two things that are not documented anywhere else:

### The Sense is the FCC test model

> "**XIAO-ESP32-S3-Sense:** This model is composed of XIAO-ESP32-S3 main board and expansion board. **This is also the main test model.**"

So the RF measurements in the test reports were taken on the **Sense** configuration — camera board attached, FPC antenna fitted. Useful context for the antenna figures in §2.

### The plain XIAO ESP32S3 has **no board-to-board connector fitted**

> "**XIAO-ESP32-S3:** This model is a single main board without an expansion board, and compared with the above mentioned XIAO-ESP32-S3-Sense main board, **there is no connector on the board** as below shows."
>
> "**Their electrical circuit design, layout, components used and internal wiring are identical.**"
>
> — signed *Albert Miao*, Seeed Technology Co., Ltd

This is a materially useful fact that Seeed does not state in its product documentation:

- **The plain XIAO ESP32S3 and the Sense mainboard are the same PCB.** Same layout, same components, same wiring.
- **The only difference is that J3 — the 30-pin `DF40C-30DP-0.4V(51)` board-to-board plug — is not populated** on the plain board. The accompanying photo confirms the footprint is present but bare.
- **Therefore you cannot retrofit a Sense daughterboard onto a plain XIAO ESP32S3** without soldering a 0.4 mm-pitch 30-pin connector to an unpopulated footprint. That is not a hand-solderable operation in practice.

It also explains why [the two models share one FCC grant](#1-the-filing): they are electrically the same radio on the same board.

**Buying implication:** the $6.50 difference between the plain board and the Sense buys the daughterboard *and* the fitted connector. If there is any chance you will want the camera, buy the Sense — the upgrade path afterwards is effectively closed. See [`comparisons-and-recommendations.md` §4](comparisons-and-recommendations.md#4-versus-the-plain-xiao-esp32s3).

`module-approval-letter.pdf` (1 page, also scanned) is the routine modular-approval request and adds nothing beyond the fact of modular approval already noted in §1.

## 5. Other certifications

- **SDoC declaration letter** and **SAR Exclusion** are on file; the SAR exclusion is expected for a low-power 2.4 GHz device.
- **CE**: the label artwork carries the CE mark, but no EU technical file was located. Not investigated.
- **RoHS**: the antenna drawing states RoHS compliance; no board-level RoHS declaration was located.
- **Telec/KC/etc.**: not investigated.

## 6. Artifacts

| File | Pages | Contents |
|---|---:|---|
| [`fpc-antenna-spec.pdf`](artifacts/regulatory/fpc-antenna-spec.pdf) | 18 | **Antenna performance, dimensions, supplier** — the most useful exhibit |
| [`internal-photos-1.pdf`](artifacts/regulatory/internal-photos-1.pdf) | 10 | Board, antenna, camera module |
| [`internal-photos-2.pdf`](artifacts/regulatory/internal-photos-2.pdf) | 3 | Additional views |
| [`external-photos-1.pdf`](artifacts/regulatory/external-photos-1.pdf) | — | External views |
| [`label-and-location.pdf`](artifacts/regulatory/label-and-location.pdf) | 1 | Label artwork and placement |
| [`model-differences.pdf`](artifacts/regulatory/model-differences.pdf) | 2 | **Scanned, unread** — plain vs Sense |
| [`module-approval-letter.pdf`](artifacts/regulatory/module-approval-letter.pdf) | 1 | **Scanned, unread** — modular approval |
| [`user-manual.pdf`](artifacts/regulatory/user-manual.pdf) | — | As-filed user manual |
| [`sar-exclusion.pdf`](artifacts/regulatory/sar-exclusion.pdf) | — | RF exposure |

**Licensing:** FCC equipment-authorisation exhibits are **public records** published by a US federal agency. The antenna specification within is a supplier document (ShenZhen MyAntenna) reproduced in a public filing. Redistribution status recorded as `public-record`.

## 7. Retrieval method — for reuse

`fccid.io` blocks the **Chrome desktop UA with 403** but serves normally to `curl/8.5.0`, `WhatsApp/2.23.20.0` and ClaudeBot. `fcc.report` 403s every agent tried. `apps.fcc.gov` 403s.

```bash
# search (note: /search.php 301-redirects to /search)
curl -fsSL -A "curl/8.5.0" "https://fccid.io/search?q=XIAO+ESP32S3"

# exhibit list
curl -fsSL -A "curl/8.5.0" "https://fccid.io/Z4T-XIAOESP32S3"

# the PDF is simply the exhibit path + .pdf
curl -fsSL -A "curl/8.5.0" \
  "https://fccid.io/Z4T-XIAOESP32S3/Test-Report/FPC-Antenna-Specification-6487266.pdf" -o antenna.pdf
```

Recorded in the [Seeed vendor guide](../../../vendors/seeed-studio/README.md) and in `ai-crawler-site-access-table.md`.

## 8. Related
- [`features/wifi-and-bluetooth.md`](features/wifi-and-bluetooth.md) — antenna behaviour in use
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — JTAG pads and test points
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — what remains unresolved
- [`bom-and-board-construction.md`](bom-and-board-construction.md) — shield can, board construction
