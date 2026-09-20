#!/usr/bin/env python3
"""Replace an exact-duplicate file with a small Markdown pointer to the retained copy.

Content-identical files waste space and, worse, create ambiguity about which is
canonical. Rather than delete silently, leave a note naming the surviving copy,
the shared SHA-256, and where the duplicate originally came from.
Executed 2026-08-24."""
import hashlib,os,sys,datetime

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()

def main():
    # argv: <keep> <dup> <why>
    keep,dup,why=sys.argv[1],sys.argv[2],sys.argv[3]
    a,b=sha(keep),sha(dup)
    if a!=b:
        print(f"REFUSING: not identical\n  {keep} {a}\n  {dup} {b}"); return 2
    rel=os.path.relpath(keep,os.path.dirname(dup))
    n=os.path.getsize(dup)
    open(dup+'.DUPLICATE.md','w').write(f"""# Duplicate removed: `{os.path.basename(dup)}`

> Content-identical to another file already in this repository. The bytes were
> **not** unique, so this copy was removed on {datetime.date.today().isoformat()} and replaced by this pointer.

| Field | Value |
|---|---|
| Canonical copy | [`{rel}`]({rel}) |
| Repo path of canonical copy | `{os.path.relpath(keep)}` |
| Shared SHA-256 | `{a}` |
| Size | {n:,} bytes |
| Why this copy existed | {why} |

Restore it, if you ever need the file at this exact path:

```bash
cp "{rel}" "{os.path.basename(dup)}"
```

Verify:

```bash
echo "{a}  {os.path.basename(dup)}" | sha256sum -c -
```
""")
    os.remove(dup)
    print(f"deduped {dup}  ->  pointer to {os.path.relpath(keep)}  ({n:,} B reclaimed)")
    return 0
sys.exit(main())
