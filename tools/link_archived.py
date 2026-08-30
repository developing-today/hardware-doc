#!/usr/bin/env python3
"""Place symlinks at the original paths of archived artifacts.

Driven by the archive itself rather than by placeholder files, so material that was
moved out without leaving a placeholder still gets a marker at its original path.

Links are made at the SHALLOWEST path the repo is missing: an archived 1,654-file
tree becomes one symlink to the directory, not 1,654 links to its contents. Where the
repo still has a real directory, we descend into it, since only part of it was moved.

Targets are relative and route through this repo's own `archive/` symlink, e.g.
`../../../archive/devices/foo/bar`, never at ../repo-archive directly - so relocating
the archive means editing one symlink instead of every link in the tree.

    python3 tools/link_archived.py            # dry run
    python3 tools/link_archived.py --apply
    python3 tools/link_archived.py --apply --remove
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(REPO, "archive")

# Never symlink git's own control files. Git reads .gitignore/.gitattributes as
# configuration rather than content: pointing them through the archive symlink makes
# it emit "Too many levels of symbolic links" on every command, and in principle lets
# a vendored upstream's ignore rules bleed into this repo. They are trivial text files
# covered by the enclosing tree's record anyway.
SKIP_NAMES = {".gitignore", ".gitattributes", ".gitmodules"}


def targets():
    """Shallowest archive paths with no corresponding entry in the repo."""
    out = []

    def walk(d):
        rel = os.path.relpath(d, ARCHIVE)
        rel = "" if rel == "." else rel
        try:
            entries = sorted(os.listdir(d))
        except OSError:
            return
        for e in entries:
            full = os.path.join(d, e)
            er = os.path.join(rel, e) if rel else e
            rp = os.path.join(REPO, er)
            if os.path.islink(rp):
                continue                       # already stood in for
            if os.path.isdir(full) and not os.path.islink(full):
                if os.path.isdir(rp):
                    walk(full)                 # partially archived - go deeper
                else:
                    out.append(er)             # whole tree absent - one link
            elif not os.path.exists(rp) and e not in SKIP_NAMES:
                out.append(er)
    walk(ARCHIVE)
    return out


def main():
    apply_ = "--apply" in sys.argv
    remove = "--remove" in sys.argv
    if not os.path.isdir(ARCHIVE):
        print("no archive/ present - run scripts/init.sh first")
        return 0

    if remove:
        n = 0
        for dp, dns, fns in os.walk(REPO):
            if ".git" in dp or dp.startswith(os.path.join(REPO, "archive")):
                continue
            for f in list(dns) + fns:
                p = os.path.join(dp, f)
                if os.path.islink(p) and "/archive/" in os.readlink(p):
                    if apply_:
                        os.unlink(p)
                    n += 1
        print(f"{'removed' if apply_ else 'would remove'} {n} archive symlink(s)")
        return 0

    made = 0
    for rel in targets():
        link = os.path.join(REPO, rel)
        depth = len(os.path.dirname(rel).split(os.sep)) if os.path.dirname(rel) else 0
        target = os.path.join(*([".."] * depth), "archive", rel) if depth else os.path.join("archive", rel)
        if apply_:
            os.makedirs(os.path.dirname(link), exist_ok=True)
            if os.path.islink(link):
                os.unlink(link)
            os.symlink(target, link)
        made += 1
    print(f"{'linked' if apply_ else 'would link'} {made} archived path(s)")
    if not apply_:
        print("re-run with --apply to create them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
