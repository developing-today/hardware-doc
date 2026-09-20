# LR2021 — ecosystem, software support and community

Companion to [`README.md`](README.md). Everything here is dated and attributed. Community reports
carry an explicit evidence class; nothing on this page is authoritative about the silicon.

**Evidence classes used below**, per the repository convention:

| Label | Meaning |
|---|---|
| **firsthand-measurement** | The poster measured something and says how |
| **firsthand-ownership** | The poster has the hardware and reports use, without measurement |
| **informed-interpretation** | Reading of a document or source by someone who plainly understands it |
| **hearsay** | Repeating something heard elsewhere |
| **vendor claim** | A vendor asserting something about its own product |

Anecdotes establish that an experience occurred, not how common it is. The sample here is
**25 Reddit threads matching `LR2021`** returned by `old.reddit.com/search.json?q=LR2021&sort=new`
on 2026-09-04, of which **9 were read in full with their comment trees**. That is the whole sample;
prevalence claims are not made from it.

---

## 1. RadioLib — the exact commit and release

`github.com/jgromes/RadioLib` · **MIT** (`license.txt`, "MIT License / Copyright (c) 2018 Jan
Gromeš" — verified identical at tags `7.2.1` and `7.7.1`, 2026-09-04) · 2 565 stars.

| Milestone | Detail |
|---|---|
| **Feature request** | Issue **#1457**, *"Feature Request: Support for Semtech LR2021"*, opened by **@serialrf433** on **2025-03-13** — the day after Semtech's announcement |
| **First code** | `2472fbdf727e7263167bdc511f2bd0744194dd33` — *"[LR2021] Initial WIP commit"*, **2025-06-09**, @jgromes |
| **Sustained work begins** | `f203c77c161c02fa4e02e9c8c4a402b1e0c6660c` *"[LR2021] Add first few SPI commands"*, **2025-10-12** |
| **New base class** | `d696fed842bc77c6699ac83d9611a7d6e1c838d6` — ***"[LRxxxx] Create base class for common LR11xx and LR20xx commands"***, **2025-10-13**. ⚠ Read that carefully: the shared ancestor RadioLib chose for the LR2021 is **LR11xx**, not SX126x |
| **The PR** | **#1676**, *"[LR2021] Add support for LR2021"*, @jgromes, opened **2026-01-17**, **merged 2026-01-30** as `013b0a114f7f29a455a7ae64b2e6db5e382f67e0`. Closes #1457 |
| **First release containing it** | **7.6.0, 2026-02-19.** Release notes list ***"[LR2021] Add support for LR2021 (#1676) (#1457)"*** |
| **Verified absent from** | 7.2.1, 7.3.0, 7.4.0, **7.5.0** — `src/modules/LR2021` returns HTTP 404 at each of those refs, and `LR2021` appears 0 times in `keywords.txt` and in `src/RadioLib.h`. Present with 15 files at 7.6.0, 7.7.0 and 7.7.1 |

**So: if you want RadioLib LR2021 support, pin ≥ 7.6.0.** 7.5.0 (2026-01-10) is only six weeks
earlier and has nothing.

### 1.1 What the module contains

15 files, ~250 KB of source, split one file per PHY — which mirrors the chip's own command grouping:

```
LR2021.cpp  LR2021.h  LR2021_commands.h  LR2021_config.cpp  LR2021_registers.h  LR2021_types.h
LR2021_cmds_{chip_control,flrc,gfsk,lora,misc,ook,oqpsk,radio,ranging}.cpp
```

`LR2021_commands.h` alone is 48 984 B and `LR2021_config.cpp` 45 527 B — a fair measure of how much
new surface Gen 4 presents compared with a Gen-2 driver.

### 1.2 Post-release work, and who is doing it

The 7.6.0 change log is dominated by LR2021 fixes from **@lyusupov** (SoftRF) — implicit/explicit
LoRa header type (#1678), `DIO5` pull-up restriction (#1685), GFSK payload-length unit (#1687),
GFSK sync-word byte order (#1686), GFSK deviation and bit-rate limits clamped to the datasheet
(#1689, #1690), no-CRC GFSK/OOK with the inverted bit set (#1688). Later, **@caveman99** (a
Meshtastic core developer) lands `lr2021-cr-constants` (#1850, merged 2026-08-11) and
**@fabianbschmid** FLRC RSSI (#1816).

**Read that as a maturity signal, in both directions.** A stream of "set max limit … in accordance
with datasheet" fixes in the *first* release after merge means the initial implementation was
written against the command reference rather than against silicon; it also means several people
with hardware were exercising it hard within weeks. As of `267d4e95f30947bb86cd49c249c18c249a7cc19a`
(**2026-08-12**, *"[LR2021] Fix temperature readout"*) commits were still landing — **135 commits
touch `src/modules/LR2021`** between 2025-06-09 and 2026-08-12.

### 1.3 A capability nobody expected: ADS-B

PR **#1700**, *"[ADS-B] ADS-B support (LR2021 only)"*, @jgromes, merged **2026-02-19** into 7.6.0.
RadioLib can receive 1090 MHz ADS-B on this part and on no other. ⚠ Note the tension: RadioLib's
own `setFrequency()` documentation states the allowed ranges as **150.0–960.0 MHz, 1900–2200 MHz and
2400–2500 MHz**, which does not include 1090 MHz, and the datasheet's sub-GHz path stops at 960 MHz.
**Unresolved** — this record has not established how the ADS-B path is reached, and it was not
tested. Related community interest: r/ADSB `1tpy1zv` *"low power ADSB RX chip"*, 2026-05-28.

### 1.4 ⚠ A documented conflict between RadioLib and the datasheet

| Source | Says |
|---|---|
| **[DS]** Table 3-4, `IDDSBRLD` | `STDBY_RC` runs the **"Internal HFRC(32MHz)"** |
| RadioLib `LR2021.h` doc comment | *"uses **13 MHz RC oscillator**"* / `RADIOLIB_LR2021_STANDBY_RC (13 MHz RC oscillator)` |

Recorded, not resolved. It is a comment, not a register write, so it is very likely inert — but it
is the kind of thing that gets copied into someone's timing calculation. `not-tested`.

---

## 2. Meshtastic — supported, but only on the 2.8 line

`github.com/meshtastic/firmware`.

| Milestone | Detail |
|---|---|
| **Announcement reaction** | The **official @meshtastic Reddit account** posted the announcement on **2025-03-12**: *"Semtech announced their 4th gen #LoRa chip! … and they specifically mentioned Meshtastic! This is big news! 🎉 … We can't wait to get hardware that supports this chip."* (82 pts, 23 comments) — **vendor/project claim** |
| **The PR** | **#10401**, *"LR2021 radio on NRF_Promicro"*, by **@NomDeTom**, opened **2026-05-06**, **merged 2026-05-08** as `5e2ca8aed4239f6682dede26485c63fcb2fdd521` |
| **What it added** | `LR2021_RADIO` in `src/detect/LoRaRadioType.h`; new `LR2021Interface` **and a generic `LR20x0Interface` base class**, described in the PR body as *"based on the LR11x0 and LR1110"*; radio-detection logic; the `nrf52_promicro_diy_tcxo` variant |
| **Release status** | ⚠ **`LR2021Interface.cpp` is absent from `v2.7.26.54e0d8d`** (2026-06-24, the last non-prerelease of the 2.7 line) and `LR2021_RADIO` is absent from its `LoRaRadioType` enum — verified by reading both at that tag. It **is** present in `v2.8.0.47db0e3` (2026-09-01, prerelease). **LR2021 is a 2.8.x feature** |
| **Portduino / native Linux** | PR **#11252** *"add LR 2021 to portduino …"*, merged **2026-07-30** (`047c4e9feb9b`). Still-open follow-ups: **#11382** *"Portduino: Fix LR2021 switch tables, power ceilings and IRQ handling"* (2026-08-10), **#11138** *"feat(lr2021): enable LR2021 LoRa radio support on native/portduino"* (2026-07-22) |
| **Ongoing** | 35 issues/PRs mention LR2021; recent ones include `fix(lr2021): live LF↔HF reconfigure via full begin()` (#11279, 2026-07-29), `enable autoLDRO on LR2021` (#11139, 2026-07-22), `fix(radio): validate 2.4 GHz bandwidths` (#11317, open) |

### 2.1 Boards upstream

`USE_LR2021` appears in three variants plus Portduino glue:

| Variant | Notes from `variant.h` |
|---|---|
| `variants/nrf52840/seeed_mesh_tracker_X1/` | **SenseCAP MeshTracker X1.** `LR2021_DIO3_TCXO_VOLTAGE 1.6`; `LORA_DIO2` (P0.07) wired as **`BUSY`**; `LORA_DIO1` (P1.01) as IRQ; `// #define LR2021_DIO_AS_RF_SWITCH` **commented out**. Also `rfswitch.h` |
| `variants/esp32s3/meshnology-w12/` | Meshnology W12 |
| `variants/nrf52840/diy/nrf52_promicro_diy_tcxo/` | The DIY board PR #10401 landed against |

⚠ **`LR2021_DIO3_TCXO_VOLTAGE` is a misleading name inherited from the SX126x world.** On this part
the TCXO is supplied from the dedicated `VTCXO` pin and configured by `SetTcxoMode`, not by "DIO3"
(see [`README.md` §2, §6.2](README.md)). The constant is RadioLib's API shape, not a pin mapping.

### 2.2 Meshtastic's practical position, in one line

Supported, actively worked on, shipping on real hardware — and **not yet in a stable release**. A
user on the 2.7 stable channel has no LR2021 support at all. When @DanRTD asked
*"Any idea when the new LR2021 based nodes will be available to buy?"* (r/meshtastic `1tcb7ni`,
2026-05-13), **@NomDeTom — the author of PR #10401 — replied five days after merging it**:
*"They're supported now, in develop. Radio modules are available now."* (**firsthand-ownership**,
and about as authoritative as a forum reply gets.)

---

## 3. Semtech's own software

| Repo | What | Licence | Last push |
|---|---|---|---|
| **`LoRa-Net/usp`** | *"MCU FW SW driving LR20xx multi-PHY radios with multiprotocol operations and radio resource arbitration. Includes LoRa Basics Modem. **Backward-compatible with SX126x and LR11xx radio devices**."* Contains `lr20xx_driver` v2.0.2 | repo `NOASSERTION` (mixed); **driver subtree is BSD-3-Clause-Clear** | 2026-04-16 |
| **`LoRa-Net/usp_zephyr`** | Zephyr RTOS integration of USP; *"Compatible with LR20xx, SX126x and LR11xx"* | NOASSERTION | 2026-04-16 |
| **`LoRa-Net/LoRaStudio`** | *"Software designed to demonstrate LoRa Plus series capabilities"* — Windows GUI. Semtech's LR2021 page links `LoRaStudio_UserGuide.pdf` and `LoRaStudio_Windows_Setup.exe` **directly from GitHub**, not from Salesforce | none declared | 2026-06-26 |
| **`LoRa-Net/swdm031_img_xfer`** | *"Image transfer with FLRC long packet"* — the demo everyone asking about camera links is pointed at | NOASSERTION | 2026-02-10 |
| **`LoRa-Net/SWL2001`** | LoRa Basics Modem LoRaWAN stack (bundled in USP as 4.9.0) | BSD-3-Clause-Clear | 2025-10-15 |
| ⚠ `LoRa-Net/LoRaMac-node` | The classic reference LoRaWAN node | NOASSERTION | **2024-07-03 — predates the part** |

⚠ **There is no `lr2021_driver` repository.** Every other generation has a standalone one —
`sx126x_driver`, `llcc68_driver`, `SWDR005` (SX128x), `lr1110_driver`, `SWDR001` (LR11xx). Gen 4's
driver ships only inside the 47 MB USP monorepo, whose README says *"not intended for production
use"*. Releases: `v0.5.1-alpha` (2025-10-15), **`v1.0.0` (2025-12-16)**, `v1.1.1-feature-202602`
(2026-03-02), `v1.1.2-feature-202604` (2026-04-16). `LoRa-Net` and `Lora-net` are the same GitHub
org (case-insensitive) and return identical repository lists.

---

## 4. Evaluation kits and modules

| Part | What is in the box | Price (date) |
|---|---|---|
| **`LR2021EVK2XBS1`** | LR2021/LR2022 LoRa Plus EVK, **2 × `LR2021RF2XDS1`** RF boards, **EU 868 MHz + 2.4 GHz** | not published without JS |
| **`LR2021EVK2XCS1`** | as above, **NA 915 MHz + 2.4 GHz** | " |
| **`LR2021EVK2XGS1`** | **2 × `LR2021RF2XGS1`**, **CN/Asia 490 MHz + 2.4 GHz** | " |
| `LR2021EVK1XGS1` | earlier EVK1 generation, still listed | " |
| **Seeed "LR2021 LoRa Plus Evaluation kit 915 MHz US V2.0"** | **nRF54L15 + Wio-LR2021 + OLED + 2 SMA antennas + USB cable, ×2** | **US$99.00** (2026-09-04) |
| **Waveshare `Core2021-LF` / `-HF` / `-XF`** | bare LR2021 module, per-band SKU | **US$11.99 / US$12.99** (2026-09-04) |
| **NiceRF `LoRa2021F33-2G4`** | LR2021 + external PA, ~1 W | page **403s** to automated clients |

⚠ **The `Wio-LR2021` is Semtech's own EVK radio board, not a Seeed original.** Semtech's USP README
names the validated platform as *"LoRa Plus EVK (LoRa Plus Expansion Board + **Wio-LR2021**/Wio-LR2022/Wio-LR2012 radios)"*.
Seeed sells it; Semtech validates against it. Also from that README: **the CN 490 MHz `Wio-LR20xx`
needs a different PA table** from the 868/915 boards, per the datasheet's page-134 CN-490 entry.

**On the $99 kit's value**, since it looks expensive next to a $12 module — @Fir3, 2026-06-27:
*"The $100 is for two of these. So that means for $50 you get the nRF54L15, the LR2021, board
connecting them, oled screen, sma connections for the antennas, 2 antennas and a usb cable."*
(**firsthand-ownership**.) A dissenting first take from @The_Cat_Commando in the same thread was
withdrawn once the two-pack was pointed out.

---

## 5. What people actually report

### 5.1 Firsthand measurement

| Date | Who / where | Report | Class |
|---|---|---|---|
| **2026-06-05** | u/Time-Guidance-5150, r/meshcore [`1txo9ii`](https://old.reddit.com/r/meshcore/comments/1txo9ii/) (22 pts) | Bench-tested a **NiceRF `LoRa2021F33-2G4` 1 W module** (LR2021 + ESP32-S3 + 5 V/3 A supply) as a MeshCore node against a **RAK 1 W / SX1262** kit at the same power setting: *"I'm seeing 15-16 dB in indoor tests (vs 12-13 on Rak 1W / sx1262)"*, and later *"Early results are roughly **+2 dBm for tx/rx** compared to Rak 1W with same power setting."* Full config given: *"30 dBm TX, raw power 44, PA duty/slices 2/7, 128 µs ramp, RX boost 7, DIO6 LF-TX switch, DIO9 IRQ, TCXO 3.3 V, calibrate 0x6F, frontend cal at 912 MHz extended frequency-error mode on"* | **firsthand-measurement** — ⚠ SNR-vs-dBm units are used loosely, the comparison unit's true output was disputed in-thread by u/IAmSoWinning (5 V rail vs battery boost path on the RAK), and the promised detailed report was not posted within the search window. **Suggestive, not conclusive** |
| **2026-06-26** | u/Fir3, r/meshtastic [`1ugfytv`](https://old.reddit.com/r/meshtastic/comments/1ugfytv/) (177 pts) | Seeed nRF54L15 + Wio-LR2021 kit running a **Zephyr-based Meshtastic fork** (`github.com/dasmensch-su/Meshtastic-nRF54L15-LR2021-Multi-SF` — note *Multi-SF* in the name). Power: *"5 V at .01 A (50 mW) or less consistently"* through a DC boost | **firsthand-measurement**, coarse (whole-node, at the boost converter's input) |
| **2026-09-02** | u/accur4te, r/Lora [`1w519gm`](https://old.reddit.com/r/Lora/comments/1w519gm/) | **A negative result, and the most useful post in the corpus.** ESP32 + Waveshare `Core2021LF`, FLRC 260 kbps, aiming at 500 m+ for 150–200 KB JPEGs in woodland; **getting ~100 m**. Measured: *"-100 to -110 RSSI … 1 m RSSI was -30 and when put the nodes at 50 m apart LOS I went directly to -90 RSSI"*. Code published: `github.com/vedantjadhavkudrat/flrc_public_test_code` | **firsthand-measurement.** −30 dBm at 1 m and −90 dBm at 50 m is ~60 dB over a 34 dB free-space delta — the thread's diagnosis (antenna/Fresnel/init) is unresolved as of the search date |

### 5.2 Comparative context offered by experienced posters

u/StuartsProject, r/Lora [`1u6ldii`](https://old.reddit.com/r/Lora/comments/1u6ldii/), 2026-06-17 —
**SX1280** measurements offered as the baseline an LR2021 FLRC design should beat
(**firsthand-measurement**, on Gen-2 2.4 GHz silicon, *not* on an LR2021):

| Type | Frequency | Settings | File | Transfer time |
|---|---|---|---|---|
| LoRa | 434 MHz | SF7 BW500k CR4:5 | 46 000 B | 26.3 s |
| LoRa | 2.4 GHz | SF5 BW1600k CR4:5 | 46 000 B | 3.4 s |
| FLRC | 2.4 GHz | BR260 BW1_2 CR_0_3 | 46 000 B | 3.9 s |
| FLRC | 2.4 GHz | BR1300 BW1_2 CR_1_0 | 46 000 B | 1.9 s |

and separately: *"Using an ESP32 and the FLRC in 1,300,000 bps mode the achieved transfer rate was
673,027 bps"* — i.e. **~52 % of the nominal rate** once acknowledgement and framing are counted.
His advice to an LR2021-curious asker was, notably, **to start on an SX1280** because *"there is
more support and libraries for the 2.4 GHz SX1280 so it might be an easier place to start."*
(2026-06-18, **informed-interpretation**.)

u/Clamsax, same thread, 2026-06-15 (**informed-interpretation**, clearly hands-on): the 2.6 Mbps
figure *"is the raw data-rate of the payload part. It does not take into account the overhead of
preamble+syncword+header+CRC … It also does not take into account use of FEC"*, and — usefully —
on clocking: *"You can rely on the crystal oscillator of the LR2021, which should be less than
±30 ppm, which can also be improved with the API `set_xosc_trim`."* That is the "no TCXO needed"
claim being used in anger by someone planning a TDMA schedule.

### 5.3 On migration and mesh compatibility

The recurring worry is fragmentation, and the recurring answer is §8 of the component record.

- u/304769 → u/Time-Guidance-5150, r/meshcore, 2026-06-06: *"Would this make our current HW garbage
  due to incompatibility?"* → *"It should be compatible on subg band. I use it in experimental MC
  repeater now."* (**firsthand-ownership**)
- u/mosaic_hops, r/meshtastic, 2025-03-13 (19 pts) — the best early read anyone posted:
  *"Multi-SF receive which could make a huge difference in mesh efficiency by enabling different SF
  for both legs of an asymmetric link along with support for Very Long Slow **without a TCXO**. Also
  some interesting opptys to use 2.4 GHz for near neighbors to take some load off of the Sub-GHz
  band."* (**informed-interpretation** — and it identified the two features that turned out to
  matter, 14 months before hardware.)
- u/ShakataGaNai, r/meshtastic, 2025-03-13 (**informed-interpretation**, and a useful corrective):
  *"This is nowhere close … These LoRa chips are integrated into larger packages by other parties,
  which are then packaged up into something you can buy. Libraries need to be written for it,
  firmwares built, etc."* He was roughly right about the shape and about the timescale — **~14
  months from announcement to a pre-orderable Meshtastic node**.
- u/rcarteraz, r/meshtastic, 2025-03-13 (**hearsay**): *"This radio isn't expected to be available
  in quantity until the end of this year."* Broadly borne out.
- u/wirecrossed, r/meshtastic, 2026-06-27 (**firsthand-ownership**): *"My Waveshare Core2021 came in
  today and I will be pairing it with a Seeed nRF54L15 … I'll be interested to compare my
  esp32s3/lr1121 setups for sure."*

### 5.4 Product reception

- **SenseCAP MeshTracker X1** pre-orders: r/meshtastic [`1uyur93`](https://old.reddit.com/r/meshtastic/comments/1uyur93/)
  (2026-07-17, **395 pts**, 77 comments) and [`1v49g4p`](https://old.reddit.com/r/meshtastic/comments/1v49g4p/)
  (2026-07-23, **170 pts**, 73 comments). By r/meshtastic standards this is a large reaction.
- By 2026-09-05 the tone had moved on from novelty to configuration: r/meshtastic
  [`1w82lwo`](https://old.reddit.com/r/meshtastic/comments/1w82lwo/) *"Recommended configs for the
  new SenseCAP MeshTracker X1 as a GPS tracker?"* — the clearest sign it has become ordinary
  hardware.
- **RF-engineering-level interest**, which is unusual for a hobby part: r/rfelectronics
  [`1qmp6op`](https://old.reddit.com/r/rfelectronics/comments/1qmp6op/) *"Measuring S11 parameter of
  LR2021 LoRa transceiver"* (2026-01-25, 22 comments), and two threads
  ([`1r68c5n`](https://old.reddit.com/r/rfelectronics/comments/1r68c5n/), 2026-02-16;
  [`1r5t97o`](https://old.reddit.com/r/AskElectronics/comments/1r5t97o/), 2026-02-15) asking what the
  **reference design** is doing and **why it ships without component values** — consistent with
  §11.2 of the record: Semtech publishes the reference design, but behind the Salesforce gate.

### 5.5 An honest summary of the community picture

**Three things are consistently reported and one is consistently *not*.**

Reported: (a) the part works, on real firmware, on buyable boards; (b) the FLRC headline rate is
achievable only at roughly half the nominal figure once framing and FEC are counted, and its
**range at sub-GHz has disappointed at least one careful tester**; (c) the migration is not
mesh-breaking on plain LoRa.

**Not reported by anyone: a controlled sensitivity or range comparison against an SX1262 with
stated method.** The nearest thing is §5.1's `+2 dB` bench note, whose comparison unit's true
output was disputed in the same thread. **Every performance claim in the component record is
therefore a Semtech specification**, and the community has not yet independently confirmed the
headline −141.5 dBm or the multi-SF advantage. `not-tested`.

---

## 6. Sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Establishes |
|---|---|---|---|---|---|---|---|
| C-1 | RadioLib repo, releases, commits, PR #1676, issue #1457 | jgromes | community | source | `github.com/jgromes/RadioLib` | 2026-09-04 | §1 |
| C-2 | Meshtastic firmware, PR #10401, variants, tags | Meshtastic | community | source | `github.com/meshtastic/firmware` | 2026-09-04 | §2 |
| C-3 | `LoRa-Net` org repository listing | Semtech | primary | source | `api.github.com/orgs/LoRa-Net/repos` | 2026-09-04 | §3 |
| C-4 | USP README @ `512a095e…` | Semtech | primary | source | `raw.githubusercontent.com/LoRa-Net/usp/512a095e…/README.md` | 2026-09-04 | §3, §4 |
| C-5 | LR2021 / EVK product pages | Semtech | primary | vendor page | `www.semtech.com/products/wireless-rf/lora-plus/…` | 2026-09-04 | §4 |
| C-6 | LR2021 LoRa Plus Evaluation kit 915 MHz US V2.0 | Seeed Studio | primary | store listing | `www.seeedstudio.com/LR2021-LoRa-Plus-Evaluation-kit-915Mhz-US-V2-0-p-6698.html` | 2026-09-04 | §4 |
| C-7 | `Core2021-XF` | Waveshare | primary | store listing | `www.waveshare.com/Core2021-XF.htm` | 2026-09-04 | §4 |
| C-8 | Reddit corpus — 25 threads from `old.reddit.com/search.json?q=LR2021&sort=new`, 9 read with full comment trees | various | community | forum | permalinks inline | 2026-09-04 | §5. ⚠ `www.reddit.com` 403s automated clients; `old.reddit.com/search.json` with UA `WhatsApp/2.23.20.0` returns 200 |
| C-9 | `dasmensch-su/Meshtastic-nRF54L15-LR2021-Multi-SF` | community | community | source | cited by C-8 `1ugfytv`; **not inspected this pass** | — | §5.1 — recorded as a lead |
| C-10 | `vedantjadhavkudrat/flrc_public_test_code` | community | community | source | cited by C-8 `1w519gm`; **not inspected this pass** | — | §5.1 — recorded as a lead |
