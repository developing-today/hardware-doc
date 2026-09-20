# Alpha & Omega Semiconductor (AOS) — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation for **any** AOS discrete or power part.

> **TL;DR** — AOS has the **best URL pattern of any vendor in this repository**. Datasheets are at
> `https://www.aosmd.com/res/data_sheets/<PART>.pdf` — uppercase part number, no revision, no hash,
> no session. Verified 2026-08-24 for `AO3400A` (S2). You can genuinely guess these.

---

## 1. Who they are

Alpha and Omega Semiconductor Limited (Sunnyvale, California and Shanghai; NASDAQ: AOSL) designs and
manufactures **power semiconductors** — MOSFETs, IGBTs, power ICs and protection devices. Unlike most
of the vendors here they are an IDM: they own fabs and packaging.

Their site is `https://www.aosmd.com/` — note the domain is **`aosmd`**, not `aos` or
`alphaomega`, which is the one thing about this vendor that is not obvious.

AOS is a *component* vendor; it appears only in
[`components/`](../../components/README.md).

---

## 2. Product lines

| Line | What it is | Relevance |
|---|---|---|
| **`AO` — MOSFETs** | The core line. N-channel and P-channel, from tiny SOT-23 signal parts to power packages | [AO3400A](../../components/alpha-and-omega-semiconductor/ao3400a/README.md) |
| **`AON` / `AOD` / `AOT` / `AOB`** | The same dies in different packages — `AON` = DFN, `AOD` = DPAK, `AOT` = TO-220, `AOB` = D²PAK | See §4; this is the key to reading the catalogue |
| **`AOZ` — power ICs** | Buck regulators, load switches, LED drivers, eFuses | Competes with [TI](../texas-instruments/README.md) and [SGMicro](../sgmicro/README.md) |
| **IGBTs and SiC** | Higher-power switching | Not relevant to boards of this class |
| **Protection (`AOTVS`, ESD)** | TVS diodes, ESD arrays | Common on USB and connector pins |

**How they fit together:** for a board like ours, AOS supplies the **discrete switching elements** —
the small N-channel MOSFETs used for load switching, level shifting, reverse-polarity protection and
power-path control. These are the parts that a schematic shows as an unremarkable three-terminal
symbol and that nobody thinks about until one is missing on a clone board. See
[clones-and-variants.md](../../guides/markets/clones-and-variants.md).

---

## 3. Market position

**The default cheap-but-real MOSFET.** The `AO3400` family in particular is one of the most widely
used small N-channel MOSFETs in existence — logic-level gate, low R<sub>DS(on)</sub>, SOT-23,
fractions of a cent in volume. It is the part a Chinese board house reaches for without thinking.

AOS competes with Vishay, Infineon, onsemi, Diodes Inc. and Toshiba in the West, and with a large
field of Chinese discrete makers (JSCJ, Slkor, Changjing) domestically. Being an IDM with US
listing puts them in an unusual middle position: cheaper than Western majors, more credible and
better documented than the domestic discrete field.

---

## 4. Part numbering — the package is the prefix

This is the important and slightly unusual part of AOS's scheme:

```
AO 3400 A
│  │    └─ Revision / generation letter — A is a later, improved die than the plain part
│  └────── Part index (encodes voltage class and R_DS(on) class within the family)
└───────── **Package family prefix**: AO = SOT-23, AON = DFN, AOD = DPAK, AOT = TO-220, AOB = D²PAK
```

Rules:

- **The alphabetic prefix is the package**, not the manufacturer name. `AO3400A` and `AON3400` are
  substantially the same die in different packages.
- **The trailing letter is a die generation and it matters.** `AO3400` → `AO3400A` improved
  R<sub>DS(on)</sub> and gate charge. Datasheets are separate; **do not read the `AO3400` datasheet
  for an `AO3400A` part.**
- **The numeric block is not independently decodable** — you cannot read voltage off it. Look it up.
  **[inference]** on this point; AOS publishes no general numbering key we have located.
- **Counterfeits and near-clones are rampant** for `AO3400`-class parts specifically, because they are
  so ubiquitous. Marking is easy to fake and the failure mode (higher R<sub>DS(on)</sub>, so it runs
  hot) is subtle.

---

## 5. Documentation: URL patterns

| Document class | Pattern | Verified |
|---|---|---|
| Corporate site | `https://www.aosmd.com/` | ✅ 2026-08-24 (S1) |
| **Datasheet PDF** | `https://www.aosmd.com/res/data_sheets/<PART>.pdf` | ✅ 2026-08-24 (S2) — **uppercase, guessable** |
| Product category | `https://www.aosmd.com/products/mosfets` | ✅ 2026-08-24 (S3) |
| Application notes | `https://www.aosmd.com/res/application_notes/...` | **[unverified]** — inferred by symmetry with `data_sheets`; not probed |
| SPICE models | Linked from product pages | |

This is the one vendor here where **constructing the URL is the recommended first move** rather than
a last resort. Try `https://www.aosmd.com/res/data_sheets/AO3400A.pdf` before anything else.

### Revision pinning

The URL contains no revision. The **PDF cover carries a `Rev N` marker and a date**; record those.
As with [TI](../texas-instruments/README.md#revision-pinning), the URL is an alias that tracks the
newest revision silently.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| **LCSC** | ✅ Excellent — and the source Chinese board houses use |
| Mouser / Digi-Key | ✅ Good — AOS is properly catalogued in the West |
| AliExpress | ⚠️ Cheap and **heavily counterfeited**; see §7 |
| AOS direct | Volume only |

---

## 7. Gotchas

- **The domain is `aosmd.com`.** Not `aos.com`, not `alphaomegasemi.com`.
- **`AO3400` ≠ `AO3400A`.** Different dies, different datasheets, different specs.
- **Package is encoded in the prefix**, so a "similar part number" may be a completely different
  physical component. See §4.
- **Counterfeit `AO3400A` is a real and common problem.** Symptoms: the part runs hotter than the
  datasheet's R<sub>DS(on)</sub> predicts, and gate threshold is higher than the logic-level spec.
  If a design that should work is thermally marginal, suspect the MOSFET before the design.
- **`AO3400A` is often specified generically.** Board schematics frequently label these simply
  "NMOS" or with a generic footprint. Identifying the actual fitted part usually requires reading the
  package marking on a physical unit. Our
  [AO3400A record](../../components/alpha-and-omega-semiconductor/ao3400a/README.md) should be read
  with that identification caveat.
- **Logic-level gate drive is a spec, not a given.** Many similar-looking SOT-23 MOSFETs need >4.5 V
  V<sub>GS</sub>. On a 3.3 V board that is the difference between working and not.

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [AO3400A](../../components/alpha-and-omega-semiconductor/ao3400a/README.md) | N-channel logic-level MOSFET, SOT-23 | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |

Related power-tree records:
[SGMicro SGM2036-3.3](../../components/sgmicro/sgm2036-3.3/README.md) ·
[TI TLV62569DBVT](../../components/texas-instruments/tlv62569dbvt/README.md) ·
[charger / power-path](../../components/generic/charger-power-path/README.md) ·
[power button](../../components/generic/power-button/README.md).

No device in this repository is manufactured by AOS.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | AOS corporate site | primary | https://www.aosmd.com/ | 2026-08-24 | HTTP 200; the `aosmd.com` domain |
| S2 | AO3400A datasheet | primary | https://www.aosmd.com/res/data_sheets/AO3400A.pdf | 2026-08-24 | **HTTP 200, 317,848 bytes, `%PDF` magic** — the `res/data_sheets/<PART>.pdf` pattern is directly constructible |
| S3 | MOSFETs product category | primary | https://www.aosmd.com/products/mosfets | 2026-08-24 | HTTP 200 |
| S4 | **Negative control** — nonexistent part | probe | https://www.aosmd.com/res/data_sheets/BOGUS999.pdf | 2026-08-24 | **HTTP 404**, 684-byte HTML body. AOS does not soft-404, so a 200 here is trustworthy |

> **Evidence boundary.** S1–S3 are **HTTP reachability probes performed 2026-08-24**. S2 confirms the
> URL resolves; it was **not** re-read for content in this pass — the part's electrical claims live in
> the [component record](../../components/alpha-and-omega-semiconductor/ao3400a/README.md) and were
> retrieved 2026-08-21. The application-note URL pattern in §5 is explicitly **[unverified]**. §3 and
> §7's counterfeit claims are **general industry observation, not measured here**. §4's numeric-block
> statement is marked **[inference]**.

---

## Related

- [Vendor guide index](../README.md)
- [AO3400A](../../components/alpha-and-omega-semiconductor/ao3400a/README.md)
- [SGMicro](../sgmicro/README.md) · [Texas Instruments](../texas-instruments/README.md) — the rest of the power tree
- [Clones and variants](../../guides/markets/clones-and-variants.md) — omitted discretes as a clone tell
