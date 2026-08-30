#!/usr/bin/env python3
"""Extract the KeebDeck keyboard footprint geometry from a KiCad .kicad_mod.

Useful if you have loose KeebDeck keypads and need to lay out your own host PCB:
reports the key grid, pad pitch, dome-contact pad geometry and board outline
without opening KiCad.

Usage: parse_keebdeck_footprint.py <Keyboard_6R13C.kicad_mod>
Executed 2026-08-24.
"""
import re, sys, collections

src = open(sys.argv[1], encoding="utf-8", errors="replace").read()

pads = []
for m in re.finditer(r'\(pad "([^"]*)"\s+(\S+)\s+(\S+)\s*\n\s*\(at ([-\d.]+) ([-\d.]+)',
                     src):
    name, ptype, shape, x, y = m.group(1), m.group(2), m.group(3), float(m.group(4)), float(m.group(5))
    pads.append((name, ptype, shape, x, y))

byname = collections.defaultdict(list)
for n, t, s, x, y in pads:
    byname[n].append((t, s, x, y))

cols = sorted({n for n in byname if re.fullmatch(r"C\d+", n)}, key=lambda s: int(s[1:]))
rows = sorted({n for n in byname if re.fullmatch(r"R\d+", n)}, key=lambda s: int(s[1:]))
other = sorted(n for n in byname if n not in cols and n not in rows)

print(f"pads total       : {len(pads)}")
print(f"column nets      : {len(cols)}  {cols}")
print(f"row nets         : {len(rows)}  {rows}")
if other:
    print(f"other nets       : {other}")

xs = [p[3] for p in pads]; ys = [p[4] for p in pads]
print(f"\npad extent       : X {min(xs):.2f}..{max(xs):.2f} ({max(xs)-min(xs):.2f} mm)"
      f"  Y {min(ys):.2f}..{max(ys):.2f} ({max(ys)-min(ys):.2f} mm)")

# unique X positions of the SMD dome pads -> horizontal pitch
smd = [(n, x, y) for n, t, s, x, y in pads if t == "smd"]
ux = sorted({round(x, 2) for _, x, _ in smd})
uy = sorted({round(y, 2) for _, _, y in smd})
def pitches(v):
    d = [round(b - a, 3) for a, b in zip(v, v[1:])]
    return collections.Counter(d).most_common(4)
print(f"SMD pads         : {len(smd)}")
print(f"unique X ({len(ux):2d})    : most common spacing {pitches(ux)}")
print(f"unique Y ({len(uy):2d})    : most common spacing {pitches(uy)}")

sizes = collections.Counter()
for m in re.finditer(r'\(pad "[^"]*"\s+(\S+)\s+(\S+)\s*\n\s*\(at [^\)]*\)\s*\n\s*\(size ([\d.]+) ([\d.]+)\)', src):
    sizes[(m.group(1), m.group(2), m.group(3), m.group(4))] += 1
print("\npad geometry:")
for (t, s, w, h), c in sizes.most_common():
    print(f"  {c:4d} x  {t:<9} {s:<8} {w} x {h} mm")

edge = [(float(a), float(b)) for a, b in
        re.findall(r'\(fp_line\s*\(start ([-\d.]+) ([-\d.]+)\)', src)]
if edge:
    ex = [p[0] for p in edge]; ey = [p[1] for p in edge]
    print(f"\nsilk/outline bbox: {max(ex)-min(ex):.2f} x {max(ey)-min(ey):.2f} mm")
