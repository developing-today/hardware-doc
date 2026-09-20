# Battery and charging — M5Stack PaperMono

> **How do I read the battery, control charging, and why is the charger missing from my
> I²C scan?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

## 1. Capability summary and the hardware path

A 1150 mAh Li-ion cell with an NTC thermistor, charged from USB-C through an
over-voltage protector and an I²C-capable charger, with battery voltage read by the
power-management chip's own ADC.

```
USB-C ──▶ AW32901FCR (U2, OVP 5.95 V) ──▶ IP2315 charger (U1) ──▶ battery (J2, 1150 mAh + 100K NTC)
                                              ↕ I²C 0x75
                                      U3 level translator (VBAT-referenced)
                                              ↕ OE = PYB_CHG_IIC
                                          M5IOE1 IO11   ◀── the gate
```

| Element | Part | Record |
|---|---|---|
| Charger | Injoinic **IP2315**, I²C `0x75` | [`components/injoinic/ip2315`](../../../../components/injoinic/ip2315/README.md) |
| USB input protection | Awinic **AW32901FCR**, `OVP = 5.95 V` | [`components/awinic/aw32901`](../../../../components/awinic/aw32901/README.md) |
| Bus gate | M5IOE1 `IO11` | [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md) · [`io-expander.md`](io-expander.md) |
| Battery telemetry | M5PM1 `BAT_ADC_EN` / `BAT_ADC_IN`, registers `0x22`/`0x23` | [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) |
| Cell | 1150 mAh Li-ion at `J2`, `100K-RNTC` thermistor | — |

> **Naming trap.** `VBUS_L0` is **not** USB VBUS. USB 5 V is `VUSB_IN`; `VBUS_L0` is the
> internal battery/system bus, tied to `VBAT_L0` through a 0 Ω link (`R20`). Reading
> `VBUS` as "USB power" inverts the entire tree.

## 2. ⚠ The charger is normally *off* the I²C bus — and a scan not finding `0x75` is correct

**This is the board's sharpest design quirk, and M5Stack documents it themselves.**

The IP2315's I²C pins are also its LED driver pins, and I²C mode requires them to be
pulled to **`VBAT`**, not to the 3.3 V logic rail. The schematic solves this with `U3`, a
dual-bit bidirectional level translator bridging the system bus (`G47_SYS_SDA` /
`G48_SYS_SCL`) to a `VBAT`-referenced charger bus (`CHG_SYS_SDA` / `CHG_SYS_SCL`). **Its
output enable is `PYB_CHG_IIC`, driven by M5IOE1 `IO11`.**

M5Stack's own warning, verbatim from the product page:

> "The I2C operating mode of the charging chip IP2315 depends on the I2C pins being
> pulled up to VBAT voltage. Connecting the device to USB triggers mode detection; **if
> the VBAT voltage is too low, the IP2315 may not initialize into I2C mode properly,
> which can interfere with other devices on the same I2C bus.** M5IOE1 controls the
> connection between the IP2315 and the system I2C bus via `PYG11_PWM3`: during device
> operation, **do not keep the IP2315 mounted on the I2C bus for extended periods;
> disconnect it promptly after communication** to avoid reducing bus communication
> stability. **If an I2C bus communication anomaly occurs, you can reset the device by
> briefly pressing the power button** to restore normal bus operation."

So:

- **`0x75` will not appear in an ordinary I²C scan.** That is the intended state, not a
  fault. Do not "fix" it.
- The IP2315 datasheet additionally documents a bus-lockup mechanism involving a **missing
  NACK on the final byte of a read** — presumably the specific failure the gate exists to
  avoid.
- **Recovery from a wedged bus is a short press of the power button**, which resets the
  device via the M5PM1.

> The dedicated Arduino power-management page **never mentions `M5IOE1_PIN_11` at all**.
> Neither of its two pin tables lists it. A reader working only from that page would not
> know the gate exists. The hazard note lives only on the product page.

### How M5Unified handles it

`M5Unified/src/utility/Power_Class.cpp:66–96` — the mitigation is structural, not
advisory:

```cpp
static void set_papermono_ip2315_enabled(bool enable) {
  M5.getIOExpander(0).digitalWrite(M5IOE1_Class::gpio11, enable);
}

static bool wait_papermono_ip2315_ready(void) {
  m5gfx::delay(2);
  for (int i = 0; i < 64; ++i) {              // 64 attempts
    if (M5.In_I2C.scanID(ip2315_i2c_addr, i2c_freq)) { return true; }
  }
  return false;
}
```

Every charger access is bracketed: gate on → wait for the device to appear → transact →
gate off. **Callers that talk to the charger without going through this will simply not
find it.**

## 3. Reading the battery and charge state

### Voltage

The battery voltage does **not** come from the charger. It comes from the M5PM1's ADC:

```cpp
int16_t mv = M5.Power.getBatteryVoltage();     // what the factory firmware uses
                                               // hal.cpp:114 -> M5.Power.getBatteryVoltage()
```

or directly, `pm1.readVbat(uint16_t* mv)` — registers `VBAT_L`/`VBAT_H` (`0x22`/`0x23`),
in millivolts, the high byte carrying 4 bits. Companion readings: `readVin()`
(`0x24`/`0x25`), `read5VInOut()` (`0x26`/`0x27`), `readVref()` (`0x20`/`0x21`).

**There is no fuel gauge and no coulomb counter.** The factory firmware derives a
percentage from a filtered voltage in `app_battery.cpp:155` (`getBatteryPercent`) — a
lookup on voltage, with all the accuracy that implies under load.

### Charge state

`M5.Power.isCharging()` on this board does something specific and worth reproducing
(`Power_Class.cpp:2714–2740`):

1. Read the M5PM1 power source. **If neither `vin` nor `vinout` is present, return
   discharging** without touching the charger at all. (`PWR_SRC` is a bitmap; the battery
   bit can coexist with VIN.)
2. Otherwise gate the IP2315 on, wait for it, read register **`0xC7`**, test **bit 7**,
   gate it off.

M5Stack's own in-code comment records measured values:

```
// its state in REG_CHG_STAT(0xC7): bit7 = charging in progress (measured:
// 0x82 charging / 0x45 charge-complete / 0x00 charge-disabled).
```

That is the closest thing to a hardware-measured fact in the whole software stack — but
it is **M5Stack's** measurement, `reported-working`, not ours.

### Enabling and disabling charging

`M5.Power.setBatteryCharge(bool)` → IP2315 register **`0x01` bit 0**, again with the
gate bracketed (`Power_Class.cpp:2398–2410`).

> Two comments in `Power_Class.cpp` say **"IP2316"** while the address constant is named
> `ip2315_i2c_addr` and the schematic part is an **IP2315**. A typo in M5Unified, not a
> second part. Noted so nobody goes looking for an IP2316 datasheet.

## 4. Charging parameters — mostly unresolved

| Parameter | Value | Status |
|---|---|---|
| Cell capacity | **1150 mAh** | vendor spec |
| Charge current | Sheet 1 annotates `充电电流 0.5C` → **~575 mA** | **`inferred`** from the annotation and capacity |
| `ICHGSET` programming resistor | **Not resolved from the schematic** | Open gap |
| Input | USB Type-C, **DC 5 V** | vendor spec |
| OVP | **5.95 V** | schematic annotation on `U2` |
| NTC | `100K-RNTC` at `J2` | schematic |
| Charge-complete detection | IP2315 `0xC7` bit 7 | M5Unified source + M5Stack's measured note |

So the 0.5 C figure rests on a single schematic annotation, with the resistor that would
confirm it unread. Treat it as approximate.

## 5. ⚠ There is no USB-PD

The USB-C connector carries the standard **5.1 kΩ CC pulldowns** (`R14` on CC2) that
advertise a plain sink, but the **IP2315's own `CC1`/`CC2` sense pins are unpopulated**
(`R1`, `R2` marked `NC`). Combined with the 5.95 V OVP upstream, this is a **5 V-only
input**; the charger's PD capability is deliberately depopulated.

*(Two earlier readings of this circuit disagreed — one saw only the `NC` resistors and
concluded there were no CC resistors at all. Both resistor groups exist; they are on
different parts. Recorded so the question is not re-opened.)*

Practical consequence: **any USB-C source will supply 5 V and nothing more.** A PD-only
charger that refuses to provide 5 V without negotiation will not charge this board.

## 6. Resources consumed

| Resource | Value |
|---|---|
| I²C address | `0x75`, **gated**, on the shared bus |
| Expander pin | `IO11` — the gate. `PWM3`-capable, used here as a digital output |
| M5PM1 pins | `BAT_ADC_EN_OD`, `BAT_ADC_IN`, `5VIN_ADC_IN`, `5VOUT_ADC_IN`, `CHG_EN_PP` |
| M5PM1 registers | `0x22`/`0x23` VBAT, `0x24`/`0x25` VIN, `0x26`/`0x27` 5VINOUT, `0x04` `PWR_SRC`, `0x08` `BATT_LVP` |
| IP2315 registers used by M5Unified | `0x01` bit 0 (charge enable), `0xC7` bit 7 (charge status) |
| ESP32-S3 GPIO | **none** |

## 7. Minimal procedure (`inferred`)

```cpp
#include <M5Unified.h>

void setup() { M5.begin(M5.config()); }

void loop() {
  M5.update();
  int16_t mv = M5.Power.getBatteryVoltage();          // millivolts, from the M5PM1 ADC
  auto chg   = M5.Power.isCharging();                 // gates the IP2315 on and off for you
  // ... render sparingly; see epaper-display.md on refresh discipline
  delay(5000);
}
```

If you must talk to the IP2315 yourself, **bracket every access**:

```cpp
auto& ioe1 = M5.getIOExpander(0);
ioe1.digitalWrite(M5IOE1_Class::gpio11, true);        // gate ON
/* ... wait for 0x75 to appear, then transact, briefly ... */
ioe1.digitalWrite(M5IOE1_Class::gpio11, false);       // gate OFF - do not skip this
```

`M5IOE1_Class::gpio11` is M5Unified's own expander enum, which is **not** the M5IOE1
library's `M5IOE1_PIN_*` enum. See [`io-expander.md`](io-expander.md) before mixing them.

## 8. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Silicon (IP2315)** | I²C pins double as LED driver pins and must be `VBAT`-referenced; a missing NACK on a final read byte can wedge the bus |
| **Board** | The charger is **gated off the bus** and only reachable through M5IOE1 `IO11` |
| **Board** | **No USB-PD** — CC sense pins depopulated (§5); 5.95 V OVP |
| **Board** | No fuel gauge. Voltage-only state of charge |
| **Framework (M5Unified)** | 64-attempt scan loop before giving up on the charger; `isCharging()` short-circuits when there is no external supply |
| **Observed (M5Stack)** | `0xC7` = `0x82` charging / `0x45` complete / `0x00` disabled |
| **Unknown** | Charge current (0.5 C `inferred`), `ICHGSET` resistor, actual runtime on any workload |

## 9. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| Charger + six other I²C devices | ⚠ **the documented hazard on this board** | Leave the gate open and bus stability degrades. Open it, transact, close it |
| Charger access + [NFC](nfc.md) polling | ⚠ | Both are on the one bus, and NFC polling is chatty. Do not gate the charger on inside an NFC scan window |
| Charger + [sleep](power-and-sleep.md) | ✅ | Charging proceeds independently of the M5PM1 power state |
| Charging + [display](epaper-display.md) + [Wi-Fi](wifi-and-bluetooth.md) | ⚠ unmeasured | No current budget exists for any combination |
| Charger + very low battery | ⚠ **the specific documented failure** | The IP2315 may fail to enter I²C mode and disturb the other six devices |
| Charger + USB-PD-only supply | ❌ | §5 |

## 10. Debugging

| Symptom | Cause |
|---|---|
| `0x75` absent from an I²C scan | **Correct behaviour** (§2). Assert `IO11` first |
| Other I²C devices become unreliable | The gate was left open. Close it |
| Bus wedged entirely | **Short press of the power button** — M5Stack's documented recovery |
| `isCharging()` always false with USB plugged in | The M5PM1 `PWR_SRC` short-circuit fires first; check `getPowerSource()` |
| Board will not charge from a particular charger | PD-only source; there is no PD here (§5) |
| Battery percentage jumps under load | Voltage-only estimation with no coulomb counting |

## 11. Unresolved questions

- **`ICHGSET` resistor value**, and therefore the real charge current.
- **No runtime figure exists** for any workload, in any state.
- Whether the NTC is actually used for charge-current derating, or only monitored.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; battery and charger identical on C153 and C153-LITE (**both are 1150 mAh** — the Lite does not get a smaller cell) |
| Framework range | M5Unified 0.2.21 · M5PM1 1.0.7 · M5IOE1 1.0.9 |
| Evidence | Gating hazard: **vendor-documented**, `reported-working`. M5Unified behaviour and register numbers: **read from source**. Charge current: **`inferred`**. Sketch: **`inferred`** |
| Confidence | High on the bus-gate mechanism; **low on every electrical figure** |
| Last verified | **2026-09-01** |

## Related

- [`../power-architecture.md#charging-and-usb-input`](../power-architecture.md#charging-and-usb-input)
- [`power-and-sleep.md`](power-and-sleep.md) · [`io-expander.md`](io-expander.md) · [`usb-and-serial.md`](usb-and-serial.md)
- [`components/injoinic/ip2315`](../../../../components/injoinic/ip2315/README.md) · [`components/awinic/aw32901`](../../../../components/awinic/aw32901/README.md) · [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md)
