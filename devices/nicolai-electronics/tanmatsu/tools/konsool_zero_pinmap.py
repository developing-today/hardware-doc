import re,collections
PCB='/home/user/hardware-doc/devices/nicolai-electronics/tanmatsu/artifacts/konsool-zero/kicad/tanmantsu-zero.kicad_pcb'
IPC='/home/user/hardware-doc/devices/nicolai-electronics/tanmatsu/artifacts/production/netlist.ipc'
# --- konsool-zero J1 pin -> net, and net -> pads
src=open(PCB,encoding='utf-8',errors='replace').read()
nets=collections.defaultdict(list); j1={}
for m in re.finditer(r'\(footprint ',src):
    i=m.start();d=0;j=i
    while j<len(src):
        if src[j]=='(':d+=1
        elif src[j]==')':
            d-=1
            if d==0:break
        j+=1
    blk=src[i:j+1]
    r=re.search(r'\(property "Reference" "([^"]*)"',blk); r=r.group(1) if r else '?'
    for p in re.finditer(r'\(pad "([^"]*)"',blk):
        pi=p.start();dd=0;k=pi
        while k<len(blk):
            if blk[k]=='(':dd+=1
            elif blk[k]==')':
                dd-=1
                if dd==0:break
            k+=1
        nm=re.search(r'\(net \d+ "([^"]*)"\)',blk[pi:k+1])
        if nm:
            nets[nm.group(1)].append((r,p.group(1)))
            if r=='J1': j1[int(p.group(1))]=nm.group(1)
# --- Tanmatsu J7 pin -> net from IPC fab netlist
j7={}
for ln in open(IPC,encoding='utf-8',errors='replace'):
    m=re.match(r'^327(.{17})(.{6})-(\d+)',ln)
    if m and m.group(2).strip()=='J7': j7[int(m.group(3))]=m.group(1).strip()
# --- E-name -> GPIO, from the vendor back-expansion page (verified against fab data, gaps §14)
gpio={'E0':36,'E1':0,'E2':6,'E3':46,'E4':47,'E5':48,'E6':45,'E7':7,'E8':54,'E9':49,'E10':53,
      'E11':52,'E12':51,'E13':50,'EXT_USB_P':26,'EXT_USB_N':27,'P4_TX':37,'P4_RX':38,
      'INT_SCL':10,'INT_SDA':9,'I2S_MCLK':30,'I2S_LRCK':31,'I2S_DATA':28,'I2S_SCLK':29,
      'I3C_SDA':33,'I3C_SCL':32}
dom={'E3':'VSDCARD','E4':'VSDCARD','E5':'VSDCARD','E6':'VSDCARD'}
print("| J7/J1 pin | Tanmatsu net (fab netlist) | ESP32-P4 GPIO | konsool-zero net | konsool-zero function (loads) |")
print("|---:|---|---:|---|---|")
for p in sorted(j7):
    tn=j7[p]; kn=j1.get(p,'—')
    g=gpio.get(tn,''); g=str(g) if g!='' else '—'
    loads=[f"`{r}.{pad}`" for r,pad in nets.get(kn,[]) if r!='J1']
    mark=' ⚠' if tn!=kn else ''
    dmark=f" *({dom[tn]} domain)*" if tn in dom else ''
    print(f"| {p} | `{tn}`{dmark} | {g} | `{kn}`{mark} | {', '.join(loads) if loads else '— (not connected on konsool-zero)'} |")
