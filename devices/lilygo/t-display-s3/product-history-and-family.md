# T-Display-S3 — product history, family and culture

## Dated timeline

| Date | Event | Evidence |
|---|---|---|
| ~2019 | **TTGO T-Display** (ESP32, 1.14″ 135×240 ST7789 on SPI) establishes the format: a cheap ESP32 with a bonded colour strip. It becomes LilyGO's most-starred repo ever — **1 192★** | `Xinyuan-LilyGO/TTGO-T-Display` |
| 2021-09-08 | `LilyGO-T-DisplayGD32` — the same format on a GD32. A dead end (41★) | org listing |
| 2022-06-13 | `Xinyuan-LilyGO/T-Display-S3` repository created | GitHub API |
| **2022-07-15** | **T-Display-S3 listed for sale** | store `published_at` |
| 2022-07-18 | T-Dongle (ESP32-S2) listed | store |
| 2022-09-21 | T-QT Pro listed | store |
| 2022-09-23 | `LilyGo-T-Display-S2` last pushed — the S2 line ends | org listing |
| 2022-10-06 | Tasmota support requested ([issue #18](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/18)); working by 2023-01 | issue |
| 2022-10-20 | T-Dongle S3 listed | store |
| 2022-11-07 | [Issue #42](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/42): `VBUS` not on the header. Never fixed | issue |
| 2022-11-12 | T-Display AMOLED Lite listed — first AMOLED in the line | store |
| 2023-01-03 | [Issue #79](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/79): the community setup guide that documents the GPIO15 trap LilyGO's own docs did not | issue |
| 2023-02-09 | T-Display TF Shield listed | store |
| 2023-02-17 | `T-Display-S3-AMOLED` repo created | GitHub API |
| 2023-03-24 | T-Display-S3 Shell listed | store |
| **2023-04-14** | **T-Display-S3 AMOLED (1.91″) listed** | store |
| 2023-05-20/31 | The board goes visibly mainstream on Reddit: r/arduino "This is T-display S3…" (583↑) and "Finally AMOLED display on the development board" (987↑ on r/arduino, 400↑ on r/esp32) | Reddit |
| 2023-08-09 | `LilyGo-AMOLED-Series` created — one library for the whole AMOLED line | GitHub API |
| 2023-08-17 | `T-Display-S3-Pro` repo created | GitHub API |
| 2023-08-22 | `T-Display-S3-Long` repo created | GitHub API |
| 2023-09-07 | **T-Display-S3 Pro listed** | store |
| 2023-10-27 | **T-Display-S3 Long listed** | store |
| 2023-11-03 | **T4-S3 (2.41″ AMOLED) listed** | store |
| 2024-03-02 | [Issue #230](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/230): an owner traces the PCB and finds the charger is not the part in the schematic | issue |
| **2024-04-29** | Title-block date on the only published base-board schematic | `T_Display_S3.pdf` |
| 2024-07-18 | **T-Display S3 AMOLED (DS)** listed — one page, four round/small panels | store |
| 2024-08-02 | LilyGO adds the README note that **TFT_eSPI does not work above Arduino core 2.0.14** | README |
| 2024-08-09 | `T-Display-S3-AMOLED` repo's **last push** — superseded by `LilyGo-AMOLED-Series` | GitHub API |
| 2024-10-31 | **T-Display-S3 AMOLED Plus** listed — BQ25896, RTC, microSD | store |
| 2025-01-09 | Newest base-board factory image (`lvgl-demo`), still built on Arduino core 2.0.14 | app descriptor |
| 2025-07-28 | [Issue #313](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/313): LilyGO confirms the GPIO16/17 pull-ups with PCB photos | issue |
| 2025-11-28 | "T-Display S3 Pro External" listed | store |
| 2026-01-28 | T-Dongle C5 listed — the ESP32-C5 era begins | store |
| 2026-07-03 | **T-Display C5** listed (ESP32-C5, ST7789 1.9″ touch, **AXP2602** PMU, CST816S) — the direct successor concept | store + repo description |
| 2026-07-27 | Duplicate `t-display-s3-copy` store listing appears | store |
| 2026-08-11 | **T-Display SF32** listed (SiFli SF32) | store |
| 2026-08-20 | T-Display K230 Kit listed | store |
| 2026-08-31 | Last push to `Xinyuan-LilyGO/T-Display-S3` — **still actively maintained after four years** | GitHub API |
| 2026-09-07 | This snapshot. Board in stock at USD 9.04 | store |

## Lineage

```
TTGO T-Display (ESP32, 1.14" SPI, ~2019, 1192*)
   │
   ├─ T-Display-GD32 (2021)            — dead end
   ├─ T-Display-S2   (→2022)           — dead end
   ├─ T-Display-RP2040 (→2023)         — dead end
   │
   └─ T-DISPLAY-S3 (ESP32-S3, 1.9" 8080 parallel, 2022-07, 1169*)   ← this board
        ├─ T-Display-S3 Touch                    (same PCB)
        ├─ T-Display-S3 AMOLED 1.91"  (2023-04)  ├ QSPI AMOLED branch
        │    └─ AMOLED Plus           (2024-10)  │  + BQ25896, RTC, microSD
        ├─ T-Display-S3 AMOLED DS 1.43/1.64/1.75 (2024-07)
        ├─ T4-S3 2.41" AMOLED         (2023-11)
        ├─ T-Display AMOLED Lite 1.47"(2022-11)  — actually predates the AMOLED 1.91"
        ├─ T-Display-S3 Long 3.4"     (2023-10)  — AXS15231B bar display
        └─ T-Display-S3 Pro 2.33"     (2023-09)  — SPI ST7796S, camera, 3 buttons
                                                   └─ Pro MVSRBoard / MVSRLora backplates

        successors reusing the "T-Display-" prefix on other silicon:
        T-Display-C5 (ESP32-C5, 2026-07) · T-Display-P4 (ESP32-P4, 2025-12)
        T-Display-K230 (Kendryte, 2025-03) · T-Display-SF32 (SiFli, 2026-08)
        T-Display-CM0 (2026-09)
```

**The AMOLED Lite predates the AMOLED 1.91″ by five months** (2022-11 vs 2023-04), despite the
"Lite" name implying it is a cut-down later model. It is not — it is the first AMOLED board,
built around a different controller (SH8501B behind a level shifter) and a different PMU
(AXP2101), and it is the *odd one out* rather than a simplification.

## Cousins that share the name but not the design

`T-Deck`, `T-Deck-Pro`, `T-Deck-MAX`, `T-Panel`, `T-Encoder-Pro`, `T-Circle-S3`,
`T-Keyboard-S3`, `T-Display-Bar`, `T-Touchbar-AMOLED`, `T-FPGA`. All ESP32-S3, all separate
PCBs. `T-Display-Bar` and `T-Touchbar-AMOLED` are particularly easy to confuse with the
T-Display-S3 Long; they are different boards with different repos.

## Culture

The most striking thing about this board's community is that **the best documentation is not
LilyGO's**. `teastainGit/LilyGO-T-display-S3-setup-and-examples` was written by an owner in
January 2023 because the vendor documentation omitted the GPIO15 requirement, and it is linked
from dozens of issue threads. LilyGO's own maintainer endorsed it in-thread on 2023-03-13:
*"Thank you for bringing more clear and concise examples."* Three years later the vendor README
has absorbed the GPIO15 note — but the third-party guide is still the one people are pointed
at.

The second pattern is **vendor responsiveness without vendor process**. `lewisxhe` answers
issues quickly, accurately, and often with photographs of the PCB — the GPIO16/17 pull-up
answer is a good example. What does not happen is any of that reaching the documentation, a
revision number, or a changelog. The knowledge lives in closed GitHub issues.
