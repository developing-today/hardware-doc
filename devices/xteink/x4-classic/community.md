# Community and owner reports — Xteink X4 Classic

Snapshot **2026-09-11**. Source: `old.reddit.com` JSON with UA
`WhatsApp/2.23.20.0`, 11/11 requests HTTP 200. **94 unique posts** naming the X4
Classic / X4 V2 / X4C were catalogued across six subreddits over a one-year
window, plus **12 full comment trees**.

**Every claim below is a community report and is labelled by evidence type.**
Nothing here was measured by this repository. The device is **five days old**
internationally at the snapshot date, so all owner reports come from either
pre-release review units or the very first retail batch.

## The sampling caveat that matters most

Three of the six subreddits searched are Xteink-specific, **one of them is
vendor-operated**, and the vendor runs a pre-release "Experts Program" that
seeds review units. Two of the three most detailed reviews below say so in
their own text. Treat the balance of sentiment in those subreddits as
**unrepresentative**; the negative reactions are, if anything, more notable for
appearing there at all.

For contrast: `r/eink` returned **0** posts and `r/ereader` returned **1** for
the same query over a year. This launch is almost invisible outside the
vendor-adjacent communities.

## Launch-week volume

| Date | Posts naming X4C/X4 V2 in the catalogued set |
|---|---:|
| 2026-04-23 → 2026-08-29 | 28 (speculation era) |
| 2026-09-03 | 2 — **the announcement** |
| 2026-09-04 | 5 |
| 2026-09-05 | 13 — **peak**, the review embargo lifting |
| 2026-09-06 → 09-08 | 16 |
| 2026-09-09 → 09-11 | 30 |

## The announcement — vendor, firsthand, primary

| Field | Value |
|---|---|
| Author | **u/xteink** — the vendor's own account |
| Post | [r/xteinkereader `1w63yyl`](https://old.reddit.com/r/xteinkereader/comments/1w63yyl/), 2026-09-03, **806 points, 300 comments** |
| Title | *"We're turning a new page on the X4."* |
| Body, verbatim and complete | *"A familiar idea, refined for everyday reading. **X4 Classic (X4 V2) is coming soon.** We'll share more details shortly."* |

**This is the vendor stating the two names as one product, three days before
listing it.** It is the strongest non-API evidence for the naming question and
it predates the store listing.

The top comments are, almost uniformly, a request for a *different* device:

| Score | Author | Comment |
|---:|---|---|
| 210 | u/xtremis | *"Damn, you were swallowed by the Anbernic syndrome! I'm waiting for my X3 DS Pro Plus with integrated stylus 🫠"* |
| 166 | u/Kiras_ | *"I would be fine with just a better screen contrast and pixel density"* |
| 92 | u/ashraf_bashir | *"X3 with light, that's it!"* |
| 77 | u/iclazz169 | *"Need and x3 with light"* |
| 65 | u/seijurogouu | *"i'd be interested in an X3 Pro. x3 size but with touch and light"* |

**Four of the five highest-scoring replies to the vendor's own launch teaser ask
for a frontlight.** This is the context for the [X4 Light](../x4-light/README.md)
filing, which was already at the FCC when this was posted.

## Firsthand owner reviews

### R1 — pre-release unit, positive

[r/XTEINK `1w7wjw2`](https://old.reddit.com/r/XTEINK/comments/1w7wjw2/), u/Which_Heart_983,
2026-09-05, **279 pts / 120 comments**. Self-identified: *"I was lucky to receive
this sneak peek version."* **Firsthand use of a vendor-supplied unit.**

Claims, each a subjective firsthand impression unless noted:

- *"surprised me with how light and slim it is… they have managed to make it
  **slimmer than an X3**"* — consistent with the vendor's 4.9 mm against the
  X3's published thickness, but **not measured here**.
- *"In the second picture you can see how much darker the letters are"* —
  **contrast**, not resolution. The same reviewer confirms, in reply to a direct
  question about pixel density: **u/scamper_ *"It does not, it's still 219"***.
  So: same panel density, claimed better contrast. Unresolved whether this is a
  panel change, a waveform change, or observer bias.
- *"**button placement is identical to the X4 Pro**"* — two side keys. Agrees
  with the FreeInk profile's `GPIO0` / `GPIO7` side pair.
- *"Has a clock"* → the BM8563 RTC. *"**Shake to turn page**"* → the QMI8658 IMU.
  Both are **owner-observed corroboration of firmware-only claims**.
- *"Items in the box are identical to the X4 Pro."*
- Con: *"Pogo pin… the in box connectors are bad. I use the X3 cable."*

### R2 — pre-release unit, mixed

[r/XTEINK `1w8bfew`](https://old.reddit.com/r/XTEINK/comments/1w8bfew/), u/Comprehensive_Oil426,
2026-09-05, 98 pts. *"I had the privilege of receiving an X4C to review."*

- *"This device is thin! … I thought I might break it if I squeezed too hard"*
- *"much more faster and intuitive than the X3"* — **stock firmware**, no
  reflash, no timings given.
- *"I also feel a slight improvement in the screen resolution"* — **this is the
  contrast claim restated as a resolution claim, and it is wrong**: the density
  is unchanged at 219 PPI. A good example of why *"better screen"* reports in
  this family must be read carefully.
- Refuses to publish cons yet: *"it would be unfair if it turned out to be a
  skill issue."*

### R3 — "Experts Program" unit, comparative, the most useful

[r/xteinkereader `1wbxvvg`](https://old.reddit.com/r/xteinkereader/comments/1wbxvvg/),
u/ajcabrera, 2026-09-09, **201 pts / 39 comments**. Owns X4C **and** X4 **and**
X4 Pro. **TL;DR in the author's own words: *"It's nice and light, but if you
already have an X4 or X3, save your coins."***

| Claim | Evidence type |
|---|---|
| *"substantially lighter than the X4… reduction in width"* | firsthand comparison, no scale used |
| *"side buttons on the left and right sides like the X4 Pro makes page scrolling a lot easier"* | firsthand |
| *"**Both use the same 219 PPI screen** I believe… only noticeable when directly comparing text side-by-side"* | firsthand, **explicitly hedged** |
| *"**Battery Capacity** — a few extra days from 100 % to 0 % when comparing both devices"* | firsthand, uncontrolled. Consistent with 920 mAh vs the X4's unpublished capacity, but **not a measurement** |
| *"Stock firmware feels very snappy… prefer the reading speed on stock vs Crosspoint"* | firsthand, subjective |

### R4 — X4 vs X4 Classic side by side

[r/XTEINK `1wdo4sa`](https://old.reddit.com/r/XTEINK/comments/1wdo4sa/), 2026-09-11,
u/Every_Purpose_1152 owns *"each iteration of the XTEINK devices"*. Cross-posted
to r/xteinkereader as [`1wdo7xw`](https://old.reddit.com/r/xteinkereader/comments/1wdo7xw/).

### R5 — retail-store review, verbatim from the vendor's own page

Judge.me review on `xteink.com`, reviewer **"anne vla"**, 5 stars, captured
2026-09-11. **A vendor-hosted review — curation cannot be excluded.** Quoted
because it is the only side-by-side X4-vs-X4C account outside Reddit:

> *"I already have the original XTEINK X4, in black and decided to go for the
> Classic in grey. Other than the pogo adapter I didn't expect a big difference
> but I think there is… The biggest improvement for me is definitely the buttons.
> The placement of them is different from the V1 and so much better… The only
> thing I'm not crazy about is the pogo charger. I would still prefer USB-C."*

Note the reviewer's own shorthand: **"the V1"** for the original X4. That usage
is independent support for the reading of `ESP32S3_X4R2_CLA` given in
[`README.md`](README.md) §`R2`.

## The two controversies

### 1. Price — the loudest thread is not a review

[r/XTEINK `1w9jzpn`](https://old.reddit.com/r/XTEINK/comments/1w9jzpn/) "X4 Classic price",
2026-09-07, 60 pts / 49 comments. Dated, region-specific figures from owners:

| Observation | Region | Date | Source |
|---|---|---|---|
| X4 Classic **€89**, X4 Pro **€110** | EU | 2026-09-07 | u/macien12, post body |
| *"earlier batches were widely available closer to €40"* | EU | pre-2026-09 | same, hearsay |
| X4 bought at **£47.70 ≈ €58** | UK | *"last minute"*, pre-launch | u/wowsomuchempty, firsthand purchase |
| *"the original X4 at around €60 was unbeatable"* | EU | pre-2026-09 | u/ShrubbyFire1729 |
| *"the X4C costs about 30 % more than original X4"* | — | 2026-09-10 | u/chicco1973, 40 pts |

**The €89 EU price against the US$79 store price is a tax/region difference, not
a contradiction** — but neither was normalised by this research, and the €40
figure is hearsay. See [`market-and-pricing.md`](market-and-pricing.md).

### 2. Pogo pin instead of USB-C

The dominant complaint, and it has a regulatory edge. Two threads:

- [r/xteinkereader `1w9r7rf`](https://old.reddit.com/r/xteinkereader/comments/1w9r7rf/),
  2026-09-07, **199 pts / 286 comments**: *"the lack of USB-C makes the X3, X4
  Pro, and X4 Classic illegal to sell in the EU"*. **Contested in its own
  thread**: u/ShrubbyFire1729 — *"Including the POGO to USB adaptor is enough to
  satisfy the EU requirement."* **This repository takes no position**; it is a
  legal question, the arguments are hearsay on both sides, and no directive
  citation was produced by either side.
- [r/xteinkereader `1wagbmu`](https://old.reddit.com/r/xteinkereader/comments/1wagbmu/),
  2026-09-08, **616 pts / 730 comments** — *"A Letter from Crusoe, Founder of
  XTEINK: Pogo, USB-C, and Where We're Going"*. **The largest thread in the
  history of this family.** A founder statement; primary, but vendor-sourced.

## Firmware community

| Thread | Date | Content |
|---|---|---|
| [r/CrossPointReader `1wbmagp`](https://old.reddit.com/r/CrossPointReader/comments/1wbmagp/) | 2026-09-09 | "Xteink X4 Classic support" |
| [r/XTEINK `1wctkd6`](https://old.reddit.com/r/XTEINK/comments/1wctkd6/) | 2026-09-10 | "Crosspoint or Crossink? Differences on x4 classic" |
| [r/xteinkHax `1wdfpij`](https://old.reddit.com/r/xteinkHax/comments/1wdfpij/) | 2026-09-11 | *"Anyone to test my firmware on X4 Classic?"* — a developer **without** the hardware |
| u/Diirge in `1wbxvvg` | 2026-09-10 | *"CrossPoint sleep screen rendering got much better as of today on the x4c"* — firsthand, dated, on-device |

## The teardown that does not exist yet

[r/xteinkereader `1wcgqub`](https://old.reddit.com/r/xteinkereader/comments/1wcgqub/),
2026-09-10. A request for *"high-resolution photos of both sides of the PCB,
ideally with the ESP32-S3 and BM8563 RTC area clearly visible"*, to determine
**whether BM8563 `CLKOUT` (pin 7) reaches ESP32-S3 `XTAL_32K_P` / GPIO15** — which
would enable a low-power always-on BLE mode with the CPU in light sleep.

The only reply, u/scarf__barf: *"there's only a handful of units circulating in
the publics' hands right now… More people will have the X4 Classic delivered in
~7-10 days."*

**Status: open.** No X4 Classic PCB photograph existed anywhere on 2026-09-10.
The FCC internal photographs become public **2027-01-16** and will answer it.
See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

## One thing the community got wrong, preserved

The 2026-06-22 sighting ([r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/),
300 pts) predicted *"Physical buttons + frontlight but no touchscreen"*. The
buttons and the absence of touch were right. **The frontlight was wrong**, and
the vendor's own spec block now says `Front light: No`. The same hope recurred
through six further threads between June and September and was wrong every time.
