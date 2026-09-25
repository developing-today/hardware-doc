# RS-C1415MBAR — side RGB indicator LED

> The three-die RGB indicator on the side of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) body, fitted as **`LED1`** on schematic sheet 5. A four-terminal common-cathode RGB LED with three individual series resistors.
> Research snapshot **2026-09-01**. **No datasheet or manufacturer attribution could be found** — see [§6](#6-datasheet-search--negative-result).

> **Headline finding:** this is **not** a fully addressable RGB indicator. The red die is driven from the [M5PM1](../../m5stack/m5pm1/README.md)'s `LED_EN_PP`, **which has no PWM mode**, while green and blue are on [M5IOE1](../../m5stack/m5ioe1/README.md) PWM channels. Red is therefore on/off only, and the achievable colour set is limited. M5Stack documents this — see [§4.3](#43--red-is-onoff-only-and-that-limits-the-colour-set).

> This record lives under `components/generic/` because the manufacturer is unidentified. Move it to `components/<manufacturer>/` if that changes.

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | M5Stack source at a cited `file:line` | `executed-success` for the read |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity — what is actually known

| Property | Value | Evidence |
|---|---|---|
| Marking / value string | **`RS-C1415MBAR`** | **[SCH]** sheet 5, next to `LED1` |
| Manufacturer | **Unknown** (§6) | — |
| Function | **RGB indicator LED**, three dies in one package | **[DOC]**; **[SCH]** |
| Terminals | **4** — three anodes plus a common cathode (§3.1) | **[SCH]** |
| Configuration | **Common cathode**, high-side driven | **[SCH]** — pin 2 is the only pin on `GND` |
| Package | Not established. A `1415` field in the part number *may* denote 1.4 × 1.5 mm, but no vendor scheme was found to confirm it | — |

**Forward voltages, luminous intensity, viewing angle, maximum forward current, colour coordinates and thermal ratings are all unknown** and are not guessed here.

> ⚠ **Do not decode the part number.** `RS-C1415MBAR` has fields that invite interpretation — `1415` as a package size, `MBAR` as a colour/bin code — but **no vendor scheme was found to confirm any of it** (§6).

---

## 2. Why this part matters more than a typical indicator LED

On most boards an RGB indicator is a footnote. Here it is not, for two reasons:

1. **The three dies are driven by two different chips**, on two different power domains, with two different capabilities (§4).
2. **It is the primary user-visible status output on a device whose display takes 0.07–4.71 s to refresh.** M5Stack's own download-mode instruction is *"press and hold the power button until the **red LED** blinks"* — i.e. the red die is the indicator that tells you the boot state before any code runs. **[DOC]**

---

## 3. Wiring **[SCH sheet 5]**

`LED1` sits on the **KEY / RGB / PDM sub-board** (`PaperMono KEY RGB.SchDoc`, dated 2026-04-14), together with the two user keys, the power button and the [PDM microphone](../lmd4737t261-ac02-pdm-microphone/README.md). It reaches the mainboard through the 12-way (+4 mount) board-to-board pair **`J1` = `AXE612124D`** ↔ **`J6` = `AXE512127D`** (sheet 4).

### 3.1 Terminals and series resistors

| `LED1` pin | Die | Series resistor | Driven from | Domain |
|---:|---|---|---|---|
| **1** | **Green** | **`R7` = 820 Ω / 1 %** | `PYB_LED_G` | M5IOE1 |
| **2** | **Common cathode** | — | `GND` | — |
| **3** | **Blue** | **`R6` = 560 Ω / 1 %** | `PYB_LED_B` | M5IOE1 |
| **4** | **Red** | **`R8` = 1 kΩ / 1 %** | `PY_LED_R` | **M5PM1** |

Board-to-board mapping **[SCH]**: `J1`/`J6` pin **5** = `PY_LED_R`, pin **7** = `PYB_LED_G`, pin **9** = `PYB_LED_B`. `C5` = 10 µF/10 V decouples the sub-board's `3V3_L2` feed.

### 3.2 What the resistor values imply

Three different values for three dies is the normal way to balance an RGB indicator, because red, green and blue dies have different forward voltages and different luminous efficiencies. **[INF]**

Rough current estimates, assuming a 3.3 V drive and typical die forward voltages (V<sub>F</sub> ≈ 2.0 V red, ≈ 3.0 V green and blue) — **arithmetic only, the die V<sub>F</sub> values are not from any datasheet**:

| Die | R | Approx. current |
|---|---:|---:|
| Red | 1 kΩ | ≈ 1.3 mA |
| Green | 820 Ω | ≈ 0.4 mA |
| Blue | 560 Ω | ≈ 0.5 mA |

These are **sub-milliamp to low-milliamp** currents — an indicator sized for a battery device and for reading in a dark room, not a torch. The absolute values depend entirely on the unknown V<sub>F</sub>, and near the knee of a diode's curve a 0.2 V error in V<sub>F</sub> changes the current by tens of percent, so treat them as order-of-magnitude only. **[INF]**

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), designator **`LED1`**, schematic sheet 5. Described by M5Stack as *"the RGB LED indicator on the side of the PaperMono body"*. **[DOC]**

#### 4.1 The three channels, in full

| Die | Net | Driver | Pin | Capability | Power domain |
|---|---|---|---|---|---|
| **Red** | `PY_LED_R` | **[M5PM1](../../m5stack/m5pm1/README.md)** `U7` **pin 5** | `LED_EN_PP` | **On/off only — no PWM** | `3V3_L0`-domain logic; lights per M5PM1 default behaviour at power-on |
| **Green** | `PYB_LED_G` | **[M5IOE1](../../m5stack/m5ioe1/README.md)** `U17` **pin 12** | **`PYG8_PWM2`** | PWM, channel 2 | `3V3_L2` |
| **Blue** | `PYB_LED_B` | **M5IOE1** `U17` **pin 13** | **`PYG9_PWM1`** | PWM, channel 1 | `3V3_L2` |

Corroborated three ways — the schematic **[SCH]**, M5Stack's PinMap **[DOC]**, and the firmware **[SRC]**:

```
RGB_GREEN_PIN = M5IOE1_PIN_8   →  M5IOE1_PWM_CH2     hal_board.cpp:25, :27
RGB_BLUE_PIN  = M5IOE1_PIN_9   →  M5IOE1_PWM_CH1     hal_board.cpp:26, :28
RGB_PWM_FREQ_HZ = 5000                               hal_board.cpp:24
```

The M5IOE1 library's own channel table matches the documentation's suffixes exactly — `M5IOE1_PWM_CH2 // IO8` and `M5IOE1_PWM_CH1 // IO9`. **[SRC]**

#### 4.2 Note the PWM channel numbers are crossed

Green is on **PWM channel 2** (`PYG8_PWM2`) and blue on **PWM channel 1** (`PYG9_PWM1`) — the channel numbers run opposite to the pin numbers. This is a real ordering in M5Stack's silicon mapping, not a transcription error, and it is confirmed by both the documentation and the library header. Anyone writing directly to `M5IOE1_REG_PWM1_DUTY_L` (`0x1B`) expecting green will get blue. **[SRC]**

#### 4.3 ⚠ Red is on/off only, and that limits the colour set

M5Stack states the constraint plainly:

> *"The RGB LED indicator on the side of the PaperMono body consists of three color LED dies, with the red LED connected to `LED_EN_PP` of the M5PM1. After the device is powered on, it will light up according to the M5PM1 default behavior. **Since `LED_EN_PP` does not support PWM output mode configuration, the adjustable colors of this indicator will be limited.**"* **[DOC]**

The schematic corroborates the pin: `PY_LED_R` reaches **M5PM1 `U7` pin 5**, whose symbol name is `LED_EN_PP` — a plain push-pull output, distinct from the M5PM1's PWM-capable `G3`/`G4` pins. **[SCH]**

**What this actually costs you.** With red as a one-bit channel and green/blue as continuous ones, the reachable colour space collapses to **two surfaces rather than a volume**:

| Red state | Reachable colours |
|---|---|
| **Off** | The full green↔blue plane: green, cyan, blue, and every mix — continuously dimmable |
| **On** | Red at exactly one intensity, plus any green/blue mix on top of it: orange, pink, magenta, white-ish — but always with the same fixed red component |

So the things you **cannot** do are: dim red, fade red in or out, produce a *dim* warm colour, or produce a colour whose red component sits between "none" and "full". A smooth red breathing pulse — the single most common firmware idiom for a status LED — is not achievable. **[INF]**

**And there is a second-order effect.** The red die's fixed contribution is set by `R8` = 1 kΩ (§3.1). Once red is on, every colour containing it is anchored to that one red level; the perceived hue of "white" and "pink" is fixed by a resistor value, not by firmware.

**Practical guidance for firmware on this board:**

- Use **green/blue for continuous state** (progress, breathing, level indication) and **red purely as a binary alarm or mode flag**.
- Do not attempt gamma-corrected colour blending that assumes three PWM channels; the result will be wrong in the red axis by construction.
- Do not design a UI that depends on distinguishing "dim red" from "bright red".

#### 4.4 Red and green/blue are on different power domains, so they die at different times

`PY_LED_R` comes from the M5PM1, which runs on the always-on `3V3_L0` rail. `PYB_LED_G` / `PYB_LED_B` come from the M5IOE1, which runs on `3V3_L2` — a rail that is switched off in `L1 Standby` and `L0 Shipping`. **[SCH]**

**Consequence:** in low-power states **red is the only channel that can be lit.** This is consistent with M5Stack's power-tree documentation, which lists *"RGB red"* among the L2/L3A loads and the whole *"RGB LED"* among the L3B loads — the red die is reachable from a lower power state than the other two. **[DOC]** It is also why the download-mode indicator is specifically the *red* LED (§2): at that point the M5IOE1 may not be running.

#### 4.5 Board variant detection depends on this LED

`M5PaperMono-UserDemo/main/hal/hal_board.cpp:160–172` distinguishes the PaperMono (C153) from the PaperMono-Lite (C153-Lite) at runtime, and **the first test is whether the RGB LED came up**:

```c
160: void Hal::detectBoardVariant()
162:     if (!_rgb_ready) { _board_variant = BoardVariant::Lite; return; }
```

followed by an attempt to power the NFC rail. **[SRC]** So a hardware fault on the M5IOE1 PWM channels does not merely lose the indicator — it makes a Pro board report itself as a Lite.

#### 4.6 Not to be confused with `LED1` on sheet 2

There is a **second** designator `LED1` on schematic **sheet 2**, in the charger block, associated with the [IP2315](../../injoinic/ip2315/README.md)'s `LED1`/`LED3` battery-level indicator pins. **[SCH]** It is a different component on a different sheet with the same reference designator — a consequence of the board being drawn as several independent Altium documents. This record is about the **sheet 5** `LED1`.

---

## 5. Drivers and software

**No component-level driver** — three LED dies with series resistors. On the PaperMono:

```cpp
// green and blue, via the M5IOE1 PWM channels
ioe1.setPwmFrequency(5000);
ioe1.analogWrite(M5IOE1_PIN_8, duty);   // green, PWM channel 2
ioe1.analogWrite(M5IOE1_PIN_9, duty);   // blue,  PWM channel 1

// red, via the M5PM1 — on/off only
pm1.setLedEnLevel(true);
```

> ⚠ **Pin-numbering trap.** M5IOE1 labels are 1-based, enum values 0-based — `M5IOE1_PIN_8 == 7` (`M5IOE1/src/M5IOE1.h`). Use the enum, never the raw number from documentation. **[SRC]**

`pm1.setLedEnLevel(bool)` is also called during shutdown sequences to hold the red LED state across an M5PM1 power-off, alongside `ldoSetPowerHold()`. **[DOC]**

Note that both the M5PM1 and the M5IOE1 also expose **NeoPixel** register blocks (`M5PM1_REG_NEO_*` at `0x50`/`0x60`–`0x9F`, `M5IOE1_REG_LED_*` at `0x24`/`0x30`–`0x6F`). **Those are not this part** — they drive addressable serial LEDs, which the PaperMono does not fit. They are generic features of M5Stack's firmware, present on this board but unused for `LED1`. **[INF]**

---

## 6. Datasheet search — negative result

**No datasheet, product page, distributor listing or manufacturer attribution was found for `RS-C1415MBAR`.** Genuine negative result.

Attempts on **2026-09-01**, Chrome 131 desktop User-Agent unless noted:

| Service / host | Query | Result |
|---|---|---|
| `search.brave.com` | `RS-C1415MBAR` | HTTP 429 (rate limited) on two attempts |
| `search.brave.com` | `RS-C1415MBAR+RGB+LED+datasheet` | HTTP 429 |
| `search.naver.com` | `RS-C1415MBAR` | HTTP 200 — three links, none relevant: a Korean marketplace, a Korean parts index, and a made-in-china listing for an unrelated **Nationstar RS-3535 RGB LED** |
| `www.google.com` | `RS-C1415MBAR` | HTTP 200 but JavaScript-gated; no result links in the HTML |
| `duckduckgo.com/html`, `html.duckduckgo.com` | `RS-C1415MBAR` | HTTP 202 challenge page |
| `www.mojeek.com` | `RS-C1415MBAR` | HTTP 403 |
| `searx.be`, `search.inetol.net`, `priv.au`, `searxng.site`, `opnxng.com` | `RS-C1415MBAR` | HTTP 429 or empty |
| `api.qwant.com/v3/search/web` | `RS-C1415MBAR` | HTTP 403 |
| `www.alldatasheet.com` | `Searchword=RS-C1415MBAR` | HTTP 403 |
| `www.datasheets360.com` | `q=RS-C1415MBAR` | HTTP 403 |
| `www.findchips.com`, `www.oneyac.com` | `RS-C1415MBAR` | HTTP 200 but JavaScript-rendered; string echoed only in page metadata |
| `www.oemsecrets.com` | `compare/RS-C1415MBAR` | HTTP 403 |
| `www.lcsc.com/search` | `RS-C1415MBAR` | Identical 97 240-byte JavaScript shell returned for every query; LCSC's search API hosts return HTTP 403 |

**One weak lead, recorded but not endorsed.** The Naver search surfaced *"Nationstar RS-3535 RGB LED"* — Nationstar Optoelectronics (国星光电) uses an `RS-` prefix for RGB LED product lines. That is a **prefix coincidence, not an identification**, and `RS-C1415MBAR` does not appear in any Nationstar material found. It is noted only so the next agent can rule it in or out quickly rather than rediscovering the same hint.

**What would resolve it, in order of likely success:**

1. **A photograph of the fitted `LED1`.** RGB LED packages of this size are usually unmarked, so this may not help — but the package outline would at least establish the dimensions.
2. A PaperMono BOM. M5Stack has not published one — `M5_Hardware` stops at SKU C152 and has no C153 directory (verified exhaustively).
3. A Chinese-language search on Baidu or 1688 domestic listings; not effectively reachable from this session.
4. Searching Nationstar's own catalogue for a `C1415` series.

**What is *not* blocked:** everything that matters for firmware — the pin map, the driver assignment, the PWM channels, the red-channel limitation and the power-domain split (§4) — is fully established. What is blocked is the photometric and electrical specification, which is why §3.2's currents are labelled as estimates.

---

## 7. Open questions

- Manufacturer and datasheet (§6); whether the Nationstar `RS-` prefix lead goes anywhere.
- Forward voltages, and therefore the actual per-die currents (§3.2).
- Package dimensions and whether it is top- or side-emitting — the indicator is described as being *"on the side of the body"*, which usually implies a side-emitting package or a light pipe, but that was not established. **[INF]**
- What the M5PM1's *"default behavior"* for the red LED at power-on actually is (**[DOC]** says only that it exists).
- Whether M5GFX or M5Unified expose a colour API that hides the red-channel limitation, or whether applications must handle it.
- No hardware measurement or photograph.

---

## Related pages

- [M5Stack M5PM1](../../m5stack/m5pm1/README.md) — drives the red die from `LED_EN_PP`; `setLedEnLevel()`
- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — drives green and blue from `PYG8_PWM2` / `PYG9_PWM1`
- [LMD4737T261-AC02 PDM microphone](../lmd4737t261-ac02-pdm-microphone/README.md) — the other undocumented part on the same sub-board
- [Normand SK6805-EC20](../../normand/sk6805-ec20/README.md) — an addressable RGB LED documented in this repository, for contrast with this simple three-die part

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, sheet 5 dated 2026-04-14 | The value string, four-terminal common-cathode topology, `R6` = 560 Ω / `R7` = 820 Ω / `R8` = 1 kΩ, `PY_LED_R` → M5PM1 `U7` pin 5 `LED_EN_PP`, `PYB_LED_G`/`PYB_LED_B` → M5IOE1 `U17` pins 12/13, the `J1`/`J6` mapping | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | PaperMono product page — HMI PinMap and RGB note | M5Stack | primary | official page | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | — | The verbatim `LED_EN_PP` / no-PWM limitation quoted in §4.3; `PYG8_PWM2` / `PYG9_PWM1`; the red-LED download-mode indicator | `archive/devices/m5stack/papermono/artifacts/research-scratch/docs/pages/en-core-PaperMono.html` |
| S3 | `M5PaperMono-UserDemo/main/hal/hal_board.cpp` | M5Stack | primary | repository | <https://github.com/m5stack/M5PaperMono-UserDemo> | 2026-09-01 | `main` @ `c1099107271d31a0678d661a896e2b04dbb331ea`, MIT | `RGB_GREEN_PIN`/`RGB_BLUE_PIN` and their PWM channels (`:25–28`), `RGB_PWM_FREQ_HZ = 5000` (`:24`), the variant-detection dependency (`:160–172`) | `archive/devices/m5stack/papermono/artifacts/source-snapshots/M5PaperMono-UserDemo/` |
| S4 | `M5IOE1/src/M5IOE1.h` | M5Stack | primary | repository | <https://github.com/m5stack/M5IOE1> | 2026-09-01 | `main` @ `846eec7d05e25c09013be2acdb8804487f48a62e`, MIT | `M5IOE1_PWM_CH2 // IO8`, `M5IOE1_PWM_CH1 // IO9`; the 1-based-label / 0-based-enum trap | `archive/devices/m5stack/papermono/artifacts/source-snapshots/M5IOE1/` |
| S5 | PaperMono M5PM1/M5IOE1 power-management page | M5Stack | primary | official page | <https://docs.m5stack.com/en/arduino/papermono/m5pm1_m5ioe1> | 2026-09-01 | — | The L0–L3B rail assignment placing "RGB red" at L2/L3A and the whole RGB LED at L3B (§4.4); `setLedEnLevel()` | `archive/devices/m5stack/papermono/artifacts/research-scratch/docs/pages/en-arduino-papermono-m5pm1_m5ioe1.html` |

**Local artifacts:** none. No document specific to this part exists to store (§6).

**Method note.** The pin/net table in §3.1 was recovered by parsing the Altium PDF's invisible pin-instance markers. The red-channel limitation in §4.3 is corroborated independently by the schematic (pin name `LED_EN_PP` on a non-PWM M5PM1 pin) and by M5Stack's own prose, which is why it is stated as fact rather than inference; only the *consequences* for the reachable colour set are labelled **[INF]**.
