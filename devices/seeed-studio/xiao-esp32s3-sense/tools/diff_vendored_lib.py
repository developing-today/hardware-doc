#!/usr/bin/env python3
"""Determine whether a vendored dependency is an unmodified upstream snapshot
or a patched fork — and, if it differs, capture the delta as a small patch file
*before* the bulky tree is archived.

Motivation (2026-08-24): a vendored library that merely lags upstream is
disposable — you can re-fetch a tagged release. A vendored library that carries
local edits by the board maker or project author is **irreplaceable**, and the
edits are frequently the most interesting thing in the tree (a pin remap, a
timing fix, a patched root CA). Deleting it loses information that exists
nowhere else. This tool tells the two cases apart and, in both cases, leaves a
unified diff behind that is a few kilobytes instead of a few megabytes.

Usage:
  diff_vendored_lib.py --vendored <dir-or-zip> --upstream-repo owner/name
                       [--upstream-ref master] [--out <file.patch>]
                       [--strip-root]

Emits: a unified diff (`diff -ruN`) plus a machine-readable summary header.
Exit status 0 = identical, 1 = differs, 2 = error.
"""

import argparse, io, json, os, shutil, subprocess, sys, tempfile, urllib.request, zipfile, hashlib, datetime

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


def fetch_zip(repo, ref, dest):
    for url in (
        f"https://codeload.github.com/{repo}/zip/refs/heads/{ref}",
        f"https://codeload.github.com/{repo}/zip/refs/tags/{ref}",
        f"https://codeload.github.com/{repo}/zip/{ref}",
    ):
        try:
            b = urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=180
            ).read()
        except Exception:
            continue
        zipfile.ZipFile(io.BytesIO(b)).extractall(dest)
        return url, hashlib.sha256(b).hexdigest(), len(b)
    raise SystemExit(f"could not fetch {repo}@{ref}")


def only_child(d):
    e = [x for x in os.listdir(d) if not x.startswith("__MACOSX")]
    return (
        os.path.join(d, e[0])
        if len(e) == 1 and os.path.isdir(os.path.join(d, e[0]))
        else d
    )


def prep_vendored(p, tmp):
    if p.endswith(".zip"):
        d = os.path.join(tmp, "vend")
        zipfile.ZipFile(p).extractall(d)
        return only_child(d)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vendored", required=True)
    ap.add_argument("--upstream-repo", required=True)
    ap.add_argument("--upstream-ref", default="master")
    ap.add_argument("--out")
    a = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="vendcmp-")
    try:
        v = prep_vendored(a.vendored, tmp)
        up = os.path.join(tmp, "up")
        url, zsha, zlen = fetch_zip(a.upstream_repo, a.upstream_ref, up)
        u = only_child(up)

        r = subprocess.run(["diff", "-ruN", u, v], capture_output=True, text=True)
        body = r.stdout
        # normalise the temp paths out of the diff headers
        body = body.replace(u, f"a/{os.path.basename(a.vendored)}")
        body = body.replace(v, f"b/{os.path.basename(a.vendored)}")

        changed, added, removed = set(), set(), set()
        for line in body.splitlines():
            if line.startswith("diff -ruN "):
                changed.add(line.split()[-1])
            elif line.startswith("Only in "):
                (
                    added
                    if "/b/" in line
                    or line.split()[2].rstrip(":").endswith(os.path.basename(v))
                    else removed
                ).add(line)

        identical = not body.strip()
        hdr = [
            "# Vendored-dependency delta report",
            "#",
            f"# vendored copy   : {a.vendored}",
            f"# upstream        : {a.upstream_repo} @ {a.upstream_ref}",
            f"# upstream source : {url}",
            f"# upstream zip    : {zlen:,} bytes, sha256 {zsha}",
            f"# compared        : {datetime.date.today().isoformat()}",
            f"# verdict         : {'IDENTICAL to upstream' if identical else 'DIFFERS from upstream'}",
            f"# files differing : {len(changed)}",
            "#",
            "# NOTE: a non-empty diff does not by itself prove local modification.",
            "#       Upstream moves; the vendored copy may simply be an older",
            "#       snapshot. Read the hunks before concluding it is a fork.",
            "#",
        ]
        out = "\n".join(hdr) + "\n" + body
        if a.out:
            os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
            open(a.out, "w").write(out)
            print(
                f"{'identical' if identical else 'DIFFERS':>10}  {len(changed):>2} files  "
                f"{len(out):>8,} B patch  {a.out}"
            )
        else:
            sys.stdout.write(out)
        return 0 if identical else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
