# XMC XM25UH128DHIQT

> **128 Mbit (16 MB) serial NOR flash** — 2.3–3.6 V, Standard / Dual / Quad SPI plus QPI and DTR read modes, 166 MHz fast read, 4 KB uniform sectors, 128-bit unique ID, SFDP, and three 1 KB OTP-lockable security registers.
> Research snapshot **2026-09-01**. Fitted as **`U13`** on sheet 3 of the [M5Stack PaperMono](../../../devices/m5stack/papermono/README.md) (SKU C153) — the ESP32-S3's application flash. **No hardware was available.**

> **Headline finding:** all four data lines are wired, and the ordering code specifies the **Quad Enable bit programmed to 1 at the factory**. The hardware therefore supports QIO in full, matching M5Stack's published `board_build.arduino.memory_type = qio_opi`, even though the shipped factory image's header reports **DIO**. See [§5 — resolving the QIO/DIO conflict](#5--resolving-the-qiodio-conflict).

---

## Evidence labelling

| Marker | Meaning | Status |
|---|---|---|
| **[DS]** | XMC `XM25UH128D` datasheet **Rev1.2**, issue date 2025-06-12 — local copy `artifacts/xm25uh128d-datasheet-ver1.2.pdf` | `not-tested` |
| **[SCH]** | `PaperMono_SCH_V0.6.2_20260522.pdf`, sheet + designator + pin | `executed-success` for the extraction; `not-tested` electrically |
| **[FW]** | Parsed from the shipped factory firmware image | `executed-success` for the parse |
| **[DOC]** | `docs.m5stack.com`, retrieved 2026-09-01 | `not-tested` |
| **[INF]** | Inference, flagged as such | `inferred` |

---

## 1. Identity and part-number decode

| Property | Value | Evidence |
|---|---|---|
| Ordering part | **`XM25UH128DHIQT`** | **[SCH]** sheet 3, `U13` |
| Base device | **`XM25UH128D`** | **[DS]** |
| Manufacturer | **Wuhan Xinxin Semiconductor Manufacturing Co., Ltd. (XMC)** | **[DS]** footer, every page |
| Density | **128 Mbit / 16 MByte** | **[DS]** §1 |
| Datasheet | **Rev1.2**, issue date **2025-06-12**, 98 pp | **[DS]** footer |

### 1.1 The ordering code, decoded **[DS §3 Ordering Information]**

```
XM  25  UH  128  D   H   I   Q   T
│   │   │   │    │   │   │   │   └── Packing:  U = tube, T = tape and reel, R = tray
│   │   │   │    │   │   │   └────── QE code:  G = green, QE = 0
│   │   │   │    │   │   │                     Q = green, QE = 1  (default)
│   │   │   │    │   │   └────────── Temperature: I = −40 … +85 °C (industrial)
│   │   │   │    │   │                           P = −40 … +105 °C
│   │   │   │    │   └────────────── Package:  H  = SOP 208 mil 8L
│   │   │   │    │                             W  = WSON 5 × 6 8L
│   │   │   │    │                             X  = WSON 6 × 8 8L
│   │   │   │    │                             U4 = FOSON 3 × 3 8L
│   │   │   │    └────────────────── Version: D
│   │   │   └─────────────────────── Density: 128 Mbit
│   │   └─────────────────────────── Series: UH = 2.3–3.6 V, 4 KB uniform sector, Quad Mode
│   └─────────────────────────────── Product family: 25 = SPI interface flash
└─────────────────────────────────── Company prefix: XMC
```

**So `XM25UH128DHIQT` is: SOP-8 208 mil, industrial temperature, `QE = 1` programmed at the factory, tape-and-reel.**

> The `Q` character is the one that matters here. It is not a marketing letter — it selects the factory state of the **Quad Enable bit in Status Register-2**, and `Q` (QE = 1) is the vendor's stated default. A host does not have to set QE before using quad-mode reads on this part. See §5.

Note also the packing character is **not on the part marking** **[DS §3 note 1]**, so a physical inspection cannot distinguish `…HIQT` from `…HIQU`.

### 1.2 Device identification **[DS §9.1]**

| Instruction | Response |
|---|---|
| `9Fh` Read JEDEC ID | `46h 40h 18h` — manufacturer `46h` (XMC Serial Flash), device ID **`4018h`** |
| `ABh` / `90h` / `92h` / `94h` | device ID **`17h`** |

Also available: `4Bh` Read Unique ID (128-bit), `5Ah` Read SFDP.

---

## 2. Key capabilities and limits **[DS §1, §10]**

| Parameter | Value |
|---|---|
| Supply | **2.3 – 3.6 V**, single |
| Interfaces | Standard SPI · **Dual SPI** · **Quad SPI** · **QPI** (2-clock instruction) · **SPI/QPI DTR** |
| Max clock — fast read (single/dual/quad) | **166 MHz** |
| Max clock — normal read (`03h`) | 108 MHz |
| Max clock — DTR read | 108 MHz |
| Equivalent throughput | 332 MHz-equivalent dual I/O, **664 MHz-equivalent quad I/O** |
| Standby current | 10 µA typ |
| **Deep power-down current** | **0.2 µA typ** (`B9h` / `ABh`) |
| Active read current | 4 mA typ @ 80 MHz quad I/O |
| Erase granularity | **4 KB sector**, 32 KB block, 64 KB block, chip |
| Program granularity | 1–256 bytes per page; **65 536 pages**, 4 096 sectors, 256 blocks |
| Page program time | 0.25 ms typ |
| Sector erase (4 KB) | 25 ms typ |
| Block erase (32 KB / 64 KB) | 100 ms / 150 ms typ |
| Chip erase | **20 s typ** |
| Endurance | > 100 000 erase/program cycles |
| Retention | > 20 years |
| Suspend/resume | Erase and program, `75h` / `7Ah` |
| Security | 128-bit unique ID · **3 × 1024-byte security registers with OTP lock bits** · software and hardware write protect · power-supply lock-down · top/bottom and complement array protection |
| Continuous read | 8 / 16 / 32 / 64-byte wrap; true XIP |
| Configurable dummy cycles | Yes, for fast-read tuning |
| Packages | SOP 208 mil 8L, WSON 5 × 6, WSON 6 × 8, FOSON 3 × 3 |

**Status-register bits a driver may care about [DS §8.1]:** `BUSY`, `WEL`, `BP2..BP0`, `TB`, `SEC`, `CMP`, `SRP1`/`SRP0`, `SUS`, `LB3..LB1` (security-register OTP locks), **`QE`**, `DRV1`/`DRV0` (output driver strength), **`HOLD/RST`** (IO3 pin function), and the dummy-cycle bits. Most are **volatile *or* non-volatile writable**, which is a useful property — you can change drive strength or QE for one session without spending a non-volatile write.

---

## 3. Pinout **[DS §5, §6]**

Standard 8-pin SPI NOR arrangement, with the three multi-function pins:

| Pin | SPI name | Dual | Quad / QPI |
|---:|---|---|---|
| 1 | `/CS` | `/CS` | `/CS` |
| 2 | `SO` | `IO1` | `IO1` |
| 3 | `/WP` | `/WP` | **`IO2`** |
| 4 | `GND` | | |
| 5 | `SI` | `IO0` | `IO0` |
| 6 | `CLK` | `CLK` | `CLK` |
| 7 | `/HOLD` **or** `/RESET` | | **`IO3`** |
| 8 | `VCC` | | |

> ⚠ **Pin 7 has three possible functions and the choice is a register bit.** `/HOLD` or `/RESET` is selected by the `HOLD/RST` bit in Status Register-3 **[DS §8.1]**; in quad/QPI mode the pin is `IO3` regardless. A part configured for `/RESET` cannot do quad I/O. This is the classic way a "QIO does not work" bug is actually a status-register bug.

---

## 4. Used By

### `devices/m5stack/papermono`

→ [M5Stack PaperMono (C153)](../../../devices/m5stack/papermono/README.md), designator **`U13`**, schematic sheet 3 (`MCU_Core`). It is the ESP32-S3R8's external application flash. M5Stack's specification lists **16 MB Flash + 8 MB Octal PSRAM**; the PSRAM is inside the [ESP32-S3R8](../../espressif/esp32-s3r8/README.md) package, the flash is this part.

#### 4.1 Exact wiring **[SCH sheet 3]**

| `U13` pin | Name | Net | ESP32-S3 (`U12`) pin | S3 signal |
|---:|---|---|---:|---|
| 1 | `CS#` | `NOR_CS` | 32 | `SPICS0` |
| 2 | `SO` / **`IO1`** | **`NOR_DO`** | 34 | `SPIQ` |
| 3 | `WP#` / **`IO2`** | **`NOR_WP`** | 31 | `SPIWP` |
| 4 | `GND` | `GND` | — | — |
| 5 | `SI` / **`IO0`** | **`NOR_DI`** | 35 | `SPID` |
| 6 | `SCLK` | `NOR_SCK` ← **`R39` = 22 Ω/1 %** ← | 33 | `SPICLK` |
| 7 | `HOLD#` / **`IO3`** | **`NOR_HOLD`** | 30 | `SPIHD` |
| 8 | `VCC` | **`VDD_NOR`** | 29 | **`VDD_SPI`** |

Decoupling: `C56` = 1 µF/25 V on `VDD_NOR`. A 22 Ω series resistor (`R39`) damps the clock — standard practice at these edge rates and worth copying.

#### 4.2 `VCC` comes from the ESP32-S3's internal `VDD_SPI` regulator

`VDD_NOR` is driven from `U12` pin 29, `VDD_SPI` — the ESP32-S3's on-chip flash-supply output, **not** from `3V3_L2` directly. **[SCH]**

That is the normal Espressif arrangement, but it carries a specific hazard: `VDD_SPI` can be configured by eFuse as either **3.3 V (pass-through)** or **1.8 V (regulated)**. This flash is a **2.3–3.6 V** part (§2). A board or a recovery procedure that burns the `VDD_SPI = 1.8 V` eFuse on this design leaves the flash below its minimum supply — and eFuses are one-way. **[INF]** Nothing observed suggests M5Stack has done this; it is recorded because it is the failure mode that a "16 MB flash, why won't it boot" investigation should rule out early.

---

## 5. ⚠ Resolving the QIO/DIO conflict

This board's documentation and its shipped binary disagree about the flash mode, and the disagreement has been recorded elsewhere in this research as an open conflict. **The schematic settles the hardware half of it.**

### 5.1 The two claims

| Source | Claim | Evidence |
|---|---|---|
| M5Stack PlatformIO config, on both product pages | `board_build.arduino.memory_type = qio_opi` — **QIO** flash + OPI PSRAM | **[DOC]** |
| Shipped factory image `C153-PaperMono-UserDemo-v1.2.bin`, ESP image headers at `0x0` (bootloader) **and** `0x10000` (app) | `flash_mode: DIO` | **[FW]** |
| Community image `crosspoint-paper-mono-cjk-1.5.0-RC.bin` | also `flash_mode: DIO` | **[FW]** |
| `M5PaperMono-UserDemo/sdkconfig.defaults` | **no** `CONFIG_ESPTOOLPY_FLASHMODE_*` entry at all — IDF default applies | source read in full |

### 5.2 What the hardware actually supports

Three independent facts, all `executed-success`:

1. **All four data lines are routed.** `NOR_DI`, `NOR_DO`, `NOR_WP` and `NOR_HOLD` each reach a dedicated ESP32-S3 SPI pin (§4.1). Nothing is tied off, pulled to a rail, or left floating. IO2 and IO3 — the two pins a DIO-only design would strap or omit — are both live signals to `SPIWP` and `SPIHD`.
2. **The part is a Quad-Mode device by series designation.** `UH` = *"2.3–3.6 V, 4 KB uniform sector, **Quad Mode**"* **[DS §3]**.
3. **`QE` is programmed to 1 at the factory.** The `Q` in `XM25UH128DHIQT` selects *"Green Package with QE = 1 (default)"* **[DS §3]**. Quad mode is available on first power-up without the host writing Status Register-2.

Pin 7's `HOLD/RST` bit would be the remaining obstacle (§3), and its default is the `/HOLD` function, i.e. IO3 usable — this is the one link in the chain not independently confirmed from the shipped part.

### 5.3 The conclusion

**The hardware is not the limitation.** The PaperMono is wired for QIO, populated with a factory-QE-enabled quad-mode flash, and documented by its vendor as a QIO build target. The `DIO` in the shipped image header reflects **how that particular image was built and flashed**, not a board constraint.

Two ordinary explanations, neither of which requires anyone to have made a mistake **[INF]**:

- `sdkconfig.defaults` pins no flash mode, so the ESP-IDF default (`DIO`) was used for the factory build. The vendor's PlatformIO snippet targets *Arduino/PlatformIO* users and is a different build path.
- ESP-IDF's `esptool.py` rewrites the flash-mode byte in the image header at flash time, and the ROM bootloader honours it. A `DIO` header is a legitimate, working configuration on QIO-capable hardware — it is simply slower.

**Practical guidance.** If you want quad-mode performance on a PaperMono, build with `CONFIG_ESPTOOLPY_FLASHMODE_QIO=y` (ESP-IDF) or `board_build.arduino.memory_type = qio_opi` (PlatformIO). Nothing on the board prevents it. If it fails, check the flash's `HOLD/RST` bit before suspecting the wiring.

**This resolves the documentation conflict rather than merely restating it**, and the resolution is: *the vendor's build config is right about the hardware; the shipped binary's header is right about that binary.* Both are true simultaneously.

---

## 6. Flash layout as shipped **[FW]**

The partition table at `0x8000` of the factory image, and the two projects' `partitions.csv`, agree:

```
# Name,   Type, SubType, Offset,  Size,     Flags
nvs,      data, nvs,     0x9000,  0x6000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 0xF00000,
```

**One 15 MiB factory app, no OTA slots, no filesystem partition**, with roughly 960 KB of the 16 MB unallocated above it. The device as shipped is therefore **not field-updatable over the air**. **[INF]**

For contrast, the community CrossPoint reader image repartitions the same chip into `nvs` / `app0` 6400 K / `cjkfont` 4096 K (custom subtype `0x40`) / `spiffs` 3456 K / `coredump` 64 K — a reminder that the 16 MB is a resource, not a fixed layout.

---

## 7. Drivers and software

| Layer | Notes |
|---|---|
| **ESP-IDF `esp_flash`** | Handles this part generically through SFDP and the standard JEDEC command set. No chip driver is needed |
| **`esptool.py`** | Detects the part by `9Fh` JEDEC ID (`46 40 18`, §1.2). If your esptool reports "unknown flash", it is an old version, not a bad chip |
| **Linux MTD `spi-nor`** | Generic SFDP-based probing works; XMC parts are not individually enumerated in older kernels |
| **SFDP** | Supported (`5Ah`), so any SFDP-aware stack can configure dummy cycles and address width without a device table |

---

## 8. Integration pitfalls

1. **Check `HOLD/RST` before blaming the wiring for a QIO failure** (§3). It is a status-register bit, and it makes IO3 unusable as data when set to `/RESET`.
2. **`QE` state depends on the ordering code** (§1.1). `…G…` parts ship with QE = 0 and need the host to set it; `…Q…` parts do not. Two part numbers that differ by one character behave differently at first boot.
3. **The packing character is not on the marking** (§1.1) — you cannot read the full ordering code off the chip.
4. **`VDD_SPI` voltage is an eFuse decision** and the flash needs ≥ 2.3 V (§4.2).
5. **Chip erase takes ~20 s** (§2). Flashing tools that appear to hang during erase are usually not hung.
6. **Security registers have OTP lock bits** (`LB3..LB1`). Writing them is irreversible.
7. **166 MHz is the *device* limit, not the achievable system clock.** The ESP32-S3 tops out at 80 MHz for QIO in most configurations, and the board's 22 Ω clock resistor and trace lengths matter more than the die's rating. **[INF]**

---

## 9. Alternatives

| Part | vs. XM25UH128D | When |
|---|---|---|
| **[Winbond W25Q128JV](../../winbond/w25q128jv/README.md)** | The de-facto reference 128 Mbit SPI NOR; same command set, JEDEC ID `EF 40 18` | Widest tool and driver support. Documented in this repository |
| **[GigaDevice GD25Q64E](../../gigadevice/gd25q64e/README.md)** | 64 Mbit, otherwise comparable | Half the density. Documented in this repository |
| XMC **XM25QH128B** | XMC's other 128 Mbit line | Different series; check the supply range and sector granularity |
| XMC **XM25RH128D** / **XM25RU128C** | Same generation, different voltage/feature classes | 1.8 V-class designs |
| Macronix **MX25L12833F**, ISSI **IS25LP128** | Second sources | Supply-chain diversity |

XM25UH128D's distinguishing features against the Winbond baseline are the **DTR read modes** and the **0.2 µA deep power-down** — neither of which the ESP32-S3's flash driver uses by default. **[INF]**

---

## 10. Open questions

- The shipped `HOLD/RST` bit state (§5.2). It is the last link in the QIO chain not independently confirmed.
- Whether a PaperMono actually boots and runs stably in QIO — untested, no hardware.
- The fitted package. The ordering code says SOP-8 208 mil; the schematic symbol shows an 8-pin device but does not carry a footprint name in the extracted text.
- Whether XMC publishes an errata sheet for this part; only the datasheet was found.
- No hardware measurement of read throughput in DIO versus QIO on this board.

---

## Manufacturer

**Wuhan Xinxin Semiconductor Manufacturing Co., Ltd. (XMC)**, `www.xmcwh.com`. No vendor sourcing guide exists in this repository yet. The recipe that worked on 2026-09-01, recorded because the site's product table is JavaScript-rendered and the datasheet link is not in the HTML:

1. `POST https://www.xmcwh.com/product/getProductList` with `page=1&limit=500` returns the **entire 519-part catalogue** as JSON in one response. (Keyword parameters are ignored — filter client-side.)
2. Each record's `form_data.picture` field holds either a datasheet path (`/uploads/<id>/<PART>_VerX.Y.pdf`) or a `/site/support?...` link.
3. `https://www.xmcwh.com/uploads/1045/XM25UH128D_Ver1.2.pdf` served the document directly, `application/pdf`, `%PDF` verified.

Plain `curl` with a Chrome 131 User-Agent; no fallback needed, no login. Note the site's own JavaScript contains a commented-out branch that would have suppressed downloads for `description == 'XM25UH'` — the family this part belongs to. It is not active, but it suggests the availability of these documents has changed before and may change again.

## Related pages

- [Espressif ESP32-S3R8](../../espressif/esp32-s3r8/README.md) — the host, and the source of `VDD_SPI`
- [Winbond W25Q128JV](../../winbond/w25q128jv/README.md) — the equivalent part on other boards in this repository
- [GigaDevice GD25Q64E](../../gigadevice/gd25q64e/README.md) — 64 Mbit sibling class

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | XM25UH128D datasheet | Wuhan Xinxin Semiconductor Manufacturing Co., Ltd. (XMC) | primary | datasheet | <https://www.xmcwh.com/uploads/1045/XM25UH128D_Ver1.2.pdf> | 2026-09-01 | **Rev1.2**, 2025-06-12, 98 pp, 3 730 929 B | Ordering-code decode incl. **QE = 1 default**, JEDEC ID, all limits in §2, pin functions, status-register bit list, timing | `artifacts/xm25uh128d-datasheet-ver1.2.pdf` |
| S1 | `PaperMono_SCH_V0.6.2_20260522.pdf` | M5Stack | primary | schematic | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | V0.6.2, 6 sheets | The §4.1 pin/net table — **all four data lines routed**, `R39` = 22 Ω, `VDD_NOR` ← `VDD_SPI` | `devices/m5stack/papermono/artifacts/schematic/PaperMono_SCH_V0.6.2_20260522.pdf` |
| S2 | PaperMono product page — PlatformIO configuration | M5Stack | primary | official page | <https://docs.m5stack.com/en/core/PaperMono> | 2026-09-01 | — | `board_build.arduino.memory_type = qio_opi` | `archive/devices/m5stack/papermono/artifacts/research-scratch/docs/pages/en-core-PaperMono.html` |
| S3 | `C153-PaperMono-UserDemo-v1.2.bin` — ESP image headers and partition table | M5Stack | primary | firmware | M5Burner API, firmware id `2089640807996628993` | 2026-09-01 | v1.2, built 2026-08-06, `app_version c78f6c5-dirty`, IDF v5.5.1; 2 868 208 B, SHA-256 `72c290bc2ffa216041b276660277369bd17ecef92315e367d98bb2c96c8428fa` | `flash_mode: DIO` in both headers; the 15 MiB single-`factory` partition table | `archive/devices/m5stack/papermono/artifacts/research-scratch/docs/firmware/` |
| S4 | `M5PaperMono-UserDemo/sdkconfig.defaults`, `partitions.csv` | M5Stack | primary | repository | <https://github.com/m5stack/M5PaperMono-UserDemo> | 2026-09-01 | `main` @ `c1099107271d31a0678d661a896e2b04dbb331ea`, MIT | **No** `CONFIG_ESPTOOLPY_FLASHMODE_*` is set — the DIO header is an IDF default, not a decision | `archive/devices/m5stack/papermono/artifacts/source-snapshots/M5PaperMono-UserDemo/` |

**Local artifacts**

| File | Bytes | SHA-256 | Pages |
|---|---:|---|---:|
| `artifacts/xm25uh128d-datasheet-ver1.2.pdf` | 3 730 929 | `a6f683599543c81d36dff7f3a20dc6f5f637e9cac6554fa87873abaf2126c014` | 98 |

**Method note.** D1 validated as `%PDF`, 98 pages, text layer intact. The §5 resolution combines three independent `executed-success` observations — the schematic netlist, the datasheet's ordering table, and the firmware image header — rather than preferring one source over another.

## FCC internal photographs — confirmation of the fitted part (2026-09-20)

The PaperMono's FCC filing (`2AN3WM5PAPERMONO`) includes an internal-photograph
exhibit, retained at
[`devices/m5stack/papermono/artifacts/certification/`](../../../devices/m5stack/papermono/artifacts/certification/README.md).
It is the first physical-hardware evidence for this part.

**The `UH` is confirmed on the package.** Page 3 shows an SOP-8 beside the
ESP32-S3 marked with the **XMC** logo and, read at 16× magnification:

```
XMC
25UH128DHIG  15
P4J71900  2529K
```

| Field | Reading | Status |
|---|---|---|
| Manufacturer | **XMC** logo | **legible** |
| Family | **`25UH…`** | **legible** — this rules out the `XM25QH` family a casual reading might assume |
| Density | **`128`** = 128 Mbit = **16 MB** | **legible**, matches M5Stack's specification |
| Suffix | `DHI` then one further character | **the final character is not resolvable** — so `…DHIQT` versus `…DHIG` is **not** settled by the photograph |
| Lot / date | `P4J71900`, `2529K` | legible, not interpreted |

The record's part number `XM25UH128DHIQT` comes from the schematic and is not
contradicted; the photograph confirms the family, voltage class and density but
**cannot confirm the `QT` package/grade suffix**. Recorded as partially legible
rather than treated as a full reading.

Extraction: [`certification.md` §6](../../../devices/m5stack/papermono/certification.md#6--what-the-internal-photographs-show).
