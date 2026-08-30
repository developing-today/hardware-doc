# AGENTS.md — hardware-doc

This repository is the **hardware research knowledge base**. It is a standalone repo
(`developing-today/hardware-doc`) that is normally checked out **beside** the repo that
consumes it, and symlinked into place from there.

```
<repo-parent>/
├── code/                     ← consuming repo (config, infra, …)
│   └── the repository root  ──────┐   symlink
├── hardware-doc/     ←─────┘   THIS REPO
└── repo-archive/       bulk artifacts moved out of this repo (separate repo, usually unpublished)
```

## Paths — always resolve, never hardcode

Two sibling directories matter, and both are located **relative to the real repository
root**, not the working directory and not `~`.

| What | Location |
|---|---|
| This repo | `<repo-parent>/hardware-doc` |
| Bulk artifact archive | `<repo-parent>/repo-archive` |

The archive is **its own git repository**, typically **unpublished/private** because of its
size (multiple GB). It is not a submodule of this repo and is not required — every archived
artifact leaves a placeholder here carrying hashes and recovery URLs.

**Resolve the real root with the git *common* directory**, which is worktree-safe:

```bash
ROOT="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
PARENT="$(dirname "$ROOT")"
ARCHIVE="$PARENT/repo-archive"
```

`--git-common-dir` matters: inside a linked worktree, `--git-dir` points at
`.git/worktrees/<name>` while `--git-common-dir` still points at the main `.git`. Using
`--show-toplevel` would give you the *worktree* root, which is the wrong parent.

Historically the archive was referred to as `../repo-archive`. That happens to be
correct when the repo lives at `~/hardware-doc`, but it is wrong under worktrees and on
any machine with a different layout. **Write `../repo-archive` relative to the
repo root, or resolve it with the command above.**

## Symlinks and `--skip-worktree`

Two symlinks are **tracked**, both committed in **relative** form:

| Link | Committed target | Points at |
|---|---|---|
| `archive` (this repo) | `../repo-archive` | the bulk-artifact archive |
| `doc/hardware` (consuming repo) | `../../hardware-doc` | this repo |

Relative is right for the normal sibling layout and keeps every clone identical to
`HEAD`. It breaks only where `../..` does not reach the target — most often a linked
worktree parked outside the repo parent. There, `hardware-doc-init.sh` substitutes an
**absolute** path derived from the git common dir.

Substituting makes the worktree differ from `HEAD`, so the script then marks the path
`--skip-worktree`.

> **`.gitignore` cannot do this.** It applies only to *untracked* paths. A tracked file
> keeps reporting modifications no matter what `.gitignore` says. `--skip-worktree` is the
> only thing that suppresses it. The `archive/*` and `doc/hardware/*` ignore entries exist
> to stop the link *contents* being committed if a link is replaced by a real directory.

### Reference archived artifacts as `archive/…` and `scratch/…`

Two tracked symlinks point into this repo's **own slice** of the shared archive:

| Link | Target | Contains |
|---|---|---|
| `archive` | `../repo-archive/hardware-doc` | bulky artifacts moved out of here |
| `scratch` | `../repo-archive/scratch/hardware-doc` | raw fetches, provenance snapshots, working files |

So a placeholder reads:

```
| Archived to | `archive/devices/<vendor>/<board>/artifacts/…` |
```

— the path after `archive/` is **the same path it had in this repository**. No prefix to
remember, nothing to recompute.

The archive is namespaced by source repository:

```
repo-archive/
├── hardware-doc/          ← what `archive` points at
└── scratch/hardware-doc/  ← what `scratch` points at
```

A second repository's material would sit beside these rather than colliding. Paths are
relative to the repository root, so run restore commands from there.

The indirection is the point: **if the archive moves or is renamed, two symlinks change** and
every reference keeps working.

> Prose that explains the layout keeps the real sibling path (`../repo-archive`),
> because it describes where the directory actually is. Only followable paths use the links.

**Caveat.** While `--skip-worktree` is set, git refuses to update that path. If a committed
link target ever legitimately changes upstream, a clone carrying the flag will **not** pick
it up on pull, and merges or checkouts touching it can fail with `Entry ... not uptodate`.
Clear it with:

```bash
git update-index --no-skip-worktree archive        # or doc/hardware in the consumer
```

The script prints that exact command whenever it sets the flag, and only sets it when the
relative default genuinely does not work.

## What belongs where

| Content | Goes in |
|---|---|
| Authored research — device records, component records, feature guides, vendor guides | **this repo** |
| Small primary artifacts — schematics, datasheets, BOMs, firmware images, EDA sources | **this repo**, under `devices/**/artifacts/` or `components/**/artifacts/` |
| Bulky derived output — 3D STEP models, panelisation files, generated doc builds, enclosure meshes, prebuilt binaries already published upstream | **`../repo-archive/`**, with a `*.ARCHIVED.md` placeholder left behind |
| Scratch downloads, raw HTML fetches, working files | `../hardware-doc-scratch/` |

Never delete an acquired artifact. Move it to the archive and leave a placeholder that
records size, SHA-256, upstream commit/author/licence and **multiple recovery URLs**.
[`tools/archive_artifact.py`](tools/archive_artifact.py) does this, verifies the move by
content fingerprint, and refuses to overwrite an existing archive entry.

## Research method

The full method lives in the skill: [`.agents/skills/hardware-device-research/SKILL.md`](.agents/skills/hardware-device-research/SKILL.md).

Points worth restating because they are repeatedly load-bearing:

- **Prefer primary machine-readable evidence.** A `.kicad_pcb` netlist beats a wiki table.
  Several findings in this repo exist only because the PCB was parsed rather than the docs read.
- **Cross-check across independent sources** and record which agree. Where they disagree,
  document the conflict rather than choosing silently.
- **Label evidence status** — `executed-success`, `reported-working`, `inferred`,
  `not-tested`. Never present an untested command as authoritative.
- **Record vendor documentation traps** in `vendors/<vendor>/README.md` — soft-404s, JS
  shells, licence mis-detection, pagination limits. They recur for every future part from
  that vendor.

## Web retrieval fallback

When retrieving public web content with `curl`, `wget`, Python HTTP clients, or similar tools:

1. Use the normal/default request first.
2. If the request returns a 403, 429, obvious bot-block page, or otherwise fails because of automated-client filtering, retry with a normal modern browser User-Agent:
   `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36`
3. If that still fails, try other well-known user agents — different sites block different agents, so it is worth rotating through several before giving up. Good next tries:
   - `WhatsApp/2.23.20.0` (link-preview fetcher; rarely blocked, often slips through news/paywall-adjacent CDNs)
   - `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot`
   - `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ClaudeBot/1.0; +claudebot@anthropic.com`
4. A full sorted list of known user-agent strings, which operators publish IP ranges for verification, and a site-by-site access matrix (which agents worked or failed on which domains) lives in [`ai-crawler-site-access-table.md`](./ai-crawler-site-access-table.md#user-agents). Check that section for details and prior findings — including notes about the specific domain you are hitting.
5. Do not use altered User-Agent headers when testing or debugging the actual HTTP behaviour of an application, API, website, authentication flow, or client, because doing so could hide genuine access-control or compatibility problems.
6. Do not treat a successful response obtained with an alternate User-Agent as evidence that the resource works normally for ordinary clients.
7. Do not use User-Agent substitution to bypass authentication, account permissions, or other explicit access controls.
8. **Document what works.** When plain requests fail but an alternate path succeeds, add your findings to `ai-crawler-site-access-table.md` (the agent's subsection under *User Agents*, the domain's subsection under *Sites*, or *General retrieval tips*) at any time, regardless of what the current session is about, and include the update in your next commit. Failures are worth recording too: e.g. "UA X has known failures on example.com, but UA Y worked."
9. **Preserve scarce sources.** If a URL was genuinely useful and hard to acquire — very few copies online, or hosted somewhere unlikely to persist — submit it to `https://web.archive.org/save/<url>` (works unauthenticated). This applies to the kind of thing that has no mirror: datasheets/whitepaper/manual PDFs, technical docs on fragile personal or CMS-hosted pages, demo/example projects that exist only to illustrate how some code works, hard-to-find header files or source snippets not in any repo or package manager, one-off benchmark posts. It does **not** apply to widely-mirrored content (Wikipedia, MDN, popular repos) or anything already covered elsewhere — you can't and shouldn't archive every page you visit. Anonymous saves are rate-limited to roughly a few per minute; don't hammer it.
   - **Rare case:** if you are confident the site is still up but you are blocked or rate-limited, and you already know from some other source that the URL is valuable (a citation, an API doc you need, source code relevant to the task), you may submit it unseen and record that it wasn't directly accessible but was submitted on `<date>` — e.g. in the relevant *Sites* subsection of `ai-crawler-site-access-table.md` — so a future agent can check `web.archive.org` for the capture. Only do this when there's a concrete reason the page matters, not speculatively.

## Size discipline

This repo is large by nature — see [`SIZE-AUDIT.md`](SIZE-AUDIT.md). Before adding
anything bulky:

- **Is it derived?** Gerbers, STEP exports and generated doc builds come from files already
  retained. Archive them.
- **Is it reproducible?** If it can be re-fetched from a pinned commit or a stable vendor
  URL, an archive placeholder with recovery URLs is usually enough.
- **Is it unique?** Firmware binaries are **not** byte-reproducible from source, and several
  datasheets here are not published by their manufacturer at all. Those stay.

Duplicate content is pooled into `shared-assets/` as relative symlinks by
[`tools/dedupe_shared_assets.py`](tools/dedupe_shared_assets.py). **Any size-accounting or
duplicate-detection script must skip symlinks** or it will double-count ~154 files and
report phantom waste.

## Git conventions

- Do not commit, amend or push unless asked.
- Never stage a deletion as part of an archive operation: stage the file's content, then
  move it, and leave the resulting worktree deletion **unstaged**.
- Filenames contain spaces (vendor EDA exports). Use `-z`/NUL-delimited git plumbing when
  scripting over `git status`.
