# Pinouts and buses

> ESP32-P4-WIFI6-Touch-LCD-3.4C and [4C](../esp32-p4-wifi6-touch-lcd-4c/README.md) — identical PCB.
> Established **2026-08-24** by reading the schematic PDF **visually** (rendered at 200 dpi and
> inspected region by region), cross-checked against Waveshare's own demo source.
>
> Evidence class per row. Nothing has been continuity-tested on hardware.

> **Confirmed three times over.** Derived here by reading the schematic visually, then matched
> against (1) Waveshare's `docs/HARDWARE.md` and (2) **the BSP source itself** —
> `waveshareteam/Waveshare-ESP32-components`, found via code search on 2026-08-26. The header
> `bsp/esp32_p4_wifi6_touch_lcd_xc/include/bsp/esp32_p4_wifi6_touch_lcd_xc.h` defines
> `BSP_I2C_SCL/SDA` 8/7, `BSP_I2S_SCLK/MCLK/LCLK/DOUT/DSIN` 12/13/10/9/11, `BSP_POWER_AMP_IO` 53,
> `BSP_LCD_BACKLIGHT` 26, `BSP_LCD_RST` 27, `BSP_SD_D0–D3` 39–42, `BSP_SD_CMD` 44, `BSP_SD_CLK` 43
> — **every value matches**.
>
> It also confirms two documented gaps: `BSP_LCD_TOUCH_RST` and `BSP_LCD_TOUCH_INT` are both
> `GPIO_NUM_NC` (C11), and there is **no define at all** for GPIO45 (SD power, C13) or GPIO33
> (`BL_EN`, C12) — so those omissions are in the vendor's *library*, not merely its demos.
>
> Waveshare's official `docs/HARDWARE.md` states the same values for I²C, LCD reset, backlight,
> `TP_RST` → GPIO23 via `R62`, `TP_INT` → TP2 with no MCU route, SD on GPIO39–44, and audio on
> GPIO9–13 with PA on GPIO53. Two independent derivations agreeing is the strongest evidence
> available short of hardware. See
> [`official-repo-and-community.md`](./official-repo-and-community.md).
>
> Prefer the **published BSP** (`waveshare/esp32_p4_wifi6_touch_lcd_xc` `3.0.1`) over hardcoding
> any of these constants.

## How these were established

The schematic's text layer is a layout dump — `pdftotext` yields no usable net list, which is why
an earlier pass left the SD and touch pins unresolved. The working method was:

1. `pdftoppm -r 200 -png` to render both A4 pages.
2. `pdftotext -bbox-layout` to get word coordinates, used **only to locate** regions of interest.
3. Crop each region with ImageMagick, upscale 300–600%, and read it.

The board maps GPIOs to named nets through **0 Ω series resistors** (`GPIOxx — Rnn 0R — NET_NAME`),
which is why a plain text grep never produced the mapping.

## Display and touch — 32-pin FPC connector `P1`

One FPC carries both the MIPI-DSI panel and the I²C touch controller.

| P1 pin | Signal | Net | GPIO | Evidence |
|---:|---|---|---:|---|
| 1, 2 | CTP_VCI | `ESP_3V3` | — | Schematic |
| 3 | CTP_RESET | `TP_RST` | **23** | Schematic (`R62`, 0 Ω) |
| 4 | CTP_SCL | `ESP_I2C_SCL` | **8** | Schematic + demo source |
| 5 | CTP_SDA | `ESP_I2C_SDA` | **7** | Schematic + demo source |
| 6 | CTP_INT | `TP_INT` | **none — see below** | Schematic |
| 7, 10, 13, 16, 19, 22 | GND | — | — | Schematic |
| 8, 9 | MIPI_D1N / D1P | — | — | Schematic |
| 11, 12 | MIPI_D2M / D2P | — | — | Schematic |
| 14, 15 | CLKN / CLKP | `DSI_CLK_N/P` | — | Schematic |
| 17, 18 | MIPI_D1N / D1P | `DSI_D1_N/P` | — | Schematic |
| 20, 21 | MIPI_D0N / D0P | `DSI_D0_N/P` | — | Schematic |
| 23 | PWM | — | — | Schematic |
| 24 | TE (tearing effect) | — | — | Schematic |
| 25 | RESET (panel) | `RESET` | **27** | Schematic (`R11`, 0 Ω) + demo source |
| 26 | IOVCC | `ESP_3V3` | — | Schematic |
| 27 | VCI | `ESP_3V3` | — | Schematic |
| 28, 29 | LEDK | `VLED-` | — | Schematic |
| 30 | LEDA | `VLED+` | — | Schematic |
| 31, 32 | GND | — | — | Schematic |

The panel reset on **GPIO27** independently confirms the value in Waveshare's demo code. That
agreement between two unrelated sources is the strongest evidence in this record.

### The touch interrupt is not wired to the SoC

`TP_INT` leaves connector pin 6, passes through a 0 Ω resistor, and terminates at **test point
TP2**. No GPIO label appears on the resistor's other terminal, and `TP_INT` occurs nowhere else on
the schematic.

**Conclusion: the GT911 interrupt line is brought out to a probe pad only, not to the ESP32-P4.
Touch must be polled.**

This is a firm reading of the schematic, but it is an argument from absence, so treat it as
**high confidence, not certainty**. If you need interrupt-driven touch, TP2 is where you would
bodge a wire. Note the 0 Ω resistor is populated, so the net *is* driven — it simply has nowhere
to go.

## Backlight — two separate controls

| Function | Net | GPIO | Evidence | Used by demo? |
|---|---|---:|---|---|
| Backlight **enable** | `BL_EN` | **33** | Schematic (`R61`, 0 Ω) | **No** |
| Backlight **brightness** (PWM) | `LCD_BL_PWM` | **26** | Schematic (`R65`, 0 Ω) + demo source | Yes |

The demo drives only **GPIO26**, active low. **GPIO33 (`BL_EN`) is never touched by any shipped
demo.**

This matters. If the enable line has a pull-up or a default-on bias, GPIO26 alone is sufficient
and the demos work — which is presumably why Waveshare ignore it. If it does not, a from-scratch
project that configures only GPIO26 could end up with a dark panel for no obvious reason. The
schematic does not resolve the default state, so **drive both**: assert `BL_EN` on GPIO33 and
modulate GPIO26.

## microSD — connector `SD1`

| SD1 pin | Signal | GPIO | Evidence |
|---:|---|---:|---|
| 1 | DAT2 | **41** | Schematic |
| 2 | CD/DAT3 | **42** | Schematic |
| 3 | CMD | **44** | Schematic |
| 4 | VDD | `SD1_VDD` (switched) | Schematic |
| 5 | CLK | **43** | Schematic |
| 6 | VSS | GND | Schematic |
| 7 | DAT0 | **39** | Schematic |
| 8 | DAT1 | **40** | Schematic |
| 9 | CD (card detect) | — | Schematic |
| 10 | GND | — | Schematic |
| — | **VDD power switch** | **45** | Schematic — gate of `Q1` (AO3401 P-MOSFET) |

The card is on a **switched supply**: GPIO45 drives an AO3401 P-channel MOSFET that gates
`SD1_VDD`. This is genuinely important and appears in **no** demo — you must power the card before
`sdmmc` init, and you can power-cycle a wedged card without resetting the board.

Because it is a **P-channel** device high-side switching the rail, the gate is pulled **low to turn
the card on**. That polarity is inferred from the topology, not stated on the schematic — verify
before relying on it. Note also `R21 NC/10K`, an unpopulated pull-up position, alongside a
populated `R27 10K`.

Full 4-bit SDIO is wired, so `slot_config.width = 4` is supported.

### Correction to an earlier finding

An earlier pass flagged the shipped `03_sdmmc` demo as untrustworthy because it is unmodified
upstream Espressif code whose `IDF_TARGET_ESP32P4` Kconfig defaults are Function-EV-Board values.

**The caution was methodologically right; the conclusion was wrong.** Those defaults —
`CMD=44, CLK=43, D0=39` — are **correct for this board**, because Waveshare followed Espressif's
reference pin assignment. The demo works by coincidence of design convergence, not by
board-specific configuration.

What the demo still does **not** do is drive **GPIO45**, so it depends on the card rail being
enabled some other way. That gap is real even though the pins are right.

See [C1](./gaps-and-conflicts.md#c1--microsd-pin-assignment--resolved-2026-08-24).

## I²C — one bus, three devices

| Signal | GPIO | Evidence |
|---|---:|---|
| SDA | **7** | Schematic + demo source |
| SCL | **8** | Schematic + demo source |

Devices: **GT911** touch (FPC pins 4/5), **ES8311** codec, **ES7210** echo-cancel ADC.

Clock rate is 100 kHz in `displays_config.h` and 400 kHz in `i2c.h` — both Waveshare's own code.
Treat 400 kHz as supported, 100 kHz as the conservative fallback. A stalled device on this bus
takes out touch **and** audio together.

## I²S — audio

| Signal | GPIO | Evidence |
|---|---:|---|
| MCLK | **13** | Demo source (`CONFIG_IDF_TARGET_ESP32P4` branch) |
| BCLK | **12** | Demo source |
| WS / LRCK | **10** | Demo source |
| DOUT (SoC → codec) | **9** | Demo source |
| DIN (codec → SoC) | **11** | Demo source |
| Amplifier enable | **53** | Demo source (`GPIO_OUTPUT_PA`) |

Originally code-only, these are now **confirmed** by Waveshare's `docs/HARDWARE.md`, which states
*"ES8311/ES7210 use I2S GPIO9..GPIO13 and PA enable GPIO53; this matches the BSP contract."*

## Complete verified GPIO map

| GPIO | Function | Confidence |
|---:|---|---|
| 7 | I²C SDA | **Confirmed** — schematic + code |
| 8 | I²C SCL | **Confirmed** — schematic + code |
| 9 | I²S DOUT | **Confirmed** — code + vendor BSP contract |
| 10 | I²S WS | **Confirmed** |
| 11 | I²S DIN | **Confirmed** |
| 12 | I²S BCLK | **Confirmed** |
| 13 | I²S MCLK | **Confirmed** |
| 23 | Touch reset (`TP_RST`) | **Schematic** |
| 26 | Backlight PWM | **Confirmed** — schematic + code |
| 27 | Panel reset | **Confirmed** — schematic + code |
| 33 | Backlight enable (`BL_EN`) | **Schematic** — unused by demos |
| 39 | SD DAT0 | **Schematic** |
| 40 | SD DAT1 | **Schematic** |
| 41 | SD DAT2 | **Schematic** |
| 42 | SD CD/DAT3 | **Schematic** |
| 43 | SD CLK | **Schematic** |
| 44 | SD CMD | **Schematic** |
| 45 | SD VDD power switch | **Schematic** — unused by demos |
| 53 | Speaker amplifier enable | **Confirmed** — code + vendor BSP contract |

## 40-pin expansion header `J8`

Designator **`J8`**, 2.54 mm pitch. Waveshare: *"compatible with some Raspberry Pi HATs (**requires
pin header adapter**)"*.

### Signal mapping

Derived from the schematic by coordinate pairing, spot-verified visually. The **same extraction
method was validated against `J4` and `J6`**, whose small pinouts could be read directly and
matched exactly.

| Pin | Signal | Pin | Signal |
|---:|---|---:|---|
| 1 | **power/GND — not identified** | 2 | **power/GND — not identified** |
| 3 | **power/GND — not identified** | 4 | GPIO30 |
| 5 | GPIO47 | 6 | GPIO46 |
| 7 | GPIO52 | 8 | GPIO31 |
| 9 | GPIO48 | 10 | **power/GND — not identified** |
| 11 | GPIO32 | 12 | GPIO34 |
| 13 | GPIO51 | 14 | **power/GND — not identified** |
| 15 | USB1P1_N | 16 | USB1P1_P |
| 17 | **power/GND — not identified** | 18 | GPIO49 |
| 19 | GPIO50 | 20 | GPIO36 |
| 21 | GPIO2 | 22 | GPIO35 |
| 23 | GPIO3 | 24 | **power/GND — not identified** |
| 25 | **power/GND — not identified** | 26 | GPIO4 |
| 27 | GPIO28 | 28 | GPIO5 |
| 29 | GPIO20 | 30 | **power/GND — not identified** |
| 31 | GPIO21 | 32 | GPIO22 |
| 33 | **power/GND — not identified** | 34 | GPIO38 |
| 35 | GPIO29 | 36 | GPIO37 |
| 37 | ESP_I2C_SCL (GPIO8) | 38 | **power/GND — not identified** |
| 39 | ESP_I2C_SDA (GPIO7) | 40 | **power/GND — not identified** |

**28 of 40 pins carry a named signal. The other 12 do not, and are deliberately left
unidentified.**

### ⚠️ The 12 unlabelled pins are the dangerous ones

Ground and power connections are drawn as **schematic symbols, not text labels**, so they yield no
token to pair against. Twelve pins — **1, 2, 3, 10, 14, 17, 24, 25, 30, 33, 38, 40** — are
therefore known to be *power or ground*, but **which is 5 V, which is 3V3 and which is GND is not
established**.

The header does carry `VCC_5V`, `ESP_3V3` and nine `GND` connections; they simply cannot be
assigned to specific pins from the text layer.

**Do not connect anything to those 12 pins without checking with a meter.** Confusing 5 V for GND
destroys hardware.

### It is not a Raspberry Pi header

Compare the power/GND positions:

| | This board | Raspberry Pi |
|---|---|---|
| Power/GND pins | 1, 2, 3, 10, 14, 17, 24, 25, 30, 33, 38, 40 | 1, 2, 4, 6, 9, 14, 17, 20, 25, 30, 34, 39 |

Only six of twelve coincide, and the mismatches are decisive: **pin 4 is a GPIO here but 5 V on a
Pi**, and **pin 6 is a GPIO here but GND on a Pi**. A HAT expecting Pi conventions would feed 5 V
into a GPIO.

Combined with Waveshare's "requires pin header adapter" wording, treat `J8` as a **GPIO breakout
that happens to have 40 pins**. Verify every connection before fitting any HAT.

### I²C on the header is the shared bus

Pins 37/39 are `ESP_I2C_SCL`/`SDA` — GPIO8/GPIO7, **the same physical bus as the GT9271 touch
controller and the ES8311/ES7210 audio chips**. Anything attached shares it: an address collision
or a stuck device takes out touch and audio too. Check addresses with `03_i2c_tools` first.

### Independently confirmed: 28 signal pins

Waveshare's **Chinese** storefront states:

> 板上引出 2 * 20 排座，引出 **28** 个剩余可编程 GPIO 接口
> *"The board brings out a 2 × 20 header, exposing **28** remaining programmable GPIO interfaces."*

My schematic extraction found **exactly 28 named signal pins** (24 GPIO + I²C SDA/SCL + USB1P1_N/P)
and 12 unlabelled power/GND pins. **28 + 12 = 40.**

Two entirely independent sources — a coordinate-paired schematic read and a vendor marketing
figure — arriving at the same count is strong evidence the split is right. It does **not** confirm
which pin is which, but it does confirm none were missed or double-counted.

Notably this figure appears **only in the Chinese material**. The English wiki, English store page
and `docs.waveshare.com` all say "40PIN GPIO header" without a usable count.

### Evidence status

Schematic-derived, **not** hardware-verified. The 28 signal rows come from an extraction method
validated against `J4` and `J6`, and the count is corroborated by the vendor. The 12 power rows
remain an explicit gap.

## MIPI-CSI camera connector `J5`

15-pin, 1.0 mm pitch FPC. Confirmed nets:

| Signal group | Nets |
|---|---|
| Data lane 0 | `CSI_D0_N`, `CSI_D0_P` |
| Data lane 1 | `CSI_D1_N`, `CSI_D1_P` |
| Clock | `CSI_CLK_N`, `CSI_CLK_P` |
| Sensor control | `ESP_I2C_SDA`, `ESP_I2C_SCL` |

**This resolves an open question in the camera guide:** the camera's SCCB control **does** share
the GPIO7/GPIO8 I²C bus with touch and audio. It is not a separate bus. Four device families now
share one bus — plan addresses accordingly.

Two data lanes plus clock matches the documented "MIPI-2lane camera" support.

## ESP32-C6 UART header `J4`

SH1.0 4-pin. **Read directly from the schematic and visually confirmed.**

| Pin | Signal |
|---:|---|
| 1 | `C6_U0TXD` |
| 2 | `C6_U0RXD` |
| 3 | `GND` |
| 4 | `C6_IO9` |

This is the header for flashing the ESP32-C6 radio co-processor. **`C6_IO9` is the C6's strapping
pin** — held low at reset to enter download mode, exactly as `GPIO9` works on other ESP32-C6
designs. So the header exposes TX, RX, GND and the boot strap: everything needed to flash the C6
with a standard USB-UART adapter.

That materially narrows the "C6 firmware procedure unknown" gap: the *interface* is now understood
even though Waveshare publish neither the image nor the offsets.

## I²C expansion header `J6`

SH1.0 4-pin. **Read directly and visually confirmed.**

| Pin | Signal |
|---:|---|
| 1 | `GND` |
| 2 | `ESP_3V3` |
| 3 | `ESP_I2C_SDA` (GPIO7) |
| 4 | `ESP_I2C_SCL` (GPIO8) |

A Qwiic/STEMMA-style breakout of the **shared** I²C bus — same caveat as `J8` pins 37/39.

## ESP32-C6 SDIO link

Not on a connector — the internal bus between the P4 and the radio co-processor. Values from the
`netseye/linux-waveshare-xc` port (**community, needs hardware validation**):

| Signal | GPIO |
|---|---|
| C6 SDIO D0–D3 | **14, 15, 16, 17** |
| C6 SDIO CLK | **18** |
| C6 SDIO CMD | **19** |
| C6 reset | **54**, active-**high** |

### The microSD / Wi-Fi contention question — likely answered

That project states plainly:

> *"microSD — **Mutually exclusive with Wi-Fi/BT**. P4 exposes one DW-MMC host; this build selects
> C6 SDIO slot 1 instead of card slot 0."*

This is the clearest answer yet to a question left open throughout this record. Read carefully, it
says the P4 exposes **one** DW-MMC controller with two slots: **slot 0 = microSD**, **slot 1 = the
C6 link**. Their build chooses one.

**Caveats before treating it as settled.** It is (a) community evidence, (b) about a *Linux* port,
not ESP-IDF, and (c) explicitly unvalidated on hardware by its own author. ESP-IDF may drive the
same silicon differently. But it is a specific, mechanism-level claim from someone who read the
same schematic, and it matches the symptom to expect.

**Practical guidance unchanged:** do not design around simultaneous microSD and Wi-Fi until tested.
If anything, this raises the odds they genuinely conflict.

## RTC backup battery `J1`

2-pin connector. Read from the schematic 2026-08-24.

| J1 pin | Net |
|---:|---|
| 1 | `ESP_VBAT` |
| 2 | `GND` |

Circuit:

```
ESP_3V3 ──┤>├── ESP_VBAT ──┬── J1 pin 1  (battery +)
          D2               │
       B5819WS            C39 1uF
       Schottky            │
                          GND
```

| Ref | Part | Function |
|---|---|---|
| `D2` | **B5819WS** Schottky | Feeds `ESP_VBAT` from `ESP_3V3` when the board is powered |
| `C39` | 1 µF | Decoupling on `ESP_VBAT` |
| `J1` | 2-pin header | Battery connection |

`ESP_VBAT` is the ESP32-P4's **RTC backup supply**. With main power on, the rail is held up through
`D2`; with main power off, the cell on `J1` maintains the RTC.

### ⚠️ Why only rechargeable cells — the circuit explains it

Waveshare's "only rechargeable RTC batteries are supported" warning is not a preference. **The
charge path is a bare Schottky diode from the 3V3 rail straight to the cell**, with no
current-limiting resistor anywhere in the RTC block.

That means whenever the board is powered, `ESP_3V3` drives current into whatever is on `J1`,
limited only by the diode drop (~0.3 V for a B5819WS) and the cell's own internal resistance.

- A **rechargeable** cell (ML2032, LIR2032) is designed to accept this as trickle charge.
- A **primary** cell (CR2032) is **not rechargeable**. Charging one causes internal gassing and
  can make it vent, leak, or rupture.

**Fitting a CR2032 to this holder is a genuine safety hazard, not just poor practice.** With no
series resistor, there is nothing else in the circuit to prevent it.

No GPIO is involved — the RTC domain is powered, not controlled, so there is nothing to configure
in firmware.

## USB connector `J3`

`VBUS`, `VBUS_OUT`, `USBD_N`, `USBD_P`, `GND` — the USB 2.0 OTG interface.

## Still unresolved

- **`J8` power/GND pins**: 12 pins known to be power or ground, but **not individually
  identified**. Requires a meter or high-zoom schematic reading.

- **RTC** circuit and any associated GPIO — still unmapped.
- **Card-detect** (SD1 pin 9) destination.
- **`BL_EN` default state** — pull-up present or not.
- **GPIO45 polarity** — inferred from P-MOSFET topology, not confirmed.
- Whether the microSD and the ESP32-C6 SDIO link share an SDMMC host.
- Audio I²S pins not schematic-confirmed.

## Related

- [Shared platform record](../esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
- [Storage](./features/storage.md) · [Touch](./features/touch.md) · [Display](./features/display.md)
- [Gaps and conflicts](./gaps-and-conflicts.md) · [Command ledger](./commands.md)
