# LoRa — Cap LoRa-1262 (U214) on Cardputer-Adv

> **Common guide:** [`guides/lora`](../../../../guides/lora/README.md) holds the
> device-independent material — SF/BW/CR against airtime, LoRa vs LoRaWAN vs Meshtastic,
> regional band plans and duty cycle, `BUSY`/TCXO/RF-switch mechanics, generic failure
> signatures.
>
> **Applicability:** the standard approach **applies with deltas**. On this board the
> radio's `NRST`, `DIO1` and `BUSY` are ordinary host GPIO (unlike the PaperMono, where
> reset hides behind an I²C expander), but the **antenna switch is behind an I²C expander**
> at `0x43`, the SPI bus is **shared with the microSD card**, and the **TCXO voltage is
> disputed between the vendor (3.0 V) and Meshtastic upstream (1.8 V)**.

> **How do I send and receive a LoRa packet?** — §5 (M5Stack/RadioLib), §6 (Meshtastic).
> **How do I port this to my own firmware?** — §11.
> Snapshot **2026-09-04** · schematic **V1.1** · nothing tested on hardware here.

---

## 1. Hardware path

```
ESP32-S3 (Stamp-S3A) ── SPI ──▶ M1  Stamp LoRa-1262 Mini ──▶ pin 12 ANT ──▶ E4 SMA/RP-SMA
  G40 SCK · G14 MOSI · G39 MISO · G5 NSS            (Semtech SX1262 inside)
  G6  ◀── BUSY   (module pin 3)
  G4  ◀── DIO1   (module pin 4, net LoRa_IRQ)
  G3  ───▶ NRST  (module pin 2)
                                    module pin 10 SW ◀── PI4IOE5V6408 P0 ◀── I²C 0x43 (G8/G9)
                                    module pin 5 3V3 ◀── JW5712 buck (no host enable)
```

| Element | Part | Record |
|---|---|---|
| Module | `Stamp LoRa-1262 Mini`, `M1` | [`components/m5stack/stamp-lora-1262`](../../../../components/m5stack/stamp-lora-1262/README.md) |
| Radio | **Semtech SX1262** | [`components/semtech/sx1262`](../../../../components/semtech/sx1262/README.md) |
| Antenna switch control | `PI4IOE5V6408` P0 @ 0x43 | [`components/diodes-incorporated/pi4ioe5v6408`](../../../../components/diodes-incorporated/pi4ioe5v6408/README.md) |
| 3.3 V rail | `JW5712` | [`components/joulwatt/jw5712`](../../../../components/joulwatt/jw5712/README.md) |
| Antenna connector | `E4` `SMA-KE` | [`components/generic/rp-sma-and-sma-antenna-connectors`](../../../../components/generic/rp-sma-and-sma-antenna-connectors/README.md) |

## 2. Resources consumed

| Resource | Value | Contention |
|---|---|---|
| Host GPIO | **7** — G40, G14, G39 (SPI), G5 (NSS), G6 (BUSY), G4 (DIO1), G3 (NRST) | SPI trio shared with **microSD** (CS = G12) |
| I²C | `0x43` on G8/G9 | shared with TCA8418 keyboard, BMI270 IMU, ES8311 codec, Grove port |
| SPI clock | M5Stack examples leave it to RadioLib's default; Meshtastic runs the shared bus with `spiLock` arbitration | |
| Interrupt | G4, rising edge (RadioLib's `setPacketReceivedAction`) | |
| 3.3 V budget | `JW5712` sheet annotation `IOUT: 0~0.6 A`; SX1262 TX at +22 dBm is the dominant load | |

> **The SPI bus is shared with the SD card and this is deliberate upstream.** Meshtastic's
> `variant.h` comment is explicit: *"SD card slot — shares the SPI bus with the LoRa radio
> (separate chip select). The default SPI instance is used; spiLock arbitrates access
> between radio and SD."* Any firmware that opens the radio on a dedicated bus and the SD
> on another will fight itself. **[SRC]**

## 3. Bring-up order

Unlike the PaperMono, **there is no host power-enable to sequence** — the JW5712 comes up
with the host's 5 V (`R1` 10 kΩ pull-up on `ENB`). What *does* have to happen before RF
works is the antenna switch:

1. Bring up I²C on **G8/G9**.
2. Probe **0x43**. Present ⇒ Cap LoRa-1262. Absent ⇒ Cap LoRa868 (or no Cap).
3. On the expander: **P0 → output**, **P0 → not high-impedance**, **P0 → HIGH**.
4. Release `NRST` (G3) — RadioLib will do this if you pass `GPIO_NUM_3` as the reset pin.
5. `radio.begin(...)`.

Skipping step 3 gives a radio that initialises perfectly and transmits into a dead port.
Both M5Stack and Meshtastic do the three expander writes in exactly that order. **[SRC]**

## 4. Software options

| Stack | What it gives you | Where |
|---|---|---|
| **RadioLib** (jgromes) | Raw LoRa / (G)FSK point-to-point. What both M5Stack examples use. **MIT** licensed (verified from the repository's licence metadata, 2026-09-04) | `github.com/jgromes/RadioLib`, latest release **7.7.1** (2026-05-31), head `187ef247…` (2026-08-22) |
| **Meshtastic** | Full mesh firmware with UI, BLE, GNSS, keyboard. **Officially supported upstream** — see §6 | `meshtastic/firmware`, board `m5stack-cardputer-adv` |
| **MeshCore** | Alternative mesh protocol. Community ports only | §7 of [`../projects-and-community.md`](../projects-and-community.md) |
| **UiFlow2 / MicroPython** | Block + MicroPython API, `uiflow-micropython.readthedocs.io/en/latest/cap/lora1262.html` | vendor |
| **LoRaWAN** | **Nothing demonstrated.** RadioLib has a LoRaWAN class that supports SX1262, but no M5Stack example, no community project and no regional-parameters configuration for this board was located | gap **G8** |
| M5Stack-specific LoRa driver | **Does not exist.** There is no `M5Unit-LoRa`-style library for either Cap; the docs' "Arduino LoRa Driver Library" link points straight at RadioLib | verified by GitHub org search, 0 results |

## 5. The vendor's exact radio configuration

From M5Stack's Arduino guide (served at `/en/arduino/projects/cap/cap_lora868`, which
covers **both** Caps and auto-detects which one is fitted). `executed-success` on the read;
`not-tested` on hardware. **[DOC]**

```cpp
#include <M5Unified.h>
#include <RadioLib.h>
#include "utility/PI4IOE5V6408_Class.hpp"

#define LORA_BW           125.0f   // kHz
#define LORA_SF           12
#define LORA_CR           5        // 4/5
#define LORA_FREQ         868.0    // MHz
#define LORA_SYNC_WORD    0x34
#define LORA_TX_POWER     22       // dBm
#define LORA_PREAMBLE_LEN 20       // symbols

// SX1262 PIN order: NSS, IRQ(DIO1), RST, BUSY
SX1262 radio = new Module(GPIO_NUM_5, GPIO_NUM_4, GPIO_NUM_3, GPIO_NUM_6);

m5::PI4IOE5V6408_Class ioe(0x43, 400000, &m5::In_I2C);

void setup() {
    M5.begin();
    if (!m5::In_I2C.begin(I2C_NUM_0, 8, 9)) { /* fail */ }

    if (ioe.begin()) {                    // 0x43 present -> Cap LoRa-1262
        ioe.setDirection(0, true);        // P0 = output
        ioe.setHighImpedance(0, false);   // actually drive it
        ioe.digitalWrite(0, true);        // P0 = HIGH -> antenna switch on
    } else {                              // 0x43 absent  -> Cap LoRa868
        /* no switch to set */
    }

    int state = radio.begin(LORA_FREQ, LORA_BW, LORA_SF, LORA_CR,
                            LORA_SYNC_WORD, LORA_TX_POWER, LORA_PREAMBLE_LEN,
                            3.0,     // tcxoVoltage  <-- see §8
                            true);   // useRegulatorLDO
    radio.setCurrentLimit(140);      // 0-140 mA, 2.5 mA step
    radio.setPacketReceivedAction(setFlag);
    radio.startReceive();
}
```

Receive-side helpers in the same guide: `radio.readData()`, `radio.getPacketLength()`,
`radio.getRSSI()`, `radio.getSNR()`, `radio.getFrequencyError()`.

**Prose on those numbers.** SF12 / BW 125 kHz / CR 4/5 at 868.0 MHz is a *long-range demo*
setting: on the order of ~250 bit/s of raw chip rate with airtimes measured in seconds for
a short payload. It is not a sane default for anything interactive, and in EU 868 the 1 %
duty-cycle limit will bite quickly at that airtime. `useRegulatorLDO = true` disables the
SX1262's internal DC-DC and roughly doubles receive current — the same choice the PaperMono
firmware makes, and the SX1262 record explains what it costs
([`components/semtech/sx1262` §5.4](../../../../components/semtech/sx1262/README.md)).

## 6. Meshtastic — officially supported, with the exact provenance

| Fact | Value |
|---|---|
| Board target | **`m5stack-cardputer-adv`** (PlatformIO env `[env:m5stack-cardputer-adv]`, `board = m5stack-stamps3`) |
| Variant directory | [`variants/esp32s3/m5stack_cardputer_adv/`](https://github.com/meshtastic/firmware/tree/master/variants/esp32s3/m5stack_cardputer_adv) — `variant.h` (2 349 B, blob `778d95f200fe116a7a413d47c7276d4193d6c7dc`), `platformio.ini` (1 164 B, blob `a38317e5be3fd62607ad6b06a1f7c7ea176a1657`), `pins_arduino.h` (494 B, blob `12581cde0200a5787d77889d4abe418229cc6952`) |
| Extra variant code | [`src/platform/extra_variants/m5stack_cardputer_adv/variant.cpp`](https://github.com/meshtastic/firmware/blob/master/src/platform/extra_variants/m5stack_cardputer_adv/variant.cpp) (2 782 B) |
| Introduced by | PR **[#9540 "Cardputer Kit"](https://github.com/meshtastic/firmware/pull/9540)** by **caveman99**, opened 2026-02-05, **merged 2026-03-06T11:34:41Z**, merge commit **`969aefa551d645e6110be11f330774e15ad9c87d`** |
| **First release containing it** | **`v2.7.20.6658ec2`, published 2026-03-11T11:43:26Z** (prerelease). Verified with the compare API: `969aefa5…` is **17 commits behind** that tag and **177 commits ahead** of the previous release `v2.7.19.bb3d6d5` (2026-02-11) |
| Device index | `firmware-2.7.20.6658ec2.json` lists `{"board": "m5stack-cardputer-adv", "platform": "esp32s3"}`; still present in `firmware-2.7.26.54e0d8d.json` |
| Protobuf hardware model | **`meshtastic_HardwareModel_M5STACK_CARDPUTER_ADV = 112`** (`src/mesh/generated/meshtastic/mesh.pb.h`). Sibling entry `M5STACK_C6L = 111` |
| Antenna-switch bug + fix | The expander init was **wrong at first**: [PR #10491 "Fix Antenna Switch on Cardputer"](https://github.com/meshtastic/firmware/pull/10491) merged **2026-05-18** (`3261c04afbdc`), followed by **`98e0604edf87`** *"Fix antenna switch initialization logic once more"* on **2026-05-19**. First release with both: **`v2.7.24.472b14c`, 2026-05-23** |
| Other notable commits | `a4b55bc6f24a` 2026-04-22 moved `variant.cpp` to `extra_variants/`; `163c54877c5b` 2026-03-24 fixed I2S sound; `8d3ad2a1462d` 2026-08-02 removed `board_check` |

Radio-relevant `variant.h` lines, verbatim:

```c
#define LORA_SCK 40
#define LORA_MISO 39
#define LORA_MOSI 14
#define LORA_CS 5              // NSS
#define USE_SX1262
#define LORA_DIO0 -1
#define LORA_RESET 3
#define LORA_DIO1 4
#define LORA_DIO2 6
#define SX126X_CS     LORA_CS
#define SX126X_DIO1   LORA_DIO1
#define SX126X_BUSY   LORA_DIO2      // note: BUSY is aliased onto the DIO2 macro
#define SX126X_RESET  LORA_RESET
#define SX126X_DIO2_AS_RF_SWITCH
#define SX126X_DIO3_TCXO_VOLTAGE 1.8
#define TCXO_OPTIONAL
```

And the expander init, verbatim from `variant.cpp`:

```c
#define PI4IO_ADDR        0x43
#define PI4IO_REG_IO_DIR  0x03
#define PI4IO_REG_OUT_SET 0x05
#define PI4IO_REG_OUT_H_IM 0x07
// probes Wire1 then Wire; logs "Cap LoRa-1262 not found" if neither answers
pi4ioWrite(bus, PI4IO_REG_IO_DIR,   0b00000001);   // P0 output
pi4ioWrite(bus, PI4IO_REG_OUT_H_IM, 0b00000000);   // P0 not high-Z
pi4ioWrite(bus, PI4IO_REG_OUT_SET,  0b00000001);   // P0 high
```

Its comment says *"PI4IOE5V6408 on the optional Cap LoRa-1262 **(and Cap LoRa868)**"* —
which contradicts M5Stack's comparison table, where the U201 has **no** RF-switch control.
The code probes and degrades gracefully either way, so the discrepancy is inert; it is
recorded as conflict **G4** in [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).

### 6.1 Meshtastic licensing of the Mesh Kit

M5Stack states the **Cardputer Mesh Kit has been officially licensed by Meshtastic**, with
a registration flow at an "M5 Meshtastic Device registration page", and adds: *"Only
devices in the Cardputer Mesh Kit set can be registered. Other Cardputer/-Adv devices are
not eligible."* **[DOC]** So a Cardputer-Adv + separately-bought U214 runs the same
firmware but cannot claim the authorised-device mark. See
[`../../cardputer-mesh-kit/README.md`](../../cardputer-mesh-kit/README.md).

## 7. Regional bands, antennas and legality — the honest position

| Question | Answer |
|---|---|
| Band the SKU claims | **868 – 923 MHz**, one wideband range |
| Regional variants | **None.** One SKU worldwide |
| Antenna supplied | **One** 3 dBi 108 mm whip, **868 MHz** |
| What M5Stack's example uses | **868.0 MHz** hard-coded (EU) |
| Certification identifier | **None published.** `docs.m5stack.com/en/certification` has no entry for `U214`, `Cap LoRa` or `Cardputer` |
| Duty-cycle handling | none in any vendor code |

Practical consequence, reported repeatedly by owners: **North-American buyers get an
868 MHz antenna and have to source a 915 MHz one.** u/Hyena_Triangles, 2026-08-22:
*"your antennae is 868MHz and for North America you need 915MHz … Edit: new antenna
worked."* ([r/CardPuter](https://old.reddit.com/r/CardPuter/comments/1vvlcs9/)). Another
owner in the same thread reports the stock antenna working fine in NA, which is what you
would expect from a mismatched-but-not-catastrophic whip. u/goattrybe: *"the 868mhz antenna
will work for 915 btw … just a tiny difference in size"*
([r/M5Stack, 2026-02-03](https://old.reddit.com/r/M5Stack/comments/1pzazbe/)). **[COM]**
Three reports across the ~217 threads reviewed; that is enough to say the problem occurs,
not enough to quantify how often.

**The connector polarity is genuinely disputed** and it will cost you an adapter if you get
it wrong — see conflict **G1** in [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md).

## 8. ⚠ The TCXO voltage conflict — the highest-stakes open question here

| Source | `DIO3` TCXO voltage |
|---|---|
| M5Stack Arduino example (both Caps) | **3.0 V** |
| M5Stack PaperMono firmware, same `Stamp LoRa-1262` module family | **3.0 V** |
| **Meshtastic upstream `variant.h`** | **1.8 V**, plus `TCXO_OPTIONAL` |

On the SX1262, `DIO3` is a *regulated supply output* for a TCXO, not a logic pin, and
setting it wrong is the classic failure that produces a radio which initialises cleanly and
then never transmits or receives ([`components/semtech/sx1262` §5.2](../../../../components/semtech/sx1262/README.md)).
Both values are in shipping software and both are reported to work, which means either the
TCXO tolerates a wide supply or `TCXO_OPTIONAL` is masking the difference by retrying
without TCXO. **No module datasheet exists** to settle it (gap **G2**).

**Guidance:** start from **3.0 V**, because that is the vendor's own number for this exact
board. If you are cloning Meshtastic's behaviour, use 1.8 V *with* the optional-retry path.
Do not silently change either to `0`.

## 9. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| LoRa + Wi-Fi/BLE | ✅ different bands, different antennas | sub-GHz SX1262 vs 2.4 GHz ESP32-S3. They share CPU and battery, not spectrum |
| **LoRa + microSD** | ⚠ **shared SPI bus** | G40/G14/G39 are the SD bus too (`SDCARD_CS` 12). Needs chip-select discipline; Meshtastic uses `spiLock` |
| LoRa + GNSS (same Cap) | ✅ | GNSS is UART1; different peripheral entirely |
| LoRa + Grove I²C device | ⚠ | The expander at `0x43` sits on the same bus a Grove sensor joins. Address collisions with `0x43` will break the antenna switch |
| LoRa + keyboard / IMU / audio | ⚠ I²C bus contention only | TCA8418, BMI270 and ES8311 all live on G8/G9 |
| LoRa TX + battery | ⚠ unquantified | +22 dBm through a 5 V→3.3 V buck off a 1750 mAh cell. Vendor gives one aggregate number (163.4 mA at 5 V) with no stated conditions |
| LoRa + deep sleep | ❓ untested | No host power-gate exists; the Cap draws from the host's 5 V rail whenever it is up |

## 10. Debugging

| Symptom | First thing to check |
|---|---|
| `radio.begin()` returns an error | Wrong pin order in `new Module(...)` — it is **NSS, DIO1, RST, BUSY** = 5, 4, 3, 6 |
| Initialises but nothing is heard, nothing gets through | **Antenna switch not set** (expander `0x43`, P0 high) — §3. Then the TCXO voltage — §8 |
| Works at 1 m, dead at 50 m | Wrong-band antenna (868 whip on 915 MHz), or the RP-SMA/SMA adapter is not making contact |
| Radio fine, "GPS not found" | Different subsystem — [`gnss.md` §6](gnss.md) |
| Works in one firmware, not another | A recurring **launcher/state** problem, not the radio: several owners traced 2026-08 breakage to M5Launcher 2.8.0 and fixed it by reflashing an earlier launcher ([r/CardPuter 2026-08-28](https://old.reddit.com/r/CardPuter/comments/1w0gv7y/)) |
| SD card corrupts while the radio is busy | SPI arbitration — §2 |

## 11. Porting checklist — what it takes to add SX1262 LoRa to *other* firmware

Written for the wider project's goal of adding LoRa to e-ink reader firmware
(CrossPoint Reader / FreeInk). Compare with the PaperMono's arrangement in
[`devices/m5stack/papermono/features/lora.md`](../../papermono/features/lora.md), which is
the *same radio module family* wired very differently — reading the two side by side is the
fastest way to see which parts are the chip's and which are the board's.

**Minimum hardware resources an SX1262 needs from a host:**

| Resource | Count | Negotiable? |
|---|---|---|
| SPI (SCK/MOSI/MISO) | 3 | Shareable with other SPI devices if you arbitrate chip-selects |
| Chip select (`NSS`) | 1 | No |
| `BUSY` | 1 | **No.** It is a mandatory handshake, not a status LED. Polling SPI without it loses commands |
| `DIO1` interrupt | 1 | Strongly recommended; polling works but wastes power |
| `NRST` | 1 | Can be omitted (`RADIOLIB_NC`) *only* if something else resets the module — PaperMono routes it through an I²C expander |
| Antenna/RF switch control | 0–1 | **Board-specific.** Cap LoRa-1262 needs one I²C write; PaperMono needs a different expander pin; Cap LoRa868 needs nothing |
| 3.3 V at TX current | — | Budget for +22 dBm; SX1262 `setCurrentLimit()` caps at 140 mA |

**Minimum software:**

1. **RadioLib** — MIT, header-only-ish Arduino/ESP-IDF library, ~1 dependency-free. It is
   what M5Stack, Meshtastic and the PaperMono firmware all use. If your firmware is not
   Arduino, implement a `RadioLibHal` subclass over your SPI/GPIO/delay primitives — that is
   exactly what M5Stack's PaperMono `hal_lora.cpp` does in ~300 lines.
2. Construct `new Module(nss, dio1, rst, busy)` — **in that order**; getting it wrong is the
   most common porting bug.
3. `begin(freq, bw, sf, cr, syncWord, power, preamble, tcxoVoltage, useRegulatorLDO)`.
   `tcxoVoltage` **must** match the module's fitted TCXO (§8) or the radio silently fails.
4. `setDio2AsRfSwitch(true)` if the module uses DIO2 internally. **PaperMono does; the Cap
   examples do not call it** — one more reason not to copy a config across boards.
5. Board-specific: whatever pin turns the external antenna switch on.

**What is *not* portable between these boards, despite the same radio:**

| Aspect | Cap LoRa-1262 | PaperMono |
|---|---|---|
| Reset | host GPIO G3 | I²C expander `M5IOE1` IO10 |
| Antenna switch | I²C expander `PI4IOE5V6408` P0 @ 0x43 | I²C expander `M5IOE1` IO2 |
| Rail enable | none (always on) | `M5PM1` G2 gates `3V3_L2_LoRa` |
| SPI host | shared with microSD | dedicated (display is on a separate host) |
| `setDio2AsRfSwitch` | not called in the vendor example | `true` |
| TCXO | 3.0 V (vendor) / 1.8 V (Meshtastic) | 3.0 V |
| Antenna | external SMA + rubber duck | built-in FPC |

**If you want mesh networking rather than raw packets**, do not write it yourself: the
Meshtastic variant above is 3 small files plus one `variant.cpp`, and the whole
board-support delta for a new board is roughly *that* much work. The expensive part of
Meshtastic is the UI/display/input integration, not the radio.

## 12. Unresolved

- **TCXO voltage** (§8) — vendor 3.0 V vs upstream 1.8 V, unsettled.
- **`SW` (module pin 10) semantics** — TX/RX path select, PA/LNA enable, or connector
  select? Nothing says. Both vendor and upstream code set it HIGH once and never touch it.
- **RF output power at the connector**, insertion loss, and the internal matching network:
  no module datasheet exists.
- **No range, throughput, sensitivity or current measurement** from anyone, vendor or
  community, for this board.
- **LoRaWAN**: never demonstrated on this hardware.

## Applicability

| Field | Value |
|---|---|
| Hardware | Cap **U214**, schematic **V1.1 / 2025-10-29**, on **Cardputer-Adv** (also claimed for CardputerZero) |
| Firmware range | RadioLib ≥ 7.x · Meshtastic ≥ **2.7.20** (antenna-switch fix from **2.7.24**) · M5Unified with `PI4IOE5V6408_Class` |
| Evidence | Pin map: **schematic + vendor pin-map + upstream variant.h, three-way cross-confirmed**. Radio parameters: **read from vendor source**, `executed-success`. TCXO: **conflicting primary sources**. RF performance: **none** |
| Confidence | High on wiring and software configuration; **none on RF performance or on legality in any region** |
| Last verified | **2026-09-04** |
