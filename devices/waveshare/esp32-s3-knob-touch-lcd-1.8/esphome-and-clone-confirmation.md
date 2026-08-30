# ESPHome support, and confirmation the Guition clone is the same design

> Found **2026-08-26** by GitHub code search on the product name — the technique in
> [`guides/research/finding-projects-that-use-a-board.md`](../../../guides/research/finding-projects-that-use-a-board.md).
> Source: [`esphome/devices.esphome.io`](https://github.com/esphome/devices.esphome.io),
> `src/docs/devices/ESP32S3-1.8-inch-JC3636K518C/index.md`, published **2025-08-22**.
>
> Local copy: `../hardware-doc-archive/scratch/esp32-s3-knob-touch-lcd-1.8/community-probe/`

## The finding

ESPHome's device catalogue carries a page for the **Guition JC3636K518C** — the red AliExpress
knob — and states plainly:

> *"A blue version is available from [Waveshare](https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm)."*

It ships a **complete working ESPHome configuration**. Comparing its pin assignments against this
record's schematic-derived pinout:

| Function | ESPHome (JC3636K518C) | This record (Waveshare) | Match |
|---|---|---|---|
| I²C SDA / SCL | `sda: 11`, `scl: 12` | GPIO11 SDA, GPIO12 SCL | ✅ |
| Display QSPI clock | `clk_pin: 13` | GPIO13–18 | ✅ |
| Display data | `data_pins: [15, 16, 17, 18]` | GPIO13–18 | ✅ |
| Display CS | `cs_pin: 14` | GPIO13–18 | ✅ |
| Display reset | `reset_pin: 21` | reset 21 | ✅ |
| Touch interrupt | `interrupt_pin: GPIO9` | GPIO9 `TP_INT` | ✅ |
| Touch reset | `reset_pin: GPIO10` | GPIO10 `TP_RST` | ✅ |
| PDM microphone | `i2s_lrclk_pin: GPIO45`, `i2s_din_pin: GPIO46` | GPIO45/46 PDM RX | ✅ |

**Every pin matches.** Eight independent assignments, derived by a different party from a
differently-branded board.

## What this resolves

The device index previously said of the Guition JC3636K518:

> *"documented — as far as the evidence allows — in clones-and-variants.md §5. It is not a separate
> device record here because we have not handled one."*

That caution was right, but the relationship is now much better evidenced. **The Guition
JC3636K518C and the Waveshare ESP32-S3-Knob-Touch-LCD-1.8 share a pin-identical hardware design.**
The differences appear to be cosmetic and commercial — red versus blue enclosure, AliExpress at
~$25 versus Waveshare's listing.

That is a stronger claim than "similar boards", and it is now backed by eight matching pins rather
than appearance.

### What it does *not* prove

- **Not proof of identical silicon.** Flash/PSRAM part numbers, display panel batch and touch
  controller revision could still differ between vendors or production runs.
- **Not proof of identical firmware compatibility.** Matching pins make it likely, but factory
  firmware, partition layouts and bootloader configuration were not compared.
- **Nobody here has handled either board**, so this remains documentary evidence.

Treat it as: *the same reference design, sold by two vendors*. Verify part-level details before
depending on interchangeability.

## Specifications from ESPHome

| Item | ESPHome page | This record |
|---|---|---|
| Display driver | **ST77916**, 360 × 360 | ST77916 marketed; **software calls it SH8601** — see [gaps-and-conflicts](./gaps-and-conflicts.md) |
| Touch | CST816 | CST816D at `0x15` |
| CPU | **ESP32-S3 *and* ESP32** | Dual-MCU — [dual-mcu-architecture](./dual-mcu-architecture.md) |
| Flash / PSRAM | 16 MB / 8 MB | — |
| Price | **~$25 on AliExpress** | Waveshare listing is dearer |

The dual-MCU description independently corroborates this board's unusual ESP32-S3 + ESP32-U4WDH
arrangement, which is the single most confusing thing about it for newcomers.

> Note ESPHome says **360 × 360** while the product is marketed as 1.8-inch. Both can be true —
> one is resolution, the other diagonal — but the ESPHome page also calls it "1.85inch" in prose
> while the directory name says "1.8-inch". Minor inconsistency in their material, not ours.

## A third firmware path

This record documents ESP-IDF and Arduino. ESPHome is a **third**, and for a knob-with-display
destined for home automation it is arguably the most practical: the config is declarative YAML with
no C at all, and it drops straight into Home Assistant.

Worth evaluating before writing custom firmware for a dashboard use case. The full configuration is
in the ESPHome page and in the local copy.

## Reacquire

```bash
curl -sSL -o esphome-jc3636k518c.md \
  https://raw.githubusercontent.com/esphome/devices.esphome.io/main/src/docs/devices/ESP32S3-1.8-inch-JC3636K518C/index.md
```

Rendered: <https://devices.esphome.io/devices/ESP32S3-1.8-inch-JC3636K518C>

## Related

- [`pinouts-and-buses.md`](./pinouts-and-buses.md) — the pinout this corroborates
- [`clones-and-variants.md §5`](../../../guides/markets/clones-and-variants.md) — the Guition comparison
- [`dual-mcu-architecture.md`](./dual-mcu-architecture.md)
