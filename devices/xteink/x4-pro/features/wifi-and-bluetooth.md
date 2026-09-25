# X4 Pro — Wi-Fi and Bluetooth

> ESP32-S3 integrated radios. **This is the weakest-evidenced guide in this
> device record** — see status. 2026-09-04.

## Capability summary

| Radio | Status |
|---|---|
| Wi-Fi 2.4 GHz b/g/n | Present (ESP32-S3 integrated) |
| Bluetooth LE 5 | Present (ESP32-S3 integrated) |
| Bluetooth Classic | **Not available** — the ESP32-S3 has no BR/EDR radio |
| Antenna | **Not characterised.** No teardown, no FCC filing |

## Evidence status — read this first

The X4 Pro `BoardProfile` says nothing about radios; the SDK simply relies on the
SoC. The **X4 Classic** doc states plainly *"WiFi and BLE radios are present"*,
and the X4 Classic shares this board. That is the strongest statement located.

So: radio presence is **`inferred` from the SoC and from a sibling's
documentation**, not directly confirmed on an X4 Pro. It is not seriously in
doubt — the stock firmware performs OTA over HTTP and hosts a web file manager —
but it has not been demonstrated here.

## What stock uses the radio for

Recovered from the **X4 (C3)** dump and assumed shared:

| Endpoint | Role |
|---|---|
| `http://gotaserver.xteink.com/api/check-update` | OTA check — **plain HTTP, not HTTPS** |
| `http://bofi.xteink.cn/index.html` | On-device web file manager |

Also present in that dump: the string `XT-EPD`, plausibly an AP SSID or BLE
device name — **not confirmed**.

## BLE in the community firmware

The FreeInk SDK ships `libs/network/BleKeyboardHost`, i.e. **BLE HID host**
support for Bluetooth page-turner remotes. There is an established accessory
ecosystem around this (`CrazyCoder/free2-updater-patch` exists to fix a broken
VID check in a JieLi page-turner's updater so it pairs with Xteink devices).

`hannah-nula/crosspoint-x3-ble-page-turner` is a fork specifically for *"validated
BLE page-turner reconnect support"* — implying reconnect is fragile by default.

## Resource notes

Wi-Fi and BLE share one 2.4 GHz radio on the ESP32-S3; concurrent use costs
throughput and power. **No coexistence testing on this device was found.**

## Status

`inferred` for presence. `reported-working` for BLE page-turners.
`not-tested` for throughput, range, coexistence and power.

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 13:* | Antenna | **Not characterised.** No teardown, no FCC filing |
>

**Xteink is an FCC grantee.** Applicant **Shenzhen Xiaohu Xingtong Technology Co., Ltd.**, grantee code **`2BTR9`**, registered 2025-12-21, holding **five granted Original Equipment authorisations**:

| FCC ID | Granted | Device |
|---|---|---|
| `2BTR9-X4L` | 2026-08-13 | XTEINK X4 Light |
| `2BTR9-X4C` | 2026-07-20 | XTEINK X4 Classic |
| `2BTR9-X4PRO` | 2026-06-16 | XTEINK X4 Pro |
| `2BTR9-XTEINKX4` | 2026-01-05 | XTEINK X4 |
| `2BTR9-XTEINKX3` | 2025-12-26 | XTEINK X3 |

The original finding confused **"no mark visible in a product photograph"** with **"no grant exists"**. Those are different claims, and only the first was tested.

- ✅ **Survives:** no FCC ID was legible on the exteriors photographed. Not re-tested.
- ❌ **Refuted:** any reading that these devices are uncertified or unauthorised for the US.

47 CFR §2.935 permits an **e-label** in software instead of a printed mark, which is ordinary for a device with a screen. **That is a likely explanation and it was not verified.**

The absence was never re-searched in 2026-09-04 because **no FCC ID was known and the grantee code had not been found**. Enumerating the grantee — not searching the product name — is what resolved it. Method: [`guides/research/finding-certification-records.md`](../../../../guides/research/finding-certification-records.md).

Full record, with controls: [`certification-and-compliance.md`](../certification-and-compliance.md).

Listed in [`research/passes/index-merge/corrections-requiring-review.md`](../../../../research/passes/index-merge/corrections-requiring-review.md).
