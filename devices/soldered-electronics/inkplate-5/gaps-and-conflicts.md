# Inkplate 5 / Gen 2 — gaps and conflicts

> Snapshot **2026-08-24**. No hardware was available.

## 1. Three names for one board

| Context | Name |
|---|---|
| Soldered store | Inkplate 5 **Gen 2** |
| Arduino library board target | **`Inkplate5V2`** |
| Hardware repository | `Soldered-Inkplate-5-**Gen2**-hardware-design` |

Not a contradiction, but a reliable source of confusion. **Select `Inkplate5V2` in Arduino.**

## 2. Peripheral Mode — the documentation describes an obsolete protocol — RESOLVED

**Resolved 2026-08-24** by reading `examples/<board>/Diagnostics/Peripheral_Mode/` in the current Arduino library.

My earlier concern was that the documented **3-digit zero-padded** coordinate format (`#0(001,005,04)*`) cannot express X ≥ 1000 on a 1280-px-wide Gen 2. Investigating it surfaced something larger: **there are two incompatible peripheral protocols, and the published documentation describes the old one.**

| | Documented (old) | Shipped in the library (new) |
|---|---|---|
| Framing | `#<op>(<args>)*` | `TS;<cmd>;<rpt>;<size>;<args…>;` |
| Opcode | one ASCII char | 16-bit hex |
| Coordinates | fixed-width, zero-padded | **variable width, `atol()`** |
| Commands | ~40 | **60** |
| Batching | none | repeatable flag, many ops per packet |

So the coordinate limit **does not exist on current firmware**, and the documented protocol will not work on a board flashed from the current library. Both `Inkplate5` and `Inkplate5V2` examples implement the new protocol.

The new protocol also adds Wi-Fi connect/disconnect, HTTP GET/POST, deep/light sleep, touch and explicit SD power control — none of which appear in the documentation.

Full detail: [`features/peripheral-mode.md`](features/peripheral-mode.md).

**Remaining open:** the exact `payloadSize` accounting was not verified, so no tested client example is offered for the new protocol.

## 3. `hardware-reference.rst` is stale

Soldered's documentation source still states *"Inkplate 5 hardware repository is coming soon"*, although `Soldered-Inkplate-5-hardware-design` has existed since **2024-10-20**.

## 4. readthedocs is deprecated but still indexed

`inkplate.readthedocs.io` now serves only a JavaScript redirect to `soldered.com/documentation/inkplate`. Search engines still surface the readthedocs URLs, and the `.rst` source still contains cross-links to `inkplate.readthedocs.io`. Use the `.rst` source in the repository. See the [vendor guide](../../../vendors/soldered-electronics/README.md#documentation-migration-readthedocs--solderedcom).

## 5. WROVER variant not specified

Both BOMs list the module only as `ESP32-WROVER` — not WROVER-B or WROVER-E, and no flash size. Determining the fitted variant requires reading the module can or querying on hardware.

## 6. No E Ink panel datasheet

No primary manufacturer datasheet was located for `ED052TC2` or `ED052TC4`. E Ink does not publish panel datasheets openly. All panel specifications in this record are **derived from Soldered's design files and library source**, not from an E Ink document.

## 7. Refresh timings — RESOLVED, and my inference was wrong

**Resolved 2026-08-24** from the Soldered-era comparison table in `features.rst` (lines 57–84), which I had not extracted on the first pass.

| | Inkplate 5 | **Inkplate 5 Gen 2 (V2)** |
|---|---|---|
| Full refresh | **1.02 s** | **1.13 s** |
| Fast refresh | **0.12 s** | **0.26 s** |

I had inferred the Gen 2 "should be materially slower" because it pushes 78 % more pixels over the same bus. **That inference was wrong in magnitude**: full refresh is only **11 % slower** (1.02 → 1.13 s), not proportional to pixel count. Fast refresh roughly doubles (0.12 → 0.26 s), which is closer to the pixel ratio but still not linear.

The likely explanation is that full-refresh time is dominated by the **e-paper waveform duration** — a physical property of the electrophoretic medium — rather than by data transfer. Fast/partial refresh uses a much shorter waveform, so transfer time becomes a larger fraction of it, which is why it scales more with resolution.

**Recorded as a caution:** this is a good example of a plausible-sounding inference from architecture being wrong. Full vendor table now captured in [`README.md`](README.md#family-comparison).

Note the Inkplate 5 has the **fastest full refresh in the entire family** (1.02 s), beating even the smaller Inkplate 6 (1.26 s) — and the Inkplate 5's 0.12 s fast refresh is the quickest of any board listed.


## 8. Not covered in this pass

- The `.rst` documentation (~10,000 lines) was surveyed, not fully mined. `arduino.rst` alone is 4,556 lines.
- The KiCad schematics were **not** netlist-parsed (unlike the XIAO ESP32S3 Sense record) — component identification came from the BOM CSVs. Full pin-level connectivity for the Inkplate 5 is therefore **not** established here.
- The Inkplate 5 examples in the Arduino library were retained but not reviewed.
- Compliance documents (CE/UKCA) were retained but not read.
- No pricing or availability research.
