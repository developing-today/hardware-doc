# T-Display-S3 — resources, ownership and conflicts

## GPIO budget

45 GPIOs on the ESP32-S3; **7 genuinely free** on this board. Derivation:
[`features/gpio-and-expansion.md`](features/gpio-and-expansion.md).

| Owner | Pins | Releasable? |
|---|---|---|
| OPI PSRAM (in package) | 26–37 | **No.** Physically bonded |
| LCD 8080 bus | 5,6,7,8,9,39,40,41,42,45,46,47,48 | only by not using the display |
| Backlight | 38 | no |
| `V3V` gate | 15 | no |
| Native USB | 19,20 | only by not using USB |
| UART0 | 43,44 | in ESP-IDF via `sdkconfig`; **not in Arduino** |
| Battery sense | 4 | yes, at the cost of all battery monitoring |
| Buttons | 0,14 | 14 yes; 0 is the strap/BOOT pin |
| I²C + fitted pull-ups | 17,18 | pull-ups are soldered |
| Touch IRQ/RST | 16,21 | **16 has a fitted pull-up even without touch** |
| **Free** | **1,2,3,10,11,12,13** | 11/12/13 lost to the TF Shield |

## Peripheral ownership

| Peripheral | Owner | Contention |
|---|---|---|
| **LCD_CAM (i80)** | the display, exclusively | one unit; nothing else can use it |
| **ADC1** | battery sense on ch3 (GPIO4) | other analogue inputs must also be ADC1 (GPIO1–10) |
| **ADC2** | — | **unusable while Wi-Fi is on.** Silicon limitation |
| **I²C0** | touch controller + the SH1.0 connector | one bus, shared |
| **UART0** | `Serial` when `USB CDC On Boot` is off | GPIO43/44 |
| **USB-Serial-JTAG** | `Serial` + flashing + JTAG when `ARDUINO_USB_MODE=1` | **mutually exclusive with TinyUSB device roles** |
| **SDMMC (1-bit)** | TF Shield only | GPIO11/12/13 |
| **Radio** | Wi-Fi and BLE time-share one radio | throughput roughly halves when both are active |
| **GDMA** | one channel per active LCD/SD transfer | ample |

## Memory

| Resource | Size | Notes |
|---|---|---|
| Internal SRAM | 512 KB (`maximum_ram_size 327680` usable per the board manifest) | |
| PSRAM | **8 MB, OPI, in package** | **requires `PSRAM = OPI PSRAM`.** Wrong setting = silently absent |
| Flash | 16 MB, W25Q128JV, QIO 80 MHz | |
| Default partitions | `default_16MB.csv` → app0/app1 6 400 KB each, SPIFFS 3 456 KB, coredump 64 KB | |
| Vendor Arduino partition | `16M Flash (3M APP/9.9MB FATFS)` | different from the PlatformIO default — a source of "it fits in PlatformIO but not Arduino" |
| Full framebuffer | 170×320×2 = **108.8 KB** | LVGL double-buffered full-height = 217.6 KB → PSRAM territory |

## Power budget

| Rail | Limit | Enforced by |
|---|---|---|
| Header `3V` | **100 mA** | vendor statement |
| Header `VBUS` 5 V | your USB supply | output only |
| Battery charge | 500 mA (README) / 580 mA (schematic) | soldered resistor |
| Battery discharge | unprotected | **use a protected cell** |

## Realistic feature combinations

| Combination | Works? | Cost |
|---|---|---|
| Display + Wi-Fi | yes | ~90–230 mA class current; framebuffer in PSRAM |
| Display + Wi-Fi + BLE | yes | radio time-shared; expect jitter in UI updates driven by network events |
| Display + touch + I²C sensor | yes | one bus; watch pull-up stacking and CST NAK behaviour |
| Display + TF Shield + Wi-Fi | yes | GPIO11/12/13 gone; only GPIO1/2/3/10 remain |
| Display + battery monitoring | yes | GPIO4 permanently spoken for; **reads 2.5 V whenever USB is attached** |
| Display + USB HID | yes, in **USB-OTG** mode | **loses built-in JTAG debugging** |
| Deep sleep + touch wake | **partial** | the touch controller is on the GPIO15-gated rail; keeping it alive costs sleep current |
| Battery operation + USB serial logging | **no** | `USB CDC On Boot` must be off for reliable battery boot, which moves `Serial` to GPIO43/44 |
| I²S audio + display | reported difficult — [issue #158](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/158) | pins are scarce; no codec fitted |

## Boot straps

| Pin | Strap | Board use | Risk |
|---|---|---|---|
| 0 | boot mode | BOOT button | pressing it during reset enters download mode |
| 3 | JTAG source | free | leave floating |
| 45 | `VDD_SPI` voltage | **LCD_D4** | driven only after boot; do not load the pin |
| 46 | boot config | **LCD_D5** | as above |
