# Sitronix — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation for Sitronix display-controller ICs — and, more
usefully, for understanding **why you usually cannot get it from Sitronix.**

> **TL;DR** — Sitronix does not publish register-level datasheets publicly. The ST77916 specification
> we hold was obtained from **Espressif's** CDN, not Sitronix's site:
> `https://dl.espressif.com/AE/esp-iot-solution/ST77916_SPEC_V1.0.pdf` (S2). For Sitronix parts, the
> practical sourcing order is: **silicon vendor's BSP repo → panel-module maker → Sitronix**.

---

## 1. Who they are

Sitronix Technology Corporation (矽創電子, Hsinchu, Taiwan; TWSE: 8016) designs display driver and
controller ICs — mostly for small and medium panels — plus touch controllers and some sensors. Its
`ST77xx` family is, by volume of hobbyist and embedded code written against it, one of the most
widely deployed display controller families in existence.

Their corporate site is `https://www.sitronix.com.tw/` and is **Traditional-Chinese-first** with an
English mirror at `/en/` (S1, S3, title `Index - 矽創電子股份有限公司`, verified 2026-08-24).

Sitronix is a *component* vendor. Crucially, **you almost never buy from Sitronix** — you buy a panel
module from a module house that has already bonded a Sitronix die to a glass panel. That commercial
reality is the root cause of every documentation problem in §7.

---

## 2. Product lines

| Line | What it is | Notes |
|---|---|---|
| **`ST77xx` — TFT LCD controllers** | `ST7735`, `ST7789`, `ST7796`, `ST77916`, `ST77922` | The dominant line. SPI / QSPI / RGB / MIPI-DSI depending on part |
| **`ST7565` / `ST75xx` — monochrome LCD** | STN/FSTN segment and dot-matrix drivers | Legacy but still shipping |
| **`ST1633` / `ST16xx` — touch controllers** | Capacitive touch | Competes with [Hynitron](../hynitron/README.md) and Goodix |
| **`ST32xx` — OLED / AMOLED drivers** | Small-panel OLED | Adjacent to the [SH8601](../../components/generic/sh8601-compatibility-driver/README.md) problem space |

**How they fit together:** the number after `ST77` tracks roughly with capability and era, not a
clean hierarchy. `ST7789` (240×320, SPI) is the classic; `ST77916` is a newer, higher-resolution
part with a **QSPI** interface, which is why it turns up on round 360×360 panels where pin count is
constrained. See the [ST77916 record](../../components/sitronix/st77916/README.md).

---

## 3. Market position

Sitronix competes with Ilitek, Novatek, Himax, Solomon Systech (`SSD1306`/`SSD1963`) and Sino Wealth
in the small-panel driver market. It wins on price and on the enormous installed base of driver code.

The market-position fact that actually affects you: **display controllers are sold to module houses
under NDA, in volume.** Sitronix has no commercial reason to serve a public datasheet, and does not.
Everything public is a leak, a redistribution, or a courtesy copy hosted by a downstream silicon
vendor who needed it to write a driver.

---

## 4. Part numbering

```
ST 779 16
│  │   └─ Variant / resolution-class index
│  └───── Generation and interface class (77x = TFT controller/driver)
└──────── Sitronix prefix
```

Conventions that hold in practice, though Sitronix documents none of them:

- **`ST77` = colour TFT controller.** `ST75` = monochrome. `ST16`/`ST17` = touch.
- **A 5-digit part (`ST77916`) is newer than a 4-digit one (`ST7789`)** and generally means higher
  resolution and/or a wider interface (QSPI, RGB, DSI).
- **Suffixes** (`ST7789V`, `ST7789VW`, `ST7796S`) denote die/packaging revisions with *minor but real*
  register differences. `ST7789V` vs `ST7789VW` is a common source of "why does my init sequence not
  work" — and note that Espressif's own [ESP32-P4-EYE](../../devices/espressif/esp32-p4-eye/README.md)
  documents an `ST7789VW` specifically.

**[inference]** This decode is derived from observed part numbers, not from a Sitronix numbering
document. No such document is public as far as we have found.

---

## 5. Documentation: where it actually comes from

Ordered by how likely you are to succeed.

| Rank | Source | Pattern | Notes |
|---|---|---|---|
| 1 | **Silicon-vendor BSP CDN** | `https://dl.espressif.com/AE/esp-iot-solution/<PART>_SPEC_V<x.y>.pdf` (S2) | ✅ How we got ST77916. Espressif hosts controller specs it needed for `esp_lcd_*` components |
| 2 | **Espressif Component Registry** | `https://components.espressif.com/components/espressif/esp_lcd_<part>` | Driver source is often more authoritative than any datasheet — it is what actually works |
| 3 | **Panel-module maker** | Varies | The module house that bonded the die sometimes ships a combined module spec |
| 4 | **Board vendor mirror** | e.g. `https://files.waveshare.com/wiki/common/*.pdf` | Courtesy copies; may be stale. See [Waveshare guide](../waveshare/README.md) |
| 5 | **Third-party datasheet aggregators** | — | **Unreliable provenance.** Frequently OCR'd, watermarked, or the wrong revision |
| 6 | **Sitronix itself** | `https://www.sitronix.com.tw/en/products/` (S3) | Product *listings* and brief selection tables. Register maps: **not published** |

### Driver code as primary source

For Sitronix parts this repository treats **working driver source as evidence of equal or higher rank
than a vendor PDF**, because the PDF is often unobtainable and the driver demonstrably works. The
[ST77916 record](../../components/sitronix/st77916/README.md) and the
[SH8601 compatibility record](../../components/generic/sh8601-compatibility-driver/README.md) are both
built this way. That is a deliberate methodological choice, and it is recorded here so it is not
mistaken for sloppiness.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ❌ Essentially none. Sitronix does not sell through Western catalogue distributors |
| LCSC | ⚠️ Some `ST77xx` bare die/COG parts; not the general case |
| **Panel module houses** | ✅ **The real channel.** You buy the controller pre-bonded to glass |
| AliExpress / Taobao | ✅ As finished panel modules, essentially never as loose ICs |

**Practical consequence:** you do not choose a Sitronix part. You choose a panel, and the panel comes
with whatever controller the module house bonded — which may **change between production runs of the
same part number.** This is precisely the failure mode documented in the
[SH8601 compatibility record](../../components/generic/sh8601-compatibility-driver/README.md).

---

## 7. Gotchas

- **No public register maps.** The single most important fact about this vendor.
- **The controller on your board may not be the controller in the spec sheet.** Vendor storefront,
  wiki, schematic and demo code routinely disagree. Our knob board is the worked example: the
  documentation set names both **ST77916 and SH8601**. That conflict is resolved — in favour of
  ST77916 — in the [ST77916 record](../../components/sitronix/st77916/README.md), and the losing
  claim is preserved rather than deleted in the
  [SH8601 record](../../components/generic/sh8601-compatibility-driver/README.md).
- **Site is Chinese-first.** `/en/` exists but is less complete.
- **Version numbers in leaked specs are unreliable.** `ST77916_SPEC_V1.0.pdf` is *a* revision 1.0;
  there is no index of revisions and no way to know whether a later one exists.
- **Init sequences are the real interface.** Two dies with the same marketing part number can require
  different power-on sequences. Always prefer the init sequence from code known to run on *your*
  panel.
- **Beware "compatible" claims.** ST77916 and SH8601 are *not* register-compatible in general;
  a driver working for one is evidence about that specific panel, not about the controllers.

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [ST77916](../../components/sitronix/st77916/README.md) | QSPI TFT display controller — **primary display record** | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |
| [SH8601 compatibility/conflict record](../../components/generic/sh8601-compatibility-driver/README.md) | The competing driver claim for the same panel | Same board — filed under `generic/` because the SH8601 is **not** a Sitronix part |
| [1.8″ 360×360 LCD panel module](../../components/generic/lcd-panel-module/README.md) | The module the ST77916 die is bonded into | Same board |

Espressif's [ESP32-P4-EYE](../../devices/espressif/esp32-p4-eye/README.md) and
[ESP32-P4X-EYE](../../devices/espressif/esp32-p4x-eye/README.md) both use a Sitronix **ST7789VW**
on their 1.54″ SPI LCD; that controller does not yet have its own component record here.

No device in this repository is manufactured by Sitronix.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Sitronix corporate site | primary | https://www.sitronix.com.tw/ | 2026-08-24 | HTTP 200; Traditional-Chinese-first with `/en/` mirror |
| S2 | ST77916 specification V1.0 | primary (redistributed) | https://dl.espressif.com/AE/esp-iot-solution/ST77916_SPEC_V1.0.pdf | 2026-08-21 | The controller's register set; **and** that Espressif, not Sitronix, is the practical host |
| S3 | Sitronix products index (EN) | primary | https://www.sitronix.com.tw/en/products/ | 2026-08-24 | HTTP 200; listing-level only |
| S4 | `esp_lcd_st77916` component | primary | https://components.espressif.com/components/espressif/esp_lcd_st77916 | 2026-08-21 | Driver source used as evidence per §5 |

> **Evidence boundary.** S1 and S3 are **reachability probes performed 2026-08-24** — they confirm the
> site responds and is Chinese-first, not the completeness of its catalogue. The claim that Sitronix
> publishes **no** public register-level datasheets is a **negative claim from repeated failure**, not
> a verified exhaustive search: it is supported by our inability to source ST77916 from
> `sitronix.com.tw` during the 2026-08-21 pass, and should be read as "we could not, by these methods"
> rather than "it is impossible". §4 (numbering) is explicitly marked **[inference]**.

---

## Related

- [Vendor guide index](../README.md)
- [ST77916](../../components/sitronix/st77916/README.md) · [SH8601 conflict record](../../components/generic/sh8601-compatibility-driver/README.md) · [LCD panel module](../../components/generic/lcd-panel-module/README.md)
- [Hynitron](../hynitron/README.md) — the touch controller bonded into the same module
- [Clones and variants guide](../../guides/markets/clones-and-variants.md) — substituted display controllers as a clone tell
