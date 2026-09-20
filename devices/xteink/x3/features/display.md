# X3 — display

> **792 × 528**, 3.7″, **~257 PPI** — the highest pixel density in the family.
> Two possible controllers. 2026-09-04.

| Property | Value |
|---|---|
| Resolution | **792 × 528** |
| Diagonal / PPI | 3.7″ / **~257** (√(792²+528²)=951.7 px ÷ 3.7) |
| Depth | 1 bpp; **4-level AA path exists on the UC8253 only** |
| Controller | **UC8253** (original) or **UC8279d** (from ~July 2026) |
| Bus | SPI shared with the SD card — SCLK 8 / MOSI 10 / CS 21 / DC 4 / RST 5 / BUSY 6 |
| Clock | **20 MHz** — UC8253 and UC8279 datasheet maximum |

Vendor claim *"over 250 PPI"* and the arithmetic agree — two independent
confirmations.

## Which controller, and how it is chosen

`detectX3DisplayController()` bit-bangs a half-duplex read of UC8279
**`VER (0x70)`** and **`FLG (0x71)`** after a reset pulse. Match requires a leading
`0x00`, a non-floating `CHIP_VER`, and `FLG` idle with `BUSY_N = 1` — **in two
passes agreeing byte-for-byte**. Anything else conservatively falls back to the
shipping **UC8253**.

**Two things the SDK admits it does not know** (both marked `Pending`):
1. **What the UC8253 actually answers to `0x70`.** The matcher relies on the
   UC815x-family REV placing the revision in the first byte — that is an
   assumption about the *other* part.
2. **Whether production MTP programs `CHIP_VER` to something other than `0x03`.**
   The matcher deliberately does not pin the value, having been burnt on the X4
   Pro where a shipping unit returned `CHIP_VER = 0x00`.

## The UC8279d driver is unvalidated

Quoted, because it is the most important caveat on this device:

> "Everything below is written from the UC8279d_B 0.1 datasheet (Dec 2025) and is
> **Pending hardware validation — no UC8279 X3 unit has been on the bench yet.**"
> — **[SDK]** `docs/xteink-x3-uc8279-support.md:13–14`

Consequences, all pending bench tuning:

- **Full / Half / Fast currently run the same OTP waveform** — likely a full
  GC-style flash on **every page turn**. Fast turns need custom register banks
  (`REG=1`, commands `0x20`–`0x24`).
- **The X3's six tuned UC8253 waveform banks cannot be copied over.** The UC8279
  LUT format is **group-based** (7-byte groups, 7 groups per LUT in KW mode), not
  the UC8253's 43-byte format. A porting effort, not a copy.
- **No grayscale** on UC8279 (`supportsStripGrayscale()` false). The 4-level AA
  path the X3 reader uses needs UC8279-format gray banks tuned on hardware.
- `TRES` is programmed 792×528, but the UC8253 init programs **VRES = 600**
  (the OEM scans the full gate count). If the image is offset or compressed, the
  SDK suggests trying `0x02 0x58`.
- `CDI` default drives the border white each refresh (`0x97`); the datasheet
  default (`0xD7`) floats it.

**Practical reading:** if you have a newer X3, expect worse page-turn behaviour
than an older one until someone tunes waveforms. `anki630/crossmosa-freeink-sdk`
is the only project found doing that work.

## UC8253 driver

KW mode (`PSR KW/R = 1`): 1 bpp, `DTM1` = OLD plane, `DTM2` = NEW plane,
differential refresh. Command set: `PSR`/`PON`/`POF`, `DTM1 0x10`, `DSP 0x11`,
`DRF 0x12`, `DTM2 0x13`, `CDI 0x50`, `TRES 0x61`, `DSLP 0x07`+`0xA5`.

The UC8279 driver uses a *near-identical* command set — which is why the port
looks deceptively easy and is not.

## Factory OTP waveforms

v1 uses `PSR REG = 0`: the **4K MTP carries 12 temperature-range LUT sets**, each
with its own frame rate and rail voltages, and **`TS_AUTO` re-senses temperature
before every booster enable**. So PWR/PLL/VDCS stay at silicon defaults and every
refresh is temperature-compensated **by the controller**, not the host.

That is a real advantage over host-authored waveforms and is worth knowing before
replacing them.

## UC8279 features not wired up

`AUTO (0x17)` — `PON→DRF→POF(→DSLP)` as one command, saving host round-trips on
sleepy updates. `PBC (0x44)` — panel-break check via the CHKGI/CHKGO loop, if the
module bonds it. `CRC (0x72)` — MTP integrity check over `0x000–0xFFF`.
`TSC (0x40)` — on-chip temperature readback.

## Status

`reported-working` for UC8253. **`not-tested` for UC8279d** — datasheet-derived
only.
