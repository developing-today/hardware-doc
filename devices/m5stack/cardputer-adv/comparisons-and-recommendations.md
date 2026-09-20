# Cardputer ADV — comparisons and recommendations

> Snapshot **2026-09-04**. Prices are M5Stack's own store for the ADV; competitor prices are
> **not** dated observations from this pass unless marked. Where I have no dated price, I say so
> rather than quoting a remembered number.
>
> Genre context: [`guides/markets/`](../../../guides/markets/README.md) —
> [`device-comparison-matrix.md`](../../../guides/markets/device-comparison-matrix.md),
> [`clones-and-variants.md`](../../../guides/markets/clones-and-variants.md).

## 1. Cardputer ADV versus Cardputer v1.1

The comparison most people actually face, because both are on sale at **the same $29.90**.

| | Cardputer v1.1 (`[EOL]`) | **Cardputer ADV** |
|---|---|---|
| Price 2026-09-04 | $29.90 | $29.90 |
| SoC / flash / PSRAM | ESP32-S3FN8 / 8 MB / **none** | **identical** |
| Display | ST7789V2 240×135 | **identical** |
| Keyboard feel | 56 keys | 56 keys, **160 gf specified** |
| Free GPIO for your project | **0** (Grove only) | **7** on the CAP header |
| Audio out | class-D to a speaker | **codec + amp + 3.5 mm jack** |
| Audio in | PDM mic | **analog MEMS via codec ADC** |
| IMU | — | **BMI270** |
| Battery | 120 + 1400 mAh, separate base | **1750 mAh, one piece** |
| Expansion modules available | none | **two official, several community** |
| Upstream Meshtastic | ❌ | ✅ |
| Weight | 90.0 g | **81.0 g** |
| Lifecycle | **end of life** | current |

**Recommendation: there is no scenario at parity pricing in which the v1.1 is the better buy.**
The only reasons to choose it are (a) you already own one, or (b) you specifically need a
firmware that has not been ported — and the honest list there is short and shrinking
(Evil-M5Project's ADV support is unconfirmed; NEMO has no ADV config).

**If you already own a v1.1:** upgrade only if you want the jack, the IMU or the CAP header. The
compute, screen and radio are unchanged, and every ESP32-S3 project you have runs on both.

## 2. Cardputer ADV versus LilyGO T-Deck

| | Cardputer ADV | LilyGO T-Deck / T-Deck Plus |
|---|---|---|
| SoC | ESP32-S3 | ESP32-S3 |
| **PSRAM** | **none** | **8 MB** ⭐ |
| Display | 1.14″ 240×135 | 2.8″ 320×240, **touch** ⭐ |
| Keyboard | **56 keys, full QWERTY row, 160 gf** ⭐ | BlackBerry-style membrane keypad, trackball |
| LoRa | via **CAP module** (+$14.50) | **on board** (SX1262) ⭐ |
| GNSS | via CAP LoRa module | Plus variant only |
| Audio | **codec + amp + 3.5 mm jack** ⭐ | I²S speaker, no jack |
| IMU | BMI270 ⭐ | — |
| Expansion | **14-pin CAP socket** ⭐ | headers, no module ecosystem |
| Price | **$29.90 (dated)** | *not observed in this pass* |
| Meshtastic | ADV variant | multiple long-standing variants |

**The two differences that decide it: PSRAM and screen size.** If you are writing a GUI, running
LVGL, buffering audio or holding a large font in RAM, the T-Deck's 8 MB of PSRAM removes the
single hardest constraint on the Cardputer platform. If you are typing — text, chat, terminal,
tracker patterns — the Cardputer's key layout is materially better than a BlackBerry keypad.

Not equivalents. **Partial substitutes**, and which is "better" depends entirely on whether your
bottleneck is memory or input.

⚠ **I did not retrieve a dated T-Deck price**, so this is a capability comparison, not a
value comparison.

## 3. Cardputer ADV versus Nicolai Electronics Tanmatsu

[`devices/nicolai-electronics/tanmatsu`](../../nicolai-electronics/tanmatsu/README.md)

| | Cardputer ADV | Tanmatsu |
|---|---|---|
| Processor | ESP32-S3, 2×LX7 @240 MHz | **ESP32-P4** + companion radio ⭐ |
| Memory | 512 KB, **no PSRAM** | far larger; MIPI DSI display pipeline |
| Display | 1.14″ SPI | **MIPI DSI** ⭐ |
| Keyboard | 56 keys, rubber dome | full QWERTY, Solder Party keyboard family |
| LoRa | CAP module | **on board** ⭐ |
| Expansion | 14-pin CAP | **36-pin expansion port** ⭐ |
| **Openness** | schematic PDF only; **no EDA source**, no published licence | **full KiCad under CERN-OHL-P**, firmware MIT, Sphinx docs in git ⭐⭐ |
| App ecosystem | ~100 GitHub repos, no app store | **AppFS + BadgeLink**, 57 catalogued apps |
| Origin | Shenzhen consumer product | Dutch hacker-camp badge lineage, low volume |
| Price | **$29.90 (dated)** | several times that — *not observed in this pass* |

These are **not competitors**; they are different answers to "I want a hackable handheld".

* Choose the **Tanmatsu** when openness is the requirement — you need the schematic *source*,
  you need to modify the hardware, you need a documented app framework, or you need P4-class
  compute and a real display pipeline.
* Choose the **Cardputer ADV** when price is the requirement, when you want the largest possible
  body of existing firmware to draw on, or when you want to buy ten of them.

One honest asymmetry worth naming: the **Tanmatsu record in this repository is better than this
one can be**, because Nicolai publishes KiCad. Several findings there exist only because the PCB
was parsed. For the Cardputer, the best available primary evidence is a PDF render and the
vendor's own firmware — which is why this record leans so hard on M5Unified, M5GFX and the
factory HAL.

## 4. Other things people actually cross-shop

| Device | Why it comes up | The real difference |
|---|---|---|
| **Flipper Zero** | the cultural reference point — *"budget Flipper zero alternative"*, r/CardPuter 2026-06-27 | Flipper has integrated sub-GHz, NFC, iButton, IR RX and a polished UX. The ADV needs a Cap CC1101 (+$18.95) and community firmware to approach it, and even then the IR receiver is missing. **Cheaper, not equivalent.** |
| **LilyGO T-Embed CC1101 Plus** | r/M5Stack, **2026-09-04**: *"which one should i get? m5stack cardputer adv or t embed c1101 plus?"* | T-Embed integrates CC1101 and has a rotary encoder; no keyboard. Choose by input method. |
| **CardputerZero (C154)** | same brand, same shape, running Linux | **A different class of machine.** Quad A53, 512 MB, camera, Ethernet, RTC, USB host. Not a faster ADV — a small Linux computer. u/G33K_FISH, r/CardPuter 2026-05-31: *"You can do things on the Zero you can not do on the ADV and vise versa."* |
| **PicoCalc** | pocket-computer scene overlap | `jblanked/Picoware` targets both |
| **Waveshare ESP32-S3 boards** | r/M5Stack 2026-08-13: *"Need help deciding between a waveshare and cardputer adv"* | Waveshare sells screens-and-MCU; the Cardputer sells a *keyboard* and a firmware ecosystem |

## 5. When to use / when not to use

**Use the Cardputer ADV when:**

* You want a **pocket device you type on** — chat, mesh messaging, notes, terminal, SSH, tracker
  sequencing. This is what it is best at and what nothing else at the price does.
* You want **Meshtastic in your pocket with a keyboard**. Buy the Mesh Kit ($48).
* You want the **largest ready-made firmware library** on a handheld ESP32.
* You want to **build an expansion board** and would rather use a documented socket than a
  soldering iron.
* You want to make music on a $30 device — the 2026 groovebox/synth/DAW scene is real and is
  ADV-only.

**Do not use it when:**

* You need **PSRAM**. Large framebuffers, LVGL, big fonts, sizeable audio buffers, ML models —
  512 KB is the wall, and the community's cleverest work is all about getting round it. Buy a
  T-Deck or a P4-class board.
* You need **wall-clock time** without a network or GNSS. There is no RTC.
* You need **IR receive**, **NFC**, or **sub-GHz** out of the box.
* You need **motion-wake from deep sleep** — no IMU interrupt line was established.
* You need **certification paperwork**. None is published (see
  [`gaps-and-conflicts.md`](gaps-and-conflicts.md)).
* You need **open hardware source**. You get a PDF, and no licence statement.
* You need a **serviceable battery** or guaranteed spares.

## 6. Alternatives by tier

| Tier | Pick | Why |
|---|---|---|
| **Cheapest keyboard handheld** | **Cardputer ADV, $29.90** | nothing else has 56 keys at this price |
| Cheapest *with* LoRa | **Cardputer Mesh Kit, $48.00** | licensed Meshtastic, antenna included |
| Cheapest with sub-GHz + NFC | ADV + Cap CC1101, $48.85 | still needs community firmware |
| **Memory-constrained work** | **LilyGO T-Deck (8 MB PSRAM)** | the ADV's hard wall is exactly what this removes |
| **Larger screen / touch** | T-Deck, or an ADV + community Cap TFT-2.8 | the Cap route keeps the good keyboard |
| **Open hardware, hackable** | **Tanmatsu** | CERN-OHL-P KiCad, MIT firmware, real docs |
| **Polished security tool** | Flipper Zero | integration and UX, at a much higher price |
| **Linux in the same shape** | CardputerZero (C154) — *when it ships* | still marked "work in progress" |
| **Buy used** | — | no used-market data was gathered; no recommendation offered |

## 7. What would change these recommendations

* A **PSRAM-equipped Cardputer** would remove the main reason to look elsewhere.
* An **RTC** — even a $0.30 PCF8563 — would remove the main functional gap.
* **Published certification** would open commercial and educational deployments.
* **EDA source** in `M5_Hardware` would make third-party CAP boards much easier and would let
  the next pass on this device parse a netlist instead of cropping a PDF.

---

## Cross-references added 2026-09-07

Append-only, from a cross-cutting synthesis pass. Nothing above was changed and no
new evidence was gathered.

- [**Handheld and e-ink device landscape, 2026-09**](../../../guides/markets/handheld-and-eink-device-landscape-2026-09.md)
  — the ADV against the v1.1, the LilyGO T-Display K230 Kit ($263.56 complete), the
  Tanmatsu (~€120) and the CardputerZero, plus a separate group covering the Caps
  and the Grove LoRa units. It makes explicit the thing casual comparisons get
  wrong: **the ADV is not a faster Cardputer** — same ESP32-S3FN8, same 8 MB flash,
  same *no PSRAM*; the change is the keyboard scanner, and the seven GPIOs it frees
  *are* the Cap header.
- [**SoC choice for battery e-ink devices**](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  — the `FN8` (flash, no PSRAM) versus `R8` (PSRAM, no flash) distinction, why it
  is the most consequential fact about every Cardputer, and this record's
  **310.89 µA → 6.84 µA Stamp-S3 → Stamp-S3A sleep** figures used as the worked
  example that **board sleep current is a power-tree property, not a SoC
  property**. It also carries the Cardputer's memory-mapped 2.16 MB Unicode font as
  the canonical no-PSRAM workaround.
- [**Adding LoRa, NFC and an RGB sidelight to e-ink firmware**](../../../guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md)
  — the two Caps are used there as **the reference implementation** for adding
  radios to an existing device, with the Cap-Bus pin map and the Cap CC1101's
  one-GPIO band-switching trick (`RF_SW1` driven from the CC1101's own `GDO2`). It
  also imports this platform's **`BL_3V3` lesson** — that PWM-dimming the backlight
  browns out the WS2812 — as the mistake to avoid when adding an LED to a device
  whose frontlight you also intend to dim.
- [**Xteink firmware ecosystem**](../../xteink/firmware-ecosystem.md) — the ADV's
  G8/G9 pull-up board autodetect is catalogued there alongside four other runtime
  fingerprints, with the shared lesson that **a fingerprint testing a proxy rather
  than the thing itself will eventually misfire**.
