# Cardputer ADV — pinouts and buses

> Snapshot **2026-09-04**. Evidence classes used below:
> **[SCH]** read off a rendered sheet of `Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf`;
> **[SRC]** vendor board-support source at a pinned commit;
> **[DOC]** the `docs.m5stack.com/en/core/Cardputer-Adv` PinMap tables;
> **[INF]** inferred, with the reasoning stated.
> Where **[DOC]** and **[SCH]**/**[SRC]** disagree, the disagreement is stated, not resolved silently.

## 1. Complete GPIO map

The ESP32-S3FN8 sits inside the Stamp-S3A; every pin below is a module castellation as well as
an SoC GPIO. "Free on ADV" means the pin is not consumed by an on-board function and is
brought out to the CAP header.

| GPIO | Function on ADV | Direction | Bus / role | Shared with | Evidence |
|---|---|---|---|---|---|
| **G0** | BOOT / user button on the Stamp | in, pull-up 10 k | strap | — | [SRC] `M5Unified.cpp:3485` reads `!gpio_in(GPIO_NUM_0)` |
| **G1** | Grove / PORT.A **SCL** | I/O | external I²C | Grove white wire | [SRC] `_pin_table_i2c_ex_in` → EX SCL = G1 · ⚠ see §5 |
| **G2** | Grove / PORT.A **SDA** | I/O | external I²C | Grove yellow wire | [SRC] same → EX SDA = G2 |
| **G3** | CAP `RESET` | out | CAP pin | *was 74HC138 sense line on v1.x* | [SCH] sheet 4, net `G3` at P3-1 |
| **G4** | CAP `INT` / `IRQ` | in | CAP pin | *was keyboard sense* | [SCH] P3-2 |
| **G5** | CAP `CS` | out | SPI CS | *was keyboard sense* | [SCH] P3-7 |
| **G6** | CAP `BUSY` | in | CAP pin | *was keyboard sense* | [SCH] P3-3 |
| **G7** | **Internal display FPC** | — | — | — | [SRC] M5GFX comment: G7 = "Internal FPC" on ADV |
| **G8** | **Internal I²C SDA** | I/O | I²C, 3.3 k pull-up R37 | TCA8418, ES8311, BMI270, **CAP pin 11** | [SCH] sheet 2/3, [SRC] `_pin_table_i2c_ex_in` |
| **G9** | **Internal I²C SCL** | I/O | I²C, 3.3 k pull-up R36 | same | same |
| **G10** | Battery ADC | in, analog | ADC1 | — | [DOC], [SRC] Bruce `ANALOG_BAT_PIN=10` |
| **G11** | TCA8418 `INT` | in, 3.3 k pull-up R35 | keypad IRQ | — | [SCH] U9-24, [SRC] `TCA8418.cpp:13` |
| **G12** | microSD `CS` | out | SPI CS | — | [SRC] `_pin_table_sd` |
| **G13** | CAP **UART TX** | out | UART | *was keyboard sense* | [SCH] net at P3, labelled `GPS-RX` · see §4 |
| **G14** | SPI `MOSI` | out | SPI | microSD **and** CAP | [SRC] `_pin_table_sd`, [SCH] P3 |
| **G15** | CAP **UART RX** | in | UART | *was keyboard sense* | [SCH] labelled `GPS-TX` · see §4 |
| **G21** | WS2812 RGB LED data | out | RMT | on the Stamp | [SRC] `M5Unified.cpp:249` |
| **G33** | LCD `RST` | out | — | — | [SRC] M5GFX `cfg.pin_rst` |
| **G34** | LCD `DC`/`RS` | out | SPI | — | [SRC] `bus_cfg.pin_dc` |
| **G35** | LCD `MOSI` | out | **separate SPI** | — | [SRC] `bus_cfg.pin_mosi` |
| **G36** | LCD `SCK` | out | **separate SPI** | — | [SRC] `bus_cfg.pin_sclk` |
| **G37** | LCD `CS` | out | SPI CS | — | [SRC] `cfg.pin_cs` |
| **G38** | LCD backlight PWM **and** `BL_3V3` rail enable | out | LEDC ch7 | **WS2812 supply** | [SRC] `_set_pwm_backlight(GPIO_NUM_38, 7, 256, false, 16)`; [SCH] Stamp-S3A U2 `EN` |
| **G39** | SPI `MISO` | in | SPI | microSD **and** CAP | [SRC], [SCH] |
| **G40** | SPI `SCK` | out | SPI | microSD **and** CAP | [SRC], [SCH] |
| **G41** | I²S `BCLK` / ES8311 `SCLK` | out | I2S_NUM_1 | — | [SRC] `spk_cfg.pin_bck`, `mic_cfg.pin_bck` |
| **G42** | I²S `DOUT` / ES8311 `DSDIN` | out | I2S_NUM_1 | — | [SRC] `spk_cfg.pin_data_out` |
| **G43** | I²S `LRCK` / ES8311 `LRCK` | out | I2S_NUM_1 | — | [SRC] `spk_cfg.pin_ws`, `mic_cfg.pin_ws` |
| **G44** | IR emitter TX | out | RMT | — | [DOC], [SRC] UserDemo `HAL_PIN_IR_TX 44` |
| **G45** | *unused on ADV* | — | — | — | Meshtastic sets `DAC_I2S_MCLK 45 // dummy` |
| **G46** | I²S `DIN` / ES8311 `ASDOUT` | in | I2S_NUM_1 | — | [SRC] `mic_cfg.pin_data_in` |

Pins **G16–G20, G22–G32, G47, G48** are not brought out on the Stamp-S3 24-pin footprint and
are unavailable.

### 1.1 What the ADV freed and spent, versus v1.x

| Pin | v1.0 / v1.1 | ADV |
|---|---|---|
| G3, G4, G5, G6, G7, G13, G15 | keyboard **sense** lines (`input_list = {13,15,3,4,5,6,7}`) | G7 → display FPC; the other six → CAP header |
| G8, G9, G11 | 74HC138 address lines `A0/A1/A2` (`output_list = {8,9,11}`) | G8/G9 → internal I²C; G11 → TCA8418 `INT` |

Both lists are literal, from
[`IOMatrix.h:29-30`](https://github.com/m5stack/M5Cardputer/blob/f1392858b9994c3547120e602a57d3553d16ab01/src/utility/Keyboard/KeyboardReader/IOMatrix.h#L29-L30):

```cpp
const std::vector<int> output_list = {8, 9, 11};
const std::vector<int> input_list  = {13, 15, 3, 4, 5, 6, 7};
```

Net gain: **fifteen pins used by the keyboard become three.**

---

## 2. Buses

### 2.1 SPI — two independent buses

| Bus | Host | SCK | MOSI | MISO | Devices | Notes |
|---|---|---|---|---|---|---|
| Display | `SPI3_HOST` | G36 | G35 | — | ST7789V2 (CS G37) | M5GFX sets `spi_3wire = true` and `pin_miso = -1`; 40 MHz write, 16 MHz read |
| Peripheral | (user's choice) | **G40** | **G14** | **G39** | microSD (CS G12), **CAP board (CS G5)** | shared — see [`resources-and-conflicts.md`](resources-and-conflicts.md) |

The display bus is genuinely separate silicon-side; the *peripheral* bus is the contended one.

### 2.2 I²C

| Bus | SDA | SCL | Pull-ups | Devices |
|---|---|---|---|---|
| **Internal** (`M5.In_I2C`) | **G8** | **G9** | R37 / R36, 3.3 kΩ to +3V3 | `0x34` TCA8418 · `0x18` ES8311 · `0x69` BMI270 · **plus whatever a CAP board adds** |
| **External** (`M5.Ex_I2C`, PORT.A) | G2 | G1 | on the Grove peripheral | user devices |

Address `0x69` for the BMI270 is printed on the schematic itself — sheet 3 carries the text
**"7-bit Address 69H"** beside U7, and R43 (3.3 kΩ) pulls `SDO` high to select it. `0x18` for
the ES8311 is `es8311_i2c_addr0` in
[`M5Unified.cpp:513`](https://github.com/m5stack/M5Unified/blob/8530f5377d782e4a25a6c482de2e71c3f75ca8eb/src/M5Unified.cpp#L513).
`0x34` for the TCA8418 is Bruce's `-DTCA8418_I2C_ADDR=0x34` and Adafruit's library default.

> **Community documentation error, recorded.** `bmorcelli/Launcher`'s `CardputerADV.md` lists
> "**0x18**: Likely accelerometer/IMU" and "**0x69**: Likely additional sensor". Both are
> inverted: `0x18` is the ES8311 codec and `0x69` is the BMI270. Harmless in that file, but it
> is the kind of thing that propagates.

### 2.3 I²S — one port, two directions, one codec

`I2S_NUM_1`, ESP32-S3 as **master**, ES8311 as slave:

| Signal | GPIO | ES8311 pin |
|---|---|---|
| `BCLK` | G41 | 6 `SCLK/DMIC_SCL` |
| `LRCK` / WS | G43 | 8 `LRCK` |
| `DOUT` (to codec DAC) | G42 | 9 `DSDIN` |
| `DIN` (from codec ADC) | G46 | 7 `ASDOUT` |
| `MCLK` | **not wired** | — |

There is no MCLK line. M5Unified's ADV callbacks therefore program the ES8311 with
`0x01 = 0xB5` or `0xBA` — "MCLK = BCLK" — and `0x02 = 0x18` (`MULT_PRE = 3`). Meshtastic
declares `DAC_I2S_MCLK 45 // dummy` for the same reason. Any driver you write must select
BCLK-as-MCLK or the codec will not clock.

The **speaker path and the microphone path share this one port and this one codec**, and
M5Unified's two enable callbacks write *different* values to register `0x01`. See the driver
audit in [`features/audio.md`](features/audio.md); this is a real defect, not a nit.

### 2.4 Timers, RMT, LEDC, ADC

| Resource | Consumer | Detail |
|---|---|---|
| LEDC channel **7** | LCD backlight | `_set_pwm_backlight(GPIO_NUM_38, 7, 256, false, 16)` — channel 7, 256 Hz, offset 16 |
| RMT | WS2812 (G21) and IR TX (G44) | two channels if both used simultaneously |
| ADC1 | battery sense on G10 | ADC1 also blocks nothing else here |
| I2S_NUM_1 | audio | I2S_NUM_0 is free |
| GPIO ISR | TCA8418 `INT` on G11 | `attachInterruptArg(..., CHANGE)` in the vendor reader |

---

## 3. Connectors

### 3.1 HY2.0-4P Grove / PORT.A (designator P1)

| Wire | Signal | GPIO |
|---|---|---|
| Black | GND | — |
| Red | +5V (from the `+5VOUT` boost rail) | — |
| Yellow | `G2` | GPIO2 |
| White | `G1` | GPIO1 |

> ⚠ **Conflict, unresolved.** M5Stack's PinMap simply names the pins `G2`/`G1` and calls the
> connector `PORT.CUSTOM`. M5Unified's `_pin_table_i2c_ex_in` row for `board_M5CardputerADV`
> reads `{ …, GPIO_NUM_1, GPIO_NUM_2 }` under the header comment `// In SCL,SDA, EX SCL,SDA`,
> i.e. **external SCL = G1, external SDA = G2**. The M5Stack Grove colour convention normally
> puts **SCL on yellow** — which would make G2 the clock and contradict the library. The
> schematic labels the connector `HY-2.0_IIC` with nets `IIC_SCL` and `IIC_SDA` present on the
> sheet, but the two labels could not be resolved to individual pins from the text layer at the
> band width used.
> **Use the library values** (`M5.Ex_I2C`, SCL = G1, SDA = G2): they are what every M5 library
> will do at runtime regardless of the colour convention. Recorded in
> [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

### 3.2 EXT 2.54-14P "CAP" header (designator P3, footprint `HDR-SMD_14P-P2.54`)

Full treatment, including the three numbering schemes, is in
[`features/cap-header.md`](features/cap-header.md). The physical table, by row and position —
which is unambiguous and does not depend on whose numbering you use:

| Row L, position (top→bottom) | Signal | GPIO | | Row R, position (top→bottom) | Signal | GPIO |
|---|---|---|---|---|---|---|
| L1 | `RESET` | G3 | | R1 | `5VIN` | — |
| L2 | `INT` | G4 | | R2 | `GND` | — |
| L3 | `BUSY` | G6 | | R3 | `5VOUT` | — |
| L4 | `SCK` | G40 | | R4 | `I2C_SDA` | G8 |
| L5 | `MOSI` | G14 | | R5 | `I2C_SCL` | G9 |
| L6 | `MISO` | G39 | | R6 | `UART_TX` (`GPS-RX`) | **G13** |
| L7 | `CS` | G5 | | R7 | `UART_RX` (`GPS-TX`) | **G15** |

Read directly off sheet 4 of the ADV schematic; the net labels `G3, G4, G6, G40, G14, G39, G5`
and `+5VIN, GND, +5VOUT, G8, G9, G13, G15` sit against the corresponding pins, and the symbol's
own pin names are `RESET, INT, BUSY, SCK, MOSI, MISO, CS` / `5VIN, GND, 5VOUT, SDA, SCL,
GPS-RX, GPS-TX`.

### 3.3 Display FPC (designator FPC1, `FPC-8P-0.5`)

An 8-pin 0.5 mm flat-flex from the front panel to the display. G7 is described by M5GFX as
"Internal FPC" on the ADV. The individual FPC conductors were not traced; the SPI signals
(G33–G37) reach the panel through it. M5Stack warns that lifting the Stamp module without
supporting this cable damages the socket.

---

## 4. The UART direction question, settled

M5Stack's own documentation contradicts itself. The resolution matters because getting it
wrong means a GPS or a serial CAP board that simply never answers.

| Source | Pin 12 / R6 (`G13`) | Pin 14 / R7 (`G15`) |
|---|---|---|
| `docs.m5stack.com/en/core/Cardputer-Adv`, EXT table | `UART_TX` | `UART_RX` |
| `…/core/Cardputer_Mesh_Kit`, **EXT table** | `UART_RX` | `UART_TX` |
| `…/core/Cardputer_Mesh_Kit`, **Cap-Bus table** | → `GPS-RX` | → `GPS-TX` |
| **ADV schematic sheet 4**, symbol pin names | `GPS-RX` | `GPS-TX` |
| **`M5Cardputer-UserDemo` @ `b549eac0`** | `HAL_PIN_GPS_TX GPIO_NUM_13` | `HAL_PIN_GPS_RX GPIO_NUM_15` |
| **Meshtastic `variant.h`** | `GPS_TX_PIN 13` | `GPS_RX_PIN 15` |

The decisive evidence is the factory firmware's actual call, in
`main/hal/cap_lora868/uart/uart_helper.c:71`:

```c
#define ECHO_TEST_TXD (HAL_PIN_GPS_TX)   /* = GPIO_NUM_13 */
#define ECHO_TEST_RXD (HAL_PIN_GPS_RX)   /* = GPIO_NUM_15 */
ESP_ERROR_CHECK(uart_set_pin(ECHO_UART_PORT_NUM, ECHO_TEST_TXD, ECHO_TEST_RXD, …));
```

`uart_set_pin(port, tx_io_num, rx_io_num, …)` — so **GPIO 13 is the ESP32-S3's TX and GPIO 15
is its RX**, host-centric. The schematic's peripheral-centric labels agree: pin `GPS-RX`
carries G13, i.e. G13 feeds the GPS receiver.

**Conclusion: G13 = TX (out), G15 = RX (in). The Cardputer Mesh Kit page's EXT table is
wrong**, and is contradicted by its own Cap-Bus table two rows further down.

---

## 5. Boot straps and reset behaviour

| Pin | Strap role | ADV wiring | Risk |
|---|---|---|---|
| G0 | boot mode | Stamp user button, 10 kΩ pull-up | download mode = **switch OFF → hold G0 → apply power → release** |
| G3 | JTAG source select (ESP32-S3) | **CAP `RESET`, no pull resistor on the host side** | ⚠ a CAP board or breadboard wire that holds G3 at a defined level during reset changes the JTAG source strap. Not observed to break anything, but worth knowing before you debug a mysterious boot difference with a CAP fitted. |
| G45 | VDD_SPI voltage | not brought out | — |
| G46 | boot log / strap | **ES8311 `ASDOUT`** | the codec is high-Z until enabled, so this is benign in practice; noted because G46 is a strap pin and the schematic shows it driven by an IC |

The **CN809J** (U3) watches `VBAT_IN` and generates a reset. R7 (100 kΩ) pulls its `RESET`
output line down. There is **no reset button** on the ADV — M5Stack's v1.1 spec table lists
"1 × Reset button + 1 × User button", the ADV table lists neither, and the ADV designator
census on sheet 1 finds exactly two switches (`BTN1`, `BTN2`) and two slide switches
(`SW1`, `SW2`).

---

## 6. Power rails

| Rail | Source | Notes |
|---|---|---|
| `VBAT_IN` / `VBAT_OUT` | 1750 mAh cell via Q1/Q2/Q3 LP3218DT1G power path | `BAT+` / `BAT-` at J8 |
| `+5VIN` | USB-C VBUS on the Stamp, through a 6 V/1 A PPTC (F1) | also CAP `5VIN` |
| `+5VOUT` | **SY7088** boost from `VBAT_OUT`, FB 75 k/22 k → **≈ 5.29 V [INF]** | Grove red wire, CAP `5VOUT` |
| `+3.3V` | **SY8089** buck, FB 68 k/15 k | everything logic |
| `VDD_3V3` (Stamp) | **JW5712** buck on Stamp-S3A, 0–0.6 A | SoC |
| `BL_3V3` (Stamp) | **AW35122FDR** load switch, `EN` = `DISP_BL` = **G38** | LCD backlight **+ WS2812** |

The sheet prints its own formula, `Vout = 1.2 V × (R1/R2 + 1)`, which is what the inferred
boost figure is computed from. Nothing here has been measured.

---

# 2026-09-07 — additions and corrections from schematic net tracing

Appended beneath the existing tables; **nothing above is altered, reworded or reordered.** Where
a row below contradicts one above, the row below is the correction and the reason is given. Full
trace with coordinates: [`schematic-netlist.md`](schematic-netlist.md). Method:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).
All corrections are indexed in
[`guides/reverse-engineering/schematic-tracing-corrections-2026-09-07.md`](../../../guides/reverse-engineering/schematic-tracing-corrections-2026-09-07.md).

## Grove / `PORT.CUSTOM` (`J2`, `HY-2.0_IIC`) — now established from the sheet

| `J2` pin | Signal | GPIO | Evidence |
|---|---|---|---|
| 1 | `IIC_SCL` | **GPIO1** | net label `GI` @ 737.32, 366.41 → module pin `P1.1`, printed pin name `G1` |
| 2 | `IIC_SDA` | **GPIO2** | net label `GO` @ 738.58, 373.60 → module pin `P1.2`, printed pin name `G2` |
| 3 | `VCC` | — | 5 V; ESD `D8` `PESDNC2FD5VB` |
| 4 | `GND` | — | ESD `D6`/`D7` `PESDNC2FD3V3B` on the two signals |

Pull-ups `R3`, `R10`, both 10 kΩ. The net *names* on the sheet are the literal strings `GI`/`GO`
(letter I, letter O) — a vendor typo — which is why searching for "G1"/"G2" near `J2` finds
nothing. Verified with a 300 dpi crop.

## Internal I²C bus

| Device | Address | SDA | SCL | Evidence |
|---|---|---|---|---|
| `U7` BMI270 | `0x69` | **G8** (pin 14 `SDX`) | **G9** (pin 13 `SCX`) | `NLG8` @ 109.50, 142.20 · `NLG9` @ 109.50, 149.20; sheet prints `7-bit Address 69H` @ 196.71, 114.51; `SDO` (pin 1) strapped high by `R43` 3.3 kΩ |
| `U9` TCA8418RTWR | `0x34` | **G8** (pin 22) | **G9** (pin 23) | `NLG8` @ 77.00, 239.20 · `NLG9` @ 77.00, 232.20; sheet prints `7-bit Address 34H` @ 106–142, 312.5 |

Bus pull-ups: `R35`, `R36`, `R37`, all 3.3 kΩ, at x = 48.5 / 59.5 / 70.5 spanning y 184.57→206.57
on sheet 2 — one each for `SDA`, `SCL` and `INT`.

## Interrupts

| Line | GPIO | Evidence |
|---|---|---|
| TCA8418 `INT` (`U9` pin 24) | **G11** | `NLG11` @ 78.50, 224.66; open-drain, pulled up by `R37` 3.3 kΩ. Matches `DEFAULT_TCA8418_INT_PIN 11` in `M5Cardputer/src/utility/Keyboard/KeyboardReader/TCA8418.cpp:13` |
| BMI270 `INT1` (`U7` pin 4) | **none — not routed** | a full-sheet row query at y 167.37 returns only `U7`'s own tokens |
| BMI270 `INT2` (`U7` pin 9) | **none — not routed** | same, at y 174.37 |

**IMU motion-wake from deep sleep is unavailable on this board.**

## Keyboard matrix (`U9` TCA8418RTWR, sheet 2)

7 rows × 8 columns = 56 keys.

| `U9` pin | Name | Net |
|---|---|---|
| 1 | `ROW7` | **unconnected** — `PIU901` @ 164.00, 206.91, no label, no aligned peer |
| 2–8 | `ROW6`…`ROW0` | `ROW6`…`ROW0` (`NLROW0`…`NLROW6`, x 184.50, y 152.66–196.20) |
| 9–16 | `COL0`…`COL7` | `Y7`…`Y0`, each through a 22 R/1 % series resistor `R27`…`R34` |
| 20 | `RESET` | `R38` 10 kΩ pull-up (`PIR382` @ 81.00, 264.37) |
| 25 | `EP` | `GND` |

## Power rails — corrected figures

| Rail | Converter | Divider | Computed | Note |
|---|---|---|---|---|
| `+3.3V` | `U4` SY8089 buck, `L2` 4.7 µH `3015` | **`R11` 68 kΩ / `R13` 15 kΩ** | 3.3 V with a **0.6 V** feedback reference | ⚠ **correction:** the earlier reading of `R12` 68 kΩ was wrong — `R12` is 100 kΩ and sits 460 pt away at (236.50, 221.20), unrelated to this network |
| `+5VOUT` | `U2` SY7088 boost, `L1` 1.5 µH `3015`, `D2` `SS34` | `R4` 75 kΩ / `R6` 22 kΩ | **5.29 V** using the sheet's own printed `Vout=1.2V*(R1/R2+1)` @ (612.67, 157.65) | ⚠ **correction:** that printed formula belongs to `U2`, **not** to `U4` — it sits directly beneath the SY7088 |

The rail is designed high on purpose; the DinMeter's equivalent SY7088 rail computes to 5.38 V.

## Module footprint `P1`, sheet 1

| Pin | Printed pin name | Net |
|---|---|---|
| 1 | `G1` | `GI` → `J2.1 IIC_SCL` |
| 2 | `G2` | `GO` → `J2.2 IIC_SDA` |
| 3–9 | `G3`…`G9` | `G3`…`G9` |
| 10 | `G10` | `GND` |
| 11 | `G11` | `G11` → `U9.24 INT` |
| 12–13 | — | `+5VIN` (`NL05VIN`; Altium's `NL` tokens substitute `0` for `+`) |
| 14–15 | `G13` | `G13` |
| 16–17 | `G15` | `G15` |

## Named parts recovered from the sheets

`U1` `TP4057` · `U2` `SY7088` · `U3` supervisor · `U4` `SY8089` · `U5` audio amplifier
(`INP`/`INN`, sheet 3) · `U6` codec (`CCLK`/`MCLK`, sheet 3) · `U7` `BMI270` ·
`U8` `MSM381A3729H9BPC` PDM microphone (sheet 3) · `U9` `TCA8418RTWR` ·
`Q1`/`Q2`/`Q3` `LP3218DT1G` · `D6`/`D7` `PESDNC2FD3V3B` · `D8` `PESDNC2FD5VB` ·
`FB7` 120 Ω/MB ferrite on the BMI270 supply.
