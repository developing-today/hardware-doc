#!/usr/bin/env python3
"""Extract text from every content stream in a PDF (incl. Form XObjects),
grouping each BT..ET block into a single string with its Tm origin."""
import sys, re
sys.path.insert(0,'/home/user/hardware-doc/archive/devices/lilygo/t-display-s3-shared/artifacts')
from pdftext import objects, stream_of, TXT, unesc

BLOCK = re.compile(rb'BT(.*?)ET', re.S)
TM    = re.compile(rb'([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm')
TD    = re.compile(rb'([-\d.]+)\s+([-\d.]+)\s+Td')

def run(path):
    data = open(path,'rb').read(); objs = objects(data); out = []
    for n, b in sorted(objs.items()):
        s, _ = stream_of(b)
        if not s or b'BT' not in s: continue
        for blk in BLOCK.findall(s):
            m = TM.search(blk)
            if m:
                a, bb = float(m.group(1)), float(m.group(2))
                x, y = float(m.group(5)), float(m.group(6))
                rot = 'V' if abs(a) < 0.01 and abs(bb) > 0.01 else 'H'
            else:
                t = TD.search(blk)
                x, y = (float(t.group(1)), float(t.group(2))) if t else (0.0, 0.0)
                rot = 'H'
            txt = ''.join(unesc(v) for v in TXT.findall(blk))
            txt = txt.strip()
            if txt: out.append((n, rot, round(x,1), round(y,1), txt))
    return out

if __name__ == '__main__':
    for n, r, x, y, t in run(sys.argv[1]):
        print(f'{n}\t{r}\t{x}\t{y}\t{t}')
