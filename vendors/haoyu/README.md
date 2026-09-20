# Haoyu Microelectronics (HYM8563 RTC) — Documentation Sourcing Guide

> **⚠️ Name collision — read this first.** "Haoyu" in this repository refers to the **semiconductor
> maker of the `HYM8563` real-time clock**, filed at
> [`components/haoyu/hym8563/`](../../components/haoyu/hym8563/artifacts/hym8563-datasheet.pdf). It is
> **not** *HAOYU Electronics* (`hotmcu.com`), the Shenzhen board retailer, which is an unrelated
> company with a confusingly similar name. See §8 for the disambiguation. If you are looking for the
> retailer, go to the [marketplace comparison](../../guides/markets/vendor-comparison.md).

> **Status: no README record yet, but we hold the datasheet.** There is no
> `components/haoyu/hym8563/README.md`; the retrieved PDF sits in that directory's `artifacts/`.

> **TL;DR** — The vendor's own domain, **read out of the datasheet's embedded text**, is
> `www.haoyu-ic.com` (S2) — and it **returns HTTP 404** as of 2026-08-24 (S3). The contact numbers in
> the same PDF use the **`027` area code, i.e. Wuhan** (S2). Treat this vendor as effectively
> unreachable and rely on the local copy.

---

## 1. Who they are

A small Chinese semiconductor company, evidenced almost entirely by its own datasheet. What we can
state from the document itself **[DOC]**:

- The document is a genuine PDF (`%PDF-1.4`, 467,968 bytes, SHA-256 prefix `a3dac953`).
- Its embedded text contains the string **`www.haoyu-ic.c`** — the company domain.
- Its contact block uses **`027-87…`** telephone numbers. `027` is the area code for **Wuhan**.

**[INF]** Everything beyond that — the company's full legal name, size, founding date and current
status — is **not established**. Do not assert them.

---

## 2. Product line — what we actually know

| Part | What it is | Evidence |
|---|---|---|
| **`HYM8563`** | Real-time clock / calendar, I²C, with alarm, timer, clock output and low-voltage detection | **[DOC]** the datasheet we hold |

That is the entire evidenced catalogue. **[INF]** The `HY` prefix presumably spans a wider range, but
we have no catalogue and the vendor site is down.

### The important structural fact

**`HYM8563` is a work-alike of the NXP `PCF8563`** — same I²C address, substantially the same
register map, same function set. That is why it exists: it is a cheaper second source for one of the
most widely designed-in RTCs in the industry.

**Practical consequence:** [NXP's `PCF8563` documentation](../nxp/README.md) — which we **also hold**,
at Rev. 11 — is a usable reference for this part, and is in better English. **Read them together, and
verify rather than assume**: work-alikes typically diverge in exactly the places that matter
(oscillator trimming, clock-out divider options, low-voltage detector thresholds).

This is the same pattern as the [`HMC5883L`/`QMC5883L` case](../qst/README.md#3-market-position--and-the-hmc5883l-story):
**a near-clone part number is a compatibility claim about the pinout and the common registers, not a
guarantee about the corners.**

---

## 3. Market position

**[INF], and weakly held.** A low-cost domestic Chinese alternative to the `PCF8563`, sold into the
same cost-driven consumer designs as [XLSEMI](../xlsemi/README.md) and
[Chipsemi](../chipsemi/README.md) parts. We have no pricing, no distribution and no volume evidence.

---

## 4. Part numbering

```
HY M 8563
│  │ └─ Deliberately echoes the PCF8563 it substitutes for
│  └─── M = ? (mixed-signal / module — unknown)
└────── HY = Haoyu
```

**[INF]** entirely — no numbering key, no catalogue. The only firm element is the **`8563`**, which is
plainly borrowed from the NXP part.

---

## 5. Documentation

| Rank | Source | Status |
|---|---|---|
| 1 | **Our local copy** | ✅ [`components/haoyu/hym8563/artifacts/hym8563-datasheet.pdf`](../../components/haoyu/hym8563/artifacts/hym8563-datasheet.pdf) — **use this** |
| 2 | **NXP `PCF8563` Rev. 11** | ✅ Also held locally, at [`components/nxp/pcf8563/artifacts/`](../../components/nxp/pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf). Better written; verify differences |
| 3 | Linux kernel | `drivers/rtc/rtc-pcf8563.c` — in-tree, and **has historically carried explicit HYM8563 support**. **[INF]**, worth checking |
| 4 | LCSC mirror | The [MEMSensing pattern](../memsensing/README.md#5-documentation-where-it-actually-comes-from) |
| 5 | `www.haoyu-ic.com` | ❌ **HTTP 404** (S3) |

**The lesson this vendor teaches:** the single most reliable Haoyu document in existence is the one
already sitting in this repository. **That is precisely why the mirroring discipline exists** — see
[vendor-comparison.md §3](../../guides/markets/vendor-comparison.md#3-documentation-durability--the-axis-nobody-advertises).

### Extracting text from this PDF

It resisted naive extraction (`poppler-utils` was unavailable in the 2026-08-24 environment). The
domain and area code in §1 were recovered by **inflating the PDF's `stream` objects with `zlib` and
scanning for literal-string operators** — a useful fallback when `pdftotext` is not to hand.

---

## 6. Distribution

**[unverified]** — not probed. Expect LCSC and Taobao; do not expect Mouser or Digi-Key.

---

## 7. Gotchas

- **The vendor site is gone (404).** Rely on the local copy.
- **The name collides with HAOYU Electronics**, an unrelated Shenzhen retailer. See §8.
- **`HYM8563` is not guaranteed identical to `PCF8563`.** See §2.
- **RTC accuracy is a crystal problem, not a chip problem.** A 32.768 kHz crystal with the wrong load
  capacitance will lose or gain minutes per week regardless of which vendor's die you chose. Match
  C_L to the datasheet before blaming the RTC.
- **Backup-battery leakage paths** are the other classic RTC failure. Check the V_BAT pin's specified
  reverse current.

---

## 8. Parts and devices we document

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **HYM8563** (I²C RTC/calendar) | [`components/haoyu/hym8563/artifacts/hym8563-datasheet.pdf`](../../components/haoyu/hym8563/artifacts/hym8563-datasheet.pdf) | 467,968 | ❌ **missing** |

**Provenance:** the PDF shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive, and
was relocated to a reusable component directory. **The HYM8563 is not fitted on the knob board** —
it is one of many parts SensorLib supports. See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

Writing the `components/haoyu/hym8563/README.md` record is **outstanding work**.

### Disambiguation: the other HAOYU

| | This vendor | The other one |
|---|---|---|
| Name | Haoyu Microelectronics (**[INF]** — exact legal name unestablished) | **HAOYU Electronics Ltd.** |
| What | Semiconductor maker — `HYM8563` RTC | Online **retailer** of dev boards and modules |
| Where | Wuhan (`027` area code, **[DOC]**) | Shenzhen |
| Site | `www.haoyu-ic.com` — **404** | `www.hotmcu.com` — **200**, *"HAOYU Electronics : Make Engineers Job Easier"* (S4) |
| Covered in | **this guide** | [markets/vendor-comparison.md](../../guides/markets/vendor-comparison.md) |

There is **no evidence of any relationship between them**, and none should be inferred. They share a
transliterated syllable, which is common.

---

## 9. Sources

| ID | Title | Class | URL / path | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | HYM8563 datasheet (local copy) | primary (redistributed) | [`components/haoyu/hym8563/artifacts/hym8563-datasheet.pdf`](../../components/haoyu/hym8563/artifacts/hym8563-datasheet.pdf) | 2026-08-23 | The part's specifications; `%PDF-1.4`, 467,968 bytes |
| S2 | Embedded text of S1 | primary | — (extracted 2026-08-24 by zlib stream inflation) | 2026-08-24 | The vendor domain string `www.haoyu-ic.c` and `027-87…` (Wuhan) contact numbers |
| S3 | **Negative probe** — vendor domain | probe | http://www.haoyu-ic.com/ | 2026-08-24 | **HTTP 404** (`<TITLE>Not Found</TITLE>`). HTTPS does not connect |
| S4 | HAOYU Electronics storefront (**the other company**) | probe | https://www.hotmcu.com/ | 2026-08-24 | HTTP 200; used only for the §8 disambiguation |
| S5 | Vendored-deps datasheet disposition | secondary (internal) | [vendored-deps/README.md](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition) | 2026-08-23 | Provenance of S1 and the not-fitted-on-this-board caveat |

> **Evidence boundary.** S2 and S3 are the strongest claims here and were made **2026-08-24**. **The
> datasheet's technical content has not been read** — extraction was limited to locating the vendor
> domain and phone prefix, because `poppler-utils` was unavailable. Therefore §2's description of the
> `HYM8563`'s features, and the entire `PCF8563` work-alike claim, are **[INF] / recalled and not
> verified against S1.** §1's company identity beyond the domain and area code, §3, §4 and §6 are
> **unverified**. An earlier draft of this guide described the wrong company entirely; that error was
> caught by checking `components/haoyu/`, and is recorded here as a caution.

---

## Related

- [Vendor guide index](../README.md)
- [NXP](../nxp/README.md) — the `PCF8563` this part shadows; **we hold that datasheet too**
- [QST](../qst/README.md) — the same near-clone-part-number pattern
- [Marketplace comparison](../../guides/markets/vendor-comparison.md) — for **HAOYU Electronics**, the unrelated retailer
