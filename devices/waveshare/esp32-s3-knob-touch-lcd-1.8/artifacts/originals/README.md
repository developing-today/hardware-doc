# Original vendor archives — acquisition record

> Retrieval date: **2026-08-21**. URLs re-probed **2026-08-23**.

All URLs were enumerated from the local wikitext snapshot
`../source-snapshots/waveshare-wiki-wikitext-oldid-111069.txt` and live-probed with HTTP HEAD.
In every case the served `Content-Length` matched the local byte size exactly.

> **⚠️ Updated 2026-08-24 — three of these four files have since been archived.**
> Only the product photograph `ESP32-S3-Knob-Touch-LCD-1.8-14.jpg` remains in this directory.
>
> `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` was archived last, after a full 1,802-member
> reconciliation and after **both** its vendor URL and its Internet Archive capture were
> downloaded in full and hash-verified. Everything below about it being "deliberately retained"
> and "single-source" is **superseded** — see
> [`ARCHIVED-ORIGINAL-ZIPS.md` §3](./ARCHIVED-ORIGINAL-ZIPS.md#3-esp32-s3-knob-touch-lcd-18-demozip).
>
> `ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` and `ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` were moved
> to `../hardware-doc-archive/` after their contents were verified byte-identical to trees that
> remain here, and after Internet Archive mirrors were found and hash-verified. See
> [`ARCHIVED-ORIGINAL-ZIPS.md`](./ARCHIVED-ORIGINAL-ZIPS.md). **The "single-source risk" note at
> the end of this file is superseded for all three ZIPs** — each now has multiple working,
> hash-verified URLs.

## The four original downloads, and where each is now

| File | Bytes | SHA-256 | Upstream `Last-Modified` | Status |
|---|---:|---|---|---|
| `ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip` | 68,704,748 | `11e382444fe93470fbe463829c1e0ebad5bdb5115fd2d72f6159cd7700015030` | Fri, 20 Jun 2025 09:19:41 GMT | **archived 2026-08-24** |
| `ESP32-S3-Knob-Touch-LCD-1.8-14.jpg` | 66,538 | — | — | present |
| `ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip` | 2,032,893 | `7d29fc1fb356059f7291eccd74bfb5c9fa7538998bc3f5ff811cd87f04c1691c` | Thu, 19 Jun 2025 12:56:40 GMT | **archived 2026-08-24** |
| `ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` | 672,290 | `baa5ac1bf75fbbd86a8135b123ff498bd7db4a5c68184481db6b82cadbaca0e5` | Thu, 19 Jun 2025 12:56:40 GMT | **archived 2026-08-24** |

Direct URLs:

```
https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip
https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-BIN.zip
https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip
```

Probe result for the Demo ZIP on 2026-08-23: `HTTP/1.1 200`, `Content-Length: 68704748` —
**matches the local byte size exactly**, so the vendor is still serving the identical artifact.

## Relationship between the ZIP and `../demo/`

`../demo/ESP32-S3-Knob-Touch-LCD-1.8-Demo/` is the **extraction of this exact ZIP**, verified
member-by-member:

- ZIP contains **1802 files**; extracted tree contains **1802 files**
- Filename sets are identical except for **three documented ASCII renames**, applied because the
  originals carry Chinese filenames that are not portable

| Original ZIP member | Renamed on disk to |
|---|---|
| `.../SensorLib/datasheet/CHSC5816触控芯片使用说明V1-20221114.pdf` | `CHSC5816-touch-controller-datasheet-v1-20221114.pdf` |
| `.../SensorLib/datasheet/海栎创触摸芯片移植手册-v3.5-20220701(1).pdf` | `hynitron-touch-driver-guide-v3.5-20220701.pdf` |
| `.../SensorLib/datasheet/环境光与接近传感器应用与选型.pdf` | `ambient-light-and-proximity-sensor-selection.pdf` |

This means the ZIP and the extracted tree are **intentional duplication** — roughly 66 MiB of the
repository is the same content stored twice.

**~~The ZIP is deliberately retained~~ — superseded 2026-08-24; it was archived.** The reasoning
below is kept for the record, with each point's resolution:

1. It is the only byte-exact original. The extracted tree has renamed files and, following the
   2026-08-23 cleanup, no longer contains the bundled LVGL and SensorLib trees.
2. It is the fallback source for restoring those archived libraries — this is precisely how they
   were recovered and hash-verified during that cleanup.
3. Waveshare serves it from a single origin with no third-party mirror; if it is withdrawn there
   is no second source.

Resolution of each point, 2026-08-24:

1. Still true, and it is why the ZIP was **archived rather than deleted**.
2. **No longer true.** [`../../tools/restore-demo-deps.sh`](../../tools/restore-demo-deps.sh)
   restores both libraries from upstream GitHub tags, verified against recorded digests. This
   was tested against this exact ZIP: the restored tree matches all 1,802 members by content.
3. **Wrong.** The Internet Archive holds a 2025-08-22 capture. It was downloaded in full on
   2026-08-24 and is byte-identical (`11e38244…5030`). The vendor URL was also downloaded in
   full the same day and matches. Two hash-verified sources.

Reacquire:

```bash
curl -L -O https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip
sha256sum ESP32-S3-Knob-Touch-LCD-1.8-Demo.zip
# expect 11e382444fe93470fbe463829c1e0ebad5bdb5115fd2d72f6159cd7700015030
```

Also linked from the product wiki: <https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8>
and the product page <https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm>.

> **Single-source risk.** Unlike the `/wiki/common/` shared-pool files, these are served only
> from this product's own directory. No GitHub, distributor, or archive mirror was located.
> Strong candidate for `https://web.archive.org/save/`.
>
> **Correction, 2026-08-24.** This was checked properly and is **wrong for all three ZIPs**.
> The Internet Archive holds captures of every one of them — two each for the BIN and schematic
> archives (2025-08, 2026-01) and one for the Demo archive (2025-08-22). All were downloaded and
> hash-verified as byte-identical. See [`ARCHIVED-ORIGINAL-ZIPS.md`](./ARCHIVED-ORIGINAL-ZIPS.md).

## What was removed from the extracted tree

See [`../vendored-deps/README.md`](../vendored-deps/README.md). Summary: the bundled
**LVGL 8.4.0** (158 MiB) and **SensorLib 0.3.1** (43 MiB) trees were moved to
`../hardware-doc-archive/`, after being verified as unmodified upstream releases apart from one
one-line patch each, both of which are preserved as patch files. All 15 SensorLib datasheets were
promoted into reusable component records first.
