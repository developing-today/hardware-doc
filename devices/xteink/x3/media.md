# Xteink X3 — images and teardown views

**The X3 is the only Xteink device with public teardowns — and it has two,
independent, in different languages.** Both are archived with placeholders.

## Teardown A — English, 13 photos, Imgur

| Field | Value |
|---|---|
| Author | Reddit user, posted to r/xteinkereader |
| Source post | <https://old.reddit.com/r/xteinkereader/comments/1uksv6s/xteink_x3_teardown/> |
| Album | <https://imgur.com/a/xteink-x3-teardown-OA6CS2C> |
| Date | **2026-07-01** (Imgur per-image timestamp 17:44:53) |
| Images | **13**, up to 5760 × 3240 |
| Local | [`artifacts/teardown/imgur-2026-07-01/`](artifacts/teardown/imgur-2026-07-01.ARCHIVED.md) — archived, 18.61 MiB |
| Rights | **Unknown** — no terms stated. Unstaged pending review |
| Stated purpose | Attach a **Nordic Power Profiler Kit II** *"to see if I can make any power optimizations to crosspoint firmware"* |

### What each image establishes

| # | Hash | Author's caption | What it establishes |
|---:|---|---|---|
| 1 | `u60Rtxi` | *"The glass back came off pretty easily with a heatgun, suction-cup, and a plastic spudger."* | **Glass back**, adhesive-mounted, serviceable |
| 3 | `Q5jsUoi` | *"The **650mAh battery** is glued to the back. So are the **magnets for the pogo connector**."* | **Battery capacity** and that the pogo magnets are glued, not soldered |
| 4 | `WAlvma8` | *"battery connector"* | The cell is connectorised, not soldered — replaceable in principle |
| 5 | `lBJtD4I` | *"The eink display is a little transparent."* | Panel construction |
| 6 | `pcqe4Q0` | *"Back of device."* | — |
| 7 | `QQz92jU` | *"Main PCB"* | Single-board construction |
| 9 | `Q0UGXpo` | *"bad overview of the esp32-c3"* | **SoC family** |
| 10 | `YgdHbR1` | *"…ESP32-C3 main CPU. **128MBit (16MB) flash for firmware**."* | SoC + **external flash size** |
| 12 | `wKlM8uS` | *"Silkscreened off areas of the PCB is where the magnets are on the back plate."* | Magnet keep-outs designed into the PCB |
| 13 | `Ay3rpJg` | ***"DS1307 RTC"*** | **The RTC conflict** — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) |

Per-image SHA-256 values are in the placeholder's Contents table and in
`manifest.json` inside the archived directory.

**Retrieval note.** `imgur.com/a/<id>` is a JavaScript shell that yields **2 of 13**
images when scraped. Use
`https://imgur.com/ajaxalbums/getimages/OA6CS2C/hit.json` to enumerate hashes and
captions, then fetch `https://i.imgur.com/<hash>.jpg`.

## Teardown B — Chinese, 10 photos **including a schematic**

| Field | Value |
|---|---|
| Author | GitHub user `sunwoods` |
| Repository | <https://github.com/sunwoods/Xteink-X3> — 收集关于阅星瞳X3的软硬件信息 |
| Local | [`artifacts/teardown/sunwoods-cn/`](artifacts/teardown/sunwoods-cn.ARCHIVED.md) — archived, 4.80 MiB |
| Rights | **None declared** — no LICENSE file. Unstaged pending review |

| File | Content |
|---|---|
| `01.jpg` | Opened device overview (拆开后的样子) |
| **`02.jpg`** | **Hand-drawn schematic sketch (原理图示意)** — the only schematic-like document for *any* Xteink device |
| `03.jpg`, `04.jpg` | **Annotated functional-block overlays** (功能模块标记) |
| `05`–`10.jpg` | Chip-marking close-ups (细节放大) |
| `README.upstream.md` | The BOM list, preserved |

**Schematic caveat, stated upstream:** 部分器件用其他类似封装替代 — *"some
components are substituted with other similar footprints"*. It is a functional
sketch, **not fabrication-accurate**.

### The BOM this teardown gives

- ESP32-C3
- **PUYA 128 Mbit Flash**
- **QMI8658** attitude sensor
- **DS系列RTC时钟芯片** — "DS-series RTC clock chip" (**deliberately not narrowed**)
- **类似TP4056的电池管理芯片** — "a TP4056-like battery-management chip"
- **TI BQ27220 库仑计** — coulomb counter
- ***ISO/IEC 14443a NFC Tag** — marked with asterisks by the author, i.e. flagged
  as notable

**The NFC tag appears in no firmware, no board profile and no English-language
source.** This teardown is the only technical evidence it exists, corroborated
only by the vendor's launch bullet *"NFC support"*.

## Why two teardowns matter more than one

They agree independently on the ESP32-C3, the 128 Mbit flash and the general
construction — and they **disagree, usefully, on the RTC**: the English author
reads a specific `DS1307` marking, the Chinese author declines to narrow past
"DS-series", and the FreeInk SDK drives a `DS3231`. Three sources, three
positions, one address (0x68). That disagreement is preserved rather than
resolved.

## What is still missing

- **No X3 Pro/variant photography** distinguishing the UC8253 and UC8279d batches.
- **No photograph of the panel's own FPC marking**, which would give the module
  part number.
- **The schematic sketch has not been read in detail.** It is held here and could
  resolve the GPIO0/GPIO20 dual-assignment conflict. Cheapest open action.
- Vendor product imagery not archived (the listing is live; URLs are in
  `vendors/xteink/artifacts/store-snapshots/2026-09-04/products-p1.json`).
