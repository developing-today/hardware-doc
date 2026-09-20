# T-Display K230 — images, flashing and recovery

**Evidence status: `reported-working` / `inferred`. Nothing here was executed.** The recovery
section in particular is assembled from primary documents and one community report, and is
labelled per claim.

---

## 1. There is no factory firmware binary

LilyGO publishes **no prebuilt image** for the T-Display K230. The repository states plainly:

> "Generated image files under `k230_bsp/images/` are local build artifacts."

The supported path is: build `sysimage-sdcard.img` yourself ([`development.md`](development.md)),
or take a **Canaan** prebuilt image from `developer.canaan-creative.com` → *K230* → *Images* —
which will boot a generic K230 Linux but will not drive this board's AMOLED, touch, keyboard or
radio, because all of that is in LilyGO's overlay.

This is a real gap. A user who bricks a board cannot download a known-good image; they must be
able to build one. Combined with the 17-month gap between the board going on sale and the BSP
being published, it explains the early-owner experience described in
[`community.md`](community.md).

## 2. Image format and layout

| Property | Value |
|---|---|
| Artifact | `k230_bsp/images/sysimage-sdcard.img` |
| Type | Whole-disk image, written with `dd` |
| Generator | Buildroot `genimage` — config at `board/canaan/k230-soc/genimage.cfg` (1 280 bytes) |
| Post-image script | `board/canaan/k230-soc/post-image.sh` (9 836 bytes) |
| Post-build script | `board/canaan/k230-soc/post-build.sh` (4 257 bytes) |
| Filesystems | Linux partitions plus a small FAT-ish region — Windows offers to format one after writing; **cancel that prompt** |
| Boot medium | **microSD**, MMC1 on `GPIO54`–`GPIO59` |
| Expansion | BSP v0.2.4 added "storage expansion settings for SD cards larger than the flashed image" — before that, a 64 GB card gave you the image's size and no more |

Exact partition offsets were not extracted, because the image is not published and could not be
built. Read `genimage.cfg` at the pinned commit for the authoritative layout.

## 3. Companion-MCU firmware — the only prebuilt binaries LilyGO ships

Both live in the companion repositories, not in the board repository.

| Artifact | Repo / commit | Bytes | Target | Role |
|---|---|---:|---|---|
| `bootloader/k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex` | `T-Display-K230-nRF52840` @ `4646a728580739d487126f47a521e9b8032b3c2c` | 525 680 | **nRF52840** | Bootloader with **UART DFU @ 115200** and **SoftDevice S140 6.1.1** |
| `firmware/k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2` | same | 296 960 | **nRF52840** | AT/BLE-Central application, build date **2026-08-16**, revision **r4**, UF2 family `0xADA52840` |

Neither has a published SHA-256 from LilyGO. Both are reacquirable from the pinned commit:
`https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840/raw/4646a728580739d487126f47a521e9b8032b3c2c/<path>`.
Full provenance in [`acquisition/manifest.json`](acquisition/manifest.json).

nRF9151 firmware is **source-only** — build `tfm_merged.hex` yourself. Note that it contains
TF-M plus the non-secure application and **does not update the modem firmware package**
(`mfw_nrf91x1_*.zip`), which is a separate signed image.

## 4. Flashing

See [`development.md` §3](development.md#3-flashing-the-sd-card). Summary: `dd` on Linux/macOS,
**Rufus in DD Image mode** on Windows.

## 5. Recovery — what is known and what is not

### 5.1 The failure that is actually reported

r/LilyGO, **2026-08-21 and 2026-08-28**, u/phirzcolru, **firsthand ownership**:

> "extensive attempts to work with this device. i managed to get an mp3 player and notepad
> working for it. but once i attempted to turn on the 'fun' features it bricked it. its not
> quite user friendly."

> "my board is **still unresponsive to boot pin and term**. I think I **flashed it into mmc mode
> vs sd card** and it's stuck."

LilyGO's reply pointed at the GitHub repository and the wiki. **Neither contains a recovery
procedure.** The user did not report recovering.

### 5.2 What the silicon offers — `inferred` from primary documents

The K230 boot ROM supports **USB boot**, and this is the lever that should exist:

| Route | Source | Status |
|---|---|---|
| **Canaan `k230_burntool`** | `K230_SDK_Burntool_User_Guide.md` in `kendryte/k230_docs` | Canaan's own flashing/recovery utility. **Not tested here.** Guide not retrieved in this pass. |
| **oreboot + `kendryte_boot`** | oreboot maintainer u/CyReVolt, r/LilyGO 2025-03-26: oreboot supports K230 and "can **boot Linux from mask ROM over USB in 3 seconds**"; `kendryte_boot` is on GitHub | **Demonstrable project**, stated by its author, with a video demo. The most promising documented path back into a board whose SD boot is broken. |
| **BOOT0/BOOT1 straps** | `IO0` = BOOT0, `IO1` = BOOT1 in the Canaan reference DTS; the pin map documents the BOOT0 **button** on `GPIO0`, idle high / pressed low | The strap pins exist and the button is on one of them. **How the strap combinations map to boot media is not documented by either vendor**, which is precisely why the reported failure was unrecoverable for that user. |

### 5.3 Honest statement of the gap

**There is no vendor-documented recovery procedure for this board.** Not in LilyGO's README, not
in the wiki, not in the BSP, not in the Quick Start. The recommended action for anyone about to
change boot configuration is:

1. Read `K230_SDK_Burntool_User_Guide.md` **before** you need it.
2. Have `kendryte_boot` and the oreboot K230 target built and tested **before** you need them.
3. Keep a known-good SD image.

Marked `not-tested`. Anyone who executes one of these successfully should replace this section
with an `executed-success` procedure.

## 6. Bricking risks, ranked

| Risk | Severity | Notes |
|---|---|---|
| Changing boot medium (SD ↔ eMMC/MMC mode) | **High** | The one confirmed brick |
| Wrong IO bank voltage in a custom device tree | **High — physical damage** | Canaan: "will damage the chip" |
| Interrupting an nRF52840 UART DFU | Medium | UART DFU bootloader should survive; USB/UF2 DFU is the fallback |
| Writing a mismatched U-Boot | Medium | Boot ROM USB path should still exist |
| SD card removal during write | Low | Reflash the card |
| nRF9151 TF-M/modem confusion | Low–Medium | Application flash does not touch modem firmware; SWD recovers |
