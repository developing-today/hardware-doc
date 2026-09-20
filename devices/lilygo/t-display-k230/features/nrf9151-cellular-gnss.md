# Cellular and GNSS via the nRF9151 companion

**Question:** *How do I get LTE data and a GPS fix?*

| | |
|---|---|
| Companion | [Nordic nRF9151](../../../../components/nordic-semiconductor/nrf9151/README.md) — LTE-M / NB-IoT / DECT NR+ / GNSS SiP |
| Where | **nRF9151 keyboard base board** — kit SKU **`K256-04`** ($113.25). SKU `K256-04-A` ($70.94) is the **same keyboard without it**. |
| Link | K230 **UART3** — `GPIO28` TX → `P0.26`, `GPIO29` RX ← `P0.27` |
| Device | `/dev/ttyS3`, **115200 8N1, no RTS/CTS** |
| Enable | **`GPIO2` high** enables the module |
| Firmware | Nordic **Serial LTE Modem**, NCS **v3.4.0** |
| Evidence | `reported-working` |

## Turning it on

1. Drive **`GPIO2` high**. Nothing works until you do.
2. Open `/dev/ttyS3` at 115200 8N1, no flow control.
3. `AT+CFUN=1` — **required before SIM commands.** LilyGO states this explicitly; `AT+CPIN?`
   before `AT+CFUN=1` fails and looks like a missing SIM.
4. Register, attach, and use the Serial LTE Modem's socket AT commands.

The launcher's Cellular page (`ui_cellular.c`) and manager (`ui_nrf9151_manager.c`) drive all of
this. Enabled by `0061-riscv-dts-rm69a10-enable-uart3-nrf9151.patch`, which also configures
`GPIO2` as the userspace modem-enable pin.

## GNSS

- `AT#XNMEA=1` enables **NMEA URCs** on the AT UART; `AT#XNMEA=0` disables them.
- On a fix, the `P0.23` LED changes to a **1 s cadence with about 300 ms on-time** — a free
  visual fix indicator that needs no software.
- The NMEA URC path is one of LilyGO's five patches on top of Nordic's Serial LTE Modem
  (`0001-k230-gnss-nmea-urc-and-led.patch`, `0004-k230-gnss-nmea-urc-worker.patch`).

## Firmware, and how to rebuild it

Two profiles in `Xinyuan-LilyGO/T-Display-K230-nRF9151` @ `ed4ecbe34162dec9b81213a400198125bbd6e36f`:

| Profile | Use |
|---|---|
| `serial_modem_k230/` | **Recommended.** What the launcher expects. |
| `at_client_k230/` | Minimal AT passthrough, bring-up only. |

Build: see [`development.md` §5](../development.md#5-building-the-nrf9151-firmware). NCS v3.4.0
via `nrfutil sdk-manager`, upstream Serial LTE Modem pinned as a submodule at
`13c80da97fe4d55ecb5a9745834d97be22821307`, five ordered patches, output
`build/serial_modem_k230/zephyr/tfm_merged.hex`.

⚠ **`tfm_merged.hex` is TF-M plus the non-secure application. It does NOT update the modem
firmware** (`mfw_nrf91x1_*.zip`), which is a separate signed package with its own procedure.
This is the classic nRF91 confusion and LilyGO pre-empted it in their README.

## Debug console

`P0.29` (TX2) and `P0.28` (RX2) are a second UART for the Serial LTE Modem log, brought out for
an **external USB-UART adapter** — not to the K230. If cellular misbehaves and the AT link tells
you nothing, this is where the answer is.

## Alternative: a USB modem

The BSP builds `CDC_MBIM`, `QMI_WWAN`, `USB_WDM`, `USB_SERIAL_OPTION` and PPP, so a **USB LTE
dongle** works on the host port without the keyboard base. Canaan publishes
`K230_4G_Module_Linux_Porting_Reference` for this. Trade-off: bulk and power versus $42.31 and an
integrated GNSS.

## Limits

| Limit | Value | Class |
|---|---|---|
| Radio | **LTE-M and NB-IoT only** — no LTE Cat-1/4, no 5G, no voice | silicon |
| Throughput | LTE-M ≈ hundreds of kbit/s | silicon |
| UART link | 115200 — a real ceiling on data | board |
| Bands | not stated by LilyGO | **unknown** |
| Carrier certification | **none stated** | **unknown** |
| SIM form factor | **not stated** | **unknown** |
| Antenna | **not documented** | **unknown** |
| Measured fix time, power, throughput | **none published** | unmeasured |

**LTE-M/NB-IoT is not general-purpose internet.** It is a low-bandwidth IoT bearer with patchy
availability outside major carriers. Check coverage in your country before buying `K256-04`
rather than `K256-04-A`.

## Pitfalls

1. Forgetting `GPIO2`.
2. `AT+CPIN?` before `AT+CFUN=1`.
3. Expecting `tfm_merged.hex` to update modem firmware.
4. Buying `K256-04-A` and expecting cellular. Read the SKU.
