# MEMSensing — Documentation Sourcing Guide

Reusable knowledge for obtaining documentation for MEMSensing MEMS microphone and sensor parts.

> **TL;DR** — MEMSensing's own site is **Chinese-first** (`https://www.memsensing.com/`, title
> 苏州敏芯微电子技术股份有限公司, verified 2026-08-24, S1). The datasheet we hold was not obtained
> from MEMSensing at all — it came from **LCSC's datasheet mirror**:
> `https://datasheet.lcsc.com/lcsc/1811081617_MEMSensing-MSM261D4030H1CPM_C74250.pdf` (S2). For this
> class of Chinese component vendor, **the distributor is the documentation host.**

---

## 1. Who they are

MEMSensing Microsystems (Suzhou) Co., Ltd. — 苏州敏芯微电子技术股份有限公司, "MEMSensing" —
is a Chinese MEMS specialist (Shanghai STAR Market listed) making microphones, pressure sensors and
inertial sensors. Their site tagline describes an ambition to be a leading global MEMS solutions
provider (S1).

They are a genuine MEMS *manufacturer* — they run their own process — rather than a fabless
re-badger, which matters because it means the parts are real designs with real specifications, even
where the public documentation is thin.

MEMSensing is a *component* vendor; it appears only in
[`components/`](../../components/README.md).

---

## 2. Product lines

| Line | What it is | Relevance |
|---|---|---|
| **`MSM` — MEMS microphones** | Analog and **digital (PDM / I²S)**, bottom- and top-port | [MSM261D4030H1CPM](../../components/memsensing/msm261d4030h1cpm/README.md) is a digital PDM part |
| **`MPS` / pressure sensors** | Absolute and differential, barometric | Competes with [Bosch Sensortec](../bosch-sensortec/README.md) `BMP` series |
| **Inertial (accel / gyro)** | 3-axis and 6-axis IMUs | Competes with [QST](../qst/README.md) and Bosch |
| **Microphone modules / ASICs** | Packaged assemblies | |

**How they fit together for an ESP32 board:** the digital PDM microphone is the interesting one,
because the ESP32-S3 can clock a PDM mic directly from an I²S peripheral with no codec in between.
That is why a two-chip audio input path (mic → SoC) is possible at all on our board, in contrast to
the output path which needs a [dedicated DAC](../texas-instruments/README.md).

---

## 3. Market position

Low cost, high volume, Chinese domestic supply chain. MEMSensing competes with Knowles, Infineon,
Goertek and AAC in MEMS microphones. Knowles and Infineon dominate Western designs and publish
excellent datasheets; MEMSensing wins on price in Chinese consumer hardware and publishes much less.

The pattern is by now familiar across this repository's Chinese component vendors — see
[Hynitron](../hynitron/README.md) and [SGMicro](../sgmicro/README.md) — and it has a consistent
practical consequence: **the part is fine; finding out what it does is the hard part.**

---

## 4. Part numbering

```
MSM 261 D 4030 H1 CPM
│   │   │ │    │  └─ Package / port / packaging configuration code
│   │   │ │    └──── Sensitivity or performance grade index
│   │   │ └───────── Package dimensions, hundredths of a mm (4030 ≈ 4.0 × 3.0 mm)
│   │   └─────────── Output type: **D = digital (PDM)**; A = analog
│   └─────────────── Series index
└─────────────────── MSM = MEMSensing Microphone
```

**[inference]** MEMSensing publishes no numbering key we have located. This decode is reconstructed
from the one part we hold plus the general convention in the MEMS-microphone industry, where a
4-digit block encoding package size in hundredths of a millimetre is near-universal.

The one element worth trusting is **`D` for digital** — it is confirmed by the part's actual PDM
behaviour, documented in the
[MSM261D4030H1CPM record](../../components/memsensing/msm261d4030h1cpm/README.md). Treat the rest as
a working hypothesis.

---

## 5. Documentation: where it actually comes from

| Rank | Source | Pattern | Notes |
|---|---|---|---|
| 1 | **LCSC datasheet mirror** | `https://datasheet.lcsc.com/lcsc/<upload-id>_<Manufacturer>-<Part>_<LCSC-code>.pdf` (S2) | ✅ How we got ours. **The most reliable source for Chinese component datasheets generally** |
| 2 | **LCSC product page** | `https://www.lcsc.com/product-detail/<...>_C<NNNNN>.html` | The `C`-number is LCSC's stable part key — record it |
| 3 | **Board-vendor mirror** | See [Waveshare guide](../waveshare/README.md) | |
| 4 | **MEMSensing direct** | `https://www.memsensing.com/` (S1) | Chinese-first; product listings; downloads sparse or contact-gated |

### The LCSC pattern is the general lesson

The filename encodes an upload timestamp-ish ID, the manufacturer, the part number **and the LCSC
`C`-code**. That is unusually good provenance for a mirror — you can tell exactly which catalogue
entry the PDF was attached to. When documenting any Chinese component, **search LCSC by part number
first**; it will frequently succeed where the manufacturer's own site does not.

**Caveat:** LCSC mirrors are snapshots. They are not revision-tracked, may be superseded silently,
and occasionally attach the wrong document to a part. Validate that the PDF's own title block names
your part.

---

## 6. Distribution

| Channel | Availability |
|---|---|
| **LCSC** | ✅ The primary channel, and the documentation host |
| JLCPCB assembly | ✅ Stocked — which is why it lands on boards like ours |
| Taobao / AliExpress | ✅ |
| Mouser / Digi-Key | ❌ Essentially absent |

---

## 7. Gotchas

- **The manufacturer is not the documentation source.** Go to LCSC first. This inverts the habit you
  bring from [TI](../texas-instruments/README.md).
- **Chinese-first site.** English content is limited.
- **Datasheets are thin on acoustics.** Frequency-response curves, THD and directivity are often
  summarised in a single typical-value table rather than plotted. For an audio design that matters,
  and it should be recorded as a gap rather than assumed adequate.
- **PDM clock requirements are easy to get wrong.** The mic's supported clock range determines
  whether it runs in normal or low-power mode, and the two have different sensitivity. Confirm
  against the datasheet, not against example code.
- **Port orientation is a mechanical constraint, not a detail.** A bottom-port mic needs a hole in
  the PCB and an acoustic seal to the enclosure. Substituting a top-port part with the same
  electrical spec will not work.
- **`http://www.memsensing.com/` and `https://www.memsensing.com/` both appear in citations.** Prefer
  HTTPS; the HTTP form is cited in the component record from the 2026-08-21 pass.

---

## 8. Parts and devices we document

| Record | Type | Used by |
|---|---|---|
| [MSM261D4030H1CPM](../../components/memsensing/msm261d4030h1cpm/README.md) | Digital PDM MEMS microphone | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |

Related audio-path records:
[TI PCM5100A DAC](../../components/texas-instruments/pcm5100a/README.md) ·
[WCH CH445P audio mux](../../components/wch/ch445p/README.md) ·
[3.5 mm line output](../../components/generic/3.5mm-audio-output/README.md) ·
[SGMicro SGM2036-3.3](../../components/sgmicro/sgm2036-3.3/README.md) (the `3V3_DAC` rail — note the
microphone is **not** on it).

No device in this repository is manufactured by MEMSensing.

---

## 9. Sources

| ID | Title | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|
| S1 | MEMSensing corporate site | primary | https://www.memsensing.com/ | 2026-08-24 | HTTP 200; title 苏州敏芯微电子技术股份有限公司; Chinese-first; MEMS positioning |
| S2 | MSM261D4030H1CPM datasheet (LCSC mirror, LCSC code `C74250`) | primary (redistributed) | https://datasheet.lcsc.com/lcsc/1811081617_MEMSensing-MSM261D4030H1CPM_C74250.pdf | 2026-08-21 | The part's specifications; the LCSC mirror filename pattern. Cited by the [component record](../../components/memsensing/msm261d4030h1cpm/README.md) |
| S3 | LCSC catalogue | primary | https://www.lcsc.com/ | 2026-08-24 | HTTP 200 |

> **Evidence boundary.** S1 and S3 are **reachability probes performed 2026-08-24** and establish only
> that the sites respond and what language they present. S2 was retrieved 2026-08-21. §4's numbering
> decode is explicitly **[inference]** except for the `D = digital` element. §3's competitive
> positioning is general industry knowledge, **not sourced or measured here**.

---

## Related

- [Vendor guide index](../README.md)
- [MSM261D4030H1CPM](../../components/memsensing/msm261d4030h1cpm/README.md)
- [Bosch Sensortec](../bosch-sensortec/README.md) and [QST](../qst/README.md) — the sensor vendors this one competes with
- [Marketplace comparison](../../guides/markets/vendor-comparison.md) — on LCSC as a documentation source
