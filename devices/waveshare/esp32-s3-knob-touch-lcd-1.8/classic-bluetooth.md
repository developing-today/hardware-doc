# Classic Bluetooth on this board

Retrieved 2026-08-21; firmware and schematic analysis 2026-08-22.

> **The short version:** Bluetooth Classic (BR/EDR) works on this board, but **only from the secondary [ESP32-U4WDH](../../../components/espressif/esp32-u4wdh/README.md) MCU**. The main ESP32-S3 physically cannot do it. Reaching the secondary MCU means flipping the USB-C plug over and flashing a second, separate firmware image. If you are trying to make Classic Bluetooth work from an S3 sketch, you are on the wrong chip and no amount of library hunting will fix it.

## Why the ESP32-S3 cannot do this

The ESP32-S3 has a **Bluetooth LE 5 radio only**. There is no BR/EDR baseband in the silicon. This is not a fuse, a licensing restriction or a missing driver — the hardware is not there. No ESP-IDF version, no Arduino-ESP32 core version and no third-party library can add it.

The chip-level treatment — datasheet evidence, the full list of unavailable profiles, what LE alternatives do and do not replace, which Espressif parts have BR/EDR, and the design workarounds of which this board is one — is in [the ESP32-S3R8 component page](../../../components/espressif/esp32-s3r8/README.md#radio-capabilities-and-the-classic-bluetooth-limitation).

The usual way people discover this is a compile error: `BluetoothSerial.h` in Arduino-ESP32 refuses to build for `esp32s3` with a message to the effect that Bluetooth Classic is not enabled or not available. That message is accurate and final.

Bluetooth **audio** as normally understood is a BR/EDR profile stack:

| Profile | What it does | BR/EDR? |
|---|---|---|
| A2DP | Streams stereo music | **Yes** |
| AVRCP | Play/pause/next/prev, volume, track metadata, album art | **Yes** |
| HFP / HSP | Hands-free calls, mic audio | **Yes** |
| SPP | Bluetooth serial port | **Yes** |
| Classic HID | Keyboards, mice, media-key remotes | **Yes** |
| GATT / BLE HID / BLE audio (LE Audio) | LE-only profiles | No — S3 can do these |

Since this product is a Bluetooth media knob, Waveshare had no choice but to add a second chip.

## What the secondary MCU actually provides

Reference designator `U14`, part `ESP32-U4WDH` — an original-series ESP32 with a BR/EDR + BLE 4.2 radio, its own 40 MHz crystal (`X2`), its own ceramic antenna (`ANT2`) and 4 MB of flash embedded in the package.

The **factory firmware already ships with** the following profiles compiled in. This is not speculation — these are symbols and log strings extracted from `ESP32-KNOB_ESP32_0.bin`:

| Role | Evidence |
|---|---|
| **A2DP sink** — the board is a Bluetooth speaker | `btc_a2dp_sink_thread_init`, `Advanced Audio Sink` |
| **A2DP source** — the board streams audio out | `btc_a2dp_source_aa_start_tx`, `btc_media_aa_prep_sbc_2_send` |
| **AVRCP controller (CT)** — the knob sends play/pause/next and absolute volume | `btc_avrc_ct_send_passthrough_cmd`, `btc_avrc_ct_send_set_absolute_volume_cmd` |
| **AVRCP target (TG)** | `btc_avrc_tg_init`, `btc_avrc_tg_send_rn_rsp` |
| **AVRCP Cover Art (OBEX/BIP)** — fetches album artwork | `btc_avrc_ct_cover_art_get_image`, `obex_main.c` |
| **SPP** | `SPP` |
| **Classic HID device** | `BT_HIDD`, `bt_hid_device_init` |
| **BLE HID device** | `BLE_HIDD`, `esp_ble_hidd_dev_feature_set` |
| Host stack | Bluedroid |

The album art path is the interesting one: the ESP32 pulls JPEG artwork over Bluetooth, then ships it across the internal UART in numbered packets for the ESP32-S3 to decode and draw on the round LCD.

The Bluetooth device name is very likely **`BTAUDIOMATE`** — that string is present in the image, but with no surrounding context proving its use, so scan for the device from a phone to confirm.

Bluetooth pairing state is stored in the ESP32's own NVS partition under the key `PEERADDR`. The S3's UI has a "Clear BT A2DP pair" action which must relay that request over the UART.

## What this costs you

Practical consequences of the split that people trip over:

1. **Two firmwares, always.** Nothing you flash to the S3 affects Bluetooth Classic behaviour, and vice versa. See [factory firmware and restore](factory-firmware.md).
2. **The screen is on the other chip.** The ESP32-U4WDH has no access to the LCD, touch panel, SD card, microphone or haptics — none of them are wired to it. Anything it wants to display must be sent over the [inter-MCU UART](README.md#the-inter-mcu-uart-bridge), whose protocol is **undocumented**.
3. **Only knob 2 is readable from the Bluetooth chip.** `SW1`/`EC2` (GPIO19/22) is the U4WDH's; `SW2`/`EC1` belongs to the S3. And there is **no push/press contact** wired from `SW1` to the U4WDH — rotation only.
4. **Audio needs both chips.** The S3 owns the CH445P mux select; the U4WDH owns the DAC mute. Neither can produce sound alone. See [shared audio output](README.md#shared-audio-output-and-why-it-needs-arbitration).
5. **No native USB on the Bluetooth chip.** You cannot make this board a USB HID device *and* a Bluetooth Classic device from the same MCU. USB HID would have to come from the S3.
6. **BLE 4.2, not 5.** The U4WDH's LE side has no coded PHY, no 2 M PHY, no extended advertising. If you want BLE 5 features, use the S3's radio instead — both radios can run simultaneously, they are independent.
7. **Tight resources.** 4 MB flash total, 520 KB SRAM, **no PSRAM**. The factory app with A2DP + AVRCP + SPP + HID enabled is already about 1 MB.
8. **Possibly single-core at 160 MHz.** See the caveat below. This one genuinely matters for A2DP + SBC decode headroom.

## ⚠ Before you write code: check the core count

Espressif PCN-2021-021 records that the ESP32-U4WDH was a **single-core, 160 MHz** part before 2021-12-02 and dual-core afterwards. **Nothing in Waveshare's documentation says which one is fitted to your board**, and the factory firmware runs on both.

Bluetooth Classic A2DP with SBC decode is not a light workload. If you are on the single-core variant, the radio stack and your application share one 160 MHz core.

Check it before you design around it:

~~~c
#include "esp_chip_info.h"
esp_chip_info_t info;
esp_chip_info(&info);
ESP_LOGI(TAG, "cores=%d rev=%d", info.cores, info.revision);
~~~

or, without flashing anything, `esptool --port PORT chip_id`. Full detail and the eFuse route are in [the component page's core-count section](../../../components/espressif/esp32-u4wdh/README.md#2--the-core-count-and-clock-speed-caveat-unresolved).

Write code that survives either answer: avoid unconditional `APP_CPU_NUM` affinity, and do not budget CPU on the assumption of 240 MHz.

## Building it

### 1. Connect to the right MCU

Plug in USB-C, then:

~~~sh
esptool --port PORT chip_id
~~~

If it reports **ESP32-S3**, unplug, **rotate the plug 180°**, and reconnect. You want `Chip is ESP32-U4WDH`. This is the number-one source of wasted time on this board.

### 2. Back up first

The factory Bluetooth firmware is the only copy of `TAIJI_KNOB_32` you will ever have in its installed state, and its NVS holds your pairings:

~~~sh
esptool --chip esp32 --port PORT --baud 921600 read_flash 0x0 0x400000 esp32-u4wdh-backup.bin
~~~

The shipped image is also archived locally — see [factory firmware and restore](factory-firmware.md).

### 3. ESP-IDF

Target is **`esp32`**, not `esp32s3`:

~~~sh
idf.py set-target esp32
idf.py menuconfig
~~~

In menuconfig:

```
Component config → Bluetooth → [*] Bluetooth
  → Bluetooth controller → mode → BR/EDR Only   (or Bluetooth Dual Mode)
  → Bluetooth Host → Bluedroid - Dual-mode      (NimBLE cannot do Classic)
  → Bluedroid Options → [*] Classic Bluetooth
      → [*] A2DP  (sink and/or source)
      → [*] AVRCP
      → [*] SPP
      → [*] Classic BT HID Device
```

Start from Espressif's own examples in `esp-idf/examples/bluetooth/bluedroid/classic_bt/` — `a2dp_sink`, `a2dp_source`, `bt_spp_acceptor`, `bt_discovery` — and `examples/bluetooth/esp_hid_device`.

Board-specific pin configuration for the I2S output:

| Signal | GPIO | Note |
|---|---:|---|
| BCLK | 25 | |
| WS / LRCK | 27 | |
| DOUT | 26 | |
| MCLK | — | **must be disabled** — no MCLK is routed to the DAC |
| DAC mute `XSMT` | 32 | **drive high to un-mute**, low to mute |

Mute the DAC (GPIO32 low) before starting or stopping I2S clocks, or you will get a click.

### 4. Arduino

Select **"ESP32 Dev Module"**, not "ESP32S3 Dev Module".

| Library | Use |
|---|---|
| `BluetoothSerial` (bundled) | SPP, one include |
| `ESP32-A2DP` (pschatzmann) | A2DP sink/source with I2S output — the usual route to "Bluetooth speaker" |
| `arduino-audio-tools` (pschatzmann) | Fuller audio pipeline; pairs with the above |
| `BLEDevice` / `NimBLE-Arduino` | BLE 4.2 |

### 5. ESP-ADF

If you want a proper element-graph audio pipeline (`bluetooth_service` → `a2dp_stream` → decoder → `i2s_stream_writer`) rather than hand-rolled ring buffers, ESP-ADF is the framework and this is the chip for it — ADF's Bluetooth pipelines target the original ESP32 precisely because that is the chip with BR/EDR. The programming guide is archived at `components/espressif/esp32-u4wdh/artifacts/esp-adf-programming-guide.pdf`.

Note the factory firmware does **not** use ADF; it drives I2S directly from the A2DP callback through its own ring buffer, i.e. the plain `a2dp_sink` example structure.

## If you reflash the U4WDH and lose all audio

This is a known trap. The PCM5100A's `XSMT` mute pin is driven **only** by U4WDH GPIO32, with no pull resistor. If your replacement firmware never drives GPIO32 high, the DAC stays muted — **including for audio coming from the ESP32-S3**, which has no way to un-mute it.

Drive GPIO32 high early in your ESP32 firmware, even if your application does not otherwise care about audio, unless you deliberately want the output muted.

(Related open question: how Waveshare's S3-only `07_Audio_Test` example gets past this at all is not established. See [gaps and conflicts](gaps-and-conflicts.md).)

## Doing it yourself, end to end

If you are building a custom product on this board rather than modifying the stock behaviour, the sane approach is:

1. Reflash **both** MCUs with your own firmware.
2. Define **your own** inter-MCU UART protocol — the stock one is undocumented and you gain nothing by reverse-engineering it if you control both ends.
3. Put Bluetooth Classic, the audio pipeline, `XSMT` and knob 2 on the U4WDH.
4. Put the GUI, touch, SD, microphone, haptics, knob 1 and the CH445P mux select on the S3.
5. Carry transport commands, track metadata, artwork and audio-path handshakes over your UART.

That is essentially the architecture Waveshare shipped, and it is the one the hardware forces.

**Budget the link realistically.** It is full duplex with no hardware flow control, so software flow control is mandatory; at 8N1 you get `baud/10` bytes per second, with a 5 Mbaud silicon ceiling. Metadata and album-art JPEGs fit comfortably; audio and video do not, which is exactly why the board routes audio through the CH445P analog mux instead. Full arithmetic in [Dual-MCU architecture §2.3](dual-mcu-architecture.md#23-bandwidth--what-this-link-can-and-cannot-carry).

## Related

- [ESP32-U4WDH component page](../../../components/espressif/esp32-u4wdh/README.md) — full pin table, firmware analysis, APIs, open questions
- [Dual-MCU architecture](dual-mcu-architecture.md) — the orientation flip, the inter-MCU link's bandwidth and protocol, the ownership table, OTA capability, backup/restore
- [Pinouts and buses](pinouts-and-buses.md)
- [Factory firmware and restore](factory-firmware.md) — including how to reset pairing by erasing NVS
- [Development and examples](development.md)
- [Gaps and conflicts](gaps-and-conflicts.md)
- [Espressif vendor sourcing guide](../../../vendors/espressif/README.md)
