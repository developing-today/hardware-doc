# Winbond — Documentation Sourcing Guide

Reusable knowledge for obtaining primary documentation for **any** Winbond serial-flash part.

> **TL;DR** — Winbond's documentation is excellent and its download URLs are **unguessable**. The
> datasheet filename embeds the revision letter *and* the release date *and* sometimes the word
> `plus`, URL-encoded with literal spaces:
> `https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf` (S2).
> Never guess a Winbond PDF URL — always resolve it from the product page.

---

## 1. Who they are

Winbond Electronics Corporation (華邦電子, Taichung, Taiwan; TWSE: 2344) is a specialist memory
manufacturer. It is one of a small handful of vendors — with Macronix, GigaDevice, ISSI and Micron —
that supply the serial NOR flash sitting next to essentially every embedded MCU in production.

Winbond is a *component* vendor only; it does not sell boards, so it appears only in
[`components/`](../../components/README.md).

---

## 2. Product lines

| Line | What it is | Relevance |
|---|---|---|
| **`W25Q` — SpiFlash NOR** | Serial NOR flash, 1 Mbit–2 Gbit, SPI / Dual / Quad / QPI | **The line we care about.** The de-facto industry standard part family |
| **`W25N` — SpiFlash NAND** | Serial NAND, 1–4 Gbit, same SPI form factor | Where you go when `W25Q` runs out of density |
| **`W25M`** | Stacked NOR+NAND in one package | Rare |
| **`W95x` / `W97x` — Specialty DRAM** | Low-density DDR/LPDDR for consumer devices | Occasionally the PSRAM beside an MCU, though Espressif's is in-package |
| **`W77` / `W78` — 8051 MCUs** | Legacy microcontrollers | Effectively historical |
| **TrustME `W74M` / `W77Q`** | Secure flash with authenticated commands | Growing; relevant to secure-boot designs |

**How they fit together:** for an ESP32-class design the choice is nearly always *within* `W25Q` —
you are picking a density and a package, not a family. The
[W25Q128JVPIQ record](../../components/winbond/w25q128jv/README.md) is the worked example: 128 Mbit
in an 8-pin SOIC, 3.3 V, quad-capable.

---

## 3. Market position

Commodity, high-volume, dependably available, and **the reference implementation everyone else clones
the command set from.** The practical consequence: SFDP-compliant drivers written against a `W25Q`
part usually work against GigaDevice `GD25Q` and XMC `XM25Q` equivalents, which is why board vendors
substitute them freely. ESP-IDF ships a
[Winbond-specific chip driver](https://github.com/espressif/esp-idf/blob/master/components/spi_flash/spi_flash_chip_winbond.c)
precisely because Winbond is common enough to deserve special-casing.

---

## 4. Part numbering — this one is worth learning properly

```
W25Q 128 J V P I Q
│    │   │ │ │ │ └─ Package: Q = SOIC-208mil (also: S = SOP, T = TFBGA, U = USON/WSON, X = XSON)
│    │   │ │ │ └─── Temperature: I = industrial (-40..+85 °C), blank/E = extended
│    │   │ │ └───── Product version / feature set (P = with programmable options, M = DTR ...)
│    │   │ └─────── Voltage: V = 2.7–3.6 V, W = 1.7–1.95 V, N = 1.65–1.95 V
│    │   └───────── Generation letter: J, F, B, E ... (J is a current, widely-used generation)
│    └───────────── Density in **Mbit** (128 = 128 Mbit = 16 MB)
└────────────────── Family: W25Q = SPI NOR
```

**The trap that catches everyone: density is in megabits, capacity is in megabytes.** A `W25Q128` is
**16 MB**, not 128 MB. Flash-size mismatches in ESP-IDF configuration are frequently this arithmetic
error rather than a hardware fault.

**The generation letter changes behaviour, not just process.** `W25Q128JV` and `W25Q128FV` differ in
SFDP tables, some status-register bits, and erase/program timing. When you have a board with an
unknown flash, read the JEDEC ID (`0x9F`) — the third byte distinguishes generations — rather than
trusting a silkscreen or a vendor spec sheet.

---

## 5. Documentation: what exists and where

| Document class | Where | Guessable? |
|---|---|---|
| Datasheet (PDF) | `https://www.winbond.com/resource-files/<messy-filename>.pdf` | ❌ **No.** See §7 |
| Product page | `https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/?__locale=en&partNo=W25Q128JV` (S3) | ✅ Yes — `partNo=` takes the base part **without** package/temp suffixes |
| Support / resource centre | `https://www.winbond.com/hq/support/resources/` (S4) | ✅ Yes |
| Application notes | Under the same resource centre, gated behind the product page | Partially |
| SFDP tables | **In the datasheet**, chapter "Serial Flash Discoverable Parameters" | — |

### The reliable procedure

1. Hit the product page with `partNo=<base part>` — e.g. `W25Q128JV`, **not** `W25Q128JVPIQ`.
2. Extract the `resource-files` PDF link from that page's HTML.
3. Download and validate by `%PDF` magic.
4. **Record the revision letter and date from the filename**, because that is the only place they
   appear in the URL, and Winbond does not maintain a "latest" alias.

Winbond is one of the few vendors where the URL *is* effectively a pinned revision — an accidental
virtue of the ugly filename. Treat that as a feature and cite the full URL.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | Excellent, full range |
| LCSC | Excellent — this is where Chinese board houses buy, and JLCPCB stocks `W25Q` for assembly |
| AliExpress | Common, and **a known counterfeit/re-mark vector**: re-marked lower-density dies sold as higher density |

Verifying a suspect part is easy and worth doing: read the JEDEC ID, then write-and-verify across the
full claimed address range. Re-marked parts alias at the real density boundary.

---

## 7. Gotchas

- **Datasheet URLs are unguessable.** Literal spaces (`%20`), lowercase part number, revision letter,
  an `MMDDYYYY` date, and sometimes a trailing ` plus`. Our verified example is
  `w25q128jv%20revf%2003272018%20plus.pdf` (S2) — note this is the **revF** document even though the
  part is a **JV** generation part. Do not attempt to construct these.
- **A guessed URL 404s silently-ish.** Our probe of a plausible `revi 11162016` variant returned
  **HTTP 404** (S5), confirming there is no forgiving alias.
- **Density is in Mbit.** See §4.
- **`partNo=` wants the base part.** Suffixes make the product-page query fail to match.
- **The `hq` path segment matters.** Winbond runs regional sites; `www.winbond.com/hq/...` is the
  global English one. Other locales exist and have different paths.
- **Board vendors substitute flash silently.** A schematic saying `W25Q128` is a *density and
  interface* claim, not a manufacturer claim. Confirm by JEDEC ID on the actual unit.

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [W25Q128JVPIQ](../../components/winbond/w25q128jv/README.md) | 128 Mbit (16 MB) SPI NOR flash | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — the ESP32-S3 application flash |

No device in this repository is manufactured by Winbond.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Winbond corporate site | primary | https://www.winbond.com/ | 2026-08-24 | Reachable (HTTP 200) |
| S2 | W25Q128JV datasheet | primary | https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf | 2026-08-21 | The `resource-files` filename convention. Cited by the [W25Q128JVPIQ record](../../components/winbond/w25q128jv/README.md) |
| S3 | Serial NOR Flash product page, `partNo=W25Q128JV` | primary | https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/?__locale=en&partNo=W25Q128JV | 2026-08-21 | The `partNo=` query pattern |
| S4 | Winbond support resources | primary | https://www.winbond.com/hq/support/resources/ | 2026-08-24 | HTTP 200 |
| S5 | Negative probe — constructed filename | probe | https://www.winbond.com/resource-files/w25q128jv%20revi%2011162016.pdf | 2026-08-24 | **HTTP 404** — filenames cannot be constructed |

> **Evidence boundary.** S1, S4 and S5 are reachability probes performed **2026-08-24**. S2 and S3
> were retrieved 2026-08-21 during the component pass and are cited in the part record. The
> part-numbering decode in §4 is **inference** from the datasheet's ordering-information section
> combined with the specific part we hold; the voltage and package letter tables are **not**
> individually verified for every letter and should be checked against the datasheet's ordering
> section before being relied on for a new part.

---

## Related

- [Vendor guide index](../README.md)
- [W25Q128JVPIQ component record](../../components/winbond/w25q128jv/README.md)
- [Espressif vendor guide](../espressif/README.md) — the SoC that boots from this flash
