# Zerowriter — vendor documentation guide

> Established **2026-08-24** while researching [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md).

**Zerowriter** — Adam Wilk, Ottawa, Canada. Open-source e-paper writing devices. Two products: **Zerowriter Ink** (Crowd Supply, 2024) and **Zerowriter Fold** (Kickstarter, later).

## The domain trap

| Domain | Reality |
|---|---|
| **`zerowriter.ink`** | ✅ **The actual site.** Shopify-hosted store + docs + web flasher |
| `zerowriter.com` | ❌ **Parked, for sale** ($7,500 via Spaceship.com). Not the project |

The Crowd Supply campaign and much press coverage point at `.com`. It is easy to conclude the project is abandoned. It is not.

**How I found the real domain:** a URL inside `firmware_releases/updates-readme.txt` in the GitHub repo. When a vendor's website appears dead, **grep the repository for the domain** — release notes, installers and READMEs frequently carry it.

## ⚠ Chrome user agent is blocked; ClaudeBot is not

`zerowriter.ink` sits behind a filter that **403s a standard desktop Chrome UA** on most pages while serving the site root fine — a confusing partial block.

| User agent | Result |
|---|---|
| `Mozilla/5.0 … Chrome/131.0.0.0 Safari/537.36` | **403** on `/pages/*`, `/products/*` |
| `Mozilla/5.0 … ClaudeBot/1.0; +claudebot@anthropic.com` | **200** ✅ |

Per the repo's [web-retrieval fallback policy](../../AGENTS.md), rotating the UA is appropriate here: this is public marketing/documentation content, no authentication or access control is being bypassed, and the alternate UA is honestly identified. Recorded in `ai-crawler-site-access-table.md`.

Note the site root returns 200 to Chrome, so a naive reachability check passes while every documentation page fails.

## Where the content is

| What | Where |
|---|---|
| Firmware updates, **web flasher**, recovery procedure | <https://zerowriter.ink/pages/firmware-updates> |
| News / release announcements | <https://zerowriter.ink/blogs/news> |
| Zerowriter Fold | <https://zerowriter.ink/pages/zerowriter-fold> |
| Hardware design (KiCad), keyboard firmware, firmware binaries, fonts, enclosure STLs | <https://github.com/zerowriter/zerowriter_ink> (GPL-3.0) |
| Original Raspberry Pi project | <https://github.com/zerowriter/zerowriter1> (MIT) |
| Support — Discord | <https://discord.gg/57yANTWGet> |
| Support — **Reddit** | <https://www.reddit.com/r/zerowriter/> |

Several page slugs guessed from navigation (`/pages/welcome-guide`, `/pages/updates-tools`, `/pages/web-flasher`, `/products/zerowriter-ink`) return **404** — it is a Shopify store, so real product URLs are under `/products/<handle>` with handles not guessable from menu labels. Fetch the site root and extract links rather than constructing them.

## What is and is not open

Worth stating plainly, because the project markets itself as open source:

| Component | Published? | Licence |
|---|---|---|
| Hardware design (main board, keyboard, breakout) | ✅ KiCad sources | GPL-3.0 repo |
| Enclosure | ✅ STL | GPL-3.0 repo |
| **Keyboard firmware** | ✅ full Arduino source | GPL-3.0 |
| **Main application firmware** | ❌ **binaries only** | — |
| Breakout board | ⚠ gerbers only, no schematic | — |

The writing application — the actual product — is **not** in the repository as source. See [`zerowriter-ink/gaps-and-conflicts.md`](../../devices/zerowriter/zerowriter-ink/gaps-and-conflicts.md).

## Repository layout

```
zerowriter_ink/
├── design/src/<board>/v<ver>/CAD/      KiCad (Soldered's template — see the Soldered vendor guide)
├── design/src/<board>/v<ver>/OUTPUTS/  BOM .csv, schematic PDF, iBOM .html, 3D .step
├── design/enclosure/                   STL
├── firmware_releases/SD-<ver>/         firmware.bin + readme.txt (changelog)
├── firmware_releases/archived updates/ older releases
├── firmware_releases/command line/     merged full-flash image + howto.txt
├── src/keyboard/<name>/                keyboard .ino
├── compiled fonts/                     .bbf
└── utils/                              Ink_Keymap_Editor.html, USB_Send.html, keymaps/
```

Because the boards were designed with Soldered, the KiCad projects carry Soldered's title block and footprint libraries — **the [Soldered vendor guide](../soldered-electronics/README.md) applies to parsing them**, including the mixed CSV-delimiter trap (Soldered exports use `;`, ZeroWriter's use `,`).

## Related

- [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md)
- [Soldered Electronics vendor guide](../soldered-electronics/README.md)
