#!/usr/bin/env python3
"""Reacquire and verify the XIAO ESP32S3 Sense artifact set from manifest.json.

Driven ONLY by manifest.json - no URLs are hardcoded here. Downloads to a
temporary file, validates HTTP status, content magic, byte size and SHA-256,
then installs atomically. Idempotent: existing files are verified, not refetched.

  ./download.py                 # fetch anything missing, verify the rest
  ./download.py --verify-only   # check what is on disk; no network (CI-safe)
  ./download.py --force         # refetch everything

Never commits and never stages. Exit status 0 = all good, 1 = problems.
Written 2026-08-24.
"""
import argparse, hashlib, json, os, sys, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEVICE_ROOT = os.path.dirname(HERE)
MANIFEST = os.path.join(HERE, "manifest.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

MAGIC = {".pdf": b"%PDF", ".zip": b"PK\x03\x04", ".xlsx": b"PK\x03\x04"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def local_path(entry):
    # manifest destinations are repo-root-relative; map back to the device dir
    d = entry["destination"]
    marker = "xiao-esp32s3-sense/"
    return os.path.join(DEVICE_ROOT, d.split(marker, 1)[1] if marker in d else d)


def check_magic(path):
    ext = os.path.splitext(path)[1].lower()
    want = MAGIC.get(ext)
    if not want:
        return True, ""
    with open(path, "rb") as f:
        head = f.read(len(want))
    if head != want:
        return False, f"bad magic {head!r}, expected {want!r} (an HTML error page saved as {ext}?)"
    return True, ""


def verify(path, entry):
    if not os.path.exists(path):
        return False, "missing"
    size = os.path.getsize(path)
    if size != entry["bytes"]:
        return False, f"size {size:,} != expected {entry['bytes']:,}"
    ok, why = check_magic(path)
    if not ok:
        return False, why
    got = sha256(path)
    if got != entry["sha256"]:
        return False, f"sha256 {got[:16]}… != expected {entry['sha256'][:16]}…"
    return True, "ok"


def fetch(entry, path):
    url = entry["url"]
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError(f"refusing non-http scheme: {url}")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=300) as r:
        if r.status != 200:
            raise IOError(f"HTTP {r.status}")
        data = r.read()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        ok, why = verify(tmp, entry)
        if not ok:
            raise IOError(f"validation failed after download: {why}")
        os.replace(tmp, path)          # atomic install
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-only", action="store_true", help="no network; check local files")
    ap.add_argument("--force", action="store_true", help="refetch even if valid")
    a = ap.parse_args()

    man = json.load(open(MANIFEST))
    arts = man["artifacts"]
    acquired = cached = failed = 0
    problems = []

    for e in arts:
        if e.get("disposition") == "archived":
            # moved out of the repo on purpose; a placeholder records hash + reacquisition.
            # Not an error, and not re-fetched by default.
            cached += 1
            continue

        if e.get("disposition") == "deduplicated":
            # byte-identical to another retained artifact; a *.DUPLICATE.md
            # pointer stands in its place. Nothing to fetch or verify.
            cached += 1
            continue

        p = local_path(e)
        rel = os.path.relpath(p, DEVICE_ROOT)
        ok, why = verify(p, e)

        if ok and not a.force:
            cached += 1
            continue
        if a.verify_only:
            failed += 1
            problems.append((rel, why))
            print(f"FAIL   {rel}: {why}")
            continue
        try:
            fetch(e, p)
            acquired += 1
            print(f"GOT    {rel}")
        except Exception as ex:
            failed += 1
            problems.append((rel, str(ex)[:120]))
            print(f"FAIL   {rel}: {str(ex)[:120]}")

    print(f"\n{len(arts)} artifacts: {cached} verified, {acquired} acquired, {failed} failed")
    if problems:
        print("\nProblems:")
        for rel, why in problems:
            print(f"  {rel}: {why}")
        print("\nNote: several artifacts have restrictive or unknown redistribution terms")
        print("(see manifest.json 'review_required'). Their absence may be intentional.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
