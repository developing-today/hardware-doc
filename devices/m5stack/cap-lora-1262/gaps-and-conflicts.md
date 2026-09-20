# Gaps and conflicts — Cap LoRa-1262 (U214)

Snapshot 2026-09-04. Each row states what would settle it.

## Conflicts between sources

### G1 — ⚠ RP-SMA or SMA? The vendor contradicts itself and owners disagree

| Source | Says |
|---|---|
| `docs.m5stack.com/en/cap/Cap_LoRa-1262` prose | *"equipped by default with an external **RP-SMA** antenna"* |
| Same page, specification row | *"Interface Type **RP-SMA (internal thread, internal hole)**"* |
| `shop.m5stack.com` product description | *"equipped by default with an external **SMA** antenna"* |
| Schematic, `E4` | footprint comment **`SMA-KE`** |
| Cap CC1101 schematic, `E1` (same connector family) | **`SMA-TH_KH-SMA-KE-Z`** |

**The specification row is self-contradictory.** *Internal thread + internal hole* describes
a **standard SMA female (jack)** — RP-SMA female has an internal thread and an inner **pin**.
So the row's parenthetical and its label disagree.

Owners disagree too, which is the practical tell:

- u/skinwill, 2025-12-30: *"Looks like RP-SMA in the image."* u/jader242: *"It's still rp."*
  ([r/M5Stack](https://old.reddit.com/r/M5Stack/comments/1pzazbe/))
- u/malonestar, 2025-11-24, with a photo: *"I think it is regular SMA female, I don't see
  any indications anywhere to RP-SMA … Worked for me with a SMA antenna."*
  ([r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1nkyy4c/)) — that thread is
  about the **U201** predecessor, which uses the same connector family
- u/Big-Bunch2804, 2026-08-23: *"Just so you know it's a rp-sma. They are a little specific."*
  ([r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1vvlcs9/))

**Would settle it:** a close photograph of `E4` showing whether the centre contact is a
socket or a pin, or an M5Stack part number for the connector. Until then, buy an adapter
kit — which is what owners repeatedly end up doing. See
[`components/generic/rp-sma-and-sma-antenna-connectors`](../../../components/generic/rp-sma-and-sma-antenna-connectors/README.md).

### G2 — TCXO voltage: 3.0 V (M5Stack) vs 1.8 V (Meshtastic)

Both in shipping software, both reported working. Detailed in
[`features/lora.md` §8](features/lora.md). **Would settle it:** a `Stamp LoRa-1262` module
datasheet or a photograph of the TCXO's marking under the shield can.

### G3 — `FM8625H` appears on the vendor pin-map but not on the schematic

The Cap LoRa-1262 pin-map graphic names an element **`FM8625H`** in the block that also
shows `PI4IOE5V6408 P0 → SX_ANT_SW`. The V1.1 schematic's only regulator is **`U3` =
`JW5712`** and there is no `FM8625H` designator anywhere in its `CO`-marker census.
Possibilities: a second-source regulator on a different build, a stale graphic, or a part
that exists inside the shielded `Stamp LoRa-1262 Mini` module. Unresolved. **Would settle
it:** a photograph of the board under the shield, or a later schematic revision.

### G4 — Does the Cap LoRa868 have a PI4IOE5V6408 or not?

M5Stack's own comparison table says U201 has **"RF Switch Control: None"**, and the U201
pin-map shows no expander. Meshtastic's `variant.cpp` comment says
*"PI4IOE5V6408 on the optional Cap LoRa-1262 **(and Cap LoRa868)**"*. The code probes and
tolerates absence, so nothing breaks either way. Unresolved; the comment is probably just
loose. **Would settle it:** the U201 schematic (published, **not fetched** in this pass).

### G5 — The Cardputer-Adv EXT pin labels `UART_RX`/`UART_TX` are backwards

Four sources against one. Fully documented in
[`pinouts-and-buses.md` §1.1](pinouts-and-buses.md). This one **is** resolved; it is listed
here because the wrong label is still live on M5Stack's Mesh Kit page and has cost at least
one owner a working GNSS.

### G6 — Two numbering conventions for the same 14-pin connector

Cap pages number LEFT 1–7 / RIGHT 14–8; the Mesh Kit page numbers odd/even. Not an error,
but a guaranteed source of miscommunication. [`pinouts-and-buses.md` §1](pinouts-and-buses.md).

## Missing documentation

| # | Missing | Consequence | Would settle it |
|---|---|---|---|
| **G7** | **No `Stamp LoRa-1262` module datasheet, in any form.** M5Stack publishes the *Semtech chip* datasheet instead | Unknown: module RF output at the connector, internal matching, TCXO vs XTAL, which SX1262 DIO pins are consumed internally, supply current, `SW` semantics | M5Stack publishing one; or a teardown photograph under the can |
| **G8** | **No certification identifier of any kind** — no FCC ID, CE, IC, RCM, TELEC/MIC. `docs.m5stack.com/en/certification` has no entry for `U214`, `Cap LoRa` or `Cardputer` | One wideband 868–923 MHz SKU sold worldwide with nothing to point at. Matters for anyone deploying rather than benching | A regulatory database hit; not found by this pass |
| **G9** | **No LoRaWAN anything** | No regional band plan, no duty-cycle handling, no join example, no community project | Someone demonstrating it |
| **G10** | **No RF or power measurement by anyone** | Every performance claim on this page is a vendor claim | A firsthand measurement |
| **G11** | `1PPS`, `NRST`, `ON/OFF`, I²C of the GNSS module are **not routed** | No precise timing, no hardware reset, no hardware standby | Nothing — it is a design decision, recorded so nobody hunts for the pins |
| **G12** | `ANT1818-04` (GNSS patch antenna) and `GP-02` (GNSS module comment) are unexplained strings from the schematic | Cannot source an exact replacement antenna | A BOM or an M5Stack parts list |
| **G13** | The `ENB` net of `U3` was **not traced end-to-end**; "always on" is `inferred` from `R1`'s adjacency plus the absence of an enable pin on the bus | A future agent should verify before relying on it for a power model | Rendering the sheet, or a netlist-grade extraction |
| **G14** | The UiFlow2/MicroPython API page was **enumerated but not fetched** | MicroPython users have no coverage here | Fetching `uiflow-micropython.readthedocs.io/en/latest/cap/lora1262.html` |
| **G15** | The **U201 schematic** and the **U214 structure/3D files** (`M5_Hardware/Products/U214_Cap_LoRa-1262/Structures`) were located but **not fetched** | Mechanical work and U201 verification blocked | Fetching them |

## Method limitations of this pass

- No hardware was present. Nothing was measured, flashed or executed on-device.
- The schematic PDF was parsed with a **pypdf-based re-implementation** of pdftotext's
  bbox output because poppler is absent on this host. Row-band grouping is reliable;
  the repo's `PI<desig><pin>`→net matcher is **not** under this extractor, so every pin
  assertion was cross-checked against M5Stack's published pin-map rather than taken from
  the matcher. See [`commands.md`](commands.md) and the
  [scratch README](../../../scratch/m5stack-lora-expansions/README.md).
- The schematic was **not rendered**; claims that depend on drawn geometry (net routing
  through resistors, no-connect glyphs) are labelled `inferred` where they occur.
