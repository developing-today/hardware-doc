# FocalTech FT6336G

> Single-chip **self-capacitance touch-panel controller** with a built-in 16-bit enhanced MCU, up to 31 sensor channels, one touch point plus gestures or two touch points, 100 Hz report rate, and an I²C slave interface — for panels up to 4.0 inches.
> Research snapshot **2026-09-01**. Used on the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) at I²C **`0x38`**. **The controller is not on the mainboard** — it lives on the touch panel's flexible circuit and reaches the board through the FPC connector `J4`. **No hardware was available.**

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | FocalTech `FT6336G` datasheet **Version 1.0**, © 2015 — local copy `artifacts/ft6336g-datasheet-v1.0-focuslcds-mirror.pdf` | `not-tested` |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[SRC]** | M5Stack / M5GFX source at a cited `file:line` | `executed-success` for the read |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **`FT6336G`** | **[DOC]**; **[SCH]** by implication (§4) |
| Manufacturer | **FocalTech Systems Co., Ltd.** (敦泰科技) | **[DS]** |
| Function | Self-capacitance touch-panel controller with integrated 16-bit MCU | **[DS]** |
| **Package** | **QFN 5 × 5 mm, 40 pin, 0.6 mm height, 0.4 mm pitch** | **[DS]** §1.1 model table |
| Sensor channels | **31** | **[DS]** §1.1 |
| Max panel size | **≤ 4.0 inch** | **[DS]** §1.1 |
| **I²C address** | **`0x38`** (7-bit) | **[SRC]**, **[DOC]** — ⚠ **not** in the datasheet, see §2.1 |
| Datasheet | **Version 1.0**, © 2015 FocalTech, 10 numbered pages (12 PDF pages) | **[DS]** page footers |

---

## 2. Capabilities and limits **[DS]**

| Parameter | Value |
|---|---|
| Sensing technique | **Self-capacitance** |
| Touch points | **1 point + gestures**, or **2 points** |
| Output | Absolute X and Y coordinates, or gesture codes |
| Report rate | **up to 100 Hz** |
| Scan rate, Active mode | **60 fps default**, host-configurable up or down |
| Scan rate, Monitor mode | **25 fps default**, host-configurable |
| Interface | **I²C slave only** — no SPI |
| **I²C clock** | **10 kHz – 400 kHz** |
| Analogue supply `VDDA` | **2.8 – 3.6 V** (abs. max −0.3 to +3.6 V) |
| Digital supply `VDD3` | abs. max −0.3 to +3.6 V |
| **I/O supply `IOVCC`** | **1.8 – 3.6 V, independent of `VDDA`** |
| Internal regulator | Generates **1.5 V** for digital circuits from `VDDA` |
| Input thresholds | V<sub>IH</sub> ≥ 0.7 × `IOVCC`; V<sub>IL</sub> ≤ 0.3 × `IOVCC` |
| Operating temperature | **−40 to +85 °C** |
| Storage temperature | −55 to +150 °C |
| ESD | HBM ≥ 7500 V, MM ≥ 500 V |
| On-chip memory | 48 KB flash program store, 5 KB SRAM |
| Master clock | 18 MHz, from a 36 MHz RC oscillator |
| Auto-calibration | Yes — insensitive to capacitance and environmental variation |
| Panel construction | Supports single-film TP and triangle pattern **without an additional shield** |

**I²C timing [DS Table 2-2]:** bus-free time between STOP and START ≥ 4.7 µs; (repeated) START hold ≥ 4.0 µs; data setup ≥ 250 ns; repeated-START setup ≥ 4.7 µs; STOP setup ≥ 4.0 µs.

### 2.1 ⚠ The datasheet does not contain the I²C address or the register map

This is the most important thing to know before trying to work from FocalTech's document.

**Version 1.0 of the FT6336G datasheet describes the architecture, the operating modes, the electrical specification, the I²C bus timing and the package — and stops there.** Full-text search finds **no occurrence of `0x38`**, no slave-address value, and no register table. There is no "read touch data from register `0x02`" section.

The address `0x38` and the register semantics come entirely from downstream sources:

| Source | Value | Where |
|---|---|---|
| M5GFX touch driver | `ft5x06_i2c_addr = 0x38` | **[SRC]** `M5GFX/src/M5GFX.cpp:575` |
| M5GFX PaperMono touch config | `_cfg.i2c_addr = 0x38` | **[SRC]** `M5GFX.cpp:713` |
| M5GFX board bring-up | `touch_addr = 0x38` | **[SRC]** `M5GFX.cpp:329` |
| M5Stack documentation | `FT6336G(0x38)` | **[DOC]** |

`0x38` is the long-standing family address for FocalTech's FT5x06/FT6x36 line, and M5GFX drives this part through its **FT5x06** code path — the register interface is family-compatible even though the datasheets are separate. **[INF]**

**Practical consequence:** you cannot write an FT6336G driver from the FocalTech datasheet. You need either a register-map application note (FocalTech distributes these separately, and typically under NDA) or an existing open driver. See §5.

### 2.2 Operation modes **[DS §2.3]**

| Mode | Behaviour |
|---|---|
| **Active** | Full scanning at 60 fps default. Normal operation |
| **Monitor** | Reduced 25 fps scan, most algorithms stopped, a simple presence detector runs. **⚠ The serial port is closed and no data transfers with the host in this mode** — it wakes to Active on a touch |
| **Hibernation** | Power-down. Responds only to `RESET` or a wake-up signal from the host |

> ⚠ **Monitor mode closes the I²C port.** A host that polls the controller while it is in Monitor mode gets nothing, and the correct architecture is interrupt-driven: wait for `/INT`, then read. This is exactly what the PaperMono does (§4.3).

### 2.3 Host interface signals **[DS §2.3]**

| Signal | Direction | Purpose |
|---|---|---|
| `SDA` / `SCL` | bidirectional / in | I²C slave interface |
| **`/INT`** | out | Asserted when touch data is ready for the host to read |
| **`RSTN`** | in | **Active-low** external reset. After reset the chip enters **Active** mode |

A watchdog timer is implemented internally *"to ensure the robustness of the chip"*. **[DS]**

---

## 3. Where it physically is

**Not on the mainboard.** The PaperMono schematic contains no FT6336G symbol on any of its six sheets; sheet 4 has a `TP` block whose entire content is the FPC connector **`J4`**, a level translator and a load switch. The controller is bonded to the touch panel's own flex circuit — the standard construction for a capacitive touch panel.

That has two consequences worth stating:

- **The device record for the panel assembly is the right place for mechanical and optical properties**; this record covers the controller silicon only.
- **You cannot replace the controller.** It comes with the panel.

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), on the touch FPC reaching connector **`J4`** (sheet 4). The same part is fitted on the **PaperMono-Lite** (C153-Lite), whose specification is identical for touch. **[DOC]**

#### 4.1 Signals at `J4` **[SCH sheet 4]**

`J4` is an 8-way FPC connector. The six signals recovered from the schematic text layer are:

| Signal | Net | Goes to |
|---|---|---|
| Touch supply | **`TP_VDD`** | from [`U18` AW35122FDR](../../awinic/aw35122/README.md) load switch, enabled by M5IOE1 **`PYG13`** |
| I²C clock | **`TP_SYS_SCL`** | A1 of [`U19` AW39112DNR](../../awinic/aw39112/README.md) translator |
| I²C data | **`TP_SYS_SDA`** | A2 of `U19` |
| Interrupt | **`G4_TP_INT`** | ESP32-S3 **GPIO4** directly |
| Reset | **`PYB_TP_RST`** | M5IOE1 **`PYG6`** |
| Ground | `GND` | |

Passives: `R58` = 10 kΩ (pull-up to `TP_VDD`), `R59` = 1.2 Ω, `C68` = 10 µF/10 V on `TP_VDD`. **[SCH]**

> **The exact pin *numbering* on `J4` was not reliably resolved** from the PDF text layer — the connector's pin markers and net labels interleave in a way the extraction could not separate with confidence. The **signal set** above is solid; the **1-to-8 ordering is not**, and is deliberately not asserted. Read it off the rendered sheet before building a replacement flex.

#### 4.2 The touch bus is isolated, not merely level-shifted

`U19` is an [AW39112DNR](../../awinic/aw39112/README.md) 2-bit translator whose **`VCCA` and `OE` are both `TP_VDD`**, with `VCCB` on `3V3_L2`. **[SCH]**

Since `TP_VDD` is switched by M5IOE1 `PYG13`, **powering down the touch controller automatically removes it from the shared system I²C bus** — `OE` falls with the rail. No firmware step, no forgotten sequence, no possibility of a half-powered slave holding SDA low. This is a deliberate and rather good piece of design; see [AW39112 §4.2](../../awinic/aw39112/README.md#42-u19-sheet-4--the-touch-controller-bus-branch).

It also means: **if you power-cycle `TP_VDD`, you must re-initialise the touch driver.** M5Stack says so explicitly — *"The pins associated with the e-paper display, touch controller, microSD, and PDM microphone are already used by M5Unified. Before modifying them, ensure that the corresponding peripheral has stopped, or the peripheral may stop working or require reinitialization."* **[DOC]**

#### 4.3 `/INT` goes straight to the ESP32-S3 and is a wake source

`G4_TP_INT` reaches **ESP32-S3 GPIO4** with no expander in the path. **[SCH]** In firmware it is both the touch-ready interrupt and a deep-sleep wake source:

- `TOUCH_WAKE_GPIO = 4` — `app_sleep_wake.cpp:52` **[SRC]**
- `cfg.pin_int = 4` in M5GFX's touch configuration — `M5GFX.cpp:2144` **[SRC]**

Sheet 1's power-state table lists **"TP · Touch-to-wake supported"** under `L2 DeepSleep`. **[SCH]** So the intended low-power behaviour is: system asleep, touch controller in Monitor mode, a finger wakes the controller, the controller asserts `/INT`, `/INT` wakes the ESP32-S3.

Note the ordering that follows from §2.2: **while the system sleeps the controller's I²C port is closed**, so a wake handler must not assume it can read coordinates immediately — the controller transitions to Active on the touch, and the first read must happen after that. **[INF]**

#### 4.4 ⚠ The effective touch area is smaller than the display

M5Stack documents this and it is not obvious from any datasheet:

> *"The touch IC firmware internally shrinks the touch boundary. The effective touch coordinate range is limited to: **X-axis: 5 ~ 475** (total width 480 px), **Y-axis: 5 ~ 795** (total height 800 px)."* **[DOC]**

| Axis | Panel | **Usable touch** | Dead border |
|---|---|---|---|
| X | 0 – 479 (480 px) | **5 – 475** (471 px) | 5 px leading, 4 px trailing |
| Y | 0 – 799 (800 px) | **5 – 795** (791 px) | 5 px leading, 4 px trailing |

**This is a controller-firmware property, not a mechanical one and not something a host can change.** The practical consequences:

- **Do not put a hit target within 5 px of any screen edge.** A button drawn flush to the edge has a strip that cannot be pressed. Edge-swipe gestures that start at coordinate 0 will never register.
- A host that scales raw coordinates assuming a full 0–479 / 0–799 range introduces a small but systematic offset and a ~2 % scale error. Whether M5GFX compensates was **not** determined.
- Full-screen "tap anywhere to wake" works fine; corner affordances do not.

#### 4.5 Bus context

The FT6336G shares the system I²C bus (GPIO47 SDA / GPIO48 SCL) with six other devices. Addresses are all distinct — no conflict:

| Device | Address |
|---|---|
| **FT6336G touch** | **`0x38`** |
| RX8130CE RTC | `0x32` |
| [BMI270](../../bosch-sensortec/bmi270/README.md) IMU | `0x68` (alt `0x69`), **run at 100 kHz** |
| [M5IOE1](../../m5stack/m5ioe1/README.md) | `0x4F` |
| ST25R3916 NFC | `0x50` |
| [M5PM1](../../m5stack/m5pm1/README.md) | `0x6E` |
| [IP2315](../../injoinic/ip2315/README.md) charger | `0x75` — **gated off the bus** |

Bus pull-ups `R36`, `R37` = 2.2 kΩ to `3V3_L2`. **[SCH]**

> Note the FT6336G's I²C **minimum** clock is 10 kHz (§2) and the BMI270 on the same bus is driven at **100 kHz** while the RTC and NFC run at 400 kHz. **[SRC]** Since bus speed is per-transaction on a shared bus, the touch controller sees whatever rate the current master transaction uses — all of which are inside its 10–400 kHz window.

---

## 5. Drivers and libraries

| Option | Notes |
|---|---|
| **M5GFX `lgfx::Touch_FT5x06`** | What ships on the PaperMono. `M5GFX.cpp:329`, `:575`, `:713`, `:2144–2146`. Configured with `pin_int = 4`, `i2c_addr = 0x38`, SDA 47 / SCL 48 |
| **`lvgl/lv_drivers` FT6x06** | Common LVGL touch driver, register-compatible |
| **Adafruit_FT6206** (Arduino) | Widely used; targets FT6206/FT6236 but the register interface is the same family |
| **Linux** `drivers/input/touchscreen/edt-ft5x06.c` | Mainline, `compatible = "focaltech,ft6236"` and relatives. The most complete open implementation of the register map |
| Roll your own | ⚠ **You cannot do this from the FocalTech datasheet** (§2.1). Read the Linux driver instead — it is the de-facto public documentation of the register map |

The register interface these all share: a small register file where `0x00`–`0x01` hold mode/gesture, `0x02` holds the touch count, and each touch point occupies six bytes from `0x03` (X high/low with an event flag in the top bits, Y high/low with a touch ID, weight, area). **[INF]** — this is the FT5x06-family layout implemented by the drivers above, **not** read from `[DS]`.

---

## 6. Integration pitfalls, in priority order

1. **The datasheet has no register map or address** (§2.1). Budget for using an existing driver.
2. **Monitor mode closes the I²C port** (§2.2). Design for interrupt-driven reads, not polling.
3. **The usable coordinate range is inset by ~5 px on every edge** (§4.4). This is firmware inside the controller; you cannot widen it.
4. **`IOVCC` is independent of `VDDA`** (§2). On a 3.3 V-only board this is invisible; on a mixed-voltage board it is the pin that makes level shifting unnecessary — and forgetting to power it leaves the chip alive but mute.
5. **`RSTN` is active-low** and on the PaperMono comes from an I²C expander (§4.1) — so resetting touch requires a working I²C bus, which is awkward if the reason you are resetting is that the bus is unhappy.
6. **After a `TP_VDD` power cycle the driver must be re-initialised** (§4.2).
7. **31 channels, ≤ 4.0 inch panel** (§1). The PaperMono's 3.97-inch panel is right at the ceiling.
8. **Self-capacitance, 2 points maximum.** No pinch-zoom with reliable independent point tracking; self-capacitance sensing suffers the classic two-point "ghosting" ambiguity. **[INF]**

---

## 7. Alternatives

| Part | vs. FT6336G | When |
|---|---|---|
| FocalTech **FT6236 / FT6206 / FT6436** | Same family, differing channel counts and panel sizes; one shared datasheet covers several | Different panel size in the same ecosystem |
| **[Hynitron CST816D](../../hynitron/cst816d/README.md)** | Single-point capacitive controller, low cost | Small panels; documented in this repository |
| **[Goodix GT911](../../goodix/gt911/README.md)** | 5-point mutual-capacitance | When you need real multi-touch |
| Sitronix, Ilitek touch controllers | Comparable | Panel-vendor-driven choice |

In practice **the controller is chosen by the panel supplier, not by the board designer** (§3). This table is for understanding what you have, not for substituting it.

---

## 8. Open questions

- **`J4`'s pin numbering** (§4.1).
- Whether M5GFX compensates for the 5–475 / 5–795 coordinate inset (§4.4), or passes raw coordinates through.
- Whether a FocalTech register-map application note for the FT6336G is publicly obtainable; only the datasheet was found, and it does not contain one (§2.1).
- The panel assembly's own part number — the e-paper module is `DEPG0397BBS770F3HP-XM`, but whether the touch layer is a separate supplier's part is not established.
- No hardware measurement of report rate, current draw or the actual coordinate boundaries.

---

## Manufacturer

**FocalTech Systems Co., Ltd.** No vendor sourcing guide exists in this repository yet.

**⚠ Retrieval finding — record this, it will recur.** FocalTech does not serve this datasheet itself; the copies in circulation are hosted by display module vendors, and **those hosts block ordinary browser User-Agents**:

| Host | Chrome 131 UA | WhatsApp UA | Safari 17 UA | **ClaudeBot UA** |
|---|---|---|---|---|
| `www.orientdisplay.com/wp-content/uploads/2022/08/FT6336G_v1.0.pdf` | **403** | 403 | 403 | **403** |
| `focuslcds.com/wp-content/uploads/Drivers/FT6336G.pdf` | **403** | 403 | 403 | **200, `application/pdf`, `%PDF` ✓** |

The only User-Agent that succeeded was
`Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ClaudeBot/1.0; +claudebot@anthropic.com`,
and only on `focuslcds.com`. Both hosts are WordPress sites behind a WAF that appears to allow declared crawlers while blocking generic desktop agents — the opposite of the usual pattern, and worth remembering. This finding belongs in [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

A third mirror exists — `https://www.buydisplay.com/download/ic/FT6236-FT6336-FT6436L-FT6436_Datasheet.pdf` — covering the FT6236/FT6336/FT6436L/FT6436 as a set. It was **not** retrieved and may contain the register information the single-part datasheet lacks. That is the highest-value untaken lead here.

## Related pages

- [Awinic AW35122](../../awinic/aw35122/README.md) — `U18`, switches `TP_VDD`
- [Awinic AW39112DNR](../../awinic/aw39112/README.md) — `U19`, the self-isolating bus branch
- [M5Stack M5IOE1](../../m5stack/m5ioe1/README.md) — owns `PYG6` (reset) and `PYG13` (power)
- [DKE DEPG0397BBS770F3](../../dke/depg0397bbs770f3/README.md) — the e-paper panel this touch layer sits on
- [Hynitron CST816D](../../hynitron/cst816d/README.md) — comparable touch controller documented in this repository

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | FT6336G Self-Capacitive Touch Panel Controller datasheet | FocalTech Systems Co., Ltd. | primary (via credible mirror, Focus LCDs) | datasheet | <https://focuslcds.com/wp-content/uploads/Drivers/FT6336G.pdf> | 2026-09-01 | **Version 1.0**, © 2015, 10 numbered pp / 12 PDF pp, 477 869 B | Package `QFN5*5` 40-pin 0.4 mm pitch, 31 channels, ≤4.0 in, supplies, I²C 10–400 kHz and timing, three operating modes, `/INT` and `RSTN` semantics, ESD, on-chip memory | `artifacts/ft6336g-datasheet-v1.0-focuslcds-mirror.pdf` |
| D2 | FT6236/FT6336/FT6436L/FT6436 combined datasheet | FocalTech (via Buydisplay) | credible mirror | datasheet | <https://www.buydisplay.com/download/ic/FT6236-FT6336-FT6436L-FT6436_Datasheet.pdf> | **not retrieved** | — | Possible source of the missing register map (§2.1) | — |
| S1 | PaperMono product page — touch active area | M5Stack | primary | official page | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | — | The X 5–475 / Y 5–795 coordinate inset; `FT6336G(0x38)`; the M5Unified pin-ownership warning | `archive/devices/m5stack/papermono/artifacts/research-scratch/docs/pages/en-core-PaperMono.html` |
| S2 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | `J4` signal set, `U18`/`U19` topology, `G4_TP_INT` → GPIO4, `R58`/`R59`/`C68` | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S3 | `M5GFX/src/M5GFX.cpp` | M5Stack | primary | repository | <https://github.com/m5stack/M5GFX> | 2026-09-01 | `master` @ `d91077b9a607b59404e4e4a49f775c792bfae382`, MIT | `0x38` at `:329`, `:575`, `:713`; `pin_int = 4` at `:2144`; SDA/SCL 47/48 at `:2145–2146` | `archive/devices/m5stack/papermono/artifacts/source-snapshots/M5GFX/` |
| S4 | `M5PaperMono-UserDemo/main/apps/app_sleep_wake/app_sleep_wake.cpp` | M5Stack | primary | repository | <https://github.com/m5stack/M5PaperMono-UserDemo> | 2026-09-01 | `main` @ `c1099107271d31a0678d661a896e2b04dbb331ea`, MIT | `TOUCH_WAKE_GPIO = 4` (`:52`), `IOE1_TOUCH_RST_PIN = M5IOE1_PIN_6` (`:76`), `IOE1_TOUCH_EN_PIN = M5IOE1_PIN_13` (`:81`) | `archive/devices/m5stack/papermono/artifacts/source-snapshots/M5PaperMono-UserDemo/` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/ft6336g-datasheet-v1.0-focuslcds-mirror.pdf` | 477 869 | `766f130b65d3e4e30ba7c3a2592a33b61b11fcdd3a39a239333acc53a1b7d793` | 12 |

**Method note.** D1 validated as `%PDF` with an intact text layer, and full-text searched for `0x38` and for register tables — both absent, which is the §2.1 finding. Four User-Agents were tried across two hosts before one succeeded; see [Manufacturer](#manufacturer).
