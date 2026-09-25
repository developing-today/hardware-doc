# Cardputer ADV — coverage matrix

> Snapshot **2026-09-04**. Every advertised or fitted capability, mapped to hardware, evidence,
> guide and gap. **No hardware test was performed**, so the "hardware-tested" column is empty
> throughout and that is stated rather than left implicit.

| Feature | Hardware | Component record | Vendor doc | Vendor code | Community | Guide | Build-tested | HW-tested | Gap |
|---|---|---|---|---|---|---|---|---|---|
| Keyboard | TCA8418RTWR @ `0x34`, INT G11 | ✅ new | ✅ PinMap | ✅ `M5Cardputer` | ✅ Bruce, Launcher | [`keyboard.md`](features/keyboard.md) | ❌ | ❌ | per-switch nets for 54 of 56 keys not individually traced |
| Display | ST7789V2, SPI3 | ✅ existing | ✅ | ✅ M5GFX | ✅ TFT_eSPI, meshtastic/st7789 | [`display.md`](features/display.md) | ❌ | ❌ | no frame-rate measurement |
| Backlight | G38 → AW35122FDR → `BL_3V3` | ✅ existing | ⚠ warning omitted on the ADV page | ✅ M5GFX | — | [`display.md`](features/display.md) | ❌ | ❌ | — |
| RGB LED | WS2812, G21, on `BL_3V3` | ✅ new | ✅ | ✅ M5Unified | ✅ | [`display.md`](features/display.md) | ❌ | ❌ | — |
| Audio out | ES8311 + NS4150B + speaker | ✅ existing ×2 | ✅ | ✅ M5Unified | ✅ Bruce, pschatzmann | [`audio.md`](features/audio.md) | ❌ | ❌ | **live driver defect** §6.2 |
| 3.5 mm jack | PJ-342 + HP_DET + 2N7002T | ✅ generic | ✅ prose | ❌ hardware-only | ✅ | [`audio.md`](features/audio.md) | ❌ | ❌ | not software-visible |
| Microphone | MSM381A3729H9BP → ES8311 ADC | ✅ new | ✅ (SNR only) | ✅ M5Unified | ✅ | [`audio.md`](features/audio.md) | ❌ | ❌ | no level/SNR measurement |
| microSD | SPI G40/14/39, CS G12 | ✅ generic | ✅ | ✅ `_pin_table_sd` | ✅ every firmware | [`microsd.md`](features/microsd.md) | ❌ | ❌ | no card-compatibility data |
| IMU | BMI270 @ `0x69` | ✅ existing | ✅ + axis diagram | ✅ M5Unified | ✅ | [`imu.md`](features/imu.md) | ❌ | ❌ | **INT1/INT2 routing not established** |
| **RTC** | **none** | — | — | — | — | [`rtc.md`](features/rtc.md) | — | — | **verified absent** |
| Battery sense | divider → G10 (ADC1) | ✅ generic | ✅ | ✅ `Power_Class` | ✅ Bruce | [`battery-and-power.md`](features/battery-and-power.md) | ❌ | ❌ | curve shared with the v1.x despite a different cell |
| Charging | TP4057, R_PROG 3.3 k | ✅ existing | ✅ + switch warning | — | — | [`battery-and-power.md`](features/battery-and-power.md) | ❌ | ❌ | charge current **inferred** |
| 5 V boost | SY7088 | ✅ existing | ❌ | — | — | [`battery-and-power.md`](features/battery-and-power.md) | — | ❌ | output **inferred**; **no current limit published** |
| 3.3 V buck | SY8089 | ✅ new | ❌ | — | — | [`battery-and-power.md`](features/battery-and-power.md) | — | ❌ | **FB arithmetic does not resolve** |
| Supervisor | CN809J | ✅ new | ❌ | — | — | [`battery-and-power.md`](features/battery-and-power.md) | — | ❌ | threshold unknown |
| Wi-Fi | ESP32-S3 radio | ✅ new (SoC) | ✅ current only | ✅ stock | ✅ Marauder, Bruce, CSI | [`wifi-and-ble.md`](features/wifi-and-ble.md) | ❌ | ❌ | no RF measurement anywhere |
| BLE | ESP32-S3 radio | ✅ | ✅ | ✅ NimBLE in factory fw | ✅ ChimeraBLE | [`wifi-and-ble.md`](features/wifi-and-ble.md) | ❌ | ❌ | vendor current figure anomalous |
| IR TX | emitter, G44 | — | ✅ | ✅ factory fw + IRremote | ✅ Ultimate-Remote | [`ir.md`](features/ir.md) | ❌ | ❌ | **no range figure published for the ADV** |
| **IR RX** | **none** | — | — | — | Grove/CAP workarounds | [`ir.md`](features/ir.md) | — | — | **verified absent** |
| Grove / PORT.A | HY2.0-4P, G1/G2 | ✅ | ✅ | ✅ `Ex_I2C` | ✅ Bruce pin menus | [`grove-port.md`](features/grove-port.md) | ❌ | ❌ | ⚠ **SCL/SDA colour conflict C2** |
| **CAP header** | P3, 14-pin | — (interface) | ✅ ×2, ⚠ conflicting | ✅ factory fw + Meshtastic | ✅ 4+ community boards | [`cap-header.md`](features/cap-header.md) | ❌ | ❌ | **no current limit**; no ESD confirmed |
| USB | native OTG, no bridge | ✅ generic | ✅ download mode | ✅ build flags | ✅ BadCard | [`usb.md`](features/usb.md) | ❌ | ❌ | — |
| USB HID | native | — | — | ✅ example + `_kb_asciimap` | ✅ | [`usb.md`](features/usb.md) | ❌ | ❌ | — |
| BLE HID | NimBLE | — | ❌ | ✅ factory sdkconfig | — | [`usb.md`](features/usb.md), [`wifi-and-ble.md`](features/wifi-and-ble.md) | ❌ | ❌ | not documented by M5Stack |
| Boot / G0 button | Stamp, 10 k pull-up | ✅ generic | ✅ | ✅ | ✅ | [`usb.md`](features/usb.md) | ❌ | ❌ | — |
| Power switch | SW1 SPDT | — | ✅ charge warning | — | — | [`battery-and-power.md`](features/battery-and-power.md) | — | ❌ | SW2's function not established |
| Magnets / LEGO base | mechanical | — | ✅ | — | ✅ r/M5Stack thread | — | — | ❌ | — |
| Lanyard hole | mechanical | — | ✅ comparison table | — | — | — | — | ❌ | — |

## Component records

| Created by this pass | Reused (existing) | Created by a **concurrent session** — linked, not written |
|---|---|---|
| `texas-instruments/tca8418` · `generic/74hc138` · `espressif/esp32-s3fn8` · `memsensing/msm381a3729h9bp` · `knowles/spm1423hm4h-b` · `nsiway/ns4168` · `worldsemi/ws2812` · `consonance/cn809` · `silergy/sy8089` · `unidentified/cardputer/lp3218dt1g` | `everest-semiconductor/es8311` · `nsiway/ns4150b` · `bosch-sensortec/bmi270` · `awinic/aw35122` · `joulwatt/jw5712` · `generic/micro-sd-sdmmc` · `generic/3.5mm-audio-output` · `generic/charger-power-path` | `m5stack/stamp-s3` · `m5stack/stamp-s3a` · `sitronix/st7789v2` · `silergy/sy7088` · `sgmicro/sgm2578` · `generic/tp4057` · `unidentified/m5stack-stamp-s3a/dcdc-u4` |

*Used By* additions for the middle and right columns are staged in
[`archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md`](../../../archive/devices/m5stack/shared-artifacts/cardputer/research-scratch/index-fragments.md).

## Uncovered

| Item | Why |
|---|---|
| Certification | `/en/certification` not fetched with a positive control — **"not established"**, not "absent" |
| I²C address table (`/en/product_i2c_addr`) | same |
| UiFlow2 / Arduino tutorial sub-pages | not fetched |
| `M5_Hardware` structure/CAD directories | not fetched |
| Factory firmware **binary** | not retrieved; no M5Burner id resolved |
| Any measurement of anything | no hardware |
| SW2's function | not traced |
| Chinese and Japanese community sources | not searched |
