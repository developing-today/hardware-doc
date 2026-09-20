# Xteink X4 Pro — product history and family

Full family context: [`../README.md`](../README.md).

## Timeline

| Date | Event | Evidence |
|---|---|---|
| 2026-06-13 | An S4 promotional video also shows unannounced hardware | **[COMM]** [r/XTEINK `1u4ty4q`](https://old.reddit.com/r/XTEINK/comments/1u4ty4q/) |
| **2026-06-22** | Community spots **a new X4 variant** in a vendor video — *"Physical buttons + frontlight but no touchscreen"*, **300 pts**. They were describing what became the [X4 Classic](../x4-classic/README.md) | **[COMM]** [`1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/) |
| 2026-07-07 | X4 Pro Shopify product record **created** | **[VENDOR]** |
| 2026-07-17 | Pre-launch poll: *"are you going to buy the X4 Pro? Or the S4?"*, 89 comments | **[COMM]** [`1uz9mtg`](https://old.reddit.com/r/xteinkereader/comments/1uz9mtg/) |
| **2026-07-21** | **Launch**, $99, Space Black only. Listed as pre-order with restock 6 Aug | **[VENDOR]** |
| 2026-07-21 | **Pogo-pin backlash** begins — 71 + 46 comments across two subreddits | **[COMM]** [`1v2txxe`](https://old.reddit.com/r/xteinkereader/comments/1v2txxe/) |
| 2026-07-22 | First unboxings — *"XTEINK X4 Pro Unboxing & First Look - Is It Any Good?"* (31 + 38 pts) | **[COMM]** |
| 2026-07-22 | *"X4 Pro **pogo pin charging loose?**"* — an early quality report | **[COMM]** [`1v3d…`](https://old.reddit.com/r/XTEINK/) |
| 2026-07-24 | *"xteink x4 pro on crosspoint: dark mode"* — community firmware running within 3 days of launch | **[COMM]** r/eink |
| 2026-07-26 / 07-28 | Matte, then tempered-glass screen protectors listed | **[VENDOR]** |
| 2026-07-30 | *"Official X4 Pro Shipping Updates"*, 100 pts | **[COMM]** |
| **2026-08-16** | *"**Easy fix for X4 Pro's magsafe alignment**"*, 44 pts — a second mechanical complaint | **[COMM]** |
| 2026-08-18 | CrossInk adds an `x4pro` device type to its bug-report template | **[SRC]** `uxjulia/CrossInk` commit |
| 2026-08-20 | *"can we install crosspoint on XTEINK X4 PRO **CHINA FIRMWARE**"* — a China/international firmware split becomes visible | **[COMM]** |
| **2026-08-27** | **Stock firmware 7.4.4 built**, ESP-IDF 6.0.1 | **[DUMP]** app descriptor |
| 2026-08-23 | Owners of all three models: *"the pro makes the other two feel obsolete"* | **[COMM]** [`1vw6haq`](https://old.reddit.com/r/XTEINK/comments/1vw6haq/) |
| 2026-09-04 | **$99, in stock.** Matte protectors and 2/3-packs of glass **sold out** | **[VENDOR]** |

## Position in the family

The X4 Pro is the **fourth ESP32 device and the current flagship**. It is the first
Xteink to move from ESP32-C3 to **ESP32-S3 with 8 MB PSRAM**, and the first — and
still only — with **touch** and a **frontlight**.

| Relationship | Device |
|---|---|
| Namesake predecessor | [X4](../x4/README.md) — **a completely different computer.** Same screen size and brand; different SoC architecture, flash layout, input hardware and charging connector |
| Board sibling | [X4 Classic](../x4-classic/README.md) — the same S3 board minus touch and frontlight, plus four buttons and an IMU |
| Cheaper sibling | [X3](../x3/README.md) — sharper screen, more sensors, no PSRAM |
| Android sibling | [S4](../s4/README.md) — half the price, more consumer features, **no programmability** |
| Accessory line | [Nano / Tong Card](../nano/README.md) |

**The naming is genuinely misleading.** "X4 Pro" implies an enhanced X4. It shares
a screen size and nothing else — and it is **not a superset**: the X4 Pro has **no
IMU**, while both the cheaper X3 and its own board sibling do.

## Its role in the software ecosystem

The X4 Pro is the **design floor** for CrossPlay, whose `LOCAL_SCOPE.md` defines
minimum viable input as *"two side keys plus touch"* — see the
[CrossPlay record](../../../software/applications/crossplay/README.md).

It is also the reason a specific porting hazard exists: CrossPlay had to repoint
`OtaUpdater.cpp` because **upstream's release URL would flash a C3 build onto an
S3**. The X4/X4-Pro naming collision has real consequences in firmware.

## The two design decisions that define its reception

**1. Magnetic pogo charging, no USB-C charge port.** The single most-contested
choice in the family. It generated the largest X4 Pro-specific thread, drove
owners to keep their X4s, and produced two separate mechanical complaints
(*"pogo pin charging loose?"*, *"magsafe alignment"*). The counter-view — *"the
pogo charger is really a non-issue"* — is also firsthand and also common.

**2. A touchscreen on a distraction-free reader.** Contested for a different
reason: *"Additional points of failure… a touch screen adds another layer on top
of the eink display dimming it."* The rebuttal, from an owner: *"I can tell you
it's imperceptible… You can set it so the touchscreen is active in menus, but not
in a book."* Both firsthand.

## What comes next

An **"X4 version 2"** was confirmed by the vendor via Instagram on **2026-08-25**
for September 2026 ([`1vxsr0x`](https://old.reddit.com/r/xteinkereader/comments/1vxsr0x/)).
Nothing about it is established. Comment-level rumour claims leaks show two
devices with pogo pins, one with *"backlight and no touch"* — **hearsay**, and if
true it is not the X4 Classic, whose firmware is unambiguous that it has no
frontlight.
