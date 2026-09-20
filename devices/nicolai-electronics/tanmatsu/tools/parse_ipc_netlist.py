#!/usr/bin/env python3
"""Parse an IPC-D-356(A) netlist into {net: [(refdes, pin), ...]}.

This is the *fabrication* netlist emitted alongside Gerbers for bare-board
electrical test. Unlike a schematic it needs no EDA tool to read, and unlike
vendor prose it cannot drift out of date relative to the copper it was
exported from - which makes it a good independent check on documented pinouts.

Record layout (columns, 1-based):
  1-3    record type: 317 = pad/via, 327 = pad with access, 378 = continuation
  4-20   net name
  21-26  reference designator
  27     '-'
  28+    pin number, then feature/geometry fields (MD.., A01, X/Y, R, S)

Usage: parse_ipc_netlist.py <file.ipc> [--ref REF | --net NET | --summary]
Executed 2026-08-24.
"""
import sys, re, collections

def parse(path):
    nets = collections.defaultdict(list)
    for line in open(path, encoding="utf-8", errors="replace"):
        if not line.startswith(("317", "327")):
            continue
        net = line[3:20].strip()
        ref = line[20:26].strip()
        rest = line[26:]
        if not rest.startswith("-"):
            continue
        m = re.match(r"-\s*(\S+?)\s", rest)
        pin = m.group(1) if m else rest[1:5].strip()
        if ref.upper() == "VIA" or not ref:
            continue
        nets[net].append((ref, pin))
    return nets

def key(rp):
    m = re.match(r"([A-Za-z]+)(\d+)", rp[0])
    p = rp[1]
    return (m.group(1), int(m.group(2)) if m else 0, int(p) if p.isdigit() else 0)

def _cli():

    nets = parse(sys.argv[1])
    mode = sys.argv[2] if len(sys.argv) > 2 else "--summary"
    arg = sys.argv[3] if len(sys.argv) > 3 else None

    if mode == "--ref":
      rows = [(p, n) for n, pins in nets.items() for r, p in pins if r == arg]
      for p, n in sorted(rows, key=lambda x: int(x[0]) if x[0].isdigit() else 999):
          print(f"{arg}.{p:<4} -> {n}")
      print(f"\n{len(rows)} pads on {arg}")
    elif mode == "--net":
      for r, p in sorted(nets.get(arg, []), key=key):
          print(f"  {r}.{p}")
      print(f"\n{len(nets.get(arg,[]))} pads on net {arg}")
    else:
      refs = collections.Counter(r for pins in nets.values() for r, _ in pins)
      print(f"{len(nets)} nets, {sum(len(v) for v in nets.values())} pads, {len(refs)} components")
      print("\nComponents by pad count:")
      for r, c in refs.most_common(30):
          print(f"  {r:<8} {c}")


if __name__ == "__main__":
    _cli()
