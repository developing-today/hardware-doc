#!/usr/bin/env python3
"""Fail if a commit SHA, content hash or URL was removed or rewritten in place.

Pins are append-only (see AGENTS.md). Upstream moving is normal; *losing the old
ref* is not, because prose elsewhere in the tree was written from it.

Compares the working tree against a git ref (default HEAD) and reports any
identifier that disappeared or changed value rather than being appended.

    ./scripts/check-pins.py                 # working tree vs HEAD
    ./scripts/check-pins.py --base origin/main
    ./scripts/check-pins.py --staged        # index vs HEAD
    ./scripts/check-pins.py --json

Exit 0 clean, 1 if pins were lost, 2 on usage/git error.
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from collections import defaultdict

# 40- and 12-hex git SHAs, sha256 prefixes, and full sha256.
SHA_RE = re.compile(r'\b[0-9a-f]{40}\b|\b[0-9a-f]{64}\b|\b[0-9a-f]{12}\b')
URL_RE = re.compile(r'https?://[^\s<>()\[\]"\'`|]+')
# Things that look like hashes but are not pins.
NOISE = re.compile(r'^(0+|f+|deadbeef\w*)$')

TEXT_SUFFIXES = ('.md', '.json', '.jsonc', '.yaml', '.yml', '.txt', '.csv', '.ini', '.toml')


def git(*args: str) -> str:
    r = subprocess.run(['git', *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"git {' '.join(args)}: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return r.stdout


def changed_files(base: str, staged: bool) -> list[str]:
    args = ['diff', '--name-only', '--diff-filter=ACMR']
    if staged:
        args.append('--cached')
    args.append(base)
    return [f for f in git(*args).splitlines() if f.endswith(TEXT_SUFFIXES)]


def blob_at(ref: str, path: str) -> str | None:
    r = subprocess.run(['git', 'show', f'{ref}:{path}'], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def working(path: str, staged: bool) -> str | None:
    if staged:
        r = subprocess.run(['git', 'show', f':{path}'], capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    try:
        return open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return None


def ids(text: str) -> dict[str, set[str]]:
    shas = {s for s in SHA_RE.findall(text) if not NOISE.match(s)}
    urls = {u.rstrip('.,;:') for u in URL_RE.findall(text)}
    return {'sha': shas, 'url': urls}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--base', default='HEAD', help='ref to compare against (default HEAD)')
    ap.add_argument('--staged', action='store_true', help='compare the index instead of the worktree')
    ap.add_argument('--json', action='store_true', dest='as_json')
    ap.add_argument('--quiet', '-q', action='store_true')
    a = ap.parse_args()

    lost: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    files = changed_files(a.base, a.staged)

    for path in files:
        old = blob_at(a.base, path)
        if old is None:          # newly added file — nothing can have been lost
            continue
        new = working(path, a.staged)
        if new is None:
            continue
        o, n = ids(old), ids(new)
        for kind in ('sha', 'url'):
            # A 12-hex prefix of a retained 40-hex SHA is not a loss, and vice versa.
            gone = set()
            for v in o[kind] - n[kind]:
                if kind == 'sha' and any(v.startswith(x[:len(v)]) or x.startswith(v[:len(x)])
                                         for x in n[kind]):
                    continue
                gone.add(v)
            if gone:
                lost[path][kind] = sorted(gone)

    if a.as_json:
        print(json.dumps({'base': a.base, 'files_checked': len(files),
                          'lost': {k: dict(v) for k, v in lost.items()}}, indent=2))
        return 1 if lost else 0

    if not lost:
        if not a.quiet:
            print(f"check-pins: OK — {len(files)} file(s) checked against {a.base}, "
                  f"no identifiers removed or rewritten")
        return 0

    total = sum(len(v) for f in lost.values() for v in f.values())
    print(f"check-pins: {total} identifier(s) LOST across {len(lost)} file(s)\n")
    for path, kinds in sorted(lost.items()):
        print(f"  {path}")
        for kind, vals in kinds.items():
            for v in vals:
                print(f"    - {kind}: {v}")
    print("\nPins are append-only (AGENTS.md § 'Pins, hashes and identifiers are append-only').")
    print("Upstream moving is fine — add the new ref and move the old one into prior_refs[],")
    print("or mark it deprecated. Do not replace it in place.")
    print("\nIf a removal is genuinely correct (e.g. the value was a typo that never resolved),")
    print("say so in the commit message.")
    return 1


if __name__ == '__main__':
    sys.exit(main())
