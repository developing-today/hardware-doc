# ARCHIVED — `docs-en-core-M5DinMeter.pdf`

Printable ("PDF" page-tool) export of the official M5Stack **DinMeter (SKU K134)** product
documentation page, generated server-side by `docs.m5stack.com`.

| Field | Value |
|---|---|
| Original repository path | `devices/m5stack/dinmeter/artifacts/docs/docs-en-core-M5DinMeter.pdf` |
| Archived to | `archive/devices/m5stack/dinmeter/artifacts/docs/docs-en-core-M5DinMeter.pdf` |
| SHA-256 | `8b3db00abbc7e31762c503b36d8406fd8c6e21bdd23f89538989031ca1b70b3a` |
| Byte size | 7 459 888 |
| Media type | PDF (validated: `%PDF` magic, opens in pdfminer.six 20260107) |
| Retrieved | 2026-09-04 |
| Upstream version/date | **Not versioned.** M5Stack regenerates this file from the live page; the capture reflects the page as served on 2026-09-04 |
| Publisher | M5Stack Technology Co., Ltd |
| Licence | **unknown** — no licence statement on the page or in the PDF. Marketing/technical documentation, vendor copyright asserted in the page footer (`Copyright © M5Stack Technology Co., Ltd. All rights reserved.`) |
| Redistribution status | `unknown` |
| Disposition | `repository` → archived for size (7.5 MB of embedded product photography for ~5 KB of text) |
| Why moved | Size. Every fact it carries has been extracted into [`../../README.md`](../../README.md), [`../../pinouts-and-buses.md`](../../pinouts-and-buses.md) and the sibling text capture `docs-en-core-M5DinMeter.txt`, which is retained in the repository. |
| Reproducible? | **Yes, but not byte-stably.** The server re-renders on each request; a fresh fetch will differ in the PDF `/ID` and creation date. The *content* is reproducible while the page exists. |
| Reacquisition | `automatic` |

## Reacquisition

Two independent hosts, most reliable first:

1. **Vendor CDN (Alibaba OSS), direct** — the durable, machine-fetchable form:
   ```bash
   curl -fSL -o docs-en-core-M5DinMeter.pdf \
     'https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/static/pdf/static/en/core/M5DinMeter.pdf'
   ```
   Path template (see [`vendors/m5stack/README.md`](../../../../../vendors/m5stack/README.md)):
   `https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/static/pdf/static/en/<section>/<PageId>.pdf`
2. **The rendered page itself**, via the "PDF" button in *Page Tools*:
   <https://docs.m5stack.com/en/core/M5DinMeter> (retrieved 2026-09-04, HTTP 200).
   Note the page id is `M5DinMeter`, **not** `DinMeter` — `https://docs.m5stack.com/en/core/DinMeter`
   returns **HTTP 404** (verified 2026-09-04; this is the negative control for the path pattern).
3. **Internet Archive** — no capture was confirmed at the time of writing; submitting
   `https://web.archive.org/save/https://docs.m5stack.com/en/core/M5DinMeter` is the fallback.

## Also see

- Full acquisition record: [`../../acquisition/manifest.json`](../../acquisition/manifest.json)
- Text extraction retained in-repo: `docs-en-core-M5DinMeter.txt` (5 214 bytes)
- The v1.1 counterpart, archived under the same convention:
  [`devices/m5stack/dinmeter-v1.1/artifacts/docs/docs-en-core-DinMeter_v1.1.pdf.ARCHIVED.md`](../../../dinmeter-v1.1/artifacts/docs/docs-en-core-DinMeter_v1.1.pdf.ARCHIVED.md)
