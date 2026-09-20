# Xteink S4

> **STUB.** This is an **Android** device, not an ESP32 device, and it is
> therefore outside the CrossPoint / FreeInk firmware ecosystem that the rest of
> this tree documents. Research retrieval date **2026-09-04**.
>
> **State this plainly: no board-level fact about the S4 is established here.**
> There is no teardown, no firmware dump, no board profile, no schematic and no
> chip identification of any kind. Everything below is a community-relayed vendor
> claim.

## Why it has a record at all

Three reasons:

1. It is a **real, shipping Xteink product** and the family index would be wrong
   without it.
2. It is the device the community repeatedly says they will buy **instead of** the
   X4 Pro, so it belongs in that comparison.
3. Recording it as a **stub with named gaps** stops the next agent from
   re-discovering it and assuming it was missed.

## Identity

| Field | Value | Evidence |
|---|---|---|
| Name | **Xteink S4** | **[COMM]** |
| Platform | **Android 11** | **[COMM]** AliExpress preorder listing, relayed |
| Class | Small Android e-ink reader | — |
| Market | **China first.** *"Android-based S4 in the works, **China-only so far**"* | **[COMM]** [r/XTEINK `1v5gh6x`](https://old.reddit.com/r/XTEINK/comments/1v5gh6x/), 2026-07-24 |
| Status | Shipping to owners; still not on `xteink.com` | **[COMM]** + **[VENDOR]** absence |

**Not present in the vendor's international catalogue.** The `xteink.com`
`/products.json` and all 11 collections were retrieved on 2026-09-04 and contain
**no S4 product and no S4 collection**.

## Claimed specifications — all single-sourced, none verified

From [r/XTEINK `1stni9p`](https://old.reddit.com/r/XTEINK/comments/1stni9p/)
(2026-04-23, 178 pts), relaying a Chinese announcement image:

| Property | Claim |
|---|---|
| Battery | **1400 mAh** |
| Thickness | **6.98 mm** |
| Mass | **95 g** |
| OS | **Android 11** |
| RAM | **2 GB** |
| Storage | **32 GB** |
| Frontlight | **cool / warm** |
| Attachment | magnetic |
| Touch | yes |

From [r/XTEINK `1u9ctsr`](https://old.reddit.com/r/XTEINK/comments/1u9ctsr/)
(2026-06-18), an AliExpress preorder listing: *"android 11, 2gb ram and 32gb
storage… Price ~$99"* — **conflicts with the ¥299/¥339 Chinese pricing below.**

**No SoC is named in any source.** That is the single most conspicuous gap: an
Android 11 device with 2 GB/32 GB is almost certainly a Rockchip, Allwinner or
UNISOC part, but **no source says which and none is asserted here.**

## Pricing

| Date | Price | Market | Source |
|---|---|---|---|
| 2026-04-23 | **¥299** (limited to existing X3/X4 owners) · **¥339** regular ≈ **US$50 / €45** | China | [r/XTEINK `1stni9p`](https://old.reddit.com/r/XTEINK/comments/1stni9p/) |
| 2026-06-18 | **~$99** | AliExpress preorder | [r/XTEINK `1u9ctsr`](https://old.reddit.com/r/XTEINK/comments/1u9ctsr/) — poster themselves says *"don't know how legit it is"* |

**Unresolved conflict.** ¥339 ≈ US$47; the AliExpress figure is roughly double.
Either the export price carries a large markup, or the listing was not genuine.
Neither was verified.

## Timeline

| Date | Event | Source |
|---|---|---|
| 2025-12-26 | Community digest: *"S4 updates (still in development, no date yet)"*; frontlight is *"the #1 feature request for X5/S4"* | [`1pw0r4y`](https://old.reddit.com/r/xteinkereader/comments/1pw0r4y/) |
| 2026-04-20 | Price announcement teased for 25 Apr; YouTube shorts posted | [`1sqawqd`](https://old.reddit.com/r/xteinkereader/comments/1sqawqd/), 100 pts |
| 2026-04-23 | **Price and preorder details drop in China.** Preorders 27 Apr, 8 pm–midnight Beijing time | [`1stni9p`](https://old.reddit.com/r/XTEINK/comments/1stni9p/), 178 pts |
| 2026-04-23 | "XTEINK S4" discussion thread — **277 pts, 170 comments** | [`1stpb4n`](https://old.reddit.com/r/xteinkereader/comments/1stpb4n/) |
| 2026-05-04 | **First owner sighting in the wild** — an r/EDC carry post lists *"Xteink S4 e reader (running crosspoint)"* | [`1t3o12l`](https://old.reddit.com/r/EDC/comments/1t3o12l/), 750 pts |
| 2026-06-13 | *"XTEINK S4, Latest Video (June Production Run)"* — *"Finally a backlight."* | [`1u4ty4q`](https://old.reddit.com/r/XTEINK/comments/1u4ty4q/), 94 pts |
| 2026-06-18 | AliExpress preorder spotted | [`1u9ctsr`](https://old.reddit.com/r/XTEINK/comments/1u9ctsr/) |
| 2026-07-06 | Second owner sighting in an r/EDC carry post | [`1uow72f`](https://old.reddit.com/r/EDC/comments/1uow72f/), 129 pts |
| **2026-09-03** | *"Demo Video of the S4"* — *"Video repost from XTEINK's red note account"* | [`1w6kx38`](https://old.reddit.com/r/XTEINK/comments/1w6kx38/), 41 pts |

## An unresolved anomaly worth flagging

The 2026-05-04 r/EDC post describes an **"Xteink S4 e reader (running
crosspoint)"**. **CrossPoint is ESP32 firmware. It cannot run on an Android
device.**

Three possible explanations, none verified:
1. The owner mislabelled an X3 or X4 as an "S4".
2. "S4" is being used loosely as a family name.
3. Something is wrong with the Android characterisation of the S4.

Given the same corpus contains a post explicitly titled *"Got my white (?) X5"*
that the author later corrected to "X4", **explanation 1 is the most likely** —
but this is recorded rather than assumed, because if explanation 3 is true, the
whole platform classification here is wrong.

## Why the community wants it

> "I'm actually interested in the S4 BECAUSE it has android, I wanna get a device
> that can fit in my pocket and can go online. This is because I want to be able
> to read from sites like scribblehub and ao3."
> — [r/ereader `1tszjnb`](https://old.reddit.com/r/ereader/comments/1tszjnb/), 2026-05-31, 72 pts

> "I probably will abandon both once the S4 is released."
> — [r/xteinkereader `1syav96`](https://old.reddit.com/r/xteinkereader/comments/1syav96/), 412 pts

The appeal is **apps and a browser** in a pocket form factor, plus a frontlight —
which the X3 and X4 lack and which was the community's top request.

## What would make this a real record

| Needed | Difficulty |
|---|---|
| **SoC identification** | Easy for an owner — `Settings → About`, or any device-info app |
| Build fingerprint / Android build props | Easy for an owner with ADB |
| Panel size, resolution, controller | Easy for an owner |
| A teardown | Moderate |
| Whether the bootloader is unlockable | Moderate |
| An international listing or price | Depends on the vendor |

**A single owner with ADB access could convert this stub into a substantial
record in an afternoon.** No such report exists in 1,798 posts.

## Explicit gaps

- **No SoC, RAM type, panel part, panel controller, or any chip whatsoever.**
- No teardown, no photograph retained, no firmware image, no partition layout.
- No confirmed international availability or price.
- No FCC/CE/SRRC record.
- **No FreeInk/CrossPoint support** and none expected — different architecture.
- The "running crosspoint" anomaly above is unresolved.

## See also

[Family index](../README.md) ·
[X4 Pro comparison](../x4-pro/comparisons-and-recommendations.md) — where the S4
is the strongest non-programmable alternative
