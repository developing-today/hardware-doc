# Power and sleep — M5Stack PaperMono

> **How do I put this thing to sleep, and how do I get it to wake up again?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

This is the board's defining feature. Most ESP32 boards have a regulator and a sleep
mode; the PaperMono has a **five-state power state machine implemented in a second
microcontroller** that owns the ESP32-S3's reset and boot straps. In power terms the
application processor is a peripheral of the power manager, not the other way round.

## 1. Capability summary and the hardware path

| Element | Part | Record |
|---|---|---|
| Power manager | **M5PM1**, I²C `0x6E` — a Puya `PY32L020F15U6` running M5Stack firmware | [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) |
| Underlying silicon | `PY32L020F15U6` Cortex-M0+ | [`components/puya/py32l020f15u6`](../../../../components/puya/py32l020f15u6/README.md) |
| Rail switching for L3B | **M5IOE1**, I²C `0x4F` | [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md) · [`io-expander.md`](io-expander.md) |
| Wake: alarm | RX8130CE RTC → M5PM1 `G0` | [`rtc.md`](rtc.md) |
| Wake: motion | BMI270 IMU → M5PM1 `G4` | [`imu.md`](imu.md) |
| Wake: touch | FT6336G → ESP32-S3 GPIO4 | [`touch.md`](touch.md) |
| Wake: button | `PWR_BTN` → M5PM1 `BTN_PU` | [`buttons-and-rgb-led.md`](buttons-and-rgb-led.md) |

## 2. The five power states

Schematic sheet 1 tabulates them as columns. Names are M5Stack's.

| State | Name | What is powered | Wakes on |
|---|---|---|---|
| **L0** | Shipping | Charger, protection, `3V3_L0`. M5PM1 alive | Power button, USB insertion |
| **L1** | Standby | + `3V3_L1` — **RTC and IMU** | Power button, **RTC alarm**, **IMU motion** |
| **L2** | DeepSleep | + `3V3_L2` — ESP32-S3, touch, NFC, keys, expander | + touch, keys, NFC, LoRa |
| **L3A** | Core active | + e-paper rail `EPD_3V3_L3B` | — |
| **L3B** | All active | + frontlight, microSD, microphone | — |

Transitions, as M5Stack states them:

- **Into L0** — the ESP32-S3 issues an I²C shutdown command to the M5PM1.
- **L0 → L1** is automatic.
- **L1 → L2** is enabled by the M5PM1 on a single power-button click, an IMU interrupt,
  or an RTC interrupt.
- **L3** switches are asserted by the ESP32-S3 through the M5IOE1.

> **The tree is parallel, not cascaded.** M5Stack: *"The PaperMono multi-level power
> switching design is **not a series structure**. The power inputs for the L1 ~ L3B
> switches all originate from the L0 (`SYS_VBUS`) source rather than from the preceding
> power level, allowing each level to be controlled independently."*
>
> And: *"After the M5PM1 powers on, L1, L2, and L3A are enabled automatically. During
> M5Unified initialization, the M5IOE1 is then controlled to enable L3B."*
>
> L2 versus L3A is a **state** distinction, not a separate rail: *"When the ESP32-S3 is
> sleeping, the power system is at level L2. When the ESP32-S3 is operating, it is at
> level L3A."* Whether L3A and L3B are genuinely separate switch groups is
> [not fully resolved](../power-architecture.md#what-is-not-established) — the rails they
> name overlap.

## 3. ⚠ RTC and IMU interrupts terminate on the M5PM1, not the ESP32-S3

**This is the structural fact that makes the whole architecture work, and it is easy to
miss.**

| Source | Lands on | Consequence |
|---|---|---|
| RX8130CE `nIRQ` | net `PYG0_RTC_INT` → **M5PM1 pin 3 (`G0`)** | An alarm can wake the board with the ESP32-S3 **unpowered** |
| BMI270 `INT1` | net `PYG4_IMU_INT` → **M5PM1 pin 12 (`G4`)** | Motion can wake the board with the ESP32-S3 **unpowered** |
| FT6336G `INT` | ESP32-S3 **GPIO4** | Touch wake requires the ESP32-S3 to be at least in its own light/deep sleep — i.e. state L2 |
| M5PM1 IRQ out | `G1` → ESP32-S3 **GPIO1** | The M5PM1 routes its own interrupts to the host when the host is awake |

There is **no path from the RTC or the IMU to an ESP32-S3 GPIO**. If you write
`esp_sleep_enable_ext0_wakeup()` on a pin expecting an RTC alarm, nothing will ever
arrive. You must configure the wake on the **M5PM1** instead.

The shipped factory binary confirms both intent and polarity:

```
PM1 shutdown, wake by BMI270 INT1 -> PM1 G4 falling edge
PM1 shutdown, wake by RX8130 timer  -> PM1 G0 falling edge
```

## 4. Prerequisites

| Item | Value |
|---|---|
| M5PM1 library | **1.0.7** (registry `m5stack/m5pm1`) |
| M5IOE1 library | **1.0.9** |
| M5Unified | 0.2.21 — `_pmic = pmic_t::pmic_m5pm1`, `_rtcIntPin = GPIO_NUM_1`, `_wakeupPin = GPIO_NUM_1` for this board |
| I²C speed | M5PM1 and M5IOE1 are brought up at **100 kHz** by both M5Unified and the factory firmware |

## 5. The API surface

Transcribed from `M5PM1/src/M5PM1.h` and M5Stack's published power-management page.
`executed-success` for the extraction; **`inferred`** for any sketch built from them.

```
pm1.begin(&M5.In_I2C, M5PM1_DEFAULT_ADDR, M5PM1_I2C_FREQ_100K)

/* rails */
pm1.setLdoEnable(bool)          // L1  (3V3_L1_EN)  - RTC + IMU
pm1.setDcdcEnable(bool)         // L2  (3V3_L2_EN)  - ESP32-S3 and friends
pm1.setBoostEnable(bool)
pm1.ldoSetPowerHold(bool)       // retain L1 across shutdown
pm1.boostSetPowerHold(bool)
pm1.gpioSetPowerHold(pin, bool)

/* shutdown, reset, timers */
pm1.shutdown()
pm1.setSingleResetDisable(bool)
pm1.timerSet(uint32_t seconds, m5pm1_tim_action_t action)
pm1.timerClear()
pm1.setI2cSleepTime(uint8_t seconds)
pm1.wdtSet(uint8_t timeout_sec) / pm1.wdtFeed() / pm1.wdtGetCount(uint8_t*)

/* GPIO + wake */
pm1.gpioSetMode / gpioSetPull / gpioSetDrive / gpioSetFunc / gpioSetOutput / gpioGetInput
pm1.gpioSetWakeEnable(M5PM1_GPIO_NUM_n, bool)
pm1.gpioSetWakeEdge(M5PM1_GPIO_NUM_n, M5PM1_GPIO_WAKE_FALLING)

/* interrupts */
pm1.irqClearGpioAll / irqClearSysAll / irqClearBtnAll
pm1.irqSetGpioMaskAll / irqSetSysMaskAll / irqSetBtnMaskAll / irqSetGpioMask

/* telemetry */
pm1.readVbat(uint16_t* mv) / readVin / read5VInOut / readVref / readTemperature
pm1.getPowerSource(m5pm1_pwr_src_t*) / getWakeSource(uint8_t*, cleanType)
```

Timer actions, verbatim from the vendor page:

```cpp
typedef enum {
    M5PM1_TIM_ACTION_STOP     = 0b000,  // Stop, no action
    M5PM1_TIM_ACTION_FLAG     = 0b001,  // Set flag only
    M5PM1_TIM_ACTION_REBOOT   = 0b010,  // System reboot
    M5PM1_TIM_ACTION_POWERON  = 0b011,  // Power on
    M5PM1_TIM_ACTION_POWEROFF = 0b100   // Power off
} m5pm1_tim_action_t;
```

## 6. Minimal procedures

### 6.1 Timed power-off / power-on (`reported-working` — vendor's own sketch)

Reproduced from `docs.m5stack.com/en/arduino/papermono/m5pm1_m5ioe1`. This is the one
procedure here that M5Stack publishes as working. It has still **not been run on
hardware in this record**.

```cpp
#include <M5Unified.h>
#include <M5PM1.h>
M5PM1 pm1;

void setup() {
  auto cfg = M5.config();
  cfg.clear_display = false;
  M5.begin(cfg);
  const m5pm1_err_t err = pm1.begin(&M5.In_I2C, M5PM1_DEFAULT_ADDR, M5PM1_I2C_FREQ_100K);
  if (err != M5PM1_OK) { /* halt */ }
  M5.Display.setEpdMode(epd_mode_t::epd_fast);
  M5.Display.drawString("BtnA: power on after 10s", M5.Display.width()/2, 280);
}

void loop() {
  M5.update();
  if (M5.BtnA.wasPressed()) {                 // shut down, come back in 10 s
    pm1.timerSet(10, M5PM1_TIM_ACTION_POWERON);
    pm1.shutdown();
  }
  if (M5.BtnB.wasPressed()) {                 // stay up 10 s, then power off
    pm1.timerSet(10, M5PM1_TIM_ACTION_POWEROFF);
  }
}
```

### 6.2 Shut down and wake on motion, keeping L1 alive (`reported-working` as a vendor fragment)

The important part is `setLdoEnable(true)` + `ldoSetPowerHold(true)` **before**
`shutdown()` — that is what keeps the IMU powered in a state where the ESP32-S3 is not.

```cpp
pm1.gpioSetWakeEnable(M5PM1_GPIO_NUM_4, true);
pm1.gpioSetWakeEdge  (M5PM1_GPIO_NUM_4, M5PM1_GPIO_WAKE_FALLING);   // active-low INT1
pm1.setSingleResetDisable(false);

/* ... configure BMI270 any-motion on INT1, active-low, push-pull ... */

pm1.setLdoEnable(true);      // L1 on
pm1.ldoSetPowerHold(true);   // and keep it on through shutdown
pm1.setLedEnLevel(true);
pm1.shutdown();
```

Full BMI270 configuration is in [`imu.md`](imu.md).

### 6.3 ESP32-S3 deep sleep via M5Unified

```cpp
M5.Power.deepSleep(seconds_us, /* touch_wakeup = */ true);
```

> ⚠ **`touch_wakeup` substitutes, it does not add.** On this board M5Unified swaps the
> EXT0 wake pin from GPIO1 (the M5PM1 IRQ) to GPIO4 (the touch INT) when
> `touch_wakeup` is true (`Power_Class.cpp:1654`, `:1786`). You get touch wake **instead
> of** the M5PM1 interrupt path, not as well as. `executed-success` on the source read.

## 7. Two operational traps

### 7.1 The first I²C transaction after M5PM1 idle-sleep fails

M5Stack, verbatim:

> "After it enters sleep, the **first communication from the ESP32-S3 is used to wake the
> M5PM1 and therefore fails.** Valid communication completes on the next attempt after
> wakeup."

Their own firmware works around it by calling `pm1.setI2cSleepTime(0)` **twice** in a row
(`hal_board.cpp:38–39`) — the first call is the sacrifice. If you have retry-free I²C
code, `setI2cSleepTime` will look intermittently broken.

### 7.2 Every optional rail defaults off

Each switched LDO carries a **1 MΩ pulldown on its enable** (`R24`, `R26`, `R23`), so
every optional rail is **off** on cold power-up. That is the correct failure mode for a
battery product, and it means firmware must explicitly bring up the panel rail before the
display responds. **A blank screen is the expected result of forgetting.**

## 8. Silicon / board / framework / observed limits

| Class | Limit |
|---|---|
| **Board** | RTC and IMU interrupts do not reach the ESP32-S3 at all (§3) |
| **Board** | The M5PM1 owns `CHIP_PU` and the GPIO0 boot strap. **You cannot reset yourself independently of it** |
| **Firmware (M5PM1)** | The register map is a *firmware API*, not silicon. Addresses moved between revisions — read `SW_REV` (`0x03`) before assuming a layout |
| **Firmware (M5PM1)** | First I²C transaction after idle-sleep fails (§7.1) |
| **Framework (M5Unified)** | `touch_wakeup` substitutes the wake pin (§6.3) |
| **Observed** | Default single-click reset is aggressive enough that **two independent third-party projects disable it** — `pm1.setSingleResetDisable(true)` |
| **Unknown** | **No current figure of any kind exists** for any state (§10) |

## 9. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| Sleep + [display](epaper-display.md) | ✅ ideal | The e-paper image persists with the rail off. Wait for `BUSY` to clear, then drop the rail |
| Sleep + [RTC alarm](rtc.md) | ✅ down to **L1** | The intended low-power pattern |
| Sleep + [motion wake](imu.md) | ✅ down to **L1** | idem. Requires `ldoSetPowerHold(true)` |
| Sleep + [touch wake](touch.md) | ✅ only in **L2** | Touch does not reach the M5PM1 |
| Touch wake + M5PM1 IRQ wake, same call | ❌ | §6.3 |
| Sleep + [microSD](microsd.md) mounted | ⚠ unmount first | The card's rail is L3B; dropping it under an open file is a corruption path |
| Sleep + [LoRa](lora.md) RX | ⚠ | The LoRa rail is switched by M5PM1 `G2`; sheet 1 lists LoRa as an L2 wake source, but no firmware exercises that path |
| Sleep + [charging](battery-and-charging.md) | ✅ | The IP2315 charges independently of the M5PM1 state |
| Sleep + [frontlight](frontlight.md) | ❌ | The boost rail is L3B |

## 10. Debugging

| Symptom | Cause |
|---|---|
| Wake-on-alarm never fires | You configured the wake on an ESP32-S3 GPIO. It has to be M5PM1 `G0` (§3) |
| Wake-on-motion never fires | Same, on `G4`; **or** you used the vendor prose's active-**high** polarity, which is wrong — see [`imu.md`](imu.md) |
| Board wakes but the IMU is dead | You did not `ldoSetPowerHold(true)`; L1 went down with everything else |
| `setI2cSleepTime` appears to fail | §7.1 — retry once |
| Board resets on a single power-button tap | Documented behaviour; `setSingleResetDisable(true)` |
| Display blank after a state transition | The panel rail (M5IOE1 `IO3`) defaults off and must be re-asserted (§7.2) |
| I²C bus wedged | Documented recovery is a **short press of the power button**. See [`battery-and-charging.md`](battery-and-charging.md) |

## 10b. ESP32 light sleep — a disputed report, and the dispute is inside one source

Two third-party projects appear to disagree about whether ESP32 light sleep works
on this board. **The disagreement is weaker than it first looks**, and the reason
is worth recording as a method lesson.

### The claim

`ciniml/paper_name_plate`'s `DESIGN.ja.md` §2.6, dated 2026-09-05:

> 「light sleep は esp-hal 1.1 でこの基板では戻ってこないため不採用（JOURNAL 2026-09-05）。」
>
> *"Light sleep was not adopted because on esp-hal 1.1 it does not return on this
> board (JOURNAL 2026-09-05)."*

`不採用` = "not adopted / rejected". Specific, dated, names the HAL version.

### The counter-example

`Corvelis/m5-touch-card` (C++) states in its README: *"While dark, controls lock
and the idle CPU enters light sleep."* The Japanese original agrees —
「通信などの処理がないときはライトスリープ」, *"light sleep when there is no processing
such as communication"*.

### ⚠ But the same Rust document says something different elsewhere

§2.3, step 8 of the **same file**:

> 「未: ESP32 light sleep（USB ログが止まるため保留）、PM1 タイマー起床。」
>
> *"Not done: ESP32 light sleep (**on hold because USB logging stops**), PM1 timer
> wake."*

`保留` = "deferred / on hold" — a **completely different and much weaker reason**
than "does not return". The two statements coexist, unreconciled, in the shipped
document. The 2026-09-05 entry is later and presumably supersedes the earlier
one, but both are present.

### Assessment

A prior analysis quoted only the stronger statement and graded it *"specific,
dated, names the HAL version, and cost them a design change"* — concluding the
fault localises to **esp-hal rather than the silicon**. That conclusion may well
be right, but it rests on:

1. the stronger of **two conflicting statements** in one document,
2. a **JOURNAL entry that was never captured** — only a one-line citation of one,
3. an attribution of `m5-touch-card`'s stack to ESP-IDF-Arduino that is
   **unverified** (its `CMakeLists.txt` was not read).

**Recorded as: unresolved.** What is reasonably supported is that *one Rust porter
using esp-hal 1.1 chose not to ship light sleep*, and that *a C++ project reports
using it*. Anything stronger — particularly "esp-hal is at fault" — is not
established. Deep sleep is unaffected and is what both the vendor firmware and
this page's §2 describe.

## 11. What is not established

- **No current or battery-life figure of any kind is published, and none was measured.**
  The state table says what is *powered*, never what it *costs*. This is the largest
  single gap in the record for a board whose entire pitch is low power.
- Whether L3A and L3B are separate switch groups or a documentation distinction.
- Whether KEY1/KEY2 are genuinely M5PM1 wake inputs (sheet 1 says so; no firmware uses
  them that way).
- The `U4` (`3V3_L0`) enable net could not be read with confidence.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; the power architecture is identical on C153 and C153-LITE |
| Framework range | M5Unified 0.2.21 · M5PM1 1.0.7 · M5IOE1 1.0.9 · ESP-IDF 5.5.1 |
| Evidence | State table and rails: **schematic**, `executed-success` extraction. API list: **vendor page + library header**. §6.1/§6.2 sketches: **`reported-working`** (vendor-published) but **`not-tested`** here. Interrupt polarity: **corroborated by the shipped binary** |
| Confidence | High on structure and wiring; **zero on power consumption**, which is unmeasured |
| Last verified | **2026-09-01** |

## Related

- [`../power-architecture.md`](../power-architecture.md) — rails, enables, charging, the full wake table
- [`../pin-naming-and-the-pyg-ambiguity.md`](../pin-naming-and-the-pyg-ambiguity.md)
- [`rtc.md`](rtc.md) · [`imu.md`](imu.md) · [`touch.md`](touch.md) · [`battery-and-charging.md`](battery-and-charging.md) · [`io-expander.md`](io-expander.md)
- [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) · [`components/puya/py32l020f15u6`](../../../../components/puya/py32l020f15u6/README.md)
