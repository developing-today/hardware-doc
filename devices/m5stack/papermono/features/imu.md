# IMU — M5Stack PaperMono

> **How do I read motion, and how do I wake the board on it?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

**This guide is short.** Reading the IMU is ordinary; the one PaperMono-specific fact —
that its interrupt goes to the power manager rather than the ESP32-S3 — is the whole
point, and the vendor's own prose gets its polarity wrong.

## 1. Capability summary and the hardware path

A Bosch six-axis IMU on the shared system I²C bus, powered from the **L1** rail so it
stays alive in a state where the application processor does not.

```
BMI270 (I2C 0x68, alt 0x69)
   ├─ SDA/SCL ──▶ system I²C bus (GPIO47/48), clocked at 100 kHz for this device
   ├─ INT1 ─────▶ PYG4_IMU_INT ──▶ M5PM1 pin 12 (G4)     <- NOT the ESP32-S3
   └─ VDD   ◀─── 3V3_L1 (SSP7615-33DFR U6), enabled by M5PM1 LDO3V3_EN_PP
```

| Element | Part | Record |
|---|---|---|
| IMU | Bosch Sensortec **BMI270**, `0x68` (alt `0x69`) | [`components/bosch-sensortec/bmi270`](../../../../components/bosch-sensortec/bmi270/README.md) |
| Interrupt destination | **M5PM1 `G4`** | [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) · [`power-and-sleep.md`](power-and-sleep.md) |

## 2. ⚠ INT1 lands on the power manager, not the ESP32-S3

There is **no path from the BMI270 to any ESP32-S3 GPIO**. If you configure
`esp_sleep_enable_ext0_wakeup()` on a pin expecting a motion interrupt, nothing will ever
arrive.

That is not an oversight — it is the design. It is what allows the board to be woken by a
motion event **while the ESP32-S3 has no power at all** (state L1). The shipped factory
binary carries the confirming log line:

```
PM1 shutdown, wake by BMI270 INT1 -> PM1 G4 falling edge
```

## 3. ⚠ The interrupt is active-**low**; vendor prose says otherwise and is wrong

| Source | Says |
|---|---|
| Vendor prose, power-management page §1 | *"Rotating the device then triggers the **active-high** IMU interrupt to wake the M5PM1"* |
| Vendor **code** on the same page | `intPinConfig.pin_cfg[0].lvl = BMI2_INT_ACTIVE_LOW;` and `pm1.gpioSetWakeEdge(M5PM1_GPIO_NUM_4, M5PM1_GPIO_WAKE_FALLING)` |
| Vendor code comment, second sketch | `// active - low` |
| Vendor narrative, end of §4 | *"maps the interrupt to **active-low** INT1"* |
| **Shipped binary** | `PM1 shutdown, wake by BMI270 INT1 -> PM1 G4 falling edge` |

**Four sources say active-low; one prose sentence says active-high.** The prose is the sole
outlier and it is wrong. Resolved in
[`../gaps-and-conflicts.md` R3](../gaps-and-conflicts.md#r3--bmi270-interrupt-polarity--resolved-against-the-vendor-prose).

Use **`BMI2_INT_ACTIVE_LOW`** and **`M5PM1_GPIO_WAKE_FALLING`**.

## 4. Prerequisites

| Item | Value |
|---|---|
| Reading motion | **M5Unified `M5.Imu`** — `imu.begin(&M5.In_I2C, M5.getBoard())`, `imu.update()`, `imu.getType()` (`hal_imu.cpp:23–40`) |
| Configuring wake | **SparkFun BMI270 Arduino Library** — `https://github.com/sparkfun/SparkFun_BMI270_Arduino_Library`, which is what the vendor's published wake sketch uses. **Not an M5Stack library** |
| Also pinned by the firmware | `Arduino_BMI270_BMM150` **1.2.3**, commit `a599119044554015e06735f9d7187fc56295b9b6`, patched — a *third* BMI270 driver in the same ecosystem |
| M5PM1 | 1.0.7 |

> Three different BMI270 drivers appear across M5Stack's own material: M5Unified's
> internal one, SparkFun's (in the published wake example), and `Arduino_BMI270_BMM150`
> (pinned in the factory firmware). They are not interchangeable. Pick one per project.

## 5. Resources consumed

| Resource | Value |
|---|---|
| I²C address | **`0x68`**, probed also at **`0x69`** (`app_sleep_wake.cpp:59–60`) |
| I²C speed | **100 kHz** for this device (`BMI270_I2C_FREQ_HZ = 100000`) — notably slower than the RTC and NFC at 400 kHz |
| M5PM1 pin | `G4`, input, pull-up, wake-enabled, falling edge |
| ESP32-S3 GPIO | **none** |
| Rail | `3V3_L1` — alive in state **L1** and above |

## 6. Minimal procedures

### 6.1 Reading motion (`inferred`)

```cpp
#include <M5Unified.h>

void setup() {
  M5.begin(M5.config());
  // M5Unified brings the IMU up itself; hal_imu.cpp retries begin() and update()
}

void loop() {
  M5.update();
  if (M5.Imu.update()) {
    auto d = M5.Imu.getImuData();
    // d.accel.x/y/z, d.gyro.x/y/z
  }
}
```

### 6.2 Wake on motion with the ESP32-S3 unpowered (`reported-working` as a vendor fragment)

The load-bearing lines, from M5Stack's own power-management page. Full sequence and the
`ldoSetPowerHold` rationale are in
[`power-and-sleep.md` §6.2](power-and-sleep.md#62-shut-down-and-wake-on-motion-keeping-l1-alive).

```cpp
Wire1.setPins(M5.getPin(m5::pin_name_t::in_i2c_sda), M5.getPin(m5::pin_name_t::in_i2c_scl));
pm1.begin(&M5.In_I2C, M5PM1_DEFAULT_ADDR, M5PM1_I2C_FREQ_100K);
pm1.gpioSetWakeEnable(M5PM1_GPIO_NUM_4, true);
pm1.gpioSetWakeEdge  (M5PM1_GPIO_NUM_4, M5PM1_GPIO_WAKE_FALLING);   // active-low
pm1.setSingleResetDisable(false);

while (imu.beginI2C(BMI2_I2C_PRIM_ADDR, Wire1) != BMI2_OK) { /* retry */ }
imu.disableFeature(BMI2_ANY_MOTION);
/* ... tune any-motion ... */
bmi2_int_pin_config intPinConfig;
intPinConfig.pin_type              = BMI2_INT1;
intPinConfig.int_latch             = BMI2_INT_NON_LATCH;
intPinConfig.pin_cfg[0].lvl        = BMI2_INT_ACTIVE_LOW;      // <- not active-high
intPinConfig.pin_cfg[0].od         = BMI2_INT_PUSH_PULL;
intPinConfig.pin_cfg[0].output_en  = BMI2_INT_OUTPUT_ENABLE;
intPinConfig.pin_cfg[0].input_en   = BMI2_INT_INPUT_DISABLE;
imu.setInterruptPinConfig(intPinConfig);
imu.mapInterruptToPin(BMI2_ANY_MOTION_INT, BMI2_INT1);

pm1.setLdoEnable(true);      // keep L1 alive across shutdown
pm1.ldoSetPowerHold(true);
pm1.setLedEnLevel(true);
pm1.shutdown();
```

Any-motion tuning constants, quoted from the vendor's own commented-out code:
`any_motion.threshold` 1 LSB = **0.48 mg** (default 83 mg); `any_motion.duration`
1 LSB = **20 ms** (default 100 ms).

### 6.3 Chained wake — M5PM1 stays awake and routes the IRQ to the host

If you want the M5PM1 alive and the ESP32-S3 woken by it rather than shut down:

```cpp
pm1.irqClearGpioAll(); pm1.irqClearSysAll(); pm1.irqClearBtnAll();
pm1.irqSetGpioMaskAll(M5PM1_IRQ_MASK_ENABLE);
pm1.irqSetGpioMask(M5PM1_IRQ_GPIO4, M5PM1_IRQ_MASK_DISABLE);   // unmask GPIO4
pm1.gpioSetMode(M5PM1_GPIO_NUM_4, M5PM1_GPIO_MODE_INPUT);
pm1.gpioSetPull(M5PM1_GPIO_NUM_4, M5PM1_GPIO_PULL_UP);

pm1.gpioSetMode (M5PM1_GPIO_NUM_1, M5PM1_GPIO_MODE_OUTPUT);
pm1.gpioSetDrive(M5PM1_GPIO_NUM_1, M5PM1_GPIO_DRIVE_PUSHPULL);
pm1.gpioSetFunc (M5PM1_GPIO_NUM_1, M5PM1_GPIO_FUNC_IRQ);       // -> ESP32-S3 GPIO1

pinMode(GPIO_NUM_1, INPUT_PULLUP);
attachInterrupt(GPIO_NUM_1, pm1_irq_handler, FALLING);
// or: esp_sleep_enable_ext0_wakeup(GPIO_NUM_1, 0); rtc_gpio_pullup_en(GPIO_NUM_1);
```

Note that `M5.Power.deepSleep(us, touch_wakeup=true)` **replaces** GPIO1 with GPIO4 as the
EXT0 pin — so this pattern and touch wake are mutually exclusive on one call. See
[`touch.md` §6](touch.md#6-wake-on-touch).

## 7. Limits

| Class | Limit |
|---|---|
| **Silicon (BMI270)** | 6-axis accel + gyro. No magnetometer on this board — the `BMM150` half of the pinned `Arduino_BMI270_BMM150` library has nothing to talk to |
| **Board** | INT1 goes only to the M5PM1 (§2) |
| **Board** | Runs at **100 kHz** on a bus whose other devices run at 400 kHz |
| **Documentation** | The vendor prose has the interrupt polarity backwards (§3) |
| **Documentation** | The M5Stack-mirrored BMI270 datasheet is **five years behind Bosch's** current revision — use Bosch's |
| **Observed** | Nothing. No orientation-detection, drift or calibration report exists for this board |

## 8. Conflicts

| Combination | Verdict | Mechanism |
|---|---|---|
| IMU + [RTC](rtc.md) wake | ✅ | Different M5PM1 GPIOs — `G4` and `G0`. Both can be enabled |
| IMU + [touch](touch.md) wake | ⚠ different levels | IMU wakes from L1; touch only from L2 |
| IMU + other I²C devices | ✅ addresses distinct | But the 100 kHz requirement means IMU transactions are slower |
| IMU + [sleep](power-and-sleep.md) | ✅ the intended pattern | Needs `setLdoEnable(true)` + `ldoSetPowerHold(true)` |
| IMU + `M5.Power.deepSleep(touch_wakeup=true)` | ❌ chained path lost | §6.3 |
| IMU + charger on the bus | ⚠ | The general I²C hazard applies |

## 9. Debugging

| Symptom | Cause |
|---|---|
| Wake-on-motion never fires | Wrong polarity — you used the prose's active-**high** (§3); or you configured wake on an ESP32-S3 pin (§2) |
| IMU disappears after shutdown | L1 not held: `ldoSetPowerHold(true)` |
| Not found at `0x68` | Try `0x69`; the firmware probes both |
| Erratic reads | Bus speed — this device wants 100 kHz |
| Wake fires constantly | `any_motion.threshold` too low; 1 LSB = 0.48 mg |
| Two BMI270 libraries fight | Pick one (§4) |

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; the BMI270 is fitted on both C153 and C153-LITE |
| Framework range | M5Unified 0.2.21 · M5PM1 1.0.7 · SparkFun BMI270 library (unpinned by the vendor) · `Arduino_BMI270_BMM150` 1.2.3 in the factory build |
| Evidence | Wiring: **schematic**. Polarity: **code + shipped binary**, three-way corroborated. Wake sketch: **`reported-working`** (vendor-published), `not-tested` here |
| Confidence | High on the interrupt path and polarity; **none on sensor behaviour** |
| Last verified | **2026-09-01** |

## Related

- [`power-and-sleep.md`](power-and-sleep.md) · [`rtc.md`](rtc.md) · [`touch.md`](touch.md) · [`../power-architecture.md`](../power-architecture.md)
- [`components/bosch-sensortec/bmi270`](../../../../components/bosch-sensortec/bmi270/README.md) · [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md)
