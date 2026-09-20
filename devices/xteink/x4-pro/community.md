# Xteink X4 Pro — community reception

> From 1,798 deduplicated Reddit posts retrieved **2026-09-04**. Evidence types:
> **O** firsthand ownership · **M** firsthand measurement · **P** demonstrable
> project · **I** informed interpretation · **Op** opinion · **H** hearsay.

## Where the community is

**Three** subreddits with confusingly similar names, plus one project sub:

| Subreddit | Posts in corpus | Character |
|---|---|---|
| **r/XTEINK** | 416 | General; heaviest firmware-release traffic |
| **r/xteinkereader** | 406 | General; heaviest owner-experience traffic |
| **r/xteinkHax** | 180 | Hacking / firmware development |
| r/CrossPointReader | 6 | Project-specific |

Spillover into r/ereader (79), r/eink (17), r/EDC (18), r/writerDeck, r/dumbphones,
r/PaperRepublic, r/Ultralight.

**Searching one subreddit finds roughly a quarter of the material.** This is the
most practically useful community finding.

## The pogo-pin controversy — the defining X4 Pro thread

[r/xteinkereader `1v2txxe`](https://old.reddit.com/r/xteinkereader/comments/1v2txxe/)
and its r/XTEINK mirror, both 2026-07-21, **71 and 46 comments**:

> "X4 Pro doesn't use USB-C for charging—it uses the magnetic pogo adapter. …
> It's enough that I'll happily keep using my original X4 instead of upgrading.
> … I'm hoping that whatever comes after the X4 Pro—maybe the S4 or another
> future model—returns to USB-C."
> — **O + Op**

The poster pre-empts the counter-argument (*"Please don't try to convince me that
the dongle is 'no big deal'"*), which tells you the argument was expected. This is
a **firsthand ownership report of a design fact**, and the fact is confirmed
independently by the vendor selling the adapter and cable as separate SKUs.

**Prevalence not established.** One thread with 71 comments shows the topic is
contested; it does not show what fraction of owners mind.

## The X4 Classic was found by the community before it was announced

[r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/),
2026-06-22, **300 points**, 53 comments:

> "Did we just spot a new X4 model? Physical buttons + frontlight but no
> touchscreen in the latest video? … Could there actually be three devices shown
> in the video? First the S4, then the X4 Pro and finally 2 devices placed in the
> dock at the end. … The front buttons look identical to the X4, but I keep
> noticing what looks like a button on the left side."
> — **I** (informed interpretation of a vendor video)

This predates the X4 Pro's 2026-07-21 listing and correctly identified a
buttons-only S3 variant. The **frontlight** detail turned out to be wrong — the
X4 Classic has none. A good illustration of community video-forensics being
directionally right and specifically wrong.

## Firmware ecosystem sentiment

| Thread | Date | Signal |
|---|---|---|
| ["CrossPoint 1.5 has officially been released!"](https://old.reddit.com/r/xteinkereader/comments/1vhvtdd/) | 2026-08-07 | **763 pts, 305 comments.** The largest thread in the corpus. Includes the soft-brick warning for stale forks — **P + I** |
| ["Tips after 1 Week and 2 Books"](https://old.reddit.com/r/XTEINK/comments/1uz8yiz/) | 2026-07-17 | **723 pts.** The de-facto onboarding post; names the three service sites — **O** |
| ["To everyone who has donated to CrossPoint"](https://old.reddit.com/r/xteinkereader/comments/1tl3gnn/) | 2026-05-23 | 346 pts. OTA unlock for USB-locked devices — **P** |
| ["If you're looking to get an X3/X4… support CrossPoint by buying from our site"](https://old.reddit.com/r/xteinkereader/comments/1uan67g/) | 2026-06-20 | 338 pts. **The vendor and the third-party firmware project have a commercial affiliate relationship**, and the vendor sells a "developer unlocked version" — a notably unusual posture for a Chinese consumer-hardware maker |
| ["Microreader 2.0 (for Xteink X4)"](https://old.reddit.com/r/XTEINK/comments/1tqbcgu/) | 2026-05-28 | 514 pts. Note the emphasis: *"If you have an unlocked X4 (!!!UNLOCKED!!!)"* — **P** |

## Vendor relationship — mixed

The founder **"Crusoe"** introduced the company on r/ereader on 2025-10-09
([`1o2203h`](https://old.reddit.com/r/ereader/comments/1o2203h/), **1,477 points**):
*"I'm Crusoe, founder of Xteink, a small team based in Shenzhen."* — **O**

But not all of it is warm. [r/XTEINK `1vrnxnq`](https://old.reddit.com/r/XTEINK/comments/1vrnxnq/)
(2026-08-18, 24 pts), from a user who bought an X3 for **$16**:

> "the double standard for different distribution channels and the official team's
> negative attitude toward the community makes me seriously doubt whether I'll buy
> the next S4."
> — **O + Op**

Same post, on firmware: *"I still flashed CrossMux onto it (a Chinese fork of
CrossPoint that adds support for online sources like WeChat Read) … I'd honestly
say 60% of my positive [experience]…"* — **the stock firmware is not what people
value.**

## Reliability

[r/XTEINK `1utbw3v`](https://old.reddit.com/r/XTEINK/comments/1utbw3v/),
2026-07-11, 81 pts, 50 comments: *"After less than 3 months, the device decided to
self-destruct"* — a careful owner, never dropped, always cased. — **O**

A second thread reports **cracked rear glass** on an X3
([`1w56phf`](https://old.reddit.com/r/xteinkereader/comments/1w56phf/), 2026-09-02)
and asks which models have metal backing rather than glass. **Unanswered.**

**Two failure anecdotes across 1,798 posts establishes that failures occur.**
It does not establish a failure rate, and should not be reported as one.

## What the community does **not** have

- **No X4 Pro teardown.** Repeatedly implied to exist (*"Fiche specs, teardowns,
  and firmware guides are awesome"*) but no X4 Pro teardown was ever posted.
- **No power measurements.** The one person who set out to make them
  ([X3 teardown](../x3/media.md), Nordic PPK II) never posted results.
- **No independent hardware documentation.** Everything traces to the FreeInk SDK.
