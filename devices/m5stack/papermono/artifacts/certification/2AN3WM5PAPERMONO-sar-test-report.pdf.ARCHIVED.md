# ARCHIVED: `2AN3WM5PAPERMONO-sar-test-report.pdf`

> This file was **moved out of the repository**, not deleted.
> Archived **2026-09-20** when the `2AN3WM5PAPERMONO` filing was filed out of scratch.

**Reason:** bulk FCC exhibit — the SAR report, 34 pp. **Fully mined** into [`certification.md`](../../certification.md) — conducted power per mode, the antenna-location map, the standalone and simultaneous SAR exclusion arithmetic, and the 0 mm test separation.

This directory follows the repository's established FCC split (see the sibling
`devices/m5stack/dinmeter` and `devices/m5stack/cardputer-adv` records):
**Internal Photos** and **ID Label / Location Info** stay in the repository because
they are the identification and teardown evidence; test reports, RF-exposure
annexes, users manuals and external-photo sets are archived.

## Identity

| Field | Value |
|---|---|
| Original repo path | `devices/m5stack/papermono/artifacts/certification/2AN3WM5PAPERMONO-sar-test-report.pdf` |
| Archived to | `archive/devices/m5stack/papermono/artifacts/certification/2AN3WM5PAPERMONO-sar-test-report.pdf` |
| Type | file (PDF, magic-byte validated `%PDF`) |
| Size | 1,718,829 B (1.64 MiB) |
| SHA-256 | `81127b874e18936fb005bf8688af350b27643b1c3e0607444ada20ae8174d982` |
| FCC ID | **`2AN3WM5PAPERMONO`** |
| Exhibit type | **RF Exposure Info** |
| Exhibit title, as filed | SAR Test Report |
| FCC document id | 9552983 |
| Upstream publication date | 2026-08-12 |
| Grant date | 2026-08-12 |
| Equipment class | Digital Transmission System (2402–2480 / 2412–2462 / 2422–2452 / 903–914.9 MHz) + Part 15 Low Power Communication Device Transmitter (13.56 MHz) |
| Applicant | M5Stack Technology Co.,Ltd |
| Test firm | Shenzhen Accurate Technology Co., Ltd. (A2LA cert. 4297.01) |
| TCB | Bay Area Compliance Laboratories Corp., Sunnyvale CA |
| Retrieved | 2026-09-11 |
| Licence | **US Government public record.** FCC equipment-authorisation exhibits are published by a federal agency under 47 CFR §2.1033 and carry no copyright claim by the agency. |
| Redistribution status | **`allowed`** |
| Disposition | `archive`, placeholder in repository |

## How to get it back

Independent reacquisition URLs, most reliable first:

- <https://fccid.io/2AN3WM5PAPERMONO/RF-Exposure-Info/SAR-Test-Report-9552983.pdf>
  fccid.io mirror — **200**, but only to a non-browser UA (`curl/8.5.0`,
  `WhatsApp/2.23.20.0`, `ChatGPT-User/1.0`, `ClaudeBot/1.0`). A Chrome UA gets a
  Cloudflare 403. The `.pdf` suffix is required.

- <https://apps.fcc.gov/eas/GetApplicationAttachment.html?id=9552983>
  official FCC Equipment Authorization System attachment — the primary record.
  **403 to all five UAs tried from this host on 2026-09-11**; try from another network.

- <https://fcc.report/FCC-ID/2AN3WM5PAPERMONO/9552983.pdf>
  fcc.report mirror. **403 to all five UAs tried on 2026-09-11.**

- <https://fccid.io/2AN3WM5PAPERMONO>
  the filing's exhibit index — re-read the row to recover a changed document slug.

- <https://web.archive.org/web/2/https://fccid.io/2AN3WM5PAPERMONO/RF-Exposure-Info/SAR-Test-Report-9552983.pdf>
  Wayback Machine, if every live route is dead.

Restore from the local archive, if you have one — run from the repository root:

```bash
mv "archive/devices/m5stack/papermono/artifacts/certification/2AN3WM5PAPERMONO-sar-test-report.pdf" \
   "devices/m5stack/papermono/artifacts/certification/2AN3WM5PAPERMONO-sar-test-report.pdf"
```

Or re-download and verify — note the User-Agent, which is not optional:

```bash
curl -fsSL -A "curl/8.5.0" "https://fccid.io/2AN3WM5PAPERMONO/RF-Exposure-Info/SAR-Test-Report-9552983.pdf" -o "2AN3WM5PAPERMONO-sar-test-report.pdf"
echo "81127b874e18936fb005bf8688af350b27643b1c3e0607444ada20ae8174d982  2AN3WM5PAPERMONO-sar-test-report.pdf" | sha256sum -c -
```

The archive path above is a **convenience** (`archive/` is a tracked symlink to a
machine-local sibling repository and will not exist in a fresh clone). Everything
needed to recover this file without the archive — hash, byte size, FCC ID, exhibit
type, document id, publication date and five URLs — is in this file.

Mined into [`certification.md`](../../certification.md); directory index:
[`README.md`](README.md).
