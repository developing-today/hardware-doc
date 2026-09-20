# X4 — display

> 800×480 mono e-ink, ~219 PPI, 4.26″. Same panel family as the X4 Pro and X4C.
> 2026-09-04.

| Property | Value |
|---|---|
| Resolution | 800 × 480, native landscape (`NO_FLIP`) |
| Depth | 1 bpp |
| Controller | **SSD1677** default; **UC8179 / UC8279** on newer batches |
| Bus | SPI **shared with the microSD card** — SCLK 8 / MOSI 10 |
| CS / DC / RST / BUSY | 21 / 4 / 5 / 6 |
| Clock | **20 MHz** default; 40 MHz opt-in |

## The clock decision — the clearest trade-off in the family

| Clock | Plane write | Spec status |
|---|---|---|
| **20 MHz** (default) | **~38 ms/refresh** | SSD1677 datasheet write maximum |
| **40 MHz** (`-DFREEINK_X4_OVERCLOCK_SPI`) | **~19 ms** — saves ~17–20 ms | **2× datasheet. Out of spec** |

40 MHz is what the **CrossPoint / Witch Reader** fork shipped. The SDK made it
opt-in and warns it *"can glitch plane writes on marginal wiring"*. Validate on
your own unit; a glitched plane write is a visibly corrupt page, not a crash.

**Trap:** `Ssd1677Driver`'s internal default is 40 MHz, so a board profile that
leaves `displaySpiHz = 0` runs out of spec **silently**. The X4 profile sets it
explicitly for exactly this reason.

## Controller detection

Identical mechanism to the [X4 Pro](../../x4-pro/features/display.md): a
bit-banged half-duplex read of `VER (0x70)` and `FLG (0x71)`, which the SSD-family
does not answer. `LUT_VER` (VER byte 2) then separates UC8279 (`0x02`/`0x68`/`0x69`)
from UC8179.

Because the X4 shares the bus with the SD card, the probe runs **before**
`EpdBus::begin()` and must release any retained GPIO hold from the sleep path
first (`gpio_hold_dis` on RST) — otherwise every `digitalWrite` bounces off the
latch and the probe selects the wrong driver. **[SDK]** `XteinkDetect.cpp:141–150`.

## Bus contention

There is no arbitration beyond chip select. A large SD read stalls the panel.
Firmware that streams a book page from the card while refreshing will serialise.

## Status

`reported-working` — the X4 is the ecosystem's most-exercised target. Refresh
timings are the only quantitative performance figures in this whole device family.
