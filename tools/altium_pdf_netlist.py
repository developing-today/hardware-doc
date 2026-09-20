"""Parse pdftotext -bbox XML into word records, classifying Altium PDF markers.

Altium Designer's PDF publisher emits invisible marker text at schematic objects:
  CO<designator>            component outline
  PI<designator><pin>       pin instance
  NL<netname>               net label
Non-alphanumerics in names are replaced by '0' in the marker, so the marker is
lossy (G0_BOOT_OUT -> NLG00BOOT0OUT). Markers therefore locate objects; the
human-readable text next to them supplies the real name.
"""
import re, sys, math, json, html

WORD = re.compile(r'<word xMin="([\d.\-]+)" yMin="([\d.\-]+)" xMax="([\d.\-]+)" yMax="([\d.\-]+)">(.*?)</word>')

def load(path):
    out = []
    for m in WORD.finditer(open(path, encoding='utf-8', errors='replace').read()):
        x0, y0, x1, y1 = (float(m.group(i)) for i in range(1, 5))
        t = html.unescape(m.group(5))
        out.append({'x': (x0+x1)/2, 'y': (y0+y1)/2, 'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 't': t})
    return out

MARKER = re.compile(r'(?<![A-Za-z])(CO|PI|NL)([A-Z0-9]+)')

def split_markers(words):
    """A single extracted 'word' may glue a marker to real text (e.g. '15PIU7015').

    The negative lookbehind matters: without it 'GPIO0' parses as G + PI-marker
    'O0' and 'SPI2_MOSI' as S + PI-marker '2', which silently eats pin names on
    every MCU sheet. Altium emits each marker as its own text object, so a real
    marker is never preceded by a letter.
    """
    plain, co, pi, nl = [], [], [], []
    for w in words:
        t = w['t']
        for mm in MARKER.finditer(t):
            kind, body = mm.group(1), mm.group(2)
            rec = dict(w); rec['body'] = body
            (co if kind == 'CO' else pi if kind == 'PI' else nl).append(rec)
        rest = MARKER.sub(' ', t).strip()
        if rest:
            rec = dict(w); rec['t'] = rest
            plain.append(rec)
    return plain, co, pi, nl

def designators(co):
    """Reference designators, from CO markers. CO markers may themselves be glued
    to a following PI marker, so take the leading letters+digits only."""
    d = set()
    for c in co:
        m = re.match(r'([A-Z]+[0-9]+)', c['body'])
        if m:
            d.add(m.group(1))
    return d

def split_pin(body, desigs):
    """PIU7015 is ambiguous: U7/pin015 or U70/pin15. Resolve with the known
    designator set, longest match first; report unresolved rather than guessing."""
    cands = [d for d in desigs if body.startswith(d) and body[len(d):].isdigit()]
    if not cands:
        return None, None
    best = max(cands, key=len)
    return best, body[len(best):].lstrip('0') or '0'

def near(w, pool, r):
    out = []
    for p in pool:
        d = math.hypot(p['x'] - w['x'], p['y'] - w['y'])
        if d <= r:
            out.append((d, p))
    out.sort(key=lambda z: z[0])
    return out

if __name__ == '__main__':
    allw = {}
    for p in range(1, 7):
        allw[p] = load(f'pdf/bbox-p{p}.xml')
    grand = set()
    for p, ws in allw.items():
        plain, co, pi, nl = split_markers(ws)
        grand |= designators(co)
    print("total distinct designators:", len(grand))
    print(json.dumps(sorted(grand), indent=0)[:4000])
