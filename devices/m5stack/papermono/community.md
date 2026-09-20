# Community, editorial and project coverage — M5Stack PaperMono

> Snapshot **2026-09-01**, eleven days after launch. Two consecutive broad search passes.
>
> ## The finding, stated before the evidence
>
> **At the snapshot date there were zero written independent reviews of this device.** One
> hands-on video existed, published on day 8, self-described as a first look, carrying a vendor
> affiliate link. **Every written article traces back to a single vendor blog post.** Hackaday
> published nothing. Hackster returned nothing reachable. Tom's Hardware returned nothing.
>
> That is not a criticism of the press. It is a direct consequence of the supply situation:
> **you cannot review hardware nobody can buy**, and this product was purchasable for
> approximately nine minutes ([`market-and-pricing.md` §7](market-and-pricing.md#7-availability-history)).
> A 162-point Hacker News thread and 61 590 video views indicate the opposite of disinterest.
>
> **The real independent signal is code, not articles** — and it is genuinely strong (§4).

## What this page is, and what it is not

This page catalogues **coverage** — who said what about this device, in what medium, and what
kind of evidence it is. Its companion, [`projects-and-community.md`](projects-and-community.md),
covers the **projects themselves** in depth: what each one builds, how, and against which
hardware.

> **That companion was being written by a parallel session at the time this page was created.**
> If the link above does not resolve in your checkout, that pass has not landed. Nothing on this
> page depends on it; §4 here summarises each project's *evidentiary* value only, and deliberately
> stops short of describing what the code does.

Also related but distinct: [`gaps-and-conflicts.md`](gaps-and-conflicts.md) holds every conflict
in the whole record; §6 below extracts the subset that came from community claims.

## Contents

- [1. Evidence-type key](#1-evidence-type-key)
- [2. Written and video coverage](#2-written-and-video-coverage)
- [3. Discussion threads](#3-discussion-threads)
- [4. Third-party code — the strongest independent evidence](#4-third-party-code--the-strongest-independent-evidence)
- [5. Where the conversation is not happening](#5-where-the-conversation-is-not-happening)
- [6. Claims examined and rejected](#6-claims-examined-and-rejected)
- [7. Community claims that survived checking](#7-community-claims-that-survived-checking)
- [8. Prevalence — what the numbers do and do not support](#8-prevalence--what-the-numbers-do-and-do-not-support)
- [9. Retrieval limitations](#9-retrieval-limitations)

---

## 1. Evidence-type key

The method requires each contribution to be classified by what kind of evidence it is, and
explicitly states that popularity and production quality do not increase authority.

| Code | Meaning |
|---|---|
| **M** | **Firsthand measurement** — a number someone produced from an instrument or an instrumented run |
| **O** | **Firsthand ownership / use report** — "I have one and it did X" |
| **RD** | **Reproduced documentation** — accurate restatement of a vendor document, adding nothing |
| **P** | **Demonstrable project** — code that exists and can be read |
| **I** | **Informed interpretation** — a reasoned inference from documents, correctly flagged or not |
| **Op** | **Opinion** |
| **H** | **Hearsay** — attributed to a source the speaker cannot produce |
| **U** | **Unsupported assertion** |
| **V** | **Vendor-published** — the origin, not independent coverage |

**Across every item catalogued on this page, the count of `M` — firsthand measurement — is
one**, and it is a *self-reported* validation claim in a repository README rather than an
instrumented measurement (§4). There is no measured number about this device from anyone.

## 2. Written and video coverage

| # | Title | Author / channel | Publisher | Date (UTC) | Medium | Evidence | Source |
|---|---|---|---|---|---|---|---|
| 1 | "M5Stack Launches PaperMono: A Compact E-Ink Development Terminal for Connected Projects" | M5Stack | shop.m5stack.com | 2026-08-21 | vendor blog | **V** — **the origin of nearly all other written coverage** | S50 |
| 2 | "New Arrivals: PaperMono & PaperMono-Lite" | M5Stack | YouTube | 2026-08-21 06:59 · 16 938 views | video | **V** | S81 |
| 3 | "ESP32-S3 handhelds with 3.97-inch e-paper and optional LoRa/NFC" | Giorgio Mendoza | **LinuxGizmos** | 2026-08-21 05:19 · 5 665 views | blog | **RD** — spec restatement, no hardware | S76 |
| 4 | "M5Stack Paper Mono – An ESP32-S3 e-paper development board with 3.97-inch touchscreen, LoRa, and NFC" | Jean-Luc Aufranc | **CNX-Software** | 2026-08-21 16:43 (mod. 08-22) | blog | **RD + two small `O`/`I` observations** — see below | S77 |
| 5 | "Dispositivo portátil ESP32-S3 con papel electrónico de 3,97 pulgadas y LoRa/NFC opcional" | — | **MuyLinux** (ES) | 2026-08-23 21:48 | blog | **RD** — a machine-flavoured translation of #3; renders "frontlight" as *faro* ("beacon") | S78 |
| 6 | "Lilbits: More phone-sized E Ink gadgets" | Brad Linder | **Liliputing** | 2026-08-28 12:10 | blog roundup | **RD**, and **contains a price/configuration error** (§6) | S79 |
| 7 | **"M5Stack PaperMono: The Ultimate ESP32 Pocket Gadget?"** | **Volos Projects** | YouTube | **2026-08-29 16:21 · 61 590 views** | video | **O + Op** — **the only hands-on found anywhere** | S80 |
| 8 | "Unboxing multiple M5Stack products in one time!" | IAMLIUBO | YouTube | 2026-08-25 · **145 views** | video | **O** — genuine unboxing including both SKUs, negligible reach, no spec claims | S82 |
| 9 | Tux Machines aggregator items (≥ 4 URLs) | — | news.tuxmachines.org | 2026-08-21/22 | aggregator | **RD** — verbatim re-syndication of #3. **Rejected as coverage**; noted only because it inflates search-result counts | S83 |

### The two independent observations in the entire written corpus

Both are CNX-Software's, and both are small enough to quote in full:

1. **"epd_fastest – 0.07 s; note: ghosting visible in demo"** — an observation of **the vendor's
   demo video**, not of hardware. Evidence type **I**, correctly scoped by CNX itself. It is
   nonetheless the only thing anyone has said about this display's real-world behaviour, and it
   is consistent with the vendor's own precaution to perform a full refresh every ~10 partial
   refreshes.
2. **"It's not listed on AliExpress (anymore)"** — an availability observation, **independently
   reproduced here on 2026-09-01** (S58). Evidence type **O**, and it holds.

CNX also has a **dimension conflict** with the vendor: 101 × 61 × 7.95 mm against the docs'
62.0 × 101.0 × 8.0 mm. Neither was measured; the vendor figure is used throughout this record.

### On the one hands-on video

Volos Projects (day 8, 61 590 views) is the only person who has been seen holding one and
talking about it. Two caveats that must travel with any citation of it:

- **The description carries a vendor referral link** (`?ref=kmjp2x8a`) — a disclosed commercial
  relationship, which does not invalidate anything but must be recorded.
- **It repeats "built-in backlight".** The device has a **frontlight**, which is a different
  thing on a reflective display: it lights the page from the front, and the panel itself is
  pure-reflective with no backlight of any kind. A small error, but it is the kind that
  propagates.

It is self-described as a first look. **No timing, current, range or battery figure appears in
it.** Evidence type **O + Op**, not **M**.

## 3. Discussion threads

| Venue | Thread | Date | Engagement | Evidence | Value |
|---|---|---|---|---|---|
| **Hacker News** | ["M5Stack Launches PaperMono"](https://news.ycombinator.com/item?id=49468593) | 2026-08-27 | **162 points, 58 comments** | **Op + H**, one adjacent **O** | The largest discussion anywhere, and it contains **no firsthand PaperMono measurement at all**. Recurring themes: M5Stack's hardware is good and its software is half-baked; everything is out of stock; XTEINK X4 Pro comparisons. `fmajid` gives a firsthand **PaperS3** ownership report ("clearer screen than my Pocketbook Verse") — adjacent, not this device. `dmitrygr` floats porting rePalm. `RobotToaster` raises Meshtastic/MeshCore support as an **open question**, not a claim. Also the origin of the driver-IC hearsay (§6) |
| **Hacker News** | [earlier submission of the same URL](https://news.ycombinator.com/item?id=49390702) | 2026-08-21 | 2 points, 1 comment | — | **Duplicate.** The submitter later notes it was ~8 h post-announcement and already sold out |
| **r/M5Stack** | ["Paper Mono coming August 21st"](https://old.reddit.com/r/M5Stack/comments/1vquxa5/paper_mono_coming_august_21st/) | 2026-08-17 | 198 score, 22 comments | **P-claims + Op** | Pre-launch leak from a vendor YouTube Short. The most valuable content in any thread: the `bb_epaper` and freeink.org support claims (§6), and Larry Bank's **correct and precise** statement of the PaperS3/PaperMono panel difference (parallel 4.7"/960×540 against SPI 3.97"/800×480) |
| **r/M5Stack** | ["Check out what's new this week!"](https://old.reddit.com/r/M5Stack/comments/1vuaneb/check_out_whats_new_this_week/) | 2026-08-21 | 75 score, 17 comments | **V + O + Op** | The vendor's own launch post. Vendor states pre-orders "reached the limit". Multiple independent **failed-purchase** reports (`shackburger`, `9mini-paralyses`). u/async2 surfaces the openelab.de pre-order — the lead that produced the EUR 79.95 observation. u/Tsixom's PaperS3 comparison, **verified accurate line by line** (§7) |
| r/hackernews, r/hypeurls | "M5Stack Launches PaperMono" | 2026-08-27/28 | 2 and 1 score | — | **Automated HN mirrors. Not independent coverage.** These are the *only* two hits for a site-wide Reddit search of `papermono` |
| **X / Twitter** | [@henry19840301](https://x.com/henry19840301/status/2090652363434647738) | **2026-08-21 04:09** | 87 likes, 23 665 views | **O — the strongest ownership evidence anywhere** | "Got lucky on Friday — the new M5Stack PaperMono Lite sold out in just one second. And YES I got one!" plus **four photographs**. The author is `github.com/MagicCube`, who then published a hardware-validated project (§4). Ownership corroborated across two independent surfaces |
| **X / Twitter** | [@berryxia](https://x.com/berryxia/status/2091105450494238837) | 2026-08-22 10:09 | 2 likes, 569 views | **O** (failed purchase) | Asks M5Stack for a restock, reports stock already gone |
| **X / Twitter** | [@M5Stack](https://x.com/M5Stack/status/2091116748686922069) | 2026-08-22 10:54 | 300 views | **V** | 「要等两三个月了」 — the primary restock statement (§6) |
| **community.m5stack.com** | — | — | — | — | **Inaccessible.** `/api/search` → **HTTP 401** "A valid login session was not found"; `/search?term=` → 302. `/api/recent` is open and returned 198 topics with **no PaperMono topic** in that window. **No determination possible** (S85) |

**The `community.m5stack.com` row is the most consequential gap on this page.** The vendor's own
forum is where owner reports for M5Stack products typically appear first, and it is the one venue
that could not be searched at all. Its absence from this catalogue is an **auth-wall, not a
negative** — do not read "nothing on the vendor forum" into it. The `/api/recent` window is 198
topics deep and is a weak negative at best.

## 4. Third-party code — the strongest independent evidence

**Four third-party projects plus a third-party SDK appeared within eleven days of launch.** That
is the strongest evidence anywhere that units actually shipped and ran. All dates from the GitHub
API, retrieved 2026-09-01.

| Repository | Created / pushed | Stars | Evidence | What it establishes |
|---|---|---|---|---|
| **`MagicCube/free-ink-on-paper-mono`** (S89) | 2026-08-25 / 08-27 | 3 | **M(self-reported) + P + O — the strongest single item** | FreeInk UI on a **PaperMono-Lite**. The README claims a complete verified hardware path: RX8130 time, M5PM1 battery/USB-power/charging telemetry, touch and physical buttons, light/dark switching, **frontlight held at 127/255**, async e-ink refresh with periodic full cleanup, a rectangular-refresh test bed with a PR-ready SDK patch, and "**verified disabling of M5PM1's dangerous default single-click reset**". Author = **Henry Li / @henry19840301**, the same person who posted the 04:09 UTC purchase photographs — **ownership corroborated across two unrelated surfaces** |
| **`Free-Ink/freeink-sdk`** (S90) | — | — | **I(informed by hardware) + P** | `libs/hardware/BoardConfig/include/PaperMonoBoard.h` is a detailed board bring-up sequencing the **M5PM1 and M5IOE1** — including disabling the PMIC's single-click reset **while preserving its hardware long-hold download escape**. That level of detail is not obtainable from a spec sheet. **Independently corroborates the same M5PM1 finding as the row above** — two sources, one hardware behaviour |
| **`MingRZou/PaperMono-Launcher`** (S91) | 2026-08-30 | 1 | **P + O** | Self-described "**hardware-validated**", with a photograph captioned "PaperMono-Launcher on real hardware". Explicitly a **port** of [`bmorcelli/Launcher`](https://github.com/bmorcelli/Launcher) from the PaperS3 — concrete evidence that the two platforms are **not drop-in compatible** |
| **`EggUncle/PaperMonoCalendar`** (S92) | 2026-08-31 | 0 | **P**; ownership **claimed, not shown** | Landscape calendar firmware for C153 with BLE activity tiles and RTC sync. **Commendably honest**: the README states its preview images are software-generated, *not device photographs* (「非设备实拍」), and that all displayed data is fictional sample data. It describes itself as extracted from a real-device project but **shows no hardware** |
| **`hectorzin/M5PaperMono-HomeAssistant-ESPHome`** (S93) | 2026-08-27 / 09-01 | 0 | **P**, early WIP | ESPHome "fase 1" minimal hardware test (SSD1677 + FT6336G via M5IOE1). **Honest about its own uncertainty** — the display/touch rotation section is labelled "**hipótesis de prueba**", i.e. unverified at time of writing |
| **`MarsTechHAN/crosspoint-reader-mono`** (S95) | — | — | **P** | The upstream of the CrossPoint e-reader build distributed through M5Burner. A working binary was **published one day after launch** and is retained in this record — see [`factory-firmware.md` §3](factory-firmware.md#3-the-community-image--crosspoint-paper-mono-cjk-150-rc). Note the M5Burner *uploader* is `IAMLIUBO`/`imliubo`, a different person, whose home directory appears in the binary's build paths |
| `crosspoint-reader/crosspoint-reader` (S94) | — | — | **P**, roadmap only | `ROADMAP.md:40` lists PaperMono among "ESP32-S3 class hardware (X4 Pro, PaperMono, Seeed Sticky)" targets. **Roadmap, not shipped support** |
| `tanakamasayuki/M5Stack-Arduino-Check` (S96) | — | — | **RD of a toolchain** | Contains `3.3.9/variants/m5stack_papermono/pins_arduino.h` — evidence that the board variant exists in arduino-esp32 3.3.9 |

### What the code evidence supports, and what it does not

**Supported.** Units shipped and boot. The M5PM1 and M5IOE1 can be driven from third-party code.
The frontlight can be set. The RTC reports time. Battery and charge telemetry can be read from
the M5PM1. Touch and both buttons respond. Async e-ink refresh with periodic full cleanup works
well enough to build a UI on. The M5PM1's default single-click reset is disruptive enough that
**two independent projects disable it** — and one of them documents how to do so without losing
the download-mode escape.

**Not supported.** Any *number*. No project reports a current, a battery runtime, a refresh time,
a Wi-Fi throughput, a LoRa range or a temperature. Every claim above is a **self-reported
functional assertion in a README**, which is real evidence and is not a measurement.

**One claim is unresolved and should not be repeated.** Larry Bank (`bitbank2`) wrote on
2026-08-17 — four days *before* launch — "I already support the Paper Mono and Paper Color in my
`bb_epaper` library … I'm also adding both to `trmnl-firmware` (TRMNL BYOD support)", and u/Diirge
wrote "We also support this in the freeink.org sdk as it's what powers crosspoint." Both were
necessarily written against documentation and schematics rather than hardware. **A GitHub code
search of `bitbank2/bb_epaper` for "PaperMono" returned 0 matches on 2026-09-01** (S97). The
support may be under a different identifier, on an unpushed branch, or it may not have landed.
**Do not cite `bb_epaper` PaperMono support as fact.** The freeink.org half of the claim *is*
separately supported — see the `freeink-sdk` row.

## 5. Where the conversation is not happening

Negative results, each from a search that returned a working result page. These are results.

| Venue | Query | Result |
|---|---|---|
| **Hackaday** | `hackaday.com/wp-json/wp/v2/search?search=papermono` | **`[]`** — nothing. For contrast the same endpoint returns two older posts for `m5paper` (2021-11-12 weather display; 2026-07-21 "20 FPS on E-Paper Display Without Help") (S84) |
| **Reddit, site-wide** | `papermono` | **Two results, both bot mirrors of the HN post.** The only genuine discussion is two threads in the vendor's own subreddit |
| r/esp32, r/eink, r/ereader, r/CrossPointReader, r/einkesp32 | various | **Zero** PaperMono results |
| Tom's Hardware, Adafruit blog | — | Nothing reachable |
| **Hackster.io** | `papermono` | `/search?q=` returns 200 but is a **JS shell**; `/search.json` and `/api/v2/projects` both return HTML. **No working path found — inaccessible, not negative** (S87) |
| **Bluesky** | `app.bsky.feed.searchPosts` | **403 for every user agent tried.** Inaccessible (S86) |

> **A retrieval trap worth reusing.** Reddit tokenises `papermono` and `paper mono` differently.
> `papermono` returned **0** results within r/M5Stack while `paper mono` returned the two real
> threads. **Always search both the closed-up and the spaced spelling** of a compound product
> name, in every subreddit. Recorded in [`research-log.md`](research-log.md) and the crawler
> access table.

## 6. Claims examined and rejected

Every row here was checked against its own citation. This table is the community-sourced subset
of [`gaps-and-conflicts.md`](gaps-and-conflicts.md#claims-examined-and-rejected); that page is
canonical.

| Claim | Source | Evidence type of the claim | Why rejected |
|---|---|---|---|
| **"Restock is 2–3 months because they're out of eink driver IC"** | HN `big_toast`, 2026-08-27, citing `x.com/M5Stack/status/2091116748686922069` | **H** | **The cited tweet was retrieved in full, with its parent and thread root.** It says only 「要等两三个月了」 ("two or three months"). The parent merely asks for a restock; the root is a marketing post. **The driver-IC reason appears nowhere in the cited chain.** This is the clearest example on the page of a plausible mechanism attaching itself to a real statement |
| "I can't remember where I read it, but … they didn't expect a restock until next year" | HN `notatoad`, 2026-08-27 | **H**, self-flagged | Honestly flagged by its own author as unsourced. Recorded, not used |
| **"$55 … with … NFC, LoRa"** | **Liliputing**, 2026-08-28 | **U** | Factually wrong. **$55 is the Lite, which has neither.** The NFC/LoRa model is $65 |
| **"PaperMono is the successor to / an upgrade over the PaperS3"** | several launch articles; implied by the naming | **U** | Contradicted by the vendor's own specifications on every measurable display and power axis: **~35 % fewer pixels, 4 grey levels vs 16, 1150 mAh vs 1800 mAh, no expansion port** — and the PaperS3 is **cheaper**. See [`product-history-and-family.md` §4](product-history-and-family.md#4-papermono-is-not-a-successor-to-the-papers3) |
| **"Bluetooth 5.0 LE + Mesh connectivity"** | CNX-Software, 2026-08-21 | **I** | A reasonable inference from the SoC — the ESP32-S3 does have BLE 5 and Mesh — but **not a vendor claim.** M5Stack's specification tables for both SKUs list **only** "2.4 GHz Wi-Fi", and no BLE bring-up for this board appears in any vendor document or example. Publication inference, presented as specification |
| **"Half the price of the XTEINK X4 Pro"** | HN `NDlurker`, 2026-08-27 | **U** (the ratio); **I** (the compatibility half) | **No X4 Pro price was captured**, so the ratio is unverifiable. More fundamentally, a sealed reader and a development board are not comparable on price. The *CrossPoint compatibility* half is separately supported |
| **"Sold out in one second"** | @henry19840301, 2026-08-21, repeated on HN | **Op** / colloquial | The checkable fact is a **nine-minute gap** between storefront publication and the sell-out report. HN user `bahmboo` made the same point at the time. **Record the nine minutes** |
| **`bb_epaper` supports PaperMono** | `bitbank2` on r/M5Stack, 2026-08-17 | **U**, pre-launch | **0 code-search matches on 2026-09-01** (§4). Unresolved rather than refuted — it may exist elsewhere |

**Six of eight rejected claims come from written or forum sources; none comes from the code.**
That asymmetry is the practical lesson of this page: on an eleven-day-old product with no
supply, the repositories are more reliable than the articles.

## 7. Community claims that survived checking

Recorded with the same rigour, because confirming that someone was right is also a result.

| Claim | Source | How it was checked | Outcome |
|---|---|---|---|
| **u/Tsixom's PaperS3-vs-PaperMono specification comparison** | r/M5Stack, 2026-08-21 | Checked **line by line** against `docs.m5stack.com` | **Accurate on every point** |
| Larry Bank's statement of the panel difference — parallel 4.7"/960×540 against SPI 3.97"/800×480 | r/M5Stack, 2026-08-17 | Against both vendor product pages | **Correct and precise**, four days before launch |
| u/poulpy123: "More expensive, smaller screen and lower resolution that the previous version" | r/M5Stack | Against vendor specifications | **Correct**, and reached independently of this record |
| **The M5PM1's default single-click reset is disruptive** | `MagicCube/free-ink-on-paper-mono` **and** `Free-Ink/freeink-sdk`, independently | Two unrelated projects describe and disable the same behaviour; the M5PM1 register map supports the mechanism | **Corroborated ×2.** The strongest community-sourced *behavioural* finding in this record, and it is now reflected in [`features/buttons-and-rgb-led.md` §6](features/buttons-and-rgb-led.md#6-the-power-button) |
| CNX-Software: "not listed on AliExpress (anymore)" | CNX-Software, 2026-08-21 | Independently reproduced 2026-09-01 (S58) | **Holds** |
| u/async2 surfaces the openelab.de pre-order | r/M5Stack, 2026-08-21 | Retrieved directly; EUR 79.95 "(Vorverkauf)" | **Holds** — this lead produced a row in [`market-and-pricing.md`](market-and-pricing.md#2-current-observations--papermono-c153) |

## 8. Prevalence — what the numbers do and do not support

The method warns that anecdotes establish that an experience *occurred*, not how common it is,
and that prevalence wording requires a defensible sample.

**What can be said with the sample inspected:**

- **Three independent failed-purchase reports** were found across the two r/M5Stack threads and X
  (`shackburger`, `9mini-paralyses`, @berryxia), plus one successful purchase (@henry19840301)
  and one unboxing showing both SKUs (IAMLIUBO). **Sample: two Reddit threads, one HN thread and
  a targeted X search.** That is enough to say purchases both succeeded and failed on launch day.
  It is **not** enough to say anything about a rate.
- **Two of six third-party projects claim hardware validation** and one of those shows a
  photograph. Sample: six repositories, which is the complete set found by GitHub search and code
  search on 2026-09-01.
- **Zero of fifty-eight Hacker News comments contain a firsthand PaperMono measurement.** That is
  a complete enumeration of one thread, and it is the most defensible prevalence statement on this
  page precisely because the denominator is known.

**What cannot be said:** anything about reliability, yield, defect rates, real battery life, or
how the device performs for any workload. Nobody has reported using one for longer than a video.

## 9. Retrieval limitations

Stated so the next pass does not mistake a wall for a finding.

| Limitation | Effect |
|---|---|
| **`community.m5stack.com` is auth-walled** (HTTP 401) | The vendor's own forum — the likeliest first home for owner reports — is **entirely unsearched**. This is the largest hole in the catalogue |
| **Hackster.io has no working search path** | JS shell; `/search.json` and `/api/v2/projects` both return HTML |
| **Bluesky's public XRPC API returned 403 to every user agent** | The crawler access table's ✓ for Bluesky evidently refers to `bsky.app` HTML, not the API |
| **DuckDuckGo and Marginalia were both unusable** on 2026-09-01 | DDG returned an HTTP 202 anomaly page — *not* a 403, and easy to mistake for success; Marginalia served a bot-wait interstitial. **Mojeek was the only general web search engine that worked**, and it is how LinuxGizmos, Liliputing and MuyLinux were found at all |
| **Mojeek result counts are inflated by re-syndication** | Tux Machines dominated pages 2–5. Read the URLs, not the count |
| **Two passes, one snapshot date** | Everything here describes **2026-09-01**. It is a reproducible broad-coverage snapshot, not proof that no other coverage exists, and it is a statement about an eleven-day-old out-of-stock product |
| **Videos were not watched in full** | Timestamps were not recorded for either video; the classification of the Volos video rests on its title, description, framing and the absence of numeric claims in the retrieved metadata |

**Re-run this sweep after the restock.** Almost every "zero" on this page is a consequence of
supply rather than of the product, and the two repositories with hardware validation
(`MagicCube/free-ink-on-paper-mono` and `Free-Ink/freeink-sdk`) are the highest-value independent
sources in existence for this device until that changes.

## Related

- [`projects-and-community.md`](projects-and-community.md) — the projects themselves, in depth *(written by a parallel pass; see the note at the top of this page)*
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — the canonical conflict list, including every claim rejected above
- [`product-history-and-family.md`](product-history-and-family.md) — the dated chronology these items sit in
- [`market-and-pricing.md`](market-and-pricing.md) — the sell-out evidence and the restock conflict
- [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) — the XTEINK and PaperS3 comparisons the community makes
- [`factory-firmware.md`](factory-firmware.md) — the community CrossPoint image, parsed
- [`compatibility-and-status.md`](compatibility-and-status.md) — community reports keyed to version
- [`research-log.md`](research-log.md) — every service, query, filter and disposition
- [`sources.md`](sources.md) — S50, S68–S97
