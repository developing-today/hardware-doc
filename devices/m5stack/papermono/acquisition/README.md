# PaperMono — acquisition

How to reconstruct every artifact for this device record from a clean clone.
Manifest: [`manifest.json`](manifest.json) · Downloader: [`fetch.py`](fetch.py)

All retrieval dates are **2026-09-01**. Nothing here was flashed to or measured
on physical hardware.

## Quick start

```bash
cd devices/m5stack/papermono/acquisition
python3 fetch.py --verify-only     # CI / post-clone check; downloads nothing
python3 fetch.py                   # fetch anything missing (disposition=repository)
python3 fetch.py --reference-only  # also attempt reference-only entries
```

`fetch.py` is standard library only. It validates HTTP status, magic bytes,
byte size **and** SHA-256 before installing atomically, is idempotent, and never
stages or commits. Verified passing for all 14 repository artifacts on
2026-09-01.

## Where things live

Artifacts are filed under the component they **describe**, not under this
device. The manifest's `owned_by` field names that owner. This manifest lives
here because the PaperMono research is what caused the fetch.

| Count | Disposition |
|---|---|
| 14 | `repository` — present in the tree, hashed, verified |
| 10 | `reference-only` — 7 GitHub repositories, 3 unobtainable datasheets |

| Count | Reacquisition |
|---|---|
| 21 | `automatic` |
| 3 | `lost` |

## Execution order for a clean clone

1. **Device artifacts** — schematic and mechanical PDFs from
   `m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1267/`. `automatic`.
2. **Firmware** — via the M5Burner API (see trap below). `automatic`.
3. **Component datasheets** — nine files, each into its owning component's
   `artifacts/`. `automatic`, except ST which needs a specific user agent.
4. **Source repositories** — not vendored; clone at the pinned commits below.
5. **Unobtainable** — three parts, recorded as `lost` with their search ledgers.

## Source repositories (not vendored, pinned)

```bash
git clone https://github.com/m5stack/M5PaperMono-UserDemo && git -C M5PaperMono-UserDemo checkout c1099107271d31a0678d661a896e2b04dbb331ea
git clone https://github.com/m5stack/M5PaperMono-OTP-Demo  && git -C M5PaperMono-OTP-Demo  checkout c7c02554f89fd06f80d988b805b2a59050c78a46
git clone https://github.com/m5stack/M5PM1                 && git -C M5PM1                 checkout be9a5456c007c333e7ac963f33bfde1ffa5d82ee
git clone https://github.com/m5stack/M5IOE1                && git -C M5IOE1                checkout 846eec7d05e25c09013be2acdb8804487f48a62e
git clone https://github.com/m5stack/M5_Hardware           && git -C M5_Hardware           checkout a240115c94b19ecf647f229c47fa9a8ce46ccdc4
git clone https://github.com/m5stack/M5Unified             # master 8530f53
git clone https://github.com/m5stack/M5GFX                 # master d91077b
```

All seven are MIT; retain their `LICENSE` files with any vendored copy.
`M5_Hardware` is listed because its **absence of a C153 entry is the finding** —
verified at that commit, dated 2026-08-17.

## Retrieval traps that will bite a re-runner

| Host | Trap | Workaround |
|---|---|---|
| `st.com` | Chrome 131 and ClaudeBot UAs get a TLS stream reset | use UA `WhatsApp/2.23.20.0` |
| `datasheet.lcsc.com` | returns **HTTP 200 with `text/html`** for PDF URLs | check `%PDF` magic bytes, never the status code |
| `burner.m5stack.com` | `/api/firmwares/{id}` returns `401 请先登录` | `/api/v1/firmwares/{id}` is public; `/versions/{vid}/download` 302s to a CDN object named by a **numeric id**, not the `binFileName` the API reports |
| `semtech.com` | canonical datasheet is behind a Salesforce JS/POST shell | **`blocked`** — three strategies failed; the M5Stack mirror is what is held |
| `support.epson.biz` | serves the **English** manual under a `_cn` filename | `_cn` = Epson's China site, not Chinese language |
| `api.github.com` | 60 requests/hour unauthenticated; 403s look like bot-blocking | authenticate (`gh auth token`); check `X-RateLimit-Remaining` before rotating UAs |

`fetch.py` refuses to write a non-matching body under a `.pdf` or `.bin`
extension, so an error page cannot be silently saved as a datasheet.

## Reacquisition marked `lost`

No datasheet could be located for `CN4040M000157A530001` (40 MHz crystal),
`LMD4737T261-AC02` (PDM microphone) or `RS-C1415MBAR` (RGB LED), across 11+
services. For the latter two the only occurrences anywhere on the public web are
M5Stack's own pages. Instructions are not omitted — there are none. The search
ledgers are in the component records and in
[`../research-log.md`](../research-log.md).

## Licence decision needing user review

Both Epson RX8130CE manuals carry an **explicit no-redistribution notice** and
are marked `redistribution: restricted` while being **held in the repository**.
They were retained because the diff between revisions is itself a finding
(`ETM50E-10` *deletes* items (1)–(7) of §14.4.2, so the older mirror carries more
text; all registers, thresholds and timings are identical). This is flagged for a
decision rather than silently resolved either way.

Everything else is `unknown` (the normal case for vendor datasheets) or MIT
(the repositories).

## Firmware notes

Both images are ESP32 images (magic `0xE9`), validated by content before being
given a `.bin` extension.

The official `C153-PaperMono-UserDemo-v1.2.bin` reports version
**`c78f6c5-dirty`** — built from an uncommitted tree, therefore **not
reproducible from any published commit**. That is why the bytes are retained
here rather than merely referenced.

Flashing commands in the manifest are marked **`inferred`, not verified**. No
device was flashed in this pass. Prefer M5Burner over a hand-rolled
`esptool.py` invocation.
