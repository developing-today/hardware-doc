# WCH CH334R

> 4-port USB 2.0 high-speed hub controller in QSOP-16. The `R` suffix is one package variant of a family covered by a single datasheet, `CH334DS1`.
> Research snapshot **2026-08-30**. Fitted as `U5` on the Nicolai Electronics Tanmatsu. **No hardware was available.**

---

## Evidence labelling

| Tag | Meaning |
|---|---|
| **[DOC]** | WCH **CH334/335 Datasheet V2.91**, uploaded **2026-08-28**, 34 pp — `artifacts/ch334ds1.pdf` |
| **[PCB]** | `tanmatsu.kicad_pcb` pad→net assignments (CERN-OHL-P) |
| **[INF]** | Author inference |

> The datasheet PDF is **encrypted** (owner password, empty user password) — a known WCH pattern documented in [`vendors/wch/README.md`](../../../vendors/wch/README.md) §5. `pypdf` and `pdftotext` both read it transparently.

---

## 1. Identity and family

| Property | Value | Source |
|---|---|---|
| Part | **CH334R** — QSOP-16 | BOM, [DOC] §1.1 |
| Function | **4-port USB 2.0 hub controller** | [DOC] |
| Upstream | USB 2.0 **high-speed and full-speed** | [DOC] |
| Downstream | High-speed **480 Mbit/s**, full-speed 12 Mbit/s, low-speed 1.5 Mbit/s | [DOC] |
| Transaction translator | **STT** (single TT, time-shared across 4 ports) **or MTT** (4 TTs, concurrent) | [DOC] |
| USB pin ESD | **6 kV enhanced, Class 3A** | [DOC] §Features |
| Datasheet | **`CH334DS1.PDF` V2.91**, 2026-08-28 | [DOC] |
| LCSC | [`C4154405`](https://www.lcsc.com/search?q=C4154405) | BOM |

### 1.1 The datasheet covers ten parts, and finding it requires searching `scope`

`CH334DS1.PDF`'s `scope` field lists:

> `CH334F, CH334H, CH334L, CH334P, **CH334R**, CH334S, CH334U, CH334X, CH335F, CH335P`

**There is no "CH334R datasheet".** WCH publishes one document per family, named after the first member — the trap that [`vendors/wch/README.md`](../../../vendors/wch/README.md) §5 documents at length. The variants differ in package and pin count, not in core function.

**CH335** additionally provides **USB 3.0 SuperSpeed passthrough** on one downstream port, and supports a 9-LED indicator configuration. **CH334 does not.** If a design needs USB 3.0, the CH334R is the wrong part.

---

## 2. Notable features **[DOC §Features]**

- **4 downstream USB 2.0 ports**, backward compatible with USB 1.1.
- **Per-port independent power control, or GANG (ganged) linkage control.**
- **Per-port independent over-current detection, or overall GANG detection.**
- **Self-powered or bus-powered**, configurable via I/O pins or an external EEPROM.
- **Built-in information memory** — manufacturer/product strings and configuration can be customised in bulk **without an EEPROM**.
- **Built-in 1.5 kΩ pull-up on the upstream port and the pull-downs required on downstream ports** — no external resistors.
- **Built-in LDO** converting the USB bus supply to the chip's 3.3 V.
- **Built-in high-precision clock** — *"you can choose to remove the external 12 MHz crystal to save costs, reduce size and reduce EMI"*.
- **Crystal oscillator with built-in load capacitors**; supports external 12 MHz input. Internal PLL generates 480 MHz for the PHY.
- Self-developed USB PHY with **LPM low-power technology**, *"significantly reduced compared to the first generation of HUB chips"*.
- Downstream port status **LED indicator** control — green on = normal, green off = no device or suspended, red on = port abnormal. 1-LED, 5-LED (and on CH335, 9-LED) configurations. Current-limiting resistors 100 Ω – 1 kΩ (200 Ω – 1 kΩ for the single-LED `LED4` mode).

---

## 3. `RESET#/CDP` — the strapping pin, and the only real configuration decision

This single pin does three different things depending on how it is driven **at power-up**.

**Electrical [DOC §3.2]:** built-in pull-up of about **25 kΩ**. To reset externally, drive it low with a source impedance **≤ 800 Ω**, with a low pulse **> 4 µs**.

**Table 3-2, Reset Pin Control and Mode Description [DOC]** — verbatim:

| `RESET#/CDP` | Condition | Result |
|---|---|---|
| **Driven low** | During power-up **or** normal operation | **Reset the HUB chip** |
| **Driven high** | **During power-up** | **Enable CDP**, and **turn off low-power sleep** |
| **No drive / no connection (default)** | During power-up | **No CDP. Low-power sleep supported** |
| Driven high, or no drive | During **normal** operation | **No effect** |

> ⚠ **CDP is Charging Downstream Port** — the USB battery-charging mode that lets a downstream device draw more current. **Enabling it also disables low-power sleep**, permanently raising idle current.

### 3.1 ⚠ The MCU-GPIO trap, called out by the vendor

[DOC §3.2] warns explicitly:

> *"For applications where the MCU pin directly drives the `RESET#/CDP` pin of the HUB chip, if the MCU pin outputs a high level during power-up, it may enable the charging function of CH334/CH335 and turn off the low-power sleep."*

Most MCU GPIOs are inputs with weak pull-ups at reset, or briefly drive high during initialisation. Either behaviour **silently enables CDP and kills sleep** — an idle-current regression with no other symptom.

**The vendor's fix** (Figure 3-2-2) is a **series Schottky diode** between the MCU pin and `RESET#/CDP`, oriented so the MCU can pull the pin *low* but never drive it *high*. The internal 25 kΩ pull-up then handles the release. This is a one-component fix that is very easy to omit.

⚠ [DOC] also notes: *"CDP is a configurable function, some package forms / partial lots of CH334/5 may not open CDP."* So the feature's availability is not guaranteed across lots — do not design a product around it without confirming with WCH.

---

## 4. Exact wiring on the Tanmatsu **[PCB]**

| Pin | [DOC] name | Net | Goes to |
|---:|---|---|---|
| **1** | `DM4` | `/Radio/C6_USB1_N` | **ESP32-C6** USB D− |
| **2** | `DP4` | `/Radio/C6_USB1_P` | **ESP32-C6** USB D+ |
| **3** | `DM3` | `/Application processor/USB1_P1_N` | **ESP32-P4** USB PHY 1 D− |
| **4** | `DP3` | `/Application processor/USB1_P1_P` | **ESP32-P4** USB PHY 1 D+ |
| **5** | `DM2` | `/UNUSED_USB_N` | **`TP1`** (test point, silkscreened `D-`) |
| **6** | `DP2` | `/UNUSED_USB_P` | test point |
| **7** | `DM1` | `HUB_USB1_N` | **Internal add-on port** pin 4 |
| **8** | `DP1` | `HUB_USB1_P` | **Internal add-on port** pin 2 |
| **9** | **`RESET#/CDP`** | **unconnected** | ⚠ see §4.2 |
| **10** | upstream `DM` | `/USB_DEVICE_N` | The **USB-C** connector |
| **11** | upstream `DP` | `/USB_DEVICE_P` | The **USB-C** connector |
| 12, 13 | `VDD33` | `+3.3V` | Externally supplied — the internal LDO is not relied on |
| 14 | `GND` | `GND` | |
| **15** | `XO` | `Net-(U5-XO)` | External **12 MHz crystal** |
| **16** | `XI` | `Net-(U5-XI)` | same crystal |

### 4.1 ⚠ The port numbering in the device record is wrong

[`pinouts-and-buses.md` §6](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md) documents the topology as *"Port 1 → ESP32-P4, Port 2 → ESP32-C6, Port 3 → internal add-on port"*. Against the datasheet's pin names **[DOC §1.1]** and the netlist **[PCB]**, the actual mapping is:

| Physical port | Pins | Actually connected to |
|---|---|---|
| **Port 1** (`DM1`/`DP1`) | 7, 8 | **Internal add-on port** |
| **Port 2** (`DM2`/`DP2`) | 5, 6 | **Unused** — test points only |
| **Port 3** (`DM3`/`DP3`) | 3, 4 | **ESP32-P4** |
| **Port 4** (`DM4`/`DP4`) | 1, 2 | **ESP32-C6** |

The *set* of three consumers is correctly described; the port numbers are not. This matters for anyone using per-port power control or reading per-port status, and for interpreting hub topology in `lsusb -t` on a host. **This is a device-side correction** — see the session report.

Note also that the 4th port is not merely "unused": `DM2`/`DP2` are routed to **test points**, so a fourth device can be bodged on.

### 4.2 ✅ `RESET#/CDP` floating is the correct configuration here

Pin 9 is **unconnected** **[PCB]**. Per Table 3-2 (§3), *"no drive or no connection (default) during power-up"* gives:

> **No CDP enabled, low-power sleep support**

For a battery-powered handheld this is the right choice, and it is achieved by doing nothing — the internal 25 kΩ pull-up holds the pin high after power-up, where it has "no effect". The board gets low-power sleep and forgoes CDP charging, and it entirely sidesteps the §3.1 MCU-GPIO trap by not connecting an MCU at all.

The trade: **the hub cannot be reset by firmware.** A wedged hub needs a power cycle. Given that the hub sits between the USB-C socket and both processors, that is a real, if remote, recovery gap. [INF]

### 4.3 The external crystal is fitted although the datasheet says it is optional

`XI`/`XO` (pins 16, 15) carry their own nets **[PCB]**, so a **12 MHz crystal is fitted**, despite [DOC §Features] offering a *"built-in professional high-precision clock"* that allows removing it *"to save costs, reduce size and reduce EMI"*.

Choosing the crystal anyway is the conservative option: USB high-speed has tight frequency tolerance, and a crystal removes any doubt. Whether that was deliberate or inherited from a reference design is not documented. [INF]

### 4.4 Consequences of the topology

```
USB-C (J1) ── upstream (pins 10/11) ── CH334R ─┬─ port 3 ─► ESP32-P4 USB PHY 1
                                               ├─ port 4 ─► ESP32-C6 USB-serial/JTAG
                                               ├─ port 1 ─► internal add-on port (pins 2/4)
                                               └─ port 2 ─► test points (unused)
```

- **Each processor keeps an independent USB device interface** rather than multiplexing one — the reason to fit a hub at all.
- The **ESP32-P4's PHY 1 defaults to USB-serial/JTAG** but firmware can replace it with a custom device; this is how **BadgeLink** (WebUSB) works.
- Because the ROM exposes USB-serial/JTAG unconditionally, **the P4 can always be flashed even with no valid firmware**.
- **Power control and over-current detection are unused on this board** — no `PGANG` or `OVCUR#` nets appear, consistent with the QSOP-16 CH334R's reduced pin count. Downstream port power comes from elsewhere; the USB-A host port is switched by a separate `SY6280AAC` (`U14`).

---

## 5. Pitfalls, in priority order

1. **Never let an MCU drive `RESET#/CDP` high at power-up.** It enables CDP and disables sleep. Use the vendor's series Schottky. §3.1.
2. **Leave `RESET#/CDP` unconnected** if you want low-power sleep and do not need CDP or firmware reset. §3, §4.2.
3. **CDP may not be present on all lots or packages.** Confirm with WCH before depending on it. §3.
4. **There is no CH334R-specific datasheet.** Search the WCH file API's `scope` field, not document titles. §1.1, §7.
5. **CH334 has no USB 3.0.** That is CH335. §1.1.
6. **STT vs MTT matters** for multiple concurrent full-speed devices. MTT gives each port its own transaction translator; STT time-shares one. Configuration is via I/O pins or EEPROM.
7. **The internal LDO exists**, but supplying `VDD33` externally (as the Tanmatsu does) is fine and gives a cleaner rail.
8. **The crystal is genuinely optional** — the internal clock is USB-compliant per WCH. Removing it saves cost and EMI. §4.3.

---

## 6. Alternatives

| Part | vs. CH334R | When |
|---|---|---|
| **CH335F/P** | Same family, **adds USB 3.0 passthrough** on one port, 9-LED support | When any downstream device needs SuperSpeed |
| **CH334F/H/L/P/S/U/X** | Same die, different packages and pin counts | Pin-count or footprint constraints; more pins expose per-port power/over-current |
| **Microchip USB2514B / USB2517** | Very mature, excellent documentation, SMBus configurable | Western supply chain, or when you need runtime configuration |
| **Terminus FE1.1s** | Extremely cheap 4-port hub, ubiquitous in low-cost designs | Cost-driven; documentation is poor |
| **Genesys Logic GL850G** | Common 4-port hub | Second source |
| **TI TUSB2046 / TUSB8041** | Well documented, industrial | Where TI's documentation posture matters — see [`vendors/texas-instruments/README.md`](../../../vendors/texas-instruments/README.md) |

The CH334R's case is **cost and integration**: built-in crystal option, built-in string memory (no EEPROM), built-in pull-ups and LDO, in a 16-pin package. The cost is WCH's documentation portal, which is genuinely hostile until you know the API (§7).

---

## 7. Acquisition — the WCH file API is the only thing that works

Every HTML URL failed, exactly as [`vendors/wch/README.md`](../../../vendors/wch/README.md) predicts. Recorded in `component-download-failures.txt`:

| URL | Result |
|---|---|
| `https://www.wch-ic.com/downloads/file/304.html` | HTTP 200, **4 305 B `application/javascript`** — the SPA shell |
| `https://www.wch-ic.com/downloads/CH334DS1_PDF.html` | HTTP 200, byte-identical 4 305 B SPA shell |
| `https://www.wch.cn/downloads/file/304.html` | HTTP 200, 4 271 B SPA shell |
| `https://www.wch-ic.com/uploads/file/20211102/1635castCH334DS1.PDF` | HTTP 200, 4 305 B SPA shell |
| variants with `?time=`, `Referer:`, `X-Requested-With:` | all identical SPA shell |
| `cdn.datasheetspdf.com` | **DNS does not resolve** |

**What worked**, straight from the vendor guide, with a plain User-Agent:

```bash
# 1. Find the document by SCOPE, not by name
curl -sS "https://www.wch-ic.com/api/official/website/files/getFilesById?id=327"
# -> {"id":327, "name":"CH334DS1.PDF", "version":"2.91",
#     "uploadTime":"2026-08-28", "size":"508KB",
#     "scope":"CH334F, CH334H, CH334L, CH334P, CH334R, CH334S, CH334U, CH334X, CH335F, CH335P"}

# 2. Download by the same id
curl -sSL "https://www.wch-ic.com/download/file?id=327" -o ch334ds1.pdf
head -c4 ch334ds1.pdf     # %PDF   -> 521 028 bytes, 34 pages
```

The correct id is **327**, not the 304 that the dead HTML paths suggested.

> **This confirms and extends the existing vendor guide.** The `getFilesById` / `download/file` API worked first time with a default User-Agent, and the `scope`-not-title lesson applied directly: searching for a "CH334R datasheet" finds nothing; searching `scope` for `CH334R` finds `CH334DS1.PDF` immediately. The guide's warning that the HTML scheme "carries no information" was reproduced exactly — six different HTML URLs all returned the same 4 305-byte shell.

---

## 8. Open questions

- Whether the fitted crystal is 12 MHz was not confirmed from the BOM; it is inferred from the datasheet's stated requirement. §4.3.
- STT vs MTT configuration on this board is unknown — the QSOP-16 CH334R may fix it, or it may be set from the built-in information memory. Not established.
- Whether WCH's built-in string memory carries custom Tanmatsu identifiers, or WCH defaults, would be answerable from `lsusb -v` on real hardware.
- Nothing was verified on hardware.

---

## Manufacturer

**WCH (Nanjing Qinheng Microelectronics, 南京沁恒微电子)** — see [`vendors/wch/README.md`](../../../vendors/wch/README.md). That guide's file-API procedure and its "search `scope`, not titles" rule are what made this datasheet obtainable; §7 is a direct confirmation of both.

## Used By

| Device | Ref | Role |
|---|---|---|
| [Nicolai Electronics Tanmatsu](../../../devices/nicolai-electronics/tanmatsu/README.md) | `U5` | Splits the single USB-C device port to the **ESP32-P4** (port 3), the **ESP32-C6** (port 4) and the **internal add-on port** (port 1); port 2 goes to test points. `RESET#/CDP` left floating for low-power sleep. See [`bom.md`](../../../devices/nicolai-electronics/tanmatsu/bom.md), [`pinouts-and-buses.md`](../../../devices/nicolai-electronics/tanmatsu/pinouts-and-buses.md) §6 — **note the port-numbering correction in §4.1** |

## Related pages

- [`components/espressif/esp32-p4/README.md`](../../espressif/esp32-p4/README.md) · [`components/espressif/esp32-c6-wroom-1/README.md`](../../espressif/esp32-c6-wroom-1/README.md)
- [`components/generic/usb-c-interface/README.md`](../../generic/usb-c-interface/README.md)
- [`components/wch/ch32v203c8t6/README.md`](../ch32v203c8t6/README.md) · [`components/wch/ch340c/README.md`](../ch340c/README.md) · [`components/wch/ch445p/README.md`](../ch445p/README.md)

## Authoritative sources

| ID | Title | Publisher | Class | Medium | URL | Retrieved | Version | Establishes | Local path |
|---|---|---|---|---|---|---|---|---|---|
| D1 | CH334/335 Datasheet | WCH | primary | datasheet | `https://www.wch-ic.com/download/file?id=327` (metadata: `…/api/official/website/files/getFilesById?id=327`) | 2026-08-30 | **V2.91**, uploaded **2026-08-28**, 34 pp, 521 028 B, `scope` covers 10 parts | §2 features, **§3 Table 3-2 strapping**, reset electricals, LED modes, pin names | `artifacts/ch334ds1.pdf` |
| S1 | `tanmatsu.kicad_pcb` | Nicolai Electronics | primary | repository | in-tree snapshot | 2026-08-24 | `tanmatsu-hardware` @ `640805dd`, CERN-OHL-P | §4 pin table, **the §4.1 port-numbering correction**, floating pin 9, the fitted crystal | `devices/nicolai-electronics/tanmatsu/artifacts/schematics/kicad/tanmatsu.kicad_pcb` |
| S2 | WCH vendor sourcing guide | this repository | — | internal | — | 2026-08-30 | — | The file-API method and the `scope` rule that made D1 obtainable | `vendors/wch/README.md` |
