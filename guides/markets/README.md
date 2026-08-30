# Markets and sourcing

Where hardware comes from, what you can expect from each source, and how to work with the copies,
siblings and variants that dominate the low-cost end of the market.

These guides are about the **commercial** layer, in contrast to
[`vendors/`](../../vendors/README.md), which is about the **documentation** layer. A vendor guide
tells you how to get a datasheet out of Winbond; these tell you whether the board vendor will still
be hosting the schematic next year.

| Guide | What it covers |
|---|---|
| [**Vendor and marketplace comparison**](vendor-comparison.md) | Waveshare, Seeed Studio, M5Stack, Adafruit, SparkFun, DFRobot, LilyGO, Espressif official, AliExpress/Taobao, Amazon/eBay, Guition, HAOYU, and the component distributors (LCSC, Mouser, Digi-Key). What each actually sells (own designs vs resale vs clones), documentation quality, schematic and EDA-source availability, licensing posture, shipping origin, and **long-term file-hosting reliability** |
| [**Clones, siblings and variants**](clones-and-variants.md) | Spotting a clone from a listing photo; what actually differs (swapped GPIO, substituted display and touch controllers, different flash/PSRAM sizes, omitted regulators and discretes, re-marked parts); a five-minute triage procedure; how to trace an unlabelled board back to a documented design; and a worked example — the **Guition JC3636K518** as a sibling of the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) |

---

## Two things to know before reading either

**1. There are no prices in these documents.** None were verified in the 2026-08-24 pass, and an
invented figure is worse than none. Relative positioning claims are labelled **[INF]**. See
[vendor-comparison.md § A note on prices](vendor-comparison.md#a-note-on-prices) for the citation
format to use if you add one.

**2. We have not handled a clone board.** The identification methodology in
[clones-and-variants.md](clones-and-variants.md) is derived from documented failure modes, not from
validated practice. Its one well-evidenced section is the Guition/Waveshare comparison, which rests
on **one community author's reports** — specific and internally consistent, but not independently
verified. Each guide states this in its own evidence-boundary section.

---

## Related

- [Guides index](../README.md) · [Vendor sourcing guides](../../vendors/README.md)
- [Espressif ecosystem map](../espressif/ecosystem-and-product-lines.md)
- [Component download failures](../../component-download-failures.txt) — the log of URLs that did not resolve
- [Crawler / site-access table](../../ai-crawler-site-access-table.md)
