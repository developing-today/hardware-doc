# Jadard — Documentation Sourcing Guide

**Jadard Technology Inc.** (誠屹科技) — Taiwanese fabless supplier of TFT-LCD display driver ICs.

Research retrieved **2026-08-30**.

> **The one-line answer:** Jadard publishes nothing usable to the public. Every Jadard document in this repository came from a **third party** — one from Espressif's CDN, one from an LCD reseller's WordPress uploads directory. Go to the mirrors first; do not waste time on the vendor.

---

## 1. Who they are

A display-driver IC house whose parts appear widely in low-cost Chinese LCD modules, particularly MIPI-DSI panels in the 5–10 inch range. The `JD` prefix in a panel init table almost always means Jadard.

**They are frequently misattributed.** This repository previously recorded the JD9365 as a **Fitipower** part; it is not. Fitipower (`EK` prefix) and Jadard (`JD` prefix) both supply driver ICs into the same market, and both appear on Espressif-adjacent hardware, which makes the confusion easy. See [`components/fitipower/`](../../components/fitipower/ek79007ad/README.md) for the parts that genuinely are Fitipower's.

Copyright lines in their documents read **"Confidential Copyright © JADARD"**.

---

## 2. Parts we document

| Part | Record | What it is |
|---|---|---|
| **JD9365DA-H3** | [components/jadard/jd9365](../../components/jadard/jd9365/README.md) | a-Si TFT single-chip driver, MIPI-DSI, 800×1280 max, no GRAM |

Other `JD` parts seen but not documented here: `JD9853` (referenced in a Waveshare demo tree), `JD9365D` and other suffixes referenced in third-party init tables with no retrievable document.

---

## 3. ⚠ Documentation: where it actually comes from

**There is no usable Jadard documentation portal.** No public datasheet index, no part search, no download area was found. Everything below is a third-party mirror.

| Document | Actual source | Notes |
|---|---|---|
| **JD9365DA-H3 Data Sheet V0.01** (2020-08-19, 204 pp) | `https://dl.espressif.com/AE/esp-iot-solution/JD9365DA-H3_DS_V0.01_20200819.pdf` | **Espressif's CDN.** Serves cleanly with a normal browser UA |
| **JD9365DA-H3 Application Note V0.03** (2021-02-01, 23 pp) | `https://lcddisplay.co/wp-content/uploads/2023/01/JD9365DA_V0.03_20210201.pdf` | An LCD reseller's WordPress uploads directory. ⚠ **HTTP 403 on browser UAs** — see §5 |

### 3.1 ⭐ The highest-yield trick: read the ESP-IDF component README

**This is how the JD9365 datasheet was found, after a general web search had failed.**

Espressif's `esp_lcd_*` display driver components each carry a README with a table row of the form:

```markdown
| LCD controller | Communication interface | Component name | Link to datasheet |
|     JD9365     |        MIPI-DSI         | esp_lcd_jd9365 | [PDF](https://dl.espressif.com/AE/esp-iot-solution/JD9365DA-H3_DS_V0.01_20200819.pdf) |
```

That link is a **direct, working URL to the manufacturer's datasheet**, mirrored on Espressif's own CDN. It works for other vendors too — the same technique produced a second [EK79007](../fitipower/README.md) revision and the [ILI9881C](../ilitek/README.md) specification in the same session.

Recipe:

```bash
# 1. list versions
curl -s "https://components.espressif.com/api/components/espressif/esp_lcd_<part>" | python3 -m json.tool | grep version

# 2. fetch the package (the registry API's "latest" field is unreliable — it returned 0.1.0
#    while 2.0.1 existed, so construct the URL from the version list yourself)
curl -sSL -o c.zip \
  "https://components-file.espressif.com/components/espressif/esp_lcd_<part>/<ver>/espressif__esp_lcd_<part>-v<ver>.zip"

# 3. read the README
unzip -p c.zip '*/README.md' | grep -i datasheet
```

**Search engines did not find this document.** Bing, Mojeek and DuckDuckGo all returned nothing useful for `JD9365 datasheet`; grep.app was behind a Vercel challenge and the GitHub code-search API required auth. The component README was the only path that worked.

---

## 4. ⚠ What the JD9365DA-H3 datasheet does not contain

Important enough to repeat at vendor level, because it is likely to be true of Jadard's other parts too:

**The datasheet documents the standard MIPI DCS command set only.** The `E0h`-paged manufacturer register banks — where every vendor init table's gamma, gate timing, power and resolution registers live — are **not** documented. See [JD9365 §4](../../components/jadard/jd9365/README.md#4--what-the-public-datasheet-does-and-does-not-contain).

**Consequence for planning:** budget for reverse-engineering. For a Jadard part, the useful register knowledge comes from **driver source**, not from the datasheet:

| Source | Why |
|---|---|
| **Mainline Linux `drivers/gpu/drm/panel/panel-jadard-jd9365da-h3.c`** | 13 panel init tables as of 2026-08-30, with `compatible` strings identifying real products. The single best register reference for this part |
| **Espressif `esp_lcd_jd9365`** | Default init table, reset timing, page-tracking logic |
| **Vendor demo trees** | Board-specific tables |

Cross-correlating the *same register across many panels* is what makes this tractable — it is how register `0x40` was identified. See [JD9365 §5](../../components/jadard/jd9365/README.md#5--register-0x40--what-it-actually-is).

> ⚠ **Pin your kernel citation to a commit.** The Linux driver grew from 4 to 13 panel tables between 2026-08-24 and 2026-08-30. A conclusion drawn from `master` on one date can be invalidated the next — and in this repository, one was.

---

## 5. Access traps

| Trap | Detail |
|---|---|
| **`lcddisplay.co` returns HTTP 403 to browser UAs** | The standard Chrome UA gets a 75 KB HTML block page. **`WhatsApp/2.23.20.0` succeeded** and returned the real 1.3 MB PDF. ⚠ **Still to be added** to the repo-root [`ai-crawler-site-access-table.md`](../../ai-crawler-site-access-table.md) — this pass was scoped to `components/**` and `vendors/**` and could not write there |
| **HTML served with a `.pdf` URL** | The 403 response *was* named `.pdf`. **Always validate `%PDF-` magic and size** before keeping a download |
| **No vendor portal** | Do not spend time looking for one |
| **Search engines are useless here** | §3.1 |
| **Espressif's registry API `latest` field lies** | It reported `0.1.0` as latest while `2.0.1` existed. Build URLs from the full version list |
| **Documents revise independently** | The datasheet is V0.01 (2020) while the application note is V0.03 (2021). Version numbers are per-document, not per-part |
| **`Ordering Information` is "TBD"** | §13 of the V0.01 datasheet is a placeholder. Lifecycle and part-ordering data are simply not published |

---

## 6. Part numbering

`JD` + 4 digits + variant letters + `-` + a program suffix, e.g. **`JD9365DA-H3`**:

| Segment | Meaning |
|---|---|
| `JD` | Jadard |
| `9365` | Family |
| `DA` | Die/process variant |
| `-H3` | Program / configuration suffix |

⚠ **Suffixes are not documented and must not be assumed equivalent.** Only `-H3` has a retrievable document. The suffix fitted inside a bonded COG panel module is generally **unknowable** without decapsulation — the [JD9365 record](../../components/jadard/jd9365/README.md#1-identity) records this as an open question rather than guessing.

---

## 7. Companion parts

Jadard's application notes pair the JD9365DA-H3 with **Fitipower FP7721** and **FP7723** PMICs for internal-DC/DC power modes. If you are designing around a Jadard driver, those are the reference power companions — and note that they are *Fitipower* parts, another route by which the two vendors get conflated.

---

## 8. Checklist for the next Jadard part

1. Search the **ESP-IDF component registry** for `esp_lcd_<part>` and read its README for a datasheet link (§3.1). Highest hit rate by far.
2. Search **mainline Linux** `drivers/gpu/drm/panel/` for `panel-jadard-*` or the part name. Pin to a commit.
3. Try `dl.espressif.com/AE/esp-iot-solution/<PART>*.pdf` directly.
4. Try LCD reseller and module-house sites, **with UA rotation** (§5).
5. Validate `%PDF-` magic on everything.
6. Expect the manufacturer register map to be **absent**; plan to correlate driver sources instead (§4).
7. Record failures in [`component-download-failures.txt`](../../component-download-failures.txt).

---

## 9. Sources

| Title | URL | Retrieved | Notes |
|---|---|---|---|
| JD9365DA-H3 Data Sheet V0.01 | <https://dl.espressif.com/AE/esp-iot-solution/JD9365DA-H3_DS_V0.01_20200819.pdf> | 2026-08-30 | Espressif mirror; clean fetch |
| JD9365DA-H3 Application Note V0.03 | <https://lcddisplay.co/wp-content/uploads/2023/01/JD9365DA_V0.03_20210201.pdf> | 2026-08-30 | 403 on browser UA; **WhatsApp UA worked** |
| `esp_lcd_jd9365` component | <https://components.espressif.com/components/espressif/esp_lcd_jd9365> | 2026-08-30 | The README that led to the datasheet |
| `panel-jadard-jd9365da-h3.c` | <https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/panel/panel-jadard-jd9365da-h3.c> | 2026-08-30 | 13 panel init tables |

## Related

- [Jadard JD9365 component record](../../components/jadard/jd9365/README.md) · [programming reference](../../components/jadard/jd9365/jd9365-programming-reference.md)
- [Fitipower sourcing guide](../fitipower/README.md) — the vendor JD9365 was previously misattributed to
- [Ilitek sourcing guide](../ilitek/README.md) — same technique, contrasting outcome: Ilitek **does** publish its register map
- [Espressif sourcing guide](../espressif/README.md) — whose CDN is doing the actual hosting here
- [Vendor guides index](../README.md)
