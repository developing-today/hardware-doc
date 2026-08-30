# Verification report — Seeed XIAO ESP32S3 Sense

Research pass **2026-08-24**. All figures recomputed from the files on disk at completion.

> **Updated after a second and third pass.** Feature guides, market/community research, FCC filings and the
> Sense daughterboard schematic were added after the first report was written. Figures below are current.

## Inventory

| Metric | Value |
|---|---|
| Files in the device tree | **1,141** |
| Total bytes | **206,492,954** (~197 MiB) |
| Authored Markdown | **38 documents + 1 reusable guide**, **5,659 lines** |
| Artifacts downloaded | **56**, all validated (`download.py --verify-only`: 56/56) |
| Wiki snapshot | 230 Markdown files |
| Vendored examples | 9 repositories |
| Component records created | **9** (+1 updated); 1 unidentified part **resolved** |
| Tools written | **9** Python scripts |
| Media catalogued | 14 images |
| Relocated to `../hardware-doc-archive` | **110 MiB** |

## Automated checks

| Check | Result |
|---|---|
| ZIP integrity (`unzip -t`, 24 archives) | ✅ all pass |
| PDF magic bytes (16 PDFs) | ✅ all `%PDF` |
| Non-ASCII / non-portable filenames | ✅ **0** |
| Broken relative Markdown links (device tree) | ✅ **0** |
| Broken relative links (components/vendors added) | ✅ **0** |
| Acquisition manifest schema | ✅ 42 entries complete |
| `download.py --verify-only` | ✅ **56/56 verified, 0 failed** |
| Staged deletions in git index | ✅ **0** |
| Archived content present in git index | ✅ verified by `git cat-file` |

## Duplicate analysis

**88 duplicate sets, 12,559,620 redundant bytes.** All explained; none accidental:

| Cause | Bytes | Intentional? |
|---|---|---|
| `xiao-esp32s3-v1.4-sch-pcb/` extracted tree | ~2.5 MB | ✅ **Yes** — Seeed serves byte-identical ZIPs under two URLs ([conflict #1](devices/seeed-studio/xiao-esp32s3-sense/gaps-and-conflicts.md#1-seeed-serves-the-wrong-file-under-the-xiao-esp32s3-v14-schematic-url)). Both extracted trees are retained as **evidence of the vendor error** |
| `camera_pins.h` / `camera_index.h` repeated across sketches | ~1.2 MB | ✅ Upstream repo structure — Arduino requires a copy per sketch folder |
| `media/` copies of files also inside extracted archives | ~230 KB | ✅ Deliberate — surfaces the block diagram where it is findable |
| Upstream `LICENSE` files shared between repos | small | ✅ Unavoidable |
| Firmware binaries identical across the two vendor releases | — | ✅ Retained under `firmware/`; the finding *is* that they are identical |

Four **exact-duplicate PDFs** were removed and replaced with `*.DUPLICATE.md` pointers (3.07 MB reclaimed), each naming the retained copy and its SHA-256.

## Evidence discipline

| Property | Status |
|---|---|
| Every GPIO claim traceable to PCB netlist, schematic or vendor header | ✅ |
| Three independent chains agree on the pin map | ✅ netlist / `camera_pins.h` / `pins_arduino.h` |
| Vendor contradictions recorded rather than resolved | ✅ 12 in `gaps-and-conflicts.md` |
| Community claims labelled by evidence type | ✅ firsthand / reported / inferred |
| Flash commands labelled by execution status | ✅ none claimed `executed-success` |
| **Hardware-tested claims** | ⚠ **zero — no hardware available** |

## Licensing

| Redistribution status | Count |
|---|---|
| `allowed` (CC BY-SA 4.0 — all schematics/KiCad) | 14 |
| `conditional` | 1 |
| **`prohibited`** | **4** — OV3660/OV5640 datasheets and module specs |
| `unknown` | 23 |

**13 artifacts >1 MB are flagged `review_required`** in `acquisition/manifest.json`. They remain staged per the user's explicit instruction to keep documents in place. The four `prohibited` items carry OmniVision's clause *"Individuals and/or organizations are not allowed to re-distribute said information."*

## Known limitations

1. **No hardware.** No first-party measurement. Partially mitigated in pass 3: the Seeed forum yielded **owner-measured** sleep-current and thermal figures, labelled as such.
2. **No example was built or flashed.** Dependencies audited by inspection only.
3. ~~Daughterboard not torn down~~ — **RESOLVED**: Seeed publishes the schematic under the misleading name *"XIAO ESP32S3 Exp. Board v1.0"*. Microphone identified as **MSM261D3526H1CPM**; full netlist in [`sense-daughterboard.md`](devices/seeed-studio/xiao-esp32s3-sense/sense-daughterboard.md).
4. ~~Regulatory filings not mined~~ — **DONE**: FCC `Z4T-XIAOESP32S3` retrieved (9 exhibits). Yielded antenna performance data and the bottom-side JTAG pads, but **did not** resolve the microphone — the schematic did.
5. **Marketplace/distributor/used/clone pricing not sampled** — only the Seeed store, one date, USD.
6. **Community search covered Reddit (115 posts) and the Seeed forum (50 topics, 3 read in full, 118 posts).** Gitee returned zero results / HTTP 405. The **zh-CN, ja and pt-BR wiki translations were compared against English and found equivalent** (identical section counts, spec values, code blocks and GPIO references) — so no non-English *official* documentation gap remains. Chinese *community* platforms (Bilibili, Zhihu) and Discord remain unsearched.
7. ~~EAGLE expansion-board XML unparsed~~ — **DONE**, and it turned out to be the Sense daughterboard itself.
8. **Five feature coverage gaps** — BLE, deep sleep, OTA, ESP-NOW, USB HID/MSC. (*On-device ML now has a guide.*)
10. **MEMSensing datasheet not obtained** — `memsensing.com` 403s all agents and **LCSC now serves HTML for every datasheet PDF URL**, including one an older record of ours cites. Microphone acoustic specs remain unestablished.
9. `raw.githubusercontent.com` snapshots of `pins_arduino.h` / `camera_pins.h` were taken from `master`, so are **not revision-pinned**.

## Corrections made to earlier passes

Later passes contradicted earlier findings in five places. All were corrected in place, with the superseded text retained and the reason recorded:

| Earlier claim | Correction | Source of correction |
|---|---|---|
| "Daughterboard schematic is not published" | It **is** — under the misleading name *"XIAO ESP32S3 Exp. Board v1.0"* | EAGLE XML parse |
| "Microphone part number unconfirmed" | **MSM261D3526H1CPM**, from the daughterboard BOM | EAGLE XML parse |
| "Camera believed to run from 3V3" | Runs from **local 2.8 V and 1.3 V LDOs** | Daughterboard schematic |
| "Deep sleep ~34 µA" (vendor figure, repeated) | **~90 mA after a capture**; ~1.45 mA with the standby workaround | Seeed forum, owner measurements |
| "Seeed barely documents LoRa/Meshtastic" | Seeed maintains **15 wiki pages** on it; only the *showcase PDF* under-represents it | Wiki corpus re-check |

A sixth correction belongs to Seeed rather than to this research: the daughterboard schematic labels a net `VCC_1V8` when the fitted regulator outputs **1.3 V**. Seeed staff confirmed the error on their forum; the schematic had not been updated as of this snapshot.

## Pre-existing issues (not introduced here)

A repository-wide link check found **28 broken relative links in other device trees** (`nicolai-electronics/tanmatsu`, `waveshare/esp32-p4-*`, `guides/espressif/*`). These predate this pass and were **not** modified.

## Related

- [Device record](devices/seeed-studio/xiao-esp32s3-sense/README.md)
- [`gaps-and-conflicts.md`](devices/seeed-studio/xiao-esp32s3-sense/gaps-and-conflicts.md)
- [`acquisition/manifest.json`](devices/seeed-studio/xiao-esp32s3-sense/acquisition/manifest.json)
- [Seeed vendor sourcing guide](vendors/seeed-studio/README.md)
