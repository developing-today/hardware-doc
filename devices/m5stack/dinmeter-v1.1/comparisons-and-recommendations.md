# DinMeter v1.1 — comparisons and recommendations

The full comparison — against the **Waveshare ESP32-S3-Knob-Touch-LCD-1.8**, the **M5Dial**, a
**DIY encoder + ESP32 build**, the alternatives-by-tier table and the DIN-cutout-versus-DIN-rail
explanation — is in
**[`../dinmeter/comparisons-and-recommendations.md`](../dinmeter/comparisons-and-recommendations.md)**
and applies to v1.1 unchanged: same enclosure, same cutout, same 6–36 V input, same display size,
same price.

This page answers only the questions that are specific to the revision.

---

## 1. v1.1 versus v1.0 — should you upgrade?

| Your situation | Answer | Why |
|---|---|---|
| You own a working v1.0 | **No** | The gains are module-level sleep figures you cannot use. The board's own standby is **38.4 µA on both revisions** — identical on both product pages — because the DinMeter *cuts the battery with a latch* rather than sleeping the SoC. See [`performance.md` §2](performance.md#2-the-important-row-is-the-last-one) |
| You are buying new | **v1.1** | It is the only one in stock. `K134` and `S007` are both marked `[EOL]` by M5Stack |
| You run continuously on battery (no latch) | **Marginal yes** | ~33.5 mA → ~25.5 mA awake ⇒ roughly **7.4 h → 9.8 h** on the bundled 250 mA·h cell. Vendor figures, unmeasured |
| You are deploying in a metal cabinet with marginal Wi-Fi | **Possibly** | The antenna match was genuinely rebuilt (3 → 6 matching positions). But M5Stack publishes **no dBi and no method**, and nothing here corroborates the claim. Do not pay for it sight-unseen; measure |
| You need to match an existing fleet on K134 | Buy v1.1 anyway | Firmware compatibility is complete except the RGB LED, and that is a two-line fix. Insisting on K134 buys nothing and the vendor no longer sells it |
| You are designing a new board around a Stamp | **Stamp-S3A**, USD 7.50 | The S3 is EOL. Budget **0.6 A** on the 3.3 V rail, not 1 A, and add the GPIO38 line if you want the LED |

**The honest summary: v1.1 is a straight replacement, not an upgrade.** Same price, same
capability, slightly better awake power, one new line of code if you use the LED. There is no
scenario in which replacing a working v1.0 with a v1.1 is worth USD 24.50.

## 2. Does the revision change any of the external comparisons?

**No.** Every axis on which the DinMeter competes — the 1/32 DIN cutout (45 × 22.5 mm), the
6–36 V screw-terminal input, the battery-backed RTC that can power the board back on, the
detented knob, the 135 × 240 display, the absence of PSRAM and touch, the 0–40 °C range, and the
USD 24.50 price — is **identical between v1.0 and v1.1**.

| Competitor | Does v1.1 change the verdict? |
|---|---|
| Waveshare ESP32-S3-Knob-Touch-LCD-1.8 | **No.** The Waveshare still has 8 MB PSRAM, a 360 × 360 round touchscreen, audio in/out, haptics, microSD, a second MCU for Bluetooth Classic — and still cannot be panel-mounted or run from 24 V |
| M5Dial v1.1 (USD 34.90) | **No.** Still +USD 10.40 for round + touch, still 5 V only, still no panel cutout. Note both products are now on their own "v1.1" — the M5Dial's is a separate SKU (`K130-V11`) and was **not** researched here |
| DIY encoder + ESP32 (≈ USD 10–18) | **No.** The enclosure and the standard aperture remain the part you cannot buy |
| M5Stack StamPLC (USD 42.90) | **No.** Still DIN-*rail*, not DIN-cutout — a different problem |

→ [`../dinmeter/comparisons-and-recommendations.md`](../dinmeter/comparisons-and-recommendations.md)

## 3. Who should buy a DinMeter v1.1

Unchanged from v1.0, and worth restating because it is narrow and specific:

**Buy it if** you have a 1/32 DIN aperture in an existing panel — a dead Omron/Autonics/Fuji
panel meter in a machine door is the canonical case — or you have 12/24 V and no 5 V, and you
want a detented knob as the primary input with timekeeping that survives power loss.

**Do not buy it if** you need PSRAM, touch, a bigger screen, more than ~6 free GPIOs, operation
outside 0–40 °C, or ESPHome/Tasmota/Meshtastic support. And do not buy it as a *first* ESP32
board — the GPIO46 power latch will catch you and the failure looks like a hardware fault.

## 4. One caution specific to v1.1

If you buy v1.1 and the RGB LED does not light, **it is not faulty**. Add:

```cpp
pinMode(38, OUTPUT); digitalWrite(38, HIGH); delay(1);
```

before driving GPIO21. No framework does this for you.
→ [`../dinmeter/features/rgb-led.md`](../dinmeter/features/rgb-led.md)

---

## Cross-references added 2026-09-07

Append-only, from a cross-cutting synthesis pass. Nothing above was changed and no
new evidence was gathered.

- [**SoC choice for battery e-ink devices**](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  — the Stamp-S3 → Stamp-S3A delta this record documents is used there as the
  general lesson for battery designs: a **45× board sleep-current improvement**
  (310.89 µA → 6.84 µA on `VIN_5V`, vendor figures, method unstated) that came
  entirely from the power tree, and that cost the RGB LED its always-on supply.
  The guide's wider point is that **this repository has no ESP32-C3, ESP32-S3 or
  ESP32-P4 deep-sleep figure at all** — every sleep number available here,
  including these two, is a board-level vendor claim under unstated conditions.
- [**Handheld and e-ink device landscape, 2026-09**](../../../guides/markets/handheld-and-eink-device-landscape-2026-09.md)
  — where the DinMeter family sits among every device record, and the observation
  that its v1.1 is the repository's cleanest example of a vendor **re-serving
  byte-identical assets under a new revision's filenames**.
