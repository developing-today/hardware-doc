# Awinic AW9967 (AW9967DNR)

> High-efficiency **boost WLED driver** with an integrated 40 V switch FET, 1.1 MHz fixed switching frequency, single-pin PWM dimming down to 0.3 % duty, and a 200 mV feedback reference that sets full-scale LED current through one resistor.
> Research snapshot **2026-09-01**. Fitted as **`U11`** on sheet 2 of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), where it generates **`BL_15V_L3B`** — the e-paper **frontlight** supply. **No hardware was available.**

> **Headline finding:** M5Stack's own display library drives this part's dimming input at **5 kHz**, while the datasheet specifies a PWM dimming range of **10 kHz – 100 kHz**. See [§6.2](#62--m5gfx-drives-the-dimming-input-at-half-the-datasheets-minimum-frequency).

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Awinic `AW9967` datasheet **V1.8**, March 2025 — local copy `artifacts/aw9967-datasheet-en-v1.8.pdf` | `not-tested` |
| **[VP]** | Awinic product page for `AW9967DNR`, retrieved 2026-09-01 | `not-tested` |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | M5Stack source at a cited `file:line` | `executed-success` for the read |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Ordering part | **`AW9967DNR`** | **[SCH]** sheet 2, `U11`; **[VP]** |
| Manufacturer | **Shanghai Awinic Technology Co., Ltd.** | **[DS]** |
| Category | *"Series backlight LED drivers"* — *"High Efficiency, Support 0.3 % PWM Dimming Boost WLED Driver"* | **[VP]** |
| Package (`DNR`) | **DFN-6L, 2.0 mm × 2.0 mm × 0.75 mm**, θ<sub>JA</sub> **84 °C/W** | **[DS]**, **[VP]** |
| Package (`FSR`) | SOT23-5L, θ<sub>JA</sub> 120 °C/W | **[DS]** |
| Datasheet | **`DS_AW9967_EN_V1.8`**, March 2025, 23 pp | **[DS]** cover |
| Lifecycle | Active | **[VP]** |

The datasheet notes the DNR package has materially better thermal dissipation than the SOT23 variant — 84 vs 120 °C/W — which is the stated reason the DFN part exists. **[DS]**

---

## 2. Key limits and capability **[DS]**

| Parameter | Value |
|---|---|
| Input voltage `VIN` | **2.7 V – 5.5 V** (abs. max −0.3 to 6 V) |
| `FB`, `CTRL` abs. max | −0.3 to 6 V |
| **`SW` abs. max** | **−0.3 to 40 V** |
| Internal switch FET | 40 V, current limit **2.3 / 2.7 A** (min/typ) |
| Switching frequency | **800 / 1100 / 1400 kHz** (min/typ/max) — fixed, not spread-spectrum |
| Maximum duty cycle | 90 / 93 % (min/typ) |
| String capability | up to **10 LEDs in series**, parallel strings supported |
| **Open-LED OVP** | **36 – 38 V** |
| Efficiency | up to 89 % for 2P7S |
| Per-channel current | up to **20 mA** **[VP]** |
| R<sub>DS(on)</sub> | 0.25 Ω @ V<sub>IN</sub> = 3.6 V |
| Other protections | over-current, over-temperature, LED-open; built-in soft start |
| Temperature | −40 to +85 °C |
| ESD | ±2 kV HBM, ±1.5 kV CDM |

### 2.1 Current setting and dimming — the numbers that matter **[DS Electrical Characteristics]**

Full-scale LED current is **`I = V_REF / R_SET`**, where `R_SET` is a single resistor from `FB` to GND:

| Parameter | Condition | Min | **Typ** | Max |
|---|---|---:|---:|---:|
| `V_REF` | PWM duty **100 %** | 194 mV | **200 mV** | 205 mV |
| `V_REF_PWM` | PWM duty 1 % | 1.575 mV | 2.25 mV | 2.925 mV |
| `V_REF_PWM` | PWM duty 0.5 % | 0.5 mV | 1.25 mV | 2 mV |
| `V_REF_PWM` | PWM duty 0.3 % | — | — | — (minimum supported duty) |
| **`f_PWM1`** — **PWM dimming frequency** | — | **10 kHz** | — | **100 kHz** |
| `D_PWM` — dimming duty range | — | 0.3 % | — | 100 % |
| `t_MIN_ON` | minimum on-pulse width | — | — | 50 ns |
| `I_Q` | operating quiescent, `V_FB` = 1 V | — | 100 µA | 250 µA |
| Shutdown current | `V_CTRL` = GND, V<sub>IN</sub> = 4.2 V | — | 0.1 µA | 1 µA |

The datasheet states the dimming range in prose too: *"The current of WLED can also be set with duty cycle of PWM signal applied to the CTRL pin with 10 kHz ~ 100 kHz."* **[DS §General Description]**

Note the strong non-linearity at the bottom of the range: at 1 % duty the reference is 2.25 mV rather than the 2.0 mV a linear law would give, and at 0.5 % it is 1.25 mV rather than 1.0 mV. Low-brightness behaviour is not simply proportional to duty.

---

## 3. Pinout **[DS Pin Description]**

| Pin (DNR) | Pin (FSR) | Name | Function |
|---:|---:|---|---|
| **1** | 6 | `FB` | Feedback. **Connect `R_SET` from `FB` to GND** |
| 2 | — | `NC` | No connection |
| **3**, **7** | 2 | `GND` | Ground. **Pin 7 is the exposed pad and must be soldered to the board and connected to GND** |
| **4** | 1 | `SW` | Switching node |
| **5** | 4 | `CTRL` | **Enable pin — also the PWM digital-dimming input** |
| **6** | 5 | `VIN` | Power |

> ⚠ **`CTRL` is both enable and dimming.** A duty of zero is a shutdown command, not "0 % brightness". There is no separate enable, so a driver that writes duty = 0 to dim to black also collapses the boost output and pays the soft-start cost on the way back up.

### 3.1 Reference application circuit **[DS Typical Application Circuits]**

```
        L1 = 10 µH            Schottky
 VIN ───────UUUU──────┬──────►|──────► LED string (e.g. 3P10S)
  │                   │                     │
 CIN1 10 µF        SW │                  COUT1 1 µF/50 V
 CIN2 100 nF (opt) ───┤                  COUT2 33 pF/50 V (opt)
                 AW9967                      │
              VIN  CTRL  FB ─── R_SET ───────┴─── (string return)
                                  │
                                 GND
```

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), designator **`U11`**, schematic sheet 2, in the block labelled `EINK_BL`.

It produces **`BL_15V_L3B`**, the e-paper frontlight supply — one of the `L3B` rails, i.e. present only in the **L3B All ACTIVE** power state defined on sheet 1.

#### 4.1 Exact wiring **[SCH]**

| Pin | Name | Net / part |
|---:|---|---|
| 1 | `FB` | **`BL_FB`** → **`R29` = 18 Ω / 1 %** to GND; also returns from the frontlight connector `J1` |
| 2 | `NC` | not connected |
| 3, 7 | `GND` / `EPAD` | `GND` |
| 4 | `SW` | **`L3` = `FTC201610S100MBCA`, 10 µH** → **`D2` = `RB162VAM-20TR`** Schottky → `BL_15V_L3B` |
| 5 | `CTRL` | **`PYG3_BL_PWM`** |
| 6 | `VIN` | **`3V3_L2`** |

Output network: `C25` = **1 µF/50 V**, `C24` = **33 pF/50 V**, `C26` = **`NC`/50 V**. **[SCH]**

**The board uses Awinic's reference circuit essentially verbatim** — 10 µH inductor, Schottky, 1 µF/50 V `COUT1`, 33 pF/50 V `COUT2`, one `R_SET`. `C26` is the depopulated third position. That is a good sign for the analogue design and means the datasheet's characterisation curves should apply directly. **[INF]**

#### 4.2 ⚠ `PYG3_BL_PWM` comes from the **M5PM1**, not the M5IOE1

The net name uses the `PYG` prefix that M5Stack's documentation otherwise reserves for M5IOE1 pins, but the schematic wires it to **`U7` pin 13**, which is the [M5PM1](../../m5stack/m5pm1/README.md) — the pin is labelled `G3_WAKEin(INT3/4)_IRQout_PWM`. **[SCH]** sheet 2

This corroborates, from the schematic, a documentation defect already recorded from the vendor's web pages: the PaperMono product page says *"the frontlight brightness is controlled via `PYG3_BL_PWM` of the M5PM1"* while the PaperMono-**Lite** page says *"`G3_WAKEin` of M5PM1"* — the Lite page is right, and both pages carry an identical PinMap row confirming M5PM1 GPIO3. **[DOC]**

> ⚠ **This one is dangerous, not cosmetic.** `PYG3` **is** also a real and different pin: **M5IOE1 IO3 is the e-paper 3.3 V power enable.** A developer who trusts the PaperMono page's prose and writes to M5IOE1 pin 3 expecting a backlight instead **cuts power to the display panel.**

#### 4.3 ⚠ `R_SET` = 18 Ω gives ≈11 mA, and the schematic's own design note disagrees with itself

Sheet 2 carries a hand-written design note next to the boost:

> *"I set max = Vfb / Rset ≤ 20 mA"*
> *"if Duty = 100 %, Vfb = Duty × 200 mV + 0.2 mV, Iset = 15 mA，即 Rset = 11R"*

Three numbers, and they do not agree:

| Source | `R_SET` | Resulting full-scale current (V<sub>REF</sub> = 200 mV typ) |
|---|---:|---:|
| **Fitted BOM value `R29`** | **18 Ω / 1 %** | **≈ 11.1 mA** |
| Design note's stated target | — | 15 mA |
| Design note's stated resistor | 11 Ω | ≈ 18.2 mA |

The note's own arithmetic is inconsistent — 200 mV / 11 Ω is 18.2 mA, not 15 mA; 15 mA would need ≈13.3 Ω. Whatever the intent, **the part actually fitted is 18 Ω**, which puts full-scale frontlight current at roughly **11 mA**, comfortably inside the ≤20 mA ceiling the note sets and well inside the AW9967's 20 mA per-channel rating. **[INF]**, from `executed-success` reads of the fitted value and the datasheet reference voltage.

If you are estimating frontlight power budget for this board, use ~11 mA at full brightness, not 15 or 20.

#### 4.4 How M5GFX actually programs the brightness **[SRC]**

The frontlight is not driven by an ESP32-S3 PWM peripheral. It is driven by the M5PM1's own PWM0 block, configured over I²C at `0x6E`. `M5GFX/src/M5GFX.cpp:819–856` (`struct Light_M5PaperMono`):

| Step | M5PM1 register | Value written | Meaning | Line |
|---|---|---|---|---|
| Bring up I²C | — | SDA 47 / SCL 48 | shared system bus | `:823` |
| `GPIO_DRV` | **`0x13`** | `bitOff 1<<3` | M5PM1 GPIO3 → **push-pull** | `:826` |
| `GPIO_FUNC0` | **`0x16`** | `bitOn 0xC0` | M5PM1 GPIO3 → **PWM** alternate function | `:829` |
| `PWM_FREQ_L` / `_H` | **`0x34` / `0x35`** | **5000** | **5 kHz** dimming frequency | `:833–836` |
| Brightness off | **`0x31`** | `0` | `PWM0_HC` = 0 | `:845` |
| Brightness on | **`0x30`** (+ `0x31`) | `br = brightness × brightness`; writes `(br>>4)&0xFF`, then `(br>>12) \| 0x10` | **squared / gamma** duty, `0x10` = enable | `:850–853` |

A **linear** brightness write exists in the same file but is **commented out** at `:847`, superseded by the squared curve at `:848–853`. The same 5 kHz figure is used for the RGB LED PWM elsewhere (`RGB_PWM_FREQ_HZ = 5000`, `hal_board.cpp:24`), which suggests it is a house default rather than a value chosen for this driver. **[INF]**

---

## 5. Drivers and libraries

**The AW9967 has no bus interface** — it is controlled entirely by the duty cycle on `CTRL`. On the PaperMono the software stack is therefore:

```
M5GFX  Light_M5PaperMono  ──I²C 0x6E──►  M5PM1 firmware  ──PWM0/GPIO3──►  AW9967 CTRL
```

| Layer | Where |
|---|---|
| Application API | `M5.Display.setBrightness(0–255)` |
| Panel light class | `M5GFX/src/M5GFX.cpp:819–856` |
| PMIC register access | [M5PM1 library](../../m5stack/m5pm1/README.md), registers `0x13`, `0x16`, `0x30`, `0x31`, `0x34`, `0x35` |

Awinic publishes a **"Series Backlight Driver Hardware Design Guide" (EN V1.0)** alongside the datasheet on the product page; it was **not** retrieved this session (the filename on the vendor CDN contains the marker `加密` — "encrypted" — and was not tested). **[VP]**

---

## 6. Integration pitfalls, in priority order

### 6.1 `CTRL` at 0 % duty is a shutdown, not a dim

See §3. Expect a soft-start ramp when coming back from zero.

### 6.2 ⚠ M5GFX drives the dimming input at half the datasheet's minimum frequency

- **Datasheet:** `f_PWM1` = **10 kHz min, 100 kHz max** (§2.1), stated twice — once in the electrical table, once in the general description. **[DS]**
- **M5GFX:** writes **5000** to the M5PM1's `PWM_FREQ_L`/`_H` (`M5GFX.cpp:833–836`). **[SRC]**

Both readings are `executed-success`. The **consequence** is `inferred` and unmeasured: below the specified minimum, the internal `V_REF` filter (the datasheet lists a `t_REF` filter time constant) has proportionally longer to droop between pulses, so the plausible symptoms are **visible flicker, audible inductor whine, and a brightness-versus-setting curve that departs from the datasheet's characterisation** — most likely at low duty, where the reference is already only 1–2 mV and non-linear (§2.1).

This is worth flagging for two reasons beyond this board:

1. It compounds with the **squared brightness curve** (§4.4). A setting of 16/255 becomes a duty of roughly (16/255)² ≈ 0.4 % — right at the AW9967's 0.3 % floor, at a switching frequency it is not specified for.
2. It is a **software-only defect**, if it is one. Writing `10000` instead of `5000` at `M5GFX.cpp:833–836` would bring the part inside spec with no hardware change.

Recorded as a conflict, not resolved: no hardware was available to measure flicker or the actual brightness curve. Anyone with a PaperMono and an oscilloscope or a photodiode can settle it in minutes.

### 6.3 Other pitfalls

3. **`SW` is rated 40 V and OVP trips at 36–38 V.** An open LED string is protected, but a probe or a scope ground clip on `SW` sees a 40 V node.
4. **The exposed pad is a required electrical connection**, not just thermal (§3).
5. **`R_SET` is the only current control.** Get it wrong and no amount of firmware fixes the full-scale current — see §4.3 for how easily the intent and the fitted value diverge.
6. **1.1 MHz fixed frequency, no spread spectrum.** If the board has an AM/LF-sensitive receiver, this is a fixed tone plus harmonics.

---

## 7. Alternatives

| Part | vs. AW9967 | When |
|---|---|---|
| TI **TPS61165** / **LM3414** | Comparable boost WLED drivers, extensive documentation and app notes | When you want a well-trodden reference design |
| TI **LM3697** / **LP8556** | I²C-controlled backlight drivers | When you want brightness in registers rather than a PWM pin — removes the whole §6.2 class of problem |
| **AW9967FSR** | Same silicon, SOT23-5L | When board area beats thermal performance (θ<sub>JA</sub> 120 vs 84 °C/W) |
| Charge-pump WLED driver | No inductor | Only for very short strings; a 15 V frontlight rail is out of reach |

The AW9967's distinguishing feature is the **0.3 % minimum dimming duty**, which is what lets an e-paper frontlight go genuinely dim for night reading. That capability is exactly what §6.2 puts at risk.

---

## 8. Open questions

- Whether 5 kHz on `CTRL` produces observable flicker or brightness non-linearity on real hardware (§6.2). **This is the highest-value open question in this record.**
- Whether the frontlight LED string is series, parallel or a mix, and how many dies — `J1` on sheet 2 is the frontlight connector, but the panel-side arrangement is not in the schematic. The 10 µH / 1 µF reference values and a `BL_15V` net name suggest a single series string of four or five white LEDs. **[INF]**, unconfirmed.
- Why the fitted `R_SET` (18 Ω) differs from the design note's own figure (11 Ω) (§4.3).
- The Awinic "Series Backlight Driver Hardware Design Guide" was not retrieved.
- No hardware measurement of efficiency, ripple or the actual frontlight current.

---

## Manufacturer

**Shanghai Awinic Technology Co., Ltd.** No vendor sourcing guide exists in this repository yet; see the [AW32901 record](../aw32901/README.md#manufacturer) for the working retrieval recipe.

## Related pages

- [M5Stack M5PM1](../../m5stack/m5pm1/README.md) — supplies `CTRL` from its GPIO3/PWM0, and holds registers `0x13`/`0x16`/`0x30`/`0x31`/`0x34`/`0x35`
- [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) — the e-paper panel this frontlight illuminates
- [Awinic AW35122](../aw35122/README.md) — the load switches for the other `L3B` rails
- [Joulwatt JW5712](../../joulwatt/jw5712/README.md) — produces `3V3_L2`, this part's input rail

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | AW9967 datasheet | Awinic | primary | datasheet | `https://www.awinic.com/en/download?file=doc/202603/d34b36c0-c0a6-4467-b148-72495c1a386a.pdf&fileName=DS_AW9967_EN_V1.8` | 2026-09-01 | **V1.8**, Mar 2025, 23 pp, 788 507 B | Pin description, `f_PWM1` 10–100 kHz, `V_REF` 200 mV, OVP 36–38 V, absolute maxima, reference application circuit | `artifacts/aw9967-datasheet-en-v1.8.pdf` |
| D2 | AW9967DNR product page | Awinic | primary | official page | <https://www.awinic.com/en/productDetail/AW9967DNR> | 2026-09-01 | — | Category, `DFN 2X2-6L`, 20 mA/ch, 0.3 % min duty, 1.1 MHz; names the Hardware Design Guide | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `U11` wiring, `R29` = 18 Ω, `L3`/`D2`/`C24`/`C25`/`C26`, the design note in §4.3, `PYG3_BL_PWM` → M5PM1 `U7` pin 13 | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | `M5GFX/src/M5GFX.cpp` — `Light_M5PaperMono` | M5Stack | primary | repository | <https://github.com/m5stack/M5GFX> | 2026-09-01 | `master` @ `d91077b9a607b59404e4e4a49f775c792bfae382`, MIT | The register writes and the 5 kHz frequency in §4.4 and §6.2 | `scratch/m5stack-papermono/repos/M5GFX/` |
| S3 | PaperMono / PaperMono-Lite product pages | M5Stack | primary | official page | <https://docs.m5stack.com/en/core/PaperMono> · <https://docs.m5stack.com/en/core/PaperMono-Lite> | 2026-09-01 | — | The `PYG3_BL_PWM` vs `G3_WAKEin` documentation conflict in §4.2 | `scratch/m5stack-papermono/docs/pages/` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/aw9967-datasheet-en-v1.8.pdf` | 788 507 | `f5fa2acb88084735a932ec4e68c2d35db83f1fe474c43b20a18a320ac1d4aa5b` | 23 |

**Method note.** D1 validated as `%PDF`, 23 pages, text layer intact. Retrieved with plain `curl` and a Chrome 131 User-Agent; no fallback needed and no login required. The §6.2 conflict was found by decoding the M5GFX register writes against the datasheet's electrical table, per [`hardware-device-research` §10](../../../.agents/skills/hardware-device-research/SKILL.md).
