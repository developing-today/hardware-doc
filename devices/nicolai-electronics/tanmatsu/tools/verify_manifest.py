#!/usr/bin/env python3
"""Verify-only check of acquisition/manifest.json. Suitable for CI / post-clone.
Exit 0 = all good, 1 = mismatch or missing. Executed 2026-08-24."""
import hashlib,json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m=json.load(open(os.path.join(ROOT,"acquisition","manifest.json")))
bad=miss=0
for f in m["files"]:
    p=os.path.join(ROOT,f["path"])
    if not os.path.exists(p): print("MISSING",f["path"]); miss+=1; continue
    h=hashlib.sha256()
    with open(p,"rb") as fh:
        for c in iter(lambda: fh.read(1<<20),b""): h.update(c)
    if h.hexdigest()!=f["sha256"]: print("MISMATCH",f["path"]); bad+=1
print(f"{len(m['files'])} files: {len(m['files'])-bad-miss} ok, {bad} mismatched, {miss} missing")
sys.exit(1 if (bad or miss) else 0)
