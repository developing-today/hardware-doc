# Power rail and Grove pass-through — Cap LoRa-1262 (U214)

Snapshot 2026-09-04, schematic V1.1. Nothing measured.

## 1. Rail

| Item | Value | Evidence |
|---|---|---|
| Input | **5 V** from the Cap-Bus (pin 5 `5V_OUT` from host, pin 7 `5V_IN` to host) | **[SCH]**, **[DOC]** |
| Regulator | **`U3` JW5712** synchronous buck | **[SCH]** |
| Output | `VDD_3V3`, sheet annotation **`IOUT: 0~0.6 A`** | **[SCH]** |
| Inductor | `L2` = `WPN201610U2R2MT`, 2.2 µH | **[SCH]** |
| Input caps | `C1` 1 nF, `C2`/`C3`/`C4` 22 µF | **[SCH]** |
| Output caps | `C15` 22 µF, `C12` 470 µF, `C16`/`C17` 100 nF | **[SCH]** |
| Feedback/mode straps | `VSEL1` (C1), `VSEL2` (D1), `VSEL3` (D2) on the JW5712's chip-scale package | **[SCH]** |
| **Enable** | `R1` **10 kΩ** adjacent to `ENB` and to the `+5V`/`+5VOUT` labels | **[SCH]**; polarity **`inferred`, not traced** |

**There is no host power-enable pin on this Cap.** Cap-Bus pin 8 — which the sibling
[Cap CC1101](../../cap-cc1101/features/power-and-grove.md) uses as `POWER_EN` — is
`LoRa_RST` here. So the practical model is: *if the host is powering the EXT connector, the
Cap is on.* Anything wanting to cut GNSS/LoRa power entirely has to do it on the host side.

> ⚠ Honest limit on that claim: the `ENB` net was **not** traced end-to-end through the PDF
> text layer. What is established is that a 10 kΩ resistor sits between the `+5V`/`+5VOUT`
> labels and the regulator's `ENB` pin, and that no Cap-Bus pin carries an enable signal.
> The conclusion "always on" follows from those two facts; it is `inferred`.

## 2. Consumers of `VDD_3V3`

| Load | Notes |
|---|---|
| `M1` Stamp LoRa-1262 Mini (pin 5) | dominant during TX at +22 dBm |
| `M2` ATGM336H-6N `VCC` (pin 8) via `FB3` 120 Ω/MB | |
| `M2` `VCC_RF` (pin 14) via `FB2` 120 Ω/MB | separate ferrite for the RF section |
| `U1` MAX2659 LNA | always on — `SHDN` is tied |
| `U2` PI4IOE5V6408 | µA-class |

The two ferrite beads are worth noticing: M5Stack isolates the GNSS digital supply and the
GNSS RF supply from each other and from the LoRa module's rail. That is the conventional
mitigation for LoRa TX transients desensitising a co-located GNSS front end. Whether it is
*sufficient* on this board — a +22 dBm transmitter roughly 40 mm from a GNSS patch — is
**not** measured by anyone.

## 3. Grove pass-through (`J2`, HY2.0-4P)

| Grove wire | Colour | Net | Host |
|---|---|---|---|
| 1 | Black | `GND` | — |
| 2 | Red | `5V` (`+5VOUT`) | host 5 V |
| 3 | Yellow | `SDA` | **G8** |
| 4 | White | `SCL` | **G9** |

`R3` = 10 kΩ pull-up. **This is the *same* I²C bus the Cap's own expander sits on**, and the
same bus as the host's keyboard controller (TCA8418), IMU (BMI270) and audio codec (ES8311).

Consequences worth stating plainly:

- **This port is not a free extra bus.** It is a tap onto a busy shared one.
- **A Grove device at 0x43 will break the antenna switch** and, worse, will be
  *mis-detected as the Cap itself* by both M5Stack's and Meshtastic's probe
  ([`io-expander-and-rf-switch.md` §4](io-expander-and-rf-switch.md)).
- The predecessor **Cap LoRa868 (U201) has no Grove port at all** — adding it is one of the
  four differences M5Stack lists between the two.
- Community context: the Grove-port + Cap combination is a recurring source of confusion.
  See *"Multiple grove addons at once?"*
  ([r/CardPuter 2026-08-07](https://old.reddit.com/r/CardPuter/comments/1vifzzz/), 17
  comments) and u/newbie20250's report that an RFID2 unit worked on the Cardputer-Adv's own
  Grove port but not through the Cap
  ([r/M5Stack 2026-04-01](https://old.reddit.com/r/M5Stack/comments/1pzazbe/)). Both are
  `reported-working`-grade anecdotes, unverified here.

## 4. Host-side 5 V direction switch

The Cardputer-Adv has a **5 V IN/OUT switch** next to its Grove port. u/pyreht reported
(firsthand experimentation, [r/CardPuter 2026-06-12](https://old.reddit.com/r/CardPuter/comments/1u3qeez/))
that with the switch in the *out* position and a load on the Grove port, the battery-sense
pin G10 reads above 5 V, and that injecting 5 V into the Grove port with the switch in the
*in* position also perturbs it. That is a **host** behaviour, not a Cap behaviour, but it
affects anyone reading battery voltage while a Cap is fitted. Recorded as a firsthand
report; not verified here. Belongs to `devices/m5stack/cardputer-adv/`.

## Applicability

| Field | Value |
|---|---|
| Hardware | U214 schematic V1.1 |
| Evidence | Parts and values: **schematic**, `executed-success`. Enable polarity: **`inferred`**. Grove I²C sharing: schematic + vendor pin-map |
| Last verified | 2026-09-04 |
