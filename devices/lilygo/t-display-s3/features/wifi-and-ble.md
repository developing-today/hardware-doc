# T-Display-S3 — Wi-Fi and Bluetooth LE

| | |
|---|---|
| Radio | integral to the **ESP32-S3R8** — 2.4 GHz Wi-Fi 4 (b/g/n) + Bluetooth 5 LE. **No 5 GHz** |
| Antenna | on-board ceramic chip antenna by default; a **u.FL/IPEX** footprint exists |
| Switching | move a **0 Ω resistor** (`RX` / `RX2` in the schematic; `RX` is fitted at `10R`, `RX2` is marked `NC`) |
| Matching | `L1 = 2.0 nH` series inductor in the antenna path |

## Switching to an external antenna

> "The default is onboard antenna. If you need to use an external antenna, you need to rotate
> the resistor in the red position in the image below to the position highlighted in yellow to
> switch to external antenna mode."
> — `README.md` @ `ec889e789b3cf093412689a143f7f37b42b56af7`, with an image at `./image/WiFi.png`

The schematic census corroborates the mechanism: `RX` (value `10R`) and `RX2` (explicitly
`(NC)`) form the two positions, with `XX1`/`XX2` antenna-related parts either side. **This is a
soldering job on 0402-class parts.** There is no switch and no solder-blob jumper.

## Reported range and reception

This is the board's most-complained-about non-power characteristic. Three separate threads,
spanning four years:

| Report | Date | Comments | Evidence class |
|---|---|---|---|
| ["wifi is very weak"](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/123) | 2023-03-17 | 14 | firsthand ownership, no instrumentation |
| ["My board doesn't connect to WiFi"](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/247) | 2024-05-11 | 19 | firsthand, mixed causes |
| ["wifi reception"](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/340) | 2026-04-12 | 17 | firsthand |

**No RSSI measurement, no anechoic data, and no comparison against a reference board exists in
any of them.** Treat "the Wi-Fi is weak" as *repeatedly reported by owners*, not as measured.
Confounders that appear in those threads and are worth eliminating first: 5 GHz-only SSIDs
(the ESP32-S3 cannot see them — a firsthand
[reminder from r/esp32, 2026-05-25](https://old.reddit.com/r/esp32/comments/1tnop7r/lilygo_tdisplay_s3_clock_with_ds18b20_and_pir/)),
WPA3-only networks, and a metal shell or a battery sitting over the antenna.

**Physical cause that is plausible and untested:** the antenna sits at one end of a board whose
other 90 % is a bonded LCD with a metal frame and a shielding layer. That is a poor RF
environment, and it is the structural difference between this board and a bare-module dev kit.

## Coexistence

Wi-Fi and BLE share the one radio; the ESP32-S3 time-slices them. Running both roughly halves
each one's throughput and adds latency jitter — this is silicon behaviour, not board behaviour,
and Espressif documents it.

**ADC2 is unusable while Wi-Fi is active.** The battery sense on GPIO4 is on **ADC1**, so it is
unaffected — but any additional analogue input you add must also be on ADC1
(GPIO1–GPIO10) or it will fail as soon as Wi-Fi starts. See
[`battery-voltage-measurement.md`](battery-voltage-measurement.md) §3.

## Power

Vendor figure for same-SoC boards in this family: *"(240MHz) WiFi On 90~230+ mA"*
(`LilyGo-AMOLED-Series/README.MD` @ `6d1dc00`). That is a **different board**; quoted for
order of magnitude. The peak matters for battery sizing — a 350 mAh cell cannot sustain 230 mA
for long, and transmit peaks brown out marginal supplies, which is one plausible reading of
[issue #143 "Unable to power board with wall plug, but computer USB-C works"](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/143).

## Provisioning

The factory firmware uses **ESP-Touch** (SmartConfig) — a phone app that pushes credentials
over Wi-Fi. Two things about it recur:

- It is called "ESP **Touch**", which people reliably confuse with the LCD touchscreen. That
  confusion is the entire content of [issue #212](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/212).
- SmartConfig does not work on many modern routers and phones. For anything real, use
  WiFiManager, ESPHome, or hardcoded credentials.
