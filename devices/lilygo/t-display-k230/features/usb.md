# USB — host, gadget, MTP, mass storage

**Question:** *What can I plug in, and how do I make the board appear as a device?*

| | |
|---|---|
| SoC | [K230](../../../../components/canaan/k230/README.md) — **2 × USB 2.0 OTG** |
| Connectors | USB-C for power; USB-C for OTG (product page: "1 × Power + 1 × USB 2.0 OTG (Type-C)") |
| Charging | 5 V, **500 mA** |
| Evidence | `reported-working` |

## Host side — three devices the BSP expects

| Device | Kernel support built | Why |
|---|---|---|
| **USB Ethernet** | `USB_USBNET`, `CDCETHER`, `CDC_NCM`, `RNDIS_HOST`, `CDC_SUBSET` | the RJ45 ([ethernet.md](ethernet.md)) |
| **USB Bluetooth** | `BT_HCIBTUSB` + `_BCM`/`_MTK`/`_RTL`, CSR8510 patches | the only Bluetooth ([wifi-and-bluetooth.md](wifi-and-bluetooth.md)) |
| **USB cellular modem** | `CDC_MBIM`, `QMI_WWAN`, `USB_WDM`, `USB_SERIAL_WWAN`, `USB_SERIAL_OPTION`, `PPP*` | an alternative to the nRF9151 base |

`USB_ACM` and `USB_SERIAL` are also on, so ordinary USB serial adapters work. Canaan publishes
`K230_4G_Module_Linux_Porting_Reference` for the modem case.

## Gadget side

`CONFIG_USB_CONFIGFS=m` with `F_FS`, **`MASS_STORAGE`**, **`RNDIS`** and **`ACM`** functions. The
rootfs overlay ships `/usr/sbin/k230-usb-storage-gadget` (5 601 bytes) and
`/etc/default/k230_usb_storage` (303 bytes), and `S41adb_mtp` starts ADB/MTP.

So the board can present itself to a PC as:

- a **mass-storage device** (expose the SD card)
- an **MTP device** (file transfer without unmounting)
- an **RNDIS network device** (USB networking to the host)
- a **serial device** (ACM console)

## Alternatives decision table

| Goal | Route |
|---|---|
| Copy media to the board, board still running | **MTP** |
| Expose the card wholesale to a PC | **mass storage gadget** |
| Network to a host with no Wi-Fi or Ethernet | **RNDIS gadget** |
| Console when the display is dead | **ACM gadget**, or UART0 |
| Add Bluetooth | USB dongle (host) |
| Add cellular without the keyboard base | USB modem (host) |

## Conflicts

Only two USB controllers exist and one is largely the power port. **Host and gadget roles on the
same connector are exclusive**; running the mass-storage gadget while a USB Ethernet dongle is
attached needs the two roles on different controllers. Untested.

## Limits

| Limit | Value | Class |
|---|---|---|
| Controllers | 2 × USB 2.0 OTG | silicon |
| Speed | USB 2.0 High-Speed per the SoC; **not confirmed for this board's ports** | silicon / unverified |
| Charge current | 5 V 500 mA | board |
| Measured throughput | **none published** | unmeasured |

## Pitfalls

1. **500 mA is a modest budget.** A 1.6 GHz SoC, an AMOLED and a charging cell on 2.5 W is tight.
   The launch thread's top comment was "Plug in that device! It's thirsty!" about the battery
   indicator in LilyGO's own promotional photo.
2. Enabling multiple gadget functions and a host role at once will contend.
3. USB Bluetooth is a **workaround-patched, experimental** path.
