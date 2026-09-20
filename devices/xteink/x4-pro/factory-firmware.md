# Xteink X4 Pro — factory firmware

> Retrieval date **2026-09-04**. **No X4 Pro stock image was located for
> download.** Everything below about the stock firmware is read from the FreeInk
> SDK's reverse-engineering notes, which were made against dumps the SDK authors
> held privately.

## Partition layout (16 MB, dual-OTA)

| Label | Type | Subtype | Offset | Size |
|---|---|---|---:|---:|
| `nvs` | data | nvs | `0x009000` | `0x005000` (20 KiB) |
| `otadata` | data | ota | `0x00E000` | `0x002000` (8 KiB) |
| `app0` | app | ota_0 | `0x010000` | `0x7E0000` (8064 KiB) |
| `app1` | app | ota_1 | `0x7F0000` | `0x7E0000` (8064 KiB) |
| `spiffs` | data | spiffs | `0xFD0000` | `0x014000` (80 KiB) |
| `coredump` | data | coredump | `0xFE4000` | `0x01C000` (112 KiB) |

**[SDK]** `docs/xteink-x4pro-support.md` §Partitions.

**This layout differs from the C3 X4's**, which uses 6400 KiB app slots and a
3456 KiB spiffs. Do not assume one from the other — see
[`../x4/factory-firmware.md`](../x4/factory-firmware.md).

## The two-image trap

The dump carries **two application images, and they are for different devices**:

| Slot | Board tag | What it is |
|---|---|---|
| `app0` @ `0x10000` | `ESP32S3_X4_TL` | **A different variant.** Arduino-era, hardcoded pins |
| `app1` @ `0x7F0000` | `XTEink X4 Pro` / `ESP32S3_X4_TL_SSD1677` | **The real firmware.** Native `esp_driver_sdmmc`, `XTEink::SSD1677_800x480`, `XTEink::GT911Driver`, `XTEink::EPDPanelInterface` |

`otadata` selects **app1**.

**Every early reverse-engineering pass read app0 and got a wrong pin map** — CS and
DC swapped, SCLK/MOSI in the wrong order — which produced months of false
conclusions about a nonexistent EPD power-management IC. If you dump an X4 Pro,
**read otadata first and analyse the slot it actually selects.**

## Known stock firmware versions

| Version | Build date | Toolchain | Evidence |
|---|---|---|---|
| **7.0.8** | not recorded | — | Frontlight init passes 25 kHz / 10-bit **[SDK]** |
| **7.0.11** | not recorded | — | The X4 **Classic** dump's app0 version, for comparison |
| **7.4.4** | **2026-08-27** | **ESP-IDF 6.0.1** | App descriptor. OTA package labels itself `V7.4.5`; **the embedded app descriptor is authoritative** |

**Conflict, recorded:** OTA package metadata says `V7.4.5` while the app descriptor
inside says `7.4.4`. The SDK states the descriptor wins. Do not report the
package label as the firmware version.

The 7.4.4 OTA package filename is
**`xteink_app_update_x4pro_7.4.4_20260827_133901.xota`**. The `.xota` extension
implies a vendor-specific (probably encrypted) container — the SDK refers to *"the
decrypted ESP32-S3 app"*, so decryption is required before analysis and the
mechanism is **not documented anywhere found**.

## OTA and network endpoints

Recovered from the **X4 (C3)** dump, and reasonably assumed shared brand-wide but
**not verified on an X4 Pro image**:

| Endpoint | Role |
|---|---|
| `http://gotaserver.xteink.com/api/check-update` | OTA update check. **Plain HTTP** |
| `http://bofi.xteink.cn/index.html` | On-device web file manager |

Both are `inferred` for this device.

## How to dump the stock firmware

`inferred` — not executed. Requires a **USB-unlocked** unit (see
[`development.md`](development.md#usb-lock)); a locked unit cannot be read at all.

```bash
# inferred — standard esptool full-flash read for a 16 MB ESP32-S3
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
           read_flash 0 0x1000000 x4pro-stock-full.bin
sha256sum x4pro-stock-full.bin
```

Then parse it:

```bash
# inferred; the repo already ships a helper
python3 tools/esp_image_info.py x4pro-stock-full.bin
```

Community tools that automate this:

| Tool | Scope | Note |
|---|---|---|
| [`HomeAssistantPi/xteink-backup-utility`](https://github.com/HomeAssistantPi/xteink-backup-utility) | *"Flash and Storage Utility for XTEINK / ESP32-S3. Built for my XTEINK 4 PRO."* | The only X4 Pro-specific backup tool found |
| [`zocs/eink-quick-flasher`](https://github.com/zocs/eink-quick-flasher) | X3/X4 only — **not** the Pro | 1:1 full-flash backup & restore, ~2 min |

## How to restore

```bash
# inferred — write a full-flash image back at offset 0
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
           write_flash 0 x4pro-stock-full.bin
```

**There is no public X4 Pro stock image to fall back on.** For the X3 and X4 there
are community-hosted stock images; for the Pro there are none. **Your own backup
is the only restore path.** Make one first.

## Artifacts held

**None.** Recorded honestly:

| Wanted | Status |
|---|---|
| X4 Pro full-flash dump | **not located** — reacquisition `blocked` (nobody has published one) |
| `xteink_app_update_x4pro_7.4.4_20260827_133901.xota` | **not located** — named in the SDK docs only; no download URL found |
| Vendor OTA feed contents | **not fetched** — `gotaserver.xteink.com` not queried this session |

Querying the OTA endpoint directly is the obvious next step and was **not done**;
see [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

By contrast the **X4 (C3)** full-flash dump *was* obtained and is archived —
see [`../x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md`](../x4/artifacts/firmware/xteink-x4-oem-full-flash-16mb.bin.ARCHIVED.md).
It is a **different device** and cannot be flashed here, but it is useful for
understanding the vendor's firmware conventions.

## Recovered OEM display command streams

Version-scoped, because the refresh sequence changed between releases:

| Mode | X4 Pro 7.4.4 | Earlier X4 Pro image | X4 default | Sticky |
|---|---|---|---|---|
| Full | `0xF7` | `0xF7` | `0xF7` | `0xF7` |
| Fast | **`0xFC`** | **`0xC7`** | `0xFC` | `0xFF` |

7.4.4 routines: FULL at IROM `0x421e36ac`, FAST at `0x421e37b8`. Both set border
`0x3C = 0xC0`, then update control `0x22`, then master activation `0x20`, then
wait BUSY. **Neither touches the LEDC/frontlight path** — so the visible
whole-panel light-then-dark flash during a FAST refresh is the electrophoretic
waveform, not a frontlight change. That distinction has confused people.

Earlier image, INIT at `0x4201a568`: SW RESET `0x12`, then a **fixed `delay(10)` —
not a BUSY-wait**; temp sensor `0x18 = 0x80` (internal); booster
`0x0C = AE C7 C3 C0 80`; driver output control `0x01 = DF 01 02` (gate lines
`0x01DF` = 479 → MUX 480, `SM=1`); border `0x3C = 0x80`; RAM window via
`0x11/0x44/0x45/0x4E/0x4F`, width `0x320` = 800, height `0x1E0` = 480.

There is **no external EPD PMIC and no external charge pump.** The controller
drives its high-voltage rails from its **internal booster** (`0x0C` soft-start).

## Vendor-driver audit findings

Reading the OEM code against the datasheets surfaced these, all recorded by the
FreeInk maintainers:

| Finding | Consequence | Severity |
|---|---|---|
| OEM clocks the panel at **5 MHz** when the SSD1677 is rated **20 MHz** for writes | ~4× slower RAM writes than necessary | Performance, not correctness |
| OEM INIT uses a **fixed 10 ms delay instead of a BUSY-wait** after SW RESET | Works, but is a timing assumption rather than a handshake | Latent |
| OEM ships a **4-threshold ADC button ladder matcher** (`0x4201f734`, BACK≈3580 / OK≈2728 / UP≈1514 / DOWN≈0, ±319) that **is not wired on this variant** | Dead code; misled RE into proposing an ADC ladder input that does not exist | Inert, but actively misleading |
| **No GT911 config table anywhere** in app0, app1, spiffs or nvs | Confirms the OEM also relies on GT911 self-load; a firmware that uploads a config is doing something the vendor does not | Informational |
| CW2017 reports 0% until an 80-byte BATINFO profile is loaded | Battery percentage silently wrong if the profile is missing | **Active** |

## Related

[`development.md`](development.md) ·
[`features/display.md`](features/display.md) ·
[`../x4/factory-firmware.md`](../x4/factory-firmware.md)

---

## Round 2 — 2026-09-11: a hardware witness

**No line above was altered.**

A third party dumped a **physical retail X4 Pro** on 2026-09-06 and published the
analysis (not the image — it is proprietary and contains the owner's Wi-Fi
credentials). [`kycube/x4pro-emu`](https://github.com/kycube/x4pro-emu/tree/bf4b86ae0471012d4d07c0bb3042f3f561c9c302) @ `bf4b86a`.

| Field | Value |
|---|---|
| Dump integrity | **two dumps, identical SHA-256** `90734554798da8dbe1961bf876a7bf44f2ea66a572ae2ed9b7ed395c9a0143fe` |
| A later dump, post-CrossPoint | `326f3c8f066a8db7857d56d80eab755bba903eb3566245a985833b09e4c5bb20` |
| Bootloader | ESP-IDF **v6.0.1** second-stage, built **2026-08-14 19:24:53**, entry `0x403c8870`, min rev v0.0 / max v0.99 |
| `app0` @ `0x10000` | **`xteink_app` 7.2.4**, ESP-IDF v6.0.1, compiled **2026-08-14 19:25:05**, 8 segments, entry `0x40379908`, ELF SHA-256 `5e6f90d4…`, **hash valid** |
| `app1` @ `0x7F0000` | **erased** (`0xFF`) |
| `otadata` @ `0xE000` | entry 0 `seq=1 state=2 (VALID) crc=0x4743989a`; entry 1 erased → **`app0` boots** |
| `spiffs` @ `0xFD0000` | 135 non-`0xFF` bytes in 80 KB — effectively empty |
| `coredump` @ `0xFE4000` | erased |
| **eFuse BLOCK3** | ASCII **`X4CB02EN26082416646`** — a factory serial |

### Version conflict — now four numbers

| Version | Where | Note |
|---|---|---|
| **7.2.4** | **a physical desk unit**, ESP-IDF v6.0.1, built 2026-08-14 | the only **hardware-read** version |
| 7.4.4 | app descriptor | pre-existing, recorded above |
| V7.4.5 | package metadata | pre-existing, recorded above |
| 7.5.4 | a third-party analysis doc `docs/stock-7.5.4.md` | — |

**Not reconcilable from public evidence.** The vendor publishes no changelog and
ships regional (`hw_calib/region` 1 = CN, 2 = overseas) and OTA-staged builds.
Recorded as a conflict, not resolved by preference.

### NVS on a retail unit

`xteink_sys` · `hw_calib` (**`screenType=2` → UC8279**, `region`, `lightDS`) ·
`user_config` (`sta_ssid`, `sta_pwd`, `wifi_creds`, `cfg_init`, `fbLangDone`,
`net_en`, `cloud_bind_st`, `otaPromptDay`, `pwrTimingVer`, `lightBri=100`,
`lightCT=100`) · `misc` · `nvs.net80211` · `phy` (`cal_data`).

`lightBri` and `lightCT` are direct evidence of a **dual-channel** frontlight
with a colour-temperature control — corroborating the warm/cool pair from a
completely different direction than the board profile.

### Community install method, restated with its hazard

The community installs CrossPoint by **writing only the app at `0x10000`** over
the stock bootloader and stock partition table. That works precisely because the
stock table already has an `otadata` partition and because `nvs` at `0x9000`
survives — and `nvs` is where `hw_calib/screenType` lives. **Any procedure that
erases the whole chip loses the panel identity.** On the X4 Pro the boot-time bus
probe repairs that automatically; on the [X4 Classic](../x4-classic/factory-firmware.md)
it cannot, because that board has no MISO.
