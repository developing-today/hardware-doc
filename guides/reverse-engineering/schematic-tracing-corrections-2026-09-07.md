# Corrections requiring review — 2026-09-07 schematic net-tracing pass

> **Provenance.** The audit trail of the 2026-09-07 schematic net-tracing pass, authored in
> `scratch/schematic-tracing/corrections-requiring-review.md` and promoted **2026-09-20**.
> Every correction listed below was verified on 2026-09-20 to have been applied, append-only,
> to the named record; this file is the consolidated index of those edits, which existed
> nowhere in the repository. Content unchanged apart from one repointed relative link.

Every change this session made to a **pre-existing** file is listed here. All were made
**append-only**: nothing above the appended section was deleted, reworded or reordered in any
file. Verification method and results are at the bottom.

Method for all of them:
[`guides/reverse-engineering/tracing-nets-from-schematic-pdfs.md`](tracing-nets-from-schematic-pdfs.md).

---

## A. Corrections — a previous claim is contradicted by the schematic

**Count: 8.**

| # | File appended to | Claim as it stood | Correction | Evidence |
|---|---|---|---|---|
| 1 | `components/unidentified/lilygo-t-display-s3-family/axpm65611/README.md` | *"the SOP-8 `TP4065` in the schematic"* | **The schematic draws a 5-pin part.** `T_Display_S3.pdf` p1 `U6` has exactly `PIU601`…`PIU605`; no `PIU606/7/8`. Pin names 1 `CHRG`, 2 `GND`, 3 `BAT`, 4 `VCC`, 5 `PROG`. Confirmed on two further sheets and by a 300 dpi render. The owner's 5-lead TSOT-23 report is **correct**; the repository's reading of the schematic was wrong. | `T_Display_S3.pdf` p1; `T-DISPLAY-S3-AMOLED.pdf` p1 `U5`; `T-Display-S3-AMOLED-Touch.pdf` p3 `U6` |
| 2 | same file | `AXPM65611` display-supply role recorded as *"the strongest hypothesis"* | **Established, not hypothesised.** 12-pin symbol: `SWP`/`SWN` two switch nodes with two 10 µH inductors, `VPOS` annotated **+4.6 V**, `VNEG` annotated **−2.2 V**, `CTRL` on net `SWIRE`. An AMOLED bipolar bias generator. Manufacturer still unknown. | `T-Display-S3-AMOLED-Touch.pdf` p3 (238.26, 474.41); `T-Display-S3-AMOLED-Plus.pdf` p3 (615.31, 171.80) |
| 3 | same file | strings A and B *"recorded together"* with a speculative link | **Refuted by pin count.** A is a 12-pin bias supply, B a 5-pin charger. They cannot be the same part. | as above |
| 4 | `components/unidentified/m5stack-stamp-s3a/dcdc-u4/README.md` | *"The `Sch_StampS3_v0.3.3.pdf` symbol carries **no part-number text**"* | **The sheet prints `JW5712`** at (193.49, 546.41), in Altium's Comment/Value position directly below the `U4` symbol, with `U4` above it at (186.67, 467.31). The sibling session's claim is confirmed **directly**, not inferentially. | `components/m5stack/stamp-s3a/artifacts/Sch_StampS3_v0.3.3-StampS3A.pdf` p1 |
| 5 | `components/unidentified/m5stack-dinmeter/rotary-encoder/README.md` | *"a **7-pad connector `J5`** … pads 6–7 present on the symbol"* | **Five pins.** `PIJ501`…`PIJ505` only; no `PIJ506`/`PIJ507` anywhere in the document; render confirms. Symbol names: 1 `b1`, 2 `b2`, 3 `A`, 4 `COM`, 5 `B`. | `K134_DIN_Meter_v1.0-schematic.pdf` |
| 6 | `components/unidentified/m5stack-dinmeter/buzzer/README.md` | *"Local bulk \| `C27` 10 µF"* | **`C27` is a series coupling capacitor in the base-drive path**, not bulk decoupling. Five tokens share y = 491.37 in x order R25.1 → R25.2 → C27.1 → C27.2 → Q5.base. `D7` clamps the base node. High-pass corner ≈ 34 Hz. | same file |
| 7 | `components/silergy/sy8089/README.md` + `devices/m5stack/cardputer-adv/{gaps-and-conflicts,pinouts-and-buses}.md` | *"R12 68 kΩ, R13 15 kΩ … gives ≈ 6.6 V, not 3.3 V"* | **The upper resistor is `R11` 68 kΩ.** `R12` is 100 kΩ at (236.50, 221.20), ~460 pt away in an unrelated network. | `Sch_M5CardputerAdv_v1.0_….pdf` p1 |
| 8 | same files | the printed `Vout=1.2V*(R1/R2+1)` treated as the SY8089's formula | **It belongs to `U2`, the SY7088 boost.** It sits at (612.67, 157.65), directly beneath that symbol (y 63–135), ~86 pt above the SY8089 (y 192–244). Applied to `R4` 75 kΩ / `R6` 22 kΩ it gives 5.29 V for `+5VOUT`. With the correct pair, the SY8089 needs **Vfb = 0.596 V**; a 0.6 V reference makes it exact. | same |

### Reviewer's note on #7 / #8

The derived 0.596 V is **inferred from the board**, not read from a datasheet. **No SY8089
datasheet is held in this repository.** The correction removes an apparent impossibility; it does
not establish the part's reference voltage from a primary source. That gap is restated in the
appended text rather than papered over.

---

## B. Resolutions — an open question closed, no prior claim contradicted

**Count: 5.**

| # | Record | Question | Resolution |
|---|---|---|---|
| 1 | `devices/m5stack/cardputer-adv/gaps-and-conflicts.md` § C2 | which Grove pin is SCL | **SCL = GPIO1, SDA = GPIO2.** `J2.1 IIC_SCL` ← net `GI` → module pin `G1`; `J2.2 IIC_SDA` ← net `GO` → `G2`. The net *names* are the literal letters `GI`/`GO` — a vendor typo — which is why every text search for "G1"/"G2" failed. Agrees with M5Unified and Bruce. Corroborated independently on the Cap-Bus. |
| 2 | same, § U3 | BMI270 `INT1`/`INT2` routing | **Neither is routed.** A full-sheet row query at y 167.37 and y 174.37 returns only `U7`'s own tokens — no label, no peer pin, no power port. The four unused OIS pins are likewise bare. IMU motion-wake from deep sleep is unavailable on this board. |
| 3 | `devices/m5stack/cap-cc1101/pinouts-and-buses.md`, `devices/m5stack/cap-lora-1262/pinouts-and-buses.md` | "pin 8 is `LoRa_RST` on U214 but `POWER_EN` on U219" | **Not a bus conflict.** Same connector (`HDR(-SMD)_14P-P2.54`), same pin number, same symbol pin name `RESET`, same host GPIO `G3` on both. The daughterboards differ in what they do with it: U214 → SX1262 `NRST`; U219 → `R1` 100 kΩ → its own `JW5712` `EN`. Driving `G3` low kills radio power on one board and merely resets it on the other. |
| 4 | `devices/m5stack/dinmeter/pinouts-and-buses.md` | Grove rail computes to 5.38 V | **Confirmed as designed, not an extraction error.** `U3` SY7088, sheet's own formula `Vout=1.2V*(R1/R2+1)` with `R16` 52.3 kΩ / `R18` 15 kΩ ⇒ **5.384 V**. The same vendor does the same on the Cardputer ADV (5.29 V). Peripherals rated 5 V ± 5 % are out of specification on this port. |
| 5 | `components/unidentified/m5stack-dinmeter/rotary-encoder/README.md` | — | **New resource conflict:** the encoder occupies GPIO41 `MTDI` and GPIO40 `MTDO`. Encoder and external JTAG cannot coexist. Not stated in the vendor header, driver or documentation. |

---

## C. Driver-versus-document defects

Recorded in `devices/m5stack/cardputer-adv/driver-vs-document-audit.md` and
`devices/m5stack/dinmeter/driver-vs-document-audit.md`. **Count: 11** (6 + 5), each labelled.

| Device | Finding | Active / inert |
|---|---|---|
| Cardputer ADV | `Adafruit_TCA8418::begin()` assigns but never tests `ret` for six of seven writes | **active**, low severity |
| Cardputer ADV | no device probe or read-back; "initialised OK" means only "last write ACKed" | inert |
| Cardputer ADV | `flush()` writes `3` to `INT_STAT`, `update()` writes `1`; `OVR_FLOW_INT` never cleared | **inert** — becomes active only if `OVR_FLOW_IEN` is ever set |
| Cardputer ADV | FIFO overflow unobservable: `KEY_LCK_EC` never read, `OVR_FLOW_M` never set, one event drained per `update()` | **active**, benign under human typing |
| Cardputer ADV | `GPI_EM_1..3 = 0xFF` enables key events on the unconnected `ROW7` | inert, fragile |
| Cardputer ADV | `attachInterruptArg(…, CHANGE)` on a level-latched active-low output | inert |
| DinMeter | `INPUT_PULLUP` in parallel with fitted 10 kΩ pull-ups | inert |
| DinMeter | hard-coded 2 000 µs settle ≈ 2.4 τ against the fitted RC (τ ≈ 0.82 ms), not the conventional 5 τ | inert, borderline |
| DinMeter | encoder consumes `MTDI`/`MTDO` — JTAG unusable with the encoder | **active**, by design, undocumented |
| DinMeter | quadrature decoder's `±2` cases guess through missed states with no error counter | inert |
| DinMeter | `M5DinMeter::begin()` has no board-specific ordering at all — nothing to compare | not a defect; stated so "no finding" is not confused with "not checked" |

**Verified agreements** (as valuable as defects, and recorded in the same files): TCA8418 `INT`
pin = GPIO11 ✅ · `matrix(7, 8)` matches the wired 7 rows ✅ · TCA8418 `INT` `pinMode(INPUT)` with
no internal pull is correct **because `R37` 3.3 kΩ is fitted** ✅ · BMI270 polled because no
interrupt exists ✅ · DinMeter encoder pins 41/40 ✅ · buzzer on GPIO3 ✅.

---

## D. Append-only verification

All ten target files are **untracked** in git (they are part of the 91-path working set), so
`git diff` cannot be used on them. Byte-prefix hashing was used instead: for each file, the first
*N* bytes — where *N* is the pre-edit size — were re-hashed after the append and compared with
the pre-edit SHA-256.

Result is recorded in the pass's scratch [`README.md`](../../archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/README.md) and re-runnable:

```bash
while read -r f; do
  old_size=...; old_hash=...
  new_prefix=$(head -c "$old_size" "$f" | sha256sum | cut -d' ' -f1)
  [ "$new_prefix" = "$old_hash" ] && echo "OK   $f" || echo "FAIL $f"
done < targets.txt
```

For tracked files the equivalent check is `git diff -- <file> | grep -c '^-[^-]'` → must print `0`.

**No pre-existing file was opened for edit that `find <file> -mmin -15` reported as recently
modified.** That check was run against all ten before any append; it returned nothing.

**Files explicitly not touched**, per the task's constraints: `README.md`, `devices/README.md`,
`components/README.md`, `vendors/README.md`, `artifact-manifest.md`, `software/README.md`,
`guides/markets/*`, and everything under `devices/xteink/`. Proposed index changes are in
[`archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md`](../../archive/guides/reverse-engineering/artifacts/schematic-tracing-2026-09-07/index-fragments.md) instead — still unapplied as of 2026-09-20.
