# Recovering netlists from vendor EDA files

Vendors increasingly publish schematic and PCB **source** alongside (or instead of) a PDF. Those files usually contain the complete, authoritative connectivity of the board — often including things the vendor's own written documentation gets wrong or omits entirely.

This guide covers how to extract that connectivity for the three cases encountered so far: **KiCad PCB**, **KiCad schematic**, and **EAGLE schematic**. It is device-independent; worked results live in the device records that link here.

> **Why bother.** On the [Seeed XIAO ESP32S3 Sense](../../devices/seeed-studio/xiao-esp32s3-sense/README.md) this method produced a board-to-board connector pinout the vendor has never published, identified a microphone the vendor never named, and exposed two pin assignments the vendor's wiki states incorrectly. Every one of those came from files that had been sitting in the download section the whole time.

---

## 1. Decide which file to parse

| Have | Parse | Difficulty | Gives you |
|---|---|---|---|
| `.kicad_pcb` | **This one, first** | Easy | **Resolved net names per pad** — ground truth |
| `.kicad_sch` | Second | Hard (geometric) | Component-level detail the PCB flattens |
| EAGLE `.sch` | This one | Easy (XML) | Explicit `<nets>` section — connectivity is *stated* |
| EAGLE `.brd` | Optional | Easy (XML) | Placement, side, board outline |
| PDF only | Try text extraction | Varies | Often nothing — see §5 |

**The single most useful rule: for KiCad, parse the `.kicad_pcb`, not the `.kicad_sch`.**

KiCad schematics store **no netlist**. Connectivity is *implied* by wire geometry — two things are connected because their coordinates coincide. Reconstructing that requires resolving symbol pin positions, applying each instance's rotation and mirror transform, snapping to a grid, and running union-find over the wire segments. It works, but it is error-prone.

The **PCB file stores resolved net names on every pad**. That is what the copper actually does. One regex pass gets you the answer.

---

## 2. KiCad PCB — the easy, authoritative path

`.kicad_pcb` is an s-expression text file. Each `footprint` contains `pad` entries, and each pad that is connected carries `(net <n> "<name>")`.

```
(footprint "..." (property "Reference" "J3") ...
  (pad "27" smd rect ... (net 42 "/IO42/PDM_CLK"))
```

A working extractor is [`kicad_pcb_nets.py`](../../tools/kicad_pcb_nets.py). Usage:

```bash
python3 kicad_pcb_nets.py board.kicad_pcb J3      # one component's pinout
python3 kicad_pcb_nets.py board.kicad_pcb --all   # every net
```

Notes:

- Net names are **hierarchical paths** (`/03 Sheet Name/NET`), and KiCad escapes `/` inside a net name as `{slash}`. Strip both.
- Unconnected pads appear as `unconnected-(J3-Pad20)`. That is a **positive finding** — it tells you a pin is deliberately not routed.
- The board outline is on the `Edge.Cuts` layer; collect `gr_line`/`gr_arc` endpoints and take the bounding box for board dimensions.
- The `(layers ...)` block gives the copper stack, so you can state layer count.

**Cross-check the result** against the vendor's own software support (see §6) before trusting it.

---

## 3. KiCad schematic — geometric reconstruction

Only worth doing when you need something the PCB flattens: series resistors, DNP parts, net-label aliases, or which pin of a symbol a net lands on.

The approach used in [`kicad_netlist.py`](../../tools/kicad_netlist.py):

1. Parse `lib_symbols` to get each symbol's pin coordinates.
2. For each placed `symbol`, apply `(at x y rot)` plus any `(mirror x|y)`.
   **Watch the sign convention** — the schematic Y axis is inverted relative to symbol space, so the transform is `gy = sy - ry`, not `+`.
3. Snap every point to a fine grid (0.001 mm) to survive float noise.
4. Union-find over `wire` segment endpoints.
5. Attach `label`, `global_label`, `hierarchical_label` and `power` symbol values to whatever net touches their coordinates.

Validation: pick a component whose pinout you already know — a header, a USB connector — and confirm the reconstruction matches. If the well-known part comes out right, the unknown parts probably are too.

**Single-pad nets are meaningful.** A pin sitting alone in its own net is a no-connect, and that is frequently the fact you are looking for (e.g. confirming which SoC pins are consumed by in-package memory rather than brought out).

---

## 4. EAGLE — XML, and it states the netlist

EAGLE `.sch` and `.brd` are plain XML with a documented DTD. Unlike KiCad schematics, **the schematic contains an explicit `<nets>` section**:

```xml
<net name="IO42/PDM_CLK">
  <segment>
    <pinref part="JA3" gate="G$1" pin="4"/>
    <pinref part="JP1" gate="G$1" pin="1"/>
  </segment>
</net>
```

So connectivity is read directly — no geometry. Extractor: [`eagle_netlist.py`](../../tools/eagle_netlist.py).

```bash
python3 eagle_netlist.py board.sch --bom     # parts list
python3 eagle_netlist.py board.sch --nets    # full netlist
python3 eagle_netlist.py board.sch --ref U1  # one component
```

The `<part>` elements carry `value` (often the **actual manufacturer part number**) and `library`, which is how an otherwise-unidentified component gets a name.

From the `.brd`, additionally:

- `<element>` gives placement `x`/`y` and `rot`; a rotation starting with `M` means **mirrored, i.e. bottom side**. Knowing which side a solder jumper or test point is on determines whether a modification is reachable when the product is assembled.
- Layer `20` (`Dimension`) wires give the board outline.

---

## 5. When the PDF is useless

Vendors that export schematics from **EAGLE via Qt** produce PDFs where all text is rendered as **vector paths**. Text extraction returns essentially nothing — a stray glyph.

Symptoms: a multi-hundred-KB PDF that `pypdf` reports as having pages but no extractable text.

**Do not conclude the schematic is unavailable.** Check whether the download is a ZIP containing the EDA source; frequently the same archive holds a fully parseable `.sch`. This exact situation hid a daughterboard schematic in plain sight for most of one research pass.

Conversely, **KiCad PDF exports usually do have a text layer**, and dumping it is a quick way to read the title block, revision history and designer annotations (charge-current formulas, current limits, and similar notes that appear nowhere else).

---

## 6. Always cross-check against software

A netlist you reconstructed is a hypothesis until something independent agrees with it. The cheapest corroboration is the **vendor's board-support code**:

| Source | Gives |
|---|---|
| `arduino-esp32/variants/<BOARD>/pins_arduino.h` | Pin aliases, `LED_BUILTIN`, USB VID/PID, bus defaults |
| `camera_pins.h`, board headers | Peripheral pin maps |
| ESP-IDF board components, Zephyr devicetree, `platformio` board JSON | Same, other ecosystems |

Three independent chains agreeing (PCB netlist, schematic, vendor header) is strong. Where they disagree, **record the disagreement** rather than silently picking one — the mismatch is usually itself the finding.

---

## 7. What this method reliably finds

Patterns worth looking for once you have a netlist:

- **No-connect pins on the main SoC** — reveals which GPIOs are consumed internally (in-package PSRAM, flash) and must never be used.
- **Shared nets** — two "different" functions on one pin. This is the classic source of silent data corruption, and vendors document the two functions on separate pages without ever connecting them.
- **DNP / 0 Ω strap pairs** — a fitted 0 Ω beside an unpopulated position is a *designed-in alternative configuration*. Moving one resistor can change a chip-select, a supply source, or a pull-up rail. Vendors rarely document these, and they frequently explain apparent contradictions in vendor pin tables.
- **Solder jumpers** — user-serviceable disconnects for peripherals.
- **Pull-up/pull-down strapping on connector pins** — a peripheral signal tied off rather than routed tells you a capability is *disabled by design*, not absent from the part.
- **Designer annotations** in the schematic text layer — component-value formulas that let you compute what changing a resistor does.

---

## 8. Evidence boundary

The techniques and the pin-convention warnings here are **[SRC]** — derived from actually parsing these formats and validating results against known-good components and independent vendor headers.

The tools linked live under a device directory because that is where they were written; they are not device-specific and can be copied. They have been exercised on **KiCad 9** and **EAGLE 9.6.2** files only. Older KiCad (pre-6, `.sch` s-expression v4) and Altium/OrCAD formats are **not covered** and were not attempted.

No claim is made that a reconstructed netlist is defect-free. Treat it as strong evidence that must still agree with an independent source.

## 9. Used by

- [Seeed XIAO ESP32S3 Sense](../../devices/seeed-studio/xiao-esp32s3-sense/pinouts-and-buses.md) — KiCad PCB + schematic (mainboard), EAGLE (daughterboard)
- [Seeed vendor sourcing guide](../../vendors/seeed-studio/README.md) — where these files live and what they are named
