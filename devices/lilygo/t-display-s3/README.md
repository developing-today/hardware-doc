# LilyGO T-Display-S3

> **Product:** T-Display-S3 · store handle `t-display-s3` · SKUs `H569` (non-soldered),
> `H577` (soldered), `H587`/`H589` (Touch), `K204`/`K206` (with shell) · published to
> LilyGO's store **2022-07-15** · **active, in stock** as of 2026-09-07 at **USD 9.04**
> (bare, non-soldered header pins).
>
> **PCB revision status:** LilyGO has never published a numbered revision for this board. The
> only schematic is one undated-by-version sheet whose title block reads **2024-04-29**, and it
> disagrees with at least one shipping board — see
> [`gaps-and-conflicts.md`](gaps-and-conflicts.md). Treat "T-Display-S3" as a *rolling* design.
>
> Research retrieved **2026-09-07**. No physical hardware was available; nothing here is
> hardware-verified by this pass, and every claim is labelled.

**Part of the [T-Display-S3 family](../t-display-s3-shared/README.md)**, which is a
name rather than a platform — eleven boards, eight display controllers, four different
chargers. Read the family hub before assuming code ports.

---

## Identity and variants

| | |
|---|---|
| Marketed name | **T-Display-S3** (LilyGO also writes it *T-Display S3*, *LILYGO T-Display-S3*, and the ESP32 core calls the board target `lilygo-t-display-s3`) |
| Predecessor | **TTGO T-Display** (ESP32, 1.14″ 135×240) — [lineage](../t-display-ttgo/README.md) |
| Sibling on the same PCB | **[T-Display-S3 Touch](../t-display-s3-touch/README.md)** — identical schematic, panel swapped |
| Add-on boards sold for it | **T-Display TF Shield** (microSD, `H609`/`H610`), **T-Display-S3 MIDI** shield (`H656`), **T-Display-S3 Shell** (`L929`/`L930`), **T-Display keyboard** |
| Not the same thing | T-Display-S3 **AMOLED**, **Long**, **Pro** — different PCBs entirely |

Purchase options that are **not** revisions, and are frequently mistaken for them: header
soldered vs not; grey vs black shell; with/without a 700 mAh battery; China/US/Germany
warehouse. The regional SKUs (`USH577`, `DEH577`, `K204US`, `K204-DE`) are the same board at a
higher price — see [`market-and-pricing.md`](market-and-pricing.md).

## What it is and visual identification

A 62 × 26 mm ESP32-S3 board dominated by a 1.9-inch landscape IPS strip bonded to the front,
with a USB-C port on the short edge, a JST 1.25 mm battery socket beside it, and two 12-pin
0.1″ header rows down the long edges. Two tactile buttons sit on the long edge next to USB-C
(`BOOT`/GPIO0 and `RST`), and a third (GPIO14) on the opposite edge.

Fastest positive identification without opening anything:

- **Green LED lit while on USB** → the `V3V` rail indicator (`LED8`). If it is *off* while the
  board is on battery, GPIO15 has not been driven high.
- **Red LED** → charge status (`LED1`). *Flashes or glows dimly when no battery is connected*,
  solid while charging, off when full — this specific behaviour is documented by LilyGO and is
  a good "is it a genuine board" check.
- **Touch vs non-touch**: the Touch panel has a glass overlay that extends past the active
  area and a slightly thicker bezel; electrically, scan I²C on GPIO17/18 — a device at `0x15`
  (CST816S) or `0x1A` (CST328) means Touch. **A non-touch board still pulls GPIO16/17 high**,
  so pin behaviour alone will not tell you.

## Product history, family and culture

Announced and listed 2022-07-15, six weeks after the GitHub repo was created (2022-06-13). It
became LilyGO's most successful board by community metrics: **1 169 GitHub stars and 273
forks** on `Xinyuan-LilyGO/T-Display-S3` as of 2026-09-07, more than double any other board in
the family and second in the whole organisation only to the original `TTGO-T-Display`
(1 192★) which it replaced.

Full dated lineage: [`product-history-and-family.md`](product-history-and-family.md).

## Key specifications

| Function | Part | Interface | Component record |
|---|---|---|---|
| SoC | **ESP32-S3R8** — bare die, *not* a module; 8 MB in-package OPI PSRAM | — | [`espressif/esp32-s3r8`](../../../components/espressif/esp32-s3r8/README.md) |
| Flash | **Winbond W25Q128JV**, 16 MB, QIO 80 MHz (`U3`) | quad SPI | [`winbond/w25q128jv`](../../../components/winbond/w25q128jv/README.md) |
| Display controller | **Sitronix ST7789V** (`ST7789V_SPEC_V1.4.pdf` ships in the repo) | 8-bit Intel-8080 | [`sitronix/st7789v`](../../../components/sitronix/st7789v/README.md) |
| Panel | 1.9″ IPS, 170 × 320, window offset 35 columns | — | — |
| Backlight driver | **Awinic AW9364DNR** (`U4`), 4-channel LED boost | GPIO38 enable / one-wire | [`awinic/aw9364`](../../../components/awinic/aw9364/README.md) |
| Touch (Touch SKU only) | **Hynitron CST816S** (early) or **CST328** (later) | I²C `0x15` / `0x1A` | [`hynitron/cst816d`](../../../components/hynitron/cst816d/README.md) · [`hynitron/cst328`](../../../components/hynitron/cst328/README.md) |
| Li-ion charger | **TP4065** per schematic (`U6`); a shipping board was found carrying a 5-lead TSOT-23 marked `65b311` instead | — | [`nanjing-top-power/tp4065`](../../../components/nanjing-top-power/tp4065/README.md) · [unidentified `AXPM65611`/`65b311`](../../../components/unidentified/lilygo-t-display-s3-family/axpm65611/README.md) |
| 3.3 V LDO | **AP2112K-3.3** (`U7`), schematic lists **RT9013** as the alternate | — | [`diodes-incorporated/ap2112k`](../../../components/diodes-incorporated/ap2112k/README.md) |
| Rail gate | `Q2`/`Q3` **SI2301**, `Q4` **SI2307** P-channel MOSFETs, driven by GPIO15 | — | — |
| USB | **native ESP32-S3 USB** on GPIO19/20 → 16-pin Type-C receptacle (`U5`). **No UART bridge fitted** | USB 1.1 FS | [`generic/usb-c-interface`](../../../components/generic/usb-c-interface/README.md) |
| Crystal | 40 MHz (`U1`) | — | — |
| Antenna | on-board ceramic + a **`RX`/`RX2` 0 Ω resistor pair** to switch to u.FL | — | [`generic/ceramic-antenna`](../../../components/generic/ceramic-antenna/README.md) |
| Battery connector | JST **1.25 mm** 2-pin, 3.7–4.2 V | — | — |
| Expansion | 2 × 12-pin 0.1″ headers, 1 × 4-pin SH1.0 I²C ("Qwiic-like", **not** Qwiic-compatible) | — | — |
| microSD | **not fitted** — only via the T-Display TF Shield | 1-bit SDMMC | [`generic/micro-sd-sdmmc`](../../../components/generic/micro-sd-sdmmc/README.md) |

Electrical envelope, from LilyGO's own table: USB-C in **5 V**; battery **3.7–4.2 V**;
header `VBUS` = 5 V (**output only**, cannot back-feed); header `VBAT` = 4.2 V; **the 3V header
pin is rated for ≤ 100 mA**. That last figure is the one people miss when hanging sensors off
the header.

Full map: [`pinouts-and-buses.md`](pinouts-and-buses.md).

## Architecture and components

Bare-die ESP32-S3R8 with external QIO flash and no module can. The design consequence that
matters: **GPIO26–37 are consumed by the in-package OPI PSRAM** and are simply not available,
which is why a 45-pin-capable chip exposes so few usable pins here once the 8-bit LCD bus takes
another thirteen.

Power is a two-stage arrangement — USB-C 5 V or battery → charger/path → AP2112K LDO → a
**gated `V3V` rail** controlled by GPIO15. Almost every "my board is dead on battery" report
resolves to that gate. See [`features/power-and-battery.md`](features/power-and-battery.md).

## Common tasks / How do I…?

| I want to… | Guide |
|---|---|
| get anything on the screen at all | [`features/display.md`](features/display.md) |
| choose between TFT_eSPI, Arduino_GFX and LovyanGFX | [`features/display.md`](features/display.md) → and [`guides/hardware/parallel-8080-lcd-buses.md`](../../../guides/hardware/parallel-8080-lcd-buses.md) |
| make it work on battery (it "does nothing") | [`features/power-and-battery.md`](features/power-and-battery.md) · [`features/usb.md`](features/usb.md) |
| read the battery voltage correctly | [`features/battery-voltage-measurement.md`](features/battery-voltage-measurement.md) |
| change the charge current | [`features/power-and-battery.md`](features/power-and-battery.md#changing-the-charge-current) |
| use the touch panel | [`features/touch.md`](features/touch.md) |
| use the buttons and wake from them | [`features/buttons.md`](features/buttons.md) |
| add a microSD card | [`features/microsd.md`](features/microsd.md) |
| get Wi-Fi/BLE range that is not terrible | [`features/wifi-and-ble.md`](features/wifi-and-ble.md) |
| sleep at low current | [`features/deep-sleep.md`](features/deep-sleep.md) |
| use the headers, I²C and the SH1.0 connector | [`features/gpio-and-expansion.md`](features/gpio-and-expansion.md) |
| flash it / un-brick it | [`development.md`](development.md) · [`factory-firmware.md`](factory-firmware.md) |
| know which Arduino core version to use | [`development.md`](development.md#arduino-core-versions) |
| run ESPHome / Tasmota / MicroPython on it | [`projects-and-community.md`](projects-and-community.md) |

## Distinctive strengths

- **Price-to-pixels.** USD 9.04 for an ESP32-S3 with 16 MB flash, 8 MB OPI PSRAM *and* a
  bonded 170×320 IPS panel is, as of 2026-09-07, the cheapest way to get all four in one part.
- **The parallel bus is genuinely fast.** 8-bit 8080 at 16 MHz beats the SPI-driven 240×240
  boards it competes with for full-screen refresh, which is why it is the default LVGL demo
  board for a lot of people.
- **Enormous community mass.** 1 169★/273 forks, plus ESPHome, Tasmota and MicroPython support
  that all name the board explicitly. Almost any question has already been asked.
- **Real 16 MB flash and 8 MB PSRAM**, not the 4 MB/no-PSRAM of most cheap display boards.

## Shortcomings and constraints

- **VBUS is not brought out**, so the battery cannot be charged from anything but USB-C.
  Reported [2022-11-07](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/42), never fixed;
  LilyGO's own answer was "maybe you can solve it by soldering a wire from VBUS."
- **No battery protection on board.** LilyGO's maintainer, 2025-02-06:
  *"No built-in battery protection, needs to be used with a lithium-ion battery with battery
  protection."* Use a protected cell.
- **Charge current is fixed at roughly 500–580 mA** by a soldered resistor, which is above 1C
  for the 350–400 mAh cells that physically fit the shell.
- **GPIO16/17 carry fitted pull-ups even on non-touch boards**, and GPIO43/44 are unusable
  under Arduino. Between those and the PSRAM pins, the genuinely free GPIO count is small.
- **The vendor pins the Arduino core at 2.0.14** and TFT_eSPI is documented as broken above it.
- **Antenna performance is a recurring complaint** — [issues #123](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/123),
  [#340](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/340). The u.FL switch exists but
  requires moving a 0 Ω resistor.

## Performance summary

See [`performance.md`](performance.md). Short version: no independent benchmark of this board
was located, and none is reproduced here. LilyGO publishes no current figures for the base
board (it does for the AMOLED boards). What *is* evidenced is the 16 MHz pixel clock LilyGO
chose, their own warning that raising or lowering it causes visible tearing, and ESPHome's
more conservative 10 MHz.

## Pricing and availability

Dated observations, all from LilyGO's own store feed on **2026-09-07**:
bare board **USD 9.04**, soldered **9.54**, Touch **12.61/13.02**, with shell **13.22**,
MIDI shield alone **15.47**. US and German warehouse stock of several SKUs was **out of
stock**. Full table, marketplace and clone pricing: [`market-and-pricing.md`](market-and-pricing.md).

## Competitors, equivalents and clones

[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) compares against
boards already documented here — Waveshare ESP32-S3-Knob-Touch-LCD-1.8, Seeed XIAO ESP32S3
Sense, M5Stack Cardputer ADV — and against the obvious rivals, and contains the worked
clone example that [`guides/markets/clones-and-variants.md`](../../../guides/markets/clones-and-variants.md)
asks for.

## Images and teardown/PCB views

No image was retained by this pass; rights for LilyGO's product photography were not
established and no third-party teardown with clear licensing was found. What exists and where
to get it is catalogued with provenance in [`media/manifest.json`](media/manifest.json), which
also records the two PCB photographs LilyGO's maintainer posted into
[issue #313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313) — the most useful
"where are the pull-up resistors" images in existence, and GitHub-hosted.

## Community, editorial and project coverage

[`projects-and-community.md`](projects-and-community.md) (software, firmware, ESPHome/Tasmota
/MicroPython status) and [`community.md`](community.md) (forums, Reddit, issue-tracker
findings, each labelled by evidence class).

## Documentation map

`pinouts-and-buses.md` · `resources-and-conflicts.md` · `development.md` ·
`factory-firmware.md` · `features/` · `examples/` · `acquisition/` · `coverage.md` ·
`compatibility-and-status.md` · `gaps-and-conflicts.md` · `performance.md` ·
`market-and-pricing.md` · `comparisons-and-recommendations.md` ·
`product-history-and-family.md` · `projects-and-community.md` · `community.md` ·
`sources.md` · `research-log.md` · `commands.md`

## Artifact layout

Board-level artifacts for this PCB live in the **[shared platform
record](../t-display-s3-shared/README.md#5-shared-artifacts-held-here)**, because the
schematic and factory firmware cover the Touch variant too and storing them twice would be
wrong. Chip datasheets live under their component records, per repository policy — including
the `ST7789V_SPEC_V1.4.pdf`, `CST816S` register guide and `CST328` datasheet that LilyGO ships
inside this *board* repository.

## Known conflicts and unresolved identities

Six, listed with evidence and what would settle each, in
[`gaps-and-conflicts.md`](gaps-and-conflicts.md). The two that matter most:
the **charger part number does not match shipping hardware**, and the two factory firmware
images that claim to be different are **byte-identical**.
