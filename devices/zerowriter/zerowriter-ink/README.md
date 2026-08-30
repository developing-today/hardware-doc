# ZeroWriter Ink

> Open-source e-paper typewriter · Crowd Supply campaign funded **2024-10-17** · **$285** · 585 backers · $147,538 raised (491 % of a $30,000 goal)
> By **Adam Wilk** / Zerowriter, Ottawa, Canada, in collaboration with **Soldered Electronics** (Osijek, Croatia)
> Research snapshot **2026-08-24**

A distraction-free writing device: a 5.2" 1280×720 e-paper display, a hot-swappable 60 % mechanical keyboard, and firmware that boots straight into a text file. No cloud, no accounts, no wireless enabled by default.

---

## The single most important architectural fact

**ZeroWriter Ink contains two ESP32s.**

| Board | Processor | Role |
|---|---|---|
| **Zerowriter Inkplate 5 Gen2** (main board) | **ESP32-WROVER** | Display, storage, RTC, application firmware |
| **Zerowriter Keyboard** (keyboard PCB) | **ESP32-WROOM-32U-N4** | Key-matrix scanning, its own firmware |

This is recovered from the two KiCad BOMs in the project's own repository ([`design/src/`](artifacts/source-snapshots/zerowriter_ink/design/src/)) and is **not stated anywhere in the campaign material or the README**, which describe the device as "built around the ubiquitous ESP32 module" — singular. If you are planning firmware work, you need to know there are two independent targets joined by a cable.

The keyboard PCB carries a `NOVA_programmer_header` (6-pin) and connects to the main board through a **`HC-1.25-6PWT` 6-pin connector**, which strongly suggests a serial link rather than a scanned matrix crossing the cable — 61 × `1N4148W` matrix diodes are on the *keyboard* board, so the matrix is decoded locally.

> Evidence status: the two-processor split is **established from primary design files**. The *protocol* between them is **inferred** from connector pin count and the placement of the matrix diodes — not confirmed from source.

---

## The second important fact: this is not a stock Inkplate 5

ZeroWriter's main board is a **respin** of Soldered's Inkplate 5 Gen 2, not the off-the-shelf product. Comparing the two BOMs designator-by-designator ([Soldered Gen 2](../../soldered-electronics/inkplate-5-gen2/README.md) vs [ZeroWriter's variant](artifacts/source-snapshots/zerowriter_ink/design/src/)) shows **8 added parts, 14 removed, and 20 changed values**.

### Which Inkplate generation? — **Gen 2**, confirmed five ways

Worth stating plainly, because the campaign's early material described a different panel (see below).

| Evidence | Result |
|---|---|
| ZeroWriter BOM, `U9` | **`ED052TC4`** |
| Soldered Inkplate 5 **Gen 2** BOM, `U9` | `ED052TC4` ✅ match |
| Soldered Inkplate 5 (gen 1) BOM, `U11` | `ED052TC2` ❌ different part *and* different designator |
| ZeroWriter's KiCad project name | `Zerowriter Inkplate 5 **Gen2**.kicad_pro` |
| Crowd Supply spec | "**second-edition** Inkplate 5.2" display with an upgraded **1280 × 720** widescreen resolution" |
| Campaign update, Nov 2024 | "we jumped on their **new generation panel: Inkplate 5v2**" |

`ED052TC4` ⇒ **1280 × 720** (`ARDUINO_INKPLATE5V2`). The gen-1 `ED052TC2` is 960 × 540.

#### ⚠ The panel changed mid-project

If you recall the ZeroWriter Ink being a **gen-1** Inkplate 5, that was true of the **development prototype**. The developer describes the switch in the Nov 2024 post-funding update:

> When it came to Zerowriter Ink, **we jumped on their new generation panel: Inkplate 5v2**… The downside? … The new panels looked great, but operated at about 200 ms. This was **a decent chunk slower than the panel I'd been developing into Zerowriter Ink**…

So the sequence was: prototype on the **gen-1 panel** → switch to **Gen 2** for the higher resolution → discover it is slower → commission [bitbank2's optimisation work](development-history.md#the-e-paper-latency-problem-and-how-it-was-solved) to get from ~200 ms to ~100 ms.

**The shipping product is Gen 2.** Pre-funding material describing a 960 × 540 panel is describing the prototype.

### "Minor tweaks" is an understatement

The respin is not a light touch. Designator-by-designator against Soldered's stock Gen 2: **8 parts added, 14 removed, 20 values changed**, including a complete charger redesign and relocation of USB-C and microSD to a separate board.

What *is* unchanged is the part that matters for software: **all 36 connected ESP32 pads carry identical net names** ([verified](../../soldered-electronics/inkplate-5-gen2/README.md#zerowriter-compatibility)), so the Inkplate Arduino library applies. That is probably the origin of the "minor tweaks" impression — from a firmware perspective it behaves like a stock Gen 2; from a hardware perspective it is substantially reworked.

### The charger was completely redesigned

| | Soldered Inkplate 5 Gen 2 | **ZeroWriter variant** |
|---|---|---|
| Charger IC | `MCP73831T` — **linear** | **`BQ25306RTER`** — TI **switch-mode** buck charger |
| Inductor | — | **`L3 = SRP3212A-1R0M`** (1 µH) added |
| Support caps | — | `C58` 4u7, `C59` 2u2, `C60`/`C61` 10u, `C62` 470p added |
| `U4` position | `MCP73831T` (charger) | **`USBLC6-2SC6`** — USB ESD protection |

A linear charger dissipates `(Vin − Vbat) × Icharge` as heat, which caps practical charge current on a small board. Swapping to a switch-mode `BQ25306` is exactly what you do when you fit a much larger cell and want it charged in reasonable time without cooking the PCB. This is consistent with the campaign's "up to weeks of daily use" and ~100 hour battery-life claim.

### Connectors moved off the display board

| Ref | Soldered Gen 2 | ZeroWriter variant | Reading |
|---|---|---|---|
| `K2` | `U262-161N-4BVC11` (**USB-C receptacle**) | `HC-1.25-6PWT` (**6-pin wire-to-board**) | USB-C is **not on the display board** — it moves to the separate breakout PCB |
| `K1` | — | `HC-1.25-16PWT` (**16-pin**) added | New inter-board link |
| `K3` | `easyC-SMD` | `qwiic-SMD` | Same physical connector, renamed. Soldered's *easyC* is pin-compatible with SparkFun *Qwiic* / Adafruit *STEMMA QT* |
| `K10` | `HYC77-TF09-200` (**microSD socket**) | *removed* | microSD relocated off the display board |

### Parts removed

`U5` (`MC14093BDTR2G` quad Schmitt NAND), `F1` (500 mA fuse), `D8`/`D9` (LEDs), `SW2` (button), `S1` (slide switch), `Q8`/`Q9`, and test points `TP60`–`TP63`. Plus ~20 resistor/capacitor value changes clustered around the power and charging sections.

**Consequence for hackers:** a stock Inkplate 5 Gen 2 is *close* to the ZeroWriter main board but not identical. Firmware written against the Inkplate Arduino library should work (same ESP32-WROVER, same `ED052TC4` panel, same `TPS65186` PMIC, same `PCAL6416A` expander, same `PCF85063A` RTC), but **power, charging, USB and SD paths differ** — do not assume battery or SD behaviour transfers.

---

## Architecture

```
┌─ Zerowriter Keyboard PCB ──────────────────────────────┐
│ ESP32-WROOM-32U-N4  (external-antenna variant)         │
│ 61 × 1N4148W matrix diodes                             │
│ Kailh Choc v1 hot-swap sockets (CPG135001S30)          │
│   incl. 1.2u / 1.5u / 1.7u / 2u / 6.25u stabilised keys│
│ RST1/RST2 tactiles · NOVA 6-pin programmer header      │
└────────────── HC-1.25-6PWT (6-pin) ────────────────────┘
                       │
┌─ Zerowriter Inkplate 5 Gen2 (main) ────────────────────┐
│ ESP32-WROVER              U11                          │
│ ED052TC4  5.2" 1280×720 e-paper   U9                   │
│ TPS65186RGZ  e-paper PMIC          U1                  │
│ PCAL6416AHF  16-bit I²C GPIO expander @ 0x20  U10      │
│ PCF85063A    RTC                    U7                 │
│ CH340C       USB-UART               U3                 │
│ BQ25306RTER  switch-mode Li-ion charger  U12  [ZW-only]│
│ TPS7A2633    3V3 LDO · TPS3840 supervisor              │
│ qwiic/easyC I²C connector                              │
└──── HC-1.25-16PWT (16-pin) ────────────────────────────┘
                       │
┌─ Zerowriter breakout board ────────────────────────────┐
│ USB-C, microSD (relocated from the display board)      │
└────────────────────────────────────────────────────────┘
```

Component records: [ESP32-WROVER](../../../components/espressif/esp32-wrover/README.md) · [ESP32-WROOM-32U](../../../components/espressif/esp32-wroom-32u/README.md) · [TPS65186](../../../components/texas-instruments/tps65186/README.md) · [PCAL6416A](../../../components/nxp/pcal6416a/README.md) · [PCF85063A](../../../components/nxp/pcf85063a/README.md) · [BQ25306](../../../components/texas-instruments/bq25306/README.md) · [CH340C](../../../components/wch/ch340c/README.md) · [ED052TC4 panel](../../../components/e-ink/ed052tc4/README.md)

## Specifications

| | |
|---|---|
| Display | **Inkplate 5 Gen 2 panel — `ED052TC4`, 5.2", 1280 × 720** e-paper |
| Keyboard | 60 %, hot-swappable, **Kailh Choc Pro Red** low-profile switches, US English legends, optional arrow-key mod |
| Languages | Extended ASCII 256 — English, French, German, Spanish, Italian and other western/latin scripts |
| Dimensions | **300 × 195 × 15 mm** (12 × 7.5 × 0.6 in) — fits most 13" laptop sleeves |
| Storage | microSD (user files), plus firmware update via SD |
| Connectivity | USB-C (charging + UART file transfer via companion app); **QR-code transfer to phone**; Wi-Fi/BLE present in silicon but **not enabled in shipped firmware** |
| Battery | Built-in, **user-replaceable** LiPo; ~100 h claimed |
| Document limit | **3,000 lines (~24,000 words)** per document |
| Firmware | Arduino-based ("Zerowriter Core"). Repo releases end at **1.30**; **current is v2.1 (July 2026)**, website-only — see [`community-and-ecosystem.md`](community-and-ecosystem.md#-the-repository-firmware-is-two-major-versions-behind) |
| Enclosure | Custom; STLs in-repo (`zw_tophousing.stl`, `zw_bottomhousing.stl`) |

**On wireless:** the campaign is explicit that shipping without wireless was a deliberate cost/certification decision — "less development time, less red-tape, and less cost to you" — not a hardware limitation. Note the keyboard uses a **WROOM-32U**, the *external antenna* variant, which has no PCB antenna at all. Enabling radio on either processor is a project, not a config flag.

## Vendor comparison (from the campaign)

| | Zerowriter Ink | Pomera DM30 | Alphasmart Neo | Freewrite Alpha | Freewrite Traveler |
|---|---|---|---|---|---|
| Display | **HD e-paper** | e-paper | LCD | LCD | e-paper |
| Cloud | Not by default | No | No | Yes | Yes |
| Availability | **New** | Used | Used | New | New |
| Mechanical keyboard | **Yes, hot-swap** | No | No | Yes | No |
| Battery (claimed) | 100 h | 20 h | **700 h** | 100 h | 4 weeks |
| Open source | **Yes** | No | No | No | No |

Vendor-authored comparison — treat as marketing. The Alphasmart Neo's 700 hours on AA cells is the honest outlier and the standard this class of device is measured against.

## Lineage

The **original ZeroWriter** ([`zerowriter/zerowriter1`](artifacts/source-snapshots/zerowriter1/), 367★, MIT) was a Raspberry Pi Zero + cheap e-paper DIY project. ZeroWriter Ink is a ground-up redesign on the Inkplate 5 — a different processor family, a different display, and a commercial product rather than a build-it-yourself guide. The two share a name and a goal, not a codebase.

## Website: zerowriter.**ink**, not .com

⚠ **`zerowriter.com` is a domain-for-sale parking page** (Spaceship.com, $7,500) and is *not* the project. The Crowd Supply campaign links to it, so it is an easy trap.

**The live site is <https://zerowriter.ink>.** Found via a URL embedded in the firmware release notes shipped in the GitHub repo (`firmware_releases/updates-readme.txt` points at `zerowriter.ink/pages/firmware-updates`), not from any link on the campaign page.

The live site reveals a **second product**: the **Zerowriter Fold**, funded via Kickstarter and shipping after the Ink.

| Source | URL | Status |
|---|---|---|
| **Official site** | <https://zerowriter.ink> | **Live** |
| Firmware updates + web flasher | <https://zerowriter.ink/pages/firmware-updates> | **Live** |
| News blog | <https://zerowriter.ink/blogs/news> | Live |
| Zerowriter Fold | <https://zerowriter.ink/pages/zerowriter-fold> | Live |
| Crowd Supply campaign | <https://www.crowdsupply.com/zerowriter/zerowriter-ink> | Live |
| GitHub (main) | <https://github.com/zerowriter/zerowriter_ink> | Live, GPL-3.0 |
| GitHub (original Pi project) | <https://github.com/zerowriter/zerowriter1> | Live, MIT |
| Discord | <https://discord.gg/57yANTWGet> | Live |
| **Reddit** | <https://www.reddit.com/r/zerowriter/> | Live — official support channel |
| `zerowriter.com` | — | **Parked / for sale. Not the project.** |

> **Retrieval trap:** `zerowriter.ink` returns **403 to a normal Chrome user agent** but **200 to the ClaudeBot UA**. See the [vendor guide](../../../vendors/zerowriter/README.md).

## Press coverage

Tom's Hardware · Liliputing · Boing Boing · Yanko Design · Notebookcheck (DE) · CircuitDigest · TechEBlog · Good e-Reader · e-ink-info · ereaderpro.co.uk · pascalforget.com — full URLs in [`sources.md`](sources.md).

## Repository contents (preserved)

```
artifacts/source-snapshots/zerowriter_ink/     GPL-3.0, commit 996207ac (2026-05-13)
├── design/
│   ├── src/Zerowriter Inkplate 5 Gen2/v1.2.0/   KiCad: main board respin
│   ├── src/Zerowriter Keyboard/v1.2.0/          KiCad: keyboard + ESP32-WROOM-32U
│   ├── src/Zerowriter breakout board/           gerbers: USB-C + microSD
│   ├── zw_keyboard/                             plate DXF, gerbers, schematic PDF
│   └── enclosure/                               zw_tophousing.stl, zw_bottomhousing.stl
├── firmware_releases/                           SD-1.3, archived updates, CLI tools
├── compiled fonts/                              .bbf bitmap fonts
├── src/keyboard/                                keyboard firmware source
└── utils/
artifacts/source-snapshots/zerowriter1/        MIT, commit e476d056 — the Pi Zero original
```

### Size cleanup — what was moved out (2026-08-24)

Two things were archived out of this tree. **Both left a placeholder in situ** carrying digests and
reacquisition commands, and neither is unique:

| Removed | Size | Placeholder | Why it was safe |
|---|---:|---|---|
| `zerowriter1/e-Paper/` — Waveshare's vendored Python driver library | 31.07 MiB, 272 files | [`e-Paper.ARCHIVED.md`](artifacts/source-snapshots/zerowriter1/e-Paper.ARCHIVED.md) | 270 of 272 files byte-identical to Waveshare upstream; the 2 that differ are preserved as patches |
| 4 × KiCad `*-backups/` auto-save ZIP directories | 27.27 MiB, 15 files | one `*.ARCHIVED.md` beside each | editor crash-recovery snapshots of designs that are still present, uncompressed, alongside |

The entire `zerowriter_ink` snapshot was verified **byte-identical** to upstream commit `996207ac`,
so the backups are recoverable verbatim. **No design file, firmware image or ZeroWriter-authored
source was removed.**

- [`artifacts/vendored-deps/README.md`](artifacts/vendored-deps/README.md) — removed-dependency register: digests, licenses, verified download URLs
- [`zerowriter1-epaper-driver-notes.md`](zerowriter1-epaper-driver-notes.md) — **what ZeroWriter changed in the Waveshare driver, and why it matters**

## Related

- [Inkplate 5 / Gen 2](../../soldered-electronics/inkplate-5/README.md) — the display platform this is built on
- [Soldered Electronics vendor guide](../../../vendors/soldered-electronics/README.md)
- [All devices](../../README.md)
- [`keyboard.md`](keyboard.md) — the second ESP32, wire protocol, matrix
- [`inter-board-wiring.md`](inter-board-wiring.md) — both connector pinouts, breakout board BOM
- [`keymap-format.md`](keymap-format.md) — `keymap.json`, full default layout
- [`software-and-shortcuts.md`](software-and-shortcuts.md) — shortcuts, Core 1.1, release timeline
- [`community-and-ecosystem.md`](community-and-ecosystem.md) — **firmware v2.1**, third-party firmware, owner reports
- [`development-history.md`](development-history.md) — design rationale from 17 campaign updates
- [`zerowriter1-original.md`](zerowriter1-original.md) — the Raspberry Pi predecessor
- [`firmware-and-updates.md`](firmware-and-updates.md) — releases, flashing, recovery
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md)
- [`sources.md`](sources.md)
- [Zerowriter Fold](../zerowriter-fold/README.md) — the second-generation device
