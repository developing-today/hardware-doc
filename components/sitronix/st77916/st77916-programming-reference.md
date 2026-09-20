# ST77916 — Programming Reference

Command set, QSPI wire protocol, initialization timing, GRAM addressing and power modes, extracted from **`artifacts/st77916-spec-v1.0.pdf`** (Sitronix ST77916 SPEC V1.0, 2022/08, 264 pages) and reconciled against the driver that actually ships on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md).

- **Companion page:** [ST77916 component record](README.md) — identity, the ST77916/SH8601 naming conflict (§2 there), board wiring, library choices. **This page does not repeat that material; read it first.**
- **Retrieved / extracted:** 2026-08-24
- **Text layer:** ✅ **Cooperated fully.** `pdftotext -layout` returns clean, correctly-encoded text including CJK. No glyph subsetting, no OCR needed. Vector figures (timing diagrams, gamma ladders) come through as ASCII-art skeletons — signal names and table data survive, waveform shapes do not.

### Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Read from `artifacts/st77916-spec-v1.0.pdf`, page cited |
| **[SRC]** | Vendor demo code, as established in [README](README.md) (`esp_lcd_sh8601.c`, `lcd_bsp.c`, `lcd_config.h`) |
| **[COM]** | Community claim |
| **[INF]** | Inference — reasoning shown |

---

## 0. Read this first: three things the spec says that the board contradicts

| # | Spec says | Board/driver does | Severity |
|---|---|---|---|
| 1 | Panel is **360 × 390**; GRAM is 360 × 390 × 18 bits **[DOC]** p.7, p.117 | Panel is **360 × 360**; `RESSET1-3` (`D0h`–`D2h`) in the init table retarget the timing controller **[SRC]** [INF] | Informational — but *never* assume `YE = 359` is the chip maximum. The chip's max row is **389** |
| 2 | QSPI read instruction is **`0x0B` FASTREAD, with 8 dummy bits** after the address phase **[DOC]** p.70 | `esp_lcd_sh8601.c` defines `LCD_OPCODE_READ_CMD (0x03)` and never uses it **[SRC]** | ⚠ **Real.** [README §7's](README.md#7-how-to-settle-the-controller-identity-empirically) suggested ID-read snippet uses `0x03` and will not work. See §2.4 |
| 3 | QSPI **read** clock cycle `TSCYCR` min is **150 ns → 6.67 MHz max** **[DOC]** p.39 Table 5 | Bus runs at **40 MHz** **[SRC]** | ⚠ **Real.** Writes are fine (`TSCYCW` min 16 ns → 62.5 MHz). **Any register read at 40 MHz is out of spec by 6×.** See §2.4 |

Findings 2 and 3 together explain why nobody has successfully read this panel's ID.

---

## 1. Command set

### 1.1 Command gating — the Sitronix "unlock"

Yes, extended commands are gated. **[DOC]** §13.1 *Page Set Table*, p.141–145.

The controller has one **Command Table 1** (the universal MIPI-DCS set, always available) and a set of **paged extended banks** reached via four *Command Set Ctrl* registers `F0h`–`F3h`.

| Cmd | Name | Params | Default (POR / SWRESET / HWRESET) | Function |
|---|---|---|---|---|
| `F0h` | **CSC1** — Command Set Ctrl 1 | 1 | `00h` | Master enables: `D0 CMD2_EN`, `D1 GAM_EN`, `D3 TEST_EN`, `D4 GIP_EN`, `D6 CDC_EN` |
| `F1h` | **CSC2** — Command Set Ctrl 2 | 1 | `10h` | `D0 CMD2_PROT1`, `D4 CMD2_xPROT2` |
| `F2h` | **CSC3** — Command Set Ctrl 3 | 1 | `84h` | `D1 CDC_xPROT1`, `D3 TST_PROT1`, `D6 CDC_PROT2`, `D7 TST_xPROT2` |
| `F3h` | **CSC4** — Command Set Ctrl 4 | 1 | `01h` | `D0 GIP_xPROT1`, `D4 GIP_PROT2` |
| `F4h` | **SPIOR** — SPI Others Read | 0 | N/A | **Toggles SPI read access to Command Table 2.** Write `F4h` → read → write `F4h` again |

**The unlock combinations, verbatim from the spec** **[DOC]** p.142:

| `F0` | `F1` | `F2` | `F3` | Unlocks |
|---|---|---|---|---|
| `00` | – | – | – | **Lock everything**: Command2, Gamma, Test, CDC and GIP command pages all disabled |
| `02` | – | – | – | **Gamma** commands (`E0h`/`E1h`) |
| `01` | `01` | – | – | **Command2 page** (`B0h`–`DEh`: power, frame rate, resolution, VCOM) |
| `08` | – | `08` | – | **Test** command page |
| `80` | – | `40` | – | **CDC** command page |
| `10` | – | – | `10` | **GIP** command page (gate-in-panel scan timing) |

Note the pairing: `F0h` is the master enable and `F1h`/`F2h`/`F3h` are per-bank *protect* registers that must be released in the same operation. This is exactly why Waveshare's init table is full of `F0`/`F1`/`F2`/`F3` writes with values `00`/`01`/`02`/`10`/`28`/`80` interleaved between register groups **[SRC]** — each pair is an unlock/relock bracket around a bank of writes.

> **Practical rule.** If you write a `B0h`–`DEh` register and nothing happens, you forgot the `F0h`/`F1h` bracket. Locking back to `F0h = 00h` when done is good hygiene and is what the vendor table does.

### 1.2 Command Table 1 — the always-available DCS set

**[DOC]** §13.2, pp.146–213. `PNUM` = parameter count. All parameters are 1 byte unless stated.

| Hex | Name | Params | What it does | Spec page |
|---|---|---:|---|---|
| `00h` | NOP | 0 | No operation | 153 |
| `01h` | **SWRESET** | 0 | Software reset. Returns to Sleep-In. **Wait 5 ms** (120 ms if it was in Sleep Out) | 153 |
| `04h` | RDDID | read 1+3 | 1 dummy byte, then `ID1`, `ID2`, `ID3` (7 bits each) | 155 |
| `09h` | RDDST | read 1+4 | Display status: `BSTON MY MX MV ML RGB MH HSD` / `IFPF ...` / `VSSON INVON DISON TEON` / `TELOM` | 155 |
| `0Ah` | RDDPM | read 1+1 | Power mode: `BSTON IDMON – SLPOUT NORON DISON` | 156 |
| `0Bh` | RDDMADCTL | read 1+1 | Reads back `MY MX MV ML BGR MH HSD` | 157 |
| `0Ch` | RDDCOLMOD | read 1+1 | Reads back `VIPF.2-0` / `IFPF.2-0` | 159 |
| `0Dh` | RDDIM | read 1+1 | Image mode: `VSSON`, `INVON` | 160 |
| `0Eh` | RDDSM | read 1+1 | Signal mode: `TEON`, `TELOM` | 160 |
| `0Fh` | RDBST | read 1+1 | Busy status, bit `RDY` | 161 |
| `10h` | **SLPIN** | 0 | Sleep in — see §5 | 161 |
| `11h` | **SLPOUT** | 0 | Sleep out — see §5 | 163 |
| `12h` | NOROFF | 0 | Normal (full-screen) mode off → partial | 164 |
| `13h` | NORON | 0 | Normal (full-screen) mode on | 166 |
| `20h` | **INVOFF** | 0 | Display inversion off | 166 |
| `21h` | **INVON** | 0 | Display inversion on. **This board's table sends it** **[SRC]** | 168 |
| `28h` | **DISPOFF** | 0 | Display off (GRAM retained, output blanked) | 169 |
| `29h` | **DISPON** | 0 | Display on | 171 |
| `2Ah` | **CASET** | **4** | Column address: `XS[8:0]`, `XE[8:0]` as 2 × 16-bit BE. Default `XS=0000h, XE=0167h` (=359) | 172 |
| `2Bh` | **RASET** | **4** | Row address: `YS[8:0]`, `YE[8:0]`. HW-reset default `XE=0167h`; SW-reset default is `0185h` (=389) when `MV=1` | 173 |
| `2Ch` | **RAMWR** | n | Memory write. **Resets column counter to `XS` and row counter to `YS`** | 175 |
| `2Eh` | RAMRD | 1 dummy + n | Memory read | 176 |
| `33h` | VSCRDEF | 6 | Vertical scrolling definition: `TFA[8:0]`, `VSA[8:0]`, `BFA[8:0]`. **Must sum to 390** | 177 |
| `34h` | **TEOFF** | 0 | Tearing-effect line off | 179 |
| `35h` | **TEON** | **1** | TE line on. `D0 = TE_MD`: `0` = V-blank only, `1` = V-blank **and** H-blank | 181 |
| `36h` | **MADCTL** | **1** | Memory data access control — §4.2 | 182 |
| `37h` | VSCSAD | 2 | Vertical scroll start address `VSP[8:0]` | 185 |
| `38h` | IDMOFF | 0 | Idle mode off (back to 262K colours) | 186 |
| `39h` | IDMON | 0 | Idle mode on — **8 colours**, RGB=(1,1,1). Low power | 187 |
| `3Ah` | **COLMOD** | **1** | Interface pixel format — §6 | 190 |
| `3Ch` | **RAMWRC** | n | **Memory write continue** — appends without resetting the address counters | 191 |
| `3Eh` | RDMEMC | 1 dummy + n | Memory read continue | 193 |
| `43h` | HSCRDEF | 6 | Horizontal scrolling definition: `LFA`, `HSA`, `RFA` | 195 |
| `44h` | **TESLWR** | **2** | Write tear scanline `N[11:0]` | 197 |
| `45h` | TESLRD | read 2 | Read tear scanline | 199 |
| `47h` | HSCSAD | 2 | Horizontal scroll start address `HSP[8:0]` | 200 |
| `4Ch` | RAMCLACT | 1 | Memory clear act, bit `FILLEN` | 201 |
| `4Dh`/`4Eh`/`4Fh` | RAMCLSETR/G/B | 1 ea | Memory-clear fill colour, `R/G/B[5:0]` in `D7-D2` | 202–203 |
| `50h` | CDCCTR | 1 | CDC control: `CDC_EN`, `CDC_COMP_EN`, `CDC_COMP_M`, `CDC_SIDE_M`, `CDC_NOTCH1/2_EN` | 204 |
| `51h` | **WRDISBV** | **1** | **Write display brightness** `DBV[7:0]`. `00h` = lowest, `FFh` = highest. Default `00h` | 204 |
| `52h` | RDDISBV | read 1+1 | Read display brightness | 206 |
| `53h` | **WRCTRLD** | **1** | Write CTRL display. **Bit `D2 = BL`** — brightness-control block enable | 207 |
| `54h` | RDCTRLD | read 1+1 | Read CTRL display | 208 |
| `DAh`/`DBh`/`DCh` | RDID1/2/3 | read 1 ea | Individual ID bytes, from OTP | 212–213 |

> **`51h`/`53h` do not drive a backlight.** They drive the ST77916's internal **brightness-control block** **[DOC]** §9.7 p.133, which modulates the panel drive. On this board the *actual* backlight is a discrete PWM on GPIO47 through an AO3400A **[SCH]**, entirely outside the controller — see [README §4](README.md#4-exact-wiring-on-this-board). Setting `51h` will not light a dark screen.

### 1.3 Command Table 2 — extended, gated behind `F0h`/`F1h`

**[DOC]** §13.3, pp.214–263. Reachable only after the Command2 unlock (§1.1). Summarised, because you should not be hand-writing these — see §3.4.

| Range | Registers | Purpose |
|---|---|---|
| `B0h`–`BDh` | VRHPS, VRHNS, VCOMS, STEP14S, STEP23S, SBSTS, TCONS, RGBVBP, RGBHBP, RGBSET | Source voltage rails, VCOM/GND, boost steps, TCON, RGB-interface porches |
| `C0h`–`C5h` | FRCTRA1-3 (normal), FRCTRB1-3 (idle) | Frame-rate control |
| `C6h`–`CBh` | PWRCTRA1-3 (normal), PWRCTRB1-3 (idle) | Power control |
| `CFh` | **DSTBDSLP** | Deep standby / deep sleep — §5.4 |
| `D0h`–`D2h` | **RESSET1/2/3** | **Resolution set.** This is where 360 × 390 gets retargeted to 360 × 360 |
| `DDh`/`DEh` | VCMOFSET, VCMOFNSET | VCOM offset |
| `E0h`/`E1h` | **GAMCTRP1 / GAMCTRN1** | Positive / negative gamma, **14 parameters each** — the Sitronix signature noted in [README §2.2](README.md#22-they-are-not-in-contradiction-and-here-is-why) |

---

## 2. The QSPI wire protocol

### 2.1 Frame structure

**[DOC]** §8.8.5.1 *Command write mode*, p.69:

> *"host needs to send 1 byte of write command instruction (0x02、0xA2、0x32 or 0x38). Then host sends 3 bytes of AD[23:0] which is composed of 1 byte of 0x00, 1 byte of command address and 1 byte of 0x00. After host sending instruction and AD[23:0], the following data is parameter (are parameters). When the last bit of parameter has been sent, CSX pin should be returned "H" level."*

So every transaction is:

```
 CS falls
 ┌────────────┬──────────────────────────────┬─────────────────────┐
 │ Instruction│         AD[23:0]             │  parameters / pixels│
 │   1 byte   │  0x00 │ command │ 0x00       │       n bytes       │
 │  1 lane    │        1 lane                │  1 / 2 / 4 lanes    │
 └────────────┴──────────────────────────────┴─────────────────────┘
 CS rises
```

**Instruction byte = 8 bits. Address phase = 24 bits. Total header = 32 bits.**

### 2.2 ⭐ Why `lcd_cmd_bits = 32`

This is the whole answer, and it is a direct consequence of §2.1 **[DOC]** p.69 + **[SRC]**.

ESP-IDF's `esp_lcd_panel_io_spi` emits `lcd_cmd_bits` of "command" before the parameter payload. The ST77916 needs a **32-bit** header (8-bit instruction + 24-bit address), not an 8-bit one. So the driver packs the entire header into the command field:

```c
#define LCD_OPCODE_WRITE_CMD    (0x02ULL)
#define LCD_OPCODE_READ_CMD     (0x03ULL)   // unused — and wrong, see §2.4
#define LCD_OPCODE_WRITE_COLOR  (0x32ULL)

lcd_cmd &= 0xff;                            // keep the 8-bit DCS opcode
lcd_cmd <<= 8;                              // → bits 15..8
lcd_cmd |= LCD_OPCODE_WRITE_CMD << 24;      // → bits 31..24
```

The resulting 32-bit word, sent MSB-first, is byte-wise:

| Byte | Value | Role |
|---|---|---|
| 0 | `0x02` | Instruction — "write command, 1-lane payload" |
| 1 | `0x00` | `AD[23:16]` |
| 2 | `cmd` | `AD[15:8]` — **the actual DCS opcode lives here** |
| 3 | `0x00` | `AD[7:0]` |

That is *exactly* the spec's `AD[23:0] = {0x00, command, 0x00}`. **The driver's framing is correct for the ST77916.** **[DOC]** p.69 **[SRC]**

`lcd_param_bits` stays at **8** because parameters are plain bytes. `dc_gpio_num = -1` because **there is no D/C pin in QSPI mode** — the command/data distinction is carried entirely by the *instruction byte* (`0x02` vs `0x32`), which is the point of the scheme.

### 2.3 Instruction opcodes and lane usage

**[DOC]** §8.8.5.1 p.69–70, §8.8.5.3 p.71–72.

| Opcode | Mnemonic | Header lanes | Payload lanes | Use |
|---|---|---|---|---|
| **`0x02`** | PP | 1 (`SDA0`) | **1** | Write command + parameters. Slow, but parameters are tiny |
| `0xA2` | PP2O | 1 | **2** (`SDA0`,`SDA1`) | Dual-lane pixel write |
| **`0x32`** | PP4O | 1 | **4** (`SDA0`–`SDA3`) | **Quad pixel write.** Address is still `{00, 2C, 00}` |
| `0x38` | PP4O | 1 | **4** | Quad pixel write, but `AD[23:0]` is a **real 24-bit RAM address** (`A23..A0` striped across all four lanes), not `{00, cmd, 00}` |
| **`0x0B`** | FASTREAD | 1 | 1 | **Read.** Followed by **8 dummy bits** before data — §2.4 |

**Command phase vs. RAM-write phase, concretely:**

| | Command phase | RAM-write phase |
|---|---|---|
| Instruction | `0x02` | `0x32` |
| Address | `{00h, opcode, 00h}` | `{00h, 2Ch, 00h}` for RAMWR, `{00h, 3Ch, 00h}` for RAMWRC |
| Payload lanes | 1 | 4 |
| Payload | parameter bytes | pixel stream |
| ESP-IDF call | `esp_lcd_panel_io_tx_param()` | `esp_lcd_panel_io_tx_color()` |

Note the spec's own diagrams label the quad address field `0x002C00 / 0x003C00` **[DOC]** p.71 — i.e. the spec explicitly anticipates both `RAMWR` and `RAMWRC` under the `0x32` opcode. **Use `3Ch` RAMWRC for continuation bursts within one window** to avoid the counter reset that `2Ch` forces (§3.3).

### 2.4 ⚠ Dummy cycles, and why reads fail on this board

**[DOC]** §8.8.5.2, p.70:

> *"host needs to send 1 byte of write command instruction (0x0B). Then host sends 3 bytes of AD[23:0] ... After host sending read command and AD[23:0], the following output data is command address parameter."*

The diagram is labelled: **`FASTREAD 0x0B` → `CMD : 0x00XX00` → `8 Dummy Bits` → `P0 : 0xXX`**.

So a QSPI read is **8-bit instruction `0x0B` + 24-bit address + 8 dummy bits + data**. There are **no dummy cycles on the write path** — writes go instruction → address → data with no gap. **[DOC]** p.69.

Two independent reasons the [README §7](README.md#7-how-to-settle-the-controller-identity-empirically) ID-read recipe will not work as written:

1. **Wrong opcode.** It uses `0x03`. The ST77916 QSPI read instruction is **`0x0B`** **[DOC]** p.70. `0x03` is the SPI-NOR *slow read* opcode and is what `esp_lcd_sh8601.c` inherited from its SH8601 ancestry — it is a genuine chip-specific difference, not a generic convention. **[INF]**
2. **Wrong clock.** **[DOC]** p.39 Table 5:

   | Symbol | Parameter | Min | Implies |
   |---|---|---:|---|
   | `TSCYCW` | Serial clock cycle (**Write**) | **16 ns** | ≤ 62.5 MHz |
   | `TSCYCR` | Serial clock cycle (**Read**) | **150 ns** | **≤ 6.67 MHz** |
   | `TCSS` | CS setup (write / read) | 15 / **60** ns | |
   | `TSCC` | CS hold (read) | **65 ns** | |
   | `TACC` | Access time | 10–50 ns | max `CL` = 30 pF |

   The board runs the bus at **40 MHz** **[SRC]**, which is comfortably legal for writes and **6× over the read limit**. A read at 40 MHz is not merely marginal, it is far outside the datasheet.

**Corrected recipe** **[INF]**, for anyone attempting [README §9's](README.md#9-open-questions) open question:

```c
// 1. Drop the bus to ≤ 6.67 MHz first — reads only.
// 2. Use instruction 0x0B, not 0x03.
// 3. Command Table 2 registers additionally need F4h (SPIOR) toggled around the read.
uint8_t id[4] = {0};
esp_lcd_panel_io_rx_param(amoled_panel_io_handle,
                          (0x0BULL << 24) | (0x04ULL << 8),   // FASTREAD + RDDID
                          id, sizeof(id));
```

`esp_lcd_panel_io_spi` handles the dummy bits via its own `dummy_bits` accounting; if it does not, the first returned byte is the dummy and `id[1..3]` are `ID1`/`ID2`/`ID3`. Note that **`RDDID` returns a dummy byte first even on the parallel bus** **[DOC]** p.146, so there are potentially *two* things to skip. Empirical work required.

### 2.5 Reading Command Table 2 needs `F4h`

**[DOC]** p.145. `SPIOR (F4h)` gates SPI read access to the extended bank, and it is a **toggle**:

```
Write F4h (enable) → Read cmd → Write F4h (disable)
Write F4h (enable) → Read cmd 1 → Read cmd 2 → Write F4h (disable)
```

Both forms are given as valid by the spec. Command Table 1 reads (`04h`, `09h`, `0Ah`…) do **not** need this.

### 2.6 Reconciling the community numbers

| Claim | Verdict |
|---|---|
| **40 MHz QSPI** **[COM]** / **[SRC]** | ✅ Legal for writes (limit 62.5 MHz). ❌ Illegal for reads (limit 6.67 MHz) **[DOC]** p.39 |
| **32-bit commands** **[COM]** / **[SRC]** | ✅ **Correct and required.** 8-bit instruction + 24-bit address = 32 **[DOC]** p.69. §2.2 |
| `0x02`/`0x32` opcode framing is generic across QSPI panels **[COM]**, per [README §2.2](README.md#22-they-are-not-in-contradiction-and-here-is-why) | ✅ Confirmed — the ST77916 uses exactly these values, which is why the SH8601 shim works unmodified |
| `0x03` read opcode is generic **[COM]** | ❌ **False for this part.** §2.4 |

---

## 3. Initialization

### 3.1 Power-on ordering

**[DOC]** §10.2, p.136.

- **`VDDI` and `VDD` may be applied in any order.** There is no mandated rail sequence, and *"there will be no damage to the display module if the power sequences are not met."*
- `CSX` may be applied at any time, or **permanently grounded**. `RESX` has priority over `CSX`.
- ⚠ *"If RESX line is not held stable by host during Power On Sequence ... then it will be necessary to apply a Hardware Reset (RESX) after Host Power On Sequence is complete to ensure correct operation. Otherwise function is not guaranteed."* — **[DOC]** p.136 Note 4. On this board `RESX` is on GPIO21 and the driver always pulses it, so this is satisfied **[SRC]**.
- **Power-down:** if in Sleep Out, rails must stay up **≥ 120 ms** after `RESX` is released. If in Sleep In, **0 ms**.

### 3.2 Reset timing

**[DOC]** §7.4.7, pp.42–43.

| Symbol | Parameter | Min | Max |
|---|---|---:|---:|
| `TRW` | Reset pulse duration | **10 µs** | – |
| `TRT` | Reset cancel (applied during **Sleep In**) | – | **5 ms** |
| `TRT` | Reset cancel (applied during **Sleep Out**) | – | **120 ms** |

Spike rejection **[DOC]** p.43:

| `RESX` pulse | Action |
|---|---|
| Shorter than 5 µs | **Reset rejected** |
| Between 5 µs and 9 µs | Reset starts |
| Longer than 9 µs | **Reset** |

Two mandatory post-reset waits, quoted **[DOC]** p.43 Note 7:

> *"It is necessary to wait 5msec after releasing RESX before sending commands. Also Sleep Out command cannot be sent for 120msec."*

And **[DOC]** p.42 Note 1: the reset-cancel window covers **loading ID bytes, VCOM setting and other settings from NVM into registers**, and this NVM load happens on every hardware-reset cancel. **This is why you cannot shorten the post-reset delay** — you would be issuing commands while the OTP is still being shadowed into the register file.

**Versus the driver** **[SRC]**: `panel_sh8601_reset()` does `RST low → 10 ms → RST high → 150 ms`.

| | Spec requires | Driver does | |
|---|---|---|---|
| Pulse width | ≥ 10 µs | **10 ms** | ✅ 1000× margin |
| Before any command | ≥ 5 ms | 150 ms | ✅ |
| Before `SLPOUT` | ≥ 120 ms | 150 ms | ✅ 30 ms margin |

[README §5.1's](README.md#51-reset-timing) "do not shorten the 150 ms" is **confirmed by the spec** — 120 ms of it is a hard requirement, and the margin above it is thin.

The software fallback path (`SWRESET` + 80 ms, used when no reset GPIO is configured) is **not spec-compliant**: `SWRESET` from Sleep Out also needs 120 ms **[DOC]** p.153/p.163. On this board the hardware path is always taken, so it does not bite **[SRC]**.

### 3.3 Sleep-out delay

**[DOC]** §SLPOUT p.163 — the restrictions are symmetric and both matter:

- **≥ 5 ms** after `SLPOUT` before sending *any* new command — *"to allow time for the supply voltages and clock circuits to stabilize."*
- **≥ 120 ms** after `SLPOUT` before sending `SLPIN`.
- *"The display module runs the self-diagnostic functions after this command is received."*

`SLPIN` (`10h`) has the mirror-image restriction **[DOC]** p.161: ≥ 5 ms before new commands, ≥ 120 ms before the opposite transition.

**Versus the driver** **[SRC]**: the vendor table entry is `{0x11, …, 120}` — a **120 ms** delay after `SLPOUT`. That satisfies the 5 ms command-gap requirement with enormous margin and pre-pays the 120 ms `SLPIN` guard. [README §5.3 item 3](README.md#53--init-table-gotchas) calls this "load-bearing"; the spec's *literal* minimum before the next command is only 5 ms, but 120 ms is the correct conservative value because the 120 ms figure governs the mode transition itself. **Do not reduce it to 5 ms.** **[INF]**

### 3.4 What must precede `DISPON`

The spec does not publish a single canonical init script — that is deliberate, because gamma/VCOM/GIP values are **glass-specific** and Sitronix expects the module house to supply them (which is exactly [README §2.4 item 3's](README.md#24-what-a-developer-should-actually-do) point). What the spec *does* constrain, in order **[DOC]** pp.42–43, 136, 141–145, 163, 190:

1. **Power rails up** (any order), `RESX` held stable.
2. **Hardware reset** — `RESX` low ≥ 10 µs, then high.
3. **Wait ≥ 5 ms** — NVM/OTP shadow load completes.
4. **Unlock** the banks you need (`F0h`/`F1h`/`F2h`/`F3h`, §1.1).
5. **Write Command Table 2**: resolution (`D0h`–`D2h`), power (`C6h`–`CBh`), frame rate (`C0h`–`C5h`), VCOM (`B2h`, `DDh`, `DEh`), TCON (`BAh`), GIP page, gamma (`E0h`/`E1h`).
6. **Relock** (`F0h = 00h`).
7. **`COLMOD` (`3Ah`)** — §6. Must be set before the first `RAMWR`; power-on default is 18 bpp, not 16.
8. **`MADCTL` (`36h`)** — §4.2.
9. **`INVON`/`INVOFF`**, `TEON` if used.
10. **`SLPOUT` (`11h`)**, then **wait ≥ 120 ms** (spec minimum before `SLPIN`; ≥ 5 ms before other commands).
11. **`DISPON` (`29h`)**.

The vendor's ~190-entry table follows exactly this shape **[SRC]**, which is corroborating evidence for the ST77916 identification in [README §2.3](README.md#23-conclusion).

> **`DISPON` ordering is not enforced by the chip.** Nothing stops you sending `29h` before `11h`; you will simply get a blank or garbage panel because the DC/DC converter and oscillator are still stopped **[DOC]** p.163. The 120 ms is the real gate.

---

## 4. RAM addressing

### 4.1 GRAM organisation

**[DOC]** §9.1, pp.117–119.

| Property | Value |
|---|---|
| Size | **360 × 390 × 18 bits = 2,527,200 bits** (~308 KB) |
| Organisation | Static RAM, `360 × RGB × 390`, 18 bpp (262K colours) |
| Address range | `X = 0 … 359` (`0167h`), `Y = 0 … 389` (`0185h`). **"Addresses outside these ranges are not allowed"** |
| Source outputs | Mapped `0 … 1079` (= 360 × 3) **[DOC]** p.118 |
| Source driver channels | **540 RGB channels** **[DOC]** p.8 |
| Concurrency | *"There will be no abnormal visible effect on the display when there is a simultaneous Panel Read and Interface Read or Write to the same location of the Frame Memory"* — no host-side tearing mitigation needed for *access conflicts*, only for *visual* tearing (§5) |

Address-counter behaviour **[DOC]** p.119:

| Condition | Column counter | Row counter |
|---|---|---|
| **`RAMWR`/`RAMRD` accepted** | **Return to `XS`** | **Return to `YS`** |
| Complete pixel read/write | Increment by 1 | No change |
| Column counter > `XE` | Return to `XS` | Increment by 1 |
| Column > `XE` **and** row > `YE` | Return to `XS` | Return to `YS` |

Horizontal addressing (`MV=0`) increments X and wraps to the next row; vertical addressing (`MV=1`) increments Y and wraps to the next column. Note the **`MV` flag also swaps the legal `XE` bound**: `XE ≤ 359` when `MV=0`, `XE ≤ 389` when `MV=1` **[DOC]** p.172.

Because `RAMWR` resets *both* counters, a multi-chunk flush into one window must use **`RAMWRC` (`3Ch`)** for chunks 2..n. `esp_lcd_sh8601.c` issues `CASET`/`RASET`/`RAMWR` per `draw_bitmap` call **[SRC]**, which is correct for LVGL's one-call-per-area model, but if you hand-roll a chunked DMA path, `2Ch` on every chunk will overwrite the top-left corner repeatedly.

### 4.2 `MADCTL` (`36h`) bit map

**[DOC]** pp.182–184. Power-on and hardware-reset default `00h`; **`SWRESET` does not change it**.

| Bit | Name | `0` | `1` |
|---:|---|---|---|
| `D7` | **MY** — Page Address Order | Top → Bottom | Bottom → Top |
| `D6` | **MX** — Column Address Order | Left → Right | Right → Left |
| `D5` | **MV** — Page/Column Order | Normal | **Reverse (X/Y exchange)** |
| `D4` | **ML** — Line Address Order | Refresh top → bottom | Refresh bottom → top |
| `D3` | **RGB** — colour order | **RGB** | **BGR** |
| `D2` | **MH** — Display Data Latch Order | Refresh left → right | Refresh right → left |
| `D1` | **HSD** — Horizontal Scroll Address Order | | |
| `D0` | — | reserved | |

The eight `MV`/`MX`/`MY` combinations and their host→DDRAM image transforms are tabulated at **[DOC]** p.120.

> ⚠ **[DOC]** p.119: *"When MX, MY and MV will be changed the data **must** be rewritten to the display RAM."* Rotating at runtime by rewriting `36h` alone leaves stale, mis-transformed GRAM contents. Redraw the full screen after any `MADCTL` change. This is an additional constraint on top of the touch-transform coupling in [README §5.3 item 6](README.md#53--init-table-gotchas).

The board's values: `00h` (normal) and `60h` = `MX|MV` (X/Y exchange + X mirror = 90° rotation) **[SRC]**.

### 4.3 ⚠ The 2-pixel rounding constraint — and what the spec does *not* say

[README §4.3](README.md#43-the-rounder_cb--a-real-constraint-easy-to-miss) documents the LVGL `rounder_cb` that snaps flush areas to even-start / odd-end, i.e. a 2-pixel grid.

**The spec does not document this.** `CASET`'s stated restriction is only **[DOC]** p.172:

> *"(Parameter range: 0 < XS [8:0] < XE [8:0] < 359 (0167h)): MV="0")"*

No alignment, no parity requirement, on either `CASET` or `RASET`. I looked; it is not there. **So where does it come from?**

**Most likely explanation [INF] — source-driver multiplexing.** The features list says **540 source channels** **[DOC]** p.8, while the memory-to-display map runs source outputs **0…1079** **[DOC]** p.118. 1080 / 540 = **2**. The panel is driven with **1:2 source multiplexing** — one physical source amplifier time-shares two adjacent columns per line. A column pair is therefore the atomic unit the analogue front end can refresh, and a window that starts or ends mid-pair cannot be driven independently. Combined with the declared **"1/2/4-dot Inversion, Column Inversion"** driving algorithms **[DOC]** p.8, which also operate on column groups, an even/odd window boundary is exactly the kind of thing that produces the "skewed or shifted output" the README warns about.

**Secondary contributor [INF] — quad-lane pixel packing.** The `0x32` RGB565 quad diagrams **[DOC]** p.71 lay out `1st pixel` and `2nd pixel` as an adjacent pair across `SDA0`–`SDA3`, and the RGB666 quad format **[DOC]** p.72 stripes a single pixel across all four lanes with padding bits. Odd pixel counts leave a partial group. This is a weaker argument than the multiplexing one — a 16-bit pixel is a whole number of quad nibbles — but it reinforces the same alignment.

**Practical guidance, unchanged:** keep the `rounder_cb`. In LVGL 9 the equivalent hook is `lv_display_add_event_cb(disp, …, LV_EVENT_INVALIDATE_AREA, …)`. The constraint is real, it is observable, and the spec's silence is a documentation gap rather than a licence to drop it. **[INF]**

### 4.4 Vertical scroll

**[DOC]** §9.4, pp.122–123. `VSCRDEF (33h)` sets `TFA` (top fixed area), `VSA` (scroll area), `BFA` (bottom fixed area); `VSCSAD (37h)` sets the start address.

> ⚠ **[DOC]** p.123: *"Do not set TFA + VSA + BFA ≠ Panel total scan lines. In that case, unexpected picture will be shown."*

On a panel retargeted to 360 rows via `RESSET`, the sum must match the **configured** scan-line count, not the die's 390. Untested on this board. **[INF]**

---

## 5. Tearing effect

### 5.1 What the controller provides

**[DOC]** §9.5, pp.124–127.

| Mode | `TEON` (`35h`) param `TE_MD` | TE output content |
|---|---|---|
| Mode 1 | `0` (default) | **V-blanking only** |
| Mode 2 | `1` | **V-blanking and H-blanking** — one V-sync and **390 H-sync pulses per field** |

TE AC characteristics at 60 Hz, Idle Mode Off, Ta = 25 °C **[DOC]** p.125:

| Symbol | Parameter | Min | Max |
|---|---|---:|---:|
| `tvdl` | Vertical timing **low** duration (display *is* being updated from GRAM) | **13 ms** | – |
| `tvdh` | Vertical timing **high** duration (display *not* updated — **the safe window**) | **1000 µs** | – |
| `thdl` | Horizontal timing low duration | 16 µs | – |
| `thdh` | Horizontal timing high duration | – | 500 µs |

Rise/fall times ≤ 15 ns. Timings hold for both `ML=0` and `ML=1` **[DOC]** p.125.

> **[DOC]** p.124: *"During Sleep In Mode, the Tearing Output Pin is active Low."* Useful as a crude sleep-state probe — if you had the pin.

The spec gives two worked synchronisation strategies **[DOC]** pp.126–127: if the **MPU write is faster** than the panel read, write during the V-sync pulse so data stays ahead of the scan; if the MPU write is **slower**, begin writing just *after* one horizontal sync pulse so the write trails the read pointer and completes before the pointer catches up on the next frame.

### 5.2 ⚠ What you lose on this board

`LCD_TE` reaches panel connector `U5` pin 23 but **is not assigned to any ESP32-S3 GPIO** — established in [README §4.2](README.md#42--no-tearing-effect-line) **[SCH]**. Consequently:

| Capability | Status on this board |
|---|---|
| `TEON` (`35h`) / `TEOFF` (`34h`) | ✅ Still *sendable*. The controller will happily drive the pin |
| `TESLWR` (`44h`) set-tear-scanline | ✅ Sendable, and the driver's SH8601 default table even sends `{0x44, {0x01, 0xD1}}` **[SRC]** |
| Reading TE state via `RDDSM` (`0Eh`) bits `TEON`/`TELOM` | ✅ Possible in principle — but see §2.4, reads are broken at 40 MHz |
| **Actually synchronising a flush to V-blank** | ❌ **No.** No electrical path to the MCU |
| The 1000 µs `tvdh` safe window | ❌ Unobservable |
| LVGL `DIRECT`/`FULL` render mode with VSync | ❌ Use `PARTIAL` with the vendor's two-buffer scheme |

**[INF]** The spec's own advice reinforces the README's mitigation: with a 13 ms minimum `tvdl` and only a 1 ms `tvdh`, the safe write window is **under 8 % of the frame period**. Even *with* a TE line you could not blind-guess it by timing. Without one, the only real mitigation is keeping redraw regions small so that any given flush finishes well inside one scan pass — exactly what [README §4.2](README.md#42--no-tearing-effect-line) concludes.

---

## 6. Colour formats

### 6.1 `COLMOD` (`3Ah`)

**[DOC]** p.190. One parameter. Note the spec's own section heading typos it as "MOLMOD"; the register table says `COLMOD`.

| Bits | Field | Values |
|---|---|---|
| `D7` | – | Set to `0` |
| `D6-D4` | **`VIPF.2-0`** — RGB *interface* colour format | `101` = 65K, `110` = 262K |
| `D3` | – | Set to `0` |
| `D2-D0` | **`IFPF.2-0`** — *control interface* colour format | `101` = **16 bit/pixel**, `110` = **18 bit/pixel** |

| Value | Meaning | Notes |
|---|---|---|
| **`55h`** | 16 bpp both fields — **RGB565** | What this board uses **[SRC]** |
| **`66h`** | 18 bpp both fields — **RGB666** | **Power-on and hardware-reset default** |
| `05h` | 16 bpp control interface only | Referenced throughout §8.8 as `3Ah="05h"` |
| `06h` | 18 bpp control interface only | Referenced as `3Ah="06h"` |

**Defaults** **[DOC]** p.190: Power-on = 18 bit/pixel. `SWRESET` = **no change**. Hardware reset = 18 bit/pixel. So **you must always send `COLMOD` explicitly** — a hardware-reset chip is in RGB666, and streaming RGB565 at it produces the classic diagonal-smear symptom.

> ⚠ **[DOC]** p.190 Note 2, and this one is easy to miss: *"The Command 3Ah should be set at 55h when writing 16-bit/pixel data into frame memory, but **3Ah should be re-set to 66h when reading pixel data from frame memory**."* Read-back of GRAM via `RAMRD`/`RDMEMC` is **always 18 bpp**. If you ever implement a GRAM read, you must flip `COLMOD` to `66h` first and back to `55h` afterwards.

**[DOC]** p.190 Note 1: in both 16 and 18 bpp modes a **LUT** is applied when transferring into the frame memory — the GRAM itself is always 18 bits deep (§4.1), so RGB565 is expanded on the way in.

### 6.2 RGB888?

**There is no RGB888 / 24-bit mode.** **[DOC]** p.8, p.190. The features list gives exactly two programmable pixel formats — `16-bit/pixel RGB(565) 65K` and `18-bit/pixel RGB(666) 262K` — and the GRAM is 18 bits deep. The display's maximum is **262K colours**.

⚠ This **corrects [README §3](README.md#3-capabilities-and-limits)**, whose capability table lists *"RGB565 (16 bpp), RGB666 (18 bpp), RGB888 (24 bpp), selected by COLMOD"*. **RGB888 is not supported by this controller.** `bits_per_pixel = 24` passed to `esp_lcd_new_panel_sh8601()` would produce an invalid `COLMOD` value.

### 6.3 Colour depth vs. mode

| Mode | Colours | Set by |
|---|---|---|
| Idle Mode **Off** (normal) | **262,144** — RGB(6,6,6) | `IDMOFF` (`38h`) |
| Idle Mode **On** | **8** — RGB(1,1,1) | `IDMON` (`39h`) |

**[DOC]** p.8, p.187. Idle mode is a power feature (§7), not a colour feature you would choose deliberately.

### 6.4 Byte order on the wire

The quad-lane bit layouts are fully specified at **[DOC]** pp.71–72 for both RGB565 and RGB666, for each of the four write opcodes. For the `0x32` RGB565 case the bits are striped across lanes as `SDA0:{R1,G3,B4,B0}`, `SDA1:{R2,G4,G0,B1}`, `SDA2:{R3,G5,G1,B2}`, `SDA3:{R4,R0,G2,B3}` per pixel — **the ESP32 QSPI peripheral produces this layout automatically** from a byte stream; you do not construct it by hand. The only host-visible choice is byte order, which `rgb_ele_order` and LVGL's `LV_COLOR_16_SWAP` control **[SRC]**.

---

## 7. Power and sleep modes

### 7.1 The six power levels

**[DOC]** §10.1, p.135, ordered maximum → minimum consumption:

| # | Mode | Description | Entered by |
|---:|---|---|---|
| 1 | Normal On, Idle Off, Sleep Out | Full display, max 262,144 colours | `NORON` + `IDMOFF` + `SLPOUT` |
| 2 | Normal Off, Idle Off, Sleep Out | **Partial** display, 262,144 colours | `NOROFF` |
| 3 | Normal On, Idle On, Sleep Out | Full display, **8 colours** | `IDMON` |
| 4 | Normal Off, Idle On, Sleep Out | Partial display, 8 colours | `NOROFF` + `IDMON` |
| 5 | **Sleep In** | DC/DC converter, internal oscillator and panel driver **stopped**. Only MCU interface + memory live, on `VDDI`. **GRAM contents safe** | `SLPIN` (`10h`) |
| 6 | Power Off | Both `VDD` and `VDDI` removed | — |

*"Transition between modes 1-5 is controllable by MCU commands. Mode 6 is entered only when both Power supplies are removed."* **[DOC]** p.135.

### 7.2 Current consumption

**[DOC]** §7.3, p.32. Conditions: `VDDI` = 1.8 V, `VDD` = 2.8 V, Ta = 25 °C, 60 Hz, IC default registers, colour picture.

| Mode | `IDDI` typ | `IDD` typ | `IDDI` max | `IDD` max |
|---|---:|---:|---:|---:|
| **Normal** | 0.001 mA | **8 mA** | 0.005 mA | **10 mA** |
| **Sleep-in** | 0.001 mA | **0.030 mA** | 0.005 mA | 0.150 mA |
| **Deep Standby** | 0.001 mA | **0.001 mA** | 0.005 mA | 0.005 mA |

**Implications for this board [INF]:**

- Normal-mode controller draw is **~8 mA**. This is *negligible* next to the backlight, which through an AO3400A at full PWM will be one to two orders of magnitude larger. **If you are optimising battery life, the backlight is the entire problem** — turning off GPIO47 saves far more than `SLPIN`.
- `SLPIN` drops the controller to **~30 µA**, a **~270×** reduction, and **preserves GRAM**. That makes it the right choice for a display-off-but-resumable state: `DISPOFF` → `SLPIN` → (backlight off), then `SLPOUT` + 120 ms → `DISPON` to restore without redrawing.
- Deep Standby reaches **~1 µA** but costs you the GRAM and a full re-init.

### 7.3 `SLPIN` / `SLPOUT` details

**[DOC]** pp.161–164.

`SLPIN` (`10h`), no parameters:
- Enters *minimum power consumption* mode. DC/DC stopped, internal oscillator stopped, panel scanning stopped.
- **MCU interface and memory keep working; memory keeps its contents.**
- Display is blanked automatically, and this is *"Automatic No effect to DISP ON/OFF Commands"* — i.e. the blanking is independent of `DISPON`/`DISPOFF` state, which is restored on wake **[DOC]** p.162 flow chart.
- Charge is drained from the LCD panel on entry.
- *"Dimming function does not work when there is changing mode from Sleep OUT to Sleep IN."*
- Can only be left by `SLPOUT` (`11h`).

Both directions: **wait 5 ms before any new command, 120 ms before the reverse transition** (§3.3).

Default state at power-on, `SWRESET` **and** hardware reset is **Sleep In** **[DOC]** p.162. `SLPOUT` is mandatory.

### 7.4 Deep Standby / Deep Sleep — `DSTBDSLP` (`CFh`)

**[DOC]** p.252. Command Table 2, so it needs the `F0h`/`F1h` unlock (§1.1). One parameter:

| Bit | Name | Effect |
|---|---|---|
| `D1` | `DSTB_EN` | `1` = **Deep Standby mode** |
| `D0` | `DSLP_EN` | `1` = **Deep Sleep In mode**, `0` = ordinary Sleep In |

Notes, quoted **[DOC]** p.252:

1. *"It will be necessary to stay at sleep in mode before enter deep sleep in mode if P80、SPI and QSPI is used."* — **must be in Sleep In first** on this board.
2. (MIPI: must be in ULPS first — not applicable here.)
3. *"No matter what status is, it is allowed to enter deep standby mode."*
4. ⚠ *"It will be necessary to set HWRST or **toggle CSX 7~8 times** to leave deep standby mode."*
5. *"It will be necessary to set HWRST or set DSLP_EN=0 to leave deep sleep in mode."*
6. *"It will be necessary to wait 10msec after set DSLP_EN=0 to leave deep sleep in mode before sending the other commands."*

**[INF]** Note 4 is the interesting one for an ESP32 design: **deep standby is escapable without a reset line**, by bit-banging `CS` 7–8 times. Since this board *does* have `RESX` on GPIO21, a hardware reset is simpler — but it costs a full ~190-command re-init. Given that the backlight dominates the power budget (§7.2), **`SLPIN` is almost certainly the right sleep state for this board and deep standby is not worth the re-init cost.** Neither is used by the vendor firmware **[SRC]**.

---

## 8. Spec vs. shipped driver — consolidated

| # | Topic | Spec **[DOC]** | `esp_lcd_sh8601` + Waveshare table **[SRC]** | Verdict |
|---:|---|---|---|---|
| 1 | Command framing | 8-bit instr + 24-bit addr = 32 bits, p.69 | `lcd_cmd_bits = 32`, `0x02<<24 \| cmd<<8` | ✅ **Exact match** |
| 2 | Write opcode | `0x02` 1-lane, `0x32` 4-lane, p.69 | `LCD_OPCODE_WRITE_CMD 0x02`, `LCD_OPCODE_WRITE_COLOR 0x32` | ✅ **Exact match** |
| 3 | **Read opcode** | **`0x0B` FASTREAD + 8 dummy bits**, p.70 | `LCD_OPCODE_READ_CMD 0x03` (defined, unused) | ❌ **Conflict.** Driver value is wrong for ST77916 |
| 4 | **Read clock** | `TSCYCR` ≥ 150 ns → **≤ 6.67 MHz**, p.39 | Bus at 40 MHz | ❌ **Conflict.** Reads out of spec by 6× |
| 5 | Write clock | `TSCYCW` ≥ 16 ns → ≤ 62.5 MHz, p.39 | 40 MHz | ✅ Legal, 36 % margin |
| 6 | Reset pulse | ≥ 10 µs, p.42 | 10 ms | ✅ Over-satisfied |
| 7 | Post-reset delay | ≥ 5 ms; ≥ 120 ms before `SLPOUT`, p.43 | 150 ms | ✅ Satisfied, 30 ms margin |
| 8 | SW-reset fallback | `SWRESET` needs 120 ms from Sleep Out, p.153 | `SWRESET` + 80 ms | ⚠ **Non-compliant**, but unreachable on this board (RST is wired) |
| 9 | `SLPOUT` delay | ≥ 5 ms next cmd, ≥ 120 ms reverse, p.163 | 120 ms | ✅ Conservative and correct |
| 10 | `COLMOD` default | **18 bpp** after power-on/HW reset, p.190 | Driver always sends `3Ah` from `bits_per_pixel` | ✅ Correct — and necessary |
| 11 | **RGB888** | **Not supported.** 16 or 18 bpp only, p.8/p.190 | — | ❌ **[README §3](README.md#3-capabilities-and-limits) is wrong.** Corrected in §6.2 |
| 12 | **Resolution** | **360 × 390** die; GRAM 360×390×18, p.7/p.117 | 360 × 360 via `RESSET1-3` | ⚠ **Apparent conflict, resolved.** Board retargets a taller die |
| 13 | Zero-param commands | `SLPOUT`/`DISPON` take **no** parameters, p.147 | Table sends `{0x11, {0x00}, 1, 120}` — 1 byte | ⚠ **Out of spec**, as [README §5.3 item 4](README.md#53--init-table-gotchas) says. The address phase already delimits the command; a stray byte lands in a don't-care parameter slot. Harmless in practice, still wrong |
| 14 | `MADCTL` after change | *"data must be rewritten to the display RAM"*, p.119 | Rotation set once at init | ✅ Fine at init; ⚠ a trap for runtime rotation. §4.2 |
| 15 | **2-pixel alignment** | **Not documented anywhere** | `rounder_cb` enforces it | ⚠ **Spec gap.** Real constraint, undocumented cause. Best explanation: 1:2 source mux (540 ch / 1080 outputs). §4.3 |
| 16 | `RAMWR` counter reset | `2Ch` resets both counters, p.119 | One `2Ch` per `draw_bitmap` | ✅ Correct for LVGL; ⚠ use `3Ch` if you chunk manually. §4.1 |
| 17 | Extended-cmd gating | `F0h`–`F3h` unlock matrix, p.142 | Table brackets banks with `F0`/`F1`/`F2`/`F3` | ✅ Consistent, and corroborates ST77916 identity |
| 18 | `51h`/`53h` brightness | Internal brightness block, p.133/204/207 | Board PWMs GPIO47 instead | ℹ Different mechanisms. Driver's SH8601 *default* table sends `53h`; Waveshare's override does not |
| 19 | TE line | Full TE support, `35h`/`34h`/`44h`, p.124 | `TE` not routed to MCU **[SCH]** | ⚠ **Hardware limitation**, not a driver bug. §5.2 |

### 8.1 What a developer should actually do

Extending [README §2.4](README.md#24-what-a-developer-should-actually-do) with what the spec adds:

1. **Keep using `esp_lcd_sh8601` with Waveshare's init table.** Rows 1, 2, 5, 6, 7, 9, 10, 16, 17 above show the transport layer and timing are all spec-correct. Nothing here changes the README's conclusion.
2. **Do not attempt register reads without fixing two things** — opcode `0x0B` and clock ≤ 6.67 MHz (§2.4). This is the concrete reason [README §9's](README.md#9-open-questions) ID question is still open, and it is now answerable.
3. **Never pass `bits_per_pixel = 24`.** There is no RGB888 mode (§6.2).
4. **Always send `COLMOD` explicitly.** Hardware-reset default is RGB666 (§6.1).
5. **Keep the 120 ms after `SLPOUT` and the 150 ms after reset.** Both are spec-backed (§3.2, §3.3).
6. **Keep the `rounder_cb`** (§4.3).
7. **If you rotate at runtime, redraw everything** (§4.2).
8. **For low power, kill the backlight first, then `SLPIN`** (§7.2). GRAM survives, so wake is cheap.
9. **If you chunk RAM writes yourself, use `RAMWRC` (`3Ch`) after the first chunk** (§4.1).

### 8.2 Which parts of the SH8601 command set are generic vs. chip-specific

This is the question [README §2.2](README.md#22-they-are-not-in-contradiction-and-here-is-why) answers from the code side; the spec now lets it be answered from the silicon side.

| `esp_lcd_sh8601.c` element | Generic or SH8601-specific? | Confirmed by ST77916 spec? |
|---|---|---|
| `0x02` write-command opcode | **Generic** QSPI-display convention | ✅ **[DOC]** p.69 — identical |
| `0x32` write-colour opcode | **Generic** | ✅ **[DOC]** p.69, p.71 — identical |
| 32-bit `{instr, 00, cmd, 00}` header | **Generic** | ✅ **[DOC]** p.69 — identical |
| `0x03` read opcode | ⚠ **SH8601-specific** | ❌ ST77916 uses `0x0B` **[DOC]** p.70 |
| `CASET`/`RASET`/`RAMWR` (`2Ah`/`2Bh`/`2Ch`) | **Generic** MIPI DCS | ✅ **[DOC]** pp.172–175 |
| `MADCTL` (`36h`), `COLMOD` (`3Ah`) | **Generic** DCS | ✅ **[DOC]** pp.182, 190 — same bit fields |
| `INVON`/`INVOFF`, `DISPON`/`DISPOFF`, `SLPIN`/`SLPOUT` | **Generic** DCS | ✅ **[DOC]** pp.161–171 |
| `TEON` (`35h`), `TESLWR` (`44h`) | **Generic** DCS | ✅ **[DOC]** pp.181, 197 |
| `vendor_specific_init_default[]` — `44h`/`35h`/`53h` | ⚠ **SH8601/AMOLED-specific** | Commands exist on ST77916, but `53h` drives a *different* mechanism and the table omits everything a TFT needs. **Overridden by Waveshare — correctly** |
| `reset` 10 ms/150 ms timing | **Generic**, conservative | ✅ Exceeds ST77916 minimums **[DOC]** p.43 |

**Summary:** everything the shim does *at runtime* is either a generic QSPI-display convention or a universal MIPI-DCS command, and all of it is confirmed by the ST77916 spec. The only genuinely SH8601-flavoured parts are the **unused `0x03` read opcode** and the **overridden default init table**. This is now a spec-backed confirmation of [README §2.3's](README.md#23-conclusion) conclusion rather than an inference from code shape alone.

---

## 9. Extraction notes

| Topic | Spec pages used |
|---|---|
| Contents, general description, features | 1–8 |
| Power consumption | 32 |
| QSPI AC characteristics | 39 |
| Reset timing + spike rejection | 42–43 |
| QSPI command write / read / colour format | 68–73 |
| Display data RAM, address control, MADCTL transforms | 117–121 |
| Vertical scroll | 122–123 |
| Tearing effect: modes, timings, worked examples | 124–128 |
| Power levels, power on/off sequence | 135–138 |
| Page Set Table (`F0h`–`F4h`) | 141–145 |
| Command Table 1 | 146–152 |
| `SLPIN` / `SLPOUT` | 161–164 |
| `CASET` / `RASET` / `RAMWR` | 172–176 |
| `TEON` | 181 |
| `MADCTL` | 182–184 |
| `COLMOD` | 190 |
| `WRDISBV` / `WRCTRLD` | 204–208 |
| `DSTBDSLP` | 252 |

**Not extracted** (out of scope for display code): pad arrangement and bump dimensions (pp.10–24), MIPI DSI protocol (pp.80–116), 8080 parallel and 3/4-line SPI interfaces (pp.44–67), RGB interface timing (pp.73–79), gamma voltage ladders (pp.128–134), NVM programming flow (p.139), layout resistance suggestions (p.140), Command Table 2 register-level detail (pp.214–263).

**Document metadata curiosity [INF]:** `pdfinfo` reports `Title: ST7796`, `Creator: Microsoft Word 2013`, author "Joseph". The ST77916 spec was written by editing the **ST7796** datasheet template. Every page footer also reads *"Preliminariy 0.1"* (sic) despite the cover saying V1.0. This is mild corroboration of [README §2.2's](README.md#22-they-are-not-in-contradiction-and-here-is-why) observation that ST77916 and ST7796 share register conventions — they literally share a source document — and a reminder that copied-and-edited documents carry copied-and-edited errors. Treat unusual values with suspicion and prefer the vendor's working init table over the datasheet where they disagree.

---

## See also

- [ST77916 component record](README.md) — identity, the SH8601 naming conflict, board wiring, libraries, open questions
- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — the device this controller ships in
- [SH8601 compatibility driver record](../../generic/sh8601-compatibility-driver/README.md) — the software artefact
- [Sitronix documentation-sourcing guide](../../../vendors/sitronix/README.md)

## Source

| Title | URL | Local artifact |
|---|---|---|
| **Sitronix ST77916 Specification V1.0** (2022/08, 264 pp.) | https://dl.espressif.com/AE/esp-iot-solution/ST77916_SPEC_V1.0.pdf | `artifacts/st77916-spec-v1.0.pdf` |
