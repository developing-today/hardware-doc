# Xteink X3 — factory firmware

> **One X3 stock image is now held: the CN V5.2.13 OTA image** (app partition only,
> 6,254,064 B). Fetched **2026-09-11**, archived and fully parsed **2026-09-20** —
> see **[`artifacts/firmware/x3-stock-firmware-teardown.md`](artifacts/firmware/x3-stock-firmware-teardown.md)**.
> The three 16 MB full-flash images remain unfetched. Original survey retrieved **2026-09-04**.
>
> ⚠ **Corrected 2026-09-20.** This page previously read *"No X3 flash dump was obtained by this
> session… Not downloaded."* That was true on 2026-09-04 and became false on 2026-09-11, when a
> later pass fetched the OTA image via the Git-LFS batch API but left it in a scratch directory
> without updating this page.

## Known stock versions

From [`zocs/eink-quick-flasher/firmware/README.md`](https://github.com/zocs/eink-quick-flasher/blob/main/firmware/README.md):

| File | Language | Version | Type | Size |
|---|---|---|---|---|
| `x3_en_v1.0.7_full.bin` | EN | **V1.0.7** | full backup | 16 MB |
| `x3_en_v5.2.13_full.bin` | EN | **V5.2.13** | full backup | 16 MB |
| `x3_cn_v5.2.13_full.bin` | CN | **V5.2.13** | full backup | 16 MB |
| `x3_cn_v5.2.13_ota.bin` | CN | V5.2.13 | OTA (app only) | ~6 MB |

The X3 is the **only Xteink with published full-flash images** — the X4 has only
OTA images in that repository (plus the separate community dump this repo
archived), and the X4 Pro and X4C have nothing.

**Key fact from that README:**

> "CN/EN 标注仅为默认界面语言不同，固件内容完全一致，刷入后可在设置中切换语言。"
> *"CN/EN designation only indicates the default UI language. Firmware content is
> identical; language can be switched in settings after flashing."*

So there is **no regional firmware split** — only a default setting. A CN unit and
an EN unit run the same code.

**Three of the four are not downloaded.** The `.bin` entries in the Git tree are
**~130-byte Git LFS pointers**; fetching the real blobs needs `git lfs` or the LFS
batch API. The **CN OTA image is held** — see
[`artifacts/firmware/x3_cn_v5.2.13_ota.bin.ARCHIVED.md`](artifacts/firmware/x3_cn_v5.2.13_ota.bin.ARCHIVED.md)
for the working recipe, which applies unchanged to the other three.

## Version numbering

V1.0.7 → V5.2.13 on the same device suggests either a renumbering or that V5.x is
a shared platform version across X3 and X4 (the X4's images are `v5.1.6` and
`v5.2.13` — **the same V5.2.13 build number appears on both devices**). That is
consistent with one codebase serving both C3 models, exactly as the community
firmware does.

## Partition layout

**Not established for the X3.** For reference, the sibling **X4** (same SoC, same
16 MB flash) uses:

`nvs` `0x9000` · `otadata` `0xE000` · `app0` `0x10000` (6400 KiB) ·
`app1` `0x650000` (6400 KiB) · `spiffs` `0xC90000` (3456 KiB) ·
`coredump` `0xFF0000`.

**Inferred, not confirmed,** that the X3 matches. Verify before writing at offsets.
An OTA image cannot show a partition table; closing this needs one of the three
16 MB full-flash images.

⚠ **The data partition's *format* is now known, and it is not SPIFFS.** The X3
application mounts **LittleFS** at `/littlefs` (`LittleFS`, `LittleFS startup
failed` and `/littlefs` all appear in the OTA image; `spiffs` appears once, as a
bare label). The partition *subtype byte* may still carry the `spiffs` value
`0x82` — harmless, since the subtype is only a label — but **anything that tries
to read the data partition as SPIFFS will fail.** `executed-success`, 2026-09-20.

## NVS

The FreeInk SDK reads NVS namespace **`hw_calib`**, key **`screenType`** (u8) for
diagnostics on the X4 family. Whether the X3 populates it is **not established**.
Note the SDK's warning that this value is unreliable in the field on devices where
the display bus can be probed: *"a full-flash from another unit overwrites it, so
it can name the wrong panel."*

**A practical consequence of that warning specific to this repository's users:**
if you restore an X3 from *someone else's* `x3_*_full.bin`, you inherit their
`hw_calib` — so a UC8253 unit can end up claiming to be a UC8279 unit. The X3's
boot probe reads the live bus and overrides it, but a naive firmware would not.

## Endpoints

Recovered from the **X4** dump and reasonably assumed shared, but **not verified
on an X3 image**:

| Endpoint | Role |
|---|---|
| `http://gotaserver.xteink.com/api/check-update` | OTA check, plain HTTP |
| `http://bofi.xteink.cn/index.html` | On-device web file manager |

## Dump and restore

```bash
# reported-working — this is what eink-quick-flasher automates (~2 min for 16 MB)
esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 921600 \
           read_flash 0 0x1000000 x3-stock-full.bin
esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 921600 \
           write_flash 0 x3-stock-full.bin
```

Requires a **USB-unlocked** unit. `zocs/eink-quick-flasher` ships an
`X3-FLASHER-GUIDE` in English and Chinese — the most detailed X3 flashing
documentation that exists.

## Artifacts held

**None.** What exists and was not fetched:

| Artifact | Status | Reacquisition |
|---|---|---|
| `x3_en_v1.0.7_full.bin` | not fetched | `manual` — Git LFS from `zocs/eink-quick-flasher` |
| `x3_en_v5.2.13_full.bin` | not fetched | same |
| `x3_cn_v5.2.13_full.bin` | not fetched | same |
| `x3_cn_v5.2.13_ota.bin` | not fetched | same |

Licence for all four: **none declared**; they are vendor firmware redistributed by
a third party. Redistribution status **unknown, probably prohibited**.

## Related

[`development.md`](development.md) · [`../x4/factory-firmware.md`](../x4/factory-firmware.md)

---

## Round 2 — 2026-09-11: the LFS gap is closed as an acquisition problem

**No line above was altered.** The statement above — *"**Not downloaded.** The
`.bin` entries in the Git tree are ~130-byte Git LFS pointers. Fetching the real
blobs needs `git lfs` or the LFS API… this is cheap to close"* — was right that
it was cheap. It is now closed **as an acquisition record**:

**[`artifacts/firmware/zocs-x3-stock-images.NOT-FETCHED.md`](artifacts/firmware/zocs-x3-stock-images.NOT-FETCHED.md)**

carries, for all four images, the **exact byte size and exact SHA-256** (the
Git-LFS `oid` *is* the content SHA-256), the pinned upstream commit
`79d2f5b8f1df08d2c8fb33146ac5f887790ddb9e`, and a **verified, unauthenticated
download recipe that does not require `git lfs`**. The placeholder stands alone:
a reader with neither this repository's archive nor an LFS client can reacquire
and verify every file from it.

| File | Bytes | SHA-256 |
|---|---:|---|
| `x3_en_v1.0.7_full.bin` | 16,777,216 | `f631402cceff2a3e39252ca1fc71afee8274b3060afe7f81d2e5dd45413c8b22` |
| `x3_en_v5.2.13_full.bin` | 16,777,216 | `37efcb7db2422b6c7b86b23b2e82b0fb4453ebde350014e7f8e8ad3f06ca2dac` |
| `x3_cn_v5.2.13_full.bin` | 16,777,216 | `edfe1e5eb0083b860f82281aa25391a3fdea2a598a1fb618408808a18a6ca9aa` |
| `x3_cn_v5.2.13_ota.bin` | 6,254,064 | `0b2cbc4a6414aef4ad6e676b59fdefa3b529189758953765b26df02bac77bcb6` |

**One image was actually fetched and parsed** to prove the method — the 6.25 MB
CN OTA — and its hash matched its oid exactly.

> ⚠ **Corrected 2026-09-20.** The next sentence used to read *"It was **not
> retained** (unknown licence, proprietary vendor firmware)."* **It was retained**
> — it sat in `archive/devices/xteink/shared-artifacts/research-scratch/x3-lfs/` from 2026-09-11. It is now archived at
> `archive/devices/xteink/x3/artifacts/firmware/x3_cn_v5.2.13_ota.bin` with a
> placeholder, and has been **fully mined**:
> **[`artifacts/firmware/x3-stock-firmware-teardown.md`](artifacts/firmware/x3-stock-firmware-teardown.md)**.
> The licence position is unchanged — redistribution status **`unknown`**, so it is
> archived rather than tracked.

What the header establishes:

| Field | Value |
|---|---|
| **`chip_id`** | **5 = ESP32-C3** — independent, machine-readable confirmation of the X3's SoC |
| `project_name` | `arduino-lib-builder`; `idf_ver` **`v4.4.7-dirty`** |
| Entry / segments | `0x40381E52`, 6 segments |
| Strings | `5.2.13`, `xteink`, **`xteink_ble`** |

**The X3 and X4 stock firmwares share a build base** — Arduino/ESP-IDF v4.4.7,
exactly as this repository established by parsing the X4 dump. That is direct
support for the "one codebase, two C3 models" reading of why `V5.2.13` appears on
both devices.

**`xteink_ble` is new.** The X3's Bluetooth capability is not characterised
anywhere in this tree, and this is the first evidence the stock firmware carries
a BLE component. Recorded as a gap, not a feature claim. The 2026-09-20 teardown
narrows it: the stack is **NimBLE-Arduino 2.3.6**, the advertised names are
`xteink_ble` / `XTEPD_BLE_`, the GATT label is `XTEINK App Connection`, and the
device ships its own protocol description on-flash at `/BLE Protocol.txt` and
`/system/BLE.txt`.

## What else the OTA image gave up

Full extraction: **[`artifacts/firmware/x3-stock-firmware-teardown.md`](artifacts/firmware/x3-stock-firmware-teardown.md)**.
Headlines, all `executed-success` 2026-09-20:

| | |
|---|---|
| Vendor OS name | **`XTOS V5.2.13`** — not previously recorded anywhere in this tree |
| Device string sent to the backend | **`ESP32C3_X3`** |
| Real toolchain | **PlatformIO on Windows** (`/C:/Users/32651/.platformio/…`), `framework-arduinoespressif32`. The `Mar 5 2024` descriptor date is the **Arduino core's** build date, not the firmware's — the image has **no trustworthy build timestamp** |
| Data filesystem | **LittleFS**, not SPIFFS — see [Partition layout](#partition-layout) |
| Backends (all plain HTTP) | `api-prod.xteink.cn`, `bofi.xteink.cn`, hardcoded `8.130.157.48:5000`, QR via `active.clewm.net` |
| On-device HTTP API | ~30 routes incl. `/Put_sdFrequency`, `/setWallpaper`, `/Read_updataAddress`, `/update.bin` |
| UI languages shipped | **EN, JA, ZH-CN** — Japanese was not previously known |
| Undocumented file formats | **`.xtc`** (cached book), **`.xtg`** (cover), **`.xth`** (chapter summary) |
| Extra features | stock ticker, weather, factory burn-in / SD-benchmark mode (`老化测试`) |

**Negative results** (searched for, absent — do not re-search): no display-controller
part number, **no RTC part number** (so this image does **not** settle the three-way
X3 RTC conflict), no fuel-gauge part number, no `hw_calib`/`screenType` key, and no
NFC string.
