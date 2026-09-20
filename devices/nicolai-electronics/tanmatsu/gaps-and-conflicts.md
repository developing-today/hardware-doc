# Tanmatsu — gaps, conflicts and unresolved questions

> Where the vendor's sources disagree, where information is missing, and what this research pass did not cover.
> Snapshot **2026-08-24**.

The Tanmatsu documentation carries its own warning, which is worth taking at face value:

> *"Note: information on this page is actively being worked on and might contain accidental errors and inaccuracies."*
> — `hardware/specifications/index.md`

It does contain at least one. This page records what I found.

---

## 1. ESP32-P4 clock speed: 360 MHz or 400 MHz?

**The two main documentation pages contradict each other**, in the same repository, at the same commit (`bd3ded51`):

| Source | Claim |
|---|---|
| `src/index.md` (Introduction → Features) | *"its **360MHz** dual-core processor and 32MB of built-in PSRAM"* |
| `src/index.md` (Summary of hardware features) | *"ESP32-P4 dual-core **360MHz** RISC-V microcontroller"* |
| `src/hardware/specifications/index.md` | *"CPU: 32-bit RISC-V dual core microprocessor, up to **400 MHz**"* |

Espressif's own public material for the ESP32-P4 has cited **400 MHz** as the maximum core frequency. The most likely reading is that **400 MHz is the silicon maximum and 360 MHz is the frequency Tanmatsu actually runs at** (or an earlier figure from pre-release silicon that was never updated on the marketing page) — but **no source states this**, and the difference is 11 %.

**Update 2026-08-24:** [badge.team's Konsool documentation](https://badge.team/docs/badges/konsool/) states **400 MHz** consistently (*"dual core 400MHz Risc-V ESP32-P4 CPU"*, *"dual-core RISC-V CPU running up to 400 MHz"*). Two of three vendor sources now say 400 MHz.

**Status: probably 400 MHz; Tanmatsu's front page is likely stale.** Still not definitive — read it back at runtime if it matters.

---

## 2. The ESP32-P4 datasheet was not public

The vendor states flatly:

> *"The datasheet for this chip is not yet publicly available"*

This is the single biggest information gap for the device. Consequences:

- Electrical limits, GPIO drive strengths, IO matrix restrictions and peripheral errata for the **ESP32-P4NRW32** must be inferred from ESP-IDF source, Espressif's dev-kit material, or the P4 documentation that has since been published.
- Anyone designing an add-on board is working without the application processor's absolute-maximum ratings.

**Status: partially resolved by time.** Espressif has since published ESP32-P4 documentation — see the [ESP32-P4 component record](../../../components/espressif/esp32-p4/README.md) in this tree, which holds the datasheet, TRM, errata and hardware design guidelines. The *Tanmatsu* documentation has not been updated to reference them.

---

## 3. What exactly is "Konsool"?

Three build targets exist and are treated as near-identical in software: `tanmatsu`, `konsool`, `why2025`. The app repository says only:

> *"Since Tanmatsu and Konsool are essentially the same device we recommend always adding both to apps that have been developed for one of these boards."*

**What is not documented anywhere I retrieved:**

- Why a second name exists for "essentially the same device"
- Who manufactures or sells Konsool
- What the actual hardware differences are — if any — that justify a separate BSP target
- The relationship to the WHY2025 camp badge

There is **no Konsool hardware repository** under Nicolai-Electronics, no Konsool documentation, and no Konsool specification page. The name appears only in software target lists and in one community repo title (`ranzbak/konsoolnes`, "NES emulator for Konsool/Tanmatsu ESP32-P4 device").

**RESOLVED 2026-08-24.** [badge.team](https://badge.team/docs/badges/konsool/) explains it directly: **Konsool is the open hardware design** (custodian: Badge.Team); **Tanmatsu is the pre-assembled version sold by Nicolai Electronics**, who take on safety and environmental certification and sell "practically at cost". Same device, same CERN-OHL-P files.

**WHY2025 is genuinely different hardware** — proven by diffing the BSP targets: different I2C pins, an I2C keyboard controller instead of a coprocessor-scanned matrix, no CATT, no SD card, no IMU, no audio codec.

There is **no `konsool` BSP target**; Konsool builds use `CONFIG_BSP_TARGET_TANMATSU`. And 56 of 57 apps ship one binary for both targets — they are binary compatible.

Full analysis: [`konsool-and-family.md`](konsool-and-family.md).

---

## 4. Hardware repo is months behind the software

| Repo | Last commit |
|---|---|
| `tanmatsu-launcher` | 2026-08-23 |
| `app-repository` | 2026-08-22 |
| `tanmatsu-documentation` | 2026-08-01 |
| `tanmatsu-mechanical` | 2026-07-03 |
| **`tanmatsu-hardware`** | **2026-02-25** |

The hardware design has not been touched in ~6 months while software ships weekly. That is normal for a product that has entered production — but it also means **the published KiCad may not match late production units**. No board revision number, PCB revision marking, or change log is published in the hardware repository, so there is no way to tell from the files which revision they represent.

**Status: open.** What would resolve it: a revision field in the KiCad title block, a `CHANGELOG`, or silkscreen revision markings documented anywhere.

---

## 5. Camera support is much narrower than the connector implies

The camera connector is *"pinout-compatible with the camera connector on the Raspberry Pi Zero and 5"*, but:

> *"software support is limited to a subset of Raspberry Pi compatible camera module sensor chips such as OV5647"*

**RESOLVED 2026-08-24** — but not by Nicolai Electronics. [badge.team publishes the list](https://badge.team/docs/badges/konsool/compatibility/camera/):

| Sensor | Max resolution | Output formats |
|---|---|---|
| GC2145 | 1600 × 1200 | RGB565, YCbCr422, 8-bit raw RGB |
| OV2710 | 1920 × 1080 | raw RGB |
| OV5645 | 2592 × 1944 | 8/10-bit raw RGB, RGB565, YUV/YCbCr422, YUV420 |
| OV5647 | 2592 × 1944 | 8/10-bit raw RGB |
| SC035HGS | 640 × 480 | raw mono, raw RGB |
| SC202CS (SC2356) | 1600 × 1200 | 8/10-bit raw RGB |
| SC2336 | 1920 × 1080 | 8/10-bit raw RGB |

Applications use Espressif's `esp_cam_sensor` driver. Note **IMX219 and IMX477 are absent** — the most common Raspberry Pi cameras will fit and not work.

**Status: resolved.** The Tanmatsu documentation still does not carry this list.

---

## 6. Display cannot use its full colour depth

> *"display supports 16M colors (24-bit / RGB888) but current software can not make use of this mode"*

A software limitation, acknowledged, with no stated timeline. Anyone planning image-heavy applications should assume **RGB565** for now.

**Status: acknowledged limitation, not a conflict.**

---

## 7. Add-on identification EEPROM format is undefined

The internal add-on port documentation asks designers to fit an EEPROM at 0x50, then says:

> *"The format for the content of this EEPROM has yet to be determined, currently the launcher firmware has no support for identifying add-ons. The format will most likely be based on the format described [in the Badge.team SAO binary descriptor standard]."*

So the identification mechanism is **specified as a socket but not as a protocol**. If you are building an add-on now, you can fit the EEPROM but cannot write meaningful contents.

**Status: open by the vendor's own admission.**

---

## 8. Coprocessor firmware licensing timing

The specifications page says:

> *"The firmware for this chip will be made available under terms of the MIT license after the product starts shipping to customers."*

As of this snapshot the [`tanmatsu-coprocessor-firmware`](https://github.com/Nicolai-Electronics/tanmatsu-coprocessor-firmware) repository **exists and does carry an MIT `LICENSE` file** (commit `57ff2505`, 2026-06-17). So the promise appears to have been kept and the specifications page is simply stale in its phrasing.

**Status: resolved; documentation wording is out of date.**

---

## 9. Repositories without licence files

Four repositories have **no `LICENSE` file**:

| Repo | Consequence |
|---|---|
| `tanmatsu-documentation` | Documentation text is under no stated licence — quoting is fine, wholesale reproduction is legally unclear |
| `tanmatsu-template` | **The template app you are told to base your project on has no licence.** This is the most consequential of the four |
| `app-repository` | The index itself; individual apps do declare licences |
| `esp32-component-tanmatsu-coprocessor` | The driver component you would link into your firmware |

The hardware and most firmware repos are properly licensed (CERN-OHL-P / MIT / Apache-2.0), so this looks like oversight rather than intent — but as written, the starting template for every Tanmatsu app grants no rights.

**Status: open.** Worth raising upstream.

---

## 10. Branding is explicitly excluded from the open licence

Not a conflict, but easy to miss when forking:

> *"All organization names, logos, trademarks and artwork including but not limited to the Nicolai Electronics and Tanmatsu branding are all rights reserved for their respective owners and may not be reproduced on derivative works."*

The **electronics** are CERN-OHL-P. The **silkscreen art and names are not.** Strip branding before fabricating a derivative.

---

## 11. Smaller open questions

| Question | Known | Would be resolved by |
|---|---|---|
| Actual battery life in realistic use | 2500 mAh cell; standby claim of ">10 years if never turned on" (theoretical, vendor's own hedge) | Measurement |
| Real Wi-Fi throughput via esp-hosted over the C6 | Nothing published | Benchmark |
| LoRa range in practice | E22-900M22S is 22 dBm | Field testing |
| Which PCB revision ships today | Not marked in published files | Silkscreen photo of a production unit |
| Price, availability, lead time | Not researched in this pass | Vendor webshop |
| Whether the SCD4x sensor header is populated on any SKU | Documented as user-solderable, "not populated" | Photos of production units |
| Total device current budget | 3.3 V rail limited to 1 A for add-ons; total system draw unpublished | Measurement |
| Contents of `tanmatsu.zip` in `production/` | Present in the hardware repo (Gerbers, presumably) | Not opened in this pass |

---

## 12. What this research pass did not cover

Stated plainly so the boundary is clear:

- **No hardware.** No measurement, no photograph, no build, no flash. Every command in [`development.md`](development.md) is `reported-working` or `inferred`.
- **Community channels not mined.** Discord and Telegram are where Tanmatsu discussion actually happens, and neither was searched. Nor were forums, blogs, YouTube or conference talks. **This is the biggest gap.**
- **Pricing and availability not researched.** No webshop scrape, no market comparison, no competitor analysis.
- **Mechanical repo cloned but not analysed** — 119 MB of case design was retrieved but not documented.
- **The launcher and coprocessor firmware source were cloned but not read in depth.** Both would repay study; the coprocessor firmware in particular is the authoritative description of the I2C register interface.
- **`badgeteam/esp32-component-badge-bsp` was not cloned** — only its target list was queried. The authoritative keymap and pin definitions live there.
- **No KiCad netlist extraction was performed.** Unlike the XIAO pass in this tree, connectivity here is taken from vendor documentation rather than derived from the PCB. The files are present ([`artifacts/schematics/kicad/`](artifacts/schematics/kicad/), [`artifacts/production/netlist.ipc`](artifacts/production/netlist.ipc)) and this would be a high-value next step — the IPC-D-356 netlist in particular is machine-readable connectivity requiring no KiCad parsing at all.

## Related

- [`README.md`](README.md) — device overview
- [`pinouts-and-buses.md`](pinouts-and-buses.md) — what *is* established
- [`sources.md`](sources.md) — provenance and evidence boundary

---

## 14. NEW — badge.team's expansion-port GPIO numbering contradicts itself

Discovered 2026-08-24. Within badge.team's own documentation, two pages disagree about which
ESP32-P4 GPIO carries which `E`-numbered expansion pin:

| Pin | [Back-expansion page](https://badge.team/docs/badges/konsool/hardware/pinout/connectors/back_expansion/) | [ESP32-P4 IC page](https://badge.team/docs/badges/konsool/hardware/pinout/ics/esp32p4/) |
|---|---|---|
| GPIO0 | `E1` | **`E2`** |
| GPIO6 | `E2` | **`E1`** |
| GPIO7 | `E7` | *"Interrupt from internal Add-On board"* |
| GPIO35 | *(not listed)* | **`E1` / BOOT** |
| GPIO49 | `E9` | **`E7`** |
| GPIO50 | `E13` | **`E8`** |
| GPIO51 | `E12` | **`E9`** |
| GPIO52 | `E11` | **`E10`** |
| GPIO53 | `E10` | **`E11`** |
| GPIO54 | `E8` | **`E12`** |

**Which to trust:** the **back-expansion page**. It agrees exactly with Nicolai Electronics'
independent internal-add-on-port documentation (`E0`=36, `E1`=0, `E2`=6, `E3`=46 … `E13`=50), so two
independent vendor sources corroborate it. The IC page appears to carry an off-by-one/misaligned
label set for the `E` names.

The IC page is still the better source for **everything else** — it is the only place the coprocessor
SWD pins (22/23), the C6 SDIO bus, the LDO allocation and the LCD TE pin are documented.

**RESOLVED 2026-08-24 from fabrication data.** [`tools/verify_expansion_pinout.py`](tools/verify_expansion_pinout.py)
cross-references the **IPC-D-356 fabrication netlist** ([`artifacts/production/netlist.ipc`](artifacts/production/netlist.ipc))
against the ESP32-P4 datasheet pin table:

```
connector page : 10 correct, 0 wrong
IC page        :  0 correct, 8 wrong
```

**The connector pinout is correct; the IC page's `E`-labels are wrong.** The rest of the IC page
(coprocessor SWD pins, C6 SDIO bus, LDO allocation, LCD TE pin) is correct and unavailable
elsewhere, so do not discard it — just ignore its `E` numbering. See
[`pinouts-and-buses.md` §2d](pinouts-and-buses.md).

## 15. NEW — coprocessor `PM_INT` is wired but unused

badge.team's CH32V203 pinout lists **pin 46 (`PB9`) = `PM_INT`**, an interrupt from the BQ25895 PMIC.
The shipped coprocessor firmware's `hardware.h` **does not define this pin at all**, which implies
the firmware **polls** the PMIC rather than responding to its interrupt.

Not necessarily a defect — polling a charger is perfectly reasonable — but it means a hardware
capability is present and unexploited, and anyone modifying the coprocessor firmware has a spare
interrupt available.

**Status: open**, inferred from absence. Not confirmed by reading `main.c` in depth.

## 16. NEW — `BOOT0` doubles as camera power enable

Also from the CH32V203 pinout: **pin 44 (`BOOT0`) = `DCAM_IO0`**, "camera module power enable (if
present)". Using a boot-strapping pin as a functional output means camera power state and coprocessor
boot behaviour are entangled. Additionally **pin 45 (`PB8`) is `RADIO_ENABLE / CAM_IO0`** — shared
between the ESP32-C6 enable and a camera IO.

Consistent with the already-documented sharing of the camera enable with the radio enable, but the
`BOOT0` reuse is not mentioned in any Tanmatsu document.

**Status: open**, documented by badge.team, unverified electrically.

## 17. Resolved since first draft

| Item | Resolution |
|---|---|
| What is Konsool? | **Resolved** — open design vs. pre-assembled product. See [`konsool-and-family.md`](konsool-and-family.md) |
| Supported camera sensors | **Resolved** — 7 sensors listed by badge.team (§5) |
| Is there a `volume_down` key? | **Resolved** — it is a discrete button on ESP32-P4 GPIO35, not a matrix key |
| Which PCB revision ships? | **Partially** — revisions 1/2/3 exist; readable via `Settings > Device information`. Rev 1→2 changes still unknown |
| Is the Tanmatsu keyboard Solder Party's? | **Strengthened** — badge.team call it a *"QWERTY dome keyboard by Arturo"* (arturo182 = Solder Party) |
| ESP32-P4 clock | **Probably 400 MHz** (§1) |


## 18. NEW — `E8` and `E10` are documented as free GPIO but carry the ESP32-C6 UART

**Found 2026-08-24 by parsing the fabrication netlist. Both vendors are wrong about this.**

Nicolai Electronics and badge.team both list these expansion pins as usable *"without limitations"*:

> `E0, E1, E7, E8, E9, E10, E11, E12 and E13`

The netlist shows otherwise:

| Net | Members | Reality |
|---|---|---|
| `E8` | `J7.19`, `U7.98` (GPIO54), **`R4` 2.2 kΩ → `/RADIO/TX` → `U20.25`** | ESP32-C6 **UART TX** |
| `E10` | `J7.21`, `U7.97` (GPIO53), **`U20.24`** | ESP32-C6 **UART RX** |
| `E0` | `J7.11`, `U7.68` (GPIO36), **`R5` 4.7 kΩ → +3.3 V** | undocumented **pull-up** |

badge.team's own [ESP32-C6 pinout page](https://badge.team/docs/badges/konsool/hardware/pinout/ics/esp32c6/)
independently lists C6 pin 24 = `RXD0` *"UART to P4 Receive"* and pin 25 = `TXD0` *"UART to P4
Transmit"* — so both halves are documented, they were simply never reconciled with the
"no limitations" list.

**Consequence:** an add-on board driving `E8` or `E10` will corrupt the ESP32-C6 serial console, and
`E10` will contend with the C6's output driver. Genuinely unrestricted pins are **`E1`, `E9`, `E11`,
`E12`, `E13`** (GPIO0, 49, 52, 51, 50). Full analysis: [`pinouts-and-buses.md` §2c](pinouts-and-buses.md).

**Status: open upstream** (not reported), **resolved here** from primary fabrication data.

## 19. NEW — the LoRa radio is controlled by the ESP32-C6, not the ESP32-P4

Every LoRa signal in the netlist connects **only** between `U20` (ESP32-C6-WROOM-1) and `U23`
(E22-900M22S):

```
LORA_SCK    U20.8   U23.18        LORA_MISO   U20.26  U23.16
LORA_CS     U20.9   U23.19  R59   LORA_MOSI   U20.27  U23.17
LORA_BUSY   U20.5   U23.14        LORA_DIO1   U20.4   U23.13
LORA_RESET  U20.11  U23.15  R62
```

**The ESP32-P4 has no electrical connection to the LoRa module at all.** Confirmed by badge.team's
ESP32-C6 pinout page (IO0=SCK, IO1=CS, IO2=MOSI, IO3=MISO, IO4=DIO1, IO5=BUSY, IO10=RESET).

Neither vendor's prose says this. Both describe LoRa as a device feature without naming the
controlling processor, and the Tanmatsu specifications page discusses the LoRa module immediately
after the application processor, which invites the wrong inference.

**Consequences:**

- LoRa application code runs on the **ESP32-C6**, not the P4 — which explains why
  [`tanmatsu-meshtastic-radio`](https://github.com/Nicolai-Electronics/tanmatsu-meshtastic-radio)
  is a fork of Meshtastic that *"requires manual recovery"*: it must replace the C6's radio firmware.
- Anything the P4 wants from LoRa must cross the SDIO/`esp-hosted` link.
- Reflashing the C6 radio firmware puts LoRa out of action too, not just Wi-Fi/BLE.

**Status: resolved** (corrected in [`README.md`](README.md) and [`pinouts-and-buses.md`](pinouts-and-buses.md)).

## 20. NEW — there is an infrared LED, documented nowhere in prose

`U21` = **`IR968-8P(X1-X4)XBY`**, a through-hole infrared LED (BOM, LCSC `C17179483`), driven from
**ESP32-C6 `IO15`** (module pin 23, net `IR_LED`) through `R64` = 52.3 Ω.

It appears in badge.team's ESP32-C6 pin table as *"Infrared LED Control"* and in the BOM, but **no
feature list, specification page or marketing description mentions infrared at all**. No app in the
57-app repository uses it.

This is a genuine undocumented capability — the device can act as an IR remote control. Note it is
**transmit only**; no IR receiver is fitted.

**Status: open** — capability confirmed from two independent primary sources, never tested.

## 21. NEW — undocumented test points and a DNP SAO header

From the fabrication netlist, absent from all documentation:

- **`TP18`–`TP21`** on `I2S_MCLK`, `I2S_SCLK`, `I2S_LRCK`, `I2S_DATA` — four I2S probe points that
  make audio bring-up much easier than the docs suggest
- **`TP8`** on `VBATT`
- **`J13`–`J16`** — the unpopulated sensor header (`+3.3V`, `INT_SDA`, `INT_SCL`, `GND`) for the
  optional SCD4x
- **`J3`** — a **6-pin SAO header footprint present in the netlist but absent from the BOM**, i.e. a
  do-not-populate position. Anyone diffing BOM against netlist will trip over this.

**Status: open**, observational.


## 22. NEW — `frontpanel.step` is exported at the wrong board thickness

The front-panel STEP model measures **1.63 mm** thick (`tools/step_bbox.py`), but the repository's own
README instructs fabrication at **0.8 mm**:

> *"When manufacturing these boards select **0.8mm** board thickness, ENIG surface finish and Remove Mark."*

1.63 mm is KiCad's **default** board thickness, so the model was almost certainly exported without
setting the intended value. Anyone using `frontpanel.step` for case fitment will model a panel
**twice as thick** as the one they receive.

**Status: open**, not reported upstream.

## 23. NEW — `tanmatsu.step` extends beyond the case length

Measured extents: mainboard model **114.90 × 142.40 mm**, front panel **114.90 × 129.94 mm**, case
**120 × 135 mm**. The mainboard model is **12.46 mm longer in Y than the front panel** and **7.4 mm
longer than the case**.

Most likely a protruding feature — the SMA antenna connector or an antenna pigtail — rather than the
PCB outline. **Unconfirmed**; resolving it requires opening the model in CAD, which was not possible
here (FreeCAD unavailable).

**Status: open.**

## 24. Mainboard PCB dimensions are not published

Neither vendor states the **mainboard PCB** size — only the case (120 × 135 × 18 mm). The ~114.9 mm
width in [`pricing-and-dimensions.md`](pricing-and-dimensions.md) is **derived from CAD**, not quoted,
and is flagged as such wherever it appears.

**Status: open** (vendor gap, worked around).

## 25. Spare-part listing does not say whether the dome sheet is included

The webshop lists *"Keyboard for Tanmatsu"* at **€4.96**. The KeebDeck keypad **requires** its adhesive
metal dome sheet to function at all ([`keyboard.md`](keyboard.md)), and the vendor previously promised
*"the keyboard **and corresponding metal dome sheet**"* as spare parts. The listing does not state
whether the sheet is included.

**Status: open** — ask before ordering.


## 26. NEW — published ESP-IDF and AppFS versions are stale

| Source | Claim | Reality (launcher `20022fce`) |
|---|---|---|
| Vendor docs / [`development.md`](development.md) | ESP-IDF **5.3+** | **`idf: ">=6.0.2"`** |
| Vendor docs | `badgeteam/appfs^1.0.0` | **`badgeteam/appfs =2.1.0`** |

Commit `db589fd` is literally *"Build with ESP-IDF v6.0.2"*. Following the published setup guide will
not build the current launcher. Flagged inline in [`development.md`](development.md).

**Status: open** (documentation lag, not a contradiction in the hardware).

## 27. NEW — the published flash layout is wrong in two places

The vendor flash-layout page versus the actual `partition_tables/esp32p4-16mb.csv`:

| Region | Docs say | Actually |
|---|---|---|
| `0x9000`–`0x18FFF` | *"Unused"* | **`coredump`, 64 KB** |
| `0x1D000`–`0x1FFFF` | OTA data, 12 KB | **`otadata` 8 KB + `phy_init` 4 KB** |

Neither is dangerous — the offsets that matter for flashing are unchanged — but "unused" is wrong,
and anyone sizing a custom partition table from the documentation would clobber the coredump area and
the RF calibration data. AppFS is additionally a **custom partition type `0x43`, subtype `3`**, which
standard tooling will not name.

**Status: resolved here**, open upstream.

## 28. NEW — an entire plugin system is undocumented publicly

The launcher ships an **840-line plugin API reference** (`docs/PLUGINAPIS.md`, API **v2.0.0**,
2026-02-14) describing dynamically-loaded **ELF plugins** with menu/service/hook types, ~40 `asp_*`
API functions, and nine system event hooks. **None of this appears on the documentation site or in
any vendor-facing material.**

It is `default n` and ESP32-P4-only, so it is plausibly considered unreleased — but the API is
versioned, the host rejects mismatched plugins, and the loader components are pinned dependencies.

**Status: open.** No example plugins were found in any official repository.

## 29. NEW — AppFS is a cache tier, not the app storage limit

The documentation presents AppFS as where apps live. The launcher treats it as a **working-set cache**
in front of FAT storage, with **LRU eviction** (`app_mgmt_appfs_evict_lru`), promotion
(`ensure_in_appfs`), demotion (`copy_appfs_to_install_dir`) and four locations
(`/int/apps`, `/sd/apps`, `/int/plugins`, `/sd/plugins`).

Practical effect: the 8 MB AppFS partition bounds how many apps can be *resident*, not how many can be
*installed*. Total capacity is AppFS + 3.9 MB internal FAT + SD card.

**Status: resolved here**, undocumented upstream.

## 30. NEW — the E22 LoRa module contains either an SX1262 or an SX1268

`main.c` branches on `status.chip_type == LORA_PROTOCOL_CHIP_SX1268` and logs which was found. So the
Ebyte E22 modules fitted are **not a single fixed Semtech part**, and firmware adapts at runtime.

Neither vendor mentions this. It matters if you intend to drive the radio directly or port
Meshtastic/MeshCore, since SX1262 and SX1268 differ in supported frequency range.

**Status: open** — observed in firmware, not confirmed against Ebyte documentation.

## 31. NEW — P4 and C6 firmware are version-coupled

The launcher pins the expected radio firmware to **`"v3.4.0"`** by exact string comparison and raises
a mismatch warning otherwise. It also pushes **board revision and country code** from P4 eFuses into
the radio whenever they disagree — so regulatory region propagates P4 → C6 at boot.

Upgrading one processor's firmware without the other will produce a mismatch warning.

**Status: observational.**


## 32. NEW — an undocumented plugin SDK, permission model and FUSE tool exist

Investigating how plugins are *built* surfaced three further undocumented pieces:

**A plugin SDK** ships inside the launcher at `tools/plugin-sdk/` — `plugin-build.cmake`,
`toolchain-plugin.cmake`, `plugin.ld`, `lib/libplugin_stubs.c` and a README. Plugins are **not** built
with `idf.py`; they are cross-compiled as `-fPIC -shared -nostdlib` RISC-V shared objects and linked
with a custom script that forces `.plugin_info` first. Full detail in
[`apps-vs-plugins.md`](apps-vs-plugins.md).

**A permission model.** `plugin.json` carries `"permissions": ["audio", "storage"]` alongside `type`,
`api_version` and `autostart`. **Nothing in the 840-line `PLUGINAPIS.md` mentions permissions**, and
whether they are enforced or merely declarative was **not determined**.

**`badgefs`** — a FUSE filesystem that mounts the device over USB (`badgefs /tmp/mnt`, `badgefs -u`),
used by community plugin Makefiles to install by file copy. Almost certainly built on BadgeLink's
filesystem operations. Documented nowhere official; appears as `nullislandspace/tanmatsu-badgefs`.

**Also inconsistent:** the plugin SDK README says **ESP-IDF v5.x**, while the launcher requires
**≥6.0.2**. The SDK only borrows the RISC-V toolchain rather than ESP-IDF's build system, so v5.x may
genuinely be sufficient — but the two documents disagree and neither was tested.

**Status: open.**


## 33. RESOLVED — `plugin.json` permissions are not enforced (and mostly not parsed)

Traced in `plugin_manager.c`. The function `parse_plugin_metadata()` is commented:

```c
// Read plugin.json for runtime fields (type, api_version, autostart, permissions)
```

but parses **only `type`**. `permissions`, `api_version` and `autostart` are never read from
`plugin.json`. **There is no permission enforcement in the launcher.**

What *is* validated, all from inside the ELF: the `"TMSP"` magic (`0x544D5350`), `struct_size`
(larger than the launcher's struct → rejected), and **API major version** from `get_info()`.

So the loader defends against the wrong file and the wrong API version, not against a malicious
plugin. Full detail in [`apps-vs-plugins.md` §11](apps-vs-plugins.md).

## 34. RESOLVED — `interpreter` / `script` app types are implemented

Earlier recorded as "keys exist, no user found". `menu/apps.c` implements them: a script app names an
**interpreter by slug**, the launcher ensures that interpreter is resident in AppFS, then calls
`appfsBootSelect(interpreter_fd, script_path)` and reboots. The interpreter gets its own LRU
timestamp so it cannot evict itself.

Script apps therefore need **no compiler** — but still cost a reboot, like any AppFS app.
See [`apps-vs-plugins.md` §8](apps-vs-plugins.md).

## 35. RESOLVED — the launcher and AppFS are not P4-specific, and need no companion chip

The launcher ships build configurations for **ESP32, ESP32-S3, ESP32-P4, ESP32-S31 and `linux`**, and
AppFS partition tables exist for ESP32 (MCH2022), S3, S31 and P4 — plus an explicit
`esp32s3-8mb-noappfs.csv` for boards without it.

**MCH2022 and Kami are single-chip ESP32 devices**, so the dual-chip arrangement is a *Tanmatsu
hardware* consequence of the ESP32-P4 having no radio — not a software requirement.

Genuinely P4-only: **plugins** (`badge-elf`/kbelf, `default n`), `rvswd` coprocessor flashing and the
on-device `esptool`. Full breakdown in [`portability.md`](portability.md).

## 36. RESOLVED — case fasteners and model structure

Extracted from `Tanmatsu_3D-printed.FCStd` by treating it as a ZIP and reading `Document.xml`
(FreeCAD unavailable): the case uses **7 × M2×12 screws and 7 × M2 nuts**, with captive-nut pockets
(`space_for_nuts`). Dominant pad extrusion is **5.0 mm**. The model also reveals **`keycord_holes`**
(lanyard) and a combined **`space_LORA_USB-A`** cut-out.

True wall thickness and tolerances still require CAD — the XML gives features and extrusion depths,
not resolved boolean geometry. See [`mechanical-and-case.md`](mechanical-and-case.md).


## 37. RESOLVED — AppFS has no permission model, in any version

The current AppFS component (`badgeteam/esp32-component-appfs` @ `eee29be`, 2026-08-25) contains
**no signing, capability, sandbox or permission mechanism**. Searching the whole component for
`permission|capabilit|sandbox|privile|signature|verify` yields only a `strnlen` bounds check on the
boot argument, an fd-validity check, stock `esp_partition_table_verify()`, and the word "permissions"
in the Apache-2.0 header.

Combined with [§33](#33-resolved--pluginjson-permissions-are-not-enforced-and-mostly-not-parsed) — the
launcher not parsing `plugin.json` permissions — **there is no permission enforcement anywhere in the
Tanmatsu software stack.**

## 38. RESOLVED — how the device chooses launcher vs app, and whether the launcher is "included"

`appfsBootSelect(fd, arg)` writes a magic-tagged record (`0x2af7de4a994f7236`) into **RTC retained
memory**; the patched bootloader reads it on the next boot. If absent or invalid it boots normally —
*"No AppFS app selected or failed to open app, starting launcher"*. If valid, it **substitutes the
AppFS partition into OTA slot 0** and lets stock ESP-IDF boot code load the selected file through a
flash-read wrapper.

The selection is **one-shot**: `bootsel->valid = false` is written *before* the app is loaded, so a
crashing app cannot trap the device and a plain reboot always returns to the launcher.

**The launcher is not "included" in AppFS.** It is ordinary firmware in `ota_0` and is the default
boot target; AppFS is a separate partition the bootloader is redirected into. Full detail in
[`badgelink-and-appfs.md` §12](badgelink-and-appfs.md).

## 39. AppFS target support is far wider than documented

The component declares **ten targets** — `esp32, esp32s3, esp32c6, esp32p4, esp32c5, esp32c3,
esp32c61, esp32h2, esp32s31, esp32c2` — against documentation claiming only ESP32/C6/P4 with
*"other ESP32 variants are not supported yet"*. **Stale documentation**, not a conflict.

---

## 40. Netlist-derived hardware constraints not previously recorded

Added 2026-08-30 from component-level audits of `tanmatsu.kicad_pcb` (pad→net parsing) read against
each part's datasheet. Each of these limits what firmware can do, and none was stated device-side.

### 40.1 BQ25895 `D+`/`D−` are unconnected — USB source detection cannot work

[SCH] The PMIC's USB data pins terminate at no net. BC1.2 / HVDCP / MaxCharge negotiation therefore
**cannot function**, and `VBUS_STAT` is uninformative regardless of what the register returns. The
coprocessor firmware nonetheless exposes setters for all of it. Input current must be set by policy,
not by detection. See [BQ25895](../../../components/texas-instruments/bq25895/README.md).

### 40.2 BQ25895 `TS` is a fixed divider — battery temperature protection is defeated

[SCH] `TS` sits on a 10 k/10 k divider with **no thermistor**. The resulting 50 % sits only
~1.25–2.25 pp above the 48.25 % hot-trip threshold, so the margin is thin as well as meaningless.

### 40.3 Charge-current ceiling is ~1.36 A, not the 1.5 A the vendor header claims

[SCH][DOC] `ILIM` = 261 Ω. 1.5 A assumes the *maximum* K_ILIM; typical is ≈1.36 A and worst case
≈1.23 A.

### 40.4 BMI270 interrupts reach no processor — the IMU must be polled

[SCH] `INT2` is unconnected; `INT1` terminates at a 4.7 kΩ pull-up and test point `TP22`. The BSP
calls `bmi2_map_data_int()` twice against pins that go nowhere (and the second call overrides the
first, both mapping `BMI2_DRDY_INT`). **Any interrupt-driven IMU design will not work on this board.**
See [BMI270](../../../components/bosch-sensortec/bmi270/README.md).

### 40.5 TPS63020 power-save is permanently disabled

[SCH] `PS/SYNC` is tied to `EN`, forcing fixed-frequency PWM at 2.4 MHz at all loads — on a
battery-powered device. This costs quiescent efficiency at light load in exchange for lower output
ripple and no mode-transition noise. Whether that trade was deliberate is **unresolved**.

### 40.6 TPS63020 `VINA`/`EN`/`PS/SYNC` form an isolated net — UNRESOLVED

[SCH] The parsed netlist shows these three pins joined to each other and to a single 100 nF cap, with
no path to a supply rail. Taken literally the converter could never be enabled, so this is more likely
a netlist-extraction artefact than a real defect. Needs the rendered schematic or hardware continuity
to settle. Recorded rather than explained away.

### 40.7 SK6805 RGB LEDs run from `VOTG` — they need the PMIC boost enabled

[SCH] The six addressable LEDs are fed from the 5 V OTG rail, not a always-on rail. **The PMIC boost
converter must be running before the LEDs will light**, which couples an apparently cosmetic feature
to power-path state.

### 40.8 E22 `DIO2` drives `RXEN` through an inverter, defaulting to receive

[SCH] `DIO2` → `74LVC1GU04` inverter → `RXEN`, with a 100 kΩ pull-down. The design is correct, but
firmware **must** call `SetDio2AsRfSwitchCtrl` or the board will receive and never transmit — a
silent, easily-misdiagnosed failure. See [E22-900M22S](../../../components/ebyte/e22-900m22s/README.md).
