# Duplicate removed: `xiao-esp32s3-v1.4-sch.pdf`

> Content-identical to another file already in this repository. The bytes were
> **not** unique, so this copy was removed on 2026-08-24 and replaced by this pointer.

| Field | Value |
|---|---|
| Canonical copy | [`xiao-esp32s3-sense-v1.5-sch.pdf`](xiao-esp32s3-sense-v1.5-sch.pdf) |
| Repo path of canonical copy | `artifacts/schematics/xiao-esp32s3-sense-v1.5-sch.pdf` |
| Shared SHA-256 | `15993097cd695d177af352f4664ca91290a99c833f51d122d1165ef222f9923c` |
| Size | 666,348 bytes |
| Why this copy existed | VENDOR BUG: Seeed's download URL '202003751_XIAO ESP32S3_v1.4_SCH_260226.pdf.pdf', advertised as the schematic for the NON-Sense XIAO ESP32S3 v1.4, actually serves the Sense v1.5 schematic. Byte-identical. The matching SCH&PCB zips are identical too - unzipping the 'v1.4' zip yields a directory named '202003753_XIAO ESP32S3 Sense_v1.5_SCH&PCB_260226'. There is currently NO way to obtain a genuine non-Sense v1.4 schematic from Seeed. See gaps-and-conflicts.md. |

Restore it, if you ever need the file at this exact path:

```bash
cp "xiao-esp32s3-sense-v1.5-sch.pdf" "xiao-esp32s3-v1.4-sch.pdf"
```

Verify:

```bash
echo "15993097cd695d177af352f4664ca91290a99c833f51d122d1165ef222f9923c  xiao-esp32s3-v1.4-sch.pdf" | sha256sum -c -
```
