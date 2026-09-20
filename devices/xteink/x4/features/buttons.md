# X4 — buttons (ADC resistor ladder)

> **Six buttons on two ADC pins.** Four on the front face, three on the right
> edge (one of which is power). 2026-09-04.

| Group | GPIO | Buttons |
|---|---:|---|
| 1 | **1** | Back · Confirm · Left · Right |
| 2 | **2** | Up · Down |
| power | **3** | digital, active-LOW |

`InputStyle::XteinkAdcLadder`, `analogSetAttenuation(ADC_11db)`.

## Calibration data — from three real devices

The SDK records the raw 12-bit readings it derived the thresholds from
(**[SDK]** `InputManager.cpp:29–45`). This is **firsthand measurement**, the only
such data in the family:

| | BACK | CONFIRM | LEFT | RIGHT |
|---|---:|---:|---:|---:|
| unit 1 | 3597 | 2760 | 1530 | 6 |
| unit 2 | 3470 | 2666 | 1480 | 6 |
| unit 3 | 3470 | 2655 | 1470 | 3 |
| **avg** | **3512** | **2694** | **1493** | **5** |

Unit-to-unit spread is ~3.6 % at the top of the ladder — small, but the SDK
deliberately uses **midpoints between adjacent averages** rather than fixed
thresholds because they are *"much more tolerant of different devices"*:

```c
const int InputManager::ADC_RANGES_1[] = {ADC_NO_BUTTON, 3100, 2090, 750, INT32_MIN};
const int InputManager::ADC_RANGES_2[] = {ADC_NO_BUTTON, 1120, INT32_MIN};
```

Group 2's local index is remapped by `+4` to `BTN_UP`/`BTN_DOWN`.

## Limits

- **One button per group at a time.** A ladder yields one voltage; two buttons in
  the same group produce a third, wrong reading. Cross-group chords are fine.
- **No interrupts.** The ladder must be polled, unlike the X4 Classic's discrete
  interrupt-driven keys.
- ADC1 also carries the battery sense on GPIO0 — three channels, read sequentially.

## The struct trap

`input = {0, 1, 2, 3, 4, 5, 3, false}` — the first six values are **logical button
indices, not GPIO numbers**. Only `power` (7th field, GPIO3) is a pin. Reading
them as pins gives a plausible-looking but entirely wrong map.

## Feel

*"the buttons on the X4 are clickier and louder. The X3's buttons are somewhat
mushy and quieter."* — [r/xteinkereader `1syav96`](https://old.reddit.com/r/xteinkereader/comments/1syav96/),
2026-04-28, 412 pts. Firsthand comparative ownership report.

## Status

`hardware-confirmed` — thresholds derived from three physical devices.
