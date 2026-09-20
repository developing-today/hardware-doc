# Calibre — e-book management for e-reader workflows

> The host-side half of getting books onto an ESP32 e-reader. Covers Calibre
> itself, its device-driver model, and the plugin landscape around CrossPoint,
> Libby/OverDrive and DRM.
>
> Snapshot **2026-09-04**. Repository facts are `executed-success` (GitHub API).
> **Nothing was installed, run or tested** — no Calibre instance and no e-reader
> in this project. Procedures are `reported-working`.

**Classification:** tooling — runs on your computer, not the device.

## Why it matters here

An ESP32 e-reader is a display for files you put on it. Calibre is how most
people convert, tag and transfer those files, and it is the point where three
separate problems meet: **format conversion**, **device transfer**, and **DRM**.
Each has different tooling and very different legal and maintenance risk.

## Installing Calibre

| Platform | Command | Notes |
|---|---|---|
| Debian / Ubuntu | `sudo apt install calibre` | Distribution builds lag upstream, sometimes by a lot |
| **Arch** | `sudo pacman -S calibre` | Well-maintained, close to upstream |
| **NixOS** | `environment.systemPackages = [ pkgs.calibre ];` | Declarative; see caveat below |
| Any Linux | `sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh \| sudo sh /dev/stdin` | Upstream's own installer — newest version, but installs outside the package manager |
| macOS | `brew install --cask calibre` | |
| Windows | `winget install calibre.calibre` | |

**NixOS caveat.** Calibre's plugin system writes into its configuration
directory, not the Nix store, so **plugins do work** — but any plugin that
expects to compile or vendor a native binary at install time may fail against the
store's read-only paths and missing FHS layout. Plugins that are pure Python are
fine. See [`guides/nixos`](../../../guides/nixos/README.md) for the general
pattern of dealing with this.

**Device access:** Calibre talks to USB mass-storage devices and to microSD cards
mounted normally — it does **not** need serial-port permissions. Serial access is
a flashing concern, not a Calibre one; see
[`guides/serial-access`](../../../guides/serial-access/README.md).

## How Calibre talks to devices

Two mechanisms, and the distinction matters for e-readers:

1. **Device drivers** — Python classes that recognise a device by USB VID/PID or
   by filesystem layout, then define where books go and what metadata is written.
   This is how "plug in Kindle, click Send to Device" works.
2. **Plain folder sync** — no driver; you copy files to a mounted SD card.

For ESP32 e-readers the second is the default: **there is no USB mass-storage
mode on most of these boards.** You take the microSD out, or you use the
firmware's web server. That is why the CrossPoint Calibre plugins exist —
they recognise a *CrossPoint-formatted SD card* rather than a USB device.

## The CrossPoint Calibre plugins

| Plugin | ★ | Licence | HEAD | Last push | What |
|---|---|---|---|---|---|
| [`crosspoint-reader/calibre-plugins`](https://github.com/crosspoint-reader/calibre-plugins) | **222** | **MIT** | `460c5308` | 2026-08-03 | **Official.** The one to use |
| [`ChristianVaughn/Crosspoint-Calibre-Plugin`](https://github.com/ChristianVaughn/Crosspoint-Calibre-Plugin) | 4 | GPL-3.0 | `f58c2c1b` | 2026-06-05 | Third-party; auto-recognises a CrossPoint SD card |
| [`yemM/crosspoint-reader-sd-calibre-plugins`](https://github.com/yemM/crosspoint-reader-sd-calibre-plugins) | 2 | **none** | `087d86da` | 2026-04-18 | Third-party device plugin for CrossPoint-formatted microSD (Xteink X4) |

The official plugin is actively maintained and MIT. The two third-party ones
solve the same problem at much lower star counts; `yemM`'s has **no licence
file**, so it is all-rights-reserved by default.

**Installing a Calibre plugin:** *Preferences → Plugins → Load plugin from file*,
pointing at the `.zip`. Calibre must be restarted. Plugins live in Calibre's
config directory (`~/.config/calibre/plugins` on Linux), not in the package.

## Libby / OverDrive

[`ping/libby-calibre-plugin`](https://github.com/ping/libby-calibre-plugin) —
★128, **GPL-3.0**, HEAD `1d115776`, **last push 2023-12-01**.

It integrates library loans from OverDrive's Libby service into Calibre: browse
loans, download, and manage holds without the Libby app.

**The maintenance状況 is the headline.** Last pushed **December 2023** — close to
three years stale at this snapshot. OverDrive's API and authentication are
vendor-controlled and change without notice, so a three-year-old client is a
substantial risk. Whether it currently works was **not tested here** and should
be verified before relying on it.

### What it can and cannot give you

This is where people's expectations break, so it is worth being precise:

- **EPUBs that Libby serves without DRM** — some publishers, and most public-domain
  titles — come through cleanly and can go straight to a device.
- **Most commercial library loans are DRM-protected**, typically Adobe ADEPT
  (`.acsm` fulfilment) or OverDrive's own scheme. **The Calibre plugin downloads
  the loan; it does not remove protection.** A protected file will not open on a
  **stock** CrossPoint reader — but see the correction immediately below: on the
  plugin firmware branch it **will**, via licensed ADEPT playback.
- **Audiobooks** are a separate pipeline and not relevant to an e-paper reader.

So "Libby → Calibre → e-reader" works end-to-end only for unprotected titles
unless a DRM step is inserted — which is the next section, and it is where the
legal picture changes.


> ⚠ **CORRECTION 2026-09-11 — the claim below that no CrossPoint firmware has a
> DRM client is WRONG.** The `feat-sd-plugins` branch carries
> `lib/Epub/ContentProtection.cpp`, which reads a `<book>.epub.rights` sidecar
> against a device credential at `/.crosspoint/content.key` and decrypts **at
> read time**, keeping the EPUB byte-identical on disk. Combined with the
> `protected-content` or `libby` plugins, a CrossPoint device is an
> **ADEPT-activated reader** and opens protected library loans directly.
> Full detail: [the Libby path](../../applications/crosspoint-reader/plugins/libby-path.md).
> The text below is retained for history.

## DRM tooling — status and honest framing

**DeDRM** is the well-known Calibre plugin for stripping e-book DRM.

| Repository | ★ | Licence | HEAD | Last push |
|---|---|---|---|---|
| [`apprenticeharper/DeDRM_tools`](https://github.com/apprenticeharper/DeDRM_tools) | **15,323** | none detected | `776f146c` | **2024-08-20** |
| [`noDRM/DeDRM_tools`](https://github.com/noDRM/DeDRM_tools) | 10,300 | none detected | `7379b453` | **2024-11-10** |

**Both are effectively dormant.** The original (`apprenticeharper`) has not been
pushed since August 2024; the active fork (`noDRM`) since November 2024. That is
roughly two years before this snapshot, during which Calibre has had multiple
major releases and Amazon has changed KFX handling more than once.

Neither repository has a detected licence, which for a redistributed Calibre
plugin is its own oddity.

**The legal position is jurisdiction-dependent and this record does not give
legal advice.** Circumventing technological protection measures is unlawful in
many jurisdictions (US DMCA §1201, EU InfoSoc Article 6) **regardless of whether
you own or have legally borrowed the content**, with narrow and varying
exceptions — accessibility and preservation among them in some countries. Some
jurisdictions permit personal-use format shifting; many do not.

What this knowledge base records, per its own method, is **metadata and
observable fact**: these tools exist, at these URLs, at these commits, in this
state of maintenance. It does not recommend a workflow, and "the maintainers
stopped in 2024" is the practically relevant fact independent of the legal one.

**Adobe ADEPT / `.acsm`.** A `.acsm` file is not a book — it is a fulfilment
token that Adobe Digital Editions exchanges for the actual EPUB. Handling it
requires an ADE authorisation. `libgourou` is the main open-source implementation.
Same legal caveats apply.

## What actually reaches an ESP32 e-reader

Setting DRM aside, the practical pipeline is:

```
source file (EPUB) → Calibre (convert / tag / cover)
                   → CrossPoint Calibre plugin  OR  manual copy
                   → microSD card  OR  firmware web server
                   → device
```

Format notes for CrossPoint-class firmware:

- **EPUB is the target format.** The [FreeInk SDK](../../frameworks/freeink-sdk/README.md)
  ships `FreeInkBook`, a full EPUB engine — streaming parse, CSS, UAX #14 line
  breaking with hyphenation.
- **Simplify before transferring.** Heavy CSS, embedded fonts and large images
  cost parse time and RAM on a device where the ESP32-C3 sets the memory ceiling.
  `uxjulia/auto-epub-optimizer` exists specifically for this.
- **Fonts and hyphenation dictionaries are device-side**, not embedded per book —
  see `crosspoint-reader/crosspoint-fonts` and upstream's `docs/sd-card-fonts.md`.

## Related tooling

| Tool | ★ | Licence | HEAD | What |
|---|---|---|---|---|
| [`shakogegia/xtlibre`](https://github.com/shakogegia/xtlibre) | 81 | MIT | `9d2c47a3` | Self-hosted companion app for Xteink and CrossPoint readers |
| [`crosspoint-reader/crosspoint-sync`](https://github.com/crosspoint-reader/crosspoint-sync) | 42 | MIT | `a986b3ce` | Lightweight **KoSync** server — syncs reading progress and stats across devices |
| `uxjulia/auto-epub-optimizer` | 25 | — | — | Pre-processes EPUBs for constrained readers |

`crosspoint-sync` implementing **KoSync** is worth noting: that is KOReader's
sync protocol, so the ecosystem deliberately reuses an existing standard rather
than inventing one.

## Sources

All retrieved **2026-09-04** from the GitHub REST API, authenticated:
repository metadata and HEAD commit for each repository named above. Commit SHAs
are given at first mention and are the identity to cite — branch names move.

## Open questions

- **Nothing was installed or tested.** Whether the Libby plugin still functions
  against OverDrive's current API is unknown and is the most consequential
  unknown here.
- The official CrossPoint Calibre plugin's actual capabilities were read from its
  description, not its source.
- **`ruqqq/crosspoint-plugins`** (the on-device plugin store) is a *different
  thing* from Calibre plugins and is covered separately — see
  [the CrossPoint plugin systems record](../../applications/crosspoint-reader/plugins/README.md).
- No format-conversion benchmark or file-size guidance is measured here.
