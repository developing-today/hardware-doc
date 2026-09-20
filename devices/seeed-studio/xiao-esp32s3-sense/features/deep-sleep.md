# Deep sleep and low power — XIAO ESP32S3 Sense

> The board's weakest area, and the workaround that makes it usable.
> Snapshot **2026-08-24**. Figures below are **owner measurements from the Seeed forum**, not vendor claims and not measured here — see [`../community.md` §4A.2](../community.md#4a2-deep-sleep-current--the-vendor-figures-are-unachievable-and-here-is-why).

## 1. The headline: vendor sleep figures are not achievable with the camera

Seeed publishes **three contradictory** deep-sleep figures (33.51 µA, 3 mA, 26.5 mA). Owner measurements show that **once the camera has been initialised, none of them is reachable**.

| Condition | Measured | Source |
|---|---:|---|
| Camera + SD fitted, **never initialised** | ~2.8 mA | `StuartsProjects` |
| **After taking a picture and saving to SD** | **~90 mA** | two reporters |
| ESPHome, camera *not* configured | ~140 µA | `JaBa` |
| ESPHome, camera configured | ~90 mA | `JaBa` |
| Light sleep, board + camera + SD | ~4 mA | `StuartsProjects` |
| Light sleep, bare XIAO (no daughterboard) | ~3 mA | `StuartsProjects` |
| **Best achieved** (OV3660 + standby trick) | **<1 mA** | `jksemple` |

**The gap between the wiki's 33.51 µA and a real ~90 mA is roughly 2,700×.** If you sized a battery from the datasheet figure, your device will last about a thousandth as long as you expected.

## 2. Why — there is no way to power the camera down

The Sense daughterboard [hard-strap the camera's `PWDN` and `RESET` pins](../sense-daughterboard.md#4-camera-fpc-connector-ja1-24-pin): FPC pin 6 is pulled **up** through R9 (10 kΩ) and pin 8 pulled **down** through R10 (10 kΩ). Neither reaches the ESP32-S3.

So the sensor is permanently enabled and out of reset whenever the 3.3 V rail is up. `esp_deep_sleep_start()` stops the CPU; it does nothing to the camera.

A forum user reached the same conclusion independently:

> "The ESP32Cam provided hardware support to cut power to the OV2640 during deep sleep... **Seeedstudio did not provide any means in the Sense design to cut power nor to drive the POWERDWN pin**, so there are no hardware [options]."
> — `jksemple`

This is an **architectural** limitation, not a software one. It is the single biggest weakness of the board.

## 3. The workaround — software standby via a sensor register

Writing an OV3660/OV5640 standby register before sleeping recovers most of the current:

```cpp
#include "esp_camera.h"
#include "esp_sleep.h"

void enterDeepSleep(uint64_t seconds) {
  sensor_t *s = esp_camera_sensor_get();
  if (s) s->set_reg(s, 0x3008, 0x40, 0x40);   // software standby (OV3660/OV5640)

  esp_sleep_enable_timer_wakeup(seconds * 1000000ULL);
  esp_deep_sleep_start();                     // never returns
}
```

Measured effect, same sketch and board, by sensor:

| Sensor | Plain deep sleep | **+ standby register** | Improvement |
|---|---:|---:|---|
| OV2640 | 22.3 mA | 22.3 mA | **none — does not work** |
| **OV3660** | 37.8 mA | **1.45 mA** | **~26×** |
| OV5640 | 104 mA | *(reported, value truncated)* | — |

Active-mode draw also drops from ~135 mA to ~50 mA when standby is asserted.

### ⚠ Two important caveats

**Cancelling standby appears to break the camera.** `StuartsProjects` reports that after issuing the standby command, attempting to resume leaves the sensor non-functional. With no `RESET` line, only a full power cycle recovers it.

Practically this means the pattern **must** be: `wake → init camera → capture → standby → deep sleep → (reset on wake)`. Deep sleep resets the SoC anyway, so re-initialising the camera on each wake is the normal path. It does **not** work for pausing a live camera.

**The OV2640 uses a different mechanism** and it is widely reported not to work — `set_reg_bits(sensor, BANK_SENSOR, COM2, 4, 1, enable)` returns `SCCB_Write Failed addr:0x30`.

**Therefore: for any battery-powered design, use an OV3660.** This is a second, independent reason to skip the [OV5640 upgrade](../market-and-pricing.md#3-upgrading-to-the-ov5640), and a reason to check which sensor an older board has.

## 4. Where the residual ~1 mA goes

Even with the sensor in standby, ~1 mA remains. `jksemple` attributes it to the rest of the board:

> "Looking at the datasheet for OV3660 the standby current is apparently **20 µA–40 µA**, so I guess most of the additional power consumption in light sleep when using the Sense board is due to the **regulators, SD card and microphone**."

That is consistent with the [daughterboard schematic](../sense-daughterboard.md#3-power--the-camera-needs-three-rails): two always-on LDOs (U1, U2), the microSD holder on a permanently-powered rail, and the microphone wired directly to 3V3 with no enable.

**None of those can be switched off in software either.** The floor for a Sense board with the daughterboard attached is therefore around 1 mA — roughly **70× worse** than the bare XIAO ESP32S3's 14 µA.

## 5. What to do about it

Ordered by effort:

| Approach | Result | Effort |
|---|---|---|
| **Use an OV3660 + the standby register** | ~1–1.45 mA | Software only |
| **Detach the daughterboard** when not needed | 14 µA (bare board figure) | Mechanical |
| Cut JP1/JP2 to remove the microphone | Small saving; frees GPIO41/42 | [Soldering, boards must be separated](../sense-daughterboard.md#2a-physical-layout-from-the-brd) |
| **External MOSFET / load switch on the daughterboard supply** | Approaches bare-board figures | Hardware modification |
| **Use a different board** | µA-class | See below |

One forum user concluded the same thing after exhausting the software options:

> "Despite all my efforts and trying all proposed solutions, it seems that the camera is still powered quite a lot when put in sleep... I'm going for the solution of an **external Pro Mini driving a MOSFET**."
> — `Congduc_Pham`

**If your design genuinely needs µA-class sleep, this is the wrong board.** The [XIAO nRF52840 Sense](../comparisons-and-recommendations.md#5-versus-xiao-nrf52840-sense) sleeps at ~5 µA and has battery sensing — it just has no camera or Wi-Fi. The XIAO ESP32C6 is cited on the forum at 15–22 µA.

## 6. Realistic battery life

Recomputed from **measured** figures rather than the vendor's. 3.7 V cell, ignoring self-discharge and converter efficiency.

| Cell | @ 1.45 mA (OV3660 + standby) | @ 90 mA (no standby) | @ 14 µA (bare board, no daughterboard) |
|---|---|---|---|
| 250 mAh | ~7 days | ~2.8 h | ~2 years |
| 500 mAh | ~14 days | ~5.5 h | ~4 years |
| 1000 mAh | ~29 days | ~11 h | ~8 years |
| 2000 mAh | ~57 days | ~22 h | ~16 years |

Duty-cycled capture designs land between columns and are dominated by **how long the camera is powered per wake** — including sensor start-up and auto-exposure settling, which happen on every wake because deep sleep resets the SoC.

Compare this table with the [one computed from vendor figures](battery-and-power.md#6-runtime-estimates), which suggests multi-year life at 34 µA. **The measured reality is days-to-weeks, not years.**

## 7. Sleep mechanics on this board

```cpp
#include "esp_sleep.h"
esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);   // 60 s
esp_deep_sleep_start();
```

- **Deep sleep resets the SoC.** Execution restarts at `setup()`; only RTC memory survives. Re-initialise the camera every wake.
- **`while(!Serial);` will hang a battery-powered board forever** — no USB host means `Serial` never becomes ready. This is the most common cause of "my board does nothing on battery" and it is a copied-tutorial artefact, not a fault. See [`../community.md` §4A.4](../community.md#4a4-other-recurring-forum-themes).
- The **USB CDC device disappears** on sleep and re-enumerates on wake, so the serial monitor must be reopened. Expected, not a fault.
- GPIO wake sources must be RTC-capable pins; with the daughterboard fitted your [free-pin choice is narrow](gpio-adc-and-pwm.md#1-the-eleven-pins-you-get).

## 8. Evidence status

Everything quantitative here is **firsthand owner measurement** from a 74-post forum thread, with multiple independent reporters and at least one using a Nordic PPK2. It is **not** reproduced here — no hardware was available.

Seeed staff responded in that thread that the wiki figures illustrate the relative impact of different peripherals rather than promising an achievable number. That is a reasonable clarification, but the wiki does not say so, and the figures are presented as specifications.

**Verify on your own hardware before committing to a battery design.** This is the single most important thing to measure on this board — see [`../performance.md` §8](../performance.md#8-what-to-benchmark-first).

## 9. Related
- [`battery-and-power.md`](battery-and-power.md) — charging, rails, vendor figures
- [`camera.md`](camera.md) — the `PWDN`/`RESET` limitation
- [`../sense-daughterboard.md`](../sense-daughterboard.md) — why the residual current exists
- [`../performance.md`](../performance.md) · [`../community.md`](../community.md) · [`../comparisons-and-recommendations.md`](../comparisons-and-recommendations.md)
