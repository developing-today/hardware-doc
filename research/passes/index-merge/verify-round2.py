#!/usr/bin/env python3
"""Round-two verification checks, re-run 2026-09-11.

Round one's numbers are NOT copied — every figure below is measured now.

  * relative-link integrity across all authored Markdown
  * typed-artifact magic-byte validation
  * device-record orphans (no inbound link from devices/README.md)
  * placeholder completeness for archived artifacts
  * counts: authored files, device records, component records, vendor guides
"""
import os, re, json, collections, sys

SKIP_DIRS = {'.git', 'archive', 'scratch', 'node_modules'}
MAGIC = {'.pdf': [b'%PDF'], '.zip': [b'PK'], '.png': [b'\x89PNG'],
         '.jpg': [b'\xff\xd8\xff'], '.jpeg': [b'\xff\xd8\xff'],
         '.gz': [b'\x1f\x8b'], '.tgz': [b'\x1f\x8b'], '.webp': [b'RIFF']}

def walk(top='.', skip_artifacts=True):
    for root, dirs, files in os.walk(top):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not os.path.islink(os.path.join(root, d))]
        if skip_artifacts and ('/artifacts' in root or root.endswith('/artifacts')):
            continue
        for f in files:
            yield os.path.join(root, f)

# ---------------------------------------------------------------- links
mds = [p for p in walk() if p.endswith('.md')]
LINK = re.compile(r'\[[^\]]*\]\(\s*<?([^)\s>]+)>?\s*(?:"[^"]*")?\)')
total = broken = 0
brokenlist = []
for m in mds:
    s = open(m, encoding='utf-8', errors='replace').read()
    s = re.sub(r'```.*?```', '', s, flags=re.S)
    s = re.sub(r'`[^`\n]*`', '', s)
    for u in LINK.findall(s):
        if u.startswith(('http://', 'https://', 'mailto:', '#')): continue
        u = u.split('#')[0]
        if not u: continue
        from urllib.parse import unquote
        u = unquote(u)
        total += 1
        t = os.path.normpath(os.path.join(os.path.dirname(m), u))
        if not os.path.exists(t):
            broken += 1; brokenlist.append((m, u))
print(f"relative links checked : {total:,}   broken: {broken}")
for m, u in brokenlist[:20]: print(f"    BROKEN  {m} -> {u}")

# ------------------------------------------------------------- artifacts
n = bad = 0
badlist = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not os.path.islink(os.path.join(root, d))]
    for f in files:
        e = os.path.splitext(f)[1].lower()
        if e not in MAGIC: continue
        p = os.path.join(root, f)
        try: head = open(p, 'rb').read(8)
        except OSError: continue
        n += 1
        if not any(head.startswith(x) for x in MAGIC[e]):
            bad += 1; badlist.append(p)
print(f"typed artifacts validated: {n:,}   magic-byte mismatches: {bad}")
for p in badlist[:10]: print("    MISMATCH", p)

# --------------------------------------------------------------- orphans
devidx = open('devices/README.md', encoding='utf-8').read()
recs = sorted({os.path.dirname(p) for p in walk('devices')
               if os.path.basename(p) == 'README.md'
               and len(os.path.relpath(os.path.dirname(p), 'devices').split(os.sep)) == 2})
orph = [r for r in recs if os.path.relpath(r, 'devices') not in devidx]
print(f"device records: {len(recs)}   orphans (no link from devices/README.md): {len(orph)}")
for r in orph: print("    ORPHAN", r)

# ---------------------------------------------------------- placeholders
ph = [p for p in walk('.', skip_artifacts=False) if p.endswith('.ARCHIVED.md')]
# Test SUBSTANCE, not field labels: earlier passes used different table headings
# ("Original repository path" vs "Original repo path"), which is not a defect.
inc = []
for p in ph:
    s = open(p, encoding='utf-8', errors='replace').read()
    urls = len({u for u in re.findall(r'https?://[^\s<>)`"\']+', s)})
    has_hash = bool(re.search(r'\b[0-9a-f]{64}\b', s))
    has_size = bool(re.search(r'(?i)(bytes?|size)', s)) and bool(re.search(r'\d[\d ,_]{2,}', s))
    has_path = bool(re.search(r'(?i)(original|former).{0,24}path', s))
    if not (has_hash and has_size and has_path and urls >= 2):
        inc.append((p, urls, has_hash, has_size, has_path))
print(f"archive placeholders: {len(ph)}   "
      f"incomplete (no hash / no size / no original path / <2 distinct URLs): {len(inc)}")
for t in inc[:10]: print(f"    INCOMPLETE {t}")

# -------------------------------------------------------------- counts
comp = sorted({os.path.dirname(p) for p in walk('components')
               if os.path.basename(p) == 'README.md'
               and 2 <= len(os.path.relpath(os.path.dirname(p), 'components').split(os.sep)) <= 3
               and not os.path.exists(os.path.join(os.path.dirname(p), '..', 'README.md'))
               or (os.path.basename(p) == 'README.md'
                   and len(os.path.relpath(os.path.dirname(p), 'components').split(os.sep)) == 2)})
vend = sorted({os.path.dirname(p) for p in walk('vendors')
               if os.path.basename(p) == 'README.md'
               and len(os.path.relpath(os.path.dirname(p), 'vendors').split(os.sep)) == 1})
print(f"component records: {len(comp)}")
print(f"vendor guides    : {len(vend)}")
print(f"authored .md files (excl artifacts/, archive/, scratch/): {len(mds):,}")
cert = [p for p in walk('devices')] + [p for p in walk('components')]
print(f"certification-and-compliance.md records: "
      f"{len([p for p in cert if os.path.basename(p)=='certification-and-compliance.md'])}")
print(f"schematic-netlist.md records: "
      f"{len([p for p in cert if os.path.basename(p)=='schematic-netlist.md'])}")
allart = [p for p in walk('.', skip_artifacts=False) if '/artifacts/' in p and not p.endswith('.md')]
print(f"binary artifacts under artifacts/: {len(allart):,}")
