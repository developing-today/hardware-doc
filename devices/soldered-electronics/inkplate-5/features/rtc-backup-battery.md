# RTC backup battery (CR2032) — Inkplate 5 / Gen 2 and ZeroWriter Ink

> The board has the footprint. It ships empty. You do **not** need an add-on board.
> Snapshot **2026-08-24**. Derived from the KiCad PCB files of all three boards.

## Short answer

**Just fit a cell — the holder footprint is already on the PCB.** There is no "CR2032 board" or module to buy. You have two options:

1. **Solder an SMD coin-cell holder** onto the existing pads (the designed part is a `BS-6-1`-style CR2032 holder), then drop a cell in. Reversible, tidy, lets you swap cells.
2. **Wire a cell directly** to the two pads — a CR2032 with solder tabs, or a coin-cell holder with flying leads. Fine if you never intend to change it, or if you want the cell somewhere else in the enclosure.

Either way it is **two connections: `+` and `−`**. Nothing else on the board needs changing, and no firmware configuration is required.

## Where it is

| Board | Designator | Part in BOM |
|---|---|---|
| **Soldered Inkplate 5** | **`K10`** | `CR2032-BS-6-1` |
| **Soldered Inkplate 5 Gen 2** | **`K11`** | `CR2032-BS-6-1` |
| **ZeroWriter Ink** (respun Gen 2) | **`K11`** | `CR2032_BS-6-1` |

⚠ **The designator differs between the Inkplate 5 and the Gen 2.** On the Inkplate 5, `K10` is the coin cell and `K11` is the microSD socket; on the Gen 2 and ZeroWriter, `K11` is the coin cell. Check the silkscreen, not a table from the other generation.

## Pad geometry

From the ZeroWriter/Gen 2 PCB (`CR2032-BS-6-1` footprint, front copper):

| Pad | Position (relative to footprint origin) | Size |
|---|---|---|
| `+` | `+14.5 mm` | **3.0 × 4.2 mm** |
| `−` | `−14.5 mm` | **3.0 × 4.2 mm** |

Both are **SMD rectangular pads on `F.Cu`** — surface mount, no through-holes. Centre-to-centre spacing is **29 mm**, which is the standard footprint for a 20 mm coin-cell holder of the BS-6 family.

They are large, well separated and on the top surface, so **hand-soldering a wire to each is straightforward** — this is not fine-pitch work.

## The circuit

Identical topology on all three boards:

```
   3V3 ────► D11 ──┐
                   ├──► 3V3_RTC ──► PCF85063A  (U7 pins 3 and 10)
CR2032 ───► D12 ──┘         │
  (K10/K11)                 └──► C36 (decoupling)
```

A **diode OR**: the main 3.3 V rail feeds the RTC through `D11` while the system is powered, and the coin cell feeds it through `D12` when it is not. Whichever is higher wins.

Both diodes are `M4_DIODA` in the BOM.

Two consequences worth knowing:

- **`D12` blocks reverse current, so the main rail can never charge the coin cell.** That is correct design for a primary (non-rechargeable) CR2032 — and it means fitting the cell backwards is *ineffective*, not dangerous. It simply will not power the RTC.
- **The cell only supplies the RTC**, nothing else. Expected drain is the PCF85063A's timekeeping current (microamps), so a CR2032 should last years.

### Test points (ZeroWriter variant only)

ZeroWriter's respin adds two test points the stock Inkplate lacks:

| Test point | Net |
|---|---|
| **`TP72`** | `RTC-BATT` — the coin-cell side of `D12` |
| **`TP71`** | `3V3_RTC` — the RTC supply rail |

`TP72` is an alternative wiring point if the holder pads are awkward to reach in the assembled device, and `TP71` lets you verify the RTC rail is alive without disassembling further.

## Do you need it?

**Only if you need wall-clock time to survive power-off.**

| Feature | Needs the cell? |
|---|---|
| Writing/typing, file save, display | ❌ No |
| RTC alarm as a wake source *while powered* | ❌ No |
| **Correct date/time after the device is switched off** | ✅ **Yes** |
| **ZeroWriter v2.1 "Writing Stats"** — streaks, long-term tracking | ✅ **Yes** — vendor states "Requires a coin cell installed for all timekeeping features" |
| Inkplate scheduled-refresh dashboards across power loss | ✅ Yes |

Without a cell the RTC loses its count whenever the board is fully unpowered, and time has to be re-set on each boot.

## Fitting one

> Status: **`inferred`** from the design files. Not performed on hardware in this research pass.

- **Cell:** CR2032 (3 V lithium primary), 20 mm. `CR2025` fits the same holder with less capacity.
- **Holder:** any SMD CR2032 holder matching a 29 mm pad spacing — the designed part is the `BS-6-1` family. Verify the footprint before buying; coin-cell holder footprints are not standardised.
- **Polarity:** `+` pad goes to the diode/RTC side, `−` to ground. On a coin cell the **large flat face is `+`**.
- **Heat:** solder the *holder* to the board, then insert the cell. Do not reflow a board with a lithium cell fitted. If you are soldering wires directly to a cell, use **tabbed** cells — soldering directly to a bare cell risks venting.
- **Access:** on ZeroWriter Ink the main board is inside the enclosure, so this means opening the case — the same M2/M2.5 screwdriver job as the [first-time firmware update](../../../zerowriter/zerowriter-ink/firmware-and-updates.md).

## Why it ships empty

Not stated by any vendor. The usual reasons are shipping regulations for lithium cells, shelf-life (a cell fitted at manufacture drains during storage), and cost on a feature most buyers never use.

Notably **none of the three products mention it**: not the Inkplate product pages, not the Inkplate documentation, not the ZeroWriter campaign, and not the ZeroWriter repo. The only public acknowledgement found in this research is one line in ZeroWriter's **v2.1 release notes**. If your application depends on timekeeping, you would otherwise discover this the hard way.

## Related

- [`../pinouts-and-buses.md`](../pinouts-and-buses.md) — full board wiring
- [`../README.md`](../README.md) — Inkplate 5 record and BOM
- [PCF85063A component record](../../../../components/nxp/pcf85063a/README.md)
- [ZeroWriter Ink § v2.1](../../../zerowriter/zerowriter-ink/community-and-ecosystem.md) — where the requirement surfaced
