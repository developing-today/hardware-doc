# Cardputer ADV — performance

> Snapshot **2026-09-04**. **No benchmark was run by this session, and no independent
> measurement of any Cardputer was found anywhere during this pass.** Everything below is a
> vendor claim, a silicon specification, a configured value read from source, or a labelled
> estimate. Nothing is a measurement.

## Silicon ceiling

| Item | Value | Class |
|---|---|---|
| CPU | Xtensa LX7 **dual-core @ 240 MHz** | silicon |
| SRAM | **512 KB** | silicon |
| **PSRAM** | **none** — `ESP32-S3FN8` is flash-in-package, no PSRAM die | **silicon — the binding constraint** |
| Flash | 8 MB, in package, quad SPI | silicon |
| ROM | 384 KB | silicon |
| Vector/AI extensions | LX7 SIMD present on S3 | silicon |
| Radio | 2.4 GHz Wi-Fi b/g/n, BLE 5 | silicon |
| CPU frequency as shipped | 240 MHz (`CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ_240=y`) | source |

## Configured throughputs

| Path | Value | Source |
|---|---|---|
| Display SPI write | **40 MHz** | M5GFX `bus_cfg.freq_write = 40000000` |
| Display SPI read | 16 MHz | M5GFX `freq_read = 16000000` |
| Display SPI (Bruce/TFT_eSPI) | **20 MHz** | Bruce `-DSPI_FREQUENCY=20000000` |
| Serial upload | **1 500 000 baud** | vendor PlatformIO profile |
| GNSS UART (Cap LoRa) | 115 200 8N1 | Mesh Kit spec, factory firmware |
| I²C internal | not specified; M5GFX probes at 100 kHz | source |
| Backlight PWM | 256 Hz, LEDC ch 7 | M5GFX `_set_pwm_backlight(38, 7, 256, false, 16)` |

40 MHz over a 3-wire SPI to a 240 × 135 × 16 bpp panel is ~518 kbit per full frame, so the bus
alone permits roughly **77 full-screen updates per second** in theory. **Actual frame rate was
not measured** and will be dominated by rendering, not by the bus.

## Memory budget — the number that matters

| Consumer | Bytes | % of 512 KB |
|---|---|---|
| Single 240×135×16 bpp framebuffer | 64 800 | 12.7 % |
| Double buffered | 129 600 | 25.3 % |
| Wi-Fi + LWIP (typical) | ~50 000–80 000 | 10–16 % |
| NimBLE | smaller than Bluedroid; why the factory firmware uses it | — |
| TLS session | tens of KB | — |

Three independent pieces of evidence that this is the real limit:

1. Meshtastic's ADV variant compiles with **`-DOLEDDISPLAY_REDUCE_MEMORY`**.
2. Bruce ships a **`-DLITE_VERSION=1`** flag explicitly "to save space".
3. The Meshtastic-client author (r/CardPuter, **2026-08-01**, firsthand engineering account):
   *"the ESP32-S3 here has no PSRAM, so a full Unicode font cannot live in RAM. It ships as its
   own 2.16 MB flash partition — 68,608 fixed-size records, one per codepoint, so a glyph lookup
   is arithmetic rather than an index search — and the partition is memory-mapped, so rendering
   Cyrillic, CJK or Greek costs no heap at all."*

That third item is the most useful performance datum in this entire record, because it names the
constraint, the workaround and the cost.

Also relevant: `engneer-hamachan/area512` — *"A self-contained Ruby & Python development
environment for the **512KB** M5Stack Cardputer"* — is named after the limit.

## Power — vendor claims

At **DC 4.2 V**, from the ADV product page. **Conditions (backlight level, CPU state, radio
duty cycle) are not stated.**

| Condition | Current |
|---|---|
| Standby, power switch OFF | **0.23 µA** |
| Operating | 120.2 mA |
| Wi-Fi | 132.3 mA |
| BLE | 154.6 mA |

⚠ **BLE reading higher than Wi-Fi is anomalous** and suggests the three figures were taken under
different display or CPU conditions. Recorded in [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

**Derived runtime, clearly labelled an estimate:** 1750 mAh ÷ 132.3 mA ≈ **13.2 h** Wi-Fi,
÷ 154.6 mA ≈ **11.3 h** BLE, at the vendor's numbers and ignoring converter efficiency, cell
derating and whatever backlight state the measurement used. Do not quote these as battery life.

**Cross-generation comparison is not possible.** The v1.1 page publishes entirely different
conditions (*IR transmission mode 148.07 mA, key mode 138.93 mA*, sleep 0.15 µA) and the v1.0 a
third set (255.6 mA IR, 165.7 mA key, 0.26 µA sleep). Three products, three measurement
protocols. Any "the ADV is more efficient" claim built from these is unsupported.

## Audio

| Item | Value | Class |
|---|---|---|
| Speaker | 8 Ω, **1 W** | vendor |
| Amplifier | NS4150B mono class-D | schematic |
| Mic SNR | **65 dB** | vendor |
| Codec | ES8311, I²S slave, **no MCLK** (BCLK-derived) | schematic + source |
| Sample rates achieved | **not measured** | — |
| THD, output level, latency | **not measured, none published** | — |

## Radio

Nothing measured, nothing published. M5Stack claims *"optimized antenna design for better
reception"* for the Stamp-S3A versus the StampS3, and the two Stamp schematics do show different
matching networks — but **no sensitivity, throughput or range figure exists** for any Cardputer
in any source found. Community antenna mods (`henriquesebastiao/external-cardputer-antenna`)
likewise carry no measurements.

The Cap LoRa-1262's radio figures (+22 dBm, −147 dBm sensitivity, up to 300 kbps) belong to the
[Cap board's record](../cap-lora-1262/README.md), not to the host.

## Thermal

Operating range **0 – 40 °C** (vendor). No thermal measurement, no throttling report, no
sustained-load characterisation found. The device is a sealed plastic case with a 1 W amplifier
and a 240 MHz dual-core part; sustained full-load thermal behaviour is **unknown**.

## What would make this section useful

An owner with a bench supply and a scope could produce, in an afternoon, the four numbers that
are missing everywhere: current at a stated backlight level, sustained frame rate with M5GFX,
free heap after `M5Cardputer.begin()` + Wi-Fi, and audio output level into 8 Ω. None of those
exists publicly for the ADV as of 2026-09-04.
