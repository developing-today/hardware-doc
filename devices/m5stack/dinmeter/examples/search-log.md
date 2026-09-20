# DinMeter — example search log

**Snapshot 2026-09-04.** Every search that contributed to [`catalog.json`](catalog.json),
including the ones that returned nothing.

## Official sources

| Source | Method | Result |
|---|---|---|
| `m5stack/M5DinMeter` `examples/` | tarball @ `8ccbad7297beb82a140f812e5606e060d8a5e0dc` | **6 examples**, all under `examples/Basic/`, all dated 2024-03-07 |
| `m5stack/M5DinMeter-UserDemo` | tarball @ `d2fdfe44e9baf810f82335faa6f5962e9fc59a44` | **1 integrated application** with 8 test components |
| `docs.m5stack.com/en/arduino/m5dinmeter/*` | 9 pages fetched, all HTTP 200 | Tutorial prose mirroring the six examples plus `battery`, `wifi`, `program` |
| `docs.m5stack.com/en/uiflow2/m5dinmeter/program` | fetched, HTTP 200 | UiFlow2 tutorial (block-based; no downloadable source project) |
| `espressif/esp-board-manager` | raw fetch @ `2beb9b22b0892b343bd555a1ebc9929a7edce8fc` | **3 YAML board files** — not "examples" but the single best reference configuration |

## Community searches

| Query | Endpoint | Results | Kept |
|---|---|---:|---:|
| `DinMeter in:name,description,readme` | GitHub repo search, 50/page | 19 | 13 |
| `DinMeter` | GitHub repo search | 5 | — (subset) |
| `M5DinMeter` | GitHub repo search | 6 | — (subset) |
| `din meter m5stack` | GitHub repo search | 2 | — (subset) |
| `M5DinMeter extension:h` | GitHub code search | 9 files / 6 repos | 4 new |
| `DinMeter in:file language:yaml` | GitHub code search | 94 | 3 (rest are false positives) |
| `din_meter` | GitHub code search | 109 | 1 (dominated by `whatnick/din_meter_atm90e26`, unrelated) |
| `repo:bmorcelli/Launcher dinmeter` | GitHub code search | 6 | 1 repo, high value |
| `repo:esphome/esphome dinmeter` | GitHub code search | **0** | — |
| `repo:arendst/Tasmota dinmeter` | GitHub code search | **0** | — |
| `repo:meshtastic/firmware dinmeter` / `din_meter` | GitHub code search | **0** / **0** | — |
| `repo:pr3y/Bruce dinmeter` | GitHub code search | **0** | — |
| `DinMeter`, `Din Meter M5Stack`, `M5Stack knob DIN`, `subreddit:M5Stack dinmeter` | `old.reddit.com/search.json` | ~200 inspected | 1 (marketing) |
| `dinmeter` | `community.m5stack.com` API + HTML | **HTTP 401** / JS shell | **blocked** |

## Deduplication and lineage

- **6 Launcher forks** (`notyetaperson/Evilware`, `darkLabz001/Dark-Div-Launcher`,
  `TeslaDeathStar/ESP32-Launcher-ES3C28P`, `ry-ops/tab5-launcher`,
  `JunFactorya04/M-5Laucher{,2}`) inherit the DinMeter board file from `bmorcelli/Launcher`.
  Catalogued once, with lineage noted; not counted as independent examples.
- `pfefferle/palnagotchi` is a fork of `viniciusbo/m5-palnagotchi`. Lineage recorded.

## Naming traps that cost time

| Trap | Cost |
|---|---|
| `din_meter` → `whatnick/din_meter_atm90e26` (unrelated ATM90E26 energy meter, ~15 Gerber files) | ~40 % of one code-search page |
| `din_meter` → EV-charging **DIN 70121** (`din_msgDefDatatypes.c`, EVerest / SmartEVSE) | noise |
| "DIN meter" on Reddit → **ski-binding release settings** (r/Skigear) | 1 of 2 relevant-looking hits |
| Bruce vs Launcher | `pr3y/Bruce` has **no** DinMeter support; `bmorcelli/Launcher` does |

## Declared exclusions

No video, blog, Hackaday.io, Chinese-platform, or package-registry-wide search was performed.
The vendor forum was inaccessible. See [`../research-log.md`](../research-log.md) §9.

## Build status

**Zero examples were built, statically validated or run.** No toolchain was installed and no
hardware was available. Every catalogue entry's `build_status` is `not-attempted`.
