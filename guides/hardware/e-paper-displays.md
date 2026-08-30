# E-paper displays

> A subject guide compiled from the e-paper knowledge scattered across this library:
> [Inkplate 5 / Gen 2](../../devices/soldered-electronics/inkplate-5/README.md),
> [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md),
> [E Ink ED052TC4 / ED052TC2](../../components/e-ink/ed052tc4/README.md) and
> [TI TPS65186](../../components/texas-instruments/tps65186/README.md).
> Compiled **2026-08-30**. **No new retrieval, no hardware.**

## 0. What this guide is, and what it is not

The deep records already exist and are better than any summary. The
[ED052TC4 record](../../components/e-ink/ed052tc4/README.md) is ~700 lines of primary-sourced panel
detail; the [TPS65186 record](../../components/texas-instruments/tps65186/README.md) is ~800 lines
of decoded datasheet and driver. **This page does not duplicate them.** It does three things they
cannot:

1. Explains the **physics and the system model** once, so the two component records can stay focused
   on their own parts.
2. **Cross-links** the facts that only make sense together — the panel's temperature dependence and
   the PMIC's thermistor input are documented in two different files and the interesting finding is
   what happens *between* them.
3. States, in one place, **what is publicly establishable about E Ink panels and what is not**,
   because that boundary is the single most consequential thing about working with this technology.

Evidence labels are the repository's. Where this guide says something the deep records do not, it is
labelled **[INF]** and the reasoning is given.

> ⚠ **Everything below about the parallel-interface panels is grounded in exactly one product
> family** — Soldered's Inkplate 5 line and ZeroWriter's respin of it. Three boards, two panels, one
> driver library. Treat generalisations accordingly.

---

## 1. How an electrophoretic display actually works

An electrophoretic film is a layer of microcapsules between a transparent front electrode and a
patterned back electrode. Each capsule holds charged white and black pigment particles suspended in
a clear fluid. Apply a field across the capsule and the particles migrate; remove the field and they
stay put, because the fluid is viscous and the particles are large. **That bistability is the whole
value proposition**: a static image costs nothing to hold.

Three consequences follow immediately, and they explain essentially every quirk in the rest of this
page.

**A pixel is addressed by a sequence of pulses over time, not by a voltage.** You cannot write "grey
level 6" to an electrophoretic pixel the way you write a value to an LCD. You apply a calibrated
pattern of push, pull and rest frames, and the particles end up somewhere. That pattern is the
**waveform**, and it depends on the starting level, the target level, the film temperature *and the
panel lot* — E Ink states that a waveform file *"is specifically adjusted for a particular display
module lot"* **[DOC-EINK]**
([ED052TC4 §7.1](../../components/e-ink/ed052tc4/README.md)).

**The drive voltages are large.** Moving pigment through fluid needs tens of volts, not the 3.3 V
your MCU runs on — hence §4.

**Nothing is instantaneous.** Particle migration takes hundreds of milliseconds. Every timing figure
in §6 is a consequence of physics, not of bus bandwidth; §6.3 makes that concrete.

### 1.1 Waveforms and LUTs, concretely

A "waveform" in practice is a look-up table indexed by phase. The
[Inkplate's table for the ED052TC4](../../components/e-ink/ed052tc4/README.md) is an **8 × 9 array of
2-bit drive codes** — 8 grey levels × 9 phases — where each code means one of four things on the
wire **[SRC]**:

| 2-bit code | Meaning |
|---|---|
| `00` | **discharge** |
| `01` | **drive dark** |
| `10` | **drive light** |
| `11` | **skip** — no drive at all |

That fourth code is the key to partial update: unchanged pixels are simply never driven. The library
builds each bus byte as `LUTW[diffw] & LUTB[diffb]`, both tables defaulting to `0xFF` (all-skip),
and each bit that must move replaces its pixel's `11` with `10` or `01`.

Two structural observations from the actual tables, both **[SRC]**, both instructive:

- **The white row is all zeros.** Grey level 7 requires no drive, because the clean sequence that
  precedes every full update has already left the panel white.
- **These are absolute-target waveforms, not transition tables.** The index is the destination level
  only. That is legitimate *only because* the clean sequence resets the whole panel to a known state
  first — which is precisely why greyscale mode cannot skip the flashing (§7).

The tables the Inkplate uses are **Soldered's, not E Ink's**: hand-tuned approximations to what a
per-lot E Ink waveform file would supply, **with no temperature dimension at all**. They are the
only public waveforms for these panels.

### 1.2 What a real waveform file contains

Worth knowing because it shows exactly what the Inkplate approach is doing *without*. From E Ink's
own `800-1101 Rev01` **[DOC-EINK]** ([ED052TC4 §8.2](../../components/e-ink/ed052tc4/README.md)):
a CRC32, a file length, a **serial number**, an **FPL lot number** (the film lot this waveform was
tuned for), a mode-version byte, the **AMEPD part number**, a frame rate, and — at offset `0x19` — a
**VCOM offset**, with the instruction *"User should set the Vcom to VCOM stored in the module flash
plus the VCOM_OFFSET"*.

So E Ink's model is: **the panel carries its own VCOM in flash, and the waveform carries an offset
to it.** Hold that thought until §5.

---

## 2. Two architectures, and which one you have

This distinction decides almost everything, and getting it wrong is
[pitfall #3](../../components/e-ink/ed052tc4/README.md) in the panel record.

| | **Controller-in-panel** (small SPI modules) | **Bare panel** (parallel "DES") |
|---|---|---|
| Examples | SSD1680, UC8151, IL0373 — the Waveshare / Good Display range | `ED052TC2`, `ED052TC4`, `ED060SC4`, `ED097OC4` |
| Contains | An integrated controller with its own frame buffer, LUT registers and a `display()` command | **Row and column driver ICs only. No memory, no controller, no LUT storage** |
| Host job | Push a bitmap, send a command, wait | **Hold the framebuffer, hold the previous image, sequence every waveform phase, time the gate scan, select by temperature** — all in real time, line by line |
| Bias supply | Usually generated on the module | **External multi-rail PMIC required** (§4) |
| In this library | ZeroWriter 1 (the Raspberry Pi predecessor) used a 3.7″ SPI module | **All three documented boards** |

The library's three e-paper devices are all in the right-hand column. On an Inkplate the host is an
ESP32 **abusing its I2S1 peripheral as an LCD interface**, with four framebuffers in PSRAM —
described in [Inkplate 5 § how the e-paper interface actually works](../../devices/soldered-electronics/inkplate-5/README.md#how-the-e-paper-interface-actually-works)
and analysed at register level in [ED052TC4 §6](../../components/e-ink/ed052tc4/README.md).

### 2.1 The signals a bare panel needs

Nine, split into fast and slow groups — and *where each is driven from* is the interesting part
**[SCH]** + **[SRC]**:

| Group | Signals | Driven from, on an Inkplate |
|---|---|---|
| **Fast — source data** | `D0`–`D7`, `CL` (source shift clock), `LE` (latch), `SPH` (horizontal start) | ESP32 GPIO, **I2S1 in LCD mode, DMA-fed**; `CL`, `LE`, `SPH` bit-banged via direct `GPIO.out_w1ts` register writes |
| **Fast — gate scan** | `CKV` (gate clock) | ESP32 GPIO32, same hot loop |
| **Slow — frame control** | `SPV` (vertical start), `OE` (output enable), `GMOD` (gate mode) | **Behind the I²C expander** at `0x20` |
| Present but unused | `XON`, `THERM`, panel SPI EEPROM, `VDD_1V8`/`VDD2` | broken out to unpopulated pads (§5.2, §8.2) |

**Each byte on the data bus carries four pixels at two bits each**, which is why a line is
`WIDTH/4 + 16` bytes — 336 for the 1280-wide TC4, 256 for the 960-wide TC2.

Two structural consequences the Inkplate record draws out and that generalise:

1. **The display eats most of your GPIO.** GPIO 0, 2, 4, 5, 18, 19, 23, 25, 26, 27, 32 and 33 are
   committed — and GPIO 0 and 2 are also ESP32 **strapping pins**. This is why the slow control
   lines were pushed onto an I²C expander in the first place: it buys back eight pins for the data
   bus.
2. **Every `OE`/`GMOD`/`SPV` toggle costs an I²C transaction.** You will not bit-bang your own
   waveform sequencing at speed through that.

---

## 3. Why an external PMIC is not optional

A bare panel needs, simultaneously and in a specific order, rails your MCU cannot produce:

| Rail | Typical value | Drives | Max load (TPS65186) |
|---|---:|---|---:|
| `VPOS` | **+15.0 V** | source drivers | 120 mA |
| `VNEG` | **−15.0 V** | source drivers | 120 mA |
| `VDDH` | **+22 V** | gate drivers | **10 mA** |
| `VEE` | **−20 V** | gate drivers | **12 mA** |
| `VCOM` | **0 to −5.11 V**, panel-specific | the common back-plane | 15 mA |
| `V3P3` | +3.3 V, **switched** | panel logic *and* the `CL` clock buffer | R<sub>DS(on)</sub> 10.5 Ω |

All six from a single 3.0–6.0 V input — one Li-ion cell. Values and limits from
[TPS65186 §2](../../components/texas-instruments/tps65186/README.md) **[DOC]**.

**The gate rails are weak — 10 mA and 12 mA.** Gate lines are almost purely capacitive so that is
normally fine, but there is no headroom for a wiring error; a short on `VDDH` fails power-good
rather than failing loudly **[INF]**.

### 3.1 It is a sequencer, not a set of regulators

This is the part people underestimate. The TPS65186 is a state machine: you write the *order* you
want into registers `0x09`–`0x0C` and then trigger it with a single `PWRUP` edge. Firmware does not
enable rails individually and **must not try** — the dependencies are enforced in silicon
**[DOC]**:

- DCDC2 (`VN`) must regulate before DCDC1 (`VB`);
- DCDC1 must regulate before `VNEG`, `VCOM`, `VEE` and `VDDH`;
- **`VNEG` must regulate before `VPOS`** — and disabling `VNEG` disables `VPOS`.

So a nonsensical power-**up** order does not destroy anything: the hardware refuses, the 50 ms
power-good timeout expires, and you get a **silent no-refresh, not smoke**.

**Power-*down* is where the danger is.** TI's `DWNSEQ1` register carries a `DFCTR` bit that
multiplies the inter-strobe delays by 16, provided *"to allow the user to space out the power down of
the rails to avoid crossing during discharge"* **[DOC]**. "Crossing" means a gate rail and a source
rail passing each other on the way down, putting the TFTs into a bias combination the waveform never
intended. Soldered's driver is blunter:

```c
// its important to use this order when turning epaper on.
// using wrong order can irreparably damage epaper
```

and refuses to clock data at all if the rails are not up:

```c
// If not, skip the update (if there is no power to the epaper,
// sending data to it can damage the epaper!)
if (!einkOn()) return;
```

> **Evidence boundary, restated from the component record.** That wrong bias *destroys* panels is
> asserted by Soldered **[SRC]** and is standard integration folklore **[COM]**. **TI's datasheet
> does not say it.** What TI does establish is the dependency gating, the explicit `DFCTR` provision,
> and "active discharge" in the product title. Well-supported; not TI-documented.

### 3.2 A deviation worth knowing about

TI's reset defaults are *"the default settings support the E Ink Vizplex panel and typically do not
need to be changed"* — power-down spacing of **6 / 24 / 48 ms**. **Soldered compresses all three gaps
to 6 ms** ([TPS65186 §8.1](../../components/texas-instruments/tps65186/README.md)).

That is a deliberate deviation from vendor-recommended defaults *in exactly the direction the
datasheet warns about*. Soldered ship it in volume, so on a warm, lightly-loaded panel it is
evidently fine. But if you are chasing intermittent artefacts on a custom board, **restoring
`DWNSEQ1 = 0xE0` is a one-line experiment** and the component record flags it as the first thing to
try.

### 3.3 The interlock nobody designed on purpose, and one you should copy

Two small circuit facts from the Inkplate that are worth stealing **[SCH]**:

- **`V3P3` powers the `CL` clock buffer as well as the panel.** So when panel logic power is off, the
  pixel clock physically cannot reach the panel even if the ESP32's I2S peripheral is running. One
  register bit removes both. That is a genuinely nice interlock.
- **`WAKEUP`, `PWRUP` and `VCOM_CTRL` all carry pull-downs to ground.** On a board whose I²C expander
  has not been initialised, the PMIC therefore sits safely in SLEEP with no rails up. Preserve that
  in any respin.

And one to *not* copy: **the QFN thermal pad is `PBKG`, the die substrate at −16 V.** Soldered tie
it to `VN` over thirteen stitching pads. Grounding it — the instinctive thing to do with a thermal
pad — shorts the negative substrate. If you respin this design, do not "fix" it.

---

## 4. The most common bring-up failure

Documented plainly in [TPS65186 §4](../../components/texas-instruments/tps65186/README.md) and worth
repeating because it costs people an afternoon:

**I²C to `0x48` NACKs because `WAKEUP` is low.** There is nothing wrong with your bus. In SLEEP the
chip is electrically absent *and its registers have been reset*, so anything you wrote before
sleeping — including a sequencer configuration — is gone. This is exactly why the Inkplate driver
re-writes `UPSEQ0` and `DWNSEQ0` inside **every** `powerUp()` rather than trusting `begin()`.

The corollary is a trap in the reference code itself: `TPS65186::begin()` writes `UPSEQ0 = 0x1B`,
which asks for positive rails first and `VNEG` last — **impossible**, per the dependency gating
above. It is harmless only because `powerUp()` overwrites it with `0xE4` on every call and because
`begin()` drops `WAKEUP` again immediately, resetting the registers anyway. **It is inert by
accident, and it is the value a reader will copy. Use `0xE4`.**

---

## 5. VCOM, and why it is per-panel

`VCOM` is the bias on the panel's common back-plane. The pixel sees the *difference* between its
source-driver voltage and VCOM, so a wrong VCOM offsets every pixel's drive symmetrically. **The
right value is a property of the individual panel lot** — it comes from the manufacturing process,
not from a formula.

### 5.1 The symptoms are not a failure

This is what makes it insidious. A wrong VCOM does not produce a blank screen. It produces
**washed-out blacks, uneven background, greyscale steps compressed at one end, and ghosting that a
full refresh does not clear**. If a board displays *something* but never looks quite right, suspect
VCOM before you suspect waveforms.

### 5.2 The Inkplate cannot discover it, because the panel's EEPROM is not wired

Here is the cross-record finding that neither file states alone. The E Ink FPC brings out an SPI bus
carrying the panel's identity and its factory VCOM — `SCL`, `NCS`, `SDI`, `SDO`. On **all three**
boards in this library those four signals terminate on **unpopulated header pads and nowhere else**
**[SCH]** ([ED052TC4 §5.3](../../components/e-ink/ed052tc4/README.md),
[TPS65186 §9.6](../../components/texas-instruments/tps65186/README.md)).

Consequences:

- **Firmware cannot discover which panel it is attached to, or what VCOM that panel wants.**
- VCOM must be programmed into the PMIC's EEPROM at manufacture, or measured.
- **Swap a panel and you inherit the previous panel's calibration.**
- E Ink's "panel flash VCOM + waveform offset" model (§1.2) is simply unavailable; the Inkplate has
  one fixed number instead.

### 5.3 Three places a VCOM number can live, and only one is authoritative

| Location | Written by | Authoritative? |
|---|---|---|
| **TPS65186 internal EEPROM** | the `PROG` bit | ✅ **Yes — this is what biases the panel** |
| ESP32 EEPROM offset 0 | `setVCOM()` | ❌ a display-only cache |
| Panel FPC SPI EEPROM | the factory | ❌ **not wired** (§5.2) |

`getVCOMValue()` reads the *second* of those. On a board you did not personally program it returns
garbage or zero while the panel is biased perfectly correctly. To read the real value, read `VCOM1`
/ `VCOM2` from the PMIC while it is awake.

### 5.4 ⚠ One hundred writes. That is the entire budget.

TI's electrical characteristics: *"Max number of EEPROM writes — VCOM calibration — **100**"*
**[DOC]**. Soldered say the same in plainer words in their own example sketch: *"Do NOT run this
sketch repeatedly or 'tune' VCOM by trial-and-error. Program it once (only if needed) and leave it
unchanged."*

**Do not put `setVCOM()` in `setup()`.** A board that reprograms VCOM on every boot exhausts its
budget in a few days of development.

### 5.5 Measuring it properly is gated behind an NDA

The TPS65186 *can* measure the panel's kick-back voltage in-system: put the `VCOM` pin in its 150 MΩ
Hi-Z state, **drive the panel with the E Ink NULL waveform**, set `ACQ`, wait for `ACQC`, read the
result. TI's own instruction for step 3 is *"Refer to E Ink specification for detail"* — and that
specification is NDA-gated (§9). **This is the reason nobody outside a panel-integration programme
performs this measurement**, and it is a compact illustration of how the NDA boundary propagates
into a chip whose datasheet is entirely public.

---

## 6. Update modes and real timings

### 6.1 E Ink's own taxonomy — the authoritative version

From `800-1101 Rev01` **[DOC-EINK]**, for a **Carta panel with an E Ink-approved controller and PMIC**,
at **25 °C and an 85 Hz frame rate**
([ED052TC4 §8.1](../../components/e-ink/ed052tc4/README.md)):

| Mode | Transitions | Ghosting | Intended use | Typical |
|---|---|---|---|---:|
| **INIT** | anything → white | n/a | erase completely; use when memory does not match the optical state | **2000 ms** |
| **DU** | any grey → **black or white only** | Low | monochrome menus, text entry, pen | **260 ms** |
| **GC16** | 16 greys → 16 greys | Very low | **high-quality images — the reference full update** | **450 ms** |
| GL16 | 16 → 16 | Medium | text on white | 450 ms |
| GLR16 / GLD16 | + states 29/31 | Low | text on white, reduced flash | 450 ms |
| **A2** | black/white only | **Medium** | **fast page flipping**, animation, at reduced contrast | **120 ms** |
| DU4 | any grey → 4 greys | Medium | anti-aliased menu text | 290 ms |

> ⚠ **Applicability caveat, carried over verbatim in spirit from the panel record.** This describes
> the **AF** waveform for E Ink Carta panels driven by an approved Generation-II controller with a
> flash waveform file. **The Inkplate has none of that** — no controller, no waveform file, no
> temperature LUTs, 8 greys rather than 16. Use the table for **concepts and relative magnitudes**,
> not as specifications for the `ED052TC4`. It is nevertheless the best primary description of
> e-paper update modes obtainable outside an NDA.

Two pieces of E Ink guidance in that document explain a behaviour everyone has seen:

> *"The use of a white image in the transition from 4-bit to 1-bit images will reduce ghosting and
> improve image quality for A2 updates"* … *"It is also recommended to use a white image after a
> sequence of A2 updates"* — followed by a **GC16**.

**That is the white flash on a Kindle every few page turns. It is specified by the manufacturer, not
a bug.**

### 6.2 What the Inkplate family actually achieves

Soldered's own published figures, from `features.rst`, reproduced in the
[Inkplate 5 record](../../devices/soldered-electronics/inkplate-5/README.md#family-comparison):

| Board | Resolution | Greys | **Full refresh** | **Fast refresh** |
|---|---|---:|---:|---:|
| Inkplate 2 (colour) | 202 × 104 | – | **21 s** | – |
| Inkplate 4 TEMPERA | 600 × 600 | 8 | 0.86 s | 0.18 s |
| **Inkplate 5** | **960 × 540** | 8 | **1.02 s** | **0.12 s** |
| **Inkplate 5 V2 / Gen 2** | **1280 × 720** | 8 | **1.13 s** | **0.26 s** |
| Inkplate 6 | 800 × 600 | 8 | 1.26 s | 0.26 s |
| Inkplate 6COLOR (colour) | 600 × 448 | – | **12 s** | – |
| Inkplate 6PLUS | 1024 × 758 | 8 | 1.27 s | 0.64 s |
| Inkplate 6FLICK | 1024 × 758 | 8 | 1.55 s | 0.23 s |
| Inkplate 10 | 1200 × 825 | 8 | 1.61 s | 0.62 s |

Three readings the device record draws out, all worth internalising:

- **The Inkplate 5 is the fastest in the family** — quicker than the physically smaller Inkplate 6.
  Size is not the predictor.
- **The Gen 2 pays only 11 % more full-refresh time for 78 % more pixels** (1.02 → 1.13 s), because
  full-refresh time is dominated by **waveform duration**, not data transfer. **Fast refresh roughly
  doubles** (0.12 → 0.26 s), where transfer *is* a large fraction.
- **Colour costs enormously.** 12–21 s full refresh and **no fast-refresh mode at all**. If your
  product needs to feel responsive, colour e-paper is not a trade-off, it is a different product
  category.

For [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md), which has to keep up with
typing, **0.26 s is the number that matters** — and it is what makes the campaign's "almost no
perceptible lag" claim at least architecturally plausible.

### 6.3 Where the time actually goes

Calculated in [ED052TC4 §6.4](../../components/e-ink/ed052tc4/README.md) **[INF]** from the driver's
own constants, at the vendor's stated ~16 MHz byte clock: a 336-byte TC4 line ≈ 21 µs, so one
full-screen pass over 720 lines ≈ **15.1 ms**.

| Operation (`ED052TC4`) | Full-screen passes | Estimate |
|---|---:|---:|
| `clean()` sequence preceding every full update | **48** | ≈ 740 ms |
| 1-bit image data (3 × `LUTB`, 1 × `LUT2`, 1 × discharge) | 5 | ≈ 77 ms |
| **`display()`, 1-bit** | **53** | **≈ 0.8 s** |
| 3-bit greyscale image data (9 waveform phases) | 9 | ≈ 139 ms |
| **`display()`, 3-bit** | **58** | **≈ 0.9 s** |
| **`partialUpdate()`** | **6** | **≈ 92 ms** |
| PMIC power sequencing, per update unless `leaveOn` | — | ≈ 30–100 ms |

**The single most useful number here: roughly 90 % of a full refresh is the black-white-black-white
flashing, not the image.** That is inherent to a high-quality update (§6.1) and it is the entire
reason partial update exists.

> ⚠ **Two caveats the record insists on.** These are **calculations, not measurements**, and
> `lcd_tx_wrx2_en = 1` may halve the effective data rate relative to BCK, so the true figures could
> be up to **2× longer**. Treat as order-of-magnitude: **full ≈ 1 s, partial ≈ 0.1 s.**

**Cross-record note.** The panel record lists "measured refresh times" as its single most valuable
open contribution, while the device record already carries Soldered's own published table (§6.2).
The two are the same order of magnitude and were derived by different methods; **neither is a
measurement made here.** Logged as
[C-5 in the device comparison matrix](../markets/device-comparison-matrix.md#10-conflicts-between-records).

### 6.4 Practical mode selection on an Inkplate

The API is narrower than E Ink's taxonomy — you get two modes and a threshold:

| Call | Cost | Constraint |
|---|---|---|
| `display()` in `INKPLATE_1BIT` | ≈0.8 s, flashing | — |
| `display()` in `INKPLATE_3BIT` | ≈0.9 s, flashing | Always runs the full clean sequence first — **not optional**, see §7.2 |
| `partialUpdate()` | ≈0.1 s, no flash | **1-bit mode only.** Silently forced full every *n*th call, §7.1 |
| `clean(code, reps)` | one pass per rep | **≥ 5 s between calls** (§8) |

---

## 7. Ghosting, and why full refreshes are forced

**Ghosting** is residual optical state from a previous image, caused by pixels being left
partly-driven. It **accumulates**: a partial update touches only changed pixels, so errors in
untouched pixels are never corrected, and errors in touched pixels compound.

### 7.1 The mitigation is a hard counter

```c
uint16_t _partialUpdateLimiter = 10;    // default
...
if (_partialUpdateCounter >= _partialUpdateLimiter && _partialUpdateLimiter != 0) {
    display1b(leaveOn);                 // force a FULL update
    _partialUpdateCounter = 0;
}
```

**After 10 partial updates, the eleventh silently becomes a ~0.8 s flashing full refresh** **[SRC]**.
Tunable with `setFullUpdateThreshold(n)`; `n = 0` disables it entirely, and `partialUpdate(true)`
bypasses it once.

> ⚠ **`setFullUpdateThreshold(0)` disables ghosting mitigation.** It is tempting for a typewriter, a
> clock, or anything latency-sensitive. The cost is **cumulative image degradation with no automatic
> recovery** — you must then call `display()` yourself on some schedule. There is also a separate
> `_blockPartial` flag that forces the *next* update to be full after certain operations regardless.

### 7.2 There is a second, independent reason

The greyscale waveform is an **absolute-target** table (§1.1), valid only from a known panel state.
Partial updates leave the panel in an *unknown* state. So **a greyscale update always runs the full
clean sequence first — that is not a tuning choice and cannot be skipped.**

This is the cleanest statement of why "e-paper flashes" is not laziness on anyone's part: it is what
you get when the host has no per-transition waveform table, and the host has no per-transition
waveform table because those tables are NDA-gated (§9).

---

## 8. Temperature dependence — the gap between what exists and what is used

E Ink's model is a **temperature-indexed set of LUTs**: *"The waveform flash file contains multiple
temperature look-up-tables (LUTs)"*, and the controller selects one at update time **[DOC-EINK]**.

The Inkplate has **[SRC]** + **[SCH]**:

| | Status |
|---|---|
| A temperature sensor | ✅ the TPS65186's ADC on a **board-mounted** NTC (`R2` = `NCP18XH103F03RB`), readable as `display.readTemperature()` |
| The panel's own thermistor | ✅ brought to the connector — ❌ **unrouted**, terminates on a header pad |
| A temperature dimension in the waveform | ❌ **none. One table. All temperatures.** |

`readTemperature()` is exposed to the application and used by Soldered's own examples to *display* a
temperature. **Nothing in the display path reads it.**

**This is the sharpest cross-record finding in the library.** Three files each hold one piece: E Ink
says waveforms must be temperature-selected; the schematic shows the *better* sensor — the one
actually touching the film — sitting on an unpopulated pad while a board-mounted NTC next to the
PMIC is used instead; and the driver source shows the value is never consumed anyway. None of the
three is wrong; together they explain a behaviour nobody documents.

**Practical consequences [INF]:**

- **Cold**: refreshes settle more slowly and ghost more. **Hot**: more over-drive and flashing
  artefacts.
- **The board's own floor is −10 °C**, set by the PMIC — *warmer* than the −40 °C of the rest of the
  silicon (the [PCAL6416A](../../components/nxp/pcal6416a/README.md) goes to −40 °C). On a
  cold-weather deployment **the PMIC, not the panel and not the ESP32, is the binding component.**
- **If you deploy outdoors and see seasonal image-quality changes, this is why.** There is no library
  setting that fixes it; it would need per-temperature waveform tables that do not exist publicly.
- Even the sensor that *is* used reports the PCB next to the PMIC, not the film. Under self-heating,
  or with the board in a case and the panel exposed, those differ.

One more efficiency note: `readTemperature()` **asserts `PWRUP`**, i.e. runs a full high-voltage
power-up and power-down cycle, just to read a thermistor. STANDBY would suffice. Do not call it in a
loop.

---

## 9. Panel lifetime, burn-in and endurance

**No E Ink lifetime, update-count or image-retention figure exists publicly for these panels.** That
is not an omission in the research; it is §10.

What exists is Soldered's mitigation API **[SRC]**:

```c
void EPDDriver::burnInClean(uint8_t clear_cycles, uint16_t cycles_delay);
// each cycle: clean(1,21) clean(2,1) clean(0,12) clean(2,1)
//             clean(1,21) clean(2,1) clean(0,12) clean(2,1)
//             then delay(cycles_delay)
```

That is **68 full-screen passes per cycle**, against 48 for a normal refresh — deliberately more
aggressive black/white cycling, with a caller-specified inter-cycle delay. The `clean()`
documentation carries a hard constraint:

> *"@note Should not be used in intervals smaller than 5 seconds"*

**Why 5 seconds is not explained by anyone.** The obvious reading is thermal and charge recovery:
back-to-back full-panel drive without settling stresses the film **[INF]**.

**Practical guidance [INF], and it is the standard e-paper practice rather than a vendor figure:**
if a device shows a fixed element for long periods — a clock face, a status bar, a typewriter's
header — **invert or move it periodically**, and run `burnInClean(2, 5000)` occasionally. There is no
vendor number to calibrate that against.

---

## 10. The NDA problem, and exactly what is publicly establishable

This deserves a section of its own because much of what circulates online about E Ink panels is
guesswork presented as fact.

**E Ink's business model is NDA distribution.** The one E Ink-authored document this library holds
says so on its own first page **[DOC-EINK]**:

> *"This specification document is for use by **E Ink Corporation and their customers under
> non-disclosure agreements**."*

That is deliberate, not accidental. E Ink sells to module integrators who receive a full panel
specification, a per-lot waveform file and an applications engineer. A hobbyist reading a schematic
is not a customer. The same posture appears at
[Hynitron](../../vendors/hynitron/README.md) and Sitronix.

### 10.1 What was probed, and what came back

From [ED052TC4 §1](../../components/e-ink/ed052tc4/README.md), 2026-08-24 **[WEB]**:

| Probe | Result |
|---|---|
| `eink.com/product/ED052TC4` | HTTP 200 — but serves the **generic category page**. No per-part page exists |
| `eink.com/products` | 204 kB of marketing; a regex scan for `ED\d{3}` returned **zero part numbers**. **E Ink publishes no public part catalogue at all** |
| `panelook.com` (the database that *does* index E Ink parts) | **Slider-CAPTCHA bot block**, with and without a browser UA |
| `crystalfontz.com/product/ed052tc4` | 404 |

### 10.2 The boundary, stated once

| Publicly establishable | Not publicly establishable |
|---|---|
| ✅ Resolutions, diagonal, grey levels **as driven** — from library headers **[SRC]** and part numbers | ❌ **Pixel pitch, contrast ratio, reflectance, viewing angle** |
| ✅ **Complete connector pinouts, both variants** — recovered from open KiCad PCB netlists **[SCH]** | ❌ **Operating and storage temperature range of the panel** |
| ✅ Bias rails and their voltages — from the schematic + the TPS65186 datasheet | ❌ **Interface timing**: no setup/hold, no max `CL` frequency, no `CKV` pulse-width spec |
| ✅ Signal names, and which are fast vs slow | ❌ **Panel lifetime / update-count endurance** |
| ✅ The waveform LUTs *the Inkplate uses* **[SRC]** | ❌ **E Ink's actual waveforms** for this panel |
| ✅ That waveforms are temperature-dependent and per-lot **[DOC-EINK]** | ❌ **The correct VCOM** — per-panel-lot by construction |
| ✅ The standard update-mode taxonomy and typical times **[DOC-EINK]** — ⚠ for *a* Carta panel, not necessarily this one | ❌ **Which E Ink film generation** this is (Pearl? Carta? Carta 1.2?) |
| ✅ That on-FPC EEPROM and thermistor **exist** — four SPI pins and a `THERM` pin on the connector | ❌ What the `XON` pin does. Pulled up 10 kΩ, broken out, undriven, purpose unknown |

**The most valuable single thing in the panel record is the connector pinout**, and it exists only
because Soldered publish KiCad sources under TAPR OHL. That is the general lesson: **when the panel
vendor publishes nothing, the board vendor's open design files are the substitute** — see
[recovering netlists from vendor EDA files](../reverse-engineering/netlists-from-vendor-eda-files.md).

### 10.3 How to tell a real E Ink document from a fake one

Check for an **E Ink header and a document number** (e.g. `800-1101 Rev01`) before believing
anything in a PDF you found. The library's own copy is a **5-page excerpt** of a waveform-file format
specification obtained from a *Waveshare* product page, not from E Ink; given the NDA notice on its
own first page, its public availability is presumably unintentional. It **never names the ED052TC4**.
Any document quoting a pixel pitch or a contrast ratio for a specific E Ink part, without such a
header, is unsourced.

---

## 11. Practical guidance for driving one

### 11.1 If you are using an Inkplate-class board

**Select the right Arduino board and nothing else matters as much.** `Soldered Inkplate5`
(`ED052TC2`) vs **`Soldered Inkplate5v2`** (`ED052TC4`) sets the resolution, the waveform table
*and* the clean sequence at compile time. Choose wrong and **the library builds, runs, and displays
garbage with no error.**

```c
#include <Inkplate.h>
Inkplate display(INKPLATE_3BIT);        // or INKPLATE_1BIT

void setup() {
    display.begin();                    // expander + PMIC + framebuffers + GLUT
    display.setFullUpdateThreshold(10); // default; 0 disables the forced full refresh
    display.clearDisplay();             // clears the BUFFER only
    display.display();                  // ~0.9 s, full flashing refresh
}
```

**PSRAM is mandatory for the ED052TC4.** Four framebuffers — `DMemoryNew` 115 kB, `_partial` 115 kB,
`_pBuffer` 230 kB, `DMemory4Bit` 461 kB — total **921,600 bytes (900 KiB)**, all `ps_malloc`. It does
not fit in ESP32 internal RAM; `begin()` fails if PSRAM is absent or not enabled. **This is why every
Inkplate uses a [WROVER](../../components/espressif/esp32-wrover/README.md) and not a WROOM.**

Use `display(true)` / `partialUpdate(false, true)` — the `leaveOn` argument — to keep the PMIC rails
up between updates and save the ~30–100 ms sequencing cost, if you are updating frequently.

### 11.2 If you are writing your own firmware

**MicroPython** works, with a caveat: the pixel-pushing loop is **native C** called from Python, with
a callback into Python only to toggle the expander-hosted `SPV`, because MicroPython cannot meet the
timing otherwise. And **the MicroPython port has no `set_vcom`** — program VCOM once from Arduino
first.

**ESP-IDF**: there is no `esp_lcd` driver and **there cannot be a straightforward one**. `esp_lcd`
targets panels with controllers; this panel has none (§2). The original ESP32 also has no `LCD_CAM`
peripheral, and IDF's modern `i2s_std`/`i2s_tdm` drivers do not expose LCD mode. **Port
`UtilI2S.cpp` rather than looking for a component.** For the PMIC you write ~150 lines against
`driver/i2c_master.h`; the complete minimum-viable sequence is given in
[TPS65186 §12.3](../../components/texas-instruments/tps65186/README.md).

*(On an ESP32-S3 you would instead use `esp_lcd_panel_io_i80` with `LCD_CAM`, which is a much better
fit — but no board in this library does that. See
[display-interfaces.md](display-interfaces.md).)*

### 11.3 The single highest-value improvement over the stock driver

Five of the TPS65186's seventeen registers are **never accessed at all** by the Inkplate library, and
one of those is `INT2` — the per-rail undervoltage, `VCOMF` and end-of-conversion status register.
So **`VCOMF` (VCOM out of range, panel-protection), per-rail undervoltage and thermal events are all
invisible to the application.**

Adding a single `INT2` read after each `powerUp()` is cheap and, per the component record, is the
**highest-value improvement available over the stock driver**.

### 11.4 If you are designing a new board

- **Route the panel's `THERM` line** and the on-FPC **SPI EEPROM**. Both exist on the flex; both are
  on pads. Routing them would let firmware discover its own panel and compensate for temperature —
  the two capabilities §5 and §8 identify as missing. *(The panel thermistor's electrical
  characteristics are NDA-gated, so this is a real experiment, not a certainty.)*
- **Keep the pull-downs** on `WAKEUP`/`PWRUP`/`VCOM_CTRL` (§3.3).
- **Tie the PowerPad to `VN`, not ground** (§3.3).
- **Start from TI's default sequencer values**, not Soldered's compressed ones (§3.2).
- **Do not substitute a TPS65185.** Different pinout *and* different register map — and Inkplate
  firmware writes sequencer registers by absolute address, so a part with a different map will
  accept the writes and mis-sequence the panel.
- **Design around a panel you can actually buy.** You cannot purchase an `ED052TC4` from a
  distributor; it reaches the world bonded into a product, or as grey-market pulls.

---

## 12. Pitfalls, consolidated

Merged from [ED052TC4 §10](../../components/e-ink/ed052tc4/README.md) and
[TPS65186 §13](../../components/texas-instruments/tps65186/README.md), ordered by how much grief each
causes.

1. **Wrong Arduino board for the panel you have.** Wrong resolution, wrong waveform, wrong clean
   sequence, **no error**.
2. **Building without PSRAM enabled.** `begin()` fails on the ED052TC4.
3. **`setVCOM()` in `setup()`.** 100 EEPROM writes, ever.
4. **Trusting `getVCOMValue()`.** It reads ESP32 EEPROM, not the PMIC.
5. **I²C to the PMIC with `WAKEUP` low.** The chip is asleep and its registers are reset.
6. **Copying `UPSEQ0 = 0x1B`** out of `TPS65186::begin()`. It is backwards (§4).
7. **Expecting SPI e-paper semantics.** No controller, no panel-side framebuffer, no `display()`
   command on the wire (§2).
8. **Calling `partialUpdate()` in 3-bit mode.** Partial update is a 1-bit path only.
9. **Disabling the full-update threshold** and then being surprised by ghosting (§7.1).
10. **`clean()` or `burnInClean()` in a tight loop.** ≥ 5 s between cleans (§9).
11. **Assuming `readTemperature()` affects the image.** It does not (§8).
12. **Assuming the panel's thermistor or EEPROM is readable.** Both on unpopulated pads.
13. **Grounding the PMIC PowerPad on a respin.** It is `PBKG` at −16 V.
14. **Never reading `INT2`** (§11.3).
15. **Swapping panels between an Inkplate 5 and a Gen 2.** Different connectors — 40-way
    `AXE540127` vs 50-way `WP27D-S050VA3-R15000` — different pin counts, different waveforms. **Not
    interchangeable.**
16. **Swapping a panel and keeping the board's VCOM** (§5.2).
17. **Tuning the magic timing constants** in `vscan_start()`. No datasheet, no spare panels.
18. **Deploying below −10 °C.** Out of PMIC spec (§8).
19. **Quoting a calculated update time as measured** (§6.3).
20. **Trusting an "ED052TC4 datasheet" found online** (§10.3).

---

## 13. Open questions this library would most like closed

Ranked by value, drawn from the two component records' own lists.

| Question | Why it matters | How to close it |
|---|---|---|
| **Measured** full, greyscale and partial update times | §6.3 is arithmetic with a 2× uncertainty; §6.2 is a vendor table. Neither is a measurement | `micros()` around `display()` / `partialUpdate()` on real hardware. **The single most useful contribution to these records** |
| Does `lcd_tx_wrx2_en = 1` halve the effective byte rate? | Resolves the 2× uncertainty above | ESP32 TRM § I2S, LCD mode |
| Does the compressed `DWNSEQ1 = 0x00` power-down spacing shorten panel life? | §3.2 — a deviation from vendor defaults, shipped in volume | Instrumented A/B on real hardware |
| Which E Ink film generation is the `ED052TC4`? | Determines which public waveform literature applies at all | Unresolved; NDA |
| What is `XON` for? | Present, pulled up, broken out, undriven on all three boards | Needs the panel spec |
| Why must `clean()` calls be ≥ 5 s apart? | Asserted by Soldered, unexplained | — |
| Would per-temperature waveform tables measurably improve cold performance? | §8 | Requires LUTs that do not exist publicly |
| What VCOM does Soldered program at the factory? | Would give a starting point for a panel swap | Not published; per-lot by construction |

---

## Related

- **[E Ink ED052TC4 / ED052TC2](../../components/e-ink/ed052tc4/README.md)** — the panel record. Connector pinouts, drive codes, waveform tables, timing constants, refresh arithmetic
- **[Texas Instruments TPS65186](../../components/texas-instruments/tps65186/README.md)** — the PMIC record. Register map, sequencing, VCOM procedures, failure symptoms, an ESP-IDF recipe
- [Soldered Inkplate 5 / Gen 2](../../devices/soldered-electronics/inkplate-5/README.md) · [Inkplate 5 Gen 2](../../devices/soldered-electronics/inkplate-5-gen2/README.md) · [ZeroWriter Ink](../../devices/zerowriter/zerowriter-ink/README.md)
- [ZeroWriter 1 e-paper driver notes](../../devices/zerowriter/zerowriter-ink/zerowriter1-epaper-driver-notes.md) — a worked example of waveform-LUT tampering, on a *different* panel and controller
- [NXP PCAL6416A](../../components/nxp/pcal6416a/README.md) — carries `OE`, `GMOD`, `SPV` and every PMIC control line
- [Espressif ESP32-WROVER](../../components/espressif/esp32-wrover/README.md) — the PSRAM that makes the framebuffers possible
- [E Ink documentation-sourcing guide](../../vendors/e-ink/README.md) · [Soldered Electronics vendor guide](../../vendors/soldered-electronics/README.md)
- [Display interfaces](display-interfaces.md) — where e-paper sits among the other transports
- [Device comparison matrix](../markets/device-comparison-matrix.md) — the three e-paper devices against the other eleven

---

## Evidence boundary

**This guide contains no new research and no measurements.** Every fact is drawn from the four
records named at the top, as they stood on **2026-08-30**, and carries their evidence labels
transitively:

- **[DOC-EINK]** claims (§1.2, §6.1, §8, §10) come from a **5-page excerpt** of E Ink `800-1101
  Rev01`, obtained third-hand from a Waveshare product page, which **never names the ED052TC4**.
  Use it for concepts, not specifications.
- **[DOC]** claims about rails, sequencing and VCOM come from TI **SLVSB04A**, held locally and read
  in full. These are solid.
- **[SCH]** claims come from resolved KiCad PCB netlists of three boards — ground truth for
  connectivity, but only for *these boards*.
- **[SRC]** claims come from the Inkplate Arduino library **v11.1.4** and the MicroPython port.
- **§6.3 timings are calculated, not measured**, with an acknowledged 2× uncertainty. **§6.2 timings
  are the vendor's published figures**, not verified here.
- **Nothing in this guide has been run on hardware by anyone who wrote it.**

New to this page and therefore carrying only this page's authority: the **§10.2 establishable /
not-establishable table**, the **§8 three-file cross-record synthesis**, the **§11.4 new-board
guidance**, and the **§12 merged pitfall ordering**. All are syntheses over the linked records; where
this guide and a deep record disagree, **the deep record wins**.
