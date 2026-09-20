# Adding LoRa and NFC to CrossPoint-family firmware on the PaperMono

> A feasibility assessment grounded in the actual SDK source, not in what the
> abstraction layer implies.
>
> Researched **2026-09-04**. Repository and source facts are `executed-success`
> — repos cloned, headers read, GitHub compare API called. Effort estimates and
> design suggestions are `inferred`. **No hardware; nothing was built or run for
> this assessment.**

## The headline

**You do not need to extend the FreeInk SDK to reach the radios.** Firmware
source can call `Wire`, `SPI` and RadioLib directly, and **CrossInk already does
exactly this for ESP-NOW** — so there is a working precedent in the ecosystem for
bypassing the capability system entirely.

The SDK abstraction is a convenience layer, not a gatekeeper. That is the
opposite of the *plugin* boundary, which is enforced at link time.

| Layer | Can it reach a bus? | Enforcement |
|---|---|---|
| **Plugin** (native ELF, `mekhontsev`) | **No** | Hard. 81-symbol allow-list; **the link fails** |
| **Plugin** (upstream JS) | **No** | Absolute — no MCU-side execution at all |
| **Firmware source** (any fork) | **Yes** | None. `#include <Wire.h>` and go |

## 1. Does CrossInk look receptive to radio work?

**Its stated scope says no. Its shipped code says it already did it.**

`README.md`: *"a **personal fork** … with a focus on **improved fonts and minimal
reading stats**"*, and *"keeping the underlying system stable while layering in a
few 'nice-to-have' features."*

`SCOPE.md` inherits upstream's anti-kitchen-sink mission verbatim and adds:
*"If you have a major feature request, it should first be directed at the main
project since this is a downstream project that consumes their updates."*

**But it has already shipped two radio features**, and they are the key evidence
for this whole assessment:

| File | What it does |
|---|---|
| `src/activities/reader/NearbyBookPositionSyncActivity.cpp` | ESP-NOW reading-position sync between two readers |
| `src/activities/network/NearbyStatsSyncActivity.cpp` | ESP-NOW stats transfer |

These `#include <esp_now.h>` and call `esp_now_init()`,
`esp_now_register_recv_cb()`, `esp_now_send()`, `esp_wifi_set_ps()` **straight
from an Activity**. There is no `FREEINK_CAP_ESPNOW`, no SDK manager, no
board-profile field. The abstraction was simply bypassed.

**Conclusion:** CrossInk demonstrates the technique but is a poor host for this
work — its supported devices are **X3, X4 and Sticky only**, it has no PaperMono
support, and its author would likely (correctly) point LoRa/NFC upstream.

## 2. Powering the radios — what already exists, and the four missing lines

On the PaperMono the radios are not on direct GPIO. The ST25R3916 and the LoRa
module sit behind the **M5IOE1 expander** and the **M5PM1 power manager**
([pinouts](../../../devices/m5stack/papermono/pinouts-and-buses.md)).

**Good news: the SDK already drives both chips.** `BoardConfig/include/` contains
`M5Ioe1.h` (160 lines) and `M5Pm1.h` (213 lines) — full register maps, bus
init, and inline I²C read/write helpers, all PaperMono-aware.

`M5Pm1.h` even handles the board difference correctly:

> *"PaperColor: SDA3/SCL2. Paper Mono: SDA47/SCL48 … its GPIO2/3 are KEY1/KEY2,
> so the PaperColor default there would put Wire on button pins and kill the
> whole bus."*

### What is missing is only the pin constants

`M5Ioe1.h` defines named masks for exactly the pins the *reader* needs:

```
PIN_TF_DETECT (IO1) · PIN_EPD_POWER (IO3) · PIN_EPD_RESET (IO5)
PIN_TOUCH_RESET (IO6) · PIN_LED_GREEN (IO8) · PIN_LED_BLUE (IO9)
PIN_MIC_POWER (IO12) · PIN_TOUCH_POWER (IO13) · PIN_SD_POWER (IO14)
```

**Absent — and they are precisely the radio pins:**

| Pin | Net | Function | In SDK? |
|---|---|---|---|
| IO2 | `PYB_LoRa_ANT_SW` | LoRa antenna switch | **no** |
| IO4 | `PYB_NFC_EN` | **NFC power enable** | **no** |
| IO10 | `PYB_LoRa_RST` | **LoRa reset** | **no** |
| IO11 | `PYB_CHG_IIC` | charger I²C gate | no |

Similarly `M5Pm1.h` names only **`GPIO0`** (EPD_EN). The PaperMono's **`G2` =
`PYG2_LoRa_EN`**, which enables the `3V3_L2_LoRa` rail through an SSP7615 LDO, has
no constant.

So step 2 is genuinely small — add four `constexpr uint16_t` masks, extend
`OUTPUT_MASK`, add a `GPIO2` constant:

```cpp
// M5Ioe1.h — additions
constexpr uint16_t PIN_LORA_ANT_SW = 1u << 1;   // IO2  PYB_LoRa_ANT_SW
constexpr uint16_t PIN_NFC_POWER   = 1u << 3;   // IO4  PYB_NFC_EN
constexpr uint16_t PIN_LORA_RESET  = 1u << 9;   // IO10 PYB_LoRa_RST
// extend OUTPUT_MASK with all three

// M5Pm1.h — addition
constexpr uint8_t GPIO2 = 1 << 2;               // PYG2_LoRa_EN -> 3V3_L2_LoRa
```

**Verify the bit positions against the schematic before use** — the masks above
are derived from the device record's pin table (IO*n* → bit *n−1*, matching the
existing entries), not read from a datasheet. `inferred`.

## 3. Talking to the radios

### The SPI pins are not in the board profile at all

The `PAPER_MONO` profile in `BoardConfig.h` covers display, touch, SD, RTC,
buttons, frontlight, audio, LEDs and mic. Grepping the whole SDK for the LoRa SPI
pins — **GPIO 38/39/40/41 (MOSI/CLK/MISO/NSS), 21 (BUSY), 5 (IRQ)** — returns
**nothing**. There is no struct field for a radio, so there is nowhere to put
them even if you wanted to.

For a prototype that does not matter: hardcode them in your Activity, exactly as
CrossInk hardcodes its ESP-NOW setup.

### LoRa — RadioLib

**RadioLib 7.2.1 is MIT** (verified: `license.txt` and `library.json` both, read
at the tag), and applies all four SX126x §15 errata workarounds at that version
(also verified at source). It is already the pinned driver in M5Stack's own
PaperMono demo.

Sketch — `inferred`, **not compiled**:

```cpp
// bring the rail up, release reset, set the antenna switch
m5pm1::setGpio(m5pm1::GPIO2, true);          // 3V3_L2_LoRa
m5ioe1::setPin(m5ioe1::PIN_LORA_RESET, true);
m5ioe1::setPin(m5ioe1::PIN_LORA_ANT_SW, /* per band */);

SPIClass spi(HSPI);
spi.begin(/*CLK*/39, /*MISO*/40, /*MOSI*/38, /*NSS*/41);
SX1262 radio = new Module(41, /*IRQ*/5, /*RST*/RADIOLIB_NC, /*BUSY*/21, spi);
radio.begin(868.0, 125.0, 9, 7, 0x12, 22, 8, /*tcxoVoltage*/3.0f, /*useRegulatorLDO*/true);
```

Two board facts that matter and are already established in this knowledge base:
**reset is not on an ESP32 GPIO** (pass `RADIOLIB_NC` and drive the expander
instead), and the vendor demo selects **LDO regulation** — roughly doubling
receive current — presumably because the module omits the DC-DC inductors.

**Regional band configuration becomes your legal responsibility** the moment you
transmit. See [`guides/lora`](../../../guides/lora/README.md).

### NFC — ST25R3916

I²C `0x50` on the **shared system bus** (SDA 47 / SCL 48), IRQ on GPIO 6, power
via M5IOE1 IO4. Driver options: ST's **RFAL** (the reference implementation) or
`M5Unit-NFC`.

**The shared-bus hazard is the real design constraint here.** That bus already
carries the RTC (`0x32`), touch (`0x38`), the expander (`0x4F`), the IMU
(`0x68`) and the PMIC (`0x6E`) — and the IP2315 charger has a documented
bus-wedge failure mode. An NFC polling loop that holds the bus will interfere
with touch responsiveness and RTC reads. See
[resources-and-conflicts](../../../devices/m5stack/papermono/resources-and-conflicts.md).

## 4. Prototype now, upstream later — and they are different jobs

| | Prototype (fork) | Upstreamable (SDK) |
|---|---|---|
| Pin constants | hardcode in the Activity | `M5Ioe1.h` / `M5Pm1.h` additions |
| Rail control | call the inline helpers directly | same, via named constants |
| Driver | RadioLib in `src/activities/` | a `LoRaManager` peer to `Rtc`/`Imu` |
| Capability gating | none | `FREEINK_CAP_LORA`, `FREEINK_CAP_NFC` |
| Board profile | untouched | new radio struct fields |
| Other boards | ignored | LilyGO T5S3 already has LoRa pins defined |
| Effort | **days** | **weeks**, plus review |

**Start with the prototype.** It answers the question that actually matters — does
the hardware work, are the rails right, does the antenna switch behave — without
committing to an SDK API design. CrossInk's ESP-NOW work is the precedent for
shipping useful radio functionality this way indefinitely.

**Then upstream if it proves out.** Note the SDK already carries LoRa pin
definitions for the **LilyGO T5S3** (`T5S3_LORA_CS/IRQ/RST/BUSY`), so a second
LoRa board exists to justify a real abstraction — that is the argument for
`FREEINK_CAP_LORA` rather than a PaperMono special case.

### Which fork to start from

**Upstream CrossPoint, not CrossInk.** It already has `[env:papermono]` and pins
the SDK commit containing PaperMono support. CrossInk would cost a **136-commit
SDK bump** *plus* a **294-commit merge into 224 modified `lib/` files**, for no
benefit — see [the fork network](fork-network.md).


## Update 2026-09-07 — NFC is now demonstrated on this board

[`ciniml/paper_name_plate`](https://github.com/ciniml/paper_name_plate) is
bare-metal `no_std` Rust firmware for the PaperMono carrying a **28.9 KB
ST25R3916 driver**, **19.8 KB of NFC Forum Type 2 Tag emulation**, ISO-DEP and
NDEF — plus its own `pm1.rs` and `ioe1.rs`.

Three things it settles:

1. **NFC works on this hardware from third-party code.** The argument above was
   that the radios were reachable from firmware source; this is the proof.
2. **It wrote its own PMIC and expander drivers rather than using the FreeInk
   SDK** — independently reaching the conclusion this assessment reached, that
   the SDK abstraction is optional.
3. **It confirms the three "missing" pins** — `IO4 = NFC_EN`, `IO10 = LoRa RST`,
   `IO2 = LoRa ANT SW` — from its own reading of the hardware, matching this
   knowledge base's schematic extraction exactly.

It also states the M5GFX waveform LUTs are **FreeBSD-licensed and reusable**,
and that recovering the panel from deep sleep **requires a hardware reset via
IOE1 IO5**.

**LoRa remains undemonstrated anywhere.** `paper_name_plate` lists the SX1262
pins and explicitly scopes it out. No project found drives LoRa on this board.

Full analysis: [new PaperMono projects, 2026-09](new-papermono-projects-2026-09.md).
It carries **no `LICENSE` file** — all rights reserved; read for technique, do not copy.

## Incidental findings

Two things surfaced that belong in the device record:

**FreeInk drives the panel at 20 MHz.** `PAPER_MONO`'s profile sets SPI to
`20000000` — matching the SSD1677 datasheet maximum, and **contradicting M5GFX's
40 MHz**, which this knowledge base recorded as an unresolved conflict. FreeInk
chose the compliant clock. That is a second independent implementation siding
with the datasheet.

**The SDK declares `ImuType::None` for the PaperMono** despite the board having a
BMI270 at `0x68` — and `FREEINK_CAP_IMU` therefore excludes it. The IMU is fitted,
wired and unused. Whether that is deliberate (power, or the interrupt landing on
the M5PM1 rather than the ESP32) or simply unported is **not established**.

## What was not done

- **Nothing was built.** No prototype compiled, no radio initialised, no hardware.
- The M5IOE1 bit positions above are **derived, not read from a datasheet**.
- `m5ioe1::setPin` / `m5pm1::setGpio` are used illustratively; the **exact helper
  signatures were not read** — only that inline read/write primitives exist.
- No check of whether upstream or FreeInk have stated any intent to add radios.
- The IMU-disabled question was not chased.

## See also

- [CrossPoint Reader](../../applications/crosspoint-reader/README.md) · [plugin systems](../../applications/crosspoint-reader/plugins/README.md) — why a plugin cannot do this
- [FreeInk SDK](../../frameworks/freeink-sdk/README.md) · [fork network](fork-network.md)
- [PaperMono pinouts](../../../devices/m5stack/papermono/pinouts-and-buses.md) · [NFC](../../../devices/m5stack/papermono/features/nfc.md) · [LoRa](../../../devices/m5stack/papermono/features/lora.md)
- [`guides/lora`](../../../guides/lora/README.md) · [`guides/nfc`](../../../guides/nfc/README.md)
