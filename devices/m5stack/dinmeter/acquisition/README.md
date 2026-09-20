# DinMeter — acquisition

How to reproduce every artifact in this record from a clean clone. Machine-readable form:
[`manifest.json`](manifest.json).

**Everything below was executed successfully on 2026-09-04**, except where marked. All 20
downloads returned HTTP 200 and validated by magic bytes; **zero failures**.

---

## 0. Prerequisites

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
GH="$(gh auth token)"          # api.github.com limits per identity: 60/h -> 5000/h
```

No fallback User-Agent was needed for any `m5stack.com` host. `api.github.com` requires the token
(no UA helps — the limit is per identity, and a 403 there carries `X-RateLimit-Remaining: 0`).

## 1. Vendor documents — in execution order

```bash
cd devices/m5stack/dinmeter/artifacts

# PRIMARY EVIDENCE: the schematic
curl -fSL -A "$UA" -o schematic/K134_DIN_Meter_v1.0-schematic.pdf \
  'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/500/DIN_Meter_v1.0.pdf'
# expect 433658 B, sha256 03ec335396e4f527119f89f697fca9887505dc1b28077871b2fb361ba6e4c070

curl -fSL -A "$UA" -o mechanical/K134-din_meter_asm_v1-dimensions.pdf \
  'https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1211/K134-din_meter_asm_v1.pdf'
# expect 117405 B, sha256 db42c8a995b6d0bf8032ee32f60e65307dca42c7c48898b1760e183c0706e579

# Documentation PDF (large -> archived; see the placeholder in docs/)
curl -fSL -A "$UA" -o docs/docs-en-core-M5DinMeter.pdf \
  'https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/static/pdf/static/en/core/M5DinMeter.pdf'
# expect 7459888 B, sha256 8b3db00abbc7e31762c503b36d8406fd8c6e21bdd23f89538989031ca1b70b3a
```

**Validate before trusting** — M5Stack's CDN returns HTML for a wrong path with a 200 in some
cases:

```bash
python3 -c "
import sys
for f in sys.argv[1:]:
    m=open(f,'rb').read(5)
    print('OK ' if m==b'%PDF-' else 'BAD', m, f)" schematic/*.pdf mechanical/*.pdf docs/*.pdf
```

## 2. Mechanical model (GitHub raw, pinned)

```bash
curl -fSL -o mechanical/DinMeter.stl \
 'https://raw.githubusercontent.com/m5stack/M5_Hardware/a240115c94b19ecf647f229c47fa9a8ce46ccdc4/Products/K134_DinMeter/Structures/DinMeter.stl'
# expect 573284 B, sha256 90f04d6a0ae2cbb6f888065382da46ab1d699188ccebf1510963cc4aef00fbf7
# NOTE: this is byte-identical to Products/K134-V11_DinMeter_v1.1/Structures/DinMeter_v1.1.stl
```

## 3. Source snapshots (pinned commits)

```bash
curl -fSL -H "Authorization: Bearer $GH" \
  -o source-snapshots/M5DinMeter-8ccbad7297beb82a140f812e5606e060d8a5e0dc.tar.gz \
  'https://api.github.com/repos/m5stack/M5DinMeter/tarball/8ccbad7297beb82a140f812e5606e060d8a5e0dc'
# expect 8532 B, sha256 de47c4109635870506bb7a02040db496f82e5bbb22a5b1befe600a3985eb0f02

curl -fSL -H "Authorization: Bearer $GH" \
  -o source-snapshots/M5DinMeter-UserDemo-d2fdfe44e9baf810f82335faa6f5962e9fc59a44.tar.gz \
  'https://api.github.com/repos/m5stack/M5DinMeter-UserDemo/tarball/d2fdfe44e9baf810f82335faa6f5962e9fc59a44'
# expect 74231 B, sha256 af58e2cdaf565bb3f97daeadd02843a4cd3dc72f504446aa842d865eb9c4ec72
```

> **⚠ GitHub tarballs are not byte-stable across time.** `api.github.com/.../tarball/<sha>`
> re-generates the archive, and gzip/mtime differences mean the SHA-256 above may not reproduce
> even from the same commit. **The commit hash is the identity; the archive hash is a
> convenience.** If they disagree, verify the *contents* against the commit.

### Board-support files (small, high value)

```bash
for f in board_info board_devices board_peripherals; do
  curl -fSL -o "source-snapshots/dinmeter-$f.yaml" \
   "https://raw.githubusercontent.com/espressif/esp-board-manager/2beb9b22b0892b343bd555a1ebc9929a7edce8fc/m5stack_boards/m5stack_dinmeter/$f.yaml"
done
# NOTE: the originals were fetched from the MOVING 'main' ref; the pinned form above is preferred.

curl -fSL -o source-snapshots/launcher-m5stack-dinmeter-platformio.ini \
 'https://raw.githubusercontent.com/bmorcelli/Launcher/main/boards/m5stack-dinmeter/platformio.ini'
# ⚠ fetched from the MOVING 'main' ref on 2026-09-04. A future fetch may differ. No release was pinned at capture.
```

## 4. Media

Ten WebP images from `static-cdn.m5stack.com/resource/docs/products/core/M5DinMeter/`. Filenames,
URLs and hashes: [`../media/manifest.json`](../media/manifest.json).

```bash
python3 - <<'EOF'
import json,urllib.request,hashlib,os
m=json.load(open('../media/manifest.json'))
for im in m['images']:
    p=os.path.join('..',im['local_path'])
    urllib.request.urlretrieve(im['direct_url'], p)
    b=open(p,'rb').read()
    assert b[:4]==b'RIFF' and b[8:12]==b'WEBP', p
    assert hashlib.sha256(b).hexdigest()==im['sha256'], p
    print('ok', p)
EOF
```

## 5. Regenerating the derived analysis

Seven files under `artifacts/schematic/` are derived from the schematic PDF, not downloaded.

```bash
# pdfminer.six is required. On a host without poppler/pypdf:
uv venv /tmp/.pdfvenv && uv pip install --python /tmp/.pdfvenv/bin/python pdfminer.six
# NOTE: pymupdf installs but fails to import on NixOS (missing libstdc++.so.6). pdfminer.six is pure Python and works.

/tmp/.pdfvenv/bin/python <path-to>/pdf_bbox.py \
    artifacts/schematic/K134_DIN_Meter_v1.0-schematic.pdf \
  > artifacts/schematic/K134_DIN_Meter_v1.0-schematic.bbox.xml

python3 artifacts/schematic/parse_dinmeter_sch.py \
    artifacts/schematic/K134_DIN_Meter_v1.0-schematic.bbox.xml \
  > artifacts/schematic/K134_DIN_Meter_v1.0-designator-census.txt
```

**`pdf_bbox.py` must deduplicate glyphs** on rounded `(x0,y0,x1,y1,char)`. Altium draws the
marker layer twice at identical coordinates; without dedup the copies interleave and `PIJ10101`
extracts as `PPIIJJ110011` — legible-looking and wrong. See [`../commands.md`](../commands.md) §4.

## 6. Component artifacts — fetched here but filed elsewhere

Filed by what they *describe*, not by what was being researched:

| Artifact | Lives at |
|---|---|
| ST7789V2 datasheet (3 216 854 B) | `components/sitronix/st7789v2/artifacts/` |
| BM8563 datasheet (590 599 B) | `components/generic/bm8563/artifacts/` |
| TP4057 datasheet (628 588 B) | `components/generic/tp4057/artifacts/` |
| MUN3CAD01-SC datasheet (2 045 960 B) | `components/murata/mun3cad01-sc/artifacts/` |
| Stamp-S3 schematic, footprints, STL, STEP, pin map | `components/m5stack/stamp-s3/artifacts/` |
| Stamp-S3A schematic, dimensions, STL, pin map | `components/m5stack/stamp-s3a/artifacts/` |

## 7. Not acquired

| Artifact | Why | Reacquisition |
|---|---|---|
| **Factory firmware binary** | Distributed only through M5Burner, which resolves images at run time from an undocumented endpoint | **manual** — run M5Burner, search "DinMeter", *DinMeter User Demo Easyloader*. Or rebuild from the MIT source (A-14) |
| **UiFlow2 firmware binary** | Same channel, same problem | **manual** |
| **ST7789P3 datasheet** | Does not exist publicly; M5Stack removed the display datasheet link on the v1.1 page rather than replacing it | **lost** |
| **ME3116AM6G / SY7088 / BL8075 / SGM2578 datasheets** | Not published by any locatable source | **lost** |
| **Gerbers / PCB / BOM** | M5Stack publishes schematics and STLs only | **blocked** |
| **M5Unified / M5GFX source** | Large and canonical; reproducible from the commits in [`../sources.md`](../sources.md) | **automatic** |

## 8. Verify

```bash
cd devices/m5stack/dinmeter
python3 - <<'EOF'
import json,hashlib,os
m=json.load(open('acquisition/manifest.json')); bad=0
for a in m['artifacts']:
    p=a['destination'].replace('devices/m5stack/dinmeter/','')
    if a['disposition']=='archive':
        print('skip (archived, placeholder holds the hash):', p); continue
    if not os.path.exists(p): print('MISSING', p); bad+=1; continue
    got=hashlib.sha256(open(p,'rb').read()).hexdigest()
    if a['expected_sha256'] and got!=a['expected_sha256']:
        print('HASH MISMATCH', p); bad+=1
print('failures:', bad)
EOF
```
`not-tested` from a clean clone; it is the same logic used to build the manifest, run in reverse.
