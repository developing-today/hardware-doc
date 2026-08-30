# Feature guides — ESP32-P4-WIFI6-Touch-LCD-3.4C

Task-oriented guides. Each answers "How do I *X* on this board?"

| Guide | Answers |
|---|---|
| [display.md](./display.md) | Drive the 3.4 in 800 × 800 round JD9365 panel over MIPI-DSI |
| [touch.md](./touch.md) | Read GT911 capacitive touch over the shared I²C bus |
| [wifi-and-bluetooth.md](./wifi-and-bluetooth.md) | Use Wi-Fi 6 / BT 5 LE via the companion ESP32-C6 over SDIO |
| [audio.md](./audio.md) | Play through the ES8311 codec and capture via the ES7210 |
| [camera.md](./camera.md) | Capture from the MIPI-CSI camera header |
| [storage.md](./storage.md) | Mount the microSD card — note **GPIO45 powers the card rail** |
| [usb.md](./usb.md) | Use the USB OTG HS port, and the Type-C serial path |
| [expansion-header.md](./expansion-header.md) | Use the 40-pin header — **not Pi-compatible, read first** |

These apply to the [4C variant](../../esp32-p4-wifi6-touch-lcd-4c/README.md) too, except
[display.md](./display.md), which the 4C maintains
[separately](../../esp32-p4-wifi6-touch-lcd-4c/features/display.md) for its 720 × 720 panel.

**Evidence status for every guide in this directory:** vendor documentation and vendor source
code, retrieved 2026-08-24. **Nothing has been built or run on hardware.** No benchmark,
throughput, or latency figure appears anywhere, because none was measured.

## Cross-cutting resource note

GPIO7 (SDA) and GPIO8 (SCL) form **one I²C bus shared by three devices** — GT911 touch, ES8311
codec, ES7210 echo-cancel ADC. Bus contention, address conflicts, and clock-rate choice are
therefore shared concerns across [touch.md](./touch.md) and [audio.md](./audio.md), not isolated
to either. `03_i2c_tools` in the shared demo archive is the right first diagnostic.
