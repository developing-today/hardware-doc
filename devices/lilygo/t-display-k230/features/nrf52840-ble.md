# BLE via the nRF52840 companion

**Question:** *How do I do Bluetooth Low Energy on a board whose SoC has no Bluetooth?*

| | |
|---|---|
| Companion | [Nordic nRF52840](../../../../components/nordic-semiconductor/nrf52840/README.md) |
| Where | **nRF52840 BLE / audio / sensor base board** (optional expansion) |
| Link | K230 **UART1** — `GPIO3` TX → `P0.11`, `GPIO4` RX ← `P0.12` |
| Device | `/dev/ttyS1`, **115200 8N1** |
| Protocol | LilyGO **AT command set** |
| Role | **BLE Central** |
| Evidence | `reported-working` |

## Why this exists

The K230 has **no Bluetooth radio**. The alternatives are a USB dongle (workaround-patched,
experimental — [wifi-and-bluetooth.md](wifi-and-bluetooth.md)) or this. This is the better one.

## AT interface

```
AT                 → OK
AT+VER?
AT+MESHSTATUS?
AT+SCAN=5          scan for 5 s
AT+LIST?           cached results
AT+CONN=0          connect to index 0
AT+GATTS?          discover services
AT+DISC            disconnect
```

Plus characteristic read / write / subscribe / unsubscribe. Every command returns `OK` or
`ERR:<reason>`. Asynchronous events arrive as URCs:

```
+SCAN:<index>,<addr>,<rssi>,<ble_uart_advertised>,<name>
+SCAN:DONE,<count>
+CONNECTED:<handle>
+DISCONNECTED:<handle>,<reason_hex>
+BOOT:K230_NRF52840_AT
+MESH:ADV,1
```

Full reference: `docs/AT_COMMANDS.md` in `Xinyuan-LilyGO/T-Display-K230-nRF52840`.

> **The complete command set has now been recovered from the shipped binary**, independently of
> that document — all 37 `+HELP:` strings, verbatim, including the six Meshtastic commands and
> the `AT+PHY=<AUTO|1M|2M|CODED>` long-range option not listed above. See
> **[`../artifacts/firmware/nrf52840-coprocessor-firmware.md` §3](../artifacts/firmware/nrf52840-coprocessor-firmware.md#3-the-at-command-set)**.
> Extraction status `executed-success`; the *behaviour* of each command remains `not-tested`.
>
> That document also carries the bootloader's flash map, UICR words, SoftDevice identity
> (S140 v6.1.1 read from the info structure, not the filename) and the UF2 target address —
> i.e. what you need to unbrick the companion board.

## Talking to it

From the K230, open `/dev/ttyS1` at 115200 8N1 and write AT lines. The launcher's BLE page
(`ui_ble.c`) does exactly this. Enabled by
`0060-riscv-dts-rm69a10-enable-uart1-nrf52840.patch`.

From a PC, connect to the nRF52840's own USB-C for a debug log at 115200. ⚠ **Some serial
monitors need DTR asserted** or the port stays silent — LilyGO says so explicitly.

## Updating the firmware

Two paths, and the second one is the interesting one.

**USB / UF2** — the developer path. Jumper `RST` to `GND` twice quickly (or touch the USB-C
shell), the Adafruit bootloader enumerates a drive, drag the `.uf2`. Family ID `0xADA52840`.
Build with PlatformIO (`nrf52840_dk_adafruit`, Arduino framework), convert with
`scripts/uf2conv.py`.

**UART DFU from the K230** — the field path. A custom bootloader
(`k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex`, SoftDevice **S140 6.1.1**) plus
`tools/k230_nrf52840_dfu.cpp` (33 370 bytes) and the launcher's `ui_nrf52840_dfu.c` let the
handheld reflash its own BLE controller with no PC attached. That is a genuinely well-thought-out
piece of product design and it is not common at this price.

**Ownership arbitration:** BSP v0.2.2 "improved nRF52840 ownership coordination between
Meshtastic BLE and UART DFU". Both want `/dev/ttyS1`; only the launcher arbitrates.

## It also controls power

`P0.04` (Arduino pin 4) is the **external 5 V boost enable** for the 21700 battery compartment,
supplying the main unit. So the nRF52840 is not only a radio peripheral, it is in the power path.
See [battery-and-power.md](battery-and-power.md).

## Limits

| Limit | Value | Class |
|---|---|---|
| Role | **Central** as shipped | firmware |
| Link rate | 115200 8N1 — caps GATT throughput | board/firmware |
| Peripheral role, mesh, Thread, Zigbee | silicon-capable, **not in the shipped firmware** | firmware |
| Requires | the nRF52840 base board (separate purchase) | board |
| Measured BLE range / throughput | **none published** | unmeasured |

## Pitfalls

1. The base board is optional. A bare `K256` has no nRF52840.
2. 115200 is the bottleneck for anything data-heavy over GATT.
3. Interrupting UART DFU — the UF2 path is the fallback.
4. Reflashing the nRF52840 while it holds the 5 V boost enable.
