# Conflicts, gaps and unresolved identities — Waveshare ESP32-S3-ePaper-3.97

> Research snapshot **2026-09-01**. Nothing verified against hardware.
> Conflicts are **recorded, not resolved by preference** — per the
> [method](../../../.agents/skills/hardware-device-research/SKILL.md#conflict-protocol).
> Where a trust order is applied it is this repository's existing Waveshare rule
> ([vendor guide §4](../../../vendors/waveshare/README.md)): **schematic > demo source
> > wiki/docs > storefront**.

## Contents

| ID | Subject | Status |
|---|---|---|
| [C-WS1](#c-ws1--the-expansion-claim-is-backwards) | The board has no expansion header | **resolved — the claim it backed is refuted** |
| [C-WS2](#c-ws2--tg28-versus-axp2101) | PMIC named `TG28` by marketing, `AXP2101` by schematic and firmware | **resolved in favour of AXP2101** |
| [C-WS3](#c-ws3--the-storefront-swaps-flash-and-psram) | Storefront says 8 MB flash / 16 MB PSRAM | **resolved — storefront is wrong** |
| [C-WS4](#c-ws4--io-expander-column-heading-with-no-io-expander-part) | `IO Expander` heading, no such part | **unresolved** |
| [C-WS5](#c-ws5--sd-card-spi-names-but-4-bit-nets) | SD wired 1-bit SPI or 4-bit? | **unresolved** |
| [C-WS6](#c-ws6--refresh-times-disagree-between-module-and-panel-documents) | Refresh timings differ panel vs storefront | **unresolved — different measurement scopes** |
| [C-WS7](#c-ws7--gate-versus-source-orientation) | Panel manual says 800 gate × 480 source | **unresolved — contradicts register evidence next door** |
| [C-WS8](#c-ws8--is-this-the-same-panel-as-the-papermonos) | Same panel as the PaperMono? | **unresolved — strong circumstantial match** |
| [C-WS9](#c-ws9--gpio39-carries-two-functions) | GPIO39 double-assigned | **unresolved** |
| [C-WS10](#c-ws10--first-pass-recorded-absences-that-are-not-real) | An earlier pass in this same session recorded false absences | **resolved — corrected, history kept** |
| [C-WS11](#c-ws11--waveshare-mirrors-a-nine-year-old-rtc-datasheet) | Waveshare's PCF85063A mirror is Rev. 6 (2015) | **resolved — both copies kept** |
| [G1–G6](#gaps) | Open gaps | — |

---

## C-WS1 — the expansion claim is backwards

**The claim.** The [PaperMono record](../../m5stack/papermono/README.md#when-to-use--when-not-to-use)
advises that for "a general e-paper development board **with expansion**", a reader
should "prefer Inkplate or a Waveshare ESP32 e-paper board". That advice is what
[C24](../../m5stack/papermono/gaps-and-conflicts.md) asked this record to substantiate.

**What the evidence shows.** The ESP32-S3-ePaper-3.97 — the Waveshare board that is
otherwise the *closest possible* substitute for a PaperMono — **has no expansion
header at all.** Its complete connector census from the schematic
([pinouts §"There is no expansion header"](pinouts-and-buses.md#there-is-no-expansion-header))
is: one USB-C, three PH1.25-2P power/speaker JSTs, the panel FPC, and a microSD
socket. No 2.54 mm header, no Qwiic/easyC, no broken-out GPIO.

Additionally, **every usable GPIO is committed** — GPIO35–37 are consumed by the
module's octal PSRAM, and GPIO7 is the only table row without a function, itself
probably `SD_D1`.

**Resolution.** The Waveshare recommendation is now *backed by an internal record*,
which is what C24 required — but the specific reason given for it ("with expansion")
is **refuted for this board**. Recorded rather than quietly reworded.

**Where the claim *is* true.** Waveshare's smaller e-paper boards do carry expansion:
the [ESP32-S3-ePaper-1.54](../esp32-s3-epaper-1.54/README.md) and
[ESP32-C6-ePaper-1.54](../esp32-c6-epaper-1.54/README.md) both document a
"reserved 2 × 6 2.54 mm pitch female header interface for external expansion", and
the C6 adds a TCA9554 I/O expander. So the honest form of the advice is:

> *For e-paper development **with expansion**, Waveshare's option is a **1.54-inch
> 200 × 200** board, not a PaperMono-sized one. You trade almost all the display
> to get the header.*

`inferred` from vendor documentation; the 1.54 boards' schematics were not retrieved
in this pass.

## C-WS2 — `TG28` versus `AXP2101`

| Source | Says | Class |
|---|---|---|
| Storefront "What's On Board" (`S01`) | "**TG28** — highly integrated power management chip" | primary, marketing |
| `docs.waveshare.com` overview (`S02`) | "Onboard **TG28** power management chip" | primary, documentation |
| **Schematic** (`S05`) | Part label **`AXP2101`**, with pin nets `ALDOIN`, `ALDO1`–`ALDO4`, `BLDOIN`, `BLDO1`–`BLDO2`, `DLDO1/DC1SW`, `DLDO2/DC4SW`, `CPUSLDO`, `VSYS`, `PWRON`, `PWROK`, `VBACKUP` | **primary, design data** |
| **Vendor firmware** (`S09`) | Component directory `axpPower/`; `static XPowersPMU axp2101;`; `axp2101.begin(AXP2101_SLAVE_ADDRESS, …)`; vendored `REG/AXP2101Constants.h` and `XPowersAXP2101.tpp` | **primary, source** |

**Resolution: the fitted part is an [X-Powers AXP2101](../../../components/x-powers/axp2101/README.md).**
The schematic net names are the AXP2101's own pin names and could not plausibly
belong to a different device, and Waveshare's own firmware drives it through
XPowersLib's AXP2101 path. Under this repository's Waveshare trust order
(schematic > demo source > docs > storefront), both of the higher-ranked sources
agree against both of the lower-ranked ones.

**What `TG28` is remains unexplained.** It may be a package/marking variant, a
second-source or rebadge, or simply an error propagated from another product's copy.
No datasheet, product page or registry entry for a PMIC called "TG28" was found in
this pass. **Do not create a `tg28` component record** — it would be a part number
promoted from marketing copy, exactly what the method's
[evidence-discipline rules](../../../.agents/skills/hardware-device-research/SKILL.md#evidence-discipline-and-known-failure-modes)
forbid.

**Practical consequence:** write firmware against the AXP2101 register map. The
vendor's own code already does.

## C-WS3 — the storefront swaps flash and PSRAM

| Source | Claim |
|---|---|
| Storefront feature bullets | "integrated **8MB PSRAM** and external **16MB Flash**" ✅ |
| Storefront "What's On Board" | "ESP32-S3-WROOM-1-N16R8 … with integrated **8MB Flash and 16MB PSRAM**" ❌ |
| `docs.waveshare.com` | "stacked with **16MB Flash and 8MB PSRAM**" ✅ |
| Schematic part label | `ESP32-S3-WROOM-1-N16R8` |

**Resolution: 16 MB flash, 8 MB PSRAM.** The module part number decides it —
Espressif's `N16R8` suffix means N=16 MB flash, R8=8 MB PSRAM. The storefront
contradicts *itself* within one page; the "What's On Board" block is wrong.

Minor, but it is the kind of error that gets copied into a partition table.

## C-WS4 — `IO Expander` column heading with no I/O expander part

The schematic's GPIO allocation table heads its `GPxx` column **"IO Expander"**, yet
no I/O expander appears anywhere in the extracted text — no TCA9554, PCA95xx or
PCAL6416.

The sibling [ESP32-C6-ePaper-1.54](../esp32-c6-epaper-1.54/README.md) *does* fit a
TCA9554 and Waveshare documents it. Most probable explanation: **template reuse from
a sibling board's schematic**.

**Unresolved.** Text extraction cannot prove absence of a symbol. What would settle
it: rendering the sheet, or a photograph of the PCB back. Until then **no component
record has been created**, and no claim of an I/O expander appears in the device
record. Per the method, a heading is not a reading.

## C-WS5 — SD card: SPI names but 4-bit nets

Net names are SPI-flavoured (`SD_CLK`, `SD_MOSI`, `SD_MISO`, `SD_CS`) but `SD_D1` and
`SD_D2` are also present — which only make sense in 4-bit SDMMC.

Two readings, both plausible: the board is wired for 4-bit SDMMC and the vendor
simply named the nets after the SPI roles those pins take in 1-bit mode; or `D1`/`D2`
are pulled up and unused.

**Unresolved.** The vendor's `04_SD_Test` / `05_SD_Test` examples were not read in
this pass — that is the cheapest way to settle it and is the first thing a follow-up
should do. Compare Waveshare's
[Knob-Touch-LCD-1.8](../esp32-s3-knob-touch-lcd-1.8/README.md), which uses genuine
4-bit SDMMC.

## C-WS6 — refresh times disagree between module and panel documents

| Mode | Storefront / docs (`S01`, `S02`) | Panel manual (`S06`) |
|---|---|---|
| Full | 3.5 s | — |
| Fast | 2.8 s | — |
| Partial | 0.6 s | **0.3 s** |
| 4-greyscale | 3.5 s | **3 s @ 23 °C** |

**Unresolved, and probably not a true contradiction.** The panel manual measures the
*panel* under a stated condition (23 °C, a defined transition pattern, Tektronix
TCP0030A probe); the storefront figures are unlabelled as to temperature, waveform or
whether they include the host's SPI transfer time. A board-level number being slower
than a panel-level number is expected.

**Do not present either as measured performance.** Both are `reported-working`
vendor claims obtained under different, partly undisclosed conditions. The
[PaperMono record makes the same point about its own numbers](../../m5stack/papermono/performance.md),
and the comparison between the two boards' published refresh figures is therefore
**not admissible** — see
[comparisons](../../m5stack/papermono/comparisons-and-recommendations.md).

## C-WS7 — gate versus source orientation

The panel manual states **"4-3: Resolution: 800 gate × 480 source"** (`S06`).

This knowledge base's [DKE DEPG0397BBS770F3 record](../../../components/dke/depg0397bbs770f3/README.md)
establishes the opposite for the PaperMono's 3.97" panel — **800 source × 480 gate** —
and does so from *register evidence*: SSD1677 command `0x44` sets `XEA = 0x31F = 799`
(800 source columns) and `0x01` sets MUX = 480 gate lines, with the 48 000-byte frame
size confirming it.

**Unresolved.** Either the two panels genuinely differ in scan orientation, or
Waveshare's manual has the terms transposed. The DKE record already documents that
*its* manual contradicts its own mechanical drawing on this exact point (§8-C3), so a
transposition error in a document of this class has precedent.

**Practical impact: low.** Drivers address the framebuffer, and the vendor's
`EPD_3in97.h` declares `WIDTH 800`, `HEIGHT 480`. The conflict matters only if you
write your own controller init.

## C-WS8 — is this the same panel as the PaperMono's?

| Property | Waveshare 3.97" (`S06`) | DKE `DEPG0397BBS770F3` |
|---|---|---|
| Diagonal | 3.97" | 3.97" |
| Resolution | 800 × 480 | 480 × 800 |
| **Active area** | **86.40 × 51.84 mm** | **51.84 × 86.40 mm** |
| **DPI** | **235** | **235** |
| **Driver IC** | **SSD1677** | **SSD1677** |
| Greyscale | 4 | 4 (marketed; manual's optical table says 2) |
| Pixel pitch | 0.108 × 0.108 mm | — |
| Outline | 56.24 × 96.62 × 0.92 mm | — |
| Vendor part number | **not published by Waveshare** | `DEPG0397BBS770F3` |

Active area matches **to 0.01 mm** transposed, DPI matches exactly, and both carry an
**SSD1677**.

**Still `inferred`, not established.** Waveshare does not name a panel supplier or
part number anywhere — not on the storefront, not in the docs, not in the manual,
not on the schematic's text layer. The match is consistent with the same panel, with
two panels built to one reference design, or with two vendors independently choosing
a common ESL-market part.

**What would settle it:** a photograph of the FPC marking on either board, or a
Waveshare-published panel part number. Recorded as an open question in both
directions rather than asserted — the PaperMono record makes the same match and
reaches the same non-conclusion.

## C-WS9 — GPIO39 carries two functions

The allocation table puts both `AudioCTR_PIN` (amplifier enable) and `AXIS_INT1`
(IMU interrupt 1) on **GPIO39**.

If literal, the two cannot coexist: an output gating an amplifier and an input
taking an interrupt. More likely one of the two is a stale candidate assignment left
in the table.

**Unresolved.** Text adjacency cannot distinguish. Settle it by rendering the sheet
or by reading the vendor's `01_Audio_Test` and `05_QMI8658A` examples.

## C-WS10 — first pass recorded absences that are not real

**Kept as history, per the method's requirement to record refuted hypotheses with the
evidence and date that refuted them.**

An earlier pass on this same board (this record's initial version, written
2026-09-01) concluded that Waveshare publishes **no wiki page, no pinout, no
schematic, no sample code, no price and no panel controller** for this product, and
that "no artifacts were retained … nothing was downloaded". It reasoned from the
legacy wiki returning 404 and from the MediaWiki API being broken.

**All six absences are false.** What actually exists, retrieved 2026-09-01:

| Claimed absent | Actually | Evidence |
|---|---|---|
| Documentation page | `https://docs.waveshare.com/ESP32-S3-ePaper-3.97` — HTTP 200, full docs | `S02` |
| Schematic | `ESP32-S3_e-Paper-3.97-schematic.pdf`, 257 550 B, valid `%PDF` | `S05`, retained |
| Pinout | Allocation table drawn on that schematic | [pinouts-and-buses.md](pinouts-and-buses.md) |
| Sample code | `github.com/waveshareteam/ESP32-S3-ePaper-3.97` — 6 Arduino + 8 ESP-IDF examples, factory firmware | `S09` |
| Price | **USD 34.99 – 47.99**, three SKUs | `S01` |
| Panel controller | **SSD1677**, stated in the panel manual | `S06` |

**Root cause — and it is a reusable lesson, not a one-off slip.** The legacy
`/wiki/` route 404s for this product *because Waveshare migrated it*, and this
repository's own
[Waveshare vendor guide §8.2](../../../vendors/waveshare/README.md) already says
**"There is a newer documentation platform … `docs.waveshare.com/<PRODUCT>` … Check
it first."** The guide was written 2026-08-24 from the ESP32-P4 pass. It was not
consulted, and a 404 on the deprecated host was read as product-level absence.

This is precisely the failure mode the method names: **"Prove absence, not just
presence."** A 404 on one host is evidence about that host.

**Corrected in place**, with the original claims preserved here.

## C-WS11 — Waveshare mirrors a nine-year-old RTC datasheet

Waveshare serves the PCF85063A datasheet from `files.waveshare.com/wiki/common/`.
Hashed against the copy this knowledge base already held from NXP:

| Copy | Bytes | SHA-256 | Revision |
|---|---|---|---|
| NXP original (already held) | 726 288 | `a09223db…` | **Rev. 7**, 2018 |
| **Waveshare mirror** (new) | 535 722 | `93b38487…` | **Rev. 6**, 2015 |

**Both retained**, per the method's rule that same-document-different-hash means
keep both and investigate. The Waveshare copy is **three years and one revision
stale**. It documents what Waveshare ships to its customers; the NXP copy is what
you should design against.

This is the third independent confirmation of the vendor guide's
"re-hosted third-party PDFs may be stale" warning.

---

## Gaps

| ID | Gap | Why it matters | Cheapest way to close |
|---|---|---|---|
| **G1** | **No rendered schematic sheet.** Text extraction only; no `pdftotext`/poppler on this host | Connectivity is inferred from text adjacency, not traced. C-WS4, C-WS9 and the panel-rail question all hinge on it | Render page 1 with any PDF rasteriser and read it |
| **G2** | **Vendor examples not retrieved.** The 14 Arduino/ESP-IDF examples were enumerated but only `DEV_Config.h`, `EPD_3in97.h` and `axp_prot.cpp` were read | I²C addresses, SD bus width and the GPIO39 conflict are all answerable from them | Clone at `9b12d40` and read |
| **G3** | **Factory firmware not downloaded.** Two 16 777 216-byte images (`260304.bin`, `260314.bin`) plus two xiaozhi images (9.9 MB, 11.2 MB) | ~54 MB. Would give partition map, IDF version, build date via `tools/esp_image_info.py` | See [acquisition/manifest.json](acquisition/manifest.json) — recorded, not fetched |
| **G4** | **No imagery retained.** No board photo, no PCB shot, no dimension drawing | Cannot confirm connector census visually; C-WS4 stays open | `docs.waveshare.com` `Interfaces`/`Dimensions` sections carry figures |
| **G5** | **No board dimensions.** The vendor publishes an outline drawing as an image only; no numeric size found | Enclosure work impossible | Read the dimension figure |
| **G6** | **Nothing hardware-verified.** No unit in hand | Every behavioural claim is vendor-stated, source-read or inferred | Buy one (USD 34.99) |

## Cross-record links

- Closes [PaperMono C24](../../m5stack/papermono/gaps-and-conflicts.md)
- Feeds [PaperMono comparisons §5](../../m5stack/papermono/comparisons-and-recommendations.md)
- Vendor findings folded into [`vendors/waveshare`](../../../vendors/waveshare/README.md)
