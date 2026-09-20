#!/usr/bin/env python3
"""Parse an EAGLE .sch (XML) into a BOM and netlist.

EAGLE schematics are XML and carry an explicit <nets> section, so unlike KiCad
schematics no geometry reconstruction is needed - the netlist is stated.
This is the only way to get connectivity for Seeed's EAGLE-era boards, whose
exported PDFs render all text as vector paths and yield no text layer.

Usage: eagle_netlist.py <file.sch> [--bom | --nets | --ref REF]
Executed 2026-08-24.
"""
import sys, xml.etree.ElementTree as ET, collections, re

f = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "--bom"
arg = sys.argv[3] if len(sys.argv) > 3 else None
root = ET.parse(f).getroot()

parts = {}
for p in root.iter("part"):
    parts[p.get("name")] = {
        "device": (p.get("deviceset") or "") + (p.get("device") or ""),
        "value": p.get("value") or "",
        "library": p.get("library") or "",
    }

nets = collections.defaultdict(list)
for net in root.iter("net"):
    n = net.get("name")
    for cr in net.iter("pinref"):
        nets[n].append((cr.get("part"), cr.get("pin")))

def key(r):
    m = re.match(r"([A-Za-z_]+)(\d+)", r or "")
    return (m.group(1), int(m.group(2))) if m else (r or "", 0)

if mode == "--bom":
    print(f"{'Ref':<8}{'Value':<26}{'Device':<34}Library")
    for r in sorted(parts, key=key):
        d = parts[r]
        print(f"{r:<8}{d['value'][:25]:<26}{d['device'][:33]:<34}{d['library']}")
    print(f"\nTOTAL {len(parts)} parts, {len(nets)} nets")
elif mode == "--ref":
    rows = [(n, pin) for n, pins in nets.items() for (pt, pin) in pins if pt == arg]
    for n, pin in sorted(rows, key=lambda x: (len(x[1]), x[1])):
        print(f"{arg}.{pin:<8} -> {n}")
    print(f"\n{len(rows)} connected pins on {arg}")
else:
    for n in sorted(nets):
        pins = nets[n]
        if len(pins) < 2:
            continue
        print(f"{n:<22} ({len(pins):2d}) " + ", ".join(f"{a}.{b}" for a, b in sorted(pins)))
    print(f"\n{len(nets)} nets")
