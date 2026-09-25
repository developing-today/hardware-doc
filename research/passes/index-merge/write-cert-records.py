#!/usr/bin/env python3
"""Round-2 integration, TASK 3 — directory READMEs and acquisition manifests.

Writes, for every record that received FCC exhibits:

  * artifacts/certification/README.md   (only where none exists — never overwrite
                                         another session's)
  * acquisition/manifest.json           (new file where none exists)
    acquisition/manifest-fcc-exhibits.json
                                        (sibling, where manifest.json exists but
                                         its `artifacts` array is inline `[]` and
                                         therefore not append-safe as JSON)
    otherwise: entries are INSERTED textually after `"artifacts": [` so that not
    one existing line is deleted, reworded or reordered.

PaperMono is skipped entirely — another session owns that tree.
"""
import json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..'))
ARCHIVE = os.path.realpath(os.path.join(REPO, 'archive'))
TODAY = '2026-09-11'
DRY = '--apply' not in sys.argv
os.chdir(REPO)

plan = json.load(open(os.path.join(HERE, 'plan.json')))
byowner = collections.defaultdict(list)
for x in plan:
    if x['owner'] and x['disposition'] != 'park':
        byowner[x['owner']].append(x)

LICENCE = ("FCC equipment-authorisation exhibits are **US Government public records**, "
           "published by a federal agency under 47 CFR §2.1033. Redistribution **`allowed`**.")

def mib(n): return f"{n/1048576:.2f} MiB"

# --------------------------------------------------------------- directory README
def dir_readme(owner, rows):
    fid = sorted({r['fccid'] for r in rows})
    meta = rows[0]
    keep = [r for r in rows if r['disposition'] == 'already-in-repo'
            and r['dest'] and os.path.exists(r['dest'])]
    arch = [r for r in rows if r['disposition'] == 'archive']
    L = [f"# FCC equipment-authorization exhibits — {', '.join('`%s`' % f for f in fid)}",
         "",
         f"Retrieved **{TODAY}** from `fccid.io` with a non-browser User-Agent "
         "(`curl/8.5.0`); every file magic-byte validated (`%PDF`). Filed here by the "
         "round-2 index merge on 2026-09-11.",
         "",
         "| Field | Value |", "|---|---|"]
    for f in fid:
        m = [r for r in rows if r['fccid'] == f][0]
        L += [f"| FCC ID | **`{f}`** |",
              f"| Applicant | {m['applicant'] or 'unknown'} |",
              f"| Granted | **{m['granted'] or 'unknown'}** |",
              f"| Equipment class | {m.get('equip_class') or 'unknown'}"
              + (f", {', '.join(m.get('freq') or [])}" if m.get('freq') else '') + " |",
              f"| Test firm | {m['test_firm'] or 'unknown'} |",
              f"| Source page | <https://fccid.io/{f}> |"]
    L += ["", "## Retained in the repository", ""]
    if keep:
        L += ["| File | Bytes | SHA-256 | Exhibit type |", "|---|---:|---|---|"]
        for r in sorted(keep, key=lambda r: r['dest']):
            L.append(f"| `{os.path.basename(r['dest'])}` | {r['bytes']:,} | "
                     f"`{r['sha256']}` | {r['exhibit_type']} |")
        L += ["",
              "**Internal Photos** and **ID Label / Location Info** are kept in the repository "
              "because they are the identification and teardown evidence: for several of these "
              "boards the internal photographs are the only public imagery of the PCB that "
              "exists anywhere.", ""]
    else:
        L += ["_None — every exhibit for this filing is archived; see below._", ""]
    L += ["## Archived out of the repository", ""]
    if arch:
        L += ["Each has a self-sufficient placeholder beside it carrying its hash, byte size, "
              "FCC document id, publication date and five reacquisition URLs. A reader without "
              "the archive can recover any of them from the placeholder alone.", "",
              "| Placeholder | Bytes | Exhibit type |", "|---|---:|---|"]
        for r in sorted(arch, key=lambda r: r['dest']):
            b = os.path.basename(r['dest'])
            L.append(f"| [`{b}.ARCHIVED.md`]({b}.ARCHIVED.md) | {r['bytes']:,} | {r['exhibit_type']} |")
        L += ["", f"Archived total: **{len(arch)} files, {mib(sum(r['bytes'] for r in arch))}**.", ""]
    else:
        L += ["_None._", ""]
    L += ["## Licensing and disposition", "", "| Field | Value |", "|---|---|",
          f"| Redistribution status | **`allowed`** — {LICENCE} |",
          "| Disposition | `repository` (retained files, **unstaged**) / `archive` (placeholders) |",
          f"| Retained in repo | **{len(keep)} files, {mib(sum(r['bytes'] for r in keep))}** |",
          f"| Archived | **{len(arch)} files, {mib(sum(r['bytes'] for r in arch))}** |", "",
          "Method, URL templates and the measured user-agent matrix: "
          "[`guides/research/finding-certification-records.md`]("
          + os.path.relpath('guides/research/finding-certification-records.md',
                            os.path.dirname(owner + '/artifacts/certification/README.md'))
          + ").", ""]
    return "\n".join(L)

# -------------------------------------------------------------------- manifest
def entries(owner, rows):
    out = []
    for r in sorted(rows, key=lambda r: r['dest'] or ''):
        if r['disposition'] == 'already-in-repo' and not (r['dest'] and os.path.exists(r['dest'])):
            continue
        archived = r['disposition'] == 'archive'
        out.append({
            "id": f"fcc-{r['fccid']}-{r['fcc_doc_id'] or os.path.basename(r['dest'])[:-4]}",
            "kind": "regulatory-exhibit",
            "canonical_url": r['url'],
            "fallback_urls": [
                f"https://apps.fcc.gov/eas/GetApplicationAttachment.html?id={r['fcc_doc_id']}",
                f"https://fcc.report/FCC-ID/{r['fccid']}/{r['fcc_doc_id']}.pdf",
                f"https://fccid.io/{r['fccid']}",
                f"https://web.archive.org/web/2/{r['url']}",
            ] if r['fcc_doc_id'] else [f"https://fccid.io/{r['fccid']}"],
            "sha256": r['sha256'],
            "bytes": r['bytes'],
            "destination": r['dest'],
            "retrieved": TODAY,
            "upstream_version_or_date": r['published'] or None,
            "fcc_id": r['fccid'],
            "fcc_document_id": r['fcc_doc_id'] or None,
            "exhibit_type": r['exhibit_type'],
            "exhibit_title_as_filed": r['document'] or None,
            "grant_date": r['granted'] or None,
            "applicant": r['applicant'] or None,
            "test_firm": r['test_firm'] or None,
            "license": "US Government public record (47 CFR 2.1033); no agency copyright claim",
            "license_evidence": "FCC Equipment Authorization System publication",
            "redistribution_status": "allowed",
            "disposition": "archive" if archived else "repository",
            "repo_state": "placeholder-only" if archived else "untracked",
            "archived_to": os.path.join(ARCHIVE, r['dest']) if archived else None,
            "placeholder": r['dest'] + '.ARCHIVED.md' if archived else None,
            "extraction": None,
            "target_hardware": owner,
            "reacquisition": "automatic",
            "reacquisition_note": ("fccid.io requires a non-browser User-Agent; a Chrome UA "
                                   "receives a Cloudflare 403. The `.pdf` suffix is mandatory."),
            "last_verified": TODAY,
            "notes": "Filed by the round-2 index merge, 2026-09-11.",
        })
    return out

wrote = []
for owner, rows in sorted(byowner.items()):
    cdir = f"{owner}/artifacts/certification"
    rp = f"{cdir}/README.md"
    if not os.path.exists(rp):
        if not DRY:
            os.makedirs(cdir, exist_ok=True)
            open(rp, 'w').write(dir_readme(owner, rows))
        wrote.append(rp)

    es = entries(owner, rows)
    if not es: continue
    adir = f"{owner}/acquisition"
    mp = f"{adir}/manifest.json"
    if not os.path.exists(mp):
        doc = {"record": owner, "generated": TODAY,
               "note": ("FCC equipment-authorization exhibits filed by the round-2 index merge, "
                        "2026-09-11. Exhibits whose `disposition` is `archive` are NOT in the "
                        "repository; a self-sufficient placeholder sits at `destination` + "
                        "`.ARCHIVED.md`."),
               "artifacts": es, "wanted": []}
        if not DRY:
            os.makedirs(adir, exist_ok=True)
            json.dump(doc, open(mp, 'w'), indent=1)
            open(mp, 'a').write("\n")
        wrote.append(mp)
    else:
        src = open(mp).read()
        m = re.search(r'^([ \t]*)"artifacts":[ \t]*\[[ \t]*$', src, re.M)
        if m:
            # additive textual insertion — not one existing line is touched
            ind = m.group(1) + ' '
            blob = json.dumps(es, indent=1)[1:-1].strip()
            blob = "\n".join(ind + l for l in blob.splitlines())
            new = src[:m.end()] + "\n" + blob + "," + src[m.end():]
            if not DRY:
                assert all(l in new for l in src.splitlines() if l.strip())
                open(mp, 'w').write(new)
            wrote.append(mp + '  (inserted)')
        else:
            # `"artifacts": []` inline is not append-safe as JSON — sibling file,
            # the same convention the schematic-tracing pass used for media manifests
            sp = f"{adir}/manifest-fcc-exhibits.json"
            doc = {"record": owner, "generated": TODAY,
                   "note": ("Sibling of `manifest.json`. That file's `artifacts` array is "
                            "written inline as `[]`, so it cannot be extended without "
                            "rewriting an existing line; this pass is append-only. Merge on "
                            "the next non-append-constrained edit."),
                   "artifacts": es}
            if not DRY:
                json.dump(doc, open(sp, 'w'), indent=1)
                open(sp, 'a').write("\n")
            wrote.append(sp + '  (sibling)')

print('DRY RUN' if DRY else 'APPLIED')
for w in wrote: print('  ', w)
print(' ', len(wrote), 'files')
