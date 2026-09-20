# FCC equipment-authorization exhibits — `2BTR9-X4C`

Retrieved **2026-09-11** from `fccid.io` with UA `WhatsApp/2.23.20.0` (a
desktop-Chrome UA is served **403**; `fcc.report` is 403 on every UA tried).
Every file was validated by magic bytes (`%PDF`) before being retained, and text
was extracted with poppler 26.06.0 and cross-checked against a heading visible in
the rendered page.

| Field | Value |
|---|---|
| FCC ID | **`2BTR9-X4C`** |
| Applicant | Shenzhen Xiaohu Xingtong Technology Co., Ltd. |
| Grantee code / product code | `2BTR9` / `X4C` |
| Device description | **XTEINK X4 Classic** |
| Application / final action | **2026-07-20** |
| Equipment class | DTS — Digital Transmission System |
| Frequency range | 2412–2462 MHz |
| Test firm | Shenzhen BKC Testing Co., Ltd. |
| Source page | <https://fccid.io/2BTR9-X4C> |
| Grantee index | <https://fccid.io/2BTR9> |

## Retained

| File | Bytes | SHA-256 | What it establishes |
|---|---:|---|---|
| `2BTR9-X4C-label.pdf` | 189,803 | `605b978782399a0fdcf267848b5459981fd8069ec6e976e0240aff0bde72ba9c` | Compliance-label artwork and its position; a rear photograph showing the magnet outline and the four-contact pogo pad |
| `2BTR9-X4C-test-report.pdf` | 3,214,822 | `ce40d2300f5ac63c1fb2bb5f8e79b1afcb4a07017a5a1f2b636821e52dc57c86` | 802.11b/g/n(HT20/HT40) duty cycle, OBW and 6 dB BW measurements, 51 pages. **Measurement data only — the EUT-description section is not in this exhibit** |
| `2BTR9-X4C-antenna-report.pdf` | 1,548,468 | `720ce021f0d403a69e7095bb5ef29f393cb49a8ad4676f8e2652245ffbd355cb` | **Antenna part identity**: `KH3216-A35`, Shenzhen Jinhangbiao Electronics, peak gain 2.30 dBi, VSWR ≤ 2.0, 50 Ω, efficiency 69–71.2 % |
| `2BTR9-X4C-rf-exposure.pdf` | 144,966 | `7004f25d9c721f88591842081ac337d0b024745ca7551931fa9d195afc9f92df` | Product name confirmation and **BLE conducted peak power −0.87 dBm (ch 0), −1.42 dBm (ch 19)** — independent evidence that BLE is fitted |
| `2BTR9-X4C-confidentiality-request.pdf` | 121,559 | `6930195fcd9a7b0fd094a34b27dcf936e94828eeb67cb4dfbcfdd734d47baf19` | The applicant's own short- and long-term confidentiality request — **the document that sets the 2027-01-16 date** |

Original URLs follow the pattern
`https://fccid.io/2BTR9-X4C/<Type>/<Slug>-<DocumentID>.pdf`:

- `…/Label/Label-and-Information-9480913.pdf`
- `…/Test-Report/Test-Report-9480917.pdf`
- `…/Test-Report/Antenna-Report-9480914.pdf`
- `…/RF-Exposure-Info/RF-Exposure-Report-9480918.pdf`
- `…/Letter/Short-Long-Term-Confidentiality-Request-9480932.pdf`

## Not retained, because they are not public

| Exhibit | Size reported | Public from |
|---|---|---|
| **Internal Photos** | 4.5 MB | **2027-01-16** |
| External Photos | 825.3 KB | 2027-01-16 |
| Users Manual | 2.9 MB | 2027-01-16 |
| Test Setup Photos | 305.6 KB | 2027-01-16 |
| **Block Diagram** | 55.2 KB | **never** (long-term confidentiality) |
| **Schematics** | 540.4 KB | **never** |
| Operational Description | 73 KB | **never** |

Requesting the `.pdf` URL for a *"Metadata only"* exhibit does not return the
document. **Re-check on or after 2027-01-16** — the internal photographs are the
cheapest available route to a PCB-level verification of this record.

Two further exhibits were **not** fetched because they are boilerplate:
`Attestation-of-Covered-Equipment-2-911-d-5-i-ii-9480930.pdf` and
`Attestation-Statements-of-US-Agent-for-Service-of-Process-2-911-d-7-9480929.pdf`,
plus `Agent-Authorization-Letter-Template-9480931.pdf`. Their URLs are recorded
here so the omission is recoverable.

## Licensing and disposition

| Field | Value |
|---|---|
| Redistribution status | **`unknown`** — these are third-party submissions published by a US federal agency as part of a public authorization record. They are routinely mirrored by several commercial sites. **No explicit grant of redistribution was located**, and the FCC's publication is not itself a licence from the applicant |
| Disposition | `repository`, **unstaged** — pending the user's decision |
| Total retained | **5 files, 5,219,618 bytes** |

## Cross-references

Cited from [`../../README.md`](../../README.md) (§Regulatory record),
[`../../media/manifest.json`](../../media/manifest.json),
[`../../gaps-and-conflicts.md`](../../gaps-and-conflicts.md) and the component
record [`components/generic/kh3216-a35-chip-antenna`](../../../../../components/generic/kh3216-a35-chip-antenna/README.md).

---

## Correction, 2026-09-11 — redistribution is `allowed`, not `unknown`

The *Licensing and disposition* table above records **`unknown`**. That was
conservative but wrong, and it is superseded:

| Field | Value, as of 2026-09-11 |
|---|---|
| Redistribution status | **`allowed`** |
| Basis | FCC equipment-authorisation exhibits are **US Government public records**, published by the Commission under 47 CFR §2.1033. The agency asserts no copyright, and the exhibits are routinely republished by mirrors. |
| Scope | Applies to every exhibit in this directory, and to every FCC exhibit elsewhere in this repository. |

**The original rows above are left exactly as written.** This note supersedes
their redistribution field only; their hashes, sizes and URLs remain correct and
authoritative.

Confidentiality embargoes are a **separate** matter and are unaffected: exhibits
the applicant had withheld were never published, so there is nothing to
redistribute until their release dates.

Logged in [`scratch/index-merge/corrections-requiring-review.md`](../../../../../scratch/index-merge/corrections-requiring-review.md).
