# STMicroelectronics ST25R3916

> **Common guide:** [`guides/nfc`](../../../guides/nfc/README.md) — the device-independent NFC material (standards landscape, antenna matching and the Q trade-off, reader-silicon comparison, RFAL and library options, symptom-to-cause debugging). This record covers the part; that guide covers the domain.

- **Category:** high-performance 13.56 MHz **NFC reader/writer + card-emulation + peer-to-peer front end**, with an integrated framing engine, a 512-byte FIFO, and both SPI and I²C host interfaces
- **Exact part fitted on the PaperMono:** **`ST25R3916-AQWT`** — 32-pin VFQFPN 5 × 5 mm with wettable flanks, −40 °C to +105 °C grade, tape and reel
- **Host interface on this board:** **I²C at address `0x50`** (fixed, no address-select pin). The chip also has a **full SPI mode**; the PaperMono does not use it — see [§3](#3-host-interface--i²c-here-spi-elsewhere)
- **Protocols:** NFC-A / ISO14443A, NFC-B / ISO14443B, NFC-F / FeliCa™, NFC-V / ISO15693; EMVCo 3.0 analog and digital compliant
- **Research status:** the **full ST datasheet is retained** (`DS12484 Rev 8`, 160 pp) and was read; the **PaperMono NFC sub-board schematic sheet was parsed pin-by-pin**. No hardware was in the loop, and no tag has been read by anyone whose report could be located.
- **Retrieved:** 2026-09-01

The NFC front end of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153), where it sits on **its own sub-board** rather than the main PCB. **The [PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) does not have it** — NFC and LoRa are the entire difference between the two SKUs.

---

## Evidence labelling

| Marker | Meaning | Evidence status |
|---|---|---|
| **[DS]** | Stated in `artifacts/st25r3916-datasheet-m5stack-mirror.pdf` (`DS12484 Rev 8`), with section/table reference | `not-tested` — manufacturer specification reproduced; nothing measured |
| **[SCH]** | Read out of `PaperMono_SCH_V0.6.2_20260522.pdf`, **sheet 6** (`02 Paper Mono NFC.SchDoc` rev V0.2), cited as designator + pin | `executed-success` for the extraction (PDF text-position layer parsed, all 33 `U2` pads enumerated); `not-tested` electrically |
| **[SRC]** | Read out of M5Stack source at a cited `file:line` | `executed-success` for the read; `not-tested` on hardware |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference drawn from two or more of the above | `inferred` |

**Nothing here was verified electrically, and no register value or pin below was guessed.** Where the schematic's text layer gives only adjacency rather than connectivity, that is stated rather than upgraded to a net list — see [§5.2](#52-what-the-text-layer-can-and-cannot-establish).

**Text-layer validation.** `pdftotext -layout` output from the datasheet was checked against the document's own running headers (`ST25R3916/7`), footers (`DS12484 Rev 8`, `n/160`) and section numbering before any value was transcribed. No glyph subsetting or code-point offset was observed. The schematic's hidden Altium annotation layer does render underscores as `0`, a defect documented in the [Stamp-LoRa-1262 record §5-G7](../../m5stack/stamp-lora-1262/README.md); the **visible** net labels used here are unaffected.

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **STMicroelectronics** | **[DS]** cover |
| Marketing name | **ST25R3916** — "High performance NFC universal device and EMVCo reader" | **[DS]** cover |
| Sibling part in the same document | **ST25R3917** — a **reduced** feature set, see §1.1 | **[DS]** Table 1 |
| Document | **DS12484 Rev 8**, 160 pp, **08-May-2023**, "production data" | **[DS]** cover, p. 157 |
| Order code on this board | **`ST25R3916-AQWT`** | **[SCH]** sheet 6, value string beside `U2` |
| Decoded order code | `A` = −40 °C to +105 °C · `QW` = 32-pin **VFQFPN 5 × 5 mm, wettable flanks** · `T` = tape and reel, 4000/reel | **[DS]** §7 |
| Other packages offered | UFQFPN32 (`QE`, non-wettable flanks), **WLCSP36** (`WL`) | **[DS]** §7, Table 2 |
| I²C address | **`0x50`**, fixed — the datasheet states it flatly and offers no address-select mechanism | **[DS]** §4.3.4 first line; **[SRC]** `M5Unit-NFC/src/unit/unit_ST25R3916.hpp:40` (`DEFAULT_ADDRESS = 0x50`); **[SRC]** `M5PaperMono-UserDemo/main/hal/hal_board.cpp:21` |
| Reference crystal | **27.12 MHz** (2 × f<sub>c</sub>), fast start-up | **[DS]** Features, Table 121 note 1 |
| Crystal fitted on this board | **`XL7EL89CMI-111YLC`**, 27.12 MHz, with `C14`/`C15` **10 pF** load caps | **[SCH]** sheet 6 `X1` |
| Reference designator on PaperMono | **`U2`, sheet 6** — the NFC sub-board, *not* the main board | **[SCH]** |
| ⚠ Marking verified? | **No.** No teardown photograph of `U2` was inspected. The identification rests on the schematic's own value string, a primary vendor document but not a photograph of the top marking | **[INF]** |

### 1.1 ST25R3916 vs ST25R3917 — the fitted part is the *full* one

Both parts share one datasheet, and it is easy to attribute an ST25R3917 limitation to the wrong chip. **[DS]** Table 1:

| Feature | ST25R3916 | ST25R3917 |
|---|:--:|:--:|
| ISO14443 A/B, ISO15693, FeliCa™, NFC tag types 1–5 read | ✅ | ✅ |
| ISO18092 **passive initiator** | ✅ | ✅ |
| Inductive sensor wake-up | ✅ | ✅ |
| **ISO18092 passive target** | ✅ | ❌ |
| **ISO18092 active initiator and target** | ✅ | ❌ |
| **Automatic antenna tuning (AAT)** | ✅ | ❌ |
| **Card emulation** | ✅ | ❌ |
| **Capacitive sensor wake-up** | ✅ | ❌ |

The PaperMono fits the **ST25R3916**, so card emulation, AAT, peer-to-peer and the capacitive sensor are all *silicon* capabilities of this board. Whether the *board* can use them is a separate question — see [§9-C3](#9-caveats-and-gaps) and [§10](#10-used-by).

The ST25R3917 also drops four pins to `NC`, including `CSI` (pin 25) and both `AAT_A`/`AAT_B` (pins 18/19) **[DS]** Table 3. A driver written against a `3917` schematic will not exercise those.

---

## 2. Pin table

**[DS]** Table 2 (U/VFQFPN32 numbering; WLCSP36 ball in the second column). The PaperMono net column is **[SCH]** sheet 6 `U2` — all 33 pads (32 signal + thermal) were enumerated from the text-position layer.

| Pin | WLCSP | Name | Type | Datasheet description | PaperMono net **[SCH]** |
|---:|---|---|---|---|---|
| 1 | A6 | `VDD_IO` | P | Positive supply for peripheral communication | `VCC_3V3` |
| 2 | B6 | `CSO` | AO | Capacitive sensor output / test output 2 | *(no net label; local passive)* |
| 3 | C5 | `VDD_D` | AO | **Digital supply regulator output** | `VDD_D` (local, decoupled) |
| 4 | C6 | `XTO` | AO | Crystal oscillator output | `X1` |
| 5 | D6 | `XTI` | AI/DI | Crystal oscillator input | `X1` |
| 6 | D5 | `GND_D` | P | Digital ground | `GND` |
| 7 | E4 | `VDD_A` | AO | **Analog supply regulator output** | `VDD_A` (local) |
| 8 | E6 | `VDD` | P | External positive supply | `VCC_3V3` |
| 9 | F6 | `VDD_RF` | AO | Regulated driver supply for antenna drivers | `VDD_RF` (local) |
| 10 | E5 | `VDD_TX` | P | External positive supply for the TX part | `VCC_3V3` |
| 11 | F5 | `VDD_AM` | AO | Regulated driver supply for AM modulation | `VDD_AM` (local) |
| 12 | F4 | `GND_DR1` | P | Antenna driver ground | `GND` |
| 13 | F3 | **`RFO1`** | AO | **Antenna driver output** | matching network → `ANT1` |
| 14 | E3 | `VDD_DR` | P | Antenna driver positive supply input | local |
| 15 | F2 | **`RFO2`** | AO | **Antenna driver output** | matching network → `ANT1` |
| 16 | F1 | `GND_DR2` | P | Antenna driver ground | `GND` |
| 17 | E2 | `EXT_LM` | AO | External load-modulation MOS gate driver | *(local passive)* |
| 18 | E1 | `AAT_A` | AO | AAT tune voltage for variable capacitor A | *(see §5.3 — AAT branch appears unpopulated)* |
| 19 | D1 | `AAT_B` | AO | AAT tune voltage for variable capacitor B | *(idem)* |
| 20 | D2 | **`I2C_EN`** | DI | **I²C interface enable (VDD_D level)** | **`VCC_3V3` through `R4` = 0 Ω ⇒ I²C mode** |
| 21 | C1–C3 | `VSS` | P | Ground, die substrate | `GND` |
| 22 | B1 | `RFI1` | AI | Receiver input | `RFI_P` |
| 23 | B2 | `RFI2` | AI | Receiver input | `RFI_N` |
| 24 | A2 | `AGDC` | AIO | Analog reference voltage | `AGDC` (local) |
| 25 | A1 | `CSI` | AIO | Capacitive sensor input / test output 1 | *(see §5.3)* |
| 26 | A3, B3, B4 | `GND_A` | P | Analog ground | `GND` |
| 27 | A4 | **`IRQ`** | DO | **Interrupt request output, active high** | **`G6_RFID_INT`** → ESP32-S3 **GPIO6** |
| 28 | C4 | `MCU_CLK` | DO | Clock output for the MCU | *(no net label — unused)* |
| 29 | A5 | `BSS` | DI | SPI enable (active low) | *(no net label — unused in I²C mode)* |
| 30 | D3 | **`SCLK`** | DI | SPI clock / **I²C clock** | **`G48_SYS_SCL`** → ESP32-S3 **GPIO48** |
| 31 | D4 | `MOSI` | DI | SPI data input | *(no net label — unused in I²C mode)* |
| 32 | B5 | **`MISO`** | DO_T | SPI data output / **I²C data line** | **`G47_SYS_SDA`** → ESP32-S3 **GPIO47** |
| 33 | — | thermal pad | P | Exposed pad | `GND` |

> ⚠ **In I²C mode the data line is the pin called `MISO` and the clock is the pin called `SCLK`.** **[DS]** Table 12 names them `MISO (SDA)` and `SCLK (SCL)`. Reading the schematic symbol's pin *names* rather than its nets will suggest, wrongly, that the board is wired for SPI.

There is **no reset pin** on this device in any package. Everything that looks like a reset on the PaperMono is really a supply gate — see [§10.2](#102-pyb_nfc_en-and-pyb_rfid_rst-are-the-same-wire-and-it-is-a-rail-enable).

---

## 3. Host interface — I²C here, SPI elsewhere

### 3.1 The interface is chosen by a strap, and this board straps it to I²C

**[DS]** §4.3.2, in full:

> The active communication interface is selected via the `I2C_EN` pin. If this pin is pulled to GND, the ST25R3916/7 operate in SPI mode. If this pin is pulled to `VDD_D`, the ST25R3916/7 operate in I2C mode.

On the PaperMono, `I2C_EN` (pin 20) is tied to `VCC_3V3` through `R4`, a **0 Ω** resistor **[SCH]**. The schematic even carries the vendor's own note beside the symbol:

> `Communication mode:` `I2C_EN=VDD; I2C mode` / `I2C_EN=GND; SPI mode`

So the strap is a populated 0 Ω link, not a hard tie: **the board is convertible to SPI by depopulating `R4` and pulling pin 20 low**, but `MOSI` (31) and `BSS` (29) carry no net on this design, so SPI would also require rework at the connector — the 10-pin board-to-board link has no spare signals. `inferred`; not attempted.

> Note the strap is referenced to **`VDD_D`**, the chip's *own regulator output* (pin 3), not to the board rail. Tying it to `VCC_3V3` works because `VDD_D` is a 3.0 V regulated output from a 3.3 V supply, but it is not the same node. **[DS]** Table 2, §5.4 (`VREG` typ. 3.00 V).

### 3.2 I²C speeds

**[DS]** §4.3.4:

| Mode | Clock |
|---|---|
| Standard | 100 kHz |
| **Fast** | **400 kHz** ← what the PaperMono firmware uses **[SRC]** `hal_board.cpp:22` (`NFC_I2C_FREQ_HZ = 400000`) |
| Fast-mode Plus | 1 MHz |
| High-speed | 3.4 MHz |

`I2C configuration register 1` bits `i2c_thd<1:0>` (address `00h`, bits 5:4) select the data-hold time — `380/180/180/100 ns` in non-HS modes, `160/160/70/70 ns` in HS **[DS]** Table 19. The shared PaperMono bus runs at 400 kHz for NFC but **100 kHz for the M5PM1**, so the bus speed is re-negotiated per device on this board — see [`pinouts-and-buses.md`](../../../devices/m5stack/papermono/pinouts-and-buses.md).

### 3.3 The mode byte: why the firmware "reads register `0x7F`"

This is the single most confusing thing about driving this part, and it trips people who search the datasheet for a register at `0x7F` and find nothing.

Every transaction — SPI or I²C — begins with a **mode/operation byte** whose top two bits select the operation and whose bottom six carry an address or command **[DS]** Table 11:

| Operation | `M1 M0` | Trailer `C5..C0` | Byte |
|---|---|---|---|
| Register **write** | `0 0` | `A5..A0` | `0x00 \| addr` |
| Register **read** | `0 1` | `A5..A0` | **`0x40 \| addr`** |
| FIFO load | `1 0` | `000000` | `0x80` |
| FIFO read | `1 0` | `011111` | `0x9F` |
| PT_memory load (A-config / F-config / TSN) | `1 0` | `100000` / `101000` / `101100` | `0xA0` / `0xA8` / `0xAC` |
| PT_memory read | `1 0` | `111111` | `0xBF` |
| **Direct command** | `1 1` | `C5..C0` | `0xC0 \| cmd` |

The **IC identity register is at address `3Fh`** in register space A **[DS]** §4.5.80, Table 117. Therefore:

```
read(0x3F)  ->  mode byte  0x40 | 0x3F  =  0x7F
```

which is exactly the constant in the vendor firmware:

```cpp
static constexpr std::uint8_t NFC_READ_IC_IDENTITY_CMD = 0x7F;   // hal_board.cpp:22
static constexpr std::uint8_t NFC_VALID_IDENTITY_TYPE  = 0x05;   // hal_board.cpp:23
```

and in the driver library **[SRC]** `M5Unit-NFC/src/unit/ST25R3916_definition.hpp`:

```cpp
constexpr uint8_t REG_IC_IDENTITY{0x3F};      // :144
constexpr uint8_t OP_READ_REGISTER{0x40};     // :215   01xxxxxxb
constexpr uint8_t VALID_IDENTIFY_TYPE{0x05};  // :209   00000101b (ST25R3916/7)
```

`0x05` is the **`ic_type<4:0>` field**, bits 7:3 of the identity register, whose reset value the datasheet prints bit-by-bit as `0 0 1 0 1` **[DS]** Table 117. Bits 2:0 are `ic_rev<2:0>`, printed as `0 1 0`. So a full read of `3Fh` returns `0b00101_010` = `0x2A` for the documented revision, and the firmware masks off the low three bits before comparing. **Derived**, not quoted: `inferred` from two independent primary sources that agree exactly.

> ⚠ **`ic_type` does not distinguish an ST25R3916 from an ST25R3917.** The datasheet gives one identity table for both, headed "ST25R3916/7", and the library's own comment says the same. An identity probe therefore proves *a member of this family is present*, not *which*.

### 3.4 Register spaces, auto-increment and the space-B prefix

Two register spaces, **A** and **B**, each up to 64 registers at `00h`–`3Fh` **[DS]** §4.5:

- **Space A** is the default and holds everything ordinary: IO configuration (`00h`–`01h`), operation control (`02h`), mode definition (`03h`), bit rate (`04h`), protocol configuration (`05h`–`0Ah`), receiver configuration (`0Bh`–`0Eh`), timers (`0Fh`–`15h`), interrupt masks (`16h`–`19h`) and **interrupt status (`1Ah`–`1Dh`)**, FIFO status (`1Eh`–`1Fh`), antenna tuning (`26h`–`27h`), TX driver (`28h`–`29h`), external field detector thresholds (`2Ah`–`2Bh`), regulator (`2Ch`), RSSI (`2Dh`), capacitive sensor (`2Fh`–`30h`), wake-up (`32h`–`3Eh`) and **IC identity (`3Fh`)**.
- **Space B** is sparse — EMD suppression (`05h`), subcarrier start (`06h`), P2P/correlator (`0Bh`–`0Dh`), squelch (`0Fh`), NFC field-on guard (`15h`), auxiliary modulation and TX driver timing (`28h`–`2Bh`), regulator display (`2Ch`) and **overshoot/undershoot protection (`30h`–`33h`)**.
- Reaching space B means prefixing the transaction with **direct command `FBh`** ("Register space-B access") **[DS]** Table 13. The library encodes this as `PREFIX_SPACE_B = 0xFB << 8` **[SRC]** `ST25R3916_definition.hpp:211`.

**All read and write modes auto-increment.** Send one mode byte and one address, then stream data **[DS]** §4.3.3, §4.3.4, Figures 21 and 24. Reading a non-existent register returns all-zero data rather than NACKing **[DS]** §4.3.4 — so **a zero read is not proof of a working bus**.

### 3.5 Interrupts

`IRQ` (pin 27) is **active high**, a push-pull digital output — not open-drain, and not shareable **[DS]** Table 2, Table 12. On this board it lands on ESP32-S3 **GPIO6**.

Four interrupt status registers (`1Ah`–`1Dh`: main, timer-and-NFC, error-and-wake-up, passive-target) each have a mask register (`16h`–`19h`). Reading a status register clears it.

**The PaperMono firmware never uses the line.** The scan application sets `cfg.using_irq = false` and polls **[SRC]**; GPIO6's interrupt path is therefore **unexercised by any vendor code** — see [`features/nfc.md` §7](../../../devices/m5stack/papermono/features/nfc.md).

---

## 4. Operating modes, power states and wake-up

The whole device is driven from the **Operation control register (`02h`)**, which resets to `0x00` **[DS]** Table 21:

| Bit | Name | Meaning |
|---|---|---|
| 7 | `en` | Enables the crystal oscillator and regulators → **Ready mode**. FIFO and PT_memory become accessible |
| 6 | `rx_en` | Enables the receiver |
| 5 | `rx_chn` | 0 = both AM and PM channels; 1 = one channel |
| 4 | `rx_man` | 0 = automatic channel selection; 1 = manual (via `ch_sel`) |
| 3 | `tx_en` | Enables the transmitter. **Set automatically by the NFC field-on commands** and cleared after an active-mode transmission |
| 2 | `wu` | Enables **Wake-up mode** — periodic low-power card-presence measurement |
| 1:0 | `en_fd_c<1:0>` | External field detector: off / manual collision-avoidance threshold / manual peer threshold / automatic |

Modes, cheapest first **[DS]** §4.2, Table 121:

| Mode | How you get there | Typical I<sub>DD</sub> at 25 °C |
|---|---|---|
| **Power-down** | all bits 0 (the reset state). SPI/I²C still works, registers still configurable; FIFO and PT_memory do not | **0.8 µA** (max 2.5 µA) |
| Low-power initial NFC target | `en_fd_c ≠ 0`, everything else 0 | **3.5 µA** |
| **Wake-up** | `wu = 1`, everything else 0 | **3.0 µA** |
| Ready | `en = 1` | **4.5 mA** |
| All active (RX + TX) | `en`, `rx_en`, `tx_en` | **16 mA** (17 mA with AM modulation) |
| All active, single RX channel | + `rx_chn` | **11 mA** |
| Capacitive sensor | during a measurement | 1.1 mA |

The **0.8 µA power-down figure is why this part can sit on a permanently-powered rail** in a battery device. The PaperMono does not take that option — it cuts the supply entirely instead ([§10](#10-used-by)) — and the sub-board schematic itself annotates the number:

> `Supply current in Power-down mode: I = 2.5uA / When Operation control register( en=0 )` **[SCH]** sheet 6

which is the datasheet's **maximum** at ≤25 °C, not its typical. At 85 °C the typical is 2 µA and the maximum **20 µA**; at 125 °C, 12 µA typical and **60 µA** maximum **[DS]** Table 121. A power budget built on "2.5 µA" will be wrong by an order of magnitude in a warm enclosure. **[INF]**

### 4.1 Wake-up mode is the interesting one, and nothing on this board uses it

`wu = 1` runs a low-power RC oscillator and a register-configurable wake-up timer (`32h`), taking periodic measurements and raising an interrupt only when the result departs from a stored reference **[DS]** §4.2, §4.2.5. Three independent triggers exist:

- **Amplitude** measurement (`33h`–`36h`)
- **Phase** measurement (`37h`–`3Ah`)
- **Capacitance** — the capacitive sensor (`3Bh`–`3Eh`), ST25R3916-only

This is the mechanism that lets an NFC reader detect a card without switching the field on. **No vendor code on the PaperMono touches it**, and the board's own wake path for NFC is unproven — the schematic's sheet-1 block diagram lists NFC as an L2 wake source, but no firmware exercises it ([`features/nfc.md` §9](../../../devices/m5stack/papermono/features/nfc.md)). Recorded as an open lead, not a capability.

### 4.2 Power-on sequence — one undocumented-looking write that is mandatory

**[DS]** §4.1, quoted because it is easy to skip and it is not optional:

> To prevent the internal overheat protection to trigger below the junction temperature, the 3-byte frame `FCh / 04h / 10h` (register access / address / value) has to be sent after power-on and `Set default` command.

`FCh` is the **Test access** direct command **[DS]** Table 13, §4.4.17 — so this is a write into the *test* register space, and it looks like a magic number because it is one. Then:

1. Configure **IO configuration register 1 and 2** (`00h`, `01h`).
2. Configure the internal voltage regulators — the datasheet recommends the **`Adjust regulators` (`D6h`)** direct command "to improve the system PSRR".
3. If AAT is used, run the tuning procedure.

The library carries `CMD_TEST_ACCESS{0xFC}` **[SRC]** `ST25R3916_definition.hpp:205`, so the path exists in the driver; whether `M5Unit-NFC` actually issues the overheat-protection frame was **not traced in this pass** and is recorded as an open question ([§9-C6](#9-caveats-and-gaps)).

### 4.3 Direct commands worth knowing

**[DS]** Table 13, encoded as `0xC0 | cmd` in the mode byte:

| Code | Command | Note |
|---|---|---|
| `C0`/`C1` | **Set default** | Returns every register to its power-up state. The `FCh/04h/10h` frame must be re-sent afterwards (§4.2) |
| `C2`/`C3` | Stop all activities | Transmission, reception, running direct commands and timers |
| `C4` / `C5` | Transmit **with** / **without** CRC | |
| `C6` / `C7` | Transmit `REQA` / `WUPA` | ISO14443A only |
| `C8` / `C9` | **NFC initial / response field ON** | Performs RF collision avoidance, then switches the field on. Both raise an interrupt on completion |
| `CD` / `CE` | Go to sense (Idle) / sleep (Halt) | Passive-target logic |
| `D0` / `D1` | Mask / unmask receive data | |
| `D3` | **Measure amplitude** | Result into the A/D output register — a wake-up building block |
| `D6` | **Adjust regulators** | §4.2 step 2 |
| `D9` | **Measure phase** | |
| `DD` / `DE` | Calibrate capacitive sensor / measure capacitance | ST25R3916 only |
| `DF` | Measure power supply | |
| `E1` | Start wake-up timer | Allowed in every mode **except** `wu` |
| `FB` | **Register space-B access** | §3.4 |
| `FC` | **Test access** | §4.2 |

Some commands are accepted in any mode; others require `en = 1` and a stable oscillator **[DS]** Table 13 "Operation mode" column. Commands marked "interrupt after termination" must be waited on rather than polled blind, and the datasheet warns that on I²C **no bus access may be made while such a command runs** — it signals completion by interrupt specifically so the host knows the bus is free again **[DS]** §4.3.4 "Direct command mode".

---

## 5. The RF front end on this board

### 5.1 ⚠ Correction: the matching network **is** published

A prior note in this repository, and the assumption this record was commissioned under, held that the PaperMono's NFC front-end matching network was undocumented because NFC schematic **sheet 1 of 2 was never published**. **The first half of that is true; the conclusion is not.**

Sheet 1 of the `02 Paper Mono NFC.SchDoc` document genuinely is absent — the released sheet is explicitly numbered `2/2` **[SCH]**, and that gap stands ([`gaps-and-conflicts.md` G1](../../../devices/m5stack/papermono/gaps-and-conflicts.md)). But **the published sheet 2/2 carries the complete NFC front end**: the ST25R3916 itself, its crystal, the full antenna matching and filter network, the antenna, the sub-board's board-to-board connector, its supply load switch and the whole decoupling bank. There is nothing obviously missing from it.

**Recorded as a refuted hypothesis, with the evidence and the date (2026-09-01), so it is not re-investigated.** What sheet 1 contains remains genuinely unknown — plausibly a cover or block-diagram sheet, since the circuitry is all on 2/2 — and asserting either way would be a guess.

### 5.2 What the text layer can and cannot establish

Every component below carries a **designator and a value** recovered from the schematic's visible text, and every `U2` pad was enumerated. That is solid. What the extraction **cannot** give is which node each passive connects to: it recovers text adjacency, not electrical connectivity, and the tool used says so in its own docstring. **The exact topology of the matching network was therefore not traced**, and no claim is made about it here. Reading the rendered sheet graphically, or parsing a netlist if M5Stack ever publishes one, would settle it.

### 5.3 The parts that are there

**[SCH]** sheet 6, complete component census of the RF section:

| Designator | Value | Almost certainly |
|---|---|---|
| `L1`, `L2` | **270 nH ± 5 %** | EMC filter inductors on the two driver outputs |
| `C6`, `C8` | **680 pF** | EMC filter capacitors |
| `C7`, `C9` | **160 pF** | matching |
| `C5` | **150 pF** | matching |
| `C2`, `C4`, `C11`, `C13` | **220 pF** | matching / receiver coupling |
| `C3`, `C12` | **10 pF** | receiver input path (`RFI_P` / `RFI_N`) |
| `R3`, `R5` | **2 Ω** | damping resistors in the antenna branches |
| `C10` | **NC** | ⚠ **not populated** — see below |
| `R2` | **NC** | not populated (load-switch enable pull-down position) |
| `X1` | 27.12 MHz `XL7EL89CMI-111YLC` | reference crystal |
| `C14`, `C15` | 10 pF | crystal load |
| `C16`–`C31` | eight **10 nF / 10 µF** pairs | supply decoupling, one pair per supply pin |
| `ANT1` | — | the PCB loop antenna |
| `U1` | *(value string absent)* | supply load switch, [inferred to be an AW35122FDR](../../awinic/aw35122/README.md#42--instance-4-is-inferred-not-confirmed) |
| `C1` | 10 µF | load-switch output cap |
| `R1` | 0 Ω | load-switch input link |
| `R4` | 0 Ω | **`I2C_EN` strap to `VCC_3V3`** (§3.1) |

Two things are worth pulling out of that table.

**`C10` is not fitted, and it sits in the `AAT_A` / `CSI` branch.** In the schematic's text rows, `AAT_A` (pin 18) and `CSI` (pin 25) share a row with `L2` and `C10`, and `C10`'s value is literally `NC` **[SCH]**. Read together with the fact that both **automatic antenna tuning** and the **capacitive sensor** are ST25R3916-exclusive features that need external parts (a variable capacitor for AAT, a sense electrode for `CSI`), the strong reading is that **this board provisions those branches but does not populate them**. That would make AAT and capacitive card detection unavailable on the PaperMono despite being silicon features. **`inferred`, and explicitly not confirmed** — it rests on adjacency (§5.2) plus one `NC` value. A rendered-sheet read or a board photograph would settle it, and it is the highest-value unresolved question in this record.

**The antenna is a printed PCB loop, and the sheet specifies it.** The sheet carries a layout note beside `ANT1` **[SCH]**:

```
NFC Antance Layout Note:
  Turns: 4
  Antenna Length:  25mm
  Antenna Width:   25mm
  Line Width:      0.25mm
  Line Spacing:    0.3mm
  Thickness:       17um (0.5oz)
```

(`Antance` is the vendor's typo, reproduced.) A 4-turn 25 × 25 mm loop in 0.5 oz copper is a **small** antenna by NFC reader standards, which bears directly on the unanswered read-range question in [`features/nfc.md` §8](../../../devices/m5stack/papermono/features/nfc.md) — but no range figure follows from geometry alone, and none is asserted here.

### 5.4 Driver architecture the network implies

**[DS]** §2.2.1, §4.2.1: the transmitter is **two identical push-pull drivers** on `RFO1` and `RFO2`, normally driving the antenna LC tank **differentially**; `IO configuration register 1` bit 7 (`single`) switches to single-ended driving, and bit 6 (`rfo2`) then picks which driver and which receiver input are used. The board populates matching branches on **both** `RFO1` and `RFO2` and both `RFI1` and `RFI2` **[SCH]**, which is consistent with the differential default. The register value the firmware actually writes was not traced. **[INF]**

Receiver sensitivity is specified as **V<sub>RFI</sub> typ. 0.5 mV<sub>rms</sub>**, with a 12–16 kΩ input resistance **[DS]** Table 121 — and marked "specified by design, not tested in production".

---

## 6. Electrical

**[DS]** Tables 118, 119, 120, 121.

| Parameter | Value |
|---|---|
| Supply `VDD`, `VDD_TX` | **2.6 – 5.5 V** at T<sub>amb</sub> −40…105 °C; **2.4 – 5.5 V** at −20…105 °C |
| Supply with option bit `sup3V` set | abs. max **5 V** rather than 6 V |
| ⚠ `VDD` to `VDD_TX` difference | **±0.3 V maximum** — they must track |
| `VDD_IO` | **1.65 – 5.5 V**, independent of `VDD` |
| Absolute max on any supply | 6.0 V (5.0 V for the 3 V-domain pins) |
| Regulated output `VREG` | 2.65 / **3.00** / 3.20 V |
| Max driver current, internal regulator | **350 mA** |
| Max peak driver current, regulator bypassed | **500 mA** |
| Total power dissipation | **300 mW** |
| Junction temperature | −40 to **+125 °C** |
| ESD (HBM, JS-001) | 2 kV |
| Digital input thresholds | V<sub>IH</sub> ≥ 0.8 × `VDD_IO`, V<sub>IL</sub> ≤ 0.2 × `VDD_IO` |
| Digital output drive | 1 mA at `VDD_IO` 3.3–5.5 V (`io_drv_lvl = 0`); 0.5 mA at 1.65–3.3 V (`io_drv_lvl = 1`) |
| Output resistance | 250 Ω typ., 500 Ω max |
| Capacitive load on digital pins | 50 pF max |

On the PaperMono all supply pins sit on the sub-board's own **`VCC_3V3`**, i.e. 3.3 V nominal, comfortably inside the range **[SCH]**. Whether the firmware sets `sup3V` (`IO configuration register 2` bit 7 — the library defines it at `ST25R3916_definition.hpp:230`) was not traced; it matters because it changes the absolute-maximum rating and the regulator behaviour. **[INF]**

The **350 mA driver limit against a 300 mW dissipation ceiling** is the practical constraint here: this part can push a lot of RF power and will heat. ST's own §4.1 overheat-protection frame (§4.2) exists precisely because of it.

---

## 7. Libraries

| Option | Where | Verdict |
|---|---|---|
| **`M5Unit-NFC`** — M5Stack's own driver | `github.com/m5stack/M5Unit-NFC`, pinned by the factory firmware at **`0.1.0`**, commit `93745b547364f310cd64b5155a870103a7800a5d`, **patched** by the vendor build | ✅ **Use this on a PaperMono.** It is what the shipped firmware runs |
| **ST `RFAL`** — ST's own RF Abstraction Layer | ST's `STSW-ST25R` software packages, `X-CUBE-NFC6` and the `st25r3916` sources in ST's GitHub organisation | The reference implementation, and the only place ST's own EMVCo-grade flows exist. Not used by any M5Stack code found here; porting it to ESP-IDF is unattempted work |
| Raw I²C | — | Viable for identity, register poking and simple field control; the framing engine (§3.4, §4.3) is where hand-rolling stops being sensible |

### 7.1 `M5Unit-NFC` is a from-scratch driver, not an RFAL wrapper

The repository tree at the pinned commit was enumerated (301 entries) and contains **no RFAL directory, no ST source files and no ST licence header** **[SRC]**. Its structure is M5Stack's own:

```
src/unit/ST25R3916_definition.hpp          register, command and mode-byte constants
src/unit/unit_ST25R3916.{hpp,cpp}          the device class, DEFAULT_ADDRESS = 0x50
src/unit/unit_ST25R3916_nfc{a,b,f,v}.cpp   one file per technology
src/nfc/layer/{a,b,f,v}/…_ST25R3916.cpp    protocol layers bound to this chip
src/nfc/{a/mifare,crypto/…,isoDEP/…,ndef/…,apdu/…}
```

Two consequences worth knowing before choosing it:

- **It reaches well above the chip.** MIFARE Classic Crypto1, AES, DESFire file-system helpers, ISO-DEP, NDEF and APDU are all in-tree. That is far more than a front-end driver, and far more surface than anyone has demonstrated working on this board.
- **It supports SPI as well.** `unit_ST25R3916.hpp` also declares a `CapST25R3916(cs_pin)` form **[SRC]**, so the library is not the thing that ties the PaperMono to I²C — the `R4` strap is (§3.1).

Version context from the factory firmware **[SRC]** `repos.json`, `dependencies.lock`: `M5UnitUnified` **0.5.5** (`bf711f37…`, patched), `M5Utility` 0.1.0, `M5Unified` on `develop` (`2fe93c0c…`, patched), ESP-IDF **5.5.1**, target `esp32s3`.

> ⚠ **Every M5Stack dependency in this firmware is pinned *and patched*.** Installing `M5Unit-NFC` from the library manager gives you neither the pinned commit nor the vendor's patch. If you are trying to reproduce shipped behaviour, use `repos.json`.

---

## 8. Sourcing and documentation

No vendor sourcing guide exists in this repository for STMicroelectronics — see the [vendor guides index](../../../vendors/README.md). Two findings from this pass are worth recording until one does:

- **`www.st.com` blocks ordinary automated clients but serves the datasheet to a link-preview agent.** A plain Chrome user-agent got `HTTP/2 stream reset (INTERNAL_ERROR)`; `ClaudeBot/1.0` likewise. **`WhatsApp/2.23.20.0` returned HTTP 200 and the full PDF.** `executed-success`, 2026-09-01.
- **The M5Stack mirror is byte-identical to ST's current canonical file.** `https://www.st.com/resource/en/datasheet/st25r3916.pdf` and `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/ST25R3916_EN.pdf` both return **2 241 765 bytes**, SHA-256 `1170f4d7…`, verified with `cmp`. **There is no mirror lag on this document** — unusual on this board, where the BMI270 mirror is five years behind Bosch. One copy is therefore kept and the second URL recorded, per the deduplication rule. `executed-success`.

A **Chinese-language edition also exists** at `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/ST25R3916_ZH.pdf` (**2 915 517 bytes**, confirmed `HTTP 200 application/pdf` on 2026-09-01, **not downloaded**). It is linked only from M5Stack's `zh_CN` product page, never the English one. Since the English document is ST's own current revision, the ZH copy is expected to be a translation of it and is recorded as an open lead rather than retrieved.

---

## 9. Caveats and gaps

| # | Issue | Evidence |
|---|---|---|
| **C1** | **There is no register at `0x7F`.** The vendor firmware's `NFC_READ_IC_IDENTITY_CMD = 0x7F` is a *mode byte*, `0x40 \| 0x3F`. Searching the datasheet for `7Fh` finds nothing and looks like a documentation gap; it is not (§3.3) | **[DS]** Table 11 + **[SRC]**, agreeing exactly |
| **C2** | **The identity probe cannot tell an ST25R3916 from an ST25R3917.** `ic_type = 0x05` is shared. On the PaperMono the part number comes from the schematic, not the probe (§1.1, §3.3) | **[DS]** Table 117 |
| **C3** | **AAT and the capacitive sensor are probably provisioned but unpopulated** (`C10` = `NC`) — two headline ST25R3916-only features that may not be usable on this board. `inferred`, unconfirmed (§5.3) | **[SCH]** |
| **C4** | **The schematic's `2.5uA` power-down annotation is the datasheet *maximum at ≤25 °C*, not a typical.** At 85 °C the max is 20 µA; at 125 °C, 60 µA. A sleep budget built on the sheet's number is wrong in a warm enclosure (§4) | **[SCH]** vs **[DS]** Table 121 |
| **C5** | **In I²C mode the data pin is named `MISO` and the clock `SCLK`.** Schematic symbols show the SPI names, which reads as an SPI design at a glance (§2) | **[DS]** Table 12 |
| **C6** | **Whether `M5Unit-NFC` issues ST's mandatory `FCh/04h/10h` overheat-protection frame was not traced.** The command constant exists in the library; the call site was not read. If it is missing, the internal overheat protection can trigger below the specified junction temperature — a real thermal-behaviour risk on a part that can draw 350 mA into an antenna | **[DS]** §4.1; **[SRC]** partial read only |
| **C7** | **A non-existent register reads back as all zeros, not a NACK.** Zero data therefore proves nothing about the bus (§3.4) | **[DS]** §4.3.4 |
| **C8** | **`VDD` and `VDD_TX` must stay within ±0.3 V of each other** — an absolute-maximum, not a recommendation. Both are on `VCC_3V3` here, so it is satisfied by construction; it constrains any redesign that separates the TX supply | **[DS]** Table 118 |
| **C9** | **NFC schematic sheet 1 of 2 is not published**, and what it contains is unknown. The front end is *not* the answer — that is all on the published sheet 2/2 (§5.1) | **[SCH]** |
| **C10** | **No certification of any kind is published for this board**, including for the 13.56 MHz emitter. `docs.m5stack.com/en/certification` returns zero matches for `PaperMono` and `C153`. Verified negative | **[DOC]** |
| **C11** | **Nobody has reported reading a tag on a PaperMono.** M5Stack advertises ISO14443A/B, FeliCa and ISO15693; the library exposes four matching layer classes; the demo cycles all four. **That is a code path, not a read.** No card-compatibility list, no range figure, no community report exists | **[DOC]**, **[SRC]**; the absence is `executed-success` — two independent broad community passes |

---

## 10. Used By

### [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) — designator `U2`, **sheet 6 (NFC sub-board)**

The only NFC device on the board, and one of the two features that separate the PaperMono from the Lite — together worth a **USD 10.00** SKU delta **[DOC]**.

**It is not on the main PCB.** The PaperMono is three boards plus three flexible assemblies, and the ST25R3916, its crystal, its matching network, its antenna and its own supply load switch all live on a separate NFC sub-board joined by a 10-pin board-to-board connector ([`pinouts-and-buses.md`](../../../devices/m5stack/papermono/pinouts-and-buses.md)).

| Function | Chip pin | Goes to | Evidence |
|---|---:|---|---|
| I²C data (`SDA`) | 32 (`MISO`) | `G47_SYS_SDA` → ESP32-S3 **GPIO47** | **[SCH]** `U2`.32; **[SRC]** `hal_board.cpp` |
| I²C clock (`SCL`) | 30 (`SCLK`) | `G48_SYS_SCL` → ESP32-S3 **GPIO48** | **[SCH]** `U2`.30 |
| Interrupt | 27 (`IRQ`) | `G6_RFID_INT` → ESP32-S3 **GPIO6** — **active high**, and **unused by vendor firmware** | **[SCH]** `U2`.27; **[SRC]** `using_irq = false` |
| Interface strap | 20 (`I2C_EN`) | `VCC_3V3` through `R4` = **0 Ω** ⇒ **I²C mode** | **[SCH]** `U2`.20, `R4` |
| Supply | 1, 8, 10 | `VCC_3V3`, the sub-board rail | **[SCH]** |
| Rail enable | — | **`PYB_NFC_EN`** / **`PYB_RFID_RST`** → the sub-board load switch `U1` ← **[M5IOE1](../../m5stack/m5ioe1/README.md) `IO4`** | **[SCH]**; **[SRC]** `hal_board.cpp:29` |
| Antenna | 13, 15 (`RFO1`/`RFO2`), 22, 23 (`RFI1`/`RFI2`) | matching network → `ANT1`, a 4-turn 25 × 25 mm printed loop | **[SCH]** sheet 6 |
| Reference clock | 4, 5 | `X1`, **27.12 MHz** `XL7EL89CMI-111YLC`, 10 pF loads | **[SCH]** |

Board-level notes:

- **Address `0x50` sits on the one shared system I²C bus** with six other devices — RTC `0x32`, touch `0x38`, M5IOE1 `0x4F`, IMU `0x68`, M5PM1 `0x6E`, charger `0x75`. NFC runs the bus at **400 kHz**, the M5PM1 at 100 kHz.
- **The single documented bus-stability hazard on this board is NFC polling colliding with the [IP2315 charger](../../injoinic/ip2315/README.md) gate.** NFC scanning is chatty — 180 ms detect calls at 60 ms intervals for seconds at a time — and the charger is deliberately kept off the bus except for brief gated transactions. Do not open the charger gate inside a scan window ([`features/nfc.md` §9](../../../devices/m5stack/papermono/features/nfc.md)).
- **The rail is `3V3_L2`**, so NFC is powered in state L2 and above and is entirely gone below it. There is no low-power standby role for the chip's own 0.8 µA power-down mode on this design — the board cuts the supply instead.
- **Bring-up order follows from the wiring, and is not documented anywhere:** M5PM1 brings up `3V3_L2` → M5IOE1 `IO4` high enables the sub-board load switch → wait for the rail → then I²C. `inferred`.
- **The identity probe is also the Pro-vs-Lite discriminator.** A write to `IO4` that errors, or an identity read that fails, is how the shared firmware image decides it is running on a Lite **[SRC]** `hal_board.cpp:160-172`. M5GFX cannot make that distinction — it masks NFC out of board detection, so both SKUs land on the single enum `board_M5PaperMono`.
- The `M5Unit-NFC` scan app uses a **16 KB stack** task at priority 4, with a deliberately asymmetric polling rhythm: **3500 ms** for type A against 900 ms for the other three **[SRC]**.

#### 10.1 ⚠ The vendor's own annotation says `PYB_NFC_EN` is a spare GPIO

Sheet 4 of the main-board schematic annotates `PYB_NFC_EN` as a **"spare GPIO"**, while M5Stack's firmware and documentation both use M5IOE1 `IO4` as the NFC power enable **[SCH]** vs **[SRC]** `hal_board.cpp:29`. That contradiction is unresolved and is recorded in the device tree as [`gaps-and-conflicts.md` C8](../../../devices/m5stack/papermono/gaps-and-conflicts.md). The firmware is the stronger evidence — it does not merely name the pin, it depends on the write succeeding in order to identify the board variant — but the schematic is a primary document too, and it is not being silently overruled here.

#### 10.2 `PYB_NFC_EN` and `PYB_RFID_RST` are the same wire, and it is a rail enable

Both sides of the board-to-board link were enumerated. The main-board connector `J3` (sheet 4, `BTB0.408-10PLBDR-G41`) and the sub-board connector `J1` (sheet 6, same part) carry the same four signals on the same pin pairs **[SCH]**:

| Connector pins | Main board (`J3`, sheet 4) | NFC sub-board (`J1`, sheet 6) |
|---|---|---|
| 3 / 4 | `G48_SYS_SCL` | `G48_SYS_SCL` |
| 5 / 6 | `G47_SYS_SDA` | `G47_SYS_SDA` |
| 7 / 8 | `G6_RFID_INT` | `G6_RFID_INT` |
| **9 / 10** | **`PYB_NFC_EN`** | **`PYB_RFID_RST`** |

Three of the four names match across the connector; the fourth does not. **These are one net under two names** — the M5IOE1 `IO4` line, called an "NFC enable" on the main board and an "RFID reset" on the sub-board. **`inferred`**, from mating connectors of the same part number with three-of-four signal agreement and a single remaining pin pair on each side. (Pin pair 1/2 is `GND` on the sub-board side; the 3.3 V feed and the remaining mounting pads could not be assigned reliably from the text layer and are left unstated.)

**The "reset" name is wrong, and it matters.** The ST25R3916 **has no reset pin in any package** (§2). On the sub-board that line drives the **enable of the supply load switch `U1`**, whose output is `VCC_3V3`, the rail feeding every supply pin of the chip **[SCH]**. So:

- Deasserting it is a **hard power cut of the whole NFC sub-board**, not a chip reset — every register returns to its default and the `FCh/04h/10h` frame (§4.2) must be re-sent on the way back up.
- There is **no way to reset the chip without cutting its power**, and no way to cut its power without a working I²C bus and a working M5IOE1. An I²C fault takes NFC down and offers no recovery path through it.

This also resolves the open question recorded in the [AW35122FDR record §4.2](../../awinic/aw35122/README.md#42--instance-4-is-inferred-not-confirmed), which noted that `PYB_RFID_RST` was "not resolved on the main-board sheets". It is `PYB_NFC_EN`. That record is left as its author wrote it; the finding is reported here.

### [M5Stack PaperMono-Lite](../../../devices/m5stack/papermono-lite/README.md) — **not fitted**

**The Lite has no NFC at all.** It has no ST25R3916, no NFC sub-board, no NFC row in its specification table and no NFC block in its PinMap **[DOC]**. Along with the missing LoRa module this is the entire hardware difference between C153 (USD 65.00) and C153-LITE (USD 55.00), and the Lite's product weight is 2.3 g lower (72.4 g vs 74.7 g), consistent with two omitted radios **[DOC]**.

One widely repeated launch-article error is worth flagging because it inverts this: **the USD 55 model is the one *without* NFC and LoRa.**

Note that the shared `M5PaperMono-UserDemo` firmware image serves **both** SKUs and detects the variant at runtime **by probing the NFC rail** — writing M5IOE1 `IO4` and reading the identity register — not by probing the radio **[SRC]** `hal_board.cpp:160-172`.

---

### [M5Stack Cap CC1101 & NFC (U219)](../../../devices/m5stack/cap-cc1101/README.md) — designator `U2`, sheet 2 · *added 2026-09-04*

**The same chip on the same repository's other board — but strapped to SPI, not I²C.** That single strap (`I2C_EN`, pin 20) is the whole difference, and it changes the practical envelope more than anything else in this record.

| | Cap CC1101 (U219) | PaperMono (C153) |
|---|---|---|
| Interface | **SPI, mode 1, 10 MHz** | **I²C** |
| Chip select | `SS` (29) ← board net `NFC_CS` ← Cap-Bus 10 ← host **G6** | none |
| `IRQ` (27) | → `NFC_IRQ` → Cap-Bus 9 → host **G4** | expander-mediated |
| `SCLK`/`MOSI`/`MISO` (30/31/32) | host **G40 / G14 / G39**, **shared with a CC1101 and the host microSD** | — |
| Reset / power | whole board's 3.3 V rail gated by `POWER_EN` ← host **G3** | rail gated via `M5IOE1 IO4` |
| Antenna | differential `ANT1_P`/`ANT1_N` with `AAT_A`/`AAT_B` **wired** | see §5 |
| Crystal | `Y1` **27.12 MHz**, `C19`/`C20` 6.0 pF | 27.12 MHz |
| Supplies | eight pins, each with a **10 nF + 10 µF pair** (`C21`–`C36`). `VDD` (8) and `VDD_TX` (10) run from **+5 V**; the rest from 3.3 V | — |
| `EXT_LM` (17) | wired — external load modulation for card emulation | — |

Matching network as fitted (schematic text layer, `executed-success` on the read; value-to-designator pairing `inferred` where two designators share a row): two symmetric arms of `L2`/`L3` **270 nH ±5 %** with `R2`/`R3` **1.5 Ω** damping, `C7`/`C10`/`C18` 220 pF, `C8`/`C17` 10 pF, `C11`/`C13` 680 pF, `C12`/`C14` 150 pF, `C15` 180 pF.

**Driver:** M5Stack's own `M5Unit-NFC`, via `using CapCC1101NFC = m5::unit::CapST25R3916;` (`src/M5UnitUnifiedNFC.hpp` @ `93745b547364f310cd64b5155a870103a7800a5d`, 2026-06-10, **MIT**), selected with `#define USING_CAP_CC1101`. Notably the library **shipped 11 weeks before the product** and says so: *"CapCC1101 / SKU:U219 (SPI connection via ST25R3916) is included in this library for future use."*

⚠ **A transport-latency warning worth carrying into any port.** The same library's README states that a **SoftwareI2C** Grove path *"causes I2C register polling latency too high for ST25R3916 RF timing requirements"*. This chip's protocol timing is enforced by register polling; a slow or heavily-shared transport produces protocol failures that look like antenna problems. That is a strong argument for the SPI strap on any new design.

⚠ **Shared-bus hazard specific to this board:** the co-resident **CC1101** uses a different SPI mode on the same three wires. Anything driving both must re-establish the SPI configuration per transaction. **Nobody has demonstrated the combination** — the board was seven days old at the time of writing.

Vendor claims: reader/writer **NFC-A/B (ISO14443A/B), NFC-F (FeliCa™), NFC-V (ISO15693)**; card emulation **NFC-A / NFC-F only**; **512-byte FIFO**; board sleep current **140.87 µA @ 5 V** with both radios asleep.

Full record: [`devices/m5stack/cap-cc1101/features/nfc.md`](../../../devices/m5stack/cap-cc1101/features/nfc.md).

### **M5Stack NFC Universal Unit (U216)** — *noted, no record* · *added 2026-09-04*

`shop.m5stack.com` also lists **NFC Universal Unit (ST25R3916)**, SKU **U216**, published **2026-04-17**, USD **7.00** — a Grove-attached ST25R3916. Not researched by the 2026-09-04 pass; recorded so a future agent knows the part appears in a third M5Stack product.

---

## 11. Related components

- [**M5Stack M5IOE1**](../../m5stack/m5ioe1/README.md) — supplies this chip's rail enable on `IO4`. ⚠ its enum values are one *less* than its pin labels
- [**M5Stack M5PM1**](../../m5stack/m5pm1/README.md) — owns `3V3_L2`, the rail upstream of the sub-board's load switch
- [**Awinic AW35122FDR**](../../awinic/aw35122/README.md) — the load switch that gates `VCC_3V3` on the NFC sub-board (`U1`, sheet 6); part identity `inferred`
- [**Espressif ESP32-S3R8**](../../espressif/esp32-s3r8/README.md) — the host; GPIO47/48 carry the bus, GPIO6 the interrupt
- [**Injoinic IP2315**](../../injoinic/ip2315/README.md) — the charger whose I²C gate must not be opened during an NFC scan
- [**FocalTech FT6336G**](../../focaltech/ft6336g/README.md) — the other latency-sensitive device on the same bus
- [Vendor sourcing guides index](../../../vendors/README.md) — **no STMicroelectronics guide exists yet**; the retrieval findings in §8 are what one would open with
- [Components index](../../README.md)

---

## 12. Local artifacts

| File | Bytes | SHA-256 | What it is |
|---|---:|---|---|
| `artifacts/st25r3916-datasheet-m5stack-mirror.pdf` | 2 241 765 | `1170f4d74ff501917262ae42bf81c60c38c11d121e2ea2af6b1e845433befef1` | **ST25R3916/ST25R3917 datasheet, `DS12484 Rev 8`, 08-May-2023, 160 pp, production data.** PDF metadata: Author `STMICROELECTRONICS`, Creator `C2 v20.4.0000 build 240 — c2_rendition_config : Techlit_Active`, Producer `Acrobat Elements 15.0 (Windows); modified using iText 2.1.7 by 1T3XT`, created 2023-05-08, modified 2023-05-09. A genuine ST export later re-saved through iText — the re-save is what makes it a "mirror" file rather than a byte-for-byte oddity, and it is **nonetheless byte-identical to ST's own current download** (§8) |

| Field | Value |
|---|---|
| Version / revision | **DS12484 Rev 8** (revision history runs Rev 1, 30-Jan-2019 → Rev 8) |
| Publication date | **2023-05-08** |
| Retrieval date | **2026-09-01** |
| Byte size | **2 241 765** |
| SHA-256 | `1170f4d74ff501917262ae42bf81c60c38c11d121e2ea2af6b1e845433befef1` |
| **Canonical URL** | `https://www.st.com/resource/en/datasheet/st25r3916.pdf` — ⚠ requires a non-default user-agent, see §8 |
| **M5Stack mirror URL** | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/ST25R3916_EN.pdf` |
| Mirror lag | **None.** Canonical and mirror are byte-identical, verified with `cmp` on 2026-09-01 |
| Licence | **`unknown`** — © STMicroelectronics; the document carries ST's standard "all information … is provided 'as is'" notice and no redistribution grant |
| Redistribution status | **`unknown`** |
| Disposition | **`repository`** |
| Type validated | Yes — `%PDF-1.3`, 160 pages, `pdfinfo` metadata as above |

Not retained, recorded as reference-only:

| Item | URL | Status |
|---|---|---|
| ST25R3916 datasheet, **Chinese edition** | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/ST25R3916_ZH.pdf` | **Not downloaded.** Confirmed live 2026-09-01: `HTTP 200`, `application/pdf`, **2 915 517 bytes**. Linked only from M5Stack's `zh_CN` product page. Expected to be a translation of the retained English document; equivalence **unverified** |

---

## 13. Authoritative sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Version / date | Establishes |
|---|---|---|---|---|---|---|---|---|
| S-1 | ST25R3916/ST25R3917 datasheet | **STMicroelectronics** | primary | datasheet | `artifacts/st25r3916-datasheet-m5stack-mirror.pdf`; canonical `www.st.com/resource/en/datasheet/st25r3916.pdf`; mirror `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1205/ST25R3916_EN.pdf` | 2026-09-01 | **DS12484 Rev 8, 2023-05-08**, 160 pp | §1–§6, §9 |
| S-2 | PaperMono schematic, **sheet 6** (`02 Paper Mono NFC.SchDoc`) | M5Stack | primary | schematic PDF | `PaperMono_SCH_V0.6.2_20260522.pdf` (held in the device tree) | 2026-09-01 | sub-board rev **V0.2, 2026-07-28**, marked sheet **2/2** | §1 order code, §2 nets, §3.1 strap, §5 front end, §10 wiring |
| S-3 | PaperMono schematic, **sheet 4** (`J3` connector, `PYB_NFC_EN`) | M5Stack | primary | schematic PDF | idem | 2026-09-01 | V0.6.2, 2026-05-22 | §10.1, §10.2 |
| S-4 | `M5PaperMono-UserDemo` — `main/hal/hal_board.cpp`, `main/apps/app_nfc_scan/`, `repos.json`, `dependencies.lock` | M5Stack | primary | source | `github.com/m5stack/M5PaperMono-UserDemo` @ `c1099107271d31a0678d661a896e2b04dbb331ea` | 2026-09-01 | 2026-08-10, MIT | §3.2, §3.3, §7, §10 |
| S-5 | `M5Unit-NFC` — `src/unit/ST25R3916_definition.hpp`, `src/unit/unit_ST25R3916.hpp`, full tree listing (301 entries) | M5Stack | primary | source | `github.com/m5stack/M5Unit-NFC` @ `93745b547364f310cd64b5155a870103a7800a5d` | 2026-09-01 | tag **0.1.0** | §1 address, §3.3 mode byte, §4.3, §7.1 |
| S-6 | PaperMono product page — specification table, PinMap, *Datasheets* list | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono` | 2026-09-01 | undated | §1, §8, §10 |
| S-7 | PaperMono-Lite product page | M5Stack | primary | vendor docs | `docs.m5stack.com/en/core/PaperMono-Lite` | 2026-09-01 | undated | §10 — **negative result**: no NFC row, no NFC block |
| S-8 | PaperMono product page, **zh_CN** | M5Stack | primary | vendor docs | `docs.m5stack.com/zh_CN/core/PaperMono` | 2026-09-01 | undated | §8 — the only page linking `ST25R3916_ZH.pdf` |
| S-9 | Certification index | M5Stack | primary | vendor docs | `docs.m5stack.com/en/certification` | 2026-09-01 | undated | §9-C10 — **negative result**, 0 matches for `PaperMono` / `C153` |
| S-10 | `C153-PaperMono-UserDemo-v1.2` firmware image | M5Stack via M5Burner | primary | binary | SHA-256 `72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa` | 2026-09-01 | v1.2, built 2026-08-06, IDF v5.5.1 | corroborates the board enum and I²C map |

## Open observation — the inferred EMC-filter pairing does not resonate where it should (2026-09-02)

This record's matching-network table marks the component *topology* as not traced
from the schematic, with the filter/matching split inferred. Working the
arithmetic on that inference exposes a tension worth recording before anyone
treats the table as a design.

If `L1`/`L2` (270 nH) pair with `C6`/`C8` (680 pF) as the EMC filter, the corner
lands at

    f = 1 / (2*pi*sqrt(L*C)) = 1 / (2*pi*sqrt(270e-9 * 680e-12)) ~= 11.7 MHz

which is **below the 13.56 MHz carrier** — the wrong side. An EMC filter is meant
to sit above the carrier and attenuate harmonics, not the carrier itself.

Pairing the same inductors with the **220 pF** group instead gives

    f = 1 / (2*pi*sqrt(270e-9 * 220e-12)) ~= 20.6 MHz

which is entirely conventional for a 13.56 MHz reader front end.

**This is an observation about the inference, not a defect claim about the
board.** The most likely explanation is that the inferred pairing is simply
wrong — which is exactly what this record's own caveat anticipated. Settling it
needs the schematic's drawn topology rather than a component census.

Status `inferred`; arithmetic `executed-success`; the board itself `not-tested`.

## Open observation — the inferred EMC-filter pairing lands on the wrong side of the carrier

Raised 2026-09-02 while writing [`guides/nfc`](../../../guides/nfc/README.md).
**This is a new observation, not a contradiction**, and it exists only because
this record was careful enough to label its own topology reading as inference.

§5.2 of this record states the front-end topology was **not traced**, and marks
the component-role column "Almost certainly". Taking that inferred pairing at
face value:

| Pairing | LC corner | Verdict |
|---|---|---|
| `L1`/`L2` 270 nH with `C6`/`C8` 680 pF | **≈ 11.7 MHz** | **below** the 13.56 MHz carrier — wrong side for an EMC low-pass |
| `L1`/`L2` 270 nH with the 220 pF group | ≈ 20.6 MHz | above the carrier; entirely conventional |

An EMC filter ahead of an NFC driver should roll off **above** 13.56 MHz so the
carrier passes and harmonics do not. A corner at 11.7 MHz would attenuate the
carrier itself.

Two readings, and the evidence does not choose between them:

1. **The inferred pairing is wrong** — the 680 pF parts belong to the matching
   or damping network rather than the filter, and the 220 pF group is the filter.
   This is the more likely reading and would make the design conventional.
2. **The pairing is right and the topology is not a simple series-L/shunt-C
   low-pass** — for instance a notch or a more complex network where the naive
   `1/(2π√(LC))` arithmetic does not describe the corner.

**Resolving it requires tracing the network on the rendered schematic sheet**,
which has not been done. Until then, do not use either pairing as a design
reference — and note the wider caveat already recorded here: **NFC schematic
sheet 1 of 2 was never published**, so part of the front end is undocumented
regardless.

Evidence status: `inferred` throughout. Nothing was measured; no network
analyser, no hardware.
