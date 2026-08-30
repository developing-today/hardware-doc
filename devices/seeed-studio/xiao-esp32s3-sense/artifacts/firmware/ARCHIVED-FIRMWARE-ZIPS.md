# Archived firmware ZIPs — reacquisition record

> Moved out of the repository **2026-08-28**, not deleted. **The extracted contents remain
> in [`../extracted/`](../extracted/)**, so the binaries are still directly readable here —
> only the redundant ZIP wrappers were archived.

## What was archived

| File | Bytes (ZIP) | SHA-256 (of the ZIP) |
|---|---:|---|
| `xiao-esp32s3-sense-firmware-20240814.zip` | 9 520 580 | `d587641766c5e6f9f923eb689f532ab0b9626ee2ccbffaad472f9bdff7f1b001` |
| `xiao-esp32s3-sense-firmware-legacy.zip` | 9 516 661 | `588fc34927522df30f6e54bbbc9f603834a90c4e8f8aaf255ee94b6cb4c1dd07` |
| `xiao-esp32s3-firmware-20240814.zip` | 8 219 852 | `7e4cc51fca6e5b16393e3bc6ed9d929b8c7e36c8a3107b4750d7991312f3fd68` |
| `xiao-esp32s3-firmware-legacy.zip` | 8 217 189 | `0383237f78e873dc7d7cd5d5ea559805ea3269b82ec2d62c9874526cf555ceda` |

Archive path: `../hardware-doc-archive/doc/hardware/devices/seeed-studio/xiao-esp32s3-sense/artifacts/firmware/`

> **The four ZIPs are four distinct files.** Note this does *not* contradict the finding below
> that the 20240814 and legacy *binaries* are identical: the ZIP wrappers differ in the flasher
> scripts and archive metadata around them, so the container hashes differ while the payload
> does not. Verify a re-fetch against the ZIP hash; verify the *firmware* claim against the
> extracted `.bin` files.

## Reacquisition

```bash
B=https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res
curl -fsSL "$B/XIAO-ESP32S3-Sense-firmware-20240814.zip" -o xiao-esp32s3-sense-firmware-20240814.zip
curl -fsSL "$B/XIAOESP32S3-Sense-firmware.zip"           -o xiao-esp32s3-sense-firmware-legacy.zip
curl -fsSL "$B/XIAO-ESP32S3-firmware-20240814.zip"       -o xiao-esp32s3-firmware-20240814.zip
curl -fsSL "$B/XIAO-ESP32S3-firmware.zip"                -o xiao-esp32s3-firmware-legacy.zip
```

Retrieved 2026-08-24. Linked from the wiki's *Resources → Factory Firmware* section.

## What was extracted before archiving

Everything of value is already in committed Markdown — see [`factory-firmware.md`](../../factory-firmware.md):

- **Exact flash offsets** (`0x0` bootloader, `0x8000` partition table, `0xe000` boot_app0, `0x10000` app) and the vendor's full `esptool` argument set
- **Partition table parsed** — `nvs` 20 KB, `otadata` 8 KB, `app0`/`app1` 3 264 KB each, `spiffs` 1 536 KB, `coredump` 64 KB
- **`esp_app_desc_t`** — project `arduino-lib-builder`, built **2023-02-08 18:07:54**, **ESP-IDF v4.4.4**, ELF SHA-256 `06d08da8…`
- **Arduino core 2.0.7** identified from embedded build paths
- **Hardcoded Wi-Fi credentials** (`seeedstudio` / `XIAO_ESP32S3_Sense`) — why the shipped demo cannot join your network
- **The "20240814" release contains 2023 binaries** — byte-identical to the legacy ZIP; only the flashing wrapper changed

Parser: [`tools/esp_image_info.py`](../../../../../tools/esp_image_info.py), re-runnable against the extracted `.bin` files.

## Also removed: `esptool.exe` ×2

Both extractions contained a **7 671 328-byte Windows `esptool.exe`** (SHA-256 `ce5a63d638cf8544…`),
byte-identical to each other — 14.6 MiB for one redundant binary.

> ⚠ **This size and hash are no longer verifiable.** The binary was deleted rather than archived,
> and no copy survives in `../hardware-doc-archive`. The figures above are as recorded at the time
> of deletion and could not be re-checked during the 2026-08-30 audit. The hash is also truncated,
> and cannot now be completed. To verify, re-fetch a firmware ZIP (above) and re-extract.
>
> Deleting rather than archiving is what made this unverifiable — the reason it is worth
> preserving even redundant binaries somewhere.

**Deleted, not archived.** It is a PyInstaller-packed build of Espressif's GPL-2.0 `esptool`,
carrying source-offer obligations, and upstream is trivially installable:

```bash
pip install esptool          # or: pipx install esptool
```

The vendor's `esp32_flasher.py` (MIT, retained in the extractions) invokes it and works fine
against a pip-installed `esptool`. Nothing depends on the bundled binary.
