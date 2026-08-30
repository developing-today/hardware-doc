# Bosch Sensortec BMI270

> 6-axis IMU — 3-axis accelerometer + 3-axis gyroscope, with an on-chip feature engine and a mandatory 8 KB configuration-file upload at every power-up.
> Research snapshot **2026-08-30**. Fitted as `U33` on the Nicolai Electronics Tanmatsu. **No hardware was available**; all claims trace to the datasheet, the published KiCad design, or the vendor BSP source.

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DOC]** | Bosch Sensortec BMI270 datasheet, document number **BST-BMI270-DS000-08**, 150 pp — local copy `artifacts/bst-bmi270-ds000.pdf` |
| **[PCB]** | `tanmatsu.kicad_pcb` pad→net assignments (`tanmatsu-hardware`, CERN-OHL-P) |
| **[BSP]** | Badge.Team BSP `targets/tanmatsu/badge_bsp_orientation.c` (MIT), snapshot in the device tree |
| **[INF]** | Author inference, flagged as such |

Nothing below is hardware-verified.

---

## 1. Identity, variants and lifecycle

| Property | Value | Source |
|---|---|---|
| Part | **BMI270** | [DOC] |
| Function | 6-axis IMU: 3-axis accel + 3-axis gyro, plus feature engine | [DOC] |
| Package | **LGA-14**, 2.5 × 3.0 × 0.8 mm | [DOC] |
| Interfaces | I²C (up to Fm+ 1 MHz) or SPI (4-wire / 3-wire) | [DOC] §6 |
| I²C addresses | **0x68** (SDO = GND) or **0x69** (SDO = VDDIO) | [DOC] §6 |
| `CHIP_ID` (reg `0x00`) | **`0x24`** | [DOC] §5.2.1 |
| VDD | 1.71 – 3.6 V | [DOC] |
| VDDIO | 1.2 – 3.6 V, **independent of VDD** | [DOC] |
| FIFO | **2 KB** | [DOC] |
| Lifecycle | Active, high volume. Bosch's mainstream wearable IMU | [DOC] |
| LCSC | [`C2836813`](https://www.lcsc.com/search?q=C2836813) | BOM |

### 1.1 Family — and the one that will actually bite you

The BMI2xx parts share a driver framework (`BMI2-Sensor-API`) and much of the register map, but **not the configuration file**:

| Part | Notes |
|---|---|
| **BMI270** | The part here. Wearable feature set. `CHIP_ID = 0x24` |
| BMI260 | Same silicon family, different feature set / config blob. `CHIP_ID = 0x27` |
| BMI261, BMI263, BMI268, BMI270 Legacy | Variants differing chiefly in the shipped feature engine firmware |
| BMI160 | **Predecessor, and completely different.** No config upload, different register map, `CHIP_ID = 0xD1` |
| BMI08x | Separate high-performance line, not a substitute |

> ⚠ **The 8 KB config file is part-specific and is not interchangeable.** Uploading the BMI260 blob to a BMI270 leaves `INTERNAL_STATUS.message ≠ 0b0001` and the feature engine dead, while raw accel/gyro reads still appear to work — which is exactly what makes it hard to diagnose. Always check `CHIP_ID` **and** `INTERNAL_STATUS`.
>
> A "BMI270 driver" ported from a BMI160 driver is a common failure. The BMI160 needs no config upload, so a port that drops the upload step yields a chip that reads plausible-looking raw data with none of the features, and with the datasheet's guaranteed performance figures not applicable.

---

## 2. Key capabilities **[DOC §Key features]**

| Capability | Value |
|---|---|
| Accelerometer ODR | **0.78 Hz … 1.6 kHz** |
| Gyroscope ODR | **25 Hz … 6.4 kHz** |
| Accel ranges | ±2 g / ±4 g / ±8 g / ±16 g |
| Gyro ranges | ±125 / ±250 / ±500 / ±1000 / **±2000 dps** |
| Data width | **16-bit, two's complement** |
| Low-pass filter BW | accel 5.5 … 740 Hz; gyro 11 … 751 Hz, programmable |
| Gyro noise density | typ. **< 7 mdps/√Hz** in performance mode |
| Start-up time | **2 ms** for both accel and gyro (fast start) |
| FIFO | 2 KB, holds accel + gyro + timestamps + AUX data |
| Aux interface | I²C master hub for **one** auxiliary sensor (e.g. magnetometer), data-synchronised |
| OIS interface | Independent 10 MHz slave SPI, up to 6.4 kHz ODR, ~680 µs group delay |
| Sync accuracy | accel/gyro/aux hardware-synchronised **< 1 µs**; sensortime to host **< 40 µs** |
| Interrupt pins | **2** independent, programmable |

**Feature engine (the reason the config upload exists) [DOC]:** significant motion, any-motion, no-motion, motion detect, stationary detect, wrist-wear wakeup, wrist-worn step counter and detector, activity-change recognition, push-arm-down, pivot-up, wrist-jiggle, flick-in/out.

These are computed on-chip so the host can stay asleep. On a device that does not wake on motion, none of it is used — but you still must upload the blob, because the same firmware image also implements parts of the normal data path.

---

## 3. Power modes **[DOC §4.5, Table 6]**

The mode is a *combination* of `PWR_CTRL`, `PWR_CONF` and the `*_filter_perf` / `gyr_noise_perf` bits, not a single field:

| Mode | `acc_en` | `gyr_en` | `acc_filter_perf` | `gyr_filter_perf` | `gyr_noise_perf` | `adv_power_save` | Typ. current |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---:|
| **Suspend** | 0 | 0 | X | X | X | 1 | **3.5 µA** |
| **Configuration** | 0 | 0 | X | X | X | 0 | 120 µA |
| Low power — accel only | 1 | 0 | 0 | X | X | 1 | down to **4 µA** |
| Low power — gyro only | 0 | 1 | X | 0 | 0 | 1 | down to 400 µA |
| Low power — IMU | 1 | 1 | 0 | 0 | 0 | 1 | down to 420 µA |
| Normal — accel only | 1 | 0 | 1 | X | X | X | 210 µA |
| Normal — gyro only | 0 | 1 | X | 1 | 0 | X | 600 µA |
| **Normal — IMU** | 1 | 1 | 1 | 1 | 0 | X | **685 µA** |
| Performance — gyro only | 0 | 1 | X | 1 | 1 | X | 900 µA |
| Performance — IMU | 1 | 1 | 1 | 1 | 1 | X | **970 µA** |

Two things follow immediately for a battery device:

1. **The gyroscope dominates.** Accel-only normal mode is 210 µA; adding the gyro takes you to 685 µA, and performance mode to 970 µA. If you only need orientation/tilt, **do not enable the gyro** — a factor of three.
2. **Suspend is 3.5 µA and retains configuration**, including the uploaded config file **[DOC §4.5: "In all global power configurations both register contents and FIFO contents are retained"]**. So you do not need to re-upload 8 KB on wake from suspend — only after a genuine POR or soft reset. This is worth exploiting; the upload takes ~7 ms plus a 20 ms status wait.

### 3.1 ⚠ `adv_power_save` changes the interface timing rules

The device comes up **with `adv_power_save = 1` after POR or soft reset [DOC §4.4]**. In that state **[DOC §4.5]**:

- **Register writes require an inter-write delay of at least 450 µs.** Back-to-back writes without the delay are silently dropped. This alone accounts for a large share of "my BMI270 init doesn't take" reports.
- Sensors still log into the FIFO in all power modes, but you must clear `adv_power_save` and respect the §6.4/§6.5 timing before reading the FIFO.

Clearing `PWR_CONF.adv_power_save` makes the device fully accessible after 450 µs.

---

## 4. The initialisation sequence — the classic gotcha **[DOC §4.4 (a)(b)(c), §7]**

This is the single most important thing to get right, and it is the thing lightweight drivers omit.

```
1.  Power up. POR runs automatically. Interface comes up in I²C.
      (If using SPI: perform one dummy read first — the initial dummy
       read is what switches the interface to SPI. [DOC §4.4a])

2.  Read CHIP_ID (0x00). Expect 0x24. Verifies communication.

3.  Disable advanced power save:
      write_reg(0x7C, 0x00)            # PWR_CONF.adv_power_save = 0
    wait >= 450 µs                     # minimum; >=450 µs recommended

4.  Prepare config load:
      write_reg(0x59, 0x00)            # INIT_CTRL = 0x00

5.  Burst-write the 8 KB configuration file to INIT_DATA:
      burst_write_reg(0x5E, init_array[])     # start at byte 0
    ~6.6 ms at 10 MHz SPI. Over I²C at 400 kHz this is ~200 ms.

    If writing in chunks, INIT_ADDR_0 (0x5B) and INIT_ADDR_1 (0x5C)
    must be incremented by the length of each chunk between writes.
    [DOC §4.4b]

6.  Complete config load:
      write_reg(0x59, 0x01)            # INIT_CTRL = 0x01

7.  wait >= 20 ms, then:
      read_reg(0x21)                   # INTERNAL_STATUS
    Check INTERNAL_STATUS.message == 0b0001.
    Anything else means initialisation FAILED. [DOC §4.4c]

8.  Only now configure ACC_CONF / GYR_CONF / ranges and enable
    sensors via PWR_CTRL.
```

The config file itself is **not in the datasheet**. It is the `bmi270_config_file[]` array in Bosch's own driver, and the datasheet says so explicitly, citing
`https://github.com/BoschSensortec/BMI270-Sensor-API/blob/master/bmi270.c` **[DOC §4.4b footnote 3]**.

**Practical consequences:**

- **You cannot write a BMI270 driver from the datasheet alone.** You need Bosch's ~8 KB blob. This is unusual among IMUs and is the reason almost everyone uses the vendor API rather than rolling their own.
- The blob costs **8 KB of flash** in your firmware image. On a constrained MCU that is a real budget line.
- **Step 7 is not optional and is frequently skipped.** Without checking `INTERNAL_STATUS`, a failed upload presents as a working chip with subtly wrong behaviour rather than an error.
- Over I²C at 400 kHz the upload is slow enough (~200 ms) that it belongs in a background init task, not in a hot path. [INF]
- After the upload, **do not soft-reset** (`CMD = 0xB6`) unless you intend to re-upload. Soft reset restores `adv_power_save = 1` and discards the config.

---

## 5. Register map — landmarks **[DOC §5.2]**

The full map is 128 registers; these are the ones a driver touches. Values are from the datasheet section numbers cited.

| Addr | Name | Purpose |
|---|---|---|
| `0x00` | `CHIP_ID` | **0x24** for BMI270 |
| `0x02` | `ERR_REG` | Fatal / internal error flags |
| `0x03` | `STATUS` | `drdy_acc`, `drdy_gyr`, `drdy_aux`, `cmd_rdy` |
| `0x04`–`0x07` | `DATA_0`–`DATA_3` | AUX sensor data |
| **`0x0C`–`0x11`** | **`DATA_8`–`DATA_13`** | **Accelerometer X/Y/Z, 16-bit LSB-first** |
| **`0x12`–`0x17`** | **`DATA_14`–`DATA_19`** | **Gyroscope X/Y/Z, 16-bit LSB-first** |
| `0x18`–`0x1A` | `SENSORTIME_0..2` | 24-bit sensor timestamp |
| `0x1C` | `INT_STATUS_0` | Feature-engine interrupt status |
| `0x1D` | `INT_STATUS_1` | Data-ready / FIFO interrupt status |
| **`0x21`** | **`INTERNAL_STATUS`** | **`message` field — `0b0001` = init OK.** See §4 |
| `0x24`–`0x25` | `FIFO_LENGTH_0/1` | Bytes currently in FIFO |
| `0x26` | `FIFO_DATA` | FIFO read port |
| `0x2F` | `FEAT_PAGE` | Selects which feature-engine page `0x30`–`0x3F` maps to |
| `0x30`–`0x3F` | `FEATURES` | Paged feature-engine config/results (step count, etc.) |
| **`0x40`** | **`ACC_CONF`** | `acc_odr[3:0]`, `acc_bwp[2:0]`, `acc_filter_perf` |
| **`0x41`** | **`ACC_RANGE`** | `acc_range[1:0]` — 00=±2 g, 01=±4 g, 10=±8 g, 11=±16 g |
| **`0x42`** | **`GYR_CONF`** | `gyr_odr[3:0]`, `gyr_bwp[1:0]`, `gyr_noise_perf`, `gyr_filter_perf` |
| **`0x43`** | **`GYR_RANGE`** | `gyr_range[2:0]`, `ois_range` |
| `0x44` | `AUX_CONF` | Auxiliary sensor ODR/config |
| `0x48`/`0x49` | `FIFO_CONFIG_0/1` | What goes into the FIFO, and stop-on-full |
| `0x4B` | `AUX_DEV_ID` | I²C address of the aux sensor |
| `0x4C` | `AUX_IF_CONF` | `aux_manual_en` — setup vs. data mode |
| `0x4D`/`0x4E`/`0x4F` | `AUX_RD_ADDR` / `AUX_WR_ADDR` / `AUX_WR_DATA` | Aux register access |
| **`0x53`** | **`INT1_IO_CTRL`** | INT1 direction, **open-drain**, level, output enable |
| `0x54` | `INT2_IO_CTRL` | Same for INT2 |
| `0x56`/`0x57` | `INT1_MAP_FEAT` / `INT2_MAP_FEAT` | Route feature interrupts to pins |
| **`0x58`** | **`INT_MAP_DATA`** | Route drdy/FIFO interrupts to INT1/INT2 |
| **`0x59`** | **`INIT_CTRL`** | `0x00` = begin config load, `0x01` = commit. See §4 |
| `0x5B`/`0x5C` | `INIT_ADDR_0/1` | Config-file write pointer (chunked uploads) |
| **`0x5E`** | **`INIT_DATA`** | Config-file burst-write port |
| `0x68` | `AUX_IF_TRIM` | |
| `0x71`–`0x77` | `OFFSET_0`–`OFFSET_6` | Accel/gyro offset compensation; `OFFSET_6` holds `gyr_gain_en`, `gyr_off_en` |
| **`0x7C`** | **`PWR_CONF`** | `adv_power_save`, `fifo_self_wakeup`, `fup_en` |
| **`0x7D`** | **`PWR_CTRL`** | `acc_en`, `gyr_en`, `aux_en`, `temp_en` — **all disabled by default** |
| **`0x7E`** | **`CMD`** | `0xB6` soft reset; also FOC, NVM program, CRT commands |

> ⚠ **`PWR_CTRL` defaults to all sensors disabled [DOC §4.5].** A driver that uploads the config, sets ODR and range, and then reads `DATA_8` gets zeroes. Enabling the sensors is a separate, easily forgotten step.

Accel and gyro data are contiguous (`0x0C`–`0x17`), so a single 12-byte burst read gets both, and auto-increment works across the boundary.

---

## 6. Exact wiring on the Tanmatsu **[PCB]**

| Pin | Name | Net | Notes |
|---:|---|---|---|
| **1** | **SDO** | **`GND`** | ⇒ **I²C address 0x68** |
| 2 | ASDX | *unconnected* | Aux sensor data — no magnetometer fitted |
| 3 | ASCX | *unconnected* | Aux sensor clock |
| **4** | **INT1** | `Net-(U33-INT1)` | ⚠ see §6.1 |
| 5, 8, 12 | VDD / VDDIO | `+3.3V` | Both supplies from the 3.3 V rail |
| 6, 7 | GND | `GND` | |
| **9** | **INT2** | **`unconnected-(U33-INT2-Pad9)`** | ⚠ see §6.1 |
| 10 | OCSB | *unconnected* | OIS interface chip-select — OIS unused |
| 11 | OSDO | *unconnected* | OIS data out |
| **12** | **CSB** | **`+3.3V`** | ⇒ **I²C mode**, per datasheet recommendation |
| 13 | SCX (SCL) | `INT_SCL` | Internal I²C bus |
| 14 | SDX (SDA) | `INT_SDA` | Internal I²C bus |

Two design decisions here are textbook-correct and worth stating so nobody "improves" them:

- **CSB tied to VDDIO.** The datasheet: *"After reset / power-up, device's primary interface is in I2C mode. If CSB is connected to VDDIO during power-up and not changed, the primary interface works in I2C mode. For using I2C, it is recommended to hard-wire the CSB line to VDDIO"* **[DOC §6]**. A floating CSB is a real hazard — *"If CSB sees a rising edge after power-up, the device interface switches to SPI after 200 µs"*, so a glitch on a floating CSB silently kills the I²C interface until the next power cycle. This board does it right.
- **SDO tied to GND** selects address **0x68**, matching `BSP_BMI270_I2C_ADDRESS` and the bus map in the device's [`pinouts-and-buses.md`](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md) §1.1.

The device shares the internal I²C bus (ESP32-P4 GPIO9 SDA / GPIO10 SCL) with the CH32V203 coprocessor (0x5F) and the ES8156 codec (0x08). No address conflict.

### 6.1 ⚠ Neither interrupt pin reaches a processor

This is the most consequential integration fact about the BMI270 on this board, and it is not documented by the vendor.

- **INT2 (pin 9) is entirely unconnected** — `unconnected-(U33-INT2-Pad9)` **[PCB]**.
- **INT1 (pin 4)** is on net `Net-(U33-INT1)`, whose only other members are:

  | Ref | Value | Role |
  |---|---|---|
  | `R86` | **4.7 kΩ** to `+3.3V` | Pull-up |
  | `TP22` | test point, silkscreened **`BI270_INT`** | Bare pad |

  It connects to **no MCU pin** — not the ESP32-P4, not the ESP32-C6, not the CH32V203.

**Consequences:**

1. **All BMI270 use on the Tanmatsu must be polled.** There is no wake-on-motion, no interrupt-driven FIFO watermark, no low-power "sleep until the user picks it up". The feature engine's headline capability — waking a sleeping host — is unavailable.
2. The 4.7 kΩ pull-up implies the intended configuration was **open-drain, active-low** (`INT1_IO_CTRL.int1_od = 1`, `int1_lvl = 0`), since a push-pull output needs no pull-up. That configuration is never applied by the BSP.
3. `TP22` means the signal is *probeable* and could be bodged to a spare GPIO on a reworked board.

---

## 7. Driver audit — Badge.Team BSP vs. BST-BMI270-DS000-08

The BSP uses **Bosch's official `BMI270-Sensor-API`** (`bmi270_init()`, `bmi2_set_sensor_config()`, `bmi2_get_sensor_data()`), which is the right choice and means the §4 initialisation sequence, including the 8 KB upload and the `INTERNAL_STATUS` check, is handled correctly by vendor code. The defects are all in the board-specific layer, `badge_bsp_orientation.c` (212 lines, MIT).

### 7.1 🟠 Both interrupt mappings target pins that reach nothing

```c
// bsp_orientation_enable_gyroscope(), badge_bsp_orientation.c:71
rslt = bmi2_map_data_int(BMI2_DRDY_INT, BMI2_INT2, &bmi);
if (rslt != BMI2_OK) { ...; return ESP_FAIL; }

// bsp_orientation_enable_accelerometer(), badge_bsp_orientation.c:131
rslt = bmi2_map_data_int(BMI2_DRDY_INT, BMI2_INT1, &bmi);
if (rslt != BMI2_OK) { ...; return ESP_FAIL; }
```

Per §6.1 **[PCB]**, **INT2 is unconnected** and **INT1 terminates at a pull-up and a test point**. Both calls configure interrupt routing that cannot be observed. Worse, both are treated as fatal — a failure returns `ESP_FAIL` and aborts sensor enable — for a facility the board cannot use.

- **Status:** inert. The calls succeed (the chip accepts the mapping), so nothing breaks; but they are dead code that advertises a capability the hardware lacks.
- **Consequence:** a developer reading this BSP reasonably concludes interrupt-driven operation is available, wires up an ISR, and finds nothing ever fires. There is no comment anywhere noting the pins are unrouted.
- **Also note the inconsistency:** the gyro maps DRDY to INT2, the accel maps DRDY to INT1. Since `BMI2_DRDY_INT` is a single interrupt source, the second call **overrides the first** — enabling both sensors leaves DRDY mapped to INT1 only. Even on a board that routed both pins, this would not behave as the code implies.
- **Fix:** delete both calls and comment that INT1/INT2 are unrouted on this hardware, or route INT1 to a GPIO in the next revision.

### 7.2 🟠 Scale factors are hardcoded, decoupled from the configuration

`bsp_orientation_get()` at `badge_bsp_orientation.c:180, 194` converts raw LSBs using literals:

```c
float gyro_x  = lsb_to_dps (sensor_data.gyr.x, (float)2000, bmi.resolution);
float accel_x = lsb_to_mps2(sensor_data.acc.x, (float)2,    bmi.resolution);
```

These match the ranges set in the enable functions (`BMI2_GYR_RANGE_2000` at `:78`, `BMI2_ACC_RANGE_2G` at `:121`), so today the numbers are right. But the coupling is by convention only — nothing reads `ACC_RANGE`/`GYR_RANGE` back from the device **[DOC §5.2.42, §5.2.44]**. Any future change to the configured range, or any application that reconfigures the sensor directly through the Bosch API, produces silently wrong physical units — off by an exact power of two, which is the hardest kind of error to notice in orientation data.

- **Status:** latent; correct as shipped.
- **Fix:** cache the configured range at enable time, or read `0x41`/`0x43` in `bsp_orientation_get()`.

### 7.3 🟡 `±2 g` is a deliberate but undocumented trade

`config.cfg.acc.range = BMI2_ACC_RANGE_2G` at `:121`. For the stated purpose — auto-rotating the display between landscape and portrait — ±2 g is the right choice: it gives the best resolution for measuring the gravity vector. But it also means **any tap, knock or shake saturates the accelerometer**, so this configuration cannot support tap detection or gesture work without being changed. Not a defect; an undocumented constraint that the next developer will rediscover the hard way.

### 7.4 🟡 No gyro CRT, no self-test

Bosch provides **Component Retrim (CRT)** for the gyroscope, which reduces sensitivity error to typically **0.4 %** **[DOC §Key features]**, and `bmi2_perform_accel_self_test()`. The BSP invokes neither. CRT is a `CMD` register operation that takes a few hundred milliseconds and its result can be written to NVM, so it is normally done once in production rather than at every boot.

- **Status:** not a defect — an omission with a real accuracy cost if uncorrected gyro sensitivity matters.
- **Relevance here:** low. Display auto-rotation uses the accelerometer.

### 7.5 🟡 Inconsistent return value

`bsp_orientation_enable_gyroscope()` ends with `return rslt;` (`:93`), returning a Bosch `int8_t` error code through an `esp_err_t`. The accelerometer twin returns `ESP_OK` (`:144`). `BMI2_OK == ESP_OK == 0`, so success is indistinguishable; a non-zero BMI2 code returned as an `esp_err_t` would print as a nonsensical ESP-IDF error name.

### 7.6 ✅ Correct

- Uses the official Bosch API, so the config upload, the 450 µs inter-write delays and the `INTERNAL_STATUS` check are all handled properly.
- Correctly passes `0x68` and takes the shared-bus semaphore before touching I²C (`:38–39`), which matters given the coprocessor and codec share the bus.
- Gates conversion on `BMI2_DRDY_ACC` / `BMI2_DRDY_GYR` from `sensor_data.status` and reports readiness to the caller, rather than converting stale registers.
- `lsb_to_mps2` uses `GRAVITY_EARTH = 9.80665` — the standard value, correct.

### 7.7 Summary

| # | Severity | Location | Defect | Live? |
|---|---|---|---|---|
| 7.1 | 🟠 | `badge_bsp_orientation.c:71, :131` | DRDY mapped to unrouted INT2/INT1; second call overrides the first | Inert but misleading |
| 7.2 | 🟠 | `:180, :194` | Hardcoded scale factors decoupled from configured range | Latent |
| 7.3 | 🟡 | `:121` | ±2 g precludes tap/gesture use; undocumented | By design |
| 7.4 | 🟡 | — | No gyro CRT, no self-test | Omission |
| 7.5 | 🟡 | `:93` | BMI2 code returned as `esp_err_t` | Cosmetic |

---

## 8. Drivers and libraries

| Option | Language | Config upload? | Notes |
|---|---|:-:|---|
| **`BoschSensortec/BMI270-Sensor-API`** | C | ✅ | **The reference.** Contains the mandatory `bmi270_config_file[]`. BSD-3-Clause. What the Tanmatsu BSP uses. Verbose and struct-heavy, but correct |
| `boschsensortec/BMI270_SensorAPI` (Arduino wrapper) | C++ | ✅ | Thin wrapper over the above |
| **Zephyr** `drivers/sensor/bosch/bmi270` | C | ✅ | Mainline, `compatible = "bosch,bmi270"`. Clean, integrates with the Zephyr sensor API. Good choice on Zephyr |
| **Linux** `drivers/iio/imu/bmi270/` | C | ✅ | Mainline IIO driver; requests the firmware blob via the firmware loader (`bmi270-init-data.fw`) |
| `bmi270-rs` (Rust, `embedded-hal`) | Rust | ✅ | Community; check that the blob is present |
| **Lightweight / hand-rolled drivers** | any | ❌ **usually not** | ⚠ The common failure mode. Many "minimal BMI270" drivers on GitHub are BMI160 drivers with the address changed. They skip §4 entirely |

> **How to tell a real BMI270 driver from a broken one in ten seconds:** grep it for an 8 KB constant array, for `0x59` (`INIT_CTRL`), or for `0x5E` (`INIT_DATA`). If none are present, it does not initialise the part correctly, regardless of whether it appears to return sensible acceleration values.

### 8.1 ESP-IDF specifics

There is no first-party Espressif BMI270 component. The Tanmatsu BSP vendors the Bosch API plus a small `bmi270_interface.c` shim providing `bmi2_set_i2c_configuration(bus_handle, addr, semaphore)` and the read/write/delay callbacks the Bosch API needs. That shim pattern — three function pointers and a delay — is the standard way to port the Bosch API and is about 80 lines.

---

## 9. Pitfalls, in priority order

1. **Upload the config file, then check `INTERNAL_STATUS` (`0x21`) for `0b0001`.** Skipping either is the number-one cause of a BMI270 that "sort of works". §4.
2. **Respect the 450 µs inter-write delay** while `adv_power_save = 1`, or clear it first. Rapid back-to-back register writes during init are silently lost. §3.1.
3. **`PWR_CTRL` defaults to all sensors off.** Configuring ODR and range does not enable anything.
4. **Do not soft-reset after init** unless you re-upload the config.
5. **Suspend retains configuration.** Use suspend (3.5 µA) rather than reset for idle; you avoid the 8 KB re-upload.
6. **Tie CSB deliberately.** Floating CSB plus one glitch equals a chip that has silently switched to SPI. §6.
7. **The gyro costs 3× the accelerometer.** Enable it only when needed. §3.
8. **Accel and gyro data are contiguous at `0x0C`–`0x17`** — read them in one burst so the samples are coherent.
9. **On this board specifically: poll.** There is no usable interrupt. §6.1.
10. **Check `CHIP_ID == 0x24`, not just "an IMU answered at 0x68".** MPU-6050, ICM-42688, LSM6DS3 and BMI160 all also live at 0x68/0x69.

---

## 10. Alternatives

| Part | vs. BMI270 | When |
|---|---|---|
| **BMI160** | Predecessor. **No config upload**, simpler driver, worse noise, fewer features | When you want a 6-axis IMU you can drive from the datasheet alone |
| **BMI323** | Newer Bosch 6-axis, no config-file upload, similar power | Strong candidate for new designs specifically to avoid the blob |
| **ICM-42688-P** (TDK) | Better noise, no config upload, very well documented | Higher-performance motion work |
| **LSM6DSO / LSM6DSV** (ST) | Comparable, with an ST-flavoured feature engine and good Zephyr support | ST-ecosystem designs |
| **MPU-6050** | Ancient, cheap, everywhere, NRND | Only for compatibility with existing code |
| **BMA400** | Accelerometer only, ~14 µA | If you never needed the gyro — which, per §3, is often true |

If your application is "which way up is the device", **an accelerometer-only part is the honest choice** and saves both the 8 KB blob and two-thirds of the current. The BMI270 earns its place when you need the feature engine or the gyro.

---

## 11. Open questions

- Whether any Tanmatsu firmware enables the feature engine (step counting, wrist gestures) at all, or whether the config upload exists purely because `bmi270_init()` performs it. Nothing in the BSP touches `FEAT_PAGE`.
- Whether `TP22` was intended as a bodge point or is a leftover from a revision where INT1 *was* routed. The vendor has not commented.
- The exact `BMI270-Sensor-API` commit vendored into the BSP was not pinned in the snapshot inspected, so the config-file revision is unknown. Bosch has revised the blob at least once.
- No hardware measurement of actual current draw in the BSP's configuration.

---

## Manufacturer

**Bosch Sensortec GmbH** — see [`vendors/bosch-sensortec/README.md`](../../../vendors/bosch-sensortec/README.md). Relevant here: datasheets are served directly from `https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/<doc-id>.pdf` with no session or JavaScript, and the **driver repositories on GitHub are part of the primary documentation** — the datasheet explicitly defers to `BMI270-Sensor-API` for the configuration file.

## Used By

| Device | Ref | Role |
|---|---|---|
| [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) | `U33` | Device orientation, at I²C **0x68** on the internal bus (`BSP_BMI270_I2C_ADDRESS`). Used by `badge_bsp_orientation.c` to auto-rotate the 800×480 display between landscape and portrait. **Polled — neither interrupt pin is routed to a processor (§6.1).** See [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md), [`pinouts-and-buses.md`](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md) §1.1 |

## Related pages

- [`components/espressif/esp32-p4/README.md`](../../espressif/esp32-p4/README.md) — the I²C controller for this bus
- [`components/everest-semiconductor/es8156/README.md`](../../everest-semiconductor/es8156/README.md) — shares the internal I²C bus at 0x08
- [`components/wch/ch32v203c8t6/README.md`](../../wch/ch32v203c8t6/README.md) — shares the bus at 0x5F

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | BMI270 Datasheet | Bosch Sensortec | primary | datasheet | <https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf> | 2026-08-30 | **BST-BMI270-DS000-08**, 150 pp, 2 636 042 B | Register map, init sequence, power-mode table, ODR/range, CSB/SDO strapping, `adv_power_save` timing | `artifacts/bst-bmi270-ds000.pdf` |
| D2 | BMI270 product page | Bosch Sensortec | primary | official page | <https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi270/> | 2026-08-30 | — | Lifecycle, positioning | — |
| D3 | BMI270-Sensor-API | Bosch Sensortec | primary | repository | <https://github.com/BoschSensortec/BMI270-Sensor-API> | 2026-08-30 | BSD-3-Clause; commit not pinned | **The `bmi270_config_file[]` blob**, cited normatively by D1 footnote 3 | not vendored |
| S1 | `badge_bsp_orientation.c` (212 lines) | Nicolai Electronics / Badge.Team | primary | repository | in-tree snapshot | 2026-08-30 | MIT, SPDX 2025 | All §7 findings; ODR/range choices; polling model | `devices/nicolai-electronics/tanmatsu/artifacts/source-snapshots/badge-bsp/tanmatsu/badge_bsp_orientation.c` |
| S2 | `tanmatsu.kicad_pcb` | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | `tanmatsu-hardware` @ `640805dd`, CERN-OHL-P | Every net in §6, including the unrouted interrupts and `R86`/`TP22` | `devices/nicolai-electronics/tanmatsu/artifacts/schematics/kicad/` |

**Method note.** D1 was fetched with `curl` and a Chrome 131 User-Agent and validated as `%PDF` (150 pages). Bosch Sensortec serves datasheets to automated clients without difficulty; no User-Agent fallback was required. The §6 pin table was produced by parsing pad→net assignments out of `tanmatsu.kicad_pcb` directly rather than reading the schematic graphically, so it reflects the manufactured netlist.
