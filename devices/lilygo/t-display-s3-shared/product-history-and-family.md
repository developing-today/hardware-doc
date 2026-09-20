# LilyGO T-Display-S3 family — history and lineage

The dated timeline, the lineage diagram and the culture notes live in the base board's record,
because that is where a reader arrives:
**→ [`../t-display-s3/product-history-and-family.md`](../t-display-s3/product-history-and-family.md)**

This page adds only what is genuinely family-scoped.

## Launch order of the whole line

| Listed | Board | Note |
|---|---|---|
| ~2019 | TTGO T-Display (ESP32) | the ancestor |
| **2022-07-15** | **T-Display-S3** | the reference board |
| 2022-11-12 | T-Display AMOLED **Lite** 1.47″ | **first AMOLED**, despite the name |
| 2023-04-14 | T-Display-S3 AMOLED 1.91″ | |
| 2023-09-07 | T-Display-S3 **Pro** 2.33″ | |
| 2023-10-27 | T-Display-S3 **Long** 3.4″ | |
| 2023-11-03 | **T4-S3** 2.41″ | not named T-Display-S3 |
| 2024-07-18 | T-Display S3 AMOLED **(DS)** 1.43/1.64/1.75″ | four panels, one page |
| 2024-10-31 | T-Display-S3 AMOLED **Plus** | |
| 2025-11-28 | T-Display S3 Pro External | |

Dates are LilyGO's own `published_at` from the store feed, retrieved 2026-09-07.

## Repository health, 2026-09-07

A useful proxy for how much you can rely on each board's software.

| Repo | ★ | Forks | Open issues | Last push | Licence |
|---|---|---|---|---|---|
| `T-Display-S3` | **1 169** | 273 | **1** | 2026-08-31 | MIT |
| `LilyGo-AMOLED-Series` | 226 | 57 | **1** | 2026-05-06 | MIT |
| `T-Display-S3-AMOLED` | 182 | 36 | 1 | **2024-08-09 (dead)** | MIT |
| `T-Display-S3-Long` | 80 | 23 | **25** | 2026-06-15 | **none** |
| `T-Display-S3-Pro` | 63 | 17 | **22** | 2026-08-06 | **none** |
| `T-Display-S3-AMOLED-1.64` | 18 | — | 1 | 2026-07-22 | GPL-3.0 |
| `T-Display-S3-AMOLED-1.43-1.75` | 34 | — | — | 2026-06-17 | MIT |
| `LilyGo-Display-IDF` | 69 | — | — | 2025-11-03 | MIT |

**Read that table before choosing a board.** The base board and the AMOLED library are
maintained to a closed-issue state; **Long and Pro carry 25 and 22 open issues** and declare
**no licence at all**, which makes the redistribution status of their schematics and firmware
unknown. `T-Display-S3-AMOLED` is dead — use `LilyGo-AMOLED-Series`.

## Default branches are not `main`

An enumeration trap worth stating once. Three of these repositories default to a branch that
encodes a hardware or toolchain fact:

| Repo | Default branch | What it means |
|---|---|---|
| `T-Display-S3-Long` | **`T-Display-S3-Long-cst3530`** | a touch-controller revision |
| `T-Display-S3-AMOLED-1.64` | **`arduino-esp32-libs_V2.0.14`** | a pinned Arduino core |
| `T-CameraPlus-S3`, `T-Circle-S3` | `arduino-esp32-libs_V2.0.14` | as above |
| `T-Encoder-Pro` | `arduino-esp32-libs_V3.0.7` | a *different* pinned core |
| `T5S3-4.7-e-paper-PRO` | `H752-01` | an SKU |

**Always read `.default_branch` from the API; never assume `main`.** Recorded in
[`vendors/lilygo/README.md`](../../../vendors/lilygo/README.md).
