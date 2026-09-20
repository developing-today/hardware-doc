# Ethernet — the RJ45

**Question:** *There's an RJ45 on a handheld. How do I use it, and what is behind it?*

| | |
|---|---|
| Interface | `eth0` |
| Physical | RJ45, confirmed present by product photography and community observation |
| Controller | **USB-attached.** Claimed [RTL8152B](../../../../components/realtek/rtl8152b/README.md), 100 Mbps, IEEE 802.3u |
| Speed | **100 Mbit/s** |
| Evidence | `reported-working` for `eth0`; the controller identity is **unresolved** — [`GC-3`](../gaps-and-conflicts.md) |

## Why it is USB

**The K230 has no Ethernet MAC.** A full-text search of Canaan's full and brief datasheets for
`ethernet`, `gmac` and `rmii` on 2026-09-04 returned **zero matches**, and the peripheral list
contains no Ethernet. Anything with an RJ45 on a K230 board is therefore behind a USB Ethernet
controller.

That is a genuine constraint dressed as a feature: 100 Mbit/s ceiling, and it occupies USB
bandwidth shared with the Bluetooth dongle and any USB modem.

## Using it

The launcher's Ethernet page (`ui_ethernet.c`) does DHCP or static, persisted as preferences
`ethernet.mode`, `ethernet.static_ip`, `ethernet.netmask`, `ethernet.gateway`, `ethernet.dns`.
Underneath it is BusyBox:

```sh
ifconfig eth0 up
udhcpc -i eth0 -p /var/run/udhcpc.eth0.pid          # DHCP
# or static:
ifconfig eth0 <ip> netmask <mask>
route del default dev eth0
route add default gw <gw> dev eth0
```

Buildroot's `BR2_SYSTEM_DHCP="eth0"` means DHCP on `eth0` is the boot default.

Status is read from `/sys/class/net/eth0/` — `carrier`, `address` and the operational state.

## The unresolved bit

LilyGO's wiki says **RTL8152B**. LilyGO's shop says **"RC01812"**, which matches no Ethernet
controller naming scheme and is most consistent with an RJ45 jack part number. And the BSP's
kernel fragment enables the USB **CDC/RNDIS/NCM/MBIM/QMI** class drivers but **not**
`CONFIG_USB_RTL8152`, which would be needed for an RTL8152B.

Most likely `CONFIG_USB_RTL8152` is already in the base `k230` defconfig. **Settle it on hardware:**

```sh
readlink /sys/class/net/eth0/device/driver
lsusb
zcat /proc/config.gz | grep -i rtl8152
```

## Realistic uses

The obvious one, from the launch thread: *"I can hot glue this to the back of a starlink dish and
connect ethernet."* Reply: *"That's a bit of a waste of the screen. There are existing boards
with Ethernet for that task."* Both fair. The port makes most sense as a **provisioning and
recovery path** when Wi-Fi is unavailable — which, given SSH-based launcher deployment
(`deploy_launcher.sh <ip>`), is exactly how a developer will use it.

## Limits

| Limit | Value | Class |
|---|---|---|
| Speed | 100 Mbit/s | board |
| MAC | none on SoC | **silicon** |
| PoE | none | board |
| Measured throughput | **none published** | unmeasured |
