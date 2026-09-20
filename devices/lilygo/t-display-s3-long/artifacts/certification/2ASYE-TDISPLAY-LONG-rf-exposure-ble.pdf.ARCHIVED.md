# ARCHIVED: `2ASYE-TDISPLAY-LONG-rf-exposure-ble.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — rf exposure info, 169,460 B (0.16 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/lilygo/t-display-s3-long/artifacts/certification/2ASYE-TDISPLAY-LONG-rf-exposure-ble.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/lilygo/t-display-s3-long/artifacts/certification/2ASYE-TDISPLAY-LONG-rf-exposure-ble.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 169,460 B (0.16 MiB) |
| SHA-256 | `6af1e686fa63f85bd4e469d66e8116e42cce5f4044e39cacac652dc690b95054` |
| FCC ID | **`2ASYE-TDISPLAY-LONG`** |
| Exhibit type | **RF Exposure Info** |
| Exhibit title, as filed | RF Exposure - BLE |
| FCC document id | 7134150 |
| Upstream publication date | 2024-02-23 |
| Grant date | 2024-02-23 |
| Equipment class | T-Display-S3-Long, 2402-2480 MHz, 2412-2462 MHz |
| Applicant | Shenzhen Xin Yuan Electronic Technology Co., Ltd. 🇨🇳 |
| Test firm | CHINA CERTIFICATION ICT CO., LTD (DONGGUAN) |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2ASYE-TDISPLAY-LONG/RF-Exposure-Info/RF-Exposure-BLE-7134150.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=7134150>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2ASYE-TDISPLAY-LONG/7134150.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2ASYE-TDISPLAY-LONG>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2ASYE-TDISPLAY-LONG/RF-Exposure-Info/RF-Exposure-BLE-7134150.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/lilygo/t-display-s3-long/artifacts/certification/2ASYE-TDISPLAY-LONG-rf-exposure-ble.pdf" \
   "devices/lilygo/t-display-s3-long/artifacts/certification/2ASYE-TDISPLAY-LONG-rf-exposure-ble.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2ASYE-TDISPLAY-LONG/RF-Exposure-Info/RF-Exposure-BLE-7134150.pdf" -o "2ASYE-TDISPLAY-LONG-rf-exposure-ble.pdf"
echo "6af1e686fa63f85bd4e469d66e8116e42cce5f4044e39cacac652dc690b95054  2ASYE-TDISPLAY-LONG-rf-exposure-ble.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
