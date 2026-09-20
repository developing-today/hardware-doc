# LilyGO T-Dongle-S3 — lineage stub

> **Stub record.** A relative, not a T-Display-S3 variant. Store handle `t-dongle-s3`,
> published **2022-10-20**, SKUs from **USD 10.99** (up to 16.49). In stock 2026-09-07.
> Repo `Xinyuan-LilyGO/T-Dongle-S3` @ **`f279831ee660346f29afd5c9a589394c1758a843`**, MIT,
> **412★** — the third-most-starred display board in the organisation.
> Research retrieved 2026-09-07. No hardware.

## Identity

| | | Source |
|---|---|---|
| Format | a **USB-A dongle**: the board *is* the plug | store, repo |
| Description | *"An ESP32S3 development board that can freely use WIFI, BLE, TF, LED, TFT_LCD functions."* | repo description |
| Display | **0.96″ 80 × 160 ST7735** on SPI | `TFT_eSPI` `Setup209_LilyGo_T_Dongle_S3.h` ships in the T-Display-S3 repo's vendored TFT_eSPI |
| Storage | **microSD on board** — unlike the T-Display-S3 | repo description |
| RGB LED | APA102/WS2812-class, driven by the vendored `FastLED` | tree listing |
| IR | `IRremoteESP8266` vendored | tree listing |
| Board variants | `boards/dongles3.json`, `dongles3-plus.json`, `dongles3-dual.json` — **three** PlatformIO board definitions in one repo | tree listing @ `f279831` |

## Relationship to the T-Display-S3

Shares the ESP32-S3, the native-USB flashing path, the `USB CDC On Boot` trap, and the
Arduino-core pinning culture. **Shares no PCB, panel, bus or pin map.** Its display is a
different controller (ST7735) on a different bus (SPI).

Two things it has that the T-Display-S3 does not, and which are the reasons to choose it:
**an on-board microSD slot** (the T-Display-S3 needs a shield) and **a USB-A plug** instead of
a socket, which makes it a dongle rather than a module.

**Three board JSONs** (`dongles3`, `dongles3-plus`, `dongles3-dual`) in one repository is the
same revision-drift pattern documented family-wide in
[`../t-display-s3-shared/board-revision-drift.md`](../t-display-s3-shared/board-revision-drift.md)
— multiple hardware variants behind one product name, distinguished only by a build target.

## Gaps

**Stub.** No schematic retrieved, no artifacts, no component records, no pinout table, and the
three board variants were not differentiated. Documented only to the depth needed to place it
in the family.
