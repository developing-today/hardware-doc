# NXP Semiconductors — Documentation Sourcing Guide

> **Status: no records yet, but we hold two NXP RTC datasheets (§8).** There is no NXP component
> record and no NXP device here.
> This guide exists because NXP is a near-certain future encounter (NFC, USB-PD, I²C peripherals,
> i.MX application processors, and the LPC/Kinetis MCUs that ESP32 designs are frequently compared
> against) and because its access behaviour is **actively counter-intuitive** and worth recording
> before someone loses an hour to it.

> **TL;DR — the finding that matters.** `nxp.com` **blocks browser User-Agents and allows the default
> `curl` User-Agent.** This is the inverse of the usual pattern and the inverse of this repository's
> standing [retrieval fallback policy](../../AGENTS.md). With a Chrome UA, `https://www.nxp.com/`
> returns **HTTP 404**; with `curl/8.5.0` it returns **HTTP 200** (S1, S2, verified 2026-08-24).
> Datasheets at `https://www.nxp.com/docs/en/data-sheet/<PART>.pdf` behave identically (S3).

---

## 1. Who they are

NXP Semiconductors N.V. (Eindhoven, Netherlands; NASDAQ: NXPI) is the former Philips Semiconductors,
spun out in 2006, later merged with Freescale (itself the former Motorola Semiconductor) in 2015.
That lineage explains the catalogue's shape: NXP owns product lines that were once three separate
industry giants, and the naming conventions never fully converged.

NXP is the world's largest automotive semiconductor supplier and the dominant NFC vendor. It is also
the origin of **I²C** — the bus that half the components in this repository sit on.

---

## 2. Product lines and how they fit together

| Line | Lineage | What it is |
|---|---|---|
| **i.MX** (`i.MX 6/7/8/9`, `i.MX RT`) | Freescale | Application processors (Cortex-A) and crossover MCUs (`RT`, Cortex-M7/M33). The `i.MX RT` line is the closest competitor to the [ESP32-P4](../../components/espressif/esp32-p4/README.md) |
| **LPC** | Philips/NXP | General-purpose Cortex-M MCUs |
| **Kinetis** (`MK…`) | Freescale | Cortex-M MCUs; being folded into MCX |
| **MCX** | NXP (new) | The unified successor to LPC and Kinetis |
| **S32** | Freescale/NXP | Automotive processors |
| **PN5xx / PN7xxx / NTAG** | Philips | **NFC** controllers and tags. The market leader |
| **PCA / PCF / PCT** | Philips | I²C peripherals — I/O expanders (`PCA9555`), RTCs (`PCF8563`), LED drivers (`PCA9685`). **The parts most likely to appear beside an ESP32** |
| **74HC / 74LVC / 74AHC** | Philips | Logic families |
| **TJA / TJF** | | CAN, LIN, automotive Ethernet PHYs |
| **PTN / PCA / TFA** | | USB-C PD controllers, muxes |

**How this connects to the rest of this repository:** NXP's `PCA`/`PCF` I²C peripherals are the
canonical way to add I/O to a pin-starved MCU, and NXP defined the I²C addressing rules that the
[CST816D at `0x15`](../../components/hynitron/cst816d/README.md) and the
[DRV2605L at `0x5A`](../../components/texas-instruments/drv2605l/README.md) both obey. If a future
board in this set adds an I/O expander, it will very likely be an NXP part or a clone of one.

---

## 3. Market position

Premium, automotive-grade, heavily certified, extensively documented. NXP competes with
[TI](../texas-instruments/README.md), STMicroelectronics, Infineon, Renesas and Microchip.

Documentation quality is **excellent**: full reference manuals (often 1,000+ pages), errata, app
notes, IBIS models, and reference designs, all public. The friction is entirely in *access*
(see §5 and §7), not in *existence*.

**NDA-gated material does exist**, principally for NFC secure-element programming and some
automotive security features. This is a genuine and well-known limitation: the public `PN5xx`
datasheet describes the hardware, while the firmware/secure-element interface requires a partner
agreement. Treat any NFC secure-element register claim from a public source with suspicion.

---

## 4. Part numbering

NXP has **at least three unreconciled numbering schemes**, by lineage:

```
# Philips heritage — function-coded, still the clearest
PCA 9685 PW
│   │    └─ Package (PW = TSSOP, D = SOIC, BS = HVQFN ...)
│   └────── Function/series index
└────────── Family: PCA/PCF = I2C peripheral, PN = NFC, TJA = automotive transceiver

# Freescale heritage — dense and positional
MK 64 F N1M0 V LL12
│  │  │     │ └─ Package + temperature + speed
│  │  │     └─── Qualification
│  │  └───────── Memory size / feature block
│  └──────────── Family index
└─────────────── MK = Kinetis

# i.MX — marketing-style, with a separate orderable part number
i.MX 8M Plus  ->  MIMX8ML8DVNLZAB
```

**The practical rule: NXP has a *marketing* name and an *orderable* part number, and they are
different strings.** "i.MX 8M Plus" is not a part number. Documentation is indexed under the
marketing name; ordering and datasheet URLs use the orderable number. Budget time for the
translation. **[inference]** — this is an observation about the catalogue's structure, not a
documented NXP policy.

---

## 5. Documentation: URL patterns

| Document class | Pattern | Status |
|---|---|---|
| Corporate / product | `https://www.nxp.com/products/...` | ✅ **with `curl` UA**, ❌ 404 with browser UA (S1, S2) |
| **Datasheet** | `https://www.nxp.com/docs/en/data-sheet/<PART>.pdf` | ✅ **with `curl` UA** (S3) |
| Reference manual | `https://www.nxp.com/docs/en/reference-manual/<DOC>.pdf` | **[unverified]** — inferred by symmetry; not probed |
| Application note | `https://www.nxp.com/docs/en/application-note/<DOC>.pdf` | **[unverified]** — inferred; not probed |
| User guide | `https://www.nxp.com/docs/en/user-guide/<DOC>.pdf` | **[unverified]** — inferred; not probed |

The `docs/en/<class>/<name>.pdf` scheme is pleasantly regular. The document name is usually the part
number for datasheets and an internal document ID (e.g. `AN12345`) otherwise.

### The retrieval procedure for this vendor

```bash
# DO NOT set a browser User-Agent. Use curl's default.
curl -sSL -o PN7150.pdf https://www.nxp.com/docs/en/data-sheet/PN7150.pdf
head -c 4 PN7150.pdf | od -c | head -1     # expect  %  P  D  F
```

If that fails, **then** try rotating UAs — but start with the default, contrary to the usual habit.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ✅ Excellent, full catalogue |
| NXP direct | ✅ Sells samples and dev boards |
| LCSC | ✅ Good for the `PCA`/`PCF`/`74` commodity parts; thin for MCUs |
| AliExpress | ⚠️ Commodity logic and I²C parts widely counterfeited or clone-sourced |

**[unverified]** No price observations are recorded. See
[markets/vendor-comparison.md](../../guides/markets/vendor-comparison.md).

---

## 7. Gotchas

- **Inverted UA blocking.** The headline finding. See the TL;DR and §5. Also recorded in the
  repository's [crawler access table](../../ai-crawler-site-access-table.md).
- **A 404 from `nxp.com` does not mean the document is absent.** It very likely means your
  User-Agent. Re-probe before concluding anything.
- **Three numbering schemes.** See §4.
- **Marketing name ≠ orderable part number.** See §4.
- **NFC secure-element documentation is NDA-gated.** See §3.
- **Freescale-era documents may still carry Freescale branding and document IDs**, and older links
  to `freescale.com` are dead. Search by document ID rather than by URL.
- **Reference manuals are enormous.** A 1,500-page RM is normal. Plan to search it, not read it.

---

## 8. Parts and devices we document

**No README records yet — but we hold two NXP datasheets**, and notably we obtained them *without*
touching `nxp.com` (which would have required the UA inversion in §7).

| Part | Artifact | Bytes | Record |
|---|---|---|---|
| **PCF85063A** (tiny RTC/calendar, I²C) | [`components/nxp/pcf85063a/artifacts/pcf85063a-datasheet.pdf`](../../components/nxp/pcf85063a/artifacts/pcf85063a-datasheet.pdf) | 726,288 | ❌ **missing** |
| **PCF8563** (RTC/calendar, I²C), Rev. 11 | [`components/nxp/pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf`](../../components/nxp/pcf8563/artifacts/pcf8563-datasheet-rev-11.pdf) | 495,457 | ❌ **missing** |

Both are **`PCF` Philips-heritage I²C peripherals** — exactly the category §2 predicted would be the
NXP parts most likely to appear beside an ESP32.

**Provenance:** both shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive.
**Neither part is fitted on the knob board.** See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).

See also [`components/haoyu/hym8563/`](../haoyu/README.md) — the **HYM8563** is a widely-used
PCF8563 work-alike, and the two datasheets are worth reading together.

Writing these records is **outstanding work**.
---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | **Negative probe** — NXP home with browser UA | probe | https://www.nxp.com/ (Chrome 131 UA) | 2026-08-24 | **HTTP 404** |
| S2 | NXP home with default `curl` UA | probe | https://www.nxp.com/ (`curl/8.5.0`) | 2026-08-24 | **HTTP 200** — the inversion |
| S3 | PN7150 datasheet, both UAs | probe | https://www.nxp.com/docs/en/data-sheet/PN7150.pdf | 2026-08-24 | **404 with Chrome UA, 200 with `curl` UA** — the `docs/en/data-sheet/<PART>.pdf` pattern works, but only unauthenticated-looking |
| S4 | UA rotation set | probe | https://www.nxp.com/ with WhatsApp, ChatGPT-User, ClaudeBot and Safari UAs | 2026-08-24 | **All returned 404.** Only the bare `curl` UA succeeded |

> **Evidence boundary.** S1–S4 are **HTTP status probes performed 2026-08-24**; they were **not**
> byte-validated for `%PDF` magic, so S3 establishes that the URL responds, not conclusively that it
> serves a valid PDF. Everything in §1–§4 and §6 is **general industry knowledge, not verified in
> this pass**, and no NXP document has been retrieved into this repository. The reference-manual,
> app-note and user-guide URL patterns in §5 are explicitly **[unverified]**. Treat this entire guide
> as a starting hypothesis to be confirmed on first real use.

---

## Related

- [Vendor guide index](../README.md)
- [Repository crawler / site-access table](../../ai-crawler-site-access-table.md) — where the UA finding is also recorded
- [Texas Instruments](../texas-instruments/README.md) — the contrasting case: browser UA works fine
- [Espressif](../espressif/README.md)
