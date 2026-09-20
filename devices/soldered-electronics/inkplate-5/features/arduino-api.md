# Inkplate Arduino API — practical reference

> The parts of the Inkplate Arduino library that actually matter when writing firmware, distilled from Soldered's `arduino.rst` (4,556 lines) and the library source.
> Snapshot **2026-08-24**. Applies to the **Inkplate 5** (`Inkplate5`) and **Inkplate 5 Gen 2** (`Inkplate5V2`).

This is not an API dump — the [upstream reference](../artifacts/docs/Inkplate-documentation/source/arduino.rst) is preserved in this tree and is authoritative for signatures. What follows is the subset with non-obvious behaviour, resource cost or footguns.

## The five things that will bite you

| # | Issue | Consequence |
|---|---|---|
| 1 | `partialUpdate()` is **1-bit mode only** | Silently does nothing useful in 3-bit greyscale |
| 2 | Partial updates accumulate ghosting | "After a few updates creates blurry parts of the screen" — must periodically call `clean()` |
| 3 | The SD card is **power-gated** | `sdCardInit()` before any SD access, or it simply fails |
| 4 | `einkOff()` / power-supply cycling dominates refresh time | The `leaveOn` flag exists specifically to avoid it |
| 5 | Several functions are **board-specific** | `readTouchpad`, `setFrontlight`, `waitForEpd` do not exist meaningfully on the Inkplate 5 |

---

## Display modes

```c
display.selectDisplayMode(INKPLATE_1BIT);   // monochrome
display.selectDisplayMode(INKPLATE_3BIT);   // 8-level greyscale
```

| Mode | Bits/px | Buffer @1280×720 | `partialUpdate()` |
|---|---:|---:|---|
| `INKPLATE_1BIT` | 1 | 115,200 B | ✅ **supported** |
| `INKPLATE_3BIT` | 4 (packed) | 460,800 B | ❌ **not supported** |

> Updates only the changed parts of the screen. **(monochrome/INKPLATE_1BIT mode only!)**

This is the single most important architectural constraint. **If you want a responsive UI, you must work in 1-bit.** Greyscale forces a full refresh every time — around 1.0–1.1 s on this family versus roughly 0.12–0.26 s for a partial update.

A text device like [ZeroWriter Ink](../../../zerowriter/zerowriter-ink/README.md) runs 1-bit for exactly this reason.

## Refresh: the functions and their cost

| Function | What it does |
|---|---|
| `display()` | Full refresh, both modes |
| `display1b()` / `display3b()` | Mode-specific full refresh |
| `partialUpdate(bool _forced=false, bool leaveOn=false)` | Update only changed regions, 1-bit only |
| `preloadScreen()` | Stage the buffer without refreshing |
| `clearDisplay()` | Clear the **buffer** — not the panel |
| `clean()` | Physically clear ghosting from the panel |

### `leaveOn` — the undocumented performance lever

```c
void partialUpdate(bool _forced = false, bool leaveOn = false);
```

> **leaveOn** — if set to 1, it will disable turning supply for eink after display update in order to save some time needed for power supply … or increase refreshing speed.

Powering the [TPS65186](../../../../components/texas-instruments/tps65186/README.md) rails up and down costs real milliseconds per refresh, and every rail transition is [I²C traffic through the expander](../pinouts-and-buses.md#3-pcal6416a-io-expander-u9--complete-pin-map).

**If you are refreshing repeatedly — typing, scrolling, animating — pass `leaveOn = true`** and only drop the supply when going idle. This is very likely part of how ZeroWriter reached [~100 ms](../../../zerowriter/zerowriter-ink/development-history.md#the-e-paper-latency-problem-and-how-it-was-solved) on the same panel.

The trade-off is power: leaving the e-paper supply up costs current, so it is exactly the wrong choice before deep sleep.

### `_forced` and deep sleep

> For advanced use with deep sleep. Can force partial update in deep sleep.

After waking from deep sleep the library does not know what is on the panel, so it would normally refuse a partial update. `_forced` overrides that — useful for a periodic-refresh dashboard, and a correctness hazard if the panel content is not what you assume.

### Ghosting

> After a few updates creates **blurry parts of the screen**. Fixed by calling `Inkplate::clean();`

There is no automatic ghosting management. **Budget a `clean()` every N partial updates** — N is a judgement call the library does not make for you. ZeroWriter exposes this to the user as `CTRL+R` ([shortcuts](../../../zerowriter/zerowriter-ink/software-and-shortcuts.md)), which is a reasonable pattern: let the human decide when the screen looks bad.

---

## Power control

| Function | Notes |
|---|---|
| `einkOff()` | "Turns the panel off to save energy" |
| `einkOn()` | Bring the panel supply back up |
| `readPowerGood()` | Reads the TPS65186 `PWR_GOOD` line — [expander pin 8](../pinouts-and-buses.md#3-pcal6416a-io-expander-u9--complete-pin-map) |
| `setPanelState()` / `getPanelState()` | Track/force supply state |

`readBattery()` returns a `double` voltage — backed by the [switched divider on GPIO35](../pinouts-and-buses.md#5-battery-sensing-is-a-switched-divider). Not available on Inkplate 2.

`readTemperature()` reads the on-board NTC. Worth surfacing in any long-running application: **e-paper waveforms are temperature-dependent**, and behaviour outside 0–50 °C is not guaranteed by the panel.

## Storage

```c
display.sdCardInit();      // MUST come first — powers the card
SdFat  &sd  = display.getSdFat();
SPIClass &spi = display.getSPI();
```

`sdCardInit()` asserts the [SD power MOSFET](../pinouts-and-buses.md#6-microsd-k11--spi-and-power-switched) via expander pin `SD_PMOS_PIN` before touching SPI. Skipping it and driving `SdFat` directly fails, because the card has no power.

The library exposes the underlying `SdFat` and `SPIClass` objects, so you are not restricted to its wrappers — useful if you need custom SPI settings or to share the bus.

## Images

| Function | Source |
|---|---|
| `drawImage()` | Generic — buffer, path or URL depending on overload |
| `drawBitmapFromSD()` | microSD |
| `drawBitmapFromWeb()` | HTTP — requires Wi-Fi |

`drawBitmapFromWeb()` plus the `NetworkClient` functions is the whole "e-paper dashboard" use case in two calls. Combined with the RTC alarm this gives the canonical low-power pattern: wake on RTC → connect → fetch → draw → deep sleep.

## Low-level panel access

The library exposes the raw scan primitives — `vscan_start()`, `hscan_start()`, `vscan_end()`, `pinsZstate()`, `pinsAsOutputs()`, `sendCommand()`, `sendData()`, `resetPanel()`.

These are how you would implement custom waveforms or a faster refresh path — which is precisely what ZeroWriter did. `pinsZstate()` tri-states the panel bus, which matters if you want to share those GPIOs (though on this board [almost all of them are committed to the display](../pinouts-and-buses.md#7-broken-out-headers)).

**This is not a supported path**, and driving e-paper with incorrect waveforms can damage a panel.

## Board-specific functions

Do **not** assume these exist on the Inkplate 5 / Gen 2:

| Function | Availability |
|---|---|
| `readTouchpad()` | **Older e-radionica (blue) boards only.** Soldered-era boards have no touchpads |
| `setFrontlight()` | 6PLUS, 6FLICK, 4TEMPERA — **not** Inkplate 5 or Gen 2 |
| `waitForEpd()` | "Supported only on Inkplate 2" |
| `partialUpdate()`, `einkOff()`, `selectDisplayMode()` | Not on 6COLOR or Inkplate 2 |
| `readBattery()` | Not on Inkplate 2 |

The Inkplate 5 family has **no frontlight and no touch** — see the [family comparison](../README.md#family-comparison). The [Zerowriter Fold](../../../zerowriter/zerowriter-fold/README.md) adds a frontlight, which is one reason it is claimed to be in-house hardware rather than an Inkplate.

## Other API areas

`arduino.rst` also documents, and the preserved copy covers in full:

| Section | Line | Contents |
|---|---:|---|
| System Functions | 44 | init, SD, panel state, power, temperature, battery, low-level scan |
| Drawing Functions | 571 | primitives, images, polygons, scanline fill, rotation, display modes |
| **NetworkClient** | 3061 | Wi-Fi HTTP fetch |
| **Real-Time clock** | 3204 | PCF85063A — time, date, epoch, **alarms**, timers |
| **Touchscreen** | 3786 | 6PLUS / 6FLICK / 4TEMPERA only |

The RTC section is the largest after drawing, and is the foundation of every battery-powered Inkplate project: set an alarm, deep-sleep, wake, refresh. Those same functions are exposed over UART in [Peripheral Mode](peripheral-mode.md#real-time-clock-pcf85063a).

## Related

- [`../README.md`](../README.md) — device record and family comparison
- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) — the hardware these APIs drive
- [`peripheral-mode.md`](peripheral-mode.md) — the same capabilities over UART
- Upstream reference: [`arduino.rst`](../artifacts/docs/Inkplate-documentation/source/arduino.rst) (preserved)
