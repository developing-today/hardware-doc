# microSD — storage and the boot medium

**Question:** *How do I use the SD card, and why does it matter more than usual?*

| | |
|---|---|
| Controller | K230 **MMC1** |
| Pins | CMD `GPIO54`, CLK `GPIO55`, D0–D3 `GPIO56`–`GPIO59` |
| Role | **Boot medium *and* main storage** |
| SoC capability | SD 3.01 / eMMC 5.0, 4- or 8-bit, HS200/HS400 | 
| Component | [generic/micro-sd-sdmmc](../../../../components/generic/micro-sd-sdmmc/README.md) |
| Evidence | `reported-working` |

## The card is the system

There is no on-board storage the system boots from — **the whole Linux image lives on the SD
card**. That has two consequences most boards do not have:

1. **Card quality is system reliability.** A flaky card is a flaky computer, not a flaky data
   store.
2. **Removing the card while running is not a hot-unplug, it is pulling the root filesystem.**

## Writing an image

See [`development.md` §3](../development.md#3-flashing-the-sd-card). `dd` on Linux/macOS,
**Rufus in DD Image mode** on Windows. After writing on Windows, decline the "format this
partition" prompt.

## Using the spare space

Before BSP **v0.2.4** the image occupied its declared size and the rest of a large card was
simply unused. v0.2.4 "added storage expansion settings for SD cards larger than the flashed
image" — `k230_storage_expand.sh` in the launcher, exposed in Settings.

`resize2fs` and `parted` are both in the image (`BR2_PACKAGE_E2FSPROGS_RESIZE2FS`,
`BR2_PACKAGE_PARTED`), as are `dosfstools` with `mkfs.fat` and `fsck.fat`.

## Getting files on and off

| Route | Notes |
|---|---|
| **MTP over USB** | `S41adb_mtp` init script; launcher has an MTP page with its own layout work in v0.2.3/v0.2.4 |
| **USB mass storage gadget** | `k230-usb-storage-gadget` + `/etc/default/k230_usb_storage`; `USB_CONFIGFS_MASS_STORAGE=y` |
| **SSH / scp** | Once networked. `deploy_launcher.sh` uses it. |
| Card reader | Offline. |

User content LilyGO deliberately does **not** ship: **NES ROMs**, **offline map tiles**, media.
Copy them to the card yourself.

## Limits

| Limit | Value | Class |
|---|---|---|
| Bus | 4-bit as wired | board |
| SoC max mode | SD 3.01 | silicon |
| Card size | expandable since v0.2.4 | framework |
| Measured throughput | **none published** | unmeasured |
| Hot-swap | not supported — it is the rootfs | board |

## Pitfalls

1. **Changing boot medium is the documented bricking path.** See
   [`factory-firmware.md`](../factory-firmware.md).
2. Formatting the "unknown partition" Windows offers to format destroys the boot partition.
3. Cheap cards. This is the rootfs.
