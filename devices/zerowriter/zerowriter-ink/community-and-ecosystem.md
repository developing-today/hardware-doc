# ZeroWriter Ink — community, third-party firmware and owner reports

> What owners actually report, the community firmware ecosystem, and the **v2.1 release that supersedes everything in the GitHub repository**.
> Snapshot **2026-08-24**. Sources: `r/zerowriter` (retrieved with the WhatsApp UA — see [vendor guide](../../../vendors/zerowriter/README.md)) and `zerowriter.ink`.

---

## ⚠ The repository firmware is two major versions behind

`firmware_releases/` in the GitHub repo tops out at **SD-1.3**, and the repo README says "current public firmware is 1.30". **That is stale.**

| Version | Where | Status |
|---|---|---|
| 1.24 – 1.30 | GitHub `firmware_releases/` | superseded |
| **2.0 / 2.1** | <https://zerowriter.ink/pages/zerowriter-ink-2-0-early-access> | **Current, released July 2026, beta** |

> **Zerowriter Ink v2.1 — Software Beta** · Released: **July 2026**
> This is a **beta release** intended for early adopters comfortable with occasional rough edges. Install at your own risk. If you don't like it, you can always downgrade to a stable version.

**If you are researching or using this device, get firmware from `zerowriter.ink`, not from GitHub.** The repo is the source of truth for *hardware*; the website is the source of truth for *firmware*.

### v2.1 changes

| Area | Change |
|---|---|
| **SD engine** | "Works with any Micro SD Card **without filesize limitations or formatting headaches**" — fixes the long-standing card-compatibility complaints |
| **Keyboard** | Configurable **debounce**; "**+20 ms** is the recommended setting if you find you have key ghosting or typos" |
| **Accents** | Accent picker — press Alt + base character, tap to cycle |
| **Internal storage** | SD-first saves with automatic fallback to internal storage, now user-visible as **"HD"** |
| **Auto-backup** | Mirror every save to HD — "your writing is twice as safe" |
| **Writing stats** | Long-term tracking, streaks. ⚠ "**Requires a coin cell installed** for all timekeeping features" |
| **Markdown/Fountain** | Bold, italic, strikethrough, inline code, blockquotes, fenced code blocks, lists — **rendered inline as you type** |
| **Status bar** | Redesigned; cycle with `CTRL+TAB` |
| **Battery** | "Improved battery sensor accuracy" |
| **Privacy Render Mode** | Masks non-active body lines with glyphs — "useful for writing something steamy in public" |
| Menu | Redesigned; "greatly improved battery life" |

Update procedure is the normal SD path: unzip, ensure the file is named **exactly `firmware.bin`**, copy to the SD root (not a folder), reboot.

Pre-update advice from the vendor: **back up the SD card** and ensure **50 %+ charge**.

### The coin cell is not fitted

"Requires a coin cell installed for all timekeeping features" is a hardware statement. Both the stock Inkplate 5 Gen 2 and ZeroWriter's respin carry **`K11` = `CR2032_BS-6-1`**, a CR2032 holder for the [PCF85063A RTC](../../../components/nxp/pcf85063a/README.md) backup supply — but it **ships empty**.

So writing-streak tracking, and any feature depending on wall-clock time across power-off, needs the user to **fit a CR2032 themselves**. This is not mentioned in the campaign or the repo.

---

## The arrow-key conflict — RESOLVED by the developer

I documented a conflict between the keyboard firmware's matrix constants (`59 = RIGHT, 60 = DOWN`) and the shipped `keymap.json` (`59 = DOWN, 60 = RIGHT`). The developer settles it on Reddit:

> **The last 4 entries on the first keymap layer determine the arrow key layout.** This keymap is for UP DOWN LEFT RIGHT. If you add it to your SD card, it will load when you start up your ZW.
> — *tincangames* (Adam Wilk), in *"Arrow key remapping?"*

**The keymap is authoritative; the firmware constants are not used for key identity.** This confirms reading (1) of the two I offered in [`keymap-format.md`](keymap-format.md#-conflict-firmware-and-keymap-disagree-on-arrow-order) — the `LEFT_R`/`UP_R`/`RIGHT_R`/`DOWN_R` constants exist only for the vestigial panic chord and their naming is simply inaccurate.

Two practical notes from the same thread:

- **The online keymap editor greys out the arrow keys**, which is why the asker could not remap them. Edit `keymap.json` in a text editor instead — the arrows are plain magic strings.
- Alternate keymaps are published at [`utils/keymaps/`](artifacts/source-snapshots/zerowriter_ink/utils/keymaps/) in the repo. A user noted one supplied file "only ha[d] the middle keys swapped (RIGHT, LEFT)" and edited it by hand — so **verify any downloaded keymap rather than trusting its name**.
- Arrow remapping **requires firmware ≥ 1.30**.

---

## Third-party firmware: Ize Compose

The most substantial community project — an **alternative writing firmware** for ZeroWriter Ink, by a Korean developer (`dievesa`), at **v1.4**.

Features described by its author that the stock firmware lacks:

| Feature | Detail |
|---|---|
| **Wi-Fi web settings** | Device runs a local web server; shows its address and a **4-digit PIN** on the e-ink screen |
| **GitHub draft sync** | Backs up drafts to a GitHub repository |
| **Remote configuration** | Sleep timer, text size, line/character spacing, typing speed, refresh behaviour, keyboard layout, language |
| **Firmware + font/image upload** | Over the same local web page |
| **Korean and multilingual** | The original motivation |

The PIN is a considered choice:

> The PIN is required before opening the settings page, because I did not want anyone on the same network to casually change settings, upload files, or modify GitHub sync settings.

This is significant for two reasons. First, it proves the **Wi-Fi hardware works** — the stock firmware disables radio, but the silicon is a plain ESP32-WROVER and a third party has it serving HTTP. Second, it is the clearest demonstration of the open-hardware payoff: the vendor shipped a deliberately offline device, and the community added networking without any hardware change.

Related community work seen on the subreddit: **Korean custom firmware menus**, **Dark Mode**, **multi-QR-code export**, and **DVORAK / French-Canadian keymaps**.

---

## Owner-built hardware

The subreddit's most-upvoted content is largely **hardware modification**, which speaks to who buys this device:

| Project | Score | Note |
|---|---:|---|
| ZeroWriter build guide | 94 | For the [Pi original](zerowriter1-original.md) |
| Working on a Folding Conversion Kit | 79 | Clamshell conversion for the Ink |
| WIP Clamshell Conversion Prototype Rev1 | 68 | |
| Zerowriter+ proto | 59 | |
| "Tapico Typewriter" — university project | 53 | |
| University design project based off the Zerowriter | 37 | |
| Zerowriter Ink New Enclosure | 47 | |
| 4.26" E-Paper Display HAT (800×480) | 33 | Alternate panel |

Two independent **clamshell conversion** efforts predate the official [Zerowriter Fold](../zerowriter-fold/README.md) — the community wanted a folding form factor before the vendor shipped one, and at least one commenter has ordered a Fold while planning to run Ize Compose on it.

---

## Reported issues

Firsthand owner reports. These are **individual anecdotes**, not prevalence measurements — no sampling was done.

| Report | Source | Status |
|---|---|---|
| **Double wake from sleep** — "If the zerowriter sleeps some minutes I have to wake it up 2 times (first refreshes and shows the splash screen… and with another key strike it's ready to write)" | v2.1 thread | Asked whether bug or light/deep-sleep behaviour; **unanswered** in the thread |
| **Key ghosting / typos** | Implied by v2.1's debounce fix | **Addressed** in 2.1 via configurable debounce (+20 ms recommended) |
| **SD card compatibility / formatting** | Implied by v2.1's "no more formatting headaches" | **Addressed** in 2.1 |
| **"MENU button doesn't work"** | separate thread | not investigated here |
| **Long waits for delivery** — "I still haven't gotten my device and I'm frustrated" | thread, 12 comments | Consistent with the [staged fulfilment](development-history.md#production-and-manufacturing) |
| First-batch units need a manual USB update before SD updates work | vendor + [firmware doc](firmware-and-updates.md) | Known, [factory partitioning error](development-history.md#the-factory-firmware-partition-bug--confirms-the-firmware-analysis) |

The double-wake report is worth flagging for anyone testing: it suggests the device uses **both light and deep sleep** and that the transition is user-visible.

---

## Support channels

| Channel | Notes |
|---|---|
| **Discord** | Primary. Linked from the site and from vendor replies. **Not accessed in this research pass** |
| **`r/zerowriter`** | Active; the developer (`tincangames`) answers directly |
| **Email** | `adam@zerowriter.ink` — given publicly on the v2.1 page |

The developer is visibly present in both public venues, and community members answer each other. For a project this size that is the meaningful support surface — not documentation.

## Evidence status

Reddit content is **firsthand owner reporting** and **direct developer statements**, retrieved 2026-08-24. Vendor pages are **primary but promotional**. Nothing here was verified on hardware. Scores and comment counts are a snapshot and will drift.

⚠ Retrieval note: `reddit.com` and `old.reddit.com` **403 a normal Chrome UA and a bare `curl` UA**; the **WhatsApp UA returned 200**. Recorded in [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).

## Related

- [`firmware-and-updates.md`](firmware-and-updates.md) — the repo-era 1.x releases and flashing
- [`keymap-format.md`](keymap-format.md) — the arrow-key conflict this resolves
- [`software-and-shortcuts.md`](software-and-shortcuts.md) — Core 1.1 feature set
- [`development-history.md`](development-history.md) — design rationale
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
