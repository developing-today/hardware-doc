# Pricing, availability and physical dimensions — Tanmatsu

> What it costs, what spare parts cost, and measured physical extents.
> Retrieved **2026-08-24** from [`shop.nicolaielectronics.nl`](https://shop.nicolaielectronics.nl/shop/category/tanmatsu-9).
> Prices change — every figure here is dated. **No hardware was measured physically**; dimensions come from the published CAD.

---

## 1. Device pricing

All observations **2026-08-24**, Nicolai Electronics official webshop, Netherlands.

| Product | Price shown | + 21% NL VAT |
|---|---:|---:|
| **Tanmatsu [black]** | **€99.17** | €119.99 |
| Tanmatsu [purple & black] | €99.17 | €119.99 |
| Tanmatsu [blue & black] | €99.17 | €119.99 |
| Tanmatsu [green & black] | €99.17 | €119.99 |
| Tanmatsu [white & black] | €99.17 | €119.99 |
| Tanmatsu [red & black] | €99.17 | €119.99 |
| **Tanmatsu [cyberdeck]** | €99.17 | €119.99 |

**All seven variants are the same price** — case colour and the cyberdeck front panel cost nothing extra.

€99.17 × 1.21 = **€119.99**, so the listed figure is clearly the ex-VAT price behind a €119.99 retail target.

### VAT and region

Quoted from the shop:

> *"For customers in the EU **21% Dutch VAT** will be charged. If you are located **outside of the European Union no VAT** will be charged by the webshop. If you are a business customer within the EU that wants to make use of intra-community invoicing then please provide your company VAT number during checkout."*

So: **~€120 inside the EU**, **~€99 outside** (before your own import duties, which the shop does not collect).

For context, badge.team say Nicolai Electronics offer the device *"practically at cost"* and take on the certification burden — see [`konsool-and-family.md`](konsool-and-family.md). The €99 figure is consistent with that claim, though I have not costed the BOM to verify it.

## 2. Spare parts and accessories

| Part | Price (ex VAT) | Note |
|---|---:|---|
| **Keyboard for Tanmatsu** | **€4.96** | The KeebDeck keypad — see [`keyboard.md`](keyboard.md) |
| Frontpanel for Tanmatsu | €4.13 | Decorative PCB, built on demand |
| **Display for Tanmatsu** | **€16.53** | SWI LH397K-IC01 + ST7701S |
| Protected 2500 mAh LiPo, PH2.0 | €8.22 | The stock cell |
| CATT to JTAG adapter | €3.26 | Adds LED + QWIIC beside a 10-pin JTAG header |
| CATT to SAO adapter kit | €3.26 | |
| Ziisor TX868-JZ-5 antenna (868 MHz) | €4.12 | Europe |
| Ziisor TX915-JZ-5 antenna (915 MHz) | €4.12 | US & Canada |
| Ziisor TX433-JZ-5 antenna (433 MHz) | €4.12 | For 433 MHz LoRa builds |

Two things worth noting:

- **The display is the single most expensive replaceable part** at €16.53 — about 17 % of the device price. It is also the part behind a 0.4 mm-pitch B2B connector, so treat the front panel with care.
- **A 433 MHz antenna is sold** even though badge.team say only the 868/915 MHz module variant has been offered. So either 433 MHz units exist, or the antenna is stocked for people fitting their own `E22-400M22S`.

The vendor's earlier promise that *"the keyboard and corresponding metal dome sheet will be available as a spare part once Tanmatsu starts shipping"* has been **kept** — though the listing does not say whether the €4.96 includes the mandatory dome sheet. **Ask before ordering** if you need the sheet too.

## 3. Availability

Quoted 2026-08-24:

> *"Demand for Tanmatsu is currently **a bit higher than the speed at which we can manufacture them**. Products that are out of stock can still be ordered but expect a **delay of a few weeks** on the processing of your order."*
>
> *"We are currently **only manufacturing black cases and spacers**, variants with other case colors are available **while stock lasts**."*
>
> *"**All front panel variants are available** and can be built on-demand."*

So: the device ships, but **supply is constrained**, non-black cases are being run down, and front panels are made to order. If you want a coloured case, that is the time-sensitive choice.

## 4. Physical dimensions

### Published figures

| Property | Value | Source |
|---|---|---|
| Case | **120 × 135 × 18 mm** | vendor specifications |
| Weight | **215 g** incl. case and battery | vendor specifications |
| Mainboard PCB | **not published** | — |

### Measured from the published CAD

Computed with [`tools/step_bbox.py`](tools/step_bbox.py), which reads `CARTESIAN_POINT` entities out of ISO 10303-21 STEP files — no CAD kernel required:

| Model | X | Y | Z | Points |
|---|---:|---:|---:|---:|
| `tanmatsu.step` (mainboard) | **114.90 mm** | **142.40 mm** | 27.13 mm | 131,475 |
| `frontpanel.step` | **114.90 mm** | **129.94 mm** | 1.63 mm | 45,987 |

> ⚠ **Method caveat:** this bounds *control points*. For spline surfaces the true surface can sit slightly inside the hull, and the Z extents include components on both board faces. Treat as approximate; **never** as a tolerance.

Reproduce:

```bash
python3 tools/step_bbox.py ../hardware-doc-archive/scratch/tanmatsu/sources/tanmatsu-mechanical/tanmatsu.step
```

### What the measurements show

**The boards share an X width of exactly 114.90 mm** — mainboard and front panel are the same width, inside the 120 mm case.

**The front panel is 129.94 mm in Y, the mainboard 142.40 mm.** The mainboard model extends **12.46 mm further** in +Y than the front panel and beyond the 135 mm case length. The most likely explanation is that `tanmatsu.step` includes a protruding feature — the SMA antenna connector or an antenna pigtail — rather than the PCB outline itself. **Not confirmed**; resolving it needs the model opened in CAD.

**The front panel measures 1.63 mm thick**, but its README instructs fabrication at **0.8 mm**:

> *"When manufacturing these boards select **0.8mm** board thickness, ENIG surface finish and Remove Mark."*

1.63 mm is KiCad's **default** board thickness, so the STEP was almost certainly exported without setting the intended 0.8 mm. **If you use `frontpanel.step` for case fitment you will model a panel twice as thick as the one you receive.** Recorded in [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

### The mainboard PCB size is not published anywhere

Neither vendor states the mainboard's PCB dimensions — only the **case** size (120 × 135 × 18 mm). The
~114.90 mm width measured above is, as far as I can tell, **the only dimensional figure available for
the board itself**, and it is derived rather than quoted. Added to [`README.md`](README.md) flagged as
measured, not vendor-stated.

### Keypad and stack-up

| Component | Dimensions |
|---|---|
| KeebDeck keypad | 85.80 × 48.60 mm, **2.50 mm** thick |
| Dome sheet | 86.75 mm wide (slightly **wider** than the keypad) |
| Front panel | 114.90 × 129.94 mm, **0.8 mm** as fabricated |

FreeCAD placement offsets for assembling these: mainboard **Z = −1.55 mm**, front panel **Z = +2.40 mm** — see [`mechanical-and-case.md`](mechanical-and-case.md).

## 5. Gaps

| Question | Status |
|---|---|
| Shipping cost / lead time by region | **Not researched** — requires checkout |
| Was there a launch or crowdfunding price? | **Not researched** — no historical pricing found |
| Second-hand market | **Not researched** |
| Is the €4.96 keyboard supplied with the dome sheet? | **Unclear** from the listing |
| Do 433 MHz units ship, or is the antenna sold standalone? | **Unresolved** — badge.team say only 868/915 has been offered |
| Exact case wall thickness, fastener sizes | **Locked in the FreeCAD files** — tool unavailable |
| Why `tanmatsu.step` exceeds the case length in Y | **Unresolved** — likely an antenna feature |
| Non-EU import duties | Not collected by the shop; buyer's responsibility |

Retrieval note: `shop.nicolaielectronics.nl` is server-rendered and needed no special headers. `tindie.com` returned **403** and `lectronz.com/stores/nicolai-electronics` **404** — neither is a current sales channel for this product.

## Related

- [`README.md`](README.md) — device overview
- [`mechanical-and-case.md`](mechanical-and-case.md) — case, revisions, FreeCAD workflow
- [`keyboard.md`](keyboard.md) — keypad dimensions and stack-up
- [`expansion-boards.md`](expansion-boards.md) — front-panel fabrication specs
- [`konsool-and-family.md`](konsool-and-family.md) — the "practically at cost" claim
