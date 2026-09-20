# Development, examples and firmware — Waveshare ESP32-S3-ePaper-3.97

> Research snapshot **2026-09-01**. **Nothing here was built, flashed or run.**
> Every procedure is `reported-working` (it is what the vendor publishes) or
> `inferred`. There is no `executed-success` claim about the device in this file.

## Target summary

| Field | Value | Evidence |
|---|---|---|
| MCU | ESP32-S3R8 in an **`ESP32-S3-WROOM-1-N16R8`** module | schematic part label `S05` |
| Flash | **16 MB** external (module) | `N16R8` suffix; docs `S02` |
| PSRAM | **8 MB octal** | `N16R8`; consumes GPIO35–37 |
| Console / flashing | **USB Type-C → native USB** (GPIO19/20) | schematic `S05` |
| USB-UART bridge | **none fitted** | no bridge part in the schematic text layer; `inferred` |
| Download mode | Hold **BOOT**, power on again | docs `S02` |
| Frameworks | **Arduino IDE** and **ESP-IDF** — vendor supports both | docs `S02` |
| Board support package | **none published** on the Espressif component registry (unlike some Waveshare boards) | `inferred` from absence in `S03` |

Because there is **no USB-UART bridge**, the serial port disappears when the
application crashes or when USB-CDC is not initialised. That is the normal
native-USB ESP32-S3 trade-off, and the BOOT-button entry path is the recovery.
`inferred` from the connector census — not tested.

## Official examples

From `waveshareteam/ESP32-S3-ePaper-3.97` at commit
**`9b12d40731a80213b927ee8a421cae4082952819`** (2026-03-20). Enumerated from the
repository tree; **not cloned, not built** ([G2](gaps-and-conflicts.md#gaps)).

### Arduino — `Arduino/examples/`

| Example | Exercises | Notable contents |
|---|---|---|
| `01_Audio_Test` | [ES8311](../../../components/everest-semiconductor/es8311/README.md) codec + mic + [NS4150B](../../../components/nsiway/ns4150b/README.md) | Ships its own `es8311.cpp`/`es8311_reg.h` rather than a library |
| `02_E-Paper_Example` | **The display** | `EPD_3in97.cpp/.h`, `GUI_Paint`, six fonts incl. two CJK. **This is the reference for the pin map** |
| `03_I2C_PCF85063` | [RTC](../../../components/nxp/pcf85063a/README.md) | Adds `i2c_bsp.c`, `i2c_equipment.cpp`, `user_config.h` |
| `04_I2C_SHTC3` | [Temp/humidity](../../../components/sensirion/shtc3/README.md) | |
| `05_SD_Test` | microSD | **Read this to settle [C-WS5](gaps-and-conflicts.md#c-ws5--sd-card-spi-names-but-4-bit-nets)** |
| `06_QMI8658A` | [IMU](../../../components/qst/qmi8658a/README.md) | Uses the bundled `SensorLib` |

Bundled library: `Arduino/libraries/SensorLib` — upstream is `lewisxhe/SensorLib`.
**Version and modification status not determined** in this pass; per the method's
vendored-dependency rule that is an open item, not an assumption of equivalence.

### ESP-IDF — `ESP-IDF/`

| Project | Exercises |
|---|---|
| `01_E-Paper_Example` | Display |
| `02_Mic_test` | Microphone capture |
| `03_Music` | Playback through the amplifier |
| `04_SD_Test` | microSD |
| `05_QMI8658A` | IMU |
| `06_I2C_PCF85063` | RTC |
| `07_I2C_SHTC3` | Temp/humidity |
| `08_ESP32-S3_e-Paper-3.97` | **The integrated application** — this is the one that contains `components/axpPower/` |

`08_…/components/axpPower/` vendors **XPowersLib** (`lewisxhe`): `XPowersLib.h`,
`XPowersAXP2101.tpp`, `XPowersCommon.tpp`, `XPowersLibInterface.cpp`, and
`REG/AXP2101Constants.h` alongside constants for AXP192/AXP202/AXP216, BQ25896,
SY6970 and HUSB238 that this board does not fit. Waveshare's own wrapper is
`axp_prot.cpp` / `axp_prot.h`.

**No ESP-IDF or Arduino-core version is declared anywhere** in the repository or the
docs — no `idf_component.yml` version pin, no `platformio.ini`, no stated minimum.
That is a genuine gap: contrast the
[Knob-Touch-LCD board](../esp32-s3-knob-touch-lcd-1.8/development.md), where
Waveshare states its toolchain versions.

## What the vendor's power code actually does

This is the highest-value read in the repository, because it settles
[C-WS2](gaps-and-conflicts.md#c-ws2--tg28-versus-axp2101) and gives real numbers.
From `ESP-IDF/08_ESP32-S3_e-Paper-3.97/components/axpPower/axp_prot.cpp` at `9b12d40`:

```cpp
static XPowersPMU axp2101;                                    // :14
axp2101.begin(AXP2101_SLAVE_ADDRESS, read, write)             // :40
axp2101.setVbusVoltageLimit(XPOWERS_AXP2101_VBUS_VOL_LIM_4V36);  // :46
axp2101.setVbusCurrentLimit(XPOWERS_AXP2101_VBUS_CUR_LIM_1500MA);// :47
axp2101.setSysPowerDownVoltage(2600);                         // :50
axp2101.setDC1Voltage(3300);                                  // :53
axp2101.setALDO1Voltage(3300); …ALDO2… …ALDO3…                // :55–57
axp2101.setChargerConstantCurr(XPOWERS_AXP2101_CHG_CUR_200MA);// :102
axp2101.setChargeTargetVoltage(XPOWERS_AXP2101_CHG_VOL_4V2);  // :106
axp2101.setWatchdogTimeout(XPOWERS_AXP2101_WDT_TIMEOUT_4S);   // :111
axp2101.setButtonBatteryChargeVoltage(3000);                  // :116
axp2101.enableButtonBatteryCharge();                          // :117
axp2101.setLowBatWarnThreshold(10);                           // :119
```

Full table in [pinouts-and-buses.md § Power domains](pinouts-and-buses.md#power-domains).

### Audit notes against the AXP2101 datasheet

Read side by side with
[`components/x-powers/axp2101`](../../../components/x-powers/axp2101/README.md)
(datasheet V1.4 held). Findings, all `inferred` from reading — none reproduced on
hardware:

1. **The PMIC watchdog is enabled with a 4 s timeout and routed to a pin**
   (`:110`–`:112`), and the commented-out `clrWatchdog()` at `:113` means **the
   sampled code never feeds it**. If `XPOWERS_AXP2101_WDT_IRQ_TO_PIN` only raises
   `PWR_IRQ` this is benign; if a later configuration promotes it to reset, an
   application that does not feed the dog gets a 4-second reboot loop. **Flagged as
   a latent trap, not an active defect** — the mode configured is the IRQ one.
2. **`setSysPowerDownVoltage(2600)`** is a hard cut-off at 2.6 V system rail. For a
   single Li-ion that is well below the cell's safe floor, so the *battery*
   protection is expected to act first — the AXP2101 value is a backstop.
3. **RTC coin-cell charging is enabled unconditionally** at 3.0 V (`:116`–`:117`).
   If a user fits a **non-rechargeable** cell to `H4`, this charges a primary cell.
   Worth a warning in any derived product. `inferred` — the header is documented
   only as "RTC backup battery".
4. **Charging is fixed at 200 mA CC / 4.2 V** with no battery-capacity awareness.
   Fine for the bundled cell; check it if you fit a small one.

## Flashing

### Factory restore

Two images in `Firmware/Factory procedure/`, each **16 777 216 bytes** — a full
16 MB flash image, so they are merged images:

| File | Bytes | Role |
|---|---|---|
| `260304.bin` | 16 777 216 | Full-flash factory image |
| `260314.bin` | 16 777 216 | Full-flash factory image, later build |

`Firmware/ReadMe_EN.txt`, verbatim:

```
Burn the website
https://espressif.github.io/esp-launchpad/

Burn the starting address
0x0
```

So: **offset `0x0`**, via ESP Launchpad or equivalently `esptool`. The filenames look
like dates (`26-03-04`, `26-03-14`) consistent with the repository's commit history,
but that is a **reading of a filename, not a build identifier** — no image header was
parsed. `inferred`.

**Inferred equivalent, NOT tested — do not treat as authoritative:**

```bash
# INFERRED from the vendor's stated offset. Not executed. Back up first.
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
           write_flash 0x0 260314.bin
```

Neither image was downloaded ([G3](gaps-and-conflicts.md#gaps)); both are recorded in
[`acquisition/manifest.json`](acquisition/manifest.json) with URLs and expected sizes
so a later pass can fetch and hash them.

### The xiaozhi AI-voice firmware

`Firmware/xiaozhi/` ships two prebuilt images:

| File | Bytes | Per `ReadMe_EN.txt` |
|---|---|---|
| `ESP32-S3_e-Paper-3.97_xiaozhi.bin` | 9 920 235 | "Pure voice, no display" |
| `ESP32-S3_e-Paper-3.97_xiaozhi-xs.bin` | 11 179 471 | "The e-ink screen is displayed in landscape" |

Upstream source is **`github.com/78/xiaozhi-esp32`**, which the repository README
points at explicitly ("Please visit the official source code"). This is what the
storefront means by "AI Voice Interaction" and "access to online large model
platforms such as DeepSeek, Doubao" — **a third-party open-source assistant firmware,
not a Waveshare service.** Worth knowing before buying the board for that feature:
the cloud dependency and its terms are xiaozhi's, not Waveshare's.

**Neither image was downloaded or parsed.** No SHA-256, no partition map, no IDF
version. Recorded in the acquisition manifest.

## Licensing

| Artifact | Licence | Evidence | Redistribution | Disposition |
|---|---|---|---|---|
| `waveshareteam/ESP32-S3-ePaper-3.97` | **`unknown`** | No `LICENSE` file; GitHub API reports `license: null` | `unknown` | reference-only (not vendored) |
| Bundled `XPowersLib` | upstream is MIT — **not verified in the vendored copy** | `inferred` | `unknown` | not vendored |
| Bundled `SensorLib` | upstream MIT — **not verified** | `inferred` | `unknown` | not vendored |
| Schematic PDF | `unknown` — no notice in the document | `unknown` | repository |
| Panel manual, IC datasheets | `unknown` — vendor documents, no stated terms | `unknown` | repository |

Per the method, licence is **metadata, not a gate**: everything useful was fetched,
and `unknown` is the ordinary value here. Nothing was omitted over licensing.

Note the contrast with Waveshare's ESP32-P4 repositories, which
[the vendor guide §8.4](../../../vendors/waveshare/README.md) records as
**Apache-2.0**. This repository is not licensed. That is a per-repository fact, not a
vendor-wide one.

## What a first project should do

`inferred` guidance, offered as a starting order rather than a tested procedure:

1. Flash `260314.bin` at `0x0` **after** dumping the existing flash — there is no
   published guarantee the images match a given board revision.
2. Build `Arduino/examples/02_E-Paper_Example` first. It is the smallest thing that
   proves toolchain, USB and panel together, and its pin map is corroborated by the
   schematic.
3. Add the AXP2101 early rather than late. On a board where the PMIC owns the panel
   rail and the power button, ignoring it makes battery behaviour inexplicable.
4. Treat GPIO43/44 carefully — they are the console *and* the LEDs
   ([C-WS9 neighbourhood](gaps-and-conflicts.md)).

## See also

- [Device record](README.md) · [Pinouts and buses](pinouts-and-buses.md)
- [Conflicts](gaps-and-conflicts.md) · [Sources](sources.md) · [Commands](commands.md)
- [Acquisition manifest](acquisition/manifest.json)
