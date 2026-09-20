# DinMeter v1.1 — command ledger

The full ledger — environment, extraction tooling, the Altium double-draw trap, GitHub,
Reddit and the blocked forum — is **[`../dinmeter/commands.md`](../dinmeter/commands.md)**.
This page holds the commands that produced the v1.1-specific findings.

Status: `executed-success` · `executed-failed` · `reported-working` · `inferred` · `not-tested`.

---

## 1. The byte-identity checks — the highest-value commands in the pass

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

curl -fSL -A "$UA" -o v1.0-schematic.pdf \
  'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/500/DIN_Meter_v1.0.pdf'
curl -fSL -A "$UA" -o v1.1-schematic.pdf \
  'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf'
sha256sum v1.0-schematic.pdf v1.1-schematic.pdf
```
`executed-success`:
```
03ec335396e4f527119f89f697fca9887505dc1b28077871b2fb361ba6e4c070  v1.0-schematic.pdf
03ec335396e4f527119f89f697fca9887505dc1b28077871b2fb361ba6e4c070  v1.1-schematic.pdf
```

```bash
RAW=https://raw.githubusercontent.com/m5stack/M5_Hardware/a240115c94b19ecf647f229c47fa9a8ce46ccdc4
curl -fsSL -o DinMeter.stl      "$RAW/Products/K134_DinMeter/Structures/DinMeter.stl"
curl -fsSL -o DinMeter_v1.1.stl "$RAW/Products/K134-V11_DinMeter_v1.1/Structures/DinMeter_v1.1.stl"
curl -fsSL -o Stamp-S3.stl      "$RAW/Products/S007_Stamp-S3/Structures/Stamp-S3.stl"
curl -fsSL -o Stamp-S3A.stl     "$RAW/Products/S007-V033_Stamp-S3A/Structures/Stamp-S3A.stl"
sha256sum *.stl
```
`executed-success` — two identical pairs:
```
90f04d6a0ae2cbb6f888065382da46ab1d699188ccebf1510963cc4aef00fbf7  DinMeter.stl
90f04d6a0ae2cbb6f888065382da46ab1d699188ccebf1510963cc4aef00fbf7  DinMeter_v1.1.stl
f72c1af2d42930fc57a3db1bd3282568a3952095f77539016a12437d59d7df5d  Stamp-S3.stl
f72c1af2d42930fc57a3db1bd3282568a3952095f77539016a12437d59d7df5d  Stamp-S3A.stl
```

**Three findings, two commands.** Had the files simply been filed by name, all three would have
been recorded as "v1.1 documentation obtained".

## 2. Enumerating what M5_Hardware actually publishes

```bash
curl -sS -H "Authorization: Bearer $(gh auth token)" \
  'https://api.github.com/repos/m5stack/M5_Hardware/git/trees/master?recursive=1' \
| python3 -c "
import json,sys
d=json.load(sys.stdin); print('paths',len(d['tree']),'truncated',d.get('truncated'))
for t in sorted(x['path'] for x in d['tree']):
    if any(k in t for k in ('DinMeter','K134','S007','Stamp-S3','StampS3')): print(' ',t)"
```
`executed-success` — 931 paths, not truncated. Result: **`Stamp-S3-SMD`, `Stamp-S3-DIP`,
`Stamp-S3_PIN1.27_Socket`, `Stamp-S3_PIN2.54_DIP` footprints exist; there is NO Stamp-S3A
footprint and no `Stamp-S3A.step`.** Another negative finding, established by enumeration rather
than by searching for what was expected.

## 3. The two Stamp schematics, parsed and diffed

```bash
for f in Sch_M5StampS3_v0.2 Sch_StampS3_v0.3.3-StampS3A; do
  /tmp/opencode/.pdfvenv/bin/python /tmp/opencode/pdf_bbox.py "$f.pdf" > "$f.bbox.xml"
  python3 parse_dinmeter_sch.py "$f.bbox.xml" | head -4
done
```
`executed-success`:
```
Sch_M5StampS3_v0.2         words=927 plain=594 CO=54 PI=229 NL=50   -> 54 designators
Sch_StampS3_v0.3.3-StampS3A words=961 plain=609 CO=59 PI=243 NL=50  -> 59 designators
```

The diff (retained as
[`components/m5stack/stamp-s3a/artifacts/stamp-s3-vs-s3a-designator-diff.txt`](../../../components/m5stack/stamp-s3a/artifacts/stamp-s3-vs-s3a-designator-diff.txt)):
```
removed: D6 JP1 JP4 M2 R3 R6 R17
added:   C15 C16 C18 C19 C20 C24 C25 L4 L6 L7 U4
```

## 4. Proving the DC-DC conflict

```bash
for f in Sch_M5StampS3_v0.2 Sch_StampS3_v0.3.3-StampS3A; do
  printf '%-32s ' "$f"; grep -c 'MUN3CAD01-SC' "$f.bbox.xml"
done
```
`executed-success`: **1** on v0.2, **0** on v0.3.3 — while the Stamp-S3A product page still lists
`DC-DC: MUN3CAD01-SC`. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md) V4.

## 5. Establishing the RGB-LED prediction — a source read, not a test

```bash
grep -n "board_M5StampS3A\|board_M5DinMeter_v11\|GPIO_NUM_38" M5Unified/src/*.cpp M5Unified/src/**/*.cpp
# executed-success: NO MATCHES for any of the three

grep -n -A2 "_pin_table_other0" M5Unified/src/M5Unified.cpp | grep DinMeter
# executed-success: { board_t::board_M5DinMeter   , GPIO_NUM_21 },   (line 246)
```
at master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb`. **`inferred`** for the consequence; the
grep itself is `executed-success`.

## 6. Pricing and lifecycle

```bash
for s in m5stack-din-meter-v1-1-with-m5stamps3a m5stack-din-meter-w-m5stamps3 \
         m5stamp-esp32s3-module m5stamps3a-with-2-54-header-pin; do
  curl -sS -A "$UA" -L "https://shop.m5stack.com/products/$s.js" | python3 -c "
import json,sys; d=json.load(sys.stdin); v=d['variants'][0]
print(f\"{d['title'][:46]:<48} sku={v.get('sku'):<20} \${int(v['price'])/100:<6} avail={v['available']} pub={d.get('published_at','')[:10]}\")"
done
```
`executed-success`:
```
M5Stack Din Meter v1.1 with M5StampS3A     sku=K134-V11            $24.5  avail=True  pub=2026-01-30
[EOL] M5Stack Din Meter w/ M5StampS3       sku=K134                $24.5  avail=False pub=2024-03-08
[EOL] M5Stamp ESP32S3 Module               sku=S007                $7.5   avail=False pub=2023-02-10
M5StampS3A with 2.54 Header Pin            sku=S007-PIN254-V033    $7.5   avail=True  pub=2025-09-11
```
The `[EOL]` prefixes are M5Stack's own title text.

## 7. For the reader — `not-tested`

```cpp
// The one test that would settle this record's biggest open question, on a v1.1 unit:
pinMode(38, OUTPUT); digitalWrite(38, HIGH); delay(1);   // then drive GPIO21
// Run it once with these lines and once without. Report the difference.
```

Flash backup, restore and build commands are identical to v1.0's:
[`../dinmeter/commands.md` §10](../dinmeter/commands.md) and
[`factory-firmware.md`](factory-firmware.md).
