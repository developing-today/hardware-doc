# Hardware subject guides

Cross-cutting guides about **hardware subsystems** rather than about a vendor, a chip family or a
market. They compile knowledge that is spread across several [component](../../components/README.md)
and [device](../../devices/README.md) records into a single treatment of the subject.

| Guide | What it covers |
|---|---|
| [**E-paper displays**](e-paper-displays.md) | How electrophoretic displays work — waveforms, LUTs, greyscale, ghosting and why periodic full refreshes are forced. Why a bare panel needs a multi-rail PMIC and a hardware power sequencer. **VCOM and why it is per-panel-lot.** Partial vs full vs greyscale trade-offs with real timings. Temperature dependence, and the gap between the sensor that exists and the sensor that is used. Burn-in and lifetime. **The NDA problem: exactly what is and is not publicly establishable about an E Ink panel.** Practical guidance for driving one |
| [**Display interfaces**](display-interfaces.md) | SPI vs QSPI vs i80/RGB parallel vs MIPI-DSI vs e-paper parallel — when each is used, who owns the frame, and bandwidth arithmetic from real figures. The ESP32 family's LCD peripheral support per chip. **Framebuffer and PSRAM sizing with worked cases.** Tearing, TE lines and what happens when TE is not routed. LVGL integration and buffer sizing. **A table of every display controller in the library**, with and without a component record |
| [**Parallel Intel-8080 LCD buses on ESP32**](parallel-8080-lcd-buses.md) | Why the display-library choice matters more than the board: 8080 vs RGB vs QSPI, the `TFT_eSPI`/`Arduino_GFX`/`LovyanGFX` decision, the `User_Setup_Select.h` trap, GRAM offsets, and a black-screen debugging checklist. Companion to [`display-interfaces.md`](display-interfaces.md). *Added 2026-09-07* |
| [**LoRa radio generations**](lora-radio-generations.md) | **The four generations of Semtech LoRa transceiver silicon.** What "the 4th generation LoRa chip" is and where the numbering comes from (Semtech's own `DS.LR20xx` §23.8); a like-for-like feature/electrical/host-interface matrix across SX127x, SX126x, SX128x, LR11xx and LR20xx; and **what breaks when you migrate**, at the level of "here is what your driver has to change". *Added 2026-09-04* |
| [**Adding LoRa, NFC and an RGB sidelight to e-ink firmware**](adding-lora-nfc-and-sidelight-to-eink-firmware.md) | What it actually takes to bolt a radio, an NFC front-end or an addressable light onto an existing e-ink reader firmware. Per capability: free-pin and interrupt prerequisites, what an e-paper refresh does to the power rail, the driver options (RadioLib, Semtech `sx126x_driver`/`lr20xx_driver`, Meshtastic, ST25R3916, PN532/RC522, RMT/`led_strip`) with licence and footprint, and flash/RAM cost. **Ends with a plugin-versus-fork verdict per capability** for CrossPoint Reader, FreeInk and CrossPlay, cited to the plugin ABI's exported-symbol list. **Nothing here was built or flashed.** *Added 2026-09-07* |
| [**SoC choice for battery e-ink devices**](soc-choice-for-battery-eink-devices.md) | Why these boards pick what they pick — ESP32-C3 vs ESP32-S3 vs ESP32-P4 vs Kendryte K230 vs nRF52/nRF9151 for a battery-powered e-ink handheld. PSRAM against framebuffer size, deep-sleep current, radio duty cycle, toolchain maturity and the price consequence. Every figure is cited to the component record it came from; missing figures are named as missing rather than estimated. *Added 2026-09-07* |

---

## Conventions

These guides follow the [repository evidence labels](../README.md#conventions) — **[DOC]** vendor
document · **[SCH]** schematic · **[SRC]** source code · **[WEB]** vendor web page · **[COM]**
community report · **[INF]** inference — applied transitively from the records they cite.

Because they **synthesise rather than research**, each ends with an explicit **evidence boundary**
section stating what is inherited and what is new. **Where a guide disagrees with a linked deep
record, the deep record wins.**

Both guides were compiled **2026-08-30** with **no new retrieval and no hardware access**, which is
consistent with every record they draw on: nothing in this library has been tested on a physical
board.

## Related

- [Guides index](../README.md) · [Espressif guides](../espressif/README.md) · [Markets and sourcing](../markets/README.md)
- [Device comparison matrix](../markets/device-comparison-matrix.md) — the display, power and input columns across every documented device
- [Component index](../../components/README.md) · [Device index](../../devices/README.md)

---

## Recovering the facts these guides rely on — *added 2026-09-11*

Every guide here cites pinouts, bus widths and controller choices that came out of a **schematic**.
Two companion guides cover how those schematics get read when the vendor publishes no netlist:

- [**Recovering netlists from vendor EDA files**](../reverse-engineering/netlists-from-vendor-eda-files.md)
  — the preferred route whenever KiCad or EAGLE sources exist. Parse the `.kicad_pcb`, not the
  `.kicad_sch`.
- [**Tracing nets from schematic PDFs**](../reverse-engineering/tracing-nets-from-schematic-pdfs.md)
  — **when a PDF is all there is.** Altium exports embed invisible `CO` / `PI` / `NL` marker
  tokens at item coordinates, which makes a net list recoverable from the text layer alone.
  ⚠ **KiCad and EAGLE exports frequently outline their text to vector paths**, yielding zero
  extractable words and a permanently untraceable file — check before concluding a design is
  undocumented, because a usable second export often sits in the same directory.

The display and e-paper claims in these guides are exactly the kind that method settles: the
[**parallel Intel-8080**](parallel-8080-lcd-buses.md) bus widths and the panel-controller
identifications in [**display interfaces**](display-interfaces.md) are schematic facts, and five
device records now carry a `schematic-netlist.md` derived this way — see
[`devices/README.md`](../../devices/README.md#two-new-per-record-file-types--added-2026-09-11).

A third guide covers the *other* non-vendor evidence route these pages increasingly depend on:
[**finding certification records**](../research/finding-certification-records.md). FCC internal
photographs establish antenna type, battery capacity and package-level construction for boards
whose vendors publish nothing — which is where the
[KH3216-A35 antenna record](../../components/generic/kh3216-a35-chip-antenna/README.md) came from.
