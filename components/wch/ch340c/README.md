# WCH CH340C

- **Category:** **USB-to-UART bridge** — full-speed USB 2.0 device → TTL asynchronous serial
- **Package:** **SOP-16**, 3.9 mm body (150 mil), 1.27 mm (50 mil) pitch
- **Distinguishing feature vs CH340G:** the **C** variant has an **integrated clock generator** — no external 12 MHz crystal, no load capacitors, no `XI`/`XO` pins
- **USB identity:** `1A86:7523` (shared across the whole CH340 line)
- **Fitted as:** `U3` on Soldered Inkplate 5, Inkplate 5 Gen 2, and the ZeroWriter Ink main board
- **Research date:** 2026-08-24

> **This repository already holds a deep CH340-family record.**
> [`components/wch/ch340x/README.md`](../../wch/ch340x/README.md) resolved the Waveshare knob board's bridge to a **CH340X in MSOP-10**, and contains the full candidate-elimination argument, the VID/PID table extracted from WCH's own macOS driver, and the CH340X pin-6 `TNOW`⇄`DTR#` mode-strap analysis. **Read it for the family.** This record covers what is specific to the **CH340C** and to the boards it is fitted on here, and deliberately does not repeat that material.

---

## Evidence labelling

| Marker | Meaning |
|---|---|
| **[DOC]** | Stated by WCH in `artifacts/ch340-datasheet-v3.4.pdf` (the document self-identifies as **Version 3D**) or in the WCH file-metadata API |
| **[SCH]** | Read out of the Soldered / ZeroWriter KiCad schematic sources, via net extraction |
| **[SRC]** | Read out of vendor-shipped source (Inkplate Arduino library, WCH Linux driver, Linux kernel) |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |
| **[INF]** | Inference. Not established by the above |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Manufacturer | Nanjing Qinheng Microelectronics (南京沁恒微电子), trading as **WCH** | **[DOC]** |
| Family | CH340 — USB bus converter, serial / printer / IrDA modes | **[DOC]** §1 |
| Package | **SOP-16**, 3.9 mm width (150 mil), **1.27 mm (50 mil) pitch** | **[DOC]** §3 package table |
| **Integrated clock** | **Yes.** *"CH340C/N/K/E/X/B chips have built-in clock generators, no need for external crystals and capacitors."* | **[DOC]** §5.1 |
| Supply | **5 V** (`VCC` = 5 V, `V3` decoupled with 0.1 µF) **or 3.3 V** (`V3` tied to `VCC`) | **[DOC]** §5.1 |
| Supply range, 3.3 V mode | **3.1 – 3.6 V** for CH340C/N/K/E/X/B (vs 2.9 – 3.6 V for CH340G/T/R) | **[DOC]** §6.3 |
| Supply range, 5 V mode | 4.0 – 5.3 V | **[DOC]** §6.2 |
| **Ambient temperature** | ⚠ **−20 … +70 °C** — *narrower* than the CH340G/T/R's −40 … +85 °C | **[DOC]** §6.1 |
| Baud range | **50 bps – 2 Mbps** | **[DOC]** §2 |
| Clock accuracy | ±0.8 % typ / **±1.2 % max** over −5…+55 °C; **±1.8 % max** over −25…+75 °C | **[DOC]** §6.4 |
| Operating current | 7 mA typ / 20 mA max @ 5 V; 4 mA typ / 12 mA max @ 3.3 V | **[DOC]** §6.2, §6.3 |
| USB-suspend current | **0.05 mA typ** @ 5 V (vs 0.09 mA for CH340G) | **[DOC]** §6.2 |
| Power-on reset | Built in; `VR` = 2.4/2.6/2.8 V, `TPR` = 20/35/50 ms | **[DOC]** §6.2, §6.4 |
| USB pull-up | **Built in.** `UD+`/`UD−` connect **directly** to the bus, *"without a series resistor"* | **[DOC]** §4 |
| 5 V-tolerant I/O | **Yes on lots whose lot number starts with `4`** | **[DOC]** §5.1 |
| Back-feed protection | **Yes on lot-`4`+ parts** — prevents current sinking into a powered-down CH340 from a live MCU | **[DOC]** §7.7, §7.8 |
| Lifecycle | **Active.** Covered by the current datasheet (v3.4 metadata / "Version 3D" cover, uploaded 2025-03-12) and by all current drivers | **[DOC]** |

### 1.1 ⚠ The "lot number starting with 4" clause

Two of the most useful CH340C properties — 5 V-tolerant I/O and back-feed protection — are **not** properties of the part number. WCH writes **[DOC]** §5.1:

> *"The IO of CH340X and CH340C/N **starting with lot number 4** support 5V withstand voltage to prevent inward current flow."*

and §7.8:

> *"CH340X and CH340C and CH340N **with lot numbers starting with 4** can also completely prevent the MCU power supply from sinking the current of the power-off CH340."*

**[INF] What this means in practice:** you cannot specify these behaviours on a purchase order, you cannot verify them from a distributor listing, and a reel from a different date code may not have them. Design as if they are absent — which is what both Soldered and Waveshare did, in different ways (§5.3, and [usb-uart-bridge §5](../../wch/ch340x/README.md#5-electrical-specifications-that-matter-here)).

### 1.2 The CH340 variant table

**[DOC]** `ch340-datasheet-v3.4.pdf` §3 and §4. The [CH340X record §1.1](../../wch/ch340x/README.md#11-ch340-variants-and-which-ones-are-10-pin) has a version of this focused on pin counts; this one is focused on **why you would pick each**.

| Part | Package | Pins | Pitch | Crystal | `CTS#` | `DTR#` | Distinguishing feature | Typical use |
|---|---|---:|---|---|---|---|---|---|
| **CH340C** | **SOP-16** | 16 | 1.27 mm | **integrated** | ✅ | ✅ | Drop-in for CH340G minus the crystal; pin 8 becomes `OUT#` | **Dev boards, ESP32 boards, anything hand-solderable that wants no crystal** |
| **CH340G** | SOP-16 | 16 | 1.27 mm | **external 12 MHz required** | ✅ | ✅ | The classic. Two more BOM lines (crystal + 2 caps) | Legacy designs, cheapest possible BOM per-chip |
| **CH340N** | SOP-8 | 8 | 1.27 mm | integrated | ❌ | ❌ | **`RTS#` only** — no `CTS#`, no `DTR#` at all | Smallest/cheapest. **Cannot do ESP32 auto-download** — one control line is not enough |
| **CH340E** | MSOP-10 | 10 | 0.50 mm | integrated | ✅ | ✅ | Tiny. Pin 6 is a plain output | Space-constrained boards |
| **CH340X** | MSOP-10 | 10 | 0.50 mm | integrated | ✅ | ✅ | **5 V-tolerant I/O by design (not lot-dependent)**; pin 6 `TNOW`⇄`DTR#` selectable by a 3–5.6 kΩ resistor | Space-constrained boards that also want one-click download with **no transistors** |
| CH340K | ESSOP-10 | 10 | 1.00 mm | integrated | ✅ | ✅ | Three built-in anti-back-feed diodes + weak pull-ups | Dual-supply designs (bridge on VBUS, MCU on its own rail) |
| CH340B | SOP-16 | 16 | 1.27 mm | integrated | ✅ | ✅ | **Built-in EEPROM** for a custom serial number / VID / PID; `RST#` on pin 7 | Products that need distinguishable serial numbers |
| CH340T | SSOP-20 | 20 | 0.65 mm | external | ✅ | ✅ | Clock output `CKO`, `ACT#`, `NOS#` | Legacy / full-modem designs |
| CH340R | SSOP-20 | 20 | 0.65 mm | external | ✅ | ✅ | IrDA SIR, inverted TXD/MODEM. **Discontinued** **[DOC]** | — |

**Why a designer picks CH340C specifically:**

1. **No crystal.** Removes a 12 MHz crystal and two load capacitors from the BOM, removes a placement, removes an oscillation-startup failure mode, and removes the layout constraint of keeping the crystal loop short.
2. **SOP-16 at 1.27 mm pitch is hand-solderable and rework-friendly**, unlike the MSOP-10 parts at 0.50 mm.
3. **Pin-for-pin with the CH340G on pins 1–6 and 9–16**, so an existing CH340G design converts by depopulating the crystal and its caps.
4. **Cheap and available**, and JLCPCB stocks it for assembly.

**What you give up versus the CH340G:** ±1.2–1.8 % clock accuracy instead of a ±30 ppm crystal (§7.1), and a **−20 … +70 °C** ambient range instead of −40 … +85 °C.

### 1.3 CH340C vs CH340G, pin by pin

The only differences are pins 7 and 8 **[DOC]** §4:

| Pin | CH340G | **CH340C** | CH340B |
|---:|---|---|---|
| 7 | `XI` — crystal input, needs a 12 MHz crystal + load cap | **`NC` — "Empty pin, must be suspended"** | `RST#` — external active-low reset with internal pull-up |
| 8 | `XO` — crystal output | **`OUT#` — a general-purpose MODEM output, software-defined, active low.** *"Some lot of CH340C can optionally be switched to the second `DTR#`"* | `NC` |

All other pins (`GND`, `TXD`, `RXD`, `V3`, `UD+`, `UD−`, `CTS#`, `DSR#`, `RI#`, `DCD#`, `DTR#`, `RTS#`, `R232`, `VCC`) are identical.

> **⚠ Pin 8 on a CH340C is `OUT#`, not `NC`.** It is a driven output, not a floating pin. Soldered's schematic symbol omits both pins 7 and 8 entirely, so `OUT#` is unbonded on these boards **[SCH]** — safe, but it means the extra software-controllable output the part offers is unavailable, and it means you cannot use the "second `DTR#`" trick that some CH340C lots support.

---

## 2. Pinout, SOP-16

**[DOC]** `ch340-datasheet-v3.4.pdf` §4, with the nets from `CTRL & COMS.kicad_sch` (Inkplate 5 V1.2.0) **[SCH]**.

| Pin | Name | Type | Datasheet function | Inkplate 5 net | What it does here |
|---:|---|---|---|---|---|
| 1 | `GND` | Power | Common ground, tied to USB bus ground | `GND` | |
| 2 | `TXD` | Output | Serial data out | `CH_TXD` | → `R24` **1 kΩ** → net `TXD` → ESP32 `RXD0` (pin 34) |
| 3 | `RXD` | Input | Serial data in; internal controllable pull-up/pull-down | `CH_RXD` | ← `R23` **1 kΩ** ← net `RXD` ← ESP32 `TXD0` (pin 35) |
| 4 | `V3` | Power | **5 V mode:** 0.1 µF to GND. **3.3 V mode:** tie to `VCC` | *(local)* | `C22` **100 nF** to GND ⇒ **5 V operation** |
| 5 | `UD+` | USB | D+, **direct to the bus, no series resistor** | `D+` | Straight to USB-C `K2` pins `A6`/`B6` |
| 6 | `UD−` | USB | D−, direct to the bus | `D-` | Straight to USB-C `K2` pins `A7`/`B7` |
| 7 | `NC` | — | **CH340C: empty, must be left floating** | *(not in symbol)* | Where a CH340G's 12 MHz crystal would be |
| 8 | `OUT#` | Output | **CH340C: general MODEM output, software-defined, active low** | *(not in symbol)* | Unused |
| 9 | `CTS#` | Input | Clear-to-send | *(floating)* | Unused — no hardware flow control |
| 10 | `DSR#` | Input | Data-set-ready | *(floating)* | Unused |
| 11 | `RI#` | Input | Ring indicator | *(floating)* | Unused |
| 12 | `DCD#` | Input | Carrier detect | *(floating)* | Unused |
| 13 | `DTR#` | **Output** | Data-terminal-ready | `DTR` | **Auto-reset:** base of `Q2` via `R26` 10 kΩ; emitter of `Q3`. §5 |
| 14 | `RTS#` | **Output** | Request-to-send | `RTS` | **Auto-reset:** base of `Q3` via `R27` 10 kΩ; emitter of `Q2`. §5 |
| 15 | `R232` | Input | Auxiliary RS-232 enable, **active high, internal pull-down** | *(floating)* | Floating ⇒ pulled down internally ⇒ **`RXD` not inverted**. Correct |
| 16 | `VCC` | Power | Positive supply, **requires an external 0.1 µF** | `VUSB` | **5 V from USB**, through `F1` 500 mA fuse. `C20` 100 nF |

Soldered's KiCad symbol has exactly **14 pins**, with 7 and 8 absent — an independent confirmation that the intended part is a crystal-less variant **[SCH]**:

```
1 GND   4 V3   9  CTS#  12 DCD#  15 R232
2 TXD   5 UD+  10 DSR#  13 DTR#  16 VCC
3 RXD   6 UD-  11 RI#   14 RTS#      (7, 8 absent)
```

The routed PCB agrees: pads **9, 10, 11, 12 and 15** appear in `Soldered Inkplate 5.kicad_pcb` as `unconnected-(U3-Pad9)` … `unconnected-(U3-Pad15)` **[SCH]**, so the four unused MODEM inputs and `R232` are genuinely floating by design, not merely un-labelled on the schematic.

---

## 3. Electrical parameters

**[DOC]** `ch340-datasheet-v3.4.pdf` §6.

### 3.1 Absolute maximum ratings

| Symbol | Parameter | Min | Max |
|---|---|---:|---:|
| `TA` | **Ambient, operating — CH340C/N/K/E/X/B** | **−20 °C** | **+70 °C** |
| `TA` | Ambient, operating — CH340G/T/R | −40 °C | +85 °C |
| `TS` | Storage | −55 °C | +125 °C |
| `VCC` | Supply | −0.5 V | **6.0 V** |
| `VIO` | Voltage on any input or output pin | −0.5 V | **`VCC` + 0.5 V** |

### 3.2 DC characteristics at `VCC` = 5 V (how these boards run it)

| Symbol | Parameter | Min | Typ | Max |
|---|---|---:|---:|---:|
| `VCC` | Supply, `V3` capacitor-only | 4.0 | 5 | 5.3 V |
| `ICC` | Operating current | — | **7 mA** | 20 mA |
| `ISLP` | USB-suspended current (CH340C/N/E/X) | — | **0.05 mA** | 0.15 mA |
| `VIL` | Low-level input | 0 | — | 0.9 V |
| `VIH` | High-level input | **2.3 V** | — | `VCC` |
| `VOL` | Low-level output (6 mA sink) | — | — | 0.5 V |
| `VOH` | **High-level output (2 mA source)** | **`VCC` − 0.6 V** | — | — |
| `IUP` | Input current, pins with internal pull-up | 3 | 150 | 300 µA |
| `IDN` | Input current, pins with internal pull-down | −40 | −100 | −300 µA |

### 3.3 ⚠ The 5 V-supply / 3.3 V-MCU level mismatch, and how these boards handle it

This is the most important electrical fact about the Inkplate implementation, and it is easy to miss.

**The boards run the CH340C at `VCC` = `VUSB` = 5 V** (`U3.4[V3]` → `C22` 100 nF → GND, which is the datasheet's 5 V configuration; `U3.16[VCC]` → `VUSB`) **[SCH]**. At 5 V:

- `VOH` ≥ `VCC` − 0.6 V ⇒ **the `TXD` pin idles at roughly 4.4 – 5.0 V**.
- The ESP32's `RXD0` (GPIO3) is on a **3.3 V** domain with an absolute maximum of `VDD` + 0.3 V ≈ **3.6 V**.

Feeding one directly into the other is out of spec.

**What Soldered did [SCH]:** `R23` and `R24`, both **1 kΩ**, in series on both UART lines:

```
U3.2 TXD ──[R24 1k]──> ESP32 pin 34 RXD0
U3.3 RXD <─[R23 1k]─── ESP32 pin 35 TXD0
```

**[INF]** The 1 kΩ in the `TXD` → `RXD0` direction limits current into the ESP32's ESD clamp diode to about (5.0 − 3.6) / 1 kΩ ≈ **1.4 mA**, comfortably inside what an ESP32 input pin tolerates. This is the conventional, widely-used mitigation for driving a 3.3 V ESP32 from a 5 V-powered CH340. It is not a level shifter, and the ESP32's input is being clamped rather than protected, but it works and it costs two 0603 resistors.

`R23` in the other direction is doing something different: the ESP32's `TXD0` drives 3.3 V into a `CH340C` input whose `VIH` at 5 V supply is **2.3 V** — comfortably satisfied, so no translation is needed. `R23` is there for symmetry, for edge-rate control, and to limit back-feed (§3.4).

> **[INF] If you are copying this design, the cleaner option is to run the CH340C at 3.3 V** — tie `V3` to `VCC` and feed both from the board's 3.3 V rail. Then everything is at one level and the series resistors become optional. Soldered chose 5 V-from-VBUS instead, which has one real advantage: **the bridge draws nothing from the battery rail when USB is unplugged.** On a device advertising 22 µA sleep current, that matters. Compare the Waveshare knob board, which does tie both pins to 3V3 and consequently pays tens of µA of bridge sleep current out of its own rail — see [usb-uart-bridge §9](../../wch/ch340x/README.md#9-open-questions).

### 3.4 The dual-supply / back-feed question

The Inkplate is exactly the case WCH's §7.7 warns about: **the bridge is on `VUSB`, the MCU is on a separate rail.** Two directions:

| Case | Risk | What the Inkplate has |
|---|---|---|
| **CH340C powered, ESP32 not** (USB in, board switched off) | 5 V on `TXD` flows through the ESP32's `RXD0` ESD diode into the dead 3V3 rail | `R24` 1 kΩ limits it. WCH's own fix is a Schottky (`BAT54`/`BAS70`) in series — not fitted **[SCH]** |
| **ESP32 powered, CH340C not** (running on battery, USB out) | 3.3 V on `TXD0` flows through the CH340C's `RXD` input diode into the dead `VUSB` rail, wasting battery | `R23` 1 kΩ limits it to ≲ 3.3 mA worst case. **Lot-`4`+ CH340C parts prevent it in silicon** **[DOC]** §7.8 — but see §1.1 |

WCH also recommends **a 2 kΩ–22 kΩ pull-up on the MCU's RX pin** in dual-supply designs, *"especially for baud rates of 120 Kbps or more"* **[DOC]** §7.7/§7.8. **There is no such pull-up on the Inkplate** **[SCH]** — the ESP32's internal `RXD0` pull-up (enabled by default on U0RXD) is doing that job. **[INF]** This works, and it is why the board is not in trouble at 115200; it would be worth revisiting if anyone tried to run this link at 921600 for faster flashing.

---

## 4. Role on these boards

Because the ESP32-D0WD (unlike the ESP32-S3) has **no native USB peripheral**, a bridge IC is mandatory — the Inkplate cannot enumerate as a USB device on its own. See [ESP32-WROVER](../../espressif/esp32-wrover/README.md).

Two practical consequences that follow from the bridge being a *separate chip*:

- **The serial port survives firmware crashes.** A wedged application cannot make `/dev/ttyUSB0` disappear, because the enumeration is done by `U3`, not by the ESP32. This makes an Inkplate noticeably easier to recover than an ESP32-S3 board with native USB-CDC, where a bad firmware image takes the port with it.
- **You may need a driver.** §6.

The bridge is also the transport for [Peripheral Mode](../../../devices/soldered-electronics/inkplate-5/features/peripheral-mode.md) — the Inkplate library's host-control protocol, whose default is **115200 baud** **[SRC]** (`InkplatePeripheralMode::begin(..., uint32_t _baud = 115200ULL, ...)`).

### 4.1 Which exact variant each board fits

**All three boards fit a CH340C in SOP-16.** Established independently from BOM value, footprint and symbol pin count:

| Board | Designator | BOM value | BOM footprint | Symbol pins | Source file |
|---|---|---|---|---:|---|
| **Soldered Inkplate 5** V1.2.0 | `U3` | `CH340C` | `SOP-16` | 14 (7, 8 absent) | `…/soldered-inkplate-5-hardware-design/OUTPUTS/V1.2.0/Soldered Inkplate 5 BOM.csv` line 42; `CAD/V1.2.0/CTRL & COMS.kicad_sch` |
| **Soldered Inkplate 5 Gen 2** V1.1.0 | `U3` | `CH340C` | `SOP-16` | 14 | `…/soldered-inkplate-5-gen2-hardware-design/OUTPUTS/V1.1.0/Soldered Inkplate 5 Gen2 BOM.csv` line 46 |
| **ZeroWriter Inkplate 5 Gen2** v1.2.0 | `U3` | `CH340C` | `Soldered footprints:SOP-16` | 14 | `…/Zerowriter Inkplate 5 Gen2/v1.2.0/OUTPUTS/Zerowriter Inkplate 5 Gen2.csv` |

**[SCH]** in all three cases. This is a stronger identification than the Waveshare board's, where the symbol carried no part number at all and the identity had to be argued from topology ([usb-uart-bridge §3](../../wch/ch340x/README.md#3-how-the-identification-was-made--the-full-chain)).

> **Cross-device note.** The two boards in this knowledge base that carry a WCH bridge carry **different CH340 variants**: **CH340C (SOP-16)** on the Inkplate family, **CH340X (MSOP-10)** on the [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md). They need the same driver but they implement download-mode entry in completely different ways — §5.4.

**Not present** on the ZeroWriter Keyboard PCB — that board is programmed through its own 6-pin `NOVA` header, not over USB. See [ESP32-WROOM-32U §7.1](../../espressif/esp32-wroom-32u/README.md#71-programming-this-board).

---

## 5. The DTR/RTS auto-reset circuit, as actually built

This is the part of a USB-UART bridge that people care about and that is almost never documented. The Inkplate implements the **classic cross-coupled two-transistor network**, and it does so correctly.

### 5.1 The topology

**[SCH]** `CTRL & COMS.kicad_sch`, Inkplate 5 V1.2.0 — identical on Inkplate 5 Gen 2 and on the ZeroWriter respin.

```
                  ┌──────── net DTR ──────────┬──[R26 10k]──┐
   U3.13 DTR# ────┤                           │             │
                  │                     Q3 emitter      Q2 base
                  │                                          │
                  │                                    Q2 (NPN, SOT-23)
                  │                                     collector
                  │                                          │
                  │                                    net MANUAL_RST
                  │                                          ├── R22 47k  -> 3V3
                  │                                          ├── C26 100n -> GND
                  │                                          ├── R33 47R  -> SW1 (reset button)
                  │                                          └── U2.4  MR  (TPS3840PL27 supervisor)
                  │
                  └──────── net RTS ──────────┬──[R27 10k]──┐
   U3.14 RTS# ────┤                           │             │
                                        Q2 emitter      Q3 base
                                                              │
                                                        Q3 (NPN, SOT-23)
                                                         collector
                                                              │
                                                        net GPIO_0
                                                              ├── R21 0R -> Q1 (DNP MOSFET)
                                                              ├── R46 330R -> JP7 (unpopulated)
                                                              └── U10.25  ESP32 IO0
```

Component values from the V1.2.0 BOM **[SCH]**: `Q2`, `Q3` = generic NPN in SOT-23-3; `R26`, `R27` = 10 kΩ; `R22` = 47 kΩ; `R33` = 47 Ω; `C26` = 100 nF; `R21` = 0 Ω; `R46` = 330 Ω.

### 5.2 Why the cross-coupling is the whole point

Each NPN conducts only when **its base is high AND its emitter is low**. Because `Q2`'s base is on `DTR` while its emitter is on `RTS`, and `Q3`'s base is on `RTS` while its emitter is on `DTR`, the truth table is:

| `DTR#` pin | `RTS#` pin | `Q2` (→ reset) | `Q3` (→ IO0) | Result |
|---|---|---|---|---|
| high | high | off | off | **nothing happens** |
| low | low | off | off | **nothing happens** |
| **high** | **low** | **on** | off | **`MANUAL_RST` pulled low ⇒ reset** |
| **low** | **high** | off | **on** | **`IO0` pulled low ⇒ boot strap = 0** |

> **⚠ This is why opening a serial monitor does not reset an Inkplate.** Most terminal programs assert **both** DTR and RTS on open. On this circuit that is row 2 — a no-op. Only the *sequence* esptool performs, which drives them to opposite states in turn, does anything.
>
> Contrast the [Waveshare knob board](../../wch/ch340x/README.md#63-serial-monitors--the-dtrrts-trap), which has **no** transistor network — `RTS#` goes straight to `EN` and `DTR#` straight to `GPIO0`. On that board any monitor that asserts DTR or RTS on open *does* reset the MCU or drop it into the bootloader. Same chip family, opposite behaviour, entirely because of two transistors.

### 5.3 Mapping onto esptool's reset sequence

WCH's MODEM outputs are active-low: when the host asserts DTR (`pyserial`'s `ser.dtr = True`), the `DTR#` **pin goes low** **[DOC]**. esptool's classic reset is:

| Step | `pyserial` | `DTR#` pin | `RTS#` pin | `Q2` | `Q3` | Board state |
|---|---|---|---|---|---|---|
| 1 | `dtr=False, rts=True` | **high** | **low** | **on** | off | **reset asserted**, `IO0` free (high) |
| 2 | *sleep 100 ms* | | | | | |
| 3 | `dtr=True, rts=False` | **low** | **high** | off | **on** | reset released; **`IO0` low** at the moment the strap latches ⇒ **ROM bootloader** |
| 4 | `dtr=False` | high | high | off | off | both released; chip is in download mode |

So `esptool --before default_reset` works unmodified. **[INF]** — derived from the schematic plus esptool's documented semantics; not instrumented on hardware.

### 5.4 ⚠ The reset does *not* go to `EN` directly — and that is a good thing

On a typical ESP32 dev board, the reset transistor's collector goes straight to `EN` with an RC. On the Inkplate it goes to **`MANUAL_RST`, which is the `MR` (manual reset) input of a `TPS3840PL27DBVR` voltage supervisor (`U2`)**. The supervisor's open-drain `RESET` output then drives net `RST`, which reaches **both**:

```
NET RST: U2.1[RESET], U10.3[EN], U9.24[~{RESET}]
```

**[SCH]** — i.e. the ESP32's `EN` **and** the [PCAL6416A](../../nxp/pcal6416a/README.md) I/O expander's `nRESET`.

Three consequences, all of them good:

1. **The reset pulse is clean and of a defined width**, generated by the supervisor rather than by an RC decaying through a transistor.
2. **The I/O expander is reset together with the ESP32.** That matters enormously on this board: the expander owns the EPD power sequencing, the microSD power switch and the panel's slow control lines. A reset that left the expander in an arbitrary state could leave the [TPS65186](../../texas-instruments/tps65186/README.md) rails up while the ESP32 rebooted.
3. **The same node is shared with the physical reset button** `SW1` (through `R33` 47 Ω) and with brown-out detection. One path, one behaviour.

The `R33` 47 Ω is current-limiting for the button against `C26`; `R22` 47 kΩ is the pull-up that holds `MR` high in the quiescent state.

`GPIO_0` also carries `R21` (0 Ω) to `Q1`, a **DNP** MOSFET whose gate is `GPIO_0_MOSFET` = the expander's `P1_0` — an unpopulated "let the expander force boot mode" feature. See [PCAL6416A §5.3](../../nxp/pcal6416a/README.md#53-p1_0-gpio0_enable-drives-an-unpopulated-part-on-inkplate-5).

### 5.5 The USB data path differs between the Soldered and ZeroWriter boards

This is the one genuine electrical difference between the stock Inkplates and the ZeroWriter respin, and it exists because **ZeroWriter moved the USB-C connector onto a separate PCB**.

| | **Soldered Inkplate 5 / Gen 2** | **ZeroWriter Inkplate 5 Gen2** |
|---|---|---|
| USB-C receptacle | `K2` `U262-161N-4BVC11`, **on the same board** | **On the breakout PCB** (`K1` there), reached over a 16-pin cable |
| `D+` path | `U3.5` ──── `K2.A6`/`K2.B6` | `U3.5` ─ **`R44` 22 Ω** ─ `U4.6`/`U4.1` (`USBLC6-2SC6`) ─ `K1.11` (`HC-1.25-16PWT`) ─ breakout ─ `K1.A6/B6` |
| `D−` path | `U3.6` ──── `K2.A7`/`K2.B7` | `U3.6` ─ **`R45` 22 Ω** ─ `U4.4`/`U4.3` ─ `K1.12` ─ breakout |
| Series resistors on the data pair | **none** | **`R44`, `R45` = 22 Ω** |
| ESD protection | **none on the data pair** | **`U4` `USBLC6-2SC6`** (SOT-23-6), `VBUS` on pin 5, GND on pin 2 |

**[SCH]**, verified against `Zerowriter Inkplate 5 Gen2-top-pos.csv` which places `R44` and `R45` as `22` in `0603R` at (13.70, 12.50) and (13.70, 10.50). The sibling agent's note about "R44/R45 22 R series resistors on the USB data lines" is **confirmed and now placed in the topology.**

> **Careful — `R44`/`R45` mean something different on the stock Inkplate.** On Soldered Inkplate 5 V1.2.0 and Gen 2 V1.1.0, `R44` and `R45` are **100 kΩ pull-ups on the microSD `MOSI` and `MISO` lines**, in the `SD & RTC` sheet, nowhere near USB **[SCH]**. Designator reuse across a respin is exactly the kind of thing that produces wrong cross-references.

**[INF] Why ZeroWriter added them.** 22 Ω series resistors on USB `D+`/`D−` are the textbook source-termination for a full-speed driver: the USB 2.0 specification wants a driver output impedance of 28–44 Ω, and adding ~22 Ω to a low-impedance CMOS driver lands in that window. On the stock Inkplate the run from the bridge to the connector is a few millimetres of controlled-ish trace and Soldered omitted them; on ZeroWriter the signal has to cross a board-to-board connector, a ribbon and a second PCB, so termination and ESD protection both become worth paying for. Note that WCH's datasheet says `UD+`/`UD−` should connect *"directly to the D+ data line of the USB bus **without a series resistor**"* **[DOC]** §4 — because the CH340 already integrates its own series/pull-up network. **These two positions are in tension.** ZeroWriter's 22 Ω is a deliberate deviation from the datasheet, presumably measured; at full speed (12 Mbit/s) the margin is large enough that it works either way. Flagged rather than resolved.

---

## 6. Drivers, per operating system

`1A86:7523` is the VID:PID for the **entire** CH340 line — you cannot tell a CH340C from a CH340G, N, E, K, X or B by enumeration **[DOC]** §5.2 (EEPROM defaults `VID = 1A86H`, `PID = 7523H`). The full WCH VID/PID table, extracted from WCH's own macOS driver, is in [usb-uart-bridge §4.1](../../wch/ch340x/README.md#41-read-the-usb-vidpid--the-first-thing-to-do).

### 6.1 Linux — nothing to do

The `ch341` driver has been in the mainline kernel for many years (`drivers/usb/serial/ch341.c`). Its ID table **[SRC]**, read from mainline on 2026-08-24:

```c
static const struct usb_device_id id_table[] = {
	{ USB_DEVICE(0x1a86, 0x5523) },   /* CH341 in serial mode */
	{ USB_DEVICE(0x1a86, 0x7522) },
	{ USB_DEVICE(0x1a86, 0x7523) },   /* <- CH340C lands here */
	{ USB_DEVICE(0x2184, 0x0057) },
	{ USB_DEVICE(0x4348, 0x5523) },   /* clone VID */
	{ USB_DEVICE(0x9986, 0x7523) },   /* clone VID */
	{ },
};
```

The device appears as `/dev/ttyUSB*`.

**Two Linux gotchas:**

- **`brltty` steals the port.** On Ubuntu and derivatives, the braille-display daemon claims `1A86:7523` and `/dev/ttyUSB0` vanishes a few seconds after plugging in. This is the single most common Linux CH340 complaint. Fix: `sudo systemctl mask brltty.path brltty.service` (and on some distributions, remove `/usr/lib/udev/rules.d/85-brltty.rules`).
- **Very old kernels have a broken baud-rate divisor.** The in-tree driver carries `CH341_QUIRK_LIMITED_PRESCALER` and `CH341_QUIRK_SIMULATE_BREAK` **[SRC]** for older chip variants. **[INF]** On any kernel from roughly 5.5 onward this is handled; below that, non-standard baud rates can be silently wrong.

WCH also ships a standalone out-of-tree driver, **`CH341SER_LINUX.ZIP` v1.8, uploaded 2024-10-24** **[DOC]**, held locally as `artifacts/ch341ser-linux-v1.8.zip` and verified byte-identical to the current download on 2026-08-24. It contains `ch341.c` (43 KB), `ch341.h`, a `Makefile` and a README. **[INF] You almost never need it** — build it only if you need a feature the in-tree driver lacks (WCH's version exposes more of the MODEM lines and some configuration ioctls).

### 6.2 macOS — the notarised-driver saga

**[WEB]/[INF]** — this is the least crisply-sourced part of this record and is labelled accordingly. The sequence, as best it can be reconstructed:

1. **Pre-2019: unsigned KEXTs.** WCH shipped a kernel extension. Users had to disable Gatekeeper protections or approve it in Security preferences. Third parties (notably a well-known independent build) circulated because WCH's own was often stale or unsigned.
2. **macOS 10.15 Catalina** tightened kext loading and required notarisation. Old CH340 kexts stopped loading, producing the classic "the port simply does not appear" symptom.
3. **macOS 11 Big Sur** deprecated kexts in favour of **DriverKit/DEXT**, and — importantly — **Apple added an in-box driver, `AppleUSBCHCOM`, that handles `1A86:7523` natively** **[WEB]**. On Big Sur and later, a CH340 often just works with nothing installed, appearing as `/dev/cu.usbserial-*` or `/dev/cu.wchusbserial*`.
4. **WCH's current answer is a DriverKit driver**, `CH34xVCPDriver`, distributed as `CH341SER_MAC.ZIP` / `CH34XSER_MAC.ZIP`, **v2.0, uploaded 2025-12-01**, 4.23 MB, and also on the Mac App Store. WCH's own description **[DOC]**: *"supports OS X 10.9~10.15, OS X 11 (Big Sur) and above, includes installation guide document."*

**[INF] Practical advice:** on macOS 11+, **plug it in first and look for `/dev/cu.usbserial*` before installing anything.** If you install WCH's driver *and* the in-box driver is active, you can end up with two device nodes for one chip, which confuses IDEs. If you must install, prefer the App Store version — it is notarised by construction.

Board vendors mirroring the macOS driver themselves (e.g. `https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z`) is a good signal for how often this bites people **[SRC]** — see [usb-uart-bridge §6.1](../../wch/ch340x/README.md#61-host-drivers).

### 6.3 Windows

| Item | Detail |
|---|---|
| Package | **`CH341SER.EXE` v4.0, uploaded 2026-06-24**, 780 KB **[DOC]** |
| Coverage | *"Windows 11/10/8.1/8/7/VISTA/XP/2000/98, Server 2025/2022/2019/2016/2012/2008/2003 −32/64-bit"* **[DOC]** |
| Signing | *"Microsoft WHQL/HCK Certified"* **[DOC]** |
| Scope | `CH340G, CH340C, CH340N, CH340K, CH340E, CH340B, CH340T, CH341A/F/T/B/C/U` **[DOC]** |
| Note | **`CH341SER`, not `CH343SER`.** The latter is for the `55Dx` PID family (CH343/CH9102) |

Windows 10 and 11 usually resolve `1A86:7523` through Windows Update without any manual install. When they do not, it is normally because the machine has no internet during first plug-in, or because an ancient `CH341SER` from a 2014-era vendor CD is already installed and wins.

**⚠ 64-bit Windows 7 is a special case.** WCH publishes a dedicated note — `InstallNoteOn64BitWIN7_EN.PDF` v1.0, *"Instructions for the driver after 18 years of August cannot be installed under some 64-bit WIN7"* **[DOC]** — held as `artifacts/wch-win7-x64-driver-install-note-v1.0.pdf`. The cause is Microsoft's 2018 move to SHA-2 driver signing: unpatched Win7 x64 installations cannot validate the newer signature and refuse the driver. The fix is Windows updates KB4474419/KB4490628, or an older driver revision.

### 6.4 Installing on a locked-down machine

**[INF]** This is a real, recurring practical problem — a corporate or school laptop where the user cannot install a driver, and the board therefore cannot be programmed. Options, roughly in order of how often they work:

1. **Try it first.** Windows 10/11 and macOS 11+ frequently need nothing. Do not assume you need admin rights until you have plugged it in.
2. **Windows Update** can deliver the WHQL driver without the user having local-admin rights, if the policy allows optional driver updates.
3. **A Linux live USB** needs no driver at all — `ch341` is in the kernel. This is the most reliable escape hatch.
4. **WSL2 with `usbipd-win`** works, but the *Windows* side still needs the driver first, so it does not help.
5. **Web-based flashing** — ESP Web Tools / ESP Launchpad via WebSerial in Chrome/Edge — needs the OS to present a serial port, so it also needs the driver. It removes the need to install *esptool*, not the driver.
6. **A different bridge.** If you control the hardware, an ESP32-S3 with native USB-CDC enumerates as a standard CDC-ACM device and needs no vendor driver on any modern OS. **[INF]** This is one of the underrated arguments for native-USB parts.

### 6.5 Counterfeits and clones

**[INF]/[WEB]** — general industry observation, not measured in this pass.

- The CH340 is itself the cheap alternative that displaced FTDI, and it is now cheap enough to be worth cloning. Clone VIDs `4348:5523` and `9986:7523` are in the mainline Linux ID table **[SRC]**, which is direct evidence that non-WCH silicon shipping the CH341 protocol exists in the wild.
- Reported symptoms: baud-rate inaccuracy (worse than the ±1.2 % the genuine part specifies), enumeration failures, and instability above ~115200.
- **Unlike FTDI, WCH has never shipped a driver that deliberately bricks non-genuine parts.** If a `1A86:7523` device misbehaves on Windows, the overwhelmingly likely cause is a stale driver, not counterfeiting.
- **[INF]** For a CH340C specifically, the integrated oscillator is the thing most likely to be substandard on a clone, and it is the thing you would notice as marginal framing errors at high baud.

---

## 7. Pitfalls, ranked

1. **Assuming the datasheet filename tells you the version.** The file held here is `ch340-datasheet-v3.4.pdf` — WCH's *metadata* version — but **the PDF's own cover says "Version: 3D"**. Both refer to the same document (id 79, uploaded 2025-03-12). The `wch/ch340x` copy is named `ch340-datasheet-v3d.pdf` and is **byte-identical** (md5 `2ca320c5f1085c404d48215b5a6dbf75`). §9.
2. **Baud accuracy at high rates.** The integrated oscillator is **±1.2 % over −5…+55 °C and ±1.8 % over −25…+75 °C** **[DOC]**. A UART link tolerates roughly ±2 % *total* across both ends for 8N1. At room temperature this is fine. Near the temperature limits, with a sloppy MCU baud divisor at the other end, framing errors become plausible. **[INF] If you need 921600 for fast flashing and the device runs hot, a CH340G with a real crystal is the more conservative part.**
3. **The −20 … +70 °C ambient limit.** Narrower than the CH340G. An Inkplate in a car windscreen in summer is outside it. **[INF]** The failure mode is degraded clock accuracy, not damage.
4. **Auto-reset capacitor / spurious resets on serial-monitor open.** On the Inkplate this is *designed out* by the cross-coupled network (§5.2) — but the moment you add your own DTR-driven reset RC, or move to a board like the Waveshare knob that lacks the network, opening a monitor resets the target. Fixes per tool are tabulated in [usb-uart-bridge §6.3](../../wch/ch340x/README.md#63-serial-monitors--the-dtrrts-trap).
5. **Latency.** The CH340 is a USB **full-speed bulk** device. Round-trip latency is dominated by the 1 ms USB frame and by the driver's read timeout, typically giving **1–4 ms** turnaround regardless of baud rate. **[INF] Do not build a tight request/response protocol that depends on sub-millisecond turnaround over a CH340.** Inkplate Peripheral Mode's line-oriented protocol at 115200 is well inside this.
6. **Expecting hardware flow control.** `CTS#`, `DSR#`, `RI#`, `DCD#` are all **floating** on these boards **[SCH]**. Enabling RTS/CTS will hang the link, because `RTS#` is wired to the reset network, not to flow control.
7. **Leaving pin 15 `R232` floating and worrying about it.** Floating is correct — it has an internal pull-down, so RS-232 inversion stays off **[DOC]**.
8. **Adding series resistors to `UD+`/`UD−`.** WCH says not to **[DOC]** §4. ZeroWriter did anyway, for board-to-board reasons; understand why before copying it. §5.5.
9. **Assuming `R44`/`R45` mean the same thing on every board in this family.** They do not. §5.5.
10. **Installing `CH343SER` instead of `CH341SER`.** Different PID family, wrong driver.
11. **Treating a CH340N as a drop-in.** It has neither `CTS#` nor `DTR#` **[DOC]** §4 — it physically cannot drive a two-line auto-reset network.
12. **Powering the bridge from 5 V and the MCU from 3.3 V without series resistors.** §3.3. `VOH` is `VCC` − 0.6 V, i.e. ~4.4 V into a 3.6 V-max pin.

---

## 8. Alternatives and equivalents

| Part | Drop-in for `U3`? | Comment |
|---|---|---|
| **CH340C** | — | The fitted part |
| **CH340G** | ⚠ **Pads yes, function no** | Same SOP-16 pinout on 1–6 and 9–16, but pins 7/8 become `XI`/`XO` and **it will not run without a 12 MHz crystal and two load caps**, which the board does not have. Wider temperature range if you add them |
| **CH340B** | ⚠ pads yes | Same package, integrated clock, adds an EEPROM for a custom serial number. **Pin 7 becomes `RST#` with an internal pull-up** — floating is fine. **[INF] The obvious upgrade if you want per-unit USB serial numbers** |
| CH340N | ❌ | SOP-8. No `CTS#`, no `DTR#` — cannot do auto-reset |
| CH340E / CH340X | ❌ | MSOP-10, 0.50 mm pitch. Different footprint entirely. CH340X can do one-click download **with no transistors** (see [usb-uart-bridge §2.1](../../wch/ch340x/README.md#21--r14-is-not-a-series-resistor-it-is-the-mode-select-resistor)) |
| CH340K | ❌ | ESSOP-10. Best-in-family back-feed protection for dual-supply designs |
| **CH9102F** | ❌ | QFN-24. WCH's higher-end bridge: better baud accuracy, higher rates, **different PID (`1A86:55D4`) and a different driver** |
| CH343P | ❌ | QFN-16. Up to 6 Mbps, separate `VIO` pin for clean level translation |
| **CP2102N** | ❌ | Silicon Labs, QFN-20/24/28. In-box drivers on all three OSes; more expensive; the conservative choice for products shipped to non-technical users |
| **FT232RL / FT231XS** | ❌ | FTDI, SSOP-28/SSOP-20. Best driver situation, worst price, and a well-known history of driver-side hostility to clones |
| **Nothing — use a native-USB MCU** | ❌ (redesign) | An ESP32-S3 or ESP32-C3 enumerates as CDC-ACM with no vendor driver at all. Costs you the "serial port survives a firmware crash" property (§4) |

---

## Manufacturer

**WCH (Nanjing Qinheng Microelectronics, 南京沁恒微电子)** — see the [WCH documentation-sourcing guide](../../../vendors/wch/README.md) for this vendor's document portals, the Chinese/English datasheet split, driver downloads and known gotchas. In particular: **every HTML path on `wch-ic.com` returns HTTP 200 with a 4,305-byte SPA shell**, so a naïve `curl` of a datasheet URL looks like a success and yields HTML. Use the JSON API.

## Used By

| Device | Designator | Notes |
|---|---|---|
| [Soldered Inkplate 5](../../../devices/soldered-electronics/inkplate-5/README.md) | `U3` | USB-C receptacle on the same board |
| [Soldered Inkplate 5 Gen 2](../../../devices/soldered-electronics/inkplate-5-gen2/README.md) | `U3` | USB-C receptacle on the same board |
| [ZeroWriter Ink](../../../devices/zerowriter/zerowriter-ink/README.md) | `U3` | Bridge retained on the main board, but the **USB-C connector moved to a separate breakout PCB**. `D+`/`D−` reach it through `R44`/`R45` 22 Ω, a `USBLC6-2SC6` ESD array (`U4`) and the 16-pin `HC-1.25-16PWT` inter-board link **[SCH]** |

**Not present** on the ZeroWriter Keyboard PCB — that board is programmed through its own 6-pin `NOVA` header, not over USB.

## Related pages

- **[wch/ch340x — the CH340-family record](../../wch/ch340x/README.md)** — the CH340X identification, the full VID/PID table from WCH's driver, the serial-monitor DTR/RTS fixes per tool, and the pin-6 mode-strap analysis. **Read it alongside this page**
- [espressif/esp32-wrover](../../espressif/esp32-wrover/README.md) — the processor it programs; it has no native USB, which is why this part is mandatory
- [espressif/esp32-wroom-32u §7.1](../../espressif/esp32-wroom-32u/README.md#71-programming-this-board) — the *other* ESP32 in ZeroWriter Ink, which this bridge cannot reach
- [nxp/pcal6416a](../../nxp/pcal6416a/README.md) — reset-shared with the ESP32 through the same supervisor (§5.4)
- [texas-instruments/bq25306](../../texas-instruments/bq25306/README.md) — shares the `VUSB` rail on ZeroWriter Ink
- [wch/ch445p](../ch445p/README.md) · [wch/ch334r](../ch334r/README.md) · [wch/ch32v203c8t6](../ch32v203c8t6/README.md) — the other WCH parts documented here
- [Inkplate 5 Peripheral Mode](../../../devices/soldered-electronics/inkplate-5/features/peripheral-mode.md) — the protocol this bridge carries at 115200 baud

---

## 9. Open questions

| Question | Status |
|---|---|
| Lot code of the fitted CH340C — does it have 5 V-tolerant I/O and back-feed protection? | **Open, and unresolvable from files.** §1.1. Requires reading the marking on a physical part |
| Is the ZeroWriter 22 Ω series termination measured, or copied from a generic USB reference? | **Open.** It contradicts WCH's explicit "no series resistor" instruction. §5.5 |
| Does the auto-reset sequence in §5.3 behave as derived on real hardware? | **Open, [INF] only.** Derived from schematic + esptool semantics; not instrumented |
| Maximum reliable flashing baud on these boards | **Open.** No pull-up on the ESP32 RX beyond the internal one, which WCH flags as marginal above 120 kbps in dual-supply designs (§3.4). 115200 is known-good from Peripheral Mode **[SRC]** |
| Whether Apple's in-box `AppleUSBCHCOM` covers all CH340 PIDs or only `7523` | **Open [WEB].** Not verified against a macOS system in this pass |

---

## 10. Local artifacts and sources

### Artifacts held

| File | Document | Version | Bytes | sha256 |
|---|---|---|---:|---|
| `artifacts/ch340-datasheet-v3.4.pdf` | **WCH CH340 Datasheet.** Cover says **"Version: 3D"**; WCH's file metadata says version **3.4**. Same document. Covers `CH340G, CH340C, CH340B, CH340N, CH340K, CH340E, CH340X, CH340T, CH340R` | 3.4 / "3D" | 325,640 | `4d7b150edfda88e44eb8f499c22693318666968125ff17f652ca9983d9929e5e` |
| `artifacts/ch341ser-linux-v1.8.zip` | WCH out-of-tree Linux driver `CH341SER_LINUX` (`ch341.c` 43 KB, `ch341.h`, `Makefile`, README) | v1.8, uploaded 2024-10-24 | 13,449 | `a7e0d7251d3cf8f8bc7b989332e2d9e3a43f0ac2da5013b1e5afe059a71e87c7` |
| `artifacts/wch-win7-x64-driver-install-note-v1.0.pdf` | WCH note: *"Instructions for the driver after 18 years of August cannot be installed under some 64-bit WIN7"* — the SHA-2 driver-signing problem. **Added 2026-08-24** | v1.0, 2019-01-10 | 364,123 | `9004941068d25d59617b61f9398950d9c8a8d660f0fa4afd91f9e0272659997c` |

**Note on the datasheet filename.** `artifacts/ch340-datasheet-v3.4.pdf` here and `../../wch/ch340x/artifacts/ch340-datasheet-v3.4.pdf` are the **same file** — md5 `2ca320c5f1085c404d48215b5a6dbf75` for both. Neither name is wrong: `3.4` is WCH's metadata `version` field, `3D` is the string on the PDF's cover page. Both were re-verified against the live download on 2026-08-24 and are **current**, not stale.

Not held, and deliberately so: the macOS and Windows driver binaries. They are large, they change often, and installing a mirrored copy is worse practice than fetching the current one. URLs are in §10 below.

#### Reacquire

```sh
# ⚠ Do NOT use https://www.wch-ic.com/downloads/CH340DS1_PDF.html — every HTML path on this
#   host returns HTTP 200 with a 4,305-byte SPA shell whether the document exists or not.

# 1. Metadata (name, version, uploadTime, and the all-important `scope` field):
curl -sS 'https://www.wch-ic.com/api/official/website/files/getFilesById?id=79'

# 2. The PDF itself:
curl -sSL -o ch340-datasheet-v3.4.pdf 'https://www.wch-ic.com/download/file?id=79'
head -c 4 ch340-datasheet-v3.4.pdf | od -An -c        # expect  %  P  D  F

# Other useful ids on this host (verified 2026-08-24):
#   id=177  CH341SER_LINUX.ZIP  v1.8   2024-10-24
#   id=178  CH341SER_MAC.ZIP    v2.0   2025-12-01   (also id=334, same file)
#   id=65   CH341SER.EXE        v4.0   2026-06-24   (Windows, WHQL)
#   id=195  CH341SER_ANDROID.ZIP v2.3  2025-08-29
#   id=283  InstallNoteOn64BitWIN7_EN.PDF v1.0
#   id=340  CH34xSerCfg.ZIP     v1.5   (serial-number / config tool)

# The CH340 PDF is AES-256 encrypted with an EMPTY user password.
#   poppler:  pdftotext -layout ch340-datasheet-v3.4.pdf -
#   python:   pip install pypdf cryptography; PdfReader(...).pages[n].extract_text()
```

Enumerating the whole file table works but **throttle to ≤ ~24 concurrent requests** — above that the API times out silently and returns a partial enumeration that looks complete. A 12-way `xargs -P 12` over ids 1–400 completed cleanly on 2026-08-24.

### Retrieval failures, 2026-08-24

None for this part. Everything needed resolved on the first attempt through the JSON API with a **plain default User-Agent** — no UA substitution required. The held datasheet was verified byte-identical to the current live download, as was the Linux driver zip, so **no re-download was necessary**. Recorded in [`component-download-failures.txt`](../../../component-download-failures.txt) as a positive control for this host.

### Design files read

| File | Used for |
|---|---|
| `devices/soldered-electronics/inkplate-5/artifacts/hardware/soldered-inkplate-5-hardware-design/CAD/V1.2.0/CTRL & COMS.kicad_sch` | `U3` symbol (14 pins — 7/8 absent), every net in §2, the whole auto-reset network in §5.1 |
| `…/CAD/V1.2.0/Soldered Inkplate 5.kicad_pcb` | **Independent net cross-check of every §2 and §5 claim.** Confirms `U3.4`→`C22` only (5 V mode), `U3.16`→`VUSB`, `D+`/`D−` direct to `K2` with no series parts, `Q2`/`Q3` base/emitter/collector assignments, and that pads 9, 10, 11, 12 and 15 are formally `unconnected-(U3-PadNN)` |
| `…/OUTPUTS/V1.2.0/Soldered Inkplate 5 BOM.csv` | `U3 = CH340C`, package `SOP-16` (line 42); `R23`/`R24` 1 kΩ; `R26`/`R27` 10 kΩ; `R22` 47 kΩ; `R33` 47 Ω; `C20`/`C22` 100 nF; `R44`/`R45` **100 kΩ** (the microSD pull-ups, §5.5) |
| `…/CAD/V1.2.0/SD & RTC.kicad_sch` | Confirms `R44`/`R45` are microSD pull-ups on the stock board |
| `devices/soldered-electronics/inkplate-5-gen2/artifacts/hardware/soldered-inkplate-5-gen2-hardware-design/CAD/V1.1.0/CTRL & COMS.kicad_sch` + `OUTPUTS/V1.1.0/…BOM.csv` | Gen 2 is electrically identical: `U3 = CH340C` SOP-16, same `Q2`/`Q3`/`R26`/`R27`, **no** series resistors, **no** ESD array |
| `devices/zerowriter/…/design/src/Zerowriter Inkplate 5 Gen2/v1.2.0/CAD/CTRL & COMS.kicad_sch` | `R44`/`R45` **22 Ω** in series, `U4 USBLC6-2SC6`, `D+`/`D+*`/`D+**` net chain to `K1.11`/`K1.12` |
| `…/Zerowriter Inkplate 5 Gen2/v1.2.0/PCBA/Zerowriter Inkplate 5 Gen2-top-pos.csv` | Per-designator values confirming `R44`,`R45` = `22`, `R23`,`R24` = `1k`, `R26`,`R27` = `10k` |
| `…/Zerowriter breakout board/v1.2.0/OUTPUTS/Zerowriter breakout board.csv` | The far end of the USB path: `K1` `U262-161N-4BVC11` USB-C, `R1`/`R2` 5k1 CC pull-downs, `F1` 350 mA polyfuse, `K3` `HC-1.25-16PWT` |

### Source files read

| File | Used for |
|---|---|
| `Inkplate-Arduino-library/examples/Inkplate5V2/Diagnostics/Peripheral_Mode/InkplatePeripheralMode.h` L73 | Default baud **115200** for Peripheral Mode |
| Linux mainline `drivers/usb/serial/ch341.c` | The `id_table` in §6.1, including the two clone VIDs; the baud-rate quirk flags |
| `artifacts/ch341ser-linux-v1.8.zip` | WCH's out-of-tree driver contents |

### Authoritative sources

| Title | URL | Retrieved | Version | Local artifact |
|---|---|---:|---|---|
| **WCH CH340 Datasheet** (packages §3, pins §4, function §5, parameters §6, applications §7) | https://www.wch-ic.com/download/file?id=79 | 2026-08-24 | 3.4 / "3D" | `artifacts/ch340-datasheet-v3.4.pdf` |
| WCH file metadata API — `name`, `version`, `uploadTime`, `scope` | https://www.wch-ic.com/api/official/website/files/getFilesById?id=79 | 2026-08-24 | — | – |
| WCH `CH341SER_LINUX` driver | https://www.wch-ic.com/download/file?id=177 | 2026-08-24 | v1.8 (2024-10-24) | `artifacts/ch341ser-linux-v1.8.zip` |
| WCH `CH341SER_MAC` / `CH34XSER_MAC` driver (macOS, DriverKit) | https://www.wch-ic.com/download/file?id=178 · https://www.wch-ic.com/download/file?id=334 | 2026-08-24 | **v2.0 (2025-12-01)** | – |
| WCH `CH341SER.EXE` (Windows, WHQL-certified) | https://www.wch-ic.com/download/file?id=65 | 2026-08-24 | **v4.0 (2026-06-24)** | – |
| WCH `CH341SER_ANDROID` | https://www.wch-ic.com/download/file?id=195 | 2026-08-24 | v2.3 (2025-08-29) | – |
| WCH 64-bit Windows 7 driver-signing install note | https://www.wch-ic.com/download/file?id=283 | 2026-08-24 | v1.0 | `artifacts/wch-win7-x64-driver-install-note-v1.0.pdf` |
| Linux `ch341` driver source — VID/PID table, baud quirks | https://raw.githubusercontent.com/torvalds/linux/master/drivers/usb/serial/ch341.c | 2026-08-24 | mainline | – |
| esptool documentation — reset sequences, `--before` / `--after` | https://docs.espressif.com/projects/esptool/en/latest/esp32/ | 2026-08-24 | latest | – |
| Soldered Inkplate 5 hardware design (KiCad, TAPR OHL) | https://github.com/SolderedElectronics/Soldered-Inkplate-5-hardware-design | 2026-08-24 | V1.2.0 | `devices/soldered-electronics/inkplate-5/artifacts/hardware/` |

> **Evidence boundary.** §§1–3 are **[DOC]** from the CH340 datasheet, quoted or tabulated directly. §§2, 4, 5 net-level claims are **[SCH]** from S-expression net extraction over the KiCad sources named above — and, importantly, **cross-checked independently against the routed `.kicad_pcb` netlist**, which is post-ERC and therefore authoritative where the schematic sheets are ambiguous. Both extractions agree on every `U3` connection. §5.3's esptool mapping is **[INF]** — logically derived, not instrumented. §6.2's macOS history is **[WEB]/[INF]** and is the weakest-sourced section here; the driver **versions and dates** in it are **[DOC]** from WCH's metadata API, but the narrative around Catalina/Big Sur is reconstructed. §6.5 on counterfeits is **[INF]** except for the clone VIDs, which are **[SRC]** from the kernel. Nothing in this record was verified on physical hardware.
