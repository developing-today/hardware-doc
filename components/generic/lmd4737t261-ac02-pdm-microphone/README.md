# LMD4737T261-AC02 — PDM MEMS microphone

> The single digital MEMS microphone fitted to the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), designator **`U1`** on schematic sheet 5 (the KEY / RGB / PDM sub-board). A **PDM** (pulse-density modulation) part with a `SELECT` channel-select pin, powered from a switched rail.
> Research snapshot **2026-09-01**. **No datasheet, product page, distributor listing or manufacturer attribution could be found** — see [§5](#5-datasheet-search--negative-result). Everything below is read off the schematic, M5Stack's own specification, or M5Stack's firmware.

> This record lives under `components/generic/` because the manufacturer is unidentified. Move it to `components/<manufacturer>/` if that changes.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | M5Stack source at a cited `file:line` | `executed-success` for the read |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[ESP]** | ESP32-S3 datasheet, held at [`components/espressif/esp32-s3r8/artifacts/`](../../espressif/esp32-s3r8/README.md) | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity — what is actually known

| Property | Value | Evidence |
|---|---|---|
| Marking / value string | **`LMD4737T261-AC02`** | **[SCH]** sheet 5, next to `U1`; **[DOC]** verbatim in the product specification |
| Manufacturer | **Unknown** (§5) | — |
| Function | **PDM digital MEMS microphone** | **[SCH]** pin names; **[DOC]** *"PDM microphone (LMD4737T261-AC02)"* |
| Package | **6 pin/pad** bottom-port or top-port MEMS package (port orientation not established) | **[SCH]** — six pin markers |
| Supply | `PDM_VDD` — a switched **3.3 V** rail (§3.2) | **[SCH]** |
| Interface | **PDM**, single data line plus clock, with a channel-`SELECT` pin | **[SCH]** |

**That is the complete list of established facts about the part itself.** Sensitivity, SNR, AOP, frequency response, current consumption, clock range, `SELECT` polarity and the port location are all **unknown** and are not guessed here.

> ⚠ **Do not infer specifications from the part number.** `LMD4737T261-AC02` looks decomposable — `4737` could be a package dimension, `T261` a variant code, `-AC02` a revision — but no vendor scheme was found to confirm any reading (§5).

---

## 2. What can be said generically about PDM MEMS microphones

Since the specific part is undocumented, this section states what is true of the *class*, so that the board integration below is interpretable. **None of it is verified for this part.** **[INF]** throughout.

- A PDM microphone outputs a **1-bit oversampled bitstream** on a single data line, clocked by the host. There is no register interface, no address, and no configuration.
- Typical host clock is **1–3.25 MHz**; most parts also define a **sleep** threshold (clock below a few tens of kHz) and enter a low-power state.
- **`SELECT` (also called `L/R`) chooses which clock phase the microphone drives.** Two microphones can share one data line: one tied low drives on the low phase, one tied high drives on the high phase. On a mono design the pin still has to be tied deliberately, because it decides *which half of each clock period* the data is valid in — and the host's PDM receiver must be configured to match.
- Output is high-Z on the phase the part is not driving, which is what makes the two-microphone sharing work.
- Decimation to PCM is the host's job — on the ESP32-S3 this is done by the I²S peripheral in PDM RX mode.

---

## 3. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), designator **`U1`**, schematic **sheet 5** (`PaperMono KEY RGB.SchDoc`, dated 2026-04-14).

Sheet 5 is a **separate sub-board** carrying the two user keys, the power button, the RGB indicator LED and this microphone. It connects to the mainboard through a 12-way (+4 mount) board-to-board pair: **`J1` = `AXE612124D`** on the sub-board, mating with **`J6` = `AXE512127D`** on sheet 4. **[SCH]**

#### 3.1 Pinout as drawn **[SCH sheet 5]**

| Pin | Name | Net |
|---:|---|---|
| 1 | `GND` | `GND` |
| **2** | **`SELECT`** | ⚠ **not resolved** — see §3.4 |
| 3 | `GND` | `GND` |
| **4** | **`CLK`** | `G45_PDM_CLK` ← **`R4` = 22 Ω/1 %** ← ESP32-S3 **GPIO45** |
| **5** | **`DAT`** | `G46_PDM_DAT` → **`R3` = 22 Ω/1 %** → ESP32-S3 **GPIO46** |
| 6 | `VDD` | **`PDM_VDD`** ← **`L1` = 2 nH** (ferrite/inductor), with **`C2` = 100 nF/10 V** decoupling |

Both signals cross the board-to-board connector: `J1`/`J6` pin **11** = `G46_PDM_DAT`, pin **12** = `G45_PDM_CLK`, pin **2** = `PDM_VDD`. **[SCH]**

The 22 Ω series resistors on both lines are edge-rate damping — sensible on a signal pair that crosses a connector at megahertz rates.

#### 3.2 The rail is switched, and that turns out to matter a great deal

`PDM_VDD` is produced by **[`U21`, an AW35122FDR load switch](../../awinic/aw35122/README.md)** on sheet 4, from `3V3_L2`, enabled by **M5IOE1 `PYG12`**. **[SCH]**

| Layer | Identifier | Evidence |
|---|---|---|
| Schematic enable net | `PYB_PDM_EN` | **[SCH]** `U17` pin 5/16 |
| M5IOE1 pin | `PYG12` → `M5IOE1_PIN_12`, enum value **11** | **[DOC]**, **[SRC]** |
| Firmware constant | `PDM_EN_PIN = M5IOE1_PIN_12` | **[SRC]** `hal_mic.cpp:13`, `hal_board.cpp:30` |
| Decoupling | `C85` = 10 µF/10 V on the switch output | **[SCH]** |

So the microphone is off unless firmware has explicitly turned it on over I²C, and it disappears entirely in the `L2 DeepSleep` power state. Sheet 1 lists `PDM_VDD` among the `L3B` rails.

#### 3.3 ⚠ Both PDM signals land on ESP32-S3 **strapping pins**

This is the most consequential integration fact on this record, and it is not documented by M5Stack.

| Net | ESP32-S3 pin | Strap function **[ESP §3]** | Default |
|---|---|---|---|
| `G45_PDM_CLK` | **GPIO45** | **`VDD_SPI` voltage select** | Weak pull-**down**, bit value **0** → `VDD_SPI` = **3.3 V** from `VDD3P3_RTC` |
| `G46_PDM_DAT` | **GPIO46** | **ROM messages printing control** | Weak pull-**down**, bit value **0** |

The schematic labels both accordingly: `GPIO45[strap]` and `GPIO46[strap]` on sheet 3. **[SCH]**

**Why GPIO45 is the dangerous one.** Per **[ESP]** Table 3-4, with `EFUSE_VDD_SPI_FORCE = 0` (the default), a **GPIO45 sampled high at reset selects `VDD_SPI` = 1.8 V**. `VDD_SPI` is the supply for the board's [XM25UH128DHIQT flash](../../xmc/xm25uh128dhiqt/README.md), which is a **2.3–3.6 V** part. A board that latched that strap high would come up with an under-volted flash and would not boot — with no diagnostic, because the failure is upstream of any code that could report it.

**Why this board is safe, and what would break it.** `CLK` is an ESP32-S3 **output** and a microphone **input**, so the microphone never drives GPIO45. GPIO46 is the reverse — the microphone drives it — but **`PDM_VDD` is off at reset** (§3.2), so the microphone is unpowered and its output is high-Z, leaving GPIO46 to its internal weak pull-down. The strapping latches sample at Chip Reset and hold until power-down **[ESP §3]**.

> ⚠ **The protection is the load switch, not the wiring.** Firmware that leaves `PDM_VDD` enabled across a soft reset re-exposes GPIO46 to whatever the microphone's `DAT` pin does while unclocked. That changes only the ROM-message destination, so it is a nuisance rather than a brick — but it is the kind of thing that makes "sometimes there is no boot log" reproducible only after using the microphone. **[INF]**

**Reusing these two GPIOs on a derivative design is where the real risk sits.** GPIO45 is a poor choice for anything that can be driven high by an external device at power-up.

#### 3.4 ⚠ `SELECT` is unresolved

The schematic symbol names pin 2 `SELECT`, but the **external net was not recovered** from the PDF text layer — the words `GND` adjacent to it in the extraction are the symbol's own pin *names* for pins 1 and 3, not necessarily pin 2's net. **[SCH]**

This is not a cosmetic gap. `SELECT` determines which clock phase the microphone drives (§2), and the ESP32-S3's I²S PDM receiver must be configured for the matching phase — get it wrong and you capture silence or noise, not quiet audio. M5Stack's `hal_mic.cpp` configures the I²S peripheral, so the answer is recoverable from firmware; it was not extracted in this pass.

Recorded as an open question rather than assumed to be grounded (§6).

#### 3.5 Firmware

| Constant | Value | Source |
|---|---|---|
| `MIC_PDM_CLK_PIN` | **45** | `hal_mic.cpp:17` **[SRC]** |
| `MIC_PDM_DATA_PIN` | **46** | `hal_mic.cpp:16` **[SRC]** |
| `PDM_EN_PIN` | `M5IOE1_PIN_12` | `hal_mic.cpp:13` **[SRC]** |

M5Stack's UserDemo includes a "mic wave" application among its fifteen demos, and the documentation site lists a `mic` API sub-page (not retrieved). **[SRC]**, **[DOC]**

On ESP-IDF the receiver is the **I²S peripheral in PDM RX mode** (`i2s_pdm_rx`), which handles clock generation and decimation to PCM. No microphone driver exists or is needed — there is nothing to configure in the part.

---

## 4. Integration pitfalls

1. **Enable `PDM_VDD` before expecting data** (§3.2). An I²S PDM RX channel reading an unpowered microphone returns a stable, plausible-looking constant — not an error.
2. **Match the I²S PDM slot to the `SELECT` strap** (§2, §3.4). The classic symptom of a mismatch is "the microphone works but the level is wrong / the audio is garbage".
3. **GPIO45 is the `VDD_SPI` strap** (§3.3). Do not reuse it for anything that can drive high at reset.
4. **Do not leave `PDM_VDD` on across a reset** if you care about ROM boot messages (§3.3).
5. **PDM needs a continuous clock.** Stopping the clock puts most PDM microphones into a sleep state with a wake-up time of tens of milliseconds; the first samples after restarting the clock are not valid. **[INF]** — generic behaviour, unverified for this part.
6. **There is no gain control, no register interface and no identification.** You cannot detect the microphone's presence in software; a dead microphone and a disabled rail look identical.

---

## 5. Datasheet search — negative result

**No datasheet, product page, distributor listing or manufacturer attribution was found for `LMD4737T261-AC02` or `LMD4737T261`.** This is a genuine negative result.

Attempts on **2026-09-01**, Chrome 131 desktop User-Agent unless noted:

| Service / host | Query | Result |
|---|---|---|
| `search.brave.com` | `LMD4737T261+microphone+datasheet` | HTTP 200 — **zero** results for the part. Returned generic PDM-microphone material instead: Adafruit PDM breakout, Analog Devices ADMP401/ADMP521, ST MP34DT06J / MP45DT02, TDK MEMS catalogue, Knowles selection guide |
| `search.brave.com` | `LMD4737T261-AC02+PDM+microphone` | HTTP 200 — results are all **M5Stack's own pages** (`docs.m5stack.com`, `shop.m5stack.com`), a CNX-Software article, and The Pi Hut's listing. The string exists on the web **only** because M5Stack publishes it |
| `search.brave.com` | `LMD4737T261` | HTTP 429 (rate limited) |
| `search.naver.com` | `LMD4737T261` | HTTP 200 — four links, all M5Stack shop/doc pages or `manuals.plus` copies of them |
| `www.google.com` | `LMD4737T261` | HTTP 200 but JavaScript-gated; no result links in the HTML |
| `duckduckgo.com/html`, `html.duckduckgo.com` | `LMD4737T261` | HTTP 202 challenge page |
| `www.mojeek.com` | `LMD4737T261` | HTTP 403 |
| `searx.be`, `search.inetol.net`, `priv.au`, `searxng.site`, `opnxng.com` | `LMD4737T261` | HTTP 429 or empty |
| `api.qwant.com/v3/search/web` | `LMD4737T261` | HTTP 403 |
| `www.alldatasheet.com` | `Searchword=LMD4737T261` | HTTP 403 |
| `www.datasheets360.com` | `q=LMD4737T261` | HTTP 403 |
| `www.findchips.com`, `www.oneyac.com` | `LMD4737T261-AC02` | HTTP 200 but JavaScript-rendered; the string appears only echoed in page metadata |
| `www.oemsecrets.com` | `compare/LMD4737T261-AC02` | HTTP 403 |
| `www.lcsc.com/search` | `LMD4737T261` | Identical 97 240-byte JavaScript shell returned for every query; the LCSC search API hosts return HTTP 403 |

**The finding inside the negative result:** the only occurrences of this part number anywhere on the indexed web are **M5Stack's own specification text and pages that copy it.** No manufacturer publishes it, no distributor stocks it under that name. That pattern is consistent with a house part number, a customer-specific marking, or a part sold only through Chinese domestic channels that the searched indexes do not cover.

**What would resolve it, in order of likely success:**

1. **A photograph of the fitted `U1`.** MEMS microphones carry a small laser marking that usually identifies the maker.
2. A PaperMono BOM. M5Stack has not published one — the `M5_Hardware` repository stops at SKU C152 and contains no C153 directory (verified exhaustively).
3. Chinese-language search on Baidu or 1688/Alibaba domestic listings, which were not effectively reachable from this session.
4. Comparing the schematic's 6-pin symbol and pad geometry against known MEMS microphone footprints, if the PCB files ever appear.

**What is *not* blocked by this gap:** the wiring, the power control, the strapping-pin hazard and the firmware pin map are all fully established (§3). What is blocked is any statement about audio quality, current draw, or the valid clock range — which is why none is made.

---

## 6. Open questions

- Manufacturer and datasheet (§5).
- **The `SELECT` net and therefore the correct I²S PDM slot** (§3.4). Recoverable from `hal_mic.cpp`'s I²S configuration; not extracted this pass. This is the highest-value cheap follow-up.
- Sensitivity, SNR, acoustic overload point, supply current, valid clock range, wake-up time — all unknown.
- Port orientation (top or bottom) and therefore what the enclosure acoustic path looks like.
- Whether the 2 nH `L1` in the supply is a ferrite bead (RF decoupling) or an actual inductor; the schematic value string says `2nH`.
- No hardware measurement of anything.

---

## Related pages

- [Awinic AW35122](../../awinic/aw35122/README.md) — `U21`, the load switch producing `PDM_VDD`
- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — owns `PYG12`
- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the I²S PDM receiver, and the owner of the two strapping pins
- [XMC XM25UH128DHIQT](../../xmc/xm25uh128dhiqt/README.md) — the flash whose supply the GPIO45 strap selects
- [MEMSensing MSM261D4030H1CPM](../../memsensing/msm261d4030h1cpm/README.md) · [MSM261D3526H1CPM](../../memsensing/msm261d3526h1cpm/README.md) — comparable PDM MEMS microphones documented in this repository, useful as a reference for what a datasheet for this class contains
- [RS-C1415MBAR RGB LED](../rs-c1415mbar-rgb-led/README.md) — the other undocumented part on the same sub-board

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, sheet 5 dated 2026-04-14 | The value string, six-pin symbol with `GND`/`SELECT`/`GND`/`CLK`/`DAT`/`VDD`, `R3`/`R4` = 22 Ω, `L1` = 2 nH, `C2` = 100 nF, the `J1`/`J6` board-to-board mapping | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | PaperMono product page | M5Stack | primary | official page | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | — | *"PDM microphone LMD4737T261-AC02"* in the specification table | `scratch/m5stack-papermono/docs/pages/en-core-PaperMono.html` |
| S3 | `M5PaperMono-UserDemo/main/hal/hal_mic.cpp`, `hal_board.cpp` | M5Stack | primary | repository | <https://github.com/m5stack/M5PaperMono-UserDemo> | 2026-09-01 | `main` @ `c1099107271d31a0678d661a896e2b04dbb331ea`, MIT | `MIC_PDM_CLK_PIN = 45`, `MIC_PDM_DATA_PIN = 46`, `PDM_EN_PIN = M5IOE1_PIN_12` | `scratch/m5stack-papermono/repos/M5PaperMono-UserDemo/` |
| S4 | ESP32-S3 Series Datasheet §3, Tables 3-1 and 3-4 | Espressif | primary | datasheet | <https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf> | 2026-08-21 (existing repository copy) | v2.2, 87 pp | GPIO45/GPIO46 strapping defaults and the `VDD_SPI` voltage-control table in §3.3 | `components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` |

**Local artifacts:** none. No document specific to this part exists to store (§5).

**Method note.** The pin table in §3.1 was recovered by parsing the Altium PDF's invisible pin-instance markers and reading the human-readable text sharing each marker's row band. That recovers text adjacency, not connectivity — which is precisely why `SELECT`'s net is marked unresolved (§3.4) rather than reported as `GND`.
