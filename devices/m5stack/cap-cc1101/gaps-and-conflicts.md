# Gaps and conflicts — Cap CC1101 & NFC (U219)

Snapshot 2026-09-04, seven days after release.

## Conflicts

### C1 — Antenna connector: "RP-SMA" in prose, `SMA-KE` on the schematic

Same family of contradiction as on the LoRa Cap. The product page says the three supplied
antennas have *"RP-SMA connector (internal thread, female pin)"* — that phrasing **does**
describe an RP-SMA jack correctly (internal thread + pin), unlike the LoRa Cap's
self-contradictory *"internal thread, internal hole"*. But the schematic's board-side
connector is `E1 = SMA-TH_KH-SMA-KE-Z`, and `SMA-KE` is the same Chinese designation used
for the LoRa Cap's `E4`. Both boards therefore carry the same connector family while their
documentation describes it differently. **Unresolved.** See
[`components/generic/rp-sma-and-sma-antenna-connectors`](../../../components/generic/rp-sma-and-sma-antenna-connectors/README.md).

### C2 — Timeline slip, stated and unexplained

M5Stack told an owner in September 2025 that the "Hacker cap" would ship in
"December or January". It shipped 2026-08-28. Not a technical conflict, but it is the
documented reason a lot of people believed this board was vapourware, and it is why
searching for it in early 2026 finds only speculation.

## Gaps

| # | Gap | Consequence | Would settle it |
|---|---|---|---|
| **G1** | **The schematic's own RF-switch truth table could not be transcribed** — the `√`/`x` grid extracts as fragments under this pass's PDF reader | The truth table in this record rests on the product page + Arduino guide + a vendor Reddit post, all consistent, **but not on the schematic** | Rendering sheet 3 |
| **G2** | **`B0310J50100AHF` balun: no datasheet located.** The part number decodes plausibly as a **300–1000 MHz, 50 Ω ↔ 100 Ω** balun (Anaren/TTM-style `B<band><pkg>J50100AHF` naming) but that is **`inferred`** | Cannot verify insertion loss, balance or power handling; cannot substitute confidently | The manufacturer datasheet |
| **G3** | **`ANT1` (NFC loop) has no published geometry** | The differential matching network cannot be re-derived for another PCB | A PCB layer view or a Gerber |
| **G4** | **`I2C_EN` strap resistor not identified** | "Strapped for SPI" is `inferred` from the vendor's interface claim plus the wired `SS`/`SCLK`/`MOSI`/`MISO` | Rendering sheet 2 |
| **G5** | **`R1` (100 kΩ) polarity on `POWER_EN` not traced** | Whether the Cap defaults on or off is unestablished; bring-up code must drive G3 high defensively | Rendering sheet 1 |
| **G6** | **`U4`/`U5` port-by-port mapping not resolved** | Which SP3T port carries which band path is unknown; only the aggregate truth table is | Rendering sheet 3 |
| **G7** | **No certification identifier** | A four-band, region-agnostic transmitter with no published FCC/CE/IC/TELEC reference, defaulting to 915 MHz in the examples. Real compliance exposure — [`features/sub-ghz.md` §7](features/sub-ghz.md) | A regulatory database hit |
| **G8** | **Nobody has demonstrated CC1101 and NFC in use together** | The shared-SPI/different-mode question is unanswered in practice | A working example |
| **G9** | **No measurement of anything** | Every performance number is a vendor claim | Field reports (the board is 7 days old) |
| **G10** | **Case incompatibility** — 19.7 mm tall vs the LoRa Cap's 15.2 mm | Existing community cases will not fit | Nothing; recorded as a fact |
| **G11** | UiFlow2 page (zh-cn path) **not fetched**; the vendor's Arduino page was fetched but its NFC examples only skimmed | MicroPython and deeper NFC-example coverage missing | Fetching them |
| **G12** | Structure/3D files for U219 not located in `M5_Hardware` | Mechanical work blocked | Checking `m5stack/M5_Hardware` |

## Method limitations

- No hardware. Nothing measured, flashed or executed.
- Schematic parsed from the text layer with a pypdf-derived bbox reader (no poppler on this
  host); **not rendered**. Six of the twelve gaps above would close with a render.
- Value-to-designator pairing on densely populated rows is `inferred` where two designators
  share a text row.
