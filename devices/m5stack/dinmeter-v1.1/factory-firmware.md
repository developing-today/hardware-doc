# DinMeter v1.1 — factory firmware

**The factory firmware, its source, its licence, its panel configuration and the backup/restore
procedure are the same as the DinMeter v1.0's.**
→ **[`../dinmeter/factory-firmware.md`](../dinmeter/factory-firmware.md)**

---

## What is v1.1-specific

| Item | Status |
|---|---|
| Source repository | **`m5stack/M5DinMeter-UserDemo`, unchanged.** Last push 2024-03-04, release `V0.1` — i.e. **22 months before the v1.1 launched**. No v1.1 branch, tag, commit or fork exists |
| EasyLoader entry | Both product pages list the same "DinMeter User Demo Easyloader" | 
| Prebuilt binary | **Still no stable download URL.** M5Burner only |
| Binary hash / build date / partition table | **unknown** for both revisions |
| Does the v1.0 image run on v1.1? | **Yes** — same target, same pin map, same board enum. The RGB LED will not light (the firmware does not raise GPIO38), but the factory demo's LED behaviour is not documented, so it may never have driven it |

**The most informative fact here is the date.** M5Stack shipped DinMeter v1.1 on 2026-01-30 using
factory-firmware source last touched on 2024-03-04. That is a strong, independent signal that the
carrier is unchanged: if the board had been revised, the evaluation firmware would have needed
attention.

## Backing up before you overwrite

Same procedure, same warning — there is no vendor-published binary with a stable URL, so read the
flash out first. All `not-tested`:

```bash
# Download mode: hold G0 on the Stamp-S3A while applying power, release after.
esptool.py --chip esp32s3 -p /dev/ttyACM0 -b 460800 read_flash 0 0x800000 dinmeter-v11-factory-backup.bin
sha256sum dinmeter-v11-factory-backup.bin
```

**If you do this, please record the hash and the flash layout.** No dump of either revision's
factory image exists in this record, and a v1.1 dump would additionally settle whether the
shipped image differs from the v1.0's at all.

→ Full detail, licence analysis and the LovyanGFX panel configuration:
[`../dinmeter/factory-firmware.md`](../dinmeter/factory-firmware.md)
