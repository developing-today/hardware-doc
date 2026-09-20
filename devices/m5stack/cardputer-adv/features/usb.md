# Cardputer ADV — USB

> **Question:** *"How do I flash it, get a serial console, or make it act as a USB keyboard?"*
> Verified **2026-09-04**.

## Hardware

USB-C on the **Stamp-S3A**, wired to the ESP32-S3's **native USB-OTG** peripheral. There is
**no USB-UART bridge chip** — no CP210x, no CH340. Confirmed by designator census of the
Stamp-S3A schematic: `J2 USB-TYPEC`, `R1`/`R2` 5.1 kΩ CC resistors, `F1` 6 V/1 A PPTC,
`L5` common-mode choke, `D14` `PESDNC2FD5VB`, `D3`/`D4` `PESDNC2FD3V3B`, `JP2`/`JP3` solder
jumpers on `USB_DU_P`/`USB_DU_N`. No bridge.

Consequences:

* The serial port **appears and disappears with the firmware**, because the CDC device is
  implemented by the running application. A crashed or non-CDC firmware means no port.
* `-DARDUINO_USB_CDC_ON_BOOT=1` and `-DARDUINO_USB_MODE=1` are in M5Stack's own PlatformIO
  profile for a reason.
* USB Serial/JTAG is available as a fallback console independent of the application.

## Download mode

M5Stack's procedure, identical on all three revisions:

> Set the side power switch to **OFF**. Then, **before powering on, hold the G0 button**, apply
> power, and release it afterwards. The device will then enter download mode.

`G0` is the button on the Stamp module, pulled up by 10 kΩ. Note this is *not* the usual
"hold BOOT, tap RESET" — **there is no reset button on the ADV**.

## Build profile

M5Stack publishes this on all three product pages:

```ini
[env:m5stack-cardputer]
platform = espressif32@6.7.0
board = esp32-s3-devkitc-1
framework = arduino
upload_speed = 1500000
build_flags =
  -DESP32S3
  -DCORE_DEBUG_LEVEL=5
  -DARDUINO_USB_CDC_ON_BOOT=1
  -DARDUINO_USB_MODE=1
lib_deps =
  M5Cardputer=https://github.com/m5stack/M5Cardputer
```

Note it targets the generic `esp32-s3-devkitc-1` board definition, not a Cardputer-specific one
— which is fine because M5GFX autodetects at runtime. Meshtastic instead uses
`board = m5stack-stamps3`, and Bruce/Launcher use `board = m5stack-cardputer` with their own
`pins_arduino.h`.

## USB HID

The ESP32-S3's native USB can enumerate as a HID keyboard, and the Cardputer's whole point is
that it has a keyboard to forward.

* `M5Cardputer/examples/Basic/keyboard/usbKeyboard/usbKeyboard.ino` (added `2c0de0e`,
  2023-10-16) — the vendor's reference.
* `Keyboard_def.h` carries a full `_kb_asciimap[128]` of **USB HID usage codes** with a `SHIFT`
  (`0x80`) flag, plus `KEY_LEFT_CTRL 0x80`, `KEY_LEFT_SHIFT 0x81`, `KEY_LEFT_ALT 0x82`,
  `KEY_FN 0xff`, `KEY_OPT 0x00`. Everything you need to be a HID keyboard is already in the
  library.
* `VoidNoi/BadCard` (★148, GPL-3.0) — BadUSB with Ducky-script support.
* Bruce: `-DUSB_as_HID=1`.
* The factory firmware also does **BLE** HID (`"CardputerADV Keyboard"`).

## Host mode

The ADV is **not** a USB host in any meaningful sense — one Type-C port, no hub, no VBUS
switching. Contrast the **CardputerZero**, which has a physical Host/Slave toggle, a
GL852G-OHY60 hub, a USB-A port and USB-Ethernet.

## Limits and pitfalls

| Limit | Class |
|---|---|
| No UART bridge — port vanishes when firmware misbehaves | board |
| No reset button; recovery is switch-OFF → hold G0 → power | board |
| PPTC F1 at 6 V/1 A limits inrush and total draw | board |
| CDC + Wi-Fi + display simultaneously is RAM-tight | silicon (no PSRAM) |
| `-DCORE_DEBUG_LEVEL=5` in the vendor profile is *verbose*; drop it for production | framework |

## Evidence status

Absence of a bridge: **verified negative** by designator census of the Stamp-S3A schematic.
Download procedure: **official** (three product pages agree verbatim).
Build profile: **official**, quoted verbatim. **Not executed by this session** — no hardware.
