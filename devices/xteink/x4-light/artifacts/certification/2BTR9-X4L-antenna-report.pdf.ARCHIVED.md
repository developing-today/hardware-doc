# ARCHIVED: `2BTR9-X4L-antenna-report.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — test report, 1,563,068 B (1.49 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/xteink/x4-light/artifacts/certification/2BTR9-X4L-antenna-report.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/xteink/x4-light/artifacts/certification/2BTR9-X4L-antenna-report.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 1,563,068 B (1.49 MiB) |
| SHA-256 | `9de0e036e525f5e6ca232f2e41ee07ffda5192fbe6e75d4bf9840e65ae19de04` |
| FCC ID | **`2BTR9-X4L`** |
| Exhibit type | **Test Report** |
| Exhibit title, as filed | Antenna Report |
| FCC document id | 9556499 |
| Upstream publication date | 2026-08-13 |
| Grant date | 2026-08-13 |
| Equipment class | XTEINK X4 Light, 2402-2480 MHz, 2412-2462 MHz |
| Applicant | Shenzhen Xiaohu Xingtong Technology Co., Ltd. 🇨🇳 |
| Test firm | Shenzhen BKC Testing Co., Ltd. |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2BTR9-X4L/Test-Report/Antenna-Report-9556499.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=9556499>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2BTR9-X4L/9556499.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2BTR9-X4L>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2BTR9-X4L/Test-Report/Antenna-Report-9556499.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/xteink/x4-light/artifacts/certification/2BTR9-X4L-antenna-report.pdf" \
   "devices/xteink/x4-light/artifacts/certification/2BTR9-X4L-antenna-report.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2BTR9-X4L/Test-Report/Antenna-Report-9556499.pdf" -o "2BTR9-X4L-antenna-report.pdf"
echo "9de0e036e525f5e6ca232f2e41ee07ffda5192fbe6e75d4bf9840e65ae19de04  2BTR9-X4L-antenna-report.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
