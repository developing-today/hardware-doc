"""Reassemble per-glyph PDF text runs into words/lines.

Altium's PDF publisher emits one Tj per glyph with its own Tm, so the raw
extraction is a bag of single characters. Group by baseline y (rounded to a
tolerance), sort by x, and join glyphs whose horizontal gap is below a
threshold; larger gaps become separate tokens.

Reading aid only: text adjacency, not electrical connectivity.
"""
import sys, collections

tol   = float(sys.argv[2]) if len(sys.argv) > 2 else 1.2
gap   = float(sys.argv[3]) if len(sys.argv) > 3 else 3.2

rows = collections.defaultdict(list)
for line in open(sys.argv[1], encoding='utf-8'):
    p = line.rstrip('\n').split('\t')
    if len(p) < 4: continue
    obj, x, y, t = p[0], float(p[1]), float(p[2]), p[3]
    rows[(obj, round(y / tol))].append((x, y, t))

out = []
for (obj, yk), items in rows.items():
    items.sort()
    toks, cur, curx = [], '', None
    lastend = None
    for x, y, t in items:
        if lastend is not None and (x - lastend) > gap:
            if cur: toks.append((curx, cur))
            cur, curx = '', None
        if not cur: curx = x
        cur += t
        lastend = x + 3.0 * len(t)
    if cur: toks.append((curx, cur))
    y = items[0][1]
    for xx, tk in toks:
        out.append((y, xx, tk))

out.sort(key=lambda r: (-r[0], r[1]))
for y, x, t in out:
    print(f'{y:9.2f}\t{x:9.2f}\t{t}')
