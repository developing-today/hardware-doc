# Cardputer ADV — gaps, conflicts and unresolved identities

> Snapshot **2026-09-04**. Each entry states what the conflict is, who says what, what would
> settle it, and — where I take a position — why.

## Conflicts

### C1 — The Mesh Kit page swaps UART TX and RX ✅ **resolved**

`docs.m5stack.com/en/core/Cardputer_Mesh_Kit`'s "Cardputer-Adv EXT 2.54-14P" table gives
pin 12 = `G13` = `UART_RX` and pin 14 = `G15` = `UART_TX`. Four sources say the opposite:
the ADV product page's identical table, the schematic's own symbol pin names (`GPS-RX` on the
G13 pin), `M5Cardputer-UserDemo`'s `uart_set_pin(port, GPIO_NUM_13 /*tx*/, GPIO_NUM_15 /*rx*/)`,
and Meshtastic's `GPS_TX_PIN 13` / `GPS_RX_PIN 15`. **The Mesh Kit page even contradicts itself**
two tables later, where its Cap-Bus table maps `G13 → GPS-RX`.

**Position: G13 = host TX, G15 = host RX.** The Mesh Kit EXT table is a documentation defect.

### C2 — Which Grove pin is SCL ⚠ **open, with a working answer**

M5Unified's `_pin_table_i2c_ex_in` row for `board_M5CardputerADV`, under the header comment
`// In SCL,SDA, EX SCL,SDA`, reads `{ …, GPIO_NUM_1, GPIO_NUM_2 }` → **EX SCL = G1** (white),
**EX SDA = G2** (yellow). Bruce agrees (`-DGROVE_SCL=1`, `-DGROVE_SDA=2`). M5Stack's usual
Grove colour convention puts SCL on **yellow**, which would invert it. The docs PinMap avoids
the question entirely by naming the port `PORT.CUSTOM` and the pins `G2`/`G1`.

The schematic sheet 1 shows `IIC_SCL` and `IIC_SDA` net labels near P1/J2, but the band-based
text extraction could not bind them to individual pins, and no page render was cropped at that
location in this pass.

**What would settle it:** a 1:1 crop of ADV schematic sheet 1 around P1, or an I²C device
plugged in and probed. **Practical answer: use the library values.** Whatever the silkscreen
implies, `M5.Ex_I2C` will drive G1 as clock.

### C3 — The v1.0 and v1.1 schematics are the same file ⚠ **open**

`…/481/Sch_M5Cardputer.pdf` and `…/1127/Sch_M5Cardputer.pdf` are byte-identical
(SHA-256 `6016c1fe6099b9e3f0d0c88f07a3fba1aa44a3da8a7a91dd7040ad0fffa2041e`, 717 743 B), as are
the two base schematics (`29542fe1…`, 24 076 B).

Two readings: (a) the v1.1 mainboard is genuinely unchanged and every difference is in the
Stamp module — which M5Stack's own comparison table supports, since it lists only module-level
differences; or (b) the v1.1 schematic was never published and the v1.0 file was reused.

**Position: no mainboard change is documented, and I do not assert one either way.** Anyone
with both boards in hand could settle it by comparing silkscreen revision markings.

### C4 — The RGB/backlight warning appears on the v1.1 page but not the ADV page ⚠ **vendor gap**

The v1.1 page: *"Since RGB and LCD backlight share the same power source, when the LCD backlight
brightness is below 100%, RGB will not be powered properly."* The ADV page carries only the
positive instruction ("set GPIO38 … to a high level") and **not** the warning — despite the ADV
using the same Stamp-S3A and therefore the same AW35122FDR-switched `BL_3V3` rail feeding the
same WS2812. Verified by comparing U3's `VDD` net across the two Stamp schematics.

**Position: the warning applies to the ADV.** The omission is a documentation defect.

### C5 — The Stamp-S3A schematic link is named for the wrong part ⚠ **cosmetic**

Both the ADV and v1.1 pages label `…/1150/Sch_StampS3_v0.3.3.pdf` as *"Stamp-S3A Schematics
PDF"*, while the filename says `StampS3`. The file's contents are unambiguously the S3A
(AW35122FDR, JW5712, `BL_3V3`-fed WS2812), so this is a filename artefact, not a wrong link.
Recorded because it is exactly the sort of thing that makes a future reader think they have the
wrong document.

### C6 — Vendor current figures are not internally consistent ⚠ **open**

The ADV page gives 120.2 mA operating / 132.3 mA Wi-Fi / **154.6 mA BLE**. BLE drawing *more*
than Wi-Fi is unusual and suggests the three measurements were taken with different display or
CPU states, which M5Stack does not state. The v1.1 page publishes an entirely different set of
conditions (*"IR transmission mode 148.07 mA, key mode 138.93 mA"*), so **the two generations'
figures cannot be compared**.

**What would settle it:** an instrumented measurement at a stated backlight level.

### C7 — ⚠ Cross-session conflict: the Stamp-S3A's `U4` **is** labelled `JW5712` ✅ **resolved here**

A concurrent session created
[`components/unidentified/m5stack-stamp-s3a/dcdc-u4`](../../../components/unidentified/m5stack-stamp-s3a/dcdc-u4/README.md)
on 2026-09-04, stating:

> "**Manufacturer / part number:** ⚠ **NOT ESTABLISHED.** The `Sch_StampS3_v0.3.3.pdf` symbol
> carries **no part-number text**."

**That is incorrect, and the correction is easy to verify.** The part number is printed in the
Altium Comment field directly beneath the symbol body.

Evidence, all from the vendor's own published render:

| Check | Result |
|---|---|
| Render used | `https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1150/Sch_StampS3_v0.3.3_page_01.png`, SHA-256 `1156e645de35fe68e6458e9131657c8f02045bbcd14f97ab190bb1486ee7a1c5` — **re-fetched and hash-matched against the live URL** while writing this entry |
| 1:1 crop, region `1000,3300–2200,3900` px | shows the yellow symbol with pins `EN`, `SW`, `VOS`, `VIN`, `VSEL1`, `VSEL2`, `VSEL3`, `GND`, and **`JW5712`** in blue immediately below the body |
| Text-layer occurrences of `JW5712` | **1** in `Sch_StampS3_v0.3.3`, **0** in `Sch_M5StampS3_v0.2` |
| Independent corroboration | the sibling record's own observed facts — *"IOUT: 0~0.6A"*, three `VSEL` strap pins, **no feedback divider**, `VOS` remote sense — match [`components/joulwatt/jw5712`](../../../components/joulwatt/jw5712/README.md) exactly: **600 mA continuous / 800 mA peak, 2.3–5.5 V in, eight resistor-free output voltages selected by three `VSEL` straps.** That record already existed, from the PaperMono pass on 2026-09-01, where the same part is fitted as `U10`. |

**Probable cause of the disagreement:** the sibling record says the marker layer was parsed.
Altium's `CO`/`PI`/`NL` markers are an *invisible* layer, and on these files the readable text —
part numbers, values, net names — lives inside a **Form XObject** that a marker-only parse never
enters. This session hit exactly the same trap and it failed *silently*, producing plausible-
looking output containing none of the readable text
([`commands.md`](commands.md) §4, attempt 3).

**Position: Stamp-S3A `U4` is a JoulWatt `JW5712`.** A ready-to-paste correction, and the
*Used By* rows this implies, are in
[`scratch/m5stack-cardputer/index-fragments.md`](../../../scratch/m5stack-cardputer/index-fragments.md).
That session's tree was **not edited** — its files were modified within the last 30 minutes.

## Unresolved identities

### U1 — The StampS3 v0.2 3.3 V regulator ✅ **resolved by a concurrent session**

Designator `M2`, a 5-terminal EN/VIN/VOUT/FB/GND symbol with an R16 100 k / R17 22.1 k feedback
divider. The value string extracted here was **`MUN3CAD01-SC`**, which this session flagged as
suspect because it resembles an ON Semi dual digital transistor and does not match the symbol —
and because **no page render exists** for product id `522` (the `_page_NN.png` convention 404s
there) to check the reading against.

**The reading was correct and the suspicion was wrong.** A concurrent session retrieved a
datasheet and identified it as a **Murata `µPOL` 1 A point-of-load power module** — a
fully-integrated converter, inductor and capacitors in a 2.9 × 2.3 × 1.05 mm package, 2.7–5.5 V
in, 0.8–4.0 V out set by an external divider. That is exactly the 5-terminal EN/VIN/VOUT/FB/GND
symbol observed. Record:
[`components/murata/mun3cad01-sc`](../../../components/murata/mun3cad01-sc/README.md).

Recorded here with the date because the skill asks for refuted hypotheses to be written down:
**hypothesis "the `MUN3CAD01-SC` string is a mis-extraction" — refuted 2026-09-04.** Affects the
Cardputer v1.0 only.

### U2 — LP3218DT1G manufacturer

Q1, Q2, Q3 on the ADV (and the same designators on the v1.x) carry the marking `LP3218DT1G` in
the schematic value field. The manufacturer is not established. Recorded at
[`components/unidentified/cardputer/lp3218dt1g`](../../../components/unidentified/cardputer/lp3218dt1g/README.md)
rather than guessed.

### U3 — BMI270 interrupt lines

`INT1` (U7 pin 4) and `INT2` (U7 pin 9) appear on the schematic symbol. Neither was resolved to
a GPIO by the text extraction, no vendor document mentions a BMI270 interrupt on this board, and
M5Unified polls. **Stated as "not established", not as "absent"** — the difference matters,
because if an interrupt *is* wired, IMU motion-wake from deep sleep becomes possible.

**What would settle it:** a 1:1 crop of ADV sheet 3 around U7 pins 4 and 9.

### U4 — The `+3.3V` feedback divider arithmetic does not work out

Applying the sheet's own `Vout = 1.2 V × (R1/R2 + 1)` to the resistors read near the SY8089
(R12 68 kΩ, R13 15 kΩ) gives ≈ 6.6 V, not 3.3 V. Either the resistor identification from the
text layer is wrong (several `R` values sit close together on sheet 1), or the SY8089 uses a
different feedback reference than the SY7088. **Recorded rather than fudged.** Do not use the
computed number.

## Gaps — things that appear not to exist

Each of these is a **verified negative** (method stated), not a failed search.

| Gap | Method | Result |
|---|---|---|
| **No RTC** | full designator census of all 4 ADV sheets; no 32.768 kHz crystal; no coin cell; no RTC row in the spec table; **positive control**: the CardputerZero page *does* list `RX8130CE @ 0x32` | verified absent |
| **No IR receiver** | designator census; **positive control**: CardputerZero lists "IR transmitter + receiver" and an `IR_RX` pin | verified absent |
| **No USB-UART bridge** | designator census of the Stamp-S3A sheet — `J2 USB-TYPEC`, CC resistors, PPTC, choke, ESD, no bridge IC | verified absent |
| **No PSRAM** | `ESP32-S3FN8` is flash-in-package only; no external PSRAM on either Stamp schematic; every spec table omits PSRAM; community firmware compensates for its absence explicitly | verified absent |
| **No fuel gauge** | designator census; battery sense is a divider on G10; **positive control**: CardputerZero lists `BQ27220YZFR` | verified absent |
| **No reset button** | ADV spec table lists no buttons; sheet 1 has exactly `BTN1`, `BTN2`, `SW1`, `SW2`; **contrast**: the v1.1 table lists "1 × Reset button + 1 × User button" | verified absent on ADV |
| **No ESD protection on the CAP header (P3)** | designator census of sheet 4 finds only `P3` | **inferred** — absence in a census, weaker than the above |
| **No CAP board ID/presence-detect pin** | full P3 pinout accounted for | verified absent |

## Gaps — things that exist but were not retrieved

| Item | Status |
|---|---|
| **Certification (FCC/CE/TELEC)** | `docs.m5stack.com/en/certification` is a known **soft gap** (see [`vendors/m5stack`](../../../vendors/m5stack/README.md) §5.1). This pass did **not** run the required positive control on that page for the Cardputer, so the correct statement is *"not established"*, **not** *"no certification exists"*. |
| `/en/product_i2c_addr` entry for the Cardputer family | not checked with a positive control |
| Hardware design files (KiCad/Altium source) | `github.com/m5stack/M5_Hardware` has `Products/K132-Adv_Cardputer-Adv/Structures` and `Products/K152_Cardputer_Mesh_Kit/Structures` per the docs links — **the structure/CAD directories were not fetched in this pass** |
| CardputerZero schematic, `CardputerZero_Labels.zip` | URLs recorded, not fetched |
| M5Burner firmware records for the Cardputer family | the `/api/v1/firmwares/{id}` route is documented in the vendor guide; **no id was resolved for the ADV** in this pass |
| EasyLoader binary `…/1178/Easy_Loader_for_Cardputer-Adv.exe` | URL recorded, **not downloaded** |
| Per-switch net assignment for all 56 keys | the rule is verified at the array corner and by the driver; 54 switches were not individually traced |
| "BKLVA Pocket DAW" repository | announced on Reddit three times; repository not located |
| Hackaday coverage of the ADV | none found |
| Any independent RF, audio, thermal or battery measurement | none found anywhere |
| M5Stack community forum reports | **auth-walled**; no determination possible |

## Refuted hypotheses, recorded with evidence

| Hypothesis | Refuted by | Date |
|---|---|---|
| "The ADV keyboard matrix must be different, since the scanner changed" | Same 56 switches, same `Y0..Y7` nets, same R27–R34 22 Ω, and the two drivers' coordinate maths proved algebraically equivalent | 2026-09-04 |
| "Cardputer v1.1 uses StampS3, ADV introduced Stamp-S3A" | M5Stack's own comparison table and the v1.1 page both say **v1.1 already uses Stamp-S3A**; only v1.0 uses StampS3 | 2026-09-04 |
| "The Stamp-S3A added a load switch that the StampS3 lacked" | StampS3 v0.2 **already has** a load switch (SGM2578). What changed is the *WS2812's supply net*: `VDD_3V3` → `BL_3V3` | 2026-09-04 |
| "`0x18` on the internal bus is an IMU" (per `Launcher/CardputerADV.md`) | `0x18` is `es8311_i2c_addr0` in M5Unified; the schematic prints `7-bit Address 69H` beside the BMI270 | 2026-09-04 |

## Confirmed-correct existing documentation

* [`vendors/m5stack/README.md`](../../../vendors/m5stack/README.md), written 2026-09-01 during
  the PaperMono pass, was **accurate in every particular exercised here**: server-rendered HTML,
  lowercase-slug 302s, the OSS numeric-product-id scheme, `search/suggest.json` →
  `<handle>.json`, and the warning that `_page_NN.png` renders are not universal. New product
  ids and one new trap are offered for appending in
  [`../../../scratch/m5stack-cardputer/index-fragments.md`](../../../scratch/m5stack-cardputer/index-fragments.md).

---

# 2026-09-07 — three open items closed by net tracing

Appended beneath the existing text; nothing above is altered. Poppler became available on
2026-09-07 and `pdftotext -bbox-layout` made net-level tracing of the schematic possible for the
first time. Method:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](../../../guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md).
Full trace: [`schematic-netlist.md`](schematic-netlist.md).

Each item below names the section above that it answers. All three are listed in
[`scratch/schematic-tracing/corrections-requiring-review.md`](../../../scratch/schematic-tracing/corrections-requiring-review.md).

## ✅ C2 — "Which Grove pin is SCL" → **RESOLVED. SCL = G1, SDA = G2.**

Answers **§ C2** above, which recorded *"the band-based text extraction could not bind them to
individual pins, and no page render was cropped at that location in this pass."*

Sheet 1, connector `J2` (`HY-2.0_IIC`):

| `J2` pin | Symbol pin name | Net label on the wire | Module pin | Module's printed pin name |
|---|---|---|---|---|
| 1 | `IIC_SCL` | **`GI`** @ 737.32, 366.41 | `P1.1` @ 333.50, 394.37 | **`G1`** |
| 2 | `IIC_SDA` | **`GO`** @ 738.58, 373.60 | `P1.2` @ 333.50, 401.37 | **`G2`** |
| 3 | `VCC` | — | — | 5 V, ESD `D8` `PESDNC2FD5VB` |
| 4 | `GND` | — | — | — |

The reason this resisted every earlier attempt: **the net names are the literal strings `GI` and
`GO`** — letter I, letter O — not `G1` and `G2`. Searching the text layer for "G1"/"G2" near `J2`
finds nothing. This is not a font-mapping artefact: `G0` and `G1` both occur elsewhere on the
same sheet and extract correctly. A 300 dpi crop shows the module symbol's own pin names printed
immediately beside those labels in an unmistakable digit glyph — `G1` and `G2`. It is a vendor
typo in the net names.

**M5Unified and Bruce were right; the colour-convention worry was not.** `EX SCL = GPIO_NUM_1`
and `EX SDA = GPIO_NUM_2` match the schematic exactly. The advice already given in § C2 — *"use
the library values"* — was correct, and now has a primary-evidence basis rather than a pragmatic
one.

Independent corroboration on a different M5Stack product: the Cap-Bus connector uses the same
`GI`/`GO` net names and pairs them with symbol pin names `SCL` and `SDA` respectively —
[`devices/m5stack/cap-lora-1262/schematic-netlist.md`](../cap-lora-1262/schematic-netlist.md) §1.

## ✅ U3 — "BMI270 interrupt lines" → **RESOLVED. Neither is routed.**

Answers **§ U3** above, which asked for *"a 1:1 crop of ADV sheet 3 around U7 pins 4 and 9"* and
correctly insisted on "not established" rather than "absent". It is now **absent**.

A row query across the *entire* sheet at each pin's y returns only `U7`'s own tokens:

```
python3 trace.py row <bbox> --y 167.37 --tol 4 --page 3     # INT1, U7 pin 4
  p3 x=157.00 y=167.37  PIU704     p3 x=157.53 y=164.84  4
  p3 x=176.83 y=168.44  INT1       p3 x=208.60 y=168.44  ASDX
  p3 x=229.00 y=167.37  PIU702     p3 x=229.72 y=164.84  2
```

No net label, no other component pin, no power port lies at that height anywhere on the page. The
same holds at y = 174.37 (`INT2`, pin 9) and at the four unused OIS pins (2 `ASDX`, 3 `ASCX`,
10 `OCSB`, 11 `OSDO`). By contrast pin 8's row *does* return `PIC2502`, `PIC2702`, `PIFB701/02`
and `+3.3V`, which shows the query finds connections when they exist.

**Consequence:** IMU motion-wake from deep sleep is **not possible on the ADV**. M5Unified's
polling is forced by the hardware, not a library shortcoming.

While tracing, the rest of `U7` was recovered and is worth recording:
`SDX` (14) = **G8**, `SCX` (13) = **G9**, `SDO` (1) pulled to `+3.3V` by `R43` 3.3 kΩ giving
address **0x69** — which matches the `7-bit Address 69H` the sheet prints at (196.71, 114.51) and
confirms § "Corrections" above, where `0x18` was already rejected.

## ✅ U4 — "The `+3.3V` feedback divider arithmetic does not work out" → **RESOLVED. It does.**

Answers **§ U4** above. Two separate mistakes produced the impossible 6.6 V.

**Mistake 1 — the upper resistor is `R11`, not `R12`.** `R11` is 68 kΩ at `COR11` (697.50,
214.20). `R12` is **100 kΩ** at `COR12` (236.50, 221.20) — 460 pt away on the other side of the
sheet, in an unrelated network. The § U4 note above anticipated exactly this: *"several `R`
values sit close together."*

The `U4` feedback column is unambiguous once the coordinates are read:

```
PIR1102 @ 690, 206.9  -> the +3.3V rail row (y 203.8)
PIR1101 @ 690, 228.9 -+
                      |-- FB node; U4.5 (FB) @ 640, 232.37
PIR1302 @ 691, 235.6 -+
PIR1301 @ 691, 258.2  -> GND (y 280.1)
R11 = 68KΩ (702, 222.4)      R13 = 15KΩ (702, 251.4)
```

**Mistake 2 — the printed formula belongs to a different converter.**
`Vout=1.2V*(R1/R2+1)` sits at (612.67, 157.65), directly beneath the **SY7088 boost `U2`**
(symbol y 63–135), ~86 pt above the SY8089. Applied to `U2`'s own divider — `R4` 75 kΩ / `R6`
22 kΩ — it gives 1.2 × (75/22 + 1) = **5.29 V**, which is self-consistent for the `+5VOUT` rail.
It was never the SY8089's formula.

With the correct pair, 3.3 V requires a feedback reference of
3.3 / (68/15 + 1) = **0.596 V**; a 0.6 V reference makes the design exact to 0.7 %.

⚠ **Evidence status:** the 0.596 V figure is *derived from the sheet*. **No SY8089 datasheet is
held in this repository**, so it is not read from a primary document. The second option offered
in § U4 — *"the SY8089 uses a different feedback reference than the SY7088"* — is the correct
one, and the value it needs is 0.6 V.

Also noted, and not a defect: **`U2`'s `+5VOUT` rail is designed to 5.29 V, not 5.00 V.** The
same vendor does the same thing on the DinMeter, whose SY7088 Grove rail computes to 5.38 V.
That is a deliberate idiom, not an arithmetic error — see
[`devices/m5stack/dinmeter/schematic-netlist.md`](../dinmeter/schematic-netlist.md) §3.

## New material, not a correction

- **`U9` `TCA8418RTWR` fully traced** — `INT` = G11, `SCL` = G9, `SDA` = G8, address `0x34`
  printed on the sheet, `ROW7` unconnected (7 rows × 8 columns), `R35`/`R36`/`R37` 3.3 kΩ
  pulling up `SDA`, `SCL` **and** `INT`. See [`schematic-netlist.md`](schematic-netlist.md) §4.
- **Vendor driver audited against the sheet and the register map** —
  [`driver-vs-document-audit.md`](driver-vs-document-audit.md). Six findings, all labelled active
  or inert; the driver's pin assignments and matrix size all agree with the schematic.
- **Acquisition gap exposed:** no TCA8418 datasheet is retained, so three register-semantics
  findings rest on the vendored header rather than on TI `SCPS215`.
