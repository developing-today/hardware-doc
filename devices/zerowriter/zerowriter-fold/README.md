# Zerowriter Fold

> Second-generation Zerowriter: 6" frontlit e-ink, folding laptop-style enclosure, hot-swap Choc keyboard.
> **Kickstarter live** at the time of this snapshot · First Wave **~$239 USD** (retail ~$329) · shipping expected **late 2026**
> Research snapshot **2026-08-24**

> ⚠ **Scope:** this is an **overview from vendor marketing material only**. The Fold was not the research target — it was discovered while correcting the [ZeroWriter Ink](../zerowriter-ink/README.md) record. No design files exist publicly yet, nothing has been independently verified, and no unit exists in the wild. Treat every figure below as a **vendor claim about an unshipped product**.

## Specifications (as claimed)

| | |
|---|---|
| Display | **6" e-ink, frontlit, 10 brightness levels**. 5" × 3.75" viewing area |
| Keyboard | Low-profile mechanical, **Choc v1**, hot-swappable, standard 60 % layout, custom keycaps |
| Dimensions | **12" × 5" × 1.25"** closed; opens to **0.6"** thin |
| Weight | **900 g** |
| Battery | **50–100 hours**, instant-on |
| Storage | microSD |
| Connectivity | USB-C + SD |
| File formats | **`.txt` and `.md`** |
| Price | ~$329 USD retail; **~$239 USD First Wave** (limited to 500 units) |
| Origin | Designed and assembled in **Ottawa, Canada**; stated capacity >300 units/month |
| Kickstarter | <https://www.kickstarter.com/projects/zerowriter/zerowriter-fold> — "Projects We Love" |

## What is different from the Ink

| | [Zerowriter **Ink**](../zerowriter-ink/README.md) | **Zerowriter Fold** |
|---|---|---|
| Display | 5.2" Inkplate 5 Gen 2, 1280×720, **no frontlight** | **6" frontlit**, 10 levels |
| Form factor | Flat slab, 300 × 195 × 15 mm | **Folding**, laptop-style, adjustable angle |
| Weight | not published | 900 g |
| Battery | ~100 h claimed | 50–100 h claimed |
| Formats | `.txt` | **`.txt` + `.md`** |
| Price | $285 | ~$329 retail / ~$239 First Wave |
| Platform | Soldered Inkplate 5 Gen 2 respin | **In-house** — "developed our own underlying display technologies, boards, and processes" |
| Status | Shipping since Jan 2026 | Prototype; ships late 2026 |

The most consequential difference is the last one: the Ink is built on a [Soldered Inkplate](../../soldered-electronics/inkplate-5/README.md), whereas the Fold is claimed to be **in-house hardware**. If accurate, the Fold will not inherit the Inkplate Arduino library or the TAPR-licensed design data, and the [Inkplate research](../../soldered-electronics/inkplate-5/README.md) will not transfer.

**The frontlight is the headline hardware addition** and the most-requested missing feature on the Ink.

## "Zerowriter Core" — and what it means for the Ink

The Fold introduces a named software platform:

> Zerowriter Fold runs on **Zerowriter Core**, written in Arduino and **releasing as open source in the coming months**. Open source means that even if the company isn't around someday, people can still build, modify, and develop for the Fold.

This is directly relevant to a finding in the Ink record. I noted that the Ink's **main application firmware is published only as binaries** despite the project's open-source positioning ([`gaps-and-conflicts.md` §3a](../zerowriter-ink/gaps-and-conflicts.md)). The Fold's page confirms that framing: Core is described in the **future tense** — "releasing as open source in the coming months."

So as of 2026-08-24, **neither product's main application is open source yet**, and the vendor is stating an intention rather than describing a current state. Whether "Zerowriter Core" also covers the Ink is **not stated**.

## Positioning

The marketing is unusually explicit about what the device refuses to do:

> **No WiFi required · No notifications · No AI integrations · No mandatory cloud · No subscriptions · No tracking · No browser**

> No subscriptions. **Venture capitalists hate us.** Buy it once, own it forever.

One networked feature is planned:

> **In development: Cloud Push** — Optionally send files to your personal Google Drive over wifi. Coming soon.

Two operating modes carry over from the Ink: **Drafting Mode** (always-forward, distraction-free) and **Word Processing Mode** (editing, bookmarks, document management).

## Company background (vendor's own account)

> We started in **2024** with a viral DIY project and a Raspberry Pi Zero (hence, the name). In **'25 and '26**, we've shipped Zerowriter Ink to writers around the world — and we still are! We learned everything about building consumer electronics the hard way and developed our own underlying display technologies, boards, and processes.

This corroborates the lineage documented in the Ink record: [`zerowriter1`](../zerowriter-ink/README.md#lineage) (Raspberry Pi Zero, MIT) → Zerowriter Ink (Inkplate-based, Crowd Supply 2024) → Zerowriter Fold (in-house, Kickstarter 2026).

Also disclosed: an **Indie Author Program** purchasing books from indie authors at wholesale to include in the box.

## Shipping and import costs

Unusually candid, and worth recording because it affects real cost:

> Shipping, handling, taxes, tariffs, and/or VAT will all be handled via a **pledge manager after the campaign ends** — they're **not included** in the First Wave price.
>
> Raw shipping ≈ **$20–35 USD**. European customers should expect **VAT on top** (~19 % Germany, 20 % France/UK, up to 25 %+ Scandinavia). **American customers: as of 2026, goods imported from Canada carry approximately a 10 % tariff.**

So a US First Wave order lands nearer **~$285–300** all-in than the advertised $239, and an EU order nearer **~$310–330**.

## Open questions

Everything, essentially. Specifically:

- **What SoC?** Not stated. The Ink uses an [ESP32-WROVER](../../../components/espressif/esp32-wrover/README.md) plus a second [ESP32-WROOM-32U](../../../components/espressif/esp32-wroom-32u/README.md) for the keyboard; whether the Fold repeats that is unknown.
- **What display controller and panel?** "Developed our own underlying display technologies" is marketing language that could mean anything from a custom PCB around an off-the-shelf E Ink panel to genuine controller work.
- **Will design files be published?** The Ink's hardware is on GitHub under GPL-3.0. Nothing has been said about the Fold's.
- **Does "Zerowriter Core" cover the Ink too**, or only the Fold?
- **Is the keyboard still a separate ESP32** on its own UART? If so, the [flash-requires-opening-the-case problem](../zerowriter-ink/firmware-and-updates.md) may recur.
- **Battery**: "50–100 hours" is a wide range and no capacity is given.
- No independent review, teardown or measurement exists — the product has not shipped.

## Sources

Full manifest with class, medium, retrieval dates, what each source establishes and its
limitations: **[`sources.md`](sources.md)**.

| Source | URL | Class |
|---|---|---|
| Product page (retained snapshot) | <https://zerowriter.ink/pages/zerowriter-fold> | primary (marketing) |
| Kickstarter campaign | <https://www.kickstarter.com/projects/zerowriter/zerowriter-fold> | primary — **not retrieved**; HTTP 403 to every user agent |

Retrieved 2026-08-24; re-verified 2026-08-28. A local snapshot of the product page is kept at
[`artifacts/product-page-2026-08-24.html`](artifacts/product-page-2026-08-24.html).

> The [vendor guide](../../../vendors/zerowriter/README.md) records that `zerowriter.ink` **403s a
> standard Chrome user agent** on `/pages/*`. **That no longer reproduces** — on 2026-08-28 default
> `curl`, Chrome 131 and `WhatsApp/2.23.20.0` all returned HTTP 200. The live page has also drifted
> from the retained snapshot. See [`sources.md` §3](sources.md#3-retrieval-findings).

The Kickstarter campaign page was not fetched and is likely to contain substantially more technical
detail, including updates. That is the obvious next step for anyone researching this device.

## Component records

**None, and correctly so.** The Fold has no published bill of materials, no design files and no
teardown, so there is nothing to link to [`components/`](../../../components/README.md). Every part
named on this page belongs to the [ZeroWriter Ink](../zerowriter-ink/README.md), not to the Fold.

## Related

- [Source manifest](sources.md)
- [ZeroWriter Ink](../zerowriter-ink/README.md) · [its sources](../zerowriter-ink/sources.md) — the shipping first-generation product
- [Zerowriter vendor guide](../../../vendors/zerowriter/README.md)
- [Soldered Inkplate 5 / Gen 2](../../soldered-electronics/inkplate-5/README.md) — the Ink's platform, which the Fold is claimed **not** to use
- [Component index](../../../components/README.md) · [Device index](../../README.md)
