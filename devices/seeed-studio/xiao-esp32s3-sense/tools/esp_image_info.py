#!/usr/bin/env python3
"""Parse ESP-IDF firmware images and partition tables from raw .bin files.
Implements the documented ESP32 image format (magic 0xE9) and the
esp_app_desc_t application descriptor at offset 0x20 of an app image,
plus the 32-byte partition-table entry format (magic 0xAA50).
Executed 2026-08-24."""
import sys,struct,hashlib,os

CHIP={0:'ESP32',2:'ESP32-S2',5:'ESP32-C3',9:'ESP32-S3',12:'ESP32-C2',13:'ESP32-C6',16:'ESP32-H2',18:'ESP32-P4'}
FMODE={0:'QIO',1:'QOUT',2:'DIO',3:'DOUT'}
FSIZE={0:'1MB',1:'2MB',2:'4MB',3:'8MB',4:'16MB',5:'32MB'}
FFREQ={0x0:'40MHz',0x1:'26MHz',0x2:'20MHz',0xf:'80MHz'}
PTYPE={0:'app',1:'data'}
PSUB={(0,0):'factory',(0,16):'ota_0',(0,17):'ota_1',(0,32):'test',
      (1,0):'otadata',(1,1):'phy',(1,2):'nvs',(1,4):'nvs_keys',
      (1,0x80):'esphttpd',(1,0x81):'fat',(1,0x82):'spiffs',(1,0x83):'littlefs'}

def imginfo(p):
    b=open(p,'rb').read()
    print(f"\n### {os.path.basename(p)}")
    print(f"    size      {len(b):,} bytes")
    print(f"    sha256    {hashlib.sha256(b).hexdigest()}")
    if not b or b[0]!=0xE9:
        print("    (not an ESP image: magic %s)"%b[:1].hex()); return
    seg=b[1]; fmode=b[2]; fsf=b[3]
    ent=struct.unpack('<I',b[4:8])[0]
    wp,spi3,chip_id,mvl=b[8],b[9:12],struct.unpack('<H',b[12:14])[0],b[14]
    print(f"    magic     0xE9  segments={seg}  entry=0x{ent:08x}")
    print(f"    chip      {CHIP.get(chip_id,'?')} (id {chip_id})")
    print(f"    flash     mode={FMODE.get(fmode,'?')} size={FSIZE.get(fsf>>4,'?')} freq={FFREQ.get(fsf&0xf,'?')}")
    # app descriptor: after 8-byte img hdr + 16-byte extended hdr = 0x18, then
    # first segment header (8 bytes) -> payload at 0x20
    magic,secver=struct.unpack('<II',b[0x20:0x28])
    if magic==0xABCD5432:
        ver=b[0x30:0x50].split(b'\0')[0].decode('utf8','replace')
        name=b[0x50:0x70].split(b'\0')[0].decode('utf8','replace')
        t=b[0x70:0x80].split(b'\0')[0].decode('utf8','replace')
        d=b[0x80:0x90].split(b'\0')[0].decode('utf8','replace')
        idf=b[0x90:0xb0].split(b'\0')[0].decode('utf8','replace')
        elfsha=b[0xb0:0xd0].hex()
        print(f"    -- esp_app_desc_t --")
        print(f"    project   {name}")
        print(f"    app ver   {ver}")
        print(f"    built     {d} {t}")
        print(f"    IDF ver   {idf}")
        print(f"    elf sha256 {elfsha}")
    else:
        print(f"    (no app descriptor; magic 0x{magic:08x} — bootloader or non-app image)")

def parttable(p):
    b=open(p,'rb').read()
    print(f"\n### {os.path.basename(p)}  (partition table)")
    print(f"    size {len(b):,}  sha256 {hashlib.sha256(b).hexdigest()}")
    print(f"    {'Name':<12}{'Type':<6}{'SubType':<10}{'Offset':>10}{'Size':>12}  Flags")
    tot=0
    for i in range(0,len(b),32):
        e=b[i:i+32]
        if len(e)<32 or e[:2]!=b'\xaa\x50': break
        t,st=e[2],e[3]
        off,size=struct.unpack('<II',e[4:12])
        nm=e[12:28].split(b'\0')[0].decode('utf8','replace')
        fl=struct.unpack('<I',e[28:32])[0]
        print(f"    {nm:<12}{PTYPE.get(t,t):<6}{PSUB.get((t,st),hex(st)):<10}{'0x%06x'%off:>10}{'%d (%.0fK)'%(size,size/1024):>12}  {'encrypted' if fl&1 else ''}")
        tot=max(tot,off+size)
    print(f"    highest end offset: 0x{tot:06x} ({tot/1024/1024:.2f} MB of 8 MB)")

for f in sys.argv[1:]:
    if 'partition' in os.path.basename(f): parttable(f)
    else: imginfo(f)
