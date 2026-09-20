# T-Display K230 — gaps and conflicts

Open items as of **2026-09-04**. Each states the conflict, both sides with sources, and **what
evidence would settle it**. None is resolved by preference.

---

## `GC-1` — Which K230 core runs Linux

| Source | Claim |
|---|---|
| **Canaan K230 brief datasheet** (primary) | "CPU 1 … 1.6 GHz … **runs RTOS system**"; "CPU 0 … 800 MHz … **runs LINUX system**" |
| **LilyGO wiki**, T-Display K230 Quick Start FAQ | "the dual-core architecture — **big core runs Linux, little core runs RT-Thread** or bare-metal" |

**Assessment.** Canaan's document is primary and matches the SDK's own configuration naming.
LilyGO's FAQ is wrong. Separately, this board's shipped image is built from
`kendryte/k230_linux_sdk`, which is **Linux-only**, so in the default configuration CPU1 is not
running RT-Smart at all.

**Settles it:** `cat /proc/cpuinfo` and `dmesg | grep -i 'cpu\|hart'` on a running unit.

---

## `GC-2` — The claimed ESP32-S3-R8 co-processor  ⚠ most consequential

| Source | Claim |
|---|---|
| **LilyGO wiki**, T-Display K230 page | Board is "combined with **ESP32-S3-R8** (16 MB Flash, 8 MB PSRAM) for Wi-Fi/Bluetooth connectivity"; lists "Bluetooth 5.0 LE (ESP32-S3)"; gives PlatformIO and Arduino build instructions for "the ESP32-S3 co-processor" |
| **LilyGO shop**, T-Display K230 Kit | "Wi-Fi Module \| 2.4G, Name: **RTL8189**, IEEE 802.11 b/g/n 2.4GHz". No Bluetooth row at all. |
| **LilyGO BSP** at `bb831ab…` | `BR2_PACKAGE_RTL8189FS=y`. Bluetooth via `BT_HCIBTUSB` + two **CSR8510/8891 USB dongle** patches. A regex sweep for every Espressif identifier across the whole repository returns **zero matches**. |
| **LilyGO wiki**, Cased Version page | "Supports 2.4GHz Wi-Fi, BLE" — **names no chip** |
| **Community**, r/meshtastic 2025-07-08 | "I don't see BT labels on the board, and the K230 page does not mention Bluetooth" |

**Assessment.** The BSP is the strongest evidence and it is unambiguous: SDIO Realtek Wi-Fi, USB
Bluetooth, no Espressif part. The wiki paragraph reads like copy-paste from a sibling T-Display
product. But the wiki is a *primary vendor source*, and a later hardware revision adding an
ESP32-S3 cannot be excluded — one owner wrote on 2026-08-28 "now that you have the keyboard and
**the esp** I might purchase again", which may reflect a newer variant or may reflect the wiki.

**Deliberate consequence:** the existing
[`components/espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) record
has **not** been given a Used-By entry for this board.

**Settles it:** `lsusb`, `dmesg | grep -i blue`, `ls /sys/class/net`, or a photograph of the PCB.

---

## `GC-3` — What drives the RJ45

| Source | Claim |
|---|---|
| **LilyGO wiki** (both pages) | "**RTL8152B** 100 Mbps Ethernet (IEEE 802.3u)" |
| **LilyGO shop**, Kit | "Ethernet Module \| Name: **RC01812** \| Connector: RJ45" |
| **Canaan K230 datasheet** | **No Ethernet MAC.** Full-text search for `ethernet`, `gmac`, `rmii` across the full and brief datasheets: **zero matches.** |
| **LilyGO BSP** `linux.fragment` | Enables `USB_USBNET`, `CDCETHER`, `CDC_NCM`, `CDC_MBIM`, `RNDIS_HOST`, `QMI_WWAN`, `CDC_SUBSET`. **Does not enable `CONFIG_USB_RTL8152`.** |
| **Launcher** | Manages `eth0` with `ifconfig`/`udhcpc`; driver-agnostic |

**Assessment.** The RJ45 is definitely USB-attached, because the SoC has no MAC. `RC01812`
matches no known Ethernet controller and is most consistent with an **RJ45 jack with magnetics**
part number — an interpretation, not a finding. `CONFIG_USB_RTL8152` is probably already set in
the base `k230` kernel defconfig, which the fragment only extends.

**Settles it:** `readlink /sys/class/net/eth0/device/driver` and `lsusb` on a running unit; or
`zcat /proc/config.gz | grep RTL8152`.

---

## `GC-4` — Is the LT9611 HDMI bridge actually fitted?

Software support is extensive (dedicated device tree, two patches, a launcher test page, 29
source references, and a headline "HDMI 1080P @ 30 FPS" on the wiki), but LilyGO calls the path
"optional" in every pin-map row and "a diagnostic feature" in the README, and **never names the
part in either shop listing**.

**Settles it:** `i2cdetect` on the touch bus for a second address, or a PCB photograph.

---

## `GC-5` — No schematic exists publicly

LilyGO's wiki page has a `#schematic` heading with **no link or file beneath it** (verified
2026-09-04). Same for `#dimension-diagram` on the bare-board page. This is a *soft* gap: no 404,
no broken link, nothing for a link checker to catch.

Consequence: the pin map is **unverifiable**, and the PMIC, speaker amplifier and microphone
remain unidentified. Every pin claim in
[`pinouts-and-buses.md`](pinouts-and-buses.md) rests on a single vendor document.

**Settles it:** LilyGO publishing one, or a competent teardown with high-resolution PCB
photographs. Neither existed on 2026-09-04.

---

## `GC-6` — GC2093 sensor parameters undocumented

The vendor V4L2 driver (`vvcam/src/gc2093.c`, 26 213 bytes) contains the full register
initialisation but **no GalaxyCore datasheet is publicly available**, so the writes were not
decoded. Pixel size, optical format, lane count, link rate, exposure and HDR/WDR limits are all
unknown.

**Settles it:** a GC2093 datasheet, or decoding the driver against a sibling GalaxyCore part.
The skill's vendor-driver-audit step was **not performed for this sensor**, and that is recorded
here rather than silently skipped.

---

## `GC-7` — 512 MB versus 1 GB in the device tree

The product specification says **8 Gb = 1 GB LPDDR4**. The Canaan U-Boot reference DTS the BSP
overlays (`k230_canmv_v3.dts`) declares `memory@0 … <0x0 0 0x0 0x20000000>` = **512 MB**.

**Assessment.** Almost certainly the upstream CanMV-v3 baseline that LilyGO's overlay replaces
or that the boot loader corrects at runtime; the K230 SDK also splits DRAM between OSes in
dual-OS configurations. **Not verified.**

**Settles it:** `free -h` or `cat /proc/meminfo` on a running unit.

---

## `GC-8` — ADC characteristics unknown

`ADC0`, `ADC1`, `ADC2` are exposed on the 40-pin header. The K230 brief datasheet's peripheral
list does **not** enumerate an ADC. Resolution, reference voltage, sample rate and input range
are all unknown.

**Settles it:** the Canaan `K230_Big_Core_Low_Speed_Driver_API_Reference` (retrieved but not yet
mined) or the missing pinout document.

---

## `GC-9` — 16 MB flash, purpose unclear

LilyGO's wiki lists "Flash 16 MB" and "1 GB LPDDR4, **16 MB Flash**, TF card slot". The BSP boots
from **SD**. The K230 supports SPI NOR and SPI NAND boot. Whether the 16 MB part is a boot NOR,
storage for the (claimed) ESP32-S3, or a wiki error tied to `GC-2` is unresolved.

**Settles it:** `cat /proc/mtd`, `dmesg | grep -i spi-nor`, or a PCB photograph.

---

## Negative results confirmed in this pass

Recorded so they are not re-investigated:

- **The K230 has no Ethernet MAC.** Searched both datasheets for `ethernet`/`gmac`/`rmii` on
  2026-09-04: zero matches.
- **The K230 has no third CPU core.** The datasheet feature list contains exactly two CPU
  subsystems. The PMU is fixed-function.
- **Canaan publishes no K230 errata.** Full recursive listing of `kendryte/k230_docs` at
  `f8e3021…`: no errata document in either language tree.
- **`K230_PINOUT_V1.0_20230524` is cited by the datasheet but is not published.** Same listing.
- **No LilyGO schematic for this board exists.** Wiki heading present, content absent.
- **Zephyr has no K230 support upstream** as of 2026-09-04.
- **No clone of this board was found** on any marketplace searched.
- **No independent benchmark of this board exists** in any source searched.
- **Canaan's `en/` documentation tree contains no binary hardware artifacts; the `zh/` tree
  does.** This is a *correction* to the natural assumption, verified by full tree listing.
