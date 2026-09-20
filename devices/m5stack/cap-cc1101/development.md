# Development — Cap CC1101 & NFC (U219)

No processor, no firmware of its own. Everything is host-side. Snapshot 2026-09-04, seven
days after release — **expect this page to age quickly**.

## 1. Toolchains

| Path | Status |
|---|---|
| **Arduino / PlatformIO** | Vendor guides published for **both** subsystems (`docs.m5stack.com/en/arduino/projects/cap/cap_cc1101`). `not-tested` |
| **ESP-IDF** | `M5Unit-NFC` ships ESP-IDF example forms (`examples/**/main/*.cpp`) and Kconfig variants. CC1101 side is RadioLib, Arduino-flavoured |
| **UiFlow2 / MicroPython** | `uiflow-micropython.readthedocs.io/zh-cn/latest/cap/cc1101.html` — note the vendor links the **zh-cn** path from the English page |
| **Meshtastic** | **Not applicable.** CC1101 cannot do LoRa |
| **Bruce / M5Launcher** | Not yet. Band switching *"will still need to be implemented by the dev"* — u/No_Confusion7932, [r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0nwti/) |

## 2. Libraries

| Library | Role | Pin |
|---|---|---|
| **RadioLib** (jgromes) | CC1101 driver — the vendor's "CC1101 Driver Library" link | release **7.7.1** (2026-05-31), head `187ef247…` (2026-08-22). **MIT** |
| **m5stack/M5Unit-NFC** | ST25R3916 driver — class `m5::unit::CapCC1101NFC` (alias of `CapST25R3916`) | head `93745b547364f310cd64b5155a870103a7800a5d` (2026-06-10), release **0.1.0** (2026-06-10). **MIT** |
| **M5Unified / M5GFX / M5UnitUnified** | board abstraction, `wiring::addSPI` | not pinned by the docs |
| **M5Cardputer** | keyboard | `github.com/m5stack/M5Cardputer` |

> **No M5Stack CC1101 library exists** (`org:m5stack cc1101` → 0 repositories, 2026-09-04).
> The NFC library, by contrast, is M5Stack's own and predates the product by 11 weeks.

Required constants from RadioLib for band switching:
`RADIOLIB_CC1101_GDOX_HW_TO_0`, `RADIOLIB_CC1101_GDO2_INV`, `RADIOLIB_CC1101_GDO2_NORM`.

## 3. Build sketch

```cpp
// platformio.ini (illustrative, not-tested)
[env:cardputer-adv-cap-cc1101]
platform  = https://github.com/pioarduino/platform-espressif32.git
board     = m5stack-stamps3
framework = arduino
lib_deps  =
  m5stack/M5Unified
  m5stack/M5Cardputer
  https://github.com/m5stack/M5Unit-NFC.git#93745b547364f310cd64b5155a870103a7800a5d
  jgromes/RadioLib@^7.7.1
build_flags = -DUSING_CAP_CC1101
```
`inferred` — assembled from the vendor guides' `#include` sets and the libraries' own
metadata. **Not built.** The `pioarduino/platform-espressif32` reference is taken from
M5Stack's own Stamp-C6LoRa documentation, which pins `#55.03.37`.

## 4. Bring-up order (matters here)

1. **Host G3 (`POWER_EN`) → HIGH.** Nothing on the Cap answers until the rail is up.
2. SPI up.
3. **CC1101:** `radio.begin(freq, bitrate, freqDev, rxBw, power, preambleLen)`.
4. **Band:** host GPIO for `RF_SW0`, `IOCFG2` write for `RF_SW1`
   ([`features/band-switching.md`](features/band-switching.md)).
5. **NFC:** `m5::unit::wiring::addSPI(Units, unit, 10'000'000, 1)` then `Units.begin()`.
   ⚠ **SPI mode 1** — different from the CC1101's.

## 5. Flashing / recovery

Host-side only; the Cap has no flash, no MCU, no bootloader. Cardputer-Adv download mode:
power switch OFF, hold **G0**, power on, release.

If the Cap seems dead: check `POWER_EN` (G3) first — that is the failure mode unique to
this board and it looks exactly like a dead Cap.

## 6. Risks

| Risk | Note |
|---|---|
| Transmitting with the **wrong band antenna** | Three whips ship; they are not interchangeable. Not damaging at +10 dBm, but range collapses |
| Transmitting with **no antenna** | The vendor's no-antenna damage warning is on the *LoRa* Cap (+22 dBm). At +10 dBm the risk is much lower, but there is no vendor statement either way for this board — treat as unknown |
| **Transmitting out of band for your region** | The examples default to **915.0 MHz**. See [`features/sub-ghz.md` §7](features/sub-ghz.md) |
| Driving both chips without re-establishing SPI mode | Silent corruption — [`features/nfc.md` §8](features/nfc.md) |

## 7. Related

[`features/sub-ghz.md`](features/sub-ghz.md) · [`features/nfc.md`](features/nfc.md) ·
[`features/band-switching.md`](features/band-switching.md) ·
[`pinouts-and-buses.md`](pinouts-and-buses.md) · [`commands.md`](commands.md)
