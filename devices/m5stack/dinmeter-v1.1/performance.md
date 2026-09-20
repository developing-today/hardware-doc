# DinMeter v1.1 — performance

**Nothing was measured.** No v1.1 hardware was available. Shared silicon limits, derivable
arithmetic and the full "not measured" list are in
**[`../dinmeter/performance.md`](../dinmeter/performance.md)**.

---

## 1. What actually changed, numerically

Module-level only, and **all vendor claims with no published method** — no instrument, no sample
count, no clock or radio state, no ambient temperature.

| Workload | Stamp-S3 (v1.0) | Stamp-S3A (v1.1) | Δ |
|---|---|---|---|
| Sleep, `VIN_5V` | 310.89 µA | **6.84 µA** | **−97.8 %** |
| Sleep, USB-C | 400.67 µA | **88.82 µA** | −77.8 % |
| Standby, `VIN_5V` | 33.56 mA | **25.53 mA** | −23.9 % |
| Standby, USB-C | 33.04 mA | **25.54 mA** | −22.7 % |
| **Board standby (latched off, battery)** | **38.4 µA** | **38.4 µA** | **unchanged** |

## 2. The important row is the last one

**The board's own standby figure did not change.** M5Stack quotes `DC 4.2 V @ 38.4 µA` on *both*
product pages, unchanged, while the module figures on the same pages *did* change.

That is internally consistent and worth understanding: the DinMeter **cuts the battery with a
latch** (GPIO46 → `Q4` → the `Q3`/`Q6` power path) rather than putting the SoC to sleep. In the
latched-off state the module is not sleeping — it is **unpowered**. The residual 38.4 µA is the
carrier's own LDO, dividers and latch network, and the module's sleep current does not enter into
it.

**Practical consequence: for the DinMeter's headline use case — a panel meter that wakes on an
RTC alarm — the Stamp-S3A's dramatic sleep improvement buys you nothing.** It matters if you
keep the module powered and use ESP32 sleep modes instead of the latch, which is not how this
board is designed to be used.

This is the single most useful thing in this document, and it is the opposite of what the
headline "−98 % sleep current" suggests.

## 3. Battery arithmetic, both revisions

Bundled cell: 250 mA·h.

| Mode | v1.0 | v1.1 |
|---|---|---|
| Continuously awake, radio up | 33.56 mA → **≈ 7.4 h** | 25.53 mA → **≈ 9.8 h** |
| Latched off between RTC wakes | 38.4 µA → ≈ 271 days | 38.4 µA → **≈ 271 days (same)** |
| 10 s awake per minute | ≈ 5.6 mA → ≈ 1.9 days | ≈ 4.3 mA → ≈ 2.4 days |

`inferred` from vendor figures ÷ nominal capacity. Ignores ageing, the 3.0 V cut-off, converter
efficiency at low load and wake inrush. **Do not design to these.**

So the honest summary of the upgrade's power benefit: **roughly +30 % awake runtime, and no
change at all to standby**.

## 4. What is claimed but unmeasured

| Claim | Source | Status |
|---|---|---|
| *"Optimized antenna design with better signal reception"* | Stamp-S3A page | **No dBi, no RSSI, no method.** The schematics do show a real topology change (3 → 6 matching positions plus a `CHIP_PU` filter, and `PROANT440` no longer named), so *something* was done — but whether it helps, and by how much, is unknown |
| ST7789P3 performs like ST7789V2 | inferred | **Unverified** — no datasheet exists |

The antenna claim matters more here than it would elsewhere: the DinMeter is designed to be
installed **behind a panel**, often in a metal cabinet, which is the worst RF case. A real link-
margin improvement would be genuinely valuable. It is simply not evidenced.

## 5. Everything else

Display throughput arithmetic, framebuffer cost (64 800 B with no PSRAM), silicon limits and the
full list of unmeasured workloads:
[`../dinmeter/performance.md`](../dinmeter/performance.md).

## 6. If you have both revisions — the two measurements worth taking

1. **RSSI at a fixed distance from the same AP, same firmware, v1.0 vs v1.1.** The only way to
   test the antenna claim, and nobody appears to have done it.
2. **Current in each state with a µA-capable meter.** Confirms or destroys the vendor figures —
   in particular whether the board standby really is identical across revisions.
