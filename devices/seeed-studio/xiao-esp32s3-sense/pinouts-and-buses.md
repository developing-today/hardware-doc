# XIAO ESP32S3 Sense — pinouts and buses

> Authoritative wiring reference for the Seeed Studio XIAO ESP32S3 Sense (SKU 113991115).
> Research snapshot **2026-08-24**. Board revision covered: **v1.3 silicon / "v1.5" file release** — see [the revision-numbering conflict](gaps-and-conflicts.md#2-the-schematics-own-revision-number-contradicts-its-filename).

## How this document was produced

> The general method — and its pitfalls — is written up reusably at
> [`guides/reverse-engineering/netlists-from-vendor-eda-files.md`](../../../guides/reverse-engineering/netlists-from-vendor-eda-files.md).


Almost every pin table published for this board — including Seeed's own wiki — is a hand-maintained prose table. This document instead derives connectivity from **primary machine-readable design data**, then cross-checks it against two independent software sources. Three fully independent chains agree:

| Evidence chain | Artifact | What it establishes |
|---|---|---|
| **A — PCB netlist (ground truth)** | [`artifacts/extracted/xiao-esp32s3-sense-v1.5-sch-pcb/…/XIAO ESP32S3_V1.5.kicad_pcb`](artifacts/extracted/) | KiCad `.kicad_pcb` stores *resolved* net names per pad. This is the actual copper. Extracted with [`tools/kicad_pcb_nets.py`](../../../tools/kicad_pcb_nets.py). |
| **B — schematic netlist** | `…/03 XIAO ESP32-S3-Sense.kicad_sch` | Reconstructed geometrically (KiCad schematics store no netlist) with [`tools/kicad_netlist.py`](../../../tools/kicad_netlist.py). Used to recover *component-level* detail such as series resistors that chain A flattens. |
| **C — vendor software** | [`artifacts/source-snapshots/pins_arduino.h`](artifacts/source-snapshots/pins_arduino.h), [`camera_pins.h`](artifacts/source-snapshots/camera_pins.h) | Espressif `arduino-esp32` `variants/XIAO_ESP32S3/` and the `CAMERA_MODEL_XIAO_ESP32S3` block, retrieved 2026-08-24 from `master`. |

Where the three disagree, the disagreement is recorded rather than averaged. **They do not disagree on any GPIO assignment** — which is itself a useful result, because it means the Arduino variant can be trusted as a pin reference for this board.

---

## 1. The 14-pin user header (U9)

This is the castellated edge connector — the only pins you can solder to without touching the daughterboard. Physical order is as printed on the silkscreen.

| Hdr pin | Silk | Arduino name | **GPIO** | ADC | Peripheral default | Notes |
|---:|---|---|---:|---|---|---|
| 1 | D0 | `D0` / `A0` | **GPIO1** | ADC1_CH0 | — | Safe general purpose |
| 2 | D1 | `D1` / `A1` | **GPIO2** | ADC1_CH1 | — | Safe general purpose |
| 3 | D2 | `D2` / `A2` | **GPIO3** | ADC1_CH2 | — | ⚠ **strapping pin** (JTAG source select). Also routed to J3.2 |
| 4 | D3 | `D3` / `A3` | **GPIO4** | ADC1_CH3 | — | Safe general purpose |
| 5 | D4 | `D4` / `A4` | **GPIO5** | ADC1_CH4 | **I2C SDA** | `Wire` default |
| 6 | D5 | `D5` / `A5` | **GPIO6** | ADC1_CH5 | **I2C SCL** | `Wire` default |
| 7 | D6 | `D6` / `TX` | **GPIO43** | — | **UART0 TX** | Via **R6 = 499 Ω series** (chain B) |
| 8 | D7 | `D7` / `RX` | **GPIO44** | — | **UART0 RX** | Direct. Also Arduino's nominal `SS` — see [§7.3](#73-the-arduino-ss-pin-is-not-the-sd-chip-select) |
| 9 | D8 | `D8` / `A8` | **GPIO7** | ADC1_CH6 | **SPI SCK** | **Shared with microSD** (J3.3) |
| 10 | D9 | `D9` / `A9` | **GPIO8** | ADC1_CH7 | **SPI MISO** | **Shared with microSD** (J3.4) |
| 11 | D10 | `D10` / `A10` | **GPIO9** | ADC1_CH8 | **SPI MOSI** | **Shared with microSD** (J3.5) |
| 12 | 3V3 | — | — | — | 3V3 rail out | Output of U3 (SGM6029), **600 mA max** |
| 13 | GND | — | — | — | ground | |
| 14 | 5V | — | — | — | **VBUS** | Straight from USB-C VBUS. See [§8](#8-power-tree) |

Chain A confirms every row: `J3`/`U9` pad-to-net dump in `tools/`. Chain C confirms D0–D10 and TX/RX/SDA/SCL/SCK/MISO/MOSI identically.

**The ADC numbering is a trap.** Seeed's marketing says "9× ADC". All nine (`A0`–`A5`, `A8`–`A10`) land on **ADC1**, which is the *good* outcome — ADC1 remains usable while Wi-Fi is active. ESP32-S3's ADC2 is not exposed on this header at all. If you have seen the widely repeated "ADC2 stops working when Wi-Fi is on" warning for ESP32 boards, it does not bite you here. Note the gap in numbering (`A6`/`A7` do not exist) is real and follows the ESP32-S3's channel map, not a documentation error.

---

## 2. The J3 board-to-board connector (Sense daughterboard interface)

**J3 = Hirose `DF40C-30DP-0.4V(51)`**, a 0.4 mm-pitch 30-signal + 4-mechanical board-to-board plug. This pinout is **not published by Seeed in any document** — it is recovered here from the PCB netlist (chain A). It is the single most useful undocumented artifact in this research pass, because it is what you need to build your own daughterboard, probe a failing camera, or design a replacement for the (fragile) sensor board.

| J3 pin | Net | GPIO | Function on the Sense board |
|---:|---|---:|---|
| 1 | `GND` | — | ground |
| 2 | `D2/A2` | GPIO3 | spare — brought to the daughterboard but **unused by the stock Sense board** |
| 3 | `D8/A8/SCK` | GPIO7 | microSD **SCK** |
| 4 | `D9/A9/MISO` | GPIO8 | microSD **MISO** (DAT0) |
| 5 | `D10/A10/MOSI` | GPIO9 | microSD **MOSI** (CMD) |
| 6 | `IO10/XMCLK` | GPIO10 | camera **XCLK** (master clock, LEDC-generated) |
| 7 | `IO11/DVP_Y8` | GPIO11 | camera **D6** |
| 8 | `IO12/DVP_Y7` | GPIO12 | camera **D5** |
| 9 | `IO13/DVP_PCLK` | GPIO13 | camera **PCLK** |
| 10 | `IO14/DVP_Y6` | GPIO14 | camera **D4** |
| 11 | `IO15/DVP_Y2` | GPIO15 | camera **D0** |
| 12 | `IO16/DVP_Y5` | GPIO16 | camera **D3** |
| 13 | `IO17/DVP_Y3` | GPIO17 | camera **D1** |
| 14 | `IO18/DVP_Y4` | GPIO18 | camera **D2** |
| 15 | `VIN` | — | **system rail** (battery-or-USB, pre-regulator) |
| 16 | `IO21/USER_LED` | GPIO21 | microSD **CS** — *and* the on-board user LED. See [§7.1](#71-the-user-led-and-the-sd-card-chip-select-are-the-same-pin) |
| 17 | `GND` | — | ground |
| 18 | `VCC_3V3` | — | 3.3 V rail |
| 19 | `VCC_3V3` | — | 3.3 V rail |
| 20 | *(no connect)* | — | unpopulated on the XIAO side (`unconnected-(J3-Pad20)`) |
| 21 | `IO48/DVP_Y9` | GPIO48 | camera **D7** (MSB) |
| 22 | `IO47/DVP_HREF` | GPIO47 | camera **HREF** |
| 23 | `IO38/DVP_VSYNC` | GPIO38 | camera **VSYNC** |
| 24 | `MTCK/IO39/CAM_SCL` | GPIO39 | camera **SCCB SCL** (`SIOC`) — **also JTAG MTCK** |
| 25 | `MTDO/IO40/CAM_SDA` | GPIO40 | camera **SCCB SDA** (`SIOD`) — **also JTAG MTDO** |
| 26 | `MTDI/IO41/PDM_DATA` | GPIO41 | microphone **PDM DATA** — **also JTAG MTDI** |
| 27 | `MTMS/IO42/PDM_CLK` | GPIO42 | microphone **PDM CLK** — **also JTAG MTMS** |
| 28 | `GND` | — | ground |
| 29 | `GND` | — | ground |
| 30 | `VIN` | — | system rail |
| 31–34 | `GND` / NC | — | mechanical/shield tabs. 31, 33, 34 = `GND`; 32 = no connect |

Two things are worth pulling out of that table.

**J3.2 (GPIO3) is a free signal across the connector.** The stock daughterboard does not use it. If you are designing a replacement sensor board, that is a spare line you already have routed — at the cost of GPIO3 being a strapping pin.

**`VIN` and `VCC_3V3` are both present, and `VIN` is the *unregulated* system node.** A custom daughterboard can draw from `VIN` and do its own regulation rather than loading the 600 mA U3 rail. The stock board does exactly this: the daughterboard takes `VIN` and generates the camera's 2.8 V and 1.3 V rails locally with its own LDOs — see [`sense-daughterboard.md` §3](sense-daughterboard.md#3-power--the-camera-needs-three-rails).

---

## 3. Camera bus (DVP, 8-bit parallel)

The camera is a **DVP (digital video port) parallel** interface, not MIPI-CSI and not SPI. Eight data lines plus three sync lines plus a master clock, with configuration over a 2-wire SCCB (I²C-alike) channel.

| Camera signal | GPIO | J3 | Direction (from ESP32-S3) |
|---|---:|---:|---|
| `XCLK` (master clock in) | GPIO10 | 6 | out — generated by **LEDC**, typically 20 MHz |
| `PCLK` | GPIO13 | 9 | in |
| `VSYNC` | GPIO38 | 23 | in |
| `HREF` | GPIO47 | 22 | in |
| `D0` (`Y2`) | GPIO15 | 11 | in |
| `D1` (`Y3`) | GPIO17 | 13 | in |
| `D2` (`Y4`) | GPIO18 | 14 | in |
| `D3` (`Y5`) | GPIO16 | 12 | in |
| `D4` (`Y6`) | GPIO14 | 10 | in |
| `D5` (`Y7`) | GPIO12 | 8 | in |
| `D6` (`Y8`) | GPIO11 | 7 | in |
| `D7` (`Y9`, MSB) | GPIO48 | 21 | in |
| `SIOC` (SCCB SCL) | GPIO39 | 24 | out |
| `SIOD` (SCCB SDA) | GPIO40 | 25 | bidir |
| `PWDN` | **−1 (absent)** | — | **not wired** |
| `RESET` | **−1 (absent)** | — | **not wired** |

### 3.1 There is no camera power-down or reset line — and that has consequences

`camera_pins.h` declares `PWDN_GPIO_NUM -1` and `RESET_GPIO_NUM -1`, and chain A confirms no such net exists on J3. Practically:

- **You cannot hardware-reset the sensor.** If the OV sensor's SCCB state machine wedges (which does happen after brown-outs and after aborted `esp_camera_deinit()`), the *only* recovery is a full board power cycle. A software reboot via `esp_restart()` does **not** reset the sensor, because its supply is never interrupted. This is the mechanism behind the very common "camera works on cold boot but fails after soft reset" complaint.
- **You cannot power the sensor down to save energy.** The camera draws its idle current whenever the 3V3 rail is up. Deep-sleep figures for the Sense are consequently much worse than for the plain XIAO ESP32S3 — see [§9](#9-power-and-sleep-numbers).
- Workaround, if you control the daughterboard: J3.2 (GPIO3) is spare and could drive a load switch. Nothing on the stock board does this.

### 3.2 SCCB is a *separate* bus from the user I²C

`SIOC`/`SIOD` on GPIO39/GPIO40 are **not** the `Wire` bus (GPIO6/GPIO5). Scanning `Wire` will never find the camera at 0x30/0x3C. The camera driver bit-bangs or drives its own SCCB peripheral on 39/40. Do not attempt to hang extra I²C devices on 39/40 — the sensor board has its own pull-ups and the driver assumes exclusive ownership.

---

## 4. Microphone (PDM)

| Signal | GPIO | J3 | Notes |
|---|---:|---:|---|
| PDM `CLK` | **GPIO42** | 27 | driven by the ESP32-S3 I²S peripheral in PDM-RX mode |
| PDM `DATA` | **GPIO41** | 26 | single data line |

It is a **PDM (pulse-density modulation) digital microphone**, mono, one data line. It is *not* I²S-standard (no `WS`/`LRCLK`, no `SD` in the classic sense) and it is *not* analogue. The ESP32-S3's I²S peripheral has a dedicated PDM-RX mode with a hardware decimation filter that converts the 1-bit stream into PCM samples.

Consequences that trip people up:

- Only **I2S_NUM_0** supports PDM RX on the ESP32-S3. `I2S_NUM_1` cannot do it. If you also want to *play* audio over I²S you must use the other peripheral instance and plan the pin budget accordingly.
- There is **no second microphone and no stereo**. Left/right channel selection is meaningless; some copied-from-elsewhere code sets a channel mask and then reports silence.
- Sample rates in the low tens of kHz are what the decimator is designed for. 16 kHz is the well-trodden path (it is what every keyword-spotting example uses).
- The Arduino 2.x `I2S` API and the Arduino 3.x / ESP-IDF 5.x `i2s_pdm` driver are **incompatible rewrites**. Most community microphone sketches for this board predate the change and will not compile on a current core. See [`development.md`](development.md).

---

## 5. microSD card

| Signal | GPIO | J3 | Shared with |
|---|---:|---:|---|
| `CLK` | GPIO7 (`D8`) | 3 | user header pin 9, SPI `SCK` |
| `MISO` / DAT0 | GPIO8 (`D9`) | 4 | user header pin 10, SPI `MISO` |
| `MOSI` / CMD | GPIO9 (`D10`) | 5 | user header pin 11, SPI `MOSI` |
| `CS` | **GPIO21** | 16 | **the user LED** |

The slot is wired for **1-bit SPI mode**, not 4-bit SDIO. You will not get SDIO throughput out of it, and no amount of driver configuration changes that — the DAT1/DAT2/DAT3 lines are simply not routed across J3.

Seeed documents `SD.begin(21)` and states plainly that "for the microSD card design of the expansion board, the CS pin is connected to **GPIO 21**" (`XIAO_ESP32S3_Sense_tf_and_filesystem.md`, retrieved 2026-08-24). Cards are officially supported to **32 GB, FAT32**. Larger cards formatted exFAT will not mount with the stock Arduino `SD` library; reformatting a 64 GB card as FAT32 usually works but is outside vendor support.

---

## 6. USB, boot and reset

| Function | Detail | Evidence |
|---|---|---|
| USB connector | `UBF31-0171` USB 2.0 Type-C receptacle | chain A/B BOM |
| CC pull-downs | R1, R2 = **5.1 kΩ** | chain B — correct UFP resistors, so it charges from a plain C-to-C cable |
| Data lines | `USB_D±` → **R3/R4 = 22 Ω series** → `ESP_USB_D±` → GPIO19/GPIO20 | chain B |
| USB peripheral | **native USB-OTG / USB-Serial-JTAG in the ESP32-S3** — there is *no* CH340/CP2102 bridge on this board | chain A: no bridge IC in BOM |
| VID / PID | `0x2886` / `0x0056` | `pins_arduino.h` |
| `RESET` button | **K1** — shorts `EN` to GND; `EN` pulled up by R8 = 10 kΩ, decoupled by C21 | chain B |
| `BOOT` button | **K2** — shorts `GPIO0` to GND; pulled up by R7 = 10 kΩ, C28 | chain B |
| Test points | TP2=`PDM_CLK`, TP3=`PDM_DATA`, TP4=`CAM_SDA`, TP5=`CAM_SCL`, TP6=`EN`, TP7=`USB_D−`, TP8=`USB_D+` | chain B |

Those test points are genuinely useful and undocumented: **TP7/TP8 give you USB D±** and **TP6 gives you `EN`**, so a board with a damaged USB-C receptacle can still be flashed by tacking wires onto the back, and an external programmer can assert reset without the button.

### The bottom side carries labelled JTAG pads

Seeed's own 3D-model render ([`media/board-bottom-view.jpg`](media/board-bottom-view.jpg)) shows the underside silkscreen clearly, and it is more informative than any published pinout diagram:

```
        MTDO    MTDI
        GND     EN
        MTCK    MTMS
        D+      D-        BAT + / −
```

**All four JTAG signals — `MTCK`, `MTMS`, `MTDI`, `MTDO` — are broken out as labelled pads**, alongside `EN`, USB `D+`/`D−`, `GND` and the battery pads.

This materially softens the [JTAG limitation](#72-the-camera-and-microphone-occupy-all-four-jtag-pins): the *mainboard* deliberately exposes the whole debug port. It is only unavailable when the Sense daughterboard is fitted and consuming those signals. **On a bare XIAO ESP32S3 you can solder to these pads and get full JTAG**, and the [microphone can be disconnected](../../../components/memsensing/msm261d3526h1cpm/README.md) at JP1/JP2 to free `MTDI`/`MTMS` while keeping the camera.

The same pads appear in the [FCC internal photos](regulatory-and-certification.md#31-the-jtag-pins-are-broken-out-as-labelled-bottom-side-pads), but at 709 × 531 px the labels are barely legible; this render is the better reference.

Because USB is native to the SoC rather than provided by a bridge chip, **the serial port disappears when your firmware crashes, reconfigures USB, or enters deep sleep.** This is normal and is the number-one support question. Recovery is the manual bootloader entry: hold **BOOT**, tap **RESET**, release **BOOT** — the ROM bootloader then enumerates unconditionally as a fixed USB-Serial-JTAG device regardless of what the application did.

---

## 7. Pin conflicts you must design around

These are the failure modes that cost people days. Each is stated with its mechanism, not just as a warning.

### 7.1 The user LED and the SD card chip-select are the same pin

**GPIO21 is simultaneously `LED_BUILTIN` and the microSD `CS`.** `pins_arduino.h` declares `static const uint8_t LED_BUILTIN = 21;`, chain A shows `J3.16 → IO21/USER_LED`, and Seeed's own SD tutorial passes `21` to `SD.begin()`.

Therefore:

- Any `digitalWrite(LED_BUILTIN, …)` while the SD library holds the bus **asserts or de-asserts the card's chip select** mid-transaction. Expect corrupted writes, failed mounts, and `SD.begin()` succeeding once and never again.
- Conversely, every SD transaction visibly flickers the user LED. That is not a fault; it is the same net.
- **Do not use `LED_BUILTIN` as a status indicator in any sketch that touches the SD card.** Use an external LED on a spare pin (GPIO1–GPIO4 are free), or accept the LED purely as an SD activity light.

This is the highest-impact undocumented interaction on the board. Seeed documents the LED and the SD `CS` in two different pages and never connects them.

### 7.2 The camera and microphone occupy all four JTAG pins

`MTCK`/`MTDO`/`MTDI`/`MTMS` = **GPIO39/40/41/42** are, on the Sense, `CAM_SCL`/`CAM_SDA`/`PDM_DATA`/`PDM_CLK`. The daughterboard consumes the entire JTAG port.

- **Hardware JTAG debugging is impossible while the Sense daughterboard is attached.** Not "degraded" — the pins are physically driven by another device.
- The ESP32-S3's *built-in* USB-Serial-JTAG bridge normally lets you debug over the USB-C connector with no extra hardware. That path uses GPIO19/20 and, crucially, still routes to the same internal JTAG signals. In practice you must choose: debug the board bare, or run it with the sensor board fitted.
- GPIO3 (`D2`) is the ESP32-S3 **JTAG source-select strapping pin**. Pulling it externally changes whether JTAG is driven by the USB bridge or the MTxx pads — another reason to leave `D2` alone if you care about debugging.

### 7.3 The Arduino `SS` pin is not the SD chip select

`pins_arduino.h` sets `static const uint8_t SS = 44;` — GPIO44, which is `D7`/`RX`. That is the *Arduino variant's* nominal SPI slave-select, and it has **nothing to do with the microSD card**, whose CS is GPIO21. Code that calls `SPI.begin()` and then relies on the default `SS` will toggle the UART RX pin. Always pass the CS explicitly.

### 7.4 Strapping pins

| GPIO | XIAO name | Strap role | Risk |
|---:|---|---|---|
| GPIO0 | — (BOOT button) | boot mode select | Held low at reset ⇒ ROM download mode. Not on the header, low risk |
| GPIO3 | `D2` | JTAG source select | **On the user header.** External pull-ups/downs affect debug routing |
| GPIO45 | — | VDD_SPI voltage select | **No-connect on this PCB** (chain A) — cannot be disturbed |
| GPIO46 | — | ROM message printing | **No-connect on this PCB** (chain A) — cannot be disturbed |

Seeed left GPIO45/46 unconnected, which is the safe choice and removes two classic ESP32-S3 footguns. Only `D2` needs care.

### 7.5 GPIO33–GPIO37 do not exist for you

Chain A is unambiguous: on the PCB, **U1 pins 38–42 (`GPIO33`–`GPIO37`) and pin 28 (`SPICS1`) terminate in single-pad nets with no other member** — they are no-connects at board level. They are consumed *inside the package* by the ESP32-S3R8's **octal PSRAM** die.

The practical rule: `GPIO33`, `GPIO34`, `GPIO35`, `GPIO36`, `GPIO37` are **unusable**. Configuring them does not raise an error — it silently corrupts PSRAM access, which typically manifests as a crash the moment the camera allocates a framebuffer, or as `Guru Meditation` / cache-access panics far away from the offending code. Likewise `GPIO26`–`GPIO32` serve the SPI flash/PSMEM interface. The usable set on this board is exactly what is in the tables above.

---

## 8. Power tree

```
USB-C VBUS ──┬── U9.14 (5V pin)
             ├── D2 (LMBR4010BST5G Schottky) ──┐
             ├── U4 SGM40567 charger ── VBAT ──┤ (via Q1 LP0404N3T5G P-MOS)
             └── R9/R11 sense                  │
                                               ▼
                                      VIN (system node) ── J3.15 / J3.30
                                               │
                                      U3 SGM6029 buck-boost
                                               │
                                          VCC_3V3 (600 mA max)
                                               ├── ESP32-S3R8
                                               ├── GD25Q64 flash
                                               └── J3.18 / J3.19 → daughterboard
```

| Rail | Source | Limit | Notes |
|---|---|---|---|
| `VBUS` | USB-C | host-dependent | Exposed on header pin 14. **No voltage on this pin when running from battery** (chain A shows no boost path back to VBUS; Seeed's wiki says the same) |
| `VBAT` | Li-ion via bottom `BAT+`/`BAT−` pads (`BAT0` test pad) | 3.7 V nominal | Charged by U4 |
| `VIN` | `VBUS` via D2, **or** `VBAT` via Q1 | — | Automatic source selection; this is what J3 carries |
| `VCC_3V3` | U3 SGM6029 **buck-boost** | **600 mA** (schematic annotation `Imax=600mA`) | Buck-boost, not LDO — so 3V3 holds up as the battery sags below 3.3 V |

### 8.1 Battery charging current is set by a resistor — and the number is disputed

The schematic carries the explicit designer's note:

> `ICharge = 24000/220K = 110mA`

with **R10 = 220 kΩ** (confirmed in the BOM, chain A/B) feeding U4's `IREF` pin. Seeed's wiki, meanwhile, states **"Charging current: 100mA (Fast) / 0.9mA (Trickle)"**.

These disagree by 10 %. The schematic's own arithmetic is self-consistent (24000 ÷ 220 000 A = 109 mA), so the most likely reading is that **110 mA is the design value and 100 mA is a rounded marketing figure**. Recorded as unresolved in [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — do not treat either number as a guaranteed spec.

The practically interesting part: **charge current is programmable by swapping R10.** Halving R10 to 110 kΩ would imply ~218 mA. This is the standard modification for people running larger cells who find the stock ~110 mA charge rate painfully slow on a 1000 mAh battery. Two cautions before anyone does it: the SGM40567 is a linear charger, so the extra current becomes heat in a WLCSP package on a 21 mm board, and this modification is entirely unsupported and untested here — it is an inference from the schematic annotation, not a verified procedure.

### 8.2 There is no battery voltage sense — confirmed by the vendor

Seeed states it directly:

> "Since all GPIO pins of the XIAO ESP32-S3 are assigned their own functions, we do not have a GPIO configured for the battery pin. this means that we cannot get the battery voltage at the software level by reading the analog value of one of the GPIOs."
> — `XIAO_ESP32S3_Getting_Started.md`, retrieved 2026-08-24

Chain A corroborates: the `VBAT` net has exactly four members — `BAT0` (test pad), `C26`, `Q1.1`, `U4.A1`. **No divider, no ADC path.** Any tutorial claiming you can `analogRead()` the battery on a XIAO ESP32S3 is describing a different XIAO (the nRF52840 variant *does* have one) or a user modification.

To measure battery voltage you must add external hardware: a 2-resistor divider from `BAT+` into a spare ADC1 pin (`D0`–`D3` are free), ideally with a MOSFET to disconnect the divider in sleep so it does not drain the cell. Note that a naive always-on 2×100 kΩ divider costs ~18 µA, which is comparable to the entire deep-sleep budget.

### 8.3 Charge LED behaviour

`CHG0` (red) is driven by U4's `NCHG` open-drain status output via R11 = 10 kΩ. Vendor-documented behaviour: on for ~30 s with USB and no battery; **flashing** while charging; off when full. The "flashing = charging" convention is unusual — on most boards a steady LED means charging — and is a frequent source of "is my battery charging?" confusion.

---

## 9. Power and sleep numbers

Vendor-published figures (`XIAO_ESP32S3_Getting_Started.md`, retrieved 2026-08-24). These are **vendor claims, not independently measured here.**

| Mode | XIAO ESP32S3 (plain) | **XIAO ESP32S3 Sense** |
|---|---|---|
| Modem-sleep | 27 mA | 3.8 V / 31.6 mA |
| Light-sleep | 2 mA | 3.8 V / 2.45 mA |
| **Deep-sleep** | **14 µA** | **3.8 V / 33.51 µA** |
| Webcam app, USB | — | avg ~140 mA, peak ~347 mA @ 5 V |
| Webcam app, battery | — | avg ~155 mA, peak ~366 mA @ 3.8 V |
| Mic record + SD write, USB | — | avg 54.58 mA, peak 86.7 mA @ 5 V |

The Sense's deep-sleep current is **~2.4× the bare board's** (33.5 µA vs 14 µA), which is exactly the cost of a camera you cannot power down ([§3.1](#31-there-is-no-camera-power-down-or-reset-line--and-that-has-consequences)). For a battery-powered periodic-capture design this is the dominant term: at 33.5 µA a 500 mAh cell lasts roughly 1.7 years in sleep alone, before any captures. That is usually acceptable — but if you were expecting the advertised 14 µA figure, note that the figure belongs to the **non-Sense** board.

Note also the third column of Seeed's own table lists a Sense deep-sleep of **3 mA** in one row and **33.51 µA** in another. See [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

---

## 10. Antenna

`ANT1` = **`U.FL-R-SMT-1`** — a U.FL/IPEX-1 coaxial receptacle, with the removable "sticker" antenna supplied in the box. Chain B shows the RF path from the ESP32-S3 `LNA_IN` (U1.1) through a matching network (`C18` 1 pF, `L2` 3.3 nH, `C17`/`L3` **DNP**) to ANT1.

There is **no PCB trace antenna and no on-board chip antenna**. If the U.FL antenna is not fitted, the radio is running into an open circuit: it will still associate with an access point a metre away, and will then behave erratically at any real distance. "Wi-Fi keeps dropping" on a XIAO ESP32S3 is very often a detached antenna — the connector is small and the antenna pops off easily.

The `C17`/`L3` DNP positions are the classic *alternate match / antenna-select* footprints, left unpopulated because only one antenna path is fitted. They are a convenient place to re-tune the match if you replace the antenna with something very different, though nothing in the vendor documentation sanctions this.

---

## 11. Full ESP32-S3R8 pin usage map

Every pin of U1, with its board-level fate. `NC` = confirmed no-connect in the PCB netlist.

| U1 pin | Signal | Net | Board use |
|---:|---|---|---|
| 1 | `LNA_IN` | match → ANT1 | RF |
| 2, 3 | `VDD3P3` | via L1 2 nH | RF supply |
| 4 | `CHIP_PU` | `EN` | RESET button K1, R8 pull-up, TP6 |
| 5 | `GPIO0` | `GPIO0` | BOOT button K2, R7 pull-up |
| 6–9 | `GPIO1`–`GPIO4` | `D0`–`D3` | user header (GPIO3 also → J3.2) |
| 10, 11 | `GPIO5`, `GPIO6` | `D4`/SDA, `D5`/SCL | user header, I²C |
| 12–14 | `GPIO7`–`GPIO9` | `D8`/SCK, `D9`/MISO, `D10`/MOSI | user header **+ microSD** via J3 |
| 15–19 | `GPIO10`–`GPIO14` | XMCLK, Y8, Y7, PCLK, Y6 | **camera**, via J3 |
| 20 | `VDD3P3_RTC` | `VCC_3V3` | supply |
| 21, 22 | `XTAL_32K_P/N` | `IO15`/Y2, `IO16`/Y5 | **camera** — the 32 kHz crystal pins are reused as DVP data |
| 23, 24 | `GPIO17`, `GPIO18` | Y3, Y4 | **camera** |
| 25, 26 | `GPIO19`, `GPIO20` | `ESP_USB_D−/+` | native USB, TP7/TP8 |
| 27 | `GPIO21` | `IO21/USER_LED` | **user LED + microSD CS** |
| 28 | `SPICS1` | — | **NC** |
| 29 | `VDD_SPI` | `VDD_SPI` | flash supply, C22 |
| 30–35 | `SPIHD/WP/CS0/CLK/Q/D` | → U5 | **QSPI flash** (GD25Q64) |
| 36, 37 | `SPICLK_N`, `SPICLK_P` | `IO48`/Y9, `IO47`/HREF | **camera** — repurposed |
| 38–42 | `GPIO33`–`GPIO37` | — | **NC — in-package octal PSRAM** |
| 43 | `GPIO38` | `IO38/DVP_VSYNC` | **camera** |
| 44–48 | `MTCK`,`MTDO`,`VDD3P3_CPU`,`MTDI`,`MTMS` | CAM_SCL, CAM_SDA, —, PDM_DATA, PDM_CLK | **camera + mic — the whole JTAG port** |
| 49 | `U0TXD` (GPIO43) | → R6 499 Ω → `D6/TX` | UART |
| 50 | `U0RXD` (GPIO44) | `D7/RX` | UART |
| 51 | `GPIO45` | — | **NC** (strap) |
| 52 | `GPIO46` | — | **NC** (strap) |
| 53, 54 | `XTAL_N/P` | X1 | **40 MHz crystal**, via L5 24 nH (see rev note) |
| 55, 56 | `VDDA` | `VCC_3V3` | supply |
| 57 | `GND` | GND | |

Note U1.54 reaches the crystal through **L5 = 24 nH**. The revision history records that in **v1.2 (2023-07-25) R5 was changed from 0 Ω to L5 24 nH** — a crystal-drive/EMC fix. Boards older than v1.2 have a plain 0 Ω link there.

---

## 12. Related documents

- [`README.md`](README.md) — device overview and identity
- [`resources-and-conflicts.md`](resources-and-conflicts.md) — peripheral, DMA, memory and simultaneous-use budgets
- [`bom-and-board-construction.md`](bom-and-board-construction.md) — full BOM, stackup, DNP parts, test points
- [`gaps-and-conflicts.md`](gaps-and-conflicts.md) — unresolved questions and source disagreements
- [`development.md`](development.md) — toolchains and build configuration
- Component records: [ESP32-S3R8](../../../components/espressif/esp32-s3r8/README.md)
