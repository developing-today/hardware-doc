# DinMeter — product history, family and culture

Dated timeline from primary evidence. Where a date is a *proxy* (a repository creation date, a
shop `published_at`) it says so rather than presenting it as an announcement date.

---

## 1. Timeline

| Date | Event | Evidence | Kind |
|---|---|---|---|
| 2023-02-10 | **Stamp-S3 (`S007`) listed** on shop.m5stack.com | shop `.js` `published_at` | proxy for launch |
| 2024-02-21 | `m5stack/M5DinMeter` repository created — the earliest DinMeter artefact anywhere | GitHub API `created_at` | firm |
| 2024-03-01 | `m5stack/M5DinMeter-UserDemo` repository created | GitHub API | firm |
| 2024-03-04 | UserDemo release **`V0.1`** — the factory firmware | GitHub release | firm |
| 2024-03-07 | `M5DinMeter` release **`1.0.0`**; all six examples dated the same day | GitHub release + file headers | firm |
| **2024-03-08** | **DinMeter (`K134`) listed on the shop** at USD 24.50 | shop `.js` `published_at` | proxy for launch |
| 2024-04-14/15 | `shi78ge/DinMeter-chan` — the first third-party project, ~5 weeks after launch | GitHub | firm |
| 2025-04-26 | `kaz-mac/M5Authenticator` with a dedicated `DinMeterUI.h` | GitHub | firm |
| **2025-09-11** | **Stamp-S3A (`S007-…-V033`) listed** | shop `.js` | proxy for launch |
| 2025-09-26 | `aoiastro/susuFW` last push | GitHub | firm |
| 2025-12-10 | `tarmn3/m5dinmeter-ble-volume-knob` | GitHub | firm |
| **2026-01-30** | **DinMeter v1.1 (`K134-V11`) announced.** Shop `created_at 10:02:16+08:00`, `published_at 12:30:47+08:00`; official r/M5Stack weekly post the same day | shop `.js` + Reddit | firm, two sources |
| 2026-06-27 | `TuF3i/DinMeterDock` | GitHub | firm |
| 2026-08-03 | Last push to `m5stack/M5DinMeter` — still `version=1.0.0`, no new release | GitHub | firm |
| 2026-08-08 | `Shark17e/M5DinMeter-KilnController` | GitHub | firm |
| 2026-09-03 | `espressif/esp-board-manager` DinMeter board definition at HEAD `2beb9b22…` | GitHub | firm |
| **2026-09-04** | Observed: **`K134` and `S007` both marked `[EOL]` and out of stock**; `K134-V11` and `S007-V033` in stock | shop `.js` | firm |

### What the timeline shows

**The v1.1 is a module-lifecycle event, not a product refresh.** The Stamp-S3A appeared
2025-09-11; the DinMeter v1.1 followed 4½ months later; and the Stamp-S3 and DinMeter K134 went
`[EOL]` together. M5Stack re-released the carrier to consume the new module, at the same price,
with the same PCB documentation. That reading is consistent with every artefact: no new
schematic, no new STL, no new footprint, no new library release, no new M5Unified board enum.

**The Arduino library has not been touched functionally since launch.** Release `1.0.0`,
2024-03-07; HEAD in 2026 is still `1.0.0`. Whatever maintenance happens, happens in M5Unified.

## 2. Family

The DinMeter sits in a tight M5Stack cluster of **Stamp-S3 carriers with a knob and a small
LCD**, and they share a single code path.

| Product | SKU | Shape | Display | Touch | Input voltage | Distinguishing feature |
|---|---|---|---|---|---|---|
| **DinMeter** | K134 / K134-V11 | rectangular, panel-mount | 1.14 in 135 × 240 | no | **6–36 V** | **1/32 DIN cutout** |
| M5Dial | K130 / K130-V11 | round puck | 1.28 in 240 × 240 round | **yes** | 5 V | round + touch |
| M5Capsule | — | capsule | — | — | 5 V | shares the same M5Unified switch cases |
| M5AirQ | — | box | — | — | 5 V | air-quality sensors |
| VA Meter | — | — | — | — | — | voltage/current instrument, Stamp-S3 |
| StamPLC | — | DIN-**rail** | — | — | — | relays, CAN, RS485 — different category |

**The shared code path is literal.** M5Unified handles `board_M5Dial`, `board_M5DinMeter` and
`board_M5Capsule` in the *same switch cases* for buttons (`M5Unified.cpp:3502`), buzzer
(`:2921`), pin setup (`:2400`) and power hold (`:282`), and gives Dial and DinMeter identical
I²C (`:96`) and Port-B (`:159`) rows.

**And the lineage is visible in the source.** `M5DinMeter.h` opens with `#define M5DIAL_H` and
defines `DIAL_ENCODER_PIN_A` / `DIAL_ENCODER_PIN_B`. The library was copied from the M5Dial's and
the names were never changed. That is not a criticism — it is the clearest possible statement
that the two are the same device in different shells.

## 3. Positioning and intended audience

M5Stack's own applications list, identical in spirit on both pages: smart-home monitoring and
control, access control, industrial control, maker/DIY.

The v1.1 description is more explicit about the thesis than the v1.0's was:

> "…adopts the 1/32 DIN standard digital meter cutout size, allowing direct installation into
> reserved mounting openings of mainstream equipment such as **industrial control cabinets and
> PLC control boxes, without the need for custom brackets or panel modifications**. This
> significantly reduces integration cost and assembly time."

That is a **retrofit** pitch aimed at people with existing panels — a narrower and more
industrial audience than most M5Stack products, and it explains the community profile in §4.

## 4. Culture — there isn't much of one, and that is informative

A broad sweep on 2026-09-04 found **13 third-party GitHub repositories** genuinely targeting the
device, **one** Reddit post in the entire index (M5Stack's own launch announcement, with one
comment), **no** ESPHome/Tasmota/Meshtastic support, and a vendor forum that could not be
enumerated (HTTP 401).

The projects that do exist are revealing: a kiln controller, a power-tool battery analyser, a
heater controller, a TOTP authenticator, a BLE volume knob, a desktop dock. **Nine of thirteen
are one-person, single-purpose instruments.** That is a product being used precisely as
intended, by people who had a panel and a problem — not a platform with a scene around it.

The one genuine ecosystem contribution is `bmorcelli/Launcher` (★2054), which carries the
DinMeter as a first-class board target in its release CI.

Full catalogue and evidence types: [`projects-and-community.md`](projects-and-community.md).

## 5. Naming traps this product creates

Worth recording, because each cost search time:

| Trap | Detail |
|---|---|
| `docs.m5stack.com/en/core/**DinMeter**` | **404.** The page id is `M5DinMeter`; only the *v1.1* page uses `DinMeter_v1.1` |
| Shop slug | `m5stack-din-meter-**w**-m5stamps3`, not `-with-`. The v1.1 uses `-with-` |
| "DIN" | Means the **panel cutout** (DIN 43700, 45 × 22.5 mm), **not** DIN rail |
| `din_meter` as a search term | Collides with `whatnick/din_meter_atm90e26` (an unrelated ATM90E26 energy meter) and with EV-charging **DIN 70121** protocol code |
| "DIN meter" on Reddit | Overwhelmingly **ski-binding release settings** |
| Stamp-S3A schematic filename | `Sch_StampS3_v0.3.3.pdf` — no "A" in it |
| Stamp docs path | `/en/core/StampS3`, **not** `/en/stamp/…` |

## Related

[`market-and-pricing.md`](market-and-pricing.md) · [`projects-and-community.md`](projects-and-community.md) ·
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) ·
[`../dinmeter-v1.1/stamp-s3-to-s3a-delta.md`](../dinmeter-v1.1/stamp-s3-to-s3a-delta.md)
