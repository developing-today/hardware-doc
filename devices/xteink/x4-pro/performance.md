# Xteink X4 Pro — performance

> **Nothing was measured.** Not by this session, and not by anyone whose results
> were published. Retrieved **2026-09-04**.

## The only quantitative figures that exist

| Quantity | Value | Status |
|---|---:|---|
| **OEM display SPI clock** | **5 MHz** (`SPISettings 0x4C4B40`) | **[DUMP]** recovered constant — a hard fact about the stock firmware |
| FreeInk display SPI clock | **20 MHz** | developer-chosen; SSD1677 datasheet write maximum |
| Frontlight PWM (stock 7.0.8) | **25 kHz, 10-bit**, LEDC ch4/ch5 | **[DUMP]** recovered |
| Frontlight PWM (bring-up dump) | 10 kHz | **[DUMP]** — an older image |
| SDMMC | 1-bit, slot 1, **40 MHz** | board profile |
| I²C | 400 kHz | board profile |

## The most actionable performance finding in the subject

**The OEM clocks its own panel at 5 MHz when the controller is rated for 20.**

That is a **4× margin left on the table** for RAM writes, in the vendor's own
shipping firmware, on the flagship model. The FreeInk SDK's comment is
matter-of-fact about it:

> "displaySpiHz: 20 MHz, matching the X4's default. **The OEM clocks the panel at
> only 5 MHz** (`SPISettings 0x4C4B40`), but the SSD1677 handles far more (X4 runs
> 20, de-link 40), so 20 MHz is well in spec and gives noticeably faster RAM
> writes. Drop back to 5 MHz if artifacts appear."

**"Noticeably faster" is not a measurement.** No before/after timing was published.
The escape hatch in the last sentence is worth taking seriously: nobody has
characterised whether every X4 Pro panel is stable at 20 MHz.

## A second OEM inefficiency

The stock `INIT` routine issues SW RESET `0x12` and then a **fixed `delay(10)` —
not a BUSY-wait** (**[DUMP]**, IROM `0x4201a568`). It works, but it is a timing
assumption rather than a handshake: on a slow-starting controller it is a race,
and on a fast one it wastes time. Latent rather than active.

## Borrowed figures — and why they are borrowed

The only plane-write timings in this tree are for the **[X4](../x4/performance.md)**:
~**38 ms** at 20 MHz, ~**19 ms** at 40 MHz. Same controller family, **same
resolution (800×480)**, different SoC and different board.

They are **indicative for the X4 Pro, not measurements of it.** The X4 Pro runs
the same 20 MHz clock on the same pixel count, so ~38 ms is a reasonable
expectation — but the S3's DMA and PSRAM behaviour differ, and nobody has checked.

## What has never been measured

| Quantity | Note |
|---|---|
| **Battery capacity** | **Unknown.** No teardown exists. The X3 is 650 mAh; the Pro is unmeasured |
| **Runtime** | No figure anywhere |
| **Sleep current** | Never measured. The SDK explicitly flags it: the sleep path drives the active-low enables to their off level, and *"worth a power-draw check"* |
| Active current | Never measured |
| Page-turn latency, end to end | Never measured — waveform time dominates and is unquantified |
| Frontlight brightness / CCT range | Never measured |
| SDMMC throughput | Never measured |
| Wi-Fi / BLE throughput, range, coexistence | Never measured |
| Touch latency or report rate | Never measured |
| Boot time | Never measured |

## The measurement attempt that produced nothing

The only person known to have set out to instrument this board family attached a
**Nordic Power Profiler Kit II** to an **X3** in July 2026 and **never published
results** ([r/xteinkereader `1uksv6s`](https://old.reddit.com/r/xteinkereader/comments/1uksv6s/)).
Nobody has attempted it on an X4 Pro.

## Where the X4 Pro should be structurally faster than the C3 models

Reasoning, not measurement:

| Advantage | Why |
|---|---|
| **8 MB PSRAM** | Multi-buffer rendering and damage-window partial refresh become possible. [`goodyttoor/inkback-freeink-sdk`](https://github.com/goodyttoor/inkback-freeink-sdk) implements exactly this — *"InkMotion (PSRAM multi-buffer, damage windows, ghost budget) and X4 Pro display work"* |
| **Native SDMMC, dedicated pins** | The card does not contend with the display bus, unlike the C3 devices where both share SCLK/MOSI |
| **Dual-core Xtensa LX7 at up to 240 MHz** | vs a single RISC-V core at 160 MHz |
| **No OTA out-of-memory** | The documented C3 failure mode does not apply |

**None of this is quantified.** It is the reason the X4 Pro is the ecosystem's
"design floor", but no benchmark supports it.

## Honest summary

**Two recovered firmware constants and one borrowed timing.** Every figure a buyer
or developer would want — battery life, refresh latency, sleep current — is
**unmeasured by anyone**, on the family's flagship.
