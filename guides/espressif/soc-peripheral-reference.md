# Espressif SoC peripheral reference — ESP32 vs ESP32-S3 vs ESP32-P4

- **Purpose:** the authoritative, *numeric* cross-target peripheral table for the three Espressif SoCs in this knowledge base, extracted from the **Technical Reference Manuals and datasheets held locally**.
- **Extracted:** 2026-08-24
- **Why this page exists:** the ESP-IDF Programming Guide renders peripheral counts *symbolically* (`SOC_PCNT_UNITS_PER_GROUP`, `SOC_LEDC_TIMER_BIT_WIDTH`, …) and explicitly defers to the TRM. That finding is recorded in [esp-idf-peripheral-capabilities.md § 1](esp-idf-peripheral-capabilities.md#1--read-this-before-using-this-page-for-peripheral-counts). **This page is where the deferral lands.**

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Quoted or read directly from the cited Espressif PDF, at the cited printed page |
| **[INF]** | Inference or synthesis by this knowledge base, not stated as such by Espressif |

## Sources

All page numbers below are **printed page numbers** (the number in the page footer), which is what a PDF viewer's "go to page" will land on for these documents.

| Key | Document | Version | Pages | Local artifact |
|---|---|---|---:|---|
| **TRM-32** | ESP32 Technical Reference Manual | **v5.8** | 784 | [`esp32-technical-reference-manual.pdf`](../../components/espressif/esp32-u4wdh/artifacts/esp32-technical-reference-manual.pdf) |
| **DS-32** | ESP32 Series Datasheet | **v5.3** | 78 | [`esp32-datasheet.pdf`](../../components/espressif/esp32-u4wdh/artifacts/esp32-datasheet.pdf) |
| **TRM-S3** | ESP32-S3 Technical Reference Manual | **v1.8** | 1531 | [`esp32-s3-technical-reference-manual.pdf`](../../components/espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual.pdf) |
| **DS-S3** | ESP32-S3 Series Datasheet | **v2.2** | 87 | [`esp32-s3-datasheet.pdf`](../../components/espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf) |
| **TRM-P4** | ESP32-P4 Technical Reference Manual | **Pre-release v0.7**, marked `PRELIMINARY` on every page | 3701 | [`esp32-p4-technical-reference-manual.pdf`](../../components/espressif/esp32-p4/artifacts/esp32-p4-technical-reference-manual.pdf) |
| **DS-P4** | ESP32-P4 Series Datasheet | **Pre-release v0.7** | 102 | [`esp32-p4-datasheet.pdf`](../../components/espressif/esp32-p4/artifacts/esp32-p4-datasheet.pdf) |

Older revisions are also held (ESP32 TRM v5.4 / DS v4.9, ESP32-S3 TRM v1.2 / DS v1.6, all Waveshare mirrors) — see [§ 14](#14-revision-differences-observed).

> ⚠ **Everything in the ESP32-P4 columns is pre-release.** The TRM and datasheet are both v0.7 and the TRM is stamped `PRELIMINARY`. Treat P4 numbers as subject to change and re-verify against a released revision when one exists. See [esp32-p4 README § 11](../../components/espressif/esp32-p4/README.md#11-documentation-maturity-and-what-that-costs-you).

**Regenerate any extract below with:**

~~~bash
nix-shell -p poppler-utils --run \
  'pdftotext -layout -f <page> -l <page> <artifact>.pdf -'
~~~

The text layer of all six documents is clean — see [§ 15](#15-extraction-notes-and-text-layer-quality).

---

## 1. The one-page answer

| Peripheral | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| **PCNT** | **8** units × 2 ch, 16-bit signed | **4** units × 2 ch, 16-bit signed | **4** units × 2 ch, 16-bit signed |
| **RMT** | **8** channels, each TX *or* RX; 512×32-bit shared RAM | **4 TX + 4 RX** (fixed); 384×32-bit shared RAM | **4 TX + 4 RX** (fixed); 384×32-bit shared RAM |
| **LEDC** | **16** channels in **2 speed modes**, 4+4 timers, 20-bit counter | **8** channels, **1 speed mode**, 4 timers, **14-bit** counter | **8** channels, **1 speed mode**, 4 timers, 20-bit counter |
| **I2S** | **2** (I2S0, I2S1); PDM on **I2S0 only**; no TDM | **2** (I2S0, I2S1); TDM ≤16 ch; PDM↔PCM on **I2S0 only** | **3** + **1 LP I2S**; TDM ≤16 ch; PDM↔PCM on **I2S0 only** |
| **Timer groups** | 2 groups × 2 timers, **64-bit** | 2 groups × 2 timers, **54-bit** | 2 groups × 2 timers, **54-bit** |
| **General-purpose SPI** | SPI2, SPI3 (SPI0/1 = memory) | SPI2, SPI3 (SPI0/1 = memory) | GP-SPI2, GP-SPI3, + **LP-SPI** |
| **I2C** | 2 | 2 | 2 + **1 LP I2C** (master only) |
| **UART** | 3 | 3 | 5 + **1 LP UART** |
| **ADC** | 2 × 12-bit SAR, 18 ch | 2 × 12-bit SAR, 20 ch | 2 × 12-bit SAR |
| **GPIO** | **34**, 6 input-only | **45**, none input-only | **55**, none input-only |
| **DMA** | 2 shared SPI/I2S DMA channels | **GDMA: 5 TX + 5 RX** | **GDMA-AHB 3+3, GDMA-AXI 3+3**, plus VDMA / 2D-DMA |
| **USB** | **none** | 1 × FS OTG + USB Serial/JTAG | 1 × **HS** OTG + 1 × FS OTG + USB Serial/JTAG |
| **TWAI (CAN)** | 1 | 1 | **3** |
| **Display / camera** | **none** — parallel LCD + DVP are *modes of I2S* | **`LCD_CAM`**: i80/MOTO6800/RGB, **8/16-bit**; DVP 8/16-bit | **`LCD_CAM`** 8/16/**24**-bit + **MIPI-DSI 2-lane** + **MIPI-CSI 2-lane** + ISP |
| **Image acceleration** | — | — | **PPA**, **2D-DMA**, **JPEG codec**, **H.264 encoder** |

Everything below gives the citation and the detail behind each cell. The display and camera rows are expanded in **[§ 16](#16-lcd-camera-and-display-peripherals)**.

---

## 2. PCNT — pulse counter

**This is the row people most often get wrong: ESP32 has *eight* units, S3 and P4 have *four*.**

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Units | **8** (`PULSE_CNT_U0…U7`) | **4** (`n` = 0…3) | **4** (`n` = 0…3) |
| Channels per unit | **2** (`ch0`, `ch1`), functionally identical, sharing one counter | **2** | **2** |
| Counter | **16-bit signed** up/down | 16-bit, "count from 1 to 65535" | **16-bit signed** |
| Clock | APB_CLK | APB_CLK (the *only* clock in PCNT) | APB_CLK |
| Max input pulse frequency | **40 MHz** | not stated in the feature list | **f<sub>APB_CLK</sub> / 2** |
| Glitch filter | per-channel, on both signal and control inputs | yes | yes |
| Per-channel controls | `POS_MODE`/`NEG_MODE` (edge action) modified by `LCTRL_MODE`/`HCTRL_MODE` (control-signal level) | same model | same model |

**Citations [DOC]:**

- ESP32: TRM-32 v5.8 **Ch. 23 § 23.1, p. 450** — *"The pulse counter has eight independent units, referred to as PULSE_CNT_Un."* and *"The maximum frequency of pulses supported by ESP32's pulse counter is 40 MHz."* Architecture and 16-bit signed up/down counter: **§ 23.2.1, p. 451**. Register block `PCNT_U0…U7_CONF0/1/2_REG` at `0x3FF57000`+: **§ 23.4, p. 456**.
- ESP32-S3: TRM-S3 v1.8 **Ch. 38, p. 1439** — *"The PCNT has four independent pulse counters called units… There is only one clock in PCNT, which is APB_CLK. In this chapter, n denotes the number of a unit from 0 ~ 3."* Features **§ 38.1, p. 1440**: *"Four independent pulse counters (units) that count from 1 to 65535"*, *"Each unit consists of two independent channels sharing one pulse counter"*. Register summary confirms only `PCNT_U0…U3`: **p. 1445**.
- ESP32-P4: TRM-P4 v0.7 **Ch. 51 § 51.1, p. 3141** — *"PCNT has four independent pulse counters called units… Each unit includes two channels (ch0 and ch1) and a 16-bit signed counter."* Feature list **§ 51.2, p. 3142**, including *"Maximum frequency of pulses: f<sub>APB_CLK</sub>/2"*. Also DS-P4 v0.7 § 4.2.2.8.

**How you get them in code [INF]:** the ESP-IDF `pcnt` driver allocates units from this pool and returns an error when exhausted — see [esp-idf-peripheral-capabilities.md § 1](esp-idf-peripheral-capabilities.md#1--read-this-before-using-this-page-for-peripheral-counts) for the guide's own wording. On S3/P4 you have **4 units × 2 channels = 8 quadrature-decodable inputs at most**; on ESP32 you have 16.

---

## 3. RMT — remote control / arbitrary pulse train

**The important difference is not the channel count — all three have eight — but whether a channel can be *either* direction.**

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Channels | 8 | 8 | 8 |
| TX/RX split | **Any channel can TX or RX** (each channel has both a transmitter and a receiver; only one active at a time) | **Fixed: ch0–3 TX only, ch4–7 RX only** | **Fixed: ch0–3 TX only, ch4–7 RX only** |
| Shared RAM | **512 × 32-bit** (64 words/channel), base `0x3FF56800` | **384 × 32-bit** (48 words/channel) | **384 × 32-bit** (48 words/channel) |
| Multi-block per channel | `RMT_MEM_SIZE_CHn > 1` borrows the *following* channels' blocks; those channels become unusable | same, `RMT_MEM_SIZE_CHn ≤ (8 − n)` | same |
| DMA | no | **TX on ch3, RX on ch7 only** | **GDMA: TX on ch3, RX on ch7 only** |
| Wrap TX / Wrap RX | not offered as a named feature | yes | yes |
| Continuous TX | yes (`RMT_REG_TX_CONTI_MODE`) | yes | yes |
| Simultaneous multi-channel TX | not offered | yes (`RMT_TX_SIM_CHn`) | yes |
| Carrier modulation / RX demodulation + filter | yes | yes | yes |
| RAM power-down | `RMT_MEM_PD` | `RMT_MEM_FORCE_PD` | yes |

**Citations [DOC]:**

- ESP32: TRM-32 v5.8 **Ch. 30 § 30.2.1, p. 727** — *"The RMT module contains eight channels. Each channel has both a transmitter and a receiver, but only one of them can be active in every channel. The eight channels share a 512x32-bit RAM block."* RAM base and `end_addr_chn` formula: **§ 30.2.2, pp. 727–728**.
- ESP32-S3: TRM-S3 v1.8 **§ 37.1, p. 1414** — *"Channel 0 ~ 3 (TX channel) are dedicated to sending signals. Channel 4 ~ 7 (RX channel) are dedicated to receiving signals."* Feature list **§ 37.2, p. 1415**: *"Four TX channels / Four RX channels / … / Eight channels share a 384 x 32-bit RAM / … / DMA access for TX mode on channel 3 / DMA access for RX mode on channel 7."* `RMT_MEM_SIZE` borrowing rule: **§ 37.3, p. 1417**. Same list is repeated verbatim in DS-S3 v2.2 § 4.2.1.11, p. 55.
- ESP32-P4: TRM-P4 v0.7 **§ 60.1, p. 3509** and **§ 60.2, pp. 3510–3511** — identical structure, *"Eight channels: TX channels 0 ~ 3 / RX channels 4 ~ 7 / Eight channels share a 384 x 32-bit RAM"*, GDMA on TX ch3 and RX ch7. Also DS-P4 v0.7 § 4.2.2.17.

**Practical consequence [INF]:** an ESP32-S3 or ESP32-P4 design that wants **more than four simultaneous RMT transmit channels** (e.g. driving five independent WS2812 strings) cannot do it in RMT alone — the RX half of the block is not repurposable. On ESP32 it can. On S3/P4, the usual escape is the SPI or I2S/LCD peripheral, or the PARLIO controller on P4.

**Memory budget [INF]:** 48 words/channel on S3/P4 versus 64 on ESP32 means the default single-block RMT symbol buffer is *smaller* on the newer parts. If you are porting ESP32 RMT code that relied on 64-symbol blocks, either raise `mem_block_symbols` (borrowing neighbours) or enable wrap mode.

---

## 4. LEDC — LED PWM controller

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Channels (PWM generators) | **16** | **8** | **8** |
| Speed modes | **2** — high-speed and low-speed, 8 channels each | **1** (low-speed only) | **1** (low-speed only) |
| Timers | **8** total: 4 high-speed (`h_timer0…3`) + 4 low-speed (`l_timer0…3`) | **4** (`Timer0…3`) | **4** (`Timer0…3`) |
| Max duty resolution (counter width) | **20 bits** | **14 bits** | **20 bits** |
| Duty dithering | yes — effectively raises resolution to **25 bits** | not listed | yes |
| Fractional clock divider | `LEDC_CLK_DIV = A + B/256`, A 10-bit, B 8-bit | same form | same form |
| Automatic duty fading | yes | yes, with fade-complete interrupt | yes, plus **up to 16 duty ranges per generator** for gamma curves |
| Output during Light-sleep | (high-speed channels update duty in hardware) | yes | yes |
| Phase adjustment | — | yes | yes |
| ETM events/tasks | — | — | yes |

**The frequency ↔ resolution tradeoff.** Resolution and output frequency are two ends of the same counter:

$$f_{\text{sig\_out}} = \frac{f_{\text{LEDC\_CLK}}}{\text{LEDC\_CLK\_DIV} \times 2^{\text{DUTY\_RES}}}$$

so

$$\text{DUTY\_RES} = \log_2\!\left(\frac{f_{\text{LEDC\_CLK}}}{f_{\text{sig\_out}} \times \text{LEDC\_CLK\_DIV}}\right)$$

Espressif tabulates the common cases for ESP32 — TRM-32 v5.8 **Table 28.2-1, p. 631** **[DOC]**:

| LEDC_CLKx | PWM frequency | Highest resolution (bit)¹ | Lowest resolution (bit)² |
|---|---|---:|---:|
| APB_CLK (80 MHz) | 1 kHz | 16 | 7 |
| APB_CLK (80 MHz) | 5 kHz | 13 | 4 |
| APB_CLK (80 MHz) | 10 kHz | 12 | 3 |
| REF_TICK (1 MHz) | 1 kHz | 9 | 1 |

> ¹ *"The highest resolution is calculated when the clock divisor LEDC_CLK_DIVx is 1 and rounded down. If the highest resolution calculated by the formula is higher than the counter's width **20 bits**, then the highest resolution should be 20 bits."*
> ² *"The lowest resolution is calculated when the clock divisor LEDC_CLK_DIVx is 1023 + 255 and rounded up."*
> — TRM-32 v5.8 p. 631 **[DOC]**

**Dithering:** TRM-32 v5.8 **p. 632** **[DOC]** — when a fractional duty is configured the controller lengthens occasional pulses by one cycle, *"effectively increas[ing] the resolution of the PWM generator to 25 bits"* (at the cost of period-to-period jitter).

**⚠ The S3 is the outlier: 14 bits, not 20.** TRM-S3 v1.8 **§ 35.2, p. 1310** **[DOC]** — *"Maximum PWM resolution: 14 bits"*, confirmed at **§ 35.3, p. 1313**: *"The `LEDC_TIMERx_DUTY_RES` field configures the overflow value of this 14-bit counter. Hence, the maximum resolution of the PWM signal is 14 bits."* **[INF]** Porting ESP32 code that asks for `LEDC_TIMER_16_BIT` or `LEDC_TIMER_20_BIT` to an S3 will fail at `ledc_timer_config()`. Cap at 14.

**Other citations [DOC]:**

- ESP32 16 channels / 2 speed modes / 4+4 timers: TRM-32 v5.8 **§ 28.1, p. 629** — *"It has 16 channels which can generate independent waveforms… The LED_PWM controller has eight high-speed and eight low-speed PWM generators… These channels can be driven from four timers."* DS-32 v5.3 § 4.8.8, p. 39 states *"Sixteen independent PWM generators / Maximum PWM duty cycle resolution of 20 bits / Eight independent timers with 20-bit counters."*
- ESP32-S3 8 channels / 4 timers: TRM-S3 v1.8 **§ 35.2, p. 1310**. DS-S3 v2.2 § "Peripherals" p. 4 says *"LED PWM controller, up to 8 channels"*.
- ESP32-P4 8 channels / 20 bits / 16 gamma ranges: TRM-P4 v0.7 **§ 58.2, p. 3398**; DS-P4 v0.7 § 4.2.2.15.

**The high-speed mode is ESP32-only and is a real capability, not a label** **[INF]**: on ESP32, high-speed channels apply duty and fade changes in hardware at the next period boundary, so a duty write is glitch-free without software timing. On S3/P4 all channels are "low speed" and duty updates need the `LEDC_*_DUTY_START` handshake.

---

## 5. I2S — audio and generic serial

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Instances | **2** — I2S0, I2S1 | **2** — I2S0, I2S1 | **3** (HP) + **1 LP I2S** |
| Per-instance structure | independent Tx and Rx unit, each with its own DMA channel | independent TX and RX unit, 64×32-bit TX FIFO, 64×32-bit RX FIFO, GDMA | independent TX and RX unit, GDMA |
| Standard modes | "multiple digital audio standards" (Philips / MSB / PCM); **no TDM** | **TDM Philips, TDM MSB-alignment, TDM PCM**, up to **16 channels** each way | same, up to **16 channels** each way |
| **PDM TX** | ✅ but **I2S0 only** | ✅ (raw); **PCM→PDM conversion I2S0 only** | ✅ (raw); **PCM→PDM conversion I2S0 only**, ≤2 ch |
| **PDM RX** | ✅ but **I2S0 only** | ✅ (raw); **PDM→PCM conversion I2S0 only** | ✅ (raw); **PDM→PCM conversion I2S0 only**, ≤8 ch |
| Data width | — | 8/16/24/32-bit | 8/16/24/32-bit |
| Sample rates called out | — | 8, 16, 32, 44.1, 48, 88.2, 96, 128, 192 kHz (192 kHz **not** in 32-bit slave mode) | high-precision divider; APLL up to **125 MHz** |
| Precision clock source | APLL_CLK (recommended for audio; PLL_F160M decimal division "not recommended") | APLL | APLL ≤125 MHz |
| A-law / µ-law | embedded compression/decompression module | yes, per direction | yes |
| LCD / camera mode | **yes — I2S doubles as the parallel LCD/camera controller**, incl. on-chip DAC/ADC modes | no — split out into the dedicated `LCD_CAM` peripheral | no — dedicated LCD/CAM + MIPI DSI/CSI |
| Extras | — | — | Synchronous counter in TX; ETM; **VAD** on LP I2S |

**Citations [DOC]:**

- ESP32: TRM-32 v5.8 **§ 22.1, p. 400** — *"The ESP32 includes two I2S interfaces: I2S0 and I2S1."* Feature list **§ 22.2, p. 401**: I2S mode features incl. *"Supports PDM signal input and output"*, then a separate **LCD mode** block (*"Supports multiple LCD modes, including external LCD / Supports external Camera / Supports on-chip DAC/ADC modes"*). **PDM is I2S0-only**: **§ 22.4.7, p. 424** — *"ESP32 I2S0 allows for pulse density modulation (PDM), which enables fast conversion between pulse code modulation (PCM) and PDM signals."* Clock source note (APLL for high-quality audio): **§ 22.3, p. 401**.
- ESP32-S3: TRM-S3 v1.8 **§ 28.1, p. 1038** — *"ESP32-S3 has two built-in I2S interfaces (i.e., I2S0 and I2S1)."* Terminology table **pp. 1038–1039** defines TDM RX/TX, PDM RX/TX and marks **PCM-to-PDM TX mode (for I2S0 only)** and **PDM-to-PCM RX mode (for I2S0 only)**. Feature list **§ 28.3, p. 1039** (standards, modes, sample rates, 8/16/24/32-bit). FIFO sizes **§ 28.4, pp. 1040–1041**. TDM ≤16 channels: **pp. 1044, 1046**.
- ESP32-P4: TRM-P4 v0.7 **§ 49.3, pp. 3071–3072** — full feature list including *"PCM-to-PDM data format conversion (for I2S0 only), up to 2 channels supported"* and *"PDM-to-PCM data format conversion (for I2S0 only), up to 8 channels supported"*, *"Configurable APLL clock with frequencies up to 125 MHz"*. Instance count: DS-P4 v0.7 § 4.2.2.6, p. 60 — *"ESP32-P4 has three built-in I2S interfaces"*; LP I2S at § 4.2.2.7 (RX only, ≤2 TDM channels, feeds VAD).

**Which support PDM RX — the short answer [INF]:** *all three* do, but on every one of them the **PDM↔PCM conversion hardware lives only on I2S0**. If you are hanging a PDM MEMS microphone off the part, budget I2S0 for it and put your DAC/codec on I2S1 (or I2S1/I2S2 on P4). On the ESP32-S3-Knob board this is exactly why the PCM5100A sits where it does — see [PCM5100A](../../components/texas-instruments/pcm5100a/README.md).

**⚠ ESP32-only trap [INF]:** because ESP32's I2S *is* the parallel LCD/camera controller, using an 8080 or DVP parallel display consumes an entire I2S instance. On S3/P4 the `LCD_CAM` peripheral is separate and I2S stays free.

The display side of that row — bus widths, pixel-clock ceilings, colour formats, MIPI — is **[§ 16](#16-lcd-camera-and-display-peripherals)**.

---

## 6. Timers and watchdogs

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Timer groups | **2** (TIMG0, TIMG1) | **2** | **2** (TIMGn, n = 0,1) |
| General-purpose timers per group | **2** (`TIMGn_Tx`, x = 0,1) | **2** | **2** |
| **Total GP timers** | **4** | **4** | **4** |
| Counter width | **64-bit** | **54-bit** | **54-bit** |
| Prescaler | 16-bit, ÷2 … ÷65536 | 16-bit, ÷2 … ÷65536 | 16-bit, ÷2 … ÷65536 |
| Up/down counting | yes | yes | yes |
| Auto-reload + software instant reload | yes | yes | yes |
| Interrupt type | **level and edge** | **level** | level |
| Clock source | APB_CLK (typ. 80 MHz) | selectable | **PLL_F80M_CLK / XTAL_CLK / RC_FAST_CLK** |
| Main System Watchdog (MWDT) | 1 per group (2 total) | 1 per group (2 total) | 1 per group (2 total), 32-bit |
| RTC watchdog | RWDT | RWDT | RWDT, 32-bit |
| Super watchdog | — | Super WDT | analog Super WDT (SWD) |
| XTAL32K watchdog | — | XTWDT (own chapter) | — |
| System timer | — | **52-bit** system timer | **two 52-bit** HP system timers |
| RTC / LP timer | 1 RTC timer | — | 48-bit LP general-purpose timer |

**Citations [DOC]:**

- ESP32: TRM-32 v5.8 **§ 10.1, p. 223** — *"There are four general-purpose timers embedded in the ESP32. They are all 64-bit generic timers based on 16-bit prescalers and 64-bit auto-reload-capable up/downcounters. The ESP32 contains two timer modules, each containing two timers."* Feature bullets incl. *"Level and edge interrupt generation"*. Prescaler quirk **§ 10.2.1, p. 223**: `TIMGn_Tx_DIVIDER` of 1 **or** 2 both give ÷2; 0 gives ÷65536. DS-32 v5.3 "Features" p. 3: *"Two timer groups, including 2 × 64-bit timers and 1 × main watchdog in each group / One RTC timer / RTC watchdog."*
- ESP32-S3: TRM-S3 v1.8 **§ 12.1, p. 654** — *"contains two timer groups… Each timer group consists of two general purpose timers referred to as Tx… and one Main System Watchdog Timer. All general purpose timers are based on 16-bit prescalers and 54-bit auto-reload-capable up-down counters."* Note that only *level* interrupt generation is listed. DS-S3 v2.2 "Features" p. 4: *"Four 54-bit general-purpose timers / 52-bit system timer / Three watchdog timers."*
- ESP32-P4: TRM-P4 v0.7 **§ 17.1–17.2, p. 1532** — two groups × (two GP timers + one MWDT), 54-bit counter, *"Three clock sources: PLL_F80M_CLK or XTAL_CLK or RC_FAST_CLK"*. DS-P4 v0.7 "Features" p. 4: *"Two 52-bit HP system timers / Four 54-bit HP general-purpose timers / Two 32-bit HP watchdog timers (MWDT) / 32-bit LP watchdog timer (RWDT) / Analog super watchdog timer (SWD) / 48-bit LP general-purpose timer (RTC Timer)."*

> **[INF]** "Three watchdog timers" on S3 = 2 × MWDT (one per timer group) + RWDT; the Super WDT and XTWDT are counted separately in the TRM's chapter list. The practical set you interact with from ESP-IDF is: task WDT and interrupt WDT (software, built on MWDT) plus RWDT for brown-out/boot recovery.

---

## 7. SPI

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Controllers | **4**: SPI0, SPI1, SPI2 (HSPI), SPI3 (VSPI) | **4**: SPI0, SPI1, SPI2, SPI3 | MSPI (2 sub-controllers) + GP-SPI2 + GP-SPI3 + **LP-SPI** |
| Reserved for memory | SPI0 (cache buffer). SPI1 = master, used by CPU for flash | **SPI0** (GDMA + cache → flash/PSRAM), **SPI1** (CPU → flash/PSRAM) | MSPI |
| **General purpose** | **SPI2, SPI3** (master or slave) | **SPI2, SPI3** | **GP-SPI2, GP-SPI3** (+ LP-SPI) |
| Max master clock | **80 MHz** (GP-SPI) | **80 MHz** full- and half-duplex; 8-line half-duplex DDR up to 40 MHz | **80 MHz**; LP-SPI 40 MHz |
| Max slave clock | — | **60 MHz** | **60 MHz**; LP-SPI 40 MHz |
| Line widths | 1/2/4 (four-line full/half-duplex, three-line half-duplex) | **1/2/4/8** master, 1/2/4 slave — *SPI2 only for 8-line*; SPI3 is 1/2/4 | 1/2/4/8 GP-SPI2; LP-SPI **1-bit only** |
| QSPI / OPI / QPI | Quad on memory bus | **Single/Dual/Quad/Octal/QPI/OPI** on SPI0/1 and SPI2 | Single/Dual/Quad/QPI on external memory bus |
| CS lines (master) | — | **SPI2: 6**, **SPI3: 3** | multiple; LP-SPI **CS0 only** |
| Pin routing | GPIO matrix or IO MUX | **SPI2: IO MUX *or* GPIO matrix. SPI3: GPIO matrix only** | — |
| DMA | 2 DMA channels shared by SPI1/2/3 | GDMA channel per controller | GDMA |
| Segmented DMA transfer | — | **SPI2 only** (`CONF` state unused on SPI3) | — |

**Citations [DOC]:**

- ESP32: DS-32 v5.3 **§ 4.8.2, p. 34** — *"ESP32 integrates four SPI controllers… Controller SPI0 is used as a buffer for accessing external memory. Controller SPI1 can be used as a master. Controllers SPI2 and SPI3 can be configured as either a master or a slave. SPI1, SPI2, and SPI3 use signal buses prefixed with SPI, HSPI, and VSPI."* DMA sharing: TRM-32 v5.8 **§ 20.2, p. 354** — *"Controllers SPI1~SPI3 share two DMA channels."*
- ESP32-S3: DS-S3 v2.2 **§ 4.2.1.5, pp. 53–54** — role split for SPI0/1/2/3 and the full clock table quoted above (*"2-line full-duplex communication with clock frequency up to 80 MHz"*, *"As a slave … up to 60 MHz"*, *"Provides six SPI_CS pins"*, *"Configurable clock frequency with a maximum of 120 MHz for 8-line SPI SDR/DDR modes"* for SPI0/1). GP-SPI2 vs GP-SPI3 differences: TRM-S3 v1.8 **§ 30.9, p. 1148** — the four bullets on data width, segmented DMA, IO MUX availability and CS count, plus **Table 30.9-1** listing registers invalid on SPI3.
- ESP32-P4: DS-P4 v0.7 **§ 4.2.2.2, pp. 57–59** — controller list and *"Master: up to 80 MHz / Slave: up to 60 MHz"* for GP-SPI, *"Master: up to 40 MHz / Slave: up to 40 MHz"*, *"1-bit SPI data mode"*, *"One CS line as master: CS0"* and the slave wake-up feature for LP-SPI. External-memory bus max 120 MHz: DS-P4 § 4.1.3.1, p. 46.

**Choosing a host [INF]:** on ESP32-S3, **prefer `SPI2_HOST` for anything demanding**. It is the only one that can use IO MUX pins (bypassing the GPIO-matrix's ~1-cycle input delay, which is what limits you to lower clocks on matrix-routed pins), the only one with 8-line/octal support, the only one with segmented DMA, and it has six CS lines rather than three. This is why the vendor QSPI display example on the Knob board uses `SPI2_HOST` — see [ST77916 § 4](../../components/sitronix/st77916/README.md#4-exact-wiring-on-this-board).

---

## 8. I2C

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Controllers ("ports") | **2** | **2** | **2 (HP)** + **1 LP I2C (master only)** + analog I2C + I3C master/slave |
| Master and slave | both | both | HP: both. **LP I2C: master only** |
| Standard mode | 100 kbit/s | 100 kbit/s | 100 kbit/s |
| Fast mode | 400 kbit/s | 400 kbit/s | 400 kbit/s |
| Above fast mode | not stated in TRM feature list | **"Up to 800 kbit/s (constrained by SCL and SDA pull-up strength)"** | not stated |
| Addressing | 7-bit and 10-bit | 7-bit and 10-bit | 7-bit and 10-bit |
| Double addressing | — | yes (slave addr + slave register addr) | yes |
| Clock stretching | continuous transfer with SCL disabled | continuous transfer by pulling SCL low | continuous transfer by pulling SCL low in slave mode |
| Digital noise filter | programmable | programmable | programmable |
| Command abstraction | yes — hardware command registers `I2C_COMD0…n` | yes | yes |

**Citations [DOC]:**

- ESP32: TRM-32 v5.8 **§ 21.2 Features, p. 393** — master/slave, multi-master, *"Supports standard mode (100 kbit/s)"*, *"Supports fast mode (400 kbit/s)"*, 7/10-bit addressing, programmable digital noise filter.
- ESP32-S3: TRM-S3 v1.8 **§ 27.2, p. 985** — same list. The **800 kbit/s** figure is from **DS-S3 v2.2 § 4.2.1.2, p. 51**: *"Up to 800 kbit/s (constrained by SCL and SDA pull-up strength)"*. DS-S3 also states *"ESP32-S3 has two I2C bus interfaces."*
- ESP32-P4: TRM-P4 v0.7 **§ 47.2 Features, p. 2976** — same list, plus the overview note that *"The two I2C controllers in the main system can act as a master or a slave… while the one in the low-power system can only act as a master (referred to as LP_I2C)."* DS-P4 v0.7 § 4.2.2.3, p. 59: *"ESP32-P4 has three I2C controllers: two in the main system and one in the low-power system."*

> **⚠ Reconciliation note [INF]:** DS-P4 v0.7's headline feature list on p. 3 says *"Two I2Cs"* and separately lists *"LP I2C"*, *"Analog I2C"* and *"I3C"*. § 4.2.2.3 says *"three I2C controllers"* counting the LP one. Both are right; the count depends on whether LP I2C is included. **From ESP-IDF you get 2 general `i2c_port_t` values** plus a separate LP I2C driver.

---

## 9. UART

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Controllers | **3** (UART0/1/2) | **3** (UART0/1/2) | **5 (HP)** + **1 LP UART** |
| FIFO | shared RAM; 2 UDMA (UHCI) controllers shared by the three | **1024 × 8-bit RAM shared by TX+RX FIFOs of all three** | — |
| Auto baud detection | yes | yes | yes |
| Data bits | 5–8 | 5–8 | 5–8 |
| Stop bits | 1, 1.5, 2 | **1, 1.5, 2, or 3** | 1, 1.5, 2, 3 |
| RS485 / IrDA | yes | yes | yes |
| Wake-up source | yes | yes | yes + LP UART wakes LP core |
| Flow control | HW (RTS/CTS) and SW (XON/XOFF) | HW and SW | HW and SW |
| DMA | UHCI/UDMA | GDMA | GDMA |

**Citations [DOC]:** TRM-32 v5.8 **§ 13.1, p. 348** — *"The ESP32 has three UART interfaces that share two UDMA (UART DMA) controllers."* DS-S3 v2.2 **§ 4.2.1.1, p. 51** — *"ESP32-S3 has three UART … controllers"* + the feature list quoted above including the *"1024 x 8-bit RAM shared by TX FIFOs and RX FIFOs of the three UART controllers"*. DS-P4 v0.7 **§ 4.2.2.1, p. 57** — *"ESP32-P4 has six UART controllers, including five UARTs in the HP system and one low-power (LP) UART."*

> **[INF]** The S3's shared 1024-byte FIFO RAM is worth remembering: the per-UART FIFO length is configurable but the three controllers draw from one pool. Giving UART1 a deep RX FIFO for a high-rate sensor link costs UART0's console FIFO.

---

## 10. ADC

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| SAR ADCs | **2**, 12-bit | **2**, 12-bit | **2**, 12-bit |
| Channels | **18 max** (ADC1 8 + ADC2 10) | **20 max** (ADC1 10 + ADC2 10) | — |
| Controllers | **5**: RTC ADC1, RTC ADC2, DIG ADC1, DIG ADC2, PWDET | **4**: RTC ADC1, RTC ADC2, DIG ADC1, PWDET | DIG ADC controller + LP DIG ADC controller |
| Sampling rate | — | **≤100 kSPS** | **≤100 kSPS** |
| DNL | — | **−4 … +4 LSB** | **−1 … +3 LSB** |
| INL | — | **−8 … +8 LSB** | **−5 … +3 LSB** |
| Uncalibrated spread | **±6 % between chips** | — | — |

### Calibrated total error and usable input range **[DOC]**

| Atten | ESP32 (DS-32 v5.3 Table 4-4, p. 44) | ESP32-S3 (DS-S3 v2.2 Table 5-6, p. 68) | ESP32-P4 (DS-P4 v0.7 Table 5-6, p. 90) |
|---|---|---|---|
| 0 | 100 – 950 mV, ±23 mV | 0 – 850 mV, ±5 mV | 0 – 1000 mV, ±12 mV |
| 1 | 100 – 1250 mV, ±30 mV | 0 – 1100 mV, ±6 mV | 0 – 1300 mV, ±12 mV |
| 2 | 150 – 1750 mV, ±40 mV | 0 – 1600 mV, ±10 mV | 0 – 1900 mV, ±12 mV |
| 3 | 150 – 2450 mV, ±60 mV | 0 – 2900 mV, **±50 mV** | 0 – 3300 mV, ±15 mV |

### ⚠ Linearity and usability caveats

1. **ESP32 has a non-zero lower bound.** The effective range starts at **100 mV (atten 0/1)** or **150 mV (atten 2/3)**, not 0 V — DS-32 v5.3 Table 4-4, p. 44 **[DOC]**. Readings below that are not specified. S3 and P4 both start at 0.
2. **ESP32 is ±6 % chip-to-chip before calibration.** DS-32 v5.3 **p. 43** **[DOC]**: *"By default, there are ±6% differences in measured results between chips. ESP-IDF provides couple of calibration methods for ADC1."* Note **calibration is offered for ADC1**; ADC2 is the poor relation.
3. **ESP32 ADC2 is shared with Wi-Fi and cannot be used while Wi-Fi is on.** TRM-32 v5.8 **§ 31.3, p. 741** **[DOC]**: *"PWDET/PKDET controller is for Wi-Fi internal use only. If Wi-Fi module is using the SAR ADC2, users can not measure the analog signal from the pins using SAR ADC2. After SAR ADC2 is released by Wi-Fi, users can use SAR ADC2 normally."*
4. **Three of ESP32's ADC2 pins are strapping pins.** TRM-32 v5.8 **p. 742** **[DOC]**: *"Some of the SAR ADC2 pins are used as strapping pins (GPIO0, GPIO2, and GPIO15), thus can not be used freely."*
5. **⚠ ESP32-S3's DIG ADC2 controller is broken.** TRM-S3 v1.8 **§ 39.3, p. 1466** carries an explicit editorial note **[DOC]**: *"The DIG ADC2 controller of ESP32-S3 doesn't work properly and related information has been deleted in this chapter."* The errata says the same thing operationally — see [errata-practical.md § ADC-183](errata-practical.md#adc-183--sar-adc2-has-no-working-dma-controller). **Practical rule: on ESP32-S3, only ADC1 has DMA/continuous mode. ADC2 is single-shot via the RTC controller only.**
6. **S3 atten-3 total error is 5–10× worse than the other attenuations** (±50 mV vs ±5…±10 mV) — DS-S3 v2.2 Table 5-6 **[DOC]**. **[INF]** If you need accuracy above 1.6 V on an S3, use an external divider at atten 2 rather than atten 3.
7. **S3's DNL/INL are the worst of the three** (±4 / ±8 LSB, vs P4's −1…+3 / −5…+3). Espressif's own mitigation, DS-S3 v2.2 Table 5-5 note 1 **[DOC]**: *"To get better DNL results, you can sample multiple times and apply a filter, or calculate the average value."*

**Other citations [DOC]:** ESP32 two 12-bit SAR ADCs on 18 pins: TRM-32 v5.8 § 31.3, p. 740 and DS-32 v5.3 § 4.8.10 p. 44 (*"the ADCs can be configured to measure voltage on 18 pins maximum"*). Five controllers: TRM-32 v5.8 **Table 31.3-2, p. 743**. S3 two 12-bit SAR ADCs / 20 pins: TRM-S3 v1.8 § 39.3, p. 1465 (*"ESP32-S3 integrates two 12-bit SAR ADCs, which are able to measure analog signals from up to 20 pins"*), channel split at **p. 1467** (*"SAR ADC1: measures voltages from up to 10 channels. SAR ADC2: measures the voltage from 10 channels."*).

---

## 11. GPIO — count, restrictions, and what the memory eats

| Property | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Programmable GPIOs | **34** | **45** | **55** |
| **Input-only** | **6** — **GPIO34–39** | **none** | **none** |
| Strapping pins | **5** — GPIO0, GPIO2, MTDI (GPIO12), MTDO (GPIO15), GPIO5 | **4** — GPIO0, GPIO3, GPIO45, GPIO46 | **5** — GPIO34, GPIO35, GPIO36, GPIO37, GPIO38 |
| Consumed by in-package flash/PSRAM | **6** | **6** (flash *or* PSRAM) / **7** (flash *and* PSRAM) | in-package PSRAM uses dedicated pins |
| Touch-capable | 10 | 14 | yes (count not in DS feature list) |

**Citations [DOC]:**

- ESP32: DS-32 v5.3 "Features" **p. 3** — *"34 programmable GPIOs / Five strapping GPIOs / Six input-only GPIOs / Six GPIOs needed for in-package flash (ESP32-U4WDH) and in-package PSRAM (ESP32-D0WDRH2-V3)"*, *"10 touch sensors"*. Input-only detail: DS-32 v5.3 **Appendix, Table IO_MUX note, p. 74** — *"GPIO pins 34-39 are input-only. These pins do not feature an output driver or internal pull-up/pull-down."* Strapping list: DS-32 v5.3 **§ 3, p. 22**.
- ESP32-S3: DS-S3 v2.2 "Features" **p. 4** — *"45 programmable GPIOs / 4 strapping GPIOs / GPIOs allocated for in-package memory: 6 GPIOs for either in-package flash or PSRAM; 7 GPIOs when both in-package flash and PSRAM are integrated"*, *"14 capacitive touch sensing IOs"*. Strapping pins named at **§ 2.3, p. 26** (*"GPIO0, GPIO3, GPIO45, GPIO46 : Strapping pins"*).
- ESP32-P4: DS-P4 v0.7 "Features" **p. 3** — *"55 programmable GPIOs / Five strapping GPIOs"*. Named at **§ 2.3, p. 20**: *"GPIO34, GPIO35, GPIO36, GPIO37, GPIO38 : Strapping pins."*

Full strapping semantics (what each pin selects, default pull, latch timing) are in [memory-and-boot.md § 4](memory-and-boot.md#4-strapping-pins-per-chip).

> **⚠ The GPIO34–39 input-only rule is the single most common ESP32 hardware mistake [INF].** No output driver *and no internal pull-up or pull-down*, so a button on GPIO34 needs an external resistor. This does not apply to S3 or P4 — every GPIO there is bidirectional.

For the U4WDH's specific six flash pins and the pin-by-pin table, see [esp32-u4wdh README § 18](../../components/espressif/esp32-u4wdh/README.md).

---

## 12. DMA, USB, SD/MMC

### 12.1 DMA

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Architecture | per-peripheral DMA; **2 DMA channels shared by SPI1/SPI2/SPI3**; I2S has its own | **GDMA** — central crossbar | **GDMA-AHB** + **GDMA-AXI** + **VDMA** + **2D-DMA** |
| Channels | 2 shared SPI + 1 per I2S direction | **5 TX + 5 RX** (10 total) | **3 TX + 3 RX per GDMA controller** (12 total across AHB+AXI) |

**Citations [DOC]:** TRM-32 v5.8 § 2.5, p. 354 (*"Controllers SPI1~SPI3 share two DMA channels"*) and § 2.5 p. 56. TRM-S3 v1.8 **§ 3.1, p. 357** — *"The GDMA controller in ESP32-S3 has ten independent channels, i.e., five transmit channels and five receive channels"*, repeated **§ 3.3, p. 358**; DS-S3 v2.2 "Features" p. 3: *"General DMA controller, with 5 transmit channels and 5 receive channels."* TRM-P4 v0.7 **§ 7, p. 659** — *"GDMA-AHB and GDMA-AXI have six independent channels respectively, i.e., three transmit channels and three receive channels"*; the interrupt matrix at **p. 1229** enumerates `AHB_PDMA_IN_CH0…2`, `AHB_PDMA_OUT_CH0…2`, `AXI_PDMA_IN_CH0…2`, `AXI_PDMA_OUT_CH0…2`, confirming the count. DS-P4 v0.7 "Features" p. 3 lists GDMA / VDMA / 2D-DMA.

> **[INF]** The S3's ten GDMA channels are a *shared pool*: SPI2, SPI3, I2S0, I2S1, SDMMC, AES, SHA, UHCI, RMT ch3/ch7 and LCD_CAM all draw from it. A design running QSPI display + I2S audio + SD card concurrently is already using 6 of the 10. `ESP_ERR_NOT_FOUND` from a driver's DMA init is the symptom of exhaustion.

### 12.2 USB

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| USB OTG | **none** | **1 × Full-Speed** | **1 × High-Speed** + **1 × Full-Speed** |
| USB Serial/JTAG | **none** | **1** (FS, CDC-ACM + JTAG) | **1** (FS, up to 12 Mbit/s) |
| Internal PHY | — | 1, time-division-multiplexed between OTG and Serial/JTAG, or use an external PHY for one of them | **2 integrated FS transceivers** (GPIO24/25 and GPIO26/27) so OTG and Serial/JTAG can run simultaneously |
| Endpoints (OTG) | — | EP0 + 6 configurable; **max 5 IN active** incl. EP0 IN; 8 host channels | FS: max 5 IN incl. EP0; 8 host channels. HS: **max 8 IN** incl. EP0 IN |
| Flashing over USB | ❌ needs an external USB-UART bridge | ✅ USB-Serial-JTAG or USB-OTG | ✅ USB-Serial-JTAG, or **HS OTG in FS mode only** |

**Citations [DOC]:** DS-S3 v2.2 **§ 4.2.1.7, p. 54** (OTG FS feature list incl. endpoint counts and transceiver multiplexing) and **§ 4.2.1.8, p. 55** (Serial/JTAG). DS-P4 v0.7 **§ 4.2.2.9 pp. 62–63** (HS OTG), **§ 4.2.2.10 p. 63** (FS OTG), **§ 4.2.2.11 p. 64** (Serial/JTAG, two transceivers). ESP32 has neither peripheral — DS-32 v5.3 contains no USB chapter; the boot mode table lists only SDIO and UART download methods (**§ 3.1, p. 23**).

> **⚠ P4 flashing gotcha [DOC]:** DS-P4 v0.7 **Table 3-3, p. 37**, note 2: *"only the USB 2.0 High-Speed OTG can be used for flashing at Full-Speed mode; the USB 2.0 Full-Speed OTG does not support device firmware upgrade."*

> **⚠ S3 USB-OTG download is disabled by eFuse on early parts** — see [errata-practical.md § USBOTG-4289](errata-practical.md#usbotg-4289--usb-otg-download-mode-fused-off-on-early-parts).

The ESP32's lack of USB is why the ESP32-S3-Knob board fits a separate bridge for its U4WDH — see [esp32-u4wdh README § 7.2](../../components/espressif/esp32-u4wdh/README.md).

### 12.3 SD/MMC host

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Host slots | **2** | **2** | **2** ("two external cards") |
| Bus widths | 1 / 4 / 8-bit | **1 / 4 / 8-bit** | **1 / 4 / 8-bit** |
| Max clock out | — | **80 MHz** | — |
| Standards | SD, SDIO, MMC | SD 3.0 & 3.01, SDIO 3.0, CE-ATA 1.1, MMC 4.41 / eMMC 4.5 & 4.51 | SD 3.0 & 3.01, SDIO 3.0, MMC 4.41/4.5/4.51, CE-ATA 1.1 |
| Notable | ESP32 also has an SDIO **slave** | 4-bit mode supports *two* SD/SDIO/MMC cards, or one SD card at 1.8 V | — |

**Citations [DOC]:** DS-S3 v2.2 **§ 4.2.1.9, p. 55** — full feature list including *"Up to 80 MHz clock output"* and *"Three data bus modes: 1-bit / 4-bit (supports two SD/SDIO/MMC 4.41 cards, and one SD card operating at 1.8 V in 4-bit mode) / 8-bit"*. DS-P4 v0.7 **§ 4.2.2.14, p. 67**. ESP32 host + slave: DS-32 v5.3 "Features" p. 4 — *"One host (SD/eMMC/SDIO) / One slave (SDIO/SPI)"*.

---

## 13. Memory, cache and crypto

Full memory maps, boot behaviour and PSRAM voltage constraints live in **[memory-and-boot.md](memory-and-boot.md)**. Summary:

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| ROM | **448 KB** (ROM0 384 KB + ROM1 64 KB) | **384 KB** | **128 KB HP** + 16 KB LP |
| SRAM | **520 KB** (SRAM0 192 + SRAM1 128 + SRAM2 200) | **512 KB** | **768 KB HP L2MEM** + 32 KB LP SRAM + 8 KB SPM |
| RTC memory | 8 KB FAST + 8 KB SLOW | 8 KB FAST + 8 KB SLOW | LP SRAM |
| eFuse | **1024 bit**, 768 for customer | **4096 bit**, 1792 for user | **4096 bit**, 1792 for user |
| Cache | shared, fixed | **I-cache 16/32 KB, D-cache 32/64 KB**, shared by both cores | two-level cache |
| External flash max | **16 MB** (11 MB+248 KB instruction / 4 MB data at a time) | 1 GB addressable; **32 MB mapped at a time**, 64 KB blocks | **64 MB** mapped, 64 KB blocks |
| External RAM max | **8 MB**, 4 MB mapped at a time | part of the 1 GB / 32 MB window | in-package only on current parts |
| PSRAM interface | QSPI | **SPI/Dual/Quad/Octal/QPI/OPI**, up to 120 MHz on 8-line SDR/DDR | in-package, **16-bit bus, 250 MHz, DDR → 8 Gbit/s**, ≤64 MB |
| Flash/PSRAM encryption | AES | **XTS-AES** | **XTS-AES** |

**Crypto accelerators:**

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| AES | ✅ FIPS-197 | ✅ typical + DMA modes | ✅ |
| SHA | ✅ FIPS-180-4 | ✅ all FIPS-180-4 hashes, typical + DMA modes | ✅ |
| RSA | ✅ **up to 4096 bit** | ✅ modexp/modmul **≤4096 bit**, multiply **≤2048 bit** | ✅ |
| HMAC | — | ✅ HMAC-SHA-256, downstream mode | ✅ |
| RSA_DS (digital signature) | — | ✅ **≤4096 bit** key | ✅ |
| ECDSA / ECC | — | — | ✅ ECC accelerator + ECDSA_DS |
| XTS-AES (flash/PSRAM) | — (plain AES flash encryption) | ✅ IEEE 1619-2007 | ✅ |
| RNG | ✅ | ✅ | ✅ **TRNG** |
| Secure boot | ✅ | ✅ + permission control on memory access | ✅ + PMS/APM permission control |
| Key manager / HUK | — | — | ✅ **HUK from SRAM PUF**, Key Manager |
| Clock-glitch detection | — | ✅ | ✅ |
| TEE / PMP-PMA | — | World Controller (WCL) | ✅ TEE, PMP and PMA |

**Citations [DOC]:** DS-32 v5.3 **§ 4.1.2, p. 26** (memory), **Table 4-1, pp. 28–29** (map), **§ 4.5, p. 39** (crypto — *"maximum operation length for RSA … is 4096 bits"*). DS-S3 v2.2 **§ 4.1.2.1–4.1.2.3, pp. 38–39** (memory, external mapping, cache banks/associativity) and **§ 4.1.4, pp. 44–48** (crypto). DS-P4 v0.7 **§ 4.1.3.1, pp. 45–46** (memory, PSRAM bandwidth formula) and **§ 4.1.5, pp. 51–56** (crypto).

> **⚠ The "16 KB SRAM in RTC" discrepancy.** Both DS-32 v5.3 (p. 3) and DS-S3 v2.2 (p. 3) list *"16 KB SRAM in RTC"* in the headline features, but § 4.1.2 of each resolves it as **8 KB RTC FAST + 8 KB RTC SLOW** — two separate blocks with different access rules (FAST: main CPU only; SLOW: main CPU *and* ULP). They are not a single 16 KB pool. **[DOC]** DS-32 v5.3 § 4.1.2 p. 26; DS-S3 v2.2 § 4.1.2.1 pp. 38–39.

---

## 14. Revision differences observed

We hold two revisions of each of the ESP32 and ESP32-S3 documents. Differences relevant to the numbers on this page:

| Document pair | Finding |
|---|---|
| ESP32 TRM **v5.4** (Waveshare mirror, 779 pp.) vs **v5.8** (784 pp.) | No change to PCNT (8 units), RMT (8 channels, 512×32 RAM), LEDC (16 ch / 2 speed modes / 20-bit), timer group (2×2, 64-bit) or I2S (2, PDM on I2S0) counts. The five extra pages are elsewhere. **[DOC]** |
| ESP32 DS **v4.9** (Waveshare mirror, 77 pp.) vs **v5.3** (78 pp.) | v5.3's own revision history records edits to § 4.8.3/4.8.4 (UART/I2C) and a **typo fix in the § 4.8.7 PCNT feature list** — DS-32 v5.3 revision history, pp. 76–77 **[DOC]**. Prefer v5.3 for PCNT. |
| ESP32-S3 TRM **v1.2** (Waveshare mirror, 1477 pp.) vs **v1.8** (1531 pp.) | Counts unchanged. v1.8 carries the editorial note that DIG ADC2 *"doesn't work properly and related information has been deleted in this chapter"* (§ 39.3, p. 1466) — check whether your copy of v1.2 still documents DIG ADC2 registers; if so, **do not use them**. **[INF]** |
| ESP32-S3 DS **v1.6** (Waveshare mirror, 75 pp.) vs **v2.2** (87 pp.) | v2.2's revision history records *"Updated the effective measurement range in Table 5-5 ADC Characteristics"* **[DOC]** (DS-S3 v2.2 p. 85). **The ADC ranges in § 10 of this page are the v2.2 values; v1.6's differ.** Use v2.2. |

Chip-**revision** (silicon) differences — as opposed to document revisions — are in **[errata-practical.md](errata-practical.md)** and, for the ESP32 v3.0/v3.1 story specifically, [esp32-u4wdh README § 21](../../components/espressif/esp32-u4wdh/README.md).

**No peripheral count in this document differs between chip revisions of a given part.** Peripheral instance counts are fixed in the die; what changes between revisions is whether a given peripheral *works* (see the errata page).

---

## 15. Extraction notes and text-layer quality

**All six primary PDFs have a clean, extractable text layer.** They are LaTeX/`xdvipdfmx` productions with real embedded fonts, not glyph-subset scans. Every number on this page was read from `pdftotext -layout` output and spot-verified against the rendered page.

Two mechanical notes for anyone re-extracting:

1. **Printed page ≠ PDF page index.** Front matter is unnumbered, so PDF page *N* is not printed page *N*. The footer line `Espressif Systems  <n>  ESP32-S3 TRM (Version 1.8)` gives the printed number and **trails** the content of that page in the text stream. A naive "last footer seen" page tracker is off by one.
2. **Register diagrams extract as vertical noise.** Bit-field labels are set rotated, so `pdftotext` emits them one character per line. Register-summary *tables* extract cleanly; register *diagrams* do not. This did not block anything on this page, which is sourced from prose and feature lists.

**Nothing was blocked by the text layer.** The only content that resisted extraction was figures (block diagrams, timing waveforms), which are raster/vector images with no text to recover — noted where relevant.

> **Update 2026-08-30:** [§ 16.10](#1610-extraction-record-for-this-section) records the same behaviour across a further ~200 pages of the three TRMs, plus **one case where a figure genuinely blocked a question** (ESP32 TRM Figures 22.5-2/22.5-3, the I2S-LCD data-frame forms — see [§ 16.2](#162-esp32--the-lcd-peripheral-that-is-really-i2s)), and one technique for reading a field width out of a register diagram whose labels do not extract.

---

## 16. LCD, camera and display peripherals

**Extracted 2026-08-30.** This section answers the question [display-interfaces.md § 4](../hardware/display-interfaces.md#4-what-each-esp32-generation-actually-provides) raised and could not answer: what each part's display peripheral actually is, in numbers. Page ranges used are listed in [§ 16.10](#1610-extraction-record-for-this-section).

The companion page is **[display-interfaces.md](../hardware/display-interfaces.md)** — transports, framebuffer arithmetic, TE lines, LVGL and the panels actually fitted in this library. **This section is the silicon; that page is the practice.**

### 16.1 The one-page display answer

| | **ESP32** | **ESP32-S3** | **ESP32-P4** |
|---|---|---|---|
| Dedicated LCD peripheral | ❌ **none** — LCD is a *mode of I2S* | ✅ **`LCD_CAM`** (Ch. 29) | ✅ **`LCD_CAM`** (Ch. 40) |
| **i80 (Intel 8080)** | ✅ (as I2S "LCD master transmitting mode") | ✅ | ✅ |
| **MOTO6800** | ❌ not named | ✅ | ✅ |
| **RGB / DPI parallel** | ❌ **no sync outputs exist** | ✅ | ✅ |
| **LCD data bus width** | **8 / 16 / 24-bit**, but **24-bit on I2S0 only** | **8 / 16-bit** | **8 / 16 / 24-bit** |
| Max LCD pixel clock, 8-bit | not stated (see § 16.2) | **< 80 MHz** (< 60 MHz with YUV conversion) | **< 80 MHz** (< 60 MHz with YUV conversion) |
| Max LCD pixel clock, 16-bit | — | **< 40 MHz** (< 30 MHz with YUV conversion) | **< 40 MHz** (< 30 MHz with YUV conversion) |
| Max LCD pixel clock, 24-bit | — | n/a | ⚠ **not stated anywhere** |
| LCD colour conversion | ❌ none | RGB565 ↔ YUV422/420/411, BT601/BT709 | + **RGB888 ↔ RGB565**, YUV → RGB888, → YUV444 |
| **DVP camera** | ✅ **8/16-bit**, **slave RX only** (as I2S mode) | ✅ **8/16-bit**, master or slave RX | ✅ **8/16-bit**, master or slave RX |
| **MIPI-DSI** | ❌ | ❌ | ✅ **1 clk + 2 data lanes, 80 Mbps – 1.5 Gbps/lane**, DPI ≤ 240 MHz |
| **MIPI-CSI** | ❌ | ❌ | ✅ **1 clk + 2 data lanes, 80 Mbps – 1.5 Gbps/lane** |
| **ISP** | ❌ | ❌ | ✅ **≤ 1920 × 1080**, RAW8/10/12 in |
| **PPA** (blend/scale/rotate/CSC) | ❌ | ❌ | ✅ |
| **2D-DMA** | ❌ | ❌ | ✅ 4 TX + 3 RX, serves **JPEG and PPA only** |
| **JPEG codec** | ❌ | ❌ | ✅ enc + dec, **1080p@40 fps** |
| **H.264 encoder** | ❌ | ❌ | ✅ baseline, **1080p@30 fps** |
| DMA feeding the display | I2S's own DMA | **GDMA** (shared 10-channel pool) | **GDMA** for `LCD_CAM`, **VDMA** for MIPI-DSI, **2D-DMA** for PPA/JPEG |

**[DOC]** Absence rows for ESP32 and ESP32-S3 are not inference from silence: DS-32 v5.3 and DS-S3 v2.2 contain **zero occurrences** of "MIPI", "JPEG", "H264" or "pixel-processing" in their full text layers. DS-S3 v2.2 "Features" **p. 4** lists exactly *"LCD interface"* and *"8-bit ~ 16-bit DVP camera interface"* and nothing else in this class.

---

### 16.2 ESP32 — the LCD peripheral that is really I2S

**There is no LCD controller on the ESP32.** TRM-32 v5.8 puts the whole thing in **Ch. 22 § 22.5, "Camera-LCD Controller", p. 426** **[DOC]**, inside the I2S chapter, with three modes:

> *"There are three operational modes in the LCD mode of ESP32 I2S: LCD master transmitting mode / Camera slave receiving mode / ADC/DAC mode. The clock configuration of the LCD master transmitting mode is identical to I2S' clock configuration. In the LCD mode, the frequency of WS is half of f<sub>BCK</sub>."*
> — TRM-32 v5.8 § 22.5, p. 426 **[DOC]**

| Property | Value | Citation **[DOC]** |
|---|---|---|
| Bus type | **i80-like only**: `WS` becomes the LCD `WR` strobe | § 22.5.1, p. 426 — *"the WR signal of LCD connects to the WS signal of I2S"* |
| Data bus width, TX | *"The LCD data bus width is 24 bits."* Configurable **N = 8, 16 or 24** | § 22.5.1, p. 426; Table 22.1-1 note 1, p. 416 |
| **⚠ 24-bit restriction** | *"note that I2S1 does not support 24-bit width"* | Table 22.1-1 note 1, **p. 416** |
| Data bus width, RX (camera) | **N = 8 or 16**; the camera path is the 16-channel `I2SnI_Data_in` | Table 22.1-1 note 1, p. 416; § 22.5.2, p. 427 |
| Enable bits | `I2S_LCD_EN` (+ `I2S_CAMERA_EN` for DVP), `I2S_TX_SLAVE_MOD = 0` | § 22.5.1–22.5.2, pp. 426–427 |
| Data-frame shaping | `I2S_LCD_TX_WRX2_EN` and `I2S_LCD_TX_SDX2_EN` select **form 1** (WRX2=1, SDX2=0) or **form 2** (both = 1) | § 22.5.1, p. 427 |
| Clock chain | `I2Sn_CLK` from **PLL_F160M_CLK (160 MHz)** or APLL; f<sub>i2s</sub> = f<sub>pll</sub>/(N + b/a), **N ≥ 2**; f<sub>BCK</sub> = f<sub>i2s</sub>/M, **M ≥ 2** | § 22.3, pp. 417–418 |
| Camera start condition | `HSYNC && VSYNC && H_ENABLE` all high; invert through the GPIO matrix if your sensor differs | § 22.5.2, p. 427 |

**⚠ The ESP32 cannot drive an RGB/DPI panel.** **[INF]**, from the signal table: Table 22.1-1 (**p. 416**) defines `I2Sn_H_SYNC`, `I2Sn_V_SYNC` and `I2Sn_H_ENABLE` as *"In Camera mode, I2S module inputs signals"* — they exist **only as inputs**. There is no `LCD_H_SYNC` / `LCD_V_SYNC` / `LCD_DE` output anywhere in the ESP32 I2S signal bus, and § 22.5 lists no RGB mode. Compare the S3's Table 29.3-1 and the P4's Table 40.3-1, which both define those three signals as **outputs** in LCD Master TX mode.

**Pixel-clock ceiling [INF]:** the TRM states no maximum for LCD mode. From the clock chain above, f<sub>i2s</sub> ≤ 160/2 = **80 MHz** and f<sub>BCK</sub> ≤ 80/2 = **40 MHz**; § 22.5 then makes the LCD `WR` strobe (WS) **half of f<sub>BCK</sub>**, so the arithmetic ceiling on the write strobe is **≈ 20 MHz** before the `WRX2`/`SDX2` framing is taken into account. **This is derived here, not quoted.**

> **⚠ Unresolved: what `I2S_LCD_TX_WRX2_EN` actually does to the effective rate.** The TRM describes forms 1 and 2 in prose (**p. 427**) but the distinguishing content is **Figures 22.5-2 and 22.5-3**, which are vector images with no recoverable text. This is the same 2× uncertainty [display-interfaces.md § 2.3](../hardware/display-interfaces.md#23-e-paper-parallel--inkplate-5-gen-2) records for the Inkplate's 16 MHz BCK, and **the TRM does not settle it**. Settling it needs the rendered figures or a measurement.

---

### 16.3 ESP32-S3 — `LCD_CAM`

TRM-S3 v1.8 **Ch. 29, p. 1078** **[DOC]**:

> *"This LCD and Camera (LCD_CAM) controller consists of a LCD module and a camera module. The LCD module is designed to send parallel video data signals, and its bus supports RGB, MOTO6800, and I8080 interface timing. The camera module is designed to receive parallel video data signals, and its bus supports DVP 8-/16-bit modes."*

**Feature list, § 29.2, p. 1078 [DOC]:** LCD master TX mode; camera slave RX mode; camera master RX mode; **simultaneous connection to an external LCD *and* an external camera**; LCD 8-/16-bit parallel output; RGB / MOTO6800 / I8080; LCD data from internal memory via GDMA; camera 8-/16-bit parallel input; camera data to internal memory via GDMA.

**Structure, § 29.3.1, pp. 1078–1079 [DOC]:** 1 × TX control unit, 1 × RX control unit, **1 × async TX FIFO**, **1 × async RX FIFO**, 2 × clock generators, **2 × RGB/YCbCr converters** (one per direction).

#### Signals — Table 29.3-1, pp. 1079–1080 **[DOC]**

| LCD Master TX | Camera RX |
|---|---|
| `LCD_PCLK` (out), `LCD_H_SYNC` (out, RGB), `LCD_V_SYNC` (out, RGB), `LCD_H_ENABLE` (out, RGB), `LCD_CD` (out, I8080), `LCD_CS` (out, I8080/MOTO6800), `LCD_Data_out[N:0]` **N = 7 or 15** | `CAM_PCLK` (in), `CAM_V_SYNC`, `CAM_H_SYNC`, `CAM_H_ENABLE`, `CAM_Data_in[N:0]` **N = 7 or 15**; master mode adds `CAM_CLK` (out) |

> **⚠ Every `LCD_CAM` signal is GPIO-matrix-only.** Table 29.3-1 note 1, **p. 1080** **[DOC]**: *"All signals of LCD_CAM must be mapped to the chip's pin via GPIO matrix."* There is **no IO MUX fast path** for the LCD bus, unlike SPI2 (§ 7). **[INF]** That matters at the top of the pixel-clock range, and it is one reason a 16-bit RGB bus on an S3 is not a trivially fast interface.

#### Clocks — § 29.3.3.1, pp. 1080–1081 **[DOC]**

`LCD_CLK_SEL` picks **0 = off, 1 = XTAL_CLK, 2 = PLL_D2_CLK, 3 = PLL_F160M_CLK**. Then

$$f_{\text{LCD\_CLK}} = \frac{f_{\text{LCD\_CLK\_S}}}{N + \frac{b}{a}}\qquad N \in [2, 256] \qquad\text{and}\qquad f_{\text{LCD\_PCLK}} = \frac{f_{\text{LCD\_CLK}}}{MO}$$

with `MO = 1` when `LCD_CAM_LCD_CLK_EQU_SYSCLK = 1`, else `LCD_CAM_LCD_CLKCNT_N + 1` (which *"must not be configured as 0"*). **[INF]** Because the minimum divider is **N = 2**, the highest `LCD_CLK` obtainable on an S3 is **PLL_D2_CLK ÷ 2 = 120 MHz** — above the peripheral's own stated pixel-clock ceiling, so the divider is not the binding constraint.

#### ⚠ Pixel-clock ceilings — § 29.4.2 Notes, **p. 1090** **[DOC]**

> *"No matter in which format, RGB or I8080/MOTO6800, the rules below must be followed when accessing internal memory via GDMA:"*

| LCD bus width | Plain | With YUV-RGB conversion enabled |
|---|---:|---:|
| **8-bit** | **< 80 MHz** | **< 60 MHz** |
| **16-bit** | **< 40 MHz** | **< 30 MHz** |

The **identical** table applies to the camera direction — § 29.4.3 Notes, **pp. 1090–1091** **[DOC]**.

> **⚠ The datasheet and the TRM do not agree.** DS-S3 v2.2 § 4.2.1.4, **p. 52** **[DOC]** says the LCD interfaces *"operate at 40 MHz or lower"* and the DVP camera *"with clock frequency of up to 40 MHz"* — a single flat 40 MHz. The TRM allows **80 MHz in 8-bit mode**. **[INF]** Read the datasheet as the conservative always-safe figure and the TRM as the width-dependent one; if you are designing to 80 MHz on an 8-bit bus you are relying on the TRM, and should say so.

#### ⚠ The 80 MB/s concurrency budget — § 29.4.3 Notes, **p. 1091** **[DOC]**

> *"If an external camera and an external LCD are connected simultaneously, ensure that the maximum data throughput on the interface is less than GDMA total data bandwidth of 80 MB/s. Note the default frequency of APB_CLK is 80 MHz here."*

**This is the only hard concurrency number Espressif publishes for `LCD_CAM`, and it is easy to blow.** **[INF]** A 16-bit DVP camera at 20 MHz PCLK is 40 MB/s on its own; a 16-bit RGB panel at 20 MHz is another 40 MB/s; together they are exactly at the limit before any other GDMA client (SPI, I2S, SDMMC — § 12.1) is considered.

#### Colour conversion — § 29.3.6, p. 1085 **[DOC]**

BT601 and BT709; **RGB565 (full/limited) ↔ YUV422 / YUV420 / YUV411 (full/limited)**, and YUV↔YUV among 422/420/411. Full conversion matrix in **Table 29.3-4, p. 1086**. Full range = 0–255; limited range = RGB 16–240, Y 16–240, U-V 16–235 (p. 1086).

> **⚠ RGB565 is the only RGB format the S3's converter knows.** There is no RGB888 path — Table 29.3-4 lists twelve conversions and every RGB entry is `RGB565`. **[INF]** A 24-bit RGB888 panel is therefore off the table on an S3 twice over: the bus is 8/16-bit only, and the converter has no RGB888 mode. This is exactly the capability the P4 adds (§ 16.4).

#### Interrupts — § 29.5, p. 1091 **[DOC]**

`LCD_CAM_CAM_HS_INT` (line count reached), `LCD_CAM_CAM_VSYNC_INT`, `LCD_CAM_LCD_TRANS_DONE_INT`, **`LCD_CAM_LCD_VSYNC_INT`** (*"triggered when the LCD transmitted a VSYNC signal"*).

> **[INF] `LCD_CAM_LCD_VSYNC_INT` is the S3's tear-avoidance hook for RGB/DPI panels**, and it is the structural answer to the TE question for a host-timed panel: with no GRAM in the panel there is no read pointer to chase, so you synchronise buffer swaps to *your own* frame output. See [display-interfaces.md § 6.5](../hardware/display-interfaces.md#65-mipi-dsi-video-mode-te-is-not-the-mechanism).

---

### 16.4 ESP32-P4 — `LCD_CAM`

TRM-P4 v0.7 **Ch. 40, p. 2300** **[DOC]**. Structurally the same block as the S3's, with three differences that matter.

**Feature list, § 40.2, p. 2300 [DOC]:** operation modes as S3; simultaneous LCD + camera; **8/16/24-bit parallel output**; RGB / MOTO6800 / I8080; *"LCD data retrieved from internal memory **or external memory** via GDMA"*; camera 8/16-bit input, also to internal **or external** memory.

| Difference vs S3 | Detail | Citation **[DOC]** |
|---|---|---|
| **24-bit output bus** | `LCD_Data_out[M:0]`, **M = 7, 15 or 23**; `LCD_CAM_LCD_BYTE_MODE = 2` selects 24-bit from GDMA; `LCD_CAM_LCD_WIRE_MODE = 2` selects 24-bit to GPIO | Table 40.3-1 note 2, p. 2302; § 40.3.5.1, pp. 2306–2307 |
| **RGB888 in the converter** | LCD module adds *"from YUV422/411 to RGB888"*, *"from RGB565 to YUV444"*, *"between RGB888 and RGB565"*, *"from YUV422/411 to YUV444"* | § 40.3.6, p. 2309; Table 40.3-5 (24-bit mode), p. 2311 |
| **Divider can be 1** | `HP_SYS_CLKRST_LCD_CLK_DIV_NUM = 0 ⇒ N = 1`, *"The divider is always 1"* | § 40.3.3.1, p. 2303 |

Clock sources are **XTAL_CLK / PLL_F160M_CLK / APLL_CLK** (§ 40.3.3.1, p. 2303) — note **PLL_D2_CLK is gone** relative to the S3. **[INF]** With N = 1 permitted, `LCD_CLK` can equal **160 MHz** on a P4 where the S3 topped out at 120 MHz; again the peripheral's own pixel-clock rule binds first.

#### Pixel-clock ceilings — § 40.5.2 Notes, **pp. 2315–2316** **[DOC]**

Numerically identical to the S3 (8-bit < 80 / < 60 MHz; 16-bit < 40 / < 30 MHz) with one wording change that is worth reading twice:

> *"…the rules below must be followed when accessing **internal and external** memory via GDMA"* — TRM-P4 v0.7 p. 2315 **[DOC]**

The S3's version of the same sentence says *"internal memory"* only (**p. 1090**). **[INF]** The P4 is explicitly stating that the same limits hold when the framebuffer lives in PSRAM, which is the case that actually matters for a large panel.

> **⚠ Gap: there is no stated pixel-clock limit for 24-bit mode.** The feature list offers a 24-bit bus (p. 2300) and the notes on p. 2315–2316 cover only **8-bit and 16-bit**. Nothing in TRM-P4 v0.7 or DS-P4 v0.7 gives a 24-bit figure. **Do not extrapolate**: the 8→16-bit step already halves the ceiling, so a naive "24-bit ⇒ < 26.7 MHz" is a guess, not a derivation.

#### The camera + LCD concurrency note lost its number

TRM-P4 v0.7 **p. 2316** **[DOC]** repeats the S3's warning — *"it is necessary to ensure that the maximum data throughput on the interface is less than the total data bandwidth of GDMA when accessing internal/external storage"* — but **drops the "80 MB/s" figure the S3 gave**. It still says *"The default frequency of APB_CLK is 80 MHz in this scenario."* **[INF]** So on P4 the budget exists but is unquantified in the pre-release TRM. Treat 80 MB/s as a floor, not a specification.

#### Interrupts — § 40.4, pp. 2313–2314 **[DOC]**

Same four as the S3: `LCD_CAM_CAM_HS_INT`, `LCD_CAM_CAM_VSYNC_INT` (*"receives a whole frame"*), `LCD_CAM_LCD_TRANS_DONE_INT`, `LCD_CAM_LCD_VSYNC_INT` (*"transmits a whole frame"*), all funnelled into one `LCD_CAM_INTR` line.

---

### 16.5 ESP32-P4 — MIPI-DSI

TRM-P4 v0.7 **Ch. 43, p. 2633** **[DOC]**:

> *"MIPI DSI in ESP32-P4 consists of three parts: a DSI Bridge, an MIPI DSI Host Controller, and an MIPI Bidirectional D-PHY. It provides **one clock lane and two data lanes**, and supports a **maximum bit rate of 1.5 Gbps per lane** for communication with a DSI-compliant display… **The PHY is only used as master.**"*

| Property | Value | Citation **[DOC]** |
|---|---|---|
| Lanes | **1 clock + 2 data**. Dedicated pins **34–40** (`DSI_CLKP/N`, `DSI_DATAP0/N0`, `DSI_DATAP1/N1`, `DSI_REXT`), rail `VDD_MIPI_DPHY` | TRM § 43.1, p. 2633; DS-P4 § 4.2.1.7, p. 67; DS-P4 pin table, p. 15 |
| Per-lane rate | **80 Mbps – 1.5 Gbps** in HS TX | TRM § 43.2, p. 2633 |
| **Aggregate link** | **3.0 Gbit/s** (2 × 1.5) | **[INF]** from the above |
| D-PHY spec | **MIPI D-PHY rev 1.1**, with its own PLL | TRM § 43.2, p. 2633; DS-P4 p. 67 |
| **Max DPI frequency** | **240 MHz** | TRM § 43.2, p. 2633 |
| Input formats (from memory) | **RGB888, RGB666, RGB565, YUV422, YUV420, GRAY** | TRM § 43.2, p. 2633; § 43.4.1, p. 2635 |
| **Output (DPI) formats** | **RGB888, RGB666, RGB565** only | TRM § 43.2, p. 2633; Table 43.4-2, p. 2636 |
| Video modes | **Burst**, **non-burst with sync pulse**, **non-burst with sync event** | TRM § 43.4.2.1, p. 2637 |
| Command mode | *"Command Mode through APB interface to **access display registers**"*, DCS supported | TRM § 43.2, p. 2634; § 43.4.2.2, p. 2637 |
| Clock lane | continuous **and** non-continuous | TRM § 43.2, p. 2633; § 43.4.4, p. 2656 |
| Escape mode | data lane 0 only; `TX_ESC_CLK` **max 20 MHz** | TRM § 43.2, p. 2633; § 43.4.4, p. 2655 |
| Extras | video pattern generator (colour bar, BER), Ultra Low-Power mode | TRM § 43.2, p. 2634; § 43.4.2.3, p. 2640 |
| DMA | **VDMA**, not GDMA | TRM § 43.1, p. 2633; § 43.6.1, pp. 2661–2662 |

#### ⚠ The pixel path is video mode. Full stop.

This is the fact that governs everything downstream, and it is stated three separate ways:

1. **DS-P4 v0.7 § 4.2.1.7, p. 67** **[DOC]** — the MIPI-DSI feature list reads *"**Using the video mode to output video stream**"* and *"Outputting image patterns"*. Those are the only two pixel sources named.
2. **TRM-P4 v0.7 § 43.6.4, p. 2662** **[DOC]** — *"System memory data output flow configuration"* has exactly two steps: configure the DSI Bridge, configure the DSI Host. The Bridge's only output is DPI (§ 43.1, p. 2633: *"outputs image data through the Display Pixel Interface (DPI) to the MIPI DSI Host Controller"*).
3. **TRM-P4 v0.7 § 43.6.6, pp. 2662–2663** **[DOC]** — the command-mode procedure is *"Using DCS command to **operate Display register**"*: write payload to `DSI_HOST_GEN_PLD_DATA_REG`, header to `DSI_HOST_GEN_HDR_REG`. It is a register channel, not a framebuffer channel.

**[INF] There is no eDPI / command-mode-video framebuffer path on the ESP32-P4.** A DSI panel that only accepts command-mode pixel writes into its own GRAM is not addressable by this peripheral for pixel data.

#### ⚠ But the DSI host *does* have tearing-effect hardware

Two register fields, both in the **Command Mode** side of the host, contradict any flat claim that "the P4 has no TE":

| Field | Register | Description, verbatim | Page |
|---|---|---|---|
| `DSI_HOST_TEAR_FX_EN` | `DSI_HOST_CMD_MODE_CFG_REG` (`0x0068`) | *"Configures whether to enable tearing effect acknowledge request. 0: disable / 1: enable"* | **2699** |
| `DSI_HOST_GEN_VCID_TEAR_AUTO` | `DSI_HOST_GEN_VCID_REG` (`0x0030`) | *"Configures hardware TEA effect virtual channel ID."* | **2693** |

**[INF]** This is the MIPI-DSI *TE-over-link* mechanism — DCS `set_tear_on` followed by the peripheral returning a TE trigger message over the link (no physical TE wire), acknowledged with a BTA. It belongs to command mode. Given that the P4's pixel path is video mode only, **these fields are not the synchronisation mechanism for a video-mode framebuffer** — but they exist, they are documented, and "the ESP32-P4 DSI has no TE support at all" would be wrong.

#### What *is* the video-mode synchronisation hook

`DSI_BRG_VSYNC_INT`, alongside `DSI_BRG_UNDERRUN_INT`, in `DSI_BRG_INT_ENA_REG` (`0x0050`) — **TRM-P4 v0.7 p. 2685** **[DOC]**: *"DSI_BRG_VSYNC_INT_ENA Configures DSI_BRG_VSYNC_INT enable."* Raw and masked status at `0x0058` / `0x005C`, **p. 2686**.

> **⚠ Documentation inconsistency in TRM-P4 v0.7.** **Table 43.5-1, p. 2657** ("DSI Bridge interrupts") lists **only** `DSI_BRG_UNDERRUN_INT`. The register descriptions on pp. 2685–2686 define enable, raw, clear and status bits for **`DSI_BRG_VSYNC_INT` as well**. The register bank is the more specific evidence; the interrupt table appears incomplete. Re-check against a released (non-`PRELIMINARY`) revision.

#### Video timing and the two timing domains

Video timing is configured **twice**, in different units, and they must agree — TRM § 43.4.4, **p. 2657** **[DOC]**:

| DSI Bridge (DPI side) | Unit | DSI Host (link side) | Unit |
|---|---|---|---|
| `DSI_BRG_HTOTAL`, `HDISP`, `HBANK` (HBP), `HSYNC` (HSA) | `DSI_DPICLK` cycles | `DSI_HOST_VID_HLINE_TIME`, `VID_HBP_TIME`, `VID_HSA_TIME` | **`TX_BYTE_CLK`** cycles |
| `DSI_BRG_VTOTAL`, `VDISP`, `VBANK` (VBP), `VSYNC` (VSA) | lines | `DSI_HOST_VSA_LINES`, `VBP_LINES`, `VFP_LINES`, `VACTIVE_LINES` | lines |

> *"The video timing configuration of DPI and DSI should match to avoid line buffer overflow. The actual timing of each line in DPI and DSI should be the same."* — TRM-P4 v0.7 p. 2657 **[DOC]**

Clock tree, § 43.4.4, **pp. 2655–2656** **[DOC]**: `DSI_DPI_CLK` from **XTAL / PLL_F240M / PLL_F160M / APLL**; D-PHY PLL reference from **XTAL / APLL / CPLL / SPLL / MPLL**; `TX_BYTE_CLK = TX_HS_CLK ÷ 8`; `TX_ESC_CLK` divided from `TX_BYTE_CLK`, **≤ 20 MHz**.

#### Burst vs non-burst — the guidance is explicit

TRM § 43.4.2.1, **p. 2637** **[DOC]**: use **Burst Mode** if *"the display peripheral supports receiving a full pixel line in one single block and the reception buffer won't overflow"* **and** *"the DSI output bandwidth is much higher than the DPI input bandwidth"*. Otherwise non-burst, *"Otherwise, the pixel data may be lost, causing malfunction of the display peripheral."* Non-burst with **sync pulse** *"allows the peripheral to accurately reconstruct original video timing, including sync pulse widths"*; **sync event** does not.

---

### 16.6 ESP32-P4 — MIPI-CSI and the DVP camera path

TRM-P4 v0.7 **Ch. 42, p. 2592** **[DOC]**: *"ESP32-P4 MIPI CSI implements a MIPI RX D-PHY and a MIPI CSI-2 host controller. It provides **one clock lane and two data lanes**, supporting a data transmission of **up to 1.5 Gbps per lane**."*

**Feature list, § 42.3, p. 2593 [DOC]:**

- MIPI RX D-PHY compliant with **D-PHY rev 1.1**; CSI-2 host compliant with the CSI-2 spec
- **Two data lanes, each 80 Mbps – 1.5 Gbps**
- Ultra Low Power State in Escape mode
- **32-bit image interface to the ISP**
- Input formats: **RGB888 / RGB666 / RGB565, YUV422 / YUV420, RAW8 / RAW10 / RAW12**
- Error detection and correction at **PHY, packet, line and frame** level
- **EMI mitigation by data scrambling**

> **⚠ No virtual-channel support.** TRM-P4 v0.7 **p. 2593** **[DOC]**: *"ESP32-P4 does not support different virtual channels defined in the MIPI specification, so virtual channel numbers in the packet header are ignored."* **[INF]** A sensor that multiplexes two streams (e.g. image + embedded metadata, or dual-exposure HDR) onto separate VCs will have them merged. Check your sensor's VC usage before designing it in.

Dedicated pins **42–48** (`CSI_CLKP/N`, `CSI_DATAP0/N0`, `CSI_DATAP1/N1`, `CSI_REXT`), also on `VDD_MIPI_DPHY` — DS-P4 v0.7 pin table, **p. 15** and § 4.2.1.6, **p. 66** **[DOC]**.

#### ISP — DS-P4 v0.7 § 4.2.1.2, pp. 63–64 **[DOC]**

| Property | Value |
|---|---|
| **Max resolution** | **1920 × 1080** |
| Input channels | **MIPI-CSI, DVP, AXI-DMAC** (three) |
| Input formats | **RAW8, RAW10, RAW12** |
| Output formats | RAW8, **RGB888, RGB565, YUV422, YUV420** |
| Pipeline | BLC, DPC, Bayer filter, LSC, demosaic, WBG, CCM, gamma, RGB2YUV, sharpen, contrast/hue/saturation/luminance, YUV limit, YUV2RGB, crop |
| Statistics | AE, AF, AWB, histogram |

**[INF] The ISP is the reason a P4 camera board looks different from an S3 one.** On an S3, a DVP sensor's output lands in memory exactly as the sensor produced it and every correction is software. On a P4, RAW from either **MIPI-CSI or the `LCD_CAM` DVP port** can go through a hardware pipeline first. The DVP path on P4 is therefore *both* a raw `LCD_CAM` capture route **and** an ISP input — which the S3's is not.

#### DVP per target, side by side

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Bus width | 8 or 16-bit | **8 or 16-bit** | **8 or 16-bit** |
| Master RX (SoC supplies `CAM_CLK`) | ❌ slave only | ✅ | ✅ |
| Max PCLK | not stated (see § 16.2) | **< 80 MHz** 8-bit / **< 40 MHz** 16-bit | same |
| Sync scheme | HSYNC && VSYNC && H_ENABLE all high | `VH_DE_MODE_EN`: VSYNC+HSYNC+DE, or DE-only | same |
| ⚠ DE-only caveat | — | *"in this case, the YUV-RGB conversion function of camera module is not available"* — p. 1080 | same wording — p. 2302 |
| Feeds an ISP | ❌ | ❌ | ✅ |
| Destination | I2S DMA | GDMA, **internal memory** | GDMA, **internal or external memory** |

---

### 16.7 ESP32-P4 — PPA, 2D-DMA, JPEG and H.264

#### PPA (Pixel-Processing Accelerator) — TRM-P4 v0.7 Ch. 39, p. 2255

> *"PPA consists of two functional modules: scaling-rotation-mirroring (SRM) and image blending (BLEND)… PPA processes images in units of pixel block. These pixel blocks are acquired from memory through **2D-DMA**."* — § 39.1, p. 2255 **[DOC]**

| Operation | Capability | Citation **[DOC]** |
|---|---|---|
| **Rotate** | counterclockwise **0° / 90° / 180° / 270°** | § 39.3, p. 2256 |
| **Scale** | horizontal and vertical, **8-bit integer + 4-bit fractional** factor, **bilinear interpolation** | § 39.3, p. 2256; § 39.4, p. 2256 |
| **Mirror** | horizontal and vertical | § 39.3, p. 2256 |
| **Blend** | two same-size layers, **alpha-based**; alpha can be supplied by register if the layer has none; **colour-key** ranges for both layers | § 39.3, p. 2256 |
| **Colour convert** | everything is converted to **ARGB8888** internally, then back out | § 39.4, pp. 2256–2257 |
| SRM formats in/out | **ARGB8888, RGB888, RGB565, YUV422, YUV420, GRAY** | § 39.3, p. 2256 |
| BLEND foreground | **ARGB8888, RGB888, RGB565, L4, L8, A4, A8** | § 39.3, p. 2256 |
| BLEND background | ARGB8888, RGB888, RGB565, YUV422, YUV420, GRAY, L4, L8 | § 39.3, p. 2256 |
| Pseudo-colour | **CLUT** with 8-bit or 4-bit entry addresses | § 39.5.1, p. 2257 |
| ⚠ Output size limit | scaled output block **must not exceed 8191** in either axis, and must not scale to 0 — enforced by `PPA_{X,Y}DST_LEN_TOO_LARGE_ERR_ST` / `_TOO_SAMLL_ERR_ST` | Table of PPA error interrupts, pp. 2265–2266 |

> **⚠ DS-P4 v0.7 states the scaling factor backwards.** DS-P4 § 4.2.1.3, **p. 64** **[DOC]** says *"scaling factors of **4-bit integer part and 8-bit fractional part**"*. TRM-P4 § 39.3, **p. 2256** **[DOC]** says *"**8-bit integer part and 4-bit fractional part**"*. **The TRM is right**: `PPA_SRM_SCAL_ROTATE_REG` (`0x0064`, **p. 2289**) lays out `PPA_SRM_SCAL_X_INT` at bits **[7:0]**, `PPA_SRM_SCAL_X_FRAG` at bits **[11:8]**, `PPA_SRM_SCAL_Y_INT` at **[19:12]**, `PPA_SRM_SCAL_Y_FRAG` at **[23:20]** — 8 integer bits, 4 fractional bits, each axis. The error-status description at **p. 2266** corroborates it by referring to *"scaling factor is 1/16"* as the smallest step, which is 2<sup>−4</sup>. **Use the TRM figure.**

**[INF] What PPA means for LVGL.** LVGL's per-frame cost on a large panel is dominated by three things, and the P4 has silicon for all three:

| LVGL operation | Software cost on an S3 | P4 hardware |
|---|---|---|
| Alpha blending a widget/overlay over the background | per-pixel multiply-add on the CPU, from PSRAM, through the cache | **PPA BLEND** |
| Rotating the whole UI (portrait panel in landscape use, or a round display) | full-buffer transpose, cache-hostile | **PPA SRM rotate** |
| Scaling images / zoom animations | bilinear interpolation on the CPU | **PPA SRM scale**, bilinear in hardware |
| Converting RGB565 ↔ RGB888 for a 24-bit panel | per-pixel shift/mask | **PPA colour convert** *and* `LCD_CAM`'s own converter (§ 16.4) |
| Moving the result to the framebuffer | `memcpy` from PSRAM to PSRAM | **2D-DMA**, with the rectangle stride handled in hardware |

The last row is the one people underestimate: **2D-DMA understands rectangles**. `2D-MOD0` mode *"reads or writes a hb×vb macroblock starting from the (X, Y) coordinates of the HA×VA image. After the last data in each row has been read or written, the address jumps to the address of the first data in the next row"* (TRM § 8.4.1, **p. 829** **[DOC]**). A partial-area LVGL flush is exactly that access pattern, and on an S3 it costs one DMA descriptor per scanline.

⚠ **No benchmark for any of this exists in this knowledge base**, and Espressif publish none in the TRM or datasheet. The table above is a mapping of capability to workload, **not** a measured speedup. [display-interfaces.md § 10](../hardware/display-interfaces.md#10-gaps-this-guide-cannot-fill) records the same gap.

#### 2D-DMA — TRM-P4 v0.7 Ch. 8, p. 828 **[DOC]**

| Property | Value | Page |
|---|---|---|
| Interface | **one AXI master** | 828 |
| Channels | **4 memory-to-peripheral (TX) + 3 peripheral-to-memory (RX)** | 828, 829 |
| **⚠ Clients** | *"In ESP32-P4, **only JPEG Codec and PPA** support 2D-DMA."* | **828** |
| Macroblock reordering | **TX ch0 and RX ch0 only** | 829 |
| Colour-space conversion | **TX ch0–3 and RX ch0** | 829 |
| Transfer modes | **1D**, **2D-MOD0** (rectangle), **2D-MOD1** (whole image in macroblocks), **DSCR-PORT** (PPA-specific) | 829–830 |
| Memory-to-memory | **only in 1D and 2D-MOD0** | 830 |
| JPEG macroblock sizes | 8×8, 8×16, 16×16 | 830 |
| Descriptors | linked lists, **five words per descriptor**, `outlink0…3` / `inlink0…2` | 829, 830 |

> **[INF] 2D-DMA is not a general-purpose DMA you can point at the display.** It serves PPA and JPEG only. `LCD_CAM` uses **GDMA**; MIPI-DSI uses **VDMA**. Three different DMA engines feed three different display-adjacent peripherals on the same chip, and they are not interchangeable.

#### VDMA — TRM-P4 v0.7 Ch. 7, p. 774 **[DOC]**

The MIPI-DSI framebuffer engine.

| Property | Value | Page |
|---|---|---|
| Protocol | **AXI3**, **two AXI master interfaces** | 774, 776 |
| Channels | **4**, each with a **64-deep × 64-bit FIFO** | 776 |
| Handshakes with | **MIPI DSI and ISP** — and nothing else | 775 |
| Handshake map | **0 = MIPI DSI**, 1 = ISP-to-memory, 2 = memory-to-ISP | Table 7.4-1, 776–777 |
| Master reach | **Master 1** → ISP, MIPI DSI, memory. **Master 2** → memory only | 776 |
| Memory it can reach | **HP L2MEM, external flash, external RAM** | 774 |
| Flow control | VDMA **or** the peripheral | 775 |

> **⚠ Use VDMA as the DSI flow controller.** TRM § 43.4.1, **p. 2635** **[DOC]**: *"The data transfer flow controller can be configured to VDMA or DSI Bridge through `DSI_BRG_DSI_DMA_FLOW_CONTROLLER`. **It is recommended to use VDMA as the flow controller for better performance.**"* The bring-up procedure (§ 43.6.1, p. 2661) writes 0 to that field to select VDMA, and sets `DSI_BRG_DSI_RAW_BUF_ALMOST_EMPTY_THRD = 1024 − DSI_BRG_DMA_BURST_LEN` *"for better performance"*.

#### JPEG codec — DS-P4 v0.7 § 4.2.1.1, pp. 62–63 **[DOC]** (TRM Ch. 37, p. 2095)

| | Encoder | Decoder |
|---|---|---|
| Input | **RGB888, RGB565, YUV444, YUV422, YUV420, GRAY** | bitstream in YUV444/422/420/GRAY |
| Compressed formats | YUV444, YUV422, YUV420 only | same |
| Still | **up to 4K** | **up to 4K**, any resolution |
| Dynamic | **1080p@40 fps, 720p@70 fps** (excl. header encoding) | **1080p@40 fps, 720p@70 fps** (excl. header parsing) |
| Tables | four quantisation tables, 8- or 16-bit precision | four quantisation tables; **two DC + two AC Huffman tables** |
| ⚠ Output rounding | — | decoded output is padded to multiples of **8** (YUV444/GRAY), **16×8** (YUV422) or **16×16** (YUV420) — *"150 × 150 images with an output resolution of 160 × 160"* |

#### H.264 encoder — DS-P4 v0.7 § 4.2.1.5, pp. 65–66 **[DOC]** (TRM Ch. 41, p. 2336)

**Baseline profile.** Progressive input in RGB888, RGB565, YUV444, YUV422, YUV420, GRAY; **maximum 1080p@30 fps** encoding (encoding format YUV420). I- and P-frames, GOP mode and **dual-stream mode** (*"the total bandwidth of the two video image sequences to be encoded should not exceed 1080p@30fps"*). CAVLC entropy coding. Motion estimation at **½ and ¼ pixel**, search range horizontal **[−29.75, +16.75]**, vertical **[−13.75, +13.75]**. All inter partition modes 4×4 … 16×16. **Up to eight rectangular ROI regions**, each with a fixed QP or QP offset. Deblocking filter can be disabled.

**[INF]** Baseline + CAVLC + no B-frames means this is a *streaming* encoder, not an archival one — which matches the P4's positioning for camera boards. There is **no H.264 decoder**.

---

### 16.8 DMA paths and framebuffer bandwidth

**Which engine feeds which display peripheral [DOC], assembled from §§ 12.1, 16.3–16.7:**

| Peripheral | DMA engine | Notes |
|---|---|---|
| ESP32 I2S-as-LCD | I2S's own DMA channel | one per I2S direction |
| ESP32-S3 `LCD_CAM` | **GDMA** | one channel from the shared pool of 5 TX + 5 RX |
| ESP32-P4 `LCD_CAM` | **GDMA-AHB / GDMA-AXI** | internal **or** external memory |
| ESP32-P4 MIPI-DSI | **VDMA** | dedicated; handshake interface 0 |
| ESP32-P4 ISP | **VDMA** | handshake interfaces 1 and 2 |
| ESP32-P4 PPA, JPEG | **2D-DMA** | nothing else uses it |

**Where the framebuffer can live [DOC]:**

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Internal SRAM | 520 KB total | 512 KB total | **768 KB L2MEM @ 200 MHz** |
| External RAM | 8 MB QSPI PSRAM, 4 MB mapped | ≤ 32 MB mapped; OPI/QPI up to 120 MHz | in-package, **16-bit @ 250 MHz DDR** |
| **PSRAM theoretical bandwidth** | not published | not published in these terms | **16 × 2 × 250 MHz = 8 Gbit/s** (= 1 GB/s) |
| Display peripheral can DMA *directly* from PSRAM? | — | ⚠ pixel-clock notes are stated for **internal** memory (p. 1090) | ✅ notes explicitly cover **internal and external** (p. 2315) |

**Citations [DOC]:** L2MEM size and clock, PSRAM interface and the bandwidth formula — DS-P4 v0.7 § 4.1.3.1, **pp. 45–46** (*"Using the parameters of the current on-package PSRAM as an example, its maximum theoretical bandwidth is: 16 × 2 × 250 MHz = 8 Gbit/s"*). Memory totals for ESP32 and S3 — see § 13.

**[INF] The framebuffer arithmetic that follows from this.** A framebuffer is read once per frame, in full, forever, on any host-timed panel (RGB/DPI or DSI video mode):

```
bytes/frame × refresh = sustained read bandwidth
```

| Panel | bpp | Bytes/frame | At 60 Hz | Fraction of P4's 1 GB/s PSRAM ceiling |
|---|---:|---:|---:|---:|
| 800 × 800 | 16 | 1.28 MB | **76.8 MB/s** | 7.7 % |
| 1024 × 600 | 16 | 1.23 MB | **73.7 MB/s** | 7.4 % |
| 1024 × 600 | 24 | 1.84 MB | **110.6 MB/s** | 11 % |
| 1280 × 720 | 24 | 2.76 MB | **165.9 MB/s** | 17 % |
| 1920 × 1080 | 24 | 6.22 MB | **373.2 MB/s** | 37 % |

**This is derived here, not quoted.** It is the *scan-out* read only — it excludes the CPU/PPA writes that produce the frame, the cache traffic, and every other PSRAM client. **[INF]** The honest reading is that scan-out alone is comfortable at every resolution the P4's other limits allow, and that the pressure lands on the *write* side and on contention, which is exactly where PPA and 2D-DMA are aimed. It also shows why the S3, with no published PSRAM bandwidth figure and an 80 MB/s `LCD_CAM` GDMA budget (**p. 1091**), sits where it does: a single 800 × 480 RGB565 panel at 60 Hz is already **46 MB/s** of that 80.

---

### 16.9 Which target drives which panel class

**[INF] throughout this subsection** — it composes the documented limits above; Espressif do not publish a panel-class table.

| Panel class | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| **SPI / QSPI, controller has GRAM** (≤ ~400 × 400) | ✅ the natural fit | ✅ | ✅ (and often the right answer — see [display-interfaces.md § 3.1](../hardware/display-interfaces.md#31-spi)) |
| **i80 parallel, 8-bit** | ⚠ possible, costs an entire I2S; strobe ceiling ≈ 20 MHz | ✅ **< 80 MHz** | ✅ **< 80 MHz** |
| **i80 parallel, 16-bit** | ⚠ as above | ✅ **< 40 MHz** | ✅ **< 40 MHz** |
| **RGB/DPI, RGB565 16-bit** | ❌ **no sync outputs** | ✅ **< 40 MHz pixel clock** | ✅ **< 40 MHz pixel clock** |
| **RGB/DPI, RGB888 24-bit** | ❌ | ❌ bus is 8/16-bit, converter is RGB565-only | ⚠ bus exists; **no pixel-clock limit published** |
| **MIPI-DSI** | ❌ | ❌ | ✅ 2 lanes |
| **Bare e-paper (DES) parallel** | ✅ via I2S LCD mode — the Inkplate route | ✅ via `LCD_CAM` i80 | ✅ |

#### The resolution ceiling for RGB/DPI on S3 and P4

The binding constraint is the 16-bit pixel-clock limit of **< 40 MHz**. At 40 MHz, allowing ~10 % for blanking:

$$\frac{40 \times 10^6 \times 0.9}{60\ \text{Hz}} \approx 600{,}000\ \text{active pixels per frame}$$

which is **1024 × 576-ish at 60 Hz**, or **800 × 480 at 60 Hz with comfortable margin** (307,200 px ⇒ ~20 MHz). **[INF]** That is consistent with — and gives a mechanism for — the threshold the [ESP32-P4 chip record](../../components/espressif/esp32-p4/README.md) states for choosing a P4: *"a display above roughly 800 × 480"*. Above that, RGB/DPI on 16 bits runs out of pixel clock and you need DSI.

#### The resolution ceiling for MIPI-DSI on P4

Two independent limits, and **the link binds first at 24 bpp**:

```
link      = 2 lanes × 1.5 Gbps                  = 3.00 Gbit/s
DPI       = 240 MHz max DPI frequency           = 240 Mpixel/s   [TRM p. 2633, DOC]

at 24 bpp (RGB888):  3.00e9 / 24 = 125 Mpixel/s   ← link-bound
at 18 bpp (RGB666):  3.00e9 / 18 = 167 Mpixel/s   ← link-bound
at 16 bpp (RGB565):  3.00e9 / 16 = 188 Mpixel/s   ← link-bound
```

Against total frame sizes **including blanking**:

| Panel | Total px/frame (typ. blanking) | @60 Hz | RGB888 (125 Mpx/s) | RGB565 (188 Mpx/s) |
|---|---:|---:|---|---|
| 800 × 800 (Waveshare 3.4C) | 880 × 840 = 739,200 | 44.4 Mpx/s | ✅ 36 % | ✅ 24 % |
| 1024 × 600 (Espressif 7″) | ~1180 × 640 = 755,200 | 45.3 Mpx/s | ✅ 36 % | ✅ 24 % |
| 1280 × 720 | ~1650 × 750 = 1,237,500 | 74.3 Mpx/s | ✅ 59 % | ✅ 40 % |
| **1920 × 1080** | ~2200 × 1125 = 2,475,000 | **148.5 Mpx/s** | ❌ **119 % — over** | ✅ 79 % |

**[INF] So 1080p60 is reachable on the P4's DSI link at RGB565 and *not* at RGB888.** The 3.4C's blanking figures are the ones established in [display-interfaces.md § 2.2](../hardware/display-interfaces.md#22-mipi-dsi--waveshare-p4-boards-24-bpp); the 1280 × 720 and 1920 × 1080 rows use conventional CVT-ish blanking and are illustrative, not from any panel record. **None of these ceilings is stated by Espressif** — the TRM gives the lane rate and the DPI ceiling and stops. Corroborating limits elsewhere in the same silicon (**ISP max 1920 × 1080**, DS-P4 p. 63; **JPEG dynamic 1080p@40 fps**, p. 62; **H.264 1080p@30 fps**, p. 65) all land at 1080p, which is at least consistent.

---

### 16.10 Extraction record for this section

Page ranges read with `pdftotext -layout -f <first> -l <last>`, printed pages (which equal PDF page indices in all three TRMs — verified by footer):

| Document | Pages | Content |
|---|---|---|
| TRM-32 v5.8 | 415–418, 426–429 | I2S overview + signal table, I2S clock, § 22.5 Camera-LCD Controller, interrupts |
| DS-32 v5.3 | 47 | I2S/LCD signal list in the peripheral pin table |
| TRM-S3 v1.8 | 1078–1095 | `LCD_CAM` Ch. 29 in full: features, signals, clocks, format control, YUV, configuration process, pixel-clock notes, interrupts |
| DS-S3 v2.2 | 4, 52 | Features list; § 4.2.1.4 LCD and Camera Controller |
| TRM-P4 v0.7 | 774–782 | VDMA Ch. 7: features, architecture, handshake map |
| TRM-P4 v0.7 | 828–838 | 2D-DMA Ch. 8: features, architecture, transfer modes |
| TRM-P4 v0.7 | 2255–2300 | PPA Ch. 39: features, architecture, colour space, SRM, registers |
| TRM-P4 v0.7 | 2300–2316 | `LCD_CAM` Ch. 40 in full |
| TRM-P4 v0.7 | 2592–2600 | MIPI CSI Ch. 42: terminology, features, architecture |
| TRM-P4 v0.7 | 2633–2700 | MIPI DSI Ch. 43: features, bridge, host, D-PHY, clocks, timing, interrupts, programming procedures, registers |
| DS-P4 v0.7 | 44–47, 62–68 | Memory/PSRAM bandwidth; § 4.2.1.1–4.2.1.7 JPEG, ISP, PPA, LCD_CAM, H264, CSI, DSI |

**Text-layer behaviour — consistent with [§ 15](#15-extraction-notes-and-text-layer-quality), with one addition.** Prose, feature lists and register-summary tables extracted cleanly from all six documents. Two things did not:

1. **Register bit-field diagrams extract as vertical character noise**, exactly as § 15 records. This mattered here because two facts had to be read *from* register diagrams — the PPA scaling field widths (**p. 2289**) and the DSI tearing-effect bits (**pp. 2693, 2699**). In both cases the **bit-range ruler line and the prose field descriptions below the diagram extract fine**, and that was enough: the ruler gives `31 30 29 28 27 26 25 | 24 | 23 20 | 19 12 | 11 8 | 7 0` for `PPA_SRM_SCAL_ROTATE_REG`, which pins the field widths without needing the rotated labels. **No guessing was required and none was done.**
2. **Figures are unrecoverable.** ESP32 TRM Figures 22.5-2 and 22.5-3 (the LCD data-frame forms) are the only place the `WRX2_EN`/`SDX2_EN` timing difference is shown, and they contain no text. That question is therefore **still open** — see § 16.2.

**Nothing was obfuscated and no fallback to the readthedocs HTML build was needed.** The one HTML artifact held for this family (`esp32-series-datasheet-v5.3.html`) was not required.

---

## Related

- **[Display interfaces](../hardware/display-interfaces.md)** — the practical companion to [§ 16](#16-lcd-camera-and-display-peripherals): transports, framebuffer arithmetic, TE lines, LVGL, and the panels actually fitted in this library
- [ESP-IDF peripheral capabilities](esp-idf-peripheral-capabilities.md) — what the *software* guide says, and why it defers here
- [Memory and boot](memory-and-boot.md) — memory maps, boot flow, strapping, flash/PSRAM voltage, eFuse
- [Errata, practical](errata-practical.md) — which silicon bugs actually bite, per revision
- [Ecosystem and product lines](ecosystem-and-product-lines.md)
- Component records: [ESP32-U4WDH](../../components/espressif/esp32-u4wdh/README.md) · [ESP32-S3R8](../../components/espressif/esp32-s3r8/README.md) · [ESP32-P4](../../components/espressif/esp32-p4/README.md)
