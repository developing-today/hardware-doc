# WCH CH340X

> **Filed under `components/wch/ch340x/` until 2026-08-30.** That location was correct
> while the part was unidentified; it stopped being correct the moment it was resolved to a CH340X,
> and the record simply never moved. It is now filed by manufacturer and part, like every other
> resolved component. A pointer remains at the old path.
>
> Not to be confused with [`components/wch/ch340c`](../ch340c/README.md) — a **different variant**
> (SOP-16, integrated clock) on different boards. The two share only WCH's family datasheet, which
> now lives once at [`vendors/wch/artifacts/`](../../../vendors/wch/artifacts/ch340-datasheet-v3.4.pdf).

Originally documented as bridge `U10` — **identified 2026-08-21 as WCH CH340X**

- **Category:** USB-to-UART bridge (full-speed USB 2.0 device → 3.3 V TTL UART)
- **Research status:** **identity resolved.** Previously recorded as "unidentified". The schematic symbol carries no part number, but the pin *names*, the pin *order*, the 10-pin package and — decisively — the `R14` resistor topology match exactly one documented part.
- **Retrieved:** 2026-08-21 (identification performed 2026-08-21 against WCH primary datasheets retrieved the same day)

This bridge serves the **ESP32-U4WDH only**. The ESP32-S3 on this board has a native USB peripheral (GPIO19/20) and does not go through `U10`. See [Dual-MCU architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md).

> **⚠ Supersedes prior guidance.** Earlier revisions of this record, of [gaps-and-conflicts](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/gaps-and-conflicts.md) and of [dual-mcu-architecture](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/dual-mcu-architecture.md) said the part was unknown and that no driver should be named. **That caution is now discharged**: the part is a CH340-family device and the WCH CH34x driver is the correct one. Section 3 records the full chain of reasoning so the conclusion stays auditable, and §4 gives the one-command confirmation to run on real hardware.

---

## Evidence labelling

Same scheme as the [ESP32-U4WDH record](../../espressif/esp32-u4wdh/README.md).

| Marker | Meaning |
|---|---|
| **[SCH]** | Read directly off the board schematic PNGs in `devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/schematic/` |
| **[DOC]** | Stated by the manufacturer in a document retrieved into `artifacts/` |
| **[SRC]** | Read out of vendor-shipped source, binaries or driver bundles in the device's `artifacts/` tree |
| **[WEB]** | Non-manufacturer web source, dated at retrieval |
| **[INF]** | Inference. Not established by the above |

---

## 1. Identity

| Property | Value | Evidence |
|---|---|---|
| Reference designator | **U10** | **[SCH]** sheet `3_ESP32-CHIP.png` |
| Part | **WCH (Nanjing Qinheng Microelectronics) CH340X** | **[INF] at very high confidence** — see §3 for the full argument |
| Family | CH340 series USB-to-serial bridge | **[DOC]** `artifacts/ch340-datasheet-v3.4.pdf` |
| Package | **MSOP-10**, 3.0 mm body (118 mil), 0.50 mm (19.7 mil) pitch | **[DOC]** CH340 datasheet §3 packages table; **[SCH]** symbol has exactly 10 pins |
| Marked on schematic | *nothing* — the symbol is drawn with functional pin names only | **[SCH]** |
| Crystal | **None required.** CH340C/N/K/E/X/B have an integrated 12 MHz oscillator | **[DOC]**; **[SCH]** no crystal is fitted near `U10` |
| Supply | `VCC` (pin 7) and `V3` (pin 10) **both tied to 3V3** | **[SCH]** — this is CH340's documented 3.3 V single-supply configuration, §5 |
| USB VID:PID when enumerated | **`1A86:7523`** | **[SRC]** WCH's own macOS driver personality table, `artifacts/wch-vid-pid-table-from-ch34xvcpdriver.txt` |
| Lifecycle | Active. CH340X is the *newest* member of the CH340 line — an improved CH340E with 5 V-tolerant I/O on a 3.3 V supply | **[DOC]** CH340 datasheet §3 note: "CH340X is improved based on the CH340E by adding the IO tolerant 5V feature for 3.3V supply" |

### 1.1 CH340 variants, and which ones are 10-pin

**[DOC]** from `artifacts/ch340-datasheet-v3.4.pdf` §3. Only two MSOP-10 parts and one ESSOP-10 part are 10-pin at all; everything else is immediately excluded by pin count.

| Order model | Package | Pins | Integrated clock | Notes |
|---|---|---:|---|---|
| CH340T | SSOP-20 | 20 | No (needs 12 MHz xtal) | Clock output `CKO` |
| CH340R | SSOP-20 | 20 | No | IrDA/SIR, **discontinued** |
| CH340G | SOP-16 | 16 | No | The classic hobbyist part |
| CH340C | SOP-16 | 16 | **Yes** | Some late lots can switch pin 8 `OUT#` → 2nd `DTR#` |
| CH340B | SOP-16 | 16 | Yes | Built-in EEPROM for serial number |
| CH340N | SOP-8 | 8 | Yes | No `CTS#`/`DTR#` at all |
| **CH340K** | **ESSOP-10** | 10 | Yes | Three built-in diodes against MCU back-feed |
| **CH340E** | **MSOP-10** | 10 | Yes | |
| **CH340X** | **MSOP-10** | 10 | Yes | **5 V-tolerant I/O; pin 6 `TNOW` ⇄ `DTR#` switchable by external resistor** |

---

## 2. Exact wiring on this board

**[SCH]** sheet `3_ESP32-CHIP.png`, read at 3× magnification.

| `U10` pin | Symbol name | Net | Goes to |
|---:|---|---|---|
| 1 | `UD+` | `USB_ESP32_DP` | USB-C data pair (ESP32 orientation); also connector `CN1` |
| 2 | `UD-` | `USB_ESP32_DN` | USB-C data pair; also `CN1` |
| 3 | `GND` | GND | |
| 4 | `RTS#` | `ESP32_EN` | **ESP32-U4WDH pin 9 `CHIP_PU`** (with `R54` 10 k pull-up, `C22` 1 µF) |
| 5 | `CTS#` | *no net label* | **`R14` 5.1 kΩ to pin 6.** Not available as flow control — see §2.1 |
| 6 | `TNOW/DTR#` | `ESP32_IO0` | **ESP32-U4WDH pin 23 `GPIO0`** (boot strap; `R50` 10 k pull-up, `C24` 100 nF); also `CN1` |
| 7 | `VCC` | 3V3 | |
| 8 | `TXD` | `ESP32_UART0_RX` | ESP32-U4WDH pin 40 `U0RXD`, through `R65` 470 Ω |
| 9 | `RXD` | `ESP32_UART0_TX` | ESP32-U4WDH pin 41 `U0TXD` |
| 10 | `V3` | 3V3 | Tied to `VCC` — the 3.3 V-supply configuration |

### 2.1 ⚠ `R14` is not a series resistor. It is the mode-select resistor.

This is the single most important thing on the sheet, and it is easy to misread from a low-resolution render. **`R14` (5.1 kΩ) connects pin 6 to pin 5**, not pin 6 to the ESP32. `ESP32_IO0` connects to pin 6 **directly**, with `R14` hanging off that node down to `CTS#`.

Quoting the CH340 datasheet §5.3 verbatim **[DOC]**:

> For CH340X, pin 6# defaults to `TNOW` … By adding an external resistor to the 6# pin, `TNOW` can be switched to `DTR#`. The two options are as follows:
>
> ① If the 6# pin is connected to an external 4.7 kΩ pull-down resistor to GND, it will enter the **open-source DTR enhancement mode** … used for multi-mode MCU downloads where `DTR#` defaults to a **low** level.
>
> ② **If a 4.7 kΩ resistor is connected between the 6# pin and the 5# pin, it will enter the push-pull DTR enhancement mode**, and the 6# pin will automatically switch to the **push-pull driven `DTR#`** … used for multi-mode MCU download with `DTR#` **default high** level.
>
> … The 4.7 kΩ pull-down resistor can be selected from **3 to 5.6 kΩ**.

Waveshare implemented **option ②**, with `R14` = 5.1 kΩ, inside WCH's stated 3–5.6 kΩ window. The choice of ② over ① is forced by the target: the ESP32-U4WDH's `GPIO0` must idle **high** to run the application, and it already has `R50` 10 k pulling it up, so the bridge needs a *push-pull* `DTR#` that defaults high. Option ① (open-source, defaults low) would hold `GPIO0` low and trap the ESP32 in the bootloader.

Practical consequences:

- **`CTS#` is consumed.** Do not enable RTS/CTS hardware flow control on this port; pin 5 is a mode-strap, not a modem line. **[INF]** — the datasheet does not say `CTS#` is unusable in mode ②, but it is tied through 5.1 kΩ to a push-pull output, so any reading of it is meaningless.
- **`R14` must not be removed or reworked.** Remove it and pin 6 reverts to `TNOW` (a half-duplex RS-485 transmit-enable indicator), auto-download breaks, and the ESP32-U4WDH becomes unprogrammable without shorting `GPIO0` by hand.
- **There is no two-transistor cross-coupled network** on this board, unlike most ESP32 dev boards. That network exists to make simultaneous DTR+RTS assertion a no-op. Here it is absent, so **any serial terminal that asserts DTR or RTS on port open will reset the ESP32 or drop it into the bootloader.** This is not a defect — WCH's §5.3 reference circuit is designed this way — but it changes your terminal settings. See §6.3.

### 2.2 The one-click download sequence this circuit implements

**[DOC]** CH340 datasheet §5.3, restated for this board:

| Step | `DTR#` (pin 6 → `GPIO0`) | `RTS#` (pin 4 → `EN`) | Effect |
|---|---|---|---|
| Idle / run | inactive ⇒ `GPIO0` high | inactive ⇒ `EN` high | ESP32 runs the application |
| Enter download | asserted ⇒ `GPIO0` **low** | pulsed ⇒ `EN` low then released | ESP32 latches `GPIO0`=0 at reset ⇒ ROM bootloader |
| Exit download | released ⇒ `GPIO0` high | pulsed again | ESP32 latches `GPIO0`=1 ⇒ application |

Note that CH340 MODEM signals are **inverted** relative to the pin level ("the MODEM data and pin level are inverted" **[DOC]**), which is why `esptool`'s ordinary `--before default_reset` works unmodified.

---

## 3. How the identification was made — the full chain

Six candidates were considered: CH340C, CH340E, CH340N, CH343P, CH9102F, CP2102N. The observable facts to explain are:

- **F1.** Exactly **10 pins**. **[SCH]**
- **F2.** Pin order, walking the symbol: `1 UD+ · 2 UD− · 3 GND · 4 RTS# · 5 CTS# · 6 TNOW/DTR# · 7 VCC · 8 TXD · 9 RXD · 10 V3`. **[SCH]**
- **F3.** The pin-6 label is the compound name **`TNOW/DTR#`** — a name that only exists because one physical pin has two mutually exclusive functions selected by an external component. **[SCH]**
- **F4.** `VCC` and `V3` are both on 3V3. **[SCH]**
- **F5.** `R14` = 5.1 kΩ **between pin 6 and pin 5**. **[SCH]**
- **F6.** Waveshare mirrors **WCH's CH34x macOS driver** in this board's own tools archive. **[SRC]** `devices/…/artifacts/tools/CH34XSER_MAC.7z`

### 3.1 Candidate elimination — ranked

| Rank | Candidate | Verdict | Evidence |
|---:|---|---|---|
| — | **CP2102N** | **Eliminated** | Silicon Labs ships CP2102N only in QFN-20 (4×4), QFN-24 (5×5) and QFN-28. There is no 10-pin CP2102N. Fails **F1**. Also uses `VBUS`/`REGIN`/`VIO` naming, never `UD+`/`UD−`/`V3` — those are WCH house names. **[WEB]** SiLabs CP2102N datasheet, retrieved 2026-08-21 |
| — | **CH9102F** | **Eliminated** | The CH9102 datasheet's own package table lists **only** `QF24_4X4` (CH9102F) and `QF28_5X5` (CH9102X). CH9102F is a **24-pin QFN**, not a 10-pin part. Fails **F1**. **[DOC]** `artifacts/ch9102-datasheet-v1.3.pdf` §3 |
| — | **CH340N** | **Eliminated** | SOP-8. Fails **F1**. Its pin table has no `CTS#` and no `DTR#` at all (`RTS#` only, on pin 4), so it physically cannot do this circuit. **[DOC]** CH340 datasheet §4 |
| — | **CH340C** | **Eliminated** | SOP-16. Fails **F1**. Its late-lot `OUT#`→2nd-`DTR#` trick is on **pin 8** and uses a **pull-down to GND**, not a pin-to-pin resistor. Fails **F5**. **[DOC]** CH340 datasheet §3 note and §5.3 |
| 3 | **CH343P / CH343K** | **Rejected — pinout mismatch** | CH343P is QFN-16, so it fails **F1** outright. The 10-pin sibling is **CH343K (ESSOP-10)**, whose pin map from the CH343 datasheet §4 is `1 UD+ · 2 UD− · 3 GND · 4 VDD5 · 5 RTS · 6 CTS-or-DTR · 7 VIO · 8 TXD · 9 RXD · 10 V3`. Pins 1,2,3,8,9,10 match, but **pin 4 is the 5 V supply, not `RTS#`, and pin 5 is `RTS`, not `CTS#`.** Fails **F2**. It also has no documented `TNOW`/`DTR#` resistor-strap on pin 6, failing **F3** and **F5**. **[DOC]** `artifacts/ch343-datasheet-v2.0.pdf` |
| 2 | **CH340E** | **Rejected — cannot explain F3/F5** | Same MSOP-10 package and same pin numbering as CH340X, so it satisfies **F1**, **F2**, **F4**. But the CH340 datasheet attributes the resistor-selectable `TNOW`→`DTR#` behaviour on pin 6# **specifically and exclusively to CH340X** (§3 note and all of §5.3). On a CH340E pin 6 is a plain output with no mode strap, so `R14` would be an inexplicable 5.1 kΩ short between two outputs and auto-download would not work. **[DOC]** |
| **1** | **CH340X** | ✅ **Accepted** | Satisfies **F1** (MSOP-10), **F2** (pin order), **F4** (`VCC`+`V3` on 3.3 V is CH340's documented 3.3 V mode), **F6** (WCH driver shipped by Waveshare), and uniquely explains **F3** and **F5**: the schematic symbol's compound `TNOW/DTR#` label *is* WCH's own name for CH340X pin 6, and `R14` at 5.1 kΩ between pins 6 and 5 *is*, verbatim, WCH §5.3 option ② with a value inside WCH's stated 3–5.6 kΩ range. **[DOC]** + **[SCH]** |

### 3.2 On the "TNOW is a CH343/CH9102 convention" hypothesis

The task that prompted this investigation noted that `TNOW`/`DTR#` naming looks like a WCH CH343/CH9102 convention. That instinct was right about the *vendor* and wrong about the *family*: `TNOW` is a **WCH-wide** house name for "UART transmit-in-progress, for RS-485 direction control", and it appears in the CH340, CH343 **and** CH9102 datasheets alike **[DOC]** (all three retrieved into `artifacts/`). What is *not* WCH-wide is the **compound** `TNOW/DTR#` on a single 10-pin package selected by a pin-5↔pin-6 resistor. That is CH340X and only CH340X.

### 3.3 Confidence statement

**Very high (~95 %) for "a CH340-family part in MSOP-10"; high (~90 %) for "CH340X specifically".**

The 5 % is the residue of never having seen the chip's top marking. The 10 % gap between the two figures is the CH340E possibility: CH340E and CH340X are pin-identical, so a board could be *drawn* with the CH340X application note and *stuffed* with a CH340E. If that happened, auto-download would be broken on real units — and it demonstrably is not, because Waveshare's own flashing instructions do not tell users to hold a BOOT button for the ESP32 (there isn't one — §7.4). **[INF]**

What would take this to certainty: a photograph of `U10`'s top marking, or the §4.2 test.

---

## 4. How to confirm it on real hardware

### 4.1 Read the USB VID/PID — the first thing to do

Plug the USB-C cable in the **ESP32-U4WDH orientation** (see [USB-C interface](../../generic/usb-c-interface/README.md); the orientation matters on this board) and enumerate.

~~~sh
# Linux
lsusb -d 1a86:                     # or: lsusb -v -d 1a86:7523
dmesg | tail -20                   # expect: ch341-uart converter now attached to ttyUSB0
udevadm info -a -n /dev/ttyUSB0 | grep -E 'idVendor|idProduct|product|manufacturer'

# macOS
system_profiler SPUSBDataType | grep -A8 -iE 'USB Serial|1a86|QinHeng'

# Windows (PowerShell)
Get-PnpDevice -Class Ports | Format-List FriendlyName,InstanceId
~~~

Expected VID/PID by candidate. **The WCH rows are [SRC]**, extracted from the `IOKitPersonalities` dictionary of `cn.wch.CH34xVCPDriver` — WCH's own first-party driver, which Waveshare itself mirrors for this board. Full dump in `artifacts/wch-vid-pid-table-from-ch34xvcpdriver.txt`.

| Candidate | VID | PID | If you see this |
|---|---|---|---|
| **CH340 family (incl. CH340X)** | **`1A86`** | **`7523`** | ✅ **Expected.** Confirms CH340 family |
| CH340 alt (rare lots) | `1A86` | `7522` | Still CH340 family |
| CH341 in serial mode | `1A86` | `5523` | Would be surprising here |
| CH330 | `1A86` | `E523` | Would falsify §3 |
| CH342 | `1A86` | `55D2` | Would falsify §3 |
| **CH343** | `1A86` | `55D3` | Would falsify §3 |
| **CH9102** | `1A86` | `55D4` | Would falsify §3 |
| CH9101 | `1A86` | `55D8` | Would falsify §3 |
| CH9103 | `1A86` | `55D7` | Would falsify §3 |
| **CP2102 / CP2102N** | `10C4` | `EA60` | Would falsify §3 entirely **[WEB]** |
| FTDI FT232R / FT231X | `0403` | `6001` / `6015` | Would falsify §3 entirely **[WEB]** |

> **⚠ The VID/PID alone cannot separate CH340X from CH340E/K/C/N/G.** WCH gives the *whole* CH340 line one PID. `7523` proves "CH340 family" and nothing finer. That is still enough to answer the only question a developer actually has — *which driver do I install* — but it does not close §3.3.

### 4.2 Finish the identification

Ranked by effort:

1. **Look at the chip.** MSOP-10 parts are marked `CH340X` or `CH340E`. A 10× loupe and a phone macro shot settle it in ten seconds. This is the definitive test.
2. **Test the auto-download.** Run `esptool --chip esp32 --port PORT --before default_reset chip_id`. If it enters the bootloader **without** you touching anything, pin 6 is behaving as a push-pull `DTR#` ⇒ CH340X in mode ②. A CH340E would leave pin 6 as `TNOW` and the command would fail unless `GPIO0` were grounded by hand.
3. **Check I/O tolerance.** CH340X's differentiator is 5 V-tolerant I/O on a 3.3 V supply **[DOC]**. Not worth testing destructively; listed for completeness.

---

## 5. Electrical specifications that matter here

**[DOC]** `artifacts/ch340-datasheet-v3.4.pdf`.

| Item | Value | Relevance on this board |
|---|---|---|
| Supply modes | 5 V (`VCC`=5 V, `V3` decoupled with 0.1 µF) **or** 3.3 V (`V3` tied to `VCC`) | Board uses the **3.3 V** mode: pins 7 and 10 both on 3V3 **[SCH]** |
| USB | Full-speed USB 2.0 device, **integrated D+ pull-up** | **`UD+`/`UD−` must connect directly to the bus with no series resistors** — the datasheet states this explicitly, and the board complies **[SCH]** |
| Clock | Integrated 12 MHz oscillator (CH340C/N/K/E/X/B) | No crystal on the board, consistent |
| I/O tolerance | CH340X (and CH340C/N with lot codes starting `4`) tolerate 5 V on I/O even at 3.3 V supply | Not exercised here — everything is 3.3 V |
| Back-feed protection | CH340X, CH340K and late CH340C/N prevent current flowing into an unpowered MCU | Relevant: the board can run from battery with USB unplugged, so `U10` may be unpowered while the ESP32 is not. **[INF]** that this is why Waveshare chose an X/K-class part |
| Baud range | 50 bps – 2 Mbps (CH340 family) | `esptool` at 115200/460800/921600 is well inside |
| Flow control | `RTS#`/`CTS#` MODEM lines | **Unavailable here** — `CTS#` is the mode strap, `RTS#` drives `EN`. §2.1 |
| Sleep current in "unified supply" mode | "tens of µA" drawn from the shared rail | The board uses the unified supply (pins 7/10 on 3V3, not on USB `VBUS`), so this current is present on battery. **[DOC]** §5.3 flags exactly this trade-off |

---

## 6. Firmware, drivers and tooling

### 6.1 Host drivers

| OS | What to do | Notes |
|---|---|---|
| **Linux** | Nothing. `ch341` is in-tree | Binds `1A86:7523` → `/dev/ttyUSB*`. If `brltty` grabs the port (common on Ubuntu), mask it: `sudo systemctl mask brltty.path brltty.service` |
| **macOS** | Install WCH's `CH34xVCPDriver` | Waveshare mirrors it: <https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z>, local copy at `devices/…/artifacts/tools/CH34XSER_MAC.7z`. macOS 11+ also ships an in-box `AppleUSBCHCOM` driver that handles `1A86:7523`; try without installing anything first |
| **Windows** | `CH341SER` from WCH (<https://www.wch-ic.com/downloads/CH341SER_EXE.html>), or let Windows Update fetch it | Windows 10/11 usually resolves `1A86:7523` automatically. Note: **`CH341SER`, not `CH343SER`** — the latter is for the 55Dx family |

The bundled macOS driver's own `Info.plist` (`artifacts/wch-vid-pid-table-from-ch34xvcpdriver.txt`) shows it covers CH330/CH340/CH342/CH343/CH344/CH347/CH9101/CH9102/CH9103/CH9104/CH9143 — so installing it is safe regardless of which WCH part turns out to be fitted. **[SRC]**

### 6.2 esptool

The target behind this bridge is the **ESP32-U4WDH**, i.e. `--chip esp32` — *not* `esp32s3`. Getting this wrong is the most common mistake on this board.

~~~sh
esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 chip_id
esptool --chip esp32 --port /dev/ttyUSB0 flash_id
esptool --chip esp32 --port /dev/ttyUSB0 --before default_reset --after hard_reset \
        write_flash 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 app.bin
~~~

`--before default_reset` uses exactly the DTR/RTS sequence in §2.2 and is the correct choice here. Do **not** use `--before no_reset` unless you are grounding `GPIO0` by hand.

For Arduino: **`Tools → Port`** will show `/dev/ttyUSB*` (CH340) for the ESP32, and `/dev/ttyACM*` (native USB CDC) for the S3. They are different ports on different cable orientations.

### 6.3 Serial monitors — the DTR/RTS trap

Because there is no two-transistor network (§2.1), **opening the port with DTR or RTS asserted will reset the ESP32 or drop it into the bootloader.** Symptoms: your monitor connects and the board immediately reboots, or prints `waiting for download`.

| Tool | Fix |
|---|---|
| `picocom` | `picocom -b 115200 --lower-dtr --lower-rts /dev/ttyUSB0` |
| `minicom` | Disable "Hardware Flow Control" in `Serial port setup`; add `--noinit` |
| `screen` | `screen` cannot deassert DTR/RTS — use something else |
| `idf.py monitor` | Fine; it manages DTR/RTS deliberately |
| Arduino IDE Serial Monitor | Toggles DTR on open. Expect a reset each time you open it |
| PuTTY | Set *Connection → Serial → Flow control* to **None** |
| SSCOM (shipped in `artifacts/tools/Sscom5.13.1.zip`) | Untick `DTR` and `RTS` before opening |
| Python `pyserial` | `serial.Serial(port, 115200, dsrdtr=False, rtscts=False)` then explicitly `ser.dtr = False; ser.rts = False` **before** the first read |

---

## 7. Common pitfalls

1. **Wrong `--chip`.** This port is the *ESP32*, not the ESP32-S3. `esptool --chip esp32s3` will fail or, worse, half-succeed.
2. **Wrong USB-C orientation.** This board multiplexes the USB data pair between the S3's native USB and `U10` depending on plug orientation **[WEB]** (Waveshare FAQ; no USB-C receptacle appears in the five published schematic sheets, so the topology is unverified). If you see an Espressif VID (`303A`) rather than `1A86:7523`, flip the cable.
3. **Assuming flow control works.** §2.1.
4. **Assuming there is a BOOT button for the ESP32.** There is not. The board's BOOT button is on the **S3** (see [ESP32-S3 BOOT button](../../generic/esp32-s3-boot-button/README.md)). The U4WDH's only route into download mode is `U10` pin 6. If `R14` is damaged you have no fallback except a wire to `CN1`'s `GPIO0` pin.
5. **`brltty` on Linux** stealing `1A86:7523` and making `/dev/ttyUSB0` vanish after ~5 seconds. Extremely common; mask the unit.
6. **Reworking `R14` to a "standard" value.** WCH's range is 3–5.6 kΩ. Going to 10 kΩ puts you outside it and the mode strap may not latch. **[DOC]**
7. **Cheap USB-C-to-USB-C cables.** Not specific to this chip, but a charge-only cable will power the board and enumerate nothing, which reads as "the bridge is dead".
8. **Counterfeit-CH340 folklore.** Unlike FTDI, WCH has never shipped a driver that bricks clones. If a `1A86:7523` device misbehaves on Windows, the usual cause is an ancient `CH341SER` from a 2014-era CD, not counterfeiting. **[INF]**

---

## 8. Alternatives and drop-in compatibility

| Part | Package | Drop-in for `U10`? | Comment |
|---|---|---|---|
| **CH340E** | MSOP-10 | Mechanically yes; **functionally no** | Pin 6 has no `DTR#` mode strap ⇒ auto-download dies |
| **CH340K** | ESSOP-10 | **No** — different pitch (1.00 mm vs 0.50 mm) and different footprint | Pinout is `1 UD+ · 2 UD− · 3 GND · 4 DTR# · 5 CTS# · 6 RTS# · 7 VCC · 8 TXD · 9 RXD · 10 V3` **[DOC]** — note pins 4 and 6 are **swapped** relative to this board, so even a hand-fitted CH340K would drive `EN` from `DTR#` and `GPIO0` from `RTS#` |
| CH340C / CH340G | SOP-16 | No | Different package. CH340C late lots can emulate the trick on pin 8 with a pull-down |
| CH343K | ESSOP-10 | No | Different pin assignment (§3.1); pin 4 is the supply |
| CH9102F | QFN-24 | No | Different package entirely |
| CP2102N | QFN-20/24/28 | No | Different everything. Would need a redesign |
| FT231XS | SSOP-20 | No | Different package |

**If you are designing your own board and want this behaviour**, use CH340X in MSOP-10 with a 4.7 kΩ (3–5.6 kΩ) resistor between pins 6 and 5, exactly as here. It is the smallest, cheapest, crystal-less way to get one-click ESP32 download with no transistors.

---

## 9. Open questions

| Question | Status |
|---|---|
| Top marking on `U10` — `CH340X` or `CH340E`? | **Open.** Resolvable with a loupe. §4.2 |
| Is `U10` powered from USB `VBUS` or from the board 3V3 rail? | **Resolved [SCH]:** pins 7/10 are on the board 3V3 net, i.e. WCH's *unified* supply variant, not the independent-VBUS one. Consequence: `U10` draws tens of µA of sleep current from the board rail even on battery |
| USB-C orientation-selection topology | **Open** — no USB-C receptacle is drawn in any of the five sheets. See [USB-C interface](../../generic/usb-c-interface/README.md) |
| Does `CN1` bring out `USB_ESP32_DP/DN` in a usable order? | **Open** — `CN1` pin numbering is deliberately not transcribed; see [Pinouts and buses § Connector records](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md) |

---

## Manufacturer

**WCH (Nanjing Qinheng)** — the part is identified as a **CH340X**. See the [WCH documentation-sourcing guide](../../../vendors/wch/README.md), and note in particular that WCH publishes **one document per family**: the CH340 family document is the one to read.

*(This record remains filed under `components/generic/` for historical reasons — it was created before the part's identity was resolved on 2026-08-21.)*

## Used By

- [Waveshare ESP32-S3-Knob-Touch-LCD-1.8](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/README.md) — reference designator **`U10`**, serving the **ESP32-U4WDH** (`U14`) only. Wiring in [Pinouts and buses § USB-UART bridge U10](../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/pinouts-and-buses.md).

## Related components

- [Espressif ESP32-U4WDH](../../espressif/esp32-u4wdh/README.md) — the target MCU
- [USB-C target-selection interface](../../generic/usb-c-interface/README.md) — which chip the cable reaches
- [WCH CH445P](../../wch/ch445p/README.md) — the other WCH part on this board

---

## Authoritative sources

| Title | URL | Retrieved | Local artifact |
|---|---|---:|---|
| **WCH CH340 Datasheet, version 3D** (covers CH340G/C/N/K/E/X/B/T/R; §3 packages, §4 pins, §5.3 DTR mode straps) | https://www.wch-ic.com/download/file?id=79 | 2026-08-21 | `artifacts/ch340-datasheet-v3.4.pdf` |
| WCH CH343 Datasheet, version 2.0 (used to **exclude** CH343P/CH343K) | https://www.wch-ic.com/download/file?id=296 | 2026-08-21 | `artifacts/ch343-datasheet-v2.0.pdf` |
| WCH CH9102 Datasheet, version 1.3 (used to **exclude** CH9102F — QFN24 only) | https://www.wch-ic.com/download/file?id=297 | 2026-08-21 | `artifacts/ch9102-datasheet-v1.3.pdf` |
| WCH file metadata API (how the above were located) | https://www.wch-ic.com/api/official/website/files/getFilesById?id=79 | 2026-08-21 | – |
| WCH CH340 product page | https://www.wch-ic.com/products/CH340.html | 2026-08-21 | – |
| WCH CH34x macOS VCP driver (mirrored by Waveshare for **this board**) — source of the VID/PID table | https://files.waveshare.com/wiki/common/CH34XSER_MAC.7z | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/tools/CH34XSER_MAC.7z` |
| VID/PID table extracted from the above driver's `IOKitPersonalities` | *(derived artifact)* | 2026-08-21 | `artifacts/wch-vid-pid-table-from-ch34xvcpdriver.txt` |
| Board schematic archive | https://files.waveshare.com/wiki/ESP32-S3-Knob-Touch-LCD-1.8/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip | 2026-08-21 | `../../../devices/waveshare/esp32-s3-knob-touch-lcd-1.8/artifacts/originals/ESP32-S3-Knob-Touch-LCD-1.8-schematic.zip` |
| Silicon Labs CP2102N datasheet (packages, used to exclude) | https://www.silabs.com/documents/public/data-sheets/cp2102n-datasheet.pdf | 2026-08-21 | – |
| esptool documentation (reset sequences, `--before`/`--after`) | https://docs.espressif.com/projects/esptool/en/latest/esp32/ | 2026-08-21 | – |
| Linux `ch341` driver source (VID/PID table cross-check) | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/usb/serial/ch341.c | 2026-08-21 | – |

### Retrieval notes

`www.wch-ic.com` is a Vue single-page app that returns **HTTP 200 with a 4305-byte HTML shell for every unknown path**, including all `…_PDF.html` document URLs. A naïve `curl` of a documentation URL therefore *looks* successful and yields HTML — which is precisely how this part stayed "unidentified" through the previous research pass, and why the earlier `component-download-failures.txt` entry for CH445 records "response was JavaScript source, not PDF".

The working route, found 2026-08-21:

1. `GET https://www.wch-ic.com/api/official/website/files/getFilesById?id=<N>` returns JSON metadata (`name`, `version`, `scope`, `size`, `content`). Enumerate `N` (documents live roughly in 1–800) and match on `name`/`scope`.
2. `GET https://www.wch-ic.com/download/file?id=<N>` returns the actual PDF. Validate `%PDF` magic.

Both endpoints worked with a plain default User-Agent; no UA substitution was needed. Concurrency above ~24 parallel requests causes silent timeouts. Findings recorded in [`ai-crawler-site-access-table.md`](../../../ai-crawler-site-access-table.md).
