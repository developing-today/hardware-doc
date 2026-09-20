"""Render an Altium schematic PDF page as ordered text rows, markers stripped.

Markers (CO/PI/NL) are dropped from the visible rendering but their designator
and pin information is re-attached inline as [D.pin] so a reader can see which
component a pin number belongs to without opening the PDF.
"""
import sys, re
sys.path.insert(0, 'tools')
from altium_pdf_netlist import load, split_markers, designators, split_pin

page = int(sys.argv[1]); tol = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
ws = load(f'pdf/bbox-p{page}.xml')
plain, co, pi, nl = split_markers(ws)
# designator set from *all* pages, since a sheet may reference parts drawn elsewhere
desig = set()
for p in range(1, 7):
    _, c2, _, _ = split_markers(load(f'pdf/bbox-p{p}.xml'))
    desig |= designators(c2)

items = [(w['y'], w['x'], w['t']) for w in plain]
for m in pi:
    d, pin = split_pin(m['body'], desig)
    items.append((m['y'], m['x'], f"[{d}.{pin}]" if d else f"[?{m['body']}]"))
for m in co:
    mm = re.match(r'([A-Z]+[0-9]+)', m['body'])
    if mm:
        items.append((m['y'], m['x'], f"<{mm.group(1)}>"))
items.sort()
rows, cur, cy = [], [], None
for y, x, t in items:
    if cy is None or abs(y - cy) <= tol:
        cur.append((x, t)); cy = y if cy is None else cy
    else:
        rows.append((cy, sorted(cur))); cur = [(x, t)]; cy = y
if cur: rows.append((cy, sorted(cur)))
for y, r in rows:
    print(f"{y:6.1f} | " + '  '.join(t for _, t in r))
