# 40 MHz crystal `CN4040M000157A530001` — ESP32-S3 main oscillator

> The 4-pad SMD quartz crystal that provides the ESP32-S3's main 40 MHz reference on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), fitted as **`X1`** on schematic sheet 3.
> Research snapshot **2026-09-01**. **No datasheet was found and no manufacturer could be identified** — see [§6](#6-datasheet-search--negative-result). Everything here is either read off the schematic or derived from the ESP32-S3's own requirements.

> This record exists under `components/generic/` because the part could not be attributed to a manufacturer. If the vendor is later identified, move it to `components/<manufacturer>/` and leave a pointer.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet 3, `X1` and neighbours | `executed-success` for the extraction; `not-tested` electrically |
| **[ESP]** | Espressif ESP32-S3 datasheet / hardware design guidelines — held at [`components/espressif/esp32-s3r8/artifacts/`](../../espressif/esp32-s3r8/README.md) | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity — what is actually known

| Property | Value | Evidence |
|---|---|---|
| Marking / value string on the schematic | **`CN4040M000157A530001`** | **[SCH]** sheet 3, adjacent to `X1` |
| Manufacturer | **Unknown.** No vendor claims this part number in any source searched (§6) | — |
| Function | Quartz crystal, ESP32-S3 main crystal oscillator | **[SCH]**, **[ESP]** |
| Frequency | **40 MHz** | **[ESP]** — the ESP32-S3 requires 40 MHz; corroborated by the substring `40M000` in the value string. **[INF]** |
| Package | **4-pad SMD**, two signal pads and two case/ground pads | **[SCH]** — the symbol has four pin markers, pins 1/2 on one side and 3/4 on the other |
| Load capacitance | **Not stated.** Estimated ≈ 12–15 pF from the fitted 24 pF loading capacitors (§3.1) | **[INF]** |

**Nothing above beyond the value string and the pad count is a direct reading of a vendor document.** The frequency is asserted because the ESP32-S3 has exactly one supported main-crystal frequency; the rest is inference or unknown, and is labelled as such.

> ⚠ **Do not decode the part number.** `CN4040M000157A530001` contains recognisable-looking fields — `4040` could be a 4.0 × 4.0 mm package code, `40M000` could be 40.000 MHz, `A5` could be a tolerance grade — but **no vendor scheme was found to confirm any of it.** Reading a package size out of it and ordering a replacement on that basis would be exactly the kind of guess this knowledge base exists to avoid.

---

## 2. Why 40 MHz, and why it is not negotiable **[ESP]**

The ESP32-S3's RF and system clocking are built around a 40 MHz reference. Unlike the original ESP32, which supported 26 MHz and 40 MHz crystals, **the ESP32-S3 supports 40 MHz only.** Fitting anything else does not produce a slow board — it produces a board whose Wi-Fi does not associate and whose UART baud rates are wrong, because the whole PLL tree is scaled from this reference.

This is worth stating in a component record because the crystal is the one part on an ESP32-S3 design where "close enough" is not a category.

---

## 3. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), designator **`X1`**, schematic sheet 3 (`MCU_Core`).

#### 3.1 Exact wiring **[SCH]**

| Node | Connection |
|---|---|
| `X1` pins **3, 4** | `XTAL_P` side → **`L7` = 24 nH** in series → ESP32-S3 (`U12`) **pin 54, `XTAL_P`** |
| `X1` pins **1, 2** | `XTAL_N` side → ESP32-S3 (`U12`) **pin 53, `XTAL_N`** |
| `C45` | **24 pF**, `XTAL_P` to GND |
| `C50` | **24 pF**, `XTAL_N` to GND |

**Load-capacitance arithmetic [INF]:** two 24 pF capacitors in series present C1·C2/(C1+C2) = **12 pF** to the crystal, plus a few pF of board and pin stray — so the fitted crystal's specified load capacitance is most likely **12 pF, or 12–15 pF including strays**. This is the standard arrangement for a 40 MHz ESP32-S3 crystal and is not unusual. It is arithmetic, not a datasheet reading.

#### 3.2 The 24 nH series inductor is a recognised ESP32-S3 practice, not an oddity

`L7` = **24 nH** sits in series in the `XTAL_P` leg. **[SCH]**

A series inductor in a crystal leg looks like a mistake to anyone meeting it for the first time. It is not — and this repository already holds an independent example: the **[Seeed Studio XIAO ESP32S3 Sense](../../../devices/seeed-studio/xiao-esp32s3-sense/README.md)** fits *"a 40 MHz crystal (`X1`, reached through `L5` **24 nH** since board revision v1.2)"*, as recorded in the [ESP32-S3R8 component record](../../espressif/esp32-s3r8/README.md#seeed-studio-xiao-esp32s3-sense).

**Two unrelated vendors, two unrelated boards, the same 24 nH value on the same pin.** That is strong evidence of a common reference design or application-note recommendation rather than a coincidence. The Seeed record notes it appeared at a board revision, which suggests it fixed something.

What it does is not documented in either vendor's material. The plausible readings — none of them confirmed here — are frequency pulling to centre the oscillator, suppression of a spurious overtone mode, or EMI shaping on the crystal edge. **[INF]** Recorded as an observed convergence between two designs; the mechanism is an open question (§7).

> **Which leg carries `L7`** was determined from text-layer adjacency in the Altium PDF (`L7`'s pin markers sit between the `XTAL_P` label and `X1` pin 3). It is the less certain of the two facts here; the presence and value of `L7` are solid, the leg assignment is `inferred`. Read it off the rendered sheet if it matters to you.

#### 3.3 Not to be confused with the other inductors on sheet 3

Sheet 3 carries several small inductors and it is easy to attribute the wrong one **[SCH]**:

| Ref | Value | Role |
|---|---|---|
| `L4` | `LQP03TN2N6B02D`, 2.6 nH | RF matching network, `ANT1` path |
| `L5` | 0 Ω | RF path link |
| `L6` | 2 nH | RF matching network |
| **`L7`** | **24 nH** | **crystal leg — this record** |

`L4`/`L5`/`L6` belong to the antenna matching network with `C39`–`C43` (two positions marked `NC(TBD)`, `GRM0335C1H2R0BA01D` 2.0 pF and `GRM0335C1H1R8BA01D` 1.8 pF), not to the oscillator.

#### 3.4 There is no 32.768 kHz crystal

`GPIO15/XTAL_32K_P` and `GPIO16/XTAL_32K_N` (ESP32-S3 pins 21 and 22) are used as **`G15_SPI2_CLK`** and **`G16_EINK_CS`** — the e-paper SPI bus. **[SCH]**

So the ESP32-S3 has **no external low-power crystal**, and its RTC runs from an internal oscillator when the main crystal is off. That is not a defect on this board: real timekeeping is done by the **RX8130CE** on the I²C bus, which has its own crystal and its own always-on `3V3_L0` supply, and which wakes the system through M5PM1 GPIO0. **[INF]**

The consequence for firmware is worth stating: **do not rely on the ESP32-S3's internal RTC for elapsed time across deep sleep on this board.** Read the RX8130CE.

---

## 4. Drivers and software

**Not applicable.** The crystal is configured by the ESP-IDF bootloader through `CONFIG_XTAL_FREQ` (40 MHz on the S3, and not selectable). No runtime interface exists.

If you are bringing up a board and the crystal is suspect, the observable symptoms are: the ROM bootloader's UART output at a wrong baud rate, `esp_timer` running fast or slow by a fixed ratio, and Wi-Fi failing to associate while everything else appears fine.

---

## 5. Integration pitfalls

1. **40 MHz only on the ESP32-S3** (§2).
2. **Load capacitance must match the crystal.** The 24 pF pair here implies a 12 pF-load part (§3.1). Substituting a crystal specified for a different load with the same capacitors shifts the frequency — typically by tens of ppm, which is enough to break Wi-Fi association margins.
3. **ESR and drive level matter.** A crystal with too high an ESR for the ESP32-S3's oscillator may start intermittently — the classic symptom is "boots warm, fails cold".
4. **Do not reuse `L7`'s value blindly on a board with different layout parasitics** (§3.2). It is evidently a tuning element, and its correct value depends on the board.
5. **There is no 32.768 kHz crystal on this design** (§3.4).

---

## 6. Datasheet search — negative result

**No datasheet, product page, distributor listing or manufacturer attribution was found for `CN4040M000157A530001`.** This is a genuine negative result, not an abandoned search.

Attempts on **2026-09-01**, all with a Chrome 131 desktop User-Agent unless noted:

| Service / host | Query | Result |
|---|---|---|
| `search.brave.com` | `CN4040M000157A530001` | HTTP 429 (rate limited) on two attempts; one earlier query in the same session returned zero relevant results |
| `search.brave.com` | `CN4040M000157A530001+crystal` | HTTP 429 |
| `www.google.com` | `CN4040M000157A530001` | HTTP 200, but JavaScript-gated — no result links in the HTML |
| `duckduckgo.com/html` · `html.duckduckgo.com` | `CN4040M000157A530001` | HTTP 202 challenge page, no results |
| `search.naver.com` | `CN4040M000157A530001` | HTTP 200; only Korean shopping-aggregator links, nothing relevant |
| `www.mojeek.com` | (rate limited before this query) | HTTP 403 |
| `searx.be`, `search.inetol.net`, `priv.au`, `searxng.site`, `opnxng.com` | `CN4040M000157A530001` | HTTP 429 or empty |
| `www.alldatasheet.com` | `Searchword=CN4040M000157A530001` | HTTP 200, no matching part |
| `www.datasheets360.com` | `q=CN4040M000157A530001` | HTTP 403 |
| `www.findchips.com`, `www.oneyac.com` | `CN4040M000157A530001` | HTTP 200 but JavaScript-rendered; the string appears only echoed in page metadata |
| `www.oemsecrets.com` | `compare/CN4040M000157A530001` | HTTP 403 |
| `www.lcsc.com/search?q=...` | — | Returns an identical 97 240-byte JavaScript shell for **every** query; the LCSC search API hosts (`wmsc.lcsc.com/ftps/...`) return HTTP 403 |

**What would resolve it, in order of likely success:**

1. A photograph of the fitted `X1` — SMD crystals carry an abbreviated marking (often just the frequency and a maker logo) that identifies the manufacturer far more reliably than the schematic string.
2. A PaperMono BOM. M5Stack has **not** published one: the `M5_Hardware` repository stops at SKU C152 and contains no C153 directory at all (verified exhaustively — `git ls-tree -r --name-only HEAD | grep -iE 'papermono|c153'` returns nothing).
3. LCSC's product-detail HTML for the part, if a part code can be found by another route. LCSC's search is unusable to automated clients but `https://www.lcsc.com/product-detail/<CODE>.html` does serve a `pdfUrl` field once you have the code.

**What is *not* affected by this gap:** the electrical requirements (§2), the wiring (§3.1) and the integration rules (§5) are all fully established from the schematic and Espressif's documentation. A missing crystal datasheet does not block using or repairing this board — it blocks sourcing an exact replacement.

---

## 7. Open questions

- Manufacturer and datasheet (§6).
- The crystal's specified load capacitance, ESR and frequency tolerance — all unknown; §3.1's 12 pF is arithmetic from the fitted capacitors.
- **What `L7` is for**, and why the same 24 nH value appears on an unrelated Seeed ESP32-S3 board (§3.2). This is the most interesting question in this record, because the answer would apply to every ESP32-S3 design.
- Which crystal leg `L7` is in (§3.2) — established only by text-layer adjacency.
- Whether the package is 3.2 × 2.5 mm or 2.0 × 1.6 mm; the schematic symbol does not carry a footprint name in the extracted text.

---

## Related pages

- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the host, and the source of the 40 MHz requirement; its Seeed XIAO section records the matching 24 nH inductor
- Seiko Epson RX8130CE (record pending; `components/seiko-epson/rx8130ce/`) — the board's actual timekeeper, which does have its own crystal
- [Generic ceramic antenna record](../../generic/ceramic-antenna/README.md) — the RF matching network on the same schematic sheet

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 2026-05-22, 6 sheets | The value string `CN4040M000157A530001`, the 4-pad symbol, `C45`/`C50` = 24 pF, `L7` = 24 nH, connection to `U12` pins 53/54, and the absence of a 32.768 kHz crystal | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | ESP32-S3 Series Datasheet | Espressif | primary | datasheet | <https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf> | 2026-08-21 (existing repository copy) | v2.2, 87 pp | The 40 MHz main-crystal requirement | `components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` |
| S3 | ESP Hardware Design Guidelines (ESP32-S3) | Espressif | primary | manual | <https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/esp-hardware-design-guidelines-en-master-esp32s3.pdf> | 2026-08-21 (existing repository copy) | esp-docs `master` build | Crystal and load-capacitor guidance | `components/espressif/esp32-s3r8/artifacts/esp32-s3-hardware-design-guidelines.pdf` |
| S4 | XIAO ESP32S3 Sense crystal note | this repository | — | derived record | — | 2026-09-01 | — | The independent 24 nH observation in §3.2 | [`components/espressif/esp32-s3r8/README.md`](../../espressif/esp32-s3r8/README.md#seeed-studio-xiao-esp32s3-sense) |

**Local artifacts:** none. No document specific to this part was obtained (§6).

**Method note.** The pin/net table in §3.1 was recovered by parsing the Altium PDF's invisible component-outline and pin-instance markers and reading the human-readable text sharing each marker's row band. That recovers text adjacency, not electrical connectivity, which is why §3.2's leg assignment is marked `inferred` while the component values are not.
