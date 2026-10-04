# Goodix GT911 — capacitive touch controller

> 5-point projected-capacitive touch controller, I²C. Widely used on small and medium embedded
> touch panels. Record created **2026-08-24**.

- **Manufacturer:** Goodix (汇顶科技)
- **Part:** GT911
- **Function:** Capacitive touch screen controller
- **Interface:** I²C, plus INT and RST lines
- **Local datasheet:** [`artifacts/gt911-datasheet-rev-1.0.pdf`](./artifacts/gt911-datasheet-rev-1.0.pdf) — Rev 1.0

## Function and capabilities

| Item | Value |
|---|---|
| Touch points | Up to **5** simultaneous |
| Interface | I²C |
| I²C addresses | **`0x5D` primary, `0x14` backup** — selected at reset by INT/RST timing |
| Extra inputs | Up to 4 capacitive "keys" outside the active area |
| Signals | SDA, SCL, INT, RST |

The dual-address behaviour is the GT911's most common source of confusion. The address is not
strapped by a pin in the usual sense — it is latched from the **state of the INT line during the
reset sequence**. Get the reset timing wrong and the device answers at the *other* address, or at
neither. If a bus scan finds nothing at `0x5D`, check `0x14` before assuming the part is dead.

## Software

| Framework | Component / driver |
|---|---|
| ESP-IDF | `esp_lcd_touch_gt911` (Espressif component registry) |
| ESP-IDF API | `esp_lcd_touch_new_i2c_gt911()`, `esp_lcd_touch_read_data()`, `esp_lcd_touch_get_coordinates()` |
| Linux | `goodix` input driver (`drivers/input/touchscreen/goodix.c`) |
| Arduino | Multiple community libraries; vendors often ship their own |

Typical ESP-IDF use:

```c
esp_lcd_touch_handle_t tp = NULL;
esp_lcd_touch_config_t cfg = {
    .x_max = /* panel width  */,
    .y_max = /* panel height */,
    .rst_gpio_num = /* board-specific */,
    .int_gpio_num = /* board-specific */,
};
esp_lcd_touch_new_i2c_gt911(io_handle, &cfg, &tp);

esp_lcd_touch_read_data(tp);
esp_lcd_touch_get_coordinates(tp, x, y, strength, &count, max_points);
```

`x_max` and `y_max` must match the **panel's** resolution, not the framebuffer's. Mismatched
values produce coordinates that are scaled or clipped rather than absent — a quiet failure that
looks like poor calibration.

## Caveats and unsafe assumptions

1. **Address depends on reset timing**, not a strap pin. See above.
2. **The controller is usually on the panel FPC**, not the mainboard. Its INT/RST GPIOs are a
   property of the *board*, and cannot be inferred from the part number or from another board
   using the same controller.
3. **Firmware varies per panel.** Vendors load panel-specific configuration into the GT911.
   Coordinate orientation, resolution and key behaviour are therefore panel-specific; do not
   assume portability of a working config between boards.
4. **Do not copy INT/RST pin numbers between boards.** This is the most common way GT911 bring-up
   goes wrong.

## Used by

### Waveshare ESP32-P4-WIFI6-Touch-LCD-3.4C and 4C

> **These boards fit a GT9271, not a GT911** — see [`../gt9271/`](../gt9271/README.md). They are
> listed here because the entire software stack, including Waveshare's published BSP, drives the
> part through the **GT911-compatible** driver and API. This record describes that driver contract.

Both variants of the [shared XC platform](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-xc-shared/README.md)
fit a GT911 on the round panel's FPC.

| Item | Value |
|---|---|
| Bus | I²C — **SDA GPIO7, SCL GPIO8** |
| Shared with | **ES8311 codec and ES7210 ADC on the same bus** |
| Clock | 100 kHz or 400 kHz — Waveshare's own sources disagree |
| Max points | 5, per Waveshare's library config |
| RST GPIO | **23** (`TP_RST`, via 0 Ohm `R62`) |
| INT GPIO | **not connected to the SoC** — terminates at test point TP2 |
| Coordinate range | 800 × 800 (3.4C) or **720 × 720** (4C) |

Because touch shares the I²C bus with both audio chips, a stalled codec presents as a touch
failure and vice versa. Scan the bus first.

**The interrupt line is not wired to the SoC.** Read from the schematic 2026-08-24: `TP_INT`
leaves the FPC, passes through a populated 0 Ohm resistor, and terminates at test point **TP2**.
Set `int_gpio_num = GPIO_NUM_NC` and **poll**. Reset *is* wired, on GPIO23.

This is a useful illustration of the second caveat above: the same GT911 part, on a board that
simply chose not to route its interrupt. See the device's
[touch guide](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/features/touch.md) and
[C11](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/gaps-and-conflicts.md#c11--touch-interrupt-is-not-wired-to-the-soc).

> Note the resolution differs between the two variants sharing this record. Use **720 × 720** on
> the 4C; using the 3.4C's 800 × 800 yields mis-scaled coordinates.

### [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md) — *added 2026-09-04*

The **only** touchscreen in the Xteink ESP32 family. On the shared I²C bus
**SDA 39 / SCL 38 @ 400 kHz**, at **0x5D** (alt 0x14), alongside a BM8563 RTC
(0x51) and a [CW2017 fuel gauge](../../cellwise/cw2017/README.md) (0x63).

| Signal | GPIO |
|---|---:|
| INT | **10** |
| RST | **4** |
| **Power enable** | **2 — ACTIVE-LOW** |

Three separate things each leave this controller **completely silent on the bus**
until fixed, and all three were hit during bring-up:

1. **The rail is gated by GPIO2 and it is active-LOW.** The OEM drives GPIO2 **LOW**
   (with GPIO1 HIGH) at boot. Driving it *high* — the naive "enable" — keeps the
   GT911 unpowered; an idle scan then shows only 0x51 and 0x63.
2. **RST = GPIO4, INT = GPIO10.** An earlier reverse-engineering pass had these
   two reversed.
3. **The reset must be long enough.** Too short a reset skips the internal config
   load and the config registers read back all-zero. The SDK uses
   **10 ms / 10 ms / 50 ms / 50 ms** with INT → INPUT.

**No host config upload.** The GT911 self-loads its internal config on the
standard reset dance, and **there is no GT911 config table anywhere in the OEM
firmware dump** (app0, app1, spiffs or nvs) — confirming the vendor relies on
self-load too.

**Point-frame layout:** `gt911CoordsAtByte0 = true` — coordinates start at **byte
0** of the `0x8150` read, not byte 1. The datasheet-standard layout puts a
track-id first; this panel does not. Getting it wrong shifts every coordinate by
one byte.

**Mounting:** the digitizer is **portrait on a landscape panel**, reporting
X: 0–480, Y: 0–800 on an 800 × 480 display → `swapXY = true`.

**Capacitive Home key:** the X4 Pro's "Home" pad is a **GT911 key bit**, status
`0x814E & 0x10`, *not* a GPIO. RE-confirmed that the OEM keys off exactly that
bit. Surfaced as `InputManager::wasHomeKeyPressed()`.

⚠ **Unresolved:** the FreeInk board header sets `flipY = true` commented *"confirmed
by corner-tap"*, while the same repository's device document says in two places
that `flipX`/`flipY` are **pending** a corner-tap test. See
[`devices/xteink/x4-pro/gaps-and-conflicts.md`](../../../devices/xteink/x4-pro/gaps-and-conflicts.md).

→ [`devices/xteink/x4-pro/features/touch.md`](../../../devices/xteink/x4-pro/features/touch.md)

## Artifacts

| File | Bytes | SHA-256 (prefix) | Provenance |
|---|---:|---|---|
| `artifacts/gt911-datasheet-rev-1.0.pdf` | 1,467,494 | `ca79a4ba` | Extracted from SensorLib 0.3.1 `datasheet/GT911 Rev.10.pdf`; originally bundled with <https://github.com/lewisxhe/SensorLib> |
| `artifacts/gt911-programming-guide-rev00-2014-08-04-crystalfontz-mirror.pdf` | 477,454 | `60c6c228` | Crystalfontz mirror, retrieved 2026-09-11 — full provenance, licence caveat and **extraction** in [*Programming Guide*](#programming-guide--retrieved-2026-09-11-and-how-it-was-found-by-accident) and [*Programming-guide extraction*](#programming-guide-extraction--register-level-facts--mined-2026-09-20) below. A byte-identical duplicate sits unmoved in the archived XTEInk scratch tree |

**Redistribution status:** `unknown`. This is a Goodix datasheet redistributed inside an
MIT-licensed library; the MIT licence covers SensorLib's own code, **not** the bundled
third-party document. Kept in the repository; terms noted above.

Reacquire:

```bash
git clone https://github.com/lewisxhe/SensorLib.git
git -C SensorLib checkout v0.3.1
# -> SensorLib/datasheet/GT911 Rev.10.pdf
```

Goodix does not publish the GT911 datasheet openly; it typically circulates via module vendors and
library bundles. That makes this copy comparatively valuable and worth preserving.

## Open questions

- Whether a later datasheet revision than Rev 1.0 exists publicly.
- Official Goodix distribution channel for the datasheet and configuration tooling.
- Confirmation on hardware that the P4 round boards' `TP_INT` really has no SoC connection.

## Related

- [ESP32-P4-WIFI6-Touch-LCD-3.4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-3.4c/README.md) · [4C](../../../devices/waveshare/esp32-p4-wifi6-touch-lcd-4c/README.md)
- [Hynitron CST816D](../../hynitron/cst816d/README.md) — a simpler single-point alternative used on the knob board
- [Components index](../../README.md)

---

## Programming Guide — retrieved 2026-09-11, and how it was found by accident

| Field | Value |
|---|---|
| Local path | [`artifacts/gt911-programming-guide-rev00-2014-08-04-crystalfontz-mirror.pdf`](artifacts/gt911-programming-guide-rev00-2014-08-04-crystalfontz-mirror.pdf) |
| **SHA-256** | `60c6c2284b482a7acdcd2747c47a9a7d25283235ccda8c688c10e2fd3216a98b` |
| **Bytes** | **477,454** |
| Pages | **31**, A4 |
| Source URL | <https://www.crystalfontz.com/controllers/UltraChip/UC8179/478/> |
| Source class | **credible mirror** — Crystalfontz, a display distributor |
| Retrieved | **2026-09-11**, HTTP 200, magic bytes `%PDF` |
| **Document title** | `GOODiX GT911 Programming Guide 2014-08-04_Rev.00` |
| Subject | *"GOODiX GT911 5-Point Capacitive Touch Controller Programming Guide"* |
| Applicability | *"firmware of version 1040 or later"* |
| Author | GOODiX, Shenzhen Huiding Technology Co., Ltd. |
| Producer / dates | Acrobat Distiller 9.0.0; created 2014-08-19, modified 2019-06-24 |
| Redistribution status | **`prohibited` as written** — the document's own first page reads *"**GOODIX CONFIDENTIAL** … Reproduction and/or distribution of this document in whole or in part is strictly prohibited without written consent of GOODIX"* |
| Disposition | `repository`, **unstaged — flagged for the user's decision**, see below |
| Known byte-identical copy | `archive/devices/xteink/shared-artifacts/research-scratch/datasheets/gt911-programming-guide-rev00-crystalfontz.pdf` — see *"A second copy…"* below |

**Text-layer validated** against the rendered page-1 heading (*"GT911 Programming
Guide (Applicable to firmware of version 1040 or later)"*) and the disclaimer
block.

### The URL is a trap, and it is why this file exists

This document was fetched while trying to obtain a **UC8179** datasheet.
`https://www.crystalfontz.com/controllers/UltraChip/UC8179/478/` returns a valid
PDF — of a **GOODiX touch controller**. The path segment `UltraChip/UC8179` is
decorative; only the trailing number selects a document, and `478` is the GT911
guide. The UC8179 document is `517`.

The file is retained here rather than discarded because **it is the right
document for this component**, filed by what it *describes* rather than by what
was being researched — and because a near-identical mis-file is exactly the
failure this repository's conventions exist to prevent.

### What it adds

Register-level detail the board profiles do not carry: the real-time command
registers, the full configuration block, the coordinate-information layout at
`0x814E`/`0x814F`/`0x8150`, command-status registers, HotKnot registers, the
power-on timing diagram, and **I²C address selection during power-on or reset** —
which is the mechanism the X4 Pro's `beginGt911()` drives with INT held at a
level across the RST pulse to choose between `0x5D` and `0x14`.

It also explains a detail a third party observed on a physical X4 Pro: the Home
pad is a **GT911 touch key**, reported in bit 4 of `0x814E` with its key byte
immediately after the last point record at `0x814F + 8·count` — and that the
Linux `goodix.c` driver reads it the same way.

### ⚠ Decision required from the user

**This document declares itself confidential and forbids redistribution without
GOODiX's written consent.** It is widely mirrored by distributors, which does not
constitute permission. It is left **unstaged**, and the options are:

1. keep it unstaged in the working tree (current state);
2. move it to the local archive with a placeholder carrying this hash, size and
   the reacquisition URL;
3. delete the bytes and keep only this metadata block as the acquisition record.

**Used by:** [Xteink X4 Pro](../../../devices/xteink/x4-pro/README.md) — the only
Xteink device with a touchscreen.

---

## A second copy exists in the archive, and it is the same bytes — *checked 2026-09-20*

The XTEInk research-scratch tree archived on 2026-09-20 contains
`datasheets/gt911-programming-guide-rev00-crystalfontz.pdf`, which **no repository record
cited**. It is the original fetch that produced the file above; the copy here was renamed to
carry its revision, date and custodian.

```
60c6c2284b482a7acdcd2747c47a9a7d25283235ccda8c688c10e2fd3216a98b  archive/devices/xteink/shared-artifacts/research-scratch/datasheets/gt911-programming-guide-rev00-crystalfontz.pdf
60c6c2284b482a7acdcd2747c47a9a7d25283235ccda8c688c10e2fd3216a98b  components/goodix/gt911/artifacts/gt911-programming-guide-rev00-2014-08-04-crystalfontz-mirror.pdf
```

**Identical SHA-256, identical 477,454 bytes — a duplicate, not a second custodian's revision.**
It was **not moved** into `artifacts/`: it is already covered by the directory-level placeholder
at [`devices/xteink/shared-artifacts/README.md`](../../../devices/xteink/shared-artifacts/README.md),
whose locale-pinned tree digest `43841e95…` would be invalidated by removing a file from that
tree.

The document itself, however, **had only been described, not mined**. The section below closes
that gap.

---

## Programming-guide extraction — register-level facts — *mined 2026-09-20*

Source throughout: `artifacts/gt911-programming-guide-rev00-2014-08-04-crystalfontz-mirror.pdf`,
*GT911 Programming Guide, Rev.00, 2014-08-04*, 31 pp. Page numbers below are the document's own
printed page numbers. **Text layer re-validated** against the rendered p.1 heading and the
p.3 interface prose before any value here was transcribed.

Evidence label for everything in this section: **`inferred` from a primary vendor document** —
none of it has been exercised on hardware by this repository. Where it contradicts the
hardware-confirmed X4 Pro findings above, **the hardware finding wins**; those cases are called
out explicitly.

### The numbers the bring-up actually depends on

| Fact | Value | Page |
|---|---|---|
| Pins | VDD, GND, SCL, SDA, INT, RESET — **6** | 3 |
| **RESET low pulse** | *"recommended that RESET pin outputs low for longer than **100 μs**"* | 3 |
| Max I²C rate | **400 kbit/s** | 3 |
| **Pull-up warning threshold** | **> 200 kbit/s** — above this, *"pay special attention to the resistance of the external pull-up resistor … to ensure the edges of SCL and SDA are steep enough"* | 3 |
| INT pin state when host reads | **floating, no internal pull-up or pull-down** | 3 |
| **Wait after INT → input floating, before sending config** | **50 ms** | 25 |
| Normal-mode refresh cycle | 5–20 ms, configurable in 1 ms steps | 27 |
| Green (low-power) mode scan cycle | ~40 ms | 27 |
| Green-mode entry timeout | 0–15 s, configurable in 1 s steps | 27 |

The **200 kbit/s pull-up threshold is the X4 Pro's operating region** — that board runs this bus
at 400 kHz. The guide does not give a resistance value, only the warning.

### I²C addressing — the dual-address mechanism, as the vendor states it

| 7-bit | 8-bit write | 8-bit read |
|---|---|---|
| **0x5D** | 0xBA | 0xBB |
| **0x14** | 0x28 | 0x29 |

*(p.3)*

The selection rule, in the guide's own words (p.24): *"Host needs to select the I2C slave device
address during power-on initialization or Reset process via Reset pin. Host can select the I2C
address by controlling Reset and INT timing sequence."* And on p.23: **the level the host drives
on INT after the point labelled `T2` is what chooses the address — high selects 0x28/0x29
(= 0x14), low selects 0xBA/0xBB (= 0x5D).**

> ⚠ **Gap — the timing values are not recoverable from this PDF.** The power-on timing diagram
> (p.23) and both address-selection diagrams (p.24) are rendered as several hundred 1-bit CCITT
> stencil glyph images, not text. `T1`…`Tn` appear nowhere in the text layer — the only reference
> is the prose phrase *"after INT T2"*. **The durations therefore cannot be transcribed from this
> document and are not reproduced here.** Reading them requires rendering pp. 23–24 as images.
> This is why the X4 Pro's empirically derived **10 ms / 10 ms / 50 ms / 50 ms** sequence
> (see *Used by* above) remains this repository's only concrete GT911 reset timing, and it is a
> *board* observation, not a vendor specification.

### Configuration table and its checksum rule

| Item | Value | Page |
|---|---|---|
| Configuration register block | **0x8047 – 0x80FE** | 10, 25 |
| First register | `Config_Version` at **0x8047** | 5 |
| **`Config_Chksum`** | **0x80FF** — *"checksum value of the bytes from 0x8047 to 0x80FE"* | 10 |
| **`Config_Fresh`** | **0x8100** — *"Configuration updated flag (the flag is written by the host)"* | 10 |
| Bytes covered by the checksum | **184** (0x80FE − 0x8047 + 1) | derived |

The commit rule, verbatim (p.25):

> *"When modifying any register in the configuration area (0x8047－0x80FE) … it is required to
> update `Config_Chksum` (0x80FF) and eventually set `Config_Fresh` (0x8100) to 1. **Otherwise,
> the modification is invalid**; when modifying any registers outside configuration area, it is
> unnecessary to modify `Config_Chksum` and `Config_Fresh`."*

**This is the trap:** a config write that omits either the checksum or the `Config_Fresh=1`
commit is silently discarded. The controller does not error — it simply keeps the old config,
which presents as "my settings don't take effect."

> ⚠ **The checksum *algorithm* is not stated in this document.** The guide gives only the
> **range** and the register. It never says how the byte is computed. The widely used rule —
> two's complement, such that the 8-bit sum of 0x8047…0x80FF is zero — is **not** sourced here
> and must be taken from the Linux `goodix.c` driver or Goodix's config tool instead.
> The only checksum arithmetic this document does spell out is for an unrelated block: the
> HotKnot `CheckSum` (p.21), described as *"the complement of the sum"*, starting from 0xAC90.
> That is suggestive of the same convention but **is not a statement about `Config_Chksum`**,
> and is not treated here as one.

`Config_Version` (0x8047) has its own trap (p.5): configuration is accepted *"only when the
version number of the new release is later than that of the previous one, or equal to that of
the previous one but there are changes in contents"*. Writing `0x00` resets the version to `'A'`.
A host that re-sends a config with a stale version number will have it ignored.

Also relevant to the X4 Pro, which uses no host config upload at all: `Vendor_id` at **0x814A**
is set by board strapping, *"codetermined by pins `sensor_opt1` and `sensor_opt2`"*, yielding
**six** module IDs 0–5 from the combinations GND / VDDIO / NC against GND / 300 kΩ (p.15).

### Coordinate report format

Identity and status block (p.14):

| Address | Contents |
|---|---|
| 0x8140–0x8143 | Product ID, 4 ASCII bytes |
| 0x8144–0x8145 | Firmware version, low then high byte |
| 0x8146–0x8149 | X then Y coordinate resolution, low/high each |
| **0x814A** | `Vendor_id` |
| **0x814E** | status byte — see below |

`0x814E` bit assignments (p.15), the only **R/W** register in the block:

| Bit | Name | Meaning |
|---:|---|---|
| **7** | **buffer status** | 1 = coordinates/key ready; 0 = not ready, data invalid |
| 6 | large detect | large-area touch present |
| 5 | Proximity Valid | HotKnot proximity |
| **4** | **HaveKey** | 1 = touch key down, 0 = released |
| **3–0** | **number of touch points** | 0–5 |

Bit 4 is the mask the X4 Pro's Home pad uses (`0x814E & 0x10`) — **confirmed against the vendor
document**, p.15, matching the hardware finding recorded above.

**Point records are 8 bytes and begin at 0x814F, track-id first:**

```
0x814F + 8·(n−1)  →  track_id, x_lo, x_hi, y_lo, y_hi, size_lo, size_hi, reserved
```

The guide's own table is self-consistent with this: it labels 0x814F *"track id"*, 0x8150/0x8151
*"point 1 x low/high"*, 0x8156 *"Reserved"*, then **0x8157 *"track id"*** immediately before
0x8158 *"point 2 x low"* (pp. 14–15). So the byte the table calls "point 1's track id" at 0x8157
is in fact the **head of record 2**.

This is precisely what the X4 Pro's `gt911CoordsAtByte0 = true` encodes: a read that starts at
**0x8150** lands on `x_lo` directly, skipping the leading track-id. The vendor document and the
board finding agree. Five records occupy 0x814F–0x8176.

### ⚠ Conflict — where the touch-key byte actually is

The *Used by* section above states the key byte sits *"immediately after the last point record at
`0x814F + 8·count`"*. **The programming guide's two worked examples do not fit that formula.**

Guide, p.15, on `KeyValue`: *"The address of KeyValue is not fixed. Instead, it stays behind
valid coordinates. For example, **0x817F** is the address of the key when there are **5**
coordinates on TP. However, if there are **4** coordinates on TP, the address of the key will be
**0x8177**."*

| `count` | Record-end + 1 (`0x814F + 8·count`) | **Guide's stated KeyValue** | Δ |
|---:|---|---|---:|
| 4 | 0x816F | **0x8177** | +8 |
| 5 | 0x8177 | **0x817F** | +8 |

Both examples are a **full 8-byte record past** the end of the valid coordinates, consistently.
The formula that fits both is:

```
KeyValue = 0x8157 + 8·count      (equivalently 0x814F + 8·(count+1))
```

Two readings are possible and this document does not settle which:

1. The record's existing formula is wrong by one record, and `KeyValue` genuinely sits one
   record beyond the valid coordinates.
2. The guide's examples are off by 8 — a plausible authoring slip, given that the same document
   is already ambiguous about whether the track-id leads or trails a record.

**Left unresolved.** What would settle it: on an X4 Pro, press the Home pad with **no** finger on
the panel (`count = 0`) and read both `0x8157` and `0x814F`; the formula above predicts the key
byte at **0x8157**. Until that is done, do not treat either address as authoritative, and note
that the X4 Pro firmware's working implementation keys off `0x814E` bit 4 for *presence* — which
is unaffected by this conflict.

### The polling contract, and the way it hangs

From §5, p.25–26, and §3.3, p.15 — **the host must write `0x814E` back to 0 after every read**:

1. Read `0x814E`. If bit 7 (buffer status) is **0**, the data is not valid — *"it will read again
   1 ms later"*.
2. If bit 7 is **1**, read the coordinate and key bytes.
3. *"After reading coordinates, host should configure this flag (or the entire byte) to **0** via
   I2C."*

The failure mode is explicit and worth quoting, because it looks like a dead controller
(p.26, describing the interrupt case):

> *"After output rising-edge in step 2, if the host fails to finish reading coordinates within
> one cycle, GT911 will output one INT pulse again **instead of update coordinates** even if it
> detects that the coordinate is updated. If the host still fails to read coordinate, GT911 will
> keep outputting INT pulse."*

**A host that reads coordinates but never clears the buffer-status bit gets interrupts forever
and the same stale coordinates forever.** The INT line stays busy, so the symptom reads as
"touch is firing constantly but the finger never moves" rather than as a silent bus.

INT idles **low** in standby and rises on coordinate update (for the rising-edge configuration);
the edge polarity itself is a config field — `Module_Switch1` at **0x804D**, bits 1–0:
`00` rising, `01` falling, `02` low level, `03` high level (p.5). The same register carries
`Driver_Resersal (Y2Y)` at bit 7 and `Sensor_Resersal (X2X)` at bit 6 — *"configured as 1
indicates Y axis reversal"* / *"X axis reversal"* (p.10). **These are the controller-side
equivalents of the X4 Pro's host-side `swapXY` / `flipY`**, and are relevant to the unresolved
`flipY` conflict noted in *Used by* above: on a panel that self-loads its config, the reversal
may already be applied in the controller, making an additional host-side flip a double negation.

### Real-time command register

`0x8040` is write-only (p.4). Values: `0` read coordinate status · `1`/`2` read diff or raw data ·
`3` reference-capacitance update (internal test) · `4` reference-capacitance calibration
(internal test) · `5` screen off · `6` enter charge mode · `7` exit charge mode · `8` gesture
mode · `0x20`–`0x2A` HotKnot modes · `0xAA` ESD-protection handshake.

Two anti-ESD mechanisms, both easy to miss:

- **`0x8046 Command_Check`** — *"For commands greater than 0x07, it is required to write the
  command to 0x8046 **before** writing to 0x8040."* Gesture mode (`8`) and every HotKnot command
  are above 0x07, so a single write to 0x8040 is **not sufficient** for them.
- **`0x8041 ESD_Check`** — reset to 0 on initialization; the driver writes `0xAA` to `0x8040` and
  re-reads `0x8040` periodically to confirm the controller is alive.

### What this document does *not* contain

- Any electrical/absolute-maximum data — it is a programming guide, not a datasheet. Use
  `artifacts/gt911-datasheet-rev-1.0.pdf` for that.
- The `Config_Chksum` algorithm (see above).
- Numeric reset/address-selection timings (images only, see above).
- Per-panel configuration values — those are panel-specific by design, as caveat 3 above states.
