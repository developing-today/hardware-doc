# Display interfaces

> How the documented devices actually get pixels onto glass: SPI, QSPI, parallel RGB / i80,
> MIPI-DSI and e-paper parallel — when each is used, what it costs in bandwidth and memory, and
> what the ESP32 family provides for each.
> Compiled **2026-08-30** from the device and component records.
> **Revised 2026-08-30** against the Espressif TRMs — see
> [soc-peripheral-reference.md §16](../espressif/soc-peripheral-reference.md#16-lcd-camera-and-display-peripherals),
> which is the numeric companion to this page. **No hardware.**

## 0. Scope

Five display transports appear across the fourteen devices in
[`devices/`](../../devices/README.md). This guide compares them, works the arithmetic that decides
which one a board can use, and collects the practical integration knowledge — TE lines, framebuffer
sizing, LVGL buffers, init tables — that is currently split across a dozen records.

For the e-paper column, **[e-paper-displays.md](e-paper-displays.md) is the deep treatment**; this
page covers only how e-paper sits among the others as a *transport*.

Evidence labels are the repository's. Arithmetic performed here is marked **[INF]** and shown so it
can be checked.

> ⚠ **Two boards in this library use MIPI-DSI, one uses QSPI, two use SPI, three use the e-paper
> parallel bus, and one has no display at all. None uses i80 or RGB parallel.** No worked example,
> pin map or measurement for those last two exists here — but as of **2026-08-30** the *silicon* side
> of both is documented with TRM page citations (§3.3, §3.4,
> [soc-peripheral-reference.md §16](../espressif/soc-peripheral-reference.md#16-lcd-camera-and-display-peripherals)),
> so they are no longer purely theoretical. See [§10](#10-gaps-this-guide-cannot-fill) for what is
> closed and what is not.

---

## 1. The one-page answer

| Transport | Wires (typ.) | Where the timing lives | Panel needs a controller? | In this library |
|---|---|---|---|---|
| **SPI** | CLK, MOSI, CS, **D/C**, (MISO) | Host sends a command, controller scans autonomously from its own GRAM | ✅ yes, with framebuffer | [P4X-EYE / P4-EYE](../../devices/espressif/esp32-p4x-eye/README.md) — ST7789VW, 240 × 240 |
| **QSPI** | CLK, **D0–D3**, CS, **no D/C** | as SPI; the command is folded into a 32-bit in-band opcode | ✅ yes, with framebuffer | [Knob 1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — ST77916, 360 × 360 @ 40 MHz |
| **i80 / 8080 parallel** | 8 or 16 data + WR, RD, DC, CS (24 data on P4) | as SPI, but wide and fast | ✅ yes, with framebuffer | **none** |
| **RGB parallel (DPI)** | 16–24 data + HSYNC, VSYNC, DE, PCLK | **the host** — it must stream every pixel of every frame, continuously | ❌ no framebuffer; host holds it | **none** |
| **MIPI-DSI** | 1–4 differential data lanes + clock lane — **the ESP32-P4 has exactly 2** | **the host**, in video (DPI) mode; the panel in command (DBI) mode — ⚠ **the P4 only does video mode for pixels** (§3.5) | usually a bridge/controller, no framebuffer in video mode | [P4 3.4C / 4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) — JD9365; [Espressif 7″ panel](../../devices/espressif/esp32-p4x-function-ev-board/README.md) — EK79007AD; [Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) — ST7701S |
| **E-paper parallel ("DES")** | 8 data + CL, LE, SPH, CKV, SPV, OE, GMOD | **entirely the host** — every phase of every waveform, in real time | ❌ **no controller at all**, no memory | [Inkplate 5 / Gen 2](../../devices/soldered-electronics/inkplate-5/README.md), [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md) |

**The organising distinction is not speed — it is *who owns the frame*.**

- **SPI, QSPI and i80 panels own their own frame.** The controller has GRAM and a scan engine. You
  push only what changed and then stop; the panel keeps displaying. Cheap in bandwidth, cheap in host
  memory, and the reason a 240 × 240 watch display works on a tiny MCU.
- **RGB parallel and MIPI-DSI video mode make the host the frame owner.** There is no GRAM to hide
  behind: the host streams every pixel of every frame forever, so it needs a framebuffer, DMA that
  never underruns, and PSRAM bandwidth to spare. This is the price of a big panel.
- **A bare e-paper panel takes that further than anything else here.** It has no controller *and* no
  memory, so the host holds the framebuffer, the *previous* image, and sequences every waveform phase
  itself ([e-paper-displays.md §2](e-paper-displays.md#2-two-architectures-and-which-one-you-have)).

Everything else in this guide follows from that one distinction.

---

## 2. Bandwidth, worked

All arithmetic below is **[INF]** — performed here from figures in the linked records, not quoted
from any vendor. It is gross link capacity and payload demand; it deliberately does **not** produce
frame rates, for the reason in §2.4.

### 2.1 QSPI — Knob 1.8, 360 × 360 RGB565

Established **[SRC]**: `pclk_hz = 40 MHz`, four data lines, `lcd_cmd_bits = 32`, 16 bpp.

```
gross link      = 40 MHz × 4 lanes            = 160 Mbit/s = 20 MB/s
full frame      = 360 × 360 × 2 B             = 259,200 B
time per frame  = 259,200 / 20e6              ≈ 13 ms
```

So a full-screen flush costs ~13 ms of pure transfer. That is comfortable for a UI and hopeless for
video — which is exactly why the vendor drives it with **partial** LVGL redraws (§7).

### 2.2 MIPI-DSI — Waveshare P4 boards, 24 bpp

Established **[SRC]**: 2 lanes at **1500 Mbps**, 24 bpp, and porch timings identical across both
variants (`hsync pw/bp/fp = 20/20/40`, `vsync pw/bp/fp = 4/12/24`).

```
gross link      = 2 × 1500 Mbit/s             = 3000 Mbit/s
payload px/s    = 3000e6 / 24 bpp             = 125 Mpixel/s        [gross, ignoring DSI overhead]

3.4C total frame incl. blanking = (800+20+20+40) × (800+4+12+24) = 880 × 840 = 739,200 px
4C   total frame incl. blanking = (720+20+20+40) × (720+4+12+24) = 800 × 760 = 608,000 px
```

**This quantifies a qualitative observation the shared record already makes.** That record notes
Waveshare use *the same* blanking and *the same* 1500 Mbps lane rate for both panels despite an 11 %
difference in horizontal pixel count, so *"the DSI link is therefore running with more slack on the
4C"* ([shared record](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md#what-is-genuinely-shared-vs-per-variant)).
The arithmetic puts a number on it: the 4C's frame is **18 % smaller** in total pixel-times for the
same link rate. **The link is not the bottleneck on either board.**

> **The 1500 Mbps in these records is the silicon maximum, not a Waveshare choice** **[DOC]**.
> TRM-P4 v0.7 **p. 2633**: the P4's DSI provides *"one clock lane and two data lanes, and supports a
> maximum bit rate of **1.5 Gbps per lane**"*, with *"Lane operation ranging from **80 Mbps to 1.5
> Gbps** in HP TX"*. DS-P4 v0.7 §4.2.1.7 p. 67 says *"2-lane × 1.5 Gbps"*. So the `3000 Mbit/s` above
> is the ceiling of the part, and **there is no faster configuration to move to** — a second
> independent limit, the **240 MHz maximum DPI frequency** (TRM p. 2633), sits above it at these
> colour depths and does not bind.
>
> At 60 Hz the two boards use **36 %** (3.4C) and **30 %** (4C) of the link at 24 bpp. Ceilings for
> larger panels, including why **1080p60 is reachable at RGB565 and not at RGB888**, are worked in
> [soc-peripheral-reference.md §16.9](../espressif/soc-peripheral-reference.md#169-which-target-drives-which-panel-class).

The record's conclusion stands and is the one that matters: **the timings are not derived per panel.**
Do not assume they are optimal for either, and re-derive them if you change pixel clock or colour
depth. Registered as
[C4](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c4--dsi-porch-timings-are-not-derived-per-panel).

### 2.3 E-paper parallel — Inkplate 5 Gen 2

Established **[SRC]**: I2S1 in LCD mode, *"BCK should be ~16 MHz"*, 8-bit bus, **4 pixels per byte**.

```
gross            = 16 MHz × 8 bit             = 128 Mbit/s = 16 MB/s
line (TC4)       = 1280/4 + 16                = 336 B      ≈ 21 µs
one full pass    = 336 B × 720 lines          ≈ 15.1 ms
full refresh     = 53 passes                  ≈ 0.8 s
```

**Nominally the slowest link here is not slow at all — one pass is 15 ms.** The ~1 s refresh comes
almost entirely from needing **53 passes**, ~90 % of them the black-white-black-white clean sequence.
**Physics, not bandwidth.** Full breakdown in
[e-paper-displays.md §6.3](e-paper-displays.md#6-update-modes-and-real-timings).

⚠ These figures carry an acknowledged **2× uncertainty** because `lcd_tx_wrx2_en = 1` may halve the
effective rate; **checked against the ESP32 TRM on 2026-08-30 and still unresolved.** TRM-32 v5.8
§22.5.1, **p. 427** **[DOC]** does describe the two shapes — *"the `I2S_LCD_TX_WRX2_EN` bit should be
set to 1 and the `I2S_LCD_TX_SDX2_EN` bit should be set to 0 in the data frame, form 1. Both …
are set to 1 in the data frame, form 2"* — but the content that distinguishes them is **Figures
22.5-2 and 22.5-3, which are vector images with no recoverable text layer.** The TRM cannot settle
this; the rendered figures or a measurement can. Context in
[soc-peripheral-reference.md §16.2](../espressif/soc-peripheral-reference.md#162-esp32--the-lcd-peripheral-that-is-really-i2s).

For what it is worth, the arithmetic ceiling now exists **[INF]**: `I2Sn_CLK` comes from
PLL_F160M_CLK (160 MHz) with divider N ≥ 2, `BCK` from `I2Sn_CLK` with M ≥ 2 (TRM-32 §22.3,
**pp. 417–418**), so **f<sub>BCK</sub> ≤ 40 MHz** — and Soldered's ~16 MHz sits comfortably inside it
either way.

### 2.4 What is *not* derived here

**No frame rate.** The 3.4C display record deliberately declines to state one:

> *"It could be computed from the pixel clock and porches, but the demo's `prefer_speed` (80 MHz) and
> the DPI clock are not unambiguously the same quantity, and guessing a frame rate would be exactly
> the kind of invented precision this repository avoids."*

That reasoning applies to this page too. §2.2 gives what the **link** can carry; it does not say what
the **panel** is clocked at, and those are different questions. Likewise the Tanmatsu's DSI lane rate
is **not documented in any record**, so its 60 Hz nominal figure (from badge.team) cannot be
cross-checked against a link budget here.

---

## 3. The interfaces in detail

### 3.1 SPI

The baseline. One clock, one data line, a chip select and a **D/C pin** that tells the controller
whether the current byte is a command or a parameter. Everything else in this section is a variation
on removing bottlenecks from this.

In the library: **[ESP32-P4X-EYE](../../devices/espressif/esp32-p4x-eye/README.md)** and its EOL
predecessor drive a 1.54″ 240 × 240 panel (`ZJY154KC-IF17` module, **ST7789VW** controller) over SPI.
That is worth pausing on — it is an **ESP32-P4**, a part with a full MIPI-DSI PHY, deliberately
driving a small SPI panel. The P4 is on that board for the *camera* and the AI workload; the display
is a viewfinder. **Having a DSI-capable SoC does not oblige you to use DSI**, and the smallest, most
power-frugal transport is often the right one for a small panel.

No SPI clock rate for that panel is documented in any record. **Unknown.**

### 3.2 QSPI

Four data lines instead of one, and **no D/C pin** — the command is folded in-band. The industry
convention, described in full in
[ST77916 §2 of the programming reference](../../components/sitronix/st77916/st77916-programming-reference.md#2-the-qspi-wire-protocol):

```c
#define LCD_OPCODE_WRITE_CMD        (0x02ULL)
#define LCD_OPCODE_READ_CMD         (0x03ULL)
#define LCD_OPCODE_WRITE_COLOR      (0x32ULL)
// 8-bit command shifted into bits 8-15 of a 32-bit word, opcode in bits 24-31
```

Two configuration values make it work, and they are the two people get wrong:

| Setting | Value | Why |
|---|---|---|
| `lcd_cmd_bits` | **32** | The command *is* the 32-bit opcode word |
| `dc_gpio_num` | **−1** | There is no D/C pin |
| `flags.use_qspi_interface` | **1** | Without it, `tx_param`/`tx_color` skip the opcode wrapping and the panel sees nonsense. **Symptom: a completely dead display with no errors** |

> **The `02h`/`32h` framing is shared by ST77916, SH8601, CO5300, RM69330, RM67162 and NV3041A. It
> is not a controller signature.** This matters more than it sounds — see §6.

QSPI's practical niche is exactly the Knob 1.8's: a panel too big for comfortable 1-line SPI
(259 kB per frame) but small enough that you do not want to spend a DSI PHY or 24 GPIOs on it.

### 3.3 i80 (Intel 8080) parallel

8 or 16 data lines plus `WR`, `RD`, `DC`, `CS`. Same *model* as SPI — the controller still owns the
frame — but 8–16× the wire width. The classic mid-size embedded display bus.

**No device in this library uses it.** It appears here for two reasons. First, it is what the
ESP32-S3's `LCD_CAM` peripheral is primarily for (§4). Second, the
[ED052TC4 record](../../components/e-ink/ed052tc4/README.md) notes that on an ESP32-S3 you would drive
the *e-paper* panel through `esp_lcd_panel_io_i80` with `LCD_CAM` — "a much better fit" than the
original ESP32's I2S abuse — **but that is a different board, and nobody has built it.** Marked as a
gap in §10.

**What the silicon actually offers [DOC]** — now extracted, from
[soc-peripheral-reference.md §16.1](../espressif/soc-peripheral-reference.md#161-the-one-page-display-answer):

| | ESP32 | ESP32-S3 | ESP32-P4 |
|---|---|---|---|
| Bus width | 8/16/**24**-bit, but **24-bit on I2S0 only** | **8/16-bit** | 8/16/**24**-bit |
| Max pixel clock, 8-bit | not stated; **≈20 MHz** by arithmetic | **< 80 MHz** | **< 80 MHz** |
| Max pixel clock, 16-bit | — | **< 40 MHz** | **< 40 MHz** |
| MOTO6800 as well as i80 | ❌ not named | ✅ | ✅ |

Those pixel-clock figures are TRM-S3 v1.8 **p. 1090** and TRM-P4 v0.7 **pp. 2315–2316**, and they
drop to **60/30 MHz** if the hardware YUV↔RGB converter is enabled at the same time. ⚠ **The S3
datasheet disagrees with the S3 TRM** — DS-S3 v2.2 p. 52 states a flat *"40 MHz or lower"* for all
widths. Designing an 8-bit bus above 40 MHz means relying on the TRM.

### 3.4 RGB parallel (DPI)

16–24 data lines plus `HSYNC`, `VSYNC`, `DE` and `PCLK`. **The panel has no memory and no scan
engine**; the host streams pixels continuously, forever, from its own framebuffer. Cheap glass,
expensive host: 24+ GPIOs, a DMA path that must never underrun, and enough PSRAM bandwidth to sustain
the full pixel rate at all times.

**No device in this library uses it**, though it is the interface that the
[ST7701S](../../components/sitronix/st7701s/README.md) — fitted to the Tanmatsu — *also* supports; the
Tanmatsu uses its DSI mode instead.

> **⚠ The original ESP32 cannot do this at all.** Previously stated on this page only as "no
> `LCD_CAM`". The mechanism is now established: the ESP32's `I2Sn_H_SYNC`, `I2Sn_V_SYNC` and
> `I2Sn_H_ENABLE` signals exist **only as camera inputs** (TRM-32 v5.8 Table 22.1-1, **p. 416** —
> *"In Camera mode, I2S module inputs signals"*), and §22.5 defines no RGB mode. There is no sync
> **output** anywhere in the ESP32 I2S signal bus. The S3 and P4 both define `LCD_H_SYNC`,
> `LCD_V_SYNC` and `LCD_DE` as **outputs** in LCD Master TX mode (TRM-S3 Table 29.3-1 p. 1079;
> TRM-P4 Table 40.3-1 pp. 2301–2302). See
> [soc-peripheral-reference.md §16.2](../espressif/soc-peripheral-reference.md#162-esp32--the-lcd-peripheral-that-is-really-i2s).

**Practical resolution ceiling on S3 and P4 [INF].** The 16-bit pixel-clock limit is `< 40 MHz`, so at
60 Hz with ~10 % blanking overhead you get roughly **600,000 active pixels per frame** — about
1024 × 576, and 800 × 480 with comfortable margin. That is a *mechanism* for the threshold the
[ESP32-P4 chip record](../../components/espressif/esp32-p4/README.md) already states for choosing a
P4 (*"a display above roughly 800 × 480"*): above it, RGB/DPI at 16 bits runs out of pixel clock.
Worked in
[soc-peripheral-reference.md §16.9](../espressif/soc-peripheral-reference.md#169-which-target-drives-which-panel-class).

⚠ **A 24-bit RGB888 panel is not an option on the S3** — the bus is 8/16-bit and the colour converter
knows only RGB565 (TRM-S3 Table 29.3-4, p. 1086). On the P4 the 24-bit bus and an RGB888↔RGB565
converter both exist (TRM-P4 §40.3.6, p. 2309), but **Espressif publish no pixel-clock limit for
24-bit mode**, so its ceiling is unknown rather than high.

### 3.5 MIPI-DSI

Differential serial lanes, so a 1024 × 600 panel needs a handful of wires rather than thirty. Two
operating modes, and the distinction governs everything downstream:

| Mode | Also called | Who drives timing | Panel memory | Tearing |
|---|---|---|---|---|
| **Video mode** | DPI | **the host**, continuously | none | managed by framebuffer swap, not a TE pin |
| **Command mode** | DBI | the panel | GRAM | TE pin — or, in DSI, a TE *message* over the link — signals the safe window |

> **⚠ On the ESP32-P4 the pixel path is video mode, and only video mode** **[DOC]**. This is not a
> driver convention; it is what the silicon offers. DS-P4 v0.7 §4.2.1.7 **p. 67** lists the DSI's
> pixel sources as *"**Using the video mode to output video stream**"* and *"Outputting image
> patterns"* — those two. TRM-P4 v0.7 §43.6.4 **p. 2662**, *"System memory data output flow
> configuration"*, routes memory → **VDMA** → DSI Bridge → **DPI** → DSI Host → D-PHY and offers no
> alternative. Command mode on this part is §43.6.6 **pp. 2662–2663**, *"Using DCS command to
> **operate Display register**"* — a register channel, not a framebuffer channel.
>
> **[INF] Consequence:** a DSI panel that only accepts command-mode pixel writes into its own GRAM
> cannot be driven for pixel data by an ESP32-P4. Every DSI panel in this library is a video-mode
> panel, which is consistent, but it is a constraint rather than a coincidence.

**Lane budget [DOC]:** 1 clock lane + **2 data lanes**, **80 Mbps – 1.5 Gbps per lane**, D-PHY
rev 1.1, maximum DPI frequency **240 MHz**, DPI output **RGB888 / RGB666 / RGB565** from inputs
**RGB888 / RGB666 / RGB565 / YUV422 / YUV420 / GRAY** — TRM-P4 v0.7 §43.1–43.2, **pp. 2633–2634**.
The DSI pins are **dedicated**, not GPIO-matrix: pins **34–40** on the `VDD_MIPI_DPHY` rail
(DS-P4 v0.7 pin table, p. 15), which is why they cannot be moved and why the PHY supply is a
separate concern (below).

**Burst vs non-burst is a real choice with a stated rule [DOC]** — TRM-P4 v0.7 §43.4.2.1, **p. 2637**.
Use **burst** only if the panel *"supports receiving a full pixel line in one single block and the
reception buffer won't overflow"* **and** *"the DSI output bandwidth is much higher than the DPI input
bandwidth"*; otherwise non-burst, because *"the pixel data may be lost, causing malfunction of the
display peripheral."* Non-burst comes in **sync-pulse** (panel can reconstruct exact sync widths) and
**sync-event** flavours.

All three DSI devices in the library are set up in **video mode with a DBI side-channel for
initialisation** — visible in the Waveshare bring-up sequence, where `esp_lcd_new_panel_io_dbi()`
creates the command channel and the DPI config carries the timing table:

```c
esp_lcd_dsi_bus_config_t bus_config = JD9365_PANEL_BUS_DSI_2CH_CONFIG();
esp_lcd_new_dsi_bus(&bus_config, &mipi_dsi_bus);

esp_lcd_dbi_io_config_t dbi_config = JD9365_PANEL_IO_DBI_CONFIG();
esp_lcd_new_panel_io_dbi(mipi_dsi_bus, &dbi_config, &mipi_dbi_io);

// DPI config carries .h_size/.v_size and the porches
esp_lcd_new_panel_jd9365(mipi_dbi_io, &panel_config, &panel_handle);
```

**The DSI PHY needs its own supply, and on the ESP32-P4 that supply is software-controlled.** This is
the single most surprising DSI fact in the library, from the
[Tanmatsu display record](../../devices/nicolai-electronics/tanmatsu/display.md): the P4's four
internal LDO channels are allocated `VO1 = VFLASH`, `VO2 = VPSRAM`, **`VO3 = VMIPI`**,
`VO4 = VSDCARD`, and Tanmatsu's BSP sets `BSP_DSI_LDO_CHAN = 3` at `BSP_DSI_LDO_VOLTAGE_MV = 2500`.

> **If LDO channel 3 is not brought up at 2.5 V, the display will not run no matter how the panel
> driver is configured.** The same mechanism explains why some Tanmatsu expansion pins need "the
> VSDCARD LDO enabled" — they sit in the `VO4` domain.

There is a second silicon-revision trap. Waveshare state that published firmware for the P4 boards is
**rev3.x only**; pre-v3 boards need a **different DSI PHY clock source** and cannot run it as-is.
Espressif's own devkit panels are likewise revision-tied — **v0.0 → ILI9881C, v0.1 → EK79007** — which
is worth checking if you cross-develop.

### 3.6 E-paper parallel

Covered in [e-paper-displays.md](e-paper-displays.md). Its place in *this* taxonomy: it is the only
transport here where the host owns not just the framebuffer but **the drive waveform itself**, and
the only one with **no controller in the panel at all**. On the original ESP32 — which has no
`LCD_CAM` — Soldered reach it by **routing the I2S1 peripheral onto the panel bus in LCD mode**,
DMA-fed, with `CL`, `CKV`, `SPH` and `LE` bit-banged from the same loop via direct
`GPIO.out_w1ts` register writes.

That is not a hack of last resort; on the original ESP32 **it is the only route**, and §4 explains
why.

---

## 4. What each ESP32 generation actually provides

Numeric peripheral counts for these three parts live in
[**soc-peripheral-reference.md**](../espressif/soc-peripheral-reference.md), extracted from the TRMs
and datasheets held locally. **The display peripherals are now extracted too, in
[§16 of that page](../espressif/soc-peripheral-reference.md#16-lcd-camera-and-display-peripherals)** —
bus widths, pixel-clock ceilings, colour formats, MIPI lane rates, PPA/2D-DMA/JPEG/H.264 and the DMA
map. The display-relevant rows:

| | **ESP32** | **ESP32-S3** | **ESP32-P4** |
|---|---|---|---|
| Dedicated LCD peripheral | ❌ **none** | ✅ **`LCD_CAM`** (i80 + MOTO6800 + RGB) | ✅ **`LCD_CAM`** *plus* **MIPI-DSI / MIPI-CSI** |
| Parallel display route | **I2S in LCD mode** — TRM-32 v5.8 **§22.5 "Camera-LCD Controller", p. 426** **[DOC]** | `LCD_CAM` Ch. 29, **p. 1078**; I2S stays free | `LCD_CAM` Ch. 40, **p. 2300**; I2S stays free |
| LCD bus width | 8/16/**24**-bit — *"The LCD data bus width is 24 bits"* (p. 426), but ⚠ *"I2S1 does not support 24-bit width"* (p. 416) **[DOC]** | **8/16-bit** only **[DOC]** p. 1078 | 8/16/**24**-bit **[DOC]** p. 2300 |
| **RGB/DPI output** | ❌ **no sync outputs exist** (§3.4) | ✅ `LCD_H_SYNC` / `LCD_V_SYNC` / `LCD_H_ENABLE` **[DOC]** p. 1079 | ✅ same **[DOC]** pp. 2301–2302 |
| Max LCD pixel clock | not stated; **≈20 MHz** derived | **< 80 MHz** (8-bit) / **< 40 MHz** (16-bit) **[DOC]** p. 1090 | same **[DOC]** pp. 2315–2316; **24-bit unstated** |
| Colour conversion in the LCD path | ❌ none | RGB565 ↔ YUV422/420/411, BT601/709 **[DOC]** p. 1085 | + **RGB888 ↔ RGB565** **[DOC]** p. 2309 |
| DVP camera | 16-bit slave RX only | **8/16-bit**, master or slave **[DOC]** p. 1078 | **8/16-bit**, master or slave, **feeds the ISP** |
| MIPI | ❌ | ❌ | **DSI 2-lane** and **CSI 2-lane**, both **80 Mbps – 1.5 Gbps/lane** **[DOC]** pp. 2633, 2592 |
| I2S instances | 2 | 2 | 3 + 1 LP |
| General-purpose SPI | SPI2, SPI3 | SPI2, SPI3 | GP-SPI2, GP-SPI3 + LP-SPI |
| DMA feeding the display | I2S's own DMA | **GDMA**, one shared pool of 5 TX + 5 RX | **GDMA** for `LCD_CAM`, **VDMA** for DSI, **2D-DMA** for PPA/JPEG **[DOC]** |
| GPIO | 34 (6 input-only) | 45 | 55 |
| Graphics acceleration | — | — | **PPA + 2D-DMA**, ISP (≤1920×1080), **H.264 enc 1080p@30**, JPEG **1080p@40** **[DOC]** |
| Practical ceiling | small SPI panels; parallel only at the cost of an I2S | QSPI and i80/RGB panels up to ~800 × 480 @ 60 Hz | MIPI-DSI panels; 1080p60 at RGB565, not at RGB888 **[INF]** |

Three consequences the peripheral reference draws out, all of which show up in this library's boards:

**⚠ On the original ESP32, a parallel display consumes an entire I2S instance.** *"because ESP32's
I2S *is* the parallel LCD/camera controller, using an 8080 or DVP parallel display consumes an entire
I2S instance. On S3/P4 the `LCD_CAM` peripheral is separate and I2S stays free"* **[INF]**. **This is
precisely the Inkplate's situation** — the ESP32-WROVER's I2S1 is the e-paper bus, and it is not
available for anything else. It also explains why the Inkplate has no audio.

**⚠ The S3's ten GDMA channels are a shared pool.** *"SPI2, SPI3, I2S0, I2S1, SDMMC, AES, SHA, UHCI,
RMT ch3/ch7 and LCD_CAM all draw from it. A design running QSPI display + I2S audio + SD card
concurrently is already using 6 of the 10. `ESP_ERR_NOT_FOUND` from a driver's DMA init is the
symptom of exhaustion"* **[INF]**. **That is the Knob 1.8's exact configuration** — QSPI panel, I2S to
the PCM5100A DAC, PDM microphone, and 4-bit SDMMC.

**⚠ And on the S3 there is a hard number for display + camera together.** TRM-S3 v1.8 **p. 1091**
**[DOC]**: *"If an external camera and an external LCD are connected simultaneously, ensure that the
maximum data throughput on the interface is less than **GDMA total data bandwidth of 80 MB/s**."*
**[INF]** A 16-bit DVP camera at 20 MHz is 40 MB/s and a 16-bit RGB panel at 20 MHz is another
40 MB/s — together they consume the entire budget before any other GDMA client is considered. This is
the closest thing this library has to a quantification of pitfall 14 in §9. ⚠ **TRM-P4 v0.7 repeats
the warning at p. 2316 but drops the number**, so on P4 the budget is real and unquantified.

**The P4's `PPA` + `2D-DMA` pair is why LVGL performance on P4 is not comparable to a software-blit
S3 port** — stated in the [chip record §4](../../components/espressif/esp32-p4/README.md). The
*mechanism* is now documented: PPA does alpha blending, 0/90/180/270° rotation, bilinear scaling and
colour-space conversion in hardware (TRM-P4 §39.3, **p. 2256**), and 2D-DMA moves **rectangles** —
*"reads or writes a `hb`×`vb` macroblock… the address jumps to the address of the first data in the
next row"* (§8.4.1, **p. 829**), which is exactly a partial LVGL flush and costs one descriptor per
scanline on an S3. Mapped operation-by-operation in
[soc-peripheral-reference.md §16.7](../espressif/soc-peripheral-reference.md#167-esp32-p4--ppa-2d-dma-jpeg-and-h264).
**No benchmark exists anywhere in this library, or in the TRM, to quantify it** — capability is not
speedup.

> ✅ **Gap closed 2026-08-30.** This box previously read: *"[soc-peripheral-reference.md] has **no LCD
> or MIPI section**… Adding a §16 there would be the single highest-value extension to that page."*
> [§16](../espressif/soc-peripheral-reference.md#16-lcd-camera-and-display-peripherals) now exists and
> carries per-chip i80/RGB bus widths, pixel-clock ceilings, DSI and CSI lane rates and PHY revisions,
> PPA/2D-DMA/VDMA/JPEG/H.264 detail, the DMA map, and the resolution ceilings — all with printed page
> citations. What it **does not** contain is anything Espressif do not publish; those residuals are
> listed in §10 of this page.

---

## 5. Framebuffers, PSRAM and the arithmetic that decides the board

**This is the calculation that determines whether a panel is viable on a part, and it is the reason
every display-carrying device in this library has PSRAM.**

| Device | Resolution | Format | Single buffer | Double | Where it lives |
|---|---|---|---:|---:|---|
| [Knob 1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) | 360 × 360 | RGB565 | 259,200 B | 518,400 B | *neither* — panel has GRAM; LVGL uses **two 25.9 kB partial buffers** (§7) |
| [Tanmatsu](../../devices/nicolai-electronics/tanmatsu/display.md) | 800 × 480 | RGB565 | **768,000 B** | **1.5 MB** | **PSRAM, at 200 MHz — mandatory** |
| [P4 3.4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/features/display.md) | 800 × 800 | 24 bpp | **1.92 MB** | **3.84 MB** | PSRAM (32 MB fitted); demo uses `.num_fbs = 1` |
| [P4X-Function-EV](../../devices/espressif/esp32-p4x-function-ev-board/README.md) | 1024 × 600 | RGB565 | **1.2 MB** | **2.4 MB** | PSRAM — the [chip record §3](../../components/espressif/esp32-p4/README.md#3-memory-subsystem) uses exactly this example |
| [Inkplate 5 Gen 2](../../devices/soldered-electronics/inkplate-5-gen2/README.md) | 1280 × 720 | 1-bit + 4-bit | **900 KiB across four buffers** | — | PSRAM — `begin()` fails without it |

### 5.1 Three worked cases from the records

**Inkplate 5 Gen 2 — four buffers, not one.** A bare e-paper panel needs the new image, the previous
image, and a greyscale working buffer:

```c
memset(_partial,    0,   E_INK_WIDTH * E_INK_HEIGHT / 8);   // 115,200 B  (1 bit/px)
memset(DMemory4Bit, 255, E_INK_WIDTH * E_INK_HEIGHT / 2);   // 460,800 B  (4 bit/px)
```

Plus `DMemoryNew` 115 kB and `_pBuffer` 230 kB → **921,600 bytes**, all `ps_malloc`. Comfortably
beyond the ESP32's 520 kB internal SRAM. **This single number is why every Inkplate uses a
[WROVER](../../components/espressif/esp32-wrover/README.md) and not a WROOM.**

**Tanmatsu — PSRAM speed, not just size.** 800 × 480 × 2 B = 768 kB single, 1.5 MB double, and the
vendor is explicit: *"for ESP32-P4 projects … enabling the `experimental` high speed PSRAM feature is
a must. On Tanmatsu your app will not have enough memory for the framebuffer otherwise."* The exact
failure is diagnostic:

```
E (230) lcd.dsi.dpi: esp_lcd_new_panel_dpi(226): no memory for frame buffer
E (230) st7701_mipi: esp_lcd_new_panel_st7701_mipi(103): create MIPI DPI panel failed
```

**If you see that pair of lines it is the PSRAM clock, not the panel, not the DSI lanes, not the
driver.** The fix is three menuconfig steps: make experimental features visible → enable external
PSRAM → set PSRAM clock to **200 MHz** (the default is 20 MHz).

**P4 3.4C — capacity is not the constraint; bandwidth is.** 1.92 MB single / 3.84 MB double against
32 MB of PSRAM. The record's own framing: *"The board has 32 MB of PSRAM so capacity is not the
constraint — **bandwidth** is, especially with the camera streaming concurrently."* And then, honestly:
*"Display + camera + audio + SD running together is **untested and unmeasured**."*

### 5.2 The L2MEM trade-off, which is easy to miss

On the ESP32-P4 the 768 KB of L2MEM is **not simply 768 KB of RAM**. Per the
[chip record §3](../../components/espressif/esp32-p4/README.md#3-memory-subsystem), it is usable as
ordinary SRAM *or* reconfigurable as **L2 cache backing external PSRAM**:

> *"dedicating more L2MEM to cache raises effective PSRAM bandwidth for framebuffer work, and
> dedicating more to directly addressed SRAM gives you deterministic, low-latency working memory.
> … This is the single most important sizing question on the part and it is why the 32 MB variant
> exists."*

For a framebuffer-in-PSRAM design — which is every DSI board here — **cache allocation is a display
performance knob**, not just a memory-management detail.

### 5.3 The rule of thumb

**[INF]**, from the five rows above:

```
bytes = width × height × bytes_per_pixel × num_buffers
```

- Below ~**150 kB** you can stay in internal SRAM on an S3 and use a GRAM-owning panel (SPI/QSPI/i80).
- **150 kB – 1 MB** needs PSRAM, and probably a GRAM-owning panel still.
- Above ~**1 MB**, or any frame-owning transport (RGB, DSI video, e-paper), you need PSRAM **and** to
  care about its clock and cache configuration.
- The chip record's own threshold for choosing a P4 over an S3 is *"a display above roughly
  800 × 480"* — which is 768 kB at RGB565, i.e. exactly where this table's third band begins.

---

## 6. Tearing, TE lines, and what happens when TE is not routed

Tearing is what you see when the panel's scan-out reads a region of GRAM while you are writing it:
the top of the display shows the new frame and the bottom the old one. The standard fix is a **TE
(tearing effect) output** from the controller, telling the host when it is safe to write.

### 6.1 What a TE line actually gives you

From the [ST77916 programming reference §5](../../components/sitronix/st77916/st77916-programming-reference.md#5-tearing-effect)
**[DOC]** — spec-sourced numbers, which is rare for this class of part:

| Mode | `TEON` (`35h`) param | TE output content |
|---|---|---|
| Mode 1 | `0` (default) | **V-blanking only** |
| Mode 2 | `1` | V-blanking **and** H-blanking — one V-sync and **390 H-sync pulses per field** |

At 60 Hz, Idle Off, 25 °C **[DOC]**:

| Symbol | Meaning | Min |
|---|---|---:|
| `tvdl` | vertical low — **display *is* being updated from GRAM** | **13 ms** |
| `tvdh` | vertical high — **the safe window** | **1000 µs** |

> **The safe write window is under 8 % of the frame period.** Even *with* a TE line you could not
> blind-guess it by timing. That single ratio is the best argument for routing the pin.

The spec also gives two synchronisation strategies **[DOC]**: if the MPU write is *faster* than the
panel read, write during the V-sync pulse so data stays ahead of the scan; if it is *slower*, begin
writing just after a horizontal sync pulse so the write trails the read pointer and finishes before
the pointer catches up next frame.

### 6.2 Knob 1.8 — the pin exists on the connector and goes nowhere

`LCD_TE` reaches panel connector `U5` **pin 23** and **is not assigned to any ESP32-S3 GPIO** **[SCH]**.
The consequences are precise:

| Capability | Status |
|---|---|
| Sending `TEON` / `TEOFF` / `TESLWR` | ✅ still works — the controller will happily drive a pin nobody listens to. The stock SH8601 default table even sends `{0x44, {0x01, 0xD1}}` |
| Reading TE state via `RDDSM` (`0Eh`) | ⚠ possible in principle, but reads are broken at 40 MHz on this board (see §6.4) |
| **Synchronising a flush to V-blank** | ❌ **No. No electrical path to the MCU** |
| Observing the 1000 µs `tvdh` window | ❌ unobservable |
| LVGL `DIRECT` / `FULL` render mode with VSync | ❌ **use `PARTIAL` with the vendor's two-buffer scheme** |

**The only real mitigation without a TE line is to keep redraw regions small**, so that any given
flush completes well inside one scan pass. That is not a workaround bolted on afterwards — it is why
the vendor's LVGL configuration looks the way it does (§7).

### 6.3 Tanmatsu — the pin *is* wired, and nobody mentions it

The mirror image, and a genuinely useful find. The Badge.Team BSP (`tanmatsu_hardware.h`, MIT)
establishes **[SRC]**:

| Signal | ESP32-P4 GPIO |
|---|---:|
| LCD reset | **14** |
| **LCD TE (tearing effect)** | **11** — *"used to avoid tearing"* |

> *"A TE pin exists and is wired. That is worth knowing because tear-free updating is possible on
> this hardware, but only if your rendering loop actually uses GPIO11. **Nothing in the vendor
> documentation mentions it.**"*

So on the two devices where TE is most relevant, the library found **opposite** failures: the Knob
board's TE is unusable because the *hardware* omits the connection, and the Tanmatsu's is unused
because the *documentation* omits the pin. Both were established by reading primary artifacts — a
schematic in one case, a BSP header in the other — rather than vendor prose.

### 6.4 The other tearing mechanism: alignment, not timing

Not all smearing is a TE problem. The ST77916 **will not accept odd start or end coordinates** for a
GRAM write, so LVGL must snap every dirty area to a 2-pixel grid or you get *"tearing, smearing, or a
one-pixel diagonal drift on partial redraws — which looks like an LVGL bug and is not"*:

```c
void example_lvgl_rounder_cb(struct _lv_disp_drv_t *drv, lv_area_t *area) { /* snap to even */ }
...
disp_drv.rounder_cb = example_lvgl_rounder_cb;   // <-- easy to forget
```

> **This is the single thing most often lost when porting a working display setup from another board
> or migrating to LVGL 9.** There is no runtime warning. If you write your own flush path, port
> `rounder_cb` with it.

Related, and worth knowing before you try to debug any of this by reading registers: on this board
**reads fail at the 40 MHz bus clock** and require dropping to ≤ 6.67 MHz, and the correct read
opcode for the ST77916 is `0x0B`, not the `0x03` the generic shim defines.

### 6.5 MIPI-DSI video mode: TE is not the mechanism

> **Revised 2026-08-30.** This section was previously **[INF]** end to end and self-flagged as the
> weakest claim on the page. It has now been checked against TRM-P4 v0.7 and DS-P4 v0.7. **The
> conclusion survives; the reasoning was incomplete and one clause was wrong.**

**What is now [DOC].**

1. **The ESP32-P4's DSI pixel path is video mode only.** DS-P4 v0.7 §4.2.1.7, **p. 67** —
   *"Using the video mode to output video stream"*. TRM-P4 v0.7 §43.6.4, **p. 2662** — the only
   *"System memory data output flow"* is memory → VDMA → DSI Bridge → **DPI** → DSI Host. Command
   mode is §43.6.6, **pp. 2662–2663**: *"Using DCS command to **operate Display register**"*. There
   is no eDPI / command-mode-video framebuffer path on this part. (§3.5.)
2. **So in that mode there is genuinely no GRAM read pointer to race**, because the panel is not
   scanning out of its own memory — the host is the timing master. The original reasoning was right.
3. **The synchronisation hook that does exist is a VSYNC interrupt from the DSI Bridge**, not a TE
   pin: `DSI_BRG_VSYNC_INT`, with enable / raw / mask / clear bits in `DSI_BRG_INT_ENA_REG` (`0x0050`)
   and friends — TRM-P4 v0.7 **pp. 2685–2686**. Its companion is `DSI_BRG_UNDERRUN_INT`, *"triggered
   when DSI Bridge buffer underruns"* (Table 43.5-1, **p. 2657**), which is the failure mode you
   actually get if the framebuffer read cannot keep up. **The same structure exists on `LCD_CAM` for
   RGB/DPI panels**: `LCD_CAM_LCD_VSYNC_INT`, *"triggered when the LCD transmitted a VSYNC signal"*
   (TRM-S3 v1.8 §29.5, **p. 1091**; TRM-P4 v0.7 §40.4, **p. 2314**).

**⚠ What was wrong.** The §3.5 table used to say command mode is where *"a TE pin signals the safe
window"*, implying the P4 has no tearing-effect hardware at all. **It does.** Two register fields:

| Field | Register | Verbatim | Page |
|---|---|---|---|
| `DSI_HOST_TEAR_FX_EN` | `DSI_HOST_CMD_MODE_CFG_REG` (`0x0068`) | *"Configures whether to enable tearing effect acknowledge request."* | **2699** |
| `DSI_HOST_GEN_VCID_TEAR_AUTO` | `DSI_HOST_GEN_VCID_REG` (`0x0030`) | *"Configures hardware TEA effect virtual channel ID."* | **2693** |

**[INF]** That is the MIPI-DSI *TE-over-link* mechanism — DCS `set_tear_on`, the peripheral returns a
TE trigger message over the link, acknowledged with a bus-turnaround. **No physical TE wire is
involved.** Both fields live on the **Command Mode** side of the host, and since the P4 cannot send
pixel data in command mode (point 1), they are not the synchronisation mechanism for a video-mode
framebuffer. But *"the ESP32-P4 DSI has no TE support"* would be a false statement, and this page
came close to implying it.

**Where this leaves the practical advice — unchanged.** Tearing on a DSI video-mode panel is managed
by **when you write or swap the framebuffer** relative to frame output, which is why the Waveshare
demo's `.num_fbs = 1` is a substantive choice and not a detail: with one buffer there is nothing to
swap and the only defence is keeping writes small or timed. `DSI_BRG_VSYNC_INT` is the hook a
double-buffered design would use, and **no shipped demo in this library uses it**.

⚠ **Still not established.** Whether ESP-IDF's `esp_lcd` DSI driver exposes `DSI_BRG_VSYNC_INT` at
all, and what any of the three fitted panels do with `set_tear_on`. Neither is answerable from the
TRM. See §10.

---

## 7. LVGL integration and buffer sizing

Three of the library's display devices ship LVGL; one deliberately does not.

| Device | LVGL | Buffers | Notes |
|---|---|---|---|
| [Knob 1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/techniques.md) | **8.4.0** (ESP-IDF and Arduino) | **two × 360 × 36 px × 2 B = 25.9 kB each**, both `MALLOC_CAP_DMA` | 1/10 screen height; `rounder_cb` **mandatory**; LVGL task priority 2, **4 kB stack**, 2 ms tick |
| [P4 3.4C / 4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/features/display.md) | **8 *and* 9 demos both ship**; Arduino bundles **9.3.0** | `.num_fbs = 1` framebuffer in PSRAM | Round panel — LVGL's rectangular layouts waste the corners |
| [Inkplate 5 / Gen 2](../../devices/soldered-electronics/inkplate-5/README.md) | `Inkplate-LVGL-Library`, **GPL-3.0** | — | Separate repository, GPL — check licence compatibility before shipping |
| [Tanmatsu](../../devices/nicolai-electronics/tanmatsu/display.md) | **not used** | — | The ecosystem uses **PAX graphics** (Badge.team's library) |

### 7.1 The buffer-sizing gotcha

> **`MALLOC_CAP_DMA` is mandatory and it means internal RAM.** The Knob's two buffers take **~52 kB
> of internal DMA-capable RAM before your application allocates anything.** You cannot move them to
> PSRAM without also handling the fact that the QSPI DMA engine needs DMA-capable memory. If you
> enlarge them for smoother animation, **watch internal-RAM headroom, not total heap.**

That is the practical difference between the two families in this library. On a GRAM-owning panel
(Knob) LVGL buffers are small, internal, and DMA-constrained. On a frame-owning panel (P4, Tanmatsu)
the *framebuffer* is large and lives in PSRAM, and the constraint moves from internal-RAM headroom to
PSRAM bandwidth and cache configuration (§5.2).

### 7.2 Pin your LVGL major version deliberately

**LVGL 8 and 9 are not source-compatible.** The Waveshare P4 demo archive ships `09_lvgl_demo_v8`
*and* `10_lvgl_demo_v9` side by side while the Arduino tree bundles 9.3.0 — so a project can
accidentally straddle both. Migrating later is a rewrite of UI code, not a version bump.

### 7.3 ⚠ Check whether your vendor patched the bundled library

The single most transferable process finding in this area, from the
[shared XC record](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md):

| Board | Bundled library | Diffed against upstream | Result |
|---|---|---|---|
| Waveshare **P4 XC** | LVGL **9.3.0** | ✅ 2026-08-24 | **zero differing files — stock** |
| Waveshare **P4 XC** | Arduino_GFX **1.6.0** | ✅ 2026-08-24 | **zero differing files — stock** |
| Waveshare **Knob 1.8** | LVGL **8.4.0** | ✅ | **a real one-line functional patch** |

> *"Same vendor, same archive style, opposite answer — **run the check, don't assume.**"*

A related reproducibility hazard: the vendor demos declare their display components with
`version: '*'`. **Pin an explicit version in your own `idf_component.yml`**, or a future release
changes behaviour under you.

---

## 8. Init tables: the thing that is actually panel-specific

**A "display driver" is two things wearing one name**: a *transport* (how bytes reach the controller)
and an *initialisation table* (gamma, power, gate/source timing for the specific glass). The library
establishes, repeatedly, that **the transport is generic and the table is not.**

| Panel / controller | Init sequence | Where it lives |
|---|---|---|
| **JD9365**, Waveshare P4 | **~250 register writes** — gamma, gate timing, power | `06_/07_displaypanel/main/test_esp_lcd_jd9365.c` and `displays_config.h`. **Exactly one byte differs between the 3.4C and 4C: register `0x40` = `0x00` vs `0x04`.** What it controls is **unnamed** — no public Fitipower datasheet found |
| **ST77916**, Knob 1.8 | **~190 entries** — `F0`–`F3` page select, `B0`–`BD` panel control, `C0`–`CB` and `D0`–`D2` power, **14-byte `E0`/`E1` gamma tables** | Waveshare's `lcd_bsp.c` / `main.c` |
| **SH8601** (the generic shim's built-in default) | **three commands** — set tear scanline, TEON, `0x53` brightness | Never executed on the Knob board; Waveshare override it |
| **ST7701S**, Tanmatsu | panel-specific, packaged by the vendor | [`nicolaielectronics/mipi_dsi_abstraction`](../../components/sitronix/st7701s/README.md) |
| **ED052TC4** (no controller) | not an init table at all — a **waveform LUT** | [e-paper-displays.md §1.1](e-paper-displays.md#1-how-an-electrophoretic-display-actually-works) |

### 8.1 The lesson the ST77916/SH8601 case teaches

The Knob board's driver file is called `esp_lcd_sh8601.c`, its constructor is
`esp_lcd_new_panel_sh8601()`, its log tag is `"sh8601"`, and `lcd_bsp.c` even contains
`#define SH8601_ID 0x86`. **None of that is evidence about the silicon**, and the
[ST77916 record §2](../../components/sitronix/st77916/README.md) takes it apart:

- `SH8601_ID 0x86` is **dead code** — `#define`d alongside `CO5300_ID 0xff`, and **neither symbol is
  referenced anywhere in the file.** Nothing reads a controller ID register.
- `esp_lcd_sh8601` is a **generic QSPI-DCS transport shim** (§3.2). Everything controller-specific
  lives in the init table the *application* passes in.
- The table Waveshare pass is **unmistakably Sitronix** — `F0` page select and 14-byte `E0`/`E1`
  gamma are the signature — and unmistakably **not** AMOLED.
- **Decisive**: the panel has a **backlight** (`LCD_BLK` on GPIO47 driving an AO3400A gate). AMOLED
  panels are emissive and have none. **SH8601 is an AMOLED driver, therefore it is not an SH8601.**

> **The general rule: the driver filename is not evidence of the silicon.** The tell is always the
> same and always cheap: **does the board have a backlight?** `esp_lcd_sh8601.c` is the smallest,
> most complete, Apache-2.0 QSPI transport reference Espressif publishes, so every vendor bringing up
> *any* QSPI panel finds it, copies it, swaps the table and ships. The filename survives; the
> controller does not.

Two further init-table traps, both real:

- **The `MADCTL` double-send warning is expected, not a bug.** The shim sends `MADCTL` from
  `rgb_ele_order`, then the vendor table sends `0x36` again, and the driver logs *"The 36h command
  has been used and will be overwritten by external initialization sequence"*. **The table wins — set
  rotation there.** Same for `COLMOD` (`0x3A`); use `bits_per_pixel` instead of adding one.
- **Reset delays are load-bearing.** 10 ms low, **150 ms** after release. Shortening this produces
  intermittent blank panels.

---

## 9. Pitfalls, consolidated

Ordered by how much time each costs.

1. **Backlight polarity and count.** On the P4 3.4C, `BK_LIGHT_ON_LEVEL` is **0** — driving the pin
   high turns the backlight *off*. And there are **two** controls: PWM on GPIO26 and a separate
   `BL_EN` on GPIO33 that **no shipped demo touches**. *"A board that boots and renders correctly but
   looks black is usually this, not a DSI fault."* **Drive both.**
2. **Wrong panel variant selected.** Waveshare's Arduino library **defaults to the 3.4C**, so a stock
   build silently configures 800 × 800 on a 720 × 720 panel; use `06_` for the 3.4C and `07_` for the
   4C. On an Inkplate, choosing `Inkplate5` on a Gen 2 board gives the wrong resolution, waveform and
   clean sequence, **and it builds cleanly**.
3. **PSRAM not enabled, or at the wrong clock.** `no memory for frame buffer` on P4 (§5.1);
   `begin()` failure on an Inkplate.
4. **Forgetting `flags.use_qspi_interface = 1`.** Dead display, no error (§3.2).
5. **Forgetting `rounder_cb`.** Smearing that looks like an LVGL bug (§6.4).
6. **Expecting a TE line that is not routed** (§6.2).
7. **Expecting SPI-e-paper semantics from a bare panel** (§3.6).
8. **`max_transfer_sz` smaller than your largest flush.** Transfers are silently split or fail.
9. **Assuming the driver filename names the silicon** (§8.1).
10. **Floating component versions** (`version: '*'`) and unverified bundled libraries (§7.3).
11. **Porting an init table between panels** because "only one byte differs". You do not know what
    that byte does (§8).
12. **Ignoring the DSI PHY LDO** on ESP32-P4 (§3.5).
13. **Assuming a DSI-capable SoC means you should use DSI** (§3.1).
14. **Running display + camera + audio + SD concurrently and assuming it works.** Unmeasured
    anywhere in this library — but **on the ESP32-S3 there is now a documented budget to check it
    against**: *"the maximum data throughput on the interface [must be] less than GDMA total data
    bandwidth of **80 MB/s**"* when an external LCD and camera are both attached (TRM-S3 v1.8
    **p. 1091** **[DOC]**). ⚠ The P4 TRM repeats the warning without a number (p. 2316).
15. **Assuming an ESP32 (original) can drive an RGB/DPI panel.** It cannot — the sync signals exist
    only as camera *inputs* (§3.4). Budget an i80 panel, or a different part.
16. **Assuming a MIPI-DSI panel that needs command-mode pixel writes will work on a P4.** The P4's
    DSI pixel path is video mode only (§3.5, §6.5).

---

## 10. Gaps this guide cannot fill

**Updated 2026-08-30.** Several entries below moved from "extractable" to "extracted"; what remains is
either genuinely unpublished by Espressif, or needs hardware.

### 10.1 ✅ Closed since the last revision

| Was | Now |
|---|---|
| *"soc-peripheral-reference.md has no LCD/MIPI section… this is extractable work, not a research gap"* | **[§16 exists](../espressif/soc-peripheral-reference.md#16-lcd-camera-and-display-peripherals)** — bus widths, pixel-clock ceilings, DSI/CSI lane rates, PPA/2D-DMA/JPEG/H.264, DMA map, resolution ceilings, all with printed page citations |
| *"§6.5 (TE in DSI video mode) is inference… It should be verified."* | **Verified and corrected** (§6.5). The core claim is now **[DOC]**-backed three ways; one clause in §3.5 was **wrong** and has been fixed — the P4 DSI host *does* have tearing-effect registers, they just live in command mode |
| *"§3.3 and §3.4 rest on the LCD_CAM feature lists, not on any worked example"* | Still no worked example, but they now rest on **numbers**: pixel-clock ceilings per bus width, colour-format limits, and a documented reason the original ESP32 cannot do RGB at all |

### 10.2 Claims upgraded from [INF] to [DOC]

| Claim | Was | Now, with citation |
|---|---|---|
| The original ESP32 cannot drive an RGB/DPI panel | asserted from "no `LCD_CAM`" | **[DOC]** — the sync signals exist only as camera *inputs*, TRM-32 v5.8 Table 22.1-1 **p. 416**; §22.5 defines no RGB mode |
| ESP32 parallel LCD is an i80-style bus | implied | **[DOC]** — *"the WR signal of LCD connects to the WS signal of I2S"*, TRM-32 §22.5.1 **p. 426** |
| ESP32 LCD bus is 24 bits wide | not stated on this page | **[DOC]** **p. 426**, with the ⚠ *"I2S1 does not support 24-bit width"* restriction, **p. 416** |
| i80/RGB is "8 or 16 data lines" on S3 | generic industry statement | **[DOC]** — S3 is 8/16-bit (TRM-S3 **p. 1078**); **P4 is 8/16/24-bit** (TRM-P4 **p. 2300**) |
| "fast" for i80/RGB | unquantified | **[DOC]** — < 80 MHz at 8-bit, < 40 MHz at 16-bit, dropping to 60/30 MHz with YUV conversion (TRM-S3 **p. 1090**, TRM-P4 **pp. 2315–2316**) |
| DSI "1–4 lanes" generically; "2 lanes at 1500 Mbps" from a device record | vendor config | **[DOC]** — the P4 *has* 1 clock + 2 data lanes and 1.5 Gbps is the **silicon ceiling**, TRM-P4 **p. 2633** |
| DSI video mode has no TE mechanism | **[INF]**, self-flagged weakest | **[DOC]** for the pixel path being video-mode-only (DS-P4 **p. 67**, TRM-P4 **p. 2662**); **[DOC]** that a VSYNC interrupt is the hook instead (**pp. 2685–2686**); **[DOC]** that TE-over-link hardware exists in command mode (**pp. 2693, 2699**) |
| P4 PPA "accelerates LVGL" | vendor assertion | **[DOC]** for *which operations*: rotate 0/90/180/270°, bilinear scale, alpha blend, colour-key, CSC (TRM-P4 **p. 2256**); and that 2D-DMA moves rectangles natively (**p. 829**). **Still [INF] and unmeasured for how much faster** |
| Display + camera concurrently is "untested" | pitfall 14, unquantified | **[DOC]** budget on S3: **80 MB/s total GDMA**, TRM-S3 **p. 1091**. ⚠ still unquantified on P4 (**p. 2316** drops the number) |

### 10.3 Still open — and why

**Not extractable: Espressif do not publish these.**

- **⚠ No pixel-clock limit for the P4's 24-bit LCD bus.** The bus exists (TRM-P4 p. 2300); the notes
  on pp. 2315–2316 cover 8-bit and 16-bit only. **Do not extrapolate** — the 8→16 step already halves
  the ceiling, so "24-bit ⇒ < 26.7 MHz" would be a guess.
- **⚠ No GDMA bandwidth figure for the P4's LCD + camera concurrency.** TRM-P4 p. 2316 repeats the
  warning and drops the S3's "80 MB/s".
- **⚠ No maximum DSI resolution or refresh is stated.** The TRM gives the lane rate and the 240 MHz
  DPI ceiling and stops. The ceilings in
  [§16.9](../espressif/soc-peripheral-reference.md#169-which-target-drives-which-panel-class) are
  **[INF]** arithmetic from those two numbers.
- **⚠ Two documentation defects found, both in P4 pre-release v0.7.** (a) DS-P4 §4.2.1.3 p. 64 states
  the PPA scaling factor as *"4-bit integer part and 8-bit fractional part"*; the TRM (p. 2256) and
  the register layout (p. 2289) both say **8 integer + 4 fractional** — the datasheet is inverted.
  (b) TRM-P4 Table 43.5-1 (p. 2657) lists only `DSI_BRG_UNDERRUN_INT` as a DSI Bridge interrupt, but
  the register bank (pp. 2685–2686) defines `DSI_BRG_VSYNC_INT` as well. **Both should be re-checked
  against a released, non-`PRELIMINARY` revision.**
- **⚠ The `lcd_tx_wrx2_en` 2× question on the original ESP32 is still open** (§2.3). The TRM describes
  the two data-frame forms in prose but the distinguishing content is in **figures with no text
  layer**.

**Extractable, but from something we do not hold.**

- Whether ESP-IDF's `esp_lcd` DSI driver exposes `DSI_BRG_VSYNC_INT`, and what the three fitted DSI
  panels do with `set_tear_on`. This is a source-code question, not a TRM question (§6.5).

**Needs hardware or a benchmark.**

- **No i80 and no RGB parallel device exists in the library.** §3.3 and §3.4 now have numbers but
  still no worked example, pin map or measurement.
- **No frame rate, throughput or latency has ever been measured.** Every number in §2 and §16.8–16.9
  of the peripheral reference is arithmetic; every number in §5 is a byte count. **The P4's PPA/2D-DMA
  advantage over an S3 software blit is now documented as a capability and remains unquantified as a
  speedup** — Espressif publish no benchmark in either the TRM or the datasheet.

**Unrelated to the SoC.**

- **Five fitted display controllers have no component record** (§11): JD9365, ST7789VW, EK79007AD,
  EK73217BCGA, ILI9881C. The JD9365 is the most consequential — it drives two boards, its register
  `0x40` is the *only* difference between two products, and **no public Fitipower datasheet was
  found**.
- **No optical specification exists for any panel here.** Not the round LCD module (no part number,
  no manufacturer, no brightness, no viewing angle, no operating temperature), not the E Ink panels
  (§10 of the e-paper guide), and the Tanmatsu's `LH397K-IC01` datasheet was **not located** — SWI do
  not appear to publish it.
- **Reads are unresolved on the Knob board.** Whether the panel answers `RDDID`/`RDID1-3` over QSPI
  at a reduced clock is open, and it is the cheapest possible way to settle the remaining ~10 % doubt
  about the controller identity.


---

## 11. Every display controller in the library

### 11.1 With a component record

| Controller | Record | Interface(s) | Colour | Used by |
|---|---|---|---|---|
| **Sitronix ST77916** | [`sitronix/st77916`](../../components/sitronix/st77916/README.md) · [programming reference](../../components/sitronix/st77916/st77916-programming-reference.md) | **QSPI** (also 1-line SPI) | RGB565 used; **RGB888 *not* supported** — the programming reference corrects the main page | [Knob 1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md), 360 × 360 round @ 40 MHz |
| **Sitronix ST7701S** | [`sitronix/st7701s`](../../components/sitronix/st7701s/README.md) | **MIPI-DSI**, RGB parallel, SPI | up to RGB888; ⚠ [disputed in use](../markets/device-comparison-matrix.md#10-conflicts-between-records) | [Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md), `LH397K-IC01` 480 × 800, DSI 2-lane |
| **"SH8601"** — *software artefact, not silicon* | [`generic/sh8601-compatibility-driver`](../../components/generic/sh8601-compatibility-driver/README.md) | generic **QSPI-DCS transport shim** | — | [Knob 1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — **the driver, not the controller** (§8.1) |
| **1.8″ 360 × 360 round module** *(controller bonded inside, unidentified module)* | [`generic/lcd-panel-module`](../../components/generic/lcd-panel-module/README.md) | one 28-pin FPC carrying **QSPI + I²C touch + backlight** | RGB565 | [Knob 1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |
| **E Ink ED052TC4 / ED052TC2** — ⚠ **no controller at all** | [`e-ink/ed052tc4`](../../components/e-ink/ed052tc4/README.md) | **parallel DES**, 8-bit + 6 control lines | 8 grey levels as driven | [Inkplate 5](../../devices/soldered-electronics/inkplate-5/README.md) (TC2), [Gen 2](../../devices/soldered-electronics/inkplate-5-gen2/README.md) and [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md) (TC4) |

Supporting parts that are not controllers but are inseparable from driving one:

| Part | Record | Role |
|---|---|---|
| **TI TPS65186** | [`texas-instruments/tps65186`](../../components/texas-instruments/tps65186/README.md) | E-paper PMIC — every bias rail plus VCOM. **Read before touching an e-paper panel** |
| **NXP PCAL6416A** | [`nxp/pcal6416a`](../../components/nxp/pcal6416a/README.md) | I²C expander carrying `OE`, `GMOD`, `SPV` and all PMIC control |
| **AOS AO3400A** | [`alpha-and-omega-semiconductor/ao3400a`](../../components/alpha-and-omega-semiconductor/ao3400a/README.md) | Backlight low-side switch on the Knob 1.8 — and the part that **settles the AMOLED question** (§8.1) |
| **Espressif ESP32-WROVER** | [`espressif/esp32-wrover`](../../components/espressif/esp32-wrover/README.md) | The PSRAM that makes the e-paper framebuffers possible |

### 11.2 Fitted, named in a device record, **no component record**

These are real parts on real boards with no entry under [`components/`](../../components/README.md).

| Controller | Interface | Device | Documentation status |
|---|---|---|---|
| **JD9365** | MIPI-DSI, 2 lane @ 1500 Mbps | [P4 3.4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) (800 × 800) and [P4 4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md) (720 × 720) | ⚠ **No public Fitipower datasheet found.** ~250-entry init table and one undocumented byte, register `0x40`. Architecture partly reconstructed in [`display-controller-jd9365.md`](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/features/display-controller-jd9365.md). ESP-IDF component `espressif/esp_lcd_jd9365` |
| **ST7789VW** | SPI, 240 × 240 | [P4X-EYE](../../devices/espressif/esp32-p4x-eye/README.md) / [P4-EYE](../../devices/espressif/esp32-p4-eye/README.md), module `ZJY154KC-IF17` | Datasheet **retained** in [`shared-artifacts/`](../../devices/espressif/shared-artifacts/README.md), 3,135,599 B — was published under a percent-encoded Chinese filename |
| **EK79007AD** + **EK73217BCGA** | MIPI-DSI, 1024 × 600 | Espressif 7″ optional panel / LCD adapter board — [P4X-Function-EV](../../devices/espressif/esp32-p4x-function-ev-board/README.md), [P4X-C5](../../devices/espressif/esp32-p4x-c5-function-ev-board/README.md), [P4-Function-EV](../../devices/espressif/esp32-p4-function-ev-board/README.md) | Datasheets **retained** in [`shared-artifacts/`](../../devices/espressif/shared-artifacts/README.md). ESP-IDF component `esp_lcd_ek79007`. **Fitted on chip-revision v0.1 devkits** |
| **[ILI9881C](../../components/ilitek/ili9881c/README.md)** | MIPI-DSI | Espressif P4 devkit with **chip revision v0.0** — no board record here | Previously recorded here as `ILI9981C`, which **does not exist**; corrected 2026-08-30. ESP-IDF component `esp_lcd_ili9881c` |
| **LT8912B** | MIPI-DSI → **HDMI** | none in this library | Named in the same driver-abstraction table. ESP-IDF component `esp_lcd_lt8912b`. **The only DSI-to-HDMI path the library is aware of** |
| **`ED052TC2`** *(panel, no controller)* | parallel DES | [Inkplate 5](../../devices/soldered-electronics/inkplate-5/README.md) | Covered *by* the [ED052TC4 record](../../components/e-ink/ed052tc4/README.md) but has **no record of its own** |

### 11.3 Touch controllers, for completeness

Not display controllers, but they share the panel FPC and the I²C bus and are part of the same
bring-up.

| Part | Record | Points | Address | Used by |
|---|---|---|---|---|
| **Hynitron CST816D** | [`hynitron/cst816d`](../../components/hynitron/cst816d/README.md) | **single** | `0x15` | [Knob 1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — INT on GPIO9 is **never configured by the vendor driver**; it polls |
| **Goodix GT911** | [`goodix/gt911`](../../components/goodix/gt911/README.md) | 5 | **`0x5D` or `0x14`**, latched from INT during reset | Named in the [shared XC record](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md) — ⚠ [conflicts with GT9271](../markets/device-comparison-matrix.md#10-conflicts-between-records) |
| **Goodix GT9271** | [`goodix/gt9271`](../../components/goodix/gt9271/README.md) | >5, exact count **not established** | same pair, same strap | [P4 3.4C / 4C](../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md), driven by `esp_lcd_touch_gt911` |

Two integration facts worth carrying: **the GT911/GT9271 address is latched from the INT line state
during reset**, so if a bus scan finds nothing at `0x5D`, check `0x14` before assuming the part is
dead — and probe both rather than assuming. And on the P4 boards **the touch interrupt is not wired
to the SoC at all** (it terminates at test point TP2), so touch must be **polled**, while touch reset
on GPIO23 is wired but **untouched by every shipped demo**.

Finally: **five of the fourteen documented devices have no touch input of any kind**, and the two
largest displays in the library — the Inkplate 5 Gen 2 and the Tanmatsu — are explicitly not
touchscreens.

---

## Related

- **[E-paper displays](e-paper-displays.md)** — the deep treatment of the e-paper column
- **[Espressif SoC peripheral reference §16](../espressif/soc-peripheral-reference.md#16-lcd-camera-and-display-peripherals)** — **the numeric companion to this page.** Per-chip `LCD_CAM` bus widths and pixel-clock ceilings, MIPI-DSI/CSI lane rates and PHY revisions, PPA / 2D-DMA / VDMA / JPEG / H.264, the DMA map, and the resolution ceilings, all with printed TRM page numbers
- [Espressif SoC peripheral reference](../espressif/soc-peripheral-reference.md) — the rest of the numeric ESP32 / S3 / P4 tables behind §4
- [ESP-IoT-Solution components](../espressif/esp-iot-solution-components.md) — the LCD driver-interface selection table and touch-controller support
- [ESP-IDF peripheral capabilities](../espressif/esp-idf-peripheral-capabilities.md) · [Ecosystem and product lines](../espressif/ecosystem-and-product-lines.md)
- [Device comparison matrix](../markets/device-comparison-matrix.md) — the display column across all fourteen devices
- [ST77916 programming reference](../../components/sitronix/st77916/st77916-programming-reference.md) — command set, QSPI framing, TE timings, colour formats, power modes
- [Recovering netlists from vendor EDA files](../reverse-engineering/netlists-from-vendor-eda-files.md) — how several pinouts on this page were established
- [Component index](../../components/README.md) · [Device index](../../devices/README.md) · [Guides index](../README.md)

---

## Evidence boundary

**No new measurement, no hardware.** Every device- and panel-level fact is drawn from the records
linked inline, as they stood on **2026-08-30**, and carries their labels transitively.

**One addition since first compilation:** the SoC-level display facts in §3.3, §3.4, §3.5, §4 and
§6.5 were **extracted from the Espressif TRMs and datasheets held locally** on 2026-08-30 and are
labelled **[DOC]** with printed page numbers. They are consolidated in
[soc-peripheral-reference.md §16](../espressif/soc-peripheral-reference.md#16-lcd-camera-and-display-peripherals),
whose §16.10 records the exact page ranges read and the text-layer behaviour. **This page quotes
those figures; that page owns them.**

Specifically:

- **All arithmetic in §2 and §5.3 is [INF]**, performed here and shown so it can be checked. It is
  gross link capacity and byte counts. **It is not a frame rate**, deliberately — see §2.4. The DSI
  *link* figures it uses are now known to be the **silicon ceiling** rather than a vendor choice
  (**[DOC]**, TRM-P4 v0.7 p. 2633), which strengthens the conclusion without changing the numbers.
- **§4's peripheral rows are [DOC]** with per-row TRM page citations. The three boxed consequences
  are labelled **[INF]** in their source and remain so here; the fourth (the S3's **80 MB/s** GDMA
  budget for LCD + camera) is **[DOC]**, TRM-S3 v1.8 p. 1091.
- **§6.1 TE timings are [DOC]** from the ST77916 specification with page citations — unusually solid
  for this class of part, and they apply **to that controller only**.
- **§6.5 is no longer the weakest claim on this page.** Its core conclusion is now **[DOC]** from
  three independent places in DS-P4 and TRM-P4; one clause of the old §3.5 table was **wrong** and
  has been corrected. What remains **[INF]** there is the identification of `DSI_HOST_TEAR_FX_EN`
  with the MIPI TE-over-link protocol, and the practical advice about framebuffer timing.
- **§3.3 and §3.4 (i80, RGB parallel) still describe interfaces no documented device uses.** They now
  rest on TRM numbers rather than feature-list prose, but **no worked example, pin map or measurement
  exists here** and that has not changed.
- **The P4's PPA/2D-DMA advantage is [DOC] as a capability and [INF] as a benefit.** Which operations
  are accelerated is cited; *how much faster anything gets* is measured nowhere in this library and
  is not published by Espressif.
- **⚠ Everything sourced from ESP32-P4 documents is pre-release.** TRM-P4 and DS-P4 are both **v0.7**
  and the TRM is stamped `PRELIMINARY` on every page. Two internal contradictions were found in them
  (§10.3). Re-verify P4 figures against a released revision.
- **§8.1's conclusion is the ST77916 record's**, which assigns it ~90 % confidence with the residue
  being that a different Sitronix-alike would fit the same evidence.
- Panel identities, pin assignments and init-table contents are **[SCH]** and **[SRC]** from vendor
  schematics and vendor source code. **Nothing was verified against a physical board by anyone who
  wrote this.**

Where this guide and a device or component record disagree, **that record wins**. Where this guide
and [soc-peripheral-reference.md](../espressif/soc-peripheral-reference.md) disagree on an SoC figure,
**that page wins** — it cites the TRM directly.
