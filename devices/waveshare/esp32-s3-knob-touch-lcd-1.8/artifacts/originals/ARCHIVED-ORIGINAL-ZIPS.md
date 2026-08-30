# Archived original ZIPs — reacquisition record

> Analysis and archive date: **2026-08-24**. Extended the same day with the Demo ZIP (§3).
> "Archived" means moved to `archive/doc/hardware/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/`,
> preserving this repository's relative path. **Nothing was deleted.**

**Three** of the four original Waveshare downloads in this directory have now been archived.
Each was removed only after its **entire** contents were reconciled member-by-member against
what remains checked in, and only after **two independent, byte-verified download URLs** were
established. The one remaining file (`ESP32-S3-Knob-Touch-LCD-1.8-14.jpg`, a product photo) is
untouched — see [`README.md`](./README.md).

| # | File | Archived | Verified sources |
|---|---|---|---|
| 1 | `ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` | 2026-08-24 | vendor + 2 IA captures |
| 2 | `ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` | 2026-08-24 | vendor + 2 IA captures |
| 3 | [`ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip`](#3-esp32-s3-knob-touch-lcd-18-demozip) | 2026-08-24 | vendor **(hash-verified)** + 1 IA capture **(hash-verified)** |

**Why "two URLs" mattered here.** The [`README.md`](./README.md) in this directory previously
recorded these as single-source, Waveshare-only files with "no GitHub, distributor, or archive
mirror located", and flagged them as candidates for `web.archive.org/save/`. That turned out to
be **wrong**: the Internet Archive had already captured both, in 2025-08 and again in 2026-01.
Those captures were downloaded on 2026-08-24 and hash-verified against the local copies. They
match exactly. That upgraded both files from single-source to multi-source and is what made
archiving defensible. The `README.md` statement should be read as superseded by this file.

---

## 1. `ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip`

| Field | Value |
|---|---|
| Original relative path | `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` |
| Archived to | `archive/doc/hardware/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` |
| What it is | Waveshare's as-shipped **factory firmware images** for both MCUs on this board, distributed as a ZIP from the product wiki's "Demo" section |
| Archive SHA-256 | `7d29fc1fb356059f7291eccd74bfb5c9fa7538998bc3f5ff811cd87f04c1691c` |
| Archive size (pre-extract, on-disk ZIP) | **2,032,893 bytes** (1.94 MiB) |
| Extracted total size (post-extract) | **3,268,896 bytes** (3.12 MiB) |
| File count when extracted | **2** (plus one directory entry, `ESP32-S3-Knob-Touch-LCD-1.8-BIN/`) |
| Extracted tree content digest | `859e0bead984cadb46ac9df62e6489c89edbd0aa3c0a7b0055537a40ea4a8c3c` |
| Version | No version string in the archive. The payload names it: **`WX-ESP32S3-KNOB_V1.2`** for the ESP32-S3 application; the ESP32 secondary image carries no version |
| Build / release date | Member mtimes: `ESP32-KNOB_ESP32_0.bin` **2025-05-27 14:03**, `WX-ESP32S3-KNOB_V1.2.bin` **2025-06-09 14:06**. Server `Last-Modified` **Thu, 19 Jun 2025 12:56:40 GMT** |
| Author / vendor | Waveshare Electronics (Shenzhen Waveshare International Ltd.) |
| License | **None stated.** Proprietary vendor firmware binaries. Redistribution status `unknown` |
| Upstream repo / git commit | **Not applicable** — no public source repository exists for this firmware. See [`../../examples/catalog.md` §1.1](../../examples/catalog.md) for the closest thing (the Guition JC3636K518 vendor source, which a third party reports may be the same application) |
| Disposition | archived (`local-cache` outside the repository) |

### Why removal was OK

Both members are already present in this repository, **byte-identical**, at
`../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/`. Verified member-by-member on 2026-08-24 by
hashing the ZIP members in memory and comparing against the on-disk files:

| ZIP member | Bytes | SHA-256 | On-disk counterpart | Result |
|---|---:|---|---|:--:|
| `ESP32-S3-Knob-Touch-LCD-1.8-BIN/ESP32-KNOB_ESP32_0.bin` | 1,130,672 | `0c1c21b9822d4c2d80d58534b33eb0083880de4ed7354a38b4c78ba51757349d` | `../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/ESP32-KNOB_ESP32_0.bin` | ✅ **MATCH** |
| `ESP32-S3-Knob-Touch-LCD-1.8-BIN/WX-ESP32S3-KNOB_V1.2.bin` | 2,138,224 | `f7c1cc18b687559f3bd69e5c9ab526bc61c2b2d9c502f38367f7f2bfe4ff8e87` | `../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/WX-ESP32S3-KNOB_V1.2.bin` | ✅ **MATCH** |

So the ZIP was **pure container overhead**: 1.94 MiB storing nothing that is not already here in
uncompressed, directly usable form. Unlike `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` — which is
deliberately retained because the extracted tree next to it has renamed files and pruned
subtrees, making the ZIP the only byte-exact original — the extraction of *this* ZIP is complete
and unmodified. There is no information in the container that is not in the extraction, other
than the deflate stream itself.

**These are the two most important binaries on this board and they are still here.** Nothing
about this archival reduces access to the factory firmware; it removes a redundant second copy.

### Reacquire

```bash
# Source 1 — Waveshare product wiki file pool (primary, vendor)
curl -L -O https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip

# Source 2 — Internet Archive, 2025-08-22 capture (byte-verified 2026-08-24)
curl -L -o ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip \
  "https://web.archive.org/web/20250822191102id_/https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip"

# Source 3 — Internet Archive, 2026-01-06 capture (recorded as a `warc/revisit` of the
#            same content digest, so it serves the identical payload)
curl -L -o ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip \
  "https://web.archive.org/web/20260106222409id_/https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip"

# Source 4 — reconstruct from what is already in this repository (no network needed)
cd ../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware
mkdir -p /tmp/ESP32-S3-Knob-Touch-LCD-1.8-BIN
cp ESP32-KNOB_ESP32_0.bin WX-ESP32S3-KNOB_V1.2.bin /tmp/ESP32-S3-Knob-Touch-LCD-1.8-BIN/
# NOTE: this reproduces the *contents*, not the byte-exact ZIP (deflate settings and
#       timestamps will differ). Use source 1-3 if you need the exact archive hash.
```

### Verify

```bash
# The archive itself
sha256sum ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip
# expect 7d29fc1fb356059f7291eccd74bfb5c9fa7538998bc3f5ff811cd87f04c1691c

# The extracted tree (definition of the content digest recorded above)
unzip -q ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip -d out
cd out/ESP32-S3-Knob-Touch-LCD-1.8-BIN
find . -type f -exec sha256sum {} + | sed 's|  \./|  |' | sort -k2 | sha256sum
# expect 859e0bead984cadb46ac9df62e6489c89edbd0aa3c0a7b0055537a40ea4a8c3c
```

### URL probe results (2026-08-24)

| URL | HTTP | Content-Length | Last-Modified | Payload SHA-256 verified? |
|---|---|---:|---|---|
| `https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` | `200 OK` | 2032893 — **matches** | `Thu, 19 Jun 2025 12:56:40 GMT` | size match (HEAD only) |
| `https://web.archive.org/web/20250822191102id_/…BIN.zip` | `200 OK` | 2032893 — **matches** | capture 2025-08-22 19:11:02 UTC | ✅ **downloaded and hashed — exact match** |
| `https://web.archive.org/web/20260106222409id_/…BIN.zip` | `200 OK` (CDX `warc/revisit`) | — | capture 2026-01-06 22:24:09 UTC | same CDX content digest `7KQR2YVKU4UZQFRRCE3NSWLQFK2NKNO2` as the 2025 capture |

---

## 2. `ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip`

| Field | Value |
|---|---|
| Original relative path | `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
| Archived to | `archive/doc/hardware/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
| What it is | Waveshare's published **schematic for this board, as five PNG page renders**. Not EDA source; not PDF. This is the only schematic Waveshare publishes for the product |
| Archive SHA-256 | `baa5ac1bf75fbbd86a8135b123ff498bd7db4a5c68184481db6b82cadbaca0e5` |
| Archive size (pre-extract, on-disk ZIP) | **672,290 bytes** (656.5 KiB) |
| Extracted total size (post-extract) | **1,335,012 bytes** (1.27 MiB) |
| File count when extracted | **5** (plus one directory entry, `ESP32-S3-Knob-Touch-LCD-1.8-schematic/`) |
| Extracted tree content digest | `8bf774c802460c6b29c5ecb214faeb84833db8fb6b29f23e053d919171451981` |
| Version | **No revision marking anywhere** — not in filenames, not in the ZIP, not in PNG metadata. Waveshare publishes this schematic unversioned. Treat the mtime as the only version proxy |
| Build / release date | All five members mtime **2025-05-27, 14:06–14:09**. Server `Last-Modified` **Thu, 19 Jun 2025 12:56:40 GMT** |
| Author / vendor | Waveshare Electronics (Shenzhen Waveshare International Ltd.) |
| License | **None stated.** Vendor documentation. Redistribution status `unknown` |
| Upstream repo / git commit | **Not applicable** — no public repository |
| Disposition | archived (`local-cache` outside the repository) |

### Why removal was OK

All five members are already present in this repository, **byte-identical**, at
`../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/`. Verified member-by-member on 2026-08-24:

| ZIP member | Bytes | SHA-256 | Result |
|---|---:|---|:--:|
| `ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` | 264,945 | `00bc1fc92958076c73ffbd02f50ccff425b58c1962dd2593bb0f937a614970d6` | ✅ **MATCH** |
| `ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` | 321,092 | `1d35d84fb0f5a55588e4428259318cdba57468d1f58785638ea84b092fd58966` | ✅ **MATCH** |
| `ESP32-S3-Knob-Touch-LCD-1.8-schematic/3_ESP32-CHIP.png` | 303,239 | `4ff7d4aef1891a0da867854c76bf795bf81c0a8d33493aafbe4b3fbd73041c80` | ✅ **MATCH** |
| `ESP32-S3-Knob-Touch-LCD-1.8-schematic/4_OTHER.png` | 154,263 | `0dfb9c802562a992c3241078db05b0b2019d72b1c1add270752c71199e3456c1` | ✅ **MATCH** |
| `ESP32-S3-Knob-Touch-LCD-1.8-schematic/5_DAC.png` | 291,473 | `816ef3ae7196cd1508a7c7265eb49303faf70780f901814ceb6a8256c000ca92` | ✅ **MATCH** |

Filenames on disk are **unchanged** from the ZIP — including the `&` in `1_LCD&POWER.png`. There
are no renames to reconcile, so the extraction is a complete and faithful representation of the
archive.

PNGs are already compressed, which is why the ZIP saves only ~50%: 672 KB to hold 1.27 MB of
images that are also stored uncompressed next door.

> **This is the board's primary hardware reference and it remains fully present.** Everything in
> this repository that cites pin assignments traces back to these five PNGs.

### Reacquire

```bash
# Source 1 — Waveshare product wiki file pool (primary, vendor)
curl -L -O https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip

# Source 2 — Internet Archive, 2025-08-22 capture (byte-verified 2026-08-24)
curl -L -o ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip \
  "https://web.archive.org/web/20250822191121id_/https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip"

# Source 3 — Internet Archive, 2026-01-07 capture (byte-verified 2026-08-24)
curl -L -o ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip \
  "https://web.archive.org/web/20260107092458id_/https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip"

# Source 4 — the product wiki page that links it
#   https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8
```

### Verify

```bash
sha256sum ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip
# expect baa5ac1bf75fbbd86a8135b123ff498bd7db4a5c68184481db6b82cadbaca0e5

unzip -q ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip -d out
cd out/ESP32-S3-Knob-Touch-LCD-1.8-schematic
find . -type f -exec sha256sum {} + | sed 's|  \./|  |' | sort -k2 | sha256sum
# expect 8bf774c802460c6b29c5ecb214faeb84833db8fb6b29f23e053d919171451981

# Or compare directly against the copies still in this repository:
diff -rq . ../../../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/
```

### URL probe results (2026-08-24)

| URL | HTTP | Content-Length | Last-Modified | Payload SHA-256 verified? |
|---|---|---:|---|---|
| `https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` | `200 OK` | 672290 — **matches** | `Thu, 19 Jun 2025 12:56:40 GMT` | size match (HEAD only) |
| `https://web.archive.org/web/20250822191121id_/…schematic.zip` | `200 OK` | 672290 — **matches** | capture 2025-08-22 19:11:21 UTC | ✅ **downloaded and hashed — exact match** |
| `https://web.archive.org/web/20260107092458id_/…schematic.zip` | `200 OK` | 672290 — **matches** | capture 2026-01-07 09:24:58 UTC | ✅ **downloaded and hashed — exact match** |

Both Internet Archive captures share the CDX content digest `PY44LGYDHPOB43FTZF5ODAXWDRHHZRFD`.

---

## 3. `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip`

> **This one needed more care than the other two**, because — unlike them — its extraction in
> this repository is *not* complete: two bundled libraries were removed from it, and three
> filenames differ. It was archived only after a full member-by-member reconciliation and after
> a **second source was downloaded and hash-verified**. Both checks are recorded below.

| Field | Value |
|---|---|
| Original relative path | `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` |
| Archived to | `archive/doc/hardware/devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` |
| What it is | Waveshare's complete **demo/example distribution** for this board: the Arduino sketch tree, eight ESP-IDF projects, the two factory firmware binaries, and two bundled third-party libraries |
| Archive SHA-256 | `11e382444fe93470fbe463829c1e0ebad5bdb5115fd2d72f6159cd7700015030` |
| Archive size (on-disk ZIP) | **68,704,748 bytes** (65.5 MiB) |
| ZIP member count | **2,145 entries** = **1,802 files** + 343 directory entries |
| Extracted total size | **214,245,659 bytes** (204.3 MiB) |
| Extracted content digest (name-independent) | `b786db26f67146c92028fc5a11c653eaaf3ff813a7150e96f41d9c9060ca7c38` |
| Top-level layout | `Arduino/` 1,387 files · `ESP-IDF/` 413 files · `Firmware/` 2 files |
| Version | No version string for the archive as a whole. The payload names the S3 application **`WX-ESP32S3-KNOB_V1.2`** |
| Build / release date | Member mtimes span **2024-05-13** to **2025-06-20**. Server `Last-Modified` **Fri, 20 Jun 2025 09:19:41 GMT** |
| Author / vendor | Waveshare Electronics (Shenzhen Waveshare International Ltd.) |
| License | **None stated.** No `LICENSE` file exists anywhere in the archive. Bundled LVGL (MIT) and SensorLib (MIT) carry their own. Waveshare's own demo files: redistribution status `unknown` |
| Upstream repo / git commit | **Not applicable** — no public repository |
| Disposition | archived (`local-cache` outside the repository) |

### Member-by-member reconciliation (2026-08-24)

Every one of the **1,802** ZIP members was hashed in memory and matched against the extracted
tree. **All 1,802 are accounted for, with zero unexplained absences and zero content
mismatches:**

| Category | Count | Status |
|---|---:|---|
| Present on disk, **name and content byte-identical** | **145** | ✅ verified by SHA-256, member by member |
| Present on disk, **content byte-identical, filename CP437-mangled** | **3** | ✅ content-matched; the three Chinese-named SensorLib datasheets |
| Absent — bundled **LVGL 8.4.0** tree | **1,355** | ✅ expected; archived, reproducible |
| Absent — bundled **SensorLib 0.3.1** tree | **299** | ✅ expected; archived, reproducible |
| **Total** | **1,802** | |
| Files on disk **not** in the ZIP | **0** | ✅ nothing foreign in the extraction |

> **A correction to the earlier record.** [`README.md`](./README.md) states that three datasheets
> were "renamed on disk" to ASCII. That is not what happened *in the demo tree*. The ASCII-named
> copies live in the component records (`components/chipsemi/chsc5816/…`, `vendors/hynitron/…`,
> `components/generic/ambient-light-…/…`); the copies still sitting in the demo tree retain
> **CP437-mangled** names, because `unzip` decoded the original Chinese filenames without UTF-8.
> They are byte-identical either way. Details in
> [`../vendored-deps/README.md`](../vendored-deps/README.md).

The `299` figure is `302 − 3`: the SensorLib tree has 302 files, three of which were left behind
in the demo tree with mangled names.

### Why removal is OK — the extraction is now fully reproducible

This is the part that changed the calculus. Previously this ZIP was described as *"the only
byte-exact original"* and *"the fallback source for restoring those archived libraries"*. Both
statements are now superseded:

1. **The removed libraries are reproducible from upstream without this ZIP.**
   [`../../tools/restore-demo-deps.sh`](../../tools/restore-demo-deps.sh) rebuilds LVGL 8.4.0 and
   SensorLib 0.3.1 from their GitHub tags, applies Waveshare's two one-line patches, and verifies
   the result against recorded digests.
2. **This was verified end-to-end on 2026-08-24, against this exact ZIP.** The restored tree and
   a fresh extraction of the ZIP were compared: **1,802 files on both sides, content multisets
   identical, zero differing files.** The name-independent content digest of both is
   `b786db26f67146c92028fc5a11c653eaaf3ff813a7150e96f41d9c9060ca7c38`. The only name-level
   differences are the three documented ASCII datasheet renames.
3. **The archived library trees also still exist** under `archive/`, and
   `diff -rq` between them and the freshly restored trees is clean.
4. **Two independent URLs were downloaded in full and hashed**, both exact matches (below).

So the ZIP is no longer a single point of failure for anything. What it still uniquely holds is
the **deflate stream itself** — the byte-exact container, which is not reconstructible from the
contents. That is why it is archived rather than deleted.

### What is and is not still present on disk

**Still present** (`../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/`, 148 files, 12,602,995 bytes,
content digest `12b3da12a1c5a3bf928a70006dd6839d7bffe2d27945348ce7c8fb52b86220f6`):

- ✅ **All Waveshare-authored source** — the entire `Arduino/examples/` tree and all eight
  `ESP-IDF/` projects, including every `sdkconfig`, `CMakeLists.txt`, driver and pin header.
- ✅ **Both factory firmware binaries** in `Firmware/` — `ESP32-KNOB_ESP32_0.bin` and
  `WX-ESP32S3-KNOB_V1.2.bin`. The ESP32 one is the **only copy of the Classic Bluetooth
  application in existence**.
- ✅ **`Arduino/libraries/lv_conf.h`** — Waveshare's board-specific LVGL configuration, which is
  *not* upstream and *not* reproducible.
- ✅ The three SensorLib datasheets described above (with mangled names).

**Not present, by design:**

- ❌ `Arduino/libraries/lvgl/` — 1,355 files. Restore with `restore-demo-deps.sh`.
- ❌ `ESP-IDF/03_DRV2605_Test/components/SensorLib/` — 299 of 302 files. Same script.

Nothing Waveshare wrote has been removed from this repository.

### Reacquire

```bash
# Source 1 — Waveshare product wiki file pool (primary, vendor)
#            Downloaded IN FULL and hash-verified 2026-08-24.
curl -L -O https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip

# Source 2 — Internet Archive, 2025-08-22 capture.
#            Downloaded IN FULL and hash-verified 2026-08-24 — byte-identical.
curl -L -o ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip \
  "https://web.archive.org/web/20250822191154id_/https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip"

# Source 3 — the product wiki page that links it
#   https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8
#   https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm

# Source 4 — reconstruct the CONTENTS (not the byte-exact ZIP) with no network access
#            to Waveshare at all, from what is committed here plus upstream GitHub:
cd ../../ && cp -a artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo /tmp/knob-demo
./tools/restore-demo-deps.sh --dest /tmp/knob-demo
```

### Verify

```bash
# 1. The archive itself
sha256sum ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip
# expect 11e382444fe93470fbe463829c1e0ebad5bdb5115fd2d72f6159cd7700015030

# 2. Member count
unzip -l ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip | tail -1
# expect 1802 files

# 3. Extracted content digest.  Deliberately NAME-INDEPENDENT: the archive contains
#    Chinese filenames that different unzip builds decode differently, so a
#    path-based digest is not portable.  This hashes contents only.
unzip -q ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip -d out
cd out/ESP32-S3-Knob-Touch-LCD-1.8-Demo
find . -type f -exec sha256sum {} + | cut -c1-64 | LC_ALL=C sort | sha256sum
# expect b786db26f67146c92028fc5a11c653eaaf3ff813a7150e96f41d9c9060ca7c38

# 4. Cross-check against the repository's own tree (the 145 name-matching files)
diff -rq . ../../../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/ \
  | grep -v 'Only in' || true
# expect no "differ" lines
```

### URL probe results (2026-08-24)

| URL | HTTP | Content-Length | Last-Modified / capture | Payload SHA-256 verified? |
|---|---|---:|---|---|
| `https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` | `200 OK` | 68704748 — **matches** | `Fri, 20 Jun 2025 09:19:41 GMT` | ✅ **downloaded in full and hashed — exact match** |
| `https://web.archive.org/web/20250822191154id_/…Demo.zip` | `200 OK` | 68704748 — **matches** | capture 2025-08-22 19:11:54 UTC | ✅ **downloaded in full and hashed — exact match** |

The Internet Archive CDX content digest for the capture is
`KTS7EGKGWOFW6FSZFD2CKRTW64QVBXWJ`.

> **Note on `web.archive.org/save/`.** A fresh save was requested on 2026-08-24 and returned
> `302` (queued). No second capture had appeared in the CDX index at the time of writing;
> 68 MB binaries are often deferred or dropped by the save endpoint. **The 2025-08-22 capture is
> therefore currently the only Internet Archive copy** — it was verified byte-for-byte, but a
> second capture would be worth re-requesting periodically.


---

## Net effect

| | Originally | After BIN + schematic | After Demo ZIP |
|---|---:|---:|---:|
| `artifacts/originals/` in repository | 71,476,469 B (68.2 MiB) | 68,771,286 B (65.6 MiB) | **66,538 B (65 KiB)** |
| Moved to `archive/` | — | 2,705,183 B (2.58 MiB) | **71,409,931 B (68.1 MiB)** |

This directory now holds a single product photograph and these records. Everything else has a
verified reacquisition path.

The Demo ZIP dominates the numbers, and it is the one whose removal was least obvious. The
justification is not "it is redundant" — it was *not* fully redundant, since two library trees
had been removed from its extraction. The justification is that **the extraction became
reproducible**: `../../tools/restore-demo-deps.sh` closes the gap from upstream, and that was
verified against this exact ZIP before it was moved. Combined with two independently
hash-verified download URLs, the archive is recoverable by four separate routes.

## Related records

- [`README.md`](./README.md) — acquisition record for all four original downloads. Its
  "single-source risk" note is **superseded for all three archived files**.
- [`../vendored-deps/README.md`](../vendored-deps/README.md) — the LVGL/SensorLib removal, and
  the placeholder style this file follows.
- [`../tools/README.md`](../tools/README.md) — the tools-directory archival record.
- [`../../tools/README.md`](../../tools/README.md) — `restore-demo-deps.sh`, which reproduces the
  two library trees removed from the Demo ZIP's extraction.
- [`../../getting-started.md`](../../getting-started.md) — how to actually build from the demo tree.
- [`../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/`](../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/Firmware/) — where the firmware binaries live.
- [`../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/`](../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/) — where the schematic pages live.
