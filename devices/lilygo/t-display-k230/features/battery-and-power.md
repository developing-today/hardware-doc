# Battery and power

**Question:** *How do I read battery state, configure charging, and stop it shutting down at the
wrong voltage?*

| | |
|---|---|
| Charger | [TI BQ25896](../../../../components/texas-instruments/bq25896/README.md), I²C4, **`0x6B`** |
| Fuel gauge | [TI BQ27220](../../../../components/texas-instruments/bq27220/README.md), I²C4, **`0x55`** |
| Cell | **21700** in the keyboard-base compartment |
| 5 V boost | enabled by the **nRF52840's `P0.04`** |
| Power key | K230 **PMU INT0**, `GPIO64`, driver `k230-pmu-pwrkey` |
| USB in | 5 V, 500 mA |
| PMIC | **unidentified** ([U1](../../../../components/unidentified/t-display-k230/README.md)) |
| Evidence | `reported-working` |

## The chain

```
USB-C 5V/500mA ──► BQ25896 charger (0x6B) ──► 21700 cell ──► BQ27220 gauge (0x55)
                                                 │
                                                 └─► 5V boost  ◄── enabled by nRF52840 P0.04
                                                          │
                                                          └─► main unit
```

**Note what that means:** on a kit configuration the **companion MCU on an expansion board
controls the rail that powers the main unit from the battery.** If the nRF52840 is wedged or
mid-DFU, that is a power dependency, not just a comms one.

## Reading state

Both chips are on the shared I²C4 bus and are treated as **optional, runtime-detected** hardware
— a bare `K256` board has neither. The launcher's `ui_power_manager.c` and `ui_hardware.c`
poll the gauge for voltage (mV), current (mA) and state of charge (%), and the charger for
USB-present and charging status.

## Low-battery shutdown is a userspace policy

Not a hardware cut-off. In `ui_hardware.c`:

- a millivolt threshold, compared against the gauge reading
- `BATTERY_LOW_SHUTDOWN_CONFIRM_COUNT` consecutive low readings before acting
- gated on charger USB-present, and it logs a "low-shutdown recovered" line when the condition
  clears

BSP **v0.2.3** "set the default low-battery shutdown threshold"; **v0.2.2** "improved first-run
charger, battery, and low-voltage shutdown defaults". Both are evidence this was tuned after
release — if you are on an older image, the defaults may be wrong.

**Anything that blocks I²C4 blinds this policy.** See
[`resources-and-conflicts.md`](../resources-and-conflicts.md).

## The power key

Not a normal GPIO. `GPIO64` is PMU input channel 0, **idle low, pressed high** — the opposite
polarity to the BOOT0 button on `GPIO0`. It reaches userspace through
`0064-input-k230-pmu-pwrkey.patch` (21 523 bytes), whose register flow "mirrors the RT-Thread PMU
pwrkey driver": route PMU `KEY_EDGE` to **CPU IRQ 175**, rising-edge detect, and on shutdown
program INT0 long-press wakeup and ask the PMU to cut power.

Launcher constants: long-press **96 000** ticks, debounce **256** ticks.

Full register list: [`pinouts-and-buses.md` §9](../pinouts-and-buses.md#9-pmu-power-key-register-flow).
Canaan's `K230_PMU_User_Guide.md` is retained under the
[K230 component](../../../../components/canaan/k230/artifacts/K230_PMU_User_Guide.md).

## Thermal

`CONFIG_CANAAN_THERMAL=y` plus `0063-thermal-canaan-convert-k230-tsensor-raw.patch` give an
on-die temperature sensor. The launcher exposes it. `K230_FAN_ENABLED 0` and a "fan" mention in
`0058-riscv-dts-rm69a10-add-audio-fan-sensor-pins.patch` suggest a fan header on some variant —
**unverified**.

## Limits and unknowns

| Item | Status |
|---|---|
| Cell capacity, chemistry, protection IC | **unknown** ([U6](../../../../components/unidentified/t-display-k230/README.md)) |
| PMIC | **unknown** |
| Battery life under any workload | **never measured or published** |
| Idle / suspend current | **unknown** |
| Deep-sleep support on this board | K230 silicon claims ≤ 20 µW standby; **nothing on this board demonstrates it** |
| Charge current setting | BQ25896 is capable of 3 A; input is 500 mA |

Community scepticism is on record and unanswered: *"the battery life on this would be less than
it would be with just a phone and a regular nRF node on a 1000mAh battery"* (2025-07-07,
opinion). Nobody has published a measurement either way. This is the **largest single evidence
gap** about the product.
