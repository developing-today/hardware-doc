# Tanmatsu — development and flashing

> Toolchain, flash layout, recovery, and the three ways to get software onto the device.
> Snapshot **2026-08-24**. Sources: `tanmatsu-documentation` @ `bd3ded51`, `tanmatsu-launcher` @ `20022fce`, `tanmatsu-template` @ `907fb965`.
> **No hardware was available.** Every command below is `reported-working` (quoted from vendor documentation) or `inferred`. **None is `executed-success`.**

---

## 1. Three ways to run code

| Route | What it is | Use when |
|---|---|---|
| **AppFS app** | Build a firmware binary, install it into the app filesystem; the launcher starts it | Normal app development — this is the intended path |
| **Full firmware flash** | `esptool` the whole thing, replacing the launcher | Bringing up a custom firmware, or recovery |
| **App repository** | Publish to the official repo; users install over the air | Distribution |

The **template app** ([`Nicolai-Electronics/tanmatsu-template`](https://github.com/Nicolai-Electronics/tanmatsu-template)) is the starting point for the first route; it uses **PAX graphics**, Badge.team's 2D graphics library.

---

## 2. ESP32-P4 flash layout

16 MB `W25Q128JVS`. The stock partitioning:

| Start | End | Size | Contents |
|---|---|---|---|
| `0x000000` | `0x001FFF` | 8 KB | *unused* — reserved for secure boot |
| `0x002000` | `0x007FFF` | 24 KB | **Second-stage bootloader** |
| `0x008000` | `0x008FFF` | 4 KB | Partition table |
| `0x009000` | `0x018FFF` | 64 KB | ⚠ **`coredump`** — the docs say "unused"; the real partition CSV says coredump. See [`software-architecture.md` §2](software-architecture.md) |
| `0x019000` | `0x01CFFF` | 16 KB | NVS |
| `0x01D000` | `0x01FFFF` | 12 KB | ⚠ Actually **8 KB `otadata` + 4 KB `phy_init`** at `0x1F000` |
| `0x020000` | `0x21FFFF` | **2 MB** | Firmware slot **A** |
| `0x220000` | `0x41FFFF` | **2 MB** | Firmware slot **B** |
| `0x420000` | `0xC1FFFF` | **8 MB** | **AppFS** — type `0x43`, subtype `3`. A **cache tier**, not the storage limit — see [`software-architecture.md` §3](software-architecture.md) |
| `0xC20000` | `0xFFFFFF` | 3.9 MB | FAT filesystem |

Two design decisions worth noting:

- **Secure boot is *permanently disabled* by design**, "to prevent accidental bricking". The 8 KB at the start of flash is left unused as a result. This is a deliberate trade of security for recoverability — reasonable for a hacker tool, but it does mean you cannot build a verified-boot product on stock Tanmatsu.
- **8 MB of AppFS** is the largest single region — more than the two firmware slots combined. The device is designed around holding many apps, not one.

The bootloader offset `0x2000` is fixed by the ESP32-P4 ROM.

---

## 3. Flashing the launcher with esptool

Download `tanmatsu.zip` from the [launcher releases](https://github.com/Nicolai-Electronics/tanmatsu-launcher/releases). It contains `.bin` files (flashable) and `.elf` files (debug symbols, for decoding backtraces).

| File | Flash address |
|---|---|
| `bootloader.bin` | `0x002000` |
| `partition-table.bin` | `0x008000` |
| `ota_data_initial.bin` | `0x01d000` |
| `tanmatsu-launcher.bin` | `0x020000` |
| `locfd.bin` (FAT filesystem) | `0xc20000` |

**Full flash — erases your files:**

```bash
python -m esptool --chip esp32p4 -b 460800 \
  --before default_reset --after hard_reset write_flash \
  --flash_mode dio --flash_size 16MB --flash_freq 80m \
  0x2000 bootloader.bin \
  0x8000 partition-table.bin \
  0x1d000 ota_data_initial.bin \
  0x20000 tanmatsu-launcher.bin \
  0xc20000 locfd.bin
```

**Firmware only — preserves the FAT partition** (omit the last line):

```bash
python -m esptool --chip esp32p4 -b 460800 \
  --before default_reset --after hard_reset write_flash \
  --flash_mode dio --flash_size 16MB --flash_freq 80m \
  0x2000 bootloader.bin \
  0x8000 partition-table.bin \
  0x1d000 ota_data_initial.bin \
  0x20000 tanmatsu-launcher.bin
```

> Status: **`reported-working`** — both commands are quoted verbatim from the vendor documentation. Not executed here.

Note these commands do **not** touch the AppFS partition at `0x420000`, so installed apps survive a firmware reflash.

---

## 4. Getting into the bootloader

The ESP32-P4 ROM exposes USB-serial/JTAG unconditionally, so the device is recoverable even with no valid firmware.

**Procedure** (vendor-documented):

1. Hold the **power button** until the device turns off.
2. Hold the **third button on the right side** — the `-` / "down" button.
3. While still holding `-`, plug in the USB-C cable.
4. The device powers on and **the screen stays black**. This is correct.

The device now enumerates in USB download mode.

---

## 5. BadgeLink — managing the device over USB

BadgeLink is a **WebUSB / Python** protocol for managing apps, settings and files. It works because firmware can swap the ESP32-P4's USB PHY 1 away from USB-serial/JTAG to a custom USB interface.

**Switching the device into USB device mode:** press the **purple diamond key** (second from the top right of the keyboard). The status icon top-right changes from a bug (debug mode) to a USB icon. It can take a second.

**Setup:**

```bash
# from https://github.com/badgeteam/esp32-component-badgelink/releases → tools.zip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Linux permissions** — without this the device is not accessible as a non-root user:

```bash
sudo cp 60-badgelink.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

**Running:** `./badgelink.sh` on Linux/macOS (it activates the venv for you); on Windows activate the venv manually and run `python badgelink.py`.

Example operations from the documentation:

```bash
./badgelink.sh appfs list                      # list installed apps
./badgelink.sh appfs download konsool64 konsool64.bin
```

There is also a **Chromium/Edge WebUSB** front-end, so no local install is needed for basic management.

> Status: **`reported-working`**, quoted from vendor docs. Not executed.

---

## 6. AppFS

**AppFS** is the mechanism behind the launcher. It is an ESP-IDF component that implements a pseudo-filesystem for firmware binaries **plus a bootloader modification** that can start a firmware directly out of that partition.

Lineage worth knowing: AppFS was created by **Jeroen Domburg (sprite_tm)** for the **PocketSprite**, and has since been extended and maintained by **Badge.team**. It supports ESP-IDF 5.3+, with bootloader modifications for ESP32, ESP32-C6 and ESP32-P4.

**Apps need no changes to be launched by AppFS.** You only need the component if you are building a *launcher*.

```bash
idf.py add-dependency "badgeteam/appfs^1.0.0"
```

Adding the dependency exposes the API but does **not** apply the bootloader changes. Those need symlinks:

```bash
mkdir bootloader_components
ln -s managed_components/badgeteam__appfs bootloader_components/appfs
ln -s managed_components/badgeteam__appfs/bootloader_main bootloader_components/main
```

This symlink step is easy to miss and produces a build that appears fine but cannot boot apps.

---

## 7. Reflashing the coprocessor from the ESP32-P4

Unusual and worth highlighting: the **CH32V203 coprocessor can be reprogrammed by the ESP32-P4** over RVSWD, using [`nicolaielectronics/rvswd`](https://components.espressif.com/components/nicolaielectronics/rvswd), which can program CH32V20x and CH32V30x parts.

Firmware source: [`Nicolai-Electronics/tanmatsu-coprocessor-firmware`](https://github.com/Nicolai-Electronics/tanmatsu-coprocessor-firmware) (**MIT**), driver component: [`esp32-component-tanmatsu-coprocessor`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-coprocessor).

The vendor's own advice: *"Modifying the firmware is of course possible but is not recommended."* The coprocessor owns power sequencing — bad firmware there is a much worse failure mode than bad P4 firmware, and it is not covered by the ROM-bootloader safety net.

---

## 8. The ESP32-C6 radio

The C6 is a **radio peripheral**, not a second application processor. It runs an `esp-hosted`-derived firmware ([`tanmatsu-radio`](https://github.com/Nicolai-Electronics/tanmatsu-radio), Apache-2.0) and the P4 drives it through [`esp32-component-tanmatsu-wifi`](https://github.com/Nicolai-Electronics/esp32-component-tanmatsu-wifi) (MIT).

Its USB-serial/JTAG interface is on the same USB-C hub, so it can be flashed over the same cable.

> ⚠ Its **boot-mode pin is shared with the USB-A port enable** — see [`pinouts-and-buses.md` §6](pinouts-and-buses.md#6-usb-topology). Reflashing the radio glitches USB-A power.

---

## 9. Board support package

The BSP is **not** in the Tanmatsu repositories — it lives at [`badgeteam/esp32-component-badge-bsp`](https://github.com/badgeteam/esp32-component-badge-bsp), which supports eleven targets:

`bornhack-2024-pov`, `bornhack-2025-circle`, `esp32-p4-function-ev-board`, `esp32-s31-korvo-1`, `hackaday2025`, `hackerhotel-2024`, `heltecv3`, `kami`, `mch2022`, **`tanmatsu`**, `why2025`

That target list is itself informative: Tanmatsu is one device in a **shared badge software ecosystem**, and the `esp32-p4-function-ev-board` target means much Tanmatsu code can be developed on Espressif's own P4 dev kit.

Keyboard handling lives in [`targets/tanmatsu/badge_bsp_input.c`](https://github.com/badgeteam/esp32-component-badge-bsp/blob/main/targets/tanmatsu/badge_bsp_input.c) — the authoritative keymap, including the full AltGr layer, is the table at roughly line 352.

---

## 10. Keyboard API

The coprocessor scans the matrix; the P4 receives **decoded** events. Each event carries:

- an **ASCII byte**
- a **UTF-8 string**, already resolved for the active modifier layer
- a **modifier bitmask**

So you do not implement a keymap — you consume characters. The six coloured function keys arrive as `BSP_INPUT_NAVIGATION_KEY_F1`…`F6`:

| Symbol | Colour | Event |
|---|---|---|
| ✕ | red | `F1` |
| △ | orange | `F2` |
| ☐ | yellow | `F3` |
| ◯ | green | `F4` |
| ☁ | blue | `F5` |
| ◇ | magenta | `F6` |

Their meaning is defined by the running application. The layout is based on **US-International with AltGr**, and the AltGr layer covers accented Latin characters, `€ ¥ ¤ © ® ™ µ ± « » ¡ ¿ ½ ¼ ¾ ² ³`, plus several **combining diacritical marks** on `= ; ' , .` and the shifted number row.

Whether a character actually appears depends on your application's **font coverage** — the keymap will happily emit `ð` or `Œ` into a font that lacks them.

---

## 11. Documentation build

The official docs are Sphinx + MyST markdown, built from [`tanmatsu-documentation`](https://github.com/Nicolai-Electronics/tanmatsu-documentation) with a `Makefile` and GitHub Actions (`build.yml`, `deploy.yml`). A full snapshot of the source is preserved at [`artifacts/source-snapshots/tanmatsu-documentation/`](artifacts/source-snapshots/tanmatsu-documentation/).

---

## Related

- [`README.md`](README.md) — architecture
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — JTAG, USB, expansion
- [`software-and-apps.md`](software-and-apps.md) — the app ecosystem
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — what is unverified
