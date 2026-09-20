# X4 Pro — USB

> ESP32-S3 native USB-OTG. Data only — **charging is over pogo pins.**
> Evidence: SDK-stated; MSC not ported. 2026-09-04.

| Signal | GPIO |
|---|---:|
| D− | **19** |
| D+ | **20** |

Native ESP32-S3 USB peripheral, no external bridge IC.

## What stock does

- **USB-CDC** serial.
- **USB-MSC** — "USB Transfer", exposing the SD card as a mass-storage device.

## What FreeInk does

CDC yes; **USB-MSC is present in stock firmware but has not been ported** to the
SDK. Listed as pending/optional. If you need SD-over-USB, you are writing it.

`FREEINK_LOG_TRANSPORT_USB_CDC_WRITE` is a supported log transport.

## Hard warning

**Never run an I²C or GPIO probe across GPIO19/20 at boot.**

The Xteink **C3** X3/X4 detect fingerprint pokes SDA 20 / SCL 0. On this **S3**
those land on **D+ and a boot strap**. This is precisely why `XteinkDetect`
compiles the C3 fingerprint to a no-op unless a C3 profile is in the build:

```c
// XteinkDetect.cpp:19, commit 2400379
#define FREEINK_XTEINK_C3 (FREEINK_DEVICE_X4 || FREEINK_DEVICE_X3)
```

A build that defines both a C3 and the X4 Pro profile would be dangerous.

## USB detect

`usbDetect = PIN_UNASSIGNED`. GPIO10 is floated in the SDK as a candidate but is
**unconfirmed** — and GPIO10 is already the GT911 INT, so treat that candidacy as
almost certainly wrong. Stock's battery icon uses the GPIO21 charge state instead.

## Status

`reported-working` for CDC. `not-ported` for MSC. `unknown` for VBUS detect.
