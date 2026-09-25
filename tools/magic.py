import sys, os, hashlib
SIG = [(b'%PDF-','pdf'),(b'PK\x03\x04','zip'),(b'\x89PNG','png'),(b'\xff\xd8\xff','jpeg'),
       (b'7z\xbc\xaf\x27\x1c','7z'),(b'\xfd7zXZ','xz'),(b'\x1f\x8b','gzip'),
       (b'ISO-10303-21','step'),(b'AC10','dwg'),(b'AC20','dwg'),(b'solid','stl-ascii'),
       (b'<!DOC','HTML'),(b'<html','HTML'),(b'<HTML','HTML'),(b'<?xml','xml')]
for p in sys.argv[1:]:
    if not os.path.isfile(p): print('MISSING',p); continue
    b=open(p,'rb').read(64); n=os.path.getsize(p)
    t=None
    for s,name in SIG:
        if b.startswith(s): t=name; break
    if t is None:
        if b[0:1]==b'\xe9' or b[0:1]==b'\xea': t='esp-image(magic 0x%02x)'%b[0]
        elif b[:4]==b'\x00\x00\x00\x00': t='binary'
        else:
            try: b.decode('utf-8'); t='text'
            except Exception: t='binary'
    h=hashlib.sha256(open(p,'rb').read()).hexdigest()
    print(f'{t:<24} {n:>10} {h} {p}')
