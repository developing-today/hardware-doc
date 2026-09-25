# Wi-Fi and Bluetooth — M5Stack PaperMono

> **How do I get on the network?**
> Hardware revision **V0.6.2** · snapshot **2026-09-01** · nothing tested on hardware.

**This is a short guide.** The radio is the ESP32-S3's own, there is nothing
PaperMono-specific about using it, and no measurement of any kind exists for this board.
What follows is the board-specific delta and nothing else.

## 1. Capability summary and the hardware path

**2.4 GHz Wi-Fi and Bluetooth LE, both from the ESP32-S3R8 die**
([`components/espressif/esp32-s3r8`](../../../../components/espressif/esp32-s3r8/README.md)),
which is a bare QFN die on the main board rather than a shielded module.

| Item | Status |
|---|---|
| **Wi-Fi 2.4 GHz** | Listed in M5Stack's specification table |
| **Bluetooth LE** | **A silicon capability M5Stack never lists.** Not in the spec table, not in the feature list, not in the comparison table |
| Wi-Fi 5 GHz / 6 | Not present — ESP32-S3 is 2.4 GHz only |
| Bluetooth Classic | Not present — ESP32-S3 has **no** BR/EDR. No A2DP, HFP or SPP |
| Antenna | Not identified in any retrieved document (see §5) |

> **"Bluetooth 5.0 LE + Mesh" is a publication's inference, not a vendor spec.** One
> launch article printed it; M5Stack's own specification table does not mention Bluetooth
> at all. BLE certainly works — it is in the silicon — but nobody has demonstrated it on
> this board, and no vendor statement backs any particular profile claim. Recorded in
> [`../gaps-and-conflicts.md`](../gaps-and-conflicts.md#claims-examined-and-rejected).
>
> Independent corroboration that BLE is at least being used: one third-party project,
> `EggUncle/PaperMonoCalendar`, describes BLE activity tiles — though its README is
> explicit that its preview images are software-generated, **not device photographs**.

## 2. Prerequisites

Nothing board-specific. arduino-esp32 3.3.10 or ESP-IDF 5.5.1, `WiFi.h` or
`esp_wifi`/NimBLE as usual. The vendor's `sdkconfig.defaults` additionally enables
`CONFIG_LWIP_IP_FORWARD=y` and `CONFIG_LWIP_IPV4_NAPT=y` — NAT/routing — for reasons the
firmware never uses. Inherited from a template, `inferred`.

## 3. Minimal procedure

The factory firmware's Wi-Fi scan app is plain arduino-esp32 (`app_wifi_scan.cpp`):

```cpp
#include <WiFi.h>

WiFi.mode(WIFI_STA);
WiFi.disconnect(false, false);
WiFi.scanDelete();
bool started = (WiFi.scanNetworks(/*async=*/true, /*show_hidden=*/true) == WIFI_SCAN_RUNNING);
// ... later
int n = WiFi.scanComplete();
for (int i = 0; i < n; ++i) {
  auto ssid = WiFi.SSID(i);
  auto rssi = WiFi.RSSI(i);
  bool secure = WiFi.encryptionType(i) != WIFI_AUTH_OPEN;
}
WiFi.scanDelete();
```

**The asynchronous scan matters on this board more than on most.** A blocking scan is
seconds of nothing, and on an e-paper device you cannot show a spinner cheaply — every
progress update is a panel refresh, and
[refresh discipline](epaper-display.md#8-panel-safety--the-rules-that-are-not-optional)
says you must not loop partial refreshes. Scan asynchronously and redraw once.

Standard approaches apply unchanged for everything else: STA/AP mode, WPA2/WPA3, ESP-NOW,
NimBLE or Bluedroid, provisioning. There is no PaperMono-specific setup step.

## 4. Resources consumed

| Resource | Value |
|---|---|
| ESP32-S3 GPIO | **none** — the radio is internal |
| RAM | The Wi-Fi and BLE stacks take internal SRAM out of the 512 KB, competing with the display driver's own allocations |
| PSRAM | Not required by the radio, but the display **mandates OPI PSRAM** anyway |
| Power | Unquantified. Wi-Fi TX bursts are the largest transient load on the board |

## 5. Limits

| Class | Limit |
|---|---|
| **Silicon** | 2.4 GHz only; **no Bluetooth Classic**; single radio shared between Wi-Fi and BLE with the usual coexistence scheduling |
| **Board** | The ESP32-S3 is a **bare die, not a shielded module**, alongside a [LoRa module](lora.md) and an [NFC front end](nfc.md) — three radios in a 62 × 101 × 8 mm slab |
| **Board** | **Antenna identified 2026-09-20.** Supplier Shenzhen Rongshengyuan, part **`RSY-E8131`** (V3.0, 2026-02-01), a multi-band assembly whose 2.4 GHz element is 14.42 × 5.04 mm, IPEX4, VSWR < 4. Measured gain across 2400–2480 MHz is **−0.94 to +0.16 dBi**, total efficiency **19.9–24.1 %**; it is tuned slightly high, peaking at 2490–2500 MHz. The FCC internal photos annotate the Wi-Fi/BLE element on the **bottom edge of the main PCB** |
| **Board** | **Certified 2026-08-12 — FCC ID `2AN3WM5PAPERMONO`.** Corrected 2026-09-20: `docs.m5stack.com/en/certification` really does return zero matches, but the board is certified. **Wi-Fi channels 1–11 only (2412–2462 MHz); 40 MHz only on 2422–2452 MHz.** Measured conducted output: 17.17 dBm max (802.11b), 16.22 (g), 15.43 (n20), 15.51 (n40); BLE 5.56 dBm. **Wi-Fi and BLE are declared *not* simultaneously transmitting.** [`../certification.md`](../certification.md) |
| **Framework** | None specific |
| **Observed** | **Nothing at all.** No throughput, range, sensitivity or power measurement exists from M5Stack or from any independent source. The FCC filing gives *conducted* power and antenna gain — not throughput, not range, and **no EIRP figure for any 2.4 GHz mode** |

## 6. Conflicts and simultaneous use

| Combination | Verdict | Mechanism |
|---|---|---|
| **Wi-Fi + [LoRa](lora.md)** | ✅ **they do not share a radio** | Wi-Fi/BLE is 2.4 GHz on the ESP32-S3 die; LoRa is **sub-GHz (868–923 MHz)** on a separate SX1262 module with its own antenna. There is no RF contention between them and no shared peripheral — LoRa is on `SPI3_HOST`, the radio is internal. The only shared resources are CPU time and the power budget |
| Wi-Fi + BLE | ⚠ coexistence | One 2.4 GHz radio, time-sliced. Standard ESP32-S3 behaviour; enable modem sleep |
| **Wi-Fi + [display](epaper-display.md) refresh + [microSD](microsd.md)** | ⚠ **untested and worth testing** | No pin conflict whatsoever. The contention is GDMA channels, PSRAM bandwidth and the L3B rail during a multi-second refresh. **Nobody has run this combination.** See [`../resources-and-conflicts.md`](../resources-and-conflicts.md) |
| Wi-Fi + [battery](battery-and-charging.md) | ⚠ unquantified | TX bursts on a 1150 mAh cell with no published current figure |
| Wi-Fi + [NFC](nfc.md) | ✅ no RF interaction | 13.56 MHz vs 2.4 GHz. Both compete for CPU and the single I²C bus, not for spectrum |
| Wi-Fi + [sleep](power-and-sleep.md) | ✅ standard | Modem sleep, then the M5PM1 states below it |

## 7. Debugging

Nothing board-specific. The one PaperMono-flavoured trap is that
`CORE_DEBUG_LEVEL=0` in the vendor's published build flags hides the logs you would use
to diagnose anything — see [`usb-and-serial.md`](usb-and-serial.md).

## 7b. A working BLE image-transfer protocol — third-party, added 2026-09-11

`ciniml/paper_name_plate` implements full-screen image push over BLE in Rust
(`esp-radio` + `bleps`, `src/app/ble.rs`). Dated 2026-09-04 in its design
document and described as implemented with a measured figure — **~12–14 s for a
full screen from a PC** — though it carries no explicit hardware-verified stamp.
Recorded as *reported working*, not verified.

It is worth documenting because it solves three problems this board actually has.

### Protocol v2 — a windowed, acknowledged transfer

```
START  : 10 w h len crc32 ack_every
DATA   : off:u16 | payload          (BLE Write Command, sent ack_every at a time)
STATUS : state received expected    (notification — ACK/NAK)
COMMIT : CRC32 verified, notified, then the display updates
```

Out-of-order DATA is **discarded and the expected offset is notified**, so the
client rewinds rather than the device reassembling. The same windowed mechanism
carries text content via `CTRL 11 len crc32 ack_every`, sending UTF-8
`name\nemail\ngithub\nx\nnote\nurl`.

### Two implementation details that are not obvious

> 「GATT テーブルは手組みで DATA/CTRL に Write-Without-Response(0x04) を宣言
> （Android Chrome が高速書き込みを許可する条件）。bleps は `mtu128`（`Data` の 256B
> バッファを超えないため）。」

*"The GATT table is hand-assembled to declare **Write-Without-Response (0x04)** on
DATA/CTRL — **the condition under which Android Chrome permits fast writes**.
`bleps` is set to `mtu128` so as not to exceed `Data`'s 256-byte buffer."*

The first is a browser-compatibility constraint, not a BLE one: **Web Bluetooth
on Android Chrome only grants fast writes if the characteristic advertises
Write-Without-Response.** That is the kind of detail that costs a day.

### BLE and NFC contend for one core

> 「BLE と NFC タグエミュレーションは 1 コアで競合するため、BLE 接続中は NFC 待受を
> 止めて BLE を優先する」

*"BLE and NFC tag emulation contend on a single core, so while BLE is connected
the NFC listen is stopped and BLE is prioritised"* (`tick_light`). During
reception everything except the HCI pump is halted.

**This is a real constraint for anyone planning to run both**, and it is not
visible from the schematic — it is a CPU-time conflict, not a bus or pin one.
Compare [`nfc.md`](nfc.md) and the resource table in
[`../resources-and-conflicts.md`](../resources-and-conflicts.md).

### The memory ceiling is the interesting part

> 「ヒープ ~155KB に BLE スタック + 受信画像 48KB + 表示中画像 48KB は入らないため、
> 8KB を超える画像は描画・保存後にヒープから捨て、再描画時にフラッシュから読み直す」

*"A ~155 KB heap cannot hold the BLE stack plus a 48 KB received image plus a
48 KB displayed image, so images over 8 KB are dropped from the heap after being
drawn and saved, and re-read from flash on redraw"* (`draw_plate` / `trim_image`).
Flash writes split header and data into two writes **to avoid making a copy**.

This is a concrete data point on the recurring PaperMono question of whether
PSRAM is needed: **a project that does not enable PSRAM has to stream through
flash to fit two framebuffers and a BLE stack.** See
[`power-and-sleep.md`](power-and-sleep.md) and the PSRAM discussion in
[`epaper-display.md`](epaper-display.md).

### Power behaviour reported alongside it

- Main-loop busy-wait replaced with esp-rtos task sleep (idle hook = WFI, 1 kHz
  tick). Their heartbeat reports `idle=NN%` — **~98 % at rest**.
- NFC chip accessed over I²C **only** when its IRQ pin (GPIO6) is high, during a
  reader exchange, or on a 250 ms safety poll. Touch read only when INT (GPIO4)
  is low. HCI pumped only when the receive queue is non-empty.
- BLE advertising interval **200–250 ms**. TF card power (`TF_EN`) switched off.
- **Deep sleep** after 120 s idle **and** 60 s since boot **and** USB host absent
  — the last detected via the **USB-JTAG SOF frame counter**. Wake sources are
  RTC-IO: NFC IRQ (GPIO6 high), touch INT (GPIO4 low), buttons A/B (GPIO2/3 low),
  plus a 6-hour timer. Wake is a reset, and `run()` checks
  `reset_reason == CoreDeepSleep` to skip the e-paper initial refresh and
  frontlight blink, since the panel holds its image.

Image transfer over NFC also exists for small images (**≤ ~630 B**), as an
`image/x-plate` MIME record or `B64:<base64>` text — see [`nfc.md`](nfc.md).

## 8. What is not established

- **No Wi-Fi or BLE measurement of any kind exists for this board.**
- **No antenna is documented.** Type, placement, gain and the effect of the metal-adjacent
  handheld form factor are all unknown.
- **No regulatory approval is published**, for Wi-Fi, BLE or LoRa.
- Whether any BLE profile has been demonstrated on a real device — one third-party
  project claims BLE tiles but shows no hardware.

## Applicability

| Field | Value |
|---|---|
| Hardware revision | **V0.6.2**; identical on C153 and C153-LITE |
| Framework range | arduino-esp32 3.3.10 · ESP-IDF 5.5.1 |
| Evidence | Capability: **silicon-level**, plus M5Stack's Wi-Fi spec line. Scan sketch: **read from vendor source** (`app_wifi_scan.cpp`). Everything performance-related: **absent** |
| Confidence | High that it works (it is stock ESP32-S3); **zero on how well** |
| Last verified | **2026-09-01** |

## Related

- [`lora.md`](lora.md) — the other radio, and why it is not in competition with this one
- [`nfc.md`](nfc.md) · [`power-and-sleep.md`](power-and-sleep.md) · [`../resources-and-conflicts.md`](../resources-and-conflicts.md)
- [`components/espressif/esp32-s3r8`](../../../../components/espressif/esp32-s3r8/README.md)
