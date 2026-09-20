# Cardputer ADV — example search log

> **2026-09-04.** Declared depth and exclusions at the end.

## Sources searched

| Source | Query / path | Depth | Useful | Notes |
|---|---|---|---|---|
| Vendor library | `M5Cardputer/examples/**` at `f1392858` | full tree, 13 sketches | **13** | all MIT, all vendored |
| Vendor firmware | `M5Cardputer-UserDemo` branches | `main` + **`CardputerADV`** | 2 | ADV code is on a **branch**, easy to miss |
| GitHub repo search | `gh search repos cardputer --limit 100` | 100 = **API cap** | ~40 catalogued in [`../projects-and-community.md`](../projects-and-community.md) | true count is higher |
| GitHub repo search | `M5Stick-Launcher`, `marauder cardputer`, `nemo esp32`, `M5Launcher` | 12 each | mixed | **two of the four returned false negatives** — see below |
| GitHub code search | `repo:{justcallmekoko/ESP32Marauder, n0xa/m5stick-nemo, meshtastic/firmware} cardputer` | full | 17 / 15 / 9 files | **this is what repo search missed** |
| GitHub contents API | `boards/`, `variants/`, `configs/` in five upstreams | one level, then drill | — | see the two directory-depth traps below |
| raw.githubusercontent | 6 build configs at `HEAD` | — | 6 | no auth, no rate limit |
| Reddit | 3 searches + 4 comment threads | ~75 threads reviewed | ~12 quoted | project announcements are a *primary* discovery channel here |
| Awesome-lists | `terremoth/awesome-m5stack-cardputer`, `ru84r8/Cardputer-firmware-list` | noted, **not mined** | — | **gap** — a further pass should walk both |

## Traps hit, in order

1. **`gh search repos "marauder cardputer"` → 0 results.** Marauder *does* support the ADV;
   `gh api search/code -f q='repo:justcallmekoko/ESP32Marauder cardputer'` returns 17 files
   including `User_Setup_marauder_m5cardputer_adv.h`. **Repo search matches metadata, not
   content.** Same false negative for NEMO.
2. **`gh api repos/meshtastic/firmware/contents/variants | grep card` → nothing.** The variant is
   at `variants/**esp32s3**/m5stack_cardputer_adv/`. Listing one directory level is not a search.
3. **`boards/m5stack-cardputer.ini` → 404.** In Bruce it is a *directory*:
   `boards/m5stack-cardputer/m5stack-cardputer.ini`, alongside `interface.cpp` and
   `pins_arduino.h`. List before guessing.
4. **Two renames.** `pr3y/Bruce` → `BruceDevices/firmware`; `bmorcelli/M5Stick-Launcher` →
   `bmorcelli/Launcher`. The GitHub API follows the redirect silently, so `gh api repos/{old}`
   still works — but a repository *search* for the old name finds only derivatives. Resolve
   canonical names before concluding a project is dead.
5. **The ADV firmware is a branch, not a repo.** `M5Cardputer-UserDemo` `main` is the v1.x
   firmware. Checking only the default branch would have missed the entire ADV application.

## Result disposition

| Status | Count |
|---|---|
| Catalogued | **25** |
| Selected | 14 |
| Vendored | 13 (all MIT, all from the vendor library) |
| Rejected with a stated reason | 11 |
| **Built or run** | **0** — no toolchain, no hardware |

## Not searched

* PlatformIO registry, Arduino Library Manager
* Hackster.io, Hackaday.io, Instructables
* YouTube (several projects are announced there first)
* M5Stack's own forum — **auth-walled**, no determination possible
* Chinese- and Japanese-language ecosystems. Several prolific Cardputer authors are Japanese
  (`shikarunochi`, `GOROman`, `Gitshaoxiang`) and at least two projects are Chinese-language
  (`fwz233-RE/M5Claw`, `nongxl/SkyCompass_CardputerADV`, `CCP101/cardputer-recoverable-multiboot`).
  **This is the largest single gap in the example survey.**
* The two curated awesome-lists, which almost certainly contain projects GitHub's 100-result cap
  hid.

## Stopping criterion

Stopped when the vendor's own example tree was exhausted, the five named upstreams had each been
resolved to a concrete build target or a stated negative, and GitHub repo search had hit its cap
with the last two query families returning only forks and duplicates. **Not** a completeness
claim — the exclusions above are real and enumerated.
