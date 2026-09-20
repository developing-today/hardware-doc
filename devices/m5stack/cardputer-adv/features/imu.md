# Cardputer ADV — IMU

> **Question:** *"How do I read motion on a Cardputer ADV?"*
> **ADV only.** v1.0 and v1.1 have no IMU at all. Verified **2026-09-04**.

## Hardware

**Bosch BMI270**, 6-axis (3-axis accelerometer + 3-axis gyroscope), designator **U7** on
schematic sheet 3, on the **internal** I²C bus.

| Property | Value | Evidence |
|---|---|---|
| Bus | internal I²C — SDA **G8**, SCL **G9** | docs PinMap; schematic U7 pins 14 (`SDX`) and 13 (`SCX`) |
| Address | **`0x69`** | the schematic prints **"7-bit Address 69H"** beside U7; R43 3.3 kΩ pulls `SDO` high |
| Interrupts | `INT1` (pin 4) and `INT2` (pin 9) present on the symbol; **neither traced to a GPIO** | schematic |
| Aux interface | `ASDX`/`ASCX`/`OSDO`/`OCSB` present (BMI270 auxiliary I²C for a magnetometer) — **no magnetometer fitted** | designator census of sheet 3 |
| Decoupling | C25 10 µF/10 V, C27 100 nF, FB7 120 Ω/MB ferrite on `VDD` | schematic |

Component record: [`bosch-sensortec/bmi270`](../../../../components/bosch-sensortec/bmi270/README.md).

M5Stack publishes an **IMU axis diagram** for the ADV at
`m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1178/IMU-Cardputer-Adv.jpg` — see
[`../media.md`](../media.md). Orientation conventions differ between boards; use it rather than
assuming.

## Minimal procedure

```cpp
#include <M5Cardputer.h>
void setup() {
  auto cfg = M5.config();
  cfg.internal_imu = true;
  M5Cardputer.begin(cfg, true);
}
void loop() {
  M5Cardputer.update();
  if (M5.Imu.update()) {
    auto d = M5.Imu.getImuData();
    M5Cardputer.Display.setCursor(0,0);
    M5Cardputer.Display.printf("%.2f %.2f %.2f\n", d.accel.x, d.accel.y, d.accel.z);
  }
  delay(20);
}
```

M5Unified's `IMU_Class` probes the internal bus and identifies the BMI270 itself; the ADV row
in `_pin_table_i2c_ex_in` (`In SCL = G9, In SDA = G8`) is what makes that possible. On a
v1.0/v1.1 the same row is `255, 255` — there is no internal bus to probe.

## Alternatives

| Approach | Notes |
|---|---|
| `M5Unified` `M5.Imu` | default; abstracts BMI270 vs other parts |
| `BoschSensortec/BMI270_SensorAPI` | full feature set — step counter, wrist gestures, any-motion, FIFO |
| `M5Cardputer-UserDemo` `app_imu` | M5Stack's own ESP-IDF demo app, on the `CardputerADV` branch |

The BMI270 needs a ~8 KB configuration blob uploaded at init; every driver does this, and it is
why first `begin()` is slow. Do not be surprised by a ~100 ms init.

## ⚠ No interrupt line

`INT1`/`INT2` are on the symbol but were not traced to any GPIO, and no vendor document or
driver references a BMI270 interrupt pin on this board. That means:

* **No motion-wake.** You cannot use the IMU to bring the ESP32-S3 out of deep sleep.
* Everything is polled, so sample rate is bounded by your loop and by bus contention with the
  keyboard scanner and the codec.

Stated as *not established* rather than *absent*: the sheet-3 pin table shows the names but the
band-based text extraction did not resolve their nets, and there is no page render at
sufficient resolution in this pass to be certain. Recorded in
[`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).

## Resources and conflicts

| Resource | Used |
|---|---|
| I²C `0x69` on the internal bus | shared with TCA8418 `0x34`, ES8311 `0x18` |
| GPIO | none exclusively |

High-rate IMU polling competes with keyboard event latency on the same bus. Nothing has been
measured; treat "1 kHz IMU + responsive keyboard" as unproven.

## Evidence status

Address `0x69`: **official** — printed on the schematic and consistent with `SDO` pulled high.
Bus assignment: **official** ×2 (docs PinMap + M5Unified table).
No-interrupt claim: **not established** (see above).
No IMU data was read from hardware by this session: **not tested**.
