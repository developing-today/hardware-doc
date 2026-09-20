# Xteink X3 — research log

The **family-wide** log — source classes, Reddit and GitHub depth, dead links,
stopping criterion — is at [`../x4-pro/research-log.md`](../x4-pro/research-log.md).
The **second-sweep methodology and what it changed** is documented at
[`../x4/research-log.md`](../x4/research-log.md). This page records what was
X3-specific. Snapshot **2026-09-04**.

## X3-specific queries and outcomes

| Target | Depth | Outcome |
|---|---|---|
| `xteink x3` (Reddit) | 100 results | Bulk owner material |
| `xteink teardown`, `xteink teardown chip` | 100 each | **Found the only two Xteink teardowns that exist — both X3** |
| **`阅星瞳`**, **`星瞳 电纸书`** (Chinese) | 100 each | Surfaced the brand-spelling split (瞳 vs 曈) |
| `sunwoods/Xteink-X3` repo + tree | full | **Chinese hardware census + hand-drawn schematic + BOM incl. the NFC tag** |
| Imgur album `OA6CS2C` | full, via `ajaxalbums` | **13 captioned teardown images**, 650 mAh, "DS1307", ESP32-C3, 128 Mbit flash |
| `zocs/eink-quick-flasher` tree + firmware README | full | **Four published stock X3 images** (V1.0.7, V5.2.13 ×3) — the only Xteink with full-flash stock images published |
| `xteink nfc` + thread `1vit43t` with comments | full | **NFC purpose resolved** |
| GitHub **discussion** #2259 via GraphQL | full | **The authoritative NFC statement**, from the CrossInk maintainer |
| Thread `1vkuhbi` "Which x3 is newer?" with comments | full | **Four back-casing variants; a visible contrast/speed difference between two units; channel-vs-lock-state data** |

## Two retrieval techniques that were essential

**1. Imgur album enumeration.** `https://imgur.com/a/<id>` is a JavaScript shell;
scraping its HTML yielded **2 of 13** images. The undocumented endpoint
`https://imgur.com/ajaxalbums/getimages/<id>/hit.json` returns the full album with
**per-image captions, dimensions and upload timestamps**, unauthenticated, with a
plain browser UA. Without it, 11 of the 13 teardown photographs — including the
one captioned "DS1307 RTC" — would have been missed.

**2. GitHub GraphQL for discussions.** `api.github.com/search/*` **does not index
Discussions**. The single most authoritative statement about the X3's NFC tag
lives in `crosspoint-reader/crosspoint-reader` discussion **#2259** and is
reachable only via `gh api graphql`. Repository-only searching missed it entirely
on the first pass.

Both are recorded in [`commands.md`](commands.md).

## Negative results, deliberately preserved

| Searched for | Result |
|---|---|
| X3 **schematic** (formal) | **None.** The `sunwoods` `02.jpg` is a **hand-drawn sketch** whose author warns *"some components are substituted with other similar footprints"* |
| X3 **flash dump** | **Not obtained.** Four stock images exist as **Git LFS pointers**; blobs not fetched |
| X3 **partition layout** | **Not established.** Assumed to match the X4's; unverified |
| **UC8279d unit on a bench** | **Does not exist anywhere** — the SDK states so explicitly |
| Power measurements | **None**, despite a teardown performed expressly to make them |
| FCC / CE / SRRC | **None** — and the community explains why: *"Regulatory info is in software on mine, back is clean"* |

## The conflict this device generated

The X3 is the **only Xteink with independent teardowns**, and consequently the
only one where sources **disagree**: the RTC is called `DS3231` by the firmware,
`DS1307` by an English teardown caption, and `DS-series` by a Chinese teardown
that declines to narrow it.

**That is a feature of having more than one source, not a defect.** The other
models have no conflicts because they have no second opinion.

## Cheapest open actions, ranked

1. **Read `artifacts/teardown/sunwoods-cn/02.jpg`** — held here, unread. Would
   likely resolve the GPIO0/GPIO20 dual-assignment.
2. **Examine `13-Ay3rpJg.jpg` (5760×3240) at full resolution** — held here,
   unread. Would test the "DS1307" caption.
3. **Examine images 10/11** (*"at an angle to better read the chip labels"*) —
   would likely give the **Puya flash part number**.
4. Git-LFS fetch the four stock images.
5. Query the vendor OTA endpoint.

**Three of the top five require no network access at all** — the evidence is
already archived in this repository and has simply not been looked at.

## Stopping criterion

Two consecutive passes returned only duplicates for X3 hardware facts. Remaining
sources require: reading images already held (deferred), an LFS fetch (deferred),
Chinese marketplaces (declared exclusion), or hardware (unavailable).

**Reproducible broad-coverage snapshot dated 2026-09-04.**
