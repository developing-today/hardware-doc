# Waveshare ESP32-S3-ePaper-3.97

> ESP32-S3 e-paper development board, 3.97 inch, 800 × 480, 4-level greyscale.
> Research snapshot **2026-09-01**. No hardware in hand — every claim here is
> `reported-working` (vendor-stated) or `inferred`. Nothing is `executed-success`.

This record exists to back a recommendation. The
[M5Stack PaperMono](../../m5stack/papermono/README.md) record advised readers who
want a general e-paper development board with expansion to "prefer Inkplate or a
Waveshare ESP32 e-paper board" — but every Waveshare record in this knowledge
base was an **LCD** board, so the second half of that advice was unsupported.
That was tracked as conflict **C24**. This record closes it.

---

> ## ⚠ Second pass, 2026-09-01 — read this before the sections below
>
> This record was **written twice on the same day by two concurrent sessions**. The
> first pass concluded that Waveshare publishes no documentation, no schematic, no
> sample code, no price and no panel controller for this board. **All of those
> absences are false**, and the sections below have been corrected in place.
>
> **Root cause:** the first pass tested the *legacy* wiki (`waveshare.com/wiki/…`),
> got a 404, and read that as product-level absence. Waveshare migrated this product
> to a newer platform — **`docs.waveshare.com/ESP32-S3-ePaper-3.97`, HTTP 200** —
> which this repository's own
> [Waveshare sourcing guide §8.2](../../../vendors/waveshare/README.md) already says
> to *"Check … first"*. A 404 on a deprecated host is evidence about that host.
>
> **What actually exists**, all retrieved 2026-09-01 and hashed:
>
> | First pass said | Actually |
> |---|---|
> | No documentation | [`docs.waveshare.com/ESP32-S3-ePaper-3.97`](https://docs.waveshare.com/ESP32-S3-ePaper-3.97) + a `Resources-And-Documents` page |
> | No schematic | **Retained** — [`artifacts/schematic/`](artifacts/schematic/ESP32-S3_e-Paper-3.97-schematic.pdf), 257 550 B, `b1203145…` |
> | No pinout | **Recovered from that schematic** — [`pinouts-and-buses.md`](pinouts-and-buses.md) |
> | No sample code | [`waveshareteam/ESP32-S3-ePaper-3.97`](https://github.com/waveshareteam/ESP32-S3-ePaper-3.97) @ `9b12d40` — 14 examples + factory firmware |
> | No price | **USD 34.99 – 47.99**, three SKUs |
> | No panel controller | **[SSD1677](../../../components/solomon-systech/ssd1677/README.md)** — stated in the panel manual |
> | Nothing downloaded | **Six PDFs retained and hashed**; see [Artifacts](#artifacts) |
>
> Two substantive corrections follow from the new evidence, and both matter:
>
> 1. **The PMIC is an [X-Powers AXP2101](../../../components/x-powers/axp2101/README.md), not the "TG28" the vendor's marketing names** — established from the schematic *and* Waveshare's own firmware. [C-WS2](gaps-and-conflicts.md#c-ws2--tg28-versus-axp2101)
> 2. **This board has no expansion header of any kind** — so the very recommendation that sent us here is, for this board, *refuted*. [C-WS1](gaps-and-conflicts.md#c-ws1--the-expansion-claim-is-backwards)
>
> The original claims are preserved as history in
> [C-WS10](gaps-and-conflicts.md#c-ws10--first-pass-recorded-absences-that-are-not-real)
> rather than deleted.

---

## Why this board specifically

Waveshare currently sells seven ESP32 e-paper products (see
[Sibling products](#sibling-products)). This one was chosen because it is the
closest like-for-like comparison to the PaperMono that exists:

| | Waveshare ESP32-S3-ePaper-3.97 | [M5Stack PaperMono](../../m5stack/papermono/README.md) |
|---|---|---|
| SoC | ESP32-S3R8 | ESP32-S3R8 |
| PSRAM / Flash | 8 MB / 16 MB | 8 MB / 16 MB |
| Panel | 3.97", 800 × 480, 4 grey | 3.97", 480 × 800, 4 grey |
| **Active area** | **86.40 × 51.84 mm** | **51.84 × 86.40 mm** |

Same SoC, same memory configuration, same panel size, same greyscale depth —
and the active area matches **to 0.01 mm**, transposed. See
[Are these the same panel?](#are-these-the-same-panel) below.

## Identity

| Field | Value |
|---|---|
| Name | ESP32-S3-ePaper-3.97 |
| Manufacturer | Waveshare Electronics (Shenzhen) |
| Store page | `https://www.waveshare.com/esp32-s3-epaper-3.97.htm` (retrieved 2026-09-01, HTTP 200) |
| **Documentation** | **`https://docs.waveshare.com/ESP32-S3-ePaper-3.97`** — HTTP 200. *Corrected 2026-09-01: the legacy `/wiki/` route 404s because the product lives on the newer platform, not because documentation is absent* |
| **Official source** | **`https://github.com/waveshareteam/ESP32-S3-ePaper-3.97`** @ `9b12d40731a80213b927ee8a421cae4082952819` (2026-03-20). No `LICENSE` file — licence **`unknown`** |
| **SKUs** | **33552** (with Li battery) · **33810** (`-EN`, without battery) · **33811** (`-Kit`: battery + 16 GB TF card + card reader + USB cable). All three flagged `unsaleable: false` on 2026-09-01 |
| **Price** | **USD 34.99 – 47.99**, observed **2026-09-01**, waveshare.com, **US region**, single unit, before shipping and duty. *Corrected — the first pass recorded this as unobtainable; the markup uses the JSON key `"sku "` with a trailing space, which a search for `"sku"` misses* |
| Bundled with every SKU | An **8 Ω 1 W speaker** |

## Key specifications

All from the vendor storefront, retrieved 2026-09-01. Evidence status
`reported-working` — these are vendor claims, not measurements.

| Specification | Value | Component record |
|---|---|---|
| SoC | ESP32-S3R8, Xtensa LX7 dual-core, up to 240 MHz — fitted as an **`ESP32-S3-WROOM-1-N16R8` module** *(module part number from the schematic)* | [esp32-s3r8](../../../components/espressif/esp32-s3r8/README.md) |
| Memory | 512 KB SRAM, 384 KB ROM, 8 MB **octal** PSRAM, 16 MB external flash. *The storefront's "What's On Board" block swaps these two — [C-WS3](gaps-and-conflicts.md#c-ws3--the-storefront-swaps-flash-and-psram)* | — |
| Wireless | 2.4 GHz Wi-Fi 802.11 b/g/n, Bluetooth 5 LE, onboard antenna | — |
| Display | 3.97" e-paper, 800 × 480, black/white, **4 greyscale**, driven by an **SSD1677** | **[3.97inch e-Paper panel](../../../components/waveshare/3.97inch-e-paper/README.md)** · [SSD1677](../../../components/solomon-systech/ssd1677/README.md) |
| Active area | 86.40 × 51.84 mm; pixel pitch 0.108 mm; **DPI 235** | — |
| Viewing angle | > 170° | — |
| Refresh — full | 3.5 s | — |
| Refresh — fast | 2.8 s | — |
| Refresh — partial | 0.6 s *(the panel manual says 0.3 s at 23 °C — [C-WS6](gaps-and-conflicts.md#c-ws6--refresh-times-disagree-between-module-and-panel-documents))* | — |
| Refresh — 4-greyscale | 3.5 s *(panel manual: 3 s at 23 °C)* | — |
| Refresh power | < 40 mW *(panel manual: 36 mW typical at 3.0 V; 0.003 mW deep sleep; 120 mA peak)* | — |
| Operating temperature | **0 to +50 °C** *(panel manual — the vendor's board pages state none)* | — |
| IMU | QMI8658A 6-axis (3-axis accel + 3-axis gyro), `INT1` GPIO39, `INT2` GPIO40 | [qmi8658a](../../../components/qst/qmi8658a/README.md) |
| RTC | PCF85063**ATL**, interrupt on GPIO45, with a dedicated backup-cell header | [pcf85063a](../../../components/nxp/pcf85063a/README.md) |
| Environment | SHTC3 temperature and humidity, I²C `0x70` | [shtc3](../../../components/sensirion/shtc3/README.md) |
| **Power management** | **X-Powers AXP2101** at I²C `0x34` — charger, multi-rail regulator, power-key controller, backup-cell charger. **Waveshare's marketing calls this "TG28"; the schematic and the vendor's own firmware both say AXP2101 — [C-WS2](gaps-and-conflicts.md#c-ws2--tg28-versus-axp2101)** | **[axp2101](../../../components/x-powers/axp2101/README.md)** |
| Battery | 3.7 V Li-ion on **PH1.25/MX1.25 header `H3`**; charge 200 mA CC to 4.2 V *(firmware default)*. Separate **RTC backup-cell header `H4`**, actively charged at 3.0 V | — |
| Audio — codec | **ES8311** mono codec, I²S on GPIO13/14/21/47/48 | [es8311](../../../components/everest-semiconductor/es8311/README.md) |
| Audio — amplifier | **NS4150B** class-D, gated by GPIO39, out to speaker header `H2` | [ns4150b](../../../components/nsiway/ns4150b/README.md) |
| Audio — input | Onboard microphone, differential `MIC_P`/`MIC_N` to the codec | — |
| Storage | microSD (TF) slot, socket `TF-07F`, FAT32. **Net names are SPI-style — [C-WS5](gaps-and-conflicts.md#c-ws5--sd-card-spi-names-but-4-bit-nets)** | [micro-sd-sdmmc](../../../components/generic/micro-sd-sdmmc/README.md) |
| Input | Programmable PWR *(an AXP2101 input, not a GPIO)* and BOOT side buttons; **3-way rotary navigation switch** on GPIO4/5/6 | — |
| USB | Type-C, receptacle `H1`, **native ESP32-S3 USB on GPIO19/20 — no USB-UART bridge fitted** | [usb-c-interface](../../../components/generic/usb-c-interface/README.md) |
| **Expansion** | **None.** No 2.54 mm header, no Qwiic/easyC, no broken-out GPIO — [C-WS1](gaps-and-conflicts.md#c-ws1--the-expansion-claim-is-backwards) | — |
| Operating voltage | 3.3 V | — |

The QMI8658A, PCF85063A and SSD1677 already had records in this knowledge base from
other boards, and were **reused rather than duplicated** — which is itself a small
signal about how conventional Waveshare's part selection is. Four records were added
by the second pass because the parts were newly evidenced *and* their datasheets were
obtained: [AXP2101](../../../components/x-powers/axp2101/README.md),
[ES8311](../../../components/everest-semiconductor/es8311/README.md),
[SHTC3](../../../components/sensirion/shtc3/README.md) and the
[3.97inch e-Paper panel](../../../components/waveshare/3.97inch-e-paper/README.md);
plus [NS4150B](../../../components/nsiway/ns4150b/README.md) as identity-only, and a
stub for [QMI8658A](../../../components/qst/qmi8658a/README.md), whose datasheet had
been sitting here since 2026-08-23 with no record beside it.

**What the vendor's specification table still does not say**, after the second pass:
there is **no battery capacity**, **no board-level power consumption in any state**,
**no board dimensions** and **no enclosure**. The operating-temperature range above
comes from the *panel* manual, not from any board page. This is a bare development
board, not a finished product — and unlike the PaperMono it is not sold as one.

## Full technical detail

The second pass produced primary-evidence documents that are too long for this page:

| Document | What is in it |
|---|---|
| **[Pinouts and buses](pinouts-and-buses.md)** | The **complete GPIO allocation table** recovered from the schematic and cross-checked against the vendor's driver, the four-device I²C bus, power domains and charge settings, the connector census, and the pin conflicts |
| **[Development, examples and firmware](development.md)** | The 14 vendor examples, the AXP2101 driver audit, factory-firmware images and offsets, the xiaozhi AI-voice firmware, and licence status |
| **[Conflicts and gaps](gaps-and-conflicts.md)** | Eleven conflicts and six gaps, including the TG28/AXP2101 identity, the expansion refutation and the panel-identity question |
| **[Sources](sources.md)** | Twenty sources with class, retrieval date, version and local path; plus every failed retrieval |
| **[Commands](commands.md)** | Every command that produced a fact here, including the PDF-extraction route that made the schematic readable |
| **[Acquisition manifest](acquisition/manifest.json)** | Fifteen artifact records with hashes, sizes, licences and dispositions |

## Are these the same panel?

The PaperMono's panel is a **DKE `DEPG0397BBS770F3`** with an active area of
**51.84 × 86.40 mm**, 480 × 800, 4-level greyscale, driven by an SSD1677
([component record](../../../components/dke/depg0397bbs770f3/README.md)).

Waveshare states **86.40 × 51.84 mm**, 800 × 480, 4-level greyscale.

Those are the same numbers transposed — portrait versus landscape convention.
Combined with identical resolution and greyscale depth, the most likely
explanation is that **both boards use the same 3.97" panel, or two panels built
to the same specification**, which would be unsurprising: DKE sells to board
vendors, and 3.97" is an unusual size.

**This is `inferred`, not established — but the second pass strengthened it
considerably.** The panel manual (Rev 1.0, 2025-04-24) states the controller
outright: **`4-2: Driver IC: SSD1677`** — the *same controller as the PaperMono's
panel* — and gives **DPI 235**, which the DKE panel also reports. So the match is now
four-way: active area to 0.01 mm, resolution, DPI, and controller.

What is *still* missing is the one thing that would settle it: **Waveshare publishes
no panel supplier or part number** — not on the storefront, not in the docs, not in
the manual, and not on the schematic's text layer, where the panel appears only as
FPC connector `J2`. A teardown photograph of the FPC marking on either board would
close it in seconds.

Recorded as an open question rather than asserted:
[C-WS8](gaps-and-conflicts.md#c-ws8--is-this-the-same-panel-as-the-papermonos), with
the panel documented in its own right at
[`components/waveshare/3.97inch-e-paper`](../../../components/waveshare/3.97inch-e-paper/README.md).

One place the two panel documents **actively disagree**: Waveshare's manual says
*"800 gate × 480 source"*, while the DKE record derives the opposite from SSD1677
register values. Low practical impact, but unresolved —
[C-WS7](gaps-and-conflicts.md#c-ws7--gate-versus-source-orientation).

If it is the same panel, the PaperMono's panel findings transfer — in particular
the DC-balance hazard, the "roughly one full refresh per ten partial refreshes"
guidance, and the manual's `2Grey Level` versus marketed 4-grey contradiction.

## Refresh performance compared

This is the one place where both vendors publish numbers for the same panel
size, so it is worth putting side by side — with the caveat that **neither set
was independently measured** and the two are not necessarily measured the same
way.

| Mode | Waveshare (vendor) | PaperMono (vendor, via M5GFX) |
|---|---|---|
| Full / quality | 3.5 s | 4.71 s (`epd_quality`) |
| Fast | 2.8 s | 0.34 s (`epd_fast`) |
| Partial | 0.6 s | 0.07 s (`epd_fastest`) |
| 4-greyscale | 3.5 s | — |
| Text | — | 0.45 s (`epd_text`) |

The two sets are **not comparable as published**. M5Stack's figures are labelled
lab results for specific M5GFX LUTs — and this knowledge base has already
recorded that those LUTs may no longer be the ones shipped, and that M5Stack
itself warns its waveforms are unstable. Waveshare's are unlabelled as to method
or waveform. Treating "0.07 s versus 0.6 s" as a real eight-fold advantage would
be unsupportable. See
[`../../m5stack/papermono/performance.md`](../../m5stack/papermono/performance.md).

## What each board is actually for

The specifications overlap heavily; the design intent does not.

**Waveshare leans into sensing and voice.** An audio codec, a microphone path
explicitly aimed at online LLM services (DeepSeek, Doubao are named), a
temperature/humidity sensor, and a rotary navigation switch. Its stated
applications are voice interaction, e-reader, calendar and weather display.

**PaperMono leans into radio and power.** NFC (ST25R3916), LoRa (SX1262), a
frontlight, and a five-state hardware power manager built around a second
microcontroller. It has no audio output, no environmental sensor, and no
expansion connector at all.

So the honest framing is not "which is better" but this — **and the second pass
inverted half of it**:

**Neither board has an expansion connector.** The sentence that stood here
previously — that Waveshare "gives you a development board with headers" — was
written before the schematic was read, and it is **wrong**. The complete connector
census is one USB-C, three PH1.25-2P power/speaker JSTs, the panel FPC and a microSD
socket. No 2.54 mm header, no Qwiic, no broken-out GPIO, and every usable GPIO
already committed. See [C-WS1](gaps-and-conflicts.md#c-ws1--the-expansion-claim-is-backwards).

What Waveshare actually gives you over the PaperMono is **sensing, sound and a
backup-battery provision at roughly half the price**; what the PaperMono gives you is
**radios, a frontlight and an enclosed product with a real power state machine**.
Neither substitutes for the other on the other's workload, and **neither is a good
answer to "I need to attach hardware"** — for that, within Waveshare's own catalogue,
the answer is the 1.54-inch boards, which do carry a 2 × 6 header and give up 90 % of
the pixels to do it ([ESP32-S3-ePaper-1.54](../esp32-s3-epaper-1.54/README.md),
[ESP32-C6-ePaper-1.54](../esp32-c6-epaper-1.54/README.md)).

## Sibling products

Waveshare's current ESP32 e-paper line, from the storefront search
(retrieved 2026-09-01). Only the 3.97" is documented in depth here; the others
are recorded so the population is known and a future pass need not re-derive it.

| Slug | SKUs | Price, 2026-09-01, US | What it is | Record |
|---|---|---|---|---|
| `esp32-s3-epaper-3.97` | 33552 / 33810 / 33811 | **USD 34.99–47.99** | **this record** — 3.97", 800 × 480, ESP32-S3 | — |
| `e-paper-esp32-driver-board` | 15823 | USD 14.99 | Universal driver board, **original ESP32**, drives **23 documented raw panels** over a 24-pin FPC. Legacy wiki only | [stub](../e-paper-esp32-driver-board/README.md) |
| `esp32-s3-epaper-1.54` | 32298 / 32299 / **34211 / 34212 (touch)** | USD 15.99–22.99 | 1.54", 200 × 200, ESP32-S3-PICO-1-N8R8. **Has a 2 × 6 2.54 mm expansion header** | [stub](../esp32-s3-epaper-1.54/README.md) |
| `esp32-c6-epaper-1.54` | 34393 / 34394 | USD 16.99–17.99 | 1.54", 200 × 200, **ESP32-C6 — Wi-Fi 6, Zigbee/Thread**. Expansion header **plus a TCA9554 I/O expander** | [stub](../esp32-c6-epaper-1.54/README.md) |
| `esp32-s3-epaper-1.54g` | 34585 / 34586 | USD 17.99–18.99 | 1.54", 200 × 200, **`G` = red/yellow/black/white 4-colour** — *confirmed from the page title, no longer a guess* | none |
| `esp32-s3-epaper-13.3e6` | 34349 | **USD 259.99** | 13.3", **`E6` = E Ink Spectra 6 full colour**, with an ESP32-S3 driver board and audio codec — *confirmed from the page title* | none |
| `esp32-s3-photopainter` | 32408 / 32753 | USD 82.99–83.99 | 7.3" Spectra 6 photo frame in a wood surround. **An appliance, not a development board** | [stub](../esp32-s3-photopainter/README.md) |

**Corrected 2026-09-01:** the first pass flagged the `g` and `e6` suffixes as
unverified guesses. Both are now **confirmed from the products' own page titles** —
`G` is the four-colour (red/yellow/black/white) variant, `E6` is E Ink Spectra 6.
Prices and SKUs were added in the same pass.

Also in the survey but **not ESP32**: `photopainter` (24708/24709, RP2040-based),
`photopainter-b` (30068/30315, processor `unknown`) and `e-paper-esp8266-driver-board`
(14138, ESP8266). Recorded so they are not mistaken for members of this family.

### Which sibling answers "e-paper development with expansion"

**Not this one.** Of the seven, only the two 1.54-inch boards document an expansion
header, and they do it at 200 × 200 — 40 000 pixels against this board's 384 000.
That trade is the real finding of the survey and is set out in
[C-WS1](gaps-and-conflicts.md#c-ws1--the-expansion-claim-is-backwards).

## Documentation status

**Corrected 2026-09-01.** The first pass recorded three "gaps" here that are not
gaps; see the [banner](#-second-pass-2026-09-01--read-this-before-the-sections-below)
and [C-WS10](gaps-and-conflicts.md#c-ws10--first-pass-recorded-absences-that-are-not-real).
What Waveshare publishes for this board is, in fact, better than average for the
vendor: a documentation site, a schematic, a panel manual, four IC datasheets and an
official example repository with factory firmware.

**Real gaps that remain**, fully enumerated in
[gaps-and-conflicts.md](gaps-and-conflicts.md#gaps):

1. **No rendered schematic read** — no PDF rasteriser on this host, so connectivity is
   text adjacency only (`G1`).
2. **The 14 vendor examples were enumerated but not retrieved** (`G2`).
3. **Factory firmware not downloaded** — ~54 MB across four images (`G3`).
4. **No imagery, and no board dimensions** — the vendor publishes an outline drawing
   as a figure only (`G4`, `G5`).
5. **No declared framework versions.** Neither the docs nor the repository state a
   minimum ESP-IDF or Arduino-core version.
6. **Nothing hardware-verified** (`G6`).

### Vendor retrieval traps

Two, both folded into [`vendors/waveshare`](../../../vendors/waveshare/README.md)
because they will affect every future Waveshare pass.

**1 — The legacy wiki no longer holds new products.** `/wiki/ESP32-S3-ePaper-3.97`
returns **404** while `/wiki/E-Paper_ESP32_Driver_Board` returns 200. The two hosts
are **disjoint, not layered**: new products are on `docs.waveshare.com`, older ones
remain on the wiki, and `docs.waveshare.com/E-Paper-ESP32-Driver-Board` is itself a
404. **Check both hosts before concluding anything is unpublished.**

**2 — Waveshare's MediaWiki API is broken.** As of **2026-09-01**:

```
https://www.waveshare.com/wiki/api.php?...        → HTTP 200, but body is
https://www.waveshare.com/wiki/index.php?...      → HTTP 200, but body is

  Parse error: syntax error, unexpected '?' in
  /yundisk/web/waveshare/dotcom/w/includes/Setup.php on line 472
```

A **PHP fatal parse error with HTTP 200** — it fails in the worst possible way,
because any script checking status codes treats it as success. The vendor guide's
`action=parse&prop=wikitext` route is dead; rendered pretty URLs still work.

**3 — The e-paper category page returns 200 and zero products.** It is JS-rendered.
Use `/catalogsearch/result/?q=` to enumerate, never the category page. Note that the
query `esp32 e-ink` returns **nothing** — the storefront does not treat "e-ink" as a
synonym for "e-Paper".

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| W01 | ESP32-S3 3.97inch e-Paper Development Board | Waveshare | primary | store listing | `waveshare.com/esp32-s3-epaper-3.97.htm` | 2026-09-01 | All specifications in this record |
| W02 | Storefront search `e-paper esp32` | Waveshare | primary | store search | `waveshare.com/catalogsearch/result/?q=e-paper+esp32` | 2026-09-01 | The seven-product sibling population |
| W03 | Wiki 404s for three slug spellings | Waveshare | primary | wiki | `waveshare.com/wiki/ESP32-S3-ePaper-3.97` | 2026-09-01 | Verified absence of a wiki page |
| W04 | MediaWiki API PHP parse error | Waveshare | primary | api | `waveshare.com/wiki/api.php` | 2026-09-01 | The retrieval trap above |

**The full source table — twenty rows with class, medium, retrieval date, version,
what each establishes, its limitations and its local path — is
[`sources.md`](sources.md).** The four rows above are the first pass's and are kept
for continuity; `W03`'s "verified absence of a wiki page" is true of the *legacy host
only* and should be read with
[C-WS10](gaps-and-conflicts.md#c-ws10--first-pass-recorded-absences-that-are-not-real).

## Artifacts

**Corrected 2026-09-01.** The first pass recorded "no artifacts were retained …
nothing was downloaded, so nothing needed hashing". **Six PDFs were in fact
published**, and all six are now retained and hashed. Every one was validated by
**magic bytes (`%PDF-`), never by HTTP status**.

| Artifact | Bytes | SHA-256 | Filed under | Why there |
|---|---:|---|---|---|
| [`ESP32-S3_e-Paper-3.97-schematic.pdf`](artifacts/schematic/ESP32-S3_e-Paper-3.97-schematic.pdf) | 257 550 | `b12031451374e2333e8eca2b8290c40b4c67955b1f12df17b96f3ee479e6f0be` | **this device** | Describes this board |
| [`schematic-text-reflowed.tsv`](artifacts/schematic/schematic-text-reflowed.tsv) | 27 638 | *regenerable — see [commands.md](commands.md)* | **this device** | Derived reading aid, 1 150 positioned tokens |
| [3.97inch e-Paper manual **Rev 1.0, 2025-04-24**](../../../components/waveshare/3.97inch-e-paper/README.md) | 2 774 287 | `4f756734…` | **component** | Describes a *panel* |
| [AXP2101 datasheet **V1.4 EN**](../../../components/x-powers/axp2101/README.md) | 1 554 740 | `9e51d16d…` | **component** | Describes a *chip* |
| [ES8311 datasheet](../../../components/everest-semiconductor/es8311/README.md) | 729 315 | `be42a2cb…` | **component** | Describes a *chip* |
| [SHTC3 datasheet](../../../components/sensirion/shtc3/README.md) | 928 256 | `d315fe3d…` | **component** | Describes a *chip* |
| [PCF85063A datasheet **Rev. 6** (Waveshare mirror)](../../../components/nxp/pcf85063a/README.md) | 535 722 | `93b38487…` | **component** | Describes a *chip*; **kept alongside NXP's Rev. 7, which this KB already held** |
| Storefront + two docs pages | 324 780 | *date-pinned, not hash-pinned* | **this device** | `artifacts/source-snapshots/` |

Four of these are **component** artifacts even though a device pass fetched them —
filed by what they *describe*, per the method. The device cites each one where it is
used, so a reader starting here can reach them without knowing which component owns
them.

**Not downloaded**, recorded with URLs and expected sizes in
[`acquisition/manifest.json`](acquisition/manifest.json): the two 16 MB factory
firmware images and the two xiaozhi images (~54 MB total), and the vendor repository
itself (~50 MB).

**Two downloads failed and were deleted rather than kept under a misleading
extension** — one returned XML, the other **267 KB of HTML** behind a `.pdf` URL.
Both are recorded in [`sources.md`](sources.md#failed-and-negative-retrievals).

**Licences:** every artifact above is **`unknown`** — none states terms, and the
vendor repository has no `LICENSE` file. Recorded as metadata; nothing was omitted
over licensing.

## Used by / referenced from

**Devices and comparisons**

- [M5Stack PaperMono — comparisons and recommendations](../../m5stack/papermono/comparisons-and-recommendations.md) — §5, where this record replaces "an explicit gap, not a verdict"
- [M5Stack PaperMono — gaps and conflicts, C24](../../m5stack/papermono/gaps-and-conflicts.md) — the conflict this record closes
- [M5Stack PaperMono](../../m5stack/papermono/README.md) — the *when not to use* recommendation that started this

**Sibling Waveshare e-paper boards** (stubs created by the same pass)

- [e-Paper ESP32 Driver Board](../e-paper-esp32-driver-board/README.md) · [ESP32-S3-ePaper-1.54](../esp32-s3-epaper-1.54/README.md) · [ESP32-C6-ePaper-1.54](../esp32-c6-epaper-1.54/README.md) · [ESP32-S3-PhotoPainter](../esp32-s3-photopainter/README.md)

**Components this board uses**

| Reused, already in this knowledge base | Added by this pass |
|---|---|
| [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md) · [SSD1677](../../../components/solomon-systech/ssd1677/README.md) · [PCF85063A](../../../components/nxp/pcf85063a/README.md) · [micro-SD](../../../components/generic/micro-sd-sdmmc/README.md) · [USB-C interface](../../../components/generic/usb-c-interface/README.md) | [AXP2101](../../../components/x-powers/axp2101/README.md) · [3.97inch e-Paper panel](../../../components/waveshare/3.97inch-e-paper/README.md) · [ES8311](../../../components/everest-semiconductor/es8311/README.md) · [SHTC3](../../../components/sensirion/shtc3/README.md) · [NS4150B](../../../components/nsiway/ns4150b/README.md) · [QMI8658A](../../../components/qst/qmi8658a/README.md) *(stub over a pre-existing artifact)* |

**Vendor knowledge**

- [Waveshare documentation-sourcing guide](../../../vendors/waveshare/README.md) — extended with this pass's findings
- [All devices](../../README.md) · [All components](../../../components/README.md)
