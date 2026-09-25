# T-Display K230 — nRF52840 co-processor firmware

> What the two prebuilt nRF52840 binaries in this directory actually contain, parsed from the
> bytes on **2026-09-20**. Every value below is **`executed-success`** — read out of the files,
> not from a README.
>
> Upstream: [`Xinyuan-LilyGO/T-Display-K230-nRF52840`](https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840)
> at commit `4646a728580739d487126f47a521e9b8032b3c2c`, retrieved **2026-09-04**.

## Why this matters

The K230 is a RISC-V application processor with **no Bluetooth of its own**. The nRF52840 on the
base board is what gives the product BLE, and it is driven over a UART with an **AT command
set** — which, before this document, was not written down anywhere in this repository or, as far
as this pass could find, anywhere public. The command set is recovered below in full.

It also explains `k230_launcher/k230_phone_ui/src/k230_meshtastic_probe.cpp` in the main
repository: **six of the AT commands are Meshtastic-specific.**

## The two files

| File | Bytes | SHA-256 |
|---|---:|---|
| `k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex` | 525,680 | `6c4eab9534e55d0e80a7797616674d68e9d9eda139222a1bb1439214ae16b7a3` |
| `k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2` | 296,960 | `931948dd024425ce8e8e455da7637cf8e9924a587e1e78b81b690416549e6022` |

Licence: **none declared** in the upstream repository. Redistribution status `unknown`.
Disposition `repository` — together 822 KB, and they are the *only* prebuilt binaries LilyGO
publishes for this product (see [`NO-FACTORY-IMAGE.md`](NO-FACTORY-IMAGE.md)).

---

## 1. The bootloader `.hex`

Intel HEX, 191,108 bytes of payload across five address ranges. This is a **combined
MBR + SoftDevice + bootloader** image — flashing it provisions a blank nRF52840 completely.

### Flash map

| Range | Bytes | Contents |
|---|---:|---|
| `0x00000000 – 0x00000B00` | 2,816 | Nordic **MBR** (master boot record) |
| `0x00001000 – 0x00025DE8` | 151,016 | **SoftDevice S140** |
| `0x000F4000 – 0x000FD124` | 37,156 | **UF2 bootloader** |
| `0x000FD800 – 0x000FD870` | 112 | bootloader tail data |
| `0x10001014 – 0x1000101C` | 8 | **UICR** |

### UICR — the two words that make it boot

| Address | Register | Value |
|---|---|---|
| `0x10001014` | `UICR.NRFFW[0]` — bootloader start address | **`0x000F4000`** |
| `0x10001018` | `UICR.NRFFW[1]` — MBR parameter page | **`0x000FE000`** |

⚠ **These are the field that a careless recovery destroys.** `nrfjprog --eraseall` and a
full-chip erase both wipe UICR; re-flashing only the bootloader region without restoring
`NRFFW[0]` leaves a chip that has a bootloader in flash and no idea where it is. **Flash this
`.hex` whole** — it carries the UICR records — rather than extracting the bootloader region.

### SoftDevice identity — from the info structure at `0x3000`

| Offset | Field | Value |
|---|---|---|
| `+0x04` | `SD_MAGIC` | `0x51B1E5DB` ✅ (the expected constant) |
| `+0x08` | `SD_SIZE` | `0x00026000` = **155,648 bytes** |
| `+0x10` | `SD_ID` | **140** |
| `+0x14` | `SD_VERSION` | `6001001` → **v6.1.1** |

**S140 v6.1.1 confirmed from the binary**, not merely from the filename. `SD_SIZE 0x26000` is
also where the application must start — and the UF2 below targets exactly `0x26000`.

### Bootloader identity — from embedded strings

| String | Meaning |
|---|---|
| `UF2 Bootloader 0.11.0-5-g4d321e2` | **Adafruit nRF52 bootloader**, version 0.11.0, 5 commits past the tag, git `4d321e2` |
| `0.11.0-5-g4d321e2 s140 6.1.1` | the combined version banner |
| `Board-ID: nRF52840-k230-v1` | the UF2 board identifier — **`v1`**, so a revision field exists |
| `Model: LILYGO T-Display K230 nRF52840` | model string in `INFO_UF2.TXT` |
| `K230NRFBOOT` + `FAT16` | the **mass-storage volume label** the bootloader presents |
| `CURRENT UF2`, `INFO_UF2TXT` | the two files on that volume |
| `AdaDFU`, `nRF Serial`, `nRF UF2` | USB interface / descriptor names |
| `location.replace("https://github.com/Xinyuan-LilyGO/T-Display-K230");` | `INDEX.HTM` redirects here |

So the recovery story is: **hold the DFU button, a FAT16 volume named `K230NRFBOOT` appears, drop
a `.uf2` on it.** Vector table at `0xF4000` reads initial SP `0x20040000` (top of the nRF52840's
256 KB RAM) and reset `0x000FC069`.

The filename's `uartdfu_115200` is corroborated by an application string:
`boot version=K230_NRF52840_AT_%s uart_rx=%d uart_tx=%d baud=%d` — the UART DFU path exists
alongside the USB one, at **115200 baud**.

---

## 2. The application `.uf2`

| Field | Value |
|---|---|
| UF2 magic | `0x0A324655` / `0x9E5D5157` ✅ on all blocks |
| Blocks | **580** × 512 B |
| Payload | **148,480 bytes** (256 B per block) |
| `familyID` | **`0xADA52840`** = Adafruit nRF52840 |
| Target range | **`0x00026000 – 0x0004A400`** |

The target start `0x26000` is exactly the `SD_SIZE` above — the application sits directly on top
of the SoftDevice, as it must.

| String | Meaning |
|---|---|
| `+BOOT:K230_NRF52840_AT` | the banner emitted at reset |
| `+VER:K230_NRF52840_AT,` | reply to `AT+VER?` |
| `2026-08-16-k230-uart-dfu-r4` | **the build identifier** — matches the filename's `20260816` / `r4` |
| `k230-%04lx` | the **default BLE device name**: `k230-` plus four hex digits, presumably from the device address |
| `…/framework-arduinoadafruitnrf52/libraries/Adafruit_LittleFS/src/littlefs/lfs.c` | built with **PlatformIO**, `framework-arduinoadafruitnrf52`, using **LittleFS** |
| `NRF52 DK` | a leftover default board string from the Nordic/Adafruit template — **not** evidence of a DK |

---

## 3. The AT command set

Recovered from the `+HELP:` strings the firmware emits for `AT+HELP?`. **`executed-success`** as
an extraction; the *behaviour* of each command is **`not-tested`** — no board was available, and
the descriptions below are the firmware's own help text plus the obvious reading of it.

### Link and device management

| Command | Help text / reading |
|---|---|
| `AT+VER?` | firmware version → `+VER:K230_NRF52840_AT,<build>` |
| `AT+RESET` | reset the nRF52840 |
| `AT+STATUS?` | connection status |
| `AT+NAME=<name>` / `AT+NAME?` | set / read the BLE device name (default `k230-xxxx`) |
| `AT+DFU` | enter DFU — the software route into the bootloader |
| `AT+HELP?` | print the command list (this is the string table mined here) |

### Radio configuration

| Command | Help text |
|---|---|
| `AT+TXPWR=<dbm>` / `AT+TXPWR?` | transmit power |
| `AT+PHY=<AUTO\|1M\|2M\|CODED>` / `AT+PHY?` | **PHY selection including CODED** — long-range BLE is available |
| `AT+MTU=<mtu>` / `AT+MTU?` | ATT MTU |
| `AT+CONNINT=<min_ms>,<max_ms>[,<lat…>]` / `AT+CONNINT?` | connection interval and latency |
| `AT+RSSI?` | RSSI of the current link |

### Central-role operation

The device is a **BLE central**, not merely a peripheral:

| Command | Help text |
|---|---|
| `AT+SCAN[=seconds]` | scan for peripherals |
| `AT+LIST?` | list scan results |
| `AT+CONN=<index\|addr>` | connect by scan index or address |
| `AT+DISC` | disconnect |
| `AT+PAIR`, `AT+BONDCLR` | pair; clear bonds |
| `AT+GATTC=<service_index>` | enumerate characteristics of a service |
| `AT+GATTD=<char_index>` | describe a characteristic |
| `AT+GATTS?` | list discovered services |
| `AT+READ=<handle>[,<offset>]` | GATT read |
| `AT+WRITE=<handle>,<hex>[,REQ\|CMD]` | GATT write, with/without response |
| `AT+SUB=<char_index>,<OFF\|NOTIFY\|INDICATE>` | subscribe |
| `AT+CCCD=<c…>` | write a CCCD directly |

### Meshtastic

**Six commands exist solely to carry Meshtastic traffic**, which is a product-level finding, not
a detail:

| Command | Help text |
|---|---|
| `AT+MESHADV=<ON\|OFF\|name>` | start/stop advertising as a Meshtastic node, with a name |
| `AT+MESHFROM=<fromRadio_hex>` | inject a `FromRadio` protobuf frame |
| `AT+MESHNUM=<fromNum>` | set the `fromNum` notification value |
| `AT+MESHLOG=<log_hex>` | push a log record |
| `AT+MESHSTATUS?` | Meshtastic link status |
| `AT+MESHCLR` | clear Meshtastic state |

`fromRadio`, `fromNum` and the log channel are the three characteristics of the **standard
Meshtastic BLE service**. So the nRF52840 is not merely a BLE modem — it implements the
Meshtastic BLE peripheral profile, with the K230 supplying the protobufs over UART. That is
exactly what `k230_meshtastic_probe.cpp` (752 KB, in the main repository) drives.

---

## Flashing and recovery — `inferred`, **not executed**

⚠ **No hardware was available. Nothing below has been run.** It is derived from the parsed
images and Adafruit-bootloader convention, and is labelled `inferred` throughout. Do not present
it as verified.

**Application only**, via the UF2 bootloader:

1. Enter the bootloader — double-tap reset, or `AT+DFU` from a working application.
2. A FAT16 volume **`K230NRFBOOT`** enumerates over USB.
3. Copy `k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2` onto it.
4. The bootloader validates `familyID 0xADA52840` and writes to `0x26000`, then resets.

**Full provisioning / unbricking**, needing an SWD probe:

```bash
# inferred — NOT executed
nrfjprog -f NRF52 --eraseall
nrfjprog -f NRF52 --program k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex --verify
nrfjprog -f NRF52 --reset
# then drop the .uf2 on the K230NRFBOOT volume
```

The `.hex` includes MBR, SoftDevice **and** the UICR words, so it is self-sufficient after an
`--eraseall`. The nRF52840 SWD pads are visible in
[`../media/nrf52840-baseboard-pins-annotated.png`](../media/nrf52840-baseboard-pins-annotated.png)
and in `images/swd.png` (3.1 MB) in the upstream repository.

## Reacquisition — `automatic`

```bash
B=https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840/raw/4646a728580739d487126f47a521e9b8032b3c2c
curl -fsSL -O "$B/bootloader/k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex"
curl -fsSL -O "$B/firmware/k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2"
sha256sum -c <<'EOF'
6c4eab9534e55d0e80a7797616674d68e9d9eda139222a1bb1439214ae16b7a3  k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex
931948dd024425ce8e8e455da7637cf8e9924a587e1e78b81b690416549e6022  k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2
EOF
```

Second, mutable URL: replace the commit SHA with `master`.

## Open questions

- **The UART link is already documented elsewhere and this image agrees with it.** The device
  record gives K230 **UART1** — `GPIO3` TX → `P0.11`, `GPIO4` RX ← `P0.12`, `/dev/ttyS1`,
  **115200 8N1** ([`../../features/nrf52840-ble.md`](../../features/nrf52840-ble.md),
  evidence `reported-working`). The application's boot banner
  `boot version=K230_NRF52840_AT_%s uart_rx=%d uart_tx=%d baud=%d` prints the values it is
  actually using, so **a single serial capture would upgrade that from `reported-working` to
  `executed-success`.** The bootloader's UART DFU path is fixed at 115200 by its filename and
  matches.
- **`Board-ID: nRF52840-k230-v1`** implies a `v2` may exist or be planned. Not seen.
- **No Meshtastic protocol version string** was found, so which Meshtastic firmware generation
  this profile matches is **not established**.
- The AT command *responses* and error formats are not recovered — only the `+HELP:` strings.

## See also

- [`NO-FACTORY-IMAGE.md`](NO-FACTORY-IMAGE.md) — there is no K230-side factory image, and why that matters
- [`../../factory-firmware.md`](../../factory-firmware.md)
- [`../../development.md`](../../development.md)
- [`../../acquisition/manifest.json`](../../acquisition/manifest.json) — the three entries corrected by this pass
- [`../media/nrf52840-baseboard-pins-annotated.png`](../media/nrf52840-baseboard-pins-annotated.png)
