# X4 — Wi-Fi and Bluetooth

> ESP32-C3 integrated radios. 2026-09-04.

| Radio | Status |
|---|---|
| Wi-Fi 2.4 GHz b/g/n | Present (SoC) |
| Bluetooth **LE 5** | Present (SoC) |
| Bluetooth Classic | **Not available** — the ESP32-C3 has no BR/EDR radio |
| Antenna | **not characterised** — no teardown of this device, no FCC filing |

## Direct evidence the radio is used

Unlike the X4 Pro, the X4's radio use is **demonstrated from its own firmware**.
Strings extracted from the factory dump
([`../factory-firmware.md`](../factory-firmware.md)):

| String | Meaning |
|---|---|
| `http://gotaserver.xteink.com/api/check-update` | Wi-Fi OTA check — **plain HTTP** |
| `http://bofi.xteink.cn/index.html` | On-device **web file manager** — the device runs an HTTP server |
| `http://bofi.xteink.cn/index.html?ip=` | same, with device IP |
| `XT-EPD` | Probable AP SSID or BLE name — **not confirmed** |

So the stock firmware both **fetches over HTTP** and **serves a web UI** — the
latter explains the unusually large 3.4 MB SPIFFS partition.

## BLE page turners

The FreeInk SDK ships `libs/network/BleKeyboardHost` (BLE HID host). There is a
real accessory ecosystem: [`CrazyCoder/free2-updater-patch`](https://github.com/CrazyCoder/free2-updater-patch)
exists purely to *"bypass broken VID check"* in a JieLi/hanlinyue page-turner's
updater *"for Free2 Bluetooth page turners (working with Xteink X4 and similar
devices)"*.

## Community projects using the radio

`maddiedreese/xteink-terminal` (*"tmux bridge for using an XTeInk X4 as a small
Wi-Fi e-ink terminal display"*), `keithwithAI/xteink-agenda` (Google Calendar via
FastAPI), `fsocietyipa/WienerLinien-XteinkX4` (departure board),
`pocmaker42/xteink-todo`, `Wferr/xteink-sync`.

## Not established

Throughput, range, coexistence, power cost, and whether `XT-EPD` is an SSID.
No measurement exists.

## Status

`reported-working` — demonstrated by firmware strings and many working projects.
`not-tested` for any quantitative property.

---

## ⚠ Correction, 2026-09-11 — Xteink FCC grants exist

The line(s) below, still present above and deliberately unedited, are **refuted**:

> *line 10:* | Antenna | **not characterised** — no teardown of this device, no FCC filing |
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
