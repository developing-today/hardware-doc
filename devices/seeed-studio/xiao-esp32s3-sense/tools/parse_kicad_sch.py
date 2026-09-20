#!/usr/bin/env python3
"""Parse a KiCad 9 .kicad_sch s-expression file into components + net labels.
Usage: parse_kicad_sch.py <file.kicad_sch> [--bom|--labels|--pins]
Executed 2026-08-24 against the Seeed XIAO ESP32S3 Sense v1.5 KiCad source."""
import sys,re

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
            if t=='(':
                sub,i=rec(i+1);node.append(sub)
            elif t==')':
                return node,i+1
            else:
                node.append(t);i+=1
        return node,i
    res=[];i=0
    while i<len(tokens):
        if tokens[i]=='(':
            sub,i=rec(i+1);res.append(sub)
        else:i+=1
    return res

def head(n):
    return n[0][1] if n and isinstance(n[0],tuple) else None

def find(node,name):
    for c in node:
        if isinstance(c,list) and head(c)==name: yield c

def prop(sym,key):
    for p in find(sym,'property'):
        if len(p)>2 and isinstance(p[1],tuple) and p[1][1]==key:
            return p[2][1] if isinstance(p[2],tuple) else None
    return None

def walk(node,name,out):
    for c in node:
        if isinstance(c,list):
            if head(c)==name: out.append(c)
            walk(c,name,out)

data=open(sys.argv[1],encoding='utf-8',errors='replace').read()
tree=parse(tokenize(data))
root=tree[0]
mode=sys.argv[2] if len(sys.argv)>2 else '--bom'

if mode=='--bom':
    syms=[];walk(root,'symbol',syms)
    rows={}
    for s in syms:
        ref=prop(s,'Reference');val=prop(s,'Value')
        if not ref or ref.startswith('#'): continue
        fp=prop(s,'Footprint') or ''
        dsc=prop(s,'Description') or ''
        mpn=prop(s,'MPN') or prop(s,'Manufacturer Part Number') or prop(s,'PN') or ''
        rows[ref]=(val,fp,mpn,dsc)
    def k(r):
        m=re.match(r'([A-Za-z_]+)(\d+)',r);return (m.group(1),int(m.group(2))) if m else (r,0)
    print(f"{'Ref':<6} {'Value':<28} {'MPN':<22} Footprint")
    for r in sorted(rows,key=k):
        v,fp,mpn,dsc=rows[r]
        print(f"{r:<6} {v:<28} {mpn:<22} {fp}")
    print(f"\nTOTAL {len(rows)} placed components")
elif mode=='--labels':
    seen={}
    for nm in ('label','global_label','hierarchical_label'):
        ls=[];walk(root,nm,ls)
        for l in ls:
            if len(l)>1 and isinstance(l[1],tuple):
                seen.setdefault(l[1][1],set()).add(nm)
    for t in sorted(seen): print(f"{t}\t{','.join(sorted(seen[t]))}")
    print(f"\nTOTAL {len(seen)} distinct net labels")
