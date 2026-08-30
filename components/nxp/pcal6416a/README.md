# NXP PCAL6416A

- **Category:** **16-bit I²C-bus / SMBus GPIO expander** with **level translation**, open-drain interrupt output, hardware `RESET` input, and NXP's **"Agile I/O"** register extensions (programmable drive strength, input latch, per-pin pull-up/pull-down, interrupt mask, interrupt status, open-drain port configuration)
- **Marked part:** **`PCAL6416AHF,128`** — HWQFN24, topside mark `L16A`
- **I²C address on every Inkplate-family board:** **`0x20`** (`ADDR` pin strapped low)
- **Research status:** NXP datasheet **Rev. 7.1** held locally and read in full. Every one of the 16 port pins traced to a net on **three** boards from the resolved KiCad PCB netlists. Driver behaviour read out of the Inkplate Arduino library **v11.1.4** and the Inkplate MicroPython library
- **Retrieved:** 2026-08-24

`U9` on the [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md); `U10` on the [Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) and the [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md).

This chip is why an ESP32 with 34 GPIOs can drive a 1280 × 720 parallel e-paper panel at all. The panel needs **eight data lines plus five timing signals plus six PMIC control signals plus SD, battery and reset housekeeping**. Soldered's split is deliberate and worth understanding before you touch anything: **fast signals on native ESP32 pins, slow signals on this expander.** §5.

There is also a documented-but-widely-missed subtlety in this part's I²C behaviour that the shipped Arduino driver gets wrong. §7.1.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated by NXP in `artifacts/pcal6416a-datasheet-rev7.1.pdf` (Rev. 7.1, 30 August 2022) |
| **[SCH]** | Read out of **resolved net names in the KiCad `.kicad_pcb`** files listed in §14, via `devices/soldered-electronics/inkplate-5/tools/kicad_pcb_nets.py` |
| **[SRC]** | Read out of the Inkplate Arduino library **v11.1.4** or the Inkplate MicroPython library, with `file:line` |
| **[WEB]** | NXP's own product page at `nxp.com`, or another non-datasheet web source. Dated at retrieval |
| **[COM]** | Soldered's own end-user documentation, or community evidence. Attributed |
| **[INF]** | Inference. Not established by the above |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **NXP Semiconductors** (originally a Philips/Signetics I²C part line) | **[DOC]** |
| Part | `PCAL6416A` | **[DOC]** |
| Fitted variant | **`PCAL6416AHF`**, orderable **`PCAL6416AHF,128`** | **[SCH]** BOM value `PCAL6416AHF`; **[DOC]** Table 2 |
| Package | **HWQFN24** — plastic thermally-enhanced very-very-thin QFN, 24 terminals, **4 × 4 × 0.75 mm**, SOT994-1 | **[DOC]** Table 1 |
| Topside mark | **`L16A`** | **[DOC]** Table 1 |
| Packing | Reel 13", Q2/T3, MOQ 6000 | **[DOC]** Table 2 |
| Temperature range | **−40 °C to +85 °C** | **[DOC]** |
| Datasheet | **Product data sheet, Rev. 7.1 — 30 August 2022** | **[DOC]** |
| **Lifecycle** | **Active**, and enrolled in NXP's **Product Longevity Program** — *"Participating products are available for a minimum of 10 years"* | **[WEB]** nxp.com/products/PCAL6416A, 2026-08-24 |
| Relationship to `PCA6416A` | *"The PCAL6416A is a **pin-to-pin replacement for the PCA6416A**, with additional Agile I/O features"*; *"software backward compatible with PCA6416A **with interrupts disabled at power-up**"* | **[WEB]** |
| I²C address | `0100 000` + `ADDR` ⇒ **`0x20`** or `0x21`. Inkplate: `ADDR` → GND ⇒ **`0x20`** | **[DOC]** §7.1; **[SCH]** `U9.18 → GND` |
| Max I²C rate | **400 kHz** (Fast-mode) | **[DOC]** Table 39, `fSCL` |
| I/O tolerance | **5 V tolerant I/O ports** regardless of `VDD(P)` | **[WEB]**; consistent with **[DOC]** `VI` abs-max 6.5 V |
| ESD / latch-up | **2000 V HBM** (JESD22-A114-A), **1000 V CDM** (C101); latch-up **> 100 mA**, JESD78 Class II | **[WEB]** |
| Schmitt trigger on `SCL`/`SDA` | Yes — V<sub>hys</sub> ≈ **0.33 V** at 3.3 V (0.18 / 0.25 / 0.5 V at 1.8 / 2.5 / 5 V) | **[WEB]** |

### 1.1 Package variants — the topside mark is ambiguous

**[DOC]** Table 1. Four packages, and **two of them share the same topside mark**:

| Type number | Topside mark | Package | Body |
|---|---|---|---|
| `PCAL6416AEV` | **`L16A`** | VFBGA24 | 3 × 3 × 0.85 mm |
| `PCAL6416AEX1` | `16X` | X2QFN24 | 2.0 × 2.0 × 0.35 mm |
| **`PCAL6416AHF`** | **`L16A`** | **HWQFN24** | **4 × 4 × 0.75 mm** |
| `PCAL6416APW` | `PCAL6416A` | TSSOP24 | 4.4 mm body width |

> ⚠ `L16A` identifies **either** the BGA **or** the QFN. On a board you cannot read a schematic for, identify by package shape, not by marking. The Inkplate is unambiguously the **HWQFN24** — 4 × 4 mm, leadless, with a centre pad. Soldered's own end-user documentation uses exactly this as the identification cue: *"If your Inkplate has a smaller one (QFN-24 package), it is PCAL. If there is a bigger IC (28-pin SSOP package), it is the [MCP23017](#12--generation-note-mcp23017-vs-pcal6416a)."* **[COM]**

**The `EX1` suffix encodes a date code, not a variant:** *"'X' rotates from 1 to 5 and indicates the work week of the indicated month"* **[DOC]** note [1].

### 1.2 ⚠ Generation note: MCP23017 vs PCAL6416A

Older, **e-radionica-branded (blue PCB)** Inkplates fit a **Microchip MCP23017** instead. Soldered says there is no functional difference for end users, and the Arduino library abstracts both behind an identical `IOExpander` class selected at compile time:

```c
#if defined(ARDUINO_INKPLATE10) || defined(ARDUINO_INKPLATE6) || defined(ARDUINO_INKPLATE6PLUS)
#include "mcpExpander/mcpExpander.h"
#else
#include "pcalExpander/pcalExpander.h"
#endif
```
— `src/system/ExpanderSelect.h` **[SRC]**

**The Inkplate 5 and 5 Gen 2 are Soldered-era and always PCAL6416A.** But the two chips are **not** register-compatible, and the abstraction is where the bug in §7.1 comes from. Also **[COM]**: *"If your Inkplate has a PCAL expander, you must use the 'Soldered Inkplate …' board definition, otherwise choose the 'e-radionica Inkplate …' board in Arduino IDE."*

---

## 2. Pinout

**[DOC]** Figure 3 (HWQFN24), with the **actual Inkplate net on every pin** from **[SCH]**. Verified identical on Inkplate 5 (`U9`), Inkplate 5 Gen 2 (`U10`) and ZeroWriter Ink (`U10`) except where noted.

| Pin | Name | Inkplate net | Function on the board |
|---:|---|---|---|
| 1 | `P0_0` | `EPD_OE` | Panel **output enable** |
| 2 | `P0_1` | `EPD_GMODE` | Panel **gate mode** |
| 3 | `P0_2` | `EPD_SPV` | Panel **vertical start pulse** |
| 4 | `P0_3` | `WAKEUP` | [TPS65186](../../texas-instruments/tps65186/README.md) pin 5 — wake |
| 5 | `P0_4` | `PWRUP` | TPS65186 pin 22 — **run the power sequence** |
| 6 | `P0_5` | `VCOM_CTRL` | TPS65186 pin 12 — VCOM amplifier enable |
| 7 | `P0_6` | `INT` | TPS65186 pin 2 — **`nINT`, open-drain, no external pull-up** |
| 8 | `P0_7` | `PWR_GOOD` | TPS65186 pin 24 — **open-drain, no external pull-up** |
| 9 | `VSS` | `GND` | Ground |
| 10 | `P1_0` | `GPIO_0_MOSFET` | Gate of `Q1` — **`Q1` and `R19` are DNP on Inkplate 5.** §5.3 |
| 11 | `P1_1` | via `JP6`/`JP8` → `V_BAT_MOS` | Battery-measurement divider enable (`Q4`) |
| 12 | `P1_2` | via `JP5`/`JP7` → `GPB_2` | **microSD power switch** (`Q10` P-MOS). §5.2 |
| 13 | `P1_3` | `GPB_3` → header | User GPIO — **but `PWR_LED` on ZeroWriter Ink.** §5.4 |
| 14 | `P1_4` | `GPB_4` → header | User GPIO |
| 15 | `P1_5` | `GPB_5` → header | User GPIO |
| 16 | `P1_6` | `GPB_6` → header | User GPIO |
| 17 | `P1_7` | `GPB_7` → header | User GPIO |
| 18 | **`ADDR`** | **`GND`** | ⇒ I²C address **`0x20`** |
| 19 | `SCL` | `I2C_SCL` | Shared with the TPS65186 (`0x48`) and the PCF85063A RTC |
| 20 | `SDA` | `I2C_SDA` | " |
| 21 | **`VDD(P)`** | `3V3` | Port supply |
| 22 | **`INT`** | `INTB` → `R47` 10 kΩ pull-up to `3V3`, and via `JP4` to **ESP32 `IO34`** | Expander interrupt out |
| 23 | **`VDD(I2C-bus)`** | `3V3` | I²C-side supply |
| 24 | **`RESET`** | `RST` | **Tied to the board reset net.** §4.2 |
| **25** | Centre pad | `GND` | **[DOC]**: *"must be connected only as a secondary ground or must be left electrically open"* — the board grounds it ✅ |

---

## 3. Electrical characteristics

**[DOC]** §10–§13.

### 3.1 Supplies and voltage translation

The part has **two independent supplies** and that is its headline feature over a plain PCA9555:

| Supply | Range | On Inkplate |
|---|---|---|
| `VDD(I2C-bus)` — SCL, SDA, RESET, INT | **1.65 – 5.5 V** | **3.3 V** |
| `VDD(P)` — port pins P0_x/P1_x, ADDR | **1.65 – 5.5 V** | **3.3 V** |

**Any combination of {1.8, 2.5, 3.3, 5} V is supported** **[DOC]** Table 4 — so the same part can bridge a 1.8 V host to 5 V I/O, or vice versa. The Inkplate does not exploit this (both rails are 3.3 V from the same `3V3` net **[SCH]**), but it is why you would choose this part over a PCA9555 in a new design.

Input thresholds scale with the relevant supply: `VIH` = 0.7 × VDD, `VIL` = 0.3 × VDD, with the **I²C-bus** supply governing `SCL`/`SDA`/`RESET` and the **port** supply governing `ADDR` and the port pins **[DOC]** Table 32.

### 3.2 Current limits

| Parameter | Value | Note |
|---|---|---|
| `IOH` per port pin, **recommended** | **10 mA** | **[DOC]** Table 32 |
| `IOL` per port pin, **recommended** | **25 mA** | **[DOC]** Table 32 |
| `IOL` per port pin, absolute max | 50 mA | **[DOC]** Table 31 |
| `IOL` on `SDA` / `INT`, absolute max | 25 mA | |
| **`IDD(P)` total through `VDD(P)`, absolute max** | **160 mA** | The real package-level ceiling |
| `IDD` total through `VSS`, absolute max | 200 mA | |
| `IDD(I2C-bus)` absolute max | 10 mA | |
| Clamping currents (`ADDR`, `RESET`, `SCL`, `INT`, port) | ±20 mA | |
| `Tj(max)` | 125 °C | |
| `Zth(j-a)` HWQFN24 | 66 K/W | **[DOC]** Table 33 |

> **You cannot drive 16 pins at 25 mA each.** 16 × 25 mA = 400 mA, far past the 160 mA `VDD(P)` ceiling. Sum your loads. **[DOC]** + **[INF]**

### 3.3 Quiescent current — why this part suits a battery e-reader

**[DOC]** Table 34, at `VDD(P)` = 2.3–3.6 V:

| Condition | Typ | Max |
|---|---:|---:|
| Idle, `fSCL` = 0, all pins inputs | **1 µA** | 3.2 µA |
| Bus active at 400 kHz, pins inputs | 6.5 µA | 15 µA |
| **Continuous register read at 400 kHz** | 40 µA | 75 µA |
| **Any internal pull-up enabled with the pin pulled to VSS** | **1.1 mA** | 1.5 mA |

> ⚠ **The last row is the deep-sleep trap.** A single enabled internal pull-up on a pin that is being held low costs **more than a milliamp** — a thousand times the idle current, and comparable to the whole rest of an Inkplate in deep sleep. The internal pull-ups are ~100 kΩ, so this figure is not the resistor: it is the analogue bias circuitry. **Turn pull-ups off before sleeping.** **[DOC]** + **[INF]**

### 3.4 Power-on reset

`VPOR` = **1.1 V typ, 1.4 V max** **[DOC]** Table 34. Registers initialise when `VDD(P)` crosses it. Critically: *"After that, `VDD(P)` must be lowered to below `VPOR` and back up to the operating voltage for a power-reset cycle"* **[DOC]** §7.6 — a brown-out that dips to, say, 2 V does **not** re-run POR, and the part comes back with whatever register state survived. This is exactly why a hardware `RESET` pin exists, and why the Inkplate wires it. §4.2.

---

## 4. Functional behaviour

### 4.1 Interrupt output

**[DOC]** §7.8.

- **`INT` is open-drain** and needs an external pull-up. On the Inkplate that is `R47`, 10 kΩ to `3V3` **[SCH]**.
- **Any rising or falling edge** on a pin configured as an input generates an interrupt. **There is no edge-select register** — you cannot ask for rising-only.
- The interrupt clears when the port that caused it is read, **or** when the input returns to its original value. Clearing happens at the ACK/NACK bit after the rising SCL edge, and *"interrupts that occur during the ACK or NACK clock pulse can be lost"*.
- **A pin configured as an output cannot cause an interrupt.** Switching a pin from output to input **may cause a false interrupt** if the pin level does not match the Input Port register.
- With the **input latch** (`0x44`/`0x45`) enabled, the pin state is captured and the interrupt is cleared **only** by reading the input port — the "returns to original state" escape is removed. This is how you avoid missing a short pulse.

The Arduino driver implements exactly this trade-off and documents the hardware limitation honestly **[SRC]** (`pcalExpander.cpp:203-214` doc comment, `414-441` implementation):

```c
// CHANGE (default): interrupt on any edge, latch disabled.
// FALLING / RISING: interrupt on any edge (hardware limitation --
// PCAL6416A has no edge-select registers), but input latch is
// enabled so the interrupt is held until the input port is read
```

`getInt()` reads the **Interrupt Status** register pair (`0x4C`/`0x4D`) and returns a 16-bit mask, which is the right way to find the source **[SRC]** (`pcalExpander.cpp:469-475`).

### 4.2 Reset — and what it is tied to on the Inkplate

**[DOC]** §7.7: hold `RESET` low for `tw(rst)` and all registers and the I²C state machine return to defaults. *"This input requires a pull-up resistor to `VDD(I2C-bus)` if no active connection is used."*

On the Inkplate the pin is **actively driven**, and the net it joins is instructive **[SCH]**:

```
RST  (3)  U10.3   <- ESP32-WROVER EN
          U2.1    <- TPS3840PL27DBVR voltage supervisor
          U9.24   <- PCAL6416A RESET
```

So **the expander is reset by the same supervisor that resets the ESP32**, and by the same edge the reset button produces. Two consequences:

- ✅ There is no window in which the ESP32 has restarted but the expander still holds stale port state. On a brown-out that trips the supervisor, both come up together. This is good design and worth copying.
- ⚠ **Conversely, `RST` is `EN`.** Anything that pulls `EN` low to reset the ESP32 also wipes the expander — including a debugger, the auto-reset circuit on the USB-UART bridge, and `esp_restart()` paths that assert `EN`. Firmware must therefore reconfigure the expander after **every** reset, not only after power-on. `Inkplate::begin()` does. Hand-rolled code that caches expander state across a soft reset will not. **[SCH]** + **[INF]**

### 4.3 Port structure defaults

**[DOC]** §7.4. After POR or `RESET`:

| Register | Default | Meaning |
|---|---|---|
| Configuration (`0x06`/`0x07`) | `0xFF` | **All pins inputs** |
| Output port (`0x02`/`0x03`) | **`0xFF`** | Output latches preloaded **high** |
| Polarity inversion (`0x04`/`0x05`) | `0x00` | No inversion |
| Drive strength (`0x40`–`0x43`) | `0xFF` | **1× (full) drive** |
| Input latch (`0x44`/`0x45`) | `0x00` | Not latched |
| Pull-up/down enable (`0x46`/`0x47`) | `0x00` | **Disconnected** |
| Pull-up/down select (`0x48`/`0x49`) | `0xFF` | Pull-**up** selected (but disabled by the line above) |
| Interrupt mask (`0x4A`/`0x4B`) | `0xFF` | **All masked** — *"disabling interrupts during system start-up"* |
| Interrupt status (`0x4C`/`0x4D`) | `0x00` | — |
| Output port config (`0x4F`) | `0x00` | **Both ports push-pull** |

> ⚠ **The output latch defaults to `0xFF`, i.e. HIGH.** NXP advertises *"no glitch on power-up"* **[WEB]** — and that is true, because every pin comes up as a **high-impedance input**. But the moment you make a pin an output, the pre-loaded latch drives it **high**. So the naïve sequence "set pin to OUTPUT, then set it LOW" produces a **glitch high** for the duration of one I²C transaction. On a pin that gates a MOSFET or asserts `PWRUP` on a PMIC, that glitch matters. The Inkplate driver handles it correctly and says so **[SRC]** (`pcalExpander.cpp:325-326`):
>
> ```c
> // There is a one cacth! Pins are by default (POR) set as HIGH. So first change it to LOW and then set is as output).
> ```
>
> It writes the **output port register first**, then the configuration register. Copy that ordering.

---

## 5. Exact role on the Inkplate family

### 5.1 The fast/slow split

**[SCH]** + **[SRC]**. This is the architectural decision the expander exists to serve.

| Panel/PMIC signal | Where it lives | Why |
|---|---|---|
| `EPD_D0`–`D7` | **ESP32 GPIO 4, 5, 18, 19, 23, 25, 26, 27** | Clocked out by the **I2S1 peripheral in parallel mode via DMA** at ~16 MHz. Must be native |
| `EPD_CL` | **ESP32 GPIO 0** (I2S bit clock), through `JP7` and buffer `U8` | Pixel clock. Must be native |
| `EPD_LE` | ESP32 GPIO 2 | Toggled per line inside the DMA loop |
| `EPD_CKV` | ESP32 GPIO 32 | Gate clock, toggled per line |
| `EPD_SPH` | ESP32 GPIO 33 | Horizontal start, toggled per line |
| **`EPD_OE`** | **Expander `P0_0`** | Set once per refresh |
| **`EPD_GMODE`** | **Expander `P0_1`** | Set once per refresh |
| **`EPD_SPV`** | **Expander `P0_2`** | Set once per frame |
| **`WAKEUP` / `PWRUP` / `VCOM_CTRL`** | **Expander `P0_3`/`P0_4`/`P0_5`** | Set once per power cycle |

Pin assignments confirmed from `src/boards/Inkplate5/pins.h` and `src/boards/Inkplate5V2/pins.h`, which are byte-identical apart from the include guard **[SRC]**:

```c
#define IO_INT_ADDR 0x20
#define SD_PMOS_PIN IO_PIN_B2   // 10
#define WAKEUP 3
#define PWRUP  4
#define VCOM   5
#define OE     0
#define GMOD   1
#define SPV    2
```
— `src/boards/Inkplate5/pins.h:7-57`

and independently from the MicroPython port, which names **all sixteen** **[SRC]** (`boards/inkplate5/inkplate5.py:97-140`):

```python
cls.EPD_OE       = GpioPin(cls._PCAL6416A, 0,  mode_output)
cls.EPD_GMODE    = GpioPin(cls._PCAL6416A, 1,  mode_output)
cls.EPD_SPV      = GpioPin(cls._PCAL6416A, 2,  mode_output)
cls.TPS_WAKEUP   = GpioPin(cls._PCAL6416A, 3,  mode_output)
cls.TPS_PWRUP    = GpioPin(cls._PCAL6416A, 4,  mode_output)
cls.TPS_VCOM     = GpioPin(cls._PCAL6416A, 5,  mode_output)
cls.TPS_INT      = GpioPin(cls._PCAL6416A, 6,  mode_input)
cls.TPS_PWR_GOOD = GpioPin(cls._PCAL6416A, 7,  mode_input)
cls.GPIO0_PUP    = GpioPin(cls._PCAL6416A, 8,  mode_output)
cls.VBAT_EN      = GpioPin(cls._PCAL6416A, 9,  mode_output)
cls.SD_ENABLE    = GpioPin(cls._PCAL6416A, 10, mode_output)
```

**Cost of the split:** `einkOn()` is roughly *six* I²C transactions plus a poll loop before a single pixel moves. That is why `display(leaveOn = true)` exists.

### 5.2 The microSD power switch — `P1_2`

**[SCH]**, Inkplate 5:

```
GPB_2           (3)  JP5.1, Q10.1, R40.2      <- Q10 gate, 100k pull-up R40 to 3V3
Net-(JP5-Pad2)  (2)  JP5.2, U9.12             <- expander P1_2
3V3_MICROSD     (9)  Q10.3, JP1.1, K11.4, C37/C38/C39, R43/R44/R45
3V3             (…)  Q10.2                    <- P-MOS source
```

`Q10` is a **P-channel MOSFET high-side switch** between `3V3` and `3V3_MICROSD`. `R40` (100 kΩ) holds the gate high — **switch off** — by default. Expander `P1_2` reaches the gate through **solder jumper `JP5`** (`JP7` on Gen 2 / ZeroWriter).

The driver exploits the pull-up rather than fighting it **[SRC]**:

```c
int16_t EPDDriver::sdCardInit() {
    expander1.pinMode(SD_PMOS_PIN, OUTPUT);
    expander1.digitalWrite(SD_PMOS_PIN, LOW);   // pull gate low -> P-MOS ON
    delay(50);
    spi2.begin(14, 12, 13, 15);
    ...
}
void EPDDriver::sdCardSleep() {
    pinMode(12/13/14/15, INPUT);                // release the SPI bus
    expander1.pinMode(SD_PMOS_PIN, INPUT);      // release gate -> R40 pulls it high -> OFF
}
```
— `Inkplate5V2Driver.cpp:888-912`

Note the elegance: **turning the card off is `pinMode(INPUT)`, not `digitalWrite(HIGH)`.** Releasing the pin lets the 100 kΩ do the work, and it is also the safe state if the expander is reset.

> ⚠ **`Inkplate::begin()` leaves the SD card powered OFF** — `gpioInit()` ends with `expander1.pinMode(SD_PMOS_PIN, INPUT)` and the comment *"And also disable uSD card supply"* **[SRC]** (`Inkplate5V2Driver.cpp:834-835`). **If you talk to the SD card without calling `sdCardInit()` first, it will not respond, and the failure looks like a dead card or a broken SPI bus.** This is the single most common first-time Inkplate SD failure. Then the 50 ms settle in `sdCardInit()` is not optional either — card supplies need it.

### 5.3 `P1_0` (`GPIO0_ENABLE`) drives an unpopulated part on Inkplate 5

`gpioInit()` does:

```c
expander1.pinMode(GPIO0_ENABLE, OUTPUT);   // GPIO0_ENABLE == 8 == P1_0
expander1.digitalWrite(GPIO0_ENABLE, 1);
```
— `Inkplate5V2Driver.cpp:810-811` **[SRC]**, `GPIO0_ENABLE 8` from `system/defines.h:74`

But the netlist says **[SCH]**:

```
GPIO_0_MOSFET  (3)  Q1.1, R19.2, U9.10
```

…and both `Q1` and `R19` are **`DNP`** in the Inkplate 5 BOM **[SCH]** (`CTRL & COMS.kicad_sch`). On other Inkplates this pin gates a transistor that pulls ESP32 `GPIO0`; here the transistor is not fitted. **`P1_0` on an Inkplate 5 is an output driving nothing.**

Practical reading: it is free for user I/O at the header pad — **but the library drives it high in `begin()` on every boot** and does not block it, so any user of `P1_0` is fighting `begin()`. **[SCH]** + **[SRC]** + **[INF]**

### 5.4 ZeroWriter Ink repurposes `P1_3`

Comparing the resolved netlists of the stock Gen 2 board and the ZeroWriter respin **[SCH]**:

| Pin | Soldered Inkplate 5 Gen 2 | **ZeroWriter Ink** |
|---|---|---|
| `P1_3` (pin 13) | `/MCU/GPB_3` → header pad `K25` | **`PWR_LED`** → `K1.2` and `K9.1` |
| `P1_4`–`P1_7` | `GPB_4`–`GPB_7` → header pads | unchanged (`GPB_4`–`GPB_7`) |
| everything else | — | **identical** |

`K1` on the ZeroWriter main board is the `HC-1.25-16PWT` link to the breakout PCB, which also carries `3V3_MICROSD`, `PWR_SW`, `CHRG-ST` and the SD SPI bus. So **on a ZeroWriter Ink, expander `P1_3` is the front-panel power LED**, not a user GPIO — and any Inkplate example that writes to expander pin 11 will blink it. Everything else about the expander block, including the `JP7` SD jumper, is unchanged from the stock Gen 2. **[SCH]**

### 5.5 Which pins the library protects

`Inkplate::begin()` → `blockGpioPins()` at `Inkplate5V2Driver.cpp:116` **[SRC]**:

```c
void EPDDriver::blockGpioPins() {
    expander1.blockPinUsage(WAKEUP);  // 3
    expander1.blockPinUsage(PWRUP);   // 4
    expander1.blockPinUsage(VCOM);    // 5
    expander1.blockPinUsage(OE);      // 0
    expander1.blockPinUsage(GMOD);    // 1
    expander1.blockPinUsage(SPV);     // 2
}
```

`pinMode()`, `digitalWrite()` and `digitalRead()` become silent no-ops on those six unless the caller passes `_bypassCheck = true` — which the internal code does everywhere **[SRC]** (`pcalExpander.cpp:151-201`).

| Expander pin | Blocked? | Actually safe for user code? |
|---:|---|---|
| `P0_0`–`P0_2` (OE/GMOD/SPV) | ✅ blocked | ❌ Panel control |
| `P0_3`–`P0_5` (WAKEUP/PWRUP/VCOM) | ✅ blocked | ❌ PMIC control |
| **`P0_6` (`nINT`)** | ❌ **not blocked** | ⚠ Input from the PMIC. Reading it is fine and useful (enable a pull-up first — §7.2); **driving it is contention** |
| **`P0_7` (`PWR_GOOD`)** | ❌ **not blocked** | ⚠ Same |
| **`P1_0` (`GPIO0_ENABLE`)** | ❌ not blocked | ⚠ Driven high by `begin()`; DNP load on Inkplate 5 (§5.3) |
| **`P1_1` (`VBAT_EN`)** | ❌ not blocked | ⚠ Battery-measurement enable; `begin()` drives it low |
| **`P1_2` (`SD_PMOS_PIN`)** | ❌ not blocked | ⚠ SD card power (§5.2) |
| `P1_3`–`P1_7` | ❌ not blocked | ✅ Header pads — **except `P1_3` on ZeroWriter Ink** (§5.4) |

> Soldered's documentation warns *"**DO NOT USE** pins that are not available! Using those, you might **permanently damage the screen**. Usage is limited by the library, but just in case don't use them!"* **[COM]**. That is accurate for `P0_0`–`P0_5`. It is **not** accurate for `P0_6`–`P1_2`, which have board functions and are **not** blocked. **[SRC]** + **[INF]**

---

## 6. Register map

**[DOC]** Table 6 and §7.4, complete. Note the **non-contiguous address space** — this is the crux of §7.1.

| Addr | Register | Access | Default | Notes |
|---|---|---|---|---|
| `0x00` | Input port 0 | R | — | Live pin state (or latched value, per `0x44`) |
| `0x01` | Input port 1 | R | — | |
| `0x02` | Output port 0 | R/W | `1111 1111` | ⚠ Defaults **high** |
| `0x03` | Output port 1 | R/W | `1111 1111` | |
| `0x04` | Polarity inversion 0 | R/W | `0000 0000` | 1 = invert the **input** reading |
| `0x05` | Polarity inversion 1 | R/W | `0000 0000` | |
| `0x06` | Configuration 0 | R/W | `1111 1111` | **1 = input**, 0 = output |
| `0x07` | Configuration 1 | R/W | `1111 1111` | |
| — | **⟨ gap: `0x08`–`0x3F` unimplemented ⟩** | | | |
| `0x40` | Output drive strength 0 — `CC0.0`–`CC0.3` | R/W | `1111 1111` | 2 bits/pin |
| `0x41` | Output drive strength 0 — `CC0.4`–`CC0.7` | R/W | `1111 1111` | |
| `0x42` | Output drive strength 1 — `CC1.0`–`CC1.3` | R/W | `1111 1111` | |
| `0x43` | Output drive strength 1 — `CC1.4`–`CC1.7` | R/W | `1111 1111` | |
| `0x44` | Input latch 0 | R/W | `0000 0000` | 1 = latch input state until read |
| `0x45` | Input latch 1 | R/W | `0000 0000` | |
| `0x46` | Pull-up/pull-down **enable** 0 | R/W | `0000 0000` | 1 = resistor connected |
| `0x47` | Pull-up/pull-down **enable** 1 | R/W | `0000 0000` | |
| `0x48` | Pull-up/pull-down **selection** 0 | R/W | `1111 1111` | **1 = pull-up**, 0 = pull-down |
| `0x49` | Pull-up/pull-down **selection** 1 | R/W | `1111 1111` | |
| `0x4A` | Interrupt mask 0 | R/W | `1111 1111` | **1 = masked** |
| `0x4B` | Interrupt mask 1 | R/W | `1111 1111` | |
| `0x4C` | Interrupt status 0 | **R** | `0000 0000` | Which pin caused it |
| `0x4D` | Interrupt status 1 | **R** | `0000 0000` | |
| — | `0x4E` unimplemented | | | |
| `0x4F` | Output port configuration | R/W | `0000 0000` | bit 0 = `ODEN0`, bit 1 = `ODEN1`; 1 = **open-drain** |

### 6.1 The Agile I/O extensions, in one paragraph each

**Drive strength (`0x40`–`0x43`)** — two bits per pin: `00` = 0.25×, `01` = 0.5×, `10` = 0.75×, `11` = 1× of full drive **[DOC]** §7.4.5. Full drive is characterised at `IOH` = −10 mA / `IOL` = 10 mA (with tighter `VOH`/`VOL` at `CC` = `11b`). Useful for EMI reduction on long or noisy traces. **The Inkplate never writes these**, leaving everything at 1×.

**Input latch (`0x44`/`0x45`)** — see §4.1. Only meaningful for pins configured as inputs.

**Pull-up/pull-down (`0x46`–`0x49`)** — enable is separate from direction. The resistor is **100 kΩ typ (50 kΩ min, 150 kΩ max)** **[DOC]** §7.4.8. *"The resistors will be disconnected when the outputs are configured as open-drain outputs."* See the current warning in §3.3.

**Interrupt mask (`0x4A`/`0x4B`)** — masked by default. Un-masking a pin that is *currently* changed will assert `INT` immediately; masking the pin currently asserting `INT` de-asserts it **[DOC]** §7.4.9.

**Interrupt status (`0x4C`/`0x4D`)** — read-only source identification.

**Output port configuration (`0x4F`)** — port-wise, not per-pin. *"The recommended command sequence is to program this register (`0x4F`) **before** the configuration register (`0x06`/`0x07`) sets the port pins as outputs"* **[DOC]** §7.4.11. Setting a port open-drain also disconnects its pull-ups.

---

## 7. ⚠ I²C behaviour, and a bug in the shipped Arduino driver

### 7.1 Registers toggle **within a pair**. They do not auto-increment.

This is the single most important thing to know about programming this chip, it is stated plainly in the datasheet, and it is very easy to miss because almost every other I²C part behaves differently.

**[DOC]** §8.1 (writes):

> *"Twenty-two registers within the PCAL6416A are configured to operate as **eleven register pairs**… After sending data to one register, **the next data byte is sent to the other register in the pair**. For example, if the first byte is sent to Output Port 1 (register 3), the next byte is stored in Output Port 0 (register 2). There is no limit on the number of data bytes sent in one write transmission."*

**[DOC]** §8.2 (reads):

> *"After the first byte is read, additional bytes may be read, but the data now reflects the information in **the other register in the pair**. For example, if Input Port 1 is read, the next byte read is Input Port 0."*

So a burst of *N* bytes starting at `0x00` returns `IN0, IN1, IN0, IN1, …` — **it never advances to `0x02`.** The address space is not linear anyway (§6): there is a 56-register hole between `0x07` and `0x40`.

Now compare `IOExpander::begin()` **[SRC]** (`pcalExpander.cpp:49-61`):

```c
void IOExpander::readPCALRegisters()
{
    Wire.beginTransmission(_ioExpanderI2CAddress);
    Wire.write(0x00);
    Wire.endTransmission();
    Wire.requestFrom(_ioExpanderI2CAddress, (uint8_t)23);
    for (int i = 0; i < 23; i++)
        _ioExpanderRegs[i] = Wire.read();
}
```

**Twenty-three bytes read from `0x00`.** Per the datasheet that returns Input Port 0 and Input Port 1 alternating twelve and eleven times respectively, so the 23-byte shadow copy `_ioExpanderRegs[]` — which the whole driver then uses for read-modify-write — is filled with **the live state of the two input ports, in every slot**, not the register contents it is named for.

**Where this comes from.** The MCP23017 sibling driver does the structurally identical thing — and for the **MCP23017 it is correct**, because that part auto-increments linearly across `0x00`–`0x15` in its default BANK = 0 mode:

```c
Wire.write(0x00);
Wire.requestFrom(_ioExpanderI2CAddress, (uint8_t)22);
for (int i = 0; i < 22; i++) _ioExpanderRegs[i] = Wire.read();
```
— `src/system/mcpExpander/mcpExpander.cpp:87-96` **[SRC]**, and its own comment at line 58 explicitly relies on sequential ordering: *"The bulk read in readMCPRegisters() returns registers 0x00..0x15 sequentially."*

**The PCAL driver is a port of the MCP driver that carried over an addressing assumption that does not hold.** `updatePCALAllRegisters()` (`pcalExpander.cpp:109-120`) has the mirror-image problem on the write side — 23 bytes from `0x00` land alternately in the two read-only Input Port registers, so it is simply a no-op. It is not called from any board driver.

**Independent confirmation that this is wrong:** Soldered's own **MicroPython** driver for the same chip reads all 23 registers **one at a time, by address** **[SRC]** (`Inkplate-micropython/shared/drivers/pcal6416a.py:84-106`):

```python
self.ioRegsInt[0] = self.read(PCAL6416A_INPORT0)
self.ioRegsInt[1] = self.read(PCAL6416A_INPORT1)
self.ioRegsInt[2] = self.read(PCAL6416A_OUTPORT0)
...
self.ioRegsInt[22] = self.read(PCAL6416A_OUTPORT_CONF)
```

Twenty-three separate transactions, same shadow array, correct data. Whoever wrote the MicroPython port knew.

**Does it break real boards?** Evidently not fatally — Inkplates ship and work. The reason is **[INF]**, and worth spelling out because it bounds the risk:

- Every pin the driver actually uses is explicitly `pinMode()`d before it is written, and `pinModeInternal()` **clears** the relevant bit in the shadow and writes the whole byte out, so each used pin converges to the intended state.
- But `pinModeInternal(OUTPUT)` writes the **entire** Configuration and Output Port byte from the shadow. The first such call on Port 0 therefore sets the direction of **all eight** Port-0 pins from a sample of the floating input pins taken during `begin()`.
- On Inkplate 5, `P0_3`/`P0_4`/`P0_5` have external pull-downs, so they sample 0 and become outputs — which is what is wanted. `P0_0`–`P0_2` go to the (unpowered) panel and `P0_6`/`P0_7` are open-drain PMIC outputs **with no pull-up** (§7.2) — all five sample **indeterminately**.
- The concrete residual risk is that **`P0_6` (`nINT`) and `P0_7` (`PWR_GOOD`) may end up configured as push-pull outputs**, contending with the PMIC's open-drain drivers when the PMIC asserts them. `P0_6` is corrected to `INPUT_PULLUP` if VCOM programming ever runs; `P0_7` never is.
- `digitalWriteInternal()` also silently **returns without doing anything** if the shadow's Configuration bit says the pin is an input (`pcalExpander.cpp:373-374`) — so a corrupted shadow can turn a `digitalWrite()` into a no-op.

> **Evidence boundary.** The datasheet statement (§8.1/§8.2) is **[DOC]** and unambiguous. The code is **[SRC]**. That the shadow array is therefore garbage is a direct **[DOC]** + **[SRC]** consequence. The specific downstream effects listed above are **[INF]** — they depend on levels sampled from floating pins and have **not** been observed on hardware. Do not report this as "the Inkplate library is broken"; report it as "the shadow copy is not what it claims to be, and here is the bounded consequence."
>
> **If you write your own driver: read registers individually, or in pairs, and never in bursts spanning pairs.**

### 7.2 Neither PMIC status line has an external pull-up

**[SCH]**, on all three boards:

```
INT       (2)  U1.2,  U9.7      <- TPS65186 nINT  -> P0_6
PWR_GOOD  (2)  U1.24, U9.8      <- TPS65186 PWR_GOOD -> P0_7
```

Two nodes each. **No resistor.** Both TPS65186 pins are open-drain **[DOC]** (TPS65186 §Pin Functions), so with the expander pin as a plain input, the "inactive" state is a **float**.

The only place the library gets this right is VCOM programming, where it enables the expander's own ~100 kΩ pull-up first **[SRC]** (`Inkplate5V2Driver.cpp:1072`):

```c
expander1.pinMode(6, INPUT_PULLUP);       // sets 0x06 bit6, 0x46 bit6, 0x48 bit6
```

Everywhere else, `PWR_GOOD` is ignored entirely and the driver polls the PMIC's `PG` register (`0x0F`) over I²C instead — the right call, and it yields per-rail detail the single pin cannot. See [TPS65186 §6.4](../../texas-instruments/tps65186/README.md).

> **If you want interrupt- or pin-driven PMIC monitoring, you must enable the internal pull-up on `P0_6` and/or `P0_7` yourself.** Nothing else on the board will. And remember §3.3: an enabled pull-up on a pin held low costs ~1.1 mA. **[SCH]** + **[DOC]** + **[INF]**

### 7.3 Bus sharing

`I2C_SCL`/`I2C_SDA` carry at least three devices on an Inkplate 5 **[SCH]**:

| Device | Address |
|---|---|
| **PCAL6416A** | **`0x20`** |
| [TPS65186](../../texas-instruments/tps65186/README.md) | `0x48` |
| PCF85063A RTC | `0x51` |
| plus whatever is plugged into the **easyC / Qwiic** connector `K3` | — |

No collisions, and the expander's alternative address `0x21` is free. **400 kHz is the expander's ceiling** **[DOC]**; check the slowest device on the bus before raising `Wire.setClock()`. The library serialises access through `i2cStart()`/`i2cEnd()` (`system/inkplateSemaphore.h`) **[SRC]** — respect that if you add your own transactions from another task.

---

## 8. Driver and library guidance

### 8.1 Arduino — Inkplate library v11.1.4

Class `IOExpander`, exposed as `display.expander1` **[SRC]**:

| Call | Notes |
|---|---|
| `expander1.begin(0x20)` | Called by `Inkplate::begin()`. Returns `false` if the address does not ACK |
| `expander1.pinMode(pin, mode, bypass = false)` | `INPUT`, `OUTPUT`, `INPUT_PULLUP`, `INPUT_PULLDOWN`. `pin` 0–15 |
| `expander1.digitalWrite(pin, state, bypass = false)` | **No-op if the shadow thinks the pin is an input** — §7.1 |
| `expander1.digitalRead(pin, bypass = false)` | |
| `expander1.setPorts(uint16_t)` / `getPorts()` | Both ports at once |
| `expander1.setIntPin(pin, mode)` | `CHANGE` (no latch) or `RISING`/`FALLING` (latch on). **No true edge selection** — §4.1 |
| `expander1.removeIntPin(pin)` | Re-masks |
| `expander1.getInt()` | Reads `0x4C`/`0x4D`, returns a 16-bit source mask |
| `expander1.blockPinUsage(pin)` / `unblockPinUsage(pin)` | The soft-lock of §5.5 |

**There is no separate library to install.** The expander driver ships inside `InkplateLibrary`; there is no standalone Soldered PCAL6416A Arduino library.

If you want a generic driver for a non-Inkplate design, the practical community options are **[WEB]**, 2026-08-24:

| Library | Notes |
|---|---|
| **`adafruit/Adafruit_PCA9555`**-style PCA9555 drivers | Cover only `0x00`–`0x07`. **None of the Agile I/O registers.** Work, but you lose pull-ups, latch, drive strength and interrupt mask |
| Zephyr `gpio_pcal64xxa` | Real PCAL6416A/PCAL6408A driver in mainline Zephyr, Agile-I/O aware. The best reference implementation if you are writing your own |
| Linux `drivers/gpio/gpio-pca953x.c` | Mainline, has explicit `PCAL6416` support including the `_PCAL_` extended registers. Also a good reference |

### 8.2 MicroPython

`Inkplate-micropython/shared/drivers/pcal6416a.py`. Same constants, same shadow-array design, but with the **correct per-register reads** (§7.1). API is `pin_mode(pin, mode)`, `digital_write(pin, v)`, `digital_read(pin)`, wrapped by the `GpioPin` helper used in `boards/inkplate5/inkplate5.py`.

### 8.3 ESP-IDF

**No Espressif-supplied `esp_io_expander` component targets the PCAL6416A.** Espressif ships `esp_io_expander_tca9554` and `esp_io_expander_ht8574`; the PCAL6416A is not among them **[WEB]**, 2026-08-24 (search negative, not proof of absence).

Writing your own is ~100 lines against `driver/i2c_master.h`. The only non-obvious rules are:

```c
// 1. Registers are NOT linearly auto-incrementing. Read/write ONE register,
//    or exactly TWO if they are a documented pair. Never burst across pairs.
// 2. Set the OUTPUT PORT register BEFORE the CONFIGURATION register when
//    making a pin an output -- the output latch defaults to HIGH (4.3).
// 3. Set 0x4F (open-drain) before 0x06/0x07 if you want open-drain outputs.
// 4. INT is open-drain; you need a pull-up. Interrupt masks default to
//    ALL MASKED (0xFF), so nothing interrupts until you clear a mask bit.
// 5. There is no edge selection. Use the input latch (0x44/0x45) if you
//    cannot afford to miss a short pulse.
```

---

## 9. Pitfalls, ranked

1. **Burst-reading or burst-writing across register boundaries.** Registers toggle within pairs. §7.1. *This is the one that will cost you a day.*
2. **Accessing the SD card without calling `sdCardInit()`.** Power is off after `begin()`. §5.2.
3. **Setting a pin to OUTPUT and then LOW.** Glitches high, because the output latch defaults to `0xFF`. Write the output register first. §4.3.
4. **Expecting rising- or falling-edge-only interrupts.** The hardware has no edge selection. §4.1.
5. **Wondering why nothing interrupts.** Interrupt masks default to all-masked. §6.1.
6. **Forgetting `INT` needs an external pull-up.** Open-drain. §4.1.
7. **Reading `P0_6`/`P0_7` without enabling an internal pull-up.** No external one exists. §7.2.
8. **Leaving an internal pull-up enabled on a pin held low before deep sleep.** ~1.1 mA. §3.3.
9. **Using `P1_0`, `P1_1` or `P1_2` as free GPIO.** They have board functions and are **not** in the library's blocked list. §5.5.
10. **Using `P1_3` on a ZeroWriter Ink.** It is the power LED there. §5.4.
11. **Assuming a soft reset preserves expander state.** `RESET` is tied to `EN`. §4.2.
12. **Assuming a brown-out re-runs POR.** `VDD(P)` must fall below `VPOR` (~1.1–1.4 V) and rise again. §3.4.
13. **Summing port currents past 160 mA on `VDD(P)`.** §3.2.
14. **Running the bus above 400 kHz.** §1.
15. **Applying MCP23017 knowledge.** Different register map, different addressing, different interrupt configuration (no `IOCON`, no polarity/mirror control). §1.2.
16. **Assuming `L16A` means QFN.** It also marks the BGA. §1.1.

---

## 10. Alternatives and equivalents

| Part | Relationship | Drop-in for `U9`/`U10`? |
|---|---|---|
| **`PCAL6416APW`** | Same die, **TSSOP24** | ⚠ Electrically identical, **different footprint** |
| **`PCAL6416AEV` / `AEX1`** | Same die, VFBGA24 / X2QFN24 | ⚠ Same |
| **`PCAL6416AHF,128`** | The fitted orderable | ✅ |
| **`PCA6416A`** | **NXP's own predecessor.** NXP states the PCAL6416A is a *"pin-to-pin replacement for the PCA6416A, with additional Agile I/O features"* and is *"software backward compatible… with interrupts disabled at power-up"* **[WEB]** | ✅ **The one genuine drop-in.** Going *from* PCAL *to* PCA loses every Agile I/O register — including the internal pull-up the driver needs on `P0_6` (§7.2) |
| **`PCA9555`** / `PCA9555A` | The classic ancestor of the whole line. Same address scheme, same `0x00`–`0x07` map | ⚠ **Register-compatible for the basic four pairs only.** No Agile I/O, no separate `VDD(I2C-bus)`, higher quiescent current. Footprint differs |
| **`TCA6416A`** (TI) | Direct functional competitor to the PCA9555 | ⚠ Same basic map; **no Agile I/O**; TI's own `TCAL6416` is the Agile-equivalent |
| **`TCAL6416`** (TI) | TI's answer to the PCAL6416A, with the same extended-register concept | ⚠ Similar but **verify the extended register addresses before assuming compatibility** |
| **`PCAL6408A`** | 8-bit sibling, same Agile I/O feature set | ❌ Half the pins |
| **`MCP23017`** (Microchip) | What older blue Inkplates fit | ❌ **28-pin SSOP, entirely different register map, linear auto-increment, `IOCON` interrupt configuration.** The library keeps two separate drivers for exactly this reason. §1.2 |
| **`MCP23S17`** | SPI version of the above | ❌ Different bus |

**Practical position:** for an Inkplate respin, fit a `PCAL6416AHF`. For a *new* design, the PCAL6416A remains a strong default — the dual supply and the per-pin pull-up/pull-down and latch registers routinely remove external parts. **[INF]**

---

## 11. Open questions

| Question | Status |
|---|---|
| On real hardware, do `P0_6`/`P0_7` end up configured as outputs after `Inkplate::begin()` (§7.1)? | **Open.** One `readReg(0x06)` on a live board settles it. **This is the highest-value single measurement in this record** |
| Has the 23-byte burst read ever been reported upstream? | **Open.** No issue found in a 2026-08-24 search of the Inkplate-Arduino-library repository — a search negative |
| Are the solder jumpers `JP5`/`JP6` (Gen 1) and `JP7`/`JP8` (Gen 2 / ZeroWriter) shipped bridged to the expander side by default? | **Open.** The KiCad netlist shows the connection but not the default bridge state; needs a board photo or a continuity check |
| Do any Inkplate 5 units ship with an MCP23017 due to the chip-shortage substitution Soldered mentions for other models? | **Open.** Soldered's docs note the substitution for *"some Inkplates"* **[COM]** but the Inkplate 5 BOM and its board define (`ARDUINO_INKPLATE5` → `pcalExpander.h`) both say PCAL. §1.2 |
| Does the ZeroWriter firmware drive `P1_3` (`PWR_LED`) itself, or is it left to the stock library? | **Open.** ZeroWriter Ink ships pre-built firmware binaries; the application source is not in the public repository |

---

## Manufacturer

**NXP Semiconductors** — see the [NXP documentation-sourcing guide](../../../vendors/nxp/README.md) for NXP's document portals and URL patterns.

> ⚠ **Retrieval note, 2026-08-24 — and a correction to our own first attempt.** `nxp.com` has an **inverted User-Agent block**: it serves a modern *browser* UA a 745-byte `<title>Page not available</title>` placeholder with **HTTP 404**, and serves **curl's default UA** the real content with **HTTP 200**. This is already documented in the [NXP vendor guide §5/§7](../../../vendors/nxp/README.md).
>
> In this research pass the datasheet was fetched **without** `-A` and succeeded first time; the product pages were then tried **with** a Chrome UA and all "404'd". That was our error, not NXP's behaviour. Re-probed with the default UA on 2026-08-24, **every** URL works:
>
> | URL | Browser UA | Default `curl` UA |
> |---|---|---|
> | `/docs/en/data-sheet/PCAL6416A.pdf` (GET) | — | **200**, 868,663 B, `%PDF` ✅ |
> | `/docs/en/data-sheet/PCAL6416A.pdf` (**HEAD**) | 404 | **200** ✅ |
> | `/part/PCAL6416AHF` | 404 | **200**, 59,823 B ✅ |
> | `/products/PCAL6416A` | 404 | **200**, 247,145 B ✅ |
> | `https://www.nxp.com/` | 404 | **200** ✅ |
>
> **Rule for this vendor: do not set a User-Agent.** Contrary to the usual habit. Recorded in [`../../../component-download-failures.txt`](../../../component-download-failures.txt) and the [crawler access table](../../../ai-crawler-site-access-table.md).

## Used By

| Device | Designator | Address | Notes |
|---|---|---|---|
| [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) | **`U9`** | `0x20` | `P1_0` drives a **DNP** MOSFET (§5.3) |
| [Soldered Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) | **`U10`** | `0x20` | Identical net-for-net to Gen 1 |
| [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md) | **`U10`** | `0x20` | **`P1_3` repurposed as `PWR_LED`** (§5.4); everything else unchanged |

## Related components

- [Texas Instruments TPS65186](../../texas-instruments/tps65186/README.md) — five of this expander's sixteen pins are its control and status lines. Documents the same interface from the PMIC side
- [E Ink ED052TC4 / ED052TC2](../../e-ink/ed052tc4/README.md) — `P0_0`–`P0_2` are three of its timing inputs

---

## 12. Local artifacts and sources

### Artifacts held

| Document | Revision | Date | Local path | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| PCAL6416A product data sheet | **Rev. 7.1** | 30 August 2022 | `artifacts/pcal6416a-datasheet-rev7.1.pdf` | 868,663 | `abe25cb2f38fb3a3c77c6aa80fdaf50928007bda3794671753ee84f55fb5eff1` |

Validated 2026-08-24: `%PDF-1.4` magic; 56 pages; `pdfinfo` author **NXP B.V.**, title *"PCAL6416A - Low-voltage translating 16-bit I2C-bus/SMBus I/O expander with…"*, produced by Apache FOP 2.6 from the DITA Open Toolkit.

#### Reacquire

```bash
# Works only as a GET. HEAD on the same URL returns 404. See the retrieval note above.
curl -L -o pcal6416a.pdf https://www.nxp.com/docs/en/data-sheet/PCAL6416A.pdf
```

### Design files read

| File | What it established |
|---|---|
| `devices/soldered-electronics/inkplate-5/artifacts/hardware/soldered-inkplate-5-hardware-design/CAD/V1.2.0/Soldered Inkplate 5.kicad_pcb` | Complete `U9` 25-pad netlist; `Q10`/`R40` SD switch; `Q1`/`R19` DNP; `RST` net membership |
| `.../CAD/V1.2.0/CTRL & COMS.kicad_sch` | `Q1` = DNP, `R19` = DNP, `R47` = 10 k |
| `.../CAD/V1.2.0/SD & RTC.kicad_sch` | `Q10` = PMOS, `R40` = 100 k |
| `.../CAD/V1.2.0/MCU.kicad_sch` | `R47` 10 k, `U10` = ESP32-WROVER |
| `devices/soldered-electronics/inkplate-5-gen2/.../CAD/V1.1.0/Soldered Inkplate 5 Gen2.kicad_pcb` | `U10` netlist identical to Gen 1's `U9` |
| `devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter_ink/design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/Zerowriter Inkplate 5 Gen2.kicad_pcb` | `P1_3 → PWR_LED`; `JP7` SD jumper; `K1` inter-board link |

### Source files read

Under `devices/soldered-electronics/inkplate-5/artifacts/source-snapshots/`:

| File | Lines cited |
|---|---|
| `Inkplate-Arduino-library/library.properties` | version **11.1.4** |
| `Inkplate-Arduino-library/src/system/ExpanderSelect.h` | 4–8 (MCP vs PCAL selection) |
| `Inkplate-Arduino-library/src/system/pcalExpander/pcalExpander.h` | 25–47 (register addresses), 75–90 (pin names), 95–146 (API) |
| `Inkplate-Arduino-library/src/system/pcalExpander/pcalExpander.cpp` | 29–42 `begin()`, **49–61 `readPCALRegisters()`**, 109–120 `updatePCALAllRegisters()`, 151–201 blocked-pin gates, 203–214 `setIntPin()` doc comment, 274–297 `blockPinUsage()`, 310–362 `pinModeInternal()`, **373–374 `digitalWriteInternal()` input guard**, 414–441 `setIntPinInternal()`, 469–475 `getINTInternal()`, 518–526 `checkForBlockedPins()` |
| `Inkplate-Arduino-library/src/system/mcpExpander/mcpExpander.cpp` | **58 (sequential-read comment), 87–96 `readMCPRegisters()`** — the origin of §7.1 |
| `Inkplate-Arduino-library/src/system/defines.h` | 74 (`GPIO0_ENABLE 8`) |
| `Inkplate-Arduino-library/src/boards/Inkplate5/pins.h` | 7–57 (address and pin defines) |
| `Inkplate-Arduino-library/src/boards/Inkplate5V2/Inkplate5V2Driver.cpp` | 116 `blockGpioPins()` call, 624–640 `pinsAsOutputs()`, 692–712 `pinsZstate()`, 801–850 `gpioInit()`, 888–912 SD power, 1072 `pinMode(6, INPUT_PULLUP)`, 1195–1203 `blockGpioPins()` |
| `Inkplate-micropython/shared/drivers/pcal6416a.py` | 5–52 (constants), **84–106 (per-register reads)**, 120–160 (`pin_mode`) |
| `Inkplate-micropython/boards/inkplate5/inkplate5.py` | 84–140 (all 16 pin names) |

### Authoritative sources

| ID | Title | Class | URL | Retrieved | Version | Establishes | Local artifact |
|---|---|---|---|---|---|---|---|
| S1 | **NXP PCAL6416A product data sheet** — §5 pinning, §6 voltage translation, §7 functional description, §7.4 register descriptions, §8 bus transactions, §10–§13 electricals | primary | https://www.nxp.com/docs/en/data-sheet/PCAL6416A.pdf | 2026-08-24 | **Rev. 7.1**, 30 Aug 2022 | Everything marked **[DOC]** | `artifacts/pcal6416a-datasheet-rev7.1.pdf` |
| S2 | **NXP PCAL6416A product page** | primary | https://www.nxp.com/products/PCAL6416A | 2026-08-24 | live | Lifecycle **Active**; **Product Longevity Program, min. 10 years**; **pin-to-pin replacement for PCA6416A**; 5 V-tolerant ports; ESD 2 kV HBM / 1 kV CDM; latch-up > 100 mA JESD78 Class II; Schmitt-trigger hysteresis figures; full Agile I/O feature list | – |
| S2b | NXP part page | primary | https://www.nxp.com/part/PCAL6416AHF | 2026-08-24 | live | Orderable-part confirmation | – |
| S2c | **UA-inversion probe** (corrects our own first attempt) | probe | `nxp.com/`, `/part/PCAL6416AHF`, `/products/PCAL6416A`, `/docs/en/data-sheet/PCAL6416A.pdf` (GET **and** HEAD) | 2026-08-24 | — | **All four 404 with a Chrome-131 UA and 200 with curl's default UA**, including HEAD. Confirms the inversion already recorded in the [NXP vendor guide](../../../vendors/nxp/README.md) | – |
| S3 | Inkplate Arduino library | primary | https://github.com/SolderedElectronics/Inkplate-Arduino-library | 2026-08-24 | **v11.1.4** | All **[SRC]** (Arduino), including §7.1 | snapshot, §12 |
| S4 | Inkplate MicroPython library | primary | https://github.com/SolderedElectronics/Inkplate-micropython | 2026-08-24 | snapshot | Per-register reads (§7.1); the full 16-pin name map (§5.1) | snapshot, §12 |
| S5 | Soldered Inkplate 5 hardware design (TAPR OHL) | primary | https://github.com/SolderedElectronics/Soldered-Inkplate-5-hardware-design | 2026-08-24 | **V1.2.0** | All **[SCH]** for Inkplate 5 | local |
| S6 | Soldered Inkplate 5 Gen2 hardware design | primary | https://github.com/SolderedElectronics/Soldered-Inkplate-5-Gen2-hardware-design | 2026-08-24 | **V1.1.0** | All **[SCH]** for Gen 2 | local |
| S7 | ZeroWriter Ink design files | primary | https://github.com/zerowriter/zerowriter_ink | 2026-08-24 | **v1.2.0** | `P1_3 → PWR_LED` | local |
| S8 | Inkplate documentation — *IO Expander Functions* | secondary | https://docs.soldered.com/inkplate/ | 2026-08-24 | live | MCP-vs-PCAL identification by package; the "do not use unavailable pins" warning; per-model available-pin table | `devices/soldered-electronics/inkplate-5/artifacts/docs/Inkplate-documentation/source/arduino.rst:2242-2300` |

> **Negative results, 2026-08-24.** No Espressif `esp_io_expander` component for the PCAL6416A was found in the ESP Component Registry (§8.3). No upstream issue about the 23-byte burst read was found in the Inkplate-Arduino-library repository (§11). Both are search negatives, not proof of absence.
