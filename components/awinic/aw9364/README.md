# Awinic AW9364 (AW9364DNR)

- **Category:** LED backlight **boost driver** with a one-wire (pulse-count) brightness
  interface; typically 4 parallel LED strings.
- **Manufacturer:** Shanghai Awinic Technology Co., Ltd.
- **Retrieved:** 2026-09-07
- **Sibling Awinic records here:** [`aw32901`](../aw32901/README.md) ·
  [`aw35122`](../aw35122/README.md) · [`aw39112`](../aw39112/README.md) ·
  [`aw9967`](../aw9967/README.md)

The backlight driver of the **LilyGO T-Display-S3**, designator `U4`.

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part marking on the schematic | **`AW9364DNR`** | designator/part string `EP 9 U4 AW9364DNR LEDK1 LEDK2 LEDK3 LEDK4` recovered from `T_Display_S3.pdf` @ `ec889e7` |
| Package pins visible | `EP` (exposed pad), plus `LEDK1`–`LEDK4` — **four LED cathode channels** | same |
| Datasheet | **not retrieved.** Awinic does not publish AW9364 on an open portal, and LilyGO does not mirror it | — |
| Local artifact | **none** | — |

> **This record is built from a schematic part string and general knowledge of the AW936x
> family, not from a datasheet.** That is stated up front because it is unusual for this
> repository. Nothing below is transcribed from a primary document.

## 2. What the four LEDK pins mean for the board

Four cathode channels means the panel's backlight is **four LED strings in parallel**, each
current-regulated. That is a normal arrangement for a 1.9″ strip and it explains why the
board's backlight is bright and reasonably even.

## 3. The control interface, and why PWM behaves oddly

The AW936x family accepts brightness in two ways:

1. **Enable/PWM.** Hold the control pin high for on; PWM it for crude dimming. This is what
   every LilyGO example and every community sketch does — `ledcAttach(38, …); ledcWrite(38, d)`.
2. **One-wire pulse count.** Pull the pin low and back high *N* times within a timeout window
   to select one of 16 brightness steps, then hold high. The chip counts edges.

**These two mechanisms interact.** A PWM waveform *is* a pulse train, so at some frequencies
and duties the driver can interpret PWM edges as brightness commands. The practical symptom is
brightness that steps rather than ramps, or that changes when the PWM frequency changes.

**Evidence status: `inferred`.** The mechanism is the documented behaviour of one-wire LED
drivers of this class; **it has not been verified on an AW9364 datasheet or on hardware**, and
no LilyGO document mentions it. It is recorded because it is the only available explanation for
the non-linear dimming behaviour users describe, and because the alternative — assuming linear
PWM dimming — silently produces a bad UI.

**What would settle it:** obtain the AW9364 datasheet, or measure backlight luminance against
PWM duty at two PWM frequencies.

## 4. Board integration notes

- The driver sits on the **gated `V3V` rail**, so it is dead until GPIO15 is high. A board with
  GPIO38 high and GPIO15 low shows **no backlight at all** — which people read as a dead
  backlight rather than a dead rail.
- Conversely GPIO38 high with GPIO15 high but no panel initialisation gives a **lit but blank**
  screen, the classic "backlight on, nothing displayed" report.
- Arduino core 3.x renamed `ledcSetup`/`ledcAttachPin` to `ledcAttach`/`ledcDetach`; LilyGO's
  dimming snippets predate that.
  ([firsthand report](https://old.reddit.com/r/esp32/comments/1tnop7r/lilygo_tdisplay_s3_clock_with_ds18b20_and_pir/),
  2026-05-25)

## 5. Gaps

- **No datasheet.** Awinic's public site does not list AW9364; no vendor mirror was found in
  any LilyGO repository. Two acquisition routes worth trying next: LCSC's product page for the
  `AW9364DNR` order code, and Awinic's `datasheet` subdomain used by the four sibling records
  in this repository.
- The one-wire timing window, step count and the exact PWM frequency at which the two
  mechanisms collide are all **unknown**.
- Not verified on hardware.

## 6. Used by

### LilyGO T-Display-S3 / T-Display-S3 Touch
→ [`devices/lilygo/t-display-s3`](../../../devices/lilygo/t-display-s3/README.md)

Designator `U4`. Drives the 1.9″ panel's backlight from **GPIO38** (`PIN_LCD_BL`,
`TFT_BL` in `Setup206`, `TFT_BACKLIGHT_ON HIGH`). Four LED channels, `LEDK1`–`LEDK4`.
Powered from the GPIO15-gated `V3V` rail. Practical guidance:
[`features/display.md`](../../../devices/lilygo/t-display-s3/features/display.md).
