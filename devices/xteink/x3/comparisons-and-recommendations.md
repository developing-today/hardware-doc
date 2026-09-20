# Xteink X3 — comparisons and recommendations

Dated **2026-09-04**. Full cross-model table: [family index](../README.md#cross-model-comparison).

## The X3's case in one paragraph

**The sharpest, lightest and best-instrumented Xteink, and the cheapest one you
can still buy.** ~257 PPI against the 4.26″ models' ~219; 55 g; a real TI fuel
gauge, an RTC, an IMU and an NFC tag that none of the S3 models combine. What you
give up is USB-C charging, button feel, and — on units shipped since ~July 2026 —
a panel controller whose fast waveforms nobody has tuned yet.

## Within the family

| | **X3** | [X4](../x4/README.md) | [X4 Pro](../x4-pro/README.md) | [X4 Classic](../x4-classic/README.md) |
|---|---|---|---|---|
| Price 2026-09-04 | **$69, in stock** | **delisted** | $99 | never priced |
| Screen | 3.7″ **792×528, ~257 PPI** | 4.26″ 800×480, ~219 | 4.26″ 800×480 | 4.26″ 800×480 |
| Mass | **55 g** | ~80 g | unknown | unknown |
| SoC / PSRAM | C3 / none | C3 / none | **S3 / 8 MB** | **S3 / 8 MB** |
| Charging | pogo | **USB-C** | pogo | unknown |
| Touch / frontlight | ✗ / ✗ | ✗ / ✗ | **✅ / ✅** | ✗ / ✗ |
| Fuel gauge | **BQ27220** — best in family, no profile upload | none (bare ADC) | CW2017 (needs BATINFO) | CW2017 |
| RTC | DS-series 0x68 (**part unresolved**) | **none** | BM8563 | BM8563 |
| IMU | **✅ QMI8658** | ✗ | ✗ | ✅ |
| **NFC** | **✅ — only model with it** | ✗ | ✗ | ✗ |
| SD sleep power-down | **✅ GPIO13** | **✗ — no enable pin** | ✅ | ✅ |
| Buttons | 6 (ADC ladder) + power | 6 (ADC ladder) + power | 2 + power | 6 discrete + power |

**Three things stand out.** The cheapest model has the **highest pixel density**;
it has **more sensors than the "Pro"**; and it is the **only one with NFC**.

## Against development platforms in this repository

| Device | Class | Schematic | USB-C | Headers | Verdict vs X3 |
|---|---|---|---|---|---|
| **Xteink X3** | sealed reader | **hand-drawn sketch only** | ✗ (pogo) | ✗ | — |
| [M5Stack PaperMono](../../m5stack/papermono/README.md) | dev board | **✅ published, 6 sheets** | ✅ | ✅ | **Better for development.** Bigger, thicker, no pocketability, no case ecosystem |
| [Waveshare ESP32-S3-ePaper-3.97](../../waveshare/esp32-s3-epaper-3.97/README.md) | dev board | partial | ✅ | ✅ | **ESP32-S3 with PSRAM**, 3.97″ SSD1677 panel, and it also carries a **QMI8658** — closest silicon analogue to an X3 in dev-board form |
| [ZeroWriter](../../zerowriter/) | DIY appliance | ✅ open | ✅ | ✅ | Different purpose — keyboard-first writing appliance |

**Partial substitutes, not equivalents.** None is 55 g, none fits in a pocket,
none has a magnetic back designed to stick to a phone. Conversely the X3 has no
headers, no schematic worth the name, and often a USB lock.

**The honest framing:** if your goal is to *build* something on e-paper, buy a dev
board — you get a schematic and no unlock dance. If your goal is to *read* on
something you can also reprogram, the X3 is the cheapest device in existence that
does both well.

## Direct competitors named by owners

| Device | Community verdict |
|---|---|
| **Murphy 3.7″ (HamGeek/墨菲)** | The closest size competitor. *"Better than XTEINK X4? (Murphy 3.7")"* drew 70 comments; owners call build quality *"pretty dodgy"* and *"unusably thick"* |
| **EEGO** small readers | Raised as an emerging alternative; the FreeInk SDK carries an EEGO A4 profile |
| **OBOOK5** | 219 PPI, 1200 mAh, ~23 GB usable, *"smaller than the boox palmas, and cheaper"* |
| **Boox Picco / Palma** | Android, much more expensive |
| **Kindle PPW 12th gen** | An r/XTEINK thread does a size comparison; different category |

An r/ereader survey thread — *"After Seeing the Xteink X3, I Want an E-Reader with
Under 4″ Screen. What's Available, What's Coming?"* — concluded the sub-4″ market
was *"about to get a bit of a shake-up"*. That was 2026-05-24; the X3 is still the
best-supported option in it.

## The buying decision that actually matters: which panel

Units shipped from ~**July 2026** carry a **UC8279d** instead of a UC8253. There
is **no external marking**. Consequences:

- Require **CrossPoint ≥ 1.5** / **CrossInk ≥ 1.5**, or a fork on a current SDK.
  Older firmware may leave a blank screen, and stale forks on locked units risk a
  soft brick.
- Expect **no grayscale** and probably a **full flash on every page turn** until
  someone tunes UC8279 waveform banks. Only
  [`anki630/crossmosa-freeink-sdk`](https://github.com/anki630/crossmosa-freeink-sdk)
  is working on it.

A firsthand two-unit comparison found a real, visible contrast/speed difference
between X3s bought from different channels — **but never determined which
controller each had**. See [`performance.md`](performance.md).

## Recommendations

| Scenario | Recommendation | Confidence |
|---|---|---|
| **Cheapest currently-buyable Xteink; sharpest text; lightest** | **X3, $69** | high |
| You want a sensor platform (IMU, RTC, real gauge, NFC) in a case | **X3** — nothing else in the family combines them | high |
| You want touch and a frontlight | **X4 Pro ($99)**, not the X3 | high |
| **You need USB-C charging** | **Not the X3.** X4 used, or a dev board | high |
| You want the best button feel | **X4** (used) — owners call the X3's *"mushy and quieter"* | medium (subjective, single source) |
| You want maximum firmware maturity | Either C3 model; the X3 needs **≥ 1.5** | high |
| You are memory-constrained (big books, heavy images) | **An S3 model.** The X3 has no PSRAM and is where OTA OOM was observed | high |
| You are buying used and want to avoid the panel lottery | **You cannot tell before purchase.** Budget for firmware ≥ 1.5 | high |

## Honest limits

- **Nothing about the X3 was measured**, by this session or anyone. No runtime, no
  refresh timing, no sleep current — despite a teardown done expressly to measure
  power.
- Battery capacity (650 mAh) is a **single-source photograph caption**.
- Competitor figures are **community-reported**, not verified.
- The **RTC part is unresolved**, so timekeeping accuracy cannot be compared.

---

## Cross-references added 2026-09-07

Append-only, from a cross-cutting synthesis pass. Nothing above was changed and no
new evidence was gathered.

- [**Handheld and e-ink device landscape, 2026-09**](../../../guides/markets/handheld-and-eink-device-landscape-2026-09.md)
  — the X3 in the pocket-e-ink-reader group alongside the PaperMono, the Waveshare
  ESP32-S3-ePaper-3.97 and ZeroWriter, with an explicit list of the comparisons the
  evidence does **not** support (battery life and refresh speed among them).
- [**Xteink firmware ecosystem**](../firmware-ecosystem.md) — the X3's two board
  profiles (`XTEINK_X3` for UC8253, `XTEINK_X3_UC8279` for the UC8279d batches),
  and the **I²C fingerprint at `0x55`/`0x68`/`0x6B` that tells an X3 from an X4**
  so one C3 binary can serve both.
- [**SoC choice for battery e-ink devices**](../../../guides/hardware/soc-choice-for-battery-eink-devices.md)
  — why the C3's missing PSRAM is the constraint behind this device's observed OTA
  out-of-memory, with the framebuffer arithmetic.
- [**Adding LoRa, NFC and an RGB sidelight to e-ink firmware**](../../../guides/hardware/adding-lora-nfc-and-sidelight-to-eink-firmware.md)
  — ⚠ **read §1.3 before planning anything around "the X3 has NFC".** The fitted
  part is a *passive tag* on no host bus; adding NFC *reading* to an X3 is a
  hardware modification, not a firmware task.
