# T-Display-S3 — example search log

Date **2026-09-07**. Depth and exclusions stated; this is a broad-coverage snapshot, not a
census.

| Source | Method | Depth | Result |
|---|---|---|---|
| Vendor repo `examples/` | full recursive tree at commit `ec889e7` | 3 431 tree entries filtered to 29 example directories | all 29 catalogued |
| Vendor repo `lib/` | same tree | 9 vendored libraries | not catalogued as examples; recorded as dependencies |
| `LilyGo-Display-IDF` | full tree at `b1a1cc5` | 84 entries | ESP-IDF example set — catalogued as external |
| GitHub code search | `repo:esphome/esphome t-display-s3` | 4 hits | ESPHome model definitions — catalogued as external |
| GitHub code search | `repo:russhughes/st7789s3_mpy t-display` | 7 hits | MicroPython driver + this board's `tft_config.py` |
| GitHub code search | `repo:arendst/Tasmota lilygo` · `TDisplayS3` | 19 / 0 hits | Tasmota support is a **runtime template**, not a source example |
| GitHub code search | `repo:wled/WLED lilygo` · `org:meshtastic tdisplay` | 10 / 247 hits | **negative** — no example exists for either |
| Issue tracker | 318 issues scanned for linked code | 22 read in full | found `teastainGit/…` (endorsed by the vendor) and several gists |
| Reddit | 4 query shapes, `t=all`, 25 results each | 27 relevant posts | project showcases; most link code |

## Not searched

Hackaday.io, Instructables, Bilibili, GitLab, YouTube descriptions, and forks of the vendor
repo (273 exist; none inspected). Recorded as deliberate exclusions.

## Rejections and negative findings

| Candidate | Disposition |
|---|---|
| `examples/WIFI_Audio_I2S` | **Broken as shipped** — a `.cpp` with no `.ino`, so the Arduino IDE will not open it as a sketch. Catalogued as such |
| `examples/ULP_ADC`, `ULP_Count` | Catalogued as a **conflict**: they state they need arduino-esp32 3.0.0-rc3, which the repository's own README forbids |
| `examples/nes` | Catalogued but not selected — the value is the vendored emulator, not board knowledge |
| `examples/ImageScroll`, `PCBClock`, `PokerS3` | Catalogued; community-authored showcases with multi-MB image headers |
| WLED / Meshtastic examples | Do not exist. Recorded as negative results in [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) |

## Not done

**No example was compiled or run.** No toolchain was installed and no board was attached, so
every `build_status` in [`catalog.json`](catalog.json) is `not-built`. Selection below is
reasoned from source reading and vendor/community reports, and is labelled as such.
