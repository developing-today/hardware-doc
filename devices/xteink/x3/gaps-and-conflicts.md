# Xteink X3 — gaps and conflicts

Snapshot **2026-09-04**.

## Conflict 1 — the RTC part. Three sources, three answers.

| Source | Class | Claim |
|---|---|---|
| FreeInk SDK `BoardConfig.h:915` | firmware, driven in production | **`RtcType::Ds3231`** at **0x68** |
| Imgur teardown, image 13 caption | firsthand photograph of the marking | **"DS1307 RTC"** |
| `sunwoods/Xteink-X3` BOM | firsthand teardown, Chinese | **"DS系列RTC时钟芯片"** — *DS-series*, deliberately unnarrowed |

**All three are consistent with I²C address 0x68**, which both the DS1307 and the
DS3231 use — so the address does not discriminate.

**Why this is not trivially resolved:**
- The DS1307 and DS3231 have **different register maps beyond the timekeeping
  bytes** and different supply requirements (the DS1307 is nominally a 5 V part;
  the DS3231 has an integrated TCXO). Getting it wrong affects accuracy and any
  use of alarms or the temperature register.
- A firmware driver working does **not** prove the part: `XteinkDetect` only reads
  `DS3231_SEC_REG = 0x00`, the seconds register, which is **identical on both**.
  So the SDK's `Ds3231` label may itself be an assumption that has never been
  falsified.
- The Chinese author explicitly **refused to narrow it**, which is the behaviour of
  someone who looked at the marking and could not read it confidently.

**Status: unresolved.** The component is filed as
[`components/unidentified/xteink-x3-x4/rtc-ds-series/`](../../../components/unidentified/xteink-x3-x4/rtc-ds-series/README.md)
rather than under Maxim/Analog Devices, per the skill's rule against promoting a
candidate to a finding.

**What would settle it:** a legible photograph of the chip's top marking, or
reading register `0x11`/`0x12` — the DS3231's temperature registers, which the
DS1307 does not have.

## Conflict 2 — GPIO0 and GPIO20 are each assigned twice

| Pin | Assignment A | Assignment B |
|---:|---|---|
| **0** | `batteryAdc = 0` | `X3_I2C_SCL = 0` |
| **20** | `usbDetect = 20` | `X3_I2C_SDA = 20` |

Same SDK, same commit. Both pairs cannot be live.

**Hypothesis (not a finding):** `batteryAdc` and `usbDetect` were copied from the
X4 profile and are dead here — the X3 has a **BQ27220 gauge** and does not need an
ADC battery sense.

**What would settle it:** the schematic sketch at
`artifacts/teardown/sunwoods-cn/02.jpg`, **which is held in this repository and has
not been read.** This is the cheapest unresolved question in the whole subject.

## Conflict 3 — the vendor's product page describes features the device lacks

The `xteink.com` X3 listing claims *"adjustable warm light settings"* and
*"Cloud sync"*. **The X3 has no frontlight** — `NO_FRONTLIGHT` in the board
profile, no frontlight in either teardown, and the X4 Pro is the only Xteink with
one. The copy is AI/SEO boilerplate.

Recorded prominently because it is the justification for the rule applied across
this whole tree: **no vendor prose is used as evidence.**

## Conflict 4 — community price

A community post lists the X3 at **$79** ([r/XTEINK `1v5gh6x`](https://old.reddit.com/r/XTEINK/comments/1v5gh6x/),
2026-07-24) while the vendor API shows **$69.00** on 2026-09-04. Could be a price
cut, or an error. Not resolved.

## Unresolved identities

| Part | Known | Missing |
|---|---|---|
| **ESP32-C3 variant** | Family only, from two teardowns | Exact package/suffix. **No part number asserted** |
| **Puya flash** | *"PUYA 128Mbit"* | Part number |
| **Charger IC** | *"TP4056-class"* | Actual part |
| **NFC tag IC** | *"ISO/IEC 14443A tag"* | Part, and **what it is for** |
| **Panel module** | Controller only (UC8253 / UC8279d) | Module/glass part number, supplier |
| **Battery cell** | **650 mAh**, connectorised | Cell part/format |

## The NFC tag — the largest open question about this device

An **ISO/IEC 14443A tag** is on the board and NFC is an advertised feature. But:

- It appears in **no** board profile, **no** firmware string, and **no** driver.
- It is a **passive tag** — nothing on the host bus.
- **Nobody has explained what it does.** Candidate uses: accessory/case
  identification, authenticity, or a "tap to open the file manager" phone hand-off.
  All speculation.

Not a single English-language source discusses it. See [`features/nfc.md`](features/nfc.md).

## Gaps — firmware

| Item | Status |
|---|---|
| Stock X3 images V1.0.7 / V5.2.13 (CN+EN, full **and** OTA) | Exist as **Git LFS blobs** in `zocs/eink-quick-flasher`; **not fetched** |
| An X3 flash dump | **Not obtained.** Only the X4's was |
| SPIFFS contents | Not extracted |
| **UC8279d variant** | *"Pending hardware validation — no UC8279 X3 unit has been on the bench yet"* |

## Gaps — measurement

**No power measurement exists**, despite the teardown being performed expressly to
make one. No runtime, no sleep current, no refresh timing for the UC8253.

## Gaps — regulatory

No FCC ID, CE or SRRC record read. **Board photographs now exist in this
repository**, so unlike the other models an FCC/SRRC ID could plausibly be **read
off the PCB silkscreen** — an unexplored, cheap avenue.

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 109:* No FCC ID, CE or SRRC record read. **Board photographs now exist in this
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

Listed in [`scratch/index-merge/corrections-requiring-review.md`](../../../scratch/index-merge/corrections-requiring-review.md).
