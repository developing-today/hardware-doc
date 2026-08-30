# ZeroWriter 1 — modifications to the vendored Waveshare e-paper Python driver

> Extracted **2026-08-24** from `artifacts/source-snapshots/zerowriter1/e-Paper/`, which has since
> been archived out of this repository. See
> [`artifacts/vendored-deps/README.md`](artifacts/vendored-deps/README.md) for the reacquisition
> record and [`artifacts/vendored-deps/patches/`](artifacts/vendored-deps/patches/) for the patches
> themselves.
>
> This document exists so the findings survive without reopening the archived tree.

## Why this matters

ZeroWriter 1 (the Raspberry Pi predecessor of ZeroWriter Ink) vendors Waveshare's official
`e-Paper` Python driver library. Of the **272 files** in that tree, **270 are byte-identical to
Waveshare upstream** at commit `fc4f54334d087dae440e3e9ac2bf8d809dfcfb53` (2023-06-12). Two files
carry ZeroWriter's own edits. Anyone rebuilding a ZeroWriter 1 from stock Waveshare sources will
silently get different behaviour in both.

| File | Nature of change | Severity |
|---|---|---|
| `lib/waveshare_epd/epdconfig.py` | platform-autodetect fallback + CRLF→LF | breaks import on some Pi configurations if reverted |
| `lib/waveshare_epd/epd3in7.py` | two waveform LUTs replaced, one init delay shortened | changes display drive behaviour |

**Scoping caveat:** these are ZeroWriter **1** (Raspberry Pi + discrete Waveshare panel) changes.
ZeroWriter **Ink** — the device this record documents — uses an ESP32 and a Soldered Inkplate 5
Gen2 respin with an `ED052TC4` panel driven by a `TPS65186` PMIC, and does **not** use this Python
library at all. Treat this page as predecessor/lineage evidence, not as Ink firmware documentation.

---

## 1. `epdconfig.py` — platform fallback

```python
 elif os.path.exists('/sys/bus/platform/drivers/gpio-x3'):
     implementation = SunriseX3()
 else:
-    implementation = JetsonNano()
+    implementation = RaspberryPi()
```

`epdconfig.py` picks a GPIO/SPI backend at **import time** by probing the filesystem. Upstream's
final `else` selects `JetsonNano()`, whose `__init__` imports `Jetson.GPIO`. ZeroWriter 1 is a
Raspberry-Pi-only product, so on any Pi where the earlier probes fail the stock library raises at
import rather than running.

This is not hypothetical for this project: the zerowriter1 README carries a prominent warning that
*"raspberry pi OS has changed GPIO support, so it is important you use archived versions of the
OS"* and links issue #26. The fallback change is a hedge against exactly that class of detection
failure.

The file was also converted from CRLF to LF. That is cosmetic, but it means a naive `diff` against
upstream reports the whole file as changed — normalise line endings before diffing.

*Evidence status: change verified from the archived file vs. upstream. The connection to the Pi OS
GPIO breakage is **inferred** from the project README's own warning, not stated by the author.*

---

## 2. `epd3in7.py` — replaced waveform LUTs and a shortened reset delay

### 2a. Shortened software-reset settle delay

```python
 self.send_command(0x12)
-epdconfig.delay_ms(300)
+epdconfig.delay_ms(100)
```

Command `0x12` is SW RESET on this controller family. Upstream waits 300 ms; ZeroWriter waits
100 ms. This shaves 200 ms off every `init()`. On a typewriter that wakes, draws a line of text
and sleeps again, init latency is felt directly by the typist.

*Evidence status: change verified. Whether 100 ms is reliably sufficient across panel batches and
temperatures is **untested** — this is a plausible place for intermittent init failures if you
inherit the patch.*

### 2b. The LUT layout, for context

The driver writes look-up tables with command `0x32` (Write LUT Register) via `load_lut()`. Each
LUT constant in this file is **105 bytes**: ten 10-byte voltage/phase rows followed by a 5-byte
trailing group. In the stock tables that trailing group is `0x22,0x22,0x22,0x22,0x22`.

Four LUTs are defined. Only three are ever used:

| LUT | Referenced by | Modified by ZeroWriter? |
|---|---|---|
| `lut_4Gray_GC` | `display_4Gray()`, `Clear()` (4-gray mode) | **Yes** |
| `lut_1Gray_GC` | **nothing — dead code** | **Yes** (therefore inert) |
| `lut_1Gray_DU` | `Clear()` (1-gray mode) | No |
| `lut_1Gray_A2` | `display_1Gray()` | No |

That table is the single most important fact here: **the two LUTs ZeroWriter left alone
(`A2`, `DU`) are the ones the fast 1-bit text path actually uses.**

### 2c. `lut_4Gray_GC` — replaced

| | Rows 1–5 | Row 6 | Row 7 | Rows 8–10 | Trailing group |
|---|---|---|---|---|---|
| **Upstream** | four populated drive rows (`2A 06 15…`, `28 06 14…`, `20 06 10…`, `14 06 28…`) then zeros | `00 02 02 0A 00 00 00 08 08 02` | `00 02 02 0A 00 00 00 00 00 00` | zeros | `22 22 22 22 22` |
| **ZeroWriter** | row 1 = `00 02 02 0A 00 00 00 08 08 02`, rows 2–5 zeros | zeros | zeros | zeros | **`00 00 00 00 00`** |

Two things happened: the surviving row was moved to position 1, and **the trailing group was
zeroed**.

In this LUT format the trailing group carries the per-phase frame counts. Setting it to all zeros
means every phase runs for zero frames, i.e. **the 4-gray greyscale update is effectively
neutered** — `display_4Gray()` will clock data into the controller and trigger an update that does
no driving.

That is consistent with ZeroWriter 1 being a **1-bit text device**: it renders through
`display_1Gray()`/`lut_1Gray_A2`, which is untouched. Disabling the greyscale path removes a slow
(multi-second) refresh mode that the product never wants to enter.

*Evidence status: the byte-level change is **verified** from the file. The reading of the trailing
group as frame counts, and therefore the conclusion that the 4-gray path is neutered, is
**inferred** from the LUT structure and from the fact that every other LUT in the file keeps
`22 22 22 22 22`. It has **not** been confirmed against the panel controller datasheet or on
hardware. Do not treat "greyscale is disabled" as established.*

### 2d. `lut_1Gray_GC` — replaced, but dead

The same reshaping was applied: the populated row `00 02 03 0A 00 02 06 0A 05 00` moved to
position 1, rows 2–10 zeroed, **trailing group `22 22 22 22 22` retained**.

Because nothing in `epd3in7.py` calls `load_lut(self.lut_1Gray_GC)`, this change has **no runtime
effect**. It is most plausibly collateral from the same hand-edit pass that produced 2c.

### 2e. A trailing blank line

The patch also appends one empty line at end of file. Noise.

---

## Why the 3.7" driver at all?

ZeroWriter 1's documented panel is the **Waveshare 4.2" e-Paper** — the project README routes users
between `main`, `main_full` and `waveshare_2.2` branches by the Rev2.1/Rev2.2 marking on the back
of a 4.2" module. `epd4in2.py` in the vendored tree is **byte-identical to upstream**.

So the modified driver is for a panel the shipping product does not use. The most likely
explanation is an earlier 3.7" prototype whose edits were never reverted before the initial import
(`epd3in7.py` first appears in zerowriter1's "Initial commit", 2023-12-13, already patched).

*Evidence status: **inferred**. No commit message, issue or README text in either repository
explains the 3.7" edits.*

---

## Practical guidance

- Rebuilding ZeroWriter 1 from stock Waveshare sources: apply
  [`waveshare-epaper-epdconfig-zerowriter.patch`](artifacts/vendored-deps/patches/waveshare-epaper-epdconfig-zerowriter.patch).
  You can safely skip the `epd3in7.py` patch unless you are driving a 3.7" panel.
- Porting ZeroWriter 1's rendering approach: the relevant art is `lut_1Gray_A2` +
  `display_1Gray()`, both **stock Waveshare**. There is no secret ZeroWriter waveform.
- If you find a ZeroWriter 1 unit that cannot do greyscale on a 3.7" panel, §2c is your first
  suspect.

## Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| S1 | `zerowriter1` repository, branch `main`, commit `e476d05` | Zerowriter (Adam Wilk) | primary | repository | <https://github.com/zerowriter/zerowriter1> | 2026-08-24 | the vendored tree and its two modified files |
| S2 | `waveshareteam/e-Paper`, commit `fc4f5433` (2023-06-12) | Waveshare | primary | repository | <https://github.com/waveshareteam/e-Paper> | 2026-08-24 | the unmodified upstream baseline |
| S3 | zerowriter1 README GPIO/OS warning + issue #26 | Zerowriter | primary | repository | <https://github.com/zerowriter/zerowriter1/issues/26> | 2026-08-24 | context for the `epdconfig.py` fallback change |
