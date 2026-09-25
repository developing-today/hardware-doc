import sys,struct,os,hashlib
MAG=struct.pack('<I',0xABCD5432)
for p in sys.argv[1:]:
    d=open(p,'rb').read()
    print('###',os.path.basename(p),len(d),hashlib.sha256(d).hexdigest()[:16])
    off=0; found=0
    while True:
        i=d.find(MAG,off)
        if i<0: break
        off=i+4
        try:
            (magic,secure_version)=struct.unpack_from('<II',d,i)
            rsv=struct.unpack_from('<2I',d,i+8)
            ver=d[i+16:i+48].split(b'\0')[0].decode('latin1')
            proj=d[i+48:i+80].split(b'\0')[0].decode('latin1')
            time=d[i+80:i+96].split(b'\0')[0].decode('latin1')
            date=d[i+96:i+112].split(b'\0')[0].decode('latin1')
            idf=d[i+112:i+144].split(b'\0')[0].decode('latin1')
        except Exception as e:
            continue
        if not proj.isprintable() or not idf.startswith('v'): continue
        found+=1
        print(f'   @0x{i:06x} proj={proj!r} ver={ver!r} date={date!r} time={time!r} idf={idf!r} secver={secure_version}')
    # partition table at 0x8000
    if len(d)>0x9000:
        pt=d[0x8000:0x9000]
        for j in range(0,0x1000,32):
            e=pt[j:j+32]
            if e[:2]!=b'\xaa\x50': continue
            t,st=e[2],e[3]
            off_,size=struct.unpack_from('<II',e,4)
            lbl=e[12:28].split(b'\0')[0].decode('latin1')
            print(f'   part {lbl:<10} type={t} subtype=0x{st:02x} off=0x{off_:06x} size=0x{size:06x} ({size//1024}K)')
    if not found: print('   (no app descriptor found)')
