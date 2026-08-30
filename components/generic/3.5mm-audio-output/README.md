# 3.5 mm stereo audio output — a *line* output, not a headphone output

- **Category:** analogue audio interface
- **Reference designator on this board:** **none.** ⚠ **No 3.5 mm jack symbol appears in the five published schematic sheets.** The DAC's analogue outputs terminate at the header `CN1`
- **Owning MCU:** **either**, arbitrated in hardware — the ESP32-S3 selects the I2S source, the ESP32-U4WDH owns the mute line. See §4
- **Research status:** the signal source, its electrical characteristics and the arbitration are fully established. The jack itself, its part, its switching contacts and any output filtering are **not in the published schematic**
- **Retrieved:** 2026-08-21; `OUTL`/`OUTR` traced end-to-end and the `CN1` termination resolved 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[DOC]** manufacturer datasheet · **[WEB]** vendor page/wiki · **[INF]** inference, reasoning given

---

## 1. ⚠ It is a line output. There is no headphone amplifier.

Waveshare's material describes a **"headphone jack"** **[WEB]**. The schematic tells a different story **[SCH]**:

- The audio source is a **PCM5100A** stereo DAC (`U12`) **[SCH sheet 5]**
- Its `OUTL` (pin 6) and `OUTR` (pin 7) go to nets `OUTL` and `OUTR`
- Those nets go to **`CN1` pins 10 and 9** **[SCH sheet 1]**
- **Nothing else is in the path. No amplifier, no buffer, no op-amp, no filter network appears on any of the five sheets**

The PCM5100A is a **line-level DAC with a differential-to-single-ended output stage**, not a headphone driver. It is specified to drive high-impedance loads (nominally into a 5 kΩ-class load). **[DOC]**

**Consequence:** this is a **line output**, appropriate for feeding an amplifier, powered speakers, or a line input. It is **not** designed to drive headphones directly.

### 1.1 What happens if you plug headphones in anyway

**[INF]**, reasoning from the PCM5100A's specifications:

| Load | Result |
|---|---|
| Line input (10–47 kΩ) | ✅ Correct use. Full level, full performance |
| High-impedance headphones (250–600 Ω) | ⚠ Will produce sound, quietly. Level and distortion both degraded |
| Typical headphones (32 Ω) | ⚠ Heavily loaded. Substantial level loss, elevated distortion, and the DAC's output stage working far outside its comfortable range |
| Earbuds (16 Ω) | ⚠ Worse still |
| Shorted | The PCM5100A has output protection, but do not rely on it |

It will make noise into headphones. It will not sound good, and it is not what the part is for. **Describe this output as a line output in anything you build.**

## 2. The output is ground-centred — do not add coupling capacitors

The PCM5100A generates a **negative rail internally** via a charge pump, and this board populates all of its supporting components **[SCH sheet 5]**:

| Pin | Name | Component |
|---:|---|---|
| 1 | `CPVDD` | from `A3V3` |
| 2 | `CAPP` | `C64` 2.2 µF |
| 3 | `CPGND` | |
| 4 | `CAPM` | (charge-pump flying capacitor pair with `CAPP`) |
| 5 | `VNEG` | `C65` 2.2 µF |

Because of that negative rail, `OUTL`/`OUTR` swing **symmetrically about ground**. That is the whole point of the PCM510xA family's architecture and it has a concrete benefit: **no DC-blocking capacitors are required, and none are fitted** **[SCH]**.

**Do not add series coupling capacitors.** You would only introduce a high-pass corner and lose bass extension, for no benefit. If you are building an interface board for `CN1`, take `OUTL`/`OUTR` straight through.

## 3. Where the jack actually is

**No jack symbol exists in the published sheets** **[SCH]**. `OUTL` and `OUTR` terminate at `CN1` pins 10 and 9 **[SCH sheet 1]** — see [generic/ph1.27-expansion-connectors §2](../ph1.27-expansion-connectors/README.md#2-pinout--resolved-sch-sheet-1-1_lcdpowerpng) for the full pinout.

**[INF]** `CN1` carries 5 V, two grounds, both USB differential pairs, S3 GPIO0, and these two audio outputs — and carries **no** I2C, SPI, UART or spare GPIO. That is precisely the signal set you would route to a **connector daughterboard** holding the USB-C receptacle and the 3.5 mm jack. The same reasoning applies to the missing USB-C receptacle ([generic/usb-c-interface §3.1](../usb-c-interface/README.md#31-the-most-likely-arrangement)) and the missing charger ([generic/charger-power-path §2.4](../charger-power-path/README.md#24-what-the-absence-probably-means)).

So the jack almost certainly exists on hardware that was not published, and **everything about it is unknown**:

| Unknown | Why it matters |
|---|---|
| Jack part number and type (3-pole TRS vs 4-pole TRRS) | A TRRS jack would suggest a microphone contact — but the board's microphone is the on-PCB PDM part, so a mic contact would be unused |
| **Whether the jack has switching contacts** | Common on 3.5 mm jacks for detecting insertion. **No detect signal reaches either MCU [SCH]**, so even if the contacts exist they are not wired to firmware |
| Series resistors, RC filtering, or ESD protection at the jack | Unknown. A well-designed line output usually has a small series resistor and an RC low-pass |
| Ground arrangement (shared sleeve, star ground) | Unknown. Matters for crosstalk and hum |
| Physical location on the device | Unknown |

**There is no headphone-detect, no jack-insertion interrupt, and no way for software to know whether anything is plugged in.**

## 4. ⚠ Which processor is driving it — the arbitration problem

This is the most consequential thing on this page, and it is a board-level issue rather than a jack-level one.

The audio path is **shared between the two MCUs** and split in an awkward way **[SCH sheet 5]**:

| Function | Owned by | Signal |
|---|---|---|
| **I2S source selection** (which MCU's I2S reaches the DAC) | **ESP32-S3 only** | GPIO0 → `I2S_SWITCH_IN` → CH445P `U18` pin 15 |
| **DAC soft-mute `XSMT`** | **ESP32-U4WDH only** | GPIO32 → PCM5100A `U12` pin 17 |

**Neither processor can produce audio alone.** The S3 chooses the source but cannot un-mute; the U4WDH can un-mute but cannot choose the source.

Three practical consequences:

1. **A source handover has to be coordinated over the inter-MCU UART**, whose protocol and even baud rate are undocumented. See [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md).
2. **If you replace the ESP32-U4WDH's firmware, drive GPIO32 high** or the board goes permanently silent — including for audio originating on the S3. This is the single most important thing to remember when writing replacement U4WDH firmware.
3. **How the S3-only `07_Audio_Test` demo gets past `XSMT` is unresolved.** Either the pin has an internal pull-up, or the stock U4WDH firmware un-mutes at boot, or the example only works with factory firmware resident. Tracked in [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md).

Additionally: **the CH445P's channel D is unconnected on both banks**, so **no MCLK reaches the PCM5100A from either processor** **[SCH]**. The DAC must run in BCK-derived clocking mode. Not a fault — the PCM5100A supports it — but easy to get wrong when configuring I2S.

The mux truth table is also unverified, because no CH445P datasheet has been obtained. See [wch/ch445p](../../wch/ch445p/README.md).

## 5. Using it from the ESP32-S3

The vendor's `07_Audio_Test` is the reference **[SRC]**:

```c
// 1. Claim the DAC by driving the CH445P mux select.
//    (Which level selects which bank is UNVERIFIED -- see wch/ch445p.)
gpio_config_t gpio_conf = {
    .pin_bit_mask = 1ULL << GPIO_NUM_0,
    .mode         = GPIO_MODE_OUTPUT,
    .pull_up_en   = GPIO_PULLUP_ENABLE,
};
gpio_config(&gpio_conf);
gpio_set_level(GPIO_NUM_0, 1);     // "give control of the PCM5100A to the S3"

// 2. I2S standard mode, TX, on I2S_NUM_1.
//    NOTE: no MCLK. .mclk = I2S_GPIO_UNUSED is correct and required.
i2s_chan_config_t tx_chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_1, I2S_ROLE_MASTER);
i2s_new_channel(&tx_chan_cfg, &tx_chan, NULL);
i2s_std_config_t tx_std_cfg = {
    .clk_cfg  = I2S_STD_CLK_DEFAULT_CONFIG(44100),
    .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT,
                                                I2S_SLOT_MODE_MONO),
    .gpio_cfg = {
        .mclk = I2S_GPIO_UNUSED,        // <-- required; no MCLK is routed
        .bclk = GPIO_NUM_39,
        .ws   = GPIO_NUM_40,
        .dout = GPIO_NUM_41,
        .din  = I2S_GPIO_UNUSED,
    },
};
i2s_channel_init_std_mode(tx_chan, &tx_std_cfg);
i2s_channel_enable(tx_chan);
```

S3 I2S pins **[SCH sheet 2]**: `BCK` = GPIO39, `WS`/`LRCK` = GPIO40, `DIN` = GPIO41. The demo runs 44.1 kHz, 16-bit.

**Volume must be done in software.** The PCM5100A on this board has no I2C control interface wired — it is the hardware-controlled variant of the family, and its `FMT`, `DEMP` and `FLT` mode pins are strapped **[SCH sheet 5]**. The vendor implements volume as a per-sample multiply **[SRC]**:

```c
float volume_factor = volume / 100.0f;
for (uint32_t i = 0; i < sample_count; i++)
    samples[i] = (int16_t)(audio_per[i] * volume_factor);
```

That works, but **do not copy the vendor's surrounding code**: it allocates and frees a 2048-byte SPIRAM buffer on every call, roughly 43 times a second at 44.1 kHz mono **[SRC]**. Scale in place, or preallocate.

**[INF]** Software volume on a 16-bit path costs resolution: attenuating by 20 dB throws away more than three bits. If you need a wide volume range with good quality, do the scaling in 32-bit and dither, or accept that quiet listening will be noisier than it needs to be. A DAC with hardware volume control would not have this problem — the PCM5100A variant fitted here does not offer one over a wired interface.

## 6. Signal quality notes

| Item | Status |
|---|---|
| DAC | PCM5100A — a genuinely good part, 106 dB SNR class **[DOC]** |
| Supply | **`3V3_DAC`, a dedicated low-noise LDO** ([sgmicro/sgm2036-3.3](../../sgmicro/sgm2036-3.3/README.md)) with a ferrite bead on its input. **This is a properly done rail split** |
| Output coupling | Direct, ground-centred, no capacitors. §2 |
| MCLK | **Absent.** BCK-derived clocking only. §4 |
| Output filtering at the jack | **Unknown** — the jack is not in the schematic |
| Ground routing to the jack | **Unknown** |
| Measured THD+N, SNR, crosstalk for this board | **Unknown.** Never published, never measured here |

**[INF]** The parts selection is good and the rail split is careful, so the ceiling here is high. Whether the board reaches it depends on the unpublished output stage and grounding, and on the software volume implementation (§5). Absent an MCLK, jitter performance depends on how cleanly the S3's I2S BCK is generated — the PCM5100A's internal PLL handles this well, which is why the omission is acceptable.

## 7. Pitfalls

1. **It is a line output, not a headphone output.** §1. This is the most common misunderstanding.
2. **Do not add DC-blocking capacitors.** §2.
3. **`XSMT` belongs to the other MCU.** §4. Replacement U4WDH firmware must drive GPIO32 high.
4. **No MCLK.** §5. `.mclk = I2S_GPIO_UNUSED` is mandatory.
5. **No jack-insertion detection.** §3.
6. **Volume is software-only, and costs bits.** §5.
7. **Which mux level selects which MCU is unverified.** §4.
8. **The jack is not in the schematic** — do not assume anything about series resistance, filtering or ESD protection at the connector. §3.

## 8. Open questions

| Question | Status |
|---|---|
| Jack part, pole count, switching contacts | **Unknown.** Not in the published schematic |
| Output filtering / series resistance at the jack | **Unknown** |
| Whether a daughterboard carries the jack | **[INF]** likely (§3), unconfirmed |
| CH445P truth table — which level selects which MCU | **Unknown.** No datasheet obtained. See [wch/ch445p](../../wch/ch445p/README.md) |
| How S3-only audio gets past `XSMT` | **Unresolved.** See [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md) |
| Measured audio performance | **Unknown** |

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — `OUTL`/`OUTR` from PCM5100A `U12`, terminating at `CN1` pins 10 and 9

## Related pages

- [texas-instruments/pcm5100a](../../texas-instruments/pcm5100a/README.md) — the DAC, its mode straps and its clocking
- [wch/ch445p](../../wch/ch445p/README.md) — the mux that decides which MCU is heard
- [sgmicro/sgm2036-3.3](../../sgmicro/sgm2036-3.3/README.md) — the dedicated low-noise rail
- [generic/ph1.27-expansion-connectors](../ph1.27-expansion-connectors/README.md) — where `OUTL`/`OUTR` actually terminate
- [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md) — the audio arbitration in full
- [Pinouts and buses](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Board schematic sheet 5 — PCM5100A `U12` with `OUTL`/`OUTR`, the charge-pump network, `XSMT`, and the CH445P mux | — | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/5_DAC.png` |
| Board schematic sheet 1 — `OUTL`/`OUTR` arriving at `CN1` pins 10 and 9; **no jack symbol** | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Board schematic sheet 2 — S3 I2S pins GPIO39/40/41 and `GPIO0` = `I2S_SWITCH_IN` | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Board schematic sheet 3 — U4WDH GPIO32 → `XSMT` | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/3_ESP32-CHIP.png` |
| PCM5100A datasheet — output architecture, load specification, charge pump | https://www.ti.com/lit/gpn/PCM5100A | 2026-08-21 | `../../texas-instruments/pcm5100a/artifacts/pcm5100a-datasheet.pdf` |
| Waveshare demo `07_Audio_Test` — `audio_bsp.c`, the I2S TX setup and software volume | — | 2026-08-21 | `.../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/examples/07_Audio_Test/` |
| ESP-IDF v5.3.2 I2S standard-mode driver | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-reference/peripherals/i2s.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
| Waveshare product page — the "headphone jack" wording | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-product-31623.html` |
| Waveshare wiki | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-wiki-current.html` |
