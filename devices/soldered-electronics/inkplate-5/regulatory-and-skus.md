# Inkplate 5 / Gen 2 — regulatory, SKUs and product identity

> Facts extracted from the compliance PDFs Soldered ships inside their hardware repositories — data that appears nowhere on the product pages.
> Snapshot **2026-08-24**. Sources: `OUTPUTS/Compliance/` in both hardware repos.

Soldered including CE/UKCA declarations and multilingual safety sheets in a public Git repository is unusual and genuinely useful. It gives you the manufacturer of record, the exact standards tested against, dates of issue, SKUs, EAN barcodes and the HS tariff code — everything you need to integrate an Inkplate into a product you intend to sell, or to import one.

## Product identity

| | **Inkplate 5** | **Inkplate 5 Gen 2** |
|---|---|---|
| Full product name | `Soldered Inkplate 5` | `Soldered Inkplate 5 Gen2` |
| **SKUs** | **333255, 333256, 333257, 333258** | **333333, 333334, 333335, 333336** |
| **EAN/UPC** | 732388677702, 732388677603, 732388677504, 732388677405 | 732388656707, 732388656608, 732388656509, 732388656400 |
| **HS tariff code** | **8531204090** | **8531204090** |
| Country of origin | **Croatia** | **Croatia** |
| Product type (declared) | E-paper display board | E-paper display board |

**Each generation has four SKUs.** What distinguishes them is *not stated* in any file in either repository — most likely enclosure/accessory bundles (Soldered sells Inkplates bare, with a case, and in kit form), but this is **inference**. If you are ordering, confirm which SKU corresponds to which bundle.

Note EAN codes descend rather than ascend alongside the SKUs, so do not assume SKU *n* maps to EAN *n* by position.

**HS 8531204090** — "indicator panels incorporating LCD or LED" — is the code customs will expect. Both generations share it, and both declare **Croatia** as country of origin, which matters for EU-internal shipping and for post-Brexit UK import.

## Declarations of conformity

Both generations hold **EU (CE)** and **UK (UKCA)** declarations, signed by **David Zovko, Board member**.

| | Inkplate 5 | Inkplate 5 Gen 2 |
|---|---|---|
| **Date of issue** | **12 August 2022** | **15 January 2025** |
| Registered address | Reisnerova ulica 100, 31000 Osijek | **Vinkovačka cesta 68, 31000 Osijek** |
| Standards contact | `standards@soldered.com` | `standards@soldered.com` |

### ⚠ Two discrepancies worth noting

**1. Soldered moved.** The Inkplate 5 declaration gives *Reisnerova ulica 100*; the Gen 2 declaration gives *Vinkovačka cesta 68*. Both Osijek. If you are citing Soldered's registered address, use the **newer** one — the 2022 document is stale.

**2. The Inkplate 5's declaration predates its published hardware revision.** The CE/UKCA declarations are dated **August 2022**, but the hardware repository publishes design revision **V1.2.0** committed **2024-10-20**. A declaration of conformity is meant to cover the product as placed on the market; a two-year-old declaration against a later board revision is at minimum an unanswered question.

Possible readings: V1.2.0 changes were judged not to affect conformity (common and legitimate for non-RF changes); or the declaration simply was not re-issued. **Not resolvable from the documents.** If conformity matters to your application, ask Soldered directly at `standards@soldered.com` before relying on it.

## Standards tested against

Identical for both generations — only the EU/UK prefixes differ (`EN`/`LVS EN` vs `BS EN`).

| Domain | Directive / Regulation | Standards |
|---|---|---|
| **EMC** | EMC Directive **2014/30/EU** · UK EMC Regulations 2016 | `EN 55032:2015+AC:2017+A11:2020+A1:2021`<br>`EN 55035:2017+AC:2020` |
| **RoHS** | **(EU) 2015/863** amending Annex II to **2011/65/EU** · UK RoHS Regs 2012 | `EN 63000:2018` |
| **Radio** | RED **2014/53/EU** · UK Radio Equipment Regs 2017 | `EN 300 328 V2.2.2`<br>`ETSI EN 301 489-1 V2.2.3`<br>`ETSI EN 301 489-17 V3.2.4` |

`EN 300 328` is the harmonised standard for **2.4 GHz wideband transmission** — it covers the ESP32's Wi-Fi and Bluetooth. `EN 301 489-17` is the EMC standard specifically for broadband data transmission systems. So the radio is properly assessed, not merely declared.

**These are self-declarations**, as RED permits for equipment using harmonised standards. No notified body number appears on either document.

## Safety sheet — the constraints that matter

From `Inkplate 5 Safety sheet EN.pdf` (also supplied in German). Condensed, with the engineering-relevant points first:

- **"There is a danger of explosion if the battery is incorrectly placed."** — Li-ion polarity warning. The Inkplate has a JST battery input with no reverse-polarity protection called out.
- **"Connection of other devices may affect compliance or result in damage to the unit, and invalidate the warranty."** — attaching peripherals to the broken-out headers can void the CE/UKCA declaration for your assembly. Relevant if you are building a product around it.
- **"Where peripherals are connected that do not include the cable or connector, the cable or connector used must offer adequate insulation…"**
- **"Should not be covered and should be operated in a well ventilated environment."**
- **"Should be placed on a stable, flat, non-conductive surface and should not be contacted by conductive items."**
- **"The product is intended to be used inside"**, at normal ambient room temperature — **indoor use only**, no outdoor rating.
- Do not expose to water or moisture; do not handle with wet hands.
- **"Should not be used outside of its specified working range."**

The compliance-invalidation clause is the one people miss: an Inkplate inside your enclosure driving your peripherals is **your** product for conformity purposes, and Soldered's declaration does not transfer to it.

## Practical notes

- **Both generations are RED-assessed radio equipment**, so the ESP32's Wi-Fi/BLE can be used in the EU/UK as sold. Contrast with [ZeroWriter Ink](../../zerowriter/zerowriter-ink/README.md), which ships wireless disabled explicitly to avoid certification cost — even though its main board is an Inkplate 5 Gen 2 respin whose *stock* form is already certified. Respinning the board (new charger, relocated USB) means the original declaration would not automatically apply.
- **No FCC declaration is present** in either repository. Only EU and UK. For US deployment you are on your own, though the ESP32-WROVER module itself carries an FCC ID that may be usable under modular approval.
- The safety sheets ship in **English and German only**.

## Files

```
inkplate-5/artifacts/hardware/…/OUTPUTS/Compliance/
├── Info.txt                       SKUs, EAN, HS code, origin
├── Inkplate 5 CE.pdf              EU DoC, 2022-08-12
├── Inkplate 5 UKCA.pdf            UK DoC, 2022-08-12
├── Inkplate 5 Safety sheet EN.pdf
└── Inkplate 5 Safety sheet DE.pdf

inkplate-5-gen2/artifacts/hardware/…/OUTPUTS/Compliance/
├── Info.txt                       SKUs, EAN, HS code, origin
├── CE.pdf                         EU DoC, 2025-01-15
├── UKCA.pdf                       UK DoC, 2025-01-15
├── Safety Instructions EN.pdf
└── Safety Instructions DE.pdf
```

## Related

- [`README.md`](README.md) — device record
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
- [Soldered vendor guide](../../../vendors/soldered-electronics/README.md)
