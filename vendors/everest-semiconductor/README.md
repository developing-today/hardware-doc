# Everest Semiconductor — Documentation Sourcing Guide

Reusable knowledge for obtaining primary documentation for **any** Everest Semiconductor audio codec.

> **TL;DR** — Everest serves datasheets from its own web root over **plain HTTP** at `http://www.everest-semi.com/pdf/<PART>%20PB.pdf`. The `PB` suffix reads as "product brief" but the file is the full datasheet. **The register map is not in it** — Everest publishes register tables only in a separate customer document, so for register-level work the authoritative public source is **driver code**, principally `espressif/esp-adf`.

Established while researching the [ES8156](../../components/everest-semiconductor/es8156/README.md) for the Nicolai Electronics Tanmatsu. Last verified **2026-08-30**.

---

## 1. Who they are

Everest Semiconductor Co., Ltd. (北京乐鑫/怡孚，Beijing) designs low-cost audio codecs, DACs and ADCs. Its parts — ES8388, ES8311, ES8156, ES7210, ES7243, ES8326 — are ubiquitous in Chinese-designed audio boards, ESP32 audio kits, single-board computers (Radxa, Orange Pi) and smart-speaker reference designs.

The commercial posture is OEM-oriented: parts are cheap, feature-rich for the price, and **under-documented in public**. Everest is a *component* vendor only; it never appears under `devices/`.

---

## 2. Where documents live

| Host | Serves | Stability |
|---|---|---|
| `http://www.everest-semi.com/pdf/<PART>%20PB.pdf` | **Datasheets.** Plain HTTP, no session, no JS | Verified working 2026-08-30 |
| `www.everest-semi.com` | Product listing | Sparse |
| `info@everest-semi.com` | The contact the datasheets themselves give for "latest datasheet" | Untested |

### 2.1 The URL pattern

```
http://www.everest-semi.com/pdf/ES8156%20PB.pdf
                                 ^^^^^^ ^^
                                 part   literal "PB", URL-encoded space
```

⚠ **Note `http://`, not `https://`.** The space before `PB` must be `%20`.

⚠ **"PB" does not mean product brief.** `ES8156 PB.pdf` is a **15-page datasheet, Revision 13.0, February 2026** — a maintained document with pinout, electricals, clock tables and the I²C protocol. Do not skip it expecting two pages of marketing.

### 2.2 Verified results (2026-08-30)

| URL | Result |
|---|---|
| `http://www.everest-semi.com/pdf/ES8156%20PB.pdf` | ✅ **HTTP 200, `%PDF`, 1 441 871 B, 15 pp, Rev 13.0** |
| `https://dl.radxa.com/rock3/docs/hw/datasheet/ES8156%20DS.pdf` | ❌ HTTP 404 (HTML) |

Radxa, Seeed and the ESP-ADF docs tree are commonly cited mirrors; the Radxa path tried was dead. **Try the manufacturer first** — unusually for a Chinese fabless vendor, it is the most reliable source here.

---

## 3. The defining trap: datasheets have no register map

This is the single most important thing to know about Everest.

The ES8156 datasheet documents:

- ✅ Pinout and pin functions
- ✅ The **I²C protocol** (address format, read/write framing, timing diagrams)
- ✅ Hardware-mode vs software-mode behaviour
- ✅ Supported MCLK/LRCK ratios and sampling frequencies
- ✅ Absolute maximum ratings and performance figures
- ❌ **No register table.** Not one register address, not one bit field.

The register map lives in a separate user guide supplied under a customer relationship. **You cannot write an Everest codec driver from the public datasheet.**

### 3.1 What to use instead

In priority order:

| Source | Covers | Licence | Notes |
|---|---|---|---|
| **`espressif/esp-adf`** `components/audio_hal/driver/es<part>/` | ES8388, ES8311, ES8156, ES7210, ES7243, ES8374, ES8323 | **ESPRESSIF MIT** | **The best public register documentation that exists.** The `.h` files carry named `#define`s for every register, grouped by function block, with comments naming the group |
| **Linux ASoC** `sound/soc/codecs/es8316.c`, `es8326.c`, `es8328.c` | Those parts | GPL-2.0 | Excellent where it covers your part; includes bit-field masks the ADF headers lack |
| `esp-idf` / `esp_codec_dev` component | Newer parts | Apache-2.0 | Handle-based API; increasingly the ESP-IDF path |
| Vendor board BSPs (Radxa, Orange Pi) | Whatever they fit | varies | Useful for init sequences |

**A worked example of what driver source gives you** — from `esp-adf`'s `es8156.h`, the register map is fully named:

```c
#define ES8156_RESET_REG00             0x00
#define ES8156_SCLK_MODE_REG02         0x02   /* bit 2 = software mode */
#define ES8156_DAC_SDP_REG11           0x11
#define ES8156_DAC_MUTE_REG13          0x13
#define ES8156_VOLUME_CONTROL_REG14    0x14
#define ES8156_CHIPID1_REGFD           0xFD
```

and the volume *scale* comes from the driver's volume descriptor (`max_dac_volume`, `min_dac_volume`, `volume_accuracy`, `zero_volume_reg`) rather than from any document.

**What driver source does *not* give you:** bit-level field definitions inside each register, and the expected chip-ID values. ADF's ES8156 driver defines `CHIPID1_REGFD`/`CHIPID0_REGFE` but never reads them, so **there is no public way to positively identify an ES8156 on a bus**. Record such gaps explicitly rather than guessing.

> **Documentation practice:** when reconstructing a register map from driver source, label every value as driver-derived, not datasheet-derived. The [ES8156 record](../../components/everest-semiconductor/es8156/README.md) §4 does this with an explicit `[ADF]` tag on every row. Do not let a reconstruction acquire the authority of a primary document.

---

## 4. Recurring behavioural traps across Everest parts

**Hardware mode is the power-on default.** Several Everest parts (ES8156 confirmed; check per-part) boot into a pin-configured "hardware mode" and require a register write to enter software/I²C mode — for the ES8156, **bit 2 of register `0x02`**. Until that write lands, the part *works* but ignores most configuration. The symptom is "audio plays, but volume/EQ/mute do nothing", and it is easy to misdiagnose as an I²C problem.

**Addresses are quoted inconsistently.** Everest datasheets give the **7-bit** address as a bit pattern with a pin-selected LSB (`0001 00x` for the ES8156 ⇒ `0x08`/`0x09`). ESP-ADF drivers use the **8-bit** form (`0x10`). Both are correct. Always state which convention you mean.

**Features gate on mode.** The ES8156's capless-headphone `HPCOM` pin is documented as *"Only available in software mode"*. Expect similar mode-gated features elsewhere.

**Pop suppression is implemented in software, not by a bit.** Everest drivers ramp digital volume to zero before analog shutdown and restore it last on power-up, often with multi-stage writes to the analog control registers. Collapsing or reordering those sequences reintroduces audible pops. Preserve them verbatim.

---

## 5. Document-class checklist

For any Everest part:

- [ ] **Datasheet** — `http://www.everest-semi.com/pdf/<PART>%20PB.pdf`. Record the revision from page 2 (they are revised often; the ES8156 is at **Revision 13.0**)
- [ ] **Register map** — assume *not* public. Go to `esp-adf`, then Linux ASoC
- [ ] **Init sequences** — from driver source; note the power-up/power-down ordering
- [ ] **Volume/gain scale** — usually only expressible from a driver's volume descriptor
- [ ] **Chip-ID values** — frequently undocumented; check whether *any* driver reads them
- [ ] Board BSPs from Radxa / Orange Pi / Espressif audio kits for worked integrations

---

## 6. Working command example

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
PART=ES8156
curl -sSL --max-time 90 -A "$UA" -o "$PART.pdf" \
  "http://www.everest-semi.com/pdf/${PART}%20PB.pdf"
head -c4 "$PART.pdf"   # must be %PDF
```

Plain HTTP, no referer, no cookie. A bare `curl` User-Agent was not tested, so whether the UA matters here is unknown.

---

## 7. Rights and licensing observations

Every page of the ES8156 datasheet is stamped **"Everest Semiconductor Confidential"**, yet the file is served without authentication from the manufacturer's own public web root and carries **no explicit redistribution clause**. That combination is common with this vendor.

Treat Everest datasheets as **`redistribution: unknown`**, disposition `repository (unstaged)`, flagged for user review. The *driver* sources used to reconstruct register maps are separately and clearly licensed (ESPRESSIF MIT for esp-adf, GPL-2.0 for Linux ASoC) — attribute them correctly and do not let the codec's documentation ambiguity contaminate the licence status of the code.

---

## Products documented in this repository

| Part | Record | Datasheet | Register map source |
|---|---|---|---|
| **ES8156** | [`components/everest-semiconductor/es8156/`](../../components/everest-semiconductor/es8156/README.md) | ✅ Rev 13.0, Feb 2026 | **Reconstructed from `esp-adf` v2.7** |

## Related pages

- [`vendors/texas-instruments/README.md`](../texas-instruments/README.md) — the opposite posture: complete public register maps at guessable URLs
- [`vendors/omnivision/README.md`](../omnivision/README.md) — another vendor whose register-level truth lives in driver code
- [`vendors/sitronix/README.md`](../sitronix/README.md) — a third instance of the same pattern
- [`component-download-failures.txt`](../../component-download-failures.txt)
