# Duplicate removed: `xiao-esp32s3-v1.4-sch-pcb.zip`

> Content-identical to `xiao-esp32s3-sense-v1.5-sch-pcb.zip`. The bytes were **not** unique,
> so this copy was removed on 2026-08-30 and replaced by this pointer.
>
> This is the ZIP counterpart of the PDF case already recorded in
> [`xiao-esp32s3-v1.4-sch.pdf.DUPLICATE.md`](xiao-esp32s3-v1.4-sch.pdf.DUPLICATE.md) —
> **the same vendor bug affects both the schematic PDF and the SCH&PCB archive.**

| Field | Value |
|---|---|
| Canonical copy | `xiao-esp32s3-sense-v1.5-sch-pcb.zip` (itself archived — see [`ARCHIVED-SCHEMATIC-ZIPS.md`](ARCHIVED-SCHEMATIC-ZIPS.md)) |
| Extracted contents, in repo | [`../extracted/xiao-esp32s3-sense-v1.5-sch-pcb/`](../extracted/xiao-esp32s3-sense-v1.5-sch-pcb/) |
| Shared SHA-256 | `a82247725c8a8bcd8cac81a7acbd126396217e5b680f6dfe28958851e02d5cdb` |
| Size | 836,170 bytes |
| Verified identical | 2026-08-30, by SHA-256 of the ZIPs **and** a recursive `diff` of both extracted trees (no differences) |

## Why this copy existed

**VENDOR BUG.** Seeed's wiki advertises two distinct downloads:

| Advertised as | URL filename |
|---|---|
| XIAO ESP32S3 **v1.4** (non-Sense) SCH&PCB | `202003751_XIAO ESP32S3_v1.4_SCH&PCB_260226.zip` |
| XIAO ESP32S3 **Sense v1.5** SCH&PCB | `202003753_XIAO ESP32S3 Sense_v1.5_SCH&PCB_260226.zip` |

Both URLs serve **the same bytes**. Unzipping the "v1.4" archive yields a directory named
`202003753_XIAO ESP32S3 Sense_v1.5_SCH&PCB_260226` — the vendor's own internal part number
`202003753` (Sense) rather than `202003751` (non-Sense), which is how the substitution is
provable rather than merely suspected.

**Consequence: there is currently no way to obtain a genuine non-Sense v1.4 SCH&PCB set from
Seeed.** Any analysis of "the v1.4 non-Sense board" derived from this file is actually
describing the Sense v1.5 board. See
[`gaps-and-conflicts.md`](../../gaps-and-conflicts.md).

## Restore, if you need the file at this exact path

```bash
cp "$HOME/hardware-doc-archive/doc/hardware/devices/seeed-studio/xiao-esp32s3-sense/artifacts/schematics/xiao-esp32s3-sense-v1.5-sch-pcb.zip" \
   xiao-esp32s3-v1.4-sch-pcb.zip
```

Or re-fetch from either vendor URL (they are interchangeable, which is the bug):

```bash
curl -fsSL "https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/202003751_XIAO%20ESP32S3_v1.4_SCH%26PCB_260226.zip" \
  -o xiao-esp32s3-v1.4-sch-pcb.zip
```

Verify:

```bash
echo "a82247725c8a8bcd8cac81a7acbd126396217e5b680f6dfe28958851e02d5cdb  xiao-esp32s3-v1.4-sch-pcb.zip" | sha256sum -c -
```

> If this check ever **fails**, that is itself a finding: it would mean Seeed has fixed the
> mispackaging and a genuine v1.4 non-Sense design set is finally available. Update
> `gaps-and-conflicts.md` if so.
