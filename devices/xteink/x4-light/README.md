# Xteink X4 Light — FCC ID `2BTR9-X4L`

> **This device has not been announced, listed, priced or reviewed.** It exists
> as a **granted United States equipment authorization**, dated **2026-08-13**,
> and as three public exhibits including photographs. Research retrieval date
> **2026-09-11**.
>
> **Depth: certification-only.** There is no board profile, no firmware support,
> no teardown, no price and no vendor statement. Everything below is either read
> off the FCC record or explicitly labelled as absent.

## Why this record exists

The 2026-09-04 family sweep recorded, under *"Models that do not exist"*, that
`X4 Plus / Air / Pro Max` had **"No evidence… not present in the vendor
catalogue, the vendor's collection handles, the FreeInk board enum, or 1,798
Reddit posts."** That was correct for those three names and remains correct.

It was not correct that the family was closed. Enumerating the vendor's **FCC
grantee code** — which the earlier sweep could not do, because no FCC ID had been
read off any board and the grantee was unknown — returns **five** Xteink devices,
and one of them is a product nobody has written about:

| FCC ID | Granted | Device description | Documented in this repository |
|---|---|---|---|
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 | [`../x3/`](../x3/README.md) |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 | [`../x4/`](../x4/README.md) |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro | [`../x4-pro/`](../x4-pro/README.md) |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic | [`../x4-classic/`](../x4-classic/README.md) |
| **`2BTR9-X4L`** | **2026-08-13** | **XTEINK X4 Light** | **this record** |

**The lesson is procedural and worth carrying forward: enumerate the grantee
code, not the product name.** A vendor's FCC grantee index lists every device it
has certified for the US, including ones it has never mentioned.

## Identity

| Field | Value | Evidence |
|---|---|---|
| Marketed name | **XTEINK X4 Light** | **[REG]** FCC device description and the test report's `EUT Name` |
| FCC ID | **`2BTR9-X4L`** | **[REG]** |
| Grantee / product code | `2BTR9` / `X4L` | **[REG]** |
| Model No. (test report) | `XTEINK X4 Light` | **[REG]** |
| **Hardware Version** | **V1.0** | **[REG]** test report §1.1 |
| **Software Version** | **V1.0** | **[REG]** test report §1.1 |
| Applicant | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.** | **[REG]** |
| Application / final action | **2026-08-13** | **[REG]** |
| Test lab / report no. | Shenzhen BKC Testing Co., Ltd. · `BKC26074010GE-2` | **[REG]** |
| Equipment class | DTS — Digital Transmission System | **[REG]** |
| Model differences | **`N/A`** — a single model, no variants declared | **[REG]** |

## What "Light" means is **not established**

The filing does not say. Two readings are equally consistent with the evidence:

1. **Frontlight.** This is what the community has asked for continuously since
   April 2026 and did not get in the X4 Classic. Four of the five top replies to
   the vendor's own 2026-09-03 announcement were requests for a lit,
   buttons-only reader. A community post on 2026-08-15 —
   [r/XTEINK `1vp4mmh`](https://old.reddit.com/r/XTEINK/comments/1vp4mmh/),
   *"It appears that the X4 with a front light is in development"* — **predates
   the 2026-08-13 grant by two days**, which is suggestive and nothing more.
2. **Lightweight.** The X4 Classic is already 68 g and 4.9 mm.

**This record takes no position.** A frontlight would appear in the internal
photographs and possibly in the user manual — both embargoed until
**2027-02-09**. Do not repeat "the X4 Light has a frontlight" as though it were
established; it is a hypothesis with a plausible motive and no evidence.

## What the filing does establish

| Field | Value | Source |
|---|---|---|
| **Radio** | 2.4 GHz only, **2412–2462 MHz**, channels 1–11 | test report §1.2 |
| Modes | 802.11b (DSSS), 802.11g / n HT20 / n HT40 (OFDM) | test report §1.5 |
| **Max conducted RF output** | **8.13 dBm** | test report §1.1 |
| **Antenna** | **Internal, maximum gain 5.19 dBi** | test report §1.1 |
| Power supply | **`Input: DC 5V from adapter`**, **`Adapter: N/A`** — it ships without a PSU | test report §1.1 |
| Compliance parts tested | 15.203, 15.247(a)(2)(b)(3)(b)(4)(d)(e), 15.205, 15.207, 15.209 — **all PASS** | test report §1.3 |
| Intended environment | residential, commercial, light industrial | test report §1.1 |

**No Bluetooth exhibit was filed under this ID.** The X4 Classic's RF-exposure
report contains BLE conducted-power figures; the X4 Light's does not appear to.
That is **not** evidence that BLE is absent — a separate DSS/BLE filing or a
module-based approval could cover it — but it is a difference between the two
records and it is recorded as such.

### The antenna is not the X4 Classic's

| | X4 Classic (`2BTR9-X4C`) | **X4 Light (`2BTR9-X4L`)** |
|---|---|---|
| Antenna part | **`KH3216-A35`** (Shenzhen Jinhangbiao) | **not named in the public exhibits** |
| Max gain | **2.30 dBi** | **5.19 dBi** |

A 5.19 dBi maximum gain against 2.30 dBi is a **different antenna**, not a
different measurement of the same one. Something about the RF layout or the
enclosure changed. What, is unknown.

## What it looks like

The X4 Light's **External Photos exhibit is public** — unlike the X4 Classic's,
which is embargoed. It is retained at
[`artifacts/certification/2BTR9-X4L-external-photos.pdf`](artifacts/certification/2BTR9-X4L-external-photos.pdf)
(3,485,136 B, SHA-256 `c6457651f19b4cac…`, **9 embedded images**), photographed
against a millimetre rule.

Read directly off those photographs:

| Observation | Confidence |
|---|---|
| Portrait slab, rounded corners, **≈114 × 69 mm** scaled off the rule | **read from image**, ±2 mm |
| Two body colours photographed: **black** and **white/silver** | read from image |
| `XTEINK` wordmark on the rear, upper third | read from image |
| **An oval magnet outline** centred on the rear — the same feature the X4 Classic's FAQ calls a "built-in magnetic ring" | read from image |
| **Four gold pogo contacts on the bottom edge.** No USB socket visible on any face | read from image |
| **Two button protrusions on the left edge, one on the right** | read from image |

**This is the X4 Classic's enclosure generation.** Same proportions, same magnet,
same four-pin pogo pad, same side-button arrangement. **It is not proof that the
internals match**, and this record does not claim it.

**Nothing in the external photographs shows a lit screen or a frontlight
diffuser**, which is the one thing that would settle the naming question. The
device is photographed powered off.

## Embargo schedule

| Exhibit | Size | **Public from** |
|---|---|---|
| External Photos | 3.3 MB | **already public — retained here** |
| Label and Information | 1.2 MB | already public — retained here |
| Antenna Report | 1.5 MB | already public |
| Test Report | 5.7 MB | already public — retained here (1.5 MB variant fetched) |
| RF Exposure Report | 143 KB | already public |
| **Internal Photos** | 842.4 KB | **2027-02-09** |
| Users Manual | 3.9 MB | **2027-02-09** — *the manual will name the features* |
| Test Setup Photos | 373.7 KB | 2027-02-09 |
| Block Diagram · Schematics · Operational Description | 53.6 KB / 573.2 KB / 89 KB | **never** |

**Re-check on 2027-02-09.** The user manual is the cheapest route to knowing what
"Light" means.

## What is completely unknown

- **SoC.** No board profile exists in any firmware project. Not in the FreeInk
  `enum class Board` at HEAD (`9f4d3f9`, 2026-09-10), not in CrossPoint, not in
  Draftling, not in any GitHub code-search result. **A new Xteink board normally
  reaches the SDK before it reaches the shop — this one has reached neither.**
- **Panel size, resolution, controller.**
- **Whether it has a frontlight, a touchscreen, an IMU, an RTC, a fuel gauge.**
- **Price, launch date, market, colours offered for sale.**
- **Whether it will ship at all.** A granted FCC authorization is a strong signal
  of intent — it costs real money and is usually filed weeks before launch, which
  is exactly the pattern the X4 Classic followed (granted 2026-07-20, listed
  2026-09-06, a 48-day gap). By that precedent an X4 Light would list around
  **2026-09-30**. **That is an extrapolation from one data point and should be
  treated as such.**

## Community awareness

Near zero. Across 94 catalogued X4C-related Reddit posts and 332 unique posts
from a broad launch-week sweep, **no post names "X4 Light"**. Two posts are
consistent with somebody having seen something:

- [r/XTEINK `1vp4mmh`](https://old.reddit.com/r/XTEINK/comments/1vp4mmh/),
  2026-08-15 — *"It appears that the X4 with a front light is in development"*
- [r/XTEINK `1w1tcx9`](https://old.reddit.com/r/XTEINK/comments/1w1tcx9/),
  2026-08-29, 80 pts — *"Well well look what we have here"*

Neither was fetched in full this pass, and neither is claimed here as evidence
about the X4L. **The FCC grantee index is, as far as this research can tell, the
only public place the name "XTEINK X4 Light" appears.**

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Published | Establishes |
|---|---|---|---|---|---|---|---|---|
| XL01 | FCC ID `2BTR9-X4L` record | US FCC via fccid.io | **primary (regulatory)** | regulatory record | <https://fccid.io/2BTR9-X4L> | 2026-09-11 | 2026-08-13 | Existence, name, applicant, exhibit list, embargo dates |
| XL02 | FCC grantee index `2BTR9` | US FCC via fccid.io | primary (regulatory) | regulatory record | <https://fccid.io/2BTR9> | 2026-09-11 | — | The complete five-device Xteink certification history |
| XL03 | Test Report `BKC26074010GE-2` | BKC Testing, filed by applicant | primary | test report | <https://fccid.io/2BTR9-X4L/Test-Report/Test-Report-9556502.pdf> | 2026-09-11 | 2026-08-13 | EUT name, HW/SW V1.0, 8.13 dBm, 5.19 dBi, DC 5 V, channel list, PASS summary |
| XL04 | External Photos | applicant | primary | photographs | <https://fccid.io/2BTR9-X4L/External-Photos/External-Photos-9556497.pdf> | 2026-09-11 | 2026-08-13 | Form factor, two colours, pogo pad, magnet outline, button layout |
| XL05 | Label and Information | applicant | primary | photographs | <https://fccid.io/2BTR9-X4L/Label/Label-and-Information-9556498.pdf> | 2026-09-11 | 2026-08-13 | Compliance-label artwork and placement |

Retrieval required UA `WhatsApp/2.23.20.0`; `fccid.io` serves **403** to a
desktop-Chrome UA and `fcc.report` serves 403 to every UA tried. See
[`../x4-classic/commands.md`](../x4-classic/commands.md) §3.

## See also

[Family index](../README.md) · [X4 Classic](../x4-classic/README.md) — the
enclosure generation this belongs to · [X4 Pro](../x4-pro/README.md) — the only
Xteink with a frontlight today
