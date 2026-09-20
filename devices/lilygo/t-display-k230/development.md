# T-Display K230 — development

**Evidence status: everything on this page is `reported-working` or `inferred`. Nothing was
executed.** No K230 hardware and no Ubuntu build host were available on 2026-09-04. Commands are
transcribed verbatim from LilyGO's and Canaan's own documentation; the command ledger with
status labels is [`commands.md`](commands.md).

---

## 1. There are four toolchains, and they are unrelated

This is the first thing to understand about the board.

| Target | Toolchain | Language / framework |
|---|---|---|
| **K230** (the main SoC) | XuanTie GCC + Buildroot + Kendryte Linux SDK | C/C++ on Linux, LVGL for UI |
| **nRF52840** companion | **PlatformIO** `nordicnrf52`, board `nrf52840_dk_adafruit` | Arduino |
| **nRF9151** companion | **nRF Connect SDK v3.4.0** via `nrfutil sdk-manager` | Zephyr |
| SD card | `dd` / Rufus | — |

**Nothing in the ESP32 world applies.** LilyGO's own FAQ: *"Q: Can I use Arduino IDE for
T-Display K230? A: **No.** T-Display K230 is based on the Kendryte K230 RISC-V SoC and requires
the K230 SDK toolchain."*

⚠ The LilyGO **wiki** contradicts this by offering PlatformIO/Arduino instructions for an
"ESP32-S3 co-processor" — see [`GC-2`](gaps-and-conflicts.md).

---

## 2. Building the K230 system image

### 2.1 Host

LilyGO: **Ubuntu 22.04 or 24.04 recommended**. Canaan's own wiki instructions say Ubuntu 20.04 or
Docker. Windows: **WSL2 with Ubuntu only** — LilyGO explicitly warns off CMD, PowerShell, Git
Bash, MSYS2 and Cygwin, and warns not to build under `/mnt/c/...` because it "is slower and can
break Linux-style permissions or symlinks used by the SDK".

```sh
sudo apt update
sudo apt install -y git ca-certificates build-essential make rsync python3
```

### 2.2 Clone — **with submodules**

```sh
git clone --recurse-submodules https://github.com/Xinyuan-LilyGO/T-Display-K230.git t-display-k230
cd t-display-k230
# if you forgot:
git submodule update --init --recursive
```

The submodule is `k230_linux_sdk` → `https://github.com/kendryte/k230_linux_sdk.git`, pinned by
`k230_bsp/metadata/upstream_sdk_commit.txt` to **`22d02c6b6783a57a3aca7eb3160e313e772cb710`**
(branch `dev`). Cloning without `--recurse-submodules` gives you an empty SDK directory and a
build that fails immediately.

### 2.3 Toolchain and host dependencies

```sh
./scripts/setup_ubuntu.sh
```

This is `apt`-based. It installs, among other things, the **XuanTie toolchain to
`/opt/toolchain/`** — the defconfig hard-codes
`BR2_TOOLCHAIN_EXTERNAL_PATH="/opt/toolchain/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V3.0.2/"`.
On a non-FHS host this is the step that breaks; see
[`guides/nixos/riscv-and-vendor-sdk-toolchains.md`](../../../guides/nixos/riscv-and-vendor-sdk-toolchains.md).

### 2.4 Apply the board overlay, then build

```sh
./scripts/apply_to_sdk.sh
./scripts/build_sdcard_image.sh
# output:
#   k230_bsp/images/sysimage-sdcard.img
```

Clean rebuild:

```sh
rm -rf k230_linux_sdk/output
./scripts/apply_to_sdk.sh
./scripts/build_sdcard_image.sh
```

The overlay is not a patch series applied to a checkout — it is a **file overlay plus a patch
set**, catalogued in `k230_bsp/metadata/overlay_manifest.txt` (5 764 bytes) and applied by
`k230_bsp/scripts/apply.sh`. That manifest is the file to read if you want to know exactly what
LilyGO changes about the stock SDK without diffing two trees.

### 2.5 What the overlay actually contains

| Area | Contents |
|---|---|
| **U-Boot** (`u-boot-2022.10-overlay`) | `k230_canmv_v3.dts`, `k230d.dtsi`, `k230_board_common.c`, a full **boot-logo** implementation (`display_logo.c/.h`, `k230_logo.c`, `st7701.c`), and `k230_canmv_t_display_defconfig` |
| **Linux patches** | 30+ numbered patches, `0025`–`0064`. Display/DSI: `0025`, `0026`, `0029`, `0030`, `0031`, `0032`, `0033`, `0038`, `0039`, `0041`, `0042`, `0043`, `0049`, `0051`. Touch: `0034` (**307 KB**). Camera: `0036`. Graphics: `0035` GDMA rotation. LoRa: `0054`. HDMI: `0055`, `0062`. Bluetooth: `0056`, `0057`. Audio: `0058`, `0059`. UARTs: `0060`, `0061`. Thermal: `0063`. Power key: `0064`. |
| **Rejected patches** | `linux/rejected/0044-drm-canaan-use-wc-allocation-for-dumb-buffers.rejected` — **kept in the tree.** Good practice; it tells you write-combine dumb-buffer allocation was tried and did not apply. |
| **Buildroot packages** | LVGL (pinned to upstream commit `59dc7e436ae97a25e32656739ea6a943f9f11b6a` with **four** LilyGO patches), `rtl8189fs`, `rtl8723ds`, `rtl8723ds-bt`, `rtl8733bs`, `vvcam` (with `gc2093.c`) |
| **Rootfs overlay** | `S40bluetoothd`, `S41adb_mtp`, `inittab`, `k230-usb-storage-gadget`, `getty-tty1-rm69a10`, and the boot splash images `logo.xrgb` (2.8 MB) / `logo.yuv` (1.0 MB) |
| **Launcher** | `k230_phone_ui`, an LVGL application with ~50 UI modules, a 9.5 MB CJK font, a Pinyin dictionary and emoji tables |

**The LVGL fork is properly documented**, which is unusual. Upstream commit is pinned in the
directory name, and the four patches are named for what they do: a pcpp Python preprocessor
fallback, K230 plane rotation in the DRM backend, FreeType fixed-colour-bitmap scaling, and a
K230 staging scanout buffer. The pinned upstream revision the patches apply to is retained.

### 2.6 Faster iteration — deploy over SSH

Once the board is running and on the network:

```sh
./scripts/deploy_launcher.sh 192.168.1.100
./scripts/deploy_launcher.sh 192.168.1.100 --full --reboot   # launcher + boot files
```

This avoids reflashing the card for every launcher change and is the practical development loop.

---

## 3. Flashing the SD card

```sh
# Linux
sudo dd if=k230_bsp/images/sysimage-sdcard.img of=/dev/sdX bs=8M status=progress conv=fsync
sync

# macOS
diskutil unmountDisk /dev/diskN
sudo dd if=k230_bsp/images/sysimage-sdcard.img of=/dev/rdiskN bs=8m status=progress
sync
```

**Windows: Rufus, in "Write in DD Image mode".** After writing, Windows offers to format an
unknown partition — **cancel it**; those are the Linux partitions.

Canaan's own wiki instructions use `bs=1M oflag=sync` instead of `bs=8M conv=fsync`; both are
correct, LilyGO's is faster.

---

## 4. Building the nRF52840 firmware

```sh
python3 -m pip install --user platformio
cd t-display-k230-nrf52840
pio run
# .pio/build/nrf52840/firmware.{elf,bin,hex}

python3 ./scripts/uf2conv.py .pio/build/nrf52840/firmware.hex \
  -c -f 0xADA52840 -o .pio/build/nrf52840/k230_nrf52840_at.uf2
```

`platform = nordicnrf52`, `board = nrf52840_dk_adafruit`, `framework = arduino`.
UF2 family ID **`0xADA52840`** (Adafruit nRF52840 bootloader).

**Entering DFU**, in LilyGO's own words: insert a jumper wire into the `RST` port and *"quickly
touch the GND hole twice with the other end… (simulating RST being pressed twice). If you find
this difficult, touching the USB-C metal casing will achieve the same effect."* The board then
enumerates as a USB drive; drag the `.uf2` onto it. Animated guides:
`image/dfu_reset_guide_en.gif` in that repository.

There is **also a UART DFU path** driven from the K230 itself
(`tools/k230_nrf52840_dfu.cpp`, launcher page `ui_nrf52840_dfu.c`, custom bootloader
`k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex`). That is what lets the handheld update
its own BLE controller with no PC.

Runtime log: nRF52840 USB-C at 115200. **Some serial monitors need DTR asserted** or you see
nothing. Expected boot banner:

```
+BOOT:K230_NRF52840_AT
+MESH:ADV,1
DBG <ms> boot
```

---

## 5. Building the nRF9151 firmware

```sh
nrfutil install sdk-manager
nrfutil sdk-manager install --install-dir "$PWD/ncs" v3.4.0     # NCS v3.4.0
export NCS_ROOT=/path/to/ncs/v3.4.0                              # only if installed elsewhere

git clone --recurse-submodules https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF9151 t-display-k230-nrf9151
cd t-display-k230-nrf9151
./build_serial_modem.sh
# build/serial_modem_k230/zephyr/tfm_merged.hex
```

If the output layout moves:

```sh
find build/serial_modem_k230 -path '*/zephyr/tfm_merged.hex' \
  -o -path '*/zephyr/zephyr.hex' -o -path '*/zephyr/zephyr.elf'
```

Two profiles: `serial_modem_k230/` (**recommended**, Nordic Serial LTE Modem adapted) and
`at_client_k230/` (bring-up only). The Serial LTE Modem source is a **pinned submodule**,
`third_party/ncs-serial-modem` at `13c80da97fe4d55ecb5a9745834d97be22821307`, with five ordered
LilyGO patches (`0001` GNSS NMEA URC + LED, `0002` optional XDFU, `0003` UART diag, `0004` GNSS
NMEA URC worker, `0005` LED AT control).

⚠ **`tfm_merged.hex` does not update the modem firmware.** The cellular modem package
`mfw_nrf91x1_*.zip` is a separate signed image with its own update procedure.

Programming: SWD (the repository ships `images/swd.png`, 3.1 MB, and an
`images/nRF-ConnectProgrammer.mp4` walkthrough, 2.1 MB).

---

## 6. Debug and diagnostics on the running board

| Tool | Where |
|---|---|
| **I²C scanner** | Launcher → I2C Scan. Async, multi-bus since v0.2.4. |
| **Display test** | `ui_display_test.c` |
| **HDMI test** | `ui_hdmi_test.c` |
| **I²S test** | `ui_i2s_test.c` |
| **Multitouch test** | `ui_multitouch.c` |
| **Mic spectrum** | `ui_mic_spectrum.c` |
| **DRM motion probe** | `drm_motion_probe.c` (34 KB) |
| **LVGL scroll probe** | `lvgl_scroll_probe.c` |
| **LoRa FLRC bench** | `lora_flrc_bench.cpp` |
| **CoreMark / CoreMark-PRO** | Built into the image (`BR2_PACKAGE_COREMARK`, `_PRO`) |
| **evtest** | Built in — the right tool for the TCA8418 keyboard and PMU power key |
| **`linux-tools-gpio`** | Built in (`BR2_PACKAGE_LINUX_TOOLS_GPIO`) — `gpioinfo`, `gpioget`, `gpioset` |
| **Terminal app** | In the launcher, so you have a shell without SSH |
| **MTP / ADB** | `S41adb_mtp` init script |

---

## 7. Alternative software stacks

| Stack | Applicability to *this board* |
|---|---|
| `kendryte/k230_sdk` (dual-OS) | Builds for CanMV/EVB targets. **No T-Display K230 board profile.** Porting means recreating LilyGO's overlay against a different SDK. |
| **CanMV / MicroPython** (`kendryte/canmv_k230`) | Runs on K230. **No T-Display K230 board support.** Display, touch and keyboard would all need porting. |
| **MaixPy** (`sipeed/MaixPy`) | Same situation. |
| **oreboot** | Has K230 support. Boots Linux from mask ROM over USB. **The most interesting recovery lever available** — see [`factory-firmware.md`](factory-firmware.md). |
| **k230-debian** (`intx82/k230-debian`) | Debian rootfs experiment, kernel 6.6 branch, last touched 2024-12. Not board-specific. |
| **RT-Thread / RT-Smart** | The CPU1 OS in the dual-OS SDK; not used by this board's Linux-only image. |
| **Zephyr** | **No K230 support upstream.** |

See [`projects-and-community.md`](projects-and-community.md) for licences, commits and status.

---

## 8. Known build and bring-up risks

1. **Cloning without submodules** → empty SDK, immediate failure.
2. **Building on native Windows or under `/mnt/c/`** → permission and symlink corruption. LilyGO
   warns explicitly.
3. **`/opt/toolchain` hard-coded** → breaks on any non-FHS host.
4. **Buildroot downloads during the build** → no offline or hermetic build without pre-seeding `dl/`.
5. **Wrong boot medium** → the documented bricking path. See [`factory-firmware.md`](factory-firmware.md).
6. **IO bank voltage** → Canaan's own DTS says a wrong setting *will damage the chip*.
7. **nncase version mismatch** → runtime failure, not build failure. Canaan publishes a
   correspondence table; use it.
8. **DTR not asserted** on the nRF52840 USB serial → silent console.
