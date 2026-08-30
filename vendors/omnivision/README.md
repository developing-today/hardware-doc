# OmniVision — Documentation Sourcing Guide

Reusable knowledge for obtaining primary documentation for **any** OmniVision image sensor.

> **TL;DR** — OmniVision publishes **nothing** to the public. There is no customer datasheet portal, no guessable URL pattern, no login you can register for. Every OmniVision datasheet in circulation reached the public through a **camera-module vendor** (Arducam, UCTRONICS, SparkFun, Waveshare, Seeed) or a distributor mirror. Plan to hunt across mirrors, expect version ambiguity, and expect explicit redistribution restrictions on the documents you find.

Established while researching the [OV5640](../../components/omnivision/ov5640/README.md), [OV3660](../../components/omnivision/ov3660/README.md) and [OV2640](../../components/omnivision/ov2640/README.md) for the Seeed XIAO ESP32S3 Sense. Last verified **2026-08-30**.

---

## 1. Who they are

OmniVision Technologies, Inc. (Santa Clara, California), founded 1995, a pioneer of CMOS image sensors. Acquired in 2016 by a Chinese consortium and since 2019 operating under **Will Semiconductor** (韦尔股份). The company sells almost exclusively to OEMs and module houses in volume; it has no hobbyist or maker channel and no distributor-style documentation posture.

This matters directly: TI's model — complete public register maps at stable URLs — is the *opposite* of OmniVision's. Compare [`vendors/texas-instruments/README.md`](../texas-instruments/README.md).

OmniVision is a **component** vendor only; it never appears under `devices/`.

---

## 2. Where documents actually live

`www.ovt.com` (and the older `www.omnivision.com`) carries **product briefs only** — one- or two-page marketing summaries with a "Contact us" button where the datasheet link would be. Register maps are behind an NDA-gated sales relationship.

In practice, documents come from these sources, in rough order of reliability:

| Source class | Examples | Notes |
|---|---|---|
| **Camera-module vendors** | `arducam.com/downloads/modules/<PART>/`, `uctronics.com/download/cam_module/` | **The most productive.** They must ship documentation with their modules. Arducam in particular hosts datasheets *and* application notes |
| **Maker distributors** | `cdn.sparkfun.com/datasheets/Sensors/LightImaging/`, `files.waveshare.com/upload/`, `files.seeedstudio.com/wiki/` | Reliable when the part matches something they sell |
| **SBC vendors** | `dl.radxa.com/.../datasheet/`, Rockchip/Allwinner BSP trees | Useful for MIPI parts |
| **Linux kernel** | `drivers/media/i2c/ov*.c` | Not a datasheet, but often the best *behavioural* documentation that exists |
| **`esp32-camera`** | `espressif/esp32-camera` `sensors/` | Authoritative for the ESP32 ecosystem; contains the init tables |
| **Datasheet aggregators** | alldatasheet, datasheetspdf | Frequently stale, frequently HTML-behind-a-PDF-URL, often DNS-blocked. Last resort |

### 2.1 Verified working URLs (2026-08-30)

| Part | URL | Result |
|---|---|---|
| OV5640 datasheet | `https://cdn.sparkfun.com/datasheets/Sensors/LightImaging/OV5640_datasheet.pdf` | ✅ v2.03, 179 pp, 1 749 719 B |
| OV5640 AF app notes | `https://www.arducam.com/downloads/modules/OV5640/OV5640_Software_app_note_parallel.pdf` | ✅ rev 2.13, 63 pp, 1 909 564 B |
| OV2640 datasheet | `https://www.uctronics.com/download/cam_module/OV2640DS.pdf` | ✅ v1.6, 43 pp, 676 989 B |

### 2.2 Verified failures (2026-08-30) — do not retry these first

| URL | Result |
|---|---|
| `https://cdn.sparkfun.com/assets/learn_tutorials/8/3/4/OV5640_Software_Application_Notes.pdf` | HTTP 404, HTML |
| `https://cdn.sparkfun.com/datasheets/Dev/Arduino/Shields/OV5640_Software_Application_Notes.pdf` | HTTP 404, HTML |
| `https://www.arducam.com/downloads/modules/OV3660/OV3660_datasheet.pdf` | HTTP 404 (260 KB HTML error page — **would have been saved as a valid-looking PDF without magic-byte validation**) |
| `https://www.arducam.com/wp-content/uploads/2018/01/OV3660_datasheet.pdf` | HTTP 404 |
| `https://www.arducam.com/wp-content/uploads/2019/10/OV3660_datasheet.pdf` | HTTP 404 |
| `https://files.waveshare.com/upload/9/9a/OV3660_datasheet.pdf` | HTTP 404 |
| `https://dl.espressif.com/dl/schematics/OV3660_datasheet.pdf` | HTTP 404 |
| `cdn.datasheetspdf.com` (any path) | **DNS does not resolve** from this network |

> ⚠ **The Arducam 404 page is 260 KB of HTML.** Saved blindly to a `.pdf` filename it looks entirely plausible by size. Always validate `%PDF` magic bytes.

---

## 3. Traps specific to OmniVision material

**Versions are rarely stated in filenames, and mirrors serve different revisions.** The OV2640 file served from a URL named `OV2640DS.pdf` turns out to be *"Version 1.6, February 28, 2006"*, and the very same bytes are served from a second UCTRONICS URL named `OV2640_DS.pdf`. Open the first page and read the revision before naming your local copy — a filename asserting "v2.2" that actually contains v1.6 is worse than no version at all.

**Datasheet maturity varies wildly within one family.** The OV5640 datasheet is a released *PRODUCT SPECIFICATION*; the OV3660's is marked **"PRELIMINARY SPECIFICATION"** with figures still "TBD". Both are the newest publicly obtainable revisions. State the maturity in the component record; do not present preliminary numbers with the same confidence as released ones.

**Application notes carry the interesting material.** The OV5640 *datasheet* documents the register block layout; the *Auto Focus Application Notes* documents the entire AF command protocol (`0x3022`/`0x3023`/`0x3029`) without which autofocus is unimplementable. Always search for `<PART>_Software_Application_Notes`, `<PART>_app_note`, `<PART> Camera Module Application Notes` in addition to the datasheet.

**The document states a redistribution limitation.** The OV3660 and OV5640 datasheets state: *"Individuals and/or organizations are not allowed to re-distribute said information."* The OV5640 AF application note is stamped **"Company Confidential / OmniVision Confidential for BYD Only"** on every page. These documents circulate freely via module vendors, but that is not a licence. Record them as redistribution status **`restricted`/`unknown`** and flag them for user review rather than staging them casually. Extracting *facts* (register addresses, values, timings) into an authored record is a different act from redistributing the document, and is what this repository does.

**Typos propagate.** OmniVision's own OV5640 AF application note refers to *"the built-in micro-controller of OV5647"* — a different sensor. Downstream, Seeed's OV5640 autofocus library unpacks to a directory named `OV5647_AF-main`. Do not conclude you fetched the wrong part; check the file contents.

**Part numbers collide on the bus.** OV5640 and OV3660 both answer SCCB at **7-bit `0x3C`**. Identification requires reading the 16-bit chip ID at register `0x300A`/`0x300B`. Any document or driver that identifies an OmniVision sensor by bus address alone is unreliable.

---

## 4. Document-class checklist

For any OmniVision part, look for:

- [ ] **Datasheet** — register block map, electricals, timing. Note the revision *and* whether it is preliminary
- [ ] **Software application notes** — the register *sequences*; often where the usable protocol lives
- [ ] **Camera module specification** — a separate document from the module house covering lens, VCM, flex pinout, mechanical
- [ ] **Init/setting tables** — realistically obtained from `esp32-camera` or the Linux kernel, not from OmniVision
- [ ] **AF firmware blob** (AF-capable parts only) — from a module vendor's library
- [ ] Linux `drivers/media/i2c/ov<part>.c` — behavioural reference

---

## 5. Working command pattern

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

fetch_ov() {  # $1 = output path, $2 = url
  tmp=$(mktemp)
  code=$(curl -sSL --max-time 90 -A "$UA" -o "$tmp" -w '%{http_code}' "$2")
  if [ "$code" = 200 ] && [ "$(head -c4 "$tmp")" = '%PDF' ]; then
    mv "$tmp" "$1"; echo "OK $1 ($(stat -c%s "$1") bytes)"
  else
    echo "REJECT $2 (http=$code, magic=$(head -c4 "$tmp" | tr -d '\0'))"; rm -f "$tmp"
  fi
}
```

The magic-byte check is not optional here — see §2.2.

A plain User-Agent works for SparkFun and UCTRONICS. Arducam served the AF application note to a Chrome UA; it was not tested with a bare `curl` UA, so whether the UA mattered is unknown.

---

## 6. Rights and licensing observations

Recurring across OmniVision material:

- Explicit no-redistribution clauses on datasheets
- "Company Confidential" / named-customer-only stamps on application notes
- No licence file, no permissive grant, no public terms of use
- Module-vendor mirrors do not add a licence; hosting is not permission

Note OmniVision PDFs as `redistribution: restricted` or `unknown` and keep them in the repository. The documents are scarce and several of their source URLs already 404, so having a copy is the point. Facts extracted into authored records are fine; wholesale reproduction is not.

---

## Products documented in this repository

| Part | Record | Datasheet obtained? |
|---|---|---|
| **OV5640** | [`components/omnivision/ov5640/`](../../components/omnivision/ov5640/README.md) | ✅ v2.03 + AF application notes rev 2.13 |
| **OV3660** | [`components/omnivision/ov3660/`](../../components/omnivision/ov3660/README.md) | ✅ (preliminary) — held in the XIAO device tree; five independent re-fetch URLs all 404 |
| **OV2640** | [`components/omnivision/ov2640/`](../../components/omnivision/ov2640/README.md) | ✅ v1.6, 2006-02-28 |

## Related pages

- [`vendors/texas-instruments/README.md`](../texas-instruments/README.md) — the contrasting case: fully public, guessable URLs
- [`vendors/sgmicro/README.md`](../sgmicro/README.md) — another vendor requiring a non-obvious extraction method
- [`component-download-failures.txt`](../../component-download-failures.txt) — the running failure ledger
- [`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md) — user-agent and site-access findings
