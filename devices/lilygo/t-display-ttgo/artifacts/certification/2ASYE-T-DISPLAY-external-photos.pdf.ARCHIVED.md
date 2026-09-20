# ARCHIVED: `2ASYE-T-DISPLAY-external-photos.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — external photos, 269,648 B (0.26 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/lilygo/t-display-ttgo/artifacts/certification/2ASYE-T-DISPLAY-external-photos.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/lilygo/t-display-ttgo/artifacts/certification/2ASYE-T-DISPLAY-external-photos.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 269,648 B (0.26 MiB) |
| SHA-256 | `1f1fce9575b54ebbbd9db1f421de4c34b903fed963fbc074048ae1e9bfde985e` |
| FCC ID | **`2ASYE-T-DISPLAY`** |
| Exhibit type | **External Photos** |
| Exhibit title, as filed | External Photos |
| FCC document id | 5793896 |
| Upstream publication date | 2022-04-01 |
| Grant date | 2022-04-01 |
| Equipment class | T-Display, 2402-2480 MHz, 2412-2462 MHz |
| Applicant | Shenzhen Xin Yuan Electronic Technology Co., Ltd. 🇨🇳 |
| Test firm | Shenzhen Accurate Technology Co., Ltd. |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2ASYE-T-DISPLAY/External-Photos/External-Photos-5793896.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=5793896>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2ASYE-T-DISPLAY/5793896.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2ASYE-T-DISPLAY>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2ASYE-T-DISPLAY/External-Photos/External-Photos-5793896.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/lilygo/t-display-ttgo/artifacts/certification/2ASYE-T-DISPLAY-external-photos.pdf" \
   "devices/lilygo/t-display-ttgo/artifacts/certification/2ASYE-T-DISPLAY-external-photos.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2ASYE-T-DISPLAY/External-Photos/External-Photos-5793896.pdf" -o "2ASYE-T-DISPLAY-external-photos.pdf"
echo "1f1fce9575b54ebbbd9db1f421de4c34b903fed963fbc074048ae1e9bfde985e  2ASYE-T-DISPLAY-external-photos.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
