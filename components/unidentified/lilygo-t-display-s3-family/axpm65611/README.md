# Unidentified — `AXPM65611` / `65b311` (LilyGO T-Display-S3 family)

- **Category:** unidentified. Two related-looking strings appear across the family; whether they
  are one part, two parts, or unrelated is **not established**.
- **Manufacturer:** **unknown.**
- **Scope:** deliberately scoped to the LilyGO T-Display-S3 family, per the repository
  convention for unidentified parts, so it cannot collide with other unknowns.
- **Retrieved:** 2026-09-07

## What is actually known

### String A — `AXPM65611`, from LilyGO schematics

Recovered from the designator/part text layer of **two** published schematics:

| Board | Designator | Adjacent pin label | Sheet |
|---|---|---|---|
| T-Display-S3 AMOLED (Touch sheet) | `U5` | `VIN`, pin 12 | `T-Display-S3-AMOLED-Touch.pdf` @ `6d1dc00` |
| T-Display-S3 AMOLED Plus | `U4` | `VIN`, pin 12 | `T-Display-S3-AMOLED-Plus.pdf` @ `6d1dc00` |

Context on both sheets places it in the **display supply** area, near `KIA3400` transistors
annotated `-2.2V` and `+4.6V` on the Plus sheet. AMOLED panels need positive and negative
supplies (ELVDD/ELVSS, commonly ≈ +4.6 V / −2.2 V), so **the strongest hypothesis is that this
is an AMOLED bipolar display-supply generator.** That is a hypothesis, clearly marked as one.

### String B — `65b311`, from a physical board

An owner tracing a **T-Display-S3** (base board) PCB reported the charger position `U6` carried
a **5-lead TSOT-23 marked `65b311`**, not the SOP-8 `TP4065` in the schematic —
[issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230), 2024-03-02, firsthand
inspection.

### The link between A and B is a guess

Both contain `65`+`6`/`b`+`311`/`611`. **That is the entire basis for connecting them, and it is
not enough.** Top-marking codes on small packages are usually vendor-internal and bear no
relation to the ordering part number, so a shared fragment between a *schematic part string* and
a *package top mark* is weak evidence. They are recorded together because a future reader
searching either string should find both, not because they are believed to be the same part.

## What was tried

| Attempt | Result |
|---|---|
| Search for a datasheet under `AXPM65611` | nothing found |
| Search for `65b311` as a top mark | nothing found |
| Look for the part in any other LilyGO repository | appears only on the two AMOLED sheets |
| Check whether X-Powers (`AXP`-prefixed parts) publishes it | no `AXPM` series found; the `AXP` prefix in "AXPM65611" may be coincidental |
| Check LilyGO's own BOM or `information/` directories | **LilyGO publishes no BOM for any board in this family** |

## What would resolve it

Any one of these, in decreasing order of decisiveness:

1. **A readable photograph of `U5`/`U4` on an AMOLED board** and of `U6` on a base board, at
   enough magnification to read the top mark and count the leads.
2. **LilyGO's BOM**, if it ever publishes one, or an answer in an issue thread — the maintainer
   answers technical questions readily and has posted PCB photographs before
   ([issue #313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313)).
3. **A measured charge current** on a base board, which would narrow the `65b311` part by
   behaviour even without a marking.
4. **Measuring the ELVDD/ELVSS rails** on an AMOLED board, which would confirm or refute the
   display-supply hypothesis for `AXPM65611`.

## Why this matters

For `65b311`: the entire published procedure for **changing the battery charge current** on the
T-Display-S3 derives from a TP4056/TP4065 datasheet. If the fitted part is different, that
procedure is unsafe advice. See
[`components/nanjing-top-power/tp4065`](../../../nanjing-top-power/tp4065/README.md).

For `AXPM65611`: if it is the AMOLED bipolar supply, it is on the critical path for anyone
trying to control panel power or measure sleep current on those boards.

## Used by

- [`devices/lilygo/t-display-s3-amoled`](../../../../devices/lilygo/t-display-s3-amoled/README.md) — `U5`
- [`devices/lilygo/t-display-s3-amoled-plus`](../../../../devices/lilygo/t-display-s3-amoled-plus/README.md) — `U4`
- [`devices/lilygo/t-display-s3`](../../../../devices/lilygo/t-display-s3/README.md) — possibly `U6`, via string B only

## Related unidentified strings in the same family

Recorded here rather than as separate stubs, since none has any evidence beyond a schematic
string:

| String | Board | Designator | Context |
|---|---|---|---|
| **`BV6802`** | T-Display-S3 AMOLED V1.0 | `U6` | near `AVDD` — display supply |
| **`BV6804`** | T-Display AMOLED Lite; T4-S3 | `U4` / `U6` | near `AVDD` — display supply |
| **`ULC0511C`** | T4-S3 | — | unknown |
| **`RS0108YTQC20`** | T-Display AMOLED Lite | `U2` | an 8-bit bidirectional **level shifter** — the Lite's panel runs at 1.8 V. Identity is well-supported by the `_1V8` net names around it; a datasheet was not obtained |

`BV6802` and `BV6804` sharing a prefix and both sitting on `AVDD` is the one genuinely
suggestive pattern here: they look like two members of one AMOLED-supply family, from a vendor
whose name begins `BV`. Still a hypothesis.

---

## Update — 2026-09-07: schematic net tracing. **String A's function is now established; string B's conflict is resolved in the owner's favour.**

Appended, not substituted. Everything above stands as written on 2026-09-07 (first pass); this
section reports what `pdftotext -bbox-layout` recovered once poppler became available. Method:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).

### String A — `AXPM65611` is an AMOLED bipolar display-bias supply. Hypothesis → established.

The symbol has **12 pins**, and both sheets agree pin-for-pin:

| Pin | Name | `T-Display-S3-AMOLED-Touch.pdf` p3 (`U5`) | `T-Display-S3-AMOLED-Plus.pdf` p3 (`U4`) |
|---|---|---|---|
| 1 | `SWP` | `PIU501` @ 282.50, 390.37 | `PIU401` @ 651.00, 95.37 |
| 2 | `PGND` | `PIU502` @ 282.50, 454.37 | `PIU402` @ 651.00, 152.91 |
| 3 | `VPOS` | `PIU503` @ 282.50, 397.83 | `PIU403` @ 651.00, 102.37 — annotated **`+4.6V`** @ 677, 100.1 |
| 4 | `EN` | `PIU504` @ 218.50, 446.37 | `PIU404` @ 593.00, 145.37 |
| 5 | `GND` | `PIU505` @ 282.50, 462.37 | `PIU405` @ 651.00, 160.37 |
| 6 | `TEST` | `PIU506` @ 282.50, 446.37 | `PIU406` @ 651.00, 145.37 |
| 7 | `CTRL` | `PIU507` @ 218.50, 462.37 | `PIU407` @ 593.00, 160.37 — net **`SWIRE`** @ 572, 196.6 |
| 8 | `AVDD` | `PIU508` @ 218.50, 422.37 | `PIU408` @ 593.00, 124.37 |
| 9 | `VNEG` | `PIU509` @ 282.50, 414.37 | `PIU409` @ 651.00, 117.37 — annotated **`-2.2V`** @ 677, 114.5; also labelled `EAVDD` |
| 10 | `SWN` | `PIU5010` @ 282.50, 430.37 | `PIU4010` @ 651.00, 131.37 |
| 11 | `VIN` | `PIU5011` @ 218.50, 397.83 | `PIU4011` @ 593.00, 102.37 — from **`+3.3V`** @ 569, 114.5 |
| 12 | `VIN` | `PIU5012` @ 218.50, 390.37 | `PIU4012` @ 593.00, 95.37 |

Two switch nodes, each with its own 10 µH inductor (`DFP252012TF-100M`: `L6`/`L7` on the Touch
sheet, `L3`/`L4` on the Plus sheet), producing one positive and one negative output at **+4.6 V**
and **−2.2 V** — the sheet states both voltages itself — plus a one-wire `SWIRE` control line on
`CTRL`.

That is unambiguously an **AMOLED panel bias generator (ELVDD / ELVSS)**. The hypothesis recorded
above is now **confirmed by the schematic, not merely plausible**. `SWIRE` in particular is the
one-wire ELVSS-trim protocol used by this class of part, and its presence on `CTRL` is strong
corroboration.

**Still unknown:** manufacturer and orderable part number. The function is established; the
identity is not. Nothing above should be read as identifying the part.

**Proposed real component record** — *proposed only, not created, and this unidentified record
must not be deleted:* `components/unidentified/lilygo-t-display-s3-family/axpm65611/` stays as
the canonical home until a manufacturer is established, at which point
`components/<manufacturer>/<part>/` should be created and this record should link forward to it.
Recorded in [`archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md`](../../../../archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md).

### String B — the `TP4065` / `65b311` conflict is **resolved**. The schematic never said SOP-8.

The claim recorded above and in the T-Display-S3 records — *"the SOP-8 `TP4065` in the
schematic"* — is **incorrect**, and the error was in this repository's reading of the schematic,
not in the owner's inspection of the board.

`T_Display_S3.pdf` p1 draws `U6` with **exactly five pin tokens**:

```
python3 trace.py grep bbox/tds3.xhtml '^PIU6'
  p1 x=264.50 y=483.48  PIU604      p1 x=283.50 y=496.46  PIU603
  p1 x=241.50 y=499.46  PIU601      p1 x=283.50 y=503.46  PIU605
  p1 x=264.50 y=518.48  PIU602
```

There is no `PIU606`, `PIU607` or `PIU608`. The pin function text at those coordinates reads
1 `CHRG`, 2 `GND`, 3 `BAT`, 4 `VCC`, 5 `PROG` — the LTC4054 / TP4054 / TP4056 **SOT-23-5**
arrangement. A 300 dpi render of the region confirms a five-terminal symbol visually.

Two sibling sheets give the same answer independently: `T-DISPLAY-S3-AMOLED.pdf` p1 `U5`
(`PIU501`…`PIU505`) and `T-Display-S3-AMOLED-Touch.pdf` p3 `U6` (`PIU601`…`PIU605`), both with
the same five function names.

**So the schematic and [issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230)
agree: the part is a 5-lead SOT-23/TSOT-23.** The owner's `65b311` top mark is consistent with
the schematic rather than contradicting it, and the two strings A and B are *still* unrelated —
string A is a 12-pin AMOLED bias supply, string B a 5-pin charger. The speculative link between
them, already described above as weak, should now be considered **refuted by pin count**: they
cannot be the same part.

### Charge current: the sheet states it

`T_Display_S3.pdf` carries a rotated note, tokens at x ≈ 311.7, y 510.95–531.81, reading
**`IBAT (mA) = 580`**, beside `R13` = 2 kΩ on `PROG`. (Poppler merges this with the adjacent
rotated designator `R13` into one apparent line; the rendered crop shows they are two separate
text objects.)

This narrows the fitted part by behaviour, which resolution route 3 above anticipated:

- It is **not a TP4057.** That part is **SOT-23-6** with a separate `STDBY` pin the symbol does
  not have, and its own datasheet — held at
  `components/generic/tp4057/artifacts/tp4057-datasheet-cn-m5stack-mirror.pdf` — specifies
  **500 mA typical at `RPROG` = 2 kΩ**, not 580 mA.
- 580 mA at 2 kΩ implies a programming constant near 1160, close to the TP4056 family's 1200.

**Consequence for the safety note above:** the published procedure for changing the T-Display-S3
charge current is derived from an 8-pin part's datasheet, and the fitted part is 5-pin. The
procedure's *arithmetic* may still be approximately right — the sheet's own 580 mA figure is
consistent with a TP4056-family constant — but it is derived from the wrong package and should
not be relied on without measurement. The warning stands; its basis is now better.

### Sheet-level evidence index

| Claim | File | Page | Coordinate |
|---|---|---|---|
| `TP4065` part string | `T_Display_S3.pdf` | 1 | 273.09, 484.09 |
| 5 pin tokens | `T_Display_S3.pdf` | 1 | see block above |
| `IBAT (mA) = 580` | `T_Display_S3.pdf` | 1 | x≈311.7, y 510.95–531.81 |
| `AXPM65611` string | `T-Display-S3-AMOLED-Touch.pdf` | 3 | 238.26, 474.41 |
| `AXPM65611` string | `T-Display-S3-AMOLED-Plus.pdf` | 3 | 615.31, 171.80 |
| `+4.6V` / `-2.2V` rails | `T-Display-S3-AMOLED-Plus.pdf` | 3 | 677, 100.1 / 677, 114.5 |

Full trace: [`devices/lilygo/t-display-s3-shared/schematic-netlist.md`](../../../../devices/lilygo/t-display-s3-shared/schematic-netlist.md).
