# Command ledger — Cap LoRa-1262 (U214)

Shell: bash on NixOS. Date: 2026-09-04. Redacted: none (no secrets used beyond
`gh auth token`, never printed).

## 1. Acquisition

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
curl -sS -A "$UA" -o Cap_LoRa-1262.html https://docs.m5stack.com/en/cap/Cap_LoRa-1262
```
`executed-success` · HTTP 200 · 141 506 B. No UA rotation needed.

```bash
curl -sS -A "$UA" -o cap-lora-1262.json \
  https://shop.m5stack.com/products/cap-lora-1262-for-cardputer-adv-sx1262-atgm336h.json
```
`executed-success` · HTTP 200 · 19 450 B. **This is the single most valuable command in the
pass** — Shopify's `.json` endpoint returns `published_at`, `created_at`, SKU and price as
machine-readable fields, which is how the release-date correction was established.

Full catalogue enumeration (662 products, 3 pages; page 4 returns `{"products":[]}`):

```bash
for p in 1 2 3; do
  curl -sS -A "$UA" -o all$p.json \
    "https://shop.m5stack.com/collections/all/products.json?limit=250&page=$p"
done
```
`executed-success`.

Artifacts:

```bash
curl -sSL -A "$UA" -o U214-Cap-LoRa1262_SCH_V1.1_20251029.pdf \
  https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1208/U214-sche-Cap-LoRa1262_SCH_V1.1_20251029_2025_11_07_22_53_19.pdf
curl -sSL -A "$UA" -o Stamp-LoRa-1262-Mini_SCH_A1_20250827.pdf \
  https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1208/NEW-1262-SCH_A1-Lora_2025_08_27_10_58_52.pdf
```
`executed-success` · 155 866 B / 184 442 B · both `%PDF-1.4`, magic verified with
`head -c 8`.

## 2. Schematic text extraction — no poppler on this host

`pdftotext`, `pdfinfo` and `qpdf` are **absent**, so `tools/altium_pdf_pin_table.py`
had nothing to read. Workaround, from the repository root:

```bash
cd scratch/m5stack-lora-expansions
uv run --quiet --with pypdf python tools/pdf_bbox.py \
    artifacts/U214-Cap-LoRa1262_SCH_V1.1_20251029.pdf \
    pdf/U214-Cap-LoRa1262_SCH_V1.1_20251029
# -> page 1: 766 words -> pdf/.../bbox-p1.xml
```
`executed-success`.

```bash
uv run --quiet python tools/sch_dump.py \
    pdf/U214-Cap-LoRa1262_SCH_V1.1_20251029/bbox-p1.xml markers   # designator census
uv run --quiet python tools/sch_dump.py \
    pdf/U214-Cap-LoRa1262_SCH_V1.1_20251029/bbox-p1.xml rows      # row-banded text
uv run --quiet python tools/sch_dump.py \
    pdf/U214-Cap-LoRa1262_SCH_V1.1_20251029/bbox-p1.xml pins:M1   # per-designator
```
`executed-success` for `markers` and `rows`.
**`executed-failed` (partially) for `pins:`** — the synthesised word boxes are not aligned
the way pdftotext's are, so the "inside symbol / outside symbol" split misattributes text.
Diagnosis: pypdf's visitor reports the text-matrix origin, not a glyph box. **Every pin
assertion in this record therefore comes from the `rows` view cross-checked against
M5Stack's published pin-map graphic, never from `pins:` alone.**

Targeted region dump used instead:

```bash
uv run --quiet python /tmp/box.py \
    pdf/U214-Cap-LoRa1262_SCH_V1.1_20251029/bbox-p1.xml 540 720 480 535   # x0 x1 y0 y1
```
`executed-success` — this is what produced the `P1` header table in
[`pinouts-and-buses.md`](pinouts-and-buses.md).

## 3. GitHub (authenticated — 5 000/h instead of 60/h)

```bash
GH="Authorization: Bearer $(gh auth token)"
curl -sS -H "$GH" "https://api.github.com/repos/meshtastic/firmware/contents/variants/esp32s3/m5stack_cardputer_adv?ref=master"
curl -sS -H "$GH" "https://api.github.com/repos/meshtastic/firmware/commits?path=variants/esp32s3/m5stack_cardputer_adv&per_page=20"
curl -sS -H "$GH" "https://api.github.com/repos/meshtastic/firmware/pulls/9540"
```
`executed-success`. Never print the token.

Establishing *which release first contains a commit* — the load-bearing trick:

```bash
curl -sS -H "$GH" \
 "https://api.github.com/repos/meshtastic/firmware/compare/969aefa551d645e6110be11f330774e15ad9c87d...v2.7.20.6658ec2"
#   -> status "ahead",  ahead_by 17,  behind_by 0     => 2.7.20 CONTAINS it
curl -sS -H "$GH" \
 "https://api.github.com/repos/meshtastic/firmware/compare/969aefa551d645e6110be11f330774e15ad9c87d...v2.7.19.bb3d6d5"
#   -> status "behind", ahead_by 0,   behind_by 177   => 2.7.19 does NOT
```
`executed-success`. Far more reliable than reading release notes.

Checking whether a board is in a release without downloading a 143 MB zip:

```bash
curl -sSL -H "$GH" -o firmware-2.7.20.6658ec2.json \
  https://github.com/meshtastic/firmware/releases/download/v2.7.20.6658ec2/firmware-2.7.20.6658ec2.json
python3 -c "import json;print([x for x in sum(json.load(open('firmware-2.7.20.6658ec2.json')).values(),[]) if 'cardputer' in json.dumps(x).lower()])"
```
`executed-success` → `{"board": "m5stack-cardputer-adv", "platform": "esp32s3"}` (8 917 B
instead of 143 239 618 B).

## 4. Reddit

```bash
curl -sS -A 'WhatsApp/2.23.20.0' -o out.json \
  'https://old.reddit.com/search.json?q=cardputer+lora&sort=new&limit=100&t=all'
curl -sS -A 'WhatsApp/2.23.20.0' -o thread.json \
  'https://old.reddit.com/r/CardPuter/comments/1w0gv7y/.json?limit=100'
```
`executed-success` · HTTP 200 on all 18 calls. `www.reddit.com` was **not** attempted; the
repo's access table already records it as 403 for automated clients.

## 5. Verification

```bash
sha256sum artifacts/*.pdf
for f in artifacts/*.pdf; do printf '%-60s %s\n' "$f" "$(head -c 8 "$f")"; done   # %PDF-1.x
```
`executed-success` — all ten downloads are genuine PDFs; no HTML error page was saved under
a `.pdf` extension.

Duplicate detection against material already in the repository:

```bash
sha256sum components/stmicroelectronics/st25r3916/artifacts/st25r3916-datasheet-m5stack-mirror.pdf \
          scratch/m5stack-lora-expansions/artifacts/st25r3916_datasheet-m5stack-mirror.pdf
# identical: 1170f4d74ff501917262ae42bf81c60c38c11d121e2ea2af6b1e845433befef1
```
`executed-success` → the second copy was **not** stored; the extra URL was recorded instead.

## 6. Not executed

- No build, flash or on-device command was run. No hardware present.
- `pio run -e m5stack-cardputer-adv` in [`development.md`](development.md) is
  **`not-tested`**, transcribed from upstream `platformio.ini`.
