"""Minimal pure-Python PDF text extractor with positions.

No poppler/pypdf on this host. Parses the xref-free way: scan all stream
objects, inflate FlateDecode ones, and interpret the content-stream text
operators (BT/ET, Tf, Td/TD/Tm/T*, Tj/TJ/'/"). Also resolves simple
/Differences-free WinAnsi text and hex strings.

Emits TSV: page  x  y  text
This is a reading aid, not an authority -- see AGENTS/skill guidance.
"""
import re, sys, zlib

def objects(data):
    """Yield (objnum, gen, dict_bytes, stream_bytes|None) for every 'N G obj'."""
    for m in re.finditer(rb'(\d+)\s+(\d+)\s+obj\b', data):
        start = m.end()
        endm = re.compile(rb'\bendobj\b').search(data, start)
        if not endm:
            continue
        body = data[start:endm.start()]
        sm = re.search(rb'\bstream\r?\n', body)
        stream = None
        if sm:
            em = body.rfind(b'endstream')
            if em > sm.end():
                stream = body[sm.end():em]
                if stream.endswith(b'\r\n'): stream = stream[:-2]
                elif stream.endswith(b'\n') or stream.endswith(b'\r'): stream = stream[:-1]
            body = body[:sm.start()]
        yield int(m.group(1)), int(m.group(2)), body, stream

def inflate(dic, raw):
    if raw is None: return None
    if b'FlateDecode' not in dic: return raw
    for trim in (0, 1, 2):
        try:
            return zlib.decompress(raw[trim:])
        except zlib.error:
            pass
    try:
        return zlib.decompressobj().decompress(raw)
    except zlib.error:
        return None

STR = re.compile(rb'\((?:\\.|[^()\\])*\)|<[0-9A-Fa-f\s]*>', re.S)

def decode_str(tok):
    if tok.startswith(b'<'):
        h = re.sub(rb'\s', b'', tok[1:-1])
        if len(h) % 2: h += b'0'
        b = bytes.fromhex(h.decode('ascii'))
        # heuristics: UTF-16BE if lots of NULs
        if b[:2] == b'\xfe\xff':
            return b[2:].decode('utf-16-be', 'replace')
        if len(b) >= 2 and b.count(0) > len(b) // 3:
            return b.decode('utf-16-be', 'replace')
        return b.decode('latin-1', 'replace')
    s = tok[1:-1]
    out, i = bytearray(), 0
    while i < len(s):
        c = s[i]
        if c == 0x5c and i + 1 < len(s):
            n = s[i+1]
            mp = {0x6e: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12}
            if n in mp: out.append(mp[n]); i += 2; continue
            if 0x30 <= n <= 0x37:
                j = i + 1; oct_ = b''
                while j < len(s) and len(oct_) < 3 and 0x30 <= s[j] <= 0x37:
                    oct_ += bytes([s[j]]); j += 1
                out.append(int(oct_, 8) & 0xFF); i = j; continue
            out.append(n); i += 2; continue
        out.append(c); i += 1
    return bytes(out).decode('latin-1', 'replace')

NUM = rb'[-+]?[\d.]+'

def extract(content):
    """Return list of (x, y, text)."""
    res = []
    tm = [1, 0, 0, 1, 0, 0]
    tlm = list(tm)
    intext = False
    # tokenize on operators we care about
    pat = re.compile(
        rb'(BT)|(ET)|'
        rb'(' + NUM + rb')\s+(' + NUM + rb')\s+(' + NUM + rb')\s+(' + NUM + rb')\s+(' + NUM + rb')\s+(' + NUM + rb')\s+Tm|'
        rb'(' + NUM + rb')\s+(' + NUM + rb')\s+(TD|Td)|'
        rb'(T\*)|'
        rb'(\[(?:[^\[\]\\]|\\.)*\])\s*TJ|'
        rb'((?:\((?:\\.|[^()\\])*\)|<[0-9A-Fa-f\s]*>))\s*Tj', re.S)
    for m in pat.finditer(content):
        if m.group(1):
            intext = True; tm = [1,0,0,1,0,0]; tlm = list(tm); continue
        if m.group(2):
            intext = False; continue
        if m.group(3):
            tm = [float(m.group(i)) for i in range(3, 9)]; tlm = list(tm); continue
        if m.group(9):
            dx, dy = float(m.group(9)), float(m.group(10))
            tlm = [tlm[0], tlm[1], tlm[2], tlm[3], tlm[4] + dx*tlm[0] + dy*tlm[2], tlm[5] + dx*tlm[1] + dy*tlm[3]]
            tm = list(tlm); continue
        if m.group(12):
            tlm = [tlm[0], tlm[1], tlm[2], tlm[3], tlm[4], tlm[5] - 12]
            tm = list(tlm); continue
        txt = None
        if m.group(13):
            parts = []
            for t in STR.finditer(m.group(13)):
                parts.append(decode_str(t.group(0)))
            txt = ''.join(parts)
        elif m.group(14):
            txt = decode_str(m.group(14))
        if txt:
            res.append((round(tm[4], 2), round(tm[5], 2), txt))
    return res

def main(path):
    data = open(path, 'rb').read()
    pages = []
    # collect content streams in object order; map page objects
    streams = {}
    page_objs = []
    for num, gen, dic, raw in objects(data):
        if raw is not None:
            streams[num] = (dic, raw)
        if re.search(rb'/Type\s*/Page\b', dic):
            page_objs.append((num, dic))
    page_objs.sort()
    if not page_objs:
        # fall back: dump all streams as one page
        page_objs = [(0, b'')]
    for pi, (pnum, pdic) in enumerate(page_objs, 1):
        refs = []
        cm = re.search(rb'/Contents\s*(?:(\d+)\s+\d+\s+R|\[(.*?)\])', pdic, re.S)
        if cm:
            if cm.group(1):
                refs = [int(cm.group(1))]
            else:
                refs = [int(x) for x in re.findall(rb'(\d+)\s+\d+\s+R', cm.group(2))]
        content = b''
        for r in refs:
            if r in streams:
                d = inflate(*streams[r])
                if d: content += d + b'\n'
        if not content and pnum == 0:
            for num, (dic, raw) in streams.items():
                d = inflate(dic, raw)
                if d and (b'BT' in d): content += d + b'\n'
        pages.append(extract(content))
    for i, items in enumerate(pages, 1):
        for x, y, t in items:
            print(f'{i}\t{x}\t{y}\t{t}')

if __name__ == '__main__':
    main(sys.argv[1])
