#!/usr/bin/env python3
"""Replace byte-identical duplicate files with symlinks into a shared asset pool.

Every duplicate set is reduced to ONE real file under `doc/hardware/shared-assets/`,
named `<sha256[:12]>-<basename>`. Each former location becomes a *relative* symlink,
so the tree still resolves from any clone and vendored example sketches keep working.

Each directory that gave up a file gains a `SHARED-ASSETS.md` placeholder recording
the hash, size, shared-pool target and the sibling copies, so the substitution is
discoverable without this script or the archive.

Usage:
    dedupe_shared_assets.py --dry-run      # report only (default)
    dedupe_shared_assets.py --apply        # perform the moves
    dedupe_shared_assets.py --verify       # re-check every symlink resolves and hashes match
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, collections
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # doc/hardware
POOL = os.path.join(ROOT, "shared-assets")
MIN_BYTES = 20_000
SKIP_DIRS = {".git", "shared-assets"}

# Duplicate sets where the automatic "longest basename wins" choice would enshrine a
# WRONG name in the shared pool. Keyed by a path fragment identifying the set; the
# value is the basename that should name the pool entry.
NAME_OVERRIDES = {
    # `ov2640-camera-module-software-application-notes.pdf` is byte-identical to
    # `ov2640-datasheet-v2.2.pdf`. It is NOT the application notes -- that document was
    # never actually obtained; the download produced a second copy of the datasheet.
    # Naming the pool entry after it would propagate the error to every linked location.
    "ov2640": "ov2640-datasheet-v2.2.pdf",
}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            p = os.path.join(dirpath, name)
            if os.path.islink(p):
                continue
            try:
                if os.path.getsize(p) < MIN_BYTES:
                    continue
            except OSError:
                continue
            yield p


def find_duplicates() -> dict[str, list[str]]:
    """Hash only within same-size groups -- avoids hashing the whole tree."""
    by_size = collections.defaultdict(list)
    for p in walk_files():
        by_size[os.path.getsize(p)].append(p)
    dups = {}
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        by_hash = collections.defaultdict(list)
        for p in paths:
            by_hash[sha256(p)].append(p)
        for h, ps in by_hash.items():
            if len(ps) > 1:
                dups[h] = sorted(ps)
    return dups


def canonical(paths: list[str]) -> str:
    """Pick whose basename names the pool entry.

    Prefer a copy filed under components/ or vendors/ -- those are the deliberate,
    classified locations, whereas a copy inside a vendor demo ZIP is incidental.
    Then prefer the most descriptive (longest) basename; tie-break alphabetically.

    NAME_OVERRIDES exists because "longest basename" assumes names are honest, and
    occasionally one is not -- see the OV2640 entry.
    """
    for frag, wanted in NAME_OVERRIDES.items():
        for p in paths:
            if os.path.basename(p) == wanted and any(frag in q for q in paths):
                return p

    def key(p: str):
        rel = os.path.relpath(p, ROOT)
        classified = rel.startswith(("components/", "vendors/", "guides/"))
        return (not classified, -len(os.path.basename(p)), p)
    return sorted(paths, key=key)[0]


def pool_name(h: str, path: str) -> str:
    return f"{h[:12]}-{os.path.basename(path)}"


def reindex() -> list[dict]:
    """Rebuild the manifest from what is actually on disk.

    Derived state, not remembered state: we walk the tree looking for symlinks that
    resolve into the pool, and group them by target. This makes the tool idempotent --
    re-running cannot produce an empty or stale manifest, which an earlier version did
    because it wrote only what the *current* dedupe scan had found (nothing, once the
    duplicates were already symlinks).
    """
    links = collections.defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        if os.path.abspath(dirpath) == os.path.abspath(POOL):
            continue
        for name in filenames:
            p = os.path.join(dirpath, name)
            if not os.path.islink(p):
                continue
            real = os.path.realpath(p)
            if os.path.dirname(real) == os.path.abspath(POOL):
                links[os.path.basename(real)].append(os.path.relpath(p, ROOT))

    entries = []
    for pool_entry in sorted(os.listdir(POOL)):
        if pool_entry == "manifest.json":
            continue
        target = os.path.join(POOL, pool_entry)
        entries.append({
            "sha256": sha256(target),
            "bytes": os.path.getsize(target),
            "pool_entry": pool_entry,
            "linked_from": sorted(links.get(pool_entry, [])),
        })
    entries.sort(key=lambda m: -m["bytes"] * max(len(m["linked_from"]) - 1, 0))
    return entries


def write_manifest(entries: list[dict]) -> None:
    payload = {
        "generated": str(date.today()),
        "tool": "doc/hardware/tools/dedupe_shared_assets.py",
        "note": "Derived from disk state by --reindex; safe to regenerate at any time.",
        "entries": entries,
    }
    with open(os.path.join(POOL, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=True)
        fh.write("\n")


PLACEHOLDER_HEAD = """# Shared assets in this directory

> One or more files here are **byte-identical to copies elsewhere in this repository**.
> Each has been replaced by a *relative symlink* into
> [`doc/hardware/shared-assets/`]({pool_rel}), which holds the single real copy.
>
> **Nothing was deleted and no path changed.** Reading, building or flashing from this
> directory works exactly as before, because the symlink resolves to the same bytes.

| File here | Bytes | SHA-256 | Shared pool entry |
|---|---:|---|---|
{rows}

## Why

Storing the same bytes N times costs space and, worse, lets the copies drift apart
silently. A symlink makes the sharing explicit and keeps every original path valid.

## Caveat for vendored upstream trees

If this directory is part of a vendored upstream snapshot, the symlink is a **local
modification**: a fresh `git clone` of upstream would contain a regular file here.
Account for that when diffing against upstream. The bytes are unchanged, so a
content comparison still matches -- only the file *type* differs.

## Restoring a real file

```bash
cp --remove-destination "$(readlink -f <file>)" <file>
```

Or re-fetch from the pool's archive copy:
`../repo-archive/doc/hardware/shared-assets/`

The full set of sharing relationships, including every location that links to each
entry, is in [`shared-assets/manifest.json`]({pool_rel}/manifest.json).
"""


def _safe(s: str) -> str:
    """Some vendor ZIPs carry filenames in a non-UTF-8 encoding, which Python surfaces
    as lone surrogates. Those cannot be written to a UTF-8 file, so render them
    losslessly-enough for a human and flag that the real name differs."""
    try:
        s.encode("utf-8")
        return s
    except UnicodeEncodeError:
        return s.encode("utf-8", "replace").decode("utf-8") + "  *(name is not valid UTF-8)*"


def write_placeholder(directory: str, entries: list[dict]) -> None:
    pool_rel = os.path.relpath(POOL, directory)
    rows = "\n".join(
        "| `{name}` | {bytes:,} | `{sha}` | [`{pn}`]({pool_rel}/{pn}) |".format(
            name=_safe(e["name"]), bytes=e["bytes"], sha=e["sha"],
            pn=_safe(e["pool"]), pool_rel=pool_rel
        )
        for e in sorted(entries, key=lambda x: x["name"])
    )
    body = PLACEHOLDER_HEAD.format(pool_rel=pool_rel, rows=rows)
    with open(os.path.join(directory, "SHARED-ASSETS.md"), "w",
              encoding="utf-8", errors="replace") as fh:
        fh.write(body)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reindex", action="store_true",
                    help="Rebuild manifest.json from disk state. Safe, read-only apart "
                         "from the manifest itself.")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    if args.reindex:
        entries = reindex()
        write_manifest(entries)
        linked = sum(len(e["linked_from"]) for e in entries)
        orphan = [e["pool_entry"] for e in entries if not e["linked_from"]]
        print(f"reindexed {len(entries)} pool entries, {linked} symlinks")
        if orphan:
            print(f"  WARNING: {len(orphan)} pool entries have no symlink pointing at them:")
            for o in orphan[:10]:
                print(f"    {o}")
        return 0

    if args.verify:
        return verify()

    dups = find_duplicates()
    total_saved = sum(os.path.getsize(v[0]) * (len(v) - 1) for v in dups.values())
    print(f"{len(dups)} duplicate sets, {total_saved/1048576:.1f} MiB reclaimable")
    if not args.apply:
        for h, paths in sorted(dups.items(), key=lambda kv: -os.path.getsize(kv[1][0])):
            print(f"  {os.path.getsize(paths[0])/1048576:6.2f} MiB x{len(paths)}  -> {pool_name(h, canonical(paths))}")
        print("\n(dry run -- pass --apply to perform)")
        return 0

    os.makedirs(POOL, exist_ok=True)
    manifest, per_dir = [], collections.defaultdict(list)

    for h, paths in sorted(dups.items()):
        canon = canonical(paths)
        pn = pool_name(h, canon)
        target = os.path.join(POOL, pn)
        size = os.path.getsize(canon)
        if not os.path.exists(target):
            os.replace(canon, target)
        links = []
        for p in paths:
            if os.path.exists(p) and not os.path.islink(p):
                os.remove(p)
            rel = os.path.relpath(target, os.path.dirname(p))
            os.symlink(rel, p)
            links.append(os.path.relpath(p, ROOT))
            per_dir[os.path.dirname(p)].append(
                {"name": os.path.basename(p), "bytes": size, "sha": h, "pool": pn}
            )
        manifest.append(
            {"sha256": h, "bytes": size, "pool_entry": pn,
             "canonical_source": os.path.relpath(canon, ROOT),
             "linked_from": sorted(links), "shared_date": str(date.today())}
        )

    manifest.sort(key=lambda m: -m["bytes"] * (len(m["linked_from"]) - 1))
    with open(os.path.join(POOL, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"generated": str(date.today()),
                   "tool": "doc/hardware/tools/dedupe_shared_assets.py",
                   "entries": manifest}, fh, indent=2)
        fh.write("\n")

    for d, entries in per_dir.items():
        write_placeholder(d, entries)

    print(f"pooled {len(manifest)} entries, wrote {len(per_dir)} SHARED-ASSETS.md placeholders")
    return 0


def verify() -> int:
    mpath = os.path.join(POOL, "manifest.json")
    if not os.path.exists(mpath):
        print("no manifest -- nothing to verify")
        return 1
    data = json.load(open(mpath, encoding="utf-8"))
    bad = 0
    for e in data["entries"]:
        target = os.path.join(POOL, e["pool_entry"])
        if not os.path.exists(target):
            print(f"  MISSING pool entry: {e['pool_entry']}"); bad += 1; continue
        actual = sha256(target)
        if actual != e["sha256"]:
            print(f"  HASH MISMATCH: {e['pool_entry']}"); bad += 1
        if os.path.getsize(target) != e["bytes"]:
            print(f"  SIZE MISMATCH: {e['pool_entry']}"); bad += 1
        for rel in e["linked_from"]:
            p = os.path.join(ROOT, rel)
            if not os.path.islink(p):
                print(f"  NOT A SYMLINK: {rel}"); bad += 1
            elif not os.path.exists(p):
                print(f"  DANGLING: {rel}"); bad += 1
            elif os.path.realpath(p) != os.path.realpath(target):
                print(f"  WRONG TARGET: {rel}"); bad += 1
    print(f"verified {len(data['entries'])} entries, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
