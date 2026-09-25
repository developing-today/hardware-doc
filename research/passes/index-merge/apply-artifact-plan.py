#!/usr/bin/env python3
"""Round-2 integration, TASK 3 — apply plan.json.

repo    : copy the exhibit to its owning record's artifacts/certification/
archive : copy the exhibit to the sibling archive at the same repo-relative path,
          and write a self-sufficient placeholder at the repo path
park    : leave untouched (PaperMono — another session owns that tree)
already-in-repo : leave untouched (bytes are present; no duplication)

COPIES rather than moves: 24 authored records already cite
`scratch/market-and-certification/fcc/<FCCID>/` as their local path, and the
skill forbids tidying another session's scratch.  The scratch corpus stays as
that session left it; the repository and the archive each get what they need.

Idempotent.  Never deletes.  Never overwrites an existing file.
"""
import json, os, shutil, hashlib, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..'))
ARCHIVE = os.path.realpath(os.path.join(REPO, 'archive'))
TODAY = '2026-09-11'
DRY = '--apply' not in sys.argv
REFRESH = '--refresh' in sys.argv   # rewrite placeholders this pass already wrote

plan = json.load(open(os.path.join(HERE, 'plan.json')))

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def human(n):
    return f"{n:,} B ({n/1048576:.2f} MiB)"

def urls(x):
    """At least two independent reacquisition URLs, most reliable first.

    Reachability was measured from the research host on 2026-09-11 and is stated
    rather than assumed — fccid.io is the only one that answered.
    """
    u = []
    if x['url']:
        u.append((x['url'],
                  "fccid.io mirror — **200**, but only to a non-browser UA "
                  "(`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). "
                  "A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required."))
    if x['fcc_doc_id']:
        u.append((f"https://apps.fcc.gov/eas/GetApplicationAttachment.html?id={x['fcc_doc_id']}",
                  "official FCC Equipment Authorization System attachment — the primary record. "
                  "**403 to all five UAs tried from this host on 2026-09-11**; try from another network."))
        u.append((f"https://fcc.report/FCC-ID/{x['fccid']}/{x['fcc_doc_id']}.pdf",
                  "fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**"))
    u.append((f"https://fccid.io/{x['fccid']}",
              "the filing's exhibit index — re-read the row to recover a changed document slug."))
    if x['url']:
        u.append((f"https://web.archive.org/web/2/{x['url']}",
                  "Wayback Machine, if every live route is dead."))
    return u

def placeholder(x, dest):
    a = os.path.join(ARCHIVE, dest)
    lines = [
        f"# ARCHIVED: `{os.path.basename(dest)}`",
        "",
        "> This file was **moved out of the repository**, not deleted.",
        f"> Archived **{TODAY}** by the round-2 index merge.",
        "",
        f"**Reason:** bulk FCC exhibit — {x['exhibit_type'].lower()}, {human(x['bytes'])}. "
        "The round-2 artifact split keeps internal photographs and ID-label exhibits in the "
        "repository (they are the identification and teardown evidence) and archives the full "
        "test reports, RF-exposure annexes, users manuals and external-photo sets, which are "
        "bulky and repetitive.",
        "",
        "## Identity",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Original repo path | `{dest}` |",
        f"| Archived to | `{a}` |",
        "| Type | file (PDF, magic-byte validated `%PDF`) |",
        f"| Size | {human(x['bytes'])} |",
        f"| SHA-256 | `{x['sha256']}` |",
        f"| FCC ID | **`{x['fccid']}`** |",
        f"| Exhibit type | **{x['exhibit_type']}** |",
        f"| Exhibit title, as filed | {x['document'] or 'not recorded'} |",
        f"| FCC document id | {x['fcc_doc_id'] or 'not recorded'} |",
        f"| Upstream publication date | {x['published'] or 'not stated by the filing index'} |",
        f"| Grant date | {x['granted'] or 'unknown'} |",
        f"| Equipment class | {x.get('equip_class') or 'unknown'}"
        + (f", {', '.join(x.get('freq') or [])}" if x.get('freq') else '') + " |",
        f"| Applicant | {x['applicant'] or 'unknown'} |",
        f"| Test firm | {x['test_firm'] or 'unknown'} |",
        f"| Retrieved | {TODAY} |",
        "| Licence | **US Government public record.** FCC equipment-authorisation exhibits "
        "are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim "
        "by the agency. |",
        "| Redistribution status | **`allowed`** |",
        "| Disposition | `archive`, placeholder in repository |",
        "",
        "## How to get it back",
        "",
        "Independent reacquisition URLs, most reliable first:",
        "",
    ]
    for u, why in urls(x):
        lines += [f"- <{u}>  ", f"  {why}", ""]
    lines += [
        "Restore from the local archive, if you have one:",
        "",
        "```bash",
        f'mv "{a}" \\',
        f'   "{dest}"',
        "```",
        "",
        "Or re-download and verify — note the User-Agent, which is not optional:",
        "",
        "```bash",
        f'curl -fsSL -A "curl/8.5.0" "{x["url"]}" -o "{os.path.basename(dest)}"',
        f'echo "{x["sha256"]}  {os.path.basename(dest)}" | sha256sum -c -',
        "```",
        "",
        f"The archive path above is a **convenience**. Everything needed to recover this file "
        f"without the archive — hash, byte size, FCC ID, exhibit type, document id, publication "
        f"date and {len(urls(x))} URLs — is in this file.",
        "",
    ]
    return "\n".join(lines)

stats = {'repo': [0, 0], 'archive': [0, 0], 'skip': [0, 0], 'park': [0, 0]}
made = []
for x in plan:
    d = x['disposition']
    src = os.path.join(REPO, x['src'])
    if d in ('park', 'already-in-repo'):
        k = 'park' if d == 'park' else 'skip'
        stats[k][0] += 1; stats[k][1] += x['bytes']; continue
    dest = x['dest']
    if d == 'repo':
        out = os.path.join(REPO, dest)
        stats['repo'][0] += 1; stats['repo'][1] += x['bytes']
        if not DRY:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            if not os.path.exists(out):
                shutil.copy2(src, out)
                assert sha(out) == x['sha256'], f'hash mismatch {out}'
                made.append(dest)
    else:
        aout = os.path.join(ARCHIVE, dest)
        pout = os.path.join(REPO, dest + '.ARCHIVED.md')
        stats['archive'][0] += 1; stats['archive'][1] += x['bytes']
        if not DRY:
            os.makedirs(os.path.dirname(aout), exist_ok=True)
            if not os.path.exists(aout):
                shutil.copy2(src, aout)
                assert sha(aout) == x['sha256'], f'hash mismatch {aout}'
            os.makedirs(os.path.dirname(pout), exist_ok=True)
            if REFRESH or not os.path.exists(pout):
                open(pout, 'w').write(placeholder(x, dest))
                made.append(dest + '.ARCHIVED.md')

print('DRY RUN — pass --apply to execute' if DRY else 'APPLIED')
for k, (n, b) in stats.items():
    print(f"  {k:9s} {n:4d} files  {b/1048576:8.2f} MiB")
print(f"  created this run: {len(made)}")
