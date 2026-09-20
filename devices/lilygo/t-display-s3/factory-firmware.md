# T-Display-S3 — factory firmware

> Six merged images retained. All decoded locally on **2026-09-07**
> (`executed-success`, host-side analysis of the binaries; **not** flashed to hardware).
> Stored once in the [shared platform record](../t-display-s3-shared/README.md) because they
> cover the Touch variant too.

## 1. The images

Source: `Xinyuan-LilyGO/T-Display-S3` → `firmware/` @ **`ec889e789b3cf093412689a143f7f37b42b56af7`**,
retrieved 2026-09-07 from `raw.githubusercontent.com`. Repository licence **MIT**; the binaries
carry no separate licence statement.

| File | Bytes | SHA-256 | Flash offset | Bootloader header | App-descriptor ESP-IDF | Core build stamp |
|---|---|---|---|---|---|---|
| `t-display-s3-touch-20230417_0x0.bin` | 1 601 328 | `f288081645eecf7bf6a17fd7b5bc2e724121d00cdc2099b5a5ea7db5107eb9fa` | `0x0` | DIO, **8 MB**, 80 MHz | `v4.4.4 e8bdaf9198` | Feb 8 2023 18:07:54 |
| `t-display-s3-no-touch-20231013_0x0.bin` | 1 601 328 | **`f288081645eecf7b…` — identical** | `0x0` | DIO, **8 MB**, 80 MHz | `v4.4.4 e8bdaf9198` | Feb 8 2023 18:07:54 |
| `t-display-s3-lvgl-demo-20250109_0x0.bin` | 675 920 | `4af91e520a3f5037d9b0420aa620f8736e4e6469601098fea6eb4985323d847f` | `0x0` | DIO, **16 MB**, 80 MHz | `v4.4.6 3572900934` | Oct 4 2023 16:40:08 |
| `t-display-s3-tft-espi-20231113_0x0.bin` | 501 520 | `45385b2a90070a7616b7fceca553d60ca984e33115f4b9586a5ebb6ddb8213f1` | `0x0` | DIO, 16 MB, 80 MHz | `v4.4.5 ac5d805d0e` | Jun 12 2023 16:32:29 |
| `t-display-s3-screen-detect-20230315_0x0.bin` | 489 616 | `2f0cf68a3ac19cec982735d7ccbcb93e522e65c9d8736e440efbf4001f9707fd` | `0x0` | DIO, 16 MB, 80 MHz | `v4.4.4 e8bdaf9198` | Apr 20 2023 00:44:44 |
| `t-display-s3-midi-v1.0.1-20231013_0x0.bin` | 971 824 | `f6883c8ba9be6b1c0b9840943a79fb6eee7d4e5af506ea42b01a95a1c7a9134a` | `0x0` | DIO, 16 MB, 80 MHz | `v4.4.4 e8bdaf9198` | Apr 20 2023 00:44:44 |

*(`t-display-s3-midi-v1.0.0-20231013_0x0.bin`, 902 784 B, exists upstream and was not
retained; it is superseded by v1.0.1 and recorded in
[`acquisition/manifest.json`](acquisition/manifest.json) as `reference-only`.)*

All six are **ESP32-S3** images (`magic 0xE9`, chip id 9). All are **merged** — bootloader at
`0x0`, partition table at `0x8000`, app at `0x10000` — so one write restores a board.

**The `project_name` in every app descriptor is `arduino-lib-builder`, not a LilyGO project
name.** That is the Arduino core's own stamp, which is why the "build date" column dates the
*core*, not the sketch. It is still useful — it is how [`development.md`](development.md#arduino-core-versions)
establishes that LilyGO never rebuilt past core 2.0.14.

## 2. Finding G1 — "touch" and "no-touch" are the same file

`t-display-s3-touch-20230417_0x0.bin` and `t-display-s3-no-touch-20231013_0x0.bin` have
**identical SHA-256, identical size, and identical app descriptors including build time**.
They are one binary published twice under two names and two dates.

- **Measured** 2026-09-07: `f288081645eecf7bf6a17fd7b5bc2e724121d00cdc2099b5a5ea7db5107eb9fa`,
  1 601 328 B, both.
- **Independently noticed by a user** in
  [issue #212 "Firmware_no_Touch is the same as Touch ?"](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/212)
  (2024-01-02). The thread never resolves it — it diverts into a separate confusion between the
  "ESP-Touch" Wi-Fi provisioning app and LCD touch, which is itself a naming trap worth
  knowing about.

**Practical consequence:** flashing the "no-touch" image to a non-touch board gives you the
touch factory demo, whose UI expects a touchscreen. Combined with the ESP-Touch confusion, this
is a reliable way to conclude your board is broken when it is not.

## 3. Finding G2 — the two big images carry an 8 MB partition table on a 16 MB board

`touch`/`no-touch` decode as:

```
bootloader header: flash size 8MB
nvs       type=1 subtype=0x02 off=0x009000 size=0x005000   20K
otadata   type=1 subtype=0x00 off=0x00e000 size=0x002000    8K
app0      type=0 subtype=0x10 off=0x010000 size=0x330000  3264K
app1      type=0 subtype=0x11 off=0x340000 size=0x330000  3264K
spiffs    type=1 subtype=0x82 off=0x670000 size=0x180000  1536K
coredump  type=1 subtype=0x03 off=0x7f0000 size=0x010000    64K      ← ends at 8 MB
```

while the other four decode as the `default_16MB` layout:

```
app0      off=0x010000 size=0x640000  6400K
app1      off=0x650000 size=0x640000  6400K
spiffs    off=0xc90000 size=0x360000  3456K
coredump  off=0xff0000 size=0x010000    64K      ← ends at 16 MB
```

The board has **16 MB**. Flashing the touch/no-touch image therefore leaves a partition table
that addresses only the lower half, and a bootloader header claiming 8 MB. It boots and runs —
the ESP32-S3 bootloader tolerates an under-declared flash size — but the upper 8 MB is
unaddressed until you flash something with the correct table. This is a plausible mechanism
behind several "16 MB flash setting not working" reports
([#8](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/8),
[#41](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/41)); **that causal link is
inferred, not demonstrated.**

Also note `flash mode = DIO` in every bootloader header, while LilyGO's Arduino instructions
and PlatformIO board file both specify **QIO**. The bootloader header is authoritative for how
the *bootloader* reads flash; the app can and does switch. Not a defect, but it means you
cannot read the recommended flash mode off these images.

## 4. Restoring a board

`reported-working` (LilyGO's documented procedure), `not-tested` here.

```bash
# 1. Manual download mode: hold BOOT, tap RST, release RST, release BOOT.
# 2. Erase — recommended when switching between the 8 MB and 16 MB layouts,
#    otherwise a stale partition table can survive.
esptool.py --chip esp32s3 --port /dev/ttyACM0 erase_flash

# 3. Write the merged image at 0x0.
esptool.py --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
    write_flash -z 0x0 t-display-s3-lvgl-demo-20250109_0x0.bin
```

LilyGO also documents two GUI routes in `firmware/README.MD` @ `ec889e7`: Espressif's
**Flash Download Tool** (Windows) and a **web flasher** (`LILYGO-Spark`, WebSerial-based,
Chrome/Edge only). Both write the same merged image to `0x0`.

**Which image to use for a first diagnosis:** `t-display-s3-screen-detect-20230315_0x0.bin`
(489 KB) exists specifically to prove the panel works. It is the smallest and the fastest
answer to "is my board dead?".

## 5. What is not established

- **No image was flashed to hardware by this pass.** Everything above is static analysis.
- **No official hash list exists** to compare against; LilyGO publishes no checksums. The
  hashes here are of the bytes as served by `raw.githubusercontent.com` at the pinned commit,
  which is the strongest available provenance.
- The **`t-display-s3-midi-v1.0.0`** image was not retained, so the v1.0.0→v1.0.1 delta is
  uncharacterised.
- **No factory image contains a LilyGO project name or version string** in its app descriptor,
  so the file name is the only version identifier. That is why the byte-identical pair in §2
  went unnoticed for years.

## Method

Decoding recipe and script: [`commands.md`](commands.md#decoding-an-esp32-app-descriptor).
The repository's [`tools/esp_image_info.py`](../../../tools/esp_image_info.py) reads the
bootloader header directly but reports *"no app descriptor"* on merged images because it looks
at offset `0x20`, not `0x10020`; the extra step is documented in `commands.md`.
