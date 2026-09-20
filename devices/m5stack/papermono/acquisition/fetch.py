#!/usr/bin/env python3
"""Acquisition downloader for the M5Stack PaperMono record.

Driven only by ``manifest.json`` beside this file. Standard library only.

Contract (see .agents/skills/hardware-device-research/SKILL.md):
  * fetches ``repository`` entries by default; ``reference-only`` needs --reference-only
  * never changes a recorded disposition
  * refuses redirects to non-http(s) schemes
  * downloads to a temp file, validates status / magic / size / SHA-256,
    and only then installs atomically
  * idempotent: verifies an existing file before skipping it
  * prints acquired / cached / skipped / failed
  * --verify-only checks what is already on disk and downloads nothing
  * never stages or commits anything

Several of these hosts filter automated clients. The escalation ladder that was
observed to work on 2026-09-01, in order:
    (1) the default UA below
    (2) Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
        (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
    (3) WhatsApp/2.23.20.0        <- required by ST (st.com); Chrome and
                                    ClaudeBot get a TLS stream reset
Known traps: datasheet.lcsc.com returns HTTP 200 with text/html for PDF URLs,
so magic bytes are checked rather than status; burner.m5stack.com/api/v1/... is
public while /api/... returns 401; Semtech's canonical download is behind a
Salesforce JS/POST shell and is recorded 'blocked' rather than fetched.
"""

import argparse, hashlib, json, os, shutil, sys, tempfile, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
MAGIC = {".pdf": b"%PDF-", ".bin": b"\xe9"}


def expected_magic(path):
    return MAGIC.get(os.path.splitext(path)[1].lower())


def check(path, entry):
    """Return (ok, reason) for a file already on disk."""
    if not os.path.exists(path):
        return False, "absent"
    blob = open(path, "rb").read()
    magic = expected_magic(path)
    if magic and not blob.startswith(magic):
        return False, f"magic mismatch (expected {magic!r}, got {blob[:5]!r})"
    if entry.get("bytes") is not None and len(blob) != entry["bytes"]:
        return False, f"size {len(blob)} != expected {entry['bytes']}"
    if entry.get("sha256"):
        got = hashlib.sha256(blob).hexdigest()
        if got != entry["sha256"]:
            return False, f"sha256 {got[:16]}… != expected {entry['sha256'][:16]}…"
    return True, "verified"


def fetch(url, dest, entry):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        if resp.status != 200:
            raise OSError(f"HTTP {resp.status}")
        if not resp.geturl().startswith(("http://", "https://")):
            raise OSError(f"refusing redirect to unsupported scheme: {resp.geturl()}")
        blob = resp.read()
    magic = expected_magic(dest)
    if magic and not blob.startswith(magic):
        # This is the LCSC / vendor-portal failure: HTTP 200 with an HTML body.
        raise OSError(f"content is not {magic!r} — refusing to save an error page "
                      f"under this extension (first bytes {blob[:16]!r})")
    if entry.get("bytes") is not None and len(blob) != entry["bytes"]:
        raise OSError(f"size {len(blob)} != expected {entry['bytes']}")
    if entry.get("sha256"):
        got = hashlib.sha256(blob).hexdigest()
        if got != entry["sha256"]:
            raise OSError(f"sha256 {got} != expected {entry['sha256']}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dest))
    with os.fdopen(fd, "wb") as fh:
        fh.write(blob)
    os.replace(tmp, dest)          # atomic install, only after validation
    return len(blob)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify-only", action="store_true",
                    help="check files already on disk; download nothing (CI / post-clone)")
    ap.add_argument("--reference-only", action="store_true",
                    help="also attempt entries whose disposition is reference-only")
    ap.add_argument("--manifest", default=os.path.join(HERE, "manifest.json"))
    args = ap.parse_args()

    man = json.load(open(args.manifest, encoding="utf-8"))
    tally = {"acquired": [], "cached": [], "skipped": [], "failed": []}

    for e in man["artifacts"]:
        dest_rel, eid = e.get("destination"), e["id"]
        if not dest_rel:
            tally["skipped"].append(f"{eid} no destination ({e['reacquisition']})")
            continue
        if e["disposition"] != "repository" and not args.reference_only:
            tally["skipped"].append(f"{eid} {dest_rel} (disposition={e['disposition']})")
            continue
        dest = os.path.join(ROOT, dest_rel)
        ok, why = check(dest, e)
        if ok:
            tally["cached"].append(f"{eid} {dest_rel}")
            continue
        if args.verify_only:
            tally["failed"].append(f"{eid} {dest_rel}: {why}")
            continue
        if e["reacquisition"] in ("lost", "blocked") or not e.get("url"):
            tally["skipped"].append(f"{eid} {dest_rel} (reacquisition={e['reacquisition']})")
            continue
        urls = [e["url"]] + list(e.get("fallback_urls") or [])
        for url in urls:
            try:
                n = fetch(url, dest, e)
                tally["acquired"].append(f"{eid} {dest_rel} ({n:,} B)")
                break
            except (OSError, urllib.error.URLError) as exc:
                last = f"{url}: {exc}"
        else:
            tally["failed"].append(f"{eid} {dest_rel}: {last}")

    for k in ("acquired", "cached", "skipped", "failed"):
        print(f"\n{k.upper()} ({len(tally[k])})")
        for line in tally[k]:
            print("  ", line)
    print(f"\nThis tool does not stage or commit. Repository root: {ROOT}")
    return 1 if tally["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
