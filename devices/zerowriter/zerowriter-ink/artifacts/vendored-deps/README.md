# Removed vendored dependencies — reacquisition record

> Scope: bundled third-party libraries inside `artifacts/source-snapshots/` that were moved out of
> this repository because they are reproducible from upstream.
> Analysis and removal date: **2026-08-24**.

Nothing unique was lost. The one library removed is an **unmodified upstream Waveshare release
except for two files**, and both modifications are preserved verbatim in [`patches/`](./patches/)
and analysed in [`../../zerowriter1-epaper-driver-notes.md`](../../zerowriter1-epaper-driver-notes.md).

---

## 1. Waveshare `e-Paper` — Raspberry Pi / Jetson Nano Python driver library

| Field | Value |
|---|---|
| Removed path | `artifacts/source-snapshots/zerowriter1/e-Paper/` |
| Archived to | `archive/devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter1/e-Paper/` |
| What it is | Waveshare's official Python driver library + demo images for their whole e-paper module range, as vendored into the **ZeroWriter 1** (Raspberry Pi) project |
| Why it was here | ZeroWriter 1 is the Raspberry-Pi-based predecessor of ZeroWriter Ink. Its repository vendors this library wholesale; the snapshot was taken as-is. |
| Removed tree size | **32,575,902 B (31.07 MiB)** across **272 files** in 16 directories |
| Tree content digest (`LC_ALL=C`) | `4148d90638b2ec989fae68a070d1b8712c3184134aa322be026a7bc940ecf75b` |
| Tree content digest (`en_US.UTF-8`, for traceability only) | `91efa3c9e739f660239c14984f4d42f45fc351d1350d99f576ea539e887dba0d` |
| `RaspberryPi_JetsonNano/python` subtree digest (`LC_ALL=C`) | `241c11cb9d7f13296b508a4e7826b6d05a5f13e70998f38e35ef3fbea72d9385` |
| License | **MIT**, stated in the per-file header of every source file. Note there is **no repo-level `LICENSE` file** in `waveshareteam/e-Paper`. |
| Redistribution status | `allowed` (MIT) |
| Disposition | `reference-only` — byte-reproducible from two independent upstreams |
| Forked/modified? | **Yes, in exactly two files.** See below. |

### Tree content digest definition

Run from the **parent** of the tree (`artifacts/source-snapshots/zerowriter1/`):

```bash
find e-Paper -type f -exec sha256sum {} + | LC_ALL=C sort -k2 | sha256sum
```

> **`LC_ALL=C` matters.** `sort` is locale-sensitive and this tree contains Chinese-named files
> (`特别提醒.txt`) plus macOS `.DS_Store` / `._.DS_Store` dotfiles that order differently under
> `C` than under `en_US.UTF-8`. **Treat the `LC_ALL=C` value as canonical.**

### Upstream identity — two independent, verified reconstructions

**Source A — the ZeroWriter 1 repository itself (exact, preferred).**
The archived tree is a byte-identical copy of `e-Paper/` on the `main` branch of
`zerowriter/zerowriter1`. Verified 2026-08-24 by `diff -rq` of a fresh clone against the
snapshot: **zero differences across the entire repository**, including the `.DS_Store` files.

| Field | Value |
|---|---|
| Repository | <https://github.com/zerowriter/zerowriter1> |
| Branch | `main` |
| Commit | `e476d0567ac89104df62815f7bd2c807b8a3e140` |
| Commit subject | "Add MIT License to the project" |
| Author / date | Zerowriter `<152807354+zerowriter@users.noreply.github.com>`, 2026-05-19T14:58:55-04:00 |
| Last commit touching `e-Paper/` | `e94940ff9004d0d32ef7706006629dc65b4dd12e` — 2023-12-19, "Update main.py" |
| License | MIT (repo-level `LICENSE`, added in the HEAD commit) |

**Source B — Waveshare upstream + the two patches in [`patches/`](./patches/).**

| Field | Value |
|---|---|
| Upstream repository | <https://github.com/waveshareteam/e-Paper> (the older `waveshare/e-Paper` URL 301-redirects here) |
| Matched commit | `fc4f54334d087dae440e3e9ac2bf8d809dfcfb53` |
| Commit subject | "e-Paper" |
| Author / date | shhds `<1873145421@qq.com>`, 2023-06-12T15:10:45+08:00 |
| Vendored subset | **only** `RaspberryPi_JetsonNano/python/` — the `Arduino/`, `STM32/`, `E-paper_Separate_Program/` and `Arduino_R4/` trees were not vendored |
| Release date of matched state | 2023-06-12 (last `Version_EN.txt` entry: `2023-05-29: Added new programs 2.13inch e-Paper (G) routine.`) |

`diff -rq` of upstream `RaspberryPi_JetsonNano/python` at that commit against the vendored copy
reports **exactly two differing files** (both patched below). Everything else — including all 121
files in `pic/`, which are 30 MiB of the 31 MiB total — is **byte-identical to upstream**.

The remaining differences are pure add/remove, not content changes:

| Difference | Direction | Detail |
|---|---|---|
| 48 `examples/epd_*_test.py` demo scripts | present upstream, **absent** in the vendored copy | ZeroWriter pruned demos for panels it does not use |
| 5 `readme_*.txt` files | present upstream, **absent** in the vendored copy | `readme_jetson_*`, `readme_sunrise_*`, `readme_rpi_CN` pruned |
| `build/lib/waveshare_epd/` (51 files) | **added** locally | setuptools output — the tree was `pip install .`-ed in place |
| `dist/`, `lib/waveshare_epd.egg-info/` | **added** locally | more setuptools output |
| `examples/waveshare_epd/` (+ `__pycache__`) | **added** locally | an installed copy of `lib/waveshare_epd/` |
| `.DS_Store`, `._.DS_Store` | **added** locally | macOS Finder droppings, at two directory levels |

None of the added files is authored content; they are build/install by-products.

### ZeroWriter's modification 1 — `lib/waveshare_epd/epdconfig.py`

[`patches/waveshare-epaper-epdconfig-zerowriter.patch`](./patches/waveshare-epaper-epdconfig-zerowriter.patch)

Changes the platform-autodetect fallback:

```python
else:
-    implementation = JetsonNano()
+    implementation = RaspberryPi()
```

Upstream defaults to Jetson Nano when no Raspberry Pi or Sunrise X3 is detected. ZeroWriter 1 is a
Raspberry-Pi-only product, so the safer fallback for them is `RaspberryPi()`. **Functional, not
cosmetic:** on a Pi whose `/proc/cpuinfo` probe fails (which the project's own README warns about —
Raspberry Pi OS changed GPIO support and the project pins archived OS images), stock upstream would
instantiate the Jetson backend and fail at import time.

ZeroWriter also converted this file from CRLF to LF line endings. The patch above is generated
against an LF-normalised upstream so it applies cleanly; apply `sed -i 's/\r$//'` to the upstream
file first.

### ZeroWriter's modification 2 — `lib/waveshare_epd/epd3in7.py`

[`patches/waveshare-epaper-epd3in7-zerowriter.patch`](./patches/waveshare-epaper-epd3in7-zerowriter.patch)

**This is the substantive one: two replaced waveform LUTs and a shortened init delay.** It is
analysed in full, with the register context, in
[`../../zerowriter1-epaper-driver-notes.md`](../../zerowriter1-epaper-driver-notes.md).

Neither modified file's content exists anywhere in `waveshareteam/e-Paper` history (checked with
`git log --all --find-object`), so these are genuinely ZeroWriter's own changes and not
version skew against a different upstream revision.

### Reacquire (multiple independent, verified sources)

All statuses checked **2026-08-24**.

```bash
# Source 1 — ZeroWriter 1 at the exact snapshot commit (reproduces the tree byte-for-byte)
#   HTTP 200, Content-Type text/html (repo page); clone is the reliable form
git clone https://github.com/zerowriter/zerowriter1.git
cd zerowriter1 && git checkout e476d0567ac89104df62815f7bd2c807b8a3e140
#   the tree you want is ./e-Paper

# Source 2 — Waveshare upstream tarball at the matched commit
#   HTTP 200, application/x-gzip, 27,470,969 bytes downloaded
#   sha256(epd-fc4f5433.tar.gz) = 59b9f65f4706aa9f1cfbcf62d432c71b59fe3ff51e72264a852c608fe2f83a01
#   NOTE: GitHub auto-generated tarballs are not guaranteed byte-stable over time.
curl -L -o epd-fc4f5433.tar.gz \
  https://codeload.github.com/waveshareteam/e-Paper/tar.gz/fc4f54334d087dae440e3e9ac2bf8d809dfcfb53

# Source 3 — Waveshare upstream zip at the matched commit
#   HTTP 200, application/zip (302 -> codeload)
curl -L -o epd-fc4f5433.zip \
  https://github.com/waveshareteam/e-Paper/archive/fc4f54334d087dae440e3e9ac2bf8d809dfcfb53.zip

# Source 4 — Waveshare upstream via git, pinned (most reliable)
git clone https://github.com/waveshareteam/e-Paper.git
cd e-Paper && git checkout fc4f54334d087dae440e3e9ac2bf8d809dfcfb53

# Source 5 — Wayback Machine (both repos already captured, no save needed)
#   https://web.archive.org/web/20260506003400/https://github.com/zerowriter/zerowriter1
#   https://web.archive.org/web/20260612184935/https://github.com/waveshareteam/e-Paper
```

### Verify a restored tree

```bash
cd artifacts/source-snapshots/zerowriter1
find e-Paper -type f -exec sha256sum {} + | LC_ALL=C sort -k2 | sha256sum
# expect: 4148d90638b2ec989fae68a070d1b8712c3184134aa322be026a7bc940ecf75b
find e-Paper -type f | wc -l          # expect 272
find e-Paper -type f -printf '%s\n' | awk '{s+=$1}END{print s}'   # expect 32575902
```

### Restore from the local archive

```bash
mv archive/devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter1/e-Paper \
   devices/zerowriter/zerowriter-ink/artifacts/source-snapshots/zerowriter1/e-Paper
```

---

## Libraries deliberately **kept**

| Library / tree | Size | Why kept |
|---|---:|---|
| `artifacts/source-snapshots/zerowriter_ink/design/` | ~100 MiB | **Not a dependency.** ZeroWriter's own KiCad designs for three custom PCBs (Inkplate 5 Gen2 respin, keyboard, breakout). Device-specific and primary — must never be archived. |
| `artifacts/source-snapshots/zerowriter_ink/src/`, `utils/`, `compiled fonts/` | ~144 KiB | ZeroWriter's own firmware/tooling source. |
| `artifacts/source-snapshots/zerowriter_ink/firmware_releases/` | 8.9 MiB | Vendor firmware binaries including `zw_latest.merged.bin`. **Scarce** — GitHub release binaries disappear; see the device README. Kept and flagged. |
| `artifacts/source-snapshots/zerowriter1/zerowriter_stl_*.zip` | 380 KiB | ZeroWriter's own enclosure STLs. Small and device-specific. |
