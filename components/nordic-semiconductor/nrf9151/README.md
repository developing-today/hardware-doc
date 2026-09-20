# Nordic Semiconductor nRF9151 — LTE-M / NB-IoT / DECT NR+ SiP with GNSS

- **Category:** cellular IoT System-in-Package — Arm Cortex-M33 application core + LTE-M/NB-IoT modem + **GNSS** + RF front end + PA in one 10 × 16 mm package
- **Manufacturer:** Nordic Semiconductor ASA
- **Research status:** part identified and integration fully documented from LilyGO's firmware repository; Nordic's own documentation referenced rather than restated.
- **Retrieved:** 2026-09-04

## 1. Core facts

| Property | Value |
|---|---|
| Application core | Arm **Cortex-M33** with **TrustZone**; secure/non-secure split enforced by **TF-M** |
| Cellular | **LTE-M (Cat-M1)** and **NB-IoT (Cat-NB1/NB2)**, 3GPP Rel-14 |
| Other radio | **DECT NR+** (non-cellular standalone) |
| Positioning | **GNSS** receiver in-package |
| Package | 10 × 16 mm SiP; successor/smaller sibling to nRF9160 |
| SDK | **nRF Connect SDK (NCS)** — Zephyr-based |
| Modem firmware | separate signed package `mfw_nrf91x1_*.zip`, **not** updated by an application build |

## 2. The TF-M split, and why it matters at build time

Every nRF91-series application is really two images: TF-M (secure) plus the non-secure
application. LilyGO's build produces **`tfm_merged.hex`**, and their README states the
consequence explicitly:

> "`tfm_merged.hex` contains TF-M plus the non-secure application. **It does not update the
> cellular modem firmware package `mfw_nrf91x1_*.zip`.**" — S2

That is the single most common nRF91 support question and LilyGO answered it in their own
README, which is worth noting because most vendors do not.

## 3. Used By

### [LilyGO T-Display K230 Kit](../../../devices/lilygo/t-display-k230/README.md) — *added 2026-09-04*

Fitted on the **nRF9151 cellular / GNSS / keyboard base board** — the keyboard half of the
T-Display K230 Kit. It is a **priced option**: SKU `K256-04` is "Keyboard Only / **With
nRF9151**" at $113.25, `K256-04-A` is "Keyboard Only / **Without nRF9151**" at $70.94
(2026-09-04, S3). The nRF9151 therefore accounts for roughly **$42** of the keyboard's price,
which is the cleanest available measure of what the cellular option costs.

**Wiring (S1, S2):**

| nRF9151 pin | Goes to | Direction | Notes |
|---|---|---|---|
| power enable | K230 **`GPIO2`** | K230 output | **high enables** the module, low disables it |
| `P0.26` (UART1 RX1) | K230 **`GPIO28`** / UART3 TX | K230 → nRF9151 | AT command link, `/dev/ttyS3` |
| `P0.27` (UART1 TX1) | K230 **`GPIO29`** / UART3 RX | nRF9151 → K230 | AT responses and URCs |
| `P0.29` (UART2 TX2) | external USB-UART RX | out | optional debug console |
| `P0.28` (UART2 RX2) | external USB-UART TX | in | optional |
| `P0.23` | blue LED **inside the PCB** | out | run/GNSS status; on by default, AT-controllable |

**115 200 8N1, no RTS/CTS.** Enabled by `0061-riscv-dts-rm69a10-enable-uart3-nrf9151.patch`,
which also configures `GPIO2` as the userspace modem-enable pin.

**Two firmware profiles** are published (`Xinyuan-LilyGO/T-Display-K230-nRF9151`, commit
`ed4ecbe34162dec9b81213a400198125bbd6e36f`, 2026-08-14):

| Profile | Use |
|---|---|
| `serial_modem_k230/` | **Recommended.** Nordic **Serial LTE Modem** adapted for the K230; provides the LTE/SIM/GNSS/NMEA/LED behaviour the launcher's Cellular app expects. |
| `at_client_k230/` | Minimal AT passthrough for bring-up only. |

The Serial LTE Modem profile is built from a **pinned submodule** —
`third_party/ncs-serial-modem` at commit `13c80da97fe4d55ecb5a9745834d97be22821307` — with five
LilyGO patches applied in order: GNSS NMEA URC + LED, optional XDFU, UART diagnostics, a GNSS
NMEA URC worker, and AT LED control. **The upstream pin and the patch set are both retained
upstream**, which makes this one of the better-documented vendor forks encountered in this
repository.

**Toolchain:** `nrfutil sdk-manager install --install-dir "$PWD/ncs" v3.4.0` — **NCS v3.4.0**,
installed repository-relative at `./ncs/v3.4.0` or overridden with `NCS_ROOT`.
Build target overlay: `boards/nrf9151dk_nrf9151_ns.overlay` (the `_ns` suffix is the
non-secure target, consistent with the TF-M split above).

**Runtime behaviour LilyGO documents (S2):** `AT+CFUN=1` is required *before* SIM commands like
`AT+CPIN?`; `AT#XNMEA=0|1` toggles NMEA URCs on the AT UART; a GNSS fix changes the LED to a
1 s cadence with ~300 ms on-time.

## 4. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `k230_bsp/docs/HARDWARE_PINMAP.md` | LILYGO | primary | repository doc | `https://github.com/Xinyuan-LilyGO/T-Display-K230/blob/bb831ab358b66f5bd9a87ecd7c580fee4537492e/k230_bsp/docs/HARDWARE_PINMAP.md` | 2026-09-04 | GPIO2 enable, UART3 mapping |
| S2 | `T-Display-K230-nRF9151` README and patch set | LILYGO | primary | repository | `https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF9151/tree/ed4ecbe34162dec9b81213a400198125bbd6e36f` | 2026-09-04 | Pin map, NCS version, submodule pin, patch list, AT behaviour, TF-M caveat |
| S3 | T-Display K230 Kit `/products/t-display-k230-kit.js` | LILYGO | primary | store listing | `https://lilygo.cc/products/t-display-k230-kit.js` | 2026-09-04 | `K256-04` $113.25 with nRF9151, `K256-04-A` $70.94 without |
| S4 | nRF91 AT Commands Reference Guide v0.7.1 | Nordic Semiconductor | primary | manual | `https://www.nordicsemi.com/-/media/Restricted/ProductKeys/L984675KPNS/nrf91atcommandsv071.pdf` | not retrieved (restricted path) | AT command reference, as cited by LilyGO |
