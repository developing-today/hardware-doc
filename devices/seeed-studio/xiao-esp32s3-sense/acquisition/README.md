# Acquisition — XIAO ESP32S3 Sense

Everything in [`../artifacts/`](../artifacts/) was downloaded on **2026-08-24**, validated by content type (PDF magic bytes, ZIP integrity test) and hashed from the local bytes. [`manifest.json`](manifest.json) is the machine-readable record: 42 artifacts, ~127 MB.

## Reacquiring everything from a clean clone

All 42 artifacts come from `files.seeedstudio.com`, which serves them over plain HTTPS with no authentication. A browser User-Agent is **not** required for `files.seeedstudio.com` (unlike `wiki.seeedstudio.com`, see below).

```bash
python3 - <<'PY'
import json, urllib.request, hashlib, os
m = json.load(open("acquisition/manifest.json"))
for a in m["artifacts"]:
    d = a["destination"].split("xiao-esp32s3-sense/", 1)[1]
    if os.path.exists(d): continue
    os.makedirs(os.path.dirname(d), exist_ok=True)
    b = urllib.request.urlopen(a["url"], timeout=300).read()
    got = hashlib.sha256(b).hexdigest()
    assert got == a["sha256"], f"{d}: expected {a['sha256']} got {got}"
    open(d, "wb").write(b)
    print("ok", d)
PY
```

Status: **`inferred`** — mechanically equivalent to the download actually performed (which was `executed-success` for all 42), but this exact script was not run.

## The wiki snapshot is acquired differently

[`../artifacts/wiki-snapshot/`](../artifacts/wiki-snapshot/) holds **230 Markdown files** — the complete official Seeed wiki source for this product family. It was *not* scraped from `wiki.seeedstudio.com`.

**`wiki.seeedstudio.com` renders as a JavaScript shell.** Fetching a wiki page with `curl` returns ~150 KB of HTML containing exactly **one** `href` (a Cloudflare email-protection link). The documentation text and every resource link are injected client-side, so ordinary scraping yields nothing usable.

The wiki is open-source. The real source is:

- **Repo:** `Seeed-Studio/wiki-documents`
- **Branch:** `docusaurus-version` (**not** `main` — `main` returns 404; `master` exists but has a different, much smaller tree)
- **Path prefix:** `sites/<lang>/docs/...` where `<lang>` ∈ `en`, `zh-CN`, `ja`, `pt-BR`

```bash
# enumerate everything
curl -fsSL "https://api.github.com/repos/Seeed-Studio/wiki-documents/git/trees/docusaurus-version?recursive=1" \
  | python3 -c "import json,sys;[print(t['path']) for t in json.load(sys.stdin)['tree'] if 'XIAO_ESP32S3' in t['path']]"

# fetch one page's real source
curl -fsSL "https://raw.githubusercontent.com/Seeed-Studio/wiki-documents/docusaurus-version/sites/en/docs/Sensor/SeeedStudio_XIAO/SeeedStudio_XIAO_ESP32S3/XIAO_ESP32S3_Getting_Started.md"
```

Status: **`executed-success`** — this is how the snapshot was actually built. The tree API call returned 16,372 entries; 230 matched and all 230 downloaded without error.

This is the single most useful sourcing technique found in this pass, and it generalises to every Seeed product. It is recorded in the [Seeed vendor guide](../../../../vendors/seeed-studio/README.md).

## Known vendor traps

1. **`202003751_XIAO ESP32S3_v1.4_SCH_260226.pdf.pdf`** — advertised as the *non-Sense* schematic, actually serves the **Sense v1.5** file. Byte-identical to `202003753_...Sense_v1.5...`. The wiki's own "Resources → XIAO ESP32-S3 Schematic" link points at it. See [`../gaps-and-conflicts.md` §1](../gaps-and-conflicts.md#1-seeed-serves-the-wrong-file-under-the-xiao-esp32s3-v14-schematic-url).
2. **Double `.pdf.pdf` extension** in that filename is genuine — not a typo in this document.
3. **URLs contain spaces and `&`**, percent-encoded (`%20`). Quote them in shells.
4. **Two firmware "releases" contain identical binaries** — see [`../factory-firmware.md` §1.1](../factory-firmware.md#11-the-two-releases-contain-identical-firmware).

## Licensing summary

Findings, not legal advice. Full per-artifact detail in [`manifest.json`](manifest.json).

| Redistribution status | Count | Examples |
|---|---:|---|
| **`allowed`** | 14 | All schematics and KiCad libraries — **CC BY-SA 4.0**, stated on every schematic sheet |
| **`conditional`** | 1 | Espressif ESP32-S3 datasheet (attribution) |
| **`restricted`** | 4 | **OV3660 / OV5640 datasheets and module specs** — explicitly state *"Individuals and/or organizations are not allowed to re-distribute said information."* |
| **`unknown`** | 23 | Firmware bundles, CAD/3D assets, pinout spreadsheets, the reference-design catalogue — Seeed publishes these as support downloads with no stated terms |

**13 artifacts over 1 MB are flagged in `manifest.json` under `review_required`** because they combine size with `restricted` or `unknown` terms. They are currently **staged** in the repository at the user's explicit instruction to keep all documents in place for now. The notable ones:

- `ov3660-datasheet.pdf` (1.9 MB) and `ov5640-datasheet.pdf` (1.7 MB) — **explicit no-redistribution clause**
- `xiao-reference-design.pdf` (49.9 MB) — largest single artifact; no stated terms; contains third-party project descriptions
- The four firmware ZIPs (~35 MB combined) — mixed LGPL/Apache/GPL provenance, no stated terms, and two pairs are byte-identical duplicates of each other

The good news is that **the material that mattered most for this research — the schematics and PCB design files — is CC BY-SA 4.0**, which is why the netlist-derived documentation in this tree could be published at all.

## Related

- [`manifest.json`](manifest.json) — per-artifact hashes, sizes, licences, disposition
- [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md) — vendor data errors found during acquisition
- [`../../../../vendors/seeed-studio/README.md`](../../../../vendors/seeed-studio/README.md) — reusable Seeed sourcing patterns
