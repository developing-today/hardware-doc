# Band switching — Cap CC1101 (U219)

The one genuinely novel thing about this board, and the part most worth stealing.

## 1. The problem

A CC1101 will operate anywhere in 300–348 / 387–464 / 779–928 MHz, but a *matching network*
will not. A single fixed match across 315 → 915 MHz costs many dB. Most CC1101 modules
therefore pick one band and stay there — which is exactly the limitation an owner named on
release day: *"I've been using the CC1101 modules for some time, but it was always limited
to a single frequency band, most often 433 MHz."*
(u/No_Confusion7932, [r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/)) **[COM]**

## 2. The solution on this board

Three narrowband LC paths, selected by **two SP3T switches** (`U4`, `U5` —
`BGS13SN8E6327XTSA1`) placed either side of them, fed from a **wideband balun** at the
CC1101's differential port and terminating in **one** SMA connector.

Two control lines, **only one of which is a host pin**:

| Control | Source | Cardputer-Adv | CardputerZero |
|---|---|---|---|
| `CC1101_RF_SW0` | host GPIO, via Cap-Bus pin 2 | **G13** | **G14** |
| `CC1101_RF_SW1` | **CC1101 `GDO2` (pin 3)** — never leaves the board | — | — |

Truth table (product page and Arduino guide agree verbatim):

| `RF_SW0` | `RF_SW1` | Band | Antenna to fit |
|:---:|:---:|---|---|
| 0 | 0 | **315 MHz** | 315 MHz whip |
| 0 | 1 | **433 MHz** | 433 MHz whip |
| 1 | 1 | **868 / 915 MHz** | 868 MHz whip (covers 915) |

`1,0` is not defined by the vendor. Do not use it.

## 3. Driving `RF_SW1` through the CC1101

You cannot `digitalWrite()` a pin you do not have. `GDO2` is configured over SPI as a
**static output**, using the CC1101's `IOCFG2` register. RadioLib exposes this through its
GDO configuration constants; M5Stack's own guide does it like this:

```cpp
void setRfBand() {
    bool rf_sw0{}, rf_sw1{};
    if (CC1101_FREQ == 315.0f)                              { rf_sw0 = 0; rf_sw1 = 0; }
    else if (CC1101_FREQ == 433.0f)                          { rf_sw0 = 0; rf_sw1 = 1; }
    else if (CC1101_FREQ == 868.0f || CC1101_FREQ == 915.0f) { rf_sw0 = 1; rf_sw1 = 1; }

    // RF_SW0 is controlled directly by the host GPIO.
    pinMode(RF_SW0, OUTPUT);
    digitalWrite(RF_SW0, rf_sw0 ? HIGH : LOW);

    // Drive RF_SW1 from CC1101 GDO2 through SPI.
    const uint8_t gdo2_config = RADIOLIB_CC1101_GDOX_HW_TO_0 |
                                (rf_sw1 ? RADIOLIB_CC1101_GDO2_INV
                                        : RADIOLIB_CC1101_GDO2_NORM);
    // ... written to IOCFG2
}
```

**Read that carefully.** The chosen GDO source is `HW_TO_0` — "hardwired to 0" — and the
*polarity-inversion* bit is then used to produce a 1. That is the idiomatic way to make a
CC1101 GDO pin a constant-level output, and it is the trick worth remembering. **[DOC]**,
`executed-success` on the read, `not-tested`.

## 4. Ordering constraint

Because `RF_SW1` lives inside the transceiver, **you cannot select the band before the
CC1101 is initialised.** Sequence:

1. Power the Cap: host **G3 (`POWER_EN`) HIGH**.
2. `radio.begin(...)` — SPI up, chip configured.
3. `setRfBand()` — host GPIO for SW0, `IOCFG2` write for SW1.
4. Set the exact carrier frequency (`radio.setFrequency()` if not already set in `begin`).
5. Transmit or receive.

Changing band later means repeating steps 3–4. Doing step 5 before step 3 transmits into
the wrong matching network — not usually damaging at +10 dBm, but the range will be
terrible and it will look like a broken board.

## 5. Why this is worth copying

| Property | Value |
|---|---|
| Host GPIO cost | **1**, not 2 |
| Extra silicon | 2 × SP3T switch (small, cheap, sub-$1 class) |
| Bands covered | 3 matched paths, 4 nominal bands |
| Antenna ports | **1** |
| Constraint | band cannot be set before the transceiver is alive |

Any design with a transceiver that has a spare GDO/DIO pin and a shortage of host GPIO can
use the same pattern. It is not CC1101-specific — an SX126x's `DIO2`/`DIO3` are used the
same way for RF-switch control and TCXO supply respectively.

## 6. Unresolved

- The **schematic's own truth table** could not be transcribed from the PDF text layer
  (the `√`/`x` grid extracted as fragments). The table above rests on **two vendor
  documents that agree** plus the community announcement — three sources, none of them the
  schematic. If a future pass renders sheet 3, check it.
- Which switch (`U4` or `U5`) carries which control on which port was **not** resolved
  pin-by-pin; both are driven from the same two nets (`V1`, `V2`).
- Isolation between paths, insertion loss per band: unmeasured, unpublished.

## Applicability

| Field | Value |
|---|---|
| Hardware | Cap **U219** schematic V0.3 |
| Software | RadioLib ≥ 7.x for `RADIOLIB_CC1101_GDOX_HW_TO_0` / `GDO2_INV` |
| Evidence | Truth table: **two vendor docs + one vendor community post**, mutually consistent. Code: **read from the vendor guide**. Behaviour: `not-tested` |
| Last verified | 2026-09-04 |
