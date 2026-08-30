# Solder Party

> Vendor guide — who they are, what they make, how their documentation and repositories are organised, and the traps.
> Snapshot **2026-08-24**.

**Solder Party AB** is a small open-hardware company based in **Malmö, Sweden**, run by **arturo182**. All orders ship from the EU. They are best known for two things: **handheld keyboards** (BlackBerry-derived and, more recently, their own silicone keypad) and the **RP2xxx "Stamp"** castellated module family.

They matter for hardware research well beyond their own products, because their parts turn up *inside* other people's devices — most relevantly, the **Tanmatsu's keyboard is a Solder Party design** ([`../devices/nicolai-electronics/tanmatsu/keyboard.md`](../../devices/nicolai-electronics/tanmatsu/keyboard.md)).

---

## Where to find things

| Resource | URL | Notes |
|---|---|---|
| Main site | <https://www.solder.party/> | Thin — mostly a signpost |
| **Documentation** | **<https://www.solder.party/docs/>** | The real content. `docs.solder.party` redirects here |
| GitHub org | <https://github.com/solderparty> | 31 public repos |
| Shop | [Lectronz](https://lectronz.com/) | Not their own storefront |
| Bluesky | <https://bsky.app/profile/solder.party> | Product announcements |
| Discord | linked from the main site | Support |
| RSS | `https://www.solder.party/docs/index.xml` | Useful for change detection |

### Documentation URL pattern

The docs site is a **Hugo** static site with clean, stable, guessable paths:

```
https://www.solder.party/docs/<product>/
https://www.solder.party/docs/<family>/<variant>/
```

Examples: `/docs/bbq20kbd/`, `/docs/keebdeck/keyboard/`, `/docs/keyboard-featherwing/rev2/`, `/docs/rp2350-stamp-xl/`.

**It is server-rendered HTML** — plain `curl` with no special headers returns full content, and text extraction works. No JavaScript shell, no bot blocking observed on 2026-08-24. This is a pleasant contrast to `tanmatsu.cloud`, which is an SPA that returns nothing useful.

Each product page carries a consistent set of sub-sections, usually including **Technical details**, **Example Code**, **Downloads**, **License Information**, and often **Dimensions** and a **Block Diagram**. Pages are dated with a "Last modified" line, which is useful for judging staleness.

### Repository naming convention

Highly regular, and worth knowing so you can guess:

| Suffix | Meaning |
|---|---|
| `_hw` | Hardware design — KiCad sources, symbols, footprints |
| `_sw` | Software |
| *(none)* | Firmware or library |

So `bbq20kbd_hw`, `keebdeck_keyboard_hw`, `rp2350_stamp_hw`, `flexypin_adapters_hw` are all design files, while `i2c_puppet` is firmware.

---

## Product lines

### Keyboards — the BlackBerry line

Boards carrying salvaged/sourced **BlackBerry** phone keyboards, with an on-board MCU presenting an **I2C peripheral** interface.

| Product | Keyboard | MCU | Interfaces |
|---|---|---|---|
| **Keyboard PMOD** | BB **Q10** | ATSAMD20 | I2C, PMOD |
| **BBQ20KBD** | BB **Q20** + optical trackpad | **RP2040** | I2C, **USB HID**, PMOD, Qwiic; injection-moulded clear case |
| **Keyboard FeatherWing Rev 1 / Rev 2** | BB Q10 | *none* | Adafruit Feather form factor; Rev 2 adds a 2.6" 320×240 touch LCD, 5-way + 4 buttons, NeoPixel, ambient light sensor, microSD, Qwiic |
| **PMOD to Qwiic Adapter** | — | — | connector adapter |

Firmware: **[`i2c_puppet`](https://github.com/solderparty/i2c_puppet)** (117★, MIT) for the RP2040 generation, a port of the older **[`bbq10kbd_i2c_sw`](https://github.com/solderparty/bbq10kbd_i2c_sw)**. Critically, **the register map is backwards compatible**, so every host library works with both generations.

Full protocol documentation and register map: [`../devices/nicolai-electronics/tanmatsu/keyboard.md` §3](../../devices/nicolai-electronics/tanmatsu/keyboard.md#3-the-blackberry-keyboards-bb-q10--q20).

⚠ **BBQ20KBD is not 5 V tolerant.**

### Keyboards — the KeebDeck line

Solder Party's own design, replacing the BlackBerry dependency with a manufactured part.

| Product | What it is |
|---|---|
| **KeebDeck Keyboard** | 69-key **silicone keypad + adhesive metal dome sheet**, 85 × 48 mm. **A bare component** — no PCB, no MCU, no interface |
| **KeebDeck Basic** | Evaluation / reference board for the above |

Repos: [`keebdeck_keyboard_hw`](https://github.com/solderparty/keebdeck_keyboard_hw) (47★), [`keebdeck_basic_hw`](https://github.com/solderparty/keebdeck_basic_hw) (40★) — footprints and drawings for popular EDA tools.

**Customisation of the laser-etched key labels is offered at 500+ units**, which is how devices like Tanmatsu get bespoke legends.

### RP2xxx Stamp modules

Castellated system-on-module parts, plus carriers.

| Product | Notes |
|---|---|
| RP2040 Stamp | [`rp2040_stamp_hw`](https://github.com/solderparty/rp2040_stamp_hw) (187★) |
| RP2350 Stamp | [`rp2350_stamp_hw`](https://github.com/solderparty/rp2350_stamp_hw) |
| **RP2350 Stamp XL** | [`rp2350_stamp_xl_hw`](https://github.com/solderparty/rp2350_stamp_xl_hw) (43★) |
| Carriers | RP2040 Stamp Carrier, RP2xxx Stamp Carrier Basic / XL, Round Carrier |
| Footprints | [`rp2xxx_stamp_footprints`](https://github.com/solderparty/rp2xxx_stamp_footprints) (87★) |

Also [`esp32p4_stamp_xl_usb_uart_bridge`](https://github.com/solderparty/esp32p4_stamp_xl_usb_uart_bridge) — evidence of an **ESP32-P4 Stamp XL**, the same SoC as Tanmatsu.

### FlexyPin

[`flexypin`](https://github.com/solderparty/flexypin) (118★) — spring-pin sockets for mounting castellated modules **without soldering**, with [`flexypin_adapters_hw`](https://github.com/solderparty/flexypin_adapters_hw) (55★). Genuinely useful for prototyping with any castellated module, not just theirs.

### USB Type-C and power

USB Type-C Plug Breakout (USB 2.0 and 3.0), USB Type-C Plug SMT Pack, CP2102 USB-to-Serial/UART, USB-C LiPo Battery Charger, [`lipo_disconnector_hw`](https://github.com/solderparty/lipo_disconnector_hw), [`type-c_plug_lipo`](https://github.com/solderparty/type-c_plug_lipo).

### Others and reference designs

**Serpente R1 / R2** (tiny SAMD21 boards), **OLED PMOD**, **PCB Holder Ruler**, **TSC2004** touch controller libraries for [Arduino](https://github.com/solderparty/arduino_tsc2004) and [CircuitPython](https://github.com/solderparty/arturo182_CircuitPython_tsc2004).

**Flux Projects** — open reference designs at `/docs/flux/`: **Handheld Console**, **MacroPad**, **Photo Light**. Corresponding repos `rp2040_stamp_console_hw`, `rp2040_stamp_macropad_hw`, `rp2040_stamp_photolight_hw`.

---

## Host libraries for the keyboards

Solder Party maintain some and link others. All work across Q10 and Q20:

| Language | Project | Maintainer |
|---|---|---|
| Arduino | [`arduino_bbq10kbd`](https://github.com/solderparty/arduino_bbq10kbd) | Solder Party |
| CircuitPython | [`arturo182_CircuitPython_BBQ10Keyboard`](https://github.com/solderparty/arturo182_CircuitPython_BBQ10Keyboard) | Solder Party |
| Rust (embedded-hal) | [`bbq10kbd` crate](https://crates.io/crates/bbq10kbd) | third party |
| Linux userspace driver | [`wallComputer/bbqX0kbd_driver`](https://github.com/wallComputer/bbqX0kbd_driver/) | third party |
| Linux kernel module | [`billylindeman/bbq10kbd-kernel-driver`](https://github.com/billylindeman/bbq10kbd-kernel-driver) | third party |

---

## Research notes and traps

**Two unrelated keyboard families share the vendor name.** The most common error when researching Solder Party keyboards is conflating the **KeebDeck** (passive silicone keypad, no electronics) with the **BB Q10/Q20 boards** (self-contained I2C devices). Advice written for one is actively wrong for the other. Always establish which you are dealing with first.

**"Keyboard PMOD" and "BBQ10" refer to the same product** in different places — the docs page is `/docs/keyboard-pmod/`, but the firmware repo, protocol and libraries are all named `bbq10kbd`. Search both terms.

**`i2c_puppet` supersedes `bbq10kbd_i2c_sw`** but the older repo is still the canonical reference for the *original* ATSAMD20 board's history. The README of `i2c_puppet` points at it for version history.

**Do not do a recursive submodule init on `i2c_puppet`.** It vendors the Pico SDK, which vendors TinyUSB, which has many submodules. The project README specifies a two-step non-recursive init instead.

**Several registers documented in `i2c_puppet` are "Currently not implemented"** — `REG_DEB` (debounce), `REG_FRQ` (poll frequency), `CFG_PANIC_INT`, `INT_PANIC`. They exist in the map but do nothing. Do not design around them.

**Interrupt status registers must be manually cleared.** `REG_INT` (0x03) and `REG_GIN` (0x10) do not self-clear on read — you must write `0x00` back. Missing this produces a device that appears to interrupt once and then stop.

**`REG_ADR` changes the I2C address immediately and is not persisted.** Write it and your very next transaction must use the new address; a power cycle reverts to `0x1F`.

**Star counts are a poor guide to importance here.** `i2c_puppet` (117★) is the firmware that makes `bbq20kbd_hw` (219★) work, and `keebdeck_keyboard_hw` (47★) is the part shipping inside Tanmatsu. Hardware repos attract stars; firmware repos are what you actually need.

**Licensing is consistently permissive but check per-repo.** `i2c_puppet` is MIT (© 2022 Solder Party AB). Hardware repos generally carry open licences, and the docs site has a **License Information** section per product — read that rather than assuming.

---

## Retrieval notes

Verified **2026-08-24**:

- Plain `curl` with a normal browser User-Agent returns full server-rendered HTML from `www.solder.party/docs/*`. No 403, no bot-block, no JS shell.
- `docs.solder.party` → 301 → `www.solder.party/docs/` (same content, same byte size).
- The GitHub org is fully public; `git clone --depth 1` works without authentication.
- The docs index (`/docs/`) lists **every** product with links, so it is a reliable enumeration point — no sitemap parsing needed.

---

## Devices in this tree using Solder Party parts

| Device | Part |
|---|---|
| [Nicolai Electronics Tanmatsu](../../devices/nicolai-electronics/tanmatsu/README.md) | **KeebDeck Keyboard** (69-key silicone keypad + dome sheet), designed by Solder Party |

## Related

- [`../devices/nicolai-electronics/tanmatsu/keyboard.md`](../../devices/nicolai-electronics/tanmatsu/keyboard.md) — full keyboard documentation including the complete `i2c_puppet` register map
- [`../README.md`](../README.md) — vendor guide index
