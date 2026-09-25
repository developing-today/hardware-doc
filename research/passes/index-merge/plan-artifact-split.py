#!/usr/bin/env python3
"""Round-2 integration, TASK 3 — decide where the FCC exhibits live.

Reads every `_filing.html` in scratch/market-and-certification/fcc/, matches the
downloaded PDFs to their exhibit rows, assigns each to the record that OWNS it
(the board or module the exhibit describes), and classifies it repository vs
archive.

Emits plan.json.  Moves nothing — see apply-artifact-plan.py.

Rule 1 (whose is it?)  FCC exhibits describe a specific board or module.
                       Boards -> devices/<vendor>/<board>/artifacts/certification/
                       Modules -> components/<vendor>/<part>/artifacts/certification/
Rule 2 (small/large?)  Internal Photos and ID-Label exhibits are the high-value,
                       modestly-sized evidence: internal photos are the only public
                       internal imagery for several of these boards, and the X4's are
                       the first public teardown of that device.  They stay in the
                       repository, subject to a 4 MiB per-file cap.
                       Test reports, users manuals, RF-exposure annexes and external
                       photos are bulk -> archive with a placeholder.
"""
import json, os, re, html, hashlib, sys

FCC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'market-and-certification', 'fcc')
FCC = os.path.normpath(FCC)
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

# ---------------------------------------------------------------- ownership
# The record each filing DESCRIBES.  `kind` distinguishes a board from a module,
# because that decides devices/ vs components/ per the skill's filing rule.
OWNER = {
  '2AN3WM5CAPCC1101':    ('devices/m5stack/cap-cc1101',              'board'),
  '2AN3WM5CAPLORA1262':  ('devices/m5stack/cap-lora-1262',           'board'),
  '2AN3WM5CARDPUTER':    ('devices/m5stack/cardputer-v1.0',          'board'),
  '2AN3WM5CARDPUTERADV': ('devices/m5stack/cardputer-adv',           'board'),
  '2AN3WM5DINMETER':     ('devices/m5stack/dinmeter',                'board'),
  '2AN3WM5STAMPC6LORA':  ('devices/m5stack/stamp-c6lora',            'board'),
  '2AN3WM5UNITC6L':      ('devices/m5stack/unit-c6l',                'board'),
  '2AN3WM5STAMPS3A':     ('components/m5stack/stamp-s3a',            'module'),
  '2AN3WSTAMPLORA1262':  ('components/m5stack/stamp-lora-1262',      'module'),
  '2ASYE-T-DISPLAY':     ('devices/lilygo/t-display-ttgo',           'board'),
  '2ASYE-T-DISPLAY-19':  ('devices/lilygo/t-display-s3-amoled',      'board'),
  '2ASYE-TDISS3-AMOLED': ('devices/lilygo/t-display-s3-amoled',      'board'),
  '2ASYE-T-DISPLAY-PRO': ('devices/lilygo/t-display-s3-pro',         'board'),
  '2ASYE-T-DISPLAY-S3':  ('devices/lilygo/t-display-s3',             'board'),
  '2ASYE-T-DONGLE-S3':   ('devices/lilygo/t-dongle-s3',              'board'),
  '2ASYE-T-QT-PRO':      ('devices/lilygo/t-qt',                     'board'),
  '2ASYE-T4-S3-241':     ('devices/lilygo/t4-s3',                    'board'),
  '2ASYE-TDISPLAY-LONG': ('devices/lilygo/t-display-s3-long',        'board'),
  '2BTR9-X4C':           ('devices/xteink/x4-classic',               'board'),
  '2BTR9-X4L':           ('devices/xteink/x4-light',                 'board'),
  '2BTR9-X4PRO':         ('devices/xteink/x4-pro',                   'board'),
  '2BTR9-XTEINKX3':      ('devices/xteink/x3',                       'board'),
  '2BTR9-XTEINKX4':      ('devices/xteink/x4',                       'board'),
  # positive controls: Espressif's own module grants.  No component record exists
  # for the WROOM-1/1U module yet, so these land in a certification-only artifacts
  # directory under the part they describe.
  '2AC7Z-ESPS3WROOM1':   ('components/espressif/esp32-s3-wroom-1',   'module'),
  '2AC7Z-ESPS3WROOM1U':  ('components/espressif/esp32-s3-wroom-1u',  'module'),
  # LIVE — another session owns this tree.  Park, do not write.
  '2AN3WM5PAPERMONO':    ('devices/m5stack/papermono',               'board'),
}
PARKED = {'2AN3WM5PAPERMONO'}

KEEP_TYPES = {'Internal Photos', 'ID Label/Location Info'}
CAP = 4 * 1024 * 1024          # "modestly sized"

EXH = re.compile(
    r'<tr><td data-label="Document"><a href="(?P<href>[^"]+)">(?P<doc>.*?)</a></td>'
    r'<td data-label="Type">(?P<type>.*?)</td>'
    r'<td data-label="Available">(?P<avail>.*?)</td>'
    r'<td data-label="File">(?P<file>.*?)</td></tr>', re.S)

def strip(x): return html.unescape(re.sub(r'<[^>]+>', ' ', x)).strip()
def slug(x):  return re.sub(r'-+', '-', re.sub(r'[^A-Za-z0-9]+', '-', x)).strip('-')

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

# ------------------------------------------------------- existing repo bytes
have = {}
for root, _, files in os.walk(REPO):
    if '/.git' in root or '/scratch/' in root or root.endswith('/scratch'): continue
    if 'artifacts/certification' not in root: continue
    for fn in files:
        if fn.endswith('.pdf'):
            p = os.path.join(root, fn)
            have[sha(p)] = os.path.relpath(p, REPO)

meta = json.load(open(os.path.join(FCC, 'filing-metadata.json')))
plan = []
for fid in sorted(os.listdir(FCC)):
    d = os.path.join(FCC, fid)
    if not os.path.isdir(d): continue
    fh = os.path.join(d, '_filing.html')
    rows = []
    if os.path.exists(fh):
        s = open(fh, encoding='utf-8', errors='replace').read()
        for m in EXH.finditer(s):
            rows.append({'doc': strip(m['doc']), 'type': strip(m['type']),
                         'avail': strip(m['avail']),
                         'url': html.unescape(m['href'])})
    # The harvester named files `<slug(type)>-<doc with spaces->dashes>.pdf`, which
    # keeps `_` and `.`; the fccid.io href slug strips them.  Index every variant so
    # no exhibit loses its reacquisition URL.
    idx = {}
    for r in rows:
        t = slug(r['type'])
        for v in (r['doc'].replace(' ', '-'), slug(r['doc']),
                  re.sub(r'[^\w.-]+', '-', r['doc']),
                  re.sub(r'[^A-Za-z0-9._]+', '-', r['doc']).strip('-')):
            idx.setdefault(f"{t}-{v}.pdf", r)
    owner, kind = OWNER.get(fid, (None, None))
    fm = meta.get(fid, {})
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.pdf'): continue
        p = os.path.join(d, fn)
        sz = os.path.getsize(p); h = sha(p)
        r = idx.get(fn, {})
        url = r.get('url', '')
        if url and url.startswith('/'): url = 'https://fccid.io' + url
        # the `.pdf` suffix is mandatory — without it fccid.io serves an HTML viewer
        if url and not url.endswith('.pdf'): url += '.pdf'
        docid = ''
        m = re.search(r'-(\d{5,})\.pdf$', url or '')
        if m: docid = m.group(1)
        etype = r.get('type') or 'unknown'
        # canonical in-repo filename
        canon = f"{fid}-{slug(r.get('doc') or fn[:-4]).lower()}.pdf"
        dest = f"{owner}/artifacts/certification/{canon}" if owner else None
        if fid in PARKED:                       disp = 'park'
        elif h in have:                         disp = 'already-in-repo'
        elif etype in KEEP_TYPES and sz <= CAP: disp = 'repo'
        else:                                   disp = 'archive'
        # `final_action` is a scrape artifact of the form
        # "<freq band> <purpose> <YYYY-MM-DD>".  Take the trailing date only; the
        # rest is already carried by `freq` and `purpose`.
        fa = fm.get('final_action') or ''
        mg = re.search(r'(\d{4}-\d{2}-\d{2})\s*$', fa)
        granted = mg.group(1) if mg else (fa or '')
        plan.append({
            'fccid': fid, 'src': os.path.relpath(p, REPO), 'dest': dest,
            'disposition': disp, 'exhibit_type': etype, 'document': r.get('doc', ''),
            'bytes': sz, 'sha256': h, 'url': url, 'fcc_doc_id': docid,
            'published': r.get('avail', ''), 'owner': owner, 'owner_kind': kind,
            'applicant': fm.get('applicant', ''), 'test_firm': fm.get('test_firm', ''),
            'granted': granted, 'grant_purpose': fm.get('purpose', ''),
            'freq': fm.get('freq', []), 'equip_class': fm.get('equip_class', ''),
            'dup_of': have.get(h, ''),
        })

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plan.json')

# Disambiguate destination names.  A Class-II permissive-change filing can carry
# several exhibits whose titles differ only in case ("External Photo" /
# "External Photos" / "External photos"), which collapse to one slug.  Where that
# happens, append the FCC document id — it is unique and keeps the file traceable
# to the exact exhibit row.
import collections as _c
_seen = _c.Counter(x['dest'] for x in plan if x['dest'])
for x in plan:
    if x['dest'] and _seen[x['dest']] > 1 and x['fcc_doc_id']:
        b, e = os.path.splitext(x['dest'])
        x['dest'] = f"{b}-{x['fcc_doc_id']}{e}"
assert len({x['dest'] for x in plan if x['dest'] and x['disposition'] in ('repo', 'archive')}) == \
       len([x for x in plan if x['dest'] and x['disposition'] in ('repo', 'archive')]), 'dest collision remains'

json.dump(plan, open(out, 'w'), indent=1)

import collections
c = collections.Counter(x['disposition'] for x in plan)
b = collections.Counter()
for x in plan: b[x['disposition']] += x['bytes']
print(f"{len(plan)} exhibits from {len(set(x['fccid'] for x in plan))} filings")
for k in ('repo', 'archive', 'already-in-repo', 'park'):
    print(f"  {k:16s} {c[k]:4d} files  {b[k]/1048576:8.2f} MiB")
nourl = [x for x in plan if not x['url']]
print("exhibits with no recovered URL:", len(nourl))
for x in nourl[:10]: print("   ", x['src'])
