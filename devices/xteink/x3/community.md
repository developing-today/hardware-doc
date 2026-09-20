# Xteink X3 — community reception

From **2,136** deduplicated Reddit posts, **2026-09-04**. Types: **O** firsthand
ownership · **M** firsthand measurement · **P** demonstrable project ·
**I** informed interpretation · **Op** opinion · **H** hearsay.

## The X3's distinctive contribution: it is the only Xteink anyone opened

Two independent teardowns exist, both of this device, and **both were motivated by
curiosity rather than repair**. See [`media.md`](media.md). Nothing comparable
exists for the X4, X4 Pro or X4 Classic.

## The comparison thread that defines it

[r/xteinkereader `1syav96`](https://old.reddit.com/r/xteinkereader/comments/1syav96/),
2026-04-28, **412 points** — "X3 vs X4 - actual experience comparison" · **O**

> "…the buttons on the X4 are **clickier and louder**. The X3's buttons are
> somewhat **mushy and quieter**. … Overall If I have to choose 1, I'd go with the
> X4. However, I probably will abandon both once the S4 is released."

A firsthand comparative ownership report, and the source of the only tactile
assessment in this tree. Note the conclusion favours the X4 — on feel, not specs.

The counterweight, from an owner of all three models
([r/XTEINK `1vw6haq`](https://old.reddit.com/r/XTEINK/comments/1vw6haq/), 2026-08-23):

> "The regular X4 definitely feels obsolete (and also literally discontinued).
> **The x3 is still a better form factor for carrying on the back of the phone**
> (+ comes in the white/grey color)." · **O**

And from a buyer choosing it deliberately:

> "someone I met had one and they let me see it and **the crispness of the screen
> was actually what really sold me on it**." · **O + Op**

That crispness is real and arithmetic: ~257 PPI against the 4.26″ models' ~219.

## Owners can see the panel-controller change

This is the most technically valuable community observation about the X3. A user
bought **two X3s from different channels** and compared them side by side, both on
CrossInk 1.5.0, both with the supplied screen protector
([r/XTEINK `1vkuhbi`](https://old.reddit.com/r/XTEINK/comments/1vkuhbi/), 2026-08-10,
41 pts, **36 comments**) · **M**:

> "**The Official Site one on the LEFT** has slightly whiter background and clearer
> text. It came with a 32gb XTEINK SD card. **Page turns and menus seem slower**,
> with all settings being equal.
> **The Amazon.ca one on the RIGHT** has slightly darker background and not as
> clear text. It came with a 16gb XTEINK SD card. **Page turns and menus seem
> faster**, with all settings being equal."

**A visible, reproducible, side-by-side difference in contrast and refresh speed
between two X3 units.** The obvious hypothesis is the
[UC8253 → UC8279d](features/display.md) transition — but **which unit carries
which controller was never determined**, and the thread never resolved it. See
[`gaps-and-conflicts.md`](gaps-and-conflicts.md).

The same thread reveals **at least four distinct back-casing variants**:

| Variant | Reported by |
|---|---|
| Black logo + **sticker label** at the bottom | official site |
| Grey logo + **engraved text** | Amazon.ca, higher serial |
| **Completely clean back**, no markings | direct, early pre-order |
| Faint labelling | direct |

> "They'll outsource to a bunch of manufacturers who can meet the specs." · **Op**

And crucially · **O**:

> "X3 from **Amazon**, light grey text, **unlocked** / X3 from their **official
> website**, light grey text but **locked** for some reason / X4 from
> **Aliexpress**, dark text, **locked**"

**USB-lock state does not correlate with channel in any predictable way.** You
cannot know before purchase.

## NFC — the community solved it, not the vendor

The X3's NFC tag went unexplained for months. The resolution came from a firmware
maintainer and three owners. See [`features/nfc.md`](features/nfc.md) for the full
evidence. Demonstrated uses:

| Use | Type |
|---|---|
| *"I **wrote my contact infos**, in case it get lost"* — via an Android NFC writer app | **O, demonstrated** |
| *"when I tap my phone to it it **automatically joins the X3 WiFi and opens the crosspoint manager** in the browser! I use it every time when I want to load up a new book."* | **P** |
| iOS Shortcuts automation opening `http://crosspoint.local/` on tag detection, with screenshot | **P** |
| *"I knew it could **clone NFC cards**"* | **H — unverified and implausible for a passive tag** |

Key facts, both firsthand: *"**By default there is no data in the nfc tag**"* and
iOS can **detect but not read/write** it while Android can do both.

## Reliability

| Report | Date | Type |
|---|---|---|
| *"My **glass cracked** a bit on the rear side. So it might not have happened if I had black x3."* — asks which models have **metal backing**; **received no authoritative answer** | 2026-09-02 | **O** |
| *"Do not step full body weight on your new XTEINK"* — r/ereader, 144 pts | 2026-05-02 | **O** |

The teardown independently confirms the back is **glass**, removable with a heat
gun and suction cup. **No replacement-part source is known.**

## Price and channel anecdotes

> "**Got an X3 for dirt cheap ($16).** Here are my thoughts after a few days of
> use. … I still flashed **CrossMux** onto it (a Chinese fork of CrossPoint that
> adds support for online sources like WeChat Read), and the experience has been
> fantastic. I can manage my library directly through Calibre, exactly like I do
> with my Kindle. **I'd honestly say 60 % of my positive** [experience]…"
> — [r/XTEINK `1vrnxnq`](https://old.reddit.com/r/XTEINK/comments/1vrnxnq/), 2026-08-18 · **O**

The same post is the sharpest published criticism of the vendor:

> "…the **double standard for different distribution channels** and the official
> team's **negative attitude toward the community** makes me seriously doubt
> whether I'll buy the next S4." · **Op**

**A single $16 anecdote with an unstated channel is not a used-market price** and
is not treated as one here.

## Reach beyond the dedicated subreddits

r/eink (*"My Xteink X3 Review (vs X4). The Antidote to Smartphones."*, 34 pts;
*"Crosspoint on X3 - preview with **smooth antialiasing waveforms**"*, 55 pts ·
**P**), r/ereader, r/kindle (*"Xteink X3 vs Kindle PPW 12th Gen Size
Comparison"*), r/koreader (multiple sync threads), r/EDC, r/microreaders.

## Weighting caveat

One of the three dedicated subreddits is **vendor-operated** —
*"r/xteinkreader is the main sub and **it's run by the company**"*
([r/xteinkHax `1sbjsr3`](https://old.reddit.com/r/xteinkHax/comments/1sbjsr3/) · **I**),
and r/xteinkHax exists partly because a post was **removed from it**. Positive
sentiment sampled from that subreddit alone should not be treated as independent.
