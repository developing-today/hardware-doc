# Realtek RTL8189FS — 802.11b/g/n 2.4 GHz SDIO Wi-Fi

- **Category:** single-band 2.4 GHz Wi-Fi 4 (802.11 b/g/n) SoC, **SDIO** host interface
- **Manufacturer:** Realtek Semiconductor
- **Research status:** identified from the vendor BSP and the vendor product listing; no Realtek datasheet is publicly distributed for this part (Realtek does not publish 8189 datasheets openly).
- **Retrieved:** 2026-09-04

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Part | **RTL8189FS** (SDIO variant of the RTL8189F) | S1 |
| Standard | 802.11 **b/g/n**, 2.4 GHz only | S2 |
| Host interface | **SDIO** | S1 |
| Bluetooth | **none** — the 8189 family is Wi-Fi only | S1 (see below) |
| Buildroot package | `BR2_PACKAGE_RTL8189FS=y` | S3 |
| Linux interface name | `wlan0` | S4 |

## 2. The Bluetooth trap on this family

The BSP also builds **RTL8723DS** (`BR2_PACKAGE_RTL8723DS=y`, `BR2_PACKAGE_RTL8723DS_BT=y`)
and **RTL8733BS**, so an unwary reader concludes the board has combo Wi-Fi+BT. LilyGO's own
pin map states the constraint plainly:

> "RTL8189FS or RTL8723DS Wi-Fi. **RTL8723DS Bluetooth requires separate BT UART hardware
> signals; SDIO covers Wi-Fi only.**" — S1

And the board's Bluetooth is in fact **USB**: the kernel fragment enables `BT_HCIBTUSB` with
`BT_HCIBTUSB_RTL`, and two downstream patches exist specifically for a **CSR8510/8891 USB
dongle** (`0056-bluetooth-btusb-force-csr8510-8891-workaround.patch`,
`0057-bluetooth-csr8510-8891-hci-init-experimental.patch`). Both are labelled *workaround* and
*experimental* by their own filenames.

Two Wi-Fi module options being compiled simultaneously is itself a finding: it means the
fitted module is **not guaranteed identical across production runs**. Verify by
`lsmod` / `dmesg` on the unit in hand rather than assuming.

## 3. Practical notes

- Out-of-tree driver. `RTL8189FS` is a Realtek vendor driver built by Buildroot, not a mainline
  `rtlwifi`/`rtw88` driver. Kernel upgrades break it routinely; that is the normal experience
  with this part.
- 2.4 GHz only, 802.11n only. No 5 GHz, no Wi-Fi 5/6.
- A community owner comparing to another LilyGO handheld said "If the WiFi is any better than
  the t-deck plus I might end up with one" (S5) — an expectation, not a measurement. **No
  throughput or sensitivity measurement for this board exists in any source found.**

## 4. Used By

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

The board's only Wi-Fi. Attached over **SDIO** (the K230's second SD/MMC controller; the first
carries the boot microSD on `GPIO54–59`). Enumerates as `wlan0`. LilyGO's kit specification
sheet calls it "Wi-Fi Module 2.4G, Name: **RTL8189**, IEEE 802.11 b/g/n 2.4 GHz", which matches.

⚠ LilyGO's **wiki** page for the same product instead claims an **ESP32-S3-R8 co-processor**
provides "Wi-Fi + Bluetooth 5.0". Nothing in the BSP, the device trees, the Buildroot config or
the launcher source references an ESP32 of any kind. Recorded as conflict `GC-2` in
[gaps-and-conflicts.md](../../../devices/lilygo/t-display-k230/gaps-and-conflicts.md).

## 5. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` and `README.MD` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/tree/bb831ab358b66f5bd9a87ecd7c580fee4537492e` | 2026-09-04 | "RTL8189FS SDIO Wi-Fi"; SDIO covers Wi-Fi only |
| S2 | T-Display K230 Kit product page | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230-kit` | 2026-09-04 | "RTL8189, IEEE 802.11 b/g/n 2.4GHz" |
| S3 | `k230_canmv_t_display_rm69a10_defconfig` | LILYGO | primary | source | same repo | 2026-09-04 | `BR2_PACKAGE_RTL8189FS/RTL8723DS/RTL8723DS_BT` |
| S4 | `k230_launcher/k230_phone_ui/src/ui_common.h` | LILYGO | primary | source | same repo | 2026-09-04 | `NET_WIFI_IFACE "wlan0"` |
| S5 | r/LilyGO comment by u/meremale | Reddit | community | forum (opinion) | `https://old.reddit.com/r/LilyGO/comments/1vtcjuj/` | 2026-09-04 | Expectation about Wi-Fi quality vs T-Deck Plus |
