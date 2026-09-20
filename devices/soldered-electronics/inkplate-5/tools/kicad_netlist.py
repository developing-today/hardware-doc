#!/usr/bin/env python3
"""Reconstruct a netlist from a KiCad 9 .kicad_sch by geometric union-find over
wire segments, junctions, symbol pin endpoints and net labels.

KiCad stores no netlist in the .kicad_sch; connectivity is implied by geometry.
This resolves lib_symbols pin positions, applies each symbol instance's
(at x y rot) + mirror transform, snaps every point to a 0.001mm grid, unions
points joined by wires, then names each net from any label touching it.

Usage: kicad_netlist.py <sheet.kicad_sch> [--net NAME | --ref REF | --all]
"""
import sys,math,collections
sys.setrecursionlimit(100000)

def tokenize(s):
    out=[];i=0;n=len(s)
    while i<n:
        c=s[i]
        if c in '()':out.append(c);i+=1
        elif c=='"':
            j=i+1;buf=[]
            while j<n:
                if s[j]=='\\':buf.append(s[j+1]);j+=2
                elif s[j]=='"':break
                else:buf.append(s[j]);j+=1
            out.append(('str',''.join(buf)));i=j+1
        elif c.isspace():i+=1
        else:
            j=i
            while j<n and not s[j].isspace() and s[j] not in '()"':j+=1
            out.append(('sym',s[i:j]));i=j
    return out

def parse(tokens):
    def rec(i):
        node=[]
        while i<len(tokens):
            t=tokens[i]
            if t=='(':sub,i=rec(i+1);node.append(sub)
            elif t==')':return node,i+1
            else:node.append(t);i+=1
        return node,i
    res=[];i=0
    while i<len(tokens):
        if tokens[i]=='(':sub,i=rec(i+1);res.append(sub)
        else:i+=1
    return res

def h(n): return n[0][1] if n and isinstance(n[0],tuple) else None
def kids(n,name): return [c for c in n if isinstance(c,list) and h(c)==name]
def val(n,i=1): return n[i][1] if len(n)>i and isinstance(n[i],tuple) else None
def nums(n): return [float(x[1]) for x in n[1:] if isinstance(x,tuple)]

def prop(sym,key):
    for p in kids(sym,'property'):
        if val(p,1)==key: return val(p,2)
    return None

src=open(sys.argv[1],encoding='utf-8',errors='replace').read()
root=parse(tokenize(src))[0]

# ---- library symbol pin geometry ----
libpins={}   # libname -> [(pinnum, name, x, y)]
for lib in kids(root,'lib_symbols'):
    for s in kids(lib,'symbol'):
        ln=val(s)
        acc=[]
        def collect(node):
            for sub in kids(node,'symbol'):
                for p in kids(sub,'pin'):
                    at=kids(p,'at')
                    if not at: continue
                    x,y=nums(at[0])[0],nums(at[0])[1]
                    num=None;nm=None
                    for nn in kids(p,'number'): num=val(nn)
                    for nn in kids(p,'name'): nm=val(nn)
                    acc.append((num,nm,x,y))
                collect(sub)
        collect(s)
        libpins[ln]=acc

Q=1000.0
def snap(x,y): return (round(x*Q),round(y*Q))

parent={}
def findp(a):
    parent.setdefault(a,a)
    while parent[a]!=a: parent[a]=parent[parent[a]];a=parent[a]
    return a
def union(a,b):
    ra,rb=findp(a),findp(b)
    if ra!=rb: parent[ra]=rb

# ---- wires ----
for w in kids(root,'wire'):
    for ptsn in kids(w,'pts'):
        pts=[snap(*nums(x)[:2]) for x in kids(ptsn,'xy')]
        for a,b in zip(pts,pts[1:]): union(a,b)

# ---- symbol instances -> pin points ----
pinpoints=collections.defaultdict(list)  # point -> [(ref,pinnum,pinname)]
for s in kids(root,'symbol'):
    lid=None
    for l in kids(s,'lib_id'): lid=val(l)
    if lid is None: continue
    at=kids(s,'at')
    if not at: continue
    a=nums(at[0]); sx,sy=a[0],a[1]; rot=a[2] if len(a)>2 else 0
    mirror=None
    for m in kids(s,'mirror'): mirror=val(m)
    ref=prop(s,'Reference')
    if not ref or ref.startswith('#'): continue
    for num,nm,px,py in libpins.get(lid,[]):
        x,y=px,py
        if mirror=='y': x=-x
        if mirror=='x': y=-y
        th=math.radians(rot)
        rx=x*math.cos(th)-y*math.sin(th)
        ry=x*math.sin(th)+y*math.cos(th)
        # KiCad schematic Y axis is inverted relative to symbol space
        gx,gy=sx+rx, sy-ry
        pinpoints[snap(gx,gy)].append((ref,num,nm))

# ---- labels ----
labelpts=collections.defaultdict(set)
for kind in ('label','global_label','hierarchical_label'):
    for l in kids(root,kind):
        t=val(l)
        at=kids(l,'at')
        if not at or t is None: continue
        p=snap(*nums(at[0])[:2])
        labelpts[p].add(t)

# power symbols contribute their Value as a net name (GND, VBUS, ...)
for s in kids(root,'symbol'):
    lid=None
    for l in kids(s,'lib_id'): lid=val(l)
    if not lid or not lid.startswith('power:'): continue
    at=kids(s,'at')
    if not at: continue
    a=nums(at[0]); sx,sy=a[0],a[1]; rot=a[2] if len(a)>2 else 0
    v=prop(s,'Value')
    for num,nm,px,py in libpins.get(lid,[]):
        th=math.radians(rot)
        gx,gy=sx+(px*math.cos(th)-py*math.sin(th)), sy-(px*math.sin(th)+py*math.cos(th))
        if v: labelpts[snap(gx,gy)].add(v)

# make sure every interesting point participates
for p in list(pinpoints)+list(labelpts): findp(p)

nets=collections.defaultdict(lambda: {'names':set(),'pins':[]})
for p in list(parent):
    r=findp(p)
    for t in labelpts.get(p,()): nets[r]['names'].add(t)
    for pin in pinpoints.get(p,()): nets[r]['pins'].append(pin)

named=[]
for r,d in nets.items():
    if not d['pins'] and not d['names']: continue
    nm=sorted(d['names'])
    name=nm[0] if nm else f"N${r[0]}_{r[1]}"
    named.append((name,sorted(set(nm)),sorted(set(d['pins']))))
named.sort(key=lambda x:x[0])

mode=sys.argv[2] if len(sys.argv)>2 else '--all'
arg=sys.argv[3] if len(sys.argv)>3 else None
if mode=='--ref':
    rows=[]
    for name,alias,pins in named:
        for ref,num,pnm in pins:
            if ref==arg: rows.append((int(num) if num and num.isdigit() else 0,num,pnm,name,alias))
    for _,num,pnm,name,alias in sorted(rows):
        print(f"{arg}.{num:<4} {str(pnm)[:22]:<22} -> {name}   {alias if len(alias)>1 else ''}")
    print(f"\n{len(rows)} connected pins on {arg}")
else:
    conn=[n for n in named if len(n[2])>1]
    print(f"{len(named)} nets, {len(conn)} with >1 pin")
    for name,alias,pins in conn:
        print(f"\n== {name}" + (f"  (aliases {alias})" if len(alias)>1 else ""))
        print("   " + ", ".join(f"{r}.{n}" for r,n,_ in pins))

# --- appended: merged-by-name report (mode --merged) ---
if mode=='--merged':
    byname=collections.defaultdict(set)
    single=[]
    for name,alias,pins in named:
        key=name if not name.startswith('N$') else name
        for p in pins: byname[key].add(p)
    # merge power/label nets sharing a name
    real=collections.defaultdict(set)
    for k,v in byname.items(): real[k]|=v
    for k in sorted(real):
        pins=sorted(real[k])
        if len(pins)==1 and k.startswith('N$'): single.append((k,pins[0]))
    print("### NETS (merged by label name)")
    for k in sorted(real):
        pins=sorted(real[k])
        if len(pins)<2 and k.startswith('N$'): continue
        print(f"{k:<26} {', '.join(f'{r}.{n}' for r,n,_ in pins)}")
    print("\n### SINGLE-PIN / NO-CONNECT pins (unnamed net, one pin only)")
    for k,(r,n,pn) in sorted(single,key=lambda x:x[1][0]):
        print(f"  {r}.{n:<4} ({pn})")
