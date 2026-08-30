# BlueKnob — vendored dependencies and archived bulk

> Archive/removal date: **2026-08-23**.
> "Archived" means moved to
> `archive/hardware-doc/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/selected/`,
> preserving this repository's relative path. Nothing was deleted.

## What BlueKnob is

A community project targeting the Waveshare ESP32-S3-Knob-Touch-LCD-1.8 — a Bluetooth
media-control knob. It is the most substantial third-party application found for this board and
is retained as the flagship *integrated* example.

It contains three sub-projects plus hardware extras:

| Path | Purpose |
|---|---|
| `BlueKnob-ESP32S3/` | Main ESP-IDF application for the ESP32-S3 |
| `BlueKnob-ESP32/` | Companion firmware for the board's second MCU (ESP32-U4WDH, the Bluetooth audio side) |
| `BlueKnob-UI/` | SquareLine Studio UI project (`.spj`) |
| `extras/knob-grip-tpu.stl` | **3D-printable TPU knob grip** — original hardware design, not reproducible from anywhere else |
| `extras/backgrounds.pdn` | Paint.NET source for the UI backgrounds |

## Source identity

All fields below were confirmed against the GitHub API on **2026-08-23** (`HTTP 200`).

| Field | Value |
|---|---|
| Repository | **`joshuacant/BlueKnob`** — <https://github.com/joshuacant/BlueKnob> |
| Author | **Joshua Cantara** |
| Archive root directory | `BlueKnob-c71c98ff5b` |
| Commit (short) | `c71c98ff5b` |
| Commit (full SHA) | **`c71c98ff5bcdd6771085f73f4bd20b19471091cd`** |
| Commit date | **2025-10-05T16:50:02Z** |
| Commit message | `Update issue templates` |
| Default branch | `main` |
| Repository created | 2025-10-05T15:59:29Z |
| Last push | 2025-10-05T16:50:02Z (repo has not changed since this commit) |
| Releases/tags | None published |
| License | **Apache-2.0** (confirmed by API and by the `LICENSE` file header) |
| Stars / forks | 7 / 1 (as of 2026-08-23) |
| Original artifact | `BlueKnob.tar.gz`, 33,507,244 bytes (31.95 MiB) |
| Artifact form | GitHub auto-generated source tarball (no `.git/` directory present) |
| Extracted size | 105 MiB, 765 files |
| Redistribution status | **`allowed`** (Apache-2.0; preserve `LICENSE` and `NOTICE` if added upstream) |

`c71c98ff5b` is the **tip of `main`** — the repository's last push equals this commit, so the
archived snapshot is the complete current state of the project, not an arbitrary mid-history
point.

Reacquire:

```bash
# GitHub source tarball, pinned to the exact commit
curl -L -o BlueKnob.tar.gz \
  https://github.com/joshuacant/BlueKnob/archive/c71c98ff5bcdd6771085f73f4bd20b19471091cd.tar.gz
# equivalently via codeload
curl -L -o BlueKnob.tar.gz \
  https://codeload.github.com/joshuacant/BlueKnob/tar.gz/c71c98ff5bcdd6771085f73f4bd20b19471091cd
# or clone and pin (authoritative)
git clone https://github.com/joshuacant/BlueKnob.git
cd BlueKnob && git checkout c71c98ff5bcdd6771085f73f4bd20b19471091cd
```

Only **1 fork** exists as of 2026-08-23, and no non-GitHub mirror was found. With 7 stars and a
single-author history, this is a **low-redundancy source**: if the author deletes the repository
it may vanish. The archived tarball plus this record is therefore the primary safeguard, and the
repository is a good candidate for `https://web.archive.org/save/`.

> GitHub auto-generated tarballs are **not guaranteed byte-stable over time**, so the 33,507,244
> byte size and any hash of `BlueKnob.tar.gz` may not reproduce on a future download even at the
> same commit. The `git clone` + `git checkout` route is authoritative; the tarball is not.
> The archived copy is the only guaranteed-identical source for those exact bytes.

## What was pruned, and why

The extracted tree was **105 MiB**; after pruning it is **9.1 MiB, 141 files** — a 92% reduction
with no loss of BlueKnob's own work. Everything removed is either a stock third-party library or
regenerable output.

| Removed | Bytes | Files | Reason |
|---|---:|---:|---|
| `BlueKnob-ESP32S3/components/lvgl/` | 20,525,067 | 416 | Stock LVGL 8.4.0 + 3 small patches (captured) |
| `BlueKnob-ESP32S3/components/SensorLib/` | 21,602,498 | 182 | Stock SensorLib 0.3.1 + 2 small patches (captured) |
| `BlueKnob-ESP32S3/main/ui/images/ui_img_*.c` | ~48,860,000 | — | **Generated** C arrays exported by SquareLine Studio from the source images |
| `extras/backgrounds.pdn` | 7,790,000 | 1 | Paint.NET source for those images |

Tree content digests, computed **before** the move (reproducible with
`find . -type f -exec sha256sum {} + | sed 's|^\(.\{64\}\)  \./|\1  |' | sort -k2 | sha256sum`):

| Tree | Digest |
|---|---|
| `components/lvgl` | `dafe517263c9ceea9a8c070da1c08493904f7d1091e99b0ebde8a31aefcf6ba2` |
| `components/SensorLib` | `4c7606b3a6c7b94c08b5d5cba82d30bf217eb00dcfac1067ae6f035b73c350d0` |

### The `ui_img_*.c` files are regenerable, not authored

These are LVGL image C arrays produced by SquareLine Studio from `BlueKnob-UI/` and the Paint.NET
artwork. They were the single largest contributor (46.6 MiB of the tarball). Regenerate by
opening `BlueKnob-UI/*.spj` in SquareLine Studio and re-exporting, or by running LVGL's
`scripts/LVGLImage.py` / online image converter against the exported PNGs.

The `.spj` SquareLine project and the `.jpg` screenshots **were kept** — they are the inputs and
documentation, and they are small.

> **Paint.NET version required for `backgrounds.pdn`: unresolved.** `.pdn` is Paint.NET's native
> format and is Windows-only. The repository does not state which version produced it, and the
> format version was not read from the file header during this pass. Any reasonably recent
> Paint.NET (<https://www.getpaint.net/>) should open it, since the format is
> backward-compatible, but this is *inferred*, not verified.

## Vendored library analysis

Both bundled libraries are the **same versions** Waveshare's official demo ships — LVGL 8.4.0 and
SensorLib 0.3.1 — but they are **differently patched**. BlueKnob's patches are *not* Waveshare's
patches. Compare with
[`../../artifacts/vendored-deps/README.md`](../../../artifacts/vendored-deps/README.md).

All five deltas are preserved verbatim in [`patches/`](./patches/).

### LVGL 8.4.0 (BlueKnob's copy)

Distributed as an **ESP-IDF component-registry package**, not a GitHub release. Evidence: it
contains `CHECKSUMS.json` and `.component_hash`, which upstream's git tree does not. Both files
are preserved here as `lvgl-8.4.0-esp-component-CHECKSUMS.json` and
`lvgl-8.4.0-esp-component_hash` so the component-registry provenance can be re-verified.

Verified against upstream `v8.4.0` with `diff -rq`. Differences:

| File | Patch | Nature |
|---|---|---|
| `src/extra/libs/fsdrv/lv_fs_fatfs.c` | `lvgl-8.4.0-blueknob-src_extra_libs_fsdrv_lv_fs_fatfs.c.patch` | **Functional** — see below |
| `idf_component.yml` | `lvgl-8.4.0-blueknob-idf_component.yml.patch` | Component-registry metadata |
| `env_support/cmake/esp.cmake` | `lvgl-8.4.0-blueknob-env_support_cmake_esp.cmake.patch` | ESP-IDF build glue |

The `lv_fs_fatfs.c` patch adapts LVGL's FatFS driver to modern ESP-IDF, which renames FatFS's
`DIR` type to `FF_DIR` to avoid colliding with POSIX `DIR`:

```c
+typedef FIL file_t;
+typedef FF_DIR dir_t;
...
-    DIR * d = lv_mem_alloc(sizeof(DIR));
+    FF_DIR * d = lv_mem_alloc(sizeof(FF_DIR));
```

Without it, SD-card filesystem access through LVGL fails to compile. This is a **known, real
portability fix**, useful to anyone wiring LVGL to SD storage on this board — which is exactly
why it was worth extracting before archiving the tree.

### SensorLib 0.3.1 (BlueKnob's copy)

Verified against upstream `v0.3.1`. Differences:

| File | Patch |
|---|---|
| `src/SensorQMI8658.hpp` | `sensorlib-0.3.1-blueknob-src_SensorQMI8658.hpp.patch` |
| `src/REG/DRV2605Constants.h` | `sensorlib-0.3.1-blueknob-src_REG_DRV2605Constants.h.patch` |

Note the `DRV2605Constants.h` change is unique to BlueKnob — Waveshare's copy does **not** patch
that file. Since this board carries a **DRV2605L** haptic driver, this patch is directly relevant
to haptics work here. See [`components/texas-instruments/drv2605l/`](../../../../../../components/texas-instruments/drv2605l/).

### Restoring BlueKnob's exact build tree

```bash
# 1. Get the pruned tree from this repository, then:
cd BlueKnob-c71c98ff5b/BlueKnob-ESP32S3/components

# 2. LVGL 8.4.0 — prefer the ESP component registry to match the original distribution form
#    https://components.espressif.com/components/lvgl/lvgl/versions/8.4.0
#    or: git clone https://github.com/lvgl/lvgl.git && git -C lvgl checkout v8.4.0
for p in ../../../blueknob-vendored-deps/patches/lvgl-8.4.0-blueknob-*.patch; do
  patch -d lvgl -p1 < "$p"
done

# 3. SensorLib 0.3.1
#    git clone https://github.com/lewisxhe/SensorLib.git && git -C SensorLib checkout v0.3.1
for p in ../../../blueknob-vendored-deps/patches/sensorlib-0.3.1-blueknob-*.patch; do
  patch -d SensorLib -p1 < "$p"
done

# 4. Regenerate ui_img_*.c from BlueKnob-UI/*.spj via SquareLine Studio,
#    or copy them back from archive/
```

Upstream projects: <https://github.com/lvgl/lvgl> · <https://github.com/lewisxhe/SensorLib>

## Open questions

These are recorded as gaps rather than guessed:

1. Paint.NET version needed for `backgrounds.pdn` (format is backward-compatible, so any recent
   version should work, but this is inferred).
2. Whether BlueKnob's LVGL `lv_fs_fatfs.c` patch was authored by Joshua Cantara or copied from an
   upstream LVGL/ESP-IDF issue thread. The change matches a widely-discussed ESP-IDF FatFS
   `DIR`/`FF_DIR` collision, so independent authorship is unlikely but unconfirmed.
3. Which SquareLine Studio version produced `BlueKnob-UI/BlueKnob.spj`.
