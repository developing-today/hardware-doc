# X3 — NFC

> **An ISO/IEC 14443A tag is on the board. Nobody has explained what it does.**
> This is the largest unexplained hardware feature in the entire Xteink family.
> 2026-09-04.

## What is established

| Fact | Source |
|---|---|
| An **ISO/IEC 14443A NFC Tag** is fitted | **[CN]** [`sunwoods/Xteink-X3`](https://github.com/sunwoods/Xteink-X3) BOM — listed as `***ISO/IEC 14443a NFC Tag`, asterisked by the author as notable |
| **"NFC support"** is an advertised X3 feature | **[VENDOR]** launch announcement, [r/xteinkereader `1pi6ezd`](https://old.reddit.com/r/xteinkereader/comments/1pi6ezd/) and [`1pjw3ay`](https://old.reddit.com/r/xteinkereader/comments/1pjw3ay/), 2025-12-09/11 |

Component record:
[`unidentified/xteink-x3-x4/nfc-tag-iso14443a`](../../../../components/unidentified/xteink-x3-x4/nfc-tag-iso14443a/README.md)

## What is not established — which is almost everything

- **The part number.** Unknown.
- **Whether it is a passive tag or a reader/writer.** The Chinese BOM says *"Tag"*,
  which implies **passive** — an NFC tag the *phone* reads, not a reader the device
  uses.
- **What it is connected to.** It appears in **no** board profile, **no** firmware
  string, **no** driver, and on **no** host bus in the FreeInk SDK. If it is a
  passive tag with no I²C interface, that is expected — but it also means firmware
  cannot use it.
- **What it is for.** Entirely unknown.

## Candidate explanations — all speculation, none supported

| Hypothesis | Argument for | Argument against |
|---|---|---|
| **Phone hand-off** — tap the reader to open the web file manager | The stock firmware serves `http://bofi.xteink.cn/index.html?ip=` — an NFC tag encoding that URL would be a neat pairing gesture | No evidence anyone has observed this |
| **Case / accessory identification** | The X3 has a strong magnetic-accessory ecosystem | A passive tag on the *device* cannot identify an accessory |
| **Authenticity / anti-counterfeit** | Common in Shenzhen consumer hardware | No vendor statement |
| **Manufacturing / QC marker** | Plausible for line tracking | Would not be advertised as a user feature — and it **was** advertised |

The vendor advertising it as a user-facing feature argues against the purely
internal explanations, and for something a phone interacts with.

## Why no one has investigated

Every community firmware replaces the stock application entirely, and the tag is
invisible to firmware. The people who could answer this — stock-firmware users
with an NFC-capable phone — are the least likely to be writing hardware notes.

## How to resolve it, cheaply

**Tap an NFC-capable phone against an X3 and read the tag.** Any NFC-reader app
will dump the NDEF payload. This is a five-minute experiment that nobody appears
to have performed, and it would resolve the question completely.

Secondarily: examine the archived teardown photographs
([`../media.md`](../media.md)) for an antenna coil trace, which would confirm the
tag is passive and show where it sits.

## Cross-device

Neither the X4, the X4 Pro nor the X4 Classic has NFC. **The X3 is the only
Xteink device with it.**

## Status

**`unknown`.** Presence: two independent sources. Function: no evidence at all.
