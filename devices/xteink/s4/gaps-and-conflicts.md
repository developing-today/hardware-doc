# Xteink S4 — gaps and conflicts

Snapshot **2026-09-04**.

## The overall state

**No hardware fact about the S4 is established.** Not one chip, not the panel, not
the panel controller, not the SoC. Everything in this record is a community-relayed
vendor claim or an ownership sighting.

The record exists because the device is real and is repeatedly used as the reason
people do *not* buy an X4 Pro — not because anything is known about it.

## Conflict 1 — the price differs by ~2×

| Source | Price | Market | Date |
|---|---|---|---|
| S01, relaying a Chinese announcement | **¥299** (limited to X3/X4 owners) / **¥339** regular ≈ **US$45–50** | China | 2026-04-23 |
| S02, AliExpress listing sighting | **~$99** | export | 2026-06-18 |

**Unresolved.** ¥339 ≈ US$47; the AliExpress figure is roughly double. Possible
explanations, none verified: an export markup, a bundle, a different
configuration, or a listing that was not genuine — the poster themselves wrote
*"don't know how legit it is"*.

**What would settle it:** an actual AliExpress or JD listing capture.

## Conflict 2 — "running crosspoint" on an Android device

The first owner sighting (S07, r/EDC, 2026-05-04, 750 points) describes:

> "Xteink S4 e reader (**running crosspoint**)"

**CrossPoint is ESP32 firmware. It cannot run on an Android device.**

Three explanations, in order of likelihood:

1. **The owner mislabelled an X3 or X4 as an "S4".** Strongly supported by
   precedent: the same corpus contains a post titled *"Got my white (?) X5"* whose
   author later edited it to *"EDIT: It's X4 and not X5."* Model confusion is
   demonstrably common in this community.
2. "S4" was used loosely as a brand/family name.
3. **The Android characterisation is wrong** — in which case the entire platform
   classification in this record is wrong.

**This is not resolved**, and it is flagged prominently because explanation 3
would invalidate the record's central premise. A second, later carry post (S08,
2026-07-06) also lists an "XTEINK S4" with no detail, so it does not help.

**What would settle it:** one photograph of an S4 running anything, or one
`Settings → About` screenshot.

## Gaps — the entire hardware stack

| Unknown | Note |
|---|---|
| **SoC** | Not named in **any** source. An Android 11 device with 2 GB/32 GB is almost certainly a Rockchip, Allwinner or UNISOC part — **not asserted**, because guessing a part number is exactly what the research method forbids |
| **RAM/storage type** | LPDDR? eMMC? Unknown |
| **Panel** | Size, resolution, PPI, colour depth all unknown |
| **Panel controller** | Unknown |
| **Touch controller** | Touch is claimed; the part is unknown |
| **Frontlight** | Cool/warm claimed; driver unknown |
| **Charging connector** | **Unknown** — and given the family's pogo-pin controversy, a first-order buyer question |
| **Radios** | Wi-Fi presumably; BT, cellular unknown |
| **Bootloader unlockability** | Unknown — the single most important question for this repository's purposes |

## Gaps — everything else

- **No firmware image, no build fingerprint, no partition layout.**
- **No teardown, no internal photograph, no retained external photograph.**
- **No confirmed international availability.** Absent from the vendor catalogue and
  from every collection — a weaker position than even the X4 Classic, which at
  least has an empty collection provisioned.
- **No regulatory filing.**
- **No FreeInk/CrossPoint support**, and none expected.

## What the vendor claims, unverified

From S01 (a relayed promotional image), all **single-sourced and unverified**:
1400 mAh · 6.98 mm · 95 g · Android 11 · 2 GB RAM · 32 GB storage ·
cool/warm frontlight · magnetic attachment · touch.

For scale: 95 g and 1400 mAh against the [X3](../x3/README.md)'s 55 g / 650 mAh
and the [X4](../x4/README.md)'s ~80 g. Internally consistent for a larger,
lit, Android device — which is weak corroboration, not confirmation.

## How to convert this stub into a real record

Ranked by cost-to-value:

| Action | Cost | Would establish |
|---|---|---|
| One owner posts `Settings → About` | minutes | **SoC, Android build, kernel** — the biggest single gap |
| One owner runs `adb shell getprop` | minutes | Full build fingerprint, board name, panel hints |
| Capture the AliExpress/JD listing | minutes | Price, dimensions, resolution, connector |
| Search Xiaohongshu / Douyin (**declared exclusion here**) | moderate | The vendor's actual primary channel |
| Retrieve S11, the Spanish community round-up | minutes | A secondary summary that may cite primaries |
| Teardown | high | Everything |

**A single owner with ADB could close most of this in an afternoon. In 2,136
Reddit posts, nobody has.**

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 74:* - **No regulatory filing.**
>

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment authorisations**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

The original finding confused **"no mark visible in a product photograph"** with **"no grant exists"**. Those are different claims, and only the first was tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is ordinary for a device with a screen. **That is a likely explanation and it was not verified.**

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

Listed in [`research/passes/index-merge/corrections-requiring-review.md`](../../../research/passes/index-merge/corrections-requiring-review.md).
