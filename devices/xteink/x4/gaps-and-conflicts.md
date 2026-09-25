# Xteink X4 — gaps and conflicts

Snapshot **2026-09-04**.

## Conflicts

### 1. GPIO20 — `usbDetect` or I²C SDA?

| Profile | GPIO20 role |
|---|---|
| `XTEINK_X4` | `usbDetect = 20` |
| `XTEINK_X3` (same board family) | `usbDetect = 20` **and** `X3_I2C_SDA = 20` for the BQ27220/DS3231/QMI8658 bus |

The X3 assigns GPIO20 **twice**, to two different functions, in the same SDK.
On the X4 there is no I²C bus so the conflict is latent — but it means
**neither assignment has been verified**, and the X4's `usbDetect` is plausibly
just copied from a template.

**What would settle it:** an oscilloscope on GPIO20 during USB plug/unplug, or a
continuity check to the USB-C connector.

### 2. Stock firmware version is not recoverable from the app descriptor

The dump's `esp_app_desc_t` reports `arduino-lib-builder` / ESP-IDF v4.4.7 /
2024-03-05, which is the **Arduino core's** identity, not the product's. Users see
V5.1.6 / V5.2.13 on screen. **Recorded so nobody reports "2024-03-05" as the
firmware date.**

### 3. Community price vs vendor API

A community post lists *"$69 X4, $79 X3, $99 X4 Pro"*
([r/XTEINK `1v5gh6x`](https://old.reddit.com/r/XTEINK/comments/1v5gh6x/), 2026-07-24)
while the vendor API shows the **X3 at $69**, not $79. The X4 figure could not be
checked because the product is delisted. Community figure not corroborated.

## Unresolved identities

| Part | What is known | What is missing |
|---|---|---|
| **ESP32-C3 variant** | Family-level: a teardown photo captioned *"ESP32-C3 main CPU"* and an independent Chinese BOM saying `ESP32-C3` | **The exact package/suffix has never been read.** With external flash it is likely a bare `ESP32-C3` QFN32, but that is inference. **No part number is asserted anywhere in this record** |
| **Puya SPI NOR flash** | *"PUYA 128Mbit Flash"* (CN BOM), *"128MBit (16MB) flash for firmware"* (EN teardown) | **No part number.** Puya's 16 MB parts include `P25Q128H`-series; **not asserted** |
| **Charger IC** | *"类似TP4056的电池管理芯片"* — TP4056-**class** (X3 board) | Actual part; and whether the X4 uses the same |
| **Panel module** | Controller only | Glass/module part number, supplier |

Per the skill's rule, none of these has been promoted from candidate to finding.
A guessed part number would be worse than "unidentified".

## Gaps — physical

**No X4 teardown was located.** The two teardowns that exist are of the **X3**, a
related but different board. Unknown: PCB layout, revision markings, antenna,
debug pads, battery capacity, connector types.

**The two board revisions** (self-latching vs not) have **no known distinguishing
marking**. This is the most operationally important unknown about the device.

## Gaps — regulatory

No FCC ID, CE or SRRC record read. No board photo exists to read one from.
Not searched.

## Gaps — firmware

| Item | Status |
|---|---|
| Stock V5.1.6 / V5.2.13 OTA images | Known to exist as **Git LFS blobs** in `zocs/eink-quick-flasher`; **not fetched** (needs an LFS-aware client). Cheap to close |
| SPIFFS contents (3.4 MB) | **Not extracted.** Should contain the web file-manager UI |
| OTA feed | `gotaserver.xteink.com/api/check-update` **not queried** |
| Payload signing/encryption | Undetermined. `secure_version = 0` means no anti-rollback |
| The dumped unit's identity | Unknown — which colour, which revision, which stock version |

## Gaps — measurement

The only quantitative figures in this record are the SDK's **~38 ms / ~19 ms**
plane-write timings and the **three-unit ADC ladder readings**. There is no power
measurement, no runtime, no sleep current, no Wi-Fi throughput. The one person who
set out to measure power on this board family
([X3 teardown](../x3/media.md), Nordic PPK II) never published results.

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 59:* No FCC ID, CE or SRRC record read. No board photo exists to read one from.
>

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment authorisations**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

The original finding confused **"no mark visible in a product photograph"** with **"no grant exists"**. Those are different claims, and only the first was tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is ordinary for a device with a screen. **That is a likely explanation and it was not verified.**

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../guides/research/finding-certification-records.md).

Full record, with controls: [`certification-and-compliance.md`](certification-and-compliance.md).

Listed in [`research/passes/index-merge/corrections-requiring-review.md`](../../../research/passes/index-merge/corrections-requiring-review.md).
