# T-Display-S3 — buttons

| Button | GPIO | Role | Notes |
|---|---|---|---|
| **BOOT** | **0** | `PIN_BUTTON_1`, and the ESP32-S3 **strapping** pin | active low. Held at reset → ROM download mode |
| **user** | **14** | `PIN_BUTTON_2` | active low, ordinary GPIO |
| **RST** | — | hardware reset, **not** a GPIO | cannot be read by software |

Three tactile switches are fitted (`S2`, `S3`, `SW` = `SW-PB` in the schematic designator
census). Two are next to the USB-C connector; the third is on the opposite long edge.

## Reading them

```cpp
pinMode(0,  INPUT_PULLUP);   // BOOT
pinMode(14, INPUT_PULLUP);   // user
// both read LOW when pressed
```

Internal pull-ups are sufficient; the schematic shows `RINT 100K`-class parts around the button
network but the individual nets were not traced.

## The BOOT-button trap

GPIO0 is a strapping pin. **Holding it during reset puts the chip in download mode instead of
running your firmware.** That is a feature — it is the recovery path — but it means:

- Do not use GPIO0 for anything that could be low at power-on. A momentary button is fine; a
  sensor output is not.
- If your product has a case where the button can be pressed while power is applied, users can
  put it into download mode and see a dead device.

## Wake from sleep

`examples/Sleep/Sleep.ino` @ `ec889e789b3cf093412689a143f7f37b42b56af7` is LilyGO's reference.
GPIO0 and GPIO14 are both RTC-capable on the ESP32-S3, so either works with
`esp_sleep_enable_ext0_wakeup()` / `ext1`. Details and the current implications:
[`deep-sleep.md`](deep-sleep.md).

## AceButton and debouncing

LilyGO's AMOLED examples pull in `AceButton v1.10.1`; the base-board examples debounce by hand.
Either is fine. There is no hardware debounce on this board.

## Comparison with the rest of the family

| Board | Buttons |
|---|---|
| T-Display-S3 / Touch | GPIO0, GPIO14, RST |
| T-Display-S3 AMOLED (all) | GPIO0, **GPIO21**, RST |
| T-Display-S3 Long | GPIO0 + a **hardware slide switch** (`SW1` = `MSK12C02-HB`) |
| T-Display-S3 Pro | **three** user buttons: GPIO0, GPIO12, GPIO16 (`BOARD_USER_BUTTON {0,12,16}`) |

**GPIO14 is not portable.** Code that hardcodes `PIN_BUTTON_2 14` will read a floating pin on
every AMOLED board.
