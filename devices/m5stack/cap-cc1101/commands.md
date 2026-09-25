# Command ledger — Cap CC1101 & NFC (U219)

bash on NixOS, 2026-09-04. Shares tooling with
[`../cap-lora-1262/commands.md`](../cap-lora-1262/commands.md) — only the deltas are here.

## Acquisition

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
curl -sS -A "$UA" -o Cap_CC1101.html https://docs.m5stack.com/en/cap/Cap_CC1101
curl -sS -A "$UA" -o cap-cc1101.json https://shop.m5stack.com/products/cap-cc1101-nfc-for-cardputer.json
curl -sS -A "$UA" -o cap_cc1101_arduino.html https://docs.m5stack.com/en/arduino/projects/cap/cap_cc1101
curl -sSL -A "$UA" -o U219-Cap_CC1101_SCH_V0.3_20260528.pdf \
  https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1250/SCH_Cap_CC1101_SCH_V0.3_20260528.pdf
```
`executed-success` — 200 / 138 934 B, 200 / 17 082 B, 200 / 456 766 B, 200 / 485 518 B
(`%PDF-1.4`).

## Schematic extraction (3 sheets)

```bash
cd archive/devices/m5stack/shared-artifacts/lora-expansions/research-scratch
uv run --quiet --with pypdf python tools/pdf_bbox.py \
    artifacts/U219-Cap_CC1101_SCH_V0.3_20260528.pdf \
    pdf/U219-Cap_CC1101_SCH_V0.3_20260528
#  page 1: 178 words   page 2: 326 words   page 3: 448 words
for p in 1 2 3; do
  uv run --quiet python tools/sch_dump.py \
      pdf/U219-Cap_CC1101_SCH_V0.3_20260528/bbox-p$p.xml rows
done
```
`executed-success`.

Targeted region dumps that produced the pin tables:

```bash
# CC1101 (U3) body, sheet 3
uv run --quiet python /tmp/box.py pdf/U219-…/bbox-p3.xml  60 340  70 230
# balun + switches, sheet 3
uv run --quiet python /tmp/box.py pdf/U219-…/bbox-p3.xml 330 560 120 230
# buck + POWER_EN, sheet 1
uv run --quiet python /tmp/box.py pdf/U219-…/bbox-p1.xml  60 400 240 340
```
`executed-success` for the first three.

```bash
# RF-switch truth table, sheet 3
uv run --quiet python /tmp/box.py pdf/U219-…/bbox-p3.xml 380 620 470 540
```
**`executed-failed`** — returned only `SMA-TH_KH-SMA-KE-Z`, `PIE10*` and `GND`. The
truth-table grid (`√` / `x` glyphs) does not survive this extractor. **Diagnosis:** the
glyphs are likely a symbol font with no usable ToUnicode mapping, and the row/column
association is geometric rather than textual. **Consequence recorded as gap G1** — the
truth table in this record comes from the product page + Arduino guide + a vendor Reddit
comment, three agreeing sources, **none of them the schematic**.

## GitHub

```bash
GH="Authorization: Bearer $(gh auth token)"
curl -sS -H "$GH" "https://api.github.com/search/repositories?q=org%3Am5stack%20cc1101"
#   -> {"total_count": 0, ...}     NEGATIVE RESULT, executed-success
curl -sS -H "$GH" "https://api.github.com/search/code?q=CapCC1101NFC+repo:m5stack/M5Unit-NFC"
#   -> 38 hits, incl. src/M5UnitUnifiedNFC.hpp
curl -sSL -H "$GH" -o M5UnitUnifiedNFC.hpp \
  https://raw.githubusercontent.com/m5stack/M5Unit-NFC/93745b547364f310cd64b5155a870103a7800a5d/src/M5UnitUnifiedNFC.hpp
grep -n 'CapCC1101NFC' M5UnitUnifiedNFC.hpp
#   48:  using CapCC1101NFC = m5::unit::CapST25R3916;
```
`executed-success`. Pinning by **commit** rather than `main` matters here: the file is
1 250 B and the alias could move.

## Duplicate check before storing a datasheet

```bash
sha256sum components/stmicroelectronics/st25r3916/artifacts/st25r3916-datasheet-m5stack-mirror.pdf \
          archive/devices/m5stack/shared-artifacts/lora-expansions/research-scratch/artifacts/st25r3916_datasheet-m5stack-mirror.pdf
# 1170f4d74ff501917262ae42bf81c60c38c11d121e2ea2af6b1e845433befef1  (both)
```
`executed-success` → **not stored twice.** The `/1229/` URL was added to the component's
source table instead. Run this before filing *any* vendor-mirrored datasheet; M5Stack
serves the same document from multiple OSS paths.

## Not executed

No build, no flash, no on-device command. The `platformio.ini` in
[`development.md`](development.md) is **`inferred`** and was **not built**.
