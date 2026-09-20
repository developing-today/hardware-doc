# Selected examples — Xteink X4 Classic

**None of these was built or run by this repository.** Selection is by what each
one *teaches*, from reading the source. Date **2026-09-11**.

## 1. Start here — `Free-Ink/freeink-sdk`, `[env:x4c]`

Commit [`9f4d3f9`](https://github.com/Free-Ink/freeink-sdk/tree/9f4d3f9ca675e64cc9d616081f39a33cdefce57e) · MIT

```ini
[env:x4c]
build_flags = -DFREEINK_DEVICE_X4CLASSIC=1 -DUSE_BLOCK_DEVICE_INTERFACE=1
```

The board profile is the origin of every other entry, and
[`docs/xteink-x4c-support.md`](https://github.com/Free-Ink/freeink-sdk/blob/9f4d3f9ca675e64cc9d616081f39a33cdefce57e/docs/xteink-x4c-support.md)
is the closest thing to a datasheet this device has.

**Read `XteinkDetect.cpp` before you write a line of display code.** The X4C is
the one board in the family whose panel bus has no MISO, so the runtime probe
every sibling uses cannot run and the driver is chosen from NVS
`hw_calib/screenType` instead. That is the whole risk surface of this device in
one function.

**Pin your commit.** Between `2400379` (2026-09-01) and `39606d5a` (2026-09-09)
the recommended `displaySpiHz` halved, 20 MHz → 10 MHz.

## 2. Best alternative approach — `clackups/draftling`

Commit [`92ba7e5`](https://github.com/clackups/draftling/tree/92ba7e514f66bbe42a7fea6d38eff45eed82617b) · MIT

Read [`firmware/main/boards/xteink_x4_classic.h`](https://github.com/clackups/draftling/blob/92ba7e514f66bbe42a7fea6d38eff45eed82617b/firmware/main/boards/xteink_x4_classic.h)
**side by side with** the FreeInk profile. It is a second author's reading of the
same reverse engineering, on ESP-IDF rather than Arduino, for an editor rather
than a reader — so where the two agree, the agreement is worth something, and
where the header adds commentary it is usually the commentary you wanted:

- why GPIO1 must be raised first and what happens if it is not;
- that GPIO0 is a boot strap **and** the Left key;
- that GPIO4 exists on the OEM board and neither project uses it;
- why the partition table keeps `otadata` — so the stock and CrossPoint OTA
  updaters can reinstall, which matters enormously on a device with **no USB
  socket**.

**Negative-example value:** its own `HARDWARE.md` states *"This board has been
added without on-hardware testing."* Its X4 **Pro** chapter, which *was* tested,
documents a real asynchronous-DMA bug and a touch-orientation correction. That
contrast is the best available illustration of how much a blind port can still
get wrong.

## 3. The integrated application — CrossPoint Reader, `x4c`

[`crosspoint-reader/crosspoint-reader`](https://github.com/crosspoint-reader/crosspoint-reader)

What owners actually run. Reported working on X4C hardware by u/Diirge on
2026-09-10. **This catalogue could not pin a commit for it**, which is a gap, not
an omission — recorded as `immutable_url: null` in `catalog.json`.

## 4. The one to build if you have no hardware — `kycube/x4pro-emu`

Commit [`bf4b86a`](https://github.com/kycube/x4pro-emu/tree/bf4b86ae0471012d4d07c0bb3042f3f561c9c302) · **no licence stated**

It models the **X4 Pro**, not the X4 Classic. But it boots real stock firmware
and real CrossPoint under QEMU, with models for the panel, the GT911, the LEDC
fade, deep sleep and the USB-Serial/JTAG console — and the X4 Classic is the same
SoC, the same flash map and the same panel stack with **fewer** peripherals.

**Adapting it to the X4 Classic is the cheapest untried way to develop for this
board**, and nobody has done it. Note the licence: none is stated, so redistribution
status is `unknown` and it is referenced here, not vendored.

## What no example covers

| Gap | Why it matters |
|---|---|
| **QMI8658 / Shake-to-Flip** | The vendor's own headline feature. No example anywhere exercises the IMU on this board |
| **NVS `screenType` recovery** | The board's worst failure mode — a full-chip erase makes the firmware unable to identify its own display — has no worked example and no documented repair |
| **USB-MSC** | Enabled in the SDK, no socket on the enclosure, never demonstrated |
| **Wi-Fi + panel refresh concurrently** | No PMIC, one cell, no measured brown-out margin |
