#!/usr/bin/env python3
"""Extract text from PDFs using Type0/Identity-H fonts by decoding /ToUnicode CMaps.
Per skill rule: validate against a known heading before transcribing values."""
import sys, re
sys.path.insert(0,'/home/user/hardware-doc/archive/devices/lilygo/t-display-s3-shared/artifacts')
from pdftext import objects, stream_of

def cmaps(objs):
    """font-resource-name is per stream; build a single global cid->unicode map
    (adequate when subsets do not collide, which we check by reporting collisions)."""
    m = {}; coll = 0
    for n, b in objs.items():
        s, _ = stream_of(b)
        if not s or b'beginbfchar' not in s and b'beginbfrange' not in s: continue
        for blk in re.findall(rb'beginbfchar(.*?)endbfchar', s, re.S):
            for a, c in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
                k = int(a, 16); v = bytes.fromhex(c.decode()).decode('utf-16-be', 'replace')
                if k in m and m[k] != v: coll += 1
                m[k] = v
        for blk in re.findall(rb'beginbfrange(.*?)endbfrange', s, re.S):
            for lo, hi, c in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
                l, h, base = int(lo,16), int(hi,16), int(c,16)
                for i in range(l, min(h,l+512)+1):
                    m[i] = chr(base + (i - l))
    return m, coll

def run(path):
    data = open(path,'rb').read(); objs = objects(data)
    cm, coll = cmaps(objs)
    out = []
    for n, b in sorted(objs.items()):
        s, _ = stream_of(b)
        if not s or b'BT' not in s: continue
        for blk in re.findall(rb'BT(.*?)ET', s, re.S):
            tm = re.search(rb'([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm', blk)
            x, y = (float(tm.group(5)), float(tm.group(6))) if tm else (0.0, 0.0)
            txt = ''
            for hexs in re.findall(rb'<([0-9A-Fa-f\s]+)>', blk):
                h = re.sub(rb'\s', b'', hexs).decode()
                for i in range(0, len(h)-3, 4):
                    txt += cm.get(int(h[i:i+4], 16), '\uFFFD')
            txt = txt.strip()
            if txt: out.append((round(x,1), round(y,1), txt))
    return out, coll

if __name__ == '__main__':
    o, coll = run(sys.argv[1])
    sys.stderr.write(f'# cmap collisions: {coll}\n')
    for x,y,t in o: print(f'{x}\t{y}\t{t}')
