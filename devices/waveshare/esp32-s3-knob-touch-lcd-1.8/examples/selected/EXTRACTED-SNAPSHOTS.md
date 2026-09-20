# `selected/` — extracted community projects, provenance record

> Tarballs extracted and verified **2026-08-24**. Compiled from
> [`../catalog.md`](../catalog.md); machine-readable metadata in [`../catalog.json`](../catalog.json).

Four `*.tar.gz` snapshots of community GitHub repositories were extracted in place. **Both the
tarball and the extraction are kept for all four** — the largest is 128 KB, so the duplication
costs ~163 KB in total and buys greppable, diffable source trees alongside byte-exact originals.

## Verification performed

Every tarball's origin URL was re-probed on 2026-08-24 against `codeload.github.com` using the
pinned commit. **All four returned HTTP 200 with a byte count exactly equal to the local file** —
which, given GitHub generates these tarballs on demand, is strong evidence the pinned commits
still resolve to the same trees.

> ⚠️ **Caveat, stated rather than glossed over:** GitHub's auto-generated tarballs are *not*
> guaranteed byte-stable over time (gzip settings and tar metadata have changed historically).
> Size equality was confirmed; full SHA-256 equality of a freshly downloaded tarball was **not**
> re-verified. If you need a cryptographically pinned source, use `git clone` + `git checkout
> <full-sha>` — the full 40-character SHAs are recorded below precisely for that purpose.

## Document scan

**All four trees were scanned for PDFs, datasheets, `.doc`/`.docx`, schematics and any other
documentation. None was found in any of them.** Consequently **nothing was moved** out of these
trees and **no component records were created** from them. Contents are source code, build
configuration, licences, `README.md` files, and — in one case — three PNG screenshots.

The only files with documentary weight are the four `README.md`s, which stay with their source
where they belong; their substantive claims are already extracted and critically assessed in
[`../catalog.md`](../catalog.md).

---

## 1. `esp32-s3-knob-hardware-explorer`

| Field | Value |
|---|---|
| Tarball | `esp32-s3-knob-hardware-explorer.tar.gz` |
| Tarball size | **16,177 bytes** |
| Tarball SHA-256 | `45ce115ab9f3e1417c3cdf70f3f28f2559aca8f7ed3f66eea9aedf9565a52b97` |
| Extracted to | `esp32-s3-knob-hardware-explorer-87602cacde/` |
| Extracted size | **46,417 bytes** across **10 files** (15 tar members incl. 5 directories) |
| Extracted tree digest | `f6e7524727354c0a636b283d6dff144059b4b285e1d9fb53ced0fb16a40b80bb` |
| Upstream repo | <https://github.com/IngoDuesentrieb/esp32-s3-knob-hardware-explorer> |
| Pinned commit | **`87602cacdecd95a34df91742df3c66192999dfe9`** (short `87602cacde`) |
| Commit date | **2026-05-04T08:24:55Z** |
| Commit subject | *"v0.4: LVGL v9.5 + Arduino_GFX läuft auf ST77916 QSPI 360x360"* |
| Author | **Ingo Hoffmann** (`IngoDuesentrieb`) |
| Repo last push | 2026-05-10T09:45:52Z · 1 star |
| License | **MIT** — `LICENSE` file present, `Copyright (c) 2026 Ingo Hoffmann`. GitHub SPDX: `MIT` ✅ |
| Redistribution status | `allowed` (MIT) |

Notable: `boards/waveshare_knob_18.json` — a PlatformIO board definition for this product.
The commit subject asserts **ST77916 QSPI at 360×360**, which is the opposite side of the
ST77916-vs-SH8601 dispute from entry 4 below. Both are pinned here; neither is resolved.

## 2. `lvgl_kawaii_face`

| Field | Value |
|---|---|
| Tarball | `lvgl_kawaii_face.tar.gz` |
| Tarball size | **16,362 bytes** |
| Tarball SHA-256 | `37b99e6162ea72990565ddf6800abc45a92066424ac0d95ec6c053a3931c7abc` |
| Extracted to | `lvgl_kawaii_face-d58e1c8f8e/` |
| Extracted size | **86,900 bytes** across **9 files** (14 tar members incl. 5 directories) |
| Extracted tree digest | `04007737871134bd3d7b8d66055db2d106a20c9336932958579a70f86b4d04ef` |
| Upstream repo | <https://github.com/0015/lvgl_kawaii_face> |
| Pinned commit | **`d58e1c8f8e7baa7bc93d5ae0dc18affee7f3ccbb`** (short `d58e1c8f8e`) |
| Commit date | **2026-02-27T04:55:38Z** |
| Commit subject | *"Upload for ESP Component"* |
| Author | **Eric N.** (`0015`, "That Project") |
| Repo last push | 2026-02-27T05:05:05Z · **26 stars** — the most-starred of the four |
| License | **MIT** — `LICENSE` file present, `Copyright (c) 2026 Eric`. GitHub SPDX: `MIT` ✅ |
| Redistribution status | `allowed` (MIT) |

A properly packaged ESP-IDF component (`idf_component.yml`, `CMakeLists.txt`) with a runnable
`examples/basic_cycle`. Not board-specific.

## 3. `lyngdorf-secondary-sleep`

| Field | Value |
|---|---|
| Tarball | `lyngdorf-secondary-sleep.tar.gz` |
| Tarball size | **2,494 bytes** |
| Tarball SHA-256 | `4573318c178b23f29179c4296fc0c259aac2c2167eda899b21b06ae2280b56da` |
| Extracted to | `lyngdorf-secondary-sleep-dfc372fb07/` |
| Extracted size | **4,202 bytes** across **7 files** (11 tar members incl. 4 directories) |
| Extracted tree digest | `fede1757b92315596469cd0c9e6d114ca4ae3418f0cc87a96e43f42583e30f5b` |
| Upstream repo | <https://github.com/svwhisper/lyngdorf-secondary-sleep> |
| Pinned commit | **`dfc372fb07f2a1c1f461bc291fd3f35ee6f26c64`** (short `dfc372fb07`) |
| Commit date | **2026-05-10T21:31:48Z** |
| Commit subject | *"Add GitHub Actions release workflow"* |
| Author | **svwhisper** |
| Repo last push | 2026-05-10T21:31:56Z · 0 stars |
| License | ⚠️ **MIT is stated in `README.md` but there is NO `LICENSE` file.** GitHub API reports `none`. Re-confirmed 2026-08-24 |
| Redistribution status | **`unclear`** — a README assertion is weaker than a licence file. Treat as unlicensed until the author adds one |

The smallest and, per [`../catalog.md` §1.2](../catalog.md), among the most valuable: the only
ESP32-U4WDH source located anywhere, quantifying the secondary MCU's ~50 mA idle draw and the
~10 µA achievable after flashing deep-sleep.

## 4. `Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test`

| Field | Value |
|---|---|
| Tarball | `Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test.tar.gz` |
| Tarball size | **128,227 bytes** |
| Tarball SHA-256 | `2b8fc74175bc801699070c4165cd12160f3c481562a142834cad2249d09c9d19` |
| Extracted to | `Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test-3cd890b473/` |
| Extracted size | **160,759 bytes** across **10 files** (12 tar members incl. 2 directories) |
| Extracted tree digest | `125fb7c0548f5a8c05cb66ab11f9f1faa0585078183235a510b5d83603b1459a` |
| Upstream repo | <https://github.com/UnkMihai/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test> |
| Pinned commit | **`3cd890b4734a51ef0d0c0809916ec3517c1a9fdc`** (short `3cd890b473`) |
| Commit date | **2026-02-20T01:29:55Z** |
| Commit subject | *"Fix compilation errors: isolate ESP-IDF headers + drv.go()"* |
| Author | **UnkMihai** |
| Repo last push | 2026-02-20T01:31:25Z · 0 stars |
| License | ⚠️ **MIT is stated in `README.md` but there is NO `LICENSE` file.** GitHub API reports `none`. Re-confirmed 2026-08-24 |
| Redistribution status | **`unclear`** — same caveat as entry 3 |

The only entry containing images: `images/pattern_color_bars.png` (45,881 B),
`images/pattern_gradient.png` (41,187 B), `images/pattern_red.png` (31,364 B) — **photographs of
test patterns on the panel, i.e. results, not documentation.** They are 74% of the tree by size
and are left in place. They were checked and are not schematics or datasheets.

> ⚠️ **Read [`../catalog.md` §1.4](../catalog.md) before trusting this repo's pin table.** Its
> README describes a *different Waveshare product* (a 1.85" round AMOLED, `H0185Y040X`). The
> display parameters cross-check against our board; the encoder and `POWER_EN` pins do not.

---

## Tree content digest definition

```bash
d=lyngdorf-secondary-sleep-dfc372fb07   # etc.
find "$d" -type f -exec sha256sum {} + | sed "s|  $d/|  |" | sort -k2 | sha256sum
```

Computed over the trees exactly as extracted; nothing has been added, removed or renamed.

## Reacquire — all four

```bash
# Source 1 — GitHub codeload, pinned to the commit (this is how the local tarballs were made).
#            All four probed 2026-08-24: HTTP 200, byte count == local file size.
curl -L -o esp32-s3-knob-hardware-explorer.tar.gz \
  https://codeload.github.com/IngoDuesentrieb/esp32-s3-knob-hardware-explorer/tar.gz/87602cacde
curl -L -o lvgl_kawaii_face.tar.gz \
  https://codeload.github.com/0015/lvgl_kawaii_face/tar.gz/d58e1c8f8e
curl -L -o lyngdorf-secondary-sleep.tar.gz \
  https://codeload.github.com/svwhisper/lyngdorf-secondary-sleep/tar.gz/dfc372fb07
curl -L -o Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test.tar.gz \
  https://codeload.github.com/UnkMihai/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test/tar.gz/3cd890b473

# Source 2 — equivalent github.com archive URLs (redirect to codeload)
#   https://github.com/<owner>/<repo>/archive/<full-sha>.tar.gz

# Source 3 — git, pinned to the FULL commit SHA (the only cryptographically stable option)
git clone https://github.com/IngoDuesentrieb/esp32-s3-knob-hardware-explorer
git -C esp32-s3-knob-hardware-explorer checkout 87602cacdecd95a34df91742df3c66192999dfe9
git clone https://github.com/0015/lvgl_kawaii_face
git -C lvgl_kawaii_face checkout d58e1c8f8e7baa7bc93d5ae0dc18affee7f3ccbb
git clone https://github.com/svwhisper/lyngdorf-secondary-sleep
git -C lyngdorf-secondary-sleep checkout dfc372fb07f2a1c1f461bc291fd3f35ee6f26c64
git clone https://github.com/UnkMihai/Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test
git -C Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test checkout 3cd890b4734a51ef0d0c0809916ec3517c1a9fdc
```

## Verify

```bash
sha256sum *.tar.gz
# 45ce115ab9f3e1417c3cdf70f3f28f2559aca8f7ed3f66eea9aedf9565a52b97  esp32-s3-knob-hardware-explorer.tar.gz
# 37b99e6162ea72990565ddf6800abc45a92066424ac0d95ec6c053a3931c7abc  lvgl_kawaii_face.tar.gz
# 4573318c178b23f29179c4296fc0c259aac2c2167eda899b21b06ae2280b56da  lyngdorf-secondary-sleep.tar.gz
# 2b8fc74175bc801699070c4165cd12160f3c481562a142834cad2249d09c9d19  Waveshare-ESP32-S3-Knob-Touch-LCD-1.8-first-successful-screen-test.tar.gz

# If a re-downloaded tarball's hash differs, do NOT assume tampering — compare the
# *extracted trees* instead, which is what the tree digests above are for:
tar xzf lyngdorf-secondary-sleep.tar.gz
find lyngdorf-secondary-sleep-dfc372fb07 -type f -exec sha256sum {} + \
  | sed 's|  lyngdorf-secondary-sleep-dfc372fb07/|  |' | sort -k2 | sha256sum
# expect fede1757b92315596469cd0c9e6d114ca4ae3418f0cc87a96e43f42583e30f5b
```

## Also in this directory

`BlueKnob-c71c98ff5b/` and `blueknob-vendored-deps/` were processed in an earlier pass and are
**not** covered by this record. See [`../catalog.md` §1.3](../catalog.md) and the
`blueknob-vendored-deps/` README. Note that BlueKnob is the only one of the five with a real,
file-backed **Apache-2.0** licence.

## Recommended, not done

1. **Ask the two README-only-MIT authors** (`svwhisper`, `UnkMihai`) to add `LICENSE` files.
   Until then those two trees are, strictly, unlicensed — which matters if anything here is ever
   republished.
2. **Submit all four repo URLs to `https://web.archive.org/save/`.** Three of the four have 0–1
   stars and a single author; personal repositories of that profile disappear.
3. **Resolve the ST77916-vs-SH8601 conflict.** Entry 1's commit message claims ST77916 QSPI works
   at 360×360; entry 4 argues from firmware binary analysis for SH8601. Both are now checked in
   with pinned commits, so a side-by-side reading is possible without further downloads. Tracked
   in `../../gaps-and-conflicts.md`.
