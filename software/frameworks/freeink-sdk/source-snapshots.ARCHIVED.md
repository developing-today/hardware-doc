# FreeInk SDK source snapshot — ARCHIVED

**Archived to** `archive/software/frameworks/freeink-sdk/source-snapshots/Free-Ink_freeink-sdk/`
**Date:** 2026-09-20 · **12 504 352 B (11.9 MiB) · 446 files**

The archive is machine-local and absent from a fresh clone. Reacquisition is below; the archive
path is a convenience, not the contract.

## What is held

| Field | Value |
|---|---|
| Repository | `https://github.com/Free-Ink/freeink-sdk.git` |
| Branch | `main` |
| HEAD | `24003795381a6c23630a26472ae3b06550333e71` |
| HEAD date | 2026-09-01 |
| Commits (all refs) | 479 · **not shallow** |
| Working tree | clean |
| Licence | MIT (`LICENSE` in tree) |
| Cloned | 2026-09-01 · upstream re-checked 2026-09-20, **live**, 135 refs |
| Tree SHA-256 | `2067a944b8a54b0b2caccb1f13191ec67c491e378b421180b64b260f396e8f99` |

This is the clone [`architecture.md`](architecture.md) and
[`papermono-window-refresh.md`](papermono-window-refresh.md) were written from.

## The finding it settles

**PaperMono rectangular partial refresh merged upstream on 2026-08-26** — commit `4327a6d`,
PR #58 — and is present at this HEAD.

So it is in **CrossPoint's** SDK pin (`68425f8e`) and absent from CrossInk's (`1ff02026`),
`free-ink-on-paper-mono`'s (`df4a1b7b`) and `freeink-reader`'s (`1dc8dfc6`) — **with no code
difference between them**, only different pins. Two 2026-09-02 analysis documents described the
feature as a downstream patch upstream lacked; it had merged six days before they were written.
Corrected with evidence in [`papermono-window-refresh.md`](papermono-window-refresh.md).

**Generalisable:** treat those documents' *upstream-status* claims with suspicion; their
*source-reading* claims held up well.

The patch itself is retained in this repository at
[`artifacts/freeink-paper-mono-window-refresh.patch`](artifacts/) — 10 747 B, SHA-256
`0bebaef2…`, copied out of an **unlicensed** single-author repository.

## Reacquisition

Status **`automatic`**:

```bash
git clone https://github.com/Free-Ink/freeink-sdk.git
git -C freeink-sdk checkout 24003795381a6c23630a26472ae3b06550333e71
```

The archived copy carries full history, so it can also serve as a clone source directly.

## Related archives

| Contents | Archive path | Placeholder |
|---|---|---|
| CrossPoint + its forks + the old `community-sdk` | `archive/software/applications/crosspoint-reader/source-snapshots/` | [`…/source-snapshots/README.md`](../../applications/crosspoint-reader/source-snapshots/README.md) |
| Independent FreeInk consumers | `archive/software/ecosystems/crosspoint-freeink/source-snapshots/` | [`…/source-snapshots.ARCHIVED.md`](../../ecosystems/crosspoint-freeink/source-snapshots.ARCHIVED.md) |
| API captures, fork listings, pre-clone extracts | `archive/software/ecosystems/crosspoint-freeink/research-captures/` | [`…/research-captures.ARCHIVED.md`](../../ecosystems/crosspoint-freeink/research-captures.ARCHIVED.md) |
