# Serial device access for embedded development

> Getting `/dev/ttyUSB0` or `/dev/ttyACM0` to appear, be writable, and stay put
> long enough to flash a board. Device-independent; Linux-first, with macOS and
> Windows notes.
>
> Written 2026-09-04. **No board was attached to a host while writing this**, so
> commands are `reported-working` from documentation and long-standing practice,
> not `executed-success`. The failure modes described are well-attested; the
> exact output on your machine will differ.

Related: [`guides/nixos`](../nixos/README.md) §4 covers how *this project's*
NixOS host is configured. This guide is the general version.

## The short diagnostic

Three questions, in order. Most problems are answered by the first two.

```bash
lsusb                    # 1. Is the device enumerating at all?
dmesg --follow           # 2. Which driver bound it, and to which node?
ls -l /dev/ttyUSB* /dev/ttyACM*   # 3. What owns the node, and can you write it?
```

If `lsusb` shows nothing, it is cable or power — a startling share of "driver
problems" are **charge-only USB cables**. If `dmesg` shows the device attaching
and immediately detaching, jump to [ModemManager and brltty](#the-two-processes-that-steal-your-port).

## Which node you get, and why it matters

| Bridge chip | Kernel driver | Node | Seen on |
|---|---|---|---|
| WCH CH340 / CH341 | `ch341` | `/dev/ttyUSB*` | Cheap ESP32/Arduino clones |
| WCH CH9102 / CH343 | `ch341` (newer kernels) | `/dev/ttyUSB*` | Newer M5Stack, many ESP32-S3 boards |
| Silicon Labs CP2102 / CP2104 | `cp210x` | `/dev/ttyUSB*` | ESP32 devkits, many vendor boards |
| FTDI FT232R / FT2232 | `ftdi_sio` | `/dev/ttyUSB*` | Older/professional boards, JTAG adapters |
| **Native USB (no bridge)** | `cdc_acm` | **`/dev/ttyACM*`** | ESP32-S3, ESP32-C3, ESP32-S2, RP2040 |

**The `ttyUSB` vs `ttyACM` split is the single most useful thing to internalise.**
A board with a USB-serial bridge chip appears as `ttyUSB*`; a board whose MCU
implements USB itself appears as `ttyACM*`. They behave differently:

- **`ttyUSB*` (bridge)** — the bridge stays enumerated regardless of what the MCU
  does. Reset the MCU and the port persists. DTR/RTS drive the auto-reset circuit.
- **`ttyACM*` (native USB)** — the USB device *is* the MCU. **Reset it and the
  port vanishes and re-enumerates**, often with a different number. This is
  normal, not a fault, and it is why `esptool` sometimes reports the port
  disappearing mid-operation on an ESP32-S3.

Some boards, including several documented in this knowledge base, expose **both**:
a bridge for the UART console and native USB for JTAG/CDC. You may see
`ttyUSB0` and `ttyACM0` from one cable.

## Permissions — and the Arch trap

The node exists but you get `Permission denied`. Check ownership:

```bash
ls -l /dev/ttyUSB0
# crw-rw---- 1 root dialout 188, 0 ...   <- Debian/Ubuntu/Fedora
# crw-rw---- 1 root uucp    188, 0 ...   <- Arch
```

**The group differs by distribution, and this is the most common wasted hour:**

| Distribution | Group |
|---|---|
| Debian, Ubuntu, Linux Mint, Raspberry Pi OS | `dialout` |
| Fedora, RHEL | `dialout` |
| **Arch, Manjaro, EndeavourOS** | **`uucp`** |
| openSUSE | `dialout` |

Every "add yourself to `dialout`" tutorial is wrong on Arch. Add yourself to the
group that actually owns the node:

```bash
sudo usermod -aG uucp "$USER"     # Arch
sudo usermod -aG dialout "$USER"  # most others
```

**Then log out and back in.** Group membership is established at login;
`newgrp uucp` works in the current shell as a stopgap. `id` should list the group
before you retry.

Arch additionally has a `lock` group used by some tools for `/var/lock`
serial lockfiles; add it if a tool complains about lockfiles specifically.

### The `chmod 666` shortcut

`sudo chmod 666 /dev/ttyUSB0` works and is reset on every replug. It is fine for
a one-off. It is not a fix, and on a shared machine it grants every user access
to the port.

## udev rules

Group membership is enough for most boards. Write a rule when you want a
**stable name**, non-standard permissions, or to exempt a device from an
interfering service.

`/etc/udev/rules.d/99-embedded.rules`:

```
# CH340
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
# CH9102 / CH343
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d4", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
# CP210x
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
# FTDI
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
# Espressif native USB (ESP32-S2/S3/C3 USB-JTAG/serial)
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
```

Reload without rebooting:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Confirm the vendor/product IDs for *your* board rather than trusting the table —
`lsusb` gives them as `ID vvvv:pppp`.

### Stable names for multi-board setups

If you have several boards attached, `ttyUSB0` is whichever enumerated first.
Pin a symlink by serial number:

```
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{serial}=="0001", SYMLINK+="esp32-devkit"
```

Then use `/dev/esp32-devkit`. Devices whose bridge has no unique serial (many
CH340s ship with an identical or absent serial) cannot be distinguished this way
— pin them by physical USB port path (`KERNELS=="1-1.2"`) instead.

## The two processes that steal your port

Both present as "the port appears then disappears", or "flashing fails only in
the first few seconds after plugging in".

### ModemManager

ModemManager probes new serial devices to see whether they are cellular modems,
sending AT commands for several seconds. On a freshly plugged board this collides
with `esptool` and looks like a flaky bridge.

- **Per-device fix (preferred):** `ENV{ID_MM_DEVICE_IGNORE}="1"` in a udev rule,
  as above.
- **Blunt fix:** `sudo systemctl disable --now ModemManager` — fine on a
  development machine with no cellular modem.

### brltty

`brltty`, the braille display daemon, claims **CH341 devices** because some braille
displays use the same USB IDs. It grabs the device and the tty node never
appears. This is a long-standing, widely reported issue on Ubuntu and Arch, and
it is baffling if you do not know about it — the symptom is a device that
enumerates in `lsusb` but produces no `/dev/ttyUSB*`.

```bash
sudo systemctl stop brltty-udev.service
sudo systemctl mask brltty-udev.service
# or, if you do not use a braille display at all:
sudo apt remove brltty     # Debian/Ubuntu
sudo pacman -Rns brltty    # Arch
```

If `dmesg` shows `ch341-uart converter now attached to ttyUSB0` immediately
followed by a detach, this is almost certainly the cause.

## NixOS

NixOS ignores `/etc/udev/rules.d` edits across rebuilds — configure declaratively.

```nix
{
  # Ship vendor udev rules from packages
  services.udev.packages = with pkgs; [
    platformio-core.udev   # covers most ESP32/Arduino bridges
    openocd
  ];

  # Or write rules inline
  services.udev.extraRules = ''
    SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
    SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
  '';

  users.users.<you>.extraGroups = [ "dialout" "plugdev" ];
}
```

Two NixOS-specific gotchas:

- **`plugdev` does not exist by default.** Rules referencing it are silently inert
  until you create the group. This project's host creates it explicitly — see
  [`guides/nixos`](../nixos/README.md) §4.
- `platformio-core.udev` is a separate output; `pkgs.platformio` alone does not
  install the rules.

Apply with `sudo nixos-rebuild switch`, then replug.

## macOS

Native USB CDC (`ttyACM`-class) devices need **no driver** — they appear as
`/dev/cu.usbmodem*`.

Bridges vary:

- **CP210x, FTDI** — drivers have shipped in macOS since 10.11ish; usually
  `/dev/cu.usbserial-*` with no install.
- **CH340/CH341** — historically needed WCH's kext, and on Apple Silicon the
  situation has changed across releases. Modern macOS generally enumerates them,
  but a vendor driver is still sometimes required.

**Use `/dev/cu.*`, not `/dev/tty.*`.** Both appear for the same device. The
`tty.*` node blocks on carrier detect (DCD) and will hang; `cu.*` ("call-up")
does not. This trips up almost everyone once.

```bash
ls /dev/cu.*
```

## Windows

- **Native USB CDC** — enumerates as a COM port with no driver on Windows 10/11.
- **CP210x, FTDI** — Windows Update usually supplies drivers; vendor installers
  exist if not.
- **CH340** — very often needs WCH's driver installed manually. Counterfeit
  FTDI chips have historically been bricked by official FTDI drivers; genuine
  parts are unaffected.

Find the port in Device Manager under **Ports (COM & LPT)**; use `COM3`-style
names. Nothing analogous to the permissions problem exists — if the port is
listed, you can open it, though **only one application at a time**. A serial
monitor left open in an IDE is the usual cause of "access denied" on Windows.

## ESP32-specific behaviour

Relevant to most boards in this knowledge base.

**Auto-reset.** Bridges wire DTR and RTS to `EN` and `GPIO0` so the flasher can
reset the chip into download mode. Boards without that circuit need a manual
button sequence — typically hold BOOT, tap RESET, release BOOT.

**Native USB and disappearing ports.** On ESP32-S3/C3 the CDC device is the MCU.
Flashing resets it, so the port disappears and returns. `esptool` handles this,
but a serial monitor holding the old node will fail. Close monitors before
flashing.

**Some boards have a firmware-controlled port.** Where the USB peripheral is
implemented by application firmware rather than a bridge, **flashing broken
firmware removes the port**, and recovery needs the hardware download-mode
sequence. Boards whose reset and boot straps are driven by a separate
power-management MCU — the
[M5Stack PaperMono](../../devices/m5stack/papermono/README.md) is one — put that
sequence under that MCU's control rather than a physical button.

**Verify before blaming permissions:**

```bash
esptool.py --port /dev/ttyUSB0 chip_id
```

A successful chip ID means enumeration, driver, permissions and the reset circuit
are all working, and any remaining problem is in the build or the flash command.

## Failure-mode summary

| Symptom | Most likely cause |
|---|---|
| Nothing in `lsusb` | Charge-only cable, dead port, unpowered board |
| In `lsusb`, no `/dev/tty*` | **brltty** (CH341), or no driver for the bridge |
| Node appears then vanishes | **ModemManager** probing, or native-USB reset (normal) |
| `Permission denied` | Wrong group — **`uucp` on Arch**, `dialout` elsewhere; or not re-logged-in |
| `Device or resource busy` | A serial monitor or another flasher holds the port |
| Port number changes each replug | No stable symlink — pin by serial or USB path |
| Works as root only | Group membership not applied to the current session |
| Flash starts then fails partway | Auto-reset circuit, cable quality, or an underpowered board |

## Evidence boundary

Nothing here was executed against attached hardware in this pass. The USB IDs,
group names and driver names are stable, long-documented facts, but **confirm the
IDs for your own board with `lsusb`** rather than copying the table. The NixOS
snippets follow the same structure as this project's working host configuration
([`guides/nixos`](../nixos/README.md)) but were not rebuilt to verify.
