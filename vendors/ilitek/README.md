# Ilitek — Documentation Sourcing Guide

**ILI Technology Corp. ("Ilitek")**, 8F No. 38 Taiyuan St, Jhubei City, Taiwan 302 — display driver and touch controller ICs.

Research retrieved **2026-08-30**.

> **The one-line answer:** Ilitek parts are extremely common and their specifications circulate widely, but **not from Ilitek**. The document retained here came from a third-party mirror that Espressif itself links to. The good news: unlike [Jadard](../jadard/README.md), Ilitek specifications **fully document the paged manufacturer register set**.

---

## 1. Who they are

One of the most widely used display-driver IC vendors in the hobbyist and low-cost-module world. The `ILI` prefix is ubiquitous.

| Family | Era / class | Examples |
|---|---|---|
| `ILI93xx` / `ILI94xx` | Older SPI / parallel controllers **with** internal GRAM | `ILI9341`, `ILI9488` |
| `ILI98xx` | MIPI-DSI a-Si single-chip drivers, generally **GRAM-less** | **`ILI9881C`**, `ILI9882T`, `ILI9806E`, `ILI7807S` |
| `ILI21xx` | Touch controllers | `ILI2118` |

⚠ **The numbering is not a compatibility guide.** `ILI9341` and `ILI9881C` share a prefix and nothing else architecturally — different interface, different era, and one has GRAM while the other does not.

---

## 2. Parts we document

| Part | Record | What it is |
|---|---|---|
| **ILI9881C** | [components/ilitek/ili9881c](../../components/ilitek/ili9881c/README.md) | a-Si TFT single-chip driver, MIPI-DSI, 800×1280, 16.7 M colour, no GRAM |

---

## 3. ⚠ `ILI9981C` does not exist

Worth stating at vendor level because the error propagated through five files in this repository.

There is **no Ilitek part numbered `ILI9981C`**, and no `esp_lcd_ili9981c` component. The real part is **`ILI9881C`**. Full disproof — registry 404 vs 200, mainline Linux driver listing, and Waveshare's own Kconfig — is in [ILI9881C §"This part is ILI9881C"](../../components/ilitek/ili9881c/README.md#-this-part-is-ili9881c-the-repository-called-it-ili9981c-that-part-does-not-exist).

**Generalisable lesson:** Ilitek's dense numbering (`9881`, `9882`, `9805`, `9806`, `9322`, `9341`, `9488`, `7807`) makes single-digit transcription errors easy and hard to spot. Before creating any record for an `ILI` part, verify the number against **two** independent indexes — the Espressif component registry and the mainline Linux `drivers/gpu/drm/panel/` listing both work well and are quick:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://components.espressif.com/api/components/espressif/esp_lcd_<part>"
curl -s "https://api.github.com/repos/torvalds/linux/contents/drivers/gpu/drm/panel" \
  | grep -o '"name": "panel-ilitek-[^"]*"'
```

---

## 4. Documentation: where it actually comes from

No usable Ilitek public download portal was found. Specifications circulate through module houses, LCD resellers and document-aggregator sites.

| Document | Actual source | Notes |
|---|---|---|
| **ILI9881C Specification V092** (`ILI9881C_IDT_V092_20141105`, 320 pp) | `https://www.internetsomething.com/lcd/ILI9881C-3lane-mipi-gramless.pdf` | ⚠ **HTTP 520** on browser UAs; **`WhatsApp/2.23.20.0` succeeded** |

**Notably, this is the URL Espressif itself links** from the `esp_lcd_ili9881c` component README, under the heading "Link to datasheet". Espressif is depending on the same third-party mirror — which means if that host goes away, the official pointer breaks too. The file has been retained in this repository accordingly.

### 4.1 The ESP-IDF component README trick works here too

Same recipe as for [Jadard §3.1](../jadard/README.md#31--the-highest-yield-trick-read-the-esp-idf-component-readme):

```bash
curl -sSL -o c.zip "https://components-file.espressif.com/components/espressif/esp_lcd_ili9881c/1.1.0/espressif__esp_lcd_ili9881c-v1.1.0.zip"
unzip -p c.zip '*/README.md' | grep -i datasheet
```

The difference from Jadard and Fitipower: Espressif's link here points **off-site** to a third-party mirror rather than to its own CDN. Do not assume the "Link to datasheet" will be an Espressif-hosted URL.

---

## 5. ⭐ Ilitek documents the manufacturer register set — and that is unusual

The most valuable thing about this vendor, and the main reason to seek out an Ilitek specification even when working on a different vendor's part.

The ILI9881C specification's §5 contains **per-page command descriptions across all 11 command pages**, with bit-field tables, reset defaults, restrictions and per-power-state availability. Page selection is documented explicitly as the `FFh` EXTC register taking `98h, 81h, PAGE[7:0]`.

Compare:

| Vendor | Page-select | Manufacturer registers documented? |
|---|---|---|
| **Ilitek** | `FFh` + `98h 81h <page>` | ✅ **Fully** |
| [Sitronix](../sitronix/README.md) | `F0h`–`F3h` | ✅ Yes |
| [Jadard](../jadard/README.md) | `E0h` after an `E1/E2/E3` unlock | ❌ **No** |

**Practical use:** when reverse-engineering an undocumented paged init table from another vendor, an Ilitek spec of the same era and class is a useful *structural* analogue — it tells you what kinds of registers occupy a gate-timing or power page. It is **not** a substitute register map and values must never be carried across. This is how the [JD9365 analysis](../../components/jadard/jd9365/README.md#5--register-0x40--what-it-actually-is) framed its inferences.

---

## 6. Access traps

| Trap | Detail |
|---|---|
| **`internetsomething.com` returns HTTP 520 to browser UAs** | A 16-byte `error` body. **`WhatsApp/2.23.20.0` returned the real 9.8 MB PDF.** ⚠ **Still to be added** to the repo-root [`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md) — this pass was scoped to `components/**` and `vendors/**` and could not write there |
| **Espressif's "official" link is third-party** | §4. Mirror it locally; do not rely on the pointer |
| **Per-configuration specification documents** | The retained file is the **3-lane, MIPI, GRAM-less** variant. Other lane counts / GRAM configurations may be separate documents. Check the cover before assuming a spec covers your configuration |
| **Old parts** | The ILI9881C spec dates from **2014**. Lifecycle and availability need independent checking |
| **Dense numbering** | §3 |
| **Large files** | The ILI9881C spec is 9.8 MB. Budget for it |

---

## 7. Part numbering

`ILI` + 4 digits + optional letter, e.g. `ILI9881C`, `ILI9882T`, `ILI9806E`.

- The trailing letter is a **variant**, not decoration — `ILI9881C` and `ILI9882T` are different parts with different drivers in mainline Linux.
- Documents are named `<PART>_IDT_V<version>_<YYYYMMDD>`, e.g. `ILI9881C_IDT_V092_20141105`. **This is a useful search string** and appears on the cover page, so it survives re-hosting and renaming.

---

## 8. Software

| Target | Driver |
|---|---|
| ESP-IDF | **`espressif/esp_lcd_ili9881c`** — registry, current **v1.1.0**. Requires ESP-IDF v5.3+ and a P4-class chip |
| Linux | **`drivers/gpu/drm/panel/panel-ilitek-ili9881c.c`** — mainline, long-standing, covers multiple panels. Also a good source of real init sequences |
| Arduino | None for DSI parts. The older GRAM-based `ILI9341`/`ILI9488` are extremely well supported (TFT_eSPI, Adafruit, LovyanGFX, Arduino_GFX) |

Mainline Ilitek panel drivers as of 2026-08-30: `ili7807s`, `ili9322`, `ili9341`, `ili9488`, `ili9805`, `ili9806e` (core/dsi/spi), `ili9881c`, `ili9882t`.

---

## 9. Checklist for the next Ilitek part

1. **Verify the part number exists** against two indexes (§3) before anything else.
2. Check the **ESP-IDF component registry** for `esp_lcd_<part>` and read its README's datasheet link — expect it to point off-site (§4.1).
3. Check **mainline Linux** `drivers/gpu/drm/panel/panel-ilitek-*`.
4. Search the document-number pattern `<PART>_IDT_V*` (§7).
5. **Rotate UAs** — the known mirrors block browser UAs (§6).
6. Validate `%PDF-` magic and check the cover for the **configuration variant** (lane count, GRAM).
7. Expect the register map to be **present** — unusual and worth exploiting (§5).
8. Record failures in [`component-download-failures.txt`](../../component-download-failures.txt).

---

## 10. Sources

| Title | URL | Retrieved | Notes |
|---|---|---|---|
| ILI9881C Specification V092 | <https://www.internetsomething.com/lcd/ILI9881C-3lane-mipi-gramless.pdf> | 2026-08-30 | 9 842 657 B, `57b146b8…`. 520 on browser UA; **WhatsApp UA worked** |
| `esp_lcd_ili9881c` component | <https://components.espressif.com/components/espressif/esp_lcd_ili9881c> | 2026-08-30 | v1.1.0; its README supplies the mirror URL above |
| `drivers/gpu/drm/panel/` listing | <https://github.com/torvalds/linux/tree/master/drivers/gpu/drm/panel> | 2026-08-30 | Ilitek driver inventory; disproves `ILI9981C` |

## Related

- [ILI9881C component record](../../components/ilitek/ili9881c/README.md)
- [Jadard sourcing guide](../jadard/README.md) — the contrasting case: no register map published
- [Fitipower sourcing guide](../fitipower/README.md) — the driver pair on the *other* Espressif devkit panel revision
- [Sitronix sourcing guide](../sitronix/README.md) — the third paging convention
- [Vendor guides index](../README.md)
