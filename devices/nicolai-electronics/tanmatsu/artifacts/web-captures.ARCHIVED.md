# Raw web captures — ARCHIVED

**Archived to** `archive/devices/nicolai-electronics/tanmatsu/artifacts/web-captures/`
**Date:** 2026-09-20 · **60 files · 6 992 608 B (6.67 MiB)**

The archive is machine-local and absent from a fresh clone. Reacquisition notes are below; the
archive path is a convenience, not the contract.

## What is held

| Archived path | Files | Bytes | Captured | Extracted text in *this* repository |
|---|---:|---:|---|---|
| `web-captures/badge-team-html/` | 44 | 5 063 454 | 2026-08-26 | [`badge-team-docs/`](badge-team-docs/) — 44 `.txt` |
| `web-captures/solder-party-html/` | 7 | 368 967 | 2026-08-26 | [`solder-party-docs/`](solder-party-docs/) — 7 `.txt` |
| `web-captures/pricing/` | 8 | 1 505 636 | 2026-08-28 | none — mined into [`pricing-and-dimensions.md`](../pricing-and-dimensions.md) |
| `web-captures/appfs-page.html` | 1 | 54 551 | 2026-08-30 | none — mined into [`badgelink-and-appfs.md`](../badgelink-and-appfs.md) |

These are the **original HTML** behind the `.txt` files in this directory. The extraction is
lossy — `tools/htmltext.py` drops tables, image references, anchors and page metadata — so when
a badge.team claim turns out to be ambiguous, the HTML is where the answer is.

⚠ The badge.team pinout captures record the **published ESP32-P4 expansion "E-numbering" that
this project has shown to be wrong** ([`gaps-and-conflicts.md` §14](../gaps-and-conflicts.md),
confirmed from copper in [`konsool-zero-wiring.md`](../konsool-zero-wiring.md)). They are
evidence of the error, not authority.

All 60 files were validated as real HTML — `<!DOCTYPE html>` plus a non-empty `<title>`, no soft
404s. `appfs-page.html`'s title pins the version: `badgeteam/appfs • v2.1.0 - ESP Component Registry`.

## Reacquisition

**`manual`, and degrading.** These are live-rendered pages, not versioned documents; re-fetching
gives a *different* page, not the same bytes — which is why they were kept.

| Set | Pattern |
|---|---|
| badge.team | `https://docs.badge.team/<path>` — filenames mirror the URL with `_` for `/` |
| solder.party | `https://www.solder.party/docs/<name>/` |
| ESP registry | `https://components.espressif.com/components/badgeteam/appfs/versions/2.1.0` |
| Pricing | **URLs were not recorded per file.** Five are named by URL digest (`0be0c9`, `55d7a9`, `7ee69d`, `shop-a2f4c0`, `shop-d6b6f6`); identify them by opening them. Prices are dated **2026-08-28** and not re-checked — cite the date |

None was submitted to `web.archive.org/save/`. For the badge.team pinout pages that is worth
doing: they are the only public statement of a table shown here to be incorrect.

## Also moved in the same pass

`archive/devices/nicolai-electronics/tanmatsu/tools/scratch-scripts-duplicates/` — six analysis
scripts proven **byte-identical by SHA-256** to copies already tracked in
[`../tools/`](../tools/): `build_manifest.py`, `htmltext.py`, `p4_pinmap.py`,
`parse_ipc_netlist.py`, `verify_expansion_pinout.py`, `verify_manifest.py`. Use the repository
copies; the archived set exists only so the redundancy is documented rather than assumed.

Four scripts from the same source directory had **no** repository counterpart and were promoted
into this repository instead of archived: [`../tools/p4pins.py`](../tools/p4pins.py),
[`../tools/p4tab.py`](../tools/p4tab.py),
[`../tools/konsool_zero_pinmap.py`](../tools/konsool_zero_pinmap.py) and
[`../acquisition/archive-manifest-2026-09-20.json`](../acquisition/archive-manifest-2026-09-20.json).

## See also

- [`source-snapshots/upstream-clones.ARCHIVED.md`](source-snapshots/upstream-clones.ARCHIVED.md)
  — the 25 upstream git clones archived in the same pass
