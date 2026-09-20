# The CrossPoint / FreeInk fork network

> How ~1,600 forks of one e-reader firmware actually relate, how far each has
> diverged, and which divergences could be patches instead of forks.
>
> Snapshot **2026-09-04**. All figures from the GitHub API (`executed-success`
> for retrieval). Nothing was built or run — no hardware. Divergence
> interpretation is `inferred`.

Records: [CrossPoint Reader](../../applications/crosspoint-reader/README.md) ·
[FreeInk SDK](../../frameworks/freeink-sdk/README.md) ·
[CrossPlay](../../applications/crossplay/README.md)

## The shape of it

```
open-x4-epaper/community-sdk          MIT, CidVonHighwind et al.
        │ code derived, re-architected
        ▼
Free-Ink/freeink-sdk                  ★248 · 95 forks · created 2026-06-03
        │ git submodule
        ▼
crosspoint-reader/crosspoint-reader   ★7,538 · 1,621 forks · created 2025-12-03
        ├── uxjulia/CrossInk          ★1,451 · true fork · itself heavily forked
        │       └── CrumBLE, InkPointX, YACP, casper, CrossPlant, CrossDiTo …
        ├── yattsu/biscuit            ★463 · true fork · stale
        ├── trilwu/crosspet           ★216
        ├── 0x1abin/crossmux          ★164 · true fork
        ├── ma-r-s/crossplay          ★17  · true fork · games
        └── MarsTechHAN/crosspoint-reader-mono  ★1 · true fork · PaperMono port
```

Note the inversion at the top: **CrossPoint predates its own SDK by six months.**
FreeInk is a later re-architecture of the SDK CrossPoint was already using, not an
upstream CrossPoint adopted.

## Finding 1 — most "forks" are not forks

Of fourteen named, actively-discussed derivatives, **only five are GitHub forks**
(`fork: true` with a `parent`). The other nine were re-uploaded as fresh
repositories and are **detached**: `fork: false`, `parent: null`.

| Repository | ★ | GitHub fork? | Pushed |
|---|---|---|---|
| `uxjulia/CrossInk` | 1,451 | **yes** → crosspoint-reader | 2026-09-03 |
| `yattsu/biscuit` | 463 | **yes** | 2026-04-08 |
| `0x1abin/crossmux` | 164 | **yes** | 2026-09-04 |
| `ma-r-s/crossplay` | 17 | **yes** | 2026-09-04 |
| `MarsTechHAN/crosspoint-reader-mono` | 1 | **yes** | 2026-08-12 |
| `imshentastic/CrumBLE` | 88 | **no — detached** | 2026-08-07 |
| `aBER0724/crosspoint-reader-cjk` | 75 | **no — detached** | 2026-09-04 |
| `yokki-vans/InkPointX` | 74 | **no — detached** | 2026-08-30 |
| `juicecultus/crosspoint-reader-papers3` | 67 | **no — detached** | 2026-05-23 |
| `Sichroteph/YACP` | 59 | **no — detached** | 2026-09-03 |
| `tweakerinc/casper` | 25 | **no — detached** | 2026-09-03 |
| `0xKnowles/CrossPlant` | 7 | **no — detached** | 2026-07-25 |
| `dito94/CrossDiTo` | 5 | **no — detached** | 2026-08-21 |
| `samfoy/CrossInk` | 1 | **no — detached** | 2026-08-24 |

**Two consequences, pulling in opposite directions:**

- GitHub's `/forks` listing **undercounts** the meaningful network — none of the
  nine detached repositories appear in it, including CrumBLE and the CJK port,
  which would rank in the top ten by stars.
- The `1,621` figure simultaneously **overcounts**, because the overwhelming
  majority of GitHub forks of any popular repository carry zero commits.

So "1,621 forks" is close to meaningless in both directions. **Enumerate by name,
not by API listing.** Anyone measuring this ecosystem from `/forks` alone will get
the wrong answer twice over.

Detachment also destroys the `ahead_by`/`behind_by` relationship — there is no
shared history to compare against — which is why several rows below are blank.

## Finding 2 — three distinct divergence patterns

Comparing each true fork against upstream `develop`, the additions-to-deletions
ratio separates them cleanly.

| Fork | Ahead | Behind | Pattern |
|---|---|---|---|
| `ma-r-s/crossplay` | **+2,610** | −2 | **Additive** |
| `0x1abin/crossmux` | +559 | −4 | **Additive** |
| `uxjulia/CrossInk` | +616 | −285 | **Divergent** |
| `trilwu/crosspet` | +309 | −536 | **Divergent + drifting** |
| `yattsu/biscuit` | +52 | **−603** | **Stale** |

**Additive** — thousands of commits ahead, almost nothing behind, and crucially
**near-zero deletions**. New code lives in new files; upstream is merged
continuously. CrossPlay is the textbook case: it is 2,610 commits ahead with
**two** commits behind, and its measured diff was ~18,000 additions against ~860
deletions. That is not a divergent codebase; it is upstream plus a large
additive tree.

**Divergent** — substantial deletions mean upstream-owned code was rewritten or
removed. CrossInk at +616/−285 is a genuine second codebase, which is consistent
with it being the only derivative that has itself become a fork parent.

**Stale** — `biscuit` is the cautionary tale and worth naming. It is the
**second-most-starred fork in the ecosystem** (463★), sits **603 commits behind**
upstream, and has not been pushed since **2026-04-08**, five months before this
snapshot. Star count is a popularity signal, not a maintenance signal, and here
the two have completely decoupled.

## Finding 3 — `behind_by` is a safety metric here, not tidiness

In most ecosystems being behind upstream is a hygiene issue. In this one it is a
**brick-risk signal**, for a specific reason: the target hardware is revised
silently. Prior research in this project recorded two X3 variants and three X4 Pro
variants appearing since July 2026 with no external versioning, and upstream
carries the fixes as they are discovered.

A fork 600 commits behind is therefore not merely missing features — it may be
missing a panel-init change for a board revision the user actually owns. Combined
with these devices' flashing risk (upstream ships a dedicated
`docs/fix-bricked-xteink.md`), **currency matters more here than the star counts
suggest**.

This also cuts against detached forks specifically: without shared history there
is no cheap way to even measure how far behind they are, and no `git merge` path
to catch up.

## Finding 4 — the fork network is upstream's stated design

`SCOPE.md` in upstream contains this acceptance test for contributions:

> **Is another popular CrossPoint fork already solving this well?** If yes, we
> generally defer to that fork if it's not part of the core reading experience.
> e.g. stats

Upstream **deliberately delegates non-core features to its fork network** rather
than absorbing them. The fork count is the governance model working, not
fragmentation.

CrossPlay states the downstream half of the same bargain in `LOCAL_SCOPE.md`:
*"Reading stays the primary purpose… the reading experience is upstream's to own.
We do not fork it, improve it, or diverge from it. Anything that makes reading
better belongs upstream, so send it there."*

That is a healthier arrangement than it looks from the raw fork number, and it
explains the additive divergence pattern: forks that only add features have no
reason to touch upstream code.

## Finding 5 — patch portability, worked

The interesting question is whether a fork's changes *need* to be a fork.
CrossPlay is the only derivative that documents its own answer, so it is the one
case that can be assessed rather than guessed. From its `LOCAL_SCOPE.md`:

**28 upstream files touched**, of which roughly half are identity (README,
LICENSE, workflows, templates) and ~15 are genuine code seams.

| Class | Examples | Portability |
|---|---|---|
| **Append-only** | Two values appended to a `UIIcon` enum; two switch cases; 3 `.gitignore` lines; one `platformio.ini` include | **Trivial.** Appending to an enum preserves every value below it; a new switch case is a pure addition. These merge indefinitely |
| **Bug fixes that belong upstream** | Thick-line direction fix in `GfxRenderer`; `openFileForAppend()` (upstream's write carries `O_TRUNC`, so nothing could append); `…FitWithin()` contain-vs-cover; `getScreenSafeArea()` bezel insets | **Should be PRs.** The bezel-inset one is a *correctness* issue affecting stock upstream on bezelled devices — upstream screens draw under the glass without it |
| **Genuinely conflict-prone** | `HomeActivity.{cpp,h}` — 4 hooks plus a method in a file upstream actively develops | **The one real seam.** Mitigated by appending after upstream's rows so indices never shift |
| **Cannot be upstreamed** | OTA release URL (pointing at upstream would flash a C3 image onto an S3); identity files | Inherent to forking |

**Verdict for CrossPlay: ~90 % new files plus about a dozen small, mostly
append-only seams.** It is far closer to "a patch series plus a large additive
tree" than to a divergent codebase — and four of its seams arguably belong
upstream, where both projects would benefit.

**Whether this generalises is unknown.** CrossPlay is the only fork in the network
that maintains an explicit seam inventory. The others were not analysed at file
level in this pass, and the deletion counts above suggest CrossInk and crosspet at
least are materially more invasive.

## Finding 6 — forks of the SDK, not just the firmware

CrossPlay's `.gitmodules` pins **`ma-r-s/freeink-sdk`** branch
`x4pro-measured-insets`, not `Free-Ink/freeink-sdk`. Prior research recorded
CrossInk pinning a different, older SDK commit.

So a downstream project can have **two upstreams**, and — importantly —
**a fork's behaviour can differ from upstream's without a single line of
fork-owned code differing**, because the SDK underneath is a different revision.
Any divergence analysis that reads only the firmware repository will miss this.

FreeInk itself has 95 forks against 248 stars — a ~38 % ratio, far higher than
CrossPoint's ~21 %, which is what an SDK meant to be embedded and adapted should
look like.

## Finding 7 — no licence fragmentation

**All fourteen named derivatives are MIT**, matching upstream and the SDK. For an
ecosystem this large and this informally governed, that is unusual and worth
noting: there is no copyleft boundary anywhere in the graph, and code can move
between forks and upstream freely.

The exception is outside the fork network: `MagicCube/free-ink-on-paper-mono`, a
FreeInk demo on the M5Stack PaperMono, has **no LICENSE file at all** and is
therefore all-rights-reserved by default. See the
[examples catalogue](../../../devices/m5stack/papermono/examples/best.md).

## Relevance to the M5Stack PaperMono

- **Upstream CrossPoint ships `[env:papermono]`** build environments — PaperMono
  support is not fork-only.
- **`MarsTechHAN/crosspoint-reader-mono`** is a true fork and the origin of the
  `crosspoint-paper-mono-cjk` binary held in the
  [PaperMono record's artifacts](../../../devices/m5stack/papermono/factory-firmware.md).
- **CrossPlay carries `papermono` envs**, but its own scope document names only
  the X4 Pro and reTerminal Sticky as targets, and nobody has reported running it
  on a PaperMono.
- **A plugin could not add NFC or LoRa.** Per carried-over analysis, the plugin
  system runs browser JavaScript with no MCU-side execution and no peripheral
  access — radios need a fork or an upstream feature. *Flagged for
  re-verification; not confirmed in this pass.*

## Method and limits

Fork identity, stars, licences and push dates: GitHub REST API, 2026-09-04,
authenticated. Divergence: `GET /repos/{upstream}/compare/develop...{owner}:{repo}:{branch}`.

**Known limits:**

- The compare endpoint **caps its file list at 300**, so per-file totals for large
  forks are floors, not totals.
- `sort=stargazers` on `/forks` is **unstable under pagination** — a prior pass
  returned 1,421 rows containing only 1,001 unique repositories. Use `sort=oldest`.
- Detached forks cannot be compared at all.
- Only CrossPlay's changes were examined at file level; the other classifications
  rest on aggregate add/delete ratios, which is weaker evidence.
- Star and fork counts moved measurably *during* this research window
  (CrossPoint 7,488 → 7,538; CrossInk 1,431 → 1,451). Figures are a snapshot, not
  a constant.
