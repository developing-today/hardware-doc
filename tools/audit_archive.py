#!/usr/bin/env python3
"""Audit archive/repo consistency.

Every artifact moved into the archive is supposed to leave something behind at its
original path: a symlink standing in for it, a `*.ARCHIVED.md` placeholder, or - for
material archived as a set - an `ARCHIVED-<TOPIC>.md` record in the containing
directory. Prose in a README or acquisition manifest also counts, provided it names
the artifact.

This finds the cases where nothing was left behind at all, which is the failure that
loses things: a reader browsing the directory has no way to know the file existed.

    python3 tools/audit_archive.py            # summary
    python3 tools/audit_archive.py --verbose  # every unrepresented entry
"""
import os
import re
import subprocess
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(REPO, "archive")

# Deliberately never linked - see tools/link_archived.py. Git reads these as
# configuration, so symlinking them produces ELOOP warnings on every command.
SKIP_NAMES = {".gitignore", ".gitattributes", ".gitmodules"}


def mentioned_in_prose(rel):
    """True if some committed markdown names this artifact.

    Cheap and deliberately loose: we are asking 'could a reader find out this
    existed', not 'is it documented to standard'. Basename is enough - the point is
    to avoid flagging things that are in fact written up in an acquisition manifest
    or a snapshot index under a slightly different path.
    """
    base = os.path.basename(rel.rstrip("/"))
    if not base:
        return False
    try:
        r = subprocess.run(
            ["git", "grep", "-l", "-F", base, "--", "*.md"],
            cwd=REPO, capture_output=True, text=True, timeout=30,
        )
        return bool(r.stdout.strip())
    except (subprocess.SubprocessError, OSError):
        return False


def represented(rel):
    p = os.path.join(REPO, rel)
    if os.path.islink(p):
        return "symlink"
    if os.path.exists(p + ".ARCHIVED.md"):
        return "placeholder"
    d = os.path.dirname(p) or REPO
    try:
        if any(f.startswith("ARCHIVED-") and f.endswith(".md") for f in os.listdir(d)):
            return "set record"
    except OSError:
        pass
    return None


def walk(d, gaps, covered):
    rel = os.path.relpath(d, ARCHIVE)
    rel = "" if rel == "." else rel
    if rel:
        r = represented(rel)
        if r:                       # whole subtree accounted for
            covered.append((rel, r))
            return
    try:
        entries = sorted(os.listdir(d))
    except OSError:
        return
    for e in entries:
        full = os.path.join(d, e)
        er = os.path.join(rel, e) if rel else e
        if os.path.isdir(full) and not os.path.islink(full):
            r = represented(er)
            if r:
                covered.append((er, r))
            else:
                walk(full, gaps, covered)
        elif e not in SKIP_NAMES:
            r = represented(er)
            if r:
                covered.append((er, r))
            else:
                gaps.append(er)


def check_records():
    """Placeholders and set records that fall short of two independent sources.

    Distinct hosts matter more than raw URL count: five links to one vendor CDN are
    one outage from useless. Reported separately so the weaker case is visible.
    """
    thin_urls, thin_hosts, no_repo, gh_only, total = [], [], [], [], 0
    for dp, dns, fns in os.walk(REPO):
        dns[:] = [d for d in dns if d not in (".git", "archive", "scratch")]
        for f in fns:
            if not (f.endswith(".ARCHIVED.md")
                    or (f.startswith("ARCHIVED-") and f.endswith(".md"))):
                continue
            p = os.path.join(dp, f)
            if os.path.islink(p):
                continue
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            total += 1
            u = set(re.findall(r'https?://[^\s<>)\]"]+', t))
            h = {re.sub(r'^https?://([^/]+).*', r'\1', x) for x in u}
            rel = os.path.relpath(p, REPO)
            if len(u) < 2:
                thin_urls.append((len(u), rel))
            elif len(h) < 2:
                thin_hosts.append((len(h), rel))
            # A record sourced only from GitHub depends on one company's availability
            # decision, and one sourced with no repository at all usually means the
            # upstream was never looked for. Both are worth surfacing; neither is fatal,
            # and for genuinely closed-source artifacts "no repository" is the right answer.
            repos = set()
            for pat in (r'github\.com/([\w.-]+/[\w.-]+?)(?:\.git)?[/)\s`">]',
                        r'raw\.githubusercontent\.com/([\w.-]+/[\w.-]+?)/',
                        r'gitlab\.com/([\w.-]+/[\w.-]+?)[/)\s`">]'):
                repos |= set(re.findall(pat, t + " "))
            repos = {x for x in repos
                     if x.split("/")[0] not in ("orgs", "features", "about",
                                                "sponsors", "topics", "repos", "search")}
            if not repos:
                no_repo.append(rel)
            if not {x for x in h if "github" not in x}:
                gh_only.append(rel)
    return total, thin_urls, thin_hosts, no_repo, gh_only


def main():
    verbose = "--verbose" in sys.argv
    if not os.path.isdir(ARCHIVE):
        print("no archive/ present - run scripts/init.sh; nothing to audit")
        return 0
    gaps, covered = [], []
    walk(ARCHIVE, gaps, covered)

    prose = [g for g in gaps if mentioned_in_prose(g)]
    silent = [g for g in gaps if g not in set(prose)]

    def mb(paths):
        t = 0
        for g in paths:
            p = os.path.join(ARCHIVE, g)
            try:
                t += os.path.getsize(p)
            except OSError:
                pass
        return t / 1e6

    print(f"represented at their original path : {len(covered)}")
    for k, n in Counter(k for _, k in covered).most_common():
        print(f"  {k:<14} {n}")
    print()
    print(f"no marker at the original path     : {len(gaps)}  ({mb(gaps):.0f} MB)")
    print(f"  named in prose somewhere          : {len(prose)}  "
          f"- findable, but add a symlink/placeholder")
    print(f"  NOT MENTIONED ANYWHERE            : {len(silent)}  ({mb(silent):.0f} MB)"
          f"  <-- these are losable")
    if silent:
        print()
        print("Unmentioned, collapsed by directory:")
        c = Counter(os.sep.join(g.split(os.sep)[:6]) for g in silent)
        for d, n in c.most_common(20 if not verbose else 10**6):
            print(f"  {n:5d}  {d}")
    if verbose and prose:
        print()
        print("Named in prose but lacking a path-level marker:")
        for g in prose:
            print(f"  {g}")
    total, thin_urls, thin_hosts, no_repo, gh_only = check_records()
    print()
    print(f"placeholders / set records         : {total}")
    print(f"  fewer than 2 URLs                 : {len(thin_urls)}")
    print(f"  2+ URLs but a single host         : {len(thin_hosts)}")
    for n, r in thin_urls:
        print(f"    [{n} url] {r}")
    for n, r in thin_hosts:
        print(f"    [1 host] {r}")
    print(f"  no git repository cited           : {len(no_repo)}")
    for r in no_repo:
        print(f"    [no repo] {r}")
    print(f"  sourced only from GitHub          : {len(gh_only)}")
    for r in gh_only:
        print(f"    [gh only] {r}")
    if thin_urls or thin_hosts or no_repo or gh_only:
        print()
        print("  Two independent sources is the rule where it is possible, and a second")
        print("  custodian beats a second path under the same one. Where a repository or")
        print("  a non-GitHub source genuinely does not exist - proprietary tools, vendor")
        print("  ZIPs with no upstream - say so in the record. An absent line should read")
        print("  as checked and absent, not as an omission waiting to be 'fixed' with a")
        print("  plausible-looking link.")

    return 1 if silent else 0


if __name__ == "__main__":
    sys.exit(main())
