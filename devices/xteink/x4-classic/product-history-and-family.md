# Product history and family — Xteink X4 Classic (X4C / "X4 V2")

Snapshot **2026-09-11**. Every dated row below cites a source that carries the
date itself: a Shopify `published_at`/`created_at`, an FCC final-action date, a
Git commit timestamp, or a Reddit post timestamp.

## The name

**"X4 Classic" and "X4 V2" are the same product.** This is not an inference:

| Evidence | Date | Form |
|---|---|---|
| Vendor Reddit post, verbatim: *"**X4 Classic (X4 V2) is coming soon**"* | 2026-09-03 | primary, vendor |
| Store product title: `XTEINK X4 Classic (X4 V2) Pocket eReader` | 2026-09-06 | primary, vendor API |
| Four accessory titles, all `XTEINK X4 Classic (X4 V2) …` | 2026-09-06 | primary, vendor API |
| Product-page FAQ prose: *"The **X4 V2** features a built-in magnetic ring…"* | 2026-09-11 | primary, vendor |
| Third-party firmware header comment: *"Xteink X4 Classic (also marketed "X4 v2")"* | 2026-09-11 | independent ([`clackups/draftling`](https://github.com/clackups/draftling/blob/92ba7e514f66bbe42a7fea6d38eff45eed82617b/firmware/main/boards/xteink_x4_classic.h)) |
| FCC device description: `XTEINK X4 Classic`, product code `X4C` | 2026-07-20 | primary, regulatory |

**The 2026-09-04 record's open item — a "vendor-confirmed X4 v2 for September
2026, spec unknown" — is closed. It was this device.** No separate X4 v2 exists,
and none is in certification under that name.

### Naming forms in circulation

| Form | Used by |
|---|---|
| **X4 Classic** | Vendor titles, FCC device description, FreeInk, CrossPoint |
| **X4 V2** / **X4 v2** | Vendor's own parenthetical and FAQ prose; the community from April 2026 onward |
| **X4C** | FCC **product code**, FreeInk doc filename `xteink-x4c-support.md`, community shorthand |
| **"V1"** for the original X4 | Owner usage, e.g. the vendor-hosted review *"different from the V1"* |
| `ESP32S3_X4_CLA` / `ESP32S3_X4R2_CLA` | Board tag and revision string in the stock firmware |

## Dated timeline

| Date | Event | Source class |
|---|---|---|
| **2025-12-21** | Grantee `2BTR9` registered with the FCC — *Shenzhen Xiaohu Xingtong Technology Co., Ltd.*, Longhua District, Shenzhen | regulatory |
| 2025-12-26 | FCC ID `2BTR9-XTEINKX3` granted (**X3**) | regulatory |
| 2026-01-05 | FCC ID `2BTR9-XTEINKX4` granted (**X4** — the "V1") | regulatory |
| **2026-04-23** | First public "X4 V2" speculation: [r/xteinkereader `1stt8ak`](https://old.reddit.com/r/xteinkereader/comments/1stt8ak/) *"Looks like they're making a X4 V2 Pro with backlight!"*, 47 pts | community |
| 2026-04-24 → 2026-08 | ~25 further "X4 v2" threads; the community conflates **X4 V2** (this device) and **X4 V2 Pro** (which became the X4 Pro) | community |
| **2026-06-16** | FCC ID `2BTR9-X4PRO` granted (**X4 Pro**) | regulatory |
| **2026-06-22** | [r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/) 300 pts — a buttons-only S3 device spotted in a vendor Rednote video. **Right about buttons and no touch; wrong about a frontlight** | community |
| 2026-07-20 | **FCC ID `2BTR9-X4C` filed and granted.** Short-term confidentiality on photos/manual to 2027-01-16; **permanent** on schematics and block diagram | regulatory |
| **2026-07-23** | [r/XTEINK `1v4824q`](https://old.reddit.com/r/XTEINK/comments/1v4824q/) 44 pts — a community member finds the filing and publishes the FCC ID. Predicts: refresh of the X4, buttons only, no touch, **pogo retained**. All four correct | community |
| 2026-07-21 | X4 Pro listed on `xteink.com` at **US$99** (`published_at`) | vendor API |
| **2026-08-03 05:06:01 −0700** | X4 Classic product record **created** in Shopify (unpublished draft) | vendor API |
| **2026-08-13** | **FCC ID `2BTR9-X4L` granted — "XTEINK X4 Light"**, a *sixth* device, still unannounced at this snapshot → [`../x4-light/`](../x4-light/README.md) | regulatory |
| 2026-08-29 | [r/XTEINK `1w1tcx9`](https://old.reddit.com/r/XTEINK/comments/1w1tcx9/) 80 pts, *"Well well look what we have here"* | community |
| 2026-08-31 19:22 → 23:43 −0700 | Four X4C accessory records created in Shopify | vendor API |
| 2026-08-31 | Shopify collection `x4-classic` **published** (still deviceless) | vendor API |
| **2026-09-01** | FreeInk SDK commit `2400379` — the `XTEINK_X4_CLASSIC` profile as the 2026-09-04 sweep read it | source |
| **2026-09-03** | **Vendor announcement**, r/xteinkereader `1w63yyl`, 806 pts | vendor |
| 2026-09-04 | *Prior research snapshot.* `x4-classic` collection contained **4 generic accessories and no device** | vendor API |
| 2026-09-04 23:22 −0700 | `XTEINK Base Stand & Charging Adapter for X3, x4 Classic and X4 Pro` published, **US$19.99** | vendor API |
| 2026-09-05 00:17 −0700 | Reader **+ base bundle** variants created, US$95.00 | vendor API |
| **2026-09-05** | Review embargo lifts — 13 posts in one day, incl. two detailed pre-release reviews | community |
| **2026-09-06 19:57:20 −0700** | **X4 Classic published — US$79.00, `X4Classic-gray` / `X4Classic-black`** | vendor API |
| 2026-09-06 20:44 −0700 | Four X4C accessories published | vendor API |
| 2026-09-08 | Founder letter on pogo vs USB-C, 616 pts / **730 comments** | vendor |
| **2026-09-09** | FreeInk commit `39606d5a` drops every Xteink `displaySpiHz` from 20 MHz to **10 MHz** | source |
| 2026-09-10 | First public request for X4C PCB photographs; **nobody has opened one** | community |
| 2026-09-11 | X4 accessories **withdrawn** from the catalogue; `x4-series` collection reduced to two generic items | vendor API |
| **2027-01-16** | FCC internal photos, external photos, user manual and test-setup photos become public | scheduled |

## Where it sits in the family

The vendor's own device-only collection (`machine`) on 2026-09-11 contains
**exactly three products**:

| | X3 | **X4 Classic** | X4 Pro |
|---|---|---|---|
| Price | $69 | **$79** | $99 |
| Published | 2025-12-11 | **2026-09-06** | 2026-07-21 |
| SoC | ESP32-C3 | **ESP32-S3** | ESP32-S3 |
| Panel | 3.7″ 792×528 | **4.26″ 800×480** | 4.26″ 800×480 |
| Touch | ✗ | **✗** | GT911 |
| Frontlight | ✗ | **✗** | dual warm/cool |
| Port | pogo | **pogo** | pogo |

**The X4 is not in it.** The X4 Classic did not join the family — it **replaced**
the X4, and the replacement is complete at the catalogue level: the X4's product
record is gone, all four of its dedicated accessories are gone, and the
`x4-series` collection holds only two generic items that fit anything.

### What "Classic" means here, and what it does not

It is **not** a cheaper or cut-down variant. It is the **successor to the
entry-level model**, priced US$10 above the model it replaces and US$20 below the
Pro. Its ancestry is split:

- **From the X4 Pro** it takes the entire board: ESP32-S3, 16 MB flash, 8 MB
  PSRAM, the 4.26″ glass, the three-way panel-controller stack, native SDMMC, the
  BM8563 RTC, the CW2017 gauge, the pogo charging.
- **From the C3 X4** it takes the four bottom keys and the buttons-only reading
  model.
- **From neither** it takes a QMI8658 IMU (which the X3 has and the Pro does not)
  and a 920 mAh cell.

The community's own summary, offered as criticism and accurate as description:
**u/Aelydam, *"disadvantages of the X4 + disadvantages of the Pro = Classic"***
([`1w7wjw2`](https://old.reddit.com/r/XTEINK/comments/1w7wjw2/), 35 pts) — it
keeps the X4's missing frontlight and the Pro's missing USB-C.

## The one thing everybody asked for and did not get

A **buttons-only reader with a frontlight** was the single most-requested
configuration across the whole sample: four of the five top replies to the
vendor's own announcement, and a recurring thread from April through September.
The X4 Classic does not have one.

**It is already certified.** `2BTR9-X4L`, *"XTEINK X4 Light"*, granted
2026-08-13 — six weeks before the X4 Classic shipped, and three weeks before the
announcement that drew those replies. See [`../x4-light/`](../x4-light/README.md).
**Whether "Light" means frontlight or lightweight is not established by the
filing**, and this record does not claim it does.
