# I/O expander and antenna RF switch — Cap LoRa-1262 (U214)

Snapshot 2026-09-04. `PI4IOE5V6408`, designator `U2`, I²C **0x43** (7-bit).

## 1. Why this page exists

The Cap has exactly **one** thing that must be configured over I²C before RF works, and
skipping it produces a radio that passes every self-test and transmits into a dead antenna
port. It is also the mechanism by which firmware distinguishes this Cap from its
predecessor.

## 2. The chip

| Property | Value | Evidence |
|---|---|---|
| Part | **PI4IOE5V6408** — 8-bit I²C GPIO expander, 16-pin | **[SCH]** `U2`; **[DOC]** pin-map graphic |
| Address | **0x43** | **[SRC]** M5Stack example `PI4IOE5V6408_Class ioe(0x43, …)`; **[SRC]** Meshtastic `#define PI4IO_ADDR 0x43`; **[SCH]** `ADDR` pin 9 strapped |
| Bus | host I²C, `SDA` = G8, `SCL` = G9 | **[SRC]** `m5::In_I2C.begin(I2C_NUM_0, 8, 9)` |
| Bus speed used by the vendor | **400 kHz** | **[SRC]** |
| Pins used | **P0 only** | **[SCH]** |
| P0 net | `SX_ANT_SW` → `Stamp LoRa-1262 Mini` pin 10 (`SW`) | **[SCH]**, **[DOC]** |
| P1–P7 | **unconnected** | **[SCH]** |
| `INT` (pin 1) | **not routed to the host** | **[SCH]** |
| `RESET` (pin 10) | tied off | **[SCH]** |

Component record: [`components/diodes-incorporated/pi4ioe5v6408`](../../../../components/diodes-incorporated/pi4ioe5v6408/README.md).

## 3. Registers actually used, and by whom

Meshtastic writes raw registers; the numbers are the primary evidence for the register map
as used here. **[SRC]** `src/platform/extra_variants/m5stack_cardputer_adv/variant.cpp`

| Register | Name in the Meshtastic source | Written value | Meaning |
|---|---|---|---|
| `0x03` | `PI4IO_REG_IO_DIR` | `0b00000001` | P0 = **output** |
| `0x07` | `PI4IO_REG_OUT_H_IM` | `0b00000000` | P0 **not** high-impedance |
| `0x05` | `PI4IO_REG_OUT_SET` | `0b00000001` | P0 = **HIGH** |

M5Stack's Arduino path does the same three things through `m5::PI4IOE5V6408_Class`:

```cpp
ioe.setDirection(0, true);        // output
ioe.setHighImpedance(0, false);   // actually drive
ioe.digitalWrite(0, true);        // high
```

**The order matters and the middle step is the one people forget.** The PI4IOE5V6408 has a
separate high-impedance control per pin; a pin can be configured as an output and still not
drive. M5Stack's own comment on that line is *"Disable high-impedance so pin can actually
drive"*.

### 3.1 Upstream got this wrong twice before getting it right

Meshtastic shipped Cardputer-Adv support in **2.7.20** (2026-03-11) and then fixed the
antenna-switch initialisation **twice**:

| Commit | Date | Message |
|---|---|---|
| `3261c04afbdc` | 2026-05-18 | *Fix Antenna Switch on Cardputer* (PR #10491) |
| `98e0604edf87` | 2026-05-19 | *Fix antenna switch initialization logic once more* |

First release with both: **`v2.7.24.472b14c`, 2026-05-23**. If you are debugging an older
build, that is a real candidate cause, not a red herring.

## 4. Runtime Cap detection — probe 0x43

Both vendor and upstream code use the presence of the expander as the *identity* of the
Cap:

| Probe result | Conclusion |
|---|---|
| **0x43 ACKs** | **Cap LoRa-1262 (U214)** — set P0 high before RF |
| **0x43 silent** | **Cap LoRa868 (U201)** — no switch to set; the radio still works |
| No Cap at all | also silent; the SX1262 will simply fail to `begin()` |

M5Stack's example prints `"Using Cap LoRa-1262"` or `"Using Cap LoRa868"` from exactly this
test. Meshtastic probes **`Wire1` first, then `Wire`**, and logs `"Cap LoRa-1262 not found"`
if neither answers — note it does *not* abort; the radio is brought up regardless.

⚠ **This detection is a heuristic, not an identity register.** Anything else at 0x43 on the
bus — including a Grove sensor plugged into the Cap's own pass-through port — will be
mistaken for the antenna switch, and the real switch will never be set. There is no vendor
ID readback in either code path.

## 5. What `SW` actually does is undocumented

Module pin 10 (`SW` here, `SX_ANT_SW` on the PaperMono) is set HIGH once at boot and never
touched again by any code located — vendor, upstream or community. Whether it selects
TX/RX paths, enables an external PA/LNA, or selects between antenna connectors is stated
**nowhere**: there is no `Stamp LoRa-1262` module datasheet
([`components/m5stack/stamp-lora-1262` §5 G1](../../../../components/m5stack/stamp-lora-1262/README.md)).

Note also that the SX1262 has its own internal `DIO2`-driven RF switch control, which is a
*different* signal. The PaperMono firmware calls `setDio2AsRfSwitch(true)`; **neither
M5Stack Cap example does**, and Meshtastic sets `SX126X_DIO2_AS_RF_SWITCH` in `variant.h`.
So on this board there are plausibly **two** switch mechanisms, one inside the module driven
by DIO2 and one outside driven by P0, and no document describes either.

## 6. Free resources for a derivative design

`P1`–`P7` are unused and already on the bus. `INT` is unrouted. If you are respinning this
Cap, that is seven I²C-reachable GPIO available for nothing.

## Applicability

| Field | Value |
|---|---|
| Hardware | U214 schematic V1.1. **Not** present on U201 |
| Software | M5Unified `PI4IOE5V6408_Class`; Meshtastic ≥ 2.7.24 for the corrected init |
| Evidence | Address and register writes: **two independent source trees agree**, `executed-success` on the reads. `SW` semantics: **unknown** |
| Last verified | 2026-09-04 |
