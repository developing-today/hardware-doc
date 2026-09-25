# USB and serial — M5Stack PaperMono

> **How do I flash it, get a serial console, and why will I not find a reset button?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

## 1. Capability summary and the hardware path

Native USB from the ESP32-S3, plus a conventional UART0, plus a USB-C connector that
carries power and data and **nothing else**.

```
USB-C (U1, TYPEC-302-BRP16SC08)
   ├─ D-/D+ ──▶ FT1 common-mode filter ──▶ ESP32-S3 GPIO19 / GPIO20   (native USB)
   └─ VBUS  ──▶ AW32901FCR OVP 5.95 V  ──▶ IP2315 charger

ESP32-S3 GPIO43 (U0TXD, 499 Ω series R30) ──┐
ESP32-S3 GPIO44 (U0RXD)                   ──┴─ UART0, not brought to any connector

M5PM1 BOOT_OUT_OD ──▶ ESP32-S3 GPIO0   (boot strap)
M5PM1 SOC_RESET   ──▶ ESP32-S3 CHIP_PU (reset)
```

| Signal | GPIO | Note |
|---|---|---|
| USB D− | **GPIO19** | via `FT1` common-mode filter |
| USB D+ | **GPIO20** | via `FT1` |
| UART0 TX | **GPIO43** | 499 Ω series (`R30`) |
| UART0 RX | **GPIO44** | |
| Boot strap | **GPIO0** | driven by the **M5PM1**, not a button |
| Reset | `CHIP_PU` | driven by the **M5PM1** |

**None of these four appear on the vendor's product-page pin tables.** USB (GPIO19/20)
and UART0 (GPIO43/44) are established from the schematic only — the product page is
otherwise accurate but omits them.

## 2. ⚠ There is no USB-PD

The connector carries the standard **5.1 kΩ CC pulldowns** (`R14` on CC2) advertising a
plain sink, but the **IP2315's own `CC1`/`CC2` sense pins are unpopulated** (`R1`, `R2`
marked `NC`). Combined with the 5.95 V OVP upstream, this is a **plain 5 V input** and the
charger's PD capability is deliberately depopulated.

| What is present | What is not |
|---|---|
| CC pulldowns on the **connector** → the board advertises itself as a 5 V sink | CC sense resistors on the **charger** → no PD negotiation of any kind |
| Over-voltage protection at 5.95 V | Any voltage above 5 V |

Practical consequence: **a PD-only source that will not supply 5 V without negotiation
will not charge this board.** See [`battery-and-charging.md`](battery-and-charging.md).

*(Two earlier readings of this circuit disagreed — one concluded there were no CC
resistors at all. Both resistor groups exist and they are on different parts. Recorded so
the question is not re-opened.)*

## 3. ⚠ Download mode is the power button — there is no reset button

```
Hold the power button ~2 seconds until the red LED blinks, then release.
```

This is stated by the **product page** (EN, zh_CN and ja) and by the **UiFlow2 page**.
The **Arduino quick-start page contradicts it**, saying *"press and hold the reset button
on the side of the device"*.

**The Arduino page is wrong.** The schematic shows exactly three switches on the KEY/RGB
sub-board — `S1` (`PWR_BTN`), `S2` (`G2_KEY1`), `S3` (`G3_KEY2`) — and **no separate reset
button**. The specification table lists *"2× user buttons + 1× power button (ON / OFF /
RESET / BOOT)"*: one physical multi-function button. Resolved in
[`../gaps-and-conflicts.md` R4](../gaps-and-conflicts.md#r4--download-mode-control--resolved-on-the-balance-of-evidence);
marked resolved but `not-tested`.

**The mechanism matters.** GPIO0 is driven by the M5PM1's open-drain `BOOT_OUT_OD`, and
`CHIP_PU` carries `SOC_RESET` from the same chip. So **the power manager, not a physical
button, puts the ESP32-S3 into download mode.** If the M5PM1 is unhappy, you cannot flash
the board — and the M5PM1's own firmware-update mode is a separate thing again
(`SYS_CMD` `0x0C` `CMD=11`, or a long press, lockable via `BTN_CFG_1[7] DL_LOCK`).

Other button behaviour: one short press = power on / reset; two presses in succession =
power off. Third-party projects disable the single-click reset — see
[`buttons-and-rgb-led.md` §6](buttons-and-rgb-led.md#6-the-power-button).

## 4. ⚠ Three strapping pins carry user-facing signals

| GPIO | Strap | Also carries |
|---|---|---|
| **GPIO0** | boot mode | driven by M5PM1 `BOOT_OUT_OD` — by design |
| **GPIO3** | strapping | **User button B** |
| **GPIO45** | strapping (`VDD_SPI`) | **PDM microphone clock** |
| **GPIO46** | strapping (boot messages) | **PDM microphone data** |

Driving the microphone or holding button B during reset perturbs the straps. The vendor
firmware does not appear to guard against this. `inferred` from the pin map,
`not-tested`. The factory firmware does explicitly release the mic pins before
reconfiguring them — see [`microphone.md` §2](microphone.md#2--both-microphone-pins-are-esp32-s3-strapping-pins).

## 5. Serial console and USB CDC

The published build configuration selects **native USB CDC as the console**:

```ini
build_flags = -DARDUINO_USB_CDC_ON_BOOT=1
              -DARDUINO_USB_MODE=1
```

So `Serial` is the USB CDC device, not UART0. Consequences of native USB, which are
normal and not faults:

- **The serial port disappears** on reset, crash, sleep or any USB reconfiguration, and
  reappears as a new device. Auto-reconnecting terminals help.
- Early boot output before CDC enumerates is lost. **UART0 on GPIO43/44 does not vanish**
  and is the reliable channel for boot-time debugging — but it is **not brought to any
  connector**, so using it means probing the board.
- `CORE_DEBUG_LEVEL=0` in the vendor's own snippet means M5GFX's diagnostic messages —
  including `"M5PaperMono need OPI-PSRAM enabled"` — are compiled out. **Raise it when
  something does not work.**

## 6. Flashing

| Route | Notes |
|---|---|
| **`idf.py -p PORT flash`** | The OTP demo README's own instruction: `idf.py set-target esp32s3` → `idf.py build` → `idf.py -p PORT flash`. `reported-working` (vendor README); **not run here** |
| **PlatformIO** | Use the published `[env:m5stack-papermono]` block. `board = esp32-s3-devkitm-1` — there is **no dedicated PlatformIO board definition** |
| **Arduino IDE** | Install the M5Stack board package, select the **`M5PaperMono`** board. Corroborated independently: the shipped binary contains `[Autodetect] board_M5PaperMono` |
| **M5Burner / EasyLoader** | The vendor's GUI route; also how UiFlow2 firmware is installed |

Flash geometry: **16 MB**, single `factory` app at `0x10000` of size `0xF00000`
(15 MiB), plus `nvs` 24 KB at `0x9000` and `phy_init` 4 KB at `0xf000`. **No OTA slot, no
filesystem partition** in either vendor project — so **the shipped firmware is not
field-updatable over the air as built**.

> **QIO vs DIO.** The vendor's PlatformIO snippet specifies `qio_opi`; both shipped
> binaries report **DIO** in their ESP image headers. The hardware supports QIO — all
> four flash data lines are routed and the `Q` in `XM25UH128DHIQT` denotes a factory-set
> QE bit — and `sdkconfig.defaults` pins no flash mode, so DIO is an ESP-IDF default, not
> a hardware limit. Not a defect. Resolved in
> [`../gaps-and-conflicts.md` R2](../gaps-and-conflicts.md#r2--qio-versus-dio-flash--resolved).

## 7. Resources consumed

| Resource | Value |
|---|---|
| ESP32-S3 GPIO | GPIO19, GPIO20 (USB); GPIO43, GPIO44 (UART0) |
| Peripheral | USB-Serial-JTAG / TinyUSB; `UART_NUM_0` |
| Connector | `U1` `TYPEC-302-BRP16SC08` |
| Filter | `FT1` common-mode choke on D±  |

USB is **not** used for anything else on this board — no UVC, no MSC, no HID in any
vendor firmware. The silicon supports them; nobody has demonstrated them here.

## 8. Limits

| Class | Limit |
|---|---|
| **Silicon (ESP32-S3)** | Native USB 1.1 full speed. No USB host in any vendor configuration |
| **Board** | **No USB-PD** (§2). 5 V only, OVP at 5.95 V |
| **Board** | UART0 is not exposed on any connector |
| **Board** | Reset and boot strap are owned by the M5PM1 — you cannot force download mode without it |
| **Framework** | `CORE_DEBUG_LEVEL=0` in the vendor snippet hides the diagnostics you need |
| **Framework** | No OTA partition as shipped |
| **Observed** | Nothing. **No one has reported a flashing session on real hardware in any source located** |

## 9. Conflicts

| Combination | Verdict | Mechanism |
|---|---|---|
| USB CDC + UART0 | ✅ independent | Different peripherals and pins |
| USB + [charging](battery-and-charging.md) | ✅ simultaneous | Same connector, separate paths |
| Download mode + [button B](buttons-and-rgb-led.md) held | ⚠ | GPIO3 strap (§4) |
| Download mode + [microphone](microphone.md) active across reset | ⚠ | GPIO45/46 straps (§4) |
| USB CDC + deep sleep | ⚠ expected | The CDC device disappears; this is normal |
| USB + a PD-only charger | ❌ | §2 |

## 10. Debugging

| Symptom | Cause |
|---|---|
| Cannot find the reset button | **There isn't one.** Use the power button (§3) |
| Board will not enter download mode | Hold the power button until the **red LED blinks** — releasing early does nothing |
| Serial port vanishes | Native USB. Expected |
| No boot log at all | `CORE_DEBUG_LEVEL=0`; or CDC had not enumerated yet. UART0 does not have this problem |
| Blank screen, everything else fine | **Look for `M5PaperMono need OPI-PSRAM enabled`** — which you will not see at debug level 0. See [`epaper-display.md` §7](epaper-display.md#7-octal-psram-is-mandatory--and-the-failure-looks-like-dead-hardware) |
| Board does not charge from a given supply | PD-only source (§2) |
| Flashed image will not run | Check `board_build.arduino.memory_type = qio_opi` and the 16 MB partition scheme |

## 11. Recovering the factory image

Two images were retrieved from the M5Burner public API and are retained in
[`../artifacts/firmware/`](../artifacts/firmware/):

| Image | Bytes | Build identity |
|---|---|---|
| `C153-PaperMono-UserDemo-v1.2.bin` | 2,868,208 | `PaperMono-UserDemo`, version **`c78f6c5-dirty`**, IDF v5.5.1, 2026-08-06 |
| `crosspoint-paper-mono-cjk-1.5.0-RC.bin` | 10,319,500 | third-party `crosspoint-reader-mono` e-reader |

> The official image reports **`-dirty`**: built from an uncommitted tree, therefore **not
> reproducible from any published commit** of `m5stack/M5PaperMono-UserDemo`. That is why
> the bytes are retained rather than referenced.
>
> Also: the vendor link labelled **"PaperMono Factory Reset Firmware"** resolves to a
> firmware record named **"PaperMono UserDemo"** — the same image, differently labelled.
> It restores the demo application; it is not a distinct factory-reset payload.

How to fetch such images yourself is in
[`vendors/m5stack` §M5Burner API](../../../../vendors/m5stack/README.md).

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; USB, UART and boot path are identical on C153 and C153-LITE |
| Framework range | ESP-IDF 5.5.1 · arduino-esp32 3.3.10 · PlatformIO `espressif32@6.12.0` |
| Evidence | USB/UART pins: **schematic only** (absent from vendor pin tables). Download mode: **vendor-documented**, `reported-working`, with one contradicting vendor page. Flash geometry: **read from both projects' `partitions.csv` and from the shipped binaries' partition tables**, `executed-success` |
| Confidence | High on wiring and partitioning; **nothing about flashing has been executed on a device** |
| Last verified | **2026-09-01** |

## Related

- [`../pinouts-and-buses.md#boot-reset-and-download-mode`](../pinouts-and-buses.md#boot-reset-and-download-mode) · [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md)
- [`battery-and-charging.md`](battery-and-charging.md) · [`buttons-and-rgb-led.md`](buttons-and-rgb-led.md) · [`microphone.md`](microphone.md) · [`power-and-sleep.md`](power-and-sleep.md)
- [`components/xmc/xm25uh128dhiqt`](../../../../components/xmc/xm25uh128dhiqt/README.md) · [`components/espressif/esp32-s3r8`](../../../../components/espressif/esp32-s3r8/README.md)
