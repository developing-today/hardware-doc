# Wi-Fi and Bluetooth

**Question:** *How do I get on Wi-Fi? And why does Bluetooth need a dongle?*

| | |
|---|---|
| Wi-Fi | [Realtek RTL8189FS](../../../../components/realtek/rtl8189fs/README.md), **SDIO**, 802.11 b/g/n 2.4 GHz, `wlan0` |
| Bluetooth | **USB dongle** — CSR8510/8891, BlueZ. **No on-board BT radio.** |
| Alternate Wi-Fi modules built | RTL8723DS, RTL8733BS |
| Evidence | `reported-working` |

## Wi-Fi

`BR2_PACKAGE_RTL8189FS=y` builds Realtek's **out-of-tree** vendor driver. Userspace has
`wpa_supplicant` (with Wi-Fi Display), `wireless_tools` and `udhcpc`. The launcher's Wi-Fi page
handles scan/connect/DHCP; nothing exotic is required.

```sh
ip link set wlan0 up
wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf
udhcpc -i wlan0
```

**2.4 GHz only. 802.11n only.** No 5 GHz, no Wi-Fi 5/6.

**Two Wi-Fi drivers are compiled simultaneously** (`RTL8189FS` *and* `RTL8723DS`). That means the
fitted module is not guaranteed identical across production runs. Check the unit in hand:
`dmesg | grep -i rtl` or `lsmod`.

Out-of-tree vendor drivers break on kernel upgrades. That is normal for this part and is a real
maintenance cost if you plan to move off LilyGO's pinned kernel
(`ruyisdk/linux-xuantie-kernel` @ `7d4e1f444f461dbe3833bd99a4640e7b6c2cd529`).

## Bluetooth — read this before buying

**The K230 has no Bluetooth radio.** The kit specification sheet lists no Bluetooth at all. What
the BSP provides is **USB** Bluetooth:

- `CONFIG_BT=m`, `BT_BREDR`, `BT_LE`, `BT_RFCOMM`, `BT_BNEP`, `BT_HIDP`
- `CONFIG_BT_HCIBTUSB=m` with `_BCM`, `_MTK`, `_RTL` vendor support
- `S40bluetoothd` init script, BlueZ runtime
- **`0056-bluetooth-btusb-force-csr8510-8891-workaround.patch`**
- **`0057-bluetooth-csr8510-8891-hci-init-experimental.patch`**

Both patch names contain the words *workaround* and *experimental*. Treat Bluetooth on this
board as working-with-a-specific-dongle, not as a platform feature.

⚠ **The wiki claims otherwise.** LilyGO's T-Display K230 wiki page states the board has an
ESP32-S3-R8 providing "Bluetooth 5.0 LE". Nothing in the BSP corroborates that — see
[`GC-2`](../gaps-and-conflicts.md). **Do not plan a project around on-board Bluetooth.**

Community, r/meshtastic 2025-07-08: *"Bluetooth seems to be missing — might that be an
impediment…"* / *"You're right. I don't see BT labels on the board, and the K230 page does not
mention Bluetooth."* / *"USB C Bluetooth adaptors are $20, but that seems like a REALLY weird
omission."*

## If you need BLE properly: use the nRF52840

The [nRF52840 base board](nrf52840-ble.md) is the sanctioned BLE path, over UART1 with an AT
protocol. It is a **BLE Central** implementation and it is what the launcher's Meshtastic BLE
support uses. That is a considerably more solid answer than the dongle.

## Wi-Fi HaLow?

The launcher has `ui_halow.c`, `halow_udp_stream.c` and `k230_halow_camera_stream.sh` —
**802.11ah HaLow** support for an external module. No HaLow hardware is listed in any product
specification, so this is presumably for a user-supplied module on the expansion header.
**Unverified.**

## Limits

| Limit | Value | Class |
|---|---|---|
| Wi-Fi bands | 2.4 GHz only | board |
| Wi-Fi standard | 802.11 b/g/n | board |
| Bluetooth | USB dongle only | **silicon** (no radio on K230) |
| BLE via nRF52840 | Central role, AT-mediated | board |
| Antenna | internal; **no external antenna connector** requested by users but not provided | board |
| Measured throughput / range | **none published** | unmeasured |

A user asked at launch: *"I'd really like to see more options to add external antennas for wifi,
lora and gps."* (2025-03-24). No response was recorded.
