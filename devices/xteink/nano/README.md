# Xteink Nano — "Tong Card" (瞳卡)

> A **battery-less, NFC-powered four-colour e-paper display card** that snaps
> magnetically to the back of a phone. **Not a reader, not an ESP32 device, and
> not part of the CrossPoint / FreeInk firmware ecosystem.**
> Research retrieval date **2026-09-04**. **Depth: sourced stub.**

## Why this record exists

The Nano was **missed by the first pass of this research** and surfaced only on a
second, wider community sweep. It is a genuine fifth Xteink product line, it is
sold internationally on AliExpress, and it is **the thing people confuse with the
[X3's embedded NFC tag](../../../components/unidentified/xteink-x3-x4/nfc-tag-iso14443a/README.md)**.
Recording it prevents that conflation and stops a future pass rediscovering it.

## Identity

| Field | Value | Evidence |
|---|---|---|
| Chinese name | **瞳卡** (*tóng kǎ*, "pupil card") | **[COMM]** [r/XTEINK `1smdpjq`](https://old.reddit.com/r/XTEINK/comments/1smdpjq/) |
| English names in use | **"Tong Card"** (community/AliExpress) · **"Nano"** (Xteink's own app) | **[COMM]** same |
| Class | Passive **NFC-powered e-paper display card** | **[COMM]** firsthand owner |
| Display | **Four-colour e-ink** | **[COMM]** firsthand owner |
| Power | **None — no battery.** Harvested from the phone's NFC field | **[COMM]** |
| Attachment | Magnetic, phone-back | **[COMM]** |
| Market | **China-first.** Not listed on `xteink.com` | **[VENDOR]** absence + **[COMM]** |
| Sales channel observed | **AliExpress** | **[COMM]** |

**The name mapping is established by a single, decisive observation.** A user
found the string `我的瞳卡` ("My Tong Card") in the *international* build of the
official Xteink Android app, untranslated, and identified 瞳卡 as *"the chinese
name of the Nano"* ([r/XTEINK `1smdpjq`](https://old.reddit.com/r/XTEINK/comments/1smdpjq/),
2026-04-15). That ties the community's "Tong Card" to Xteink's own "Nano".

## What is established, and how

### It works, but not with the international app

> "Basically it is a **four-colour eink display with NFC capability** that allows
> you to load an image onto it and then snap it onto the back of your phone or
> other magnetic surface. When I saw one on AE I took a chance and bought one…
> **So far I haven't been able to** [load an image] **no matter what I have
> tried.** … unless you have a way of doing this through the official channels I'd
> hold off getting one at the moment."
> — [r/xteinkHax `1sbjsr3`](https://old.reddit.com/r/xteinkHax/comments/1sbjsr3/), 2026-04-03, **110 points** · **firsthand ownership**

The blocker is that image upload requires the **China-mainland Xteink app**. A
second owner reported the same: *"I'm stuck too, got mine and haven't been able to
find a work around to get onto the China mainland app."* — **firsthand ownership**

### A third-party app works

The same thread resolves it. The original poster confirms:

> "I have an app, **NFC Eink**, that works so I'm good thanks."
> — **firsthand, demonstrated**

and a third user points to a written procedure:
`https://www.spokenlikeageek.com/2026/04/09/xteink-tong-card-in-use/`
(the OP is also its author). **Not retrieved this session** — recorded as an open
acquisition.

### It is probably a re-badged Waveshare module

> "Try this app, there is a QR code towards the bottom. **I bet it's a waveshare
> display.** I got one for my wife for Christmas and it's awesome but kind of a
> pain to get working. `https://www.waveshare.com/wiki/1.54inch_NFC-Powered_e-Paper_(G)`"
> — [r/xteinkHax `1sbjsr3`](https://old.reddit.com/r/xteinkHax/comments/1sbjsr3/) · **informed interpretation, not verified**

**This is a hypothesis, not a finding**, and it is flagged as such. But it is a
well-motivated one: Waveshare's "NFC-Powered e-Paper" line is exactly this product
category — battery-less, NFC-written, multi-colour — and the fact that a
*third-party* app written for Waveshare-class NFC e-paper successfully drives the
Tong Card is meaningful circumstantial support.

A competing product the same thread raises, the Vidabay Snap
(`theverge.com/tech/917067/...`), was tried by the OP and **does not work** —
*"Thanks for the tip but it doesn't. NFC Eink works but isn't great."* A useful
negative result: whatever protocol the Tong Card uses, it is not universal across
NFC e-paper cards.

### Xteink's own app support is partial and wobbly

- The international Android app briefly exposed the Nano wallpaper section
  **untranslated**, then *"They seem to have removed it with a new update."*
- On iOS: *"Nano is wallpapers show in the international iOS app, but no upload
  yet."* — **firsthand ownership**

So as of the snapshot the official international path is **incomplete**.

## What is completely unknown

**Everything at the hardware level.** No teardown, no photograph of the internals,
no part identification of any kind:

| Unknown | Note |
|---|---|
| **NFC front-end / e-paper driver IC** | Not identified |
| **Display size and resolution** | *"four-colour"* is the only display fact; the suspected Waveshare sibling is 1.54″, **not confirmed for this product** |
| **Tag type / protocol** | Unknown. Only that "NFC Eink" drives it and the Vidabay app does not |
| **Price** | Never captured |
| **Whether Xteink designed it or re-badged it** | Open |
| **Relationship to the X3's embedded tag** | **None established.** Different products; see below |

## Do not confuse it with the X3's NFC tag

| | **Nano / Tong Card** | **[X3's embedded NFC tag](../../../components/unidentified/xteink-x3-x4/nfc-tag-iso14443a/README.md)** |
|---|---|---|
| What | A **separate product** you buy | A **passive tag inside the X3** |
| Display | Yes — four-colour e-paper | No |
| Power | Harvested from the phone's NFC field | None needed; it stores bytes |
| Purpose | Show an image on your phone's back | Trigger a phone automation / store contact info |
| Written with | The Xteink China app, or "NFC Eink" | Any Android NFC writer app |

The confusion is real and documented: the user who found the Nano section in the
official app initially *"thought it was for the X3's NFC functionality"*.

## Community and channel notes

Two facts from this thread are worth carrying into the family record:

1. **The post was removed from the official subreddit.** *"(This post was removed
   by the mods on the official subreddit)"* — and r/xteinkHax exists partly
   because of that.
2. **The subreddit split is now explained.** *"r/xteinkreader is the main sub and
   **it's run by the company**; there's another one r/XTEINK which is opened by
   supporters"* — **informed community statement**. That is directly relevant to
   how the community evidence in this tree should be weighted: one of the three
   subreddits is vendor-operated.

## Sources

| ID | What | URL | Retrieved | Type | Establishes |
|---|---|---|---|---|---|
| N01 | "I bought an Xteink Tong Card so you don't have to!" | <https://old.reddit.com/r/xteinkHax/comments/1sbjsr3/> | 2026-09-04 | community, **firsthand ownership** | Product exists; four-colour NFC e-paper; China-app lock-in; NFC Eink works; Vidabay app does not; Waveshare hypothesis; **the official sub removed the post** |
| N02 | "Xteink Nano option in the official app" | <https://old.reddit.com/r/XTEINK/comments/1smdpjq/> | 2026-09-04 | community, **firsthand** | **瞳卡 = Nano**; the international app briefly exposed it, then removed it; iOS shows wallpapers but cannot upload |
| N03 | Waveshare 1.54″ NFC-Powered e-Paper (G) wiki | <https://www.waveshare.com/wiki/1.54inch_NFC-Powered_e-Paper_(G)> | **not retrieved** | vendor | The suspected sibling product line — **hypothesis only** |
| N04 | "Xteink Tong Card in use" | <https://www.spokenlikeageek.com/2026/04/09/xteink-tong-card-in-use/> | **not retrieved** | community blog | A written working procedure, by the N01 poster |

## What would turn this into a real record

In rough order of value:

1. **Retrieve N04 and N03** — cheap, and N04 is a firsthand working procedure.
2. **A teardown**, or even a photograph of the card's back with markings.
3. **An Android NFC tag-info dump** (technology list, UID prefix) — 30 seconds for
   any owner, and it would likely identify the driver IC family outright.
4. An AliExpress listing capture for price, dimensions and resolution.

## See also

[Family index](../README.md) ·
[X3 NFC feature guide](../x3/features/nfc.md) — the thing this is *not*
