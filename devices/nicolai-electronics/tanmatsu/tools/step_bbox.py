#!/usr/bin/env python3
"""Compute the bounding box of an ISO 10303-21 (STEP) file without a CAD kernel.

STEP is plain text; CARTESIAN_POINT entities carry the geometry. Reading every
point and taking min/max gives the overall extent, which is enough to answer
"will it fit" questions without installing FreeCAD.

Caveat: this bounds *control points*, which for spline/NURBS geometry can lie
slightly outside the visible surface. For mostly-prismatic mechanical parts the
error is small, but treat results as approximate and never as a tolerance.

Usage: step_bbox.py <file.step> [...]
Executed 2026-08-24.
"""
import re, sys

PT = re.compile(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*"
                r"(-?[\d.E+-]+)\s*,\s*(-?[\d.E+-]+)\s*,\s*(-?[\d.E+-]+)", re.I)

for path in sys.argv[1:]:
    xs = ys = zs = None
    n = 0
    with open(path, encoding="utf-8", errors="replace") as f:
        buf = ""
        for chunk in iter(lambda: f.read(1 << 20), ""):
            buf += chunk
            *done, buf = buf.rsplit(";", 1)
            for m in PT.finditer(";".join(done)):
                x, y, z = (float(m.group(i)) for i in (1, 2, 3))
                n += 1
                if xs is None:
                    xs = [x, x]; ys = [y, y]; zs = [z, z]
                else:
                    xs[0] = min(xs[0], x); xs[1] = max(xs[1], x)
                    ys[0] = min(ys[0], y); ys[1] = max(ys[1], y)
                    zs[0] = min(zs[0], z); zs[1] = max(zs[1], z)
    name = path.rsplit("/", 1)[-1]
    if not n:
        print(f"{name}: no CARTESIAN_POINT found"); continue
    print(f"{name}")
    print(f"  points {n:,}")
    print(f"  X {xs[0]:9.2f} .. {xs[1]:9.2f}   = {xs[1]-xs[0]:8.2f} mm")
    print(f"  Y {ys[0]:9.2f} .. {ys[1]:9.2f}   = {ys[1]-ys[0]:8.2f} mm")
    print(f"  Z {zs[0]:9.2f} .. {zs[1]:9.2f}   = {zs[1]-zs[0]:8.2f} mm")
