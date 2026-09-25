# Awinic AW39112 (AW39112DNR)

> 2-bit **bidirectional voltage-level translator with no direction-control pin**, for open-drain and push-pull signals, with integrated pull-ups on both ports and a single `OE` that can take the whole part into an ultra-low-power state.
> Research snapshot **2026-09-01**. Fitted **twice** on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — once as the gate that keeps the IP2315 charger off the shared I²C bus, once as the touch controller's bus interface. **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | Awinic `AW39112` datasheet **V1.6**, December 2025 — local copy `artifacts/aw39112dnr-datasheet-en-v1.6.pdf` | `not-tested` |
| **[VP]** | Awinic product page for `AW39112DNR`, retrieved 2026-09-01 | `not-tested` |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | M5Stack source at a cited `file:line` | `executed-success` for the read |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Ordering part | **`AW39112DNR`** | **[SCH]**, **[VP]** |
| Manufacturer | **Shanghai Awinic Technology Co., Ltd.** | **[DS]** |
| Category | *"Voltage level translators"* — *"2-Bit Bidirectional Voltage-Level Translator for Open-Drain and Push-Pull Applications"* | **[VP]**, **[DS]** |
| Package (`DNR` suffix) | **DFN-8L, 1.4 mm × 1.0 mm × 0.37 mm** | **[DS]** |
| Package (`FOR` suffix) | FOWLP-8B, 0.928 × 1.928 × 0.463 mm | **[DS]** |
| Datasheet | **`DS_AW39112DNR_FOR_EN_V1.6`**, December 2025, 27 pp | **[DS]** cover; **[VP]** lists the document dated **2025-12-19** |
| Lifecycle | Active | **[VP]** |

---

## 2. Key limits and capability **[DS Features]**

| Parameter | Value |
|---|---|
| Channels | **2**, bidirectional, non-inverting |
| Direction control | **None** — auto-sensing |
| A port / `VCCA` | **1.1 V – 3.6 V** |
| B port / `VCCB` | **1.65 V – 5.5 V** |
| Constraint | **V<sub>CCA</sub> ≤ V<sub>CCB</sub>** |
| Max data rate, push-pull | **24 Mbps** |
| Max data rate, open-drain | **2 Mbps** |
| Pull-up resistors | **Integrated on both A and B ports** |
| Power-supply sequencing | **None required** — either rail may ramp first |
| `OE` supply domain | **`VCCA`** |
| Low-power state | `OE` low → ultra-low consumption |
| Latch-up | > ±200 mA, JESD 78 |
| Supported nodes | 1.2 / 1.8 / 2.5 / 3.3 / 5 V |
| Applications named by the vendor | **I²C / SMBus**, UART, GPIO |

> ⚠ **2 Mbps is the open-drain figure, and I²C is open-drain.** A 400 kHz I²C bus is comfortably inside that, but this part is not a general-purpose high-speed translator when used on an open-drain bus.

> ⚠ **`OE` is supplied from `VCCA`.** The datasheet recommends tying it to GND through an external pull-down so that all I/O default to their supply rails, and states the sequencing rule plainly: *"OE should be enabled after both VCCA and VCCB are established."* **[DS]** Asserting `OE` before both rails exist is a documented misuse.

---

## 3. Pinout **[DS Pin Definition]**

| Pin (DNR) | Pin (FOR) | Name |
|---:|---|---|
| 1 | C1 | `VCCA` |
| 2 | D2 | `A1` |
| 3 | D1 | `A2` |
| 4 | B1 | `GND` |
| 5 | C2 | `OE` |
| 6 | A1 | `B2` |
| 7 | A2 | `B1` |
| 8 | B2 | `VCCB` |

Recommended decoupling: 0.1 µF on each of `VCCA` and `VCCB`. **[DS Typical Application Circuit]**

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md). Two instances, both on the **shared system I²C bus** (ESP32-S3 `GPIO47` SDA / `GPIO48` SCL), and both used as *switches* as much as translators.

#### 4.1 `U3` (sheet 2) — the IP2315 charger gate

| Pin | Name | Net | Domain |
|---:|---|---|---|
| 1 | `VCCA` | `VBUS_L0` | system logic side |
| 2 | `A1` | `G48_SYS_SCL` | ESP32-S3 GPIO48 |
| 3 | `A2` | `G47_SYS_SDA` | ESP32-S3 GPIO47 |
| 4 | `GND` | `GND` | |
| **5** | **`OE`** | **`PYB_CHG_IIC`** | from M5IOE1 `PYG11_PWM3` (`U17` pin 10/11, sheet 4) |
| 6 | `B2` | `CHG_SYS_SDA` | → [IP2315](../../injoinic/ip2315/README.md) pin 9 (`LED2`/`SDA`) |
| 7 | `B1` | `CHG_SYS_SCL` | → IP2315 pin 8 (`LED1`/`SCL`) |
| 8 | `VCCB` | **`VBAT_L0`** | battery side |

**This is the single most consequential use of the part on the board**, and both halves of the design are deliberate:

- **`VCCB = VBAT_L0`** means the charger-side bus idles at battery voltage. The IP2315 selects I²C mode at power-up *based on those pins being pulled to V<sub>BAT</sub>* — see [IP2315 §3](../../injoinic/ip2315/README.md#3--the-ic-pins-are-the-led-driver-pins--this-is-the-whole-hazard). The translator's integrated B-port pull-ups (§2) tracking `VCCB` are what supply that condition.
- **`OE = PYB_CHG_IIC`** turns the charger's presence on the shared bus into a firmware decision. M5Stack's driver connects it only for the duration of a transaction and disconnects afterwards (`M5Unified/src/utility/Power_Class.cpp:78–80, 85`, with a 64-attempt scan loop at `:88–96` and disconnects at `:2399`, `:2724`). **[SRC]**

M5Stack's own product-page warning is the reason: *"do not keep the IP2315 mounted on the I2C bus for extended periods; disconnect it promptly after communication to avoid reducing bus communication stability."* **[DOC]**

Adjacent parts on this net that the text-layer extraction identified but did not fully resolve: `Q5` (`SK2301AAT`, P-channel), `Q2` (`SK2302AAT`, N-channel) with `R9` = 100 kΩ, `R19` = 10 kΩ, `R21` = 10 kΩ, `R45`, `C12` = 100 nF. `VBAT_DET` appears in the same cluster. Their exact roles were **not** resolved and are not asserted here. **[SCH]**

#### 4.2 `U19` (sheet 4) — the touch-controller bus branch

| Pin | Name | Net | Domain |
|---:|---|---|---|
| 1 | `VCCA` | `TP_VDD` | touch rail (switched — see below) |
| 2 | `A1` | `TP_SYS_SCL` | → FPC `J4` |
| 3 | `A2` | `TP_SYS_SDA` | → FPC `J4` |
| 4 | `GND` | `GND` | |
| **5** | **`OE`** | **`TP_VDD`** | tied to the touch rail itself |
| 6 | `B2` | `G47_SYS_SDA` | ESP32-S3 GPIO47 |
| 7 | `B1` | `G48_SYS_SCL` | ESP32-S3 GPIO48 |
| 8 | `VCCB` | `3V3_L2` | system logic rail |

Here the translator is used as an **automatic isolator**: `TP_VDD` is switched by [`U18` (AW35122FDR)](../aw35122/README.md) under M5IOE1 `PYG13`, and both `VCCA` **and** `OE` hang off that rail. When the touch controller is powered down, `OE` falls with it and the [FT6336G](../../focaltech/ft6336g/README.md) branch drops off the system bus by construction — no separate control signal, no firmware step, no possibility of forgetting.

That is a neat piece of design and worth stating explicitly, because it is easy to misread the schematic as "a redundant translator between two 3.3 V rails". It is not a level shift; **it is a fail-safe bus isolator that costs one part.** **[INF]**

`R58` = 10 kΩ (to `TP_VDD`) and `R59` = 1.2 Ω sit on the `J4` side; `C68` = 10 µF/10 V decouples `TP_VDD`. **[SCH]**

#### 4.3 Both instances honour the datasheet's sequencing rule — one by accident of topology

The datasheet requires `OE` to be asserted only after both supplies are up (§2).

- **`U19` satisfies this structurally**: `OE` *is* `VCCA`, so it cannot lead `VCCA`. `VCCB` (`3V3_L2`) is up long before `TP_VDD` is switched on, because the M5IOE1 that switches it runs from `3V3_L2`. **[INF]**
- **`U3` depends on firmware**: `PYB_CHG_IIC` comes from the M5IOE1, which itself runs from `3V3_L2` = `VBUS_L0`-derived, while `VCCB` is `VBAT_L0` — present whenever there is a battery at all. So `OE` cannot be asserted before either rail exists. **[INF]**

Note the `VCCA ≤ VCCB` constraint (§2) is also satisfied in both cases: `VBUS_L0 ≤ VBAT_L0` (they are joined through the 0 Ω `R20`, so equal), and `TP_VDD ≤ 3V3_L2` (`TP_VDD` is `3V3_L2` through a load switch, so slightly lower).

---

## 5. Drivers and libraries

**Not applicable at the component level** — no bus interface, no registers. On the PaperMono the only software that touches it is whatever drives the `OE` nets:

```cpp
// U3's OE — via M5IOE1 pin 11 (label PYG11_PWM3), enum value 10
ioe1.pinMode(M5IOE1_PIN_11, OUTPUT);
ioe1.digitalWrite(M5IOE1_PIN_11, HIGH);   // charger onto the bus
// ... transaction at 0x75 ...
ioe1.digitalWrite(M5IOE1_PIN_11, LOW);    // and off again
```

M5Unified wraps this as `set_papermono_ip2315_enabled()`. **[SRC]** `U19` has no software at all.

Awinic publishes an **evaluation board**, `AW39112DNR_EVB_V1.0`, listed on the product page. **[VP]**

---

## 6. Integration pitfalls

1. **`VCCA ≤ VCCB` is a hard constraint** (§2), not a recommendation. The A side is the *lower* voltage domain.
2. **Assert `OE` only after both rails are up** (§2). Tying `OE` to `VCCA` — as `U19` does — makes this impossible to get wrong.
3. **Pull-ups are integrated.** Adding external I²C pull-ups on a translated branch changes the bus's effective pull-up strength on that side; check before copying a pull-up value from another design.
4. **2 Mbps open-drain ceiling** (§2). Fine for 400 kHz I²C, not for a fast SPI-like open-drain link.
5. **This part hides a device from a bus scan.** A shared-bus device behind an `OE` that firmware has not asserted is simply absent. Budget for that in your enumeration code rather than treating a missing address as a hardware fault — the PaperMono's charger is exactly this case.

---

## 7. Alternatives

| Part | vs. AW39112 | When |
|---|---|---|
| TI **TXS0102** | The classic 2-bit auto-direction translator; very well documented | When you want the reference part and its extensive app notes |
| TI **PCA9306** | 2-bit I²C-specific translator, no `OE` low-power state on some variants | Pure I²C level shifting |
| NXP **NTS0102** | Comparable | Second source |
| **Discrete dual N-FET translator** (the classic Philips AN97055 circuit) | Two FETs and four resistors | Cheapest; loses the `OE` gate, which is the entire point on this board |
| **[SGM40567](../../sgmicro/sgm40567/README.md)**-class analogue switch | Switches without translating | When both sides are already the same voltage and you only need the gate |

---

## 8. Open questions

- The exact roles of `Q2`/`Q5`/`R9`/`R19`/`R21`/`R45` around `U3`, and where `VBAT_DET` is generated (§4.1).
- Whether the integrated pull-ups alone hold `CHG_SYS_SCL/SDA` at V<sub>BAT</sub>, or whether one of the discrete parts above supplies additional pull-up. This determines how robust the IP2315's mode detection actually is on a partly-discharged cell.
- No hardware measurement of bus rise times on either translated branch.

---

## Manufacturer

**Shanghai Awinic Technology Co., Ltd.** No vendor sourcing guide exists in this repository yet; see the [AW32901 record](../aw32901/README.md#manufacturer) for the working retrieval recipe (full ordering part number → `productDetail` page → `data-file-url` → `/en/download`).

Worth noting for this part specifically: the product page's **Technical documentation** table exposes the document title and date directly (`Datasheet | DS_AW39112DNR_FOR_EN_V1.6 | 英文 | 2025-12-19`), which is the cleanest way to confirm you have the current revision before downloading.

## Related pages

- [Injoinic IP2315](../../injoinic/ip2315/README.md) — the device `U3` gates
- [Awinic AW35122](../aw35122/README.md) — switches `TP_VDD`, which powers and enables `U19`
- [FocalTech FT6336G](../../focaltech/ft6336g/README.md) — the device behind `U19`
- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — drives `U3`'s `OE`

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | AW39112 datasheet | Awinic | primary | datasheet | `https://www.awinic.com/en/download?file=doc/202512/460d535f-8aa2-4946-862a-131be2e3fb79.pdf&fileName=DS_AW39112DNR_FOR_EN_V1.6` | 2026-09-01 | **V1.6**, Dec 2025, 27 pp, 673 762 B | Pin definition, supply ranges, `VCCA ≤ VCCB` rule, data rates, `OE` sequencing requirement, integrated pull-ups | `artifacts/aw39112dnr-datasheet-en-v1.6.pdf` |
| D2 | AW39112DNR product page | Awinic | primary | official page | <https://www.awinic.com/en/productDetail/AW39112DNR> | 2026-09-01 | doc dated 2025-12-19 | Category, package options, EVB availability | — |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | Both instances' net assignments in §4 | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | `M5Unified/src/utility/Power_Class.cpp` | M5Stack | primary | repository | <https://github.com/m5stack/M5Unified> | 2026-09-01 | `master` @ `8530f537…`, MIT | The gating discipline in §4.1 | `archive/devices/m5stack/papermono/artifacts/source-snapshots/M5Unified/` |
| S3 | PaperMono product page | M5Stack | primary | official page | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | — | The verbatim bus-stability warning | `archive/devices/m5stack/papermono/artifacts/research-scratch/docs/pages/en-core-PaperMono.html` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/aw39112dnr-datasheet-en-v1.6.pdf` | 673 762 | `c248668d7cf5fc2ab59a4ae67a7a15c9fc84c7be520571a04542217fe71b9151` | 27 |

**Method note.** D1 validated as `%PDF`, 27 pages, text layer intact. Retrieved with plain `curl` and a Chrome 131 User-Agent; no fallback needed and no login required.
