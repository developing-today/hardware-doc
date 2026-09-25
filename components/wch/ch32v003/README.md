# WCH CH32V003

> Ultra-low-cost 32-bit RISC-V microcontroller, **RV32EC**, 48 MHz, 16 KB flash / 2 KB SRAM.
> Manufacturer: **WCH (Nanjing Qinheng Microelectronics)** · Research snapshot **2026-09-20**
> **Fitment established:** `badgeteam/konsool-zero` expansion board, designator **`U19`**,
> part **`CH32V003F4U6`** (QFN-20) — from the project's own KiCad schematic. See §8.

⚠ **This is not the CH32V203.** The Tanmatsu mainboard's coprocessor is a
[CH32V203C8T6](../ch32v203c8t6/README.md) — a *different part* with a different core
(`IMAC` vs `RV32EC`), 4× the flash and 10× the SRAM. The two are not source- or
pin-compatible. See §7.

## 1. Function and capabilities

| Property | Value | Evidence |
|---|---|---|
| Core | QingKe **V2A**, 32-bit RISC-V, **RV32EC** instruction set | DS V1.4 Features · `primary` |
| Max clock | **48 MHz** (SYSCLK/HCLK) | DS V1.4 Features; RM V1.6 §3.3.1 |
| Flash | **16 KB** CodeFlash | DS V1.4 model table |
| SRAM | **2 KB** | DS V1.4 model table |
| Other NVM | 1920 B bootloader · 64 B system config · 64 B user-defined | DS V1.4 Features |
| Supply | **3.3 V or 5 V** rated; **2.7–5.5 V** operating | DS V1.4 Features; RM V1.6 Fig 1-1 |
| Temperature | −40 to +85 °C (industrial) | DS V1.4 Overview |
| Interrupts | PFIC, hardware interrupt stack, **2-level nesting** | DS V1.4 Features |
| DMA | 1 controller, **7 channels**, ring-buffer capable | DS V1.4 Features |
| Debug | **1-wire serial debug (SDI)** on `SWIO` — *not* SWD, *not* JTAG | DS V1.4; RM V1.6 §18 — see §4 |
| Package (as fitted) | **QFN-20**, 3.0 × 3.0 mm, 0.4 mm pitch | DS V1.4 §4 Packages |

### The core is the headline constraint

`RV32EC` is **RV32E + C**, and both letters matter:

- **`E`** — the *embedded* base: only **16** integer registers instead of 32.
- **No `M`** — there is **no hardware multiply or divide**. Every `*` and `/` on a non-power-of-two
  becomes a compiler-emitted software routine. This is the single most consequential difference
  from every other CH32 part, all of which are `IMAC` or `IMAFC`
  ([family RM](../ch32f2x-ch32v2x-ch32v3x/README.md) §2).
- **No `A`** — no atomics.
- **`C`** — compressed instructions, which is what makes 16 KB of flash go as far as it does.

A toolchain configured for `rv32imac` will emit instructions this part cannot execute. The
correct `-march` is **`rv32ec`** (or `rv32ecxw` for WCH's extension).

## 2. Peripheral set

| Block | Count / detail |
|---|---|
| GPIO | **3 ports, 18 I/O** total (on the 20-pin packages) |
| USART | 1 |
| I2C | 1 |
| SPI | 1 |
| ADC | 1 × **10-bit**, 8 external + 2 internal channels, external delayed trigger |
| Analog | 1 × **OPA + comparator**, tied to the ADC and TIM2 |
| Timers | 1 × 16-bit advanced (dead-time, brake, complementary PWM) · 1 × 16-bit general-purpose · IWDG · WWDG · 32-bit SysTick |
| External interrupt | **1 mapped EXTI line** — unusually scarce; plan for it |
| ID | unique identifier (⚠ see §6 — the datasheet and the RM disagree on its width) |

## 3. Clock tree

From RM V1.6 §3.3.1, Figure 3-2:

| Source | Frequency | Notes |
|---|---|---|
| **HSI** | **24 MHz** RC, factory-trimmed | default SYSCLK after reset and after Standby wake |
| **HSE** | **4–25 MHz** external | `OSC_IN` / `OSC_OUT` |
| **LSI** | **128 kHz** RC | IWDG and the auto-wakeup (AWU) time base |
| **PLL** | **×2 only** | fixed multiplier — the one knob you do not get |
| SYSCLK | ≤ **48 MHz** | AHB prescaler /1…/256 → HCLK |

**The PLL is a fixed doubler.** 48 MHz is reached as HSI 24 MHz × 2, or HSE 24 MHz × 2. There is
no other multiplier, so an HSE that is not 24 MHz cannot produce exactly 48 MHz through the PLL.
A clock security system (CSS) and an `MCO` output (HSI/HSE/PLLCLK) are provided.

> ⚠ **Design observation on konsool-zero.** That board fits a **25 MHz** oscillator (`U17`,
> `S3225SMD25MOSC`, LCSC `C7431183`) as HSE. 25 MHz is legal as a raw HSE input (the range is
> 4–25 MHz, so it sits exactly at the ceiling), but **25 × 2 = 50 MHz exceeds the 48 MHz
> maximum**. Either the PLL is left off and the part runs directly from a 25 MHz HSE, or the
> design is 4 % over-clocked. **No firmware exists in the repository to settle which** — the
> project has a single commit and no source. `not-tested`, flagged for whoever builds one.

## 4. Debug: the one-wire interface that trips people up

The CH32V003 has **no SWD and no JTAG**. It exposes WCH's proprietary **single-wire debug
interface (SDI)** on a single pin, `SWIO` (PD1). The reference manual and datasheet both call it
"SWD (SDI)", which is misleading — it is *one* wire plus ground, not ARM's two-wire SWD, and an
ARM SWD probe will not talk to it.

**The trap.** `AFIO_PCFR1` bit field **`SWCFG[2:0]` resets to `000` = SDI enabled** (RM V1.6,
AFIO register description). So **PD1 is a debug pin out of reset**, not a GPIO. To use PD1 as
general-purpose I/O you must explicitly write `SWCFG = 100` ("turn off SWD (SDI), which functions
as a GPIO"). Every value other than `0xx` and `100` is documented as invalid.

**The consequence of doing that:** once SDI is disabled in firmware, the part can no longer be
attached by the debugger at will. Recovery requires the programmer to hold the part in reset and
re-enable the interface during the power-up window — the standard WCH-LinkE "power-cycle unbrick"
dance. Treat `SWCFG = 100` as a decision with a cost.

| Route | Notes |
|---|---|
| **WCH-LinkE** | Vendor USB probe; the only widely-supported SDI host. Needed for recovery |
| **`ch32v003fun`** | Minimal open-source bare-metal framework — the part this project is *named* for. Also bit-bangs SDI from a host MCU |
| MounRiver Studio | WCH's Eclipse-based vendor IDE |
| ⚠ **`nicolaielectronics/rvswd`** | **Does not apply.** That ESP-IDF component targets **CH32V20x/V30x over RVSWD** (two-wire), not the V003's one-wire SDI. Do not assume it reflashes a V003 |

Flash security (RM V1.6 §16.2.2): under read protection, main-memory pages 0–32 (2 KB) are
automatically write-protected regardless of `FLASH_WPR`; the boot-code area, SDI mode area and
RAM are not erasable except by whole-chip erase; and **attempting to remove read protection
auto-erases the entire user area.** The HSI must be running for any flash program/erase.

## 5. Power modes and wake sources

Only **two** low-power modes — there is no Stop mode (contrast the
[CH32V2x/V3x family](../ch32f2x-ch32v2x-ch32v3x/README.md) §4, which has three).

| Mode | Entry | Wake sources | Clocks | Regulator |
|---|---|---|---|---|
| **Sleep** | `SLEEPDEEP=0`, `PDDS=0`, then `WFI`/`WFE` | any interrupt (`WFI`) or wake-up event (`WFE`) | core clock off, **all peripheral clocks still running** | ON |
| **Standby** | `SLEEPDEEP=1`, `PDDS=1`, then `WFI`/`WFE` | any EXTI-configured interrupt/event; **AWU event** | HSE, HSI, PLL and peripheral clocks off | **OFF** |

Facts worth carrying into firmware:

- **Sleep does not gate peripheral clocks.** The RM is explicit: "turn off useless peripheral
  clocks before entering Sleep mode to reduce power consumption." Sleep alone buys less than
  people expect.
- **Standby retains SRAM, registers and I/O pin state, and does *not* reset on wake.** SYSCLK
  reverts to HSI. Only IWDG and LSI keep running.
- **AWU (auto-wakeup)** is the periodic self-wake: LSI 128 kHz time base, via
  `PWR_AWUCSR` / `PWR_AWUWR` (window compare) / `PWR_AWUPSC` (prescaler) at `0x40007008`–`0x40007010`.
  ⚠ **Non-obvious requirement:** the AWU is wired to **EXTI line 9 internally**, so you must also
  configure EXTI line 9's rising/falling edge trigger and enable that interrupt, or the AWU will
  never fire (RM V1.6 §2.3.4).
- Standby entry is **deferred** while a flash program/erase is in progress.
- `SLEEPONEXIT` and `SEVONPEND` behave as on ARM; `SLEEPDEEP` lives in the core-private
  `PFIC_SCTLR`, not in `PWR`.

## 6. Conflicts, caveats and unknowns

⚠ **Unique-ID width: the vendor contradicts itself.**

| Source | Claim |
|---|---|
| CH32V003 **Datasheet V1.4**, Features | "Security features: **64-bit** unique ID" |
| CH32V003 **Reference Manual V1.6**, §15.1 (ESIG) | "Unique identification: **96-bit** binary code" |

Both documents are WCH primary sources, both are held locally (§9), and neither is newer in a way
that obviously supersedes the other (DS V1.4 is dated 2023-05-18, RM V1.6 2023-12-13). The RM is
the register-level document and describes the ESIG block directly, which weakly favours **96 bits**
— the same width ST and WCH use elsewhere for this block. **Unresolved.** What would settle it:
reading `ESIG` on real silicon, or a later datasheet revision. Do not size a buffer from either
number without checking. `not-tested`.

Other caveats:

- **One EXTI line.** Designs that need several pin interrupts will not fit comfortably.
- **2 KB of SRAM** is the real ceiling on what this part can do, not the 16 KB of flash.
- **Package determines I/O count**, not just pinout: F4P6/F4U6 have 18 I/O, A4M6 has 14, J4M6 has 6.
- **Errata not researched.** WCH errata were not located in this pass.
- **Nothing here was verified on hardware.**

### Ordering-part decode (DS V1.4 §4)

| Part | Package | Body | Pitch | I/O |
|---|---|---|---|---|
| `CH32V003F4P6` | TSSOP20 | 4.4 × 6.5 mm | 0.65 mm | 18 |
| **`CH32V003F4U6`** | **QFN20** | **3.0 × 3.0 mm** | **0.4 mm** | **18** |
| `CH32V003A4M6` | SOP16 | 3.9 × 10 mm | 1.27 mm | 14 |
| `CH32V003J4M6` | SOP8 | 3.9 × 5.0 mm | 1.27 mm | 6 |

All four carry the same 16 KB flash / 2 KB SRAM. Suffix letters: `T` = LQFP, `U` = QFN,
`R` = QSOP, `P` = TSSOP, `M` = SOP.

## 7. Related components

- [**WCH CH32V203C8T6**](../ch32v203c8t6/README.md) — the Tanmatsu mainboard coprocessor.
  A *different* part: QingKe V4B `IMAC`, 144 MHz, 64 KB flash, 20 KB SRAM, LQFP-48, two-wire
  RVSWD debug. Confusing the two is the most likely error in this area of the repository.
- [**WCH CH32F2x / CH32V2x / CH32V3x family reference manual**](../ch32f2x-ch32v2x-ch32v3x/README.md)
  — the *other* WCH reference manual acquired in the same pass; covers the V203, not the V003.
- [Texas Instruments CC1101](../../texas-instruments/cc1101/README.md) and
  [ST ST25R3916](../../stmicroelectronics/st25r3916/README.md) — the two radios this MCU shares
  the konsool-zero board with.

## 8. Used by

### [`badgeteam/konsool-zero`](https://github.com/badgeteam/konsool-zero) — designator `U19`

A **work-in-progress** Flipper-Zero-class radio expansion board for the
[Tanmatsu / Konsool](../../../devices/nicolai-electronics/tanmatsu/README.md) rear 36-pin port.
Fitment is established from the project's **own KiCad schematic**, sheet `zero-mcu.kicad_sch`, at
commit `0f0b964` (2025-03-22, the repository's only commit):

| Field | Value |
|---|---|
| Reference | **`U19`** |
| Value | **`CH32V003F4U6`** |
| Footprint | `Package_DFN_QFN:QFN-20-1EP_3x3mm_P0.4mm_EP1.65x1.65mm` |

The footprint matches the datasheet's QFN20 3.0 × 3.0 mm / 0.4 mm-pitch package, so the schematic
symbol and the land pattern agree — this is a genuine reading, not a library placeholder.

**Role on that board.** Hierarchical labels on the `zero-mcu` sheet show what the part is wired to:

| Label group | Signals | Apparent function |
|---|---|---|
| RFID | `RFID_CARRIER`, `RFID_IN`, `RFID_PULL`, `RFID_RF_OUT`, `RFID_WR` | Drives and reads the **125 kHz RFID** analog front end (`rfid-schematic.kicad_sch`: `U10`/`U14` LMV358, `U12` LMV331, 1N4148 detectors) |
| Band select | `RF_SW_0`, `RF_SW_1` | Controls the two Infineon `BGS13S4N9E6327XTSA1` SP3T switches (`U3`, `U4`) on the antenna-balance sheet |
| NFC | `NFC_IRQ` | Interrupt in from the `ST25R3916` (`U5`) |
| Host | `SCL_MCU`, `SDA_MCU` | I2C |
| Debug | `SWIO` | The single-wire SDI of §4, brought to `J4` (2-pin header) |

So the V003 is a **small helper MCU — carrier generation, band switching and an I2C shim — not
an application processor.** The CC1101 and ST25R3916 SPI buses (`SPI_R_*`, `NFC_*`) are separate
hierarchical nets that do not appear on the `zero-mcu` sheet, consistent with those radios being
driven by the Tanmatsu host across the expansion connector rather than by this MCU.

⚠ **This corrects an earlier claim in this repository** that konsool-zero carried an
**STM32WB55CC** as "an on-board processor". It does not; see
[`stm32wb55xx`](../../stmicroelectronics/stm32wb55xx/README.md) §5 and the Tanmatsu
[`expansion-boards.md` §2](../../../devices/nicolai-electronics/tanmatsu/expansion-boards.md).

**Status: design study, not a buildable board.** One commit, no README, no stated licence, no
firmware. Nothing was built or powered. `not-tested`.

## 9. Local artifacts

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/ch32v003-reference-manual-v1.6.pdf`](artifacts/ch32v003-reference-manual-v1.6.pdf) | 2 287 272 | `9349c1044cb890aad2d7f60945342a02393ead3fc9011de23a3bfa46d96206b7` | WCH, **CH32V003 Reference Manual V1.6**, 185 pp., PDF metadata `CreationDate 2023-12-13`, producer `pdfFactory Pro 8.31`. Vendored in `badgeteam/konsool-zero` `docs/ch32/CH32V003RM.PDF` @ `0f0b964`; moved here 2026-09-20 |
| [`artifacts/ch32v003-datasheet-v1.4.pdf`](artifacts/ch32v003-datasheet-v1.4.pdf) | 607 396 | `7a328077bfde400485effb9cae0f8bbd4741e9c07de867f937fa86748427b9e4` | WCH, **CH32V003 Datasheet V1.4**, 33 pp., `CreationDate 2023-05-18`. Same origin; moved here 2026-09-20 |

Both validated as `%PDF-1.7` from content. Text layer cross-checked against the rendered cover
headings ("CH32V003 Reference Manual / V1.6", "CH32V003 Datasheet / V1.4") before any value above
was transcribed — `executed-success`, 2026-09-20.

**Upstream canonical URLs** (WCH serves these behind HTML download shells, not as direct PDF links):

- Reference manual: <https://www.wch-ic.com/downloads/CH32V003RM_PDF.html>
- Datasheet: <https://www.wch-ic.com/downloads/CH32V003DS0_PDF.html>

Licence: **unknown** — no notice found in either document. Redistribution status: `unknown`.
Disposition: **repository, unstaged.**

## 10. Sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| V3-1 | CH32V003 Reference Manual V1.6 | WCH | primary | reference manual | [`artifacts/…-v1.6.pdf`](artifacts/ch32v003-reference-manual-v1.6.pdf) | 2026-09-20 | 2023-12-13 | §3 clock tree, §4 debug/flash security, §5 power modes, §6 96-bit ID |
| V3-2 | CH32V003 Datasheet V1.4 | WCH | primary | datasheet | [`artifacts/…-v1.4.pdf`](artifacts/ch32v003-datasheet-v1.4.pdf) | 2026-09-20 | 2023-05-18 | §1 core/memory, §2 peripherals, §6 package table, §6 64-bit ID |
| V3-3 | `badgeteam/konsool-zero` @ `0f0b964` | Badge.Team | primary | repository (KiCad) | `scratch/tanmatsu/sources/konsool-zero/` | 2026-08-26 | 2025-03-22 | §8 fitment — `U19 = CH32V003F4U6`; §3 the 25 MHz HSE observation |
| V3-4 | `ch32v003fun` | cnlohr et al. | community | repository | <https://github.com/cnlohr/ch32v003fun> | 2026-09-20 | — | §4 toolchain route. **Not re-verified in this pass** — carried from the [CH32V203C8T6 record](../ch32v203c8t6/README.md) |
