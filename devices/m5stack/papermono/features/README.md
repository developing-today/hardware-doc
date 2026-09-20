# Feature guides — M5Stack PaperMono

Task-oriented guides. Each answers "how do I use X on this board", and states what it
costs you in pins, bus bandwidth and power, what it collides with, and which of its
limits are **silicon**, **board**, **framework** or **observed**.

> **Read this first.** There is **no PaperMono in hand**. Nothing in any guide below is
> `executed-success` on a device. Code sketches derived from M5Stack's own libraries are
> marked `inferred`; procedures M5Stack publishes as working are marked
> `reported-working`. No flash sequence, API call or register write here has been
> verified electrically. Snapshot **2026-09-01**, hardware revision **V0.6.2**.

| Guide | Covers | Headline gotcha |
|---|---|---|
| [`epaper-display.md`](epaper-display.md) | SSD1677 + DKE panel, refresh modes, OTP waveforms | **Vendor says its own M5GFX waveforms are unstable**; continuous partial refresh destroys the panel |
| [`frontlight.md`](frontlight.md) | AW9967 boost, brightness, gamma | Driven from the **M5PM1**, not the expander — and `PYG3` means the other chip |
| [`touch.md`](touch.md) | FT6336G, coordinates, wake-on-touch | Usable area is **X 5–475, Y 5–795** — a dead border you cannot widen |
| [`buttons-and-rgb-led.md`](buttons-and-rgb-led.md) | Two user keys, power button, RGB indicator | **Red has no PWM** — the LED is not a full-colour indicator |
| [`power-and-sleep.md`](power-and-sleep.md) | Five power states, wake sources, shutdown | RTC and IMU interrupts land on the **M5PM1**, not the ESP32-S3 |
| [`battery-and-charging.md`](battery-and-charging.md) | IP2315, battery ADC, charge state | `0x75` **not appearing in an I²C scan is correct** — the charger is gated off the bus |
| [`wifi-and-bluetooth.md`](wifi-and-bluetooth.md) | 2.4 GHz Wi-Fi, BLE | Bluetooth is a **silicon** capability M5Stack never specifies |
| [`lora.md`](lora.md) | Stamp LoRa-1262 / SX1262 via RadioLib | Sub-GHz — it does **not** share the Wi-Fi radio. Regional bands are undocumented |
| [`nfc.md`](nfc.md) | ST25R3916, ISO14443A/B, FeliCa, ISO15693 | **Not fitted on the Lite**; which card types were actually tested is unknown |
| [`imu.md`](imu.md) | BMI270, motion wake | Its interrupt goes to the **power manager**, and vendor prose has the polarity wrong |
| [`rtc.md`](rtc.md) | RX8130CE, alarms, timed wake | Alarm wake works with the ESP32-S3 **unpowered** |
| [`microsd.md`](microsd.md) | 4-bit SDMMC on GPIO8–13 | Power (IO14) and detect (IO1) are both behind the **expander** |
| [`microphone.md`](microphone.md) | PDM mic, I²S | On **GPIO45/46 — both strapping pins** |
| [`buzzer.md`](buzzer.md) | Magnetic buzzer on GPIO42 | LEDC only; there is **no speaker and no amplifier** |
| [`usb-and-serial.md`](usb-and-serial.md) | USB CDC, UART0, download mode | **No USB-PD.** Download mode is the **power button**, not a reset button |
| [`io-expander.md`](io-expander.md) | M5IOE1 — the chip everything else goes through | `M5IOE1_PIN_3 = 2`, and `PYG3` denotes two different pins |

## Cross-cutting constraints

Four facts shape every design on this board:

1. **There is no free GPIO and no expansion connector.** No Grove port, no M-Bus, no
   header. Anything you add shares the single I²C bus or steals an expander pin.
   See [`../resources-and-conflicts.md`](../resources-and-conflicts.md).
2. **Two auxiliary microcontrollers sit between the application processor and the
   board.** Panel power, panel reset, touch power and reset, microSD power and detect,
   microphone power, NFC enable, LoRa reset and antenna switch, two LED colours and the
   charger's bus gate are behind the [M5IOE1](io-expander.md); reset, boot mode, rail
   enables and every deep wake source are behind the
   [M5PM1](power-and-sleep.md). Neither is optional.
3. **`PYG<n>` is ambiguous and the ambiguity is dangerous.** Read
   [`../pin-naming-and-the-pyg-ambiguity.md`](../pin-naming-and-the-pyg-ambiguity.md)
   before acting on any vendor pin name.
4. **Octal PSRAM is a hard build requirement.** Without `qio_opi`, M5GFX aborts display
   init with `"M5PaperMono need OPI-PSRAM enabled"` and you get a blank screen on
   working hardware.

## Deliberately short guides

Three guides are short because the evidence is thin, and say so rather than padding:

- **UiFlow2 has no guide at all.** M5Stack advertises UiFlow2 support and publishes a
  page that states no required firmware version, no block list and no limitations. That
  is a documented gap, confirmed by full-text search, not a retrieval failure. Tracked
  in [`../coverage.md`](../coverage.md) and `gaps-and-conflicts.md` G4.
- [`lora.md`](lora.md) — **regional band configuration is undocumented.** One wideband
  868–923 MHz SKU, no per-region variant, no certification, no module datasheet.
- [`nfc.md`](nfc.md) — **no evidence exists about which card types were actually
  tested.** The library exposes four technology layers; nobody has reported results.

## Related

- [`../README.md`](../README.md) — device overview and the "How do I…?" index
- [`../coverage.md`](../coverage.md) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md) · [`../compatibility-and-status.md`](../compatibility-and-status.md)
- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) · [`../power-architecture.md`](../power-architecture.md) · [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md)
- [`vendors/m5stack`](../../../../vendors/m5stack/README.md) — how to find M5Stack documentation
