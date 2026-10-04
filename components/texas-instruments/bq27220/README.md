# Texas Instruments BQ27220 — I²C battery fuel gauge

- **Category:** single-cell Li-ion gas gauge using **CEDV** (Compensated End-of-Discharge
  Voltage) gauging. ⚠ *This line previously read "Impedance Track™" — that was wrong. Corrected
  2026-09-20 against the TRM; see [the correction note](#correction-the-bq27220-is-a-cedv-gauge-not-impedance-track--2026-09-20).*
- **Manufacturer:** Texas Instruments.
- **Research status:** ⚠ Identified from **firmware source plus an independent
  teardown BOM**. No datasheet retrieved in this session.
- **Retrieved:** 2026-09-04

The battery gauge of the **Xteink X3**, and of the LilyGo T5-S3 boards the same
SDK supports.

## 1. What is established

| Property | Value | Evidence |
|---|---|---|
| I²C address | **0x55** | FreeInk board profile; `XteinkDetect` probe |
| Bus speed used on the X3 | 400 kHz | board profile |
| **State of charge** | command register **`0x2C`** | `XteinkDetect.cpp` (`BQ27220_SOC_REG`) |
| **Voltage** | command register **`0x08`** | `XteinkDetect.cpp` (`BQ27220_VOLT_REG`) |
| Access model | **TI command registers** | `GaugeType::Bq27220` |
| **Battery-profile upload** | **NOT required** — *"TI command registers, no profile upload"* | `BoardConfig.h:474-476` |
| Companion charger | optional; `chargerAddr = 0` on the X3 (**none on this bus**) | board profile |

## 2. Why this part is the family's best battery instrumentation

Three Xteink approaches, worst to best:

| Device | Method | Failure mode |
|---|---|---|
| [X4](../../../devices/xteink/x4/features/battery-and-power.md) | Bare **ADC** on GPIO0 with a ÷2 divider | Voltage-curve estimate only; no coulomb counting; cannot see charging |
| [X4 Pro](../../../devices/xteink/x4-pro/features/battery-and-power.md), X4 Classic | [CW2017](../../cellwise/cw2017/README.md) | **Reports 0 % until an 80-byte BATINFO profile is uploaded**; no current register |
| **X3** | **BQ27220** | **No profile upload needed** *(for basic SOC/voltage reads — see the [CONFIG UPDATE caveat](#so-does-the-x3-need-a-profile-upload-or-not))*. CEDV coulomb counting |

The BQ27220 is the **least fragile of the three for a firmware author**: read
`0x2C`, get a number. That is worth knowing when choosing which Xteink to build a
project on.

## 3. Its second job: device identification

`XteinkDetect::detectXteinkVerdict()` scores the presence of three parts on the
C3 boards' secondary I²C bus (**SDA 20 / SCL 0**) to decide whether it is running
on an X3 or an X4:

| Address | Part | Probe |
|---|---|---|
| **0x55** | **BQ27220** | SoC reg `0x2C`, voltage reg `0x08` |
| 0x68 | [DS-series RTC](../../unidentified/xteink-x3-x4/rtc-ds-series/README.md) | seconds reg `0x00` |
| 0x6B | [QMI8658](../../qst/qmi8658a/README.md) | `WHO_AM_I` == `0x05` |

Finding them → **X3**. Finding nothing → **X4**. So a missing or mis-addressed
BQ27220 does not merely break the battery display — it can cause the firmware to
select the wrong board profile entirely.

## 4. Datasheet

> **Superseded — both documents were retrieved on 2026-09-11 and the TRM was mined on
> 2026-09-20.** See [*Datasheet and technical reference manual*](#datasheet-and-technical-reference-manual--retrieved-2026-09-11)
> and [*TRM extraction*](#trm-extraction--configuration-access-model-and-traps--mined-2026-09-20).
> The literature number guessed below (`SLUUBD2`) is **wrong** — it returns an unrelated TPS53317
> EVM guide. The correct number is **`SLUUBD4`** / `SLUUBD4A`. Kept for the record.

**Not retrieved.** TI publishes `BQ27220` documentation openly at
`https://www.ti.com/product/BQ27220` (technical reference manual `SLUUBD2`);
retrieval status `not-attempted` this session. Recorded as an open acquisition —
this is one of the few chips in the Xteink subject with a **genuinely public,
authoritative vendor datasheet**, and it should be fetched and hashed.

## 5. Caveats

- The two register numbers above are the only ones the Xteink firmware uses. The
  BQ27220 has a much larger command set (`Control()`, `RemainingCapacity()`,
  `StateOfHealth()`, flags) that **no Xteink firmware touches** — including
  charge/discharge flags that would give charge state without a STAT GPIO.
- **The gauge's configured chemistry and design capacity were never audited.**
  The X3's cell is 650 mAh by teardown; whether the gauge is configured for that
  is unknown. → **The TRM now gives the address and the default:** `Design Capacity`
  at **0x929F**, ROM default **3000 mAh**, readable without unsealing via
  `DesignCapacity()` (0x3C/0x3D). See
  [*What a wrong profile actually costs*](#what-a-wrong-profile-actually-costs). Still
  unverified on hardware.
- Do not assume BQ27220 register semantics from the BQ27441 or BQ27441-G1 — they
  differ. ⚠ **The TRM itself violates this in chapters 3 and 4** — see
  [*A caution about this TRM's provenance*](#a-caution-about-this-trms-provenance).

---

## Used By

### [Xteink X3](../../../devices/xteink/x3/README.md)

At **0x55** on the secondary I²C bus **SDA 20 / SCL 0 @ 400 kHz**, shared with the
[DS-series RTC](../../unidentified/xteink-x3-x4/rtc-ds-series/README.md) (0x68)
and the [QMI8658 IMU](../../qst/qmi8658a/README.md) (0x6B).
`chargerAddr = 0` — **no charger IC on this bus**, and unlike the S3 boards there
is also **no charge-STAT GPIO declared**, so how the stock firmware displays
charging state is **not established**.

Cell: **650 mAh**, connectorised, glued to the back cover (teardown). Charger:
a [TP4056-class part](../../unidentified/xteink-x3-x4/battery-charger-tp4056-class/README.md).

Corroborated independently by the Chinese teardown BOM: *"TI BQ27220 库仑计"*
(coulomb counter).

→ [`devices/xteink/x3/features/battery-and-power.md`](../../../devices/xteink/x3/features/battery-and-power.md)
→ [`devices/xteink/x3/pinouts-and-buses.md`](../../../devices/xteink/x3/pinouts-and-buses.md)

### LilyGo T5-S3 (not documented in this repository)

The same SDK pairs a BQ27220 with a BQ25896 charger at 0x6B on that board.
Recorded only to show the SDK's `chargerAddr` field has a real user.

### LilyGO T-Display K230 Kit — [`devices/lilygo/t-display-k230`](../../../devices/lilygo/t-display-k230/README.md) · *added 2026-09-07*

On the **nRF9151 keyboard base board**. I²C4: `SDA` ← `GPIO47`, `SCL` ← `GPIO46`, 7-bit address
**`0x55`**. Shares the bus with a [BQ25896](../bq25896/README.md) charger at `0x6B`, a
[TCA8418](../tca8418/README.md) at `0x34`, an [XL9555](../../xlsemi/xl9555/README.md) at a probed
address in `0x20`–`0x27`, and an [AHT20](../../asair/aht20/README.md) at `0x38`.

Cell is a **21700** in the keyboard-base compartment; the 5 V boost that powers the main unit from
it is enabled by the **nRF52840's `P0.04`**, not by the K230.

Low-battery shutdown is a **userspace policy** (`ui_hardware.c`), not a hardware cut-off: a
millivolt threshold against the gauge reading, with a confirm count and a recovery log line,
gated on BQ25896 USB-present. Defaults were tuned post-release in BSP v0.2.2 and v0.2.3.

*Source: `archive/devices/lilygo/t-display-k230/artifacts/research-scratch/index-fragments.md` §F3.*

---

## Datasheet and technical reference manual — retrieved 2026-09-11

The record above stated *"No datasheet retrieved in this session"* and that the
authoritative vendor datasheet *"should be fetched and hashed"*. **Both the
datasheet and the technical reference manual have now been fetched, validated
and retained.**

| | Datasheet | Technical Reference Manual |
|---|---|---|
| Local path | [`artifacts/bq27220-datasheet-sluscb7a-rev-a.pdf`](artifacts/bq27220-datasheet-sluscb7a-rev-a.pdf) | [`artifacts/bq27220-technical-reference-manual-sluubd4-rev-a.pdf`](artifacts/bq27220-technical-reference-manual-sluubd4-rev-a.pdf) |
| **SHA-256** | `9fffe0b632cd287c9210aa1d2e71af1816b31764c11f1b62425de3a4a7cfe5f4` | `44779f229423d649e410439d1d1a3a65026d5919cdd43112ee3a3d8d9811ead9` |
| **Bytes** | **570,379** | **2,768,446** |
| Pages | 24 | — |
| TI literature number | **`SLUSCB7A`** | **`SLUUBD4`** |
| **Revision** | **Rev. A** — *SLUSCB7A – MARCH 2016 – REVISED APRIL 2016* | **Rev. A** |
| PDF title | `bq27220 Single-Cell CEDV Fuel Gauge datasheet (Rev. A)` | `BQ27220 Technical Reference Manual (Rev. A)` |
| PDF `CreationDate` | 2025-11-11 (TI re-renders on request) | — |
| Source URL | <https://www.ti.com/lit/ds/symlink/bq27220.pdf> | <https://www.ti.com/lit/ug/sluubd4/sluubd4.pdf> |
| Source class | **primary** | **primary** |
| Redistribution status | **`restricted`** — see the note below the table | same |
| Disposition | `repository`, **unstaged** | `repository`, **unstaged** |
| Known byte-identical copy | — | `archive/devices/xteink/shared-artifacts/research-scratch/datasheets/bq27220-technical-reference-manual-sluubd4a.pdf` |

> **Redistribution corrected 2026-09-20.** This row previously read `unknown — TI literature
> carries no explicit redistribution grant`. It does carry one. The TRM's IMPORTANT NOTICE
> (p. 91) states: *"TI grants you permission to use these resources only for development of an
> application that uses the TI products described in the resource. **Other reproduction and
> display of these resources is prohibited.**"* That is an explicit limitation, so the correct
> label is `restricted`, not `unknown`. The same notice appears in the datasheet. This does not
> change the disposition — both files stay in the tree, unstaged — but it should be visible to
> whoever decides whether to stage them.

**Text-layer validated** for both against their rendered page-1 headings
(*"bq27220 Single-Cell CEDV Fuel Gauge"*, `SLUSCB7A – MARCH 2016 – REVISED APRIL
2016`; and *"BQ27220 Technical Reference Manual"*).

### A failed guess, preserved

`https://www.ti.com/lit/ug/sluubd2/sluubd2.pdf` was tried first and returned a
**valid 1,277,976-byte PDF** titled ***"Using the TPS53317AEVM-726"*** — an
evaluation-module user's guide for an entirely unrelated part. TI's `sluubdN`
literature numbers are **not** sequential within a product family, and a
successful HTTP 200 plus a `%PDF` magic number proves nothing about *which*
document you got. The file was discarded. **Read the PDF title before filing
anything from `ti.com/lit`.** The correct number is `SLUUBD4`.

### Why the TRM matters more than the datasheet here

The X3's gauge is described in this repository as *"needing no profile upload"*,
in contrast to the X4 Pro's and X4 Classic's CW2017, which reports 0 % until an
80-byte BATINFO table is written. The **CEDV** configuration model, the
`Data Memory` layout and the gauging-parameter defaults that make that true are
in the **TRM**, not the datasheet. It is now available for the next session to
audit the FreeInk `BatteryMonitor` code against.

**Used by:** [Xteink X3](../../../devices/xteink/x3/README.md).

---

## A second copy of the TRM exists in the archive, and it is the same bytes — *checked 2026-09-20*

The XTEInk research-scratch tree archived on 2026-09-20 contains
`datasheets/bq27220-technical-reference-manual-sluubd4a.pdf`, which **no repository record
cited**. It is the original fetch that produced the file above.

```
44779f229423d649e410439d1d1a3a65026d5919cdd43112ee3a3d8d9811ead9  archive/devices/xteink/shared-artifacts/research-scratch/datasheets/bq27220-technical-reference-manual-sluubd4a.pdf
44779f229423d649e410439d1d1a3a65026d5919cdd43112ee3a3d8d9811ead9  components/texas-instruments/bq27220/artifacts/bq27220-technical-reference-manual-sluubd4-rev-a.pdf
```

**Identical SHA-256, identical 2,768,446 bytes — a duplicate, not a second revision.** It was
**not moved** into `artifacts/`: it is already covered by the directory-level placeholder at
[`devices/xteink/shared-artifacts/README.md`](../../../devices/xteink/shared-artifacts/README.md),
whose locale-pinned tree digest `43841e95…` would be invalidated by removing a file from that
tree. (The archive also holds `datasheets/bq27220-datasheet-ti.pdf`, 570,379 bytes — likewise
byte-identical to `artifacts/bq27220-datasheet-sluscb7a-rev-a.pdf`, `9fffe0b6…`.)

The TRM itself, however, had been **retained and described but never mined** — the section above
ends by saying it *"is now available for the next session to audit."* That session is this one.

---

## TRM extraction — configuration, access model and traps — *mined 2026-09-20*

Source throughout: `artifacts/bq27220-technical-reference-manual-sluubd4-rev-a.pdf` —
**SLUUBD4A, APRIL 2016 – REVISED NOVEMBER 2022**, 91 pp. Page numbers are the document's own.

**Text layer validated** against the rendered cover (*"BQ27220 / Technical Reference Manual /
Literature Number: SLUUBD4A"*) and the PDF `Keywords` field (`SLUUBD4A`) before transcription.

> **Note the revision string.** The record above lists this document as *"Rev. A"* with
> literature number `SLUUBD4`. The cover and metadata both say **`SLUUBD4A`**, and the date line
> is **APRIL 2016 – REVISED NOVEMBER 2022** — six and a half years newer than the datasheet it
> sits beside (`SLUSCB7A`, MARCH 2016 – REVISED APRIL 2016). Where the two disagree, the TRM is
> the later document.

Evidence label for this entire section: **`inferred` from a primary vendor document.** Nothing
here has been exercised on an X3 or any other board by this repository. The arithmetic
cross-checks noted below are derivations *within* the document, not measurements.

### Correction: the BQ27220 is a CEDV gauge, not Impedance Track — *2026-09-20*

This record previously described the part as *"single-cell Li-ion gas gauge with Impedance
Track™"* and its method as *"Impedance Track™ coulomb counting."* **Both were wrong.**

> *"The BQ27220 device features the **Compensated End-of-Discharge Voltage (CEDV)** gauging
> algorithm, capable of gauging a maximum capacity of 32 Ah."* — §1.1, p. 9

The datasheet title already said so (*"bq27220 Single-Cell **CEDV** Fuel Gauge"*) and was quoted
verbatim in this very record, directly below the incorrect claim, without the contradiction being
noticed. Impedance Track and CEDV are **different algorithms with different configuration
requirements** — Impedance Track learns cell impedance and needs a chemistry ID; CEDV is a
voltage-compensated coulomb counter driven by an EDV curve plus an 11-point loaded-voltage table.
Advice written for one does not transfer to the other.

Corrected in §1 and §2 above. Recorded here rather than silently fixed, per the repository's rule
on refuted claims.

**Consequence for the task framing that prompted this pass:** there is no "Impedance Track
configuration that has to be programmed" on this part, because there is no Impedance Track. The
equivalent is the **CEDV profile**, described below.

### Access model — three states, not two

| State | `OperationStatus()[SEC1:SEC0]` | How reached |
|---|---|---|
| **SEALED** | `11` | `SEALED` subcommand `0x0030` |
| **UNSEALED** | `10` | unseal keys to `Control()` |
| **FULL ACCESS** | `01` | `0xFFFF` written twice to `Control()` |

*(§2.27 p. 25; §6.1 steps 1–2, p. 65)*

Three things here routinely surprise people:

1. **The part boots UNSEALED.** §3.2, p. 27: *"The default access mode of the fuel gauge is
   UNSEALED, so the system processor must send a SEALED subcommand after a gauge reset to utilize
   the data protection feature."* Sealing is opt-in and does not survive a reset unless the
   `Default Seal` bit in Operation Config B is set.
2. **UNSEALED is not enough to touch data memory.** §6.1 step 2, p. 65, is explicit:
   *"The BQ27220 boots up in UNSEAL, but **not in FULL ACCESS**. Enter FULL ACCESS to gain access
   to the Data Memory."* A host that unseals and then writes config will find its writes ignored.
3. **Calibration requires FULL ACCESS specifically** — §4.9.1 note, p. 53: *"Calibrate the gauge
   only when it is in FULL ACCESS UNSEALED mode."*

> ⚠ **Conflict — the unseal key is given twice, with two different values.**
>
> | Source | Key |
> |---|---|
> | §3.3, p. 27 | *"two identical words stored in ROM with a value of **0x8000 8000**; therefore, `Control()` should supply 0x8000 and 0x8000 (again) to unseal the part"* |
> | §6.1 step 1, p. 65 | `wr 0x00 0x14 0x04; wr 0x00 0x72 0x36` → words **0x0414** then **0x3672** |
>
> These cannot both be the default. `0x0414` / `0x3672` is TI's long-standing default
> unseal key across the bq27xxx family, and §6.1 is a worked, byte-level procedure rather than
> prose, which makes it the better evidence — but **this is not resolved here**. Try
> `0x0414`/`0x3672` first and fall back to `0x8000`/`0x8000`; confirm by reading
> `OperationStatus()[SEC]` rather than by assuming either worked. Note also that the keys *"must
> be sent consecutively, with no other data being written to the `Control()` register in
> between"* (§3.3, p. 27).

### Data memory: layout, and the fact that it is volatile

Data memory parameters live in **RAM initialized from ROM** (§3.1, p. 27). The practical
consequences are stated plainly and are the most important thing in the document:

> *"None of the data written to memory is bounded by the fuel gauge — the values are **not
> rejected** by the fuel gauge. Writing an incorrect value may result in incorrect operation due
> to firmware program interpretation of the invalid data. The written data is **not persistent**,
> so a POR does resolve the fault."* — §3.1, p. 27

So: **no range checking on writes**, and **a power-on reset wipes everything back to ROM
defaults**. The second half is the answer to "what does a gauge reset cost": §8.3.1, p. 76, step
4 — *"Use the gm.fs to program the BQ27220 RAM **every time on a power up**."* Unless OTP has
been burned, the host owns re-applying the entire configuration after every POR. There is no
"it was configured at the factory and stays configured" for the RAM path.

Addressing has two banks:

| Address range | Contents |
|---|---|
| **0x91xx – 0x92xx** | the **live, writable** RAM parameters |
| 0x40xx and 0x48xx | *"Gas Gauging (ROM Default)"* mirrors of the three ROM CEDV profiles |

Classes and subclasses in the live bank (§3.4, Table 3-2, pp. 28–44):

| Class | Subclasses |
|---|---|
| **Calibration** | Offset · Temperature · Current |
| **Configuration** | Safety · Power · Current Thresholds · Registers · Discharge · Charge · Charge Inhibit Cfg · BTP · SOC |
| **Gas Gauging** | CEDV Profile 1 · CEDV Smoothing Config · CEDV Configuration · Cycle · FD · FC · TD · TC |

Anchor values for orientation (all §3.4):

| Parameter | Address | Type | Default |
|---|---|---|---|
| `Operation Config A` | **0x9206** | H2 | **0x0484** |
| `Operation Config B` | **0x9208** | H2 | **0x1000** |
| `Smoothing Config` | 0x9271 | H1 | 0x08 |
| `Battery Low %` | 0x9251 | U2 | 700 (= 7.00 %) |
| `Near Full` | 0x926B | I2 | 200 mAh |
| `Gauging Configuration` | 0x929B | H2 | 0x102A |
| `Full Charge Capacity` | 0x929D | I2 | 3000 mAh |
| **`Design Capacity`** | **0x929F** | I2 | **3000 mAh** |
| `Design Voltage` | 0x92A3 | I2 | 3700 mV |
| CEDV coefficients `EMF`/`C0`/`R0`/`T0`/`R1`/`TC`/`C1` | 0x92A7–0x92B2 | — | 3743 / 149 / 867 / 4030 / 316 / 9 / 0 |
| `Fixed EDV0` / `EDV1` / `EDV2` | 0x92B4 / 0x92B7 / 0x92BA | I2 | 3031 / 3385 / 3501 mV |
| `Voltage 0 % DOD` … `100 % DOD` | 0x92BD – 0x92D1 | I2 ×11 | 4173 … 2713 mV |

**The X3's cell is 650 mAh by teardown. The gauge's `Design Capacity` default is 3000 mAh.**
If nothing has written 0x929F, every capacity-derived reading on that board — `RemainingCapacity()`,
`StateOfHealth()`, `TimeToEmpty()` — is scaled against a figure **4.6× too large**. This record
already flagged that *"the gauge's configured chemistry and design capacity were never audited"*;
the TRM now says exactly which address to read to settle it, and that the default is wrong for
this cell. **Still unverified on hardware.** Note that `StateOfCharge()` (0x2C), the one register
the Xteink firmware actually reads, is a *relative* percentage against FCC, which is why a wrong
`Design Capacity` can go unnoticed for a long time.

### How to write a parameter — the procedure, and a typo in it

The MAC (ManufacturerAccess) block (§2.29–2.31, p. 26):

| Address | Register | Role |
|---|---|---|
| 0x3E–0x3F | `ManufacturerAccessControl` | subcommand / DM address, **little-endian** |
| 0x40–0x5F | `MACData()` | up to 32 data bytes |
| **0x60** | **`MACDataSum()`** | checksum |
| **0x61** | **`MACDataLen()`** | length |

Checksum definition, §2.30, p. 26: *"the **complement of the sum** of the
`ManufacturerAccessControl()` and the `MACData()` bytes."* Length, §2.31: *"Subcommands that
require block data are **not executed until `MACDataSum()` and `MACDataLen()` are written
together as a word**."* So the commit is a single word write at 0x60.

The authoritative worked example is **§6.1, pp. 65–66** (changing `Design Capacity` from 3000 to
1200 mAh). Its shape: unseal → FULL ACCESS → `ENTER_CFG_UPDATE` (0x0090) → poll
`OperationStatus()` → write DM address to 0x3E/0x3F → read old checksum/length → read/modify/write
bytes at 0x40+ → write new checksum to **0x60** → write length to **0x61** → `EXIT_CFG_UPDATE`
→ re-seal.

Two details from it that are easy to get wrong:

- **Poll `0x3B`, not `0x3A`.** Steps 4 and 15 read **`0x3B`** — the *high* byte of
  `OperationStatus()` — and test **bit 2**, because `CFGUPDATE` is bit 2 of the high byte
  (§2.27 table, p. 25). Reading the low byte at 0x3A and testing bit 2 gets you `SEC1` instead.
  *"May take up to 1 second."*
- **`MACDataLen` counts two more than the bytes you wrote.** §6.1 writes 2 address bytes + 32 data
  bytes and sets length `0x24` (36). §4.6 writes 2 address bytes + 1 data byte and sets length
  `0x05`. Both are *bytes + 2*, the extra two being the checksum and length registers themselves.

> ⚠ **§4.6's worked example contains an off-by-one and will not work as written.**
>
> §4.6, p. 52, gives a four-step recipe for setting `Hibernate I` to 0:
>
> > 2. Write (hex) `21 92 00`, starting at **0x3E**.
> > 3. Write (hex) `4C 05`, starting at **0x61**.
>
> Step 3 is wrong: `0x4C` is the **checksum** and belongs at **0x60**, with `0x05` (the length)
> at 0x61. Writing both "starting at 0x61" puts the checksum in `MACDataLen` and the length one
> byte past it.
>
> Verified two ways *within the document*, so this is a derivation rather than a guess:
> 1. **Arithmetic.** Step 2 writes `0x21 0x92 0x00`. Sum = `0xB3`. Complement = **`0x4C`** —
>    exactly the first byte of step 3, and exactly what §2.30 defines `MACDataSum()` to hold.
>    The three bytes written plus 2 = **5** = `0x05`, matching `MACDataLen()`.
> 2. **The authoritative example disagrees with it.** §6.1 steps 12–13 write the checksum to
>    `0x60` and the length to `0x61`, as separate, correctly addressed writes.
>
> Use **`wr 0x60 0x4C 0x05`** (a word write at 0x60, per §2.31). The rest of §4.6 is sound, and
> its advice is worth keeping: *"Because the BQ27220 device does not support HIBERNATE mode, it
> is highly recommended to set `Hibernate I` to 0."*

### CONFIG UPDATE mode

| Subcommand | Value | Effect |
|---|---|---|
| `ENTER_CFG_UPDATE` | **0x0090** | enter; UNSEALED only (§2.2.21, p. 22) |
| `EXIT_CFG_UPDATE_REINIT` | **0x0091** | exit **and re-initialize** the gauge (§2.2.22) |
| `EXIT_CFG_UPDATE` | **0x0092** | exit **without** re-initializing (§2.2.23) |

**Gauging is suspended for the whole time you are in this mode** (§2.27, p. 25:
*"Gauge is in CONFIG UPDATE mode. Gauging is suspended."*). There is an automatic escape:
**~240 seconds (4 minutes)**, after which the gauge exits on its own (§4.6, p. 52).

> ⚠ **Conflict — how long to wait before reading the mode flag.** §2.2.21, p. 22: *"To read the
> flag, the host must wait at least **2 seconds**."* §4.6, p. 52: *"wait **1100 ms** for it to
> fully enter CONFIG UPDATE mode."* §6.1 step 4, p. 65: *"May take up to **1 second**."* Three
> figures in one document. Polling `0x3B` bit 2 until it sets — §6.1's approach — is the only one
> of the three that is robust to all of them.

### CEDV profiles — and whether the X3 needs one

**Six** `SET_PROFILE` subcommands exist, `0x0015`–`0x001A` (§2.2.13, p. 20), and they are only
accepted **in CONFIG UPDATE mode** (§4.8.1, p. 52). The split:

- **Profiles 1–3** are pre-defined in device **ROM** — usable immediately, no programming.
- **Profiles 4–6** live in **OTP** and must be burned by the customer (§4.8.1, p. 52).

Per §1.1.10, p. 14, `Learned Full Charge Capacity`, `DOD at EDV2`, `Qmax Pack` and the CEDV
coefficients are stored **separately per profile** — but *"there is only a **single OCV lookup
table**. The OCV table should be selected based on a best fit for all cell profiles."*

> ⚠ **Conflict — how many profiles are there?** §2.2.13 (p. 20) and §4.8.1 (p. 52) both imply
> **six**. §1.1.10 (p. 14) says *"each of the **four** selectable battery profiles."* And §8.3.1
> (p. 76) contradicts itself in consecutive sentences: *"The host programs the configuration/
> profile into one of the **three** available OTP areas. The BQ27220 fuel gauge has **two**
> One-Time Programmable (OTP) areas…"* before settling on **two OTP *sections*** (a Configuration
> Area and a Profile Area) holding **three** profiles. The self-consistent reading is
> **3 ROM + 3 OTP = 6 selectable, in 2 OTP sections**; the "four" and the "three available OTP
> areas" appear to be errors. Not resolved.

#### So does the X3 need a profile upload or not?

This record's framing — *"BQ27220: no profile upload needed"*, versus the CW2017 which
*"reports 0 % until an 80-byte BATINFO profile is uploaded"* — **survives, with a boundary.**

- **True, for what the Xteink firmware does.** The gauge boots on a ROM CEDV profile and returns
  a plausible `StateOfCharge()` from `0x2C` with no host configuration whatsoever. There is no
  CW2017-style "returns 0 % until you feed it a table." That is a real and material difference
  and remains the reason this is the least fragile of the three Xteink gauges.
- **Not true, if you want the numbers to be right for a 650 mAh cell.** The ROM defaults describe
  a 3000 mAh pack (`Design Capacity` 0x929F, `Full Charge Capacity` 0x929D), with EDV thresholds
  and an 11-point loaded-voltage curve to match. Getting accurate capacity out of this part means
  the full CONFIG UPDATE dance above, re-applied on every POR unless OTP is burned.

The distinction worth carrying forward: **the BQ27220 degrades to "approximately right" where the
CW2017 degrades to "zero."**

#### What a wrong profile actually costs

The equivalent of "the chem ID is wrong" on a CEDV part:

- **Nothing rejects it.** §3.1, p. 27 — values are not bounded or validated. A wrong
  `Design Capacity` is accepted silently.
- **FCC starts from a lie and only learns out of it slowly.** §1.1.10, p. 14: initial FCC is *"a
  direct copy of the data flash parameter `Learned Full Charge Capacity`"*, and initial RM/RSOC
  come from the OCV table, `DOD at EDV2` and `Qmax Pack`.
- **Recovery requires a qualified discharge**, and the bar is high (§1.1.3, p. 11): discharge from
  `RM ≥ FCC − Near Full` all the way to the EDV2 threshold with **no valid charge** (≥10 mAh)
  anywhere in between, **≤256 mAh** of self-discharge/load estimation, temperature never below
  `Low Temp`, current **≥ 3C/32** at EDV2, and no overload at EDV2. `OperationStatus()[VDQ]`
  tracks whether the current cycle still qualifies — it is set when one begins and **cleared the
  moment any disqualifying condition occurs**. On a device charged opportunistically, a qualified
  discharge may essentially never happen, so a bad FCC can persist indefinitely.
- **Initialization values TI specifies** (§1.1.10, p. 14): `Learned Full Charge Capacity` should
  be initialized to `Design Capacity mAh`, and `DOD at EDV2` to `(1 − Battery_Low%) × 16384`.
- **`Qmax Pack`** (§1.1.12, p. 15) should come from the cell manufacturer's datasheet × parallel
  cell count — not measured, not guessed.

### Status registers, decoded

**`BatteryStatus()` — 0x0A (low) / 0x0B (high)** (§2.7, Table 2-6, p. 23):

| Bit | Name | Meaning |
|---:|---|---|
| 15 | `FD` | full discharge detected |
| 14 | `OCVCOMP` | OCV measurement complete |
| 13 | `OCVFAIL` | OCV read failed due to current |
| 12 | `SLEEP` | in SLEEP mode (clears briefly during SLEEP-mode A/D measurements) |
| 11 | `OTC` | overtemperature in charge |
| 10 | `OTD` | overtemperature in discharge |
| 9 | `FC` | full charge detected |
| 8 | `CHGINH` | charge inhibit — `Temperature()` outside the Charge Inhibit window |
| 7 | *reserved* | |
| 6 | `TCA` | terminate-charge alarm |
| 5 | `OCVGD` | good OCV measurement taken |
| 4 | `AUTH_GD` | inserted battery detected |
| **3** | **`BATTPRES`** | **battery present** |
| 2 | `TDA` | terminate-discharge alarm |
| 1 | `SYSDWN` | system should shut down |
| **0** | **`DSG`** | **in DISCHARGE mode when set; CHARGING or RELAXATION when clear** |

**`OperationStatus()` — 0x3A (low) / 0x3B (high)** (§2.27, Table 2-7, p. 25):

| Bit | Name | Meaning |
|---:|---|---|
| **10** | **`CFGUPDATE`** | in CONFIG UPDATE mode, gauging suspended — **bit 2 of the byte at 0x3B** |
| 7 | `BTPINT` | battery-trip-point threshold crossed |
| 6 | `SMTH` | `RemainingCapacity()` currently scaled by the smoothing engine |
| 5 | `INITCOMP` | gauge initialization complete — *"can only be set with battery presence"* |
| 4 | `VDQ` | current discharge cycle still qualifies for an FCC update |
| 3 | `EDV2` | cell voltage below the EDV2 threshold |
| **2–1** | **`SEC1:SEC0`** | **11 sealed · 10 unsealed · 01 full access** |
| 0 | `CALMD` | calibration mode, toggled by `CAL_TOGGLE` (0x002D) |

**`DSG` means different things in the two registers.** §1.1.11, p. 15, is explicit: the `[DSG]`
flag in the `GaugingStatus()` subcommand (0x0056) *"is set in both RELAXATION and DISCHARGE
modes"*, whereas *"the `[DSG]` flag in `BatteryStatus()` … sets only in DISCHARGE mode and not in
RELAXATION mode."* Same name, two registers, two meanings — a trap for anyone porting a driver.

**This record previously noted that no Xteink firmware reads any flags**, and that charge state
would otherwise need a STAT GPIO. `BatteryStatus()` bit 0 is the register that would have
supplied it, from a single word read at 0x0A, with no extra pin. The X3 declares no charge-STAT
GPIO and has no charger on the bus (`chargerAddr = 0`), so this is the available path.

### I²C — the constraints that bear on the X3's 400 kHz bus

§5.1–5.4, pp. 63–64:

| Constraint | Value |
|---|---|
| 7-bit address | **fixed at `1010101` = 0x55**, not strappable (§5.1) |
| 8-bit write / read | 0xAA / 0xAB |
| Reads above **0x6B** | **NACKed** |
| Writes to a read-only address | NACK after the data byte |
| **Bus-free time `t(BUF)` between packets** | **≥ 66 μs** (§5.3) |
| **If `fSCL` > 100 kHz** | ⚠ *"use **individual 1-byte write commands** for proper data flow control"* (§5.3) |
| Read-write standard command | **≥ 2 s** before the result is updated |
| Read-only standard commands | no wait, but **≤ 2 polls per second** or the watchdog resets the gauge |
| `DF_CHECKSUM()` subcommand | ≥ 100 ms before reading the result |
| Clock stretching, NORMAL/INITIALIZATION | **up to 4 ms** within a packet |
| Clock stretching, SLEEP | ≤ 100 μs on all traffic (device must wake to process) |
| Bus held low for **2 s** | I²C engine releases SDA and SCL; if something external holds them, it enters SLEEP |

Three of these land directly on the X3, which runs this bus at **400 kHz**:

1. **Multi-byte writes are not supported at 400 kHz.** Above 100 kHz the TRM requires one-byte
   writes. The §6.1 procedure offers both a *"two-byte incremental method"* and an
   *"alternative single byte method"* precisely for this reason — at 400 kHz, only the
   single-byte form is sanctioned.
2. **A 4 ms clock stretch is legal.** Any host I²C timeout shorter than that will intermittently
   fail against a healthy gauge. This matters on the X3's shared bus, where the
   [DS-series RTC](../../unidentified/xteink-x3-x4/rtc-ds-series/README.md) and
   [QMI8658](../../qst/qmi8658a/README.md) share SDA 20 / SCL 0 — a 4 ms stretch by the gauge
   stalls the other two as well.
3. **Do not poll faster than 2 Hz.** Exceeding it is documented to cause a **watchdog reset of
   the gauge**, which per §3.1 discards all RAM configuration. A tight battery-display loop is
   therefore not merely wasteful; it can silently reset the part.

The `t(BUF) ≥ 66 μs` figure is from the §5.3 body text. **The accompanying figures label the same
interval "66ms"** — an inconsistency in the document; the text is taken as authoritative here.

### Board-level parameters the TRM pins down

From the overview, p. 9:

| Item | Value |
|---|---|
| Sense resistor | **5 mΩ to 20 mΩ typical**, between system VSS and PACK− |
| External thermistor | NTC, **R25 = 10.0 kΩ ±1 %, B25/85 = 3435 ±1 %** (e.g. Semitec NTC 103AT) |
| Temperature source | external NTC, internal sensor, or **host-written** — selected by `Operation Config A[TEMPS]` / `[WRTEMP]` |
| Max gaugeable capacity | 32 Ah (§1.1) |

`Operation Config A` default **0x0484** decodes (§4.1.2, pp. 45–46) to: `TEMPS = 0` → **internal**
temperature sensor; `BATG_EN = 0` → BAT_GD disabled; `SLEEP = 1` → SLEEP permitted;
`BIEnable = 1` → battery insertion detected via the TS pin rather than host `BAT_INSERT()`;
`WAKE_EN = 1`; `PFC = 00`.

> **A typo worth knowing about, since it makes the default look wrong.** Table 4-2 (p. 45) prints
> *"Default 0x04"* under **both** bytes, which would give 0x0404 — but the bit row beneath the low
> byte reads `1 0 0 0 0 1 0 0` = **0x84**, and the Data Memory Table (§3.4) gives the register's
> default as **0x0484**. Two sources against one: the low-byte default is **0x84**. If you program
> 0x0404 you will clear `BIEnable` and `WAKE_EN` without meaning to.

Also note §4.1.2: `WRTEMP` carries the parenthetical *"(May not be fully implemented.)"* — TI's
own hedge on host-written temperature. Treat that path as unproven.

### Unresolved and not verified

- **The unseal key** — §3.3 and §6.1 disagree (above). Not resolved.
- **Profile count** — six vs four vs "three OTP areas" (above). Not resolved.
- **`Smoothing Config` (0x9271) default** — Table 4-1 (p. 45) shows an all-zero bit row and
  labels the default `0x00`, its prose says `SMOOTHEOC_EN` is *"1 (default)"*, and §3.4 gives
  `0x08`. Three values. The bit row was also mangled by `pdftotext` (the `SMOOTHEOC_EN` label
  wrapped across lines), so **bit positions in Table 4-1 were not transcribed** and should be
  read from the rendered page before use.
- **`Operation Config B` bit positions** — same extraction problem (the `Default Seal` label
  wraps). The default `0x1000` and the meaning of `Default Seal` (*"0 = No Seal after POR
  (default)"*, consistent with §3.2) are recorded; the exact bit index of `NR` is **inferred**
  from `0x10` and not confirmed.
- **Everything about the X3's actual gauge contents.** No register on a physical X3 has been read
  by this repository. `Design Capacity` (0x929F), `Learned Full Charge Capacity`, the selected
  profile and the `SEC` bits are all **unknown on hardware**.
- **A `DEVICE_NUMBER` discrepancy.** §2.2.2 (p. 19) states the subcommand returns **`0x0220`**.
  The worked example seven lines earlier (p. 19) shows a readback of `0x01 0x00 0x20 0x03` —
  little-endian **`0x0320`**, which is the *bq27320*. The example appears to have been carried
  over from another part's manual. **Expect `0x0220` from a BQ27220**; if you get `0x0320` you are
  talking to a different chip, not reading it wrong.

### A caution about this TRM's provenance

This record already warned: *"Do not assume BQ27220 register semantics from the BQ27441 or
BQ27441-G1 — they differ."* **The TRM itself does not consistently honour that**, which is worth
knowing before trusting any single sentence in it:

- **§4.6 (p. 52)** names the subcommands `SET_CFGUPDATE`, `EXIT_CFGUPMODE` and `EXIT_RESIM`, and
  the status bits `Flags()[CFGUPMODE]` and `[ITPOR]`. **The BQ27220 has no `Flags()` register and
  no `ITPOR` bit.** Chapter 2 of the same document names these `ENTER_CFG_UPDATE` (0x0090),
  `EXIT_CFG_UPDATE_REINIT` (0x0091) and `EXIT_CFG_UPDATE` (0x0092), with `CFGUPDATE` living in
  `OperationStatus()`. The §4.6 vocabulary is bq27421/bq27441 family.
- **§3.1 (p. 27)** describes access via `BlockDataControl()` (0x61), `BlockData()` (0x40–0x5F) and
  `BlockDataChecksum()` (0x60) — the older bq27xxx naming — and refers the reader to
  *"Chapter 5, Extended Data Commands."* **Chapter 5 of this document is "Communications."**
  There is no "Extended Data Commands" chapter. Chapter 2 names those same addresses
  `MACDataLen()`, `MACData()` and `MACDataSum()`.
- **§2.2.24 (p. 22)** instructs the reader to write to `ManufacturerAccess()` — again not a
  BQ27220 register name.
- **§2.2.2 (p. 19)**, the `0x0320` readback above.

**Chapters 2, 5 and 6 are internally consistent and read as native BQ27220 material; chapters 3
and 4 carry inherited text.** Where they conflict, prefer chapter 2 for register definitions and
**§6.1 for procedure** — it is the only end-to-end sequence in the document written at the byte
level, and it is the one that survives arithmetic checking. This is the documented failure mode of
*"a datasheet derived by editing another part's document"*, visible here in TI's own TRM.

### Pointers for the next session

- Audit the FreeInk `BatteryMonitor` / `XteinkDetect` code against §2 of the TRM — in particular
  whether anything ever writes `Design Capacity`, and whether the SOC read loop respects the
  **2 Hz** polling ceiling and tolerates a **4 ms** clock stretch.
- On hardware: read `OperationStatus()` (0x3A/0x3B) for the `SEC` bits, and `DesignCapacity()`
  (0x3C/0x3D) — a plain, always-readable standard command needing neither unseal nor FULL ACCESS.
  **If it returns 3000, the gauge is running ROM defaults against a 650 mAh cell.** That single
  two-byte read settles the largest open question in this record.

**Used by:** [Xteink X3](../../../devices/xteink/x3/README.md) ·
LilyGO T-Display K230 keyboard base ·
LilyGo T5-S3 (not documented here).
