#!/usr/bin/env python3
"""Parse the M5Stack DinMeter (K134) Altium-published schematic PDF bbox XML.

Altium's PDF publisher emits an invisible marker layer:
  CO<designator>       component outline
  PI<designator><pin>  pin instance
  NL<netname>          net label
Non-alphanumerics are replaced by '0' in markers, so markers locate objects;
the human-readable text beside them supplies the real name.

Usage: parse_dinmeter_sch.py <bbox.xml>
"""
import re, sys, math, html, json

WORD = re.compile(r'<word xMin="([\d.\-]+)" yMin="([\d.\-]+)" xMax="([\d.\-]+)" yMax="([\d.\-]+)">(.*?)</word>')
MARKER = re.compile(r'(?<![A-Za-z])(CO|PI|NL)([A-Z0-9]+)')

def load(path):
    out=[]
    for m in WORD.finditer(open(path,encoding='utf-8',errors='replace').read()):
        x0,y0,x1,y1=(float(m.group(i)) for i in range(1,5))
        out.append({'x':(x0+x1)/2,'y':(y0+y1)/2,'x0':x0,'y0':y0,'x1':x1,'y1':y1,
                    't':html.unescape(m.group(5))})
    return out

def split_markers(words):
    plain,co,pi,nl=[],[],[],[]
    for w in words:
        for mm in MARKER.finditer(w['t']):
            kind,body=mm.group(1),mm.group(2)
            rec=dict(w); rec['body']=body
            (co if kind=='CO' else pi if kind=='PI' else nl).append(rec)
        rest=MARKER.sub(' ',w['t']).strip()
        if rest:
            rec=dict(w); rec['t']=rest; plain.append(rec)
    return plain,co,pi,nl

def designators(co):
    d=set()
    for c in co:
        m=re.match(r'([A-Z]+[0-9]+)',c['body'])
        if m: d.add(m.group(1))
    return d

def split_pin(body,desigs):
    c=[d for d in desigs if body.startswith(d) and body[len(d):].isdigit()]
    if not c: return None,None
    best=max(c,key=len)
    return best, body[len(best):].lstrip('0') or '0'

def near(w,pool,r):
    out=[(math.hypot(p['x']-w['x'],p['y']-w['y']),p) for p in pool]
    out=[o for o in out if o[0]<=r]; out.sort(key=lambda z:z[0]); return out

if __name__=='__main__':
    ws=load(sys.argv[1])
    plain,co,pi,nl=split_markers(ws)
    des=designators(co)
    print(f"# words={len(ws)} plain={len(plain)} CO={len(co)} PI={len(pi)} NL={len(nl)}")
    print(f"# designators ({len(des)}):")
    print(json.dumps(sorted(des,key=lambda d:(re.match(r'[A-Z]+',d).group(),int(re.search(r'\d+',d).group())))))
    print("\n## net labels (NL markers, with nearest plain text)")
    seen=set()
    for n in sorted(nl,key=lambda z:(z['y'],z['x'])):
        cands=near(n,plain,14)
        txt=cands[0][1]['t'] if cands else ''
        key=(n['body'],txt)
        if key in seen: continue
        seen.add(key)
        print(f"  NL{n['body']:<18} x={n['x']:7.1f} y={n['y']:7.1f}  text={txt!r}")
    print("\n## pin instances -> nearest plain text (pin name / net)")
    rows=[]
    for p in pi:
        d,pn=split_pin(p['body'],des)
        cands=near(p,plain,16)
        nls=near(p,nl,16)
        rows.append((d or '?',int(pn) if pn and pn.isdigit() else 0,p['x'],p['y'],
                     [c[1]['t'] for c in cands[:3]],
                     [c[1]['body'] for c in nls[:2]]))
    for d,pn,x,y,txts,nls in sorted(rows,key=lambda r:(r[0],r[1])):
        print(f"  {d:<6} pin {pn:<3} x={x:7.1f} y={y:7.1f}  near={txts}  NL={nls}")
