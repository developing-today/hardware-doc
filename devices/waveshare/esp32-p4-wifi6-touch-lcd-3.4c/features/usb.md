# How do I use USB? — ESP32-P4-WIFI6-Touch-LCD-3.4C

> Evidence status: **vendor documentation + schematic. Untested on hardware.**
> Applies equally to the [4C](../../esp32-p4-wifi6-touch-lcd-4c/README.md).

## Two USB ports, three roles

| Port | Speed | Role | Behind it |
|---|---|---|---|
| **Type-A** | USB 2.0 **High Speed** | **OTG** — host or device | ESP32-P4 native USB PHY |
| **Type-C** | USB 2.0 **Full Speed** | Power, flashing, debug | **CH343P** USB-UART bridge |

The Type-A port is the interesting one: a genuine HS OTG interface on the P4's own PHY. The Type-C
is the everyday port — power in, firmware out.

Connector `J3` carries `VBUS`, `VBUS_OUT`, `USBD_N`, `USBD_P`, `GND`. The presence of a separate
**`VBUS_OUT`** net is what makes host mode plausible: the board can supply bus power outward rather
than only consuming it.

## Device mode — the covered case

`12_usb_extend_screen` turns the board into a **USB external display** for a host computer.

```yaml
dependencies:
  espressif/tinyusb: "0.17.0~2"
  espressif/usb_device_uac: "1.2.0"
```

**Those pins are exact and deliberate.** Waveshare state that `0.17.0~2` is the precise TinyUSB
release `usb_device_uac 1.2.0` permits, and that keeping both exact *"prevents a future TinyUSB
upload from silently changing USB descriptors or P4 PHY behavior."* Do not float them.

The UAC component is gated behind the CMake option `USB_DEVICE_UAC_COMPONENT`. Normal builds leave
it on; the CI vendor-only path disables both it and `CONFIG_UAC_AUDIO_ENABLE`. A CMake option is
used rather than a Kconfig manifest condition because Kconfig conditions need ESP-IDF 6.0 and this
repository also validates against 5.5.

Reference: `examples/esp-idf/12_usb_extend_screen/` in the
[official repository](../official-repo-and-community.md#1-waveshares-official-repository).

## Host mode — advertised, undemonstrated

The board is documented as **USB 2.0 OTG HS** with a Type-A socket, and `VBUS_OUT` exists in the
schematic. But **no shipped example uses host mode**, and no community project was found doing so.

So: the hardware appears capable, ESP-IDF supports USB host on the P4, and nothing here validates
the combination on this board. Unresolved specifics:

- Whether `VBUS_OUT` is switched under software control or always-on when powered
- Available current budget for a bus-powered peripheral
- Whether over-current protection is fitted

**Check these against the schematic before attaching anything that draws real current.**

## Serial, flashing and a genuine trap

The Type-C port presents through a **CH343P**. On Linux it usually enumerates with no driver work;
on macOS a WCH driver is generally needed — see the
[USB-UART bridge record](../../../../components/wch/ch340x/README.md).

```bash
idf.py -p /dev/ttyACM0 flash monitor      # port name varies
```

> **⚠️ Arduino does not use the CH343P.** For the tested Arduino FQBN, sketch `Serial` is
> **Hardware CDC on the Type-C USB port**, not the CH343P UART. Start the sketch with the monitor
> closed or disconnected; missing startup lines are expected because the non-blocking logger drops
> them.
>
> This costs people an afternoon: the same physical connector serves two different endpoints
> depending on framework.

Waveshare also document Espressif's Windows **Flash Download Tool**.

## Not a third USB port: the C6 header

Flashing the ESP32-C6 radio uses **`J4`**, an SH1.0 4-pin UART header — `C6_U0TXD`, `C6_U0RXD`,
`GND`, `C6_IO9` (the boot strap). It is not USB and is not reachable from either USB port. See
[development.md](../development.md).

## Resource conflicts

| Resource | Shared with | Note |
|---|---|---|
| Type-A HS OTG | — | Dedicated P4 USB PHY |
| Type-C FS | CH343P | Power + serial |
| `USB1P1_N/P` on header `J8` pins 15/16 | **The 40-pin header** | A USB pair is also brought out there — see [expansion-header.md](./expansion-header.md) |
| PSRAM bandwidth | Display, camera | USB display streaming competes with the DSI path |

`12_usb_extend_screen` drives the display *from* USB, so it exercises USB and DSI together — the
one combination with an official example.

## Limits

| Limit | Value | Kind |
|---|---|---|
| Type-A | USB 2.0 High Speed, OTG | Silicon + board |
| Type-C | USB 2.0 Full Speed | Board |
| Throughput | **Unknown — not measured** | — |
| Host-mode current budget | **Unknown** | — |

## Pitfalls

1. **Arduino `Serial` is USB CDC, not the CH343P.** Most likely time-waster here.
2. **Floating TinyUSB versions.** Waveshare pin `0.17.0~2` for a stated reason.
3. **Assuming host mode works.** Advertised, not demonstrated.
4. **Expecting the C6 over USB.** It is on a separate UART header.
5. **macOS without the WCH driver** — the port simply will not appear.

## Open questions

- Is host mode functional on this board, and what is the `VBUS_OUT` current budget?
- Is `VBUS_OUT` software-switched?
- Is over-current protection fitted?
- What is the relationship between `USB1P1_N/P` on `J8` and the Type-A port — same controller or a
  second interface?

## Related

- [Expansion header](./expansion-header.md) — also carries a USB pair
- [Development and flashing](../development.md) · [Full pinout](../pinouts-and-buses.md)
- [USB-UART bridge component](../../../../components/wch/ch340x/README.md)
