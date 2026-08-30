# MEMSensing MSM261D4030H1CPM — the PDM microphone

- **Category:** digital PDM MEMS microphone
- **Reference designator on this board:** `MIC1`
- **Marking in the schematic BOM field:** `MSM261D4030H1CPM`
- **Owning MCU:** **ESP32-S3 only**, on I2S0 in PDM RX mode
- **Research status:** board wiring fully established pin-by-pin; the ESP32-S3 side is fully documented. ⚠ **No manufacturer datasheet has been obtainable** — every acoustic figure (sensitivity, SNR, AOP, clock range, current) is therefore **unknown and is not guessed here**
- **Retrieved:** 2026-08-21; schematic re-read and retrieval retried 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[DOC]** manufacturer datasheet or official programming guide · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. ⚠ The datasheet problem, stated up front

**No MSM261D4030H1CPM datasheet exists in this repository, and none could be retrieved.** Attempts on 2026-08-21 and again on 2026-08-23, with a desktop Chrome User-Agent, a WhatsApp link-preview User-Agent and an `lcsc.com` referrer:

| Endpoint | Result |
|---|---|
| `datasheet.lcsc.com/lcsc/1811081617_MEMSensing-MSM261D4030H1CPM_C74250.pdf` | HTTP 200 but `text/html`, ~906 KB anti-bot interstitial. Identical under both User-Agents. **Rejected — never saved as `.pdf`** |
| `wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/...` | HTTP 200, `text/html`, 91 bytes, a `<script>` redirect stub |
| `mouser.com/datasheet/2/MSM261D4030H1CPM.pdf` | HTTP 200, `text/html`, ~14 KB |
| `memsensing.com/product/detail/id/16.html`, `/en/product.html` | HTTP 404 — the manufacturer reorganised its CMS |
| `memsensing.com/Uploads/file/20200708/*.pdf` | HTTP 403 |
| `memsensing.com/` homepage crawl | HTTP 200, but the link set contains **no PDFs and no per-part product pages** |
| Wayback availability API / CDX | HTTP 429 and a 40 s timeout respectively. **Worth one more attempt from a different network** |

Full detail is recorded in [component-download-failures.txt](../../../component-download-failures.txt).

**Consequence.** The following are all **UNKNOWN** and must not be quoted from anywhere else in this repository, because nothing here establishes them:

- Sensitivity (dBFS at 94 dB SPL)
- Signal-to-noise ratio (dB(A))
- Acoustic overload point (AOP, dB SPL)
- Supply current, and sleep/standby current
- Supported PDM clock frequency range, and the low-power/sleep clock thresholds
- Frequency response, directionality, port orientation (top-port vs bottom-port)
- Package dimensions and footprint
- Operating temperature range

**Do not substitute figures from a similar-sounding part.** MEMSensing's MSM261 family spans multiple sensitivity and SNR grades that differ only in the trailing characters of the part number. A number lifted from `MSM261S4030H0` is not a number about `MSM261D4030H1CPM`.

### 1.1 What the part number probably encodes

Purely as an aid to future retrieval, **[INF]** and explicitly not a specification:

| Fragment | Likely meaning |
|---|---|
| `MSM261` | MEMSensing digital microphone series |
| `D` | **D**igital PDM output (the `S` variants in this family are I2S/TDM; `A` variants are analog) |
| `4030` | Package footprint, most likely 4.0 × 3.0 mm |
| `H1` | Sensitivity/SNR grade code |
| `CPM` | Package/port style suffix |

The `D` = PDM reading is the one corroborated by the board: the part is wired to the ESP32-S3's PDM RX pins and driven with `driver/i2s_pdm.h` **[SCH, SRC]**. The rest is pattern-matching on the family's naming and should be treated as a lead, not a fact.

## 2. Exact wiring on this board **[SCH, sheet 4 `4_OTHER.png`]**

`MIC1` is drawn as an 8-pin symbol. Every pin is accounted for:

| Pin | Name | Connected to | Detail |
|---:|---|---|---|
| 1 | `VDD` | **3V3** | Decoupled by `C19` 100 nF **and** `C20` 10 µF, both local to the mic |
| 2 | **`L/R`** | **GND** | **Tied low.** This is the channel-select strap — see §3 |
| 3 | `CLK` | `PDM_MIC_SCK` → **ESP32-S3 GPIO45** | PDM clock, driven by the S3 |
| 4 | `DATA` | `PDM_MIC_DATA` → **ESP32-S3 GPIO46** | PDM bitstream, driven by the mic |
| 5 | `GND` | GND | |
| 6 | `GND` | GND | |
| 7 | `GND` | GND | |
| 8 | `GND` | GND | |

Points worth noting:

- **Four dedicated ground pins.** Typical of MEMS microphone packages, where the ground pins double as the acoustic seal and the shield.
- **Two decoupling capacitors, 100 nF and 10 µF, both local.** This is more generous than the single 100 nF you often see, and it is the right call: PDM microphones draw current in bursts synchronous with the clock, and supply noise lands directly in the audio band.
- **The 3V3 rail is the main board rail**, from the `TLV62569DBVT` buck — *not* the quieter `3V3_DAC` LDO rail that feeds the PCM5100A **[SCH sheets 1 and 5]**. See §6.
- **There is no `SELECT`, `WS`, `SD` or chip-enable pin.** The interface is two wires plus a strap. There is no I2C address and no register interface — **the microphone is not configurable at all.**
- **GPIO45 and GPIO46 are ESP32-S3 strapping pins.** GPIO45 is `VDD_SPI` voltage select and GPIO46 is `ROM message print` control. They are sampled at reset only, and driving them afterwards is fine — but see §5 pitfall 6.

## 3. The `L/R` strap, and why it is the single biggest gotcha

`L/R` is tied to **GND** **[SCH sheet 4]** — the ground symbol sits directly on the pin-2 net, adjacent to the `PDM_MIC_SCK` label.

For essentially every PDM microphone, the convention is:

| `L/R` | Mic drives `DATA` during | Conventionally called |
|---|---|---|
| **GND (this board)** | the **low** half of the `CLK` cycle | the **left** channel |
| VDD | the **high** half of the `CLK` cycle | the **right** channel |

This exists so two microphones can share one clock and one data line, each driving its own half-cycle, giving stereo on two wires. **This board has one microphone**, so the strap's only job is to decide which half-cycle the S3 must sample.

### 3.1 What this means for ESP-IDF configuration

ESP-IDF's PDM RX slot configuration has a `slot_mask` field taking `I2S_PDM_SLOT_LEFT`, `I2S_PDM_SLOT_RIGHT` or `I2S_PDM_SLOT_BOTH`, and the GPIO configuration has an `invert_flags.clk_inv` **[DOC]**. Espressif's own note is: *"The right slot is received first in stereo mode. To switch the left and right slots in the buffer, please set the `i2s_pdm_rx_gpio_config_t::invert_flags::clk_inv` to force invert the clock signal."* **[DOC]**

**The failure mode when this is wrong is silence, or near-silence — not an error.** The DMA fills, `i2s_channel_read()` returns `ESP_OK`, and the buffer contains the *other* half-cycle, which this microphone is not driving. You get a floating-line pattern that reads as very quiet noise or a DC offset.

If you get no audio, this is the **first** thing to change, before you suspect the microphone, the clock rate or your gain. There are only four combinations:

1. `slot_mask = I2S_PDM_SLOT_LEFT`, `clk_inv = false` ← try first; matches `L/R` = GND
2. `slot_mask = I2S_PDM_SLOT_RIGHT`, `clk_inv = false`
3. `slot_mask = I2S_PDM_SLOT_LEFT`, `clk_inv = true`
4. `slot_mask = I2S_PDM_SLOT_RIGHT`, `clk_inv = true`

**Note that the vendor demo does not set `slot_mask` at all** — it uses `I2S_PDM_RX_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_MONO)` and accepts whatever default that macro carries **[SRC]**. Since the demo is reported to work, that default evidently matches `L/R` = GND on ESP-IDF 5.3.2 — but **the default is an implementation detail of a version-specific macro and it has changed across ESP-IDF releases.** If you upgrade IDF and the microphone goes quiet, set `slot_mask` explicitly and stop relying on the default. That is the specific gotcha to remember from this page.

## 4. The PDM-to-PCM path on the ESP32-S3

### 4.1 Peripheral constraints **[DOC, ESP-IDF v5.3.2 I2S guide]**

| Constraint | Value | Why it matters here |
|---|---|---|
| PDM RX is available on **I2S0 only** | ESP32-S3 | You do not get to choose the port. The vendor demo correctly uses `I2S_NUM_0` for RX and `I2S_NUM_1` for the DAC TX **[SRC]** |
| PDM data width is **fixed at 16-bit** | — | `I2S_DATA_BIT_WIDTH_16BIT`. Requesting 24 or 32 is an error |
| Signals required | `CLK` + `DIN` only | No WS, no BCLK. Matches the two-wire interface |
| Down-sampling modes | `I2S_PDM_DSR_8S` → **Fpdm = sample_rate × 64**<br>`I2S_PDM_DSR_16S` → **Fpdm = sample_rate × 128** | This is how you control the actual clock on GPIO45. See §4.2 |
| Max data lines in PDM RX | 4, i.e. up to 8 mics | Irrelevant here — one mic, one line |
| **PDM full-duplex is not supported** | — | PDM TX and PDM RX have different clocks. Not a problem on this board: the output path is standard-mode I2S to a PCM5100A, not PDM |
| Clock sources | `I2S_CLK_SRC_DEFAULT` (PLL) or `I2S_CLK_SRC_PLL_160M` | Default is fine |

The hardware does the sinc decimation for you. **You do not need to write a CIC filter**; `i2s_channel_read()` hands back signed 16-bit PCM.

### 4.2 The clock rate you are actually generating

This is the number to reason about, because it is the one constrained by the (unknown) microphone specification.

```
Fpdm = sample_rate × 64      with I2S_PDM_DSR_8S  (the default)
Fpdm = sample_rate × 128     with I2S_PDM_DSR_16S
```

Applied to the vendor demo's chosen rate, and to rates you might prefer:

| Sample rate | `DSR_8S` → Fpdm | `DSR_16S` → Fpdm | Comment |
|---:|---:|---:|---|
| 8 kHz | 512 kHz | 1.024 MHz | **`DSR_8S` at 512 kHz is very likely below the mic's minimum.** See below |
| 16 kHz | 1.024 MHz | 2.048 MHz | The classic voice/ASR rate. Both plausible |
| 22.05 kHz | 1.4112 MHz | 2.8224 MHz | |
| **44.1 kHz** | **2.8224 MHz** | 5.6448 MHz | **What the vendor demo uses** (`EXAMPLE_PDM_RX_FREQ_HZ 44100`, default DSR) **[SRC]**. 2.8224 MHz is squarely in the normal PDM band |
| 48 kHz | 3.072 MHz | 6.144 MHz | 3.072 MHz is a very standard PDM rate |

**The gotcha at low sample rates.** Almost all PDM microphones specify a *minimum* clock frequency, typically around 1 MHz, below which they either mute, enter a low-power mode with degraded SNR, or produce garbage. Many also have a *maximum* around 3.25–4.8 MHz. **This board's microphone has no published range**, so:

- At 44.1 kHz / `DSR_8S` you are at **2.8224 MHz**, which is the rate the vendor validated. **This is the safe configuration.**
- If you want **16 kHz** for speech (and you probably do — it halves the data rate and every ASR engine wants it), do **not** naively set `sample_rate = 16000` with the default `DSR_8S`, because that gives **1.024 MHz**, right on the typical minimum-clock boundary. Either:
  - set `dn_sample_mode = I2S_PDM_DSR_16S` to get **2.048 MHz** at 16 kHz, or
  - keep the mic at 44.1 kHz / 2.8224 MHz and **downsample in software**, which is what we would recommend since it is the only configuration with any empirical support on this board.

Set the mode explicitly rather than relying on the macro default:

```c
i2s_pdm_rx_config_t cfg = {
    .clk_cfg = I2S_PDM_RX_CLK_DEFAULT_CONFIG(16000),
    ...
};
cfg.clk_cfg.dn_sample_mode = I2S_PDM_DSR_16S;   // -> 2.048 MHz, not 1.024 MHz
```

**Verify the actual clock on GPIO45 with a scope before shipping.** It is one probe and it removes the largest remaining unknown on this page.

### 4.3 What the vendor demo does **[SRC]**

`Arduino/examples/07_Audio_Test/audio_bsp.c` is the only microphone code in the archive. It builds a straight PDM-in → I2S-out loopback:

```c
#define EXAMPLE_PDM_RX_FREQ_HZ  44100

i2s_chan_config_t rx_chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
i2s_new_channel(&rx_chan_cfg, NULL, &rx_chan);
i2s_pdm_rx_config_t pdm_rx_cfg = {
    .clk_cfg  = I2S_PDM_RX_CLK_DEFAULT_CONFIG(EXAMPLE_PDM_RX_FREQ_HZ),
    /* The data bit-width of PDM mode is fixed to 16 */
    .slot_cfg = I2S_PDM_RX_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT,
                                               I2S_SLOT_MODE_MONO),
    .gpio_cfg = {
        .clk = (gpio_num_t)45,
        .din = (gpio_num_t)46,
        .invert_flags = { .clk_inv = false },
    },
};
i2s_channel_init_pdm_rx_mode(rx_chan, &pdm_rx_cfg);
i2s_channel_enable(rx_chan);
```

and then a task that reads 2048 bytes at a time and pushes them straight to the DAC:

```c
static void i2s_adc_dac_loop_task(void *arg) {
    int16_t *r_buf = (int16_t *)calloc(1, 2048);
    size_t r_bytes = 0;
    for (;;) {
        if (i2s_channel_read(rx_chan, r_buf, 2048, &r_bytes, 1000) == ESP_OK) {
            bsp_i2s_write(r_buf, 2048, &r_bytes);
        }
    }
}
```

Three observations:

1. **It is mono at 44.1 kHz**, matching the DAC's TX rate exactly, which is why the loopback needs no resampling.
2. **`audio_gpio_init()` drives GPIO0 high before anything else**, with the comment *"把PCM5100A的控制权给到ESP32S3"* — "give control of the PCM5100A to the ESP32-S3". That is the CH445P audio mux select. The microphone path itself does not need it; the *playback* half of the loopback does. See [Pinouts and buses → Audio arbitration](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md#audio-arbitration-ch445p-u18).
3. **The write path allocates and frees a 2048-byte SPIRAM buffer on every iteration** (`heap_caps_malloc(len, MALLOC_CAP_SPIRAM)` … `heap_caps_free`) just to apply a volume scale. At 44.1 kHz mono that is ~43 allocations per second. Do not copy that pattern; scale in place or use a preallocated buffer.

### 4.4 Sizing the DMA, if you go beyond the demo

Espressif's own procedure **[DOC]**, applied to this microphone:

```
dma_buffer_size = dma_frame_num × slot_num × data_bit_width / 8   (must be <= 4092)
interrupt_interval = dma_frame_num / sample_rate
dma_desc_num > polling_cycle / interrupt_interval
recv_buffer_size > dma_desc_num × dma_buffer_size
```

For mono 16-bit at 44.1 kHz, `slot_num × data_bit_width / 8` = 2, so `dma_frame_num ≤ 2046`. Choosing `dma_frame_num = 1024` gives a 2048-byte DMA buffer and a 23.2 ms interrupt interval — comfortable for a UI-driven read loop. Register `on_recv_q_ovf` via `i2s_channel_register_event_callback()` during bring-up; a silent overflow is otherwise indistinguishable from a glitchy microphone.

### 4.5 Libraries and versions

| Option | Version | Where | Notes |
|---|---|---|---|
| ESP-IDF `driver/i2s_pdm.h` | new driver, ESP-IDF ≥ 5.0; board demos build on **5.3.2** | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/i2s.html | **Use this.** It is what the vendor demo uses |
| ESP-IDF legacy `driver/i2s.h` | deprecated | — | Cannot coexist with the new driver in one project. Do not start new work on it |
| Arduino-ESP32 `I2S` class | 3.x | https://github.com/espressif/arduino-esp32 | Arduino-ESP32 3.x is built on IDF 5.x and exposes PDM. The vendor's own "Arduino" example bypasses it and calls the IDF driver directly **[SRC]** — follow their lead |
| ESP-SR / ESP-ADF | — | https://github.com/espressif/esp-sr | If you want wake-word or ASR. **Note ESP-SR's models generally expect 16 kHz mono** — see the §4.2 clock discussion before you set 16 kHz |

## 5. Pitfalls

1. **Silence with no error → check `slot_mask`/`clk_inv` first.** §3.1. This is the number one failure.
2. **Do not set 16 kHz with the default down-sample mode.** §4.2. 1.024 MHz may be below the mic's minimum clock, and you have no datasheet to check against.
3. **Do not assume any acoustic number.** §1. If you need sensitivity or SNR figures for a gain-staging calculation, **measure them** with a reference source rather than quoting a similar part.
4. **PDM RX is I2S0 and only I2S0.** If you also want a second standard-mode input, it must go on I2S1.
5. **You cannot mute or power down the microphone.** There is no enable pin **[SCH]**. Stopping the clock (`i2s_channel_disable()`) is the only lever, and what the microphone does with a stopped clock is undocumented. For privacy-sensitive applications this is a real limitation: **there is no hardware mute on this board.**
6. **GPIO45 and GPIO46 are ESP32-S3 strapping pins** (`VDD_SPI` voltage select and ROM-message-print control). They are only sampled at reset, so using them as PDM signals afterwards is legitimate and is what the vendor does. But be aware that if you ever hold GPIO45 in an unexpected state *through a reset* — for instance by leaving a bench probe or a pull-up on it — you can change the `VDD_SPI` voltage selection and fail to boot. Do not attach permanent external pull resistors to either pin.
7. **PDM microphones are sensitive to supply noise in-band.** This one runs from the main 3V3 buck rail, not the audio LDO. §6.
8. **Acoustic port orientation and the enclosure.** Whether this part is top-port or bottom-port is **unknown**, and so is where the enclosure's sound hole is. If you are designing a replacement enclosure, do not assume; MEMS mics need a sealed, correctly sized port and a gasket, and getting the acoustic path wrong costs far more SNR than any firmware choice.
9. **There is no automatic gain control anywhere in this path.** The mic outputs a fixed-sensitivity bitstream and the S3 decimates it. All level management is yours, in software.

## 6. Power and noise

| Item | Value | Evidence |
|---|---|---|
| Supply | **3V3**, the main board rail from the `TLV62569DBVT` buck | [SCH sheets 1, 4] |
| Local decoupling | `C19` 100 nF + `C20` 10 µF | [SCH sheet 4] |
| Supply current | **Unknown** | no datasheet |
| Is it on the quiet audio rail? | **No** | [SCH] |

The board has two 3.3 V domains: `3V3` (switching buck, feeds the S3, the display, the radios, the SD card and this microphone) and `3V3_DAC` (a low-noise `SGM2036-3.3` LDO, feeding only the PCM5100A and the CH445P) **[SCH sheets 1, 5]**. **The microphone is on the noisy one.**

That is a defensible design choice — the mic's own PDM modulator has substantial supply rejection and the 10 µF local capacitor helps — but it means microphone noise floor is coupled to what the rest of the board is doing. **[INF]** If you are chasing a noise floor, the things most likely to show up in the recording are the display backlight PWM (50 kHz on GPIO47, [ao3400a](../../alpha-and-omega-semiconductor/ao3400a/README.md)), Wi-Fi TX bursts, and the buck's own switching ripple. All three are above the audio band, but their *envelopes* are not, and envelope modulation aliases down. Test by recording silence with the backlight off and the radio idle, then re-enabling each.

## 7. Open questions

| Question | Status |
|---|---|
| Sensitivity, SNR, AOP, frequency response | **Unknown.** §1. No datasheet obtainable |
| Supported PDM clock range, and low-power-mode threshold | **Unknown.** §1. The 2.8224 MHz used by the vendor demo is the only rate with empirical support |
| Supply current | **Unknown** |
| Top-port or bottom-port; package dimensions | **Unknown** |
| What the `H1` and `CPM` suffixes select | **Unknown.** §1.1 is inference only |
| Whether `I2S_PDM_RX_SLOT_DEFAULT_CONFIG`'s default `slot_mask` will stay correct across IDF versions | **Not guaranteed.** §3.1. Set it explicitly |
| Fitted date code / lot | **Unknown** |

Closing the first four requires either a MEMSensing datasheet (try the Wayback CDX index again from a different network — see [component-download-failures.txt](../../../component-download-failures.txt)) or acoustic measurement against a calibrated reference.

## 8. Alternatives

If you are respinning rather than programming, and you want a part you can actually get a datasheet for:

| Part | Notes |
|---|---|
| Knowles SPK0641HT4H-1 | PDM, well documented, widely stocked |
| TDK/InvenSense ICS-41350, T5837 | PDM, published sensitivity/SNR/AOP, application notes on port design |
| Infineon IM69D130 | PDM, 69 dB(A) SNR, 130 dB AOP — the choice when dynamic range matters |
| STMicroelectronics MP34DT06J | PDM, very common, good documentation |
| Any I2S/TDM MEMS mic | Higher pin count, but avoids the PDM clock-range question entirely. Would need a WS line this board does not route |

None of these are drop-in without knowing this part's footprint and port style, both of which are unknown.

## Manufacturer

**MEMSensing** — see the [MEMSensing documentation-sourcing guide](../../../vendors/memsensing/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `MIC1`, ESP32-S3 I2S0 PDM RX on GPIO45 (CLK) / GPIO46 (DATA)

## Related pages

- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)
- [texas-instruments/pcm5100a](../../texas-instruments/pcm5100a/README.md) — the output half of the vendor's loopback demo
- [wch/ch445p](../../wch/ch445p/README.md) — the audio mux the demo has to set before playback works
- [texas-instruments/tlv62569dbvt](../../texas-instruments/tlv62569dbvt/README.md) — the buck supplying this microphone's 3V3
- [component-download-failures.txt](../../../component-download-failures.txt) — the full retrieval log for the missing datasheet

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Board schematic sheet 4 (`MIC1` symbol, `L/R` to GND, `C19`/`C20`) | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/4_OTHER.png` |
| Board schematic sheet 2 (`PDM_MIC_SCK` → GPIO45, `PDM_MIC_DATA` → GPIO46) | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Waveshare demo `07_Audio_Test` — `audio_bsp.c`, `user_config.h` | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/07_Audio_Test/` |
| ESP-IDF v5.3.2 I2S driver, PDM RX section — source of every constraint in §4.1 and §4.2 | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/i2s.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
| ESP32-S3 Technical Reference Manual (I2S/PDM chapter) | https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-technical-reference-manual.pdf` |
| ESP32-S3 datasheet (GPIO45/GPIO46 strapping behaviour) | https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` |
| Distributor datasheet endpoint — **failed, returns HTML** | https://datasheet.lcsc.com/lcsc/1811081617_MEMSensing-MSM261D4030H1CPM_C74250.pdf | 2026-08-23 | none. See [component-download-failures.txt](../../../component-download-failures.txt) |
| MEMSensing corporate site — **no per-part pages, no PDFs** | http://www.memsensing.com/ | 2026-08-23 | — |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |

## Artifacts

**No local MSM261D4030H1CPM PDF exists**, because every retrieval endpoint serves HTML or 403/404. **No HTML was ever saved with a `.pdf` extension.** Every attempt, with the exact URL, User-Agent, HTTP status and content type, is logged in [component-download-failures.txt](../../../component-download-failures.txt).
