# NFC — M5Stack PaperMono

> **Common guide:** [`guides/nfc`](../../../../guides/nfc/README.md) holds the device-independent NFC material — standards, silicon choice, antenna and matching, libraries and debugging.
>
> **Applicability:** the standard approach **applies with deltas**. On this board the chip is power-gated through the M5IOE1 I/O expander, the net named `PYB_RFID_RST` is a **load-switch enable rather than a reset** (the ST25R3916 has no reset pin), the reader sits on the shared system I²C bus at `0x50`, and **one sheet of the NFC front-end schematic was never published**.

> **How do I set up NFC on this device?**
> Hardware revision **V0.6.2** (SKU **C153 only** — not fitted on the Lite) ·
> snapshot **2026-09-01** · nothing tested on hardware.

> **This guide is short on results and says so.** The API surface and the wiring are well
> evidenced. **Which card types have actually been read on a real PaperMono is unknown** —
> no vendor test report, no community report, no measurement. §8.

## 1. Capability summary and the hardware path

An ST NFC reader/writer front end on its own sub-board, on the shared system I²C bus,
with an interrupt line to the ESP32-S3 and its supply enabled through the
[I/O expander](io-expander.md).

```
ST25R3916 (I2C 0x50, NFC sub-board)
   ├─ SDA/SCL ──▶ system I²C bus (GPIO47/48)
   ├─ IRQ ─────▶ ESP32-S3 GPIO6
   ├─ enable ◀── M5IOE1 IO4 (PYB_NFC_EN)
   └─ 3V3_L2 ◀── main board, via J3 (10-pin B2B)
```

| Element | Part | Record |
|---|---|---|
| NFC front end | ST **ST25R3916**, I²C `0x50` | [`components/stmicroelectronics/st25r3916/`](../../../../components/stmicroelectronics/st25r3916/) — **record is written**: the datasheet artifact is held, the write-up is not yet done |
| Power enable | M5IOE1 `IO4` | [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md) |
| Sub-board | `02 Paper Mono NFC.SchDoc`, rev **V0.2**, dated 2026-07-28 | [`../pinouts-and-buses.md`](../pinouts-and-buses.md#board-set--this-is-not-one-pcb) |
| Connector | `J3`, `BTB0.408-10PLBDR-G41` | idem |

Advertised card technologies (vendor specification table):
**ISO14443A, ISO14443B, FeliCa™, ISO15693.**

> ⚠ **Sheet 1 of 2 of the NFC schematic is not published.** The included sheet is
> explicitly numbered `2/2`. **The NFC front-end matching network, antenna and crystal
> details on sheet 1 are undocumented, not absent.** Recorded as
> [`../gaps-and-conflicts.md` G1](../gaps-and-conflicts.md#g1--nfc-schematic-sheet-1-of-2-is-not-published).

## 2. Prerequisites

| Item | Value |
|---|---|
| **M5Unit-NFC** | pinned at **`0.1.0`**, commit `93745b547364f310cd64b5155a870103a7800a5d`, **patched** by the vendor build |
| **M5UnitUnified** | **`0.5.5`**, commit `bf711f37…`, patched |
| M5Utility | `0.1.0` |
| M5IOE1 | 1.0.9, for `IO4` |
| Header | `#include <M5UnitUnifiedNFC.h>` |

> ⚠ **Two vendor pages disagree about `M5UnitUnified`.** The Arduino quick-start page tells
> you to install it; the PlatformIO `lib_deps` on both product pages **omits it entirely**
> while listing `M5Unit-NFC`. The factory firmware needs both. Install both.
>
> Also note the PlatformIO block pins nothing — a library-manager install gives you
> current releases, not the commits the factory firmware was built against.

## 3. Resources consumed

| Resource | Value |
|---|---|
| I²C address | **`0x50`** on the shared bus, at **400 kHz** (`NFC_I2C_FREQ_HZ = 400000`) |
| ESP32-S3 GPIO | **GPIO6** — `IRQ`. The scan app runs with `using_irq = false` and polls |
| Expander pin | `IO4` (`PYB_NFC_EN`) |
| Rail | `3V3_L2` — NFC is powered in state **L2** |
| Task | The factory scan app uses a **16 KB stack** task at priority 4 |

> Schematic sheet 4 annotates `PYB_NFC_EN` as a **"spare GPIO"** while the factory
> firmware uses it as the NFC enable. Likely a stale annotation; unresolved
> ([C8](../gaps-and-conflicts.md#c8--pyb_nfc_en-annotated-spare-gpio)).

## 4. Identity probe and the Pro-vs-Lite discriminator

The firmware confirms the part is present by reading register **`0x7F`** and comparing
against expected type **`0x05`** (`hal_board.cpp:22–23`, used at `:145`).

That probe, together with a write to `IO4`, is **how the firmware tells a PaperMono from a
PaperMono-Lite** (`hal_board.cpp:160–172`). See
[`io-expander.md` §9](io-expander.md#9-the-expander-is-the-pro-vs-lite-discriminator).

**M5GFX cannot make this distinction** — it masks NFC out of its board-detection test
(`M5GFX.cpp:1945`) so both SKUs land on the single enum `board_M5PaperMono`. Only the
application layer can tell.

## 5. Minimal procedure (`inferred`)

Transcribed in shape from `M5PaperMono-UserDemo/main/apps/app_nfc_scan/app_nfc_scan.cpp`.
**Not run on hardware.**

```cpp
#include <M5Unified.h>
#include <M5UnitUnifiedNFC.h>
#include <M5IOE1.h>

m5::unit::UnitUnified s_hub;
m5::unit::UnitNFC     s_nfc;
m5::nfc::NFCLayerA    s_a{s_nfc};      // ISO14443A
m5::nfc::NFCLayerB    s_b{s_nfc};      // ISO14443B
m5::nfc::NFCLayerF    s_f{s_nfc};      // FeliCa
m5::nfc::NFCLayerV    s_v{s_nfc};      // ISO15693

bool nfcBegin() {
  ioe1.pinMode(M5IOE1_PIN_4, OUTPUT);
  ioe1.setDriveMode(M5IOE1_PIN_4, M5IOE1_DRIVE_PUSHPULL);
  m5ioe1_err_t err = M5IOE1_OK;
  ioe1.digitalWriteWithRes(M5IOE1_PIN_4, HIGH, &err);   // power the NFC sub-board
  if (err != M5IOE1_OK) return false;                   // -> this is a Lite

  auto cfg      = s_nfc.config();
  cfg.emulation = false;
  cfg.mode      = m5::nfc::NFC::A;
  cfg.using_irq = false;                                // vendor polls; GPIO6 unused
  s_nfc.config(cfg);

  return s_hub.add(s_nfc, M5.In_I2C) && s_hub.begin();
}

void scanA() {
  s_hub.update();
  std::vector<...> piccs;
  if (s_a.detect(piccs, /*timeout_ms=*/180) && !piccs.empty()) {
    auto& picc = piccs.front();
    Serial.println(picc.uidAsString().c_str());
  }
}
```

Switching technology mid-run, as the vendor app does:

```cpp
s_nfc.disableField();
auto cfg = s_nfc.config(); cfg.emulation = false; cfg.mode = mode; s_nfc.config(cfg);
s_nfc.configureNFCMode(mode);
s_nfc.begin();
s_hub.update();
```

Per-layer detect signatures, exactly as the vendor calls them:

| Layer | Call |
|---|---|
| A | `s_a.detect(piccs, timeout_ms)` |
| B | `s_b.detect(piccs, 0x00, 4, timeout_ms)` |
| F (FeliCa) | `s_f.detect(piccs, m5::nfc::f::TimeSlot::Slot16, timeout_ms)` |
| V (ISO15693) | `s_v.detect(piccs, timeout_ms)` |

## 6. The vendor's scan timings

`app_nfc_scan.cpp:21–28`. Worth copying because they encode the polling rhythm someone
tuned:

| Constant | Value |
|---|---|
| `NFC_A_SCAN_WINDOW_MS` | **3500** — type A gets far the longest window |
| `NFC_OTHER_SCAN_WINDOW_MS` | 900 |
| `NFC_DETECT_TIMEOUT_MS` | 180 |
| `NFC_DETECT_GAP_MS` | 60 |
| `NFC_MODE_STABLE_MS` | 200 |
| `NFC_TOUCH_COOLDOWN_MS` | 300 |

The app cycles through modes, calls `disableField()` between them, and rate-limits UI
updates — which on an e-paper device is not optional. See
[`epaper-display.md` §8](epaper-display.md#8-panel-safety--the-rules-that-are-not-optional).

## 7. Limits

| Class | Limit |
|---|---|
| **Board** | **Not fitted on the PaperMono-Lite.** NFC + LoRa is the entire USD 10 SKU delta |
| **Board** | The NFC sub-board is powered from `3V3_L2` and enabled via I²C. **No I²C, no NFC** |
| **Board** | Sheet 1 of the NFC schematic is unpublished — matching network and antenna undocumented (§1) |
| **Board** | **Certified 2026-09-20 correction.** The 13.56 MHz emitter has its own grant under **FCC ID `2AN3WM5PAPERMONO`** — equipment class **DXX**, Part 15 Low Power Communication Device Transmitter, granted 2026-08-12. Measured field **66.65 dBµV/m at 3 m = −28.55 dBm (0.0014 mW) EIRP**, against a SAR-exclusion threshold of 443 mW — excluded by five orders of magnitude. It is a near-field reader, not an emitter of any consequence at distance. [`../certification.md` §4](../certification.md#4--rf-exposure-and-sar) |
| **Board** | The NFC antenna is a **separate FPC daughterboard** carrying a printed loop and its own reader IC, bonded into the upper part of the rear housing, silkscreened `Paper_Mono_NFC V0.2 M5STACK`. The FCC internal photographs show it clearly; **the reader IC's part number is not legible at 200 ppi** — the ST logo is unmistakable, the `ST25R3916` marking is not confirmed |
| **Framework** | Vendor uses **polling**, `using_irq = false`. The GPIO6 interrupt path is **unexercised by any vendor code** |
| **Framework** | Card emulation is exposed (`cfg.emulation`) but **set false everywhere** in vendor code and never demonstrated |
| **Observed** | **Nothing** (§8) |

## 8. ⚠ What has actually been tested: nothing that we can see

This is the honest state of the evidence, and it is the reason this guide is short:

- **M5Stack advertises ISO14443A, ISO14443B, FeliCa and ISO15693.** That is a
  specification-table claim, `not-tested`.
- The library exposes four layer classes matching those four technologies, and the vendor
  demo cycles through all four. **That the code path exists is not evidence that a card
  was read.**
- **No vendor test report, no card compatibility list, no community report, and no
  hands-on account** mentions reading any specific tag on a PaperMono. Two broad
  independent community passes found one hands-on video (a first look, with an affiliate
  link) and no written review at all.
- The scan-window asymmetry (3500 ms for type A vs 900 ms for the others) is the only
  indirect hint that type A is the primary case, and even that is an inference from a
  constant.

So: **do not assume MIFARE Classic, MIFARE DESFire, NTAG, FeliCa or a specific ISO15693
tag family works until you have tried it.** No read range figure exists either. If you
have hardware, this is the single highest-value thing in this record to go and measure.

## 9. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| NFC + [Wi-Fi](wifi-and-bluetooth.md)/[LoRa](lora.md) | ✅ RF-wise | 13.56 MHz vs 2.4 GHz vs sub-GHz. No spectral interaction |
| **NFC + [charger](battery-and-charging.md) on the shared I²C bus** | ⚠ **the combination to be careful with** | Both are on the **one** I²C bus. NFC polling is chatty — the vendor app runs 180 ms detect calls with 60 ms gaps for seconds at a time — and gating the IP2315 onto that bus is the **one documented bus-stability hazard on this board**. Do not open the charger gate inside an NFC scan window; batch charger reads between scans, and close the gate immediately. If the bus wedges, the documented recovery is a short press of the power button |
| NFC + [touch](touch.md) | ⚠ bandwidth | Same bus, distinct addresses. Touch is latency-sensitive; a long NFC transaction adds jitter |
| NFC + [display](epaper-display.md) | ✅ | Different buses; but rate-limit your UI |
| NFC + [sleep](power-and-sleep.md) | ⚠ | Sheet 1 lists NFC as an L2 wake source; **no vendor firmware exercises it**. Untested |
| NFC + the [expander](io-expander.md) | ⚠ | `IO4` is the enable, and `IO4` is one of only two expander pins the vendor product page omits |

## 10. Debugging

| Symptom | Cause |
|---|---|
| `0x50` absent from an I²C scan | `IO4` not asserted — or you have a **Lite**, which has no NFC at all |
| `digitalWriteWithRes(IO4, …)` errors | Same — that error *is* the Lite detection (§4) |
| Identity probe fails | Read `0x7F`, expect `0x05` |
| No cards detected in any mode | Field disabled, or wrong layer for the card. Try type A first |
| Other I²C devices misbehave during scanning | Bus contention — see §9, especially the charger gate |
| `M5UnitUnified` missing at compile time | The PlatformIO snippet omits it; install it anyway (§2) |

## 11. Unresolved questions

- **Which card types actually work, and at what range** (§8).
- **NFC schematic sheet 1** — antenna, matching, crystal.
- Whether the GPIO6 interrupt path works; nothing uses it.
- Whether card **emulation** works; the flag exists, nothing sets it.
- The `PYB_NFC_EN` "spare GPIO" annotation.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**, **SKU C153 only**. ❌ Not fitted on C153-LITE |
| Framework range | M5Unit-NFC 0.1.0 (pinned, patched) · M5UnitUnified 0.5.5 · M5Unified 0.2.21 · M5IOE1 1.0.9 |
| Evidence | Address, IRQ pin, enable pin, identity probe: **read from vendor source**, `executed-success`. API and timings: **read from the vendor demo**. Card compatibility: **`not-tested` and unreported by anyone** |
| Confidence | High on the wiring and API shape; **zero on real-world tag reading** |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md#i²c-bus--the-one-shared-bus`](../pinouts-and-buses.md#i²c-bus--the-one-shared-bus) · [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md)
- [`io-expander.md`](io-expander.md) · [`battery-and-charging.md`](battery-and-charging.md) · [`lora.md`](lora.md) · [`power-and-sleep.md`](power-and-sleep.md)
- [`components/stmicroelectronics/st25r3916/`](../../../../components/stmicroelectronics/st25r3916/) (stub) · [`components/m5stack/m5ioe1`](../../../../components/m5stack/m5ioe1/README.md)
- [`vendors/m5stack`](../../../../vendors/m5stack/README.md) — the ST25R3916 datasheet exists in **EN and ZH editions** on M5Stack's CDN; only the zh_CN product page links the ZH one
- [**`guides/nfc`**](../../../../guides/nfc/README.md) — the device-independent companion to this page (see the applicability note at the top): the standards landscape, antenna and matching, the operation-byte pattern, software stacks and generic failure signatures
