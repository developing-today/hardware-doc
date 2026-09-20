# Clones, siblings and variants — identification and survival guide

How to tell what board you are actually holding, what is likely to differ from the documentation you
are reading, and how to trace an unlabelled board back to a design that *is* documented.

- **Compiled:** 2026-08-24.
- **Evidence labels:** **[DOC]** vendor document · **[SCH]** schematic · **[SRC]** source code ·
  **[COM]** community report · **[WEB]** vendor web page · **[INF]** inference.

> **The core problem.** In the Shenzhen hardware ecosystem, a "product" is often a *reference design*
> that several vendors build, each with their own PCB revision, their own BOM substitutions and their
> own firmware. **There is frequently no original and no clone — there are siblings.** Treating one
> vendor's documentation as authoritative for another's board is the single most common way to waste
> a day.

---

## 1. Vocabulary — worth being precise

| Term | Meaning |
|---|---|
| **Clone** | A deliberate copy of an identifiable original, usually cheaper, often with substitutions |
| **Sibling** | Two vendors building the same reference design or buying from the same ODM. **Neither is the original** |
| **Variant** | Same vendor, same product name, different BOM or PCB revision — often undocumented |
| **Re-mark** | A different, usually inferior, die marked as the expected part. A counterfeiting problem, not a design one |
| **ODM/white-label** | One factory's design sold under many brands |

**The worked example in §5 is a *sibling* relationship**, not a clone-of-original, and the
community source that identified it says so explicitly. Getting this distinction right changes what
you conclude when the two boards differ.

---

## 2. Spotting a clone or variant from a product listing

Ordered by how reliable each signal is.

### High-confidence signals

1. **The listing photo shows a different PCB silkscreen than the vendor's own photos.** Compare
   component *positions*, not just the outline. Look at the corners of the board and at test points.
2. **The photo is reused across multiple sellers with different brand names.** Reverse-image search.
   Many sellers, one photo, several product names = an ODM design.
3. **The claimed flash/PSRAM does not match the module marking visible in the photo.** An
   `ESP32-S3-WROOM-1-N16R8` marking is legible in a decent photo, and it *states* 16 MB flash +
   8 MB PSRAM. See
   [ecosystem-and-product-lines.md §7.2](../espressif/ecosystem-and-product-lines.md#72-s3-and-later--r-and-n).
4. **The listing names a display controller that contradicts the panel size or interface.** A round
   360×360 panel on a controller that only does 240×320 is a copy-paste error, and copy-paste errors
   travel with cloned listings.

### Medium-confidence signals

5. **Missing shielding can, missing regulator, or an obviously smaller component count** versus the
   reference photos. Cost reduction is visible.
6. **The listing links documentation belonging to a *different* vendor.** This is common and is
   actually a gift — it tells you which design to trace back to (§4).
7. **"Compatible with X" rather than "is X".**
8. **Price substantially below the vendor's own.**

### Low-confidence signals (do not conclude from these alone)

9. Different colour solder mask — vendors change this themselves.
10. Different packaging or box art.
11. Slightly different product name — vendors rename constantly.

> **The honest caveat:** photographs establish *hypotheses*, not facts. **Nothing in this section
> substitutes for enumerating the buses on the physical board** (§3). **[INF]**

---

## 3. What actually differs — and how to detect each

This is the list to work through when a board "should" work and doesn't.

| Difference | How it bites | How to detect |
|---|---|---|
| **Swapped GPIO assignments** | Display blank, touch dead, SD card absent | The single most common difference. Compare against the [pinout record](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md); bisect by toggling pins |
| **Substituted display controller** | Garbage or blank display; init sequence hangs | Read the controller ID register. Our own board's documentation set names **two different controllers** for one panel — see [ST77916](../../components/sitronix/st77916/README.md) vs the [SH8601 conflict record](../../components/generic/sh8601-compatibility-driver/README.md) **[DOC]** |
| **Substituted touch controller** | Touch dead; I²C scan finds nothing at the expected address | **Scan the whole I²C bus.** `CST816x` is at `0x15`; [Goodix `GT911`](../../vendors/goodix/README.md) is at `0x5D` **or** `0x14` depending on reset timing; [Chipsemi `CHSC5816`](../../vendors/chipsemi/README.md) differs again. **None are register-compatible** **[DOC]** |
| **Different flash size** | Boots then crashes; partition table overruns | Read the JEDEC ID (`0x9F`) and compare — see [Winbond §4](../../vendors/winbond/README.md#4-part-numbering--this-one-is-worth-learning-properly). **Remember `W25Q128` = 128 **Mbit** = 16 MB** |
| **Different PSRAM size or absent PSRAM** | LVGL allocation failures; no framebuffer | `esp_psram_get_size()`; check the module suffix |
| **Omitted regulator / power path** | Works on USB, dies on battery | Compare against the [power tree](../../components/texas-instruments/tlv62569dbvt/README.md) and [charger record](../../components/generic/charger-power-path/README.md) |
| **Omitted discretes** | Subtle: level shifting or protection gone | The [MOSFET](../../components/alpha-and-omega-semiconductor/ao3400a/README.md) that isn't there |
| **Different / absent second MCU** | Bluetooth Classic simply absent | Our board's [U4WDH](../../components/espressif/esp32-u4wdh/README.md) exists *only* for Classic BT. A clone that drops it drops the feature — see [dual-mcu-architecture.md](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md) |
| **Re-marked or counterfeit parts** | Runs hot, out of spec, intermittent | Hardest class. See [AOS §7](../../vendors/alpha-and-omega-semiconductor/README.md#7-gotchas) and [TI §6](../../vendors/texas-instruments/README.md#6-distribution) |
| **Near-identical part number, different registers** | Driver reads garbage | The `HMC5883L` / `QMC5883L` case — see [QST §3](../../vendors/qst/README.md#3-market-position--and-the-hmc5883l-story) |

### The five-minute triage

```
1. esptool chip_id / flash_id      -> which SoC, which flash, how big
2. I2C scan across the whole range -> which peripherals, at which addresses
3. Read each peripheral's ID reg   -> which die, not which silkscreen
4. esp_psram_get_size()            -> PSRAM present and how much
5. Only then open the schematic
```

**Read chip IDs, not silkscreens, not listings, not schematics.** Every layer above the silicon can
be, and frequently is, wrong. **[INF]**

---

## 4. Tracing a board back to a documented original

1. **Read the module marking.** `ESP32-S3-WROOM-1-N16R8` narrows things enormously.
2. **Search the PCB silkscreen text verbatim.** Board designators, revision codes and the ODM's
   internal project name are often printed and are highly searchable. **`JC3636K518` in §5 is exactly
   such a string.**
3. **Search the panel's dimensions and resolution** — "1.8 inch 360x360 round" finds the module
   family across vendors.
4. **Search GitHub for the silkscreen string and the vendor names together.** Community projects
   frequently support several siblings from one repo, and their README will tell you which. This is
   precisely how the §5 relationship was documented **[COM]**.
5. **Look for an ESPHome or LVGL port** — those configs are effectively a machine-readable pinout.
6. **Check the vendor's siblings.** Waveshare copy-pastes wiki pages across a product family; a
   sibling board's page is sometimes better written **[DOC]**.

---

## 5. Worked example — Waveshare knob board and Guition `JC3636K518`

The best-evidenced sibling relationship in this repository. Full detail, with repository links and
commit hashes, is in
[examples/catalog.md §1.1](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/catalog.md).

**The two boards:**

| | [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) | **Guition K5 Knob Series JC3636K518** |
|---|---|---|
| Vendor | Waveshare (product ID 31623) | Guition |
| Documentation | MediaWiki, schematic ZIP, demo, factory BIN **[DOC]** | Vendor source ZIP on `pan.jczn1688.com` **[COM]** |
| Relationship | **Siblings.** Neither is established as the original | |

### What is shared — [COM], quoting the `nkinnan` repository

> *"I wouldn't be surprised if Waveshare and Guition are buying the screens and the housing from the
> same supplier made on the same production line. […] They are largely identical though, right down
> to the spot for the battery and the daughter PCB underneath the main PCB, even connected the same
> way."*

Shared: the screen, the housing, the battery location, and **the daughter-PCB-under-main-PCB
architecture, connected the same way** — i.e. the [dual-MCU
structure](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md) is common to
both.

### What differs — [COM]

> *"There are some very small differences in the PCB between the two of them, enough to know it was
> re-laid-out."*

**The PCB was re-laid-out.** The differences are described as small, and are **not enumerated** in the
source — so *which* nets or components differ is **unknown**. Do not assume pin-for-pin identity.

### The asymmetry worth knowing about

**Guition publishes application source that Waveshare does not.** The `JC3636K518CN_knob_EN.zip`
appears to be the same application as the Waveshare comprehensive example **[COM]**:

> *"The JC3636K518 source code seems to be identical to the shipping Waveshare firmware (or at least
> an older version of it […]). I have no idea how that happened, I doubt they re-implemented it."*

If accurate, **this is the closest thing to source for the factory UI that exists publicly** — which
directly addresses the "no source for the comprehensive example" gap in our device documentation.

**We could not retrieve it.** `pan.jczn1688.com` is a JavaScript file manager; the direct link
returns HTML and the Cloudreve API paths 404. It needs a browser session **[COM]**:

```
https://pan.jczn1688.com/s/54f682          (file: JC3636K518CN_knob_EN.zip)
https://pan.jczn1688.com/directlink/1/HMI%20display/JC3636K518CN_knob_EN.zip
```

### The methodological warning this example produced

A chip readout in the `nkinnan` repository reports the ESP32-U4WDH as *"Dual Core + LP Core,
240MHz"*. That is relevant to the
[core-count question](../../components/espressif/esp32-u4wdh/README.md), **but it is a reading from
the Guition board, not from a Waveshare unit** — and `esptool`'s feature string for U4WDH parts is
exactly what that record says is unreliable. **It does not settle the question** **[COM]**.

> **This is the general lesson, and it is the most useful thing on this page.** A measurement taken
> from a sibling board is evidence *about that sibling*. It is a strong hint about the other, and it
> is **not** a substitute for measuring the board you actually have. Record which unit a reading came
> from, always.

### Licensing note

The `nkinnan` repositories declare **no licence**, and the SD-card archive contains commercial anime
artwork and copyrighted music. **This repository deliberately does not mirror them** — link-only
**[COM]**.

---

## 6. Working with a clone you already own

1. **Do the §3 triage before anything else.**
2. **Find the nearest documented sibling** (§4) and read its record — but treat every pin assignment
   as a hypothesis.
3. **Write down the differences you find.** A clone with a known pin map is as good as an original.
4. **Prefer community drivers over vendor drivers.** They are usually written against several
   siblings and are more defensive. Our display situation is the case in point — the
   [SH8601 compatibility record](../../components/generic/sh8601-compatibility-driver/README.md)
   exists precisely because driver reality and vendor labelling diverged.
5. **Mirror any vendor file you find, immediately**, with checksum and retrieval date. Tier-4 vendors
   delete things — see
   [vendor-comparison.md §3](vendor-comparison.md#3-documentation-durability--the-axis-nobody-advertises).
6. **Contribute the pin map back.** This is the only mechanism by which this class of hardware ever
   becomes documented.

---

## 7. Evidence boundary

- **[COM]-sourced and well-evidenced:** everything in §5 about the Waveshare/Guition relationship,
  quoted from the `nkinnan` repositories via
  [examples/catalog.md](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/catalog.md)
  (repository metadata retrieved 2026-08-23). **These are one community author's reports.** They are
  specific, internally consistent and cite a person who owned both boards — but they are **not
  independently verified**, and **we have handled neither board**.
- **[DOC]-sourced:** the display-controller conflict, the touch-controller address differences, the
  dual-MCU architecture, and the Waveshare documentation characteristics — all from this repository's
  2026-08-21 to 2026-08-23 research passes.
- **[INF] — not verified:** all of §2 (listing-photo heuristics), the §3 triage procedure, and §4's
  tracing method. These are **methodology proposals based on the failure modes we have documented**,
  not a validated procedure. **No clone board has been purchased, received or tested by this
  repository.**
- **Explicitly unknown:** *which* nets or components differ between the Waveshare and Guition PCBs;
  whether the Guition source is genuinely identical to the Waveshare factory firmware; whether either
  vendor is the original designer.
- **Not retrieved:** `JC3636K518CN_knob_EN.zip`.

---

## 8. Related

- [Vendor and marketplace comparison](vendor-comparison.md) — the companion document
- [Waveshare knob board](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) · [community catalogue](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/examples/catalog.md) · [gaps and conflicts](../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md)
- [Espressif ecosystem map](../espressif/ecosystem-and-product-lines.md)
- Touch-controller vendors: [Hynitron](../../vendors/hynitron/README.md) · [Goodix](../../vendors/goodix/README.md) · [Chipsemi](../../vendors/chipsemi/README.md)
- Display: [Sitronix](../../vendors/sitronix/README.md)
