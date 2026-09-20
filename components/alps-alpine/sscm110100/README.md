# Alps Alpine SSCM110100 — the two knob rotation sensors

- **Category:** detector switch — Alps Alpine's own classification is **"Compact Two-way Detection"**, *not* rotary encoder
- **Reference designators:** `SW2` (knob 1) and `SW1` (knob 2)
- **Owning MCUs:** **split.** `SW2` → ESP32-S3. `SW1` → ESP32-U4WDH. Different processors, no shared electrical path
- **Research status:** part identified from the manufacturer's own catalog; board wiring read pin-by-pin; decoding behaviour read from vendor source. **Two widespread assumptions about these parts are contradicted by the evidence — see §2**
- **Retrieved:** 2026-08-21; catalog, schematic and decoder source re-audited 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[FW]** shipped factory binary · **[SRC]** vendor demo source · **[DOC]** manufacturer catalog/datasheet · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. Identity

`SSCM110100` appears twice in the schematic as the BOM string for `SW1` and `SW2` **[SCH sheet 1 `1_LCD&POWER.png`]**. Alps Alpine's SSCM series catalog (retained locally, `Update: 2510`) lists exactly two members **[DOC]**:

| Product No. | Poles | Positions | Operating force | Terminal type | Total travel | Location lug | Dimensions (W×D×H) |
|---|---:|---:|---|---|---:|---|---|
| **SSCM110100** (fitted) | 1 | 2 | 0.35 N max | For PC board (reflow) | 1.57 mm | **With** | 4.0 × 5.0 × 1.5 mm |
| SSCM120100 | 1 | 2 | 0.35 N max | For PC board (reflow) | 1.57 mm | Without | 4.0 × 5.0 × 1.5 mm |

The only difference between the two part numbers is the **location lug**, a mechanical alignment peg. `SSCM110100` is the one **with** the lug.

Alps Alpine describes the series as: *"Thin-profile type with a body height of 1.5 mm, capable of detecting two lateral directions."* **[DOC]** The catalog's listed applications are smartphones, headsets, wearables, handheld consoles and cameras.

### 1.1 Electrical and mechanical ratings **[DOC]**

| Parameter | Value |
|---|---|
| Rating, max (resistive load) | **1 mA at 5 V DC** |
| Rating, min (resistive load) | **50 µA at 3 V DC** |
| Contact resistance, initial | **2 Ω max** |
| Contact resistance, after operating life | **5 Ω max** |
| Operating life, no load | **50,000 cycles** |
| Operating life, at max rating | **50,000 cycles**, contact resistance 5 Ω max |
| Operating force | 0.35 N max |
| Total travel | 1.57 mm |
| Body height | 1.5 mm |
| Mounting | SMT, reflow |
| Packing | 3,000 per reel, 16 mm tape |

Two of these deserve emphasis:

- **The maximum rating is 1 mA at 5 V.** This is a *signal* switch, not a power switch. On this board that is comfortably satisfied — see §3.2 — but do not repurpose one to switch anything.
- **50,000 cycles.** For a control a user twiddles, this is the number that governs product life. It is a consumer-grade, not industrial-grade, rating. A panel-mount industrial encoder is typically 100,000–1,000,000 cycles. (The detent count per revolution is not published for this board — see §5 — so this does not convert cleanly into "full turns".)

The catalog carries an explicit disclaimer: *"This catalog shows only outline specifications. When using the products, please obtain formal specifications for supply."* **[DOC]** There is therefore **no published bounce time, no contact timing diagram and no operating/release position tolerance** for this part. Everything about timing in §4 is derived from the vendor's own debounce constants and from general practice, and is labelled accordingly.

## 2. ⚠ Two things this part is not

Both are commonly assumed — including in some of the language used around this board — and both are contradicted by primary evidence.

### 2.1 It is not a quadrature rotary encoder

Waveshare's material calls the assembly a "dual encoder" **[WEB]**, and the nets are named `EC1_A`/`EC1_B`/`EC2_A`/`EC2_B`, which looks exactly like two channels of a quadrature encoder. But:

- Alps Alpine classifies `SSCM110100` as a **detector switch**, 1 pole / 2 positions, "capable of detecting two lateral directions" **[DOC]**. A quadrature encoder is not 1 pole / 2 positions.
- The catalog gives an **operating force** and a **total travel** — switch parameters. Rotary encoders are specified in detents per revolution and pulses per revolution, neither of which appears anywhere.
- Decisively: **Waveshare's own decoder does not perform quadrature decoding.** See §4.1. It treats the A and B lines as two entirely independent momentary contacts — one meaning "left", one meaning "right" — with no phase relationship and no state machine.

The physical arrangement is therefore **[INF]**: a rotating cam or lever driven by the knob deflects the detector switch laterally, closing the "left" contact or the "right" contact depending on the direction of travel, once per detent. The knob feels like an encoder and behaves like one at the API level, but the sensing element is a two-way switch and **the electrical waveform is not a quadrature pattern.**

The practical consequences are in §4 and they are significant — most importantly, **the ESP32's PCNT peripheral in quadrature mode is the wrong tool here**, which is the opposite of the usual advice for a knob.

### 2.2 There is no push contact on either knob

`SSCM110100` has **no push function** — it detects two *lateral* directions **[DOC]**. And the schematic confirms the board does not wire one:

- `SW2` (knob 1): pins **1 and 4 tied to GND**; pin **2** = `EC1_A`; pin **3** = `EC1_B` **[SCH sheet 1]**
- `SW1` (knob 2): pins **1 and 4 tied to GND**; pin **2** = `EC2_A`; pin **3** = `EC2_B` **[SCH sheet 1]**

Four terminals, all accounted for, two of them common. **There is no fifth terminal and no separate push-switch symbol anywhere in the five sheets.**

If your application needs "click the knob", the mechanism available on this board is the **touchscreen** — the knob's top face is the 1.8" round touch LCD **[INF, consistent with the CST816D touch controller being present]**. A tap on the display is the press gesture. There is no mechanical press to debounce.

This is separately recorded board-wide: [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md) notes *"There is no push/press contact wired from knob 2 to the secondary MCU. Rotation only."* The finding here is stronger: **neither knob has a push contact wired, and the part has no push function to wire.**

## 3. Exact wiring on this board

### 3.1 The two knobs, and which MCU owns each

| | **Knob 1** | **Knob 2** |
|---|---|---|
| Designator | `SW2` | `SW1` |
| Nets | `EC1_A`, `EC1_B` | `EC2_A`, `EC2_B` |
| **Owning MCU** | **ESP32-S3** (`U2`) | **ESP32-U4WDH** (`U14`) |
| A channel → | **GPIO8** | **GPIO19** (package pin 38) |
| B channel → | **GPIO7** | **GPIO22** (package pin 39) |
| Pull-up on A | `R60` 10 kΩ → 3V3 | `R55` 10 kΩ → 3V3 |
| Pull-up on B | `R59` 10 kΩ → 3V3 | `R56` 10 kΩ → 3V3 |
| Common (switch pins 1, 4) | GND | GND |
| Active level | **Low** (contact pulls to GND) | **Low** |
| Vendor source exists? | **Yes** — `04_Encoder_Test`, `07_Audio_Test` | **No. None, anywhere in the archive** |

**[SCH sheets 1, 2 and 3]** for the wiring; **[SRC]** for source availability.

Note the A/B GPIO ordering on the S3: `EC1_A` is GPIO**8** and `EC1_B` is GPIO**7**. The vendor's example defines them in that order (`EXAMPLE_ENCODER_ECA_PIN 8`, `EXAMPLE_ENCODER_ECB_PIN 7`) **[SRC]**. Swapping them inverts the direction sense.

### 3.2 Why the wiring is electrically comfortable

The switch is rated 1 mA max **[DOC]**. Closed-contact current here is `3.3 V / 10 kΩ = 330 µA` — a third of the maximum, and comfortably above the 50 µA minimum. The minimum matters as much as the maximum: dry-circuit switching below the specified minimum current is what causes contact-resistance drift over time, and 330 µA is safely clear of it.

Voltage across a closed contact at 2 Ω initial resistance: `330 µA × 2 Ω = 0.66 mV`; at end-of-life 5 Ω, 1.65 mV. **Contact resistance will never be why a read fails on this board.**

### 3.3 The ESP32-U4WDH side is a documentation dead end

`SW1` is wired to GPIO19 and GPIO22 of the secondary MCU. That MCU has:

- **No published source code of any kind.** All eight ESP-IDF demo projects target `esp32s3`; not one targets `esp32` **[SRC]**
- Only a prebuilt blob, `ESP32-KNOB_ESP32_0.bin`, which cannot be rebuilt **[FW]**
- No spare pins, and no documented inter-MCU protocol

So knob 2's rotation events reach the S3, if they reach it at all, over the undocumented inter-MCU UART. See [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md#2-the-inter-mcu-link-a-two-wire-uart). **If you want knob 2 in your own application, you will be writing replacement ESP32-U4WDH firmware.** Back up the factory blob first.

## 4. Decoding: what the vendor does, and what you should do

### 4.1 Waveshare's decoder — read it before you copy it

The file is `bidi_switch_knob.c`, present identically in `Arduino/examples/04_Encoder_Test/` and `Arduino/examples/07_Audio_Test/` **[SRC]**. Its header says:

```
SPDX-FileCopyrightText: 2016-2024 Espressif Systems (Shanghai) CO LTD
SPDX-License-Identifier: Apache-2.0
Modified by planevina 2025-01-20
```

It is **a fork of Espressif's `knob` component from esp-iot-solution with the quadrature state machine removed.** The name is the tell: *bidi*rectional *switch* knob.

What it actually does:

| Aspect | Implementation **[SRC]** |
|---|---|
| Sampling | `esp_timer` periodic callback, `TICKS_INTERVAL` = **3 ms**. Polling, not interrupts |
| Debounce | `DEBOUNCE_TICKS` = **2** — a contact must be held closed across at least two polls (**≥ ~6 ms**) before it counts |
| Decoding | **None.** `process_knob_channel()` is called twice, once per line, entirely independently |
| A line | Counted as `KNOB_RIGHT`, `count_value += 1` |
| B line | Counted as `KNOB_LEFT`, `count_value -= 1` |
| Edge counted | The **rising** edge — i.e. contact *release*, after a qualifying low period |
| GPIO config | `GPIO_MODE_INPUT`, `pull_up_en = 1`, `intr_type = GPIO_INTR_DISABLE` |

The two channels never look at each other. There is no `(prev_state << 2) | new_state` lookup table, no ×1/×2/×4 decoding, no direction inference from phase. **That Waveshare's own engineer deleted the quadrature logic from Espressif's component is the strongest available evidence about what this hardware actually produces.**

The counting logic is subtle enough to be worth reading closely:

```c
if (current_level == 0) {                       // contact closed
    if (current_level != *prev_level) *debounce_cnt = 0;   // just closed: restart
    else (*debounce_cnt)++;                                // still closed: accumulate
} else {                                        // contact open
    if (current_level != *prev_level && ++(*debounce_cnt) >= DEBOUNCE_TICKS) {
        *debounce_cnt = 0;
        *count_value += is_increment ? 1 : -1;  // COUNT HERE, on release
        knob->event = event;
        CALL_EVENT_CB(event);
    } else *debounce_cnt = 0;
}
*prev_level = current_level;
```

The accumulator only increments while the contact is *held closed*. The count fires on the transition back to open, and only if the accumulator had already reached 1 — meaning the contact was closed across at least two 3 ms polls. So: **closed for ≥ ~6 ms, then released → one count.** Anything shorter is discarded as bounce.

Also note `knob_gpio_init()` sets `pull_up_en = 1`, enabling the S3's internal pull-up on top of the external 10 kΩ. Harmless here (the parallel result is ~8.2 kΩ), but redundant, and it would mask a missing-external-pull-up fault on a port.

### 4.2 Consequences and limits of that design

| Consequence | Detail |
|---|---|
| **Maximum rate is bounded by the poll interval** | Each detent needs ≥ 2 polls closed plus 1 poll open ≈ 9 ms. **Roughly 110 detents/second ceiling**, and that is optimistic. Fast flicks will lose counts |
| **No error detection** | A real quadrature decoder can spot an illegal state transition and refuse to count. This cannot. Bounce that survives 6 ms is counted as a real detent |
| **Both directions can count in the same poll** | Nothing prevents it. On a two-way switch that should be mechanically impossible, but a fault or marginal cam position produces net-zero jitter rather than an error |
| **No ×2 or ×4 resolution** | With no phase information, one count per detent is all there is. This is a design consequence, not a tuning parameter |
| **Latency** | ~6–9 ms best case from contact to callback. Fine for making a haptic click feel simultaneous with the detent — see [generic/lra-motor §5](../../generic/lra-motor/README.md#5-pitfalls) |

### 4.3 ⚠ PCNT: right peripheral, wrong mode

For a genuine quadrature encoder on an ESP32-S3 the correct answer is almost always the **PCNT (Pulse Counter)** peripheral: hardware decoding, zero CPU cost, no missed pulses, a clean ESP-IDF driver (`driver/pulse_cnt.h`, the `pcnt_unit_*` API, stable since ESP-IDF 5.0), 4 units × 2 channels on the S3, and a hardware glitch filter **[DOC, ESP32-S3 TRM]**.

**On this board the usual advice does not apply**, for the reason in §2.1.

| Approach | Suitability here |
|---|---|
| **PCNT in quadrature mode** (edge action on A, B as level control) | **Wrong.** It requires a phase relationship this hardware does not produce. It will count erratically |
| **PCNT as two independent edge counters** (A → increment, B → decrement, two channels on one unit, both `LEVEL_ACTION_KEEP`) | **Works, and is the best hardware-assisted option.** You get a free hardware glitch filter and lose the 3 ms polling ceiling |
| **GPIO ISR on both lines** | Workable. `GPIO_INTR_NEGEDGE` plus a timestamp in the handler. But you now own debounce, in an ISR, with `IRAM_ATTR` discipline. More code, more ways to be wrong |
| **Polling (what the vendor does)** | Simplest, adequate for a hand-turned knob, and has the great merit of being the code known to work with this exact mechanism. **Start here** |

If you do move to PCNT-as-two-counters, the glitch filter is the thing you actually want from it. The SSCM110100 has **no published bounce time** **[DOC — outline specifications only]**, so size it empirically. The vendor's ~6 ms is a generous starting point; a hardware filter of 1–2 ms plus a short software confirmation usually beats it on responsiveness without losing counts.

### 4.4 A minimal ESP-IDF PCNT setup, if you want it

```c
#include "driver/pulse_cnt.h"

// Knob 1 only: EC1_A = GPIO8 (right), EC1_B = GPIO7 (left).
// NOT quadrature -- two independent edge counters on one unit.

pcnt_unit_config_t unit_cfg = { .high_limit = 1000, .low_limit = -1000 };
pcnt_unit_handle_t unit;
ESP_ERROR_CHECK(pcnt_new_unit(&unit_cfg, &unit));

// Glitch filter. Tune this: the switch has no published bounce spec.
pcnt_glitch_filter_config_t filt = { .max_glitch_ns = 1000 * 1000 };  // 1 ms
ESP_ERROR_CHECK(pcnt_unit_set_glitch_filter(unit, &filt));

pcnt_chan_config_t ch_a = { .edge_gpio_num = 8, .level_gpio_num = -1 };
pcnt_chan_config_t ch_b = { .edge_gpio_num = 7, .level_gpio_num = -1 };
pcnt_channel_handle_t a, b;
ESP_ERROR_CHECK(pcnt_new_channel(unit, &ch_a, &a));
ESP_ERROR_CHECK(pcnt_new_channel(unit, &ch_b, &b));

// Contacts are active LOW (10k pull-ups to 3V3, common to GND).
// Count the falling edge = contact closure.
ESP_ERROR_CHECK(pcnt_channel_set_edge_action(a,
    PCNT_CHANNEL_EDGE_ACTION_INCREASE,   // negedge: A closed -> right
    PCNT_CHANNEL_EDGE_ACTION_HOLD));
ESP_ERROR_CHECK(pcnt_channel_set_edge_action(b,
    PCNT_CHANNEL_EDGE_ACTION_DECREASE,   // negedge: B closed -> left
    PCNT_CHANNEL_EDGE_ACTION_HOLD));
ESP_ERROR_CHECK(pcnt_channel_set_level_action(a,
    PCNT_CHANNEL_LEVEL_ACTION_KEEP, PCNT_CHANNEL_LEVEL_ACTION_KEEP));
ESP_ERROR_CHECK(pcnt_channel_set_level_action(b,
    PCNT_CHANNEL_LEVEL_ACTION_KEEP, PCNT_CHANNEL_LEVEL_ACTION_KEEP));

ESP_ERROR_CHECK(pcnt_unit_enable(unit));
ESP_ERROR_CHECK(pcnt_unit_clear_count(unit));
ESP_ERROR_CHECK(pcnt_unit_start(unit));

// Then poll pcnt_unit_get_count(unit, &delta) from your UI task,
// or register a watch point with pcnt_unit_add_watch_point().
```

**Validate this against real hardware before relying on it.** It is the correct construction *given* the two-independent-contacts model established in §2.1 and §4.1, but no vendor code uses PCNT on this board, so it is untested here.

### 4.5 Libraries and versions

| Option | Version | Where | Notes |
|---|---|---|---|
| `bidi_switch_knob.c` (vendored) | modified 2025-01-20 | demo archive, `Arduino/examples/04_Encoder_Test/` | **What actually works on this board.** Apache-2.0, forked from Espressif's `knob`. Depends only on `driver/gpio` and `esp_timer` |
| esp-iot-solution `knob` | `espressif/knob` via the component registry | https://components.espressif.com/components/espressif/knob | The upstream this was forked from. **It expects real quadrature** — using it unmodified here is a mistake |
| ESP-IDF `driver/pulse_cnt.h` | ESP-IDF ≥ 5.0; board demos build on **5.3.2** | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/pcnt.html | See §4.3–4.4 |
| Arduino `ESP32Encoder` | 0.11.x | https://github.com/madhephaestus/ESP32Encoder | Wraps PCNT in quadrature mode. **Do not use here** — wrong model |
| LVGL encoder input device | LVGL 8.x, vendored in the demo | `Arduino/libraries/lvgl/` | `LV_INDEV_TYPE_ENCODER`. Feed it the +1/−1 deltas from whichever decoder you pick; it does not care how you got them |

The ESP-IDF projects in the archive build against **ESP-IDF 5.3.2** **[SRC, `sdkconfig` header line]**.

### 4.6 The vendor's usage pattern

`04_Encoder_Test` is worth reading as the canonical integration **[SRC]**: it registers `KNOB_LEFT` / `KNOB_RIGHT` callbacks that only set FreeRTOS event-group bits, and does all the actual work in a separate task waiting on `xEventGroupWaitBits()`. That is the right shape — the callback runs from the `esp_timer` task, and you do not want display or I2C work happening there. `07_Audio_Test` reuses the identical file to drive playback volume.

## 5. Open questions

| Question | Status |
|---|---|
| **Detents per revolution** | **Unknown.** Not published by Waveshare, and not a property of the SSCM110100 itself — it is set by the cam/lever in the knob assembly, which has no documentation. Measure it: `iot_knob_clear_count_value()`, one full turn, `iot_knob_get_count_value()` |
| Contact bounce time | **Unknown.** The Alps catalog is explicitly outline specifications only and omits it. Formal specifications must be obtained from Alps Alpine for supply |
| Operating/release position tolerance | **Unknown**, same reason |
| The cam/lever mechanism | **Undocumented.** No mechanical CAD, assembly drawing or exploded view in the published archive |
| Whether the factory ESP32-U4WDH firmware forwards knob 2 events over the inter-MCU UART | **Unknown.** The link's framing is undocumented — see [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md#2-the-inter-mcu-link-a-two-wire-uart) |
| Fitted date code / lot | **Unknown** |

## 6. Alternatives

If you are respinning rather than programming:

| Part | Trade-off |
|---|---|
| **SSCM110100** (this) | 4.0 × 5.0 × 1.5 mm, extremely thin, cheap, SMT. **50,000 cycles**, no push, no true quadrature, resolution fixed by the cam |
| SSCM120100 | Identical but without the location lug. Electrically drop-in; check whether the PCB has a lug hole |
| A real SMT quadrature encoder (Alps EC05 family, Bourns PEC11R, …) | True phase quadrature, ×4 decoding, PCNT-friendly, usually a push contact, often 100,000+ cycles. **Much taller** — an EC11 is ~20 mm deep, which is why it is not here |
| Magnetic encoder (AS5600, MT6701) | Contactless, effectively unlimited life, absolute angle, I2C. No detents unless you add them mechanically. Adds an I2C device and a diametric magnet |
| Optical encoder | Highest resolution, no wear. Power-hungry and physically large |

For a device this thin the SSCM110100 choice is defensible. The 50,000-cycle rating is the thing to be aware of if you are designing something a user turns constantly.

## Manufacturer

**Alps Alpine** — see the [Alps Alpine documentation-sourcing guide](../../../vendors/alps-alpine/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `SW2` on ESP32-S3 GPIO8/GPIO7, `SW1` on ESP32-U4WDH GPIO19/GPIO22

## Related pages

- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)
- [Dual-MCU architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md) — why knob 2 is on the other processor
- [espressif/esp32-u4wdh](../../espressif/esp32-u4wdh/README.md) — the MCU that owns knob 2, and has no published source
- [generic/lra-motor](../../generic/lra-motor/README.md) — the haptic feedback felt alongside each mechanical detent

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Alps Alpine SSCM110100 product page | https://tech.alpsalpine.com/e/products/detail/SSCM110100/ | 2026-08-21 | — |
| Alps Alpine SSCM series catalog PDF (`Update: 2510`) — source of every rating in §1.1 | https://tech.alpsalpine.com/cms.media/product_catalog_sw_01_sscm_en_90b44d6d7f.pdf | 2026-08-21 | [artifacts/sscm-series-catalog.pdf](artifacts/sscm-series-catalog.pdf) |
| Board schematic sheet 1 (`SW1`/`SW2` symbols, pull-ups `R55`/`R56`/`R59`/`R60`) | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Board schematic sheet 2 (`EC1_A`/`EC1_B` → S3 GPIO8/GPIO7) | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Board schematic sheet 3 (`EC2_A`/`EC2_B` → U4WDH GPIO19/GPIO22) | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/3_ESP32-CHIP.png` |
| Waveshare demo `04_Encoder_Test` — `bidi_switch_knob.c` / `.h` | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/04_Encoder_Test/` |
| Espressif `knob` component (the upstream that was forked) | https://components.espressif.com/components/espressif/knob | 2026-08-23 | — |
| ESP-IDF v5.3.2 PCNT driver | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/pcnt.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
| ESP32-S3 Technical Reference Manual (PCNT chapter, unit/channel counts) | https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual.pdf` |
| Waveshare product page ("dual encoder" wording) | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
