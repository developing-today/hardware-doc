# Archived: `xiao-esp32s3-plus-v1.1-kicad.zip`

> Moved out of the repository **2026-08-30**, not deleted. Its full extraction remains in
> this repository at
> [`../extracted/xiao-esp32s3-plus-v1.1-kicad/`](../extracted/xiao-esp32s3-plus-v1.1-kicad/) —
> only the redundant ZIP wrapper was archived.

| Field | Value |
|---|---|
| Original path | `artifacts/kicad/xiao-esp32s3-plus-v1.1-kicad.zip` |
| **SHA-256** | `8a90aa5990a835e97bc1e74afdd36f6a84dc32ad2eee2c423a6818157e1e65cd` |
| **Size** | 678 481 bytes |
| Root directory inside the ZIP | `202004052_XIAO ESP32S3 Plus_v1.1_KiCad` (vendor part number `202004052`) |
| Retrieved | 2026-08-24 |
| Archive path | `archive/hardware-doc/devices/seeed-studio/xiao-esp32s3-sense/artifacts/kicad/` |

Full details, alongside the three schematic ZIPs archived at the same time, are in
[`../schematics/ARCHIVED-SCHEMATIC-ZIPS.md`](../schematics/ARCHIVED-SCHEMATIC-ZIPS.md).

## Why this file mattered

It is the design source for the **XIAO ESP32S3 Plus**, and the evidence behind two comparisons
in [`comparisons-and-recommendations.md`](../../comparisons-and-recommendations.md):

- The Plus uses the **same B2B footprint and pin assignment** as the Sense, but a **different
  connector part** — `LBF11-G30P-BOR` rather than the Hirose `DF40C-30DP`.
- The Plus adds **`ADC_BAT` on GPIO10**, a battery-sense divider the Sense does not have.

## Reacquisition

Despite being a KiCad library rather than a schematic, this file is served from the **same wiki
resources bucket** as the schematic ZIPs — note the vendor's own filename encodes `260115`, a
different release date from the `260226` schematic set:

```bash
curl -fsSL "https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_Plus_V1.1_KiCad_260115.zip" \
  -o xiao-esp32s3-plus-v1.1-kicad.zip

echo "8a90aa5990a835e97bc1e74afdd36f6a84dc32ad2eee2c423a6818157e1e65cd  xiao-esp32s3-plus-v1.1-kicad.zip" | sha256sum -c -
```

Fallback: `https://web.archive.org/web/2/https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_Plus_V1.1_KiCad_260115.zip`

Licence **CC BY-SA 4.0**, redistribution allowed — see the record for `xiao-esp32s3-plus-v1.1-kicad`
in [`../../acquisition/manifest.json`](../../acquisition/manifest.json) and
[`sources.md`](../../sources.md).

The other ZIPs still present in this directory (`xiao-series-footprints.zip`,
`xiao-series-sch-symbols.zip`, `xiao-esp32s3-package.zip`,
`seeeduino-xiao-esp32s3-kicad-library.zip`) were **not** archived — they have no extraction in
the repository, so the ZIP is the only copy.
