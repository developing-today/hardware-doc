# PaperMono — gaps, conflicts and refuted hypotheses

> Research snapshot **2026-09-01**. Nothing in this record was verified against
> physical hardware; there is no PaperMono in hand. Every behavioural claim
> elsewhere in this device record is `inferred`, `reported-working`, or read
> from vendor source — never `executed-success` on a device.

This file exists so that a later pass does not re-investigate settled questions
and does not silently resolve unsettled ones. Conflicts are recorded, not
arbitrated, except where primary evidence genuinely settles them — and those are
marked **resolved** with the artifact that did it.

## Resolved by primary evidence

### R1 — `PYG3` is an M5PM1 net *and* an M5IOE1 pin — **resolved**

An earlier pass in this session concluded the vendor's PaperMono page was
defective for saying the frontlight is driven by `PYG3_BL_PWM` "of the M5PM1",
reasoning from the Arduino libraries that `PYG` was an M5IOE1-only prefix, and
that the PaperMono-Lite page (which says `G3_WAKEin` of M5PM1) was the correct
one.

**Refuted.** Schematic sheets 2 and 4 show the two chips use the `PYG` prefix at
*opposite layers*: on the M5IOE1 it is the symbol pin name (nets are `PYB_*`);
on the M5PM1 it is the net name (pin names are `G<n>_…`). Both vendor pages are
accurate; they quote different layers. The defect is ambiguity, not error.
Full write-up and the hazard it creates:
[`pin-naming-and-the-pyg-ambiguity.md`](pin-naming-and-the-pyg-ambiguity.md).
Refuting artifact `PaperMono_SCH_V0.6.2_20260522.pdf`; date 2026-09-01.

### R2 — QIO versus DIO flash — **resolved**

The vendor PlatformIO snippet specifies `qio_opi`; the shipped factory image
reports **DIO** in its header. The schematic shows all four flash data lines
routed (`NOR_DI`, `NOR_DO`, `NOR_WP`, `NOR_HOLD`) and the `Q` in
`XM25UH128DHIQT` denotes a factory-set QE bit, so **the hardware supports QIO**.
`sdkconfig.defaults` pins no flash mode, so the DIO header is an ESP-IDF default,
not a hardware limitation. Not a defect; a build-configuration artefact.

### R3 — BMI270 interrupt polarity — **resolved against the vendor prose**

Vendor prose says the IMU interrupt is active-high. The vendor's own code
(`BMI2_INT_ACTIVE_LOW` + `WAKE_FALLING`) and the shipped binary's log string
(`PM1 shutdown, wake by BMI270 INT1 -> PM1 G4 falling edge`) both say
active-low / falling. The prose is the sole outlier and is wrong.

### R4 — download-mode control — **resolved on the balance of evidence**

The product page and specification table say the power button; the Arduino
tutorial page refers to "the reset button on the side". The schematic shows
three switches on the KEY/RGB sub-board — `S1` (`PWR_BTN`), `S2` (`G2_KEY1`),
`S3` (`G3_KEY2`) — and **no separate reset button**. The power-button reading is
correct; the Arduino page is wrong. Marked resolved but `not-tested`.

### R5 — `M5Unified#develop` requirement — **resolved, the instruction is stale**

`board_M5PaperMono = 29` is byte-identical on `master` and `develop`, and board
support ships in released tags M5Unified 0.2.21 and M5GFX 0.2.28. The
master↔develop deltas are unrelated fixes. The vendor's `#develop` pin is
unnecessary as of the snapshot date.

### R6 — the vendor product page's pin tables are accurate — **confirmed correct**

Recorded because confirming existing documentation is a result. Every GPIO,
every I²C address and every expander assignment on the product page matches the
schematic. The page has exactly two **omissions** (not errors): M5IOE1 `PYG4`
(NFC enable, which the firmware uses) and `PYG7` (`ADD_SET`). It additionally
omits USB (GPIO19/20) and UART0 (GPIO43/44), which the schematic supplies.

### R7 — RTC rail: the vendor block diagram is wrong — **resolved**

Schematic sheet 1's power-state matrix places the RX8130CE RTC on `3V3_L1`.
Sheet 4 shows its `VBAT`, `VIO`, `VDD` and `VOUT` pins all tied to one node on
**`3V3_L0`**, the always-on rail, with the `nIRQ` pull-up also to `3V3_L0`. The
IMU beside it genuinely is on `3V3_L1`. The circuit is right and the block
diagram is wrong; the RTC therefore keeps time in L0 shipping mode. Recorded in
[`power-architecture.md`](power-architecture.md). Additionally, `VBAT` tied to
`VDD` means **there is no separate backup cell**, which makes M5Unified's
`CHGEN=1` backup-charge enable a no-op. Sheet 4 also carries **drawn
no-connect markers** on the RTC's `nRSTO` and `FOUT` — positive assertions, not
omissions.

### R8 — the NFC front end *is* published — **resolved**

An earlier reading of this record assumed the NFC matching network was
undocumented because NFC schematic sheet 1 of 2 is missing. **Refuted.** Sheet 1
is genuinely absent, but the released sheet `2/2` carries the complete front
end: `ST25R3916-AQWT`, a 27.12 MHz crystal, the L/C matching bank, series
resistors, the load switch and an antenna construction note (4 turns,
25 × 25 mm, 0.25 mm trace, 0.3 mm gap, 17 µm copper). What sheet 1 contains
remains unknown. Date 2026-09-01.

### R9 — `PYB_NFC_EN` is a power cut, not a reset — **resolved**

`PYB_NFC_EN` on the main board and `PYB_RFID_RST` on the NFC sub-board are the
same wire across the `BTB0.408-10PLBDR-G41` mating pair. It drives a load-switch
enable, and the ST25R3916 **has no reset pin in any package** — so asserting it
removes power rather than resetting the device. The `_RST` half of the name is
misleading.

### R10 — the firmware's "register `0x7F`" is not a register — **resolved**

`0x7F` is the mode byte `0x40 | 0x3F`: an ST25R3916 read-register command
targeting the IC identity register at `3Fh`. `0x05` is the returned `ic_type`.
Confirmed independently from the ST datasheet's command table and from
`M5Unit-NFC`'s own `OP_READ_REGISTER` / `REG_IC_IDENTITY` constants.


### R11 — IP2315 charge-programming resistor — **resolved**

`R17` = 15 kΩ sits on `ICHGSET`; `R18` on `LED3` is `NC`. This closes half of G9.
It also **sharpens** conflict C18: 15 kΩ is not one of the values tabulated in
the IP2315 datasheet, so the resulting charge current cannot be read off the
table directly and the sheet-1 annotation `充电电流 0.5C` remains the only
statement of intent.

### R12 — the battery connector has no NTC pin — **resolved, and it corrects this record**

`J2` is a **2-contact** `CON2_SMD` carrying only `VBAT_L0` and ground. The
`100K-RNTC` thermistor is **`R15`, a mainboard part on the IP2315's `NTC` pin
(26)**. Four places in this record previously said the battery was "NTC-sensed"
at `J2`; that was **wrong** and has been corrected in `README.md`,
`pinouts-and-buses.md` and `power-architecture.md`. Whether `R15` is thermally
coupled to the cell by board layout is not established — so pack temperature
protection is, on this evidence, weaker than the earlier wording implied.

### R13 — both USB-C CC pulldowns are fitted — **resolved**

There are **two** 5.1 kΩ Rd pulldowns, `R4` on `CC1` and `R14` on `CC2`, not one.
The conclusion is unchanged (a plain 5 V sink, no PD, IP2315 CC pins
depopulated) but the earlier record named only `R14`.

### R14 — the USB-C receptacle's designator is `USB` — **resolved**

Not `U1`. The bare string `USB` is the reference designator; `TYPEC-302-BRP16SC08`
is the part number printed above the symbol. `pinouts-and-buses.md` previously
listed it as `U1` on sheet 2, which collided with the real `U1` on that sheet.
This also explains why the automated designator census missed it: the extraction
filtered on `[A-Z]+[0-9]+`, which a purely alphabetic designator cannot match.

### R15 — the "missing `N1`" is a parser artifact, not a design gap — **resolved**

An earlier reading reported `N1` missing from the designator sequence. `N`-series
designators **do not exist on this board**: `CON2_SMD` (J2's footprint label) and
`PIN1`…`PIN24` (J5's pin labels) were being mis-parsed as components. The
genuine designator gaps are **`R46`, `R48`, `R55`, `R56`, `R57`** only, absent
from every word on every sheet, and most consistent with parts deleted during
design (`R55`–`R57` being consecutive) rather than an unpublished sheet — a
missing sheet would remove a contiguous block across several prefixes, which is
not what is observed. Corrected component count: **290 placed components, 230
distinct designators.**


### R16 — an independent third party confirms this record's pin map — **corroboration, 2026-09-07**

[`ciniml/paper_name_plate`](https://github.com/ciniml/paper_name_plate) (HEAD
`7eac75dfc9`) is bare-metal Rust firmware for this board whose `DESIGN.md` was
derived independently. It agrees with this record on **every previously contested
point**:

- **`PYGn` is 1-based** — *"docs' `PYGn` = 1-based"*, and it states the 0-based
  index alongside each pin (*"IO5 (0-based index 4)"*). Confirms R1/R15.
- **Frontlight is M5PM1 GPIO3 → PWM0** — confirms R1 and the vendor page, and
  independently refutes the earlier claim that the page was defective.
- **`IO4 = NFC_EN`, `IO10 = LoRa RST`, `IO2 = LoRa ANT SW`** — the three expander
  pins this record identified as absent from the FreeInk SDK.
- LoRa SPI pin set, IP2315 bus hazard, and the SSD1677 4-gray OTP path
  (`0x1A=0x5A` + `0x22=0xD7`) all match.

Two new facts from it: recovering the panel from deep sleep **requires a hardware
reset via IOE1 IO5**, and the shared I²C bus runs **PM1/IOE1 at 100 kHz but
touch and NFC at 400 kHz**.

**It also demonstrates NFC working on this board** — a 28.9 KB ST25R3916 driver
with Type 2 Tag emulation. NFC is no longer resting on the vendor demo alone.

### C25 — SSD1677 booster parameter — **RESOLVED 2026-09-11: both are correct**

**Not a defect in either implementation.** The SSD1677 datasheet (Rev 1.0,
command table p. 24/47) defines command `0x0C` *Booster Soft-start Control* as
taking **five** data bytes `A[7:0] B[7:0] C[7:0] D[7:0] E[7:0]`, and documents
**exactly two** permitted settings:

| Setting | A | B | C | D | **E** |
|---|---|---|---|---|---|
| **Level 1** | AE | C7 | C3 | C0 | **40** |
| **Level 2** | AE | C7 | C3 | C0 | **80** |

The command *"is used to control the inrush current for the booster… **Two level
of strengths can be selected**"*. The disputed fifth byte is the strength
selector, and both observed values are tabulated.

**What each implementation sends** (both verified in source, `executed-success`):

| Implementation | Value | Level | Evidence |
|---|---|---|---|
| `m5stack/M5PaperMono-OTP-Demo` @ `c7c0255` | **`0x80`** | **Level 2** | `components/EDP_OTP_LUT_demo/src/EDP_OTP_LUT_demo.cpp:221` **and** `:336` — twice, consistently |
| `ciniml/paper_name_plate` @ `7eac75d` | **`0x40`** | **Level 1** | `src/ssd1677/mod.rs:187`, and `DESIGN.md` line 60 agrees |

Both are internally consistent. This record's earlier `0x80` came from the vendor
demo and was correct; `ciniml`'s `0x40` is equally valid and simply selects the
weaker booster soft-start.

**The sibling controllers decode this command in full; the SSD1677 does not.**
SSD1680 (Rev 0.14, p.22), SSD1681 (Rev 0.13, p.22) and SSD1683 (Rev 1.0, pp.23-24)
all document `0x0C` with a complete bit-field table — but in a **4-byte** form:

| Field | Meaning |
|---|---|
| `A/B/C bit[6:4]` | **Driving strength**, `000` = 1 (weakest) … `111` = 8 (strongest) |
| `A/B/C bit[3:0]` | **Min off-time of GDR**, `0100` = 2.6 … `1111` = 16.5 [time units] |
| `D[5:4] / [3:2] / [1:0]` | **Duration** of phases 3 / 2 / 1: `00` = 10 ms … `11` = 40 ms |

So the command is a **three-phase soft ramp of the external boost converter**:
each phase sets how hard `GDR` drives the switching MOSFET and the minimum
off-time (which caps duty cycle, hence peak inductor current), for a programmed
number of milliseconds. Start weak, get stronger — so the 47 µH inductor doesn't
slam inrush through the 2.2 Ω sense resistor into empty rail capacitors.

**Applying that decode to the SSD1677's bytes gives a partial fit:**

| Byte | Value | Strength | Min off-time | Fit |
|---|---|---|---|---|
| A | `0xAE` | 3 | 13.8 | consistent |
| B | `0xC7` | 5 | 4.6 | consistent |
| C | `0xC3` | 5 | *(`0011` = NA)* | ⚠ low nibble illegal in the 4-byte table |
| D | `0xC0` | — | — | ✗ **incompatible** — the family's duration byte requires bits 7:6 = `00`; `0xC0` sets both |

A, B and C have the *form* of per-phase soft-start bytes with a sensible
weak→strong progression (3, 5, 5). D does not fit the family's duration encoding,
and E has no counterpart at all. **The SSD1677 uses a different, undocumented
5-byte encoding** — there is no bit table anywhere in its 47 pages.

**The most likely reading of E is a one-hot strength selector** (`E[6]` = Level 1,
`E[7]` = Level 2), and there is evidence for it in the wild: **Waveshare's own
SSD1677 driver for the 3.7" panel ships `AE C7 C3 C0 C0`** — *both* bits set, a
value that appears nowhere in the datasheet (`EPD_3in7.c:204-209`, verified
directly). Under a two-value enum, `0xC0` is meaningless; under one-hot it is
coherent. **This is inferred and unverified.**

**What everyone else actually sends** — and `ciniml` is the lone outlier:

| Project | Panel | E byte |
|---|---|---|
| Waveshare `EPD_10in2b.c` | 10.2" 960×640 | `0x80` |
| Waveshare `EPD_3in7.c` | 3.7" 280×480 | **`0xC0`** (undocumented) |
| GxEPD2 `GxEPD2_426_GDEQ0426T82` | 4.26" | `0x80` |
| `osptek` vendor demo | 4.26" | `0x80` |
| `bootdsc/fastwave` (measurement-driven) | 4.26" | `0x80` |
| **`m5stack/M5PaperMono-OTP-Demo`** | PaperMono | **`0x80`** |
| **`ciniml/paper_name_plate`** | PaperMono | **`0x40`** |

`0x80` is the de-facto standard across Good Display's, Waveshare's and Seeed's own
reference code, on three different panel sizes. There is **no size correlation** —
the smallest panel gets the odd `0xC0`.

### What the booster command physically drives — added 2026-09-11

The SSD16xx application circuit explains why a *soft-start* command exists at all,
and it is more elegant than "there is a boost converter". From a Chinese
walkthrough of an SSD16xx-family panel
([CSDN `sandwich_iot`, 2021-11-04](https://blog.csdn.net/sandwich_iot/article/details/121136582)),
cross-checked against the SSD1677 datasheet's own application circuit:

**One MOSFET, driven by `GDR`, generates both supply polarities.**

| Phase | Positive rail (→ `VGH`) | Negative rail (→ `VGL`) |
|---|---|---|
| Q1 **on** | L1 current ramps linearly through sense resistor R2 to GND; C1 supplies the load | C2 discharges through D2; D2's cathode sits at **−(3.3 V + Vs)** |
| Q1 **off** | L1's back-EMF `Vs` adds to 3.3 V; D3 conducts, feeding the load and recharging C1 | C2 charges through D1 to ≈ 3.3 V + Vs |

So the positive rail is a **textbook boost** and the negative rail is a
**charge-pump inversion of the same switch node**. `RESE` closes the current-sense
loop.

The pin descriptions make the dependency chain explicit:

> `VGH` — *"positive gate drive voltage **and the supply pin for `VSH1`**"*
> `VGL` — *"negative gate drive voltage, **and supply pin for `VCOM` and `VSL`**"*

**That is the point.** You generate only two rails, and the source drivers and
`VCOM` are *derived* from them. Every pixel voltage on the panel traces back to
that single MOSFET. An inrush surge at start-up therefore disturbs **everything at
once** — which is exactly what a three-phase soft-start with per-phase drive
strength and minimum off-time exists to prevent.

This is the mechanism behind the `0x0C` fields decoded above, and it makes the
"strength" semantics concrete: the setting controls **how hard `GDR` switches Q1
into the `RESE` current limit**, per phase.

### Related voltage registers, for context

The sibling SSD1683 documents the rails that the booster feeds
([CSDN `weixin_43550576`, 2024-04-04](https://blog.csdn.net/weixin_43550576/article/details/137375815)
— the free original; see the caution below):

| Cmd | Register | Default |
|---|---|---|
| `0x03` | `VGH` gate drive | `00h`, range 10–20 V |
| `0x04` | `VSH1` / `VSH2` / `VSL` source drive | `41h` (≈15 V) / `A8h` (≈5 V) / `32h` (≈−15 V) |
| `0x2C` | `VCOM` | `00h` |

In an **external waveform** (LUT) blob, these are not written separately — they
are the **trailing bytes of the LUT array**: a 227-byte waveform payload followed
by six parameter bytes (`0x3F`, VGH, VSH1, VSH2, VSL, VCOM). That is the SSD1683
analogue of the familiar 153-byte SSD1681 LUT layout, and it means **changing a
waveform silently changes the rail voltages** unless you preserve those six bytes.

> ⚠ **Source caution.** Three CSDN articles titled *"SSD1683 driver voltage
> parameter optimisation"* are AI-generated rewrites of the single free 2024
> original cited above, two of them behind a VIP paywall. The rewrites add
> plausible-sounding claims the original does not make — e.g. that `00h`
> "corresponds to the middle value" — which could not be corroborated.
> **Cite the original, not the rewrites.**

### The negative finding stands

**Across eight retrieved CSDN documents there is not one mention of `0x0C`,
`booster`, or 软启动 (soft-start).** A search for `SSD1677` returns 69 hits, of
which exactly one is a genuine SSD1677 article; the rest match on the digit
string. The Chinese-language corpus does **not** discuss this command.

**No measurement distinguishing Level 1 from Level 2 exists in public anywhere** —
not in the datasheet, not in any driver, not in any writeup. A current probe on
VCI during the boost ramp would produce the first.

**Practical meaning** (inferred from the mechanism above, not measured). Level 2
ramps harder — rails reach operating voltage sooner, at the cost of higher inrush;
Level 1 is gentler, which matters for a weak or high-impedance supply. On a battery device
sharing rails with radios, the gentler setting is a defensible choice — and
`ciniml` also drives the panel through the M5IOE1-gated `EPD_3V3_L3B` rail, where
inrush interacts with the load switch. **Neither is "the right answer"; they are a
tuning decision.**

**How to validate on hardware** (none of this was done — no device):

1. **Scope the `EPD_3V3_L3B` rail** during panel power-up with each setting;
   compare peak inrush and settle time.
2. **Watch `BUSY`** — measure time from `0x20` Master Activation to BUSY release
   for a full refresh under each. Level 2 should reach operating voltage sooner.
3. **Vary temperature.** Booster behaviour is temperature-dependent, and the SSD1677
   has an internal sensor (`0x18 0x80`); a setting that works at room temperature
   may not at 0 °C.
4. **Check for artefacts** — insufficient boost shows as weak blacks or incomplete
   clearing, not as an error code.
5. **Low battery is the real test.** Inrush margin is worst at minimum cell
   voltage; test near the cut-off, not on a full charge.

Recorded as a **specification-permitted variation**, not a conflict. The original
entry is kept below for history.

### C25-original — SSD1677 booster parameter disagreement

`paper_name_plate`'s `DESIGN.md` gives the init as `0x0C AE C7 C3 C0 **40**`.
This record's OTP-demo analysis has `0x0C = {0xAE, 0xC7, 0xC3, 0xC0, **0x80**}`.
The fifth byte differs. One is wrong, or they derive from different sources.
**Unresolved** — check against `M5PaperMono-OTP-Demo` directly before relying on
either.

## Unresolved conflicts

### C1 — 4 grey levels versus 2

M5Stack markets "4-level greyscale" and the vendor OTP demo implements a working
four-grey mode with a distinct update-control value (`0xD7`) and a
grey-mode temperature register write (`0x1A = 0x5A`). The DKE panel manual's own
optical specification table reads `GN — 2Grey Level`, and its overview describes
1-bit black and white. Three readings are possible — a stale manual template, a
panel binned for mono with usable grey, or a marketing overstatement — and
nothing in evidence chooses between them. **Unresolved.**

### C2 — panel part number

Manual cover and mechanical drawing say `DEPG0397BBS770F3`. The
`M5PaperMono-OTP-Demo` README calls the fitted panel
`DEPG0397BBS770F3HP-XM`. The suffix is undocumented. **Unresolved.**

### C3 — SPI clock exceeds the panel's rated maximum

M5GFX drives the panel at **40 MHz**. The SSD1677 datasheet (§12.1) and the DKE
manual (p. 16) *independently* state a 20 MHz maximum write clock, and the
vendor's own OTP demo uses 20 MHz. This may or may not be a factor in the
refresh instability M5Stack itself warns about. **Unresolved, untested, and the
most likely single cause worth investigating first.**

### C4 — the M5IOE1's I²C address is not in its own manual

Everything uses `0x4F`. The M5IOE1 V1.4 manual states the range `0x6F`–`0x76` in
three places, the chip's `IO7` is genuinely wired to an `ADD_SET` divider, and
the vendor library constant is named `..._ADDR_2` with an autodetect sweeping
both ranges. **Unresolved.**

### C5 — frontlight PWM frequency below the driver's rated range

M5GFX programs the M5PM1 PWM at 5 kHz; the AW9967 datasheet specifies a
10–100 kHz dimming input. Compounded by a squared gamma curve applied in
software. **Unresolved; software-only fix if real.**

### C6 — frontlight current annotation contradicts the fitted part

The schematic note claims `Iset = 15 mA` with `Rset = 11 R`, but the fitted
`R29` is 18 Ω, giving roughly 11 mA — and the note's own arithmetic is
internally inconsistent. Annotation appears stale. **Unresolved.**

### C7 — restock timing

Vendor said "two or three months" (2026-08-22); CNX-Software reported "next
year". Both recorded, neither preferred.

### C8 — `PYB_NFC_EN` annotated "spare GPIO"

Schematic sheet 4 annotates the net as a spare GPIO while the factory firmware
uses it as the NFC enable. **Unresolved**; likely a stale annotation.

### C9 — SSD1677 mirror integrity

The M5Stack-hosted SSD1677 PDF has 46 pages but numbers itself `n/47`, and its
PDF Producer is `PDFill` rather than a Solomon Systech export. It is also marked
"Advance Information", Rev 1.0, Nov 2018. Treat as a re-processed copy of a
preliminary document. **Unresolved provenance.**

### C10 — DKE drawing note reversed

DKE's mechanical drawing note 3 reads `800 gate × 480 source`, which is provably
backwards: 800 gate lines would exceed the SSD1677's 680 gate outputs, and the
firmware configures 480 gates via `0x01 = {0xDF,0x01,0x02}`. The drawing note is
wrong; the arithmetic is in the component record.

### C11 — mislabelled firmware link

The vendor link "PaperMono Factory Reset Firmware" resolves to a record named
"PaperMono UserDemo". Same image, different label.

### C12 — M5PM1 manual internal inconsistencies

PWM0/1 versus PWM1/2 naming; NeoPixel buffer documented at `0x60` in one place
and `0x36` in another; an appendix citing pre-`SW:6` register addresses;
`SW_REV` default disagreeing with the changelog. Documented in the component
record. **Unresolved.**

## Open questions and missing evidence

### G1 — NFC schematic sheet 1 of 2 is not published

The included NFC sheet is explicitly numbered `2/2`. Sheet 1 is absent from the
released PDF. NFC front-end details not visible on sheet 6 are **undocumented,
not absent**.

### G2 — no certification identifiers exist on the vendor site

`/en/certification` returns HTTP 200 and **zero** matches for `PaperMono` and
`C153`. Verified negative.

### G3 — the product I²C address table omits this board

`/en/product_i2c_addr` returns 200 with zero matches, despite seven I²C devices.

### G4 — UiFlow2 support is advertised but undocumented

The UiFlow2 page states no required firmware version, no block list and no
limitations. Confirmed by full-text search, not a retrieval failure.

### G5 — no `Stamp-LoRa-1262` module datasheet exists anywhere located

Consequently TCXO-versus-XTAL and the semantics of `SX_ANT_SW` are unknown.
Module pins 11–13 carry pad markers but **no printed name, no net label, and no
drawn no-connect glyph** — recorded as *unlabelled*, which is not the same as
*proven no-connect*.

### G6 — three parts have no obtainable datasheet

`CN4040M000157A530001` (crystal), `LMD4737T261-AC02` (microphone) and
`RS-C1415MBAR` (RGB LED). For the latter two the only web occurrences anywhere
are M5Stack's own pages. Full search ledgers are in the component records.

### G7 — no power or battery-life figure exists

The power-state table says what is *powered*, never what it *costs*. No vendor
figure, no independent measurement, none derived here.

### G8 — DKE's OTP waveform contents are unpublished

How many of the 34 WS/TR slots are programmed, and over what temperature span,
is not documented — a silent no-refresh failure mode outside the programmed
range.

### G9 — unresolved schematic details (narrowed 2026-09-01)

Still open: `J4` pin ordering; the PDM `SELECT` net; the JW5712 `VSEL` truth
table; the `U4` (`3V3_L0`) enable net; PY32L020 QFN20 pin 1 orientation. Each is
left unfilled rather than guessed.

**Closed since first writing:** the IP2315 `ICHGSET` resistor is **`R17` = 15 kΩ**
(with `R18` = `NC` on `LED3`) — see R11 below.

### G10 — no independent technical coverage existed at the snapshot date

One hands-on video with an affiliate link; every written article traces to one
vendor blog post. Two broad passes agreed. This is a statement about 2026-09-01,
not a permanent property.

## Claims examined and rejected

| Claim | Source | Why rejected |
|---|---|---|
| Restock delayed by an e-ink driver IC shortage | widely repeated | The cited post and its full reply chain were retrieved; the reason **does not appear in them**. Hearsay. |
| "$55 with NFC and LoRa" | Liliputing | $55 is the Lite, which has neither. |
| PaperMono is the successor to / an upgrade over PaperS3 | several launch articles | Contradicted by the vendor's own specs: ~35 % fewer pixels, 4 vs 16 grey levels, 1150 vs 1800 mAh, no expansion port. A repositioning, not an upgrade. |
| "Bluetooth 5.0 LE + Mesh" | CNX-Software | Publication's inference from the SoC; not in M5Stack's specification table. |
| "Half the price of the XTEINK X4 Pro" | launch coverage | No X4 Pro price was captured, and a sealed reader versus a development board is not a like-for-like comparison. |

## Method limitations worth knowing

The schematic netlist was recovered from Altium's invisible `CO`/`PI`/`NL`
marker text in the published PDF, paired by spatial adjacency
([`tools/altium_pdf_pin_table.py`](../../../tools/altium_pdf_pin_table.py)).
This recovers **text adjacency, not electrical connectivity**: unlabelled
wire-only connections are invisible to it, and dense areas of sheet 2 produced
readings that had to be corrected by rendering the sheet and reading it. Every
pin assertion in this record was cross-checked that way or against a second
independent source (vendor firmware, vendor product page, or the DKE panel
manual's own pinout). Where only the extraction supported a claim, it is marked
`inferred`.

### C13 — M5Unified `getVoltLow()` reads the wrong RTC flag

`getVoltLow()` returns `0x1D & 0x80`, which is **`VBLF`** (backup battery low),
not **`VLF`** (bit 1: oscillation stopped, register contents invalid). After a
power-on reset `VLF=1` and `VBLF=0`, so the call returns `false` on precisely
the occasion it is used to detect. Latent rather than active, and this record's
own `features/rtc.md` previously recommended it for that purpose. Source: the
RX8130CE application manual against the M5Unified source.

### C14 — RX8130CE `BFVSEL` encoded two contradictory ways

Tables 38 and 39 of the Epson application manual encode `BFVSEL` transposed
relative to each other, in **both** revisions `ETM50E-09` and `-10`. Safety-adjacent
where a rechargeable backup cell is fitted — though on this board none is.
**Unresolved.**

### C15 — SX1262 datasheet figure text is legible but wrong

Figure fonts in the SX1261/2 datasheet carry a uniform **+31 code-point offset**:
`LoRa(R)` extracts as `-P3B¥`. Body text and tables extract cleanly. This is
exactly the glyph-offset failure the method warns about; nothing in this record
was transcribed from a figure in that document.

### C16 — Semtech mirror currency unresolved

Semtech's product page lists a datasheet dated 2025-04-07; the copy held is
Rev 2.2 (Dec 2024). The canonical download sits behind a Salesforce JS/POST
shell and three retrieval strategies failed. Status **blocked**, not "not
checked".

### C17 — arduino-esp32 version differs between sources

`M5PaperMono-UserDemo` pins arduino-esp32 **3.3.10**; `M5Stack-Arduino-Check`
shows the `m5stack_papermono` variant in **3.3.9**. Both are true statements
about different artifacts; recorded so it is not later "resolved" as an error.

### C18 — IP2315 charge current cannot be read from the datasheet table

`ICHGSET` = 15 kΩ (`R17`) is **not** a tabulated value in the IP2315 datasheet,
so the programmed charge current is not directly derivable. Sheet 1's annotation
`充电电流 0.5C` (~575 mA for the 1150 mAh cell) is the only statement of intent
and is **unverified against the part**. Unresolved.

### C19 — the NFC board-to-board halves disagree on pin numbering

The `BTB0.408-10PLBDR-G41` mating pair is numbered such that a literal 1↔1
mating would short 3V3 to GND. One half's numbering must be mirrored, but the
schematic does not say which. **Unresolved, and worth care before probing.**

### C20 — official firmware carries two disagreeing build identifiers

M5Burner's `binFileName` embeds `…-yaozhenquan-8300e309-20260806_0x00.bin`
while the `esp_app_desc_t` inside those same bytes says `c78f6c5-dirty`.
**Neither is a commit in the published `M5PaperMono-UserDemo` history.**
Unresolved.

### C21 — vendor PlatformIO block disagrees with the shipped flash map

The vendor snippet sets `board_build.partitions = default_16MB.csv`, the Arduino
stock scheme. The shipped image and both vendor `partitions.csv` files use a
three-entry layout with a single ~15 MiB `factory` app. Following the published
snippet does not reproduce the shipped partition table.

### C22 — the vendor publishes power figures for the neighbouring products, not this one

M5Stack lists consumption for the **PaperS3** (9.28 µA / 949.58 µA / 154.02 mA at
4.2 V, 0–40 °C) and the **PaperColor** (92.53 µA / 211.97 mA). The PaperMono
specification table has **no power row and no operating-temperature row**
(verified negative by full-text search). So G7's "no figure exists" is true but
incomplete: the vendor supplies the figure for the products either side of this
one, which makes the omission look deliberate rather than accidental.

### C23 — source-ID numbering diverged between two files — **RESOLVED 2026-09-02**

**Closed by giving the two files disjoint namespaces.** `acquisition/manifest.json`
now uses an **`A##`** namespace and carries a `source_id` field pointing at the
canonical `sources.md` **`S##`** row for each artifact (16 of 24 mapped; the other
8 are reference-only entries with no `sources.md` row, left `null` rather than
guessed).

This was worse than a simple offset and worth recording: the two schemes
**crossed over**. Manifest `S20` was the M5PM1 manual while `sources.md` `S20` is
the SSD1677; manifest `S22`/`S24` were the reciprocal swap of `sources.md`
`S24`/`S22`. Following an ID from one file into the other therefore landed on a
*plausible but wrong* artifact — the most dangerous kind of error, because it
does not look like one.

Renumbering the manifest to match was rejected as the fix: three other documents
cite manifest entries, and a blind renumber through a crossing-over mapping is
exactly how a silent mis-citation gets introduced. Disjoint namespaces make the
mistake structurally impossible instead.

`acquisition/fetch.py --verify-only` re-run after the change: **0 failed**.

The original defect, for the history:

### C23-original — source-ID numbering diverged between two files in this record

`acquisition/manifest.json` and `sources.md` use different `S##` numbering for
the same artifacts (schematic `S10` vs `S14`; firmware `S30`/`S31` vs
`S38`/`S39`; datasheets `S20`–`S29` vs `S18`–`S26`). Hashes, sizes and URLs agree
in both, so no artifact is ambiguous, but an ID followed from one file into the
other lands on the wrong row. **`sources.md` is canonical**; the manifest's IDs
are superseded and should be renumbered in a future pass.

### C24 — Waveshare alternative was unbacked — **RESOLVED 2026-09-01**

**Closed** by writing
[`devices/waveshare/esp32-s3-epaper-3.97`](../../waveshare/esp32-s3-epaper-3.97/README.md),
a real Waveshare **e-paper** ESP32-S3 board: same SoC, same 8 MB PSRAM / 16 MB
flash, same 3.97" 4-greyscale panel, and an active area matching the PaperMono's
DKE panel to 0.01 mm. The recommendation is now backed by an internal record.

Two things surfaced while closing it, both recorded in that record: the two
boards may well carry **the same panel** (`inferred`, not established), and
Waveshare's **MediaWiki API currently returns a PHP parse error with HTTP 200**,
which breaks the enumeration route this knowledge base's own Waveshare vendor
guide recommends.

#### Addendum, second pass 2026-09-01 — the recommendation is backed, but half of it is refuted

The Waveshare record was revisited the same day once its **schematic**, **panel
manual** and **official example repository** were located on
`docs.waveshare.com` — a host the first pass had not checked. Three findings change
what C24 should be read as saying:

1. **C24 is genuinely closed.** The recommendation now rests on a real internal
   record backed by primary design data, not on a store listing. Price **USD
   34.99–47.99** (2026-09-01), panel controller **SSD1677** — *the same controller as
   the PaperMono's own panel*, which strengthens the same-panel inference to a
   four-way match (active area, resolution, DPI, controller).

2. **But the *reason* the README gave for the recommendation is wrong for that
   board.** `README.md` recommends a Waveshare board for e-paper development **"with
   expansion"**. The Waveshare board that actually competes with a PaperMono has
   **no expansion header at all** — its complete connector census is one USB-C, three
   PH1.25-2P power/speaker JSTs, the panel FPC and a microSD socket, with every
   usable GPIO committed. On expansion it is **no better than the PaperMono**.
   See [C-WS1](../../waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws1--the-expansion-claim-is-backwards).

3. **Waveshare's expansion answer exists, at a different size.** The
   [ESP32-S3-ePaper-1.54](../../waveshare/esp32-s3-epaper-1.54/README.md) and
   [ESP32-C6-ePaper-1.54](../../waveshare/esp32-c6-epaper-1.54/README.md) both carry a
   **2 × 6, 2.54 mm header** — at **200 × 200**, i.e. 40 000 pixels against the
   PaperMono's 384 000. The honest recommendation is therefore *"a Waveshare **1.54-inch**
   e-paper board, if you will trade 90 % of the display for a header"*, which is a
   materially different piece of advice from the one the README currently gives.

**Status: resolved for the record-exists question, and the residual advice defect is
tracked as [C25](#c25--the-expansion-recommendation-is-still-imprecise) rather than
folded silently back into C24.**

A fourth finding, unrelated to the recommendation but recorded here because it came
out of the same pass: Waveshare's marketing names the board's PMIC **"TG28"**, while
the schematic and Waveshare's own firmware both say **X-Powers AXP2101**
([C-WS2](../../waveshare/esp32-s3-epaper-3.97/gaps-and-conflicts.md#c-ws2--tg28-versus-axp2101)).

### C25 — the expansion recommendation is still imprecise

`README.md`'s *when not to use* says: *"For a general e-paper development board with
expansion, prefer Inkplate or a Waveshare ESP32 e-paper board."*

C24 established that a Waveshare ESP32 e-paper board now **exists** in this knowledge
base. C25 records what remains wrong with the sentence:

- **"a Waveshare ESP32 e-paper board" is too vague to act on.** Of the seven in the
  catalogue, only the two 1.54-inch models have expansion headers, and they are
  200 × 200 devices. Pointed at the like-for-like board, a reader gets **no
  expansion** — the exact thing the sentence promised.
- **The Inkplate half remains sound.** Inkplate 5 / Gen 2 have easyC/Qwiic *and*
  broken-out GPIO *and* published KiCad sources, so for W4 they are still the better
  recommendation, and by a wider margin than before.

**Not resolved by rewriting the README sentence in this pass** — that is a
recommendation change, and the evidence for it is now written down in
[comparisons §5](comparisons-and-recommendations.md) where a reader will meet it.
Recorded so the imprecision is not lost.

The original defect, for the history:

### C24-original — this record recommended a Waveshare alternative it could not support

`README.md`'s *when not to use* suggests "prefer Inkplate or a Waveshare ESP32
e-paper board". The Inkplate half is backed by internal records; **the Waveshare
half is not** — all four Waveshare records in this knowledge base are LCD boards,
not e-paper. Recorded as an unbacked inference rather than silently deleted.
