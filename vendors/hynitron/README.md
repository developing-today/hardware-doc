# Hynitron — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation for Hynitron touch-controller ICs. This is the
**worst-documented vendor** in this repository, and the guide is mostly about how to work around that.

> **TL;DR** — Hynitron's own site is **HTTP-only, Chinese-only, and serves no public datasheets**
> (`http://www.hynitron.com/`, title 上海海栎创科技股份有限公司; **HTTPS does not connect**, verified
> 2026-08-24, S1/S2). The CST816D datasheet we hold came from **Waveshare's mirror**:
> `https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf` (S3). Board-vendor mirrors
> and driver source are the practical sources.

---

## 1. Who they are

Shanghai Hynitron Technology Co., Ltd. (上海海栎创科技股份有限公司) is a Chinese fabless designer of
touch controllers, fingerprint ICs and audio amplifier ICs. Their `CST` touch-controller family is
extremely common in low-cost Chinese display modules — particularly the small round and square
capacitive panels used on ESP32 smart-knob and smartwatch-style boards.

Like [Sitronix](../sitronix/README.md), Hynitron sells **to module houses, not to you.** The
controller arrives already bonded into a panel assembly.

---

## 2. Product lines

| Line | What it is | Notes |
|---|---|---|
| **`CST8xx` — capacitive touch controllers** | `CST816`, `CST816S`, `CST816D`, `CST816T`, `CST820`, `CST826` | **The line that matters here.** Single-point (some multi-point), I²C, small panels |
| **`CST1xx` / `CST2xx`** | Larger-panel multi-touch controllers | Competes with Goodix `GT911` |
| **`CSA` / `CST9xx` — fingerprint** | Capacitive fingerprint sensing | |
| **Audio amplifier ICs** | Class-D / smart PA | Listed on their site's keywords (S1) |

**How the `CST816` family fits together** is the single most confusing thing about this vendor, and
the [CST816D record](../../components/hynitron/cst816d/README.md) exists largely to untangle it. The
`S`, `D` and `T` suffixes are **different dies with overlapping but not identical register maps and
different gesture support** — not packaging variants. Community driver code
(`esp_lcd_touch_cst816s`, `SensorLib`) frequently treats them as one part, which works until it
doesn't.

---

## 3. Market position

Cheap, high-volume, invisible. Hynitron competes with Goodix, [Sitronix](../sitronix/README.md)'s
`ST16xx`, FocalTech (`FT6236`) and Chipsemi (`CHSC5816`) in the small-panel capacitive touch market.
They win on unit cost in the Chinese module supply chain.

The documentation posture follows directly from the business model: their customers are module houses
under NDA who get a full register manual and an integration engineer. A hobbyist reading a schematic
is not a customer, and is served accordingly.

---

## 4. Part numbering

```
CST 816 D
│   │   └─ Die/feature variant — S, D, T. NOT a package code. Registers differ.
│   └───── Family: 8xx = small-panel capacitive touch
└───────── Hynitron "Capacitive Sensing Touch" prefix
```

**[inference]** No Hynitron numbering document is public. This decode comes from the parts observed
in the wild and from the register differences documented in the
[CST816D record](../../components/hynitron/cst816d/README.md).

The practical rule: **treat `CST816S`, `CST816D` and `CST816T` as three parts.** Confirm which one you
have by reading the chip-ID register, not by trusting a schematic label — board schematics in this
market are frequently copy-pasted from a reference design and name the wrong suffix.

---

## 5. Documentation: where it actually comes from

Ordered by likelihood of success.

| Rank | Source | Pattern | Notes |
|---|---|---|---|
| 1 | **Board-vendor mirror** | `https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf` (S3) | ✅ How we got ours. English, V1.3. Also mirrored per-product: `.../wiki/<Product>/CST816D_datasheet_En_V1.3.pdf` |
| 2 | **Driver source** | `https://components.espressif.com/components/espressif/esp_lcd_touch_cst816s` · [`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) | Often the only description of registers the datasheet omits |
| 3 | **Module-house documentation** | Varies | Whoever bonded the panel |
| 4 | **Hynitron direct** | `http://www.hynitron.com/` (S1) | Chinese-only, HTTP-only, product listings; **no downloadable datasheets found** |

### We hold a Hynitron vendor-level document

Filed at the **vendor** level rather than under a part, because it covers the family rather than one die:

| Document | Local path | Bytes |
|---|---|---|
| **Hynitron touch-driver porting guide, V3.5, 2022-07-01** (Chinese) | [`artifacts/hynitron-touch-driver-porting-guide-v3.5-20220701-zh.pdf`](artifacts/hynitron-touch-driver-porting-guide-v3.5-20220701-zh.pdf) | 660,817 |

**This partially closes the register-map gap below** — a *porting guide* is written for exactly the
integrator audience that the datasheet neglects, and is the best Hynitron-authored description of
driver behaviour we hold. It is **in Chinese** and **V3.5-era**, so it may not match current silicon.

**Provenance:** it shipped inside `SensorLib/datasheet/` in the vendored
[`lewisxhe/SensorLib`](https://github.com/lewisxhe/SensorLib) copy in the Waveshare demo archive —
**not** downloaded from Hynitron. See
[vendored-deps § Datasheet disposition](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/vendored-deps/README.md#datasheet-disposition).
This is a second, independent demonstration of §5's thesis: **the vendor was not the source.**

### The register-map gap

This is the defining Hynitron gotcha and deserves its own note. The public `CST816D` datasheet is
**thin**: it covers I²C addressing, the basic coordinate registers and gesture codes, but community
drivers use registers that appear in **no public document** — auto-sleep configuration, chip-ID
readback, interrupt-mode selection. Those were derived from vendor sample code and from experiment.

Where this repository states such a register, it is sourced to the **driver** and marked as such.
Do not upgrade a driver-derived register to "datasheet-confirmed" without the datasheet in hand.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| Mouser / Digi-Key | ❌ None |
| LCSC | ⚠️ Occasionally, as bare COG die/COF — not a normal purchase |
| **Panel module houses** | ✅ The real channel, pre-bonded |
| AliExpress / Taobao | ✅ As finished touch panel modules |

You cannot meaningfully "buy a CST816D". You buy a panel and inherit one.

---

## 7. Gotchas

- **No HTTPS.** `https://www.hynitron.com/` and `https://hynitron.com/` both **fail to connect**
  (curl exit, no HTTP status); `http://www.hynitron.com/` returns 200 (S1, S2). Any tooling that
  upgrades HTTP to HTTPS will report the site as dead when it is not.
- **Chinese-only site.** No English mirror found.
- **No public register manual** — though the **V3.5 porting guide we hold** (§5) covers some of the
  same ground. Note it is Chinese-only and was obtained from a third-party bundle, not from Hynitron.
- **Suffix variants are different parts.** See §4.
- **Community drivers are named for `CST816S` but used for everything.** `esp_lcd_touch_cst816s`
  drives `CST816D` panels in practice. That it works is an empirical fact about specific panels, not
  a compatibility guarantee.
- **The I²C address is `0x15` for our part** — but the family is not consistent across variants, and
  the address collides with nothing on our board only by luck. Compare against the
  [DRV2605L at `0x5A`](../../components/texas-instruments/drv2605l/README.md) sharing the same bus.
- **Competing controllers use different maps entirely.** The
  [CST816D record](../../components/hynitron/cst816d/README.md) tabulates Goodix `GT911`
  (address `0x5D`/`0x14`, 5-point) and Chipsemi `CHSC5816` as **not** drop-in compatible. If a clone
  board substituted the touch IC, nothing will work — see
  [clones-and-variants.md](../../guides/markets/clones-and-variants.md).

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [CST816D / CST816 family](../../components/hynitron/cst816d/README.md) | Capacitive touch controller, I²C `0x15` | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |

Related non-Hynitron records for the same physical assembly:
[LCD panel module](../../components/generic/lcd-panel-module/README.md) ·
[ST77916 display controller](../../components/sitronix/st77916/README.md).

No device in this repository is manufactured by Hynitron.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | Hynitron corporate site | primary | http://www.hynitron.com/ | 2026-08-24 | HTTP 200; title 上海海栎创科技股份有限公司; Chinese-only; keywords list touch/fingerprint/audio-amplifier lines |
| S2 | Negative probe — HTTPS | probe | https://www.hynitron.com/ and https://hynitron.com/ | 2026-08-24 | **Connection failure (no HTTP status)** — the site is HTTP-only |
| S3 | CST816D datasheet English V1.3 | primary (redistributed) | https://files.waveshare.com/wiki/common/CST816D_datasheet_En_V1.3.pdf | 2026-08-21 | The register content we hold; **and** that a board vendor, not Hynitron, is the practical host |
| S4 | `esp_lcd_touch_cst816s` | primary | https://components.espressif.com/components/espressif/esp_lcd_touch_cst816s | 2026-08-21 | Driver-derived register behaviour per §5 |
| S5 | `lewisxhe/SensorLib` | secondary | https://github.com/lewisxhe/SensorLib | 2026-08-21 | Cross-controller comparison table cited in §7; **and the bundle that supplied both S3 and S6** |
| S6 | Hynitron touch-driver porting guide V3.5 (Chinese) | primary (redistributed) | bundled in SensorLib; local copy at [`artifacts/`](artifacts/hynitron-touch-driver-porting-guide-v3.5-20220701-zh.pdf) | 2026-08-23 | Vendor-authored driver-integration guidance — see §5 |

> **Evidence boundary.** S1 and S2 are **reachability probes performed 2026-08-24**. The claim that
> Hynitron publishes no downloadable datasheets is a **negative result from our search**, not proof of
> absence — we did not read the full Chinese site tree, and a login-gated or partner-portal
> distribution may well exist. §4 is marked **[inference]**.

---

## Related

- [Vendor guide index](../README.md)
- [Sitronix](../sitronix/README.md) — the display controller in the same bonded module, with the same documentation posture
- [Waveshare](../waveshare/README.md) — the mirror that actually served us the datasheet
- [Clones and variants](../../guides/markets/clones-and-variants.md)
