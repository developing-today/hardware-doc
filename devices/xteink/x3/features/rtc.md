# X3 — real-time clock

> **The part is not established.** Three sources give three answers, all at I²C
> address 0x68. 2026-09-04.

| Property | Value |
|---|---|
| Address | **0x68** |
| Bus | I²C SDA **20** / SCL **0** @ 400 kHz |
| SDK type | `RtcType::Ds3231` |
| Component record | [`unidentified/xteink-x3-x4/rtc-ds-series`](../../../../components/unidentified/xteink-x3-x4/rtc-ds-series/README.md) |

## The conflict

| Source | Claim |
|---|---|
| FreeInk SDK `BoardConfig.h:915` | **DS3231** |
| Imgur teardown, image 13 caption | **"DS1307 RTC"** |
| `sunwoods/Xteink-X3` BOM | **"DS系列RTC时钟芯片"** — *DS-series*, unnarrowed |

**The address does not discriminate**: the DS1307 and DS3231 both live at 0x68.

**And the firmware does not either.** `XteinkDetect` probes only
`DS3231_SEC_REG = 0x00` — the seconds register — which is **identical on both
parts**. So the SDK's `Ds3231` label is an assumption that has never been
falsified by the code that appears to test it.

## Why it matters

| | DS1307 | DS3231 |
|---|---|---|
| Timekeeping registers | same layout at 0x00–0x06 | same |
| Accuracy | External crystal, **no compensation** | **Integrated TCXO**, ±2 ppm |
| Temperature registers | **none** | `0x11`/`0x12` |
| Alarms | none | two |
| Nominal supply | 5 V part | 2.3–5.5 V |

Drift on an e-reader that shows a clock is a user-visible difference. Alarms and
temperature readback are simply absent on one of them.

## How to resolve it

**Read registers `0x11` and `0x12`.** The DS3231 returns a temperature there; the
DS1307 does not implement them. One I²C read settles it.

Alternatively, a legible photograph of the chip's top marking. The existing
teardown photo (`13-Ay3rpJg.jpg`, 5760×3240) is archived in this repository and
**has not been examined at full resolution** — the caption may or may not be
supported by the image.

## Cross-device note

The S3 devices — [X4 Pro](../../x4-pro/features/rtc.md) and X4 Classic — use a
**BM8563 at 0x51**, a completely different part at a different address. The
[X4](../../x4/README.md) has **no RTC at all**.

## Status

**`unresolved`.** Presence and address confirmed; **part identity is not**.
