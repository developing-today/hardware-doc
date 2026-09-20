# USB-C interface — one receptacle, two targets, orientation-selected

- **Category:** USB-C power and data interface
- **Reference designator on this board:** **none.** ⚠ **No USB Type-C receptacle symbol appears anywhere in the five published schematic sheets**
- **Owning MCU:** **both, alternately** — which one you reach depends on which way round the plug is inserted
- **Research status:** the *behaviour* is confirmed by the vendor and corroborated by the presence of two independent USB endpoints. The *topology* is entirely unresolved
- **Retrieved:** 2026-08-21; both USB pairs traced to their endpoints and `CN1` pinout resolved 2026-08-23

## Evidence labelling

**[SCH]** schematic PNG · **[SRC]** vendor demo source · **[WEB]** vendor page/wiki/FAQ · **[INF]** inference, reasoning given

---

## 1. The behaviour — this is the thing to know

**This board has one USB-C receptacle but two USB endpoints behind it. Which one you talk to depends on which way round you insert the plug.** Rotate the plug 180° to reach the other processor.

| Plug orientation | You reach | Appears as |
|---|---|---|
| One way | **ESP32-S3** via its **native USB** peripheral (GPIO19/GPIO20) | USB CDC-ACM, plus USB-JTAG and DFU |
| The other way | **ESP32-U4WDH** via the **USB-UART bridge `U10`** | A USB-serial port |

This is documented product behaviour, stated by Waveshare in its own FAQ **[WEB]**, and it is **by far the most common cause of "no serial port appeared" and "esptool says the wrong chip"** on this board.

**If your toolchain reports the wrong chip, or no port at all: unplug, rotate the plug 180°, reconnect.** That is the fix, and it is not a joke.

Full development-workflow context is in [development.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/development.md) and [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md).

## 2. ⚠ The receptacle is not in the schematic

All five sheets were searched **[SCH]**. There is:

- **No USB Type-C receptacle symbol**
- **No `CC1`/`CC2` configuration-channel pins**
- **No 5.1 kΩ `Rd` pull-down resistors** (the pair every USB-C sink needs to be recognised as a device)
- **No VBUS protection, no TVS array, no polyfuse**
- **No analogue multiplexer, no orientation-detection logic, no USB switch IC**

What the schematic *does* show is where the two USB pairs go **[SCH]**:

| Net | Endpoint | Sheet |
|---|---|---|
| `USB_DP` / `USB_DN` | **ESP32-S3** GPIO20 / GPIO19 | 2 |
| `USB_ESP32_DP` / `USB_ESP32_DN` | **Bridge `U10`** pins 1 / 2 | 3 |
| **All four** | **`CN1`** pins 4, 3, 5, 6 | 1 |

So **both differential pairs terminate only at the ten-pin header `CN1`**, alongside 5 V, ground, S3 GPIO0 and the DAC's analogue outputs. See [generic/ph1.27-expansion-connectors §2](../ph1.27-expansion-connectors/README.md#2-pinout--resolved-sch-sheet-1-1_lcdpowerpng) for the resolved pinout.

## 3. What can be inferred about the topology

**[INF]**, and clearly labelled as such. Nothing in this section is established.

### 3.1 The most likely arrangement

`CN1`'s composition — 5 V, ground ×2, both USB pairs, and the two audio line outputs — is **exactly the signal set you would route to a connector daughterboard** carrying the USB-C receptacle and the 3.5 mm jack. It carries no I2C, no SPI, no UART and no spare GPIO, which is what an actual expansion header would carry.

So the most economical explanation is: **`CN1` is an internal board-to-board connector, and the USB-C receptacle lives on an unpublished sheet or a separate flex/daughterboard.** The charger block (see [generic/charger-power-path](../charger-power-path/README.md)) and the 3.5 mm jack (see [generic/3.5mm-audio-output](../3.5mm-audio-output/README.md)) are missing from the schematic for what is very likely the same reason.

### 3.2 How the orientation selection could work

USB-C has **two** sets of D+/D− pins (A6/A7 and B6/B7) precisely so that a plug can be inserted either way. In a normal design these are shorted together on the receptacle, or muxed, so the host sees one pair regardless of orientation.

**This board evidently does not short them.** Instead, the two positions are wired to two different targets:

```
USB-C receptacle
   A6/A7  ────  one USB pair   ──── target 1
   B6/B7  ────  other USB pair ──── target 2
```

A Type-C **plug** only connects one of the two D+/D− positions (the one matching its orientation), so this arrangement genuinely gives orientation-selected targeting with **no active components at all** — just wiring. **[INF]** That elegance is a strong argument that this is what is happening: it explains the observed behaviour, requires nothing that would need to appear on a schematic sheet other than the receptacle itself, and is consistent with the absence of any mux IC in the published sheets.

### 3.3 What this implies, if §3.2 is right

| Implication | Detail |
|---|---|
| **USB-C-to-USB-C cables may behave differently from A-to-C** | A full C-to-C cable with a `CC` handshake behaves the same electrically for D+/D−, but the orientation is still whatever you physically insert |
| **The board is a "non-compliant" USB-C sink in one respect** | A device that presents different data endpoints depending on orientation is outside the spirit of the specification, which expects orientation to be transparent |
| **`CC` resistors must exist somewhere** | Without 5.1 kΩ `Rd` on at least one `CC` pin, a USB-C source will not supply VBUS at all. Since the board demonstrably charges and powers from USB-C **[WEB]**, they exist — just not on a published sheet |
| **There is probably no orientation *detection* available to firmware** | No `CC`-sense signal reaches either MCU **[SCH]**. Neither processor can tell which way the plug is in |
| **Only one target is reachable at a time** | You cannot monitor the S3 and flash the U4WDH simultaneously over USB |

### 3.4 What is genuinely unresolved

- Whether §3.2 is correct at all
- Whether any switch IC, ESD array or protection exists
- The `CC` resistor values and placement, and therefore the **advertised current draw** (500 mA default? 1.5 A? 3 A?)
- Whether USB Power Delivery is negotiated (**almost certainly not** **[INF]** — there is no PD controller in evidence and no reason for one)
- VBUS over-voltage and reverse-current protection
- Whether the receptacle is a 16-pin (USB 2.0) or 24-pin part

## 4. The ESP32-S3 side: native USB

When the plug selects the S3, you get the S3's **built-in USB OTG/serial-JTAG** peripheral on GPIO19 (`D−`) and GPIO20 (`D+`) **[SCH sheet 2]**. That gives you, with no extra hardware:

| Capability | Note |
|---|---|
| **USB CDC-ACM serial** | Enable "USB CDC On Boot" in Arduino, or `CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG` in ESP-IDF |
| **USB-JTAG debugging** | Built into the same peripheral. No external probe needed — this is a genuinely valuable feature people often overlook on this board |
| **DFU / ROM download** | `esptool` works directly over native USB |
| **USB device stack (TinyUSB)** | HID, MSC, MIDI, composite devices — the S3 can be any of them |

Two gotchas specific to native USB:

1. **The port disappears on reset.** Native USB is implemented by the running chip, so resetting or reflashing the S3 drops the USB device off the bus and the host re-enumerates it. Serial monitors need to handle the port vanishing and reappearing. This is normal, not a fault.
2. **If your firmware crashes early or disables USB, the port never appears.** Recovery is the ROM bootloader, reached by holding BOOT (S3 GPIO0) low during reset — see [generic/esp32-s3-boot-button](../esp32-s3-boot-button/README.md), and note that GPIO0 has a second job on this board.

**The ESP32-S3's UART0 console is *not* routed to the USB bridge** **[SCH]** — the S3 is reachable only over native USB. There is no fallback serial path.

## 5. The ESP32-U4WDH side: the bridge

When the plug selects the other orientation, you reach the **USB-UART bridge `U10`**, which is drawn as a bare 10-pin functional symbol with no BOM string **[SCH sheet 3]** and was therefore long recorded as unidentified. It was **resolved to a WCH CH340X on 2026-08-21** — see [`components/wch/ch340x`](../../wch/ch340x/README.md).

The bridge fronts the ESP32-U4WDH's UART0 (GPIO1 TX / GPIO3 RX) and provides automatic download mode **[SCH]**:

- `U10` `RTS#` → `ESP32_EN` (reset)
- `U10` `TNOW/DTR#` → `ESP32_IO0` (boot strap), via `R14` 5.1 kΩ

**These are direct connections, not the two-transistor cross-coupled network used on most ESP32 dev boards** **[SCH]**. The practical consequence is real: **a serial terminal that asserts DTR or RTS when it opens the port can reset the ESP32 or drop it into the bootloader.** If your monitor session dies the instant you connect, turn off DTR/RTS assertion in your terminal program.

## 6. Power

`VBUS` becomes the board's **`5V`** net, which feeds:

- The `TLV62569DBVT` buck's `VIN` and `EN` → the 3.3 V rail **[SCH sheet 1]**
- The `SGM2036-3.3` LDO via ferrite `L8` → the audio rail **[SCH sheet 5]**
- The `BATT_ADC` divider `R62`/`R63` **[SCH sheet 4]**
- `CN1` pin 1
- The unidentified charger **[INF — see [charger-power-path](../charger-power-path/README.md)]**

**How much current the board advertises to a USB-C source is unknown** (§3.4). Peak board draw is estimated at up to ~1.3 A on the 3.3 V rail in the worst case, which is ~900 mA on the 5 V input after buck efficiency — see [tlv62569dbvt §5.2](../../texas-instruments/tlv62569dbvt/README.md#52-scenarios). **[INF]** That is comfortably inside 1.5 A but above the 500 mA a non-negotiating USB 2.0 port nominally provides, so **a weak or unpowered hub port may cause brownouts under simultaneous peak load.** Use a proper charger or a powered hub if you see instability.

## 7. Pitfalls

1. **Wrong chip, or no port at all → rotate the plug.** §1. This is the single most common problem with this board.
2. **You cannot reach both MCUs at once.** §3.3.
3. **Neither MCU can detect the orientation.** §3.3. Firmware cannot tell you which target is live.
4. **The S3's native USB port disappears on reset.** §4.
5. **DTR/RTS assertion can reset the ESP32-U4WDH.** §5.
6. **There is no serial fallback for the S3.** UART0 is not routed. §4.
7. **The receptacle's protection is unknown.** §3.4. Do not assume there is a TVS array between a hot-plugged cable and the MCU pins.
8. **Do not connect to `CN1`'s USB pins while a USB-C cable is attached.** §3.1 — you would be driving the same pairs from two places.

## 8. Open questions

| Question | Status | Method |
|---|---|---|
| Receptacle part, pin count, and whether it is on a daughterboard | **Unknown** | Disassembly and photograph |
| Whether §3.2's passive-orientation theory is correct | **Unverified** | Continuity from the receptacle's A6/A7 and B6/B7 to the two pairs |
| `CC` resistor values and advertised current | **Unknown** | Measure `CC1`/`CC2` to ground |
| Presence of ESD/TVS protection | **Unknown** | Photograph |
| Whether `CN1` is user-facing or an internal interconnect | **Unresolved** | §3.1 argues internal **[INF]** |
| USB descriptors in each orientation | **Not captured** | `lsusb -v` in both orientations — a five-minute experiment that would also identify bridge `U10` |

That last one is worth highlighting: **capturing the USB descriptors in the bridge orientation would very likely identify the unknown `U10` part outright**, since USB-serial bridges report distinctive VID/PID pairs. It is the cheapest available route to closing two gaps at once.

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — the single USB-C port, orientation-selecting between the two MCUs

## Related pages

- [development.md](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/development.md) — the practical flashing workflow for both orientations
- [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md) — why there are two targets
- [`wch/ch340x`](../../wch/ch340x/README.md) — `U10`, resolved to a WCH CH340X
- [generic/ph1.27-expansion-connectors](../ph1.27-expansion-connectors/README.md) — where both USB pairs actually terminate in the schematic
- [generic/charger-power-path](../charger-power-path/README.md) — the other function missing from the published sheets
- [generic/esp32-s3-boot-button](../esp32-s3-boot-button/README.md) — the recovery path when native USB does not enumerate
- [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md)

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| Waveshare wiki / FAQ — the vendor's own statement of the orientation behaviour | https://www.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8 | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/source-snapshots/waveshare-wiki-current.html` |
| Waveshare product page | https://www.waveshare.com/esp32-s3-knob-touch-lcd-1.8.htm | 2026-08-21 | `.../artifacts/source-snapshots/waveshare-product-31623.html` |
| Board schematic sheet 1 — `CN1`, the only place either USB pair terminates | — | 2026-08-21 | `.../artifacts/schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/1_LCD&POWER.png` |
| Board schematic sheet 2 — `USB_DP`/`USB_DN` at S3 GPIO20/GPIO19 | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/2_ESP32S3-R8.png` |
| Board schematic sheet 3 — `USB_ESP32_DP`/`DN` at bridge `U10`, and the `RTS#`/`DTR#` auto-download wiring | — | 2026-08-21 | `.../schematic/ESP32-S3-Knob-Touch-LCD-1.8-schematic/3_ESP32-CHIP.png` |
| ESP32-S3 datasheet — native USB on GPIO19/GPIO20 | https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf | 2026-08-21 | `../../espressif/esp32-s3r8/artifacts/esp32-s3-datasheet.pdf` |
| ESP-IDF v5.3.2 — USB Serial/JTAG console | https://docs.espressif.com/projects/esp-idf/en/v5.3.2/esp32s3/api-guides/usb-serial-jtag-console.html | 2026-08-23 | closest archived PDF: `../../espressif/esp32-s3r8/artifacts/esp-idf-programming-guide-v5.2.5-esp32s3.pdf` |
