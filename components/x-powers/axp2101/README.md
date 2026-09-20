# X-Powers AXP2101

- **Category:** highly integrated single-cell Li-ion **power-management IC** — charger, multi-rail regulator (DC-DCs + ALDO/BLDO/DLDO/CPUSLDO), power-key controller, ADC/fuel-gauge inputs, watchdog, backup-battery charger
- **Manufacturer:** X-Powers (Shenzhen X-Powers Technology / 芯智慧)
- **Host interface:** I²C, slave address **`0x34`**
- **Document status:** datasheet **V1.4, English** — retained in [`artifacts/`](artifacts/)
- **Research status:** **stub-plus.** The datasheet is held and the part's identity on one board is firmly established, but the register map has **not** been mined and no independent audit of the vendor driver against the datasheet has been done. What is written below is what the evidence supports.
- **Retrieved:** 2026-09-01. **Nothing verified on hardware.**

## Why this record exists: a marketing-versus-silicon conflict

This part is documented here primarily because **Waveshare does not call it by its
name.** Both the storefront and the official documentation for the
[ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md)
describe the PMIC as a **"TG28"**:

> "Onboard **TG28** power management chip … supports outputting multiple configurable
> voltages, and integrates charging and battery management functions"

Two higher-authority sources say otherwise:

| Source | Evidence | Class |
|---|---|---|
| **Board schematic** | Part label `AXP2101`, with nets `ALDOIN`, `ALDO1`–`ALDO4`, `BLDOIN`, `BLDO1`–`BLDO2`, `DLDO1/DC1SW`, `DLDO2/DC4SW`, `CPUSLDO`, `VSYS`, `PWRON`, `PWROK`, `VBACKUP` — **these are the AXP2101's own pin names** | primary, design data |
| **Waveshare's own firmware** | Component directory named `axpPower/`; `static XPowersPMU axp2101;`; `axp2101.begin(AXP2101_SLAVE_ADDRESS, …)`; vendored `REG/AXP2101Constants.h` and `XPowersAXP2101.tpp` | primary, source |

Under this repository's Waveshare trust order
([vendor guide §4](../../../vendors/waveshare/README.md): schematic > demo source >
wiki > storefront), **both higher-ranked sources agree against both lower-ranked
ones**. The fitted part is an AXP2101.

**What "TG28" refers to is unexplained.** No datasheet, product page or registry
entry for a PMIC of that name was found in this pass. It may be a marking variant, a
second-source, or an error copied from another product. **No `tg28` component record
has been created** — that would be a part number promoted from marketing copy, which
the method's
[evidence-discipline rules](../../../.agents/skills/hardware-device-research/SKILL.md#evidence-discipline-and-known-failure-modes)
forbid. Recorded as an open question in
[C-WS2](../../../devices/waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws2--tg28-versus-axp2101).

## Rails observed on a real design

Named on the ESP32-S3-ePaper-3.97 schematic. This is **that board's** use of the
part, not a general pinout:

| Rail | Present | Configured to | Evidence |
|---|---|---|---|
| `DC1` (via `DLDO1/DC1SW`) | yes | **3300 mV** | vendor source `axp_prot.cpp:53` |
| `ALDO1` | yes | **3300 mV** | `:55` |
| `ALDO2` | yes | **3300 mV** | `:56` |
| `ALDO3` | yes | **3300 mV** | `:57` |
| `ALDO4` | yes | not set in the sampled source | schematic |
| `BLDO1`, `BLDO2` | yes | not set in the sampled source | schematic |
| `CPUSLDO` | yes | — | schematic |
| `VBACKUP` | yes | RTC coin cell, charge target **3000 mV** | `:116` |
| `VSYS`, `PWRON`, `PWROK` | yes | power sequencing and key | schematic |

## Capabilities exercised by a shipping driver

Read from Waveshare's `axp_prot.cpp` at commit `9b12d40`. These are **firmware
settings, not silicon limits** — a different program may choose differently.

| Capability | Setting | Line |
|---|---|---|
| VBUS voltage limit | 4.36 V | `:46` |
| VBUS current limit | **1500 mA** | `:47` |
| System power-down voltage | 2600 mV | `:50` |
| Precharge current | 50 mA | `:101` |
| Constant-current charge | **200 mA** | `:102` |
| Termination current | 25 mA | `:103` |
| Charge target voltage | **4.2 V** | `:106` |
| Power-key press-off hold | 4 s | `:61` |
| Power-key press-on hold | 1 s | `:76` |
| Watchdog | 4 s, **IRQ to pin** | `:110`–`:112` |
| Backup-battery charging | **enabled**, 3.0 V | `:116`–`:117` |
| Low-battery warning | 10 % | `:119` |
| Measurements enabled | die temperature, battery detect, VBUS voltage, battery voltage, system voltage | `:91`–`:95` |
| Charge LED | off | `:98` |

That list is a reasonable summary of what the part does: **it charges a cell, powers
several rails, debounces a power button, watches the system, and measures itself.**

### Two things worth flagging to anyone using this part

Both `inferred` from reading the vendor driver, neither reproduced:

1. **The watchdog is enabled and never fed** in the sampled code — `clrWatchdog()` is
   present but commented out at `:113`. Configured as `WDT_IRQ_TO_PIN`, so it raises
   an interrupt rather than resetting, and is therefore **a latent trap, not an
   active defect**. If a derived design promotes the watchdog to reset without adding
   a feed, it becomes a 4-second reboot loop.
2. **Backup-battery charging is enabled unconditionally.** If a **non-rechargeable**
   coin cell is fitted to the RTC backup header, this charges a primary cell. Worth a
   warning in any product derived from a board that does this.

## What has *not* been done

Stated plainly so the next pass knows where to start:

- **The datasheet has not been mined.** No register map, no electrical limits, no
  package or thermal data has been transcribed from the held V1.4 document.
- **No audit of XPowersLib against the datasheet.** The method's
  [step 10](../../../.agents/skills/hardware-device-research/SKILL.md#10-audit-vendor-firmware-and-driver-source-against-the-primary-documents)
  asks for exactly that, and it is the obvious next piece of work — the library is
  widely used well beyond Waveshare.
- **No lifecycle, pricing, packaging or availability information.**
- **No comparison** against the obvious alternatives (AXP192/AXP202 in the same
  family; BQ25896 and SY6970, whose constants XPowersLib also ships).

## Artifacts

| File | Bytes | SHA-256 | Source | Retrieved | Version |
|---|---|---|---|---|---|
| [`artifacts/axp2101-datasheet-v1.4-en-xpowerslib-mirror.pdf`](artifacts/axp2101-datasheet-v1.4-en-xpowerslib-mirror.pdf) | 1 554 740 | `9e51d16d84d905c32a001a123be8e6c58213ee21e42d5bdb1458b731dba10f6d` | `https://raw.githubusercontent.com/lewisxhe/XPowersLib/master/datasheet/AXP2101_Datasheet_V1.4_en.pdf` | 2026-09-01 | **V1.4, English** |

**This is a community mirror, not the manufacturer's copy.** X-Powers publishes no
accessible primary URL that this pass could find. Two direct attempts failed and
**neither was retained under a `.pdf` name**:

| Attempt | Result |
|---|---|
| `files.waveshare.com/wiki/common/AXP2101.pdf` | HTTP 404, body was XML |
| `github.com/lewisxhe/XPowersLib/raw/master/datasheet/AXP2101_Datasheet_V1.0_en.pdf` | HTTP 404, body was **267 330 bytes of HTML** — a size that would pass a naive length check |

The working filename was found by listing the repository directory through the GitHub
API rather than guessing. Validated by magic bytes (`%PDF-`).

**Licence `unknown`.** The document states no terms; the hosting library is MIT but a
library's licence does not govern a manufacturer datasheet it redistributes.
Disposition: `repository`. If X-Powers' own copy is later located, keep both and hash
them — mirrors of this document may well differ by revision, as
[has already happened](../../nxp/pcf85063a/README.md) with another datasheet on the
same board.

## Used by

- [LilyGO T-Display AMOLED Lite (1.47″)](../../../devices/lilygo/t-display-amoled-lite/README.md) — designator `U5`, the **only full PMU anywhere in the [LilyGO T-Display-S3 family](../../../devices/lilygo/t-display-s3-shared/README.md)**. It is fitted because that board's [SH8501B](../../shenghe-microelectronics/sh8501b/README.md) AMOLED panel runs at **1.8 V** behind an RS0108 level translator and needs rails the family's other boards do not. Driven with `lewisxhe/XPowersLib`; LilyGO ships `examples/PMU_ADC` and `examples/PMU_Interrupt` marked *“only support 1.47-inch AMOLED”*. PMU interrupt GPIO3; I²C SDA GPIO1 / SCL GPIO2 per `LilyGo-Display-IDF/main/product_pins.h` @ `b1a1cc54994bf1b417e3bb30c437bbe1036bff7f`. Every other board in that family uses a plain charger instead — [SY6970](../../silergy/sy6970/README.md), [BQ25896](../../texas-instruments/bq25896/README.md) or a linear [TP4065-class part](../../nanjing-top-power/tp4065/README.md). *(Added 2026-09-07.)*

### [Waveshare ESP32-S3-ePaper-3.97](../../../devices/waveshare/esp32-s3-epaper-3.97/README.md)

The board's **sole** power-management device. On the shared I²C bus at `0x34`
(GPIO41 SDA / GPIO42 SCL), with `PWR_IRQ` on GPIO38, `ESP_CHG` on GPIO2 and
`PWR_OUT` on GPIO1. It owns:

- the 3.3 V logic rail and the e-paper panel supply (`EPD_VCC_AXP`),
- charging of the MX1.25/PH1.25 3.7 V Li-ion on header `H3`,
- charging of the RTC backup cell on header `H4`,
- the **PWR button**, which is why that button is described as programmable — it is a
  PMIC input, not a GPIO.

Consequence for developers: **on this board the PMIC gates the display.** Ignoring
the AXP2101 makes battery and panel behaviour inexplicable. Details in
[pinouts-and-buses.md § Power domains](../../../devices/waveshare/esp32-s3-epaper-3.97/pinouts-and-buses.md#power-domains)
and [development.md](../../../devices/waveshare/esp32-s3-epaper-3.97/development.md).

Marketed by Waveshare as "TG28" — see the [conflict](#why-this-record-exists-a-marketing-versus-silicon-conflict).

## See also

- [XPowersLib](https://github.com/lewisxhe/XPowersLib) — the de-facto driver, vendored by Waveshare
- [All components](../../README.md)
