#!/usr/bin/env python3
"""Relocate bulky/duplicate artifacts out of the repository without losing them.

Policy (per user instruction, 2026-08-24): never delete a downloaded artifact.
Move it into the archive (resolved from the git common dir, namespaced by repo)
preserving its relative path, and leave a
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

def _repo_root():
    """Real repository root, worktree-safe (--git-common-dir, not --show-toplevel)."""
    out = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("not inside a git repository")
    return os.path.dirname(out.stdout.strip())


# Resolve the archive rather than hardcoding it. Layout:
#
#   <repo-parent>/
#   |- <repo>/                     this repository
#   \- repo-archive/       shared archive
#      |- <repo>/                  <- our namespace, mirrors in-repo paths
#      \- scratch/<repo>/          <- working files
#
# Namespacing by source repository means a second repo's material sits beside ours
# instead of colliding. Overridable for testing.
REPO_ROOT = _repo_root()
NAMESPACE = os.path.basename(REPO_ROOT)
ARCHIVE_ROOT = os.environ.get(
    "REPO_ARCHIVE_ROOT",
    os.path.join(os.path.dirname(REPO_ROOT), "repo-archive"))
ARCHIVE = os.path.join(ARCHIVE_ROOT, NAMESPACE)
SCRATCH = os.path.join(ARCHIVE_ROOT, "scratch", NAMESPACE)


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
    # First-class multi-URL list. Not everything archived is a git repo - vendor
    # datasheets, forum attachments and archive.org captures have no commit to
    # derive a URL from, so they must be listed explicitly. Each entry is either a
    # bare string or {"url": ..., "desc": ...}.
    for key in ("urls", "extra_urls"):
        for u in src.get(key) or []:
            if isinstance(u, dict):
                out.append((u.get("desc") or "additional source", u["url"]))
            else:
                out.append(("additional source", u))
    # De-duplicate while preserving order; the same link often arrives from two
    # places (derived from repo+commit, and listed by hand).
    seen, uniq = set(), []
    for desc, link in out:
        if link not in seen:
            seen.add(link)
            uniq.append((desc, link))
    return uniq


# Git reads these as configuration rather than content. A symlinked .gitignore makes
# git print "Too many levels of symbolic links" on every command, and would let a
# vendored upstream's ignore rules bleed into this repo.
NO_LINK_NAMES = {".gitignore", ".gitattributes", ".gitmodules"}


def stand_in(rel, full):
    """Symlink `rel` to its archive copy, plus a matching *.ARCHIVED.link.

    The target is relative and routes through this repo's own `archive/` symlink -
    `../../../archive/devices/foo/bar` - never at the archive root directly. That
    leaves one indirection point: relocating the archive means editing a single
    symlink rather than every artifact link in the tree.
    """
    if os.path.basename(rel) in NO_LINK_NAMES:
        return
    depth = len(os.path.dirname(rel).split(os.sep)) if os.path.dirname(rel) else 0
    target = os.path.join(*([".."] * depth), "archive", rel) if depth else os.path.join("archive", rel)
    try:
        if os.path.lexists(full):
            if not os.path.islink(full):
                return          # something real is there; do not clobber it
            os.unlink(full)
        os.symlink(target, full)
        link = full + ".ARCHIVED.link"
        if os.path.lexists(link):
            os.unlink(link)
        os.symlink(os.path.basename(full), link)
    except OSError as e:
        print(f"  !! could not create stand-in symlink for {rel}: {e}")


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
    # Git-sourced material is only half of what gets archived. Vendor PDFs have a
    # version and a publication date but no commit or author, and are usually the
    # hard ones to re-obtain - so difficulty and access notes matter more for them
    # than a hash does. Render whatever the manifest supplies; omit the rest.
    for k, label in (
        ("repo", "Upstream repository"),
        ("commit", "Commit"),
        ("tag", "Tag / release"),
        ("version", "Document version"),
        ("author", "Author / committer"),
        ("committed", "Commit date"),
        ("published", "Published / revised"),
        ("retrieved", "Retrieved"),
        ("license", "License"),
        ("path_in_repo", "Path within upstream repo"),
        ("difficulty", "Difficulty to re-obtain"),
        ("access_notes", "Access notes"),
    ):
        if src.get(k):
            v = f"`{src[k]}`" if k in ("commit", "path_in_repo", "tag", "version") else src[k]
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
    # A patch-over-upstream artifact is meaningless without its base. State the
    # relationship on EVERY placeholder derived from it, not once in a README:
    # placeholders are read one at a time, usually by someone who found only this file.
    base = src.get("base")
    if base:
        lines.append("## Derived from a common base")
        lines.append("")
        lines.append(
            "This artifact is **not standalone** - it is a modification of the source below. "
            "Re-acquiring it means obtaining that base and re-applying the changes."
        )
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("| --- | --- |")
        # `repo` accepts a string or a list. Upstreams move, get forked, or are
        # mirrored - a vendor repo that also lives on GitLab, or a project whose
        # canonical home changed owner - and one dead URL should not strand the base.
        repos = base.get("repo") or []
        if isinstance(repos, str):
            repos = [repos]
        for i, r in enumerate(repos):
            label = "Base repository" if i == 0 else "Mirror / fork"
            url = r if r.startswith("http") else f"https://github.com/{r}"
            lines.append(f"| {label} | [`{r}`]({url}) |")
        if len(repos) > 1:
            lines.append(f"| Repository count | {len(repos)} known locations |")
        for k, label in (("commit", "Base commit"),
                         ("tag", "Base tag / release"), ("url", "Base URL"),
                         ("note", "Relationship")):
            if base.get(k):
                v = f"`{base[k]}`" if k in ("commit", "tag") else base[k]
                lines.append(f"| {label} | {v} |")
        lines.append("")
        if base.get("patches"):
            lines.append("Patches applied over that base, in order:")
            lines.append("")
            for i, pt in enumerate(base["patches"], 1):
                if isinstance(pt, dict):
                    lines.append(f"{i}. {pt.get('desc', '(undescribed)')}"
                                 + (f" - `{pt['path']}`" if pt.get("path") else ""))
                else:
                    lines.append(f"{i}. {pt}")
            lines.append("")
        if base.get("siblings"):
            lines.append("Other archived artifacts sharing this base:")
            lines.append("")
            for sib in base["siblings"]:
                lines.append(f"- `{sib}`")
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
    # Two independent URLs is the target: one host disappearing should not strand
    # the artifact. Sometimes only one exists, or none - say so explicitly rather
    # than leaving a silent gap that reads like an oversight.
    if len(u) < 2:
        lines.append(
            f"> **Only {len(u) or 'no'} recovery URL{'' if len(u) == 1 else 's'} "
            "recorded.** Two or more independent sources are the target. If you find "
            "another - a mirror, a vendor page, an archive.org capture - add it here."
        )
        lines.append("")
    # Bulk archiving cannot always establish per-file provenance. That is acceptable
    # only if the detail lives somewhere findable, and the placeholder names it.
    if src.get("documented_in"):
        lines.append(f"Fuller sourcing for this artifact is recorded in "
                     f"`{src['documented_in']}`.")
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
    thin_urls = []

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
            "mtime": datetime.datetime.fromtimestamp(
                os.path.getmtime(full), datetime.timezone.utc
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

        # Leave a symlink standing in for the artifact at its original path, so a
        # checkout holding the archive behaves as though nothing moved: relative
        # references from KiCad projects and build scripts keep resolving, and the
        # directory still shows that the file exists. Without this, an archived file
        # vanishes from the tree and is discoverable only via the placeholder.
        stand_in(rel, full)

        # Two independent sources is the bar: one host going away should not strand
        # the artifact. Warn loudly at archive time, when the person still has the
        # context to fix it - not months later when the link has rotted.
        nurl = len(urls(it.get("source", {}), rel, is_dir))
        if nurl < 2:
            thin_urls.append((rel, nurl))
            print(f"  !! only {nurl} recovery URL(s) for {rel}\n"
                  f"       add more to the manifest's source.urls[], or record in the "
                  f"directory's ARCHIVED-*.md why no second source exists")
    if thin_urls:
        print(f"\n!! {len(thin_urls)} artifact(s) archived with fewer than two recovery URLs:")
        for r, n in thin_urls:
            print(f"     [{n}] {r}")
        print("   These are the ones that go missing. Add sources before they rot.")

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
