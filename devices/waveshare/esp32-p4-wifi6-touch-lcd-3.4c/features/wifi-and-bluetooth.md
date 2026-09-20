# How do I use Wi-Fi 6 and Bluetooth? — ESP32-P4-WIFI6-Touch-LCD-3.4C

> Evidence status: **vendor documentation + vendor source code. Untested on hardware.**
> Applies equally to the [4C](../../esp32-p4-wifi6-touch-lcd-4c/README.md).

## Read this before anything else

**The ESP32-P4 has no radio.** None. No Wi-Fi, no Bluetooth, no 802.15.4.

Every wireless capability on this board comes from a **second, separate microcontroller** — an
ESP32-C6-MINI-1-N4 — connected to the P4 over **SDIO**. The P4 runs your application; the C6 runs
a firmware that exposes its radio as a remote service.

This is the single most important architectural fact about the board, and it is where most of the
surprises live.

## Hardware path

```
  ESP32-P4  <--- SDIO ---> ESP32-C6-MINI-1-N4  ---> antenna
 (your app)                (radio co-processor,
  esp_wifi_remote           runs its own firmware,
                            flashed via its OWN header)
```

| Item | Value |
|---|---|
| Radio module | ESP32-C6-MINI-1-N4 |
| Host link | SDIO |
| Software model | Espressif `esp_hosted` / `esp_wifi_remote` split stack |
| Capabilities | Wi-Fi 6 (802.11ax, 2.4 GHz), Bluetooth 5 LE, 802.15.4 |
| C6 flashing | **Separate SH1.0 4-pin header** |
| Components | `espressif/esp_hosted: "*"`, `espressif/esp_wifi_remote: "*"` |

Note "Wi-Fi 6" here means **2.4 GHz 802.11ax**. The ESP32-C6 is a 2.4 GHz-only part. Do not expect
5 GHz or 6 GHz operation from a board marketed as "WIFI6".

802.15.4 means the C6 is capable of Thread/Zigbee in principle. Whether Waveshare's shipped C6
firmware exposes that through the P4 is **unknown** — no demo uses it.

## Software

Your P4 application does **not** call `esp_wifi_*` against local hardware. It links
`esp_wifi_remote`, which forwards the same familiar API over SDIO to the C6.

```yaml
# idf_component.yml
dependencies:
  idf: "^5.0"
  espressif/esp_hosted: "*"
  espressif/esp_wifi_remote: "*"
```

Reference project:
`../../esp32-p4-wifi6-touch-lcd-xc-shared/artifacts/demo/ESP-IDF/04_wifistation/`

The API surface is deliberately close to normal ESP-IDF Wi-Fi, so most example code ports with
little change. What does *not* port is anything assuming the radio is local — RF calibration,
direct PHY access, or coexistence tuning.

> The `"*"` version floats in Waveshare's manifests. `esp_hosted` and `esp_wifi_remote` are
> actively evolving and the P4/C6 pairing is comparatively new; **pin explicit versions** in real
> projects or a component update can change behaviour under you.

## Flashing — there are two MCUs

This is where boards "break".

| Target | Port | Purpose |
|---|---|---|
| **ESP32-P4** | Type-C (CH343P USB-UART) | Your application |
| **ESP32-C6** | **SH1.0 4-pin header** | Radio firmware |

The board exposes **two** SH1.0 4-pin headers — one brings out the C6 for firmware flashing, one
brings out the P4 serial port for flashing and debugging. They are not interchangeable.

**A board that will not join Wi-Fi very often has perfectly good P4 firmware and stale or missing
C6 firmware.** Symptoms look like an application bug — init failures, timeouts, no scan results —
but the fault is on the other chip, which your normal flashing workflow never touches.

Before debugging your Wi-Fi code, confirm the C6 firmware version matches what your
`esp_hosted` / `esp_wifi_remote` version expects. Version skew across the SDIO link is a real and
easy-to-hit failure mode.

## Resource conflicts

| Resource | Shared with | Note |
|---|---|---|
| SDIO bus to C6 | — | Dedicated to the radio link |
| SDIO 3.0 microSD | **Possibly the same peripheral** | See below |

The board has **two** SDIO consumers: the C6 radio link and the microSD slot. The
[microSD pins are now known](../pinouts-and-buses.md#microsd--connector-sd1) — CLK 43, CMD 44,
DAT0–3 on 39–42 — but whether the two consumers use separate SDMMC host peripherals or share one
is still **unresolved**. The P4 has more than one SDMMC host, so separate hosts are plausible;
the C6 link's own SDIO net names were not traced.

### Likely answered 2026-08-26 — and the answer is "they conflict"

The `netseye/linux-waveshare-xc` port states:

> *"microSD — **Mutually exclusive with Wi-Fi/BT**. P4 exposes one DW-MMC host; this build selects
> C6 SDIO slot 1 instead of card slot 0."*

So: one DW-MMC controller, two slots — **slot 0 = microSD, slot 1 = the C6 radio link** — and their
build picks one.

**Caveats:** community evidence, about a *Linux* port rather than ESP-IDF, and explicitly
unvalidated on hardware by its own author. ESP-IDF may arbitrate differently.

**Practical guidance is unchanged, but firmer: do not design around simultaneous microSD and Wi-Fi
until you have tested it on hardware.** This raises the odds they genuinely conflict.

They also document the link itself: **SDIO D0–D3 = GPIO14–17, CLK = 18, CMD = 19, C6 reset =
GPIO54 active-high** — see [`pinouts-and-buses.md`](../pinouts-and-buses.md#esp32-c6-sdio-link).

## Limits

| Limit | Value | Kind |
|---|---|---|
| Bands | 2.4 GHz only | Silicon (ESP32-C6) |
| Standards | Wi-Fi 6 (11ax), BT 5 LE, 802.15.4 | Silicon |
| Host link | SDIO | Board |
| Throughput | **Unknown — not measured** | — |
| Latency | **Unknown — not measured** | — |

Throughput and latency are bounded by the SDIO link and the hosted-stack overhead, **not** by the
radio alone. No figure is given because none was measured, and quoting an ESP32-C6 standalone
number here would be misleading — the bottleneck is a different component.

## Pitfalls

1. **Assuming the P4 has a radio.** It does not.
2. **Forgetting the C6 firmware.** Two chips, two flash targets.
3. **Expecting 5 GHz** from "WIFI6" branding. 2.4 GHz only.
4. **Floating component versions** across a fast-moving hosted stack.
5. **Assuming Wi-Fi and SD coexist freely.** Both are SDIO; contention unverified.

## Open questions

- Does Waveshare ship prebuilt C6 firmware, and at what version? (They appear not to.)
- ~~Do the C6 link and the microSD share an SDMMC host?~~ — **likely yes, one DW-MMC host**;
  needs hardware confirmation.
- Is 802.15.4 (Thread/Zigbee) reachable from the P4 with the shipped firmware?
- Real throughput and latency over the SDIO link.

## Related

- [Storage](./storage.md) — the other SDIO consumer
- [Development and flashing](../development.md)
- [ESP32-P4 chip record](../../../../components/espressif/esp32-p4/README.md)
- [Gaps and conflicts](../gaps-and-conflicts.md)
