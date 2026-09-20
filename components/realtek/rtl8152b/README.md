# Realtek RTL8152B — USB 2.0 to 10/100 Ethernet controller

- **Category:** USB 2.0 Fast Ethernet MAC + PHY in one package
- **Manufacturer:** Realtek Semiconductor
- **Research status:** identified from LilyGO's wiki specification. **Not corroborated by the BSP kernel fragment** — see §3, which is the whole reason this record exists.
- **Retrieved:** 2026-09-04

## 1. Why an *USB* Ethernet part is on a board with a "gigabit-capable" SoC

It is not. **The Kendryte K230 has no Ethernet MAC at all.** A full-text search of both the K230
full datasheet and the K230 brief datasheet for `ethernet`, `gmac` and `rmii` on 2026-09-04
returned **zero matches**, and neither peripheral list contains Ethernet. Any RJ45 on a K230
board is therefore behind a USB Ethernet controller, and LilyGO's wiki names that controller
as **RTL8152B, 100 Mbps, IEEE 802.3u**.

This is a good example of a specification that reads like a headline feature and is actually a
constraint: the port is limited to 100 Mbit/s and it consumes one of the K230's two USB 2.0 OTG
controllers' bandwidth.

## 2. Known properties

| Property | Value | Evidence |
|---|---|---|
| Part | **RTL8152B** | S1 |
| Rate | **100 Mbps**, IEEE 802.3u | S1 |
| Host attach | USB 2.0 | inferred from part family; RTL8152B is a USB device-side controller |
| Linux driver | `r8152` (`CONFIG_USB_RTL8152`) | see §3 |
| Interface name on the board | `eth0` | S2 |

## 3. The unresolved part — driver evidence does not match

LilyGO's BSP kernel fragment (`linux.fragment`, S3) enables a long list of USB networking
classes — `USB_USBNET`, `CDCETHER`, `CDC_NCM`, `CDC_MBIM`, `RNDIS_HOST`, `QMI_WWAN`,
`CDC_SUBSET` — and **does not enable `CONFIG_USB_RTL8152`**. The launcher's Ethernet page
manages `eth0` with `ifconfig`/`udhcpc` and does not care what drives it.

Three readings, none yet eliminated:

1. `CONFIG_USB_RTL8152` is already set in the base `k230` kernel defconfig, so the fragment has
   nothing to add. **Most likely**, and testable by dumping the built `.config`.
2. The fitted part is not an RTL8152B and the wiki is wrong — the CDC/RNDIS list would then be
   the real driver path.
3. The RJ45 is only ever used with an external USB dongle, and the wiki is describing an
   accessory.

**How to settle it:** on a running board, `readlink /sys/class/net/eth0/device/driver` and
`lsusb`. Until then this record must not be read as confirming a fitted RTL8152B. Tracked as
`GC-3` in [gaps-and-conflicts.md](../../../devices/lilygo/t-display-k230/gaps-and-conflicts.md).

## 4. Used By

### [LilyGO T-Display K230 / Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

Claimed by LilyGO's wiki as the RJ45 Ethernet path on both the bare board and the Cased
Version. The kit's shop listing instead names the Ethernet part **"RC01812"** with an RJ45
connector — a third, unexplained designation that matches no Realtek part number and is most
likely the **RJ45 jack/magnetics** part rather than the controller. Both are recorded; neither
is confirmed.

The RJ45's physical presence *is* confirmed by community observation: "the ethernet port is an
odd choice. It just seems too big for this type of device" (S4, 2025-07-07).

## 5. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | T-Display K230 wiki page and Cased Version page | LILYGO | primary | official wiki | `https://wiki.lilygo.cc/products/t-display-series/t-display-k230/` · `.../cased-version.html` | 2026-09-04 | "RTL8152B 100 Mbps Ethernet (IEEE 802.3u)" |
| S2 | `k230_launcher/k230_phone_ui/src/ui_common.h` | LILYGO | primary | source | `https://github.com/Xinyuan-LilyGO/T-Display-K230` | 2026-09-04 | `NET_ETH_IFACE "eth0"` |
| S3 | `k230_bsp/overlay/buildroot-overlay/linux/linux.fragment` | LILYGO | primary | source | same repo | 2026-09-04 | USB net classes enabled; **no** `USB_RTL8152` |
| S4 | r/meshtastic comment by u/Nobodytoyou_ | Reddit | community | forum (firsthand observation of product photos) | `https://old.reddit.com/r/meshtastic/comments/1ltxxxo/` | 2026-09-04 | RJ45 physically present |
| S5 | K230 full + brief datasheet, searched for `ethernet\|gmac\|rmii` | Canaan | primary | datasheet | `https://github.com/kendryte/k230_docs` @ `f8e3021` | 2026-09-04 | **Negative result:** no Ethernet MAC on the SoC |
