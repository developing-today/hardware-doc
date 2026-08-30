# Hynitron CST816D / CST816 family

- **Category:** self-capacitance touch controller with on-chip gesture engine, I²C slave interface
- **Research status:** datasheet (EN v1.3) held locally and read in full; **the register map is *not* in it** and is reconstructed from two independent vendor drivers shipped with this board. That distinction is maintained explicitly throughout — see §3.
- **Retrieved:** 2026-08-21

The touch controller of the round 360 × 360 panel on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md). It sits at I²C address **`0x15`**, shares a bus with the [DRV2605L haptic driver](../../texas-instruments/drv2605l/README.md), and has both `INT` and `RST` wired to the ESP32-S3.

The thing to internalise before writing any code: **Hynitron's public datasheet documents the chip's electricals, packaging and I²C *timing*, but contains no register map at all.** Everything anyone knows about registers `0x00`–`0xFE` comes from vendor-supplied drivers and reverse engineering. §3 says so explicitly and labels every register accordingly.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[SCH]** | Read directly off the board schematic PNGs in `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/` |
| **[DOC]** | Stated by Hynitron in `artifacts/cst816d-datasheet-v1.3.pdf` |
| **[SRC]** | Read out of driver source shipped in the device's `artifacts/demo/` tree |
| **[COM]** | Community evidence — GitHub issue, library, forum. Attributed |
| **[INF]** | Inference. Not established by the above |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Hynitron** — Shanghai Hynitron Technology Co., Ltd (上海海栎创科技股份有限公司) | **[DOC]** |
| Part | `CST816D` | **[DOC]** the local datasheet is the CST816D document, English **V1.3** |
| Package | **QFN 3 × 3 mm, 20-lead** (`QFN3X3-20L`) | **[DOC]** §5 ordering information |
| Top marking | Dot = pin-1 mark; `CST816D`; `XXXXX` = 5-digit production tracking code | **[DOC]** §5 |
| Packing | Tape-and-reel, 5000 pcs | **[DOC]** §5 |
| ⚠ Fitted part verified? | **No.** The controller is inside the bonded panel module and its marking is not visible in any published image or schematic. `CST816D` is the best-supported family identification, not a verified top marking | **[INF]** |
| Chip-ID register value | `0xB6` for CST816D | **[SRC]** — §3.3 |
| Touch points | **Single point** for coordinates; "real two-point operation" for gestures | **[DOC]** §1, §7.1; **[SRC]** every driver treats it as single-touch |
| Sensing channels | Up to **13** | **[DOC]** §2 |
| Report rate | **> 100 Hz** | **[DOC]** §2 |

### 1.1 The CST816 family, and why the letter matters

Hynitron ships several near-identical parts. **They are not interchangeable in software**, because they differ in chip ID, in whether the auto-sleep register exists, and in gesture behaviour. **[SRC]** from `TouchDrvCST816.cpp`/`.h` in the bundled SensorLib:

| Part | Chip ID (`0xA7`) | Notes |
|---|---:|---|
| CST716 | `0x20` | Older; **does not support the `0xFE` auto-sleep-disable register** — the driver has an explicit special case |
| CST816S | `0xB4` | The most common in the wild; most community libraries target this |
| CST816T | `0xB5` | **Known to return all-`0xFF`** from the status block after auto-sleep is disabled — the driver checks for this explicitly |
| **CST816D** | **`0xB6`** | This board's identification |
| CST820 | `0xB7` | |
| CST226SE | reads `0x20` at `0xA7` | Multi-touch; a *different* driver (`TouchDrvCST226`). Colliding ID with CST716, which is why the CST716 case also tests the firmware-version register |

**Read `0xA7` at bring-up and log it.** It is one I²C transaction and it removes all ambiguity. §7.1.

### 1.2 Lifecycle and documentation quality

Hynitron does not run a Western-style documentation portal. The CST816D datasheet in `artifacts/` is the one **Waveshare** mirrors (`files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf`) and is the most authoritative English document that circulates. It is 8 pages of substance and, as noted, has **no register map**. Treat any "CST816 datasheet with registers" you find online as a community compilation unless it carries a Hynitron header.

---

## 2. Electrical and timing specifications

**[DOC]** §9.

### 2.1 Absolute maximum ratings

| Symbol | Parameter | Min | Max | Unit |
|---|---|---:|---:|---|
| `TSTG` | Storage temperature | −40 | 125 | °C |
| `Ta` | Operating ambient temperature | **−20** | **85** | °C |
| `Vdd` | Supply relative to Vss | −0.3 | **+3.6** | V |
| `Vio` | DC input voltage | VSS − 0.3 | VDD + 0.3 | V |
| `LU` | Latch-up current | | 200 | mA |
| CDM | ESD, charged-device model | | 1000 | V |
| HBM | ESD, human-body model | | **8000** | V |

Note the **−20 °C** lower operating limit — narrower than most of this board's other parts, several of which go to −40 °C. If you are deploying this device outdoors in winter, the touch controller is your limiting component. **[DOC]**

### 2.2 Supply and power

| Parameter | Value | Evidence |
|---|---|---|
| Supply voltage | **2.8 – 3.6 V**, ripple ≤ **50 mV** | **[DOC]** §2 |
| I/O level compatibility | **1.8 V / 3.3 V** | **[DOC]** §2 |
| Dynamic-mode current | **1.8 mA** typ | **[DOC]** §2 |
| Sleep-mode current | **2 µA** typ | **[DOC]** §2 |

The 50 mV ripple limit is worth respecting. Capacitive sensing is sensitive to supply noise, and Hynitron devotes §8.6 to grounding advice (star ground, ferrite bead in the ground return, separate the touch ground from high-current device grounds).

### 2.3 AC characteristics

| Symbol | Parameter | Typ |
|---|---|---:|
| `Fcpu` | Internal CPU frequency | 20 MHz ±2 % |
| `F32k` | Internal low-speed clock | 32 kHz ±5 % |
| `txRST` | External reset pulse width | 0.1 ms |
| `tPOWERUP` | POR end → CPU executing code | 4 ms |
| `FGPIO` | GPIO switching frequency | 2 MHz |
| `tRISE` | Pin rise time, Cload = 50 pF | 32 ns |

### 2.4 ⚠ Power-on and reset timing — the numbers that break naïve drivers

**[DOC]** §7.1. **These are the most commonly violated constraints on this chip.**

| Symbol | Description | Min | Unit |
|---|---|---:|---|
| **`Tpor`** | **Chip initialization time after power-on** | **100** | **ms** |
| `Tpr` | `RST` pin delayed pull-up time | 5 | ms |
| **`Tron`** | **Chip re-initialization time after reset** | **100** | **ms** |
| `Trst` | Reset pulse width | 0.1 | ms |

**You must wait 100 ms after power-on, and 100 ms after releasing `RST`, before the chip will answer I²C.** A driver that resets and immediately reads gets a NACK or garbage. See §6.4 — one of the two vendor drivers on this board gets this wrong.

### 2.5 I²C timing

**[DOC]** §7.6(g). Standard-ish, but note the rate ceiling.

| Symbol | Parameter | Min | Max | Unit |
|---|---|---:|---:|---|
| `Fscl` | SCL clock frequency | 10 | **400** | kHz |
| `Tst1` | START hold time | 0.6 | | µs |
| `Tlo` | SCL low period | 1.3 | | µs |
| `Thi` | SCL high period | 0.6 | | µs |
| `Tds` | SDA setup | 0.6 | | µs |
| `Tdh` | SDA hold | 100 | | ns |
| `Tst2` | STOP setup | 0.6 | | µs |
| `Tbuf` | Bus free between STOP and START | 4.5 | | µs |

> **⚠ 400 kHz is the maximum, and Hynitron says so twice** ("the rate is 10 kHz ~ 400 kHz configurable" §2; "it is recommended to use a maximum communication rate of 400 Kbps" §7.6(b)). **Waveshare's own example runs the bus at 300 kHz** **[SRC]** — inside spec. But see §7.3: some community code runs this bus at 400 kHz *with the DRV2605L on it*, and the DRV2605L's own limit is what binds then.

### 2.6 Other design notes from the datasheet

- **`CMOD0`/`CMOD1` regulator capacitors** must be **1 nF – 5.6 nF, NPO/COG, ≥10 % accuracy**, placed as close to the pins as possible. Generally 1 nF. **[DOC]** §4, §8.2. Not adjustable from the outside on this board — the panel module is bonded — but relevant if you are designing your own.
- **`RST` may be left floating.** The chip has a built-in power-on-reset. **[DOC]** §7.1. This board wires it anyway, which is better.
- **`IRQ` edge is configurable** — rising or falling. **[DOC]** §7.5. Which one *your* panel's firmware uses is a per-project configuration Hynitron makes at the module level. §7.2.
- **`SCL`/`SDA` support internal pull-up as well as open-drain**, selectable. **[DOC]** §7.4. This board fits external 5.1 kΩ pull-ups anyway **[SCH]**.

---

## 3. ⚠ Register map — provenance warning

**The Hynitron CST816D datasheet contains no register map.** It documents I²C *framing* (single-byte write, multi-byte write, single-byte read, multi-byte read) and *timing*, and it uses `0x1E`, `0x1F` and `0x21` as arbitrary examples in the framing diagrams — with no statement of what those registers do. **[DOC]** §7.6(c)–(f).

Everything below is therefore **[SRC]** or **[COM]**, not **[DOC]**. It is nonetheless reliable: the same map appears independently in Waveshare's minimal driver, in Lewis He's SensorLib, and in essentially every community CST816 library, and it is corroborated by the on-wire behaviour those drivers depend on.

### 3.1 The status block — registers `0x00`–`0x06`

Both drivers on this board read **7 bytes starting at `0x00`** in one transaction **[SRC]**:

| Offset | Register | Contents | Notes |
|---:|---|---|---|
| 0 | `0x00` | Mode / `GestureID` **[COM]** | Written with `0x00` at init by both vendor drivers to "switch to normal mode" **[SRC]** |
| 1 | `0x01` | `Gesture` **[COM]** | Neither vendor driver reads it. §4 |
| 2 | `0x02` | **`FingerNum`** | Low nibble = number of touch points. `0` ⇒ no touch **[SRC]** |
| 3 | `0x03` | `XposH` | **Low 4 bits** are X[11:8]; the **high 4 bits are the event flag** **[COM]** |
| 4 | `0x04` | `XposL` | X[7:0] |
| 5 | `0x05` | `YposH` | **Low 4 bits** are Y[11:8] |
| 6 | `0x06` | `YposL` | Y[7:0] |

Coordinate assembly, verbatim from both vendor drivers **[SRC]**:

~~~c
x = ((uint16_t)(data[3] & 0x0F) << 8) + (uint16_t)data[4];
y = ((uint16_t)(data[5] & 0x0F) << 8) + (uint16_t)data[6];
~~~

The `& 0x0F` is **mandatory**. The upper nibble of `0x03` carries a touch-event code (community consensus: `0` = press down, `1` = lift up, `2` = contact) and will corrupt your X coordinate by up to 4096 if you forget to mask it. **[COM]**

### 3.2 Control and identity registers

**[SRC]** from `TouchDrvCST816.h` in the bundled SensorLib 0.3.1:

| Register | Name | Value / meaning |
|---:|---|---|
| `0xA7` | **`CHIP_ID`** | `0x20` CST716 · `0xB4` CST816S · `0xB5` CST816T · **`0xB6` CST816D** · `0xB7` CST820 |
| `0xA9` | **`FW_VERSION`** | Firmware version. Used together with `0xA7` to disambiguate CST716 from CST226SE (both read `0x20`) |
| `0xE5` | **`SLEEP`** | Write **`0x03`** to enter deep sleep. Exit only by pulsing `RST` |
| `0xFE` | **`DIS_AUTOSLEEP`** | Write `0x01` to **disable** the 2-second auto-sleep; `0x00` to re-enable. **Not present on CST716** |

Community sources add these; treat as **[COM]** and verify before relying on them:

| Register | Name | Meaning |
|---:|---|---|
| `0xEC` | `AutoReset` | Time in seconds with touch but no gesture before auto-reset |
| `0xED` | `LongPressTime` | Long-press auto-reset time, seconds |
| `0xFA` | `IrqCtl` | Interrupt behaviour bitfield: bit 7 `EnTest`, bit 6 `EnTouch`, bit 5 `EnChange`, bit 4 `EnMotion`, bit 0 `OnceWLP` |
| `0xEE` | `MotionMask` | Bit 0 `EnDClick` (double-click), bit 1 `EnConUD` (continuous up/down), bit 2 `EnConLR` |
| `0xEB` | `DisAutoSleep` on some variants | Conflicting reports — prefer `0xFE` |

### 3.3 Working mode state machine

**[DOC]** §7.2 — this part *is* documented.

| Mode | Entered by | Exited by | Current |
|---|---|---|---|
| **Dynamic** | Touch activity | 2 s without touch → Standby (register-controllable) | 1.8 mA |
| **Standby** | 2 s idle | Touch | between the two |
| **Sleep** | The sleep command (`0xE5` ← `0x03`) | **`RST` pin only** | 2 µA |

> **⚠ Sleep is a one-way door without `RST`.** Hynitron: "In this mode, the touch chip is in a deep sleep state … and **can be switched to dynamic mode through the reset pin**." **[DOC]** §7.2. If you put the chip to sleep and your `RST` GPIO is not wired or not driven, the only recovery is a power cycle. On this board `RST` **is** wired, to S3 GPIO10 **[SCH]** — use it.

---

## 4. The gesture engine

**[DOC]** §1, §2: the chip supports "single-point gestures and real two-point operation", "supports multiple keys", and — importantly for a battery device — **"supports sleep gesture wake-up"**, where the `IRQ` pin wakes the host when a predefined gesture is matched in standby.

The gesture codes are read from register `0x01` and are **[COM]**, universally agreed across community libraries:

| Value | Gesture |
|---:|---|
| `0x00` | None |
| `0x01` | Slide up |
| `0x02` | Slide down |
| `0x03` | Slide left |
| `0x04` | Slide right |
| `0x05` | Single click |
| `0x0B` | Double click |
| `0x0C` | Long press |

> **⚠ Neither driver shipped with this board reads the gesture register.** Waveshare's `cst816.cpp` and `lcd_touch_bsp.c` both read 7 bytes from `0x00` and use only `data[2]`, `data[3..6]` **[SRC]**. SensorLib's `TouchDrvCST816` reads 13 bytes and also ignores `0x01`, though it does expose a `HomeButtonCallback` hook. **If you want gestures, you have to add the read yourself** — it is `data[1]` of a block you are already fetching, so it costs nothing.
>
> This is arguably the largest piece of unused hardware capability on the board: a 360 × 360 round watch-style UI is exactly the use case the gesture engine exists for, and LVGL has native gesture events (`LV_EVENT_GESTURE`) ready to receive them. **[INF]**

Whether the specific gesture set is enabled in *your* panel's controller firmware is a per-module configuration. Hynitron: "The iic address of some projects may be different, please consult the corresponding project and engineering personnel" **[DOC]** §7.6(a) — the same caveat applies to gesture configuration.

---

## 5. Exact wiring on this board

**[SCH]**, cross-checked against **[SRC]** `lcd_config.h`.

| Signal | ESP32-S3 GPIO | Notes |
|---|---:|---|
| `SDA` | **GPIO11** (`TP_SDA` / `HAPTIC_SDA`) | Shared bus. Pull-up `R5` **5.1 kΩ** to 3V3 |
| `SCL` | **GPIO12** (`TP_SCL` / `HAPTIC_SCL`) | Shared bus. Pull-up `R6` **5.1 kΩ** to 3V3 |
| `INT` / `IRQ` | **GPIO9** (`TP_INT`) | No pull resistor drawn |
| `RST` | **GPIO10** (`TP_RST`) | Active low |
| Supply | 3.3 V | Inside the bonded panel module |

**I²C address `0x15`** (7-bit) ⇒ write address `0x2A`, read address `0x2B` **[DOC]** §7.6(a). Confirmed by `#define EXAMPLE_TOUCH_ADDR 0x15` **[SRC]**.

### 5.1 The shared bus

`I2C0` on GPIO11/12 carries **two** devices:

| Device | Address | Max I²C rate |
|---|---:|---|
| CST816D touch | `0x15` | **400 kHz** **[DOC]** |
| [DRV2605L haptic](../../texas-instruments/drv2605l/README.md) | `0x5A` | 400 kHz |

No conflict, and both tolerate 400 kHz — but you must serialise access from a single I²C driver instance, and if you drive the haptic motor from an ISR while polling touch you need a mutex. **Waveshare's ESP-IDF examples factor this into a shared `i2c_bsp` component** **[SRC]**, which is the right pattern; the Arduino examples each open their own bus, which is not.

### 5.2 Rotation

`lcd_config.h` carries a commented-out `#define EXAMPLE_Rotate_90`, and `lcd_bsp.c` applies the matching transform in the LVGL read callback **[SRC]**:

~~~c
#ifdef EXAMPLE_Rotate_90
    data->point.x = tp_y;
    data->point.y = (EXAMPLE_LCD_V_RES - tp_x);
#else
    data->point.x = tp_x;
    data->point.y = tp_y;
#endif
~~~

Note that touch rotation is applied **in software on the host**, while display rotation is done by writing MADCTL (`0x36` ← `0x60`) to the [display controller](../../sitronix/st77916/README.md). **The two are independent switches and it is easy to rotate one and not the other.** If touch lands 90° off, this is why.

---

## 6. Drivers: what to use, and what ships

### 6.1 Summary

| Framework | Recommended | Where |
|---|---|---|
| **ESP-IDF** | `espressif/esp_lcd_touch_cst816s` | Component registry. Integrates with `esp_lcd_touch` and therefore with `esp_lvgl_port` cleanly |
| **ESP-IDF (minimal)** | Waveshare's `lcd_touch_bsp` | 30 lines, in the demo archive. Fine for simple use; see §6.4 |
| **Arduino** | `SensorLib` by Lewis He — `TouchDrvCST816` | <https://github.com/lewisxhe/SensorLib>. Bundled at **v0.3.1** in this board's demo **[SRC]** |
| **Arduino (minimal)** | Waveshare's `cst816.cpp` | In the demo archive |
| **LVGL** | Any of the above behind an `lv_indev_drv_t` with `LV_INDEV_TYPE_POINTER` | |

### 6.2 `esp_lcd_touch_cst816s` (ESP-IDF, recommended)

~~~yaml
# main/idf_component.yml
dependencies:
  espressif/esp_lcd_touch_cst816s: "^1.0.0"
~~~

~~~c
#include "esp_lcd_touch_cst816s.h"

esp_lcd_panel_io_handle_t tp_io = NULL;
esp_lcd_panel_io_i2c_config_t tp_io_cfg = ESP_LCD_TOUCH_IO_I2C_CST816S_CONFIG();
ESP_ERROR_CHECK(esp_lcd_new_panel_io_i2c((esp_lcd_i2c_bus_handle_t)I2C_NUM_0, &tp_io_cfg, &tp_io));

esp_lcd_touch_config_t tp_cfg = {
    .x_max = 360, .y_max = 360,
    .rst_gpio_num = GPIO_NUM_10,
    .int_gpio_num = GPIO_NUM_9,
    .levels = { .reset = 0, .interrupt = 0 },
    .flags  = { .swap_xy = 0, .mirror_x = 0, .mirror_y = 0 },
};
esp_lcd_touch_handle_t tp = NULL;
ESP_ERROR_CHECK(esp_lcd_touch_new_i2c_cst816s(tp_io, &tp_cfg, &tp));
~~~

Despite the `cst816s` name it works with CST816D — same protocol, different chip ID. **[INF]**, corroborated by widespread community use. **[COM]**

### 6.3 SensorLib (Arduino / ESP-IDF)

Bundled at **v0.3.1** **[SRC]**. Offers `begin()` overloads for Arduino `TwoWire`, the ESP-IDF legacy `i2c_port_t` API, the new `i2c_master_bus_handle_t` API, and a custom-callback shim — which is why it drops cleanly into either framework.

~~~cpp
#include "TouchDrvCST816.h"
TouchDrvCST816 touch;

touch.setPins(/*rst*/ 10, /*irq*/ 9);
if (!touch.begin(Wire, CST816_SLAVE_ADDRESS /*0x15*/, /*sda*/ 11, /*scl*/ 12)) { /* ... */ }
Serial.println(touch.getModelName());     // "CST816D" if 0xA7 reads 0xB6

int16_t x[1], y[1];
if (touch.getPoint(x, y, 1)) { /* ... */ }
touch.disableAutoSleep();                 // writes 0xFE <- 0x01
~~~

`TouchDrvCST816::reset()` implements the sequence correctly: `RST` low, **30 ms**, `RST` high, **50 ms** **[SRC]**. See §6.4.

### 6.4 ⚠ What the vendor's own minimal driver gets wrong

Waveshare's `cst816.cpp` (Arduino) and `lcd_touch_bsp.c` (ESP-IDF) are 30-line drivers **[SRC]**. They work, but they omit four things:

| Omission | Consequence |
|---|---|
| **Never asserts `RST`.** `Touch_Init()` goes straight to an I²C write | Relies entirely on the chip's internal POR. Works from cold boot; **may fail after a soft reset of the S3**, where the S3 restarts but the touch controller does not, potentially mid-transaction **[INF]** |
| **No `Tpor`/`Tron` delay.** No 100 ms wait anywhere | On a fast-booting app the first I²C write can land before the controller is ready. §2.4 |
| **Never reads `0xA7`.** No chip-ID check | You get no diagnostic if the part is a CST816S/T/820 with different quirks — or if the bus is dead |
| **Ignores I²C return codes.** `I2C_read_buff()` returns `ret` but `getTouch()` discards it | A NACKed read leaves `data[]` as stale zeros, which reads as "no touch". **A completely dead touch controller is indistinguishable from a finger-free screen.** This is the single most misleading behaviour in the shipped code |

Also note `Touch_Init()` calls `i2c_driver_install()` itself, so it **conflicts with any other code that installs `I2C_NUM_0`** — including the DRV2605L examples. The ESP-IDF tree's shared `i2c_bsp` component fixes this; the Arduino tree does not.

**Recommended minimum fix**, keeping the vendor structure:

~~~c
void Touch_Init(void)
{
    // ... i2c_param_config / i2c_driver_install (or use a shared bus) ...

    gpio_set_direction(GPIO_NUM_10, GPIO_MODE_OUTPUT);   // TP_RST
    gpio_set_level(GPIO_NUM_10, 0);
    vTaskDelay(pdMS_TO_TICKS(10));                       // Trst >= 0.1 ms; 10 ms is generous
    gpio_set_level(GPIO_NUM_10, 1);
    vTaskDelay(pdMS_TO_TICKS(120));                      // Tron >= 100 ms  [DOC] 7.1

    uint8_t id = 0, fw = 0;
    if (I2C_read_buff(0x15, 0xA7, &id, 1) != ESP_OK) { ESP_LOGE(TAG, "touch not responding"); return; }
    I2C_read_buff(0x15, 0xA9, &fw, 1);
    ESP_LOGI(TAG, "touch chip id=0x%02X fw=0x%02X", id, fw);   // expect 0xB6 for CST816D

    uint8_t z = 0x00;
    I2C_writr_buff(0x15, 0x00, &z, 1);                   // normal mode
}
~~~

### 6.5 Interrupt-driven versus polled

Both vendor drivers **poll**: LVGL's input-device read callback runs on the LVGL tick and issues an I²C transaction every time, whether or not anything was touched **[SRC]**. At the example's 2 ms LVGL tick that is a lot of bus traffic and a lot of wake-ups.

`INT` (GPIO9) is wired **[SCH]** and the chip asserts it "only when a valid touch is detected and needs to be reported to the host, this can improve efficiency and reduce the burden on the CPU" **[DOC]** §7.5. For a battery device this is worth doing: attach a GPIO ISR, set a flag or give a semaphore, and only read I²C when the flag is set.

**Which edge?** Configurable in the controller **[DOC]** §7.5, and *this* module's setting is unknown. Waveshare's code never configures `INT` at all, so there is no evidence either way. **[INF]** The safe approach is `GPIO_INTR_ANYEDGE` on first bring-up, log what you see, then narrow it.

---

## 7. Pitfalls, in rough order of likelihood

1. **Forgetting `& 0x0F` on the high coordinate bytes.** X or Y jumps by thousands. §3.1.
2. **Silent failure looking like "no touch".** The vendor driver discards I²C errors. §6.4. Always log the chip ID at boot.
3. **Reading too soon after reset or power-up.** `Tpor`/`Tron` are **100 ms**. §2.4.
4. **Rotating the display but not the touch, or vice versa.** §5.2.
5. **Two `i2c_driver_install()` calls on `I2C_NUM_0`.** Touch and haptic both want the bus. §5.1, §6.4.
6. **Putting the chip to sleep with no `RST` control.** One-way door. §3.3.
7. **Expecting multi-touch.** Coordinates are single-point. The "two-point" claim in the datasheet is about *gesture* recognition, not two independent coordinate pairs **[DOC]** §1; every driver treats it as single-touch **[SRC]**.
8. **Assuming `0x15` universally.** Hynitron explicitly warns the address can differ per project **[DOC]** §7.6(a). It is `0x15` here **[SRC]**, but scan the bus if you are bringing up a variant panel.
9. **Running the bus above 400 kHz.** §2.5.
10. **Assuming the CST816T all-`0xFF` bug does not apply.** SensorLib carries an explicit workaround: *"Some CST816T will return all 0xFF after turning off automatic sleep"* **[SRC]**. If you call `disableAutoSleep()` and touch stops working, this is why — check the chip ID.
11. **Assuming auto-sleep is off.** The chip enters standby after **2 s** without touch **[DOC]** §7.2. The first touch after idle may be swallowed as the wake event. If your UI feels like it ignores the first tap, write `0xFE ← 0x01`.
12. **Deploying below −20 °C.** §2.1.
13. **Trusting a "CST816 datasheet with a register map" found online.** §3.

---

## 8. Alternatives and compatibility

The panel is a bonded module, so replacing the touch controller is not a board-level option. This table is for software compatibility and for people designing something similar.

| Part | Relationship | Software compatible? |
|---|---|---|
| **CST816S** (`0xB4`) | The most common family member | ✅ Same register map. Most libraries target this name |
| **CST816T** (`0xB5`) | Same family | ✅ ⚠ Has the all-`0xFF`-after-`disableAutoSleep` quirk. §7.10 |
| **CST820** (`0xB7`) | Same family | ✅ Same map |
| **CST716** (`0x20`) | Older | ⚠ **No `0xFE` auto-sleep register.** Drivers need a special case |
| **CST226SE** | Hynitron multi-touch | ❌ Different driver (`TouchDrvCST226`), different map. Also reads `0x20` at `0xA7` — disambiguate with `0xA9` |
| **FocalTech FT6236 / FT6336** | The other ubiquitous small-panel controller | ❌ Different register map, usually address `0x38`. Genuine multi-touch |
| **Goodix GT911** | Larger panels | ❌ Different map, address `0x5D`/`0x14`, 5-point |
| **Chipsemi CHSC5816** | Also supported by SensorLib | ❌ Different map |

For ESP-IDF, `esp_lcd_touch` abstracts all of these behind one handle type, which is the main argument for §6.2 over a hand-rolled driver.

---

## 9. Open questions

| Question | Status |
|---|---|
| Does the fitted part actually report `0xB6`? | **Open — and trivial to answer.** One I²C read of `0xA7`. Please record the result here |
| Which `IRQ` edge does this module's firmware use? | **Open.** No vendor code configures `INT`. §6.5 |
| Which gestures are enabled in this module's controller firmware? | **Open.** No vendor code reads `0x01`. §4 |
| Is the panel's controller firmware version (`0xA9`) consistent across units? | **Open** |
| Top marking of the controller | **Unobtainable** — bonded inside the panel module |
| Are the `0xEC`/`0xED`/`0xFA`/`0xEE` community registers real on CST816D? | **Open.** **[COM]** only; not in any vendor driver shipped with this board |

---

## Manufacturer

**Hynitron** — see the [Hynitron documentation-sourcing guide](../../../vendors/hynitron/README.md) for this vendor's document portals, URL patterns, part-numbering conventions, distribution channels and known gotchas.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — touch controller of the bonded 360 × 360 round panel. I²C `0x15` on S3 GPIO11 (SDA) / GPIO12 (SCL), `INT` GPIO9, `RST` GPIO10; shares the bus with the DRV2605L at `0x5A`. See [Pinouts and buses § Bus inventory](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md).

## Related components

- [1.8-inch 360 × 360 LCD panel module](../../generic/lcd-panel-module/README.md) — the module this controller is bonded into
- [Sitronix ST77916](../../sitronix/st77916/README.md) — the display controller in the same module
- [Texas Instruments DRV2605L](../../texas-instruments/drv2605l/README.md) — the other device on this I²C bus
- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the I²C master

---

## Local artifacts and document revisions held

Only **one** revision of this datasheet is known to exist in circulation, and only one copy is
stored:

| Document | Revision | Language | Source | Local path | Bytes | SHA-256 |
|---|---|---|---|---|---:|---|
| Hynitron CST816D Datasheet | **V1.3** | English | Waveshare mirror, `files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf` | `artifacts/cst816d-datasheet-v1.3.pdf` | 1,098,205 | `a0b14a06ef5d82050d1e98092e2249060438e8dd0dc56f96821259e9175c3409` |

**Which applies to the fitted part?** V1.3 is the only revision available and it covers the
**CST816D** fitted on the knob board. Note the standing caveat in §3: this datasheet contains
**no register map**, so the register documentation in this file is reconstructed from driver
source, not from the vendor document — that limitation is a property of V1.3 itself, not of this
copy.

Unlike the Espressif and TI parts in this project, there is **no newer vendor revision to prefer**
here, and no evidence Waveshare is shipping a stale document for this part. Hynitron does not
publish datasheets openly; the Waveshare mirror is effectively the primary source.

### A byte-identical duplicate was removed

The Waveshare device record previously held a second copy at
`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/datasheets/CST816D_datasheet_En_V1.3.pdf`.
It was confirmed **byte-identical** to the file above — same SHA-256 `a0b14a06…`, same 1,098,205
bytes, `cmp` clean. The device-side copy was moved to `../hardware-doc-archive/` on 2026-08-24 and
the copy here is canonical. See the placeholder at
`devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/datasheets/README.md`.

Verified 2026-08-24 by `sha256sum`, `cmp`, and
`nix-shell -p poppler-utils --run 'pdftotext -f 1 -l 2 <file> -'` (page 2 reports `V1.3`).

### Reacquire

```bash
# Primary: the Waveshare shared wiki pool
curl -L -O https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf
# Secondary: the per-board mirror of the same file
curl -L -O https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/CST816D_datasheet_En_V1.3.pdf
# Tertiary: vendor site (datasheets sit behind the product/contact flow)
#   https://www.hynitron.com/
# Also: SensorLib bundles touch-controller datasheets
#   https://github.com/lewisxhe/SensorLib -> datasheet/
```

> Waveshare updates its `/wiki/common/` pool **in place**; a future download may not reproduce the
> hash above. Worth submitting to `https://web.archive.org/save/` — Hynitron documents are scarce.

---

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| **Hynitron CST816D Datasheet, English V1.3** — §7.1 power-on/reset timing, §7.2 working modes, §7.6 I²C, §9 electricals. **Contains no register map** | https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf | 2026-08-21 | `artifacts/cst816d-datasheet-v1.3.pdf` |
| Same document, Waveshare board mirror — **byte-identical duplicate, no longer stored separately** (see below) | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/CST816D_datasheet_En_V1.3.pdf | 2026-08-21 | `artifacts/cst816d-datasheet-v1.3.pdf` (single canonical copy) |
| Hynitron corporate site | https://www.hynitron.com/ | 2026-08-21 | – |
| Official demo archive — `08_LVGL_Test/cst816.cpp`, `lcd_touch_bsp.c`, `lcd_config.h`, and bundled **SensorLib 0.3.1** (`TouchDrvCST816.cpp/.h`, `REG/CSTxxxConstants.h`) | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` |
| SensorLib upstream (chip-ID table, reset sequence, CST816T workaround) | https://github.com/lewisxhe/SensorLib | 2026-08-21 | – |
| Espressif `esp_lcd_touch_cst816s` component | https://components.espressif.com/components/espressif/esp_lcd_touch_cst816s | 2026-08-21 | – |
| Espressif `esp_lcd_touch` abstraction | https://components.espressif.com/components/espressif/esp_lcd_touch | 2026-08-21 | – |
| LVGL input-device porting guide (`LV_EVENT_GESTURE`, pointer indev) | https://docs.lvgl.io/8.4/porting/indev.html | 2026-08-21 | – |
| Board schematic archive | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
