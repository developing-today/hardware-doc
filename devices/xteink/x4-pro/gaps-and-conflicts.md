# Xteink X4 Pro — gaps and conflicts

> Snapshot **2026-09-04**.

## Active conflicts

### 1. Touch axis flip: the SDK contradicts itself

| Source | Claim |
|---|---|
| `BoardConfig.h:1567` | `flipY = true`, comment: *"swapXY + flipY **(confirmed by corner-tap)**"* |
| `docs/xteink-x4pro-support.md:154` | *"`flipX`/`flipY` **pending** a corner-tap test"* |
| same doc, `:351–353` | *"**Pending** — Touch flip — `flipX`/`flipY` still to confirm with a corner-tap test"* |

Same repository, same commit `2400379`. One says confirmed, two say pending.

**Not resolved here.** The likeliest reading is that the header was updated when
the test was done and the prose doc was not — but that is a hypothesis, not a
finding. **What would settle it:** a corner-tap test on hardware, or the commit
history of `BoardConfig.h:1567` versus the doc.

**Practical impact:** low. Taps register and navigation works either way; only
mirroring is at stake.

### 2. Stock firmware version: 7.4.4 vs V7.4.5

The OTA package `xteink_app_update_x4pro_7.4.4_20260827_133901.xota` has metadata
labelling it **`V7.4.5`** while the embedded app descriptor says **`7.4.4`**.
The SDK states the **descriptor is authoritative**. Recorded so nobody "fixes" a
version string to match packaging.

### 3. Resolved: the "EPD PMIC at 0x63"

An earlier narrative held that I²C `0x63` was a display power-management IC and
that the panel had dead rails needing an external supply. **Refuted.** `0x63` is a
**CW2017 battery fuel gauge** — an I²C register dump showed the classic BATINFO
battery-model curve at `0x10`–`0x3F`. The panel runs off the controller's internal
booster. Recorded because the refuted version is more memorable than the correct
one and keeps resurfacing.

### 4. Resolved: the ADC button ladder

Earlier RE proposed an ADC resistor ladder on GPIO10. **Refuted on hardware** —
this variant has plain digital buttons. The ladder matcher at IROM `0x4201f734`
is real but **vestigial**. It *is* live on the X3 and X4.

### 5. Resolved: GPIO7 as a display enable

Proposed, then refuted: GPIO7 reads `INPUT_PULLUP` and is the **Right button**.

## Gaps — physical

| Unknown | Why it matters | What would close it |
|---|---|---|
| **Battery capacity** | No runtime estimate is possible | A teardown photo of the cell label |
| **Device mass and dimensions** | Only a 250 g *packaged* weight exists | A vendor spec sheet or an owner measurement |
| **Charger IC part** | Not on I²C; unidentified | Teardown |
| **Panel module part number** | Only the controller is known, not the glass/module | Teardown or FPC marking |
| **Antenna type** | Not characterised | Teardown or an FCC internal-photos exhibit |
| **Debug pads / test points** | No known UART or JTAG access | Teardown |
| **PCB revision markings** | No revision scheme is known for this device | Teardown |

**All seven would be closed by one teardown. There is no X4 Pro teardown
anywhere public** — this is the largest single gap in the record.

## Gaps — regulatory

**No FCC ID, CE marking or SRRC certificate has been read for any Xteink device.**
No board photo exists to read one from, so there is no ID to query. Not searched
to completion. An FCC filing would supply internal photographs, antenna details
and RF test data in one document — the highest-value unexplored source.

## Gaps — firmware

| Unknown | Note |
|---|---|
| **No public X4 Pro stock image** | Unlike the X3/X4, no dump or OTA package is downloadable. Your own backup is the only restore path |
| **`.xota` container format** | The SDK refers to *"the decrypted"* app; the encryption is undocumented |
| **OTA feed contents** | `gotaserver.xteink.com/api/check-update` was **not queried** this session — an obvious and cheap next step |
| **USB-MSC** | In stock, not ported to the SDK |
| **`usbDetect` pin** | GPIO10 floated as a candidate but is already the touch INT — treat as wrong |
| **`batteryAdc` pin** | Not isolated |

## Gaps — measurement

**Nothing about this device was measured by this session.** No power draw, no
sleep current, no refresh timing, no runtime, no throughput. The one refresh
figure quoted (~38 ms/plane write @20 MHz) is from the **X4**, same controller,
different board.

## Gaps — market

- **Chinese-market pricing** for the X4 Pro was never captured; only the $99 USD
  store price.
- **The delisted X4 product page** could not be recovered — the Wayback CDX query
  timed out and was not retried.

---

## Round 2 — 2026-09-11

**No line above was altered.**

### Resolved

| Was | Now | By |
|---|---|---|
| No regulatory filing known | **FCC ID `2BTR9-X4PRO`, granted 2026-06-16**; internal photos public **2026-12-12** | fccid.io |
| Manufacturer's legal identity unknown | **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, FRN `0037772233`, `chuchen@xteink.cn` | FCC grantee record |
| No teardown, no stock dump, no price-independent corroboration | **A third party dumped a physical unit twice (identical hashes), read its eFuses, decoded its partitions and traced its I²C and LEDC** | [`kycube/x4pro-emu`](https://github.com/kycube/x4pro-emu/tree/bf4b86ae0471012d4d07c0bb3042f3f561c9c302) |
| Which panel controller ships | **One retail unit: `hw_calib/screenType = 2` → UC8279, and `VER=00 0F 68 00 00 FLG=13` → LUT_VER `0x68` → UC8279.** One unit, not a distribution | same |
| `0x63` identity | **CW2017 fuel gauge**, confirmed on the live bus. The earlier "display PMIC" hypothesis stays refuted | same |
| GPIO7 is the Right button, not a display enable | **Confirmed independently** | same |
| FreeInk support-doc I²C paragraph | **Stale — INT and RST are swapped in the doc.** The struct is correct | same |

### New conflict — X4 Pro touch orientation

| # | Source | Claim | Basis |
|---|---|---|---|
| R2-P1a | FreeInk `BoardConfig.h` | `swapXY=true, flipX=false, flipY=true`, annotated *"confirmed by corner-tap"* | reverse engineering + the author's own corner-tap |
| R2-P1b | `kycube/x4pro-emu` `docs/hardware.md` | repeats FreeInk's values; models them in the emulator | repetition, not an independent test |
| R2-P1c | **`clackups/draftling` `HARDWARE.md`** | FreeInk's values *"had touches landing **180 degrees opposite** of where the finger was"*; corrected to `TOUCH_MIRROR_X`/`TOUCH_MIRROR_Y` = `1`/`0` **against a physical unit** | **on-hardware** |

**Unresolved.** R2-P1c is the only on-hardware claim, but the two projects use
different rendering stacks with different orientation conventions, so a mapping
that is "180° wrong" in one may be correct in the other. **What would settle it:**
one person, one device, both firmwares, four corner taps, reported with the raw
`0x8150` values alongside the rendered coordinates.

This supersedes nothing: the pre-existing conflict — the SDK header says
"confirmed" while its own doc says "pending", **twice** — remains, and now has a
third position.

### New conflict — stock firmware version

**Four numbers, one device.** `7.2.4` (desk unit, ESP-IDF v6.0.1, built
2026-08-14, hardware-read), `7.4.4` (app descriptor), `V7.4.5` (package
metadata), `7.5.4` (a third-party analysis document). Not reconcilable from
public evidence; the vendor publishes no changelog and ships regional and
OTA-staged builds. **Recorded, not resolved.**

### Still open

| # | Gap | What would settle it |
|---|---|---|
| R2-P2 | **The panel pinout is still single-source.** SCLK 12 / MOSI 11 / CS 13 / DC 18 / RST 14 / BUSY 6 traces only to FreeInk; both new firmware custodians cite FreeInk rather than deriving it | **FCC internal photos, 2026-12-12**, or a continuity measurement |
| R2-P3 | Charge-`STAT` polarity on GPIO21 | a multimeter on a charging unit |
| R2-P4 | Refresh timings (~1800 ms full / ~500 ms fast) are inherited from FreeInk's docs; the desk unit's author marks the measurement **pending** | `micros()` around DRF → BUSY on the device |
| R2-P5 | The `XteinkDetect` bit-banged probe **algorithm** has never been independently re-derived | a second reverse engineering, or the permanently-confidential schematic |
