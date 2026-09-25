# ARCHIVED: `artifacts/originals/`

> This directory was **moved out of the repository**, not deleted. `originals` is a symlink
> pointing into the machine-local archive, so on a fresh clone it **dangles**. Everything needed
> to reacquire its contents without the archive is below.

Archived **2026-08-30**. Placeholder written **2026-09-20** — until then the directory had only
a symlink and a provenance block in [`../README.md`](../README.md), which a reader arriving at
this path directly would not have found.

| Field | Value |
|---|---|
| Original repo path | `devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/originals/` |
| Archived to | `archive/devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/originals/` |
| Type | directory, **1 file** |
| Reason | 112 MiB vendor demo archive; bulky, and mined — see below |

## Contents

| File | Bytes | SHA-256 |
|---|---:|---|
| `ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip` | 117,768,225 | `b5319593738e114270852d84be0fdd8ccdc21ef1dac897b15f4fad5069dd66b8` |

## How to get it back

Vendor download, the only known source — **no third-party mirror has been located**:

```bash
curl -L -O https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip
echo "b5319593738e114270852d84be0fdd8ccdc21ef1dac897b15f4fad5069dd66b8  ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip" | sha256sum -c -
```

Probed 2026-08-24: `HTTP/1.1 200`, `Content-Length: 117768225` — matches the archived byte size
exactly. If that URL dies, try `https://web.archive.org/web/2/https://files.waveshare.com/wiki/ESP32-P4-WIFI6-Touch-LCD-XC/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip`.

> **Single-source risk.** Unlike Waveshare's `/wiki/common/` shared pool this file sits under a
> product-specific directory with no mirror found. Strong candidate for `web.archive.org/save/`.

Restore from the local archive:

```bash
mv "$(git rev-parse --show-toplevel)/../repo-archive/hardware-doc/devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/originals/ESP32-P4-WIFI6-Touch-LCD-XC-Demo.zip" \
   "devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/originals/"
```

## What the repository still knows without it

This is the test that matters. The extraction is in [`../README.md`](../README.md):
the extracted tree digest and file count, the per-project demo inventory, the bundled
third-party trees and their upstream identity, and the board-specific findings
(`test_esp_lcd_jd9365.c` init tables, `displays_config.h`, register `0x40`) which are written up
in [`components/jadard/jd9365`](../../../../components/jadard/jd9365/README.md) and the two
variant records. The ZIP is raw material; none of the findings depend on reopening it.

## Two bundled trees are **not** in the archive, deliberately

Both were checked against upstream and found **byte-for-byte stock**, so they are reacquirable
by definition and no copy is retained anywhere:

| Bundled path in the demo | Upstream | Version | Pinned commit |
|---|---|---|---|
| `Arduino/libraries/lvgl` | [`lvgl/lvgl`](https://github.com/lvgl/lvgl) | **v9.3.0** | `c033a98afddd65aaafeebea625382a94020fe4a7` |
| `Arduino/libraries/GFX_Library_for_Arduino` | [`moononournation/Arduino_GFX`](https://github.com/moononournation/Arduino_GFX) | **v1.6.0** | `e7f29f12b247015c0cf99f59a525e30cd1b1dab1` |

Standalone release zips of both were downloaded in 2026-08 for that comparison and held in
scratch until **2026-09-20**, when they were dropped as reacquirable upstream releases:

| Release zip | Bytes | SHA-256 |
|---|---:|---|
| `lvgl-9.3.0.zip` | 90,040,639 | `7225e7d2b83f89f3d089d3c3492083d447abb990fded24ad5bbaaa541e8746af` |
| `Arduino_GFX-1.6.0.zip` | 10,824,248 | `00b69b399408691aa21ecbe2113277541241d33cebc0865ccbf1c5024a2270cd` |
| `esp_lcd_jd9365-2.0.2.zip` | 16,200 | `ab5975120d8c10d5de422bfe6eb0056af7a762ce7e57d67c8529987e858dd72a` |

```bash
curl -L -o lvgl-9.3.0.zip          https://github.com/lvgl/lvgl/archive/refs/tags/v9.3.0.zip
curl -L -o Arduino_GFX-1.6.0.zip   https://github.com/moononournation/Arduino_GFX/archive/refs/tags/v1.6.0.zip
# esp_lcd_jd9365 comes from the Espressif component registry, not GitHub releases:
#   https://components.espressif.com/components/espressif/esp_lcd_jd9365/versions/2.0.2
```

⚠ A GitHub **tag zipball is not guaranteed byte-stable** across regeneration, so the two SHA-256
values above may not reproduce even though the *content* will. The commit hashes are the
reliable identity — they were read out of the zip archive comments, which is where GitHub
records them. `esp_lcd_jd9365-2.0.2.zip` carries no such comment; its identity is the registry
version plus the `repository_info.commit_sha` in its own `idf_component.yml`,
`bd85f52467353dae3bd5f551054795287b0042a4` in `espressif/esp-iot-solution`.
