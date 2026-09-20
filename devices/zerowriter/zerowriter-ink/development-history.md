# ZeroWriter Ink — development history and design rationale

> Why the device is built the way it is, in the developer's own words.
> Compiled **2026-08-24** from all **17 Crowd Supply campaign updates** (2024-09 → 2026-05). Preserved locally at [`artifacts/crowdsupply-updates/`](artifacts/crowdsupply-updates/).

These updates are the only place where the design decisions are explained. They answer several questions that the repository, the campaign page and the press coverage all leave open — most importantly **why the keyboard has its own ESP32**, and **why the main firmware still is not published**.

---

## The e-paper latency problem, and how it was solved

This is the central engineering story of the product, told in *"Optimizing E-Paper Performance"*.

> The reason Inkplate appealed to me originally was their fast e-paper promising very fast partial updates…
>
> When it came to Zerowriter Ink, we jumped on their new generation panel: **Inkplate 5v2**. The updated screens operate at a much higher resolution: that means more text on the screen, at a higher clarity.
>
> **The downside? Well, it turned out that the higher resolution panels came at a cost: speed.** The new panels looked great, but **operated at about 200 ms**. This was a decent chunk slower than the panel I'd been developing into Zerowriter Ink…

**Note what this implies about the prototype.** "the panel I'd been developing into Zerowriter Ink" was the **gen-1 Inkplate 5** (`ED052TC2`, 960 × 540). The move to Gen 2 (`ED052TC4`, 1280 × 720) was a **mid-project hardware change made after funding**, taken for resolution and paid for in refresh speed. Anyone remembering an earlier gen-1-based ZeroWriter Ink is remembering the prototype — see [`README.md`](README.md#which-inkplate-generation--gen-2-confirmed-five-ways).

The fix came from **[@bitbank2](https://github.com/bitbank2) (Larry Bank)**, an e-paper optimisation specialist:

> The end result? Zerowriter Ink now operates at **about 100 ms** — that is **roughly twice as fast as the original Inkplate 5v2**, and **about 50 % faster than the lower-resolution Inkplate 5**.

| Configuration | Partial-refresh latency |
|---|---|
| Stock Inkplate 5 (960×540) | ~150 ms *(implied by "50 % faster")* |
| **Stock Inkplate 5 Gen 2 (1280×720)** | **~200 ms** |
| **ZeroWriter Ink (same panel, optimised)** | **~100 ms** |

### How this squares with Soldered's own numbers

Soldered publishes **0.26 s fast refresh** for the Inkplate 5 V2 and **0.12 s** for the Inkplate 5 ([Inkplate 5 § family comparison](../../soldered-electronics/inkplate-5/README.md#family-comparison)). ZeroWriter reports ~200 ms and ~150 ms for what sound like the same operations.

The two sets are **close but not identical**, and neither party states test conditions — refresh timing depends on update region size, temperature, waveform and greyscale mode. Treat them as **the same ballpark from different measurements**, not as a contradiction. What both agree on: **the Gen 2's higher resolution costs refresh speed**, and ZeroWriter's software recovers more than that cost.

**This is the most interesting single fact about the device**: it runs the same panel as a stock Inkplate 5 Gen 2 but roughly twice as fast, purely through driver and font optimisation. Anyone building on an Inkplate should know that the stock library is not the performance ceiling.

### Why latency mattered so much

> a lower latency panel opens up a ton of development possibilities. Less time spent on updates is more time the MCU can spend on other tasks. More responsive controls and feedback means things like **cursor-based editing** and more traditional word-processing features are much more approachable.

And on the feature it unlocked:

> Basically, **latency made it difficult to use before. But now, there's no latency.** Now it just… works.

Cursor-based editing — the most requested feature — was gated on the display driver, not on UI work.

---

## Why the keyboard has its own ESP32 — answered

I had recorded this as an open question, noting only that the firmware author called it over-specified. The deep-dive update gives the actual reason:

> I decided to use a **clocked down ESP32** to drive the keyboard, which is **overkill for a keyboard MCU**, but now **anyone looking to customize the keyboard only needs to learn one MCU for the whole project** — both the Zerowriter and Inkplate use the same **ESP32-WROOM module**.

So it is a **deliberate developer-ergonomics decision**, not a parts-bin accident: one toolchain, one MCU family, one set of docs for anyone modifying either board. That is consistent with the "clocked down" description — the firmware runs at [80 MHz with radio torn down](keyboard.md#power-management).

It also confirms the modularity intent:

> Note that the **keyboard PCB is a removable component**. This means you could swap out the keyboard entirely for a different design, like an **ortho keyboard layout, or a full 100 % keyboard, maybe make it tiny with a 40 % keyboard**, or whatever you want!

Which is exactly what the [6-pin connector](inter-board-wiring.md) and the byte-per-key protocol enable — a replacement keyboard only has to emit key indices 0–60 over UART.

---

## Why the main firmware is not published yet — answered

Another open question. From *"More Orders Fulfilled Plus a Pre-Launch Announcement"*:

> As promised, the **source code and design files for Zerowriter Ink will be published in GitHub when the final batch of units is fulfilled.** This is in respect to those who have been waiting very patiently for their units.

And earlier, in the shipping/tariffs update, the staged plan:

> I'll release the **3D files** for people who want to print their own enclosure…
> I'll also put the **firmware and design files for the keyboard** up, initially…
> **Once we have a good number of units out in the wild, I'll push the main Zerowriter codebase**, along with some documentation.

That plan has been followed exactly, and explains the current state: hardware ✅, enclosure ✅, keyboard firmware ✅, **main codebase pending final fulfilment**. It is a deliberate sequencing decision, not an abandoned promise — though note the last fulfilment update (2026-04-15) said "about 4–6 weeks" to completion, and as of this snapshot (2026-08-24) the main codebase is still unpublished.

---

## The factory firmware partition bug — confirms the firmware analysis

From *"Progress Report, New Improvements"*:

> **Firmware.** Due to a mistake on my part, the flashed firmware from the factory was **not partitioned in a way that supported the Zerowriter's SD-card based update system**. So, early backers had to do a **manual update method which involved opening up their ZW Ink**. Subsequent units will be reflashed and partitioned…

This independently confirms what I inferred from parsing the binaries and the web-updater page ([`firmware-and-updates.md`](firmware-and-updates.md)): the "no version number in the menu ⇒ must web-flash first" symptom is a **factory partitioning error**, and the command-line merged image exists precisely because it "builds a new partition structure".

So there are effectively **three unit cohorts**:

| Cohort | Firmware state |
|---|---|
| **First batch** (early backers) | Mispartitioned — SD updates do not work until a one-time USB/web reflash |
| **Later batches** | Reflashed and repartitioned at the factory; SD updates work out of the box |
| **Second-pass units** | "firmware fixed and updated, the keyboards tweaked slightly, and some of the internal fixtures adjusted" |

---

## The font system

From *"Huge Performance Improvements…"*:

> Thanks to a new font library, and **@bitbank2's outstanding work**, Zerowriter Ink operate[s] on a new **compressed font system**. While offering some truly amazing performance increases, it also **enables users to convert and implement their own TTF fonts**.
>
> More fonts, more sizes, **in less memory. 80–90 % less memory, actually.**

Also a **1-bit-optimised font system**, and:

> This also means the **foundation is there to implement non-Latin languages: Chinese, Korean, Japanese, etc.**

A **Korean custom firmware** is mentioned as existing in a later update. The original Raspberry Pi project's font (**Courier Prime**) was ported over.

Character encoding moved **from ASCII to extended ASCII (256 chars)**, covering most Western/European languages — this is the basis of the [keymap format](keymap-format.md).

---

## Production and manufacturing

| Fact | Source |
|---|---|
| First production run **~600 units** | "Huge Performance Improvements" |
| Assembled in **Croatia by Soldered Electronics** ("product of Croatia") | "What We Don't Know About Tariffs…" |
| Soldered assembly ≈ **6 weeks**, then flashing, boxing, ship to **Mouser** for fulfilment | idem |
| Enclosure design refined with **Momentum Design** (Ottawa) | idem |
| Sold out or near it by 2026-04 | "More Orders Fulfilled" |

### The enclosure was redesigned mid-campaign

> The original design — while full of character — was based on a **4-piece enclosure** due to prototyping equipment… This all seemed fine until **field testing and shipping prototypes around the world, where some issues cropped up**… The revised enclosure will deliver **rigidity and simplify manufacturing**.

The original 4-piece design was promised as printable STLs for anyone who preferred it. Note the shipped enclosure is **3D printed**, with the expected consequences stated plainly:

> there's some mild level of "wear" to be expected from a 3D-printed part. You will find **seam lines**, stuff like that.

### Tariffs

> Everything was manageable and accounted for, **in a pre-tariff world**… If I could afford to, I would subsidize the import/tariff cost, but **all funds have been allocated**.

Consistent with the [Fold's](../zerowriter-fold/README.md) later disclosure of ~10 % US tariffs on Canadian-origin goods.

---

## What owners need on hand

From *"First Shipments and Resources to Get Started"* — a genuinely useful list:

> **USB-C cable** for charging · **M2 / 2.5 screwdrivers** (laptop/smartphone kind) · **micro SD card reader** · **keycap remover**

The screwdriver is not optional for first-batch units, since the initial update requires opening the case to [unplug the keyboard](firmware-and-updates.md#-you-must-unplug-the-keyboard-before-flashing-over-usb).

Also noted: Espressif's ESP32 updater "can be a bit funky", and community members help troubleshoot it.

## Community keymaps

> we have a couple people who have built keymaps for **DVORAK and French Canadian** layouts

Plus the **Korean custom firmware**. These live in the Discord rather than the repository, so they are not preserved here — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

---

## Timeline from the updates

| Update | Date | Substance |
|---|---|---|
| The Campaign Is Live | 2024-09 | launch |
| Fully Funded, Draftober Giveaway, CBC Radio Interview | 2024-10 | funded; CBC radio appearance |
| Why Open Source | 2024-10 | open-source commitments |
| Keycaps, Shoutouts and Backstory | 2024-11 | KiCad + keycap STL release promised |
| All Things Keyboard | 2024-11 | switch selection |
| The Final Stretch | 2024-11 | **enclosure redesign** 4-piece → revised |
| A Deep Dive Into Our New Keyboard PCB… | 2024-12 | **ESP32-for-keyboard rationale**; modular keyboard |
| Huge Performance Improvements… | 2024-12 | **font system**, cursor edits, extended ASCII, 600-unit run |
| New Timelines, New Features | 2025 | custom fonts via SD, failsafe internal storage |
| Optimizing E-Paper Performance | 2025 | **200 ms → 100 ms**, bitbank2 |
| What We Don't Know About Tariffs… | 2025 | teardown video, field testing, Croatia assembly |
| Shipping This Month, Tariffs, Pricing… | 2025 | **staged open-source release plan** |
| All The Latest… Plus A Retro Tribute | 2025 | unboxing; "firmware is locked in" |
| First Shipments and Resources to Get Started | 2026-01 | update procedure, tools needed |
| Progress Report, New Improvements | 2026-02 | **factory partition bug** |
| More Orders Fulfilled Plus a Pre-Launch Announcement | 2026-04 | source release tied to final fulfilment; Fold teased |
| Shipping Status and the Latest Developments | 2026-05 | **hardware files published**; Korean firmware |

---

## Evidence status

All quotations are **firsthand statements by the developer** (Adam Wilk) on the official campaign page — primary, but self-reported and promotional in context. The performance figures (200 ms / 100 ms) are **developer measurements with unstated conditions**, not independently verified, and no unit was available here to check them.

Where these updates conflict with or refine what I recorded earlier, the earlier documents have been corrected and cross-referenced.

## Related

- [`README.md`](README.md) · [`keyboard.md`](keyboard.md) · [`inter-board-wiring.md`](inter-board-wiring.md)
- [`firmware-and-updates.md`](firmware-and-updates.md) — the partition bug in practice
- [`software-and-shortcuts.md`](software-and-shortcuts.md) — the feature set these updates announce
- [Inkplate 5 / Gen 2](../../soldered-electronics/inkplate-5/README.md) — the panel being optimised
