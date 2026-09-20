# ZeroWriter Ink — sources

Retrieved **2026-08-24**. `Class`: primary / community / press.

| ID | Title | Publisher | Class | Medium | URL | Establishes | Status |
|---|---|---|---|---|---|---|---|
| ZW-1 | Zerowriter Ink campaign | Crowd Supply | primary | campaign page | <https://www.crowdsupply.com/zerowriter/zerowriter-ink> | Specs, price ($285), funding (2024-10-17, 585 backers, $147,538), Inkplate 5 collaboration, comparison table | **Live** |
| ZW-2 | `zerowriter/zerowriter_ink` | Zerowriter | primary | repository | <https://github.com/zerowriter/zerowriter_ink> | KiCad design files, firmware releases, fonts, enclosure STLs. GPL-3.0, commit `996207ac` (2026-05-13) | **Live**, preserved |
| ZW-3 | `zerowriter/zerowriter1` | Zerowriter | primary | repository | <https://github.com/zerowriter/zerowriter1> | The original Raspberry Pi Zero project. MIT, commit `e476d056` (2026-05-19) | **Live**, preserved |
| ZW-4 | zerowriter.com | Zerowriter | primary | website | <https://zerowriter.com> | — | **DEAD** — domain parked for sale ($7,500, Spaceship.com) |
| ZW-5 | Zerowriter Discord | Zerowriter | community | chat | <https://discord.gg/57yANTWGet> | Support, community builds | Live, not accessed |
| ZW-6 | Zerowriter YouTube | Zerowriter | primary | video | <https://www.youtube.com/@ZeroWriter> | Demos | Live, not reviewed |
| ZW-7 | Tom's Hardware coverage | Tom's Hardware | press | article | <https://www.tomshardware.com/raspberry-pi/zerowriter-ink-typewriter-sequel-comes-with-larger-52-inch-eink-screen-all-week-battery-and-mechanical-keyboard> | Independent writeup | Live |
| ZW-8 | Liliputing coverage | Liliputing | press | article | <https://liliputing.com/zerowriter-ink-is-an-open-source-word-processor-with-an-e-ink-display-and-a-mechanical-keyboard-crowdfunding/> | | Live |
| ZW-9 | Boing Boing coverage | Boing Boing | press | article | <https://boingboing.net/2026/02/02/zerowriter.html> | | Live |
| ZW-10 | Yanko Design coverage | Yanko Design | press | article | <https://www.yankodesign.com/2026/02/04/zerowriter-ink-is-an-open-source-e-paper-typewriter-built-for-writers/> | | Live |
| ZW-11 | Notebookcheck (DE) | Notebookcheck | press | article | <https://www.notebookcheck.com/Zerowriter-Ink-Offenes-System-bringt-einen-E-Ink-Bildschirm-und-eine-mechanische-Tastatur-fuer-Texterstellung-mit.868781.0.html> | German-language coverage | Live |
| ZW-12 | CircuitDigest | CircuitDigest | press | article | <https://circuitdigest.com/news/zerowriter-ink-an-open-source-epaper-typewriter-for-writers> | | Live |
| ZW-13 | TechEBlog | TechEBlog | press | article | <https://www.techeblog.com/zerowriter-ink-typewriter-e-ink/> | | Live |
| ZW-14 | Good e-Reader | Good e-Reader | press | article | <https://goodereader.com/blog/technology/zerowriter-ink-e-paper-typewriter-crowd-funding-campaign-to-start-soon> | | Live |
| ZW-15 | e-ink-info | e-ink-info | press | article | <https://www.e-ink-info.com/zerowriter-ink> | | Live |
| ZW-16 | Pascal Forget | pascalforget.com | community | blog | <https://www.pascalforget.com/zerowriter-ink/> | Owner/reviewer perspective (French) | Live, not reviewed |
| ZW-17 | ereaderpro coverage | ereaderpro.co.uk | press | article | <https://www.ereaderpro.co.uk/en/blogs/news/e-ink-new-product-the-e-ink-typewriter-focused-on-writing-zerowriter-ink-is-coming-soon-to-crowdfunding-platforms> | | Live |
| ZW-18 | Crowd Supply campaign updates (17) | Zerowriter / Crowd Supply | primary | campaign updates | <https://www.crowdsupply.com/zerowriter/zerowriter-ink/updates> | **Design rationale**: e-paper 200→100 ms optimisation, why the keyboard uses an ESP32, staged open-source plan, factory partition bug, ~600-unit first run, enclosure redesign, tariffs | **Live**, all 17 preserved at [`artifacts/crowdsupply-updates/`](artifacts/crowdsupply-updates/) |
| ZW-19 | Zerowriter Ink v2.1 release | Zerowriter | primary | release notes | <https://zerowriter.ink/pages/zerowriter-ink-2-0-early-access> | **Current firmware (July 2026)**; SD engine, debounce, accents, HD internal storage, coin-cell requirement | **Live**, preserved |
| ZW-20 | Zerowriter Ink User Guide | Zerowriter | primary | manual | <https://zerowriter.ink/pages/zerowriter-ink-user-guide> | Updated user guide for 2.1 | Live, preserved |
| ZW-21 | Shortcut Keys Reference | Zerowriter | primary | blog | <https://zerowriter.ink/blogs/news/shortcut-keys-reference> | Complete keyboard shortcut list | Live, preserved |
| ZW-22 | Zerowriter Core 1.1 Update | Zerowriter | primary | blog | <https://zerowriter.ink/blogs/news/zerowriter-core-1-1-update> | Core is the Ink's software; folders, Save-As, hotswap slots | Live, preserved |
| ZW-23 | Zerowriter Ink Is Shipping | Zerowriter | primary | blog | <https://zerowriter.ink/blogs/news/zerowriter-ink-is-shipping> | Direct orders shipped 2025-10-10 | Live, preserved |
| ZW-24 | `r/zerowriter` | community | community | forum | <https://www.reddit.com/r/zerowriter/> | **Arrow-key conflict resolved by the developer**; Ize Compose third-party firmware; owner reports (double-wake, key ghosting, SD compatibility); clamshell conversions | Live. ⚠ 403s Chrome/curl; **WhatsApp UA returns 200** |
| ZW-25 | Zerowriter Fold Kickstarter | Zerowriter | primary | campaign | <https://www.kickstarter.com/projects/zerowriter/zerowriter-fold> | Fold funding and specs | ⚠ **403 to every UA tried.** Wayback snapshot `20260824205508` exists; IA returned 503 during this pass — **retrievable later** |

## Notes on evidence

- **The architectural findings in [`README.md`](README.md) — the dual-ESP32 design and the Inkplate respin — come from ZW-2's KiCad BOMs**, not from any prose source. No press article and no vendor page mentions either.
- Press coverage (ZW-7 … ZW-17) is uniformly derived from the campaign page and contains no independent technical measurement. It establishes that the product was announced and received attention; it does not corroborate any specification.
- **All 17 Crowd Supply updates were read and mined** (ZW-18) — they proved to be the best source of design rationale, and are distilled in [`development-history.md`](development-history.md). Raw HTML preserved in-tree.
- **`zerowriter.ink` is the authoritative source for firmware**, the GitHub repo for hardware. The repo's firmware is two major versions stale.
