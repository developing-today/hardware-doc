# T-Display K230 — acquisition

Clean-clone reproduction, in execution order. Every step states its expected result and its
failure mode. Machine-readable form: [`manifest.json`](manifest.json).

## 0. Prerequisites

```sh
# GitHub token: api.github.com limits per identity, so no User-Agent helps.
gh auth status
export GH_TOKEN="$(gh auth token)"    # or use `gh api` directly
```

`curl`, `git`, `python3`, `sha256sum`, `file`.

## 1. Chip documentation — **filed under the component, not here**

The K230 datasheets belong to `components/canaan/k230/artifacts/` because they describe the
**chip**, not this board. They are already retained there; this section exists so a reader
starting from the board record can reach them.

```sh
cd components/canaan/k230/artifacts
SHA=f8e30213963e0ed5cf995c3cd4701218a45e4793
for p in en/00_hardware/K230_datasheet.md en/K230_brief_datasheet.md \
         en/00_hardware/K230_Hardware_Design_Guide.md \
         en/01_software/board/osdrv/K230_PMU_User_Guide.md \
         en/01_software/board/ai/K230_nncase_Development_Guide.md \
         en/02_applications/tutorials/K230_RVV_In_Action.md \
         en/02_applications/tutorials/K230_RVV_optimization_performance_description.md; do
  curl -sSLo "$(basename "$p")" "https://raw.githubusercontent.com/kendryte/k230_docs/$SHA/$p"
done
sha256sum -c SHA256SUMS      # expect: all OK
```

Reacquisition: **automatic**. Fallback host:
`https://www.kendryte.com/k230/en/main/00_hardware/K230_datasheet.html`.

The Canaan reference-board EDA set is **enumerated but not retrieved** —
[`CANAAN-EDA-SET.md`](../../../../components/canaan/k230/artifacts/CANAAN-EDA-SET.md) carries
every path, exact byte size and two reacquisition URLs.

## 2. Board software — pinned commits

```sh
git clone https://github.com/Xinyuan-LilyGO/T-Display-K230.git
git -C T-Display-K230 checkout bb831ab358b66f5bd9a87ecd7c580fee4537492e
# with the SDK submodule (adds ~100 MB):
git -C T-Display-K230 submodule update --init --recursive

git clone https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840.git
git -C T-Display-K230-nRF52840 checkout 4646a728580739d487126f47a521e9b8032b3c2c

git clone https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF9151.git
git -C T-Display-K230-nRF9151 checkout ed4ecbe34162dec9b81213a400198125bbd6e36f
```

**Not vendored into this repository.** Reasons: ~192 MB combined, **no licence file on any of
them**, and they are reproducible from pinned commits. Facts extracted from them are in
[`pinouts-and-buses.md`](../pinouts-and-buses.md), [`development.md`](../development.md) and the
component records, so no future work depends on re-reading the trees.

Disposition `reference-only`; redistribution status `unknown`; reacquisition `automatic`.

## 3. Companion-MCU prebuilt firmware

```sh
B=https://github.com/Xinyuan-LilyGO/T-Display-K230-nRF52840/raw/4646a728580739d487126f47a521e9b8032b3c2c
curl -sSLO "$B/firmware/k230_nrf52840_at_20260816_r4_k230_uart_dfu.uf2"    # 296 960 B
curl -sSLO "$B/bootloader/k230_nrf52840_bootloader_uartdfu_115200_s140_6.1.1.hex"  # 525 680 B
file *.uf2 *.hex     # validate from content, never from the extension
```

**Not retained here** — no licence, and byte sizes are recorded so identity can be confirmed on
reacquisition. **SHA-256 is unknown**: the files were enumerated from the Git tree API, not
downloaded. Recorded as unknown rather than omitted.

## 4. Images

Retained in [`../media/`](../media/) with SHA-256 and byte size for all 14 in
[`../media/manifest.json`](../media/manifest.json). Held **unstaged** — no licence statement
exists on either lilygo.cc or wiki.lilygo.cc.

**Enumerated but not fetched:** the six Cased Version wiki images, base URL
`https://wiki.lilygo.cc/products/t-display-series/t-display-k230/cased-version/image/<name>.jpg`,
names `t-display-k230-cased-{angle,front-back,dimensions,features,details,pinmap}.jpg`. And the
repository images, notably **`image/pins_annotated.png` (699 111 B)** in the nRF52840 repository —
an annotated pin photograph of the base board, and the most useful un-fetched image known.

## 5. Verification

```sh
sha256sum -c components/canaan/k230/artifacts/SHA256SUMS      # expect: 7x OK

# Verify every retained image against its manifest, and check JPEG magic bytes.
# (`file` is absent on some hosts; check the magic directly.)
python3 tools/verify_media_manifest.py devices/lilygo/t-display-k230/media/manifest.json
```

If that helper does not exist in your checkout, the equivalent inline check is: for each record
in `media/manifest.json`, recompute `sha256` over the file at `devices/lilygo/t-display-k230/` +
its `file` field, compare against the recorded value, and confirm the first three bytes are
`FF D8 FF`. All 14 records were verified this way on 2026-09-04 and all matched.

## 6. Reacquisition status summary

| Class | Status |
|---|---|
| Canaan documentation | **automatic** — pinned commit + a second host |
| Canaan EDA set | **automatic** — enumerated, two URLs each |
| LilyGO repositories | **automatic** — pinned commits |
| Companion firmware binaries | **automatic** — pinned raw URLs; **SHA-256 unknown** (enumerated from the tree API, not downloaded) |
| Product/wiki images | **automatic**, retained |
| Cased Version images | **automatic**, enumerated but not fetched |
| `image/pins_annotated.png` | **automatic**, not fetched |
| **A LilyGO schematic** | **lost** — never published ([`GC-5`](../gaps-and-conflicts.md)) |
| **`K230_PINOUT_V1.0_20230524`** | **lost** — cited by Canaan’s datasheet, absent from the repository |
| **A factory system image** | **does not exist** — LilyGO publishes none |

## 7. Licence and decisions report

| Group | Items | Recommendation |
|---|---|---|
| **Known permissive** | `kendryte/k230_linux_sdk`, `k230_sdk`, `k230_docs` repositories — BSD-2-Clause | Safe to reference and to build from |
| **Conflicting / strict** | The Canaan **documents**, which carry “shall not disseminate … in any form” inside a BSD-2-Clause repository | 7 files retained **unstaged**. User decision needed: stage, move to local cache, or keep metadata only. |
| **Unknown terms** | **Every LilyGO repository** (no LICENSE file), the prebuilt nRF52840 firmware and bootloader, and all 14 product/wiki images | Repositories and firmware kept `reference-only`; images retained **unstaged**. User decision needed on the images. |
| **Large paths** | LilyGO BSP ~110 MB (+ ~100 MB SDK submodule); `T-Display-K230_canmv_rt` **745 MB**; Canaan EDA set ~19 MB | All `reference-only`. None downloaded into the repository. |
| **Opaque binaries** | `k230_nrf52840_at_*.uf2`, `k230_nrf52840_bootloader_*.hex` | Not downloaded. Byte sizes recorded; SHA-256 unknown and recorded as unknown. |

**Nothing has been staged or committed by this session.**
