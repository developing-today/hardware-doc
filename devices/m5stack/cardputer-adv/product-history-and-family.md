# Cardputer family — history, timeline and culture

> Snapshot **2026-09-04**. Dates are sourced individually; the three kinds of "launch date"
> M5Stack produces (Shopify `created_at`, Shopify `published_at`, and `docs.m5stack.com/en/history`)
> are **not** the same thing and are labelled as such.

## Timeline

| Date | Event | SKU | Source |
|---|---|---|---|
| 2023-10-10 … 10-16 | First `M5Cardputer` library commits — examples, USB keyboard demo, `v1.0.1` release | K132 | library git log |
| 2024-01-19 | `sdcard` example added | | library git log |
| 2024-12-25 | `mic_wav_record` demo added | | library git log |
| **2025-03-07** | **Cardputer v1.1** created **and** published on the store, same day | K132-V11 | Shopify `created_at`/`published_at` |
| 2025-03-07 | `add8b6f` "fix button reference issues, use M5.getButton method" | | library git log |
| **2025-06-20** | **ADV schematic file stamp** — `Sch_M5CardputerAdv_v1.0_2025_06_20_17_19_58` | K132-Adv | artifact filename |
| **2025-07-03 / 07-04** | Cardputer Accessory Kit v1.1 (M5StampS3A + display) created / published, $9.95 | — | Shopify |
| **2025-08-29** | `c331c7d` *"basic extract"* — the M5Cardputer library's keyboard reader is refactored behind an interface **in preparation for the ADV** | | library git log |
| **2025-09-01** | `630bcfc` vendored `Adafruit_TCA8418`; `6928513` *"add basic tca8418 reader"*; `db011a8`, `c2fbc89` fixes; `9e9ad46` REPL UI example; `7e97cc8` version bump | | library git log |
| **2025-09-02** | `8ab9f43` **PR #9 "add-cardputer-adv-support"** merged | | library git log |
| **2025-09-04** | Cardputer ADV **created** on the store | K132-Adv | Shopify `created_at` |
| **2025-09-05** | Cardputer ADV **published** — public availability | K132-Adv | Shopify `published_at` |
| 2025-09-28 | `0b23b2c` *"fix modifier handle before normal key"* | | library git log |
| **2026-01-04** | **Cap LoRa-1262** released, category *"For Cardputer-Adv"* | U214 | `docs.m5stack.com/en/history` |
| 2026-02-27 | **Plai** Meshtastic client first beta — r/CardPuter ↑153, 139 comments | | Reddit |
| **2026-04-30** | **Cardputer Mesh Kit** released | K152 | `/en/history` |
| 2026-05-11 / 05-12 | `eccba25` fn-layer support (PR #15), `84e5201` mapping fix — **arrow keys arrive** | | library git log |
| 2026-06-08 | `b549eac0` factory-firmware `CardputerADV` branch head — *"improve boot UX"* | | UserDemo git log |
| 2026-06-22 | Community **Cap TFT-2.8** announced — r/CardPuter ↑989, the pass's highest-scoring hardware post | | Reddit |
| 2026-07-20 / 07-21 | `5604284`, `f1392858` — `M5Cardputer` **1.1.1** head | | library git log |
| **2026-08-28** | **Cap CC1101 & NFC** released, *"For Cardputer-Adv"* | U219 | `/en/history` |
| **2026-09-04** | Cardputer **v1.1 listed as `[EOL]`** on M5Stack's own store; ADV in stock at $29.90 | | Shopify `suggest.json` |
| *pending* | **CardputerZero** — Kickstarter ran spring 2026; docs page carries a *"Work in progress"* banner | C154 / C155 | docs, Reddit |

Two things fall out of that ordering.

**The library led the product by three days.** ADV support was merged into `M5Cardputer` on
2025-09-02; the store record was created on 2025-09-04. M5Stack ships software before hardware,
which is why "update your library" is the first answer to almost every ADV problem.

**The CAP ecosystem is the ADV's second act.** The board shipped in September 2025 with an
expansion header and nothing to plug into it. The first CAP board arrived **four months later**
(2026-01-04) and the second **eleven months later** (2026-08-28). The community filled the gap
in between — the Cap TFT-2.8 predates the Cap CC1101 by two months.

## The family

| Product | SKU | Class | Core | Keyboard | Status 2026-09-04 |
|---|---|---|---|---|---|
| **Cardputer** | K132 | MCU | StampS3 (ESP32-S3FN8) | 74HC138 matrix | superseded |
| **Cardputer v1.1** | K132-V11 | MCU | **Stamp-S3A** | 74HC138 matrix | **`[EOL]`** |
| **Cardputer ADV** | K132-Adv | MCU | Stamp-S3A | **TCA8418 I²C** | current, $29.90 |
| **Cardputer Mesh Kit** | K152 | bundle | = ADV + Cap LoRa-1262 | = ADV | current, $48.00 |
| **CardputerZero** | C154 | **Linux** | Raspberry Pi CM0 (BCM2837, 4×A53, 512 MB) | **46-key**, TCA8418 | *work in progress* |
| **CardputerZero-Lite** | C155 | Linux | as C154, no bundled SD card | as C154 | *work in progress* |
| Cardputer Accessory Kit | — | spare | StampS3 + display | — | superseded |
| Cardputer Accessory Kit v1.1 | — | spare | **M5StampS3A** + display | — | current, $9.95 |
| Cap LoRa-1262 | U214 | CAP module | — | — | $14.50 |
| Cap CC1101 & NFC | U219 | CAP module | — | — | $18.95 |

Records: [`cardputer-v1.0`](../cardputer-v1.0/README.md) ·
[`cardputer-v1.1`](../cardputer-v1.1/README.md) ·
[`cardputer-zero`](../cardputer-zero/README.md) ·
[`cardputer-mesh-kit`](../cardputer-mesh-kit/README.md) ·
[`cap-lora-1262`](../cap-lora-1262/README.md) · [`cap-cc1101`](../cap-cc1101/README.md).

## Shared DNA, and where it stops

Three things travel across the whole line:

1. **The 84 × 54 mm card format** and the LEGO-compatible magnetic base.
2. **The keyboard matrix**, identical between v1.0, v1.1 and ADV — same switches, same `Y0..Y7`
   nets, same 22 Ω series resistors. Only the scanner changed.
3. **The `TCA8418` and the `EXT 2.54-14P` connector**, which the ADV introduced and the
   CardputerZero inherited — even though the Zero is a completely different computer.

Where it stops: the **CardputerZero shares almost no silicon with the ADV.** It is a
Raspberry-Pi-CM0 Linux machine with a bigger 320 × 170 display, a 46-key keyboard, a camera, a
magnetometer, an **RTC**, a **fuel gauge**, an **M5IOE1** I/O expander, USB host/slave switching
and Ethernet. The family resemblance is industrial design plus two component choices.

The r/CardPuter thread of 2026-05-31 captures the confusion this causes better than any spec
sheet. u/G33K_FISH: *"FYI, the ADV and the Zero are different. The Zero will be linux based. You
can do things on the Zero you can not do on the ADV and vise versa."*

## Culture

The Cardputer's community is disproportionately large and unusually *productive* — it makes
things rather than just discussing them. Three dedicated subreddits (**r/CardPuter**,
**r/CardPuterZero**, and heavy traffic in **r/M5Stack**), an official Discord, two curated
awesome-lists (`terremoth/awesome-m5stack-cardputer` ★734, `ru84r8/Cardputer-firmware-list`),
and 100+ GitHub repositories.

Two cultural currents dominate:

* **"Cheap Flipper Zero."** Explicit in the threads — *"I want to turn Cardputer Adv in budget
  Flipper zero alternative"* (r/CardPuter 2026-06-27, ↑88), and in the firmware names. Bruce,
  Marauder and Evil-M5Project all live here. It is also why the platform attracts more
  attention than a $30 dev board otherwise would.
* **Cyberdeck and pocket-computer romance.** r/cyberDeck 2026-06-22, ↑710. The mod scene
  (external antennas, XL cases, dual screens, 3D-printed key caps) is large.

A third current appeared in **mid-2026 and is specific to the ADV**: a **music scene**, made
possible entirely by the ES8311 codec and the 3.5 mm jack. Grooveboxes, synths and a pocket DAW
all appeared between June and August 2026. No such projects exist for the v1.x, because the v1.x
has no line out.

## Positioning, then and now

**At launch (September 2025)** the ADV was a $29.90 refresh of a popular $29.90 board, and the
case for upgrading was not obvious to an existing v1.x owner: same SoC, same flash, same screen,
same price. The pitch was the peripherals.

**By late 2026** the picture has inverted. The v1.1 is `[EOL]`, Meshtastic upstream supports
only the ADV, the entire CAP accessory line is ADV-only, and new community projects target the
ADV by default. The v1.x is now the compatibility case, not the default.

See [`comparisons-and-recommendations.md`](comparisons-and-recommendations.md) for buying
guidance dated to this snapshot.
