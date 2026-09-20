# DinMeter — performance

**Nothing in this document was measured.** No hardware was available. This page exists to state
exactly what is known, what is claimed by whom, what can be derived arithmetically, and what
would have to be measured — rather than to present an unmeasured device as characterised.

---

## 1. Vendor-claimed figures

Every one of these is a **vendor claim with no published method** — no instrument, no sample
count, no clock/radio/peripheral state, no ambient temperature.

| Workload | Device/config | Figure | Source | Status |
|---|---|---|---|---|
| Standby (latched off, battery) | DinMeter, DC 4.2 V | **38.4 µA** | both product pages | official claim |
| Sleep | Stamp-S3, `VIN_5V` | 310.89 µA | Stamp-S3 page | official claim |
| Sleep | **Stamp-S3A**, `VIN_5V` | **6.84 µA** | Stamp-S3A page | official claim |
| Sleep | Stamp-S3, USB-C | 400.67 µA | Stamp-S3 page | official claim |
| Sleep | **Stamp-S3A**, USB-C | **88.82 µA** | Stamp-S3A page | official claim |
| Standby (active, radio state unstated) | Stamp-S3, `VIN_5V` | 33.56 mA | Stamp-S3 page | official claim |
| Standby | **Stamp-S3A**, `VIN_5V` | **25.53 mA** | Stamp-S3A page | official claim |
| Grove port load | either port | 5 V @ 220 mA max | both product pages | official claim |
| Charge current | — | 100 mA | both product pages | official claim |

**Two decimal places on an unspecified method is not precision, it is formatting.** Treat
`6.84 µA` as "single-digit microamps under some sleep configuration".

**Note the 38.4 µA figure is identical on the v1.0 and v1.1 pages** despite the module's sleep
current improving ~45×. That is internally consistent: the board *cuts the battery* with a latch
rather than sleeping the SoC, so the residual is dominated by the carrier's LDO and latch
network, not by the module. It is also a useful cross-check that M5Stack did not simply
copy-paste the number — the module numbers *did* change on the same pages.

## 2. Silicon limits (not measurements)

| Property | Value | Source |
|---|---|---|
| CPU | Xtensa LX7 dual-core, up to **240 MHz** | ESP32-S3 datasheet |
| SRAM | ~512 KB internal | ESP32-S3 datasheet |
| **PSRAM** | **none** | `ESP32-S3FN8`; confirmed by `build_unflags = -DBOARD_HAS_PSRAM` in `bmorcelli/Launcher` |
| Flash | 8 MB in-package | vendor spec |
| Display SPI clock as configured | **40 MHz** | three independent sources agree |
| Wi-Fi | 2.4 GHz 802.11 b/g/n | ESP32-S3 datasheet |
| Bluetooth | BLE 5 only, **no Classic** | ESP32-S3 datasheet |

## 3. Derivable arithmetic (labelled as such, not as measurement)

**Display throughput ceiling.** 135 × 240 × 16 bpp = 64 800 B = 518 400 bits per full frame. At
40 MHz SPI with zero overhead that is **≈ 77 full frames/s**. Real figures will be materially
lower — SPI transaction overhead, DMA setup, `startWrite`/`endWrite` batching, and the CPU time
to *produce* the pixels. `inferred` arithmetic; **no frame rate was measured**.

**Framebuffer cost.** A full-screen `M5Canvas` sprite is **64 800 B** of the ESP32-S3's ~512 KB
SRAM, with no PSRAM to spill into. Espressif's board definition sizes its SPI transfers at
`max_transfer_sz: 6480` = 135 × 24 lines × 2 B, i.e. a **24-line band buffer** — a deliberate
choice on a PSRAM-less part, and the right default.

**Battery life, first-order.** Bundled cell is 250 mA·h.

| Duty | Current | Runtime |
|---|---|---|
| Continuously awake with radio (Stamp-S3A standby figure) | 25.53 mA | **≈ 9.8 h** |
| Continuously awake (Stamp-S3 figure) | 33.56 mA | ≈ 7.4 h |
| Latched off between RTC wakes | 38.4 µA | **≈ 271 days** at zero duty |
| 10 s awake per minute | ≈ 4.3 mA average | ≈ 2.4 days |

`inferred` from vendor figures ÷ nominal capacity. Ignores cell ageing, the 3.0 V cut-off,
converter efficiency at low load, and the inrush of waking. **Do not design to these**; they
show the shape of the problem, which is that this device is only a long-life device if you use
the RTC latch.

## 4. Stamp-S3 → Stamp-S3A, as a percentage

| Metric | S3 | S3A | Δ |
|---|---|---|---|
| Sleep, `VIN_5V` | 310.89 µA | 6.84 µA | **−97.8 %** |
| Sleep, USB-C | 400.67 µA | 88.82 µA | **−77.8 %** |
| Standby, `VIN_5V` | 33.56 mA | 25.53 mA | −23.9 % |
| Standby, USB-C | 33.04 mA | 25.54 mA | −22.7 % |

Mechanistically consistent with the two power changes found in the schematics: a modern buck IC
with selectable light-load modes replacing a fixed µPOL module, plus removing the WS2812B-2020's
quiescent draw from the always-on 3.3 V rail (a WS2812B-2020 idles around 0.6–1 mA). That
accounts for roughly the standby delta on its own. **`inferred` — not decomposed, not measured.**

## 5. What was NOT measured

Stated as a list so no reader mistakes silence for a null result.

| Workload | Status |
|---|---|
| Boot time | **not measured** |
| Display frame rate, fill rate, tearing | **not measured** |
| Encoder maximum tracked rotation rate | **not measured** |
| SPI throughput at 40 MHz | **not measured** |
| Wi-Fi throughput, RSSI, range | **not measured** |
| **RF: whether the Stamp-S3A antenna is actually better** | **not measured** — the vendor's claim is qualitative and uncorroborated |
| BLE latency / connection interval | **not measured** |
| Actual current in any state | **not measured** |
| Buzzer SPL and resonant frequency | **not measured** |
| Grove 5 V rail actual voltage (5.00 or ≈5.38 V?) | **not measured** — see [`gaps-and-conflicts.md`](gaps-and-conflicts.md) §6 |
| Thermal behaviour, throttling | **not measured** |
| Behaviour at 36 V input | **not measured** |
| Charge-cycle profile | **not measured** |
| Battery runtime, real | **not measured** |

## 6. If you have hardware — the measurements worth taking, in order

1. **Current in each state**, with a µA-capable meter: latched off, idle with radio off, Wi-Fi
   associated, display on at full brightness. Confirms or destroys the entire battery story.
2. **Grove rail voltage** on `J3` pin 3. One reading, settles a documented conflict.
3. **Display frame rate** for a full-screen fill and for a band-buffered update.
4. **Wi-Fi RSSI at a fixed distance, v1.0 vs v1.1** — the only way to test the antenna claim.
5. **Buzzer SPL swept 1–12 kHz** — finds the resonance the datasheet does not exist to state.

Each records device revision, software versions, method, environment, sample count, units and
variability. Results belong here and in
[`compatibility-and-status.md`](compatibility-and-status.md).

## Related

[`features/power-and-battery.md`](features/power-and-battery.md) ·
[`resources-and-conflicts.md`](resources-and-conflicts.md) ·
[`../dinmeter-v1.1/stamp-s3-to-s3a-delta.md`](../dinmeter-v1.1/stamp-s3-to-s3a-delta.md)
