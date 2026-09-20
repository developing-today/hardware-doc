# DinMeter v1.1 — acquisition

Machine-readable form: [`manifest.json`](manifest.json). Component artifacts (the Stamp-S3A
schematic, dimensions, STL, pin map) and all shared-carrier artifacts are manifested in
[`../../dinmeter/acquisition/`](../../dinmeter/acquisition/README.md).

**All 8 downloads returned HTTP 200 on 2026-09-04 and validated by magic bytes. Zero failures.**

---

## 0. Prerequisites

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
GH="$(gh auth token)"
```

## 1. v1.1 documents

```bash
cd devices/m5stack/dinmeter-v1.1/artifacts

curl -fSL -A "$UA" -o schematic/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58-schematic.pdf \
  'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1211/K134-V11_DIN_Meter_v1.0_2025_11_25_17_15_58.pdf'
# expect 433658 B, sha256 03ec335396e4f527119f89f697fca9887505dc1b28077871b2fb361ba6e4c070
#   ^ IDENTICAL to the v1.0 schematic. Verify this - it is one of the record's key findings.

curl -fSL -o mechanical/DinMeter_v1.1.stl \
  'https://raw.githubusercontent.com/m5stack/M5_Hardware/a240115c94b19ecf647f229c47fa9a8ce46ccdc4/Products/K134-V11_DinMeter_v1.1/Structures/DinMeter_v1.1.stl'
# expect 573284 B, sha256 90f04d6a0ae2cbb6f888065382da46ab1d699188ccebf1510963cc4aef00fbf7
#   ^ IDENTICAL to DinMeter.stl.

curl -fSL -A "$UA" -o docs/docs-en-core-DinMeter_v1.1.pdf \
  'https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/static/pdf/static/en/core/DinMeter_v1.1.pdf'
# expect 11261000 B, sha256 617a9ea8039ed1fced04cf68de4e12ccd1759140f5f440778b0638b2cc811b46
#   ^ ARCHIVED for size; the placeholder in docs/ holds the recovery URLs. Genuinely v1.1 content.
```

**Validate before trusting:**
```bash
python3 -c "
import sys
for f in sys.argv[1:]:
    m=open(f,'rb').read(5); print('OK ' if m==b'%PDF-' else 'BAD', f)" schematic/*.pdf docs/*.pdf
```

## 2. Reproducing the byte-identity findings

Two commands establish three of this record's central conclusions. **Run them.**

```bash
sha256sum schematic/K134-V11_*.pdf ../../dinmeter/artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf
sha256sum mechanical/DinMeter_v1.1.stl ../../dinmeter/artifacts/mechanical/DinMeter.stl
```
Both pairs must match. If a future fetch produces *different* hashes, M5Stack has finally
published v1.1-specific assets — which would be a significant change, and this record should be
revised.

## 3. Media

One WebP from the docs CDN and four images from the shop listing.

> **⚠ The four shop URLs end `.webp` but the CDN serves JPEG.** Shopify content-negotiates the
> format and ignores the path extension. They are stored locally as `.jpg` so the extension
> matches the content; the URLs in the manifest are exactly as served.
>
> **Validate by magic bytes, never by URL suffix.**

```bash
python3 - <<'EOF'
import json,urllib.request,hashlib,os
m=json.load(open('../media/manifest.json'))
for im in m['images']:
    p=os.path.join('..',im['local_path'])
    urllib.request.urlretrieve(im['direct_url'], p)
    b=open(p,'rb').read()
    ok = (b[:4]==b'RIFF' and b[8:12]==b'WEBP') or b[:3]==b'\xff\xd8\xff'
    assert ok, ('bad magic', p, b[:8])
    print('sha match' if hashlib.sha256(b).hexdigest()==im['sha256'] else 'HASH DIFFERS', p)
EOF
```
Shopify serves through a mutable CDN with a `?v=` cache-buster; a hash change there is expected
over time and is **not** the same kind of signal as §2.

## 4. Not acquired

| Artifact | Why | Reacquisition |
|---|---|---|
| **A v1.1-specific schematic** | **Does not exist.** M5Stack serves the v1.0 file | **lost** |
| **A v1.1-specific STL or footprint** | Does not exist | **lost** |
| **ST7789P3 datasheet** | Not published by Sitronix or any mirror; M5Stack removed the display datasheet link rather than replacing it | **lost** |
| **Stamp-S3A `U4` part number** | Not printed on the schematic, not stated on any page | **lost** |
| **v1.1 factory-firmware binary** | M5Burner only; no stable URL | **manual** |
| **UiFlow2 firmware binary** | Same | **manual** |
| **Gerbers / PCB / BOM** | M5Stack publishes schematics and STLs only | **blocked** |

## 5. Verify

```bash
cd devices/m5stack/dinmeter-v1.1
python3 - <<'EOF'
import json,hashlib,os
m=json.load(open('acquisition/manifest.json')); bad=0
for a in m['artifacts']:
    p=a['destination'].replace('devices/m5stack/dinmeter-v1.1/','')
    if a['disposition']=='archive':
        print('skip (archived; placeholder holds the hash):', p); continue
    if not os.path.exists(p): print('MISSING', p); bad+=1; continue
    got=hashlib.sha256(open(p,'rb').read()).hexdigest()
    if a['expected_sha256'] and got!=a['expected_sha256']: print('HASH MISMATCH', p); bad+=1
print('failures:', bad)
EOF
```
`not-tested` from a clean clone.
