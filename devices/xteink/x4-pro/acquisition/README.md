# Xteink X4 Pro — acquisition

**No artifact was acquired for this device.** That is not for lack of trying — see
the table below. The X4 Pro is the family's flagship and has the **thinnest
artifact position** of any model with a public existence.

## Clean-clone commands

None. Nothing is held.

The one thing worth cloning is the SDK that documents the board, which is a
*source* dependency rather than a device artifact:

```bash
git clone https://github.com/Free-Ink/freeink-sdk
git -C freeink-sdk checkout 24003795381a6c23630a26472ae3b06550333e71
```

## Wanted artifacts

| Artifact | Reacquisition | Notes |
|---|---|---|
| **An X4 Pro stock firmware image** | **`blocked`** | **No public X4 Pro image exists anywhere.** The X3 has four published stock images and the X4 has a community dump; the flagship has neither. Only route: dump a USB-unlocked unit |
| `xteink_app_update_x4pro_7.4.4_20260827_133901.xota` | **`blocked`** | Named in the FreeInk SDK docs; **no download URL found**. The `.xota` container appears encrypted — the SDK refers to *"the decrypted"* app and the mechanism is undocumented |
| Vendor OTA feed response | **`manual`** | `http://gotaserver.xteink.com/api/check-update` — endpoint recovered from the **X4** dump. **Not queried.** Request format unknown |
| Any teardown or PCB photograph | **`lost`** | None exists. Would close **seven** separate unknowns at once — see [`gaps-and-conflicts.md`](../gaps-and-conflicts.md) |
| Vendor product imagery | **`automatic`** | Listing is **live**; URLs are in `vendors/xteink/artifacts/store-snapshots/2026-09-04/products-p1.json` under `products[].images[].src`. **Capture before delisting** — the X4's imagery was lost exactly that way |
| FCC / CE / SRRC filing | **`blocked`** | No ID known, and the community reports Xteink devices **carry no external regulatory marking** — regulatory text is placed in software instead |

## Why nothing was downloaded

Not a scope decision. The X4 Pro simply has **no public binary or document** to
fetch:

- **No vendor SDK, datasheet, manual, schematic or BSP.** Xteink publishes none.
- **No community firmware dump.** Unlike the X3 and X4.
- **No teardown.** Unlike the X3.
- **No regulatory filing.** Unlike almost any consumer radio device.

Everything in this device record derives from **one repository at one commit** —
`Free-Ink/freeink-sdk` @ `24003795381a6c23630a26472ae3b06550333e71` — plus the
vendor's Shopify API and Reddit.

## Chip datasheets belong to components, not here

Per the filing rule, datasheets for the SSD1677, UC8179, UC8279, GT911, CW2017,
BM8563 and ESP32-S3 are **component** artifacts. Their acquisition status is
recorded in each component record; several are `not-attempted` and are flagged
there as open.

## Verification

```bash
python3 tools/audit_archive.py     # confirms nothing archived here is unreferenced
```

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 28:* | FCC / CE / SRRC filing | **`blocked`** | No ID known, and the community reports Xteink devices **carry no external regulatory marking** — regulatory text is placed in software instead |
>
> *line 38:* - **No regulatory filing.** Unlike almost any consumer radio device.
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

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../../guides/research/finding-certification-records.md).

Full record, with controls: [`certification-and-compliance.md`](../certification-and-compliance.md).

Listed in [`research/passes/index-merge/corrections-requiring-review.md`](../../../../research/passes/index-merge/corrections-requiring-review.md).
