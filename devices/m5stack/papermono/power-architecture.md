# PaperMono — power architecture

> Source: official schematic `PaperMono_SCH_V0.6.2_20260522.pdf`, sheets 1
> (block diagram / power-state matrix) and 2 (power circuits), read as rendered
> images at 200 dpi as well as by text extraction. Research snapshot 2026-09-01.
> Evidence status `executed-success` for extraction, `not-tested` for every
> current, timing and behavioural claim — nothing here was measured on hardware.

Related: [`pinouts-and-buses.md`](pinouts-and-buses.md) ·
[`components/m5stack/m5pm1`](../../../components/m5stack/m5pm1/README.md) ·
[`components/injoinic/ip2315`](../../../components/injoinic/ip2315/README.md) ·
[`components/awinic/aw9967`](../../../components/awinic/aw9967/README.md)

## Why this board has a power architecture at all

Most ESP32 boards have a regulator and a charger. The PaperMono has a
**five-state power state machine implemented in a second microcontroller**, and
that is the single most important thing to understand about the product. The
e-paper panel holds its image with no power at all, so the interesting engineering
is not in driving the display — it is in switching almost everything else off
while remaining able to wake on a touch, a button, a motion event, an RTC alarm,
a LoRa packet, an NFC field or a card insertion.

The state machine lives in the **M5PM1**, which schematic sheet 1 identifies as a
`PY32L020F15U6` — a Puya Cortex-M0+ microcontroller running M5Stack firmware,
not a fixed-function PMIC. It owns the ESP32-S3's reset and boot straps, so in
power terms the application processor is a peripheral of the power manager
rather than the other way round.

## The five power states

Sheet 1 tabulates them as columns. Names are the vendor's.

| State | Name | What is on | Wakes on |
|---|---|---|---|
| **L0** | Shipping | Charger, protection, `3V3_L0` only. M5PM1 alive. | Power button, USB insertion |
| **L1** | Standby | + `3V3_L1` — RTC and IMU powered | Power button, RTC alarm, IMU motion |
| **L2** | DeepSleep | + `3V3_L2` — ESP32-S3, touch, NFC, keys, expander | + touch, keys, NFC, LoRa |
| **L3A** | Core active | + e-paper rail `EPD_3V3_L3B` | — |
| **L3B** | All active | + frontlight `BL_15V_L3B`, microSD `TF_3V3_L3B`, microphone `PDM_VDD` | — |

The vendor's stated transitions:

- **Into L0** — the ESP32-S3 issues an I²C shutdown command to the M5PM1.
- **L0 → L1** is automatic.
- **L1 → L2** is enabled by the M5PM1 on a single power-button click, an IMU
  interrupt, or an RTC interrupt.
- **L3** switches are asserted by the ESP32-S3 through the M5IOE1.

Sheet 1's own annotation for the button behaviour is `开机` (power on) beside
`PWR_BTN`, and `唤醒` (wake) beside the L2 wake sources.

## Rails and what produces them

| Rail | Source | Enable | Feeds |
|---|---|---|---|
| `VUSB_IN` | USB-C connector | — | input only |
| `VBUS_L0` | battery bus after protection; tied to `VBAT_L0` through `R20` (0 Ω) | — | everything downstream |
| `3V3_L0` | `U4` SSP7615-33DFR LDO, 400 mA | always on | M5PM1, always-on logic |
| `3V3_L1` | `U6` SSP7615-33DFR LDO, 400 mA | `3V3_L1_EN` ← M5PM1 `LDO3V3_EN_PP` | IMU (**not** the RTC — see below) |
| `3V3_L2` | `U10` JW5712 DC-DC, 600 mA, `L2` = 2.2 µH | `3V3_L2_EN` ← M5PM1 `DCDC3V3_EN_PP` | ESP32-S3, I²C bus pull-ups, keys, NFC sub-board |
| `3V3_L2_LoRa` | `U9` SSP7615-33DFR LDO, 400 mA | `PYG2_LoRa_EN` ← **M5PM1 G2** | Stamp LoRa-1262 |
| `EPD_3V3_L3B` | `U5` SSP7615-33DFR LDO, 400 mA | `PYB_EPD_EN` ← **M5IOE1 IO3** | e-paper panel |
| `BL_15V_L3B` | `U11` AW9967 boost | `PYG3_BL_PWM` ← **M5PM1 G3**, feedback `BL_FB` | frontlight |
| `TF_3V3_L3B` | `U8` AW35122 load switch | `PYB_TF_EN` ← M5IOE1 IO14 | microSD |
| `TP_VDD` | `U18` AW35122 load switch | `PYB_TP_EN` ← M5IOE1 IO13 | touch controller |
| `PDM_VDD` | `U21` AW35122 load switch | `PYB_PDM_EN` ← M5IOE1 IO12 | PDM microphone |
| `VDD_NOR` | from `3V3_L2` domain | — | SPI NOR flash |

Each switched LDO carries a 1 MΩ pulldown on its enable (`R24`, `R26`, `R23`),
so every optional rail defaults **off** on cold power-up. That is the correct
failure mode for a battery product, and it means firmware must explicitly bring
up the panel rail before the display will respond — a blank screen is the
expected result of forgetting.

> **Naming trap.** `VBUS_L0` is *not* USB VBUS. USB 5 V is `VUSB_IN`; `VBUS_L0`
> is the internal battery/system bus, tied to `VBAT_L0` through a 0 Ω link
> (`R20`). Reading `VBUS` as "USB power" inverts the entire tree.

### The RTC is on `3V3_L0`, not `3V3_L1` — the vendor block diagram is wrong

Sheet 1's power-state matrix places both the RTC and the IMU on `3V3_L1`, i.e.
powered from state L1 upward. Reading the actual circuit on **sheet 4**
contradicts this for the RTC.

The RX8130CE (`U16`) has `VBAT` (pin 10), `VIO` (pin 1), `VDD` (pin 8) and
`VOUT` (pin 9) **all tied to the same node, and that node is `3V3_L0`** — the
always-on rail. Its `nIRQ` pull-up (`R49`, 100 kΩ) also goes to `3V3_L0`. The
IMU beside it genuinely is on `3V3_L1`.

This is architecturally the *better* arrangement — an RTC that loses power in
shipping mode would be useless — so the block diagram is the document at fault,
not the board. Evidence: sheet 4 rendered at 200 dpi and read directly;
`executed-success` for the extraction, `not-tested` electrically.

Two consequences follow:

- **The RTC keeps time in L0.** Sheet 1 implies it does not.
- **There is no separate backup cell.** `VBAT` is tied to `VDD`, so the
  RX8130CE's backup-supply input is the main rail. M5Unified's `begin()` sets
  `CHGEN=1`, enabling the backup-charge path — into a node that is already the
  supply. At best a no-op; it is not charging a coin cell, because there isn't
  one. Flagged rather than asserted as a defect: `inferred`.

Also worth recording because the method distinguishes them: `nRSTO` (pin 5) and
`FOUT` (pin 4) carry **drawn no-connect markers**. That is a positive assertion
by the designer that they are unused, not a blank cell that merely tells us
nothing.

## Charging and USB input

```
USB-C  →  AW32901FCR (OVP = 5.95 V, surge protection)  →  IP2315 charger  →  battery
                                                              ↕ I²C @ 0x75
                                                         via U3 level translator
                                                         gated by M5IOE1 IO11
```

- **`U2` AW32901FCR** sits on the USB input. Its schematic annotation reads
  `OVP = 5.95V`. This is **input over-voltage and surge protection, not battery
  protection** — a distinction worth stating because the part sits where a
  battery protector normally would.
- **`U10`… no: `U10` is the DC-DC.** The charger is the Injoinic **IP2315**,
  identifiable by its `LED1/SCL`, `LED2/SDA`, `VSYS`, `LX`, `CC1`, `CC2`, `HLED`
  and `nACOK` pins. Sheet 1 annotates the charge current as `充电电流 0.5C`
  — 0.5 C, i.e. about 575 mA for the 1150 mAh cell. `inferred` from the
  annotation and the cell capacity. The programming resistor is now resolved:
  **`R17` = 15 kΩ on `ICHGSET`** (and `R18` = `NC` on `LED3`), a value that does
  not appear in the IP2315 datasheet's tabulated set — recorded as a conflict.
- **No USB-PD.** The connector carries **both** standard 5.1 kΩ CC pulldowns
  (`R4` on CC1 **and** `R14` on CC2) that advertise a plain sink, but the **IP2315's own `CC1`/`CC2`
  sense pins are unpopulated** (`R1`, `R2` marked `NC`). Combined with the
  5.95 V OVP upstream, this is a 5 V-only input; the charger's PD capability is
  deliberately depopulated. *(Two earlier readings of this circuit disagreed —
  one saw only the `NC` resistors and concluded there were no CC resistors at
  all. Both resistor groups exist and they are on different parts.)*
- Battery connects at `J2` (`CON2_SMD`), a **2-contact** part carrying only
  `VBAT_L0` and ground. The `100K-RNTC` thermistor is **`R15` on the mainboard**,
  at the IP2315's `NTC` pin — not inside the pack. Capacity 1150 mAh, per the vendor specification.

### The charger is normally *off* the I²C bus

This is the board's sharpest design quirk and it is documented by M5Stack
themselves.

The IP2315's I²C pins must be pulled to `VBAT`, not to the 3.3 V logic rail. The
schematic solves this with **`U3`, a dual-bit bidirectional level translator**
(`VCCA`/`VCCB`/`A1`/`B1`/`A2`/`B2`/`OE`) bridging the system bus
(`G47_SYS_SDA` / `G48_SYS_SCL`) to a `VBAT`-referenced charger bus
(`CHG_SYS_SDA` / `CHG_SYS_SCL`). Its **output enable is `PYB_CHG_IIC`, driven by
M5IOE1 IO11.**

So `0x75` is only present on the bus while firmware has asserted that pin. The
vendor's guidance is to attach the charger, transact, and detach promptly,
because leaving it attached degrades bus stability — and if the battery is too
low the IP2315 may fail to enter I²C mode at all and disturb the other six
devices. The IP2315 datasheet documents a bus-lockup mechanism involving a
missing NACK on the final byte of a read, which is presumably the specific
failure being avoided.

**Consequence for anyone writing an I²C scanner:** not finding `0x75` is normal.
The vendor's documented recovery from a wedged bus is a short press of the power
button, which resets the device.

## Frontlight

The e-paper frontlight is a boost converter (`U11`, Awinic **AW9967**) producing
`BL_15V_L3B` from the L3B domain, with current feedback on `BL_FB` set by `R29`
and brightness controlled by a PWM input from **M5PM1 G3** (`PYG3_BL_PWM`).

Two independent observations about how M5Stack drives it, both worth knowing
before trusting the brightness curve:

- M5GFX programs the M5PM1's PWM at **5 kHz** (registers `0x34`/`0x35`), while
  the AW9967 datasheet specifies a **10–100 kHz** dimming input range. Below the
  specified range, dimming linearity and audible behaviour are not guaranteed.
- M5GFX applies a **squared gamma curve** to the requested brightness before
  writing the duty registers (`0x30`/`0x31`), so `setBrightness(128)` is roughly
  a quarter of full output, not half.
- The schematic's own note claims `Iset = 15 mA` at 100 % duty with
  `Rset = 11 R`, but the fitted `R29` is **18 Ω**, which gives roughly 11 mA. The
  note's arithmetic is also internally inconsistent with its own formula. Treat
  the annotation as stale.

All three are software or documentation issues rather than hardware faults, and
all three are fixable without touching the board.

## Wake sources and how they reach the M5PM1

| Source | Path | Note |
|---|---|---|
| Power button | `PWR_BTN` → M5PM1 `BTN_PU` | single press = on/reset, double press = off |
| RTC RX8130CE | `nIRQ` → `PYG0_RTC_INT` → **M5PM1 G0** | alarm/timer wake from L1 |
| IMU BMI270 | `INT1` → `PYG4_IMU_INT` → **M5PM1 G4** | motion wake from L1 |
| Touch FT6336G | `G4_TP_INT` → ESP32-S3 GPIO4 | "touch-to-wake supported" per sheet 1; wakes from L2 |
| Keys | `G2_KEY1`, `G3_KEY2` → ESP32-S3 | also listed as M5PM1 wake inputs on sheet 1 |
| LoRa, NFC, microSD insert | to ESP32-S3 | sheet 1 marks LoRa, NFC and card-detect as wake-capable |

The critical structural point is that **the RTC and IMU interrupts do not go to
the ESP32-S3 at all.** They terminate on the power manager. That is what makes
an alarm-driven or motion-driven wake possible from a state in which the
application processor has no power.

The shipped factory firmware's own log string confirms the intent and the
polarity: `PM1 shutdown, wake by BMI270 INT1 -> PM1 G4 falling edge`. Note that
the vendor's prose documentation describes this interrupt as *active-high*,
while the code (`BMI2_INT_ACTIVE_LOW` + `WAKE_FALLING`) and the shipped binary
both say active-low. The prose is the outlier.

## What is not established

- No current or battery-life figure of any kind is published, and none was
  measured. The state table says what is *powered*, not what it *costs*.
- The IP2315 charge-current programming resistor was not resolved from the
  schematic, so the 0.5 C figure rests on the sheet-1 annotation alone.
- The `U4` (`3V3_L0`) enable net could not be read with confidence; it is drawn
  as permanently enabled, but that is `inferred`.
- Whether L3A and L3B are genuinely separate switch groups or a documentation
  distinction is not clear from the schematic; the rails they name overlap.
