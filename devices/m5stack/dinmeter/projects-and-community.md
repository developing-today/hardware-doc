# DinMeter — projects, community and ecosystem

**Retrieved 2026-09-04.** Search depth, queries and negative results are in
[`research-log.md`](research-log.md). Applies to K134 and K134-V11 — no project found
distinguishes between them.

Every item is labelled by evidence type: **demonstrable project** (code exists and builds are
published) · **reproduced documentation** (restates the vendor) · **firsthand report** ·
**hearsay** · **marketing**.

---

## 1. The headline: this device has almost no public community

That is a finding, not a gap in the search. Stated precisely, with the sample:

| Search | Result |
|---|---|
| GitHub repository search, `DinMeter in:name,description,readme` | **19 repositories**, of which **13** actually target the device (the rest are Launcher forks that inherit the board list, or false positives on "DIN") |
| GitHub code search, `M5DinMeter extension:h` | 9 files across 6 repositories |
| `old.reddit.com/search.json`, three query forms, 150 results inspected | **exactly one** relevant post |
| `community.m5stack.com` search | API returns HTTP 401 (login required); HTML search page returns 200 but is a JS shell — **no thread could be enumerated** |
| ESPHome | **zero** — `repo:esphome/esphome dinmeter` → 0 results |
| Tasmota | **zero** — `repo:arendst/Tasmota dinmeter` → 0 results |
| Meshtastic | **zero** — `repo:meshtastic/firmware dinmeter` and `din_meter` → 0 results each |

For comparison, the same repository holds a Waveshare knob device with an
[ESPHome confirmation document](../../waveshare/esp32-s3-knob-touch-lcd-1.8/esphome-and-clone-confirmation.md)
because that ecosystem exists. **The DinMeter's does not.** If you need Home Assistant
integration you will be writing it yourself, or using M5Stack's own UiFlow2 → Home Assistant
path.

**Prevalence caveat.** "Almost no community" is a statement about *public, indexed* activity on
GitHub and Reddit on 2026-09-04. M5Stack's own forum could not be enumerated (see above), and
Chinese-language platforms (Bilibili, CSDN, Taobao Q&A) were not searched. Do not read this as
"nobody uses it".

---

## 2. Firmware platforms that support it

### Bruce / M5Launcher — `bmorcelli/Launcher` ★2054 · MIT · **demonstrable project**

The most significant third-party support by a wide margin, and the only one with CI-built
binaries.

| Field | Value |
|---|---|
| Repository | <https://github.com/bmorcelli/Launcher> |
| Created / last push | 2024-02-10 / **2026-09-04** (actively maintained) |
| Board target | `boards/m5stack-dinmeter/platformio.ini` |
| CI | `.github/workflows/main.yml` builds `{ env: "m5stack-dinmeter" }` on every release |
| Distributed as | `Launcher-m5stack-dinmeter.bin`, MD5 `bccbefef5284357a2a7c3c7cc196fd98`, mapped in `support_files/m5burner_post.py` — i.e. **shipped through M5Burner** |
| Status in README | listed twice, once as `[x] Port to M5-DinMeter` and once as `[ ] (Beta) M5-DinMeter port` — **the README contradicts itself**; the CI matrix and the MD5 map both say it ships |

Its board file is also a genuinely useful **independent corroboration** of the pin map, from a
party with no reason to copy M5Stack's table wrongly. Retained at
[`artifacts/source-snapshots/`](artifacts/source-snapshots/) — key lines:

```ini
board = esp32s3
board_upload.flash_size = 8MB
build_unflags = -DBOARD_HAS_PSRAM          ; ← confirms: no PSRAM
-DARDUINO_USB_MODE=1  -DARDUINO_USB_CDC_ON_BOOT=1
-D HAS_ENCODER=1   -DROTATION=3
-DTFT_WIDTH=135 -DTFT_HEIGHT=240 -D TFT_IPS=1
-DTFT_CS=7 -DTFT_DC=4 -DTFT_RST=8 -DTFT_MOSI=5 -DTFT_SCLK=6 -DTFT_MISO=-1 -DTFT_BL=9
-D TFT_COL_OFS1=52  -D TFT_ROW_OFS1=40     ; ← the GRAM gap, third independent source
-D TFT_COL_OFS2=53  -D TFT_ROW_OFS2=40
-DSDCARD_CS=13 -DSDCARD_SCK=15 -DSDCARD_MISO=2 -DSDCARD_MOSI=1
; No PMIC on DinMeter: battery is a plain ADC divider on GPIO10 (ratio 2.0,
; matching M5Unified's board table)
-DANALOG_BAT_PIN=10
lib_deps = mathertel/RotaryEncoder @1.5.3
```

Two things worth extracting:

1. **It bit-bangs an SD card across both Grove ports.** `SDCARD_CS=13`, `SCK=15` (PORT.A) and
   `MISO=2`, `MOSI=1` (PORT.B). That is a real, shipped demonstration that the four Grove signals
   can be used as a software SPI bus — see
   [`features/porta-portb-expansion.md`](features/porta-portb-expansion.md).
2. **It confirms the battery divider ratio is 2.0**, matching the schematic's `R7`/`R8` 1 MΩ +
   1 MΩ pair. Independent of M5Stack.

A separate note in `boards/lilygo-t-lora-pager/interface.cpp` says that board's quadrature pins
are *"swapped on purpose … opposite to lilygo-t-embed-cc1101/m5stack-dinmeter"* — so the
DinMeter's A/B ordering is treated as the reference convention in that codebase.

**Forks that inherit DinMeter support** (lineage preserved, not separately verified):
`notyetaperson/Evilware`, `darkLabz001/Dark-Div-Launcher`,
`TeslaDeathStar/ESP32-Launcher-ES3C28P`, `ry-ops/tab5-launcher`, `JunFactorya04/M-5Laucher{,2}`.
These are copies of the board list, not independent ports.

### `viniciusbo/m5-palnagotchi` ★81 · MIT · **demonstrable project**

A Pwnagotchi companion. Created 2024-02-14, last push 2026-01-28. `palnagotchi/ui.h` references
`M5DinMeter`. Fork `pfefferle/palnagotchi` ★1 (2026-03) carries the same. The second-most-starred
project touching the device.

### UiFlow2 / MicroPython — `m5stack/uiflow-micropython` · **vendor**

DinMeter appears in both `.gitlab-ci.yml` and `.github/workflows/build-firmware.yml`. This is
the vendor's own MicroPython firmware and the backing for the UiFlow2 tutorial at
`docs.m5stack.com/en/uiflow2/m5dinmeter/program`.

### `mattytrentini/chipboard` · **demonstrable project (unverified)**

`boards/m5stack_din_meter.yaml` — a board definition for generic MicroPython. Not built or
evaluated here. Vanilla `micropython/micropython` has **no** DinMeter port.

### `espressif/esp-board-manager` · **vendor-adjacent, primary**

Not a "project" so much as first-party ESP-IDF board support from Espressif:
`m5stack_boards/m5stack_dinmeter/{board_info,board_devices,board_peripherals}.yaml`, HEAD
`2beb9b22b0892b343bd555a1ebc9929a7edce8fc` (2026-09-03). Its comments are the single best
technical writing about this board that exists anywhere, M5Stack included — it documents the
GRAM offset, the PCNT decoder pattern, an ESP32-S3-specific build break, and it resolves the
GPIO3/GPIO42 ambiguity in M5Stack's own pin table by citing M5Unified. Fully quoted in
[`development.md`](development.md) §2a.

---

## 3. Application projects

| Project | Stars | Language | Licence | Last push | What it is | Evidence type |
|---|---:|---|---|---|---|---|
| [`no-body-in-particular/m5din-hikoki`](https://github.com/no-body-in-particular/m5din-hikoki) | **25** | C++ | — | 2026-05-05 | HiKOKI power-tool battery analyser | demonstrable project |
| [`Shark17e/M5DinMeter-KilnController`](https://github.com/Shark17e/M5DinMeter-KilnController) | 1 | C++ | NOASSERTION | 2026-08-08 | Ceramic-kiln controller: PID with auto-correction, temperature curves | demonstrable project |
| [`kaz-mac/M5Authenticator`](https://github.com/kaz-mac/M5Authenticator) | 2 | C | MIT | 2025-04-26 | TOTP 2FA device; has a dedicated `src/DinMeterUI.h` | demonstrable project |
| [`TuF3i/DinMeterDock`](https://github.com/TuF3i/DinMeterDock) | 0 | C | MIT | 2026-06-27 | Desktop dock controller (Chinese) | demonstrable project |
| [`aoiastro/susuFW`](https://github.com/aoiastro/susuFW) | 1 | — | — | 2025-09-26 | Multi-function firmware for the DinMeter (Japanese) | demonstrable project |
| [`shi78ge/DinMeter-chan`](https://github.com/shi78ge/DinMeter-chan) | 1 | C++ | NOASSERTION | 2024-04-15 | Character/mascot display — the earliest third-party project found, six weeks after launch | demonstrable project |
| [`tarmn3/m5dinmeter-ble-volume-knob`](https://github.com/tarmn3/m5dinmeter-ble-volume-knob) | 0 | C++ | none | 2025-12-10 | BLE HID volume knob | demonstrable project |
| [`Yuichiroh-Kobayashi/DinMeter_ScrambleMDtest`](https://github.com/Yuichiroh-Kobayashi/DinMeter_ScrambleMDtest) | 0 | — | MIT | 2026-06-03 | test sketch | demonstrable project |
| [`todateman/Chibi-T_Furoshiki_Heater`](https://github.com/todateman/Chibi-T_Furoshiki_Heater) | 1 | C++ | NOASSERTION | 2026-08-15 | Heater controller | demonstrable project |
| [`AH2005NA/m5stick-shark`](https://github.com/AH2005NA/m5stick-shark) | — | C++ | — | — | `Defines.h` references M5DinMeter | demonstrable project |
| [`jd3096-mpy/micropython-Coin-Operated-Beverage-Machine`](https://github.com/jd3096-mpy/micropython-Coin-Operated-Beverage-Machine) | 0 | Python | MIT | 2025-07-10 | MicroPython vending machine | demonstrable project |
| [`3110/m5stack-platformio-boilerplate-code`](https://github.com/3110/m5stack-platformio-boilerplate-code) | — | C++ | — | — | `include/main.hpp` includes a DinMeter branch | demonstrable project |

**Observations across the set.** Nine of the twelve are one-person single-purpose instruments —
a kiln, a battery tester, a heater, a volume knob, an authenticator. That is the DinMeter being
used for exactly what it looks like it is for. There is no framework, no library ecosystem, no
"awesome-dinmeter" list, and no project has more than 25 stars.

**Nationality skew.** Of the identifiable authors, the projects are Japanese, Italian, Chinese
and Brazilian. This is a product with a distributed, low-density user base rather than a
concentrated scene.

---

## 4. Reddit

Searched via `old.reddit.com/search.json` with UA `WhatsApp/2.23.20.0` (which returns HTTP 200
where `www.reddit.com` returns 403 — see
[`../../../ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md)). Three
query forms, ~150 results inspected, plus a subreddit-restricted pass.

**One relevant result in the entire index:**

| Date | Sub | Score | Comments | Post | Type |
|---|---|---:|---:|---|---|
| 2026-01-30 | r/M5Stack | 22–23 | 1 | ["Check out what's new this week!"](https://old.reddit.com/r/M5Stack/comments/1qr0ju2/check_out_whats_new_this_week/) — the official M5Stack weekly-products post announcing DinMeter v1.1 alongside the LLM-8850 Kit | **marketing** (vendor-posted) |

Its body text is the same paragraph as the v1.1 product page. It has **one** comment. This is
the *entire* Reddit footprint of the product line and it corroborates the launch date
(2026-01-30), which independently matches the shop listing's `created_at`.

The other search hits matching "DIN meter" were about **ski-binding release settings**
(r/Skigear) — a genuine homonym trap worth recording so the next agent does not re-chase it.

---

## 5. M5Stack community forum — could not be enumerated

| Attempt | Result |
|---|---|
| `https://community.m5stack.com/api/search?term=dinmeter&in=titlesposts` | **HTTP 401** — `{"status":{"code":"not-authorised","message":"A valid login session was not found."}}` |
| `https://community.m5stack.com/search?term=dinmeter&in=titlesposts` (browser UA) | HTTP 200, 16 986 bytes — a NodeBB **JS shell**; no results in the served HTML |

The forum runs NodeBB with its search API behind authentication. **No forum thread could be
cited.** This is a blocked source, not an empty one, and it is the largest single gap in this
document. What would fix it: an authenticated session, or Google's `site:community.m5stack.com`
index.

---

## 6. Other sources searched with nothing found

| Source | Query | Result |
|---|---|---|
| Hackaday / Hackaday.io | project search | no DinMeter project located |
| ESPHome | `repo:esphome/esphome dinmeter` | 0 |
| Tasmota | `repo:arendst/Tasmota dinmeter` | 0 |
| Meshtastic | `repo:meshtastic/firmware {dinmeter,din_meter}` | 0 each |
| `pr3y/Bruce` (upstream Bruce) | `repo:pr3y/Bruce dinmeter` | 0 — **support is in `bmorcelli/Launcher`, not in Bruce upstream**. Easy to get wrong |
| AliExpress clones | product search | none found (negative result, not proof of absence) |
| YouTube / video | not systematically searched | **declared exclusion** |
| Bilibili / CSDN / Chinese platforms | not searched | **declared exclusion** |

---

## 7. What a new user should actually do

1. Start from the **vendor examples** in `m5stack/M5DinMeter` — six of them, one per feature.
   See [`examples/best.md`](examples/best.md).
2. For ESP-IDF, read **Espressif's board definition** before writing anything; it will save you
   the GRAM offset and the PCNT build break.
3. If you want a ready-made multi-tool, flash **Launcher** via M5Burner.
4. Do **not** expect ESPHome, Tasmota or Meshtastic. They do not support it.

## Related

[`community.md`](community.md) · [`examples/best.md`](examples/best.md) ·
[`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) ·
[`research-log.md`](research-log.md)
