# T-Display-S3 — community evidence

Every item is labelled by evidence class:
**FM** firsthand measurement · **FO** firsthand ownership/use · **DP** demonstrable project ·
**VC** vendor confirmation · **II** informed interpretation · **HS** hearsay/unsupported.

Sampling is stated where a prevalence claim would otherwise be implied. **No claim below is a
prevalence claim** unless it names its sample.

## The issue tracker is the primary community source

318 issues on `Xinyuan-LilyGO/T-Display-S3`, retrieved 2026-09-07. Selection rule for deep
reading: **≥5 comments or ≥2 reactions**, then filtered for technical content → 56 candidates,
22 read in full.

Nearly all are closed, most by a stale-bot after 30 + 14 days. **The bot closes threads, not
questions** — several of the most valuable findings sit in threads marked "closed as inactive".

### Highest-value threads

| # | Title | Date | c | Finding | Class |
|---|---|---|---|---|---|
| [230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230) | T-Display-S3 Battery Charge Circuit? | 2024-03-02 | 9 | Owner traced the PCB: the charger is **a 5-lead TSOT-23 marked `65b311`**, not the SOP-8 part in the schematic. Also the correct `analogReadMilliVolts` recipe. LilyGO confirms **no battery protection** (2025-02-06) | **FM + VC** |
| [313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313) | Pins 16 and 17 in floating mode | 2025-07-28 | 11 | Fitted pull-ups on GPIO16/17 **on non-touch boards**; pins go high again on deep-sleep entry. LilyGO answered **with two PCB photographs** and offered removal instructions | **FO → VC** |
| [190](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/190) | Measure BAT_ADC incorrect voltage | 2023-09-22 | 17 | ESP-IDF `raw*3.3/4096` gave **2.14 V** against a multimeter's **3.9 V**. Wrong in a plausible-looking way | **FM** |
| [212](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/212) | Firmware_no_Touch is the same as Touch? | 2024-01-02 | 9 | Independent notice of the byte-identical firmware pair; **and** the `User_Setup_Select.h` overwrite fix, which resolved the reporter's problem | **FO** |
| [42](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/42) | Can not charge the battery via IO PIN | 2022-11-07 | 10 | `VBUS` not on the header. LilyGO: *"We have not considered this situation. Maybe you can solve it by soldering a wire from VBUS."* Later (2023-11-01) a firsthand back-powering hazard report | **FO + VC** |
| [79](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/79) | If you are having difficulty with your new T-Display S3 | 2023-01-03 | 11 | The GPIO15 trap, and the community guide that documents it. LilyGO's maintainer thanked the author in-thread | **DP + VC** |
| [313→](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/326) 326 | TFT_eSPI Setup206 `#error` | 2026-02-23 | 11 | The `User_Setup_Select.h` problem now fails loudly at compile time rather than silently at runtime | **FO** |
| [18](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/18) | Tasmota support | 2022-10-06 | 25, 4👍 | Tasmota works via `Tasmota32-S3 (QIO/OPI)` + the "Lilygo S3 Display" template. **`displaydimmer 100` is required** or the screen looks dead. A Tasmota maintainer participated | **FO** |
| [151](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/151) | Black screen with TFT | 2023-05-19 | **32** | The single largest thread on the repo, and it is the `User_Setup_Select.h`/GPIO15 pair again | **FO** |
| [205](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/205) | Power with external 3.3 V / 5 V | 2023-11-30 | 22 | Supported inputs are USB-C and the JST connector only. Answers are **community**, not vendor | **II** |
| [181](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/181) | None of my Qwiic sensors is recognized | 2023-08-08 | 12 | The SH1.0 connector is **not** Qwiic pin-compatible | **FO** |
| [168](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/168) | Constant I²C errors with touch | 2023-06-29 | 21 | CST parts NAK while idle | **FO** |
| [12](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/12) | Where is the schematic for this board | 2022-09-19 | 9, **7👍** | The most-upvoted issue on the repo is *"please publish the schematic"* — a fair summary of the documentation culture | **—** |

### Recurring themes, with counts from the read sample

Of the **22 threads read in full**:

| Root cause | Threads |
|---|---|
| `User_Setup_Select.h` not selecting Setup206 | 5 |
| GPIO15 not driven | 4 |
| Battery / charging / ADC | 5 |
| `USB CDC On Boot` or port enumeration | 4 |
| Wi-Fi range or connection | 2 |
| Flash size / partition scheme | 2 |

Those are counts **within the deliberately biased sample** (selected for engagement), not
across all 318 issues. They indicate what generates long threads, not what happens most often.

## Reddit

Search method: `old.reddit.com/search.json` with a link-preview User-Agent (the standard
`www.reddit.com` path returns 403 to scripts), four query shapes, `t=all`, 25 results each →
**27 family-relevant posts**. Two threads read in full.

### The single most useful community post

[r/esp32, 2026-05-25, "LilyGo T-Display S3 Clock with DS18B20 and PIR — lessons learned"](https://old.reddit.com/r/esp32/comments/1tnop7r/lilygo_tdisplay_s3_clock_with_ds18b20_and_pir/)

| Claim | Class | Note |
|---|---|---|
| "GPIO 43 and 44 are blocked by UART0 in Arduino IDE **even when using Hardware CDC**" | **FM, independently reproduced** | A second commenter (`u/MrBoomer1951`) initially disputed it, tested, and retracted: *"OKAY! I just tried it and it does not work on 43 or 44! TIL"*. This is the strongest single piece of community evidence in the whole record |
| "`ledcSetup` and `ledcAttachPin` are deprecated in core 3.x — use `ledcAttach`/`ledcDetach`" | **FM** | Confirms the core-3.x break extends past TFT_eSPI |
| "needs **both** GPIO 15 (LCD power) and GPIO 38 (backlight) set HIGH" | **FO** | Matches the vendor README |
| "5 GHz WiFi doesn't work on ESP32-S3" | **II** | Correct, and silicon-level, not board-level |
| "The UART0 pins can be used if you disabled it in sdkconfig (esp-idf). Harder to do in Arduino." | **II, untested** | A plausible workaround nobody in-thread verified |
| MakerFocus 3.7 V 1000 mAh #952540 fits a printed backpack for the LilyGO shell | **FO** | A dated, specific, working battery combination — rare and useful |

### Visibility, dated

| Post | Sub | Date | Score |
|---|---|---|---|
| ESP32 Internet Weather Station | r/esp32 | 2024-08-16 | 1312↑ / 68c |
| DIY auto gauge UI (LVGL) | r/esp32 | 2025-03-11 | 840↑ / 61c |
| "Finally AMOLED display on the development board" | r/arduino | 2023-05-31 | 987↑ / 76c |
| same, cross-posted | r/esp32 | 2023-05-31 | 400↑ / 32c |
| "This is T-display S3… internet weather station" | r/arduino | 2023-05-20 | 583↑ / 17c |
| "The LILYGO T-Display-S3 Amoled is quite good" | r/Esphome | 2024-10-19 | 65↑ |
| Bitcoin ticker on the AMOLED | r/esp32 | 2024-09-11 | 184↑ |

**Interpretation, offered as interpretation:** the high-scoring posts are almost all *finished
projects with a photograph*, and the help requests score near zero. Reddit is where this board
is shown off; GitHub is where it is debugged.

### A negative result worth keeping

[r/arduino, 2026-06-11, "T-Display S3 AMOLED Touch schematics accurate?"](https://old.reddit.com/r/arduino/comments/1u3et4u/tdisplay_s3_amoled_touch_schematics_accurate/) —
an owner reported that driving GPIO13 broke touch on an AMOLED Touch board, suspected the
schematic was wrong, and **two days later retracted**: *"today, I cannot reproduce the
behavior. Must have been something else."* Recorded because the thread is findable, the
retraction is not prominent, and the intermediate hypothesis (that LilyGO's schematic is wrong
about GPIO13) would otherwise propagate. The thread also surfaced `LilyGo-Display-IDF`'s
`product_pins.h` — which turned out to be one of the best sources in this whole pass.

## Not searched

Hackaday, YouTube, Bilibili/Zhihu/CSDN, the ESP32 forum, and Discord. Deliberate exclusions,
recorded in [`research-log.md`](research-log.md).
