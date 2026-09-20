# Tanmatsu board annotations and block diagram — extracted from upstream figures

Content transcribed from two figures in the upstream `tanmatsu-documentation` snapshot so that it
survives independently of the images. Both are **uncited by any authored document in this
repository** — their content had been absorbed into prose without the figures ever being
referenced — so this file closes that gap before the bulky originals are archived.

| Source figure | Bytes | Status |
|---|---:|---|
| `hardware/back-annotated.png` | 1,215,041 | Retained in repo (see note below) |
| `hardware/blockdiagram.png` | 1,010,730 | Retained in repo |

Upstream: `Nicolai-Electronics/tanmatsu-documentation`, commit `bd3ded51548433bd7d614f5607b7d36f5eed61fa`.

---

## 1. Annotated board photo — `back-annotated.png`

A production photograph of the **Prototype**-marked board, silkscreen side, with 22 leader-line
callouts. The board is marked `Tanmatsu`, `Prototype`, `Nicolai Electronics` and the
**`open hardware`** gear logo.

### Callouts, left side (top to bottom)

| Callout | Silkscreen / location |
|---|---|
| WiFi, BLE and IEEE802.15.4 radio module | ESP32-C6 module, top centre |
| Optional: External LoRa antenna SMA connector | `H6` / `J14`, top edge |
| LoRa radio module | shielded can marked `LoRa` |
| Power button | left edge, top |
| "+" button | left edge |
| "−" button | left edge |
| Raspberry Pi compatible CSI camera connector | FFC connector marked `CAMERA` |
| QWIIC compatible I2C **& I3C** expansion port | white 4-pin JST, left edge |
| Headphone jack | marked `AUDIO` |
| Audio DAC | small IC adjacent to the audio block |
| Speaker amplifier | adjacent to audio DAC |
| Speaker connector | marked `SPEAKER` |
| Internal expansion header | the long ~40-pin header across the board centre |

### Callouts, right side (top to bottom)

| Callout | Silkscreen / location |
|---|---|
| USB-C device port | top right |
| **16MB FLASH memory for ESP32-P4** | small package left of the USB-A port |
| **USB-A host port (super-speed 480MBit)** | ⚠ see contradiction below |
| SD card slot (**SDIO 3.0, 1.8 V & 3.3 V cards**) | right edge |
| ESP32-P4 application processor | large QFN, centre right, silkscreen `ESP32-P4` |
| External expansion connector **PMOD, SAO and JTAG** | 2×10 header, silkscreen `CATT` / `SAO, PMOD & JTAG` |
| Coprocessor | QFP left of the CATT connector |
| Battery connector | marked `BATTERY` |
| Sensor connector | `J16`, 4-pin, bottom right |

> ### ⚠ Vendor contradiction: "super-speed 480MBit"
>
> The callout reads **"USB-A host port (super-speed 480MBit)"**. These are mutually exclusive in
> USB terminology: **SuperSpeed is USB 3.0 at 5 Gbit/s**, whereas **480 Mbit/s is High-Speed
> USB 2.0**. The ESP32-P4 provides a **USB 2.0 High-Speed (480 Mbit/s)** OTG peripheral and has no
> USB 3.x capability, so **480 Mbit/s is the correct figure and "super-speed" is wrong** —
> most likely a colloquial use of the phrase rather than the USB-IF term.
>
> Treat any claim of 5 Gbit/s on this port as unsupported. See
> [`gaps-and-conflicts.md`](gaps-and-conflicts.md).

### Detail visible in the photograph but not called out

- Silkscreen block labels: `LoRa`, `CAMERA`, `AUDIO`, `SPEAKER`, `BATTERY`, `EXP`, `CATT`.
- The board is a **`Prototype`** revision — figures derived from it may not match production.
- Four corner mounting holes plus a dense grid of unpopulated test/via points across the lower half.
- The lower third of the board is largely empty copper — the keyboard matrix sits on a separate
  assembly, consistent with [`keyboard.md`](keyboard.md).

---

## 2. Architecture block diagram — `blockdiagram.png`

Overlaid on a faded board photo, with a **colour-coded bus legend**. The legend is the most useful
part, because it disambiguates which interface each peripheral actually sits on.

### Bus legend

| Colour | Bus |
|---|---|
| Red | **Power** |
| Blue | **USB** |
| Mauve | **SDIO** |
| Cyan | **I2S audio** |
| Green | **MIPI DSI / CSI** |
| Magenta | **SPI** |
| Orange | **Internal I2C bus** |
| Black | GPIO / other |

### Connectivity, as drawn

**ESP32-P4** is the hub. Radiating from it:

| Peer | Bus | Notes |
|---|---|---|
| MIPI DSI display | green | |
| MIPI CSI camera | green | |
| **Flash 16MB** | **magenta (SPI)** | confirms the flash is on SPI, not a parallel/quad-dedicated bus in this drawing |
| **ESP32-C6** radio module | **magenta (SPI)** + blue | the C6 is drawn with **both** an SPI link and a USB link |
| **LoRa radio module** | **magenta (SPI)** | |
| USB hub | blue | |
| MMC card reader (SDIO 3.0) | mauve | |
| I2S DAC → Amp → headphone jack / speaker connector | cyan then black | |
| CH32 coprocessor | black + orange | |
| Internal expansion header | multiple | fanned from several buses |
| CATT connector | black | |
| **BMI270** | **orange (internal I2C)** | the IMU sits on the internal I2C bus |
| PMIC | orange + red | |
| QWIIC I3C connector | orange | |
| I2C sensor connector | orange | |

**USB hub** fans out to the **USB-C device port** and the **USB-A host port** — so both external USB
connectors are behind a hub rather than wired directly to the P4.

**CH32 coprocessor** owns:

- **Keyboard matrix** (black)
- **LEDs** (drawn with a **dashed** outline — provisional or optional in this revision)
- a link to the **PMIC**

**Power chain (red):** `1S LiPo battery connector` → `PMIC` → `3.3 V DC/DC` → the rest of the board.
The **power button** is drawn into the **PMIC**, not into a GPIO — consistent with a
PMIC-controlled power path.

**Button routing is not uniform**, and this is the diagram's most useful single detail:

| Button | Goes to |
|---|---|
| Power button | **PMIC** |
| "+" button | **Keyboard matrix** |
| "− / boot" button | **P4 GPIO** directly |

That the "−" button doubles as **boot** and is wired to a P4 GPIO rather than the matrix is exactly
what you need to know to enter download mode. Cross-check against
[`pinouts-and-buses.md`](pinouts-and-buses.md).

---

## Provenance and reuse

Both figures are from the upstream documentation repository, which states **no licence**. They are
reproduced here only as transcribed text and factual description, not as copied images. See
[`sources.md`](sources.md) for the full provenance record and
[`gaps-and-conflicts.md`](gaps-and-conflicts.md) for the "super-speed 480MBit" contradiction.
