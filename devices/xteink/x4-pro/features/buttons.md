# X4 Pro — buttons

> Two physical navigation keys plus power. Everything else is touch.
> Evidence: hardware-confirmed by a pull-up edge test. Last verified 2026-09-04.

## Capability summary

| Button | GPIO | Logical action | Polarity |
|---|---:|---|---|
| **Left** (side) | 0 | Up / previous page | active-LOW, `INPUT_PULLUP` |
| **Right** (side) | 7 | Down / next page | active-LOW, `INPUT_PULLUP` |
| **Power** | 3 | power | active-LOW (`powerActiveHigh = false`) |
| **Home** | — | home | **GT911 capacitive key**, see [`touch.md`](touch.md) |

`InputStyle::DigitalButtons`. Back and Confirm come from touch.

## The corrected record

An earlier revision of the FreeInk documentation described this device as having
an **ADC resistor ladder** on GPIO10 with thresholds
BACK ≈ 3580 / OK ≈ 2728 / UP ≈ 1514 / DOWN ≈ 0 (±319, raw 12-bit).

**Hardware disproved it.** The ladder matcher at IROM `0x4201f734` is real code
in the dump but is **vestigial firmware — not wired on this variant**. The device
uses plain digital buttons. GPIO7 reads `INPUT_PULLUP`, which also confirms it is
the Right button and **not** a display enable, another earlier hypothesis.

This is recorded rather than deleted because the ladder *is* the input path on the
[X3](../../x3/pinouts-and-buses.md) and [X4](../../x4/features/buttons.md), and
somebody reading the shared firmware will meet it again.

## Boot-strap warning

**GPIO0 is the ESP32-S3 boot strap.** It works fine as a button provided it is not
held during reset. Holding Left while powering on enters download mode.

## Minimal use

```c
pinMode(0, INPUT_PULLUP);   // Left  -> up/prev
pinMode(7, INPUT_PULLUP);   // Right -> down/next
pinMode(3, INPUT_PULLUP);   // Power
// pressed == LOW
```
`inferred` from the profile; the SDK's `InputManager` does this for you.

## Why only two nav keys

CrossPlay's `LOCAL_SCOPE.md` names the X4 Pro's "two side keys plus touch" as the
ecosystem's **minimum viable input**, i.e. the design floor. A firmware that needs
four nav keys will not work here without touch.

## Status

`hardware-confirmed`.
