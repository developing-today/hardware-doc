#!/usr/bin/env python3
"""
render.py - re-flow a `pdftotext -bbox-layout` XHTML into readable rows.

`pdftotext -layout` collapses catastrophically on wide (A3/tabloid) schematic
sheets because it tries to reconcile one global column grid across the whole
page.  This instead buckets words into rows by their y centre and prints each
row left-to-right, optionally restricted to an x/y window, so a symbol can be
read in isolation.

Usage:
  python3 render.py FILE.xhtml [--page N] [--x0 X --x1 X --y0 Y --y1 Y]
                    [--rowtol 2.0] [--hide-pi]
"""
import re
import argparse
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/1999/xhtml}"


def load(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<!DOCTYPE[^>]*>", "", raw, count=1)
    root = ET.fromstring(raw)
    out = []
    for pno, page in enumerate(root.iter(NS + "page"), 1):
        for w in page.iter(NS + "word"):
            t = (w.text or "").strip()
            if not t:
                continue
            x0, y0 = float(w.get("xMin")), float(w.get("yMin"))
            x1, y1 = float(w.get("xMax")), float(w.get("yMax"))
            out.append((pno, (x0 + x1) / 2, (y0 + y1) / 2, t))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--page", type=int)
    ap.add_argument("--x0", type=float, default=-1e9)
    ap.add_argument("--x1", type=float, default=1e9)
    ap.add_argument("--y0", type=float, default=-1e9)
    ap.add_argument("--y1", type=float, default=1e9)
    ap.add_argument("--rowtol", type=float, default=2.0)
    ap.add_argument("--hide-pi", action="store_true",
                    help="drop Altium PI*/CO* hidden designator tokens")
    a = ap.parse_args()

    ws = [w for w in load(a.file)
          if (a.page is None or w[0] == a.page)
          and a.x0 <= w[1] <= a.x1 and a.y0 <= w[2] <= a.y1]
    if a.hide_pi:
        ws = [w for w in ws if not re.match(r"^(PI|CO|NL)[A-Z]", w[3])]

    for pno in sorted({w[0] for w in ws}):
        pw = sorted([w for w in ws if w[0] == pno], key=lambda w: (w[2], w[1]))
        print(f"########## page {pno} ##########")
        rows, cur = [], []
        for w in pw:
            if cur and abs(w[2] - cur[0][2]) > a.rowtol:
                rows.append(cur); cur = []
            cur.append(w)
        if cur:
            rows.append(cur)
        for r in rows:
            r = sorted(r, key=lambda w: w[1])
            y = sum(w[2] for w in r) / len(r)
            cells = "  ".join(f"{w[3]}@{w[1]:.0f}" for w in r)
            print(f"y={y:7.1f} | {cells}")


if __name__ == "__main__":
    main()
