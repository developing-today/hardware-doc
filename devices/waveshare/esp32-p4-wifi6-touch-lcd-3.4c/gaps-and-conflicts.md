# Gaps, conflicts and unresolved identities

> ESP32-P4-WIFI6-Touch-LCD-3.4C and 4C. Snapshot **2026-08-24**.
> Applies to both variants unless stated. Nothing here has been tested on hardware.

## C1 — microSD pin assignment — **RESOLVED 2026-08-24**

**Status:** **resolved by reading the schematic visually.** Superseded; kept for the record because
the reasoning matters.

### Resolution

| SD1 pin | Signal | GPIO |
|---:|---|---:|
| 1 | DAT2 | **41** |
| 2 | CD/DAT3 | **42** |
| 3 | CMD | **44** |
| 5 | CLK | **43** |
| 7 | DAT0 | **39** |
| 8 | DAT1 | **40** |
| — | **VDD power switch** (AO3401 P-MOSFET gate) | **45** |

Full detail: [`pinouts-and-buses.md`](./pinouts-and-buses.md#microsd--connector-sd1).

### What the original concern was, and why it was half right

The shipped `ESP-IDF/03_sdmmc` is **unmodified upstream Espressif code**. Its Kconfig sets
`CMD=44, CLK=43, D0=39` for `IDF_TARGET_ESP32P4` — values that describe Espressif's
**ESP32-P4-Function-EV-Board**, selected by *chip target*, not by any Waveshare board symbol.
Waveshare added no board-specific defaults and no `sdkconfig`.

That reasoning was sound, and the resulting caution was correct practice. **The conclusion was
wrong.** Those pins are right for this board — Waveshare followed Espressif's reference pin
assignment, so the generic defaults happen to match. The demo works by design convergence, not by
board-specific configuration.

The methodological lesson survives intact: *the demo was not evidence*. It only agreed with the
truth. Had Waveshare chosen different pins, the same file would have been confidently wrong, and
nothing in the archive would have said so.

### What is still genuinely missing

The demo **never drives GPIO45**, the microSD VDD power switch. The card sits on a rail gated by an
AO3401 P-channel MOSFET. A from-scratch project must enable that rail before `sdmmc` init.

### Complicated 2026-08-26 — the BSP uses a different mechanism entirely

The official BSP does **not** touch GPIO45. It powers the card through an **on-chip LDO**:

```c
sd_pwr_ctrl_ldo_config_t ldo_config = { .ldo_chan_id = 4 };
sd_pwr_ctrl_new_on_chip_ldo(&ldo_config, &pwr_ctrl_handle);
host.pwr_ctrl_handle = pwr_ctrl_handle;
```

Both can be true: the ESP32-P4 powers its SD **IO rail** from an internal LDO, while an external
P-MOSFET could gate the **card's VDD** separately. Different rails, different jobs.

But it is also possible the schematic reading is wrong, or that `SD1_VDD` is default-on and the BSP
simply relies on it. **Unresolved, and it matters** — if GPIO45 must be asserted and the BSP never
does, BSP-based SD access would fail on a fresh board.

**How to settle it:** trace `SD1_VDD` against the P4's `VDD_SDIO` pin, or test empirically — if
`bsp_sdcard_mount()` works without touching GPIO45, the BSP path is self-sufficient.

Also still unconfirmed:

- **GPIO45 polarity.** Inferred low-to-enable from P-MOSFET high-side topology.
- **Card-detect** (SD1 pin 9) destination — the BSP uses `SDMMC_SLOT_NO_CD`, so it is unused either
  way.



## C2 — 4C availability — **RESOLVED 2026-08-24**

**Status:** fully resolved. **The 4C is a normal, purchasable product.** My earlier conclusion was
wrong, and wrong in a way worth understanding.

### The answer

Waveshare sell **both variants under a single product listing**, chosen with a *Version Options*
selector. The page's own option data:

```json
[{"sku":"31523","attributes":["3.4inch Round Touch Display (800 × 800 pixels)"],"unsaleable":false},
 {"sku":"31522","attributes":["4inch Round Touch Display (720 × 720 pixels)"],"unsaleable":false}]
```

| SKU | Variant | Saleable |
|---|---|---|
| **31523** | ESP32-P4-WIFI6-Touch-LCD-3.4C, 800 × 800 | **yes** |
| **31522** | ESP32-P4-WIFI6-Touch-LCD-4C, 720 × 720 | **yes** |

Waveshare's own repository README states it plainly: *"Both variants are available from the same
product page; select the required model under **Version Options**."*

### Why I got it wrong

I searched for a **dedicated 4C product URL**, found `HTTP 404`, saw catalogue search return only
the 3.4C, and noticed the 4C wiki linking to the 3.4C store page. Every one of those observations
was accurate. The inference drawn from them was not.

They all have one mundane explanation: **there is no separate 4C page because there does not need
to be one.** The 4C wiki links to the 3.4C store page because that *is* the 4C's store page. The
catalogue returns one result because there is one listing.

The lesson: **absence of a product page is not absence of a product.** A 404 answers "does this URL
exist", not "can I buy this". The check that would have settled it immediately — reading the
purchase options on the listing I had already downloaded — was never run.

### What this also resolves

This closes [C6](#c6--purchase-options-for-the-34c--resolved-2026-08-24) as well: the five option
slugs and the `$64.99 – $74.99` span are the **two display variants**, not accessory bundles.

## C3 — PCB revision — **RESOLVED 2026-08-24**

**Status:** resolved. The board revision is **rev1.1**, stated in Waveshare's official
`docs/HARDWARE.md`.

It appears on neither the wiki, the store listing, nor the schematic title block — only in the
repository's hardware audit. All observations in this record therefore apply to **rev1.1**.

**Do not confuse this with the silicon profiles.** `rev1_3` and `rev3_x` appear throughout
Waveshare's build configuration and are **ESP32-P4 chip compatibility profiles, not PCB
revisions**. They select the DSI PHY clock reference — see
[C14](#c14--esp32-p4-silicon-revision-changes-the-dsi-phy-clock-source).

## C4 — DSI porch timings are not derived per panel

**Status:** observed, explained, not a defect. **Impact:** low, but a trap if you change timings.

Both variants use **identical** blanking intervals and an identical 1500 Mbps lane rate:

| | 3.4C | 4C |
|---|---|---|
| Active | 800 × 800 | 720 × 720 |
| hsync pw / bp / fp | 20 / 20 / 40 | **same** |
| vsync pw / bp / fp | 4 / 12 / 24 | **same** |
| Lane rate | 1500 Mbps | **same** |

An 11% difference in horizontal pixel count with unchanged blanking means the DSI link carries
more slack on the 4C. This evidently works — Waveshare ship it — but the timings were clearly not
computed per panel. **Inference:** they were derived once for the 800 × 800 panel and reused. If
you change pixel clock, colour depth, or refresh rate, re-derive rather than scaling these.

## C5 — Bundled third-party libraries — **RESOLVED 2026-08-24**

**Status:** resolved by direct diff against upstream. **Both libraries are stock.**

### Result

| Tree | Upstream | Differing files | Verdict |
|---|---|---:|---|
| `Arduino/libraries/lvgl` | LVGL **v9.3.0** | **0** | **Unmodified** |
| `Arduino/libraries/GFX_Library_for_Arduino` | Arduino_GFX **v1.6.0** | **0** | **Unmodified** |

```bash
curl -L -o lvgl-9.3.0.zip https://github.com/lvgl/lvgl/archive/refs/tags/v9.3.0.zip
curl -L -o gfx-1.6.0.zip  https://github.com/moononournation/Arduino_GFX/archive/refs/tags/v1.6.0.zip
unzip -q lvgl-9.3.0.zip && unzip -q gfx-1.6.0.zip
diff -rq lvgl-9.3.0            <demo>/Arduino/libraries/lvgl
diff -rq Arduino_GFX-1.6.0     <demo>/Arduino/libraries/GFX_Library_for_Arduino
```

**Not a single file's contents differ in either tree.** You can rebuild from stock upstream with
no patch step.

### The only deltas, all benign

**Arduino_GFX** — 2 paths present upstream, absent in the vendored copy: `.github`, `.gitignore`.
Packaging strip. Nothing else.

**LVGL** — 11 upstream paths stripped (`.devcontainer`, `.github`, `.gitignore` ×5,
`.pre-commit-config.yaml`, `.typos.toml`), plus two additions:

1. **`.vscode/settings.json`** — 66 bytes, one editor file association. Inert.
2. **`src/demos/`** — a ~30 MB copy of `demos/`, added so the Arduino IDE compiles the demos
   (Arduino only builds sources under `src/`). Same trick as the knob board's LVGL 8.4.0.

Within that copy exactly **one** file differs from its original, and only in include paths:

```diff
--- demos/widgets/lv_demo_widgets.h
+++ src/demos/widgets/lv_demo_widgets.h
-#include "../../src/draw/lv_draw.h"
-#include "../../src/draw/lv_draw_triangle.h"
+#include "../../draw/lv_draw.h"
+#include "../../draw/lv_draw_triangle.h"
```

A mechanical fix-up for the copy's new depth — it now sits *inside* `src/`, so the `src/` hop is
removed. Not a functional change.

### Why this was worth checking

The equivalent check on the **knob board** found a genuine one-line functional patch in LVGL 8.4.0
(`lv_refr.c`, forcing even flush-row height for the ST77916). A stock rebuild there silently
reintroduces a display bug.

**This board is not that case.** Same vendor, same kind of archive, opposite answer — which is
exactly why the check has to be run rather than assumed in either direction.

### Consequence for the repository

Neither tree needs vendoring, and neither needs a patch file. The `reference-only` disposition in
[`acquisition/manifest.json`](./acquisition/manifest.json) is correct, and reconstruction is a
plain download at the pinned tag.

> `ESP-IDF/11_esp_brookesia_phone` (73 MiB) remains **undiffed** — the demo pins no version for
> `esp-brookesia`, so there is no upstream revision to compare against. Still `unknown`.

## C6 — Purchase options for the 3.4C — **RESOLVED 2026-08-24**

**Status:** resolved by [C2](#c2--4c-availability--resolved-2026-08-24).

The listing's *Version Options* are the **two display variants**, not accessory bundles:

| Option | SKU |
|---|---|
| 3.4inch Round Touch Display (800 × 800 pixels) | 31523 |
| 4inch Round Touch Display (720 × 720 pixels) | 31522 |

The `$64.99 – $74.99` range therefore spans the two variants.

> **Still unresolved:** which price belongs to which SKU. Both figures appear on the page, but the
> per-option price is rendered client-side and was not extractable from static HTML. Do not assume
> the larger or the higher-resolution panel is the dearer one — check at purchase.

Whether a camera module is included in either option is also unconfirmed; the option attributes
mention only the display.

## C7 — Demo licence — **RESOLVED 2026-08-24**

**Status:** resolved for the source code.

The demo **ZIP** still contains no `LICENSE`. But Waveshare's official repository for these boards,
<https://github.com/waveshareteam/ESP32-P4-WIFI6-Touch-LCD-XC>, is **Apache-2.0**, and the
published BSP component `waveshare/esp32_p4_wifi6_touch_lcd_xc` is **Apache-2.0** as well.

The repository and the ZIP are the same body of work, so the sensible reading is that Waveshare's
example code for this board is Apache-2.0 and the ZIP simply omits the notice.

**Prefer the repository** when redistribution matters — it carries the licence text the ZIP lacks.

Still `unknown`: the **schematic PDF** and the **wiki page content**, which carry no stated terms
and are not covered by the source-code licence.

## C8 — I²C clock rate — **RESOLVED 2026-08-26**

**Status:** resolved from the BSP's own Kconfig.

```kconfig
config BSP_I2C_FAST_MODE
    bool "Enable I2C fast mode"
    default y
config BSP_I2C_CLK_SPEED_HZ
    default 400000 if BSP_I2C_FAST_MODE
    default 100000
```

**400 kHz is the vendor default.** The 100 kHz value in Waveshare's Arduino `displays_config.h` is
the non-fast-mode *fallback*, not a competing recommendation — the two sources were never really in
conflict, they are the two branches of one option.

Use 400 kHz. Drop to 100 kHz only if a bus carrying four device families (GT9271, ES8311, ES7210,
camera SCCB) plus anything on `J6`/`J8` proves unreliable. More devices means more capacitance, and
capacitance is what caps achievable clock rate.

## C9 — Community evidence — **RESOLVED 2026-08-26**

**Status:** resolved. Earlier passes recorded "a small community"; that was **an artefact of how I
was searching**, not a fact about the board.

### What changed

Repository-name search finds projects that *name* the product. Almost nobody does. **Authenticated
GitHub code search** on the BSP macro and component name found projects by what they *build
against*:

| Query | Type | Distinct projects |
|---|---|---|
| `ESP32-P4-WIFI6-Touch-LCD-3.4C` | repo name | 2 community |
| `BSP_LCD_TYPE_800_800_3_4_INCH` | **code** | 187 matches, 8+ projects |
| `esp32_p4_wifi6_touch_lcd_xc` | **code** | 178 matches, incl. the **BSP source repo** |

### Verified on this hardware

Variant confirmed from each project's own `sdkconfig`:

| Project | ★ | Variant | Licence |
|---|---:|---|---|
| [`garagetinkering/Video_Game_Mini_Maps`](https://github.com/garagetinkering/Video_Game_Mini_Maps) | **256** | **3.4C** | none |
| [`fabkury/p3a`](https://github.com/fabkury/p3a) | **89** | **4C** | Apache-2.0 |
| [`traviscea/center-cluster-esp32-p4`](https://github.com/traviscea/center-cluster-esp32-p4) | 54 | **3.4C** | NOASSERTION |
| [`cptkirki/BETTA-HA-PANEL`](https://github.com/cptkirki/BETTA-HA-PANEL) | 23 | P4, XC macro | NOASSERTION |
| [`Alex-developer/ADSB-Radar`](https://github.com/Alex-developer/ADSB-Radar) | 3 | **4C** | MIT |
| [`ShizhanQiao/FishAgent`](https://github.com/ShizhanQiao/FishAgent) | 3 | P4, XC BSP | MIT |
| [`netseye/linux-waveshare-xc`](https://github.com/netseye/linux-waveshare-xc) | 1 | **3.4C + 4C** | NOASSERTION |

Plus `0015/StickiNote` (51★), `0015/map_tiles_projects` (48★), `0015/Grid_Board` (38★) and others
on sibling P4 boards.

### Two corrections this forces

**The 4C has real users.** Multiple records here stated "zero community projects target the 4C".
That is **wrong** — `fabkury/p3a` (89★, actively maintained) and `Alex-developer/ADSB-Radar` both
select `CONFIG_BSP_LCD_TYPE_720_720_4_INCH=y`. People own this board and build for it.

**A Chinese-language project exists.** `ShizhanQiao/FishAgent` — 一只会聊天、会放歌、有记忆的桌面小鱼
— partially closes the "Chinese community unsearched" gap, and is the closest thing found to an
**ES7210 capture** example, since it does both audio in and out.

### The lesson

*Absence of evidence was evidence of a bad query.* Three separate passes concluded the community
was tiny. It was not — it simply does not put product names in repository descriptions. Technique
written up in
[`guides/research/finding-projects-that-use-a-board.md`](../../../guides/research/finding-projects-that-use-a-board.md).

## C10 — Waveshare MediaWiki API is broken

**Status:** confirmed, worked around. **Impact:** affects future research method.

`https://www.waveshare.com/wiki/api.php?action=parse&…` returns a **PHP fatal error**, not JSON:

```
Parse error: syntax error, unexpected '?' in /yundisk/web/waveshare/dotcom/w/includes/Setup.php on line 472
```

The documented wikitext-enumeration method therefore does not work on this host right now.
Workaround used: fetch the rendered wiki HTML and regex the `files.waveshare.com` URLs, which
recovered every download link successfully. Should be reflected in the
[Waveshare vendor guide](../../../vendors/waveshare/README.md).

## C11 — Touch interrupt is not wired to the SoC

**Status:** established 2026-08-24. **Impact:** medium — determines your touch driver design.

`TP_INT` leaves LCD/touch FPC connector pin 6, passes through a populated 0 Ohm resistor, and
terminates at **test point TP2**. No GPIO label appears on the resistor's far terminal, and
`TP_INT` occurs nowhere else on the schematic.

**The GT911 interrupt is a probe pad, not a SoC connection. Touch must be polled.**

This is an argument from absence, so it is **high confidence rather than certainty**. If you need
interrupt-driven touch, TP2 is the bodge point. Touch *reset* **is** wired, on **GPIO23**.

## C12 — Backlight has two controls and the demos use only one

**Status:** established 2026-08-24. **Impact:** medium — a from-scratch project may get a dark panel.

| Function | Net | GPIO | Driven by any demo? |
|---|---|---:|---|
| Backlight enable | `BL_EN` | **33** | **No** |
| Backlight brightness (PWM) | `LCD_BL_PWM` | **26** | Yes, active low |

No shipped demo touches GPIO33. If `BL_EN` has a pull-up or default-on bias, GPIO26 alone
suffices and the demos work — which presumably explains the omission. If it does not, code that
configures only GPIO26 gets a dark panel with no obvious cause.

The schematic does not resolve the default state. **Drive both**: assert `BL_EN` on GPIO33, then
modulate GPIO26.

## C13 — microSD sits on a switched rail no demo enables

**Status:** established 2026-08-24. **Impact:** medium.

`SD1_VDD` is gated by an **AO3401 P-channel MOSFET** whose gate is **GPIO45**. No shipped demo
drives it. A from-scratch project must enable the card rail before `sdmmc` init.

Useful corollary: you can power-cycle a wedged card without resetting the board.

**Polarity is inferred**, not stated — a P-channel high-side switch implies gate-low turns the card
on. Verify before relying on it.


## C14 — ESP32-P4 silicon revision changes the DSI PHY clock source

**Status:** established 2026-08-24 from Waveshare's `docs/HARDWARE.md` and `docs/FIRMWARE.md`.
**Impact:** medium — wrong choice risks a non-functional display on one silicon generation.

| Silicon | DSI PHY reference |
|---|---|
| ESP32-P4 **pre-v3** | legacy **PLL_F20M** |
| ESP32-P4 **rev3.x** | **XTAL** |

Waveshare set **`.phy_clk_src = 0`**, letting ESP-IDF pick from the active silicon profile. The DPI
pixel clock stays **80 MHz** regardless, and both panels use 2 lanes at 1500 Mbps.

Their explicit audit rule: *"never force the legacy PLL_F20M source for a rev3.x build."*

Two traps here:

1. `rev1_3` and `rev3_x` look like board revisions. They are **chip** profiles.
2. The maintained firmware builds **rev3.x only**. There is no `rev1_3` firmware profile, so a
   pre-v3 board cannot run the published factory image as-is.

Related: `esp_audio_codec` **2.6+ requires ESP32-P4 rev ≥ 3.0**, which is why Waveshare pin
`2.5.0` to keep the `rev1_3` profile viable.

## C15 — JD9365 register `0x40` is panel-specific and undocumented

**Status:** characterised, not explained. **Impact:** low, but blocks safe porting of init tables.

Register `0x40` (page 1, i.e. after `{0xE0, 0x01}`) is the single byte differing between the two
variants' vendor init sequences. Three values are now observed in the wild:

| Source | Panel | `0x40` |
|---|---|---|
| Waveshare 3.4C | 800 × 800 round | **`0x00`** |
| Waveshare 4C | 720 × 720 round | **`0x04`** |
| Espressif `esp_lcd_jd9365` **2.0.2** default | reference panel | **`0x06`** |

Three independent panels, three values. It is therefore a **panel-specific parameter**, not a
board or vendor constant.

The surrounding block `0x40`–`0x45` also differs wholesale between vendors — Espressif use
`0x06, 0xA0, …, 0x1E`, Waveshare use `0x00/0x04, 0x64, 0xC7, 0x18, 0x0B, 0x14` — so `0x40` sits
inside a panel-geometry/gate-timing group rather than being an isolated flag.

Espressif's driver states the position plainly:

```c
// vendor specific initialization, it can be different between manufacturers
```

**What it actually controls is still unknown.** The JD9365 is a Fitipower part and no public
datasheet was located; the register is not documented in the ESP-IDF driver, the component README,
or Waveshare's material. Attempts: Espressif component registry (driver source obtained, no
register docs), GitHub search, vendor docs.

**Practical rule:** treat the whole `0x40`–`0x45` block as belonging to the panel. Never port an
init table between panels on the assumption these bytes are cosmetic — use the table shipped for
your exact panel.

## C16 — Camera SCCB shares the main I²C bus — **confirmed**

**Status:** resolved 2026-08-24 from the schematic. **Impact:** medium for concurrent use.

The MIPI-CSI connector `J5` carries `ESP_I2C_SDA` and `ESP_I2C_SCL` — **GPIO7/GPIO8, the same
physical bus** as the GT9271 touch controller and the ES8311/ES7210 audio chips.

An earlier pass flagged this as unconfirmed because matching grep hits sat in code containing other
boards' defaults. The schematic settles it.

**Four device families share one I²C bus**: touch, codec, echo-cancel ADC, camera sensor — plus
anything you attach to `J6` or `J8` pins 37/39. Consequences:

- A camera sensor whose address collides with `0x5D`/`0x14` (touch), or the audio chips, will not
  work without a mux.
- A stuck device takes out **all four** subsystems at once. A "camera bug" may be a wedged codec.
- `03_i2c_tools` is the first diagnostic for any of them.

## C17 — ESP32-C6 flashing interface — **partly resolved**

**Status:** interface known; firmware image and offsets still unknown.

Header `J4` (SH1.0 4-pin), read directly from the schematic:

| Pin | Signal |
|---:|---|
| 1 | `C6_U0TXD` |
| 2 | `C6_U0RXD` |
| 3 | `GND` |
| 4 | `C6_IO9` |

`C6_IO9` is the ESP32-C6's **strapping pin** — held low at reset to enter serial download mode, as
on any ESP32-C6 design. So `J4` exposes TX, RX, GND and the boot strap: everything a standard
USB-UART adapter needs to flash the co-processor.

**Waveshare still publish no image**, and their `docs/COMPONENTS.md` implies they have not recorded
one either — they defer revisiting hosted-Wi-Fi version ranges until *"the exact ESP32-C6 image or
source revision is recorded."*

### Community answer found 2026-08-26

The `netseye/linux-waveshare-xc` Linux port documents a complete C6 procedure. **Community
evidence, unvalidated on hardware by its own author**, but specific:

- Build **ESP-Hosted-NG**, keeping host and slave on the same tag — they use `release/ng-1.0.6`
- Source: `esp-hosted/esp_hosted_fg/esp/esp_driver/network_adapter`, with the C6 example
  configured for SDIO
- Flash to the C6 at **offset `0x0`**:
  ```bash
  esptool --chip esp32c6 -p "$C6_PORT" write-flash 0x0 out/esp32c6.bin
  ```
- Power-cycle afterwards
- ⚠️ *"Do not flash the original WHY2025 C6 firmware: that firmware expects the badge's SPI
  wiring."* — a real bricking-adjacent warning for anyone reusing that project's binaries

They also give the link pins: **SDIO D0–D3 = 14–17, CLK = 18, CMD = 19, reset = GPIO54
active-high**.

This is for a Linux host, not ESP-IDF, so the *image* differs — but the flashing mechanism, port
and offset are properties of the C6, not the host OS. Treat as a strong starting point, still
unverified.

## C18 — RTC battery is charged through a bare Schottky diode

**Status:** resolved 2026-08-24 from the schematic. **Impact: safety.**

The RTC backup circuit is `ESP_3V3` → **B5819WS Schottky (`D2`)** → `ESP_VBAT` → `J1` pin 1, with
a 1 µF cap (`C39`) to ground. **There is no current-limiting resistor.**

So whenever the board is powered, the 3V3 rail pushes current into whatever cell is fitted,
limited only by the diode drop and the cell's internal resistance.

This turns Waveshare's *"only rechargeable RTC batteries are supported"* note from a preference
into a **hard safety requirement**:

- **ML2032 / LIR2032** (rechargeable) — designed for exactly this trickle charge. Correct.
- **CR2032** (primary) — **not rechargeable**. Charging causes gassing; the cell can vent, leak or
  rupture. Nothing in this circuit prevents it.

Worth stating plainly because CR2032 is the default assumption for a coin cell in a 20 mm holder,
and the holder accepts one mechanically.

No GPIO is involved; the RTC domain is powered, not controlled.

## C19 — Independent confirmation of three schematic findings

**Status:** confirmation, not a conflict. Recorded because independent agreement is rare here.

The `netseye/linux-waveshare-xc` port was written from the same public schematic by an unrelated
author, and independently states:

| Their statement | Matches |
|---|---|
| *"GT911 touch — GPIO7/8 bit-banged I²C; **polling because TP INT/RST are NC**"* | [C11](#c11--touch-interrupt-is-not-wired-to-the-soc) |
| *"Backlight — P4 **GPIO26, active-low**"* | [C12](#c12--backlight-has-two-controls-and-the-demos-use-only-one) |
| *"P4 exposes **one DW-MMC host**"* | The open microSD/Wi-Fi contention question |

Two independent readings of the same schematic agreeing on the touch and backlight findings is
about as good as evidence gets without hardware. Note they reached "polling because INT/RST are NC"
by the same route — reading the netlist — so it is corroboration, not replication by a different
method.

Their work also **contradicts nothing** in this record.

## C20 — The BSP omits `BL_EN` too, so C12 is a library-level gap

**Status:** escalation of [C12](#c12--backlight-has-two-controls-and-the-demos-use-only-one).

C12 recorded that no *demo* drives GPIO33 (`BL_EN`). The BSP source shows it is worse than that:
**there is no `BSP_BL_EN` define and no code touching GPIO33 anywhere in the vendor library.**

So the omission is not a demo oversight — the entire vendor software stack ignores that pin.

Two readings, and the evidence does not distinguish them:

1. `BL_EN` has a pull-up or default-on bias, making it genuinely unnecessary in software. Most
   likely, since the demos and BSP visibly work.
2. It is an oversight that happens not to bite because of board defaults.

Either way, a from-scratch project that configures only GPIO26 is relying on undocumented default
state. **Drive both** unless you have measured otherwise.

The BSP *does* handle the backlight's active-low polarity correctly, via LEDC
`.flags.output_invert = 1` rather than arithmetic — see
[`bsp-source-findings.md`](./bsp-source-findings.md#2-the-backlight-polarity-contradiction--resolved).

## Summary

| ID | Issue | Status | Impact |
|---|---|---|---|
| C1 | microSD pins | **Resolved** 2026-08-24 — upstream defaults happened to be correct | — |
| C2 | 4C availability | **Resolved** — sold as SKU 31522, same listing | — |
| C3 | PCB revision | **Resolved** — rev1.1 | — |
| C4 | DSI porches reused across panels | Explained | Low |
| C5 | Bundled LVGL / Arduino_GFX | **Resolved** — both stock, unmodified | — |
| C6 | Purchase options | **Resolved** — they are the two display variants | — |
| C7 | Demo licence | **Resolved** — repo is Apache-2.0 | — |
| C8 | I²C clock rate | **Resolved** — 400 kHz is the vendor default | — |
| C9 | Community evidence | **Resolved** — a dozen+ projects, incl. 256★ and 89★ | — |
| C10 | Waveshare wiki API returns PHP error | Confirmed | Method |
| C11 | Touch INT goes to a test point, not the SoC | Established | Medium |
| C12 | Two backlight controls; demos drive only one | Established | Medium |
| C13 | microSD rail switched by GPIO45; no demo enables it | Established | Medium |
| C14 | P4 silicon revision changes DSI PHY clock source | Established | Medium |
| C15 | JD9365 `0x40` is panel-specific, meaning undocumented | Characterised | Low |
| C16 | Camera SCCB shares the main I²C bus | **Resolved** — confirmed | Medium |
| C17 | ESP32-C6 flashing | **Partly resolved** — interface known, image not | Medium |
| C18 | RTC cell charged via bare Schottky, no current limit | **Resolved** | **Safety** |
| C19 | Third party independently confirms C11, C12 and one-DW-MMC-host | Confirmation | — |
| C20 | BSP omits `BL_EN` — C12 is library-wide, not demo-only | Established | Medium |

With C1 resolved, the entries most likely to bite someone writing code are now **C12** (dark
panel) and **C13** (dead card slot) — both are things the vendor demos silently rely on rather
than configure. **C11** shapes driver design. The rest affect buying decisions, redistribution, or
research method.

C1 is retained rather than deleted because its *reasoning* was correct even though its conclusion
was not: a vendor-shipped upstream example is not evidence about a board, even when it happens to
agree with the truth.
