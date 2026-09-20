# LoRa — M5Stack PaperMono

> **Common guide:** [`guides/lora`](../../../../guides/lora/README.md) holds the device-independent LoRa material — standards, silicon choice, antenna and matching, libraries and debugging.
>
> **Applicability:** the standard approach **applies with deltas**. On this board reset and antenna-switch control run through the M5IOE1 I/O expander, the `3V3_L2_LoRa` rail is enabled by the M5PM1 power-management MCU, **no datasheet exists for the Stamp LoRa-1262 module**, and the vendor firmware selects **LDO regulation**, which roughly doubles receive current.

> **How do I send and receive a LoRa packet?**
> Hardware revision **V0.6.2** (SKU **C153 only** — not fitted on the Lite) ·
> snapshot **2026-09-01** · nothing tested on hardware.

> **Regional band configuration is a documented gap.** One wideband 868–923 MHz SKU, no
> per-region variant, **no module datasheet anywhere**, and **no published certification
> of any kind**. §7 says what that means; the guide is deliberately short there rather
> than inventing regional guidance.

## 1. Capability summary and the hardware path

A plug-in `Stamp-LoRa-1262-mini` module carrying a Semtech SX1262, on its own SPI bus,
with its power rail switched by the [power manager](power-and-sleep.md) and its reset and
antenna switch behind the [I/O expander](io-expander.md).

```
ESP32-S3 ──SPI3_HOST──▶ Stamp-LoRa-1262 (U14, 13-pin) ──▶ FPC antenna
   GPIO38 MOSI, GPIO39 SCK, GPIO40 MISO, GPIO41 NSS
   GPIO21 ◀── BUSY
   GPIO5  ◀── DIO1 / LORA_IRQ
                   ▲ SX_NRST   ◀── M5IOE1 IO10
                   ▲ SX_ANT_SW ◀── M5IOE1 IO2
                   ▲ VIN_3V3   ◀── 3V3_L2_LoRa (SSP7615-33DFR U9), enabled by M5PM1 G2
```

| Element | Part | Record |
|---|---|---|
| Module | M5Stack `Stamp-LoRa-1262-mini`, designator `U14` | [`components/m5stack/stamp-lora-1262`](../../../../components/m5stack/stamp-lora-1262/README.md) |
| Radio | Semtech **SX1262** | (module-internal) |
| Rail enable | **M5PM1 `G2`** (`PYG2_LoRa_EN`) | [`components/m5stack/m5pm1`](../../../../components/m5stack/m5pm1/README.md) |
| Reset / antenna switch | M5IOE1 `IO10` / `IO2` | [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md) |
| Antenna | built-in FPC | vendor spec; no part identified |

> **Bus naming.** The schematic net names say `SPI1` (`G38_SPI1_MOSI` etc.), but the
> firmware opens **`SPI3_HOST`** (`hal_lora.cpp:22`). Both are correct in their own
> namespace — the schematic labels are M5Stack's, `SPI3_HOST` is ESP-IDF's. The e-paper's
> `SPI2` labels happen to coincide with `SPI2_HOST`, which makes the LoRa mismatch easy
> to miss. Recorded because it will confuse anyone reading the two side by side.

## 2. Prerequisites and exact versions

| Item | Value | Note |
|---|---|---|
| **RadioLib** | **7.2.1**, commit `b91c6af112e423dcb14529ade5827802a14e1015` | What the factory firmware pins |
| RadioLib in the published PlatformIO snippet | **unpinned** — `https://github.com/jgromes/RadioLib` | ⚠ pulls `master`, not 7.2.1 |
| M5PM1 / M5IOE1 | 1.0.7 / 1.0.9 | Needed for the rail and reset |
| ESP-IDF | 5.5.1 | |

> The vendor's own build **patches RadioLib to remove `idf_component.yml`** so it builds
> as a plain component rather than a managed one. If you are reproducing factory
> behaviour, use the pinned commit **and** expect that patch.
>
> **Licence note, flagged not confirmed:** RadioLib is LGPL-3.0 upstream while the M5Stack
> demo carrying it is MIT. Not verified in this pass.

There is **no M5Stack-specific LoRa library**. `hal_lora.cpp` is a thin wrapper that
implements a `RadioLibHal` over ESP-IDF SPI/GPIO and hands six pin numbers to RadioLib.

## 3. Resources consumed

| Resource | Value |
|---|---|
| ESP32-S3 GPIO | **six**: GPIO38, 39, 40, 41 (SPI), GPIO21 (`BUSY`), GPIO5 (`DIO1`) |
| SPI host | **`SPI3_HOST`**, **8 MHz** (`LORA_SPI_FREQ_HZ = 8000000`) |
| Series resistor | 22 Ω on SCK (`R34`) |
| Expander pins | `IO10` reset, `IO2` antenna switch |
| M5PM1 pin | `G2`, rail enable |
| Rail | `3V3_L2_LoRa`, an SSP7615-33DFR LDO rated 400 mA |
| Interrupt | GPIO5, `GPIO_INTR_POSEDGE` in the vendor's RadioLibHal |

## 4. Bring-up order matters

The module has a **hard power cut** independent of the SX1262's own sleep modes. Nothing
in the vendor documentation states the ordering explicitly; it follows from the wiring
and is exactly what the factory firmware does (`hal_lora.cpp:299–319`):

1. **M5PM1 `G2` → output high** — power the module.
2. **M5IOE1 `IO2` (antenna switch) → output, push-pull, HIGH.**
3. **M5IOE1 `IO10` (`SX_NRST`) → output, push-pull, LOW → `delay(100)` → HIGH →
   `delay(20)`.**
4. Only then open SPI and call RadioLib.

Skipping step 1 or 3 gives you a radio that appears absent. Both steps require a working
I²C bus.

## 5. The vendor's exact radio configuration

`hal_lora.cpp:32–43` and `:333–344`. `executed-success` on the read; `not-tested`.

| Parameter | Value |
|---|---|
| Frequency | **868.0 MHz** |
| Bandwidth | **62.5 kHz** |
| Spreading factor | **12** |
| Coding rate | **8** (4/8) |
| Sync word | **`0x34`** |
| TX power | **22 dBm** |
| Preamble | 10 symbols |
| **TCXO voltage** | **3.0 V** |
| Regulator | **LDO** (`useRegulatorLDO = true`) |
| Current limit | **140 mA** |
| Max packet | 255 bytes |
| `setDio2AsRfSwitch` | **true** |

```cpp
radio.begin(868.0f, 62.5f, 12, 8, 0x34, 22, 10, 3.0f, true);
radio.setDio2AsRfSwitch(true);
radio.setCurrentLimit(140.0f);
radio.setPacketReceivedAction(loraSetRxFlag);
radio.startReceive();
```

> **This partially resolves an open question in the module record.** The
> [Stamp-LoRa-1262 record §5 G3](../../../../components/m5stack/stamp-lora-1262/README.md)
> records TCXO-vs-XTAL as unknown, and warns that getting it wrong produces a radio that
> initialises and then fails to transmit. The vendor firmware passes
> **`tcxoVoltage = 3.0f`**, which in RadioLib configures `DIO3` as a **3.0 V TCXO
> supply**. So the module almost certainly fits a TCXO on `DIO3`. `inferred` from the
> firmware, `not-tested` — but it is the value to start from, and changing it blindly is
> exactly the mistake the module record warns about.
>
> `setDio2AsRfSwitch(true)` likewise says `DIO2` drives an internal RF switch. That is
> *not* the same signal as `SX_ANT_SW` on M5IOE1 `IO2`, whose semantics remain
> undocumented (module record G4) — the firmware sets it HIGH once and never touches it
> again.

Note this is a **very slow, very robust** configuration: SF12 at 62.5 kHz is on the order
of a few tens of bits per second. It is a range demo, not a throughput default.

## 6. Minimal procedure (`inferred`)

```cpp
// after the bring-up sequence in section 4:
auto hal    = new PaperMonoRadioLibHal(GPIO_NUM_39, GPIO_NUM_40, GPIO_NUM_38);  // sck, miso, mosi
auto module = new Module(hal, GPIO_NUM_41, GPIO_NUM_5, RADIOLIB_NC, GPIO_NUM_21);
auto radio  = new SX1262(module);                        // NSS, DIO1, RST=NC, BUSY

int st = radio->begin(868.0f, 62.5f, 12, 8, 0x34, 22, 10, 3.0f, true);
if (st != RADIOLIB_ERR_NONE) { /* fail */ }
radio->setDio2AsRfSwitch(true);
radio->setCurrentLimit(140.0f);
radio->setPacketReceivedAction(onRx);
radio->startReceive();
```

**`RST` is passed as `RADIOLIB_NC`** — RadioLib never resets the module, because reset is
an expander pin. You must do it yourself (§4).

## 7. Regional bands, certification and legality — the honest position

**This section is short because the evidence is thin, not because the topic is minor.**

| Question | Answer |
|---|---|
| Band the SKU claims | **868 MHz – 923 MHz**, one wideband range |
| Regional variants | **None.** One SKU, one default variant, both products |
| What the firmware uses | **868.0 MHz**, hard-coded — the EU band |
| Regional band plan support | **Not documented anywhere.** No LoRaWAN region table, no channel plan, no duty-cycle handling in any vendor code |
| Certification | **None published.** `/en/certification` returns HTTP 200 with **zero** matches for `PaperMono` and `C153`. No FCC ID, CE, IC, RCM or TELEC/MIC identifier appears on any of the 13 documentation pages, either product page, or either store listing |
| Module datasheet | **Does not exist in any form located.** M5Stack's datasheet list links the *Semtech chip* datasheet, not a module document |

So: RF output power at the connector, antenna gain, the internal matching network, and
the module's supply current are all **unknown**, and **there is no regulatory paperwork to
point at**. A single wideband SKU spanning EU 868, US 915 and JP 920 allocations, with no
per-region variant and no certification, is worth flagging to anyone intending to deploy
the radio rather than experiment with it on a bench.

Meshtastic/MeshCore support was raised as an open question in the largest community
discussion of this board and **was not answered**. No LoRaWAN stack has been demonstrated
on it.

## 8. Limits

| Class | Limit |
|---|---|
| **Silicon (SX1262)** | 255-byte packets; TCXO configuration must match the module or the radio fails silently after apparently initialising |
| **Board** | **LoRa is not fitted on the PaperMono-Lite.** The entire USD 10 price delta is NFC + LoRa |
| **Board** | Reset and antenna switch behind I²C — **no I²C, no LoRa reset** |
| **Board** | Rail enable behind the M5PM1 — **no I²C, no LoRa power** |
| **Board** | Module pins 11–13 carry pad markers but **no printed name, no net label and no drawn no-connect glyph**. Recorded as *unlabelled*, which is not the same as *proven no-connect* |
| **Framework** | RadioLib unpinned in the published config vs 7.2.1 pinned in the firmware |
| **Observed** | **Nothing.** No range, throughput, sensitivity or current measurement exists from anyone |

## 9. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| **LoRa + [Wi-Fi](wifi-and-bluetooth.md)** | ✅ **they do not share a radio** | LoRa is **sub-GHz, 868–923 MHz**, on a separate SX1262 with its own FPC antenna. Wi-Fi/BLE is **2.4 GHz** inside the ESP32-S3. Different bands, different antennas, different peripherals (`SPI3_HOST` vs the internal radio). There is no coexistence scheduling to do. What they *do* share is CPU time and the battery |
| LoRa + [display](epaper-display.md) | ✅ | Separate SPI hosts — `SPI3_HOST` vs `SPI2_HOST` |
| LoRa + [microSD](microsd.md) | ✅ | SD is SDMMC, not SPI |
| LoRa + [NFC](nfc.md) | ✅ RF-wise | 13.56 MHz vs sub-GHz. Both need the shared I²C bus for their enables |
| LoRa TX + [battery](battery-and-charging.md) | ⚠ unquantified | 22 dBm on a 400 mA LDO with a 140 mA current limit set in software. No measurement exists |
| LoRa + [sleep](power-and-sleep.md) | ⚠ | Sheet 1 lists LoRa as an **L2 wake source**, but **no vendor firmware exercises that path**. Untested |
| LoRa + expander interrupts on `IO2`/`IO3` | ❌ | Documented M5IOE1 interrupt exclusion pair — LoRa antenna switch vs e-paper rail |
| LoRa + expander interrupts on `IO10`/`IO14` | ❌ | Same — LoRa reset vs microSD power |

## 10. Debugging

| Symptom | Cause |
|---|---|
| `begin()` returns an error | Rail not enabled (M5PM1 `G2`); or reset never released (M5IOE1 `IO10`); or the bring-up order was wrong (§4) |
| Initialises, then never transmits or receives | **The classic TCXO mismatch.** Use `tcxoVoltage = 3.0f` as the firmware does; do not "simplify" it to 0 |
| No interrupt on RX | GPIO5 `DIO1`; the vendor HAL registers `GPIO_INTR_POSEDGE` and skips registration entirely if the GPIO ISR service is not installed |
| Works, but glacially | SF12 / BW 62.5 kHz is the vendor default (§5). Change it deliberately |
| Different behaviour from the factory demo | The published PlatformIO snippet pulls RadioLib `master`, not 7.2.1 |
| Radio disappears after a sleep cycle | The rail is M5PM1-owned; re-run the whole bring-up |

## 11. Unresolved questions

- **`SX_ANT_SW` semantics.** Whether it selects TX/RX paths, enables a PA/LNA, or switches
  antenna connectors is stated nowhere. The firmware sets it HIGH and forgets it.
- **Module pins 11–13.** Unlabelled.
- **TCXO confirmed only by inference** from the firmware's `3.0f` (§5).
- **No regional band plan, no certification, no module datasheet** (§7).
- Whether LoRa genuinely works as an L2 wake source.


## 12. Software that actually exists — added 2026-09-11

Prior sweeps recorded **"zero LoRa implementations found"**. That was a
search-term artifact: searching `papermono` rather than `lora` surfaces three
working radios immediately.

| Project | Stack | What it does |
|---|---|---|
| **`m5stack/M5PaperMono-UserDemo`** @ `c109910` | ESP-IDF + **RadioLib** | The factory demo. Full TX/RX app in `main/apps/app_lora/`; HAL in `main/hal/hal_lora.cpp` |
| **`canardleteer/papermono-rs`** @ `67ee512` | Rust / Embassy, bare-metal SX1262 | Behind `--features c153`. Includes a **104-slot US915 channel energy sweeper** and a packet sniffer |
| **`osprey74/Nostos`** @ `56acd5e` | Rust | **Receives Meshtastic traffic** — on-air header parse, AES-CTR decrypt, Position protobuf decode |

### `Nostos` is the most interesting of the three

`crates/nostos-meshtastic` implements a *custom* Meshtastic receiver — it is not
Meshtastic firmware. Its radio config differs from the vendor's in every
parameter:

| | Factory demo | Nostos (Meshtastic RX) |
|---|---|---|
| Frequency | 868.0 MHz | **923.000 MHz** |
| Bandwidth | 62.5 kHz | **125 kHz** |
| Spreading factor | SF12 | **SF9** |
| Coding rate | 4/8 | **4/5** |
| Sync word | `0x34` | **`0x3A`** |

That is a second, independently-chosen configuration on this exact hardware —
useful as a cross-check that the bring-up sequence in §4 is not vendor-specific
folklore.

### Meshtastic upstream does **not** support this device

`meshtastic/firmware` has **no PaperMono or M5Paper variant** (code search for
`papermono` in that repo: 0 results). M5Stack devices that *are* supported
include **`m5stack_coreink`** — an ESP32 e-paper device — plus `m5stack_core`,
`cores3`, `cardputer_adv`, `unitc6l` and `stamp-c3`. The single `m5paper` hit is
a URL in a comment in `variants/esp32/m5stack_coreink/variant.h:96`, pointing at
the *old* M5Paper schematic.

**Porting is feasible but not trivial.** Every pin is known and the SX1262 is a
first-class Meshtastic radio — but `SX_NRST`, `SX_ANT_SW` and the rail enable all
sit **behind two I²C chips**, whereas Meshtastic's variant system expects plain
GPIOs. That indirection, not the radio, is the work.

### Partial answer to the `SX_ANT_SW` question (§11)

Still not *documented* anywhere, but the vendor HAL's own comment names the
intent — `hal_lora.cpp:299-313` drives it HIGH during bring-up with the comment
**"engage FPC antenna"**:

```c
ioe1.digitalWriteWithRes(LORA_ANT_SW_IOE1_PIN, HIGH, &ioe_err);  // engage FPC antenna
ioe1.digitalWriteWithRes(LORA_RST_IOE1_PIN,    LOW,  &ioe_err);
ioe1.digitalWriteWithRes(LORA_RST_IOE1_PIN,    HIGH, &ioe_err);  // release reset
```

So it is **an antenna-path enable for the onboard FPC antenna**, set once and
left — consistent with "the firmware sets it HIGH and forgets it". Whether it
additionally selects between TX/RX paths or gates a PA/LNA remains **unknown**;
the comment is the vendor's, not a datasheet, and no module datasheet exists.

`papermono-rs` documents the timings the vendor code leaves implicit:
reset LOW → ant-sw HIGH → rail HIGH → **15 ms settle** → reset HIGH →
**20 ms TCXO/boot settle**.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**, **SKU C153 only**. ❌ Not fitted on C153-LITE |
| Framework range | RadioLib **7.2.1** (pinned) · ESP-IDF 5.5.1 · M5PM1 1.0.7 · M5IOE1 1.0.9 |
| Evidence | Pin map: **schematic + firmware, cross-confirmed**. Radio parameters: **read from vendor source** at cited `file:line`, `executed-success`. TCXO: **`inferred`** from the firmware. Regional/regulatory: **verified negative** |
| Confidence | High on wiring and the vendor's radio config; **none on RF performance or legality in any region** |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md#spi-buses`](../pinouts-and-buses.md#spi-buses) · [`../power-architecture.md`](../power-architecture.md) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md)
- [`wifi-and-bluetooth.md`](wifi-and-bluetooth.md) · [`nfc.md`](nfc.md) · [`io-expander.md`](io-expander.md) · [`power-and-sleep.md`](power-and-sleep.md)
- [`components/m5stack/stamp-lora-1262`](../../../../components/m5stack/stamp-lora-1262/README.md)
- [**`guides/lora`**](../../../../guides/lora/README.md) — the device-independent companion to this page (see the applicability note at the top): SF/BW/CR against airtime and battery, LoRa vs LoRaWAN vs Meshtastic, regional band plans and duty cycle, `BUSY`/TCXO/RF-switch mechanics, and generic failure signatures. ⚠ Its §5.6 finds that **current RadioLib implements all four of Semtech's mandatory errata workarounds** — but that was verified on `master` (7.7.1), **not** on the **7.2.1** pinned here
