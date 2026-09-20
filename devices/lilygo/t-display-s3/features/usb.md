# T-Display-S3 — USB, and the `USB CDC On Boot` trap

> Applies to: **every board in the [T-Display-S3 family](../../t-display-s3-shared/README.md)**,
> and to essentially every native-USB ESP32-S3/C3/S2 board. Written here because this is where
> people hit it. Evidence status: **vendor-documented** + **many independent user reports**;
> not hardware-verified by this pass.

## The one-paragraph version

The T-Display-S3 has **no USB-UART bridge**. There is no CH340, no CP2102, no FTDI — the
ESP32-S3's own USB peripheral drives the Type-C connector directly (GPIO19/20 → `U5`). That
buys you flashing, `Serial`, JTAG debugging and USB-device roles over one cable. It costs you
three things that a bridge would have given you for free: an auto-reset circuit, a serial port
that exists when your firmware is broken, and a `Serial` object that does not care whether a
host is attached. **The board setting `USB CDC On Boot` decides which of those you lose**, and
with it selected — as LilyGO requires — a board running from a battery **stops during startup
and waits for a PC that will never arrive**.

## Why a board "does nothing"

```
Symptom                                   Almost always
────────────────────────────────────────  ─────────────────────────────────────────────
Works on USB, dead on battery             GPIO15 not driven high  → power-and-battery.md
Works on USB, hangs on battery            USB CDC On Boot = Enable → this page
No serial output at all                   USB CDC On Boot = Disable, and you are
                                          watching the USB port instead of GPIO43/44
Port appears then vanishes, repeatedly    firmware crashed/reconfigured USB → manual
                                          download mode (below)
```

The second and third rows are the *same setting* producing opposite symptoms, which is why the
trap survives so well: whichever way you have it set, the failure looks like a hardware fault.

## What the setting actually does

With `USB CDC On Boot = Enable` (PlatformIO: `-DARDUINO_USB_CDC_ON_BOOT=1`), the Arduino core
aliases `Serial` to the USB CDC device and, during core startup, **waits for the host to open
the port** before proceeding. On a desk with a PC attached that wait is invisible. On battery
it never ends.

LilyGO documents it, twice, in two different repos:

> "**If you use an external power supply instead of USB-C, please disable the CDC option.** The
> board waits for USB access on startup when CDC is enabled.
> — Arduino IDE: `Tools` > `USB CDC On Boot` > `Disable`
> > Disabling USB CDC turns off Serial redirection to USB-C. Serial output will come from
> > GPIO43 and GPIO44 instead."
> — `T-Display-S3/README.md` FAQ 5 @ `ec889e789b3cf093412689a143f7f37b42b56af7`

> "If you use external power supply instead of USBC, please turn off the CDC option. This is
> because the board will wait for USB access when it starts."
> — `LilyGo-AMOLED-Series/README.MD` FAQ 4 @ `6d1dc008b94578cc34ba4a0f3b223dd808ca963f`

PlatformIO form, verbatim from the same FAQ — note that it uses `-U` (undefine) rather than
`=0`, because the core tests for *definedness*:

```ini
build_flags =
    ; -DARDUINO_USB_CDC_ON_BOOT=1   ; enable: prints, and blocks at startup awaiting a terminal
    -UARDUINO_USB_CDC_ON_BOOT        ; disable: no blocking when running from the battery
```

**`-DARDUINO_USB_CDC_ON_BOOT=0` is not equivalent to `-U…` in all core versions.** Use `-U`.

## The decision table

| Your situation | `USB CDC On Boot` | Where `Serial` goes | Cost |
|---|---|---|---|
| Developing at a desk, board on USB | **Enable** | USB-C | none |
| Shipping a battery-powered device | **Disable** | GPIO43 (TX) / GPIO44 (RX) at 115200 | you need a USB-TTL adapter to see logs |
| Battery device, but you still want USB logs | Enable **and** never let the code depend on `Serial` being open | USB-C | boot still blocks — do not do this |
| Using the board as a USB HID/MIDI device | Enable, `USB Mode = CDC and JTAG` for the built-in JTAG, or the OTG mode for TinyUSB roles | — | the two USB modes are mutually exclusive; see below |

## The second, quieter setting: `USB Mode`

`USB Mode` picks which silicon block owns the port.

| `USB Mode` | PlatformIO flag | Gives you | Takes away |
|---|---|---|---|
| **CDC and JTAG** (LilyGO's default) | `-DARDUINO_USB_MODE=1` | hardware USB-Serial-JTAG: flashing, `Serial`, **and built-in JTAG debugging** over the one cable (`debug_tool = esp-builtin`) | TinyUSB device roles — no USB HID, MSC or MIDI |
| **USB-OTG (TinyUSB)** | `-DARDUINO_USB_MODE=0` | full TinyUSB: HID keyboard/mouse/gamepad, MSC, MIDI — this is what `examples/usb_hid_pad` and the MIDI shield examples need | **the built-in JTAG debugger stops working** |

This is the "USB-OTG" half of the trap. People switch to OTG mode to build a USB HID gadget,
then find their debugger gone and, worse, that a crashing TinyUSB descriptor takes the whole
port down — at which point flashing requires the manual button ritual below. The VID/PID also
changes: native USB-Serial-JTAG enumerates as **`303A:1001`** (per LilyGO's own
`boards/lilygo-t-display-s3.json`), TinyUSB as whatever your descriptor says.

## Manual download mode — the ritual

When there is no port, or it flashes in and out, put the ROM bootloader in charge. From the
README, and repeated identically in the AMOLED README:

1. Connect the board via the USB cable.
2. **Press and hold BOOT** (GPIO0, the button next to USB-C).
3. While still holding BOOT, **press RST**.
4. Release **RST**.
5. Release **BOOT**. The port should now be stable.
6. Upload.
7. Press **RST** to exit download mode.

The ROM bootloader's USB stack is in mask ROM, so this works no matter how broken the
application is. This is the reason a bricked-looking board is almost never bricked — see
[issue #16 "Device is bricked"](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/16) and
[#162](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/162), both resolved this way.

## Host-side symptoms worth recognising

- **Linux:** `Can't connect to ttyACM0` — [issue #7](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/7).
  The device is `/dev/ttyACM*` (CDC-ACM), *not* `/dev/ttyUSB*` (which is what a CH340 gives).
  If you are looking for `ttyUSB0` you will never find it. `dialout`/`uucp` group membership
  still applies.
- **Windows 10:** "does not appear as USB device" — [issue #166](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/166).
  No driver is needed for CDC-ACM on Win10+; a missing device is a cable (charge-only) or a
  blocked-boot problem, not a driver problem.
- **macOS:** enumerates as `/dev/cu.usbmodem*`.
- **A charge-only USB-C cable will do exactly this too**, and is the single most common cause
  of "no port" reports across the whole family. Rule it out first.

## Powering from something that is not USB-C

`VBUS` is **not** brought out to the headers on this board. The 5 V header pin is an *output*
sourced from USB-C. Consequences, from
[issue #205](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/205) and
[#42](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/42):

- You **cannot** charge the battery from the 5 V pin, a solar panel or a wireless charger
  without soldering to `VBUS`. LilyGO's own answer, 2022-11-12: *"We have not considered this
  situation. Maybe you can solve it by soldering a wire from VBUS."*
- Feeding 5 V into the 5 V pin **back-powers the charger input**. A firsthand report
  (2023-11-01): *"The charging voltage jumps up to 5V, because of backpowering. If you're using
  an unprotected battery it might blow up in this case!"* — evidence class: firsthand
  measurement by one owner, not independently reproduced, but consistent with the topology.
- The supported ways in are **USB-C** and **the JST battery connector** (3–6 V per a
  community answer; LilyGO states 3.7–4.2 V, and the lower bound in that community answer is
  *not* vendor-confirmed).

## Cross-references

- [`features/power-and-battery.md`](power-and-battery.md) — the GPIO15 gate, charging
- [`../development.md`](../development.md) — the flags in context, and core versions
- [`../factory-firmware.md`](../factory-firmware.md) — recovery when nothing else works
- [`../../t-display-s3-shared/README.md#31-the-usb-cdc-on-boot-trap`](../../t-display-s3-shared/README.md#31-the-usb-cdc-on-boot-trap) — family-level summary
