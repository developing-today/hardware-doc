# Keyboards — Tanmatsu and the Solder Party family

> Everything about the Tanmatsu keyboard, the Solder Party keyboards it is related to, and how to drive both.
> Snapshot **2026-08-24**. Primary evidence: Tanmatsu coprocessor firmware (MIT), the Tanmatsu production BOM (CERN-OHL-P), Solder Party product documentation, and the `i2c_puppet` firmware source.
> **No hardware was available** — nothing here has been verified with a meter or an oscilloscope.

---

## 0. Read this first: there are two different things called "the Solder Party keyboard"

This is the single most important distinction in this document, and it is easy to get wrong.

| | **KeebDeck Keyboard** | **BB Q10 / Q20 keyboards** |
|---|---|---|
| What it is | Custom **silicone keypad + metal dome sheet**, designed by Solder Party | Salvaged/sourced **BlackBerry** phone keyboards on a Solder Party carrier PCB |
| Keys | **69**, orthogonal, PC-style layout | 35 (Q10) / 39 + trackpad (Q20) |
| Interface | **None** — it is a bare component. You provide the PCB and the matrix scanning | **I2C peripheral** (and USB HID) via an on-board MCU |
| Controller | Whatever you design | ATSAMD20 (Q10 PMOD) or **RP2040** (BBQ20KBD) |
| Firmware | Yours | Solder Party [`i2c_puppet`](https://github.com/solderparty/i2c_puppet) |
| **Used in Tanmatsu** | ✅ **Yes** | ❌ No |

**The Tanmatsu uses the KeebDeck Keyboard, not a BlackBerry keyboard.** See [§1.1](#11-evidence-that-the-tanmatsu-keyboard-is-the-keebdeck-keyboard) for the evidence. Solder Party's BlackBerry-based products are a separate, older product line — excellent, widely used, and covered from [§3](#3-the-blackberry-keyboards-bb-q10--q20) onward, but not what is inside a Tanmatsu.

If you have "a stack of extra keyboards", **which kind you have determines everything**: a KeebDeck keypad is a passive silicone part needing a host PCB, whereas a BBQ10/BBQ20 board is a self-contained I2C device you can talk to immediately.

---

## 1. The Tanmatsu keyboard

### 1.1 Evidence that the Tanmatsu keyboard is the KeebDeck Keyboard

Nicolai Electronics says only that *"the keyboard has been developed by our awesome friends at Solder Party"* and never names the product. The identification is mine, from three independent matches:

| Property | Tanmatsu documentation / BOM | KeebDeck Keyboard documentation |
|---|---|---|
| Key count | "Full **69-key** alphanumeric keyboard with colored 6 function keys" | "compact (85×48 mm) **69-key** alphanumeric silicone keypad" |
| Actuation | "**Metal dome sheet** for tactile feeling" | "an adhesive **metal dome sheet**… required regardless" |
| Backlight LED | BOM `D4–D7, D14–D17` = **`LTW-010DCG-SR-G`** ×8 | "can also be backlit using **LTW-010DCG** LEDs (or similar)" |

The LED part number is the decisive one: KeebDeck's documentation names that exact LED because the dome sheet has an etched light-guide layer designed around it, and the Tanmatsu BOM fits eight of them.

> **Status: high confidence, not vendor-confirmed.** Nicolai Electronics has not publicly stated that the part is a KeebDeck. It is possible Tanmatsu uses a precursor or a Tanmatsu-specific variant of the same design — the key labels certainly differ (Tanmatsu has six coloured symbol keys). Treat "same family, near-certainly the same physical component" as the claim.

### 1.2 Physical construction

From the KeebDeck Keyboard documentation:

| Property | Value |
|---|---|
| Overall size | **85 × 48 mm** |
| Keys | 69, orthogonal layout based on standard PC keyboards |
| Standard key size | **5.2 × 6.6 mm** |
| Standard key pitch | **6.6 mm horizontal**, **7.9 mm vertical** |
| Top-row key size | **8.275 × 6.6 mm** |
| Top-row pitch | **9.675 mm horizontal** |
| Centre cutout | Sized for a **PAW-A350 optical finger navigation** module (the same class of sensor as the BBQ20 trackpad) |
| Front-cover clearance | ≥ **0.2 mm** padding if using a PCB as the front cover |

**Stack-up, bottom to top:**

```
   ┌─────────────────────────────┐  top cover (PCB, 3D print or milled)
   │  ███  silicone keypad  ███  │  ← white silicone, inked, black-coated, laser-etched labels
   ├─────────────────────────────┤
   │  ~~~ adhesive metal dome ~~~ │  ← tactile domes + etched light-guide layer
   ├─────────────────────────────┤
   │  PCB with KeebDeck footprint │  ← your board: pads + LEDs
   └─────────────────────────────┘
```

The dome sheet is **mandatory** whether or not you fit the backlight — it provides both the tactile action and the electrical contact. It has **two alignment holes in the corners**; Solder Party recommends mirroring those holes on your PCB to make application easier. Two further holes near the centre take reinforcement posts, needed if the front cover is large or flexible (which a 3D print usually is).

**How the backlight works** — this is a genuinely clever bit of design worth understanding before you place LEDs: the LEDs shine light *edgewise into the dome sheet*, which carries a diffusing layer with **etched dots at strategic points**. Light bounces off the dots up into the keypad. The keypad is white silicone, inked underneath the macro keys, then coated black on the front, then **laser-etched** to expose the silicone. So the etched glyphs light up. LED placement is therefore not free — it must match the positions in Solder Party's footprints.

### 1.3 The matrix — 9 rows × 8 columns

Established from `tanmatsu-coprocessor-firmware/src/application/keyboard.c` (MIT), the authoritative source:

```c
static const uint8_t keyboard_rows[]    = {PA8, PA9, PA10, PA4, PA3, PA1, PA6, PA5, PA2};
static const uint8_t keyboard_columns[] = {PB14, PB12, PB1, PA7, PB15, PB13, PB2, PB0};
```

**9 rows × 8 columns = 72 matrix positions**, which matches the **72 × `1N4148WS` diodes** in the BOM (`D8`–`D83`) exactly — one diode per key position, giving full **N-key rollover** with no ghosting. That is a deliberate quality decision for a device intended to be typed on properly.

| | CH32V203 pins |
|---|---|
| **Rows** (driven, push-pull output) | `PA8, PA9, PA10, PA4, PA3, PA1, PA6, PA5, PA2` |
| **Columns** (read, floating input) | `PB14, PB12, PB1, PA7, PB15, PB13, PB2, PB0` |

Note the row/column order is **not** monotonic in pin number — it follows PCB routing convention. Row index 0 is `PA8`, row index 3 is `PA4`, and so on. If you rewrite the firmware, preserve the order or your keymap shifts.

### 1.4 Scanning algorithm

Rows are configured `GPIO_CNF_OUT_PP` at 10 MHz and driven **LOW** at rest; columns are `GPIO_CNF_IN_FLOATING`. Scanning is **active-high**: a row is driven high, and any pressed key in that row pulls its column high through the key's diode.

The firmware has **two modes**, which is the interesting part:

**Idle mode** — entered after `input_scan_timeout = 20` steps with no activity and no key held:

```c
// Enable ALL rows simultaneously, then watch for any column going high
for (row...) funDigitalWrite(keyboard_rows[row], FUN_HIGH);
for (column...) if (funDigitalRead(keyboard_columns[column])) { ...wake... }
```

All rows are asserted at once, so a single read of the eight columns detects *any* keypress. No per-row cycling, so it costs almost nothing.

**Scan mode** — one row per call to `keyboard_step()`, reading all eight columns into a byte:

```c
uint8_t value = 0;
for (column...) value |= funDigitalRead(keyboard_columns[column]) << column;
registers[row] = value;
```

Each row's 8-bit state goes straight into I2C register `I2C_REG_KEYBOARD_0 + row`. The function returns `true` when a row's value changed, which the main loop uses to raise the host interrupt. Any key held resets the timeout, so the device stays in fast-scan mode while you are typing and drops to idle when you stop.

**Design lesson worth stealing:** the idle mode costs one GPIO write burst plus eight reads, versus nine row-cycles in scan mode. On a device whose coprocessor is always powered, that ratio matters.

### 1.4a Independent confirmation: the CH32V203 pinout

Badge.Team publish a **full 48-pin CH32V203 pinout with net names** at
[`badge.team/docs/badges/konsool/hardware/pinout/ics/ch32v203/`](https://badge.team/docs/badges/konsool/hardware/pinout/ics/ch32v203/)
(retrieved 2026-08-24). It corroborates the firmware pin lists exactly — and, better, it gives the
**KB_ROW / KB_COL net numbering**, which the firmware does not:

| Firmware row index | CH32V203 pin | Net name | | Firmware col index | CH32V203 pin | Net name |
|---:|---|---|---|---:|---|---|
| 0 | `PA8` (29) | `KB_ROW0` | | 0 | `PB14` (27) | `KB_COL0` |
| 1 | `PA9` (30) | `KB_ROW1` | | 1 | `PB12` (25) | `KB_COL1` |
| 2 | `PA10` (31) | `KB_ROW2` | | 2 | `PB1` (19) | `KB_COL2` |
| 3 | `PA4` (14) | `KB_ROW3` | | 3 | `PA7` (17) | `KB_COL3` |
| 4 | `PA3` (13) | `KB_ROW4` | | 4 | `PB15` (28) | `KB_COL4` |
| 5 | `PA1` (11) | `KB_ROW5` | | 5 | `PB13` (26) | `KB_COL5` |
| 6 | `PA6` (16) | `KB_ROW6` | | 6 | `PB2` (20) | `KB_COL6` |
| 7 | `PA5` (15) | `KB_ROW7` | | 7 | `PB0` (18) | `KB_COL7` |
| 8 | `PA2` (12) | `KB_ROW8` | | | | |

**Firmware index N corresponds exactly to `KB_ROW`N / `KB_COL`N.** The apparently scrambled pin
order in `keyboard.c` is therefore not arbitrary — it is the schematic net order, and the firmware
array is deliberately written to preserve it. If you rewrite the scanning code, keep this ordering
and your keymap stays valid.

Note `PB2` doubles as **`BOOT1`** on the CH32V203 — it is a strapping pin serving as `KB_COL6`.
A key held down in column 6 at coprocessor reset could in principle affect its boot mode.

### 1.4b Full CH32V203 pin assignment

Everything the coprocessor does, in one table. Source: badge.team, cross-checked against
`hardware.h` in the firmware.

| Pin | Port | Net | Dir | Purpose |
|---:|---|---|---|---|
| 1 | `VBAT` | `VBAT` | Power | **Regulated 2.5 V standby supply** — always on |
| 2 | `PC13` | `POWER_ON_PULSE` | Out | **Pulse to wake the badge** (drives the power latch) |
| 3, 4 | `PC14/15` | `XTAL` | In | 32.768 kHz RTC crystal |
| 5 | `PD0` | `AMP_EN` | Out | Enable speaker amplifier |
| 6 | `PD1` | `USB_ENABLE` | Out | Enable USB-A OTG port |
| 7 | `NRST` | `NRST` | In | Reset, 3V3 |
| 10 | `PA0` | `INT` | Out | **Interrupt to ESP32-P4** (P4 GPIO1) |
| 11–16 | `PA1..PA6` | `KB_ROW5,8,4,3,7,6` | Out | Keyboard rows |
| 17 | `PA7` | `KB_COL3` | In | Keyboard column |
| 18–20 | `PB0,PB1,PB2` | `KB_COL7,2,6` | In | Keyboard columns |
| 21 | `PB10` | `PM_SCL` | Out | **PMIC I2C clock** |
| 22 | `PB11` | `PM_SDA` | Bidir | **PMIC I2C data** |
| 25–28 | `PB12..PB15` | `KB_COL1,5,0,4` | In | Keyboard columns |
| 29–31 | `PA8..PA10` | `KB_ROW0,1,2` | Out | Keyboard rows |
| 32 | `PA11` | `LED_DATA` | Out | SK6805 serial data |
| 33 | `PA12` | `POWER_BTN` | In | Power button — **low when pressed** |
| 34 | `PA13` | `SWDIO` | Bidir | **Debug/programming** (from P4 GPIO22) |
| 37 | `PA14` | `SWCLK` | Out | **Debug clock** (from P4 GPIO23) |
| 38 | `PA15` | `SD_DET` | In | SD card detect |
| 39 | `PB3` | `KEYBOARD_BL` | Out | **Keyboard backlight PWM** |
| 40 | `PB4` | `DISPLAY_BL` | Out | **Display backlight PWM** |
| 41 | `PB5` | `HP_DET` | In | Headphone detect |
| 42 | `PB6` | `SCL` | In | **Host I2C clock** (shared bus) |
| 43 | `PB7` | `SDA` | Bidir | **Host I2C data** (shared bus) |
| 44 | `BOOT0` | `DCAM_IO0` | Out | **Camera module power enable** |
| 45 | `PB8` | `RADIO_ENABLE / CAM_IO0` | Out | **ESP32-C6 enable + camera IO0** (shared) |
| 46 | `PB9` | `PM_INT` | In | **PMIC interrupt** — not present in `hardware.h` |

Two facts here are not in the Tanmatsu documentation at all:

- **`PB9` = `PM_INT`**, a PMIC interrupt line. The firmware's `hardware.h` does not define it, so the
  shipped firmware appears to **poll** the BQ25895 rather than use its interrupt.
- **`BOOT0` is reused as `DCAM_IO0`**, a camera power enable. Using the CH32V203's boot strap as a
  functional output is unusual and means camera power state is entangled with coprocessor boot.

### 1.4c The keyboard is confirmed as Solder Party's

Badge.Team's Konsool keyboard specification page reads, in full:

> *"QWERTY dome keyboard by Arturo"*

**"Arturo"** is *arturo182*, who runs Solder Party. This independently corroborates the
identification in [§1.1](#11-evidence-that-the-tanmatsu-keyboard-is-the-keebdeck-keyboard) — a
*dome* keyboard by *Arturo* is the KeebDeck. It is still not an explicit product name, so the
finding stays "high confidence, not vendor-confirmed", but two independent vendors now point at
Solder Party.

### 1.5 Complete key map

The row/bit → key mapping, from `esp32-component-tanmatsu-coprocessor/tanmatsu_coprocessor.h`. **Bit 0 is the first column** (`PB14`).

| Row | Reg | bit 0 | bit 1 | bit 2 | bit 3 | bit 4 | bit 5 | bit 6 | bit 7 |
|---:|---|---|---|---|---|---|---|---|---|
| 0 | `0x02` | `esc` | `f1` | `f2` | `f3` | `` ` `` | `1` | `2` | `3` |
| 1 | `0x03` | `tab` | `q` | `w` | `e` | **`fn`** | `a` | `s` | `d` |
| 2 | `0x04` | `shift_l` | `z` | `x` | `c` | `ctrl` | `meta` | `alt_l` | `\` |
| 3 | `0x05` | `4` | `5` | `6` | `7` | `r` | `t` | `y` | `u` |
| 4 | `0x06` | `f` | `g` | `h` | `j` | `v` | `b` | `n` | `m` |
| 5 | `0x07` | `f4` | `f5` | `f6` | `backspace` | `9` | `0` | `-` | `=` |
| 6 | `0x08` | `o` | `p` | `[` | `]` | `l` | `;` | `'` | `return` |
| 7 | `0x09` | `.` | `/` | `up` | `shift_r` | `alt_r` | `left` | `down` | `right` |
| 8 | `0x0A` | `8` | `i` | `k` | `,` | `space_l` | `space_m` | `space_r` | `volume_up` |

Things worth noticing:

- **The space bar is three separate switches** (`space_l`, `space_m`, `space_r`) — a wide key needs multiple domes to actuate reliably wherever you hit it. Your driver should OR them together.
- **`volume_up` exists but there is no `volume_down`** in the matrix. **This is now resolved:** `volume_down` is *not a matrix key at all* — it is a **discrete GPIO button on ESP32-P4 GPIO35**, per the BSP (`#define BSP_GPIO_BTN_VOLUME_DOWN 35`). Badge.Team's P4 pinout notes GPIO35 is *"Connected up to volume down button"* and is also a boot strap (`1` during reset release = SPI boot, `0` = DEBUG). So volume-down is read by the application processor directly, not through the coprocessor.
- **`meta`** (the Windows/Super key) is present, at row 2 bit 5.
- **`fn`** sits oddly at row 1 bit 4, between `e` and `a`, which reflects physical position rather than logical grouping.
- The layout is **not** contiguous — `8` is on row 8 while `9` and `0` are on row 5. Do not attempt to infer the map; use the table.

### 1.6 The six coloured function keys

| Symbol | Colour | BSP event | Matrix position |
|---|---|---|---|
| ✕ | red | `BSP_INPUT_NAVIGATION_KEY_F1` | row 0, bit 1 |
| △ | orange | `F2` | row 0, bit 2 |
| ☐ | yellow | `F3` | row 0, bit 3 |
| ◯ | green | `F4` | row 5, bit 0 |
| ☁ | blue | `F5` | row 5, bit 1 |
| ◇ | magenta | `F6` | row 5, bit 2 |

Their meaning is defined by the running application. The launcher uses **the magenta ◇ key (second from the top right)** to toggle USB mode between debug and BadgeLink — see [`development.md` §5](development.md#5-badgelink--managing-the-device-over-usb).

### 1.7 AltGr layer

The keyboard is based on **US-International with AltGr**. Holding AltGr gives accented letters and symbols directly:

| Key | AltGr | +Shift | | Key | AltGr | +Shift |
|---|---|---|---|---|---|---|
| Q | ä | Ä | | A | á | Á |
| W | å | Å | | S | ß | § |
| E | é | É | | D | ð | Ð |
| R | ® | ™ | | F | ë | Ë |
| T | þ | Þ | | J | ï | Ï |
| Y | ü | Ü | | K | œ | Œ |
| U | ú | Ú | | L | ø | |
| I | í | Í | | Z | æ | Æ |
| O | ó | Ó | | X | · | |
| P | ö | Ö | | C | © | ¢ |
| | | | | N | ñ | Ñ |
| | | | | M | µ | ± |

| Key | AltGr | | Key | AltGr |
|---|---|---|---|---|
| 1 | ¡ | | 8 | ¾ |
| 2 | ² | | 9 | ‘ |
| 3 | ³ | | 0 | ’ |
| 4 | ¤ | | - | ¥ |
| 5 | € | | [ | « |
| 6 | ¼ | | ] | » |
| 7 | ½ | | / | ¿ |
| | | | \ | ¬ |

`= ; ' , .` and the shifted number row carry **combining diacritical marks**, which combine with the *next* character rather than printing standalone.

⚠ **Whether a character appears depends on your application's font coverage.** The BSP will happily hand you `ð` or `Œ`; a font without those glyphs renders nothing. This is an application bug that looks like a keyboard bug.

The authoritative keymap table is in [`badge_bsp_input.c`](https://github.com/badgeteam/esp32-component-badge-bsp/blob/main/targets/tanmatsu/badge_bsp_input.c#L352), around line 352.

### 1.8 Reading the keyboard from the ESP32-P4

The coprocessor is an I2C peripheral at **0x5F** on the internal bus (GPIO9 SDA / GPIO10 SCL). Registers, from `i2c_registers.h`:

| Reg | Name | Notes |
|---|---|---|
| `0x00`–`0x01` | `FW_VERSION_0/1` | LSB, MSB |
| **`0x02`–`0x0A`** | **`KEYBOARD_0`…`KEYBOARD_8`** | **one byte per matrix row** |
| `0x0B` | `DISPLAY_BACKLIGHT` | PWM duty |
| `0x0C` | `KEYBOARD_BACKLIGHT` | PWM duty |
| `0x0D` | `INTERRUPT` | |
| `0x0E` | `LED_BRIGHTNESS` | |
| `0x0F` | `INPUT` | bit 0 = SD card detect, bit 1 = headphone detect |
| `0x10` | `OUTPUT` | |
| `0x11` | `RADIO_CONTROL` | ESP32-C6 power/boot mode |
| `0x12`–`0x15` | `RTC_VALUE_0..3` | 32-bit RTC |
| `0x16`–`0x69` | `BACKUP_0`…`BACKUP_83` | **84 bytes of battery-backed scratch RAM** |
| … | PMIC block | see [§1.10](#110-what-else-the-coprocessor-exposes) |

**The pattern is simple:** read 9 bytes from `0x02`, and you have the entire keyboard state. A change raises the interrupt pin (`PA0` on the coprocessor). There is **no FIFO and no keycode translation** in the coprocessor — it reports raw matrix state, and the ESP32-P4 side (the BSP) does debouncing semantics, modifier resolution and UTF-8 mapping.

This is the opposite of the Solder Party `i2c_puppet` design ([§3](#3-the-blackberry-keyboards-bb-q10--q20)), which does keycode translation and FIFO buffering *on the keyboard controller*. Neither is wrong; Tanmatsu's approach keeps the coprocessor tiny and puts policy where it is easy to update.

Use the driver component rather than raw I2C: [`esp32-component-tanmatsu-coprocessor`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-coprocessor), which gives you a `tanmatsu_coprocessor_keys_t` bitfield struct and a callback:

```c
typedef void (*tanmatsu_coprocessor_keyboard_cb)(
    tanmatsu_coprocessor_handle_t, tanmatsu_coprocessor_keys_t* prev,
    tanmatsu_coprocessor_keys_t* curr);
```

### 1.9 Backlight

Register **`0x0C`** (`I2C_REG_KEYBOARD_BACKLIGHT`) sets the PWM duty. The coprocessor drives pin **`PB3`** (`pin_keyboard_backlight`) into an **AP3032KTR** LED driver (`U16`/`U18` — one for the keyboard, one for the display). The display backlight is the sibling register `0x0B` on coprocessor pin `PB4`.

Eight white `LTW-010DCG-SR-G` LEDs edge-light the dome sheet.

### 1.10 What else the coprocessor exposes

Worth knowing because it is all on the same 9-byte-away register file:

- **PMIC telemetry in engineering units** — `PMIC_ADC_VBAT` (mV), `VSYS` (mV), `VBUS` (mV), `ICHGR` (**mA**), `TS` (% of REGN). The coprocessor does the BQ25895 conversion for you, so battery voltage is a 2-byte read, not an I2C dance with the PMIC.
- **`PMIC_CHARGING_CONTROL` / `CHARGING_STATUS` / `OTG_CONTROL` / `POWER_CONTROL`**
- **`ALARM_0..3`** — the RTC alarm that can power the whole device on via the latch circuit
- **`LED_DATA_LED0_G/R/B` … `LED5_*`** — the six SK6805s, **note the G,R,B byte order**, plus `LED_MODE`
- **`BACKUP_0..83`** — 84 bytes preserved across power-off, useful for state you want to survive a shutdown

### 1.11 Verified coprocessor behaviour (from firmware source)

Read from [`artifacts/source-snapshots/coprocessor-firmware/main.c`](artifacts/source-snapshots/coprocessor-firmware/main.c)
(MIT), not from documentation:

| Behaviour | Detail |
|---|---|
| Input scan interval | **50 ms** (`input_scan_interval`) |
| **Power-off hold time** | **> 500 ms** — `power_button_counter > 500 / input_scan_interval`, i.e. 10 scans |
| Power button polarity | **Active low** (`!funDigitalRead(pin_power_in)`) |
| Power button feedback | The LED beside the power button turns **red** (`0xFF0000`) while held, and off on release |
| Shutdown sequence | stop timers 2 and 3 → blank all six LEDs (both banks) → `Delay_Ms(10)` → `pmic_power_off()` |
| Anti-repeat | A `power_button_latch` flag requires the button to be **released once** before another power-off can trigger — so holding through boot does not immediately shut down again |
| RTC register update | every **1 ms** |

Two things worth taking from this:

- **One of the six SK6805 LEDs is physically next to the power button** and is used as a power-state
  indicator by the firmware. The vendor documentation describes the LEDs only as six generic
  addressable LEDs.
- **`PM_INT` (coprocessor `PB9`) appears nowhere in the firmware source** — confirmed by grep across
  every `.c`/`.h` in the application. badge.team's pin table documents the net, but the shipped
  firmware **polls** the BQ25895 instead. The interrupt line is available to anyone writing custom
  coprocessor firmware.

---

## 2. Building your own board around a KeebDeck keypad

If your spare keyboards are **KeebDeck keypads**, they are passive and you need to design the host PCB.

**What you need:**

1. **The KeebDeck footprint** on your PCB — pads in the exact geometry. Solder Party publishes footprints for popular EDA tools: [`solderparty/keebdeck_keyboard_hw`](https://github.com/solderparty/keebdeck_keyboard_hw) (47★).
2. **The adhesive metal dome sheet** — mandatory, supplied with the keypad.
3. **A top cover** to retain the keypad — PCB, 3D print or milled. ≥0.2 mm padding if it is a PCB.
4. **Alignment holes** in the corners, matching the dome sheet's.
5. Optional: **`LTW-010DCG` LEDs** in the specified positions for backlight.
6. Optional: **PAW-A350** optical finger navigation in the centre-top cutout.

**Reference design:** [`solderparty/keebdeck_basic_hw`](https://github.com/solderparty/keebdeck_basic_hw) (40★) — Solder Party's own evaluation board, open source. Their advice: *"The recommended way to drive the keyboard is by implementing it as a column and row matrix, but the final choice is up to you."*

**The Tanmatsu itself is the other reference design**, and arguably the better one for a complete product: [`keyboard_matrix.kicad_sch`](artifacts/schematics/kicad/keyboard_matrix.kicad_sch) in the hardware repo shows the full 9×8 matrix with per-key diodes and the backlight LED placement, under CERN-OHL-P.

**Customisation:** for orders of **500+**, Solder Party will customise the laser-etched key labels. This is presumably how Tanmatsu got its six coloured symbol keys.

---

## 2a. VERIFIED: the KeebDeck footprint, measured from the source files

Solder Party publish the footprint under **CERN-OHL v1.2**. The library is retained locally at
[`artifacts/keebdeck-keyboard/`](artifacts/keebdeck-keyboard/) (KiCad `.pretty` + symbol +
`dimensions.pdf`), from [`solderparty/keebdeck_keyboard_hw`](https://github.com/solderparty/keebdeck_keyboard_hw)
@ `f1c074c` (2025-11-11). Figures below were extracted with
[`tools/parse_keebdeck_footprint.py`](tools/parse_keebdeck_footprint.py), not retyped.

### ⚠ Only the 6×13 variant is finished

The repository ships four sizes, and its README is explicit:

> *"Only the **6x13** KeebDeck Keyboard files are final. The 3D models and footprints for all other
> sizes should be considered **work in progress**."*

| Footprint | Grid | Status |
|---|---|---|
| **`Keyboard_6R13C`** | **6 rows × 13 columns** | ✅ **final** — this is the 69-key keypad, and the one on Tanmatsu |
| `Keyboard_5R11C` | 5 × 11 | ⚠ WIP |
| `Keyboard_4R12C` | 4 × 12 | ⚠ WIP |
| `Keyboard_4R11C` | 4 × 11 | ⚠ WIP |

If you have spare keypads, they are almost certainly the 6×13. **Design against `Keyboard_6R13C` only.**

### Physical vs electrical matrix — do not confuse them

This is the subtlety that will cost you a board spin:

| | Grid | Where it comes from |
|---|---|---|
| **Physical key grid** | **6 rows × 13 columns** | The KeebDeck footprint — nets `R0`–`R5`, `C0`–`C12` |
| **Electrical scan matrix (Tanmatsu)** | **9 rows × 8 columns** | Tanmatsu's own wiring into the CH32V203 |

The keypad's row/column nets are **not** the scan matrix. Tanmatsu re-groups the 6×13 physical grid
into a 9×8 electrical matrix on its mainboard. Your host PCB can choose its own grouping — you are
free to wire the 19 footprint nets however your MCU's pin budget prefers.

### Pad geometry (from `Keyboard_6R13C.kicad_mod`)

```
pads total       : 213
column nets      : 13  (C0..C12)
row nets         :  6  (R0..R5)
pad extent       : X 79.20 mm,  Y 42.59 mm
silk outline     : 86.75 x 54.41 mm

  71 x  smd        circle   2.5 x 2.5 mm     <- outer dome contact ring
  71 x  smd        custom   0.9 x 0.9 mm     <- inner dome contact
  69 x  thru_hole  circle   1.0 x 1.0 mm
   2 x  thru_hole  circle   0.85 x 0.85 mm   <- corner alignment holes
```

**Why 71 contacts for a "69-key" keypad:** the space bar has **three** dome contacts so it actuates
wherever you press it. 68 single-contact keys + 3 space contacts = **71**. This independently
confirms the `space_l` / `space_m` / `space_r` triple seen in the Tanmatsu keymap
([§1.5](#15-complete-key-map)) — and explains why Tanmatsu fits **72** diodes for 69 keys.

The **two 0.85 mm through-holes** are the corner alignment holes Solder Party recommend mirroring on
your PCB so the adhesive dome sheet can be positioned accurately.

### Pitch, derived from the pad coordinates

| Axis | Observed | Meaning |
|---|---|---|
| X | **6.6 mm** dominant spacing | Standard key pitch — matches the published 6.6 mm |
| Y | alternating **2.5 mm** and **5.4 mm** | The two pads of each dome pair are offset; **2.5 + 5.4 = 7.9 mm**, the published vertical pitch |

So the vertical figure in the datasheet is the *key* pitch, not the *pad* pitch — the pads alternate
within each row. Laying out on a uniform 7.9 mm grid will not match the footprint.

### Dimensional drawing (`dimensions.pdf`, 4 pages)

| Page | Content | Key figures (mm) |
|---|---|---|
| 1 | Keypad front view | overall **85.80**, **48.60**; 38.60, 8.60, 8.85, 19.80, 23.70, 24.90; **5 × Ø2.00** holes |
| 2 | Keypad **side** view | **2.50** total height, 0.70, 0.80, 4.00; length 46.70 |
| 3 | Front-view fragment | key **5.2**, top-row key **8.275**; pitches **6.6** and **7.9**; top-row pitch **9.675**; 1.3, 1.4, 1.9 |
| 4 | **Dome sheet** front view | **86.75** wide, **52.3**; 14.6, 29.2, 14, 28, 15.375, 14.175; **Ø1.3** and **Ø1.2** holes; R1.5 corners |

**The keypad is only 2.50 mm thick** (page 2) — useful when budgeting enclosure depth. Note the dome
sheet (86.75 mm) is slightly **wider** than the keypad (85.80 mm).

### Library formats available

| Format | Path in repo | Note |
|---|---|---|
| **KiCad** | [`artifacts/keebdeck-keyboard/KeebDeck_Keyboard.pretty/`](artifacts/keebdeck-keyboard/KeebDeck_Keyboard.pretty/) + `.kicad_sym` | Retained locally |
| Eagle / Fusion | archive only | `Eagle/KeebDeck_Eagle.lbr`, `KeebDeck_Fusion.lbr` (2.0 MB) |
| Altium | archive only | `Altium/KeebDeck.{SchLib,PcbLib}` (740 KB) |
| EasyEDA | archive only | `EasyEDA/KeebDeck_Keyboard.elibz` (32 KB) |
| 3D STEP | archive only | `KeebDeck_Keyboard.3dshapes/` (14 MB) — keypad, dome sheet **and `ADBM-A350.step`**, the optical finger-navigation module |

Non-KiCad libraries and the 14 MB of STEP models are in
`../hardware-doc-archive/scratch/tanmatsu/sources/keebdeck_keyboard_hw/`; re-fetch with
[`tools/fetch_sources.sh`](tools/fetch_sources.sh).

### Checklist for building a board around a spare keypad

1. Use **`Keyboard_6R13C`** — the only finished footprint.
2. Mirror the **two 0.85 mm corner alignment holes** for dome-sheet placement.
3. Consider the **two extra centre holes** for reinforcement if your cover is 3D-printed (it will flex).
4. Budget **2.50 mm** keypad height plus dome sheet, and a cover with **≥0.2 mm** padding if it is a PCB.
5. Decide your own row/column grouping — you have 6 + 13 = 19 nets and no obligation to copy
   Tanmatsu's 9×8.
6. Add **one diode per key position** if you want N-key rollover (Tanmatsu uses 72 × `1N4148WS`).
7. If backlighting, place **`LTW-010DCG`** LEDs at the positions in the footprint — the dome sheet's
   etched light-guide dots are designed around them.
8. Reference design: [`solderparty/keebdeck_basic_hw`](https://github.com/solderparty/keebdeck_basic_hw)
   (also retained in the archive), or Tanmatsu's own
   [`keyboard_matrix.kicad_sch`](artifacts/schematics/kicad/keyboard_matrix.kicad_sch).

---

## 3. The BlackBerry keyboards (BB Q10 / Q20)

Solder Party's older and more famous line. If your spare keyboards are these, they are **self-contained I2C devices** and much easier to use.

### 3.1 The product family

| Product | Keyboard | Controller | Interfaces | Repo |
|---|---|---|---|---|
| **Keyboard PMOD** | BB **Q10** | ATSAMD20 | I2C, PMOD | [`bbq10kbd_i2c_sw`](https://github.com/solderparty/bbq10kbd_i2c_sw) |
| **BBQ20KBD** | BB **Q20** + trackpad | **RP2040** | I2C, **USB HID**, PMOD, Qwiic | [`bbq20kbd_hw`](https://github.com/solderparty/bbq20kbd_hw) (219★) |
| **Keyboard FeatherWing Rev 1 / Rev 2** | BB Q10 | — | Adafruit Feather form factor | — |
| **PMOD to Qwiic Adapter** | — | — | adapter | [`pmod_to_qwiic_adapter`](https://github.com/solderparty/pmod_to_qwiic_adapter) |

**BBQ20KBD** is the current one: a Q20 keyboard in an injection-moulded clear plastic case, with four extra buttons over the Q10 and an **optical trackpad**. Plugged into a PC, phone or SBC it enumerates as a **USB HID keyboard + mouse combo** with no driver. Over I2C it is a keyboard peripheral. It is **not 5 V tolerant.**

The **Keyboard FeatherWing Rev 2** is a whole handheld front-end: BB Q10 keyboard + 2.6" 320×240 16-bit LCD with resistive touch, 5-way button, 4 tactile buttons, a NeoPixel, ambient light sensor, microSD, Qwiic, on/off switch. It contains **no MCU** — you supply an Adafruit Feather.

### 3.2 `i2c_puppet` — the firmware

[`solderparty/i2c_puppet`](https://github.com/solderparty/i2c_puppet) (117★) is the RP2040 firmware, a port of the older ATSAMD20 `bbq10kbd_i2c_sw`, **backwards compatible** with it. So the same host libraries drive both generations — Solder Party say so explicitly on the BBQ20KBD page.

Build:

```bash
git clone https://github.com/solderparty/i2c_puppet
cd i2c_puppet
git submodule update --init
cd 3rdparty/pico-sdk && git submodule update --init && cd ../..
mkdir build && cd build
cmake -DPICO_BOARD=bbq20kbd_breakout -DCMAKE_BUILD_TYPE=Debug ..
make
```

> Status: **`reported-working`** — quoted from the project README. Not executed here. Note the deliberate **non-recursive** submodule init: a recursive init pulls in all of TinyUSB's own submodules and is not recommended.

### 3.3 I2C protocol

**Default address `0x1F`** (configurable in `app/config/conf_app.h`, and at runtime via `REG_ADR`).

**Writing:** apply the write mask **`0x80`** to the register ID. Backlight `0x05` becomes `0x85`.

| Reg | Name | Size | Purpose |
|---|---|---|---|
| `0x01` | `REG_VER` | 1 | Firmware version — high nibble major, low nibble minor |
| `0x02` | `REG_CFG` | 1 | Configuration bitmap (below) |
| `0x03` | `REG_INT` | 1 | Interrupt status — **must be manually reset to `0x00`** after reading |
| `0x04` | `REG_KEY` | 1 | bits 0–4 FIFO count, bit 5 caps lock, bit 6 num lock |
| `0x05` | `REG_BKL` | 1 | **Keyboard backlight** PWM, `0x00`–`0xFF`. Default `0xFF` |
| `0x06` | `REG_DEB` | 1 | Debounce — *not implemented* |
| `0x07` | `REG_FRQ` | 1 | Poll frequency — *not implemented* |
| `0x08` | `REG_RST` | — | Read **or** write triggers a software reset |
| **`0x09`** | **`REG_FIF`** | **2** | **FIFO read: key state byte + key code byte** |
| `0x0A` | `REG_BK2` | 1 | **Secondary backlight** (e.g. a screen). Default `0xFF` |
| `0x0B` | `REG_DIR` | 1 | GPIO expander direction. `1` = input. Default `0xFF` |
| `0x0C` | `REG_PUE` | 1 | GPIO pull enable. Default `0x00` |
| `0x0D` | `REG_PUD` | 1 | GPIO pull direction. `1` = pull-up. Default `0xFF` |
| `0x0E` | `REG_GIO` | 1 | GPIO values (read gives inputs *and* outputs) |
| `0x0F` | `REG_GIC` | 1 | GPIO interrupt config. Default `0x00` |
| `0x10` | `REG_GIN` | 1 | GPIO interrupt status — **must be manually reset** |
| `0x11` | `REG_HLD` | 1 | Hold threshold, units of **10 ms**. Default 30 = 300 ms |
| `0x12` | `REG_ADR` | 1 | I2C address. Takes effect **immediately**, not persisted across reset |
| `0x13` | `REG_IND` | 1 | Interrupt pin LOW duration in ms. Default 1 |
| `0x14` | `REG_CF2` | 1 | Configuration bitmap 2 (below) |
| `0x15` | `REG_TOX` | 1 | **Trackpad X delta**, signed −128…127, **cleared on read** |
| `0x16` | `REG_TOY` | 1 | **Trackpad Y delta**, signed −128…127, **cleared on read** |

**`REG_CFG` (0x02):**

| Bit | Name | Meaning |
|---|---|---|
| 7 | `CFG_USE_MODS` | Alt/Sym/Shift modify reported keys |
| 6 | `CFG_REPORT_MODS` | Report the modifier keys themselves |
| 5 | `CFG_PANIC_INT` | *not implemented* |
| 4 | `CFG_KEY_INT` | Interrupt on key press |
| 3 | `CFG_NUMLOCK_INT` | Interrupt on Num Lock |
| 2 | `CFG_CAPSLOCK_INT` | Interrupt on Caps Lock |
| 1 | `CFG_OVERFLOW_INT` | Interrupt on FIFO overflow |
| 0 | `CFG_OVERFLOW_ON` | On overflow, overwrite oldest (`1`) or drop new (`0`) |

Default: `CFG_OVERFLOW_INT | CFG_KEY_INT | CFG_USE_MODS`

**`REG_CF2` (0x14):** bit 2 `CF2_USB_MOUSE_ON`, bit 1 `CF2_USB_KEYB_ON`, bit 0 `CF2_TOUCH_INT`. Default all three set — so **USB HID is on out of the box**.

**`REG_INT` (0x03):** bit 6 `INT_TOUCH`, bit 5 `INT_GPIO`, bit 4 `INT_PANIC` (n/i), bit 3 `INT_KEY`, bit 2 `INT_NUMLOCK`, bit 1 `INT_CAPSLOCK`, bit 0 `INT_OVERFLOW`.

**FIFO key states** (`REG_FIF` first byte): `1` = pressed, `2` = pressed-and-held, `3` = released. FIFO depth is **31** entries (`KEY_FIFO_SIZE`).

### 3.4 Special key codes

Beyond ASCII, from `app/keyboard.h`:

| Code | Key |
|---|---|
| `0x01`–`0x04` | Joystick up / down / left / right |
| `0x05` | Joystick centre |
| `0x06` | Button left 1 |
| `0x07` | Button right 1 |
| `0x11` | Button left 2 |
| `0x12` | Button right 2 |
| `0x1A` | Alt modifier |
| `0x1B` | Left Shift |
| `0x1C` | Right Shift |
| `0x1D` | Sym modifier |

On the BBQ20, **trackpad motion is also synthesised into joystick key codes** (`touchpad.c`), so a device that only understands the FIFO still gets directional input.

### 3.5 BBQ20KBD matrix and pin map

From `boards/bbq20kbd_breakout.h` — **7 rows × 6 columns**, RP2040 GPIO numbers:

| | RP2040 pins |
|---|---|
| Rows | `1, 2, 3, 4, 5, 6, 7` |
| Columns | `8, 9, 14, 13, 12, 11` |
| Extra button | `10` → `KEY_BTN_RIGHT2` |
| GPIO expander | `15, 17, 19, 21, 26` |
| Backlight | `25` |
| Host I2C | SDA `18`, SCL `23` |
| "Puppet" I2C | SDA `28`, SCL `29` |
| Trackpad | reset `16`, motion `22`, shutdown `24` |
| Interrupt out | `0` |
| USB | VID `0x1209`, PID `0xB182`, product `"BBQ20KBD"` |

The character matrix (`kbd_entries` in `app/keyboard.c`), unshifted / Sym:

| Row | col 0 | col 1 | col 2 | col 3 | col 4 | col 5 |
|---:|---|---|---|---|---|---|
| 0 | JOY_CENTER | `W` `1` | `G` `/` | `S` `4` | `L` `"` | `H` `:` |
| 1 | — | `Q` `#` | `R` `3` | `E` `2` | `O` `+` | `U` `_` |
| 2 | BTN_LEFT1 | `~` `0` | `F` `6` | *Shift L* | `K` `'` | `J` `;` |
| 3 | — | `space` `tab` | `C` `9` | `Z` `7` | `M` `.` | `N` `,` |
| 4 | BTN_LEFT2 | *Sym* | `T` `(` | `D` `5` | `I` `-` | `Y` `)` |
| 5 | BTN_RIGHT1 | *Alt* | `V` `?` | `X` `8` | `$` `` ` `` | `B` `!` |
| 6 | — | `A` `*` | *Shift R* | `P` `@` | `backspace` | `enter` `\|` |

### 3.6 Host libraries

Solder Party links five independent implementations — useful, because it means you rarely need to write the I2C code yourself:

| Language | Project |
|---|---|
| Arduino | [`solderparty/arduino_bbq10kbd`](https://github.com/solderparty/arduino_bbq10kbd) |
| CircuitPython | [`arturo182_CircuitPython_BBQ10Keyboard`](https://github.com/solderparty/arturo182_CircuitPython_BBQ10Keyboard) |
| Rust (embedded-hal) | [`bbq10kbd` crate](https://crates.io/crates/bbq10kbd) |
| Linux (feature-rich userspace driver) | [`wallComputer/bbqX0kbd_driver`](https://github.com/wallComputer/bbqX0kbd_driver/) |
| Linux kernel module | [`billylindeman/bbq10kbd-kernel-driver`](https://github.com/billylindeman/bbq10kbd-kernel-driver) |

**All of these work with both Q10 and Q20 boards** because `i2c_puppet` kept the register map backwards compatible.

### 3.7 USB configuration without I2C

`i2c_puppet` exposes the **same register file over a USB Vendor Class interface**, so you can configure a BBQ20KBD from a PC with no I2C at all:

```bash
sudo cp etc/99-i2c_puppet.rules /lib/udev/rules.d/
sudo udevadm control --reload
sudo udevadm trigger
```

Then use `etc/i2c_puppet.py` — import it, construct an `I2C_Puppet` object, and the API mirrors the CircuitPython I2C class.

---

## 4. Solder Party

**Solder Party AB** — Malmö, **Sweden**; ships from the EU. Founded/run by **arturo182**. Sells through **[Lectronz](https://lectronz.com/)**.

> *"All our products are Open Source, both hardware, and software; we also welcome contributions and comments."*

That is not a slogan — 31 public repositories, and the hardware repos contain KiCad sources, symbols and footprints, not just PDFs.

### 4.1 Product lines

**Keyboards**
- KeebDeck Keyboard — 69-key silicone keypad + dome sheet *(this is what Tanmatsu uses)*
- KeebDeck Basic — evaluation/reference board for the above
- BBQ20KBD — BB Q20 keyboard + trackpad, USB/PMOD/Qwiic, cased
- Keyboard PMOD — BB Q10 in PMOD form
- Keyboard FeatherWing Rev 1 / Rev 2 — Q10 + 2.6" LCD handheld front-end
- PMOD to Qwiic Adapter

**RP2xxx "Stamp" modules** — castellated SoM modules, the other thing Solder Party is known for
- RP2040 Stamp, RP2350 Stamp, **RP2350 Stamp XL**
- Carriers: RP2040 Stamp Carrier, RP2xxx Stamp Carrier Basic, Carrier XL, Round Carrier
- [`rp2xxx_stamp_footprints`](https://github.com/solderparty/rp2xxx_stamp_footprints) (87★)
- [`esp32p4_stamp_xl_usb_uart_bridge`](https://github.com/solderparty/esp32p4_stamp_xl_usb_uart_bridge) — note: an **ESP32-P4** Stamp XL exists, same SoC as Tanmatsu

**FlexyPin** (118★) — spring-pin sockets for mounting castellated modules without soldering, plus [`flexypin_adapters_hw`](https://github.com/solderparty/flexypin_adapters_hw) (55★)

**USB Type-C breakouts** — USB 2.0 / 3.0 plug breakouts, SMT pack, CP2102 USB-UART, LiPo charger plug

**Others** — Serpente R1/R2 (tiny SAMD21 boards), OLED PMOD, LiPo Disconnector

**Flux Projects** — open reference designs: Handheld Console, MacroPad, Photo Light

### 4.2 Why this matters for Tanmatsu

Solder Party is not just a supplier here — Tanmatsu's design vocabulary is visibly shared with theirs: PMOD and Qwiic connectors, open KiCad sources, castellated-module thinking. The **CATT** port's simultaneous PMOD+SAO+JTAG compatibility is exactly the kind of connector pragmatism Solder Party's catalogue is built on.

### 4.3 Contact and community

- Docs: <https://www.solder.party/docs/>
- Shop: [Lectronz](https://lectronz.com/)
- GitHub: <https://github.com/solderparty>
- Bluesky: <https://bsky.app/profile/solder.party>
- Discord: linked from <https://www.solder.party/>

---

## 5. Gaps

| Question | Status |
|---|---|
| Is the Tanmatsu keypad *exactly* a KeebDeck, or a variant? | **Open.** Strong circumstantial evidence ([§1.1](#11-evidence-that-the-tanmatsu-keyboard-is-the-keebdeck-keyboard)); no vendor statement. Key labels definitely differ |
| KeebDeck footprint dimensions in full | Published by Solder Party in [`keebdeck_keyboard_hw`](https://github.com/solderparty/keebdeck_keyboard_hw) — **repo not cloned in this pass** |
| Tanmatsu `keyboard_matrix.kicad_sch` netlist | File retained at [`artifacts/schematics/kicad/`](artifacts/schematics/kicad/) but **not parsed**. Would give exact key↔diode↔LED placement |
| Does Tanmatsu populate the PAW-A350 trackpad cutout? | **No trackpad in the BOM.** The KeebDeck cutout exists but Tanmatsu appears not to use it |
| Is there a `volume_down` key? | Not in the coprocessor struct. Possibly `fn`+`volume_up` |
| Debounce strategy | The coprocessor does **no** debouncing — it reports raw matrix state at ~1 row/step. Debounce semantics live in the BSP, **not read in this pass** |
| Dome sheet lifetime / actuation force | Not published |
| Spare-part availability and price | Vendor says keyboard and dome sheet will be webshop spare parts "once Tanmatsu starts shipping". Not researched |

## Related

- [`README.md`](README.md) — device overview
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — I2C buses, coprocessor position
- [`development.md`](development.md) — BSP, keyboard API, AltGr layer
- [`bom.md`](bom.md) — the 72 diodes and 8 backlight LEDs
- [`sources.md`](sources.md) — provenance
