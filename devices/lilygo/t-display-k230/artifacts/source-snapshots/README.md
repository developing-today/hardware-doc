# Extracted facts — LilyGO T-Display K230 BSP

Source: `Xinyuan-LilyGO/T-Display-K230` @ **`bb831ab358b66f5bd9a87ecd7c580fee4537492e`**
(`main`, 2026-09-03, changelog v0.2.4). Extracted **2026-09-04**.

This file exists so that nothing in this repository depends on re-cloning an unlicensed 110 MB
tree. Where a fact is long, it is written up in full in the authored documents and only pointed
at from here.

## Pinned revisions

| Thing | Pin |
|---|---|
| BSP commit | `bb831ab358b66f5bd9a87ecd7c580fee4537492e` |
| Upstream SDK | `kendryte/k230_linux_sdk` @ `22d02c6b6783a57a3aca7eb3160e313e772cb710` (branch `dev`) — recorded in `k230_bsp/metadata/upstream_sdk_commit.txt` |
| Kernel | `ruyisdk/linux-xuantie-kernel` @ `7d4e1f444f461dbe3833bd99a4640e7b6c2cd529`, defconfig `k230` |
| Toolchain | `/opt/toolchain/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V3.0.2/`, prefix `riscv64-unknown-linux-gnu` |
| Target flags | `-mcpu=c908v -mtune=c908 -mrvv-v0p10-compatible -mrvv-auto-vectorize` |
| LVGL | upstream `59dc7e436ae97a25e32656739ea6a943f9f11b6a` + 4 LilyGO patches |
| Device trees built | `canaan/k230-canmv-rm69a10`, `canaan/k230-canmv-v3`, `canaan/k230-canmv-rm69a10-hdmi` |
| nRF52840 repo | `4646a728580739d487126f47a521e9b8032b3c2c` |
| nRF9151 repo | `ed4ecbe34162dec9b81213a400198125bbd6e36f`; upstream SLM submodule `13c80da97fe4d55ecb5a9745834d97be22821307`; NCS **v3.4.0** |

## Extracted content, and where it now lives

| Content | Written up in |
|---|---|
| Complete GPIO / bus / I²C-address map | [`pinouts-and-buses.md` §1–§7](../../pinouts-and-buses.md) |
| **Full TCA8418 keyboard matrix**, key codes, labels, layout, repeat timing, hotkeys | [`pinouts-and-buses.md` §8](../../pinouts-and-buses.md#8-keyboard-matrix--full-decode) |
| PMU power-key register flow and constants | [`pinouts-and-buses.md` §9](../../pinouts-and-buses.md#9-pmu-power-key-register-flow) |
| IO bank voltage table and the damage warning | [`pinouts-and-buses.md` §6](../../pinouts-and-buses.md#6-io-bank-voltages--the-hardware-damage-path) |
| Build, flash and deploy procedure | [`development.md`](../../development.md) |
| Kernel patch inventory (`0025`–`0064`) | [`development.md` §2.5](../../development.md) |
| Buildroot package selections | [`development.md`](../../development.md), [`features/*`](../../features/) |
| Companion-MCU wiring, AT sets, DFU | [`features/nrf52840-ble.md`](../../features/nrf52840-ble.md), [`features/nrf9151-cellular-gnss.md`](../../features/nrf9151-cellular-gnss.md) |
| Part-number census | [`research-log.md` #19](../../research-log.md) |

## Part-number census — the raw result

Regex sweep over `*.c/cpp/h/md/MD/sh/patch/dts/mk/in/_defconfig` at the pinned commit, ranked:

```
579 lr2021      532 k230       203 nrf9151    168 nrf52840   151 sx1262
124 rm69a10      72 tca8418     59 bq25896     57 bq27220     54 aht20
 44 gc2093       42 xl9555      29 lt9611      25 max98357a   19 gt9895
 16 rtl8723ds    13 sx1268       9 sx1261       6 rtl8189fs    5 k230d
  4 csr8510       3 sx1231       3 rtl8733bs    2 tca8414      2 ov5647
  2 aht10         1 sx1278       1 sx1272       1 rtl8723bs    1 imx219
  1 cp2104        1 bq25890
```

**Zero hits for `esp32`, `esp32s3` or any Espressif identifier.** That negative result is the
evidence behind [`GC-2`](../../gaps-and-conflicts.md).

**Zero hits for any PMIC family** (`axp`, `sy`, `mp`, `tps`, `eta`, `sgm`, `rk8`, `hi65`), which
is why the PMIC is [U1 in the unidentified record](../../../../../components/unidentified/t-display-k230/README.md).

`lr2021` outranking `sx1262` almost four to one is itself informative: LilyGO's recent
development effort is going into the newer radio.

## Files worth re-reading if you do clone it

| Path | Bytes | Why |
|---|---:|---|
| `k230_bsp/docs/HARDWARE_PINMAP.md` | 8 593 | The authoritative pin map |
| `k230_launcher/k230_phone_ui/src/ui_hardware.c` | large | Keyboard matrix, TCA8418 registers, PMU constants, battery policy, XL9555 probe |
| `k230_bsp/metadata/overlay_manifest.txt` | 5 764 | Exactly what the overlay changes, without diffing trees |
| `.../linux/0034-gt9895-touch.patch` | 307 439 | The vendored Goodix Berlin driver |
| `.../linux/0064-input-k230-pmu-pwrkey.patch` | 21 523 | The PMU power-key driver |
| `.../linux/rejected/0044-*.rejected` | 829 | A retained failed patch — write-combine dumb buffers |
| `.../package/vvcam/src/gc2093.c` | 26 213 | Camera sensor register writes, **undecoded** ([`GC-6`](../../gaps-and-conflicts.md)) |
| `.../board/canaan/k230-soc/genimage.cfg` | 1 280 | Authoritative SD image partition layout |
