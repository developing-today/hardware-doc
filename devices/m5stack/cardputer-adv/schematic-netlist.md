# Cardputer ADV — net list traced from `Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf`

**Traced:** 2026-09-07 · **Method:**
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md)
· **Tool:** poppler 26.06.0.

**New file.** It does not replace `pinouts-and-buses.md`; where it contradicts an existing claim,
the contradiction is appended to that file and listed in
[`scratch/schematic-tracing/corrections-requiring-review.md`](../../../scratch/schematic-tracing/corrections-requiring-review.md).

## 0. Traceability

4 pages, A4 landscape 842 × 595 pt, `Creator: Altium Designer`. `pdfimages -list` returns
**zero rows — no embedded raster anywhere in the document.** 1 710 words, 66 `NL` net-label
tokens, full `CO`/`PI` coverage. **Fully traceable.**

### Calibration of the label-binding rule

Altium floats a net label ~3.2–4.2 pt *above* its wire, and symbol pins here are 7 pt apart, so a
label is nearly equidistant from the pin above and the pin below. The sign was fixed against a
known answer before anything else was trusted:

> `U7` (BMI270) pin 1 is `SDO`. The sheet prints **`7-bit Address 69H`** at (196.7–214.3,
> 114.51), and `R43` 3.3 kΩ runs from `+3.3V` (78.3) down to (136.00, 120.62) and across to
> `PIU701` at (157.00, 138.37). A BMI270's `SDO` selects the I²C address, so it must be strapped
> — it cannot also be a GPIO. Therefore `NLG8` (y 142.20) belongs to pin 14 (y 145.37), not to
> pin 1 (y 138.37): **labels bind downwards.**

Independently confirmed two sheets later: `U9` (TCA8418) has `SDA` and `SCL` on the same
`G8`/`G9` pair, which is only self-consistent under the same reading.

---

## 1. `U7` — BMI270 IMU, sheet 3. **`INT1` and `INT2` are not routed.**

| Pin | Name | Token @ coordinate | Net |
|---|---|---|---|
| 1 | `SDO` | `PIU701` @ 157.00, 138.37 | **`R43` 3.3 kΩ pull-up to `+3.3V`** → address `0x69` |
| 2 | `ASDX` | `PIU702` @ 229.00, 167.37 | *nothing* |
| 3 | `ASCX` | `PIU703` @ 229.00, 174.37 | *nothing* |
| 4 | **`INT1`** | `PIU704` @ 157.00, 167.37 | **⚠ nothing — not connected** |
| 5 | `VDDIO` | `PIU705` @ 229.00, 145.37 | `+3.3V` via `FB7` |
| 6 | `GNDIO` | `PIU706` @ 157.00, 188.91 | `GND` |
| 7 | `GND` | `PIU707` @ 157.00, 196.37 | `GND` |
| 8 | `VDD` | `PIU708` @ 229.00, 138.37 | `+3.3V` through `FB7` 120 Ω/MB ferrite; `C25` 10 µF/10 V, `C27` 100 nF |
| 9 | **`INT2`** | `PIU709` @ 157.00, 174.37 | **⚠ nothing — not connected** |
| 10 | `OCSB` | `PIU7010` @ 229.00, 196.37 | *nothing* |
| 11 | `OSDO` | `PIU7011` @ 229.00, 188.91 | *nothing* |
| 12 | `CSB` | `PIU7012` @ 229.00, 152.91 | tied to `VDDIO` (I²C mode) |
| 13 | `SCX` | `PIU7013` @ 157.00, 152.91 | **`G9`** (`NLG9` @ 109.50, 149.20) |
| 14 | `SDX` | `PIU7014` @ 157.00, 145.37 | **`G8`** (`NLG8` @ 109.50, 142.20) |

### The evidence for "not connected"

A row query at each pin's y across the **entire** page returns only `U7`'s own tokens:

```
python3 trace.py row <bbox> --y 167.37 --tol 4 --page 3
  p3 x=157.00 y=167.37  PIU704      p3 x=157.53 y=164.84  4
  p3 x=176.83 y=168.44  INT1        p3 x=208.60 y=168.44  ASDX
  p3 x=229.00 y=167.37  PIU702      p3 x=229.72 y=164.84  2
```

Nothing else on the sheet lies at that height — no net label, no other component pin, no power
port. The same is true at y=174.37, and at the four OIS pins (2, 3, 10, 11) which are likewise
bare. Compare pin 8's row, which *does* return `PIC2502`, `PIC2702`, `PIFB701/02` and `+3.3V`.

**Consequence:** IMU motion-wake from deep sleep is **not available on the ADV**. M5Unified's
polling is not a library shortcoming; there is no interrupt line to use. This closes the
"not established, not absent" state the record previously carried, in the direction of *absent*.

## 2. `J2` — the Grove / `HY-2.0_IIC` port, sheet 1. **SCL = GPIO1, SDA = GPIO2.**

| `J2` pin | Symbol name | Net label on the wire | Module pin | Module pin name |
|---|---|---|---|---|
| 1 | `IIC_SCL` | **`GI`** @ 737.32, 366.41 | `P1.1` | **`G1`** |
| 2 | `IIC_SDA` | **`GO`** @ 738.58, 373.60 | `P1.2` | **`G2`** |
| 3 | `VCC` | — | — | 5 V rail via `D8` `PESDNC2FD5VB` |
| 4 | `GND` | — | — | — |

Pull-ups `R3` and `R10`, both 10 kΩ, sit above the pair (`PIR301`/`PIR1001` @ y 354.6). ESD
protection is `D6`/`D7` `PESDNC2FD3V3B` on the two signals and `D8` `PESDNC2FD5VB` on `VCC`.

### Why this took a render to settle

The net labels extract as the literal strings **`GI`** and **`GO`** — letter *I*, letter *O*.
This is not a font-mapping fault: `G0` and `G1` both appear elsewhere on the same sheet and
extract correctly. A 300 dpi crop shows the module symbol's own pin names printed immediately
beside them in an unmistakable digit glyph: **`G1`** and **`G2`**.

So the nets are *named* `GI`/`GO` — a vendor typo in the net names — while the pins they land on
are `G1` and `G2`. Searching the text layer for "G1" or "G2" near `J2` finds nothing, which is
exactly why earlier passes could not bind them.

**This agrees with M5Unified** (`_pin_table_i2c_ex_in`, `EX SCL = GPIO_NUM_1`,
`EX SDA = GPIO_NUM_2`) and with Bruce (`-DGROVE_SCL=1 -DGROVE_SDA=2`). The worry that M5Stack's
yellow-wire convention would invert it is **not borne out by the schematic**.

Independently corroborated on a different product: the M5Stack Cap-Bus connector uses the same
`GI`/`GO` net names and pairs them explicitly with symbol pin names `SCL` and `SDA` —
see [`devices/m5stack/cap-lora-1262/schematic-netlist.md`](../cap-lora-1262/schematic-netlist.md).

## 3. `U4` — SY8089 buck. **The feedback arithmetic does resolve.**

| Pin | Name | Token | Connects to |
|---|---|---|---|
| 4 | `IN` | `PIU404` @ 582.50, 203.37 | 5 V rail, `C12` 22 µF |
| 1 | `EN` | `PIU401` @ 582.50, 210.37 | — |
| 3 | `LX` | `PIU403` @ 640.00, 203.37 | `L2` 4.7 µH `3015` → `+3.3V` |
| 5 | `FB` | `PIU405` @ 640.00, 232.37 | divider midpoint |
| 2 | `GND` | `PIU402` @ 582.50, 232.37 | — |

The divider is **`R11` 68 kΩ upper / `R13` 15 kΩ lower**, both in the column at x ≈ 690:

```
PIR1102 @ 690, 206.9   (to the +3.3V rail at y 203.8)
PIR1101 @ 690, 228.9 ─┐
                      ├─ FB node, U4.5 @ 640, 232.37
PIR1302 @ 691, 235.6 ─┘
PIR1301 @ 691, 258.2   (to GND at y 280.1)
COR11 @ 697.50, 214.20 · "68KΩ" @ 702, 222.4
COR13 @ 698.00, 243.93 · "15KΩ" @ 702, 251.4
```

Two errors produced the earlier impossible result:

1. **The upper resistor is `R11`, not `R12`.** `R12` is 100 kΩ and sits at `COR12` @ 236.50,
   221.20 — 450 pt away, on the opposite side of the sheet, in an unrelated network.
2. **The printed formula `Vout=1.2V*(R1/R2+1)` belongs to `U2`, not `U4`.** It is at
   (612.67, 157.65), directly beneath the **SY7088** boost converter (`U2`, symbol at y 63–135),
   about 86 pt above the SY8089. Applied to `U2`'s own divider — `R4` 75 kΩ / `R6` 22 kΩ — it
   gives 1.2 × (75/22 + 1) = **5.29 V** for the `+5VOUT` rail, which is self-consistent.

With the correct pair, 3.3 V requires a feedback reference of 3.3 / (68/15 + 1) = **0.596 V**.
A 0.6 V reference makes the design exact. That is *derived from the sheet*, not read from a
datasheet — no SY8089 datasheet is held in this repository — but 0.6 V is the value commonly
published for the part, and the agreement to 0.7 % is not a coincidence.

## 4. `U9` — TCA8418RTWR keyboard controller, sheet 2

Address printed on the sheet: **`7-bit Address 34H`** @ (106–142, 312.5).

| Pin | Name | Net | Evidence |
|---|---|---|---|
| 1 | `ROW7` | **unconnected** | `PIU901` @ 164.00, 206.91 — no label, no peer |
| 2–8 | `ROW6`…`ROW0` | `ROW6`…`ROW0` | `NLROW0`…`NLROW6` @ x 184.50, y 152.66–196.20 |
| 9–18 | `COL0`…`COL9` | `Y7`…`Y0` via 22 R/1 % series resistors `R27`…`R34` | x 164.00, y 221.37–286.37 |
| 19 | `GND` | `GND` | |
| 20 | `RESET` | `R38` 10 kΩ pull-up | `PIR382` @ 81.00, 264.37 |
| 21 | `VCC` | `+3.3V` | |
| 22 | `SDA` | **`G8`** | `NLG8` @ 77.00, 239.20 |
| 23 | `SCL` | **`G9`** | `NLG9` @ 77.00, 232.20 |
| 24 | `INT` | **`G11`** | `NLG11` @ 78.50, 224.66 |
| 25 | `EP` | `GND` | |

`R35`, `R36`, `R37` — three 3.3 kΩ resistors at x = 48.5 / 59.5 / 70.5, all spanning y 184.57 →
206.57 — pull up `SDA`, `SCL` **and `INT`** to `+3.3V`. The `INT` pull-up matters: the TCA8418's
`INT` is open-drain, and the driver deliberately configures its GPIO as plain `INPUT` with no
internal pull (see the driver audit), which is correct *only because* `R37` exists.

Seven rows are wired, eight columns are used → a 7 × 8 = 56-key matrix.

## 5. `P1` — the Stamp-S3A module footprint, sheet 1

| Pin | Module pin name | Net |
|---|---|---|
| 1 | `G1` | `GI` → `J2.1 IIC_SCL` |
| 2 | `G2` | `GO` → `J2.2 IIC_SDA` |
| 3–9 | `G3`…`G9` | `G3`…`G9` |
| 10 | `G10` | `GND` label at +30.0 dx |
| 11 | `G11` | `G11` → `U9.24 INT` |
| 12–13 | | `05VIN` (i.e. `+5VIN`; `NL` tokens substitute `0` for `+`) |
| 14–15 | `G13` | `G13` |
| 16–17 | `G15` | `G15` |

Note the `NL`-token mangling rule: `NL05VIN` is the net `+5VIN`, not a net called `05VIN`.

## 6. Other named parts on the sheets

`U1` `TP4057` charger (sheet 1) · `U2` `SY7088` boost · `U3` reset/supervisor · `U4` `SY8089`
buck · `U5` audio amplifier (`INP`/`INN`, sheet 3) · `U6` I²S codec (`CCLK`/`MCLK`, sheet 3) ·
`U7` `BMI270` · `U8` `MSM381A3729H9BPC` PDM microphone (sheet 3) · `U9` `TCA8418RTWR`.

---

## Reproducing

```bash
nix-shell -p poppler-utils --run 'pdftotext -bbox-layout \
  "devices/m5stack/cardputer-adv/artifacts/schematic/Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58.pdf" /tmp/adv.xhtml'
cd scratch/schematic-tracing
python3 netlist.py /tmp/adv.xhtml --page 3 --des U7
python3 netlist.py /tmp/adv.xhtml --page 2 --des U9
python3 trace.py   row /tmp/adv.xhtml --y 167.37 --tol 4 --page 3    # the INT1 negative result
```
