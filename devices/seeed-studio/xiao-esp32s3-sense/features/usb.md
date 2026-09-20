# USB — XIAO ESP32S3 Sense

> The board has **native USB**, which is more capable — and more confusing — than a bridge chip.
> Snapshot **2026-08-24**. No hardware testing.

## 1. There is no USB-UART bridge

The ESP32-S3's USB-OTG peripheral connects **directly** to the USB-C receptacle:

```
USB-C (UBF31-0171) ──22 Ω (R3/R4)── GPIO19 (D−) / GPIO20 (D+)
CC1/CC2 ── 5.1 kΩ (R1/R2) to GND      [correct UFP pull-downs]
```

The BOM contains **no CH340, CP2102 or FTDI part**. Consequences:

| | |
|---|---|
| Serial device | **`/dev/ttyACM*`** (Linux), `/dev/cu.usbmodem*` (macOS) — *not* `ttyUSB*` |
| VID:PID (application) | **`2886:0056`** — from `pins_arduino.h` |
| VID:PID (ROM bootloader) | **`303a:1001`** — Espressif USB-Serial-JTAG |
| Charging | Works from a plain C-to-C cable (correct 5.1 kΩ CC resistors) |
| Test points | **TP7 = `USB_D−`, TP8 = `USB_D+`**, TP6 = `EN` |

TP6/TP7/TP8 are worth remembering and are undocumented by Seeed: a board with a torn-off USB-C receptacle can still be flashed by tacking wires to those pads.

## 2. The port disappears — this is normal

Because USB is provided by the application processor rather than a separate chip, **the serial device vanishes whenever the firmware crashes, reconfigures USB, or enters deep sleep.** On a CH340-style board the port persists regardless; here it does not.

This is the single most common support question for the board, and it is not a fault.

**Recovery:** hold **BOOT**, tap **RESET**, release **BOOT** — or hold **BOOT** while plugging in USB. The mask-ROM bootloader then enumerates unconditionally as `303a:1001`, regardless of what the application did.

A udev rule matching only the application VID/PID will **not** match a board in download mode, so you want both:

```
# /etc/udev/rules.d/99-xiao-esp32s3.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="2886", ATTRS{idProduct}=="0056", MODE="0666", SYMLINK+="xiao-esp32s3"
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", MODE="0666", SYMLINK+="xiao-esp32s3-boot"
```
Status: **`inferred`** — correct IDs, standard syntax, untested here.

## 3. USB CDC on boot

The Arduino option **USB CDC On Boot** decides where `Serial` goes:

| Setting | `Serial` goes to |
|---|---|
| **Enabled** | Native USB (the USB-C port) |
| Disabled | **UART0 on `D6`/`D7`** (GPIO43/44) |

Sketches that print nothing over USB are usually built with it disabled.

## 4. The board can be a USB device of any class

This is the underexploited capability. Because the S3 has a real USB-OTG peripheral, the board can present as:

- **USB CDC** (serial) — the default
- **USB HID** — keyboard, mouse, gamepad
- **USB MSC** — mass storage, e.g. exposing the microSD to a host
- **USB UVC — a standard webcam**

The last is the most interesting on a Sense board, and there is a working ESP-IDF example: [`XIAO_Webcam`](../examples/selected/XIAO_Webcam/) (MIT). Plug it into a PC and it appears in any video application — no Wi-Fi, no app, no streaming protocol, and none of the latency of a network hop.

Almost every other project treats USB purely as a flashing port. **If you need a small tethered camera, UVC is a materially better answer than MJPEG-over-Wi-Fi.**

### HID and MSC in practice

Arduino-ESP32 ships TinyUSB wrappers, so HID does not require dropping to ESP-IDF:

```cpp
// Tools > USB Mode: "USB-OTG (TinyUSB)"
#include <USB.h>
#include <USBHIDKeyboard.h>
USBHIDKeyboard Keyboard;

void setup() { Keyboard.begin(); USB.begin(); }
void loop()  { Keyboard.println("hello"); delay(5000); }
```

**MSC** (`USBMSC.h`) can expose a storage device to the host. The obvious application on a Sense board is **presenting the microSD card as a USB drive** so captured images can be copied off without removing the card — but note the host and the ESP32 cannot both own the card safely, so your firmware must relinquish it.

⚠ **Selecting "USB-OTG (TinyUSB)" mode changes how the serial port behaves**, and a sketch that claims the USB device can make the board harder to reflash. Keep [BOOT+RESET recovery](#2-the-port-disappears--this-is-normal) in mind before flashing HID/MSC firmware.

**Status:** HID and MSC are **`inferred`** — the silicon and the Arduino API both support them, and the pattern above is standard Arduino-ESP32 TinyUSB usage, but **no HID or MSC example for this board was located** in the 18-project survey, and none was tested here. UVC ([`XIAO_Webcam`](../examples/selected/XIAO_Webcam/)) is the only USB device class with a demonstrated implementation. See [`../coverage.md`](../coverage.md).

## 5. Constraints

- **USB and JTAG share the internal bridge.** With the Sense daughterboard fitted the four JTAG pins are consumed by the camera and microphone, so USB-JTAG debugging is unavailable — see [`../pinouts-and-buses.md` §7.2](../pinouts-and-buses.md#72-the-camera-and-microphone-occupy-all-four-jtag-pins).
- **The `5V` header pin is `VBUS`** — 0 V when running on battery.
- **GPIO19/20 are not available as GPIO.**
- **USB host (OTG master)** is theoretically possible on the S3, but this board has no `VBUS` supply or ID-pin arrangement for it. Not practical here.

## 6. Related
- [`../pinouts-and-buses.md` §6](../pinouts-and-buses.md#6-usb-boot-and-reset) · [`../development.md` §5](../development.md#5-usb-serial-and-recovery) · [`../factory-firmware.md`](../factory-firmware.md) · [`camera.md`](camera.md)
