# Infineon BGS13SN8

- **Category:** **SP3T (single-pole, triple-throw) RF switch**, sub-1 GHz
- **Ordering part as fitted:** **`BGS13SN8E6327XTSA1`** (`E6327` = green/RoHS tape-and-reel
  suffix; `XTSA1` = packing)
- **Research status:** **no datasheet retrieved.** Identity from a schematic symbol;
  behaviour inferred from how the board drives it and from the vendor's published truth
  table.
- **Retrieved:** 2026-09-04

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | **Infineon Technologies** (`BGS` = Infineon RF-switch family) | part-number convention, `inferred` |
| Function | **SP3T RF switch** — one common port, three switched ports | M5Stack product page: *"Built-in dual single-pole triple-throw (SP3T) RF switches"* |
| Control | **two logic inputs `V1`, `V2`** | schematic |
| Ports as drawn | `RF1` (5), `RF2` (7), `RF3` (4), `RFin` (6); `V1` (3), `V2` (2), `VDD` (1), `GND` (8) — pin numbering differs between the two instances as drawn | schematic |
| Supply | `VDD_3V3`, decoupled `C56`/`C57` 100 nF | schematic |

⚠ **Insertion loss, isolation, power handling, control-logic thresholds and switching time
are not stated here** — no datasheet was retrieved. Anything performance-related about this
part in the device records is a *board-level* vendor claim.

## 2. What it is doing on the one board that uses it

A CC1101 covers 315/433/868/915 MHz, but a single matching network cannot. The Cap CC1101
places **two** BGS13SN8 devices either side of **three** narrowband LC matching paths and
switches whole paths in and out:

```
CC1101 ─ balun ─▶ U4 (SP3T) ─┬─ 315 MHz match ─┬─▶ U5 (SP3T) ─▶ SMA
                             ├─ 433 MHz match ─┤
                             └─ 868/915 match ─┘
              V1,V2 ◀── RF_SW0, RF_SW1 ──▶ V1,V2
```

Both switches are driven from the **same two nets**, so they move together. Truth table (from
M5Stack's product page and Arduino guide, which agree):

| `RF_SW0` | `RF_SW1` | Band |
|:---:|:---:|---|
| 0 | 0 | 315 MHz |
| 0 | 1 | 433 MHz |
| 1 | 1 | 868 / 915 MHz |

`1,0` unlisted — undefined.

⚠ **Which physical switch port carries which band path was not resolved** pin-by-pin from
the schematic text layer. The aggregate mapping above is vendor-published; the port-level
mapping is a gap.

## 3. Used By

### [M5Stack Cap CC1101 & NFC (U219)](../../../devices/m5stack/cap-cc1101/README.md) — designators `U4` and `U5`, sheet 3

| Item | Value |
|---|---|
| Count | **two** |
| Control nets | `CC1101_RF_SW0` (from host **G13**, or **G14** on CardputerZero) and `CC1101_RF_SW1` (from the **CC1101's own `GDO2` pin**) |
| Supply | `VDD_3V3` with `C56` / `C57` 100 nF |
| Common port | `E1` `SMA-TH_KH-SMA-KE-Z` antenna connector |
| Band paths | 315 MHz (`L6` 10 nH, `L7` 0 R, `L8` 10 nH, `L17` 3.6 nH, `C50` 8 pF, `C51` DNP) · 433 MHz (`L9`, `L10`–`L13` = 0 R/0 R/15 nH/0 R, `C52`–`C55` = 10 pF/NC/6.2 pF) · 868–915 MHz (`L15` 0 R, `L16` 10 nH, `C58`–`C61`, `R7`, `D1` 0 R) |

The clever part is not the switch — it is that **only one of its two control lines costs a
host GPIO**. Full walkthrough:
[`devices/m5stack/cap-cc1101/features/band-switching.md`](../../../devices/m5stack/cap-cc1101/features/band-switching.md).

## 4. Reusability

This is a transferable pattern for any multi-band sub-GHz design: **wideband balun at the
transceiver, narrowband matched paths, SP3T switches at both ends, one antenna port.** The
alternatives are worse — a single compromise match loses several dB in every band, and
separate antenna connectors per band cost mechanical space and confuse users.

## 5. Local artifacts

**None.** An Infineon datasheet would fill in §1 and settle §2's port mapping.

## 6. Sources

| ID | Title | Publisher | Class | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|
| B-1 | Cap CC1101 schematic V0.3 | M5Stack | primary | [`devices/m5stack/cap-cc1101/artifacts/schematic/`](../../../devices/m5stack/cap-cc1101/artifacts/schematic/) | 2026-09-04 | Part number `BGS13SN8E6327XTSA1`, two instances, control nets, band paths |
| B-2 | Cap CC1101 documentation | M5Stack | primary | `https://docs.m5stack.com/en/cap/Cap_CC1101` | 2026-09-04 | "dual SP3T" description and the **truth table** |
| B-3 | Cap CC1101 Arduino guide | M5Stack | primary | `https://docs.m5stack.com/en/arduino/projects/cap/cap_cc1101` | 2026-09-04 | Truth table restated in code form |
| B-4 | r/CardPuter release thread | community | `https://old.reddit.com/r/CardPuter/comments/1w0nwti/` | 2026-09-04 | Independent statement of the SW0/SW1 sources |
