#!/usr/bin/env python3
"""
trace.py - spatial net tracing helper for vector schematic PDFs.

Parses `pdftotext -bbox-layout` XHTML into (page, x, y, text) word records and
provides proximity queries, so a net label can be associated with the pin it
sits beside on the sheet.

Usage:
  python3 trace.py words   FILE.xhtml [--page N]
  python3 trace.py near    FILE.xhtml TOKEN [--r 40] [--page N]
  python3 trace.py grep    FILE.xhtml REGEX [--page N]
  python3 trace.py row     FILE.xhtml --y Y [--tol 3] [--page N]
  python3 trace.py col     FILE.xhtml --x X [--tol 3] [--page N]
  python3 trace.py pins    FILE.xhtml [--page N]        # Altium PI<des><pin> tokens
  python3 trace.py cluster FILE.xhtml --x X --y Y --r R [--page N]

Coordinate system: PDF user space as emitted by poppler; yMin increases
*downwards* in poppler's bbox output (top-left origin).
"""
import re
import sys
import argparse
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/1999/xhtml}"


def load(path):
    """Return list of dicts: page, x, y, x1, y1, cx, cy, t."""
    # poppler emits an XHTML doctype with an external DTD; strip it.
    raw = open(path, "r", encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<!DOCTYPE[^>]*>", "", raw, count=1)
    root = ET.fromstring(raw)
    words = []
    for pno, page in enumerate(root.iter(NS + "page"), start=1):
        for w in page.iter(NS + "word"):
            t = (w.text or "").strip()
            if not t:
                continue
            x0 = float(w.get("xMin")); y0 = float(w.get("yMin"))
            x1 = float(w.get("xMax")); y1 = float(w.get("yMax"))
            words.append(dict(page=pno, x=x0, y=y0, x1=x1, y1=y1,
                              cx=(x0 + x1) / 2, cy=(y0 + y1) / 2, t=t))
    return words


def fmt(w):
    return f"p{w['page']} x={w['cx']:8.2f} y={w['cy']:8.2f}  {w['t']}"


def sel(words, page):
    return [w for w in words if page is None or w["page"] == page]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("file")
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--page", type=int, default=None)
    ap.add_argument("--r", type=float, default=40.0)
    ap.add_argument("--x", type=float)
    ap.add_argument("--y", type=float)
    ap.add_argument("--tol", type=float, default=3.0)
    a = ap.parse_args()

    words = load(a.file)
    ws = sel(words, a.page)

    if a.cmd == "words":
        for w in sorted(ws, key=lambda w: (w["page"], w["cy"], w["cx"])):
            print(fmt(w))

    elif a.cmd == "grep":
        rx = re.compile(a.arg)
        for w in sorted(ws, key=lambda w: (w["page"], w["cy"], w["cx"])):
            if rx.search(w["t"]):
                print(fmt(w))

    elif a.cmd == "near":
        anchors = [w for w in ws if w["t"] == a.arg]
        if not anchors:
            anchors = [w for w in ws if a.arg in w["t"]]
        for an in anchors:
            print(f"=== anchor {fmt(an)}")
            got = []
            for w in ws:
                if w is an or w["page"] != an["page"]:
                    continue
                d = ((w["cx"] - an["cx"]) ** 2 + (w["cy"] - an["cy"]) ** 2) ** 0.5
                if d <= a.r:
                    got.append((d, w))
            for d, w in sorted(got):
                dx = w["cx"] - an["cx"]; dy = w["cy"] - an["cy"]
                print(f"   d={d:7.2f} dx={dx:+8.2f} dy={dy:+8.2f}  {w['t']}")

    elif a.cmd == "row":
        got = [w for w in ws if abs(w["cy"] - a.y) <= a.tol]
        for w in sorted(got, key=lambda w: w["cx"]):
            print(fmt(w))

    elif a.cmd == "col":
        got = [w for w in ws if abs(w["cx"] - a.x) <= a.tol]
        for w in sorted(got, key=lambda w: w["cy"]):
            print(fmt(w))

    elif a.cmd == "cluster":
        for w in sorted(ws, key=lambda w: (w["cy"], w["cx"])):
            d = ((w["cx"] - a.x) ** 2 + (w["cy"] - a.y) ** 2) ** 0.5
            if d <= a.r:
                print(f"d={d:7.2f} {fmt(w)}")

    elif a.cmd == "pins":
        # Altium PDF exports carry hidden PI<designator><pin> tokens placed at
        # the exact pin coordinate, and CO<designator> at the component origin.
        rx = re.compile(r"^PI([A-Z]+[0-9]+)0?([0-9A-Z]+)$")
        for w in sorted(ws, key=lambda w: (w["page"], w["cy"], w["cx"])):
            m = rx.match(w["t"])
            if m:
                print(f"p{w['page']} x={w['cx']:8.2f} y={w['cy']:8.2f}  "
                      f"{m.group(1)}.{m.group(2)}   ({w['t']})")
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
