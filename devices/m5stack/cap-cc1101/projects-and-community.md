# Projects and community — Cap CC1101 & NFC (U219)

**Released 2026-08-28. This snapshot is 2026-09-04.** There are, as of this date, **no
projects** — only anticipation, ordering intent, and a year-long wait. That is itself the
finding, and it is recorded rather than padded.

## 1. The wait — a documented eleven-month slip

| Date | Event | Source |
|---|---|---|
| **2025-09-08** | An owner emails M5Stack about the *"Cardputer ADV Hacker cap (CC1101 SubGHz & ST25R3916 RFID)"* and posts the reply: **"release will be in around 3-4 months, either in December or January"**. Both chips named correctly, a year early | [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1nbe134/), 20 pts |
| 2025-09-08 | In the same thread, u/RJ01988 says he *started making a CC1101 module* for the ADV and is *"waiting to find out the correct pinout required for Bruce"*; u/heytheremonkeyboy points at [`pr3y/Bruce` commit `34aabec`](https://github.com/pr3y/Bruce/commit/34aabecb3e7b1b6ad9a64176e6fa0aa0c9da90ec) for v1.1 pinouts | same |
| 2025-09-08 | The community wish, stated plainly by u/heytheremonkeyboy: *"Will be interesting to see how many modules we can run in one Cap with the extra GPIO pins. Would love to have a CC1101/GPS/NRF24/RFID/LoRa all in one."* | same |
| **2026-01-31** | u/Relevant-Lynx-6688: *"Hi guys, do you have any updates about the release of this cap?"* — **no reply** | same |
| **2026-08-28** | Ships | [r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1w0nwti/) |

## 2. Release-day thread — what was actually established

[r/CardPuter, 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/), 41 upvotes,
16 comments. The most technically substantive post about this board anywhere.

**From M5Stack's community manager (the OP):**

> *"The Cap CC1101 module supports multiple frequency bands: 315 / 433 / 868 / 915 MHz,
> which can be switched via firmware using a combination of **G13 (Cardputer ADV) or G14
> (CardputerZero) as SW0 and GDO2 from the CC1101 as SW1**."*

This is the **only** published statement of the CardputerZero pin difference, and it
independently confirms the architecture read from the schematic. **[COM]**, but corroborated.

> *"M5Stack also expanding the Cardputer lineup with the **Cardputer P4 (Next)**. It is
> still in the development phase … Compared to the Cardputer ADV, it adds Ethernet, HDMI…"*

Followed by an exchange establishing the P4 uses an **ESP32-C5 co-processor** for Wi-Fi/BLE
(u/A31Nesta: *"there are older photos of the board … they mentioned it in a twitter reply"*),
with hopes for the P4X rather than the EOL original P4. **Speculation about an unreleased
product**, recorded as such.

**The recurring question, correctly answered twice:** can the CC1101 do LoRa? No — see
[README §6](README.md).

**What it is for**, per u/No_Confusion7932: *"Copy/read/transmit signals on the specified
frequencies, and jam. The CC1101 also has a longer range."* The "jam" part is illegal
essentially everywhere; recorded because it is what the community says, not as a
recommendation. Same commenter links a YouTube demonstration of CC1101 use under Bruce
firmware on a different device (`youtube.com/watch?v=BUwrWKDqtak`, 7:28–8:51) — **not
watched** by this pass.

**On firmware readiness:** *"The dev will still need to implement band switching, which
shouldn't be too difficult, since M5Stack has already published examples for this on their
website."* So **Bruce does not support this Cap yet** as of 2026-08-28.

## 3. Ordering intent (all the field evidence there is)

u/Zatoichi80: *"I have mine ordered with the Zero, good to see more info on it."*
u/Awkward_Can_1516: *"Ordered!"* — 4 upvotes each. u/zellotron on the P4: *"Very keen …
but it better damn well have PSRAM!"*

**No owner has posted a photograph, a measurement, or a working result.**

## 4. Adjacent projects that will probably adopt it

| Project | Why |
|---|---|
| **Bruce** (`pr3y/Bruce`) | The de-facto sub-GHz/RF firmware for the Cardputer family; already supports CC1101 on other hardware. Needs band-switch support |
| **M5Launcher** (`bmorcelli`) | The launcher most owners use; its author is active in Cardputer threads |
| **M5Stack `M5Unit-NFC`** | **Already supports it** — the only software that does, and it shipped 11 weeks early |

## 5. Evidence discipline

Every item above is announcement, ordering intent, informed interpretation, or a direct
quote of a vendor email. **None of it is measurement, and none of it is a firsthand use
report.** Anyone reading this after ~2026-10 should re-search: this section will be
obsolete, and that is a good thing.
