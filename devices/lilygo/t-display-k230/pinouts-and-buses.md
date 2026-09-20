# T-Display K230 — pinouts, buses and addresses

**All tables below are reproduced from LilyGO's own `k230_bsp/docs/HARDWARE_PINMAP.md` at commit
`bb831ab358b66f5bd9a87ecd7c580fee4537492e` (2026-09-03) unless a different source is named.**
That document is the board's authoritative pin map; there is **no published schematic** to
cross-check it against ([`GC-5`](gaps-and-conflicts.md)). Where the Canaan reference device tree
adds detail, it is cited as `C3`.

Evidence status for every row here: **`reported-working`** — LilyGO states these are the
assignments its shipped BSP uses, and the corresponding device-tree patches exist in the same
repository. **None has been verified against hardware.**

---

## 1. 40-pin expansion header (2 × 20)

Orientation: **USB-C facing down; the left column below is the physical left side.**

| Left | Right |
|---|---|
| `ADC0` | `ADC2` |
| `ADC1` | `GND` |
| `GPIO47` | `GPIO43` |
| `GPIO14` | `GPIO46` |
| `GPIO17` | `GPIO18` |
| `GPIO53` | `GPIO52` |
| `GPIO33` | `GPIO62` |
| `GPIO34` | `GPIO32` |
| `GPIO29` | `GPIO31` |
| `GPIO28` | `GPIO30` |
| `GPIO6` | `GPIO26` |
| `GPIO3` | `GPIO5` |
| `GPIO63` | `GPIO27` |
| `GPIO35` | `GPIO4` |
| `GPIO45` | `GPIO2` |
| `GPIO44` | `GPIO42` |
| `GPIO15` | `GPIO16` |
| `GPIO19` | `GPIO20` |
| `5V` | `3V3` |
| `GND` | `USB-IN-5V` |

**The header is not "spare I/O".** Read it against §2 and §3: `GPIO14/15/16/17/19/20/44` are the
LoRa SPI, `GPIO3/4` are the nRF52840 UART, `GPIO28/29` are the nRF9151 UART, `GPIO2` is the
nRF9151 enable, `GPIO42/43` are the keyboard IRQ and reset, `GPIO46/47` are the shared I²C4 bus,
`GPIO32/33/34/35` are the I²S path, and `GPIO52` is the keyboard backlight PWM. **The base
boards plug into this header and claim most of it.** Genuinely uncommitted pins are
`GPIO6`, `GPIO18`, `GPIO26`, `GPIO27`, `GPIO30`, `GPIO31`, `GPIO45`, `GPIO53`, `GPIO62`,
`GPIO63`, plus `ADC0/1/2`.

Three analogue inputs (`ADC0`, `ADC1`, `ADC2`) are exposed. The K230 datasheet does not
enumerate an ADC in its peripheral list, so their electrical characteristics are **unknown**
([`GC-8`](gaps-and-conflicts.md)).

---

## 2. K230 main board

| Function | K230 signal | Dir | Peripheral signal | Notes |
|---|---|---|---|---|
| BOOT0 button | `GPIO0` | in | button | **Idle high, pressed low.** The launcher repurposes it as a screen/backlight toggle. |
| PMU INT0 / power key | `GPIO64` | PMU in | PMU input channel 0 | **Not a normal GPIO.** **Idle low, pressed high** — inverted relative to BOOT0. Reaches userspace through the `k230-pmu-pwrkey` input driver. |
| RM69A10 AMOLED | `GPIO22` | out | panel **reset** | Used by both the U-Boot logo path and Linux bring-up |
| RM69A10 AMOLED | `GPIO25` | out | panel **enable** | Boot logo + launcher backlight/display enable |
| RM69A10 AMOLED | MIPI DSI | out | display data | Default output. **Validated LVGL path is RGB565.** |
| GT9895 touch | `GPIO37` | I²C SDA | touch SDA | ⚠ shared with LT9611 |
| GT9895 touch | `GPIO36` | I²C SCL | touch SCL | address **`0x5D`** |
| GT9895 touch | `GPIO23` | in | touch IRQ | ⚠ shared with LT9611 IRQ |
| GT9895 touch | `GPIO24` | out | touch reset | ⚠ shared with LT9611 reset |
| LT9611 HDMI bridge | `GPIO37`/`GPIO36`/`GPIO23`/`GPIO24` | — | SDA/SCL/IRQ/RST | **Optional path.** Same four lines as touch. |
| GC2093 camera | `GPIO49` | I²C SDA | camera SDA | address **`0x37`** |
| GC2093 camera | `GPIO48` | I²C SCL | camera SCL | |
| GC2093 camera | MIPI CSI | in | camera data | preview, capture, RTSP, AI camera |
| microSD | `GPIO54` | SDIO CMD | SD CMD | **boot + storage** |
| microSD | `GPIO55` | SDIO CLK | SD CLK | |
| microSD | `GPIO56`…`GPIO59` | SDIO D0–D3 | SD D0–D3 | |
| Wi-Fi | SDIO | I/O | RTL8189FS or RTL8723DS | "RTL8723DS Bluetooth requires separate BT UART hardware signals; **SDIO covers Wi-Fi only**" |
| USB host | USB | I/O | USB Ethernet, USB modem, USB Bluetooth | root filesystem carries the drivers |
| LoRa | `GPIO16` | SPI MOSI | MOSI | |
| LoRa | `GPIO17` | SPI MISO | MISO | |
| LoRa | `GPIO15` | SPI SCLK | SCK | |
| LoRa | `GPIO14` | out | CS | |
| LoRa | `GPIO5` | out | RESET | driven by the RadioLib HAL |
| LoRa | `GPIO19` | in | BUSY | |
| LoRa | `GPIO20` | in | IRQ | **SX1262 → `DIO1`; LR2021 → `DIO11`.** Same K230 pin, different radio pin. |
| LoRa | `GPIO44` | out | power enable | enables the module's power path |

---

## 3. nRF52840 BLE / audio / sensor base board

| Base-board function | Base signal | K230 signal | Dir from K230 | Notes |
|---|---|---|---|---|
| nRF52840 UART | `P0.11` / Arduino 11 (RX) | `GPIO3` / UART1 TX | out | K230 → nRF52840, `/dev/ttyS1`, **115200 8N1** |
| nRF52840 UART | `P0.12` / Arduino 12 (TX) | `GPIO4` / UART1 RX | in | AT responses and BLE events |
| nRF52840 LED | `P1.00` / Arduino 32 | — | (nRF out) | blue activity LED on the nRF52840 board |
| **5 V boost enable** | `P0.04` / Arduino 4 | — | (nRF out) | **Boosts the 21700 battery compartment to a stable 5 V for the host unit.** Source: the nRF52840 firmware README, not the pin map. |
| nRF52840 debug | USB CDC | host PC | I/O | 115200; **some monitors need DTR asserted** |
| AHT20 | SCL | `GPIO46` / I²C4 SCL | I²C | **`0x38`** |
| AHT20 | SDA | `GPIO47` / I²C4 SDA | I²C | shared expansion bus |
| MAX98357A | `DIN` | `GPIO35` / I²S data | out | |
| MAX98357A | `BCLK` | `GPIO32` / I²S BCLK | out | |
| MAX98357A | `LRCK`/`WS` | `GPIO33` / I²S LRCK | out | |
| MAX98357A | shutdown | `GPIO34` | out | **high = enabled** |

---

## 4. nRF9151 cellular / GNSS / keyboard base board

| Base-board function | Base signal | K230 signal | Dir from K230 | Notes |
|---|---|---|---|---|
| nRF9151 enable | power enable | `GPIO2` | out | **drive high to enable** |
| nRF9151 UART1 | `P0.26` / RX1 | `GPIO28` / UART3 TX | out | `/dev/ttyS3`, **115200 8N1, no flow control** |
| nRF9151 UART1 | `P0.27` / TX1 | `GPIO29` / UART3 RX | in | AT responses + URCs |
| nRF9151 debug UART2 | `P0.29` / TX2 | external USB-UART RX | (nRF out) | optional Serial LTE Modem log |
| nRF9151 debug UART2 | `P0.28` / RX2 | external USB-UART TX | (nRF in) | optional |
| nRF9151 LED | `P0.23` | — | (nRF out) | blue LED **inside the PCB**; GNSS fix → 1 s cadence, ~300 ms on |
| BQ25896 charger | SCL/SDA | `GPIO46`/`GPIO47` | I²C4 | **`0x6B`** |
| BQ27220 gauge | SCL/SDA | `GPIO46`/`GPIO47` | I²C4 | **`0x55`** |
| TCA8418 keyboard | SCL/SDA | `GPIO46`/`GPIO47` | I²C4 | **`0x34`** (7-bit, as Linux uses it) |
| TCA8418 keyboard | RESET | `GPIO43` | out | |
| TCA8418 keyboard | IRQ | `GPIO42` | in | |
| XL9555 expander | SCL/SDA | `GPIO46`/`GPIO47` | I²C4 | **`0x20`–`0x27`; software probes and caches** |
| Keyboard backlight | PWM | `GPIO52` / **PWM4** | out | userspace drives brightness |

---

## 5. I²C address map

| Bus | K230 pins | 7-bit addr | Device | Board |
|---|---|---|---|---|
| I²C0 | `GPIO48` SCL / `GPIO49` SDA | `0x37` | GC2093 camera | main |
| I²C3 | `GPIO36` SCL / `GPIO37` SDA | `0x5D` | GT9895 touch | main |
| I²C3 | same | ? | LT9611 HDMI bridge (if fitted) | main |
| **I²C4** | `GPIO46` SCL / `GPIO47` SDA | `0x34` | TCA8418 keyboard | nRF9151 base |
| I²C4 | same | `0x38` | AHT20 | nRF52840 base |
| I²C4 | same | `0x55` | BQ27220 gauge | nRF9151 base |
| I²C4 | same | `0x6B` | BQ25896 charger | nRF9151 base |
| I²C4 | same | `0x20`–`0x27` | XL9555 expander | nRF9151 base |

I²C4 is also exposed on the 40-pin header, so **anything you attach there shares a bus with the
keyboard scanner and the power-management chips.** An address collision in `0x20–0x27` is the
most likely accident, because the XL9555's address is not fixed.

The launcher ships an **I²C scanner** (`ui_i2c_scan.c`; v0.2.4 made it asynchronous and
multi-bus) — use it before assuming anything on a board in hand.

---

## 6. IO bank voltages — the hardware-damage path

Canaan's reference device tree (`C3`) sets a `MSC` (voltage) field per bank and carries the
comment:

> `// Please pay attention to the bank voltage! will damage the chip.`

| Bank | Reference-design setting |
|---|---|
| `IO0`–`IO1` | **`K230_MSC_1V8` — FIXED** |
| `IO2`–`IO13` | `K230_MSC_3V3` |
| `IO14`–`IO25` | `K230_MSC_3V3` |
| `IO26`–`IO37` | `K230_MSC_3V3` |
| `IO38`–`IO49` | `K230_MSC_3V3` |
| `IO50`–`IO61` | `K230_MSC_3V3` |
| `IO62`–`IO63` | `K230_MSC_3V3` |

`IO0`/`IO1` are the **BOOT0/BOOT1 strapping pins** and are fixed at 1.8 V. Note that the pin map
describes the **BOOT0 button on `GPIO0`** and the reference DTS configures `IO0` as *output with
pull-up* — the button and the strap are the same pin, which is normal but worth knowing before
attaching anything to it.

---

## 7. UART summary

| Linux device | K230 pins | Peer | Rate |
|---|---|---|---|
| `/dev/ttyS0` | `IO38` TX / `IO39` RX (reference DTS) | console | typically 115200 |
| `/dev/ttyS1` | `GPIO3` TX / `GPIO4` RX | **nRF52840** | 115200 8N1 |
| `/dev/ttyS3` | `GPIO28` TX / `GPIO29` RX | **nRF9151** | 115200 8N1, no flow control |

Enabled by `0060-riscv-dts-rm69a10-enable-uart1-nrf52840.patch` and
`0061-riscv-dts-rm69a10-enable-uart3-nrf9151.patch` respectively.

---

## 8. Keyboard matrix — full decode

Source: `k230_launcher/k230_phone_ui/src/ui_hardware.c`, same commit. Scanner is a
**TCA8418 configured `TCA8418_ROWS 7` × `TCA8418_COLS 10`**; the *displayed* layout is
`KEYBOARD_LAYOUT_ROWS 6` × `KEYBOARD_LAYOUT_COLS 11`. Key code → (row, col) is
`row = (code-1)/10`, `col = (code-1)%10`.

Physical layout as the launcher draws it, by key code:

| | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|
| `50` F1 | `60` F2 | `59` F3 | `68` F4 | `67` F5 | `66` F6 | `65` F7 | `64` F8 | `63` F9 | `62` F10 | `61` F11 |
| `40` ESC | `49` 1 | `48` 2 | `58` 3 | `57` 4 | `56` 5 | `55` 6 | `54` 7 | `53` 8 | `52` 9 | `51` 0 |
| `20` Q | `39` W | `38` E | `37` R | `47` T | `46` Y | `45` U | `44` I | `43` O | `42` P | `41` DEL |
| `10` CAPS | `29` A | `28` S | `27` D | `26` F | `36` G | `35` H | `34` J | `33` K | `32` L | `21` ENTER |
| `19` ALT | `18` Z | `17` X | `16` C | `15` V | `25` B | `24` N | `13` M | `23` CTRL | `22` UP | `11` MIC |
| `9` FN | `8` LILYGO | `7` SHIFT | `6` TAB | `5` SPACE | `14` SPACE | `3` FN-R | `2` LEFT | `12` DOWN | `1` RIGHT | `0` — |

Notes that matter when writing a driver:

- **Two `SPACE` codes** (`5` and `14`) — a wide spacebar spanning two matrix intersections.
- **Two `FN` keys**: `9` (`FN`, left) and `3` (`FN-R`, right). `extension_keyboard_fn_pressed()`
  returns true for either.
- A dedicated **`LILYGO`** key (code `8`) and a dedicated **`MIC`** key (code `11`).
- Code `0` is not a key; TCA8418 key codes are 1-based.
- Only `UP`/`DOWN`/`LEFT`/`RIGHT` arrows exist as codes `22`/`12`/`2`/`1` — arranged in the
  bottom two rows, not as a cluster.
- **11 F-keys**, each remappable: preference key `keyboard.hotkey.f<N>`. Defaults changed in BSP
  v0.2.4 to **F3/F4 = keyboard backlight down/up, F7 = screenshot**.
- `FN+B` toggles the keyboard backlight.
- ESC-as-back is a preference (`keyboard.esc_back`, default on).
- Key repeat: **450 ms** to first repeat, then **85 ms** period.

TCA8418 registers the launcher touches: `CFG 0x01`, `INT_STAT 0x02`, `KEY_LCK_EC 0x03`,
`KEY_EVENT_A 0x04`, `KP_GPIO_1/2/3 0x1D/0x1E/0x1F`, `DEBOUNCE_DIS_1/2/3 0x29/0x2A/0x2B`.
Configuration mode is `KE_IEN | OVR_FLOW_IEN | OVR_FLOW_M` when IRQ mode is enabled
(`K230_TCA8418_USE_IRQ 1`, the default), otherwise `OVR_FLOW_M` alone with polling.

The launcher also **rewrites the K230 IOMUX for `GPIO42` directly** —
`TCA8418_IRQ_IOMUX_IO42_OFFSET (42*4)`, value `0x00000344` — to force it to GPIO input mode.
That is userspace reaching into the pin controller behind the kernel's back, and it is worth
knowing about if you see the IRQ line behave unexpectedly after another driver claims it.

---

## 9. PMU power-key register flow

The `k230-pmu-pwrkey` driver (added by `0064-input-k230-pmu-pwrkey.patch`, 21 523 bytes) states
that its register flow "mirrors the RT-Thread PMU pwrkey driver": route PMU `KEY_EDGE` to
**CPU IRQ 175**, start with rising-edge detection, and on shutdown program INT0 long-press
wakeup and ask the PMU to cut power.

Registers used: `PMU_STATUS 0x3c`, `INT0_TO_CTL 0x40`, `INT1_TO_CTL 0x44`, `INT0_TO_CPU 0x48`,
`INT_DETECT_EN 0x4c`, `INT_DETECT_TYP 0x50`, `INT_DETECT_CLR 0x54`,
`INT0_LONG_PRESS_TRIGGER_VAL 0x58`, `INT0_LEVEL_DEBOUNCE_VAL 0x64`, `SYSCTRL_REG 0x78`,
`OUT_EVENT_CTRL 0xa4`, `OUT_LOGIC_CTRL 0xa8`, `INT_STATE_REG 0xac`, and
`PWR_PMU_PWR_ISO_CTRL_REG 0x158`. Node address `pmu-pwrkey@91000000`, `reg-names = "pmu", "pwr"`.

Launcher-side constants: long-press `96000` ticks, debounce `256` ticks.

Canaan's `K230_PMU_User_Guide.md` is retained at
[`components/canaan/k230/artifacts/K230_PMU_User_Guide.md`](../../../components/canaan/k230/artifacts/K230_PMU_User_Guide.md).
