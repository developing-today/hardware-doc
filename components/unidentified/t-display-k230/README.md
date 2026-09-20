# Unidentified parts — LilyGO T-Display K230

Scope-limited to this board, per the convention that unidentified parts must not collapse into a
single shared record. Every entry states what is known, what evidence would resolve it, and why
it was not resolved on 2026-09-04.

## U1 — Main-board PMIC

**Known:** the K230's PMU block provides "**two output IOs to control PMIC and system reset**"
(Canaan brief datasheet), so an external PMIC is architecturally required. The board is
battery-powered and runs a 1.6 GHz core with DVFS, so it is not a two-LDO design.

**Not known:** manufacturer or part number. A full part-number sweep of the LilyGO BSP,
launcher, device trees and Buildroot config on 2026-09-04 — regex-matching every common
PMIC/regulator prefix including `axp`, `sy`, `mp`, `tps`, `eta`, `sgm`, `rk8`, `hi65` — returned
**no PMIC part at all**. This is consistent with a PMIC that Linux never touches, i.e. one
sequenced entirely by the K230 PMU in hardware.

**What would resolve it:** a photograph of the main-board PCB, or a LilyGO schematic. Neither
exists publicly; the wiki's `#schematic` heading has **no link under it** (verified 2026-09-04).

**Why it matters:** without it, nothing can be said about rail voltages, DVFS operating points,
programmable current limits or true shutdown behaviour.

## U2 — Speaker amplifier on the main board / cased version

**Known:** the Cased Version wiki page lists "microphone, **speaker**, 3.5 mm headphone jack".
The K230 has an on-die codec with 2 DAC channels, but a codec cannot drive a speaker directly.
A separate amplifier must exist on the main board or in the case assembly.

**Not known:** part number. The only amplifier named anywhere in LilyGO's sources is the
**MAX98357A on the nRF52840 base board**, which is a *different* board.

**What would resolve it:** PCB photograph, or an `aplay -l` / ALSA control dump from a running
cased unit.

## U3 — Microphone

**Known:** a microphone is listed on the wiki and the launcher has `ui_mic_spectrum.c` and a
Xiaozhi wake-word path that "owns the microphone". The K230 supports up to 8 PDM DMICs *and* 2
analogue ADC channels, so either type is possible.

**Not known:** PDM or analogue, part number, count.

## U4 — "RC01812" Ethernet part

**Known:** the T-Display K230 Kit shop listing states "Ethernet Module | Name: **RC01812** |
Connector: RJ45". The wiki instead names **RTL8152B**.

**Assessment:** `RC01812` matches no Realtek, Microchip, ASIX or Corechips Ethernet controller
naming scheme. It is most consistent with an **RJ45 jack with integrated magnetics** part number
from a Chinese connector vendor. **This is an interpretation, not a finding.** Both designations
are recorded in [`components/realtek/rtl8152b`](../../realtek/rtl8152b/README.md) and in
`GC-3`.

## U5 — Claimed ESP32-S3-R8 co-processor

**Known:** LilyGO's wiki page for the T-Display K230 states the board is "combined with
**ESP32-S3-R8** (16 MB Flash, 8 MB PSRAM) for Wi-Fi/Bluetooth connectivity", offers PlatformIO
and Arduino instructions for an "ESP32-S3 co-processor", and lists "Bluetooth 5.0 LE (ESP32-S3)".

**Contradicting evidence:** an exhaustive part-number sweep of the entire T-Display-K230
repository at commit `bb831ab…` finds **zero** occurrences of `esp32`, `esp32s3` or any
Espressif identifier. The BSP's Wi-Fi is RTL8189FS over SDIO; its Bluetooth is a USB dongle with
a CSR8510 workaround patch. The shop listing names RTL8189, not ESP32-S3. The Cased Version wiki
page names no Wi-Fi chip at all.

**Assessment:** most likely a copy-paste from a sibling LilyGO product page. **Not resolved.**
Recorded as `GC-2`. A component record for
[`espressif/esp32-s3r8`](../../espressif/esp32-s3r8/README.md) already exists in this repository
and has deliberately **not** been given a Used-By entry for this board, because the claim is
unverified.

## U6 — 21700 cell and battery assembly

**Known:** the nRF52840 base board's `P0.04` enables an "external 5 V boost … for boosting the
**21700 battery compartment**". So the kit's power source is a 21700 cell, not a pouch LiPo.

**Not known:** capacity, chemistry, protection-circuit part, cell vendor, whether a cell is
included in any SKU. Community report 2026-08-20: an early buyer received "just the screen and
motherboard on risers in the package" with no case or battery.

## Sources

All claims above are sourced from the same primary set used by the device record: LilyGO's
`T-Display-K230` repository at commit `bb831ab358b66f5bd9a87ecd7c580fee4537492e`, LilyGO's shop
listings and wiki retrieved 2026-09-04, and the Canaan K230 datasheets at `k230_docs` commit
`f8e30213963e0ed5cf995c3cd4701218a45e4793`. See
[`devices/lilygo/t-display-k230/sources.md`](../../../devices/lilygo/t-display-k230/sources.md).
