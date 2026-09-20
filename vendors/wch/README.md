# WCH (Nanjing Qinheng Microelectronics) — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation for **any** WCH part. WCH is unusual: the
documentation is genuinely good, genuinely public, and behind a URL scheme that is **opaque numeric
IDs** rather than part numbers.

> **TL;DR** — **Do not use the `downloads/<PART>DS1_PDF.html` URLs.** `wch-ic.com` is a Vue SPA that
> returns **HTTP 200 and an identical 4,305-byte app shell for every path**, including paths that do
> not exist (verified 2026-08-24 against a deliberately bogus path, S3). Use the **JSON API** instead:
> `https://www.wch-ic.com/api/official/website/files/getFilesById?id=<N>` for metadata and
> `https://www.wch-ic.com/download/file?id=<N>` for the PDF, enumerating `N` over roughly 1–800 (S4).
> And search the metadata's **`scope`** field, not document titles — see §5.

---

## 1. Who they are

Nanjing Qinheng Microelectronics Co., Ltd. — 南京沁恒微电子, trading internationally as **WCH** — is a
Chinese fabless semiconductor company best known for interface and connectivity ICs. If you have ever
plugged in a cheap USB-serial adapter, you have used a `CH340`.

Two domains, both live (verified 2026-08-24):

| Host | Role |
|---|---|
| `https://www.wch-ic.com/` | International / English-oriented site (S2) |
| `https://www.wch.cn/` | Chinese site; same document tree, sometimes updated first (S5) |

WCH is a *component* vendor; it appears only in [`components/`](../../components/README.md).

---

## 2. Product lines and how they fit together

WCH's catalogue is coherent once you see the organising idea: **they make the glue between a bus and
everything else.**

| Line | What it is | Examples | Relevance |
|---|---|---|---|
| **`CH34x` — USB-to-serial bridges** | USB ↔ UART / I²C / SPI / parallel | `CH340`, `CH341`, `CH343`, `CH9102` | **Ubiquitous.** The default USB-UART on cost-sensitive ESP32 boards |
| **`CH44x` — analog switches / muxes** | Signal routing | `CH440`, `CH445`, `CH446` | Our audio-source mux |
| **`CH32V` — RISC-V MCUs** | 32-bit RISC-V MCUs, some with USB PD | `CH32V003` (famously ~10¢), `CH32V307` | Rapidly growing; the `CH32V003` is a hobbyist phenomenon |
| **`CH32F` — Arm MCUs** | Cortex-M3/M4 | `CH32F103` | STM32-adjacent |
| **`CH37x` / `CH9xx` — USB host/hub/PD** | USB host controllers, hubs, Type-C PD | `CH372`, `CH334`, `CH224` | |
| **`CH9121` / `CH39x` — Ethernet** | Serial-to-Ethernet, MAC/PHY | | |

**The pattern:** WCH takes a bus that is annoying to implement (USB, Ethernet, USB-PD) and sells a
cheap fixed-function part that hides it. That is why they show up on boards next to an MCU that
technically *could* do it natively — the WCH part is cheaper than the engineering time.

---

## 3. Market position

Extremely cheap, extremely available in China, and **increasingly the default rather than the budget
option**. The `CH340` displaced the FTDI `FT232R` and Silicon Labs `CP2102` on hobbyist boards after
FTDI's driver controversy, and WCH now has the volume.

Documentation quality is a pleasant surprise: WCH publishes **full English datasheets** for its
interface parts, including register maps and truth tables. This is markedly better than
[Sitronix](../sitronix/README.md) or [Hynitron](../hynitron/README.md). The catch is driver
distribution rather than documentation — see §7.

---

## 4. Part numbering

```
CH 445 P
│  │   └─ Package / variant suffix (P = a specific package; T, X, N, G also seen)
│  └───── Function series (34x = USB-serial, 44x = analog switch, 32V = RISC-V MCU)
└──────── WCH prefix ("CH" = 沁恒)
```

Conventions:

- **The numeric series is the functional family.** `CH44x` are all switches/muxes; `CH34x` are all
  USB bridges. Once you know the series you know the shape of the part.
- **A trailing letter is package or minor variant.** `CH445P` vs `CH445` differ in package; the
  [CH445P record](../../components/wch/ch445p/README.md) and the datasheet cover both.
- **`CH340X` / `CH340C` / `CH340G` / `CH340N` are meaningfully different**, not just packaging: they
  differ in whether an external crystal is required and in pinout. The
  [USB-UART bridge record](../../components/wch/ch340x/README.md) resolves our board's
  part to a **CH340X** specifically for this reason.
- **Datasheet naming appends `DS1`** — the document, not the part, is `CH445DS1`. See §5.

---

## 5. Documentation: URL patterns

**Read §7 first if you are in a hurry.** The obvious URLs do not work the way they appear to.

| Document class | Pattern | Status |
|---|---|---|
| Any `www.wch-ic.com/...` HTML path | `products/<PART>.html`, `downloads/<PART>DS1_PDF.html`, `downloads/file/<N>.html` | ❌ **Always HTTP 200 + 4,305-byte SPA shell**, existing or not (S3) |
| Any `www.wch.cn/...` HTML path | same | ❌ Same behaviour, ~4,271-byte shell |
| **File metadata (JSON)** | `https://www.wch-ic.com/api/official/website/files/getFilesById?id=<N>` | ✅ **The reliable path** (S4) |
| **File download (PDF)** | `https://www.wch-ic.com/download/file?id=<N>` | ✅ Real bytes; validate `%PDF` (S4) |

Both API endpoints work with a **plain default User-Agent** — no UA substitution needed.

### The metadata record

`getFilesById` returns JSON with `name`, `version`, `uploadTime`, `size`, `content`, and — the field
that matters — **`scope`**, a comma-separated list of *every part number the document covers*.

### The `scope` lesson, which cost us a wrong conclusion once

**WCH publishes one document per _family_, named after the family's first member.** `CH445P` has **no
document of its own.** It is documented inside `CH440DS1.PDF`, whose `scope` reads:

> `CH440G, CH440P, CH440R, CH442E, CH442Q, CH443K, CH443L, CH444G, CH444P, `**`CH445P`**`, CH448F, CH448U`

An earlier research pass recorded the CH445P as *"no datasheet exists"* precisely because it searched
document titles. **Search the `scope` field, not titles.**

### The reliable procedure

```bash
# Enumerate the file table (no UA needed). THROTTLE to <= ~24 concurrent requests:
# above that the API times out silently and you get a partial enumeration.
for N in $(seq 1 800); do
  curl -sS "https://www.wch-ic.com/api/official/website/files/getFilesById?id=$N"
done > wch-files.jsonl

# Find the document covering your part by SCOPE, not by name
grep -i 'CH445P' wch-files.jsonl

# Fetch and validate
curl -sSL "https://www.wch-ic.com/download/file?id=135" -o CH440DS1.PDF
head -c 4 CH440DS1.PDF | od -c | head -1     # expect  %  P  D  F
```

### Encrypted PDFs

Several WCH PDFs carry an **owner password with an empty user password**. `CH440DS1.PDF` and
`CH9102DS1.PDF` use `/Filter /Standard /V 2 /R 3` (RC4-128); `CH340DS1.PDF` and `CH343DS1.PDF` use
AES-256. Raw stream inflation yields nothing. **`poppler-utils`' `pdftotext -layout` handles all four
transparently** — reach for that rather than writing a decryptor.

### Driver bundles are primary sources

WCH's macOS `CH34xVCPDriver` embeds an `IOKitPersonalities` dictionary listing every VID/PID the
vendor claims — better evidence of supported silicon than any web page. The extraction recipe is
recorded in the repository's
[crawler/site-access notes](../../ai-crawler-site-access-table.md#vendor-documentation-portals).

---

## 6. Distribution

| Channel | Availability |
|---|---|
| LCSC | ✅ **Excellent.** The primary channel; JLCPCB stocks `CH340`/`CH44x` for assembly |
| Taobao / AliExpress | ✅ Excellent and cheap |
| Mouser / Digi-Key | ⚠️ Very limited — a few `CH32V` parts have appeared; interface parts largely absent |
| WCH direct | ✅ Sells samples and dev boards, but the site is China-oriented |

Sourcing WCH parts outside China means LCSC in practice. This is a genuine supply-chain
consideration for anyone reproducing a design that uses them.

---

## 7. Gotchas

- **Every HTML path returns HTTP 200.** The SPA shell is 4,305 bytes on `wch-ic.com` and ~4,271 on
  `wch.cn`, for existing *and* nonexistent paths alike. **A naive `curl` of a datasheet URL looks
  like a success and yields HTML.** This is the single most dangerous thing about this vendor, and it
  is why the "verified 200" of a landing page proves nothing. Always check byte size and magic bytes.
- **Documents are per-family, named after the family's first member.** `CH445P` lives in
  `CH440DS1.PDF`. Search `scope`, not titles. See §5.
- **Some datasheet PDFs are password-encrypted.** Use `pdftotext -layout`. See §5.
- **The API times out silently above ~24 concurrent requests**, producing a partial enumeration that
  looks complete. One observed run returned 246 of 800.
- **Two hosts, two ID spaces.** A `file?id=135` on `wch-ic.com` is not `file/135.html` on `wch.cn`.
- **Driver signing, not documentation, is the real pain.** `CH340` needs a driver on older Windows and
  macOS; the macOS situation has historically been poor. Board vendors mirror the drivers themselves
  — e.g. `https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z` — which is a signal about how
  often it bites people. Linux has had `ch341` in-tree for years
  (`drivers/usb/serial/ch341.c`).
- **`CH340` variants are not interchangeable.** See §4.
- **Counterfeit `CH340` exists** — cloning a clone. Symptoms are baud-rate inaccuracy and enumeration
  failures.
- **Some documents are Chinese-only.** The interface-part datasheets have good English versions; MCU
  reference manuals and application notes frequently do not.
- **The English site's phrasing can be ambiguous.** Where the English and Chinese datasheets disagree,
  the Chinese one is the source of truth — it is the original.

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [CH445P](../../components/wch/ch445p/README.md) | Quad 2:1 analog switch — audio-source mux. **Datasheet and truth table resolved** | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |
| [USB-UART bridge `U10` — **CH340X**](../../components/wch/ch340x/README.md) | USB-to-UART bridge. Identity resolved 2026-08-21 | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |

The USB-UART record is filed under `components/generic/` rather than `components/wch/` because it was
created before the part's identity was resolved; the record itself now identifies it as a WCH CH340X.
**This is a known filing inconsistency**, left in place because moving records is out of scope for
this pass and the cross-links resolve correctly either way.

No device in this repository is manufactured by WCH.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | WCH Chinese site | primary | https://www.wch.cn/ | 2026-08-24 | HTTP 200 (but see S3 — the status code is meaningless here) |
| S2 | WCH international site | primary | https://www.wch-ic.com/ | 2026-08-24 | HTTP 200 |
| S3 | **Negative control** — bogus path vs. real path | probe | `https://www.wch-ic.com/downloads/CH445DS1_PDF.html` and `https://www.wch-ic.com/downloads/TOTALLYBOGUS_PDF.html` | 2026-08-24 | **Both return HTTP 200 with exactly 4,305 bytes of identical SPA shell.** The HTML URL scheme carries no information |
| S4 | WCH file API and download endpoints | primary | https://www.wch-ic.com/api/official/website/files/getFilesById?id=79 · https://www.wch-ic.com/download/file?id=135 | 2026-08-21 | The working retrieval method; the `scope` field; that `CH445P` is documented inside `CH440DS1.PDF`. Cited by the [CH445P record](../../components/wch/ch445p/README.md) |
| S5 | Repository crawler/site-access notes, "Vendor documentation portals" | secondary (internal) | [`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md#vendor-documentation-portals) | 2026-08-21 | The SPA-shell fingerprint, the ≤24-concurrency limit, the PDF encryption handlers, the driver-bundle extraction recipe |

> **Evidence boundary.** S1–S3 are **probes performed 2026-08-24**. S3 is a deliberate negative
> control and is the reason this guide contradicts an earlier draft that reported the
> `downloads/<PART>DS1_PDF.html` pattern as working — **it does not; it merely returns 200.** S4
> reflects files actually retrieved during the 2026-08-21 component pass, and the numeric IDs there
> are **historical observations that may not remain valid**. §4's numbering decode is **inference**
> from the parts we hold; WCH publishes no numbering guide we have found. The `CH340` counterfeit
> claim in §7 is **general industry observation, not measured here**.

---

## Related

- [Vendor guide index](../README.md)
- [CH445P](../../components/wch/ch445p/README.md) · [USB-UART bridge (CH340X)](../../components/wch/ch340x/README.md)
- [Espressif vendor guide](../espressif/README.md) — the SoC on the other side of the CH340X
- [Texas Instruments](../texas-instruments/README.md) — the audio chain the CH445P switches
