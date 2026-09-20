# ISO/IEC 14443A NFC tag — Xteink X3 (part unresolved, **purpose established**)

- **Category:** passive NFC tag, **not connected to the host processor**.
- **Manufacturer / part:** **unknown.**
- **Research status:** ⚠ Part unidentified — but **what it is and what it does is
  now established** from an authoritative maintainer statement plus multiple
  firsthand owner reports.
- **Retrieved:** 2026-09-04

## What it is — resolved

**A blank, user-writable passive NFC tag embedded in the device.** It is
*not* an NFC reader, and it is **electrically independent of the ESP32-C3**.

The decisive statement is from **uxjulia**, maintainer of the CrossInk firmware,
on the CrossPoint Reader discussion board:

> "The NFC chip on the device is **independent of the firmware**. The iPhone can't
> read/write from it because of the type of NFC chip that's being used, but you
> can use Apple's Shortcuts app to **detect** the NFC tag and run an automation.
> **Android phones seem to have no problem reading/writing to it** though."
> — [`crosspoint-reader/crosspoint-reader` discussion #2259](https://github.com/crosspoint-reader/crosspoint-reader/discussions/2259), 2026-06-03 · *informed maintainer statement*

Corroborating firsthand owner reports, all from
[r/xteinkereader `1vit43t`](https://old.reddit.com/r/xteinkereader/comments/1vit43t/) (2026-08-08):

| Report | Type |
|---|---|
| *"It's not an NFC reader afaik. Just a **writeable nfc tag, like an embedded NFC sticker**"* | informed interpretation |
| *"**By default there is no data in the nfc tag** of the xteink3"* | **firsthand ownership** |
| *"In my case, I **wrote my contact infos**, in case it get lost… Used an NFC writer app on my Android phone, created a contact card format and used it as payload"* | **firsthand ownership, demonstrated** |
| *"I made a post how I use NFC so when I **tap my phone to it it automatically joins the X3 WiFi and opens the crosspoint manager** in the browser! I use it every time when I want to load up a new book."* | **firsthand, demonstrable project** |
| *"I knew it could **clone NFC cards**, not encrypted of course"* | hearsay — **unverified**, and implausible for a passive tag |

A second demonstrated use, from the same GitHub discussion: a user built an iOS
Shortcuts automation to **open `http://crosspoint.local/` when the tag is
detected**, with a screenshot.

**This resolves the open question recorded earlier in this repository.** The tag
is a convenience feature for phone hand-off, shipped **blank**, and it is up to
the owner to write something to it.

## What is still unknown

| Unknown | Note |
|---|---|
| **Part number** | Never read from any photograph |
| **Tag type** | Some type that **iOS can detect but not read or write**, while Android can do both. That asymmetry is a strong clue — it suggests a tag outside iOS's supported NDEF-formatted set, or an unformatted tag — but no source names the type |
| **Capacity** | Unknown |
| **Antenna location** | Not identified in either teardown |
| **Whether the X3 is the only model with it** | No X4/X4 Pro/X4C owner report of NFC was found, and no board profile mentions it |

## Why firmware cannot help

Because the tag is **not on any host bus**, no amount of firmware work exposes it.
This is worth stating plainly because a user spent effort trying:

> "I did try with claude code to figure out if i can add the functionality to the
> crosspoint-reader code but no luck, **it could not find the driver for the nfc
> chip and also scanning the original firmware bin file for the driver didn't
> work.**"
> — discussion #2259, 2026-06-03

The search failed because there is nothing to find. That negative result is
recorded here so nobody repeats it.

## What would resolve the part identity

An Android NFC app that reports tag technology (`NfcA`, `MifareUltralight`,
`Ndef`) and the tag's UID prefix — a 30-second operation for any owner. Failing
that, an antenna-coil trace visible in a teardown photograph.

## Do not confuse this with the "Tong Card" / "Nano"

Xteink also sells a **separate product**, the **Tong Card (瞳卡)**, marketed
internationally as the **Nano**: a battery-less four-colour e-paper display that
is **powered and written over NFC** and snaps magnetically to a phone. That is a
distinct device with an NFC-powered display, not this embedded tag. See
[`devices/xteink/nano/README.md`](../../../../devices/xteink/nano/README.md).

---

## Used By

### [Xteink X3](../../../../devices/xteink/x3/README.md)

Fitted; **not on any bus**; blank from the factory. Advertised by the vendor at
launch as *"NFC support"*
([r/xteinkereader `1pi6ezd`](https://old.reddit.com/r/xteinkereader/comments/1pi6ezd/), 2025-12-09)
and listed in the Chinese teardown BOM as `***ISO/IEC 14443a NFC Tag`, asterisked
by that author as notable.

**The X3 is the only Xteink device evidenced to carry one.**

→ [`devices/xteink/x3/features/nfc.md`](../../../../devices/xteink/x3/features/nfc.md)
