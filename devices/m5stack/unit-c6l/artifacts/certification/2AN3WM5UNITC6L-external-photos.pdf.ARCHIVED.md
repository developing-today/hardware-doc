# ARCHIVED: `2AN3WM5UNITC6L-external-photos.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — external photos, 569,103 B (0.54 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/m5stack/unit-c6l/artifacts/certification/2AN3WM5UNITC6L-external-photos.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/m5stack/unit-c6l/artifacts/certification/2AN3WM5UNITC6L-external-photos.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 569,103 B (0.54 MiB) |
| SHA-256 | `da57901ddd9a17f13444016de61985749404dcf83223ce0c57fcbf4b3af0df2b` |
| FCC ID | **`2AN3WM5UNITC6L`** |
| Exhibit type | **External Photos** |
| Exhibit title, as filed | External Photos |
| FCC document id | 8610509 |
| Upstream publication date | 2025-08-26 |
| Grant date | 2025-08-26 |
| Equipment class | M5Unit C6L, 2402-2480 MHz, 2412-2462 MHz, 902.3-914.9 MHz |
| Applicant | M5Stack Technology Co.,Ltd 🇨🇳 |
| Test firm | Shenzhen Accurate Technology Co., Ltd. |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2AN3WM5UNITC6L/External-Photos/External-Photos-8610509.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=8610509>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2AN3WM5UNITC6L/8610509.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2AN3WM5UNITC6L>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2AN3WM5UNITC6L/External-Photos/External-Photos-8610509.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/m5stack/unit-c6l/artifacts/certification/2AN3WM5UNITC6L-external-photos.pdf" \
   "devices/m5stack/unit-c6l/artifacts/certification/2AN3WM5UNITC6L-external-photos.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2AN3WM5UNITC6L/External-Photos/External-Photos-8610509.pdf" -o "2AN3WM5UNITC6L-external-photos.pdf"
echo "da57901ddd9a17f13444016de61985749404dcf83223ce0c57fcbf4b3af0df2b  2AN3WM5UNITC6L-external-photos.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
