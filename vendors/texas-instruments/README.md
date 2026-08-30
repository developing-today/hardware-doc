# Texas Instruments — Documentation Sourcing Guide

Reusable knowledge for obtaining primary documentation for **any** TI part. TI is the best-documented
vendor in this repository by a wide margin, and it is worth understanding why: the difference between
TI's public register maps and, say, [Sitronix's](../sitronix/README.md) is the difference between
writing a driver from the datasheet and reverse-engineering one from vendor sample code.

> **TL;DR** — Every TI datasheet lives at a **predictable, stable, guessable URL**:
> `https://www.ti.com/lit/ds/symlink/<part-in-lowercase>.pdf`. This works without a session, without
> JavaScript, and without a login. Verified 2026-08-24 for all three TI parts we document (S4).

---

## 1. Who they are

Texas Instruments Incorporated (Dallas, Texas; NASDAQ: TXN) is one of the largest analog and embedded
semiconductor companies in the world. Founded 1930; the company that commercialised the integrated
circuit. For our purposes the relevant fact is not scale but **posture**: TI publishes complete,
English-language, register-level datasheets, application notes, reference designs, IBIS/SPICE models
and evaluation-module documentation for essentially its entire catalogue, without an NDA and without
an account.

TI is a *component* vendor only. It does not sell finished consumer boards, so it never appears in
[`devices/`](../../devices/README.md) — only in [`components/`](../../components/README.md).

---

## 2. Product lines and how they fit together

TI's catalogue is organised by function, not by process or family. The lines that matter to the kind
of board this repository documents:

| Line | What it is | Parts we document |
|---|---|---|
| **Motor drivers / haptics (`DRV`)** | Motor, solenoid, LED and haptic drivers | [DRV2605L](../../components/texas-instruments/drv2605l/README.md), [DRV2605](../../components/texas-instruments/drv2605/README.md) |
| **Audio (`PCM`, `TAS`, `TLV320`)** | `PCM` = data converters (DAC/ADC); `TAS` = amplifiers; `TLV320` = codecs | [PCM5100A](../../components/texas-instruments/pcm5100a/README.md) |
| **Power — switching (`TPS`, `TLV62xxx`, `LM`)** | Buck/boost converters, chargers, power-path | [TLV62569DBVT](../../components/texas-instruments/tlv62569dbvt/README.md) |
| **Power — linear (`TLV7xx`, `TPS7Axx`, `LP`)** | LDO regulators | — (our LDO is an [SGMicro](../sgmicro/README.md) part) |
| **Interface (`SN65`, `TCA`, `TUSB`, `TXB/TXS`)** | Level shifters, I²C expanders/muxes, USB, RS-485 | — |
| **Logic (`SN74`)** | The industry-standard 74-series | — |
| **MCUs (`MSP430`, `MSPM0`, `C2000`, `TM4C`, `CC13xx/CC26xx`)** | 16-bit ultra-low-power, ARM Cortex-M0+/M4, wireless SoCs | — |

The important structural point for board work: TI's **`DRV`, `PCM` and `TLV62` parts frequently sit
next to an Espressif SoC** in exactly the arrangement our knob board uses — TI supplies the analog and
electromechanical periphery that the MCU vendor deliberately does not integrate. See
[Pinouts and buses](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md) for the
worked example.

---

## 3. Market position

Premium-priced, universally second-sourced, indefinitely available. TI parts appear in Chinese
consumer boards **despite** costing more than the local equivalent, usually because a cheap clone of
that exact function does not exist or does not work as well — the DRV2605L's closed-loop LRA
auto-resonance tracking is a good example of a feature nobody has cloned convincingly.

A corollary worth internalising when reading a BOM: **a TI part on an otherwise cost-optimised Chinese
board is a signal.** It marks the function the designer was not willing to compromise on.

---

## 4. Part-numbering conventions

TI part numbers are dense but fully decodable, and the suffix carries the package, which is what you
actually need when reading a board:

```
TLV62569 D BV T
│        │ │  └─ Tape-and-reel / quantity code (T = small reel, R = large reel)
│        │ └──── Package designator (BV = SOT-23-5 / DBV)
│        └────── Package family prefix (D = SOT/SOIC family)
└─────────────── Base part number
```

```
DRV2605 L
│       └─ Variant suffix. Here: I²C-only, no PWM/analog input pin.
└───────── Base part
```

Rules that hold generally:

- **The base part number is what you look up.** The datasheet at `.../symlink/drv2605l.pdf` covers all
  packages of `DRV2605L`; the package suffix does not get its own document.
- **A trailing letter before the package code is a functional variant**, and it matters. `DRV2605`
  and `DRV2605L` are *different parts with different pinouts*, which is exactly why this repository
  keeps [two separate records](../../components/texas-instruments/drv2605/README.md).
- **A trailing `A`** (as in `PCM5100A`) usually denotes a minor silicon revision or improved spec,
  and usually shares a datasheet with the non-`A` part.
- **`R` / `T` suffixes are packaging only** and never change electrical behaviour.

---

## 5. Documentation: what exists and where

TI's documentation is unusually complete. Expect *all* of the following per part, and treat a missing
item as evidence you have the wrong part number rather than evidence TI didn't publish it.

| Document class | URL pattern | Notes |
|---|---|---|
| Datasheet | `https://www.ti.com/lit/ds/symlink/<part>.pdf` | **The workhorse.** Lowercase, no package suffix. Verified (S4) |
| Datasheet (versioned) | `https://www.ti.com/lit/ds/<doc-id>/<doc-id>.pdf` | e.g. `slos825`. Use when you must pin a revision |
| Product page | `https://www.ti.com/product/<PART>` | Uppercase. Ordering, package options, related docs |
| Application note | `https://www.ti.com/lit/an/<doc-id>/<doc-id>.pdf` | |
| User guide (EVM) | `https://www.ti.com/lit/ug/<doc-id>/<doc-id>.pdf` | |
| Errata | `https://www.ti.com/lit/er/<doc-id>/<doc-id>.pdf` | |
| Any literature by ID | `https://www.ti.com/lit/<id>` | Redirects to the right class — handy when you have only a doc number from a citation |

### Revision pinning

TI datasheet URLs of the `symlink` form are **aliases that silently track the newest revision.** The
PDF itself carries the revision in its footer (e.g. `SLOS825C — OCTOBER 2012 — REVISED APRIL 2018`)
and TI includes a *Revision History* table near the end listing what changed per revision. **Record
the literature number and revision letter from inside the PDF**, not the URL, because the URL alone
does not identify what you read. This is the TI analogue of the
[Waveshare `oldid` problem](../waveshare/README.md#the-oldid-gotcha-important).

---

## 6. Distribution

| Channel | Availability | Notes |
|---|---|---|
| TI direct (ti.com store) | Excellent | Sells single units; often the cheapest source for small quantities; ships worldwide |
| Mouser / Digi-Key | Excellent | Full catalogue, full datasheet mirrors |
| LCSC | Good for popular parts | The parts Chinese board houses actually use — `DRV2605L`, `TLV62569` — are stocked; exotic TI parts are not |
| AliExpress | **Counterfeit risk** | TI parts are among the most-counterfeited on the market. Re-marked or blank-die "DRV2605L" is a known problem class |

**[unverified]** No current price observations are recorded here. See
[markets/vendor-comparison.md](../../guides/markets/vendor-comparison.md) for the sourcing-comparison
policy on prices.

---

## 7. Gotchas

- **`www.ti.com` serves fine to scripted clients** (HTTP 200 with a browser User-Agent, verified
  2026-08-24, S4) but the *search* and *parametric-selector* pages are JavaScript applications and
  will not yield results to `curl`. Go directly to `lit/ds/symlink/`.
- **The `symlink` alias moves under you.** See §5.
- **`DRV2605` ≠ `DRV2605L`.** Vendor board documentation and community code routinely name the wrong
  one; the pinouts differ. This repository documents both specifically so the confusion is
  resolvable — see the [DRV2605 record](../../components/texas-instruments/drv2605/README.md).
- **The package suffix is not in the datasheet URL.** `tlv62569dbvt` will 404; `tlv62569` is correct.
  When a datasheet URL 404s, strip suffixes right-to-left before concluding the document is absent.
- **"Enhanced product" / space-grade variants** (`-EP`, `-SP`, `-Q1`) have *separate* datasheets and
  different URLs. `-Q1` (automotive) is the one you will actually encounter.
- **Counterfeits.** See §6. If a part behaves as if a documented register does not exist, consider
  that the die may not be TI's before concluding the datasheet is wrong.

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [DRV2605L](../../components/texas-instruments/drv2605l/README.md) | Haptic driver, I²C `0x5A` | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |
| [DRV2605](../../components/texas-instruments/drv2605/README.md) | Haptic driver, non-`L` variant | *None* — reference/disambiguation record |
| [PCM5100A](../../components/texas-instruments/pcm5100a/README.md) | Stereo audio DAC, no control bus | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |
| [TLV62569DBVT](../../components/texas-instruments/tlv62569dbvt/README.md) | 3.3 V synchronous buck | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |

No device in this repository is manufactured by TI.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | TI corporate site | primary | https://www.ti.com/ | 2026-08-24 | Reachable to scripted clients with a browser UA (HTTP 200) |
| S2 | DRV2605L datasheet | primary | https://www.ti.com/lit/ds/symlink/drv2605l.pdf | 2026-08-24 | HTTP 200 — the `symlink` pattern resolves |
| S3 | PCM5100A datasheet | primary | https://www.ti.com/lit/ds/symlink/pcm5100a.pdf | 2026-08-24 | HTTP 200 |
| S4 | TLV62569 datasheet | primary | https://www.ti.com/lit/ds/symlink/tlv62569.pdf | 2026-08-24 | HTTP 200 — **and** that the package suffix must be stripped (`tlv62569`, not `tlv62569dbvt`) |
| S5 | **Negative control** — nonexistent part | probe | https://www.ti.com/lit/ds/symlink/boguspart999.pdf | 2026-08-24 | **HTTP 404**, 3,298-byte HTML body. TI does *not* soft-404, so a 200 from this pattern is trustworthy |

> **Byte-level verification.** S2 returned 2,642,481 bytes beginning `%PDF`; the negative control S5
> returned a 404 and an HTML body. Unlike [WCH](../wch/README.md#7-gotchas), TI's status codes mean
> what they say.

> **Evidence boundary.** S1–S4 are **HTTP reachability probes performed 2026-08-24**, not content
> reads. They establish that these URL patterns resolve; they do not re-verify the technical content
> of the per-part records, which was retrieved 2026-08-21 and is cited in those records. Claims in
> §3 (market position) and §4 (numbering conventions beyond the parts we hold) are **inference** from
> the parts we document plus general familiarity, and are not individually sourced.

---

## Related

- [Vendor guide index](../README.md)
- [Component index](../../components/README.md)
- [Espressif vendor guide](../espressif/README.md) — the MCU these parts sit beside
- [SGMicro](../sgmicro/README.md) — the low-cost analog vendor TI competes with on these boards
