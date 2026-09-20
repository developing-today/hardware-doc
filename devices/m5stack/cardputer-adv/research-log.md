# Cardputer ADV — research log

> One session, **2026-09-04**. Declared depth, exclusions and stopping criterion at the end.
> Companion: [`commands.md`](commands.md) for the commands, [`sources.md`](sources.md) for the
> curated source table. This file is the **raw ledger**, including dead ends.

## Method

Followed [`vendors/m5stack/README.md`](../../../vendors/m5stack/README.md) §7 "per-product
procedure" as written, and it worked without modification. Order of work:

1. Vendor pages, EN + `zh_CN`, for all five family members → asset-URL extraction → product ids.
2. Schematics and mechanical drawings, hashed.
3. **Custom PDF text extractor** (no `pdftotext` on this host) → designator census → pin tables.
4. **Custom PNG cropper** → read the values off rendered sheets rather than trusting the text layer.
5. Vendor source repositories at pinned commits; read HALs and board tables, not READMEs.
6. GitHub ecosystem survey; then per-project build configs via `raw.githubusercontent.com`.
7. Reddit; Shopify; release history.

## Query ledger

### `docs.m5stack.com`

| Query / URL | Result | Disposition |
|---|---|---|
| `/en/core/Cardputer-Adv` | 200, 147 339 B | **primary source S1** |
| `/zh_CN/core/Cardputer-Adv` | 200, 146 690 B | control; **no CN-only asset delta** found (unlike PaperMono) |
| `/en/core/Cardputer` | 200 | S3 |
| `/en/core/Cardputer%20V1.1` | 200 | S2 |
| `/en/core/Cardputer_Mesh_Kit` | 200 | S4 — and the source of conflict C1 |
| `/en/CardputerZero` | 200, *"Work in progress"* | S5 |
| `/en/accessory/Cardputer%20Accessory%20Kit` | 200 | S6 |
| `/en/accessory/Cardputer%20Accessory%20Kit_v1.1` | **404, 4 162 B** | **dead — recorded**; the `_v1.1` form does not exist |
| `/en/history` | 200 | S7 — dated the three CAP/kit releases |
| `/en/certification` | **not fetched** | ⚠ **gap.** The vendor guide flags it as a *soft gap* needing a positive control; that control was not run. "Not established", not "absent". |
| `/en/product_i2c_addr` | **not fetched** | same |
| `/en/uiflow2/cardputer-adv/program` | **not fetched** | gap; noted that the path differs from the v1.x |
| `/en/arduino/m5cardputer/program` | **not fetched** | gap |
| `/en/guide/lora/meshtastic/cardputer_mesh_kit` | **not fetched** | gap; belongs mostly to the Mesh Kit record |

### Aliyun OSS asset enumeration

Product ids recovered from asset URLs: **ADV `1178`**, **v1.1 `1127`**, **v1.0 `481`**,
**Stamp-S3A `1150`**, **StampS3 `522`**, **Mesh Kit `1240`**, **CardputerZero `1243`**,
Cap LoRa-1262 `1208`, Cap CC1101 `1250`, SX1262 `1177`, CASIC protocol `1173`.

| Asset | Result |
|---|---|
| `1178/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf` | 200, 878 155 B — **retained** |
| `1178/…_page_0{1..4}.png` | 200 ×4, 5848×4132 — **retained in scratch, crops made** |
| `1178/K132-Adv-cardputer-ADV.pdf` | 200, 127 977 B — **retained** |
| `1150/Sch_StampS3_v0.3.3.pdf` | 200, 369 766 B — belongs to the component |
| `1127/Sch_M5Cardputer.pdf` + `481/Sch_M5Cardputer.pdf` | 200 — **byte-identical**, finding C3 |
| `522/Sch_M5StampS3_v0.2.pdf` | 200, 348 884 B — the v1.0 Stamp |
| `522/Sch_M5StampS3_v0.2_page_01.png` | **402 B, not a PNG** — **dead, recorded**; the render convention is not universal |
| `1178/IMU-Cardputer-Adv.jpg`, `1178/Cardputer-Adv_{01..13}.webp`, `K132-Adv-weight.jpg` | URLs recorded; **not retained** — imagery unlicensed |
| `1178/Easy_Loader_for_Cardputer-Adv.exe` | **not downloaded** — gap |
| `1243/C154-CardputerZERO_SCH_V0.6.1_20260702.pdf`, `1243/CardputerZero_Labels.zip` | **not downloaded** — CardputerZero record is deliberately lighter |

### GitHub

| Query | Depth | Result |
|---|---|---|
| `gh search repos cardputer --limit 100` | 100 (**API cap**) | ~40 catalogued in [`projects-and-community.md`](projects-and-community.md); the rest are duplicates/forks/thin |
| `gh search repos "M5Stick-Launcher"` | 12 | only derivatives — led to discovering the **rename** to `bmorcelli/Launcher` |
| `gh search repos "marauder cardputer"` | 12 | **0 results** — a false negative; `gh api search/code` inside the repo found 17 files including `User_Setup_marauder_m5cardputer_adv.h`. **Repo search is not a substitute for code search.** |
| `gh search repos "nemo esp32"` | 12 | 0 useful — same lesson |
| `gh search repos "M5Launcher"` | 12 | community ports and `CCP101/cardputer-recoverable-multiboot` |
| `gh api repos/{pr3y/Bruce, bmorcelli/M5Stick-Launcher, justcallmekoko/ESP32Marauder, n0xa/m5stick-nemo, meshtastic/firmware, BruceDevices/firmware, 7h30th3r0n3/Evil-M5Project}` | direct | **two renames discovered** |
| `gh api search/code repo:… cardputer` ×3 | full | Marauder 17 hits, NEMO 15, Meshtastic 9 |
| `gh api repos/meshtastic/firmware/contents/variants` | full | **no top-level `cardputer`** — the variant is at `variants/esp32s3/m5stack_cardputer_adv/`. A directory listing at the wrong level produced a false negative first. |
| `raw.githubusercontent.com` fetches of 6 build configs | — | all 200 |
| `gh api repos/BruceDevices/firmware/contents/boards` | full | `m5stack-cardputer` — a **directory**, and the `.ini` is *inside* it. First guess (`boards/m5stack-cardputer.ini`) 404'd. |

### Reddit

`old.reddit.com/search.json` with `User-Agent: WhatsApp/2.23.20.0`, three queries, `limit=25`,
`t=all`:

| Query | Sort | Results | Useful |
|---|---|---|---|
| `cardputer adv` | relevance | 25 | 20 |
| `cardputer` in `r/M5Stack` | new | 25 | 14 |
| `cardputer` | relevance | 25 | 15 |

Plus four comment threads fetched in full (`/comments/{id}.json?limit=20`): `1tsr5ke`,
`1vcxsv8`, `1vgmcvn`, `1vv4jk3`. **~75 threads reviewed, ~12 quoted.** Subreddits observed:
r/CardPuter (dominant), r/CardPuterZero, r/M5Stack, r/cyberDeck, r/synthdiy, r/meshtastic,
r/flipperzero, r/hacking (no Cardputer-specific hits in the sample).

### Shopify

`search/suggest.json?q=cardputer` → 10 products; `<handle>.json` for four of them.
**Discovered `[EOL]` on the v1.1** — which no documentation page states.

### Not searched

* **Chinese-language sources** beyond the `zh_CN` docs mirror. No Bilibili, Zhihu, Taobao,
  CSDN or WeChat search was run. Given M5Stack is a Shenzhen company this is a real gap.
* **Japanese sources** — the `/ja/` docs tree exists and was not fetched; M5Stack has a large
  Japanese community (`shikarunochi`, `GOROman`, `Gitshaoxiang` all appear in the repo list).
* Hackaday, Hackster, YouTube, Discord.
* AliExpress, Amazon, Taobao, distributor pricing.
* FCC ID / CE / TELEC databases.
* `community.m5stack.com` — **auth-walled**, no determination possible.
* `github.com/m5stack/M5_Hardware` — the docs link `Products/K132-Adv_Cardputer-Adv/Structures`
  and `Products/K152_Cardputer_Mesh_Kit/Structures`; **neither was fetched.**

## Dead ends and corrections, in order

1. **`pdftotext` absent** → wrote `pdfbbox.py`. Three silent failure modes, each fixed and
   documented in [`commands.md`](commands.md) §4. The Form-XObject one is the dangerous one: the
   output *looks* plausible while containing none of the readable text.
2. **`file` absent** → magic-byte checks in Python instead.
3. **No image library** → wrote `pngcrop.py`.
4. **`curl` glob error** on the Shopify bracket syntax → `-g`.
5. **`522/…_page_01.png` is not a PNG** → the render convention is per-product, not universal.
6. **`gh search repos` false negatives** for Marauder and NEMO → always follow with
   `gh api search/code` scoped to the repo.
7. **Meshtastic variant not at `variants/<name>`** but `variants/esp32s3/<name>` → listing one
   directory level is not a search.
8. **Two repository renames** (`pr3y/Bruce`, `bmorcelli/M5Stick-Launcher`) → resolve canonical
   names via `gh api repos/{old}` before concluding a project is gone.
9. **Assumed v1.1 used StampS3** (a widely repeated community belief) → **refuted** by M5Stack's
   own comparison table and the v1.1 page: v1.1 already uses Stamp-S3A. Recorded in
   [`gaps-and-conflicts.md`](gaps-and-conflicts.md).
10. **Assumed the ADV redesigned the keyboard matrix** → **refuted**: identical matrix, identical
    nets, identical designators; only the scanner changed.

## Concurrent sessions

At the time of writing, another session was actively creating
`components/m5stack/stamp-s3`, `stamp-s3a`, `unidentified/m5stack-stamp-s3a/dcdc-u4`,
`silergy/sy7088`, `sgmicro/sgm2578`, `generic/tp4057`, `sitronix/st7789v2` and
`devices/m5stack/cap-lora-1262/` (mtimes within 30 minutes). **Those trees were not written to.**
This record links to them and leaves proposed *Used By* additions in
[`scratch/m5stack-cardputer/index-fragments.md`](../../../scratch/m5stack-cardputer/index-fragments.md).

## Stopping criterion

Stopped when the **primary evidence was exhausted for the ADV specifically**: every published
vendor asset for product id `1178` was enumerated and either retrieved or recorded; the
schematic's designator census was complete with no gaps in the `U` sequence; all four vendor
source repositories were read at pinned commits; and the GitHub repo search hit its 100-result
cap with the last two passes returning only duplicates and thin forks.

**Not** stopped because the internet was exhausted. The declared exclusions above — Chinese and
Japanese sources, certification databases, `M5_Hardware`, M5Burner, marketplace pricing — are
each a real avenue that a further pass should take. This is a **reproducible broad-coverage
snapshot dated 2026-09-04**, not a completeness claim.
