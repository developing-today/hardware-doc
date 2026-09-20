# Inkplate Peripheral Mode — drive the display over UART, no reprogramming

> Every Inkplate ships with firmware that turns it into a **serial-controlled display**. You send ASCII commands over UART; it draws. No Arduino, no flashing, no ESP32 code.
> Snapshot **2026-08-24**. Source: `peripheral-mode.rst` from Soldered's documentation repository, preserved at [`artifacts/docs/Inkplate-documentation/source/peripheral-mode.rst`](../artifacts/docs/Inkplate-documentation/source/peripheral-mode.rst).

## Why this matters

This is the most under-advertised feature of the Inkplate platform. It means:

- You can attach an Inkplate to a **Raspberry Pi, an STM32, a laptop, or any microcontroller with a UART** and use it as a dumb e-paper display, with no ESP32 development at all.
- You can prototype layouts from a Python REPL before writing a line of firmware.
- You can drive it from a language or platform with no ESP32 toolchain.
- It is a **diagnostic tool**: if `#?*` returns `OK`, the board, USB bridge, ESP32 and panel are all alive. That is a fast way to triage a board that seems dead.

Soldered publishes reference integrations for both use cases:

- [`Inkplate-Peripheral-Mode-Raspberry-Pi-Example`](https://github.com/SolderedElectronics/Inkplate-Peripheral-Mode-Raspberry-Pi-Example)
- [`Inkplate-Peripheral-Mode-STM32-Example`](https://github.com/SolderedElectronics/Inkplate-Peripheral-Mode-STM32-Example)

## ⚠ There are TWO incompatible peripheral protocols

**The published documentation describes the OLD protocol. The current library ships the NEW one.** This is the most important thing on this page, and it is not flagged anywhere by the vendor.

| | **Old (documented)** | **New (shipped in the library)** |
|---|---|---|
| Framing | `#<op>(<args>)*` | `TS;<cmd>;<rpt>;<size>;<payload>;<stop>` |
| Start flag | `#` | **`TS`** (literal two characters) |
| Separator | `,` inside parentheses | **`;`** (`TEMR_CHAR` in `settings.h`) |
| Opcode | single ASCII char (`0`, `A`, `C`…) | **16-bit hex** (`0x000A` = drawPixel) |
| Coordinates | **fixed-width, zero-padded** (`001`) | **variable width**, parsed with `atol()` |
| Batching | one command per message | **repeatable flag** — many pixels in one packet |
| Commands | ~40 | **60** |

Both the `Inkplate5` and `Inkplate5V2` examples in the current library (`examples/<board>/Diagnostics/Peripheral_Mode/`) implement the **new** protocol. Source: `InkplatePeripheralMode.cpp`, `commandList.h`, `settings.h`.

### This resolves the "coordinates above 999" question

I previously recorded as unresolved whether the 3-digit `XXX` format could address the Inkplate 5 Gen 2's 1280-pixel width. **The question is moot on the current firmware**: the new protocol splits arguments on `;` and converts them with `atol()`, so coordinates are arbitrary-width and 1280 is expressible without difficulty.

If you are running genuinely old firmware that implements the `#0(001,005,04)*` format, the limit is real — but that firmware is no longer what the library builds.

## New protocol format

```
TS;<command>;<repeatable>;<payloadSize>;<arg>;<arg>;…;<stop>
```

| Field | Encoding |
|---|---|
| `TS` | literal start flag, found with `strstr(_buffer, "TS")` |
| `<command>` | **hex**, e.g. `A` for `CMD_DRAW_PIXEL` (0x000A). Zero is rejected as invalid |
| `<repeatable>` | **hex**, `0` or `1` only — anything else is discarded |
| `<payloadSize>` | **hex**, byte count of the payload |
| args | separated by `;`, variable width |
| stop | the parser locates the final `;` at `payload + payloadSize` |

The **repeatable flag** is the interesting part. With it set, one packet can carry many argument groups and the handler loops over them:

```c
checkArguments(&_numberOfArgs, 3, _repeat);
for (int i = 0; i < _numberOfArgs; i += 3) { … drawPixel(atol(_argX), atol(_argY), atol(_argColor)); }
```

So `drawPixel` can plot hundreds of pixels per packet instead of one command per pixel — a large throughput win over the old protocol, and the reason the serial buffer is **65,535 bytes allocated in PSRAM**.

### Runtime settings (`settings.h`)

| Constant | Value |
|---|---|
| `SERIAL_BUFFER_SIZE` | **65535** bytes, in PSRAM |
| `SERIAL_TIMEOUT_MS` | 100 ms after the last character |
| `SERIAL_BUFFER_CLEAN_TIME_MS` | 60000 ms — stale/invalid commands are flushed after a minute |
| `TEMR_CHAR` | `;` |
| `SERIAL_UART_RX_PIN` / `TX` | **3** / **1** |
| Default baud | **115200** (`begin(..., 115200ULL, ...)`) |

### New capabilities absent from the old protocol

The 60-command list includes things the documentation never mentions:

| Command | Code | Note |
|---|---|---|
| `CMD_CONNECT_WIFI` / `CMD_DISCONNECT_WIFI` | 0x41 / 0x42 | **Wi-Fi control over UART** |
| `CMD_GET_REQUEST` / `CMD_POST_REQUEST` | 0x43 / 0x44 | **HTTP from the host, via the Inkplate** |
| `CMD_ESP32_DEEPSLEEP` / `LIGHTSLEEP` | 0x3B / 0x3C | Host-commanded sleep |
| `CMD_TOUCH_INIT` / `AVAILABLE` / `GET_DATA` | 0x3D–0x3F | Touch (on touch-capable boards) |
| `CMD_SD_CARD_INIT` / `SD_CARD_SLEEP` | 0x1F / 0x20 | Explicit SD power control — see [`../pinouts-and-buses.md` §6](../pinouts-and-buses.md#6-microsd-k11--spi-and-power-switched) |
| `CMD_DRAW_IMAGE_BUFFER` | 0x40 | Push a raw framebuffer |
| `CMD_RTC_IS_SET` / `RTC_RESET` | 0x39 / 0x3A | |

`CMD_GET_REQUEST` and `CMD_CONNECT_WIFI` are notable: a host with no network stack can use the Inkplate as a **Wi-Fi modem plus display**, which makes it far more useful to a small MCU than the old protocol suggested.

Slots `0x0045`–`0x0047` are reserved-but-commented in `commandList.h`.

---

## Old protocol (as documented by the vendor)

Everything below describes the **old** `#<op>(<args>)*` format from Soldered's `peripheral-mode.rst`. Retained because it is what the official documentation still shows, and because units running older firmware will speak it.

## Command reference

### Diagnostics

| Command | Syntax | Notes |
|---|---|---|
| echo | `#?*` | Returns `OK`. **Use this first.** |
| getPanelState | `#R(?)*` | |
| readTemperature | `#N(?)*` | From the on-board NTC — e-paper waveforms are temperature-dependent |
| readBattery | `#P(?)*` | |
| readTouchpad | `#O(P)*` | Older ("e-Radionica", blue) boards only — see [§ board generations](#board-generations) |

### Drawing primitives

| Command | Syntax |
|---|---|
| drawPixel | `#0(XXX,YYY,CC)*` |
| drawLine | `#1(XXX,YYY,III,JJJ,CC)*` |
| drawFastVLine | `#2(XXX,YYY,LLL,CC)*` |
| drawFastHLine | `#3(XXX,YYY,LLL,CC)*` |
| drawRect | `#4(XXX,YYY,WWW,HHH,CC)*` |
| drawCircle | `#5(XXX,YYY,RRR,CC)*` |
| drawTriangle | `#6(XX1,YY1,XX2,YY2,XX3,YY3,CC)*` |
| drawRoundRect | `#7(XXX,YYY,WWW,HHH,RRR,CC)*` |
| fillRect | `#8(XXX,YYY,WWW,HHH,CC)*` |
| fillCircle | `#9(XXX,YYY,RRR,CC)*` |
| fillTriangle | `#A(XX1,YY1,XX2,YY2,XX3,YY3,CC)*` |
| fillRoundRect | `#B(XXX,YYY,WWW,HHH,RRR,CC)*` |
| drawThickLine | `#T(XXX,YYY,III,JJJ,TT,CC)*` |
| drawEllipse | `#U(XXX,YYY,RRX,RRY,CC)*` |
| fillEllipse | `#V(XXX,YYY,RRX,RRY,CC)*` |

### Text

| Command | Syntax |
|---|---|
| print | `#C("STRING")*` |
| setTextSize | `#D(NN)*` |
| setCursor | `#E(XXX,YYY)*` |
| setTextWrap | `#F(T/F)*` |
| setRotation | `#G(RRR)*` |

### Images

| Command | Syntax | Notes |
|---|---|---|
| drawBitmap | `#H(XXX,YYY,"PATH")*` | Path on the microSD card |
| drawImage | `#S(XXX,YYY,"PATH")*` | |

### Display control

| Command | Syntax | Notes |
|---|---|---|
| setDisplayMode | `#I(D)*` | 1-bit mono vs 3-bit greyscale |
| getDisplayMode | `#J(?)*` | |
| clearDisplay | `#K(1)*` | Clears the **buffer**, not the panel — still needs `#L(1)*` |
| **display** | **`#L(1)*`** | **Pushes the buffer to the panel** |
| partialUpdate | `#M(YY1,XX2,YY2)*` | Much faster; avoids full-screen flashing |

### Real-time clock (PCF85063A)

| Command | Syntax |
|---|---|
| rtcSetTime | `#W(H,M,S)*` |
| rtcSetDate | `#X(WD,D,M,Y)*` |
| rtcSetEpoch | `#Y(E)*` |
| rtcGetRtcData | `#a(D)*` |
| rtcSetAlarm | `#b(AS,AM,AH,AD,AW)*` |
| rtcSetAlarmEpoch | `#c(AE,AMC)*` |
| rtcCheckAlarmFlag | `#d(?)*` |
| rtcClearAlarmFlag | `#e(1)*` |

The RTC commands make the alarm usable as a **wake source for a host system**, not just for the ESP32 — a nicely-designed detail.

## Worked example

Draw a filled rectangle and a label on an Inkplate 5 Gen 2 (1280 × 720):

```bash
stty -F /dev/ttyUSB0 115200 raw -echo
{
  printf '#K(1)*\n\r'                    # clear buffer
  printf '#8(050,050,300,120,00)*\n\r'   # fillRect x=50 y=50 w=300 h=120 colour=0
  printf '#D(04)*\n\r'                   # text size 4
  printf '#E(070,100)*\n\r'              # cursor
  printf '#C("Hello Inkplate")*\n\r'
  printf '#L(1)*\n\r'                    # <-- REQUIRED: push to panel
} > /dev/ttyUSB0
```

> Status: **`inferred`**, and **for the OLD protocol only**. Assembled from the vendor's documented syntax. Not executed on hardware.
>
> ⚠ **If your unit runs current firmware it will not understand this.** The new protocol equivalent of `drawPixel(1,5,4)` is roughly `TS;A;0;<size>;1;5;4;` — but the exact payload-size accounting was not verified here, so no worked example is offered for the new protocol. Read `InkplatePeripheralMode.cpp::checkPacket()` before writing a client.

**Determining which protocol your unit speaks:** send the old-style `#?*`. If you get `OK`, it is old firmware. Otherwise reflash the `Peripheral_Mode` example from the current library and use the new protocol.

## Restoring peripheral mode

If you have flashed your own firmware and want peripheral mode back:

> Peripheral mode Arduino code for all Inkplates can be found under `examples/Diagnostics` if needed to be installed again.

For the Inkplate 5 family that is in the retained library snapshot at [`artifacts/source-snapshots/Inkplate-Arduino-library/examples/Inkplate5V2/Diagnostics/`](../artifacts/source-snapshots/Inkplate-Arduino-library/examples/Inkplate5V2/).

## Board generations

`readTouchpad` (`#O(P)*`) only works on **older, e-Radionica-branded** boards. Soldered's own comparison:

| Feature | Older (e-Radionica) | Newer (Soldered) |
|---|---|---|
| Board definition | `e-Radionica Inkplate` | `Soldered Inkplate` |
| Board colour | **Blue** (usually) | **Purple** |
| Capacitive touchpads | **Yes** | **No** |
| GPIO expander | **MCP23017** | **PCAL6416A** |

So: **if your Inkplate is blue, it is a pre-rebrand board with touchpads and an MCP23017.** If it is purple, it is a Soldered-era board with no touchpads and a PCAL6416A. Soldered states there is no functional difference between the expanders for end users, and that all boards remain supported by the current library.

The Inkplate 5 and 5 Gen 2 are both **Soldered-era** (PCAL6416A, no touchpads) — they were never sold under the e-Radionica brand.

## Related

- [`../README.md`](../README.md) — Inkplate 5 / Gen 2 hardware
- [ZeroWriter Ink](../../../zerowriter/zerowriter-ink/README.md) — writes its own firmware rather than using peripheral mode
- [Soldered vendor guide](../../../../vendors/soldered-electronics/README.md) — including the readthedocs → soldered.com documentation migration
