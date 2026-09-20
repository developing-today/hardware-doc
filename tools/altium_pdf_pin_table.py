"""Recover a per-component pin table from an Altium schematic PDF.

For each PI<desig><pin> marker, collect the human-readable words sharing its
row band, split into what lies inside the symbol body (pin name) and what lies
outside it (the attached net label). The symbol's horizontal extent is estimated
from the spread of its own pin markers.

This is a reading aid, not an authority: it recovers text adjacency, not
electrical connectivity, so unlabelled wire-only connections are invisible to it
and every row must be checked against the rendered sheet before being asserted.
"""
import sys, re
sys.path.insert(0, 'tools')
from altium_pdf_netlist import load, split_markers, designators, split_pin

page, target = int(sys.argv[1]), sys.argv[2]
band = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5

desig = set()
for p in range(1, 7):
    _, c2, _, _ = split_markers(load(f'pdf/bbox-p{p}.xml'))
    desig |= designators(c2)

ws = load(f'pdf/bbox-p{page}.xml')
plain, co, pi, nl = split_markers(ws)

mine = []
for m in pi:
    d, pin = split_pin(m['body'], desig)
    if d == target:
        mine.append((pin, m))
if not mine:
    print(f"no pin markers for {target} on page {page}"); sys.exit(0)

xs = [m['x'] for _, m in mine]
lo, hi = min(xs), max(xs)
print(f"# {target} on sheet {page}: {len(mine)} pin markers, x span {lo:.0f}..{hi:.0f}")
print(f"{'pin':>5} | {'x':>6} | inside symbol (pin name)            | outside (net / value)")
print("-" * 110)
for pin, m in sorted(mine, key=lambda z: (int(z[0]) if z[0].isdigit() else 999, z[1]['y'])):
    row = [w for w in plain if abs(w['y'] - m['y']) <= band]
    row.sort(key=lambda w: abs(w['x'] - m['x']))
    inside = [w['t'] for w in row if lo - 2 <= w['x'] <= hi + 2][:4]
    outside = [w['t'] for w in row if not (lo - 2 <= w['x'] <= hi + 2)][:5]
    print(f"{pin:>5} | {m['x']:6.1f} | {' '.join(inside)[:35]:35s} | {' '.join(outside)[:45]}")
