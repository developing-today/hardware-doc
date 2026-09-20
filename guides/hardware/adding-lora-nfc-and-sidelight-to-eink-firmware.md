# Adding LoRa, NFC and an RGB sidelight to an existing e-ink reader firmware

> **Nothing in this pass was built, compiled, flashed or measured.** No hardware
> was in hand. Every claim below is read out of a record already in this
> repository, and carries that record's evidence label. Where a number would be a
> guess, it says so instead of guessing.
>
> Snapshot **2026-09-07**. Device-independent companions:
> [`guides/lora`](../lora/README.md) · [`guides/nfc`](../nfc/README.md) ·
> [`guides/hardware/e-paper-displays.md`](e-paper-displays.md).

## Evidence labels used throughout

| Label | Meaning here |
|---|---|
| `executed-success` | Someone in this repository read the cited file/API and recorded the result. **Not** "it ran on hardware" |
| `reported-working` | A third party states it works; not reproduced here |
| `inferred` | Derived from wiring, source or arithmetic; not observed |
| `not-tested` | Nobody has tried it, or nobody has published trying it |

---

## 0. The short answer

| Capability | Is there working hardware evidence? | Plugin, or fork? |
|---|---|---|
| **LoRa** | Hardware exists and is fully wired on the PaperMono; the vendor's own factory firmware initialises it. **No third party has ever driven LoRa on that board** | **Firmware change required.** Not reachable from either plugin system |
| **NFC read/write** | **Demonstrated on real hardware by a third party** ([`ciniml/paper_name_plate`](https://github.com/ciniml/paper_name_plate), Rust, 2026-09-06) | **Firmware change required**, but a *small, structured* one |
| **RGB sidelight / frontlight** | Both exist on the PaperMono and are driven by stock firmware. On the Xteink X4 Pro a dual warm/cool frontlight exists. **Neither is an addressable LED string** | **Firmware change required.** Frontlight is not even on a host GPIO |

Every one of the three needs a firmware change. **None of them can be a plugin
under either CrossPoint plugin system**, and §4 shows exactly why — the boundary
is a link-time symbol allow-list that contains no bus, no pin and no filesystem
access. The good news buried in that: the gap between "plugin" and "fork of the
reader" is much narrower than it sounds.

---

## 1. The three things this is grounded in

### 1.1 The M5Stack PaperMono ships LoRa **and** NFC in its stock firmware

This is the load-bearing fact, and it is why the question is answerable at all
rather than speculative. The
[PaperMono](../../devices/m5stack/papermono/README.md) (SKU C153, USD 65) fits an
ST25R3916 NFC front end and a `Stamp-LoRa-1262-mini` (Semtech SX1262) module, and
M5Stack's `M5PaperMono-UserDemo` drives both. The
[PaperMono-Lite](../../devices/m5stack/papermono-lite/README.md) at USD 55 is the
same board with both radios depopulated — **the USD 10 delta is exactly NFC + LoRa
and nothing else.**

What the stock firmware actually does, read from vendor source at cited
`file:line` (`executed-success` on the read, `not-tested` on hardware):

| | LoRa | NFC |
|---|---|---|
| Driver | **RadioLib**, pinned **7.2.1** commit `b91c6af1…`, and **patched** to remove `idf_component.yml` | **`M5Unit-NFC` 0.1.0** commit `93745b54…` + **`M5UnitUnified` 0.5.5**, both **patched** |
| Host glue | `hal_lora.cpp` — a thin `RadioLibHal` over ESP-IDF SPI/GPIO, handing RadioLib six pin numbers | `M5UnitUnified` hub; the app adds `NFCLayerA/B/F/V` objects |
| Bus | **`SPI3_HOST`**, 8 MHz, GPIO38 MOSI / 39 SCK / 40 MISO / 41 NSS | **Shared system I²C**, GPIO47/48 @ 400 kHz, address `0x50` |
| Handshake | `BUSY` GPIO21, `DIO1` GPIO5 (`GPIO_INTR_POSEDGE`) | `IRQ` GPIO6 — **and the vendor app sets `using_irq = false` and polls** |
| Reset | **not on an ESP32 GPIO** — M5IOE1 `IO10`. RadioLib is passed `RADIOLIB_NC` | ST25R3916 **has no reset pin**; `PYB_RFID_RST` is a load-switch enable |
| Power enable | **M5PM1 `G2`** → `3V3_L2_LoRa` rail (SSP7615-33DFR LDO, 400 mA) | **M5IOE1 `IO4`** → NFC sub-board |
| Vendor radio config | 868.0 MHz · BW 62.5 kHz · **SF12** · CR 4/8 · sync `0x34` · **22 dBm** · TCXO **3.0 V** · **LDO regulation** · current limit 140 mA | mode A/B/F/V cycled; identity probe reads register `0x7F`, expects `0x05` |

Two of those rows are the whole shape of the problem:

- **The reset and the power rail are both behind I²C.** No I²C, no LoRa reset. No
  I²C, no LoRa power. No I²C, no NFC at all.
- **The vendor picked LDO regulation**, which on an SX1262 roughly doubles receive
  current — 4.6 mA → 8.8 mA for LoRa at 125 kHz — presumably because the module
  omits the DC-DC inductors.
  ([SX1262 record §5.4](../../components/semtech/sx1262/README.md).)

The bring-up **order** is not optional and is not stated in any vendor document;
it follows from the wiring and is what `hal_lora.cpp:299–319` does:

1. M5PM1 `G2` high — power the module.
2. M5IOE1 `IO2` (antenna switch) → output, push-pull, HIGH.
3. M5IOE1 `IO10` (`SX_NRST`) → LOW → 100 ms → HIGH → 20 ms.
4. *Then* open SPI and call RadioLib.

Skip step 1 or 3 and the radio looks absent.

**NFC is now demonstrated by a third party, LoRa is not.**
[`ciniml/paper_name_plate`](https://github.com/ciniml/paper_name_plate) is
bare-metal `no_std` Rust for this board carrying its own ST25R3916 driver
(`src/st25r3916.rs`, 28,899 B of source), NFC Forum Type 2 Tag emulation
(`src/t2t_emu.rs`, 19,784 B), ISO-DEP and NDEF — plus its own `pm1.rs` and
`ioe1.rs`, because it concluded independently that the FreeInk SDK abstraction is
optional. It lists the SX1262 pins and **explicitly scopes LoRa out**. `⚠ It has
no LICENSE file — all rights reserved. Read it for technique; do not copy.`
Details: [new PaperMono projects, 2026-09](../../software/ecosystems/crosspoint-freeink/new-papermono-projects-2026-09.md).

### 1.2 The M5Stack Caps are the reference implementation, with published pinouts

Two [Cardputer](../../devices/m5stack/cardputer-adv/README.md) expansion boards do
the same jobs as *attachable* modules with schematics in this repository. If you
are designing a new board or reasoning about a port, read these before the
PaperMono, because their wiring is simpler and published.

**[Cap LoRa-1262 (U214), USD 14.50](../../devices/m5stack/cap-lora-1262/README.md)** —
SX1262 in a `Stamp LoRa-1262 Mini` plus an ATGM336H GNSS. Host pin map, verbatim
from the vendor (identical on the `[EOL]` [U201](../../devices/m5stack/cap-lora868/README.md)):

| Cap signal | Cardputer-Adv GPIO |
|---|---|
| `LoRa_NSS` | **G5** |
| `LoRa_RST` | **G3** |
| `LoRa_IRQ` (DIO1) | **G4** |
| `LoRa_BUSY` | **G6** |
| `LoRa_SCK` / `MOSI` / `MISO` | **G40 / G14 / G39** — *shared with the microSD card* |
| `GPS_TX` → host RX / `GPS_RX` ← host TX | **G15 / G13** |
| `SCL` / `SDA` | **G9 / G8** — the host's *internal* bus |

Plus a `PI4IOE5V6408` I/O expander at **`0x43`** whose **P0 drives the RF antenna
switch**. M5Stack states plainly that initialising the radio requires *"set P0 of
the PI4IOE I/O expander to HIGH"*. Omit it and the SX1262 transmits into a
disconnected antenna.

**[Cap CC1101 & NFC (U219), USD 18.95](../../devices/m5stack/cap-cc1101/README.md)** —
a TI CC1101 multi-band sub-GHz transceiver **and** an ST25R3916 NFC front end
**on a shared SPI bus**, behind a host-gated rail, with three antennas in the box.
That is the closest published analogue of "add both radios to an existing device"
that exists anywhere in this repository, and its
[`features/nfc.md` §10](../../devices/m5stack/cap-cc1101/features/nfc.md) and
[`features/sub-ghz.md` §9](../../devices/m5stack/cap-cc1101/features/sub-ghz.md)
are written as portability checklists.

Two ideas from it are worth stealing:

- **Band switching that costs one host GPIO instead of two.** Two SP3T switches
  select one of three matched LC paths to a single antenna port. `RF_SW0` is a host
  GPIO (`G13` on Cardputer-Adv, `G14` on CardputerZero); **`RF_SW1` is the
  CC1101's own `GDO2` pin, set over SPI.** Cost: you cannot select a band before
  the transceiver is talking.
- **The same ST25R3916 appears on both boards with a different host interface** —
  **SPI** on the Cap, **I²C** on the PaperMono. The part is strapped by `I2C_EN`.
  A driver written against one is not a driver against the other at the bus layer,
  though everything above `rfal_rf.h`
  ([`guides/nfc` §6.1](../nfc/README.md#61-rfals-structure-and-the-one-thing-to-know-before-porting-it))
  is portable by construction.

⚠ **The CC1101 cannot do LoRa.** The frequencies overlap so people keep asking.
LoRa is chirp spread spectrum, the patents are Semtech's, TI does not make LoRa
silicon. If you want LoRa on a Cardputer that is the Cap LoRa-1262, and there is
**one Cap slot**.

### 1.3 ⚠ The Xteink X3 carries a passive NFC **tag**, which is not an NFC reader

**Read this before you plan anything around "the X3 has NFC".** It is the
confusion that wastes weeks, and it has already produced one wrong product
identification in this repository's own community sources.

| | **NFC reader/writer** (PaperMono, Cap CC1101) | **Passive NFC tag** (Xteink X3) |
|---|---|---|
| What it is | An active front end — ST25R3916 | An **ISO/IEC 14443A tag**, part number unknown |
| Who energises the field | **The device** | **Someone else's phone** |
| Host bus | I²C `0x50` or SPI | **None. It is on no host bus at all** |
| Firmware can use it | Yes — read, write, emulate | **No. It is invisible to firmware** |
| Appears in a board profile | Yes | **No** — no board profile, no firmware string, no driver, anywhere in the FreeInk SDK |
| Power cost | rail + polling | **Zero. It is not powered** |
| What you can build | tag reading, card emulation, access control | **Nothing in firmware** |

The X3's tag is fitted (two independent sources: the Chinese BOM lists
`***ISO/IEC 14443a NFC Tag`, and Xteink advertised "NFC support" at launch) and
**its function is entirely unknown** — see
[`x3/features/nfc.md`](../../devices/xteink/x3/features/nfc.md), which records four
candidate explanations and endorses none. Resolving it costs five minutes and an
Android phone, and nobody has done it.

**Adding NFC *reading* to an X3 is not a firmware task at all — it is a hardware
modification**, because there is no reader on the board and no free SPI/I²C
front end to attach one to without a redesign. Any plan that starts "the X3
already has NFC" is starting from a false premise.

A third confusion worth killing at the same time: the
[Xteink Nano / "Tong Card"](../../devices/xteink/nano/README.md) is a **separate
product** — a battery-less, NFC-powered four-colour e-paper card that a phone
writes an image to. It is not the X3's tag and it is not a reader either.

---

## 2. What the e-ink refresh does to the power rail

This is the question that gets skipped and then bites during the first field test.
**No measurement of it exists anywhere in this repository**, so what follows is
sourced parts arithmetic, labelled `inferred`, and should be treated as a reason
to instrument rather than as a budget.

Sourced current figures, each cited to its record:

| Load | Figure | Source |
|---|---|---|
| E-paper refresh, 3.97″ 800×480 | **< 40 mW** claimed; panel manual **36 mW typical @ 3.0 V**, **120 mA peak**, 0.003 mW deep sleep | [Waveshare 3.97 record](../../devices/waveshare/esp32-s3-epaper-3.97/README.md) |
| SX1262 TX @ **+22 dBm**, 868/915 MHz | **118 mA** | [SX1262 §5](../../components/semtech/sx1262/README.md) |
| SX1262 TX @ +14 dBm, PA re-matched | **45 mA** — but that needs a *different matching network*, not a software change | idem |
| SX1262 RX, LoRa 125 kHz, **LDO** (what the PaperMono selects) | **8.8 mA** | idem |
| SX1262 RX, LoRa 125 kHz, DC-DC | 4.6 mA | idem |
| SX1262 sleep, config retained | **600 nA** | idem |
| PaperMono LoRa rail | SSP7615-33DFR LDO, **400 mA** rating; firmware sets a **140 mA** software current limit | [PaperMono `features/lora.md` §3](../../devices/m5stack/papermono/features/lora.md) |
| Cap LoRa868 board, GPS sleep / LoRa TX max | **129.72 mA @ 5 V** | [Cap LoRa868 §3](../../devices/m5stack/cap-lora868/README.md) |
| PaperMono frontlight LED current | **~11 mA** `inferred` from the fitted `R29 = 18 Ω`; the schematic's own annotation claiming 15 mA is **stale** | [PaperMono `features/frontlight.md` §5.3](../../devices/m5stack/papermono/features/frontlight.md) |
| PaperMono battery | 1150 mAh | device record |

**What actually matters** (`inferred` throughout):

1. **A panel refresh and a LoRa transmission are each ~120 mA-class events on a
   1150 mAh cell.** On the PaperMono they are on *different rails* — the panel on
   `3V3_L2` behind M5IOE1 `IO3`, the radio on `3V3_L2_LoRa` behind M5PM1 `G2` —
   so the LDOs are not fighting, but the **cell and its ESR are shared**. The
   obvious failure mode is a brown-out when a transmit lands inside a refresh
   window. Nobody has tested this.
2. **Do not transmit during a refresh, as a firmware rule.** An e-paper refresh is
   a fixed-duration waveform the panel must complete; a mid-refresh supply
   disturbance is the classic cause of ghosting and incomplete development. The
   cheap mitigation is to serialise them — the panel is already blocking on `BUSY`,
   so there is a natural place to gate the radio.
3. **The frontlight is the one continuous load.** ~11 mA held for a whole reading
   session dwarfs a duty-cycled radio. It is also the one nobody has measured:
   *"No power figure exists. Nobody has published frontlight current draw or its
   effect on battery life."*
4. **Receive, not transmit, is what kills a mesh node's battery**, and the
   PaperMono's LDO choice doubles it. See
   [`guides/lora` §1.5](../lora/README.md#15-the-battery-consequence-which-is-not-the-one-people-expect).
5. **On the Xteink devices none of this can be computed at all** — only the X3 has
   a published battery capacity (650 mAh), and none of them has a radio beyond the
   SoC's own.

---

## 3. Capability by capability

### 3.1 LoRa

#### Hardware prerequisites

| Requirement | Why | On the PaperMono | On an Xteink |
|---|---|---|---|
| A free SPI host + 4 pins | SX126x is SPI-only | ✅ `SPI3_HOST`, GPIO38/39/40/41 | ❌ **The C3 devices share one SPI bus between the panel and the SD card**; the S3 devices have SDMMC free but no spare CS/IRQ pins documented |
| **`BUSY` line** | **Mandatory handshake**, not optional. Every command must wait for it | ✅ GPIO21 | ❌ |
| **`DIO1` interrupt** | RX-done / TX-done. Polling works but wastes the sleep budget | ✅ GPIO5 | ❌ |
| A reset you can drive | The module needs a hard reset in the bring-up sequence | ⚠ **behind M5IOE1 `IO10`** — RadioLib gets `RADIOLIB_NC` | ❌ |
| A switchable power rail | The radio must be off in sleep or it dominates the budget | ✅ M5PM1 `G2` | ❌ |
| **An antenna and an RF path** | Not optional and not free | ✅ FPC antenna, `SX_ANT_SW` on M5IOE1 `IO2` | ❌ no antenna, no matching, no connector |
| Current headroom at TX | 118 mA @ +22 dBm | ⚠ 400 mA LDO, 140 mA software limit | ❌ unknown battery |

**On any Xteink device this is a hardware project, not a firmware project.** There
is no radio, no antenna, no RF path, no free interrupt line and — on the C3
devices — not even a spare SPI bus. Do not let the "add LoRa to my e-reader"
framing hide that.

#### Driver options

| Option | Licence | Footprint | RTOS assumptions | SoCs | Verdict |
|---|---|---|---|---|---|
| **RadioLib** `jgromes/RadioLib` | **MIT** (declared on `master`; ⚠ an older note in this repo said LGPL-3.0 — [unresolved discrepancy](../lora/README.md#72--pinning-is-not-optional-and-nobody-does-it-the-same-way), and the licence of the *pinned 7.2.1 tree* was never checked) | Not measured. The porting surface is two headers — `Hal.h`, `Module.h` | **None.** Blocking API; you supply a `RadioLibHal` over your own SPI/GPIO | Anything with SPI + 4 GPIO. Arduino **and** ESP-IDF | ⭐ **The default.** It is what M5Stack's own PaperMono firmware uses, at 7.2.1, and it implements **all four** of Semtech's mandatory SX126x errata workarounds |
| Semtech **`sx126x_driver`** / LoRaMac-node | `NOASSERTION` | not measured | none, but LoRaMac-node's timing assumptions are strict | any | The authoritative reference and the certification lineage. Heavy. Last push 2024-07-03 |
| Semtech **LoRa Basics Modem** (`SWL2001`) | BSD-3-Clause-Clear | not measured | own scheduler | any | The live Semtech stack; the successor to LoRaMac-node |
| Semtech **`lr20xx_driver`** (inside **USP**) | BSD-3-Clause-Clear | not measured | none | LR2021/22/12, with claimed back-compat to SX126x/LR11xx | ⚠ **Explicitly pre-production**: *"not intended for production use."* Only relevant if you fit an [LR2021](../../components/semtech/lr2021/README.md) |
| **Meshtastic** (whole stack) | **GPL-3.0** | A complete application, not a library | FreeRTOS + its own scheduler | many | Off-grid messaging out of the box. ⚠ **GPL-3.0 will infect an MIT reader firmware.** This is the licence decision, not a technical one |
| Raw SPI | — | smallest | none | any | Feasible — the command interface is small — but §5.6 of the LoRa guide lists exactly the four errata workarounds a hand-rolled driver silently omits |

**Pin the driver.** M5Stack's own published PlatformIO snippet pins nothing and
pulls `master`; its shipped firmware pins 7.2.1 *and patches it*. Meshtastic pins a
raw commit archive. Building from the documentation does not reproduce the shipped
firmware.

#### Flash and RAM cost

**`inferred`, and weakly — nothing here was measured.** What is actually known:

- RadioLib is 409 files, but a build links only `src/modules/SX126x/` plus
  `Module`/`Hal`. **No size for that subset was measured by anyone in this
  repository.**
- The upstream CrossPoint project's stated current focus is *"DRAM/heap footprint
  (the C3 sets the ceiling), then flash footprint"* — i.e. the memory budget is
  already the binding constraint on the ecosystem's tightest target.
- The realistic added cost is a driver plus a protocol plus a UI, and on a
  **C3 with no PSRAM** the UI is likely to dominate.

**Anyone who needs a real number should build `[env:papermono]` twice, with and
without the radio, and diff the `pio run` size report.** That is a ten-minute job
that nobody has done, and it would replace this whole paragraph.

#### Plugin, or fork?

**Firmware change required.** See §4 — LoRa needs SPI and expander-controlled
enables, and neither is on the plugin ABI.

### 3.2 NFC read/write

#### Hardware prerequisites

| Requirement | Why | PaperMono | Cap CC1101 |
|---|---|---|---|
| A free I²C **or** SPI attachment | The ST25R3916 is strapped by `I2C_EN` to either | ✅ I²C `0x50` @ 400 kHz on the **shared** system bus | ✅ SPI, shared with the CC1101 |
| An **IRQ line** | The chip signals through a single IRQ; the transaction shape is IRQ-driven | ⚠ GPIO6 exists and **no vendor code uses it** — the app polls | present |
| A power enable | The front end idles expensively; you want it off | ✅ M5IOE1 `IO4` | host-gated rail |
| **A tuned antenna** | An NFC reader is *a tuned transformer, not a transmitter* | ⚠ present — but **schematic sheet 1 of 2, containing the matching network, antenna and crystal, is unpublished** | ✅ full differential match + EMC filter on the schematic |
| A 27.12 MHz reference | 13.56 MHz carrier = 27.12/2 | on the unpublished sheet | ✅ `Y1`, C19/C20 = 6.0 pF |
| Current headroom | field generation is bursty | no figure published | vendor: **96 mA** for CC1101 continuous TX *and* NFC continuously reading; **140.87 µA** with both asleep |

**The antenna is the hard part and it is not a software problem.** A correct
driver on a badly matched antenna reads nothing and looks exactly like a driver
bug. RFAL even ships **`rfal_rfst25r3916_analogConfigTbl.h` — analog register
settings per technology, per bit rate, per direction — matched to a reference
antenna**, so a different antenna may need a different table. See
[`guides/nfc` §4](../nfc/README.md#4-antenna-and-matching--the-part-people-get-wrong).

#### Driver options

| Option | Licence | Footprint | RTOS assumptions | Silicon | Verdict |
|---|---|---|---|---|---|
| **ST RFAL** (`stm32duino/NFC-RFAL` 2.0.2 + `stm32duino/ST25R3916` 2.1.0) | `NOASSERTION` on the stm32duino packaging | not measured; full stack RF → technology layers → ISO-DEP/NFC-DEP → tag types → NDEF | none inherent; needs a timer and a bus layer | **ST25R only** | ⭐ **The reference implementation**, and the only 2026-maintained line with a vendor behind it. **Porting = implementing `st25r3916_com.cpp` + `st25r3916_timer.cpp` + interrupts.** Everything above `rfal_rf.h` is portable by construction |
| **`M5Unit-NFC`** | — | not measured; reaches *higher* than RFAL (Crypto1, AES, DESFire helpers, ISO-DEP, NDEF, APDU) | M5UnitUnified hub | ST25R3916, **SPI and I²C** | What the PaperMono actually ships. ⚠ It is **not** an RFAL wrapper — 301 entries in the pinned tree, **no ST source, no ST licence header**. Correspondingly less provenance |
| **PN532** (`adafruit/Adafruit-PN532`, `elechouse/PN532`) | `NOASSERTION` / none declared | small | none | PN532 | Only if you are *choosing* the front end. ⚠ **No ISO 15693** — it will never read an ICODE tag |
| **MFRC522 / "RC522"** (`miguelbalboa/rfid`) | Unlicense | smallest | none | MFRC522 | ⚠ **Frozen** — *"development by owner miguelbalboa has ended"*, badge `no/2019`. **Type A only.** Successor: `OSSLibraries/Arduino_MFRC522v2`, LGPL-2.1 |
| PN5180 (`ATrappmann/PN5180-Library`) | LGPL-2.1 | — | none | PN5180 | ⚠ **archived**, last push 2022-06 |
| A hand-written driver | yours | `paper_name_plate`: **28.9 KB of Rust source** for the ST25R3916 + **19.8 KB** for Type-2 tag emulation | `no_std`, blocking | ST25R3916 | **Proven on this exact board.** Those are *source* sizes, not compiled footprint |

**The selection axis is which technologies you must support, not price.** An RC522
that cannot see an ISO 15693 tag is not cheap, it is wrong.

#### ⚠ What has actually been read on a PaperMono: nothing that anyone published

M5Stack advertises ISO14443A, ISO14443B, FeliCa and ISO15693. The library exposes
four matching layer classes and the demo cycles all four. **That the code path
exists is not evidence that a card was read.** No vendor test report, no
compatibility list, no community report and no read-range figure exists. The only
indirect hint is the scan-window asymmetry (3500 ms for type A vs 900 ms for the
others), and that is an inference from a constant. `not-tested`.

#### Flash and RAM cost

`inferred`. RFAL is a full protocol stack and is the larger of the two realistic
options; `M5Unit-NFC` goes further up the stack still (Crypto1, DESFire). The
vendor's own scan app runs in a **16 KB stack task at priority 4**, which is the
only concrete resource figure anyone publishes. Nothing else was measured.

#### Plugin, or fork?

**Firmware change required — but the smallest of the three.** NFC needs one I²C
transfer service, one expander pin and one IRQ. §4.4 argues this is the capability
worth exporting as a *capability service* rather than as raw bus access.

### 3.3 RGB frontlight / sidelight

⚠ **Terminology first, because three different things get called this.**

| Thing | What it is | On which device |
|---|---|---|
| **Frontlight** | An LED string edge-lit into the e-paper stack so you can read in the dark. **Not** RGB — warm/cool at best | PaperMono (white, AW9967 boost, 15 V rail) · Xteink X4 Pro (**dual warm/cool**) · ZeroWriter Fold (claimed, 10 levels) |
| **RGB status indicator** | A single side-mounted RGB LED that shows state | PaperMono (`RS-C1415MBAR`) |
| **Addressable RGB string** (WS2812 &c.) | A chain of self-clocked smart LEDs | **No e-ink device in this repository has one.** The Cardputers and the Unit C6L do |

If the goal is "a coloured glow along the edge of my reader", that is the third
row, and **nothing in this repository does it today** — you are adding a part, not
enabling one.

#### Hardware prerequisites

| Requirement | Frontlight (PaperMono) | RGB indicator (PaperMono) | Addressable string (hypothetical) |
|---|---|---|---|
| Host GPIO | **none — costs you zero host pins** | **none** | **one**, and it must reach RMT or an equivalent |
| Control path | M5PM1 `G3` → **PWM0** → AW9967 boost → 15 V rail | red = M5PM1 `LED_EN_PP`; green = M5IOE1 `IO8` PWM2; blue = M5IOE1 `IO9` PWM1 | direct |
| Power state | **L3B only.** There is no way to light it from L0/L1/L2 | red survives on the M5PM1; **green/blue die with L3B** | rail-dependent |
| Current | **~11 mA** `inferred` from `R29 = 18 Ω` | not published | ~20 mA per LED at full white, ×N |
| Timing | 5 kHz PWM (see below) | 5 kHz | **~800 kbit/s self-clocked, tight enough that bit-banging is unreliable under interrupts** |

#### Three things that will surprise you on the PaperMono

All three are software or documentation issues, fixable without touching the board:

1. **The brightness curve is squared.** `M5GFX.cpp:849` does
   `br = brightness * brightness`. `setBrightness(128)` is roughly a **quarter** of
   full output, not half. A linear UI slider is lying to the user. A commented-out
   linear write sits directly above it at `:847`.
2. **The PWM frequency is below the driver's rated range.** M5GFX programs 5 kHz;
   the AW9967 datasheet specifies **10–100 kHz**. A 5 kHz square wave into an
   inductor-based boost converter is inside the audible band. Rewriting registers
   `0x34`/`0x35` to 20–50 kHz after `M5.begin()` is a one-line change. **Nobody has
   reported whether the board audibly whines.**
3. **The red die has no PWM at all** — it is on `LED_EN_PP`, which is not a PWM
   output. This is a **board** limit and cannot be worked around. Any colour needing
   partial red — orange, pink, warm white, most pastels — is unreachable. M5Unified
   is more limited still: it writes blue as a *binary* level, so through `M5.Led`
   you get red on/off × blue on/off × green graded. The factory firmware PWMs both
   green and blue by driving M5IOE1 directly, and **nothing documents why M5Unified
   does not.**

⚠ **`PYG3` is the most dangerous token in the PaperMono's documentation.** On the
**M5PM1** it is the frontlight PWM net. On the **M5IOE1** it is the **e-paper 3.3 V
rail enable**. Write to the wrong one and you cut the display's power, with no
error reported. Read
[`pin-naming-and-the-pyg-ambiguity.md`](../../devices/m5stack/papermono/pin-naming-and-the-pyg-ambiguity.md)
before touching either.

#### Driver options for an addressable string

| Option | Licence | Footprint | RTOS assumptions | SoCs | Verdict |
|---|---|---|---|---|---|
| **ESP-IDF `led_strip`** | Apache-2.0 | small | ESP-IDF | ESP32 family | The idiomatic ESP-IDF answer. Uses RMT or SPI backend |
| **RMT directly** | (IDF) | smallest | ESP-IDF | ESP32 family | Full control. Note the **ESP32-S3 has 4 TX + 4 RX RMT channels, fixed, sharing a 384×32-bit RAM** — the RX half is *not* repurposable, so more than four simultaneous strings needs SPI, I2S/LCD or PARLIO. The plain ESP32 has 8 flexible channels |
| **FastLED** | MIT | larger — it carries colour maths, palettes and effects | none | wide | Good if you want the animation library. Overkill for a status indicator |

⚠ **On an ESP32-S3 the GDMA pool is already crowded.** SPI2, SPI3, I2S0, I2S1,
SDMMC, AES, SHA, UHCI, RMT ch3/ch7 and LCD_CAM all draw from ten shared channels; a
design running QSPI display + I2S audio + SD concurrently is already using six.
`ESP_ERR_NOT_FOUND` from a driver's DMA init is the symptom of exhaustion.

#### One real-world lesson from the Cardputers, worth importing

The Cardputer v1.1 and ADV put the WS2812's supply on **`BL_3V3`**, the *switched
backlight rail*, where the v1.0 had it on always-on `VDD_3V3`. Consequence, in
M5Stack's own words: *"when the LCD backlight brightness is below 100%, RGB will
not be powered properly."* **PWM-dimming the display browns out the indicator.**
That is a regression introduced to buy lower sleep current, and it is exactly the
mistake to avoid when adding an LED to a device whose frontlight you also intend
to dim.

#### Flash and RAM cost

`inferred`, small in all three cases — an LED driver is a handful of kilobytes.
The cost of an addressable string is **RMT channels and DMA**, not flash.

#### Plugin, or fork?

**Firmware change required.** GPIO, ADC, PWM and LEDC are all absent from the
plugin ABI (§4), and on the PaperMono the frontlight is not on a host GPIO at all —
it is two I²C writes to a power-management MCU.

---

## 4. The crux: what the plugin surface can and cannot reach

**This is the section to read if you read only one.** The authoritative document is
[`software/applications/crosspoint-reader/plugins/README.md`](../../software/applications/crosspoint-reader/plugins/README.md),
and its central finding is that **there is no single "CrossPoint plugin system" —
there are two, of completely different kinds**, and confusing them produces wrong
answers.

| System | Where code runs | Can it reach GPIO / I²C / SPI? | Enforcement |
|---|---|---|---|
| **Upstream CrossPoint** (roadmap, unmerged branches) | **Browser only** — JavaScript + JSON manifests | **No.** No code executes on the MCU at all | Absolute. There is nothing to work with |
| **`mekhontsev` fork** — native SD plugins | **On the MCU** — native C++ ELF modules loaded from `/plugins` against a versioned host ABI (v3) | **No** — but only because the host symbol allow-list omits them | **Hard: the link fails** |
| **Firmware source** (any fork) | on the MCU | **Yes.** `#include <Wire.h>` and go | **None** |

### 4.1 The allow-list, read at source

`mekhontsev/crosspoint-reader:main/src/plugins/PluginHostSymbols.inc` — 81 lines,
5,201 bytes — was **read directly** on 2026-09-04 (`executed-success`). Census:

| Category | In the allow-list? |
|---|---|
| **I²C** | **absent** |
| **SPI** | **absent** |
| **GPIO** (`pinMode`, `digitalWrite`) | **absent** |
| **ADC / PWM / LEDC** | **absent** |
| **Wi-Fi** | **absent** |
| **Storage / file** | **absent** |
| BLE (`ble_terminal::*`) | **present, 15 symbols** |

What *is* exported: `logPrintf`; `GfxRenderer` (fonts, clear, text width, buffer);
`UITheme` centred/wrapped text; `Activity` lifecycle; `I18n::getInstance`;
`EspClass::getFreeHeap` / `getFreePsram`; the `ble_terminal` transport.

**A plugin gets UI, input, BLE, i18n and heap introspection — and nothing that
touches a bus, a pin or a filesystem.** That is not a documentation gap; it is the
contract, in the file, and the build enforces it.

### 4.2 Therefore, per capability

| Capability | Upstream JS plugin | Native ELF plugin | Firmware source |
|---|---|---|---|
| **LoRa** | ❌ impossible — no MCU execution | ❌ needs SPI + expander enables → **link-time failure by design** | ✅ |
| **NFC read/write** | ❌ impossible | ❌ needs I²C + expander enable | ✅ **demonstrated** by `paper_name_plate` |
| **RGB sidelight** | ❌ impossible | ❌ needs GPIO/RMT, or I²C for the PaperMono's LED | ✅ |
| A *UI* for any of the above | ⚠ partial — a web page talking to the firmware's HTTP server | ✅ | ✅ |

### 4.3 But the gap is smaller than "fork the reader"

The native-plugin documentation states the escape hatch itself: *"When a genuinely
reusable host service is missing, add the smallest stable entry point to the
firmware ABI, add it to the allow-list, and increment the ABI if the change is
incompatible."*

So the honest verdict is **a firmware change is required, but a small, structured
one** — an `i2cTransfer` / `spiTransfer` host service plus expander-pin control,
added to `PluginHostSymbols.inc` with an ABI bump. The radio driver itself
(RadioLib, an ST25R3916 stack) could then live entirely in the plugin.

Two caveats before treating that as a plan:

- **The native plugin ABI is Xteink X4 Pro-only today.** The PaperMono is not a
  target of that fork, and its peripherals sit behind an M5IOE1 expander and an
  M5PM1 power manager the fork has never seen. The port comes first.
- **Exporting raw bus access weakens the containment story.** The plugin host is
  explicitly *not* a sandbox — *"a bad plugin can crash and restart the reader"* —
  and a plugin that can drive I²C can wedge the bus that the RTC, touch, IMU,
  expander and power manager all share. The IP2315 charger on that bus already has
  a documented wedge failure mode.

### 4.4 The design recommendation

**Export *capability* services, not raw buses.** "Read an NFC tag", "send a LoRa
packet", "set the indicator colour" — keeping bus arbitration inside the firmware
where it belongs. That is a firmware feature with a plugin-facing API, which is
arguably the right architecture anyway, and it is the only version that survives
the shared-I²C-bus hazard.

### 4.5 And note: the *SDK* boundary is not a barrier at all

Do not confuse the plugin boundary with the FreeInk SDK boundary. **Firmware source
can call `Wire`, `SPI` and RadioLib directly, and CrossInk already does exactly
this for ESP-NOW** — `NearbyBookPositionSyncActivity.cpp` and
`NearbyStatsSyncActivity.cpp` `#include <esp_now.h>` and call `esp_now_init()`
straight from an Activity, with no `FREEINK_CAP_ESPNOW`, no SDK manager and no
board-profile field. The abstraction was simply bypassed, and it shipped.

The SDK *does* already carry `M5Ioe1.h` (160 lines) and `M5Pm1.h` (213 lines) with
full register maps and PaperMono-aware bus init. **What is missing is four pin
constants**, and they are precisely the radio pins:

| Expander pin | Net | Function | In the SDK? |
|---|---|---|---|
| M5IOE1 `IO2` | `PYB_LoRa_ANT_SW` | LoRa antenna switch | **no** |
| M5IOE1 `IO4` | `PYB_NFC_EN` | **NFC power enable** | **no** |
| M5IOE1 `IO10` | `PYB_LoRa_RST` | **LoRa reset** | **no** |
| M5PM1 `G2` | `PYG2_LoRa_EN` | **LoRa 3V3 rail** | **no** |

⚠ Bit positions for those masks are **`inferred`** from the device record's pin
table (IO*n* → bit *n*−1), not read from a datasheet. Verify against the schematic
before use. Independent corroboration that the three expander assignments are
right comes from `paper_name_plate`, which derived them from its own reading of the
hardware and matched exactly.

---

## 5. Difficulty and conflict-risk, per capability per target firmware

Ratings are **`inferred`** — no port was attempted. The reasoning is shown so you
can disagree with it.

### 5.1 CrossPoint Reader (MIT, upstream, ★7,538)

| Capability | Difficulty | Conflict risk | Reasoning |
|---|---|---|---|
| **LoRa** | **High** | **Medium** | Driver work is easy (RadioLib, a `RadioLibHal`, six pin numbers). The hard parts are: upstream's `SCOPE.md` says the project is *"a dedicated e-reader"* and is explicitly not kitchen-sink, so this is out of scope by policy; the C3 sets a **DRAM/heap ceiling** that upstream is actively trying to reduce; and any UI lands in files upstream develops. Conflict risk is *medium* not *high* only because a radio Activity is a new file |
| **NFC** | **Medium** | **Low** | Smallest hardware surface: one I²C address, one enable, one IRQ. `paper_name_plate` proves the chip works. Same scope objection applies |
| **RGB sidelight** | **Low** | **Medium** | Trivially small code. But the frontlight already has an `ActivityManager` gesture and a `Frontlight.present()` guard, so a second light source lands in files upstream touches |

**Upstream will probably not take any of these**, and its acceptance test says so
politely: *"Is another popular CrossPoint fork already solving this well? If yes,
defer to that fork."* Upstream deliberately delegates non-core features to its own
fork network. That is a feature of the ecosystem's design, not an obstacle.

### 5.2 FreeInk SDK (MIT, the framework beneath CrossPoint)

| Capability | Difficulty | Conflict risk | Reasoning |
|---|---|---|---|
| **LoRa** | **High** | **Low** | Doing it *properly* means new board-profile struct fields (there is **nowhere to put SPI radio pins today** — grepping the SDK for GPIO 38/39/40/41/21/5 returns nothing), a `LoRaManager` peer to `Rtc`/`Imu`, and a `FREEINK_CAP_LORA` gate. Weeks, plus review. **But there is a real argument for it**: the SDK already carries `T5S3_LORA_CS/IRQ/RST/BUSY` for the LilyGO T5S3, so a *second* LoRa board exists to justify the abstraction |
| **NFC** | **Medium** | **Low** | Same shape, smaller. `FREEINK_CAP_NFC` |
| **RGB sidelight** | **Low** | **Low** | The SDK already has an LED manager and capability gates; `PIN_LED_GREEN (IO8)` / `PIN_LED_BLUE (IO9)` are already defined for the PaperMono |
| **The four missing pin constants** | **Trivial** | **Very low** | Four `constexpr uint16_t` masks, one `GPIO2` constant, extend `OUTPUT_MASK`. This is the single highest-value small change available |

⚠ **The SDK has no CI validation for device ports**, so a port can break without
its own tests noticing. And **forks pin different SDK commits**, so a fork's
behaviour can differ from upstream's *without a single line of fork-owned code
differing*.

Also recorded for whoever picks this up: **the SDK declares `ImuType::None` for
the PaperMono despite a BMI270 being fitted and wired.** Whether that is
deliberate or simply unported is **not established**.

### 5.3 CrossPlay (MIT, `ma-r-s/crossplay`, ★15/17)

| Capability | Difficulty | Conflict risk | Reasoning |
|---|---|---|---|
| **LoRa** | **Medium** | **Very low** | CrossPlay's quarantine pattern — everything new lives in `src/apps_local/`, `assets_local/`, `host-tests/`, paths that **do not exist upstream** — means a radio app is a new-file addition that cannot conflict. Its fork is ~90 % new files with about a dozen small, mostly append-only seams |
| **NFC** | **Medium** | **Very low** | idem |
| **RGB sidelight** | **Low** | **Low** | idem, though it already touches `ActivityManager.cpp` for the frontlight gesture |
| **Any of them, as an upstreamable change** | **High** | — | CrossPlay's own `LOCAL_SCOPE.md` says *"anything that makes reading better belongs upstream, so send it there"* — a radio is not that |

⚠ **CrossPlay's PaperMono support is unverified.** The `papermono` envs are in
`platformio.ini`, **absent from `LOCAL_SCOPE.md`**, and nobody has reported running
it on that board. Do not start here assuming the target works.

### 5.4 Summary matrix

| | CrossPoint Reader | FreeInk SDK | CrossPlay |
|---|---|---|---|
| **LoRa** | High / Medium — **blocked by scope policy** | High / Low — *the right home, eventually* | Medium / **Very low** — ⭐ **start here** |
| **NFC** | Medium / Low | Medium / Low | Medium / **Very low** |
| **RGB sidelight** | Low / Medium | **Low / Low** — ⭐ | Low / Low |

---

## 6. The order of work, if you are actually going to do this

`inferred` — a plan, not a report.

1. **Prototype in a fork, hardcoding pins in an Activity.** Exactly as CrossInk
   hardcodes its ESP-NOW setup. This answers the only question that matters — does
   the hardware work, are the rails right, does the antenna switch behave — without
   committing to an API design. **Effort: days.**
2. **Start from upstream CrossPoint, not CrossInk.** Upstream already has
   `[env:papermono]` and pins an SDK commit containing PaperMono support. CrossInk
   would cost a **136-commit SDK bump plus a 294-commit merge into 224 modified
   `lib/` files**, for no benefit, and it has no PaperMono support at all.
3. **Do NFC before LoRa.** Smaller hardware surface, a working third-party
   implementation to compare against, no antenna design, no regional legality
   question, and the failure modes are well characterised.
4. **Measure the two things nobody has measured** while you have it on a bench:
   frontlight current, and what a LoRa transmit does to a panel refresh. Both are
   cheap and both are currently blank in this repository.
5. **Then upstream to the SDK if it proves out** — the four pin constants first,
   then `FREEINK_CAP_LORA` / `FREEINK_CAP_NFC` and a manager, using the LilyGO
   T5S3's existing LoRa pins as the second board that justifies the abstraction.
   **Effort: weeks, plus review.**
6. **Only then think about the plugin ABI**, and export capability services rather
   than raw buses (§4.4).

⚠ **Regional band configuration becomes your legal responsibility the moment you
transmit.** The PaperMono, the Cap LoRa-1262 and the Cap CC1101 are all **single
wideband SKUs spanning EU 868, US 915 and JP 920 allocations with no published
certification of any kind**, and there is **no module datasheet for the
`Stamp-LoRa-1262` in any form located** — so RF output at the connector, antenna
gain and the internal matching network are all unknown. See
[`guides/lora` §3](../lora/README.md#3-regional-band-plans-and-duty-cycle).

---

## 7. Evidence boundary

- **Nothing was built, compiled, flashed, transmitted or measured in this pass.**
- Every "vendor firmware does X" claim is `executed-success` **on the read of the
  source**, and `not-tested` on hardware.
- Every flash/RAM figure is `inferred` or explicitly absent. **No binary size for
  any of these capabilities exists anywhere in this repository.**
- Every current figure is a datasheet or vendor number under conditions that are
  often unstated. The one board-level state-resolved table that exists
  (Cap LoRa868) is for a *different board* at a *different TX power*.
- **NFC on the PaperMono is `reported-working` by exactly one third party**
  (`paper_name_plate`); **LoRa on the PaperMono is `not-tested` by anyone,
  anywhere.**
- The plugin ABI census is `executed-success` — the file was read — but **no plugin
  was built and the ABI-v3 contract is untested here.**
- The M5IOE1 bit positions in §4.5 are **derived, not read from a datasheet**.

## Related

- [`guides/lora`](../lora/README.md) · [`guides/nfc`](../nfc/README.md) · [`guides/hardware/e-paper-displays.md`](e-paper-displays.md)
- [PaperMono LoRa](../../devices/m5stack/papermono/features/lora.md) · [NFC](../../devices/m5stack/papermono/features/nfc.md) · [frontlight](../../devices/m5stack/papermono/features/frontlight.md) · [buttons and RGB LED](../../devices/m5stack/papermono/features/buttons-and-rgb-led.md) · [I/O expander](../../devices/m5stack/papermono/features/io-expander.md) · [power and sleep](../../devices/m5stack/papermono/features/power-and-sleep.md)
- [Cap LoRa-1262](../../devices/m5stack/cap-lora-1262/README.md) · [Cap CC1101 & NFC](../../devices/m5stack/cap-cc1101/README.md) · [Cap LoRa868](../../devices/m5stack/cap-lora868/README.md)
- [Xteink X3 NFC tag](../../devices/xteink/x3/features/nfc.md) — **the thing that is not a reader** · [Xteink Nano](../../devices/xteink/nano/README.md)
- [Radios on the PaperMono](../../software/ecosystems/crosspoint-freeink/radios-on-papermono.md) — the feasibility assessment this guide generalises
- [CrossPoint plugin systems](../../software/applications/crosspoint-reader/plugins/README.md) — **the plugin ABI, read at source**
- [CrossPoint Reader](../../software/applications/crosspoint-reader/README.md) · [FreeInk SDK](../../software/frameworks/freeink-sdk/README.md) · [CrossPlay](../../software/applications/crossplay/README.md) · [fork network](../../software/ecosystems/crosspoint-freeink/fork-network.md)
- [Xteink firmware ecosystem](../../devices/xteink/firmware-ecosystem.md) — which firmware supports which board, and what a new board must provide
- [Components: SX1262](../../components/semtech/sx1262/README.md) · [LR2021](../../components/semtech/lr2021/README.md) · [ST25R3916](../../components/stmicroelectronics/st25r3916/README.md) · [CC1101](../../components/texas-instruments/cc1101/README.md) · [AW9967](../../components/awinic/aw9967/README.md) · [WS2812](../../components/worldsemi/ws2812/README.md) · [M5IOE1](../../components/m5stack/m5ioe1/README.md) · [M5PM1](../../components/m5stack/m5pm1/README.md)
