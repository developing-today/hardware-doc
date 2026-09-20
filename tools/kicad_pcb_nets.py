#!/usr/bin/env python3
"""Authoritative netlist from a KiCad .kicad_pcb: footprints -> pads -> (net N "NAME").
Unlike .kicad_sch, the PCB file stores resolved net names, so this is the
ground truth for connectivity. Executed 2026-08-24."""
import sys,re,collections
src=open(sys.argv[1],encoding='utf-8',errors='replace').read()
nets=collections.defaultdict(list)
# iterate footprints
for m in re.finditer(r'\(footprint ',src):
    i=m.start();depth=0;j=i
    while j<len(src):
        if src[j]=='(':depth+=1
        elif src[j]==')':
            depth-=1
            if depth==0:break
        j+=1
    blk=src[i:j+1]
    ref=re.search(r'\(property "Reference" "([^"]*)"',blk)
    ref=ref.group(1) if ref else '?'
    val=re.search(r'\(property "Value" "([^"]*)"',blk)
    val=val.group(1) if val else ''
    for p in re.finditer(r'\(pad "([^"]*)"[^\n]*',blk):
        pi=p.start();d=0;k=pi
        while k<len(blk):
            if blk[k]=='(':d+=1
            elif blk[k]==')':
                d-=1
                if d==0:break
            k+=1
        pb=blk[pi:k+1]
        nm=re.search(r'\(net \d+ "([^"]*)"\)',pb)
        if nm: nets[nm.group(1)].append((ref,p.group(1),val))
arg=sys.argv[2] if len(sys.argv)>2 else None
if arg and arg!='--all':
    rows=[(n,r,pad) for n,pins in nets.items() for r,pad,_ in pins if r==arg]
    for n,r,pad in sorted(rows,key=lambda x:(int(x[2]) if x[2].isdigit() else 999,x[2])):
        print(f"{r}.{pad:<5} -> {n}")
    print(f"\n{len(rows)} pads")
else:
    for n in sorted(nets):
        pins=sorted(set(nets[n]))
        print(f"{n:<26} ({len(pins):2d}) " + ", ".join(f"{r}.{p}" for r,p,_ in pins))
