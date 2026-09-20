# ARCHIVED: `2AC7Z-ESPS3WROOM1-sar-report.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — rf exposure info, 1,936,491 B (1.85 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `components/espressif/esp32-s3-wroom-1/artifacts/certification/2AC7Z-ESPS3WROOM1-sar-report.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/components/espressif/esp32-s3-wroom-1/artifacts/certification/2AC7Z-ESPS3WROOM1-sar-report.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 1,936,491 B (1.85 MiB) |
| SHA-256 | `60f7208dd54ccff8d2af1d93c2e7d706c2259d0f2b9de6563b606057d49ba7a4` |
| FCC ID | **`2AC7Z-ESPS3WROOM1`** |
| Exhibit type | **RF Exposure Info** |
| Exhibit title, as filed | SAR Report |
| FCC document id | 9104679 |
| Upstream publication date | 2026-02-27 |
| Grant date | 2026-02-27 |
| Equipment class | BrushBot, 2402-2480 MHz, 2412-2462 MHz |
| Applicant | ESPRESSIF SYSTEMS (SHANGHAI) CO., LTD 🇨🇳 |
| Test firm | SGS-CSTC Standards Technical Services Co., Ltd. |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2AC7Z-ESPS3WROOM1/RF-Exposure-Info/SAR-Report-9104679.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=9104679>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2AC7Z-ESPS3WROOM1/9104679.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2AC7Z-ESPS3WROOM1>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2AC7Z-ESPS3WROOM1/RF-Exposure-Info/SAR-Report-9104679.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/components/espressif/esp32-s3-wroom-1/artifacts/certification/2AC7Z-ESPS3WROOM1-sar-report.pdf" \
   "components/espressif/esp32-s3-wroom-1/artifacts/certification/2AC7Z-ESPS3WROOM1-sar-report.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2AC7Z-ESPS3WROOM1/RF-Exposure-Info/SAR-Report-9104679.pdf" -o "2AC7Z-ESPS3WROOM1-sar-report.pdf"
echo "60f7208dd54ccff8d2af1d93c2e7d706c2259d0f2b9de6563b606057d49ba7a4  2AC7Z-ESPS3WROOM1-sar-report.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
