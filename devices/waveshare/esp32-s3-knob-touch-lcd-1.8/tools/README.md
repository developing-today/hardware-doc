# `tools/` — developer scripts for this board

Scripts here are meant to be **run**, unlike `artifacts/tools/`, which holds vendor-supplied
utilities kept for the record.

| Script | Purpose |
|---|---|
| [`restore-demo-deps.sh`](./restore-demo-deps.sh) | Rebuild the two third-party libraries removed from the vendor demo tree, from upstream, verified |

---

## `restore-demo-deps.sh`

### What problem it solves

Waveshare's `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` bundles two third-party libraries inside the
demo tree. Together they are about **200 MiB** — roughly 90 % of the entire archive — and both
are ordinary upstream releases with a **single one-line vendor patch each**. Committing them
would mean storing 200 MiB of reproducible third-party code.

So they were removed, and this script puts them back **byte-for-byte**.

| Library | Version | Upstream tag | Restored to |
|---|---|---|---|
| **LVGL** | 8.4.0 | [`v8.4.0`](https://github.com/lvgl/lvgl/releases/tag/v8.4.0) | `Arduino/libraries/lvgl/` |
| **SensorLib** | 0.3.1 | [`v0.3.1`](https://github.com/lewisxhe/SensorLib/releases/tag/v0.3.1) | `ESP-IDF/03_DRV2605_Test/components/SensorLib/` |

Provenance, licensing and the full analysis:
[`../artifacts/vendored-deps/README.md`](../artifacts/vendored-deps/README.md).

### Requirements

`bash`, `curl`, `unzip`, `patch`, `sha256sum`, `find`, `sort`. Nothing else. No Python, no git,
no package manager.

### Usage

```sh
# The committed demo tree is deliberately kept WITHOUT these dependencies,
# and the script refuses to write into it. Work on a copy.
cp -a ../artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo ~/knob-demo

./restore-demo-deps.sh --dest ~/knob-demo
```

| Option | Effect |
|---|---|
| `--dest DIR` | **Required.** The demo-tree root — the directory containing `Arduino/` and `ESP-IDF/`. Created if absent |
| `--only lvgl` \| `--only sensorlib` | Restore just one of the two |
| `--no-datasheets` | Skip SensorLib's `datasheet/` directory: 15 PDFs, 17.9 MiB, **no effect on the build**. Verified against a separate code-only digest |
| `--force` | Replace an existing tree even if it fails verification |
| `--cache DIR` | Download cache. Default `$KNOB_DEPS_CACHE`, else `$TMPDIR/knob-demo-deps-cache` |
| `--allow-zip-drift` | Continue if the GitHub source archive hash differs (see [below](#on-github-archive-hash-drift)) |
| `-h`, `--help` | Usage |

### What it actually does

**LVGL**

1. Downloads `https://github.com/lvgl/lvgl/archive/refs/tags/v8.4.0.zip`, verifies SHA-256
   `28ff0b5b…ca9f`.
2. Removes the seven packaging dotfiles Waveshare's tooling stripped (`.codecov.yml`,
   `.editorconfig`, `.github/`, `.gitignore`, `.pre-commit-config.yaml`, `scripts/.gitignore`,
   `tests/.gitignore`). Required to reproduce the tree exactly.
3. Copies `demos/` to `src/demos/`. Waveshare did this because **the Arduino IDE only compiles
   sources under `src/`**. This duplication alone is ~60 MiB.
4. Applies `lvgl-8.4.0-waveshare.patch` — one line in `src/core/lv_refr.c` forcing the flush row
   height to an even number, which the rotated ST77916 panel requires. **This is a functional
   fix, not cosmetic**; stock upstream LVGL risks tearing/offset artifacts on this board.
5. Verifies: **1,355 files, 160,828,075 bytes**, tree digest
   `a5e84c30a760f8fecf68b3a2ea98386b11db95acf06af125876f4e51f634c47e`.

**SensorLib**

1. Downloads `https://github.com/lewisxhe/SensorLib/archive/refs/tags/v0.3.1.zip`, verifies
   SHA-256 `99234b92…f808`.
2. Applies `sensorlib-0.3.1-waveshare.patch` — adds `#include <cmath>` to
   `src/SensorQMI8658.hpp`. A build fix; without it the header fails to compile under the
   toolchain Waveshare targeted.
3. Renames three datasheets from Chinese filenames to portable ASCII (contents byte-identical;
   the names are not portable across filesystems and get mangled by `unzip` on many systems).
4. Verifies: **302 files, 43,501,941 bytes**, tree digest
   `a60fd281a66a027b0eefc37384c743125a23ff8dfc06b7436dd879b877ff1608`.
   With `--no-datasheets`: **287 files, 25,301,012 bytes**, digest
   `2e5060efad5e2dfbb2fafd8bc0ddd33ef980895670480deb0d1efac31d30e6f6`.

Both patches live in
[`../artifacts/vendored-deps/patches/`](../artifacts/vendored-deps/patches/).

### The tree-digest recipe

```sh
cd <parent-of-tree>
find <tree-name> -type f -exec sha256sum {} + | LC_ALL=C sort -k2 | sha256sum
```

> **`LC_ALL=C` is required.** `sort` is locale-sensitive, and these trees contain filenames
> whose ordering differs between `C` and `en_US.UTF-8`. The same directory yields a different
> digest under each. The values above are the **`LC_ALL=C`** ones, which are the portable and
> reproducible choice. See the note in
> [`../artifacts/vendored-deps/README.md`](../artifacts/vendored-deps/README.md) about the
> earlier, locale-dependent values.

### Behaviour

- **Idempotent.** If a target tree already exists and verifies, it is left alone and the script
  reports "nothing to do".
- **Fails loudly.** Any hash mismatch — source archive or restored tree — aborts non-zero with
  the expected and actual values printed. It will not report success on a tree it cannot vouch
  for.
- **Refuses to touch the repository.** `--dest` pointing at (or inside) this repo's own
  `artifacts/demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/` is rejected with an explanation. That tree
  is kept dependency-free on purpose.
- **Stub-aware.** The committed demo tree keeps three orphaned datasheet PDFs at the SensorLib
  path (they have CP437-mangled filenames and were left behind when the library was archived).
  A `SensorLib/` with no `src/`, or an `lvgl/` with no `lvgl.h`, is recognised as a stub and
  replaced rather than treated as a corrupt install.
- **Caches downloads**, and re-verifies the cache on each run.

### ⚠ `lv_conf.h` is not restored, and must not be moved

```
Arduino/libraries/lv_conf.h     <-- committed. board-specific. NOT restored by this script.
Arduino/libraries/lvgl/         <-- restored by this script.
```

`lv_conf.h` is **Waveshare's LVGL build configuration for this panel** — colour depth, buffer
strategy, enabled widgets, fonts. It is not an upstream LVGL file and cannot be regenerated from
the LVGL repository. It survived the dependency removal precisely because it sits one level
**above** `lvgl/`, which is where LVGL's build system looks for it.

Do not move it inside `lvgl/`; do not substitute upstream's `lv_conf_template.h`. If it goes
missing, copy it back from this repository. The script warns if it is absent from `--dest`.

### On GitHub archive hash drift

GitHub's auto-generated tag archives (`/archive/refs/tags/*.zip`) are **not guaranteed
byte-stable** — GitHub has changed its compression settings before, which changes the archive
hash without changing a single byte of content. If that happens here, the script aborts with an
explanation.

The **authoritative** check is the extracted-tree digest, which is content-only and immune to
recompression. To rely on it:

```sh
./restore-demo-deps.sh --dest ~/knob-demo --allow-zip-drift
```

The tree digest is still enforced, so this is safe: a genuinely tampered archive would fail at
that step.

For a cryptographically pinned source, use git instead:

```sh
git clone https://github.com/lvgl/lvgl.git      && git -C lvgl      checkout v8.4.0
git clone https://github.com/lewisxhe/SensorLib.git && git -C SensorLib checkout v0.3.1
```

### Verification status

Verified **2026-08-24** on Linux by restoring into `/tmp/knob-build-test/` and comparing the
result against the original `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip`:

- LVGL tree digest matched, 1,355 files, 160,828,075 bytes.
- SensorLib tree digest matched, 302 files, 43,501,941 bytes.
- `diff -rq` against the archived Waveshare trees: **identical**.
- Whole restored tree vs. the ZIP: **1,802 files on both sides, content multisets identical,
  zero files differing** — the only name-level differences are the three documented ASCII
  datasheet renames.
- Second run reported "nothing to do" (idempotency confirmed).
- `--no-datasheets` produced the expected 287-file tree with the patch applied.
- Pointing `--dest` at the repository's demo tree was correctly refused.

---

## Related

- [`../getting-started.md`](../getting-started.md) — the practical build guide; run this script first
- [`../artifacts/vendored-deps/README.md`](../artifacts/vendored-deps/README.md) — why the libraries were removed, and their provenance
- [`../artifacts/tools/README.md`](../artifacts/tools/README.md) — vendor-supplied utilities kept for the record
- [`../development.md`](../development.md) — the vendor toolchain version audit
