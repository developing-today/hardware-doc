# ARCHIVED: `xiao-reference-design.pdf`

> Moved out of the repository **2026-08-28**, not deleted. Content already mined — see below.

| Field | Value |
|---|---|
| Original path | `devices/seeed-studio/xiao-esp32s3-sense/artifacts/datasheets/xiao-reference-design.pdf` |
| **SHA-256** | `22914bcb0d541de5b2dab1f9f941dc9529a53ffcc7d7f01f4468a9aaecc4625d` |
| **Size** | **49 878 649 bytes** (47.6 MiB) — the largest file in the repository |
| Pages | 129 |
| Published | 2025-11-15 (Adobe InDesign 20.5) |
| Retrieved | 2026-08-24 |
| Licence | Unstated — Seeed marketing catalogue |
| Reason archived | Largest file in the repo; **its content is fully extracted into committed Markdown and JSON** |

## Reacquisition

```bash
curl -fsSL "https://files.seeedstudio.com/wiki/XIAO/XIAO-Reference-Design.pdf" \
  -o xiao-reference-design.pdf
```

Fallbacks, in order: the [XIAO wiki resources section](https://wiki.seeedstudio.com/SeeedStudio_XIAO_Series_Introduction/) · `https://web.archive.org/web/2/https://files.seeedstudio.com/wiki/XIAO/XIAO-Reference-Design.pdf`

Archive copy (if you hold it): `archive/doc/hardware/devices/seeed-studio/xiao-esp32s3-sense/artifacts/datasheets/xiao-reference-design.pdf`

## What was extracted before archiving

Despite its name this is **not a hardware design guide** — pages 14–129 are a curated community project showcase.

| Extracted to | What |
|---|---|
| [`artifacts/showcase-projects.json`](../showcase-projects.json) | **117 project entries** — category, XIAO variant, title, author, keywords, intro, and the `/Annots` hyperlinks |
| [`projects-and-community.md`](../../projects-and-community.md) | The 28 ESP32-S3/Sense projects, tabulated by category with source links and platform statistics |
| [`product-history-and-family.md`](../../product-history-and-family.md) | The cross-XIAO comparison tables (pp. 9–12) — SKUs, chips, RAM, flash, sensors, low-power figures |
| [`gaps-and-conflicts.md`](../../gaps-and-conflicts.md) | The **third contradictory low-power figure** (26.5 mA) that this catalogue adds |
| [`tools/extract_showcase.py`](../../../../../tools/extract_showcase.py) | The extractor — re-runnable against a re-downloaded copy |

**Two extraction traps** are recorded in the tool and the vendor guide: project URLs live in PDF **link annotations**, not text, so they are invisible to text extraction; and InDesign kerning scatters spaces inside words (`W e ar ables`), requiring vocabulary-based re-joining.

You should not need this PDF again unless re-mining for something the extractor missed.
