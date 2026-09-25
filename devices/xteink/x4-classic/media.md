# Xteink X4 Classic — images and media

**No image of this device exists in this repository, and none was found anywhere.**

## What was searched

| Target | Where | Result |
|---|---|---|
| Teardown / PCB | Reddit, 2,136 posts, terms including `xteink teardown`, `xteink x4 classic`, `xteink x4c` | **none** |
| Owner photographs | same corpus | **none** |
| Vendor product imagery | `xteink.com` `/products.json` and the `x4-classic` collection | **The device is not in the catalogue**, so it has no images |
| GitHub | ~200-repository census | **none** |
| FCC internal photos | not searched | no FCC ID known — and Xteink devices generally carry **no external regulatory marking** |

## The only visual evidence that has ever been claimed

A vendor **video**, in June 2026, in which the community believed it saw this
device:

> "Could there actually be three devices shown in the video? First the S4, then
> the X4 Pro and finally 2 devices placed in the dock at the end. At first I
> assumed the last one was just the standard X4, but after rewatching it a few
> times I'm not so sure anymore. The front buttons look identical to the X4, but I
> keep noticing what looks like a button on the left side."
> — [r/XTEINK `1ud0d9c`](https://old.reddit.com/r/XTEINK/comments/1ud0d9c/), 2026-06-22, **300 points** · *interpretation of a video, not a photograph*

That reading was **partly right** (buttons, no touchscreen; and the side button is
consistent with GPIO0/GPIO7 being side keys) and **partly wrong** (it reported a
frontlight; the firmware says there is none).

The video itself was **not retrieved** — the thread does not carry a stable link
in the retrieved JSON. Recorded as an open acquisition: it is currently the only
known imagery of this device anywhere.

## What one photograph would settle

| Question | Currently |
|---|---|
| **Charging connector** — USB-C or pogo? | **Unknown**, and it is a first-order buyer question |
| Physical size and mass | Unknown |
| Whether the back is glass or metal | Unknown |
| External regulatory marking | Unknown (family precedent: none) |
| Button arrangement as built | Inferred from the firmware map only |

## Related

The [X3 teardowns](../x3/media.md) are the only Xteink internal photography that
exists, and they are of a **completely different board** (ESP32-C3, different
panel, different peripherals). They establish the vendor's construction style —
glass back, glued cell, glued pogo magnets — and nothing about this device.

---

## Round 2 — 2026-09-11

**No line above was altered.** Full provenance for everything below is in
[`media/manifest.json`](media/manifest.json).

### One photograph is now retained

`artifacts/certification/2BTR9-X4C-label.pdf` — the FCC *ID Label and Location
Info* exhibit, 189,803 bytes, SHA-256
`605b978782399a0fdcf267848b5459981fd8069ec6e976e0240aff0bde72ba9c`. It embeds a
single 1039×779 photograph at 220 ppi.

- **Caption.** The X4 Classic's rear face in Mist White, photographed on a blue
  mat beside a millimetre rule and its magnetic charging adapter. Visible: the
  `XTEINK` wordmark, the **oval outline of the internal magnet ring** at the
  centre, the **four gold pogo contacts** on the bottom edge, two button
  protrusions on the left edge and one on the right.
- **Alt text.** *"White rectangular e-reader seen from the back, with a small
  magnetic charging adapter beside it and a ruler for scale."*
- **Modifications.** None. Retained as the original PDF; no crop, no rotation,
  no annotation, no watermark removal.
- **Rights.** Applicant's photograph, published by the US FCC in a public
  equipment-authorization record. Redistribution status **`unknown`**;
  disposition `repository`, **unstaged**.

That photograph is the **first image of an X4 Classic anywhere in this
repository**. It is also a *product* photograph; it shows nothing internal.

### The images that would actually settle the open questions

| Image class | Status |
|---|---|
| **FCC Internal Photos** (4.5 MB) | **Exists. Embargoed to 2027-01-16.** |
| FCC External Photos (825.3 KB) | Exists. Embargoed to 2027-01-16 |
| FCC Schematics / Block Diagram | Exist. **Permanently confidential** |
| Community PCB photographs | **None exist.** Asked for publicly 2026-09-10; the only reply confirms none had been posted |
| Vendor product photography | 14 images on the Shopify CDN. `reference-only` — vendor marketing, no licence offered |
| Owner photographs | Several launch-week Reddit galleries, all exterior. `reference-only` — no licence offered by any poster |

### Use the sibling's photographs for form-factor questions

The **X4 Light**'s FCC external photographs are **not** embargoed and are
retained at
[`../x4-light/artifacts/certification/2BTR9-X4L-external-photos.pdf`](../x4-light/artifacts/certification/2BTR9-X4L-external-photos.pdf)
(3,485,136 B, SHA-256 `c6457651f19b4cac…`). They show the same enclosure
generation — same proportions, same magnet outline, same four-pin pogo pad — in
both black and white, against a millimetre rule.

**They are a different device.** Use them for the shape of this product family.
**Do not cite them as evidence about the X4 Classic's dimensions or internals.**

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 13:* | FCC internal photos | not searched | no FCC ID known — and Xteink devices generally carry **no external regulatory marking** |
>

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment authorisations**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

The original finding confused **"no mark visible in a product photograph"** with **"no grant exists"**. Those are different claims, and only the first was tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is ordinary for a device with a screen. **That is a likely explanation and it was not verified.**

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

Full record, with controls: [`certification-and-compliance.md`](certification-and-compliance.md).

Listed in [`research/passes/index-merge/corrections-requiring-review.md`](../../../research/passes/index-merge/corrections-requiring-review.md).
