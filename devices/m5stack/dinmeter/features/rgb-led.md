# How do I light the RGB LED — and why doesn't it work on v1.1?

**Applies to:** K134 (works out of the box) and **K134-V11 (needs an extra line)**.
**Evidence status:** `executed-success` for the schematic net reading; the v1.1 failure mode is
**`inferred`** — predicted from vendor documentation + schematic + a source read, and **not
reproduced on hardware**. **Last verified:** 2026-09-04.

---

## Where the LED is

**Not on the carrier board.** The DinMeter's own 84-part designator census contains no LED
driver and no addressable LED. The RGB LED is **inside the Stamp module**:

```
Stamp module:  ESP32-S3 GPIO21 ──"SK_DIN"──► U3  WS2812B-2020  ──"SK_DOUT"──► (unused)
                                              VDD ← ???  ← this is what changed
```

- Part: **WS2812B-2020**, ×1, stated on both Stamp product pages.
- Data: **GPIO21**, `U1` pad 27 on both Stamp schematics.
- M5Unified: `_pin_table_other0` → `{ board_M5DinMeter, GPIO_NUM_21 }`, `M5Unified.cpp:246`.
- **GPIO21 is not one of the Stamp's 23 broken-out IOs** — it is internal, so nothing on the
  DinMeter carrier can conflict with it.

## The difference between the two revisions

| | DinMeter (K134) — Stamp-S3 v0.2 | DinMeter v1.1 (K134-V11) — Stamp-S3A v0.3.3 |
|---|---|---|
| WS2812B `VDD` | **`VDD_3V3`** — always powered | **`BL_3V3`** — switched |
| Switch | — | `U2` **AW35122FDR** load switch |
| Switch enable | — | `DISP_BL` = **GPIO38** |
| Default state at reset | LED powered | **LED unpowered** (AW35122 `EN` has a ~7.1 MΩ internal pull-down) |
| Works with stock M5Unified? | **yes** | **predicted no** |

M5Stack states it plainly on the v1.1 page:

> "Stamp-S3A adds an independent electronic switch for the RGB LED power supply compared with the
> previous Stamp-S3. Before controlling the RGB LED in software, set **GPIO38**, which controls
> this switch, to a high level."

## Portable code — works on both

```cpp
#include <M5DinMeter.h>

void setup() {
    auto cfg = M5.config();
    DinMeter.begin(cfg, true);

    // Stamp-S3A (DinMeter v1.1): enable the BL_3V3 rail that feeds the WS2812B.
    // On Stamp-S3 (DinMeter v1.0) GPIO38 is unused by the carrier, so this is harmless.
    pinMode(38, OUTPUT);
    digitalWrite(38, HIGH);
    delay(1);                       // AW35122 typ. rise 165 us; 1 ms is comfortable

    // ... then drive GPIO21 with your WS2812 library of choice
}
```
`not-tested`. The 1 ms settle is prudence, not a documented requirement.

Any WS2812 driver works: `FastLED`, `Adafruit_NeoPixel`, `Freenove_WS2812_Lib`, or ESP-IDF's
`led_strip` RMT/SPI backend. Nothing here is board-specific beyond the pin numbers.

## Why this is worth a whole page

The failure is **silent and misattributed**. On a v1.1 unit, code that worked on v1.0 compiles,
links, boots, runs, and the LED simply does not light. Nothing errors. The natural conclusion is
"the LED is faulty" or "my library is broken", and neither is true.

And **M5Unified will not rescue you**, at master `8530f5377d782e4a25a6c482de2e71c3f75ca8eb`
(2026-09-04):

- there is **no `board_M5DinMeter_v11`** and **no `board_M5StampS3A`** enum (grep of `src/`,
  `executed-success`);
- the RGB-LED table has one entry for `board_M5DinMeter` and it is just `GPIO_NUM_21`;
- **no board in the whole table has a power-enable step.**

So a v1.1 unit enumerates as `board_M5DinMeter` and gets the v1.0 behaviour. If someone with a
v1.1 unit tests this, the result belongs in
[`../compatibility-and-status.md`](../compatibility-and-status.md) and would be the single most
valuable addition to this record.

## Resource cost and conflicts

| Resource | Used |
|---|---|
| GPIO | 21 (data, internal) + **38 on v1.1** (enable, internal) |
| RMT / SPI channel | 1, if you use a hardware-timed driver |

**No conflicts.** Neither pin is available to the carrier or to the Grove ports, so nothing else
can want them. On the DinMeter, GPIO38 has exactly one job.

## Pitfalls

| Symptom | Cause |
|---|---|
| LED dark on a new (v1.1) unit, code unchanged | GPIO38 not raised. **This is the one** |
| LED dark on v1.0 | genuinely a fault, or the wrong pin |
| First frame wrong colour after enabling | rail had not settled — add the delay |
| LED stays lit in sleep, wasting current on v1.0 | it is on the always-on rail; that is the design M5Stack changed |

## Related

[`../../dinmeter-v1.1/stamp-s3-to-s3a-delta.md`](../../dinmeter-v1.1/stamp-s3-to-s3a-delta.md) §3
(the full evidence chain) ·
[`components/m5stack/stamp-s3a`](../../../../components/m5stack/stamp-s3a/README.md) ·
[`components/awinic/aw35122`](../../../../components/awinic/aw35122/README.md) ·
[`components/sgmicro/sgm2578`](../../../../components/sgmicro/sgm2578/README.md)
