# Espressif errata, in practical form — ESP32 and ESP32-S3

- **Purpose:** of the 32 ESP32 errata and 8 ESP32-S3 errata, **which ones actually change what you write or how you wire a board**, per silicon revision, with the symptom and the workaround.
- **Extracted:** 2026-08-24
- **Companion pages:** [soc-peripheral-reference.md](soc-peripheral-reference.md) (peripheral counts) · [memory-and-boot.md](memory-and-boot.md) (memory maps, boot, strapping, eFuse)

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Quoted or read directly from the cited Espressif errata / TRM / datasheet PDF |
| **[INF]** | Inference, prioritisation or synthesis by this knowledge base |

## Sources

| Key | Document | Version | Pages | Local artifact |
|---|---|---|---:|---|
| **ERR-32** | ESP32 Series SoC Errata | **v3.0** | 36 | [`esp32-errata.pdf`](../../components/espressif/esp32-u4wdh/artifacts/esp32-errata.pdf) |
| **ERR-S3** | ESP32-S3 Series SoC Errata | **v1.3** | 15 | [`esp32-s3-errata.pdf`](../../components/espressif/esp32-s3r8/artifacts/esp32-s3-errata.pdf) |
| **ERR-P4** | ESP32-P4 Series SoC Errata | — | 19 | [`esp32-p4-errata.pdf`](../../components/espressif/esp32-p4/artifacts/esp32-p4-errata.pdf) — summarised in [esp32-p4 README § 10](../../components/espressif/esp32-p4/README.md#10-errata-summary), not re-covered here |

Chip-revision identification (which eFuse bits, which chip/module markings) is in **[memory-and-boot.md § 7](memory-and-boot.md#7-efuse-and-chip-revision-detection)**.

---

## 1. ⚠ Read this first: most errata do not need your attention

**ESP-IDF already works around the majority of these.** Espressif's own text repeatedly says so — e.g. *"This issue has been automatically bypassed … in ESP-IDF v4.4.6+, v5.0.4+, v5.1.1+, v5.2, and above versions."* **[DOC]** ERR-S3 v1.3 § 3.1, p. 6.

So the useful question is not "what errata exist" but **"what do I have to do differently?"** Three categories:

| Category | What it means for you |
|---|---|
| 🔴 **Design-level** | Changes your **schematic, pin allocation, or firmware architecture**. IDF cannot save you. |
| 🟠 **Code-level** | You must write code a particular way, or avoid an API. IDF may partly help. |
| 🟢 **Handled** | IDF bypasses it silently, on a modern version. Know it exists; do nothing. |

Everything below is sorted into these.

---

## 2. ESP32 — the errata that actually bite

**Revision landscape:** v0.0, v1.0, v1.1, v3.0, v3.1 (there is no v2.x). **[DOC]** ERR-32 v3.0 Table 2.1, p. 6. Currently-manufactured ESP32 parts, including the **ESP32-U4WDH** on the Knob board, are **v3.0 or v3.1** — see [esp32-u4wdh README § 21](../../components/espressif/esp32-u4wdh/README.md).

### 2.1 The short list for a v3.0/v3.1 part

If you have modern silicon, **these are the errata still affecting you.** Everything else on ESP32 was fixed at v1.0 or v3.0.

| ID | Class | One-line symptom |
|---|---|---|
| [CPU-3.16](#cpu-316--speculative-reads-and-fifo-read-pointer-lag) | 🟠 | Peripheral register reads are speculative; FIFO reads at high CPU clock return stale data |
| [CPU-3.21](#cpu-321--an-interrupt-during-a-uarti2s-fifo-read-hangs-the-bus-bridge) | 🔴 | An interrupt during a UART/I2S FIFO **read** hangs all subsequent APB access |
| [CPU-3.18](#cpu-318--the-umbrella-entry) | 🟢 | Umbrella entry pointing at the other three |
| [ULP-3.19](#ulp-319--ulptouch-and-ext0-wake-are-mutually-exclusive-in-deep-sleep) | 🔴 | **ULP/touch and EXT0 wake cannot both be used in Deep-sleep** |
| [GPIO-3.6](#-handled-by-esp-idf-or-fixed-in-silicon-you-probably-have) | 🟢 | GPIO pull registers are inert on RTC-capable pads |
| [GPIO-3.14](#gpio-314--one-edge-triggered-gpio-interrupt-poisons-its-whole-group) | 🔴 | **One edge-triggered GPIO IRQ disables all other IRQs in its 32-pin group** |
| [GPIO-3.11](#gpio-311--gpio36-and-gpio39-glitch-low-when-an-adc-powers-on) | 🔴 | GPIO36/GPIO39 glitch low ~80 ns whenever an ADC or AMP powers on |
| [CLK-3.22](#clk-322--wi-fi--ethernet-cannot-share-the-internal-apll) | 🔴 | Wi-Fi + Ethernet needs an **external** RMII clock source |
| [RTC-126](#rtc-126--rtc-register-read-error-after-light-sleep-both-chips) | 🟠 | Don't power down RTC peripherals in Light-sleep |
| [WDT-3.15](#wdt-315--dual-core-cache-live-lock-v30v31-only) | 🟠 | **New in v3.0/v3.1** — dual-core cache live lock → interrupt watchdog |
| [UART-3.17](#-handled-by-esp-idf-or-fixed-in-silicon-you-probably-have) | 🟢 | `fifo_cnt` under-reports by 1 if the read is interrupted |
| [LEDC-3.12](#ledc-312--duty-overflow-in-decremental-fade) | 🟠 | Duty overflow during decremental fade |
| TWAI-3.13.\* (11 entries) | 🟠 | CAN protocol conformance deviations, all revisions, mostly unfixable |

---

### 🔴 Design-level

#### `ULP-3.19` — ULP/touch and EXT0 wake are mutually exclusive in Deep-sleep

**Affects: v0.0, v1.0, v1.1, v3.0, v3.1. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.9, p. 13.

> *"In Deep-sleep mode, if the RTC_PERIH power domain (RTC Peripherals) remains powered up, the ULP coprocessor and touch sensor will receive the wake-up signal earlier than the clock management module. This causes them to operate under SLOW_CLK for a period before switching to FAST_CLK, leading to inaccuracies in the operating clock. Therefore, in Deep-sleep mode, if RTC_PERIH is powered up, the ULP co-processor and touch sensor cannot be used."*

**The trade Espressif spells out [DOC]:**

- Need **EXT0 wake**? `RTC_PERIPH` must stay powered → **no ULP, no touch**.
- Need **ULP or touch**? `RTC_PERIPH` must be powered down → **no EXT0 wake**.

**[INF] Why this is design-level, not code-level:** it decides your *wake architecture* before you cut a PCB. If a product needs both a capacitive-touch wake and a single-pin external wake, on ESP32 you must use **EXT1** (which does not require `RTC_PERIPH`) for the external signal, or move to a different part. Discovering this after layout is expensive.

#### `GPIO-3.14` — one edge-triggered GPIO interrupt poisons its whole group

**Affects: all revisions. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.11, pp. 15–16.

> *"GPIO0 ~ GPIO31 share a set of interrupt configuration registers and belong to one group, GPIO32 ~ GPIO39 share another set of registers and belong to another group, and RTC GPIO0 ~ GPIO17 share yet another set of registers and belong to yet another group. If one GPIO pad within a group is configured with edge-triggered interrupt, then other interrupts (including both edge-triggered and level-triggered interrupts) within that group cannot be configured."*
>
> *"There is no such limitation for level-triggered interrupts."*

**Workaround — simulate edges with levels [DOC]:**

> To trigger on a **rising** edge: set the interrupt type to *high*; after servicing, change it to *low* (a second interrupt fires immediately — ignore it).
> To trigger on a **falling** edge: set the interrupt type to *low*; after servicing, change it to *high* (again, ignore the immediate second interrupt).

**[INF] This is the errata most likely to surprise you in a real design.** Any board with several interrupt-driven inputs — a rotary encoder, a touch controller IRQ, an accelerometer IRQ, a button — will land them in GPIO0–31 together. The *first* one you configure edge-triggered silently breaks the rest. Symptom: "my second interrupt handler never fires and `gpio_isr_handler_add` returned OK." **Design rule: on ESP32, use level-triggered GPIO interrupts throughout, or accept the level-simulation dance everywhere.**

#### `GPIO-3.11` — GPIO36 and GPIO39 glitch low when an ADC powers on

**Affects: all revisions. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.12, p. 16.

Powering on **SAR ADC1**, **SAR ADC2** or **AMP** pulls the *inputs* of GPIO36 and GPIO39 down for approximately **80 ns**.

> **Workaround [DOC]:** *"When enabling power for any of these peripherals, ignore input from GPIO36 and GPIO39."*

**[INF] Design-level because GPIO36 and GPIO39 are two of the six input-only pins** ([soc-peripheral-reference.md § 11](soc-peripheral-reference.md#11-gpio--count-restrictions-and-what-the-memory-eats)) — the ones a designer reaches for precisely because they cannot accidentally be driven. Putting an edge-sensitive signal (encoder, pulse counter input, IRQ line) on GPIO36/39 in a design that also uses the ADC produces spurious counts or interrupts. **Put ADC inputs on 36/39 if you like; do not put digital edge inputs there.**

#### `CPU-3.21` — an interrupt during a UART/I2S FIFO *read* hangs the bus bridge

**Affects: all revisions. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.7, p. 12.

> *"When the CPU attempts to read five FIFO registers `0x3FF40000` (UART0), `0x3FF50000` (UART1), `0x3FF6E000` (UART2), `0x3FF4F004` (I2S0), and `0x3FF6D004` (I2S1), and if an interrupt occurs, the read request will be interrupted. This will cause the bus bridge to be stuck in a state of waiting for the read request to end. Consequently, the subsequent access to the APB peripheral registers (`0x3FF40000` ~ `0x3FF7FFFF` or `0x60000000` ~ `0x6003FFFF`) by any CPUs will be rejected and halted."*
>
> *"Writing to these five FIFO registers does not have such an issue."*
>
> **Workaround:** *"Disable CPU interrupts before reading these five FIFO registers. Enable CPU interrupts after read access."*

**[INF]** A **hard hang of all peripheral access**, not a data corruption. If you write your own UART or I2S FIFO drain loop instead of using the IDF driver, you must bracket it with `portENTER_CRITICAL`/`portEXIT_CRITICAL`. This is why hand-rolled "fast" UART reads on ESP32 sometimes lock the whole chip under load.

#### `CLK-3.22` — Wi-Fi + Ethernet cannot share the internal APLL

**Affects: all revisions. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.17, p. 19.

> *"In RMII working mode, the Ethernet MAC and PHY require a common 50 MHz reference clock (i.e., the RMII clock). If Wi-Fi and Ethernet are used simultaneously, the RMII clock cannot be generated by the internal APLL clock, as it would result in clock instability."*
>
> **Workarounds [DOC]:**
> 1. *"If you want to use the internal APLL to generate the reference clock, you need to disable Wi-Fi."*
> 2. *"If you want to use both Ethernet and Wi-Fi simultaneously, you need to use an external PHY or external clock source to provide the reference clock."*

**[INF] This is a BOM decision.** A Wi-Fi + wired-Ethernet gateway on ESP32 needs an **external 50 MHz oscillator** on the board. Omitting it to save a part means Ethernet works only with Wi-Fi off.

---

### 🟠 Code-level

#### `CPU-3.16` — speculative reads and FIFO read-pointer lag

**Affects: all revisions. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.3, pp. 9–10.

Three related problems in `0x3FF0_0000`–`0x3FF1_EFFF` and `0x3FF4_0000`–`0x3FF7_FFFF`:

1. *"The CPU read operations that fall in these two address spaces are speculative. Speculative read operations can cause the behavior described by the program to be inconsistent with the actual behavior of the hardware."*
2. *"If the two CPUs continuously access address space `0x3FF0_0000` ~ `0x3FF1_EFFF` at the same time, some of the access may be lost."*
3. *"When the CPU reads FIFO through the address space `0x3FF4_0000` ~ `0x3FF7_0000`, the FIFO read pointer is updated with delays… When a new FIFO read request arrives, the FIFO read pointer has not been updated, causing the CPU to read the value of the previous FIFO read operation."*

**Workarounds [DOC]:**

1. *"Insert 'MEMW' instruction before the CPU access operation… That is, in C/C++, software needs to always use the 'volatile' attribute when accessing registers in these two address spaces."*
2. *"When the CPU frequency is 160 MHz, add six 'nop' between two consecutive FIFO reads. When the CPU frequency is 240 MHz, add seven 'nop' between two consecutive FIFO reads."*

**[INF] The `volatile` requirement is the one to internalise.** Any hand-written register access on ESP32 must go through a `volatile` pointer — this is not merely good practice, it is a documented hardware requirement. The `nop` padding requirement is *frequency-dependent*, which means code that works at 80 MHz can fail at 240 MHz. If you bump `CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ` and a hand-rolled FIFO reader starts duplicating bytes, this is why.

#### `CPU-3.18` — the umbrella entry

**Affects: all revisions.** **[DOC]** ERR-32 v3.0 § 3.2, pp. 8–9. Not an independent bug; it aggregates `CPU-3.3`, `CPU-3.10` and `CPU-3.16` into one table showing which operations are safe on which address space per revision. Useful reference, no separate action. Class 🟢.

The table's headline result for **v3.0/v3.1** **[DOC]**: DPORT non-FIFO reads and writes and FIFO reads and writes are all *"Yes"* (correct); AHB FIFO **reads** are *"No (No such feature, unpredictable results)"* on every revision — **you cannot read a FIFO through the AHB alias, ever.** ERR-32 v3.0 § 3.8, p. 13 restates it: *"Software cannot use AHB addresses to read FIFO."*

#### `RTC-126` — RTC register read error after Light-sleep (both chips)

**Affects: ESP32 all revisions; ESP32-S3 v0.0, v0.1, v0.2. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.18, p. 19 and ERR-S3 v1.3 § 3.2, pp. 6–7 — identical text.

> *"If an RTC peripheral is turned off in Light-sleep mode, there is a certain probability that after waking up from Light-sleep, the CPU … will read the registers in the RTC power domain incorrectly."*
>
> **Workaround:** *"Users are suggested not to power down RTC peripherals in Light-sleep mode. **There will be no impact on power consumption.**"*

ERR-S3 adds: *"This issue has been bypassed in ESP-IDF v4.4 and above."* **[DOC]**

**[INF]** Free workaround — the errata explicitly says leaving RTC peripherals powered costs nothing in Light-sleep. Only matters if you are hand-managing power domains rather than using `esp_sleep_pd_config()`.

#### `WDT-3.15` — dual-core cache live lock (v3.0/v3.1 only)

**Affects: v3.0, v3.1 — i.e. *current* silicon and nothing older. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.19, p. 20.

> *"…when the following conditions are met at the same time, a live lock will occur, causing the CPUs to get stuck in the state of memory access and stop executing instructions.*
> *1. Dual-core system.*
> *2. Of the four Instruction/Data buses (IBUS/DBUS) that access external memory, three simultaneously initiate access requests to the same cache set, and all three requests result in cache misses."*

**Workaround [DOC]:** software must break the cache-line contention. Outside critical sections, ordinary interrupts do it automatically. Inside critical sections (where interrupts level ≤3 are masked), you must *"set up a high priority (level 4 or 5) interrupt for each core in advance, connect the interrupts to the same timer, and configure an appropriate timeout threshold."*

**[INF] This is the only ESP32 erratum that is *worse* on newer silicon.** Symptom: an interrupt watchdog panic with both cores apparently stuck, on a dual-core ESP32 running code from external flash/PSRAM. The IDF option that implements the workaround is `CONFIG_ESP32_ECO3_CACHE_LOCK_FIX`. **If you are on a v3.x dual-core ESP32 and see unexplained interrupt-WDT panics, check that this is enabled.** Note it is irrelevant on a single-core part.

#### `LEDC-3.12` — duty overflow in decremental fade

**Affects: all revisions. No fix scheduled.** **[DOC]** ERR-32 v3.0 § 3.32, p. 27.

*"When the LEDC is in decremental fade mode, a duty overflow error may occur."*

**[INF]** Symptom: an LED fading *down* momentarily jumps to full brightness near the end of the fade. Mitigation is to stop the fade slightly above zero and set duty 0 explicitly, or use the IDF fade API which handles the endpoint.

#### `TWAI-3.13.*` — eleven CAN conformance deviations

**Affects: all revisions. Almost all "no fix scheduled".** **[DOC]** ERR-32 v3.0 §§ 3.21–3.31, pp. 21–27.

The set (Espressif's own titles):

| ID | Deviation |
|---|---|
| TWAI-3.13.6 | After losing arbitration, a dominant bit on the 3rd bit of intermission is not interpreted as an SOF |
| **TWAI-3.13.3** | **Message transmitted after bus-off recovery is erroneous** |
| TWAI-3.13.7 | When the 8th bit of the error delimiter is dominant, the error-passive state is not entered |
| TWAI-3.13.2 | Error status bit is not frozen during bus-off recovery |
| TWAI-3.13.5 | Receiving an erroneous data frame can corrupt the data bytes of the *next* frame |
| TWAI-3.13.10 | A negative phase error where \|e\| > SJW(N) left-shifts the remaining transmitted bits |
| TWAI-3.13.1 | Receive Error Counter may change during reset mode or bus-off recovery |
| **TWAI-3.13.11** | **When the RX FIFO overruns with ≥64 messages, the RX FIFO becomes unrecoverable** |
| TWAI-3.13.8 | Suspend transmission is included even after losing arbitration |
| TWAI-3.13.9 | Stuff error during arbitration while transmitting does not increase the TEC |
| TWAI-3.13.4 | Reading the interrupt register may lose a transmit interrupt |

Only **TWAI-3.13.3** has a real workaround **[DOC]** ERR-32 v3.0 § 3.22, p. 22: *"Upon detecting the completion of bus-off recovery (via the error warning interrupt), the TWAI controller should enter then exit reset mode so that the controller's internal signals are reset."* Several others say plainly *"There is no workaround for this issue."*

**[INF] Practical reading:** ESP32's TWAI is fine on a well-behaved, lightly-loaded bus. It is **not** a part to choose for a safety-relevant or heavily-loaded CAN segment, nor one to submit for CAN conformance certification. The two that will actually be observed in the field are **TWAI-3.13.3** (garbage frame after bus-off — handle it) and **TWAI-3.13.11** (unrecoverable RX FIFO under burst load — size your polling accordingly).

---

### 🟢 Handled by ESP-IDF, or fixed in silicon you probably have

| ID | Affects | Status **[DOC]** |
|---|---|---|
| `CPU-3.5` CPU crashes on direct 240 → 80/160 MHz switch | **v0.0 only** | *"Fixed in chip revision v1.0."* ERR-32 § 3.1, p. 8 |
| `CPU-3.9` External SRAM store-then-load read/write errors | v1.0, v1.1 | *"automatically worked around when external SRAM use is enabled in ESP-IDF v3.0 and newer."* **Fixed in v3.0 silicon.** § 3.4, pp. 10–11 |
| `CPU-3.2` External SRAM through cache, pipelined access | **v0.0 only** | Fixed in v1.0. § 3.5, p. 11 |
| `CPU-3.10` Simultaneous dual-core reads of two address spaces | v0.0, v1.0, v1.1 | **Fixed in v3.0.** § 3.6, pp. 11–12 |
| `CPU-3.3` Repeated writes to one DPORT address may be lost | **v0.0 only** | Fixed in v1.0. Workaround = use the AHB alias; § 3.8 pp. 12–13 carries the full DPORT↔AHB address table |
| `GPIO-3.6` GPIO pull registers inert on RTC-capable pads | all | *"automatically worked around when using GPIO drivers in ESP-IDF v2.1 or newer."* § 3.10, p. 14 |
| `RES-3.4` Brown-out Reset does not work | **v0.0 only** | *"There is no workaround."* **Fixed in v1.0.** § 3.13, p. 16 |
| `RES-3.1` Spurious WDT reset on power-up / Deep-sleep wake | **v0.0 only** | Fixed in v1.0. § 3.14, p. 17 |
| `RES-3.8` Spurious WDT reset due to flash start-up time | v0.0, v1.0, v1.1 | Workaround: flash with <800 µs power-on-to-ready, or IDF ≥ v2.0 delay. **Fixed in v3.0.** § 3.15, pp. 17–18 |
| `CLK-3.7` Audio PLL frequency range limited (`sdm0`/`sdm1` unused) | **v0.0 only** | Fixed in v1.0. § 3.16, p. 18 |
| `UART-3.17` `fifo_cnt` decrements by 1 if the DPORT read is interrupted | all | Workaround: compute length from FIFO read/write offsets — code snippet at § 3.20, pp. 20–21 |

**[INF] Net effect for a v3.0/v3.1 ESP32:** the whole external-SRAM/PSRAM erratum family (`CPU-3.2`, `CPU-3.9`, `CPU-3.10`), the brown-out reset failure, both spurious-watchdog issues, and the audio-PLL limitation are **gone in silicon**. This is the strongest single argument for insisting on v3.x parts, and it is why the numbering-scheme change matters — see [esp32-u4wdh README § 21](../../components/espressif/esp32-u4wdh/README.md).

---

## 3. ESP32-S3 — eight errata, all revisions

**Revision landscape:** v0.0, v0.1, v0.2 — **all major revision 0**. **[DOC]** ERR-S3 v1.3 Table 2.1, p. 5.

**Every one of the eight affects all three revisions**, except `USBOTG-4289` which is *"fixed in some batches of chip revision v0.2"* (marked `Y*` = *"some batches of a revision are affected"*). **[DOC]**

**[INF] There is no S3 revision to upgrade to.** Unlike ESP32, where moving from v1.1 to v3.0 eliminated six errata, on S3 you work around everything in software on every part.

| ID | Class | Affects | Symptom |
|---|---|---|---|
| [ANALOG-160](#analog-160--the-one-that-destroys-the-chip) | 🔴 | all | **Permanent chip damage** in sleep with ULP/touch |
| [ADC-183](#adc-183--sar-adc2-has-no-working-dma-controller) | 🔴 | all | ADC2 has no DMA/continuous mode |
| [USBOTG-4289](#usbotg-4289--usb-otg-download-mode-fused-off-on-early-parts) | 🔴 | all (fixed in some v0.2 batches) | USB-OTG **download/flashing** unavailable |
| [LCD-239](#lcd-239--lcd-clock-divider-of-1-is-unreliable) | 🟠 | all | RGB/I8080 corruption at divider 1 |
| [RMT-176](#rmt-176--indeterminate-idle-level-after-continuous-tx) | 🟠 | all | Wrong idle level after continuous TX |
| [TOUCH-100](#touch-100--first-two-scan-done-interrupts-are-garbage) | 🟠 | all | First two touch scan results undefined |
| [CACHE-126](#cache-126--cache-hit-error-during-write-back) | 🟢 | all | Cache returns stale/lost data during write-back |
| [RTC-126](#rtc-126--rtc-register-read-error-after-light-sleep-both-chips) | 🟢 | all | Same as the ESP32 entry above |

---

### 🔴 Design-level

#### `ANALOG-160` — the one that destroys the chip

**Affects: v0.0, v0.1, v0.2. No fix scheduled.** **[DOC]** ERR-S3 v1.3 § 3.3, p. 7.

> *"If the analog power is configured as `BIAS_SLEEP = 0` and `PD_CUR = 1`, the chip will be **permanently damaged**. This issue might be triggered when ULP and/or touch sensor is used during Light-sleep or Deep-sleep."*
>
> *"Users are suggested to disable such analog power configuration in sleep mode through software. This issue has been bypassed by disabling the above configuration in ESP-IDF v4.4.2+, v5.0 and above."*

**[INF] The only erratum in either document whose failure mode is destroyed hardware.** Three consequences:

1. **Never run ULP or touch in sleep on an S3 with ESP-IDF older than v4.4.2.** Not "expect bugs" — expect dead parts.
2. If you write to RTC analog registers directly (bypassing IDF's power management), you can re-create the fatal configuration on *any* IDF version. Do not hand-poke `RTC_CNTL_BIAS_CONF_REG`.
3. It is a **minimum-toolchain-version constraint on the project**, which makes it a design decision, not a coding one. Pin `idf_version` accordingly.

#### `ADC-183` — SAR ADC2 has no working DMA controller

**Affects: v0.0, v0.1, v0.2. No fix scheduled.** **[DOC]** ERR-S3 v1.3 § 3.8, p. 10.

> *"The Digital Controller of SAR ADC2, i.e., DIG ADC2 controller, may receive a false sampling enable signal. In such a case, the controller will enter an inoperative state."*
>
> *"It is suggested to use RTC controller to control SAR ADC2."*

**The TRM says the same thing more bluntly** **[DOC]** TRM-S3 v1.8 § 39.3, p. 1466:

> *"The DIG ADC2 controller of ESP32-S3 doesn't work properly and related information has been deleted in this chapter."*

**[INF] Concretely: on ESP32-S3 only ADC1 supports continuous (DMA) mode.** ADC2's ten channels are usable **one-shot only**, via the RTC controller. This is a **pin-allocation decision**: if a signal needs continuous sampling — audio-rate analogue input, a current-sense loop, anything you would attach `adc_continuous_read()` to — it must land on an **ADC1** pin. Getting this wrong means re-spinning the board. See [soc-peripheral-reference.md § 10](soc-peripheral-reference.md#10-adc) for the ADC1/ADC2 channel split.

Note this is **less severe than on ESP32**, where ADC2 is unavailable *entirely* while Wi-Fi is active (TRM-32 v5.8 p. 741) — but the S3 restriction is permanent rather than conditional.

#### `USBOTG-4289` — USB-OTG download mode fused off on early parts

**Affects: v0.0, v0.1, and some batches of v0.2.** **[DOC]** ERR-S3 v1.3 § 3.5, p. 9.

> *"For ESP32-S3 series chips manufactured before the Date Code 2219 and series of modules and development boards with the PW Number before PW-2022-06-XXXX, the `EFUSE_DIS_USB_OTG_DOWNLOAD_MODE` (BLK0 B19[7]) bit of eFuse is set by default and cannot be modified. Therefore, the USB-OTG Download function is unavailable for these products."*
>
> **Workaround:** *"ESP32-S3 also supports downloading firmware through USB-Serial-JTAG."*
>
> **Solution:** *"For ESP32-S3 series chips manufactured on and after the Date Code 2219 and … PW Number of and after PW-2022-06-XXXX, the bit … will not be programmed by default and thus is open for users to program."*

**[INF] Affects your connector, not your code.** If the plan was "flash the product through its USB-OTG port in the factory", on early silicon that port cannot do it — you need the USB-Serial/JTAG pins brought out too, or a UART header. Identification is by **Date Code / PW Number**, not by revision number ([memory-and-boot.md § 7.4](memory-and-boot.md#74-additional-identification-date-code-and-pw-number)). **[INF]** Any S3 board purchased in 2026 is comfortably past Date Code 2219; this matters for old stock and for parts pulled from long-shelved inventory.

---

### 🟠 Code-level

#### `LCD-239` — LCD clock divider of 1 is unreliable

**Affects: v0.0, v0.1, v0.2. No fix scheduled.** **[DOC]** ERR-S3 v1.3 § 3.4, pp. 7–8.

Two distinct failures **[DOC]**:

1. **RGB format with `LCD_CAM_LCD_CLK_EQU_SYSCLK = 1`** (divider 1):
   - *"The pixel clock output (LCD_PCLK) will not be able to be set to falling edge trigger."*
   - *"When frames are continuously sent in this mode (i.e., `LCD_CAM_LCD_NEXT_FRAME_EN = 1`), it might occur that the second frame inserts the last data of the previous frame in the first frame."*
2. **I8080 format**: if the clock cycle count before data transmission is ≤ 2, *"it can result in incorrect value of the first data and the subsequent data quantity."* Espressif defines the calculation:
   - `total_pixels = VFK cycle length + CMD cycle length + DUMMY cycle length`
   - `cycle_unit = 1` if `LCD_CAM_LCD_CLK_EQU_SYSCLK = 1`, else `LCD_CAM_LCD_CLKCNT_N + 1`
   - `ahead_cycle = total_pixels × cycle_unit` — **must be > 2**

> **Workarounds [DOC]:** *"When using the RGB format, avoid configuring `LCD_CAM_LCD_CLK_EQU_SYSCLK` as 1. When using the I8080 format: try to avoid configuring `LCD_CAM_LCD_CLK_EQU_SYSCLK` as 1; ensure that `ahead_cycle` is larger than 2 if [it] has to be set as 1."*
>
> *"This issue has been bypassed through the methods described above in ESP-IDF v4.4.5+, v5.0.3+, v5.1 and above."*

**[INF]** Symptom on an RGB panel: a horizontal band of the previous frame's last row appearing at the top of the next frame, only at the highest pixel clock. **Do not chase the last increment of PCLK by setting the divider to 1.** This does *not* affect QSPI or SPI displays, which do not use the `LCD_CAM` peripheral — so it is **not** relevant to the ST77916 on the Knob board ([ST77916 README](../../components/sitronix/st77916/README.md)), which goes through `SPI2_HOST`.

#### `RMT-176` — indeterminate idle level after continuous TX

**Affects: v0.0, v0.1, v0.2. No fix scheduled.** **[DOC]** ERR-S3 v1.3 § 3.6, pp. 9–10.

> *"…if the continuous TX mode is enabled, it is expected that the data transmission stops after the data is sent for `RMT_TX_LOOP_NUM_CHn` rounds, and after that, the signal level in idle state should be controlled by the 'level' field of the end-marker. However, in real situation, after the data transmission stops, the channel's idle state signal level is not controlled by the 'level' field of the end-marker, but by the level in the data wrapped back, which is **indeterminate**."*
>
> **Workaround:** *"Users are suggested to set `RMT_IDLE_OUT_EN_CHn` to 1 to only use registers to control the idle level."*
>
> *"This issue has been bypassed since the first ESP-IDF version that supports continuous TX mode (v5.0)."*

**[INF]** Matters if you drive addressable LEDs (WS2812 etc.) in RMT loop mode: the data line can be left high, which some strips latch as a partial frame. IDF ≥ 5.0 sets the register-controlled idle level for you; a hand-written RMT driver must do it explicitly.

#### `TOUCH-100` — first two scan-done interrupts are garbage

**Affects: v0.0, v0.1, v0.2. No fix scheduled.** **[DOC]** ERR-S3 v1.3 § 3.7, p. 10.

> *"For ESP32-S3's touch sensor, the raw data value is undefined for the first two `TOUCH_SCAN_DONE_INT` interrupts."*
>
> **Workaround:** *"Users are suggested to skip the first two `TOUCH_SCAN_DONE_INT` interrupts, then turn them off and stop using them."*

**[INF]** Note the workaround is stronger than "discard two samples" — Espressif recommends **abandoning `TOUCH_SCAN_DONE_INT` entirely** after the first two. Use the threshold/active interrupts instead. A touch baseline calibrated on the first two scans will be wrong.

---

### 🟢 Handled

#### `CACHE-126` — cache hit error during write-back

**Affects: v0.0, v0.1, v0.2. No fix scheduled.** **[DOC]** ERR-S3 v1.3 § 3.1, p. 6.

> *"When a cache write-back is in progress, if the CPU accesses other addresses within the same cache line, the access request will be treated as a cache miss… resulting in two identical cache data entries in the same cache line. Due to hardware logic issues, the cache hit logic may select incorrect cache data, causing the CPU to return incorrect results. If the CPU also writes to the cache line, it may cause the data being written back to be lost."*

Two triggering scenarios named **[DOC]**: an **interrupt handler** touching the same cache line as an in-progress write-back, and **CPU1 accessing a line CPU0 is writing back**.

> **Workaround:** disable interrupts on the current CPU for the duration of the write-back, **and** enable the cache freeze feature to stop the other CPU. *"This issue has been automatically bypassed using the above methods in ESP-IDF v4.4.6+, v5.0.4+, v5.1.1+, v5.2, and above versions."*

**[INF]** Silent data corruption on a dual-core S3 using PSRAM — the worst kind of bug to debug from symptoms. **The only action is a toolchain floor: use ESP-IDF ≥ v5.1.1 (or the listed patch releases).** Combined with `ANALOG-160`'s v4.4.2+ requirement, the practical minimum for any S3 project touching PSRAM or sleep is **v5.1.1+**.

---

## 4. Conflicts and reconciliations found

| # | Finding |
|---|---|
| **1** | **`ADC-183` (errata) and TRM-S3 § 39.3 (TRM) agree, but say it very differently.** The errata frames DIG ADC2 as a bug with a workaround; the TRM says the controller *"doesn't work properly"* and has **deleted its register documentation**. **[INF]** The TRM's position is the operationally correct one — there is nothing to program. Do not look for DIG ADC2 registers in TRM v1.8; if you have the older **v1.2** mirror, it may still document them. **Do not use them.** |
| **2** | **`RTC-126` is shared verbatim between ESP32 and ESP32-S3** with the same ID and the same text (ERR-32 § 3.18 p. 19; ERR-S3 § 3.2 pp. 6–7), but only the S3 document states the ESP-IDF version that bypasses it (v4.4+). **[INF]** The bypass presumably applies to both; the ESP32 errata simply omits it. |
| **3** | **`WDT-3.15`'s title contains an unsubstituted template variable** — *"[WDT-3.15] {idf_target_name} Chip May Have A Live Lock…"* — in both the table of contents (p. i) and the summary table (p. 7) of **ERR-32 v3.0** **[DOC]**. A documentation-build defect, not a technical one, but it makes the entry hard to find by search. The body text (§ 3.19, p. 20) correctly says "ESP32". |
| **4** | **`CPU-3.18`'s table gives contradictory-looking entries for v1.0/v1.1** because the cells span revisions unevenly and `pdftotext` reflows them. **[INF]** Read § 3.18's table from the rendered PDF page 8, not from extracted text; the three underlying errata (`CPU-3.3`, `CPU-3.10`, `CPU-3.16`) are individually unambiguous and are what you should actually consult. |
| **5** | **Datasheet vs TRM on ESP32-S3 boot mode** — DS-S3 v2.2 names two boot-mode pins, TRM-S3 v1.8 names four. Not an errata issue but the same class of hazard; documented in [memory-and-boot.md § 2.2](memory-and-boot.md#22-boot-mode-selection). |
| **6** | **No conflict found between any errata and the corresponding TRM/datasheet peripheral counts.** Every count in [soc-peripheral-reference.md](soc-peripheral-reference.md) survives the errata unchanged — the errata affect *behaviour*, never *instance counts*. |

---

## 5. Practical checklists

### Starting an ESP32 design **[INF]**

- [ ] Specify **v3.0 or v3.1 silicon** in the BOM. Six errata disappear.
- [ ] Do **not** put digital edge-sensitive inputs on **GPIO36 / GPIO39** if the ADC is used (`GPIO-3.11`).
- [ ] Decide **EXT0 wake *or* ULP/touch** before layout (`ULP-3.19`). If both are needed, use EXT1.
- [ ] Plan on **level-triggered** GPIO interrupts throughout (`GPIO-3.14`).
- [ ] Wi-Fi **and** Ethernet? Budget an **external 50 MHz oscillator** (`CLK-3.22`).
- [ ] Dual-core + external flash/PSRAM? Enable `CONFIG_ESP32_ECO3_CACHE_LOCK_FIX` (`WDT-3.15`).
- [ ] Leave **MTDI/GPIO12** alone, or burn the VDD_SDIO eFuses first — [memory-and-boot.md § 5.1](memory-and-boot.md#51-esp32-vdd_sdio-mtdi-and-the-18-v-trap).
- [ ] Any hand-written register access: **`volatile`, always** (`CPU-3.16`).
- [ ] Any hand-written UART/I2S FIFO read: **bracket with interrupt disable** (`CPU-3.21`).

### Starting an ESP32-S3 design **[INF]**

- [ ] Pin **ESP-IDF ≥ v5.1.1** (or v4.4.6 / v5.0.4). Below that you risk **permanent chip damage** (`ANALOG-160`) and **silent cache corruption** (`CACHE-126`).
- [ ] Any signal needing **continuous/DMA ADC** must be on an **ADC1** pin (`ADC-183`).
- [ ] Factory-flashing over USB-OTG? Verify **Date Code ≥ 2219** or bring out USB-Serial/JTAG (`USBOTG-4289`).
- [ ] RGB or I8080 panel: **never set the LCD clock divider to 1** (`LCD-239`).
- [ ] RMT continuous/loop TX: set the idle level from registers (`RMT-176`) — free on IDF ≥ 5.0.
- [ ] Touch sensing: **do not use `TOUCH_SCAN_DONE_INT`** (`TOUCH-100`).
- [ ] Cap **LEDC duty resolution at 14 bits** — not an erratum, a silicon limit; see [soc-peripheral-reference.md § 4](soc-peripheral-reference.md#4-ledc--led-pwm-controller).

---

## 6. Extraction notes

Both errata PDFs have **clean text layers** and extract fully with `pdftotext -layout`. Unlike the TRMs, they are short enough to read end to end and every erratum body was read in full rather than sampled.

Two extraction caveats:

1. **Multi-revision "Affected Revisions" tables reflow badly.** The `Y`/blank grids in ERR-32 Tables 2.1/2.2 and the `CPU-3.18` address-space table lose their column alignment in the text layer. Every revision attribution in this page was **re-checked against the per-erratum "Affected revisions:" line** in § 3, which is plain text and unambiguous.
2. **Figures 1.1–1.3 (chip marking, module marking, product label diagrams) do not extract** — they are images. The *tables* that go with them (1.2, 1.3) do, and are reproduced in [memory-and-boot.md § 7](memory-and-boot.md#7-efuse-and-chip-revision-detection). If you need to physically read a part's marking, open the PDF to those figures.

---

## Related

- [SoC peripheral reference](soc-peripheral-reference.md) — peripheral counts, with the ADC and LEDC limits that interact with these errata
- [Memory and boot](memory-and-boot.md) — chip-revision eFuse decoding, strapping, VDD_SDIO/VDD_SPI voltage hazards
- [ESP-IDF peripheral capabilities](esp-idf-peripheral-capabilities.md)
- [esp32-u4wdh README § 21](../../components/espressif/esp32-u4wdh/README.md) — the ESP32 v3.0/v3.1 revision story in depth, incl. the AES fault-injection advisory
- [esp32-s3r8 README](../../components/espressif/esp32-s3r8/README.md)
- [esp32-p4 README § 10](../../components/espressif/esp32-p4/README.md#10-errata-summary) — ESP32-P4 errata
