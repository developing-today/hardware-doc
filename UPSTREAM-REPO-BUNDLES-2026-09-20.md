# Upstream repository bundles — 2026-09-20

The archive held **81 nested git repositories** — upstream clones gathered as evidence by earlier
passes. None of them was under version control, and none could be, for a reason that is worth
stating plainly because it fails silently.

**A directory containing `.git` cannot be committed to a parent repository.** Git converts it to a
gitlink (mode `160000`) with no `.gitmodules` entry and no remote recorded. A clone of the parent
then yields an empty directory, and nothing reports an error. Running `git add -A` across the
archive would have committed 1.8 GB while discarding 3.7 GB — including 1.9 GB of ordinary files
that have nothing to do with git history — in a commit that looked complete.

Each repository is therefore preserved as a **single-file git bundle** in
[`archive/hardware-doc/_repo-bundles/`](archive/hardware-doc/_repo-bundles/README.md), and every
source directory is listed in `repo-archive/.gitignore` so none can become a gitlink. Embedded-repo
warnings went from 80 to 0.

**81 bundles, 1.97 GB. 11,523 files and 13,129 commits restore.**

## Restoring one

```bash
git clone archive/hardware-doc/_repo-bundles/<owner>__<repo>.bundle <dir>
```

That yields the full repository: all refs, all history, working tree at HEAD. The clone lands on
an ignored path, so the arrangement does not degrade on the next `git add`.

## `git bundle verify` does not mean the bundle works

This cost the most to learn and is the one thing to carry forward.

A bundle built from a **shallow** clone passes `git bundle verify` cleanly and then fails to clone
with `fatal: remote did not send all necessary objects`. Twenty bundles were originally built from
shallow clones; **nineteen verified and nineteen could not be restored.** `git bundle create --all`
on a shallow repository also succeeds without warning, so no step in the chain reports a problem.

All twenty sources were unshallowed from their live upstreams and rebundled. The recoveries were
not marginal:

| Repository | Before | After |
|---|---:|---:|
| `MingRZou/PaperMono-Launcher` | 1 commit | **817** |
| `uxjulia/CrossInk` | 3,181 | **3,739** |
| `m5stack/M5Unified` | 1 | **780** |
| `Xinyuan-LilyGO/T-Display-K230` | 1 | **377** |
| `crosspoint-reader/crosspoint-simulator` | 1 | **145** |

No shallow bundles remain, and **all 81 were tested by actual `git clone`**, not by verification.
If you add a bundle, clone-test it.

## Risk tiers

Four factors, each an independent route to a repository becoming unrecoverable: **zero forks** (no
independent copy exists on GitHub's infrastructure), **fewer than ten stars**, **no licence** (no
mirror or package manager will carry it), and a **personal rather than organisational account**.
Three or more → HIGH, two → MED, at most one → LOW. Upstream already 404 → CRITICAL.

| Tier | Repos | Size | Meaning |
|---|---:|---:|---|
| CRITICAL | 1 | 252 MB | upstream gone; this is the only copy |
| HIGH | 30 | 405 MB | no fork, no licence, personal account |
| MED | 12 | 158 MB | vendor-owned but thinly mirrored |
| LOW | 37 | 1.19 GB | well-mirrored; re-clonable |

The tier boundary is recorded in the bundle manifest, so dropping LOW later is a one-line
`.gitignore` change rather than a restructuring.

### The CRITICAL one

**`ideo2004-afk/crosspoint-reader-lua` returns 404.** Software Heritage never crawled it; because
there is nothing left to fetch, it can never be submitted — Save Code Now requires a live origin.
No fork existed. The bundle holds **784 commits across 59 refs**, and cloning it restores 934
files. It is the only copy known to exist.

## Submodules are not included in bundles

`git bundle --all` records a submodule as a gitlink and **omits its objects**. Submodules also
carry `.git` as a *file*, not a directory, so a `find -name .git -type d` scan does not see them.

Of **21 declared submodules, 5 are populated** and all 5 are covered — four are
`Free-Ink/freeink-sdk`, whose gitlink commits were each verified present inside the existing
`freeink-sdk` bundle, and the fifth is `open-x4-sdk` inside the CRITICAL repository, bundled
separately.

The other **16 were never initialised**. They hold no content here and never did, which is not the
same as being preserved. Seven are declared in `.gitmodules` but absent from the parent's HEAD
tree, so no gitlink exists to recover. One real gap is recorded rather than smoothed over:
`mekhontsev/crosspoint-reader`'s reference to `freeink-sdk` (`cb9167d5`) is **not** present in the
`freeink-sdk` bundle held here. All uncovered upstreams were alive when checked.

## Uncommitted working-tree state

Bundles preserve **committed history only**. Scanning all 80 repos found six with uncommitted
state; four fragments exist in no git object and are kept in
[`_repo-bundles/local-state/`](archive/hardware-doc/_repo-bundles/local-state/README.md) — notably
a 70-line `platformio.ini` pinning `JPEGDEC` to a specific commit, and a local patch to
`JPEGDEC`'s `src/jpeg.inl`.

## Software Heritage

Checked 2026-09-20: **65 of the 69 upstreams are absent from Software Heritage**, and the four
present are all LOW tier. It is not currently a safety net for this material. Submission is
programmatic and anonymous —
`POST https://archive.softwareheritage.org/api/1/origin/save/git/url/<url>/` — but capped at
**10 requests per hour**. Ten are queued; 28 remain.

## Two false artifacts produced while doing this

Both are recorded because each verified clean and looked correct.

**A 1.3 GB bundle of the wrong repository.**
`upstream-clones/konsool-expansion-template/` holds a `.git` with `config`, `HEAD`, `hooks` and
`info` but **no `objects/` and no `refs/`** — an aborted clone. Git does not recognise it as a
repository, so `git -C` there silently resolves to the *parent*, and the bundling run produced a
1.3 GB file that was the whole of `repo-archive` under a Tanmatsu part name. All 81 were audited
for the same defect: one affected, eighty clean. No upstream by that name exists.

**Seven datasheets "found" that were already filed.**
`badgeteam/konsool-zero` has seven PDFs deleted from its working tree. They were reported as
existing nowhere else in the archive, on the strength of a search written
`find . -type f -name '*.pdf' -o -name '*.PDF'` — where `-o` breaks the `-type f` binding and the
precedence silently returns the wrong set. Re-run correctly across 619 PDFs, **all seven matched
documents already filed** under proper component names covering ST25R3916, CC1101, STM32WB55 and
three WCH CH32 parts.

## Relationship to the scratch relocation

[`SCRATCH-RELOCATION-2026-09-20.md`](SCRATCH-RELOCATION-2026-09-20.md) describes the move of
`scratch/` into the archive on the same day. That move completed on disk but was never committed:
4,370 tracked deletions and 5.5 GB untracked were left in the archive's working tree. Nothing was
lost — the deletions remained recoverable from `HEAD`, and sampled files were confirmed
content-identical at their destinations by hash — but the archive's git did not describe the
archive. The nested repositories were the blocker, which is why both are resolved together.
