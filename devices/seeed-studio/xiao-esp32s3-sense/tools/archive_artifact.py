#!/usr/bin/env python3
"""Relocate bulky/duplicate artifacts out of the repository without losing them.

Policy (per user instruction, 2026-08-24): never delete a downloaded artifact.
Move it to ../repo-archive/ preserving its relative path, and leave a
Markdown placeholder in its place carrying everything needed to get the exact
bytes back: size, SHA-256, mtime, upstream repo + commit + author, and several
independent recovery URLs.

Usage:
  archive_artifact.py --repo-root <dir> --manifest <json> [--dry-run]

The manifest is a list of objects:
  {"path": "<path relative to repo root>",
   "reason": "...",
   "source": {"repo": "owner/name", "commit": "<sha>", "path_in_repo": "...",
              "author": "...", "committed": "...", "license": "..."}}
Directories are archived recursively as a unit with one placeholder.
"""

import argparse, hashlib, json, os, re, shutil, subprocess, datetime, sys

ARCHIVE = os.path.expanduser("../repo-archive")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def du(p):
    if os.path.isfile(p):
        return os.path.getsize(p)
    return sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, _, fs in os.walk(p)
        for f in fs
        if os.path.isfile(os.path.join(dp, f))
    )


def fingerprint(p):
    """Content identity for a file or a whole directory.

    For a file: its SHA-256.
    For a directory: a sorted manifest of (relative path, size, SHA-256) for every
    member, itself hashed. Two directories with the same fingerprint hold
    byte-identical content under identical names.

    Used to decide whether an archive collision is a genuine conflict or a
    harmless re-archive of the same bytes.
    """
    if os.path.isfile(p):
        return sha256(p), 1
    entries = []
    for dp, _, fs in os.walk(p):
        for f in sorted(fs):
            fp = os.path.join(dp, f)
            if os.path.isfile(fp):
                entries.append(
                    f"{os.path.relpath(fp, p)}\0{os.path.getsize(fp)}\0{sha256(fp)}"
                )
    entries.sort()
    h = hashlib.sha256("\n".join(entries).encode()).hexdigest()
    return h, len(entries)


def compare_trees(a, b):
    """Return (only_in_a, only_in_b, differing) keyed by relative path."""
    def manifest(root):
        m = {}
        if os.path.isfile(root):
            return {os.path.basename(root): sha256(root)}
        for dp, _, fs in os.walk(root):
            for f in fs:
                fp = os.path.join(dp, f)
                if os.path.isfile(fp):
                    m[os.path.relpath(fp, root)] = sha256(fp)
        return m
    ma, mb = manifest(a), manifest(b)
    only_a = sorted(set(ma) - set(mb))
    only_b = sorted(set(mb) - set(ma))
    diff = sorted(k for k in set(ma) & set(mb) if ma[k] != mb[k])
    return only_a, only_b, diff


def human(n):
    for u in ("B", "KiB", "MiB", "GiB"):
        if n < 1024 or u == "GiB":
            return (
                f"{n:,} bytes ({n / 1024 ** (('B', 'KiB', 'MiB', 'GiB').index(u)) if u != 'B' else n:.1f} {u})"
                if u != "B"
                else f"{n:,} bytes"
            )
        n_ = n
    return f"{n:,} bytes"


def size_str(n):
    if n < 1024:
        return f"{n:,} B"
    if n < 1024**2:
        return f"{n:,} B ({n / 1024:.1f} KiB)"
    return f"{n:,} B ({n / 1024**2:.2f} MiB)"


def urls(src, rel, is_dir=False):
    """Several independent ways to re-obtain the same bytes.

    GitHub's raw/blob/CDN endpoints only address *files*; for a directory the
    only single-request recovery is the repository tarball, so file-scoped URLs
    are suppressed to avoid emitting links that 404.
    """
    out = []
    repo = src.get("repo")
    commit = src.get("commit")
    pir = src.get("path_in_repo")
    if repo and commit and pir and not is_dir:
        out.append(
            (
                "raw file, pinned to commit (exact bytes)",
                f"https://raw.githubusercontent.com/{repo}/{commit}/{pir}",
            )
        )
        out.append(
            (
                "GitHub blob view, pinned to commit",
                f"https://github.com/{repo}/blob/{commit}/{pir}",
            )
        )
        out.append(
            (
                "jsDelivr CDN mirror, pinned to commit",
                f"https://cdn.jsdelivr.net/gh/{repo}@{commit}/{pir}",
            )
        )
    if repo and commit:
        out.append(
            (
                "whole-repository tarball at that commit (**works for directories**)",
                f"https://codeload.github.com/{repo}/tar.gz/{commit}",
            )
        )
    if repo and commit and pir and is_dir:
        out.append(
            (
                "browse the directory at that commit",
                f"https://github.com/{repo}/tree/{commit}/{pir}",
            )
        )
        out.append(
            (
                "jsDelivr directory listing at that commit",
                f"https://cdn.jsdelivr.net/gh/{repo}@{commit}/{pir}/",
            )
        )
    if repo and pir:
        out.append(
            (
                "current default branch (may have changed)",
                f"https://github.com/{repo}/{'tree' if is_dir else 'raw'}/HEAD/{pir}",
            )
        )
    if src.get("url"):
        out.append(("original download URL", src["url"]))
    if src.get("extra_urls"):
        for u in src["extra_urls"]:
            out.append(("additional mirror", u))
    return out


def placeholder(rel, dest, meta, src, is_dir, files=None, collision_note=None):
    lines = []
    name = os.path.basename(rel)
    lines.append(f"# ARCHIVED: `{name}`")
    lines.append("")
    lines.append(
        f"> This {'directory' if is_dir else 'file'} was **moved out of the repository**, not deleted."
    )
    lines.append(f"> Archived **{datetime.date.today().isoformat()}**.")
    lines.append("")
    lines.append(
        f"**Reason:** {meta.get('reason', 'bulky artifact, reproducible from upstream')}"
    )
    lines.append("")
    if collision_note:
        lines.append(collision_note)
        lines.append("")
    lines.append("## Identity")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| Original repo path | `{rel}` |")
    lines.append(f"| Archived to | `{dest}` |")
    lines.append(f"| Type | {'directory' if is_dir else 'file'} |")
    lines.append(f"| Size | {size_str(meta['bytes'])} |")
    if not is_dir:
        lines.append(f"| SHA-256 | `{meta['sha256']}` |")
    else:
        lines.append(f"| File count | {meta.get('nfiles', '?')} |")
    lines.append(f"| Last modified (mtime) | {meta['mtime']} |")
    for k, label in (
        ("repo", "Upstream repository"),
        ("commit", "Commit"),
        ("author", "Author / committer"),
        ("committed", "Commit date"),
        ("license", "License"),
        ("path_in_repo", "Path within upstream repo"),
    ):
        if src.get(k):
            v = f"`{src[k]}`" if k in ("commit", "path_in_repo") else src[k]
            lines.append(f"| {label} | {v} |")
    lines.append("")
    if meta.get("notes"):
        lines.append("## Why this matters / what is in it")
        lines.append("")
        for n in meta["notes"]:
            lines.append(f"- {n}")
        lines.append("")
    if meta.get("verification"):
        lines.append("## Upstream-equivalence check")
        lines.append("")
        lines.append(meta["verification"])
        lines.append("")
    if is_dir and files:
        lines.append("## Contents")
        lines.append("")
        lines.append("| File | Bytes | SHA-256 |")
        lines.append("|---|---:|---|")
        for f, b, s in files:
            lines.append(f"| `{f}` | {b:,} | `{s}` |")
        lines.append("")
    lines.append("## How to get it back")
    lines.append("")
    u = urls(src, rel, is_dir)
    if u:
        lines.append("Independent recovery URLs, most reliable first:")
        lines.append("")
        for desc, link in u:
            lines.append(f"- {desc}:  \n  <{link}>")
        lines.append("")
    lines.append("Restore from the local archive:")
    lines.append("")
    lines.append("```bash")
    lines.append(f'mv "{dest}" \\')
    lines.append(f'   "{rel}"')
    lines.append("```")
    lines.append("")
    if not is_dir and u:
        lines.append("Or re-download and verify:")
        lines.append("")
        lines.append("```bash")
        lines.append(f'curl -fsSL "{u[0][1]}" -o "{name}"')
        lines.append(f'echo "{meta["sha256"]}  {name}" | sha256sum -c -')
        lines.append("```")
        lines.append("")
    lines.append("If every URL above is dead, try the Wayback Machine:")
    lines.append("")
    if u:
        lines.append(f"    https://web.archive.org/web/2/{u[0][1]}")
    lines.append("")
    return "\n".join(lines) + "\n"


def verify_mode(repo_root, items):
    """Re-hash every archived entry named by the manifest and report drift.

    Reads the `Archived to` path out of each placeholder rather than recomputing
    it, so it catches placeholders left pointing at a path that later moved or
    was replaced.
    """
    ok = miss = drift = 0
    for it in items:
        rel = it["path"]
        full = os.path.join(repo_root, rel)
        ph = os.path.normpath(
            full + (".ARCHIVED.md" if not os.path.isdir(full)
                    else "/../" + os.path.basename(rel) + ".ARCHIVED.md"))
        if not os.path.exists(ph):
            print(f"NO PLACEHOLDER  {rel}")
            miss += 1
            continue
        text = open(ph).read()
        m = re.search(r"\| Archived to \| `([^`]+)`", text)
        if not m:
            print(f"PLACEHOLDER HAS NO PATH  {ph}")
            miss += 1
            continue
        dest = os.path.expanduser(m.group(1))
        if not os.path.exists(dest):
            print(f"TARGET MISSING  {rel}\n    -> {dest}")
            miss += 1
            continue
        fp, n = fingerprint(dest)
        recorded = re.search(r"\| SHA-256 \| `([0-9a-f]{64})`", text)
        if recorded and os.path.isfile(dest):
            if recorded.group(1) != fp:
                print(f"HASH DRIFT  {rel}\n    recorded {recorded.group(1)[:16]}…"
                      f"  actual {fp[:16]}…")
                drift += 1
                continue
        ok += 1
    print(f"\nverified {ok}, missing {miss}, drifted {drift}")
    return 1 if (miss or drift) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true",
                    help="Verify existing placeholders resolve to real archive "
                         "content and re-hash it. Makes no changes.")
    a = ap.parse_args()
    items = json.load(open(a.manifest))
    total = 0
    verified = 0
    failures = []

    if a.verify:
        return verify_mode(a.repo_root, items)
    for it in items:
        rel = it["path"]
        full = os.path.join(a.repo_root, rel)
        if not os.path.exists(full):
            print(f"SKIP (missing) {rel}")
            continue
        is_dir = os.path.isdir(full)
        b = du(full)
        meta = {
            "bytes": b,
            "mtime": datetime.datetime.utcfromtimestamp(
                os.path.getmtime(full)
            ).strftime("%Y-%m-%d %H:%M:%SZ"),
            "reason": it.get("reason"),
        }
        files = None
        if is_dir:
            files = []
            for dp, _, fs in os.walk(full):
                for f in sorted(fs):
                    p = os.path.join(dp, f)
                    files.append(
                        (os.path.relpath(p, full), os.path.getsize(p), sha256(p))
                    )
            meta["nfiles"] = len(files)
        else:
            meta["sha256"] = sha256(full)
        dest = os.path.join(ARCHIVE, rel)
        ph = full + (
            ".ARCHIVED.md"
            if not is_dir
            else "/../" + os.path.basename(rel) + ".ARCHIVED.md"
        )
        ph = os.path.normpath(ph)
        print(f"{'DRY ' if a.dry_run else ''}ARCHIVE {size_str(b):>22}  {rel}")
        total += b
        if a.dry_run:
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        src_fp, src_n = fingerprint(full)
        collision_note = None

        if os.path.exists(dest):
            # NEVER destroy an existing archive entry. A previous pass may have
            # archived something *nested inside* this path (e.g. PANEL/foo-backups
            # archived first, then PANEL/ archived wholesale). Blowing it away
            # silently orphans that earlier placeholder and loses the only copy.
            dst_fp, dst_n = fingerprint(dest)
            if src_fp == dst_fp:
                # Identical bytes already archived. Do not duplicate — just drop
                # the working-tree copy and point the placeholder at what is there.
                print(f"  = already archived, identical content ({src_n} file(s), "
                      f"fingerprint {src_fp[:16]}…) — not duplicating")
                if os.path.isdir(full):
                    shutil.rmtree(full)
                else:
                    os.remove(full)
                collision_note = (
                    f"An identical copy was already present in the archive "
                    f"(content fingerprint `{src_fp[:16]}…`, {src_n} file(s)), so this "
                    f"pass did not create a second copy."
                )
                with open(ph, "w") as f:
                    f.write(placeholder(rel, dest, meta, it.get("source", {}),
                                        is_dir, files, collision_note))
                continue
            # Genuine conflict: same path, different content. Keep both.
            only_a, only_b, diff = compare_trees(dest, full)
            stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            alt = f"{dest}.conflict-{stamp}"
            print(f"  ! CONFLICT: archive path exists with DIFFERENT content\n"
                  f"      existing: {dest}  ({dst_n} file(s), {dst_fp[:16]}…)\n"
                  f"      incoming: {full}  ({src_n} file(s), {src_fp[:16]}…)\n"
                  f"      only in existing: {len(only_a)} | only in incoming: {len(only_b)} | differing: {len(diff)}")
            for k in (only_a[:5] + only_b[:5] + diff[:5]):
                print(f"        - {k}")
            print(f"      storing incoming at: {alt}\n"
                  f"      REVIEW: merge, and fix any placeholder pointing at the old path")
            collision_note = (
                f"⚠ **Archive path collision.** `{dest}` already existed with **different** "
                f"content (existing fingerprint `{dst_fp[:16]}…`, {dst_n} file(s); this copy "
                f"`{src_fp[:16]}…`, {src_n} file(s)). Differences: {len(only_a)} only in the "
                f"existing copy, {len(only_b)} only in this one, {len(diff)} present in both but "
                f"differing. **Both copies were kept** — this one is at the path below."
            )
            dest = alt

        shutil.move(full, dest)

        # Verify the move preserved content.
        moved_fp, moved_n = fingerprint(dest)
        if moved_fp != src_fp:
            print(f"  !! VERIFY FAILED after move: {rel}\n"
                  f"       expected {src_fp[:16]}… ({src_n} files)\n"
                  f"       got      {moved_fp[:16]}… ({moved_n} files)")
            failures.append(rel)
        else:
            verified += 1

        with open(ph, "w") as f:
            f.write(placeholder(rel, dest, meta, it.get("source", {}), is_dir,
                                files, collision_note))
    print(f"\nTOTAL {'would be ' if a.dry_run else ''}archived: {size_str(total)}")
    if not a.dry_run:
        print(f"Verified after move: {verified}/{verified + len(failures)}")
        if failures:
            print("!! VERIFICATION FAILURES:")
            for f in failures:
                print("   ", f)
            print("   The archive copy does NOT match what left the repository.")
    print(f"Archive root: {ARCHIVE}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
