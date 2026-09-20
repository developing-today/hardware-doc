# WS2812 — addressable RGB LED

> Schematic value string on the M5Stack Stamp-S3 and Stamp-S3A: **`WS2812`** exactly.
> Record created **2026-09-04**. Manufacturer conventionally **Worldsemi** (世微 / WorldSemi
> Co., Ltd), which originated the family; the part is widely second-sourced and the exact
> package variant on these modules is **not established** — see *Gaps*.

## Function

A single-wire addressable RGB LED: a 24-bit (GRB) shift register, a constant-current driver and
three LED dice in one package. Data enters on `DI`, the first 24 bits are consumed, and the
remainder is retransmitted on `DO` — so devices chain without any addressing.

Timing is encoded in pulse width at roughly 800 kbit/s and is tight enough that bit-banging is
unreliable under interrupts; on ESP32 the **RMT** peripheral is the normal driver.

## Key capabilities

| Property | Value |
|---|---|
| Interface | single-wire, ~800 kbit/s, self-clocked |
| Colour order | **GRB**, 8 bits each |
| Supply | 3.3 V on these modules (many WS2812 variants specify 3.5–5.3 V — see *Gaps*) |
| Pins | `VDD`, `GND`, `DI`, `DO` — 4 |
| Reset | a low period of ≳ 50 µs latches the frame |

## Pinout as drawn on the M5Stack Stamp modules

| Pin | Name | Stamp-S3 v0.2 | Stamp-S3A v0.3.3 |
|---|---|---|---|
| 1 | `DO` | `SK_DOUT` (no downstream device) | `SK_DOUT` |
| 2 | `GND` | GND | GND |
| 3 | `DI` | `SK_DIN` ← **GPIO 21** | `SK_DIN` ← **GPIO 21** |
| 4 | `VDD` | **`VDD_3V3`** | **`BL_3V3`** |

Decoupled by C17, 10 µF/10 V.

## ⚠ The rail change is the whole story

This part is the reason the Cardputer family has a documented behavioural quirk, and it is
visible only by **diffing two schematics**:

| | StampS3 `v0.2` (Cardputer v1.0) | Stamp-S3A `v0.3.3` (Cardputer v1.1, ADV) |
|---|---|---|
| WS2812 `VDD` net | **`VDD_3V3`** — always on | **`BL_3V3`** |
| `BL_3V3` source | — | **AW35122FDR** load switch, `EN` = `DISP_BL` = **GPIO 38** |
| Also on that rail | — | the **LCD backlight** |
| Consequence | the LED works whenever the board is on | **PWM-dimming the backlight chops the LED's supply** |

M5Stack documents the consequence on the **Cardputer v1.1** page:

> "Since RGB and LCD backlight share the same power source, when the LCD backlight brightness is
> below 100%, RGB will not be powered properly. Please use the RGB function when the backlight is
> at full brightness."

…and **omits it from the Cardputer ADV page**, which instead says only *"set GPIO38, which
controls this switch, to a high level"* before using the LED. Both describe the same
AW35122FDR. The omission is a vendor documentation defect, recorded at
[`devices/m5stack/cardputer-adv/gaps-and-conflicts.md`](../../../devices/m5stack/cardputer-adv/gaps-and-conflicts.md) §C4.

The trade was deliberate: gating the LED rail is part of how the Stamp-S3A gets its sleep current
from **0.26 µA to 0.15 µA**.

Also removed between the two revisions: a solder jumper **`JP4`** sat beside the WS2812 on
v0.2 and is absent on v0.3.3.

## Software

| Option | Note |
|---|---|
| `M5Unified` | `_pin_table_rgb` gives `GPIO_NUM_21` for `board_M5Cardputer` and `board_M5CardputerADV`; `M5.Display`-adjacent LED APIs handle the timing |
| `xylopyrographer/LiteLED` `^1.2.0` | what **Bruce** uses (`-DHAS_RGB_LED=1 -DRGB_LED=21`) |
| `FastLED`, `Adafruit_NeoPixel`, `led_strip` (ESP-IDF) | all standard; all use RMT on ESP32-S3 |

**On the Stamp-S3A you must raise GPIO 38 first**, or the LED has no supply — and raising it also
turns the backlight fully on. There is no way to have a dark screen and a lit status LED.

## Used By

### M5Stack Stamp-S3 and Stamp-S3A modules

[`components/m5stack/stamp-s3`](../../m5stack/stamp-s3/README.md) ·
[`components/m5stack/stamp-s3a`](../../m5stack/stamp-s3a/README.md)
*(both created by a concurrent session)*

Designator **U3** on both. Data from GPIO 21; supply as tabulated above. `DO` goes to a net
named `SK_DOUT` with no downstream device — a single LED, not a chain, but the output is
available at the module edge on v0.2 via `JP4`.

### M5Stack Cardputer v1.0, v1.1, ADV

[`devices/m5stack/cardputer-v1.0`](../../../devices/m5stack/cardputer-v1.0/README.md) ·
[`devices/m5stack/cardputer-v1.1`](../../../devices/m5stack/cardputer-v1.1/README.md) ·
[`devices/m5stack/cardputer-adv`](../../../devices/m5stack/cardputer-adv/README.md)

All three inherit the LED from their Stamp module; none adds one on the mainboard. GPIO 21 on all
three. The v1.0 is **the only Cardputer whose RGB LED is independent of the backlight.**

## Substitutes

| Part | Note |
|---|---|
| WS2812B, WS2812C, WS2812C-2020 | package and supply-range variants of the same protocol |
| SK6812 | compatible protocol, slightly different timing tolerance; RGBW variants exist |
| **APA102 / SK9822** | two-wire (clock + data) — **not protocol-compatible**, but immune to timing jitter |
| Any 800 kbit/s single-wire LED | check the reset-period requirement, which has shortened in newer parts |

Related record already in this repository:
[`generic/rs-c1415mbar-rgb-led`](../../generic/rs-c1415mbar-rgb-led/README.md).

## Gaps

* **No datasheet retrieved**, and the exact variant is unknown. The schematic says `WS2812`
  without a suffix; the physical part could be a WS2812B or a small WS2812C-2020. **This matters**
  — the original WS2812 specifies 3.5 V minimum supply, while these modules run it at **3.3 V**,
  which is out of spec for some variants and in spec for others (WS2812C is specified from 3.0 V).
  A board photograph or a BOM would settle it.
* Manufacturer not confirmed; the family is heavily second-sourced.
* No measurement of actual brightness, current draw or timing margin at 3.3 V.
