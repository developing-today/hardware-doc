# Removed vendored dependencies — reacquisition record

> Scope: bundled third-party libraries that shipped inside `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip`
> and were removed from this repository because they are reproducible from upstream.
> Analysis and removal date: **2026-08-23**.

Nothing unique was lost. Both libraries are **unmodified upstream releases except for one
one-line patch each**, and both patches are preserved verbatim in [`patches/`](./patches/).
Restoring upstream and applying the patch reproduces Waveshare's tree byte-for-byte.

> **This is automated.** [`../../tools/restore-demo-deps.sh`](../../tools/restore-demo-deps.sh)
> downloads both upstream tags, verifies their hashes, applies both patches and checks the
> result against the digests below. Verified end-to-end on 2026-08-24 — the restored tree is a
> byte-identical reconstruction of all 1,802 files in the original demo ZIP. See
> [`../../tools/README.md`](../../tools/README.md).

Device-specific files that were *not* part of the upstream libraries were kept in place:

| File | Location (still present) | Why it matters |
|---|---|---|
| `lv_conf.h` | `../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/libraries/lv_conf.h` | Waveshare's LVGL build configuration for this board. Not upstream; not reproducible. |

---

## 1. LVGL 8.4.0

| Field | Value |
|---|---|
| Removed path | `artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Arduino/libraries/lvgl/` |
| Version | `8.4.0` (`LVGL_VERSION_MAJOR/MINOR/PATCH` in `lvgl.h`; `library.properties` `version=8.4.0`) |
| Upstream tag | `v8.4.0` |
| Upstream release date | 2024-03-19 (mtime of upstream sources in the release archive) |
| Waveshare copy mtime | 2025-03-05 |
| Removed tree size | 160,828,075 bytes (153.4 MiB) across 1,355 files |
| Tree content digest (`LC_ALL=C`) | `a5e84c30a760f8fecf68b3a2ea98386b11db95acf06af125876f4e51f634c47e` |
| Tree content digest (`en_US.UTF-8`, legacy) | `eab1941c863ee56c1b45b801fe5a135fd74a459d6cff52e6e9764fb839eae999` |
| License | MIT (`LICENCE.txt`, preserved here as `lvgl-8.4.0-LICENCE.txt`) |
| Redistribution status | `allowed` (MIT) |
| Disposition | `reference-only` — reproducible from upstream |
| Forked/modified by Waveshare? | **Yes, minimally.** One line added to `src/core/lv_refr.c`. See below. |

### Tree content digest definition

Run from the **parent** of the tree (`Arduino/libraries/` for LVGL,
`ESP-IDF/03_DRV2605_Test/components/` for SensorLib):

```bash
find <tree-name> -type f -exec sha256sum {} + | LC_ALL=C sort -k2 | sha256sum
```

> **⚠ `LC_ALL=C` matters, and the originally recorded digests omitted it.** `sort` is
> locale-sensitive and these trees contain filenames that order differently under `C` than under
> `en_US.UTF-8`, so the *same directory* hashes to two different values depending on the
> ambient locale. Both are given above. **Treat the `LC_ALL=C` value as canonical** — it is the
> portable, reproducible one, and it is what
> [`../../tools/restore-demo-deps.sh`](../../tools/restore-demo-deps.sh) checks.
> The legacy `en_US.UTF-8` values are retained only so the earlier records remain traceable.

### Waveshare's modification

`patches/lvgl-8.4.0-waveshare.patch` — forces the flush row height to an even number,
which the ST77916 panel requires when the display is rotated:

```c
lv_coord_t height = LV_MIN(max_row, area_h - row);
height &= ~0x1UL;                 /* <-- Waveshare addition */
```

This is a **functional fix, not cosmetic**. Any rebuild from stock upstream LVGL 8.4.0 without
this patch risks display tearing/offset artifacts in rotated rendering on this board.

### Other differences from upstream (both benign)

1. **Dotfiles stripped** by Waveshare's packaging: `.codecov.yml`, `.editorconfig`, `.github/`,
   `.gitignore`, `.pre-commit-config.yaml`, `scripts/.gitignore`, `tests/.gitignore`.
2. **`src/demos/` is a byte-identical duplicate of `demos/`**, added so the Arduino IDE compiles
   the demos (Arduino only builds sources under `src/`). This duplication alone accounted for
   roughly 60 MiB of the removed tree — the three ~9.4 MiB `img_lv_demo_music_cover_*_large.c`
   generated image files exist twice each.

Verified by `diff -rq` against upstream: apart from the seven dotfile paths, `src/demos`, and
`src/core/lv_refr.c`, **every file matched byte-for-byte**.

### Reacquire (multiple independent sources)

```bash
# Source 1 — GitHub release tarball (primary)
curl -L -o lvgl-8.4.0.zip https://github.com/lvgl/lvgl/archive/refs/tags/v8.4.0.zip
# sha256 of this archive as retrieved 2026-08-23:
#   28ff0b5b1e544f83b670533cd9bdf193df5c2260687af8a8ca48b737c937ca9f
# NOTE: GitHub auto-generated tarballs are not guaranteed byte-stable over time.
#       Prefer the git clone below if you need a cryptographically pinned source.

# Source 2 — git, pinned to the tag (most reliable)
git clone https://github.com/lvgl/lvgl.git && cd lvgl && git checkout v8.4.0

# Source 3 — Arduino Library Manager
arduino-cli lib install "lvgl@8.4.0"

# Source 4 — PlatformIO registry
pio pkg install --library "lvgl/lvgl@8.4.0"

# Source 5 — ESP-IDF component registry
#   https://components.espressif.com/components/lvgl/lvgl/versions/8.4.0

# Source 6 — the original Waveshare demo ZIP (see ../originals/README.md),
#   which contains this exact patched tree.
```

Then restore Waveshare's behaviour:

```bash
cd lvgl && patch -p1 < .../vendored-deps/patches/lvgl-8.4.0-waveshare.patch
# and, for Arduino builds only, recreate the demos duplication:
cp -r demos src/demos
```

Upstream project: <https://github.com/lvgl/lvgl> · <https://lvgl.io>

---

## 2. SensorLib 0.3.1

| Field | Value |
|---|---|
| Removed path | `artifacts/demo/.../ESP-IDF/03_DRV2605_Test/components/SensorLib/` |
| Version | `0.3.1` (`library.properties` `version=0.3.1`) |
| Upstream tag | `v0.3.1` |
| Author | Lewis He (`lewisxhe`) |
| Upstream source mtime | 2025-04-08 |
| Waveshare copy mtime | 2025-06-04 |
| Removed tree size | 43,501,941 bytes (41.5 MiB) across 302 files |
| Tree content digest (`LC_ALL=C`) | `a60fd281a66a027b0eefc37384c743125a23ff8dfc06b7436dd879b877ff1608` |
| Tree content digest (`en_US.UTF-8`) | `ac0c833502d2669f0e27b3d7778a742e8bce080e705724678f68ef794a60af4a` |
| Tree content digest, code only, no `datasheet/` (`LC_ALL=C`) | `2e5060efad5e2dfbb2fafd8bc0ddd33ef980895670480deb0d1efac31d30e6f6` (287 files, 25,301,012 bytes) |
| ~~Previously recorded digest~~ | ~~`efafe894cfdbe5bd396a148bce593e2750969c8cea052acb576463b9990165be`~~ — **superseded, see below** |
| License | MIT (`LICENSE`, preserved here as `sensorlib-0.3.1-LICENSE`) |
| Redistribution status | `allowed` (MIT) |
| Disposition | `reference-only` — reproducible from upstream |
| Forked/modified by Waveshare? | **Yes, minimally.** One `#include` added. See below. |

Note that `library.properties` gives the URL as `https://github.com/lewisxhe/SensorsLib`
(with an "s"), which is a **typo in upstream metadata**. The real repository is
`https://github.com/lewisxhe/SensorLib`.

### Waveshare's modification

`patches/sensorlib-0.3.1-waveshare.patch` — adds `#include <cmath>` to `src/SensorQMI8658.hpp`.
This is a build fix; without it the header fails to compile under the ESP-IDF toolchain version
Waveshare targeted.

### The `datasheet/` directory was NOT discarded

SensorLib bundles 15 component datasheets (17.9 MiB). These are **independent primary documents**,
several of which are genuinely scarce online (the Chinese-language Hynitron and Chipsemi
documents in particular). Rather than deleting them with the library, each was promoted into its
own reusable component record. See [Datasheet disposition](#datasheet-disposition) below.

### Other differences from upstream

Three datasheet files were renamed from their original Chinese filenames to portable ASCII.
Contents are byte-identical; only the names changed:

| Upstream filename | Renamed to |
|---|---|
| `CHSC5816触控芯片使用说明V1-20221114.pdf` | `CHSC5816-touch-controller-datasheet-v1-20221114.pdf` |
| `海栎创触摸芯片移植手册-v3.5-20220701(1).pdf` | `hynitron-touch-driver-guide-v3.5-20220701.pdf` |
| `环境光与接近传感器应用与选型.pdf` | `ambient-light-and-proximity-sensor-selection.pdf` |

Apart from these renames and `src/SensorQMI8658.hpp`, `diff -rq` against upstream showed
**every file matched byte-for-byte**.

### ⚠ Correction to the previously recorded digest (2026-08-24)

The value `efafe894…65be` recorded here on 2026-08-23 is **not reproducible** and has been
superseded. No digest recipe was recorded alongside it, and none of the plausible
reconstructions (any path prefix, either sort locale, either filename encoding, with or without
`datasheet/`) reproduces it. It appears to have been recorded in error.

**The tree itself is fine.** This was verified on 2026-08-24 by rebuilding it from upstream
`v0.3.1` + the patch + the three ASCII renames and running `diff -rq` against the archived
Waveshare copy: **identical, 302 files, 43,501,941 bytes** — which also matches the file count
and byte total recorded above. Only the digest string was wrong. The replacement values are
stated with an explicit recipe and locale so they can be checked.

### Three orphaned datasheet files remain in the repository

> **Updated 2026-08-30.** These three are **no longer regular files** — they are now **symlinks**
> into `shared-assets/`, pointing at the same bytes as the canonical component copies
> listed below. The reconciliation consequences described at the end of this section still apply,
> and the CP437 filenames are unchanged.

When SensorLib was archived, three PDFs were left behind in the otherwise-empty directory
`../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/ESP-IDF/03_DRV2605_Test/components/SensorLib/datasheet/`.
They carry **CP437-mangled filenames** — the result of `unzip` decoding the original Chinese
names without UTF-8 — which is why they did not move with the rest of the tree.

They are byte-identical duplicates of three files already promoted into component records:

| Mangled name (on disk) | SHA-256 | Canonical copy |
|---|---|---|
| `CHSC5816…V1-20221114.pdf` | `670808e3…` | `components/chipsemi/chsc5816/artifacts/chsc5816-datasheet-v1-20221114-zh.pdf` |
| `…-v3.5-20220701(1).pdf` | `0e9a0c42…` | `vendors/hynitron/artifacts/hynitron-touch-driver-porting-guide-v3.5-20220701-zh.pdf` |
| `…-.pdf` | `dc831848…` | `components/generic/ambient-light-and-proximity-sensor-selection/artifacts/…-zh.pdf` |

They are harmless but they are the reason the ZIP-to-disk reconciliation shows three name
mismatches, and the reason
[`../../tools/restore-demo-deps.sh`](../../tools/restore-demo-deps.sh) treats a `SensorLib/`
directory with no `src/` as a stub to be replaced rather than a corrupt install.

### Reacquire (multiple independent sources)

```bash
# Source 1 — GitHub release tarball (primary)
curl -L -o sensorlib-0.3.1.zip https://github.com/lewisxhe/SensorLib/archive/refs/tags/v0.3.1.zip
# sha256 as retrieved 2026-08-23:
#   99234b9296af8b5504aa6e3cf9828c93f25dde7ec852de4c42b82fad8ef7f808
# (GitHub auto-generated tarballs are not guaranteed byte-stable; prefer git.)

# Source 2 — git, pinned to the tag
git clone https://github.com/lewisxhe/SensorLib.git && cd SensorLib && git checkout v0.3.1

# Source 3 — Arduino Library Manager
arduino-cli lib install "SensorLib@0.3.1"

# Source 4 — PlatformIO registry
pio pkg install --library "lewisxhe/SensorLib@0.3.1"

# Source 5 — the original Waveshare demo ZIP (see ../originals/README.md)
```

Then:

```bash
cd SensorLib && patch -p1 < .../vendored-deps/patches/sensorlib-0.3.1-waveshare.patch
```

Upstream project: <https://github.com/lewisxhe/SensorLib>

---

## Datasheet disposition

Every PDF that shipped in `SensorLib/datasheet/` was retained, relocated to a reusable
component or vendor record, and is now discoverable independently of this device.

| Original filename | SHA-256 (prefix) | Bytes | New location |
|---|---|---|---|
| `BMA423.PDF` | `55fd9587` | 2,803,247 | `components/bosch-sensortec/bma423/artifacts/bma423-datasheet.pdf` |
| `CHSC5816-touch-controller-datasheet-v1-20221114.pdf` | `670808e3` | 950,989 | `components/chipsemi/chsc5816/artifacts/chsc5816-datasheet-v1-20221114-zh.pdf` |
| `CM32181A3OP.pdf` | `b4303a95` | 977,240 | `components/capella-microsystems/cm32181/artifacts/cm32181a3op-datasheet.pdf` |
| `CM32181 Application Note for Archtech.pdf` | `403cabd3` | 716,648 | `components/capella-microsystems/cm32181/artifacts/cm32181-application-note-archtech.pdf` |
| `DRV2605.pdf` | `c8248776` | 2,557,610 | `components/texas-instruments/drv2605/artifacts/drv2605-datasheet-slos825c-2014-09-26.pdf` |
| `GT911 Rev.10.pdf` | `ca79a4ba` | 1,467,494 | `components/goodix/gt911/artifacts/gt911-datasheet-rev-1.0.pdf` |
| `HYM8563.pdf` | `a3dac953` | 467,968 | `components/haoyu/hym8563/artifacts/hym8563-datasheet.pdf` |
| `hynitron-touch-driver-guide-v3.5-20220701.pdf` | `0e9a0c42` | 660,817 | `vendors/hynitron/artifacts/hynitron-touch-driver-porting-guide-v3.5-20220701-zh.pdf` |
| `LTR-553ALS-01.pdf` | `c27f435f` | 741,439 | `components/lite-on/ltr-553als-01/artifacts/ltr-553als-01-datasheet.pdf` |
| `PCF85063A.pdf` | `a09223db` | 726,288 | `components/nxp/pcf85063a/artifacts/pcf85063a-datasheet.pdf` |
| `PCF8563 Datasheet Rev.11.pdf` | `871273b1` | 495,457 | `components/nxp/pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf` |
| `QMC6310 Datasheet Rev.C.pdf` | `335dce94` | 884,797 | `components/qst/qmc6310/artifacts/qmc6310-datasheet-rev-c.pdf` |
| `QMI8658A Datasheet Rev A.pdf` | `bc371af1` | 3,085,534 | `components/qst/qmi8658a/artifacts/qmi8658a-datasheet-rev-a.pdf` |
| `XL9555 Datasheet Rev2.3.PDF` | `80ea36f9` | 589,855 | `components/xlsemi/xl9555/artifacts/xl9555-datasheet-rev-2.3.pdf` |
| `ambient-light-and-proximity-sensor-selection.pdf` | `dc831848` | 1,075,546 | `components/generic/ambient-light-and-proximity-sensor-selection/artifacts/ambient-light-and-proximity-sensor-selection-zh.pdf` |

**Important scoping caveat:** only the DRV2605 family and the Hynitron touch-driver guide relate
to parts actually fitted on the ESP32-S3-Knob-Touch-LCD-1.8. The remaining thirteen documents
cover other devices supported by SensorLib and are retained purely as reusable component
references. Do not infer from their presence that any of these parts is on this board.

Redistribution status for all fifteen is `unknown` — they are third-party manufacturer datasheets
redistributed by SensorLib under its MIT license, but MIT covers SensorLib's own code, **not**
these bundled third-party documents. They are kept unstaged pending review.
