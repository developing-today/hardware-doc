# ARCHIVED: `2AN3WM5DINMETER-user-manual.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-11** by the round-2 index merge.

**Reason:** bulk FCC exhibit — users manual, 2,021,122 B (1.93 MiB). The round-2 artifact split keeps internal photographs and ID-label exhibits in the repository (they are the identification and teardown evidence) and archives the full test reports, RF-exposure annexes, users manuals and external-photo sets, which are bulky and repetitive.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/m5stack/dinmeter/artifacts/certification/2AN3WM5DINMETER-user-manual.pdf` |
| Archived to | `/home/user/repo-archive/hardware-doc/devices/m5stack/dinmeter/artifacts/certification/2AN3WM5DINMETER-user-manual.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 2,021,122 B (1.93 MiB) |
| SHA-256 | `b472ab81821318a605ad749b318b9ec0626926669b567d756dd8b2378898015e` |
| FCC ID | **`2AN3WM5DINMETER`** |
| Exhibit type | **Users Manual** |
| Exhibit title, as filed | User Manual |
| FCC document id | 7497882 |
| Upstream publication date | 2024-07-23 |
| Grant date | 2024-07-23 |
| Equipment class | M5DinMeter, 2402-2480 MHz, 2412-2462 MHz |
| Applicant | M5Stack Technology Co.,Ltd 🇨🇳 |
| Test firm | Dongguan Yaxu (AiT) Technology Limited |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2AN3WM5DINMETER/User-Manual/User-Manual-7497882.pdf>  
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`, `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=7497882>  
  official FCC Equipment Authorization System attachment — the primary record. **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2AN3WM5DINMETER/7497882.pdf>  
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2AN3WM5DINMETER>  
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2AN3WM5DINMETER/User-Manual/User-Manual-7497882.pdf>  
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one:

```bash
mv "/home/user/repo-archive/hardware-doc/devices/m5stack/dinmeter/artifacts/certification/2AN3WM5DINMETER-user-manual.pdf" \
   "devices/m5stack/dinmeter/artifacts/certification/2AN3WM5DINMETER-user-manual.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2AN3WM5DINMETER/User-Manual/User-Manual-7497882.pdf" -o "2AN3WM5DINMETER-user-manual.pdf"
echo "b472ab81821318a605ad749b318b9ec0626926669b567d756dd8b2378898015e  2AN3WM5DINMETER-user-manual.pdf" | sha256sum -c -
```

The archive path above is a **convenience**. Everything needed to recover this file without the archive — hash, byte size, FCC ID, exhibit type, document id, publication date and 5 URLs — is in this file.
