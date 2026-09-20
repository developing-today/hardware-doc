# Display — Tanmatsu

> The panel, the MIPI DSI path, the driver stack, and the configuration that must be right or nothing renders.
> Snapshot **2026-08-24**. Sources: Tanmatsu documentation (`bd3ded51`), production BOM (CERN-OHL-P), Espressif component registry.
> **No hardware was available** — no rendering, timing or brightness was measured.

---

## 1. The panel

| Property | Value |
|---|---|
| Model | **SWI `LH397K-IC01`** ([swicn.com](http://www.swicn.com/)) |
| Diagonal | **3.97"** |
| Active area | **51.84 × 86.40 mm** |
| Resolution | **480 × 800** (portrait native) |
| Colour | 65 536 colours (**16-bit RGB565**) in current software |
| Panel capability | **16.7 M colours (24-bit RGB888)** — *not currently used* |
| Controller | **Sitronix ST7701S** |
| Interface | **MIPI DSI, 2 data lanes** |
| Brightness | **330 cd/m²** |

The KiCad library contains a dedicated symbol for the panel: `library/LH397K-IC01.kicad_sym` — useful if you are designing a board around the same display.

**The RGB888 gap is a software limitation, not a hardware one.** The vendor states plainly: *"display supports 16M colors (24-bit / RGB888) but current software can not make use of this mode."* Interestingly, the BSP documentation says something subtly different — that for Tanmatsu *"888RGB and 565RGB are both valid options which will be honoured"*. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md); the safe assumption for now is **RGB565**.

Note the panel is **480×800 portrait** but the device is used in **landscape** (800×480 is how the marketing material describes it). Rotation is handled in software.

---

## 2. Electrical path

The display attaches to the mainboard through `CN1` — a **Hirose `DF37NB-24DS-0.4V(51)`** 24-pin 0.4 mm board-to-board connector, hidden under the front panel. It is factory-fitted; you should not normally need to touch it.

| Signal group | Detail |
|---|---|
| MIPI DSI | **three differential pairs** — 2 data lanes + 1 clock |
| Logic supply | 3.3 V |
| **Backlight supply** | **≈24 V @ 20 mA** rail |

### 2.1 Backlight is driven by the coprocessor, not the P4

This trips people up. The ~24 V backlight rail comes from an **`AP3032KTR`** boost LED driver (`U16` or `U18` — the board has two, one for the display and one for the keyboard). Its output current is set by a **PWM signal from the CH32V203 coprocessor**, on coprocessor pin **`PB4`** (`pin_display_backlight`).

So to change screen brightness you **write an I2C register on the coprocessor at address 0x5F**, not a P4 PWM peripheral:

| Register | Name |
|---|---|
| **`0x0B`** | `I2C_REG_DISPLAY_BACKLIGHT` |
| `0x0C` | `I2C_REG_KEYBOARD_BACKLIGHT` |

There is no direct GPIO from the ESP32-P4 to the backlight at all. If the coprocessor is not running or not addressed, the screen stays dark regardless of what the P4 renders.

---

## 2a. Additional pin and rail facts from the BSP

The Badge.Team BSP (`targets/tanmatsu/tanmatsu_hardware.h`, MIT, commit `9037f0e`) and badge.team's
ESP32-P4 pinout page supply display details the Tanmatsu documentation omits:

| Signal | ESP32-P4 GPIO | Notes |
|---|---:|---|
| **LCD reset** | **14** | Hardware reset for the ST7701S |
| **LCD TE (tearing effect)** | **11** | Frame-sync input — *"used to avoid tearing"* |

| Rail | Detail |
|---|---|
| **`BSP_DSI_LDO_CHAN`** | **3** — the MIPI PHY runs from ESP32-P4 **internal LDO channel 3** |
| **`BSP_DSI_LDO_VOLTAGE_MV`** | **2500** (2.5 V) |

The ESP32-P4's four internal LDO outputs are allocated on this board as
`VO1 = VFLASH`, `VO2 = VPSRAM`, `VO3 = VMIPI`, `VO4 = VSDCARD`. So **the DSI PHY supply is
software-controlled** — if LDO channel 3 is not brought up at 2.5 V, the display will not run no
matter how the panel driver is configured. (The same mechanism explains why expansion pins `E3`–`E6`
need "the VSDCARD LDO enabled": they sit in the `VO4` domain.)

**A TE pin exists and is wired.** That is worth knowing because tear-free updating is possible on
this hardware, but only if your rendering loop actually uses GPIO11. Nothing in the vendor
documentation mentions it.

## 2b. Refresh rate

Badge.Team describe the panel as a **"high resolution 60Hz screen"**
([badge.team Konsool docs](https://badge.team/docs/badges/konsool/), retrieved 2026-08-24) — the
only refresh-rate figure published by either vendor. Treat 60 Hz as the panel's nominal rate, not as
an achievable application frame rate; see [§7](#7-gaps-and-open-questions).

## 2c. Hardware video encoding

Also from badge.team, and absent from all Tanmatsu documentation:

> *"The ESP32-P4 also includes hardware-accelerated encoding of h264 video through its MIPI DSI and
> CSI interfaces. This powerful CPU can record video from devices such as a Raspberry Pi camera,
> encode it, and stream it wirelessly over WiFi."*

This is a significant capability for a device in this class and materially changes what the camera
port is good for. **Not verified here** — no hardware, and no example application in the app
repository exercises it.

---

## 3. Driver stack

Espressif's `esp_lcd_st7701` driver does the heavy lifting, but the **initialisation command sequence is panel-specific** and Nicolai Electronics package theirs in a component:

**[`nicolaielectronics/mipi_dsi_abstraction`](https://components.espressif.com/components/nicolaielectronics/mipi_dsi_abstraction)**

```bash
idf.py add-dependency "nicolaielectronics/mipi-dsi-abstraction"
```

It is an abstraction over several MIPI DSI panels:

| LCD controller | Espressif component | Used by |
|---|---|---|
| EK79007 | `esp_lcd_ek79007` | ESP32-P4-Function-EV-Board, **v0.1** chip kit |
| [ILI9881C](../../../components/ilitek/ili9881c/README.md) | `esp_lcd_ili9881c` | ESP32-P4 devkit, **v0.0** chip |
| **ST7701(S)** | `esp_lcd_st7701` | **Tanmatsu** |
| LT8912B | `esp_lcd_lt8912b` | MIPI DSI → HDMI adapter |

**Why this matters practically:** because the same component supports both the Tanmatsu panel *and* the official ESP32-P4 dev-kit displays, **you can develop Tanmatsu display code on an Espressif P4 devkit** and switch targets with configuration rather than a rewrite. The BSP carries an `esp32-p4-function-ev-board` target for exactly this reason.

Note the two different dev-kit panels tied to **chip revision** (v0.0 → ILI9881C, v0.1 → EK79007). If you are cross-developing, check which devkit you have.

The component's own caveat is honest and worth heeding:

> *"This component was made to facilitate easier testing for our firmwares on both the devkits and our target hardware and thus the configurations we use are the only supported display configurations."*

It is not a general-purpose DSI panel library. Licence on the example code: **CC0-1.0**.

---

## 4. The configuration you must get right

This is the highest-value section of this document. There are **three** ESP-IDF settings that are not defaults, and getting them wrong produces failures that look like driver bugs.

### 4.1 Enable high-speed PSRAM — or the framebuffer will not allocate

An 800×480 16-bit framebuffer is 768 000 bytes; double-buffered, 1.5 MB. That must live in PSRAM, and **the ESP32-P4's PSRAM must be run at 200 MHz**, which is behind ESP-IDF's *experimental features* flag.

The vendor states it flatly: *"for ESP32-P4 projects (Tanmatsu projects) enabling the `experimental` high speed PSRAM feature is a must. On Tanmatsu your app will not have enough memory for the framebuffer otherwise."*

**The exact failure:**

```
E (230) lcd.dsi.dpi: esp_lcd_new_panel_dpi(226): no memory for frame buffer
E (230) st7701_mipi: esp_lcd_new_panel_st7701_mipi(103): create MIPI DPI panel failed
```

If you see that pair of lines, this is your problem — not the panel, not the DSI lanes, not the driver.

**Fix, in `idf.py menuconfig`:**

1. Main menu → enable **`Make experimental features visible`**
2. `Component config` → `ESP PSRAM` → **`Support for external PSRAM`**
3. Enter the new `PSRAM config` menu → `Set PSRAM clock speed` → select **`200MHz clock speed`** (the default is 20 MHz)

### 4.2 Select the BSP target

The `badge-bsp` component defaults to a **stub target** that does nothing.

`Component config` → `Badge.Team BSP` → `Board (...)` → **`Nicolai Electronics Tanmatsu`**

### 4.3 Reserve RTC retained memory

`badge-bsp` requires a user section in RTC FAST memory, which is not enabled by default.

`Bootloader config` → **`Reserve RTC FAST memory for custom purposes`** → set **`Size in bytes for custom purposes` = `0x100`**

Then `q`, `y` to save, and rebuild:

```bash
idf.py build flash monitor --port /dev/ttyACM0
```

> Status: **`reported-working`** — all three steps and the error text are quoted from the vendor's "ESP-IDF from scratch" guide. Not executed here.

---

## 5. Bringing the display up

The BSP handles initialisation; you generally do not talk to `esp_lcd` directly:

```c
esp_err_t res = bsp_device_initialize(&bsp_configuration);
if (res != ESP_OK) {
    printf("Failed to initialize BSP\r\n");
    return;
}
```

**Colour format is negotiated, not commanded.** The BSP documentation notes: *"the color format provided can differ from the requested color format depending on the target hardware, for Tanmatsu 888RGB and 565RGB are both valid options which will be honoured, but for other targets this does not have to be the case."*

So **read back** the format the BSP gives you rather than assuming your request was honoured — code that hard-codes RGB565 pixel packing will produce garbage on a target that hands you RGB888.

For 2D drawing, the ecosystem uses **PAX graphics** (Badge.team's library); the [`tanmatsu-template`](https://github.com/Nicolai-Electronics/tanmatsu-template) app is built around it.

---

## 6. Spare parts and repair

Nicolai Electronics: *"The display will be available as a spare part from our webshop once Tanmatsu is shipped."*

The display sits behind the front panel on a 0.4 mm-pitch B2B connector. That pitch is not hand-solderable in practice, but the connector is *mateable* — a display swap is a mechanical operation, not a soldering one, provided you do not damage `CN1`.

---

## 7. Gaps and open questions

| Question | Status |
|---|---|
| Is RGB888 usable or not? | **Conflict.** The specifications page says software "can not make use of this mode"; the BSP guide says 888RGB "will be honoured" on Tanmatsu. Unresolved — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |
| Achievable frame rate | **Unknown.** No figure published, none measured. DSI 2-lane at 800×480 is not the bottleneck; PSRAM bandwidth and the drawing library likely are |
| Backlight PWM frequency and dimming curve | **Unknown.** Register `0x0B` is documented as a value, with no stated scale or linearity |
| Panel datasheet | **Not located.** SWI (swicn.com) does not appear to publish `LH397K-IC01` publicly. The KiCad symbol is the best local reference |
| Actual power draw of the backlight | ~24 V @ 20 mA is the rail spec — that is ≈0.5 W at full brightness, but the real curve is unmeasured |
| Touch input | **There is none.** The panel is not a touchscreen; input is the keyboard |
| Display rotation handling | Panel is native 480×800 portrait, used as 800×480 landscape. Where the rotation happens (driver, PAX, or panel command) was **not traced** |

## Related

- [`README.md`](README.md) — device overview
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — CN1, coprocessor I2C
- [`keyboard.md`](keyboard.md) — the other half of the human interface, and the same coprocessor backlight mechanism
- [`development.md`](development.md) — full toolchain setup
- [`bom.md`](bom.md) — `CN1`, `U16`/`U18` backlight drivers
