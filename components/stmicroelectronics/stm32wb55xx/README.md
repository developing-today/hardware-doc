# STMicroelectronics STM32WB55xx / STM32WB35xx

> Multiprotocol wireless MCU: **Cortex-M4F @ 64 MHz** (application) + **Cortex-M0+** (radio),
> **Bluetooth LE 5.4** and **IEEE 802.15.4** (Thread 1.3 / Zigbee 3.0), 2.4 GHz.
> Manufacturer: **STMicroelectronics** · Research snapshot **2026-09-20**

## ⚠ Fitment: NOT established

**No board documented in this repository fits an STM32WB55xx or STM32WB35xx.**

This record exists because the datasheet was acquired alongside the Tanmatsu research, as
reference material in the `docs/` folder of `badgeteam/konsool-zero`. It is filed as a component
record so the document is mined, hashed and findable — **not** because any board carries the part.

**Correcting an earlier claim in this repository.** The Tanmatsu
[`expansion-boards.md` §2](../../../devices/nicolai-electronics/tanmatsu/expansion-boards.md)
previously listed, under the heading *"Silicon identified from the KiCad schematics"*:

> | **STM32WB55CC** | Wireless MCU (Cortex-M4 + M0+, BLE) — an on-board processor, not just a peripheral |

**That is not supported by the schematics.** Evidence, all `executed-success` 2026-09-20:

| Test | Result |
|---|---|
| Case-insensitive search for `stm32` or `wb55` across every `.kicad_sch`, `.kicad_pcb`, `.kicad_pro` and `jlcpcb/project.db` in the project | **zero matches** |
| Same search across the project's entire git history (`0f0b964`, the only commit) | **zero matches** |
| Full reference-designator census of all nine schematic sheets | `U1` CC1101RGPR · `U2` 27 MHz · `U3`,`U4` BGS13S4N9E6327XTSA1 · `U5` ST25R3916-AQWT · `U6` TSOP75338TR · `U7`–`U9` VSMY14940 · `U10`,`U14` LMV358 · `U11`,`U13`,`U15`,`U16` 1N4148X-TP · `U12` LMV331IDCKR · `U17` S3225SMD25MOSC · **`U19` CH32V003F4U6** · `X1` XRCGB27M120F3M00R0. **No `U18`** (gap in the sequence); no ST MCU of any kind |

The board's on-board processor is a **[WCH CH32V003F4U6](../../wch/ch32v003/README.md)** (`U19`,
QFN-20) — a 16 KB / 2 KB RV32EC part, not a dual-core wireless MCU. The two claims are not close.

**Why the datasheet was there.** The same `docs/` folder contains six **Flipper Devices Inc.**
schematic sheets and a folder of annotated Flipper Zero teardown photographs. The Flipper Zero's
own main MCU *is* an STM32WB55, and its sub-GHz and NFC front ends are the same `CC1101RGPR` and
`ST25R3916-AQWT` that konsool-zero adopted. The folder is a **prior-art study of the Flipper
Zero**, and this datasheet is part of that study. The earlier record appears to have read the
presence of a datasheet as evidence of a fitted part.

*This is a negative result, recorded with its evidence and date so it is not re-investigated.*

---

## 1. Identity and capability

| Property | Value | Evidence |
|---|---|---|
| Application core | **Arm Cortex-M4 with FPU**, ART accelerator (0-wait flash), MPU, DSP, **64 MHz**, 80 DMIPS | DS11929 Rev 17 Features |
| Radio core | **Arm Cortex-M0+**, dedicated to the real-time radio layer — runs ST's binary stack | ibid. |
| Benchmarks | 1.25 DMIPS/MHz · **219.48 CoreMark** (3.43/MHz @ 64 MHz) · 303 ULPMark-CP | ibid. |
| Radio | 2.4 GHz; **Bluetooth 5.4**, IEEE **802.15.4-2011** PHY+MAC, Thread 1.3, Zigbee 3.0 | ibid. |
| RX sensitivity | **−96 dBm** (BLE 1 Mbps), **−100 dBm** (802.15.4) | ibid. |
| TX power | programmable **up to +6 dBm**, 1 dB steps; external PA supported | ibid. |
| Radio current | **Rx 4.5 mA**, **Tx 5.2 mA @ 0 dBm** | ibid. |
| Balun | **integrated** — reduces BOM. Optional IPD matching companion (`MLPF-WB-01E3` / `MLPF-WB55-02E3` / `MLPF-WB-02D3`) | ibid. |
| Supply | **1.71–3.6 V**; embedded **SMPS step-down with intelligent bypass** | ibid. |
| Flash | up to **1 MB**, with PCROP sector protection (shields the radio stack) | ibid. |
| SRAM | up to **256 KB**, incl. 64 KB with **hardware parity** | ibid. |
| Crystal | **32 MHz** (radio *and* CPU) with integrated trimming caps; **32 kHz LSE** for RTC | ibid. |
| Bootloader | ROM, over **USART / SPI / I2C / USB**; plus BLE/802.15.4 **OTA** update | ibid. |
| Security | 3× AES-256, **PKA** (RSA, Diffie-Hellman, ECC over GF(p)), customer key manager, **SFI** secure firmware install, 1 KB OTP | ibid. |
| Temperature | −40 to 85 °C / 105 °C | ibid. |

**The dual-core split is the defining architectural fact.** CPU2 (M0+) is not yours: it runs
ST's precompiled wireless coprocessor binary, and the application on CPU1 (M4F) talks to it
through a mailbox/IPCC shared-memory interface. This is why the part needs a specific ST firmware
binary flashed at a version-dependent address alongside your application — a well-known source of
"it built but the radio does nothing".

## 2. Variants — reading the part number

Decoder from DS11929 Rev 17 §8:

| Field | Values |
|---|---|
| Subfamily | `55` = die 5, full features · `35` = die 3 |
| **Pin count** | **`C` = 48** · `R` = 68 · `V` = 100 or 129 |
| **Flash** | **`C` = 256 KB** · `E` = 512 KB · `Y` = 640 KB (WB55VY only) · `G` = 1 MB |
| Package | `U` = UFQFPN48 7×7 · `V` = VFQFPN68 8×8 · `Y` = WLCSP100 0.4 mm · `Q` = UFBGA129 0.5 mm |
| Temperature | `6` = −40…85 °C · `7` = −40…105 °C |
| ID code | `A` = proprietary · blank = non-proprietary |
| Packing | `TR` = tape and reel |

So the **`STM32WB55CC`** named in the acquired filename is the **48-pin, 256 KB flash** device.
Per Table 2 that implies:

| Feature | STM32WB55Cx (48-pin) |
|---|---|
| Flash / SRAM | 256 KB / **128 KB** (SRAM1 64 K + SRAM2 64 K) |
| GPIOs | **30** |
| SPI / I2C / USART / LPUART | 1 / 2 / 1 / 1 |
| Wake-up pins | **2** |
| Tamper pins | 1 |
| ADC | 12-bit, **13 channels** (incl. 3 internal) |
| LCD | 4×13 |
| Capacitive sensing | **no** (68- and 100-pin parts have 6 and 18 sensors) |

Note `STM32WB55CC` is a *base* part number; a real orderable adds package, temperature, ID and
packing (e.g. `STM32WB55CCU6TR`). The konsool-zero filename carries no such suffix, which is
consistent with it being a **downloaded reference document rather than a BOM line**.

## 3. Power modes and wake sources

DS11929 Rev 17, Table 8. The low end is the reason this part gets designed in:

| Mode | Regulator | CPU1 | RAM | Clocks | Wake sources | Typical current | Wake time |
|---|---|---|---|---|---|---:|---:|
| **Stop 2** | LPR | off | on | LSE, LSI | reset pin, **all I/Os**, RF, BOR, PVD/PVM, RTC, LCD, IWDG, COMP1/2, LPUART1, I2C3, LPTIM1 | 1.85 µA (2.1 µA w/ RTC) | **5.71 µs** |
| **Standby** | LPR or off | off | SRAM2a optional | LSE, LSI | **RF**, reset pin, **5 × `WKUPx` I/Os**, BOR, RTC, IWDG | 0.11–0.32 µA (0.39–0.60 µA w/ RTC) | **51 µs** |
| **Shutdown** | off | off | **off** | LSE only | **5 × `WKUPx` I/Os**, RTC | **0.028 µA** (0.315 µA w/ RTC) | — |

Traps worth carrying forward:

- **The wake-up-pin count is package-dependent.** The table's "5 I/Os (WKUPx)" is the 68/100-pin
  figure; **WB55Cx and WB35Cx have only 2** (Table 2). Designing a 48-pin part around five wake
  pins will not work.
- **RF is itself a wake source** from Stop 2 and Standby — the radio can wake the application core.
  It is *not* a wake source from Shutdown.
- **Shutdown loses all RAM** and keeps only LSE + RTC. Coming out of it is a reset, not a resume.
- Flash programming is **only possible in Range 2 voltage**, and the flash controller can be
  power-gated if the RF subsystem is idle and code runs from SRAM.
- HSE 32 MHz is **automatically engaged whenever the RF subsystem needs it**, regardless of what
  the application selected — budget the current accordingly.

## 4. Clock sources

32 MHz crystal (shared radio + CPU, integrated trim caps) · 32 kHz LSE crystal · LSI1 internal
32 kHz RC ±5 % · LSI2 internal 32 kHz RC ±500 ppm · **MSI** multispeed 100 kHz–48 MHz auto-trimmed
by LSE to better than ±0.25 % · HSI16 16 MHz factory-trimmed ±1 % · 2 × PLL for system/USB/SAI/ADC.

The **MSI auto-trimmed by LSE** is the interesting one: it gives a USB-capable clock without a
high-speed crystal, and the USB FS device is explicitly **crystal-less**.

## 5. Related and comparable parts

- [**WCH CH32V208**](../../wch/ch32f2x-ch32v2x-ch32v3x/README.md) — WCH's BLE 5.3 wireless MCU
  (QingKe V4C, 128 KB flash / 64 KB SRAM). The closest architectural analogue in the WCH line
- [**WCH CH32V003**](../../wch/ch32v003/README.md) — what konsool-zero *actually* fits
- [**TI CC1101**](../../texas-instruments/cc1101/README.md) and
  [**ST ST25R3916**](../st25r3916/README.md) — the two radio front ends the Flipper Zero pairs
  with its STM32WB55, both of which konsool-zero *does* fit
- [**ST STM32WLE5**](../stm32wle5/README.md) — ST's sub-GHz sibling (LoRa), already recorded here

## 6. Local artifacts

| File | Bytes | SHA-256 | Provenance |
|---|---:|---|---|
| [`artifacts/stm32wb55xx-stm32wb35xx-datasheet-ds11929-rev17.pdf`](artifacts/stm32wb55xx-stm32wb35xx-datasheet-ds11929-rev17.pdf) | 3 096 637 | `94daab4aca690492b84e0898cfd1ee05ed829ee15faca86332ff63e5c6c4da72` | STMicroelectronics, **DS11929 Rev 17**, dated **October 2024**, 194 pp. PDF metadata: `Author STMICROELECTRONICS`, `Creator C2 v20.4.0000 build 240 – Techlit_Active`, `CreationDate 2024-10-07`. An **unmodified ST-produced document** (contrast the Alldatasheet-wrappered ST25R3916 copy). Vendored in `badgeteam/konsool-zero` `docs/stm32wb55cc.pdf` @ `0f0b964`; moved here 2026-09-20 |

Validated as `%PDF-1.3` from content. Text layer cross-checked against the rendered cover heading
("STM32WB55xx / STM32WB35xx / Multiprotocol wireless 32-bit MCU…") and against the Rev 17 revision
row (07-Oct-2024) before transcription — `executed-success`, 2026-09-20.

Canonical URL: <https://www.st.com/resource/en/datasheet/stm32wb55cc.pdf>
*(constructed from ST's standard `resource/en/datasheet/<part>.pdf` template and the acquired
filename — **not re-fetched in this pass**, so treat the URL as `inferred` and the hash above as
describing only the local copy.)*

Licence: **unknown** — ST's standard "IMPORTANT NOTICE" appears; no redistribution grant.
Redistribution: `unknown`. Disposition: **repository, unstaged.**

## 7. Sources

| ID | Title | Publisher | Class | Medium | URL / path | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| WB-1 | STM32WB55xx/STM32WB35xx datasheet DS11929 Rev 17 | STMicroelectronics | primary | datasheet | [`artifacts/…rev17.pdf`](artifacts/stm32wb55xx-stm32wb35xx-datasheet-ds11929-rev17.pdf) | 2026-09-20 | 2024-10-07 | §1 capability, §2 variants, §3 power modes, §4 clocks |
| WB-2 | `badgeteam/konsool-zero` @ `0f0b964` | Badge.Team | primary | repository (KiCad) | `scratch/tanmatsu/sources/konsool-zero/` | 2026-08-26 | 2025-03-22 | **The negative result above** — designator census, git-history search |
| WB-3 | Flipper Zero schematic set (iButton, NFC, Power, Power+vibro, RFID, Sub-1 GHz CC1101) | **Flipper Devices Inc.** | primary (third-party) | schematic | `scratch/tanmatsu/sources/konsool-zero/docs/` | 2026-08-26 | unknown | Why an STM32WB55 datasheet was in that folder; title blocks read "Flipper Devices Inc" |
