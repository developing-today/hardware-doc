#!/usr/bin/env python3
"""
netlist.py - derive a designator/pin -> net-label table from an Altium PDF export.

Altium's PDF export writes three families of *invisible* helper tokens into the
text layer, each placed at the exact schematic coordinate of the thing it names:

  CO<designator>            component outline origin        e.g. COU7, COR13
  PI<designator><pin>       pin electrical end point        e.g. PIU7014, PIR902
  NL<netname>               net label anchor                e.g. NLG8, NLVBUS

Because PI and NL carry true coordinates, a net label can be bound to the pin it
labels by geometry alone.  Altium anchors a net label at the *lower-left* of its
text and floats it just above the wire, so the label's y sits ~2-5 pt above the
horizontal wire it names; for a vertical wire the label's x sits ~2-5 pt left.

Output columns: designator, pin, candidate net(s) with the offset used.

Usage:
  python3 netlist.py FILE.xhtml [--page N] [--des U7] [--tol 5] [--reach 60]
  python3 netlist.py FILE.xhtml --nets          # just dump every NL token
  python3 netlist.py FILE.xhtml --components    # designator -> value/part guess
"""
import re
import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict

NS = "{http://www.w3.org/1999/xhtml}"
# `PIU7014` is ambiguous on its own -- U701 pin 4 or U7 pin 14?  Altium zero-pads
# the pin number to two digits, but the designator may itself end in digits, so
# the split is only decidable once the sheet's real designator set is known from
# the CO<designator> tokens.  Parse CO first, then split PI against that set.
NET_RX = re.compile(r"^NL(.+)$")
CO_RX = re.compile(r"^CO([A-Z]+[0-9]+)$")
POWER_RX = re.compile(r"^(GND|GNDA|AGND|PGND|DGND|\+?[0-9]V[0-9]?|\+[0-9]\.[0-9]V|V(BUS|BAT|CC|DD|SYS|IN|OUT|3V3|DD3V3)|3V3|VDD3V3|\+5V|\+3\.3V|\+1\.8V|\+4\.2V)$")


def split_pin(tok, designators):
    """'PIU7014' + {'U7'} -> ('U7','14').  Longest known designator wins."""
    body = tok[2:]
    best = None
    for d in designators:
        if body.startswith(d):
            rest = body[len(d):]
            if rest and re.fullmatch(r"[0-9A-Z]+", rest):
                if best is None or len(d) > len(best[0]):
                    best = (d, rest)
    if best is None:
        return None
    d, rest = best
    # Altium pads to two digits: '04' -> 4, '14' -> 14, '0A' -> A
    if len(rest) > 1 and rest[0] == "0":
        rest = rest[1:]
    return d, rest


def load(path):
    raw = re.sub(r"<!DOCTYPE[^>]*>", "",
                 open(path, encoding="utf-8", errors="replace").read(), count=1)
    root = ET.fromstring(raw)
    out = []
    for pno, page in enumerate(root.iter(NS + "page"), 1):
        for w in page.iter(NS + "word"):
            t = (w.text or "").strip()
            if not t:
                continue
            x0, y0 = float(w.get("xMin")), float(w.get("yMin"))
            x1, y1 = float(w.get("xMax")), float(w.get("yMax"))
            out.append(dict(p=pno, x=(x0 + x1) / 2, y=(y0 + y1) / 2, t=t))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--page", type=int)
    ap.add_argument("--des")
    ap.add_argument("--tol", type=float, default=5.0,
                    help="row/column alignment tolerance, pt")
    ap.add_argument("--reach", type=float, default=60.0,
                    help="max distance along the wire to accept a label, pt")
    ap.add_argument("--nets", action="store_true")
    ap.add_argument("--components", action="store_true")
    a = ap.parse_args()

    ws = [w for w in load(a.file) if a.page is None or w["p"] == a.page]

    # pass 1 -- learn the designator set from CO tokens (all pages, so a symbol
    # whose outline lands on one page still resolves pins seen on another)
    allw = load(a.file)
    designators = {m.group(1) for w in allw
                   for m in [CO_RX.match(w["t"])] if m}

    nets, pins, cos, plain = [], [], [], []
    for w in ws:
        t = w["t"]
        if t.startswith("PI"):
            sp = split_pin(t, designators)
            if sp:
                pins.append((w, sp[0], sp[1])); continue
        m = CO_RX.match(t)
        if m:
            cos.append((w, m.group(1))); continue
        m = NET_RX.match(t)
        if m:
            nets.append((w, m.group(1))); continue
        plain.append(w)

    if a.nets:
        for w, n in sorted(nets, key=lambda r: (r[0]["p"], r[0]["y"], r[0]["x"])):
            print(f"p{w['p']} x={w['x']:7.2f} y={w['y']:7.2f}  {n}")
        return

    if a.components:
        for w, d in sorted(cos, key=lambda r: (r[0]["p"], r[0]["y"], r[0]["x"])):
            near = sorted(
                (((v["x"] - w["x"]) ** 2 + (v["y"] - w["y"]) ** 2) ** 0.5, v["t"])
                for v in plain if v["p"] == w["p"]
                and abs(v["x"] - w["x"]) < 60 and abs(v["y"] - w["y"]) < 24)[:6]
            print(f"p{w['p']} {d:8} x={w['x']:7.2f} y={w['y']:7.2f}  "
                  + " | ".join(f"{t}({d2:.0f})" for d2, t in near))
        return

    by_des = defaultdict(list)
    for w, d, pin in pins:
        by_des[d].append((w, pin))

    for des in sorted(by_des, key=lambda s: (re.sub(r"\d", "", s),
                                             int(re.sub(r"\D", "", s) or 0))):
        if a.des and des != a.des:
            continue
        print(f"\n=== {des} ===")
        for w, pin in sorted(by_des[des], key=lambda r: int(re.sub(r"\D", "", r[1]) or 0)):
            cands = []
            for nw, name in nets:
                if nw["p"] != w["p"]:
                    continue
                dx, dy = nw["x"] - w["x"], nw["y"] - w["y"]
                # Altium floats a net label just ABOVE its horizontal wire, so the
                # correct binding has a small NEGATIVE dy.  A label with positive
                # dy at the same x belongs to the pin one row down; rank it last.
                if -a.tol - 1 <= dy <= a.tol and abs(dx) <= a.reach:
                    rank = 0 if dy < -0.5 else 2
                    cands.append((rank, abs(dx), f"{name} [h dx={dx:+.1f} dy={dy:+.1f}]"))
                elif -a.tol - 1 <= dx <= a.tol and abs(dy) <= a.reach:
                    rank = 0 if dx < -0.5 else 2
                    cands.append((rank, abs(dy), f"{name} [v dy={dy:+.1f} dx={dx:+.1f}]"))
            # power-port symbols are plain text (GND, +3.3V, VBUS...) sitting
            # directly above or below the pin, aligned in x
            for pw in plain:
                if pw["p"] != w["p"] or not POWER_RX.match(pw["t"]):
                    continue
                dx, dy = pw["x"] - w["x"], pw["y"] - w["y"]
                if abs(dx) <= a.tol and abs(dy) <= 14:
                    cands.append((1, abs(dy), f"{pw['t']} [pwr dx={dx:+.1f} dy={dy:+.1f}]"))
            cands.sort()
            cands.sort()
            # nearest same-row / same-column *other* pin, for point-to-point wires
            peers = []
            for w2, d2, p2 in pins:
                if w2 is w or w2["p"] != w["p"]:
                    continue
                dx, dy = w2["x"] - w["x"], w2["y"] - w["y"]
                if abs(dy) <= 1.0 and 0 < abs(dx) <= a.reach:
                    peers.append((abs(dx), f"{d2}.{p2}[h {dx:+.1f}]"))
                elif abs(dx) <= 1.0 and 0 < abs(dy) <= a.reach:
                    peers.append((abs(dy), f"{d2}.{p2}[v {dy:+.1f}]"))
            peers.sort()
            nstr = "; ".join(c for _, _, c in cands[:3]) or "-"
            pstr = "; ".join(c for _, c in peers[:3]) or "-"
            print(f"  p{w['p']} {des}.{pin:<4} x={w['x']:7.2f} y={w['y']:7.2f}  "
                  f"net: {nstr:<46} peer: {pstr}")


if __name__ == "__main__":
    main()
