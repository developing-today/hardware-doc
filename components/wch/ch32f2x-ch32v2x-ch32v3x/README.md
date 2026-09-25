# WCH CH32F2x / CH32V2x / CH32V3x — family reference manual

> The WCH reference manual that covers **CH32F20x (Cortex-M3)**, **CH32V20x** and **CH32V30x**
> (RISC-V QingKe V4) as one document.
> Manufacturer: **WCH (Nanjing Qinheng Microelectronics)** · Research snapshot **2026-09-20**

**This is a family/document record, not a part record.** WCH ships *one* reference manual for
three series across two instruction-set architectures, and that document is the register-level
authority for several parts this repository already documents. It is filed here so the
part records can cite it instead of each holding a copy of a 6.4 MB PDF.

> ⚠ **Fitment: none established, and none claimed.** No board documented in this repository fits
> a CH32F2x or CH32V3x part. The manual was acquired as reference material vendored in
> `badgeteam/konsool-zero`'s `docs/` folder. **However**, it is *not* merely reference material:
> it is the reference manual for the **CH32V20x** series, which includes the
> **[CH32V203C8T6](../ch32v203c8t6/README.md)** fitted on the Tanmatsu mainboard as `U12`. See §5.

## 1. What the document covers

CH32FV2x_V3x Reference Manual **V2.1** (595 pp.). From its own Overview:

> "For users' application development, this manual provides detailed use information of CH32F2x
> series, CH32V2x series and CH32V3x series products."

It explicitly defers device characteristics to per-series datasheets:

| Series class | Datasheet the RM points to | Held locally? |
|---|---|---|
| CH32F20x_D6 | `CH32F203DS0` | no |
| CH32F20x_D8, _D8C | `CH32F207DS0` | no |
| CH32F20x_D8W | `CH32F208DS0` | no |
| **CH32V20x_D6, _D8** | **`CH32V203DS0`** | ✅ **yes** — [`ch32v203c8t6/artifacts/ch32v203-datasheet-v2.7.pdf`](../ch32v203c8t6/artifacts/ch32v203-datasheet-v2.7.pdf) |
| CH32V20x_D8W | `CH32V208DS0` | no |
| CH32V30x_D8, _D8C | `CH32V307DS0` | no |

**Density-class decoder** (RM V2.1, "Classification description of CH32 MCUs"):

| Class | Flash | Product type |
|---|---|---|
| `D6` | 32 KB or 64 KB | Low-and-medium-density general |
| `D8` | 128 KB or 256 KB | High-density general |
| `D8C` | 128 KB or 256 KB | Connectivity / interconnectivity |
| `D8W` | 128 KB or 256 KB | **Wireless** |

`D` = density, `6` = 2⁶, `8` = 2⁸. The manual then enumerates membership explicitly — and this is
the line that matters here:

> "**CH32V20x_D6:** CH32V203F6, CH32V203G6, CH32V203K6, CH32V203F8, CH32V203G8, CH32V203K8,
> **CH32V203C6 and CH32V203C8.**"

So the Tanmatsu's `CH32V203C8T6` is a **CH32V20x_D6** part and **this manual is its register
reference**. `primary`.

## 2. The cores — and why the V003 is not in this document

| Core | ISA | HW stack | Nested IRQ | Fast-IRQ ch. | Int-divide cycles | MPU | Used by |
|---|---|---|---|---:|---:|---|---|
| **QingKe V4B** | `IMAC` | 2 | 2 | 4 | 9 | **none** | CH32V203, CH32V205 |
| **QingKe V4C** | `IMAC` | 2 | 2 | 4 | 5 | standard | CH32V208 |
| **QingKe V4F** | **`IMAFC`** | 3 | 8 | 4 | 5 | standard | CH32V303 / V305 / V307 |
| *(QingKe V2A)* | *`RV32EC`* | — | 2 | — | — | none | *[CH32V003](../ch32v003/README.md) — **covered by a different manual*** |

Three things fall out of this table:

- **V4F adds `F`** — a hardware FPU. V4B and V4C do not have one.
- **V4B has no MPU.** If you need memory protection on a CH32 RISC-V part, you need a V4C or V4F,
  which in practice means V208 or V30x — not the V203.
- **All of these are `IMAC`/`IMAFC`**, i.e. hardware multiply and divide. The
  [CH32V003](../ch32v003/README.md) is `RV32EC` — no multiplier, 16 registers, and a *different*
  reference manual. **Code and toolchain flags do not transfer between them.**

CH32F2x is the odd one out: an **ARM Cortex-M3** family sharing the same peripheral IP and
register map as the RISC-V parts. That is the reason one manual serves both — the peripherals are
identical, only the core differs.

## 3. Series feature map

From the RM's "CH32V2x and CH32V3x serial products overview":

| | **V203** low/med general | **V303** high-density | **V305** connectivity | **V307** interconnect | **V208** wireless |
|---|---|---|---|---|---|
| Core | V4B | V4F | V4F | V4F | **V4C** |
| Flash | 32 K / **64 K** | 128 K / 256 K | 128 K | 256 K | 128 K |
| SRAM | 10 K / **20 K** | 32 K / 64 K | 32 K | 64 K | 64 K |
| USB | USBD + USBFS | USBFS | OTG_FS + USBHS(+PHY) | OTG_FS + USBHS(+PHY) | USBD + USBFS |
| Ethernet | — | — | — | **ETH-1000MAC / 10M-PHY** | ETH-10M(+PHY) |
| Radio | — | — | — | — | **BLE 5.3** |
| Other | 2×OPA, CAN, RTC, 2×WDG | +DAC, RNG, SDIO, FSMC | +2×CAN | +DVP, SDIO, FSMC | — |

**`CH32V208` is the WCH part with an integrated BLE 5.3 radio** — worth knowing as the
architectural counterpart to ST's
[STM32WB55xx](../../stmicroelectronics/stm32wb55xx/README.md), should anyone revisit the
"wireless MCU on an expansion board" idea that
[konsool-zero](../../../devices/nicolai-electronics/tanmatsu/expansion-boards.md) did *not*
actually implement.

## 4. Power modes and wake sources

**Three** low-power modes — one more than the [CH32V003](../ch32v003/README.md), and the extra one
(Stop) is the useful one.

| Mode | Entry | Wake sources | Retained | Resets on wake? |
|---|---|---|---|---|
| **Sleep** | `SLEEPDEEP=0`, `PDDS=0`, `WFI`/`WFE` | any interrupt or wake-up event | everything; peripheral clocks keep running | no |
| **Stop** | `SLEEPDEEP=1`, `PDDS=0`, `WFI`/`WFE` | any **external interrupt/event** set in the EXTI register | SRAM, registers, I/O pin state | **no** — resumes, HSI becomes SYSCLK |
| **Standby** | `SLEEPDEEP=1`, `PDDS=1`, `WFI`/`WFE` | **`WKUP` pin rising edge**, **RTC alarm rising edge**, **`NRST` external reset**, **IWDG reset**; plus any EXTI event | see RAM-retention bits below | **yes** — power reset performed |

Load-bearing details for an always-on coprocessor design:

- **Still running in Stop *and* Standby:** IWDG, **RTC**, and the low-frequency clocks **LSI/LSE**.
  (The V003 keeps only IWDG and LSI, and has no RTC at all.) This is what makes a V203 usable as
  a battery-backed real-time-clock-plus-alarm part — precisely the
  [Tanmatsu coprocessor pattern](../ch32v203c8t6/README.md#design-notes).
- **Stop-mode regulator choice:** `LPDS=0` → regulator in normal mode; `LPDS=1` → low-power mode.
  For the floor, additionally set **`RAMLV=1`** in `PWR_CTRL` to enable RAM low-voltage mode.
- **Standby RAM retention is opt-in and split by supply:**
  - Mains/battery-rail supplied: `R2KSTY=1` keeps 2 KB, `R30KSTY=1` keeps 30 KB.
  - **VBAT** supplied: `R2KVBAT=1` keeps 2 KB, `R32KVBAT=1` keeps 30 KB.
  - Default is **no retention** — Standby throws SRAM away unless you ask for it.
- **Stop entry is deferred** while flash programming or a PB-domain access is in flight.
- `SEVONPEND` / `SLEEPONEXIT` semantics are as on ARM; three WFE wake-configuration routes are
  documented (EXTI event mode, interrupt-equivalent, or `SLEEPONPEN` with manual pending-bit clear).

## 5. Why this record exists — and what it does *not* establish

**What it establishes.** This manual is the register-level reference for the
**[CH32V203C8T6](../ch32v203c8t6/README.md)** on the Tanmatsu mainboard (`U12`). That record
previously noted *"No local datasheet copy"*; this pass resolves that — both the family RM and the
**CH32V203 datasheet V2.7** are now held (§6 and the V203 record's artifacts).

**What it does not establish.** Nothing in this document is evidence that any CH32F2x or CH32V3x
part is fitted on any board in this repository. It reached the repository because the
`badgeteam/konsool-zero` author vendored a folder of WCH documentation alongside a
[CH32V003](../ch32v003/README.md) design. The plausible reason is simply that WCH's download page
offers this manual next to the V003's, and the author took both — but **that is an inference about
motive, not a finding.** No CH32F2x/V2x/V3x part appears in konsool-zero's schematics; a full
reference-designator census of all nine sheets found none (see
[`ch32v003` §8](../ch32v003/README.md#8-used-by)).

## 6. Local artifacts

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/ch32fv2x-v3x-reference-manual-v2.1.pdf`](artifacts/ch32fv2x-v3x-reference-manual-v2.1.pdf) | 6 406 562 | `49b9db372935753b277dd7f3dcdef812db3e7ecf8abf0109cb4f1eea50ae2d6e` | WCH, **CH32FV2x_V3x Reference Manual V2.1**, 595 pp., PDF metadata `Title CH32FV2x_V3xRM-EN`, `Author WCH`, `CreationDate 2024-03-01`, producer `pdfFactory Pro 8.31`. Vendored in `badgeteam/konsool-zero` `docs/ch32/CH32FV2x_V3xRM.PDF` @ `0f0b964`; moved here 2026-09-20 |

Validated as `%PDF-1.7` from content. Text layer cross-checked against the rendered cover heading
("CH32FV2x_V3x Reference Manual / V2.1 / https://wch-ic.com") before transcription —
`executed-success`, 2026-09-20. At 6.4 MB this is large but well within the repository's existing
tolerance (the tree already holds a 23 MB Espressif TRM); kept in-repo rather than archived
because it is **primary and served only behind a vendor HTML shell**.

Upstream canonical URL: <https://www.wch-ic.com/downloads/CH32FV2x_V3xRM_PDF.html>
(an HTML download page, not a direct PDF link — see the [WCH vendor guide](../../../vendors/wch/README.md)).

Licence: **unknown** — no notice found in the document. Redistribution: `unknown`.
Disposition: **repository, unstaged.**

## 7. Related records

- [**WCH CH32V203C8T6**](../ch32v203c8t6/README.md) — the part this manual actually documents that
  this repository fits (Tanmatsu `U12`)
- [**WCH CH32V003**](../ch32v003/README.md) — *not* covered by this manual; different core, different RM
- [WCH vendor documentation guide](../../../vendors/wch/README.md)

## 8. Sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| F2-1 | CH32FV2x_V3x Reference Manual V2.1 | WCH | primary | reference manual | [`artifacts/…-v2.1.pdf`](artifacts/ch32fv2x-v3x-reference-manual-v2.1.pdf) | 2026-09-20 | 2024-03-01 | §1 scope and density classes, §2 core table, §3 series map, §4 power modes |
| F2-2 | `badgeteam/konsool-zero` @ `0f0b964` | Badge.Team | primary | repository (KiCad) | `scratch/tanmatsu/sources/konsool-zero/` | 2026-08-26 | 2025-03-22 | §5 — acquisition context, and the negative result that no CH32F2x/V3x part is fitted |
