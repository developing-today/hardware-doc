# The JD9365 panel controller — what public sources actually cover

> Both P4 Touch-LCD variants drive their panels with a Jadard **JD9365DA**-family
> controller over MIPI DSI. No official datasheet was obtained during the original
> research pass, which left register `0x40` unexplained. This page aggregates what
> *public* sources do establish. Research pass **2026-08-24**.
>
> ⚠ Which exact suffix Waveshare fits (-H3? -B3? a custom program?) is **unknown**;
> everything below describes the JD9365DA-H3 as documented publicly and should be
> treated as strong prior, not confirmed fact, for these panels.

---

## 1. New public sources found (2026-08-24)

| Source | What it gives | Where |
|---|---|---|
| **JD9365DA-H3 Application Note V0.03** (2021-02-01) | Application circuits for BOE panels (10.1″, 8.9″, 8″, 6.95″…), 3-power-mode wiring, companion FP7721/FP7723 PMIC pairings | [lcddisplay.co PDF](https://lcddisplay.co/wp-content/uploads/2023/01/JD9365DA_V0.03_20210201.pdf) — submitted to web.archive.org 2026-08-24 |
| **Linux kernel driver `panel-jadard-jd9365da-h3.c`** | Register-level init tables for four production panels (Radxa 8HD AD002, CZ CZ101B4001, Kingdisplay KD101NE3, Melfas LMFBX101117480), reset/power sequencing timings | [torvalds/linux](https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/panel/panel-jadard-jd9365da-h3.c) |
| **LKML patch series (v2–v7, Jun–Jul 2024)** | Confirms the command-transfer protocol change (see §4) and documents real-world init timing | [patch v6](https://lists.openwall.net/linux-kernel/2024/06/28/733) |

## 2. Controller architecture (from kernel driver, confirmed across panels)

The register file is **banked**: register `0xE0` selects the active page, after which
`0x00–0xFF` address that page's registers.

```
write(0xE0, page)   ; switch page (pages 0x00 … 0x04 appear in public code)
<register writes>   ; addresses are page-local
```

Before touching configuration pages, every public init table starts with the same
**unlock / standard-command-enable sequence** on page 0:

```c
write(0xE0, 0x00);   // select page 0
write(0xE1, 0x93);
write(0xE2, 0x65);
write(0xE3, 0xF8);
write(0x80, 0x03);
// now switch to target page(s) for gamma/source/gate tuning
```

Waveshare's vendored table follows exactly this pattern (`E0/E1/E2/E3/80` prologue,
page switches interleaved, final `E0→0x00`), which corroborates that the fitted part
is a JD9365DA-family device using the same banking scheme.

Reset sequencing from `jadard_prepare()`: VCCIO/VDD enable → (optional LP11 hold) →
reset low 5 ms → high 10 ms → low 130 ms → init codes → sleep-out handled separately.

## 3. What this tells us about register `0x40`

> **⚠ Superseded 2026-08-30.** The conclusion below — that `0x40` is a panel-specific
> tune rather than a fixed-function bit — was drawn from **four** kernel panel tables that
> all wrote `0x06`. The mainline driver has since grown to **thirteen** panels, and
> correlating page-1 `0x40` against each panel's `hdisplay` shows it is the
> **horizontal-resolution selector**:
>
> | `0x40` | Horizontal resolution | Panels |
> |---|---|---|
> | `0x02` | 600 | 1 |
> | `0x03` | 640 | 1 |
> | `0x04` | **720** | 3 |
> | `0x06` | **800** | 7 |
>
> 12 of 13 are consistent. The JD9365DA datasheet corroborates independently: §3.1 lists
> exactly 800/768/750/720/640/600 RGB as supported widths, and §6 tabulates source-channel
> remapping per width.
>
> This **explains the 3.4C/4C difference directly** — the two boards differ only in width
> (800 vs 720), which is exactly what the differing byte encodes. It is *not* an untouchable
> per-panel magic number.
>
> **One anomaly remains open:** the 3.4C writes `0x00` for an 800-wide panel, which fits no
> row above. Flagged rather than explained away.
>
> The register's official name and bit-fields are still **not** in the datasheet — the
> `E0h`-paged manufacturer registers are absent from it — so the "RSO" label that circulates
> in vendor tables has **not** been adopted here. Full derivation:
> [components/jadard/jd9365](../../../../components/jadard/jd9365/README.md).

The original reasoning, retained for provenance:

- In all four kernel panel tables *then available*, page-0x01 `0x40` is written to **0x06**, sitting in
  a dense block (`0x37…0x45`) alongside what are recognizably gate/source timing and
  VCOM-adjacent tunables by their value patterns.
- Waveshare writes **0x00** (3.4C) and **0x04** (4C) at the same location — i.e. the
  byte varies *per panel* even within one vendor's product line, consistent with it
  being a panel-specific tune rather than a fixed-function mode bit.
- ~~**Practical rule stands:** the byte is part of the panel's tuned characterisation.~~
  **Revised:** do not port the byte between the 3.4C and 4C — but because it selects
  resolution, not because it is opaque.

If someone obtains the `E0h`-paged manufacturer register map, the first thing to look up is this
block (`page 01, registers 0x35–0x57`) — that would retroactively explain most of the
vendor magic numbers in both Waveshare tables.

## 4. Practical gotcha from upstream: where you send init codes matters

The LKML series documents that sending the ~200-instruction init table while the DSI
host is in **high-speed mode** costs ~17 ms *per instruction* (mode-switch overhead:
HS→LP→cmd→HS each write), versus ~25 µs when sent in LP mode — 3.5 s total vs ~5 ms.
On ESP32-P4 + `esp_lcd`, the DBI/DPI command path used by Waveshare's demos sends
commands before enabling HS video, so this mostly bites people porting the panel to
hosts that start in HS mode. Symptom if hit: multi-second boot delay between panel
reset and first frame, not corruption.

## 5. Related

- [`features/display.md`](display.md) — board-side usage, vendor init table, Arduino library
- [4C record §"JD9365 register 0x40"](../../esp32-p4-wifi6-touch-lcd-4c/gaps-and-conflicts.md#jd9365-register-0x40--0x04) — the differing byte
- [`gaps-and-conflicts.md`](../gaps-and-conflicts.md) — conflict register for both variants
