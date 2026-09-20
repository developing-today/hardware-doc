# X4 Pro — frontlight (dual warm/cool)

> Two-channel colour-temperature LED frontlight. **Unique to the X4 Pro** in the
> ESP32 Xteink family. Evidence: hardware-confirmed. Last verified 2026-09-04.

## Capability summary

| Channel | GPIO | Colour | LEDC channel |
|---|---:|---|---:|
| `frontlight.gpio` | **8** | cool / white | 4 |
| `frontlight.gpioWarm` | **9** | warm | 5 |

Both **active-HIGH** — driving a pin high lights that LED; init drives it LOW
(off) and brightness raises duty.

Config: `FrontlightConfig{8, 25000, 10, true, 9}` — **25 kHz, 10-bit**.

## API

`FrontlightManager` mixes the two channels:
- `setBrightness()` — total level
- `setColorTemperature()` — warm/cool split

Stock persists the state in NVS as `lightWarmValue`, `lightColdValue`, `lightCT`,
`lightBri`, `lightOn`.

## A version conflict, resolved

| Source | Frequency | Resolution |
|---|---|---|
| Original board bring-up dump | **10 kHz** | — |
| Stock **7.0.8** | **25 kHz** | 10-bit |

Same GPIO pair, same active-high polarity. The SDK follows the **directly
recovered 7.0.8 value (25 kHz / 10-bit)**. This PWM change is independent of the
panel-waveform change between firmware versions — do not conflate them.

## Resource conflicts

LEDC channels 4 and 5 are reserved. On the **X4 Classic**, GPIO8 and GPIO9 are
**button inputs**, so code that unconditionally configures them as PWM outputs
will break that device — always gate on `FREEINK_CAP_FRONTLIGHT`.

## Pitfall

A whole-panel light-then-dark flash during a fast page turn is **the e-ink
waveform, not the frontlight**. The refresh routines never touch LEDC. See
[`display.md`](display.md).

## Status

`hardware-confirmed` — *"driving each pin high lights that LED"*, identities
"nailed down".
