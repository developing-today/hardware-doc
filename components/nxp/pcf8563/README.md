# NXP PCF8563

- **Category:** real-time clock/calendar, I²C-bus, with alarm, timer and a programmable
  clock output. Low-voltage, extremely low standby current.
- **Manufacturer:** NXP Semiconductors (originally Philips).
- **Retrieved:** 2026-09-07
- **Sibling here:** [`pcf85063a`](../pcf85063a/README.md) — the newer, smaller NXP RTC used on
  other boards in this repository.

> **This record was created 2026-09-07 to fill a gap.** The directory already held
> [`artifacts/pcf8563-datasheet-rev-11.pdf`](artifacts/pcf8563-datasheet-rev-11.pdf) (495 457 B,
> added 2026-08-23 by an earlier pass) with **no `README.md` beside it**. The datasheet was
> **not read** by this pass; nothing below is transcribed from it. This is a stub whose purpose
> is to make the artifact discoverable and to record which device uses the part.

## 1. Identity

| Property | Value |
|---|---|
| Part | **PCF8563** |
| Datasheet | Rev. 11, retained locally as `artifacts/pcf8563-datasheet-rev-11.pdf` — acquired 2026-08-23 by an earlier pass; provenance URL not recorded at the time |
| Interface | I²C |
| Address | **not verified here.** The PCF8563 is conventionally at `0x51`; that is stated as an expectation, not a finding |

**Provenance gap:** the artifact has no acquisition record. NXP publishes PCF8563 openly
(`nxp.com`, document `PCF8563`), so re-acquisition is `automatic`; the exact URL used
originally is unknown.

## 2. Used By

### LilyGO T-Display-S3 AMOLED 1.43″ / 1.75″
→ [`devices/lilygo/t-display-s3-amoled-1-43-1-75`](../../../devices/lilygo/t-display-s3-amoled-1-43-1-75/README.md)

The RTC on LilyGO's round AMOLED boards, and the reason those are the only boards in the
[T-Display-S3 family](../../../devices/lilygo/t-display-s3-shared/README.md) that can wake from
deep sleep at a **wall-clock time** rather than after an interval.

`PCF8563_INT` is **GPIO9** in `components/private_library/pin_config.h` @
`87aabe888eea6a7c0f95ce1991ca75fa98c2a172` — **the same pin that file assigns to `TP_INT`**.
Either the two open-drain interrupts are wire-ORed or one define is wrong; **no schematic is
published for these boards**, so it is unresolved. If you use both the touch controller and an
RTC alarm, your ISR must distinguish them by polling both devices.

I²C bus: SDA **GPIO7** / SCL **GPIO6**, shared with the
[FT3168 touch controller](../../focaltech/ft3168/README.md) and the
[SY6970 PMIC](../../silergy/sy6970/README.md).

Vendor examples @ `87aabe8`: `PCF8563`, `PCF8563_Scheduled_INT`, `PCF8563_Timer_INT`,
`Deep_Sleep_PCF8563_Scheduled_Wake_Up`, `Deep_Sleep_PCF8563_Timer_Wake_Up`. LilyGO also
mirrors two PCF8563 documents in that repository (`PCF8563.pdf`, 498 308 B, and a Chinese
`C5795601_实时时钟RTC_PCF8563_规格书_WJ490310.pdf`, 3 131 978 B) — **neither retrieved**, since
this record already holds an NXP copy. Whether the LilyGO mirror is the same revision as the
retained Rev. 11 is **unknown**.

## 3. Gaps

- Datasheet not read; no register, address or electrical value recorded.
- Original acquisition URL unknown.
- The GPIO9 double-assignment on the LilyGO boards is unresolved.
- The LilyGO mirror was not compared against the retained copy.
