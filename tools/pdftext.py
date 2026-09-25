#!/usr/bin/env python3
"""Minimal PDF text extractor: FlateDecode content streams, Tj/TJ/' /" operators.
Emits one line per text-showing op with page and rough x,y from Tm/Td.
Validate output against a rendered page before trusting values (skill rule)."""
import sys, re, zlib

def objects(data):
    objs = {}
    for m in re.finditer(rb'(\d+)\s+(\d+)\s+obj\b', data):
        num = int(m.group(1)); start = m.end()
        e = data.find(b'endobj', start)
        objs[num] = data[start:e if e > 0 else len(data)]
    return objs

def stream_of(body):
    m = re.search(rb'stream\r?\n', body)
    if not m: return None, body
    dic = body[:m.start()]
    end = body.find(b'endstream', m.end())
    raw = body[m.end():end if end > 0 else len(body)]
    if b'FlateDecode' in dic:
        for trim in (0, 1, 2):
            try: return zlib.decompress(raw[:len(raw)-trim] if trim else raw), dic
            except Exception: pass
        try:
            d = zlib.decompressobj(); return d.decompress(raw), dic
        except Exception: return None, dic
    return raw, dic

TXT = re.compile(rb"\((?:\\.|[^\\()])*\)|<[0-9A-Fa-f\s]+>")
def unesc(b):
    if b.startswith(b'<'):
        h = re.sub(rb'\s', b'', b[1:-1])
        try: raw = bytes.fromhex(h.decode())
        except Exception: return ''
        # try UTF-16BE-ish 2-byte codes, else latin1
        if len(raw) % 2 == 0 and all(raw[i] == 0 for i in range(0, len(raw), 2)):
            return raw.decode('utf-16-be', 'replace')
        return raw.decode('latin1', 'replace')
    s = b[1:-1]
    out = bytearray(); i = 0
    while i < len(s):
        c = s[i]
        if c == 0x5c and i + 1 < len(s):
            n = s[i+1]
            mp = {0x6e:10, 0x72:13, 0x74:9, 0x62:8, 0x66:12}
            if n in mp: out.append(mp[n]); i += 2; continue
            if 0x30 <= n <= 0x37:
                j = i+1; oc = b''
                while j < len(s) and 0x30 <= s[j] <= 0x37 and len(oc) < 3:
                    oc += s[j:j+1]; j += 1
                out.append(int(oc, 8) & 0xFF); i = j; continue
            out.append(n); i += 2; continue
        out.append(c); i += 1
    return bytes(out).decode('latin1', 'replace')

def extract(path, pages=None):
    data = open(path, 'rb').read()
    objs = objects(data)
    # page order
    kids = []
    for num, body in objs.items():
        if re.search(rb'/Type\s*/Page\b(?!s)', body): kids.append(num)
    kids.sort()
    out = []
    for pi, pnum in enumerate(kids, 1):
        if pages and pi not in pages: continue
        body = objs[pnum]
        cm = re.search(rb'/Contents\s+(?:(\d+)\s+\d+\s+R|\[([^\]]*)\])', body)
        cids = []
        if cm:
            if cm.group(1): cids = [int(cm.group(1))]
            else: cids = [int(x) for x in re.findall(rb'(\d+)\s+\d+\s+R', cm.group(2))]
        content = b''
        for cid in cids:
            if cid in objs:
                s, _ = stream_of(objs[cid])
                if s: content += s + b'\n'
        x = y = 0.0
        for line in content.split(b'\n'):
            mtm = re.search(rb'([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm', line)
            if mtm: x, y = float(mtm.group(5)), float(mtm.group(6))
            mtd = re.search(rb'([-\d.]+)\s+([-\d.]+)\s+Td', line)
            if mtd and not mtm: x += float(mtd.group(1)); y += float(mtd.group(2))
            if re.search(rb'\bT[Jj]\b|\bT\*|\'|"', line):
                parts = [unesc(t) for t in TXT.findall(line)]
                s = ''.join(parts).strip()
                if s: out.append((pi, round(x, 1), round(y, 1), s))
    return out

if __name__ == '__main__':
    ap = sys.argv[1]
    pg = set(int(v) for v in sys.argv[2].split(',')) if len(sys.argv) > 2 else None
    for p, x, y, s in extract(ap, pg):
        print(f'{p}\t{x}\t{y}\t{s}')
